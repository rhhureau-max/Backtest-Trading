#!/usr/bin/env python3
"""
PBTrading Silver Bullet & IFVG Backtest Strategy V2 for NQ Futures

UPDATED CONDITIONS:
- Liquidity sweep on 15m timeframe (looking for swing high/low within 50 candles)
- Wait for FVG creation on 5m timeframe and its violation to become IFVG
- Entry when price closes having filled/tested the IFVG
- Two SL options: under the candle that filled the FVG OR under the IFVG
- Multiple RR targets: 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5
"""

import os
import zipfile
from datetime import datetime, time
from typing import Optional, Tuple, List

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from backtesting import Backtest, Strategy


# =============================================================================
# CONSTANTS
# =============================================================================

TRADING_DAYS_PER_YEAR = 252
MINUTES_PER_TRADING_DAY = 390
SWEEP_LOOKBACK_15M = 50  # 50 candles lookback for 15m sweep
SWEEP_VALIDITY_BARS_1M = 75  # 15m * 5 = 75 bars validity window in 1m
FVG_LOOKBACK = 100  # Bars to keep FVG tracking
INFINITE_PROFIT_FACTOR = 999.0


# =============================================================================
# DATA LOADING AND CLEANING
# =============================================================================

def _parse_ohlcv_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Convert raw CSV data to OHLCV DataFrame with datetime index."""
    df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], dayfirst=True)
    df.set_index('Datetime', inplace=True)
    df = df[['Open', 'High', 'Low', 'Close', 'Volume']].astype(float)
    return df


def load_csv_data(filepath: str) -> pd.DataFrame:
    """Load semicolon-separated CSV data."""
    df = pd.read_csv(
        filepath,
        sep=';',
        names=['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume'],
        skiprows=1,
        encoding='utf-8-sig'
    )
    return _parse_ohlcv_dataframe(df)


def load_from_zip(zip_path: str) -> pd.DataFrame:
    """Extract and load CSV from zip file."""
    with zipfile.ZipFile(zip_path, 'r') as z:
        csv_name = z.namelist()[0]
        with z.open(csv_name) as f:
            df = pd.read_csv(
                f,
                sep=';',
                names=['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume'],
                skiprows=1,
                encoding='utf-8-sig'
            )
    return _parse_ohlcv_dataframe(df)


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Remove holidays, empty data, and clean the dataset."""
    df = df.dropna()
    df = df[(df['Volume'] > 0) & (df['Close'] > 0)]
    
    daily_volume = df.groupby(df.index.date)['Volume'].sum()
    avg_volume = daily_volume.mean()
    low_volume_days = daily_volume[daily_volume < avg_volume * 0.1].index
    low_volume_dates = pd.DatetimeIndex(low_volume_days).normalize()
    df = df[~df.index.normalize().isin(low_volume_dates)]
    
    return df.sort_index()


def load_data(data_dir: str, year: int, timeframe: str = '1m') -> pd.DataFrame:
    """Load data for a specific year and timeframe."""
    if timeframe == '1m':
        csv_path = os.path.join(data_dir, f'{year} 1m.csv')
        zip_path = os.path.join(data_dir, f'{year} 1m.csv.zip')
        
        if os.path.exists(csv_path):
            return load_csv_data(csv_path)
        elif os.path.exists(zip_path):
            return load_from_zip(zip_path)
    else:
        csv_path = os.path.join(data_dir, f'{year} {timeframe}.csv')
        if os.path.exists(csv_path):
            return load_csv_data(csv_path)
    
    raise FileNotFoundError(f"Data file not found for {year} {timeframe}")


def resample_to_timeframe(df_1m: pd.DataFrame, timeframe: str) -> pd.DataFrame:
    """Resample 1-minute data to specified timeframe."""
    return df_1m.resample(timeframe).agg({
        'Open': 'first',
        'High': 'max',
        'Low': 'min',
        'Close': 'last',
        'Volume': 'sum'
    }).dropna()


# =============================================================================
# MULTI-TIMEFRAME INDICATOR CALCULATIONS
# =============================================================================

class MTFIndicators:
    """Multi-Timeframe Indicators for the strategy."""
    
    def __init__(self, df_1m: pd.DataFrame):
        """Initialize with 1-minute data."""
        self.df_1m = df_1m
        self.df_5m = resample_to_timeframe(df_1m, '5min')
        self.df_15m = resample_to_timeframe(df_1m, '15min')
        
        # Pre-calculate 15m fractal levels (50 candle lookback)
        self.fractal_high_15m = self.df_15m['High'].rolling(
            window=SWEEP_LOOKBACK_15M, min_periods=SWEEP_LOOKBACK_15M
        ).max()
        self.fractal_low_15m = self.df_15m['Low'].rolling(
            window=SWEEP_LOOKBACK_15M, min_periods=SWEEP_LOOKBACK_15M
        ).min()
        
    def get_15m_fractal_at_time(self, dt) -> Tuple[Optional[float], Optional[float]]:
        """Get the 15m fractal high/low valid at a given datetime."""
        # Find the 15m bar that contains this datetime
        mask = self.df_15m.index <= dt
        if not mask.any():
            return None, None
        
        idx = self.df_15m.index[mask][-1]
        loc = self.df_15m.index.get_loc(idx)
        
        if loc > 0:
            # Use the previous completed bar's fractal
            fractal_high = self.fractal_high_15m.iloc[loc - 1]
            fractal_low = self.fractal_low_15m.iloc[loc - 1]
            return fractal_high, fractal_low
        return None, None
    
    def check_15m_sweep(self, dt, current_high: float, current_low: float, 
                        current_close: float) -> Tuple[bool, bool]:
        """
        Check if current bar creates a liquidity sweep on 15m level.
        
        Returns:
            (buy_side_sweep, sell_side_sweep)
        """
        fractal_high, fractal_low = self.get_15m_fractal_at_time(dt)
        
        if fractal_high is None or fractal_low is None:
            return False, False
        
        if np.isnan(fractal_high) or np.isnan(fractal_low):
            return False, False
        
        # Buy-side sweep: high wicks above 15m fractal high, close below
        buy_side_sweep = current_high > fractal_high and current_close < fractal_high
        
        # Sell-side sweep: low wicks below 15m fractal low, close above
        sell_side_sweep = current_low < fractal_low and current_close > fractal_low
        
        return buy_side_sweep, sell_side_sweep


class FVGTrackerV2:
    """
    Enhanced FVG Tracker for V2 strategy.
    
    Tracks FVGs on 5m timeframe:
    - Detects FVG creation
    - Tracks violation (FVG becomes IFVG)
    - Detects IFVG fill (price closes through the IFVG zone)
    """
    
    def __init__(self, lookback: int = FVG_LOOKBACK):
        self.bullish_fvgs = []  # List of active bullish FVGs
        self.bearish_fvgs = []  # List of active bearish FVGs
        self.bullish_ifvgs = []  # Inverted bullish FVGs (now bearish zones)
        self.bearish_ifvgs = []  # Inverted bearish FVGs (now bullish zones)
        self.lookback = lookback
        
    def update(self, idx: int, opens: np.ndarray, highs: np.ndarray,
               lows: np.ndarray, closes: np.ndarray):
        """Update FVG tracking with new bar data (5m timeframe)."""
        if idx < 2:
            return
        
        current_close = closes[idx]
        current_low = lows[idx]
        current_high = highs[idx]
        
        # Check for new FVGs using the 3-bar pattern
        # FVG is the gap between candle[idx-2] and candle[idx]
        bar_minus_2_low = lows[idx - 2]
        bar_minus_2_high = highs[idx - 2]
        
        # Bullish FVG: bar[idx-2].low > bar[idx].high (gap up)
        if bar_minus_2_low > current_high:
            self.bullish_fvgs.append({
                'top': bar_minus_2_low,
                'bottom': current_high,
                'created_idx': idx,
                'violated': False,
                'fill_candle_low': None
            })
        
        # Bearish FVG: bar[idx-2].high < bar[idx].low (gap down)
        if bar_minus_2_high < current_low:
            self.bearish_fvgs.append({
                'top': current_low,
                'bottom': bar_minus_2_high,
                'created_idx': idx,
                'violated': False,
                'fill_candle_high': None
            })
        
        # Check for FVG violations -> creates IFVG
        # Bullish FVG violated when price closes below bottom
        for fvg in self.bullish_fvgs:
            if not fvg['violated'] and current_close < fvg['bottom']:
                fvg['violated'] = True
                # This bullish FVG is now a bearish IFVG (resistance zone)
                self.bullish_ifvgs.append({
                    'top': fvg['top'],
                    'bottom': fvg['bottom'],
                    'created_idx': idx,
                    'filled': False,
                    'fill_candle_low': None
                })
        
        # Bearish FVG violated when price closes above top
        for fvg in self.bearish_fvgs:
            if not fvg['violated'] and current_close > fvg['top']:
                fvg['violated'] = True
                # This bearish FVG is now a bullish IFVG (support zone)
                self.bearish_ifvgs.append({
                    'top': fvg['top'],
                    'bottom': fvg['bottom'],
                    'created_idx': idx,
                    'filled': False,
                    'fill_candle_high': None
                })
        
        # Check for IFVG fills (price closes through the zone)
        # Bullish IFVG (inverted bearish) filled when price closes above top
        for ifvg in self.bearish_ifvgs:
            if not ifvg['filled']:
                # Price enters and closes within/above the zone = fill
                if current_close >= ifvg['bottom']:
                    ifvg['filled'] = True
                    ifvg['fill_candle_high'] = current_high
                    ifvg['fill_idx'] = idx
        
        # Bearish IFVG (inverted bullish) filled when price closes below bottom
        for ifvg in self.bullish_ifvgs:
            if not ifvg['filled']:
                # Price enters and closes within/below the zone = fill
                if current_close <= ifvg['top']:
                    ifvg['filled'] = True
                    ifvg['fill_candle_low'] = current_low
                    ifvg['fill_idx'] = idx
        
        # Clean old entries
        self._cleanup()
    
    def _cleanup(self):
        """Remove old FVGs beyond lookback period."""
        self.bullish_fvgs = [f for f in self.bullish_fvgs if not f['violated']][-self.lookback:]
        self.bearish_fvgs = [f for f in self.bearish_fvgs if not f['violated']][-self.lookback:]
        self.bullish_ifvgs = self.bullish_ifvgs[-self.lookback:]
        self.bearish_ifvgs = self.bearish_ifvgs[-self.lookback:]
    
    def get_filled_bullish_ifvg(self) -> Optional[dict]:
        """Get the most recently filled bullish IFVG for long entry."""
        for ifvg in reversed(self.bearish_ifvgs):
            if ifvg['filled'] and ifvg.get('fill_candle_high') is not None:
                return ifvg
        return None
    
    def get_filled_bearish_ifvg(self) -> Optional[dict]:
        """Get the most recently filled bearish IFVG for short entry."""
        for ifvg in reversed(self.bullish_ifvgs):
            if ifvg['filled'] and ifvg.get('fill_candle_low') is not None:
                return ifvg
        return None


# =============================================================================
# STRATEGY IMPLEMENTATION V2
# =============================================================================

class SilverBulletIFVGStrategyV2(Strategy):
    """
    Silver Bullet + IFVG Trading Strategy V2
    
    Updated conditions:
    - Liquidity sweep on 15m (50 candle lookback)
    - FVG creation on 5m, violated to become IFVG
    - Entry when price fills the IFVG
    - SL options: under fill candle OR under IFVG
    """
    
    fractal_lookback = 50  # For 15m sweep detection
    rr_target = 2.0
    use_break_even = True
    sl_type = 'fill_candle'  # 'fill_candle' or 'ifvg'
    
    def init(self):
        """Initialize indicators and tracking variables."""
        # We'll track 5m FVGs using resampled data
        self.fvg_tracker = FVGTrackerV2(lookback=FVG_LOOKBACK)
        
        # Build 5m data from 1m for FVG tracking
        self.data_5m = resample_to_timeframe(
            pd.DataFrame({
                'Open': self.data.Open,
                'High': self.data.High,
                'Low': self.data.Low,
                'Close': self.data.Close,
                'Volume': self.data.Volume if hasattr(self.data, 'Volume') else np.ones(len(self.data.Close))
            }, index=self.data.index),
            '5min'
        )
        
        # Build 15m data for sweep detection
        self.data_15m = resample_to_timeframe(
            pd.DataFrame({
                'Open': self.data.Open,
                'High': self.data.High,
                'Low': self.data.Low,
                'Close': self.data.Close,
                'Volume': self.data.Volume if hasattr(self.data, 'Volume') else np.ones(len(self.data.Close))
            }, index=self.data.index),
            '15min'
        )
        
        # Pre-calculate 15m fractal levels
        self.fractal_high_15m = self.data_15m['High'].rolling(
            window=self.fractal_lookback, min_periods=self.fractal_lookback
        ).max()
        self.fractal_low_15m = self.data_15m['Low'].rolling(
            window=self.fractal_lookback, min_periods=self.fractal_lookback
        ).min()
        
        # Track sweep signals
        self.last_buy_sweep_time = None
        self.last_sell_sweep_time = None
        
        # Track current 5m bar index for FVG updates
        self.last_5m_idx = -1
        
        # Entry tracking
        self.entry_price = None
        self.stop_loss = None
        self.take_profit = None
        self.breakeven_activated = False
        self.current_ifvg = None
        
    def is_trading_window(self, dt) -> bool:
        """Check if current time is within Silver Bullet window (9:00-10:00 CT)."""
        current_time = dt.time() if hasattr(dt, 'time') else time(dt.hour, dt.minute)
        return time(9, 0) <= current_time < time(10, 0)
    
    def is_forced_close_time(self, dt) -> bool:
        """Check if it's time to force close all positions (15:00 CT)."""
        current_time = dt.time() if hasattr(dt, 'time') else time(dt.hour, dt.minute)
        return current_time >= time(15, 0)
    
    def get_15m_bar_index(self, dt):
        """Get the index of the 15m bar for a given datetime."""
        mask = self.data_15m.index <= dt
        if not mask.any():
            return -1
        return len(self.data_15m.index[mask]) - 1
    
    def get_5m_bar_index(self, dt):
        """Get the index of the 5m bar for a given datetime."""
        mask = self.data_5m.index <= dt
        if not mask.any():
            return -1
        return len(self.data_5m.index[mask]) - 1
    
    def check_15m_sweep(self, current_dt) -> Tuple[bool, bool]:
        """Check for 15m liquidity sweep."""
        idx_15m = self.get_15m_bar_index(current_dt)
        
        if idx_15m < self.fractal_lookback:
            return False, False
        
        # Get current 15m bar data
        current_15m = self.data_15m.iloc[idx_15m]
        
        # Get previous bar's fractal levels
        fractal_high = self.fractal_high_15m.iloc[idx_15m - 1]
        fractal_low = self.fractal_low_15m.iloc[idx_15m - 1]
        
        if pd.isna(fractal_high) or pd.isna(fractal_low):
            return False, False
        
        # Buy-side sweep: high wicks above fractal high, close below
        buy_side = current_15m['High'] > fractal_high and current_15m['Close'] < fractal_high
        
        # Sell-side sweep: low wicks below fractal low, close above
        sell_side = current_15m['Low'] < fractal_low and current_15m['Close'] > fractal_low
        
        return buy_side, sell_side
    
    def update_5m_fvg(self, current_dt):
        """Update 5m FVG tracking."""
        idx_5m = self.get_5m_bar_index(current_dt)
        
        if idx_5m <= self.last_5m_idx or idx_5m < 2:
            return
        
        self.last_5m_idx = idx_5m
        
        # Update FVG tracker with 5m data
        self.fvg_tracker.update(
            idx_5m,
            self.data_5m['Open'].values,
            self.data_5m['High'].values,
            self.data_5m['Low'].values,
            self.data_5m['Close'].values
        )
    
    def next(self):
        """Main strategy logic executed on each bar."""
        idx = len(self.data) - 1
        
        if idx < 100:  # Need enough data
            return
        
        current_dt = self.data.index[-1]
        current_price = self.data.Close[-1]
        current_high = self.data.High[-1]
        current_low = self.data.Low[-1]
        
        # Update 5m FVG tracking
        self.update_5m_fvg(current_dt)
        
        # Check for 15m sweeps
        buy_sweep, sell_sweep = self.check_15m_sweep(current_dt)
        
        if buy_sweep:
            self.last_buy_sweep_time = current_dt
        if sell_sweep:
            self.last_sell_sweep_time = current_dt
        
        # Force close at 15:00
        if self.is_forced_close_time(current_dt) and self.position:
            self.position.close()
            self._reset_trade_state()
            return
        
        # Break-even management
        if self.position and self.use_break_even and self.entry_price and self.stop_loss:
            if not self.breakeven_activated:
                risk = abs(self.entry_price - self.stop_loss)
                
                if self.position.is_long:
                    if current_price >= self.entry_price + risk:
                        self.stop_loss = self.entry_price
                        self.breakeven_activated = True
                else:
                    if current_price <= self.entry_price - risk:
                        self.stop_loss = self.entry_price
                        self.breakeven_activated = True
        
        # Check stop loss and take profit
        if self.position:
            if self.position.is_long:
                if self.stop_loss and current_low <= self.stop_loss:
                    self.position.close()
                    self._reset_trade_state()
                    return
                if self.take_profit and current_high >= self.take_profit:
                    self.position.close()
                    self._reset_trade_state()
                    return
            else:
                if self.stop_loss and current_high >= self.stop_loss:
                    self.position.close()
                    self._reset_trade_state()
                    return
                if self.take_profit and current_low <= self.take_profit:
                    self.position.close()
                    self._reset_trade_state()
                    return
        
        # Only enter during trading window
        if not self.is_trading_window(current_dt):
            return
        
        # Skip if already in position
        if self.position:
            return
        
        # Check sweep validity (within last 75 1m bars = 15 x 5m bars)
        sweep_validity_minutes = 75
        
        # LONG ENTRY: Sell-side sweep on 15m + filled bullish IFVG on 5m
        if self.last_sell_sweep_time is not None:
            time_since_sweep = (current_dt - self.last_sell_sweep_time).total_seconds() / 60
            if time_since_sweep <= sweep_validity_minutes:
                ifvg = self.fvg_tracker.get_filled_bullish_ifvg()
                if ifvg and ifvg.get('fill_candle_high') is not None:
                    # Entry at current price (IFVG has been filled)
                    self.entry_price = current_price
                    
                    # Calculate SL based on sl_type
                    if self.sl_type == 'fill_candle':
                        # SL under the candle that filled the IFVG
                        fill_idx = ifvg.get('fill_idx', self.last_5m_idx)
                        if fill_idx < len(self.data_5m):
                            self.stop_loss = self.data_5m['Low'].iloc[fill_idx] - 0.25
                        else:
                            self.stop_loss = current_low - 0.25
                    else:
                        # SL under the IFVG zone
                        self.stop_loss = ifvg['bottom'] - 0.25
                    
                    risk = self.entry_price - self.stop_loss
                    if risk > 0:
                        self.take_profit = self.entry_price + (risk * self.rr_target)
                        self.breakeven_activated = False
                        self.current_ifvg = ifvg
                        
                        # Mark IFVG as used
                        ifvg['filled'] = False  # Prevent re-entry
                        
                        self.buy()
                        return
        
        # SHORT ENTRY: Buy-side sweep on 15m + filled bearish IFVG on 5m
        if self.last_buy_sweep_time is not None:
            time_since_sweep = (current_dt - self.last_buy_sweep_time).total_seconds() / 60
            if time_since_sweep <= sweep_validity_minutes:
                ifvg = self.fvg_tracker.get_filled_bearish_ifvg()
                if ifvg and ifvg.get('fill_candle_low') is not None:
                    # Entry at current price (IFVG has been filled)
                    self.entry_price = current_price
                    
                    # Calculate SL based on sl_type
                    if self.sl_type == 'fill_candle':
                        # SL above the candle that filled the IFVG
                        fill_idx = ifvg.get('fill_idx', self.last_5m_idx)
                        if fill_idx < len(self.data_5m):
                            self.stop_loss = self.data_5m['High'].iloc[fill_idx] + 0.25
                        else:
                            self.stop_loss = current_high + 0.25
                    else:
                        # SL above the IFVG zone
                        self.stop_loss = ifvg['top'] + 0.25
                    
                    risk = self.stop_loss - self.entry_price
                    if risk > 0:
                        self.take_profit = self.entry_price - (risk * self.rr_target)
                        self.breakeven_activated = False
                        self.current_ifvg = ifvg
                        
                        # Mark IFVG as used
                        ifvg['filled'] = False  # Prevent re-entry
                        
                        self.sell()
                        return
    
    def _reset_trade_state(self):
        """Reset all trade-related state variables."""
        self.entry_price = None
        self.stop_loss = None
        self.take_profit = None
        self.breakeven_activated = False
        self.current_ifvg = None


# =============================================================================
# PERFORMANCE METRICS
# =============================================================================

def calculate_metrics(stats) -> dict:
    """Calculate and format performance metrics."""
    equity_curve = stats['_equity_curve']['Equity']
    returns = equity_curve.pct_change().dropna()
    
    total_trades = stats.get('# Trades', 0)
    if total_trades == 0:
        return {
            'Win Rate (%)': 0,
            'Profit Factor': 0,
            'Max Drawdown (%)': 0,
            'Sharpe Ratio': 0,
            'Total Trades': 0
        }
    
    win_rate = stats.get('Win Rate [%]', 0)
    
    trades = stats.get('_trades', pd.DataFrame())
    if len(trades) > 0 and 'PnL' in trades.columns:
        gross_profit = trades[trades['PnL'] > 0]['PnL'].sum()
        gross_loss = abs(trades[trades['PnL'] < 0]['PnL'].sum())
        profit_factor = gross_profit / gross_loss if gross_loss > 0 else INFINITE_PROFIT_FACTOR
    else:
        profit_factor = 0
    
    max_dd = stats.get('Max. Drawdown [%]', 0)
    
    annualization_factor = np.sqrt(TRADING_DAYS_PER_YEAR * MINUTES_PER_TRADING_DAY)
    if len(returns) > 0 and returns.std() > 0:
        sharpe = (returns.mean() / returns.std()) * annualization_factor
    else:
        sharpe = 0
    
    return {
        'Win Rate (%)': round(win_rate, 2),
        'Profit Factor': round(profit_factor, 2),
        'Max Drawdown (%)': round(abs(max_dd), 2),
        'Sharpe Ratio': round(sharpe, 2),
        'Total Trades': total_trades
    }


def plot_results(results_df: pd.DataFrame, stats, sl_type: str):
    """Generate results visualization."""
    fig = plt.figure(figsize=(18, 14))
    fig.suptitle(f'PBTrading Silver Bullet & IFVG V2 Backtest Results\n'
                 f'NQ Futures 2025 | SL Type: {sl_type.upper()}', 
                 fontsize=16, fontweight='bold', y=0.98)

    gs = fig.add_gridspec(2, 2, height_ratios=[1, 1], hspace=0.3, wspace=0.2)

    # Data
    rr_targets = results_df['RR Target'].values
    win_rates = results_df['Win Rate (%)'].values
    profit_factors = results_df['Profit Factor'].values
    max_drawdowns = results_df['Max Drawdown (%)'].values
    sharpe_ratios = results_df['Sharpe Ratio'].values

    colors = plt.cm.viridis(np.linspace(0.2, 0.8, len(rr_targets)))

    # Plot 1: Win Rate
    ax1 = fig.add_subplot(gs[0, 0])
    bars1 = ax1.bar(rr_targets, win_rates, color=colors, edgecolor='black', linewidth=0.5)
    ax1.set_xlabel('Risk-Reward Target', fontsize=11)
    ax1.set_ylabel('Win Rate (%)', fontsize=11)
    ax1.set_title('Win Rate by RR Target', fontsize=13, fontweight='bold')
    ax1.grid(axis='y', alpha=0.3)
    for bar, val in zip(bars1, win_rates):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, f'{val}%', 
                 ha='center', va='bottom', fontsize=9)

    # Plot 2: Profit Factor
    ax2 = fig.add_subplot(gs[0, 1])
    bars2 = ax2.bar(rr_targets, profit_factors, color=colors, edgecolor='black', linewidth=0.5)
    ax2.set_xlabel('Risk-Reward Target', fontsize=11)
    ax2.set_ylabel('Profit Factor', fontsize=11)
    ax2.set_title('Profit Factor by RR Target', fontsize=13, fontweight='bold')
    ax2.axhline(y=1.0, color='red', linestyle='--', linewidth=1.5, label='Break-even')
    ax2.grid(axis='y', alpha=0.3)
    ax2.legend(loc='upper right')
    for bar, val in zip(bars2, profit_factors):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02, f'{val}', 
                 ha='center', va='bottom', fontsize=9)

    # Plot 3: Max Drawdown & Sharpe
    ax3 = fig.add_subplot(gs[1, 0])
    x = np.arange(len(rr_targets))
    bars3 = ax3.bar(x, max_drawdowns, color='#ff6b6b', edgecolor='black', linewidth=0.5, 
                    label='Max Drawdown (%)')
    ax3_twin = ax3.twinx()
    line3 = ax3_twin.plot(x, sharpe_ratios, 'o-', color='#4ecdc4', linewidth=2, markersize=8, 
                          label='Sharpe Ratio')
    ax3.set_xlabel('Risk-Reward Target', fontsize=11)
    ax3.set_ylabel('Max Drawdown (%)', fontsize=11, color='#ff6b6b')
    ax3_twin.set_ylabel('Sharpe Ratio', fontsize=11, color='#4ecdc4')
    ax3.set_title('Max Drawdown & Sharpe Ratio', fontsize=13, fontweight='bold')
    ax3.set_xticks(x)
    ax3.set_xticklabels(rr_targets)
    ax3.grid(axis='y', alpha=0.3)
    ax3.legend(loc='upper left')
    ax3_twin.legend(loc='upper right')

    # Plot 4: Summary Table
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.axis('off')

    table_data = [['RR', 'Win Rate', 'PF', 'MaxDD', 'Sharpe', 'Trades']]
    for i in range(len(rr_targets)):
        table_data.append([
            f'{rr_targets[i]}',
            f'{win_rates[i]}%',
            f'{profit_factors[i]}',
            f'{max_drawdowns[i]}%',
            f'{sharpe_ratios[i]}',
            f'{results_df["Total Trades"].iloc[i]}'
        ])

    table = ax4.table(cellText=table_data, loc='center', cellLoc='center',
                       colWidths=[0.12, 0.16, 0.12, 0.14, 0.14, 0.14])
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.8)

    for j in range(6):
        table[(0, j)].set_facecolor('#2c3e50')
        table[(0, j)].set_text_props(color='white', fontweight='bold')

    # Highlight best values
    if len(win_rates) > 0:
        best_wr_idx = np.argmax(win_rates) + 1
        best_pf_idx = np.argmax(profit_factors) + 1
        best_dd_idx = np.argmin(max_drawdowns) + 1
        best_sh_idx = np.argmax(sharpe_ratios) + 1

        table[(best_wr_idx, 1)].set_facecolor('#a8e6cf')
        table[(best_pf_idx, 2)].set_facecolor('#a8e6cf')
        table[(best_dd_idx, 3)].set_facecolor('#a8e6cf')
        table[(best_sh_idx, 4)].set_facecolor('#a8e6cf')

    ax4.set_title('Results Summary Table\n(Green = Best Value)', fontsize=13, fontweight='bold', pad=20)

    info_text = f"""
Strategy: Silver Bullet + IFVG V2
Sweep Detection: 15m (50 candle lookback)
FVG/IFVG: 5m timeframe
Entry: On IFVG fill
SL Type: {sl_type.upper()}
Trading Window: 9:00-10:00 CT
"""
    fig.text(0.5, 0.02, info_text, ha='center', fontsize=10, 
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    plt.tight_layout(rect=[0, 0.08, 1, 0.95])
    filename = f'RESULTS_V2_{sl_type}.png'
    plt.savefig(filename, dpi=150, bbox_inches='tight', facecolor='white')
    print(f"Results saved to '{filename}'")
    
    return filename


# =============================================================================
# MAIN EXECUTION
# =============================================================================

def run_backtest_v2(data_dir: str, years: list = None, rr_targets: list = None, 
                    sl_type: str = 'fill_candle'):
    """
    Run the V2 backtest with specified parameters.
    
    Args:
        data_dir: Directory containing the data files
        years: List of years to test (default: [2025])
        rr_targets: List of RR ratios to test
        sl_type: 'fill_candle' or 'ifvg' for stop loss placement
    """
    if years is None:
        years = [2025]
    
    if rr_targets is None:
        rr_targets = [1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]
    
    print("Loading data...")
    all_data = []
    
    for year in years:
        try:
            df = load_data(data_dir, year, '1m')
            df = clean_data(df)
            all_data.append(df)
            print(f"  Loaded {year}: {len(df)} bars")
        except FileNotFoundError as e:
            print(f"  Warning: {e}")
    
    if not all_data:
        print("No data loaded. Exiting.")
        return None, None
    
    data = pd.concat(all_data).sort_index()
    data = data[~data.index.duplicated(keep='first')]
    
    print(f"\nTotal data: {len(data)} bars from {data.index[0]} to {data.index[-1]}")
    
    results = []
    best_stats = None
    best_sharpe = -float('inf')
    
    print("\n" + "=" * 60)
    print(f"Running V2 backtests (SL Type: {sl_type.upper()})...")
    print("=" * 60)
    
    for rr in rr_targets:
        print(f"\nTesting RR = {rr}...")
        
        bt = Backtest(
            data,
            SilverBulletIFVGStrategyV2,
            cash=100000,
            commission=0.0002,
            exclusive_orders=True
        )
        
        stats = bt.run(rr_target=rr, sl_type=sl_type)
        metrics = calculate_metrics(stats)
        metrics['RR Target'] = rr
        results.append(metrics)
        
        print(f"  Win Rate: {metrics['Win Rate (%)']}%")
        print(f"  Profit Factor: {metrics['Profit Factor']}")
        print(f"  Max Drawdown: {metrics['Max Drawdown (%)']}%")
        print(f"  Sharpe Ratio: {metrics['Sharpe Ratio']}")
        print(f"  Total Trades: {metrics['Total Trades']}")
        
        if metrics['Sharpe Ratio'] > best_sharpe:
            best_sharpe = metrics['Sharpe Ratio']
            best_stats = stats
    
    print("\n" + "=" * 60)
    print("RESULTS SUMMARY")
    print("=" * 60)
    
    results_df = pd.DataFrame(results)
    results_df = results_df[['RR Target', 'Win Rate (%)', 'Profit Factor', 
                             'Max Drawdown (%)', 'Sharpe Ratio', 'Total Trades']]
    print(results_df.to_string(index=False))
    
    # Generate visualization
    if len(results_df) > 0:
        plot_results(results_df, best_stats, sl_type)
    
    return results_df, best_stats


if __name__ == '__main__':
    DATA_DIR = os.path.dirname(os.path.abspath(__file__))
    YEARS_TO_TEST = [2025]
    RR_TARGETS = [1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]
    
    print("=" * 70)
    print("PBTrading Silver Bullet & IFVG V2 Backtest Strategy")
    print("=" * 70)
    print("\nUpdated Conditions:")
    print("  - Liquidity sweep on 15m (50 candle lookback)")
    print("  - FVG creation on 5m, violated to become IFVG")
    print("  - Entry when price fills the IFVG")
    print("  - Two SL options tested: under fill candle AND under IFVG")
    print()
    
    # Test with SL under fill candle
    print("\n" + "=" * 70)
    print("TEST 1: SL under the candle that filled the IFVG")
    print("=" * 70)
    results_fill, stats_fill = run_backtest_v2(DATA_DIR, YEARS_TO_TEST, RR_TARGETS, 
                                                sl_type='fill_candle')
    
    # Test with SL under IFVG
    print("\n" + "=" * 70)
    print("TEST 2: SL under the IFVG zone")
    print("=" * 70)
    results_ifvg, stats_ifvg = run_backtest_v2(DATA_DIR, YEARS_TO_TEST, RR_TARGETS, 
                                               sl_type='ifvg')

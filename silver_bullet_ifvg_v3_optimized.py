#!/usr/bin/env python3
"""
PBTrading Silver Bullet & IFVG Optimized Strategy V3 for NQ Futures

OPTIMIZED FOR BEST PROFIT FACTOR:
- Grid search over multiple parameters
- Filters for higher quality setups
- Improved entry timing
- Better risk management
"""

import os
import zipfile
from datetime import datetime, time
from typing import Optional, Tuple, List
from itertools import product

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from backtesting import Backtest, Strategy


# =============================================================================
# CONSTANTS
# =============================================================================

TRADING_DAYS_PER_YEAR = 252
MINUTES_PER_TRADING_DAY = 390
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
# ENHANCED FVG TRACKER WITH QUALITY FILTERS
# =============================================================================

class EnhancedFVGTracker:
    """
    Enhanced FVG Tracker with quality filters for better signal selection.
    """
    
    def __init__(self, lookback: int = 100, min_fvg_size: float = 0.0):
        self.bullish_fvgs = []
        self.bearish_fvgs = []
        self.bullish_ifvgs = []
        self.bearish_ifvgs = []
        self.lookback = lookback
        self.min_fvg_size = min_fvg_size
        
    def update(self, idx: int, opens: np.ndarray, highs: np.ndarray,
               lows: np.ndarray, closes: np.ndarray):
        """Update FVG tracking with new bar data."""
        if idx < 2:
            return
        
        current_close = closes[idx]
        current_low = lows[idx]
        current_high = highs[idx]
        
        bar_minus_2_low = lows[idx - 2]
        bar_minus_2_high = highs[idx - 2]
        
        # Bullish FVG: bar[idx-2].low > bar[idx].high (gap up)
        if bar_minus_2_low > current_high:
            fvg_size = bar_minus_2_low - current_high
            if fvg_size >= self.min_fvg_size:
                self.bullish_fvgs.append({
                    'top': bar_minus_2_low,
                    'bottom': current_high,
                    'size': fvg_size,
                    'created_idx': idx,
                    'violated': False,
                    'fill_candle_low': None
                })
        
        # Bearish FVG: bar[idx-2].high < bar[idx].low (gap down)
        if bar_minus_2_high < current_low:
            fvg_size = current_low - bar_minus_2_high
            if fvg_size >= self.min_fvg_size:
                self.bearish_fvgs.append({
                    'top': current_low,
                    'bottom': bar_minus_2_high,
                    'size': fvg_size,
                    'created_idx': idx,
                    'violated': False,
                    'fill_candle_high': None
                })
        
        # Check for FVG violations -> creates IFVG
        for fvg in self.bullish_fvgs:
            if not fvg['violated'] and current_close < fvg['bottom']:
                fvg['violated'] = True
                self.bullish_ifvgs.append({
                    'top': fvg['top'],
                    'bottom': fvg['bottom'],
                    'size': fvg['size'],
                    'created_idx': idx,
                    'filled': False,
                    'fill_candle_low': None
                })
        
        for fvg in self.bearish_fvgs:
            if not fvg['violated'] and current_close > fvg['top']:
                fvg['violated'] = True
                self.bearish_ifvgs.append({
                    'top': fvg['top'],
                    'bottom': fvg['bottom'],
                    'size': fvg['size'],
                    'created_idx': idx,
                    'filled': False,
                    'fill_candle_high': None
                })
        
        # Check for IFVG fills
        for ifvg in self.bearish_ifvgs:
            if not ifvg['filled']:
                if current_close >= ifvg['bottom']:
                    ifvg['filled'] = True
                    ifvg['fill_candle_high'] = current_high
                    ifvg['fill_candle_low'] = current_low
                    ifvg['fill_idx'] = idx
        
        for ifvg in self.bullish_ifvgs:
            if not ifvg['filled']:
                if current_close <= ifvg['top']:
                    ifvg['filled'] = True
                    ifvg['fill_candle_low'] = current_low
                    ifvg['fill_candle_high'] = current_high
                    ifvg['fill_idx'] = idx
        
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
# OPTIMIZED STRATEGY V3
# =============================================================================

class OptimizedSilverBulletIFVG(Strategy):
    """
    Optimized Silver Bullet + IFVG Strategy
    
    Optimization parameters:
    - fractal_lookback: Lookback for 15m sweep detection
    - sweep_validity: How long a sweep signal remains valid
    - min_fvg_size: Minimum FVG size filter
    - trading_start_hour/minute: Start of trading window
    - trading_end_hour/minute: End of trading window
    - rr_target: Risk-reward ratio
    - sl_type: 'fill_candle' or 'ifvg'
    - use_trend_filter: Filter trades against trend
    - min_volume_ratio: Minimum volume filter
    """
    
    # Optimization parameters with defaults
    fractal_lookback = 50
    sweep_validity = 60  # minutes
    min_fvg_size = 0.0
    trading_start_hour = 9
    trading_start_minute = 0
    trading_end_hour = 10
    trading_end_minute = 0
    rr_target = 2.0
    sl_type = 'fill_candle'
    use_break_even = True
    use_trend_filter = False
    trend_lookback = 100
    min_volume_ratio = 0.0
    
    def init(self):
        """Initialize indicators and tracking variables."""
        self.fvg_tracker = EnhancedFVGTracker(lookback=100, min_fvg_size=self.min_fvg_size)
        
        # Build multi-timeframe data
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
        
        # Trend filter (simple MA comparison)
        if self.use_trend_filter:
            self.trend_ma = self.data_15m['Close'].rolling(window=self.trend_lookback).mean()
        
        # Track sweep signals
        self.last_buy_sweep_time = None
        self.last_sell_sweep_time = None
        
        self.last_5m_idx = -1
        
        self.entry_price = None
        self.stop_loss = None
        self.take_profit = None
        self.breakeven_activated = False
        self.current_ifvg = None
        
    def is_trading_window(self, dt) -> bool:
        """Check if current time is within trading window."""
        current_time = dt.time() if hasattr(dt, 'time') else time(dt.hour, dt.minute)
        start_time = time(self.trading_start_hour, self.trading_start_minute)
        end_time = time(self.trading_end_hour, self.trading_end_minute)
        return start_time <= current_time < end_time
    
    def is_forced_close_time(self, dt) -> bool:
        """Check if it's time to force close all positions."""
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
        
        current_15m = self.data_15m.iloc[idx_15m]
        
        fractal_high = self.fractal_high_15m.iloc[idx_15m - 1]
        fractal_low = self.fractal_low_15m.iloc[idx_15m - 1]
        
        if pd.isna(fractal_high) or pd.isna(fractal_low):
            return False, False
        
        buy_side = current_15m['High'] > fractal_high and current_15m['Close'] < fractal_high
        sell_side = current_15m['Low'] < fractal_low and current_15m['Close'] > fractal_low
        
        return buy_side, sell_side
    
    def check_trend_filter(self, current_dt, is_long: bool) -> bool:
        """Check if trade aligns with trend."""
        if not self.use_trend_filter:
            return True
        
        idx_15m = self.get_15m_bar_index(current_dt)
        if idx_15m < self.trend_lookback:
            return True
        
        current_price = self.data_15m['Close'].iloc[idx_15m]
        ma_value = self.trend_ma.iloc[idx_15m]
        
        if pd.isna(ma_value):
            return True
        
        if is_long:
            return current_price > ma_value
        else:
            return current_price < ma_value
    
    def update_5m_fvg(self, current_dt):
        """Update 5m FVG tracking."""
        idx_5m = self.get_5m_bar_index(current_dt)
        
        if idx_5m <= self.last_5m_idx or idx_5m < 2:
            return
        
        self.last_5m_idx = idx_5m
        
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
        
        if idx < 100:
            return
        
        current_dt = self.data.index[-1]
        current_price = self.data.Close[-1]
        current_high = self.data.High[-1]
        current_low = self.data.Low[-1]
        
        self.update_5m_fvg(current_dt)
        
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
        
        if not self.is_trading_window(current_dt):
            return
        
        if self.position:
            return
        
        # LONG ENTRY
        if self.last_sell_sweep_time is not None:
            time_since_sweep = (current_dt - self.last_sell_sweep_time).total_seconds() / 60
            if time_since_sweep <= self.sweep_validity:
                # Check trend filter
                if not self.check_trend_filter(current_dt, is_long=True):
                    return
                
                ifvg = self.fvg_tracker.get_filled_bullish_ifvg()
                if ifvg and ifvg.get('fill_candle_high') is not None:
                    self.entry_price = current_price
                    
                    if self.sl_type == 'fill_candle':
                        fill_idx = ifvg.get('fill_idx', self.last_5m_idx)
                        if fill_idx < len(self.data_5m):
                            self.stop_loss = self.data_5m['Low'].iloc[fill_idx] - 0.25
                        else:
                            self.stop_loss = current_low - 0.25
                    else:
                        self.stop_loss = ifvg['bottom'] - 0.25
                    
                    risk = self.entry_price - self.stop_loss
                    if risk > 0:
                        self.take_profit = self.entry_price + (risk * self.rr_target)
                        self.breakeven_activated = False
                        self.current_ifvg = ifvg
                        ifvg['filled'] = False
                        self.buy()
                        return
        
        # SHORT ENTRY
        if self.last_buy_sweep_time is not None:
            time_since_sweep = (current_dt - self.last_buy_sweep_time).total_seconds() / 60
            if time_since_sweep <= self.sweep_validity:
                # Check trend filter
                if not self.check_trend_filter(current_dt, is_long=False):
                    return
                
                ifvg = self.fvg_tracker.get_filled_bearish_ifvg()
                if ifvg and ifvg.get('fill_candle_low') is not None:
                    self.entry_price = current_price
                    
                    if self.sl_type == 'fill_candle':
                        fill_idx = ifvg.get('fill_idx', self.last_5m_idx)
                        if fill_idx < len(self.data_5m):
                            self.stop_loss = self.data_5m['High'].iloc[fill_idx] + 0.25
                        else:
                            self.stop_loss = current_high + 0.25
                    else:
                        self.stop_loss = ifvg['top'] + 0.25
                    
                    risk = self.stop_loss - self.entry_price
                    if risk > 0:
                        self.take_profit = self.entry_price - (risk * self.rr_target)
                        self.breakeven_activated = False
                        self.current_ifvg = ifvg
                        ifvg['filled'] = False
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
            'Total Trades': 0,
            'Avg Trade': 0
        }
    
    win_rate = stats.get('Win Rate [%]', 0)
    
    trades = stats.get('_trades', pd.DataFrame())
    if len(trades) > 0 and 'PnL' in trades.columns:
        gross_profit = trades[trades['PnL'] > 0]['PnL'].sum()
        gross_loss = abs(trades[trades['PnL'] < 0]['PnL'].sum())
        profit_factor = gross_profit / gross_loss if gross_loss > 0 else INFINITE_PROFIT_FACTOR
        avg_trade = trades['PnL'].mean()
    else:
        profit_factor = 0
        avg_trade = 0
    
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
        'Total Trades': total_trades,
        'Avg Trade': round(avg_trade, 2)
    }


# =============================================================================
# OPTIMIZATION ENGINE
# =============================================================================

def run_optimization(data_dir: str, years: list = None):
    """
    Run parameter optimization to find best Profit Factor.
    """
    if years is None:
        years = [2025]
    
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
    
    # Focused parameter combinations based on V2 results
    test_configs = [
        # RR variations with fill_candle SL
        {'rr_target': 1.5, 'sl_type': 'fill_candle', 'fractal_lookback': 50, 'sweep_validity': 60, 
         'trading_start_hour': 9, 'trading_start_minute': 0, 'trading_end_hour': 10, 'trading_end_minute': 0,
         'use_trend_filter': False},
        {'rr_target': 2.0, 'sl_type': 'fill_candle', 'fractal_lookback': 50, 'sweep_validity': 60,
         'trading_start_hour': 9, 'trading_start_minute': 0, 'trading_end_hour': 10, 'trading_end_minute': 0,
         'use_trend_filter': False},
        {'rr_target': 2.5, 'sl_type': 'fill_candle', 'fractal_lookback': 50, 'sweep_validity': 60,
         'trading_start_hour': 9, 'trading_start_minute': 0, 'trading_end_hour': 10, 'trading_end_minute': 0,
         'use_trend_filter': False},
        # With trend filter
        {'rr_target': 2.0, 'sl_type': 'fill_candle', 'fractal_lookback': 50, 'sweep_validity': 60,
         'trading_start_hour': 9, 'trading_start_minute': 0, 'trading_end_hour': 10, 'trading_end_minute': 0,
         'use_trend_filter': True},
        {'rr_target': 2.5, 'sl_type': 'fill_candle', 'fractal_lookback': 50, 'sweep_validity': 60,
         'trading_start_hour': 9, 'trading_start_minute': 0, 'trading_end_hour': 10, 'trading_end_minute': 0,
         'use_trend_filter': True},
        # Different fractal lookback
        {'rr_target': 2.0, 'sl_type': 'fill_candle', 'fractal_lookback': 30, 'sweep_validity': 60,
         'trading_start_hour': 9, 'trading_start_minute': 0, 'trading_end_hour': 10, 'trading_end_minute': 0,
         'use_trend_filter': False},
        {'rr_target': 2.0, 'sl_type': 'fill_candle', 'fractal_lookback': 70, 'sweep_validity': 60,
         'trading_start_hour': 9, 'trading_start_minute': 0, 'trading_end_hour': 10, 'trading_end_minute': 0,
         'use_trend_filter': False},
        # Different sweep validity
        {'rr_target': 2.0, 'sl_type': 'fill_candle', 'fractal_lookback': 50, 'sweep_validity': 30,
         'trading_start_hour': 9, 'trading_start_minute': 0, 'trading_end_hour': 10, 'trading_end_minute': 0,
         'use_trend_filter': False},
        {'rr_target': 2.0, 'sl_type': 'fill_candle', 'fractal_lookback': 50, 'sweep_validity': 90,
         'trading_start_hour': 9, 'trading_start_minute': 0, 'trading_end_hour': 10, 'trading_end_minute': 0,
         'use_trend_filter': False},
        # IFVG SL type variations
        {'rr_target': 2.0, 'sl_type': 'ifvg', 'fractal_lookback': 50, 'sweep_validity': 60,
         'trading_start_hour': 9, 'trading_start_minute': 0, 'trading_end_hour': 10, 'trading_end_minute': 0,
         'use_trend_filter': False},
        {'rr_target': 2.0, 'sl_type': 'ifvg', 'fractal_lookback': 50, 'sweep_validity': 60,
         'trading_start_hour': 9, 'trading_start_minute': 0, 'trading_end_hour': 10, 'trading_end_minute': 0,
         'use_trend_filter': True},
        # Extended trading window
        {'rr_target': 2.0, 'sl_type': 'fill_candle', 'fractal_lookback': 50, 'sweep_validity': 60,
         'trading_start_hour': 9, 'trading_start_minute': 0, 'trading_end_hour': 10, 'trading_end_minute': 30,
         'use_trend_filter': False},
        # Later start
        {'rr_target': 2.0, 'sl_type': 'fill_candle', 'fractal_lookback': 50, 'sweep_validity': 60,
         'trading_start_hour': 9, 'trading_start_minute': 15, 'trading_end_hour': 10, 'trading_end_minute': 0,
         'use_trend_filter': False},
        # Best V2 config with trend filter
        {'rr_target': 2.5, 'sl_type': 'fill_candle', 'fractal_lookback': 50, 'sweep_validity': 75,
         'trading_start_hour': 9, 'trading_start_minute': 0, 'trading_end_hour': 10, 'trading_end_minute': 0,
         'use_trend_filter': True},
        # Tight sweep validity with trend filter
        {'rr_target': 2.0, 'sl_type': 'fill_candle', 'fractal_lookback': 50, 'sweep_validity': 45,
         'trading_start_hour': 9, 'trading_start_minute': 0, 'trading_end_hour': 10, 'trading_end_minute': 0,
         'use_trend_filter': True},
    ]
    
    print(f"\nTesting {len(test_configs)} focused configurations...")
    print("=" * 80)
    
    results = []
    best_pf = 0
    best_params = None
    best_stats = None
    
    for i, params in enumerate(test_configs):
        print(f"\nConfig {i+1}/{len(test_configs)}: RR={params['rr_target']}, SL={params['sl_type']}, "
              f"Trend={'ON' if params['use_trend_filter'] else 'OFF'}")
        
        try:
            bt = Backtest(
                data,
                OptimizedSilverBulletIFVG,
                cash=100000,
                commission=0.0002,
                exclusive_orders=True
            )
            
            stats = bt.run(**params)
            metrics = calculate_metrics(stats)
            
            result = {**params, **metrics}
            results.append(result)
            
            print(f"  PF: {metrics['Profit Factor']}, WR: {metrics['Win Rate (%)']}%, "
                  f"DD: {metrics['Max Drawdown (%)']}%, Trades: {metrics['Total Trades']}")
            
            if metrics['Profit Factor'] > best_pf and metrics['Total Trades'] >= 30:
                best_pf = metrics['Profit Factor']
                best_params = params
                best_stats = stats
        except Exception as e:
            print(f"  Error: {e}")
            continue
    
    print(f"\n" + "=" * 80)
    print("OPTIMIZATION COMPLETE!")
    print("=" * 80)
    
    if not results:
        print("No valid results found.")
        return None, None, None
    
    results_df = pd.DataFrame(results)
    results_df = results_df.sort_values('Profit Factor', ascending=False)
    
    print("\n🏆 TOP 5 CONFIGURATIONS BY PROFIT FACTOR:")
    print("-" * 80)
    
    for i, row in results_df.head(5).iterrows():
        print(f"\n#{results_df.index.get_loc(i)+1}: PF={row['Profit Factor']}, WR={row['Win Rate (%)']}%, "
              f"DD={row['Max Drawdown (%)']}%")
        print(f"   RR={row['rr_target']}, SL={row['sl_type']}, Trend={'ON' if row['use_trend_filter'] else 'OFF'}, "
              f"Lookback={row['fractal_lookback']}, Validity={row['sweep_validity']}min")
    
    return results_df, best_stats, best_params


def plot_optimization_results(results_df: pd.DataFrame, best_params: dict):
    """Generate visualization of optimization results."""
    fig = plt.figure(figsize=(18, 14))
    fig.suptitle('PBTrading Silver Bullet & IFVG V3 - Optimization Results\n'
                 'Best Configuration for Maximum Profit Factor', 
                 fontsize=16, fontweight='bold', y=0.98)

    gs = fig.add_gridspec(2, 2, height_ratios=[1, 1], hspace=0.3, wspace=0.25)

    # Filter for plotting
    plot_df = results_df.head(20)  # Top 20 configurations

    # Plot 1: Profit Factor Distribution
    ax1 = fig.add_subplot(gs[0, 0])
    pf_values = plot_df['Profit Factor'].values
    colors = ['#28a745' if pf >= 1.0 else '#dc3545' for pf in pf_values]
    bars = ax1.bar(range(len(pf_values)), pf_values, color=colors, edgecolor='black', linewidth=0.5)
    ax1.axhline(y=1.0, color='blue', linestyle='--', linewidth=2, label='Break-even (PF=1.0)')
    ax1.set_xlabel('Configuration Rank', fontsize=11)
    ax1.set_ylabel('Profit Factor', fontsize=11)
    ax1.set_title('Top 20 Configurations by Profit Factor', fontsize=13, fontweight='bold')
    ax1.legend()
    ax1.grid(axis='y', alpha=0.3)

    # Plot 2: PF vs Win Rate scatter
    ax2 = fig.add_subplot(gs[0, 1])
    scatter = ax2.scatter(results_df['Win Rate (%)'], results_df['Profit Factor'], 
                         c=results_df['Total Trades'], cmap='viridis', 
                         alpha=0.6, edgecolors='black', linewidth=0.5)
    ax2.axhline(y=1.0, color='red', linestyle='--', linewidth=1.5, label='Break-even')
    ax2.set_xlabel('Win Rate (%)', fontsize=11)
    ax2.set_ylabel('Profit Factor', fontsize=11)
    ax2.set_title('Profit Factor vs Win Rate', fontsize=13, fontweight='bold')
    cbar = plt.colorbar(scatter, ax=ax2)
    cbar.set_label('Total Trades')
    ax2.legend()
    ax2.grid(alpha=0.3)

    # Plot 3: RR Target impact on PF
    ax3 = fig.add_subplot(gs[1, 0])
    for sl in ['fill_candle', 'ifvg']:
        subset = results_df[results_df['sl_type'] == sl]
        grouped = subset.groupby('rr_target')['Profit Factor'].mean()
        ax3.plot(grouped.index, grouped.values, 'o-', linewidth=2, markersize=8, 
                label=f'SL: {sl}')
    ax3.axhline(y=1.0, color='red', linestyle='--', linewidth=1.5)
    ax3.set_xlabel('RR Target', fontsize=11)
    ax3.set_ylabel('Average Profit Factor', fontsize=11)
    ax3.set_title('Impact of RR Target on Profit Factor', fontsize=13, fontweight='bold')
    ax3.legend()
    ax3.grid(alpha=0.3)

    # Plot 4: Best Configuration Summary
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.axis('off')
    
    best_row = results_df.iloc[0]
    
    summary_text = f"""
    🏆 BEST CONFIGURATION (OPTIMIZED FOR PROFIT FACTOR)
    
    ══════════════════════════════════════════════════════
    
    PARAMETERS:
    ─────────────────────────────────────
    • Fractal Lookback (15m): {best_row.get('fractal_lookback', 'N/A')} candles
    • Sweep Validity: {best_row.get('sweep_validity', 'N/A')} minutes
    • RR Target: {best_row.get('rr_target', 'N/A')}
    • SL Type: {best_row.get('sl_type', 'N/A').upper()}
    • Trading Window: {best_row.get('trading_start_hour', 9)}:{best_row.get('trading_start_minute', 0):02d} - {best_row.get('trading_end_hour', 10)}:{best_row.get('trading_end_minute', 0):02d} CT
    • Trend Filter: {'ON' if best_row.get('use_trend_filter', False) else 'OFF'}
    
    RESULTS:
    ─────────────────────────────────────
    ✓ Profit Factor: {best_row['Profit Factor']}
    ✓ Win Rate: {best_row['Win Rate (%)']}%
    ✓ Max Drawdown: {best_row['Max Drawdown (%)']}%
    ✓ Sharpe Ratio: {best_row['Sharpe Ratio']}
    ✓ Total Trades: {int(best_row['Total Trades'])}
    
    ══════════════════════════════════════════════════════
    """
    
    ax4.text(0.5, 0.5, summary_text, transform=ax4.transAxes, fontsize=11,
             verticalalignment='center', horizontalalignment='center',
             fontfamily='monospace', 
             bbox=dict(boxstyle='round', facecolor='#f8f9fa', edgecolor='#2c3e50', linewidth=2))

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig('RESULTS_V3_OPTIMIZED.png', dpi=150, bbox_inches='tight', facecolor='white')
    print("\nResults saved to 'RESULTS_V3_OPTIMIZED.png'")
    
    return fig


# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == '__main__':
    DATA_DIR = os.path.dirname(os.path.abspath(__file__))
    YEARS_TO_TEST = [2025]
    
    print("=" * 80)
    print("PBTrading Silver Bullet & IFVG V3 - OPTIMIZATION FOR BEST PROFIT FACTOR")
    print("=" * 80)
    print("\nGoal: Find parameter combination with highest Profit Factor (PF > 1.0)")
    print()
    
    results_df, best_stats, best_params = run_optimization(DATA_DIR, YEARS_TO_TEST)
    
    if results_df is not None and len(results_df) > 0:
        plot_optimization_results(results_df, best_params)
        
        # Save results to markdown
        with open('RESULTS_V3.md', 'w') as f:
            f.write("# PBTrading Silver Bullet & IFVG V3 - Optimization Results\n\n")
            f.write("## Objective: Maximize Profit Factor\n\n")
            f.write("### Best Configuration\n\n")
            
            best = results_df.iloc[0]
            f.write(f"| Parameter | Value |\n")
            f.write(f"|-----------|-------|\n")
            f.write(f"| Fractal Lookback | {best.get('fractal_lookback', 'N/A')} |\n")
            f.write(f"| Sweep Validity | {best.get('sweep_validity', 'N/A')} min |\n")
            f.write(f"| RR Target | {best.get('rr_target', 'N/A')} |\n")
            f.write(f"| SL Type | {best.get('sl_type', 'N/A')} |\n")
            f.write(f"| Trading Start | {best.get('trading_start_hour', 9)}:{best.get('trading_start_minute', 0):02d} |\n")
            f.write(f"| Trading End | {best.get('trading_end_hour', 10)}:{best.get('trading_end_minute', 0):02d} |\n")
            f.write(f"| Trend Filter | {'Yes' if best.get('use_trend_filter', False) else 'No'} |\n\n")
            
            f.write("### Performance Metrics\n\n")
            f.write(f"| Metric | Value |\n")
            f.write(f"|--------|-------|\n")
            f.write(f"| **Profit Factor** | **{best['Profit Factor']}** |\n")
            f.write(f"| Win Rate | {best['Win Rate (%)']}% |\n")
            f.write(f"| Max Drawdown | {best['Max Drawdown (%)']}% |\n")
            f.write(f"| Sharpe Ratio | {best['Sharpe Ratio']} |\n")
            f.write(f"| Total Trades | {int(best['Total Trades'])} |\n\n")
            
            f.write("### Top 10 Configurations\n\n")
            top_10 = results_df.head(10)[['Profit Factor', 'Win Rate (%)', 'Max Drawdown (%)', 
                                          'rr_target', 'sl_type', 'use_trend_filter', 'Total Trades']]
            f.write(top_10.to_markdown(index=False))
            f.write("\n\n*Generated on 2025-11-30*\n")
        
        print("\nResults saved to 'RESULTS_V3.md'")

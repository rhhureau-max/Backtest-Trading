#!/usr/bin/env python3
"""
PBTrading Silver Bullet & IFVG Backtest Strategy for NQ Futures

This script implements a complete backtesting strategy based on:
- Silver Bullet trading window (9:00-10:00 Chicago Time)
- Liquidity Sweep detection
- Fair Value Gap (FVG) and Inversion FVG (IFVG) entry logic
- Multiple RR targets with break-even management
"""

import os
import zipfile
from datetime import datetime, time
from typing import Optional, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from backtesting import Backtest, Strategy


# =============================================================================
# CONSTANTS
# =============================================================================

TRADING_DAYS_PER_YEAR = 252
MINUTES_PER_TRADING_DAY = 390
SWEEP_LOOKBACK_BARS = 10  # Bars to look back for sweep validation and swing levels
INFINITE_PROFIT_FACTOR = 999.0  # Sentinel value when no losing trades


# =============================================================================
# DATA LOADING AND CLEANING
# =============================================================================

def _parse_ohlcv_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Convert raw CSV data to OHLCV DataFrame with datetime index."""
    # Handle mixed date formats (DD/MM/YYYY and MM/DD/YYYY)
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
    # Remove rows with zero or NaN values
    df = df.dropna()
    df = df[(df['Volume'] > 0) & (df['Close'] > 0)]
    
    # Remove days with very low volume (holidays/half-days)
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


def resample_to_5m(df_1m: pd.DataFrame) -> pd.DataFrame:
    """Resample 1-minute data to 5-minute bars."""
    return df_1m.resample('5min').agg({
        'Open': 'first',
        'High': 'max',
        'Low': 'min',
        'Close': 'last',
        'Volume': 'sum'
    }).dropna()


# =============================================================================
# INDICATOR CALCULATIONS
# =============================================================================

def calculate_fractal_highs(df: pd.DataFrame, lookback: int = 20) -> pd.Series:
    """Calculate fractal highs (highest high in lookback period)."""
    return df['High'].rolling(window=lookback, min_periods=lookback).max()


def calculate_fractal_lows(df: pd.DataFrame, lookback: int = 20) -> pd.Series:
    """Calculate fractal lows (lowest low in lookback period)."""
    return df['Low'].rolling(window=lookback, min_periods=lookback).min()


def detect_liquidity_sweep(df: pd.DataFrame, lookback: int = 20) -> Tuple[pd.Series, pd.Series]:
    """
    Detect liquidity sweeps (wicks through fractal high/low).
    
    Returns:
        buy_side_sweep: True when price wicks above fractal high then closes below
        sell_side_sweep: True when price wicks below fractal low then closes above
    """
    fractal_high = calculate_fractal_highs(df, lookback).shift(1)
    fractal_low = calculate_fractal_lows(df, lookback).shift(1)
    
    # Buy-side sweep: wick above fractal high, close below
    buy_side_sweep = (df['High'] > fractal_high) & (df['Close'] < fractal_high)
    
    # Sell-side sweep: wick below fractal low, close above
    sell_side_sweep = (df['Low'] < fractal_low) & (df['Close'] > fractal_low)
    
    return buy_side_sweep, sell_side_sweep


def detect_fvg(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Detect Fair Value Gaps (FVG) using wicks of candles n-1 and n+1.
    
    Bullish FVG: candle[n-1].low > candle[n+1].high (gap above current candle)
    Bearish FVG: candle[n-1].high < candle[n+1].low (gap below current candle)
    
    Returns DataFrames with FVG zones (top, bottom, index)
    """
    bullish_fvg_data = []
    bearish_fvg_data = []
    
    for i in range(1, len(df) - 1):
        prev_low = df['Low'].iloc[i - 1]
        next_high = df['High'].iloc[i + 1]
        prev_high = df['High'].iloc[i - 1]
        next_low = df['Low'].iloc[i + 1]
        
        # Bullish FVG: gap up
        if prev_low > next_high:
            bullish_fvg_data.append({
                'top': prev_low,
                'bottom': next_high,
                'created_at': df.index[i]
            })
        
        # Bearish FVG: gap down
        if prev_high < next_low:
            bearish_fvg_data.append({
                'top': next_low,
                'bottom': prev_high,
                'created_at': df.index[i]
            })
    
    bullish_fvg = pd.DataFrame(bullish_fvg_data, columns=['top', 'bottom', 'created_at'])
    bearish_fvg = pd.DataFrame(bearish_fvg_data, columns=['top', 'bottom', 'created_at'])
    
    return bullish_fvg, bearish_fvg


class FVGTracker:
    """Track Fair Value Gaps and Inversion FVGs for the strategy."""
    
    def __init__(self, lookback: int = 50):
        self.bullish_fvgs = []  # List of (top, bottom, created_idx, violated)
        self.bearish_fvgs = []  # List of (top, bottom, created_idx, violated)
        self.bullish_ifvgs = []  # Inverted bullish FVGs (now bearish zones)
        self.bearish_ifvgs = []  # Inverted bearish FVGs (now bullish zones)
        self.lookback = lookback
    
    def update(self, idx: int, opens: np.ndarray, highs: np.ndarray, 
               lows: np.ndarray, closes: np.ndarray):
        """Update FVG tracking with new bar data."""
        if idx < 2:
            return
        
        current_close = closes[idx]
        
        # Check for new FVGs (need at least 3 bars)
        prev_low = lows[idx - 1]
        next_high = highs[idx]  # Current bar is "next" relative to middle bar
        prev_high = highs[idx - 1]
        next_low = lows[idx]
        
        # Using bar at idx-2 as reference (middle bar of the 3-bar pattern)
        if idx >= 2:
            bar_minus_2_low = lows[idx - 2]
            bar_minus_2_high = highs[idx - 2]
            current_high = highs[idx]
            current_low = lows[idx]
            
            # Bullish FVG: bar[idx-2].low > bar[idx].high
            if bar_minus_2_low > current_high:
                self.bullish_fvgs.append({
                    'top': bar_minus_2_low,
                    'bottom': current_high,
                    'created_idx': idx - 1,
                    'violated': False
                })
            
            # Bearish FVG: bar[idx-2].high < bar[idx].low
            if bar_minus_2_high < current_low:
                self.bearish_fvgs.append({
                    'top': current_low,
                    'bottom': bar_minus_2_high,
                    'created_idx': idx - 1,
                    'violated': False
                })
        
        # Check for FVG violations and create IFVGs
        # Bullish FVG violated when price closes below bottom -> becomes bearish IFVG
        for fvg in self.bullish_fvgs:
            if not fvg['violated'] and current_close < fvg['bottom']:
                fvg['violated'] = True
                self.bullish_ifvgs.append({
                    'top': fvg['top'],
                    'bottom': fvg['bottom'],
                    'created_idx': idx,
                    'tested': False
                })
        
        # Bearish FVG violated when price closes above top -> becomes bullish IFVG
        for fvg in self.bearish_fvgs:
            if not fvg['violated'] and current_close > fvg['top']:
                fvg['violated'] = True
                self.bearish_ifvgs.append({
                    'top': fvg['top'],
                    'bottom': fvg['bottom'],
                    'created_idx': idx,
                    'tested': False
                })
        
        # Clean old FVGs (keep only last N)
        self.bullish_fvgs = self.bullish_fvgs[-self.lookback:]
        self.bearish_fvgs = self.bearish_fvgs[-self.lookback:]
        self.bullish_ifvgs = self.bullish_ifvgs[-self.lookback:]
        self.bearish_ifvgs = self.bearish_ifvgs[-self.lookback:]
    
    def get_bullish_ifvg_entry(self, current_price: float) -> Optional[dict]:
        """Get bullish IFVG zone for long entry (inverted bearish FVG)."""
        for ifvg in reversed(self.bearish_ifvgs):
            if not ifvg['tested'] and ifvg['bottom'] <= current_price <= ifvg['top']:
                return ifvg
        return None
    
    def get_bearish_ifvg_entry(self, current_price: float) -> Optional[dict]:
        """Get bearish IFVG zone for short entry (inverted bullish FVG)."""
        for ifvg in reversed(self.bullish_ifvgs):
            if not ifvg['tested'] and ifvg['bottom'] <= current_price <= ifvg['top']:
                return ifvg
        return None


# =============================================================================
# STRATEGY IMPLEMENTATION
# =============================================================================

class SilverBulletIFVGStrategy(Strategy):
    """
    Silver Bullet + IFVG Trading Strategy
    
    Parameters:
    - fractal_lookback: Lookback period for fractal high/low detection
    - rr_target: Risk-reward ratio for take profit
    - use_break_even: Enable break-even at 1R
    """
    
    fractal_lookback = 20
    rr_target = 2.0  # Default RR, will be tested with multiple values
    use_break_even = True
    
    def init(self):
        """Initialize indicators and tracking variables."""
        self.fvg_tracker = FVGTracker(lookback=50)
        
        # Pre-calculate fractal levels
        self.fractal_high = self.I(
            lambda x: pd.Series(x).rolling(self.fractal_lookback).max().values,
            self.data.High
        )
        self.fractal_low = self.I(
            lambda x: pd.Series(x).rolling(self.fractal_lookback).min().values,
            self.data.Low
        )
        
        # Track sweep signals
        self.last_buy_sweep_idx = -100
        self.last_sell_sweep_idx = -100
        
        # Track entry levels for break-even
        self.entry_price = None
        self.stop_loss = None
        self.take_profit = None
        self.breakeven_activated = False
        
    def is_trading_window(self, dt) -> bool:
        """Check if current time is within Silver Bullet window (9:00-10:00 CT)."""
        # Data is already in Chicago time based on typical NQ data
        current_time = dt.time() if hasattr(dt, 'time') else time(dt.hour, dt.minute)
        return time(9, 0) <= current_time < time(10, 0)
    
    def is_forced_close_time(self, dt) -> bool:
        """Check if it's time to force close all positions (15:00 CT)."""
        current_time = dt.time() if hasattr(dt, 'time') else time(dt.hour, dt.minute)
        return current_time >= time(15, 0)
    
    def get_swing_low(self, lookback: int = SWEEP_LOOKBACK_BARS) -> float:
        """Get recent swing low for stop loss."""
        return min(self.data.Low[-lookback:])
    
    def get_swing_high(self, lookback: int = SWEEP_LOOKBACK_BARS) -> float:
        """Get recent swing high for stop loss."""
        return max(self.data.High[-lookback:])
    
    def next(self):
        """Main strategy logic executed on each bar."""
        idx = len(self.data) - 1
        
        if idx < self.fractal_lookback + 5:
            return
        
        current_dt = self.data.index[-1]
        current_price = self.data.Close[-1]
        current_high = self.data.High[-1]
        current_low = self.data.Low[-1]
        
        # Update FVG tracker
        self.fvg_tracker.update(
            idx,
            self.data.Open,
            self.data.High,
            self.data.Low,
            self.data.Close
        )
        
        # Detect liquidity sweeps (skip if insufficient data)
        if len(self.fractal_high) > 1 and len(self.fractal_low) > 1:
            prev_fractal_high = self.fractal_high[-2]
            prev_fractal_low = self.fractal_low[-2]
            
            # Skip sweep detection if fractal values are NaN
            if not np.isnan(prev_fractal_high) and not np.isnan(prev_fractal_low):
                # Buy-side sweep: high wicks above fractal high, close below
                if current_high > prev_fractal_high and current_price < prev_fractal_high:
                    self.last_buy_sweep_idx = idx
                
                # Sell-side sweep: low wicks below fractal low, close above
                if current_low < prev_fractal_low and current_price > prev_fractal_low:
                    self.last_sell_sweep_idx = idx
        
        # Force close at 15:00
        if self.is_forced_close_time(current_dt) and self.position:
            self.position.close()
            self.entry_price = None
            self.stop_loss = None
            self.take_profit = None
            self.breakeven_activated = False
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
                    self.entry_price = None
                    self.stop_loss = None
                    self.take_profit = None
                    self.breakeven_activated = False
                    return
                if self.take_profit and current_high >= self.take_profit:
                    self.position.close()
                    self.entry_price = None
                    self.stop_loss = None
                    self.take_profit = None
                    self.breakeven_activated = False
                    return
            else:
                if self.stop_loss and current_high >= self.stop_loss:
                    self.position.close()
                    self.entry_price = None
                    self.stop_loss = None
                    self.take_profit = None
                    self.breakeven_activated = False
                    return
                if self.take_profit and current_low <= self.take_profit:
                    self.position.close()
                    self.entry_price = None
                    self.stop_loss = None
                    self.take_profit = None
                    self.breakeven_activated = False
                    return
        
        # Only enter during trading window
        if not self.is_trading_window(current_dt):
            return
        
        # Skip if already in position
        if self.position:
            return
        
        # LONG ENTRY: Sell-side sweep + bullish IFVG
        # Check if we had a recent sell-side sweep (within lookback bars)
        if idx - self.last_sell_sweep_idx <= SWEEP_LOOKBACK_BARS:
            # Look for bullish IFVG entry
            ifvg = self.fvg_tracker.get_bullish_ifvg_entry(current_price)
            if ifvg:
                swing_low = self.get_swing_low()
                risk = current_price - swing_low
                
                if risk > 0:
                    self.entry_price = current_price
                    self.stop_loss = swing_low
                    self.take_profit = current_price + (risk * self.rr_target)
                    self.breakeven_activated = False
                    ifvg['tested'] = True
                    
                    self.buy()
                    return
        
        # SHORT ENTRY: Buy-side sweep + bearish IFVG
        if idx - self.last_buy_sweep_idx <= SWEEP_LOOKBACK_BARS:
            # Look for bearish IFVG entry
            ifvg = self.fvg_tracker.get_bearish_ifvg_entry(current_price)
            if ifvg:
                swing_high = self.get_swing_high()
                risk = swing_high - current_price
                
                if risk > 0:
                    self.entry_price = current_price
                    self.stop_loss = swing_high
                    self.take_profit = current_price - (risk * self.rr_target)
                    self.breakeven_activated = False
                    ifvg['tested'] = True
                    
                    self.sell()
                    return


# =============================================================================
# PERFORMANCE METRICS
# =============================================================================

def calculate_metrics(stats) -> dict:
    """Calculate and format performance metrics."""
    equity_curve = stats['_equity_curve']['Equity']
    returns = equity_curve.pct_change().dropna()
    
    # Calculate metrics
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
    
    # Profit Factor calculation
    trades = stats.get('_trades', pd.DataFrame())
    if len(trades) > 0 and 'PnL' in trades.columns:
        gross_profit = trades[trades['PnL'] > 0]['PnL'].sum()
        gross_loss = abs(trades[trades['PnL'] < 0]['PnL'].sum())
        profit_factor = gross_profit / gross_loss if gross_loss > 0 else INFINITE_PROFIT_FACTOR
    else:
        profit_factor = 0
    
    # Max Drawdown
    max_dd = stats.get('Max. Drawdown [%]', 0)
    
    # Sharpe Ratio (annualized for 1-minute data)
    # Note: Standard annualization assumes normal distribution of returns
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


def plot_last_trades(stats, n_trades: int = 10):
    """Plot the last N trades on a price chart."""
    trades = stats.get('_trades', pd.DataFrame())
    equity = stats.get('_equity_curve', pd.DataFrame())
    
    if len(trades) == 0:
        print("No trades to plot.")
        return
    
    last_trades = trades.tail(n_trades)
    
    fig, axes = plt.subplots(2, 1, figsize=(14, 10))
    
    # Plot equity curve
    if len(equity) > 0:
        axes[0].plot(equity.index, equity['Equity'], label='Equity', color='blue')
        axes[0].set_title('Equity Curve')
        axes[0].set_xlabel('Date')
        axes[0].set_ylabel('Equity')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)
    
    # Plot trades
    if len(last_trades) > 0:
        colors = ['green' if pnl > 0 else 'red' for pnl in last_trades['PnL']]
        axes[1].bar(range(len(last_trades)), last_trades['PnL'], color=colors)
        axes[1].axhline(y=0, color='black', linestyle='-', linewidth=0.5)
        axes[1].set_title(f'Last {len(last_trades)} Trades P&L')
        axes[1].set_xlabel('Trade #')
        axes[1].set_ylabel('P&L')
        axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('last_trades.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("Trade plot saved to 'last_trades.png'")


# =============================================================================
# MAIN EXECUTION
# =============================================================================

def run_backtest(data_dir: str, years: list = None, rr_targets: list = None):
    """
    Run the backtest with specified parameters.
    
    Args:
        data_dir: Directory containing the data files
        years: List of years to test (default: [2025])
        rr_targets: List of RR ratios to test (default: [1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5])
    """
    if years is None:
        years = [2025]
    
    if rr_targets is None:
        rr_targets = [1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]
    
    # Load and combine data
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
        return
    
    data = pd.concat(all_data).sort_index()
    data = data[~data.index.duplicated(keep='first')]
    
    print(f"\nTotal data: {len(data)} bars from {data.index[0]} to {data.index[-1]}")
    
    # Run backtest for each RR target
    results = []
    best_stats = None
    best_sharpe = -float('inf')
    
    print("\n" + "=" * 60)
    print("Running backtests for different RR targets...")
    print("=" * 60)
    
    for rr in rr_targets:
        print(f"\nTesting RR = {rr}...")
        
        bt = Backtest(
            data,
            SilverBulletIFVGStrategy,
            cash=100000,
            commission=0.0002,  # 0.02% commission
            exclusive_orders=True
        )
        
        stats = bt.run(rr_target=rr)
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
    
    # Display summary table
    print("\n" + "=" * 60)
    print("RESULTS SUMMARY")
    print("=" * 60)
    
    results_df = pd.DataFrame(results)
    results_df = results_df[['RR Target', 'Win Rate (%)', 'Profit Factor', 
                             'Max Drawdown (%)', 'Sharpe Ratio', 'Total Trades']]
    print(results_df.to_string(index=False))
    
    # Plot last 10 trades from best performing configuration
    if best_stats is not None:
        print(f"\nPlotting last 10 trades from best configuration (Sharpe = {best_sharpe})...")
        plot_last_trades(best_stats, n_trades=10)
    
    return results_df, best_stats


if __name__ == '__main__':
    # Configuration
    DATA_DIR = os.path.dirname(os.path.abspath(__file__))
    YEARS_TO_TEST = [2025]  # Add more years as needed: [2023, 2024, 2025]
    RR_TARGETS = [1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]
    
    print("=" * 60)
    print("PBTrading Silver Bullet & IFVG Backtest Strategy")
    print("=" * 60)
    print(f"Data directory: {DATA_DIR}")
    print(f"Years to test: {YEARS_TO_TEST}")
    print(f"RR targets: {RR_TARGETS}")
    
    results, stats = run_backtest(DATA_DIR, YEARS_TO_TEST, RR_TARGETS)

#!/usr/bin/env python3
"""
Liquidity Sweep Multi-Timeframe Smart Money Concepts (SMC) Backtesting Strategy

This script implements a multi-timeframe SMC strategy based on:
1. M15: Liquidity sweep detection (wick-only break of swing high/low)
2. M5: Fair Value Gap (FVG) / Inversion FVG confirmation
3. M1: Entry execution with fixed 1:3 Risk/Reward

Author: Backtest-Trading
"""

import pandas as pd
import numpy as np
import zipfile
import os
from datetime import datetime
from typing import Tuple, Optional, List
import warnings
import argparse

# Filter only the specific FutureWarning from pandas resampling
warnings.filterwarnings('ignore', category=FutureWarning, module='pandas')


# Configuration
DATA_DIR = os.path.dirname(os.path.abspath(__file__))
SWING_LOOKBACK = 5  # Candles left and right for swing detection
FVG_LOOKBACK_CANDLES = 3  # M5 candles to look for FVG after sweep
RISK_REWARD_RATIO = 3.0  # 1:3 RR
SL_BUFFER_POINTS = 0.5  # Buffer for stop loss placement


def load_csv_data(filepath: str) -> pd.DataFrame:
    """
    Load CSV data from file (supports both .csv and .csv.zip formats).
    
    Args:
        filepath: Path to the CSV file or zip file
        
    Returns:
        DataFrame with parsed OHLCV data indexed by datetime
    """
    if filepath.endswith('.zip'):
        with zipfile.ZipFile(filepath, 'r') as z:
            # Find the CSV file inside the zip (exclude __MACOSX files)
            csv_files = [f for f in z.namelist() if f.endswith('.csv') and not f.startswith('__MACOSX')]
            if not csv_files:
                raise ValueError(f"No CSV file found in {filepath}")
            with z.open(csv_files[0]) as f:
                df = pd.read_csv(f, sep=';')
    else:
        df = pd.read_csv(filepath, sep=';')
    
    # Rename columns
    df.columns = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
    
    # Parse datetime
    df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%d/%m/%Y %H:%M:%S')
    df.set_index('Datetime', inplace=True)
    df.drop(['Date', 'Time'], axis=1, inplace=True)
    
    # Ensure numeric columns
    for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    df.sort_index(inplace=True)
    return df


def load_all_1m_data(years: List[int] = None) -> pd.DataFrame:
    """
    Load all 1-minute data for specified years.
    
    Args:
        years: List of years to load. If None, auto-detects available years.
        
    Returns:
        Combined DataFrame with all 1-minute data
    """
    if years is None:
        # Auto-detect available years from file system
        current_year = datetime.now().year
        # Search for data files in a reasonable range around current year
        search_start = 2010
        search_end = current_year + 2
        years = []
        for year in range(search_start, search_end + 1):
            zip_path = os.path.join(DATA_DIR, f"{year} 1m.csv.zip")
            csv_path = os.path.join(DATA_DIR, f"{year} 1m.csv")
            if os.path.exists(zip_path) or os.path.exists(csv_path):
                years.append(year)
        if not years:
            raise ValueError("No 1m data files found in directory!")
        years.sort()
    
    all_data = []
    
    for year in years:
        # Try zip file first, then plain CSV
        zip_path = os.path.join(DATA_DIR, f"{year} 1m.csv.zip")
        csv_path = os.path.join(DATA_DIR, f"{year} 1m.csv")
        
        if os.path.exists(zip_path):
            print(f"Loading {year} 1m data from zip...")
            df = load_csv_data(zip_path)
            all_data.append(df)
        elif os.path.exists(csv_path):
            print(f"Loading {year} 1m data from CSV...")
            df = load_csv_data(csv_path)
            all_data.append(df)
        else:
            print(f"Warning: No 1m data found for {year}")
    
    if not all_data:
        raise ValueError("No data loaded!")
    
    combined = pd.concat(all_data)
    combined.sort_index(inplace=True)
    combined = combined[~combined.index.duplicated(keep='first')]
    
    print(f"Total 1m candles loaded: {len(combined)}")
    print(f"Date range: {combined.index.min()} to {combined.index.max()}")
    
    return combined


def resample_to_timeframe(df_1m: pd.DataFrame, timeframe: str) -> pd.DataFrame:
    """
    Resample 1-minute data to higher timeframe.
    
    Args:
        df_1m: 1-minute DataFrame
        timeframe: Target timeframe ('5min', '15min', etc.)
        
    Returns:
        Resampled DataFrame
    """
    resampled = df_1m.resample(timeframe).agg({
        'Open': 'first',
        'High': 'max',
        'Low': 'min',
        'Close': 'last',
        'Volume': 'sum'
    }).dropna()
    
    return resampled


def identify_swing_highs_lows(df: pd.DataFrame, lookback: int = 5) -> pd.DataFrame:
    """
    Identify swing highs and swing lows on the given timeframe.
    A swing high/low is confirmed when we have 'lookback' candles on each side.
    
    Args:
        df: OHLCV DataFrame
        lookback: Number of candles to look left and right
        
    Returns:
        DataFrame with swing_high and swing_low columns
    """
    df = df.copy()
    df['swing_high'] = np.nan
    df['swing_low'] = np.nan
    
    highs = df['High'].values
    lows = df['Low'].values
    
    for i in range(lookback, len(df) - lookback):
        # Check for swing high
        is_swing_high = True
        current_high = highs[i]
        for j in range(i - lookback, i + lookback + 1):
            if j != i and highs[j] >= current_high:
                is_swing_high = False
                break
        if is_swing_high:
            df.iloc[i, df.columns.get_loc('swing_high')] = current_high
        
        # Check for swing low
        is_swing_low = True
        current_low = lows[i]
        for j in range(i - lookback, i + lookback + 1):
            if j != i and lows[j] <= current_low:
                is_swing_low = False
                break
        if is_swing_low:
            df.iloc[i, df.columns.get_loc('swing_low')] = current_low
    
    return df


def detect_liquidity_sweep(df_m15: pd.DataFrame, idx: int) -> Optional[dict]:
    """
    Detect liquidity sweep on M15 timeframe.
    
    A sweep occurs when:
    - Price breaks a previous swing high/low with wick only
    - The candle closes back inside the previous range
    
    Args:
        df_m15: M15 DataFrame with swing levels identified
        idx: Current candle index
        
    Returns:
        Dictionary with sweep info or None
    """
    if idx < 1:
        return None
    
    current_candle = df_m15.iloc[idx]
    
    # Look for the most recent swing high and swing low before current candle
    past_data = df_m15.iloc[:idx]
    
    # Find most recent swing high
    recent_swing_highs = past_data[past_data['swing_high'].notna()]
    recent_swing_lows = past_data[past_data['swing_low'].notna()]
    
    sweep_info = None
    
    # Check for bearish sweep (sweep of swing high)
    if len(recent_swing_highs) > 0:
        latest_swing_high = recent_swing_highs.iloc[-1]['swing_high']
        latest_swing_high_idx = recent_swing_highs.index[-1]
        
        # Price wicks above swing high but closes below it
        if (current_candle['High'] > latest_swing_high and 
            current_candle['Close'] < latest_swing_high and
            current_candle['Open'] < latest_swing_high):
            sweep_info = {
                'type': 'bearish',
                'sweep_level': latest_swing_high,
                'sweep_wick': current_candle['High'],
                'sweep_time': df_m15.index[idx],
                'swing_time': latest_swing_high_idx
            }
    
    # Check for bullish sweep (sweep of swing low)
    if len(recent_swing_lows) > 0:
        latest_swing_low = recent_swing_lows.iloc[-1]['swing_low']
        latest_swing_low_idx = recent_swing_lows.index[-1]
        
        # Price wicks below swing low but closes above it
        if (current_candle['Low'] < latest_swing_low and 
            current_candle['Close'] > latest_swing_low and
            current_candle['Open'] > latest_swing_low):
            # If we already have a bearish sweep, prefer the one with bigger wick
            if sweep_info is None:
                sweep_info = {
                    'type': 'bullish',
                    'sweep_level': latest_swing_low,
                    'sweep_wick': current_candle['Low'],
                    'sweep_time': df_m15.index[idx],
                    'swing_time': latest_swing_low_idx
                }
    
    return sweep_info


def detect_fvg(df_m5: pd.DataFrame, sweep_type: str, start_idx: int, max_candles: int = 3) -> Optional[dict]:
    """
    Detect Fair Value Gap (FVG) or Inversion FVG on M5 timeframe.
    
    FVG conditions:
    - Bullish FVG: Current candle's low > Previous candle's high (gap up)
    - Bearish FVG: Current candle's high < Previous candle's low (gap down)
    
    For bearish sweep -> look for bullish FVG (reversal)
    For bullish sweep -> look for bearish FVG (reversal)
    
    Args:
        df_m5: M5 DataFrame
        sweep_type: 'bearish' or 'bullish'
        start_idx: Starting index to look for FVG
        max_candles: Maximum candles to search
        
    Returns:
        Dictionary with FVG info or None
    """
    end_idx = min(start_idx + max_candles + 2, len(df_m5))
    
    for i in range(start_idx + 1, end_idx - 1):
        if i < 1:
            continue
            
        # We need 3 candles to identify FVG
        # Candle i-1, i, i+1
        prev_candle = df_m5.iloc[i - 1]
        curr_candle = df_m5.iloc[i]
        next_candle = df_m5.iloc[i + 1]
        
        # For bearish sweep, look for bullish FVG (sign of buying pressure)
        if sweep_type == 'bearish':
            # Bullish FVG: gap between candle i-1 high and candle i+1 low
            if next_candle['Low'] > prev_candle['High']:
                return {
                    'type': 'bullish_fvg',
                    'fvg_high': next_candle['Low'],
                    'fvg_low': prev_candle['High'],
                    'fvg_time': df_m5.index[i],
                    'fvg_candle_idx': i
                }
        
        # For bullish sweep, look for bearish FVG (sign of selling pressure)
        elif sweep_type == 'bullish':
            # Bearish FVG: gap between candle i-1 low and candle i+1 high
            if next_candle['High'] < prev_candle['Low']:
                return {
                    'type': 'bearish_fvg',
                    'fvg_high': prev_candle['Low'],
                    'fvg_low': next_candle['High'],
                    'fvg_time': df_m5.index[i],
                    'fvg_candle_idx': i
                }
    
    return None


def find_fvg_fill_entry(df_m1: pd.DataFrame, fvg_info: dict, sweep_info: dict, 
                         start_time: datetime, max_search_candles: int = 60) -> Optional[dict]:
    """
    Find entry point on M1 when FVG is filled.
    
    Args:
        df_m1: M1 DataFrame
        fvg_info: FVG information dictionary
        sweep_info: Sweep information dictionary
        start_time: Time to start searching from
        max_search_candles: Maximum M1 candles to search
        
    Returns:
        Dictionary with entry info or None
    """
    # Filter M1 data from start_time onwards
    mask = df_m1.index >= start_time
    search_data = df_m1.loc[mask].head(max_search_candles)
    
    if len(search_data) == 0:
        return None
    
    fvg_high = fvg_info['fvg_high']
    fvg_low = fvg_info['fvg_low']
    
    for i, (time, row) in enumerate(search_data.iterrows()):
        # For bullish FVG (after bearish sweep) - looking for SHORT entry
        if fvg_info['type'] == 'bullish_fvg':
            # Price fills the FVG by coming down into it
            if row['Close'] <= fvg_high and row['Close'] >= fvg_low:
                # Entry is SHORT
                entry_price = row['Close']
                stop_loss = sweep_info['sweep_wick'] + SL_BUFFER_POINTS
                risk = stop_loss - entry_price
                take_profit = entry_price - (risk * RISK_REWARD_RATIO)
                
                return {
                    'direction': 'SHORT',
                    'entry_time': time,
                    'entry_price': entry_price,
                    'stop_loss': stop_loss,
                    'take_profit': take_profit,
                    'risk': risk
                }
        
        # For bearish FVG (after bullish sweep) - looking for LONG entry
        elif fvg_info['type'] == 'bearish_fvg':
            # Price fills the FVG by coming up into it
            if row['Close'] >= fvg_low and row['Close'] <= fvg_high:
                # Entry is LONG
                entry_price = row['Close']
                stop_loss = sweep_info['sweep_wick'] - SL_BUFFER_POINTS
                risk = entry_price - stop_loss
                take_profit = entry_price + (risk * RISK_REWARD_RATIO)
                
                return {
                    'direction': 'LONG',
                    'entry_time': time,
                    'entry_price': entry_price,
                    'stop_loss': stop_loss,
                    'take_profit': take_profit,
                    'risk': risk
                }
    
    return None


def simulate_trade(df_m1: pd.DataFrame, trade: dict) -> dict:
    """
    Simulate trade execution and determine outcome.
    
    Args:
        df_m1: M1 DataFrame
        trade: Trade dictionary with entry details
        
    Returns:
        Updated trade dictionary with outcome
    """
    entry_time = trade['entry_time']
    entry_price = trade['entry_price']
    stop_loss = trade['stop_loss']
    take_profit = trade['take_profit']
    direction = trade['direction']
    
    # Get data after entry
    mask = df_m1.index > entry_time
    future_data = df_m1.loc[mask]
    
    trade['outcome'] = 'OPEN'
    trade['exit_time'] = None
    trade['exit_price'] = None
    trade['pnl'] = 0
    
    for time, row in future_data.iterrows():
        if direction == 'LONG':
            # Check stop loss first (more conservative)
            if row['Low'] <= stop_loss:
                trade['outcome'] = 'LOSS'
                trade['exit_time'] = time
                trade['exit_price'] = stop_loss
                trade['pnl'] = stop_loss - entry_price
                break
            # Check take profit
            elif row['High'] >= take_profit:
                trade['outcome'] = 'WIN'
                trade['exit_time'] = time
                trade['exit_price'] = take_profit
                trade['pnl'] = take_profit - entry_price
                break
                
        elif direction == 'SHORT':
            # Check stop loss first (more conservative)
            if row['High'] >= stop_loss:
                trade['outcome'] = 'LOSS'
                trade['exit_time'] = time
                trade['exit_price'] = stop_loss
                trade['pnl'] = entry_price - stop_loss
                break
            # Check take profit
            elif row['Low'] <= take_profit:
                trade['outcome'] = 'WIN'
                trade['exit_time'] = time
                trade['exit_price'] = take_profit
                trade['pnl'] = entry_price - take_profit
                break
    
    return trade


def run_backtest(df_m1: pd.DataFrame, verbose: bool = True) -> Tuple[List[dict], dict]:
    """
    Run the full backtest on the provided 1-minute data.
    
    Args:
        df_m1: 1-minute DataFrame
        verbose: Print progress updates
        
    Returns:
        Tuple of (trades list, statistics dictionary)
    """
    if verbose:
        print("\n" + "="*60)
        print("LIQUIDITY SWEEP SMC BACKTEST")
        print("="*60)
    
    # Resample data
    if verbose:
        print("\nResampling data to M5 and M15...")
    df_m5 = resample_to_timeframe(df_m1, '5min')
    df_m15 = resample_to_timeframe(df_m1, '15min')
    
    if verbose:
        print(f"M1 candles: {len(df_m1)}")
        print(f"M5 candles: {len(df_m5)}")
        print(f"M15 candles: {len(df_m15)}")
    
    # Identify swing highs and lows on M15
    if verbose:
        print("\nIdentifying swing highs and lows on M15...")
    df_m15 = identify_swing_highs_lows(df_m15, SWING_LOOKBACK)
    
    swing_highs_count = df_m15['swing_high'].notna().sum()
    swing_lows_count = df_m15['swing_low'].notna().sum()
    if verbose:
        print(f"Found {swing_highs_count} swing highs and {swing_lows_count} swing lows")
    
    trades = []
    last_trade_exit_time = None
    
    if verbose:
        print("\nScanning for liquidity sweeps...")
    
    # Iterate through M15 candles
    for i in range(SWING_LOOKBACK * 2, len(df_m15)):
        current_m15_time = df_m15.index[i]
        
        # Skip if we're still in a trade
        if last_trade_exit_time is not None and current_m15_time <= last_trade_exit_time:
            continue
        
        # Detect liquidity sweep
        sweep_info = detect_liquidity_sweep(df_m15, i)
        
        if sweep_info is None:
            continue
        
        # Find corresponding M5 data window
        sweep_time = sweep_info['sweep_time']
        try:
            # Use searchsorted for forward-fill behavior (bfill equivalent)
            m5_start_idx = df_m5.index.searchsorted(sweep_time, side='left')
            if m5_start_idx >= len(df_m5):
                continue
        except Exception:
            continue
        
        # Detect FVG on M5
        fvg_info = detect_fvg(df_m5, sweep_info['type'], m5_start_idx, FVG_LOOKBACK_CANDLES)
        
        if fvg_info is None:
            continue
        
        # Find entry on M1
        fvg_time = fvg_info['fvg_time']
        entry_info = find_fvg_fill_entry(df_m1, fvg_info, sweep_info, fvg_time)
        
        if entry_info is None:
            continue
        
        # Create trade record
        trade = {
            'sweep_type': sweep_info['type'],
            'sweep_level': sweep_info['sweep_level'],
            'sweep_wick': sweep_info['sweep_wick'],
            'sweep_time': sweep_info['sweep_time'],
            'fvg_type': fvg_info['type'],
            'fvg_time': fvg_info['fvg_time'],
            'fvg_high': fvg_info['fvg_high'],
            'fvg_low': fvg_info['fvg_low'],
            **entry_info
        }
        
        # Simulate trade
        trade = simulate_trade(df_m1, trade)
        trades.append(trade)
        
        if trade['exit_time'] is not None:
            last_trade_exit_time = trade['exit_time']
        
        if verbose and len(trades) % 100 == 0:
            print(f"Processed {len(trades)} trades...")
    
    # Calculate statistics
    stats = calculate_statistics(trades)
    
    return trades, stats


def calculate_statistics(trades: List[dict]) -> dict:
    """
    Calculate backtest statistics.
    
    Args:
        trades: List of trade dictionaries
        
    Returns:
        Statistics dictionary
    """
    if not trades:
        return {
            'total_trades': 0,
            'wins': 0,
            'losses': 0,
            'open_trades': 0,
            'win_rate': 0,
            'total_pnl': 0,
            'avg_pnl': 0,
            'max_drawdown': 0,
            'profit_factor': 0
        }
    
    completed_trades = [t for t in trades if t['outcome'] in ['WIN', 'LOSS']]
    wins = [t for t in completed_trades if t['outcome'] == 'WIN']
    losses = [t for t in completed_trades if t['outcome'] == 'LOSS']
    open_trades = [t for t in trades if t['outcome'] == 'OPEN']
    
    total_pnl = sum(t['pnl'] for t in completed_trades)
    cumulative_pnl = []
    running_pnl = 0
    for t in completed_trades:
        running_pnl += t['pnl']
        cumulative_pnl.append(running_pnl)
    
    # Calculate max drawdown
    max_drawdown = 0
    peak = 0
    for pnl in cumulative_pnl:
        if pnl > peak:
            peak = pnl
        drawdown = peak - pnl
        if drawdown > max_drawdown:
            max_drawdown = drawdown
    
    # Calculate profit factor
    gross_profit = sum(t['pnl'] for t in wins) if wins else 0
    gross_loss = abs(sum(t['pnl'] for t in losses)) if losses else 0
    # Use None when there are no losses (will be displayed as 'N/A')
    profit_factor = gross_profit / gross_loss if gross_loss > 0 else None
    
    win_rate = len(wins) / len(completed_trades) * 100 if completed_trades else 0
    
    return {
        'total_trades': len(trades),
        'completed_trades': len(completed_trades),
        'wins': len(wins),
        'losses': len(losses),
        'open_trades': len(open_trades),
        'win_rate': win_rate,
        'total_pnl': total_pnl,
        'avg_pnl': total_pnl / len(completed_trades) if completed_trades else 0,
        'max_drawdown': max_drawdown,
        'profit_factor': profit_factor,
        'gross_profit': gross_profit,
        'gross_loss': gross_loss,
        'long_trades': len([t for t in trades if t['direction'] == 'LONG']),
        'short_trades': len([t for t in trades if t['direction'] == 'SHORT'])
    }


def print_results(trades: List[dict], stats: dict):
    """
    Print backtest results.
    
    Args:
        trades: List of trade dictionaries
        stats: Statistics dictionary
    """
    print("\n" + "="*60)
    print("BACKTEST RESULTS")
    print("="*60)
    
    print(f"\n{'TRADE SUMMARY':^60}")
    print("-"*60)
    print(f"Total Trades:        {stats['total_trades']}")
    print(f"Completed Trades:    {stats['completed_trades']}")
    print(f"Open Trades:         {stats['open_trades']}")
    print(f"Long Trades:         {stats['long_trades']}")
    print(f"Short Trades:        {stats['short_trades']}")
    
    print(f"\n{'PERFORMANCE METRICS':^60}")
    print("-"*60)
    print(f"Wins:                {stats['wins']}")
    print(f"Losses:              {stats['losses']}")
    print(f"Win Rate:            {stats['win_rate']:.2f}%")
    pf_display = f"{stats['profit_factor']:.2f}" if stats['profit_factor'] is not None else "N/A (no losses)"
    print(f"Profit Factor:       {pf_display}")
    
    print(f"\n{'PNL ANALYSIS':^60}")
    print("-"*60)
    print(f"Total PnL:           {stats['total_pnl']:.2f} points")
    print(f"Average PnL/Trade:   {stats['avg_pnl']:.2f} points")
    print(f"Gross Profit:        {stats['gross_profit']:.2f} points")
    print(f"Gross Loss:          {stats['gross_loss']:.2f} points")
    print(f"Max Drawdown:        {stats['max_drawdown']:.2f} points")
    
    # Print sample trades
    if trades:
        print(f"\n{'SAMPLE TRADES (First 10)':^60}")
        print("-"*60)
        for i, trade in enumerate(trades[:10]):
            print(f"\nTrade #{i+1}:")
            print(f"  Direction: {trade['direction']}")
            print(f"  Entry Time: {trade['entry_time']}")
            print(f"  Entry Price: {trade['entry_price']:.2f}")
            print(f"  Stop Loss: {trade['stop_loss']:.2f}")
            print(f"  Take Profit: {trade['take_profit']:.2f}")
            print(f"  Outcome: {trade['outcome']}")
            print(f"  PnL: {trade['pnl']:.2f}")
    
    print("\n" + "="*60)


def export_trades_to_csv(trades: List[dict], filename: str = 'backtest_trades.csv'):
    """
    Export trades to CSV file.
    
    Args:
        trades: List of trade dictionaries
        filename: Output filename
    """
    if not trades:
        print("No trades to export.")
        return
    
    df = pd.DataFrame(trades)
    output_path = os.path.join(DATA_DIR, filename)
    df.to_csv(output_path, index=False)
    print(f"\nTrades exported to: {output_path}")


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description='Liquidity Sweep Multi-Timeframe SMC Strategy Backtester',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python liquidity_sweep_backtest.py --years 2024 2025
  python liquidity_sweep_backtest.py --years 2020 2021 2022 2023 2024
  python liquidity_sweep_backtest.py  # Auto-detects all available years
        '''
    )
    parser.add_argument(
        '--years', 
        type=int, 
        nargs='+',
        default=None,
        help='Years to backtest (e.g., --years 2024 2025). If not specified, auto-detects available years.'
    )
    parser.add_argument(
        '--rr-ratio',
        type=float,
        default=RISK_REWARD_RATIO,
        help=f'Risk/Reward ratio (default: {RISK_REWARD_RATIO})'
    )
    parser.add_argument(
        '--swing-lookback',
        type=int,
        default=SWING_LOOKBACK,
        help=f'Swing lookback period in candles (default: {SWING_LOOKBACK})'
    )
    parser.add_argument(
        '--no-export',
        action='store_true',
        help='Skip exporting trades to CSV'
    )
    return parser.parse_args()


def main():
    """Main function to run the backtest."""
    args = parse_arguments()
    
    # Update global parameters if provided via CLI
    global RISK_REWARD_RATIO, SWING_LOOKBACK
    RISK_REWARD_RATIO = args.rr_ratio
    SWING_LOOKBACK = args.swing_lookback
    
    print("="*60)
    print("LIQUIDITY SWEEP SMC STRATEGY BACKTEST")
    print("="*60)
    print(f"\nStrategy Parameters:")
    print(f"  - Swing Lookback: {SWING_LOOKBACK} candles")
    print(f"  - FVG Search Window: {FVG_LOOKBACK_CANDLES} M5 candles")
    print(f"  - Risk/Reward Ratio: 1:{RISK_REWARD_RATIO}")
    print(f"  - Stop Loss Buffer: {SL_BUFFER_POINTS} points")
    
    # Load data - use CLI args or auto-detect
    years_to_load = args.years
    
    if years_to_load:
        print(f"\nLoading 1-minute data for years: {years_to_load}")
    else:
        print("\nAuto-detecting available years...")
    
    df_m1 = load_all_1m_data(years=years_to_load)
    
    # Run backtest
    trades, stats = run_backtest(df_m1, verbose=True)
    
    # Print results
    print_results(trades, stats)
    
    # Export trades
    if not args.no_export:
        export_trades_to_csv(trades)
    
    return trades, stats


if __name__ == "__main__":
    trades, stats = main()

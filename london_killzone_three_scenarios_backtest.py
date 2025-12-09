#!/usr/bin/env python3
"""
London Killzone Three Scenarios Backtest
=========================================

This script implements three distinct FVG-based trading scenarios during the London Killzone
(01:00-04:00 Chicago Time) in NQ futures data:

Scenario 1: Liquidity Sweep + FVG (Turtle Soup)
    - Price sweeps beyond 12-candle high/low
    - Candle closes back inside range (rejection)
    - Immediate FVG forms after the sweep

Scenario 2: Inverted FVG (IFVG)
    - Standard FVG gets "flipped" by opposite price action
    - Bearish FVG becomes bullish support (and vice versa)
    - Entry on return to test the inverted zone

Scenario 3: Continuation FVG (Control Group)
    - Standard FVG without sweep or inversion
    - Simple trend continuation setups

All trades use:
- Entry: Price mitigation of FVG zone
- Stop Loss: Beyond the setup candle
- Take Profit: Fixed 2:1 Risk/Reward
- Session Close: 16:00 Chicago time (exit at market)
"""

import pandas as pd
import numpy as np
from datetime import datetime, time, timedelta
import os
from typing import List, Dict, Tuple, Optional
import warnings
import pytz

warnings.filterwarnings('ignore')

# ============================================================================
# CONSTANTS
# ============================================================================

# London Killzone hours (Chicago Time - CST/CDT)
KILLZONE_START = time(1, 0)   # 01:00 Chicago time
KILLZONE_END = time(4, 0)     # 04:00 Chicago time
SESSION_END = time(16, 0)     # 16:00 Chicago time - force close

# Analysis parameters
LOOKBACK_CANDLES = 12         # 60 minutes (12 * 5 minutes) for liquidity sweep
MITIGATION_WINDOW = 60        # Number of candles to check for mitigation (5 hours)
INVERSION_WINDOW = 40         # Number of candles to check for FVG inversion

# Risk-Reward ratio
RR_RATIO = 2.0                # Fixed 2:1 Risk/Reward

# Data years
DATA_YEARS = range(2018, 2026)  # 2018 to 2025

# Time zones
UTC = pytz.UTC
CHICAGO_TZ = pytz.timezone('America/Chicago')

# ============================================================================
# DATA LOADING AND PREPROCESSING
# ============================================================================

def load_all_data(base_path: str) -> pd.DataFrame:
    """
    Load all 5-minute NQ data from CSV files (2018-2025).
    Convert to Chicago time (CST/CDT).
    
    Args:
        base_path: Base directory containing the CSV files
        
    Returns:
        Combined DataFrame with all data in Chicago time
    """
    print("=" * 80)
    print("LOADING DATA")
    print("=" * 80)
    
    all_data = []
    
    for year in DATA_YEARS:
        filename = f"{year} 5m.csv"
        filepath = os.path.join(base_path, filename)
        
        if os.path.exists(filepath):
            print(f"Loading {filename}...")
            
            try:
                # Read CSV with semicolon separator
                df = pd.read_csv(filepath, sep=';')
                
                # Combine date and time columns
                df['DateTime'] = pd.to_datetime(
                    df['Column1'] + ' ' + df['Column2'],
                    format='%d/%m/%Y %H:%M:%S'
                )
                
                # Assume input is UTC, convert to Chicago time
                df['DateTime'] = df['DateTime'].dt.tz_localize(UTC).dt.tz_convert(CHICAGO_TZ)
                
                # Rename columns for clarity
                df = df.rename(columns={
                    'Column3': 'Open',
                    'Column4': 'High',
                    'Column5': 'Low',
                    'Column6': 'Close',
                    'Column7': 'Volume'
                })
                
                # Select relevant columns
                df = df[['DateTime', 'Open', 'High', 'Low', 'Close', 'Volume']]
                
                all_data.append(df)
                print(f"  Loaded {len(df)} rows from {year}")
            except Exception as e:
                print(f"  ERROR loading {filename}: {e}")
        else:
            print(f"  WARNING: {filename} not found, skipping...")
    
    if not all_data:
        raise FileNotFoundError("No data files found!")
    
    # Combine all data
    combined_df = pd.concat(all_data, ignore_index=True)
    
    # Sort by datetime
    combined_df = combined_df.sort_values('DateTime').reset_index(drop=True)
    
    print(f"\nTotal rows loaded: {len(combined_df)}")
    print(f"Date range: {combined_df['DateTime'].min()} to {combined_df['DateTime'].max()}")
    print("=" * 80)
    
    return combined_df


def filter_killzone_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Filter data for London Killzone hours (01:00-04:00 Chicago time).
    
    Args:
        df: DataFrame with DateTime column
        
    Returns:
        Filtered DataFrame
    """
    df['Time'] = df['DateTime'].dt.time
    killzone_df = df[(df['Time'] >= KILLZONE_START) & (df['Time'] < KILLZONE_END)].copy()
    
    print(f"\nKillzone data points: {len(killzone_df)}")
    print(f"Killzone hours: {KILLZONE_START} to {KILLZONE_END} Chicago time")
    
    return killzone_df


# ============================================================================
# FVG DETECTION
# ============================================================================

def detect_bullish_fvg(df: pd.DataFrame, idx: int) -> Optional[Tuple[float, float]]:
    """
    Detect bullish FVG at given index.
    Bullish FVG: High(n-1) < Low(n+1)
    
    Args:
        df: DataFrame with OHLC data
        idx: Index to check (this is candle 'n')
        
    Returns:
        Tuple of (lower_bound, upper_bound) or None
    """
    if idx < 1 or idx >= len(df) - 1:
        return None
    
    high_prev = df.iloc[idx - 1]['High']
    low_next = df.iloc[idx + 1]['Low']
    
    if high_prev < low_next:
        return (high_prev, low_next)
    
    return None


def detect_bearish_fvg(df: pd.DataFrame, idx: int) -> Optional[Tuple[float, float]]:
    """
    Detect bearish FVG at given index.
    Bearish FVG: Low(n-1) > High(n+1)
    
    Args:
        df: DataFrame with OHLC data
        idx: Index to check (this is candle 'n')
        
    Returns:
        Tuple of (upper_bound, lower_bound) or None
    """
    if idx < 1 or idx >= len(df) - 1:
        return None
    
    low_prev = df.iloc[idx - 1]['Low']
    high_next = df.iloc[idx + 1]['High']
    
    if low_prev > high_next:
        return (low_prev, high_next)
    
    return None


# ============================================================================
# SCENARIO 1: LIQUIDITY SWEEP + FVG (TURTLE SOUP)
# ============================================================================

def detect_liquidity_sweep_short(df: pd.DataFrame, idx: int) -> Optional[Dict]:
    """
    Detect bearish liquidity sweep + FVG setup.
    
    Criteria:
    - Price wicks ABOVE the highest high of last 12 candles
    - Current candle CLOSES BELOW that high (rejection)
    - Next candle creates a BEARISH FVG
    
    Args:
        df: DataFrame with OHLC data
        idx: Index to check (sweep candle)
        
    Returns:
        Dictionary with setup details or None
    """
    if idx < LOOKBACK_CANDLES + 1 or idx >= len(df) - 1:
        return None
    
    # Get the 12 previous candles (before current)
    lookback_start = idx - LOOKBACK_CANDLES
    lookback_end = idx
    lookback_high = df.iloc[lookback_start:lookback_end]['High'].max()
    
    current = df.iloc[idx]
    
    # Check if price wicked above the lookback high
    if current['High'] <= lookback_high:
        return None
    
    # Check if candle closed below the lookback high (rejection)
    if current['Close'] >= lookback_high:
        return None
    
    # Check if next candle creates a bearish FVG
    fvg = detect_bearish_fvg(df, idx)
    
    if fvg is None:
        return None
    
    # Valid Scenario 1 SHORT setup
    return {
        'type': 'SHORT',
        'scenario': 'Scenario 1: Sweep + FVG',
        'setup_idx': idx,
        'fvg_idx': idx,  # FVG is formed with idx as middle candle
        'fvg_upper': fvg[0],
        'fvg_lower': fvg[1],
        'sweep_level': lookback_high,
        'setup_candle_high': current['High'],
        'setup_candle_low': current['Low'],
        'datetime': df.iloc[idx]['DateTime']
    }


def detect_liquidity_sweep_long(df: pd.DataFrame, idx: int) -> Optional[Dict]:
    """
    Detect bullish liquidity sweep + FVG setup.
    
    Criteria:
    - Price wicks BELOW the lowest low of last 12 candles
    - Current candle CLOSES ABOVE that low (rejection)
    - Next candle creates a BULLISH FVG
    
    Args:
        df: DataFrame with OHLC data
        idx: Index to check (sweep candle)
        
    Returns:
        Dictionary with setup details or None
    """
    if idx < LOOKBACK_CANDLES + 1 or idx >= len(df) - 1:
        return None
    
    # Get the 12 previous candles (before current)
    lookback_start = idx - LOOKBACK_CANDLES
    lookback_end = idx
    lookback_low = df.iloc[lookback_start:lookback_end]['Low'].min()
    
    current = df.iloc[idx]
    
    # Check if price wicked below the lookback low
    if current['Low'] >= lookback_low:
        return None
    
    # Check if candle closed above the lookback low (rejection)
    if current['Close'] <= lookback_low:
        return None
    
    # Check if next candle creates a bullish FVG
    fvg = detect_bullish_fvg(df, idx)
    
    if fvg is None:
        return None
    
    # Valid Scenario 1 LONG setup
    return {
        'type': 'LONG',
        'scenario': 'Scenario 1: Sweep + FVG',
        'setup_idx': idx,
        'fvg_idx': idx,
        'fvg_upper': fvg[1],
        'fvg_lower': fvg[0],
        'sweep_level': lookback_low,
        'setup_candle_high': current['High'],
        'setup_candle_low': current['Low'],
        'datetime': df.iloc[idx]['DateTime']
    }


# ============================================================================
# SCENARIO 2: INVERTED FVG (IFVG)
# ============================================================================

def detect_inverted_fvg(df: pd.DataFrame, idx: int, existing_setups: List[Dict]) -> Optional[Dict]:
    """
    Detect Inverted FVG (IFVG).
    
    For LONG setup:
    - Find a previously identified BEARISH FVG
    - A subsequent candle CLOSES ABOVE the high boundary of this bearish FVG
    - The bearish FVG is now "inverted" and becomes a BUY zone
    
    For SHORT setup:
    - Find a previously identified BULLISH FVG
    - A subsequent candle CLOSES BELOW the low boundary of this bullish FVG
    - The bullish FVG is now "inverted" and becomes a SELL zone
    
    Args:
        df: DataFrame with OHLC data
        idx: Current index
        existing_setups: List of already detected Scenario 1 setups to avoid duplicates
        
    Returns:
        Dictionary with setup details or None
    """
    if idx < LOOKBACK_CANDLES + 2:
        return None
    
    current = df.iloc[idx]
    
    # Look back for potential FVGs that could be inverted
    lookback_start = max(0, idx - INVERSION_WINDOW)
    
    for check_idx in range(lookback_start, idx - 1):
        # Check for bearish FVG that gets inverted to bullish
        bearish_fvg = detect_bearish_fvg(df, check_idx)
        if bearish_fvg:
            fvg_high = bearish_fvg[0]
            fvg_low = bearish_fvg[1]
            
            # Check if current candle closes above the bearish FVG high (inversion)
            if current['Close'] > fvg_high:
                # This bearish FVG is now inverted to bullish
                # Make sure this isn't already part of a Scenario 1 setup
                is_duplicate = any(
                    s['fvg_idx'] == check_idx and s['type'] == 'LONG'
                    for s in existing_setups
                )
                
                if not is_duplicate:
                    return {
                        'type': 'LONG',
                        'scenario': 'Scenario 2: Inverted FVG',
                        'setup_idx': idx,  # Inversion candle
                        'fvg_idx': check_idx,  # Original FVG candle
                        'fvg_upper': fvg_high,
                        'fvg_lower': fvg_low,
                        'inversion_candle_high': current['High'],
                        'inversion_candle_low': current['Low'],
                        'datetime': df.iloc[idx]['DateTime']
                    }
        
        # Check for bullish FVG that gets inverted to bearish
        bullish_fvg = detect_bullish_fvg(df, check_idx)
        if bullish_fvg:
            fvg_low = bullish_fvg[0]
            fvg_high = bullish_fvg[1]
            
            # Check if current candle closes below the bullish FVG low (inversion)
            if current['Close'] < fvg_low:
                # This bullish FVG is now inverted to bearish
                is_duplicate = any(
                    s['fvg_idx'] == check_idx and s['type'] == 'SHORT'
                    for s in existing_setups
                )
                
                if not is_duplicate:
                    return {
                        'type': 'SHORT',
                        'scenario': 'Scenario 2: Inverted FVG',
                        'setup_idx': idx,  # Inversion candle
                        'fvg_idx': check_idx,  # Original FVG candle
                        'fvg_upper': fvg_high,
                        'fvg_lower': fvg_low,
                        'inversion_candle_high': current['High'],
                        'inversion_candle_low': current['Low'],
                        'datetime': df.iloc[idx]['DateTime']
                    }
    
    return None


# ============================================================================
# SCENARIO 3: CONTINUATION FVG (CONTROL GROUP)
# ============================================================================

def detect_continuation_fvg(df: pd.DataFrame, idx: int, existing_setups: List[Dict]) -> List[Dict]:
    """
    Detect Continuation FVG - standard FVG that doesn't match Scenarios 1 or 2.
    
    Args:
        df: DataFrame with OHLC data
        idx: Index to check
        existing_setups: Already detected setups to avoid duplicates
        
    Returns:
        List of setup dictionaries (can be both bullish and bearish)
    """
    if idx < 1 or idx >= len(df) - 1:
        return []
    
    setups = []
    
    # Check for bullish FVG
    bullish_fvg = detect_bullish_fvg(df, idx)
    if bullish_fvg:
        # Make sure not already classified as Scenario 1 or 2
        is_duplicate = any(
            s['fvg_idx'] == idx and s['type'] == 'LONG'
            for s in existing_setups
        )
        
        if not is_duplicate:
            current = df.iloc[idx]
            setups.append({
                'type': 'LONG',
                'scenario': 'Scenario 3: Continuation FVG',
                'setup_idx': idx - 1,  # Use the first candle of the FVG formation
                'fvg_idx': idx,
                'fvg_upper': bullish_fvg[1],
                'fvg_lower': bullish_fvg[0],
                'setup_candle_high': df.iloc[idx - 1]['High'],
                'setup_candle_low': df.iloc[idx - 1]['Low'],
                'datetime': df.iloc[idx]['DateTime']
            })
    
    # Check for bearish FVG
    bearish_fvg = detect_bearish_fvg(df, idx)
    if bearish_fvg:
        # Make sure not already classified as Scenario 1 or 2
        is_duplicate = any(
            s['fvg_idx'] == idx and s['type'] == 'SHORT'
            for s in existing_setups
        )
        
        if not is_duplicate:
            current = df.iloc[idx]
            setups.append({
                'type': 'SHORT',
                'scenario': 'Scenario 3: Continuation FVG',
                'setup_idx': idx - 1,
                'fvg_idx': idx,
                'fvg_upper': bearish_fvg[0],
                'fvg_lower': bearish_fvg[1],
                'setup_candle_high': df.iloc[idx - 1]['High'],
                'setup_candle_low': df.iloc[idx - 1]['Low'],
                'datetime': df.iloc[idx]['DateTime']
            })
    
    return setups


# ============================================================================
# TRADE EXECUTION AND MANAGEMENT
# ============================================================================

def check_mitigation(df: pd.DataFrame, setup: Dict, start_idx: int) -> Optional[int]:
    """
    Check if price mitigates (touches) the FVG zone within the mitigation window.
    
    Args:
        df: DataFrame with OHLC data
        setup: Setup dictionary
        start_idx: Index to start checking from
        
    Returns:
        Index where mitigation occurs, or None
    """
    fvg_upper = setup['fvg_upper']
    fvg_lower = setup['fvg_lower']
    
    end_idx = min(start_idx + MITIGATION_WINDOW, len(df))
    
    for idx in range(start_idx, end_idx):
        candle = df.iloc[idx]
        
        # Check if price touches the FVG zone
        if candle['Low'] <= fvg_upper and candle['High'] >= fvg_lower:
            return idx
    
    return None


def simulate_trade(df: pd.DataFrame, setup: Dict, entry_idx: int) -> Dict:
    """
    Simulate a trade from entry to exit.
    
    Entry: At FVG mitigation
    Stop Loss: Beyond setup candle (Scenario 1 & 3) or inversion candle (Scenario 2)
    Take Profit: 2:1 Risk/Reward
    Exit: At TP, SL, or 16:00 session close
    
    Args:
        df: DataFrame with OHLC data
        setup: Setup dictionary
        entry_idx: Index where entry occurs
        
    Returns:
        Trade result dictionary
    """
    entry_candle = df.iloc[entry_idx]
    entry_price = (setup['fvg_upper'] + setup['fvg_lower']) / 2  # Enter at FVG midpoint
    entry_datetime = entry_candle['DateTime']
    
    # Determine stop loss based on scenario
    if setup['scenario'].startswith('Scenario 2'):
        # IFVG: Stop beyond inversion candle
        if setup['type'] == 'LONG':
            stop_loss = setup['inversion_candle_low']
        else:
            stop_loss = setup['inversion_candle_high']
    else:
        # Scenarios 1 & 3: Stop beyond setup candle
        if setup['type'] == 'LONG':
            stop_loss = setup['setup_candle_low']
        else:
            stop_loss = setup['setup_candle_high']
    
    # Calculate risk and take profit
    if setup['type'] == 'LONG':
        risk = entry_price - stop_loss
        take_profit = entry_price + (risk * RR_RATIO)
    else:  # SHORT
        risk = stop_loss - entry_price
        take_profit = entry_price - (risk * RR_RATIO)
    
    # Initialize trade result
    trade = {
        'scenario': setup['scenario'],
        'type': setup['type'],
        'entry_datetime': entry_datetime,
        'entry_price': entry_price,
        'stop_loss': stop_loss,
        'take_profit': take_profit,
        'risk': risk,
        'exit_datetime': None,
        'exit_price': None,
        'pnl': 0,
        'pnl_points': 0,
        'result': None
    }
    
    # Get session date for 16:00 close check
    session_date = entry_datetime.date()
    session_close_time = CHICAGO_TZ.localize(datetime.combine(session_date, SESSION_END))
    
    # Simulate price movement after entry
    for idx in range(entry_idx + 1, len(df)):
        candle = df.iloc[idx]
        current_datetime = candle['DateTime']
        
        # Check for session close at 16:00
        if current_datetime >= session_close_time:
            trade['exit_datetime'] = current_datetime
            trade['exit_price'] = candle['Close']
            
            if setup['type'] == 'LONG':
                trade['pnl_points'] = trade['exit_price'] - entry_price
            else:
                trade['pnl_points'] = entry_price - trade['exit_price']
            
            trade['pnl'] = trade['pnl_points']
            trade['result'] = 'Session Close'
            break
        
        # Check for stop loss hit
        if setup['type'] == 'LONG':
            if candle['Low'] <= stop_loss:
                trade['exit_datetime'] = current_datetime
                trade['exit_price'] = stop_loss
                trade['pnl_points'] = stop_loss - entry_price
                trade['pnl'] = trade['pnl_points']
                trade['result'] = 'Stop Loss'
                break
        else:  # SHORT
            if candle['High'] >= stop_loss:
                trade['exit_datetime'] = current_datetime
                trade['exit_price'] = stop_loss
                trade['pnl_points'] = entry_price - stop_loss
                trade['pnl'] = trade['pnl_points']
                trade['result'] = 'Stop Loss'
                break
        
        # Check for take profit hit
        if setup['type'] == 'LONG':
            if candle['High'] >= take_profit:
                trade['exit_datetime'] = current_datetime
                trade['exit_price'] = take_profit
                trade['pnl_points'] = take_profit - entry_price
                trade['pnl'] = trade['pnl_points']
                trade['result'] = 'Take Profit'
                break
        else:  # SHORT
            if candle['Low'] <= take_profit:
                trade['exit_datetime'] = current_datetime
                trade['exit_price'] = take_profit
                trade['pnl_points'] = entry_price - take_profit
                trade['pnl'] = trade['pnl_points']
                trade['result'] = 'Take Profit'
                break
    
    # If no exit found, close at last available price
    if trade['exit_datetime'] is None:
        last_candle = df.iloc[-1]
        trade['exit_datetime'] = last_candle['DateTime']
        trade['exit_price'] = last_candle['Close']
        
        if setup['type'] == 'LONG':
            trade['pnl_points'] = trade['exit_price'] - entry_price
        else:
            trade['pnl_points'] = entry_price - trade['exit_price']
        
        trade['pnl'] = trade['pnl_points']
        trade['result'] = 'End of Data'
    
    return trade


# ============================================================================
# MAIN ANALYSIS
# ============================================================================

def detect_all_setups(df: pd.DataFrame) -> List[Dict]:
    """
    Detect all three scenarios of setups in the data.
    
    Args:
        df: DataFrame with OHLC data
        
    Returns:
        List of all detected setups
    """
    print("\n" + "=" * 80)
    print("DETECTING SETUPS")
    print("=" * 80)
    
    all_setups = []
    scenario1_setups = []
    scenario2_setups = []
    
    total_candles = len(df)
    
    for idx in range(LOOKBACK_CANDLES + 2, total_candles - 1):
        # Progress indicator
        if idx % 10000 == 0:
            print(f"Processing candle {idx}/{total_candles}...")
        
        # Scenario 1: Liquidity Sweep + FVG
        sweep_short = detect_liquidity_sweep_short(df, idx)
        if sweep_short:
            scenario1_setups.append(sweep_short)
            all_setups.append(sweep_short)
        
        sweep_long = detect_liquidity_sweep_long(df, idx)
        if sweep_long:
            scenario1_setups.append(sweep_long)
            all_setups.append(sweep_long)
        
        # Scenario 2: Inverted FVG
        ifvg = detect_inverted_fvg(df, idx, scenario1_setups)
        if ifvg:
            scenario2_setups.append(ifvg)
            all_setups.append(ifvg)
    
    # Scenario 3: Continuation FVG (process after Scenarios 1 & 2)
    print("\nDetecting Continuation FVGs (Scenario 3)...")
    for idx in range(1, total_candles - 1):
        if idx % 10000 == 0:
            print(f"Processing candle {idx}/{total_candles}...")
        
        continuation_setups = detect_continuation_fvg(df, idx, all_setups)
        all_setups.extend(continuation_setups)
    
    print(f"\nTotal setups detected: {len(all_setups)}")
    print(f"  Scenario 1 (Sweep + FVG): {len([s for s in all_setups if 'Scenario 1' in s['scenario']])}")
    print(f"  Scenario 2 (Inverted FVG): {len([s for s in all_setups if 'Scenario 2' in s['scenario']])}")
    print(f"  Scenario 3 (Continuation): {len([s for s in all_setups if 'Scenario 3' in s['scenario']])}")
    
    return all_setups


def backtest_scenarios(df: pd.DataFrame, setups: List[Dict]) -> pd.DataFrame:
    """
    Backtest all detected setups and generate trade results.
    
    Args:
        df: DataFrame with OHLC data
        setups: List of detected setups
        
    Returns:
        DataFrame with all trade results
    """
    print("\n" + "=" * 80)
    print("BACKTESTING TRADES")
    print("=" * 80)
    
    trades = []
    
    for i, setup in enumerate(setups):
        if (i + 1) % 100 == 0:
            print(f"Processing setup {i + 1}/{len(setups)}...")
        
        # Find mitigation
        start_idx = setup['setup_idx'] + 1
        mitigation_idx = check_mitigation(df, setup, start_idx)
        
        if mitigation_idx is not None:
            # Simulate trade
            trade = simulate_trade(df, setup, mitigation_idx)
            trades.append(trade)
    
    print(f"\nTotal trades executed: {len(trades)}")
    
    return pd.DataFrame(trades)


def calculate_statistics(trades_df: pd.DataFrame, scenario_name: str) -> Dict:
    """
    Calculate performance statistics for a scenario.
    
    Args:
        trades_df: DataFrame with trade results
        scenario_name: Name of the scenario
        
    Returns:
        Dictionary with statistics
    """
    if len(trades_df) == 0:
        return {
            'Scenario': scenario_name,
            'Total Trades': 0,
            'Win Rate (%)': 0,
            'Profit Factor': 0,
            'Avg PnL (points)': 0,
            'Total PnL': 0,
            'Max Consecutive Wins': 0,
            'Max Consecutive Losses': 0
        }
    
    # Basic statistics
    total_trades = len(trades_df)
    winning_trades = len(trades_df[trades_df['pnl'] > 0])
    losing_trades = len(trades_df[trades_df['pnl'] <= 0])
    
    win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
    
    total_wins = trades_df[trades_df['pnl'] > 0]['pnl'].sum()
    total_losses = abs(trades_df[trades_df['pnl'] <= 0]['pnl'].sum())
    
    profit_factor = (total_wins / total_losses) if total_losses > 0 else (total_wins if total_wins > 0 else 0)
    
    avg_pnl = trades_df['pnl_points'].mean()
    total_pnl = trades_df['pnl'].sum()
    
    # Calculate consecutive wins/losses
    results = (trades_df['pnl'] > 0).astype(int)
    max_consecutive_wins = 0
    max_consecutive_losses = 0
    current_wins = 0
    current_losses = 0
    
    for result in results:
        if result == 1:  # Win
            current_wins += 1
            current_losses = 0
            max_consecutive_wins = max(max_consecutive_wins, current_wins)
        else:  # Loss
            current_losses += 1
            current_wins = 0
            max_consecutive_losses = max(max_consecutive_losses, current_losses)
    
    return {
        'Scenario': scenario_name,
        'Total Trades': total_trades,
        'Win Rate (%)': round(win_rate, 2),
        'Profit Factor': round(profit_factor, 2),
        'Avg PnL (points)': round(avg_pnl, 2),
        'Total PnL': round(total_pnl, 2),
        'Max Consecutive Wins': max_consecutive_wins,
        'Max Consecutive Losses': max_consecutive_losses
    }


def generate_comparison_table(trades_df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate comparison table for all three scenarios.
    
    Args:
        trades_df: DataFrame with all trade results
        
    Returns:
        Comparison DataFrame
    """
    print("\n" + "=" * 80)
    print("GENERATING COMPARISON TABLE")
    print("=" * 80)
    
    scenarios = [
        'Scenario 1: Sweep + FVG',
        'Scenario 2: Inverted FVG',
        'Scenario 3: Continuation FVG'
    ]
    
    comparison = []
    
    for scenario in scenarios:
        scenario_trades = trades_df[trades_df['scenario'] == scenario]
        stats = calculate_statistics(scenario_trades, scenario)
        comparison.append(stats)
    
    comparison_df = pd.DataFrame(comparison)
    
    return comparison_df


def generate_monthly_breakdown(trades_df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate monthly breakdown of performance by scenario.
    
    Args:
        trades_df: DataFrame with all trade results
        
    Returns:
        Monthly breakdown DataFrame
    """
    trades_df['YearMonth'] = pd.to_datetime(trades_df['entry_datetime']).dt.to_period('M')
    
    monthly_stats = []
    
    for scenario in trades_df['scenario'].unique():
        scenario_trades = trades_df[trades_df['scenario'] == scenario]
        
        for period in scenario_trades['YearMonth'].unique():
            period_trades = scenario_trades[scenario_trades['YearMonth'] == period]
            
            monthly_stats.append({
                'Scenario': scenario,
                'Year-Month': str(period),
                'Trades': len(period_trades),
                'Win Rate (%)': round(len(period_trades[period_trades['pnl'] > 0]) / len(period_trades) * 100, 2) if len(period_trades) > 0 else 0,
                'Total PnL': round(period_trades['pnl'].sum(), 2)
            })
    
    return pd.DataFrame(monthly_stats)


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """
    Main execution function.
    """
    print("\n" + "=" * 80)
    print("LONDON KILLZONE THREE SCENARIOS BACKTEST")
    print("=" * 80)
    print(f"Analysis Period: 2018-2025")
    print(f"Timeframe: 5-minute")
    print(f"Killzone Hours: {KILLZONE_START} to {KILLZONE_END} Chicago Time")
    print(f"Session Close: {SESSION_END} Chicago Time")
    print(f"Risk/Reward: Fixed {RR_RATIO}:1")
    print("=" * 80)
    
    # Get the base path (current directory)
    base_path = os.path.dirname(os.path.abspath(__file__))
    
    # Load data
    df = load_all_data(base_path)
    
    # Filter for killzone hours
    killzone_df = filter_killzone_data(df)
    
    # Detect all setups
    setups = detect_all_setups(killzone_df)
    
    if len(setups) == 0:
        print("\nNo setups detected. Exiting.")
        return
    
    # Backtest all setups
    trades_df = backtest_scenarios(df, setups)
    
    if len(trades_df) == 0:
        print("\nNo trades executed. Exiting.")
        return
    
    # Generate comparison table
    comparison_df = generate_comparison_table(trades_df)
    
    # Display results
    print("\n" + "=" * 80)
    print("SCENARIO COMPARISON RESULTS")
    print("=" * 80)
    print(comparison_df.to_string(index=False))
    print("=" * 80)
    
    # Generate monthly breakdown
    monthly_df = generate_monthly_breakdown(trades_df)
    
    print("\n" + "=" * 80)
    print("MONTHLY BREAKDOWN (Sample - First 20 rows)")
    print("=" * 80)
    print(monthly_df.head(20).to_string(index=False))
    print("=" * 80)
    
    # Save detailed results to CSV
    output_file_trades = os.path.join(base_path, 'three_scenarios_detailed_trades.csv')
    output_file_comparison = os.path.join(base_path, 'three_scenarios_comparison.csv')
    output_file_monthly = os.path.join(base_path, 'three_scenarios_monthly_breakdown.csv')
    
    trades_df.to_csv(output_file_trades, index=False)
    comparison_df.to_csv(output_file_comparison, index=False)
    monthly_df.to_csv(output_file_monthly, index=False)
    
    print(f"\nDetailed trades saved to: {output_file_trades}")
    print(f"Comparison table saved to: {output_file_comparison}")
    print(f"Monthly breakdown saved to: {output_file_monthly}")
    
    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()

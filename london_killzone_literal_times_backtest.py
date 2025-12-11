#!/usr/bin/env python3
"""
London Killzone FVG Analysis - LITERAL TIMES
=============================================

This script analyzes Fair Value Gaps (FVG) during LITERAL hours 01:00-04:00
from the CSV files WITHOUT any timezone conversion.

IMPORTANT:
- Uses exact times from CSV files: 01:00, 01:05, 01:10... to 03:55
- NO timezone conversion - timestamps are used as-is
- CSV Format: Date;Time;Open;High;Low;Close;Volume
- Example: "10/11/2025;01:00:00;25469.5;25481.5;25463.25;25474.5;793"

Three Trading Scenarios:
========================
1. Liquidity Sweep + FVG (Turtle Soup)
   - Price sweeps beyond 12-candle high/low
   - Candle closes back inside range (rejection)
   - Immediate FVG forms after the sweep

2. Inverted FVG (IFVG)
   - Standard FVG gets "flipped" by opposite price action
   - Bearish FVG becomes bullish support (vice versa)
   - Entry on return to test the inverted zone

3. Continuation FVG (Control Group)
   - Standard FVG without sweep or inversion
   - Simple trend continuation setups

Trade Rules:
============
- Entry: Price mitigation of FVG zone
- Stop Loss: According to scenario rules
- Take Profit: Fixed 2:1 Risk/Reward
- Forced Exit: 16:00 (literal time from CSV)
"""

import pandas as pd
import numpy as np
from datetime import datetime, time, timedelta
import os
from typing import List, Dict, Tuple, Optional
import warnings

warnings.filterwarnings('ignore')

# ============================================================================
# CONSTANTS
# ============================================================================

# London Killzone hours (LITERAL TIMES from CSV)
KILLZONE_START = time(1, 0)   # 01:00 literal
KILLZONE_END = time(4, 0)     # 04:00 literal (03:55 is last candle)
SESSION_END = time(16, 0)     # 16:00 literal - force close

# Analysis parameters
LOOKBACK_CANDLES = 12         # 60 minutes (12 * 5 minutes) for liquidity sweep
MITIGATION_WINDOW = 60        # Number of candles to check for mitigation (5 hours)
INVERSION_WINDOW = 40         # Number of candles to check for FVG inversion

# Risk-Reward ratio
RR_RATIO = 2.0                # Fixed 2:1 Risk/Reward

# Data years
DATA_YEARS = range(2018, 2026)  # 2018 to 2025

# ============================================================================
# DATA LOADING AND PREPROCESSING
# ============================================================================

def load_all_data(base_path: str) -> pd.DataFrame:
    """
    Load all 5-minute NQ data from CSV files (2018-2025).
    Uses LITERAL times from CSV without any timezone conversion.
    
    Args:
        base_path: Base directory containing the CSV files
        
    Returns:
        Combined DataFrame with all data using literal times
    """
    print("=" * 80)
    print("LOADING DATA - LITERAL TIMES (NO TIMEZONE CONVERSION)")
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
                
                # Combine date and time columns - NO TIMEZONE CONVERSION
                df['DateTime'] = pd.to_datetime(
                    df['Column1'] + ' ' + df['Column2'],
                    format='%d/%m/%Y %H:%M:%S'
                )
                
                # Rename OHLCV columns
                df = df.rename(columns={
                    'Column3': 'Open',
                    'Column4': 'High',
                    'Column5': 'Low',
                    'Column6': 'Close',
                    'Column7': 'Volume'
                })
                
                # Keep only needed columns
                df = df[['DateTime', 'Open', 'High', 'Low', 'Close', 'Volume']]
                
                # Convert price columns to float
                for col in ['Open', 'High', 'Low', 'Close']:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                
                # Add date and time columns for filtering
                df['Date'] = df['DateTime'].dt.date
                df['Time'] = df['DateTime'].dt.time
                
                all_data.append(df)
                print(f"  ✓ Loaded {len(df)} rows from {year}")
                
            except Exception as e:
                print(f"  ✗ Error loading {filename}: {e}")
    
    if not all_data:
        raise ValueError("No data files found!")
    
    # Combine all years
    combined_df = pd.concat(all_data, ignore_index=True)
    combined_df = combined_df.sort_values('DateTime').reset_index(drop=True)
    
    print(f"\n✓ Total rows loaded: {len(combined_df):,}")
    print(f"✓ Date range: {combined_df['DateTime'].min()} to {combined_df['DateTime'].max()}")
    
    return combined_df


def filter_killzone_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Filter data to keep only candles during LITERAL killzone hours (01:00-03:55).
    
    Args:
        df: Full DataFrame
        
    Returns:
        Filtered DataFrame with only killzone candles
    """
    print("\n" + "=" * 80)
    print("FILTERING KILLZONE DATA (01:00-03:55 LITERAL)")
    print("=" * 80)
    
    # Filter by literal time (01:00:00 to 03:55:00)
    mask = (df['Time'] >= KILLZONE_START) & (df['Time'] < KILLZONE_END)
    killzone_df = df[mask].copy()
    
    print(f"✓ Killzone candles: {len(killzone_df):,} (from {len(df):,} total)")
    print(f"✓ Percentage: {100 * len(killzone_df) / len(df):.2f}%")
    
    # Show time distribution
    time_counts = killzone_df['Time'].value_counts().sort_index()
    print(f"\n✓ Sample of time distribution:")
    for t in list(time_counts.index)[:5]:
        print(f"  {t}: {time_counts[t]} candles")
    
    return killzone_df


# ============================================================================
# FVG DETECTION
# ============================================================================

def detect_fvgs(df: pd.DataFrame) -> pd.DataFrame:
    """
    Detect Fair Value Gaps (FVG) in the data.
    
    A FVG occurs when there's a gap between three consecutive candles:
    - Bullish FVG: High of candle n-1 < Low of candle n+1 (gap up)
    - Bearish FVG: Low of candle n-1 > High of candle n+1 (gap down)
    
    Args:
        df: DataFrame with OHLC data
        
    Returns:
        DataFrame with FVG information added
    """
    print("\n" + "=" * 80)
    print("DETECTING FAIR VALUE GAPS")
    print("=" * 80)
    
    df = df.copy()
    
    # Initialize FVG columns
    df['IsFVG'] = False
    df['FVGType'] = None  # 'Bullish' or 'Bearish'
    df['FVGTop'] = np.nan
    df['FVGBottom'] = np.nan
    df['FVGSize'] = np.nan
    
    # Need at least 3 candles
    for i in range(1, len(df) - 1):
        # Get three consecutive candles
        prev_high = df.iloc[i - 1]['High']
        prev_low = df.iloc[i - 1]['Low']
        next_high = df.iloc[i + 1]['High']
        next_low = df.iloc[i + 1]['Low']
        
        # Check for Bullish FVG (gap up)
        if prev_high < next_low:
            df.at[df.index[i], 'IsFVG'] = True
            df.at[df.index[i], 'FVGType'] = 'Bullish'
            df.at[df.index[i], 'FVGBottom'] = prev_high
            df.at[df.index[i], 'FVGTop'] = next_low
            df.at[df.index[i], 'FVGSize'] = next_low - prev_high
        
        # Check for Bearish FVG (gap down)
        elif prev_low > next_high:
            df.at[df.index[i], 'IsFVG'] = True
            df.at[df.index[i], 'FVGType'] = 'Bearish'
            df.at[df.index[i], 'FVGTop'] = prev_low
            df.at[df.index[i], 'FVGBottom'] = next_high
            df.at[df.index[i], 'FVGSize'] = prev_low - next_high
    
    num_fvgs = df['IsFVG'].sum()
    num_bullish = (df['FVGType'] == 'Bullish').sum()
    num_bearish = (df['FVGType'] == 'Bearish').sum()
    
    print(f"✓ Total FVGs detected: {num_fvgs}")
    print(f"  - Bullish FVGs: {num_bullish}")
    print(f"  - Bearish FVGs: {num_bearish}")
    
    if num_fvgs > 0:
        avg_size = df[df['IsFVG']]['FVGSize'].mean()
        print(f"  - Average FVG size: {avg_size:.2f} points")
    
    return df


# ============================================================================
# SCENARIO 1: LIQUIDITY SWEEP + FVG
# ============================================================================

def detect_liquidity_sweep(df: pd.DataFrame, fvg_idx: int) -> Optional[Dict]:
    """
    Detect if an FVG was preceded by a liquidity sweep.
    
    A liquidity sweep occurs when:
    1. Price breaks beyond the high/low of the last N candles
    2. The candle closes back inside the range (rejection)
    3. An FVG forms immediately after
    
    Args:
        df: DataFrame with OHLC data
        fvg_idx: Index value (not position) of the FVG candle
        
    Returns:
        Dict with sweep info if detected, None otherwise
    """
    # Get position in DataFrame
    try:
        fvg_pos = df.index.get_loc(fvg_idx)
    except KeyError:
        return None
    
    # Need enough lookback data
    if fvg_pos < LOOKBACK_CANDLES + 1:
        return None
    
    fvg_type = df.loc[fvg_idx, 'FVGType']
    
    # Get the candle before the FVG (the potential sweep candle)
    sweep_pos = fvg_pos - 1
    if sweep_pos < 0:
        return None
    
    sweep_idx = df.index[sweep_pos]
    sweep_candle = df.loc[sweep_idx]
    
    # Get lookback range (excluding sweep candle)
    lookback_start = max(0, sweep_pos - LOOKBACK_CANDLES)
    lookback_end = sweep_pos
    lookback_data = df.iloc[lookback_start:lookback_end]
    
    # For Bullish FVG: look for bullish sweep (sweep above high, close inside)
    if fvg_type == 'Bullish':
        lookback_high = lookback_data['High'].max()
        
        # Check if sweep candle broke above and closed inside
        if sweep_candle['High'] > lookback_high and sweep_candle['Close'] < lookback_high:
            return {
                'type': 'Bullish',
                'sweep_high': sweep_candle['High'],
                'range_high': lookback_high,
                'sweep_candle_idx': sweep_idx
            }
    
    # For Bearish FVG: look for bearish sweep (sweep below low, close inside)
    elif fvg_type == 'Bearish':
        lookback_low = lookback_data['Low'].min()
        
        # Check if sweep candle broke below and closed inside
        if sweep_candle['Low'] < lookback_low and sweep_candle['Close'] > lookback_low:
            return {
                'type': 'Bearish',
                'sweep_low': sweep_candle['Low'],
                'range_low': lookback_low,
                'sweep_candle_idx': sweep_idx
            }
    
    return None


def find_scenario1_setups(df: pd.DataFrame) -> List[Dict]:
    """
    Find Scenario 1 setups: Liquidity Sweep + FVG.
    
    Args:
        df: DataFrame with FVG data
        
    Returns:
        List of setup dictionaries
    """
    print("\n" + "=" * 80)
    print("SCENARIO 1: LIQUIDITY SWEEP + FVG")
    print("=" * 80)
    
    setups = []
    fvg_indices = df[df['IsFVG']].index.tolist()
    
    for fvg_idx in fvg_indices:
        sweep_info = detect_liquidity_sweep(df, fvg_idx)
        
        if sweep_info:
            fvg_data = df.loc[fvg_idx]
            
            setup = {
                'scenario': 'Scenario1_Sweep',
                'fvg_idx': fvg_idx,
                'fvg_datetime': fvg_data['DateTime'],
                'fvg_type': fvg_data['FVGType'],
                'fvg_top': fvg_data['FVGTop'],
                'fvg_bottom': fvg_data['FVGBottom'],
                'sweep_info': sweep_info
            }
            
            setups.append(setup)
    
    print(f"✓ Scenario 1 setups found: {len(setups)}")
    return setups


# ============================================================================
# SCENARIO 2: INVERTED FVG (IFVG)
# ============================================================================

def check_fvg_inversion(df: pd.DataFrame, fvg_idx: int) -> Optional[Dict]:
    """
    Check if an FVG gets inverted (flipped) by opposite price action.
    
    An inversion occurs when:
    - Bearish FVG: Price breaks above it and holds (becomes support)
    - Bullish FVG: Price breaks below it and holds (becomes resistance)
    
    Args:
        df: DataFrame with OHLC data
        fvg_idx: Index value (not position) of the FVG candle
        
    Returns:
        Dict with inversion info if detected, None otherwise
    """
    # Get position in DataFrame
    try:
        fvg_pos = df.index.get_loc(fvg_idx)
    except KeyError:
        return None
    
    # Need enough forward data
    if fvg_pos + INVERSION_WINDOW >= len(df):
        return None
    
    fvg_data = df.loc[fvg_idx]
    fvg_type = fvg_data['FVGType']
    fvg_top = fvg_data['FVGTop']
    fvg_bottom = fvg_data['FVGBottom']
    
    # Look forward for inversion
    forward_data = df.iloc[fvg_pos + 1:fvg_pos + 1 + INVERSION_WINDOW]
    
    # For Bearish FVG: look for price breaking above and holding
    if fvg_type == 'Bearish':
        # Find candles that break above FVG
        break_candles = forward_data[forward_data['Close'] > fvg_top]
        
        if len(break_candles) > 0:
            break_idx = break_candles.index[0]
            break_pos = df.index.get_loc(break_idx)
            # Check if subsequent candles hold above
            after_break = df.iloc[break_pos:fvg_pos + 1 + INVERSION_WINDOW]
            
            # Consider inverted if majority of closes are above FVG bottom
            holds = (after_break['Low'] >= fvg_bottom).sum()
            total = len(after_break)
            
            if holds / total >= 0.6:  # 60% threshold
                return {
                    'original_type': 'Bearish',
                    'inverted_type': 'Bullish',
                    'break_idx': break_idx,
                    'break_datetime': df.loc[break_idx, 'DateTime']
                }
    
    # For Bullish FVG: look for price breaking below and holding
    elif fvg_type == 'Bullish':
        # Find candles that break below FVG
        break_candles = forward_data[forward_data['Close'] < fvg_bottom]
        
        if len(break_candles) > 0:
            break_idx = break_candles.index[0]
            break_pos = df.index.get_loc(break_idx)
            # Check if subsequent candles hold below
            after_break = df.iloc[break_pos:fvg_pos + 1 + INVERSION_WINDOW]
            
            # Consider inverted if majority of closes are below FVG top
            holds = (after_break['High'] <= fvg_top).sum()
            total = len(after_break)
            
            if holds / total >= 0.6:  # 60% threshold
                return {
                    'original_type': 'Bullish',
                    'inverted_type': 'Bearish',
                    'break_idx': break_idx,
                    'break_datetime': df.loc[break_idx, 'DateTime']
                }
    
    return None


def find_scenario2_setups(df: pd.DataFrame) -> List[Dict]:
    """
    Find Scenario 2 setups: Inverted FVG (IFVG).
    
    Args:
        df: DataFrame with FVG data
        
    Returns:
        List of setup dictionaries
    """
    print("\n" + "=" * 80)
    print("SCENARIO 2: INVERTED FVG (IFVG)")
    print("=" * 80)
    
    setups = []
    fvg_indices = df[df['IsFVG']].index.tolist()
    
    for fvg_idx in fvg_indices:
        inversion_info = check_fvg_inversion(df, fvg_idx)
        
        if inversion_info:
            fvg_data = df.loc[fvg_idx]
            
            setup = {
                'scenario': 'Scenario2_IFVG',
                'fvg_idx': fvg_idx,
                'fvg_datetime': fvg_data['DateTime'],
                'fvg_type': fvg_data['FVGType'],
                'fvg_top': fvg_data['FVGTop'],
                'fvg_bottom': fvg_data['FVGBottom'],
                'inversion_info': inversion_info
            }
            
            setups.append(setup)
    
    print(f"✓ Scenario 2 setups found: {len(setups)}")
    return setups


# ============================================================================
# SCENARIO 3: CONTINUATION FVG (CONTROL)
# ============================================================================

def find_scenario3_setups(df: pd.DataFrame, scenario1_fvgs: set, scenario2_fvgs: set) -> List[Dict]:
    """
    Find Scenario 3 setups: Simple continuation FVGs (control group).
    These are FVGs that don't qualify for Scenario 1 or 2.
    
    Args:
        df: DataFrame with FVG data
        scenario1_fvgs: Set of FVG indices used in Scenario 1
        scenario2_fvgs: Set of FVG indices used in Scenario 2
        
    Returns:
        List of setup dictionaries
    """
    print("\n" + "=" * 80)
    print("SCENARIO 3: CONTINUATION FVG (CONTROL)")
    print("=" * 80)
    
    setups = []
    fvg_indices = df[df['IsFVG']].index.tolist()
    
    for fvg_idx in fvg_indices:
        # Skip if already used in Scenario 1 or 2
        if fvg_idx in scenario1_fvgs or fvg_idx in scenario2_fvgs:
            continue
        
        fvg_data = df.loc[fvg_idx]
        
        setup = {
            'scenario': 'Scenario3_Continuation',
            'fvg_idx': fvg_idx,
            'fvg_datetime': fvg_data['DateTime'],
            'fvg_type': fvg_data['FVGType'],
            'fvg_top': fvg_data['FVGTop'],
            'fvg_bottom': fvg_data['FVGBottom']
        }
        
        setups.append(setup)
    
    print(f"✓ Scenario 3 setups found: {len(setups)}")
    return setups


# ============================================================================
# TRADE SIMULATION
# ============================================================================

def simulate_trade(df: pd.DataFrame, setup: Dict) -> Dict:
    """
    Simulate a trade based on a setup.
    
    Entry: Price mitigates (touches) the FVG zone
    Stop Loss: Based on scenario rules
    Take Profit: 2:1 Risk/Reward
    Exit: Forced at 16:00 literal time if not closed
    
    Args:
        df: Full DataFrame
        setup: Setup dictionary
        
    Returns:
        Trade result dictionary
    """
    fvg_idx = setup['fvg_idx']
    fvg_type = setup['fvg_type']
    fvg_top = setup['fvg_top']
    fvg_bottom = setup['fvg_bottom']
    scenario = setup['scenario']
    
    # Get position in DataFrame
    try:
        fvg_pos = df.index.get_loc(fvg_idx)
    except KeyError:
        return {
            'scenario': scenario,
            'status': 'No Entry',
            'entry_datetime': None,
            'entry_price': None,
            'exit_datetime': None,
            'exit_price': None,
            'pnl_points': 0,
            'exit_reason': 'FVG Index Not Found'
        }
    
    # Start looking for entry after FVG forms
    start_pos = fvg_pos + 2  # Skip the FVG candle itself
    end_pos = min(start_pos + MITIGATION_WINDOW, len(df))
    
    # Find mitigation (entry)
    entry_pos = None
    entry_price = None
    
    for i in range(start_pos, end_pos):
        candle = df.iloc[i]
        
        # Check if price touches FVG zone
        if fvg_type == 'Bullish':
            # For bullish FVG, wait for price to drop into zone
            if candle['Low'] <= fvg_top and candle['Low'] >= fvg_bottom:
                entry_pos = i
                entry_price = (fvg_top + fvg_bottom) / 2  # Enter at mid-point
                break
        
        elif fvg_type == 'Bearish':
            # For bearish FVG, wait for price to rise into zone
            if candle['High'] >= fvg_bottom and candle['High'] <= fvg_top:
                entry_pos = i
                entry_price = (fvg_top + fvg_bottom) / 2  # Enter at mid-point
                break
    
    # No entry found
    if entry_pos is None:
        return {
            'scenario': scenario,
            'status': 'No Entry',
            'entry_datetime': None,
            'entry_price': None,
            'exit_datetime': None,
            'exit_price': None,
            'pnl': 0,
            'pnl_points': 0,
            'exit_reason': 'No Mitigation'
        }
    
    # Set stop loss based on scenario
    if scenario == 'Scenario1_Sweep':
        # Stop beyond sweep level
        if fvg_type == 'Bullish':
            # For bullish FVG, sweep was high, so stop below FVG
            stop_loss = fvg_bottom - 10
        else:
            # For bearish FVG, sweep was low, so stop above FVG
            stop_loss = fvg_top + 10
    
    elif scenario == 'Scenario2_IFVG':
        # Stop beyond the original FVG
        if fvg_type == 'Bullish':
            stop_loss = fvg_bottom - 10
        else:
            stop_loss = fvg_top + 10
    
    else:  # Scenario 3
        # Stop beyond FVG zone
        if fvg_type == 'Bullish':
            stop_loss = fvg_bottom - 10
        else:
            stop_loss = fvg_top + 10
    
    # Calculate take profit (2:1 RR)
    risk = abs(entry_price - stop_loss)
    
    if fvg_type == 'Bullish':
        take_profit = entry_price + (risk * RR_RATIO)
        direction = 'Long'
    else:
        take_profit = entry_price - (risk * RR_RATIO)
        direction = 'Short'
    
    # Monitor trade
    entry_datetime = df.iloc[entry_pos]['DateTime']
    
    for i in range(entry_pos + 1, len(df)):
        candle = df.iloc[i]
        candle_time = candle['Time']
        
        # Check for forced exit at 16:00
        if candle_time >= SESSION_END:
            exit_price = candle['Close']
            
            if direction == 'Long':
                pnl_points = exit_price - entry_price
            else:
                pnl_points = entry_price - exit_price
            
            return {
                'scenario': scenario,
                'status': 'Closed',
                'entry_datetime': entry_datetime,
                'entry_price': entry_price,
                'exit_datetime': candle['DateTime'],
                'exit_price': exit_price,
                'pnl_points': pnl_points,
                'exit_reason': 'Session Close (16:00)',
                'direction': direction,
                'stop_loss': stop_loss,
                'take_profit': take_profit
            }
        
        # Check for stop loss hit
        if direction == 'Long':
            if candle['Low'] <= stop_loss:
                pnl_points = stop_loss - entry_price
                
                return {
                    'scenario': scenario,
                    'status': 'Closed',
                    'entry_datetime': entry_datetime,
                    'entry_price': entry_price,
                    'exit_datetime': candle['DateTime'],
                    'exit_price': stop_loss,
                    'pnl_points': pnl_points,
                    'exit_reason': 'Stop Loss',
                    'direction': direction,
                    'stop_loss': stop_loss,
                    'take_profit': take_profit
                }
            
            # Check for take profit hit
            if candle['High'] >= take_profit:
                pnl_points = take_profit - entry_price
                
                return {
                    'scenario': scenario,
                    'status': 'Closed',
                    'entry_datetime': entry_datetime,
                    'entry_price': entry_price,
                    'exit_datetime': candle['DateTime'],
                    'exit_price': take_profit,
                    'pnl_points': pnl_points,
                    'exit_reason': 'Take Profit',
                    'direction': direction,
                    'stop_loss': stop_loss,
                    'take_profit': take_profit
                }
        
        else:  # Short
            if candle['High'] >= stop_loss:
                pnl_points = entry_price - stop_loss
                
                return {
                    'scenario': scenario,
                    'status': 'Closed',
                    'entry_datetime': entry_datetime,
                    'entry_price': entry_price,
                    'exit_datetime': candle['DateTime'],
                    'exit_price': stop_loss,
                    'pnl_points': pnl_points,
                    'exit_reason': 'Stop Loss',
                    'direction': direction,
                    'stop_loss': stop_loss,
                    'take_profit': take_profit
                }
            
            # Check for take profit hit
            if candle['Low'] <= take_profit:
                pnl_points = entry_price - take_profit
                
                return {
                    'scenario': scenario,
                    'status': 'Closed',
                    'entry_datetime': entry_datetime,
                    'entry_price': entry_price,
                    'exit_datetime': candle['DateTime'],
                    'exit_price': take_profit,
                    'pnl_points': pnl_points,
                    'exit_reason': 'Take Profit',
                    'direction': direction,
                    'stop_loss': stop_loss,
                    'take_profit': take_profit
                }
    
    # Trade still open at end of data
    return {
        'scenario': scenario,
        'status': 'Open',
        'entry_datetime': entry_datetime,
        'entry_price': entry_price,
        'exit_datetime': None,
        'exit_price': None,
        'pnl_points': 0,
        'exit_reason': 'Still Open',
        'direction': direction,
        'stop_loss': stop_loss,
        'take_profit': take_profit
    }


def backtest_scenario(df: pd.DataFrame, setups: List[Dict]) -> pd.DataFrame:
    """
    Backtest all setups for a scenario.
    
    Args:
        df: Full DataFrame
        setups: List of setup dictionaries
        
    Returns:
        DataFrame with trade results
    """
    trades = []
    
    for setup in setups:
        trade = simulate_trade(df, setup)
        trades.append(trade)
    
    return pd.DataFrame(trades)


# ============================================================================
# RESULTS ANALYSIS
# ============================================================================

def analyze_results(trades_df: pd.DataFrame, scenario_name: str):
    """
    Analyze and print results for a scenario.
    
    Args:
        trades_df: DataFrame with trade results
        scenario_name: Name of the scenario
    """
    print(f"\n{'=' * 80}")
    print(f"{scenario_name} - RESULTS")
    print(f"{'=' * 80}")
    
    if len(trades_df) == 0:
        print("No trades executed.")
        return
    
    # Filter closed trades
    closed_trades = trades_df[trades_df['status'] == 'Closed'].copy()
    
    if len(closed_trades) == 0:
        print("No closed trades.")
        return
    
    # Calculate statistics
    total_trades = len(closed_trades)
    winning_trades = len(closed_trades[closed_trades['pnl_points'] > 0])
    losing_trades = len(closed_trades[closed_trades['pnl_points'] < 0])
    breakeven_trades = len(closed_trades[closed_trades['pnl_points'] == 0])
    
    win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
    
    total_pnl = closed_trades['pnl_points'].sum()
    avg_pnl = closed_trades['pnl_points'].mean()
    
    avg_winner = closed_trades[closed_trades['pnl_points'] > 0]['pnl_points'].mean() if winning_trades > 0 else 0
    avg_loser = closed_trades[closed_trades['pnl_points'] < 0]['pnl_points'].mean() if losing_trades > 0 else 0
    
    profit_factor = abs(closed_trades[closed_trades['pnl_points'] > 0]['pnl_points'].sum() / 
                       closed_trades[closed_trades['pnl_points'] < 0]['pnl_points'].sum()) if losing_trades > 0 else float('inf')
    
    # Print statistics
    print(f"\nTotal Trades: {total_trades}")
    print(f"  Winning: {winning_trades} ({win_rate:.1f}%)")
    print(f"  Losing: {losing_trades}")
    print(f"  Breakeven: {breakeven_trades}")
    print(f"\nP&L:")
    print(f"  Total: {total_pnl:+.2f} points")
    print(f"  Average per trade: {avg_pnl:+.2f} points")
    print(f"  Average winner: {avg_winner:+.2f} points")
    print(f"  Average loser: {avg_loser:+.2f} points")
    print(f"\nProfit Factor: {profit_factor:.2f}")
    
    # Exit reason breakdown
    print(f"\nExit Reasons:")
    exit_reasons = closed_trades['exit_reason'].value_counts()
    for reason, count in exit_reasons.items():
        print(f"  {reason}: {count} ({count/total_trades*100:.1f}%)")
    
    # Direction breakdown
    if 'direction' in closed_trades.columns:
        print(f"\nDirection:")
        direction_stats = closed_trades.groupby('direction').agg({
            'pnl_points': ['count', 'sum', 'mean']
        }).round(2)
        print(direction_stats)


def print_comparative_summary(all_results: Dict[str, pd.DataFrame]):
    """
    Print comparative summary of all scenarios.
    
    Args:
        all_results: Dictionary mapping scenario names to trade DataFrames
    """
    print("\n" + "=" * 80)
    print("COMPARATIVE SUMMARY - ALL SCENARIOS")
    print("=" * 80)
    
    summary_data = []
    
    for scenario_name, trades_df in all_results.items():
        closed_trades = trades_df[trades_df['status'] == 'Closed']
        
        if len(closed_trades) == 0:
            continue
        
        total_trades = len(closed_trades)
        winning_trades = len(closed_trades[closed_trades['pnl_points'] > 0])
        win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
        total_pnl = closed_trades['pnl_points'].sum()
        avg_pnl = closed_trades['pnl_points'].mean()
        
        profit_factor = abs(closed_trades[closed_trades['pnl_points'] > 0]['pnl_points'].sum() / 
                           closed_trades[closed_trades['pnl_points'] < 0]['pnl_points'].sum()) if len(closed_trades[closed_trades['pnl_points'] < 0]) > 0 else float('inf')
        
        summary_data.append({
            'Scenario': scenario_name,
            'Total Trades': total_trades,
            'Win Rate': f"{win_rate:.1f}%",
            'Total P&L': f"{total_pnl:+.2f}",
            'Avg P&L': f"{avg_pnl:+.2f}",
            'Profit Factor': f"{profit_factor:.2f}"
        })
    
    summary_df = pd.DataFrame(summary_data)
    print("\n" + summary_df.to_string(index=False))
    
    # Best scenario
    if len(summary_data) > 0:
        best_scenario = max(summary_data, key=lambda x: float(x['Total P&L'].replace('+', '')))
        print(f"\n🏆 Best Scenario: {best_scenario['Scenario']}")
        print(f"   Total P&L: {best_scenario['Total P&L']} points")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main execution function."""
    print("\n" + "=" * 80)
    print("LONDON KILLZONE FVG ANALYSIS - LITERAL TIMES")
    print("=" * 80)
    print("\nAnalyzing Fair Value Gaps during LITERAL hours 01:00-03:55")
    print("(NO timezone conversion - using exact times from CSV)")
    print("\n")
    
    # Get base path
    base_path = '/home/runner/work/Backtest-Trading/Backtest-Trading'
    
    # Load data
    full_df = load_all_data(base_path)
    
    # Filter killzone data
    killzone_df = filter_killzone_data(full_df)
    
    # Detect FVGs
    killzone_df = detect_fvgs(killzone_df)
    
    # Find setups for each scenario
    scenario1_setups = find_scenario1_setups(killzone_df)
    scenario2_setups = find_scenario2_setups(killzone_df)
    
    # Get FVG indices used in scenarios 1 and 2
    scenario1_fvgs = {setup['fvg_idx'] for setup in scenario1_setups}
    scenario2_fvgs = {setup['fvg_idx'] for setup in scenario2_setups}
    
    scenario3_setups = find_scenario3_setups(killzone_df, scenario1_fvgs, scenario2_fvgs)
    
    # Backtest each scenario
    print("\n" + "=" * 80)
    print("BACKTESTING SCENARIOS")
    print("=" * 80)
    
    results = {}
    
    if scenario1_setups:
        print("\nBacktesting Scenario 1...")
        results['Scenario 1: Liquidity Sweep'] = backtest_scenario(full_df, scenario1_setups)
    
    if scenario2_setups:
        print("Backtesting Scenario 2...")
        results['Scenario 2: Inverted FVG'] = backtest_scenario(full_df, scenario2_setups)
    
    if scenario3_setups:
        print("Backtesting Scenario 3...")
        results['Scenario 3: Continuation'] = backtest_scenario(full_df, scenario3_setups)
    
    # Analyze results
    for scenario_name, trades_df in results.items():
        analyze_results(trades_df, scenario_name)
    
    # Print comparative summary
    print_comparative_summary(results)
    
    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()

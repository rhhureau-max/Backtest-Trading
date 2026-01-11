#!/usr/bin/env python3
"""
FVG (Fair Value Gap) Analysis Script

Analyzes FVG patterns from 2018 to 2025 on 1m, 5m, and 15m timeframes.
Looks for the pattern: FVG → normal candle (no FVG) → FVG (same direction)
Both FVGs must be of the same direction (bullish-bullish or bearish-bearish)
During session hours: 8:30 to 12:00 (as recorded in the CSV data files)

Includes backtesting with multiple SL and TP levels at various RR ratios.
"""

import os
import zipfile
import pandas as pd
from datetime import time
from collections import defaultdict

DATA_DIR = os.path.dirname(os.path.abspath(__file__))

# Session hours as recorded in the CSV data files (8:30 to 12:00)
SESSION_START = time(8, 30)
SESSION_END = time(12, 0)

# Early session hours (8:30 to 9:00)
EARLY_SESSION_START = time(8, 30)
EARLY_SESSION_END = time(9, 0)

# Minimum candles required for FVG pattern analysis:
# - Need 3 candles to determine if middle candle has FVG (candle n-1, n, n+1)
# - For the FVG-Normal-FVG pattern, we need 3 consecutive positions (i, i+1, i+2)
# - Each position needs its neighbors, so we need positions 0 to 4 at minimum (5 candles)
MIN_CANDLES_FOR_ANALYSIS = 5

def load_csv_data(filepath):
    """Load CSV data from file, handling zip files if needed."""
    if filepath.endswith('.zip'):
        with zipfile.ZipFile(filepath, 'r') as z:
            # Get the first CSV file in the archive
            csv_files = [f for f in z.namelist() if f.endswith('.csv')]
            if not csv_files:
                return None
            with z.open(csv_files[0]) as f:
                df = pd.read_csv(f, sep=';', header=0)
    else:
        df = pd.read_csv(filepath, sep=';', header=0)
    
    # Rename columns for clarity
    df.columns = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
    
    # Parse datetime
    df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%d/%m/%Y %H:%M:%S')
    df['TimeOnly'] = df['DateTime'].dt.time
    
    return df


def filter_session_hours(df, start_time=SESSION_START, end_time=SESSION_END):
    """Filter data to only include rows within session hours."""
    mask = (df['TimeOnly'] >= start_time) & (df['TimeOnly'] <= end_time)
    return df[mask].copy()


def is_bullish_fvg(candle_prev, candle_current, candle_next):
    """
    Check if the current candle forms a bullish FVG.
    Bullish FVG: Gap between the high of candle n-1 and the low of candle n+1
    (low of n+1 > high of n-1)
    """
    return candle_next['Low'] > candle_prev['High']


def is_bearish_fvg(candle_prev, candle_current, candle_next):
    """
    Check if the current candle forms a bearish FVG.
    Bearish FVG: Gap between the low of candle n-1 and the high of candle n+1
    (high of n+1 < low of n-1)
    """
    return candle_next['High'] < candle_prev['Low']


def analyze_fvg_patterns(df):
    """
    Analyze FVG patterns in the dataframe.
    Looking for: FVG → normal candle (no FVG) → FVG
    
    Returns:
        dict with counts of patterns found
    """
    if len(df) < MIN_CANDLES_FOR_ANALYSIS:
        return {
            'total_candles': len(df),
            'total_sessions': 0,
            'fvg_count': 0,
            'fvg_normal_fvg_count': 0,
            'bullish_fvg_count': 0,
            'bearish_fvg_count': 0,
            'bullish_pattern_count': 0,
            'bearish_pattern_count': 0
        }
    
    df = df.reset_index(drop=True)
    
    # Calculate FVG for each candle (we need candle n-1, n, and n+1 to determine if n has FVG)
    fvg_markers = []
    bullish_count = 0
    bearish_count = 0
    
    for i in range(1, len(df) - 1):
        candle_prev = df.iloc[i - 1]
        candle_current = df.iloc[i]
        candle_next = df.iloc[i + 1]
        
        is_bullish = is_bullish_fvg(candle_prev, candle_current, candle_next)
        is_bearish = is_bearish_fvg(candle_prev, candle_current, candle_next)
        
        if is_bullish:
            bullish_count += 1
            fvg_markers.append((i, 'bullish'))
        elif is_bearish:
            bearish_count += 1
            fvg_markers.append((i, 'bearish'))
        else:
            fvg_markers.append((i, None))
    
    # Now look for the pattern: FVG → normal → FVG (same direction)
    # We need to check consecutive groups of 3 candles
    fvg_normal_fvg_count = 0
    bullish_pattern_count = 0
    bearish_pattern_count = 0
    
    # Create a simple list of whether each position has FVG and its direction
    fvg_status = {item[0]: item[1] for item in fvg_markers}
    
    # Loop through positions that can be evaluated for FVG (indices 1 to len-2)
    # and check pattern at positions i, i+1, i+2 where each must be in fvg_status
    for i in range(1, len(df) - 2):  # Position i+2 must be <= len(df) - 2
        # Position i is our first potential FVG
        # Position i+1 should be normal (no FVG)
        # Position i+2 should be another FVG of the same direction
        
        pos1 = i
        pos2 = i + 1
        pos3 = i + 2
        
        # Check if all positions have been evaluated for FVG
        if pos1 in fvg_status and pos2 in fvg_status and pos3 in fvg_status:
            fvg_type_1 = fvg_status[pos1]
            fvg_type_2 = fvg_status[pos2]
            fvg_type_3 = fvg_status[pos3]
            
            # Pattern: FVG (bullish/bearish) → normal (None) → FVG (same direction)
            if fvg_type_1 is not None and fvg_type_2 is None and fvg_type_3 is not None:
                # Both FVGs must be of the same direction
                if fvg_type_1 == fvg_type_3:
                    fvg_normal_fvg_count += 1
                    if fvg_type_1 == 'bullish':
                        bullish_pattern_count += 1
                    else:
                        bearish_pattern_count += 1
    
    # Count unique trading sessions (days)
    unique_dates = df['Date'].nunique()
    
    return {
        'total_candles': len(df),
        'total_sessions': unique_dates,
        'fvg_count': bullish_count + bearish_count,
        'bullish_fvg_count': bullish_count,
        'bearish_fvg_count': bearish_count,
        'fvg_normal_fvg_count': fvg_normal_fvg_count,
        'bullish_pattern_count': bullish_pattern_count,
        'bearish_pattern_count': bearish_pattern_count
    }


# Risk-Reward ratios to test
RR_LEVELS = [1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]

# SL types
SL_TYPES = ['50%', '100%', 'gap']


def find_fvg_patterns_with_details(df):
    """
    Find all FVG-Normal-FVG patterns and return detailed information
    needed for backtesting.
    
    Returns:
        list of pattern details: [
            {
                'pattern_type': 'bullish' or 'bearish',
                'fvg1_idx': index of first FVG candle,
                'neutral_idx': index of neutral candle,
                'fvg2_idx': index of second FVG candle,
                'entry_candle_idx': index of entry candle (n+1 of second FVG),
                'fvg2_prev': candle n-1 of second FVG,
                'fvg2_current': candle n of second FVG (the FVG candle),
                'fvg2_next': candle n+1 of second FVG (entry reference),
            }
        ]
    """
    if len(df) < MIN_CANDLES_FOR_ANALYSIS:
        return []
    
    df = df.reset_index(drop=True)
    
    # Calculate FVG for each candle
    fvg_markers = {}
    
    for i in range(1, len(df) - 1):
        candle_prev = df.iloc[i - 1]
        candle_current = df.iloc[i]
        candle_next = df.iloc[i + 1]
        
        if is_bullish_fvg(candle_prev, candle_current, candle_next):
            fvg_markers[i] = 'bullish'
        elif is_bearish_fvg(candle_prev, candle_current, candle_next):
            fvg_markers[i] = 'bearish'
        else:
            fvg_markers[i] = None
    
    # Find FVG-Normal-FVG patterns
    patterns = []
    
    for i in range(1, len(df) - 4):  # Need at least 2 more candles after pattern for entry
        pos1 = i
        pos2 = i + 1
        pos3 = i + 2
        
        if pos1 in fvg_markers and pos2 in fvg_markers and pos3 in fvg_markers:
            fvg_type_1 = fvg_markers[pos1]
            fvg_type_2 = fvg_markers[pos2]
            fvg_type_3 = fvg_markers[pos3]
            
            # Pattern: FVG → normal → FVG (same direction)
            if fvg_type_1 is not None and fvg_type_2 is None and fvg_type_3 is not None:
                if fvg_type_1 == fvg_type_3:
                    # Entry candle is n+1 of the second FVG (pos3 + 1)
                    entry_idx = pos3 + 1
                    
                    if entry_idx < len(df):
                        patterns.append({
                            'pattern_type': fvg_type_1,
                            'fvg1_idx': pos1,
                            'neutral_idx': pos2,
                            'fvg2_idx': pos3,
                            'entry_candle_idx': entry_idx,
                            'fvg2_prev': df.iloc[pos3 - 1],
                            'fvg2_current': df.iloc[pos3],
                            'fvg2_next': df.iloc[pos3 + 1],
                        })
    
    return patterns


def calculate_sl_levels(pattern, sl_type):
    """
    Calculate stop loss level based on the pattern and SL type.
    
    For LONG (bullish pattern):
        - 50%: SL at 50% of n+1 candle range below entry
        - 100%: SL at bottom of n+1 candle (Low)
        - gap: SL below the FVG gap (low of candle n-1 of second FVG)
    
    For SHORT (bearish pattern):
        - 50%: SL at 50% of n+1 candle range above entry
        - 100%: SL at top of n+1 candle (High)
        - gap: SL above the FVG gap (high of candle n-1 of second FVG)
    
    Returns:
        (entry_price, sl_price, sl_distance)
    """
    entry_candle = pattern['fvg2_next']  # n+1 of second FVG
    fvg2_prev = pattern['fvg2_prev']     # n-1 of second FVG
    
    if pattern['pattern_type'] == 'bullish':
        # LONG trade - entry at close of entry candle
        entry_price = entry_candle['Close']
        candle_range = entry_candle['High'] - entry_candle['Low']
        
        if sl_type == '50%':
            # SL at 50% of entry candle range below entry candle low
            sl_price = entry_candle['Low'] - (candle_range * 0.5)
        elif sl_type == '100%':
            # SL at entry candle low
            sl_price = entry_candle['Low']
        else:  # gap
            # SL below the FVG gap - use high of n-1 (bottom of gap for bullish)
            sl_price = fvg2_prev['High']
        
        sl_distance = entry_price - sl_price
        
    else:  # bearish
        # SHORT trade - entry at close of entry candle
        entry_price = entry_candle['Close']
        candle_range = entry_candle['High'] - entry_candle['Low']
        
        if sl_type == '50%':
            # SL at 50% of entry candle range above entry candle high
            sl_price = entry_candle['High'] + (candle_range * 0.5)
        elif sl_type == '100%':
            # SL at entry candle high
            sl_price = entry_candle['High']
        else:  # gap
            # SL above the FVG gap - use low of n-1 (top of gap for bearish)
            sl_price = fvg2_prev['Low']
        
        sl_distance = sl_price - entry_price
    
    return entry_price, sl_price, sl_distance


def simulate_trade(df, pattern, entry_idx, entry_price, sl_price, tp_price, is_long, max_candles=100):
    """
    Simulate a trade starting from entry_idx.
    
    Returns:
        'win' if TP hit first
        'loss' if SL hit first
        'timeout' if neither hit within max_candles
    """
    for i in range(entry_idx + 1, min(entry_idx + max_candles + 1, len(df))):
        candle = df.iloc[i]
        
        if is_long:
            # Check if SL hit (price went below sl_price)
            if candle['Low'] <= sl_price:
                # Check if TP was also hit in same candle
                if candle['High'] >= tp_price:
                    # Assume SL hit first if open is closer to SL
                    if abs(candle['Open'] - sl_price) < abs(candle['Open'] - tp_price):
                        return 'loss'
                    else:
                        return 'win'
                return 'loss'
            # Check if TP hit
            if candle['High'] >= tp_price:
                return 'win'
        else:  # short
            # Check if SL hit (price went above sl_price)
            if candle['High'] >= sl_price:
                # Check if TP was also hit in same candle
                if candle['Low'] <= tp_price:
                    # Assume SL hit first if open is closer to SL
                    if abs(candle['Open'] - sl_price) < abs(candle['Open'] - tp_price):
                        return 'loss'
                    else:
                        return 'win'
                return 'loss'
            # Check if TP hit
            if candle['Low'] <= tp_price:
                return 'win'
    
    return 'timeout'


def backtest_patterns(df, patterns):
    """
    Backtest all patterns with different SL types and RR levels.
    
    Returns:
        dict with backtest results organized by pattern type, SL type, and RR level
    """
    results = {
        'bullish': {sl: {rr: {'wins': 0, 'losses': 0, 'timeouts': 0} for rr in RR_LEVELS} for sl in SL_TYPES},
        'bearish': {sl: {rr: {'wins': 0, 'losses': 0, 'timeouts': 0} for rr in RR_LEVELS} for sl in SL_TYPES}
    }
    
    for pattern in patterns:
        pattern_type = pattern['pattern_type']
        entry_idx = pattern['entry_candle_idx']
        is_long = (pattern_type == 'bullish')
        
        for sl_type in SL_TYPES:
            entry_price, sl_price, sl_distance = calculate_sl_levels(pattern, sl_type)
            
            # Skip if SL distance is 0 or negative
            if sl_distance <= 0:
                continue
            
            for rr in RR_LEVELS:
                # Calculate TP based on RR
                if is_long:
                    tp_price = entry_price + (sl_distance * rr)
                else:
                    tp_price = entry_price - (sl_distance * rr)
                
                # Simulate trade
                result = simulate_trade(df, pattern, entry_idx, entry_price, sl_price, tp_price, is_long)
                
                if result == 'win':
                    results[pattern_type][sl_type][rr]['wins'] += 1
                elif result == 'loss':
                    results[pattern_type][sl_type][rr]['losses'] += 1
                else:
                    results[pattern_type][sl_type][rr]['timeouts'] += 1
    
    return results


def aggregate_backtest_results(all_results):
    """Aggregate backtest results from multiple data files."""
    aggregated = {
        'bullish': {sl: {rr: {'wins': 0, 'losses': 0, 'timeouts': 0} for rr in RR_LEVELS} for sl in SL_TYPES},
        'bearish': {sl: {rr: {'wins': 0, 'losses': 0, 'timeouts': 0} for rr in RR_LEVELS} for sl in SL_TYPES}
    }
    
    for result in all_results:
        for pattern_type in ['bullish', 'bearish']:
            for sl_type in SL_TYPES:
                for rr in RR_LEVELS:
                    aggregated[pattern_type][sl_type][rr]['wins'] += result[pattern_type][sl_type][rr]['wins']
                    aggregated[pattern_type][sl_type][rr]['losses'] += result[pattern_type][sl_type][rr]['losses']
                    aggregated[pattern_type][sl_type][rr]['timeouts'] += result[pattern_type][sl_type][rr]['timeouts']
    
    return aggregated


def print_backtest_results(results, session_name):
    """Print formatted backtest results."""
    print(f"\n{'='*100}")
    print(f"BACKTEST RESULTS - {session_name}")
    print(f"{'='*100}")
    
    for pattern_type in ['bullish', 'bearish']:
        trade_type = "LONG" if pattern_type == 'bullish' else "SHORT"
        print(f"\n{'-'*100}")
        print(f"{trade_type} TRADES ({pattern_type.upper()} patterns)")
        print(f"{'-'*100}")
        
        # Header
        header = f"{'SL Type':<12}"
        for rr in RR_LEVELS:
            header += f"{'RR '+str(rr):>10}"
        print(header)
        print("-" * (12 + 10 * len(RR_LEVELS)))
        
        for sl_type in SL_TYPES:
            # Win rates row
            row = f"SL {sl_type:<8}"
            for rr in RR_LEVELS:
                data = results[pattern_type][sl_type][rr]
                total = data['wins'] + data['losses']
                if total > 0:
                    win_rate = (data['wins'] / total) * 100
                    row += f"{win_rate:>9.1f}%"
                else:
                    row += f"{'N/A':>10}"
            print(row)
        
        # Print totals for reference
        print(f"\nTrade counts (wins/losses/timeouts):")
        for sl_type in SL_TYPES:
            row = f"SL {sl_type:<8}"
            for rr in RR_LEVELS:
                data = results[pattern_type][sl_type][rr]
                row += f" {data['wins']}/{data['losses']}/{data['timeouts']}"
            print(row)


def run_backtest_for_timeframe(timeframe, session_start, session_end, session_name):
    """Run backtest for a specific timeframe and session."""
    print(f"\n{'='*60}")
    print(f"Backtesting {timeframe} timeframe - {session_name}")
    print(f"{'='*60}")
    
    files = get_data_files(timeframe)
    all_backtest_results = []
    
    for year, filepath in files:
        print(f"Processing {year}...")
        try:
            df = load_csv_data(filepath)
            if df is None or len(df) == 0:
                continue
            
            # Filter to session hours
            df_filtered = filter_session_hours(df, session_start, session_end)
            
            if len(df_filtered) >= MIN_CANDLES_FOR_ANALYSIS:
                # Find patterns
                patterns = find_fvg_patterns_with_details(df_filtered)
                
                if patterns:
                    # Backtest patterns
                    bt_results = backtest_patterns(df_filtered, patterns)
                    all_backtest_results.append(bt_results)
                    
                    bull_patterns = sum(1 for p in patterns if p['pattern_type'] == 'bullish')
                    bear_patterns = sum(1 for p in patterns if p['pattern_type'] == 'bearish')
                    print(f"  Found {len(patterns)} patterns (Bull: {bull_patterns}, Bear: {bear_patterns})")
                    
        except Exception as e:
            print(f"  Error: {e}")
    
    if all_backtest_results:
        return aggregate_backtest_results(all_backtest_results)
    
    return None


def get_data_files(timeframe):
    """Get all data files for a specific timeframe."""
    files = []
    years = range(2018, 2026)
    
    for year in years:
        if timeframe == '1m':
            # 1m files are mostly zipped except 2025
            if year == 2025:
                filepath = os.path.join(DATA_DIR, f"{year} 1m.csv")
            else:
                filepath = os.path.join(DATA_DIR, f"{year} 1m.csv.zip")
        else:
            filepath = os.path.join(DATA_DIR, f"{year} {timeframe}.csv")
        
        if os.path.exists(filepath):
            files.append((year, filepath))
    
    return files


def analyze_timeframe(timeframe, include_early_session=True):
    """Analyze all data for a specific timeframe."""
    print(f"\n{'='*60}")
    print(f"Analyzing {timeframe} timeframe")
    print(f"{'='*60}")
    
    files = get_data_files(timeframe)
    
    total_results = {
        'total_candles': 0,
        'total_sessions': 0,
        'fvg_count': 0,
        'bullish_fvg_count': 0,
        'bearish_fvg_count': 0,
        'fvg_normal_fvg_count': 0,
        'bullish_pattern_count': 0,
        'bearish_pattern_count': 0
    }
    
    # Results for early session (8:30-9:00)
    early_results = {
        'total_candles': 0,
        'total_sessions': 0,
        'fvg_count': 0,
        'bullish_fvg_count': 0,
        'bearish_fvg_count': 0,
        'fvg_normal_fvg_count': 0,
        'bullish_pattern_count': 0,
        'bearish_pattern_count': 0
    }
    
    yearly_results = []
    early_yearly_results = []
    
    for year, filepath in files:
        print(f"\nProcessing {year}...")
        try:
            df = load_csv_data(filepath)
            if df is None or len(df) == 0:
                print(f"  No data found in {filepath}")
                continue
            
            # Filter to full session hours (8:30-12:00)
            df_filtered = filter_session_hours(df)
            print(f"  Total candles: {len(df)}, Session candles (8:30-12:00): {len(df_filtered)}")
            
            if len(df_filtered) >= MIN_CANDLES_FOR_ANALYSIS:
                # Analyze patterns for full session
                results = analyze_fvg_patterns(df_filtered)
                
                print(f"  [8:30-12:00] FVGs: {results['fvg_count']} (Bull: {results['bullish_fvg_count']}, Bear: {results['bearish_fvg_count']})")
                print(f"  [8:30-12:00] Patterns: {results['fvg_normal_fvg_count']} (Bull: {results['bullish_pattern_count']}, Bear: {results['bearish_pattern_count']})")
                
                yearly_results.append({
                    'year': year,
                    **results
                })
                
                # Add to totals
                for key in total_results:
                    total_results[key] += results[key]
            
            # Filter to early session hours (8:30-9:00)
            if include_early_session:
                df_early = filter_session_hours(df, EARLY_SESSION_START, EARLY_SESSION_END)
                print(f"  Early session candles (8:30-9:00): {len(df_early)}")
                
                if len(df_early) >= MIN_CANDLES_FOR_ANALYSIS:
                    early_res = analyze_fvg_patterns(df_early)
                    
                    print(f"  [8:30-9:00] FVGs: {early_res['fvg_count']} (Bull: {early_res['bullish_fvg_count']}, Bear: {early_res['bearish_fvg_count']})")
                    print(f"  [8:30-9:00] Patterns: {early_res['fvg_normal_fvg_count']} (Bull: {early_res['bullish_pattern_count']}, Bear: {early_res['bearish_pattern_count']})")
                    
                    early_yearly_results.append({
                        'year': year,
                        **early_res
                    })
                    
                    for key in early_results:
                        early_results[key] += early_res[key]
                
        except Exception as e:
            print(f"  Error processing {filepath}: {e}")
    
    return total_results, yearly_results, early_results, early_yearly_results


def main():
    print("="*60)
    print("FVG (Fair Value Gap) Analysis")
    print("="*60)
    print(f"\nFull session: {SESSION_START} to {SESSION_END}")
    print(f"Early session: {EARLY_SESSION_START} to {EARLY_SESSION_END}")
    print("\nPattern: FVG → Normal candle (no FVG) → FVG (same direction)")
    print("Both FVGs must be of the same direction (bullish-bullish or bearish-bearish)")
    
    timeframes = ['1m', '5m', '15m']
    all_results = {}
    
    for tf in timeframes:
        total_results, yearly_results, early_results, early_yearly_results = analyze_timeframe(tf)
        all_results[tf] = {
            'total': total_results,
            'yearly': yearly_results,
            'early_total': early_results,
            'early_yearly': early_yearly_results
        }
    
    # Print summary for full session (8:30-12:00)
    print("\n" + "="*60)
    print("SUMMARY RESULTS - FULL SESSION (8:30-12:00)")
    print("="*60)
    
    for tf in timeframes:
        results = all_results[tf]['total']
        print(f"\n{tf} Timeframe:")
        print(f"  Total candles analyzed: {results['total_candles']:,}")
        print(f"  Total trading sessions (days): {results['total_sessions']:,}")
        print(f"  Total FVGs found: {results['fvg_count']:,}")
        print(f"    - Bullish FVGs: {results['bullish_fvg_count']:,}")
        print(f"    - Bearish FVGs: {results['bearish_fvg_count']:,}")
        print(f"  FVG-Normal-FVG patterns (same direction): {results['fvg_normal_fvg_count']:,}")
        print(f"    - Bullish patterns: {results['bullish_pattern_count']:,}")
        print(f"    - Bearish patterns: {results['bearish_pattern_count']:,}")
        
        if results['total_candles'] > 0:
            fvg_ratio = results['fvg_count'] / results['total_candles'] * 100
            pattern_ratio = results['fvg_normal_fvg_count'] / results['total_candles'] * 100
            print(f"  FVG occurrence rate: {fvg_ratio:.2f}%")
            print(f"  FVG-Normal-FVG pattern rate: {pattern_ratio:.4f}%")
        
        if results['fvg_count'] > 0:
            pattern_to_fvg = results['fvg_normal_fvg_count'] / results['fvg_count'] * 100
            print(f"  Pattern-to-FVG ratio: {pattern_to_fvg:.2f}%")
    
    # Print summary for early session (8:30-9:00)
    print("\n" + "="*60)
    print("SUMMARY RESULTS - EARLY SESSION (8:30-9:00)")
    print("="*60)
    
    for tf in timeframes:
        results = all_results[tf]['early_total']
        print(f"\n{tf} Timeframe:")
        print(f"  Total candles analyzed: {results['total_candles']:,}")
        print(f"  Total trading sessions (days): {results['total_sessions']:,}")
        print(f"  Total FVGs found: {results['fvg_count']:,}")
        print(f"    - Bullish FVGs: {results['bullish_fvg_count']:,}")
        print(f"    - Bearish FVGs: {results['bearish_fvg_count']:,}")
        print(f"  FVG-Normal-FVG patterns (same direction): {results['fvg_normal_fvg_count']:,}")
        print(f"    - Bullish patterns: {results['bullish_pattern_count']:,}")
        print(f"    - Bearish patterns: {results['bearish_pattern_count']:,}")
        
        if results['total_candles'] > 0:
            fvg_ratio = results['fvg_count'] / results['total_candles'] * 100
            pattern_ratio = results['fvg_normal_fvg_count'] / results['total_candles'] * 100
            print(f"  FVG occurrence rate: {fvg_ratio:.2f}%")
            print(f"  FVG-Normal-FVG pattern rate: {pattern_ratio:.4f}%")
        
        if results['fvg_count'] > 0:
            pattern_to_fvg = results['fvg_normal_fvg_count'] / results['fvg_count'] * 100
            print(f"  Pattern-to-FVG ratio: {pattern_to_fvg:.2f}%")
    
    # Yearly breakdown table for full session
    print("\n" + "="*60)
    print("YEARLY BREAKDOWN - FULL SESSION (8:30-12:00)")
    print("="*60)
    
    for tf in timeframes:
        print(f"\n{tf} Timeframe - Yearly Details:")
        print(f"{'Year':<6} {'Candles':>10} {'Sessions':>10} {'FVGs':>8} {'Bull FVG':>9} {'Bear FVG':>9} {'Patterns':>9} {'Bull Pat':>9} {'Bear Pat':>9}")
        print("-" * 90)
        
        for yr in all_results[tf]['yearly']:
            print(f"{yr['year']:<6} {yr['total_candles']:>10,} {yr['total_sessions']:>10,} {yr['fvg_count']:>8,} {yr['bullish_fvg_count']:>9,} {yr['bearish_fvg_count']:>9,} {yr['fvg_normal_fvg_count']:>9,} {yr['bullish_pattern_count']:>9,} {yr['bearish_pattern_count']:>9,}")
    
    # Yearly breakdown table for early session
    print("\n" + "="*60)
    print("YEARLY BREAKDOWN - EARLY SESSION (8:30-9:00)")
    print("="*60)
    
    for tf in timeframes:
        print(f"\n{tf} Timeframe - Yearly Details:")
        print(f"{'Year':<6} {'Candles':>10} {'Sessions':>10} {'FVGs':>8} {'Bull FVG':>9} {'Bear FVG':>9} {'Patterns':>9} {'Bull Pat':>9} {'Bear Pat':>9}")
        print("-" * 90)
        
        for yr in all_results[tf]['early_yearly']:
            print(f"{yr['year']:<6} {yr['total_candles']:>10,} {yr['total_sessions']:>10,} {yr['fvg_count']:>8,} {yr['bullish_fvg_count']:>9,} {yr['bearish_fvg_count']:>9,} {yr['fvg_normal_fvg_count']:>9,} {yr['bullish_pattern_count']:>9,} {yr['bearish_pattern_count']:>9,}")
    
    # Run backtesting
    print("\n" + "="*100)
    print("BACKTESTING ANALYSIS")
    print("="*100)
    print("\nSL Types:")
    print("  - 50%: Stop loss at 50% of entry candle (n+1) range beyond its extreme")
    print("  - 100%: Stop loss at the extreme of entry candle (n+1)")
    print("  - gap: Stop loss beyond the FVG gap of the second FVG")
    print("\nRR Levels: 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5")
    print("\nWin Rate = Wins / (Wins + Losses) * 100")
    
    backtest_results = {}
    
    for tf in timeframes:
        # Backtest full session
        full_bt = run_backtest_for_timeframe(tf, SESSION_START, SESSION_END, f"Full Session (8:30-12:00)")
        if full_bt:
            backtest_results[f"{tf}_full"] = full_bt
        
        # Backtest early session
        early_bt = run_backtest_for_timeframe(tf, EARLY_SESSION_START, EARLY_SESSION_END, f"Early Session (8:30-9:00)")
        if early_bt:
            backtest_results[f"{tf}_early"] = early_bt
    
    # Print all backtest results
    for tf in timeframes:
        if f"{tf}_full" in backtest_results:
            print(f"\n\n{'#'*100}")
            print(f"# {tf.upper()} TIMEFRAME - FULL SESSION (8:30-12:00)")
            print(f"{'#'*100}")
            print_backtest_results(backtest_results[f"{tf}_full"], f"{tf} Full Session (8:30-12:00)")
        
        if f"{tf}_early" in backtest_results:
            print(f"\n\n{'#'*100}")
            print(f"# {tf.upper()} TIMEFRAME - EARLY SESSION (8:30-9:00)")
            print(f"{'#'*100}")
            print_backtest_results(backtest_results[f"{tf}_early"], f"{tf} Early Session (8:30-9:00)")


if __name__ == "__main__":
    main()

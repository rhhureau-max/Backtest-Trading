#!/usr/bin/env python3
"""
FVG (Fair Value Gap) Analysis Script

Analyzes FVG patterns from 2018 to 2025 on 1m, 5m, and 15m timeframes.
Looks for the pattern: FVG → normal candle (no FVG) → FVG (same direction)
Both FVGs must be of the same direction (bullish-bullish or bearish-bearish)
During session hours: 8:30 to 12:00 (as recorded in the CSV data files)
"""

import os
import zipfile
import pandas as pd
from datetime import time

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


if __name__ == "__main__":
    main()

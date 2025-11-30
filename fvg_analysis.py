#!/usr/bin/env python3
"""
FVG (Fair Value Gap) Analysis Script

Analyzes FVG patterns from 2018 to 2025 on 1m, 5m, and 15m timeframes.
Looks for the pattern: FVG → normal candle (no FVG) → FVG
During session hours: 15:30 to 19:00 (data timezone, corresponds to 8:30-12:00 NY time)
"""

import os
import zipfile
import pandas as pd
from datetime import time

DATA_DIR = "/home/runner/work/Backtest-Trading/Backtest-Trading"

# Session hours in data timezone (15:30 to 19:00 corresponds to 8:30-12:00 NY time)
SESSION_START = time(15, 30)
SESSION_END = time(19, 0)

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


def has_fvg(candle_prev, candle_current, candle_next):
    """Check if the current candle forms any FVG (bullish or bearish)."""
    return is_bullish_fvg(candle_prev, candle_current, candle_next) or \
           is_bearish_fvg(candle_prev, candle_current, candle_next)


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
            'bearish_fvg_count': 0
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
    
    # Now look for the pattern: FVG → normal → FVG
    # We need to check consecutive groups of 3 candles
    fvg_normal_fvg_count = 0
    
    # Create a simple list of whether each position has FVG
    fvg_status = {item[0]: item[1] for item in fvg_markers}
    
    # Loop through positions that can be evaluated for FVG (indices 1 to len-2)
    # and check pattern at positions i, i+1, i+2 where each must be in fvg_status
    for i in range(1, len(df) - 3):  # Position i+2 must be < len(df) - 1
        # Position i is our first potential FVG
        # Position i+1 should be normal (no FVG)
        # Position i+2 should be another FVG
        
        pos1 = i
        pos2 = i + 1
        pos3 = i + 2
        
        # Check if all positions have been evaluated for FVG
        if pos1 in fvg_status and pos2 in fvg_status and pos3 in fvg_status:
            has_fvg_1 = fvg_status[pos1] is not None
            has_fvg_2 = fvg_status[pos2] is not None
            has_fvg_3 = fvg_status[pos3] is not None
            
            if has_fvg_1 and not has_fvg_2 and has_fvg_3:
                fvg_normal_fvg_count += 1
    
    # Count unique trading sessions (days)
    unique_dates = df['Date'].nunique()
    
    return {
        'total_candles': len(df),
        'total_sessions': unique_dates,
        'fvg_count': bullish_count + bearish_count,
        'bullish_fvg_count': bullish_count,
        'bearish_fvg_count': bearish_count,
        'fvg_normal_fvg_count': fvg_normal_fvg_count
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


def analyze_timeframe(timeframe):
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
        'fvg_normal_fvg_count': 0
    }
    
    yearly_results = []
    
    for year, filepath in files:
        print(f"\nProcessing {year}...")
        try:
            df = load_csv_data(filepath)
            if df is None or len(df) == 0:
                print(f"  No data found in {filepath}")
                continue
            
            # Filter to session hours
            df_filtered = filter_session_hours(df)
            print(f"  Total candles: {len(df)}, Session candles: {len(df_filtered)}")
            
            if len(df_filtered) < MIN_CANDLES_FOR_ANALYSIS:
                print(f"  Not enough data after filtering")
                continue
            
            # Analyze patterns
            results = analyze_fvg_patterns(df_filtered)
            
            print(f"  FVGs found: {results['fvg_count']} (Bullish: {results['bullish_fvg_count']}, Bearish: {results['bearish_fvg_count']})")
            print(f"  FVG-Normal-FVG patterns: {results['fvg_normal_fvg_count']}")
            
            yearly_results.append({
                'year': year,
                **results
            })
            
            # Add to totals
            for key in total_results:
                total_results[key] += results[key]
                
        except Exception as e:
            print(f"  Error processing {filepath}: {e}")
    
    return total_results, yearly_results


def main():
    print("="*60)
    print("FVG (Fair Value Gap) Analysis")
    print("="*60)
    print(f"\nSession hours: {SESSION_START} to {SESSION_END} (data timezone)")
    print("(Corresponds to 8:30 AM to 12:00 PM New York time)")
    print("\nPattern: FVG → Normal candle (no FVG) → FVG")
    
    timeframes = ['1m', '5m', '15m']
    all_results = {}
    
    for tf in timeframes:
        total_results, yearly_results = analyze_timeframe(tf)
        all_results[tf] = {
            'total': total_results,
            'yearly': yearly_results
        }
    
    # Print summary
    print("\n" + "="*60)
    print("SUMMARY RESULTS")
    print("="*60)
    
    for tf in timeframes:
        results = all_results[tf]['total']
        print(f"\n{tf} Timeframe:")
        print(f"  Total candles analyzed: {results['total_candles']:,}")
        print(f"  Total trading sessions (days): {results['total_sessions']:,}")
        print(f"  Total FVGs found: {results['fvg_count']:,}")
        print(f"    - Bullish FVGs: {results['bullish_fvg_count']:,}")
        print(f"    - Bearish FVGs: {results['bearish_fvg_count']:,}")
        print(f"  FVG-Normal-FVG patterns: {results['fvg_normal_fvg_count']:,}")
        
        if results['total_candles'] > 0:
            fvg_ratio = results['fvg_count'] / results['total_candles'] * 100
            pattern_ratio = results['fvg_normal_fvg_count'] / results['total_candles'] * 100
            print(f"  FVG occurrence rate: {fvg_ratio:.2f}%")
            print(f"  FVG-Normal-FVG pattern rate: {pattern_ratio:.4f}%")
        
        if results['fvg_count'] > 0:
            pattern_to_fvg = results['fvg_normal_fvg_count'] / results['fvg_count'] * 100
            print(f"  Pattern-to-FVG ratio: {pattern_to_fvg:.2f}%")
    
    # Yearly breakdown table
    print("\n" + "="*60)
    print("YEARLY BREAKDOWN")
    print("="*60)
    
    for tf in timeframes:
        print(f"\n{tf} Timeframe - Yearly Details:")
        print(f"{'Year':<6} {'Candles':>10} {'Sessions':>10} {'FVGs':>8} {'Bullish':>8} {'Bearish':>8} {'FVG-N-FVG':>10}")
        print("-" * 70)
        
        for yr in all_results[tf]['yearly']:
            print(f"{yr['year']:<6} {yr['total_candles']:>10,} {yr['total_sessions']:>10,} {yr['fvg_count']:>8,} {yr['bullish_fvg_count']:>8,} {yr['bearish_fvg_count']:>8,} {yr['fvg_normal_fvg_count']:>10,}")


if __name__ == "__main__":
    main()

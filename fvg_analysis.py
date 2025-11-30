#!/usr/bin/env python3
"""
FVG (Fair Value Gap) Consecutive Pattern Analysis at 8:30 AM Opening

This script analyzes win rates for two consecutive FVGs at the 8:30 AM opening:
- FVG on 8:30 candle: imbalance between n-1 (8:29) and n+1 (8:31) candles
- FVG on 8:31 candle: imbalance between n-1 (8:30) and n+1 (8:32) candles

The analysis is performed on 1m, 5m, and 15m timeframes.
"""

import pandas as pd
import os
from datetime import datetime, timedelta
from typing import Tuple, Optional, Dict, List


def load_csv_data(filepath: str) -> pd.DataFrame:
    """Load CSV data with proper column names."""
    df = pd.read_csv(filepath, sep=';', 
                     names=['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume'],
                     skiprows=1)
    df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%d/%m/%Y %H:%M:%S')
    return df


def check_fvg(candle_prev: pd.Series, candle_current: pd.Series, candle_next: pd.Series) -> Tuple[bool, str, float]:
    """
    Check if there's a Fair Value Gap (FVG) for the current candle.
    
    FVG occurs when there's an imbalance (gap) between:
    - The body/wick of candle n-1 and
    - The body/wick of candle n+1
    
    Bullish FVG: Low of n+1 > High of n-1 (gap up)
    Bearish FVG: High of n+1 < Low of n-1 (gap down)
    
    Returns: (has_fvg, direction, gap_size)
    """
    # Get the high of n-1 and low of n+1 for bullish FVG
    high_prev = candle_prev['High']
    low_next = candle_next['Low']
    
    # Get the low of n-1 and high of n+1 for bearish FVG
    low_prev = candle_prev['Low']
    high_next = candle_next['High']
    
    # Bullish FVG: gap up (n+1 low > n-1 high)
    if low_next > high_prev:
        gap_size = low_next - high_prev
        return True, 'bullish', gap_size
    
    # Bearish FVG: gap down (n+1 high < n-1 low)
    if high_next < low_prev:
        gap_size = low_prev - high_next
        return True, 'bearish', gap_size
    
    return False, 'none', 0.0


def analyze_1m_fvg(df: pd.DataFrame) -> Dict:
    """
    Analyze FVG patterns for 1-minute timeframe at 8:30 AM opening.
    
    Checks for:
    - FVG on 8:30 candle (gap between 8:29 and 8:31)
    - FVG on 8:31 candle (gap between 8:30 and 8:32)
    """
    results = {
        'total_days': 0,
        'fvg_830': 0,
        'fvg_831': 0,
        'consecutive_fvg': 0,
        'fvg_830_bullish': 0,
        'fvg_830_bearish': 0,
        'fvg_831_bullish': 0,
        'fvg_831_bearish': 0,
        'consecutive_same_direction': 0,
        'consecutive_bullish': 0,
        'consecutive_bearish': 0,
        'days_with_data': []
    }
    
    # Group by date
    df['DateOnly'] = df['Datetime'].dt.date
    grouped = df.groupby('DateOnly')
    
    for date, group in grouped:
        # Get candles for 8:29, 8:30, 8:31, 8:32
        candle_829 = group[group['Time'] == '08:29:00']
        candle_830 = group[group['Time'] == '08:30:00']
        candle_831 = group[group['Time'] == '08:31:00']
        candle_832 = group[group['Time'] == '08:32:00']
        
        # Skip if missing any candle
        if len(candle_829) == 0 or len(candle_830) == 0 or len(candle_831) == 0 or len(candle_832) == 0:
            continue
        
        results['total_days'] += 1
        
        # Check FVG on 8:30 candle (gap between 8:29 and 8:31)
        has_fvg_830, direction_830, gap_830 = check_fvg(
            candle_829.iloc[0], candle_830.iloc[0], candle_831.iloc[0]
        )
        
        # Check FVG on 8:31 candle (gap between 8:30 and 8:32)
        has_fvg_831, direction_831, gap_831 = check_fvg(
            candle_830.iloc[0], candle_831.iloc[0], candle_832.iloc[0]
        )
        
        if has_fvg_830:
            results['fvg_830'] += 1
            if direction_830 == 'bullish':
                results['fvg_830_bullish'] += 1
            else:
                results['fvg_830_bearish'] += 1
        
        if has_fvg_831:
            results['fvg_831'] += 1
            if direction_831 == 'bullish':
                results['fvg_831_bullish'] += 1
            else:
                results['fvg_831_bearish'] += 1
        
        # Check for consecutive FVGs
        if has_fvg_830 and has_fvg_831:
            results['consecutive_fvg'] += 1
            results['days_with_data'].append({
                'date': str(date),
                'fvg_830_direction': direction_830,
                'fvg_830_gap': gap_830,
                'fvg_831_direction': direction_831,
                'fvg_831_gap': gap_831
            })
            
            if direction_830 == direction_831:
                results['consecutive_same_direction'] += 1
                if direction_830 == 'bullish':
                    results['consecutive_bullish'] += 1
                else:
                    results['consecutive_bearish'] += 1
    
    return results


def analyze_5m_fvg(df: pd.DataFrame) -> Dict:
    """
    Analyze FVG patterns for 5-minute timeframe.
    
    For 5m timeframe at 8:30 opening:
    - Check the 8:30 candle (covers 8:30-8:35)
    - Compare with adjacent 5m candles
    """
    results = {
        'total_days': 0,
        'fvg_830': 0,
        'fvg_835': 0,
        'consecutive_fvg': 0,
        'fvg_830_bullish': 0,
        'fvg_830_bearish': 0,
        'fvg_835_bullish': 0,
        'fvg_835_bearish': 0,
        'consecutive_same_direction': 0,
        'consecutive_bullish': 0,
        'consecutive_bearish': 0,
        'days_with_data': []
    }
    
    # Group by date
    df['DateOnly'] = df['Datetime'].dt.date
    grouped = df.groupby('DateOnly')
    
    for date, group in grouped:
        # Get 5m candles: 8:25, 8:30, 8:35, 8:40
        candle_825 = group[group['Time'] == '08:25:00']
        candle_830 = group[group['Time'] == '08:30:00']
        candle_835 = group[group['Time'] == '08:35:00']
        candle_840 = group[group['Time'] == '08:40:00']
        
        # Skip if missing any candle
        if len(candle_825) == 0 or len(candle_830) == 0 or len(candle_835) == 0 or len(candle_840) == 0:
            continue
        
        results['total_days'] += 1
        
        # Check FVG on 8:30 candle (gap between 8:25 and 8:35)
        has_fvg_830, direction_830, gap_830 = check_fvg(
            candle_825.iloc[0], candle_830.iloc[0], candle_835.iloc[0]
        )
        
        # Check FVG on 8:35 candle (gap between 8:30 and 8:40)
        has_fvg_835, direction_835, gap_835 = check_fvg(
            candle_830.iloc[0], candle_835.iloc[0], candle_840.iloc[0]
        )
        
        if has_fvg_830:
            results['fvg_830'] += 1
            if direction_830 == 'bullish':
                results['fvg_830_bullish'] += 1
            else:
                results['fvg_830_bearish'] += 1
        
        if has_fvg_835:
            results['fvg_835'] += 1
            if direction_835 == 'bullish':
                results['fvg_835_bullish'] += 1
            else:
                results['fvg_835_bearish'] += 1
        
        # Check for consecutive FVGs
        if has_fvg_830 and has_fvg_835:
            results['consecutive_fvg'] += 1
            results['days_with_data'].append({
                'date': str(date),
                'fvg_830_direction': direction_830,
                'fvg_830_gap': gap_830,
                'fvg_835_direction': direction_835,
                'fvg_835_gap': gap_835
            })
            
            if direction_830 == direction_835:
                results['consecutive_same_direction'] += 1
                if direction_830 == 'bullish':
                    results['consecutive_bullish'] += 1
                else:
                    results['consecutive_bearish'] += 1
    
    return results


def analyze_15m_fvg(df: pd.DataFrame) -> Dict:
    """
    Analyze FVG patterns for 15-minute timeframe.
    
    For 15m timeframe at 8:30 opening:
    - Check the 8:30 candle (covers 8:30-8:45)
    - Compare with adjacent 15m candles
    """
    results = {
        'total_days': 0,
        'fvg_830': 0,
        'fvg_845': 0,
        'consecutive_fvg': 0,
        'fvg_830_bullish': 0,
        'fvg_830_bearish': 0,
        'fvg_845_bullish': 0,
        'fvg_845_bearish': 0,
        'consecutive_same_direction': 0,
        'consecutive_bullish': 0,
        'consecutive_bearish': 0,
        'days_with_data': []
    }
    
    # Group by date
    df['DateOnly'] = df['Datetime'].dt.date
    grouped = df.groupby('DateOnly')
    
    for date, group in grouped:
        # Get 15m candles: 8:15, 8:30, 8:45, 9:00
        candle_815 = group[group['Time'] == '08:15:00']
        candle_830 = group[group['Time'] == '08:30:00']
        candle_845 = group[group['Time'] == '08:45:00']
        candle_900 = group[group['Time'] == '09:00:00']
        
        # Skip if missing any candle
        if len(candle_815) == 0 or len(candle_830) == 0 or len(candle_845) == 0 or len(candle_900) == 0:
            continue
        
        results['total_days'] += 1
        
        # Check FVG on 8:30 candle (gap between 8:15 and 8:45)
        has_fvg_830, direction_830, gap_830 = check_fvg(
            candle_815.iloc[0], candle_830.iloc[0], candle_845.iloc[0]
        )
        
        # Check FVG on 8:45 candle (gap between 8:30 and 9:00)
        has_fvg_845, direction_845, gap_845 = check_fvg(
            candle_830.iloc[0], candle_845.iloc[0], candle_900.iloc[0]
        )
        
        if has_fvg_830:
            results['fvg_830'] += 1
            if direction_830 == 'bullish':
                results['fvg_830_bullish'] += 1
            else:
                results['fvg_830_bearish'] += 1
        
        if has_fvg_845:
            results['fvg_845'] += 1
            if direction_845 == 'bullish':
                results['fvg_845_bullish'] += 1
            else:
                results['fvg_845_bearish'] += 1
        
        # Check for consecutive FVGs
        if has_fvg_830 and has_fvg_845:
            results['consecutive_fvg'] += 1
            results['days_with_data'].append({
                'date': str(date),
                'fvg_830_direction': direction_830,
                'fvg_830_gap': gap_830,
                'fvg_845_direction': direction_845,
                'fvg_845_gap': gap_845
            })
            
            if direction_830 == direction_845:
                results['consecutive_same_direction'] += 1
                if direction_830 == 'bullish':
                    results['consecutive_bullish'] += 1
                else:
                    results['consecutive_bearish'] += 1
    
    return results


def print_results(results: Dict, timeframe: str, year: str = 'All'):
    """Print analysis results in a formatted manner."""
    print(f"\n{'='*60}")
    print(f"  {timeframe} Timeframe Analysis - Year: {year}")
    print(f"{'='*60}")
    
    if results['total_days'] == 0:
        print("  No valid trading days found with complete data.")
        return
    
    # First FVG candle key - using dictionary for clarity
    first_key = 'fvg_830'
    second_key_map = {'1m': 'fvg_831', '5m': 'fvg_835', '15m': 'fvg_845'}
    second_time_map = {'1m': '08:31', '5m': '08:35', '15m': '08:45'}
    second_key = second_key_map.get(timeframe, 'fvg_831')
    second_time = second_time_map.get(timeframe, '08:31')
    
    print(f"\n  Total Trading Days Analyzed: {results['total_days']}")
    print(f"\n  --- FVG at 08:30 Candle ---")
    print(f"  FVG Found: {results[first_key]} ({results[first_key]/results['total_days']*100:.2f}%)")
    print(f"    - Bullish: {results[first_key + '_bullish']}")
    print(f"    - Bearish: {results[first_key + '_bearish']}")
    
    print(f"\n  --- FVG at {second_time} Candle ---")
    print(f"  FVG Found: {results[second_key]} ({results[second_key]/results['total_days']*100:.2f}%)")
    print(f"    - Bullish: {results[second_key + '_bullish']}")
    print(f"    - Bearish: {results[second_key + '_bearish']}")
    
    print(f"\n  --- Consecutive FVGs (Both Present) ---")
    print(f"  Consecutive FVG Days: {results['consecutive_fvg']} ({results['consecutive_fvg']/results['total_days']*100:.2f}%)")
    
    if results['consecutive_fvg'] > 0:
        print(f"    - Same Direction: {results['consecutive_same_direction']} ({results['consecutive_same_direction']/results['consecutive_fvg']*100:.2f}%)")
        print(f"      - Both Bullish: {results['consecutive_bullish']}")
        print(f"      - Both Bearish: {results['consecutive_bearish']}")


def aggregate_results(all_results: Dict, results: Dict) -> None:
    """Helper function to aggregate results from individual years into totals."""
    for key in all_results:
        if key == 'days_with_data':
            all_results[key].extend(results[key])
        else:
            all_results[key] += results[key]


def main():
    """Main function to run the FVG analysis."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    years = ['2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025']
    
    # Aggregate results for each timeframe
    all_results_1m = {
        'total_days': 0, 'fvg_830': 0, 'fvg_831': 0, 'consecutive_fvg': 0,
        'fvg_830_bullish': 0, 'fvg_830_bearish': 0, 'fvg_831_bullish': 0, 'fvg_831_bearish': 0,
        'consecutive_same_direction': 0, 'consecutive_bullish': 0, 'consecutive_bearish': 0,
        'days_with_data': []
    }
    all_results_5m = {
        'total_days': 0, 'fvg_830': 0, 'fvg_835': 0, 'consecutive_fvg': 0,
        'fvg_830_bullish': 0, 'fvg_830_bearish': 0, 'fvg_835_bullish': 0, 'fvg_835_bearish': 0,
        'consecutive_same_direction': 0, 'consecutive_bullish': 0, 'consecutive_bearish': 0,
        'days_with_data': []
    }
    all_results_15m = {
        'total_days': 0, 'fvg_830': 0, 'fvg_845': 0, 'consecutive_fvg': 0,
        'fvg_830_bullish': 0, 'fvg_830_bearish': 0, 'fvg_845_bullish': 0, 'fvg_845_bearish': 0,
        'consecutive_same_direction': 0, 'consecutive_bullish': 0, 'consecutive_bearish': 0,
        'days_with_data': []
    }
    
    print("\n" + "=" * 80)
    print("  FVG CONSECUTIVE PATTERN ANALYSIS AT 8:30 AM OPENING")
    print("  Analyzing Fair Value Gaps (FVG) with Two Consecutive Patterns")
    print("=" * 80)
    
    for year in years:
        print(f"\n\n{'#' * 80}")
        print(f"  YEAR: {year}")
        print(f"{'#' * 80}")
        
        # Analyze 1m timeframe
        file_1m = os.path.join(base_dir, f"{year} 1m.csv")
        if os.path.exists(file_1m):
            df_1m = load_csv_data(file_1m)
            results_1m = analyze_1m_fvg(df_1m)
            print_results(results_1m, '1m', year)
            aggregate_results(all_results_1m, results_1m)
        else:
            print(f"\n  1m file not found: {file_1m}")
        
        # Analyze 5m timeframe
        file_5m = os.path.join(base_dir, f"{year} 5m.csv")
        if os.path.exists(file_5m):
            df_5m = load_csv_data(file_5m)
            results_5m = analyze_5m_fvg(df_5m)
            print_results(results_5m, '5m', year)
            aggregate_results(all_results_5m, results_5m)
        else:
            print(f"\n  5m file not found: {file_5m}")
        
        # Analyze 15m timeframe
        file_15m = os.path.join(base_dir, f"{year} 15m.csv")
        if os.path.exists(file_15m):
            df_15m = load_csv_data(file_15m)
            results_15m = analyze_15m_fvg(df_15m)
            print_results(results_15m, '15m', year)
            aggregate_results(all_results_15m, results_15m)
        else:
            print(f"\n  15m file not found: {file_15m}")
    
    # Print aggregate results
    print("\n\n" + "=" * 80)
    print("  AGGREGATE RESULTS - ALL YEARS (2018-2025)")
    print("=" * 80)
    
    print_results(all_results_1m, '1m', 'All (2018-2025)')
    print_results(all_results_5m, '5m', 'All (2018-2025)')
    print_results(all_results_15m, '15m', 'All (2018-2025)')
    
    # Print summary ratio table
    print("\n\n" + "=" * 80)
    print("  SUMMARY RATIO TABLE - FVG OCCURRENCES")
    print("=" * 80)
    
    print(f"\n  {'Timeframe':<12} {'Total Days':<15} {'FVG 1st':<15} {'FVG 2nd':<15} {'Consecutive':<15} {'Ratio':<10}")
    print(f"  {'-'*12} {'-'*15} {'-'*15} {'-'*15} {'-'*15} {'-'*10}")
    
    if all_results_1m['total_days'] > 0:
        ratio_1m = all_results_1m['consecutive_fvg'] / all_results_1m['total_days'] * 100
        print(f"  {'1 minute':<12} {all_results_1m['total_days']:<15} {all_results_1m['fvg_830']:<15} {all_results_1m['fvg_831']:<15} {all_results_1m['consecutive_fvg']:<15} {ratio_1m:.2f}%")
    
    if all_results_5m['total_days'] > 0:
        ratio_5m = all_results_5m['consecutive_fvg'] / all_results_5m['total_days'] * 100
        print(f"  {'5 minutes':<12} {all_results_5m['total_days']:<15} {all_results_5m['fvg_830']:<15} {all_results_5m['fvg_835']:<15} {all_results_5m['consecutive_fvg']:<15} {ratio_5m:.2f}%")
    
    if all_results_15m['total_days'] > 0:
        ratio_15m = all_results_15m['consecutive_fvg'] / all_results_15m['total_days'] * 100
        print(f"  {'15 minutes':<12} {all_results_15m['total_days']:<15} {all_results_15m['fvg_830']:<15} {all_results_15m['fvg_845']:<15} {all_results_15m['consecutive_fvg']:<15} {ratio_15m:.2f}%")
    
    # Print detailed consecutive FVG days for 1m (sample)
    print("\n\n" + "=" * 80)
    print("  SAMPLE: CONSECUTIVE FVG DAYS (1m timeframe - First 20)")
    print("=" * 80)
    
    if len(all_results_1m['days_with_data']) > 0:
        print(f"\n  {'Date':<15} {'FVG 8:30':<12} {'Gap Size':<15} {'FVG 8:31':<12} {'Gap Size':<15}")
        print(f"  {'-'*15} {'-'*12} {'-'*15} {'-'*12} {'-'*15}")
        
        for day in all_results_1m['days_with_data'][:20]:
            print(f"  {day['date']:<15} {day['fvg_830_direction']:<12} {day['fvg_830_gap']:<15.4f} {day['fvg_831_direction']:<12} {day['fvg_831_gap']:<15.4f}")


if __name__ == "__main__":
    main()

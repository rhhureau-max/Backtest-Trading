#!/usr/bin/env python3
"""
Analyze Fair Value Gap (FVG) quality at 8:30 AM candle with multiple candle windows
Analyzes trading data files from 2018 onwards for 1m, 5m, and 15m timeframes
Tests different candle windows: 5, 10, 15, 20, 25, 30, 50 candles

FVG Quality Definition:
- Good FVG: Price doesn't return to FVG zone after X candles
- Bad FVG: Price returns to FVG zone after X candles
"""

import pandas as pd
import os
from datetime import time, datetime

def load_data_file(filename):
    """Load a data file (XLSX or CSV)"""
    if filename.endswith('.xlsx'):
        return pd.read_excel(filename)
    elif filename.endswith('.csv'):
        # CSV files in this dataset use semicolon as delimiter
        return pd.read_csv(filename, sep=';')
    else:
        raise ValueError(f"Unsupported file format: {filename}")

def analyze_fvg_quality_multiwindow(df, year, timeframe, candle_windows):
    """
    Analyze FVG quality at 8:30 AM for a given year with multiple candle windows
    
    Parameters:
    - df: DataFrame with OHLC data
    - year: Year being analyzed
    - timeframe: '1m', '5m', or '15m'
    - candle_windows: List of candle windows to test (e.g., [5, 10, 15, 20, 25, 30, 50])
    
    Returns dict with results for each window
    """
    # Find all 8:30 AM entries
    target_time = time(8, 30)
    
    # Check if DataFrame is empty
    if len(df) == 0:
        return {window: {'year': year, 'total_fvg': 0, 'good_bullish': 0, 'bad_bullish': 0,
                        'good_bearish': 0, 'bad_bearish': 0} for window in candle_windows}
    
    # Handle both time objects and string formats
    if 'Column2' not in df.columns:
        return {window: {'year': year, 'total_fvg': 0, 'good_bullish': 0, 'bad_bullish': 0,
                        'good_bearish': 0, 'bad_bearish': 0} for window in candle_windows}
    
    # Convert Column2 to time if needed
    if df['Column2'].dtype == 'object':
        try:
            df['Column2'] = pd.to_datetime(df['Column2'], format='%H:%M:%S').dt.time
        except:
            try:
                df['Column2'] = pd.to_datetime(df['Column2'], format='%H:%M').dt.time
            except:
                pass
    
    # Initialize results for each window
    results = {}
    for window in candle_windows:
        results[window] = {
            'year': year,
            'total_fvg': 0,
            'good_bullish': 0,
            'bad_bullish': 0,
            'good_bearish': 0,
            'bad_bearish': 0
        }
    
    # Store FVG data for processing
    fvg_data = []
    
    # Find FVG occurrences at 8:30
    for idx in df.index:
        if idx == 0 or idx >= len(df) - 1:
            continue
        
        current_time = df.loc[idx, 'Column2']
        if isinstance(current_time, str):
            if current_time not in ['08:30:00', '8:30:00', '08:30', '8:30']:
                continue
        elif current_time != target_time:
            continue
        
        # Get the three candles for FVG detection
        candle_prev = df.loc[idx - 1]  # Previous candle
        candle_current = df.loc[idx]   # Current (8:30)
        candle_next = df.loc[idx + 1]  # Next candle
        
        # Validate adjacent candles based on timeframe
        if timeframe == '1m':
            expected_prev_times = ['08:29:00', '8:29:00', '08:29', '8:29']
            expected_next_times = ['08:31:00', '8:31:00', '08:31', '8:31']
        elif timeframe == '5m':
            expected_prev_times = ['08:25:00', '8:25:00', '08:25', '8:25']
            expected_next_times = ['08:35:00', '8:35:00', '08:35', '8:35']
        elif timeframe == '15m':
            expected_prev_times = ['08:15:00', '8:15:00', '08:15', '8:15']
            expected_next_times = ['08:45:00', '8:45:00', '08:45', '8:45']
        
        prev_time = candle_prev['Column2']
        if isinstance(prev_time, str):
            if prev_time not in expected_prev_times:
                continue
        
        next_time = candle_next['Column2']
        if isinstance(next_time, str):
            if next_time not in expected_next_times:
                continue
        
        # Extract OHLC values (Column3=Open, Column4=High, Column5=Low, Column6=Close)
        high_prev = float(candle_prev['Column4'])
        low_prev = float(candle_prev['Column5'])
        high_next = float(candle_next['Column4'])
        low_next = float(candle_next['Column5'])
        
        # Check for FVG
        is_bullish_fvg = low_next > high_prev
        is_bearish_fvg = high_next < low_prev
        
        if not is_bullish_fvg and not is_bearish_fvg:
            continue
        
        # Store FVG data for processing with different windows
        fvg_info = {
            'idx': idx,
            'is_bullish': is_bullish_fvg,
            'is_bearish': is_bearish_fvg,
            'fvg_low': high_prev if is_bullish_fvg else high_next,
            'fvg_high': low_next if is_bullish_fvg else low_prev
        }
        fvg_data.append(fvg_info)
    
    # Process each FVG with different candle windows
    for fvg in fvg_data:
        idx = fvg['idx']
        
        for window in candle_windows:
            # Get next N candles AFTER the third candle closes
            next_candles = df.loc[idx+2:idx+1+window]
            
            if len(next_candles) < window:
                continue  # Not enough data for this window
            
            results[window]['total_fvg'] += 1
            
            # Check if price returns to FVG zone
            price_returned = False
            for i in range(len(next_candles)):
                candle_low = float(next_candles.iloc[i]['Column5'])
                candle_high = float(next_candles.iloc[i]['Column4'])
                
                # Check if candle overlaps with FVG zone
                if candle_low <= fvg['fvg_high'] and candle_high >= fvg['fvg_low']:
                    price_returned = True
                    break
            
            if fvg['is_bullish']:
                if price_returned:
                    results[window]['bad_bullish'] += 1
                else:
                    results[window]['good_bullish'] += 1
            elif fvg['is_bearish']:
                if price_returned:
                    results[window]['bad_bearish'] += 1
                else:
                    results[window]['good_bearish'] += 1
    
    return results

def main():
    """Main analysis function"""
    candle_windows = [5, 10, 15, 20, 25, 30, 50]
    timeframes = {
        '1m': ('1m', '1-Minute'),
        '5m': ('5m', '5-Minute'),
        '15m': ('15m', '15-Minute')
    }
    
    years = range(2018, 2026)
    
    for tf_key, (tf_suffix, tf_name) in timeframes.items():
        print(f"\n{'='*80}")
        print(f"ANALYZING {tf_name.upper()} DATA")
        print(f"{'='*80}\n")
        
        # Initialize aggregated results
        total_results = {window: {
            'years': {},
            'total': {'total_fvg': 0, 'good_bullish': 0, 'bad_bullish': 0,
                     'good_bearish': 0, 'bad_bearish': 0}
        } for window in candle_windows}
        
        # Process each year
        for year in years:
            if year == 2025:
                filename = f'{year} {tf_suffix}.csv'
            else:
                if tf_key == '1m':
                    filename = f'{year} {tf_suffix}.xlsx'
                else:
                    filename = f'{year} {tf_suffix}.csv'
            
            if not os.path.exists(filename):
                print(f"✗ File not found: {filename}")
                continue
            
            print(f"Analyzing {filename}...")
            try:
                df = load_data_file(filename)
                year_results = analyze_fvg_quality_multiwindow(df, year, tf_key, candle_windows)
                
                for window in candle_windows:
                    total_results[window]['years'][year] = year_results[window]
                    total_results[window]['total']['total_fvg'] += year_results[window]['total_fvg']
                    total_results[window]['total']['good_bullish'] += year_results[window]['good_bullish']
                    total_results[window]['total']['bad_bullish'] += year_results[window]['bad_bullish']
                    total_results[window]['total']['good_bearish'] += year_results[window]['good_bearish']
                    total_results[window]['total']['bad_bearish'] += year_results[window]['bad_bearish']
                
                print(f"✓ {year} processed")
                
            except Exception as e:
                print(f"✗ Error processing {filename}: {str(e)}")
                continue
        
        # Generate markdown report
        generate_md_report(tf_key, tf_name, total_results, candle_windows)

def generate_md_report(tf_key, tf_name, total_results, candle_windows):
    """Generate markdown report for a timeframe"""
    filename = f"FVG_Quality_MultiWindow_{tf_key}.md"
    
    with open(filename, 'w') as f:
        f.write(f"# FVG Quality Analysis - {tf_name} Data (Multiple Candle Windows)\n\n")
        f.write(f"## Overview\n\n")
        f.write(f"This document analyzes FVG quality at 8:30 AM using different look-ahead windows.\n")
        f.write(f"Tested candle windows: {', '.join(map(str, candle_windows))} candles\n\n")
        
        f.write(f"---\n\n")
        
        # Overall comparison table
        f.write(f"## Overall Results by Candle Window (2018-2025)\n\n")
        f.write(f"| Window | Total FVG | Good FVG | Good % | Bad FVG | Bad % |\n")
        f.write(f"|--------|-----------|----------|--------|---------|-------|\n")
        
        for window in candle_windows:
            total = total_results[window]['total']
            total_fvg = total['total_fvg']
            good_fvg = total['good_bullish'] + total['good_bearish']
            bad_fvg = total['bad_bullish'] + total['bad_bearish']
            good_pct = (good_fvg / total_fvg * 100) if total_fvg > 0 else 0
            bad_pct = (bad_fvg / total_fvg * 100) if total_fvg > 0 else 0
            
            f.write(f"| {window} | {total_fvg} | {good_fvg} | {good_pct:.2f}% | {bad_fvg} | {bad_pct:.2f}% |\n")
        
        f.write(f"\n---\n\n")
        
        # Detailed results for each window
        for window in candle_windows:
            f.write(f"## {window}-Candle Window Analysis\n\n")
            
            # Year-by-year table
            f.write(f"### Year-by-Year Breakdown\n\n")
            f.write(f"| Year | Total FVG | Good Bull | Bad Bull | Good Bear | Bad Bear | Good % |\n")
            f.write(f"|------|-----------|-----------|----------|-----------|----------|--------|\n")
            
            years = sorted(total_results[window]['years'].keys())
            for year in years:
                data = total_results[window]['years'][year]
                total_fvg = data['total_fvg']
                good_fvg = data['good_bullish'] + data['good_bearish']
                good_pct = (good_fvg / total_fvg * 100) if total_fvg > 0 else 0
                
                f.write(f"| {year} | {total_fvg} | {data['good_bullish']} | {data['bad_bullish']} | ")
                f.write(f"{data['good_bearish']} | {data['bad_bearish']} | {good_pct:.2f}% |\n")
            
            # Total row
            total = total_results[window]['total']
            total_fvg = total['total_fvg']
            good_fvg = total['good_bullish'] + total['good_bearish']
            good_pct = (good_fvg / total_fvg * 100) if total_fvg > 0 else 0
            
            f.write(f"| **TOTAL** | **{total_fvg}** | **{total['good_bullish']}** | **{total['bad_bullish']}** | ")
            f.write(f"**{total['good_bearish']}** | **{total['bad_bearish']}** | **{good_pct:.2f}%** |\n\n")
            
            f.write(f"---\n\n")
    
    print(f"\n✓ Report saved to {filename}\n")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
FVG Size vs Maximum Excursion Analysis
Analyzes the relationship between FVG size and the maximum price excursion
achieved before price returns to the FVG zone (for Good FVG only)
"""

import pandas as pd
import os
from datetime import datetime, time

def load_data(filepath, timeframe):
    """Load data from XLSX or CSV file"""
    if filepath.endswith('.xlsx'):
        df = pd.read_excel(filepath)
    else:
        # For CSV files (2025), use semicolon delimiter
        df = pd.read_csv(filepath, delimiter=';')
    
    # Validate columns
    expected_cols = 5  # time, open, high, low, close
    if len(df.columns) < expected_cols:
        raise ValueError(f"Expected at least {expected_cols} columns, got {len(df.columns)}")
    
    # Rename columns to standard names
    df.columns = ['time', 'open', 'high', 'low', 'close'] + list(df.columns[5:])
    
    # Convert time to datetime
    df['time'] = pd.to_datetime(df['time'])
    
    return df

def identify_fvg_with_excursion(df, timeframe='1m'):
    """Identify FVG and calculate max excursion for Good FVG"""
    results = []
    
    # Define target time based on timeframe
    if timeframe == '1m':
        target_time = time(8, 30)
        check_candles = 5  # Check next 5 candles (8:32-8:36)
    elif timeframe == '5m':
        target_time = time(8, 30)
        check_candles = 5  # Check next 5 candles (8:35-9:00)
    else:  # 15m
        target_time = time(8, 30)
        check_candles = 5  # Check next 5 candles (8:45-10:00)
    
    # Group by date
    df['date'] = df['time'].dt.date
    
    for date, day_data in df.groupby('date'):
        day_data = day_data.sort_values('time').reset_index(drop=True)
        
        # Find 8:30 candle
        target_idx = day_data[day_data['time'].dt.time == target_time].index
        
        if len(target_idx) == 0:
            continue
            
        idx = target_idx[0]
        
        # Need previous and next candle
        if idx < 1 or idx >= len(day_data) - 1:
            continue
        
        prev_candle = day_data.iloc[idx - 1]
        curr_candle = day_data.iloc[idx]
        next_candle = day_data.iloc[idx + 1]
        
        # Check for FVG
        # Bullish FVG: low of candle 3 > high of candle 1
        bullish_fvg = next_candle['low'] > prev_candle['high']
        # Bearish FVG: high of candle 3 < low of candle 1
        bearish_fvg = next_candle['high'] < prev_candle['low']
        
        if not (bullish_fvg or bearish_fvg):
            continue
        
        fvg_type = 'Bullish' if bullish_fvg else 'Bearish'
        
        # Calculate FVG size
        if bullish_fvg:
            fvg_low = prev_candle['high']
            fvg_high = next_candle['low']
            fvg_size = fvg_high - fvg_low
        else:
            fvg_low = next_candle['high']
            fvg_high = prev_candle['low']
            fvg_size = fvg_high - fvg_low
        
        # Check if Good FVG (doesn't return in next 5 candles)
        is_good = True
        max_excursion_ticks = 0
        
        # Check next 5 candles after the 3rd candle (idx+1)
        for check_idx in range(idx + 2, min(idx + 2 + check_candles, len(day_data))):
            check_candle = day_data.iloc[check_idx]
            
            # Calculate excursion from close of 3rd candle
            if bullish_fvg:
                excursion = check_candle['high'] - next_candle['close']
            else:
                excursion = next_candle['close'] - check_candle['low']
            
            excursion_ticks = excursion * 4  # Convert to ticks
            max_excursion_ticks = max(max_excursion_ticks, excursion_ticks)
            
            # Check if price returns to FVG zone
            if bullish_fvg:
                if check_candle['low'] <= fvg_high and check_candle['high'] >= fvg_low:
                    is_good = False
            else:
                if check_candle['high'] >= fvg_low and check_candle['low'] <= fvg_high:
                    is_good = False
        
        if is_good:
            results.append({
                'date': date,
                'type': fvg_type,
                'size_ticks': fvg_size * 4,
                'max_excursion_ticks': max_excursion_ticks,
                'fvg_low': fvg_low,
                'fvg_high': fvg_high
            })
    
    return pd.DataFrame(results)

def analyze_by_size_bins(df):
    """Analyze maximum excursion by size bins"""
    
    # Define size bins
    bins = [0, 4, 8, 12, 16, 20, 30, 50, 100, float('inf')]
    labels = ['0-4', '4-8', '8-12', '12-16', '16-20', '20-30', '30-50', '50-100', '100+']
    
    df['size_bin'] = pd.cut(df['size_ticks'], bins=bins, labels=labels, right=False)
    
    results = []
    for bin_label in labels:
        bin_data = df[df['size_bin'] == bin_label]
        
        if len(bin_data) == 0:
            continue
        
        results.append({
            'size_bin': bin_label,
            'count': len(bin_data),
            'avg_size': bin_data['size_ticks'].mean(),
            'avg_excursion': bin_data['max_excursion_ticks'].mean(),
            'median_excursion': bin_data['max_excursion_ticks'].median(),
            'min_excursion': bin_data['max_excursion_ticks'].min(),
            'max_excursion': bin_data['max_excursion_ticks'].max()
        })
    
    return pd.DataFrame(results)

def main():
    base_dir = '/home/runner/work/Backtest-Trading/Backtest-Trading'
    os.chdir(base_dir)
    
    results_all = {}
    
    # Analyze each timeframe
    timeframes = {
        '1m': ['1m.xlsx', '1m.csv'],
        '5m': ['5m.csv'],
        '15m': ['15m.csv']
    }
    
    for tf_name, tf_extensions in timeframes.items():
        print(f"\n{'='*60}")
        print(f"Analyzing {tf_name} timeframe")
        print(f"{'='*60}")
        
        all_fvg = []
        
        # Process 2018-2024 (skip 2025 for now due to date format issues)
        for year in range(2018, 2025):
            # Try different file formats
            df = None
            for ext in tf_extensions:
                filepath = f"{year} {ext}"
                if os.path.exists(filepath):
                    try:
                        print(f"Processing {filepath}...")
                        df = load_data(filepath, tf_name)
                        break
                    except Exception as e:
                        print(f"Error loading {filepath}: {e}")
                        continue
            
            if df is None:
                continue
            
            year_fvg = identify_fvg_with_excursion(df, tf_name)
            print(f"  Found {len(year_fvg)} Good FVG in {year}")
            if len(year_fvg) > 0:
                all_fvg.append(year_fvg)
        
        # Combine all years
        if all_fvg:
            combined_fvg = pd.concat(all_fvg, ignore_index=True)
            print(f"\nTotal Good FVG found: {len(combined_fvg)}")
            
            # Analyze by size bins
            size_analysis = analyze_by_size_bins(combined_fvg)
            
            print(f"\n{tf_name.upper()} Size vs Excursion Analysis:")
            print(size_analysis.to_string(index=False))
            
            results_all[tf_name] = {
                'fvg_data': combined_fvg,
                'size_analysis': size_analysis
            }
    
    # Save results to file
    output_file = 'fvg_size_excursion_analysis.txt'
    with open(output_file, 'w') as f:
        f.write("FVG Size vs Maximum Excursion Analysis (2018-2025)\n")
        f.write("=" * 80 + "\n\n")
        
        for tf_name in ['1m', '5m', '15m']:
            if tf_name not in results_all:
                continue
            
            f.write(f"\n{tf_name.upper()} TIMEFRAME\n")
            f.write("-" * 80 + "\n")
            
            analysis = results_all[tf_name]['size_analysis']
            f.write(analysis.to_string(index=False))
            f.write("\n\n")
            
            f.write("Summary by Type:\n")
            fvg_data = results_all[tf_name]['fvg_data']
            
            for fvg_type in ['Bullish', 'Bearish']:
                type_data = fvg_data[fvg_data['type'] == fvg_type]
                if len(type_data) > 0:
                    f.write(f"\n{fvg_type}:\n")
                    f.write(f"  Count: {len(type_data)}\n")
                    f.write(f"  Avg Size: {type_data['size_ticks'].mean():.2f} ticks\n")
                    f.write(f"  Avg Excursion: {type_data['max_excursion_ticks'].mean():.2f} ticks\n")
            
            f.write("\n" + "=" * 80 + "\n")
    
    print(f"\nResults saved to: {output_file}")
    
    return results_all

if __name__ == "__main__":
    main()

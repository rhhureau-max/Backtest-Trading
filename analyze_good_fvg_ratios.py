#!/usr/bin/env python3
"""
Analyze the ratio of Good Bullish FVG and Good Bearish FVG compared to total FVG
across all timeframes (2018-2025)
"""

import pandas as pd
import os
from datetime import time

def load_data_file(filename):
    """Load a data file (XLSX or CSV)"""
    if filename.endswith('.xlsx'):
        return pd.read_excel(filename)
    elif filename.endswith('.csv'):
        # CSV files in this dataset use semicolon as delimiter
        return pd.read_csv(filename, sep=';')
    else:
        raise ValueError(f"Unsupported file format: {filename}")

def analyze_fvg_and_quality(df, timeframe='1m'):
    """
    Analyze all FVG and determine which are Good FVG
    
    Args:
        df: DataFrame with OHLCV data
        timeframe: '1m', '5m', or '15m'
    
    Returns:
        dict with FVG counts
    """
    # Define target time based on timeframe
    if timeframe == '1m':
        target_time = time(8, 30)
        prev_time_str = ['08:29:00', '8:29:00', '08:29', '8:29']
        next_time_str = ['08:31:00', '8:31:00', '08:31', '8:31']
        check_window = 5  # Check 5 candles after (8:32-8:36)
    elif timeframe == '5m':
        target_time = time(8, 30)
        prev_time_str = ['08:25:00', '8:25:00', '08:25', '8:25']
        next_time_str = ['08:35:00', '8:35:00', '08:35', '8:35']
        check_window = 5  # Check 5 candles after (8:40-9:00)
    elif timeframe == '15m':
        target_time = time(8, 30)
        prev_time_str = ['08:15:00', '8:15:00', '08:15', '8:15']
        next_time_str = ['08:45:00', '8:45:00', '08:45', '8:45']
        check_window = 5  # Check 5 candles after (9:00-10:00)
    else:
        raise ValueError(f"Unsupported timeframe: {timeframe}")
    
    # Standardize column names
    # Expected format: Column1=Date, Column2=Time, Column3=Open, Column4=High, Column5=Low, Column6=Close, Column7=Volume
    if 'Column1' in df.columns:
        df = df.rename(columns={
            'Column1': 'Date',
            'Column2': 'Time',
            'Column3': 'Open',
            'Column4': 'High',
            'Column5': 'Low',
            'Column6': 'Close',
            'Column7': 'Volume'
        })
    
    # Ensure the DataFrame has the required columns
    required_cols = ['Open', 'High', 'Low', 'Close', 'Time']
    if not all(col in df.columns for col in required_cols):
        raise ValueError(f"DataFrame missing required columns. Has: {df.columns.tolist()}")
    
    # Convert Time column if it's a string
    if df['Time'].dtype == 'object':
        # Handle both time objects and string formats
        if not isinstance(df['Time'].iloc[0], time):
            # It's a string, parse it
            df['Time_str'] = df['Time'].astype(str)
            df['time_only'] = pd.to_datetime(df['Time_str'], format='%H:%M:%S', errors='coerce').dt.time
        else:
            df['time_only'] = df['Time']
    else:
        df['time_only'] = pd.to_datetime(df['Time'], format='%H:%M:%S', errors='coerce').dt.time
    
    # Remove rows with invalid time
    df = df.dropna(subset=['time_only']).reset_index(drop=True)
    
    total_bullish_fvg = 0
    total_bearish_fvg = 0
    good_bullish_fvg = 0
    good_bearish_fvg = 0
    
    # Find all FVG at 8:30
    target_indices = df[df['time_only'] == target_time].index.tolist()
    
    for idx in target_indices:
        # Make sure we have enough candles before and after
        if idx < 1 or idx >= len(df) - 6:
            continue
        
        # Get adjacent candles (in sequential order, they should be the right times)
        prev_candle = df.iloc[idx - 1]
        current_candle = df.iloc[idx]
        next_candle = df.iloc[idx + 1]
        next_idx = idx + 1
        
        # Validate the adjacent times match what we expect for this timeframe
        # For simplicity, we'll trust the data is sequential and correctly formatted
        
        # Check for FVG
        is_bullish_fvg = next_candle['Low'] > prev_candle['High']
        is_bearish_fvg = next_candle['High'] < prev_candle['Low']
        
        if not is_bullish_fvg and not is_bearish_fvg:
            continue
        
        # We have an FVG - now check if it's good or bad
        # Get the next 'check_window' candles after the third candle
        check_candles = df.iloc[next_idx + 1:next_idx + 1 + check_window]
        
        if len(check_candles) < check_window:
            continue
        
        is_good_fvg = True
        
        if is_bullish_fvg:
            total_bullish_fvg += 1
            fvg_high = prev_candle['High']
            fvg_low = next_candle['Low']
            
            # Check if price returns to FVG zone
            for _, candle in check_candles.iterrows():
                if candle['Low'] <= fvg_high:
                    is_good_fvg = False
                    break
            
            if is_good_fvg:
                good_bullish_fvg += 1
                
        elif is_bearish_fvg:
            total_bearish_fvg += 1
            fvg_high = next_candle['High']
            fvg_low = prev_candle['Low']
            
            # Check if price returns to FVG zone
            for _, candle in check_candles.iterrows():
                if candle['High'] >= fvg_low:
                    is_good_fvg = False
                    break
            
            if is_good_fvg:
                good_bearish_fvg += 1
    
    return {
        'total_bullish': total_bullish_fvg,
        'total_bearish': total_bearish_fvg,
        'good_bullish': good_bullish_fvg,
        'good_bearish': good_bearish_fvg
    }

def main():
    years = [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]
    timeframes = {
        '1m': '1m',
        '5m': '5m',
        '15m': '15m'
    }
    
    results = {tf: {'total_bullish': 0, 'total_bearish': 0, 'good_bullish': 0, 'good_bearish': 0} 
               for tf in timeframes}
    
    for tf_name, tf_code in timeframes.items():
        print(f"\nProcessing {tf_name} timeframe...")
        
        for year in years:
            # Try both XLSX and CSV formats
            xlsx_filename = f'{year} {tf_code}.xlsx'
            csv_filename = f'{year} {tf_code}.csv'
            
            filename = None
            if os.path.exists(xlsx_filename):
                filename = xlsx_filename
            elif os.path.exists(csv_filename):
                filename = csv_filename
            
            if filename is None:
                print(f"  File not found for {year} (tried {xlsx_filename} and {csv_filename}), skipping...")
                continue
            
            print(f"  Analyzing {year}...")
            df = load_data_file(filename)
            year_results = analyze_fvg_and_quality(df, timeframe=tf_code)
            
            results[tf_name]['total_bullish'] += year_results['total_bullish']
            results[tf_name]['total_bearish'] += year_results['total_bearish']
            results[tf_name]['good_bullish'] += year_results['good_bullish']
            results[tf_name]['good_bearish'] += year_results['good_bearish']
    
    # Generate report
    print("\n" + "="*80)
    print("GOOD FVG RATIO ANALYSIS (2018-2025)")
    print("="*80)
    print("\nRatio of Good Bullish and Good Bearish FVG compared to Total FVG")
    print("across all three timeframes, all periods combined (2018-2025)")
    print("="*80)
    
    output_lines = []
    output_lines.append("="*80)
    output_lines.append("GOOD FVG RATIO ANALYSIS (2018-2025)")
    output_lines.append("="*80)
    output_lines.append("")
    output_lines.append("Ratio of Good Bullish and Good Bearish FVG compared to Total FVG")
    output_lines.append("across all three timeframes, all periods combined (2018-2025)")
    output_lines.append("="*80)
    output_lines.append("")
    
    for tf_name in ['1m', '5m', '15m']:
        data = results[tf_name]
        total_fvg = data['total_bullish'] + data['total_bearish']
        good_fvg = data['good_bullish'] + data['good_bearish']
        
        if total_fvg == 0:
            continue
        
        # Calculate percentages
        bullish_pct = (data['total_bullish'] / total_fvg * 100) if total_fvg > 0 else 0
        bearish_pct = (data['total_bearish'] / total_fvg * 100) if total_fvg > 0 else 0
        good_bullish_pct = (data['good_bullish'] / total_fvg * 100) if total_fvg > 0 else 0
        good_bearish_pct = (data['good_bearish'] / total_fvg * 100) if total_fvg > 0 else 0
        good_fvg_pct = (good_fvg / total_fvg * 100) if total_fvg > 0 else 0
        
        # Calculate ratio of good within each type
        good_of_bullish_pct = (data['good_bullish'] / data['total_bullish'] * 100) if data['total_bullish'] > 0 else 0
        good_of_bearish_pct = (data['good_bearish'] / data['total_bearish'] * 100) if data['total_bearish'] > 0 else 0
        
        print(f"\n{tf_name.upper()} TIMEFRAME:")
        print("-" * 80)
        print(f"Total FVG:                    {total_fvg:4d}")
        print(f"  - Bullish FVG:              {data['total_bullish']:4d} ({bullish_pct:5.2f}% of total)")
        print(f"  - Bearish FVG:              {data['total_bearish']:4d} ({bearish_pct:5.2f}% of total)")
        print()
        print(f"Good FVG (total):             {good_fvg:4d} ({good_fvg_pct:5.2f}% of total FVG)")
        print(f"  - Good Bullish FVG:         {data['good_bullish']:4d} ({good_bullish_pct:5.2f}% of total FVG)")
        print(f"  - Good Bearish FVG:         {data['good_bearish']:4d} ({good_bearish_pct:5.2f}% of total FVG)")
        print()
        print(f"Good FVG Quality by Type:")
        print(f"  - Good of all Bullish FVG:  {data['good_bullish']:4d} / {data['total_bullish']:4d} = {good_of_bullish_pct:5.2f}%")
        print(f"  - Good of all Bearish FVG:  {data['good_bearish']:4d} / {data['total_bearish']:4d} = {good_of_bearish_pct:5.2f}%")
        
        output_lines.append(f"{tf_name.upper()} TIMEFRAME:")
        output_lines.append("-" * 80)
        output_lines.append(f"Total FVG:                    {total_fvg:4d}")
        output_lines.append(f"  - Bullish FVG:              {data['total_bullish']:4d} ({bullish_pct:5.2f}% of total)")
        output_lines.append(f"  - Bearish FVG:              {data['total_bearish']:4d} ({bearish_pct:5.2f}% of total)")
        output_lines.append("")
        output_lines.append(f"Good FVG (total):             {good_fvg:4d} ({good_fvg_pct:5.2f}% of total FVG)")
        output_lines.append(f"  - Good Bullish FVG:         {data['good_bullish']:4d} ({good_bullish_pct:5.2f}% of total FVG)")
        output_lines.append(f"  - Good Bearish FVG:         {data['good_bearish']:4d} ({good_bearish_pct:5.2f}% of total FVG)")
        output_lines.append("")
        output_lines.append(f"Good FVG Quality by Type:")
        output_lines.append(f"  - Good of all Bullish FVG:  {data['good_bullish']:4d} / {data['total_bullish']:4d} = {good_of_bullish_pct:5.2f}%")
        output_lines.append(f"  - Good of all Bearish FVG:  {data['good_bearish']:4d} / {data['total_bearish']:4d} = {good_of_bearish_pct:5.2f}%")
        output_lines.append("")
    
    # Summary comparison
    print("\n" + "="*80)
    print("SUMMARY COMPARISON ACROSS TIMEFRAMES")
    print("="*80)
    print(f"\n{'Timeframe':<12} {'Total FVG':<12} {'Bullish':<12} {'Bearish':<12} {'Good FVG':<12} {'Good %':<10}")
    print("-" * 80)
    
    output_lines.append("="*80)
    output_lines.append("SUMMARY COMPARISON ACROSS TIMEFRAMES")
    output_lines.append("="*80)
    output_lines.append("")
    output_lines.append(f"{'Timeframe':<12} {'Total FVG':<12} {'Bullish':<12} {'Bearish':<12} {'Good FVG':<12} {'Good %':<10}")
    output_lines.append("-" * 80)
    
    for tf_name in ['1m', '5m', '15m']:
        data = results[tf_name]
        total_fvg = data['total_bullish'] + data['total_bearish']
        good_fvg = data['good_bullish'] + data['good_bearish']
        good_pct = (good_fvg / total_fvg * 100) if total_fvg > 0 else 0
        
        print(f"{tf_name.upper():<12} {total_fvg:<12d} {data['total_bullish']:<12d} {data['total_bearish']:<12d} {good_fvg:<12d} {good_pct:5.2f}%")
        output_lines.append(f"{tf_name.upper():<12} {total_fvg:<12d} {data['total_bullish']:<12d} {data['total_bearish']:<12d} {good_fvg:<12d} {good_pct:5.2f}%")
    
    print("\n" + "="*80)
    print("GOOD FVG DISTRIBUTION")
    print("="*80)
    print(f"\n{'Timeframe':<12} {'Good Bullish':<15} {'Good Bearish':<15} {'Bull/Total %':<15} {'Bear/Total %':<15}")
    print("-" * 80)
    
    output_lines.append("")
    output_lines.append("="*80)
    output_lines.append("GOOD FVG DISTRIBUTION")
    output_lines.append("="*80)
    output_lines.append("")
    output_lines.append(f"{'Timeframe':<12} {'Good Bullish':<15} {'Good Bearish':<15} {'Bull/Total %':<15} {'Bear/Total %':<15}")
    output_lines.append("-" * 80)
    
    for tf_name in ['1m', '5m', '15m']:
        data = results[tf_name]
        total_fvg = data['total_bullish'] + data['total_bearish']
        good_bull_pct = (data['good_bullish'] / total_fvg * 100) if total_fvg > 0 else 0
        good_bear_pct = (data['good_bearish'] / total_fvg * 100) if total_fvg > 0 else 0
        
        print(f"{tf_name.upper():<12} {data['good_bullish']:<15d} {data['good_bearish']:<15d} {good_bull_pct:<14.2f}% {good_bear_pct:<14.2f}%")
        output_lines.append(f"{tf_name.upper():<12} {data['good_bullish']:<15d} {data['good_bearish']:<15d} {good_bull_pct:<14.2f}% {good_bear_pct:<14.2f}%")
    
    # Write to file
    with open('good_fvg_ratio_analysis.txt', 'w') as f:
        f.write('\n'.join(output_lines))
    
    print("\n" + "="*80)
    print("Analysis complete! Results saved to 'good_fvg_ratio_analysis.txt'")
    print("="*80)

if __name__ == '__main__':
    main()

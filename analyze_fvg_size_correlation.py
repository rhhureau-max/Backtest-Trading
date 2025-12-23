#!/usr/bin/env python3
"""
Analyze correlation between FVG size (in ticks) and FVG quality
Determines if larger FVG gaps have better continuation or higher retracement rates
Analyzes 1-minute, 5-minute, and 15-minute trading data from 2018 onwards
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

def analyze_fvg_size_correlation(df, year, timeframe_name, prev_time_str, curr_time_str, next_time_str):
    """
    Analyze correlation between FVG size and quality
    
    Returns list of dicts with FVG data:
    - fvg_size_ticks: size of FVG gap in ticks (0.25 = 1 tick for NQ)
    - fvg_type: 'bullish' or 'bearish'
    - is_good: True if doesn't retrace, False if retraces
    """
    target_time = curr_time_str.replace(':', '')  # e.g., '0830'
    prev_time = prev_time_str.replace(':', '')
    next_time = next_time_str.replace(':', '')
    
    # Check if DataFrame is empty
    if len(df) == 0:
        return []
    
    # Find all target time entries
    mask = df['Column2'].astype(str).str.replace(':', '').str.replace('00', '', 1) == target_time
    indices = df[mask].index.tolist()
    
    fvg_data = []
    
    # For each target candle, check for FVG
    for idx in indices:
        # Make sure we have previous, next, and 5 future candles
        if idx < 1 or idx >= len(df) - 6:
            continue
        
        # Get the three candles for FVG detection
        candle_prev = df.loc[idx - 1]
        candle_curr = df.loc[idx]
        candle_next = df.loc[idx + 1]
        
        # Validate adjacent candles
        prev_time_val = str(candle_prev['Column2']).replace(':', '').replace('00', '', 1)
        next_time_val = str(candle_next['Column2']).replace(':', '').replace('00', '', 1)
        
        if prev_time_val != prev_time or next_time_val != next_time:
            continue
        
        # Extract OHLC values (Column3=Open, Column4=High, Column5=Low, Column6=Close)
        high_prev = float(candle_prev['Column4'])
        low_prev = float(candle_prev['Column5'])
        high_next = float(candle_next['Column4'])
        low_next = float(candle_next['Column5'])
        
        # Check for Bullish FVG: low of next candle > high of prev candle
        if low_next > high_prev:
            fvg_size = low_next - high_prev
            fvg_size_ticks = fvg_size / 0.25  # 0.25 = 1 tick for NQ
            
            # Check if price returns to FVG zone in next 5 candles (idx+2 to idx+6)
            price_returns = False
            for future_idx in range(idx + 2, min(idx + 7, len(df))):
                future_candle = df.loc[future_idx]
                future_low = float(future_candle['Column5'])
                
                # If price goes back into FVG zone (below low_next), it's a bad FVG
                if future_low <= high_prev:
                    price_returns = True
                    break
            
            fvg_data.append({
                'year': year,
                'timeframe': timeframe_name,
                'fvg_size_ticks': fvg_size_ticks,
                'fvg_size_points': fvg_size,
                'fvg_type': 'bullish',
                'is_good': not price_returns
            })
        
        # Check for Bearish FVG: high of next candle < low of prev candle
        elif high_next < low_prev:
            fvg_size = low_prev - high_next
            fvg_size_ticks = fvg_size / 0.25  # 0.25 = 1 tick for NQ
            
            # Check if price returns to FVG zone in next 5 candles
            price_returns = False
            for future_idx in range(idx + 2, min(idx + 7, len(df))):
                future_candle = df.loc[future_idx]
                future_high = float(future_candle['Column4'])
                
                # If price goes back into FVG zone (above high_next), it's a bad FVG
                if future_high >= low_prev:
                    price_returns = True
                    break
            
            fvg_data.append({
                'year': year,
                'timeframe': timeframe_name,
                'fvg_size_ticks': fvg_size_ticks,
                'fvg_size_points': fvg_size,
                'fvg_type': 'bearish',
                'is_good': not price_returns
            })
    
    return fvg_data

def main():
    # File directories
    files_1m = {
        2018: '2018 1m.xlsx',
        2019: '2019 1m.xlsx',
        2020: '2020 1m.xlsx',
        2021: '2021 1m.xlsx',
        2022: '2022 1m.xlsx',
        2023: '2023 1m.xlsx',
        2024: '2024 1m.xlsx',
        2025: '2025 1m.csv'
    }
    
    files_5m = {
        2018: '2018 5m.csv',
        2019: '2019 5m.csv',
        2020: '2020 5m.csv',
        2021: '2021 5m.csv',
        2022: '2022 5m.csv',
        2023: '2023 5m.csv',
        2024: '2024 5m.csv',
        2025: '2025 5m.csv'
    }
    
    files_15m = {
        2018: '2018 15m.csv',
        2019: '2019 15m.csv',
        2020: '2020 15m.csv',
        2021: '2021 15m.csv',
        2022: '2022 15m.csv',
        2023: '2023 15m.csv',
        2024: '2024 15m.csv',
        2025: '2025 15m.csv'
    }
    
    all_fvg_data = []
    
    print("Analyzing FVG Size Correlation (2018-2025)...")
    print("=" * 80)
    
    # Analyze 1-minute data
    print("\n1-MINUTE DATA:")
    for year, filename in sorted(files_1m.items()):
        if not os.path.exists(filename):
            print(f"  {year}: File not found - {filename}")
            continue
        
        df = load_data_file(filename)
        year_data = analyze_fvg_size_correlation(df, year, '1m', '08:29', '08:30', '08:31')
        all_fvg_data.extend(year_data)
        print(f"  {year}: {len(year_data)} FVG found")
    
    # Analyze 5-minute data
    print("\n5-MINUTE DATA:")
    for year, filename in sorted(files_5m.items()):
        if not os.path.exists(filename):
            print(f"  {year}: File not found - {filename}")
            continue
        
        df = load_data_file(filename)
        year_data = analyze_fvg_size_correlation(df, year, '5m', '08:25', '08:30', '08:35')
        all_fvg_data.extend(year_data)
        print(f"  {year}: {len(year_data)} FVG found")
    
    # Analyze 15-minute data
    print("\n15-MINUTE DATA:")
    for year, filename in sorted(files_15m.items()):
        if not os.path.exists(filename):
            print(f"  {year}: File not found - {filename}")
            continue
        
        df = load_data_file(filename)
        year_data = analyze_fvg_size_correlation(df, year, '15m', '08:15', '08:30', '08:45')
        all_fvg_data.extend(year_data)
        print(f"  {year}: {len(year_data)} FVG found")
    
    # Create DataFrame for analysis
    df_analysis = pd.DataFrame(all_fvg_data)
    
    if len(df_analysis) == 0:
        print("\nNo FVG data found!")
        return
    
    print(f"\n\nTOTAL FVG ANALYZED: {len(df_analysis)}")
    print("=" * 80)
    
    # Analyze by timeframe
    for timeframe in ['1m', '5m', '15m']:
        tf_data = df_analysis[df_analysis['timeframe'] == timeframe]
        if len(tf_data) == 0:
            continue
        
        print(f"\n{timeframe.upper()} TIMEFRAME ANALYSIS:")
        print("-" * 80)
        
        # Create size bins
        bins = [0, 4, 8, 12, 16, 20, 30, 50, 100, float('inf')]
        labels = ['0-4', '4-8', '8-12', '12-16', '16-20', '20-30', '30-50', '50-100', '100+']
        
        tf_data['size_bin'] = pd.cut(tf_data['fvg_size_ticks'], bins=bins, labels=labels, right=False)
        
        print("\nOverall Statistics:")
        print(f"  Total FVG: {len(tf_data)}")
        print(f"  Good FVG: {tf_data['is_good'].sum()} ({tf_data['is_good'].mean()*100:.2f}%)")
        print(f"  Bad FVG: {(~tf_data['is_good']).sum()} ({(~tf_data['is_good']).mean()*100:.2f}%)")
        print(f"  Average FVG Size: {tf_data['fvg_size_ticks'].mean():.2f} ticks ({tf_data['fvg_size_points'].mean():.2f} points)")
        print(f"  Median FVG Size: {tf_data['fvg_size_ticks'].median():.2f} ticks ({tf_data['fvg_size_points'].median():.2f} points)")
        
        # Analyze by size bins
        print("\nGood FVG % by Size Bin:")
        print(f"  {'Size (ticks)':<15} {'Count':<10} {'Good %':<15} {'Avg Size':<15}")
        print("  " + "-" * 60)
        
        for bin_label in labels:
            bin_data = tf_data[tf_data['size_bin'] == bin_label]
            if len(bin_data) > 0:
                good_pct = bin_data['is_good'].mean() * 100
                avg_size = bin_data['fvg_size_ticks'].mean()
                print(f"  {bin_label:<15} {len(bin_data):<10} {good_pct:<14.2f}% {avg_size:<14.2f}")
        
        # Analyze by type
        print("\nBy FVG Type:")
        for fvg_type in ['bullish', 'bearish']:
            type_data = tf_data[tf_data['fvg_type'] == fvg_type]
            if len(type_data) > 0:
                print(f"\n  {fvg_type.upper()}:")
                print(f"    Count: {len(type_data)}")
                print(f"    Good %: {type_data['is_good'].mean()*100:.2f}%")
                print(f"    Avg Size: {type_data['fvg_size_ticks'].mean():.2f} ticks")
                print(f"    Median Size: {type_data['fvg_size_ticks'].median():.2f} ticks")
                
                # Good vs Bad size comparison
                good_data = type_data[type_data['is_good']]
                bad_data = type_data[~type_data['is_good']]
                
                if len(good_data) > 0:
                    print(f"    Good FVG Avg Size: {good_data['fvg_size_ticks'].mean():.2f} ticks")
                if len(bad_data) > 0:
                    print(f"    Bad FVG Avg Size: {bad_data['fvg_size_ticks'].mean():.2f} ticks")
                
                if len(good_data) > 0 and len(bad_data) > 0:
                    diff = good_data['fvg_size_ticks'].mean() - bad_data['fvg_size_ticks'].mean()
                    diff_pct = (diff / bad_data['fvg_size_ticks'].mean()) * 100
                    print(f"    Difference: {diff:+.2f} ticks ({diff_pct:+.2f}%)")
    
    # Cross-timeframe comparison
    print("\n" + "=" * 80)
    print("CROSS-TIMEFRAME COMPARISON:")
    print("-" * 80)
    print(f"\n{'Timeframe':<12} {'Avg Size':<15} {'Good %':<12} {'Good Avg Size':<18} {'Bad Avg Size':<18}")
    print("-" * 80)
    
    for timeframe in ['1m', '5m', '15m']:
        tf_data = df_analysis[df_analysis['timeframe'] == timeframe]
        if len(tf_data) > 0:
            avg_size = tf_data['fvg_size_ticks'].mean()
            good_pct = tf_data['is_good'].mean() * 100
            
            good_data = tf_data[tf_data['is_good']]
            bad_data = tf_data[~tf_data['is_good']]
            
            good_avg = good_data['fvg_size_ticks'].mean() if len(good_data) > 0 else 0
            bad_avg = bad_data['fvg_size_ticks'].mean() if len(bad_data) > 0 else 0
            
            print(f"{timeframe:<12} {avg_size:<14.2f}t {good_pct:<11.2f}% {good_avg:<17.2f}t {bad_avg:<17.2f}t")
    
    # Save detailed results to file
    output_file = 'fvg_size_correlation_analysis.txt'
    with open(output_file, 'w') as f:
        f.write("FVG SIZE CORRELATION ANALYSIS (2018-2025)\n")
        f.write("=" * 80 + "\n\n")
        
        for timeframe in ['1m', '5m', '15m']:
            tf_data = df_analysis[df_analysis['timeframe'] == timeframe]
            if len(tf_data) == 0:
                continue
            
            f.write(f"\n{timeframe.upper()} TIMEFRAME:\n")
            f.write("-" * 80 + "\n")
            
            tf_data['size_bin'] = pd.cut(tf_data['fvg_size_ticks'], 
                                        bins=[0, 4, 8, 12, 16, 20, 30, 50, 100, float('inf')],
                                        labels=['0-4', '4-8', '8-12', '12-16', '16-20', '20-30', '30-50', '50-100', '100+'],
                                        right=False)
            
            for bin_label in ['0-4', '4-8', '8-12', '12-16', '16-20', '20-30', '30-50', '50-100', '100+']:
                bin_data = tf_data[tf_data['size_bin'] == bin_label]
                if len(bin_data) > 0:
                    f.write(f"\nSize Bin: {bin_label} ticks\n")
                    f.write(f"  Count: {len(bin_data)}\n")
                    f.write(f"  Good FVG: {bin_data['is_good'].sum()} ({bin_data['is_good'].mean()*100:.2f}%)\n")
                    f.write(f"  Bad FVG: {(~bin_data['is_good']).sum()} ({(~bin_data['is_good']).mean()*100:.2f}%)\n")
                    f.write(f"  Avg Size: {bin_data['fvg_size_ticks'].mean():.2f} ticks\n")
                    
                    # By type
                    for fvg_type in ['bullish', 'bearish']:
                        type_bin_data = bin_data[bin_data['fvg_type'] == fvg_type]
                        if len(type_bin_data) > 0:
                            f.write(f"    {fvg_type.capitalize()}: {len(type_bin_data)} ({type_bin_data['is_good'].mean()*100:.2f}% good)\n")
    
    print(f"\n\nDetailed results saved to: {output_file}")
    print("=" * 80)

if __name__ == "__main__":
    main()

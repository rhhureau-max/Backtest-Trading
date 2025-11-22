#!/usr/bin/env python3
"""
Analyze Fair Value Gap (FVG) occurrences at 8:30 AM candle
Analyzes 15-minute trading data files from 2018 onwards

FVG Definition:
- Bullish FVG: Low of candle 3 (8:45) > High of candle 1 (8:15)
- Bearish FVG: High of candle 3 (8:45) < Low of candle 1 (8:15)
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

def analyze_fvg_at_830(df, year):
    """
    Analyze FVG occurrences at 8:30 AM for a given year (15-minute candles)
    
    Returns dict with:
    - total_days: number of trading days with 8:30 candle
    - bullish_fvg: count of bullish FVG
    - bearish_fvg: count of bearish FVG
    - no_fvg: count of days without FVG
    """
    # Find all 8:30 AM entries
    target_time = time(8, 30)
    
    # Check if DataFrame is empty
    if len(df) == 0:
        return {
            'year': year,
            'total_days': 0,
            'bullish_fvg': 0,
            'bearish_fvg': 0,
            'no_fvg': 0,
            'total_fvg': 0,
            'fvg_ratio': 0
        }
    
    # Handle both time objects and string formats
    if df['Column2'].dtype == 'object':
        # Could be time objects or strings
        if isinstance(df['Column2'].iloc[0], time):
            mask = df['Column2'] == target_time
        else:
            # String format
            mask = df['Column2'].isin(['08:30:00', '8:30:00', '08:30', '8:30'])
    else:
        mask = df['Column2'] == target_time
    
    indices_830 = df[mask].index.tolist()
    
    total_days = len(indices_830)
    bullish_fvg = 0
    bearish_fvg = 0
    no_fvg = 0
    
    # For each 8:30 candle, check for FVG with 8:15 and 8:45 candles
    for idx in indices_830:
        # Make sure we have previous and next candles
        if idx < 1 or idx >= len(df) - 1:
            continue
        
        # Get the three candles
        candle_815 = df.loc[idx - 1]  # Previous (should be 8:15)
        candle_830 = df.loc[idx]      # Current (8:30)
        candle_845 = df.loc[idx + 1]  # Next (should be 8:45)
        
        # Validate that adjacent candles are actually 8:15 and 8:45
        # This handles potential gaps in time-series data
        expected_prev_time = time(8, 15)
        expected_next_time = time(8, 45)
        
        # Check previous candle time
        prev_time = candle_815['Column2']
        if isinstance(prev_time, str):
            if prev_time not in ['08:15:00', '8:15:00', '08:15', '8:15']:
                continue
        elif prev_time != expected_prev_time:
            continue
        
        # Check next candle time
        next_time = candle_845['Column2']
        if isinstance(next_time, str):
            if next_time not in ['08:45:00', '8:45:00', '08:45', '8:45']:
                continue
        elif next_time != expected_next_time:
            continue
        
        # Extract OHLC values (Column3=Open, Column4=High, Column5=Low, Column6=Close)
        high_815 = float(candle_815['Column4'])
        low_815 = float(candle_815['Column5'])
        
        high_845 = float(candle_845['Column4'])
        low_845 = float(candle_845['Column5'])
        
        # Check for FVG
        # Bullish FVG: Low of candle 3 (8:45) > High of candle 1 (8:15)
        if low_845 > high_815:
            bullish_fvg += 1
        # Bearish FVG: High of candle 3 (8:45) < Low of candle 1 (8:15)
        elif high_845 < low_815:
            bearish_fvg += 1
        else:
            no_fvg += 1
    
    return {
        'year': year,
        'total_days': total_days,
        'bullish_fvg': bullish_fvg,
        'bearish_fvg': bearish_fvg,
        'no_fvg': no_fvg,
        'total_fvg': bullish_fvg + bearish_fvg,
        'fvg_ratio': ((bullish_fvg + bearish_fvg) / total_days * 100) if total_days > 0 else 0
    }

def main():
    """Main analysis function"""
    print("=" * 80)
    print("FVG ANALYSIS AT 8:30 AM CANDLE - 15-MINUTE DATA (2018-2025)")
    print("=" * 80)
    print()
    print("Fair Value Gap (FVG) Definition:")
    print("  - Bullish FVG: Low of 8:45 candle > High of 8:15 candle")
    print("  - Bearish FVG: High of 8:45 candle < Low of 8:15 candle")
    print()
    print("=" * 80)
    print()
    
    # Years to analyze (starting from 2018)
    years = [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]
    results = []
    
    # Analyze each year
    for year in years:
        # Try CSV first (15m data is in CSV format)
        csv_file = f'{year} 15m.csv'
        
        if not os.path.exists(csv_file):
            print(f"⚠️  No data file found for {year}")
            continue
        
        print(f"Analyzing {csv_file}...")
        try:
            df = load_data_file(csv_file)
            result = analyze_fvg_at_830(df, year)
            results.append(result)
            
            print(f"✓ {year}:")
            print(f"  Total days analyzed: {result['total_days']}")
            print(f"  Bullish FVG: {result['bullish_fvg']}")
            print(f"  Bearish FVG: {result['bearish_fvg']}")
            print(f"  No FVG: {result['no_fvg']}")
            print(f"  FVG Ratio: {result['fvg_ratio']:.2f}%")
            print()
        except Exception as e:
            print(f"✗ Error processing {year}: {e}")
            print()
    
    # Calculate overall statistics
    if results:
        print("=" * 80)
        print("SUMMARY - FVG AT 8:30 AM CANDLE (15-MINUTE DATA)")
        print("=" * 80)
        print()
        print(f"{'Year':<8} {'Days':<8} {'Bullish':<10} {'Bearish':<10} {'No FVG':<10} {'Total FVG':<12} {'FVG %':<10}")
        print("-" * 80)
        
        total_days_all = 0
        total_bullish_all = 0
        total_bearish_all = 0
        total_no_fvg_all = 0
        
        for result in results:
            print(f"{result['year']:<8} {result['total_days']:<8} "
                  f"{result['bullish_fvg']:<10} {result['bearish_fvg']:<10} "
                  f"{result['no_fvg']:<10} {result['total_fvg']:<12} "
                  f"{result['fvg_ratio']:>7.2f}%")
            
            total_days_all += result['total_days']
            total_bullish_all += result['bullish_fvg']
            total_bearish_all += result['bearish_fvg']
            total_no_fvg_all += result['no_fvg']
        
        total_fvg_all = total_bullish_all + total_bearish_all
        overall_fvg_ratio = (total_fvg_all / total_days_all * 100) if total_days_all > 0 else 0
        
        print("-" * 80)
        print(f"{'TOTAL':<8} {total_days_all:<8} "
              f"{total_bullish_all:<10} {total_bearish_all:<10} "
              f"{total_no_fvg_all:<10} {total_fvg_all:<12} "
              f"{overall_fvg_ratio:>7.2f}%")
        print()
        
        # Additional statistics
        print("OVERALL STATISTICS (2018-2025):")
        print(f"  Total trading days analyzed: {total_days_all}")
        print(f"  Total FVG occurrences: {total_fvg_all} ({overall_fvg_ratio:.2f}%)")
        print(f"  Bullish FVG: {total_bullish_all} ({total_bullish_all/total_days_all*100:.2f}%)")
        print(f"  Bearish FVG: {total_bearish_all} ({total_bearish_all/total_days_all*100:.2f}%)")
        print(f"  No FVG: {total_no_fvg_all} ({total_no_fvg_all/total_days_all*100:.2f}%)")
        print()
        
        if total_fvg_all > 0:
            bullish_of_total_fvg = (total_bullish_all / total_fvg_all * 100)
            bearish_of_total_fvg = (total_bearish_all / total_fvg_all * 100)
            print("FVG DISTRIBUTION:")
            print(f"  Bullish FVG: {bullish_of_total_fvg:.2f}% of all FVG")
            print(f"  Bearish FVG: {bearish_of_total_fvg:.2f}% of all FVG")
        
        print()
        print("=" * 80)
        
        # Save results to a file
        with open('fvg_analysis_15m.txt', 'w') as f:
            f.write("=" * 80 + "\n")
            f.write("FVG ANALYSIS AT 8:30 AM CANDLE - 15-MINUTE DATA (2018-2025)\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("Fair Value Gap (FVG) Definition:\n")
            f.write("  - Bullish FVG: Low of 8:45 candle > High of 8:15 candle\n")
            f.write("  - Bearish FVG: High of 8:45 candle < Low of 8:15 candle\n\n")
            
            f.write("SUMMARY - FVG AT 8:30 AM CANDLE (15-MINUTE DATA)\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"{'Year':<8} {'Days':<8} {'Bullish':<10} {'Bearish':<10} {'No FVG':<10} {'Total FVG':<12} {'FVG %':<10}\n")
            f.write("-" * 80 + "\n")
            
            for result in results:
                f.write(f"{result['year']:<8} {result['total_days']:<8} "
                       f"{result['bullish_fvg']:<10} {result['bearish_fvg']:<10} "
                       f"{result['no_fvg']:<10} {result['total_fvg']:<12} "
                       f"{result['fvg_ratio']:>7.2f}%\n")
            
            f.write("-" * 80 + "\n")
            f.write(f"{'TOTAL':<8} {total_days_all:<8} "
                   f"{total_bullish_all:<10} {total_bearish_all:<10} "
                   f"{total_no_fvg_all:<10} {total_fvg_all:<12} "
                   f"{overall_fvg_ratio:>7.2f}%\n\n")
            
            f.write("OVERALL STATISTICS (2018-2025):\n")
            f.write(f"  Total trading days analyzed: {total_days_all}\n")
            f.write(f"  Total FVG occurrences: {total_fvg_all} ({overall_fvg_ratio:.2f}%)\n")
            f.write(f"  Bullish FVG: {total_bullish_all} ({total_bullish_all/total_days_all*100:.2f}%)\n")
            f.write(f"  Bearish FVG: {total_bearish_all} ({total_bearish_all/total_days_all*100:.2f}%)\n")
            f.write(f"  No FVG: {total_no_fvg_all} ({total_no_fvg_all/total_days_all*100:.2f}%)\n\n")
            
            if total_fvg_all > 0:
                f.write("FVG DISTRIBUTION:\n")
                f.write(f"  Bullish FVG: {bullish_of_total_fvg:.2f}% of all FVG\n")
                f.write(f"  Bearish FVG: {bearish_of_total_fvg:.2f}% of all FVG\n")
            
            f.write("\n" + "=" * 80 + "\n")
        
        print(f"Results saved to 'fvg_analysis_15m.txt'")
    else:
        print("No data files could be processed.")

if __name__ == '__main__':
    main()

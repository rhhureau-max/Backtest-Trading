#!/usr/bin/env python3
"""
Analyze maximum price excursion for Good FVG
Calculates the average maximum distance (in ticks) from the close of the third candle (8:31)
for Good FVG across different time periods

For Nasdaq: 1 tick = 0.25 points
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

def analyze_fvg_max_excursion(df, year, timeframe='1m', num_candles=5):
    """
    Analyze maximum price excursion for good FVG
    
    Args:
        df: DataFrame with OHLCV data
        year: Year being analyzed
        timeframe: '1m', '5m', or '15m'
        num_candles: Number of candles to check after FVG formation
    
    Returns:
        dict with excursion statistics for good FVG
    """
    # Define target time based on timeframe
    if timeframe == '1m':
        target_time = time(8, 30)
        prev_time_str = ['08:29:00', '8:29:00', '08:29', '8:29']
        next_time_str = ['08:31:00', '8:31:00', '08:31', '8:31']
    elif timeframe == '5m':
        target_time = time(8, 30)
        prev_time_str = ['08:25:00', '8:25:00', '08:25', '8:25']
        next_time_str = ['08:35:00', '8:35:00', '08:35', '8:35']
    elif timeframe == '15m':
        target_time = time(8, 30)
        prev_time_str = ['08:15:00', '8:15:00', '08:15', '8:15']
        next_time_str = ['08:45:00', '8:45:00', '08:45', '8:45']
    else:
        raise ValueError(f"Unsupported timeframe: {timeframe}")
    
    if len(df) == 0:
        return {
            'year': year,
            'timeframe': timeframe,
            'good_bullish_count': 0,
            'good_bearish_count': 0,
            'bullish_avg_max_excursion_ticks': 0,
            'bearish_avg_max_excursion_ticks': 0,
            'bullish_excursions': [],
            'bearish_excursions': []
        }
    
    # Find all target time entries
    if df['Column2'].dtype == 'object':
        if isinstance(df['Column2'].iloc[0], time):
            mask = df['Column2'] == target_time
        else:
            mask = df['Column2'].isin(['08:30:00', '8:30:00', '08:30', '8:30'])
    else:
        mask = df['Column2'] == target_time
    
    indices_target = df[mask].index.tolist()
    
    bullish_excursions = []
    bearish_excursions = []
    
    # For each target candle, check for FVG and calculate max excursion for good FVG
    for idx in indices_target:
        # Make sure we have previous, next, and future candles
        if idx < 1 or idx >= len(df) - (num_candles + 1):
            continue
        
        # Get the three candles for FVG detection
        candle_prev = df.loc[idx - 1]
        candle_mid = df.loc[idx]
        candle_next = df.loc[idx + 1]
        
        # Validate adjacent candles
        prev_time = candle_prev['Column2']
        if isinstance(prev_time, str):
            if prev_time not in prev_time_str:
                continue
        
        next_time = candle_next['Column2']
        if isinstance(next_time, str):
            if next_time not in next_time_str:
                continue
        
        # Extract OHLC values
        high_prev = float(candle_prev['Column4'])
        low_prev = float(candle_prev['Column5'])
        high_next = float(candle_next['Column4'])
        low_next = float(candle_next['Column5'])
        close_next = float(candle_next['Column6'])  # Close of third candle
        
        # Check for FVG
        is_bullish_fvg = low_next > high_prev
        is_bearish_fvg = high_next < low_prev
        
        if not is_bullish_fvg and not is_bearish_fvg:
            continue
        
        # Get next candles AFTER the third candle closes
        next_candles = df.loc[idx+2:idx+1+num_candles]
        
        if len(next_candles) < num_candles:
            continue
        
        if is_bullish_fvg:
            # Bullish FVG zone: between high_prev and low_next
            fvg_low = high_prev
            fvg_high = low_next
            
            # Check if price returns to FVG zone (bad FVG)
            price_returned = False
            for i in range(len(next_candles)):
                candle_low = float(next_candles.iloc[i]['Column5'])
                candle_high = float(next_candles.iloc[i]['Column4'])
                
                if candle_low <= fvg_high and candle_high >= fvg_low:
                    price_returned = True
                    break
            
            # Only analyze good FVG (where price doesn't return)
            if not price_returned:
                # Calculate maximum excursion from close_next
                max_high = close_next
                for i in range(len(next_candles)):
                    candle_high = float(next_candles.iloc[i]['Column4'])
                    if candle_high > max_high:
                        max_high = candle_high
                
                # Calculate excursion in ticks (1 tick = 0.25 points for Nasdaq)
                excursion_points = max_high - close_next
                excursion_ticks = excursion_points / 0.25
                bullish_excursions.append(excursion_ticks)
        
        elif is_bearish_fvg:
            # Bearish FVG zone: between low_prev and high_next
            fvg_low = high_next
            fvg_high = low_prev
            
            # Check if price returns to FVG zone (bad FVG)
            price_returned = False
            for i in range(len(next_candles)):
                candle_low = float(next_candles.iloc[i]['Column5'])
                candle_high = float(next_candles.iloc[i]['Column4'])
                
                if candle_low <= fvg_high and candle_high >= fvg_low:
                    price_returned = True
                    break
            
            # Only analyze good FVG (where price doesn't return)
            if not price_returned:
                # Calculate maximum excursion from close_next (down move)
                max_low = close_next
                for i in range(len(next_candles)):
                    candle_low = float(next_candles.iloc[i]['Column5'])
                    if candle_low < max_low:
                        max_low = candle_low
                
                # Calculate excursion in ticks (1 tick = 0.25 points for Nasdaq)
                excursion_points = close_next - max_low
                excursion_ticks = excursion_points / 0.25
                bearish_excursions.append(excursion_ticks)
    
    # Calculate averages
    bullish_avg = sum(bullish_excursions) / len(bullish_excursions) if bullish_excursions else 0
    bearish_avg = sum(bearish_excursions) / len(bearish_excursions) if bearish_excursions else 0
    
    return {
        'year': year,
        'timeframe': timeframe,
        'good_bullish_count': len(bullish_excursions),
        'good_bearish_count': len(bearish_excursions),
        'bullish_avg_max_excursion_ticks': bullish_avg,
        'bearish_avg_max_excursion_ticks': bearish_avg,
        'bullish_excursions': bullish_excursions,
        'bearish_excursions': bearish_excursions
    }

def main():
    print("Analyzing Maximum Price Excursion for Good FVG (2018-2025)")
    print("=" * 80)
    
    # Timeframes to analyze
    timeframes = {
        '1m': ['1m.xlsx', '1m.csv'],
        '5m': ['5m.csv'],
        '15m': ['15m.csv']
    }
    
    years = range(2018, 2026)
    
    results_by_timeframe = {}
    
    for tf_name, tf_extensions in timeframes.items():
        print(f"\n{'='*80}")
        print(f"Timeframe: {tf_name}")
        print(f"{'='*80}")
        
        results_by_timeframe[tf_name] = []
        
        for year in years:
            # Try different file formats
            df = None
            for ext in tf_extensions:
                filename = f"{year} {ext}"
                if os.path.exists(filename):
                    try:
                        df = load_data_file(filename)
                        print(f"\nLoaded {filename}")
                        break
                    except Exception as e:
                        print(f"Error loading {filename}: {e}")
                        continue
            
            if df is None:
                print(f"No data file found for {year} {tf_name}")
                continue
            
            # Analyze for 5 candles window
            result = analyze_fvg_max_excursion(df, year, tf_name, num_candles=5)
            results_by_timeframe[tf_name].append(result)
            
            print(f"\nYear {year}:")
            print(f"  Good Bullish FVG: {result['good_bullish_count']}")
            print(f"  Avg Max Excursion (Bullish): {result['bullish_avg_max_excursion_ticks']:.2f} ticks")
            print(f"  Good Bearish FVG: {result['good_bearish_count']}")
            print(f"  Avg Max Excursion (Bearish): {result['bearish_avg_max_excursion_ticks']:.2f} ticks")
    
    # Generate summary report
    print("\n\n" + "="*80)
    print("SUMMARY REPORT: Average Maximum Excursion for Good FVG by Period")
    print("="*80)
    
    for tf_name in timeframes.keys():
        results = results_by_timeframe[tf_name]
        if not results:
            continue
        
        print(f"\n{tf_name.upper()} Timeframe:")
        print("-" * 80)
        
        # Overall statistics
        all_bullish_excursions = []
        all_bearish_excursions = []
        for r in results:
            all_bullish_excursions.extend(r['bullish_excursions'])
            all_bearish_excursions.extend(r['bearish_excursions'])
        
        overall_bullish_avg = sum(all_bullish_excursions) / len(all_bullish_excursions) if all_bullish_excursions else 0
        overall_bearish_avg = sum(all_bearish_excursions) / len(all_bearish_excursions) if all_bearish_excursions else 0
        
        print(f"\nOverall (2018-2025):")
        print(f"  Total Good Bullish FVG: {len(all_bullish_excursions)}")
        print(f"  Avg Max Excursion (Bullish): {overall_bullish_avg:.2f} ticks ({overall_bullish_avg * 0.25:.2f} points)")
        print(f"  Total Good Bearish FVG: {len(all_bearish_excursions)}")
        print(f"  Avg Max Excursion (Bearish): {overall_bearish_avg:.2f} ticks ({overall_bearish_avg * 0.25:.2f} points)")
        print(f"  Combined Average: {(overall_bullish_avg + overall_bearish_avg) / 2:.2f} ticks ({(overall_bullish_avg + overall_bearish_avg) / 2 * 0.25:.2f} points)")
        
        # Period breakdowns
        periods = {
            'Pre-COVID (2018-2019)': [2018, 2019],
            'COVID Era (2020-2021)': [2020, 2021],
            'Post-COVID (2022-2023)': [2022, 2023],
            'Recent (2024-2025)': [2024, 2025]
        }
        
        print("\n  By Period:")
        for period_name, period_years in periods.items():
            period_bullish = []
            period_bearish = []
            for r in results:
                if r['year'] in period_years:
                    period_bullish.extend(r['bullish_excursions'])
                    period_bearish.extend(r['bearish_excursions'])
            
            if period_bullish or period_bearish:
                period_bullish_avg = sum(period_bullish) / len(period_bullish) if period_bullish else 0
                period_bearish_avg = sum(period_bearish) / len(period_bearish) if period_bearish else 0
                period_combined_avg = (period_bullish_avg + period_bearish_avg) / 2 if (period_bullish or period_bearish) else 0
                
                print(f"\n    {period_name}:")
                print(f"      Good Bullish: {len(period_bullish)}, Avg: {period_bullish_avg:.2f} ticks ({period_bullish_avg * 0.25:.2f} points)")
                print(f"      Good Bearish: {len(period_bearish)}, Avg: {period_bearish_avg:.2f} ticks ({period_bearish_avg * 0.25:.2f} points)")
                print(f"      Combined Avg: {period_combined_avg:.2f} ticks ({period_combined_avg * 0.25:.2f} points)")
    
    # Save detailed results to file
    output_file = "fvg_max_excursion_analysis.txt"
    with open(output_file, 'w') as f:
        f.write("Maximum Price Excursion Analysis for Good FVG\n")
        f.write("=" * 80 + "\n")
        f.write("Measuring average maximum distance (in ticks) from close of third candle\n")
        f.write("for Good FVG across different time periods (2018-2025)\n")
        f.write("Nasdaq: 1 tick = 0.25 points\n")
        f.write("=" * 80 + "\n\n")
        
        for tf_name in timeframes.keys():
            results = results_by_timeframe[tf_name]
            if not results:
                continue
            
            f.write(f"\n{tf_name.upper()} TIMEFRAME\n")
            f.write("-" * 80 + "\n")
            
            # Year by year
            f.write("\nYear-by-Year Breakdown:\n")
            f.write(f"{'Year':<8} {'Good Bull':<12} {'Avg Ticks':<15} {'Good Bear':<12} {'Avg Ticks':<15}\n")
            f.write("-" * 80 + "\n")
            
            for r in results:
                f.write(f"{r['year']:<8} "
                       f"{r['good_bullish_count']:<12} "
                       f"{r['bullish_avg_max_excursion_ticks']:.2f} ticks{'':<6} "
                       f"{r['good_bearish_count']:<12} "
                       f"{r['bearish_avg_max_excursion_ticks']:.2f} ticks\n")
            
            # Overall
            all_bullish_excursions = []
            all_bearish_excursions = []
            for r in results:
                all_bullish_excursions.extend(r['bullish_excursions'])
                all_bearish_excursions.extend(r['bearish_excursions'])
            
            overall_bullish_avg = sum(all_bullish_excursions) / len(all_bullish_excursions) if all_bullish_excursions else 0
            overall_bearish_avg = sum(all_bearish_excursions) / len(all_bearish_excursions) if all_bearish_excursions else 0
            
            f.write("\n" + "-" * 80 + "\n")
            f.write(f"OVERALL (2018-2025):\n")
            f.write(f"  Bullish: {len(all_bullish_excursions)} good FVG, Avg: {overall_bullish_avg:.2f} ticks ({overall_bullish_avg * 0.25:.2f} points)\n")
            f.write(f"  Bearish: {len(all_bearish_excursions)} good FVG, Avg: {overall_bearish_avg:.2f} ticks ({overall_bearish_avg * 0.25:.2f} points)\n")
            f.write(f"  Combined: {(overall_bullish_avg + overall_bearish_avg) / 2:.2f} ticks ({(overall_bullish_avg + overall_bearish_avg) / 2 * 0.25:.2f} points)\n")
            
            # Periods
            periods = {
                'Pre-COVID (2018-2019)': [2018, 2019],
                'COVID Era (2020-2021)': [2020, 2021],
                'Post-COVID (2022-2023)': [2022, 2023],
                'Recent (2024-2025)': [2024, 2025]
            }
            
            f.write("\nBy Period:\n")
            for period_name, period_years in periods.items():
                period_bullish = []
                period_bearish = []
                for r in results:
                    if r['year'] in period_years:
                        period_bullish.extend(r['bullish_excursions'])
                        period_bearish.extend(r['bearish_excursions'])
                
                if period_bullish or period_bearish:
                    period_bullish_avg = sum(period_bullish) / len(period_bullish) if period_bullish else 0
                    period_bearish_avg = sum(period_bearish) / len(period_bearish) if period_bearish else 0
                    period_combined_avg = (period_bullish_avg + period_bearish_avg) / 2
                    
                    f.write(f"\n  {period_name}:\n")
                    f.write(f"    Bullish: {len(period_bullish)} good FVG, Avg: {period_bullish_avg:.2f} ticks ({period_bullish_avg * 0.25:.2f} points)\n")
                    f.write(f"    Bearish: {len(period_bearish)} good FVG, Avg: {period_bearish_avg:.2f} ticks ({period_bearish_avg * 0.25:.2f} points)\n")
                    f.write(f"    Combined: {period_combined_avg:.2f} ticks ({period_combined_avg * 0.25:.2f} points)\n")
            
            f.write("\n" + "=" * 80 + "\n")
    
    print(f"\n\nDetailed results saved to: {output_file}")
    print("\nAnalysis complete!")

if __name__ == "__main__":
    main()

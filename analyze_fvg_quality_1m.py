#!/usr/bin/env python3
"""
Analyze Fair Value Gap (FVG) quality at 8:30 AM candle
Analyzes 1-minute trading data files from 2018 onwards

FVG Quality Definition:
- Good FVG: Price doesn't return to FVG zone after 5 candles (by 8:36)
- Bad FVG: Price returns to FVG zone after 5 candles (by 8:36)
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

def analyze_fvg_quality_at_830(df, year):
    """
    Analyze FVG quality at 8:30 AM for a given year (1-minute candles)
    
    Returns dict with:
    - total_fvg: total FVG occurrences
    - good_bullish_fvg: bullish FVG where price doesn't return
    - bad_bullish_fvg: bullish FVG where price returns
    - good_bearish_fvg: bearish FVG where price doesn't return
    - bad_bearish_fvg: bearish FVG where price returns
    """
    # Find all 8:30 AM entries
    target_time = time(8, 30)
    
    # Check if DataFrame is empty
    if len(df) == 0:
        return {
            'year': year,
            'total_fvg': 0,
            'good_bullish': 0,
            'bad_bullish': 0,
            'good_bearish': 0,
            'bad_bearish': 0
        }
    
    # Handle both time objects and string formats
    if df['Column2'].dtype == 'object':
        if isinstance(df['Column2'].iloc[0], time):
            mask = df['Column2'] == target_time
        else:
            mask = df['Column2'].isin(['08:30:00', '8:30:00', '08:30', '8:30'])
    else:
        mask = df['Column2'] == target_time
    
    indices_830 = df[mask].index.tolist()
    
    good_bullish = 0
    bad_bullish = 0
    good_bearish = 0
    bad_bearish = 0
    
    # For each 8:30 candle, check for FVG and quality
    for idx in indices_830:
        # Make sure we have previous, next, and 5 future candles
        if idx < 1 or idx >= len(df) - 6:
            continue
        
        # Get the three candles for FVG detection
        candle_829 = df.loc[idx - 1]  # Previous (should be 8:29)
        candle_830 = df.loc[idx]      # Current (8:30)
        candle_831 = df.loc[idx + 1]  # Next (should be 8:31)
        
        # Validate adjacent candles
        expected_prev_time = time(8, 29)
        expected_next_time = time(8, 31)
        
        prev_time = candle_829['Column2']
        if isinstance(prev_time, str):
            if prev_time not in ['08:29:00', '8:29:00', '08:29', '8:29']:
                continue
        elif prev_time != expected_prev_time:
            continue
        
        next_time = candle_831['Column2']
        if isinstance(next_time, str):
            if next_time not in ['08:31:00', '8:31:00', '08:31', '8:31']:
                continue
        elif next_time != expected_next_time:
            continue
        
        # Extract OHLC values (Column3=Open, Column4=High, Column5=Low, Column6=Close)
        high_829 = float(candle_829['Column4'])
        low_829 = float(candle_829['Column5'])
        high_831 = float(candle_831['Column4'])
        low_831 = float(candle_831['Column5'])
        
        # Check for FVG
        is_bullish_fvg = low_831 > high_829
        is_bearish_fvg = high_831 < low_829
        
        if not is_bullish_fvg and not is_bearish_fvg:
            continue
        
        # Get next 5 candles AFTER the third candle closes (8:32 to 8:36)
        next_5_candles = df.loc[idx+2:idx+6]
        
        if len(next_5_candles) < 5:
            continue
        
        if is_bullish_fvg:
            # Bullish FVG zone: between high_829 and low_831
            fvg_low = high_829
            fvg_high = low_831
            
            # Check if price returns to FVG zone in next 5 candles
            # Price returns if any candle's low touches or enters the FVG zone
            price_returned = False
            for i in range(len(next_5_candles)):
                candle_low = float(next_5_candles.iloc[i]['Column5'])
                candle_high = float(next_5_candles.iloc[i]['Column4'])
                
                # Check if candle overlaps with FVG zone
                if candle_low <= fvg_high and candle_high >= fvg_low:
                    price_returned = True
                    break
            
            if price_returned:
                bad_bullish += 1
            else:
                good_bullish += 1
        
        elif is_bearish_fvg:
            # Bearish FVG zone: between low_829 and high_831
            fvg_low = high_831
            fvg_high = low_829
            
            # Check if price returns to FVG zone in next 5 candles
            # Price returns if any candle's high touches or enters the FVG zone
            price_returned = False
            for i in range(len(next_5_candles)):
                candle_low = float(next_5_candles.iloc[i]['Column5'])
                candle_high = float(next_5_candles.iloc[i]['Column4'])
                
                # Check if candle overlaps with FVG zone
                if candle_low <= fvg_high and candle_high >= fvg_low:
                    price_returned = True
                    break
            
            if price_returned:
                bad_bearish += 1
            else:
                good_bearish += 1
    
    total_fvg = good_bullish + bad_bullish + good_bearish + bad_bearish
    
    return {
        'year': year,
        'total_fvg': total_fvg,
        'good_bullish': good_bullish,
        'bad_bullish': bad_bullish,
        'good_bearish': good_bearish,
        'bad_bearish': bad_bearish
    }

def main():
    """Main analysis function"""
    print("=" * 80)
    print("FVG QUALITY ANALYSIS AT 8:30 AM - 1-MINUTE DATA (2018-2025)")
    print("=" * 80)
    print()
    print("FVG Quality Definition:")
    print("  - Good FVG: Price doesn't return to FVG zone after 5 candles (by 8:36)")
    print("  - Bad FVG: Price returns to FVG zone after 5 candles (by 8:36)")
    print()
    print("=" * 80)
    print()
    
    # Years to analyze (starting from 2018)
    years = [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]
    results = []
    
    # Analyze each year
    for year in years:
        # Try XLSX first, then CSV
        xlsx_file = f'{year} 1m.xlsx'
        csv_file = f'{year} 1m.csv'
        
        if os.path.exists(xlsx_file):
            filename = xlsx_file
        elif os.path.exists(csv_file):
            filename = csv_file
        else:
            print(f"⚠️  No data file found for {year}")
            continue
        
        print(f"Analyzing {filename}...")
        try:
            df = load_data_file(filename)
            result = analyze_fvg_quality_at_830(df, year)
            results.append(result)
            
            total_good = result['good_bullish'] + result['good_bearish']
            total_bad = result['bad_bullish'] + result['bad_bearish']
            good_ratio = (total_good / result['total_fvg'] * 100) if result['total_fvg'] > 0 else 0
            
            print(f"✓ {year}:")
            print(f"  Total FVG: {result['total_fvg']}")
            print(f"  Good Bullish: {result['good_bullish']}, Bad Bullish: {result['bad_bullish']}")
            print(f"  Good Bearish: {result['good_bearish']}, Bad Bearish: {result['bad_bearish']}")
            print(f"  Good FVG Ratio: {good_ratio:.2f}%")
            print()
        except Exception as e:
            print(f"✗ Error processing {year}: {e}")
            print()
    
    # Calculate overall statistics
    if results:
        print("=" * 80)
        print("SUMMARY - FVG QUALITY AT 8:30 AM (1-MINUTE DATA)")
        print("=" * 80)
        print()
        print(f"{'Year':<8} {'Total':<8} {'Good Bull':<12} {'Bad Bull':<12} {'Good Bear':<12} {'Bad Bear':<12} {'Good %':<10}")
        print("-" * 80)
        
        total_fvg_all = 0
        total_good_bull_all = 0
        total_bad_bull_all = 0
        total_good_bear_all = 0
        total_bad_bear_all = 0
        
        for result in results:
            total_good = result['good_bullish'] + result['good_bearish']
            good_pct = (total_good / result['total_fvg'] * 100) if result['total_fvg'] > 0 else 0
            
            print(f"{result['year']:<8} {result['total_fvg']:<8} "
                  f"{result['good_bullish']:<12} {result['bad_bullish']:<12} "
                  f"{result['good_bearish']:<12} {result['bad_bearish']:<12} "
                  f"{good_pct:>7.2f}%")
            
            total_fvg_all += result['total_fvg']
            total_good_bull_all += result['good_bullish']
            total_bad_bull_all += result['bad_bullish']
            total_good_bear_all += result['good_bearish']
            total_bad_bear_all += result['bad_bearish']
        
        total_good_all = total_good_bull_all + total_good_bear_all
        total_bad_all = total_bad_bull_all + total_bad_bear_all
        overall_good_pct = (total_good_all / total_fvg_all * 100) if total_fvg_all > 0 else 0
        
        print("-" * 80)
        print(f"{'TOTAL':<8} {total_fvg_all:<8} "
              f"{total_good_bull_all:<12} {total_bad_bull_all:<12} "
              f"{total_good_bear_all:<12} {total_bad_bear_all:<12} "
              f"{overall_good_pct:>7.2f}%")
        print()
        
        # Additional statistics
        print("OVERALL STATISTICS (2018-2025):")
        print(f"  Total FVG analyzed: {total_fvg_all}")
        print(f"  Good FVG: {total_good_all} ({overall_good_pct:.2f}%)")
        print(f"  Bad FVG: {total_bad_all} ({100-overall_good_pct:.2f}%)")
        print()
        print(f"  Good Bullish FVG: {total_good_bull_all} ({total_good_bull_all/total_fvg_all*100:.2f}%)")
        print(f"  Bad Bullish FVG: {total_bad_bull_all} ({total_bad_bull_all/total_fvg_all*100:.2f}%)")
        print(f"  Good Bearish FVG: {total_good_bear_all} ({total_good_bear_all/total_fvg_all*100:.2f}%)")
        print(f"  Bad Bearish FVG: {total_bad_bear_all} ({total_bad_bear_all/total_fvg_all*100:.2f}%)")
        print()
        
        print("=" * 80)
        
        # Save results to a file
        with open('fvg_quality_analysis_1m.txt', 'w') as f:
            f.write("=" * 80 + "\n")
            f.write("FVG QUALITY ANALYSIS AT 8:30 AM - 1-MINUTE DATA (2018-2025)\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("FVG Quality Definition:\n")
            f.write("  - Good FVG: Price doesn't return to FVG zone after 5 candles (by 8:36)\n")
            f.write("  - Bad FVG: Price returns to FVG zone after 5 candles (by 8:36)\n\n")
            
            f.write("SUMMARY - FVG QUALITY AT 8:30 AM (1-MINUTE DATA)\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"{'Year':<8} {'Total':<8} {'Good Bull':<12} {'Bad Bull':<12} {'Good Bear':<12} {'Bad Bear':<12} {'Good %':<10}\n")
            f.write("-" * 80 + "\n")
            
            for result in results:
                total_good = result['good_bullish'] + result['good_bearish']
                good_pct = (total_good / result['total_fvg'] * 100) if result['total_fvg'] > 0 else 0
                
                f.write(f"{result['year']:<8} {result['total_fvg']:<8} "
                       f"{result['good_bullish']:<12} {result['bad_bullish']:<12} "
                       f"{result['good_bearish']:<12} {result['bad_bearish']:<12} "
                       f"{good_pct:>7.2f}%\n")
            
            f.write("-" * 80 + "\n")
            f.write(f"{'TOTAL':<8} {total_fvg_all:<8} "
                   f"{total_good_bull_all:<12} {total_bad_bull_all:<12} "
                   f"{total_good_bear_all:<12} {total_bad_bear_all:<12} "
                   f"{overall_good_pct:>7.2f}%\n\n")
            
            f.write("OVERALL STATISTICS (2018-2025):\n")
            f.write(f"  Total FVG analyzed: {total_fvg_all}\n")
            f.write(f"  Good FVG: {total_good_all} ({overall_good_pct:.2f}%)\n")
            f.write(f"  Bad FVG: {total_bad_all} ({100-overall_good_pct:.2f}%)\n\n")
            f.write(f"  Good Bullish FVG: {total_good_bull_all} ({total_good_bull_all/total_fvg_all*100:.2f}%)\n")
            f.write(f"  Bad Bullish FVG: {total_bad_bull_all} ({total_bad_bull_all/total_fvg_all*100:.2f}%)\n")
            f.write(f"  Good Bearish FVG: {total_good_bear_all} ({total_good_bear_all/total_fvg_all*100:.2f}%)\n")
            f.write(f"  Bad Bearish FVG: {total_bad_bear_all} ({total_bad_bear_all/total_fvg_all*100:.2f}%)\n")
            
            f.write("\n" + "=" * 80 + "\n")
        
        print(f"Results saved to 'fvg_quality_analysis_1m.txt'")
    else:
        print("No data files could be processed.")

if __name__ == '__main__':
    main()

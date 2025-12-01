#!/usr/bin/env python3
"""
Analyze trading data files to count impulsive candles.

An impulsive candle is one where the close breaks above the high 
OR below the low of the last N candles of the range.
"""

import os
import zipfile
import pandas as pd
from datetime import datetime, time
from collections import defaultdict
import argparse


# Default configuration - can be overridden via command line
DEFAULT_DATA_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_YEARS = range(2018, 2026)
TIMEFRAMES = ["1m", "5m", "15m"]
LOOKBACK_PERIODS = [5, 10, 15, 20]
TIME_START = time(2, 0, 0)
TIME_END = time(12, 0, 0)


def load_csv_data(file_path):
    """Load CSV data from a file."""
    df = pd.read_csv(
        file_path,
        sep=';',
        header=0,
        names=['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
    )
    
    # Parse datetime
    df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%d/%m/%Y %H:%M:%S')
    df['TimeOnly'] = pd.to_datetime(df['Time'], format='%H:%M:%S').dt.time
    
    # Convert OHLC to numeric
    for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    return df


def extract_zip(zip_path):
    """Extract zip file and return the path to the extracted CSV."""
    extract_dir = os.path.dirname(zip_path)
    csv_name = os.path.basename(zip_path).replace('.zip', '')
    csv_path = os.path.join(extract_dir, csv_name)
    
    # Only extract if CSV doesn't already exist
    if not os.path.exists(csv_path):
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
    
    return csv_path


def get_file_path(year, timeframe, data_dir):
    """Get the file path for a given year and timeframe."""
    if timeframe == "1m":
        if year == 2025:
            csv_path = os.path.join(data_dir, f"{year} 1m.csv")
            if os.path.exists(csv_path):
                return csv_path
        else:
            # Check for zip file
            zip_path = os.path.join(data_dir, f"{year} 1m.csv.zip")
            if os.path.exists(zip_path):
                return extract_zip(zip_path)
    else:
        csv_path = os.path.join(data_dir, f"{year} {timeframe}.csv")
        if os.path.exists(csv_path):
            return csv_path
    
    return None


def count_impulsive_candles(df, lookback):
    """
    Count impulsive candles in the data.
    
    An impulsive candle is one where:
    - close > max(high of last N candles) [bullish breakout]
    - close < min(low of last N candles) [bearish breakout]
    """
    bullish_count = 0
    bearish_count = 0
    
    # Filter for time range (2:00 to 12:00)
    df_range = df[(df['TimeOnly'] >= TIME_START) & (df['TimeOnly'] <= TIME_END)].copy()
    
    if len(df_range) < lookback + 1:
        return bullish_count, bearish_count
    
    # Group by date to reset lookback window for each day
    for date, day_df in df_range.groupby(df_range['DateTime'].dt.date):
        day_df = day_df.reset_index(drop=True)
        
        if len(day_df) < lookback + 1:
            continue
        
        for i in range(lookback, len(day_df)):
            current_close = day_df.iloc[i]['Close']
            
            # Get the last N candles (excluding current)
            lookback_data = day_df.iloc[i - lookback:i]
            max_high = lookback_data['High'].max()
            min_low = lookback_data['Low'].min()
            
            # Check for bullish breakout
            if current_close > max_high:
                bullish_count += 1
            
            # Check for bearish breakout
            if current_close < min_low:
                bearish_count += 1
    
    return bullish_count, bearish_count


def main(data_dir=None, years=None):
    """Main function to run the analysis."""
    if data_dir is None:
        data_dir = DEFAULT_DATA_DIR
    if years is None:
        years = DEFAULT_YEARS
    
    results = []
    
    print("Starting impulsive candles analysis...")
    print("=" * 60)
    
    for timeframe in TIMEFRAMES:
        print(f"\nProcessing {timeframe} data...")
        
        for lookback in LOOKBACK_PERIODS:
            total_bullish = 0
            total_bearish = 0
            yearly_data = {}
            
            for year in years:
                file_path = get_file_path(year, timeframe, data_dir)
                
                if file_path and os.path.exists(file_path):
                    print(f"  Loading {year} {timeframe}...")
                    try:
                        df = load_csv_data(file_path)
                        bullish, bearish = count_impulsive_candles(df, lookback)
                        total_bullish += bullish
                        total_bearish += bearish
                        yearly_data[year] = (bullish, bearish)
                        print(f"    {year}: Bullish={bullish}, Bearish={bearish}")
                    except Exception as e:
                        print(f"    Error processing {year} {timeframe}: {e}")
                else:
                    print(f"  File not found for {year} {timeframe}")
            
            total = total_bullish + total_bearish
            results.append({
                'Timeframe': timeframe,
                'Lookback': lookback,
                'Bullish_Count': total_bullish,
                'Bearish_Count': total_bearish,
                'Total_Count': total
            })
            
            print(f"  Lookback {lookback}: Total Bullish={total_bullish}, Bearish={total_bearish}, Total={total}")
    
    # Create results DataFrame
    results_df = pd.DataFrame(results)
    
    # Save to CSV
    output_path = os.path.join(data_dir, "impulsive_candles_analysis.csv")
    results_df.to_csv(output_path, index=False)
    print(f"\nResults saved to: {output_path}")
    
    # Also create a detailed text report
    report_path = os.path.join(data_dir, "impulsive_candles_analysis.txt")
    with open(report_path, 'w') as f:
        f.write("=" * 70 + "\n")
        f.write("IMPULSIVE CANDLES ANALYSIS REPORT\n")
        f.write("=" * 70 + "\n\n")
        f.write(f"Time Range: {TIME_START} to {TIME_END}\n")
        f.write(f"Years Analyzed: {list(years)}\n")
        f.write(f"Timeframes: {TIMEFRAMES}\n")
        f.write(f"Lookback Periods: {LOOKBACK_PERIODS}\n\n")
        
        f.write("Definition of Impulsive Candle:\n")
        f.write("- Bullish: Close > max(High of last N candles)\n")
        f.write("- Bearish: Close < min(Low of last N candles)\n\n")
        
        f.write("-" * 70 + "\n")
        f.write("SUMMARY TABLE\n")
        f.write("-" * 70 + "\n")
        f.write(f"{'Timeframe':<12} {'Lookback':<10} {'Bullish':<12} {'Bearish':<12} {'Total':<12}\n")
        f.write("-" * 70 + "\n")
        
        for _, row in results_df.iterrows():
            f.write(f"{row['Timeframe']:<12} {row['Lookback']:<10} {row['Bullish_Count']:<12} {row['Bearish_Count']:<12} {row['Total_Count']:<12}\n")
        
        f.write("-" * 70 + "\n")
    
    print(f"Detailed report saved to: {report_path}")
    
    # Print summary table
    print("\n" + "=" * 70)
    print("SUMMARY TABLE")
    print("=" * 70)
    print(f"{'Timeframe':<12} {'Lookback':<10} {'Bullish':<12} {'Bearish':<12} {'Total':<12}")
    print("-" * 70)
    for _, row in results_df.iterrows():
        print(f"{row['Timeframe']:<12} {row['Lookback']:<10} {row['Bullish_Count']:<12} {row['Bearish_Count']:<12} {row['Total_Count']:<12}")
    print("=" * 70)
    
    return results_df


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze trading data for impulsive candles")
    parser.add_argument("--data-dir", type=str, default=None,
                        help="Directory containing the CSV data files")
    parser.add_argument("--start-year", type=int, default=2018,
                        help="First year to analyze (default: 2018)")
    parser.add_argument("--end-year", type=int, default=2025,
                        help="Last year to analyze (default: 2025)")
    args = parser.parse_args()
    
    years = range(args.start_year, args.end_year + 1)
    main(data_dir=args.data_dir, years=years)

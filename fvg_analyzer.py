#!/usr/bin/env python3
"""
Fair Value Gap (FVG) Analyzer

This script analyzes 15-minute candlestick data from 2018 to 2025 to find
Fair Value Gaps (FVG) between 8:30 and 10:00.

FVG Definitions:
- Bullish FVG: When the high of candle N is lower than the low of candle N+2 (gap up)
- Bearish FVG: When the low of candle N is higher than the high of candle N+2 (gap down)
"""

import os
import pandas as pd
from datetime import datetime, time

# Configuration
DATA_DIR = os.path.dirname(os.path.abspath(__file__))
YEARS = list(range(2018, 2026))
TIME_START = time(8, 30, 0)
TIME_END = time(10, 0, 0)


def load_csv_file(year):
    """Load a 15-minute CSV file for a given year."""
    filepath = os.path.join(DATA_DIR, f"{year} 15m.csv")
    
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return None
    
    df = pd.read_csv(
        filepath, 
        delimiter=';',
        names=['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume'],
        skiprows=1  # Skip header row
    )
    
    # Convert Date and Time columns
    df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%d/%m/%Y %H:%M:%S')
    df['TimeOnly'] = pd.to_datetime(df['Time'], format='%H:%M:%S').dt.time
    
    # Convert price columns to float
    for col in ['Open', 'High', 'Low', 'Close']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    return df


def filter_time_window(df, start_time, end_time):
    """Filter dataframe to only include rows within the time window."""
    mask = (df['TimeOnly'] >= start_time) & (df['TimeOnly'] <= end_time)
    return df[mask].copy()


def find_fvg(df):
    """
    Find Fair Value Gaps in the data.
    
    Bullish FVG: High of candle N < Low of candle N+2 (gap up)
    Bearish FVG: Low of candle N > High of candle N+2 (gap down)
    
    Returns a list of dictionaries containing FVG information.
    """
    fvgs = []
    
    # Group by date to analyze each day separately
    df['DateOnly'] = df['DateTime'].dt.date
    
    for date, day_df in df.groupby('DateOnly'):
        day_df = day_df.sort_values('DateTime').reset_index(drop=True)
        
        # Need at least 3 candles to detect FVG
        if len(day_df) < 3:
            continue
        
        for i in range(len(day_df) - 2):
            candle_n = day_df.iloc[i]
            candle_n2 = day_df.iloc[i + 2]
            
            # Bullish FVG: High of candle N < Low of candle N+2
            if candle_n['High'] < candle_n2['Low']:
                gap_size = round(candle_n2['Low'] - candle_n['High'], 4)
                fvgs.append({
                    'Type': 'Bullish',
                    'Date': date,
                    'Candle_N_Time': candle_n['Time'],
                    'Candle_N2_Time': candle_n2['Time'],
                    'Candle_N_Price': round(candle_n['High'], 4),
                    'Candle_N2_Price': round(candle_n2['Low'], 4),
                    'Gap_Size': gap_size
                })
            
            # Bearish FVG: Low of candle N > High of candle N+2
            if candle_n['Low'] > candle_n2['High']:
                gap_size = round(candle_n['Low'] - candle_n2['High'], 4)
                fvgs.append({
                    'Type': 'Bearish',
                    'Date': date,
                    'Candle_N_Time': candle_n['Time'],
                    'Candle_N2_Time': candle_n2['Time'],
                    'Candle_N_Price': round(candle_n['Low'], 4),
                    'Candle_N2_Price': round(candle_n2['High'], 4),
                    'Gap_Size': gap_size
                })
    
    return fvgs


def main():
    print("=" * 70)
    print("Fair Value Gap (FVG) Analysis")
    print("Time Window: 8:30:00 to 10:00:00")
    print("Years: 2018 to 2025")
    print("=" * 70)
    print()
    
    all_fvgs = []
    yearly_stats = {}
    
    for year in YEARS:
        print(f"Processing {year}...")
        
        # Load data
        df = load_csv_file(year)
        if df is None:
            continue
        
        # Filter to time window
        df_filtered = filter_time_window(df, TIME_START, TIME_END)
        
        # Find FVGs
        fvgs = find_fvg(df_filtered)
        
        # Count by type
        bullish_count = sum(1 for f in fvgs if f['Type'] == 'Bullish')
        bearish_count = sum(1 for f in fvgs if f['Type'] == 'Bearish')
        
        yearly_stats[year] = {
            'Total': len(fvgs),
            'Bullish': bullish_count,
            'Bearish': bearish_count,
            'Total_Candles': len(df_filtered)
        }
        
        all_fvgs.extend(fvgs)
        
        print(f"  Total candles in time window: {len(df_filtered)}")
        print(f"  FVGs found: {len(fvgs)} (Bullish: {bullish_count}, Bearish: {bearish_count})")
    
    print()
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print()
    
    # Print yearly summary table
    print(f"{'Year':<10} {'Total FVGs':<15} {'Bullish':<15} {'Bearish':<15} {'Candles':<10}")
    print("-" * 65)
    
    total_fvgs = 0
    total_bullish = 0
    total_bearish = 0
    total_candles = 0
    
    for year in YEARS:
        if year in yearly_stats:
            stats = yearly_stats[year]
            print(f"{year:<10} {stats['Total']:<15} {stats['Bullish']:<15} {stats['Bearish']:<15} {stats['Total_Candles']:<10}")
            total_fvgs += stats['Total']
            total_bullish += stats['Bullish']
            total_bearish += stats['Bearish']
            total_candles += stats['Total_Candles']
    
    print("-" * 65)
    print(f"{'TOTAL':<10} {total_fvgs:<15} {total_bullish:<15} {total_bearish:<15} {total_candles:<10}")
    print()
    
    # Print some sample FVGs
    print("=" * 70)
    print("SAMPLE FVGs (First 10)")
    print("=" * 70)
    
    for i, fvg in enumerate(all_fvgs[:10]):
        print(f"\n{i+1}. {fvg['Type']} FVG on {fvg['Date']}")
        if fvg['Type'] == 'Bullish':
            print(f"   Candle N ({fvg['Candle_N_Time']}) High: {fvg['Candle_N_Price']:.2f}")
            print(f"   Candle N+2 ({fvg['Candle_N2_Time']}) Low: {fvg['Candle_N2_Price']:.2f}")
        else:
            print(f"   Candle N ({fvg['Candle_N_Time']}) Low: {fvg['Candle_N_Price']:.2f}")
            print(f"   Candle N+2 ({fvg['Candle_N2_Time']}) High: {fvg['Candle_N2_Price']:.2f}")
        print(f"   Gap Size: {fvg['Gap_Size']:.2f}")
    
    print()
    print("=" * 70)
    print("ANALYSIS COMPLETE")
    print(f"Total Fair Value Gaps found: {total_fvgs}")
    print(f"  - Bullish FVGs: {total_bullish}")
    print(f"  - Bearish FVGs: {total_bearish}")
    print("=" * 70)
    
    # Save results to CSV
    if all_fvgs:
        results_df = pd.DataFrame(all_fvgs)
        output_path = os.path.join(DATA_DIR, "fvg_results.csv")
        results_df.to_csv(output_path, index=False)
        print(f"\nResults saved to: {output_path}")
    
    return all_fvgs, yearly_stats


if __name__ == "__main__":
    fvgs, stats = main()

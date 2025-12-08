#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FVG (Fair Value Gap) Tokyo Session Analysis
Analyzes Fair Value Gaps formed during Tokyo session hours (19:00-23:00)
on NQ (Nasdaq Futures) 1H data from 2018 to present.

Author: Quant Data Scientist
Date: 2025-12-08
"""

import pandas as pd
import numpy as np
from datetime import datetime
import glob
import os


def load_1h_data(data_dir='.'):
    """
    Load all 1H CSV files from 2018 to 2025 and combine them.
    
    Args:
        data_dir: Directory containing the CSV files
        
    Returns:
        pandas.DataFrame: Combined dataframe with all 1H data
    """
    print("Loading 1H data files...")
    
    # Find all 1H CSV files
    pattern = os.path.join(data_dir, '*1H.csv')
    files = sorted(glob.glob(pattern))
    
    if not files:
        raise FileNotFoundError(f"No 1H CSV files found in {data_dir}")
    
    print(f"Found {len(files)} files: {[os.path.basename(f) for f in files]}")
    
    dfs = []
    for file in files:
        print(f"  Loading {os.path.basename(file)}...")
        # Based on the data structure: semicolon delimiter, DD/MM/YYYY format
        df = pd.read_csv(
            file,
            sep=';',
            header=0,
            names=['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
        )
        dfs.append(df)
    
    # Combine all dataframes
    df = pd.concat(dfs, ignore_index=True)
    
    # Create datetime column
    df['Datetime'] = pd.to_datetime(
        df['Date'] + ' ' + df['Time'],
        format='%d/%m/%Y %H:%M:%S'
    )
    
    # Sort by datetime
    df = df.sort_values('Datetime').reset_index(drop=True)
    
    # Extract hour for filtering
    df['Hour'] = df['Datetime'].dt.hour
    
    print(f"\nTotal records loaded: {len(df)}")
    print(f"Date range: {df['Datetime'].min()} to {df['Datetime'].max()}")
    
    return df


def identify_fvg(df):
    """
    Identify Fair Value Gaps (FVG) in the dataset.
    
    FVG Bullish: Low[i] > High[i-2] -> Gap zone between High[i-2] and Low[i]
    FVG Bearish: High[i] < Low[i-2] -> Gap zone between Low[i-2] and High[i]
    
    Args:
        df: pandas.DataFrame with OHLC data
        
    Returns:
        list: List of dictionaries containing FVG information
    """
    print("\nIdentifying Fair Value Gaps...")
    
    fvgs = []
    
    # Start from index 2 (need i-2)
    for i in range(2, len(df)):
        current_low = df.loc[i, 'Low']
        current_high = df.loc[i, 'High']
        prev2_high = df.loc[i-2, 'High']
        prev2_low = df.loc[i-2, 'Low']
        
        # Check for Bullish FVG: Low[i] > High[i-2]
        if current_low > prev2_high:
            fvg = {
                'index': i,
                'datetime': df.loc[i, 'Datetime'],
                'date': df.loc[i, 'Date'],
                'time': df.loc[i, 'Time'],
                'hour': df.loc[i, 'Hour'],
                'type': 'Bullish',
                'zone_low': prev2_high,
                'zone_high': current_low,
                'gap_size': current_low - prev2_high,
                'filled': False,
                'fill_index': None,
                'fill_datetime': None,
                'candles_to_fill': None
            }
            fvgs.append(fvg)
        
        # Check for Bearish FVG: High[i] < Low[i-2]
        elif current_high < prev2_low:
            fvg = {
                'index': i,
                'datetime': df.loc[i, 'Datetime'],
                'date': df.loc[i, 'Date'],
                'time': df.loc[i, 'Time'],
                'hour': df.loc[i, 'Hour'],
                'type': 'Bearish',
                'zone_low': current_high,
                'zone_high': prev2_low,
                'gap_size': prev2_low - current_high,
                'filled': False,
                'fill_index': None,
                'fill_datetime': None,
                'candles_to_fill': None
            }
            fvgs.append(fvg)
    
    print(f"Total FVGs identified: {len(fvgs)}")
    return fvgs


def filter_tokyo_session(fvgs, start_hour=19, end_hour=23):
    """
    Filter FVGs to only those created during Tokyo session (19:00-23:00).
    
    Args:
        fvgs: List of FVG dictionaries
        start_hour: Start hour of Tokyo session (default 19)
        end_hour: End hour of Tokyo session (default 23)
        
    Returns:
        list: Filtered list of FVGs
    """
    print(f"\nFiltering FVGs for Tokyo session ({start_hour}:00-{end_hour}:00)...")
    
    tokyo_fvgs = [
        fvg for fvg in fvgs
        if start_hour <= fvg['hour'] <= end_hour
    ]
    
    print(f"FVGs during Tokyo session: {len(tokyo_fvgs)}")
    return tokyo_fvgs


def check_fvg_fill(df, fvgs):
    """
    Check if each FVG was filled/touched by future price action.
    
    For Bullish FVG: Filled if future Low < zone_high (upper boundary of gap)
    For Bearish FVG: Filled if future High > zone_low (lower boundary of gap)
    
    Args:
        df: pandas.DataFrame with OHLC data
        fvgs: List of FVG dictionaries
        
    Returns:
        list: Updated list of FVGs with fill information
    """
    print("\nChecking FVG fills/retracements...")
    
    filled_count = 0
    
    for fvg in fvgs:
        i = fvg['index']
        fvg_type = fvg['type']
        zone_low = fvg['zone_low']
        zone_high = fvg['zone_high']
        
        # Check all future candles
        for j in range(i + 1, len(df)):
            future_low = df.loc[j, 'Low']
            future_high = df.loc[j, 'High']
            
            # Check if FVG is filled
            if fvg_type == 'Bullish':
                # Bullish FVG filled if price retraces down into gap
                if future_low <= zone_high:
                    fvg['filled'] = True
                    fvg['fill_index'] = j
                    fvg['fill_datetime'] = df.loc[j, 'Datetime']
                    fvg['candles_to_fill'] = j - i
                    filled_count += 1
                    break
            else:  # Bearish
                # Bearish FVG filled if price retraces up into gap
                if future_high >= zone_low:
                    fvg['filled'] = True
                    fvg['fill_index'] = j
                    fvg['fill_datetime'] = df.loc[j, 'Datetime']
                    fvg['candles_to_fill'] = j - i
                    filled_count += 1
                    break
    
    print(f"FVGs filled: {filled_count} / {len(fvgs)}")
    return fvgs


def calculate_statistics(df, fvgs):
    """
    Calculate comprehensive statistics for FVGs.
    
    Args:
        df: pandas.DataFrame with OHLC data
        fvgs: List of FVG dictionaries with fill information
        
    Returns:
        dict: Dictionary of statistics
    """
    print("\nCalculating statistics...")
    
    # Total FVGs
    total_fvgs = len(fvgs)
    
    # Bullish and Bearish FVGs
    bullish_fvgs = [fvg for fvg in fvgs if fvg['type'] == 'Bullish']
    bearish_fvgs = [fvg for fvg in fvgs if fvg['type'] == 'Bearish']
    
    # Filled FVGs
    filled_fvgs = [fvg for fvg in fvgs if fvg['filled']]
    filled_bullish = [fvg for fvg in bullish_fvgs if fvg['filled']]
    filled_bearish = [fvg for fvg in bearish_fvgs if fvg['filled']]
    
    # Calculate unique trading days
    unique_dates = df['Date'].nunique()
    
    # Fill rates
    fill_rate_global = (len(filled_fvgs) / total_fvgs * 100) if total_fvgs > 0 else 0
    fill_rate_bullish = (len(filled_bullish) / len(bullish_fvgs) * 100) if bullish_fvgs else 0
    fill_rate_bearish = (len(filled_bearish) / len(bearish_fvgs) * 100) if bearish_fvgs else 0
    
    # Average FVGs per session
    avg_fvgs_per_session = total_fvgs / unique_dates if unique_dates > 0 else 0
    
    # Average candles to fill
    candles_to_fill = [fvg['candles_to_fill'] for fvg in filled_fvgs]
    avg_candles_to_fill = np.mean(candles_to_fill) if candles_to_fill else 0
    
    # Average gap sizes
    avg_gap_size_all = np.mean([fvg['gap_size'] for fvg in fvgs]) if fvgs else 0
    avg_gap_size_bullish = np.mean([fvg['gap_size'] for fvg in bullish_fvgs]) if bullish_fvgs else 0
    avg_gap_size_bearish = np.mean([fvg['gap_size'] for fvg in bearish_fvgs]) if bearish_fvgs else 0
    
    stats = {
        'total_fvgs': total_fvgs,
        'bullish_count': len(bullish_fvgs),
        'bearish_count': len(bearish_fvgs),
        'unique_trading_days': unique_dates,
        'avg_fvgs_per_session': avg_fvgs_per_session,
        'filled_total': len(filled_fvgs),
        'fill_rate_global': fill_rate_global,
        'filled_bullish': len(filled_bullish),
        'fill_rate_bullish': fill_rate_bullish,
        'filled_bearish': len(filled_bearish),
        'fill_rate_bearish': fill_rate_bearish,
        'avg_candles_to_fill': avg_candles_to_fill,
        'avg_gap_size_all': avg_gap_size_all,
        'avg_gap_size_bullish': avg_gap_size_bullish,
        'avg_gap_size_bearish': avg_gap_size_bearish,
        'date_range_start': df['Datetime'].min(),
        'date_range_end': df['Datetime'].max()
    }
    
    return stats


def display_results(stats, fvgs):
    """
    Display comprehensive analysis results.
    
    Args:
        stats: Dictionary of statistics
        fvgs: List of FVG dictionaries
    """
    print("\n" + "="*80)
    print("FVG TOKYO SESSION ANALYSIS RESULTS (19:00-23:00)")
    print("="*80)
    
    print(f"\nDATE RANGE: {stats['date_range_start']} to {stats['date_range_end']}")
    print(f"Total Trading Days: {stats['unique_trading_days']}")
    
    print("\n" + "-"*80)
    print("GLOBAL STATISTICS")
    print("-"*80)
    print(f"Total FVGs Created (Tokyo Session):     {stats['total_fvgs']}")
    print(f"  - Bullish FVGs:                        {stats['bullish_count']} ({stats['bullish_count']/stats['total_fvgs']*100:.2f}%)")
    print(f"  - Bearish FVGs:                        {stats['bearish_count']} ({stats['bearish_count']/stats['total_fvgs']*100:.2f}%)")
    print(f"\nAverage FVGs per Session:                {stats['avg_fvgs_per_session']:.2f}")
    print(f"Average Gap Size (All):                  {stats['avg_gap_size_all']:.2f} points")
    print(f"  - Bullish Avg Gap Size:                {stats['avg_gap_size_bullish']:.2f} points")
    print(f"  - Bearish Avg Gap Size:                {stats['avg_gap_size_bearish']:.2f} points")
    
    print("\n" + "-"*80)
    print("FILL/RETRACEMENT ANALYSIS")
    print("-"*80)
    print(f"Total FVGs Filled:                       {stats['filled_total']} / {stats['total_fvgs']}")
    print(f"Global Fill Rate:                        {stats['fill_rate_global']:.2f}%")
    print(f"\nBullish FVGs Filled:                     {stats['filled_bullish']} / {stats['bullish_count']}")
    print(f"Bullish Fill Rate:                       {stats['fill_rate_bullish']:.2f}%")
    print(f"\nBearish FVGs Filled:                     {stats['filled_bearish']} / {stats['bearish_count']}")
    print(f"Bearish Fill Rate:                       {stats['fill_rate_bearish']:.2f}%")
    print(f"\nAverage Candles to Fill (when filled):   {stats['avg_candles_to_fill']:.2f} candles")
    
    print("\n" + "-"*80)
    print("SAMPLE FVGs (First 10)")
    print("-"*80)
    
    # Display first 10 FVGs
    for i, fvg in enumerate(fvgs[:10]):
        print(f"\nFVG #{i+1}")
        print(f"  DateTime:     {fvg['datetime']}")
        print(f"  Type:         {fvg['type']}")
        print(f"  Zone:         {fvg['zone_low']:.2f} - {fvg['zone_high']:.2f} (Gap: {fvg['gap_size']:.2f} pts)")
        print(f"  Filled:       {'Yes' if fvg['filled'] else 'No'}")
        if fvg['filled']:
            print(f"  Fill Time:    {fvg['fill_datetime']}")
            print(f"  Candles:      {fvg['candles_to_fill']} candles to fill")
    
    print("\n" + "="*80)


def export_to_csv(fvgs, filename='fvg_tokyo_session_results.csv'):
    """
    Export FVG results to CSV file.
    
    Args:
        fvgs: List of FVG dictionaries
        filename: Output filename
    """
    print(f"\nExporting results to {filename}...")
    
    # Convert to DataFrame
    df_export = pd.DataFrame(fvgs)
    
    # Select and order columns
    columns = [
        'datetime', 'date', 'time', 'hour', 'type',
        'zone_low', 'zone_high', 'gap_size',
        'filled', 'fill_datetime', 'candles_to_fill'
    ]
    df_export = df_export[columns]
    
    # Export to CSV
    df_export.to_csv(filename, index=False)
    print(f"Results exported successfully to {filename}")


def main():
    """
    Main function to run the FVG Tokyo Session analysis.
    """
    print("="*80)
    print("FVG (Fair Value Gap) Tokyo Session Analysis")
    print("="*80)
    
    try:
        # Step 1: Load data
        df = load_1h_data()
        
        # Step 2: Identify all FVGs
        all_fvgs = identify_fvg(df)
        
        # Step 3: Filter for Tokyo session (19:00-23:00)
        tokyo_fvgs = filter_tokyo_session(all_fvgs, start_hour=19, end_hour=23)
        
        # Step 4: Check which FVGs were filled
        tokyo_fvgs = check_fvg_fill(df, tokyo_fvgs)
        
        # Step 5: Calculate statistics
        stats = calculate_statistics(df, tokyo_fvgs)
        
        # Step 6: Display results
        display_results(stats, tokyo_fvgs)
        
        # Step 7: Export to CSV
        export_to_csv(tokyo_fvgs)
        
        print("\nAnalysis completed successfully!")
        
    except Exception as e:
        print(f"\nError during analysis: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

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
from collections import defaultdict
import glob
import os

# Constants for display formatting
BAR_SCALE_FACTOR = 2  # Scale factor for console bar charts
BAR_CHAR = '█'  # Character used for bar charts


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


def check_london_killzone_fill(df, fvgs, london_start=1, london_end=4):
    """
    Check if Tokyo FVGs from day N-1 are filled during London killzone on day N.
    
    London killzone is typically 01:00-04:00 (3 hours).
    For each Tokyo FVG, we check if it gets filled on the NEXT day during London hours.
    IMPORTANT: Only considers FVGs that remain UNFILLED before London killzone starts.
    
    Args:
        df: pandas.DataFrame with OHLC data
        fvgs: List of FVG dictionaries
        london_start: Start hour of London killzone (default 1 = 01:00)
        london_end: End hour of London killzone (default 4 = 04:00)
        
    Returns:
        list: Updated list of FVGs with London killzone fill information
    """
    print(f"\nChecking London killzone fills ({london_start:02d}:00-{london_end:02d}:00 next day)...")
    print("Filtering for FVGs that remain UNFILLED before London killzone starts...")
    
    london_filled_count = 0
    unfilled_before_london = 0
    
    for fvg in fvgs:
        i = fvg['index']
        fvg_type = fvg['type']
        zone_low = fvg['zone_low']
        zone_high = fvg['zone_high']
        fvg_date = fvg['datetime'].date()
        
        # Initialize London killzone fill tracking
        fvg['london_filled'] = False
        fvg['london_fill_index'] = None
        fvg['london_fill_datetime'] = None
        fvg['london_candles_to_fill'] = None
        fvg['unfilled_before_london'] = False
        
        # First, check if FVG was already filled BEFORE London killzone starts
        filled_before_london = False
        london_start_index = None
        
        for j in range(i + 1, len(df)):
            future_datetime = df.loc[j, 'Datetime']
            future_date = future_datetime.date()
            future_hour = df.loc[j, 'Hour']
            future_low = df.loc[j, 'Low']
            future_high = df.loc[j, 'High']
            
            # Calculate day difference
            days_diff = (future_date - fvg_date).days
            
            # Mark the start of London killzone
            if days_diff == 1 and future_hour == london_start:
                london_start_index = j
                break
            
            # Check if FVG was filled before London killzone
            if days_diff <= 1:
                if fvg_type == 'Bullish':
                    if future_low <= zone_high:
                        filled_before_london = True
                        break
                else:  # Bearish
                    if future_high >= zone_low:
                        filled_before_london = True
                        break
        
        # Only proceed if FVG was NOT filled before London killzone
        if not filled_before_london and london_start_index is not None:
            fvg['unfilled_before_london'] = True
            unfilled_before_london += 1
            
            # Now check if it gets filled during London killzone
            for j in range(london_start_index, len(df)):
                future_datetime = df.loc[j, 'Datetime']
                future_date = future_datetime.date()
                future_hour = df.loc[j, 'Hour']
                future_low = df.loc[j, 'Low']
                future_high = df.loc[j, 'High']
                
                # Calculate day difference
                days_diff = (future_date - fvg_date).days
                
                # Only check London killzone on the next day
                if days_diff == 1 and london_start <= future_hour <= london_end:
                    # Check if FVG is filled during London killzone
                    if fvg_type == 'Bullish':
                        if future_low <= zone_high:
                            fvg['london_filled'] = True
                            fvg['london_fill_index'] = j
                            fvg['london_fill_datetime'] = future_datetime
                            fvg['london_candles_to_fill'] = j - i
                            london_filled_count += 1
                            break
                    else:  # Bearish
                        if future_high >= zone_low:
                            fvg['london_filled'] = True
                            fvg['london_fill_index'] = j
                            fvg['london_fill_datetime'] = future_datetime
                            fvg['london_candles_to_fill'] = j - i
                            london_filled_count += 1
                            break
                
                # Stop checking after London killzone window
                elif days_diff > 1:
                    break
    
    print(f"FVGs unfilled before London killzone: {unfilled_before_london} / {len(fvgs)}")
    print(f"FVGs filled during London killzone (of unfilled): {london_filled_count} / {unfilled_before_london}")
    return fvgs


def calculate_london_statistics(fvgs):
    """
    Calculate statistics specifically for London killzone fills.
    Only considers FVGs that were UNFILLED before London killzone started.
    
    Args:
        fvgs: List of FVG dictionaries with London fill information
        
    Returns:
        dict: Dictionary of London-specific statistics
    """
    print("\nCalculating London killzone statistics...")
    
    # Filter for FVGs that were unfilled before London
    unfilled_before_london = [fvg for fvg in fvgs if fvg.get('unfilled_before_london', False)]
    
    # Total FVGs (unfilled before London)
    total_fvgs = len(unfilled_before_london)
    
    # Bullish and Bearish FVGs (unfilled before London)
    bullish_fvgs = [fvg for fvg in unfilled_before_london if fvg['type'] == 'Bullish']
    bearish_fvgs = [fvg for fvg in unfilled_before_london if fvg['type'] == 'Bearish']
    
    # London filled FVGs (from those unfilled before)
    london_filled_fvgs = [fvg for fvg in unfilled_before_london if fvg['london_filled']]
    london_filled_bullish = [fvg for fvg in bullish_fvgs if fvg['london_filled']]
    london_filled_bearish = [fvg for fvg in bearish_fvgs if fvg['london_filled']]
    
    # London fill rates (of those unfilled before London)
    london_fill_rate_global = (len(london_filled_fvgs) / total_fvgs * 100) if total_fvgs > 0 else 0
    london_fill_rate_bullish = (len(london_filled_bullish) / len(bullish_fvgs) * 100) if bullish_fvgs else 0
    london_fill_rate_bearish = (len(london_filled_bearish) / len(bearish_fvgs) * 100) if bearish_fvgs else 0
    
    # Average candles to fill during London
    london_candles_to_fill = [fvg['london_candles_to_fill'] for fvg in london_filled_fvgs]
    avg_london_candles_to_fill = np.mean(london_candles_to_fill) if london_candles_to_fill else 0
    
    stats = {
        'total_unfilled_before_london': total_fvgs,
        'bullish_unfilled_before_london': len(bullish_fvgs),
        'bearish_unfilled_before_london': len(bearish_fvgs),
        'london_filled_total': len(london_filled_fvgs),
        'london_fill_rate_global': london_fill_rate_global,
        'london_filled_bullish': len(london_filled_bullish),
        'london_fill_rate_bullish': london_fill_rate_bullish,
        'london_filled_bearish': len(london_filled_bearish),
        'london_fill_rate_bearish': london_fill_rate_bearish,
        'avg_london_candles_to_fill': avg_london_candles_to_fill
    }
    
    return stats


def analyze_multiple_fvgs_per_session(fvgs):
    """
    Analyze sessions with multiple FVGs and track how many get filled in London.
    
    When multiple FVGs form in the same Tokyo session, this function determines:
    - How many sessions have 1, 2, 3, or more FVGs
    - For sessions with multiple FVGs, how many of them get filled in London
    
    Args:
        fvgs: List of FVG dictionaries with London fill information
        
    Returns:
        dict: Dictionary with distribution statistics
    """
    print("\nAnalyzing multiple FVGs per Tokyo session...")
    
    # Group FVGs by date (Tokyo session date)
    sessions = defaultdict(list)
    
    for fvg in fvgs:
        session_date = fvg['datetime'].date()
        sessions[session_date].append(fvg)
    
    # Analyze distribution
    session_counts = {}  # How many sessions have N FVGs
    fill_distribution = {}  # For sessions with N FVGs, how many get filled
    
    for session_date, session_fvgs in sessions.items():
        num_fvgs = len(session_fvgs)
        num_filled = sum(1 for fvg in session_fvgs if fvg['london_filled'])
        
        # Count sessions by number of FVGs
        if num_fvgs not in session_counts:
            session_counts[num_fvgs] = 0
        session_counts[num_fvgs] += 1
        
        # Track fill distribution for sessions with multiple FVGs
        if num_fvgs not in fill_distribution:
            fill_distribution[num_fvgs] = defaultdict(int)
        fill_distribution[num_fvgs][num_filled] += 1
    
    # Calculate probabilities for sessions with multiple FVGs
    multi_fvg_stats = {}
    
    for num_fvgs in sorted(session_counts.keys()):
        if num_fvgs >= 2:  # Only analyze sessions with 2+ FVGs
            total_sessions = session_counts[num_fvgs]
            fill_probs = {}
            
            for num_filled in range(num_fvgs + 1):
                count = fill_distribution[num_fvgs].get(num_filled, 0)
                probability = (count / total_sessions * 100) if total_sessions > 0 else 0
                fill_probs[num_filled] = {
                    'count': count,
                    'probability': probability
                }
            
            multi_fvg_stats[num_fvgs] = {
                'total_sessions': total_sessions,
                'fill_probabilities': fill_probs
            }
    
    stats = {
        'total_sessions': len(sessions),
        'session_counts': session_counts,
        'multi_fvg_stats': multi_fvg_stats
    }
    
    return stats


def display_multiple_fvgs_analysis(multi_stats):
    """
    Display analysis of sessions with multiple FVGs.
    
    Args:
        multi_stats: Dictionary with multiple FVG statistics
    """
    print("\n" + "="*80)
    print("MULTIPLE FVGs PER SESSION ANALYSIS")
    print("="*80)
    print("\nWhen multiple FVGs form in the same Tokyo session, how many get filled in London?")
    
    print("\n" + "-"*80)
    print("SESSION DISTRIBUTION")
    print("-"*80)
    
    session_counts = multi_stats['session_counts']
    total_sessions = multi_stats['total_sessions']
    
    for num_fvgs in sorted(session_counts.keys()):
        count = session_counts[num_fvgs]
        percentage = (count / total_sessions * 100) if total_sessions > 0 else 0
        print(f"Sessions with {num_fvgs} FVG(s):                {count:4d} ({percentage:5.2f}%)")
    
    print(f"\nTotal sessions with FVGs:             {total_sessions}")
    
    # Display detailed analysis for sessions with 2+ FVGs
    multi_fvg_stats = multi_stats['multi_fvg_stats']
    
    if not multi_fvg_stats:
        print("\nNo sessions with multiple FVGs found.")
        return
    
    for num_fvgs in sorted(multi_fvg_stats.keys()):
        stats = multi_fvg_stats[num_fvgs]
        total_sessions = stats['total_sessions']
        fill_probs = stats['fill_probabilities']
        
        print("\n" + "-"*80)
        print(f"SESSIONS WITH {num_fvgs} FVGs (Total: {total_sessions} sessions)")
        print("-"*80)
        
        print(f"\nProbability distribution of London fills:")
        for num_filled in range(num_fvgs + 1):
            prob_info = fill_probs[num_filled]
            count = prob_info['count']
            probability = prob_info['probability']
            
            if num_filled == 0:
                label = "None filled"
            elif num_filled == 1:
                label = "1 filled"
            elif num_filled == num_fvgs:
                label = f"All {num_fvgs} filled"
            else:
                label = f"{num_filled} filled"
            
            # Create a simple bar chart
            bar_length = int(probability / BAR_SCALE_FACTOR)
            bar = BAR_CHAR * bar_length
            
            print(f"  {label:15s}: {count:4d} sessions ({probability:5.2f}%) {bar}")
    
    print("\n" + "="*80)


def display_london_results(stats, london_stats, fvgs):
    """
    Display London killzone analysis results.
    Only shows stats for FVGs that were UNFILLED before London killzone.
    
    Args:
        stats: Dictionary of overall statistics
        london_stats: Dictionary of London-specific statistics
        fvgs: List of FVG dictionaries
    """
    print("\n" + "="*80)
    print("LONDON KILLZONE FILL ANALYSIS (UNFILLED FVGs ONLY)")
    print("="*80)
    print("\nAnalyzing Tokyo FVGs (day N-1) that remain UNFILLED until London killzone")
    print("Then checking if they get filled during London killzone (01:00-04:00 on day N)")
    
    print("\n" + "-"*80)
    print("FILTERING RESULTS")
    print("-"*80)
    print(f"Total Tokyo FVGs:                        {stats['total_fvgs']}")
    print(f"Unfilled before London killzone:         {london_stats['total_unfilled_before_london']} ({london_stats['total_unfilled_before_london']/stats['total_fvgs']*100:.2f}%)")
    print(f"  - Bullish unfilled:                    {london_stats['bullish_unfilled_before_london']}")
    print(f"  - Bearish unfilled:                    {london_stats['bearish_unfilled_before_london']}")
    
    print("\n" + "-"*80)
    print("LONDON KILLZONE FILL RATES (OF UNFILLED FVGs)")
    print("-"*80)
    print(f"Filled in London Killzone:               {london_stats['london_filled_total']} / {london_stats['total_unfilled_before_london']}")
    print(f"London Killzone Fill Rate:               {london_stats['london_fill_rate_global']:.2f}%")
    print(f"\nBullish FVGs in London:                  {london_stats['london_filled_bullish']} / {london_stats['bullish_unfilled_before_london']}")
    print(f"Bullish London Fill Rate:                {london_stats['london_fill_rate_bullish']:.2f}%")
    print(f"\nBearish FVGs in London:                  {london_stats['london_filled_bearish']} / {london_stats['bearish_unfilled_before_london']}")
    print(f"Bearish London Fill Rate:                {london_stats['london_fill_rate_bearish']:.2f}%")
    print(f"\nAverage Candles to Fill (London):        {london_stats['avg_london_candles_to_fill']:.2f} candles")
    
    print("\n" + "-"*80)
    print("SAMPLE LONDON KILLZONE FILLS (First 10)")
    print("-"*80)
    
    # Display first 10 FVGs that were filled in London killzone
    london_fills = [fvg for fvg in fvgs if fvg['london_filled']]
    for i, fvg in enumerate(london_fills[:10]):
        print(f"\nFVG #{i+1}")
        print(f"  Tokyo DateTime:   {fvg['datetime']}")
        print(f"  Type:             {fvg['type']}")
        print(f"  Zone:             {fvg['zone_low']:.2f} - {fvg['zone_high']:.2f} (Gap: {fvg['gap_size']:.2f} pts)")
        print(f"  London Fill Time: {fvg['london_fill_datetime']}")
        print(f"  Candles to Fill:  {fvg['london_candles_to_fill']} candles")
    
    if len(london_fills) == 0:
        print("\n  No FVGs were filled during London killzone.")
    
    print("\n" + "="*80)


def export_london_csv(fvgs, filename='fvg_tokyo_london_killzone_results.csv'):
    """
    Export FVG results with London killzone information to CSV file.
    
    Args:
        fvgs: List of FVG dictionaries
        filename: Output filename
    """
    print(f"\nExporting London killzone results to {filename}...")
    
    # Convert to DataFrame
    df_export = pd.DataFrame(fvgs)
    
    # Select and order columns
    columns = [
        'datetime', 'date', 'time', 'hour', 'type',
        'zone_low', 'zone_high', 'gap_size',
        'filled', 'fill_datetime', 'candles_to_fill',
        'unfilled_before_london', 'london_filled', 'london_fill_datetime', 'london_candles_to_fill'
    ]
    df_export = df_export[columns]
    
    # Export to CSV
    df_export.to_csv(filename, index=False)
    print(f"London killzone results exported successfully to {filename}")


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
        
        # Step 8: Check London killzone fills (NEW)
        tokyo_fvgs = check_london_killzone_fill(df, tokyo_fvgs, london_start=1, london_end=4)
        
        # Step 9: Calculate London statistics
        london_stats = calculate_london_statistics(tokyo_fvgs)
        
        # Step 10: Display London results
        display_london_results(stats, london_stats, tokyo_fvgs)
        
        # Step 11: Export London CSV
        export_london_csv(tokyo_fvgs)
        
        # Step 12: Analyze multiple FVGs per session (NEW)
        multi_stats = analyze_multiple_fvgs_per_session(tokyo_fvgs)
        
        # Step 13: Display multiple FVGs analysis
        display_multiple_fvgs_analysis(multi_stats)
        
        print("\nAnalysis completed successfully!")
        
    except Exception as e:
        print(f"\nError during analysis: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

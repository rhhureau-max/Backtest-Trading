#!/usr/bin/env python3
"""
Tokyo-London Session Analysis for NQ 1-minute Data
Analyzes Judas Swing vs London Continuation patterns during London Killzone
"""

import pandas as pd
import numpy as np
from datetime import datetime, time
import zipfile
import os
import glob


def load_nq_data(base_path):
    """
    Load all NQ 1-minute data from CSV and ZIP files (2018 to present)
    Optimized for large dataset processing
    """
    print("Loading NQ 1-minute data...")
    all_data = []
    
    # Get all relevant files
    csv_files = sorted(glob.glob(os.path.join(base_path, "*1m.csv")))
    zip_files = sorted(glob.glob(os.path.join(base_path, "*1m.csv.zip")))
    
    # Process CSV files directly
    for csv_file in csv_files:
        try:
            df = pd.read_csv(csv_file, sep=';', 
                           names=['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume'],
                           skiprows=1)
            all_data.append(df)
            print(f"  Loaded: {os.path.basename(csv_file)}")
        except Exception as e:
            print(f"  Error loading {csv_file}: {e}")
    
    # Process ZIP files
    for zip_file in zip_files:
        try:
            with zipfile.ZipFile(zip_file, 'r') as z:
                # Get the CSV filename inside the ZIP
                csv_name = [name for name in z.namelist() if name.endswith('.csv')][0]
                with z.open(csv_name) as f:
                    df = pd.read_csv(f, sep=';',
                                   names=['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume'],
                                   skiprows=1)
                    all_data.append(df)
                    print(f"  Loaded: {os.path.basename(zip_file)}")
        except Exception as e:
            print(f"  Error loading {zip_file}: {e}")
    
    # Combine all data
    if not all_data:
        raise ValueError("No data files found!")
    
    df = pd.concat(all_data, ignore_index=True)
    
    # Parse datetime
    df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%d/%m/%Y %H:%M:%S')
    df = df.sort_values('DateTime').reset_index(drop=True)
    
    # Convert price columns to float
    for col in ['Open', 'High', 'Low', 'Close']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Extract time for session filtering
    df['Time_Only'] = df['DateTime'].dt.time
    df['Date_Only'] = df['DateTime'].dt.date
    
    print(f"Total rows loaded: {len(df):,}")
    print(f"Date range: {df['DateTime'].min()} to {df['DateTime'].max()}")
    
    return df


def identify_sessions(df):
    """
    Identify Tokyo and London sessions for each trading day
    Tokyo: 18:00 - 01:00 (previous day 18:00 to next day 01:00)
    London: 01:00 - 05:00
    Optimized using vectorized operations
    """
    print("\nIdentifying trading sessions...")
    
    # Add hour column for faster filtering
    df['Hour'] = df['DateTime'].dt.hour
    
    # Mark Tokyo session data (18:00-23:59)
    df['is_tokyo_evening'] = (df['Hour'] >= 18)
    # Mark Tokyo session data (00:00-00:59)
    df['is_tokyo_night'] = (df['Hour'] == 0)
    # Mark London session data (01:00-04:59)
    df['is_london'] = (df['Hour'] >= 1) & (df['Hour'] < 5)
    
    sessions = []
    
    # Group by date for efficient processing
    df_grouped = df.groupby('Date_Only')
    dates = sorted(df['Date_Only'].unique())
    
    for i in range(len(dates) - 1):
        current_date = dates[i]
        next_date = dates[i + 1]
        
        try:
            current_df = df_grouped.get_group(current_date)
            next_df = df_grouped.get_group(next_date)
        except KeyError:
            continue
        
        # Tokyo session: 18:00+ on current_date and 00:00-00:59 on next_date
        tokyo_evening = current_df[current_df['is_tokyo_evening']]
        tokyo_night = next_df[next_df['is_tokyo_night']]
        tokyo_data = pd.concat([tokyo_evening, tokyo_night])
        
        # London session: 01:00-04:59 on next_date
        london_data = next_df[next_df['is_london']]
        
        if len(tokyo_data) > 0 and len(london_data) > 0:
            sessions.append({
                'date': next_date,
                'tokyo_data': tokyo_data,
                'london_data': london_data
            })
    
    print(f"Total sessions identified: {len(sessions)}")
    return sessions


def analyze_session(session):
    """
    Analyze a single Tokyo-London session pair
    Returns: dict with session analysis results
    Optimized for speed
    """
    tokyo_data = session['tokyo_data']
    london_data = session['london_data']
    
    # Calculate Tokyo Range
    tokyo_high = tokyo_data['High'].max()
    tokyo_low = tokyo_data['Low'].min()
    tokyo_eq = (tokyo_high + tokyo_low) / 2
    tokyo_range = tokyo_high - tokyo_low
    
    # Check for breakout during London session
    london_high = london_data['High'].max()
    london_low = london_data['Low'].min()
    
    breakout = False
    breakout_direction = None
    
    # Determine if breakout occurred
    if london_high > tokyo_high:
        breakout = True
        breakout_direction = 'bullish'
    elif london_low < tokyo_low:
        breakout = True
        breakout_direction = 'bearish'
    
    if not breakout:
        return None
    
    # Check if price touched Tokyo_EQ after breakout (vectorized)
    touched_eq = False
    london_sorted = london_data.sort_values('DateTime')
    
    if breakout_direction == 'bullish':
        # Find first breakout candle
        breakout_mask = london_sorted['High'] > tokyo_high
        if breakout_mask.any():
            first_breakout_idx = london_sorted[breakout_mask].index[0]
            # Check if any subsequent candle touched EQ
            subsequent = london_sorted.loc[first_breakout_idx:]
            touched_eq = (subsequent['Low'] <= tokyo_eq).any()
    else:  # bearish
        # Find first breakout candle
        breakout_mask = london_sorted['Low'] < tokyo_low
        if breakout_mask.any():
            first_breakout_idx = london_sorted[breakout_mask].index[0]
            # Check if any subsequent candle touched EQ
            subsequent = london_sorted.loc[first_breakout_idx:]
            touched_eq = (subsequent['High'] >= tokyo_eq).any()
    
    # Classify scenario
    if touched_eq:
        scenario = 'Judas_Swing'
        max_expansion = None
        expansion_ratio = None
    else:
        scenario = 'Continuation'
        
        # Calculate expansion metrics for continuation
        if breakout_direction == 'bullish':
            max_expansion = london_high - tokyo_high
        else:
            max_expansion = tokyo_low - london_low
        
        expansion_ratio = max_expansion / tokyo_range if tokyo_range > 0 else 0
    
    return {
        'date': session['date'],
        'tokyo_high': tokyo_high,
        'tokyo_low': tokyo_low,
        'tokyo_eq': tokyo_eq,
        'tokyo_range': tokyo_range,
        'breakout': breakout,
        'breakout_direction': breakout_direction,
        'scenario': scenario,
        'max_expansion': max_expansion,
        'expansion_ratio': expansion_ratio
    }


def calculate_statistics(results):
    """
    Calculate and print comprehensive statistics
    """
    print("\n" + "="*70)
    print("TOKYO-LONDON SESSION ANALYSIS RESULTS")
    print("="*70)
    
    # Filter valid results
    valid_results = [r for r in results if r is not None]
    
    total_sessions = len(valid_results)
    judas_swings = [r for r in valid_results if r['scenario'] == 'Judas_Swing']
    continuations = [r for r in valid_results if r['scenario'] == 'Continuation']
    
    print(f"\n1. BREAKOUT STATISTICS:")
    print(f"   Total sessions with breakout: {total_sessions}")
    print(f"   - Judas Swings (Reversal): {len(judas_swings)} ({len(judas_swings)/total_sessions*100:.1f}%)")
    print(f"   - London Continuations: {len(continuations)} ({len(continuations)/total_sessions*100:.1f}%)")
    
    if len(continuations) > 0:
        print(f"\n2. CONTINUATION PROBABILITY:")
        continuation_rate = len(continuations) / total_sessions * 100
        judas_rate = len(judas_swings) / total_sessions * 100
        print(f"   Probability of Continuation: {continuation_rate:.2f}%")
        print(f"   Probability of Judas Swing: {judas_rate:.2f}%")
        
        # Direction analysis
        bullish_cont = [r for r in continuations if r['breakout_direction'] == 'bullish']
        bearish_cont = [r for r in continuations if r['breakout_direction'] == 'bearish']
        
        print(f"\n3. CONTINUATION DIRECTION:")
        print(f"   Bullish Continuations: {len(bullish_cont)} ({len(bullish_cont)/len(continuations)*100:.1f}%)")
        print(f"   Bearish Continuations: {len(bearish_cont)} ({len(bearish_cont)/len(continuations)*100:.1f}%)")
        
        # Expansion metrics
        expansions = [r['max_expansion'] for r in continuations if r['max_expansion'] is not None]
        expansion_ratios = [r['expansion_ratio'] for r in continuations if r['expansion_ratio'] is not None]
        
        print(f"\n4. EXPANSION METRICS (for Continuations):")
        print(f"   Max Expansion - Mean: {np.mean(expansions):.2f} points")
        print(f"   Max Expansion - Median: {np.median(expansions):.2f} points")
        print(f"   Max Expansion - Min: {np.min(expansions):.2f} points")
        print(f"   Max Expansion - Max: {np.max(expansions):.2f} points")
        
        print(f"\n5. RANGE MULTIPLIER (Expansion Ratio):")
        print(f"   Mean Ratio: {np.mean(expansion_ratios):.2f}x")
        print(f"   Median Ratio: {np.median(expansion_ratios):.2f}x")
        print(f"   Min Ratio: {np.min(expansion_ratios):.2f}x")
        print(f"   Max Ratio: {np.max(expansion_ratios):.2f}x")
        print(f"   Interpretation: On average, London continuation extends Tokyo range by {np.mean(expansion_ratios):.2f}x")
        
        # Bullish vs Bearish breakdown
        if len(bullish_cont) > 0:
            bullish_exp = [r['max_expansion'] for r in bullish_cont]
            bullish_ratio = [r['expansion_ratio'] for r in bullish_cont]
            print(f"\n6. BULLISH CONTINUATION METRICS:")
            print(f"   Mean Expansion: {np.mean(bullish_exp):.2f} points")
            print(f"   Mean Ratio: {np.mean(bullish_ratio):.2f}x")
        
        if len(bearish_cont) > 0:
            bearish_exp = [r['max_expansion'] for r in bearish_cont]
            bearish_ratio = [r['expansion_ratio'] for r in bearish_cont]
            print(f"\n7. BEARISH CONTINUATION METRICS:")
            print(f"   Mean Expansion: {np.mean(bearish_exp):.2f} points")
            print(f"   Mean Ratio: {np.mean(bearish_ratio):.2f}x")
    
    print("\n" + "="*70)


def main():
    """
    Main execution function
    """
    start_time = datetime.now()
    
    # Set base path
    base_path = '/home/runner/work/Backtest-Trading/Backtest-Trading'
    
    # Load data
    df = load_nq_data(base_path)
    
    # Identify sessions
    sessions = identify_sessions(df)
    
    # Analyze each session
    print("\nAnalyzing sessions...")
    results = []
    for i, session in enumerate(sessions):
        if i % 100 == 0:
            print(f"  Processing session {i+1}/{len(sessions)}")
        result = analyze_session(session)
        results.append(result)
    
    # Calculate and display statistics
    calculate_statistics(results)
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    print(f"\nExecution time: {duration:.2f} seconds")
    print(f"Processing speed: {len(df)/duration:,.0f} rows/second")


if __name__ == "__main__":
    main()

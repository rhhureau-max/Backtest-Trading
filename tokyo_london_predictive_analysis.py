#!/usr/bin/env python3
"""
Advanced Predictive Analysis for Tokyo-London Session Patterns
Identifies factors that predict Judas Swings vs London Continuations
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import zipfile
import os
import glob
import sys


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
                csv_name = [name for name in z.namelist() if name.endswith('.csv')][0]
                with z.open(csv_name) as f:
                    df = pd.read_csv(f, sep=';',
                                   names=['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume'],
                                   skiprows=1)
                    all_data.append(df)
                    print(f"  Loaded: {os.path.basename(zip_file)}")
        except Exception as e:
            print(f"  Error loading {zip_file}: {e}")
    
    if not all_data:
        raise ValueError("No data files found!")
    
    df = pd.concat(all_data, ignore_index=True)
    
    # Parse datetime
    try:
        df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%d/%m/%Y %H:%M:%S')
    except Exception as e:
        print(f"Warning: Error parsing datetime, trying automatic detection: {e}")
        df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])
    
    df = df.sort_values('DateTime').reset_index(drop=True)
    
    # Convert price columns to float
    for col in ['Open', 'High', 'Low', 'Close']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    df['Hour'] = df['DateTime'].dt.hour
    df['Date_Only'] = df['DateTime'].dt.date
    
    print(f"Total rows loaded: {len(df):,}")
    print(f"Date range: {df['DateTime'].min()} to {df['DateTime'].max()}")
    
    return df


def identify_sessions(df):
    """
    Identify Tokyo and London sessions with detailed data
    
    Args:
        df: DataFrame with NQ 1-minute data including DateTime, High, Low, Close columns
    
    Returns:
        List of dicts containing:
            - date: Session date
            - tokyo_data: DataFrame of Tokyo session (18:00-01:00)
            - london_data: DataFrame of London session (01:00-05:00)
    """
    print("\nIdentifying trading sessions...")
    
    df['is_tokyo_evening'] = (df['Hour'] >= 18)
    df['is_tokyo_night'] = (df['Hour'] == 0)
    df['is_london'] = (df['Hour'] >= 1) & (df['Hour'] < 5)
    
    sessions = []
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
        
        tokyo_evening = current_df[current_df['is_tokyo_evening']]
        tokyo_night = next_df[next_df['is_tokyo_night']]
        tokyo_data = pd.concat([tokyo_evening, tokyo_night])
        london_data = next_df[next_df['is_london']]
        
        if len(tokyo_data) > 0 and len(london_data) > 0:
            sessions.append({
                'date': next_date,
                'tokyo_data': tokyo_data.sort_values('DateTime'),
                'london_data': london_data.sort_values('DateTime')
            })
    
    print(f"Total sessions identified: {len(sessions)}")
    return sessions


def analyze_session_detailed(session):
    """
    Analyze a session with detailed predictive metrics
    
    Args:
        session: Dict with 'date', 'tokyo_data', and 'london_data' DataFrames
    
    Returns:
        Dict containing analysis results with keys:
            - date, scenario, breakout_direction, tokyo_range, tokyo_close_position,
              minutes_to_breakout, velocity, initial_extension, max_expansion, expansion_ratio
        Returns None if no breakout occurred
    """
    tokyo_data = session['tokyo_data']
    london_data = session['london_data']
    
    # Tokyo Range metrics
    tokyo_high = tokyo_data['High'].max()
    tokyo_low = tokyo_data['Low'].min()
    tokyo_eq = (tokyo_high + tokyo_low) / 2
    tokyo_range = tokyo_high - tokyo_low
    
    # Tokyo close position (at 01:00)
    tokyo_close = tokyo_data['Close'].iloc[-1]
    tokyo_close_position = (tokyo_close - tokyo_low) / tokyo_range if tokyo_range > 0 else 0.5
    
    # London session analysis
    london_high = london_data['High'].max()
    london_low = london_data['Low'].min()
    
    # Determine breakout
    breakout = False
    breakout_direction = None
    
    if london_high > tokyo_high:
        breakout = True
        breakout_direction = 'bullish'
    elif london_low < tokyo_low:
        breakout = True
        breakout_direction = 'bearish'
    
    if not breakout:
        return None
    
    # Find breakout timing and velocity
    london_sorted = london_data.sort_values('DateTime')
    breakout_time = None
    breakout_candle = None
    
    if breakout_direction == 'bullish':
        breakout_mask = london_sorted['High'] > tokyo_high
        if breakout_mask.any():
            breakout_indices = london_sorted[breakout_mask].index
            if len(breakout_indices) > 0:
                breakout_candle = london_sorted.loc[breakout_indices[0]]
                breakout_time = breakout_candle['DateTime']
    else:  # bearish
        breakout_mask = london_sorted['Low'] < tokyo_low
        if breakout_mask.any():
            breakout_indices = london_sorted[breakout_mask].index
            if len(breakout_indices) > 0:
                breakout_candle = london_sorted.loc[breakout_indices[0]]
                breakout_time = breakout_candle['DateTime']
    
    if breakout_time is None:
        return None
    
    # Calculate time to breakout (minutes after 01:00)
    london_start = london_sorted['DateTime'].iloc[0]
    minutes_to_breakout = (breakout_time - london_start).total_seconds() / 60
    
    # Calculate initial velocity
    # Get candles in first 15 minutes or until max/min reached
    first_15min = london_sorted[
        london_sorted['DateTime'] <= london_start + timedelta(minutes=15)
    ]
    
    if breakout_direction == 'bullish':
        max_reached = first_15min['High'].max()
        initial_extension = max_reached - tokyo_high
    else:
        min_reached = first_15min['Low'].min()
        initial_extension = tokyo_low - min_reached
    
    # Calculate velocity (points per minute)
    time_elapsed = len(first_15min)  # number of candles (minutes)
    velocity = initial_extension / time_elapsed if time_elapsed > 0 else 0
    
    # Check if touched EQ (for scenario classification)
    touched_eq = False
    
    if breakout_direction == 'bullish':
        if breakout_mask.any():
            breakout_indices = london_sorted[breakout_mask].index
            if len(breakout_indices) > 0:
                first_breakout_idx = breakout_indices[0]
                subsequent = london_sorted.loc[first_breakout_idx:]
                touched_eq = (subsequent['Low'] <= tokyo_eq).any()
    else:
        if breakout_mask.any():
            breakout_indices = london_sorted[breakout_mask].index
            if len(breakout_indices) > 0:
                first_breakout_idx = breakout_indices[0]
                subsequent = london_sorted.loc[first_breakout_idx:]
                touched_eq = (subsequent['High'] >= tokyo_eq).any()
    
    # Classify scenario
    scenario = 'Judas_Swing' if touched_eq else 'Continuation'
    
    # Calculate max expansion for continuations
    if breakout_direction == 'bullish':
        max_expansion = london_high - tokyo_high
    else:
        max_expansion = tokyo_low - london_low
    
    expansion_ratio = max_expansion / tokyo_range if tokyo_range > 0 else 0
    
    return {
        'date': session['date'],
        'scenario': scenario,
        'breakout_direction': breakout_direction,
        'tokyo_range': tokyo_range,
        'tokyo_close_position': tokyo_close_position,
        'minutes_to_breakout': minutes_to_breakout,
        'velocity': velocity,
        'initial_extension': initial_extension,
        'max_expansion': max_expansion,
        'expansion_ratio': expansion_ratio
    }


def calculate_predictive_statistics(results):
    """
    Calculate and display comprehensive predictive statistics
    
    Args:
        results: List of analysis result dicts from analyze_session_detailed()
    
    Displays comparative analysis including:
        - Tokyo context (range size, close position)
        - Breakout timing patterns
        - Movement velocity analysis
        - Conditional probabilities
        - Multi-factor scenario analysis
    """
    print("\n" + "="*80)
    print("PREDICTIVE ANALYSIS: JUDAS SWING vs CONTINUATION FACTORS")
    print("="*80)
    
    valid_results = [r for r in results if r is not None]
    
    # Separate into groups
    judas_group = [r for r in valid_results if r['scenario'] == 'Judas_Swing']
    continuation_group = [r for r in valid_results if r['scenario'] == 'Continuation']
    
    print(f"\nDataset Summary:")
    print(f"  Total breakouts analyzed: {len(valid_results)}")
    print(f"  Group A (Judas Swings): {len(judas_group)} ({len(judas_group)/len(valid_results)*100:.1f}%)")
    print(f"  Group B (Continuations): {len(continuation_group)} ({len(continuation_group)/len(valid_results)*100:.1f}%)")
    
    # Helper function for stats
    def calc_stats(data, field):
        values = [r[field] for r in data if r[field] is not None]
        if len(values) == 0:
            return {'mean': 0, 'median': 0, 'min': 0, 'max': 0}
        return {
            'mean': np.mean(values),
            'median': np.median(values),
            'min': np.min(values),
            'max': np.max(values)
        }
    
    # 1. TOKYO CONTEXT ANALYSIS
    print("\n" + "-"*80)
    print("1. TOKYO CONTEXT (Pre-Breakout Conditions)")
    print("-"*80)
    
    judas_range = calc_stats(judas_group, 'tokyo_range')
    cont_range = calc_stats(continuation_group, 'tokyo_range')
    
    print(f"\nTokyo Range Size (Points):")
    print(f"  {'':20} {'Judas Swings':>15} {'Continuations':>15} {'Difference':>15}")
    print(f"  {'Mean':20} {judas_range['mean']:>15.2f} {cont_range['mean']:>15.2f} {cont_range['mean']-judas_range['mean']:>15.2f}")
    print(f"  {'Median':20} {judas_range['median']:>15.2f} {cont_range['median']:>15.2f} {cont_range['median']-judas_range['median']:>15.2f}")
    
    # Interpretation
    if cont_range['mean'] > judas_range['mean']:
        print(f"\n  💡 Insight: Continuations occur with LARGER Tokyo ranges on average")
        print(f"     ({cont_range['mean']:.1f} vs {judas_range['mean']:.1f} points)")
    else:
        print(f"\n  💡 Insight: Judas Swings occur with LARGER Tokyo ranges on average")
        print(f"     ({judas_range['mean']:.1f} vs {cont_range['mean']:.1f} points)")
    
    # Tokyo Close Position
    print(f"\nTokyo Close Position (0=Low, 1=High):")
    judas_close = calc_stats(judas_group, 'tokyo_close_position')
    cont_close = calc_stats(continuation_group, 'tokyo_close_position')
    
    print(f"  {'':20} {'Judas Swings':>15} {'Continuations':>15} {'Difference':>15}")
    print(f"  {'Mean':20} {judas_close['mean']:>15.3f} {cont_close['mean']:>15.3f} {cont_close['mean']-judas_close['mean']:>15.3f}")
    print(f"  {'Median':20} {judas_close['median']:>15.3f} {cont_close['median']:>15.3f} {cont_close['median']-judas_close['median']:>15.3f}")
    
    if abs(cont_close['mean'] - 0.5) > abs(judas_close['mean'] - 0.5):
        print(f"\n  💡 Insight: Continuations favor extreme closes (near High/Low)")
    else:
        print(f"\n  💡 Insight: Judas Swings favor extreme closes (near High/Low)")
    
    # 2. TIMING ANALYSIS
    print("\n" + "-"*80)
    print("2. BREAKOUT TIMING (Temporal Element)")
    print("-"*80)
    
    judas_timing = calc_stats(judas_group, 'minutes_to_breakout')
    cont_timing = calc_stats(continuation_group, 'minutes_to_breakout')
    
    print(f"\nTime to Breakout (Minutes after 01:00):")
    print(f"  {'':20} {'Judas Swings':>15} {'Continuations':>15} {'Difference':>15}")
    print(f"  {'Mean':20} {judas_timing['mean']:>15.2f} {cont_timing['mean']:>15.2f} {cont_timing['mean']-judas_timing['mean']:>15.2f}")
    print(f"  {'Median':20} {judas_timing['median']:>15.2f} {cont_timing['median']:>15.2f} {cont_timing['median']-judas_timing['median']:>15.2f}")
    
    # Early breakouts (within 30 minutes)
    judas_early = len([r for r in judas_group if r['minutes_to_breakout'] <= 30])
    cont_early = len([r for r in continuation_group if r['minutes_to_breakout'] <= 30])
    
    judas_early_pct = (judas_early / len(judas_group) * 100) if len(judas_group) > 0 else 0
    cont_early_pct = (cont_early / len(continuation_group) * 100) if len(continuation_group) > 0 else 0
    
    print(f"\nBreakouts within first 30 minutes:")
    print(f"  Judas Swings:    {judas_early:4d} ({judas_early_pct:.1f}%)")
    print(f"  Continuations:   {cont_early:4d} ({cont_early_pct:.1f}%)")
    
    if judas_early_pct > cont_early_pct:
        print(f"\n  💡 Insight: Early breakouts (0-30min) are MORE likely to be Judas Swings")
        print(f"     ({judas_early_pct:.1f}% vs {cont_early_pct:.1f}%)")
    else:
        print(f"\n  💡 Insight: Early breakouts (0-30min) are MORE likely to be Continuations")
        print(f"     ({cont_early_pct:.1f}% vs {judas_early_pct:.1f}%)")
    
    # 3. VELOCITY ANALYSIS
    print("\n" + "-"*80)
    print("3. MOVEMENT VELOCITY (Impulse Strength)")
    print("-"*80)
    
    judas_vel = calc_stats(judas_group, 'velocity')
    cont_vel = calc_stats(continuation_group, 'velocity')
    
    print(f"\nInitial Extension Velocity (Points/Minute):")
    print(f"  {'':20} {'Judas Swings':>15} {'Continuations':>15} {'Difference':>15}")
    print(f"  {'Mean':20} {judas_vel['mean']:>15.3f} {cont_vel['mean']:>15.3f} {cont_vel['mean']-judas_vel['mean']:>15.3f}")
    print(f"  {'Median':20} {judas_vel['median']:>15.3f} {cont_vel['median']:>15.3f} {cont_vel['median']-judas_vel['median']:>15.3f}")
    
    if cont_vel['mean'] > judas_vel['mean']:
        print(f"\n  💡 Insight: HIGHER velocity indicates Continuation (stronger impulse)")
        print(f"     ({cont_vel['mean']:.2f} vs {judas_vel['mean']:.2f} pts/min)")
    else:
        print(f"\n  💡 Insight: HIGHER velocity indicates Judas Swing (stop hunt)")
        print(f"     ({judas_vel['mean']:.2f} vs {cont_vel['mean']:.2f} pts/min)")
    
    # 4. CONDITIONAL PROBABILITIES
    print("\n" + "-"*80)
    print("4. CONDITIONAL PROBABILITIES")
    print("-"*80)
    
    # Small Tokyo Range
    small_range_threshold = 20
    small_range_judas = [r for r in judas_group if r['tokyo_range'] < small_range_threshold]
    small_range_cont = [r for r in continuation_group if r['tokyo_range'] < small_range_threshold]
    total_small_range = len(small_range_judas) + len(small_range_cont)
    
    if total_small_range > 0:
        cont_prob_small = len(small_range_cont) / total_small_range * 100
        print(f"\nIf Tokyo Range < {small_range_threshold} points:")
        print(f"  Continuation probability: {cont_prob_small:.1f}%")
        print(f"  Judas Swing probability:  {100-cont_prob_small:.1f}%")
        print(f"  (Based on {total_small_range} occurrences)")
    
    # Large Tokyo Range
    large_range_threshold = 60
    large_range_judas = [r for r in judas_group if r['tokyo_range'] >= large_range_threshold]
    large_range_cont = [r for r in continuation_group if r['tokyo_range'] >= large_range_threshold]
    total_large_range = len(large_range_judas) + len(large_range_cont)
    
    if total_large_range > 0:
        cont_prob_large = len(large_range_cont) / total_large_range * 100
        print(f"\nIf Tokyo Range >= {large_range_threshold} points:")
        print(f"  Continuation probability: {cont_prob_large:.1f}%")
        print(f"  Judas Swing probability:  {100-cont_prob_large:.1f}%")
        print(f"  (Based on {total_large_range} occurrences)")
    
    # Early breakout (within 15 minutes)
    early_threshold = 15
    early_judas = [r for r in judas_group if r['minutes_to_breakout'] <= early_threshold]
    early_cont = [r for r in continuation_group if r['minutes_to_breakout'] <= early_threshold]
    total_early = len(early_judas) + len(early_cont)
    
    if total_early > 0:
        cont_prob_early = len(early_cont) / total_early * 100
        print(f"\nIf Breakout occurs within {early_threshold} minutes:")
        print(f"  Continuation probability: {cont_prob_early:.1f}%")
        print(f"  Judas Swing probability:  {100-cont_prob_early:.1f}%")
        print(f"  (Based on {total_early} occurrences)")
    
    # High velocity
    high_vel_threshold = np.percentile([r['velocity'] for r in valid_results], 75)
    high_vel_judas = [r for r in judas_group if r['velocity'] >= high_vel_threshold]
    high_vel_cont = [r for r in continuation_group if r['velocity'] >= high_vel_threshold]
    total_high_vel = len(high_vel_judas) + len(high_vel_cont)
    
    if total_high_vel > 0:
        cont_prob_high_vel = len(high_vel_cont) / total_high_vel * 100
        print(f"\nIf Velocity >= {high_vel_threshold:.2f} pts/min (top 25%):")
        print(f"  Continuation probability: {cont_prob_high_vel:.1f}%")
        print(f"  Judas Swing probability:  {100-cont_prob_high_vel:.1f}%")
        print(f"  (Based on {total_high_vel} occurrences)")
    
    # 5. COMBINED FACTORS
    print("\n" + "-"*80)
    print("5. MULTI-FACTOR SCENARIOS")
    print("-"*80)
    
    # Scenario 1: Large range + Early breakout
    scenario1_judas = [r for r in judas_group 
                       if r['tokyo_range'] >= large_range_threshold 
                       and r['minutes_to_breakout'] <= early_threshold]
    scenario1_cont = [r for r in continuation_group 
                      if r['tokyo_range'] >= large_range_threshold 
                      and r['minutes_to_breakout'] <= early_threshold]
    total_scenario1 = len(scenario1_judas) + len(scenario1_cont)
    
    if total_scenario1 > 0:
        cont_prob_s1 = len(scenario1_cont) / total_scenario1 * 100
        print(f"\nScenario 1: Large Range (>={large_range_threshold}pts) + Early Breakout (<={early_threshold}min)")
        print(f"  Continuation probability: {cont_prob_s1:.1f}%")
        print(f"  Judas Swing probability:  {100-cont_prob_s1:.1f}%")
        print(f"  (Based on {total_scenario1} occurrences)")
    
    # Scenario 2: Small range + High velocity
    scenario2_judas = [r for r in judas_group 
                       if r['tokyo_range'] < small_range_threshold 
                       and r['velocity'] >= high_vel_threshold]
    scenario2_cont = [r for r in continuation_group 
                      if r['tokyo_range'] < small_range_threshold 
                      and r['velocity'] >= high_vel_threshold]
    total_scenario2 = len(scenario2_judas) + len(scenario2_cont)
    
    if total_scenario2 > 0:
        cont_prob_s2 = len(scenario2_cont) / total_scenario2 * 100
        print(f"\nScenario 2: Small Range (<{small_range_threshold}pts) + High Velocity (top 25%)")
        print(f"  Continuation probability: {cont_prob_s2:.1f}%")
        print(f"  Judas Swing probability:  {100-cont_prob_s2:.1f}%")
        print(f"  (Based on {total_scenario2} occurrences)")
    
    print("\n" + "="*80)


def main():
    """
    Main execution function
    
    Loads NQ 1-minute data, identifies Tokyo-London sessions, analyzes breakout patterns,
    and displays predictive statistics comparing Judas Swings vs Continuations.
    
    Command-line usage:
        python tokyo_london_predictive_analysis.py [data_path]
        
    Environment variable:
        BACKTEST_DATA_PATH: Path to data directory
    """
    start_time = datetime.now()
    
    # Set base path
    if len(sys.argv) > 1:
        base_path = sys.argv[1]
    else:
        base_path = os.environ.get('BACKTEST_DATA_PATH', 
                                   '/home/runner/work/Backtest-Trading/Backtest-Trading')
        if not os.path.exists(base_path):
            base_path = os.getcwd()
    
    print(f"Data path: {base_path}")
    
    # Load data
    df = load_nq_data(base_path)
    
    # Identify sessions
    sessions = identify_sessions(df)
    
    # Analyze each session with detailed metrics
    print("\nAnalyzing sessions with predictive metrics...")
    results = []
    for i, session in enumerate(sessions):
        if i % 100 == 0:
            print(f"  Processing session {i+1}/{len(sessions)}")
        result = analyze_session_detailed(session)
        results.append(result)
    
    # Calculate and display predictive statistics
    calculate_predictive_statistics(results)
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    print(f"\nExecution time: {duration:.2f} seconds")
    print(f"Processing speed: {len(df)/duration:,.0f} rows/second")


if __name__ == "__main__":
    main()

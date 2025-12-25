#!/usr/bin/env python3
"""
Predictive Analysis: Judas Swing vs Continuation
Advanced comparative analysis to identify predictive factors for pattern anticipation.

Author: Senior Quantitative Trading Expert
Date: 2025-12-25
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import zipfile
import os
import argparse
from typing import List, Tuple, Dict

# Trading Session Constants
TOKYO_SESSION_START = 17  # 17:00 previous day
TOKYO_SESSION_END = 24    # 24:00 previous day (midnight)
LONDON_KILLZONE_START = 1 # 01:00 current day
LONDON_KILLZONE_END = 5   # 05:00 current day

# Data Format Constants
DEFAULT_CSV_SEPARATOR = ';'
DEFAULT_DATETIME_FORMAT = '%d/%m/%Y %H:%M:%S'


def load_csv_data(file_path: str, separator: str = DEFAULT_CSV_SEPARATOR) -> pd.DataFrame:
    """Load CSV data from either a regular CSV file or a ZIP archive."""
    try:
        if file_path.endswith('.zip'):
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                system_prefixes = ('.', '__MACOSX', 'System Volume Information', '$RECYCLE.BIN')
                csv_files = [f for f in zip_ref.namelist() 
                           if f.endswith('.csv') and not any(f.startswith(prefix) for prefix in system_prefixes)]
                if not csv_files:
                    raise ValueError(f"No CSV file found in {file_path}")
                
                csv_file = csv_files[0]
                with zip_ref.open(csv_file) as f:
                    df = pd.read_csv(f, sep=separator, header=0)
        else:
            df = pd.read_csv(file_path, sep=separator, header=0)
        
        return df
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return None


def prepare_dataframe(df: pd.DataFrame, datetime_format: str = DEFAULT_DATETIME_FORMAT) -> pd.DataFrame:
    """Prepare the dataframe by renaming columns and creating datetime index."""
    column_mapping = {
        'Column1': 'Date',
        'Column2': 'Time',
        'Column3': 'Open',
        'Column4': 'High',
        'Column5': 'Low',
        'Column6': 'Close',
        'Column7': 'Volume'
    }
    
    if 'Column1' in df.columns:
        df = df.rename(columns=column_mapping)
    
    try:
        df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format=datetime_format)
    except Exception:
        df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])
    
    df = df.sort_values('DateTime').reset_index(drop=True)
    return df


def load_all_data(data_dir: str, years: List[int]) -> pd.DataFrame:
    """Load and combine data from multiple years."""
    all_data = []
    
    for year in years:
        zip_path = os.path.join(data_dir, f"{year} 1m.csv.zip")
        csv_path = os.path.join(data_dir, f"{year} 1m.csv")
        
        if os.path.exists(zip_path):
            print(f"Loading {year} data from ZIP...")
            df = load_csv_data(zip_path)
        elif os.path.exists(csv_path):
            print(f"Loading {year} data from CSV...")
            df = load_csv_data(csv_path)
        else:
            print(f"Warning: No data file found for year {year}")
            continue
        
        if df is not None and len(df) > 0:
            df = prepare_dataframe(df)
            all_data.append(df)
            print(f"  Loaded {len(df)} rows for {year}")
    
    if not all_data:
        raise ValueError("No data loaded!")
    
    combined_df = pd.concat(all_data, ignore_index=True)
    combined_df = combined_df.sort_values('DateTime').reset_index(drop=True)
    
    print(f"\nTotal rows loaded: {len(combined_df)}")
    print(f"Date range: {combined_df['DateTime'].min()} to {combined_df['DateTime'].max()}")
    
    return combined_df


def analyze_session(df: pd.DataFrame, date: datetime) -> Dict:
    """
    Comprehensive analysis of a single trading session.
    Returns detailed metrics for both Tokyo session and London Killzone.
    """
    prev_date = date - timedelta(days=1)
    
    # Tokyo Session (previous day 17:00-24:00)
    tokyo_start = pd.Timestamp(prev_date.date()) + pd.Timedelta(hours=TOKYO_SESSION_START)
    tokyo_end = pd.Timestamp(prev_date.date()) + pd.Timedelta(hours=TOKYO_SESSION_END)
    tokyo_data = df[(df['DateTime'] >= tokyo_start) & (df['DateTime'] < tokyo_end)]
    
    if len(tokyo_data) == 0:
        return None
    
    # Tokyo metrics
    tokyo_high = tokyo_data['High'].max()
    tokyo_low = tokyo_data['Low'].min()
    tokyo_eq = (tokyo_high + tokyo_low) / 2
    tokyo_range = tokyo_high - tokyo_low
    
    # Price at end of Tokyo session (close to 01:00)
    tokyo_close = tokyo_data.iloc[-1]['Close']
    tokyo_close_position = (tokyo_close - tokyo_low) / tokyo_range if tokyo_range > 0 else 0.5
    
    # London Killzone (current day 01:00-05:00)
    killzone_start = pd.Timestamp(date.date()) + pd.Timedelta(hours=LONDON_KILLZONE_START)
    killzone_end = pd.Timestamp(date.date()) + pd.Timedelta(hours=LONDON_KILLZONE_END)
    killzone_data = df[(df['DateTime'] >= killzone_start) & (df['DateTime'] < killzone_end)]
    
    if len(killzone_data) == 0:
        return None
    
    # Check for breakouts
    broke_high = killzone_data['High'].max() > tokyo_high
    broke_low = killzone_data['Low'].min() < tokyo_low
    
    # Initialize result
    result = {
        'date': date,
        'tokyo_range': tokyo_range,
        'tokyo_close_position': tokyo_close_position,
        'broke_high': broke_high,
        'broke_low': broke_low,
        'pattern_type': None,  # Will be 'judas_swing' or 'continuation' or 'no_break' or 'both_sides'
        'breakout_time_minutes': None,
        'peak_size': None,
        'velocity': None,  # Points per minute
        'eq_touched': False
    }
    
    # No breakout at all
    if not broke_high and not broke_low:
        result['pattern_type'] = 'no_break'
        return result
    
    # Both sides broken (ambiguous)
    if broke_high and broke_low:
        result['pattern_type'] = 'both_sides'
        return result
    
    # Single side breakout - analyze in detail
    if broke_high:
        # Break above Tokyo High
        peak_idx = killzone_data['High'].idxmax()
        peak_value = killzone_data.loc[peak_idx, 'High']
        peak_time = killzone_data.loc[peak_idx, 'DateTime']
        result['peak_size'] = peak_value - tokyo_high
        
        # Time to breakout (when price first exceeds Tokyo High)
        breakout_candles = killzone_data[killzone_data['High'] > tokyo_high]
        if len(breakout_candles) > 0:
            breakout_time = breakout_candles.iloc[0]['DateTime']
            result['breakout_time_minutes'] = (breakout_time - killzone_start).total_seconds() / 60
            
            # Velocity calculation (peak size / time to peak)
            time_to_peak = (peak_time - breakout_time).total_seconds() / 60
            if time_to_peak > 0:
                result['velocity'] = result['peak_size'] / time_to_peak
            else:
                result['velocity'] = result['peak_size']  # Immediate peak
        
        # Check if EQ touched after peak
        data_after_peak = killzone_data[killzone_data['DateTime'] > peak_time]
        if len(data_after_peak) > 0:
            eq_touched = (data_after_peak['Low'] <= tokyo_eq).any()
            result['eq_touched'] = eq_touched
            result['pattern_type'] = 'judas_swing' if eq_touched else 'continuation'
        else:
            result['pattern_type'] = 'continuation'
            
    elif broke_low:
        # Break below Tokyo Low
        peak_idx = killzone_data['Low'].idxmin()
        peak_value = killzone_data.loc[peak_idx, 'Low']
        peak_time = killzone_data.loc[peak_idx, 'DateTime']
        result['peak_size'] = tokyo_low - peak_value
        
        # Time to breakout (when price first breaks Tokyo Low)
        breakout_candles = killzone_data[killzone_data['Low'] < tokyo_low]
        if len(breakout_candles) > 0:
            breakout_time = breakout_candles.iloc[0]['DateTime']
            result['breakout_time_minutes'] = (breakout_time - killzone_start).total_seconds() / 60
            
            # Velocity calculation
            time_to_peak = (peak_time - breakout_time).total_seconds() / 60
            if time_to_peak > 0:
                result['velocity'] = result['peak_size'] / time_to_peak
            else:
                result['velocity'] = result['peak_size']
        
        # Check if EQ touched after peak
        data_after_peak = killzone_data[killzone_data['DateTime'] > peak_time]
        if len(data_after_peak) > 0:
            eq_touched = (data_after_peak['High'] >= tokyo_eq).any()
            result['eq_touched'] = eq_touched
            result['pattern_type'] = 'judas_swing' if eq_touched else 'continuation'
        else:
            result['pattern_type'] = 'continuation'
    
    return result


def run_comparative_analysis(df: pd.DataFrame) -> Dict:
    """
    Run comprehensive comparative analysis between Judas Swings and Continuations.
    """
    df['Date_only'] = df['DateTime'].dt.date
    unique_dates = sorted(df['Date_only'].unique())
    
    print(f"\nAnalyzing {len(unique_dates)} trading days...")
    
    all_sessions = []
    
    for i, date in enumerate(unique_dates):
        if i == 0:
            continue  # Skip first day (need previous day for Tokyo)
        
        current_date = pd.Timestamp(date)
        session_result = analyze_session(df, current_date)
        
        if session_result is not None:
            all_sessions.append(session_result)
        
        if (len(all_sessions) % 100) == 0:
            print(f"  Processed {len(all_sessions)} sessions...")
    
    # Convert to DataFrame for easier analysis
    sessions_df = pd.DataFrame(all_sessions)
    
    # Separate into groups
    judas_swings = sessions_df[sessions_df['pattern_type'] == 'judas_swing']
    continuations = sessions_df[sessions_df['pattern_type'] == 'continuation']
    
    print(f"\nTotal sessions with single-side breakout: {len(judas_swings) + len(continuations)}")
    print(f"  Judas Swings (Group A): {len(judas_swings)}")
    print(f"  Continuations (Group B): {len(continuations)}")
    print(f"  No Break: {len(sessions_df[sessions_df['pattern_type'] == 'no_break'])}")
    print(f"  Both Sides: {len(sessions_df[sessions_df['pattern_type'] == 'both_sides'])}")
    
    return {
        'all_sessions': sessions_df,
        'judas_swings': judas_swings,
        'continuations': continuations
    }


def calculate_comparative_metrics(judas_swings: pd.DataFrame, continuations: pd.DataFrame) -> Dict:
    """
    Calculate and compare key metrics between Judas Swings and Continuations.
    """
    metrics = {}
    
    # 1. Tokyo Range Analysis
    metrics['tokyo_range'] = {
        'judas_mean': judas_swings['tokyo_range'].mean(),
        'judas_median': judas_swings['tokyo_range'].median(),
        'continuation_mean': continuations['tokyo_range'].mean(),
        'continuation_median': continuations['tokyo_range'].median()
    }
    
    # 2. Tokyo Close Position (0=Low, 1=High)
    metrics['tokyo_close_position'] = {
        'judas_mean': judas_swings['tokyo_close_position'].mean(),
        'judas_median': judas_swings['tokyo_close_position'].median(),
        'continuation_mean': continuations['tokyo_close_position'].mean(),
        'continuation_median': continuations['tokyo_close_position'].median()
    }
    
    # 3. Breakout Timing (minutes after 01:00)
    judas_with_time = judas_swings[judas_swings['breakout_time_minutes'].notna()]
    cont_with_time = continuations[continuations['breakout_time_minutes'].notna()]
    
    metrics['breakout_timing'] = {
        'judas_mean': judas_with_time['breakout_time_minutes'].mean(),
        'judas_median': judas_with_time['breakout_time_minutes'].median(),
        'continuation_mean': cont_with_time['breakout_time_minutes'].mean(),
        'continuation_median': cont_with_time['breakout_time_minutes'].median()
    }
    
    # Early breakout analysis (first 30 minutes)
    judas_early = (judas_with_time['breakout_time_minutes'] <= 30).sum()
    cont_early = (cont_with_time['breakout_time_minutes'] <= 30).sum()
    
    metrics['early_breakout_pct'] = {
        'judas': (judas_early / len(judas_with_time) * 100) if len(judas_with_time) > 0 else 0,
        'continuation': (cont_early / len(cont_with_time) * 100) if len(cont_with_time) > 0 else 0
    }
    
    # 4. Velocity Analysis (Points per minute)
    judas_with_vel = judas_swings[judas_swings['velocity'].notna()]
    cont_with_vel = continuations[continuations['velocity'].notna()]
    
    metrics['velocity'] = {
        'judas_mean': judas_with_vel['velocity'].mean(),
        'judas_median': judas_with_vel['velocity'].median(),
        'continuation_mean': cont_with_vel['velocity'].mean(),
        'continuation_median': cont_with_vel['velocity'].median()
    }
    
    # 5. Peak Size Analysis
    judas_with_peak = judas_swings[judas_swings['peak_size'].notna()]
    cont_with_peak = continuations[continuations['peak_size'].notna()]
    
    metrics['peak_size'] = {
        'judas_mean': judas_with_peak['peak_size'].mean(),
        'judas_median': judas_with_peak['peak_size'].median(),
        'continuation_mean': cont_with_peak['peak_size'].mean(),
        'continuation_median': cont_with_peak['peak_size'].median()
    }
    
    return metrics


def calculate_conditional_probabilities(judas_swings: pd.DataFrame, continuations: pd.DataFrame) -> Dict:
    """
    Calculate conditional probabilities for different scenarios.
    """
    probs = {}
    
    # Total breakouts (single side)
    total = len(judas_swings) + len(continuations)
    
    # Base rates
    probs['base_rate_judas'] = len(judas_swings) / total * 100 if total > 0 else 0
    probs['base_rate_continuation'] = len(continuations) / total * 100 if total > 0 else 0
    
    # Conditional: Tokyo Range < 20 points
    small_range_threshold = 20
    judas_small_range = judas_swings[judas_swings['tokyo_range'] < small_range_threshold]
    cont_small_range = continuations[continuations['tokyo_range'] < small_range_threshold]
    total_small_range = len(judas_small_range) + len(cont_small_range)
    
    probs['tokyo_range_lt_20'] = {
        'continuation_prob': (len(cont_small_range) / total_small_range * 100) if total_small_range > 0 else 0,
        'judas_prob': (len(judas_small_range) / total_small_range * 100) if total_small_range > 0 else 0,
        'sample_size': total_small_range
    }
    
    # Conditional: Tokyo Range > 50 points
    large_range_threshold = 50
    judas_large_range = judas_swings[judas_swings['tokyo_range'] > large_range_threshold]
    cont_large_range = continuations[continuations['tokyo_range'] > large_range_threshold]
    total_large_range = len(judas_large_range) + len(cont_large_range)
    
    probs['tokyo_range_gt_50'] = {
        'continuation_prob': (len(cont_large_range) / total_large_range * 100) if total_large_range > 0 else 0,
        'judas_prob': (len(judas_large_range) / total_large_range * 100) if total_large_range > 0 else 0,
        'sample_size': total_large_range
    }
    
    # Conditional: Early breakout (first 15 minutes)
    judas_with_time = judas_swings[judas_swings['breakout_time_minutes'].notna()]
    cont_with_time = continuations[continuations['breakout_time_minutes'].notna()]
    
    judas_early_15 = judas_with_time[judas_with_time['breakout_time_minutes'] <= 15]
    cont_early_15 = cont_with_time[cont_with_time['breakout_time_minutes'] <= 15]
    total_early_15 = len(judas_early_15) + len(cont_early_15)
    
    probs['early_breakout_15min'] = {
        'continuation_prob': (len(cont_early_15) / total_early_15 * 100) if total_early_15 > 0 else 0,
        'judas_prob': (len(judas_early_15) / total_early_15 * 100) if total_early_15 > 0 else 0,
        'sample_size': total_early_15
    }
    
    # Conditional: Close position near extremes (> 0.8 or < 0.2)
    judas_extreme_close = judas_swings[(judas_swings['tokyo_close_position'] > 0.8) | 
                                       (judas_swings['tokyo_close_position'] < 0.2)]
    cont_extreme_close = continuations[(continuations['tokyo_close_position'] > 0.8) | 
                                       (continuations['tokyo_close_position'] < 0.2)]
    total_extreme = len(judas_extreme_close) + len(cont_extreme_close)
    
    probs['extreme_close_position'] = {
        'continuation_prob': (len(cont_extreme_close) / total_extreme * 100) if total_extreme > 0 else 0,
        'judas_prob': (len(judas_extreme_close) / total_extreme * 100) if total_extreme > 0 else 0,
        'sample_size': total_extreme
    }
    
    return probs


def print_comparative_report(metrics: Dict, probs: Dict):
    """
    Print a comprehensive comparative report.
    """
    print("\n" + "="*80)
    print(" PREDICTIVE ANALYSIS: JUDAS SWING vs CONTINUATION")
    print("="*80)
    
    print("\n" + "-"*80)
    print(" 1. TOKYO RANGE ANALYSIS (Pre-Breakout Context)")
    print("-"*80)
    print(f"{'Metric':<40} {'Judas Swing':>18} {'Continuation':>18}")
    print("-"*80)
    print(f"{'Average Tokyo Range (points)':<40} {metrics['tokyo_range']['judas_mean']:>18.2f} {metrics['tokyo_range']['continuation_mean']:>18.2f}")
    print(f"{'Median Tokyo Range (points)':<40} {metrics['tokyo_range']['judas_median']:>18.2f} {metrics['tokyo_range']['continuation_median']:>18.2f}")
    
    diff_pct = ((metrics['tokyo_range']['judas_mean'] - metrics['tokyo_range']['continuation_mean']) / 
                metrics['tokyo_range']['continuation_mean'] * 100)
    print(f"\n→ Judas Swings occur with Tokyo ranges {abs(diff_pct):.1f}% {'larger' if diff_pct > 0 else 'smaller'} on average")
    
    print("\n" + "-"*80)
    print(" 2. TOKYO CLOSE POSITION (0=Low, 1=High)")
    print("-"*80)
    print(f"{'Metric':<40} {'Judas Swing':>18} {'Continuation':>18}")
    print("-"*80)
    print(f"{'Average Close Position':<40} {metrics['tokyo_close_position']['judas_mean']:>18.3f} {metrics['tokyo_close_position']['continuation_mean']:>18.3f}")
    print(f"{'Median Close Position':<40} {metrics['tokyo_close_position']['judas_median']:>18.3f} {metrics['tokyo_close_position']['continuation_median']:>18.3f}")
    
    if metrics['tokyo_close_position']['judas_mean'] > 0.6:
        print(f"\n→ Judas Swings tend to close near the top of Tokyo range (bias towards upper extreme)")
    elif metrics['tokyo_close_position']['judas_mean'] < 0.4:
        print(f"\n→ Judas Swings tend to close near the bottom of Tokyo range (bias towards lower extreme)")
    else:
        print(f"\n→ Judas Swings show balanced close positions within Tokyo range")
    
    print("\n" + "-"*80)
    print(" 3. BREAKOUT TIMING (Minutes after 01:00)")
    print("-"*80)
    print(f"{'Metric':<40} {'Judas Swing':>18} {'Continuation':>18}")
    print("-"*80)
    print(f"{'Average Breakout Time (minutes)':<40} {metrics['breakout_timing']['judas_mean']:>18.2f} {metrics['breakout_timing']['continuation_mean']:>18.2f}")
    print(f"{'Median Breakout Time (minutes)':<40} {metrics['breakout_timing']['judas_median']:>18.2f} {metrics['breakout_timing']['continuation_median']:>18.2f}")
    print(f"{'% Breaking in First 30 minutes':<40} {metrics['early_breakout_pct']['judas']:>18.1f} {metrics['early_breakout_pct']['continuation']:>18.1f}")
    
    if metrics['breakout_timing']['judas_mean'] < metrics['breakout_timing']['continuation_mean']:
        print(f"\n→ Judas Swings tend to break EARLIER than Continuations")
    else:
        print(f"\n→ Continuations tend to break EARLIER than Judas Swings")
    
    print("\n" + "-"*80)
    print(" 4. VELOCITY ANALYSIS (Points per Minute)")
    print("-"*80)
    print(f"{'Metric':<40} {'Judas Swing':>18} {'Continuation':>18}")
    print("-"*80)
    print(f"{'Average Velocity (pts/min)':<40} {metrics['velocity']['judas_mean']:>18.2f} {metrics['velocity']['continuation_mean']:>18.2f}")
    print(f"{'Median Velocity (pts/min)':<40} {metrics['velocity']['judas_median']:>18.2f} {metrics['velocity']['continuation_median']:>18.2f}")
    
    vel_diff_pct = ((metrics['velocity']['judas_mean'] - metrics['velocity']['continuation_mean']) / 
                    metrics['velocity']['continuation_mean'] * 100)
    if abs(vel_diff_pct) > 10:
        print(f"\n→ {'Judas Swings' if vel_diff_pct > 0 else 'Continuations'} show {abs(vel_diff_pct):.1f}% higher velocity")
        print(f"   {'Rapid spikes may indicate stop-hunting behavior (Judas)' if vel_diff_pct > 0 else 'Sustained momentum suggests genuine directional move (Continuation)'}")
    else:
        print(f"\n→ Velocity is similar between patterns (difference: {abs(vel_diff_pct):.1f}%)")
    
    print("\n" + "-"*80)
    print(" 5. PEAK SIZE ANALYSIS")
    print("-"*80)
    print(f"{'Metric':<40} {'Judas Swing':>18} {'Continuation':>18}")
    print("-"*80)
    print(f"{'Average Peak Size (points)':<40} {metrics['peak_size']['judas_mean']:>18.2f} {metrics['peak_size']['continuation_mean']:>18.2f}")
    print(f"{'Median Peak Size (points)':<40} {metrics['peak_size']['judas_median']:>18.2f} {metrics['peak_size']['continuation_median']:>18.2f}")
    
    print("\n" + "="*80)
    print(" CONDITIONAL PROBABILITIES")
    print("="*80)
    
    print(f"\nBase Rates:")
    print(f"  Judas Swing:   {probs['base_rate_judas']:.2f}%")
    print(f"  Continuation:  {probs['base_rate_continuation']:.2f}%")
    
    print(f"\n" + "-"*80)
    print(f"Scenario 1: Tokyo Range < 20 points (n={probs['tokyo_range_lt_20']['sample_size']})")
    print(f"  → Continuation Probability: {probs['tokyo_range_lt_20']['continuation_prob']:.2f}%")
    print(f"  → Judas Swing Probability:  {probs['tokyo_range_lt_20']['judas_prob']:.2f}%")
    
    print(f"\n" + "-"*80)
    print(f"Scenario 2: Tokyo Range > 50 points (n={probs['tokyo_range_gt_50']['sample_size']})")
    print(f"  → Continuation Probability: {probs['tokyo_range_gt_50']['continuation_prob']:.2f}%")
    print(f"  → Judas Swing Probability:  {probs['tokyo_range_gt_50']['judas_prob']:.2f}%")
    
    print(f"\n" + "-"*80)
    print(f"Scenario 3: Breakout in First 15 minutes (n={probs['early_breakout_15min']['sample_size']})")
    print(f"  → Continuation Probability: {probs['early_breakout_15min']['continuation_prob']:.2f}%")
    print(f"  → Judas Swing Probability:  {probs['early_breakout_15min']['judas_prob']:.2f}%")
    
    print(f"\n" + "-"*80)
    print(f"Scenario 4: Tokyo Close at Extremes (>80% or <20%) (n={probs['extreme_close_position']['sample_size']})")
    print(f"  → Continuation Probability: {probs['extreme_close_position']['continuation_prob']:.2f}%")
    print(f"  → Judas Swing Probability:  {probs['extreme_close_position']['judas_prob']:.2f}%")
    
    print("\n" + "="*80)
    print(" KEY INSIGHTS FOR ANTICIPATION")
    print("="*80)
    
    # Generate insights based on the data
    insights = []
    
    # Range insight
    if abs(diff_pct) > 15:
        if diff_pct > 0:
            insights.append("• Larger Tokyo ranges are associated with Judas Swings")
        else:
            insights.append("• Smaller Tokyo ranges are associated with Judas Swings")
    
    # Timing insight
    if abs(metrics['breakout_timing']['judas_mean'] - metrics['breakout_timing']['continuation_mean']) > 10:
        if metrics['breakout_timing']['judas_mean'] < metrics['breakout_timing']['continuation_mean']:
            insights.append("• Earlier breakouts (first 30min) tend to be Judas Swings")
        else:
            insights.append("• Later breakouts tend to be Judas Swings")
    
    # Velocity insight
    if abs(vel_diff_pct) > 15:
        if vel_diff_pct > 0:
            insights.append("• Higher velocity spikes suggest Judas Swing (stop hunt)")
        else:
            insights.append("• Higher velocity suggests Continuation (genuine momentum)")
    
    # Conditional probability insights
    if probs['tokyo_range_lt_20']['continuation_prob'] > 70:
        insights.append("• Small Tokyo ranges (<20pts) strongly favor Continuations")
    elif probs['tokyo_range_lt_20']['judas_prob'] > 50:
        insights.append("• Small Tokyo ranges (<20pts) favor Judas Swings")
    
    if len(insights) > 0:
        for insight in insights:
            print(insight)
    else:
        print("• Patterns show similar characteristics - additional factors needed")
    
    print("\n" + "="*80)


def main():
    """Main function to run the predictive analysis."""
    parser = argparse.ArgumentParser(description='Predictive Analysis: Judas Swing vs Continuation')
    parser.add_argument('--data-dir', type=str, 
                       default=os.path.dirname(os.path.abspath(__file__)) or '.',
                       help='Directory containing the data files')
    parser.add_argument('--years', type=int, nargs='+',
                       default=[2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025],
                       help='Years to analyze (default: 2018-2025)')
    args = parser.parse_args()
    
    print("="*80)
    print(" PREDICTIVE ANALYSIS: JUDAS SWING vs CONTINUATION")
    print(" NQ (Nasdaq Futures) - 1 Minute Data")
    print("="*80)
    
    try:
        # Load data
        print("\nStep 1: Loading data...")
        df = load_all_data(args.data_dir, args.years)
        
        # Run comparative analysis
        print("\nStep 2: Running comparative analysis...")
        results = run_comparative_analysis(df)
        
        # Calculate metrics
        print("\nStep 3: Calculating comparative metrics...")
        metrics = calculate_comparative_metrics(results['judas_swings'], results['continuations'])
        
        # Calculate conditional probabilities
        print("\nStep 4: Calculating conditional probabilities...")
        probs = calculate_conditional_probabilities(results['judas_swings'], results['continuations'])
        
        # Print report
        print("\nStep 5: Generating comparative report...")
        print_comparative_report(metrics, probs)
        
        print("\n✓ Analysis completed successfully!")
        
    except Exception as e:
        print(f"\n✗ Error during analysis: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())

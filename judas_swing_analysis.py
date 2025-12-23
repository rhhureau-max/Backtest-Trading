#!/usr/bin/env python3
"""
Judas Swing Analysis for NQ (Nasdaq Futures)
Analyzes Tokyo-London session manipulation patterns from 2018 to present

This script performs statistical analysis ONLY - no trading logic applied.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, time
import glob

# Constants for session times (no timezone conversion - using timestamps as-is)
TOKYO_START = time(19, 0)  # 19:00
TOKYO_END = time(0, 0)     # 00:00 (midnight)
LONDON_START = time(1, 0)   # 01:00
LONDON_END = time(5, 0)     # 05:00


def load_nq_data(base_path, years, timeframe='15m'):
    """
    Load NQ futures data from CSV files for specified years and timeframe.
    
    Args:
        base_path: Path to directory containing CSV files
        years: List of years to load
        timeframe: Timeframe of data (e.g., '15m', '5m', '1H')
    
    Returns:
        DataFrame with combined data
    """
    all_data = []
    
    for year in years:
        file_pattern = f"{year} {timeframe}.csv"
        file_path = Path(base_path) / file_pattern
        
        if not file_path.exists():
            print(f"Warning: File not found: {file_path}")
            continue
        
        print(f"Loading {file_path}...")
        
        # Read CSV with semicolon delimiter
        df = pd.read_csv(
            file_path,
            sep=';',
            header=0,
            names=['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume'],
            skiprows=1  # Skip header row
        )
        
        # Parse datetime
        df['DateTime'] = pd.to_datetime(
            df['Date'] + ' ' + df['Time'],
            format='%d/%m/%Y %H:%M:%S'
        )
        
        # Extract time component for session filtering
        df['TimeOnly'] = df['DateTime'].dt.time
        df['DateOnly'] = df['DateTime'].dt.date
        
        all_data.append(df)
    
    if not all_data:
        raise ValueError("No data loaded. Check file paths and years.")
    
    # Combine all years
    combined_df = pd.concat(all_data, ignore_index=True)
    combined_df = combined_df.sort_values('DateTime').reset_index(drop=True)
    
    print(f"\nTotal records loaded: {len(combined_df)}")
    print(f"Date range: {combined_df['DateTime'].min()} to {combined_df['DateTime'].max()}")
    
    return combined_df


def is_in_tokyo_session(time_obj):
    """Check if a time is within Tokyo session (19:00-00:00)"""
    if TOKYO_START > TOKYO_END:  # Session spans midnight
        return time_obj >= TOKYO_START or time_obj < TOKYO_END
    return TOKYO_START <= time_obj < TOKYO_END


def is_in_london_session(time_obj):
    """Check if a time is within London session (01:00-05:00)"""
    return LONDON_START <= time_obj < LONDON_END


def calculate_tokyo_range(df, date):
    """
    Calculate Tokyo session High, Low, and Range for a given date.
    Tokyo session: 19:00 on the previous day to 00:00 on current date.
    
    Args:
        df: DataFrame with market data
        date: Date for which to calculate Tokyo range
    
    Returns:
        dict with tokyo_high, tokyo_low, tokyo_range
    """
    # Get previous date for Tokyo session start
    prev_date = pd.Timestamp(date) - pd.Timedelta(days=1)
    
    # Filter data for Tokyo session
    # Tokyo session runs from 19:00 previous day to 00:00 current date
    tokyo_data = df[
        ((df['DateOnly'] == prev_date.date()) & (df['TimeOnly'] >= TOKYO_START)) |
        ((df['DateOnly'] == date) & (df['TimeOnly'] < TOKYO_END))
    ]
    
    if tokyo_data.empty:
        return None
    
    tokyo_high = tokyo_data['High'].max()
    tokyo_low = tokyo_data['Low'].min()
    tokyo_range = tokyo_high - tokyo_low
    
    return {
        'tokyo_high': tokyo_high,
        'tokyo_low': tokyo_low,
        'tokyo_range': tokyo_range
    }


def detect_judas_swing(df, date, tokyo_stats):
    """
    Detect Judas Swing during London session for a given date.
    
    A Judas Swing is a manipulation of Tokyo session liquidity during London session,
    characterized by a break of Tokyo High or Low followed by directional extension.
    
    Args:
        df: DataFrame with market data
        date: Date to analyze
        tokyo_stats: Dict with tokyo_high, tokyo_low, tokyo_range
    
    Returns:
        dict with swing details or None if no swing detected
    """
    if tokyo_stats is None:
        return None
    
    # Filter data for London session
    london_data = df[
        (df['DateOnly'] == date) &
        (df['TimeOnly'] >= LONDON_START) &
        (df['TimeOnly'] < LONDON_END)
    ]
    
    if london_data.empty:
        return None
    
    tokyo_high = tokyo_stats['tokyo_high']
    tokyo_low = tokyo_stats['tokyo_low']
    
    london_high = london_data['High'].max()
    london_low = london_data['Low'].min()
    
    # Check for Tokyo High break (bullish manipulation)
    high_break = london_high > tokyo_high
    
    # Check for Tokyo Low break (bearish manipulation)
    low_break = london_low < tokyo_low
    
    # Determine if there's a Judas Swing
    if high_break and not low_break:
        # Bullish manipulation: break above Tokyo High
        amplitude = london_high - tokyo_high
        return {
            'date': date,
            'direction': 'bullish',
            'tokyo_high': tokyo_high,
            'tokyo_low': tokyo_low,
            'tokyo_range': tokyo_stats['tokyo_range'],
            'manipulation_high': london_high,
            'manipulation_low': None,
            'amplitude': amplitude
        }
    elif low_break and not high_break:
        # Bearish manipulation: break below Tokyo Low
        amplitude = tokyo_low - london_low
        return {
            'date': date,
            'direction': 'bearish',
            'tokyo_high': tokyo_high,
            'tokyo_low': tokyo_low,
            'tokyo_range': tokyo_stats['tokyo_range'],
            'manipulation_high': None,
            'manipulation_low': london_low,
            'amplitude': amplitude
        }
    elif high_break and low_break:
        # Both sides broken - prioritize the larger amplitude
        amplitude_high = london_high - tokyo_high
        amplitude_low = tokyo_low - london_low
        
        if amplitude_high >= amplitude_low:
            return {
                'date': date,
                'direction': 'bullish',
                'tokyo_high': tokyo_high,
                'tokyo_low': tokyo_low,
                'tokyo_range': tokyo_stats['tokyo_range'],
                'manipulation_high': london_high,
                'manipulation_low': None,
                'amplitude': amplitude_high
            }
        else:
            return {
                'date': date,
                'direction': 'bearish',
                'tokyo_high': tokyo_high,
                'tokyo_low': tokyo_low,
                'tokyo_range': tokyo_stats['tokyo_range'],
                'manipulation_high': None,
                'manipulation_low': london_low,
                'amplitude': amplitude_low
            }
    
    return None


def analyze_judas_swings(df):
    """
    Perform comprehensive Judas Swing analysis on the dataset.
    
    Args:
        df: DataFrame with market data
    
    Returns:
        DataFrame with detected Judas Swings
    """
    # Get unique dates that have London session data
    london_dates = df[df['TimeOnly'] >= LONDON_START]['DateOnly'].unique()
    
    print(f"\nAnalyzing {len(london_dates)} trading days...")
    
    judas_swings = []
    
    for date in london_dates:
        # Calculate Tokyo session stats
        tokyo_stats = calculate_tokyo_range(df, date)
        
        # Detect Judas Swing
        swing = detect_judas_swing(df, date, tokyo_stats)
        
        if swing is not None:
            judas_swings.append(swing)
    
    if not judas_swings:
        print("No Judas Swings detected in the dataset.")
        return pd.DataFrame()
    
    return pd.DataFrame(judas_swings)


def calculate_statistics(swings_df):
    """
    Calculate comprehensive statistics on detected Judas Swings.
    
    Args:
        swings_df: DataFrame with detected swings
    
    Returns:
        dict with all statistics
    """
    if swings_df.empty:
        return None
    
    stats = {}
    
    # Global statistics
    total_swings = len(swings_df)
    bullish_swings = swings_df[swings_df['direction'] == 'bullish']
    bearish_swings = swings_df[swings_df['direction'] == 'bearish']
    
    stats['total_swings'] = total_swings
    stats['bullish_count'] = len(bullish_swings)
    stats['bearish_count'] = len(bearish_swings)
    
    # Amplitude statistics (all swings)
    amplitudes = swings_df['amplitude']
    stats['amplitude_mean'] = amplitudes.mean()
    stats['amplitude_median'] = amplitudes.median()
    stats['amplitude_min'] = amplitudes.min()
    stats['amplitude_max'] = amplitudes.max()
    stats['amplitude_std'] = amplitudes.std()
    
    # Bullish statistics
    if len(bullish_swings) > 0:
        bull_amp = bullish_swings['amplitude']
        stats['bullish_amplitude_mean'] = bull_amp.mean()
        stats['bullish_amplitude_median'] = bull_amp.median()
        stats['bullish_amplitude_min'] = bull_amp.min()
        stats['bullish_amplitude_max'] = bull_amp.max()
        stats['bullish_amplitude_std'] = bull_amp.std()
    
    # Bearish statistics
    if len(bearish_swings) > 0:
        bear_amp = bearish_swings['amplitude']
        stats['bearish_amplitude_mean'] = bear_amp.mean()
        stats['bearish_amplitude_median'] = bear_amp.median()
        stats['bearish_amplitude_min'] = bear_amp.min()
        stats['bearish_amplitude_max'] = bear_amp.max()
        stats['bearish_amplitude_std'] = bear_amp.std()
    
    # Distribution buckets
    buckets = [0, 5, 10, 15, 20, 25, 30, 50, 100, float('inf')]
    bucket_labels = ['0-5', '5-10', '10-15', '15-20', '20-25', '25-30', '30-50', '50-100', '100+']
    stats['distribution'] = pd.cut(amplitudes, bins=buckets, labels=bucket_labels).value_counts().sort_index()
    
    # Probability thresholds
    stats['prob_above_5'] = (amplitudes > 5).sum() / len(amplitudes) * 100
    stats['prob_above_10'] = (amplitudes > 10).sum() / len(amplitudes) * 100
    stats['prob_above_15'] = (amplitudes > 15).sum() / len(amplitudes) * 100
    stats['prob_above_20'] = (amplitudes > 20).sum() / len(amplitudes) * 100
    
    return stats


def print_report(swings_df, stats, total_days):
    """
    Print comprehensive analysis report.
    
    Args:
        swings_df: DataFrame with detected swings
        stats: Dictionary with calculated statistics
        total_days: Total number of trading days analyzed
    """
    print("\n" + "="*80)
    print("JUDAS SWING ANALYSIS - NASDAQ FUTURES (NQ)")
    print("Statistical Analysis of Tokyo-London Session Manipulation")
    print("="*80)
    
    if swings_df.empty:
        print("\nNo Judas Swings detected in the analyzed period.")
        print(f"Total trading days analyzed: {total_days}")
        return
    
    # Global Results
    print("\n" + "-"*80)
    print("GLOBAL RESULTS")
    print("-"*80)
    print(f"Total trading days analyzed: {total_days}")
    print(f"Judas Swings detected: {stats['total_swings']}")
    print(f"Percentage of days with Judas Swing: {stats['total_swings']/total_days*100:.2f}%")
    print(f"  - Bullish manipulations (Tokyo High break): {stats['bullish_count']}")
    print(f"  - Bearish manipulations (Tokyo Low break): {stats['bearish_count']}")
    
    # Amplitude Statistics (All Swings)
    print("\n" + "-"*80)
    print("AMPLITUDE STATISTICS (ALL SWINGS) - in NQ points")
    print("-"*80)
    print(f"Mean amplitude: {stats['amplitude_mean']:.2f} points")
    print(f"Median amplitude: {stats['amplitude_median']:.2f} points")
    print(f"Minimum amplitude: {stats['amplitude_min']:.2f} points")
    print(f"Maximum amplitude: {stats['amplitude_max']:.2f} points")
    print(f"Standard deviation: {stats['amplitude_std']:.2f} points")
    
    # Directional Comparison
    print("\n" + "-"*80)
    print("DIRECTIONAL COMPARISON")
    print("-"*80)
    
    if stats['bullish_count'] > 0:
        print("\nBullish Manipulations (Tokyo High breaks):")
        print(f"  Count: {stats['bullish_count']}")
        print(f"  Mean amplitude: {stats['bullish_amplitude_mean']:.2f} points")
        print(f"  Median amplitude: {stats['bullish_amplitude_median']:.2f} points")
        print(f"  Min amplitude: {stats['bullish_amplitude_min']:.2f} points")
        print(f"  Max amplitude: {stats['bullish_amplitude_max']:.2f} points")
        print(f"  Std deviation: {stats['bullish_amplitude_std']:.2f} points")
    
    if stats['bearish_count'] > 0:
        print("\nBearish Manipulations (Tokyo Low breaks):")
        print(f"  Count: {stats['bearish_count']}")
        print(f"  Mean amplitude: {stats['bearish_amplitude_mean']:.2f} points")
        print(f"  Median amplitude: {stats['bearish_amplitude_median']:.2f} points")
        print(f"  Min amplitude: {stats['bearish_amplitude_min']:.2f} points")
        print(f"  Max amplitude: {stats['bearish_amplitude_max']:.2f} points")
        print(f"  Std deviation: {stats['bearish_amplitude_std']:.2f} points")
    
    # Distribution
    print("\n" + "-"*80)
    print("AMPLITUDE DISTRIBUTION (in NQ points)")
    print("-"*80)
    for bucket, count in stats['distribution'].items():
        percentage = count / stats['total_swings'] * 100
        print(f"{bucket:>8} points: {count:4d} swings ({percentage:5.2f}%)")
    
    # Probability Analysis
    print("\n" + "-"*80)
    print("PROBABILITY ANALYSIS")
    print("-"*80)
    print(f"Probability manipulation exceeds  5 points: {stats['prob_above_5']:.2f}%")
    print(f"Probability manipulation exceeds 10 points: {stats['prob_above_10']:.2f}%")
    print(f"Probability manipulation exceeds 15 points: {stats['prob_above_15']:.2f}%")
    print(f"Probability manipulation exceeds 20 points: {stats['prob_above_20']:.2f}%")
    
    print("\n" + "="*80)
    print("Analysis complete. This is statistical data only - no trading logic applied.")
    print("="*80 + "\n")


def save_results(swings_df, stats, output_path='judas_swing_results.csv'):
    """
    Save detailed results to CSV file.
    
    Args:
        swings_df: DataFrame with detected swings
        stats: Dictionary with statistics
        output_path: Path to output CSV file
    """
    if not swings_df.empty:
        swings_df.to_csv(output_path, index=False)
        print(f"\nDetailed results saved to: {output_path}")


def main():
    """Main execution function"""
    print("="*80)
    print("NQ JUDAS SWING ANALYSIS")
    print("Analyzing Nasdaq Futures from 2018 to present")
    print("="*80)
    
    # Configuration
    base_path = '/home/runner/work/Backtest-Trading/Backtest-Trading'
    years = list(range(2018, 2026))  # 2018 to 2025
    timeframe = '15m'  # Using 15-minute data for precision
    
    # Load data
    print(f"\nLoading {timeframe} data for years: {years}")
    df = load_nq_data(base_path, years, timeframe)
    
    # Get total trading days
    total_days = df['DateOnly'].nunique()
    
    # Analyze Judas Swings
    swings_df = analyze_judas_swings(df)
    
    # Calculate statistics
    if not swings_df.empty:
        stats = calculate_statistics(swings_df)
        
        # Print report
        print_report(swings_df, stats, total_days)
        
        # Save results
        save_results(swings_df, stats)
    else:
        print(f"\nNo Judas Swings detected.")
        print(f"Total trading days analyzed: {total_days}")


if __name__ == "__main__":
    main()

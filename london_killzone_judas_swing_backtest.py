#!/usr/bin/env python3
"""
London Killzone Judas Swing Backtest Script
Analyzes NQ (Nasdaq Futures) 1-minute data for Judas Swing patterns
within the London Killzone based on ICT concepts.

Author: Quantitative Trading Expert
Date: 2025-12-25
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import zipfile
import os
import glob
import argparse
from typing import List, Tuple, Dict

# Trading Session Constants (in hours)
TOKYO_SESSION_START = 17  # 17:00 previous day
TOKYO_SESSION_END = 24    # 24:00 previous day (midnight)
LONDON_KILLZONE_START = 1 # 01:00 current day
LONDON_KILLZONE_END = 5   # 05:00 current day

# Data Format Constants
DEFAULT_CSV_SEPARATOR = ';'
DEFAULT_DATETIME_FORMAT = '%d/%m/%Y %H:%M:%S'


def load_csv_data(file_path: str, separator: str = DEFAULT_CSV_SEPARATOR) -> pd.DataFrame:
    """
    Load CSV data from either a regular CSV file or a ZIP archive.
    
    Args:
        file_path: Path to the CSV or ZIP file
        separator: CSV field separator (default: ';')
        
    Returns:
        DataFrame with the loaded data
    """
    try:
        if file_path.endswith('.zip'):
            # Extract CSV from ZIP file
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                # Get the CSV file name (filter out system files)
                csv_files = [f for f in zip_ref.namelist() 
                           if f.endswith('.csv') and not f.startswith(('.', '__'))]
                if not csv_files:
                    raise ValueError(f"No CSV file found in {file_path}")
                
                csv_file = csv_files[0]
                with zip_ref.open(csv_file) as f:
                    df = pd.read_csv(f, sep=separator, header=0)
        else:
            # Load regular CSV file
            df = pd.read_csv(file_path, sep=separator, header=0)
        
        return df
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return None


def prepare_dataframe(df: pd.DataFrame, datetime_format: str = DEFAULT_DATETIME_FORMAT) -> pd.DataFrame:
    """
    Prepare the dataframe by renaming columns and creating datetime index.
    
    Args:
        df: Raw dataframe
        datetime_format: Format string for parsing datetime (default: '%d/%m/%Y %H:%M:%S')
        
    Returns:
        Processed dataframe with proper datetime index
    """
    # Rename columns to standard names
    column_mapping = {
        'Column1': 'Date',
        'Column2': 'Time',
        'Column3': 'Open',
        'Column4': 'High',
        'Column5': 'Low',
        'Column6': 'Close',
        'Column7': 'Volume'
    }
    
    # Check if columns need renaming
    if 'Column1' in df.columns:
        df = df.rename(columns=column_mapping)
    
    # Create datetime column with error handling
    try:
        df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format=datetime_format)
    except Exception as e:
        print(f"Warning: Failed to parse datetime with format '{datetime_format}', trying automatic detection")
        df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])
    
    # Sort by datetime
    df = df.sort_values('DateTime').reset_index(drop=True)
    
    return df


def load_all_data(data_dir: str, years: List[int]) -> pd.DataFrame:
    """
    Load and combine data from multiple years.
    
    Args:
        data_dir: Directory containing the data files
        years: List of years to load
        
    Returns:
        Combined dataframe
    """
    all_data = []
    
    for year in years:
        # Try both .zip and .csv extensions
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
    
    # Combine all dataframes
    combined_df = pd.concat(all_data, ignore_index=True)
    combined_df = combined_df.sort_values('DateTime').reset_index(drop=True)
    
    print(f"\nTotal rows loaded: {len(combined_df)}")
    print(f"Date range: {combined_df['DateTime'].min()} to {combined_df['DateTime'].max()}")
    
    return combined_df


def get_tokyo_session(df: pd.DataFrame, date: datetime) -> Tuple[float, float, float]:
    """
    Calculate Tokyo session High, Low, and Equilibrium for a given date.
    Tokyo Session: TOKYO_SESSION_START (previous day) to TOKYO_SESSION_END (previous day)
    
    Args:
        df: Dataframe with DateTime index
        date: The date for which to calculate Tokyo session (current day)
        
    Returns:
        Tuple of (Tokyo_High, Tokyo_Low, Tokyo_EQ)
    """
    # Tokyo session is from previous day
    prev_date = date - timedelta(days=1)
    
    tokyo_start = pd.Timestamp(prev_date.date()) + pd.Timedelta(hours=TOKYO_SESSION_START)
    tokyo_end = pd.Timestamp(prev_date.date()) + pd.Timedelta(hours=TOKYO_SESSION_END)
    
    # Filter data for Tokyo session
    tokyo_data = df[(df['DateTime'] >= tokyo_start) & (df['DateTime'] < tokyo_end)]
    
    if len(tokyo_data) == 0:
        return None, None, None
    
    tokyo_high = tokyo_data['High'].max()
    tokyo_low = tokyo_data['Low'].min()
    tokyo_eq = (tokyo_high + tokyo_low) / 2
    
    return tokyo_high, tokyo_low, tokyo_eq


def detect_judas_swing(df: pd.DataFrame, date: datetime, tokyo_high: float, 
                       tokyo_low: float, tokyo_eq: float) -> Dict:
    """
    Detect Judas Swing pattern in the London Killzone.
    
    A Judas Swing occurs when:
    1. Price breaks Tokyo_High OR Tokyo_Low (manipulation)
    2. Price then touches Tokyo_EQ before end of Killzone (retracement)
    
    Args:
        df: Dataframe with price data
        date: Current date
        tokyo_high, tokyo_low, tokyo_eq: Tokyo session levels
        
    Returns:
        Dictionary with detection results
    """
    result = {
        'detected': False,
        'direction': None,  # 'bullish' or 'bearish'
        'peak_size': None,  # Distance beyond Tokyo extreme
        'time_to_peak': None,  # Minutes from Killzone start to peak
        'eq_touched': False
    }
    
    # London Killzone
    killzone_start = pd.Timestamp(date.date()) + pd.Timedelta(hours=LONDON_KILLZONE_START)
    killzone_end = pd.Timestamp(date.date()) + pd.Timedelta(hours=LONDON_KILLZONE_END)
    
    # Filter data for London Killzone
    killzone_data = df[(df['DateTime'] >= killzone_start) & (df['DateTime'] < killzone_end)]
    
    if len(killzone_data) == 0:
        return result
    
    # Check for manipulation (break of Tokyo High or Low)
    broke_high = killzone_data['High'].max() > tokyo_high
    broke_low = killzone_data['Low'].min() < tokyo_low
    
    if not (broke_high or broke_low):
        return result
    
    # Determine direction and find peak
    if broke_high and not broke_low:
        # Bullish manipulation (break above Tokyo High)
        result['direction'] = 'bearish_reversal'  # ICT concept: break high, then reverse down
        peak_idx = killzone_data['High'].idxmax()
        peak_value = killzone_data.loc[peak_idx, 'High']
        result['peak_size'] = peak_value - tokyo_high
        peak_time = killzone_data.loc[peak_idx, 'DateTime']
        
        # Check if EQ was touched AFTER the peak
        data_after_peak = killzone_data[killzone_data['DateTime'] > peak_time]
        if len(data_after_peak) > 0:
            # Check if price touched EQ
            eq_touched = (data_after_peak['Low'] <= tokyo_eq).any()
            result['eq_touched'] = eq_touched
            result['detected'] = eq_touched
            
    elif broke_low and not broke_high:
        # Bearish manipulation (break below Tokyo Low)
        result['direction'] = 'bullish_reversal'  # ICT concept: break low, then reverse up
        peak_idx = killzone_data['Low'].idxmin()
        peak_value = killzone_data.loc[peak_idx, 'Low']
        result['peak_size'] = tokyo_low - peak_value
        peak_time = killzone_data.loc[peak_idx, 'DateTime']
        
        # Check if EQ was touched AFTER the peak
        data_after_peak = killzone_data[killzone_data['DateTime'] > peak_time]
        if len(data_after_peak) > 0:
            # Check if price touched EQ
            eq_touched = (data_after_peak['High'] >= tokyo_eq).any()
            result['eq_touched'] = eq_touched
            result['detected'] = eq_touched
            
    else:
        # Both highs and lows broken - ambiguous, not a clear Judas Swing
        return result
    
    # Calculate time to peak (in minutes from Killzone start)
    if result['detected']:
        time_diff = (peak_time - killzone_start).total_seconds() / 60
        result['time_to_peak'] = time_diff
    
    return result


def run_backtest(df: pd.DataFrame) -> Dict:
    """
    Run the complete backtest analysis.
    
    Args:
        df: Dataframe with all price data
        
    Returns:
        Dictionary with backtest results
    """
    # Get unique dates (for London Killzone sessions)
    df['Date_only'] = df['DateTime'].dt.date
    unique_dates = sorted(df['Date_only'].unique())
    
    print(f"\nAnalyzing {len(unique_dates)} trading days...")
    
    results = []
    sessions_analyzed = 0
    judas_swings_detected = 0
    peak_sizes = []
    time_to_peaks = []
    
    for i, date in enumerate(unique_dates):
        # Skip first day (need previous day for Tokyo session)
        if i == 0:
            continue
        
        current_date = pd.Timestamp(date)
        
        # Get Tokyo session data
        tokyo_high, tokyo_low, tokyo_eq = get_tokyo_session(df, current_date)
        
        if tokyo_high is None:
            # Missing Tokyo session data
            continue
        
        sessions_analyzed += 1
        
        # Detect Judas Swing
        swing_result = detect_judas_swing(df, current_date, tokyo_high, tokyo_low, tokyo_eq)
        
        if swing_result['detected']:
            judas_swings_detected += 1
            peak_sizes.append(swing_result['peak_size'])
            time_to_peaks.append(swing_result['time_to_peak'])
            
            results.append({
                'date': date,
                'direction': swing_result['direction'],
                'peak_size': swing_result['peak_size'],
                'time_to_peak': swing_result['time_to_peak']
            })
        
        # Progress indicator
        if (sessions_analyzed % 100) == 0:
            print(f"  Processed {sessions_analyzed} sessions...")
    
    # Calculate statistics
    ratio = (judas_swings_detected / sessions_analyzed * 100) if sessions_analyzed > 0 else 0
    
    stats = {
        'total_sessions': sessions_analyzed,
        'judas_swings_detected': judas_swings_detected,
        'ratio_percent': ratio,
        'peak_size_mean': np.mean(peak_sizes) if peak_sizes else 0,
        'peak_size_median': np.median(peak_sizes) if peak_sizes else 0,
        'time_to_peak_mean': np.mean(time_to_peaks) if time_to_peaks else 0,
        'detailed_results': results
    }
    
    return stats


def print_report(stats: Dict):
    """
    Print a formatted report of the backtest results.
    
    Args:
        stats: Dictionary with backtest statistics
    """
    print("\n" + "="*70)
    print(" LONDON KILLZONE JUDAS SWING BACKTEST REPORT")
    print("="*70)
    print()
    print(f"Total Sessions Analyzed:       {stats['total_sessions']}")
    print(f"Judas Swings Detected:         {stats['judas_swings_detected']}")
    print(f"Success Ratio:                 {stats['ratio_percent']:.2f}%")
    print()
    print("-" * 70)
    print(" PEAK SIZE STATISTICS (Manipulation Distance)")
    print("-" * 70)
    print(f"Average Peak Size:             {stats['peak_size_mean']:.2f} points")
    print(f"Median Peak Size:              {stats['peak_size_median']:.2f} points")
    print()
    print("-" * 70)
    print(" TIME TO PEAK STATISTICS")
    print("-" * 70)
    print(f"Average Time to Peak:          {stats['time_to_peak_mean']:.2f} minutes")
    print(f"                               ({stats['time_to_peak_mean']/60:.2f} hours)")
    print()
    
    if stats['detailed_results']:
        print("-" * 70)
        print(" SAMPLE DETECTIONS (First 10)")
        print("-" * 70)
        for i, result in enumerate(stats['detailed_results'][:10]):
            print(f"  {result['date']} - {result['direction']:20s} - "
                  f"Peak: {result['peak_size']:7.2f} pts - "
                  f"Time: {result['time_to_peak']:5.1f} min")
    
    print("\n" + "="*70)


def main():
    """
    Main function to run the backtest.
    """
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='London Killzone Judas Swing Backtest')
    parser.add_argument('--data-dir', type=str, 
                       default='/home/runner/work/Backtest-Trading/Backtest-Trading',
                       help='Directory containing the data files (default: current script directory)')
    parser.add_argument('--years', type=int, nargs='+',
                       default=[2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025],
                       help='Years to analyze (default: 2018-2025)')
    args = parser.parse_args()
    
    print("="*70)
    print(" LONDON KILLZONE JUDAS SWING BACKTEST")
    print(" NQ (Nasdaq Futures) - 1 Minute Data (2018-2025)")
    print("="*70)
    
    # Configuration - use script directory as default if in relative mode
    data_dir = args.data_dir
    if data_dir == '/home/runner/work/Backtest-Trading/Backtest-Trading':
        # Check if we're in the repository directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        if os.path.exists(script_dir):
            data_dir = script_dir
    
    years = args.years
    
    try:
        # Load data
        print("\nStep 1: Loading data...")
        df = load_all_data(data_dir, years)
        
        # Run backtest
        print("\nStep 2: Running backtest analysis...")
        stats = run_backtest(df)
        
        # Print report
        print("\nStep 3: Generating report...")
        print_report(stats)
        
        print("\n✓ Backtest completed successfully!")
        
    except Exception as e:
        print(f"\n✗ Error during backtest: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())

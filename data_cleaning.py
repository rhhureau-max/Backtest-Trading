"""
Data Cleaning Utility for Trading Data

This script provides comprehensive data cleaning and validation
for trading data files before running backtests.
"""

import pandas as pd
import numpy as np
from datetime import datetime
from london_killzone_strategies import DataLoader, TimeManager


def detect_missing_candles(df, expected_interval_minutes=5):
    """
    Detect missing candles in a time series.
    
    Args:
        df: DataFrame with datetime index
        expected_interval_minutes: Expected interval between candles
    
    Returns:
        List of timestamps where candles are missing
    """
    expected_interval = pd.Timedelta(minutes=expected_interval_minutes)
    missing_periods = []
    
    for i in range(1, len(df)):
        time_diff = df.index[i] - df.index[i-1]
        if time_diff > expected_interval * 1.5:  # Allow small tolerance
            missing_periods.append({
                'after': df.index[i-1],
                'before': df.index[i],
                'gap_duration': time_diff,
                'missing_candles': int(time_diff / expected_interval) - 1
            })
    
    return missing_periods


def detect_price_outliers(df, std_threshold=5):
    """
    Detect price outliers.
    
    Args:
        df: DataFrame with OHLCV columns
        std_threshold: Number of standard deviations to consider as outlier
    
    Returns:
        DataFrame with suspicious rows
    """
    df_copy = df.copy()
    df_copy['price_change_pct'] = df_copy['Close'].pct_change() * 100
    
    mean = df_copy['price_change_pct'].mean()
    std = df_copy['price_change_pct'].std()
    
    outliers = df_copy[
        (df_copy['price_change_pct'] > mean + std_threshold * std) |
        (df_copy['price_change_pct'] < mean - std_threshold * std)
    ]
    
    return outliers


def validate_ohlc_consistency(df):
    """
    Verify OHLC data consistency.
    
    Returns:
        DataFrame with inconsistent rows
    """
    inconsistent = df[
        (df['High'] < df['Low']) |
        (df['High'] < df['Open']) |
        (df['High'] < df['Close']) |
        (df['Low'] > df['Open']) |
        (df['Low'] > df['Close']) |
        (df['Close'] <= 0) |
        (df['Open'] <= 0)
    ]
    
    return inconsistent


def analyze_volume_distribution(df):
    """Analyze volume distribution."""
    stats = {
        'mean': df['Volume'].mean(),
        'median': df['Volume'].median(),
        'min': df['Volume'].min(),
        'max': df['Volume'].max(),
        'zero_volume_candles': (df['Volume'] == 0).sum(),
        'low_volume_candles': (df['Volume'] < 10).sum()
    }
    return stats


def comprehensive_data_cleaning(filepath, expected_interval_minutes=5, 
                               min_volume=0, remove_outliers=False):
    """
    Complete data cleaning pipeline.
    
    Args:
        filepath: Path to CSV file
        expected_interval_minutes: Expected interval between candles
        min_volume: Minimum volume threshold (0 = keep all)
        remove_outliers: Whether to remove price outliers
    
    Returns:
        Cleaned DataFrame and cleaning report
    """
    report = []
    report.append("="*80)
    report.append("DATA CLEANING REPORT")
    report.append("="*80)
    report.append(f"File: {filepath}")
    report.append(f"Date: {datetime.now()}")
    report.append("")
    
    # 1. Load data
    report.append("[1] Loading data...")
    df_original = DataLoader.load_csv(filepath)
    original_length = len(df_original)
    report.append(f"    Loaded: {original_length} rows")
    report.append("")
    
    df = df_original.copy()
    
    # 2. Remove missing values
    report.append("[2] Removing missing values...")
    before = len(df)
    df = df.dropna()
    removed = before - len(df)
    if removed > 0:
        report.append(f"    Removed {removed} rows with missing values")
    else:
        report.append("    ✓ No missing values found")
    report.append(f"    Current size: {len(df)} rows")
    report.append("")
    
    # 3. Validate OHLC consistency
    report.append("[3] Validating OHLC consistency...")
    inconsistent = validate_ohlc_consistency(df)
    if len(inconsistent) > 0:
        report.append(f"    ⚠️  Found {len(inconsistent)} inconsistent rows")
        for idx in inconsistent.index[:3]:  # Show first 3
            row = inconsistent.loc[idx]
            report.append(f"       {idx}: O={row['Open']:.2f} H={row['High']:.2f} " +
                         f"L={row['Low']:.2f} C={row['Close']:.2f}")
        
        df = df[
            (df['High'] >= df['Low']) &
            (df['High'] >= df['Open']) &
            (df['High'] >= df['Close']) &
            (df['Low'] <= df['Open']) &
            (df['Low'] <= df['Close']) &
            (df['Close'] > 0) &
            (df['Open'] > 0)
        ]
        report.append(f"    After cleaning: {len(df)} rows")
    else:
        report.append("    ✓ All OHLC data is consistent")
    report.append("")
    
    # 4. Detect missing candles
    report.append("[4] Detecting missing candles...")
    missing = detect_missing_candles(df, expected_interval_minutes)
    if missing:
        report.append(f"    ⚠️  Found {len(missing)} gaps in the data")
        for gap in missing[:5]:  # Show first 5
            report.append(f"       Gap of {gap['missing_candles']} candles " +
                         f"after {gap['after']}")
        if len(missing) > 5:
            report.append(f"       ... and {len(missing) - 5} more gaps")
    else:
        report.append("    ✓ No missing candles detected")
    report.append("")
    
    # 5. Remove duplicates
    report.append("[5] Removing duplicates...")
    before = len(df)
    df = df[~df.index.duplicated(keep='first')]
    removed = before - len(df)
    if removed > 0:
        report.append(f"    Removed {removed} duplicate rows")
    else:
        report.append("    ✓ No duplicates found")
    report.append("")
    
    # 6. Filter abnormal volume
    report.append("[6] Analyzing volume...")
    vol_stats = analyze_volume_distribution(df)
    report.append(f"    Mean volume: {vol_stats['mean']:.0f}")
    report.append(f"    Median volume: {vol_stats['median']:.0f}")
    report.append(f"    Zero volume candles: {vol_stats['zero_volume_candles']}")
    
    if min_volume > 0:
        before = len(df)
        df = df[df['Volume'] >= min_volume]
        removed = before - len(df)
        if removed > 0:
            report.append(f"    Filtered {removed} rows with volume < {min_volume}")
    report.append("")
    
    # 7. Detect price outliers
    report.append("[7] Detecting price outliers...")
    outliers = detect_price_outliers(df, std_threshold=5)
    if len(outliers) > 0:
        report.append(f"    ⚠️  Found {len(outliers)} potential outliers")
        report.append("    (These may be legitimate in volatile markets)")
        for idx in outliers.index[:3]:
            row = outliers.loc[idx]
            report.append(f"       {idx}: Price change = {row['price_change_pct']:.2f}%")
        
        if remove_outliers:
            df = df[~df.index.isin(outliers.index)]
            report.append(f"    Removed outliers. Current size: {len(df)} rows")
    else:
        report.append("    ✓ No extreme outliers detected")
    report.append("")
    
    # 8. Convert to Paris timezone
    report.append("[8] Converting to Paris timezone...")
    try:
        df = TimeManager.convert_to_paris_time(df)
        report.append(f"    ✓ Converted to {df.index.tz}")
    except Exception as e:
        report.append(f"    Note: {e}")
    report.append("")
    
    # Summary
    report.append("="*80)
    report.append("CLEANING SUMMARY")
    report.append("="*80)
    report.append(f"Original rows: {original_length}")
    report.append(f"Final rows: {len(df)}")
    report.append(f"Removed: {original_length - len(df)} ({(original_length - len(df))/original_length*100:.2f}%)")
    report.append(f"Period: {df.index.min()} to {df.index.max()}")
    report.append(f"Trading days: {df.index.date.nunique()}")
    report.append("="*80)
    
    report_text = "\n".join(report)
    print(report_text)
    
    return df, report_text


def main():
    """Main execution function."""
    import sys
    
    print("="*80)
    print("DATA CLEANING UTILITY")
    print("="*80)
    print()
    
    # Get file path from user
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
    else:
        filepath = input("Enter path to CSV file: ").strip()
    
    if not filepath:
        print("Error: No file path provided")
        return
    
    # Get interval
    interval_input = input("Enter expected interval in minutes (default=5): ").strip()
    interval = int(interval_input) if interval_input else 5
    
    # Get volume filter
    volume_input = input("Enter minimum volume threshold (default=0, no filter): ").strip()
    min_volume = int(volume_input) if volume_input else 0
    
    # Remove outliers?
    outliers_input = input("Remove price outliers? (y/n, default=n): ").strip().lower()
    remove_outliers = outliers_input == 'y'
    
    print("\nProcessing...\n")
    
    # Clean data
    df_clean, report = comprehensive_data_cleaning(
        filepath, 
        expected_interval_minutes=interval,
        min_volume=min_volume,
        remove_outliers=remove_outliers
    )
    
    # Save options
    print("\nOptions:")
    print("1. Save cleaned data to new CSV file")
    print("2. Save cleaning report to text file")
    print("3. Both")
    print("4. Neither (exit)")
    
    choice = input("\nEnter choice (1-4): ").strip()
    
    if choice in ['1', '3']:
        output_file = filepath.replace('.csv', '_cleaned.csv')
        # Save without timezone info for compatibility
        df_save = df_clean.copy()
        df_save.index = df_save.index.tz_localize(None)
        
        # Convert to semicolon separator format
        df_save.to_csv(output_file, sep=';', date_format='%d/%m/%Y %H:%M:%S')
        print(f"✓ Cleaned data saved to: {output_file}")
    
    if choice in ['2', '3']:
        report_file = filepath.replace('.csv', '_cleaning_report.txt')
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"✓ Cleaning report saved to: {report_file}")
    
    print("\nDone!")


if __name__ == "__main__":
    main()

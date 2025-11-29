"""
Data Loader Module for 8:30 Strategy Backtest

This module handles loading and preparing CSV data for backtesting.
Supports 1-minute, 5-minute, and 15-minute timeframes.
"""

import os
import zipfile
import pandas as pd
from typing import Dict, Optional


def load_csv_file(filepath: str) -> pd.DataFrame:
    """
    Load a single CSV file with the expected format.
    
    Args:
        filepath: Path to the CSV file
        
    Returns:
        DataFrame with columns: datetime, open, high, low, close, volume
    """
    df = pd.read_csv(
        filepath,
        sep=';',
        names=['date', 'time', 'open', 'high', 'low', 'close', 'volume'],
        skiprows=1  # Skip header row
    )
    
    # Create datetime column
    df['datetime'] = pd.to_datetime(
        df['date'] + ' ' + df['time'],
        format='%d/%m/%Y %H:%M:%S'
    )
    
    # Set datetime as index
    df = df.set_index('datetime')
    df = df.drop(columns=['date', 'time'])
    
    # Convert to numeric
    for col in ['open', 'high', 'low', 'close', 'volume']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    return df.sort_index()


def load_zip_csv(zip_filepath: str) -> pd.DataFrame:
    """
    Load a CSV file from a ZIP archive.
    
    Args:
        zip_filepath: Path to the ZIP file
        
    Returns:
        DataFrame with the loaded data
    """
    with zipfile.ZipFile(zip_filepath, 'r') as zip_ref:
        # Find the CSV file inside (exclude __MACOSX folder)
        csv_files = [f for f in zip_ref.namelist() 
                     if f.endswith('.csv') and not f.startswith('__MACOSX')]
        
        if not csv_files:
            raise ValueError(f"No CSV file found in {zip_filepath}")
        
        csv_name = csv_files[0]
        
        with zip_ref.open(csv_name) as csv_file:
            df = pd.read_csv(
                csv_file,
                sep=';',
                names=['date', 'time', 'open', 'high', 'low', 'close', 'volume'],
                skiprows=1
            )
    
    # Create datetime column
    df['datetime'] = pd.to_datetime(
        df['date'] + ' ' + df['time'],
        format='%d/%m/%Y %H:%M:%S'
    )
    
    # Set datetime as index
    df = df.set_index('datetime')
    df = df.drop(columns=['date', 'time'])
    
    # Convert to numeric
    for col in ['open', 'high', 'low', 'close', 'volume']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    return df.sort_index()


def load_timeframe_data(data_dir: str, timeframe: str, years: list = None) -> pd.DataFrame:
    """
    Load all data for a specific timeframe across multiple years.
    
    Args:
        data_dir: Directory containing data files
        timeframe: '1m', '5m', or '15m'
        years: List of years to load (default: 2018-2025)
        
    Returns:
        Combined DataFrame for all years
    """
    if years is None:
        years = list(range(2018, 2026))
    
    all_data = []
    
    for year in years:
        if timeframe == '1m':
            # Check for uncompressed file first (2025)
            csv_path = os.path.join(data_dir, f"{year} 1m.csv")
            zip_path = os.path.join(data_dir, f"{year} 1m.csv.zip")
            
            if os.path.exists(csv_path):
                df = load_csv_file(csv_path)
                all_data.append(df)
            elif os.path.exists(zip_path):
                df = load_zip_csv(zip_path)
                all_data.append(df)
        else:
            csv_path = os.path.join(data_dir, f"{year} {timeframe}.csv")
            if os.path.exists(csv_path):
                df = load_csv_file(csv_path)
                all_data.append(df)
    
    if not all_data:
        raise ValueError(f"No data found for timeframe {timeframe}")
    
    combined = pd.concat(all_data)
    combined = combined.sort_index()
    
    # Remove any duplicates
    combined = combined[~combined.index.duplicated(keep='first')]
    
    return combined


def get_830_candles(df: pd.DataFrame) -> pd.DataFrame:
    """
    Extract candles at 8:30 from the DataFrame.
    
    Args:
        df: DataFrame with datetime index
        
    Returns:
        DataFrame containing only 8:30 candles
    """
    mask = (df.index.hour == 8) & (df.index.minute == 30)
    return df[mask].copy()


def get_previous_candles(df: pd.DataFrame, target_time: pd.Timestamp, 
                         n_candles: int = 5) -> pd.DataFrame:
    """
    Get the n previous candles before a target time.
    
    Args:
        df: Full DataFrame
        target_time: Target timestamp
        n_candles: Number of previous candles to retrieve
        
    Returns:
        DataFrame with the previous n candles
    """
    # Get all candles before the target time on the same day
    day_start = target_time.replace(hour=0, minute=0, second=0)
    mask = (df.index >= day_start) & (df.index < target_time)
    day_candles = df[mask]
    
    if len(day_candles) < n_candles:
        return day_candles
    
    return day_candles.tail(n_candles)


def prepare_simulation_data(data_1m: pd.DataFrame, entry_time: pd.Timestamp) -> pd.DataFrame:
    """
    Prepare 1-minute data for trade simulation starting from entry time.
    
    Args:
        data_1m: 1-minute DataFrame
        entry_time: Entry timestamp
        
    Returns:
        DataFrame with 1-minute data from entry onwards
    """
    return data_1m[data_1m.index > entry_time].copy()


if __name__ == "__main__":
    # Test the data loader
    import sys
    
    data_dir = os.path.dirname(os.path.abspath(__file__))
    
    print("Testing data loader...")
    
    # Test loading 15m data
    print("\nLoading 15m data...")
    df_15m = load_timeframe_data(data_dir, '15m')
    print(f"Loaded {len(df_15m)} rows")
    print(f"Date range: {df_15m.index.min()} to {df_15m.index.max()}")
    
    # Get 8:30 candles
    candles_830 = get_830_candles(df_15m)
    print(f"\n8:30 candles found: {len(candles_830)}")
    print("\nFirst 5 candles at 8:30:")
    print(candles_830.head())

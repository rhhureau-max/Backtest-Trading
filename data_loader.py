"""
Data Loader Module for NQ Backtesting
Handles loading and combining CSV files for multiple timeframes
"""

import pandas as pd
import numpy as np
from pathlib import Path
import zipfile
import os
from typing import Dict, List
import warnings
warnings.filterwarnings('ignore')


class DataLoader:
    """Loads and preprocesses NQ data from CSV files"""
    
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.years = list(range(2018, 2026))  # 2018-2025
        
    def extract_1m_zips(self):
        """Extract zipped 1-minute files if they exist"""
        for year in self.years:
            zip_path = self.base_path / f"{year} 1m.csv.zip"
            csv_path = self.base_path / f"{year} 1m.csv"
            
            if zip_path.exists() and not csv_path.exists():
                print(f"Extracting {zip_path.name}...")
                try:
                    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                        zip_ref.extractall(self.base_path)
                    print(f"  ✓ Extracted successfully")
                except Exception as e:
                    print(f"  ✗ Error extracting {zip_path.name}: {e}")
    
    def load_timeframe(self, timeframe: str) -> pd.DataFrame:
        """
        Load and combine data for a specific timeframe
        
        Args:
            timeframe: '1m', '5m', '1H', or '4H'
            
        Returns:
            Combined DataFrame with all years
        """
        print(f"\nLoading {timeframe} data...")
        
        dfs = []
        for year in self.years:
            file_path = self.base_path / f"{year} {timeframe}.csv"
            
            if not file_path.exists():
                print(f"  ⚠ {file_path.name} not found, skipping")
                continue
                
            try:
                # Read CSV with semicolon separator
                df = pd.read_csv(
                    file_path,
                    sep=';',
                    header=0,
                    names=['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
                )
                
                # Combine Date and Time columns
                df['DateTime'] = pd.to_datetime(
                    df['Date'] + ' ' + df['Time'],
                    format='%d/%m/%Y %H:%M:%S'
                )
                
                # Set timezone to Chicago (US/Central)
                df['DateTime'] = df['DateTime'].dt.tz_localize('US/Central', ambiguous='infer', nonexistent='shift_forward')
                
                # Keep only necessary columns
                df = df[['DateTime', 'Open', 'High', 'Low', 'Close', 'Volume']]
                
                # Sort by datetime
                df = df.sort_values('DateTime').reset_index(drop=True)
                
                dfs.append(df)
                print(f"  ✓ Loaded {year} {timeframe}: {len(df)} rows")
                
            except Exception as e:
                print(f"  ✗ Error loading {file_path.name}: {e}")
                continue
        
        if not dfs:
            raise ValueError(f"No data loaded for timeframe {timeframe}")
        
        # Combine all years
        combined = pd.concat(dfs, ignore_index=True)
        combined = combined.sort_values('DateTime').reset_index(drop=True)
        
        # Remove duplicates
        combined = combined.drop_duplicates(subset=['DateTime'], keep='first')
        
        print(f"  ✓ Combined {timeframe}: {len(combined)} total rows")
        print(f"  ✓ Date range: {combined['DateTime'].min()} to {combined['DateTime'].max()}")
        
        return combined
    
    def load_all_timeframes(self) -> Dict[str, pd.DataFrame]:
        """
        Load all required timeframes
        
        Returns:
            Dictionary with keys '1m', '5m', '1H', '4H' and DataFrames as values
        """
        print("=" * 70)
        print("NQ DATA LOADER - Starting data load process")
        print("=" * 70)
        
        # Extract 1-minute zipped files first
        self.extract_1m_zips()
        
        # Load each timeframe
        data = {}
        timeframes = ['1m', '5m', '1H', '4H']
        
        for tf in timeframes:
            try:
                data[tf] = self.load_timeframe(tf)
            except Exception as e:
                print(f"Failed to load {tf}: {e}")
                # Continue with other timeframes
                
        print("\n" + "=" * 70)
        print(f"Data loading complete. Loaded {len(data)} timeframes.")
        print("=" * 70)
        
        return data


def get_market_data(base_path: str = ".") -> Dict[str, pd.DataFrame]:
    """
    Convenience function to load all market data
    
    Args:
        base_path: Path to directory containing CSV files
        
    Returns:
        Dictionary with timeframe data
    """
    loader = DataLoader(base_path)
    return loader.load_all_timeframes()


if __name__ == "__main__":
    # Test the data loader
    data = get_market_data()
    
    print("\nData Summary:")
    print("-" * 70)
    for tf, df in data.items():
        print(f"{tf:4s}: {len(df):,} rows | {df['DateTime'].min()} to {df['DateTime'].max()}")

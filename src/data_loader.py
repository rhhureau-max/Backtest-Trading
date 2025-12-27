"""
Data loading utilities for CSV files.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional
import config


class DataLoader:
    """
    Loads and preprocesses OHLCV data from CSV files.
    """
    
    def __init__(self, data_dir: str = config.DATA_DIR):
        self.data_dir = Path(data_dir)
    
    def load_timeframe(self, timeframe: str, years: Optional[List[int]] = None) -> pd.DataFrame:
        """
        Load data for a specific timeframe across multiple years.
        
        Args:
            timeframe: Timeframe string ('5m', '15m', '1h', '4h', '1d')
            years: List of years to load. If None, loads all available years.
        
        Returns:
            Combined DataFrame with datetime index
        """
        if years is None:
            years = config.YEARS
        
        dfs = []
        for year in years:
            filepath = self.data_dir / f"{year} {timeframe}.csv"
            if filepath.exists():
                df = self._load_single_file(filepath)
                if df is not None and not df.empty:
                    dfs.append(df)
        
        if not dfs:
            return pd.DataFrame()
        
        # Combine all years
        combined_df = pd.concat(dfs, axis=0)
        combined_df = combined_df.sort_index()
        
        # Remove duplicates
        combined_df = combined_df[~combined_df.index.duplicated(keep='first')]
        
        return combined_df
    
    def _load_single_file(self, filepath: Path) -> Optional[pd.DataFrame]:
        """
        Load a single CSV file and parse it.
        
        Args:
            filepath: Path to CSV file
        
        Returns:
            DataFrame with parsed datetime index
        """
        try:
            # Read CSV with semicolon separator
            df = pd.read_csv(filepath, sep=';')
            
            # Remove unnamed columns (Column1, Column2, etc.)
            df.columns = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
            
            # Combine Date and Time into datetime
            df['datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%d/%m/%Y %H:%M:%S')
            
            # Set datetime as index
            df.set_index('datetime', inplace=True)
            
            # Keep only OHLCV columns
            df = df[['Open', 'High', 'Low', 'Close', 'Volume']]
            
            # Convert to numeric
            for col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # Drop rows with NaN values
            df = df.dropna()
            
            # Convert from Chicago time (UTC-6) to Paris time (CET/CEST)
            # Step 1: Localize as Chicago time (America/Chicago includes DST)
            df.index = df.index.tz_localize('America/Chicago', ambiguous='infer', nonexistent='shift_forward')
            # Step 2: Convert to Paris timezone
            df.index = df.index.tz_convert('Europe/Paris')
            
            return df
        
        except Exception as e:
            print(f"Error loading {filepath}: {e}")
            return None
    
    def load_multiple_timeframes(self, timeframes: List[str], years: Optional[List[int]] = None) -> Dict[str, pd.DataFrame]:
        """
        Load multiple timeframes at once.
        
        Args:
            timeframes: List of timeframe strings
            years: List of years to load
        
        Returns:
            Dictionary mapping timeframe to DataFrame
        """
        data = {}
        for tf in timeframes:
            df = self.load_timeframe(tf, years)
            if not df.empty:
                data[tf] = df
        return data
    
    def filter_london_session(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Filter data to London session hours (08:00-12:00 Paris time).
        
        Args:
            df: DataFrame with datetime index
        
        Returns:
            Filtered DataFrame
        """
        london_start = pd.to_datetime(config.LONDON_SESSION_START).time()
        london_end = pd.to_datetime(config.LONDON_SESSION_END).time()
        
        mask = (df.index.time >= london_start) & (df.index.time < london_end)
        return df[mask].copy()
    
    def filter_asian_session(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Filter data to Asian session hours (00:00-08:00 Paris time).
        
        Args:
            df: DataFrame with datetime index
        
        Returns:
            Filtered DataFrame
        """
        asian_start = pd.to_datetime(config.ASIAN_SESSION_START).time()
        asian_end = pd.to_datetime(config.ASIAN_SESSION_END).time()
        
        mask = (df.index.time >= asian_start) & (df.index.time < asian_end)
        return df[mask].copy()
    
    def get_trading_days(self, df: pd.DataFrame) -> List[pd.Timestamp]:
        """
        Get list of unique trading days from DataFrame.
        
        Args:
            df: DataFrame with datetime index
        
        Returns:
            List of dates
        """
        return df.index.normalize().unique().tolist()

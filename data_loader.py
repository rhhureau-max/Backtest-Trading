"""
Data Loader Module for NQ Futures Backtest
Loads and preprocesses NQ futures data from CSV files (2018-2025)
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List
import warnings
warnings.filterwarnings('ignore')


class DataLoader:
    """Loads and processes NQ futures data across multiple timeframes"""
    
    def __init__(self, data_dir: str = "/home/runner/work/Backtest-Trading/Backtest-Trading"):
        self.data_dir = Path(data_dir)
        self.timeframes = ['5m', '15m', '1H']
        self.years = list(range(2018, 2026))  # 2018-2025
        
    def load_timeframe(self, timeframe: str) -> pd.DataFrame:
        """
        Load all years for a specific timeframe and merge into single dataframe
        
        Args:
            timeframe: '5m', '15m', or '1H'
            
        Returns:
            Merged dataframe with datetime index
        """
        dfs = []
        
        for year in self.years:
            file_path = self.data_dir / f"{year} {timeframe}.csv"
            
            if not file_path.exists():
                print(f"Warning: File not found: {file_path}")
                continue
                
            try:
                # Read CSV with semicolon separator
                df = pd.read_csv(file_path, sep=';', skiprows=1)
                
                # The CSV has 7 columns: Date, Time, Open, High, Low, Close, Volume
                df.columns = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
                
                # Create datetime column from Date and Time
                df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], 
                                                format='%d/%m/%Y %H:%M:%S')
                
                # Select relevant columns
                df = df[['Datetime', 'Open', 'High', 'Low', 'Close', 'Volume']]
                
                # Convert price columns to float
                for col in ['Open', 'High', 'Low', 'Close']:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                df['Volume'] = pd.to_numeric(df['Volume'], errors='coerce')
                
                # Drop any rows with NaN values
                df = df.dropna()
                
                dfs.append(df)
                print(f"Loaded {len(df)} bars from {year} {timeframe}")
                
            except Exception as e:
                print(f"Error loading {file_path}: {str(e)}")
                continue
        
        if not dfs:
            raise ValueError(f"No data loaded for timeframe {timeframe}")
        
        # Merge all dataframes
        merged_df = pd.concat(dfs, ignore_index=True)
        
        # Sort by datetime and set as index
        merged_df = merged_df.sort_values('Datetime')
        merged_df = merged_df.set_index('Datetime')
        
        # Remove any duplicate timestamps (keep first)
        merged_df = merged_df[~merged_df.index.duplicated(keep='first')]
        
        print(f"Total {timeframe} data: {len(merged_df)} bars from {merged_df.index[0]} to {merged_df.index[-1]}")
        
        return merged_df
    
    def load_all_timeframes(self) -> Dict[str, pd.DataFrame]:
        """
        Load all required timeframes
        
        Returns:
            Dictionary with keys '5m', '15m', '1H' containing respective dataframes
        """
        data = {}
        
        for tf in self.timeframes:
            print(f"\n{'='*50}")
            print(f"Loading {tf} data...")
            print(f"{'='*50}")
            data[tf] = self.load_timeframe(tf)
        
        return data
    
    def get_trading_days(self, df: pd.DataFrame) -> List[str]:
        """
        Get list of unique trading days from dataframe
        
        Args:
            df: Dataframe with datetime index
            
        Returns:
            List of date strings in YYYY-MM-DD format
        """
        unique_dates = pd.Series(df.index.date).unique()
        return sorted([str(d) for d in unique_dates])


if __name__ == "__main__":
    # Test the data loader
    loader = DataLoader()
    
    print("Testing Data Loader...")
    print("="*50)
    
    try:
        data = loader.load_all_timeframes()
        
        print("\n" + "="*50)
        print("Data Loading Summary")
        print("="*50)
        
        for tf, df in data.items():
            print(f"\n{tf} timeframe:")
            print(f"  Total bars: {len(df)}")
            print(f"  Date range: {df.index[0].date()} to {df.index[-1].date()}")
            print(f"  Sample data:")
            print(df.head(3))
        
        # Test getting trading days
        days = loader.get_trading_days(data['5m'])
        print(f"\nTotal trading days: {len(days)}")
        print(f"First day: {days[0]}")
        print(f"Last day: {days[-1]}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()

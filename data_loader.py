"""
Data Loader Module for FVG Backtest
Handles loading and preprocessing of trading data from CSV and ZIP files
"""

import pandas as pd
import zipfile
import os
from datetime import datetime, time
import warnings
warnings.filterwarnings('ignore')


class DataLoader:
    """Load and preprocess trading data from CSV files"""
    
    def __init__(self, base_path="/home/runner/work/Backtest-Trading/Backtest-Trading"):
        self.base_path = base_path
        
    def load_csv_data(self, year, timeframe):
        """
        Load data for a specific year and timeframe
        
        Parameters:
        -----------
        year : int
            Year of the data (2018-2025)
        timeframe : str
            Timeframe ('1m', '5m', '15m', '1H', '4H', '1D')
            
        Returns:
        --------
        pd.DataFrame
            Loaded and preprocessed data
        """
        filename = f"{year} {timeframe}.csv"
        filepath = os.path.join(self.base_path, filename)
        
        # Handle 1-minute data from ZIP files (2018-2024)
        if timeframe == '1m' and year < 2025:
            zip_filename = f"{year} 1m.csv.zip"
            zip_filepath = os.path.join(self.base_path, zip_filename)
            
            if os.path.exists(zip_filepath):
                with zipfile.ZipFile(zip_filepath, 'r') as zip_ref:
                    csv_filename = f"{year} 1m.csv"
                    with zip_ref.open(csv_filename) as csv_file:
                        df = pd.read_csv(csv_file, sep=';', skiprows=1)
            else:
                raise FileNotFoundError(f"ZIP file not found: {zip_filepath}")
        else:
            if os.path.exists(filepath):
                df = pd.read_csv(filepath, sep=';', skiprows=1)
            else:
                raise FileNotFoundError(f"CSV file not found: {filepath}")
        
        # Rename columns
        df.columns = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
        
        # Parse datetime
        df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], 
                                        format='%d/%m/%Y %H:%M:%S')
        
        # Set DateTime as index
        df.set_index('DateTime', inplace=True)
        
        # Convert price columns to float
        for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Drop rows with NaN values
        df.dropna(inplace=True)
        
        # Add time features
        df['Hour'] = df.index.hour
        df['Minute'] = df.index.minute
        df['DayOfWeek'] = df.index.dayofweek
        df['Date_only'] = df.index.date
        
        return df
    
    def load_multiple_years(self, start_year, end_year, timeframe):
        """
        Load data for multiple years and concatenate
        
        Parameters:
        -----------
        start_year : int
            Starting year
        end_year : int
            Ending year (inclusive)
        timeframe : str
            Timeframe ('1m', '5m', '15m')
            
        Returns:
        --------
        pd.DataFrame
            Combined data for all years
        """
        dfs = []
        
        for year in range(start_year, end_year + 1):
            try:
                df = self.load_csv_data(year, timeframe)
                print(f"Loaded {year} {timeframe} data: {len(df)} rows")
                dfs.append(df)
            except FileNotFoundError as e:
                print(f"Warning: {e}")
                continue
        
        if not dfs:
            raise ValueError("No data loaded for the specified years and timeframe")
        
        # Concatenate all dataframes
        combined_df = pd.concat(dfs, axis=0)
        combined_df.sort_index(inplace=True)
        
        print(f"\nTotal rows loaded: {len(combined_df)}")
        print(f"Date range: {combined_df.index.min()} to {combined_df.index.max()}")
        
        return combined_df
    
    def filter_trading_hours(self, df, start_hour=8, end_hour=17):
        """
        Filter data to include only trading hours
        
        Parameters:
        -----------
        df : pd.DataFrame
            Input data
        start_hour : int
            Start hour (default 8 for 8:00 AM)
        end_hour : int
            End hour (default 17 for 5:00 PM)
            
        Returns:
        --------
        pd.DataFrame
            Filtered data
        """
        mask = (df.index.hour >= start_hour) & (df.index.hour < end_hour)
        return df[mask].copy()

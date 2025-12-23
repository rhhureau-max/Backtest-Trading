"""
Module for loading and preprocessing NQ futures data.
"""
import pandas as pd
import glob
from datetime import datetime, time


class DataLoader:
    """Loads and filters NQ 5-minute data from CSV files."""
    
    def __init__(self, data_directory="."):
        """
        Initialize the data loader.
        
        Args:
            data_directory: Directory containing the CSV files
        """
        self.data_directory = data_directory
        
    def load_data(self, start_year=2018, end_year=2025):
        """
        Load all 5-minute NQ data files from start_year to end_year.
        
        Args:
            start_year: Starting year (inclusive)
            end_year: Ending year (inclusive)
            
        Returns:
            DataFrame with columns: datetime, open, high, low, close, volume
        """
        all_data = []
        
        for year in range(start_year, end_year + 1):
            filename = f"{self.data_directory}/{year} 5m.csv"
            try:
                # Read CSV with semicolon separator
                df = pd.read_csv(filename, sep=';', decimal='.', encoding='utf-8')
                
                # Rename columns for easier access
                df.columns = ['date', 'time', 'open', 'high', 'low', 'close', 'volume']
                
                # Combine date and time into a single datetime column
                df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'], format='%d/%m/%Y %H:%M:%S')
                
                # Drop original date and time columns
                df = df.drop(['date', 'time'], axis=1)
                
                # Reorder columns
                df = df[['datetime', 'open', 'high', 'low', 'close', 'volume']]
                
                all_data.append(df)
                print(f"Loaded {len(df)} rows from {year}")
                
            except FileNotFoundError:
                print(f"Warning: File not found for year {year}")
                continue
            except Exception as e:
                print(f"Error loading {year}: {e}")
                continue
        
        if not all_data:
            raise ValueError("No data files could be loaded")
        
        # Concatenate all dataframes
        combined_df = pd.concat(all_data, ignore_index=True)
        
        # Sort by datetime
        combined_df = combined_df.sort_values('datetime').reset_index(drop=True)
        
        print(f"\nTotal rows loaded: {len(combined_df)}")
        print(f"Date range: {combined_df['datetime'].min()} to {combined_df['datetime'].max()}")
        
        return combined_df
    
    def filter_trading_session(self, df, start_hour=2, start_minute=0, end_hour=6, end_minute=0):
        """
        Filter data to only include candles within the specified trading session.
        
        Args:
            df: DataFrame with datetime column
            start_hour: Session start hour (0-23)
            start_minute: Session start minute (0-59)
            end_hour: Session end hour (0-23)
            end_minute: Session end minute (0-59)
            
        Returns:
            Filtered DataFrame
        """
        # Extract time from datetime
        df['time_only'] = df['datetime'].dt.time
        
        # Create time objects for comparison
        session_start = time(start_hour, start_minute)
        session_end = time(end_hour, end_minute)
        
        # Filter for trading session (2:00 AM to 6:00 AM)
        mask = (df['time_only'] >= session_start) & (df['time_only'] < session_end)
        filtered_df = df[mask].copy()
        
        # Drop the temporary time_only column
        filtered_df = filtered_df.drop('time_only', axis=1)
        
        print(f"Filtered to {len(filtered_df)} rows in trading session ({start_hour:02d}:{start_minute:02d} - {end_hour:02d}:{end_minute:02d})")
        
        return filtered_df.reset_index(drop=True)
    
    def add_session_markers(self, df):
        """
        Add a column to identify different trading sessions (one per day).
        
        Args:
            df: DataFrame with datetime column
            
        Returns:
            DataFrame with session_id column added
        """
        # Create a date column (without time)
        df['date_only'] = df['datetime'].dt.date
        
        # Assign session ID based on date
        df['session_id'] = pd.factorize(df['date_only'])[0]
        
        # Drop temporary date column
        df = df.drop('date_only', axis=1)
        
        num_sessions = df['session_id'].nunique()
        print(f"Identified {num_sessions} trading sessions")
        
        return df

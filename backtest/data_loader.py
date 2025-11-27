"""
Data loader module for loading and preparing OHLC data from CSV files.
"""
import os
import zipfile
import pandas as pd
from datetime import datetime
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)


def parse_datetime(date_str: str, time_str: str) -> datetime:
    """Parse date and time strings into datetime object."""
    # Date format: DD/MM/YYYY, Time format: HH:MM:SS
    try:
        return datetime.strptime(f"{date_str} {time_str}", "%d/%m/%Y %H:%M:%S")
    except ValueError:
        # Try alternative formats
        try:
            return datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M:%S")
        except ValueError:
            return datetime.strptime(f"{date_str} {time_str}", "%m/%d/%Y %H:%M:%S")


def load_csv_file(filepath: str) -> pd.DataFrame:
    """
    Load a single CSV file and return a DataFrame with proper column names and datetime index.
    
    Args:
        filepath: Path to the CSV file
        
    Returns:
        DataFrame with columns: Open, High, Low, Close, Volume and datetime index
    """
    logger.debug(f"Loading file: {filepath}")
    
    # Check if it's a zip file
    if filepath.endswith('.zip'):
        # Extract and read the CSV from zip
        with zipfile.ZipFile(filepath, 'r') as z:
            # Get the first CSV file in the archive
            csv_names = [n for n in z.namelist() if n.endswith('.csv')]
            if not csv_names:
                raise ValueError(f"No CSV file found in {filepath}")
            with z.open(csv_names[0]) as f:
                df = pd.read_csv(f, sep=';', header=0)
    else:
        df = pd.read_csv(filepath, sep=';', header=0)
    
    # Rename columns
    df.columns = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
    
    # Convert to numeric, handling potential issues
    for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Create datetime index
    df['Datetime'] = df.apply(lambda row: parse_datetime(str(row['Date']), str(row['Time'])), axis=1)
    df.set_index('Datetime', inplace=True)
    df.drop(['Date', 'Time'], axis=1, inplace=True)
    
    # Sort by datetime
    df.sort_index(inplace=True)
    
    # Remove duplicates
    df = df[~df.index.duplicated(keep='first')]
    
    # Remove rows with NaN values
    df.dropna(inplace=True)
    
    logger.debug(f"Loaded {len(df)} rows from {filepath}")
    return df


def load_timeframe_data(
    data_dir: str,
    file_pattern: str,
    start_year: int,
    end_year: int
) -> pd.DataFrame:
    """
    Load data for a specific timeframe across multiple years.
    
    Args:
        data_dir: Directory containing the data files
        file_pattern: Pattern for file names (e.g., "{year} 5m.csv")
        start_year: First year to load
        end_year: Last year to load
        
    Returns:
        Combined DataFrame with all years' data
    """
    all_data = []
    
    for year in range(start_year, end_year + 1):
        filename = file_pattern.format(year=year)
        filepath = os.path.join(data_dir, filename)
        
        # Check for regular CSV or zip file
        if not os.path.exists(filepath):
            # Try zip extension for 1m files
            zip_filepath = filepath.replace('.csv', '.csv.zip')
            if os.path.exists(zip_filepath):
                filepath = zip_filepath
            else:
                logger.warning(f"File not found: {filepath}")
                continue
        
        try:
            df = load_csv_file(filepath)
            all_data.append(df)
            logger.info(f"Loaded {len(df)} rows from {filename}")
        except Exception as e:
            logger.error(f"Error loading {filepath}: {e}")
            continue
    
    if not all_data:
        raise ValueError(f"No data loaded for pattern {file_pattern}")
    
    # Combine all years
    combined = pd.concat(all_data)
    combined.sort_index(inplace=True)
    combined = combined[~combined.index.duplicated(keep='first')]
    
    logger.info(f"Total rows loaded for {file_pattern}: {len(combined)}")
    return combined


class DataLoader:
    """
    Class to manage loading and caching of OHLC data for multiple timeframes.
    """
    
    def __init__(self, data_dir: str, start_year: int = 2018, end_year: int = 2025):
        """
        Initialize the data loader.
        
        Args:
            data_dir: Directory containing the data files
            start_year: First year to load
            end_year: Last year to load
        """
        self.data_dir = data_dir
        self.start_year = start_year
        self.end_year = end_year
        self._cache: Dict[str, pd.DataFrame] = {}
    
    def get_h1_data(self) -> pd.DataFrame:
        """Load 1-hour (H1) data."""
        if 'H1' not in self._cache:
            self._cache['H1'] = load_timeframe_data(
                self.data_dir, "{year} 1H.csv", self.start_year, self.end_year
            )
        return self._cache['H1']
    
    def get_m15_data(self) -> pd.DataFrame:
        """Load 15-minute (M15) data."""
        if 'M15' not in self._cache:
            self._cache['M15'] = load_timeframe_data(
                self.data_dir, "{year} 15m.csv", self.start_year, self.end_year
            )
        return self._cache['M15']
    
    def get_m5_data(self) -> pd.DataFrame:
        """Load 5-minute (M5) data."""
        if 'M5' not in self._cache:
            self._cache['M5'] = load_timeframe_data(
                self.data_dir, "{year} 5m.csv", self.start_year, self.end_year
            )
        return self._cache['M5']
    
    def get_all_data(self) -> Dict[str, pd.DataFrame]:
        """Load all timeframes and return as dictionary."""
        return {
            'H1': self.get_h1_data(),
            'M15': self.get_m15_data(),
            'M5': self.get_m5_data()
        }
    
    def clear_cache(self):
        """Clear the data cache."""
        self._cache.clear()

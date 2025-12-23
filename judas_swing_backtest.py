#!/usr/bin/env python3
"""
Judas Swing Backtest Strategy for Nasdaq 100 (NQ)

This script backtests the "Judas Swing" strategy which identifies manipulation patterns
during the London session following the Tokyo session range.

Strategy Logic:
1. Tokyo Session: 18:00 (previous day) to 01:00 (current day) - Calculate High/Low range
2. London Manipulation Window: 01:00 to 05:00 - Observe price action
3. Bearish Manipulation (Long Setup): Price breaks below Tokyo Low
4. Bullish Manipulation (Short Setup): Price breaks above Tokyo High

Author: Algorithmic Trading Agent
Date: 2025-12-23
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import glob
import os
import warnings

warnings.filterwarnings('ignore')


class JudasSwingBacktest:
    """
    Backtest class for the Judas Swing trading strategy.
    """
    
    def __init__(self, data_source='combined', years=None):
        """
        Initialize the backtest.
        
        Parameters:
        -----------
        data_source : str
            'single' to load NQ_Data.csv or 'combined' to load multiple yearly files
        years : list
            List of years to load (e.g., [2018, 2019, 2020])
        """
        self.data_source = data_source
        self.years = years if years else [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]
        self.df = None
        self.results = []
        
    def load_data(self):
        """
        Load and prepare the data based on the data source.
        """
        if self.data_source == 'single':
            # Load single file (NQ_Data.csv)
            if os.path.exists('NQ_Data.csv'):
                print("Loading NQ_Data.csv...")
                self.df = pd.read_csv('NQ_Data.csv')
                print(f"Loaded {len(self.df)} rows from NQ_Data.csv")
            else:
                print("Warning: NQ_Data.csv not found. Falling back to combined mode.")
                self.data_source = 'combined'
                self.load_data()
                return
        
        if self.data_source == 'combined':
            # Load multiple yearly files
            print("Loading combined yearly data files...")
            dfs = []
            
            for year in self.years:
                # Try to load 5-minute data first
                filename_5m = f"{year} 5m.csv"
                
                if os.path.exists(filename_5m):
                    print(f"Loading {filename_5m}...")
                    try:
                        # Read with semicolon separator
                        df_year = pd.read_csv(
                            filename_5m,
                            sep=';',
                            skiprows=1,  # Skip the "Column1;Column2..." header row
                            names=['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
                        )
                        dfs.append(df_year)
                        print(f"  Loaded {len(df_year)} rows from {filename_5m}")
                    except Exception as e:
                        print(f"  Error loading {filename_5m}: {e}")
                else:
                    print(f"  Warning: {filename_5m} not found, skipping...")
            
            if not dfs:
                raise FileNotFoundError("No data files found. Please check the file paths.")
            
            # Combine all dataframes
            self.df = pd.concat(dfs, ignore_index=True)
            print(f"\nTotal rows loaded: {len(self.df)}")
        
        # Parse datetime
        self._parse_datetime()
        
        # Sort by datetime
        self.df = self.df.sort_values('DateTime').reset_index(drop=True)
        
        print(f"Data range: {self.df['DateTime'].min()} to {self.df['DateTime'].max()}")
        print(f"Total trading days available: {self.df['DateTime'].dt.date.nunique()}\n")
    
    def _parse_datetime(self):
        """
        Parse Date and Time columns into a single DateTime column.
        Assumes EST/New York timezone (data is already in EST).
        """
        print("Parsing datetime columns...")
        
        # Combine Date and Time into DateTime
        self.df['DateTime'] = pd.to_datetime(
            self.df['Date'] + ' ' + self.df['Time'],
            format='%d/%m/%Y %H:%M:%S',
            errors='coerce'
        )
        
        # Drop rows with invalid datetime
        invalid_count = self.df['DateTime'].isna().sum()
        if invalid_count > 0:
            print(f"  Warning: Dropping {invalid_count} rows with invalid datetime")
            self.df = self.df.dropna(subset=['DateTime'])
        
        # Extract date and time components
        self.df['Date_Only'] = self.df['DateTime'].dt.date
        self.df['Hour'] = self.df['DateTime'].dt.hour
        self.df['Minute'] = self.df['DateTime'].dt.minute
        self.df['Time_Only'] = self.df['DateTime'].dt.time
    
    def identify_sessions(self):
        """
        Identify Tokyo session and London manipulation window for each trading day.
        
        Tokyo Session: 18:00 (previous day) to 01:00 (current day)
        London Manipulation: 01:00 to 05:00 (current day)
        """
        print("Identifying trading sessions...")
        
        # Get unique trading days (based on the date when London session occurs)
        # A trading day is defined by the date when the London session (01:00-05:00) occurs
        unique_dates = sorted(self.df['Date_Only'].unique())
        
        print(f"Processing {len(unique_dates)} unique dates...\n")
        
        for current_date in unique_dates:
            self._analyze_trading_day(current_date)
    
    def _analyze_trading_day(self, trading_date):
        """
        Analyze a single trading day for Judas Swing patterns.
        
        Parameters:
        -----------
        trading_date : date
            The date for which to analyze the trading pattern
        """
        # Tokyo Session: 18:00 previous day to 01:00 current day
        # We need data from the previous day's 18:00 onwards
        previous_date = trading_date - timedelta(days=1)
        
        # Filter Tokyo session data (18:00 previous day to 01:00 current day)
        tokyo_session = self.df[
            ((self.df['Date_Only'] == previous_date) & (self.df['Hour'] >= 18)) |
            ((self.df['Date_Only'] == trading_date) & (self.df['Hour'] < 1))
        ]
        
        # Filter London manipulation window (01:00 to 05:00 current day)
        london_window = self.df[
            (self.df['Date_Only'] == trading_date) &
            (self.df['Hour'] >= 1) &
            (self.df['Hour'] < 5)
        ]
        
        # Check if we have sufficient data
        if len(tokyo_session) == 0 or len(london_window) == 0:
            return
        
        # Calculate Tokyo range
        tokyo_high = tokyo_session['High'].max()
        tokyo_low = tokyo_session['Low'].min()
        
        # Get London window extremes
        london_high = london_window['High'].max()
        london_low = london_window['Low'].min()
        
        # Check for bearish manipulation (break below Tokyo low)
        if london_low < tokyo_low:
            extension_points = tokyo_low - london_low
            self.results.append({
                'Date': trading_date,
                'Type': 'Bearish',
                'Tokyo_High': tokyo_high,
                'Tokyo_Low': tokyo_low,
                'Manipulation_Extreme': london_low,
                'Extension_Points': extension_points
            })
        
        # Check for bullish manipulation (break above Tokyo high)
        elif london_high > tokyo_high:
            extension_points = london_high - tokyo_high
            self.results.append({
                'Date': trading_date,
                'Type': 'Bullish',
                'Tokyo_High': tokyo_high,
                'Tokyo_Low': tokyo_low,
                'Manipulation_Extreme': london_high,
                'Extension_Points': extension_points
            })
    
    def calculate_statistics(self):
        """
        Calculate and display statistics from the backtest results.
        """
        if not self.results:
            print("No Judas Swing patterns detected in the data.")
            return
        
        results_df = pd.DataFrame(self.results)
        
        # Overall statistics
        total_occurrences = len(results_df)
        bearish_count = len(results_df[results_df['Type'] == 'Bearish'])
        bullish_count = len(results_df[results_df['Type'] == 'Bullish'])
        
        avg_extension_all = results_df['Extension_Points'].mean()
        avg_extension_bearish = results_df[results_df['Type'] == 'Bearish']['Extension_Points'].mean() if bearish_count > 0 else 0
        avg_extension_bullish = results_df[results_df['Type'] == 'Bullish']['Extension_Points'].mean() if bullish_count > 0 else 0
        
        # Calculate percentiles
        p25 = results_df['Extension_Points'].quantile(0.25)
        p50 = results_df['Extension_Points'].quantile(0.50)
        p75 = results_df['Extension_Points'].quantile(0.75)
        p90 = results_df['Extension_Points'].quantile(0.90)
        
        min_extension = results_df['Extension_Points'].min()
        max_extension = results_df['Extension_Points'].max()
        
        # Total days analyzed
        total_days = self.df['Date_Only'].nunique()
        
        # Print statistics
        print("=" * 70)
        print("JUDAS SWING BACKTEST RESULTS")
        print("=" * 70)
        print(f"\nDATA SUMMARY:")
        print(f"  Total trading days analyzed: {total_days}")
        print(f"  Date range: {self.df['DateTime'].min().date()} to {self.df['DateTime'].max().date()}")
        print(f"\nMANIPULATION OCCURRENCES:")
        print(f"  Total Tokyo range breaks (01:00-05:00): {total_occurrences}")
        print(f"  Bearish manipulations (break below Tokyo low): {bearish_count} ({bearish_count/total_occurrences*100:.1f}%)")
        print(f"  Bullish manipulations (break above Tokyo high): {bullish_count} ({bullish_count/total_occurrences*100:.1f}%)")
        print(f"  Percentage of days with manipulation: {total_occurrences/total_days*100:.1f}%")
        print(f"\nEXTENSION STATISTICS (in points):")
        print(f"  Average extension (all): {avg_extension_all:.2f}")
        print(f"  Average extension (bearish): {avg_extension_bearish:.2f}")
        print(f"  Average extension (bullish): {avg_extension_bullish:.2f}")
        print(f"\nEXTENSION DISTRIBUTION:")
        print(f"  Minimum: {min_extension:.2f}")
        print(f"  25th percentile: {p25:.2f}")
        print(f"  Median (50th percentile): {p50:.2f}")
        print(f"  75th percentile: {p75:.2f}")
        print(f"  90th percentile: {p90:.2f}")
        print(f"  Maximum: {max_extension:.2f}")
        print("=" * 70)
        
        return results_df
    
    def plot_distribution(self, results_df, save_path='judas_swing_distribution.png'):
        """
        Create and save a histogram showing the distribution of extensions.
        
        Parameters:
        -----------
        results_df : DataFrame
            Results dataframe from calculate_statistics
        save_path : str
            Path to save the histogram
        """
        if results_df is None or len(results_df) == 0:
            print("No data to plot.")
            return
        
        # Create figure with two subplots
        fig, axes = plt.subplots(2, 1, figsize=(14, 10))
        
        # Overall distribution
        ax1 = axes[0]
        ax1.hist(results_df['Extension_Points'], bins=50, color='steelblue', 
                 edgecolor='black', alpha=0.7)
        ax1.axvline(results_df['Extension_Points'].mean(), color='red', 
                    linestyle='--', linewidth=2, label=f'Mean: {results_df["Extension_Points"].mean():.2f}')
        ax1.axvline(results_df['Extension_Points'].median(), color='green', 
                    linestyle='--', linewidth=2, label=f'Median: {results_df["Extension_Points"].median():.2f}')
        ax1.set_xlabel('Extension Beyond Tokyo Range (points)', fontsize=12)
        ax1.set_ylabel('Frequency', fontsize=12)
        ax1.set_title('Judas Swing Extension Distribution - All Manipulations', 
                      fontsize=14, fontweight='bold')
        ax1.legend(fontsize=10)
        ax1.grid(True, alpha=0.3)
        
        # Split by type
        ax2 = axes[1]
        bearish_data = results_df[results_df['Type'] == 'Bearish']['Extension_Points']
        bullish_data = results_df[results_df['Type'] == 'Bullish']['Extension_Points']
        
        if len(bearish_data) > 0:
            ax2.hist(bearish_data, bins=30, color='red', alpha=0.5, 
                     label=f'Bearish (n={len(bearish_data)}, avg={bearish_data.mean():.2f})', 
                     edgecolor='black')
        
        if len(bullish_data) > 0:
            ax2.hist(bullish_data, bins=30, color='green', alpha=0.5, 
                     label=f'Bullish (n={len(bullish_data)}, avg={bullish_data.mean():.2f})', 
                     edgecolor='black')
        
        ax2.set_xlabel('Extension Beyond Tokyo Range (points)', fontsize=12)
        ax2.set_ylabel('Frequency', fontsize=12)
        ax2.set_title('Judas Swing Extension Distribution - By Manipulation Type', 
                      fontsize=14, fontweight='bold')
        ax2.legend(fontsize=10)
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"\nHistogram saved to: {save_path}")
        plt.close()
    
    def export_results(self, results_df, csv_path='judas_swing_results.csv'):
        """
        Export detailed results to CSV file.
        
        Parameters:
        -----------
        results_df : DataFrame
            Results dataframe from calculate_statistics
        csv_path : str
            Path to save the CSV file
        """
        if results_df is None or len(results_df) == 0:
            print("No data to export.")
            return
        
        results_df.to_csv(csv_path, index=False)
        print(f"Detailed results exported to: {csv_path}")
    
    def run(self):
        """
        Execute the complete backtest workflow.
        """
        print("\n" + "=" * 70)
        print("JUDAS SWING BACKTEST - NASDAQ 100 (NQ)")
        print("=" * 70 + "\n")
        
        # Step 1: Load data
        self.load_data()
        
        # Step 2: Identify sessions and analyze
        self.identify_sessions()
        
        # Step 3: Calculate and display statistics
        results_df = self.calculate_statistics()
        
        # Step 4: Create visualizations
        if results_df is not None and len(results_df) > 0:
            self.plot_distribution(results_df)
            self.export_results(results_df)
        
        print("\nBacktest complete!")
        print("=" * 70 + "\n")
        
        return results_df


def main():
    """
    Main entry point for the script.
    """
    # Configuration
    # Set data_source to 'single' to load NQ_Data.csv
    # Set data_source to 'combined' to load multiple yearly files
    DATA_SOURCE = 'combined'
    
    # Years to analyze (only used when data_source='combined')
    YEARS_TO_ANALYZE = [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]
    
    # Create backtest instance
    backtest = JudasSwingBacktest(
        data_source=DATA_SOURCE,
        years=YEARS_TO_ANALYZE
    )
    
    # Run the backtest
    results = backtest.run()
    
    return results


if __name__ == "__main__":
    main()

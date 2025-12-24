#!/usr/bin/env python3
"""
Judas Swing Analyzer for NQ (Nasdaq 100) Trading Data

This script analyzes trading data to identify and measure "Judas Swings" - 
false breakouts during the London Killzone that reverse direction.

Author: Trading Analysis System
Date: 2025-12-24
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta, time
import sys
import argparse


class JudasSwingAnalyzer:
    """
    Analyzes trading data to detect Judas Swings and calculate their metrics.
    
    A Judas Swing occurs when:
    1. Price breaks Asian Range (High or Low) during London Killzone (01:00-04:00)
    2. BUT the 04:00 candle closes on the opposite side (inside range or past Midnight Open)
    3. This represents a false breakout/liquidity trap
    """
    
    # Time constants to avoid repeated parsing
    ASIAN_START_TIME = time(18, 0, 0)
    ASIAN_END_TIME = time(23, 0, 0)
    MIDNIGHT_CANDLE_TIME = time(23, 0, 0)  # Same as ASIAN_END_TIME but used to get the open price
    KILLZONE_START_TIME = time(1, 0, 0)
    KILLZONE_END_TIME = time(4, 0, 0)
    
    def __init__(self, csv_path):
        """
        Initialize the analyzer with a CSV file path.
        
        Args:
            csv_path (str): Path to the CSV file containing trading data
        """
        self.csv_path = csv_path
        self.df = None
        self.judas_swings = []
        
    def load_data(self):
        """
        Load and preprocess the CSV data.
        
        Returns:
            bool: True if data loaded successfully, False otherwise
        """
        try:
            # Load CSV with semicolon separator
            self.df = pd.read_csv(
                self.csv_path, 
                sep=';',
                names=['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume'],
                skiprows=1  # Skip header row
            )
            
            # Combine Date and Time into a single datetime column
            self.df['DateTime'] = pd.to_datetime(
                self.df['Date'] + ' ' + self.df['Time'],
                format='%d/%m/%Y %H:%M:%S'
            )
            
            # Set DateTime as index
            self.df.set_index('DateTime', inplace=True)
            
            # Ensure numeric columns are float type
            for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
                self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
            
            # Sort by datetime
            self.df.sort_index(inplace=True)
            
            # Extract date and time components for easier filtering
            self.df['DateOnly'] = self.df.index.date
            self.df['TimeOnly'] = self.df.index.time
            
            print(f"✓ Successfully loaded {len(self.df)} candles from {self.csv_path}")
            print(f"✓ Date range: {self.df.index[0].date()} to {self.df.index[-1].date()}")
            
            return True
            
        except FileNotFoundError:
            print(f"✗ Error: File not found: {self.csv_path}")
            return False
        except Exception as e:
            print(f"✗ Error loading data: {str(e)}")
            return False
    
    def get_asian_range(self, target_date):
        """
        Calculate the Asian Range for a given date.
        Asian Range: High and Low between 18:00 (D-1) and 23:00 (D-1)
        
        Args:
            target_date: The date for which to calculate the range (D)
            
        Returns:
            tuple: (asian_high, asian_low) or (None, None) if insufficient data
        """
        # Asian session is from 18:00 on previous day to 23:00 on previous day
        prev_date = target_date - timedelta(days=1)
        
        # Filter data for Asian session (excluding 23:00 to avoid overlap with midnight candle)
        asian_data = self.df[
            (self.df['DateOnly'] == prev_date) &
            (self.df.index.time >= self.ASIAN_START_TIME) &
            (self.df.index.time < self.ASIAN_END_TIME)
        ]
        
        if len(asian_data) == 0:
            return None, None
        
        asian_high = asian_data['High'].max()
        asian_low = asian_data['Low'].min()
        
        return asian_high, asian_low
    
    def get_midnight_open(self, target_date):
        """
        Get the Midnight Open price (open at 23:00 on D-1).
        
        Args:
            target_date: The date (D)
            
        Returns:
            float: Midnight open price or None if not found
        """
        prev_date = target_date - timedelta(days=1)
        
        # Find the 23:00 candle on previous day
        midnight_candle = self.df[
            (self.df['DateOnly'] == prev_date) &
            (self.df.index.time == self.MIDNIGHT_CANDLE_TIME)
        ]
        
        if len(midnight_candle) == 0:
            return None
        
        return midnight_candle['Open'].iloc[0]
    
    def get_killzone_data(self, target_date):
        """
        Get data for the London Killzone (01:00 to 04:00 on D).
        
        Args:
            target_date: The date (D)
            
        Returns:
            DataFrame: Killzone candles or empty DataFrame
        """
        # Get data for the London Killzone (inclusive of both start and end times)
        killzone_data = self.df[
            (self.df['DateOnly'] == target_date) &
            (self.df.index.time >= self.KILLZONE_START_TIME) &
            (self.df.index.time <= self.KILLZONE_END_TIME)
        ]
        
        return killzone_data
    
    def detect_judas_swing(self, target_date):
        """
        Detect if a Judas Swing occurred on the given date.
        
        A Judas Swing is:
        - Bearish Judas (Bull Trap): Price breaks Asian High during Killzone but 04:00 closes below Midnight Open
        - Bullish Judas (Bear Trap): Price breaks Asian Low during Killzone but 04:00 closes above Midnight Open
        
        Args:
            target_date: The date to analyze
            
        Returns:
            dict: Judas Swing details or None if no valid swing detected
        """
        # Get required data
        asian_high, asian_low = self.get_asian_range(target_date)
        midnight_open = self.get_midnight_open(target_date)
        killzone_data = self.get_killzone_data(target_date)
        
        # Check if we have all required data
        if asian_high is None or asian_low is None or midnight_open is None or len(killzone_data) == 0:
            return None
        
        # Get killzone metrics
        killzone_high = killzone_data['High'].max()
        killzone_low = killzone_data['Low'].min()
        
        # Get 04:00 closing candle
        close_04 = killzone_data[
            killzone_data.index.time == self.KILLZONE_END_TIME
        ]
        
        if len(close_04) == 0:
            return None
        
        close_04_price = close_04['Close'].iloc[0]
        
        # Check for Bearish Judas (Bull Trap)
        # Price breaks above Asian High during killzone but closes below Midnight Open at 04:00
        if killzone_high > asian_high and close_04_price < midnight_open:
            # Calculate time to peak (when the high was reached)
            peak_candle = killzone_data[killzone_data['High'] == killzone_high].iloc[0]
            peak_time = peak_candle.name
            
            # Calculate minutes from 01:00 to peak
            killzone_start = datetime.combine(target_date, self.KILLZONE_START_TIME)
            time_to_peak = int((peak_time - killzone_start).total_seconds() / 60)
            
            # Calculate extension (magnitude)
            extension = killzone_high - asian_high
            
            return {
                'date': target_date,
                'type': 'Bearish (Bull Trap)',
                'asian_high': asian_high,
                'asian_low': asian_low,
                'midnight_open': midnight_open,
                'killzone_high': killzone_high,
                'killzone_low': killzone_low,
                'close_04': close_04_price,
                'extension': extension,
                'time_to_peak_minutes': time_to_peak,
                'peak_time': peak_time.strftime('%H:%M:%S')
            }
        
        # Check for Bullish Judas (Bear Trap)
        # Price breaks below Asian Low during killzone but closes above Midnight Open at 04:00
        elif killzone_low < asian_low and close_04_price > midnight_open:
            # Calculate time to peak (when the low was reached)
            peak_candle = killzone_data[killzone_data['Low'] == killzone_low].iloc[0]
            peak_time = peak_candle.name
            
            # Calculate minutes from 01:00 to peak
            killzone_start = datetime.combine(target_date, self.KILLZONE_START_TIME)
            time_to_peak = int((peak_time - killzone_start).total_seconds() / 60)
            
            # Calculate extension (magnitude)
            extension = asian_low - killzone_low
            
            return {
                'date': target_date,
                'type': 'Bullish (Bear Trap)',
                'asian_high': asian_high,
                'asian_low': asian_low,
                'midnight_open': midnight_open,
                'killzone_high': killzone_high,
                'killzone_low': killzone_low,
                'close_04': close_04_price,
                'extension': extension,
                'time_to_peak_minutes': time_to_peak,
                'peak_time': peak_time.strftime('%H:%M:%S')
            }
        
        return None
    
    def analyze(self):
        """
        Analyze the entire dataset to find all Judas Swings.
        
        Returns:
            bool: True if analysis completed successfully
        """
        if self.df is None:
            print("✗ Error: No data loaded. Call load_data() first.")
            return False
        
        print("\n" + "="*70)
        print("ANALYZING JUDAS SWINGS")
        print("="*70)
        
        # Get unique dates in the dataset
        unique_dates = self.df['DateOnly'].unique()
        
        # Analyze each date
        for date in unique_dates:
            swing = self.detect_judas_swing(date)
            if swing:
                self.judas_swings.append(swing)
        
        print(f"\n✓ Analysis complete. Found {len(self.judas_swings)} valid Judas Swings.")
        
        return True
    
    def generate_report(self):
        """
        Generate a comprehensive statistical report of all detected Judas Swings.
        """
        if len(self.judas_swings) == 0:
            print("\n" + "="*70)
            print("JUDAS SWING ANALYSIS REPORT")
            print("="*70)
            print("\n⚠ No valid Judas Swings detected in the dataset.")
            print("\nPossible reasons:")
            print("  - The market didn't produce any false breakouts during the analysis period")
            print("  - Data quality issues or missing time periods")
            print("  - Parameters need adjustment for this specific market behavior")
            return
        
        # Convert to DataFrame for easier analysis
        df_swings = pd.DataFrame(self.judas_swings)
        
        # Separate by type
        bearish_swings = df_swings[df_swings['type'] == 'Bearish (Bull Trap)']
        bullish_swings = df_swings[df_swings['type'] == 'Bullish (Bear Trap)']
        
        print("\n" + "="*70)
        print("JUDAS SWING ANALYSIS REPORT")
        print("="*70)
        
        # Overall Statistics
        print(f"\n{'OVERALL STATISTICS':-^70}")
        print(f"\nTotal Judas Swings Detected: {len(self.judas_swings)}")
        print(f"  - Bearish (Bull Traps):    {len(bearish_swings)} ({len(bearish_swings)/len(self.judas_swings)*100:.1f}%)")
        print(f"  - Bullish (Bear Traps):    {len(bullish_swings)} ({len(bullish_swings)/len(self.judas_swings)*100:.1f}%)")
        
        # Extension Analysis
        print(f"\n{'EXTENSION ANALYSIS (Magnitude of False Breakout)':-^70}")
        print(f"\nAll Judas Swings:")
        print(f"  Mean Extension:      {df_swings['extension'].mean():.2f} points")
        print(f"  Median Extension:    {df_swings['extension'].median():.2f} points")
        print(f"  Max Extension:       {df_swings['extension'].max():.2f} points")
        print(f"  Min Extension:       {df_swings['extension'].min():.2f} points")
        print(f"  Std Deviation:       {df_swings['extension'].std():.2f} points")
        
        if len(bearish_swings) > 0:
            print(f"\nBearish Judas (Bull Traps):")
            print(f"  Mean Extension:      {bearish_swings['extension'].mean():.2f} points")
            print(f"  Median Extension:    {bearish_swings['extension'].median():.2f} points")
            print(f"  Max Extension:       {bearish_swings['extension'].max():.2f} points")
        
        if len(bullish_swings) > 0:
            print(f"\nBullish Judas (Bear Traps):")
            print(f"  Mean Extension:      {bullish_swings['extension'].mean():.2f} points")
            print(f"  Median Extension:    {bullish_swings['extension'].median():.2f} points")
            print(f"  Max Extension:       {bullish_swings['extension'].max():.2f} points")
        
        # Temporal Analysis
        print(f"\n{'TEMPORAL ANALYSIS (Time to Peak)':-^70}")
        print(f"\nAverage Time to Peak: {df_swings['time_to_peak_minutes'].mean():.1f} minutes")
        print(f"Median Time to Peak:  {df_swings['time_to_peak_minutes'].median():.1f} minutes")
        print(f"Fastest Peak:         {df_swings['time_to_peak_minutes'].min()} minutes")
        print(f"Slowest Peak:         {df_swings['time_to_peak_minutes'].max()} minutes")
        
        # Time distribution histogram (30-min intervals)
        print(f"\nDistribution by 30-minute intervals:")
        time_bins = [0, 30, 60, 90, 120, 150, 180, float('inf')]
        time_labels = ['0-30', '30-60', '60-90', '90-120', '120-150', '150-180', '180+']
        
        df_swings['time_bin'] = pd.cut(
            df_swings['time_to_peak_minutes'], 
            bins=time_bins,
            labels=time_labels,
            right=False
        )
        
        time_distribution = df_swings['time_bin'].value_counts().sort_index()
        
        # Visual scaling factor for bar chart (percentage / BAR_SCALE_FACTOR = bar length)
        BAR_SCALE_FACTOR = 2
        
        for interval, count in time_distribution.items():
            percentage = (count / len(df_swings)) * 100
            bar = '█' * int(percentage / BAR_SCALE_FACTOR)
            print(f"  {interval:>10} min: {bar:20} {count:3d} ({percentage:5.1f}%)")
        
        # Top 5 Most Violent Judas Swings
        print(f"\n{'TOP 5 MOST VIOLENT JUDAS SWINGS':-^70}")
        print(f"\n{'Date':<12} {'Type':<25} {'Extension':>12} {'Peak Time':>10}")
        print("-" * 70)
        
        top_5 = df_swings.nlargest(5, 'extension')
        for _, swing in top_5.iterrows():
            date_str = swing['date'].strftime('%Y-%m-%d')
            print(f"{date_str:<12} {swing['type']:<25} {swing['extension']:>12.2f} {swing['peak_time']:>10}")
        
        # Additional Insights
        print(f"\n{'ADDITIONAL INSIGHTS':-^70}")
        
        # Monthly distribution
        df_swings['month'] = pd.to_datetime(df_swings['date']).dt.to_period('M')
        monthly_counts = df_swings['month'].value_counts().sort_index()
        
        if len(monthly_counts) > 1:
            print(f"\nMonthly Distribution:")
            for month, count in monthly_counts.items():
                print(f"  {month}: {count} swings")
        
        # Average extension by type
        print(f"\nAverage Extension Comparison:")
        if len(bearish_swings) > 0:
            print(f"  Bull Traps (Bearish):  {bearish_swings['extension'].mean():.2f} points")
        if len(bullish_swings) > 0:
            print(f"  Bear Traps (Bullish):  {bullish_swings['extension'].mean():.2f} points")
        
        print("\n" + "="*70)
        print("END OF REPORT")
        print("="*70 + "\n")
    
    def export_results(self, output_path=None):
        """
        Export detailed results to a CSV file.
        
        Args:
            output_path (str): Path to output CSV file
        """
        if len(self.judas_swings) == 0:
            print("No Judas Swings to export.")
            return
        
        if output_path is None:
            output_path = self.csv_path.replace('.csv', '_judas_swings.csv')
        
        df_export = pd.DataFrame(self.judas_swings)
        df_export.to_csv(output_path, index=False)
        print(f"\n✓ Results exported to: {output_path}")


def main():
    """
    Main entry point for the script.
    """
    parser = argparse.ArgumentParser(
        description='Analyze Judas Swings in NQ trading data',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python judas_swing_analyzer.py
  python judas_swing_analyzer.py --file "2024 15m.csv"
  python judas_swing_analyzer.py --file "2024 15m.csv" --export results.csv
        """
    )
    
    parser.add_argument(
        '--file', '-f',
        default='2024 15m.csv',
        help='Path to CSV file (default: 2024 15m.csv)'
    )
    
    parser.add_argument(
        '--export', '-e',
        help='Export results to CSV file'
    )
    
    args = parser.parse_args()
    
    print("="*70)
    print("JUDAS SWING ANALYZER - NQ Trading Data Analysis")
    print("="*70)
    print(f"\nAnalyzing: {args.file}")
    print("\nDefinition:")
    print("  A Judas Swing is a false breakout during London Killzone (01:00-04:00)")
    print("  that reverses by the 04:00 close, trapping traders on the wrong side.")
    print()
    
    # Create analyzer instance
    analyzer = JudasSwingAnalyzer(args.file)
    
    # Load data
    if not analyzer.load_data():
        sys.exit(1)
    
    # Analyze data
    if not analyzer.analyze():
        sys.exit(1)
    
    # Generate report
    analyzer.generate_report()
    
    # Export if requested
    if args.export:
        analyzer.export_results(args.export)
    
    print("✓ Analysis complete!\n")


if __name__ == "__main__":
    main()

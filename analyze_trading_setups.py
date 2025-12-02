#!/usr/bin/env python3
"""
Trading Setup Pattern Analyzer

This script analyzes trading data from 2018 to today for specific setup patterns:
1. Bearish Setup: 8:30 AM candle is bearish, next candle is bullish and closes above max of last 5 candles
2. Bullish Setup: 8:30 AM candle is bullish, next candle is bearish and closes below min of last 5 candles

Data analyzed: 1-minute, 5-minute, and 15-minute timeframes
"""

import pandas as pd
import zipfile
import os
from datetime import datetime, time
from typing import List, Dict, Tuple
import io

class TradingSetupAnalyzer:
    def __init__(self, base_path: str, start_year: int = 2018, end_year: int = 2025):
        self.base_path = base_path
        self.years = list(range(start_year, end_year + 1))
        self.timeframes = ['1m', '5m', '15m']
        self.results = {tf: {'bearish_setups': [], 'bullish_setups': []} for tf in self.timeframes}
        
    def load_data(self, year: int, timeframe: str) -> pd.DataFrame:
        """Load data for a specific year and timeframe"""
        filename = f"{year} {timeframe}.csv"
        filepath = os.path.join(self.base_path, filename)
        
        # For 1m data from 2018-2024, read from zip files
        if timeframe == '1m' and year < 2025:
            zip_filename = f"{year} {timeframe}.csv.zip"
            zip_filepath = os.path.join(self.base_path, zip_filename)
            
            if not os.path.exists(zip_filepath):
                print(f"Warning: {zip_filename} not found")
                return pd.DataFrame()
            
            try:
                with zipfile.ZipFile(zip_filepath, 'r') as zip_ref:
                    # Get the name of the CSV file inside the zip
                    csv_filename = zip_ref.namelist()[0]
                    with zip_ref.open(csv_filename) as csv_file:
                        df = pd.read_csv(csv_file, sep=';', header=0)
            except Exception as e:
                print(f"Error reading {zip_filename}: {e}")
                return pd.DataFrame()
        else:
            # For other files, read directly
            if not os.path.exists(filepath):
                print(f"Warning: {filename} not found")
                return pd.DataFrame()
            
            try:
                df = pd.read_csv(filepath, sep=';', header=0)
            except Exception as e:
                print(f"Error reading {filename}: {e}")
                return pd.DataFrame()
        
        # Rename columns for easier access
        df.columns = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
        
        # Parse datetime
        df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%d/%m/%Y %H:%M:%S')
        df['TimeOnly'] = pd.to_datetime(df['Time'], format='%H:%M:%S').dt.time
        
        # Convert price columns to float
        for col in ['Open', 'High', 'Low', 'Close']:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        return df
    
    def is_bearish_candle(self, row: pd.Series) -> bool:
        """Check if a candle is bearish (Close < Open)"""
        return row['Close'] < row['Open']
    
    def is_bullish_candle(self, row: pd.Series) -> bool:
        """Check if a candle is bullish (Close > Open)"""
        return row['Close'] > row['Open']
    
    def find_setups(self, df: pd.DataFrame, timeframe: str) -> Tuple[List[Dict], List[Dict]]:
        """
        Find both setup patterns in the data
        
        Returns:
            Tuple of (bearish_setups, bullish_setups)
        """
        bearish_setups = []
        bullish_setups = []
        
        if len(df) < 7:  # Need at least 7 candles (5 previous + 8:30 + next)
            return bearish_setups, bullish_setups
        
        # Define 8:30 AM time
        target_time = time(8, 30, 0)
        
        # Iterate through the dataframe
        for i in range(5, len(df) - 1):  # Need 5 previous candles and 1 next candle
            current_row = df.iloc[i]
            next_row = df.iloc[i + 1]
            
            # Check if current candle is at 8:30 AM
            if current_row['TimeOnly'] != target_time:
                continue
            
            # Get the last 5 candles before 8:30 AM
            prev_5_candles = df.iloc[i-5:i]
            max_of_last_5 = prev_5_candles['High'].max()
            min_of_last_5 = prev_5_candles['Low'].min()
            
            # BEARISH SETUP: 8:30 bearish, next bullish and closes above max of last 5
            if self.is_bearish_candle(current_row) and self.is_bullish_candle(next_row):
                if next_row['Close'] > max_of_last_5:
                    setup = {
                        'date': current_row['Date'],
                        'time_830': current_row['Time'],
                        'time_next': next_row['Time'],
                        'open_830': current_row['Open'],
                        'high_830': current_row['High'],
                        'low_830': current_row['Low'],
                        'close_830': current_row['Close'],
                        'open_next': next_row['Open'],
                        'high_next': next_row['High'],
                        'low_next': next_row['Low'],
                        'close_next': next_row['Close'],
                        'max_last_5': max_of_last_5,
                        'min_last_5': min_of_last_5,
                        'close_above_max_by': next_row['Close'] - max_of_last_5,
                        'timeframe': timeframe
                    }
                    bearish_setups.append(setup)
            
            # BULLISH SETUP: 8:30 bullish, next bearish and closes below min of last 5
            if self.is_bullish_candle(current_row) and self.is_bearish_candle(next_row):
                if next_row['Close'] < min_of_last_5:
                    setup = {
                        'date': current_row['Date'],
                        'time_830': current_row['Time'],
                        'time_next': next_row['Time'],
                        'open_830': current_row['Open'],
                        'high_830': current_row['High'],
                        'low_830': current_row['Low'],
                        'close_830': current_row['Close'],
                        'open_next': next_row['Open'],
                        'high_next': next_row['High'],
                        'low_next': next_row['Low'],
                        'close_next': next_row['Close'],
                        'max_last_5': max_of_last_5,
                        'min_last_5': min_of_last_5,
                        'close_below_min_by': min_of_last_5 - next_row['Close'],
                        'timeframe': timeframe
                    }
                    bullish_setups.append(setup)
        
        return bearish_setups, bullish_setups
    
    def analyze_all_data(self):
        """Analyze all years and timeframes"""
        print("=" * 80)
        print("TRADING SETUP PATTERN ANALYZER")
        print("=" * 80)
        print(f"Analysis Period: 2018-2025")
        print(f"Timeframes: {', '.join(self.timeframes)}")
        print("=" * 80)
        print()
        
        for timeframe in self.timeframes:
            print(f"\nProcessing {timeframe} data...")
            
            for year in self.years:
                print(f"  Loading {year}...", end=" ")
                df = self.load_data(year, timeframe)
                
                if df.empty:
                    print("SKIPPED (no data)")
                    continue
                
                bearish, bullish = self.find_setups(df, timeframe)
                self.results[timeframe]['bearish_setups'].extend(bearish)
                self.results[timeframe]['bullish_setups'].extend(bullish)
                
                print(f"✓ (Bearish: {len(bearish)}, Bullish: {len(bullish)})")
        
        print("\nAnalysis complete!")
    
    def generate_report(self, output_file: str = "trading_setup_report.txt"):
        """Generate a detailed report of the findings"""
        report_lines = []
        
        # Header
        report_lines.append("=" * 100)
        report_lines.append("TRADING SETUP PATTERN ANALYSIS REPORT")
        report_lines.append("=" * 100)
        report_lines.append(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append(f"Analysis Period: 2018 - 2025")
        report_lines.append("")
        
        # Setup Definitions
        report_lines.append("SETUP DEFINITIONS:")
        report_lines.append("-" * 100)
        report_lines.append("1. BEARISH SETUP:")
        report_lines.append("   - 8:30 AM candle is BEARISH (Close < Open)")
        report_lines.append("   - Next candle is BULLISH (Close > Open)")
        report_lines.append("   - Next candle closes ABOVE the maximum of the last 5 candles")
        report_lines.append("")
        report_lines.append("2. BULLISH SETUP:")
        report_lines.append("   - 8:30 AM candle is BULLISH (Close > Open)")
        report_lines.append("   - Next candle is BEARISH (Close < Open)")
        report_lines.append("   - Next candle closes BELOW the minimum of the last 5 candles")
        report_lines.append("")
        report_lines.append("=" * 100)
        report_lines.append("")
        
        # Summary Statistics
        report_lines.append("SUMMARY STATISTICS")
        report_lines.append("=" * 100)
        report_lines.append("")
        
        total_bearish = 0
        total_bullish = 0
        
        for timeframe in self.timeframes:
            bearish_count = len(self.results[timeframe]['bearish_setups'])
            bullish_count = len(self.results[timeframe]['bullish_setups'])
            total_bearish += bearish_count
            total_bullish += bullish_count
            
            report_lines.append(f"{timeframe.upper()} Timeframe:")
            report_lines.append(f"  Bearish Setups: {bearish_count}")
            report_lines.append(f"  Bullish Setups: {bullish_count}")
            report_lines.append(f"  Total Setups:   {bearish_count + bullish_count}")
            report_lines.append("")
        
        report_lines.append("-" * 100)
        report_lines.append(f"GRAND TOTAL:")
        report_lines.append(f"  Total Bearish Setups: {total_bearish}")
        report_lines.append(f"  Total Bullish Setups: {total_bullish}")
        report_lines.append(f"  Total All Setups:     {total_bearish + total_bullish}")
        report_lines.append("")
        report_lines.append("=" * 100)
        report_lines.append("")
        
        # Detailed Setup Information
        for timeframe in self.timeframes:
            report_lines.append("")
            report_lines.append("=" * 100)
            report_lines.append(f"DETAILED SETUPS - {timeframe.upper()} TIMEFRAME")
            report_lines.append("=" * 100)
            report_lines.append("")
            
            # Bearish Setups
            bearish_setups = self.results[timeframe]['bearish_setups']
            report_lines.append(f"BEARISH SETUPS ({len(bearish_setups)} found)")
            report_lines.append("-" * 100)
            
            if bearish_setups:
                for idx, setup in enumerate(bearish_setups, 1):
                    report_lines.append(f"\n#{idx}. Date: {setup['date']}")
                    report_lines.append(f"    8:30 AM Candle (Bearish):")
                    report_lines.append(f"      Time: {setup['time_830']}")
                    report_lines.append(f"      Open:  {setup['open_830']:.2f}")
                    report_lines.append(f"      High:  {setup['high_830']:.2f}")
                    report_lines.append(f"      Low:   {setup['low_830']:.2f}")
                    report_lines.append(f"      Close: {setup['close_830']:.2f}")
                    report_lines.append(f"    Next Candle (Bullish):")
                    report_lines.append(f"      Time: {setup['time_next']}")
                    report_lines.append(f"      Open:  {setup['open_next']:.2f}")
                    report_lines.append(f"      High:  {setup['high_next']:.2f}")
                    report_lines.append(f"      Low:   {setup['low_next']:.2f}")
                    report_lines.append(f"      Close: {setup['close_next']:.2f}")
                    report_lines.append(f"    Key Levels:")
                    report_lines.append(f"      Max of Last 5 Candles: {setup['max_last_5']:.2f}")
                    report_lines.append(f"      Close Above Max By:    {setup['close_above_max_by']:.2f}")
            else:
                report_lines.append("  No bearish setups found.")
            
            report_lines.append("")
            report_lines.append("-" * 100)
            
            # Bullish Setups
            bullish_setups = self.results[timeframe]['bullish_setups']
            report_lines.append(f"\nBULLISH SETUPS ({len(bullish_setups)} found)")
            report_lines.append("-" * 100)
            
            if bullish_setups:
                for idx, setup in enumerate(bullish_setups, 1):
                    report_lines.append(f"\n#{idx}. Date: {setup['date']}")
                    report_lines.append(f"    8:30 AM Candle (Bullish):")
                    report_lines.append(f"      Time: {setup['time_830']}")
                    report_lines.append(f"      Open:  {setup['open_830']:.2f}")
                    report_lines.append(f"      High:  {setup['high_830']:.2f}")
                    report_lines.append(f"      Low:   {setup['low_830']:.2f}")
                    report_lines.append(f"      Close: {setup['close_830']:.2f}")
                    report_lines.append(f"    Next Candle (Bearish):")
                    report_lines.append(f"      Time: {setup['time_next']}")
                    report_lines.append(f"      Open:  {setup['open_next']:.2f}")
                    report_lines.append(f"      High:  {setup['high_next']:.2f}")
                    report_lines.append(f"      Low:   {setup['low_next']:.2f}")
                    report_lines.append(f"      Close: {setup['close_next']:.2f}")
                    report_lines.append(f"    Key Levels:")
                    report_lines.append(f"      Min of Last 5 Candles: {setup['min_last_5']:.2f}")
                    report_lines.append(f"      Close Below Min By:    {setup['close_below_min_by']:.2f}")
            else:
                report_lines.append("  No bullish setups found.")
            
            report_lines.append("")
        
        # Additional Statistics
        report_lines.append("")
        report_lines.append("=" * 100)
        report_lines.append("ADDITIONAL STATISTICS")
        report_lines.append("=" * 100)
        report_lines.append("")
        
        for timeframe in self.timeframes:
            report_lines.append(f"{timeframe.upper()} Timeframe Analysis:")
            
            bearish_setups = self.results[timeframe]['bearish_setups']
            bullish_setups = self.results[timeframe]['bullish_setups']
            
            if bearish_setups:
                avg_break = sum(s['close_above_max_by'] for s in bearish_setups) / len(bearish_setups)
                max_break = max(s['close_above_max_by'] for s in bearish_setups)
                min_break = min(s['close_above_max_by'] for s in bearish_setups)
                
                report_lines.append(f"  Bearish Setup Statistics:")
                report_lines.append(f"    Average breakout above max: {avg_break:.2f}")
                report_lines.append(f"    Maximum breakout above max: {max_break:.2f}")
                report_lines.append(f"    Minimum breakout above max: {min_break:.2f}")
            
            if bullish_setups:
                avg_break = sum(s['close_below_min_by'] for s in bullish_setups) / len(bullish_setups)
                max_break = max(s['close_below_min_by'] for s in bullish_setups)
                min_break = min(s['close_below_min_by'] for s in bullish_setups)
                
                report_lines.append(f"  Bullish Setup Statistics:")
                report_lines.append(f"    Average breakout below min: {avg_break:.2f}")
                report_lines.append(f"    Maximum breakout below min: {max_break:.2f}")
                report_lines.append(f"    Minimum breakout below min: {min_break:.2f}")
            
            report_lines.append("")
        
        report_lines.append("=" * 100)
        report_lines.append("END OF REPORT")
        report_lines.append("=" * 100)
        
        # Write to file
        report_content = "\n".join(report_lines)
        output_path = os.path.join(self.base_path, output_file)
        
        with open(output_path, 'w') as f:
            f.write(report_content)
        
        print(f"\nReport saved to: {output_path}")
        print(f"Report size: {len(report_content)} bytes")
        print("\nTo view the full report, run: cat {0}".format(output_path))
        
        return output_path

def main():
    # Get the base path (use current directory if running from repo, or use absolute path)
    import sys
    base_path = os.path.dirname(os.path.abspath(__file__)) if os.path.dirname(os.path.abspath(__file__)) else os.getcwd()
    
    # Parse command-line arguments if provided
    if len(sys.argv) > 1:
        base_path = sys.argv[1]
    
    print(f"Using base path: {base_path}")
    
    # Create analyzer instance (default: 2018-2025)
    analyzer = TradingSetupAnalyzer(base_path)
    
    # Analyze all data
    analyzer.analyze_all_data()
    
    # Generate report
    analyzer.generate_report()

if __name__ == "__main__":
    main()

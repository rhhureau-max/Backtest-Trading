#!/usr/bin/env python3
"""
Backtesting Strategy Script
Analyzes historical trades from 2018 to today based on 08:30:00 candle conditions.

For bullish candles (close > open): close must be above the highest high of the previous 5 candles
For bearish candles (close < open): close must be below the lowest low of the previous 5 candles
"""

import pandas as pd
import os
import zipfile
from datetime import datetime
from typing import List, Dict, Tuple
import glob


class BacktestStrategy:
    def __init__(self, base_path: str):
        self.base_path = base_path
        self.timeframes = ['1m', '5m', '15m']
        self.years = list(range(2018, 2026))  # 2018 to 2025
        self.results = []
        
    def extract_zip_if_needed(self, zip_path: str) -> str:
        """Extract zip file if it exists and return the path to the CSV file."""
        if not os.path.exists(zip_path):
            return None
            
        csv_path = zip_path.replace('.zip', '')
        
        # Check if already extracted
        if os.path.exists(csv_path):
            print(f"  CSV already extracted: {os.path.basename(csv_path)}")
            return csv_path
            
        print(f"  Extracting: {os.path.basename(zip_path)}")
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(self.base_path)
            return csv_path
        except Exception as e:
            print(f"  Error extracting {zip_path}: {e}")
            return None
    
    def load_data(self, year: int, timeframe: str) -> pd.DataFrame:
        """Load data for a specific year and timeframe."""
        filename = f"{year} {timeframe}.csv"
        filepath = os.path.join(self.base_path, filename)
        
        # For 1m files from 2018-2024, check if we need to extract from zip
        if timeframe == '1m' and year < 2025:
            zip_path = filepath + '.zip'
            csv_path = self.extract_zip_if_needed(zip_path)
            if csv_path:
                filepath = csv_path
            elif not os.path.exists(filepath):
                print(f"  File not found: {filename}")
                return None
        
        if not os.path.exists(filepath):
            print(f"  File not found: {filename}")
            return None
        
        try:
            # Read CSV with semicolon separator
            df = pd.read_csv(filepath, sep=';', header=0)
            
            # Rename columns for easier access
            df.columns = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
            
            # Convert price columns to float
            for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # Create datetime column
            df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%d/%m/%Y %H:%M:%S', errors='coerce')
            
            # Sort by datetime
            df = df.sort_values('Datetime').reset_index(drop=True)
            
            print(f"  Loaded {len(df)} rows from {filename}")
            return df
            
        except Exception as e:
            print(f"  Error loading {filename}: {e}")
            return None
    
    def check_830_condition(self, df: pd.DataFrame, timeframe: str) -> List[Dict]:
        """
        Check for trades at 08:30:00 that meet the strategy conditions.
        
        Returns a list of trade dictionaries with details.
        """
        trades = []
        
        if df is None or len(df) < 6:
            return trades
        
        # Filter for 08:30:00 candles
        df_830 = df[df['Time'] == '08:30:00'].copy()
        
        for idx in df_830.index:
            # Get the position in the original dataframe
            pos = df.index.get_loc(idx)
            
            # Need at least 5 previous candles
            if pos < 5:
                continue
            
            # Get current candle
            current = df.iloc[pos]
            
            # Get previous 5 candles
            previous_5 = df.iloc[pos-5:pos]
            
            # Skip if any data is missing
            if current.isnull().any() or previous_5.isnull().any().any():
                continue
            
            # Determine if bullish or bearish
            is_bullish = current['Close'] > current['Open']
            is_bearish = current['Close'] < current['Open']
            
            # Skip doji candles (close == open)
            if current['Close'] == current['Open']:
                continue
            
            # Get max high and min low of previous 5 candles
            max_high_prev5 = previous_5['High'].max()
            min_low_prev5 = previous_5['Low'].min()
            
            trade_found = False
            trade_type = None
            
            if is_bullish and current['Close'] > max_high_prev5:
                trade_found = True
                trade_type = 'BULLISH'
            elif is_bearish and current['Close'] < min_low_prev5:
                trade_found = True
                trade_type = 'BEARISH'
            
            if trade_found:
                trade = {
                    'Date': current['Date'],
                    'Time': current['Time'],
                    'Datetime': current['Datetime'],
                    'Timeframe': timeframe,
                    'Type': trade_type,
                    'Open': current['Open'],
                    'High': current['High'],
                    'Low': current['Low'],
                    'Close': current['Close'],
                    'Volume': current['Volume'],
                    'Max_High_Prev5': max_high_prev5,
                    'Min_Low_Prev5': min_low_prev5,
                    'Condition_Met': f"Close ({current['Close']:.2f}) {'>' if is_bullish else '<'} {'Max High' if is_bullish else 'Min Low'} Prev5 ({max_high_prev5 if is_bullish else min_low_prev5:.2f})"
                }
                trades.append(trade)
        
        return trades
    
    def run_backtest(self):
        """Run the backtest for all years and timeframes."""
        print("=" * 80)
        print("BACKTESTING STRATEGY - 08:30:00 CANDLE ANALYSIS")
        print("=" * 80)
        print(f"Period: 2018 - 2025")
        print(f"Timeframes: {', '.join(self.timeframes)}")
        print(f"Target Time: 08:30:00")
        print("=" * 80)
        print()
        
        for timeframe in self.timeframes:
            print(f"\n{'=' * 80}")
            print(f"Processing Timeframe: {timeframe}")
            print(f"{'=' * 80}")
            
            timeframe_trades = []
            
            for year in self.years:
                print(f"\nYear {year}:")
                df = self.load_data(year, timeframe)
                
                if df is not None:
                    trades = self.check_830_condition(df, timeframe)
                    timeframe_trades.extend(trades)
                    print(f"  Found {len(trades)} trades at 08:30:00 meeting conditions")
            
            self.results.extend(timeframe_trades)
            print(f"\nTotal trades for {timeframe}: {len(timeframe_trades)}")
        
        print("\n" + "=" * 80)
        print(f"TOTAL TRADES FOUND: {len(self.results)}")
        print("=" * 80)
    
    def save_results(self, output_file: str = 'backtest_results.csv'):
        """Save results to CSV file."""
        if not self.results:
            print("\nNo trades found to save.")
            return
        
        results_df = pd.DataFrame(self.results)
        
        # Sort by datetime
        results_df = results_df.sort_values('Datetime').reset_index(drop=True)
        
        # Select and order columns for output
        output_columns = [
            'Date', 'Time', 'Timeframe', 'Type', 'Close', 
            'Open', 'High', 'Low', 'Volume',
            'Max_High_Prev5', 'Min_Low_Prev5', 'Condition_Met'
        ]
        
        results_df = results_df[output_columns]
        
        # Save to CSV
        output_path = os.path.join(self.base_path, output_file)
        results_df.to_csv(output_path, index=False, sep=';')
        print(f"\nResults saved to: {output_file}")
        print(f"Total records: {len(results_df)}")
        
        # Generate summary report
        self.generate_summary_report(results_df)
    
    def generate_summary_report(self, results_df: pd.DataFrame):
        """Generate a summary report of the backtest results."""
        report_path = os.path.join(self.base_path, 'backtest_summary.txt')
        
        with open(report_path, 'w') as f:
            f.write("=" * 80 + "\n")
            f.write("BACKTESTING STRATEGY SUMMARY REPORT\n")
            f.write("=" * 80 + "\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Period: 2018 - 2025\n")
            f.write(f"Target Time: 08:30:00\n")
            f.write("=" * 80 + "\n\n")
            
            # Overall statistics
            f.write("OVERALL STATISTICS\n")
            f.write("-" * 80 + "\n")
            f.write(f"Total Trades Found: {len(results_df)}\n")
            f.write(f"Bullish Trades: {len(results_df[results_df['Type'] == 'BULLISH'])}\n")
            f.write(f"Bearish Trades: {len(results_df[results_df['Type'] == 'BEARISH'])}\n\n")
            
            # Statistics by timeframe
            f.write("STATISTICS BY TIMEFRAME\n")
            f.write("-" * 80 + "\n")
            for tf in self.timeframes:
                tf_data = results_df[results_df['Timeframe'] == tf]
                f.write(f"\n{tf} Timeframe:\n")
                f.write(f"  Total Trades: {len(tf_data)}\n")
                f.write(f"  Bullish: {len(tf_data[tf_data['Type'] == 'BULLISH'])}\n")
                f.write(f"  Bearish: {len(tf_data[tf_data['Type'] == 'BEARISH'])}\n")
                
                if len(tf_data) > 0:
                    f.write(f"  Average Close Price: {tf_data['Close'].mean():.2f}\n")
                    f.write(f"  Average Volume: {tf_data['Volume'].mean():.2f}\n")
            
            # Statistics by year
            f.write("\n\nSTATISTICS BY YEAR\n")
            f.write("-" * 80 + "\n")
            results_df['Year'] = pd.to_datetime(results_df['Date'], format='%d/%m/%Y').dt.year
            for year in sorted(results_df['Year'].unique()):
                year_data = results_df[results_df['Year'] == year]
                f.write(f"\n{year}:\n")
                f.write(f"  Total Trades: {len(year_data)}\n")
                f.write(f"  Bullish: {len(year_data[year_data['Type'] == 'BULLISH'])}\n")
                f.write(f"  Bearish: {len(year_data[year_data['Type'] == 'BEARISH'])}\n")
            
            f.write("\n" + "=" * 80 + "\n")
            f.write("END OF REPORT\n")
            f.write("=" * 80 + "\n")
        
        print(f"Summary report saved to: backtest_summary.txt")
        
        # Print summary to console
        print("\n" + "=" * 80)
        print("SUMMARY BY TIMEFRAME")
        print("=" * 80)
        for tf in self.timeframes:
            tf_data = results_df[results_df['Timeframe'] == tf]
            bullish = len(tf_data[tf_data['Type'] == 'BULLISH'])
            bearish = len(tf_data[tf_data['Type'] == 'BEARISH'])
            print(f"{tf:>5}: {len(tf_data):>4} trades (Bullish: {bullish:>3}, Bearish: {bearish:>3})")


def main():
    """Main entry point for the backtest script."""
    # Get the base path (current directory where the script is run)
    base_path = os.path.dirname(os.path.abspath(__file__))
    
    # Create backtest instance
    backtest = BacktestStrategy(base_path)
    
    # Run the backtest
    backtest.run_backtest()
    
    # Save results
    backtest.save_results()
    
    print("\n" + "=" * 80)
    print("BACKTEST COMPLETED SUCCESSFULLY")
    print("=" * 80)
    print("\nOutput files:")
    print("  - backtest_results.csv: Detailed results of all trades found")
    print("  - backtest_summary.txt: Summary report with statistics")
    print("=" * 80)


if __name__ == "__main__":
    main()

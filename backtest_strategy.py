#!/usr/bin/env python3
"""
Backtest Trading Strategy: 8:30 AM Candle Analysis
Analyzes trades from 2018 to 2025 where the 8:30 AM candle meets specific conditions
relative to the previous 5 candles.
"""

import pandas as pd
import numpy as np
import os
import zipfile
import tempfile
from datetime import datetime
from typing import List, Dict, Tuple
import glob


class BacktestStrategy:
    """
    Backtest strategy for analyzing 8:30 AM candles against previous 5 candles.
    """
    
    def __init__(self, base_path: str):
        """
        Initialize the backtest strategy.
        
        Args:
            base_path: Base directory containing the CSV files
        """
        self.base_path = base_path
        self.timeframes = ['1m', '5m', '15m']
        self.years = list(range(2018, 2026))  # 2018 to 2025
        self.results = []
        
    def read_csv_file(self, filepath: str) -> pd.DataFrame:
        """
        Read CSV file, handling both zipped and regular files.
        
        Args:
            filepath: Path to the CSV file (can be .csv or .csv.zip)
            
        Returns:
            DataFrame containing the data
        """
        try:
            if filepath.endswith('.zip'):
                # Extract zip file to temporary location
                with zipfile.ZipFile(filepath, 'r') as zip_ref:
                    # Get the name of the CSV file inside the zip
                    csv_filename = zip_ref.namelist()[0]
                    
                    # Extract to temporary directory
                    with tempfile.TemporaryDirectory() as temp_dir:
                        zip_ref.extract(csv_filename, temp_dir)
                        temp_csv_path = os.path.join(temp_dir, csv_filename)
                        
                        # Read the CSV file
                        df = pd.read_csv(
                            temp_csv_path,
                            sep=';',
                            names=['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume'],
                            skiprows=1
                        )
            else:
                # Read regular CSV file
                df = pd.read_csv(
                    filepath,
                    sep=';',
                    names=['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume'],
                    skiprows=1
                )
            
            # Convert data types
            df['Open'] = pd.to_numeric(df['Open'], errors='coerce')
            df['High'] = pd.to_numeric(df['High'], errors='coerce')
            df['Low'] = pd.to_numeric(df['Low'], errors='coerce')
            df['Close'] = pd.to_numeric(df['Close'], errors='coerce')
            df['Volume'] = pd.to_numeric(df['Volume'], errors='coerce')
            
            # Parse datetime
            df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%d/%m/%Y %H:%M:%S')
            
            # Sort by datetime
            df = df.sort_values('DateTime').reset_index(drop=True)
            
            return df
            
        except Exception as e:
            print(f"Error reading {filepath}: {e}")
            return pd.DataFrame()
    
    def is_bullish(self, open_price: float, close_price: float) -> bool:
        """Check if candle is bullish."""
        return close_price > open_price
    
    def is_bearish(self, open_price: float, close_price: float) -> bool:
        """Check if candle is bearish."""
        return close_price < open_price
    
    def check_bullish_condition(self, current_close: float, prev_5_highs: List[float]) -> bool:
        """
        Check if bullish candle closes above the wicks (highs) of previous 5 candles.
        
        Args:
            current_close: Close price of current candle
            prev_5_highs: List of high prices of previous 5 candles
            
        Returns:
            True if condition is met, False otherwise
        """
        if len(prev_5_highs) < 5:
            return False
        
        max_high = max(prev_5_highs)
        return current_close > max_high
    
    def check_bearish_condition(self, current_close: float, prev_5_lows: List[float]) -> bool:
        """
        Check if bearish candle closes below the wicks (lows) of previous 5 candles.
        
        Args:
            current_close: Close price of current candle
            prev_5_lows: List of low prices of previous 5 candles
            
        Returns:
            True if condition is met, False otherwise
        """
        if len(prev_5_lows) < 5:
            return False
        
        min_low = min(prev_5_lows)
        return current_close < min_low
    
    def analyze_timeframe(self, timeframe: str, year: int) -> List[Dict]:
        """
        Analyze a specific timeframe for a given year.
        
        Args:
            timeframe: Timeframe to analyze (1m, 5m, or 15m)
            year: Year to analyze
            
        Returns:
            List of dictionaries containing trade information
        """
        trades = []
        
        # Construct filename
        filename = f"{year} {timeframe}.csv"
        filepath = os.path.join(self.base_path, filename)
        
        # Check if zipped version exists
        if not os.path.exists(filepath):
            filepath = os.path.join(self.base_path, f"{filename}.zip")
        
        if not os.path.exists(filepath):
            print(f"File not found: {filename} or {filename}.zip")
            return trades
        
        print(f"Analyzing {year} {timeframe}...")
        
        # Read the data
        df = self.read_csv_file(filepath)
        
        if df.empty:
            return trades
        
        # Filter for 8:30 AM candles
        df_830 = df[df['Time'] == '08:30:00'].copy()
        
        print(f"  Found {len(df_830)} candles at 8:30 AM")
        
        # For each 8:30 AM candle, check the conditions
        for idx, row in df_830.iterrows():
            current_datetime = row['DateTime']
            current_open = row['Open']
            current_close = row['Close']
            current_high = row['High']
            current_low = row['Low']
            
            # Get index in original dataframe
            original_idx = df[df['DateTime'] == current_datetime].index[0]
            
            # Get previous 5 candles
            if original_idx >= 5:
                prev_5 = df.iloc[original_idx-5:original_idx]
                prev_5_highs = prev_5['High'].tolist()
                prev_5_lows = prev_5['Low'].tolist()
                
                # Determine if candle is bullish or bearish
                is_bull = self.is_bullish(current_open, current_close)
                is_bear = self.is_bearish(current_open, current_close)
                
                condition_met = False
                candle_type = None
                reference_level = None
                
                if is_bull:
                    # Check if bullish condition is met
                    if self.check_bullish_condition(current_close, prev_5_highs):
                        condition_met = True
                        candle_type = 'BULLISH'
                        reference_level = max(prev_5_highs)
                        
                elif is_bear:
                    # Check if bearish condition is met
                    if self.check_bearish_condition(current_close, prev_5_lows):
                        condition_met = True
                        candle_type = 'BEARISH'
                        reference_level = min(prev_5_lows)
                
                if condition_met:
                    trade = {
                        'Date': row['Date'],
                        'Time': row['Time'],
                        'Timeframe': timeframe,
                        'Candle_Type': candle_type,
                        'Open': current_open,
                        'High': current_high,
                        'Low': current_low,
                        'Close': current_close,
                        'Reference_Level': reference_level,
                        'Condition': f"Close ({current_close:.2f}) {'>' if is_bull else '<'} Reference ({reference_level:.2f})"
                    }
                    trades.append(trade)
        
        print(f"  Found {len(trades)} trades meeting conditions")
        return trades
    
    def run_backtest(self) -> pd.DataFrame:
        """
        Run the complete backtest analysis across all timeframes and years.
        
        Returns:
            DataFrame containing all identified trades
        """
        print("=" * 80)
        print("Starting Backtest Analysis")
        print("=" * 80)
        print(f"Analyzing timeframes: {', '.join(self.timeframes)}")
        print(f"Analyzing years: {', '.join(map(str, self.years))}")
        print("=" * 80)
        print()
        
        all_trades = []
        
        for timeframe in self.timeframes:
            print(f"\n{'='*80}")
            print(f"Processing {timeframe} data")
            print(f"{'='*80}")
            
            for year in self.years:
                trades = self.analyze_timeframe(timeframe, year)
                all_trades.extend(trades)
            
            print()
        
        # Convert to DataFrame
        if all_trades:
            df_results = pd.DataFrame(all_trades)
            self.results = df_results
            return df_results
        else:
            print("No trades found meeting the conditions.")
            return pd.DataFrame()
    
    def generate_summary(self, df_results: pd.DataFrame) -> Dict:
        """
        Generate summary statistics for the backtest results.
        
        Args:
            df_results: DataFrame containing backtest results
            
        Returns:
            Dictionary containing summary statistics
        """
        if df_results.empty:
            return {
                'total_trades': 0,
                'by_timeframe': {},
                'by_candle_type': {}
            }
        
        summary = {
            'total_trades': len(df_results),
            'by_timeframe': df_results.groupby('Timeframe').size().to_dict(),
            'by_candle_type': df_results.groupby('Candle_Type').size().to_dict(),
            'by_timeframe_and_type': df_results.groupby(['Timeframe', 'Candle_Type']).size().to_dict()
        }
        
        return summary
    
    def save_results(self, df_results: pd.DataFrame, output_dir: str = None):
        """
        Save results to CSV files.
        
        Args:
            df_results: DataFrame containing backtest results
            output_dir: Directory to save results (defaults to base_path)
        """
        if output_dir is None:
            output_dir = self.base_path
        
        if df_results.empty:
            print("No results to save.")
            return
        
        # Save all trades
        output_file = os.path.join(output_dir, 'backtest_results.csv')
        df_results.to_csv(output_file, index=False)
        print(f"\nAll trades saved to: {output_file}")
        
        # Save trades by timeframe
        for timeframe in self.timeframes:
            df_tf = df_results[df_results['Timeframe'] == timeframe]
            if not df_tf.empty:
                tf_output_file = os.path.join(output_dir, f'backtest_results_{timeframe}.csv')
                df_tf.to_csv(tf_output_file, index=False)
                print(f"Trades for {timeframe} saved to: {tf_output_file}")
    
    def print_summary_report(self, summary: Dict):
        """
        Print a formatted summary report.
        
        Args:
            summary: Dictionary containing summary statistics
        """
        print("\n" + "=" * 80)
        print("BACKTEST SUMMARY REPORT")
        print("=" * 80)
        print(f"\nTotal Trades Found: {summary['total_trades']}")
        
        print("\n" + "-" * 80)
        print("Trades by Timeframe:")
        print("-" * 80)
        for timeframe, count in sorted(summary['by_timeframe'].items()):
            print(f"  {timeframe:>5}: {count:>6} trades")
        
        print("\n" + "-" * 80)
        print("Trades by Candle Type:")
        print("-" * 80)
        for candle_type, count in sorted(summary['by_candle_type'].items()):
            print(f"  {candle_type:>8}: {count:>6} trades")
        
        print("\n" + "-" * 80)
        print("Trades by Timeframe and Candle Type:")
        print("-" * 80)
        for (timeframe, candle_type), count in sorted(summary['by_timeframe_and_type'].items()):
            print(f"  {timeframe:>5} - {candle_type:>8}: {count:>6} trades")
        
        print("\n" + "=" * 80)


def main():
    """Main execution function."""
    # Set the base path to the repository
    base_path = '/home/runner/work/Backtest-Trading/Backtest-Trading'
    
    # Initialize the backtest strategy
    strategy = BacktestStrategy(base_path)
    
    # Run the backtest
    results_df = strategy.run_backtest()
    
    # Generate and print summary
    summary = strategy.generate_summary(results_df)
    strategy.print_summary_report(summary)
    
    # Save results
    strategy.save_results(results_df)
    
    print("\nBacktest analysis complete!")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Backtesting Strategy: 8:30 AM Candle Analysis
Analyzes 1m, 5m, and 15m timeframes from 2018-2025
"""

import pandas as pd
import numpy as np
from datetime import datetime, time
import zipfile
import os
from pathlib import Path

# Configuration
BASE_DIR = Path(__file__).parent.absolute()
YEARS = range(2018, 2026)  # 2018 to 2025
TIMEFRAMES = ['1m', '5m', '15m']
TARGET_TIME = time(8, 30)  # 8:30 AM


def load_csv_data(filepath, is_zipped=False):
    """Load CSV data from file or zip archive."""
    try:
        if is_zipped:
            zip_path = filepath
            csv_filename = filepath.stem  # Get filename without .zip extension
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                # Read the CSV file from the zip
                with zip_ref.open(f"{csv_filename}") as csv_file:
                    df = pd.read_csv(csv_file, sep=';', header=0)
        else:
            df = pd.read_csv(filepath, sep=';', header=0)
        
        # Rename columns to standard names
        df.columns = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
        
        # Parse datetime
        df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%d/%m/%Y %H:%M:%S')
        df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')
        df['Time'] = pd.to_datetime(df['Time'], format='%H:%M:%S').dt.time
        
        # Convert price columns to float
        for col in ['Open', 'High', 'Low', 'Close']:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        df['Volume'] = pd.to_numeric(df['Volume'], errors='coerce')
        
        # Sort by datetime
        df = df.sort_values('DateTime').reset_index(drop=True)
        
        return df
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return None


def is_bullish_candle(row):
    """Check if candle is bullish (close > open)."""
    return row['Close'] > row['Open']


def is_bearish_candle(row):
    """Check if candle is bearish (close < open)."""
    return row['Close'] < row['Open']


def check_bullish_condition(df, idx, lookback=5):
    """
    Check if bullish condition is met:
    Close of current candle > max(highs of previous 5 candles)
    """
    if idx < lookback:
        return False, None
    
    current_close = df.loc[idx, 'Close']
    previous_highs = df.loc[idx-lookback:idx-1, 'High'].values
    max_previous_high = np.max(previous_highs)
    
    return current_close > max_previous_high, max_previous_high


def check_bearish_condition(df, idx, lookback=5):
    """
    Check if bearish condition is met:
    Close of current candle < min(lows of previous 5 candles)
    """
    if idx < lookback:
        return False, None
    
    current_close = df.loc[idx, 'Close']
    previous_lows = df.loc[idx-lookback:idx-1, 'Low'].values
    min_previous_low = np.min(previous_lows)
    
    return current_close < min_previous_low, min_previous_low


def find_trades_in_timeframe(timeframe, years):
    """Find all valid trades for a specific timeframe across multiple years."""
    print(f"\n{'='*60}")
    print(f"Analyzing {timeframe} timeframe...")
    print(f"{'='*60}")
    
    all_trades = []
    
    for year in years:
        # Determine file path
        if timeframe == '1m':
            if year == 2025:
                # 2025 1m data is not zipped
                filepath = BASE_DIR / f"{year} {timeframe}.csv"
                is_zipped = False
            else:
                filepath = BASE_DIR / f"{year} {timeframe}.csv.zip"
                is_zipped = True
        else:
            filepath = BASE_DIR / f"{year} {timeframe}.csv"
            is_zipped = False
        
        if not filepath.exists():
            print(f"  Warning: File not found - {filepath}")
            continue
        
        print(f"  Loading {year} data...")
        df = load_csv_data(filepath, is_zipped)
        
        if df is None or len(df) == 0:
            print(f"  Warning: No data loaded for {year}")
            continue
        
        print(f"    Loaded {len(df)} candles")
        
        # Find all 8:30 AM candles
        target_candles = df[df['Time'] == TARGET_TIME].copy()
        print(f"    Found {len(target_candles)} 8:30 AM candles")
        
        # Analyze each 8:30 AM candle
        trades_found = 0
        for _, target_row in target_candles.iterrows():
            target_idx = target_row.name
            target_date = target_row['Date']
            
            is_bullish = is_bullish_candle(target_row)
            is_bearish = is_bearish_candle(target_row)
            
            trade_entry = None
            
            if is_bullish:
                # Check bullish condition
                condition_met, reference_level = check_bullish_condition(df, target_idx)
                if condition_met:
                    trade_entry = {
                        'Date': target_date.strftime('%Y-%m-%d'),
                        'Time': '08:30:00',
                        'Timeframe': timeframe,
                        'Direction': 'LONG',
                        'Open': target_row['Open'],
                        'High': target_row['High'],
                        'Low': target_row['Low'],
                        'Close': target_row['Close'],
                        'Volume': target_row['Volume'],
                        'Reference_Level': reference_level,
                        'Condition': f"Close ({target_row['Close']:.2f}) > Max Previous 5 Highs ({reference_level:.2f})"
                    }
            
            elif is_bearish:
                # Check bearish condition
                condition_met, reference_level = check_bearish_condition(df, target_idx)
                if condition_met:
                    trade_entry = {
                        'Date': target_date.strftime('%Y-%m-%d'),
                        'Time': '08:30:00',
                        'Timeframe': timeframe,
                        'Direction': 'SHORT',
                        'Open': target_row['Open'],
                        'High': target_row['High'],
                        'Low': target_row['Low'],
                        'Close': target_row['Close'],
                        'Volume': target_row['Volume'],
                        'Reference_Level': reference_level,
                        'Condition': f"Close ({target_row['Close']:.2f}) < Min Previous 5 Lows ({reference_level:.2f})"
                    }
            
            if trade_entry:
                all_trades.append(trade_entry)
                trades_found += 1
        
        print(f"    Found {trades_found} valid trades in {year}")
    
    return all_trades


def main():
    """Main execution function."""
    print("="*60)
    print("BACKTESTING STRATEGY: 8:30 AM CANDLE ANALYSIS")
    print("="*60)
    print(f"Period: 2018-2025")
    print(f"Timeframes: {', '.join(TIMEFRAMES)}")
    print(f"Target Time: 08:30 AM")
    print("="*60)
    
    # Store all results
    all_results = {}
    
    # Process each timeframe
    for timeframe in TIMEFRAMES:
        trades = find_trades_in_timeframe(timeframe, YEARS)
        all_results[timeframe] = trades
        
        # Save to CSV
        if trades:
            df_trades = pd.DataFrame(trades)
            output_file = BASE_DIR / f"trades_{timeframe}.csv"
            df_trades.to_csv(output_file, index=False)
            print(f"\n  ✓ Saved {len(trades)} trades to {output_file}")
        else:
            print(f"\n  ⚠ No trades found for {timeframe}")
    
    # Create summary report
    print("\n" + "="*60)
    print("SUMMARY REPORT")
    print("="*60)
    
    summary_data = []
    for timeframe in TIMEFRAMES:
        trades = all_results[timeframe]
        if trades:
            df = pd.DataFrame(trades)
            long_count = len(df[df['Direction'] == 'LONG'])
            short_count = len(df[df['Direction'] == 'SHORT'])
            
            summary_data.append({
                'Timeframe': timeframe,
                'Total_Trades': len(trades),
                'Long_Trades': long_count,
                'Short_Trades': short_count
            })
            
            print(f"\n{timeframe} Timeframe:")
            print(f"  Total Trades: {len(trades)}")
            print(f"  Long Trades:  {long_count}")
            print(f"  Short Trades: {short_count}")
        else:
            summary_data.append({
                'Timeframe': timeframe,
                'Total_Trades': 0,
                'Long_Trades': 0,
                'Short_Trades': 0
            })
            print(f"\n{timeframe} Timeframe:")
            print(f"  No trades found")
    
    # Save summary
    if summary_data:
        df_summary = pd.DataFrame(summary_data)
        summary_file = BASE_DIR / "trades_summary.csv"
        df_summary.to_csv(summary_file, index=False)
        print(f"\n✓ Summary saved to {summary_file}")
    
    # Create detailed report with all trades combined
    all_trades_combined = []
    for timeframe in TIMEFRAMES:
        all_trades_combined.extend(all_results[timeframe])
    
    if all_trades_combined:
        df_all = pd.DataFrame(all_trades_combined)
        df_all = df_all.sort_values(['Date', 'Timeframe'])
        all_trades_file = BASE_DIR / "all_trades.csv"
        df_all.to_csv(all_trades_file, index=False)
        print(f"✓ All trades saved to {all_trades_file}")
        
        # Show first few trades as sample
        print("\n" + "="*60)
        print("SAMPLE TRADES (first 10):")
        print("="*60)
        print(df_all.head(10).to_string(index=False))
    
    print("\n" + "="*60)
    print("BACKTESTING COMPLETE!")
    print("="*60)


if __name__ == "__main__":
    main()

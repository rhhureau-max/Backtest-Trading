#!/usr/bin/env python3
"""
Trading Setup Analysis Script

This script analyzes a specific trading setup:
- Looks at the 8:30 AM (Europe time / 06:30 UTC / 08:30 CET) candle
- If bearish: checks if next candle is bullish AND closes above max high of previous 5 candles
- If bullish: checks if next candle is bearish AND closes below min low of previous 5 candles

Analyzes 1-minute, 5-minute, and 15-minute data from 2018 to 2025.
"""

import pandas as pd
import numpy as np
from datetime import datetime, time
import os
import zipfile
import glob
from collections import defaultdict
import json

class TradingSetupAnalyzer:
    def __init__(self, base_path):
        self.base_path = base_path
        self.results = defaultdict(lambda: defaultdict(list))
        self.summary = defaultdict(lambda: defaultdict(int))
        
    def unzip_1m_files(self):
        """Unzip all 1-minute data files if they haven't been already"""
        print("Checking and unzipping 1-minute data files...")
        zip_files = glob.glob(os.path.join(self.base_path, "*1m.csv.zip"))
        
        for zip_file in zip_files:
            csv_filename = zip_file.replace('.zip', '')
            if not os.path.exists(csv_filename):
                print(f"Unzipping {os.path.basename(zip_file)}...")
                try:
                    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                        zip_ref.extractall(self.base_path)
                    print(f"  ✓ Extracted {os.path.basename(csv_filename)}")
                except Exception as e:
                    print(f"  ✗ Error extracting {zip_file}: {e}")
            else:
                print(f"  - {os.path.basename(csv_filename)} already exists")
        print()
    
    def load_data(self, year, timeframe):
        """Load CSV data for a specific year and timeframe"""
        filename = os.path.join(self.base_path, f"{year} {timeframe}.csv")
        
        if not os.path.exists(filename):
            print(f"Warning: File not found: {filename}")
            return None
        
        try:
            # Read CSV with semicolon delimiter
            df = pd.read_csv(filename, sep=';', header=0)
            
            # Rename columns for easier access
            df.columns = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
            
            # Parse datetime
            df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], 
                                           format='%d/%m/%Y %H:%M:%S')
            
            # Convert price columns to float
            for col in ['Open', 'High', 'Low', 'Close']:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            
            df = df.sort_values('DateTime').reset_index(drop=True)
            
            print(f"Loaded {len(df)} rows from {year} {timeframe}")
            return df
            
        except Exception as e:
            print(f"Error loading {filename}: {e}")
            return None
    
    def identify_830_candle_index(self, df, timeframe):
        """
        Identify the index of the 8:30 AM (Europe time) candle
        8:30 AM Europe time = 06:30 UTC (standard time) or 07:30 UTC (daylight saving)
        For simplicity, we'll look for 08:30 in the time column
        """
        # Extract time component
        df['TimeOnly'] = df['DateTime'].dt.time
        
        # Look for 8:30 AM candles
        target_time = time(8, 30, 0)
        
        if timeframe == '1m':
            # For 1-minute data, exact match at 08:30:00
            mask = df['TimeOnly'] == target_time
        elif timeframe == '5m':
            # For 5-minute data, candle starting at 08:30:00
            mask = df['TimeOnly'] == target_time
        elif timeframe == '15m':
            # For 15-minute data, candle starting at 08:30:00
            mask = df['TimeOnly'] == target_time
        
        return df[mask].index.tolist()
    
    def check_setup(self, df, idx):
        """
        Check if the trading setup conditions are met at a given index
        
        Returns:
            dict with setup information or None if no setup found
        """
        # Need at least 5 candles before and 1 candle after
        if idx < 5 or idx >= len(df) - 1:
            return None
        
        # Get the 8:30 candle
        candle_830 = df.iloc[idx]
        
        # Get the next candle
        next_candle = df.iloc[idx + 1]
        
        # Get previous 5 candles (indices idx-5 to idx-1)
        prev_5_candles = df.iloc[idx-5:idx]
        
        # Calculate max high and min low of previous 5 candles
        max_high_prev5 = prev_5_candles['High'].max()
        min_low_prev5 = prev_5_candles['Low'].min()
        
        # Determine if 8:30 candle is bearish or bullish
        is_830_bearish = candle_830['Close'] < candle_830['Open']
        is_830_bullish = candle_830['Close'] > candle_830['Open']
        
        # Determine if next candle is bearish or bullish
        is_next_bearish = next_candle['Close'] < next_candle['Open']
        is_next_bullish = next_candle['Close'] > next_candle['Open']
        
        setup_found = False
        setup_type = None
        
        # Check bearish 8:30 setup
        if is_830_bearish and is_next_bullish:
            if next_candle['Close'] > max_high_prev5:
                setup_found = True
                setup_type = 'bearish_830_to_bullish_breakout'
        
        # Check bullish 8:30 setup
        if is_830_bullish and is_next_bearish:
            if next_candle['Close'] < min_low_prev5:
                setup_found = True
                setup_type = 'bullish_830_to_bearish_breakdown'
        
        if setup_found:
            return {
                'date': candle_830['DateTime'].date(),
                'time': candle_830['DateTime'].time(),
                'setup_type': setup_type,
                'candle_830_open': candle_830['Open'],
                'candle_830_high': candle_830['High'],
                'candle_830_low': candle_830['Low'],
                'candle_830_close': candle_830['Close'],
                'next_candle_open': next_candle['Open'],
                'next_candle_high': next_candle['High'],
                'next_candle_low': next_candle['Low'],
                'next_candle_close': next_candle['Close'],
                'prev5_max_high': max_high_prev5,
                'prev5_min_low': min_low_prev5,
            }
        
        return None
    
    def analyze_timeframe(self, year, timeframe):
        """Analyze a specific year and timeframe combination"""
        print(f"\nAnalyzing {year} {timeframe}...")
        
        df = self.load_data(year, timeframe)
        if df is None:
            return
        
        # Find all 8:30 candles
        candle_830_indices = self.identify_830_candle_index(df, timeframe)
        print(f"Found {len(candle_830_indices)} candles at 8:30 AM")
        
        # Check each 8:30 candle for the setup
        setups_found = 0
        for idx in candle_830_indices:
            setup = self.check_setup(df, idx)
            if setup:
                self.results[timeframe][year].append(setup)
                setups_found += 1
        
        self.summary[timeframe][year] = setups_found
        print(f"✓ Found {setups_found} setups in {year} {timeframe}")
    
    def analyze_all(self):
        """Analyze all years and timeframes"""
        print("="*80)
        print("TRADING SETUP ANALYSIS")
        print("="*80)
        
        # Unzip 1-minute files first
        self.unzip_1m_files()
        
        years = [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]
        timeframes = ['1m', '5m', '15m']
        
        for timeframe in timeframes:
            print(f"\n{'='*80}")
            print(f"TIMEFRAME: {timeframe}")
            print(f"{'='*80}")
            
            for year in years:
                self.analyze_timeframe(year, timeframe)
    
    def generate_report(self):
        """Generate comprehensive report"""
        print("\n" + "="*80)
        print("COMPREHENSIVE REPORT")
        print("="*80)
        
        report_lines = []
        report_lines.append("="*80)
        report_lines.append("TRADING SETUP ANALYSIS REPORT")
        report_lines.append("="*80)
        report_lines.append("")
        report_lines.append("Analysis Date: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        report_lines.append("")
        report_lines.append("SETUP DEFINITION:")
        report_lines.append("-" * 80)
        report_lines.append("Looking at the 8:30 AM (Europe time) candle:")
        report_lines.append("1. If 8:30 candle is BEARISH (close < open):")
        report_lines.append("   - Next candle must be BULLISH (close > open)")
        report_lines.append("   - AND next candle close must be ABOVE max high of previous 5 candles")
        report_lines.append("")
        report_lines.append("2. If 8:30 candle is BULLISH (close > open):")
        report_lines.append("   - Next candle must be BEARISH (close < open)")
        report_lines.append("   - AND next candle close must be BELOW min low of previous 5 candles")
        report_lines.append("")
        report_lines.append("="*80)
        report_lines.append("")
        
        # Summary by timeframe
        for timeframe in ['1m', '5m', '15m']:
            report_lines.append(f"\n{timeframe.upper()} TIMEFRAME RESULTS:")
            report_lines.append("-" * 80)
            
            total_setups = 0
            for year in sorted(self.summary[timeframe].keys()):
                count = self.summary[timeframe][year]
                total_setups += count
                report_lines.append(f"  {year}: {count:4d} setups")
            
            report_lines.append(f"  {'Total':<6}: {total_setups:4d} setups")
            report_lines.append("")
        
        # Overall summary
        report_lines.append("\n" + "="*80)
        report_lines.append("OVERALL SUMMARY")
        report_lines.append("="*80)
        
        grand_total = 0
        for timeframe in ['1m', '5m', '15m']:
            timeframe_total = sum(self.summary[timeframe].values())
            grand_total += timeframe_total
            report_lines.append(f"{timeframe.upper():>5}: {timeframe_total:5d} setups")
        
        report_lines.append("-" * 80)
        report_lines.append(f"{'TOTAL':>5}: {grand_total:5d} setups")
        report_lines.append("")
        
        # Detailed breakdown by setup type
        report_lines.append("\n" + "="*80)
        report_lines.append("SETUP TYPE BREAKDOWN")
        report_lines.append("="*80)
        
        for timeframe in ['1m', '5m', '15m']:
            report_lines.append(f"\n{timeframe.upper()} Timeframe:")
            report_lines.append("-" * 80)
            
            bearish_count = 0
            bullish_count = 0
            
            for year in self.results[timeframe]:
                for setup in self.results[timeframe][year]:
                    if setup['setup_type'] == 'bearish_830_to_bullish_breakout':
                        bearish_count += 1
                    else:
                        bullish_count += 1
            
            report_lines.append(f"  Bearish 8:30 → Bullish Breakout: {bearish_count}")
            report_lines.append(f"  Bullish 8:30 → Bearish Breakdown: {bullish_count}")
            report_lines.append("")
        
        # Print and save report
        report_text = "\n".join(report_lines)
        print(report_text)
        
        # Save summary report
        with open(os.path.join(self.base_path, 'trading_setup_report.txt'), 'w') as f:
            f.write(report_text)
        
        print("\n✓ Summary report saved to: trading_setup_report.txt")
        
        # Save detailed results to JSON
        detailed_results = {
            'summary': dict(self.summary),
            'detailed_setups': {}
        }
        
        for timeframe in self.results:
            detailed_results['detailed_setups'][timeframe] = {}
            for year in self.results[timeframe]:
                # Convert date/time objects to strings for JSON serialization
                setups_serializable = []
                for setup in self.results[timeframe][year]:
                    setup_copy = setup.copy()
                    setup_copy['date'] = str(setup['date'])
                    setup_copy['time'] = str(setup['time'])
                    setups_serializable.append(setup_copy)
                detailed_results['detailed_setups'][timeframe][year] = setups_serializable
        
        with open(os.path.join(self.base_path, 'trading_setup_detailed_results.json'), 'w') as f:
            json.dump(detailed_results, f, indent=2)
        
        print("✓ Detailed results saved to: trading_setup_detailed_results.json")
        
        # Save detailed CSV for each timeframe
        for timeframe in ['1m', '5m', '15m']:
            all_setups = []
            for year in self.results[timeframe]:
                for setup in self.results[timeframe][year]:
                    setup_copy = setup.copy()
                    setup_copy['year'] = year
                    all_setups.append(setup_copy)
            
            if all_setups:
                df_setups = pd.DataFrame(all_setups)
                csv_filename = f'trading_setup_{timeframe}_detailed.csv'
                df_setups.to_csv(os.path.join(self.base_path, csv_filename), index=False)
                print(f"✓ Detailed {timeframe} setups saved to: {csv_filename}")
        
        print("\n" + "="*80)
        print("ANALYSIS COMPLETE!")
        print("="*80)

def main():
    base_path = '/home/runner/work/Backtest-Trading/Backtest-Trading'
    
    analyzer = TradingSetupAnalyzer(base_path)
    analyzer.analyze_all()
    analyzer.generate_report()

if __name__ == "__main__":
    main()

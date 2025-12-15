#!/usr/bin/env python3
"""
Backtesting Strategy Script
Analyzes historical trades from 2018 to today based on 08:30:00 candle conditions.

For bullish candles (close > open): close must be above the highest high of the previous 5 candles
For bearish candles (close < open): close must be below the lowest low of the previous 5 candles

Extended with Risk/Reward Analysis:
- 4 Stop Loss types: 100%, 75%, 50%, 25% body retracement
- 9 Risk/Reward ratios: 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0
"""

import pandas as pd
import os
import zipfile
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional
import glob
import numpy as np


class BacktestStrategy:
    def __init__(self, base_path: str):
        self.base_path = base_path
        self.timeframes = ['1m', '5m', '15m']
        self.years = list(range(2018, 2026))  # 2018 to 2025
        self.results = []
        
        # Risk/Reward analysis parameters
        self.sl_types = {
            'SL100': 1.00,  # 100% retracement (back to open)
            'SL75': 0.75,   # 75% retracement
            'SL50': 0.50,   # 50% retracement (middle of body)
            'SL25': 0.25    # 25% retracement
        }
        self.rr_ratios = [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]
        self.rr_results = []
        self.data_cache = {}  # Cache loaded data for RR analysis
        
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
    
    def calculate_sl_tp_levels(self, trade: Dict, sl_type: str, rr_ratio: float) -> Tuple[float, float]:
        """
        Calculate Stop Loss and Take Profit levels for a trade.
        
        Args:
            trade: Trade dictionary with OHLC data
            sl_type: Type of SL ('SL100', 'SL75', 'SL50', 'SL25')
            rr_ratio: Risk/Reward ratio
            
        Returns:
            Tuple of (stop_loss, take_profit) levels
        """
        entry = trade['Close']
        open_price = trade['Open']
        trade_type = trade['Type']
        
        # Calculate body size
        if trade_type == 'BULLISH':
            body = entry - open_price
        else:  # BEARISH
            body = open_price - entry
        
        # Get retracement percentage for this SL type
        retracement = self.sl_types[sl_type]
        
        # Calculate SL and TP
        if trade_type == 'BULLISH':
            # For bullish: SL below entry, TP above entry
            sl = entry - (body * retracement)
            risk = entry - sl
            tp = entry + (risk * rr_ratio)
        else:  # BEARISH
            # For bearish: SL above entry, TP below entry
            sl = entry + (body * retracement)
            risk = sl - entry
            tp = entry - (risk * rr_ratio)
        
        return sl, tp
    
    def simulate_trade_outcome(self, trade: Dict, sl: float, tp: float, df: pd.DataFrame) -> Dict:
        """
        Simulate a trade by checking subsequent candles to see if SL or TP is hit.
        
        Args:
            trade: Trade dictionary
            sl: Stop Loss level
            tp: Take Profit level
            df: DataFrame with all data for this timeframe/year
            
        Returns:
            Dictionary with outcome information
        """
        trade_type = trade['Type']
        trade_datetime = trade['Datetime']
        
        # Find the position of the trade in the dataframe
        trade_pos = df[df['Datetime'] == trade_datetime].index
        if len(trade_pos) == 0:
            return {'outcome': 'NOT_FOUND', 'candles_to_hit': None, 'exit_price': None}
        
        trade_idx = trade_pos[0]
        df_pos = df.index.get_loc(trade_idx)
        
        # Get remaining candles for the same day
        trade_date = trade['Date']
        same_day_df = df[(df['Date'] == trade_date) & (df.index > trade_idx)]
        
        if len(same_day_df) == 0:
            return {'outcome': 'INCONCLUSIVE', 'candles_to_hit': None, 'exit_price': None}
        
        # Check each subsequent candle
        for idx, (candle_idx, candle) in enumerate(same_day_df.iterrows(), 1):
            if trade_type == 'BULLISH':
                # Check if SL hit (low touches or goes below SL)
                if candle['Low'] <= sl:
                    return {'outcome': 'LOSS', 'candles_to_hit': idx, 'exit_price': sl}
                # Check if TP hit (high touches or goes above TP)
                if candle['High'] >= tp:
                    return {'outcome': 'WIN', 'candles_to_hit': idx, 'exit_price': tp}
            else:  # BEARISH
                # Check if SL hit (high touches or goes above SL)
                if candle['High'] >= sl:
                    return {'outcome': 'LOSS', 'candles_to_hit': idx, 'exit_price': sl}
                # Check if TP hit (low touches or goes below TP)
                if candle['Low'] <= tp:
                    return {'outcome': 'WIN', 'candles_to_hit': idx, 'exit_price': tp}
        
        # If we reach here, neither SL nor TP was hit by end of day
        last_close = same_day_df.iloc[-1]['Close']
        return {'outcome': 'INCONCLUSIVE', 'candles_to_hit': len(same_day_df), 'exit_price': last_close}
    
    def analyze_rr_for_trade(self, trade: Dict, year: int) -> List[Dict]:
        """
        Analyze all Risk/Reward scenarios for a single trade.
        
        Args:
            trade: Trade dictionary
            year: Year of the trade
            
        Returns:
            List of dictionaries with RR analysis results
        """
        timeframe = trade['Timeframe']
        
        # Get the full dataframe for this year/timeframe
        cache_key = f"{year}_{timeframe}"
        if cache_key in self.data_cache:
            df = self.data_cache[cache_key]
        else:
            df = self.load_data(year, timeframe)
            if df is not None:
                self.data_cache[cache_key] = df
            else:
                return []
        
        if df is None:
            return []
        
        rr_results = []
        
        # Test all combinations of SL types and RR ratios
        for sl_type in self.sl_types.keys():
            for rr_ratio in self.rr_ratios:
                # Calculate SL and TP
                sl, tp = self.calculate_sl_tp_levels(trade, sl_type, rr_ratio)
                
                # Simulate the trade
                outcome_info = self.simulate_trade_outcome(trade, sl, tp, df)
                
                # Calculate P&L
                entry = trade['Close']
                risk = abs(entry - sl)
                reward = abs(tp - entry)
                
                if outcome_info['outcome'] == 'WIN':
                    pnl = reward
                elif outcome_info['outcome'] == 'LOSS':
                    pnl = -risk
                else:  # INCONCLUSIVE
                    if outcome_info['exit_price'] is not None:
                        pnl = outcome_info['exit_price'] - entry if trade['Type'] == 'BULLISH' else entry - outcome_info['exit_price']
                    else:
                        pnl = 0
                
                # Store result
                result = {
                    'Date': trade['Date'],
                    'Time': trade['Time'],
                    'Timeframe': timeframe,
                    'Type': trade['Type'],
                    'Entry': entry,
                    'SL_Type': sl_type,
                    'RR_Ratio': rr_ratio,
                    'Stop_Loss': sl,
                    'Take_Profit': tp,
                    'Risk': risk,
                    'Reward': reward,
                    'Outcome': outcome_info['outcome'],
                    'Candles_To_Hit': outcome_info['candles_to_hit'],
                    'Exit_Price': outcome_info['exit_price'],
                    'PnL': pnl
                }
                rr_results.append(result)
        
        return rr_results
    
    def run_rr_analysis(self):
        """
        Run Risk/Reward analysis on all identified trades.
        """
        print("\n" + "=" * 80)
        print("RISK/REWARD ANALYSIS")
        print("=" * 80)
        print(f"SL Types: {', '.join(self.sl_types.keys())}")
        print(f"RR Ratios: {', '.join(map(str, self.rr_ratios))}")
        print(f"Total Scenarios per Trade: {len(self.sl_types) * len(self.rr_ratios)}")
        print(f"Total Trades to Analyze: {len(self.results)}")
        print("=" * 80)
        
        if not self.results:
            print("No trades found. Run backtest first.")
            return
        
        # Group trades by year for efficient data loading
        trades_by_year = {}
        for trade in self.results:
            year = int(trade['Date'].split('/')[-1])
            if year not in trades_by_year:
                trades_by_year[year] = []
            trades_by_year[year].append(trade)
        
        total_trades = len(self.results)
        processed = 0
        
        for year in sorted(trades_by_year.keys()):
            year_trades = trades_by_year[year]
            print(f"\nProcessing {year}: {len(year_trades)} trades...")
            
            for i, trade in enumerate(year_trades, 1):
                rr_results = self.analyze_rr_for_trade(trade, year)
                self.rr_results.extend(rr_results)
                processed += 1
                
                if processed % 100 == 0 or processed == total_trades:
                    print(f"  Progress: {processed}/{total_trades} trades ({100*processed/total_trades:.1f}%)")
        
        print("\n" + "=" * 80)
        print(f"RR ANALYSIS COMPLETED")
        print(f"Total Scenarios Analyzed: {len(self.rr_results)}")
        print("=" * 80)
    
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
    
    def save_rr_results(self):
        """Save Risk/Reward analysis results to CSV files and generate comprehensive report."""
        if not self.rr_results:
            print("\nNo RR analysis results to save.")
            return
        
        rr_df = pd.DataFrame(self.rr_results)
        
        # Save detailed results
        detailed_path = os.path.join(self.base_path, 'backtest_rr_analysis_detailed.csv')
        rr_df.to_csv(detailed_path, index=False, sep=';')
        print(f"\nDetailed RR results saved to: backtest_rr_analysis_detailed.csv")
        print(f"Total records: {len(rr_df)}")
        
        # Generate summary statistics
        summary_data = []
        
        for timeframe in self.timeframes:
            tf_data = rr_df[rr_df['Timeframe'] == timeframe]
            
            if len(tf_data) == 0:
                continue
            
            for sl_type in self.sl_types.keys():
                sl_data = tf_data[tf_data['SL_Type'] == sl_type]
                
                for rr_ratio in self.rr_ratios:
                    rr_data = sl_data[sl_data['RR_Ratio'] == rr_ratio]
                    
                    if len(rr_data) == 0:
                        continue
                    
                    wins = len(rr_data[rr_data['Outcome'] == 'WIN'])
                    losses = len(rr_data[rr_data['Outcome'] == 'LOSS'])
                    inconclusive = len(rr_data[rr_data['Outcome'] == 'INCONCLUSIVE'])
                    total = len(rr_data)
                    
                    win_rate = (wins / total * 100) if total > 0 else 0
                    
                    total_pnl = rr_data['PnL'].sum()
                    avg_win = rr_data[rr_data['Outcome'] == 'WIN']['PnL'].mean() if wins > 0 else 0
                    avg_loss = rr_data[rr_data['Outcome'] == 'LOSS']['PnL'].mean() if losses > 0 else 0
                    
                    avg_candles_win = rr_data[rr_data['Outcome'] == 'WIN']['Candles_To_Hit'].mean() if wins > 0 else 0
                    avg_candles_loss = rr_data[rr_data['Outcome'] == 'LOSS']['Candles_To_Hit'].mean() if losses > 0 else 0
                    
                    summary = {
                        'Timeframe': timeframe,
                        'SL_Type': sl_type,
                        'RR_Ratio': rr_ratio,
                        'Total_Trades': total,
                        'Wins': wins,
                        'Losses': losses,
                        'Inconclusive': inconclusive,
                        'Win_Rate_%': round(win_rate, 2),
                        'Total_PnL': round(total_pnl, 2),
                        'Avg_Win': round(avg_win, 2),
                        'Avg_Loss': round(avg_loss, 2),
                        'Avg_Candles_To_Win': round(avg_candles_win, 1),
                        'Avg_Candles_To_Loss': round(avg_candles_loss, 1),
                        'Win_Loss_Ratio': round(abs(avg_win / avg_loss), 2) if avg_loss != 0 else 0
                    }
                    summary_data.append(summary)
        
        # Save summary
        summary_df = pd.DataFrame(summary_data)
        summary_path = os.path.join(self.base_path, 'backtest_rr_summary.csv')
        summary_df.to_csv(summary_path, index=False, sep=';')
        print(f"Summary statistics saved to: backtest_rr_summary.csv")
        
        # Generate comprehensive markdown report
        self.generate_rr_report(rr_df, summary_df)
    
    def generate_rr_report(self, rr_df: pd.DataFrame, summary_df: pd.DataFrame):
        """Generate a comprehensive Risk/Reward analysis report in Markdown format."""
        report_path = os.path.join(self.base_path, 'backtest_rr_analysis.md')
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("# Risk/Reward Analysis Report\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"**Period:** 2018 - 2025\n\n")
            f.write(f"**Analysis Target:** 08:30:00 candle trades\n\n")
            
            f.write("---\n\n")
            f.write("## Methodology\n\n")
            f.write("This analysis evaluates each identified trade at 08:30:00 with multiple Risk/Reward configurations:\n\n")
            
            f.write("### Stop Loss Types\n\n")
            f.write("Stop Loss levels are calculated based on the body retracement of the 08:30 candle:\n\n")
            f.write("- **SL100 (100% retracement)**: Stop Loss placed at the opening price of the candle\n")
            f.write("- **SL75 (75% retracement)**: Stop Loss placed at 75% retracement of the candle body\n")
            f.write("- **SL50 (50% retracement)**: Stop Loss placed at the middle of the candle body\n")
            f.write("- **SL25 (25% retracement)**: Stop Loss placed close to the closing price (25% retracement)\n\n")
            
            f.write("### Risk/Reward Ratios\n\n")
            f.write("Nine different Risk/Reward ratios were tested: ")
            f.write(", ".join(map(str, self.rr_ratios)) + "\n\n")
            
            f.write("### Trade Simulation\n\n")
            f.write("For each trade:\n")
            f.write("1. Entry is taken at the close of the 08:30:00 candle\n")
            f.write("2. Stop Loss and Take Profit levels are calculated based on the configuration\n")
            f.write("3. Subsequent candles are analyzed to determine which level is hit first\n")
            f.write("4. Outcomes are classified as: WIN (TP hit), LOSS (SL hit), or INCONCLUSIVE (neither hit by end of day)\n\n")
            
            f.write("---\n\n")
            f.write("## Executive Summary\n\n")
            
            # Overall statistics
            total_scenarios = len(rr_df)
            total_trades = len(rr_df) // (len(self.sl_types) * len(self.rr_ratios))
            
            f.write(f"- **Total Trades Analyzed:** {total_trades}\n")
            f.write(f"- **Total Scenarios Tested:** {total_scenarios} ({len(self.sl_types)} SL types × {len(self.rr_ratios)} RR ratios × {total_trades} trades)\n")
            f.write(f"- **Timeframes:** {', '.join(self.timeframes)}\n\n")
            
            # Find best configurations
            if len(summary_df) > 0:
                best_winrate = summary_df.loc[summary_df['Win_Rate_%'].idxmax()]
                best_pnl = summary_df.loc[summary_df['Total_PnL'].idxmax()]
                
                f.write("### Top Performing Configurations\n\n")
                f.write(f"**Highest Win Rate:**\n")
                f.write(f"- Configuration: {best_winrate['Timeframe']} | {best_winrate['SL_Type']} | RR {best_winrate['RR_Ratio']}\n")
                f.write(f"- Win Rate: {best_winrate['Win_Rate_%']:.2f}%\n")
                f.write(f"- Wins/Losses: {best_winrate['Wins']}/{best_winrate['Losses']}\n")
                f.write(f"- Total P&L: {best_winrate['Total_PnL']:.2f}\n\n")
                
                f.write(f"**Highest Total P&L:**\n")
                f.write(f"- Configuration: {best_pnl['Timeframe']} | {best_pnl['SL_Type']} | RR {best_pnl['RR_Ratio']}\n")
                f.write(f"- Total P&L: {best_pnl['Total_PnL']:.2f}\n")
                f.write(f"- Win Rate: {best_pnl['Win_Rate_%']:.2f}%\n")
                f.write(f"- Wins/Losses: {best_pnl['Wins']}/{best_pnl['Losses']}\n\n")
            
            f.write("---\n\n")
            f.write("## Detailed Results by Timeframe\n\n")
            
            # Results for each timeframe
            for timeframe in self.timeframes:
                tf_summary = summary_df[summary_df['Timeframe'] == timeframe]
                
                if len(tf_summary) == 0:
                    continue
                
                f.write(f"### {timeframe} Timeframe\n\n")
                
                # Create comparison table for each SL type
                for sl_type in self.sl_types.keys():
                    sl_summary = tf_summary[tf_summary['SL_Type'] == sl_type]
                    
                    if len(sl_summary) == 0:
                        continue
                    
                    f.write(f"#### {sl_type} Stop Loss\n\n")
                    f.write("| RR Ratio | Win Rate % | Wins | Losses | Inconcl. | Total P&L | Avg Win | Avg Loss | W/L Ratio |\n")
                    f.write("|----------|------------|------|--------|----------|-----------|---------|----------|-----------|\n")
                    
                    for _, row in sl_summary.iterrows():
                        f.write(f"| {row['RR_Ratio']:.1f} | {row['Win_Rate_%']:.2f}% | {row['Wins']} | {row['Losses']} | {row['Inconclusive']} | ")
                        f.write(f"{row['Total_PnL']:.2f} | {row['Avg_Win']:.2f} | {row['Avg_Loss']:.2f} | {row['Win_Loss_Ratio']:.2f} |\n")
                    
                    f.write("\n")
                
                # Best configuration for this timeframe
                best_tf = tf_summary.loc[tf_summary['Win_Rate_%'].idxmax()]
                f.write(f"**Best Configuration for {timeframe}:**\n")
                f.write(f"- {best_tf['SL_Type']} with RR {best_tf['RR_Ratio']}\n")
                f.write(f"- Win Rate: {best_tf['Win_Rate_%']:.2f}%\n")
                f.write(f"- Total P&L: {best_tf['Total_PnL']:.2f}\n\n")
            
            f.write("---\n\n")
            f.write("## Stop Loss Type Comparison\n\n")
            
            # Compare SL types across all timeframes
            for sl_type in self.sl_types.keys():
                sl_summary = summary_df[summary_df['SL_Type'] == sl_type]
                
                if len(sl_summary) == 0:
                    continue
                
                f.write(f"### {sl_type} Analysis\n\n")
                
                avg_winrate = sl_summary['Win_Rate_%'].mean()
                total_pnl = sl_summary['Total_PnL'].sum()
                
                f.write(f"- **Average Win Rate:** {avg_winrate:.2f}%\n")
                f.write(f"- **Total P&L across all scenarios:** {total_pnl:.2f}\n")
                f.write(f"- **Number of scenarios:** {len(sl_summary)}\n\n")
                
                # Best RR for this SL type
                best_rr = sl_summary.loc[sl_summary['Win_Rate_%'].idxmax()]
                f.write(f"**Best performing RR ratio:** {best_rr['RR_Ratio']} ({best_rr['Timeframe']})\n")
                f.write(f"- Win Rate: {best_rr['Win_Rate_%']:.2f}%\n")
                f.write(f"- Total P&L: {best_rr['Total_PnL']:.2f}\n\n")
            
            f.write("---\n\n")
            f.write("## Risk/Reward Ratio Comparison\n\n")
            
            # Compare RR ratios
            f.write("Average Win Rate by RR Ratio (across all SL types and timeframes):\n\n")
            f.write("| RR Ratio | Avg Win Rate % | Total Scenarios | Total P&L |\n")
            f.write("|----------|----------------|-----------------|------------|\n")
            
            for rr in self.rr_ratios:
                rr_summary = summary_df[summary_df['RR_Ratio'] == rr]
                if len(rr_summary) > 0:
                    avg_wr = rr_summary['Win_Rate_%'].mean()
                    total_pnl = rr_summary['Total_PnL'].sum()
                    count = len(rr_summary)
                    f.write(f"| {rr:.1f} | {avg_wr:.2f}% | {count} | {total_pnl:.2f} |\n")
            
            f.write("\n")
            
            f.write("---\n\n")
            f.write("## Conclusions and Recommendations\n\n")
            
            # Generate recommendations based on data
            if len(summary_df) > 0:
                # Best overall configurations
                top_5 = summary_df.nlargest(5, 'Win_Rate_%')
                
                f.write("### Top 5 Configurations by Win Rate\n\n")
                f.write("| Rank | Timeframe | SL Type | RR Ratio | Win Rate % | Total P&L | Wins/Losses |\n")
                f.write("|------|-----------|---------|----------|------------|-----------|-------------|\n")
                
                for i, (_, row) in enumerate(top_5.iterrows(), 1):
                    f.write(f"| {i} | {row['Timeframe']} | {row['SL_Type']} | {row['RR_Ratio']:.1f} | ")
                    f.write(f"{row['Win_Rate_%']:.2f}% | {row['Total_PnL']:.2f} | {row['Wins']}/{row['Losses']} |\n")
                
                f.write("\n### Key Insights\n\n")
                
                # Analyze trends
                avg_wr_by_sl = summary_df.groupby('SL_Type')['Win_Rate_%'].mean().sort_values(ascending=False)
                f.write(f"1. **Best Stop Loss Type:** {avg_wr_by_sl.index[0]} with average win rate of {avg_wr_by_sl.iloc[0]:.2f}%\n")
                
                avg_wr_by_rr = summary_df.groupby('RR_Ratio')['Win_Rate_%'].mean().sort_values(ascending=False)
                f.write(f"2. **Best Risk/Reward Ratio:** {avg_wr_by_rr.index[0]:.1f} with average win rate of {avg_wr_by_rr.iloc[0]:.2f}%\n")
                
                avg_wr_by_tf = summary_df.groupby('Timeframe')['Win_Rate_%'].mean().sort_values(ascending=False)
                f.write(f"3. **Best Timeframe:** {avg_wr_by_tf.index[0]} with average win rate of {avg_wr_by_tf.iloc[0]:.2f}%\n")
                
                f.write("\n### Trading Recommendations\n\n")
                f.write("Based on the analysis:\n\n")
                
                best_config = summary_df.loc[summary_df['Win_Rate_%'].idxmax()]
                f.write(f"- **Recommended Configuration:** {best_config['Timeframe']} | {best_config['SL_Type']} | RR {best_config['RR_Ratio']}\n")
                f.write(f"  - Win Rate: {best_config['Win_Rate_%']:.2f}%\n")
                f.write(f"  - Average Win: {best_config['Avg_Win']:.2f} points\n")
                f.write(f"  - Average Loss: {best_config['Avg_Loss']:.2f} points\n")
                f.write(f"  - Win/Loss Ratio: {best_config['Win_Loss_Ratio']:.2f}\n\n")
                
                # Profitable configurations
                profitable = summary_df[summary_df['Total_PnL'] > 0]
                f.write(f"- **Profitable Configurations:** {len(profitable)} out of {len(summary_df)} ({100*len(profitable)/len(summary_df):.1f}%)\n\n")
                
                f.write("### Risk Considerations\n\n")
                f.write("- Tighter stop losses (SL25) reduce risk per trade but may result in more frequent stop-outs\n")
                f.write("- Wider stop losses (SL100) allow more room for price movement but increase risk per trade\n")
                f.write("- Higher RR ratios offer better reward potential but typically have lower win rates\n")
                f.write("- Consider your risk tolerance and account size when selecting a configuration\n\n")
            
            f.write("---\n\n")
            f.write("## Data Files\n\n")
            f.write("- `backtest_rr_analysis_detailed.csv`: Complete trade-by-trade results for all scenarios\n")
            f.write("- `backtest_rr_summary.csv`: Aggregated statistics for each configuration\n")
            f.write("- `backtest_results.csv`: Original identified trades at 08:30:00\n")
            f.write("- `backtest_summary.txt`: Summary of identified trades\n\n")
            
            f.write("---\n\n")
            f.write(f"*Report generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")
        
        print(f"Comprehensive RR analysis report saved to: backtest_rr_analysis.md")
        print("\n" + "=" * 80)
        print("Top 3 Configurations by Win Rate:")
        print("=" * 80)
        
        if len(summary_df) > 0:
            top_3 = summary_df.nlargest(3, 'Win_Rate_%')
            for i, (_, row) in enumerate(top_3.iterrows(), 1):
                print(f"{i}. {row['Timeframe']:>4} | {row['SL_Type']:>5} | RR {row['RR_Ratio']:>3.1f} | "
                      f"WR: {row['Win_Rate_%']:>5.2f}% | P&L: {row['Total_PnL']:>8.2f} | "
                      f"W/L: {row['Wins']}/{row['Losses']}")
        
        print("=" * 80)


def main():
    """Main entry point for the backtest script."""
    import sys
    
    # Get the base path (current directory where the script is run)
    base_path = os.path.dirname(os.path.abspath(__file__))
    
    # Create backtest instance
    backtest = BacktestStrategy(base_path)
    
    # Check if user wants to run RR analysis
    run_rr = '--rr' in sys.argv or '--risk-reward' in sys.argv
    
    # Run the backtest
    backtest.run_backtest()
    
    # Save results
    backtest.save_results()
    
    if run_rr:
        # Run Risk/Reward analysis
        backtest.run_rr_analysis()
        
        # Save RR results
        backtest.save_rr_results()
        
        print("\n" + "=" * 80)
        print("BACKTEST WITH RR ANALYSIS COMPLETED SUCCESSFULLY")
        print("=" * 80)
        print("\nOutput files:")
        print("  - backtest_results.csv: Detailed results of all trades found")
        print("  - backtest_summary.txt: Summary report with statistics")
        print("  - backtest_rr_analysis_detailed.csv: Detailed RR analysis for all trades")
        print("  - backtest_rr_summary.csv: Summary statistics for each configuration")
        print("  - backtest_rr_analysis.md: Comprehensive RR analysis report")
        print("=" * 80)
    else:
        print("\n" + "=" * 80)
        print("BACKTEST COMPLETED SUCCESSFULLY")
        print("=" * 80)
        print("\nOutput files:")
        print("  - backtest_results.csv: Detailed results of all trades found")
        print("  - backtest_summary.txt: Summary report with statistics")
        print("\nTo run Risk/Reward analysis, use: python backtest_strategy.py --rr")
        print("=" * 80)


if __name__ == "__main__":
    main()

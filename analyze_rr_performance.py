#!/usr/bin/env python3
"""
Risk/Reward Performance Analysis Script

This script performs comprehensive backtesting of trading setups with different
Stop Loss (SL) and Take Profit (TP) configurations.

SL Strategies (based on 8:30 candle body retracement):
- 100%: SL at full body opposite end
- 75%: SL at 75% body retracement
- 50%: SL at 50% body retracement (middle)
- 25%: SL at 25% body retracement (close to entry)

Risk/Reward Ratios:
- 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0

For each setup, the script:
1. Loads the identified setups from detailed CSV files
2. Loads the raw price data for post-entry tracking
3. Simulates each trade with all SL/RR combinations
4. Tracks whether SL or TP was hit first
5. Generates comprehensive performance reports
"""

import pandas as pd
import numpy as np
from datetime import datetime, time, timedelta
import os
import zipfile
import glob
from collections import defaultdict
import json


class RRPerformanceAnalyzer:
    def __init__(self, base_path):
        self.base_path = base_path
        self.timeframes = ['1m', '5m', '15m']
        
        # SL percentages (of 8:30 candle body)
        self.sl_percentages = [100, 75, 50, 25]
        
        # RR ratios
        self.rr_ratios = [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]
        
        # Store all results
        self.all_trades = defaultdict(list)  # timeframe -> list of trade results
        self.performance_matrix = {}  # (timeframe, sl_pct, rr) -> stats
        
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
    
    def load_setups(self, timeframe):
        """Load identified setups from detailed CSV"""
        filename = os.path.join(self.base_path, f'trading_setup_{timeframe}_detailed.csv')
        
        if not os.path.exists(filename):
            print(f"Warning: File not found: {filename}")
            return None
        
        try:
            df = pd.read_csv(filename)
            # Parse date and time
            df['date'] = pd.to_datetime(df['date'])
            df['time'] = pd.to_datetime(df['time'], format='%H:%M:%S').dt.time
            
            print(f"Loaded {len(df)} setups from {filename}")
            return df
        except Exception as e:
            print(f"Error loading {filename}: {e}")
            return None
    
    def load_raw_data(self, year, timeframe):
        """Load raw CSV data for price tracking"""
        filename = os.path.join(self.base_path, f"{year} {timeframe}.csv")
        
        if not os.path.exists(filename):
            print(f"Warning: File not found: {filename}")
            return None
        
        try:
            # Read CSV with semicolon delimiter
            df = pd.read_csv(filename, sep=';', header=0)
            
            # Rename columns
            df.columns = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
            
            # Parse datetime
            df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], 
                                           format='%d/%m/%Y %H:%M:%S')
            
            # Convert price columns to float
            for col in ['Open', 'High', 'Low', 'Close']:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            
            df = df.sort_values('DateTime').reset_index(drop=True)
            return df
            
        except Exception as e:
            print(f"Error loading {filename}: {e}")
            return None
    
    def calculate_sl_tp_levels(self, setup, sl_percentage, rr_ratio):
        """
        Calculate Stop Loss and Take Profit levels
        
        Args:
            setup: Dict with setup information
            sl_percentage: Percentage of body for SL (100, 75, 50, 25)
            rr_ratio: Risk/Reward ratio
        
        Returns:
            dict with entry, sl, tp, direction
        """
        # Determine trade direction
        if setup['setup_type'] == 'bearish_830_to_bullish_breakout':
            direction = 'LONG'
        else:  # bullish_830_to_bearish_breakdown
            direction = 'SHORT'
        
        # Entry is at the close of the next candle (candle after 8:30)
        entry_price = setup['next_candle_close']
        
        # Calculate 8:30 candle body
        candle_830_open = setup['candle_830_open']
        candle_830_close = setup['candle_830_close']
        body_size = abs(candle_830_close - candle_830_open)
        
        # For bearish 8:30 candle: close is at bottom, open is at top
        # For bullish 8:30 candle: open is at bottom, close is at top
        is_830_bearish = candle_830_close < candle_830_open
        
        if is_830_bearish:
            body_top = candle_830_open
            body_bottom = candle_830_close
        else:
            body_top = candle_830_close
            body_bottom = candle_830_open
        
        # Calculate SL based on body retracement
        if direction == 'LONG':
            # For LONG: SL is below entry, at some level of body retracement
            # 100% = full body bottom, 75% = 75% down from top, etc.
            sl_level = body_top - (body_size * sl_percentage / 100.0)
            risk = entry_price - sl_level
            tp_level = entry_price + (risk * rr_ratio)
        else:  # SHORT
            # For SHORT: SL is above entry, at some level of body retracement
            # 100% = full body top, 75% = 75% up from bottom, etc.
            sl_level = body_bottom + (body_size * sl_percentage / 100.0)
            risk = sl_level - entry_price
            tp_level = entry_price - (risk * rr_ratio)
        
        return {
            'entry': entry_price,
            'sl': sl_level,
            'tp': tp_level,
            'risk': risk,
            'direction': direction,
            'body_size': body_size,
            'body_top': body_top,
            'body_bottom': body_bottom
        }
    
    def simulate_trade(self, setup, levels, raw_data, timeframe):
        """
        Simulate a trade to see if SL or TP was hit first
        
        Args:
            setup: Setup dict
            levels: Dict with entry, sl, tp, direction
            raw_data: DataFrame with price data
            timeframe: String like '1m', '5m', '15m'
        
        Returns:
            dict with trade result
        """
        direction = levels['direction']
        entry = levels['entry']
        sl = levels['sl']
        tp = levels['tp']
        
        # Find the entry candle in raw data
        # The entry is at next_candle_close, which is the candle after 8:30
        setup_datetime = datetime.combine(setup['date'], setup['time'])
        
        # Get timeframe offset for next candle
        if timeframe == '1m':
            entry_time = setup_datetime + timedelta(minutes=2)  # 2 candles after 8:30
        elif timeframe == '5m':
            entry_time = setup_datetime + timedelta(minutes=10)  # 2 candles after 8:30
        elif timeframe == '15m':
            entry_time = setup_datetime + timedelta(minutes=30)  # 2 candles after 8:30
        else:
            return None
        
        # Get candles after entry
        future_candles = raw_data[raw_data['DateTime'] >= entry_time].copy()
        
        if len(future_candles) == 0:
            return None
        
        # Check each candle to see if SL or TP was hit
        for idx, candle in future_candles.iterrows():
            if direction == 'LONG':
                # For LONG: check if price went down to SL or up to TP
                # Check SL first (conservative assumption: low happens before high)
                if candle['Low'] <= sl:
                    return {
                        'outcome': 'LOSS',
                        'exit_price': sl,
                        'exit_time': candle['DateTime'],
                        'pnl': -levels['risk'],  # Lost 1 risk unit
                        'bars_held': (candle['DateTime'] - setup_datetime).total_seconds() / 60
                    }
                elif candle['High'] >= tp:
                    return {
                        'outcome': 'WIN',
                        'exit_price': tp,
                        'exit_time': candle['DateTime'],
                        'pnl': levels['risk'] * (tp - entry) / (entry - sl),  # Profit in risk units
                        'bars_held': (candle['DateTime'] - setup_datetime).total_seconds() / 60
                    }
            else:  # SHORT
                # For SHORT: check if price went up to SL or down to TP
                # Check SL first (conservative assumption: high happens before low)
                if candle['High'] >= sl:
                    return {
                        'outcome': 'LOSS',
                        'exit_price': sl,
                        'exit_time': candle['DateTime'],
                        'pnl': -levels['risk'],  # Lost 1 risk unit
                        'bars_held': (candle['DateTime'] - setup_datetime).total_seconds() / 60
                    }
                elif candle['Low'] <= tp:
                    return {
                        'outcome': 'WIN',
                        'exit_price': tp,
                        'exit_time': candle['DateTime'],
                        'pnl': levels['risk'] * (entry - tp) / (sl - entry),  # Profit in risk units
                        'bars_held': (candle['DateTime'] - setup_datetime).total_seconds() / 60
                    }
        
        # Neither SL nor TP was hit in available data
        return {
            'outcome': 'NO_EXIT',
            'exit_price': None,
            'exit_time': None,
            'pnl': 0,
            'bars_held': None
        }
    
    def analyze_timeframe(self, timeframe):
        """Analyze all setups for a given timeframe with all SL/RR combinations"""
        print(f"\n{'='*80}")
        print(f"ANALYZING TIMEFRAME: {timeframe}")
        print(f"{'='*80}")
        
        # Load setups
        setups_df = self.load_setups(timeframe)
        if setups_df is None or len(setups_df) == 0:
            print(f"No setups found for {timeframe}")
            return
        
        # Group by year to load raw data efficiently
        years = setups_df['year'].unique()
        
        for year in sorted(years):
            print(f"\nProcessing {year} {timeframe}...")
            year_setups = setups_df[setups_df['year'] == year]
            
            # Load raw data for this year
            raw_data = self.load_raw_data(year, timeframe)
            if raw_data is None:
                print(f"  ✗ Could not load raw data for {year} {timeframe}")
                continue
            
            # Process each setup
            for idx, setup in year_setups.iterrows():
                # Test all SL/RR combinations
                for sl_pct in self.sl_percentages:
                    for rr in self.rr_ratios:
                        # Calculate levels
                        levels = self.calculate_sl_tp_levels(setup, sl_pct, rr)
                        
                        # Simulate trade
                        result = self.simulate_trade(setup, levels, raw_data, timeframe)
                        
                        if result is None:
                            continue
                        
                        # Store comprehensive trade data
                        trade_data = {
                            'timeframe': timeframe,
                            'year': year,
                            'date': setup['date'],
                            'time': setup['time'],
                            'setup_type': setup['setup_type'],
                            'direction': levels['direction'],
                            'sl_percentage': sl_pct,
                            'rr_ratio': rr,
                            'entry_price': levels['entry'],
                            'sl_price': levels['sl'],
                            'tp_price': levels['tp'],
                            'risk': levels['risk'],
                            'body_size': levels['body_size'],
                            'outcome': result['outcome'],
                            'exit_price': result['exit_price'],
                            'exit_time': result['exit_time'],
                            'pnl': result['pnl'],
                            'bars_held': result['bars_held']
                        }
                        
                        self.all_trades[timeframe].append(trade_data)
            
            print(f"  ✓ Processed {len(year_setups)} setups from {year}")
        
        print(f"\n✓ Completed {timeframe}: {len(self.all_trades[timeframe])} total trade simulations")
    
    def calculate_performance_metrics(self):
        """Calculate performance metrics for each SL/RR combination"""
        print("\n" + "="*80)
        print("CALCULATING PERFORMANCE METRICS")
        print("="*80)
        
        for timeframe in self.timeframes:
            if timeframe not in self.all_trades or len(self.all_trades[timeframe]) == 0:
                continue
            
            trades_df = pd.DataFrame(self.all_trades[timeframe])
            
            # Calculate metrics for each SL/RR combination
            for sl_pct in self.sl_percentages:
                for rr in self.rr_ratios:
                    # Filter trades for this combination
                    mask = (trades_df['sl_percentage'] == sl_pct) & (trades_df['rr_ratio'] == rr)
                    subset = trades_df[mask]
                    
                    if len(subset) == 0:
                        continue
                    
                    # Calculate statistics
                    total_trades = len(subset)
                    wins = len(subset[subset['outcome'] == 'WIN'])
                    losses = len(subset[subset['outcome'] == 'LOSS'])
                    no_exit = len(subset[subset['outcome'] == 'NO_EXIT'])
                    
                    win_rate = (wins / (wins + losses) * 100) if (wins + losses) > 0 else 0
                    
                    # PnL calculations (assuming 1 risk unit per trade)
                    total_pnl = subset['pnl'].sum()
                    avg_pnl = subset['pnl'].mean()
                    
                    winning_trades = subset[subset['outcome'] == 'WIN']
                    losing_trades = subset[subset['outcome'] == 'LOSS']
                    
                    avg_win = winning_trades['pnl'].mean() if len(winning_trades) > 0 else 0
                    avg_loss = losing_trades['pnl'].mean() if len(losing_trades) > 0 else 0
                    
                    best_trade = subset['pnl'].max() if len(subset) > 0 else 0
                    worst_trade = subset['pnl'].min() if len(subset) > 0 else 0
                    
                    # Average bars held
                    avg_bars = subset[subset['bars_held'].notna()]['bars_held'].mean()
                    
                    # Store metrics
                    key = (timeframe, sl_pct, rr)
                    self.performance_matrix[key] = {
                        'timeframe': timeframe,
                        'sl_percentage': sl_pct,
                        'rr_ratio': rr,
                        'total_trades': total_trades,
                        'wins': wins,
                        'losses': losses,
                        'no_exit': no_exit,
                        'win_rate': win_rate,
                        'total_pnl': total_pnl,
                        'avg_pnl': avg_pnl,
                        'avg_win': avg_win,
                        'avg_loss': avg_loss,
                        'best_trade': best_trade,
                        'worst_trade': worst_trade,
                        'avg_bars_held': avg_bars
                    }
        
        print(f"✓ Calculated metrics for {len(self.performance_matrix)} combinations")
    
    def generate_detailed_csv_reports(self):
        """Generate detailed CSV reports for each timeframe"""
        print("\n" + "="*80)
        print("GENERATING DETAILED CSV REPORTS")
        print("="*80)
        
        for timeframe in self.timeframes:
            if timeframe not in self.all_trades or len(self.all_trades[timeframe]) == 0:
                continue
            
            trades_df = pd.DataFrame(self.all_trades[timeframe])
            
            # Sort by date and time
            trades_df = trades_df.sort_values(['date', 'time', 'sl_percentage', 'rr_ratio'])
            
            filename = f'rr_analysis_detailed_{timeframe}.csv'
            filepath = os.path.join(self.base_path, filename)
            trades_df.to_csv(filepath, index=False)
            
            print(f"✓ Saved {filename} ({len(trades_df)} records)")
    
    def generate_matrix_report(self):
        """Generate win rate matrix CSV"""
        print("\n" + "="*80)
        print("GENERATING MATRIX REPORT")
        print("="*80)
        
        matrix_data = []
        
        for key, metrics in self.performance_matrix.items():
            matrix_data.append(metrics)
        
        if len(matrix_data) > 0:
            matrix_df = pd.DataFrame(matrix_data)
            
            # Sort by timeframe, SL%, RR
            matrix_df = matrix_df.sort_values(['timeframe', 'sl_percentage', 'rr_ratio'])
            
            filename = 'rr_analysis_matrix.csv'
            filepath = os.path.join(self.base_path, filename)
            matrix_df.to_csv(filepath, index=False)
            
            print(f"✓ Saved {filename} ({len(matrix_df)} records)")
    
    def generate_comprehensive_report(self):
        """Generate comprehensive text report"""
        print("\n" + "="*80)
        print("GENERATING COMPREHENSIVE TEXT REPORT")
        print("="*80)
        
        report_lines = []
        report_lines.append("="*80)
        report_lines.append("RISK/REWARD PERFORMANCE ANALYSIS - COMPREHENSIVE REPORT")
        report_lines.append("="*80)
        report_lines.append("")
        report_lines.append("Analysis Date: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        report_lines.append("")
        report_lines.append("METHODOLOGY:")
        report_lines.append("-" * 80)
        report_lines.append("Stop Loss Placements (% of 8:30 candle body retracement):")
        report_lines.append("  - 100%: SL at opposite end of body (full body)")
        report_lines.append("  - 75%:  SL at 75% of body (long retracement)")
        report_lines.append("  - 50%:  SL at middle of body")
        report_lines.append("  - 25%:  SL at 25% of body (close SL)")
        report_lines.append("")
        report_lines.append("Risk/Reward Ratios Tested:")
        report_lines.append("  - 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0")
        report_lines.append("")
        report_lines.append("Entry Logic:")
        report_lines.append("  - Entry at close of candle that triggered setup (after 8:30)")
        report_lines.append("  - Bearish 8:30 → Bullish breakout = LONG")
        report_lines.append("  - Bullish 8:30 → Bearish breakdown = SHORT")
        report_lines.append("")
        report_lines.append("="*80)
        report_lines.append("")
        
        # Overall summary by timeframe
        report_lines.append("OVERALL SUMMARY BY TIMEFRAME:")
        report_lines.append("-" * 80)
        
        for timeframe in self.timeframes:
            if timeframe not in self.all_trades:
                continue
            
            trades_df = pd.DataFrame(self.all_trades[timeframe])
            if len(trades_df) == 0:
                continue
            
            # Unique setups (date/time combinations)
            unique_setups = trades_df[['date', 'time']].drop_duplicates()
            
            report_lines.append(f"\n{timeframe.upper()} Timeframe:")
            report_lines.append(f"  Total Unique Setups: {len(unique_setups)}")
            report_lines.append(f"  Total Trade Simulations: {len(trades_df)}")
            report_lines.append(f"  Years Covered: {sorted(trades_df['year'].unique())}")
            
            # Breakdown by setup type
            for setup_type in trades_df['setup_type'].unique():
                count = len(trades_df[trades_df['setup_type'] == setup_type])
                report_lines.append(f"    {setup_type}: {count} simulations")
        
        report_lines.append("")
        report_lines.append("="*80)
        
        # Performance by timeframe
        for timeframe in self.timeframes:
            report_lines.append(f"\n{'='*80}")
            report_lines.append(f"{timeframe.upper()} TIMEFRAME DETAILED ANALYSIS")
            report_lines.append(f"{'='*80}")
            
            # Get all metrics for this timeframe
            tf_metrics = [v for k, v in self.performance_matrix.items() if k[0] == timeframe]
            
            if len(tf_metrics) == 0:
                report_lines.append("No data available.")
                continue
            
            # Organize by SL percentage
            for sl_pct in self.sl_percentages:
                report_lines.append(f"\n{'-'*80}")
                report_lines.append(f"Stop Loss at {sl_pct}% Body Retracement:")
                report_lines.append(f"{'-'*80}")
                
                sl_metrics = [m for m in tf_metrics if m['sl_percentage'] == sl_pct]
                
                if len(sl_metrics) == 0:
                    continue
                
                report_lines.append(f"\n{'RR':<6} {'Trades':<8} {'Wins':<6} {'Losses':<8} "
                                  f"{'WinRate':<10} {'TotalPnL':<12} {'AvgPnL':<10} "
                                  f"{'AvgWin':<10} {'AvgLoss':<10}")
                report_lines.append("-" * 80)
                
                for m in sorted(sl_metrics, key=lambda x: x['rr_ratio']):
                    report_lines.append(
                        f"{m['rr_ratio']:<6.1f} {m['total_trades']:<8} "
                        f"{m['wins']:<6} {m['losses']:<8} "
                        f"{m['win_rate']:<10.2f} {m['total_pnl']:<12.2f} "
                        f"{m['avg_pnl']:<10.2f} {m['avg_win']:<10.2f} "
                        f"{m['avg_loss']:<10.2f}"
                    )
                
                report_lines.append("")
        
        # Best performing configurations
        report_lines.append("\n" + "="*80)
        report_lines.append("TOP PERFORMING CONFIGURATIONS")
        report_lines.append("="*80)
        
        # Sort by total PnL
        all_metrics = list(self.performance_matrix.values())
        
        report_lines.append("\nTop 10 by Total PnL:")
        report_lines.append("-" * 80)
        top_pnl = sorted(all_metrics, key=lambda x: x['total_pnl'], reverse=True)[:10]
        
        report_lines.append(f"{'Rank':<6} {'TF':<6} {'SL%':<6} {'RR':<6} {'WinRate':<10} "
                          f"{'TotalPnL':<12} {'Trades':<8}")
        report_lines.append("-" * 80)
        
        for i, m in enumerate(top_pnl, 1):
            report_lines.append(
                f"{i:<6} {m['timeframe']:<6} {m['sl_percentage']:<6} "
                f"{m['rr_ratio']:<6.1f} {m['win_rate']:<10.2f} "
                f"{m['total_pnl']:<12.2f} {m['total_trades']:<8}"
            )
        
        report_lines.append("\nTop 10 by Win Rate (min 10 trades):")
        report_lines.append("-" * 80)
        valid_metrics = [m for m in all_metrics if m['total_trades'] >= 10]
        top_winrate = sorted(valid_metrics, key=lambda x: x['win_rate'], reverse=True)[:10]
        
        report_lines.append(f"{'Rank':<6} {'TF':<6} {'SL%':<6} {'RR':<6} {'WinRate':<10} "
                          f"{'TotalPnL':<12} {'Trades':<8}")
        report_lines.append("-" * 80)
        
        for i, m in enumerate(top_winrate, 1):
            report_lines.append(
                f"{i:<6} {m['timeframe']:<6} {m['sl_percentage']:<6} "
                f"{m['rr_ratio']:<6.1f} {m['win_rate']:<10.2f} "
                f"{m['total_pnl']:<12.2f} {m['total_trades']:<8}"
            )
        
        report_lines.append("\nTop 10 by Average PnL per Trade:")
        report_lines.append("-" * 80)
        top_avg_pnl = sorted(all_metrics, key=lambda x: x['avg_pnl'], reverse=True)[:10]
        
        report_lines.append(f"{'Rank':<6} {'TF':<6} {'SL%':<6} {'RR':<6} {'WinRate':<10} "
                          f"{'AvgPnL':<12} {'Trades':<8}")
        report_lines.append("-" * 80)
        
        for i, m in enumerate(top_avg_pnl, 1):
            report_lines.append(
                f"{i:<6} {m['timeframe']:<6} {m['sl_percentage']:<6} "
                f"{m['rr_ratio']:<6.1f} {m['win_rate']:<10.2f} "
                f"{m['avg_pnl']:<12.2f} {m['total_trades']:<8}"
            )
        
        report_lines.append("")
        report_lines.append("="*80)
        report_lines.append("END OF REPORT")
        report_lines.append("="*80)
        
        # Save report
        report_text = "\n".join(report_lines)
        filename = 'rr_analysis_comprehensive_report.txt'
        filepath = os.path.join(self.base_path, filename)
        
        with open(filepath, 'w') as f:
            f.write(report_text)
        
        print(f"✓ Saved {filename}")
        
        # Also print to console
        print("\n" + report_text)
    
    def generate_summary_markdown(self):
        """Generate executive summary in Markdown format"""
        print("\n" + "="*80)
        print("GENERATING EXECUTIVE SUMMARY (MARKDOWN)")
        print("="*80)
        
        md_lines = []
        md_lines.append("# Risk/Reward Analysis - Executive Summary")
        md_lines.append("")
        md_lines.append(f"**Analysis Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        md_lines.append("")
        md_lines.append("## Overview")
        md_lines.append("")
        md_lines.append("This analysis evaluates the performance of identified trading setups across different Stop Loss (SL) and Take Profit (TP) configurations.")
        md_lines.append("")
        md_lines.append("### Tested Configurations")
        md_lines.append("")
        md_lines.append("**Stop Loss Placements** (% of 8:30 candle body retracement):")
        md_lines.append("- **100%**: SL at opposite end of body (full body)")
        md_lines.append("- **75%**: SL at 75% of body (long retracement)")
        md_lines.append("- **50%**: SL at middle of body")
        md_lines.append("- **25%**: SL at 25% of body (close SL)")
        md_lines.append("")
        md_lines.append("**Risk/Reward Ratios:** 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0")
        md_lines.append("")
        md_lines.append("## Key Findings")
        md_lines.append("")
        
        # Calculate overall statistics
        all_metrics = list(self.performance_matrix.values())
        
        if len(all_metrics) > 0:
            # Best overall configuration
            best_pnl = max(all_metrics, key=lambda x: x['total_pnl'])
            
            md_lines.append("### Best Overall Configuration")
            md_lines.append("")
            md_lines.append(f"- **Timeframe:** {best_pnl['timeframe']}")
            md_lines.append(f"- **Stop Loss:** {best_pnl['sl_percentage']}% body retracement")
            md_lines.append(f"- **Risk/Reward:** {best_pnl['rr_ratio']}")
            md_lines.append(f"- **Win Rate:** {best_pnl['win_rate']:.2f}%")
            md_lines.append(f"- **Total PnL:** {best_pnl['total_pnl']:.2f} risk units")
            md_lines.append(f"- **Total Trades:** {best_pnl['total_trades']}")
            md_lines.append("")
            
            # Highest win rate (with sufficient trades)
            valid_metrics = [m for m in all_metrics if m['total_trades'] >= 10]
            if len(valid_metrics) > 0:
                best_winrate = max(valid_metrics, key=lambda x: x['win_rate'])
                
                md_lines.append("### Highest Win Rate Configuration (min 10 trades)")
                md_lines.append("")
                md_lines.append(f"- **Timeframe:** {best_winrate['timeframe']}")
                md_lines.append(f"- **Stop Loss:** {best_winrate['sl_percentage']}% body retracement")
                md_lines.append(f"- **Risk/Reward:** {best_winrate['rr_ratio']}")
                md_lines.append(f"- **Win Rate:** {best_winrate['win_rate']:.2f}%")
                md_lines.append(f"- **Total PnL:** {best_winrate['total_pnl']:.2f} risk units")
                md_lines.append(f"- **Total Trades:** {best_winrate['total_trades']}")
                md_lines.append("")
        
        # Summary by timeframe
        md_lines.append("## Performance by Timeframe")
        md_lines.append("")
        
        for timeframe in self.timeframes:
            if timeframe not in self.all_trades:
                continue
            
            trades_df = pd.DataFrame(self.all_trades[timeframe])
            if len(trades_df) == 0:
                continue
            
            unique_setups = trades_df[['date', 'time']].drop_duplicates()
            
            md_lines.append(f"### {timeframe.upper()} Timeframe")
            md_lines.append("")
            md_lines.append(f"- **Unique Setups:** {len(unique_setups)}")
            md_lines.append(f"- **Total Simulations:** {len(trades_df)}")
            
            # Get best configuration for this timeframe
            tf_metrics = [v for k, v in self.performance_matrix.items() if k[0] == timeframe]
            if len(tf_metrics) > 0:
                best_tf = max(tf_metrics, key=lambda x: x['total_pnl'])
                md_lines.append(f"- **Best Config:** SL {best_tf['sl_percentage']}%, RR {best_tf['rr_ratio']} "
                              f"(Win Rate: {best_tf['win_rate']:.2f}%, Total PnL: {best_tf['total_pnl']:.2f})")
            
            md_lines.append("")
        
        # Top configurations table
        md_lines.append("## Top 10 Configurations by Total PnL")
        md_lines.append("")
        md_lines.append("| Rank | Timeframe | SL % | RR | Win Rate | Total PnL | Trades |")
        md_lines.append("|------|-----------|------|-----|----------|-----------|--------|")
        
        top_configs = sorted(all_metrics, key=lambda x: x['total_pnl'], reverse=True)[:10]
        for i, m in enumerate(top_configs, 1):
            md_lines.append(f"| {i} | {m['timeframe']} | {m['sl_percentage']} | "
                          f"{m['rr_ratio']:.1f} | {m['win_rate']:.2f}% | "
                          f"{m['total_pnl']:.2f} | {m['total_trades']} |")
        
        md_lines.append("")
        md_lines.append("## Recommendations")
        md_lines.append("")
        md_lines.append("Based on this analysis:")
        md_lines.append("")
        md_lines.append("1. Review the top performing configurations in detail")
        md_lines.append("2. Consider the trade-off between win rate and total PnL")
        md_lines.append("3. Examine the distribution of wins/losses across different market conditions")
        md_lines.append("4. Test the selected configurations on out-of-sample data before live trading")
        md_lines.append("")
        md_lines.append("## Files Generated")
        md_lines.append("")
        md_lines.append("- `rr_analysis_detailed_1m.csv` - Per-trade results for 1-minute timeframe")
        md_lines.append("- `rr_analysis_detailed_5m.csv` - Per-trade results for 5-minute timeframe")
        md_lines.append("- `rr_analysis_detailed_15m.csv` - Per-trade results for 15-minute timeframe")
        md_lines.append("- `rr_analysis_matrix.csv` - Performance matrix for all configurations")
        md_lines.append("- `rr_analysis_comprehensive_report.txt` - Full detailed report")
        md_lines.append("")
        
        # Save markdown
        md_text = "\n".join(md_lines)
        filename = 'rr_analysis_summary.md'
        filepath = os.path.join(self.base_path, filename)
        
        with open(filepath, 'w') as f:
            f.write(md_text)
        
        print(f"✓ Saved {filename}")
    
    def run_full_analysis(self):
        """Run the complete analysis pipeline"""
        print("="*80)
        print("RISK/REWARD PERFORMANCE ANALYSIS")
        print("="*80)
        print("")
        print(f"Base Path: {self.base_path}")
        print(f"Timeframes: {', '.join(self.timeframes)}")
        print(f"SL Percentages: {', '.join(map(str, self.sl_percentages))}")
        print(f"RR Ratios: {', '.join(map(str, self.rr_ratios))}")
        print("")
        
        # Unzip files if needed
        self.unzip_1m_files()
        
        # Analyze each timeframe
        for timeframe in self.timeframes:
            self.analyze_timeframe(timeframe)
        
        # Calculate performance metrics
        self.calculate_performance_metrics()
        
        # Generate reports
        self.generate_detailed_csv_reports()
        self.generate_matrix_report()
        self.generate_comprehensive_report()
        self.generate_summary_markdown()
        
        print("\n" + "="*80)
        print("ANALYSIS COMPLETE!")
        print("="*80)
        print("\nGenerated files:")
        print("  - rr_analysis_detailed_1m.csv")
        print("  - rr_analysis_detailed_5m.csv")
        print("  - rr_analysis_detailed_15m.csv")
        print("  - rr_analysis_matrix.csv")
        print("  - rr_analysis_comprehensive_report.txt")
        print("  - rr_analysis_summary.md")
        print("")


def main():
    base_path = '/home/runner/work/Backtest-Trading/Backtest-Trading'
    
    analyzer = RRPerformanceAnalyzer(base_path)
    analyzer.run_full_analysis()


if __name__ == "__main__":
    main()

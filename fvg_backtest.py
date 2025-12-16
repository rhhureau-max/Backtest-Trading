#!/usr/bin/env python3
"""
FVG (Fair Value Gap) Trading Strategy Backtesting System
---------------------------------------------------------
This script analyzes FVG-based trading strategies across multiple timeframes,
stop-loss configurations, and risk-to-reward ratios for the period 2018-2025.

Author: Trading Strategy Analyzer
Date: 2025-11-24
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, time, timedelta
from pathlib import Path
import warnings
from tabulate import tabulate
import os

warnings.filterwarnings('ignore')

# Set style for plots
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)


class FVGBacktester:
    """
    Fair Value Gap Backtesting System
    
    This class handles FVG detection, trade execution, and performance analysis
    for multiple configurations of timeframes, stop-loss types, and RR ratios.
    """
    
    def __init__(self, data_directory="."):
        """
        Initialize the FVG Backtester
        
        Parameters:
        -----------
        data_directory : str
            Path to directory containing CSV files
        """
        self.data_directory = Path(data_directory)
        self.years = list(range(2018, 2026))  # 2018-2025
        self.timeframes = ['1m', '5m', '15m']
        self.rr_ratios = [1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 10]
        self.stop_loss_types = ['middle', 'edge']  # middle or edge of FVG
        
        # Entry times based on timeframe
        self.entry_times = {
            '1m': time(8, 32),   # 8:32 AM
            '5m': time(8, 40),   # 8:40 AM
            '15m': time(9, 0)    # 9:00 AM
        }
        
        self.results = []
        self.all_trades = []
        
        # Cache for loaded data and FVGs
        self.data_cache = {}
        self.fvg_cache = {}
        
    def load_data(self, year, timeframe):
        """
        Load CSV data for a specific year and timeframe (with caching)
        
        Parameters:
        -----------
        year : int
            Year to load
        timeframe : str
            Timeframe ('1m', '5m', or '15m')
            
        Returns:
        --------
        pd.DataFrame
            Loaded and processed dataframe
        """
        cache_key = (year, timeframe)
        
        # Return cached data if available
        if cache_key in self.data_cache:
            return self.data_cache[cache_key]
        
        filename = f"{year} {timeframe}.csv"
        filepath = self.data_directory / filename
        
        if not filepath.exists():
            print(f"Warning: File not found: {filepath}")
            return None
        
        try:
            # Read CSV with semicolon delimiter
            df = pd.read_csv(filepath, sep=';', skiprows=1,
                           names=['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume'])
            
            # Parse datetime
            df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], 
                                          format='%d/%m/%Y %H:%M:%S')
            
            # Convert price columns to float
            for col in ['Open', 'High', 'Low', 'Close']:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            
            df['Volume'] = pd.to_numeric(df['Volume'], errors='coerce')
            
            # Sort by datetime and reset index
            df = df.sort_values('DateTime').reset_index(drop=True)
            
            # Extract date and time separately for easier filtering
            df['DateOnly'] = df['DateTime'].dt.date
            df['TimeOnly'] = df['DateTime'].dt.time
            
            print(f"Loaded {len(df)} rows from {filename}")
            
            # Cache the data
            self.data_cache[cache_key] = df
            
            return df
            
        except Exception as e:
            print(f"Error loading {filepath}: {e}")
            return None
    
    def detect_fvg_at_830(self, df):
        """
        Detect Fair Value Gaps forming at 8:30 AM
        
        A FVG is detected when:
        - Bullish FVG: high[i-2] < low[i] (gap up)
        - Bearish FVG: low[i-2] > high[i] (gap down)
        
        Parameters:
        -----------
        df : pd.DataFrame
            DataFrame with OHLC data
            
        Returns:
        --------
        list of dict
            List of detected FVGs with details
        """
        fvgs = []
        
        # Get unique dates
        dates = df['DateOnly'].unique()
        
        for date in dates:
            # Get data around 8:30 AM for this date
            day_data = df[df['DateOnly'] == date].copy()
            
            # Find the 8:30 AM candle
            candle_830_idx = day_data[day_data['TimeOnly'] == time(8, 30)].index
            
            if len(candle_830_idx) == 0:
                continue
                
            candle_830_idx = candle_830_idx[0]
            
            # Get position in the day_data dataframe
            pos_in_day = day_data.index.get_loc(candle_830_idx)
            
            # Need at least 2 previous candles
            if pos_in_day < 2:
                continue
            
            # Get the three candles: i-2, i-1, i
            idx_i = candle_830_idx
            idx_i_minus_1 = day_data.index[pos_in_day - 1]
            idx_i_minus_2 = day_data.index[pos_in_day - 2]
            
            candle_i = day_data.loc[idx_i]
            candle_i_minus_2 = day_data.loc[idx_i_minus_2]
            
            # Check for Bullish FVG: high[i-2] < low[i]
            if candle_i_minus_2['High'] < candle_i['Low']:
                fvg = {
                    'date': date,
                    'datetime_830': candle_i['DateTime'],
                    'type': 'bullish',
                    'fvg_top': candle_i['Low'],
                    'fvg_bottom': candle_i_minus_2['High'],
                    'fvg_middle': (candle_i['Low'] + candle_i_minus_2['High']) / 2,
                    'candle_830_open': candle_i['Open'],
                    'candle_830_close': candle_i['Close']
                }
                fvgs.append(fvg)
            
            # Check for Bearish FVG: low[i-2] > high[i]
            elif candle_i_minus_2['Low'] > candle_i['High']:
                fvg = {
                    'date': date,
                    'datetime_830': candle_i['DateTime'],
                    'type': 'bearish',
                    'fvg_top': candle_i_minus_2['Low'],
                    'fvg_bottom': candle_i['High'],
                    'fvg_middle': (candle_i_minus_2['Low'] + candle_i['High']) / 2,
                    'candle_830_open': candle_i['Open'],
                    'candle_830_close': candle_i['Close']
                }
                fvgs.append(fvg)
        
        return fvgs
    
    def get_entry_price(self, df, fvg, timeframe):
        """
        Get entry price based on timeframe
        
        Parameters:
        -----------
        df : pd.DataFrame
            DataFrame with OHLC data
        fvg : dict
            FVG details
        timeframe : str
            Timeframe ('1m', '5m', or '15m')
            
        Returns:
        --------
        float or None
            Entry price (open of entry candle) or None if not found
        """
        entry_time = self.entry_times[timeframe]
        date = fvg['date']
        
        # Find the entry candle
        entry_candles = df[(df['DateOnly'] == date) & (df['TimeOnly'] == entry_time)]
        
        if len(entry_candles) == 0:
            return None
        
        return entry_candles.iloc[0]['Open']
    
    def simulate_trade(self, df, fvg, entry_price, stop_loss_type, rr_ratio, timeframe):
        """
        Simulate a trade with given parameters
        
        Parameters:
        -----------
        df : pd.DataFrame
            DataFrame with OHLC data
        fvg : dict
            FVG details
        entry_price : float
            Entry price
        stop_loss_type : str
            'middle' or 'edge' of FVG
        rr_ratio : float
            Risk-to-reward ratio
        timeframe : str
            Timeframe
            
        Returns:
        --------
        dict
            Trade result with outcome and details
        """
        trade_type = fvg['type']
        
        # Calculate stop loss
        if trade_type == 'bullish':
            if stop_loss_type == 'middle':
                stop_loss = fvg['fvg_middle']
            else:  # edge
                stop_loss = fvg['fvg_bottom']
            
            # For long trades, stop should be below entry
            if stop_loss >= entry_price:
                return None  # Invalid trade setup
            
            risk = entry_price - stop_loss
            take_profit = entry_price + (risk * rr_ratio)
            
        else:  # bearish
            if stop_loss_type == 'middle':
                stop_loss = fvg['fvg_middle']
            else:  # edge
                stop_loss = fvg['fvg_top']
            
            # For short trades, stop should be above entry
            if stop_loss <= entry_price:
                return None  # Invalid trade setup
            
            risk = stop_loss - entry_price
            take_profit = entry_price - (risk * rr_ratio)
        
        # Get data from entry time onwards
        entry_time = self.entry_times[timeframe]
        date = fvg['date']
        
        entry_datetime = df[(df['DateOnly'] == date) & (df['TimeOnly'] == entry_time)]
        if len(entry_datetime) == 0:
            return None
        
        entry_datetime = entry_datetime.iloc[0]['DateTime']
        
        # Get subsequent candles for the same day
        subsequent_data = df[(df['DateTime'] > entry_datetime) & (df['DateOnly'] == date)]
        
        if len(subsequent_data) == 0:
            return {
                'outcome': 'no_data',
                'entry_price': entry_price,
                'stop_loss': stop_loss,
                'take_profit': take_profit,
                'risk': risk
            }
        
        # Check each candle for stop loss or take profit
        for idx, candle in subsequent_data.iterrows():
            if trade_type == 'bullish':
                # Check stop loss first (conservative approach)
                if candle['Low'] <= stop_loss:
                    return {
                        'outcome': 'loss',
                        'exit_price': stop_loss,
                        'entry_price': entry_price,
                        'stop_loss': stop_loss,
                        'take_profit': take_profit,
                        'risk': risk,
                        'pnl': -risk,
                        'exit_datetime': candle['DateTime']
                    }
                # Then check take profit
                if candle['High'] >= take_profit:
                    return {
                        'outcome': 'win',
                        'exit_price': take_profit,
                        'entry_price': entry_price,
                        'stop_loss': stop_loss,
                        'take_profit': take_profit,
                        'risk': risk,
                        'pnl': risk * rr_ratio,
                        'exit_datetime': candle['DateTime']
                    }
            
            else:  # bearish
                # Check stop loss first
                if candle['High'] >= stop_loss:
                    return {
                        'outcome': 'loss',
                        'exit_price': stop_loss,
                        'entry_price': entry_price,
                        'stop_loss': stop_loss,
                        'take_profit': take_profit,
                        'risk': risk,
                        'pnl': -risk,
                        'exit_datetime': candle['DateTime']
                    }
                # Then check take profit
                if candle['Low'] <= take_profit:
                    return {
                        'outcome': 'win',
                        'exit_price': take_profit,
                        'entry_price': entry_price,
                        'stop_loss': stop_loss,
                        'take_profit': take_profit,
                        'risk': risk,
                        'pnl': risk * rr_ratio,
                        'exit_datetime': candle['DateTime']
                    }
        
        # If we get here, trade didn't hit SL or TP by end of day
        return {
            'outcome': 'no_exit',
            'entry_price': entry_price,
            'stop_loss': stop_loss,
            'take_profit': take_profit,
            'risk': risk
        }
    
    def backtest_configuration(self, year, timeframe, stop_loss_type, rr_ratio):
        """
        Backtest a specific configuration
        
        Parameters:
        -----------
        year : int
            Year to test
        timeframe : str
            Timeframe
        stop_loss_type : str
            Stop loss type
        rr_ratio : float
            Risk-to-reward ratio
            
        Returns:
        --------
        dict
            Results summary
        """
        # Load data (cached)
        df = self.load_data(year, timeframe)
        if df is None or len(df) == 0:
            return None
        
        # Detect FVGs at 8:30 AM (cached)
        cache_key = (year, timeframe)
        if cache_key not in self.fvg_cache:
            fvgs = self.detect_fvg_at_830(df)
            self.fvg_cache[cache_key] = fvgs
        else:
            fvgs = self.fvg_cache[cache_key]
        
        if len(fvgs) == 0:
            return {
                'year': year,
                'timeframe': timeframe,
                'stop_loss_type': stop_loss_type,
                'rr_ratio': rr_ratio,
                'total_fvgs': 0,
                'total_trades': 0,
                'wins': 0,
                'losses': 0,
                'no_exit': 0,
                'win_rate': 0,
                'total_pnl': 0,
                'avg_win': 0,
                'avg_loss': 0,
                'profit_factor': 0
            }
        
        # Execute trades
        trades = []
        for fvg in fvgs:
            entry_price = self.get_entry_price(df, fvg, timeframe)
            if entry_price is None:
                continue
            
            trade_result = self.simulate_trade(df, fvg, entry_price, stop_loss_type, 
                                              rr_ratio, timeframe)
            if trade_result is None:
                continue
            
            trade_result['year'] = year
            trade_result['timeframe'] = timeframe
            trade_result['stop_loss_type'] = stop_loss_type
            trade_result['rr_ratio'] = rr_ratio
            trade_result['fvg_type'] = fvg['type']
            trade_result['date'] = fvg['date']
            
            trades.append(trade_result)
        
        # Calculate statistics
        wins = [t for t in trades if t['outcome'] == 'win']
        losses = [t for t in trades if t['outcome'] == 'loss']
        no_exits = [t for t in trades if t['outcome'] == 'no_exit']
        
        total_trades = len(wins) + len(losses)
        win_rate = (len(wins) / total_trades * 100) if total_trades > 0 else 0
        
        total_pnl = sum([t.get('pnl', 0) for t in trades])
        avg_win = np.mean([t.get('pnl', 0) for t in wins]) if len(wins) > 0 else 0
        avg_loss = np.mean([abs(t.get('pnl', 0)) for t in losses]) if len(losses) > 0 else 0
        
        gross_profit = sum([t.get('pnl', 0) for t in wins])
        gross_loss = sum([abs(t.get('pnl', 0)) for t in losses])
        profit_factor = (gross_profit / gross_loss) if gross_loss > 0 else 0
        
        result = {
            'year': year,
            'timeframe': timeframe,
            'stop_loss_type': stop_loss_type,
            'rr_ratio': rr_ratio,
            'total_fvgs': len(fvgs),
            'total_trades': total_trades,
            'wins': len(wins),
            'losses': len(losses),
            'no_exit': len(no_exits),
            'win_rate': win_rate,
            'total_pnl': total_pnl,
            'avg_win': avg_win,
            'avg_loss': avg_loss,
            'profit_factor': profit_factor,
            'gross_profit': gross_profit,
            'gross_loss': gross_loss
        }
        
        self.all_trades.extend(trades)
        
        return result
    
    def run_full_backtest(self):
        """
        Run backtest for all configurations
        """
        print("=" * 80)
        print("FVG BACKTESTING SYSTEM - FULL ANALYSIS")
        print("=" * 80)
        print(f"Years: {self.years}")
        print(f"Timeframes: {self.timeframes}")
        print(f"Stop Loss Types: {self.stop_loss_types}")
        print(f"RR Ratios: {self.rr_ratios}")
        print("=" * 80)
        print()
        
        total_configs = len(self.years) * len(self.timeframes) * len(self.stop_loss_types) * len(self.rr_ratios)
        current = 0
        
        for year in self.years:
            for timeframe in self.timeframes:
                for stop_loss_type in self.stop_loss_types:
                    for rr_ratio in self.rr_ratios:
                        current += 1
                        print(f"[{current}/{total_configs}] Testing: {year} | {timeframe} | SL:{stop_loss_type} | RR:{rr_ratio}", end='\r')
                        
                        result = self.backtest_configuration(year, timeframe, stop_loss_type, rr_ratio)
                        if result is not None:
                            self.results.append(result)
        
        print("\n" + "=" * 80)
        print(f"Backtest Complete! Total configurations tested: {len(self.results)}")
        print(f"Total trades executed: {len(self.all_trades)}")
        print("=" * 80)
    
    def generate_summary_tables(self):
        """
        Generate summary tables for different aggregations
        """
        if not self.results:
            print("No results to summarize!")
            return
        
        df_results = pd.DataFrame(self.results)
        
        print("\n" + "=" * 80)
        print("SUMMARY TABLES")
        print("=" * 80)
        
        # 1. Overall performance by timeframe and stop loss type
        print("\n1. OVERALL PERFORMANCE BY TIMEFRAME AND STOP LOSS TYPE (All Years Combined)")
        print("-" * 80)
        
        summary1 = df_results.groupby(['timeframe', 'stop_loss_type']).agg({
            'total_trades': 'sum',
            'wins': 'sum',
            'losses': 'sum',
            'win_rate': lambda x: (df_results.loc[x.index, 'wins'].sum() / 
                                  (df_results.loc[x.index, 'wins'].sum() + df_results.loc[x.index, 'losses'].sum()) * 100)
                                  if (df_results.loc[x.index, 'wins'].sum() + df_results.loc[x.index, 'losses'].sum()) > 0 else 0,
            'total_pnl': 'sum',
            'profit_factor': lambda x: (df_results.loc[x.index, 'gross_profit'].sum() / 
                                       df_results.loc[x.index, 'gross_loss'].sum())
                                       if df_results.loc[x.index, 'gross_loss'].sum() > 0 else 0
        }).round(2)
        
        print(tabulate(summary1, headers='keys', tablefmt='grid'))
        
        # 2. Performance by RR ratio (averaged across all configurations)
        print("\n2. PERFORMANCE BY RISK-REWARD RATIO (All Configurations)")
        print("-" * 80)
        
        summary2 = df_results.groupby('rr_ratio').agg({
            'total_trades': 'sum',
            'wins': 'sum',
            'losses': 'sum',
            'win_rate': lambda x: (df_results.loc[x.index, 'wins'].sum() / 
                                  (df_results.loc[x.index, 'wins'].sum() + df_results.loc[x.index, 'losses'].sum()) * 100)
                                  if (df_results.loc[x.index, 'wins'].sum() + df_results.loc[x.index, 'losses'].sum()) > 0 else 0,
            'total_pnl': 'sum',
            'profit_factor': lambda x: (df_results.loc[x.index, 'gross_profit'].sum() / 
                                       df_results.loc[x.index, 'gross_loss'].sum())
                                       if df_results.loc[x.index, 'gross_loss'].sum() > 0 else 0
        }).round(2)
        
        print(tabulate(summary2, headers='keys', tablefmt='grid'))
        
        # 3. Yearly performance breakdown
        print("\n3. YEARLY PERFORMANCE (All Configurations Combined)")
        print("-" * 80)
        
        summary3 = df_results.groupby('year').agg({
            'total_fvgs': 'sum',
            'total_trades': 'sum',
            'wins': 'sum',
            'losses': 'sum',
            'win_rate': lambda x: (df_results.loc[x.index, 'wins'].sum() / 
                                  (df_results.loc[x.index, 'wins'].sum() + df_results.loc[x.index, 'losses'].sum()) * 100)
                                  if (df_results.loc[x.index, 'wins'].sum() + df_results.loc[x.index, 'losses'].sum()) > 0 else 0,
            'total_pnl': 'sum',
            'profit_factor': lambda x: (df_results.loc[x.index, 'gross_profit'].sum() / 
                                       df_results.loc[x.index, 'gross_loss'].sum())
                                       if df_results.loc[x.index, 'gross_loss'].sum() > 0 else 0
        }).round(2)
        
        print(tabulate(summary3, headers='keys', tablefmt='grid'))
        
        # 4. Best performing configurations
        print("\n4. TOP 10 BEST PERFORMING CONFIGURATIONS (by Profit Factor)")
        print("-" * 80)
        
        df_valid = df_results[df_results['total_trades'] >= 10].copy()  # At least 10 trades
        df_valid = df_valid.sort_values('profit_factor', ascending=False).head(10)
        
        display_cols = ['year', 'timeframe', 'stop_loss_type', 'rr_ratio', 'total_trades', 
                       'wins', 'losses', 'win_rate', 'profit_factor']
        print(tabulate(df_valid[display_cols], headers='keys', tablefmt='grid', showindex=False))
        
        # 5. Detailed matrix: Timeframe x Stop Loss x RR Ratio
        print("\n5. DETAILED WIN RATE MATRIX")
        print("-" * 80)
        
        for timeframe in self.timeframes:
            print(f"\n{timeframe.upper()} TIMEFRAME - Win Rates (%)")
            
            tf_data = df_results[df_results['timeframe'] == timeframe]
            pivot = tf_data.pivot_table(
                values='win_rate',
                index='stop_loss_type',
                columns='rr_ratio',
                aggfunc=lambda x: (tf_data.loc[x.index, 'wins'].sum() / 
                                  (tf_data.loc[x.index, 'wins'].sum() + tf_data.loc[x.index, 'losses'].sum()) * 100)
                                  if (tf_data.loc[x.index, 'wins'].sum() + tf_data.loc[x.index, 'losses'].sum()) > 0 else 0
            ).round(2)
            
            print(tabulate(pivot, headers='keys', tablefmt='grid'))
    
    def generate_visualizations(self, output_dir='results'):
        """
        Generate visualizations
        
        Parameters:
        -----------
        output_dir : str
            Directory to save plots
        """
        if not self.results:
            print("No results to visualize!")
            return
        
        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        df_results = pd.DataFrame(self.results)
        
        print(f"\nGenerating visualizations in '{output_dir}/' directory...")
        
        # 1. Win Rate by RR Ratio
        plt.figure(figsize=(14, 8))
        
        for timeframe in self.timeframes:
            for sl_type in self.stop_loss_types:
                data = df_results[(df_results['timeframe'] == timeframe) & 
                                 (df_results['stop_loss_type'] == sl_type)]
                
                summary = data.groupby('rr_ratio').apply(
                    lambda x: (x['wins'].sum() / (x['wins'].sum() + x['losses'].sum()) * 100)
                    if (x['wins'].sum() + x['losses'].sum()) > 0 else 0
                ).reset_index()
                summary.columns = ['rr_ratio', 'win_rate']
                
                label = f"{timeframe} - {sl_type}"
                plt.plot(summary['rr_ratio'], summary['win_rate'], marker='o', label=label, linewidth=2)
        
        plt.xlabel('Risk-Reward Ratio', fontsize=12)
        plt.ylabel('Win Rate (%)', fontsize=12)
        plt.title('Win Rate vs Risk-Reward Ratio (All Configurations)', fontsize=14, fontweight='bold')
        plt.legend(loc='best', fontsize=10)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(output_path / 'win_rate_by_rr_ratio.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 2. Profit Factor by Configuration
        plt.figure(figsize=(14, 8))
        
        for timeframe in self.timeframes:
            for sl_type in self.stop_loss_types:
                data = df_results[(df_results['timeframe'] == timeframe) & 
                                 (df_results['stop_loss_type'] == sl_type)]
                
                summary = data.groupby('rr_ratio').apply(
                    lambda x: (x['gross_profit'].sum() / x['gross_loss'].sum())
                    if x['gross_loss'].sum() > 0 else 0
                ).reset_index()
                summary.columns = ['rr_ratio', 'profit_factor']
                
                label = f"{timeframe} - {sl_type}"
                plt.plot(summary['rr_ratio'], summary['profit_factor'], marker='s', label=label, linewidth=2)
        
        plt.axhline(y=1.0, color='r', linestyle='--', label='Break-even', linewidth=2)
        plt.xlabel('Risk-Reward Ratio', fontsize=12)
        plt.ylabel('Profit Factor', fontsize=12)
        plt.title('Profit Factor vs Risk-Reward Ratio (All Configurations)', fontsize=14, fontweight='bold')
        plt.legend(loc='best', fontsize=10)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(output_path / 'profit_factor_by_rr_ratio.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 3. Heatmap of Win Rates
        fig, axes = plt.subplots(1, 3, figsize=(20, 6))
        
        for idx, timeframe in enumerate(self.timeframes):
            tf_data = df_results[df_results['timeframe'] == timeframe]
            
            pivot = tf_data.pivot_table(
                values='wins',
                index='stop_loss_type',
                columns='rr_ratio',
                aggfunc=lambda x: (tf_data.loc[x.index, 'wins'].sum() / 
                                  (tf_data.loc[x.index, 'wins'].sum() + tf_data.loc[x.index, 'losses'].sum()) * 100)
                                  if (tf_data.loc[x.index, 'wins'].sum() + tf_data.loc[x.index, 'losses'].sum()) > 0 else 0
            )
            
            sns.heatmap(pivot, annot=True, fmt='.1f', cmap='RdYlGn', center=50,
                       ax=axes[idx], cbar_kws={'label': 'Win Rate (%)'})
            axes[idx].set_title(f'{timeframe.upper()} Timeframe', fontsize=12, fontweight='bold')
            axes[idx].set_xlabel('Risk-Reward Ratio', fontsize=10)
            axes[idx].set_ylabel('Stop Loss Type', fontsize=10)
        
        plt.tight_layout()
        plt.savefig(output_path / 'win_rate_heatmaps.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 4. Total Trades by Year
        plt.figure(figsize=(12, 6))
        
        yearly_trades = df_results.groupby('year')['total_trades'].sum()
        plt.bar(yearly_trades.index, yearly_trades.values, color='steelblue', alpha=0.7, edgecolor='black')
        plt.xlabel('Year', fontsize=12)
        plt.ylabel('Total Trades', fontsize=12)
        plt.title('Total Trades Executed by Year', fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        plt.savefig(output_path / 'trades_by_year.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 5. Comparison of Stop Loss Types
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        
        metrics = ['win_rate', 'profit_factor', 'total_trades', 'total_pnl']
        titles = ['Win Rate (%)', 'Profit Factor', 'Total Trades', 'Total P&L']
        
        for idx, (metric, title) in enumerate(zip(metrics, titles)):
            ax = axes[idx // 2, idx % 2]
            
            comparison = df_results.groupby(['timeframe', 'stop_loss_type']).agg({
                'wins': 'sum',
                'losses': 'sum',
                'gross_profit': 'sum',
                'gross_loss': 'sum',
                'total_trades': 'sum',
                'total_pnl': 'sum'
            })
            
            if metric == 'win_rate':
                comparison[metric] = (comparison['wins'] / (comparison['wins'] + comparison['losses']) * 100)
            elif metric == 'profit_factor':
                comparison[metric] = comparison['gross_profit'] / comparison['gross_loss']
            
            comparison = comparison.reset_index()
            
            pivot = comparison.pivot(index='timeframe', columns='stop_loss_type', values=metric)
            pivot.plot(kind='bar', ax=ax, width=0.7, edgecolor='black')
            ax.set_title(title, fontsize=12, fontweight='bold')
            ax.set_xlabel('Timeframe', fontsize=10)
            ax.set_ylabel(title, fontsize=10)
            ax.legend(title='Stop Loss Type')
            ax.grid(True, alpha=0.3, axis='y')
            
            if metric == 'profit_factor':
                ax.axhline(y=1.0, color='r', linestyle='--', linewidth=2, alpha=0.7)
        
        plt.tight_layout()
        plt.savefig(output_path / 'stop_loss_comparison.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✓ Generated 5 visualization files in '{output_dir}/' directory")
    
    def export_results(self, output_dir='results'):
        """
        Export results to CSV files
        
        Parameters:
        -----------
        output_dir : str
            Directory to save CSV files
        """
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # Export full results
        if self.results:
            df_results = pd.DataFrame(self.results)
            results_file = output_path / 'backtest_results_summary.csv'
            df_results.to_csv(results_file, index=False)
            print(f"✓ Exported results summary to: {results_file}")
        
        # Export all trades
        if self.all_trades:
            df_trades = pd.DataFrame(self.all_trades)
            trades_file = output_path / 'all_trades_detailed.csv'
            df_trades.to_csv(trades_file, index=False)
            print(f"✓ Exported detailed trades to: {trades_file}")
        
        print(f"\nAll results exported to '{output_dir}/' directory")


def main():
    """
    Main execution function
    """
    print("\n" + "=" * 80)
    print(" FVG TRADING STRATEGY BACKTESTING SYSTEM ".center(80, "="))
    print("=" * 80)
    print("\nInitializing backtester...")
    
    # Initialize backtester
    backtester = FVGBacktester(data_directory=".")
    
    # Run full backtest
    print("\nStarting full backtest analysis...")
    backtester.run_full_backtest()
    
    # Generate summary tables
    backtester.generate_summary_tables()
    
    # Generate visualizations
    backtester.generate_visualizations()
    
    # Export results
    backtester.export_results()
    
    print("\n" + "=" * 80)
    print(" BACKTEST COMPLETE ".center(80, "="))
    print("=" * 80)
    print("\nResults have been saved to the 'results/' directory:")
    print("  - backtest_results_summary.csv (summary statistics)")
    print("  - all_trades_detailed.csv (individual trade details)")
    print("  - Various PNG visualization files")
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()

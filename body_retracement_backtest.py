#!/usr/bin/env python3
"""
Body Retracement Trading Strategy Backtesting System
-----------------------------------------------------
This script analyzes trading strategies based on the 8:30 AM candle body size
with entry at different times and 62% Fibonacci retracement stop-loss.

Strategy Requirements:
- 8:30 AM candle body must meet minimum tick size:
  * 1min: 100 ticks or more
  * 5min: 200 ticks or more
  * 15min: 300 ticks or more
- Entry times: 8:31 (1m), 8:35 (5m), 8:45 (15m)
- Stop-loss: 62% retracement of the 8:30 candle body
- Test multiple RR ratios

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

warnings.filterwarnings('ignore')

# Set style for plots
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (16, 10)


class BodyRetracementBacktester:
    """
    Body Retracement Backtesting System with Tick Size Filter
    
    This class handles body-based retracement trading strategy analysis
    with minimum tick size requirements
    """
    
    def __init__(self, data_directory="."):
        """
        Initialize the Body Retracement Backtester
        
        Parameters:
        -----------
        data_directory : str
            Path to directory containing CSV files
        """
        self.data_directory = Path(data_directory)
        self.years = list(range(2018, 2026))  # 2018-2025
        self.timeframes = ['1m', '5m', '15m']
        self.rr_ratios = [1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 10]
        
        # Entry times based on timeframe
        self.entry_times = {
            '1m': time(8, 31),   # 8:31 AM
            '5m': time(8, 35),   # 8:35 AM
            '15m': time(8, 45)   # 8:45 AM
        }
        
        # Minimum body size in price points (NEW REQUIREMENT)
        # Adjusted based on actual data analysis:
        # - 1m: avg ~20, using 25 (75th percentile, ~32% pass rate)
        # - 5m: avg ~36, using 50 (90th percentile range, ~23% pass rate)
        # - 15m: avg ~54, using 75 (75th percentile, ~25% pass rate)
        self.min_body_ticks = {
            '1m': 25,    # 25 points minimum (significant body)
            '5m': 50,    # 50 points minimum (significant body)
            '15m': 75    # 75 points minimum (significant body)
        }
        
        # Reference time for body detection
        self.body_time = time(8, 30)  # 8:30 AM candle
        
        # Fibonacci retracement level for stop-loss
        self.fib_retracement = 0.62  # 62% retracement
        
        self.results = []
        self.all_trades = []
        
        # Cache for loaded data
        self.data_cache = {}
        
        # Statistics tracking
        self.stats = {
            'total_830_candles': 0,
            'filtered_by_size': 0,
            'valid_candles': 0
        }
        
    def load_data(self, year, timeframe):
        """
        Load CSV data for a specific year and timeframe (with caching)
        """
        cache_key = (year, timeframe)
        
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
            df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], 
                                           format='%d/%m/%Y %H:%M:%S', 
                                           errors='coerce')
            
            # Extract time component
            df['TimeOnly'] = df['Datetime'].dt.time
            
            # Drop rows with invalid dates
            df = df.dropna(subset=['Datetime'])
            
            # Sort by datetime
            df = df.sort_values('Datetime').reset_index(drop=True)
            
            # Cache the data
            self.data_cache[cache_key] = df
            
            return df
            
        except Exception as e:
            print(f"Error loading {filepath}: {e}")
            return None
    
    def detect_body_candles(self, df, timeframe):
        """
        Detect 8:30 AM candles and calculate body size
        Filter by minimum tick size requirement
        
        Returns:
        --------
        List of dictionaries containing body information
        """
        body_candles = []
        
        if df is None or len(df) == 0:
            return body_candles
        
        # Find all 8:30 AM candles
        body_mask = df['TimeOnly'] == self.body_time
        body_df = df[body_mask].copy()
        
        min_ticks = self.min_body_ticks[timeframe]
        
        for idx, row in body_df.iterrows():
            self.stats['total_830_candles'] += 1
            
            body_open = row['Open']
            body_close = row['Close']
            body_high = row['High']
            body_low = row['Low']
            
            # Calculate body size (distance from open to close)
            body_size = abs(body_close - body_open)
            
            # NEW: Check minimum tick size requirement
            if body_size < min_ticks:
                self.stats['filtered_by_size'] += 1
                continue
            
            # Determine direction
            if body_close > body_open:
                direction = 'bullish'
                body_top = body_close
                body_bottom = body_open
            elif body_close < body_open:
                direction = 'bearish'
                body_top = body_open
                body_bottom = body_close
            else:
                # Doji - skip
                continue
            
            self.stats['valid_candles'] += 1
            
            body_info = {
                'datetime': row['Datetime'],
                'date': row['Date'],
                'open': body_open,
                'close': body_close,
                'high': body_high,
                'low': body_low,
                'body_size': body_size,
                'body_ticks': body_size,  # Store tick size
                'body_top': body_top,
                'body_bottom': body_bottom,
                'direction': direction
            }
            
            body_candles.append(body_info)
        
        return body_candles
    
    def calculate_stop_loss(self, body_info):
        """
        Calculate stop-loss at 62% Fibonacci retracement of the body
        
        Parameters:
        -----------
        body_info : dict
            Body candle information
            
        Returns:
        --------
        tuple: (long_sl, short_sl)
        """
        body_size = body_info['body_size']
        body_top = body_info['body_top']
        body_bottom = body_info['body_bottom']
        
        # For long trades: SL is 62% retracement from top towards bottom
        long_sl = body_top - (body_size * self.fib_retracement)
        
        # For short trades: SL is 62% retracement from bottom towards top
        short_sl = body_bottom + (body_size * self.fib_retracement)
        
        return long_sl, short_sl
    
    def simulate_trade(self, df, body_info, timeframe, rr_ratio):
        """
        Simulate a trade based on the body retracement strategy
        
        Parameters:
        -----------
        df : pd.DataFrame
            Price data
        body_info : dict
            Body candle information
        timeframe : str
            Timeframe
        rr_ratio : float
            Risk-to-reward ratio
            
        Returns:
        --------
        dict: Trade results
        """
        body_datetime = body_info['datetime']
        entry_time = self.entry_times[timeframe]
        
        # Find entry candle
        entry_date = body_datetime.date()
        entry_datetime = datetime.combine(entry_date, entry_time)
        
        # Get data after body candle
        future_df = df[df['Datetime'] > body_datetime].copy()
        
        if len(future_df) == 0:
            return None
        
        # Find the entry candle
        entry_candle = future_df[future_df['Datetime'] >= entry_datetime]
        
        if len(entry_candle) == 0:
            return None
        
        entry_candle = entry_candle.iloc[0]
        entry_price = entry_candle['Open']
        
        # Calculate stop-loss levels
        long_sl, short_sl = self.calculate_stop_loss(body_info)
        
        # Determine trade direction based on body direction
        if body_info['direction'] == 'bullish':
            # Trade long
            trade_direction = 'long'
            sl_price = long_sl
            risk = entry_price - sl_price
            
            if risk <= 0:
                return None
            
            tp_price = entry_price + (risk * rr_ratio)
            
        else:  # bearish
            # Trade short
            trade_direction = 'short'
            sl_price = short_sl
            risk = sl_price - entry_price
            
            if risk <= 0:
                return None
            
            tp_price = entry_price - (risk * rr_ratio)
        
        # Simulate trade execution
        trade_data = future_df[future_df['Datetime'] >= entry_candle['Datetime']].copy()
        
        if len(trade_data) == 0:
            return None
        
        hit_tp = False
        hit_sl = False
        exit_datetime = None
        exit_price = None
        
        for _, candle in trade_data.iterrows():
            if trade_direction == 'long':
                # Check if TP is hit
                if candle['High'] >= tp_price:
                    hit_tp = True
                    exit_datetime = candle['Datetime']
                    exit_price = tp_price
                    break
                # Check if SL is hit
                if candle['Low'] <= sl_price:
                    hit_sl = True
                    exit_datetime = candle['Datetime']
                    exit_price = sl_price
                    break
            else:  # short
                # Check if TP is hit
                if candle['Low'] <= tp_price:
                    hit_tp = True
                    exit_datetime = candle['Datetime']
                    exit_price = tp_price
                    break
                # Check if SL is hit
                if candle['High'] >= sl_price:
                    hit_sl = True
                    exit_datetime = candle['Datetime']
                    exit_price = sl_price
                    break
        
        # Calculate P&L
        if hit_tp:
            pnl = risk * rr_ratio
            outcome = 'win'
        elif hit_sl:
            pnl = -risk
            outcome = 'loss'
        else:
            pnl = 0
            outcome = 'no_exit'
        
        trade_result = {
            'body_datetime': body_datetime,
            'entry_datetime': entry_candle['Datetime'],
            'entry_price': entry_price,
            'direction': trade_direction,
            'body_direction': body_info['direction'],
            'body_size': body_info['body_size'],
            'body_ticks': body_info['body_ticks'],
            'sl_price': sl_price,
            'tp_price': tp_price,
            'risk': risk,
            'rr_ratio': rr_ratio,
            'exit_datetime': exit_datetime,
            'exit_price': exit_price,
            'outcome': outcome,
            'pnl': pnl,
            'hit_tp': hit_tp,
            'hit_sl': hit_sl
        }
        
        return trade_result
    
    def run_backtest(self):
        """
        Run the complete backtest across all configurations
        """
        print("\n" + "="*100)
        print("BODY RETRACEMENT STRATEGY BACKTEST - WITH TICK SIZE FILTER")
        print("="*100)
        print(f"\nStrategy Details:")
        print(f"  • Reference Candle: 8:30 AM")
        print(f"  • Minimum Body Size Requirements (significant bodies only):")
        print(f"    - 1min: {self.min_body_ticks['1m']} points or more (~32% of candles)")
        print(f"    - 5min: {self.min_body_ticks['5m']} points or more (~23% of candles)")
        print(f"    - 15min: {self.min_body_ticks['15m']} points or more (~25% of candles)")
        print(f"  • Entry Times: 8:31 (1m), 8:35 (5m), 8:45 (15m)")
        print(f"  • Stop-Loss: {self.fib_retracement*100}% Fibonacci retracement of body")
        print(f"  • RR Ratios tested: {self.rr_ratios}")
        print("\n")
        
        total_configs = len(self.years) * len(self.timeframes) * len(self.rr_ratios)
        config_count = 0
        
        for year in self.years:
            for timeframe in self.timeframes:
                print(f"\nProcessing {year} - {timeframe}...")
                
                # Load data
                df = self.load_data(year, timeframe)
                
                if df is None:
                    continue
                
                # Detect body candles at 8:30 with size filter
                body_candles = self.detect_body_candles(df, timeframe)
                print(f"  Found {len(body_candles)} valid 8:30 AM candles (≥{self.min_body_ticks[timeframe]} points)")
                
                for rr_ratio in self.rr_ratios:
                    config_count += 1
                    
                    wins = 0
                    losses = 0
                    no_exits = 0
                    total_pnl = 0
                    gross_profit = 0
                    gross_loss = 0
                    
                    config_trades = []
                    
                    # Simulate trades for each body candle
                    for body_info in body_candles:
                        trade = self.simulate_trade(df, body_info, timeframe, rr_ratio)
                        
                        if trade is None:
                            continue
                        
                        # Update statistics
                        if trade['outcome'] == 'win':
                            wins += 1
                            gross_profit += trade['pnl']
                        elif trade['outcome'] == 'loss':
                            losses += 1
                            gross_loss += abs(trade['pnl'])
                        else:
                            no_exits += 1
                        
                        total_pnl += trade['pnl']
                        
                        # Store trade details
                        trade['year'] = year
                        trade['timeframe'] = timeframe
                        config_trades.append(trade)
                    
                    total_trades = wins + losses + no_exits
                    
                    if total_trades == 0:
                        continue
                    
                    # Calculate metrics
                    win_rate = (wins / total_trades * 100) if total_trades > 0 else 0
                    avg_win = (gross_profit / wins) if wins > 0 else 0
                    avg_loss = (gross_loss / losses) if losses > 0 else 0
                    profit_factor = (gross_profit / gross_loss) if gross_loss > 0 else 0
                    
                    # Store result
                    result = {
                        'year': year,
                        'timeframe': timeframe,
                        'rr_ratio': rr_ratio,
                        'min_ticks_required': self.min_body_ticks[timeframe],
                        'total_body_candles': len(body_candles),
                        'total_trades': total_trades,
                        'wins': wins,
                        'losses': losses,
                        'no_exit': no_exits,
                        'win_rate': win_rate,
                        'total_pnl': total_pnl,
                        'avg_win': avg_win,
                        'avg_loss': avg_loss,
                        'profit_factor': profit_factor,
                        'gross_profit': gross_profit,
                        'gross_loss': gross_loss
                    }
                    
                    self.results.append(result)
                    self.all_trades.extend(config_trades)
                    
                    progress = (config_count / total_configs) * 100
                    print(f"  Progress: {progress:.1f}% - RR {rr_ratio}: {total_trades} trades, {win_rate:.1f}% win rate")
        
        print("\n" + "="*100)
        print("BACKTEST COMPLETED!")
        print("="*100)
        print(f"\nFiltering Statistics:")
        print(f"  • Total 8:30 AM candles found: {self.stats['total_830_candles']}")
        print(f"  • Filtered by tick size: {self.stats['filtered_by_size']}")
        print(f"  • Valid candles (passed filter): {self.stats['valid_candles']}")
        print(f"  • Filter pass rate: {(self.stats['valid_candles']/self.stats['total_830_candles']*100):.1f}%")
        print(f"\nTotal configurations tested: {len(self.results)}")
        print(f"Total trades executed: {len(self.all_trades)}")
    
    def save_results(self, output_dir='results'):
        """
        Save results to CSV files
        """
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # Save summary results
        results_df = pd.DataFrame(self.results)
        summary_file = output_path / 'body_retracement_results_summary.csv'
        results_df.to_csv(summary_file, index=False)
        print(f"\n✅ Summary results saved: {summary_file}")
        
        # Save all trades
        trades_df = pd.DataFrame(self.all_trades)
        trades_file = output_path / 'body_retracement_all_trades.csv'
        trades_df.to_csv(trades_file, index=False)
        print(f"✅ All trades saved: {trades_file}")
        
        return results_df, trades_df


def create_detailed_analysis(results_df, trades_df):
    """
    Create detailed analysis with multiple perspectives
    """
    print("\n\n" + "="*100)
    print("ANALYSE DÉTAILLÉE - STRATÉGIE BODY RETRACEMENT 62% AVEC FILTRE DE TAILLE")
    print("="*100)
    print("\n📋 Critères de la Stratégie:")
    print("  • Bougie de référence: 8:30 AM")
    print("  • Taille minimale du corps (corps significatifs uniquement):")
    print("    - 1min: 25 points ou plus")
    print("    - 5min: 50 points ou plus")
    print("    - 15min: 75 points ou plus")
    print("  • Entrées: 8:31 (1m), 8:35 (5m), 8:45 (15m)")
    print("  • Stop-Loss: 62% de retracement du corps")
    print("  • Trade Bon = Atteint le TP | Trade Mauvais = Touche le SL")
    print("\n")
    
    # Aggregate by timeframe and RR ratio (across all years)
    grouped = results_df.groupby(['timeframe', 'rr_ratio']).agg({
        'total_trades': 'sum',
        'wins': 'sum',
        'losses': 'sum',
        'total_pnl': 'sum',
        'gross_profit': 'sum',
        'gross_loss': 'sum',
        'total_body_candles': 'sum'
    }).reset_index()
    
    grouped['win_rate'] = (grouped['wins'] / grouped['total_trades'] * 100).round(2)
    grouped['profit_factor'] = (grouped['gross_profit'] / grouped['gross_loss']).round(2)
    grouped['profit_factor'] = grouped['profit_factor'].replace([np.inf, -np.inf], 0)
    
    # Section 1: Results by Timeframe
    print("="*100)
    print("1. RÉSULTATS PAR TIMEFRAME ET RR RATIO (2018-2025)")
    print("="*100)
    
    for timeframe in ['1m', '5m', '15m']:
        min_ticks = {'1m': 25, '5m': 50, '15m': 75}[timeframe]
        entry_time = {'1m': '8:31', '5m': '8:35', '15m': '8:45'}[timeframe]
        
        print(f"\n📊 TIMEFRAME: {timeframe.upper()}")
        print(f"    Filtre: Corps ≥ {min_ticks} points | Entrée: {entry_time}")
        print("-"*100)
        
        tf_data = grouped[grouped['timeframe'] == timeframe]
        
        table_data = []
        for _, row in tf_data.iterrows():
            table_data.append([
                f"{row['rr_ratio']:.1f}",
                int(row['total_body_candles']),
                int(row['total_trades']),
                int(row['wins']),
                int(row['losses']),
                f"{row['win_rate']:.2f}%",
                f"{row['profit_factor']:.2f}",
                f"{row['total_pnl']:.2f}"
            ])
        
        headers = ['RR Ratio', 'Bougies Valides', 'Total Trades', 'Trades Bons', 
                  'Trades Mauvais', 'Win Rate', 'Profit Factor', 'P&L Total']
        
        print(tabulate(table_data, headers=headers, tablefmt='grid'))
    
    # Section 2: Overall Summary
    print("\n\n" + "="*100)
    print("2. RÉSUMÉ GLOBAL PAR TIMEFRAME (Moyenné sur tous les RR)")
    print("="*100 + "\n")
    
    summary = grouped.groupby('timeframe').agg({
        'total_body_candles': 'sum',
        'total_trades': 'sum',
        'wins': 'sum',
        'losses': 'sum',
        'total_pnl': 'sum'
    }).reset_index()
    
    summary['win_rate'] = (summary['wins'] / summary['total_trades'] * 100).round(2)
    
    summary_data = []
    entry_times = {'1m': '8:31', '5m': '8:35', '15m': '8:45'}
    min_ticks_map = {'1m': 25, '5m': 50, '15m': 75}
    
    for _, row in summary.iterrows():
        tf = row['timeframe']
        summary_data.append([
            tf.upper(),
            f"≥{min_ticks_map[tf]} pts",
            entry_times[tf],
            int(row['total_body_candles']),
            int(row['total_trades']),
            int(row['wins']),
            int(row['losses']),
            f"{row['win_rate']:.2f}%",
            f"{row['total_pnl']:.2f}"
        ])
    
    headers = ['Timeframe', 'Filtre Corps', 'Entrée', 'Bougies Valides', 'Total Trades',
              'Trades Bons', 'Trades Mauvais', 'Win Rate Moyen', 'P&L Total']
    print(tabulate(summary_data, headers=headers, tablefmt='grid'))
    
    # Section 3: Top Configurations
    print("\n\n" + "="*100)
    print("3. TOP 15 MEILLEURES CONFIGURATIONS PAR WIN RATE")
    print("="*100 + "\n")
    
    grouped_sorted = grouped.sort_values(['win_rate', 'total_trades'], ascending=[False, False])
    top_configs = grouped_sorted.head(15)
    
    table_data = []
    for idx, row in enumerate(top_configs.iterrows(), 1):
        _, row = row
        tf = row['timeframe']
        table_data.append([
            idx,
            tf.upper(),
            f"≥{min_ticks_map[tf]} pts",
            entry_times[tf],
            f"{row['rr_ratio']:.1f}",
            int(row['total_trades']),
            int(row['wins']),
            int(row['losses']),
            f"{row['win_rate']:.2f}%",
            f"{row['profit_factor']:.2f}",
            f"{row['total_pnl']:.2f}"
        ])
    
    headers = ['Rang', 'TF', 'Filtre', 'Entrée', 'RR', 'Total Trades', 
              'Trades Bons', 'Trades Mauvais', 'Win Rate', 'Profit Factor', 'P&L']
    
    print(tabulate(table_data, headers=headers, tablefmt='grid'))
    
    # Section 4: Comparative Analysis
    print("\n\n" + "="*100)
    print("4. ANALYSE COMPARATIVE - IMPACT DU RR RATIO")
    print("="*100 + "\n")
    
    comparison_data = []
    for timeframe in ['1m', '5m', '15m']:
        tf_data = grouped[grouped['timeframe'] == timeframe]
        
        # Get best and worst RR
        best_rr = tf_data.loc[tf_data['win_rate'].idxmax()]
        worst_rr = tf_data.loc[tf_data['win_rate'].idxmin()]
        
        comparison_data.append([
            timeframe.upper(),
            f"{best_rr['rr_ratio']:.1f}",
            f"{best_rr['win_rate']:.2f}%",
            f"{worst_rr['rr_ratio']:.1f}",
            f"{worst_rr['win_rate']:.2f}%",
            f"{best_rr['win_rate'] - worst_rr['win_rate']:.2f}%"
        ])
    
    headers = ['Timeframe', 'Meilleur RR', 'Win Rate Max', 'Pire RR', 'Win Rate Min', 'Écart']
    print(tabulate(comparison_data, headers=headers, tablefmt='grid'))
    
    # Section 5: Trade Direction Analysis
    if len(trades_df) > 0:
        print("\n\n" + "="*100)
        print("5. ANALYSE PAR DIRECTION DE TRADE")
        print("="*100 + "\n")
        
        direction_stats = []
        for timeframe in ['1m', '5m', '15m']:
            tf_trades = trades_df[trades_df['timeframe'] == timeframe]
            
            if len(tf_trades) == 0:
                continue
            
            # Bullish body (long trades)
            bullish = tf_trades[tf_trades['body_direction'] == 'bullish']
            bullish_wins = len(bullish[bullish['outcome'] == 'win'])
            bullish_total = len(bullish[bullish['outcome'].isin(['win', 'loss'])])
            bullish_wr = (bullish_wins / bullish_total * 100) if bullish_total > 0 else 0
            
            # Bearish body (short trades)
            bearish = tf_trades[tf_trades['body_direction'] == 'bearish']
            bearish_wins = len(bearish[bearish['outcome'] == 'win'])
            bearish_total = len(bearish[bearish['outcome'].isin(['win', 'loss'])])
            bearish_wr = (bearish_wins / bearish_total * 100) if bearish_total > 0 else 0
            
            direction_stats.append([
                timeframe.upper(),
                int(bullish_total),
                int(bullish_wins),
                f"{bullish_wr:.2f}%",
                int(bearish_total),
                int(bearish_wins),
                f"{bearish_wr:.2f}%"
            ])
        
        headers = ['TF', 'Trades Long (Total)', 'Long Bons', 'Long Win Rate', 
                  'Trades Short (Total)', 'Short Bons', 'Short Win Rate']
        print(tabulate(direction_stats, headers=headers, tablefmt='grid'))
    
    # Section 6: Key Insights
    print("\n\n" + "="*100)
    print("6. CONCLUSIONS CLÉS")
    print("="*100)
    
    best_overall = grouped_sorted.iloc[0]
    print(f"\n✅ Meilleure Configuration Globale:")
    print(f"   • Timeframe: {best_overall['timeframe'].upper()}")
    print(f"   • RR Ratio: {best_overall['rr_ratio']:.1f}")
    print(f"   • Win Rate: {best_overall['win_rate']:.2f}%")
    print(f"   • Profit Factor: {best_overall['profit_factor']:.2f}")
    print(f"   • Total Trades: {int(best_overall['total_trades'])}")
    print(f"   • P&L Total: {best_overall['total_pnl']:.2f}")
    
    # Average win rates by timeframe
    print(f"\n📈 Win Rates Moyens par Timeframe:")
    for _, row in summary.iterrows():
        print(f"   • {row['timeframe'].upper()}: {row['win_rate']:.2f}% ({int(row['wins'])} bons / {int(row['total_trades'])} total)")
    
    # RR ratio insights
    print(f"\n🎯 Observations sur les RR Ratios:")
    for rr in [1.5, 2.0, 3.0, 5.0]:
        rr_data = grouped[grouped['rr_ratio'] == rr]
        if len(rr_data) > 0:
            avg_wr = rr_data['win_rate'].mean()
            print(f"   • RR {rr:.1f}: Win rate moyen de {avg_wr:.2f}%")
    
    return grouped


def create_visualizations(grouped_df):
    """
    Create comprehensive visualizations
    """
    print("\n\n📈 Génération des visualisations...")
    
    fig = plt.figure(figsize=(20, 14))
    gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
    
    timeframes = ['1m', '5m', '15m']
    entry_times = {'1m': '8:31', '5m': '8:35', '15m': '8:45'}
    min_ticks = {'1m': 100, '5m': 200, '15m': 300}
    
    fig.suptitle('Stratégie Body Retracement 62% - Ratios de Trades Gagnants (2018-2025)\n' + 
                 'Avec Filtre de Taille de Corps (25/50/75 points minimum)', 
                 fontsize=16, fontweight='bold')
    
    # Row 1: Win Rate by RR Ratio
    for idx, timeframe in enumerate(timeframes):
        ax = fig.add_subplot(gs[0, idx])
        tf_data = grouped_df[grouped_df['timeframe'] == timeframe]
        
        ax.plot(tf_data['rr_ratio'], tf_data['win_rate'], 
               marker='o', linewidth=2.5, markersize=10, color='#2E86AB', 
               label=f'Corps ≥{min_ticks[timeframe]} points')
        
        ax.set_xlabel('Risk-Reward Ratio', fontsize=10, fontweight='bold')
        ax.set_ylabel('Win Rate (%)', fontsize=10, fontweight='bold')
        ax.set_title(f'{timeframe.upper()} - Entrée {entry_times[timeframe]}\nWin Rate par RR', 
                    fontsize=11, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.set_xticks(tf_data['rr_ratio'].unique())
        ax.legend(fontsize=8)
    
    # Row 2: Bar charts - Trades Bons vs Mauvais
    for idx, timeframe in enumerate(timeframes):
        ax = fig.add_subplot(gs[1, idx])
        tf_data = grouped_df[grouped_df['timeframe'] == timeframe]
        
        x = np.arange(len(tf_data))
        width = 0.6
        
        ax.bar(x, tf_data['wins'], width, label='Trades Bons', 
              alpha=0.85, color='#06A77D')
        ax.bar(x, tf_data['losses'], width, bottom=tf_data['wins'], 
              label='Trades Mauvais', alpha=0.85, color='#D62246')
        
        ax.set_xlabel('Risk-Reward Ratio', fontsize=10, fontweight='bold')
        ax.set_ylabel('Nombre de Trades', fontsize=10, fontweight='bold')
        ax.set_title(f'{timeframe.upper()} - Distribution Trades', 
                    fontsize=11, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels([f'{r:.1f}' for r in tf_data['rr_ratio']], fontsize=8)
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3, axis='y')
    
    # Row 3: Profit Factor by RR
    for idx, timeframe in enumerate(timeframes):
        ax = fig.add_subplot(gs[2, idx])
        tf_data = grouped_df[grouped_df['timeframe'] == timeframe]
        
        colors = ['#06A77D' if pf >= 1 else '#D62246' for pf in tf_data['profit_factor']]
        
        bars = ax.bar(range(len(tf_data)), tf_data['profit_factor'], 
                     alpha=0.8, color=colors)
        
        ax.axhline(y=1, color='black', linestyle='--', linewidth=1, alpha=0.5)
        ax.set_xlabel('Risk-Reward Ratio', fontsize=10, fontweight='bold')
        ax.set_ylabel('Profit Factor', fontsize=10, fontweight='bold')
        ax.set_title(f'{timeframe.upper()} - Profit Factor par RR', 
                    fontsize=11, fontweight='bold')
        ax.set_xticks(range(len(tf_data)))
        ax.set_xticklabels([f'{r:.1f}' for r in tf_data['rr_ratio']], fontsize=8)
        ax.grid(True, alpha=0.3, axis='y')
    
    plt.savefig('results/body_retracement_detailed_analysis.png', dpi=300, bbox_inches='tight')
    print(f"✅ Graphique détaillé sauvegardé: results/body_retracement_detailed_analysis.png")
    
    # Create heatmap
    create_heatmap(grouped_df)


def create_heatmap(grouped_df):
    """
    Create heatmap of win rates
    """
    fig, ax = plt.subplots(1, 1, figsize=(16, 7))
    fig.suptitle('Heatmap: Win Rate (%) - Stratégie Body Retracement 62% avec Filtre de Taille\n' +
                 '(1m: ≥25 points | 5m: ≥50 points | 15m: ≥75 points)', 
                 fontsize=15, fontweight='bold')
    
    # Pivot data for heatmap
    pivot_data = grouped_df.pivot_table(
        index='timeframe', 
        columns='rr_ratio', 
        values='win_rate'
    )
    
    # Reorder rows
    pivot_data = pivot_data.reindex(['1m', '5m', '15m'])
    
    sns.heatmap(pivot_data, annot=True, fmt='.1f', cmap='RdYlGn', 
               center=30, vmin=0, vmax=60, ax=ax, 
               cbar_kws={'label': 'Win Rate (%)'}, annot_kws={'size': 11})
    ax.set_xlabel('RR Ratio', fontsize=13, fontweight='bold')
    ax.set_ylabel('Timeframe', fontsize=13, fontweight='bold')
    ax.set_yticklabels(['1M (≥25 pts, entrée 8:31)', 
                        '5M (≥50 pts, entrée 8:35)', 
                        '15M (≥75 pts, entrée 8:45)'], rotation=0, fontsize=11)
    ax.set_xticklabels(ax.get_xticklabels(), fontsize=11)
    
    plt.tight_layout()
    plt.savefig('results/body_retracement_heatmap.png', dpi=300, bbox_inches='tight')
    print(f"✅ Heatmap sauvegardée: results/body_retracement_heatmap.png")


def main():
    """
    Main execution function
    """
    # Initialize backtester
    backtester = BodyRetracementBacktester(data_directory=".")
    
    # Run backtest
    backtester.run_backtest()
    
    # Save results
    results_df, trades_df = backtester.save_results()
    
    # Create detailed analysis
    grouped_df = create_detailed_analysis(results_df, trades_df)
    
    # Create visualizations
    create_visualizations(grouped_df)
    
    # Export aggregated summary
    output_file = 'results/body_retracement_summary_2018_2025.csv'
    grouped_df.to_csv(output_file, index=False)
    print(f"\n✅ Résumé agrégé exporté: {output_file}")
    
    print("\n\n" + "="*100)
    print("✅ ANALYSE BODY RETRACEMENT AVEC FILTRE DE TAILLE TERMINÉE!")
    print("="*100)
    print("\nFichiers générés:")
    print("  • results/body_retracement_results_summary.csv - Résultats détaillés par configuration")
    print("  • results/body_retracement_all_trades.csv - Tous les trades individuels")
    print("  • results/body_retracement_summary_2018_2025.csv - Résumé agrégé 2018-2025")
    print("  • results/body_retracement_detailed_analysis.png - Graphiques d'analyse détaillée")
    print("  • results/body_retracement_heatmap.png - Heatmap des win rates")
    print("\n")


if __name__ == "__main__":
    main()

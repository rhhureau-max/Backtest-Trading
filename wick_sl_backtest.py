#!/usr/bin/env python3
"""
Wick-Based Stop Loss Trading Strategy Backtesting System
---------------------------------------------------------
This script analyzes trading strategies based on the 8:30 AM candle with:
- Stop-loss: 1 point below wick (low) for long, 1 point above wick (high) for short
- Body size displayed in points for all timeframes
- Entry times: 8:31 (1m), 8:35 (5m), 8:45 (15m)

Author: Trading Strategy Analyzer
Date: 2025-11-25
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
plt.rcParams['figure.figsize'] = (18, 14)


class WickSLBacktester:
    """
    Wick-Based Stop Loss Backtesting System
    
    Stop-loss placement:
    - Long: 1 point below the low (wick) of the 8:30 candle
    - Short: 1 point above the high (wick) of the 8:30 candle
    """
    
    def __init__(self, data_directory="."):
        """
        Initialize the Wick SL Backtester
        """
        self.data_directory = Path(data_directory)
        self.years = list(range(2018, 2026))  # 2018-2025
        self.timeframes = ['5m', '15m']  # 1m data not available for most years
        self.rr_ratios = [1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 10]
        
        # Entry times based on timeframe
        self.entry_times = {
            '1m': time(8, 31),   # 8:31 AM
            '5m': time(8, 35),   # 8:35 AM
            '15m': time(8, 45)   # 8:45 AM
        }
        
        # Reference time for candle detection
        self.candle_time = time(8, 30)  # 8:30 AM candle
        
        # SL offset (1 point)
        self.sl_offset = 1.0
        
        self.results = []
        self.all_trades = []
        
        # Cache for loaded data
        self.data_cache = {}
        
        # Statistics tracking
        self.stats = {
            'total_830_candles': 0,
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
    
    def detect_candles(self, df, timeframe):
        """
        Detect 8:30 AM candles and calculate body size in points
        
        Returns:
        --------
        List of dictionaries containing candle information
        """
        candles = []
        
        if df is None or len(df) == 0:
            return candles
        
        # Find all 8:30 AM candles
        candle_mask = df['TimeOnly'] == self.candle_time
        candle_df = df[candle_mask].copy()
        
        for idx, row in candle_df.iterrows():
            self.stats['total_830_candles'] += 1
            
            candle_open = row['Open']
            candle_close = row['Close']
            candle_high = row['High']
            candle_low = row['Low']
            
            # Calculate body size in points
            body_size = abs(candle_close - candle_open)
            
            # Skip doji candles (no body)
            if body_size < 0.5:
                continue
            
            # Determine direction
            if candle_close > candle_open:
                direction = 'bullish'
                body_top = candle_close
                body_bottom = candle_open
            else:
                direction = 'bearish'
                body_top = candle_open
                body_bottom = candle_close
            
            self.stats['valid_candles'] += 1
            
            candle_info = {
                'datetime': row['Datetime'],
                'date': row['Date'],
                'open': candle_open,
                'close': candle_close,
                'high': candle_high,
                'low': candle_low,
                'body_size': body_size,
                'body_top': body_top,
                'body_bottom': body_bottom,
                'direction': direction
            }
            
            candles.append(candle_info)
        
        return candles
    
    def calculate_stop_loss(self, candle_info):
        """
        Calculate stop-loss based on wick (high/low) + 1 point offset
        
        Parameters:
        -----------
        candle_info : dict
            Candle information
            
        Returns:
        --------
        tuple: (long_sl, short_sl)
        """
        # For long trades: SL is 1 point below the low (wick)
        long_sl = candle_info['low'] - self.sl_offset
        
        # For short trades: SL is 1 point above the high (wick)
        short_sl = candle_info['high'] + self.sl_offset
        
        return long_sl, short_sl
    
    def simulate_trade(self, df, candle_info, timeframe, rr_ratio):
        """
        Simulate a trade based on the wick SL strategy
        """
        candle_datetime = candle_info['datetime']
        entry_time = self.entry_times[timeframe]
        
        # Find entry candle
        entry_date = candle_datetime.date()
        entry_datetime = datetime.combine(entry_date, entry_time)
        
        # Get data after candle
        future_df = df[df['Datetime'] > candle_datetime].copy()
        
        if len(future_df) == 0:
            return None
        
        # Find the entry candle
        entry_candle = future_df[future_df['Datetime'] >= entry_datetime]
        
        if len(entry_candle) == 0:
            return None
        
        entry_candle = entry_candle.iloc[0]
        entry_price = entry_candle['Open']
        
        # Calculate stop-loss levels
        long_sl, short_sl = self.calculate_stop_loss(candle_info)
        
        # Determine trade direction based on candle direction
        if candle_info['direction'] == 'bullish':
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
            'candle_datetime': candle_datetime,
            'entry_datetime': entry_candle['Datetime'],
            'entry_price': entry_price,
            'direction': trade_direction,
            'candle_direction': candle_info['direction'],
            'body_size_points': candle_info['body_size'],
            'candle_high': candle_info['high'],
            'candle_low': candle_info['low'],
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
        print("\n" + "="*120)
        print("STRATÉGIE WICK-BASED STOP LOSS BACKTEST")
        print("="*120)
        print(f"\nConfiguration de la Stratégie:")
        print(f"  • Bougie de référence: 8:30 AM")
        print(f"  • Stop-Loss Long: 1 point sous le LOW (mèche basse) de la bougie 8:30")
        print(f"  • Stop-Loss Short: 1 point au-dessus du HIGH (mèche haute) de la bougie 8:30")
        print(f"  • Entrées: 8:31 (1m), 8:35 (5m), 8:45 (15m)")
        print(f"  • RR Ratios testés: {self.rr_ratios}")
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
                
                # Detect 8:30 candles
                candles = self.detect_candles(df, timeframe)
                print(f"  Found {len(candles)} valid 8:30 AM candles")
                
                for rr_ratio in self.rr_ratios:
                    config_count += 1
                    
                    wins = 0
                    losses = 0
                    no_exits = 0
                    total_pnl = 0
                    gross_profit = 0
                    gross_loss = 0
                    
                    config_trades = []
                    
                    # Simulate trades for each candle
                    for candle_info in candles:
                        trade = self.simulate_trade(df, candle_info, timeframe, rr_ratio)
                        
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
                        'total_candles': len(candles),
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
        
        print("\n" + "="*120)
        print("BACKTEST COMPLETED!")
        print("="*120)
        print(f"\nStatistiques:")
        print(f"  • Total de bougies 8:30 trouvées: {self.stats['total_830_candles']}")
        print(f"  • Bougies valides: {self.stats['valid_candles']}")
        print(f"\nTotal configurations testées: {len(self.results)}")
        print(f"Total trades exécutés: {len(self.all_trades)}")
    
    def save_results(self, output_dir='results'):
        """
        Save results to CSV files
        """
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # Save summary results
        results_df = pd.DataFrame(self.results)
        summary_file = output_path / 'wick_sl_results_summary.csv'
        results_df.to_csv(summary_file, index=False)
        print(f"\n✅ Summary results saved: {summary_file}")
        
        # Save all trades
        trades_df = pd.DataFrame(self.all_trades)
        trades_file = output_path / 'wick_sl_all_trades.csv'
        trades_df.to_csv(trades_file, index=False)
        print(f"✅ All trades saved: {trades_file}")
        
        return results_df, trades_df


def create_detailed_analysis(results_df, trades_df):
    """Create a comprehensive analysis report with body sizes in points"""
    
    print("\n\n" + "="*120)
    print("ANALYSE DÉTAILLÉE - STRATÉGIE WICK-BASED STOP LOSS")
    print("="*120)
    print("\n📋 Configuration:")
    print("  • Bougie de référence: 8:30 AM")
    print("  • Stop-Loss Long: 1 point sous le LOW de la bougie 8:30")
    print("  • Stop-Loss Short: 1 point au-dessus du HIGH de la bougie 8:30")
    print("  • Entrées: 8:31 (1m), 8:35 (5m), 8:45 (15m)")
    print("\n")
    
    # Aggregate by timeframe and RR ratio
    grouped = results_df.groupby(['timeframe', 'rr_ratio']).agg({
        'total_trades': 'sum',
        'wins': 'sum',
        'losses': 'sum',
        'total_pnl': 'sum',
        'gross_profit': 'sum',
        'gross_loss': 'sum',
        'total_candles': 'sum'
    }).reset_index()
    
    grouped['win_rate'] = (grouped['wins'] / grouped['total_trades'] * 100).round(2)
    grouped['profit_factor'] = (grouped['gross_profit'] / grouped['gross_loss']).round(2)
    grouped['profit_factor'] = grouped['profit_factor'].replace([np.inf, -np.inf], 0)
    
    # Section 1: Body Size Statistics in Points
    print("="*120)
    print("1. STATISTIQUES DES TAILLES DE CORPS (EN POINTS)")
    print("="*120 + "\n")
    
    body_stats = []
    for timeframe in ['1m', '5m', '15m']:
        tf_trades = trades_df[trades_df['timeframe'] == timeframe]
        if len(tf_trades) > 0:
            body_sizes = tf_trades['body_size_points'].dropna()
            body_stats.append({
                'Timeframe': timeframe.upper(),
                'Min (pts)': f"{body_sizes.min():.1f}",
                'Max (pts)': f"{body_sizes.max():.1f}",
                'Moyenne (pts)': f"{body_sizes.mean():.1f}",
                'Médiane (pts)': f"{body_sizes.median():.1f}",
                'Écart-type': f"{body_sizes.std():.1f}"
            })
    
    print(tabulate(body_stats, headers='keys', tablefmt='grid'))
    
    # Section 2: Results by Timeframe and RR
    print("\n\n" + "="*120)
    print("2. RÉSULTATS PAR TIMEFRAME ET RR RATIO (2018-2025)")
    print("="*120)
    
    for timeframe in ['1m', '5m', '15m']:
        # Get body size stats for this TF
        tf_trades = trades_df[trades_df['timeframe'] == timeframe]
        avg_body = tf_trades['body_size_points'].mean() if len(tf_trades) > 0 else 0
        
        print(f"\n📊 TIMEFRAME: {timeframe.upper()}")
        print(f"    Taille moyenne du corps: {avg_body:.1f} points")
        print(f"    SL Long: 1pt sous le LOW | SL Short: 1pt au-dessus du HIGH")
        print("-"*120)
        
        tf_data = grouped[grouped['timeframe'] == timeframe]
        
        table_data = []
        for _, row in tf_data.iterrows():
            table_data.append([
                f"{row['rr_ratio']:.1f}",
                int(row['total_trades']),
                int(row['wins']),
                int(row['losses']),
                f"{row['win_rate']:.2f}%",
                f"{row['profit_factor']:.2f}",
                f"{row['total_pnl']:.2f}"
            ])
        
        headers = ['RR Ratio', 'Total Trades', 'Trades Bons', 'Trades Mauvais', 
                  'Win Rate', 'Profit Factor', 'P&L Total']
        
        print(tabulate(table_data, headers=headers, tablefmt='grid'))
    
    # Section 3: Body Size Ranges Analysis
    print("\n\n" + "="*120)
    print("3. WIN RATE PAR TRANCHE DE TAILLE DU CORPS (EN POINTS)")
    print("="*120 + "\n")
    
    body_range_results = []
    
    for timeframe in ['1m', '5m', '15m']:
        tf_trades = trades_df[trades_df['timeframe'] == timeframe].copy()
        
        if len(tf_trades) == 0:
            continue
        
        # Create body size ranges in points
        tf_trades['body_range'] = pd.cut(tf_trades['body_size_points'], 
                                         bins=5, 
                                         precision=0)
        
        print(f"\n📊 {timeframe.upper()}:")
        
        for rr in sorted(tf_trades['rr_ratio'].unique()):
            rr_trades = tf_trades[tf_trades['rr_ratio'] == rr]
            
            range_data = []
            for body_range in sorted(rr_trades['body_range'].unique(), key=lambda x: x.left if pd.notna(x) else 0):
                if pd.isna(body_range):
                    continue
                    
                range_trades = rr_trades[rr_trades['body_range'] == body_range]
                wins = len(range_trades[range_trades['outcome'] == 'win'])
                total = len(range_trades[range_trades['outcome'].isin(['win', 'loss'])])
                
                if total > 0:
                    wr = (wins / total) * 100
                    range_data.append({
                        'range': f"{body_range.left:.0f}-{body_range.right:.0f} pts",
                        'rr': rr,
                        'total': total,
                        'wins': wins,
                        'win_rate': wr
                    })
            
            if range_data:
                body_range_results.extend([{**d, 'timeframe': timeframe} for d in range_data])
        
        # Display pivot table for this timeframe
        tf_range_df = pd.DataFrame([r for r in body_range_results if r['timeframe'] == timeframe])
        if len(tf_range_df) > 0:
            pivot = tf_range_df.pivot_table(
                index='range',
                columns='rr',
                values='win_rate',
                aggfunc='mean'
            )
            
            table_data = []
            for range_val in pivot.index:
                row_data = [range_val]
                for rr in sorted(pivot.columns):
                    val = pivot.loc[range_val, rr] if rr in pivot.columns else 0
                    row_data.append(f"{val:.1f}%" if not pd.isna(val) else "-")
                table_data.append(row_data)
            
            headers = ['Taille Corps (pts)'] + [f'RR {r:.1f}' for r in sorted(pivot.columns)]
            print(tabulate(table_data, headers=headers, tablefmt='grid'))
    
    # Section 4: Global Summary
    print("\n\n" + "="*120)
    print("4. RÉSUMÉ GLOBAL PAR TIMEFRAME")
    print("="*120 + "\n")
    
    summary = grouped.groupby('timeframe').agg({
        'total_trades': 'sum',
        'wins': 'sum',
        'losses': 'sum',
        'total_pnl': 'sum'
    }).reset_index()
    
    summary['win_rate'] = (summary['wins'] / summary['total_trades'] * 100).round(2)
    
    summary_data = []
    for _, row in summary.iterrows():
        tf = row['timeframe']
        tf_trades = trades_df[trades_df['timeframe'] == tf]
        avg_body = tf_trades['body_size_points'].mean() if len(tf_trades) > 0 else 0
        
        summary_data.append([
            tf.upper(),
            f"{avg_body:.1f} pts",
            int(row['total_trades']),
            int(row['wins']),
            int(row['losses']),
            f"{row['win_rate']:.2f}%",
            f"{row['total_pnl']:.2f}"
        ])
    
    headers = ['TF', 'Corps Moyen', 'Total Trades', 'Bons', 'Mauvais', 'Win Rate', 'P&L Total']
    print(tabulate(summary_data, headers=headers, tablefmt='grid'))
    
    # Section 5: Top Configurations
    print("\n\n" + "="*120)
    print("5. TOP 15 MEILLEURES CONFIGURATIONS PAR WIN RATE")
    print("="*120 + "\n")
    
    grouped_sorted = grouped.sort_values(['win_rate', 'total_trades'], ascending=[False, False])
    top_configs = grouped_sorted.head(15)
    
    table_data = []
    for idx, (_, row) in enumerate(top_configs.iterrows(), 1):
        tf = row['timeframe']
        tf_trades = trades_df[trades_df['timeframe'] == tf]
        avg_body = tf_trades['body_size_points'].mean() if len(tf_trades) > 0 else 0
        
        table_data.append([
            idx,
            tf.upper(),
            f"{avg_body:.0f} pts",
            f"{row['rr_ratio']:.1f}",
            int(row['total_trades']),
            int(row['wins']),
            int(row['losses']),
            f"{row['win_rate']:.2f}%",
            f"{row['profit_factor']:.2f}",
            f"{row['total_pnl']:.2f}"
        ])
    
    headers = ['Rang', 'TF', 'Corps Moy', 'RR', 'Total', 'Bons', 'Mauvais', 'Win Rate', 'PF', 'P&L']
    print(tabulate(table_data, headers=headers, tablefmt='grid'))
    
    # Section 6: Direction Analysis
    print("\n\n" + "="*120)
    print("6. ANALYSE PAR DIRECTION DE TRADE")
    print("="*120 + "\n")
    
    direction_stats = []
    for timeframe in ['1m', '5m', '15m']:
        tf_trades = trades_df[trades_df['timeframe'] == timeframe]
        
        if len(tf_trades) == 0:
            continue
        
        # Long trades (bullish candle)
        long_trades = tf_trades[tf_trades['direction'] == 'long']
        long_wins = len(long_trades[long_trades['outcome'] == 'win'])
        long_total = len(long_trades[long_trades['outcome'].isin(['win', 'loss'])])
        long_wr = (long_wins / long_total * 100) if long_total > 0 else 0
        long_avg_body = long_trades['body_size_points'].mean() if len(long_trades) > 0 else 0
        
        # Short trades (bearish candle)
        short_trades = tf_trades[tf_trades['direction'] == 'short']
        short_wins = len(short_trades[short_trades['outcome'] == 'win'])
        short_total = len(short_trades[short_trades['outcome'].isin(['win', 'loss'])])
        short_wr = (short_wins / short_total * 100) if short_total > 0 else 0
        short_avg_body = short_trades['body_size_points'].mean() if len(short_trades) > 0 else 0
        
        direction_stats.append([
            timeframe.upper(),
            f"{long_avg_body:.1f} pts",
            long_total,
            long_wins,
            f"{long_wr:.1f}%",
            f"{short_avg_body:.1f} pts",
            short_total,
            short_wins,
            f"{short_wr:.1f}%"
        ])
    
    headers = ['TF', 'Corps Long', 'Long Total', 'Long Bons', 'Long WR', 
               'Corps Short', 'Short Total', 'Short Bons', 'Short WR']
    print(tabulate(direction_stats, headers=headers, tablefmt='grid'))
    
    return grouped


def create_visualizations(grouped_df, trades_df):
    """Create comprehensive visualizations"""
    
    print("\n\n📈 Génération des visualisations...")
    
    # Figure 1: Win Rate Heatmap by Timeframe and RR
    fig, axes = plt.subplots(1, 3, figsize=(20, 6))
    fig.suptitle('Heatmap Win Rate (%) - Stratégie Wick-Based SL (2018-2025)\n' +
                 'SL: 1pt sous LOW (Long) | 1pt au-dessus HIGH (Short)', 
                 fontsize=16, fontweight='bold')
    
    for idx, timeframe in enumerate(['1m', '5m', '15m']):
        ax = axes[idx]
        tf_data = grouped_df[grouped_df['timeframe'] == timeframe]
        tf_trades = trades_df[trades_df['timeframe'] == timeframe]
        avg_body = tf_trades['body_size_points'].mean() if len(tf_trades) > 0 else 0
        
        # Create simple heatmap data
        rr_values = sorted(tf_data['rr_ratio'].unique())
        win_rates = [tf_data[tf_data['rr_ratio'] == rr]['win_rate'].values[0] if len(tf_data[tf_data['rr_ratio'] == rr]) > 0 else 0 for rr in rr_values]
        
        # Bar chart instead of heatmap for single row
        colors = ['#2E7D32' if wr >= 35 else '#FBC02D' if wr >= 25 else '#D32F2F' for wr in win_rates]
        bars = ax.bar(range(len(rr_values)), win_rates, color=colors, alpha=0.8)
        
        # Add value labels
        for i, (bar, wr) in enumerate(zip(bars, win_rates)):
            ax.annotate(f'{wr:.1f}%', xy=(bar.get_x() + bar.get_width()/2, bar.get_height()),
                       ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        ax.set_xlabel('RR Ratio', fontsize=11, fontweight='bold')
        ax.set_ylabel('Win Rate (%)', fontsize=11, fontweight='bold')
        ax.set_title(f'{timeframe.upper()} (Corps moyen: {avg_body:.1f} pts)', fontsize=13, fontweight='bold')
        ax.set_xticks(range(len(rr_values)))
        ax.set_xticklabels([f'{r:.1f}' for r in rr_values], fontsize=10)
        ax.set_ylim(0, max(win_rates) * 1.2 if win_rates else 50)
        ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig('results/wick_sl_win_rate_by_rr.png', dpi=300, bbox_inches='tight')
    print("✅ Win rate par RR sauvegardé: results/wick_sl_win_rate_by_rr.png")
    
    # Figure 2: Body Size Distribution and Win Rate Trend
    fig, axes = plt.subplots(2, 3, figsize=(20, 12))
    fig.suptitle('Stratégie Wick-Based SL - Analyse des Tailles de Corps (2018-2025)', 
                 fontsize=16, fontweight='bold')
    
    for idx, timeframe in enumerate(['1m', '5m', '15m']):
        tf_trades = trades_df[trades_df['timeframe'] == timeframe]
        
        # Row 1: Body Size Distribution
        ax1 = axes[0, idx]
        if len(tf_trades) > 0:
            ax1.hist(tf_trades['body_size_points'], bins=30, color='steelblue', alpha=0.7, edgecolor='black')
            ax1.axvline(tf_trades['body_size_points'].mean(), color='red', linestyle='--', linewidth=2, 
                       label=f'Moyenne: {tf_trades["body_size_points"].mean():.1f} pts')
            ax1.axvline(tf_trades['body_size_points'].median(), color='orange', linestyle='--', linewidth=2,
                       label=f'Médiane: {tf_trades["body_size_points"].median():.1f} pts')
        ax1.set_xlabel('Taille du Corps (points)', fontsize=11, fontweight='bold')
        ax1.set_ylabel('Fréquence', fontsize=11, fontweight='bold')
        ax1.set_title(f'{timeframe.upper()} - Distribution des Corps', fontsize=12, fontweight='bold')
        ax1.legend(fontsize=9)
        ax1.grid(True, alpha=0.3)
        
        # Row 2: Win Rate by RR
        ax2 = axes[1, idx]
        tf_data = grouped_df[grouped_df['timeframe'] == timeframe]
        ax2.plot(tf_data['rr_ratio'], tf_data['win_rate'], marker='o', linewidth=2.5, 
                markersize=10, color='#2E86AB')
        ax2.set_xlabel('RR Ratio', fontsize=11, fontweight='bold')
        ax2.set_ylabel('Win Rate (%)', fontsize=11, fontweight='bold')
        ax2.set_title(f'{timeframe.upper()} - Win Rate par RR', fontsize=12, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        ax2.set_xticks(tf_data['rr_ratio'].unique())
    
    plt.tight_layout()
    plt.savefig('results/wick_sl_body_size_analysis.png', dpi=300, bbox_inches='tight')
    print("✅ Analyse taille de corps sauvegardée: results/wick_sl_body_size_analysis.png")
    
    # Figure 3: Combined Heatmap
    fig, ax = plt.subplots(1, 1, figsize=(16, 6))
    fig.suptitle('Heatmap Win Rate (%) - Toutes Configurations\n' +
                 'Stratégie Wick SL: 1pt sous/au-dessus de la mèche', 
                 fontsize=16, fontweight='bold')
    
    # Create pivot for heatmap
    pivot = grouped_df.pivot_table(
        index='timeframe',
        columns='rr_ratio',
        values='win_rate'
    )
    pivot = pivot.reindex(['1m', '5m', '15m'])
    
    # Create custom labels with body sizes
    y_labels = []
    for tf in ['1m', '5m', '15m']:
        tf_trades = trades_df[trades_df['timeframe'] == tf]
        avg_body = tf_trades['body_size_points'].mean() if len(tf_trades) > 0 else 0
        y_labels.append(f'{tf.upper()} (corps: {avg_body:.0f} pts)')
    
    sns.heatmap(pivot, annot=True, fmt='.1f', cmap='RdYlGn', 
               center=30, vmin=0, vmax=50, ax=ax,
               cbar_kws={'label': 'Win Rate (%)'})
    ax.set_xlabel('RR Ratio', fontsize=12, fontweight='bold')
    ax.set_ylabel('Timeframe', fontsize=12, fontweight='bold')
    ax.set_yticklabels(y_labels, rotation=0, fontsize=11)
    
    plt.tight_layout()
    plt.savefig('results/wick_sl_heatmap.png', dpi=300, bbox_inches='tight')
    print("✅ Heatmap sauvegardée: results/wick_sl_heatmap.png")


def export_results(grouped_df, trades_df):
    """Export analysis results to CSV"""
    
    # Add body size stats to grouped results
    grouped_with_body = grouped_df.copy()
    body_stats = []
    for _, row in grouped_with_body.iterrows():
        tf_trades = trades_df[trades_df['timeframe'] == row['timeframe']]
        avg_body = tf_trades['body_size_points'].mean() if len(tf_trades) > 0 else 0
        body_stats.append(avg_body)
    grouped_with_body['avg_body_size_points'] = body_stats
    
    grouped_with_body.to_csv('results/wick_sl_summary_2018_2025.csv', index=False)
    print("\n✅ Résumé agrégé exporté: results/wick_sl_summary_2018_2025.csv")


def main():
    """Main execution function"""
    
    # Initialize backtester
    backtester = WickSLBacktester(data_directory=".")
    
    # Run backtest
    backtester.run_backtest()
    
    # Save results
    results_df, trades_df = backtester.save_results()
    
    # Create detailed analysis
    grouped_df = create_detailed_analysis(results_df, trades_df)
    
    # Create visualizations
    create_visualizations(grouped_df, trades_df)
    
    # Export results
    export_results(grouped_df, trades_df)
    
    print("\n\n" + "="*120)
    print("✅ ANALYSE WICK-BASED STOP LOSS TERMINÉE!")
    print("="*120)
    print("\nFichiers générés:")
    print("  • results/wick_sl_results_summary.csv - Résultats détaillés")
    print("  • results/wick_sl_all_trades.csv - Tous les trades")
    print("  • results/wick_sl_summary_2018_2025.csv - Résumé agrégé avec tailles de corps")
    print("  • results/wick_sl_win_rate_by_rr.png - Win rate par RR")
    print("  • results/wick_sl_body_size_analysis.png - Analyse taille de corps")
    print("  • results/wick_sl_heatmap.png - Heatmap des win rates")
    print("\n")


if __name__ == "__main__":
    main()

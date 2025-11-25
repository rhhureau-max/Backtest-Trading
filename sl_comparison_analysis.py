#!/usr/bin/env python3
"""
Stop-Loss Placement Comparison Analysis
========================================
This script compares different stop-loss placements based on the 8:30 AM candle:
- Middle of body (50% retracement)
- 62% retracement of body
- 78% retracement of body

With body size filters: 50, 100, 150, 200, 250 points
And RR ratios: 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5

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
plt.rcParams['figure.figsize'] = (20, 14)


class SLComparisonBacktester:
    """
    Stop-Loss Placement Comparison Backtesting System
    
    Compares multiple SL placements:
    - Middle (50%): SL at middle of candle body
    - 62%: SL at 62% retracement of body
    - 78%: SL at 78% retracement of body
    """
    
    def __init__(self, data_directory="."):
        """Initialize the SL Comparison Backtester"""
        self.data_directory = Path(data_directory)
        self.years = list(range(2018, 2026))  # 2018-2025
        self.timeframes = ['5m', '15m']
        self.rr_ratios = [1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]
        self.sl_placements = ['middle', '62%', '78%']
        self.body_size_filters = [50, 100, 150, 200, 250]  # In points
        
        # Entry times based on timeframe
        self.entry_times = {
            '1m': time(8, 31),
            '5m': time(8, 35),
            '15m': time(8, 45)
        }
        
        # Reference time for candle detection
        self.candle_time = time(8, 30)
        
        self.results = []
        self.all_trades = []
        self.data_cache = {}
        
    def load_data(self, year, timeframe):
        """Load CSV data for a specific year and timeframe"""
        cache_key = (year, timeframe)
        
        if cache_key in self.data_cache:
            return self.data_cache[cache_key]
        
        filename = f"{year} {timeframe}.csv"
        filepath = self.data_directory / filename
        
        if not filepath.exists():
            return None
        
        try:
            df = pd.read_csv(filepath, sep=';', skiprows=1,
                           names=['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume'])
            
            df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], 
                                           format='%d/%m/%Y %H:%M:%S', 
                                           errors='coerce')
            df['TimeOnly'] = df['Datetime'].dt.time
            df = df.dropna(subset=['Datetime'])
            df = df.sort_values('Datetime').reset_index(drop=True)
            
            self.data_cache[cache_key] = df
            return df
            
        except Exception as e:
            print(f"Error loading {filepath}: {e}")
            return None
    
    def detect_candles(self, df, min_body_size=0):
        """Detect 8:30 AM candles with optional body size filter"""
        candles = []
        
        if df is None or len(df) == 0:
            return candles
        
        candle_mask = df['TimeOnly'] == self.candle_time
        candle_df = df[candle_mask].copy()
        
        for idx, row in candle_df.iterrows():
            candle_open = row['Open']
            candle_close = row['Close']
            candle_high = row['High']
            candle_low = row['Low']
            
            # Calculate body size in points
            body_size = abs(candle_close - candle_open)
            
            # Skip doji candles (no body) or small bodies
            if body_size < 0.5:
                continue
            
            # Apply body size filter if specified
            if min_body_size > 0 and body_size < min_body_size:
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
    
    def calculate_stop_loss(self, candle_info, sl_type):
        """
        Calculate stop-loss based on retracement level
        
        For Long trades (bullish candle):
        - Middle (50%): SL at middle of body
        - 62%: SL at 62% retracement (closer to bottom)
        - 78%: SL at 78% retracement (even closer to bottom)
        
        For Short trades (bearish candle):
        - Middle (50%): SL at middle of body
        - 62%: SL at 62% retracement (closer to top)
        - 78%: SL at 78% retracement (even closer to top)
        """
        body_top = candle_info['body_top']
        body_bottom = candle_info['body_bottom']
        body_range = body_top - body_bottom
        
        if sl_type == 'middle':
            retracement = 0.50
        elif sl_type == '62%':
            retracement = 0.62
        elif sl_type == '78%':
            retracement = 0.78
        else:
            retracement = 0.50
        
        # Calculate SL level
        if candle_info['direction'] == 'bullish':
            # For long trades: SL is below entry (retracement from top)
            sl_level = body_top - (body_range * retracement)
        else:
            # For short trades: SL is above entry (retracement from bottom)
            sl_level = body_bottom + (body_range * retracement)
        
        return sl_level
    
    def simulate_trade(self, df, candle_info, timeframe, rr_ratio, sl_type):
        """Simulate a trade based on the SL placement strategy"""
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
        
        # Calculate stop-loss
        sl_price = self.calculate_stop_loss(candle_info, sl_type)
        
        # Determine trade direction based on candle direction
        if candle_info['direction'] == 'bullish':
            trade_direction = 'long'
            risk = entry_price - sl_price
            
            if risk <= 0:
                return None
            
            tp_price = entry_price + (risk * rr_ratio)
            
        else:
            trade_direction = 'short'
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
                if candle['High'] >= tp_price:
                    hit_tp = True
                    exit_datetime = candle['Datetime']
                    exit_price = tp_price
                    break
                if candle['Low'] <= sl_price:
                    hit_sl = True
                    exit_datetime = candle['Datetime']
                    exit_price = sl_price
                    break
            else:
                if candle['Low'] <= tp_price:
                    hit_tp = True
                    exit_datetime = candle['Datetime']
                    exit_price = tp_price
                    break
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
            'body_size_points': candle_info['body_size'],
            'sl_type': sl_type,
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
        """Run the complete backtest across all configurations"""
        print("\n" + "="*120)
        print("COMPARAISON DES PLACEMENTS DE STOP-LOSS")
        print("="*120)
        print(f"\nConfiguration de la Stratégie:")
        print(f"  • Bougie de référence: 8:30 AM")
        print(f"  • Stop-Loss Types: Middle (50%), 62%, 78% retracement du corps")
        print(f"  • Filtres de taille de corps: {self.body_size_filters} points")
        print(f"  • RR Ratios testés: {self.rr_ratios}")
        print(f"  • Entrées: 8:35 (5m), 8:45 (15m)")
        print("\n")
        
        for year in self.years:
            for timeframe in self.timeframes:
                print(f"\nProcessing {year} - {timeframe}...")
                
                df = self.load_data(year, timeframe)
                
                if df is None:
                    continue
                
                for body_filter in self.body_size_filters:
                    # Detect candles with body size filter
                    candles = self.detect_candles(df, min_body_size=body_filter)
                    
                    if len(candles) == 0:
                        continue
                    
                    for sl_type in self.sl_placements:
                        for rr_ratio in self.rr_ratios:
                            wins = 0
                            losses = 0
                            no_exits = 0
                            total_pnl = 0
                            gross_profit = 0
                            gross_loss = 0
                            
                            config_trades = []
                            
                            for candle_info in candles:
                                trade = self.simulate_trade(df, candle_info, timeframe, rr_ratio, sl_type)
                                
                                if trade is None:
                                    continue
                                
                                if trade['outcome'] == 'win':
                                    wins += 1
                                    gross_profit += trade['pnl']
                                elif trade['outcome'] == 'loss':
                                    losses += 1
                                    gross_loss += abs(trade['pnl'])
                                else:
                                    no_exits += 1
                                
                                total_pnl += trade['pnl']
                                
                                trade['year'] = year
                                trade['timeframe'] = timeframe
                                trade['body_filter'] = body_filter
                                config_trades.append(trade)
                            
                            total_trades = wins + losses + no_exits
                            
                            if total_trades == 0:
                                continue
                            
                            win_rate = (wins / total_trades * 100) if total_trades > 0 else 0
                            profit_factor = (gross_profit / gross_loss) if gross_loss > 0 else 0
                            
                            result = {
                                'year': year,
                                'timeframe': timeframe,
                                'body_filter': body_filter,
                                'sl_type': sl_type,
                                'rr_ratio': rr_ratio,
                                'total_candles': len(candles),
                                'total_trades': total_trades,
                                'wins': wins,
                                'losses': losses,
                                'no_exit': no_exits,
                                'win_rate': win_rate,
                                'total_pnl': total_pnl,
                                'profit_factor': profit_factor,
                                'gross_profit': gross_profit,
                                'gross_loss': gross_loss
                            }
                            
                            self.results.append(result)
                            self.all_trades.extend(config_trades)
        
        print("\n" + "="*120)
        print("BACKTEST COMPLETED!")
        print("="*120)
        print(f"\nTotal configurations testées: {len(self.results)}")
        print(f"Total trades exécutés: {len(self.all_trades)}")
    
    def save_results(self, output_dir='results'):
        """Save results to CSV files"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        results_df = pd.DataFrame(self.results)
        results_df.to_csv(output_path / 'sl_comparison_results.csv', index=False)
        
        trades_df = pd.DataFrame(self.all_trades)
        trades_df.to_csv(output_path / 'sl_comparison_all_trades.csv', index=False)
        
        return results_df, trades_df


def create_detailed_analysis(results_df, trades_df):
    """Create a comprehensive comparison analysis"""
    
    print("\n\n" + "="*120)
    print("ANALYSE DÉTAILLÉE - COMPARAISON DES PLACEMENTS DE STOP-LOSS")
    print("="*120)
    
    # Aggregate by configuration
    grouped = results_df.groupby(['timeframe', 'body_filter', 'sl_type', 'rr_ratio']).agg({
        'total_trades': 'sum',
        'wins': 'sum',
        'losses': 'sum',
        'total_pnl': 'sum',
        'gross_profit': 'sum',
        'gross_loss': 'sum'
    }).reset_index()
    
    grouped['win_rate'] = (grouped['wins'] / grouped['total_trades'] * 100).round(2)
    grouped['profit_factor'] = (grouped['gross_profit'] / grouped['gross_loss']).round(2)
    grouped['profit_factor'] = grouped['profit_factor'].replace([np.inf, -np.inf], 0)
    
    # Section 1: Results by Body Size Filter and SL Type
    print("\n\n" + "="*120)
    print("1. WIN RATE PAR TAILLE DE CORPS ET TYPE DE STOP-LOSS")
    print("="*120)
    
    for timeframe in ['5m', '15m']:
        print(f"\n📊 TIMEFRAME: {timeframe.upper()}")
        print("-"*100)
        
        for body_filter in [50, 100, 150, 200, 250]:
            print(f"\n  Corps ≥ {body_filter} points:")
            
            tf_body_data = grouped[(grouped['timeframe'] == timeframe) & 
                                    (grouped['body_filter'] == body_filter)]
            
            table_data = []
            for sl_type in ['middle', '62%', '78%']:
                sl_data = tf_body_data[tf_body_data['sl_type'] == sl_type]
                
                row = [sl_type]
                for rr in [1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]:
                    rr_data = sl_data[sl_data['rr_ratio'] == rr]
                    if len(rr_data) > 0:
                        wr = rr_data['win_rate'].values[0]
                        trades = int(rr_data['total_trades'].values[0])
                        row.append(f"{wr:.1f}% ({trades})")
                    else:
                        row.append("-")
                table_data.append(row)
            
            headers = ['SL Type'] + [f'RR {r}' for r in [1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]]
            print(tabulate(table_data, headers=headers, tablefmt='grid'))
    
    # Section 2: Best Configurations per Body Size
    print("\n\n" + "="*120)
    print("2. MEILLEURES CONFIGURATIONS PAR TAILLE DE CORPS")
    print("="*120)
    
    best_configs = []
    for timeframe in ['5m', '15m']:
        for body_filter in [50, 100, 150, 200, 250]:
            tf_body_data = grouped[(grouped['timeframe'] == timeframe) & 
                                    (grouped['body_filter'] == body_filter)]
            
            if len(tf_body_data) > 0:
                best = tf_body_data.loc[tf_body_data['win_rate'].idxmax()]
                best_configs.append({
                    'Timeframe': timeframe.upper(),
                    'Corps Min (pts)': body_filter,
                    'SL Type': best['sl_type'],
                    'RR': best['rr_ratio'],
                    'Win Rate': f"{best['win_rate']:.1f}%",
                    'Trades': int(best['total_trades']),
                    'Profit Factor': f"{best['profit_factor']:.2f}"
                })
    
    print("\n")
    print(tabulate(best_configs, headers='keys', tablefmt='grid'))
    
    # Section 3: Summary by SL Type
    print("\n\n" + "="*120)
    print("3. RÉSUMÉ PAR TYPE DE STOP-LOSS (TOUS FILTRES CONFONDUS)")
    print("="*120)
    
    sl_summary = grouped.groupby(['timeframe', 'sl_type']).agg({
        'total_trades': 'sum',
        'wins': 'sum',
        'losses': 'sum'
    }).reset_index()
    sl_summary['win_rate'] = (sl_summary['wins'] / sl_summary['total_trades'] * 100).round(2)
    
    summary_table = []
    for timeframe in ['5m', '15m']:
        for sl_type in ['middle', '62%', '78%']:
            data = sl_summary[(sl_summary['timeframe'] == timeframe) & 
                              (sl_summary['sl_type'] == sl_type)]
            if len(data) > 0:
                summary_table.append([
                    timeframe.upper(),
                    sl_type,
                    int(data['total_trades'].values[0]),
                    int(data['wins'].values[0]),
                    int(data['losses'].values[0]),
                    f"{data['win_rate'].values[0]:.2f}%"
                ])
    
    headers = ['TF', 'SL Type', 'Total Trades', 'Bons', 'Mauvais', 'Win Rate']
    print("\n")
    print(tabulate(summary_table, headers=headers, tablefmt='grid'))
    
    # Section 4: Summary by RR Ratio
    print("\n\n" + "="*120)
    print("4. WIN RATE MOYEN PAR RR RATIO (TOUS SL CONFONDUS)")
    print("="*120)
    
    rr_summary = grouped.groupby(['timeframe', 'rr_ratio']).agg({
        'total_trades': 'sum',
        'wins': 'sum',
        'losses': 'sum'
    }).reset_index()
    rr_summary['win_rate'] = (rr_summary['wins'] / rr_summary['total_trades'] * 100).round(2)
    
    for timeframe in ['5m', '15m']:
        print(f"\n📊 {timeframe.upper()}:")
        tf_data = rr_summary[rr_summary['timeframe'] == timeframe]
        
        table_data = []
        for _, row in tf_data.iterrows():
            table_data.append([
                row['rr_ratio'],
                int(row['total_trades']),
                int(row['wins']),
                int(row['losses']),
                f"{row['win_rate']:.2f}%"
            ])
        
        headers = ['RR Ratio', 'Total', 'Bons', 'Mauvais', 'Win Rate']
        print(tabulate(table_data, headers=headers, tablefmt='grid'))
    
    return grouped


def create_visualizations(grouped_df):
    """Create comprehensive visualizations"""
    
    print("\n\n📈 Génération des visualisations...")
    
    # Figure 1: Heatmaps by Body Size Filter (for each TF and SL type)
    for timeframe in ['5m', '15m']:
        fig, axes = plt.subplots(1, 3, figsize=(22, 8))
        fig.suptitle(f'Win Rate (%) - {timeframe.upper()} - Comparaison des Stop-Loss\n' +
                     'Par Taille de Corps et RR Ratio (2018-2025)', 
                     fontsize=16, fontweight='bold')
        
        for idx, sl_type in enumerate(['middle', '62%', '78%']):
            ax = axes[idx]
            
            sl_data = grouped_df[(grouped_df['timeframe'] == timeframe) & 
                                  (grouped_df['sl_type'] == sl_type)]
            
            if len(sl_data) == 0:
                continue
            
            # Create pivot table
            pivot = sl_data.pivot_table(
                index='body_filter',
                columns='rr_ratio',
                values='win_rate',
                aggfunc='mean'
            )
            
            # Sort index
            pivot = pivot.sort_index()
            
            # Create heatmap
            sns.heatmap(pivot, annot=True, fmt='.1f', cmap='RdYlGn', 
                       center=30, vmin=0, vmax=60, ax=ax,
                       cbar_kws={'label': 'Win Rate (%)'})
            
            ax.set_xlabel('RR Ratio', fontsize=12, fontweight='bold')
            ax.set_ylabel('Taille Corps Min (points)', fontsize=12, fontweight='bold')
            ax.set_title(f'SL: {sl_type.upper()}', fontsize=14, fontweight='bold')
            ax.set_yticklabels([f'≥{int(v)} pts' for v in pivot.index], rotation=0)
        
        plt.tight_layout()
        plt.savefig(f'results/sl_comparison_heatmap_{timeframe}.png', dpi=300, bbox_inches='tight')
        print(f"✅ Heatmap {timeframe.upper()} sauvegardé: results/sl_comparison_heatmap_{timeframe}.png")
    
    # Figure 2: Comparison of SL types across body sizes
    fig, axes = plt.subplots(2, 5, figsize=(25, 12))
    fig.suptitle('Comparaison des Types de Stop-Loss par Taille de Corps\n' +
                 'Win Rate (%) par RR Ratio (2018-2025)', 
                 fontsize=16, fontweight='bold')
    
    for tf_idx, timeframe in enumerate(['5m', '15m']):
        for body_idx, body_filter in enumerate([50, 100, 150, 200, 250]):
            ax = axes[tf_idx, body_idx]
            
            for sl_type in ['middle', '62%', '78%']:
                sl_data = grouped_df[(grouped_df['timeframe'] == timeframe) & 
                                      (grouped_df['body_filter'] == body_filter) &
                                      (grouped_df['sl_type'] == sl_type)]
                
                if len(sl_data) > 0:
                    sl_data = sl_data.sort_values('rr_ratio')
                    ax.plot(sl_data['rr_ratio'], sl_data['win_rate'], 
                           marker='o', linewidth=2, markersize=6, label=sl_type)
            
            ax.set_xlabel('RR Ratio', fontsize=10)
            ax.set_ylabel('Win Rate (%)', fontsize=10)
            ax.set_title(f'{timeframe.upper()} | Corps ≥{body_filter} pts', fontsize=11, fontweight='bold')
            ax.legend(fontsize=8)
            ax.grid(True, alpha=0.3)
            ax.set_ylim(0, 70)
    
    plt.tight_layout()
    plt.savefig('results/sl_comparison_by_body_size.png', dpi=300, bbox_inches='tight')
    print("✅ Comparaison par taille de corps sauvegardée: results/sl_comparison_by_body_size.png")
    
    # Figure 3: Bar chart comparison - Best RR for each configuration
    fig, axes = plt.subplots(2, 3, figsize=(20, 12))
    fig.suptitle('Comparaison Détaillée des Stop-Loss\nWin Rate par RR Ratio et Taille de Corps', 
                 fontsize=16, fontweight='bold')
    
    for tf_idx, timeframe in enumerate(['5m', '15m']):
        for sl_idx, sl_type in enumerate(['middle', '62%', '78%']):
            ax = axes[tf_idx, sl_idx]
            
            sl_data = grouped_df[(grouped_df['timeframe'] == timeframe) & 
                                  (grouped_df['sl_type'] == sl_type)]
            
            if len(sl_data) == 0:
                continue
            
            # Group by body filter and RR
            pivot = sl_data.pivot_table(
                index='rr_ratio',
                columns='body_filter',
                values='win_rate',
                aggfunc='mean'
            )
            
            pivot.plot(kind='bar', ax=ax, width=0.8)
            ax.set_xlabel('RR Ratio', fontsize=11)
            ax.set_ylabel('Win Rate (%)', fontsize=11)
            ax.set_title(f'{timeframe.upper()} - SL: {sl_type.upper()}', fontsize=13, fontweight='bold')
            ax.legend(title='Corps Min (pts)', fontsize=8)
            ax.set_xticklabels([f'{x:.1f}' for x in pivot.index], rotation=0)
            ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig('results/sl_comparison_bar_charts.png', dpi=300, bbox_inches='tight')
    print("✅ Bar charts sauvegardés: results/sl_comparison_bar_charts.png")
    
    # Figure 4: Summary heatmap - Average win rate by SL type and body filter
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    fig.suptitle('Résumé: Win Rate Moyen par Type de SL et Taille de Corps\n' +
                 'Moyenne sur tous les RR Ratios (2018-2025)', 
                 fontsize=16, fontweight='bold')
    
    for tf_idx, timeframe in enumerate(['5m', '15m']):
        ax = axes[tf_idx]
        
        tf_data = grouped_df[grouped_df['timeframe'] == timeframe]
        
        # Aggregate by SL type and body filter
        summary = tf_data.groupby(['sl_type', 'body_filter']).agg({
            'total_trades': 'sum',
            'wins': 'sum'
        }).reset_index()
        summary['win_rate'] = (summary['wins'] / summary['total_trades'] * 100).round(1)
        
        pivot = summary.pivot_table(
            index='sl_type',
            columns='body_filter',
            values='win_rate'
        )
        
        # Reorder index
        pivot = pivot.reindex(['middle', '62%', '78%'])
        
        sns.heatmap(pivot, annot=True, fmt='.1f', cmap='RdYlGn', 
                   center=25, vmin=15, vmax=40, ax=ax,
                   cbar_kws={'label': 'Win Rate Moyen (%)'})
        
        ax.set_xlabel('Taille Corps Min (points)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Type de Stop-Loss', fontsize=12, fontweight='bold')
        ax.set_title(f'{timeframe.upper()}', fontsize=14, fontweight='bold')
        ax.set_xticklabels([f'≥{int(v)} pts' for v in pivot.columns])
        ax.set_yticklabels(['Middle (50%)', '62%', '78%'], rotation=0)
    
    plt.tight_layout()
    plt.savefig('results/sl_comparison_summary_heatmap.png', dpi=300, bbox_inches='tight')
    print("✅ Heatmap résumé sauvegardé: results/sl_comparison_summary_heatmap.png")


def export_summary(grouped_df):
    """Export summary to CSV"""
    
    # Create detailed summary
    summary = grouped_df.copy()
    
    # Calculate expected value
    summary['expected_value'] = (summary['win_rate']/100 * summary['rr_ratio']) - \
                                 ((100 - summary['win_rate'])/100)
    
    summary.to_csv('results/sl_comparison_summary.csv', index=False)
    print("\n✅ Résumé exporté: results/sl_comparison_summary.csv")
    
    # Create best configurations table
    best_per_filter = []
    for timeframe in ['5m', '15m']:
        for body_filter in [50, 100, 150, 200, 250]:
            tf_body_data = grouped_df[(grouped_df['timeframe'] == timeframe) & 
                                       (grouped_df['body_filter'] == body_filter)]
            
            if len(tf_body_data) > 0:
                # Best by win rate
                best_wr = tf_body_data.loc[tf_body_data['win_rate'].idxmax()]
                
                # Calculate EV
                ev = (best_wr['win_rate']/100 * best_wr['rr_ratio']) - \
                     ((100 - best_wr['win_rate'])/100)
                
                best_per_filter.append({
                    'timeframe': timeframe,
                    'body_filter': body_filter,
                    'best_sl_type': best_wr['sl_type'],
                    'best_rr': best_wr['rr_ratio'],
                    'win_rate': best_wr['win_rate'],
                    'total_trades': int(best_wr['total_trades']),
                    'expected_value': round(ev, 4)
                })
    
    best_df = pd.DataFrame(best_per_filter)
    best_df.to_csv('results/sl_comparison_best_configs.csv', index=False)
    print("✅ Meilleures configurations exportées: results/sl_comparison_best_configs.csv")


def main():
    """Main execution function"""
    
    # Initialize backtester
    backtester = SLComparisonBacktester(data_directory=".")
    
    # Run backtest
    backtester.run_backtest()
    
    # Save results
    results_df, trades_df = backtester.save_results()
    
    # Create detailed analysis
    grouped_df = create_detailed_analysis(results_df, trades_df)
    
    # Create visualizations
    create_visualizations(grouped_df)
    
    # Export summary
    export_summary(grouped_df)
    
    print("\n\n" + "="*120)
    print("✅ ANALYSE COMPARAISON STOP-LOSS TERMINÉE!")
    print("="*120)
    print("\nFichiers générés:")
    print("  • results/sl_comparison_results.csv - Résultats détaillés")
    print("  • results/sl_comparison_all_trades.csv - Tous les trades")
    print("  • results/sl_comparison_summary.csv - Résumé agrégé")
    print("  • results/sl_comparison_best_configs.csv - Meilleures configurations")
    print("  • results/sl_comparison_heatmap_5m.png - Heatmap 5M")
    print("  • results/sl_comparison_heatmap_15m.png - Heatmap 15M")
    print("  • results/sl_comparison_by_body_size.png - Comparaison par taille")
    print("  • results/sl_comparison_bar_charts.png - Bar charts détaillés")
    print("  • results/sl_comparison_summary_heatmap.png - Heatmap résumé")
    print("\n")


if __name__ == "__main__":
    main()

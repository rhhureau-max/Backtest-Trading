"""
Visualization Module
Creates comprehensive charts and plots for backtest analysis
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.gridspec import GridSpec
import seaborn as sns
from datetime import datetime
import warnings
# Suppress only matplotlib deprecation warnings
warnings.filterwarnings('ignore', category=DeprecationWarning)
warnings.filterwarnings('ignore', category=FutureWarning)

# Set style
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.size'] = 10


class Visualizer:
    """Create visualizations for backtest results"""
    
    def __init__(self, trades_df, metrics, timeframe, output_dir='results'):
        """
        Initialize Visualizer
        
        Parameters:
        -----------
        trades_df : pd.DataFrame
            DataFrame containing trade data
        metrics : dict
            Dictionary of performance metrics
        timeframe : str
            Timeframe identifier (e.g., '1m', '5m', '15m')
        output_dir : str
            Directory to save output files
        """
        self.trades_df = trades_df
        self.metrics = metrics
        self.timeframe = timeframe
        self.output_dir = output_dir
        
    def plot_equity_curve(self, filename=None):
        """Plot cumulative equity curve"""
        if len(self.trades_df) == 0:
            print("No trades to plot")
            return
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), 
                                        gridspec_kw={'height_ratios': [3, 1]})
        
        # Equity curve
        ax1.plot(self.trades_df['entry_time'], self.trades_df['equity'], 
                 linewidth=2, color='#2E86AB', label='Equity')
        ax1.axhline(y=self.trades_df['equity'].iloc[0], color='gray', 
                   linestyle='--', alpha=0.5, label='Initial Capital')
        ax1.fill_between(self.trades_df['entry_time'], 
                         self.trades_df['equity'].iloc[0], 
                         self.trades_df['equity'], 
                         where=(self.trades_df['equity'] >= self.trades_df['equity'].iloc[0]),
                         alpha=0.3, color='green', interpolate=True)
        ax1.fill_between(self.trades_df['entry_time'], 
                         self.trades_df['equity'].iloc[0], 
                         self.trades_df['equity'], 
                         where=(self.trades_df['equity'] < self.trades_df['equity'].iloc[0]),
                         alpha=0.3, color='red', interpolate=True)
        
        ax1.set_title(f'Equity Curve - {self.timeframe} Timeframe', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Equity ($)', fontsize=12)
        ax1.legend(loc='best')
        ax1.grid(True, alpha=0.3)
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        
        # Cumulative returns
        ax2.plot(self.trades_df['entry_time'], self.trades_df['cumulative_pnl'], 
                 linewidth=2, color='#A23B72')
        ax2.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        ax2.fill_between(self.trades_df['entry_time'], 0, self.trades_df['cumulative_pnl'],
                         where=(self.trades_df['cumulative_pnl'] >= 0),
                         alpha=0.3, color='green', interpolate=True)
        ax2.fill_between(self.trades_df['entry_time'], 0, self.trades_df['cumulative_pnl'],
                         where=(self.trades_df['cumulative_pnl'] < 0),
                         alpha=0.3, color='red', interpolate=True)
        
        ax2.set_title('Cumulative P&L', fontsize=12, fontweight='bold')
        ax2.set_xlabel('Date', fontsize=12)
        ax2.set_ylabel('Cumulative P&L ($)', fontsize=12)
        ax2.grid(True, alpha=0.3)
        ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        
        plt.tight_layout()
        
        if filename:
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"Saved equity curve to {filename}")
        else:
            plt.savefig(f'{self.output_dir}/equity_curve_{self.timeframe}.png', 
                       dpi=300, bbox_inches='tight')
        plt.close()
        
    def plot_drawdown(self, filename=None):
        """Plot drawdown chart"""
        if len(self.trades_df) == 0:
            print("No trades to plot")
            return
        
        # Calculate drawdown
        running_max = self.trades_df['equity'].expanding().max()
        drawdown = (self.trades_df['equity'] - running_max) / running_max * 100
        
        fig, ax = plt.subplots(figsize=(14, 6))
        
        ax.fill_between(self.trades_df['entry_time'], 0, drawdown, 
                       color='red', alpha=0.3, label='Drawdown')
        ax.plot(self.trades_df['entry_time'], drawdown, color='red', linewidth=2)
        
        ax.set_title(f'Drawdown - {self.timeframe} Timeframe', fontsize=14, fontweight='bold')
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Drawdown (%)', fontsize=12)
        ax.legend(loc='lower left')
        ax.grid(True, alpha=0.3)
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        
        # Add max drawdown line
        max_dd = drawdown.min()
        ax.axhline(y=max_dd, color='darkred', linestyle='--', alpha=0.7,
                  label=f'Max Drawdown: {max_dd:.2f}%')
        ax.legend(loc='lower left')
        
        plt.tight_layout()
        
        if filename:
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"Saved drawdown chart to {filename}")
        else:
            plt.savefig(f'{self.output_dir}/drawdown_{self.timeframe}.png', 
                       dpi=300, bbox_inches='tight')
        plt.close()
        
    def plot_trade_distribution(self, filename=None):
        """Plot distribution of winning/losing trades"""
        if len(self.trades_df) == 0:
            print("No trades to plot")
            return
        
        fig = plt.figure(figsize=(16, 10))
        gs = GridSpec(2, 2, figure=fig)
        
        # 1. P&L Distribution
        ax1 = fig.add_subplot(gs[0, 0])
        wins = self.trades_df[self.trades_df['pnl'] > 0]['pnl']
        losses = self.trades_df[self.trades_df['pnl'] < 0]['pnl']
        
        ax1.hist(wins, bins=30, alpha=0.7, color='green', label='Wins', edgecolor='black')
        ax1.hist(losses, bins=30, alpha=0.7, color='red', label='Losses', edgecolor='black')
        ax1.axvline(x=0, color='black', linestyle='--', alpha=0.5)
        ax1.set_title('P&L Distribution', fontsize=12, fontweight='bold')
        ax1.set_xlabel('P&L ($)', fontsize=10)
        ax1.set_ylabel('Frequency', fontsize=10)
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 2. Return % Distribution
        ax2 = fig.add_subplot(gs[0, 1])
        ax2.hist(self.trades_df['return_pct'], bins=50, alpha=0.7, 
                color='#2E86AB', edgecolor='black')
        ax2.axvline(x=0, color='black', linestyle='--', alpha=0.5)
        ax2.axvline(x=self.trades_df['return_pct'].mean(), color='red', 
                   linestyle='--', alpha=0.7, label=f"Mean: {self.trades_df['return_pct'].mean():.2f}%")
        ax2.set_title('Return % Distribution', fontsize=12, fontweight='bold')
        ax2.set_xlabel('Return (%)', fontsize=10)
        ax2.set_ylabel('Frequency', fontsize=10)
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # 3. Win/Loss by Exit Reason
        ax3 = fig.add_subplot(gs[1, 0])
        exit_reasons = self.trades_df['exit_reason'].value_counts()
        colors = {'TP': 'green', 'SL': 'red', 'EOD': 'orange'}
        bars = ax3.bar(exit_reasons.index, exit_reasons.values, 
                      color=[colors.get(x, 'gray') for x in exit_reasons.index],
                      edgecolor='black', alpha=0.7)
        ax3.set_title('Trades by Exit Reason', fontsize=12, fontweight='bold')
        ax3.set_xlabel('Exit Reason', fontsize=10)
        ax3.set_ylabel('Count', fontsize=10)
        ax3.grid(True, alpha=0.3, axis='y')
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}',
                    ha='center', va='bottom', fontsize=10)
        
        # 4. Long vs Short Performance
        ax4 = fig.add_subplot(gs[1, 1])
        direction_pnl = self.trades_df.groupby('direction')['pnl'].sum()
        colors_dir = {'Long': 'green', 'Short': 'red'}
        bars = ax4.bar(direction_pnl.index, direction_pnl.values,
                      color=[colors_dir.get(x, 'gray') for x in direction_pnl.index],
                      edgecolor='black', alpha=0.7)
        ax4.set_title('P&L by Direction', fontsize=12, fontweight='bold')
        ax4.set_xlabel('Direction', fontsize=10)
        ax4.set_ylabel('Total P&L ($)', fontsize=10)
        ax4.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        ax4.grid(True, alpha=0.3, axis='y')
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width()/2., height,
                    f'${height:.2f}',
                    ha='center', va='bottom' if height > 0 else 'top', fontsize=10)
        
        plt.suptitle(f'Trade Distribution Analysis - {self.timeframe} Timeframe', 
                    fontsize=14, fontweight='bold', y=0.995)
        plt.tight_layout()
        
        if filename:
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"Saved trade distribution to {filename}")
        else:
            plt.savefig(f'{self.output_dir}/trade_distribution_{self.timeframe}.png', 
                       dpi=300, bbox_inches='tight')
        plt.close()
        
    def plot_performance_heatmap(self, filename=None):
        """Plot monthly performance heatmap"""
        if len(self.trades_df) == 0:
            print("No trades to plot")
            return
        
        df = self.trades_df.copy()
        df['year'] = pd.to_datetime(df['entry_time']).dt.year
        df['month'] = pd.to_datetime(df['entry_time']).dt.month
        
        # Create pivot table for monthly P&L
        monthly_pnl = df.groupby(['year', 'month'])['pnl'].sum().reset_index()
        pivot = monthly_pnl.pivot(index='year', columns='month', values='pnl')
        
        # Create figure
        fig, ax = plt.subplots(figsize=(14, 8))
        
        # Create heatmap
        sns.heatmap(pivot, annot=True, fmt='.0f', cmap='RdYlGn', center=0,
                   cbar_kws={'label': 'P&L ($)'}, linewidths=0.5, ax=ax)
        
        ax.set_title(f'Monthly Performance Heatmap - {self.timeframe} Timeframe', 
                    fontsize=14, fontweight='bold')
        ax.set_xlabel('Month', fontsize=12)
        ax.set_ylabel('Year', fontsize=12)
        
        # Set month labels
        month_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                       'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        ax.set_xticklabels(month_labels, rotation=0)
        
        plt.tight_layout()
        
        if filename:
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"Saved performance heatmap to {filename}")
        else:
            plt.savefig(f'{self.output_dir}/performance_heatmap_{self.timeframe}.png', 
                       dpi=300, bbox_inches='tight')
        plt.close()
        
    def create_all_visualizations(self):
        """Create all visualizations"""
        print(f"\nGenerating visualizations for {self.timeframe}...")
        
        self.plot_equity_curve()
        self.plot_drawdown()
        self.plot_trade_distribution()
        self.plot_performance_heatmap()
        
        print(f"All visualizations saved to {self.output_dir}/")

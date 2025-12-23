"""
Visualization module for displaying backtest results.
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
import numpy as np
from datetime import datetime


class Visualizer:
    """Creates charts for backtest analysis."""
    
    def __init__(self):
        self.fig = None
        self.axes = None
    
    def plot_equity_curve(self, trades, initial_capital, filename='equity_curve.png'):
        """
        Plot the equity curve over time.
        
        Args:
            trades: List of Trade objects
            initial_capital: Starting capital
            filename: Output filename for the chart
        """
        if not trades:
            print("No trades to plot equity curve.")
            return
        
        trades_df = pd.DataFrame([t.to_dict() for t in trades])
        
        # Calculate cumulative P&L
        trades_df['cumulative_pnl'] = trades_df['pnl'].cumsum()
        trades_df['equity'] = initial_capital + trades_df['cumulative_pnl']
        
        # Create figure
        fig, ax = plt.subplots(figsize=(14, 7))
        
        # Plot equity curve
        ax.plot(trades_df['exit_datetime'], trades_df['equity'], linewidth=2, color='blue', label='Equity')
        ax.axhline(y=initial_capital, color='gray', linestyle='--', label='Initial Capital')
        
        # Mark winning and losing trades
        wins = trades_df[trades_df['pnl'] > 0]
        losses = trades_df[trades_df['pnl'] < 0]
        
        ax.scatter(wins['exit_datetime'], wins['equity'], color='green', s=50, alpha=0.6, label='Winning Trades')
        ax.scatter(losses['exit_datetime'], losses['equity'], color='red', s=50, alpha=0.6, label='Losing Trades')
        
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Equity ($)', fontsize=12)
        ax.set_title('Equity Curve', fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(filename, dpi=150)
        print(f"Equity curve saved to {filename}")
        plt.close()
    
    def plot_trade_distribution(self, trades, filename='trade_distribution.png'):
        """
        Plot distribution of trade P&L.
        
        Args:
            trades: List of Trade objects
            filename: Output filename for the chart
        """
        if not trades:
            print("No trades to plot distribution.")
            return
        
        trades_df = pd.DataFrame([t.to_dict() for t in trades])
        
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        # P&L Distribution
        ax1 = axes[0, 0]
        ax1.hist(trades_df['pnl'], bins=30, color='steelblue', edgecolor='black', alpha=0.7)
        ax1.axvline(x=0, color='red', linestyle='--', linewidth=2)
        ax1.set_xlabel('P&L ($)', fontsize=10)
        ax1.set_ylabel('Frequency', fontsize=10)
        ax1.set_title('P&L Distribution', fontsize=12, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        
        # Win/Loss Ratio
        ax2 = axes[0, 1]
        win_count = len(trades_df[trades_df['pnl'] > 0])
        loss_count = len(trades_df[trades_df['pnl'] < 0])
        ax2.bar(['Wins', 'Losses'], [win_count, loss_count], color=['green', 'red'], alpha=0.7)
        ax2.set_ylabel('Number of Trades', fontsize=10)
        ax2.set_title('Win/Loss Count', fontsize=12, fontweight='bold')
        ax2.grid(True, alpha=0.3, axis='y')
        
        # Cumulative P&L
        ax3 = axes[1, 0]
        cumulative_pnl = trades_df['pnl'].cumsum()
        ax3.plot(range(len(cumulative_pnl)), cumulative_pnl, linewidth=2, color='purple')
        ax3.axhline(y=0, color='gray', linestyle='--')
        ax3.set_xlabel('Trade Number', fontsize=10)
        ax3.set_ylabel('Cumulative P&L ($)', fontsize=10)
        ax3.set_title('Cumulative P&L by Trade', fontsize=12, fontweight='bold')
        ax3.grid(True, alpha=0.3)
        
        # Trade Type Distribution
        ax4 = axes[1, 1]
        long_count = len(trades_df[trades_df['position_type'] == 'long'])
        short_count = len(trades_df[trades_df['position_type'] == 'short'])
        ax4.bar(['Long', 'Short'], [long_count, short_count], color=['blue', 'orange'], alpha=0.7)
        ax4.set_ylabel('Number of Trades', fontsize=10)
        ax4.set_title('Long vs Short Trades', fontsize=12, fontweight='bold')
        ax4.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        plt.savefig(filename, dpi=150)
        print(f"Trade distribution saved to {filename}")
        plt.close()
    
    def plot_sample_trades(self, df, trades, num_trades=5, filename='sample_trades.png'):
        """
        Plot a sample of trades with entry/exit points and FVG zones.
        
        Args:
            df: DataFrame with OHLC data
            trades: List of Trade objects
            num_trades: Number of trades to plot
            filename: Output filename for the chart
        """
        if not trades:
            print("No trades to plot.")
            return
        
        # Select a sample of trades
        sample_trades = trades[:min(num_trades, len(trades))]
        
        fig, axes = plt.subplots(num_trades, 1, figsize=(16, 4*num_trades))
        
        if num_trades == 1:
            axes = [axes]
        
        for idx, trade in enumerate(sample_trades):
            ax = axes[idx]
            
            # Get data around the trade
            entry_idx = df[df['datetime'] == trade.entry_datetime].index[0]
            exit_idx = df[df['datetime'] == trade.exit_datetime].index[0] if trade.exit_datetime else entry_idx + 50
            
            # Expand window to show context
            start_idx = max(0, entry_idx - 20)
            end_idx = min(len(df), exit_idx + 20)
            
            trade_df = df.iloc[start_idx:end_idx].copy()
            trade_df['x'] = range(len(trade_df))
            
            # Plot candlesticks
            for i, row in trade_df.iterrows():
                color = 'green' if row['close'] > row['open'] else 'red'
                x = trade_df.loc[i, 'x']
                
                # Draw candle body
                ax.plot([x, x], [row['low'], row['high']], color=color, linewidth=1)
                body_height = abs(row['close'] - row['open'])
                body_bottom = min(row['open'], row['close'])
                rect = mpatches.Rectangle((x-0.3, body_bottom), 0.6, body_height, 
                                         linewidth=1, edgecolor=color, facecolor=color, alpha=0.7)
                ax.add_patch(rect)
            
            # Mark entry point
            entry_x = trade_df[trade_df['datetime'] == trade.entry_datetime]['x'].values[0]
            ax.scatter([entry_x], [trade.entry_price], color='blue', s=200, marker='^', 
                      zorder=5, label='Entry')
            
            # Mark exit point if available
            if trade.exit_datetime:
                exit_mask = trade_df['datetime'] == trade.exit_datetime
                if exit_mask.any():
                    exit_x = trade_df[exit_mask]['x'].values[0]
                    exit_color = 'green' if trade.pnl > 0 else 'red'
                    ax.scatter([exit_x], [trade.exit_price], color=exit_color, s=200, marker='v', 
                              zorder=5, label='Exit')
            
            # Draw stop loss and take profit lines
            ax.axhline(y=trade.stop_loss, color='red', linestyle='--', linewidth=2, 
                      alpha=0.7, label='Stop Loss')
            ax.axhline(y=trade.take_profit, color='green', linestyle='--', linewidth=2, 
                      alpha=0.7, label='Take Profit')
            
            # Title with trade info
            pnl_color = 'green' if trade.pnl > 0 else 'red'
            ax.set_title(f"Trade {idx+1}: {trade.position_type.upper()} | "
                        f"Entry: ${trade.entry_price:.2f} | Exit: ${trade.exit_price:.2f} | "
                        f"P&L: ${trade.pnl:.2f} ({trade.exit_reason})", 
                        fontsize=11, fontweight='bold', color=pnl_color)
            
            ax.set_ylabel('Price', fontsize=10)
            ax.legend(loc='upper left', fontsize=8)
            ax.grid(True, alpha=0.3)
            
            # Remove x-axis labels
            ax.set_xticks([])
        
        plt.tight_layout()
        plt.savefig(filename, dpi=150)
        print(f"Sample trades chart saved to {filename}")
        plt.close()
    
    def plot_monthly_returns(self, trades, filename='monthly_returns.png'):
        """
        Plot monthly returns.
        
        Args:
            trades: List of Trade objects
            filename: Output filename for the chart
        """
        if not trades:
            print("No trades to plot monthly returns.")
            return
        
        trades_df = pd.DataFrame([t.to_dict() for t in trades])
        trades_df['exit_datetime'] = pd.to_datetime(trades_df['exit_datetime'])
        trades_df['year_month'] = trades_df['exit_datetime'].dt.to_period('M')
        
        # Group by month
        monthly_pnl = trades_df.groupby('year_month')['pnl'].sum()
        
        fig, ax = plt.subplots(figsize=(14, 7))
        
        # Plot bars
        colors = ['green' if pnl > 0 else 'red' for pnl in monthly_pnl.values]
        ax.bar(range(len(monthly_pnl)), monthly_pnl.values, color=colors, alpha=0.7)
        
        # Set labels
        ax.set_xticks(range(len(monthly_pnl)))
        ax.set_xticklabels([str(period) for period in monthly_pnl.index], rotation=45, ha='right')
        ax.set_xlabel('Month', fontsize=12)
        ax.set_ylabel('P&L ($)', fontsize=12)
        ax.set_title('Monthly Returns', fontsize=14, fontweight='bold')
        ax.axhline(y=0, color='black', linestyle='-', linewidth=1)
        ax.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        plt.savefig(filename, dpi=150)
        print(f"Monthly returns saved to {filename}")
        plt.close()

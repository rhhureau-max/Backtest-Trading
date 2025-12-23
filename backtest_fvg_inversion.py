"""
FVG Inversion Backtesting Script for NQ Futures 5-Minute Data

This script implements a Fair Value Gap (FVG) inversion strategy with the following rules:
1. Identify the first FVG during the 02:00-06:00 session
2. Wait for price to invert (close beyond the FVG zone)
3. Enter trade on signal candle close
4. Use swing high/low for stop loss and 1:1 R:R for take profit
5. Maximum one trade per day
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import glob
from datetime import datetime, time


class FVGInversionBacktest:
    """Backtesting engine for FVG Inversion strategy"""
    
    def __init__(self, data_dir='.'):
        self.data_dir = data_dir
        self.df = None
        self.trades = []
        
    def load_data(self):
        """Load and concatenate all 5-minute CSV files"""
        print("Loading data files...")
        
        # Find all yearly 5m CSV files
        csv_files = sorted(glob.glob(f"{self.data_dir}/[0-9][0-9][0-9][0-9] 5m.csv"))
        
        if not csv_files:
            raise FileNotFoundError("No 5-minute CSV files found!")
        
        print(f"Found {len(csv_files)} files: {[Path(f).name for f in csv_files]}")
        
        # Load and concatenate all files
        dfs = []
        for file in csv_files:
            df = pd.read_csv(
                file,
                sep=';',
                header=0,
                names=['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
            )
            dfs.append(df)
        
        # Concatenate all dataframes
        self.df = pd.concat(dfs, ignore_index=True)
        
        # Parse datetime - NO timezone conversion, keep as-is
        self.df['DateTime'] = pd.to_datetime(
            self.df['Date'] + ' ' + self.df['Time'],
            format='%d/%m/%Y %H:%M:%S'
        )
        
        # Extract time and date components
        self.df['TimeOnly'] = self.df['DateTime'].dt.time
        self.df['DateOnly'] = self.df['DateTime'].dt.date
        
        # Convert OHLC to numeric
        for col in ['Open', 'High', 'Low', 'Close']:
            self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
        
        # Drop any rows with NaN values
        self.df.dropna(subset=['Open', 'High', 'Low', 'Close'], inplace=True)
        
        # Sort by datetime
        self.df.sort_values('DateTime', inplace=True)
        self.df.reset_index(drop=True, inplace=True)
        
        print(f"Loaded {len(self.df)} candles from {self.df['DateTime'].min()} to {self.df['DateTime'].max()}")
        
        return self.df
    
    def detect_fvg(self, i):
        """
        Detect Fair Value Gap at index i
        Returns: ('bullish', gap_low, gap_high) or ('bearish', gap_low, gap_high) or None
        
        Bullish FVG: High[i-2] < Low[i] -> Gap is [High[i-2], Low[i]]
        Bearish FVG: Low[i-2] > High[i] -> Gap is [High[i], Low[i-2]]
        """
        if i < 2:
            return None
        
        high_i_minus_2 = self.df.loc[i-2, 'High']
        low_i_minus_2 = self.df.loc[i-2, 'Low']
        high_i = self.df.loc[i, 'High']
        low_i = self.df.loc[i, 'Low']
        
        # Bullish FVG
        if high_i_minus_2 < low_i:
            return ('bullish', high_i_minus_2, low_i)
        
        # Bearish FVG
        if low_i_minus_2 > high_i:
            return ('bearish', high_i, low_i_minus_2)
        
        return None
    
    def get_swing_low(self, i, lookback=5):
        """Get the lowest low of the last 'lookback' candles"""
        start_idx = max(0, i - lookback + 1)
        return self.df.loc[start_idx:i, 'Low'].min()
    
    def get_swing_high(self, i, lookback=5):
        """Get the highest high of the last 'lookback' candles"""
        start_idx = max(0, i - lookback + 1)
        return self.df.loc[start_idx:i, 'High'].max()
    
    def run_backtest(self):
        """Execute the backtest strategy"""
        print("\nRunning backtest...")
        
        if self.df is None or len(self.df) == 0:
            raise ValueError("No data loaded. Call load_data() first.")
        
        # Session times
        session_start = time(2, 0)  # 02:00
        session_end = time(6, 0)    # 06:00
        
        # State variables
        current_date = None
        session_fvg = None  # Store the first FVG of the session
        session_fvg_type = None
        in_position = False
        position_type = None  # 'long' or 'short'
        entry_price = None
        stop_loss = None
        take_profit = None
        entry_index = None
        
        for i in range(2, len(self.df)):
            current_time = self.df.loc[i, 'TimeOnly']
            current_date_value = self.df.loc[i, 'DateOnly']
            close_price = self.df.loc[i, 'Close']
            high_price = self.df.loc[i, 'High']
            low_price = self.df.loc[i, 'Low']
            
            # Check if we're in a new trading day
            if current_date != current_date_value:
                current_date = current_date_value
                # Reset session state for new day
                session_fvg = None
                session_fvg_type = None
            
            # Reset session at 02:00
            if current_time == session_start:
                session_fvg = None
                session_fvg_type = None
            
            # Manage existing position (check for SL/TP hit)
            if in_position:
                # Check if stop loss or take profit hit
                if position_type == 'long':
                    if low_price <= stop_loss:
                        # Stop loss hit
                        exit_price = stop_loss
                        pnl = exit_price - entry_price
                        self.trades.append({
                            'entry_time': self.df.loc[entry_index, 'DateTime'],
                            'exit_time': self.df.loc[i, 'DateTime'],
                            'type': position_type,
                            'entry_price': entry_price,
                            'exit_price': exit_price,
                            'stop_loss': stop_loss,
                            'take_profit': take_profit,
                            'pnl': pnl,
                            'result': 'loss'
                        })
                        in_position = False
                    elif high_price >= take_profit:
                        # Take profit hit
                        exit_price = take_profit
                        pnl = exit_price - entry_price
                        self.trades.append({
                            'entry_time': self.df.loc[entry_index, 'DateTime'],
                            'exit_time': self.df.loc[i, 'DateTime'],
                            'type': position_type,
                            'entry_price': entry_price,
                            'exit_price': exit_price,
                            'stop_loss': stop_loss,
                            'take_profit': take_profit,
                            'pnl': pnl,
                            'result': 'win'
                        })
                        in_position = False
                
                elif position_type == 'short':
                    if high_price >= stop_loss:
                        # Stop loss hit
                        exit_price = stop_loss
                        pnl = entry_price - exit_price
                        self.trades.append({
                            'entry_time': self.df.loc[entry_index, 'DateTime'],
                            'exit_time': self.df.loc[i, 'DateTime'],
                            'type': position_type,
                            'entry_price': entry_price,
                            'exit_price': exit_price,
                            'stop_loss': stop_loss,
                            'take_profit': take_profit,
                            'pnl': pnl,
                            'result': 'loss'
                        })
                        in_position = False
                    elif low_price <= take_profit:
                        # Take profit hit
                        exit_price = take_profit
                        pnl = entry_price - exit_price
                        self.trades.append({
                            'entry_time': self.df.loc[entry_index, 'DateTime'],
                            'exit_time': self.df.loc[i, 'DateTime'],
                            'type': position_type,
                            'entry_price': entry_price,
                            'exit_price': exit_price,
                            'stop_loss': stop_loss,
                            'take_profit': take_profit,
                            'pnl': pnl,
                            'result': 'win'
                        })
                        in_position = False
            
            # Only look for setups during session hours and if not in position
            if not in_position and session_start <= current_time < session_end:
                # Look for first FVG of the session if we don't have one yet
                if session_fvg is None:
                    fvg = self.detect_fvg(i)
                    if fvg is not None:
                        session_fvg_type, gap_low, gap_high = fvg
                        session_fvg = (gap_low, gap_high)
                        # print(f"FVG detected on {current_date_value} at {current_time}: {session_fvg_type} [{gap_low:.2f}, {gap_high:.2f}]")
                
                # Check for inversion signal
                if session_fvg is not None:
                    gap_low, gap_high = session_fvg
                    
                    # Long Signal: Bearish FVG exists, candle closes above gap top
                    if session_fvg_type == 'bearish' and close_price > gap_high:
                        # Enter long
                        entry_price = close_price
                        stop_loss = self.get_swing_low(i, lookback=5)
                        risk = entry_price - stop_loss
                        take_profit = entry_price + risk  # 1:1 R:R
                        
                        in_position = True
                        position_type = 'long'
                        entry_index = i
                        
                        # print(f"LONG entry on {self.df.loc[i, 'DateTime']}: Entry={entry_price:.2f}, SL={stop_loss:.2f}, TP={take_profit:.2f}")
                    
                    # Short Signal: Bullish FVG exists, candle closes below gap bottom
                    elif session_fvg_type == 'bullish' and close_price < gap_low:
                        # Enter short
                        entry_price = close_price
                        stop_loss = self.get_swing_high(i, lookback=5)
                        risk = stop_loss - entry_price
                        take_profit = entry_price - risk  # 1:1 R:R
                        
                        in_position = True
                        position_type = 'short'
                        entry_index = i
                        
                        # print(f"SHORT entry on {self.df.loc[i, 'DateTime']}: Entry={entry_price:.2f}, SL={stop_loss:.2f}, TP={take_profit:.2f}")
        
        print(f"Backtest complete. Total trades: {len(self.trades)}")
        return self.trades
    
    def calculate_metrics(self):
        """Calculate performance metrics"""
        if not self.trades:
            print("No trades executed!")
            return None
        
        trades_df = pd.DataFrame(self.trades)
        
        total_trades = len(trades_df)
        wins = len(trades_df[trades_df['result'] == 'win'])
        losses = len(trades_df[trades_df['result'] == 'loss'])
        win_rate = (wins / total_trades * 100) if total_trades > 0 else 0
        
        total_pnl = trades_df['pnl'].sum()
        avg_win = trades_df[trades_df['result'] == 'win']['pnl'].mean() if wins > 0 else 0
        avg_loss = trades_df[trades_df['result'] == 'loss']['pnl'].mean() if losses > 0 else 0
        
        # Calculate equity curve
        trades_df['cumulative_pnl'] = trades_df['pnl'].cumsum()
        
        # Calculate max drawdown
        running_max = trades_df['cumulative_pnl'].cummax()
        drawdown = trades_df['cumulative_pnl'] - running_max
        max_drawdown = drawdown.min()
        
        metrics = {
            'Total Trades': total_trades,
            'Wins': wins,
            'Losses': losses,
            'Win Rate (%)': win_rate,
            'Net Profit': total_pnl,
            'Average Win': avg_win,
            'Average Loss': avg_loss,
            'Max Drawdown': max_drawdown,
            'Profit Factor': abs(trades_df[trades_df['pnl'] > 0]['pnl'].sum() / 
                                trades_df[trades_df['pnl'] < 0]['pnl'].sum()) if losses > 0 and trades_df[trades_df['pnl'] < 0]['pnl'].sum() != 0 else float('inf')
        }
        
        return metrics, trades_df
    
    def print_metrics(self):
        """Print performance metrics"""
        if not self.trades:
            print("\nNo trades to analyze!")
            return
        
        metrics, trades_df = self.calculate_metrics()
        
        print("\n" + "="*60)
        print("BACKTEST RESULTS")
        print("="*60)
        print(f"Total Trades:       {metrics['Total Trades']}")
        print(f"Wins:               {metrics['Wins']}")
        print(f"Losses:             {metrics['Losses']}")
        print(f"Win Rate:           {metrics['Win Rate (%)']:.2f}%")
        print(f"Net Profit:         ${metrics['Net Profit']:.2f}")
        print(f"Average Win:        ${metrics['Average Win']:.2f}")
        print(f"Average Loss:       ${metrics['Average Loss']:.2f}")
        print(f"Max Drawdown:       ${metrics['Max Drawdown']:.2f}")
        print(f"Profit Factor:      {metrics['Profit Factor']:.2f}")
        print("="*60)
        
        return metrics, trades_df
    
    def plot_equity_curve(self):
        """Plot the cumulative returns"""
        if not self.trades:
            print("No trades to plot!")
            return
        
        _, trades_df = self.calculate_metrics()
        
        plt.figure(figsize=(14, 7))
        
        # Plot equity curve
        plt.subplot(2, 1, 1)
        plt.plot(trades_df['exit_time'], trades_df['cumulative_pnl'], linewidth=2, color='blue')
        plt.title('Equity Curve - FVG Inversion Strategy', fontsize=14, fontweight='bold')
        plt.xlabel('Date')
        plt.ylabel('Cumulative P&L ($)')
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        
        # Plot individual trade results
        plt.subplot(2, 1, 2)
        colors = ['green' if result == 'win' else 'red' for result in trades_df['result']]
        plt.bar(range(len(trades_df)), trades_df['pnl'], color=colors, alpha=0.6)
        plt.title('Individual Trade Results', fontsize=14, fontweight='bold')
        plt.xlabel('Trade Number')
        plt.ylabel('P&L ($)')
        plt.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('equity_curve.png', dpi=300, bbox_inches='tight')
        print("\nEquity curve saved as 'equity_curve.png'")
        plt.show()
    
    def export_trades(self, filename='trades.csv'):
        """Export trades to CSV file"""
        if not self.trades:
            print("No trades to export!")
            return
        
        trades_df = pd.DataFrame(self.trades)
        trades_df.to_csv(filename, index=False)
        print(f"\nTrades exported to '{filename}'")


def main():
    """Main execution function"""
    print("="*60)
    print("FVG INVERSION BACKTEST")
    print("="*60)
    
    # Initialize backtest
    bt = FVGInversionBacktest(data_dir='/home/runner/work/Backtest-Trading/Backtest-Trading')
    
    # Load data
    bt.load_data()
    
    # Run backtest
    bt.run_backtest()
    
    # Print metrics
    bt.print_metrics()
    
    # Plot equity curve
    bt.plot_equity_curve()
    
    # Export trades
    bt.export_trades()


if __name__ == "__main__":
    main()

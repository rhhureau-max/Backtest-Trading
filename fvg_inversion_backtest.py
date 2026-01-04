"""
FVG Inversion Strategy Backtest for Nasdaq (NQ) - 5 Minutes
============================================================

Strategy: FVG Inversion with London Killzone Time Filter
Timeframe: 5 minutes
Period: 2018 to 2025
Starting Capital: $100,000
Time Filter: London Killzone (01:00 to 04:00 Chicago time)

Author: Backtest Trading System
Date: 2026-01-04
"""

import pandas as pd
import numpy as np
from datetime import datetime, time
import os
from typing import List, Tuple, Optional

class FVGInversionBacktest:
    """
    Backtest implementation for FVG (Fair Value Gap) Inversion strategy
    """
    
    def __init__(self, initial_capital: float = 100000):
        self.initial_capital = initial_capital
        self.capital = initial_capital
        self.trades = []
        self.equity_curve = []
        self.position = None  # Current open position
        self.active_fvgs = {'bullish': [], 'bearish': []}  # Track recent FVGs
        
    def load_data(self, file_paths: List[str]) -> pd.DataFrame:
        """
        Load and combine multiple CSV files
        
        Args:
            file_paths: List of CSV file paths
            
        Returns:
            Combined DataFrame with all data
        """
        dfs = []
        
        for file_path in file_paths:
            if not os.path.exists(file_path):
                print(f"Warning: File not found - {file_path}")
                continue
                
            # Read CSV with semicolon separator
            df = pd.read_csv(file_path, sep=';')
            
            # Rename columns for easier access
            df.columns = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
            
            # Combine Date and Time into datetime (flexible parsing)
            df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], 
                                           format='mixed', dayfirst=False)
            
            # Keep only necessary columns
            df = df[['Datetime', 'Open', 'High', 'Low', 'Close', 'Volume']]
            
            dfs.append(df)
            print(f"Loaded {len(df)} rows from {os.path.basename(file_path)}")
        
        # Combine all dataframes
        combined_df = pd.concat(dfs, ignore_index=True)
        
        # Sort by datetime
        combined_df = combined_df.sort_values('Datetime').reset_index(drop=True)
        
        # Remove duplicates if any
        combined_df = combined_df.drop_duplicates(subset=['Datetime']).reset_index(drop=True)
        
        print(f"\nTotal rows after combining: {len(combined_df)}")
        print(f"Date range: {combined_df['Datetime'].min()} to {combined_df['Datetime'].max()}")
        
        return combined_df
    
    def is_london_killzone(self, dt: datetime) -> bool:
        """
        Check if the time is within London Killzone (01:00 to 04:00 Chicago time)
        
        Args:
            dt: Datetime to check
            
        Returns:
            True if within London Killzone, False otherwise
        """
        hour = dt.hour
        return 1 <= hour <= 4
    
    def identify_fvg(self, df: pd.DataFrame, i: int) -> Optional[dict]:
        """
        Identify FVG (Fair Value Gap) at position i
        
        Args:
            df: DataFrame with OHLC data
            i: Current index
            
        Returns:
            Dict with FVG info or None if no FVG
        """
        if i < 2:
            return None
        
        # Get the three candles needed
        low_i_minus_2 = df.loc[i-2, 'Low']
        high_i_minus_2 = df.loc[i-2, 'High']
        high_i = df.loc[i, 'High']
        low_i = df.loc[i, 'Low']
        
        # Bearish FVG: Low[i-2] > High[i]
        if low_i_minus_2 > high_i:
            return {
                'type': 'bearish',
                'top': low_i_minus_2,
                'bottom': high_i,
                'created_at': i,
                'datetime': df.loc[i, 'Datetime']
            }
        
        # Bullish FVG: High[i-2] < Low[i]
        if high_i_minus_2 < low_i:
            return {
                'type': 'bullish',
                'top': low_i,
                'bottom': high_i_minus_2,
                'created_at': i,
                'datetime': df.loc[i, 'Datetime']
            }
        
        return None
    
    def check_long_entry(self, df: pd.DataFrame, i: int) -> Optional[dict]:
        """
        Check for LONG entry signal (inversion of bearish FVG)
        
        Args:
            df: DataFrame with OHLC data
            i: Current index
            
        Returns:
            Entry signal dict or None
        """
        if not self.active_fvgs['bearish']:
            return None
        
        close = df.loc[i, 'Close']
        
        # Check each active bearish FVG
        for fvg in self.active_fvgs['bearish']:
            # If close is above the top of the bearish FVG (inversion)
            if close > fvg['top']:
                return {
                    'type': 'LONG',
                    'entry_price': close,
                    'entry_index': i,
                    'entry_datetime': df.loc[i, 'Datetime'],
                    'stop_loss': df.loc[i, 'Low'],  # Below the signal candle's low
                    'fvg': fvg
                }
        
        return None
    
    def check_short_entry(self, df: pd.DataFrame, i: int) -> Optional[dict]:
        """
        Check for SHORT entry signal (inversion of bullish FVG)
        
        Args:
            df: DataFrame with OHLC data
            i: Current index
            
        Returns:
            Entry signal dict or None
        """
        if not self.active_fvgs['bullish']:
            return None
        
        close = df.loc[i, 'Close']
        
        # Check each active bullish FVG
        for fvg in self.active_fvgs['bullish']:
            # If close is below the bottom of the bullish FVG (inversion)
            if close < fvg['bottom']:
                return {
                    'type': 'SHORT',
                    'entry_price': close,
                    'entry_index': i,
                    'entry_datetime': df.loc[i, 'Datetime'],
                    'stop_loss': df.loc[i, 'High'],  # Above the signal candle's high
                    'fvg': fvg
                }
        
        return None
    
    def manage_position(self, df: pd.DataFrame, i: int) -> Optional[dict]:
        """
        Manage open position - check for SL or TP hit
        
        Args:
            df: DataFrame with OHLC data
            i: Current index
            
        Returns:
            Exit info dict or None if position still open
        """
        if not self.position:
            return None
        
        high = df.loc[i, 'High']
        low = df.loc[i, 'Low']
        
        if self.position['type'] == 'LONG':
            # Check Stop Loss
            if low <= self.position['stop_loss']:
                return {
                    'exit_price': self.position['stop_loss'],
                    'exit_reason': 'Stop Loss',
                    'exit_datetime': df.loc[i, 'Datetime'],
                    'exit_index': i
                }
            
            # Check Take Profit
            if high >= self.position['take_profit']:
                return {
                    'exit_price': self.position['take_profit'],
                    'exit_reason': 'Take Profit',
                    'exit_datetime': df.loc[i, 'Datetime'],
                    'exit_index': i
                }
        
        elif self.position['type'] == 'SHORT':
            # Check Stop Loss
            if high >= self.position['stop_loss']:
                return {
                    'exit_price': self.position['stop_loss'],
                    'exit_reason': 'Stop Loss',
                    'exit_datetime': df.loc[i, 'Datetime'],
                    'exit_index': i
                }
            
            # Check Take Profit
            if low <= self.position['take_profit']:
                return {
                    'exit_price': self.position['take_profit'],
                    'exit_reason': 'Take Profit',
                    'exit_datetime': df.loc[i, 'Datetime'],
                    'exit_index': i
                }
        
        return None
    
    def calculate_position_size(self, risk_amount: float) -> float:
        """
        Calculate position size based on risk
        For simplicity, using 1 contract per trade
        
        Args:
            risk_amount: Amount risked per trade
            
        Returns:
            Position size (contracts)
        """
        return 1.0  # Fixed 1 contract per trade for NQ futures
    
    def open_position(self, signal: dict, df: pd.DataFrame) -> None:
        """
        Open a new position based on entry signal
        
        Args:
            signal: Entry signal dict
            df: DataFrame with OHLC data
        """
        entry_price = signal['entry_price']
        stop_loss = signal['stop_loss']
        
        # Calculate risk per contract
        if signal['type'] == 'LONG':
            risk_per_contract = entry_price - stop_loss
            take_profit = entry_price + risk_per_contract  # 1:1 RR
        else:  # SHORT
            risk_per_contract = stop_loss - entry_price
            take_profit = entry_price - risk_per_contract  # 1:1 RR
        
        self.position = {
            'type': signal['type'],
            'entry_price': entry_price,
            'stop_loss': stop_loss,
            'take_profit': take_profit,
            'entry_datetime': signal['entry_datetime'],
            'entry_index': signal['entry_index'],
            'contracts': 1.0,
            'risk': risk_per_contract * 20  # NQ multiplier is $20 per point
        }
    
    def close_position(self, exit_info: dict) -> None:
        """
        Close current position and record trade
        
        Args:
            exit_info: Exit information dict
        """
        if not self.position:
            return
        
        entry_price = self.position['entry_price']
        exit_price = exit_info['exit_price']
        contracts = self.position['contracts']
        
        # Calculate PnL (NQ futures: $20 per point)
        if self.position['type'] == 'LONG':
            pnl = (exit_price - entry_price) * 20 * contracts
        else:  # SHORT
            pnl = (entry_price - exit_price) * 20 * contracts
        
        # Update capital
        self.capital += pnl
        
        # Record trade
        trade = {
            'Entry Date': self.position['entry_datetime'].strftime('%Y-%m-%d %H:%M:%S'),
            'Exit Date': exit_info['exit_datetime'].strftime('%Y-%m-%d %H:%M:%S'),
            'Type': self.position['type'],
            'Entry Price': round(entry_price, 2),
            'Exit Price': round(exit_price, 2),
            'Stop Loss': round(self.position['stop_loss'], 2),
            'Take Profit': round(self.position['take_profit'], 2),
            'Exit Reason': exit_info['exit_reason'],
            'PnL': round(pnl, 2),
            'Capital': round(self.capital, 2)
        }
        
        self.trades.append(trade)
        self.equity_curve.append(self.capital)
        
        # Clear position
        self.position = None
    
    def run_backtest(self, df: pd.DataFrame) -> None:
        """
        Run the complete backtest
        
        Args:
            df: DataFrame with OHLC data
        """
        print("\n" + "="*80)
        print("RUNNING BACKTEST...")
        print("="*80)
        
        # Initialize equity curve
        self.equity_curve = [self.initial_capital]
        
        # Main backtest loop
        for i in range(2, len(df)):
            current_dt = df.loc[i, 'Datetime']
            
            # Check if in London Killzone
            in_killzone = self.is_london_killzone(current_dt)
            
            # Manage existing position
            if self.position:
                exit_info = self.manage_position(df, i)
                if exit_info:
                    self.close_position(exit_info)
            
            # Only look for new trades during London Killzone and when no position is open
            if in_killzone and not self.position:
                # Identify new FVG at current candle
                fvg = self.identify_fvg(df, i)
                if fvg:
                    if fvg['type'] == 'bearish':
                        self.active_fvgs['bearish'].append(fvg)
                        # Keep only recent FVGs (last 50 candles)
                        self.active_fvgs['bearish'] = [f for f in self.active_fvgs['bearish'] 
                                                       if i - f['created_at'] <= 50]
                    else:  # bullish
                        self.active_fvgs['bullish'].append(fvg)
                        # Keep only recent FVGs (last 50 candles)
                        self.active_fvgs['bullish'] = [f for f in self.active_fvgs['bullish'] 
                                                       if i - f['created_at'] <= 50]
                
                # Check for entry signals
                long_signal = self.check_long_entry(df, i)
                if long_signal:
                    self.open_position(long_signal, df)
                    # Clear bearish FVGs after entry
                    self.active_fvgs['bearish'] = []
                    continue
                
                short_signal = self.check_short_entry(df, i)
                if short_signal:
                    self.open_position(short_signal, df)
                    # Clear bullish FVGs after entry
                    self.active_fvgs['bullish'] = []
            
            # Track equity even when no trade
            if i % 10000 == 0:
                print(f"Processing: {current_dt} (Row {i}/{len(df)})")
        
        # Close any remaining open position at the end
        if self.position:
            last_index = len(df) - 1
            exit_info = {
                'exit_price': df.loc[last_index, 'Close'],
                'exit_reason': 'End of Data',
                'exit_datetime': df.loc[last_index, 'Datetime'],
                'exit_index': last_index
            }
            self.close_position(exit_info)
        
        print(f"\nBacktest completed! Processed {len(df)} candles.")
    
    def calculate_statistics(self) -> dict:
        """
        Calculate performance statistics
        
        Returns:
            Dictionary with performance metrics
        """
        if not self.trades:
            return {
                'Total Trades': 0,
                'Winning Trades': 0,
                'Losing Trades': 0,
                'Win Rate (%)': 0,
                'Average Win': 0,
                'Average Loss': 0,
                'Profit Factor': 0,
                'Total PnL': 0,
                'Max Drawdown': 0,
                'Max Drawdown (%)': 0,
                'Final Capital': self.capital
            }
        
        # Convert trades to DataFrame for easier analysis
        trades_df = pd.DataFrame(self.trades)
        
        # Basic statistics
        total_trades = len(trades_df)
        winning_trades = len(trades_df[trades_df['PnL'] > 0])
        losing_trades = len(trades_df[trades_df['PnL'] < 0])
        
        win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
        
        # PnL statistics
        total_pnl = trades_df['PnL'].sum()
        avg_win = trades_df[trades_df['PnL'] > 0]['PnL'].mean() if winning_trades > 0 else 0
        avg_loss = trades_df[trades_df['PnL'] < 0]['PnL'].mean() if losing_trades > 0 else 0
        
        # Profit Factor
        gross_profit = trades_df[trades_df['PnL'] > 0]['PnL'].sum()
        gross_loss = abs(trades_df[trades_df['PnL'] < 0]['PnL'].sum())
        profit_factor = gross_profit / gross_loss if gross_loss != 0 else float('inf')
        
        # Max Drawdown
        equity_curve = np.array(self.equity_curve)
        running_max = np.maximum.accumulate(equity_curve)
        drawdown = equity_curve - running_max
        max_drawdown = abs(drawdown.min())
        max_drawdown_pct = (max_drawdown / self.initial_capital * 100) if self.initial_capital > 0 else 0
        
        return {
            'Initial Capital': self.initial_capital,
            'Final Capital': round(self.capital, 2),
            'Total PnL': round(total_pnl, 2),
            'Total Return (%)': round((self.capital - self.initial_capital) / self.initial_capital * 100, 2),
            'Total Trades': total_trades,
            'Winning Trades': winning_trades,
            'Losing Trades': losing_trades,
            'Win Rate (%)': round(win_rate, 2),
            'Average Win': round(avg_win, 2),
            'Average Loss': round(avg_loss, 2),
            'Profit Factor': round(profit_factor, 2),
            'Max Drawdown': round(max_drawdown, 2),
            'Max Drawdown (%)': round(max_drawdown_pct, 2)
        }
    
    def print_results(self) -> None:
        """
        Print backtest results in a formatted way
        """
        stats = self.calculate_statistics()
        
        print("\n" + "="*80)
        print("BACKTEST RESULTS - FVG INVERSION STRATEGY")
        print("="*80)
        print(f"\n{'CAPITAL PERFORMANCE':-^80}")
        print(f"Initial Capital:        ${stats['Initial Capital']:,.2f}")
        print(f"Final Capital:          ${stats['Final Capital']:,.2f}")
        print(f"Total PnL:              ${stats['Total PnL']:,.2f}")
        print(f"Total Return:           {stats['Total Return (%)']:.2f}%")
        
        print(f"\n{'TRADE STATISTICS':-^80}")
        print(f"Total Trades:           {stats['Total Trades']}")
        print(f"Winning Trades:         {stats['Winning Trades']}")
        print(f"Losing Trades:          {stats['Losing Trades']}")
        print(f"Win Rate:               {stats['Win Rate (%)']}%")
        
        print(f"\n{'PERFORMANCE METRICS':-^80}")
        print(f"Average Win:            ${stats['Average Win']:,.2f}")
        print(f"Average Loss:           ${stats['Average Loss']:,.2f}")
        print(f"Profit Factor:          {stats['Profit Factor']:.2f}")
        print(f"Max Drawdown:           ${stats['Max Drawdown']:,.2f}")
        print(f"Max Drawdown (%):       {stats['Max Drawdown (%)']:.2f}%")
        
        print(f"\n{'TRADE LOG (First 20 trades)':-^80}")
        if self.trades:
            trades_df = pd.DataFrame(self.trades)
            print(trades_df.head(20).to_string(index=False))
            
            if len(self.trades) > 20:
                print(f"\n... and {len(self.trades) - 20} more trades")
                print(f"\n{'TRADE LOG (Last 10 trades)':-^80}")
                print(trades_df.tail(10).to_string(index=False))
        else:
            print("No trades executed.")
        
        print("\n" + "="*80)
    
    def export_trades_to_csv(self, filename: str = 'fvg_inversion_trades.csv') -> None:
        """
        Export all trades to CSV file
        
        Args:
            filename: Output CSV filename
        """
        if self.trades:
            trades_df = pd.DataFrame(self.trades)
            trades_df.to_csv(filename, index=False)
            print(f"\nTrades exported to: {filename}")
        else:
            print("\nNo trades to export.")


def main():
    """
    Main function to run the backtest
    """
    print("="*80)
    print("FVG INVERSION STRATEGY BACKTEST")
    print("Nasdaq (NQ) - 5 Minutes - 2018 to 2025")
    print("="*80)
    
    # Define file paths
    base_path = "/home/runner/work/Backtest-Trading/Backtest-Trading"
    file_paths = [
        os.path.join(base_path, "2018 5m.csv"),
        os.path.join(base_path, "2019 5m.csv"),
        os.path.join(base_path, "2020 5m.csv"),
        os.path.join(base_path, "2021 5m.csv"),
        os.path.join(base_path, "2022 5m.csv"),
        os.path.join(base_path, "2023 5m.csv"),
        os.path.join(base_path, "2024 5m.csv"),
        os.path.join(base_path, "2025 5m.csv"),
    ]
    
    # Initialize backtest
    backtest = FVGInversionBacktest(initial_capital=100000)
    
    # Load data
    print("\nLoading data...")
    df = backtest.load_data(file_paths)
    
    # Run backtest
    backtest.run_backtest(df)
    
    # Print results
    backtest.print_results()
    
    # Export trades to CSV
    backtest.export_trades_to_csv('fvg_inversion_trades.csv')


if __name__ == "__main__":
    main()

"""
Backtesting engine for the FVG strategy.
"""
import pandas as pd
import numpy as np
from strategy import FVGStrategy


class Trade:
    """Represents a single trade."""
    
    def __init__(self, entry_datetime, entry_price, position_type, stop_loss, take_profit):
        self.entry_datetime = entry_datetime
        self.entry_price = entry_price
        self.position_type = position_type
        self.stop_loss = stop_loss
        self.take_profit = take_profit
        self.exit_datetime = None
        self.exit_price = None
        self.exit_reason = None
        self.pnl = 0.0
        
    def close_trade(self, exit_datetime, exit_price, exit_reason):
        """Close the trade and calculate P&L."""
        self.exit_datetime = exit_datetime
        self.exit_price = exit_price
        self.exit_reason = exit_reason
        
        if self.position_type == 'long':
            self.pnl = exit_price - self.entry_price
        else:  # short
            self.pnl = self.entry_price - exit_price
        
    def to_dict(self):
        """Convert trade to dictionary for export."""
        return {
            'entry_datetime': self.entry_datetime,
            'entry_price': self.entry_price,
            'position_type': self.position_type,
            'stop_loss': self.stop_loss,
            'take_profit': self.take_profit,
            'exit_datetime': self.exit_datetime,
            'exit_price': self.exit_price,
            'exit_reason': self.exit_reason,
            'pnl': self.pnl,
        }


class Backtest:
    """Backtesting engine for the FVG strategy."""
    
    def __init__(self, strategy, initial_capital=100000):
        """
        Initialize the backtesting engine.
        
        Args:
            strategy: FVGStrategy instance
            initial_capital: Starting capital for the backtest
        """
        self.strategy = strategy
        self.initial_capital = initial_capital
        self.trades = []
        self.equity_curve = []
        
    def run(self, df):
        """
        Run the backtest on the provided data.
        
        Args:
            df: DataFrame with OHLC data, FVG signals, and entry signals
            
        Returns:
            List of Trade objects
        """
        print("\nRunning backtest...")
        
        active_position = None
        
        for i in range(len(df)):
            row = df.iloc[i]
            
            # Check if we have an active position and need to check exit
            if active_position is not None:
                # Check stop loss
                if active_position.position_type == 'long':
                    if row['low'] <= active_position.stop_loss:
                        active_position.close_trade(row['datetime'], active_position.stop_loss, 'stop_loss')
                        self.trades.append(active_position)
                        active_position = None
                        continue
                    # Check take profit
                    elif row['high'] >= active_position.take_profit:
                        active_position.close_trade(row['datetime'], active_position.take_profit, 'take_profit')
                        self.trades.append(active_position)
                        active_position = None
                        continue
                
                elif active_position.position_type == 'short':
                    if row['high'] >= active_position.stop_loss:
                        active_position.close_trade(row['datetime'], active_position.stop_loss, 'stop_loss')
                        self.trades.append(active_position)
                        active_position = None
                        continue
                    # Check take profit
                    elif row['low'] <= active_position.take_profit:
                        active_position.close_trade(row['datetime'], active_position.take_profit, 'take_profit')
                        self.trades.append(active_position)
                        active_position = None
                        continue
            
            # Check for new entry signal (only if no active position)
            if active_position is None and pd.notna(row['entry_signal']):
                # Calculate swing levels
                swing_low, swing_high = self.strategy.calculate_swing_levels(df, i)
                
                if swing_low is None or swing_high is None:
                    continue
                
                entry_price = row['close']
                
                if row['entry_signal'] == 'long':
                    stop_loss = swing_low
                    take_profit = self.strategy.calculate_position_levels(entry_price, stop_loss, 'long')
                    
                    # Make sure stop loss is below entry
                    if stop_loss >= entry_price:
                        continue
                    
                    active_position = Trade(
                        entry_datetime=row['datetime'],
                        entry_price=entry_price,
                        position_type='long',
                        stop_loss=stop_loss,
                        take_profit=take_profit
                    )
                
                elif row['entry_signal'] == 'short':
                    stop_loss = swing_high
                    take_profit = self.strategy.calculate_position_levels(entry_price, stop_loss, 'short')
                    
                    # Make sure stop loss is above entry
                    if stop_loss <= entry_price:
                        continue
                    
                    active_position = Trade(
                        entry_datetime=row['datetime'],
                        entry_price=entry_price,
                        position_type='short',
                        stop_loss=stop_loss,
                        take_profit=take_profit
                    )
        
        # Close any remaining open position at the end
        if active_position is not None:
            last_row = df.iloc[-1]
            active_position.close_trade(last_row['datetime'], last_row['close'], 'end_of_data')
            self.trades.append(active_position)
        
        print(f"Backtest complete. Total trades: {len(self.trades)}")
        
        return self.trades
    
    def calculate_statistics(self):
        """
        Calculate performance statistics from trades.
        
        Returns:
            Dictionary with performance metrics
        """
        if not self.trades:
            return {
                'total_trades': 0,
                'win_rate': 0,
                'total_pnl': 0,
                'avg_pnl': 0,
                'max_drawdown': 0,
                'sharpe_ratio': 0
            }
        
        # Convert trades to DataFrame for easier analysis
        trades_df = pd.DataFrame([t.to_dict() for t in self.trades])
        
        # Basic statistics
        total_trades = len(trades_df)
        winning_trades = len(trades_df[trades_df['pnl'] > 0])
        losing_trades = len(trades_df[trades_df['pnl'] < 0])
        win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
        
        total_pnl = trades_df['pnl'].sum()
        avg_pnl = trades_df['pnl'].mean()
        
        # Calculate equity curve
        cumulative_pnl = trades_df['pnl'].cumsum()
        equity = self.initial_capital + cumulative_pnl
        
        # Maximum drawdown
        running_max = equity.expanding().max()
        drawdown = equity - running_max
        max_drawdown = drawdown.min()
        max_drawdown_pct = (max_drawdown / self.initial_capital * 100) if self.initial_capital > 0 else 0
        
        # Sharpe ratio (annualized)
        if len(trades_df) > 1:
            returns = trades_df['pnl'] / self.initial_capital
            sharpe_ratio = np.sqrt(252) * (returns.mean() / returns.std()) if returns.std() > 0 else 0
        else:
            sharpe_ratio = 0
        
        # Profit factor
        gross_profit = trades_df[trades_df['pnl'] > 0]['pnl'].sum()
        gross_loss = abs(trades_df[trades_df['pnl'] < 0]['pnl'].sum())
        profit_factor = gross_profit / gross_loss if gross_loss > 0 else float('inf')
        
        # Average winning and losing trade
        avg_win = trades_df[trades_df['pnl'] > 0]['pnl'].mean() if winning_trades > 0 else 0
        avg_loss = trades_df[trades_df['pnl'] < 0]['pnl'].mean() if losing_trades > 0 else 0
        
        stats = {
            'total_trades': total_trades,
            'winning_trades': winning_trades,
            'losing_trades': losing_trades,
            'win_rate': win_rate,
            'total_pnl': total_pnl,
            'avg_pnl': avg_pnl,
            'avg_win': avg_win,
            'avg_loss': avg_loss,
            'max_drawdown': max_drawdown,
            'max_drawdown_pct': max_drawdown_pct,
            'sharpe_ratio': sharpe_ratio,
            'profit_factor': profit_factor,
            'final_equity': self.initial_capital + total_pnl
        }
        
        return stats
    
    def export_trades(self, filename='trade_journal.csv'):
        """
        Export all trades to a CSV file.
        
        Args:
            filename: Output filename
        """
        if not self.trades:
            print("No trades to export.")
            return
        
        trades_df = pd.DataFrame([t.to_dict() for t in self.trades])
        trades_df.to_csv(filename, index=False)
        print(f"Exported {len(trades_df)} trades to {filename}")
    
    def print_statistics(self):
        """Print performance statistics to console."""
        stats = self.calculate_statistics()
        
        print("\n" + "="*60)
        print("BACKTEST PERFORMANCE STATISTICS")
        print("="*60)
        print(f"Initial Capital:        ${self.initial_capital:,.2f}")
        print(f"Final Equity:           ${stats['final_equity']:,.2f}")
        print(f"Total P&L:              ${stats['total_pnl']:,.2f}")
        print(f"\nTotal Trades:           {stats['total_trades']}")
        print(f"Winning Trades:         {stats['winning_trades']}")
        print(f"Losing Trades:          {stats['losing_trades']}")
        print(f"Win Rate:               {stats['win_rate']:.2f}%")
        print(f"\nAverage P&L:            ${stats['avg_pnl']:,.2f}")
        print(f"Average Win:            ${stats['avg_win']:,.2f}")
        print(f"Average Loss:           ${stats['avg_loss']:,.2f}")
        print(f"\nProfit Factor:          {stats['profit_factor']:.2f}")
        print(f"Maximum Drawdown:       ${stats['max_drawdown']:,.2f} ({stats['max_drawdown_pct']:.2f}%)")
        print(f"Sharpe Ratio:           {stats['sharpe_ratio']:.2f}")
        print("="*60 + "\n")

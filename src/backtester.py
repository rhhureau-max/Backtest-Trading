"""
Core backtesting engine.
"""

from typing import Dict, List
import pandas as pd
from strategies.base_strategy import BaseStrategy, Trade


class Backtester:
    """
    Core backtesting engine for running strategies.
    """
    
    def __init__(self, strategy: BaseStrategy):
        self.strategy = strategy
    
    def run(self, data: Dict[str, pd.DataFrame]) -> List[Trade]:
        """
        Run backtest for the strategy.
        
        Args:
            data: Dictionary of DataFrames for different timeframes
        
        Returns:
            List of all trades executed
        """
        # Get unique trading days from 5m data
        df_5m = data.get('5m')
        if df_5m is None or df_5m.empty:
            print(f"No 5m data available for {self.strategy.name}")
            return []
        
        trading_days = df_5m.index.normalize().unique()
        
        print(f"\nRunning backtest for {self.strategy.name}...")
        print(f"Total trading days: {len(trading_days)}")
        
        open_trade = None
        
        # Iterate through each trading day
        for day_idx, day in enumerate(trading_days):
            # Progress indicator
            if (day_idx + 1) % 100 == 0:
                print(f"  Processed {day_idx + 1}/{len(trading_days)} days...")
            
            # Get data for the current day
            day_start = day
            day_end = day + pd.Timedelta(days=1)
            
            day_mask = (df_5m.index >= day_start) & (df_5m.index < day_end)
            day_data_5m = df_5m[day_mask]
            
            if day_data_5m.empty:
                continue
            
            # If no open trade, look for entry signal
            if open_trade is None:
                signal = self.strategy.generate_signals(data, day)
                
                if signal is not None:
                    open_trade = signal
                    self.strategy.trades.append(open_trade)
            
            # If there's an open trade, update it throughout the day
            if open_trade is not None:
                for timestamp in day_data_5m.index:
                    # Update the trade
                    open_trade = self.strategy.update_trade(open_trade, data, timestamp)
                    
                    # Check if trade is closed
                    if open_trade.status in ['closed', 'stopped']:
                        open_trade = None
                        break  # Only one trade per day
        
        # Close any remaining open trades at the end
        if open_trade is not None:
            last_timestamp = df_5m.index[-1]
            last_price = df_5m.loc[last_timestamp, 'Close']
            
            open_trade.exit_time = last_timestamp
            open_trade.exit_price = last_price
            open_trade.status = 'closed'
            
            remaining_position = 1.0
            if open_trade.tp1_hit:
                remaining_position -= open_trade.tp1_percentage
            
            exit_pnl = self.strategy.calculate_pnl(open_trade.entry_price, open_trade.exit_price,
                                                    open_trade.direction, remaining_position)
            open_trade.pnl = open_trade.tp1_pnl + exit_pnl
        
        print(f"Backtest complete. Total trades: {len(self.strategy.trades)}")
        
        return self.strategy.trades
    
    def get_trades_dataframe(self) -> pd.DataFrame:
        """
        Convert trades to DataFrame for analysis.
        
        Returns:
            DataFrame with trade information
        """
        trades = self.strategy.get_closed_trades()
        
        if not trades:
            return pd.DataFrame()
        
        trade_data = []
        for trade in trades:
            trade_data.append({
                'entry_time': trade.entry_time,
                'entry_price': trade.entry_price,
                'exit_time': trade.exit_time,
                'exit_price': trade.exit_price,
                'direction': trade.direction,
                'pnl': trade.pnl,
                'status': trade.status,
                'tp1_hit': trade.tp1_hit,
                'tp2_hit': trade.tp2_hit,
                'breakeven_moved': trade.breakeven_moved
            })
        
        return pd.DataFrame(trade_data)

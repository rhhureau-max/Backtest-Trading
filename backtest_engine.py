"""
Backtesting Engine for FVG Strategy
Handles trade execution, position management, and performance tracking
"""

import pandas as pd
import numpy as np
from datetime import datetime


class Trade:
    """Represents a single trade"""
    
    def __init__(self, entry_time, entry_price, direction, stop_loss, take_profit, fvg_info):
        self.entry_time = entry_time
        self.entry_price = entry_price
        self.direction = direction  # 1 for long, -1 for short
        self.stop_loss = stop_loss
        self.take_profit = take_profit
        self.exit_time = None
        self.exit_price = None
        self.exit_reason = None  # 'TP', 'SL', 'EOD'
        self.pnl = 0
        self.return_pct = 0
        self.fvg_info = fvg_info
        
    def close(self, exit_time, exit_price, exit_reason):
        """Close the trade"""
        self.exit_time = exit_time
        self.exit_price = exit_price
        self.exit_reason = exit_reason
        
        # Calculate P&L
        if self.direction == 1:  # Long
            self.pnl = exit_price - self.entry_price
        else:  # Short
            self.pnl = self.entry_price - exit_price
            
        self.return_pct = (self.pnl / self.entry_price) * 100
        
    def to_dict(self):
        """Convert trade to dictionary"""
        return {
            'entry_time': self.entry_time,
            'entry_price': self.entry_price,
            'exit_time': self.exit_time,
            'exit_price': self.exit_price,
            'direction': 'Long' if self.direction == 1 else 'Short',
            'stop_loss': self.stop_loss,
            'take_profit': self.take_profit,
            'exit_reason': self.exit_reason,
            'pnl': self.pnl,
            'return_pct': self.return_pct,
            'fvg_lower': self.fvg_info.get('lower'),
            'fvg_upper': self.fvg_info.get('upper'),
            'fvg_middle': self.fvg_info.get('middle'),
        }


class BacktestEngine:
    """Execute backtest with FVG strategy"""
    
    def __init__(self, initial_capital=10000):
        self.initial_capital = initial_capital
        self.capital = initial_capital
        self.trades = []
        self.equity_curve = []
        
    def calculate_stop_loss_take_profit(self, entry_price, fvg_middle, direction):
        """
        Calculate stop loss and take profit levels
        
        Parameters:
        -----------
        entry_price : float
            Entry price
        fvg_middle : float
            Middle of FVG (stop loss level)
        direction : int
            1 for long, -1 for short
            
        Returns:
        --------
        tuple
            (stop_loss, take_profit)
        """
        stop_loss = fvg_middle
        risk = abs(entry_price - stop_loss)
        
        if direction == 1:  # Long
            take_profit = entry_price + (2 * risk)
        else:  # Short
            take_profit = entry_price - (2 * risk)
            
        return stop_loss, take_profit
    
    def check_exit(self, trade, current_candle):
        """
        Check if trade should be exited based on current candle
        
        Parameters:
        -----------
        trade : Trade
            Active trade
        current_candle : pd.Series
            Current candle data
            
        Returns:
        --------
        tuple
            (should_exit, exit_price, exit_reason)
        """
        if trade.direction == 1:  # Long position
            # Check stop loss
            if current_candle['Low'] <= trade.stop_loss:
                return True, trade.stop_loss, 'SL'
            # Check take profit
            if current_candle['High'] >= trade.take_profit:
                return True, trade.take_profit, 'TP'
        else:  # Short position
            # Check stop loss
            if current_candle['High'] >= trade.stop_loss:
                return True, trade.stop_loss, 'SL'
            # Check take profit
            if current_candle['Low'] <= trade.take_profit:
                return True, trade.take_profit, 'TP'
                
        return False, None, None
    
    def run_backtest(self, df, timeframe):
        """
        Run backtest on data with FVG signals
        
        Parameters:
        -----------
        df : pd.DataFrame
            Data with FVG signals
        timeframe : str
            Timeframe ('1m', '5m', '15m')
            
        Returns:
        --------
        pd.DataFrame
            Trade results
        """
        print(f"\n{'='*60}")
        print(f"Running backtest for {timeframe} timeframe")
        print(f"{'='*60}")
        
        self.trades = []
        active_trade = None
        
        # Get FVG signals
        fvg_signals = df[df['FVG_Signal'] != 0].copy()
        print(f"Processing {len(fvg_signals)} FVG signals...")
        
        for fvg_idx, fvg_row in fvg_signals.iterrows():
            # Determine entry time based on timeframe
            if timeframe == '1m':
                entry_time = fvg_idx + pd.Timedelta(minutes=1)
            elif timeframe == '5m':
                entry_time = fvg_idx + pd.Timedelta(minutes=5)
            elif timeframe == '15m':
                entry_time = fvg_idx + pd.Timedelta(minutes=15)
            else:
                continue
            
            # Check if entry candle exists
            if entry_time not in df.index:
                continue
            
            # Get entry candle
            entry_candle = df.loc[entry_time]
            entry_price = entry_candle['Close']
            
            # Direction: 1 for bullish, -1 for bearish
            direction = 1 if fvg_row['FVG_Signal'] == 1 else -1
            
            # Calculate SL and TP
            fvg_middle = fvg_row['FVG_Middle']
            stop_loss, take_profit = self.calculate_stop_loss_take_profit(
                entry_price, fvg_middle, direction
            )
            
            # Create trade
            fvg_info = {
                'lower': fvg_row['FVG_Lower'],
                'upper': fvg_row['FVG_Upper'],
                'middle': fvg_row['FVG_Middle']
            }
            
            trade = Trade(
                entry_time=entry_time,
                entry_price=entry_price,
                direction=direction,
                stop_loss=stop_loss,
                take_profit=take_profit,
                fvg_info=fvg_info
            )
            
            # Find exit for this trade
            # Look at candles after entry until end of day or exit condition met
            entry_date = entry_time.date()
            remaining_candles = df.loc[entry_time:]
            same_day_candles = remaining_candles[remaining_candles.index.date == entry_date]
            
            trade_closed = False
            for check_time, check_candle in same_day_candles.iloc[1:].iterrows():
                should_exit, exit_price, exit_reason = self.check_exit(trade, check_candle)
                
                if should_exit:
                    trade.close(check_time, exit_price, exit_reason)
                    trade_closed = True
                    break
            
            # If not closed, close at end of day
            if not trade_closed and len(same_day_candles) > 1:
                last_candle = same_day_candles.iloc[-1]
                trade.close(last_candle.name, last_candle['Close'], 'EOD')
            
            # Only add completed trades
            if trade.exit_time is not None:
                self.trades.append(trade)
        
        print(f"Completed {len(self.trades)} trades")
        
        # Convert trades to DataFrame
        if self.trades:
            trades_df = pd.DataFrame([t.to_dict() for t in self.trades])
            return trades_df
        else:
            return pd.DataFrame()

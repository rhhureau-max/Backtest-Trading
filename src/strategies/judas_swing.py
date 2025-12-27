"""
Strategy A: Judas Swing (Mean Reversion)

Logic:
1. Calculate Asian Range (00:00-08:00 Paris time): High and Low
2. Trigger: Price breaks Asian High/Low, then M5 candle closes back inside range (fakeout)
3. Stop Loss: High of manipulation wick for short (Low of manipulation wick for long)
4. Take Profit: TP1 (50% position) = 50% retracement of Asian Range, then move SL to breakeven
              TP2 (50%) = opposite liquidity (Asian Low for short)
"""

from typing import Optional, Dict
import pandas as pd
import sys
sys.path.append('..')

from strategies.base_strategy import BaseStrategy, Trade
from indicators import calculate_asian_range
import config


class JudasSwingStrategy(BaseStrategy):
    """
    Judas Swing Mean Reversion Strategy.
    """
    
    def __init__(self, spread_points: float = 1.5):
        super().__init__("Judas Swing", spread_points)
        self.tp1_percentage = config.JUDAS_SWING_PARAMS['tp1_percentage']
        self.tp2_percentage = config.JUDAS_SWING_PARAMS['tp2_percentage']
    
    def generate_signals(self, data: Dict[str, pd.DataFrame], date: pd.Timestamp) -> Optional[Trade]:
        """
        Generate Judas Swing signal for a specific date.
        
        Args:
            data: Dictionary with '5m' DataFrame
            date: Trading date
        
        Returns:
            Trade object if signal generated, None otherwise
        """
        df_5m = data.get('5m')
        
        if df_5m is None:
            return None
        
        # 1. Calculate Asian Range (00:00-08:00)
        asian_high, asian_low = calculate_asian_range(df_5m, date)
        
        if asian_high is None or asian_low is None:
            return None
        
        # 2. Look for fakeout during London session (08:00-12:00)
        london_start = date.replace(hour=8, minute=0, second=0)
        london_end = date.replace(hour=12, minute=0, second=0)
        london_mask = (df_5m.index >= london_start) & (df_5m.index < london_end)
        london_data = df_5m[london_mask].copy()
        
        if london_data.empty:
            return None
        
        # Track if we've seen a breakout and subsequent fakeout
        for i in range(len(london_data)):
            current_candle = london_data.iloc[i]
            current_time = london_data.index[i]
            
            # Check for breakout above Asian High
            if current_candle['High'] > asian_high:
                # Look for M5 candle that closes back inside range
                if current_candle['Close'] < asian_high:
                    # SHORT signal - price faked out above, now back inside
                    manipulation_high = current_candle['High']
                    stop_loss = manipulation_high
                    
                    # TP1: 50% retracement of Asian Range
                    asian_mid = asian_low + (asian_high - asian_low) * 0.5
                    tp1 = asian_mid
                    
                    # TP2: Asian Low (opposite liquidity)
                    tp2 = asian_low
                    
                    trade = Trade(
                        entry_time=current_time,
                        entry_price=current_candle['Close'],
                        direction='short',
                        stop_loss=stop_loss,
                        take_profit_1=tp1,
                        take_profit_2=tp2,
                        tp1_percentage=self.tp1_percentage,
                        tp2_percentage=self.tp2_percentage
                    )
                    
                    return trade
            
            # Check for breakout below Asian Low
            elif current_candle['Low'] < asian_low:
                # Look for M5 candle that closes back inside range
                if current_candle['Close'] > asian_low:
                    # LONG signal - price faked out below, now back inside
                    manipulation_low = current_candle['Low']
                    stop_loss = manipulation_low
                    
                    # TP1: 50% retracement of Asian Range
                    asian_mid = asian_low + (asian_high - asian_low) * 0.5
                    tp1 = asian_mid
                    
                    # TP2: Asian High (opposite liquidity)
                    tp2 = asian_high
                    
                    trade = Trade(
                        entry_time=current_time,
                        entry_price=current_candle['Close'],
                        direction='long',
                        stop_loss=stop_loss,
                        take_profit_1=tp1,
                        take_profit_2=tp2,
                        tp1_percentage=self.tp1_percentage,
                        tp2_percentage=self.tp2_percentage
                    )
                    
                    return trade
        
        return None
    
    def update_trade(self, trade: Trade, data: Dict[str, pd.DataFrame], current_time: pd.Timestamp) -> Trade:
        """
        Update trade: check for TP1, TP2, and stop loss.
        
        Args:
            trade: Current open trade
            data: Dictionary with DataFrames
            current_time: Current timestamp
        
        Returns:
            Updated trade
        """
        df_5m = data.get('5m')
        
        if df_5m is None:
            return trade
        
        # Get current candle
        if current_time not in df_5m.index:
            return trade
        
        current_candle = df_5m.loc[current_time]
        
        # Check stop loss first
        if self.check_stop_loss(trade, current_candle):
            trade.exit_time = current_time
            trade.exit_price = trade.stop_loss
            trade.status = 'stopped'
            
            # Calculate remaining position PnL
            remaining_position = 1.0
            if trade.tp1_hit:
                remaining_position -= trade.tp1_percentage
            
            exit_pnl = self.calculate_pnl(trade.entry_price, trade.exit_price, trade.direction, remaining_position)
            trade.pnl = trade.tp1_pnl + exit_pnl
            
            return trade
        
        # Check TP1
        if not trade.tp1_hit and trade.take_profit_1 is not None:
            if self.check_take_profit(trade, current_candle, trade.take_profit_1):
                trade.tp1_hit = True
                trade.tp1_exit_time = current_time
                trade.tp1_exit_price = trade.take_profit_1
                trade.tp1_pnl = self.calculate_pnl(trade.entry_price, trade.tp1_exit_price, 
                                                    trade.direction, trade.tp1_percentage)
                
                # Move stop loss to breakeven
                trade.stop_loss = trade.entry_price
                trade.breakeven_moved = True
        
        # Check TP2
        if trade.tp1_hit and not trade.tp2_hit and trade.take_profit_2 is not None:
            if self.check_take_profit(trade, current_candle, trade.take_profit_2):
                trade.tp2_hit = True
                trade.tp2_exit_time = current_time
                trade.tp2_exit_price = trade.take_profit_2
                trade.tp2_pnl = self.calculate_pnl(trade.entry_price, trade.tp2_exit_price,
                                                    trade.direction, trade.tp2_percentage)
                
                # Close the trade
                trade.exit_time = current_time
                trade.exit_price = trade.tp2_exit_price
                trade.status = 'closed'
                trade.pnl = trade.tp1_pnl + trade.tp2_pnl
        
        return trade

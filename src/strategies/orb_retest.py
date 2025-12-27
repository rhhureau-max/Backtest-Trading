"""
Strategy B: ORB Retest (Expansion)

Logic:
1. Define "Box" 08:00-09:00 Paris (High and Low)
2. Calculate Box_Size in points
3. Trigger: Breakout after 09:00 + retest of breakout level
4. Stop Loss: Behind the M15 breakout candle low
5. Take Profit: TP1 (70%) = 1x Box_Size projection, TP2 (30%) = 2.5x Box_Size projection
"""

from typing import Optional, Dict
import pandas as pd
import sys
sys.path.append('..')

from strategies.base_strategy import BaseStrategy, Trade
import config


class ORBRetestStrategy(BaseStrategy):
    """
    Opening Range Breakout with Retest Strategy.
    """
    
    def __init__(self, spread_points: float = 1.5):
        super().__init__("ORB Retest", spread_points)
        self.orb_start = config.ORB_RETEST_PARAMS['orb_start']
        self.orb_end = config.ORB_RETEST_PARAMS['orb_end']
        self.tp1_percentage = config.ORB_RETEST_PARAMS['tp1_percentage']
        self.tp2_percentage = config.ORB_RETEST_PARAMS['tp2_percentage']
    
    def generate_signals(self, data: Dict[str, pd.DataFrame], date: pd.Timestamp) -> Optional[Trade]:
        """
        Generate ORB Retest signal for a specific date.
        
        Args:
            data: Dictionary with '5m' and '15m' DataFrames
            date: Trading date
        
        Returns:
            Trade object if signal generated, None otherwise
        """
        df_5m = data.get('5m')
        df_15m = data.get('15m')
        
        if df_5m is None or df_15m is None:
            return None
        
        # 1. Define Opening Range Box (08:00-09:00)
        orb_start_time = date.replace(hour=8, minute=0, second=0)
        orb_end_time = date.replace(hour=9, minute=0, second=0)
        
        orb_mask = (df_5m.index >= orb_start_time) & (df_5m.index < orb_end_time)
        orb_data = df_5m[orb_mask]
        
        if orb_data.empty:
            return None
        
        box_high = orb_data['High'].max()
        box_low = orb_data['Low'].min()
        box_size = box_high - box_low
        
        if box_size == 0:
            return None
        
        # 2. Look for breakout after 09:00
        london_end = date.replace(hour=12, minute=0, second=0)
        post_orb_mask = (df_5m.index >= orb_end_time) & (df_5m.index < london_end)
        post_orb_data = df_5m[post_orb_mask].copy()
        
        if post_orb_data.empty:
            return None
        
        # Track breakout and retest
        breakout_direction = None
        breakout_candle_idx = None
        
        for i in range(len(post_orb_data)):
            current_candle = post_orb_data.iloc[i]
            current_time = post_orb_data.index[i]
            
            # Look for breakout above box high
            if breakout_direction is None and current_candle['Close'] > box_high:
                breakout_direction = 'long'
                breakout_candle_idx = i
            
            # Look for breakout below box low
            elif breakout_direction is None and current_candle['Close'] < box_low:
                breakout_direction = 'short'
                breakout_candle_idx = i
            
            # Look for retest after breakout
            elif breakout_direction == 'long' and i > breakout_candle_idx:
                # Retest: price comes back to box_high level
                if current_candle['Low'] <= box_high <= current_candle['High']:
                    # LONG signal - retest confirmed
                    
                    # Get M15 breakout candle for stop loss
                    m15_mask = (df_15m.index >= orb_end_time) & (df_15m.index <= current_time)
                    m15_breakout_data = df_15m[m15_mask]
                    
                    if m15_breakout_data.empty:
                        continue
                    
                    # Stop loss: behind M15 breakout candle low
                    m15_breakout_low = m15_breakout_data['Low'].min()
                    stop_loss = m15_breakout_low
                    
                    # TP1: 1x Box_Size projection
                    tp1 = box_high + (1.0 * box_size)
                    
                    # TP2: 2.5x Box_Size projection
                    tp2 = box_high + (2.5 * box_size)
                    
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
            
            elif breakout_direction == 'short' and i > breakout_candle_idx:
                # Retest: price comes back to box_low level
                if current_candle['Low'] <= box_low <= current_candle['High']:
                    # SHORT signal - retest confirmed
                    
                    # Get M15 breakout candle for stop loss
                    m15_mask = (df_15m.index >= orb_end_time) & (df_15m.index <= current_time)
                    m15_breakout_data = df_15m[m15_mask]
                    
                    if m15_breakout_data.empty:
                        continue
                    
                    # Stop loss: behind M15 breakout candle high
                    m15_breakout_high = m15_breakout_data['High'].max()
                    stop_loss = m15_breakout_high
                    
                    # TP1: 1x Box_Size projection
                    tp1 = box_low - (1.0 * box_size)
                    
                    # TP2: 2.5x Box_Size projection
                    tp2 = box_low - (2.5 * box_size)
                    
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
        
        # Check TP2
        if not trade.tp2_hit and trade.take_profit_2 is not None:
            if self.check_take_profit(trade, current_candle, trade.take_profit_2):
                trade.tp2_hit = True
                trade.tp2_exit_time = current_time
                trade.tp2_exit_price = trade.take_profit_2
                
                # Calculate TP2 PnL
                remaining_position = trade.tp2_percentage
                trade.tp2_pnl = self.calculate_pnl(trade.entry_price, trade.tp2_exit_price,
                                                    trade.direction, remaining_position)
                
                # Close the trade
                trade.exit_time = current_time
                trade.exit_price = trade.tp2_exit_price
                trade.status = 'closed'
                trade.pnl = trade.tp1_pnl + trade.tp2_pnl
        
        return trade

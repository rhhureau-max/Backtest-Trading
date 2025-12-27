"""
Strategy C: HTF Trend Continuation

Logic:
1. Daily trend direction = previous daily close direction
2. Wait for retracement into OTE zone (62-79% Fibonacci) of overnight impulse
3. Trigger: M5 reversal candle in OTE zone
4. Stop Loss: Strictly under Swing Low (Fib 0%)
5. Take Profit: No fixed TP. Trailing stop based on EMA(9) on M15. Exit when M15 closes below EMA9 (for long)
"""

from typing import Optional, Dict
import pandas as pd
import sys
sys.path.append('..')

from strategies.base_strategy import BaseStrategy, Trade
from indicators import (calculate_ema, calculate_fibonacci_levels, 
                       calculate_overnight_impulse, is_reversal_candle, is_in_ote_zone)
import config


class HTFTrendContinuationStrategy(BaseStrategy):
    """
    Higher Timeframe Trend Continuation Strategy with Trailing Stop.
    """
    
    def __init__(self, spread_points: float = 1.5):
        super().__init__("HTF Trend Continuation", spread_points)
        self.ema_period = config.HTF_TREND_PARAMS['ema_period']
        self.fib_ote_low = config.HTF_TREND_PARAMS['fib_ote_low']
        self.fib_ote_high = config.HTF_TREND_PARAMS['fib_ote_high']
    
    def generate_signals(self, data: Dict[str, pd.DataFrame], date: pd.Timestamp) -> Optional[Trade]:
        """
        Generate HTF Trend Continuation signal for a specific date.
        
        Args:
            data: Dictionary with '5m', '15m', and '1D' DataFrames
            date: Trading date
        
        Returns:
            Trade object if signal generated, None otherwise
        """
        df_5m = data.get('5m')
        df_15m = data.get('15m')
        df_1d = data.get('1D')
        
        if df_5m is None or df_15m is None or df_1d is None:
            return None
        
        # 1. Determine daily trend direction from previous day
        prev_day = (date - pd.Timedelta(days=1)).normalize()
        
        # Get previous two daily closes
        daily_mask = df_1d.index.normalize() <= prev_day
        daily_data = df_1d[daily_mask]
        
        if len(daily_data) < 2:
            return None
        
        prev_close = daily_data['Close'].iloc[-1]
        prev_prev_close = daily_data['Close'].iloc[-2]
        
        # Trend direction
        if prev_close > prev_prev_close:
            trend_direction = 'bullish'
        elif prev_close < prev_prev_close:
            trend_direction = 'bearish'
        else:
            return None  # No clear trend
        
        # 2. Calculate overnight impulse move
        london_start = date.replace(hour=8, minute=0, second=0)
        impulse_high, impulse_low = calculate_overnight_impulse(df_5m, london_start)
        
        if impulse_high is None or impulse_low is None:
            return None
        
        # 3. Calculate Fibonacci levels
        if trend_direction == 'bullish':
            fib_levels = calculate_fibonacci_levels(impulse_high, impulse_low, is_uptrend=True)
            swing_low = impulse_low  # Fib 100%
        else:
            fib_levels = calculate_fibonacci_levels(impulse_high, impulse_low, is_uptrend=False)
            swing_high = impulse_high  # Fib 100%
        
        # 4. Look for retracement into OTE zone during London session
        london_end = date.replace(hour=12, minute=0, second=0)
        london_mask = (df_5m.index >= london_start) & (df_5m.index < london_end)
        london_data = df_5m[london_mask].copy()
        
        if london_data.empty:
            return None
        
        # Look for M5 reversal candle in OTE zone
        for i in range(len(london_data)):
            current_candle = london_data.iloc[i]
            current_time = london_data.index[i]
            current_price = current_candle['Close']
            
            # Check if price is in OTE zone
            in_ote = is_in_ote_zone(current_price, fib_levels, self.fib_ote_low, self.fib_ote_high)
            
            if not in_ote:
                continue
            
            # Check for reversal candle in the trend direction
            if trend_direction == 'bullish':
                if is_reversal_candle(current_candle, direction='bullish'):
                    # LONG signal
                    stop_loss = swing_low  # Below Fib 0% (Swing Low)
                    
                    trade = Trade(
                        entry_time=current_time,
                        entry_price=current_candle['Close'],
                        direction='long',
                        stop_loss=stop_loss,
                        take_profit_1=None,  # No fixed TP, using trailing stop
                        take_profit_2=None,
                        tp1_percentage=1.0,  # 100% of position
                        tp2_percentage=0.0
                    )
                    
                    return trade
            
            elif trend_direction == 'bearish':
                if is_reversal_candle(current_candle, direction='bearish'):
                    # SHORT signal
                    stop_loss = swing_high  # Above Fib 0% (Swing High)
                    
                    trade = Trade(
                        entry_time=current_time,
                        entry_price=current_candle['Close'],
                        direction='short',
                        stop_loss=stop_loss,
                        take_profit_1=None,  # No fixed TP, using trailing stop
                        take_profit_2=None,
                        tp1_percentage=1.0,  # 100% of position
                        tp2_percentage=0.0
                    )
                    
                    return trade
        
        return None
    
    def update_trade(self, trade: Trade, data: Dict[str, pd.DataFrame], current_time: pd.Timestamp) -> Trade:
        """
        Update trade: check for trailing stop based on EMA(9) on M15.
        
        Args:
            trade: Current open trade
            data: Dictionary with DataFrames
            current_time: Current timestamp
        
        Returns:
            Updated trade
        """
        df_5m = data.get('5m')
        df_15m = data.get('15m')
        
        if df_5m is None or df_15m is None:
            return trade
        
        # Get current M5 candle
        if current_time not in df_5m.index:
            return trade
        
        current_candle_5m = df_5m.loc[current_time]
        
        # Check stop loss first
        if self.check_stop_loss(trade, current_candle_5m):
            trade.exit_time = current_time
            trade.exit_price = trade.stop_loss
            trade.status = 'stopped'
            trade.pnl = self.calculate_pnl(trade.entry_price, trade.exit_price, trade.direction, 1.0)
            
            return trade
        
        # Update trailing stop based on EMA(9) on M15
        # Check if current time is on a M15 boundary
        if current_time.minute % 15 == 0:
            # Get M15 data up to current time
            m15_mask = df_15m.index <= current_time
            m15_data = df_15m[m15_mask].copy()
            
            if len(m15_data) >= self.ema_period:
                # Calculate EMA(9)
                ema9 = calculate_ema(m15_data['Close'], self.ema_period)
                current_ema = ema9.iloc[-1]
                
                if pd.notna(current_ema):
                    # Get current M15 candle
                    current_m15_candle = m15_data.iloc[-1]
                    
                    # Check for exit condition
                    if trade.direction == 'long':
                        # Exit when M15 closes below EMA9
                        if current_m15_candle['Close'] < current_ema:
                            trade.exit_time = current_time
                            trade.exit_price = current_m15_candle['Close']
                            trade.status = 'closed'
                            trade.pnl = self.calculate_pnl(trade.entry_price, trade.exit_price, 
                                                           trade.direction, 1.0)
                        else:
                            # Update trailing stop to EMA9
                            trade.trailing_stop = current_ema
                            # Update stop loss to trailing stop if it's higher
                            if current_ema > trade.stop_loss:
                                trade.stop_loss = current_ema
                    
                    elif trade.direction == 'short':
                        # Exit when M15 closes above EMA9
                        if current_m15_candle['Close'] > current_ema:
                            trade.exit_time = current_time
                            trade.exit_price = current_m15_candle['Close']
                            trade.status = 'closed'
                            trade.pnl = self.calculate_pnl(trade.entry_price, trade.exit_price,
                                                           trade.direction, 1.0)
                        else:
                            # Update trailing stop to EMA9
                            trade.trailing_stop = current_ema
                            # Update stop loss to trailing stop if it's lower
                            if current_ema < trade.stop_loss:
                                trade.stop_loss = current_ema
        
        return trade

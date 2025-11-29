"""
Strategy Module for 8:30 Strategy Backtest

This module contains the strategy logic for entry conditions,
stop loss, and take profit calculations.
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple, Optional
from enum import Enum


class Direction(Enum):
    LONG = "LONG"
    SHORT = "SHORT"


class SLType(Enum):
    SL_25 = "SL_25%"
    SL_50 = "SL_50%"
    SL_75 = "SL_75%"
    SL_100 = "SL_100%"
    SL_WICK = "SL_Wick"


# Buffer for wick-based SL (in points)
WICK_BUFFER = 2.0


def check_long_entry(candle_830: pd.Series, prev_candles: pd.DataFrame) -> bool:
    """
    Check if the 8:30 candle qualifies for a LONG entry.
    
    Conditions:
    - Close > all previous 5 closes
    - Close > all previous 5 highs
    - Bullish candle (Close > Open)
    
    Args:
        candle_830: The 8:30 candle data
        prev_candles: Previous 5 candles
        
    Returns:
        True if LONG entry conditions are met
    """
    if len(prev_candles) < 5:
        return False
    
    close_830 = candle_830['close']
    open_830 = candle_830['open']
    
    # Check if bullish
    if close_830 <= open_830:
        return False
    
    # Check if close > all previous closes
    if not (close_830 > prev_candles['close'].max()):
        return False
    
    # Check if close > all previous highs
    if not (close_830 > prev_candles['high'].max()):
        return False
    
    return True


def check_short_entry(candle_830: pd.Series, prev_candles: pd.DataFrame) -> bool:
    """
    Check if the 8:30 candle qualifies for a SHORT entry.
    
    Conditions:
    - Close < all previous 5 closes
    - Close < all previous 5 lows
    - Bearish candle (Close < Open)
    
    Args:
        candle_830: The 8:30 candle data
        prev_candles: Previous 5 candles
        
    Returns:
        True if SHORT entry conditions are met
    """
    if len(prev_candles) < 5:
        return False
    
    close_830 = candle_830['close']
    open_830 = candle_830['open']
    
    # Check if bearish
    if close_830 >= open_830:
        return False
    
    # Check if close < all previous closes
    if not (close_830 < prev_candles['close'].min()):
        return False
    
    # Check if close < all previous lows
    if not (close_830 < prev_candles['low'].min()):
        return False
    
    return True


def get_entry_direction(candle_830: pd.Series, prev_candles: pd.DataFrame) -> Optional[Direction]:
    """
    Determine the entry direction for the 8:30 candle.
    
    Args:
        candle_830: The 8:30 candle data
        prev_candles: Previous 5 candles
        
    Returns:
        Direction.LONG, Direction.SHORT, or None if no valid entry
    """
    if check_long_entry(candle_830, prev_candles):
        return Direction.LONG
    elif check_short_entry(candle_830, prev_candles):
        return Direction.SHORT
    return None


def calculate_sl(candle_830: pd.Series, direction: Direction, 
                 sl_type: SLType) -> float:
    """
    Calculate the stop loss price.
    
    Args:
        candle_830: The 8:30 candle data
        direction: LONG or SHORT
        sl_type: Type of stop loss
        
    Returns:
        Stop loss price
    """
    entry = candle_830['close']
    open_price = candle_830['open']
    high = candle_830['high']
    low = candle_830['low']
    
    # Calculate candle body
    body = abs(entry - open_price)
    
    sl_percentages = {
        SLType.SL_25: 0.25,
        SLType.SL_50: 0.50,
        SLType.SL_75: 0.75,
        SLType.SL_100: 1.00,
    }
    
    if sl_type in sl_percentages:
        pct = sl_percentages[sl_type]
        if direction == Direction.LONG:
            return entry - (body * pct)
        else:
            return entry + (body * pct)
    
    elif sl_type == SLType.SL_WICK:
        if direction == Direction.LONG:
            return low - WICK_BUFFER
        else:
            return high + WICK_BUFFER
    
    raise ValueError(f"Unknown SL type: {sl_type}")


def calculate_tp(entry: float, sl: float, rr: float, 
                 direction: Direction) -> float:
    """
    Calculate the take profit price.
    
    Args:
        entry: Entry price
        sl: Stop loss price
        rr: Risk/Reward ratio
        direction: LONG or SHORT
        
    Returns:
        Take profit price
    """
    sl_distance = abs(entry - sl)
    tp_distance = sl_distance * rr
    
    if direction == Direction.LONG:
        return entry + tp_distance
    else:
        return entry - tp_distance


def simulate_trade(data_1m: pd.DataFrame, entry_time: pd.Timestamp,
                   entry_price: float, sl: float, tp: float,
                   direction: Direction) -> Dict:
    """
    Simulate a trade using 1-minute data (vectorized for performance).
    
    Args:
        data_1m: 1-minute price data
        entry_time: Entry timestamp
        entry_price: Entry price
        sl: Stop loss price
        tp: Take profit price
        direction: LONG or SHORT
        
    Returns:
        Dict with trade result information
    """
    # Get data after entry - limit to 10 trading days (approx 10000 minutes)
    future_data = data_1m[data_1m.index > entry_time].head(10000)
    
    if len(future_data) == 0:
        return {
            'result': None,
            'exit_time': None,
            'exit_price': None,
            'pnl_r': 0
        }
    
    highs = future_data['high'].values
    lows = future_data['low'].values
    indices = future_data.index
    
    if direction == Direction.LONG:
        # Find first SL hit (low <= sl)
        sl_hits = np.where(lows <= sl)[0]
        sl_idx = sl_hits[0] if len(sl_hits) > 0 else -1
        
        # Find first TP hit (high >= tp)
        tp_hits = np.where(highs >= tp)[0]
        tp_idx = tp_hits[0] if len(tp_hits) > 0 else -1
        
        if sl_idx == -1 and tp_idx == -1:
            return {'result': None, 'exit_time': None, 'exit_price': None, 'pnl_r': 0}
        
        if sl_idx != -1 and (tp_idx == -1 or sl_idx <= tp_idx):
            return {
                'result': 'Loss',
                'exit_time': indices[sl_idx],
                'exit_price': sl,
                'pnl_r': -1.0
            }
        else:
            rr_achieved = (tp - entry_price) / (entry_price - sl)
            return {
                'result': 'Win',
                'exit_time': indices[tp_idx],
                'exit_price': tp,
                'pnl_r': rr_achieved
            }
    
    else:  # SHORT
        # Find first SL hit (high >= sl)
        sl_hits = np.where(highs >= sl)[0]
        sl_idx = sl_hits[0] if len(sl_hits) > 0 else -1
        
        # Find first TP hit (low <= tp)
        tp_hits = np.where(lows <= tp)[0]
        tp_idx = tp_hits[0] if len(tp_hits) > 0 else -1
        
        if sl_idx == -1 and tp_idx == -1:
            return {'result': None, 'exit_time': None, 'exit_price': None, 'pnl_r': 0}
        
        if sl_idx != -1 and (tp_idx == -1 or sl_idx <= tp_idx):
            return {
                'result': 'Loss',
                'exit_time': indices[sl_idx],
                'exit_price': sl,
                'pnl_r': -1.0
            }
        else:
            rr_achieved = (entry_price - tp) / (sl - entry_price)
            return {
                'result': 'Win',
                'exit_time': indices[tp_idx],
                'exit_price': tp,
                'pnl_r': rr_achieved
            }


def simulate_trade_fast(future_data: pd.DataFrame,
                        entry_price: float, sl: float, tp: float,
                        direction: Direction) -> Dict:
    """
    Fast trade simulation on pre-sliced data.
    
    Args:
        future_data: Pre-sliced 1-minute data after entry
        entry_price: Entry price
        sl: Stop loss price
        tp: Take profit price
        direction: LONG or SHORT
        
    Returns:
        Dict with trade result information
    """
    if len(future_data) == 0:
        return {
            'result': None,
            'exit_time': None,
            'exit_price': None,
            'pnl_r': 0
        }
    
    highs = future_data['high'].values
    lows = future_data['low'].values
    indices = future_data.index
    
    if direction == Direction.LONG:
        # Find first SL hit (low <= sl)
        sl_hits = np.where(lows <= sl)[0]
        sl_idx = sl_hits[0] if len(sl_hits) > 0 else -1
        
        # Find first TP hit (high >= tp)
        tp_hits = np.where(highs >= tp)[0]
        tp_idx = tp_hits[0] if len(tp_hits) > 0 else -1
        
        if sl_idx == -1 and tp_idx == -1:
            return {'result': None, 'exit_time': None, 'exit_price': None, 'pnl_r': 0}
        
        if sl_idx != -1 and (tp_idx == -1 or sl_idx <= tp_idx):
            return {
                'result': 'Loss',
                'exit_time': indices[sl_idx],
                'exit_price': sl,
                'pnl_r': -1.0
            }
        else:
            rr_achieved = (tp - entry_price) / (entry_price - sl)
            return {
                'result': 'Win',
                'exit_time': indices[tp_idx],
                'exit_price': tp,
                'pnl_r': rr_achieved
            }
    
    else:  # SHORT
        # Find first SL hit (high >= sl)
        sl_hits = np.where(highs >= sl)[0]
        sl_idx = sl_hits[0] if len(sl_hits) > 0 else -1
        
        # Find first TP hit (low <= tp)
        tp_hits = np.where(lows <= tp)[0]
        tp_idx = tp_hits[0] if len(tp_hits) > 0 else -1
        
        if sl_idx == -1 and tp_idx == -1:
            return {'result': None, 'exit_time': None, 'exit_price': None, 'pnl_r': 0}
        
        if sl_idx != -1 and (tp_idx == -1 or sl_idx <= tp_idx):
            return {
                'result': 'Loss',
                'exit_time': indices[sl_idx],
                'exit_price': sl,
                'pnl_r': -1.0
            }
        else:
            rr_achieved = (entry_price - tp) / (sl - entry_price)
            return {
                'result': 'Win',
                'exit_time': indices[tp_idx],
                'exit_price': tp,
                'pnl_r': rr_achieved
            }


def get_all_sl_types() -> list:
    """Return all SL types for analysis."""
    return list(SLType)


def get_all_rr_values() -> list:
    """Return all RR values for analysis."""
    return [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]


if __name__ == "__main__":
    # Test the strategy module
    print("Strategy module loaded successfully")
    print(f"SL Types: {[sl.value for sl in get_all_sl_types()]}")
    print(f"RR Values: {get_all_rr_values()}")

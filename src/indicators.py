"""
Technical indicators for backtesting strategies.
"""

import pandas as pd
import numpy as np
from typing import Tuple


def calculate_atr(df: pd.DataFrame, period: int = 14) -> pd.Series:
    """
    Calculate Average True Range (ATR).
    
    Args:
        df: DataFrame with High, Low, Close columns
        period: ATR period
    
    Returns:
        Series with ATR values
    """
    high = df['High']
    low = df['Low']
    close = df['Close']
    
    # True Range calculation
    tr1 = high - low
    tr2 = abs(high - close.shift(1))
    tr3 = abs(low - close.shift(1))
    
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    
    # ATR is the moving average of True Range
    atr = tr.rolling(window=period).mean()
    
    return atr


def calculate_ema(series: pd.Series, period: int = 9) -> pd.Series:
    """
    Calculate Exponential Moving Average (EMA).
    
    Args:
        series: Price series (typically Close)
        period: EMA period
    
    Returns:
        Series with EMA values
    """
    return series.ewm(span=period, adjust=False).mean()


def calculate_fibonacci_levels(high: float, low: float, is_uptrend: bool = True) -> dict:
    """
    Calculate Fibonacci retracement levels.
    
    Args:
        high: High price of the impulse move
        low: Low price of the impulse move
        is_uptrend: True for uptrend, False for downtrend
    
    Returns:
        Dictionary with Fibonacci levels
    """
    diff = high - low
    
    levels = {
        '0%': high if is_uptrend else low,
        '23.6%': high - 0.236 * diff if is_uptrend else low + 0.236 * diff,
        '38.2%': high - 0.382 * diff if is_uptrend else low + 0.382 * diff,
        '50%': high - 0.5 * diff if is_uptrend else low + 0.5 * diff,
        '61.8%': high - 0.618 * diff if is_uptrend else low + 0.618 * diff,
        '78.6%': high - 0.786 * diff if is_uptrend else low + 0.786 * diff,
        '100%': low if is_uptrend else high
    }
    
    return levels


def calculate_asian_range(df: pd.DataFrame, date: pd.Timestamp) -> Tuple[float, float]:
    """
    Calculate Asian session range (00:00-08:00 Paris time) for a specific date.
    
    Args:
        df: DataFrame with OHLCV data
        date: Date to calculate range for
    
    Returns:
        Tuple of (asian_high, asian_low)
    """
    # Filter for Asian session on the specific date
    asian_start = date.replace(hour=0, minute=0, second=0)
    asian_end = date.replace(hour=8, minute=0, second=0)
    
    mask = (df.index >= asian_start) & (df.index < asian_end)
    asian_data = df[mask]
    
    if asian_data.empty:
        return None, None
    
    asian_high = asian_data['High'].max()
    asian_low = asian_data['Low'].min()
    
    return asian_high, asian_low


def calculate_overnight_impulse(df: pd.DataFrame, current_time: pd.Timestamp) -> Tuple[float, float]:
    """
    Calculate overnight impulse move (from previous day close to current time).
    
    Args:
        df: DataFrame with OHLCV data
        current_time: Current timestamp
    
    Returns:
        Tuple of (impulse_high, impulse_low)
    """
    # Get previous day's close
    prev_day = (current_time - pd.Timedelta(days=1)).normalize()
    
    # Get data from previous day close to current time
    mask = (df.index > prev_day) & (df.index <= current_time)
    impulse_data = df[mask]
    
    if impulse_data.empty:
        return None, None
    
    impulse_high = impulse_data['High'].max()
    impulse_low = impulse_data['Low'].min()
    
    return impulse_high, impulse_low


def is_reversal_candle(candle: pd.Series, direction: str = 'bullish') -> bool:
    """
    Check if a candle is a reversal candle.
    
    Args:
        candle: Series with Open, High, Low, Close
        direction: 'bullish' or 'bearish'
    
    Returns:
        True if candle is a reversal candle
    """
    body = abs(candle['Close'] - candle['Open'])
    total_range = candle['High'] - candle['Low']
    
    if total_range == 0:
        return False
    
    body_ratio = body / total_range
    
    if direction == 'bullish':
        # Bullish reversal: close > open, small lower wick, decent body
        is_bullish = candle['Close'] > candle['Open']
        lower_wick = candle['Open'] - candle['Low']
        has_small_wick = lower_wick / total_range < 0.3
        has_body = body_ratio > 0.5
        
        return is_bullish and has_small_wick and has_body
    
    elif direction == 'bearish':
        # Bearish reversal: close < open, small upper wick, decent body
        is_bearish = candle['Close'] < candle['Open']
        upper_wick = candle['High'] - candle['Open']
        has_small_wick = upper_wick / total_range < 0.3
        has_body = body_ratio > 0.5
        
        return is_bearish and has_small_wick and has_body
    
    return False


def is_in_ote_zone(price: float, fib_levels: dict, fib_low: float = 0.62, fib_high: float = 0.79) -> bool:
    """
    Check if price is in Optimal Trade Entry (OTE) zone (62-79% Fibonacci).
    
    Args:
        price: Current price
        fib_levels: Dictionary with Fibonacci levels
        fib_low: Lower bound of OTE zone (default 62%)
        fib_high: Upper bound of OTE zone (default 79%)
    
    Returns:
        True if price is in OTE zone
    """
    fib_62 = fib_levels.get('61.8%')
    fib_79 = fib_levels.get('78.6%')
    
    if fib_62 is None or fib_79 is None:
        return False
    
    # OTE zone is between 62% and 79%
    lower_bound = min(fib_62, fib_79)
    upper_bound = max(fib_62, fib_79)
    
    return lower_bound <= price <= upper_bound

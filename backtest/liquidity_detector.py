"""
Liquidity detection module for identifying swing highs/lows and liquidity sweeps.

Uses fractal/pivot point detection to identify significant highs and lows,
and detects when these levels are swept (taken out) by price.
"""
import pandas as pd
import numpy as np
from dataclasses import dataclass
from typing import List, Optional, Tuple
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


@dataclass
class SwingPoint:
    """Represents a swing high or swing low (fractal point)."""
    timestamp: datetime
    price: float
    type: str  # 'high' or 'low'
    is_swept: bool = False
    sweep_timestamp: Optional[datetime] = None
    
    def __repr__(self):
        return f"SwingPoint({self.type} at {self.price:.2f} on {self.timestamp})"


@dataclass
class LiquiditySweep:
    """Represents a liquidity sweep event."""
    timestamp: datetime
    swept_point: SwingPoint
    sweep_price: float
    direction: str  # 'bullish' (swept low) or 'bearish' (swept high)
    
    def __repr__(self):
        return f"LiquiditySweep({self.direction} at {self.timestamp}, swept {self.swept_point.type} at {self.sweep_price:.2f})"


def detect_fractals(
    df: pd.DataFrame,
    lookback: int = 2
) -> List[SwingPoint]:
    """
    Detect fractal highs and lows (Williams fractals).
    
    A fractal high is a candle with 'lookback' lower highs on each side.
    A fractal low is a candle with 'lookback' higher lows on each side.
    
    Args:
        df: DataFrame with OHLC data
        lookback: Number of candles to check on each side
        
    Returns:
        List of SwingPoint objects
    """
    swing_points = []
    
    if len(df) < (2 * lookback + 1):
        return swing_points
    
    highs = df['High'].values
    lows = df['Low'].values
    timestamps = df.index.to_numpy()
    
    for i in range(lookback, len(df) - lookback):
        is_swing_high = True
        is_swing_low = True
        
        # Check for swing high (fractal high)
        for j in range(1, lookback + 1):
            if highs[i] <= highs[i - j] or highs[i] <= highs[i + j]:
                is_swing_high = False
                break
        
        # Check for swing low (fractal low)
        for j in range(1, lookback + 1):
            if lows[i] >= lows[i - j] or lows[i] >= lows[i + j]:
                is_swing_low = False
                break
        
        if is_swing_high:
            swing_points.append(SwingPoint(
                timestamp=pd.Timestamp(timestamps[i]),
                price=highs[i],
                type='high'
            ))
            
        if is_swing_low:
            swing_points.append(SwingPoint(
                timestamp=pd.Timestamp(timestamps[i]),
                price=lows[i],
                type='low'
            ))
    
    logger.debug(f"Detected {len(swing_points)} swing points")
    return swing_points


def detect_liquidity_sweeps(
    df: pd.DataFrame,
    swing_points: List[SwingPoint],
    min_sweep_buffer_pct: float = 0.0001
) -> List[LiquiditySweep]:
    """
    Detect liquidity sweeps where price takes out old highs or lows.
    
    Args:
        df: DataFrame with OHLC data
        swing_points: List of previously identified swing points
        min_sweep_buffer_pct: Minimum buffer percentage for sweep confirmation
        
    Returns:
        List of LiquiditySweep objects
    """
    sweeps = []
    
    for point in swing_points:
        if point.is_swept:
            continue
            
        # Get data after this swing point
        subsequent = df[df.index > point.timestamp]
        
        if len(subsequent) == 0:
            continue
        
        buffer = point.price * min_sweep_buffer_pct
        
        if point.type == 'high':
            # Look for a candle that takes out this high
            sweep_mask = subsequent['High'] > (point.price + buffer)
            sweep_candles = subsequent[sweep_mask]
            
            if len(sweep_candles) > 0:
                sweep_time = sweep_candles.index[0]
                sweep_price = sweep_candles.iloc[0]['High']
                
                point.is_swept = True
                point.sweep_timestamp = sweep_time
                
                sweeps.append(LiquiditySweep(
                    timestamp=sweep_time,
                    swept_point=point,
                    sweep_price=sweep_price,
                    direction='bearish'  # Swept high typically leads to bearish move
                ))
                
        else:  # swing low
            # Look for a candle that takes out this low
            sweep_mask = subsequent['Low'] < (point.price - buffer)
            sweep_candles = subsequent[sweep_mask]
            
            if len(sweep_candles) > 0:
                sweep_time = sweep_candles.index[0]
                sweep_price = sweep_candles.iloc[0]['Low']
                
                point.is_swept = True
                point.sweep_timestamp = sweep_time
                
                sweeps.append(LiquiditySweep(
                    timestamp=sweep_time,
                    swept_point=point,
                    sweep_price=sweep_price,
                    direction='bullish'  # Swept low typically leads to bullish move
                ))
    
    logger.debug(f"Detected {len(sweeps)} liquidity sweeps")
    return sweeps


def find_active_liquidity_zone(
    h1_data: pd.DataFrame,
    m15_data: pd.DataFrame,
    current_time: datetime,
    lookback_hours: int = 48,
    fractal_lookback: int = 2,
    sweep_buffer_pct: float = 0.0002
) -> Optional[Tuple[str, float, datetime]]:
    """
    Find if price is currently in a liquidity zone (just swept an old high/low).
    
    Args:
        h1_data: 1-hour OHLC data
        m15_data: 15-minute OHLC data
        current_time: Current timestamp
        lookback_hours: How far back to look for swing points
        fractal_lookback: Fractal detection lookback period
        sweep_buffer_pct: Buffer percentage for sweep detection
        
    Returns:
        Tuple of (direction, swept_price, sweep_time) if in zone, None otherwise
    """
    from datetime import timedelta
    
    lookback_start = current_time - timedelta(hours=lookback_hours)
    
    # Get H1 data for swing point detection
    h1_window = h1_data[h1_data.index <= current_time]
    if len(h1_window) < 10:
        return None
    
    # Detect swing points
    swing_points = detect_fractals(h1_window.tail(200), fractal_lookback)
    
    if not swing_points:
        return None
    
    # Filter to recent swing points
    recent_points = [p for p in swing_points if p.timestamp >= lookback_start and p.timestamp < current_time]
    
    if not recent_points:
        return None
    
    # Check for very recent sweeps (within last few candles)
    recent_window = h1_data[(h1_data.index > lookback_start) & (h1_data.index <= current_time)]
    
    if len(recent_window) < 2:
        return None
    
    current_candle = recent_window.iloc[-1]
    prev_candle = recent_window.iloc[-2]
    
    for point in recent_points:
        if point.timestamp >= current_time - timedelta(hours=2):
            continue  # Too recent to be a valid old high/low
            
        buffer = point.price * sweep_buffer_pct
        
        if point.type == 'high':
            # Check if we just swept this high
            if (current_candle['High'] > point.price + buffer or 
                prev_candle['High'] > point.price + buffer):
                # This is a potential bearish setup (swept high)
                return ('bearish', point.price, current_time)
                
        else:  # low
            # Check if we just swept this low
            if (current_candle['Low'] < point.price - buffer or 
                prev_candle['Low'] < point.price - buffer):
                # This is a potential bullish setup (swept low)
                return ('bullish', point.price, current_time)
    
    return None


def get_htf_context(
    h1_data: pd.DataFrame,
    m15_data: pd.DataFrame,
    current_time: datetime,
    lookback_hours: int = 24,
    fractal_lookback: int = 2,
    min_gap_pct: float = 0.0001
) -> Optional[Tuple[str, str]]:
    """
    Determine if we have a valid HTF context for trading.
    
    Checks for:
    1. Price retracing into an FVG zone (H1 or M15)
    2. Liquidity sweep on an old high/low
    
    Args:
        h1_data: 1-hour OHLC data
        m15_data: 15-minute OHLC data
        current_time: Current timestamp
        lookback_hours: How far back to look
        fractal_lookback: Fractal detection lookback
        min_gap_pct: Minimum FVG gap percentage
        
    Returns:
        Tuple of (trade_direction, context_type) if valid, None otherwise
        trade_direction: 'bullish' or 'bearish'
        context_type: 'fvg' or 'liquidity_sweep'
    """
    from fvg_detector import find_active_htf_fvg
    
    # Check for FVG first
    fvg = find_active_htf_fvg(h1_data, m15_data, current_time, lookback_hours, min_gap_pct)
    if fvg:
        return (fvg.direction, 'fvg')
    
    # Check for liquidity sweep
    liq_zone = find_active_liquidity_zone(h1_data, m15_data, current_time, lookback_hours * 2, fractal_lookback)
    if liq_zone:
        direction, _, _ = liq_zone
        return (direction, 'liquidity_sweep')
    
    return None

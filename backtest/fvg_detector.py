"""
Fair Value Gap (FVG) detection module.

An FVG (Fair Value Gap) is an imbalance in price action that creates a gap between:
- Bullish FVG: High of candle n-2 and Low of candle n (gap below current candle)
- Bearish FVG: Low of candle n-2 and High of candle n (gap above current candle)
"""
import pandas as pd
import numpy as np
from dataclasses import dataclass
from typing import List, Optional, Tuple
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


@dataclass
class FVG:
    """Represents a Fair Value Gap."""
    timestamp: datetime  # When the FVG was created (candle n)
    direction: str  # 'bullish' or 'bearish'
    top: float  # Upper boundary of the gap
    bottom: float  # Lower boundary of the gap
    is_filled: bool = False  # Whether the gap has been filled
    fill_timestamp: Optional[datetime] = None  # When it was filled
    
    @property
    def size(self) -> float:
        """Size of the gap in price units."""
        return self.top - self.bottom
    
    @property
    def midpoint(self) -> float:
        """Midpoint of the FVG zone."""
        return (self.top + self.bottom) / 2
    
    def contains_price(self, price: float) -> bool:
        """Check if a price is within the FVG zone."""
        return self.bottom <= price <= self.top


def detect_fvg(
    df: pd.DataFrame,
    min_gap_pct: float = 0.0001,
    log_results: bool = False
) -> List[FVG]:
    """
    Detect all Fair Value Gaps in the given OHLC data.
    
    Args:
        df: DataFrame with OHLC data (columns: Open, High, Low, Close)
        min_gap_pct: Minimum gap size as percentage of price to be considered valid
        log_results: Whether to log FVG detection results
        
    Returns:
        List of FVG objects detected in the data
    """
    fvgs = []
    
    if len(df) < 3:
        return fvgs
    
    # Get arrays for vectorized operations
    highs = df['High'].values
    lows = df['Low'].values
    timestamps = df.index.to_numpy()
    
    for i in range(2, len(df)):
        # Current candle (n), previous (n-1), and two back (n-2)
        high_n = highs[i]
        low_n = lows[i]
        high_n2 = highs[i-2]
        low_n2 = lows[i-2]
        
        current_price = (high_n + low_n) / 2
        min_gap = current_price * min_gap_pct
        
        # Bullish FVG: Gap between high of n-2 and low of n (price moved up quickly)
        # The gap is below the current candle
        if low_n > high_n2:
            gap_size = low_n - high_n2
            if gap_size >= min_gap:
                fvg = FVG(
                    timestamp=pd.Timestamp(timestamps[i]),
                    direction='bullish',
                    top=low_n,
                    bottom=high_n2,
                )
                fvgs.append(fvg)
                logger.debug(f"Bullish FVG at {fvg.timestamp}: {fvg.bottom:.2f} - {fvg.top:.2f}")
        
        # Bearish FVG: Gap between low of n-2 and high of n (price moved down quickly)
        # The gap is above the current candle
        if high_n < low_n2:
            gap_size = low_n2 - high_n
            if gap_size >= min_gap:
                fvg = FVG(
                    timestamp=pd.Timestamp(timestamps[i]),
                    direction='bearish',
                    top=low_n2,
                    bottom=high_n,
                )
                fvgs.append(fvg)
                logger.debug(f"Bearish FVG at {fvg.timestamp}: {fvg.bottom:.2f} - {fvg.top:.2f}")
    
    if log_results:
        logger.info(f"Detected {len(fvgs)} FVGs in data")
    return fvgs


def check_fvg_fill(
    fvg: FVG,
    df: pd.DataFrame,
    start_from: Optional[datetime] = None
) -> Tuple[bool, Optional[datetime], Optional[int]]:
    """
    Check if an FVG has been filled by subsequent price action.
    
    Args:
        fvg: The FVG to check
        df: DataFrame with OHLC data
        start_from: Optional timestamp to start checking from
        
    Returns:
        Tuple of (is_filled, fill_timestamp, candle_index)
    """
    # Get data after FVG creation
    start_ts = start_from if start_from else fvg.timestamp
    subsequent_data = df[df.index > start_ts]
    
    if len(subsequent_data) == 0:
        return False, None, None
    
    for idx, (ts, row) in enumerate(subsequent_data.iterrows()):
        # For bullish FVG: price needs to come down and touch the zone
        if fvg.direction == 'bullish':
            if row['Low'] <= fvg.top:  # Price entered the FVG zone from above
                return True, ts, idx
        # For bearish FVG: price needs to come up and touch the zone
        else:
            if row['High'] >= fvg.bottom:  # Price entered the FVG zone from below
                return True, ts, idx
    
    return False, None, None


def find_active_htf_fvg(
    h1_data: pd.DataFrame,
    m15_data: pd.DataFrame,
    current_time: datetime,
    lookback_hours: int = 24,
    min_gap_pct: float = 0.0001,
    zone_tolerance_upper: float = 1.001,
    zone_tolerance_lower: float = 0.999
) -> Optional[FVG]:
    """
    Find an active (unfilled) HTF FVG that price is currently in or approaching.
    
    Args:
        h1_data: 1-hour OHLC data
        m15_data: 15-minute OHLC data
        current_time: Current timestamp to evaluate
        lookback_hours: How far back to look for FVGs
        min_gap_pct: Minimum gap percentage
        zone_tolerance_upper: Upper tolerance multiplier for zone interaction
        zone_tolerance_lower: Lower tolerance multiplier for zone interaction
        
    Returns:
        Active FVG if found, None otherwise
    """
    from datetime import timedelta
    
    lookback_start = current_time - timedelta(hours=lookback_hours)
    
    # Check H1 FVGs first
    h1_window = h1_data[(h1_data.index >= lookback_start) & (h1_data.index < current_time)]
    h1_fvgs = detect_fvg(h1_window, min_gap_pct)
    
    # Check M15 FVGs
    m15_window = m15_data[(m15_data.index >= lookback_start) & (m15_data.index < current_time)]
    m15_fvgs = detect_fvg(m15_window, min_gap_pct)
    
    all_fvgs = h1_fvgs + m15_fvgs
    
    # Sort by timestamp, most recent first
    all_fvgs.sort(key=lambda x: x.timestamp, reverse=True)
    
    # Get current price from the most recent data
    if current_time in h1_data.index:
        current_high = h1_data.loc[current_time, 'High']
        current_low = h1_data.loc[current_time, 'Low']
    elif len(m15_data[m15_data.index <= current_time]) > 0:
        latest = m15_data[m15_data.index <= current_time].iloc[-1]
        current_high = latest['High']
        current_low = latest['Low']
    else:
        return None
    
    # Find FVG that price is currently interacting with
    for fvg in all_fvgs:
        # Check if current price is in or near the FVG zone
        if fvg.direction == 'bullish':
            # For bullish FVG, price should be coming down into it
            if current_low <= fvg.top * zone_tolerance_upper:
                # Verify it hasn't been completely filled
                check_data = h1_data[(h1_data.index > fvg.timestamp) & (h1_data.index < current_time)]
                if len(check_data) > 0:
                    if check_data['Low'].min() > fvg.bottom:
                        return fvg
                else:
                    return fvg
        else:
            # For bearish FVG, price should be coming up into it
            if current_high >= fvg.bottom * zone_tolerance_lower:
                # Verify it hasn't been completely filled
                check_data = h1_data[(h1_data.index > fvg.timestamp) & (h1_data.index < current_time)]
                if len(check_data) > 0:
                    if check_data['High'].max() < fvg.top:
                        return fvg
                else:
                    return fvg
    
    return None


def detect_m5_fvg_for_entry(
    m5_data: pd.DataFrame,
    start_time: datetime,
    direction: str,
    max_candles: int = 50,
    min_gap_pct: float = 0.0001
) -> Optional[Tuple[FVG, datetime, pd.Series]]:
    """
    Detect M5 FVG formation and subsequent fill for entry signal.
    
    Args:
        m5_data: 5-minute OHLC data
        start_time: Time to start looking for FVG
        direction: Expected trade direction ('bullish' or 'bearish')
        max_candles: Maximum candles to look ahead
        min_gap_pct: Minimum gap percentage
        
    Returns:
        Tuple of (fvg, fill_time, reversal_candle) if entry signal found, None otherwise
    """
    # Get M5 data from start_time
    window_data = m5_data[m5_data.index >= start_time].head(max_candles)
    
    if len(window_data) < 5:
        return None
    
    # Detect FVGs in this window
    for i in range(2, len(window_data) - 2):
        sub_df = window_data.iloc[:i+1]
        fvgs = detect_fvg(sub_df, min_gap_pct)
        
        # Filter for FVGs matching our direction
        matching_fvgs = [f for f in fvgs if f.direction == direction and f.timestamp == sub_df.index[i]]
        
        if not matching_fvgs:
            continue
        
        fvg = matching_fvgs[-1]  # Take the most recent
        
        # Look for fill and reversal in subsequent candles
        remaining = window_data.iloc[i+1:]
        
        for j in range(len(remaining)):
            candle = remaining.iloc[j]
            candle_time = remaining.index[j]
            
            # Check if price came back to fill the FVG
            if fvg.direction == 'bullish':
                # Price should come down and touch the FVG zone, then reverse up
                if candle['Low'] <= fvg.top:
                    # Check for reversal (close above the low, showing rejection)
                    if j + 1 < len(remaining):
                        next_candle = remaining.iloc[j + 1]
                        # Bullish reversal: close higher than open, showing buying pressure
                        if next_candle['Close'] > next_candle['Open']:
                            return (fvg, remaining.index[j + 1], next_candle)
            else:
                # Price should come up and touch the FVG zone, then reverse down
                if candle['High'] >= fvg.bottom:
                    # Check for reversal
                    if j + 1 < len(remaining):
                        next_candle = remaining.iloc[j + 1]
                        # Bearish reversal: close lower than open, showing selling pressure
                        if next_candle['Close'] < next_candle['Open']:
                            return (fvg, remaining.index[j + 1], next_candle)
    
    return None

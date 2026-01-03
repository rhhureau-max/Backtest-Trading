"""
Fair Value Gap (FVG) Detection Module
Implements ICT-style FVG detection for entry signals
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Optional
from dataclasses import dataclass


@dataclass
class FVG:
    """Represents a Fair Value Gap"""
    start_time: pd.Timestamp
    end_time: pd.Timestamp
    gap_high: float
    gap_low: float
    fvg_type: str  # 'bullish' or 'bearish'
    filled: bool = False
    
    def is_in_zone(self, price: float) -> bool:
        """Check if price is within the FVG zone"""
        return self.gap_low <= price <= self.gap_high
    
    def __repr__(self):
        return f"FVG({self.fvg_type}, {self.gap_low:.2f}-{self.gap_high:.2f}, filled={self.filled})"


class FVGDetector:
    """Detects and tracks Fair Value Gaps"""
    
    def __init__(self, max_fvgs_to_track: int = 10):
        """
        Args:
            max_fvgs_to_track: Maximum number of unfilled FVGs to track at once
        """
        self.max_fvgs_to_track = max_fvgs_to_track
        self.active_fvgs: List[FVG] = []
    
    def detect_fvgs(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Detect FVGs in the DataFrame (Vectorized for performance)
        
        Bearish FVG: Gap between candle[i-2].Low and candle[i].High
                     where candle[i-2].Low > candle[i].High
        
        Bullish FVG: Gap between candle[i-2].High and candle[i].Low
                     where candle[i-2].High < candle[i].Low
        
        Args:
            df: DataFrame with OHLC data
            
        Returns:
            DataFrame with added FVG columns
        """
        df = df.copy()
        
        # Shift data for vectorized comparison
        low_shifted = df['Low'].shift(2)  # candle[i-2].Low
        high_shifted = df['High'].shift(2)  # candle[i-2].High
        
        # Bearish FVG: candle[i-2].Low > candle[i].High
        df['bearish_fvg'] = low_shifted > df['High']
        df['bearish_fvg_high'] = np.where(df['bearish_fvg'], low_shifted, np.nan)
        df['bearish_fvg_low'] = np.where(df['bearish_fvg'], df['High'], np.nan)
        
        # Bullish FVG: candle[i-2].High < candle[i].Low
        df['bullish_fvg'] = high_shifted < df['Low']
        df['bullish_fvg_high'] = np.where(df['bullish_fvg'], df['Low'], np.nan)
        df['bullish_fvg_low'] = np.where(df['bullish_fvg'], high_shifted, np.nan)
        
        return df
    
    def add_fvg(self, fvg: FVG):
        """Add a new FVG to tracking list"""
        self.active_fvgs.append(fvg)
        
        # Keep only unfilled FVGs and limit the number tracked
        self.active_fvgs = [f for f in self.active_fvgs if not f.filled]
        if len(self.active_fvgs) > self.max_fvgs_to_track:
            self.active_fvgs = self.active_fvgs[-self.max_fvgs_to_track:]
    
    def update_fvgs(self, current_high: float, current_low: float):
        """Update FVG filled status based on current price action"""
        for fvg in self.active_fvgs:
            if not fvg.filled:
                # FVG is filled if price moves through it
                if current_low <= fvg.gap_low or current_high >= fvg.gap_high:
                    fvg.filled = True
    
    def get_unfilled_fvgs(self, fvg_type: str = None) -> List[FVG]:
        """
        Get list of unfilled FVGs
        
        Args:
            fvg_type: Optional filter for 'bullish' or 'bearish'
            
        Returns:
            List of unfilled FVGs
        """
        unfilled = [f for f in self.active_fvgs if not f.filled]
        
        if fvg_type:
            unfilled = [f for f in unfilled if f.fvg_type == fvg_type]
        
        return unfilled
    
    def check_fvg_inversion_long(self, close_price: float) -> Optional[FVG]:
        """
        Check if price has closed above a bearish FVG (bullish inversion)
        
        Args:
            close_price: Current candle close price
            
        Returns:
            FVG that was inverted, or None
        """
        bearish_fvgs = self.get_unfilled_fvgs('bearish')
        
        for fvg in bearish_fvgs:
            # Price closed above the bearish FVG (FVG becomes support)
            if close_price > fvg.gap_high:
                return fvg
        
        return None
    
    def check_fvg_inversion_short(self, close_price: float) -> Optional[FVG]:
        """
        Check if price has closed below a bullish FVG (bearish inversion)
        
        Args:
            close_price: Current candle close price
            
        Returns:
            FVG that was inverted, or None
        """
        bullish_fvgs = self.get_unfilled_fvgs('bullish')
        
        for fvg in bullish_fvgs:
            # Price closed below the bullish FVG (FVG becomes resistance)
            if close_price < fvg.gap_low:
                return fvg
        
        return None


class FVGTracker:
    """Manages FVG detection and tracking for backtesting"""
    
    def __init__(self, data_1m: pd.DataFrame):
        """
        Args:
            data_1m: 1-minute OHLC data with DateTime as index
        """
        self.detector = FVGDetector()
        
        print("Detecting FVGs on 1-minute data...")
        self.data_1m = self.detector.detect_fvgs(data_1m)
        
        # Count FVGs
        bearish_count = self.data_1m['bearish_fvg'].sum()
        bullish_count = self.data_1m['bullish_fvg'].sum()
        print(f"  ✓ Found {bearish_count} Bearish FVGs")
        print(f"  ✓ Found {bullish_count} Bullish FVGs")
    
    def get_data_at_time(self, timestamp: pd.Timestamp) -> Optional[pd.Series]:
        """Get 1-minute bar at or before a specific timestamp"""
        idx = self.data_1m.index.searchsorted(timestamp, side='right') - 1
        if idx < 0 or idx >= len(self.data_1m):
            return None
        return self.data_1m.iloc[idx]
    
    def get_recent_fvgs(self, timestamp: pd.Timestamp, lookback_minutes: int = 120) -> List[Dict]:
        """
        Get FVGs created in the recent past
        
        Args:
            timestamp: Current timestamp
            lookback_minutes: How many minutes to look back
            
        Returns:
            List of FVG dictionaries
        """
        start_time = timestamp - pd.Timedelta(minutes=lookback_minutes)
        
        mask = (self.data_1m.index >= start_time) & (self.data_1m.index <= timestamp)
        recent_data = self.data_1m[mask]
        
        fvgs = []
        
        # Collect bearish FVGs
        bearish_mask = recent_data['bearish_fvg'] == True
        for idx, row in recent_data[bearish_mask].iterrows():
            fvgs.append({
                'time': idx,
                'type': 'bearish',
                'high': row['bearish_fvg_high'],
                'low': row['bearish_fvg_low']
            })
        
        # Collect bullish FVGs
        bullish_mask = recent_data['bullish_fvg'] == True
        for idx, row in recent_data[bullish_mask].iterrows():
            fvgs.append({
                'time': idx,
                'type': 'bullish',
                'high': row['bullish_fvg_high'],
                'low': row['bullish_fvg_low']
            })
        
        return fvgs


if __name__ == "__main__":
    # Test FVG detection
    from data_loader import get_market_data
    
    print("Testing FVG Detection...")
    data = get_market_data()
    
    tracker = FVGTracker(data['1m'])
    
    # Test getting recent FVGs
    test_date = pd.Timestamp('2024-03-15 10:30:00', tz='US/Central')
    recent_fvgs = tracker.get_recent_fvgs(test_date, lookback_minutes=60)
    print(f"\nFVGs in the hour before {test_date}: {len(recent_fvgs)}")
    
    if recent_fvgs:
        print("\nSample FVGs:")
        for fvg in recent_fvgs[:3]:
            print(f"  {fvg}")

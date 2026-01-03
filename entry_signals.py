"""
Entry Signal Generation Module
Implements the complete entry logic with opening range, breakout, and FVG inversion
"""

import pandas as pd
import numpy as np
from typing import Optional, Dict, List, Tuple
from dataclasses import dataclass
from datetime import time


@dataclass
class OpeningRange:
    """Represents the 08:30 opening range"""
    date: pd.Timestamp
    high: float
    low: float
    
    def __repr__(self):
        return f"OpeningRange({self.date.date()}, {self.low:.2f}-{self.high:.2f})"


@dataclass
class EntrySignal:
    """Represents a trade entry signal"""
    timestamp: pd.Timestamp
    direction: str  # 'LONG' or 'SHORT'
    entry_price: float
    reason: str
    opening_range: OpeningRange
    
    def __repr__(self):
        return f"EntrySignal({self.direction}, {self.entry_price:.2f}, {self.timestamp})"


class EntrySignalGenerator:
    """Generates entry signals based on opening range and FVG inversions"""
    
    def __init__(self, data_1m: pd.DataFrame, data_5m: pd.DataFrame):
        """
        Args:
            data_1m: 1-minute OHLC data
            data_5m: 5-minute OHLC data
        """
        self.data_1m = data_1m.copy()
        self.data_5m = data_5m.copy()
        
        # Set DateTime as index for easier lookup
        if 'DateTime' in self.data_1m.columns:
            self.data_1m = self.data_1m.set_index('DateTime')
        if 'DateTime' in self.data_5m.columns:
            self.data_5m = self.data_5m.set_index('DateTime')
    
    def get_opening_range(self, date: pd.Timestamp) -> Optional[OpeningRange]:
        """
        Get the 08:30 opening range for a specific date
        
        Args:
            date: Date to get opening range for
            
        Returns:
            OpeningRange object or None if not found
        """
        # Create timestamp for 08:30 on this date
        target_time = date.replace(hour=8, minute=30, second=0, microsecond=0)
        
        # Find the 5-minute candle at 08:30
        try:
            # Look for candles within a 5-minute window
            start_window = target_time - pd.Timedelta(minutes=2)
            end_window = target_time + pd.Timedelta(minutes=5)
            
            mask = (self.data_5m.index >= start_window) & (self.data_5m.index <= end_window)
            candles = self.data_5m[mask]
            
            if len(candles) == 0:
                return None
            
            # Get the candle closest to 08:30
            time_diffs = abs((candles.index - target_time).total_seconds())
            closest_idx = time_diffs.argmin()
            candle = candles.iloc[closest_idx]
            
            return OpeningRange(
                date=candles.index[closest_idx],
                high=candle['High'],
                low=candle['Low']
            )
            
        except Exception as e:
            return None
    
    def check_breakout_and_return(
        self,
        opening_range: OpeningRange,
        current_time: pd.Timestamp,
        lookback_minutes: int = 60
    ) -> Optional[str]:
        """
        Check if price broke out of the opening range and returned
        
        Args:
            opening_range: The opening range to check against
            current_time: Current timestamp
            lookback_minutes: How far back to check for breakout
            
        Returns:
            'broke_high' or 'broke_low' if condition met, None otherwise
        """
        # Get data from opening range close to current time
        start_time = opening_range.date + pd.Timedelta(minutes=5)
        end_time = current_time
        
        mask = (self.data_1m.index >= start_time) & (self.data_1m.index <= end_time)
        recent_data = self.data_1m[mask]
        
        if len(recent_data) == 0:
            return None
        
        # Check if price broke above the range high
        broke_high = (recent_data['High'] > opening_range.high).any()
        
        # Check if price broke below the range low
        broke_low = (recent_data['Low'] < opening_range.low).any()
        
        # Check if price is currently back in or near the range
        current_candle = recent_data.iloc[-1]
        current_price = current_candle['Close']
        
        # Allow some tolerance for "return to range"
        tolerance = 5  # 5 points
        in_range = (current_price >= opening_range.low - tolerance and 
                   current_price <= opening_range.high + tolerance)
        
        if broke_high and in_range:
            return 'broke_high'
        elif broke_low and in_range:
            return 'broke_low'
        
        return None
    
    def check_long_setup(
        self,
        opening_range: OpeningRange,
        current_time: pd.Timestamp,
        fvg_data: pd.DataFrame
    ) -> Optional[EntrySignal]:
        """
        Check for LONG entry setup
        
        Conditions:
        1. Price broke out of opening range
        2. Price returned to range
        3. Bearish FVG was created
        4. Current candle closed above the bearish FVG
        
        Args:
            opening_range: Opening range for the day
            current_time: Current timestamp
            fvg_data: 1-minute data with FVG detection
            
        Returns:
            EntrySignal or None
        """
        # Check breakout and return
        breakout_status = self.check_breakout_and_return(opening_range, current_time)
        
        if breakout_status is None:
            return None
        
        # Look for recent bearish FVGs (last 2 hours)
        lookback_time = current_time - pd.Timedelta(minutes=120)
        mask = (fvg_data.index >= lookback_time) & (fvg_data.index <= current_time)
        recent_fvg_data = fvg_data[mask]
        
        # Find bearish FVGs
        bearish_fvgs = recent_fvg_data[recent_fvg_data['bearish_fvg'] == True]
        
        if len(bearish_fvgs) == 0:
            return None
        
        # Get current candle
        try:
            current_candle = fvg_data.loc[current_time]
        except:
            return None
        
        current_close = current_candle['Close']
        
        # Check if current close is above any recent bearish FVG (inversion)
        for idx, fvg_row in bearish_fvgs.iterrows():
            fvg_high = fvg_row['bearish_fvg_high']
            fvg_low = fvg_row['bearish_fvg_low']
            
            # Entry signal: closed above the bearish FVG
            if current_close > fvg_high:
                return EntrySignal(
                    timestamp=current_time,
                    direction='LONG',
                    entry_price=current_close,
                    reason=f"Bearish FVG inversion (FVG: {fvg_low:.2f}-{fvg_high:.2f})",
                    opening_range=opening_range
                )
        
        return None
    
    def check_short_setup(
        self,
        opening_range: OpeningRange,
        current_time: pd.Timestamp,
        fvg_data: pd.DataFrame
    ) -> Optional[EntrySignal]:
        """
        Check for SHORT entry setup
        
        Conditions:
        1. Price broke out of opening range
        2. Price returned to range
        3. Bullish FVG was created
        4. Current candle closed below the bullish FVG
        
        Args:
            opening_range: Opening range for the day
            current_time: Current timestamp
            fvg_data: 1-minute data with FVG detection
            
        Returns:
            EntrySignal or None
        """
        # Check breakout and return
        breakout_status = self.check_breakout_and_return(opening_range, current_time)
        
        if breakout_status is None:
            return None
        
        # Look for recent bullish FVGs (last 2 hours)
        lookback_time = current_time - pd.Timedelta(minutes=120)
        mask = (fvg_data.index >= lookback_time) & (fvg_data.index <= current_time)
        recent_fvg_data = fvg_data[mask]
        
        # Find bullish FVGs
        bullish_fvgs = recent_fvg_data[recent_fvg_data['bullish_fvg'] == True]
        
        if len(bullish_fvgs) == 0:
            return None
        
        # Get current candle
        try:
            current_candle = fvg_data.loc[current_time]
        except:
            return None
        
        current_close = current_candle['Close']
        
        # Check if current close is below any recent bullish FVG (inversion)
        for idx, fvg_row in bullish_fvgs.iterrows():
            fvg_high = fvg_row['bullish_fvg_high']
            fvg_low = fvg_row['bullish_fvg_low']
            
            # Entry signal: closed below the bullish FVG
            if current_close < fvg_low:
                return EntrySignal(
                    timestamp=current_time,
                    direction='SHORT',
                    entry_price=current_close,
                    reason=f"Bullish FVG inversion (FVG: {fvg_low:.2f}-{fvg_high:.2f})",
                    opening_range=opening_range
                )
        
        return None
    
    def is_in_trading_window(self, timestamp: pd.Timestamp) -> bool:
        """
        Check if timestamp is in the trading window (08:35 - 11:00)
        
        Args:
            timestamp: Timestamp to check
            
        Returns:
            True if in trading window
        """
        t = timestamp.time()
        return time(8, 35) <= t <= time(11, 0)


if __name__ == "__main__":
    # Test entry signal generation
    from data_loader import get_market_data
    from fvg_detector import FVGDetector
    
    print("Testing Entry Signal Generation...")
    data = get_market_data()
    
    # Detect FVGs
    detector = FVGDetector()
    fvg_data = detector.detect_fvgs(data['1m'])
    
    # Create signal generator
    signal_gen = EntrySignalGenerator(data['1m'], data['5m'])
    
    # Test getting opening range for a specific date
    test_date = pd.Timestamp('2024-03-15', tz='US/Central')
    opening_range = signal_gen.get_opening_range(test_date)
    
    if opening_range:
        print(f"\nOpening Range for {test_date.date()}: {opening_range}")
    else:
        print(f"\nNo opening range found for {test_date.date()}")

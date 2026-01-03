"""
Simplified Entry Signal Generation Module
ICT 2022 Model with permissive FVG touch entry
"""

import pandas as pd
import numpy as np
from typing import Optional, Dict, List
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
    fvg_touched: Dict[str, float]  # Details of the FVG
    
    def __repr__(self):
        return f"EntrySignal({self.direction}, {self.entry_price:.2f}, {self.timestamp})"


class SimplifiedEntrySignalGenerator:
    """Simplified entry logic - trade on any FVG touch after liquidity grab"""
    
    def __init__(self, data_1m: pd.DataFrame, data_5m: pd.DataFrame, min_fvg_size: float = 2.0):
        """
        Args:
            data_1m: 1-minute OHLC data
            data_5m: 5-minute OHLC data
            min_fvg_size: Minimum FVG size in points (default: 2.0)
        """
        self.data_1m = data_1m.copy()
        self.data_5m = data_5m.copy()
        self.min_fvg_size = min_fvg_size
        
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
    
    def check_liquidity_grab(
        self,
        opening_range: OpeningRange,
        current_time: pd.Timestamp
    ) -> Optional[str]:
        """
        Check if price grabbed liquidity (broke opening range high or low)
        
        Args:
            opening_range: The opening range to check against
            current_time: Current timestamp
            
        Returns:
            'grabbed_high' or 'grabbed_low' if liquidity taken, None otherwise
        """
        # Get data from after opening range to current time
        start_time = opening_range.date + pd.Timedelta(minutes=5)
        end_time = current_time
        
        mask = (self.data_1m.index >= start_time) & (self.data_1m.index <= end_time)
        recent_data = self.data_1m[mask]
        
        if len(recent_data) == 0:
            return None
        
        # Check if price broke above the range high (grabbed buy-side liquidity)
        broke_high = (recent_data['High'] > opening_range.high).any()
        
        # Check if price broke below the range low (grabbed sell-side liquidity)
        broke_low = (recent_data['Low'] < opening_range.low).any()
        
        # Return the first liquidity grab that occurred
        if broke_low:
            return 'grabbed_low'  # For LONG setups
        elif broke_high:
            return 'grabbed_high'  # For SHORT setups
        
        return None
    
    def find_recent_fvgs(
        self,
        fvg_data: pd.DataFrame,
        current_time: pd.Timestamp,
        direction: str,
        lookback_bars: int = 30
    ) -> List[Dict]:
        """
        Find recent FVGs of the specified type
        
        Args:
            fvg_data: DataFrame with FVG columns
            current_time: Current timestamp
            direction: 'bullish' or 'bearish'
            lookback_bars: Number of bars to look back
            
        Returns:
            List of FVG dictionaries
        """
        # Get recent data
        idx = fvg_data.index.searchsorted(current_time, side='right') - 1
        if idx < lookback_bars:
            start_idx = 0
        else:
            start_idx = idx - lookback_bars
        
        recent_data = fvg_data.iloc[start_idx:idx+1]
        
        fvgs = []
        
        if direction == 'bullish':
            # Find bullish FVGs
            mask = recent_data['bullish_fvg'] == True
            for idx, row in recent_data[mask].iterrows():
                fvg_size = row['bullish_fvg_high'] - row['bullish_fvg_low']
                if fvg_size >= self.min_fvg_size:
                    fvgs.append({
                        'time': idx,
                        'type': 'bullish',
                        'high': row['bullish_fvg_high'],
                        'low': row['bullish_fvg_low'],
                        'size': fvg_size
                    })
        else:  # bearish
            # Find bearish FVGs
            mask = recent_data['bearish_fvg'] == True
            for idx, row in recent_data[mask].iterrows():
                fvg_size = row['bearish_fvg_high'] - row['bearish_fvg_low']
                if fvg_size >= self.min_fvg_size:
                    fvgs.append({
                        'time': idx,
                        'type': 'bearish',
                        'high': row['bearish_fvg_high'],
                        'low': row['bearish_fvg_low'],
                        'size': fvg_size
                    })
        
        return fvgs
    
    def check_fvg_touch(
        self,
        current_candle: pd.Series,
        fvg: Dict
    ) -> bool:
        """
        Check if current candle touched/entered the FVG zone
        
        Args:
            current_candle: Current 1-minute candle
            fvg: FVG dictionary with high/low
            
        Returns:
            True if FVG was touched
        """
        candle_low = current_candle['Low']
        candle_high = current_candle['High']
        
        # Check if candle overlaps with FVG zone
        touched = not (candle_high < fvg['low'] or candle_low > fvg['high'])
        
        return touched
    
    def check_long_setup(
        self,
        opening_range: OpeningRange,
        current_time: pd.Timestamp,
        current_candle: pd.Series,
        fvg_data: pd.DataFrame,
        liquidity_status: str
    ) -> Optional[EntrySignal]:
        """
        Check for LONG entry setup (after grabbing low-side liquidity)
        
        Args:
            opening_range: Opening range object
            current_time: Current timestamp
            current_candle: Current 1-minute candle
            fvg_data: DataFrame with FVG data
            liquidity_status: Current liquidity grab status
            
        Returns:
            EntrySignal if setup is valid, None otherwise
        """
        # Need to have grabbed the low first
        if liquidity_status != 'grabbed_low':
            return None
        
        # Find recent bullish FVGs
        fvgs = self.find_recent_fvgs(fvg_data, current_time, 'bullish')
        
        if not fvgs:
            return None
        
        # Check if current candle touches any FVG
        for fvg in fvgs:
            if self.check_fvg_touch(current_candle, fvg):
                # Entry on FVG touch - use close price
                entry_price = current_candle['Close']
                
                return EntrySignal(
                    timestamp=current_time,
                    direction='LONG',
                    entry_price=entry_price,
                    reason=f"Bullish FVG touch after liquidity grab (FVG: {fvg['low']:.2f}-{fvg['high']:.2f})",
                    opening_range=opening_range,
                    fvg_touched=fvg
                )
        
        return None
    
    def check_short_setup(
        self,
        opening_range: OpeningRange,
        current_time: pd.Timestamp,
        current_candle: pd.Series,
        fvg_data: pd.DataFrame,
        liquidity_status: str
    ) -> Optional[EntrySignal]:
        """
        Check for SHORT entry setup (after grabbing high-side liquidity)
        
        Args:
            opening_range: Opening range object
            current_time: Current timestamp
            current_candle: Current 1-minute candle
            fvg_data: DataFrame with FVG data
            liquidity_status: Current liquidity grab status
            
        Returns:
            EntrySignal if setup is valid, None otherwise
        """
        # Need to have grabbed the high first
        if liquidity_status != 'grabbed_high':
            return None
        
        # Find recent bearish FVGs
        fvgs = self.find_recent_fvgs(fvg_data, current_time, 'bearish')
        
        if not fvgs:
            return None
        
        # Check if current candle touches any FVG
        for fvg in fvgs:
            if self.check_fvg_touch(current_candle, fvg):
                # Entry on FVG touch - use close price
                entry_price = current_candle['Close']
                
                return EntrySignal(
                    timestamp=current_time,
                    direction='SHORT',
                    entry_price=entry_price,
                    reason=f"Bearish FVG touch after liquidity grab (FVG: {fvg['low']:.2f}-{fvg['high']:.2f})",
                    opening_range=opening_range,
                    fvg_touched=fvg
                )
        
        return None


if __name__ == "__main__":
    # Test the entry signal generator
    from data_loader import get_market_data
    from fvg_detector import FVGDetector
    
    print("Testing Simplified Entry Signal Generator...")
    data = get_market_data()
    
    # Detect FVGs
    detector = FVGDetector()
    fvg_data = detector.detect_fvgs(data['1m'])
    
    generator = SimplifiedEntrySignalGenerator(data['1m'], data['5m'])
    
    # Test on a specific date
    test_date = pd.Timestamp('2021-08-16', tz='US/Central')
    opening_range = generator.get_opening_range(test_date)
    
    if opening_range:
        print(f"Opening Range: {opening_range}")

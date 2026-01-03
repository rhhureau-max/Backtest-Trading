"""
Market Structure Detection Module
Implements Higher Highs/Higher Lows (bullish) and Lower Highs/Lower Lows (bearish) detection
"""

import pandas as pd
import numpy as np
from typing import Tuple, Optional


class MarketStructureDetector:
    """Detects market structure (HH/HL or LH/LL) on higher timeframes"""
    
    def __init__(self, lookback_window: int = 20):
        """
        Args:
            lookback_window: Number of candles to analyze for structure (default: 20)
        """
        self.lookback_window = lookback_window
    
    def find_swing_points(self, df: pd.DataFrame, window: int = 5) -> Tuple[pd.Series, pd.Series]:
        """
        Identify swing highs and swing lows
        
        Args:
            df: DataFrame with OHLC data
            window: Window size for identifying pivots
            
        Returns:
            Tuple of (swing_highs, swing_lows) as boolean Series
        """
        highs = df['High'].values
        lows = df['Low'].values
        
        swing_highs = np.zeros(len(df), dtype=bool)
        swing_lows = np.zeros(len(df), dtype=bool)
        
        for i in range(window, len(df) - window):
            # Swing high: highest point in the window
            if highs[i] == max(highs[i-window:i+window+1]):
                swing_highs[i] = True
            
            # Swing low: lowest point in the window
            if lows[i] == min(lows[i-window:i+window+1]):
                swing_lows[i] = True
        
        return pd.Series(swing_highs, index=df.index), pd.Series(swing_lows, index=df.index)
    
    def detect_structure_type(self, df: pd.DataFrame, end_idx: int) -> str:
        """
        Detect if recent structure is bullish (HH/HL) or bearish (LH/LL)
        
        Args:
            df: DataFrame with OHLC data and swing points
            end_idx: Index to analyze up to
            
        Returns:
            'bullish', 'bearish', or 'neutral'
        """
        start_idx = max(0, end_idx - self.lookback_window)
        
        if start_idx >= end_idx:
            return 'neutral'
        
        window_df = df.iloc[start_idx:end_idx+1].copy()
        
        # Get swing points in this window
        swing_highs_mask = window_df['swing_high'] == True
        swing_lows_mask = window_df['swing_low'] == True
        
        swing_high_values = window_df.loc[swing_highs_mask, 'High'].values
        swing_low_values = window_df.loc[swing_lows_mask, 'Low'].values
        
        # Need at least 2 swings to determine structure
        if len(swing_high_values) < 2 or len(swing_low_values) < 2:
            return 'neutral'
        
        # Check for Higher Highs and Higher Lows (Bullish)
        hh_count = 0
        hl_count = 0
        for i in range(1, len(swing_high_values)):
            if swing_high_values[i] > swing_high_values[i-1]:
                hh_count += 1
        
        for i in range(1, len(swing_low_values)):
            if swing_low_values[i] > swing_low_values[i-1]:
                hl_count += 1
        
        # Check for Lower Highs and Lower Lows (Bearish)
        lh_count = 0
        ll_count = 0
        for i in range(1, len(swing_high_values)):
            if swing_high_values[i] < swing_high_values[i-1]:
                lh_count += 1
        
        for i in range(1, len(swing_low_values)):
            if swing_low_values[i] < swing_low_values[i-1]:
                ll_count += 1
        
        # Determine structure
        bullish_signals = hh_count + hl_count
        bearish_signals = lh_count + ll_count
        
        if bullish_signals > bearish_signals and bullish_signals >= 2:
            return 'bullish'
        elif bearish_signals > bullish_signals and bearish_signals >= 2:
            return 'bearish'
        else:
            return 'neutral'
    
    def add_structure_to_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Add market structure columns to DataFrame
        
        Args:
            df: DataFrame with OHLC data
            
        Returns:
            DataFrame with added 'swing_high', 'swing_low', and 'structure' columns
        """
        df = df.copy()
        
        # Find swing points
        df['swing_high'], df['swing_low'] = self.find_swing_points(df)
        
        # Detect structure for each bar
        structure = []
        for i in range(len(df)):
            struct = self.detect_structure_type(df, i)
            structure.append(struct)
        
        df['structure'] = structure
        
        return df


def get_trend_alignment(h1_structure: str, h4_structure: str) -> Optional[str]:
    """
    Determine overall trend based on H1 and H4 alignment
    
    Args:
        h1_structure: Structure on H1 timeframe ('bullish', 'bearish', 'neutral')
        h4_structure: Structure on H4 timeframe ('bullish', 'bearish', 'neutral')
        
    Returns:
        'bullish' if both are bullish, 'bearish' if both are bearish, None otherwise
    """
    if h1_structure == 'bullish' and h4_structure == 'bullish':
        return 'bullish'
    elif h1_structure == 'bearish' and h4_structure == 'bearish':
        return 'bearish'
    else:
        return None


class TrendFilter:
    """Manages trend filtering across multiple timeframes"""
    
    def __init__(self, h1_data: pd.DataFrame, h4_data: pd.DataFrame):
        """
        Args:
            h1_data: 1-hour OHLC data
            h4_data: 4-hour OHLC data
        """
        self.detector = MarketStructureDetector(lookback_window=20)
        
        # Add structure detection to both timeframes
        print("Detecting market structure on H1...")
        self.h1_data = self.detector.add_structure_to_dataframe(h1_data)
        
        print("Detecting market structure on H4...")
        self.h4_data = self.detector.add_structure_to_dataframe(h4_data)
        
        print("Market structure detection complete.")
    
    def get_trend_at_time(self, timestamp: pd.Timestamp) -> Optional[str]:
        """
        Get the overall trend at a specific timestamp
        
        Args:
            timestamp: Timestamp to check
            
        Returns:
            'bullish', 'bearish', or None
        """
        # Find nearest H1 bar
        h1_idx = self.h1_data.index.searchsorted(timestamp, side='right') - 1
        if h1_idx < 0 or h1_idx >= len(self.h1_data):
            return None
        h1_structure = self.h1_data.iloc[h1_idx]['structure']
        
        # Find nearest H4 bar
        h4_idx = self.h4_data.index.searchsorted(timestamp, side='right') - 1
        if h4_idx < 0 or h4_idx >= len(self.h4_data):
            return None
        h4_structure = self.h4_data.iloc[h4_idx]['structure']
        
        # Return aligned trend
        return get_trend_alignment(h1_structure, h4_structure)


if __name__ == "__main__":
    # Test the market structure detector
    from data_loader import get_market_data
    
    print("Testing Market Structure Detection...")
    data = get_market_data()
    
    trend_filter = TrendFilter(data['1H'], data['4H'])
    
    # Test at a specific date
    test_date = pd.Timestamp('2024-03-15 10:00:00', tz='US/Central')
    trend = trend_filter.get_trend_at_time(test_date)
    print(f"\nTrend at {test_date}: {trend}")

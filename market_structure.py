"""
Market Structure Detection Module
Implements SMC/ICT concepts: Asian Range, Daily Bias, FVG, MSS, Order Blocks, etc.
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple, Optional, List
from datetime import time, datetime, timedelta


class MarketStructureDetector:
    """Detects key market structure elements for SMC/ICT trading"""
    
    def __init__(self):
        self.asian_start = time(19, 0)  # 19:00 EST
        self.asian_end = time(0, 0)     # 00:00 EST (next day)
        self.london_start = time(2, 0)   # 02:00 EST
        self.london_end = time(5, 0)     # 05:00 EST
        
    def get_asian_range(self, df: pd.DataFrame, target_date: str) -> Optional[Dict]:
        """
        Calculate Asian session range (19:00-00:00 EST) for a given date
        
        Args:
            df: 5m or 15m dataframe with datetime index
            target_date: Date string 'YYYY-MM-DD'
            
        Returns:
            Dictionary with 'high', 'low', 'start_time', 'end_time' or None
        """
        try:
            target = pd.to_datetime(target_date).date()
            
            # Asian session starts at 19:00 on the target date
            # and ends at 00:00 on the next day
            start_dt = pd.Timestamp(year=target.year, month=target.month, 
                                    day=target.day, hour=19, minute=0)
            
            # End is 00:00 next day (5 hours later)
            end_dt = start_dt + timedelta(hours=5)
            
            # Filter data for Asian session
            asian_data = df[(df.index >= start_dt) & (df.index < end_dt)]
            
            if len(asian_data) == 0:
                return None
            
            asian_high = asian_data['High'].max()
            asian_low = asian_data['Low'].min()
            
            return {
                'high': asian_high,
                'low': asian_low,
                'start_time': start_dt,
                'end_time': end_dt,
                'range': asian_high - asian_low
            }
            
        except Exception as e:
            print(f"Error calculating Asian range for {target_date}: {str(e)}")
            return None
    
    def get_london_killzone(self, df: pd.DataFrame, target_date: str) -> pd.DataFrame:
        """
        Get London Killzone data (02:00-05:00 EST) for a given date
        
        Args:
            df: 5m or 15m dataframe
            target_date: Date string 'YYYY-MM-DD'
            
        Returns:
            DataFrame containing only London Killzone bars
        """
        try:
            target = pd.to_datetime(target_date).date()
            
            # London session is 02:00-05:00 on the day AFTER the Asian session date
            next_day = target + timedelta(days=1)
            
            start_dt = pd.Timestamp(year=next_day.year, month=next_day.month, 
                                    day=next_day.day, hour=2, minute=0)
            end_dt = pd.Timestamp(year=next_day.year, month=next_day.month, 
                                  day=next_day.day, hour=5, minute=0)
            
            # Filter for London Killzone
            london_data = df[(df.index >= start_dt) & (df.index < end_dt)]
            
            return london_data
            
        except Exception as e:
            print(f"Error getting London Killzone for {target_date}: {str(e)}")
            return pd.DataFrame()
    
    def determine_daily_bias(self, df_1h: pd.DataFrame, target_date: str, 
                             lookback_bars: int = 24) -> str:
        """
        Determine daily bias from H1 structure
        
        Args:
            df_1h: 1H dataframe
            target_date: Date to analyze
            lookback_bars: Number of H1 bars to analyze
            
        Returns:
            'BULLISH', 'BEARISH', or 'NEUTRAL'
        """
        try:
            target = pd.to_datetime(target_date).date()
            
            # Get data up to the target date (before London Killzone)
            # We want data BEFORE 02:00 on the day after target_date
            end_dt = pd.Timestamp(year=target.year, month=target.month, 
                                  day=target.day, hour=19, minute=0)
            
            # Get last N bars before Asian session
            h1_data = df_1h[df_1h.index <= end_dt].tail(lookback_bars)
            
            if len(h1_data) < 5:
                return 'NEUTRAL'
            
            # Detect Higher Highs and Higher Lows (bullish)
            # Detect Lower Highs and Lower Lows (bearish)
            highs = h1_data['High'].values
            lows = h1_data['Low'].values
            
            # Count swing points
            higher_highs = 0
            lower_highs = 0
            higher_lows = 0
            lower_lows = 0
            
            for i in range(2, len(highs)):
                # Check highs
                if highs[i] > highs[i-1] and highs[i-1] > highs[i-2]:
                    higher_highs += 1
                elif highs[i] < highs[i-1] and highs[i-1] < highs[i-2]:
                    lower_highs += 1
                
                # Check lows
                if lows[i] > lows[i-1] and lows[i-1] > lows[i-2]:
                    higher_lows += 1
                elif lows[i] < lows[i-1] and lows[i-1] < lows[i-2]:
                    lower_lows += 1
            
            # Determine bias
            bullish_score = higher_highs + higher_lows
            bearish_score = lower_highs + lower_lows
            
            if bullish_score > bearish_score * 1.5:
                return 'BULLISH'
            elif bearish_score > bullish_score * 1.5:
                return 'BEARISH'
            else:
                return 'NEUTRAL'
                
        except Exception as e:
            print(f"Error determining bias for {target_date}: {str(e)}")
            return 'NEUTRAL'
    
    def detect_fvg(self, df: pd.DataFrame, start_idx: int, end_idx: int) -> List[Dict]:
        """
        Detect Fair Value Gaps (FVG) in a price range
        
        A bullish FVG: Gap between candle[i-1].high and candle[i+1].low
        A bearish FVG: Gap between candle[i-1].low and candle[i+1].high
        
        Args:
            df: DataFrame with OHLC data
            start_idx: Start index in df
            end_idx: End index in df
            
        Returns:
            List of FVG dictionaries
        """
        fvgs = []
        
        if end_idx - start_idx < 3:
            return fvgs
        
        df_section = df.iloc[start_idx:end_idx]
        
        for i in range(1, len(df_section) - 1):
            prev_candle = df_section.iloc[i-1]
            curr_candle = df_section.iloc[i]
            next_candle = df_section.iloc[i+1]
            
            # Bullish FVG: gap up
            if prev_candle['High'] < next_candle['Low']:
                gap_size = next_candle['Low'] - prev_candle['High']
                fvgs.append({
                    'type': 'BULLISH',
                    'top': next_candle['Low'],
                    'bottom': prev_candle['High'],
                    'size': gap_size,
                    'time': df_section.index[i+1]
                })
            
            # Bearish FVG: gap down
            elif prev_candle['Low'] > next_candle['High']:
                gap_size = prev_candle['Low'] - next_candle['High']
                fvgs.append({
                    'type': 'BEARISH',
                    'top': prev_candle['Low'],
                    'bottom': next_candle['High'],
                    'size': gap_size,
                    'time': df_section.index[i+1]
                })
        
        return fvgs
    
    def detect_mss(self, df: pd.DataFrame, start_idx: int, end_idx: int, 
                   direction: str) -> Optional[Dict]:
        """
        Detect Market Structure Shift (MSS)
        
        Bullish MSS: Price breaks above recent swing high
        Bearish MSS: Price breaks below recent swing low
        
        Args:
            df: DataFrame with OHLC
            start_idx: Start index
            end_idx: End index
            direction: 'BULLISH' or 'BEARISH'
            
        Returns:
            MSS dictionary or None
        """
        if end_idx - start_idx < 5:
            return None
        
        df_section = df.iloc[start_idx:end_idx]
        
        if direction == 'BULLISH':
            # Look for break above recent swing high
            swing_high = df_section['High'].iloc[:-2].max()
            
            for i in range(len(df_section) - 2, len(df_section)):
                if df_section['Close'].iloc[i] > swing_high:
                    return {
                        'direction': 'BULLISH',
                        'level': swing_high,
                        'break_time': df_section.index[i],
                        'break_price': df_section['Close'].iloc[i]
                    }
        
        elif direction == 'BEARISH':
            # Look for break below recent swing low
            swing_low = df_section['Low'].iloc[:-2].min()
            
            for i in range(len(df_section) - 2, len(df_section)):
                if df_section['Close'].iloc[i] < swing_low:
                    return {
                        'direction': 'BEARISH',
                        'level': swing_low,
                        'break_time': df_section.index[i],
                        'break_price': df_section['Close'].iloc[i]
                    }
        
        return None
    
    def find_order_blocks(self, df_1h: pd.DataFrame, target_date: str, 
                          direction: str) -> List[Dict]:
        """
        Find H1 Order Blocks (last opposite candle before strong move)
        
        Args:
            df_1h: 1H dataframe
            target_date: Date to analyze
            direction: 'BULLISH' or 'BEARISH'
            
        Returns:
            List of order block dictionaries
        """
        order_blocks = []
        
        try:
            target = pd.to_datetime(target_date).date()
            
            # Look at last 48 H1 bars (2 days)
            end_dt = pd.Timestamp(year=target.year, month=target.month, 
                                  day=target.day, hour=19, minute=0)
            
            h1_data = df_1h[df_1h.index <= end_dt].tail(48)
            
            if len(h1_data) < 10:
                return order_blocks
            
            # Look for strong moves (>1% in one candle)
            for i in range(5, len(h1_data)):
                candle = h1_data.iloc[i]
                body_size = abs(candle['Close'] - candle['Open'])
                price_change_pct = (body_size / candle['Open']) * 100
                
                if price_change_pct > 1.0:  # Strong move
                    # The previous opposite candle is the order block
                    if direction == 'BULLISH' and candle['Close'] > candle['Open']:
                        # Find last bearish candle before this
                        for j in range(i-1, max(0, i-5), -1):
                            prev = h1_data.iloc[j]
                            if prev['Close'] < prev['Open']:
                                order_blocks.append({
                                    'type': 'BULLISH',
                                    'high': prev['High'],
                                    'low': prev['Low'],
                                    'time': h1_data.index[j]
                                })
                                break
                    
                    elif direction == 'BEARISH' and candle['Close'] < candle['Open']:
                        # Find last bullish candle before this
                        for j in range(i-1, max(0, i-5), -1):
                            prev = h1_data.iloc[j]
                            if prev['Close'] > prev['Open']:
                                order_blocks.append({
                                    'type': 'BEARISH',
                                    'high': prev['High'],
                                    'low': prev['Low'],
                                    'time': h1_data.index[j]
                                })
                                break
        
        except Exception as e:
            print(f"Error finding order blocks: {str(e)}")
        
        return order_blocks


if __name__ == "__main__":
    # Test the detector
    print("Market Structure Detector Module")
    print("="*50)
    print("Module loaded successfully")

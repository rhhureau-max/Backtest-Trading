"""
Strategy 1: Liquidity Raid (Reversal/Turtle Soup)
Detects Judas Swings and generates entry signals
"""

import pandas as pd
import numpy as np
from typing import Dict, Optional, List
from datetime import datetime, timedelta


class LiquidityRaidStrategy:
    """Strategy 1: Liquidity Raid / Judas Swing Detection"""
    
    def __init__(self, market_detector):
        self.detector = market_detector
        self.min_wick_ratio = 0.40  # 40% wick requirement
        
    def detect_judas_swing(self, london_data: pd.DataFrame, asian_range: Dict, 
                           bias: str) -> Optional[Dict]:
        """
        Detect Judas Swing (liquidity raid of Asian range)
        
        Args:
            london_data: 5m data during London Killzone
            asian_range: Asian range dictionary with 'high' and 'low'
            bias: Daily bias ('BULLISH' or 'BEARISH')
            
        Returns:
            Dictionary with Judas swing details or None
        """
        if len(london_data) == 0 or asian_range is None:
            return None
        
        asian_high = asian_range['high']
        asian_low = asian_range['low']
        
        # For bearish bias, look for violation of Asian HIGH
        if bias == 'BEARISH':
            for i in range(len(london_data)):
                candle = london_data.iloc[i]
                
                # Check if high violated Asian high
                if candle['High'] > asian_high:
                    # Validate rejection
                    if self._validate_rejection(candle, asian_high, 'ABOVE'):
                        return {
                            'type': 'BEARISH',
                            'swing_time': london_data.index[i],
                            'swing_high': candle['High'],
                            'swing_low': candle['Low'],
                            'close': candle['Close'],
                            'open': candle['Open'],
                            'asian_level': asian_high,
                            'validated': True,
                            'wick_pct': self._calculate_wick_ratio(candle, 'UPPER')
                        }
        
        # For bullish bias, look for violation of Asian LOW
        elif bias == 'BULLISH':
            for i in range(len(london_data)):
                candle = london_data.iloc[i]
                
                # Check if low violated Asian low
                if candle['Low'] < asian_low:
                    # Validate rejection
                    if self._validate_rejection(candle, asian_low, 'BELOW'):
                        return {
                            'type': 'BULLISH',
                            'swing_time': london_data.index[i],
                            'swing_high': candle['High'],
                            'swing_low': candle['Low'],
                            'close': candle['Close'],
                            'open': candle['Open'],
                            'asian_level': asian_low,
                            'validated': True,
                            'wick_pct': self._calculate_wick_ratio(candle, 'LOWER')
                        }
        
        return None
    
    def _validate_rejection(self, candle: pd.Series, asian_level: float, 
                           direction: str) -> bool:
        """
        Validate rejection: close inside range OR wick >40% of candle
        
        Args:
            candle: OHLC candle data
            asian_level: Asian high or low level
            direction: 'ABOVE' or 'BELOW'
            
        Returns:
            True if validated
        """
        close = candle['Close']
        high = candle['High']
        low = candle['Low']
        
        if direction == 'ABOVE':
            # Violation of Asian high (bearish swing)
            # Close should be back inside range (below Asian high)
            if close < asian_level:
                return True
            
            # Or upper wick should be >40% of total candle
            wick_ratio = self._calculate_wick_ratio(candle, 'UPPER')
            if wick_ratio > self.min_wick_ratio:
                return True
        
        elif direction == 'BELOW':
            # Violation of Asian low (bullish swing)
            # Close should be back inside range (above Asian low)
            if close > asian_level:
                return True
            
            # Or lower wick should be >40% of total candle
            wick_ratio = self._calculate_wick_ratio(candle, 'LOWER')
            if wick_ratio > self.min_wick_ratio:
                return True
        
        return False
    
    def _calculate_wick_ratio(self, candle: pd.Series, wick_type: str) -> float:
        """
        Calculate wick size as percentage of total candle range
        
        Args:
            candle: OHLC data
            wick_type: 'UPPER' or 'LOWER'
            
        Returns:
            Wick ratio (0.0 to 1.0)
        """
        high = candle['High']
        low = candle['Low']
        close = candle['Close']
        open_price = candle['Open']
        
        total_range = high - low
        
        if total_range == 0:
            return 0.0
        
        if wick_type == 'UPPER':
            # Upper wick from max(close, open) to high
            wick_size = high - max(close, open_price)
            return wick_size / total_range
        
        elif wick_type == 'LOWER':
            # Lower wick from low to min(close, open)
            wick_size = min(close, open_price) - low
            return wick_size / total_range
        
        return 0.0
    
    def generate_aggressive_entry(self, judas_swing: Dict) -> Dict:
        """
        Generate aggressive entry signal (at close of rejection candle)
        
        Args:
            judas_swing: Judas swing dictionary
            
        Returns:
            Entry signal dictionary
        """
        swing_type = judas_swing['type']
        entry_price = judas_swing['close']
        
        # Stop loss beyond the swing wick
        if swing_type == 'BEARISH':
            stop_loss = judas_swing['swing_high'] + 5  # 5 points buffer
            tp1 = judas_swing['asian_level'] - (judas_swing['swing_high'] - judas_swing['asian_level'])
            tp2 = tp1 - (judas_swing['swing_high'] - judas_swing['swing_low']) * 2.0  # Fib 2.0
        else:  # BULLISH
            stop_loss = judas_swing['swing_low'] - 5  # 5 points buffer
            tp1 = judas_swing['asian_level'] + (judas_swing['asian_level'] - judas_swing['swing_low'])
            tp2 = tp1 + (judas_swing['swing_high'] - judas_swing['swing_low']) * 2.0  # Fib 2.0
        
        return {
            'entry_type': 'AGGRESSIVE',
            'entry_price': entry_price,
            'entry_time': judas_swing['swing_time'],
            'stop_loss': stop_loss,
            'tp1': tp1,
            'tp2': tp2,
            'direction': swing_type,
            'risk': abs(entry_price - stop_loss),
            'reward_tp1': abs(tp1 - entry_price),
            'reward_tp2': abs(tp2 - entry_price)
        }
    
    def generate_conservative_entry(self, judas_swing: Dict, london_data: pd.DataFrame, 
                                    data_5m: pd.DataFrame) -> Optional[Dict]:
        """
        Generate conservative entry (wait for MSS + FVG on M5)
        
        Args:
            judas_swing: Judas swing dictionary
            london_data: London session data
            data_5m: Full 5m dataframe
            
        Returns:
            Entry signal dictionary or None
        """
        swing_time = judas_swing['swing_time']
        swing_type = judas_swing['type']
        
        # Get data after the swing
        post_swing = london_data[london_data.index > swing_time]
        
        if len(post_swing) < 5:
            return None
        
        # Look for MSS in post-swing data
        start_idx = data_5m.index.get_loc(swing_time) + 1
        end_idx = min(start_idx + 20, len(data_5m))  # Next 20 bars max
        
        mss = self.detector.detect_mss(data_5m, start_idx, end_idx, swing_type)
        
        if mss is None:
            return None
        
        # Look for FVG after MSS
        mss_idx = data_5m.index.get_loc(mss['break_time'])
        fvgs = self.detector.detect_fvg(data_5m, mss_idx, min(mss_idx + 10, len(data_5m)))
        
        # Find FVG matching our direction
        target_fvg = None
        for fvg in fvgs:
            if fvg['type'] == swing_type:
                target_fvg = fvg
                break
        
        if target_fvg is None:
            return None
        
        # Entry at FVG midpoint
        entry_price = (target_fvg['top'] + target_fvg['bottom']) / 2
        
        # Stop loss beyond the swing wick
        if swing_type == 'BEARISH':
            stop_loss = judas_swing['swing_high'] + 5
            tp1 = judas_swing['asian_level'] - (judas_swing['swing_high'] - judas_swing['asian_level'])
            tp2 = tp1 - (judas_swing['swing_high'] - judas_swing['swing_low']) * 2.0
        else:  # BULLISH
            stop_loss = judas_swing['swing_low'] - 5
            tp1 = judas_swing['asian_level'] + (judas_swing['asian_level'] - judas_swing['swing_low'])
            tp2 = tp1 + (judas_swing['swing_high'] - judas_swing['swing_low']) * 2.0
        
        return {
            'entry_type': 'CONSERVATIVE',
            'entry_price': entry_price,
            'entry_time': target_fvg['time'],
            'stop_loss': stop_loss,
            'tp1': tp1,
            'tp2': tp2,
            'direction': swing_type,
            'risk': abs(entry_price - stop_loss),
            'reward_tp1': abs(tp1 - entry_price),
            'reward_tp2': abs(tp2 - entry_price),
            'mss_level': mss['level'],
            'fvg_zone': f"{target_fvg['bottom']:.2f}-{target_fvg['top']:.2f}"
        }
    
    def analyze_day(self, date: str, data_5m: pd.DataFrame, data_1h: pd.DataFrame) -> List[Dict]:
        """
        Analyze a single trading day for Strategy 1 signals
        
        Args:
            date: Date string 'YYYY-MM-DD'
            data_5m: 5-minute dataframe
            data_1h: 1-hour dataframe
            
        Returns:
            List of entry signals
        """
        signals = []
        
        # Get Asian range
        asian_range = self.detector.get_asian_range(data_5m, date)
        if asian_range is None:
            return signals
        
        # Determine daily bias
        bias = self.detector.determine_daily_bias(data_1h, date)
        if bias == 'NEUTRAL':
            return signals
        
        # Get London Killzone data
        london_data = self.detector.get_london_killzone(data_5m, date)
        if len(london_data) == 0:
            return signals
        
        # Detect Judas Swing
        judas_swing = self.detect_judas_swing(london_data, asian_range, bias)
        if judas_swing is None:
            return signals
        
        # Generate aggressive entry
        aggressive_entry = self.generate_aggressive_entry(judas_swing)
        aggressive_entry['date'] = date
        aggressive_entry['strategy'] = 'STRATEGY_1_AGGRESSIVE'
        aggressive_entry['asian_high'] = asian_range['high']
        aggressive_entry['asian_low'] = asian_range['low']
        aggressive_entry['bias'] = bias
        signals.append(aggressive_entry)
        
        # Try to generate conservative entry
        conservative_entry = self.generate_conservative_entry(judas_swing, london_data, data_5m)
        if conservative_entry is not None:
            conservative_entry['date'] = date
            conservative_entry['strategy'] = 'STRATEGY_1_CONSERVATIVE'
            conservative_entry['asian_high'] = asian_range['high']
            conservative_entry['asian_low'] = asian_range['low']
            conservative_entry['bias'] = bias
            signals.append(conservative_entry)
        
        return signals


if __name__ == "__main__":
    print("Strategy 1: Liquidity Raid Module")
    print("="*50)
    print("Module loaded successfully")

"""
Strategy 2: Trend Continuation (Breakout & Momentum)
Detects strong breakouts and generates entry signals
"""

import pandas as pd
import numpy as np
from typing import Dict, Optional, List
from datetime import datetime, timedelta


class TrendContinuationStrategy:
    """Strategy 2: Trend Continuation / Breakout Detection"""
    
    def __init__(self, market_detector):
        self.detector = market_detector
        self.min_breakout_strength = 0.5  # Minimum 0.5% move for breakout candle
        
    def detect_strong_bias(self, df_1h: pd.DataFrame, target_date: str) -> Optional[str]:
        """
        Detect VERY strong daily bias (confirmed BOS on H1)
        More stringent than Strategy 1 bias detection
        
        Args:
            df_1h: 1H dataframe
            target_date: Date to analyze
            
        Returns:
            'BULLISH', 'BEARISH', or None
        """
        try:
            target = pd.to_datetime(target_date).date()
            
            # Get data up to target date
            end_dt = pd.Timestamp(year=target.year, month=target.month, 
                                  day=target.day, hour=19, minute=0)
            
            # Look at last 48 H1 bars (2 days)
            h1_data = df_1h[df_1h.index <= end_dt].tail(48)
            
            if len(h1_data) < 10:
                return None
            
            # Calculate recent price movement
            recent_close = h1_data['Close'].iloc[-1]
            price_10_bars_ago = h1_data['Close'].iloc[-10]
            price_change_pct = ((recent_close - price_10_bars_ago) / price_10_bars_ago) * 100
            
            # Look for strong directional move (>2% in last 10 bars)
            if price_change_pct > 2.0:
                # Confirm with structure
                recent_highs = h1_data['High'].tail(10).values
                if recent_highs[-1] > recent_highs[-5]:  # Recent high > previous high
                    return 'BULLISH'
            
            elif price_change_pct < -2.0:
                # Confirm with structure
                recent_lows = h1_data['Low'].tail(10).values
                if recent_lows[-1] < recent_lows[-5]:  # Recent low < previous low
                    return 'BEARISH'
            
            return None
            
        except Exception as e:
            print(f"Error detecting strong bias: {str(e)}")
            return None
    
    def detect_breakout(self, london_data: pd.DataFrame, asian_range: Dict, 
                       bias: str) -> Optional[Dict]:
        """
        Detect momentum breakout of Asian range with strong candle
        
        Args:
            london_data: London Killzone data (5m)
            asian_range: Asian range dictionary
            bias: Strong bias direction
            
        Returns:
            Breakout dictionary or None
        """
        if len(london_data) == 0 or asian_range is None:
            return None
        
        asian_high = asian_range['high']
        asian_low = asian_range['low']
        
        # For bullish bias, look for breakout ABOVE Asian high
        if bias == 'BULLISH':
            for i in range(len(london_data)):
                candle = london_data.iloc[i]
                
                # Check if close is above Asian high (strong breakout)
                if candle['Close'] > asian_high and candle['Open'] < asian_high:
                    # Validate momentum
                    body_size = abs(candle['Close'] - candle['Open'])
                    strength = (body_size / candle['Open']) * 100
                    
                    if strength >= self.min_breakout_strength:
                        return {
                            'type': 'BULLISH',
                            'breakout_time': london_data.index[i],
                            'breakout_high': candle['High'],
                            'breakout_low': candle['Low'],
                            'breakout_close': candle['Close'],
                            'breakout_open': candle['Open'],
                            'asian_level': asian_high,
                            'strength_pct': strength,
                            'body_size': body_size
                        }
        
        # For bearish bias, look for breakout BELOW Asian low
        elif bias == 'BEARISH':
            for i in range(len(london_data)):
                candle = london_data.iloc[i]
                
                # Check if close is below Asian low (strong breakout)
                if candle['Close'] < asian_low and candle['Open'] > asian_low:
                    # Validate momentum
                    body_size = abs(candle['Close'] - candle['Open'])
                    strength = (body_size / candle['Open']) * 100
                    
                    if strength >= self.min_breakout_strength:
                        return {
                            'type': 'BEARISH',
                            'breakout_time': london_data.index[i],
                            'breakout_high': candle['High'],
                            'breakout_low': candle['Low'],
                            'breakout_close': candle['Close'],
                            'breakout_open': candle['Open'],
                            'asian_level': asian_low,
                            'strength_pct': strength,
                            'body_size': body_size
                        }
        
        return None
    
    def find_breaker_block(self, breakout: Dict, london_data: pd.DataFrame) -> Optional[Dict]:
        """
        Find Breaker Block after breakout (last opposite candle before breakout)
        
        Args:
            breakout: Breakout dictionary
            london_data: London session data
            
        Returns:
            Breaker Block dictionary or None
        """
        breakout_time = breakout['breakout_time']
        breakout_type = breakout['type']
        
        # Get candles before breakout
        pre_breakout = london_data[london_data.index < breakout_time]
        
        if len(pre_breakout) < 2:
            return None
        
        # Look for last opposite candle
        if breakout_type == 'BULLISH':
            # Find last bearish candle
            for i in range(len(pre_breakout) - 1, -1, -1):
                candle = pre_breakout.iloc[i]
                if candle['Close'] < candle['Open']:  # Bearish
                    return {
                        'type': 'BULLISH_BB',
                        'high': candle['High'],
                        'low': candle['Low'],
                        'time': pre_breakout.index[i]
                    }
        
        elif breakout_type == 'BEARISH':
            # Find last bullish candle
            for i in range(len(pre_breakout) - 1, -1, -1):
                candle = pre_breakout.iloc[i]
                if candle['Close'] > candle['Open']:  # Bullish
                    return {
                        'type': 'BEARISH_BB',
                        'high': candle['High'],
                        'low': candle['Low'],
                        'time': pre_breakout.index[i]
                    }
        
        return None
    
    def wait_for_retest(self, breakout: Dict, breaker_block: Optional[Dict], 
                       london_data: pd.DataFrame, data_5m: pd.DataFrame) -> Optional[Dict]:
        """
        Wait for retest of Breaker Block or FVG continuation pattern
        NEVER enter on initial breakout
        
        Args:
            breakout: Breakout dictionary
            breaker_block: Breaker Block dictionary (may be None)
            london_data: London session data
            data_5m: Full 5m dataframe
            
        Returns:
            Entry signal or None
        """
        breakout_time = breakout['breakout_time']
        breakout_type = breakout['type']
        
        # Get data after breakout
        post_breakout = london_data[london_data.index > breakout_time]
        
        if len(post_breakout) < 3:
            return None
        
        # Strategy: Wait for pullback to Breaker Block OR FVG
        if breaker_block is not None:
            # Wait for retest of BB
            bb_high = breaker_block['high']
            bb_low = breaker_block['low']
            
            for i in range(len(post_breakout)):
                candle = post_breakout.iloc[i]
                
                if breakout_type == 'BULLISH':
                    # Price should pull back to BB zone and bounce
                    if candle['Low'] <= bb_high and candle['Close'] > bb_low:
                        # Entered BB zone and closed above it
                        entry_price = (bb_high + bb_low) / 2
                        stop_loss = bb_low - 10  # Below BB
                        
                        # TP: Next H1 liquidity zone (simplified: 2x range)
                        asian_level = breakout['asian_level']
                        breakout_range = breakout['breakout_high'] - asian_level
                        tp = breakout['breakout_high'] + breakout_range * 2
                        
                        return {
                            'entry_price': entry_price,
                            'entry_time': post_breakout.index[i],
                            'stop_loss': stop_loss,
                            'tp': tp,
                            'direction': breakout_type,
                            'entry_reason': 'BREAKER_BLOCK_RETEST',
                            'bb_zone': f"{bb_low:.2f}-{bb_high:.2f}"
                        }
                
                elif breakout_type == 'BEARISH':
                    # Price should pull back to BB zone and reject
                    if candle['High'] >= bb_low and candle['Close'] < bb_high:
                        # Entered BB zone and closed below it
                        entry_price = (bb_high + bb_low) / 2
                        stop_loss = bb_high + 10  # Above BB
                        
                        # TP: Next H1 liquidity zone (simplified: 2x range)
                        asian_level = breakout['asian_level']
                        breakout_range = asian_level - breakout['breakout_low']
                        tp = breakout['breakout_low'] - breakout_range * 2
                        
                        return {
                            'entry_price': entry_price,
                            'entry_time': post_breakout.index[i],
                            'stop_loss': stop_loss,
                            'tp': tp,
                            'direction': breakout_type,
                            'entry_reason': 'BREAKER_BLOCK_RETEST',
                            'bb_zone': f"{bb_low:.2f}-{bb_high:.2f}"
                        }
        
        # Alternative: Look for FVG continuation
        breakout_idx = data_5m.index.get_loc(breakout_time)
        fvgs = self.detector.detect_fvg(data_5m, breakout_idx, 
                                        min(breakout_idx + 20, len(data_5m)))
        
        for fvg in fvgs:
            if fvg['type'] == breakout_type:
                # Entry at FVG
                entry_price = (fvg['top'] + fvg['bottom']) / 2
                
                if breakout_type == 'BULLISH':
                    stop_loss = fvg['bottom'] - 10
                    asian_level = breakout['asian_level']
                    breakout_range = breakout['breakout_high'] - asian_level
                    tp = breakout['breakout_high'] + breakout_range * 2
                else:  # BEARISH
                    stop_loss = fvg['top'] + 10
                    asian_level = breakout['asian_level']
                    breakout_range = asian_level - breakout['breakout_low']
                    tp = breakout['breakout_low'] - breakout_range * 2
                
                return {
                    'entry_price': entry_price,
                    'entry_time': fvg['time'],
                    'stop_loss': stop_loss,
                    'tp': tp,
                    'direction': breakout_type,
                    'entry_reason': 'FVG_CONTINUATION',
                    'fvg_zone': f"{fvg['bottom']:.2f}-{fvg['top']:.2f}"
                }
        
        return None
    
    def analyze_day(self, date: str, data_5m: pd.DataFrame, data_1h: pd.DataFrame) -> List[Dict]:
        """
        Analyze a single trading day for Strategy 2 signals
        
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
        
        # Detect STRONG bias
        bias = self.detect_strong_bias(data_1h, date)
        if bias is None:
            return signals
        
        # Get London Killzone data
        london_data = self.detector.get_london_killzone(data_5m, date)
        if len(london_data) == 0:
            return signals
        
        # Detect breakout
        breakout = self.detect_breakout(london_data, asian_range, bias)
        if breakout is None:
            return signals
        
        # Find Breaker Block
        breaker_block = self.find_breaker_block(breakout, london_data)
        
        # Wait for retest entry
        entry = self.wait_for_retest(breakout, breaker_block, london_data, data_5m)
        if entry is None:
            return signals
        
        # Build signal
        entry['date'] = date
        entry['strategy'] = 'STRATEGY_2_CONTINUATION'
        entry['asian_high'] = asian_range['high']
        entry['asian_low'] = asian_range['low']
        entry['bias'] = bias
        entry['breakout_strength'] = breakout['strength_pct']
        entry['risk'] = abs(entry['entry_price'] - entry['stop_loss'])
        entry['reward'] = abs(entry['tp'] - entry['entry_price'])
        
        signals.append(entry)
        
        return signals


if __name__ == "__main__":
    print("Strategy 2: Trend Continuation Module")
    print("="*50)
    print("Module loaded successfully")

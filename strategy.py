"""
Module implementing the Fair Value Gap (FVG) trading strategy.
"""
import pandas as pd
import numpy as np


class FVGStrategy:
    """Fair Value Gap trading strategy for NQ futures."""
    
    def __init__(self, risk_reward_ratio=1.0, swing_lookback=5):
        """
        Initialize the FVG strategy.
        
        Args:
            risk_reward_ratio: Take profit to stop loss ratio (default 1:1)
            swing_lookback: Number of candles to look back for swing points
        """
        self.risk_reward_ratio = risk_reward_ratio
        self.swing_lookback = swing_lookback
        
    def detect_fvg(self, df):
        """
        Detect Fair Value Gaps in the data.
        
        A bearish FVG forms when there's a gap between:
        - Low of candle N-2 and high of candle N (candle N-1 doesn't cover the gap)
        
        A bullish FVG forms when there's a gap between:
        - High of candle N-2 and low of candle N (candle N-1 doesn't cover the gap)
        
        Args:
            df: DataFrame with OHLC data
            
        Returns:
            DataFrame with FVG columns added
        """
        df = df.copy()
        
        # Initialize FVG columns
        df['fvg_type'] = None  # 'bearish' or 'bullish'
        df['fvg_top'] = np.nan
        df['fvg_bottom'] = np.nan
        
        # Need at least 3 candles to detect FVG
        for i in range(2, len(df)):
            candle_n_minus_2 = df.iloc[i-2]
            candle_n_minus_1 = df.iloc[i-1]
            candle_n = df.iloc[i]
            
            # Check for bearish FVG
            # Gap between low of N-2 and high of N, where N-1 doesn't fill it
            # First condition: there's a gap (low of N-2 > high of N)
            # Second condition: middle candle (N-1) doesn't cover the gap
            if (candle_n_minus_2['low'] > candle_n['high'] and 
                candle_n_minus_1['low'] > candle_n['high']):
                df.at[i, 'fvg_type'] = 'bearish'
                df.at[i, 'fvg_top'] = candle_n_minus_2['low']
                df.at[i, 'fvg_bottom'] = candle_n['high']
            
            # Check for bullish FVG
            # Gap between high of N-2 and low of N, where N-1 doesn't fill it
            # First condition: there's a gap (high of N-2 < low of N)
            # Second condition: middle candle (N-1) doesn't cover the gap
            elif (candle_n_minus_2['high'] < candle_n['low'] and 
                  candle_n_minus_1['high'] < candle_n['low']):
                df.at[i, 'fvg_type'] = 'bullish'
                df.at[i, 'fvg_top'] = candle_n['low']
                df.at[i, 'fvg_bottom'] = candle_n_minus_2['high']
        
        return df
    
    def get_first_fvg_per_session(self, df):
        """
        Identify the first FVG in each trading session.
        
        Args:
            df: DataFrame with FVG data and session_id
            
        Returns:
            DataFrame with first_fvg_of_session column added
        """
        df = df.copy()
        df['first_fvg_of_session'] = False
        
        # Group by session and mark first FVG
        for session_id in df['session_id'].unique():
            session_mask = df['session_id'] == session_id
            session_df = df[session_mask]
            
            # Find first FVG in this session
            fvg_indices = session_df[session_df['fvg_type'].notna()].index
            if len(fvg_indices) > 0:
                first_fvg_idx = fvg_indices[0]
                df.at[first_fvg_idx, 'first_fvg_of_session'] = True
        
        return df
    
    def check_fvg_fill_and_reversal(self, df):
        """
        Check if a candle fills and reverses a FVG.
        
        For LONG (after bearish FVG):
        - Bullish candle (close > open) fills the FVG completely
        - Closes ABOVE the FVG top
        
        For SHORT (after bullish FVG):
        - Bearish candle (close < open) fills the FVG completely
        - Closes BELOW the FVG bottom
        
        Args:
            df: DataFrame with FVG data
            
        Returns:
            DataFrame with entry signal columns added
        """
        df = df.copy()
        
        # Initialize entry signal columns
        df['entry_signal'] = None  # 'long' or 'short'
        df['signal_fvg_top'] = np.nan
        df['signal_fvg_bottom'] = np.nan
        
        # Track active FVGs per session
        active_fvg = {}  # session_id: {'type', 'top', 'bottom', 'index'}
        
        for i in range(len(df)):
            row = df.iloc[i]
            session_id = row['session_id']
            
            # Check if this is the first FVG of the session
            if row['first_fvg_of_session']:
                active_fvg[session_id] = {
                    'type': row['fvg_type'],
                    'top': row['fvg_top'],
                    'bottom': row['fvg_bottom'],
                    'index': i
                }
                continue
            
            # Check if there's an active FVG for this session
            if session_id not in active_fvg:
                continue
            
            fvg = active_fvg[session_id]
            
            # Check for LONG signal (bearish FVG reversal)
            if fvg['type'] == 'bearish':
                # Bullish candle that closes above FVG top
                is_bullish = row['close'] > row['open']
                fills_gap = row['high'] >= fvg['top'] and row['low'] <= fvg['bottom']
                closes_above = row['close'] > fvg['top']
                
                if is_bullish and fills_gap and closes_above:
                    df.at[i, 'entry_signal'] = 'long'
                    df.at[i, 'signal_fvg_top'] = fvg['top']
                    df.at[i, 'signal_fvg_bottom'] = fvg['bottom']
                    # Remove FVG after signal
                    del active_fvg[session_id]
            
            # Check for SHORT signal (bullish FVG reversal)
            elif fvg['type'] == 'bullish':
                # Bearish candle that closes below FVG bottom
                is_bearish = row['close'] < row['open']
                fills_gap = row['low'] <= fvg['bottom'] and row['high'] >= fvg['top']
                closes_below = row['close'] < fvg['bottom']
                
                if is_bearish and fills_gap and closes_below:
                    df.at[i, 'entry_signal'] = 'short'
                    df.at[i, 'signal_fvg_top'] = fvg['top']
                    df.at[i, 'signal_fvg_bottom'] = fvg['bottom']
                    # Remove FVG after signal
                    del active_fvg[session_id]
        
        return df
    
    def calculate_swing_levels(self, df, index):
        """
        Calculate swing high and swing low from the last N candles before the given index.
        
        Args:
            df: DataFrame with OHLC data
            index: Current candle index
            
        Returns:
            Tuple of (swing_low, swing_high)
        """
        # Get the last N candles before entry
        start_idx = max(0, index - self.swing_lookback)
        lookback_candles = df.iloc[start_idx:index]
        
        if len(lookback_candles) == 0:
            return None, None
        
        swing_low = lookback_candles['low'].min()
        swing_high = lookback_candles['high'].max()
        
        return swing_low, swing_high
    
    def calculate_position_levels(self, entry_price, stop_loss, position_type):
        """
        Calculate take profit level based on risk/reward ratio.
        
        Args:
            entry_price: Entry price
            stop_loss: Stop loss price
            position_type: 'long' or 'short'
            
        Returns:
            Take profit price
        """
        risk = abs(entry_price - stop_loss)
        reward = risk * self.risk_reward_ratio
        
        if position_type == 'long':
            take_profit = entry_price + reward
        else:  # short
            take_profit = entry_price - reward
        
        return take_profit

"""
FVG (Fair Value Gap) Detection Module
Detects Fair Value Gaps at 8:30 AM candles
"""

import pandas as pd
import numpy as np
from datetime import time


class FVGDetector:
    """Detect Fair Value Gaps in trading data"""
    
    def __init__(self):
        self.fvg_signals = []
        
    def detect_fvg(self, df, target_time='08:30:00'):
        """
        Detect FVG patterns at specific time (default 8:30 AM)
        
        A bullish FVG occurs when: candle[i-1].high < candle[i+1].low
        A bearish FVG occurs when: candle[i-1].low > candle[i+1].high
        
        Parameters:
        -----------
        df : pd.DataFrame
            Trading data with OHLCV
        target_time : str
            Time to detect FVG (default '08:30:00')
            
        Returns:
        --------
        pd.DataFrame
            DataFrame with FVG signals
        """
        # Create a copy to avoid modifying original
        data = df.copy()
        
        # Initialize FVG columns
        data['FVG_Signal'] = 0  # 0: No FVG, 1: Bullish, -1: Bearish
        data['FVG_Upper'] = np.nan
        data['FVG_Lower'] = np.nan
        data['FVG_Middle'] = np.nan
        
        # Parse target time
        target_hour = int(target_time.split(':')[0])
        target_minute = int(target_time.split(':')[1])
        
        # Filter for 8:30 candles
        mask_830 = (data['Hour'] == target_hour) & (data['Minute'] == target_minute)
        candles_830_idx = data[mask_830].index
        
        print(f"Found {len(candles_830_idx)} candles at {target_time}")
        
        # For each 8:30 candle, check if it forms an FVG
        for idx in candles_830_idx:
            # Get position in dataframe
            pos = data.index.get_loc(idx)
            
            # Need at least one candle before and one after
            if pos < 1 or pos >= len(data) - 1:
                continue
            
            # Get the three candles: before (i-1), current (i), after (i+1)
            prev_idx = data.index[pos - 1]
            curr_idx = idx
            next_idx = data.index[pos + 1]
            
            prev_candle = data.loc[prev_idx]
            curr_candle = data.loc[curr_idx]
            next_candle = data.loc[next_idx]
            
            # Check for Bullish FVG: prev.high < next.low
            if prev_candle['High'] < next_candle['Low']:
                data.loc[curr_idx, 'FVG_Signal'] = 1  # Bullish
                data.loc[curr_idx, 'FVG_Lower'] = prev_candle['High']
                data.loc[curr_idx, 'FVG_Upper'] = next_candle['Low']
                data.loc[curr_idx, 'FVG_Middle'] = (prev_candle['High'] + next_candle['Low']) / 2
                
            # Check for Bearish FVG: prev.low > next.high
            elif prev_candle['Low'] > next_candle['High']:
                data.loc[curr_idx, 'FVG_Signal'] = -1  # Bearish
                data.loc[curr_idx, 'FVG_Upper'] = prev_candle['Low']
                data.loc[curr_idx, 'FVG_Lower'] = next_candle['High']
                data.loc[curr_idx, 'FVG_Middle'] = (prev_candle['Low'] + next_candle['High']) / 2
        
        # Count signals
        bullish_count = (data['FVG_Signal'] == 1).sum()
        bearish_count = (data['FVG_Signal'] == -1).sum()
        
        print(f"Detected FVGs: {bullish_count} Bullish, {bearish_count} Bearish")
        
        return data
    
    def get_fvg_signals(self, df):
        """
        Get all FVG signals from processed data
        
        Parameters:
        -----------
        df : pd.DataFrame
            Data with FVG signals
            
        Returns:
        --------
        pd.DataFrame
            Only rows with FVG signals
        """
        return df[df['FVG_Signal'] != 0].copy()
    
    def get_entry_candle_time(self, timeframe, fvg_time):
        """
        Calculate entry candle time based on timeframe
        
        Parameters:
        -----------
        timeframe : str
            Timeframe ('1m', '5m', '15m')
        fvg_time : datetime
            Time of FVG detection (8:30)
            
        Returns:
        --------
        datetime
            Entry time
        """
        if timeframe == '1m':
            # Enter at 8:31 (1 minute after)
            return pd.Timestamp(fvg_time.date()) + pd.Timedelta(hours=8, minutes=31)
        elif timeframe == '5m':
            # Enter at 8:35 (5 minutes after)
            return pd.Timestamp(fvg_time.date()) + pd.Timedelta(hours=8, minutes=35)
        elif timeframe == '15m':
            # Enter at 8:45 (15 minutes after)
            return pd.Timestamp(fvg_time.date()) + pd.Timedelta(hours=8, minutes=45)
        else:
            raise ValueError(f"Unsupported timeframe: {timeframe}")

"""
EMA-Based Trend Filter Module
Simplified trend detection using EMA 200 on 1H timeframe
"""

import pandas as pd
import numpy as np
from typing import Optional


class EMATrendFilter:
    """Uses EMA 200 on H1 to determine market bias"""
    
    def __init__(self, data_h1: pd.DataFrame, ema_period: int = 200):
        """
        Args:
            data_h1: 1-hour OHLC data with DateTime as index
            ema_period: Period for EMA calculation (default: 200)
        """
        self.data_h1 = data_h1.copy()
        self.ema_period = ema_period
        
        # Calculate EMA 200
        print(f"Calculating EMA {ema_period} on H1 data...")
        self.data_h1['ema_200'] = self.data_h1['Close'].ewm(span=ema_period, adjust=False).mean()
        
        # Determine trend
        self.data_h1['trend'] = np.where(
            self.data_h1['Close'] > self.data_h1['ema_200'],
            'bullish',
            'bearish'
        )
        
        bullish_count = (self.data_h1['trend'] == 'bullish').sum()
        bearish_count = (self.data_h1['trend'] == 'bearish').sum()
        print(f"  ✓ Bullish periods: {bullish_count}")
        print(f"  ✓ Bearish periods: {bearish_count}")
    
    def get_trend_at_time(self, timestamp: pd.Timestamp) -> Optional[str]:
        """
        Get trend (bullish/bearish) at a specific timestamp
        
        Args:
            timestamp: Timestamp to check
            
        Returns:
            'bullish', 'bearish', or None if no data
        """
        # Find nearest H1 bar at or before timestamp
        idx = self.data_h1.index.searchsorted(timestamp, side='right') - 1
        
        if idx < 0 or idx >= len(self.data_h1):
            return None
        
        # Make sure we have EMA calculated (need at least ema_period bars)
        if idx < self.ema_period:
            return None
        
        trend = self.data_h1.iloc[idx]['trend']
        return trend if pd.notna(trend) else None


if __name__ == "__main__":
    # Test the EMA trend filter
    from data_loader import get_market_data
    
    print("Testing EMA Trend Filter...")
    data = get_market_data()
    
    filter = EMATrendFilter(data['1H'])
    
    # Test a few timestamps
    test_times = [
        pd.Timestamp('2021-08-16 09:30:00', tz='US/Central'),
        pd.Timestamp('2022-05-24 09:30:00', tz='US/Central'),
        pd.Timestamp('2024-01-17 09:30:00', tz='US/Central'),
    ]
    
    for ts in test_times:
        trend = filter.get_trend_at_time(ts)
        print(f"{ts.date()}: {trend}")

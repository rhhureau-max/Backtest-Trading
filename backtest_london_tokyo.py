#!/usr/bin/env python3
"""
LONDON-TOKYO KILLZONE BACKTEST SYSTEM
Professional backtesting implementation for 3 institutional scenarios on NQ data (2018-2025)

Author: Institutional Trading System
Version: 1.0
"""

import pandas as pd
import numpy as np
from datetime import datetime, time, timedelta
import glob
import os
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

# Configure matplotlib for better-looking charts
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")


class LondonTokyoBacktest:
    """
    Professional backtesting system for London-Tokyo killzone strategies
    """
    
    def __init__(self, slippage_points: float = 1.5):
        """
        Initialize the backtest system
        
        Args:
            slippage_points: Slippage in points per trade (conservative: 1.5)
        """
        self.slippage = slippage_points
        self.data = None
        self.trades = []
        self.daily_data = None
        
        # Session times in NY time
        self.TOKYO_START = time(20, 0)  # 20:00 NY (Tokyo open)
        self.TOKYO_END = time(0, 0)     # 00:00 NY (Tokyo close)
        self.LONDON_START = time(2, 0)  # 02:00 NY (London open)
        self.LONDON_END = time(5, 0)    # 05:00 NY (London close)
        
        # Scenario parameters
        self.COMPRESSION_THRESHOLD = 40  # points
        self.EXPANSION_THRESHOLD = 60    # points
        
        print("🚀 London-Tokyo Killzone Backtest System Initialized")
        print(f"   Slippage: {slippage_points} points per trade")
        print("="*70)
    
    def load_data(self, years: List[int] = None) -> pd.DataFrame:
        """
        Load and consolidate 15m NQ data from multiple years
        
        Args:
            years: List of years to load (default: 2018-2025)
        
        Returns:
            Consolidated dataframe with all data
        """
        if years is None:
            years = [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]
        
        print("\n📂 Loading NQ 15m data...")
        all_data = []
        
        for year in years:
            file_path = f"{year} 15m.csv"
            if os.path.exists(file_path):
                try:
                    df = pd.read_csv(file_path, sep=';', skiprows=1, 
                                   names=['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume'])
                    
                    # Parse datetime
                    df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], 
                                                    format='%d/%m/%Y %H:%M:%S', 
                                                    errors='coerce')
                    
                    # Drop rows with invalid dates
                    df = df.dropna(subset=['Datetime'])
                    
                    # Convert price columns to float
                    for col in ['Open', 'High', 'Low', 'Close']:
                        df[col] = pd.to_numeric(df[col], errors='coerce')
                    
                    df = df.dropna(subset=['Open', 'High', 'Low', 'Close'])
                    
                    all_data.append(df)
                    print(f"   ✓ Loaded {year}: {len(df):,} bars")
                except Exception as e:
                    print(f"   ✗ Error loading {year}: {e}")
        
        if not all_data:
            raise ValueError("No data loaded!")
        
        # Concatenate all data
        self.data = pd.concat(all_data, ignore_index=True)
        self.data = self.data.sort_values('Datetime').reset_index(drop=True)
        
        # Add time components
        self.data['Date'] = self.data['Datetime'].dt.date
        self.data['Time'] = self.data['Datetime'].dt.time
        self.data['Hour'] = self.data['Datetime'].dt.hour
        self.data['Minute'] = self.data['Datetime'].dt.minute
        self.data['DayOfWeek'] = self.data['Datetime'].dt.dayofweek  # 0=Monday
        
        # Filter out weekends
        self.data = self.data[self.data['DayOfWeek'] < 5].reset_index(drop=True)
        
        print(f"\n✅ Total data loaded: {len(self.data):,} bars")
        print(f"   Date range: {self.data['Datetime'].min()} to {self.data['Datetime'].max()}")
        print(f"   Unique trading days: {self.data['Date'].nunique():,}")
        
        return self.data
    
    def calculate_daily_bias(self) -> pd.DataFrame:
        """
        Calculate daily trend bias (Higher Highs/Higher Lows vs Lower Highs/Lower Lows)
        Uses previous day's structure to determine bias
        
        Returns:
            DataFrame with daily bias
        """
        print("\n📊 Calculating Daily Bias...")
        
        # Get daily data
        daily = self.data.groupby('Date').agg({
            'Open': 'first',
            'High': 'max',
            'Low': 'min',
            'Close': 'last',
            'Volume': 'sum'
        }).reset_index()
        
        # Calculate structure
        daily['Prev_High'] = daily['High'].shift(1)
        daily['Prev_Low'] = daily['Low'].shift(1)
        daily['Prev_Close'] = daily['Close'].shift(1)
        
        # Determine bias
        daily['Bias'] = 'NEUTRAL'
        
        # Bullish: Higher High AND Higher Low
        bullish_condition = (daily['High'] > daily['Prev_High']) & (daily['Low'] > daily['Prev_Low'])
        daily.loc[bullish_condition, 'Bias'] = 'BULLISH'
        
        # Bearish: Lower High AND Lower Low
        bearish_condition = (daily['High'] < daily['Prev_High']) & (daily['Low'] < daily['Prev_Low'])
        daily.loc[bearish_condition, 'Bias'] = 'BEARISH'
        
        # Use 3-day moving bias for more stability
        daily['Bullish_Count'] = (daily['Bias'] == 'BULLISH').rolling(3, min_periods=1).sum()
        daily['Bearish_Count'] = (daily['Bias'] == 'BEARISH').rolling(3, min_periods=1).sum()
        
        daily['Daily_Bias'] = 'NEUTRAL'
        daily.loc[daily['Bullish_Count'] >= 2, 'Daily_Bias'] = 'BULLISH'
        daily.loc[daily['Bearish_Count'] >= 2, 'Daily_Bias'] = 'BEARISH'
        
        self.daily_data = daily
        
        bias_counts = daily['Daily_Bias'].value_counts()
        print(f"   Bullish days: {bias_counts.get('BULLISH', 0)}")
        print(f"   Bearish days: {bias_counts.get('BEARISH', 0)}")
        print(f"   Neutral days: {bias_counts.get('NEUTRAL', 0)}")
        
        return daily
    
    def calculate_asian_range(self, date) -> Dict:
        """
        Calculate the Tokyo session range for a given date
        
        Args:
            date: Trading date
        
        Returns:
            Dictionary with range statistics
        """
        # Get data for the specific date
        # Tokyo session: 20:00 previous day to 00:00 current day
        prev_date = date - timedelta(days=1)
        
        # Get Tokyo session data (previous day 20:00 to current day 00:00)
        tokyo_data = self.data[
            ((self.data['Date'] == prev_date) & (self.data['Hour'] >= 20)) |
            ((self.data['Date'] == date) & (self.data['Hour'] < 0))  # This catches midnight bars
        ]
        
        # Also get data from current date between 00:00-00:00 (midnight bars)
        tokyo_data_current = self.data[
            (self.data['Date'] == date) & 
            (self.data['Hour'] == 0) & 
            (self.data['Minute'] == 0)
        ]
        
        tokyo_data = pd.concat([tokyo_data, tokyo_data_current]).drop_duplicates()
        
        if len(tokyo_data) == 0:
            return None
        
        asian_high = tokyo_data['High'].max()
        asian_low = tokyo_data['Low'].min()
        asian_range = asian_high - asian_low
        asian_open = tokyo_data.iloc[0]['Open']
        asian_close = tokyo_data.iloc[-1]['Close']
        
        # Determine if trending
        is_trending = abs(asian_close - asian_open) > (asian_range * 0.6)
        trend_direction = 'BULLISH' if asian_close > asian_open else 'BEARISH'
        
        return {
            'date': date,
            'asian_high': asian_high,
            'asian_low': asian_low,
            'asian_range': asian_range,
            'asian_open': asian_open,
            'asian_close': asian_close,
            'is_trending': is_trending,
            'trend_direction': trend_direction if is_trending else 'NEUTRAL',
            'num_bars': len(tokyo_data)
        }
    
    def detect_scenario(self, asian_info: Dict, daily_bias: str) -> List[str]:
        """
        Detect which scenarios apply based on Asian range
        Can return multiple scenarios to test
        
        Args:
            asian_info: Asian session information
            daily_bias: Daily trend bias
        
        Returns:
            List of applicable scenario names
        """
        if asian_info is None:
            return []
        
        asian_range = asian_info['asian_range']
        scenarios = []
        
        # SCENARIO 1: COMPRESSION (Range < 40 points)
        if asian_range < self.COMPRESSION_THRESHOLD:
            scenarios.append('COMPRESSION')
        
        # SCENARIO 2: EXPANSION (Range > 60 points with trend)
        if asian_range > self.EXPANSION_THRESHOLD and asian_info['is_trending']:
            scenarios.append('EXPANSION')
        
        # SCENARIO 3: CONTINUATION (medium range with potential structure break)
        # Test for continuation if range is reasonable and trending
        if asian_range >= 30 and asian_info['is_trending']:
            scenarios.append('POTENTIAL_CONTINUATION')
        
        return scenarios
    
    def execute_compression_scenario(self, date, asian_info: Dict, daily_bias: str) -> Optional[Dict]:
        """
        SCENARIO 1: COMPRESSION - London Reversal / Liquidity Sweep
        
        Strategy:
        - Wait for sweep of Asian high/low in first 30min of London
        - Enter on M15 close back into range
        - Stop: 3-5 points beyond sweep
        - Target: Opposite side + 1.5x extension
        - R:R: 1:3 minimum
        """
        # Get London session data (02:00 - 05:00 NY)
        london_data = self.data[
            (self.data['Date'] == date) & 
            (self.data['Hour'] >= 2) & 
            (self.data['Hour'] < 5)
        ].copy()
        
        if len(london_data) < 4:  # Need at least 4 bars (1 hour)
            return None
        
        asian_high = asian_info['asian_high']
        asian_low = asian_info['asian_low']
        asian_mid = (asian_high + asian_low) / 2
        
        # Look for liquidity sweep in first 30 minutes (02:00-02:30)
        early_london = london_data[london_data['Hour'] == 2].head(2)  # First 30 min
        
        if len(early_london) == 0:
            return None
        
        swept_high = early_london['High'].max() > asian_high
        swept_low = early_london['Low'].min() < asian_low
        
        # Look for reversal back into range
        for idx in range(2, len(london_data)):
            bar = london_data.iloc[idx]
            prev_bar = london_data.iloc[idx - 1]
            
            entry_price = None
            direction = None
            stop_loss = None
            take_profit = None
            
            # BULLISH SETUP: Swept low, now reversing up
            if swept_low and daily_bias in ['BULLISH', 'NEUTRAL']:
                # Check if price closed back into range
                if prev_bar['Close'] < asian_low and bar['Close'] > asian_low:
                    direction = 'LONG'
                    entry_price = bar['Close'] + self.slippage
                    
                    # Find the sweep low
                    sweep_low = early_london['Low'].min()
                    stop_loss = sweep_low - 4  # 4 points beyond sweep
                    
                    # Target: Asian high + 1.5x range extension
                    range_size = asian_info['asian_range']
                    take_profit = asian_high + (range_size * 1.5)
            
            # BEARISH SETUP: Swept high, now reversing down
            elif swept_high and daily_bias in ['BEARISH', 'NEUTRAL']:
                # Check if price closed back into range
                if prev_bar['Close'] > asian_high and bar['Close'] < asian_high:
                    direction = 'SHORT'
                    entry_price = bar['Close'] - self.slippage
                    
                    # Find the sweep high
                    sweep_high = early_london['High'].max()
                    stop_loss = sweep_high + 4  # 4 points beyond sweep
                    
                    # Target: Asian low - 1.5x range extension
                    range_size = asian_info['asian_range']
                    take_profit = asian_low - (range_size * 1.5)
            
            if entry_price is not None:
                # Calculate R:R
                risk = abs(entry_price - stop_loss)
                reward = abs(take_profit - entry_price)
                
                if risk > 0:
                    rr_ratio = reward / risk
                    
                    # Only take trade if R:R >= 2.5
                    if rr_ratio >= 2.5:
                        return {
                            'scenario': 'COMPRESSION',
                            'date': date,
                            'entry_time': bar['Datetime'],
                            'entry_price': entry_price,
                            'direction': direction,
                            'stop_loss': stop_loss,
                            'take_profit': take_profit,
                            'risk_points': risk,
                            'reward_points': reward,
                            'rr_ratio': rr_ratio,
                            'daily_bias': daily_bias,
                            'asian_range': asian_info['asian_range']
                        }
        
        return None
    
    def execute_expansion_scenario(self, date, asian_info: Dict, daily_bias: str) -> Optional[Dict]:
        """
        SCENARIO 2: EXPANSION - Asian Fade (Counter-trend)
        
        Strategy:
        - Asian range > 60 points with directional trend
        - Fade the move at London open if rejection occurs
        - Entry: Break of structure in opposite direction
        - Stop: Beyond Asian extreme
        - Target: Return to 50% of Asian range
        - R:R: 1:2.5 minimum
        """
        # Get London session data
        london_data = self.data[
            (self.data['Date'] == date) & 
            (self.data['Hour'] >= 2) & 
            (self.data['Hour'] < 5)
        ].copy()
        
        if len(london_data) < 3:
            return None
        
        asian_high = asian_info['asian_high']
        asian_low = asian_info['asian_low']
        asian_mid = (asian_high + asian_low) / 2
        asian_range = asian_info['asian_range']
        trend_direction = asian_info['trend_direction']
        
        # Look for rejection in first hour of London (02:00-03:00)
        early_london = london_data[(london_data['Hour'] >= 2) & (london_data['Hour'] < 3)].copy()
        
        if len(early_london) < 2:
            return None
        
        # Check for failure to continue Asian momentum
        london_high = early_london['High'].max()
        london_low = early_london['Low'].min()
        
        # More lenient conditions for fade
        if trend_direction == 'BULLISH':
            # Look for failure to make significant new highs
            extension = london_high - asian_high
            failed_to_extend_up = extension < (asian_range * 0.15)  # Less than 15% extension
        else:
            failed_to_extend_up = False
        
        if trend_direction == 'BEARISH':
            # Look for failure to make significant new lows
            extension = asian_low - london_low
            failed_to_extend_down = extension < (asian_range * 0.15)
        else:
            failed_to_extend_down = False
        
        # Look for fade entry in rest of London session
        for idx in range(len(early_london), min(len(london_data), len(early_london) + 8)):
            if idx >= len(london_data):
                break
            
            bar = london_data.iloc[idx]
            prev_bar = london_data.iloc[idx - 1] if idx > 0 else early_london.iloc[-1]
            
            entry_price = None
            direction = None
            stop_loss = None
            take_profit = None
            
            # FADE BULLISH ASIAN MOVE (Go Short)
            if trend_direction == 'BULLISH' and (failed_to_extend_up or london_high < asian_high):
                # Check for bearish momentum - price moving back down
                if bar['Close'] < prev_bar['Close'] and bar['Close'] < asian_high:
                    direction = 'SHORT'
                    entry_price = bar['Close'] - self.slippage
                    stop_loss = london_high + 8  # Beyond London high with buffer
                    take_profit = asian_mid  # Target middle of Asian range
            
            # FADE BEARISH ASIAN MOVE (Go Long)
            elif trend_direction == 'BEARISH' and (failed_to_extend_down or london_low > asian_low):
                # Check for bullish momentum - price moving back up
                if bar['Close'] > prev_bar['Close'] and bar['Close'] > asian_low:
                    direction = 'LONG'
                    entry_price = bar['Close'] + self.slippage
                    stop_loss = london_low - 8  # Beyond London low with buffer
                    take_profit = asian_mid  # Target middle of Asian range
            
            if entry_price is not None:
                risk = abs(entry_price - stop_loss)
                reward = abs(take_profit - entry_price)
                
                if risk > 0:
                    rr_ratio = reward / risk
                    
                    # Only take trade if R:R >= 2.0
                    if rr_ratio >= 2.0:
                        return {
                            'scenario': 'EXPANSION',
                            'date': date,
                            'entry_time': bar['Datetime'],
                            'entry_price': entry_price,
                            'direction': direction,
                            'stop_loss': stop_loss,
                            'take_profit': take_profit,
                            'risk_points': risk,
                            'reward_points': reward,
                            'rr_ratio': rr_ratio,
                            'daily_bias': daily_bias,
                            'asian_range': asian_info['asian_range']
                        }
        
        return None
    
    def execute_continuation_scenario(self, date, asian_info: Dict, daily_bias: str) -> Optional[Dict]:
        """
        SCENARIO 3: CONTINUATION - London Breakout Continuation
        
        Strategy:
        - Asian session breaks key structure with volume
        - Must align with daily bias
        - Entry: Retest of broken level at London
        - Stop: Behind broken level
        - Target: 2x extension of initial move
        - R:R: 1:3 minimum
        """
        # Get London session data
        london_data = self.data[
            (self.data['Date'] == date) & 
            (self.data['Hour'] >= 2) & 
            (self.data['Hour'] < 6)
        ].copy()
        
        if len(london_data) < 3:
            return None
        
        # Get previous 3 days for better structure context
        lookback_days = 3
        prev_dates = [date - timedelta(days=i) for i in range(1, lookback_days + 1)]
        prev_days_data = self.data[self.data['Date'].isin(prev_dates)]
        
        if len(prev_days_data) == 0:
            return None
        
        # Get swing high/low from previous days
        swing_high = prev_days_data['High'].max()
        swing_low = prev_days_data['Low'].min()
        
        # Also get most recent day high/low
        recent_date = date - timedelta(days=1)
        recent_data = self.data[self.data['Date'] == recent_date]
        
        if len(recent_data) > 0:
            recent_high = recent_data['High'].max()
            recent_low = recent_data['Low'].min()
        else:
            recent_high = swing_high
            recent_low = swing_low
        
        asian_high = asian_info['asian_high']
        asian_low = asian_info['asian_low']
        asian_range = asian_info['asian_range']
        asian_close = asian_info['asian_close']
        
        # Check if Asian session broke structure (must be aligned with daily bias)
        # Bullish break: Asian high above recent swing high
        broke_structure_up = (asian_high > swing_high * 1.001) and daily_bias == 'BULLISH'
        
        # Bearish break: Asian low below recent swing low  
        broke_structure_down = (asian_low < swing_low * 0.999) and daily_bias == 'BEARISH'
        
        if not (broke_structure_up or broke_structure_down):
            return None
        
        # Look for continuation at London - price should hold above/below break level
        for idx in range(1, min(len(london_data), 12)):  # First 3 hours of London
            bar = london_data.iloc[idx]
            prev_bar = london_data.iloc[idx - 1]
            
            entry_price = None
            direction = None
            stop_loss = None
            take_profit = None
            
            # BULLISH CONTINUATION
            if broke_structure_up:
                # Look for pullback to broken level or bullish continuation
                # Entry on retest (price dips near swing high but holds above)
                if bar['Low'] <= swing_high * 1.003 and bar['Close'] > swing_high:
                    direction = 'LONG'
                    entry_price = bar['Close'] + self.slippage
                    stop_loss = swing_high - 12  # Stop below broken level
                    
                    # Target: Extension based on Asian breakout size
                    breakout_size = asian_high - swing_high
                    take_profit = entry_price + max(breakout_size * 2, asian_range * 1.5)
                
                # Alternative: Direct continuation without retest
                elif idx <= 3 and bar['Close'] > bar['Open'] and bar['Close'] > asian_high:
                    direction = 'LONG'
                    entry_price = bar['Close'] + self.slippage
                    stop_loss = asian_high - 10
                    
                    breakout_size = asian_high - swing_high
                    take_profit = entry_price + max(breakout_size * 2, asian_range * 1.5)
            
            # BEARISH CONTINUATION
            elif broke_structure_down:
                # Look for pullback to broken level or bearish continuation
                if bar['High'] >= swing_low * 0.997 and bar['Close'] < swing_low:
                    direction = 'SHORT'
                    entry_price = bar['Close'] - self.slippage
                    stop_loss = swing_low + 12  # Stop above broken level
                    
                    # Target: Extension based on Asian breakout size
                    breakout_size = swing_low - asian_low
                    take_profit = entry_price - max(breakout_size * 2, asian_range * 1.5)
                
                # Alternative: Direct continuation without retest
                elif idx <= 3 and bar['Close'] < bar['Open'] and bar['Close'] < asian_low:
                    direction = 'SHORT'
                    entry_price = bar['Close'] - self.slippage
                    stop_loss = asian_low + 10
                    
                    breakout_size = swing_low - asian_low
                    take_profit = entry_price - max(breakout_size * 2, asian_range * 1.5)
            
            if entry_price is not None:
                risk = abs(entry_price - stop_loss)
                reward = abs(take_profit - entry_price)
                
                if risk > 0:
                    rr_ratio = reward / risk
                    
                    # Only take trade if R:R >= 2.5
                    if rr_ratio >= 2.5:
                        return {
                            'scenario': 'CONTINUATION',
                            'date': date,
                            'entry_time': bar['Datetime'],
                            'entry_price': entry_price,
                            'direction': direction,
                            'stop_loss': stop_loss,
                            'take_profit': take_profit,
                            'risk_points': risk,
                            'reward_points': reward,
                            'rr_ratio': rr_ratio,
                            'daily_bias': daily_bias,
                            'asian_range': asian_info['asian_range']
                        }
        
        return None
    
    def simulate_trade_outcome(self, trade: Dict, date) -> Dict:
        """
        Simulate the trade outcome by checking if SL or TP was hit
        
        Args:
            trade: Trade dictionary
            date: Trading date
        
        Returns:
            Updated trade dictionary with outcome
        """
        # Get rest of day data after entry
        entry_time = trade['entry_time']
        
        rest_of_day = self.data[
            (self.data['Datetime'] > entry_time) &
            (self.data['Date'] == date)
        ].copy()
        
        if len(rest_of_day) == 0:
            # Trade didn't complete same day - mark as scratch
            trade['outcome'] = 'SCRATCH'
            trade['exit_price'] = trade['entry_price']
            trade['pnl_points'] = 0
            trade['r_multiple'] = 0
            return trade
        
        direction = trade['direction']
        stop_loss = trade['stop_loss']
        take_profit = trade['take_profit']
        entry_price = trade['entry_price']
        
        for idx, bar in rest_of_day.iterrows():
            if direction == 'LONG':
                # Check if stop hit first
                if bar['Low'] <= stop_loss:
                    trade['outcome'] = 'LOSS'
                    trade['exit_price'] = stop_loss
                    trade['exit_time'] = bar['Datetime']
                    trade['pnl_points'] = stop_loss - entry_price
                    trade['r_multiple'] = -1.0
                    return trade
                
                # Check if target hit
                if bar['High'] >= take_profit:
                    trade['outcome'] = 'WIN'
                    trade['exit_price'] = take_profit
                    trade['exit_time'] = bar['Datetime']
                    trade['pnl_points'] = take_profit - entry_price
                    trade['r_multiple'] = trade['rr_ratio']
                    return trade
            
            else:  # SHORT
                # Check if stop hit first
                if bar['High'] >= stop_loss:
                    trade['outcome'] = 'LOSS'
                    trade['exit_price'] = stop_loss
                    trade['exit_time'] = bar['Datetime']
                    trade['pnl_points'] = entry_price - stop_loss
                    trade['r_multiple'] = -1.0
                    return trade
                
                # Check if target hit
                if bar['Low'] <= take_profit:
                    trade['outcome'] = 'WIN'
                    trade['exit_price'] = take_profit
                    trade['exit_time'] = bar['Datetime']
                    trade['pnl_points'] = entry_price - take_profit
                    trade['r_multiple'] = trade['rr_ratio']
                    return trade
        
        # Trade didn't hit SL or TP by end of day - close at market
        last_bar = rest_of_day.iloc[-1]
        trade['outcome'] = 'SCRATCH'
        trade['exit_price'] = last_bar['Close']
        trade['exit_time'] = last_bar['Datetime']
        
        if direction == 'LONG':
            trade['pnl_points'] = last_bar['Close'] - entry_price
        else:
            trade['pnl_points'] = entry_price - last_bar['Close']
        
        trade['r_multiple'] = trade['pnl_points'] / trade['risk_points']
        
        return trade
    
    def run_backtest(self) -> pd.DataFrame:
        """
        Run the complete backtest across all scenarios
        
        Returns:
            DataFrame of all trades
        """
        print("\n" + "="*70)
        print("🎯 STARTING BACKTEST EXECUTION")
        print("="*70)
        
        if self.data is None:
            raise ValueError("Data not loaded! Call load_data() first.")
        
        if self.daily_data is None:
            self.calculate_daily_bias()
        
        # Get unique trading dates
        unique_dates = sorted(self.data['Date'].unique())
        
        self.trades = []
        scenario_counts = {'COMPRESSION': 0, 'EXPANSION': 0, 'CONTINUATION': 0}
        
        print(f"\n📅 Processing {len(unique_dates)} trading days...")
        
        for i, date in enumerate(unique_dates):
            # Skip first few days (need historical data for bias)
            if i < 5:
                continue
            
            # Get daily bias
            daily_info = self.daily_data[self.daily_data['Date'] == date]
            if len(daily_info) == 0:
                continue
            
            daily_bias = daily_info.iloc[0]['Daily_Bias']
            
            # Calculate Asian range
            asian_info = self.calculate_asian_range(date)
            if asian_info is None or asian_info['num_bars'] < 4:
                continue
            
            # Detect scenarios (can be multiple)
            scenarios = self.detect_scenario(asian_info, daily_bias)
            
            if not scenarios:
                continue
            
            # Try each applicable scenario (take first valid trade)
            trade = None
            
            for scenario in scenarios:
                if trade is not None:
                    break  # Already found a trade
                
                if scenario == 'COMPRESSION':
                    trade = self.execute_compression_scenario(date, asian_info, daily_bias)
                    if trade:
                        scenario_counts['COMPRESSION'] += 1
                
                elif scenario == 'EXPANSION':
                    trade = self.execute_expansion_scenario(date, asian_info, daily_bias)
                    if trade:
                        scenario_counts['EXPANSION'] += 1
                
                elif scenario == 'POTENTIAL_CONTINUATION':
                    trade = self.execute_continuation_scenario(date, asian_info, daily_bias)
                    if trade:
                        scenario_counts['CONTINUATION'] += 1
            
            # Simulate trade outcome
            if trade:
                trade = self.simulate_trade_outcome(trade, date)
                self.trades.append(trade)
            
            # Progress indicator
            if (i + 1) % 250 == 0:
                print(f"   Processed {i + 1}/{len(unique_dates)} days...")
        
        print(f"\n✅ Backtest Complete!")
        print(f"\n📊 Scenario Distribution:")
        print(f"   COMPRESSION:   {scenario_counts['COMPRESSION']} trades")
        print(f"   EXPANSION:     {scenario_counts['EXPANSION']} trades")
        print(f"   CONTINUATION:  {scenario_counts['CONTINUATION']} trades")
        print(f"   TOTAL:         {len(self.trades)} trades")
        
        return pd.DataFrame(self.trades)
    
    def calculate_metrics(self, trades_df: pd.DataFrame) -> Dict:
        """
        Calculate comprehensive performance metrics
        
        Args:
            trades_df: DataFrame of trades
        
        Returns:
            Dictionary of metrics
        """
        if len(trades_df) == 0:
            return {}
        
        # Filter out scratches for win rate calculation
        completed_trades = trades_df[trades_df['outcome'].isin(['WIN', 'LOSS'])]
        
        if len(completed_trades) == 0:
            return {}
        
        # Basic metrics
        total_trades = len(completed_trades)
        winning_trades = len(completed_trades[completed_trades['outcome'] == 'WIN'])
        losing_trades = len(completed_trades[completed_trades['outcome'] == 'LOSS'])
        
        win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
        
        # R-multiple statistics
        avg_win_r = completed_trades[completed_trades['outcome'] == 'WIN']['r_multiple'].mean()
        avg_loss_r = abs(completed_trades[completed_trades['outcome'] == 'LOSS']['r_multiple'].mean())
        avg_r = completed_trades['r_multiple'].mean()
        
        # Profit factor
        gross_profit = completed_trades[completed_trades['pnl_points'] > 0]['pnl_points'].sum()
        gross_loss = abs(completed_trades[completed_trades['pnl_points'] < 0]['pnl_points'].sum())
        profit_factor = (gross_profit / gross_loss) if gross_loss > 0 else float('inf')
        
        # Expectancy
        expectancy = completed_trades['r_multiple'].sum()
        
        # Drawdown calculation
        cumulative_r = completed_trades['r_multiple'].cumsum()
        running_max = cumulative_r.cummax()
        drawdown = running_max - cumulative_r
        max_drawdown = drawdown.max()
        
        # Win/loss streaks
        outcomes = completed_trades['outcome'].values
        current_streak = 1
        max_win_streak = 1
        max_loss_streak = 1
        
        for i in range(1, len(outcomes)):
            if outcomes[i] == outcomes[i-1]:
                current_streak += 1
                if outcomes[i] == 'WIN':
                    max_win_streak = max(max_win_streak, current_streak)
                else:
                    max_loss_streak = max(max_loss_streak, current_streak)
            else:
                current_streak = 1
        
        return {
            'total_trades': total_trades,
            'winning_trades': winning_trades,
            'losing_trades': losing_trades,
            'win_rate': win_rate,
            'avg_win_r': avg_win_r,
            'avg_loss_r': avg_loss_r,
            'avg_r': avg_r,
            'total_r': expectancy,
            'profit_factor': profit_factor,
            'max_drawdown_r': max_drawdown,
            'max_win_streak': max_win_streak,
            'max_loss_streak': max_loss_streak,
            'avg_rr_ratio': completed_trades['rr_ratio'].mean()
        }
    
    def generate_report(self, output_file: str = 'BACKTEST_RESULTS_NQ_2018_2025.md'):
        """
        Generate comprehensive markdown report
        
        Args:
            output_file: Output filename
        """
        if not self.trades:
            print("❌ No trades to report!")
            return
        
        print(f"\n📝 Generating comprehensive report: {output_file}")
        
        trades_df = pd.DataFrame(self.trades)
        
        # Overall metrics
        overall_metrics = self.calculate_metrics(trades_df)
        
        # Metrics by scenario
        scenario_metrics = {}
        for scenario in ['COMPRESSION', 'EXPANSION', 'CONTINUATION']:
            scenario_trades = trades_df[trades_df['scenario'] == scenario]
            if len(scenario_trades) > 0:
                scenario_metrics[scenario] = self.calculate_metrics(scenario_trades)
        
        # Generate report
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# 📊 BACKTEST RESULTS: NQ LONDON-TOKYO KILLZONE (2018-2025)\n\n")
            f.write("## 🎯 EXECUTIVE SUMMARY\n\n")
            
            f.write(f"**Backtest Period:** {trades_df['date'].min()} to {trades_df['date'].max()}\n\n")
            f.write(f"**Total Trades Executed:** {overall_metrics['total_trades']}\n\n")
            f.write(f"**Overall Win Rate:** {overall_metrics['win_rate']:.2f}%\n\n")
            f.write(f"**Total Return:** {overall_metrics['total_r']:.2f}R\n\n")
            f.write(f"**Profit Factor:** {overall_metrics['profit_factor']:.2f}\n\n")
            f.write(f"**Average R-Multiple:** {overall_metrics['avg_r']:.2f}R\n\n")
            f.write(f"**Maximum Drawdown:** {overall_metrics['max_drawdown_r']:.2f}R\n\n")
            
            # Performance interpretation
            f.write("### 💰 Performance Interpretation\n\n")
            
            if overall_metrics['total_r'] > 150:
                f.write("✅ **EXCEPTIONAL PERFORMANCE** - Strategy significantly exceeds institutional benchmarks.\n\n")
            elif overall_metrics['total_r'] > 100:
                f.write("✅ **STRONG PERFORMANCE** - Strategy meets institutional profitability standards.\n\n")
            elif overall_metrics['total_r'] > 50:
                f.write("⚠️ **MODERATE PERFORMANCE** - Strategy is profitable but requires optimization.\n\n")
            else:
                f.write("❌ **UNDERPERFORMANCE** - Strategy needs significant refinement.\n\n")
            
            # Detailed metrics by scenario
            f.write("---\n\n")
            f.write("## 📈 DETAILED RESULTS BY SCENARIO\n\n")
            
            # Create comparison table
            f.write("| Metric | Scenario 1: COMPRESSION | Scenario 2: EXPANSION | Scenario 3: CONTINUATION |\n")
            f.write("|--------|------------------------|----------------------|-------------------------|\n")
            
            metrics_to_show = [
                ('Total Trades', 'total_trades', ''),
                ('Win Rate', 'win_rate', '%'),
                ('Avg Win', 'avg_win_r', 'R'),
                ('Avg Loss', 'avg_loss_r', 'R'),
                ('Avg R-Multiple', 'avg_r', 'R'),
                ('Total Return', 'total_r', 'R'),
                ('Profit Factor', 'profit_factor', ''),
                ('Max Drawdown', 'max_drawdown_r', 'R'),
            ]
            
            for metric_name, metric_key, suffix in metrics_to_show:
                row = f"| **{metric_name}** |"
                
                for scenario in ['COMPRESSION', 'EXPANSION', 'CONTINUATION']:
                    if scenario in scenario_metrics and metric_key in scenario_metrics[scenario]:
                        value = scenario_metrics[scenario][metric_key]
                        if suffix == '%':
                            row += f" {value:.2f}% |"
                        elif suffix == 'R':
                            row += f" {value:.2f}R |"
                        else:
                            if isinstance(value, float):
                                row += f" {value:.2f} |"
                            else:
                                row += f" {value} |"
                    else:
                        row += " N/A |"
                
                f.write(row + "\n")
            
            f.write("\n---\n\n")
            
            # Individual scenario analysis
            for scenario in ['COMPRESSION', 'EXPANSION', 'CONTINUATION']:
                if scenario not in scenario_metrics:
                    continue
                
                metrics = scenario_metrics[scenario]
                scenario_name = {
                    'COMPRESSION': 'SCENARIO 1: COMPRESSION (London Reversal / Liquidity Sweep)',
                    'EXPANSION': 'SCENARIO 2: EXPANSION (Asian Fade)',
                    'CONTINUATION': 'SCENARIO 3: CONTINUATION (London Breakout)'
                }[scenario]
                
                f.write(f"### {scenario_name}\n\n")
                
                f.write(f"**Trading Statistics:**\n")
                f.write(f"- Total Trades: {metrics['total_trades']}\n")
                f.write(f"- Winners: {metrics['winning_trades']} | Losers: {metrics['losing_trades']}\n")
                f.write(f"- Win Rate: {metrics['win_rate']:.2f}%\n")
                f.write(f"- Longest Win Streak: {metrics['max_win_streak']} | Longest Loss Streak: {metrics['max_loss_streak']}\n\n")
                
                f.write(f"**Risk/Reward Metrics:**\n")
                f.write(f"- Average Win: {metrics['avg_win_r']:.2f}R\n")
                f.write(f"- Average Loss: {metrics['avg_loss_r']:.2f}R\n")
                f.write(f"- Average R-Multiple: {metrics['avg_r']:.2f}R\n")
                f.write(f"- Average R:R Ratio: {metrics['avg_rr_ratio']:.2f}\n\n")
                
                f.write(f"**Performance:**\n")
                f.write(f"- Total Return: {metrics['total_r']:.2f}R\n")
                f.write(f"- Profit Factor: {metrics['profit_factor']:.2f}\n")
                f.write(f"- Maximum Drawdown: {metrics['max_drawdown_r']:.2f}R\n\n")
                
                # Interpretation
                f.write("**Analysis:**\n")
                
                if metrics['win_rate'] >= 50:
                    f.write(f"✅ Win rate of {metrics['win_rate']:.1f}% meets or exceeds institutional expectations.\n")
                else:
                    f.write(f"⚠️ Win rate of {metrics['win_rate']:.1f}% is below target but may be acceptable with proper R:R.\n")
                
                if metrics['profit_factor'] >= 2.0:
                    f.write(f"✅ Profit factor of {metrics['profit_factor']:.2f} indicates strong edge.\n")
                elif metrics['profit_factor'] >= 1.5:
                    f.write(f"⚠️ Profit factor of {metrics['profit_factor']:.2f} is acceptable but could be improved.\n")
                else:
                    f.write(f"❌ Profit factor of {metrics['profit_factor']:.2f} needs improvement.\n")
                
                f.write("\n---\n\n")
            
            # Monthly performance
            f.write("## 📅 PERFORMANCE BY YEAR\n\n")
            
            trades_df['year'] = pd.to_datetime(trades_df['date']).dt.year
            yearly_performance = trades_df.groupby('year').agg({
                'r_multiple': ['sum', 'mean', 'count']
            }).round(2)
            
            f.write("| Year | Total Trades | Total Return (R) | Avg R per Trade |\n")
            f.write("|------|-------------|------------------|----------------|\n")
            
            for year in sorted(trades_df['year'].unique()):
                year_trades = trades_df[trades_df['year'] == year]
                year_trades_completed = year_trades[year_trades['outcome'].isin(['WIN', 'LOSS'])]
                
                if len(year_trades_completed) > 0:
                    total_r = year_trades_completed['r_multiple'].sum()
                    avg_r = year_trades_completed['r_multiple'].mean()
                    count = len(year_trades_completed)
                    
                    f.write(f"| {year} | {count} | {total_r:.2f}R | {avg_r:.2f}R |\n")
            
            f.write("\n---\n\n")
            
            # Daily bias performance
            f.write("## 🎯 PERFORMANCE BY DAILY BIAS\n\n")
            
            f.write("| Daily Bias | Total Trades | Win Rate | Avg R | Total Return |\n")
            f.write("|-----------|-------------|----------|-------|-------------|\n")
            
            for bias in ['BULLISH', 'BEARISH', 'NEUTRAL']:
                bias_trades = trades_df[trades_df['daily_bias'] == bias]
                bias_trades_completed = bias_trades[bias_trades['outcome'].isin(['WIN', 'LOSS'])]
                
                if len(bias_trades_completed) > 0:
                    metrics = self.calculate_metrics(bias_trades_completed)
                    f.write(f"| {bias} | {metrics['total_trades']} | {metrics['win_rate']:.2f}% | "
                           f"{metrics['avg_r']:.2f}R | {metrics['total_r']:.2f}R |\n")
            
            f.write("\n---\n\n")
            
            # Key insights
            f.write("## 💡 KEY INSIGHTS & RECOMMENDATIONS\n\n")
            
            f.write("### Strengths:\n")
            
            # Find best performing scenario
            best_scenario = max(scenario_metrics.items(), key=lambda x: x[1]['total_r'])
            f.write(f"- **{best_scenario[0]}** scenario shows strongest performance with "
                   f"{best_scenario[1]['total_r']:.2f}R total return\n")
            
            # Check consistency
            if overall_metrics['profit_factor'] > 2.0:
                f.write(f"- Strong profit factor of {overall_metrics['profit_factor']:.2f} demonstrates consistent edge\n")
            
            if overall_metrics['win_rate'] > 50:
                f.write(f"- Win rate of {overall_metrics['win_rate']:.2f}% exceeds 50% threshold\n")
            
            f.write("\n### Areas for Improvement:\n")
            
            # Find weakest scenario
            if len(scenario_metrics) > 1:
                weak_scenario = min(scenario_metrics.items(), key=lambda x: x[1]['total_r'])
                f.write(f"- **{weak_scenario[0]}** scenario needs refinement (only {weak_scenario[1]['total_r']:.2f}R total)\n")
            
            if overall_metrics['max_drawdown_r'] > 15:
                f.write(f"- Maximum drawdown of {overall_metrics['max_drawdown_r']:.2f}R exceeds 15R threshold\n")
            
            f.write("\n### Recommendations:\n")
            f.write("1. **Focus on High-Performing Scenarios:** Allocate more capital to scenarios with best risk-adjusted returns\n")
            f.write("2. **Refine Entry Timing:** Consider adding filters to reduce losing streaks\n")
            f.write("3. **Daily Bias Filter:** Strictly trade with the daily bias for optimal results\n")
            f.write("4. **Position Sizing:** Use variable position sizing based on scenario win rate\n")
            f.write("5. **Risk Management:** Keep maximum drawdown under 15R through proper position sizing\n")
            
            f.write("\n---\n\n")
            
            # Footer
            f.write("## 📌 DISCLAIMER\n\n")
            f.write("*This backtest is based on historical data and does not guarantee future performance. "
                   "Past results do not predict future returns. Trading involves substantial risk of loss. "
                   "This analysis is for educational purposes only and is not financial advice.*\n\n")
            
            f.write("---\n\n")
            f.write(f"**Report Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("**Backtest Engine:** London-Tokyo Killzone Backtest System v1.0\n")
        
        print(f"✅ Report saved to {output_file}")
    
    def generate_charts(self, output_dir: str = '.'):
        """
        Generate performance visualization charts
        
        Args:
            output_dir: Directory to save charts
        """
        if not self.trades:
            print("❌ No trades to visualize!")
            return
        
        print(f"\n📊 Generating performance charts...")
        
        trades_df = pd.DataFrame(self.trades)
        completed_trades = trades_df[trades_df['outcome'].isin(['WIN', 'LOSS'])]
        
        if len(completed_trades) == 0:
            print("❌ No completed trades to visualize!")
            return
        
        # Create figure with subplots
        fig = plt.figure(figsize=(20, 12))
        
        # 1. Equity Curve
        ax1 = plt.subplot(2, 3, 1)
        completed_trades['cumulative_r'] = completed_trades['r_multiple'].cumsum()
        ax1.plot(completed_trades.index, completed_trades['cumulative_r'], linewidth=2, color='#2E86AB')
        ax1.fill_between(completed_trades.index, completed_trades['cumulative_r'], alpha=0.3, color='#2E86AB')
        ax1.set_title('Cumulative Equity Curve', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Trade Number')
        ax1.set_ylabel('Cumulative R-Multiple')
        ax1.grid(True, alpha=0.3)
        ax1.axhline(y=0, color='red', linestyle='--', linewidth=1)
        
        # 2. R-Multiple Distribution
        ax2 = plt.subplot(2, 3, 2)
        ax2.hist(completed_trades['r_multiple'], bins=30, edgecolor='black', alpha=0.7, color='#A23B72')
        ax2.set_title('R-Multiple Distribution', fontsize=14, fontweight='bold')
        ax2.set_xlabel('R-Multiple')
        ax2.set_ylabel('Frequency')
        ax2.axvline(x=0, color='red', linestyle='--', linewidth=2)
        ax2.grid(True, alpha=0.3)
        
        # 3. Win Rate by Scenario
        ax3 = plt.subplot(2, 3, 3)
        scenario_win_rates = []
        scenarios = []
        
        for scenario in ['COMPRESSION', 'EXPANSION', 'CONTINUATION']:
            scenario_trades = completed_trades[completed_trades['scenario'] == scenario]
            if len(scenario_trades) > 0:
                win_rate = (len(scenario_trades[scenario_trades['outcome'] == 'WIN']) / len(scenario_trades)) * 100
                scenario_win_rates.append(win_rate)
                scenarios.append(scenario)
        
        colors = ['#F18F01', '#C73E1D', '#6A994E']
        bars = ax3.bar(scenarios, scenario_win_rates, color=colors[:len(scenarios)], edgecolor='black')
        ax3.set_title('Win Rate by Scenario', fontsize=14, fontweight='bold')
        ax3.set_ylabel('Win Rate (%)')
        ax3.set_ylim(0, 100)
        ax3.axhline(y=50, color='blue', linestyle='--', linewidth=1, label='50% Threshold')
        ax3.legend()
        ax3.grid(True, alpha=0.3, axis='y')
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}%', ha='center', va='bottom', fontweight='bold')
        
        # 4. Monthly Performance
        ax4 = plt.subplot(2, 3, 4)
        completed_trades['year_month'] = pd.to_datetime(completed_trades['date']).dt.to_period('M')
        monthly_perf = completed_trades.groupby('year_month')['r_multiple'].sum()
        
        colors_monthly = ['green' if x > 0 else 'red' for x in monthly_perf.values]
        ax4.bar(range(len(monthly_perf)), monthly_perf.values, color=colors_monthly, alpha=0.7, edgecolor='black')
        ax4.set_title('Monthly Performance', fontsize=14, fontweight='bold')
        ax4.set_xlabel('Month')
        ax4.set_ylabel('R-Multiple')
        ax4.axhline(y=0, color='black', linewidth=1)
        ax4.grid(True, alpha=0.3, axis='y')
        
        # 5. Profit Factor by Scenario
        ax5 = plt.subplot(2, 3, 5)
        profit_factors = []
        
        for scenario in ['COMPRESSION', 'EXPANSION', 'CONTINUATION']:
            scenario_trades = completed_trades[completed_trades['scenario'] == scenario]
            if len(scenario_trades) > 0:
                gross_profit = scenario_trades[scenario_trades['pnl_points'] > 0]['pnl_points'].sum()
                gross_loss = abs(scenario_trades[scenario_trades['pnl_points'] < 0]['pnl_points'].sum())
                pf = (gross_profit / gross_loss) if gross_loss > 0 else 0
                profit_factors.append(pf)
        
        bars = ax5.bar(scenarios, profit_factors, color=colors[:len(scenarios)], edgecolor='black')
        ax5.set_title('Profit Factor by Scenario', fontsize=14, fontweight='bold')
        ax5.set_ylabel('Profit Factor')
        ax5.axhline(y=2.0, color='green', linestyle='--', linewidth=1, label='Target: 2.0')
        ax5.axhline(y=1.0, color='red', linestyle='--', linewidth=1, label='Break-even')
        ax5.legend()
        ax5.grid(True, alpha=0.3, axis='y')
        
        # Add value labels
        for bar in bars:
            height = bar.get_height()
            ax5.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.2f}', ha='center', va='bottom', fontweight='bold')
        
        # 6. Drawdown
        ax6 = plt.subplot(2, 3, 6)
        cumulative_r = completed_trades['r_multiple'].cumsum()
        running_max = cumulative_r.cummax()
        drawdown = running_max - cumulative_r
        
        ax6.fill_between(completed_trades.index, drawdown, alpha=0.5, color='red')
        ax6.plot(completed_trades.index, drawdown, linewidth=2, color='darkred')
        ax6.set_title('Drawdown Profile', fontsize=14, fontweight='bold')
        ax6.set_xlabel('Trade Number')
        ax6.set_ylabel('Drawdown (R)')
        ax6.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        output_file = os.path.join(output_dir, 'backtest_performance_charts.png')
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✅ Charts saved to {output_file}")
        
        # Generate additional scenario comparison chart
        self._generate_scenario_comparison_chart(completed_trades, output_dir)
    
    def _generate_scenario_comparison_chart(self, trades_df: pd.DataFrame, output_dir: str):
        """Generate detailed scenario comparison chart"""
        
        fig, axes = plt.subplots(1, 3, figsize=(18, 6))
        
        scenarios = ['COMPRESSION', 'EXPANSION', 'CONTINUATION']
        scenario_names = {
            'COMPRESSION': 'Scenario 1:\nCompression',
            'EXPANSION': 'Scenario 2:\nExpansion',
            'CONTINUATION': 'Scenario 3:\nContinuation'
        }
        
        for idx, scenario in enumerate(scenarios):
            ax = axes[idx]
            scenario_trades = trades_df[trades_df['scenario'] == scenario]
            
            if len(scenario_trades) > 0:
                # Calculate equity curve for this scenario
                scenario_trades = scenario_trades.sort_values('entry_time')
                scenario_trades['cumulative_r'] = scenario_trades['r_multiple'].cumsum()
                
                ax.plot(range(len(scenario_trades)), scenario_trades['cumulative_r'], 
                       linewidth=2.5, color='#2E86AB')
                ax.fill_between(range(len(scenario_trades)), scenario_trades['cumulative_r'], 
                               alpha=0.3, color='#2E86AB')
                
                # Add stats
                total_r = scenario_trades['r_multiple'].sum()
                win_rate = (len(scenario_trades[scenario_trades['outcome'] == 'WIN']) / 
                          len(scenario_trades)) * 100
                
                ax.set_title(f"{scenario_names[scenario]}\nTotal: {total_r:.1f}R | WR: {win_rate:.1f}%", 
                           fontsize=12, fontweight='bold')
                ax.set_xlabel('Trade Number')
                ax.set_ylabel('Cumulative R')
                ax.grid(True, alpha=0.3)
                ax.axhline(y=0, color='red', linestyle='--', linewidth=1)
        
        plt.tight_layout()
        
        output_file = os.path.join(output_dir, 'scenario_comparison_chart.png')
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✅ Scenario comparison chart saved to {output_file}")


def main():
    """
    Main execution function
    """
    print("\n" + "="*70)
    print("🏛️  LONDON-TOKYO KILLZONE BACKTEST SYSTEM")
    print("    NQ Futures | 2018-2025 | Institutional Analysis")
    print("="*70)
    
    # Initialize backtest system
    backtest = LondonTokyoBacktest(slippage_points=1.5)
    
    # Load data
    backtest.load_data(years=[2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025])
    
    # Run backtest
    trades_df = backtest.run_backtest()
    
    # Generate comprehensive report
    backtest.generate_report('BACKTEST_RESULTS_NQ_2018_2025.md')
    
    # Generate performance charts
    backtest.generate_charts('.')
    
    print("\n" + "="*70)
    print("✅ BACKTEST COMPLETE!")
    print("="*70)
    print("\n📁 Generated files:")
    print("   1. BACKTEST_RESULTS_NQ_2018_2025.md - Comprehensive results report")
    print("   2. backtest_performance_charts.png - Performance visualizations")
    print("   3. scenario_comparison_chart.png - Scenario comparison")
    print("\n" + "="*70)


if __name__ == "__main__":
    main()

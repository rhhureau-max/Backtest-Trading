"""
ICT Three Strategies Backtesting Script
========================================
A comprehensive backtesting system for three distinct ICT (Inner Circle Trader) strategies:
- Strategy A: Silver Bullet (Time-Based)
- Strategy B: 2022 Mentorship Model (Structure-Based)
- Strategy C: Unicorn Model (OB + FVG Confluence)

Author: Senior Quantitative Developer
Data: NQ (Nasdaq 100) Futures 2018-Present
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, time
import os
import warnings
warnings.filterwarnings('ignore')


class ICT_Features:
    """
    Phase 1: Feature Engineering & Pattern Recognition
    
    This class adds ICT-specific features to a dataframe:
    - Swing Points (Highs and Lows)
    - Fair Value Gaps (FVG)
    - Market Structure Shift (MSS)
    - Order Blocks (OB)
    """
    
    def __init__(self, df):
        """
        Initialize with a dataframe containing OHLCV data
        
        Args:
            df: DataFrame with columns ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
        """
        self.df = df.copy()
        self.df.reset_index(drop=True, inplace=True)
        
    def detect_swing_points(self, window=1):
        """
        Detect Swing Highs and Swing Lows using 3-candle fractal pattern (vectorized)
        
        Swing High: High[i] > High[i-1] AND High[i] > High[i+1]
        Swing Low: Low[i] < Low[i-1] AND Low[i] < Low[i+1]
        
        Args:
            window: lookback/forward period (default=1 for 3-candle pattern)
        """
        self.df['Swing_High'] = 0.0
        self.df['Swing_Low'] = 0.0
        
        # Vectorized approach for 3-candle fractal (window=1)
        if window == 1:
            # Swing High: High[i] > High[i-1] AND High[i] > High[i+1]
            swing_high_mask = (self.df['High'] > self.df['High'].shift(1)) & \
                              (self.df['High'] > self.df['High'].shift(-1))
            self.df.loc[swing_high_mask, 'Swing_High'] = self.df.loc[swing_high_mask, 'High']
            
            # Swing Low: Low[i] < Low[i-1] AND Low[i] < Low[i+1]
            swing_low_mask = (self.df['Low'] < self.df['Low'].shift(1)) & \
                             (self.df['Low'] < self.df['Low'].shift(-1))
            self.df.loc[swing_low_mask, 'Swing_Low'] = self.df.loc[swing_low_mask, 'Low']
        else:
            # Original loop for other window sizes
            for i in range(window, len(self.df) - window):
                # Check for Swing High
                is_swing_high = True
                for j in range(1, window + 1):
                    if self.df.loc[i, 'High'] <= self.df.loc[i-j, 'High'] or \
                       self.df.loc[i, 'High'] <= self.df.loc[i+j, 'High']:
                        is_swing_high = False
                        break
                
                if is_swing_high:
                    self.df.loc[i, 'Swing_High'] = self.df.loc[i, 'High']
                
                # Check for Swing Low
                is_swing_low = True
                for j in range(1, window + 1):
                    if self.df.loc[i, 'Low'] >= self.df.loc[i-j, 'Low'] or \
                       self.df.loc[i, 'Low'] >= self.df.loc[i+j, 'Low']:
                        is_swing_low = False
                        break
                
                if is_swing_low:
                    self.df.loc[i, 'Swing_Low'] = self.df.loc[i, 'Low']
        
        return self
    
    def detect_fvg(self):
        """
        Detect Fair Value Gaps (FVG)
        
        Bullish FVG: Low[i] > High[i-2] (gap up)
        - Gap zone: Between High[i-2] and Low[i]
        
        Bearish FVG: High[i] < Low[i-2] (gap down)
        - Gap zone: Between Low[i-2] and High[i]
        
        Stores: FVG_Bullish_Top, FVG_Bullish_Bottom, FVG_Bullish_Mean
                FVG_Bearish_Top, FVG_Bearish_Bottom, FVG_Bearish_Mean
        """
        self.df['FVG_Bullish_Top'] = np.nan
        self.df['FVG_Bullish_Bottom'] = np.nan
        self.df['FVG_Bullish_Mean'] = np.nan
        
        self.df['FVG_Bearish_Top'] = np.nan
        self.df['FVG_Bearish_Bottom'] = np.nan
        self.df['FVG_Bearish_Mean'] = np.nan
        
        for i in range(2, len(self.df)):
            # Bullish FVG: Low[i] > High[i-2]
            if self.df.loc[i, 'Low'] > self.df.loc[i-2, 'High']:
                self.df.loc[i, 'FVG_Bullish_Bottom'] = self.df.loc[i-2, 'High']
                self.df.loc[i, 'FVG_Bullish_Top'] = self.df.loc[i, 'Low']
                self.df.loc[i, 'FVG_Bullish_Mean'] = (self.df.loc[i-2, 'High'] + self.df.loc[i, 'Low']) / 2
            
            # Bearish FVG: High[i] < Low[i-2]
            if self.df.loc[i, 'High'] < self.df.loc[i-2, 'Low']:
                self.df.loc[i, 'FVG_Bearish_Top'] = self.df.loc[i-2, 'Low']
                self.df.loc[i, 'FVG_Bearish_Bottom'] = self.df.loc[i, 'High']
                self.df.loc[i, 'FVG_Bearish_Mean'] = (self.df.loc[i-2, 'Low'] + self.df.loc[i, 'High']) / 2
        
        return self
    
    def detect_mss(self, lookback=20):
        """
        Detect Market Structure Shift (MSS)
        
        Bullish MSS: Price closes above a recent Swing High with displacement
        Bearish MSS: Price closes below a recent Swing Low with displacement
        
        Displacement = large body candle (body > 50% of range)
        
        Args:
            lookback: period to look for previous swing points
        """
        self.df['MSS_Bullish'] = 0
        self.df['MSS_Bearish'] = 0
        
        for i in range(lookback, len(self.df)):
            # Calculate candle body percentage
            body = abs(self.df.loc[i, 'Close'] - self.df.loc[i, 'Open'])
            range_candle = self.df.loc[i, 'High'] - self.df.loc[i, 'Low']
            
            if range_candle > 0:
                body_pct = body / range_candle
            else:
                body_pct = 0
            
            # Check for displacement (body > 50% of range)
            has_displacement = body_pct > 0.5
            
            if has_displacement:
                # Look for recent Swing High
                recent_highs = self.df.loc[i-lookback:i, 'Swing_High']
                recent_highs = recent_highs[recent_highs > 0]
                
                if len(recent_highs) > 0:
                    max_swing_high = recent_highs.max()
                    # Bullish MSS: Close above recent Swing High
                    if self.df.loc[i, 'Close'] > max_swing_high:
                        self.df.loc[i, 'MSS_Bullish'] = 1
                
                # Look for recent Swing Low
                recent_lows = self.df.loc[i-lookback:i, 'Swing_Low']
                recent_lows = recent_lows[recent_lows > 0]
                
                if len(recent_lows) > 0:
                    min_swing_low = recent_lows.min()
                    # Bearish MSS: Close below recent Swing Low
                    if self.df.loc[i, 'Close'] < min_swing_low:
                        self.df.loc[i, 'MSS_Bearish'] = 1
        
        return self
    
    def detect_order_blocks(self):
        """
        Detect Order Blocks (OB)
        
        Bullish OB: Last down-candle (red) before a move that caused Bullish MSS and left an FVG
        Bearish OB: Last up-candle (green) before a move that caused Bearish MSS and left an FVG
        
        Stores: OB_Bullish_High, OB_Bullish_Low
                OB_Bearish_High, OB_Bearish_Low
        """
        self.df['OB_Bullish_High'] = np.nan
        self.df['OB_Bullish_Low'] = np.nan
        self.df['OB_Bearish_High'] = np.nan
        self.df['OB_Bearish_Low'] = np.nan
        
        for i in range(5, len(self.df)):
            # Check for Bullish MSS with FVG
            if self.df.loc[i, 'MSS_Bullish'] == 1 and not pd.isna(self.df.loc[i, 'FVG_Bullish_Top']):
                # Find last down-candle before this point
                for j in range(i-1, max(0, i-10), -1):
                    if self.df.loc[j, 'Close'] < self.df.loc[j, 'Open']:
                        # This is a down-candle (red)
                        self.df.loc[i, 'OB_Bullish_Low'] = self.df.loc[j, 'Low']
                        self.df.loc[i, 'OB_Bullish_High'] = self.df.loc[j, 'High']
                        break
            
            # Check for Bearish MSS with FVG
            if self.df.loc[i, 'MSS_Bearish'] == 1 and not pd.isna(self.df.loc[i, 'FVG_Bearish_Top']):
                # Find last up-candle before this point
                for j in range(i-1, max(0, i-10), -1):
                    if self.df.loc[j, 'Close'] > self.df.loc[j, 'Open']:
                        # This is an up-candle (green)
                        self.df.loc[i, 'OB_Bearish_Low'] = self.df.loc[j, 'Low']
                        self.df.loc[i, 'OB_Bearish_High'] = self.df.loc[j, 'High']
                        break
        
        return self
    
    def get_dataframe(self):
        """Return the dataframe with all features added"""
        return self.df


class DataLoader:
    """
    Load and synchronize multi-timeframe NQ data
    Handles timezone conversion from UTC to US/Eastern
    """
    
    def __init__(self, data_path='/home/runner/work/Backtest-Trading/Backtest-Trading'):
        self.data_path = data_path
        
    def load_data(self, timeframe, start_year=2018, end_year=2025):
        """
        Load NQ data for specified timeframe and year range
        
        Args:
            timeframe: '1m', '5m', '15m', '1H'
            start_year: starting year
            end_year: ending year
        
        Returns:
            DataFrame with columns ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Datetime']
        """
        dfs = []
        
        # Map timeframe to file suffix
        tf_map = {'1m': '1m', '5m': '5m', '15m': '15m', '1H': '1H'}
        
        for year in range(start_year, end_year + 1):
            # Note: 1m data is in zip/xlsx format, we'll skip it for now
            if timeframe == '1m':
                # Skip 1m for now as it's in zip/xlsx format
                continue
            
            filename = f"{year} {tf_map[timeframe]}.csv"
            filepath = os.path.join(self.data_path, filename)
            
            if os.path.exists(filepath):
                try:
                    # Read CSV with semicolon separator
                    df = pd.read_csv(filepath, sep=';')
                    
                    # Rename columns
                    df.columns = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
                    
                    # Parse datetime
                    df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], 
                                                    format='%d/%m/%Y %H:%M:%S')
                    
                    dfs.append(df)
                except Exception as e:
                    print(f"Error loading {filename}: {e}")
        
        if len(dfs) == 0:
            raise ValueError(f"No data loaded for timeframe {timeframe}")
        
        # Concatenate all dataframes
        result = pd.concat(dfs, ignore_index=True)
        result.sort_values('Datetime', inplace=True)
        result.reset_index(drop=True, inplace=True)
        
        # Convert timezone from UTC to US/Eastern
        result['Datetime'] = pd.to_datetime(result['Datetime'], utc=True)
        result['Datetime'] = result['Datetime'].dt.tz_convert('US/Eastern')
        
        # Update Date and Time columns
        result['Date'] = result['Datetime'].dt.date
        result['Time'] = result['Datetime'].dt.time
        
        return result


class Backtester:
    """
    Phase 2: Strategy Logic Implementation
    
    Implements three ICT strategies:
    - Strategy A: Silver Bullet
    - Strategy B: 2022 Mentorship Model
    - Strategy C: Unicorn Model
    """
    
    def __init__(self, m5_data, m15_data, h1_data, initial_capital=100000, risk_per_trade=0.01):
        """
        Initialize backtester with multi-timeframe data
        
        Args:
            m5_data: 5-minute dataframe with ICT features
            m15_data: 15-minute dataframe with ICT features
            h1_data: 1-hour dataframe with ICT features
            initial_capital: starting capital ($100,000)
            risk_per_trade: risk percentage per trade (1% = 0.01)
        """
        self.m5_data = m5_data.copy()
        self.m15_data = m15_data.copy()
        self.h1_data = h1_data.copy()
        
        self.initial_capital = initial_capital
        self.risk_per_trade = risk_per_trade
        
        # NQ futures: $20 per point
        self.point_value = 20
        
        # Results storage
        self.strategy_results = {
            'A': {'trades': [], 'equity_curve': []},
            'B': {'trades': [], 'equity_curve': []},
            'C': {'trades': [], 'equity_curve': []}
        }
    
    def get_h1_trend_bias(self, current_datetime):
        """
        Determine trend bias from H1 timeframe
        Uses simple price > EMA 50 logic
        
        Returns: 'bullish', 'bearish', or 'neutral'
        """
        # Get H1 data up to current time
        h1_subset = self.h1_data[self.h1_data['Datetime'] <= current_datetime].copy()
        
        if len(h1_subset) < 50:
            return 'neutral'
        
        # Calculate EMA 50
        h1_subset['EMA_50'] = h1_subset['Close'].ewm(span=50, adjust=False).mean()
        
        last_close = h1_subset.iloc[-1]['Close']
        last_ema = h1_subset.iloc[-1]['EMA_50']
        
        if last_close > last_ema:
            return 'bullish'
        elif last_close < last_ema:
            return 'bearish'
        else:
            return 'neutral'
    
    def get_session_high_low(self, current_datetime, lookback_hours=12):
        """
        Get previous session high/low for liquidity sweep detection
        
        Args:
            current_datetime: current timestamp
            lookback_hours: hours to look back for high/low
        
        Returns: (session_high, session_low)
        """
        # Get M5 data from previous session
        start_time = current_datetime - pd.Timedelta(hours=lookback_hours)
        session_data = self.m5_data[
            (self.m5_data['Datetime'] >= start_time) & 
            (self.m5_data['Datetime'] < current_datetime)
        ]
        
        if len(session_data) == 0:
            return None, None
        
        return session_data['High'].max(), session_data['Low'].min()
    
    def strategy_a_silver_bullet(self):
        """
        Strategy A: The "Silver Bullet" (Time-Based)
        
        Time Window: 10:00 AM - 11:00 AM EST
        Setup: Liquidity Sweep + FVG creation on M5
        Entry: Limit order at FVG Low (buy) or FVG High (sell)
        Stop Loss: 5 points below Swing Low
        Take Profit: 2:1 Risk/Reward
        """
        print("\n=== Running Strategy A: Silver Bullet ===")
        
        capital = self.initial_capital
        trades = []
        equity_curve = [(self.m5_data.iloc[0]['Datetime'], capital)]
        
        # Filter M5 data for time window 10:00-11:00 EST
        m5_silvertime = self.m5_data[
            (self.m5_data['Time'] >= time(10, 0)) & 
            (self.m5_data['Time'] <= time(11, 0))
        ].copy()
        
        i = 0
        while i < len(m5_silvertime):
            row = m5_silvertime.iloc[i]
            current_datetime = row['Datetime']
            
            # Get session high/low for liquidity sweep detection
            session_high, session_low = self.get_session_high_low(current_datetime)
            
            if session_high is None or session_low is None:
                i += 1
                continue
            
            # Check for liquidity sweep
            swept_high = row['High'] > session_high
            swept_low = row['Low'] < session_low
            
            # Look for FVG in next few candles after sweep
            if swept_high or swept_low:
                for j in range(i+1, min(i+10, len(m5_silvertime))):
                    fvg_row = m5_silvertime.iloc[j]
                    
                    # Bullish setup: Swept low + Bullish FVG
                    if swept_low and not pd.isna(fvg_row['FVG_Bullish_Top']):
                        # Find swing low for stop loss
                        swing_lows = m5_silvertime.iloc[max(0, j-20):j]['Swing_Low']
                        swing_lows = swing_lows[swing_lows > 0]
                        
                        if len(swing_lows) > 0:
                            swing_low = swing_lows.min()
                            
                            # Entry at FVG Low (proximal line)
                            entry_price = fvg_row['FVG_Bullish_Bottom']
                            stop_loss = swing_low - 5  # 5 points below swing low
                            risk_points = entry_price - stop_loss
                            
                            if risk_points > 0:
                                # 2:1 Risk/Reward
                                take_profit = entry_price + (2 * risk_points)
                                
                                # Position sizing: 1% risk
                                risk_amount = capital * self.risk_per_trade
                                position_size = risk_amount / (risk_points * self.point_value)
                                
                                # Simulate trade execution - check if price touches entry
                                trade_executed = False
                                for k in range(j+1, min(j+20, len(m5_silvertime))):
                                    exec_row = m5_silvertime.iloc[k]
                                    
                                    # Check if entry is filled
                                    if exec_row['Low'] <= entry_price:
                                        trade_executed = True
                                        entry_datetime = exec_row['Datetime']
                                        
                                        # Check exit conditions
                                        for m in range(k+1, len(m5_silvertime)):
                                            exit_row = m5_silvertime.iloc[m]
                                            
                                            # Stop loss hit
                                            if exit_row['Low'] <= stop_loss:
                                                pnl_points = stop_loss - entry_price
                                                pnl = pnl_points * self.point_value * position_size
                                                capital += pnl
                                                
                                                trades.append({
                                                    'entry_time': entry_datetime,
                                                    'exit_time': exit_row['Datetime'],
                                                    'direction': 'LONG',
                                                    'entry_price': entry_price,
                                                    'exit_price': stop_loss,
                                                    'stop_loss': stop_loss,
                                                    'take_profit': take_profit,
                                                    'pnl': pnl,
                                                    'pnl_points': pnl_points
                                                })
                                                equity_curve.append((exit_row['Datetime'], capital))
                                                break
                                            
                                            # Take profit hit
                                            if exit_row['High'] >= take_profit:
                                                pnl_points = take_profit - entry_price
                                                pnl = pnl_points * self.point_value * position_size
                                                capital += pnl
                                                
                                                trades.append({
                                                    'entry_time': entry_datetime,
                                                    'exit_time': exit_row['Datetime'],
                                                    'direction': 'LONG',
                                                    'entry_price': entry_price,
                                                    'exit_price': take_profit,
                                                    'stop_loss': stop_loss,
                                                    'take_profit': take_profit,
                                                    'pnl': pnl,
                                                    'pnl_points': pnl_points
                                                })
                                                equity_curve.append((exit_row['Datetime'], capital))
                                                break
                                        
                                        break
                                
                                if trade_executed:
                                    i = m + 1
                                    break
                    
                    # Bearish setup: Swept high + Bearish FVG
                    if swept_high and not pd.isna(fvg_row['FVG_Bearish_Top']):
                        # Find swing high for stop loss
                        swing_highs = m5_silvertime.iloc[max(0, j-20):j]['Swing_High']
                        swing_highs = swing_highs[swing_highs > 0]
                        
                        if len(swing_highs) > 0:
                            swing_high = swing_highs.max()
                            
                            # Entry at FVG High (proximal line)
                            entry_price = fvg_row['FVG_Bearish_Top']
                            stop_loss = swing_high + 5  # 5 points above swing high
                            risk_points = stop_loss - entry_price
                            
                            if risk_points > 0:
                                # 2:1 Risk/Reward
                                take_profit = entry_price - (2 * risk_points)
                                
                                # Position sizing: 1% risk
                                risk_amount = capital * self.risk_per_trade
                                position_size = risk_amount / (risk_points * self.point_value)
                                
                                # Simulate trade execution
                                trade_executed = False
                                for k in range(j+1, min(j+20, len(m5_silvertime))):
                                    exec_row = m5_silvertime.iloc[k]
                                    
                                    if exec_row['High'] >= entry_price:
                                        trade_executed = True
                                        entry_datetime = exec_row['Datetime']
                                        
                                        for m in range(k+1, len(m5_silvertime)):
                                            exit_row = m5_silvertime.iloc[m]
                                            
                                            # Stop loss hit
                                            if exit_row['High'] >= stop_loss:
                                                pnl_points = entry_price - stop_loss
                                                pnl = pnl_points * self.point_value * position_size
                                                capital += pnl
                                                
                                                trades.append({
                                                    'entry_time': entry_datetime,
                                                    'exit_time': exit_row['Datetime'],
                                                    'direction': 'SHORT',
                                                    'entry_price': entry_price,
                                                    'exit_price': stop_loss,
                                                    'stop_loss': stop_loss,
                                                    'take_profit': take_profit,
                                                    'pnl': pnl,
                                                    'pnl_points': pnl_points
                                                })
                                                equity_curve.append((exit_row['Datetime'], capital))
                                                break
                                            
                                            # Take profit hit
                                            if exit_row['Low'] <= take_profit:
                                                pnl_points = entry_price - take_profit
                                                pnl = pnl_points * self.point_value * position_size
                                                capital += pnl
                                                
                                                trades.append({
                                                    'entry_time': entry_datetime,
                                                    'exit_time': exit_row['Datetime'],
                                                    'direction': 'SHORT',
                                                    'entry_price': entry_price,
                                                    'exit_price': take_profit,
                                                    'stop_loss': stop_loss,
                                                    'take_profit': take_profit,
                                                    'pnl': pnl,
                                                    'pnl_points': pnl_points
                                                })
                                                equity_curve.append((exit_row['Datetime'], capital))
                                                break
                                        
                                        break
                                
                                if trade_executed:
                                    i = m + 1
                                    break
            
            i += 1
        
        self.strategy_results['A']['trades'] = trades
        self.strategy_results['A']['equity_curve'] = equity_curve
        
        return trades, equity_curve
    
    def strategy_b_mentorship_model(self):
        """
        Strategy B: The "2022 Mentorship Model" (Structure-Based)
        
        Context: H1 trend bias (Price > EMA 50)
        Trigger: M5 MSS contrary to short-term but aligned with H1
        Confirmation: Displacement leaves FVG
        Entry: Limit at FVG
        Stop Loss: Above/Below MSS Swing High/Low
        Take Profit: Next major Swing Point
        """
        print("\n=== Running Strategy B: 2022 Mentorship Model ===")
        
        capital = self.initial_capital
        trades = []
        equity_curve = [(self.m5_data.iloc[0]['Datetime'], capital)]
        
        for i in range(50, len(self.m5_data)):
            row = self.m5_data.iloc[i]
            current_datetime = row['Datetime']
            
            # Get H1 trend bias
            h1_bias = self.get_h1_trend_bias(current_datetime)
            
            if h1_bias == 'neutral':
                continue
            
            # Look for MSS on M5
            if h1_bias == 'bullish' and row['MSS_Bullish'] == 1:
                # Check for FVG confirmation
                if not pd.isna(row['FVG_Bullish_Top']):
                    # Find swing low for stop loss
                    swing_lows = self.m5_data.iloc[max(0, i-20):i]['Swing_Low']
                    swing_lows = swing_lows[swing_lows > 0]
                    
                    if len(swing_lows) > 0:
                        swing_low = swing_lows.min()
                        
                        # Entry at FVG proximal (bottom)
                        entry_price = row['FVG_Bullish_Bottom']
                        stop_loss = swing_low - 5
                        risk_points = entry_price - stop_loss
                        
                        if risk_points > 0:
                            # Target next major swing high
                            future_swings = self.m5_data.iloc[i:min(i+100, len(self.m5_data))]['Swing_High']
                            future_swings = future_swings[future_swings > entry_price]
                            
                            if len(future_swings) > 0:
                                take_profit = future_swings.iloc[0]
                            else:
                                # Default to 2:1 if no swing found
                                take_profit = entry_price + (2 * risk_points)
                            
                            # Position sizing
                            risk_amount = capital * self.risk_per_trade
                            position_size = risk_amount / (risk_points * self.point_value)
                            
                            # Simulate execution
                            for j in range(i+1, min(i+20, len(self.m5_data))):
                                exec_row = self.m5_data.iloc[j]
                                
                                if exec_row['Low'] <= entry_price:
                                    entry_datetime = exec_row['Datetime']
                                    
                                    for k in range(j+1, len(self.m5_data)):
                                        exit_row = self.m5_data.iloc[k]
                                        
                                        if exit_row['Low'] <= stop_loss:
                                            pnl_points = stop_loss - entry_price
                                            pnl = pnl_points * self.point_value * position_size
                                            capital += pnl
                                            
                                            trades.append({
                                                'entry_time': entry_datetime,
                                                'exit_time': exit_row['Datetime'],
                                                'direction': 'LONG',
                                                'entry_price': entry_price,
                                                'exit_price': stop_loss,
                                                'stop_loss': stop_loss,
                                                'take_profit': take_profit,
                                                'pnl': pnl,
                                                'pnl_points': pnl_points
                                            })
                                            equity_curve.append((exit_row['Datetime'], capital))
                                            break
                                        
                                        if exit_row['High'] >= take_profit:
                                            pnl_points = take_profit - entry_price
                                            pnl = pnl_points * self.point_value * position_size
                                            capital += pnl
                                            
                                            trades.append({
                                                'entry_time': entry_datetime,
                                                'exit_time': exit_row['Datetime'],
                                                'direction': 'LONG',
                                                'entry_price': entry_price,
                                                'exit_price': take_profit,
                                                'stop_loss': stop_loss,
                                                'take_profit': take_profit,
                                                'pnl': pnl,
                                                'pnl_points': pnl_points
                                            })
                                            equity_curve.append((exit_row['Datetime'], capital))
                                            break
                                    break
            
            elif h1_bias == 'bearish' and row['MSS_Bearish'] == 1:
                # Check for FVG confirmation
                if not pd.isna(row['FVG_Bearish_Top']):
                    # Find swing high for stop loss
                    swing_highs = self.m5_data.iloc[max(0, i-20):i]['Swing_High']
                    swing_highs = swing_highs[swing_highs > 0]
                    
                    if len(swing_highs) > 0:
                        swing_high = swing_highs.max()
                        
                        # Entry at FVG proximal (top)
                        entry_price = row['FVG_Bearish_Top']
                        stop_loss = swing_high + 5
                        risk_points = stop_loss - entry_price
                        
                        if risk_points > 0:
                            # Target next major swing low
                            future_swings = self.m5_data.iloc[i:min(i+100, len(self.m5_data))]['Swing_Low']
                            future_swings = future_swings[(future_swings > 0) & (future_swings < entry_price)]
                            
                            if len(future_swings) > 0:
                                take_profit = future_swings.iloc[0]
                            else:
                                take_profit = entry_price - (2 * risk_points)
                            
                            # Position sizing
                            risk_amount = capital * self.risk_per_trade
                            position_size = risk_amount / (risk_points * self.point_value)
                            
                            # Simulate execution
                            for j in range(i+1, min(i+20, len(self.m5_data))):
                                exec_row = self.m5_data.iloc[j]
                                
                                if exec_row['High'] >= entry_price:
                                    entry_datetime = exec_row['Datetime']
                                    
                                    for k in range(j+1, len(self.m5_data)):
                                        exit_row = self.m5_data.iloc[k]
                                        
                                        if exit_row['High'] >= stop_loss:
                                            pnl_points = entry_price - stop_loss
                                            pnl = pnl_points * self.point_value * position_size
                                            capital += pnl
                                            
                                            trades.append({
                                                'entry_time': entry_datetime,
                                                'exit_time': exit_row['Datetime'],
                                                'direction': 'SHORT',
                                                'entry_price': entry_price,
                                                'exit_price': stop_loss,
                                                'stop_loss': stop_loss,
                                                'take_profit': take_profit,
                                                'pnl': pnl,
                                                'pnl_points': pnl_points
                                            })
                                            equity_curve.append((exit_row['Datetime'], capital))
                                            break
                                        
                                        if exit_row['Low'] <= take_profit:
                                            pnl_points = entry_price - take_profit
                                            pnl = pnl_points * self.point_value * position_size
                                            capital += pnl
                                            
                                            trades.append({
                                                'entry_time': entry_datetime,
                                                'exit_time': exit_row['Datetime'],
                                                'direction': 'SHORT',
                                                'entry_price': entry_price,
                                                'exit_price': take_profit,
                                                'stop_loss': stop_loss,
                                                'take_profit': take_profit,
                                                'pnl': pnl,
                                                'pnl_points': pnl_points
                                            })
                                            equity_curve.append((exit_row['Datetime'], capital))
                                            break
                                    break
        
        self.strategy_results['B']['trades'] = trades
        self.strategy_results['B']['equity_curve'] = equity_curve
        
        return trades, equity_curve
    
    def strategy_c_unicorn_model(self):
        """
        Strategy C: The "Unicorn Model" (OB + FVG Confluence)
        
        Setup: Breaker Block (failed OB) overlapping with FVG on M15
        Entry: Market execution when price touches overlap zone
        Stop Loss: Outside Breaker Block range
        Take Profit: 3:1 Risk/Reward
        """
        print("\n=== Running Strategy C: Unicorn Model ===")
        
        capital = self.initial_capital
        trades = []
        equity_curve = [(self.m15_data.iloc[0]['Datetime'], capital)]
        
        for i in range(30, len(self.m15_data)):
            row = self.m15_data.iloc[i]
            
            # Look for Order Block + FVG confluence
            # Bullish setup: Bullish OB overlapping with Bullish FVG
            if not pd.isna(row['OB_Bullish_High']) and not pd.isna(row['FVG_Bullish_Top']):
                ob_low = row['OB_Bullish_Low']
                ob_high = row['OB_Bullish_High']
                fvg_bottom = row['FVG_Bullish_Bottom']
                fvg_top = row['FVG_Bullish_Top']
                
                # Check for overlap
                overlap = (ob_low <= fvg_top) and (ob_high >= fvg_bottom)
                
                if overlap:
                    # Entry at overlap zone center
                    entry_price = (max(ob_low, fvg_bottom) + min(ob_high, fvg_top)) / 2
                    stop_loss = ob_low - 5  # Outside breaker block
                    risk_points = entry_price - stop_loss
                    
                    if risk_points > 0:
                        # 3:1 Risk/Reward
                        take_profit = entry_price + (3 * risk_points)
                        
                        # Position sizing
                        risk_amount = capital * self.risk_per_trade
                        position_size = risk_amount / (risk_points * self.point_value)
                        
                        # Market execution when price touches zone
                        for j in range(i+1, min(i+20, len(self.m15_data))):
                            exec_row = self.m15_data.iloc[j]
                            
                            # Check if price touches overlap zone
                            if exec_row['Low'] <= entry_price <= exec_row['High']:
                                entry_datetime = exec_row['Datetime']
                                
                                for k in range(j+1, len(self.m15_data)):
                                    exit_row = self.m15_data.iloc[k]
                                    
                                    if exit_row['Low'] <= stop_loss:
                                        pnl_points = stop_loss - entry_price
                                        pnl = pnl_points * self.point_value * position_size
                                        capital += pnl
                                        
                                        trades.append({
                                            'entry_time': entry_datetime,
                                            'exit_time': exit_row['Datetime'],
                                            'direction': 'LONG',
                                            'entry_price': entry_price,
                                            'exit_price': stop_loss,
                                            'stop_loss': stop_loss,
                                            'take_profit': take_profit,
                                            'pnl': pnl,
                                            'pnl_points': pnl_points
                                        })
                                        equity_curve.append((exit_row['Datetime'], capital))
                                        break
                                    
                                    if exit_row['High'] >= take_profit:
                                        pnl_points = take_profit - entry_price
                                        pnl = pnl_points * self.point_value * position_size
                                        capital += pnl
                                        
                                        trades.append({
                                            'entry_time': entry_datetime,
                                            'exit_time': exit_row['Datetime'],
                                            'direction': 'LONG',
                                            'entry_price': entry_price,
                                            'exit_price': take_profit,
                                            'stop_loss': stop_loss,
                                            'take_profit': take_profit,
                                            'pnl': pnl,
                                            'pnl_points': pnl_points
                                        })
                                        equity_curve.append((exit_row['Datetime'], capital))
                                        break
                                break
            
            # Bearish setup: Bearish OB overlapping with Bearish FVG
            if not pd.isna(row['OB_Bearish_High']) and not pd.isna(row['FVG_Bearish_Top']):
                ob_low = row['OB_Bearish_Low']
                ob_high = row['OB_Bearish_High']
                fvg_bottom = row['FVG_Bearish_Bottom']
                fvg_top = row['FVG_Bearish_Top']
                
                # Check for overlap
                overlap = (ob_low <= fvg_top) and (ob_high >= fvg_bottom)
                
                if overlap:
                    # Entry at overlap zone center
                    entry_price = (max(ob_low, fvg_bottom) + min(ob_high, fvg_top)) / 2
                    stop_loss = ob_high + 5  # Outside breaker block
                    risk_points = stop_loss - entry_price
                    
                    if risk_points > 0:
                        # 3:1 Risk/Reward
                        take_profit = entry_price - (3 * risk_points)
                        
                        # Position sizing
                        risk_amount = capital * self.risk_per_trade
                        position_size = risk_amount / (risk_points * self.point_value)
                        
                        # Market execution when price touches zone
                        for j in range(i+1, min(i+20, len(self.m15_data))):
                            exec_row = self.m15_data.iloc[j]
                            
                            if exec_row['Low'] <= entry_price <= exec_row['High']:
                                entry_datetime = exec_row['Datetime']
                                
                                for k in range(j+1, len(self.m15_data)):
                                    exit_row = self.m15_data.iloc[k]
                                    
                                    if exit_row['High'] >= stop_loss:
                                        pnl_points = entry_price - stop_loss
                                        pnl = pnl_points * self.point_value * position_size
                                        capital += pnl
                                        
                                        trades.append({
                                            'entry_time': entry_datetime,
                                            'exit_time': exit_row['Datetime'],
                                            'direction': 'SHORT',
                                            'entry_price': entry_price,
                                            'exit_price': stop_loss,
                                            'stop_loss': stop_loss,
                                            'take_profit': take_profit,
                                            'pnl': pnl,
                                            'pnl_points': pnl_points
                                        })
                                        equity_curve.append((exit_row['Datetime'], capital))
                                        break
                                    
                                    if exit_row['Low'] <= take_profit:
                                        pnl_points = entry_price - take_profit
                                        pnl = pnl_points * self.point_value * position_size
                                        capital += pnl
                                        
                                        trades.append({
                                            'entry_time': entry_datetime,
                                            'exit_time': exit_row['Datetime'],
                                            'direction': 'SHORT',
                                            'entry_price': entry_price,
                                            'exit_price': take_profit,
                                            'stop_loss': stop_loss,
                                            'take_profit': take_profit,
                                            'pnl': pnl,
                                            'pnl_points': pnl_points
                                        })
                                        equity_curve.append((exit_row['Datetime'], capital))
                                        break
                                break
        
        self.strategy_results['C']['trades'] = trades
        self.strategy_results['C']['equity_curve'] = equity_curve
        
        return trades, equity_curve
    
    def calculate_metrics(self, trades, equity_curve, strategy_name):
        """
        Calculate performance metrics for a strategy
        
        Returns: dict with metrics
        """
        if len(trades) == 0:
            return {
                'strategy': strategy_name,
                'total_trades': 0,
                'winning_trades': 0,
                'losing_trades': 0,
                'win_rate': 0,
                'total_net_profit': 0,
                'profit_factor': 0,
                'max_drawdown_pct': 0,
                'final_capital': self.initial_capital
            }
        
        df_trades = pd.DataFrame(trades)
        
        winning_trades = df_trades[df_trades['pnl'] > 0]
        losing_trades = df_trades[df_trades['pnl'] < 0]
        
        total_wins = len(winning_trades)
        total_losses = len(losing_trades)
        win_rate = (total_wins / len(trades)) * 100 if len(trades) > 0 else 0
        
        gross_profit = winning_trades['pnl'].sum() if len(winning_trades) > 0 else 0
        gross_loss = abs(losing_trades['pnl'].sum()) if len(losing_trades) > 0 else 0
        
        profit_factor = gross_profit / gross_loss if gross_loss > 0 else 0
        
        total_net_profit = df_trades['pnl'].sum()
        
        # Calculate max drawdown
        equity_values = [eq[1] for eq in equity_curve]
        peak = equity_values[0]
        max_drawdown = 0
        
        for value in equity_values:
            if value > peak:
                peak = value
            drawdown = ((peak - value) / peak) * 100
            if drawdown > max_drawdown:
                max_drawdown = drawdown
        
        final_capital = equity_values[-1]
        
        return {
            'strategy': strategy_name,
            'total_trades': len(trades),
            'winning_trades': total_wins,
            'losing_trades': total_losses,
            'win_rate': win_rate,
            'total_net_profit': total_net_profit,
            'profit_factor': profit_factor,
            'max_drawdown_pct': max_drawdown,
            'final_capital': final_capital
        }
    
    def generate_report(self):
        """
        Phase 3: Generate comparison report for all strategies
        """
        print("\n" + "="*80)
        print("ICT STRATEGIES COMPARISON REPORT")
        print("="*80)
        print(f"\nInitial Capital: ${self.initial_capital:,.2f}")
        print(f"Risk Per Trade: {self.risk_per_trade*100:.1f}%")
        print(f"Point Value: ${self.point_value}")
        print("\n" + "-"*80)
        
        # Calculate metrics for each strategy
        strategy_names = {
            'A': 'Silver Bullet',
            'B': '2022 Mentorship Model',
            'C': 'Unicorn Model'
        }
        
        for key in ['A', 'B', 'C']:
            trades = self.strategy_results[key]['trades']
            equity_curve = self.strategy_results[key]['equity_curve']
            metrics = self.calculate_metrics(trades, equity_curve, strategy_names[key])
            
            print(f"\nStrategy {key}: {metrics['strategy']}")
            print("-" * 80)
            print(f"Total Number of Trades:  {metrics['total_trades']}")
            print(f"Winning Trades:          {metrics['winning_trades']}")
            print(f"Losing Trades:           {metrics['losing_trades']}")
            print(f"Win Rate:                {metrics['win_rate']:.2f}%")
            print(f"Total Net Profit:        ${metrics['total_net_profit']:,.2f}")
            print(f"Profit Factor:           {metrics['profit_factor']:.2f}")
            print(f"Maximum Drawdown:        {metrics['max_drawdown_pct']:.2f}%")
            print(f"Final Capital:           ${metrics['final_capital']:,.2f}")
            print(f"Return:                  {((metrics['final_capital'] - self.initial_capital) / self.initial_capital * 100):.2f}%")
        
        print("\n" + "="*80)
    
    def plot_equity_curves(self, save_path='equity_curves.png'):
        """
        Plot equity curves for all strategies
        """
        fig, axes = plt.subplots(3, 1, figsize=(12, 10))
        
        strategy_names = {
            'A': 'Silver Bullet',
            'B': '2022 Mentorship Model',
            'C': 'Unicorn Model'
        }
        
        for idx, key in enumerate(['A', 'B', 'C']):
            equity_curve = self.strategy_results[key]['equity_curve']
            
            if len(equity_curve) > 0:
                dates = [eq[0] for eq in equity_curve]
                values = [eq[1] for eq in equity_curve]
                
                axes[idx].plot(dates, values, linewidth=2)
                axes[idx].set_title(f"Strategy {key}: {strategy_names[key]}", fontsize=12, fontweight='bold')
                axes[idx].set_ylabel('Equity ($)', fontsize=10)
                axes[idx].grid(True, alpha=0.3)
                axes[idx].axhline(y=self.initial_capital, color='r', linestyle='--', alpha=0.5, label='Initial Capital')
                axes[idx].legend()
        
        axes[2].set_xlabel('Date', fontsize=10)
        plt.tight_layout()
        plt.savefig(save_path, dpi=150)
        print(f"\nEquity curves saved to: {save_path}")


def main(start_year=2023, end_year=2024):
    """
    Main execution function
    
    Args:
        start_year: Starting year for backtest (default: 2023)
        end_year: Ending year for backtest (default: 2024)
    """
    print("="*80)
    print("ICT THREE STRATEGIES BACKTESTING SYSTEM")
    print("="*80)
    print(f"\nLoading NQ Futures Data ({start_year}-{end_year})...")
    
    # Initialize data loader
    loader = DataLoader()
    
    # Load multi-timeframe data
    print("Loading 5-minute data...")
    m5_data = loader.load_data('5m', start_year=start_year, end_year=end_year)
    print(f"  Loaded {len(m5_data):,} candles")
    
    print("Loading 15-minute data...")
    m15_data = loader.load_data('15m', start_year=start_year, end_year=end_year)
    print(f"  Loaded {len(m15_data):,} candles")
    
    print("Loading 1-hour data...")
    h1_data = loader.load_data('1H', start_year=start_year, end_year=end_year)
    print(f"  Loaded {len(h1_data):,} candles")
    
    # Apply ICT features to each timeframe
    print("\nApplying ICT Feature Engineering...")
    
    print("  Processing M5 features...")
    m5_features = ICT_Features(m5_data)
    m5_features.detect_swing_points(window=1) \
               .detect_fvg() \
               .detect_mss(lookback=20) \
               .detect_order_blocks()
    m5_data = m5_features.get_dataframe()
    
    print("  Processing M15 features...")
    m15_features = ICT_Features(m15_data)
    m15_features.detect_swing_points(window=1) \
                .detect_fvg() \
                .detect_mss(lookback=20) \
                .detect_order_blocks()
    m15_data = m15_features.get_dataframe()
    
    print("  Processing H1 features...")
    h1_features = ICT_Features(h1_data)
    h1_features.detect_swing_points(window=1) \
               .detect_fvg() \
               .detect_mss(lookback=20) \
               .detect_order_blocks()
    h1_data = h1_features.get_dataframe()
    
    print("\nInitializing Backtester...")
    backtester = Backtester(
        m5_data=m5_data,
        m15_data=m15_data,
        h1_data=h1_data,
        initial_capital=100000,
        risk_per_trade=0.01
    )
    
    # Run all strategies
    print("\n" + "="*80)
    print("RUNNING BACKTESTS")
    print("="*80)
    
    backtester.strategy_a_silver_bullet()
    backtester.strategy_b_mentorship_model()
    backtester.strategy_c_unicorn_model()
    
    # Generate report
    backtester.generate_report()
    
    # Plot equity curves
    backtester.plot_equity_curves()
    
    print("\n" + "="*80)
    print("BACKTEST COMPLETE")
    print("="*80)


if __name__ == "__main__":
    import sys
    
    # Parse command-line arguments
    if len(sys.argv) >= 3:
        start_year = int(sys.argv[1])
        end_year = int(sys.argv[2])
        print(f"\nRunning backtest from {start_year} to {end_year}...")
        main(start_year, end_year)
    elif len(sys.argv) == 2 and sys.argv[1] in ['--help', '-h']:
        print("Usage: python ict_three_strategies_backtest.py [start_year] [end_year]")
        print("\nExamples:")
        print("  python ict_three_strategies_backtest.py           # Default: 2023-2024")
        print("  python ict_three_strategies_backtest.py 2024 2024 # Single year")
        print("  python ict_three_strategies_backtest.py 2018 2025 # Full dataset")
    else:
        # Default to 2023-2024 for faster testing
        print("\nRunning backtest with default years: 2023-2024")
        print("Use --help to see usage options\n")
        main()

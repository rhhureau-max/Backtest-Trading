"""
ICT Fair Value Gap (FVG) Reversal Strategy Backtest
====================================================

Strategy: ICT FVG Reversal with time-based filtering and hierarchical setup classification
Author: Expert Quant Developer
Date: 2024

TRADING RULES:
-------------
1. TIME CONSTRAINT: Entry window 01:00-04:00, Force close at 06:00
2. SETUP HIERARCHY (confluence-based):
   - Setup C: FVG + MSS (Low Probability)
   - Setup B: Setup C + Liquidity Sweep (Standard)
   - Setup A: Setup B + Displacement + OTE (High Probability)
   - Setup A+: Setup A + Breaker Block + London Macro (Unicorn)

3. MONEY MANAGEMENT:
   - Entry: Limit order at FVG entry level
   - Stop Loss: Swing extreme + 2 points
   - Take Profit: 50% at 2R, 50% at 2.5 SD or force close at 05:00
   - Risk: 1% per trade
"""

import pandas as pd
import numpy as np
from datetime import datetime, time, timedelta
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')


class FVGReversalBacktest:
    """
    Complete ICT FVG Reversal Strategy Backtest with hierarchical setup classification
    """
    
    def __init__(self, capital: float = 100000, risk_per_trade: float = 0.01):
        """
        Initialize backtest parameters
        
        Args:
            capital: Starting capital in USD
            risk_per_trade: Risk percentage per trade (default 1%)
        """
        self.capital = capital
        self.risk_per_trade = risk_per_trade
        self.point_value = 20  # NQ point value in USD
        
        # Configuration
        self.config = {
            'entry_start_time': time(1, 0),     # 01:00
            'entry_end_time': time(4, 0),       # 04:00
            'tp_force_close_time': time(5, 0),  # 05:00
            'all_force_close_time': time(6, 0), # 06:00
            'swing_lookback': 20,               # Minimum bars for swing point
            'displacement_multiplier': 2.0,     # Body must be 2x average
            'displacement_lookback': 10,        # Average of last 10 bars
            'ote_lower': 0.62,                  # OTE lower bound (62%)
            'ote_upper': 0.79,                  # OTE upper bound (79%)
            'sl_buffer': 2.0,                   # Stop loss buffer in points
            'rr_target_1': 2.0,                 # First TP at 2R
            'sd_multiplier': 2.5,               # Second TP at 2.5 SD
            'london_macro_1': (time(2, 33), time(3, 0)),   # London Macro 1
            'london_macro_2': (time(3, 0), time(4, 0)),    # London Macro 2 (Silver Bullet)
        }
        
        # Results storage
        self.trades = []
        
    def load_data(self, timeframe: str, year: int) -> pd.DataFrame:
        """
        Load CSV data for specific timeframe and year
        
        Args:
            timeframe: '5m' or '15m'
            year: Year to load
            
        Returns:
            DataFrame with OHLCV data
        """
        filename = f"/home/runner/work/Backtest-Trading/Backtest-Trading/{year} {timeframe}.csv"
        
        # Load with semicolon separator
        df = pd.read_csv(filename, sep=';')
        
        # Rename columns to standard names
        df.columns = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
        
        # Combine Date and Time into DateTime
        df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%d/%m/%Y %H:%M:%S')
        
        # Set DateTime as index
        df.set_index('DateTime', inplace=True)
        
        # Drop original Date and Time columns
        df.drop(['Date', 'Time'], axis=1, inplace=True)
        
        # Convert to numeric
        for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Sort by index
        df.sort_index(inplace=True)
        
        return df
    
    def detect_fvg(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Detect Fair Value Gaps (FVG) - 3-candle pattern with gap
        
        Bullish FVG: Low[i+1] > High[i-1]
        Bearish FVG: High[i+1] < Low[i-1]
        
        Args:
            df: OHLCV DataFrame
            
        Returns:
            DataFrame with FVG columns added
        """
        df = df.copy()
        
        # Initialize columns
        df['fvg_bullish'] = False
        df['fvg_bearish'] = False
        df['fvg_high'] = np.nan
        df['fvg_low'] = np.nan
        df['fvg_entry'] = np.nan  # Entry level (proximal line)
        
        # Vectorized FVG detection
        for i in range(2, len(df)):
            # Bullish FVG: Gap between candle i-1 high and candle i+1 low
            if df['Low'].iloc[i] > df['High'].iloc[i-2]:
                df.loc[df.index[i], 'fvg_bullish'] = True
                df.loc[df.index[i], 'fvg_low'] = df['High'].iloc[i-2]
                df.loc[df.index[i], 'fvg_high'] = df['Low'].iloc[i]
                # Entry at proximal line (lower boundary for bullish)
                df.loc[df.index[i], 'fvg_entry'] = df['High'].iloc[i-2]
            
            # Bearish FVG: Gap between candle i-1 low and candle i+1 high
            elif df['High'].iloc[i] < df['Low'].iloc[i-2]:
                df.loc[df.index[i], 'fvg_bearish'] = True
                df.loc[df.index[i], 'fvg_high'] = df['Low'].iloc[i-2]
                df.loc[df.index[i], 'fvg_low'] = df['High'].iloc[i]
                # Entry at proximal line (upper boundary for bearish)
                df.loc[df.index[i], 'fvg_entry'] = df['Low'].iloc[i-2]
        
        return df
    
    def detect_swing_points(self, df: pd.DataFrame, lookback: int = 20) -> pd.DataFrame:
        """
        Detect swing highs and lows
        
        Args:
            df: OHLCV DataFrame
            lookback: Minimum bars on each side
            
        Returns:
            DataFrame with swing columns added
        """
        df = df.copy()
        
        df['swing_high'] = False
        df['swing_low'] = False
        df['swing_high_price'] = np.nan
        df['swing_low_price'] = np.nan
        
        for i in range(lookback, len(df) - lookback):
            # Swing High: highest high in window
            window_highs = df['High'].iloc[i-lookback:i+lookback+1]
            if df['High'].iloc[i] == window_highs.max():
                df.loc[df.index[i], 'swing_high'] = True
                df.loc[df.index[i], 'swing_high_price'] = df['High'].iloc[i]
            
            # Swing Low: lowest low in window
            window_lows = df['Low'].iloc[i-lookback:i+lookback+1]
            if df['Low'].iloc[i] == window_lows.min():
                df.loc[df.index[i], 'swing_low'] = True
                df.loc[df.index[i], 'swing_low_price'] = df['Low'].iloc[i]
        
        return df
    
    def detect_mss(self, df: pd.DataFrame, idx: int) -> Tuple[bool, str]:
        """
        Detect Market Structure Shift (MSS) before FVG formation
        
        MSS = Break of structure (BOS) - price breaks recent swing high/low
        
        Args:
            df: OHLCV DataFrame
            idx: Current index to check
            
        Returns:
            (has_mss, direction) - True if MSS detected, 'bullish' or 'bearish'
        """
        if idx < 30:
            return False, ''
        
        # Look back 30 bars for recent structure
        lookback_data = df.iloc[max(0, idx-30):idx]
        
        # For bullish MSS: price should have broken above recent swing high
        if df['fvg_bullish'].iloc[idx]:
            recent_swing_highs = lookback_data[lookback_data['swing_high']]
            if len(recent_swing_highs) > 0:
                last_swing_high = recent_swing_highs['swing_high_price'].iloc[-1]
                # Check if price broke above it
                if df['High'].iloc[idx] > last_swing_high:
                    return True, 'bullish'
        
        # For bearish MSS: price should have broken below recent swing low
        elif df['fvg_bearish'].iloc[idx]:
            recent_swing_lows = lookback_data[lookback_data['swing_low']]
            if len(recent_swing_lows) > 0:
                last_swing_low = recent_swing_lows['swing_low_price'].iloc[-1]
                # Check if price broke below it
                if df['Low'].iloc[idx] < last_swing_low:
                    return True, 'bearish'
        
        return False, ''
    
    def detect_liquidity_sweep(self, df: pd.DataFrame, idx: int, direction: str) -> bool:
        """
        Detect Liquidity Sweep (Turtle Soup)
        
        Price should have swept a swing high/low that's at least 20 bars old
        before the FVG formation
        
        Args:
            df: OHLCV DataFrame
            idx: Current index
            direction: 'bullish' or 'bearish'
            
        Returns:
            True if liquidity sweep detected
        """
        lookback = self.config['swing_lookback']
        
        if idx < lookback + 10:
            return False
        
        # Get data before FVG formation (at least 5 bars before)
        lookback_data = df.iloc[max(0, idx-50):idx-5]
        
        if direction == 'bullish':
            # For bullish: should have swept a swing low
            swing_lows = lookback_data[lookback_data['swing_low']]
            if len(swing_lows) > 0:
                target_low = swing_lows['swing_low_price'].iloc[-1]
                # Check if price swept below it in recent bars
                recent_bars = df.iloc[max(0, idx-10):idx]
                if recent_bars['Low'].min() <= target_low:
                    return True
        
        elif direction == 'bearish':
            # For bearish: should have swept a swing high
            swing_highs = lookback_data[lookback_data['swing_high']]
            if len(swing_highs) > 0:
                target_high = swing_highs['swing_high_price'].iloc[-1]
                # Check if price swept above it in recent bars
                recent_bars = df.iloc[max(0, idx-10):idx]
                if recent_bars['High'].max() >= target_high:
                    return True
        
        return False
    
    def check_displacement(self, df: pd.DataFrame, idx: int) -> bool:
        """
        Check if the FVG-creating candle shows strong displacement
        
        Body must be > 2x average body size of last 10 candles
        
        Args:
            df: OHLCV DataFrame
            idx: Current index (FVG candle)
            
        Returns:
            True if displacement criteria met
        """
        lookback = self.config['displacement_lookback']
        
        if idx < lookback + 2:
            return False
        
        # Calculate body sizes for last 10 candles (before current)
        recent_data = df.iloc[idx-lookback-2:idx-2]
        avg_body = abs(recent_data['Close'] - recent_data['Open']).mean()
        
        # Body of the candle that created the FVG (candle at idx-1)
        fvg_candle_body = abs(df['Close'].iloc[idx-1] - df['Open'].iloc[idx-1])
        
        # Check if displacement is strong enough
        if fvg_candle_body > (self.config['displacement_multiplier'] * avg_body):
            return True
        
        return False
    
    def check_ote_zone(self, df: pd.DataFrame, idx: int, direction: str) -> bool:
        """
        Check if entry is in Optimal Trade Entry (OTE) zone
        
        OTE = 62% to 79% retracement of the manipulation range
        
        Args:
            df: OHLCV DataFrame
            idx: Current index
            direction: 'bullish' or 'bearish'
            
        Returns:
            True if in OTE zone
        """
        if idx < 30:
            return False
        
        # Define manipulation range (last 20 bars)
        range_data = df.iloc[max(0, idx-20):idx]
        range_high = range_data['High'].max()
        range_low = range_data['Low'].min()
        range_size = range_high - range_low
        
        if range_size == 0:
            return False
        
        # Get current entry price
        entry_price = df['fvg_entry'].iloc[idx]
        
        if direction == 'bullish':
            # For bullish: entry should be in lower part of range (discount)
            # 62-79% from high = 21-38% from low
            retracement_from_low = (entry_price - range_low) / range_size
            if 0.21 <= retracement_from_low <= 0.38:
                return True
        
        elif direction == 'bearish':
            # For bearish: entry should be in upper part of range (premium)
            # 62-79% from low = 79-62% from high
            retracement_from_high = (range_high - entry_price) / range_size
            if 0.21 <= retracement_from_high <= 0.38:
                return True
        
        return False
    
    def detect_breaker_block(self, df: pd.DataFrame, idx: int, direction: str) -> bool:
        """
        Detect Breaker Block confluence
        
        Breaker Block = Old demand zone that became supply (or vice versa)
        Check if FVG overlaps with a previous broken structure
        
        Args:
            df: OHLCV DataFrame
            idx: Current index
            direction: 'bullish' or 'bearish'
            
        Returns:
            True if breaker block confluence exists
        """
        if idx < 50:
            return False
        
        fvg_low = df['fvg_low'].iloc[idx]
        fvg_high = df['fvg_high'].iloc[idx]
        
        # Look for previous structure breaks in last 50 bars
        lookback_data = df.iloc[max(0, idx-50):idx-10]
        
        if direction == 'bullish':
            # For bullish: look for old resistance that was broken (now support)
            # Find previous swing highs
            prev_swing_highs = lookback_data[lookback_data['swing_high']]
            for i, row in prev_swing_highs.iterrows():
                swing_price = row['swing_high_price']
                # Check if this swing was broken (price went above it)
                if swing_price is not None and not pd.isna(swing_price):
                    # Check if FVG overlaps with this level
                    if fvg_low <= swing_price <= fvg_high:
                        return True
        
        elif direction == 'bearish':
            # For bearish: look for old support that was broken (now resistance)
            # Find previous swing lows
            prev_swing_lows = lookback_data[lookback_data['swing_low']]
            for i, row in prev_swing_lows.iterrows():
                swing_price = row['swing_low_price']
                # Check if this swing was broken (price went below it)
                if swing_price is not None and not pd.isna(swing_price):
                    # Check if FVG overlaps with this level
                    if fvg_low <= swing_price <= fvg_high:
                        return True
        
        return False
    
    def check_london_macro_timing(self, timestamp: datetime) -> bool:
        """
        Check if entry is during London Macro windows
        
        Macro 1: 02:33 - 03:00
        Macro 2 (Silver Bullet): 03:00 - 04:00
        
        Args:
            timestamp: Entry timestamp
            
        Returns:
            True if during macro window
        """
        entry_time = timestamp.time()
        
        # London Macro 1
        macro1_start, macro1_end = self.config['london_macro_1']
        if macro1_start <= entry_time < macro1_end:
            return True
        
        # London Macro 2 (Silver Bullet)
        macro2_start, macro2_end = self.config['london_macro_2']
        if macro2_start <= entry_time < macro2_end:
            return True
        
        return False
    
    def classify_setup(self, df: pd.DataFrame, idx: int, direction: str) -> str:
        """
        Classify setup into hierarchy: C, B, A, or A+
        
        Setup C: FVG + MSS
        Setup B: Setup C + Liquidity Sweep
        Setup A: Setup B + Displacement + OTE
        Setup A+: Setup A + Breaker Block + London Macro
        
        Args:
            df: OHLCV DataFrame
            idx: Current index
            direction: 'bullish' or 'bearish'
            
        Returns:
            Setup classification: 'C', 'B', 'A', or 'A+'
        """
        # Base requirement: FVG + MSS
        has_mss, _ = self.detect_mss(df, idx)
        if not has_mss:
            return None
        
        # Setup C achieved
        setup_level = 'C'
        
        # Check for Setup B: + Liquidity Sweep
        has_liquidity_sweep = self.detect_liquidity_sweep(df, idx, direction)
        if has_liquidity_sweep:
            setup_level = 'B'
            
            # Check for Setup A: + Displacement + OTE
            has_displacement = self.check_displacement(df, idx)
            has_ote = self.check_ote_zone(df, idx, direction)
            
            if has_displacement and has_ote:
                setup_level = 'A'
                
                # Check for Setup A+: + Breaker Block + London Macro
                has_breaker = self.detect_breaker_block(df, idx, direction)
                timestamp = df.index[idx]
                is_macro_time = self.check_london_macro_timing(timestamp)
                
                if has_breaker and is_macro_time:
                    setup_level = 'A+'
        
        return setup_level
    
    def calculate_position_size(self, stop_loss_points: float) -> float:
        """
        Calculate position size based on risk percentage
        
        Args:
            stop_loss_points: Stop loss distance in points
            
        Returns:
            Number of contracts
        """
        risk_amount = self.capital * self.risk_per_trade
        risk_per_contract = stop_loss_points * self.point_value
        
        if risk_per_contract <= 0:
            return 0
        
        position_size = risk_amount / risk_per_contract
        return max(1, int(position_size))  # At least 1 contract
    
    def simulate_trade(self, df: pd.DataFrame, entry_idx: int, setup_class: str, direction: str) -> Dict:
        """
        Simulate trade execution and management
        
        Args:
            df: OHLCV DataFrame
            entry_idx: Entry bar index
            setup_class: Setup classification (C, B, A, A+)
            direction: 'bullish' or 'bearish'
            
        Returns:
            Trade result dictionary
        """
        entry_price = df['fvg_entry'].iloc[entry_idx]
        entry_time = df.index[entry_idx]
        
        # Calculate stop loss
        if direction == 'bullish':
            # Find recent swing low
            lookback_data = df.iloc[max(0, entry_idx-30):entry_idx]
            swing_lows = lookback_data[lookback_data['swing_low']]
            if len(swing_lows) > 0:
                swing_extreme = swing_lows['swing_low_price'].iloc[-1]
            else:
                swing_extreme = lookback_data['Low'].min()
            stop_loss = swing_extreme - self.config['sl_buffer']
        else:
            # Find recent swing high
            lookback_data = df.iloc[max(0, entry_idx-30):entry_idx]
            swing_highs = lookback_data[lookback_data['swing_high']]
            if len(swing_highs) > 0:
                swing_extreme = swing_highs['swing_high_price'].iloc[-1]
            else:
                swing_extreme = lookback_data['High'].max()
            stop_loss = swing_extreme + self.config['sl_buffer']
        
        # Calculate risk and position size
        stop_loss_points = abs(entry_price - stop_loss)
        position_size = self.calculate_position_size(stop_loss_points)
        
        # Calculate take profit levels
        risk_points = stop_loss_points
        
        if direction == 'bullish':
            tp1 = entry_price + (risk_points * self.config['rr_target_1'])
            # For TP2, use 2.5 SD of range
            range_data = df.iloc[max(0, entry_idx-20):entry_idx]
            range_sd = range_data['Close'].std()
            tp2 = entry_price + (range_sd * self.config['sd_multiplier'])
        else:
            tp1 = entry_price - (risk_points * self.config['rr_target_1'])
            range_data = df.iloc[max(0, entry_idx-20):entry_idx]
            range_sd = range_data['Close'].std()
            tp2 = entry_price - (range_sd * self.config['sd_multiplier'])
        
        # Simulate trade management
        position_1_active = True  # 50% position
        position_2_active = True  # 50% position
        
        exit_reason = None
        exit_price_1 = None
        exit_price_2 = None
        exit_time_1 = None
        exit_time_2 = None
        
        # Determine end of scanning window (must close by 06:00 same day)
        entry_date = entry_time.date()
        
        # Scan forward bars for exit conditions (limited to same trading day)
        for i in range(entry_idx + 1, min(entry_idx + 200, len(df))):  # Max 200 bars forward (10 hours on 5m)
            current_bar = df.iloc[i]
            current_time = df.index[i]
            current_time_only = current_time.time()
            current_date = current_time.date()
            
            # Check force close at 06:00 (must be on same date or next if entry is after midnight)
            # Since entry window is 01:00-04:00, close at 06:00 same day
            if current_date == entry_date and current_time_only >= self.config['all_force_close_time']:
                if position_1_active:
                    exit_price_1 = current_bar['Open']
                    exit_time_1 = current_time
                    position_1_active = False
                if position_2_active:
                    exit_price_2 = current_bar['Open']
                    exit_time_2 = current_time
                    position_2_active = False
                exit_reason = 'Force Close 06:00'
                break
            
            # Also force close if we're on the next day (safety check)
            if current_date > entry_date:
                if position_1_active:
                    exit_price_1 = current_bar['Open']
                    exit_time_1 = current_time
                    position_1_active = False
                if position_2_active:
                    exit_price_2 = current_bar['Open']
                    exit_time_2 = current_time
                    position_2_active = False
                exit_reason = 'Force Close Next Day'
                break
            
            # Check TP2 force close at 05:00 (same day only, before 06:00 force close)
            if current_date == entry_date and current_time_only >= self.config['tp_force_close_time']:
                # Close position 2 at 05:00 if still active
                if position_2_active:
                    exit_price_2 = current_bar['Open']
                    exit_time_2 = current_time
                    position_2_active = False
                # If position 1 is also still active after 06:00, close it too
                if current_time_only >= self.config['all_force_close_time'] and position_1_active:
                    exit_price_1 = current_bar['Open']
                    exit_time_1 = current_time
                    position_1_active = False
                    exit_reason = 'Force Close 06:00'
                    break
            
            
            # Check stop loss
            if direction == 'bullish':
                if current_bar['Low'] <= stop_loss:
                    if position_1_active:
                        exit_price_1 = stop_loss
                        exit_time_1 = current_time
                        position_1_active = False
                    if position_2_active:
                        exit_price_2 = stop_loss
                        exit_time_2 = current_time
                        position_2_active = False
                    exit_reason = 'Stop Loss'
                    break
            else:
                if current_bar['High'] >= stop_loss:
                    if position_1_active:
                        exit_price_1 = stop_loss
                        exit_time_1 = current_time
                        position_1_active = False
                    if position_2_active:
                        exit_price_2 = stop_loss
                        exit_time_2 = current_time
                        position_2_active = False
                    exit_reason = 'Stop Loss'
                    break
            
            # Check TP1 (50% position)
            if position_1_active:
                if direction == 'bullish' and current_bar['High'] >= tp1:
                    exit_price_1 = tp1
                    exit_time_1 = current_time
                    position_1_active = False
                    if exit_reason is None:
                        exit_reason = 'Partial TP1'
                elif direction == 'bearish' and current_bar['Low'] <= tp1:
                    exit_price_1 = tp1
                    exit_time_1 = current_time
                    position_1_active = False
                    if exit_reason is None:
                        exit_reason = 'Partial TP1'
            
            # Check TP2 (50% position)
            if position_2_active and not position_1_active:  # Only after TP1 hit
                if direction == 'bullish' and current_bar['High'] >= tp2:
                    exit_price_2 = tp2
                    exit_time_2 = current_time
                    position_2_active = False
                    exit_reason = 'Full TP2'
                    break
                elif direction == 'bearish' and current_bar['Low'] <= tp2:
                    exit_price_2 = tp2
                    exit_time_2 = current_time
                    position_2_active = False
                    exit_reason = 'Full TP2'
                    break
        
        # If still open at end of data
        if position_1_active or position_2_active:
            last_bar = df.iloc[-1]
            if position_1_active:
                exit_price_1 = last_bar['Close']
                exit_time_1 = df.index[-1]
            if position_2_active:
                exit_price_2 = last_bar['Close']
                exit_time_2 = df.index[-1]
            if exit_reason is None:
                exit_reason = 'End of Data'
        
        # Calculate P&L
        pnl_1 = 0
        pnl_2 = 0
        
        if exit_price_1 is not None:
            if direction == 'bullish':
                pnl_1 = (exit_price_1 - entry_price) * (position_size / 2) * self.point_value
            else:
                pnl_1 = (entry_price - exit_price_1) * (position_size / 2) * self.point_value
        
        if exit_price_2 is not None:
            if direction == 'bullish':
                pnl_2 = (exit_price_2 - entry_price) * (position_size / 2) * self.point_value
            else:
                pnl_2 = (entry_price - exit_price_2) * (position_size / 2) * self.point_value
        
        total_pnl = pnl_1 + pnl_2
        
        # Calculate R-multiple
        risk_amount = stop_loss_points * position_size * self.point_value
        r_multiple = total_pnl / risk_amount if risk_amount > 0 else 0
        
        return {
            'entry_time': entry_time,
            'entry_price': entry_price,
            'direction': direction,
            'setup_class': setup_class,
            'position_size': position_size,
            'stop_loss': stop_loss,
            'tp1': tp1,
            'tp2': tp2,
            'exit_price_1': exit_price_1,
            'exit_price_2': exit_price_2,
            'exit_time_1': exit_time_1,
            'exit_time_2': exit_time_2,
            'exit_reason': exit_reason,
            'pnl': total_pnl,
            'r_multiple': r_multiple,
            'winner': total_pnl > 0
        }
    
    def run_backtest(self, years: List[int] = [2024]) -> pd.DataFrame:
        """
        Run complete backtest across specified years
        
        Args:
            years: List of years to backtest
            
        Returns:
            DataFrame with all trades
        """
        print("="*80)
        print("ICT FVG REVERSAL STRATEGY BACKTEST")
        print("="*80)
        print(f"Capital: ${self.capital:,.2f}")
        print(f"Risk per trade: {self.risk_per_trade*100}%")
        print(f"Time window: {self.config['entry_start_time']} - {self.config['entry_end_time']}")
        print(f"Force close: {self.config['all_force_close_time']}")
        print("="*80)
        
        all_trades = []
        
        for year in years:
            print(f"\nProcessing year {year}...")
            
            # Load both timeframes
            df_5m = self.load_data('5m', year)
            df_15m = self.load_data('15m', year)
            
            print(f"  Loaded {len(df_5m)} bars (5m), {len(df_15m)} bars (15m)")
            
            # Detect features on 15m (structure) and 5m (entry)
            print("  Detecting swing points and structure...")
            df_15m = self.detect_swing_points(df_15m, self.config['swing_lookback'])
            df_5m = self.detect_swing_points(df_5m, self.config['swing_lookback'])
            
            # Detect FVGs on both timeframes
            print("  Detecting Fair Value Gaps...")
            df_15m = self.detect_fvg(df_15m)
            df_5m = self.detect_fvg(df_5m)
            
            # Scan for setups on 15m
            print("  Scanning for setups...")
            setup_count = {'C': 0, 'B': 0, 'A': 0, 'A+': 0}
            
            for i in range(50, len(df_15m)):
                row = df_15m.iloc[i]
                timestamp = df_15m.index[i]
                time_only = timestamp.time()
                
                # Check time window (01:00 - 04:00)
                if not (self.config['entry_start_time'] <= time_only < self.config['entry_end_time']):
                    continue
                
                # Check if FVG exists
                if row['fvg_bullish']:
                    direction = 'bullish'
                elif row['fvg_bearish']:
                    direction = 'bearish'
                else:
                    continue
                
                # Classify setup
                setup_class = self.classify_setup(df_15m, i, direction)
                
                if setup_class is not None:
                    setup_count[setup_class] += 1
                    
                    # Simulate trade
                    trade = self.simulate_trade(df_15m, i, setup_class, direction)
                    all_trades.append(trade)
            
            print(f"  Setups found: C={setup_count['C']}, B={setup_count['B']}, A={setup_count['A']}, A+={setup_count['A+']}")
        
        # Convert to DataFrame
        if len(all_trades) > 0:
            self.trades = pd.DataFrame(all_trades)
            print(f"\nTotal trades: {len(self.trades)}")
        else:
            print("\nNo trades found!")
            self.trades = pd.DataFrame()
        
        return self.trades
    
    def generate_results(self) -> pd.DataFrame:
        """
        Generate comparative results for each setup class
        
        Returns:
            DataFrame with metrics per setup class
        """
        if len(self.trades) == 0:
            print("No trades to analyze!")
            return pd.DataFrame()
        
        results = []
        
        for setup_class in ['C', 'B', 'A', 'A+']:
            class_trades = self.trades[self.trades['setup_class'] == setup_class]
            
            if len(class_trades) == 0:
                results.append({
                    'Setup Class': setup_class,
                    'Num Trades': 0,
                    'Winrate (%)': 0,
                    'Profit Factor': 0,
                    'Max Drawdown ($)': 0,
                    'Net Profit ($)': 0,
                    'Avg R-Multiple': 0
                })
                continue
            
            # Calculate metrics
            num_trades = len(class_trades)
            winners = class_trades[class_trades['winner']]
            losers = class_trades[~class_trades['winner']]
            
            winrate = (len(winners) / num_trades) * 100 if num_trades > 0 else 0
            
            gross_profit = winners['pnl'].sum() if len(winners) > 0 else 0
            gross_loss = abs(losers['pnl'].sum()) if len(losers) > 0 else 0
            profit_factor = gross_profit / gross_loss if gross_loss > 0 else 0
            
            net_profit = class_trades['pnl'].sum()
            
            # Calculate drawdown
            cumulative_pnl = class_trades['pnl'].cumsum()
            running_max = cumulative_pnl.cummax()
            drawdown = running_max - cumulative_pnl
            max_drawdown = drawdown.max()
            
            avg_r = class_trades['r_multiple'].mean()
            
            results.append({
                'Setup Class': setup_class,
                'Num Trades': num_trades,
                'Winrate (%)': round(winrate, 2),
                'Profit Factor': round(profit_factor, 2),
                'Max Drawdown ($)': round(max_drawdown, 2),
                'Net Profit ($)': round(net_profit, 2),
                'Avg R-Multiple': round(avg_r, 2)
            })
        
        results_df = pd.DataFrame(results)
        
        print("\n" + "="*80)
        print("RESULTS BY SETUP CLASS")
        print("="*80)
        print(results_df.to_string(index=False))
        print("="*80)
        
        return results_df


def main():
    """
    Main execution function
    """
    # Initialize backtest
    backtest = FVGReversalBacktest(capital=100000, risk_per_trade=0.01)
    
    # Run backtest for 2024
    trades = backtest.run_backtest(years=[2024])
    
    # Generate results
    results = backtest.generate_results()
    
    # Save results
    if len(trades) > 0:
        trades.to_csv('/home/runner/work/Backtest-Trading/Backtest-Trading/fvg_reversal_trades.csv', index=False)
        print("\nTrades saved to: fvg_reversal_trades.csv")
    
    if len(results) > 0:
        results.to_csv('/home/runner/work/Backtest-Trading/Backtest-Trading/fvg_reversal_results.csv', index=False)
        print("Results saved to: fvg_reversal_results.csv")
    
    return backtest, trades, results


if __name__ == "__main__":
    backtest, trades, results = main()

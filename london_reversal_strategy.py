#!/usr/bin/env python3
"""
London Reversal Strategy - ICT Accumulation, Manipulation, Distribution Model
==============================================================================

This script implements a complete backtesting strategy for the "London Reversal" setup
based on the AMD (Accumulation, Manipulation, Distribution) model.

Strategy Phases:
1. Asian Range (Tokyo Session): 19:00-00:00 (previous day) - Accumulation
2. Judas Swing (London Open): 02:00-03:00 - Manipulation (liquidity sweep)
3. Reversal Signal: Hammer/Shooting Star - Distribution beginning
4. Inversion FVG Trigger: Entry signal

Author: ICT Trading Strategy Implementation
Date: 2024
"""

import pandas as pd
import numpy as np
from datetime import datetime, time, timedelta
from typing import Tuple, Dict, List, Optional
import warnings
warnings.filterwarnings('ignore')


class LondonReversalStrategy:
    """
    Implements the London Reversal strategy with comprehensive analysis.
    """
    
    def __init__(self, data_5m_path: str, data_1h_path: str):
        """
        Initialize the strategy with 5-minute and 1-hour data.
        
        Args:
            data_5m_path: Path to 5-minute CSV data file
            data_1h_path: Path to 1-hour CSV data file
        """
        self.data_5m = self._load_data(data_5m_path, '5T')
        self.data_1h = self._load_data(data_1h_path, '1H')
        
        # Strategy parameters
        self.asian_start = time(19, 0)  # 19:00
        self.asian_end = time(23, 59)   # 23:59
        self.judas_start = time(2, 0)   # 02:00 London open
        self.judas_end = time(3, 0)     # 03:00
        
        # Trade tracking
        self.trades = []
        self.setups_analyzed = []
        
    def _load_data(self, filepath: str, freq: str) -> pd.DataFrame:
        """
        Load and prepare CSV data with proper datetime handling.
        
        Args:
            filepath: Path to CSV file
            freq: Frequency for resampling if needed
            
        Returns:
            DataFrame with datetime index and OHLCV data
        """
        # Load CSV with semicolon delimiter
        df = pd.read_csv(filepath, sep=';')
        
        # Combine date and time columns
        df['datetime'] = pd.to_datetime(
            df['Column1'] + ' ' + df['Column2'],
            format='%d/%m/%Y %H:%M:%S'
        )
        
        # Rename columns
        df = df.rename(columns={
            'Column3': 'Open',
            'Column4': 'High',
            'Column5': 'Low',
            'Column6': 'Close',
            'Column7': 'Volume'
        })
        
        # Set datetime as index
        df = df.set_index('datetime')
        df = df[['Open', 'High', 'Low', 'Close', 'Volume']]
        
        # Sort by index
        df = df.sort_index()
        
        return df
    
    def identify_asian_range(self, date: pd.Timestamp) -> Optional[Dict]:
        """
        Identify Asian session range for a given date.
        
        Phase 1: Asian Range (Tokyo Session)
        - Session: 19:00 to 00:00 (previous day, n-1)
        - Identify range with Buy-Side Liquidity (high) and Sell-Side Liquidity (low)
        
        Args:
            date: Date to analyze (will look at previous day's session)
            
        Returns:
            Dictionary with asian_high, asian_low, buy_side_liquidity, sell_side_liquidity
            or None if insufficient data
        """
        # Asian session is on the previous day
        prev_day = date - timedelta(days=1)
        
        # Get Asian session data (19:00 previous day to 23:59)
        asian_start_dt = pd.Timestamp.combine(prev_day.date(), self.asian_start)
        asian_end_dt = pd.Timestamp.combine(prev_day.date(), self.asian_end)
        
        asian_data = self.data_5m[
            (self.data_5m.index >= asian_start_dt) & 
            (self.data_5m.index <= asian_end_dt)
        ]
        
        if len(asian_data) < 12:  # Need at least 1 hour of data
            return None
        
        asian_high = asian_data['High'].max()
        asian_low = asian_data['Low'].min()
        
        # Buy-Side Liquidity = Asian High (stops above)
        # Sell-Side Liquidity = Asian Low (stops below)
        range_size = asian_high - asian_low
        
        if range_size < 3:  # Range too small (less than 3 points)
            return None
        
        return {
            'asian_high': asian_high,
            'asian_low': asian_low,
            'buy_side_liquidity': asian_high,
            'sell_side_liquidity': asian_low,
            'range_size': range_size,
            'start_time': asian_start_dt,
            'end_time': asian_end_dt
        }
    
    def detect_fvg(self, df: pd.DataFrame, index: int) -> Optional[Dict]:
        """
        Detect Fair Value Gap (FVG) at given index.
        
        FVG Detection:
        - Bullish FVG: Low[i] > High[i-2] (gap up)
        - Bearish FVG: High[i] < Low[i-2] (gap down)
        
        Args:
            df: DataFrame with OHLC data
            index: Index to check for FVG
            
        Returns:
            Dictionary with FVG details or None
        """
        if index < 2:
            return None
        
        # Get the three candles
        current = df.iloc[index]
        prev1 = df.iloc[index - 1]
        prev2 = df.iloc[index - 2]
        
        # Bullish FVG: Low[i] > High[i-2]
        if current['Low'] > prev2['High']:
            return {
                'type': 'bullish',
                'top': current['Low'],
                'bottom': prev2['High'],
                'size': current['Low'] - prev2['High'],
                'time': df.index[index],
                'index': index
            }
        
        # Bearish FVG: High[i] < Low[i-2]
        if current['High'] < prev2['Low']:
            return {
                'type': 'bearish',
                'top': prev2['Low'],
                'bottom': current['High'],
                'size': prev2['Low'] - current['High'],
                'time': df.index[index],
                'index': index
            }
        
        return None
    
    def detect_liquidity_sweep(self, asian_range: Dict, judas_data: pd.DataFrame) -> Optional[Dict]:
        """
        Detect liquidity sweep during Judas Swing (London manipulation).
        
        Phase 2: Judas Swing (London Open Manipulation)
        - Time: 02:00 to 03:00
        - Aggressive move that sweeps Tokyo session extreme
        - Creates FVG M5 in the direction of movement
        
        Args:
            asian_range: Asian session range data
            judas_data: DataFrame for Judas period (02:00-03:00)
            
        Returns:
            Dictionary with sweep details or None
        """
        if len(judas_data) < 3:
            return None
        
        judas_high = judas_data['High'].max()
        judas_low = judas_data['Low'].min()
        
        asian_high = asian_range['asian_high']
        asian_low = asian_range['asian_low']
        
        # Check for sweep of buy-side liquidity (sweep above Asian high)
        if judas_high > asian_high:
            sweep_type = 'buy_side_sweep'
            sweep_extreme = judas_high
            expected_direction = 'bearish'  # Expect reversal down
            
        # Check for sweep of sell-side liquidity (sweep below Asian low)
        elif judas_low < asian_low:
            sweep_type = 'sell_side_sweep'
            sweep_extreme = judas_low
            expected_direction = 'bullish'  # Expect reversal up
        else:
            return None
        
        # Find FVGs created during the sweep
        fvgs_created = []
        for i in range(2, len(judas_data)):
            fvg = self.detect_fvg(judas_data.reset_index(drop=False), i)
            if fvg and fvg['type'] == expected_direction:
                fvgs_created.append(fvg)
        
        if not fvgs_created:
            return None
        
        # Use the largest FVG created during manipulation
        largest_fvg = max(fvgs_created, key=lambda x: x['size'])
        
        return {
            'sweep_type': sweep_type,
            'sweep_extreme': sweep_extreme,
            'direction': expected_direction,
            'fvg_created': largest_fvg,
            'judas_high': judas_high,
            'judas_low': judas_low
        }
    
    def get_htf_levels(self, date: pd.Timestamp, price: float, direction: str) -> Dict:
        """
        Get Higher Time Frame (HTF) levels for confluence.
        
        Checks if the sweep price tests H1 Order Block or H4 Support/Resistance.
        
        Args:
            date: Current date
            price: Price level to check
            direction: 'bullish' or 'bearish'
            
        Returns:
            Dictionary with HTF confluence information
        """
        # Get H1 data around the time period
        lookback_start = date - timedelta(days=7)
        h1_data = self.data_1h[
            (self.data_1h.index >= lookback_start) & 
            (self.data_1h.index <= date)
        ]
        
        if len(h1_data) < 10:
            return {'has_confluence': False, 'distance': None}
        
        # Identify recent H1 swing highs and lows
        window = 5
        h1_data_copy = h1_data.copy()
        
        # Find swing highs (local maxima)
        h1_data_copy['swing_high'] = h1_data_copy['High'].rolling(
            window=window*2+1, center=True
        ).apply(lambda x: 1 if x[window] == max(x) else 0, raw=True)
        
        # Find swing lows (local minima)
        h1_data_copy['swing_low'] = h1_data_copy['Low'].rolling(
            window=window*2+1, center=True
        ).apply(lambda x: 1 if x[window] == min(x) else 0, raw=True)
        
        swing_highs = h1_data_copy[h1_data_copy['swing_high'] == 1]['High'].values
        swing_lows = h1_data_copy[h1_data_copy['swing_low'] == 1]['Low'].values
        
        # Check proximity to HTF levels (within 15 points)
        tolerance = 15
        
        if direction == 'bearish':
            # Look for resistance levels near the sweep high
            for level in swing_highs:
                if abs(price - level) <= tolerance:
                    return {
                        'has_confluence': True,
                        'level': level,
                        'distance': abs(price - level),
                        'type': 'H1_resistance'
                    }
        else:  # bullish
            # Look for support levels near the sweep low
            for level in swing_lows:
                if abs(price - level) <= tolerance:
                    return {
                        'has_confluence': True,
                        'level': level,
                        'distance': abs(price - level),
                        'type': 'H1_support'
                    }
        
        return {'has_confluence': False, 'distance': None}
    
    def detect_reversal_candle(self, df: pd.DataFrame, direction: str) -> Optional[Dict]:
        """
        Detect reversal candle pattern (Hammer or Shooting Star).
        
        Phase 3: Reversal Signal
        - Hammer (after drop): Long lower wick, small body at top
        - Shooting Star (after rally): Long upper wick, small body at bottom
        
        Args:
            df: DataFrame with OHLC data
            direction: Expected reversal direction ('bullish' or 'bearish')
            
        Returns:
            Dictionary with reversal candle details or None
        """
        if len(df) == 0:
            return None
        
        for i in range(len(df) - 1, max(len(df) - 10, -1), -1):
            candle = df.iloc[i]
            
            body_size = abs(candle['Close'] - candle['Open'])
            total_range = candle['High'] - candle['Low']
            
            if total_range < 1.5:  # Too small
                continue
            
            if direction == 'bullish':
                # Look for Hammer pattern
                lower_wick = min(candle['Open'], candle['Close']) - candle['Low']
                upper_wick = candle['High'] - max(candle['Open'], candle['Close'])
                
                # Hammer: lower wick >= 1.5x body, upper wick small
                if (lower_wick >= 1.5 * body_size and 
                    upper_wick < body_size * 1.5 and
                    lower_wick > 2):
                    return {
                        'type': 'hammer',
                        'time': df.index[i],
                        'index': i,
                        'high': candle['High'],
                        'low': candle['Low'],
                        'close': candle['Close'],
                        'open': candle['Open'],
                        'lower_wick': lower_wick
                    }
            
            elif direction == 'bearish':
                # Look for Shooting Star pattern
                upper_wick = candle['High'] - max(candle['Open'], candle['Close'])
                lower_wick = min(candle['Open'], candle['Close']) - candle['Low']
                
                # Shooting Star: upper wick >= 1.5x body, lower wick small
                if (upper_wick >= 1.5 * body_size and 
                    lower_wick < body_size * 1.5 and
                    upper_wick > 2):
                    return {
                        'type': 'shooting_star',
                        'time': df.index[i],
                        'index': i,
                        'high': candle['High'],
                        'low': candle['Low'],
                        'close': candle['Close'],
                        'open': candle['Open'],
                        'upper_wick': upper_wick
                    }
        
        return None
    
    def detect_fvg_inversion(self, df: pd.DataFrame, fvg: Dict, 
                            direction: str, start_index: int) -> Optional[Dict]:
        """
        Detect FVG inversion (entry trigger).
        
        Phase 4: Inversion FVG Trigger
        - Price reverses with displacement
        - M5 candle completely fills and closes decisively beyond the FVG
        - FVG becomes "Inversion FVG" (inverted support/resistance)
        
        Args:
            df: DataFrame with OHLC data
            fvg: FVG created during manipulation
            direction: Expected reversal direction
            start_index: Start looking from this index
            
        Returns:
            Dictionary with inversion details or None
        """
        for i in range(start_index, len(df)):
            candle = df.iloc[i]
            
            if direction == 'bullish':
                # Bullish inversion: Price comes back down, fills bearish FVG, closes above
                # FVG top = prev2['Low'], FVG bottom = current['High']
                fvg_top = fvg['top']
                fvg_bottom = fvg['bottom']
                
                # Check if candle closes decisively above FVG
                if (candle['Low'] <= fvg_bottom and 
                    candle['Close'] > fvg_top):
                    
                    # Check for displacement (strong bullish candle)
                    body_size = candle['Close'] - candle['Open']
                    if body_size > 2:  # Displacement threshold
                        # Get actual timestamp if df has datetime column
                        if 'datetime' in df.columns:
                            entry_timestamp = df.iloc[i]['datetime']
                        else:
                            entry_timestamp = df.index[i]
                        
                        return {
                            'entry_time': entry_timestamp,
                            'entry_price': candle['Close'],
                            'entry_index': i,
                            'fvg_inverted': fvg,
                            'displacement': body_size
                        }
            
            elif direction == 'bearish':
                # Bearish inversion: Price comes back up, fills bullish FVG, closes below
                fvg_top = fvg['top']
                fvg_bottom = fvg['bottom']
                
                # Check if candle closes decisively below FVG
                if (candle['High'] >= fvg_top and 
                    candle['Close'] < fvg_bottom):
                    
                    # Check for displacement (strong bearish candle)
                    body_size = candle['Open'] - candle['Close']
                    if body_size > 2:  # Displacement threshold
                        # Get actual timestamp if df has datetime column
                        if 'datetime' in df.columns:
                            entry_timestamp = df.iloc[i]['datetime']
                        else:
                            entry_timestamp = df.index[i]
                        
                        return {
                            'entry_time': entry_timestamp,
                            'entry_price': candle['Close'],
                            'entry_index': i,
                            'fvg_inverted': fvg,
                            'displacement': body_size
                        }
        
        return None
    
    def calculate_stop_loss(self, reversal_candle: Dict, fvg: Dict, 
                           direction: str) -> Tuple[float, float]:
        """
        Calculate both stop loss levels.
        
        SL A (Structural - Safe): 1 point beyond extreme wick of Hammer/Shooting Star
        SL B (Aggressive - Inversion): 1 point beyond Inverted FVG
        
        Args:
            reversal_candle: Reversal candle data
            fvg: FVG data
            direction: Trade direction
            
        Returns:
            Tuple of (SL_A, SL_B)
        """
        if direction == 'bullish':
            # Long trade
            sl_a = reversal_candle['low'] - 1  # 1 point below hammer low
            sl_b = fvg['bottom'] - 1  # 1 point below bearish FVG bottom
        else:
            # Short trade
            sl_a = reversal_candle['high'] + 1  # 1 point above shooting star high
            sl_b = fvg['top'] + 1  # 1 point above bullish FVG top
        
        return sl_a, sl_b
    
    def calculate_take_profits(self, entry_price: float, direction: str,
                               asian_range: Dict, judas_data: pd.DataFrame) -> Dict:
        """
        Calculate take profit levels.
        
        TP1: Opposite liquidity of Asian Range
        TP2: Fibonacci extension (Standard Deviation) -1 or -1.5 of manipulation range
        
        Args:
            entry_price: Entry price
            direction: Trade direction
            asian_range: Asian range data
            judas_data: Judas swing data
            
        Returns:
            Dictionary with TP levels
        """
        if direction == 'bullish':
            tp1 = asian_range['asian_high']  # Target opposite side
            
            # Calculate manipulation range for extension
            manip_low = judas_data['Low'].min()
            manip_high = judas_data['High'].max()
            manip_range = manip_high - manip_low
            
            # Fibonacci extensions
            tp2_1x = entry_price + manip_range * 1.0
            tp2_15x = entry_price + manip_range * 1.5
            
        else:  # bearish
            tp1 = asian_range['asian_low']
            
            manip_low = judas_data['Low'].min()
            manip_high = judas_data['High'].max()
            manip_range = manip_high - manip_low
            
            tp2_1x = entry_price - manip_range * 1.0
            tp2_15x = entry_price - manip_range * 1.5
        
        return {
            'tp1': tp1,
            'tp2_1x': tp2_1x,
            'tp2_15x': tp2_15x
        }
    
    def simulate_trade(self, entry_data: Dict, sl_a: float, sl_b: float,
                      tps: Dict, direction: str, df: pd.DataFrame,
                      entry_index: int) -> Dict:
        """
        Simulate trade execution and track results.
        
        Args:
            entry_data: Entry signal data
            sl_a: Stop loss A (structural)
            sl_b: Stop loss B (aggressive)
            tps: Take profit levels
            direction: Trade direction
            df: DataFrame with price data
            entry_index: Index of entry
            
        Returns:
            Dictionary with trade results for both SL approaches
        """
        entry_price = entry_data['entry_price']
        
        # Look forward up to 200 candles (16+ hours to catch full moves)
        max_lookforward = min(entry_index + 200, len(df))
        
        # Initialize results
        result_sl_a = {'status': 'open', 'exit_price': None, 'exit_time': None, 
                      'pnl': 0, 'rr_achieved': 0}
        result_sl_b = {'status': 'open', 'exit_price': None, 'exit_time': None,
                      'pnl': 0, 'rr_achieved': 0}
        
        tp1_hit_a = False
        tp1_hit_b = False
        
        for i in range(entry_index + 1, max_lookforward):
            candle = df.iloc[i]
            
            # Check SL A (structural)
            if result_sl_a['status'] == 'open':
                if direction == 'bullish':
                    if candle['Low'] <= sl_a:
                        result_sl_a = {
                            'status': 'stopped_out',
                            'exit_price': sl_a,
                            'exit_time': df.index[i],
                            'pnl': sl_a - entry_price,
                            'rr_achieved': 0
                        }
                    elif candle['High'] >= tps['tp1'] and not tp1_hit_a:
                        tp1_hit_a = True
                    elif candle['High'] >= tps['tp2_15x']:
                        result_sl_a = {
                            'status': 'tp_hit',
                            'exit_price': tps['tp2_15x'],
                            'exit_time': df.index[i],
                            'pnl': tps['tp2_15x'] - entry_price,
                            'rr_achieved': (tps['tp2_15x'] - entry_price) / abs(entry_price - sl_a)
                        }
                else:  # bearish
                    if candle['High'] >= sl_a:
                        result_sl_a = {
                            'status': 'stopped_out',
                            'exit_price': sl_a,
                            'exit_time': df.index[i],
                            'pnl': entry_price - sl_a,
                            'rr_achieved': 0
                        }
                    elif candle['Low'] <= tps['tp1'] and not tp1_hit_a:
                        tp1_hit_a = True
                    elif candle['Low'] <= tps['tp2_15x']:
                        result_sl_a = {
                            'status': 'tp_hit',
                            'exit_price': tps['tp2_15x'],
                            'exit_time': df.index[i],
                            'pnl': entry_price - tps['tp2_15x'],
                            'rr_achieved': (entry_price - tps['tp2_15x']) / abs(entry_price - sl_a)
                        }
            
            # Check SL B (aggressive/inversion)
            if result_sl_b['status'] == 'open':
                if direction == 'bullish':
                    if candle['Low'] <= sl_b:
                        result_sl_b = {
                            'status': 'stopped_out',
                            'exit_price': sl_b,
                            'exit_time': df.index[i],
                            'pnl': sl_b - entry_price,
                            'rr_achieved': 0
                        }
                    elif candle['High'] >= tps['tp1'] and not tp1_hit_b:
                        tp1_hit_b = True
                    elif candle['High'] >= tps['tp2_15x']:
                        result_sl_b = {
                            'status': 'tp_hit',
                            'exit_price': tps['tp2_15x'],
                            'exit_time': df.index[i],
                            'pnl': tps['tp2_15x'] - entry_price,
                            'rr_achieved': (tps['tp2_15x'] - entry_price) / abs(entry_price - sl_b) if abs(entry_price - sl_b) > 0 else 0
                        }
                else:  # bearish
                    if candle['High'] >= sl_b:
                        result_sl_b = {
                            'status': 'stopped_out',
                            'exit_price': sl_b,
                            'exit_time': df.index[i],
                            'pnl': entry_price - sl_b,
                            'rr_achieved': 0
                        }
                    elif candle['Low'] <= tps['tp1'] and not tp1_hit_b:
                        tp1_hit_b = True
                    elif candle['Low'] <= tps['tp2_15x']:
                        result_sl_b = {
                            'status': 'tp_hit',
                            'exit_price': tps['tp2_15x'],
                            'exit_time': df.index[i],
                            'pnl': entry_price - tps['tp2_15x'],
                            'rr_achieved': (entry_price - tps['tp2_15x']) / abs(entry_price - sl_b) if abs(entry_price - sl_b) > 0 else 0
                        }
        
        return {
            'sl_a': result_sl_a,
            'sl_b': result_sl_b,
            'tp1_hit_a': tp1_hit_a,
            'tp1_hit_b': tp1_hit_b
        }
    
    def run_backtest(self) -> Dict:
        """
        Run complete backtest of London Reversal strategy.
        
        Returns:
            Dictionary with comprehensive results and statistics
        """
        print("=" * 80)
        print("LONDON REVERSAL STRATEGY BACKTEST")
        print("=" * 80)
        print("\nPhase 1: Identifying Trading Days...")
        
        # Get unique trading days
        dates = pd.date_range(
            start=self.data_5m.index.min().date() + timedelta(days=1),
            end=self.data_5m.index.max().date(),
            freq='D'
        )
        
        total_days = len(dates)
        setups_found = 0
        
        for date_idx, date in enumerate(dates):
            if date_idx % 50 == 0:
                print(f"Progress: {date_idx}/{total_days} days analyzed...")
            
            # Phase 1: Identify Asian Range
            asian_range = self.identify_asian_range(date)
            if not asian_range:
                continue
            
            # Get Judas period data (02:00-03:00 on current day)
            judas_start_dt = pd.Timestamp.combine(date.date(), self.judas_start)
            judas_end_dt = pd.Timestamp.combine(date.date(), self.judas_end)
            
            judas_data = self.data_5m[
                (self.data_5m.index >= judas_start_dt) &
                (self.data_5m.index <= judas_end_dt)
            ]
            
            if len(judas_data) < 3:
                continue
            
            # Phase 2: Detect Liquidity Sweep
            sweep = self.detect_liquidity_sweep(asian_range, judas_data)
            if not sweep:
                continue
            
            # Check HTF confluence
            htf_confluence = self.get_htf_levels(
                judas_end_dt,
                sweep['sweep_extreme'],
                sweep['direction']
            )
            
            # Get post-Judas data for reversal detection (extend to full trading day)
            post_judas_start = judas_end_dt
            post_judas_end = post_judas_start + timedelta(hours=12)
            
            post_judas_data = self.data_5m[
                (self.data_5m.index > post_judas_start) &
                (self.data_5m.index <= post_judas_end)
            ]
            
            if len(post_judas_data) < 10:
                continue
            
            # Phase 3: Detect Reversal Candle
            reversal_candle = self.detect_reversal_candle(
                post_judas_data.reset_index(drop=False),
                sweep['direction']
            )
            
            if not reversal_candle:
                continue
            
            # Phase 4: Detect FVG Inversion (Entry Trigger)
            fvg_inversion = self.detect_fvg_inversion(
                post_judas_data.reset_index(drop=False),
                sweep['fvg_created'],
                sweep['direction'],
                reversal_candle['index'] + 1
            )
            
            if not fvg_inversion:
                continue
            
            setups_found += 1
            
            # Calculate stop losses
            sl_a, sl_b = self.calculate_stop_loss(
                reversal_candle,
                sweep['fvg_created'],
                sweep['direction']
            )
            
            # Calculate take profits
            tps = self.calculate_take_profits(
                fvg_inversion['entry_price'],
                sweep['direction'],
                asian_range,
                judas_data
            )
            
            # Get extended forward-looking data for trade simulation
            sim_end = fvg_inversion['entry_time'] + timedelta(hours=20)
            sim_data = self.data_5m[
                (self.data_5m.index >= fvg_inversion['entry_time']) &
                (self.data_5m.index <= sim_end)
            ]
            
            # Simulate trade
            trade_results = self.simulate_trade(
                fvg_inversion,
                sl_a,
                sl_b,
                tps,
                sweep['direction'],
                sim_data,
                0  # Entry is at index 0 in sim_data
            )
            
            # Store trade data
            trade_record = {
                'date': date,
                'direction': sweep['direction'],
                'asian_high': asian_range['asian_high'],
                'asian_low': asian_range['asian_low'],
                'sweep_type': sweep['sweep_type'],
                'sweep_extreme': sweep['sweep_extreme'],
                'htf_confluence': htf_confluence['has_confluence'],
                'htf_distance': htf_confluence.get('distance', None),
                'reversal_type': reversal_candle['type'],
                'entry_time': fvg_inversion['entry_time'],
                'entry_price': fvg_inversion['entry_price'],
                'sl_a': sl_a,
                'sl_b': sl_b,
                'tp1': tps['tp1'],
                'tp2_1x': tps['tp2_1x'],
                'tp2_15x': tps['tp2_15x'],
                'result_sl_a': trade_results['sl_a'],
                'result_sl_b': trade_results['sl_b'],
                'risk_sl_a': abs(fvg_inversion['entry_price'] - sl_a),
                'risk_sl_b': abs(fvg_inversion['entry_price'] - sl_b)
            }
            
            self.trades.append(trade_record)
        
        print(f"\nBacktest Complete!")
        print(f"Total days analyzed: {total_days}")
        print(f"Setups found: {setups_found}")
        
        return self.analyze_results()
    
    def analyze_results(self) -> Dict:
        """
        Analyze backtest results and generate comprehensive statistics.
        
        Returns:
            Dictionary with detailed statistics and analysis
        """
        if not self.trades:
            return {
                'error': 'No trades found',
                'total_setups': 0
            }
        
        df_trades = pd.DataFrame(self.trades)
        
        # Analysis 1: Inversion FVG Failure Rate Analysis
        print("\n" + "=" * 80)
        print("ANALYSIS 1: INVERSION FVG FAILURE RATE")
        print("=" * 80)
        
        # SL A Results
        sl_a_wins = len([t for t in self.trades if t['result_sl_a']['status'] == 'tp_hit'])
        sl_a_losses = len([t for t in self.trades if t['result_sl_a']['status'] == 'stopped_out'])
        sl_a_win_rate = sl_a_wins / len(self.trades) * 100 if self.trades else 0
        
        sl_a_total_pnl = sum(t['result_sl_a']['pnl'] for t in self.trades)
        sl_a_avg_win = np.mean([t['result_sl_a']['pnl'] for t in self.trades 
                                if t['result_sl_a']['status'] == 'tp_hit']) if sl_a_wins > 0 else 0
        sl_a_avg_loss = np.mean([t['result_sl_a']['pnl'] for t in self.trades 
                                 if t['result_sl_a']['status'] == 'stopped_out']) if sl_a_losses > 0 else 0
        
        sl_a_profit_factor = (abs(sl_a_avg_win * sl_a_wins) / abs(sl_a_avg_loss * sl_a_losses) 
                             if sl_a_losses > 0 and sl_a_avg_loss != 0 else float('inf'))
        
        # SL B Results
        sl_b_wins = len([t for t in self.trades if t['result_sl_b']['status'] == 'tp_hit'])
        sl_b_losses = len([t for t in self.trades if t['result_sl_b']['status'] == 'stopped_out'])
        sl_b_win_rate = sl_b_wins / len(self.trades) * 100 if self.trades else 0
        
        sl_b_total_pnl = sum(t['result_sl_b']['pnl'] for t in self.trades)
        sl_b_avg_win = np.mean([t['result_sl_b']['pnl'] for t in self.trades 
                                if t['result_sl_b']['status'] == 'tp_hit']) if sl_b_wins > 0 else 0
        sl_b_avg_loss = np.mean([t['result_sl_b']['pnl'] for t in self.trades 
                                 if t['result_sl_b']['status'] == 'stopped_out']) if sl_b_losses > 0 else 0
        
        sl_b_profit_factor = (abs(sl_b_avg_win * sl_b_wins) / abs(sl_b_avg_loss * sl_b_losses) 
                             if sl_b_losses > 0 and sl_b_avg_loss != 0 else float('inf'))
        
        print(f"\nSL A (Structural - Safe):")
        print(f"  Win Rate: {sl_a_win_rate:.2f}% ({sl_a_wins}W / {sl_a_losses}L)")
        print(f"  Total P&L: {sl_a_total_pnl:.2f} points")
        print(f"  Avg Win: {sl_a_avg_win:.2f} points")
        print(f"  Avg Loss: {sl_a_avg_loss:.2f} points")
        print(f"  Profit Factor: {sl_a_profit_factor:.2f}")
        
        print(f"\nSL B (Aggressive - Inversion):")
        print(f"  Win Rate: {sl_b_win_rate:.2f}% ({sl_b_wins}W / {sl_b_losses}L)")
        print(f"  Total P&L: {sl_b_total_pnl:.2f} points")
        print(f"  Avg Win: {sl_b_avg_win:.2f} points")
        print(f"  Avg Loss: {sl_b_avg_loss:.2f} points")
        print(f"  Profit Factor: {sl_b_profit_factor:.2f}")
        
        # Fakeout analysis for SL B
        fakeouts = len([t for t in self.trades 
                       if t['result_sl_b']['status'] == 'stopped_out' and 
                       t['result_sl_a']['status'] == 'tp_hit'])
        fakeout_rate = fakeouts / len(self.trades) * 100 if self.trades else 0
        
        print(f"\nInversion FVG Fakeout Analysis:")
        print(f"  Fakeouts (SL B stopped but SL A wins): {fakeouts}")
        print(f"  Fakeout Rate: {fakeout_rate:.2f}%")
        
        # Analysis 2: Sweep Quality Analysis
        print("\n" + "=" * 80)
        print("ANALYSIS 2: SWEEP QUALITY (HTF Confluence Impact)")
        print("=" * 80)
        
        htf_trades = [t for t in self.trades if t['htf_confluence']]
        no_htf_trades = [t for t in self.trades if not t['htf_confluence']]
        
        if htf_trades:
            htf_sl_a_wins = len([t for t in htf_trades if t['result_sl_a']['status'] == 'tp_hit'])
            htf_sl_a_wr = htf_sl_a_wins / len(htf_trades) * 100
            htf_sl_b_wins = len([t for t in htf_trades if t['result_sl_b']['status'] == 'tp_hit'])
            htf_sl_b_wr = htf_sl_b_wins / len(htf_trades) * 100
            
            print(f"\nWith HTF Confluence ({len(htf_trades)} trades):")
            print(f"  SL A Win Rate: {htf_sl_a_wr:.2f}%")
            print(f"  SL B Win Rate: {htf_sl_b_wr:.2f}%")
        
        if no_htf_trades:
            no_htf_sl_a_wins = len([t for t in no_htf_trades if t['result_sl_a']['status'] == 'tp_hit'])
            no_htf_sl_a_wr = no_htf_sl_a_wins / len(no_htf_trades) * 100
            no_htf_sl_b_wins = len([t for t in no_htf_trades if t['result_sl_b']['status'] == 'tp_hit'])
            no_htf_sl_b_wr = no_htf_sl_b_wins / len(no_htf_trades) * 100
            
            print(f"\nWithout HTF Confluence ({len(no_htf_trades)} trades):")
            print(f"  SL A Win Rate: {no_htf_sl_a_wr:.2f}%")
            print(f"  SL B Win Rate: {no_htf_sl_b_wr:.2f}%")
        
        # Analysis 3: Long-term Profitability Comparison
        print("\n" + "=" * 80)
        print("ANALYSIS 3: LONG-TERM PROFITABILITY (100+ Trades)")
        print("=" * 80)
        
        # Expectancy = (Win% × Avg Win) - (Loss% × Avg Loss)
        sl_a_expectancy = (sl_a_win_rate/100 * sl_a_avg_win) + ((100-sl_a_win_rate)/100 * sl_a_avg_loss)
        sl_b_expectancy = (sl_b_win_rate/100 * sl_b_avg_win) + ((100-sl_b_win_rate)/100 * sl_b_avg_loss)
        
        print(f"\nExpectancy per Trade:")
        print(f"  SL A: {sl_a_expectancy:.2f} points")
        print(f"  SL B: {sl_b_expectancy:.2f} points")
        
        # RR Ratio Analysis
        sl_a_rr_ratios = [t['result_sl_a']['rr_achieved'] for t in self.trades 
                          if t['result_sl_a']['status'] == 'tp_hit']
        sl_b_rr_ratios = [t['result_sl_b']['rr_achieved'] for t in self.trades 
                          if t['result_sl_b']['status'] == 'tp_hit']
        
        sl_a_avg_rr = np.mean(sl_a_rr_ratios) if sl_a_rr_ratios else 0
        sl_b_avg_rr = np.mean(sl_b_rr_ratios) if sl_b_rr_ratios else 0
        
        print(f"\nAverage RR Achieved on Wins:")
        print(f"  SL A: 1:{sl_a_avg_rr:.2f}")
        print(f"  SL B: 1:{sl_b_avg_rr:.2f}")
        
        # Cumulative returns (assuming $100 per point)
        sl_a_cumulative = sl_a_total_pnl * 100
        sl_b_cumulative = sl_b_total_pnl * 100
        
        print(f"\nCumulative Returns (@ $100/point):")
        print(f"  SL A: ${sl_a_cumulative:,.2f}")
        print(f"  SL B: ${sl_b_cumulative:,.2f}")
        
        # Generate trade log
        print("\n" + "=" * 80)
        print("DETAILED TRADE LOG (First 10 trades)")
        print("=" * 80)
        
        for i, trade in enumerate(self.trades[:10]):
            print(f"\nTrade #{i+1} - {trade['date'].date()} - {trade['direction'].upper()}")
            print(f"  Sweep: {trade['sweep_type']}")
            print(f"  HTF Confluence: {'YES' if trade['htf_confluence'] else 'NO'}")
            print(f"  Entry: {trade['entry_price']:.2f}")
            print(f"  SL A: {trade['result_sl_a']['status']} | P&L: {trade['result_sl_a']['pnl']:.2f}")
            print(f"  SL B: {trade['result_sl_b']['status']} | P&L: {trade['result_sl_b']['pnl']:.2f}")
        
        # Summary
        print("\n" + "=" * 80)
        print("SUMMARY & CONCLUSIONS")
        print("=" * 80)
        
        print(f"\nTotal Setups Found: {len(self.trades)}")
        print(f"\nBest Approach: ", end="")
        if sl_b_expectancy > sl_a_expectancy:
            print(f"SL B (Aggressive) - Higher Expectancy ({sl_b_expectancy:.2f} vs {sl_a_expectancy:.2f})")
        else:
            print(f"SL A (Structural) - Higher Expectancy ({sl_a_expectancy:.2f} vs {sl_b_expectancy:.2f})")
        
        print(f"\nHTF Confluence Impact: ", end="")
        if htf_trades and no_htf_trades:
            if htf_sl_a_wr > no_htf_sl_a_wr:
                improvement = htf_sl_a_wr - no_htf_sl_a_wr
                print(f"Significant (+{improvement:.2f}% win rate improvement)")
            else:
                print("Minimal impact")
        else:
            print("Insufficient data")
        
        # Return structured results
        return {
            'total_trades': len(self.trades),
            'sl_a': {
                'wins': sl_a_wins,
                'losses': sl_a_losses,
                'win_rate': sl_a_win_rate,
                'total_pnl': sl_a_total_pnl,
                'avg_win': sl_a_avg_win,
                'avg_loss': sl_a_avg_loss,
                'profit_factor': sl_a_profit_factor,
                'expectancy': sl_a_expectancy,
                'avg_rr': sl_a_avg_rr
            },
            'sl_b': {
                'wins': sl_b_wins,
                'losses': sl_b_losses,
                'win_rate': sl_b_win_rate,
                'total_pnl': sl_b_total_pnl,
                'avg_win': sl_b_avg_win,
                'avg_loss': sl_b_avg_loss,
                'profit_factor': sl_b_profit_factor,
                'expectancy': sl_b_expectancy,
                'avg_rr': sl_b_avg_rr
            },
            'fakeout_analysis': {
                'fakeouts': fakeouts,
                'fakeout_rate': fakeout_rate
            },
            'htf_analysis': {
                'trades_with_htf': len(htf_trades),
                'trades_without_htf': len(no_htf_trades)
            },
            'trades': self.trades
        }


def load_and_combine_data(file_patterns: List[str], freq: str) -> pd.DataFrame:
    """
    Load and combine multiple CSV files into a single DataFrame.
    
    Args:
        file_patterns: List of file paths to load
        freq: Frequency identifier
        
    Returns:
        Combined DataFrame
    """
    dfs = []
    for filepath in file_patterns:
        try:
            # Load CSV with semicolon delimiter
            df = pd.read_csv(filepath, sep=';')
            
            # Combine date and time columns
            df['datetime'] = pd.to_datetime(
                df['Column1'] + ' ' + df['Column2'],
                format='%d/%m/%Y %H:%M:%S'
            )
            
            # Rename columns
            df = df.rename(columns={
                'Column3': 'Open',
                'Column4': 'High',
                'Column5': 'Low',
                'Column6': 'Close',
                'Column7': 'Volume'
            })
            
            # Set datetime as index
            df = df.set_index('datetime')
            df = df[['Open', 'High', 'Low', 'Close', 'Volume']]
            dfs.append(df)
            print(f"  Loaded: {filepath}")
        except Exception as e:
            print(f"  Warning: Could not load {filepath}: {e}")
    
    if not dfs:
        raise ValueError("No data files could be loaded")
    
    # Combine and sort
    combined = pd.concat(dfs, axis=0)
    combined = combined.sort_index()
    combined = combined[~combined.index.duplicated(keep='first')]  # Remove duplicates
    
    return combined


def main():
    """
    Main execution function.
    """
    print("London Reversal Strategy Backtester")
    print("=" * 80)
    
    # Try to load comprehensive dataset
    import os
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    print("\nLoading 5-minute data...")
    files_5m = [
        os.path.join(base_dir, "ES 5m (2018-2020).csv"),
        os.path.join(base_dir, "ES 5m (2021-2023).csv"),
        os.path.join(base_dir, "ES 5m (2024-2025).csv")
    ]
    
    print("\nLoading 1-hour data...")
    files_1h = [
        os.path.join(base_dir, "ES 1h (2018-2025).csv")
    ]
    
    # Create temporary combined strategy class
    class CombinedLondonReversalStrategy(LondonReversalStrategy):
        def __init__(self, data_5m: pd.DataFrame, data_1h: pd.DataFrame):
            self.data_5m = data_5m
            self.data_1h = data_1h
            
            # Strategy parameters
            self.asian_start = time(19, 0)  # 19:00
            self.asian_end = time(23, 59)   # 23:59
            self.judas_start = time(2, 0)   # 02:00 London open
            self.judas_end = time(3, 0)     # 03:00
            
            # Trade tracking
            self.trades = []
            self.setups_analyzed = []
    
    # Load data
    data_5m_combined = load_and_combine_data(files_5m, '5T')
    data_1h_combined = load_and_combine_data(files_1h, '1H')
    
    print(f"\n5m Data: {len(data_5m_combined)} bars from {data_5m_combined.index.min()} to {data_5m_combined.index.max()}")
    print(f"1H Data: {len(data_1h_combined)} bars from {data_1h_combined.index.min()} to {data_1h_combined.index.max()}")
    
    # Initialize strategy
    strategy = CombinedLondonReversalStrategy(data_5m_combined, data_1h_combined)
    
    # Run backtest
    results = strategy.run_backtest()
    
    # Export results to CSV
    if results['total_trades'] > 0:
        df_results = pd.DataFrame(results['trades'])
        output_file = "/home/runner/work/Backtest-Trading/Backtest-Trading/london_reversal_results.csv"
        df_results.to_csv(output_file, index=False)
        print(f"\n\nResults exported to: {output_file}")
    
    print("\n" + "=" * 80)
    print("BACKTEST COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()

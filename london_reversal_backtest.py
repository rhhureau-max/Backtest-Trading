#!/usr/bin/env python3
"""
London Reversal Backtesting Script
===================================
A complete backtesting system for the London Reversal strategy based on Smart Money Concepts (SMC).

Strategy Overview:
1. Tokyo Session Range: Identify High/Low between 17:00-00:00 Chicago time
2. London Killzone: Monitor 01:00-04:00 for entry setups
3. Validation Sequence:
   - Manipulation: Price sweeps Tokyo High/Low
   - FVG Formation: Fair Value Gap forms opposite to manipulation
   - MSS: Market Structure Shift confirms reversal
4. Entry: 50% Fib retracement from manipulation peak to MSS bottom
5. Exit: Multiple TP levels at 1R, 1.5R, 2R

Author: Senior Quant Developer
Date: December 2024
"""

import pandas as pd
import numpy as np
from datetime import datetime, time, timedelta
import zipfile
import os
import glob
from typing import List, Dict, Tuple, Optional
import warnings
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
warnings.filterwarnings('ignore')


class LondonReversalBacktest:
    """
    Complete backtesting engine for London Reversal strategy.
    """
    
    def __init__(self, data_dir: str = "/home/runner/work/Backtest-Trading/Backtest-Trading"):
        """
        Initialize the backtesting engine.
        
        Args:
            data_dir: Directory containing CSV data files
        """
        self.data_dir = data_dir
        self.trade_log = pd.DataFrame()  # Main data structure for all trades
        self.missed_trades = 0  # Counter for missed opportunities
        
    def load_data(self, timeframe: str, years: List[int]) -> pd.DataFrame:
        """
        Load and combine data from multiple years for specified timeframe.
        
        Args:
            timeframe: '1m', '5m', '15m', '1H', '4H'
            years: List of years to load
            
        Returns:
            Combined DataFrame with all data
        """
        all_data = []
        
        for year in years:
            # Construct filename based on timeframe
            if timeframe == '1m':
                filename = f"{year} 1m.csv.zip"
            elif timeframe == '5m':
                filename = f"{year} 5m.csv"
            elif timeframe == '15m':
                filename = f"{year} 15m.csv"
            elif timeframe == '1H':
                filename = f"{year} 1H.csv"
            elif timeframe == '4H':
                filename = f"{year} 4H.csv"
            else:
                raise ValueError(f"Unsupported timeframe: {timeframe}")
                
            filepath = os.path.join(self.data_dir, filename)
            
            if not os.path.exists(filepath):
                print(f"Warning: File not found: {filepath}")
                continue
                
            try:
                # Handle zipped files
                if filepath.endswith('.zip'):
                    with zipfile.ZipFile(filepath, 'r') as zip_ref:
                        # Get the CSV filename inside the zip
                        csv_filename = zip_ref.namelist()[0]
                        with zip_ref.open(csv_filename) as f:
                            df = pd.read_csv(
                                f,
                                delimiter=';',
                                names=['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume'],
                                skiprows=1,
                                dtype={'Open': float, 'High': float, 'Low': float, 'Close': float, 'Volume': float}
                            )
                else:
                    # Regular CSV file
                    df = pd.read_csv(
                        filepath,
                        delimiter=';',
                        names=['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume'],
                        skiprows=1,
                        dtype={'Open': float, 'High': float, 'Low': float, 'Close': float, 'Volume': float}
                    )
                
                # Combine Date and Time columns
                df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%d/%m/%Y %H:%M:%S')
                df = df.drop(['Date', 'Time'], axis=1)
                df = df.set_index('Datetime')
                df = df.sort_index()
                
                all_data.append(df)
                print(f"Loaded {year} {timeframe}: {len(df)} bars")
                
            except Exception as e:
                print(f"Error loading {filepath}: {e}")
                continue
        
        if not all_data:
            raise ValueError("No data loaded!")
            
        # Combine all years
        combined_df = pd.concat(all_data, axis=0)
        combined_df = combined_df.sort_index()
        
        # Remove duplicates
        combined_df = combined_df[~combined_df.index.duplicated(keep='first')]
        
        print(f"\nTotal data loaded: {len(combined_df)} bars from {combined_df.index[0]} to {combined_df.index[-1]}")
        
        return combined_df
    
    def identify_swings(self, data: pd.DataFrame, lookback: int = 2) -> pd.DataFrame:
        """
        Identify swing highs and swing lows using fractal algorithm.
        
        Swing High: High > lookback candles before AND after
        Swing Low: Low < lookback candles before AND after
        
        Args:
            data: DataFrame with OHLC data
            lookback: Number of candles to look before/after (default=2)
            
        Returns:
            DataFrame with 'SwingHigh' and 'SwingLow' columns
        """
        df = data.copy()
        df['SwingHigh'] = np.nan
        df['SwingLow'] = np.nan
        
        # Need at least lookback candles on each side
        for i in range(lookback, len(df) - lookback):
            # Check for Swing High
            current_high = df.iloc[i]['High']
            is_swing_high = True
            
            # Check lookback candles before
            for j in range(1, lookback + 1):
                if df.iloc[i - j]['High'] >= current_high:
                    is_swing_high = False
                    break
            
            # Check lookback candles after
            if is_swing_high:
                for j in range(1, lookback + 1):
                    if df.iloc[i + j]['High'] >= current_high:
                        is_swing_high = False
                        break
            
            if is_swing_high:
                df.iloc[i, df.columns.get_loc('SwingHigh')] = current_high
            
            # Check for Swing Low
            current_low = df.iloc[i]['Low']
            is_swing_low = True
            
            # Check lookback candles before
            for j in range(1, lookback + 1):
                if df.iloc[i - j]['Low'] <= current_low:
                    is_swing_low = False
                    break
            
            # Check lookback after
            if is_swing_low:
                for j in range(1, lookback + 1):
                    if df.iloc[i + j]['Low'] <= current_low:
                        is_swing_low = False
                        break
            
            if is_swing_low:
                df.iloc[i, df.columns.get_loc('SwingLow')] = current_low
        
        return df
    
    def detect_fvg(self, data: pd.DataFrame, start_idx: int, end_idx: int, 
                   direction: str) -> Optional[Dict]:
        """
        Detect Fair Value Gap (FVG) in specified range.
        
        Bearish FVG: Gap between candle[i-1].Low and candle[i+1].High
        Bullish FVG: Gap between candle[i-1].High and candle[i+1].Low
        
        Args:
            data: DataFrame with OHLC data
            start_idx: Start index for search
            end_idx: End index for search
            direction: 'bearish' or 'bullish'
            
        Returns:
            Dictionary with FVG details or None
        """
        # Need at least 3 candles for FVG
        if end_idx - start_idx < 2:
            return None
        
        for i in range(start_idx + 1, min(end_idx - 1, len(data) - 1)):
            if direction == 'bearish':
                # Bearish FVG: candle[i-1].Low > candle[i+1].High
                if data.iloc[i - 1]['Low'] > data.iloc[i + 1]['High']:
                    return {
                        'index': i,
                        'datetime': data.index[i],
                        'top': data.iloc[i - 1]['Low'],
                        'bottom': data.iloc[i + 1]['High'],
                        'direction': 'bearish'
                    }
            
            elif direction == 'bullish':
                # Bullish FVG: candle[i-1].High < candle[i+1].Low
                if data.iloc[i - 1]['High'] < data.iloc[i + 1]['Low']:
                    return {
                        'index': i,
                        'datetime': data.index[i],
                        'bottom': data.iloc[i - 1]['High'],
                        'top': data.iloc[i + 1]['Low'],
                        'direction': 'bullish'
                    }
        
        return None
    
    def detect_mss(self, data: pd.DataFrame, start_idx: int, end_idx: int,
                   direction: str, fvg_idx: int) -> Optional[Dict]:
        """
        Detect Market Structure Shift (MSS).
        
        SHORT: Price body breaks below last Swing Low
        LONG: Price body breaks above last Swing High
        
        CRITICAL: FVG must be created BEFORE or AT the MSS candle.
        
        Args:
            data: DataFrame with OHLC and swing data
            start_idx: Start index for search
            end_idx: End index for search
            direction: 'short' or 'long'
            fvg_idx: Index where FVG was detected
            
        Returns:
            Dictionary with MSS details or None
        """
        for i in range(start_idx, min(end_idx, len(data))):
            if direction == 'short':
                # Find last Swing Low before current candle
                swing_lows = data.loc[:data.index[i], 'SwingLow'].dropna()
                if len(swing_lows) == 0:
                    continue
                
                last_swing_low = swing_lows.iloc[-1]
                
                # Check if close breaks below swing low (body break)
                if data.iloc[i]['Close'] < last_swing_low:
                    # CRITICAL CHECK: FVG must be before or at MSS candle
                    if fvg_idx <= i:
                        return {
                            'index': i,
                            'datetime': data.index[i],
                            'swing_level': last_swing_low,
                            'close': data.iloc[i]['Close'],
                            'direction': 'short'
                        }
            
            elif direction == 'long':
                # Find last Swing High before current candle
                swing_highs = data.loc[:data.index[i], 'SwingHigh'].dropna()
                if len(swing_highs) == 0:
                    continue
                
                last_swing_high = swing_highs.iloc[-1]
                
                # Check if close breaks above swing high (body break)
                if data.iloc[i]['Close'] > last_swing_high:
                    # CRITICAL CHECK: FVG must be before or at MSS candle
                    if fvg_idx <= i:
                        return {
                            'index': i,
                            'datetime': data.index[i],
                            'swing_level': last_swing_high,
                            'close': data.iloc[i]['Close'],
                            'direction': 'long'
                        }
        
        return None
    
    def find_tokyo_range(self, data: pd.DataFrame, date: datetime.date) -> Optional[Dict]:
        """
        Find Tokyo session range for given date.
        
        Tokyo Session: 17:00 to 00:00 Chicago time (previous day/night)
        
        Args:
            data: DataFrame with OHLC data
            date: The date for which to find Tokyo range (will look at previous evening)
            
        Returns:
            Dictionary with Tokyo High/Low or None
        """
        # Tokyo session is from 17:00 previous day to 00:00 current day
        previous_date = date - timedelta(days=1)
        
        # Create datetime range for Tokyo session
        tokyo_start = datetime.combine(previous_date, time(17, 0))
        tokyo_end = datetime.combine(date, time(0, 0))
        
        # Filter data for Tokyo session
        tokyo_data = data[(data.index >= tokyo_start) & (data.index < tokyo_end)]
        
        if len(tokyo_data) == 0:
            return None
        
        tokyo_high = tokyo_data['High'].max()
        tokyo_low = tokyo_data['Low'].min()
        
        return {
            'date': date,
            'high': tokyo_high,
            'low': tokyo_low,
            'start': tokyo_start,
            'end': tokyo_end
        }
    
    def check_manipulation(self, data: pd.DataFrame, tokyo_range: Dict,
                          killzone_start_idx: int, killzone_end_idx: int) -> Optional[Dict]:
        """
        Check if price swept/raided Tokyo High or Low during killzone.
        
        Args:
            data: DataFrame with OHLC data
            tokyo_range: Dictionary with Tokyo High/Low
            killzone_start_idx: Start index of killzone
            killzone_end_idx: End index of killzone
            
        Returns:
            Dictionary with manipulation details or None
        """
        tokyo_high = tokyo_range['high']
        tokyo_low = tokyo_range['low']
        
        for i in range(killzone_start_idx, min(killzone_end_idx, len(data))):
            # Check for bearish manipulation (sweep above Tokyo High)
            if data.iloc[i]['High'] > tokyo_high:
                # Find the highest point reached during sweep
                sweep_high = data.iloc[killzone_start_idx:i+1]['High'].max()
                
                return {
                    'type': 'bearish',
                    'level_swept': tokyo_high,
                    'peak': sweep_high,
                    'index': i,
                    'datetime': data.index[i]
                }
            
            # Check for bullish manipulation (sweep below Tokyo Low)
            if data.iloc[i]['Low'] < tokyo_low:
                # Find the lowest point reached during sweep
                sweep_low = data.iloc[killzone_start_idx:i+1]['Low'].min()
                
                return {
                    'type': 'bullish',
                    'level_swept': tokyo_low,
                    'peak': sweep_low,
                    'index': i,
                    'datetime': data.index[i]
                }
        
        return None
    
    def calculate_entry_and_targets(self, manipulation: Dict, mss: Dict,
                                   direction: str) -> Dict:
        """
        Calculate entry price (50% Fib) and target levels.
        
        Args:
            manipulation: Manipulation details
            mss: MSS details
            direction: 'short' or 'long'
            
        Returns:
            Dictionary with entry, stop loss, and take profit levels
        """
        if direction == 'short':
            # Fib from manipulation peak to MSS low
            fib_high = manipulation['peak']
            fib_low = mss['close']
            
            # Entry at 50% retracement
            entry = fib_low + (fib_high - fib_low) * 0.5
            
            # Stop loss: 0.5 points above manipulation peak
            stop_loss = manipulation['peak'] + 0.5
            
            # Risk
            risk = stop_loss - entry
            
            # Take profits
            tp1 = entry - (risk * 1.0)  # 1R
            tp2 = entry - (risk * 1.5)  # 1.5R
            tp3 = entry - (risk * 2.0)  # 2R
            
        else:  # long
            # Fib from manipulation peak to MSS high
            fib_low = manipulation['peak']
            fib_high = mss['close']
            
            # Entry at 50% retracement
            entry = fib_low + (fib_high - fib_low) * 0.5
            
            # Stop loss: 0.5 points below manipulation peak
            stop_loss = manipulation['peak'] - 0.5
            
            # Risk
            risk = entry - stop_loss
            
            # Take profits
            tp1 = entry + (risk * 1.0)  # 1R
            tp2 = entry + (risk * 1.5)  # 1.5R
            tp3 = entry + (risk * 2.0)  # 2R
        
        return {
            'direction': direction,
            'entry': entry,
            'stop_loss': stop_loss,
            'risk': risk,
            'tp1': tp1,
            'tp2': tp2,
            'tp3': tp3
        }
    
    def execute_trade(self, data: pd.DataFrame, trade_setup: Dict,
                     mss_idx: int) -> Dict:
        """
        Execute trade and track outcome for each TP level.
        CRITICAL: Check if TP1 is hit BEFORE entry price is triggered (missed trade logic).
        
        Args:
            data: DataFrame with OHLC data
            trade_setup: Trade setup with entry/SL/TP levels
            mss_idx: Index where MSS was detected (start monitoring from here)
            
        Returns:
            Dictionary with trade results (can be 'Missed' if TP1 hit before entry)
        """
        direction = trade_setup['direction']
        entry = trade_setup['entry']
        stop_loss = trade_setup['stop_loss']
        tp1 = trade_setup['tp1']
        tp2 = trade_setup['tp2']
        tp3 = trade_setup['tp3']
        
        # Apply spread/slippage (0.5 points)
        if direction == 'short':
            entry = entry + 0.5  # Worse fill for short
        else:  # long
            entry = entry - 0.5  # Worse fill for long
        
        entry_triggered = False
        entry_datetime = None
        
        # Track results for each TP level
        results = {
            'TP1': None,
            'TP2': None,
            'TP3': None
        }
        
        # Monitor bar-by-bar from MSS point forward
        for i in range(mss_idx, len(data)):
            candle = data.iloc[i]
            
            if not entry_triggered:
                # CRITICAL: Check if TP1 is hit BEFORE entry
                if direction == 'short':
                    if candle['Low'] <= tp1:
                        # Missed trade: TP1 hit before entry
                        return {
                            'missed': True,
                            'missed_datetime': data.index[i],
                            'entry': entry,
                            'direction': direction
                        }
                    # Check if entry is triggered
                    if candle['High'] >= entry:
                        entry_triggered = True
                        entry_datetime = data.index[i]
                else:  # long
                    if candle['High'] >= tp1:
                        # Missed trade: TP1 hit before entry
                        return {
                            'missed': True,
                            'missed_datetime': data.index[i],
                            'entry': entry,
                            'direction': direction
                        }
                    # Check if entry is triggered
                    if candle['Low'] <= entry:
                        entry_triggered = True
                        entry_datetime = data.index[i]
            else:
                # Entry triggered, now monitor for SL/TP
                if direction == 'short':
                    # Check stop loss hit
                    if candle['High'] >= stop_loss:
                        # All TPs hit stop loss if not already closed
                        for tp_level in ['TP1', 'TP2', 'TP3']:
                            if results[tp_level] is None:
                                results[tp_level] = {
                                    'outcome': 'Loss',
                                    'exit_price': stop_loss,
                                    'exit_datetime': data.index[i],
                                    'pnl': stop_loss - entry  # Negative for loss
                                }
                        break
                    
                    # Check TP levels hit (from closest to furthest)
                    if results['TP1'] is None and candle['Low'] <= tp1:
                        results['TP1'] = {
                            'outcome': 'Win',
                            'exit_price': tp1,
                            'exit_datetime': data.index[i],
                            'pnl': entry - tp1  # Positive for win
                        }
                    
                    if results['TP2'] is None and candle['Low'] <= tp2:
                        results['TP2'] = {
                            'outcome': 'Win',
                            'exit_price': tp2,
                            'exit_datetime': data.index[i],
                            'pnl': entry - tp2
                        }
                    
                    if results['TP3'] is None and candle['Low'] <= tp3:
                        results['TP3'] = {
                            'outcome': 'Win',
                            'exit_price': tp3,
                            'exit_datetime': data.index[i],
                            'pnl': entry - tp3
                        }
                    
                    # If all TPs hit, exit
                    if all(results[tp] is not None for tp in ['TP1', 'TP2', 'TP3']):
                        break
                        
                else:  # long
                    # Check stop loss hit
                    if candle['Low'] <= stop_loss:
                        # All TPs hit stop loss if not already closed
                        for tp_level in ['TP1', 'TP2', 'TP3']:
                            if results[tp_level] is None:
                                results[tp_level] = {
                                    'outcome': 'Loss',
                                    'exit_price': stop_loss,
                                    'exit_datetime': data.index[i],
                                    'pnl': stop_loss - entry  # Negative for loss
                                }
                        break
                    
                    # Check TP levels hit
                    if results['TP1'] is None and candle['High'] >= tp1:
                        results['TP1'] = {
                            'outcome': 'Win',
                            'exit_price': tp1,
                            'exit_datetime': data.index[i],
                            'pnl': tp1 - entry
                        }
                    
                    if results['TP2'] is None and candle['High'] >= tp2:
                        results['TP2'] = {
                            'outcome': 'Win',
                            'exit_price': tp2,
                            'exit_datetime': data.index[i],
                            'pnl': tp2 - entry
                        }
                    
                    if results['TP3'] is None and candle['High'] >= tp3:
                        results['TP3'] = {
                            'outcome': 'Win',
                            'exit_price': tp3,
                            'exit_datetime': data.index[i],
                            'pnl': tp3 - entry
                        }
                    
                    # If all TPs hit, exit
                    if all(results[tp] is not None for tp in ['TP1', 'TP2', 'TP3']):
                        break
        
        # If entry never triggered, return as missed
        if not entry_triggered:
            return {
                'missed': True,
                'missed_datetime': data.index[-1],
                'entry': entry,
                'direction': direction
            }
        
        # If trade still open at end of data, mark as losses
        for tp_level in ['TP1', 'TP2', 'TP3']:
            if results[tp_level] is None:
                results[tp_level] = {
                    'outcome': 'Loss',
                    'exit_price': stop_loss,
                    'exit_datetime': data.index[-1],
                    'pnl': -(trade_setup['risk'])
                }
        
        results['entry_datetime'] = entry_datetime
        results['entry'] = entry
        results['missed'] = False
        
        return results
    
    def run_backtest(self, scan_timeframe: str = '5m', tokyo_timeframe: str = '15m',
                    years: List[int] = None):
        """
        Run complete backtest for London Reversal strategy.
        
        Args:
            scan_timeframe: Timeframe for entry scanning ('1m' or '5m')
            tokyo_timeframe: Timeframe for Tokyo range ('15m' or '1H')
            years: List of years to backtest (default: 2018-2025)
        """
        if years is None:
            years = list(range(2018, 2026))
        
        print("=" * 80)
        print("LONDON REVERSAL BACKTEST")
        print("=" * 80)
        print(f"\nConfiguration:")
        print(f"  Scan Timeframe: {scan_timeframe}")
        print(f"  Tokyo Timeframe: {tokyo_timeframe}")
        print(f"  Years: {years}")
        print(f"\nLoading data...\n")
        
        # Load data
        data = self.load_data(scan_timeframe, years)
        
        # Identify swings
        print("\nIdentifying swing points...")
        data = self.identify_swings(data, lookback=2)
        
        # Get unique dates
        dates = data.index.date
        unique_dates = sorted(set(dates))
        
        print(f"\nBacktesting {len(unique_dates)} trading days...")
        print("-" * 80)
        
        # Iterate through each day
        for date_idx, date in enumerate(unique_dates):
            # Skip first day (need previous day for Tokyo session)
            if date_idx == 0:
                continue
            
            # Progress indicator
            if date_idx % 100 == 0:
                print(f"Processing: {date} ({date_idx}/{len(unique_dates)})")
            
            # Step 1: Find Tokyo Range
            tokyo_range = self.find_tokyo_range(data, date)
            if tokyo_range is None:
                continue
            
            # Step 2: Define London Killzone (01:00 - 04:00)
            killzone_start = datetime.combine(date, time(1, 0))
            killzone_end = datetime.combine(date, time(4, 0))
            
            # Get killzone data indices
            killzone_mask = (data.index >= killzone_start) & (data.index < killzone_end)
            killzone_data_indices = data.index[killzone_mask]
            
            if len(killzone_data_indices) == 0:
                continue
            
            killzone_start_idx = data.index.get_loc(killzone_data_indices[0])
            killzone_end_idx = data.index.get_loc(killzone_data_indices[-1]) + 1
            
            # Step 3: Check for Manipulation
            manipulation = self.check_manipulation(data, tokyo_range, 
                                                   killzone_start_idx, killzone_end_idx)
            if manipulation is None:
                continue
            
            # Determine direction based on manipulation
            if manipulation['type'] == 'bearish':
                direction = 'short'
                fvg_direction = 'bearish'
            else:
                direction = 'long'
                fvg_direction = 'bullish'
            
            # Step 4: Detect FVG after manipulation
            fvg = self.detect_fvg(data, manipulation['index'], killzone_end_idx, fvg_direction)
            if fvg is None:
                continue
            
            # Step 5: Detect MSS with FVG constraint
            mss = self.detect_mss(data, fvg['index'], killzone_end_idx, direction, fvg['index'])
            if mss is None:
                continue
            
            # Step 6: Calculate entry and targets
            trade_setup = self.calculate_entry_and_targets(manipulation, mss, direction)
            
            # Add context to trade setup
            trade_setup['entry_datetime'] = data.index[mss['index']]
            trade_setup['tokyo_range'] = tokyo_range
            trade_setup['manipulation'] = manipulation
            trade_setup['fvg'] = fvg
            trade_setup['mss'] = mss
            
            # Step 7: Execute trade (with missed trade logic)
            trade_results = self.execute_trade(data, trade_setup, mss['index'])
            
            # Check if trade was missed
            if trade_results.get('missed', False):
                self.missed_trades += 1
                continue
            
            # Step 8: Record results for each TP level as separate rows
            entry_dt = trade_results['entry_datetime']
            entry_price = trade_results['entry']
            
            # Create three separate records (one for each TP level)
            for tp_level, tp_value, rr_used in [('TP1', trade_setup['tp1'], 1.0),
                                                  ('TP2', trade_setup['tp2'], 1.5),
                                                  ('TP3', trade_setup['tp3'], 2.0)]:
                result = trade_results[tp_level]
                
                trade_record = {
                    'Date': date.strftime('%Y-%m-%d'),
                    'Entry_Time': entry_dt.strftime('%H:%M:%S'),
                    'Type': 'Long' if direction == 'long' else 'Short',
                    'Entry_Price': entry_price,
                    'SL_Price': trade_setup['stop_loss'],
                    'TP_Price': tp_value,
                    'Exit_Time': result['exit_datetime'].strftime('%H:%M:%S'),
                    'Outcome': result['outcome'],
                    'PnL_Amount': result['pnl'],
                    'Risk_Reward_Used': rr_used,
                    'Entry_Hour': entry_dt.hour,
                    'Day_of_Week': entry_dt.strftime('%A'),
                    'Year': entry_dt.year,
                    'TP_Level': tp_level
                }
                
                # Add to trade log
                if self.trade_log.empty:
                    self.trade_log = pd.DataFrame([trade_record])
                else:
                    self.trade_log = pd.concat([self.trade_log, pd.DataFrame([trade_record])], ignore_index=True)
        
        print(f"\nBacktest complete! Processed {len(unique_dates)} days.")
        if not self.trade_log.empty:
            total_setups = len(self.trade_log[self.trade_log['TP_Level'] == 'TP1'])
            print(f"Total setups found: {total_setups}")
            print(f"Missed trades: {self.missed_trades}")
        else:
            print("No trades executed during backtest period.")
    
    def calculate_drawdown(self, equity_curve: pd.Series) -> Tuple[float, float]:
        """
        Calculate maximum drawdown in dollars and percentage.
        
        Args:
            equity_curve: Series of cumulative PnL
            
        Returns:
            Tuple of (max_drawdown_dollars, max_drawdown_percent)
        """
        if len(equity_curve) == 0:
            return 0.0, 0.0
        
        running_max = equity_curve.cummax()
        drawdown = equity_curve - running_max
        max_drawdown_dollars = drawdown.min()
        
        # Calculate percentage drawdown
        if max_drawdown_dollars < 0:
            # Find the index of max drawdown
            dd_idx = drawdown.idxmin()
            # Get the peak value at that point
            peak_value = running_max.loc[dd_idx]
            if peak_value > 0:
                max_drawdown_percent = (max_drawdown_dollars / peak_value) * 100
            else:
                max_drawdown_percent = 0.0
        else:
            max_drawdown_percent = 0.0
        
        return max_drawdown_dollars, abs(max_drawdown_percent)
    
    def analyze_by_year(self, tp_level: str) -> Dict:
        """
        Analyze performance by year.
        
        Args:
            tp_level: 'TP1', 'TP2', or 'TP3'
            
        Returns:
            Dictionary with year-based statistics
        """
        df = self.trade_log[self.trade_log['TP_Level'] == tp_level].copy()
        if df.empty:
            return {}
        
        year_stats = {}
        for year in sorted(df['Year'].unique()):
            year_data = df[df['Year'] == year]
            total_pnl = year_data['PnL_Amount'].sum()
            wins = len(year_data[year_data['Outcome'] == 'Win'])
            total = len(year_data)
            winrate = (wins / total * 100) if total > 0 else 0
            
            year_stats[year] = {
                'pnl': total_pnl,
                'trades': total,
                'winrate': winrate
            }
        
        return year_stats
    
    def analyze_by_weekday(self, tp_level: str) -> Dict:
        """
        Analyze performance by day of week.
        
        Args:
            tp_level: 'TP1', 'TP2', or 'TP3'
            
        Returns:
            Dictionary with weekday statistics
        """
        df = self.trade_log[self.trade_log['TP_Level'] == tp_level].copy()
        if df.empty:
            return {}
        
        weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        weekday_stats = {}
        
        for day in weekday_order:
            day_data = df[df['Day_of_Week'] == day]
            if len(day_data) > 0:
                wins = len(day_data[day_data['Outcome'] == 'Win'])
                total = len(day_data)
                winrate = (wins / total * 100) if total > 0 else 0
                
                weekday_stats[day] = {
                    'trades': total,
                    'winrate': winrate
                }
        
        return weekday_stats
    
    def analyze_by_hour(self, tp_level: str) -> Dict:
        """
        Analyze performance by entry hour.
        
        Args:
            tp_level: 'TP1', 'TP2', or 'TP3'
            
        Returns:
            Dictionary with hour-based statistics
        """
        df = self.trade_log[self.trade_log['TP_Level'] == tp_level].copy()
        if df.empty:
            return {}
        
        hour_stats = {}
        for hour in sorted(df['Entry_Hour'].unique()):
            hour_data = df[df['Entry_Hour'] == hour]
            wins = len(hour_data[hour_data['Outcome'] == 'Win'])
            total = len(hour_data)
            winrate = (wins / total * 100) if total > 0 else 0
            
            hour_stats[hour] = {
                'trades': total,
                'winrate': winrate
            }
        
        return hour_stats
    
    def generate_report(self):
        """
        Generate comprehensive backtest report with institutional-grade analytics.
        """
        print("\n" + "=" * 80)
        print("LONDON REVERSAL BACKTEST - COMPREHENSIVE REPORT")
        print("=" * 80)
        
        if self.trade_log.empty:
            print("\nNo trades executed during backtest period.")
            return
        
        total_setups = len(self.trade_log[self.trade_log['TP_Level'] == 'TP1'])
        print(f"\nTotal Setups: {total_setups}")
        print(f"Missed Trades: {self.missed_trades}")
        if total_setups + self.missed_trades > 0:
            missed_pct = (self.missed_trades / (total_setups + self.missed_trades)) * 100
            print(f"Missed Trade %: {missed_pct:.2f}%")
        
        # Analyze each TP level
        for tp_level, rr_label in [('TP1', '1R'), ('TP2', '1.5R'), ('TP3', '2R')]:
            print("\n" + "=" * 80)
            print(f"{tp_level} ({rr_label}) - GLOBAL STATISTICS")
            print("=" * 80)
            
            df = self.trade_log[self.trade_log['TP_Level'] == tp_level].copy()
            
            if df.empty:
                print("No trades for this TP level.")
                continue
            
            # Basic metrics
            total_trades = len(df)
            wins = len(df[df['Outcome'] == 'Win'])
            losses = len(df[df['Outcome'] == 'Loss'])
            winrate = (wins / total_trades * 100) if total_trades > 0 else 0
            
            # PnL metrics
            total_pnl = df['PnL_Amount'].sum()
            winning_trades = df[df['Outcome'] == 'Win']['PnL_Amount']
            losing_trades = df[df['Outcome'] == 'Loss']['PnL_Amount']
            
            avg_win = winning_trades.mean() if len(winning_trades) > 0 else 0
            avg_loss = losing_trades.mean() if len(losing_trades) > 0 else 0
            
            # Profit Factor
            sum_wins = winning_trades.sum() if len(winning_trades) > 0 else 0
            sum_losses = abs(losing_trades.sum()) if len(losing_trades) > 0 else 0
            profit_factor = (sum_wins / sum_losses) if sum_losses != 0 else float('inf')
            
            # Expectancy
            win_pct = winrate / 100
            loss_pct = 1 - win_pct
            expectancy = (win_pct * avg_win) - (loss_pct * abs(avg_loss))
            
            # Drawdown
            df_sorted = df.sort_values('Date')
            df_sorted['Cumulative_PnL'] = df_sorted['PnL_Amount'].cumsum()
            max_dd_dollars, max_dd_pct = self.calculate_drawdown(df_sorted['Cumulative_PnL'])
            
            print(f"\n  Net Profit: ${total_pnl:.2f}")
            print(f"  Profit Factor: {profit_factor:.2f}")
            print(f"  Win Rate: {winrate:.2f}%")
            print(f"  Total Trades: {total_trades}")
            print(f"  Wins: {wins} | Losses: {losses}")
            print(f"  Max Drawdown: ${max_dd_dollars:.2f} ({max_dd_pct:.2f}%)")
            print(f"  Avg Win: ${avg_win:.2f}")
            print(f"  Avg Loss: ${avg_loss:.2f}")
            print(f"  Expectancy: ${expectancy:.2f}")
            
            # Temporal Analysis
            print(f"\n  --- PnL by Year ---")
            year_stats = self.analyze_by_year(tp_level)
            for year, stats in sorted(year_stats.items()):
                print(f"    {year}: ${stats['pnl']:.2f} | {stats['trades']} trades | {stats['winrate']:.1f}% WR")
            
            print(f"\n  --- Winrate by Day of Week ---")
            weekday_stats = self.analyze_by_weekday(tp_level)
            for day, stats in weekday_stats.items():
                print(f"    {day}: {stats['winrate']:.1f}% ({stats['trades']} trades)")
            
            print(f"\n  --- Winrate by Entry Hour ---")
            hour_stats = self.analyze_by_hour(tp_level)
            for hour, stats in sorted(hour_stats.items()):
                print(f"    {hour:02d}:00: {stats['winrate']:.1f}% ({stats['trades']} trades)")
        
        print("\n" + "=" * 80)
    
    def save_results(self):
        """
        Save detailed results to three separate CSV files (one for each TP level).
        """
        if self.trade_log.empty:
            print("\nNo trades to save.")
            return
        
        print("\n" + "-" * 80)
        print("SAVING TRADE LOGS")
        print("-" * 80)
        
        # Create separate CSV for each TP level
        for tp_level, filename in [('TP1', 'london_reversal_TP1_trades.csv'),
                                     ('TP2', 'london_reversal_TP2_trades.csv'),
                                     ('TP3', 'london_reversal_TP3_trades.csv')]:
            df = self.trade_log[self.trade_log['TP_Level'] == tp_level].copy()
            
            # Drop the TP_Level column as it's redundant in individual files
            df = df.drop('TP_Level', axis=1)
            
            # Reorder columns to match specification
            columns_order = [
                'Date', 'Entry_Time', 'Type', 'Entry_Price', 'SL_Price', 'TP_Price',
                'Exit_Time', 'Outcome', 'PnL_Amount', 'Risk_Reward_Used',
                'Entry_Hour', 'Day_of_Week', 'Year'
            ]
            df = df[columns_order]
            
            filepath = os.path.join(self.data_dir, filename)
            df.to_csv(filepath, index=False)
            print(f"  {filename}: {len(df)} trades saved")
        
        print("-" * 80)
    
    def plot_equity_curve(self):
        """
        Generate equity curve visualizations for all TP levels.
        Creates individual plots and a combined comparison plot.
        """
        if self.trade_log.empty:
            print("\nNo trades to plot.")
            return
        
        print("\n" + "-" * 80)
        print("GENERATING EQUITY CURVE PLOTS")
        print("-" * 80)
        
        # Prepare data for combined plot
        fig_combined, ax_combined = plt.subplots(figsize=(14, 8))
        colors = ['#2E86AB', '#A23B72', '#F18F01']  # Blue, Purple, Orange
        
        # Plot each TP level
        for idx, (tp_level, filename, color) in enumerate([
            ('TP1', 'equity_curve_TP1.png', colors[0]),
            ('TP2', 'equity_curve_TP2.png', colors[1]),
            ('TP3', 'equity_curve_TP3.png', colors[2])
        ]):
            df = self.trade_log[self.trade_log['TP_Level'] == tp_level].copy()
            
            if df.empty:
                continue
            
            # Sort by date and time
            df = df.sort_values('Date')
            df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Entry_Time'])
            df['Cumulative_PnL'] = df['PnL_Amount'].cumsum()
            
            # Individual plot
            fig, ax = plt.subplots(figsize=(14, 8))
            ax.plot(df['Datetime'], df['Cumulative_PnL'], 
                   color=color, linewidth=2, label=f'{tp_level}')
            ax.fill_between(df['Datetime'], 0, df['Cumulative_PnL'], 
                           alpha=0.3, color=color)
            
            ax.set_xlabel('Date', fontsize=12, fontweight='bold')
            ax.set_ylabel('Cumulative PnL ($)', fontsize=12, fontweight='bold')
            ax.set_title(f'Equity Curve - {tp_level}', fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3)
            ax.axhline(y=0, color='black', linestyle='--', linewidth=1)
            
            # Format x-axis
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
            ax.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
            plt.xticks(rotation=45, ha='right')
            
            # Add statistics box
            total_pnl = df['Cumulative_PnL'].iloc[-1]
            wins = len(df[df['Outcome'] == 'Win'])
            total = len(df)
            winrate = (wins / total * 100) if total > 0 else 0
            
            stats_text = f'Total PnL: ${total_pnl:.2f}\n'
            stats_text += f'Trades: {total}\n'
            stats_text += f'Win Rate: {winrate:.1f}%'
            
            ax.text(0.02, 0.98, stats_text,
                   transform=ax.transAxes,
                   fontsize=10,
                   verticalalignment='top',
                   bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
            
            plt.tight_layout()
            filepath = os.path.join(self.data_dir, filename)
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            plt.close()
            print(f"  {filename} saved")
            
            # Add to combined plot
            ax_combined.plot(df['Datetime'], df['Cumulative_PnL'],
                           color=color, linewidth=2, label=f'{tp_level} (${total_pnl:.2f})')
        
        # Finalize combined plot
        ax_combined.set_xlabel('Date', fontsize=12, fontweight='bold')
        ax_combined.set_ylabel('Cumulative PnL ($)', fontsize=12, fontweight='bold')
        ax_combined.set_title('Equity Curve Comparison - All TP Levels', 
                             fontsize=14, fontweight='bold')
        ax_combined.grid(True, alpha=0.3)
        ax_combined.axhline(y=0, color='black', linestyle='--', linewidth=1)
        ax_combined.legend(loc='best', fontsize=10)
        
        # Format x-axis
        ax_combined.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        ax_combined.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
        plt.xticks(rotation=45, ha='right')
        
        plt.tight_layout()
        combined_filepath = os.path.join(self.data_dir, 'equity_curve_combined.png')
        plt.savefig(combined_filepath, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  equity_curve_combined.png saved")
        
        print("-" * 80)


def main():
    """
    Main execution function.
    """
    print("\n" + "=" * 80)
    print("LONDON REVERSAL STRATEGY BACKTEST")
    print("Smart Money Concepts (SMC) - Nasdaq Futures (NQ)")
    print("=" * 80)
    
    # Initialize backtest engine
    backtest = LondonReversalBacktest()
    
    # Run backtest
    # Using 5m for scanning (can change to '1m' for more precision)
    # Using 15m for Tokyo range identification
    backtest.run_backtest(
        scan_timeframe='5m',
        tokyo_timeframe='15m',
        years=list(range(2018, 2026))
    )
    
    # Generate comprehensive report
    backtest.generate_report()
    
    # Save results to CSV files
    backtest.save_results()
    
    # Plot equity curves
    backtest.plot_equity_curve()
    
    print("\n" + "=" * 80)
    print("BACKTEST COMPLETE")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()

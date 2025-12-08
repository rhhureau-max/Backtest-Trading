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
        self.trades = []
        self.results = {
            'TP1_1R': {'trades': [], 'wins': 0, 'losses': 0, 'total_pnl': 0},
            'TP2_1.5R': {'trades': [], 'wins': 0, 'losses': 0, 'total_pnl': 0},
            'TP3_2R': {'trades': [], 'wins': 0, 'losses': 0, 'total_pnl': 0}
        }
        
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
                     entry_idx: int) -> Dict:
        """
        Execute trade and track outcome for each TP level.
        
        Args:
            data: DataFrame with OHLC data
            trade_setup: Trade setup with entry/SL/TP levels
            entry_idx: Index where trade is entered
            
        Returns:
            Dictionary with trade results
        """
        direction = trade_setup['direction']
        entry = trade_setup['entry']
        stop_loss = trade_setup['stop_loss']
        tp1 = trade_setup['tp1']
        tp2 = trade_setup['tp2']
        tp3 = trade_setup['tp3']
        
        # Track results for each TP level
        results = {
            'TP1': None,
            'TP2': None,
            'TP3': None
        }
        
        # Simulate from entry point forward
        for i in range(entry_idx, len(data)):
            candle = data.iloc[i]
            
            if direction == 'short':
                # Check stop loss hit
                if candle['High'] >= stop_loss:
                    # All TPs hit stop loss if not already closed
                    for tp_level in ['TP1', 'TP2', 'TP3']:
                        if results[tp_level] is None:
                            results[tp_level] = {
                                'outcome': 'loss',
                                'exit_price': stop_loss,
                                'exit_datetime': data.index[i],
                                'pnl': stop_loss - entry  # Negative for loss
                            }
                    break
                
                # Check TP levels hit (from closest to furthest)
                if results['TP1'] is None and candle['Low'] <= tp1:
                    results['TP1'] = {
                        'outcome': 'win',
                        'exit_price': tp1,
                        'exit_datetime': data.index[i],
                        'pnl': entry - tp1  # Positive for win
                    }
                
                if results['TP2'] is None and candle['Low'] <= tp2:
                    results['TP2'] = {
                        'outcome': 'win',
                        'exit_price': tp2,
                        'exit_datetime': data.index[i],
                        'pnl': entry - tp2
                    }
                
                if results['TP3'] is None and candle['Low'] <= tp3:
                    results['TP3'] = {
                        'outcome': 'win',
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
                                'outcome': 'loss',
                                'exit_price': stop_loss,
                                'exit_datetime': data.index[i],
                                'pnl': stop_loss - entry  # Negative for loss
                            }
                    break
                
                # Check TP levels hit
                if results['TP1'] is None and candle['High'] >= tp1:
                    results['TP1'] = {
                        'outcome': 'win',
                        'exit_price': tp1,
                        'exit_datetime': data.index[i],
                        'pnl': tp1 - entry
                    }
                
                if results['TP2'] is None and candle['High'] >= tp2:
                    results['TP2'] = {
                        'outcome': 'win',
                        'exit_price': tp2,
                        'exit_datetime': data.index[i],
                        'pnl': tp2 - entry
                    }
                
                if results['TP3'] is None and candle['High'] >= tp3:
                    results['TP3'] = {
                        'outcome': 'win',
                        'exit_price': tp3,
                        'exit_datetime': data.index[i],
                        'pnl': tp3 - entry
                    }
                
                # If all TPs hit, exit
                if all(results[tp] is not None for tp in ['TP1', 'TP2', 'TP3']):
                    break
        
        # If trade still open at end of data, mark as losses
        for tp_level in ['TP1', 'TP2', 'TP3']:
            if results[tp_level] is None:
                results[tp_level] = {
                    'outcome': 'loss',
                    'exit_price': stop_loss,
                    'exit_datetime': data.index[-1],
                    'pnl': -(trade_setup['risk'])
                }
        
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
            
            # Step 7: Execute trade
            trade_results = self.execute_trade(data, trade_setup, mss['index'])
            
            # Step 8: Record results
            trade_record = {
                'date': date,
                'direction': direction,
                'entry_datetime': trade_setup['entry_datetime'],
                'entry': trade_setup['entry'],
                'stop_loss': trade_setup['stop_loss'],
                'risk': trade_setup['risk'],
                'tp1': trade_setup['tp1'],
                'tp2': trade_setup['tp2'],
                'tp3': trade_setup['tp3'],
                'tokyo_high': tokyo_range['high'],
                'tokyo_low': tokyo_range['low'],
                'manipulation_type': manipulation['type'],
                'manipulation_peak': manipulation['peak'],
                'fvg_datetime': fvg['datetime'],
                'mss_datetime': mss['datetime'],
            }
            
            # Add results for each TP level
            for tp_level, result in trade_results.items():
                trade_record[f'{tp_level}_outcome'] = result['outcome']
                trade_record[f'{tp_level}_exit_price'] = result['exit_price']
                trade_record[f'{tp_level}_exit_datetime'] = result['exit_datetime']
                trade_record[f'{tp_level}_pnl'] = result['pnl']
                
                # Update statistics
                if tp_level == 'TP1':
                    key = 'TP1_1R'
                elif tp_level == 'TP2':
                    key = 'TP2_1.5R'
                else:
                    key = 'TP3_2R'
                
                self.results[key]['trades'].append(trade_record)
                if result['outcome'] == 'win':
                    self.results[key]['wins'] += 1
                else:
                    self.results[key]['losses'] += 1
                self.results[key]['total_pnl'] += result['pnl']
            
            self.trades.append(trade_record)
        
        print(f"\nBacktest complete! Processed {len(unique_dates)} days.")
        print(f"Total setups found: {len(self.trades)}")
    
    def generate_report(self):
        """
        Generate comprehensive backtest report.
        """
        print("\n" + "=" * 80)
        print("BACKTEST RESULTS SUMMARY")
        print("=" * 80)
        
        if len(self.trades) == 0:
            print("\nNo trades executed during backtest period.")
            return
        
        print(f"\nTotal Setups: {len(self.trades)}")
        print("\n" + "-" * 80)
        
        # Results for each TP level
        for tp_name, results in self.results.items():
            total_trades = results['wins'] + results['losses']
            if total_trades == 0:
                continue
            
            winrate = (results['wins'] / total_trades) * 100
            avg_pnl = results['total_pnl'] / total_trades
            
            print(f"\n{tp_name} Results:")
            print(f"  Total Trades: {total_trades}")
            print(f"  Wins: {results['wins']}")
            print(f"  Losses: {results['losses']}")
            print(f"  Win Rate: {winrate:.2f}%")
            print(f"  Total PnL: {results['total_pnl']:.2f} points")
            print(f"  Average PnL per Trade: {avg_pnl:.2f} points")
            
            # Calculate additional metrics
            if results['wins'] > 0:
                winning_trades = [t for t in results['trades'] 
                                if t[f"{tp_name.split('_')[0]}_outcome"] == 'win']
                avg_win = sum([t[f"{tp_name.split('_')[0]}_pnl"] 
                             for t in winning_trades]) / results['wins']
            else:
                avg_win = 0
            
            if results['losses'] > 0:
                losing_trades = [t for t in results['trades'] 
                               if t[f"{tp_name.split('_')[0]}_outcome"] == 'loss']
                avg_loss = sum([t[f"{tp_name.split('_')[0]}_pnl"] 
                              for t in losing_trades]) / results['losses']
            else:
                avg_loss = 0
            
            print(f"  Average Win: {avg_win:.2f} points")
            print(f"  Average Loss: {avg_loss:.2f} points")
            
            if avg_loss != 0:
                profit_factor = abs(avg_win * results['wins']) / abs(avg_loss * results['losses'])
                print(f"  Profit Factor: {profit_factor:.2f}")
        
        print("\n" + "=" * 80)
    
    def save_results(self, filename: str = "london_reversal_results.csv"):
        """
        Save detailed results to CSV file.
        
        Args:
            filename: Output filename
        """
        if len(self.trades) == 0:
            print("No trades to save.")
            return
        
        filepath = os.path.join(self.data_dir, filename)
        df = pd.DataFrame(self.trades)
        df.to_csv(filepath, index=False)
        print(f"\nResults saved to: {filepath}")
        print(f"Total records: {len(df)}")


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
    
    # Generate report
    backtest.generate_report()
    
    # Save results
    backtest.save_results("london_reversal_results.csv")
    
    print("\n" + "=" * 80)
    print("BACKTEST COMPLETE")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
SMT (Smart Money Technique) Divergence Detector

This script analyzes NQ (NASDAQ) and ES (S&P 500) trading data to detect
SMT divergences during London and New York AM trading sessions.

SMT Divergence occurs when:
- Bullish SMT: One asset makes Lower Low (LL) while other makes Higher Low (HL)
  → The asset with HL is the bullish leader (stronger/refuses to go lower)
- Bearish SMT: One asset makes Higher High (HH) while other makes Lower High (LH)
  → The asset with LH is the bearish leader (weaker/refuses to go higher)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import argrelextrema
from datetime import datetime, time
import os
from typing import Tuple, List, Dict
import warnings
warnings.filterwarnings('ignore')


class SMTDivergenceDetector:
    """Detects SMT divergences between NQ and ES futures."""
    
    # Configuration for ES file patterns by timeframe
    ES_FILE_PATTERNS = {
        '5m': {
            'ranges': [
                (2018, 2020, "2018-2020"),
                (2021, 2023, "2021-2023"),
                (2024, 2025, "2024-2025")
            ]
        },
        '15m': {
            'ranges': [(2018, 2025, "2018-2025")]
        }
    }
    
    def __init__(self, base_path: str = "."):
        """
        Initialize the detector.
        
        Args:
            base_path: Base directory containing CSV files
        """
        self.base_path = base_path
        self.london_session = (time(2, 0), time(5, 0))  # 02:00-05:00 Chicago time
        self.ny_session = (time(8, 30), time(11, 0))    # 08:30-11:00 Chicago time
        
    def load_data(self, filepath: str) -> pd.DataFrame:
        """
        Load OHLC data from CSV file.
        
        Args:
            filepath: Path to CSV file
            
        Returns:
            DataFrame with datetime index and OHLC columns
        """
        # Read CSV with semicolon delimiter
        df = pd.read_csv(
            filepath,
            sep=';',
            parse_dates=False,
            dayfirst=True
        )
        
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
        
        # Set datetime as index and select relevant columns
        df = df.set_index('datetime')[['Open', 'High', 'Low', 'Close', 'Volume']]
        
        # Convert to numeric
        for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        return df.dropna()
    
    def load_nq_data(self, year: int, timeframe: str) -> pd.DataFrame:
        """Load NQ data for a specific year and timeframe."""
        filepath = os.path.join(self.base_path, f"{year} {timeframe}.csv")
        if os.path.exists(filepath):
            return self.load_data(filepath)
        return pd.DataFrame()
    
    def load_es_data(self, year_range: str, timeframe: str) -> pd.DataFrame:
        """Load ES data for a year range and timeframe."""
        filepath = os.path.join(self.base_path, f"ES {timeframe} ({year_range}).csv")
        if os.path.exists(filepath):
            return self.load_data(filepath)
        return pd.DataFrame()
    
    def _get_es_year_ranges(self, year: int, timeframe: str) -> List[str]:
        """
        Get appropriate ES file year ranges for a given year and timeframe.
        
        Args:
            year: Year to find data for
            timeframe: Timeframe (e.g., '5m', '15m')
            
        Returns:
            List of year range strings to try
        """
        if timeframe not in self.ES_FILE_PATTERNS:
            # Default to widest range for unknown timeframes
            return ["2018-2025"]
        
        ranges = self.ES_FILE_PATTERNS[timeframe]['ranges']
        year_ranges = []
        
        # Find matching range for the year
        for start_year, end_year, range_str in ranges:
            if start_year <= year <= end_year:
                year_ranges.append(range_str)
        
        # If no match found, try all ranges
        if not year_ranges:
            year_ranges = [range_str for _, _, range_str in ranges]
        
        return year_ranges
    
    def _get_fallback_year_ranges(self, year: int) -> List[str]:
        """
        Generate fallback year range patterns dynamically.
        
        Args:
            year: Year to generate fallback patterns for
            
        Returns:
            List of fallback year range strings
        """
        return [
            f"{year}-{year+1}",     # Adjacent year
            f"{year-1}-{year+1}",   # Surrounding years
            f"{year-2}-{year+2}",   # Extended range
        ]
    
    def filter_session(self, df: pd.DataFrame, session_name: str) -> pd.DataFrame:
        """
        Filter dataframe to specific trading session.
        
        Args:
            df: DataFrame with datetime index
            session_name: 'london' or 'ny'
            
        Returns:
            Filtered DataFrame
        """
        if session_name.lower() == 'london':
            start_time, end_time = self.london_session
        elif session_name.lower() == 'ny':
            start_time, end_time = self.ny_session
        else:
            raise ValueError("session_name must be 'london' or 'ny'")
        
        # Filter by time of day
        mask = (df.index.time >= start_time) & (df.index.time < end_time)
        return df[mask].copy()
    
    def find_swing_points(self, df: pd.DataFrame, order: int = 5) -> Tuple[pd.Series, pd.Series]:
        """
        Find swing highs and swing lows using local extrema.
        
        Args:
            df: DataFrame with OHLC data
            order: Number of candles on each side to compare (default: 5)
            
        Returns:
            Tuple of (swing_highs, swing_lows) as Series with datetime index
        """
        # Find local maxima (swing highs) using High prices
        high_indices = argrelextrema(df['High'].values, np.greater_equal, order=order)[0]
        swing_highs = pd.Series(df['High'].iloc[high_indices].values, 
                               index=df.index[high_indices])
        
        # Find local minima (swing lows) using Low prices
        low_indices = argrelextrema(df['Low'].values, np.less_equal, order=order)[0]
        swing_lows = pd.Series(df['Low'].iloc[low_indices].values,
                              index=df.index[low_indices])
        
        return swing_highs, swing_lows
    
    def align_swings(self, swings1: pd.Series, swings2: pd.Series, 
                    tolerance_minutes: int = 10) -> List[Tuple[datetime, float, float]]:
        """
        Align swing points between two assets within a time tolerance.
        
        Args:
            swings1: Swing points for asset 1
            swings2: Swing points for asset 2
            tolerance_minutes: Time tolerance in minutes (default: 10)
            
        Returns:
            List of tuples (timestamp, value1, value2) for aligned swings
        """
        aligned = []
        tolerance = pd.Timedelta(minutes=tolerance_minutes)
        
        for ts1, val1 in swings1.items():
            # Find closest swing in asset 2 within tolerance
            time_diffs = abs(swings2.index - ts1)
            if len(time_diffs) > 0:
                min_diff_idx = time_diffs.argmin()
                min_diff = time_diffs[min_diff_idx]
                
                if min_diff <= tolerance:
                    ts2 = swings2.index[min_diff_idx]
                    val2 = swings2.iloc[min_diff_idx]
                    aligned.append((ts1, val1, val2))
        
        return aligned
    
    def detect_divergence_type(self, prev_val: float, curr_val: float,
                              prev_val_other: float, curr_val_other: float,
                              is_high: bool) -> Dict:
        """
        Detect if there's an SMT divergence between two aligned swing points.
        
        Args:
            prev_val: Previous swing value for asset 1
            curr_val: Current swing value for asset 1
            prev_val_other: Previous swing value for asset 2
            curr_val_other: Current swing value for asset 2
            is_high: True if analyzing highs, False if analyzing lows
            
        Returns:
            Dict with divergence info or None if no divergence
        """
        if is_high:
            # Analyzing swing highs for bearish divergence
            asset1_direction = "HH" if curr_val > prev_val else "LH" if curr_val < prev_val else "EH"
            asset2_direction = "HH" if curr_val_other > prev_val_other else "LH" if curr_val_other < prev_val_other else "EH"
            
            # Bearish SMT: One makes HH, other makes LH
            if asset1_direction == "HH" and asset2_direction == "LH":
                return {
                    'type': 'bearish',
                    'leader': 'asset2',  # Asset 2 is weaker (refuses to go higher)
                    'asset1_dir': asset1_direction,
                    'asset2_dir': asset2_direction
                }
            elif asset1_direction == "LH" and asset2_direction == "HH":
                return {
                    'type': 'bearish',
                    'leader': 'asset1',  # Asset 1 is weaker (refuses to go higher)
                    'asset1_dir': asset1_direction,
                    'asset2_dir': asset2_direction
                }
        else:
            # Analyzing swing lows for bullish divergence
            asset1_direction = "LL" if curr_val < prev_val else "HL" if curr_val > prev_val else "EL"
            asset2_direction = "LL" if curr_val_other < prev_val_other else "HL" if curr_val_other > prev_val_other else "EL"
            
            # Bullish SMT: One makes LL, other makes HL
            if asset1_direction == "LL" and asset2_direction == "HL":
                return {
                    'type': 'bullish',
                    'leader': 'asset2',  # Asset 2 is stronger (refuses to go lower)
                    'asset1_dir': asset1_direction,
                    'asset2_dir': asset2_direction
                }
            elif asset1_direction == "HL" and asset2_direction == "LL":
                return {
                    'type': 'bullish',
                    'leader': 'asset1',  # Asset 1 is stronger (refuses to go lower)
                    'asset1_dir': asset1_direction,
                    'asset2_dir': asset2_direction
                }
        
        return None
    
    def detect_smt_divergences(self, nq_highs: pd.Series, nq_lows: pd.Series,
                              es_highs: pd.Series, es_lows: pd.Series) -> List[Dict]:
        """
        Detect SMT divergences between NQ and ES.
        
        Returns:
            List of divergence dictionaries
        """
        divergences = []
        
        # Align swing highs for bearish divergence detection
        aligned_highs = self.align_swings(nq_highs, es_highs)
        
        # Detect bearish divergences (comparing consecutive swing highs)
        for i in range(1, len(aligned_highs)):
            prev_ts, prev_nq, prev_es = aligned_highs[i-1]
            curr_ts, curr_nq, curr_es = aligned_highs[i]
            
            div = self.detect_divergence_type(prev_nq, curr_nq, prev_es, curr_es, is_high=True)
            
            if div:
                divergences.append({
                    'timestamp': curr_ts,
                    'prev_timestamp': prev_ts,
                    'type': div['type'],
                    'leader': 'NQ' if div['leader'] == 'asset1' else 'ES',
                    'nq_prev': prev_nq,
                    'nq_curr': curr_nq,
                    'es_prev': prev_es,
                    'es_curr': curr_es,
                    'nq_direction': div['asset1_dir'],
                    'es_direction': div['asset2_dir'],
                    'swing_type': 'high'
                })
        
        # Align swing lows for bullish divergence detection
        aligned_lows = self.align_swings(nq_lows, es_lows)
        
        # Detect bullish divergences (comparing consecutive swing lows)
        for i in range(1, len(aligned_lows)):
            prev_ts, prev_nq, prev_es = aligned_lows[i-1]
            curr_ts, curr_nq, curr_es = aligned_lows[i]
            
            div = self.detect_divergence_type(prev_nq, curr_nq, prev_es, curr_es, is_high=False)
            
            if div:
                divergences.append({
                    'timestamp': curr_ts,
                    'prev_timestamp': prev_ts,
                    'type': div['type'],
                    'leader': 'NQ' if div['leader'] == 'asset1' else 'ES',
                    'nq_prev': prev_nq,
                    'nq_curr': curr_nq,
                    'es_prev': prev_es,
                    'es_curr': curr_es,
                    'nq_direction': div['asset1_dir'],
                    'es_direction': div['asset2_dir'],
                    'swing_type': 'low'
                })
        
        return divergences
    
    def analyze_session(self, nq_df: pd.DataFrame, es_df: pd.DataFrame,
                       session_name: str) -> Tuple[List[Dict], pd.DataFrame, pd.DataFrame]:
        """
        Analyze a specific session for SMT divergences.
        
        Returns:
            Tuple of (divergences, filtered_nq, filtered_es)
        """
        # Filter to session times
        nq_session = self.filter_session(nq_df, session_name)
        es_session = self.filter_session(es_df, session_name)
        
        if len(nq_session) == 0 or len(es_session) == 0:
            return [], nq_session, es_session
        
        # Find swing points
        nq_highs, nq_lows = self.find_swing_points(nq_session)
        es_highs, es_lows = self.find_swing_points(es_session)
        
        # Detect divergences
        divergences = self.detect_smt_divergences(nq_highs, nq_lows, es_highs, es_lows)
        
        # Add session info
        for div in divergences:
            div['session'] = session_name
        
        return divergences, nq_session, es_session
    
    def backtest_divergence(self, divergence: Dict, full_df: pd.DataFrame) -> Dict:
        """
        Backtest a single divergence to determine if it would have been a winning trade.
        
        For Bullish SMT:
        - Entry: At the close of the candle that confirms the 2nd swing low
        - Target: Highest high between the two swing lows
        - Stop: Below the 2nd swing low
        
        For Bearish SMT:
        - Entry: At the close of the candle that confirms the 2nd swing high
        - Target: Lowest low between the two swing highs
        - Stop: Above the 2nd swing high
        
        Args:
            divergence: Divergence dictionary
            full_df: Full dataframe with OHLC data for the leader asset
            
        Returns:
            Dict with backtest results
        """
        result = {
            'outcome': 'unknown',  # 'win', 'loss', or 'unknown'
            'target': None,
            'stop': None,
            'entry': None
        }
        
        try:
            # Get timestamps
            prev_ts = divergence['prev_timestamp']
            curr_ts = divergence['timestamp']
            
            # Determine which asset is the leader and get its values
            if divergence['leader'] == 'NQ':
                prev_price = divergence['nq_prev']
                curr_price = divergence['nq_curr']
            else:  # ES
                prev_price = divergence['es_prev']
                curr_price = divergence['es_curr']
            
            # Get data between the two swing points
            mask = (full_df.index > prev_ts) & (full_df.index < curr_ts)
            between_data = full_df[mask]
            
            if len(between_data) == 0:
                return result
            
            # Calculate target and stop based on divergence type
            if divergence['type'] == 'bullish':
                # For bullish: target is highest high between swings, stop is below curr swing low
                target = between_data['High'].max()
                stop = curr_price
                entry = curr_price
                
            else:  # bearish
                # For bearish: target is lowest low between swings, stop is above curr swing high
                target = between_data['Low'].min()
                stop = curr_price
                entry = curr_price
            
            result['target'] = target
            result['stop'] = stop
            result['entry'] = entry
            
            # Get future data after the divergence
            future_mask = full_df.index > curr_ts
            future_data = full_df[future_mask]
            
            if len(future_data) == 0:
                return result
            
            # Check each future candle to see if target or stop is hit first
            for idx, row in future_data.iterrows():
                if divergence['type'] == 'bullish':
                    # Check if target (high) is reached
                    if row['High'] >= target:
                        result['outcome'] = 'win'
                        break
                    # Check if stop (low below entry) is hit
                    if row['Low'] <= stop:
                        result['outcome'] = 'loss'
                        break
                        
                else:  # bearish
                    # Check if target (low) is reached
                    if row['Low'] <= target:
                        result['outcome'] = 'win'
                        break
                    # Check if stop (high above entry) is hit
                    if row['High'] >= stop:
                        result['outcome'] = 'loss'
                        break
            
        except Exception as e:
            # If any error occurs, mark as unknown
            pass
        
        return result
    
    def find_fvgs(self, df: pd.DataFrame, fvg_type: str = 'bullish', include_candle1: bool = False) -> List[Tuple]:
        """
        Find Fair Value Gaps (FVGs) in the data.
        
        Args:
            df: DataFrame with OHLC data
            fvg_type: 'bullish' or 'bearish'
            include_candle1: If True, include candle1 high/low in the tuple
            
        Returns:
            List of tuples (timestamp, fvg_high, fvg_low) or 
            (timestamp, fvg_high, fvg_low, candle1_high, candle1_low) if include_candle1=True
        """
        fvgs = []
        
        if len(df) < 3:
            return fvgs
        
        df_list = df.reset_index()
        
        for i in range(len(df_list) - 2):
            candle1 = df_list.iloc[i]
            candle2 = df_list.iloc[i + 1]  # Middle candle (not used in gap detection)
            candle3 = df_list.iloc[i + 2]
            
            if fvg_type == 'bullish':
                # Bullish FVG: candle1.High < candle3.Low
                if candle1['High'] < candle3['Low']:
                    fvg_high = candle3['Low']
                    fvg_low = candle1['High']
                    timestamp = candle3['datetime'] if 'datetime' in candle3 else candle3.name
                    if include_candle1:
                        fvgs.append((timestamp, fvg_high, fvg_low, candle1['High'], candle1['Low']))
                    else:
                        fvgs.append((timestamp, fvg_high, fvg_low))
                    
            else:  # bearish
                # Bearish FVG: candle1.Low > candle3.High
                if candle1['Low'] > candle3['High']:
                    fvg_low = candle3['High']
                    fvg_high = candle1['Low']
                    timestamp = candle3['datetime'] if 'datetime' in candle3 else candle3.name
                    if include_candle1:
                        fvgs.append((timestamp, fvg_high, fvg_low, candle1['High'], candle1['Low']))
                    else:
                        fvgs.append((timestamp, fvg_high, fvg_low))
        
        return fvgs
    
    def backtest_divergence_with_fvg(self, divergence: Dict, full_df: pd.DataFrame) -> Dict:
        """
        Backtest a divergence with FVG breakout confirmation.
        
        For Bullish SMT:
        - Find the last Bearish FVG before the swing low
        - Wait for price to close above the FVG high
        - Entry: At that close
        - Stop: 1 point below the swing low
        - Target: Highest high between swings
        
        For Bearish SMT:
        - Find the last Bullish FVG before the swing high
        - Wait for price to close below the FVG low
        - Entry: At that close
        - Stop: 1 point above the swing high
        - Target: Lowest low between swings
        
        Args:
            divergence: Divergence dictionary
            full_df: Full dataframe with OHLC data for the leader asset
            
        Returns:
            Dict with backtest results including entry price and R:R
        """
        result = {
            'outcome': 'no_trade',  # 'win', 'loss', 'no_trade'
            'target': None,
            'stop': None,
            'entry': None,
            'entry_timestamp': None,
            'risk': None,
            'reward': None,
            'rr_ratio': None
        }
        
        try:
            # Get timestamps
            prev_ts = divergence['prev_timestamp']
            curr_ts = divergence['timestamp']
            
            # Determine which asset is the leader and get its values
            if divergence['leader'] == 'NQ':
                prev_price = divergence['nq_prev']
                curr_price = divergence['nq_curr']
            else:  # ES
                prev_price = divergence['es_prev']
                curr_price = divergence['es_curr']
            
            # Get data between the two swing points
            mask = (full_df.index > prev_ts) & (full_df.index < curr_ts)
            between_data = full_df[mask]
            
            if len(between_data) == 0:
                return result
            
            # Calculate target based on divergence type
            if divergence['type'] == 'bullish':
                target = between_data['High'].max()
                stop = curr_price - 1  # 1 point below swing low
                
                # Find Bearish FVGs before the swing low
                data_before_swing = full_df[full_df.index <= curr_ts]
                # Look back a reasonable window (e.g., last 100 candles before swing)
                lookback_start = max(0, len(data_before_swing) - 100)
                data_to_check = data_before_swing.iloc[lookback_start:]
                
                fvgs = self.find_fvgs(data_to_check, fvg_type='bearish')
                
                if len(fvgs) == 0:
                    return result
                
                # Get the last FVG before the swing
                last_fvg = fvgs[-1]
                fvg_ts, fvg_high, fvg_low = last_fvg
                
                # Now look for price to close above FVG high after the divergence
                future_mask = full_df.index > curr_ts
                future_data = full_df[future_mask]
                
                entry_found = False
                for idx, row in future_data.iterrows():
                    # Check if stop is hit before entry
                    if row['Low'] <= stop:
                        result['outcome'] = 'no_trade'
                        return result
                    
                    # Check for FVG breakout (close above FVG high)
                    if row['Close'] > fvg_high:
                        entry_found = True
                        result['entry'] = row['Close']
                        result['entry_timestamp'] = idx
                        result['stop'] = stop
                        result['target'] = target
                        break
                
                if not entry_found:
                    return result
                
                # Calculate risk/reward
                result['risk'] = result['entry'] - result['stop']
                result['reward'] = result['target'] - result['entry']
                if result['risk'] > 0:
                    result['rr_ratio'] = result['reward'] / result['risk']
                
                # Continue from entry point to check if target or stop is hit
                entry_idx = future_data.index.get_loc(result['entry_timestamp'])
                remaining_data = future_data.iloc[entry_idx + 1:]
                
                for idx, row in remaining_data.iterrows():
                    # Check if target is reached
                    if row['High'] >= target:
                        result['outcome'] = 'win'
                        break
                    # Check if stop is hit
                    if row['Low'] <= stop:
                        result['outcome'] = 'loss'
                        break
                        
            else:  # bearish
                target = between_data['Low'].min()
                stop = curr_price + 1  # 1 point above swing high
                
                # Find Bullish FVGs before the swing high
                data_before_swing = full_df[full_df.index <= curr_ts]
                # Look back a reasonable window
                lookback_start = max(0, len(data_before_swing) - 100)
                data_to_check = data_before_swing.iloc[lookback_start:]
                
                fvgs = self.find_fvgs(data_to_check, fvg_type='bullish')
                
                if len(fvgs) == 0:
                    return result
                
                # Get the last FVG before the swing
                last_fvg = fvgs[-1]
                fvg_ts, fvg_high, fvg_low = last_fvg
                
                # Now look for price to close below FVG low after the divergence
                future_mask = full_df.index > curr_ts
                future_data = full_df[future_mask]
                
                entry_found = False
                for idx, row in future_data.iterrows():
                    # Check if stop is hit before entry
                    if row['High'] >= stop:
                        result['outcome'] = 'no_trade'
                        return result
                    
                    # Check for FVG breakout (close below FVG low)
                    if row['Close'] < fvg_low:
                        entry_found = True
                        result['entry'] = row['Close']
                        result['entry_timestamp'] = idx
                        result['stop'] = stop
                        result['target'] = target
                        break
                
                if not entry_found:
                    return result
                
                # Calculate risk/reward
                result['risk'] = result['stop'] - result['entry']
                result['reward'] = result['entry'] - result['target']
                if result['risk'] > 0:
                    result['rr_ratio'] = result['reward'] / result['risk']
                
                # Continue from entry point to check if target or stop is hit
                entry_idx = future_data.index.get_loc(result['entry_timestamp'])
                remaining_data = future_data.iloc[entry_idx + 1:]
                
                for idx, row in remaining_data.iterrows():
                    # Check if target is reached
                    if row['Low'] <= target:
                        result['outcome'] = 'win'
                        break
                    # Check if stop is hit
                    if row['High'] >= stop:
                        result['outcome'] = 'loss'
                        break
            
        except Exception as e:
            # If any error occurs, mark as no_trade
            result['outcome'] = 'no_trade'
        
        return result
    
    def backtest_divergence_with_fvg_multi_sl(self, divergence: Dict, full_df: pd.DataFrame) -> Dict:
        """
        Backtest a divergence with FVG confirmation using THREE different stop loss strategies:
        1. Structural SL: At the swing point (safest, widest)
        2. FVG Invalidation SL: At candle1 of the FVG (standard)
        3. Signal Candle SL: At the entry candle high/low (aggressive, tightest)
        
        Args:
            divergence: Divergence dictionary
            full_df: Full dataframe with OHLC data for the leader asset
            
        Returns:
            Dict with backtest results for all three SL strategies
        """
        result = {
            'structural_outcome': 'no_trade',
            'structural_stop': None,
            'structural_risk': None,
            'structural_reward': None,
            'structural_rr': None,
            'fvg_inv_outcome': 'no_trade',
            'fvg_inv_stop': None,
            'fvg_inv_risk': None,
            'fvg_inv_reward': None,
            'fvg_inv_rr': None,
            'signal_outcome': 'no_trade',
            'signal_stop': None,
            'signal_risk': None,
            'signal_reward': None,
            'signal_rr': None,
            'entry': None,
            'entry_timestamp': None,
            'target': None
        }
        
        try:
            # Get timestamps
            prev_ts = divergence['prev_timestamp']
            curr_ts = divergence['timestamp']
            
            # Determine which asset is the leader and get its values
            if divergence['leader'] == 'NQ':
                prev_price = divergence['nq_prev']
                curr_price = divergence['nq_curr']
            else:  # ES
                prev_price = divergence['es_prev']
                curr_price = divergence['es_curr']
            
            # Get data between the two swing points
            mask = (full_df.index > prev_ts) & (full_df.index < curr_ts)
            between_data = full_df[mask]
            
            if len(between_data) == 0:
                return result
            
            # Calculate target based on divergence type
            if divergence['type'] == 'bullish':
                target = between_data['High'].max()
                
                # Find Bearish FVGs before the swing low (with candle1 info)
                data_before_swing = full_df[full_df.index <= curr_ts]
                lookback_start = max(0, len(data_before_swing) - 100)
                data_to_check = data_before_swing.iloc[lookback_start:]
                
                fvgs = self.find_fvgs(data_to_check, fvg_type='bearish', include_candle1=True)
                
                if len(fvgs) == 0:
                    return result
                
                # Get the last FVG before the swing
                last_fvg = fvgs[-1]
                fvg_ts, fvg_high, fvg_low, candle1_high, candle1_low = last_fvg
                
                # Define the three stop loss levels (with 1 point buffer)
                structural_sl = curr_price - 1  # Below swing low
                fvg_inv_sl = candle1_low - 1    # Below candle1 low (FVG invalidation)
                
                # Now look for price to close above FVG high after the divergence
                future_mask = full_df.index > curr_ts
                future_data = full_df[future_mask]
                
                entry_found = False
                entry_price = None
                entry_ts = None
                signal_candle_low = None
                
                for idx, row in future_data.iterrows():
                    # Check if structural stop is hit before entry
                    if row['Low'] <= structural_sl:
                        return result
                    
                    # Check for FVG breakout (close above FVG high)
                    if row['Close'] > fvg_high:
                        entry_found = True
                        entry_price = row['Close']
                        entry_ts = idx
                        signal_candle_low = row['Low']  # For signal candle SL
                        break
                
                if not entry_found:
                    return result
                
                # Calculate signal candle SL (1 point below signal candle low)
                signal_sl = signal_candle_low - 1
                
                # Store common info
                result['entry'] = entry_price
                result['entry_timestamp'] = entry_ts
                result['target'] = target
                
                # Calculate risks and rewards for each SL
                result['structural_stop'] = structural_sl
                result['structural_risk'] = entry_price - structural_sl
                result['structural_reward'] = target - entry_price
                if result['structural_risk'] > 0:
                    result['structural_rr'] = result['structural_reward'] / result['structural_risk']
                
                result['fvg_inv_stop'] = fvg_inv_sl
                result['fvg_inv_risk'] = entry_price - fvg_inv_sl
                result['fvg_inv_reward'] = target - entry_price
                if result['fvg_inv_risk'] > 0:
                    result['fvg_inv_rr'] = result['fvg_inv_reward'] / result['fvg_inv_risk']
                
                result['signal_stop'] = signal_sl
                result['signal_risk'] = entry_price - signal_sl
                result['signal_reward'] = target - entry_price
                if result['signal_risk'] > 0:
                    result['signal_rr'] = result['signal_reward'] / result['signal_risk']
                
                # Continue from entry point to check outcomes for each SL
                entry_idx = future_data.index.get_loc(entry_ts)
                remaining_data = future_data.iloc[entry_idx + 1:]
                
                # Track outcomes separately for each SL
                structural_hit = False
                fvg_inv_hit = False
                signal_hit = False
                
                for idx, row in remaining_data.iterrows():
                    # Check if target is reached first
                    if row['High'] >= target:
                        # All remaining SLs that haven't been hit are wins
                        if not structural_hit:
                            result['structural_outcome'] = 'win'
                        if not fvg_inv_hit:
                            result['fvg_inv_outcome'] = 'win'
                        if not signal_hit:
                            result['signal_outcome'] = 'win'
                        break
                    
                    # Check each SL independently
                    if not structural_hit and row['Low'] <= structural_sl:
                        result['structural_outcome'] = 'loss'
                        structural_hit = True
                    
                    if not fvg_inv_hit and row['Low'] <= fvg_inv_sl:
                        result['fvg_inv_outcome'] = 'loss'
                        fvg_inv_hit = True
                    
                    if not signal_hit and row['Low'] <= signal_sl:
                        result['signal_outcome'] = 'loss'
                        signal_hit = True
                    
                    # If all SLs are hit, we can stop
                    if structural_hit and fvg_inv_hit and signal_hit:
                        break
                        
            else:  # bearish
                target = between_data['Low'].min()
                
                # Find Bullish FVGs before the swing high (with candle1 info)
                data_before_swing = full_df[full_df.index <= curr_ts]
                lookback_start = max(0, len(data_before_swing) - 100)
                data_to_check = data_before_swing.iloc[lookback_start:]
                
                fvgs = self.find_fvgs(data_to_check, fvg_type='bullish', include_candle1=True)
                
                if len(fvgs) == 0:
                    return result
                
                # Get the last FVG before the swing
                last_fvg = fvgs[-1]
                fvg_ts, fvg_high, fvg_low, candle1_high, candle1_low = last_fvg
                
                # Define the three stop loss levels (with 1 point buffer)
                structural_sl = curr_price + 1  # Above swing high
                fvg_inv_sl = candle1_high + 1   # Above candle1 high (FVG invalidation)
                
                # Now look for price to close below FVG low after the divergence
                future_mask = full_df.index > curr_ts
                future_data = full_df[future_mask]
                
                entry_found = False
                entry_price = None
                entry_ts = None
                signal_candle_high = None
                
                for idx, row in future_data.iterrows():
                    # Check if structural stop is hit before entry
                    if row['High'] >= structural_sl:
                        return result
                    
                    # Check for FVG breakout (close below FVG low)
                    if row['Close'] < fvg_low:
                        entry_found = True
                        entry_price = row['Close']
                        entry_ts = idx
                        signal_candle_high = row['High']  # For signal candle SL
                        break
                
                if not entry_found:
                    return result
                
                # Calculate signal candle SL (1 point above signal candle high)
                signal_sl = signal_candle_high + 1
                
                # Store common info
                result['entry'] = entry_price
                result['entry_timestamp'] = entry_ts
                result['target'] = target
                
                # Calculate risks and rewards for each SL
                result['structural_stop'] = structural_sl
                result['structural_risk'] = structural_sl - entry_price
                result['structural_reward'] = entry_price - target
                if result['structural_risk'] > 0:
                    result['structural_rr'] = result['structural_reward'] / result['structural_risk']
                
                result['fvg_inv_stop'] = fvg_inv_sl
                result['fvg_inv_risk'] = fvg_inv_sl - entry_price
                result['fvg_inv_reward'] = entry_price - target
                if result['fvg_inv_risk'] > 0:
                    result['fvg_inv_rr'] = result['fvg_inv_reward'] / result['fvg_inv_risk']
                
                result['signal_stop'] = signal_sl
                result['signal_risk'] = signal_sl - entry_price
                result['signal_reward'] = entry_price - target
                if result['signal_risk'] > 0:
                    result['signal_rr'] = result['signal_reward'] / result['signal_risk']
                
                # Continue from entry point to check outcomes for each SL
                entry_idx = future_data.index.get_loc(entry_ts)
                remaining_data = future_data.iloc[entry_idx + 1:]
                
                # Track outcomes separately for each SL
                structural_hit = False
                fvg_inv_hit = False
                signal_hit = False
                
                for idx, row in remaining_data.iterrows():
                    # Check if target is reached first
                    if row['Low'] <= target:
                        # All remaining SLs that haven't been hit are wins
                        if not structural_hit:
                            result['structural_outcome'] = 'win'
                        if not fvg_inv_hit:
                            result['fvg_inv_outcome'] = 'win'
                        if not signal_hit:
                            result['signal_outcome'] = 'win'
                        break
                    
                    # Check each SL independently
                    if not structural_hit and row['High'] >= structural_sl:
                        result['structural_outcome'] = 'loss'
                        structural_hit = True
                    
                    if not fvg_inv_hit and row['High'] >= fvg_inv_sl:
                        result['fvg_inv_outcome'] = 'loss'
                        fvg_inv_hit = True
                    
                    if not signal_hit and row['High'] >= signal_sl:
                        result['signal_outcome'] = 'loss'
                        signal_hit = True
                    
                    # If all SLs are hit, we can stop
                    if structural_hit and fvg_inv_hit and signal_hit:
                        break
            
        except Exception as e:
            # If any error occurs, mark as no_trade for all
            pass
        
        return result
    
    def generate_statistics(self, divergences: List[Dict]) -> pd.DataFrame:
        """
        Generate summary statistics from detected divergences.
        
        Returns:
            DataFrame with statistics
        """
        if not divergences:
            return pd.DataFrame()
        
        df = pd.DataFrame(divergences)
        
        # Statistics by session
        stats = []
        
        for session in ['london', 'ny']:
            session_divs = df[df['session'] == session]
            
            if len(session_divs) == 0:
                continue
            
            total = len(session_divs)
            bullish = len(session_divs[session_divs['type'] == 'bullish'])
            bearish = len(session_divs[session_divs['type'] == 'bearish'])
            
            # Count leadership
            nq_bullish_leader = len(session_divs[(session_divs['type'] == 'bullish') & 
                                                 (session_divs['leader'] == 'NQ')])
            es_bullish_leader = len(session_divs[(session_divs['type'] == 'bullish') & 
                                                 (session_divs['leader'] == 'ES')])
            nq_bearish_leader = len(session_divs[(session_divs['type'] == 'bearish') & 
                                                  (session_divs['leader'] == 'NQ')])
            es_bearish_leader = len(session_divs[(session_divs['type'] == 'bearish') & 
                                                  (session_divs['leader'] == 'ES')])
            
            stats.append({
                'Session': session.upper(),
                'Total Divergences': total,
                'Bullish SMT': bullish,
                'Bearish SMT': bearish,
                'NQ Bullish Leader': nq_bullish_leader,
                'ES Bullish Leader': es_bullish_leader,
                'NQ Bearish Leader': nq_bearish_leader,
                'ES Bearish Leader': es_bearish_leader
            })
        
        # Add totals
        if len(df) > 0:
            total = len(df)
            bullish = len(df[df['type'] == 'bullish'])
            bearish = len(df[df['type'] == 'bearish'])
            
            nq_bullish_leader = len(df[(df['type'] == 'bullish') & (df['leader'] == 'NQ')])
            es_bullish_leader = len(df[(df['type'] == 'bullish') & (df['leader'] == 'ES')])
            nq_bearish_leader = len(df[(df['type'] == 'bearish') & (df['leader'] == 'NQ')])
            es_bearish_leader = len(df[(df['type'] == 'bearish') & (df['leader'] == 'ES')])
            
            stats.append({
                'Session': 'TOTAL',
                'Total Divergences': total,
                'Bullish SMT': bullish,
                'Bearish SMT': bearish,
                'NQ Bullish Leader': nq_bullish_leader,
                'ES Bullish Leader': es_bullish_leader,
                'NQ Bearish Leader': nq_bearish_leader,
                'ES Bearish Leader': es_bearish_leader
            })
        
        return pd.DataFrame(stats)
    
    def generate_backtest_statistics(self, divergences: List[Dict]) -> pd.DataFrame:
        """
        Generate backtest statistics showing win rates for SMT divergences.
        
        Args:
            divergences: List of divergence dictionaries with backtest results
            
        Returns:
            DataFrame with backtest statistics
        """
        if not divergences:
            return pd.DataFrame()
        
        df = pd.DataFrame(divergences)
        
        # Filter only divergences with known outcomes
        df = df[df['backtest_outcome'].isin(['win', 'loss'])]
        
        if len(df) == 0:
            return pd.DataFrame()
        
        stats = []
        
        # Statistics by timeframe, session, and divergence type
        for timeframe in df['timeframe'].unique() if 'timeframe' in df.columns else ['5m']:
            tf_df = df[df['timeframe'] == timeframe] if 'timeframe' in df.columns else df
            
            for session in ['london', 'ny']:
                session_df = tf_df[tf_df['session'] == session]
                
                if len(session_df) == 0:
                    continue
                
                # Overall session stats
                total = len(session_df)
                wins = len(session_df[session_df['backtest_outcome'] == 'win'])
                losses = len(session_df[session_df['backtest_outcome'] == 'loss'])
                win_rate = (wins / total * 100) if total > 0 else 0
                
                stats.append({
                    'Timeframe': timeframe,
                    'Session': session.upper(),
                    'Type': 'ALL',
                    'Total Trades': total,
                    'Wins': wins,
                    'Losses': losses,
                    'Win Rate (%)': round(win_rate, 1)
                })
                
                # Stats by divergence type (bullish/bearish)
                for div_type in ['bullish', 'bearish']:
                    type_df = session_df[session_df['type'] == div_type]
                    
                    if len(type_df) == 0:
                        continue
                    
                    total = len(type_df)
                    wins = len(type_df[type_df['backtest_outcome'] == 'win'])
                    losses = len(type_df[type_df['backtest_outcome'] == 'loss'])
                    win_rate = (wins / total * 100) if total > 0 else 0
                    
                    stats.append({
                        'Timeframe': timeframe,
                        'Session': session.upper(),
                        'Type': div_type.upper(),
                        'Total Trades': total,
                        'Wins': wins,
                        'Losses': losses,
                        'Win Rate (%)': round(win_rate, 1)
                    })
                    
                    # Stats by leader for this type
                    for leader in ['NQ', 'ES']:
                        leader_df = type_df[type_df['leader'] == leader]
                        
                        if len(leader_df) == 0:
                            continue
                        
                        total = len(leader_df)
                        wins = len(leader_df[leader_df['backtest_outcome'] == 'win'])
                        losses = len(leader_df[leader_df['backtest_outcome'] == 'loss'])
                        win_rate = (wins / total * 100) if total > 0 else 0
                        
                        stats.append({
                            'Timeframe': timeframe,
                            'Session': session.upper(),
                            'Type': f"{div_type.upper()} - {leader} Leader",
                            'Total Trades': total,
                            'Wins': wins,
                            'Losses': losses,
                            'Win Rate (%)': round(win_rate, 1)
                        })
        
        return pd.DataFrame(stats)
    
    def generate_fvg_backtest_statistics(self, divergences: List[Dict]) -> pd.DataFrame:
        """
        Generate FVG-based backtest statistics with R:R ratios.
        
        Args:
            divergences: List of divergence dictionaries with FVG backtest results
            
        Returns:
            DataFrame with FVG backtest statistics including R:R ratios
        """
        if not divergences:
            return pd.DataFrame()
        
        df = pd.DataFrame(divergences)
        
        # Filter only divergences with FVG outcomes
        if 'fvg_outcome' not in df.columns:
            return pd.DataFrame()
        
        stats = []
        
        # Statistics by timeframe and session
        for timeframe in df['timeframe'].unique() if 'timeframe' in df.columns else ['5m']:
            tf_df = df[df['timeframe'] == timeframe] if 'timeframe' in df.columns else df
            
            for session in ['london', 'ny']:
                session_df = tf_df[tf_df['session'] == session]
                
                if len(session_df) == 0:
                    continue
                
                # Total SMT detected
                total_smt = len(session_df)
                
                # Trades taken (FVG breakout confirmed)
                trades_taken_df = session_df[session_df['fvg_outcome'].isin(['win', 'loss'])]
                trades_taken = len(trades_taken_df)
                
                if trades_taken == 0:
                    stats.append({
                        'Timeframe': timeframe,
                        'Session': session.upper(),
                        'Type': 'ALL',
                        'Total SMT': total_smt,
                        'Trades Taken': 0,
                        'Wins': 0,
                        'Losses': 0,
                        'Win Rate (%)': 0,
                        'Avg R:R': 0
                    })
                    continue
                
                wins = len(trades_taken_df[trades_taken_df['fvg_outcome'] == 'win'])
                losses = len(trades_taken_df[trades_taken_df['fvg_outcome'] == 'loss'])
                win_rate = (wins / trades_taken * 100) if trades_taken > 0 else 0
                
                # Calculate average R:R for winning trades
                winning_trades = trades_taken_df[trades_taken_df['fvg_outcome'] == 'win']
                avg_rr = winning_trades['fvg_rr_ratio'].mean() if len(winning_trades) > 0 else 0
                
                stats.append({
                    'Timeframe': timeframe,
                    'Session': session.upper(),
                    'Type': 'ALL',
                    'Total SMT': total_smt,
                    'Trades Taken': trades_taken,
                    'Wins': wins,
                    'Losses': losses,
                    'Win Rate (%)': round(win_rate, 1),
                    'Avg R:R': round(avg_rr, 2) if not pd.isna(avg_rr) else 0
                })
                
                # Stats by divergence type
                for div_type in ['bullish', 'bearish']:
                    type_df = session_df[session_df['type'] == div_type]
                    
                    if len(type_df) == 0:
                        continue
                    
                    total_smt_type = len(type_df)
                    type_trades_df = type_df[type_df['fvg_outcome'].isin(['win', 'loss'])]
                    trades_taken_type = len(type_trades_df)
                    
                    if trades_taken_type == 0:
                        continue
                    
                    wins = len(type_trades_df[type_trades_df['fvg_outcome'] == 'win'])
                    losses = len(type_trades_df[type_trades_df['fvg_outcome'] == 'loss'])
                    win_rate = (wins / trades_taken_type * 100) if trades_taken_type > 0 else 0
                    
                    winning_trades = type_trades_df[type_trades_df['fvg_outcome'] == 'win']
                    avg_rr = winning_trades['fvg_rr_ratio'].mean() if len(winning_trades) > 0 else 0
                    
                    stats.append({
                        'Timeframe': timeframe,
                        'Session': session.upper(),
                        'Type': div_type.upper(),
                        'Total SMT': total_smt_type,
                        'Trades Taken': trades_taken_type,
                        'Wins': wins,
                        'Losses': losses,
                        'Win Rate (%)': round(win_rate, 1),
                        'Avg R:R': round(avg_rr, 2) if not pd.isna(avg_rr) else 0
                    })
                    
                    # Stats by leader
                    for leader in ['NQ', 'ES']:
                        leader_df = type_df[type_df['leader'] == leader]
                        
                        if len(leader_df) == 0:
                            continue
                        
                        total_smt_leader = len(leader_df)
                        leader_trades_df = leader_df[leader_df['fvg_outcome'].isin(['win', 'loss'])]
                        trades_taken_leader = len(leader_trades_df)
                        
                        if trades_taken_leader == 0:
                            continue
                        
                        wins = len(leader_trades_df[leader_trades_df['fvg_outcome'] == 'win'])
                        losses = len(leader_trades_df[leader_trades_df['fvg_outcome'] == 'loss'])
                        win_rate = (wins / trades_taken_leader * 100) if trades_taken_leader > 0 else 0
                        
                        winning_trades = leader_trades_df[leader_trades_df['fvg_outcome'] == 'win']
                        avg_rr = winning_trades['fvg_rr_ratio'].mean() if len(winning_trades) > 0 else 0
                        
                        stats.append({
                            'Timeframe': timeframe,
                            'Session': session.upper(),
                            'Type': f"{div_type.upper()} - {leader} Leader",
                            'Total SMT': total_smt_leader,
                            'Trades Taken': trades_taken_leader,
                            'Wins': wins,
                            'Losses': losses,
                            'Win Rate (%)': round(win_rate, 1),
                            'Avg R:R': round(avg_rr, 2) if not pd.isna(avg_rr) else 0
                        })
        
        return pd.DataFrame(stats)
    
    def generate_multi_sl_statistics(self, divergences: List[Dict]) -> pd.DataFrame:
        """
        Generate comparative statistics for three stop loss strategies.
        
        Args:
            divergences: List of divergence dictionaries with multi-SL backtest results
            
        Returns:
            DataFrame comparing the three SL strategies
        """
        if not divergences:
            return pd.DataFrame()
        
        df = pd.DataFrame(divergences)
        
        # Filter divergences that have multi-SL results
        required_cols = ['structural_outcome', 'fvg_inv_outcome', 'signal_outcome']
        if not all(col in df.columns for col in required_cols):
            return pd.DataFrame()
        
        stats = []
        
        # For each timeframe and session
        for timeframe in df['timeframe'].unique() if 'timeframe' in df.columns else ['5m']:
            tf_df = df[df['timeframe'] == timeframe] if 'timeframe' in df.columns else df
            
            for session in ['london', 'ny']:
                session_df = tf_df[tf_df['session'] == session]
                
                if len(session_df) == 0:
                    continue
                
                total_smt = len(session_df)
                
                # Process each SL strategy
                for sl_type in ['structural', 'fvg_inv', 'signal']:
                    outcome_col = f'{sl_type}_outcome'
                    risk_col = f'{sl_type}_risk'
                    rr_col = f'{sl_type}_rr'
                    
                    # Trades taken (not 'no_trade')
                    trades_df = session_df[session_df[outcome_col].isin(['win', 'loss'])]
                    trades_taken = len(trades_df)
                    
                    if trades_taken == 0:
                        continue
                    
                    wins = len(trades_df[trades_df[outcome_col] == 'win'])
                    losses = len(trades_df[trades_df[outcome_col] == 'loss'])
                    win_rate = (wins / trades_taken * 100) if trades_taken > 0 else 0
                    loss_rate = (losses / trades_taken * 100) if trades_taken > 0 else 0
                    
                    # Calculate average R:R for winning trades
                    winning_trades = trades_df[trades_df[outcome_col] == 'win']
                    avg_rr = winning_trades[rr_col].mean() if len(winning_trades) > 0 and rr_col in winning_trades.columns else 0
                    
                    # Calculate expectancy (assuming 1R risk)
                    # Expectancy = (Win_Rate * Avg_Win_R) - (Loss_Rate * 1R)
                    # For wins, we use the average R:R ratio as the reward in R multiples
                    # For losses, we lose 1R
                    expectancy = (win_rate / 100 * avg_rr) - (loss_rate / 100 * 1)
                    
                    # Map SL type to friendly name
                    sl_names = {
                        'structural': 'Structural (Safe)',
                        'fvg_inv': 'FVG Invalidation',
                        'signal': 'Signal Candle (Aggressive)'
                    }
                    
                    stats.append({
                        'Timeframe': timeframe,
                        'Session': session.upper(),
                        'SL Strategy': sl_names[sl_type],
                        'Total SMT': total_smt,
                        'Trades Taken': trades_taken,
                        'Wins': wins,
                        'Losses': losses,
                        'Win Rate (%)': round(win_rate, 1),
                        'Avg R:R': round(avg_rr, 2) if not pd.isna(avg_rr) else 0,
                        'Expectancy (R)': round(expectancy, 2)
                    })
        
        return pd.DataFrame(stats)
    
    def plot_divergence_example(self, divergence: Dict, nq_df: pd.DataFrame, 
                               es_df: pd.DataFrame, output_path: str = None):
        """
        Plot an example of detected SMT divergence.
        
        Args:
            divergence: Divergence dictionary
            nq_df: NQ DataFrame for the session
            es_df: ES DataFrame for the session
            output_path: Path to save the plot (optional)
        """
        # Get time window around divergence (2 hours before to 1 hour after)
        start_time = divergence['prev_timestamp'] - pd.Timedelta(hours=1)
        end_time = divergence['timestamp'] + pd.Timedelta(minutes=30)
        
        nq_plot = nq_df[(nq_df.index >= start_time) & (nq_df.index <= end_time)]
        es_plot = es_df[(es_df.index >= start_time) & (es_df.index <= end_time)]
        
        if len(nq_plot) == 0 or len(es_plot) == 0:
            return
        
        # Create figure with two subplots
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10), sharex=True)
        
        # Plot NQ
        ax1.plot(nq_plot.index, nq_plot['Close'], label='NQ Close', color='blue', linewidth=1.5)
        ax1.scatter([divergence['prev_timestamp'], divergence['timestamp']],
                   [divergence['nq_prev'], divergence['nq_curr']], 
                   color='red', s=100, zorder=5, label='Swing Points')
        ax1.plot([divergence['prev_timestamp'], divergence['timestamp']],
                [divergence['nq_prev'], divergence['nq_curr']], 
                color='red', linestyle='--', linewidth=2, alpha=0.7)
        ax1.set_ylabel('NQ Price', fontsize=12, fontweight='bold')
        ax1.set_title(f"NQ: {divergence['nq_direction']}", fontsize=11)
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        
        # Plot ES
        ax2.plot(es_plot.index, es_plot['Close'], label='ES Close', color='green', linewidth=1.5)
        ax2.scatter([divergence['prev_timestamp'], divergence['timestamp']],
                   [divergence['es_prev'], divergence['es_curr']], 
                   color='red', s=100, zorder=5, label='Swing Points')
        ax2.plot([divergence['prev_timestamp'], divergence['timestamp']],
                [divergence['es_prev'], divergence['es_curr']], 
                color='red', linestyle='--', linewidth=2, alpha=0.7)
        ax2.set_ylabel('ES Price', fontsize=12, fontweight='bold')
        ax2.set_xlabel('Time', fontsize=12, fontweight='bold')
        ax2.set_title(f"ES: {divergence['es_direction']}", fontsize=11)
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        
        # Main title
        div_type = divergence['type'].upper()
        leader = divergence['leader']
        session = divergence['session'].upper()
        fig.suptitle(f"{div_type} SMT Divergence - {leader} Leader - {session} Session\n"
                    f"Detected at {divergence['timestamp'].strftime('%Y-%m-%d %H:%M')}",
                    fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        
        if output_path:
            plt.savefig(output_path, dpi=150, bbox_inches='tight')
            print(f"Plot saved to: {output_path}")
        
        plt.close()
    
    def run_analysis(self, years: List[int] = [2024], timeframe: str = '5m',
                    output_dir: str = 'smt_analysis_results'):
        """
        Run complete SMT divergence analysis.
        
        Args:
            years: List of years to analyze
            timeframe: '5m' or '15m'
            output_dir: Directory to save results
        """
        print("="*80)
        print("SMT DIVERGENCE DETECTOR")
        print("="*80)
        print(f"Analyzing {timeframe} timeframe for years: {years}")
        print(f"Sessions: London (02:00-05:00), New York AM (08:30-11:00)")
        print("="*80)
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        all_divergences = []
        
        for year in years:
            print(f"\n### Processing {year} ###")
            
            # Load NQ data
            nq_df = self.load_nq_data(year, timeframe)
            if len(nq_df) == 0:
                print(f"  ⚠ No NQ data found for {year}")
                continue
            
            # Load ES data - try different year ranges based on configuration
            es_df = pd.DataFrame()
            
            # Get year ranges from configuration
            year_ranges = self._get_es_year_ranges(year, timeframe)
            
            # Try the configured ranges
            for year_range in year_ranges:
                es_df = self.load_es_data(year_range, timeframe)
                if len(es_df) > 0:
                    break
            
            # If still no ES data, try dynamic fallback patterns
            if len(es_df) == 0:
                fallback_ranges = self._get_fallback_year_ranges(year)
                for year_range in fallback_ranges:
                    es_df = self.load_es_data(year_range, timeframe)
                    if len(es_df) > 0:
                        break
            
            if len(es_df) == 0:
                print(f"  ⚠ No ES data found for {year}")
                continue
            
            # Filter ES data to match year
            es_df = es_df[es_df.index.year == year]
            
            print(f"  ✓ Loaded {len(nq_df)} NQ candles, {len(es_df)} ES candles")
            
            # Analyze London session
            print("  → Analyzing London session...")
            london_divs, nq_london, es_london = self.analyze_session(nq_df, es_df, 'london')
            print(f"    Found {len(london_divs)} divergences")
            
            # Analyze NY session
            print("  → Analyzing NY session...")
            ny_divs, nq_ny, es_ny = self.analyze_session(nq_df, es_df, 'ny')
            print(f"    Found {len(ny_divs)} divergences")
            
            # Backtest each divergence (standard and FVG-based)
            print("  → Backtesting divergences...")
            for div in london_divs + ny_divs:
                # Determine which asset to backtest (the leader)
                leader_df = nq_df if div['leader'] == 'NQ' else es_df
                
                # Run standard backtest
                backtest_result = self.backtest_divergence(div, leader_df)
                
                # Add standard backtest results to divergence
                div['backtest_outcome'] = backtest_result['outcome']
                div['backtest_target'] = backtest_result['target']
                div['backtest_stop'] = backtest_result['stop']
                div['backtest_entry'] = backtest_result['entry']
                div['timeframe'] = timeframe
                
                # Run FVG-based backtest
                fvg_result = self.backtest_divergence_with_fvg(div, leader_df)
                
                # Add FVG backtest results to divergence
                div['fvg_outcome'] = fvg_result['outcome']
                div['fvg_target'] = fvg_result['target']
                div['fvg_stop'] = fvg_result['stop']
                div['fvg_entry'] = fvg_result['entry']
                div['fvg_entry_timestamp'] = fvg_result['entry_timestamp']
                div['fvg_risk'] = fvg_result['risk']
                div['fvg_reward'] = fvg_result['reward']
                div['fvg_rr_ratio'] = fvg_result['rr_ratio']
                
                # Run multi-SL FVG-based backtest
                multi_sl_result = self.backtest_divergence_with_fvg_multi_sl(div, leader_df)
                
                # Add multi-SL backtest results
                div['structural_outcome'] = multi_sl_result['structural_outcome']
                div['structural_stop'] = multi_sl_result['structural_stop']
                div['structural_risk'] = multi_sl_result['structural_risk']
                div['structural_reward'] = multi_sl_result['structural_reward']
                div['structural_rr'] = multi_sl_result['structural_rr']
                
                div['fvg_inv_outcome'] = multi_sl_result['fvg_inv_outcome']
                div['fvg_inv_stop'] = multi_sl_result['fvg_inv_stop']
                div['fvg_inv_risk'] = multi_sl_result['fvg_inv_risk']
                div['fvg_inv_reward'] = multi_sl_result['fvg_inv_reward']
                div['fvg_inv_rr'] = multi_sl_result['fvg_inv_rr']
                
                div['signal_outcome'] = multi_sl_result['signal_outcome']
                div['signal_stop'] = multi_sl_result['signal_stop']
                div['signal_risk'] = multi_sl_result['signal_risk']
                div['signal_reward'] = multi_sl_result['signal_reward']
                div['signal_rr'] = multi_sl_result['signal_rr']
                
                div['multi_sl_entry'] = multi_sl_result['entry']
                div['multi_sl_target'] = multi_sl_result['target']
            
            all_divergences.extend(london_divs)
            all_divergences.extend(ny_divs)
            
            # Plot examples (first divergence of each type per session)
            plotted_types = set()
            for div in london_divs + ny_divs:
                plot_key = (div['session'], div['type'])
                if plot_key not in plotted_types and len(plotted_types) < 4:
                    session_df_nq = nq_london if div['session'] == 'london' else nq_ny
                    session_df_es = es_london if div['session'] == 'london' else es_ny
                    
                    filename = f"smt_example_{year}_{div['session']}_{div['type']}.png"
                    output_path = os.path.join(output_dir, filename)
                    
                    self.plot_divergence_example(div, session_df_nq, session_df_es, output_path)
                    plotted_types.add(plot_key)
        
        print("\n" + "="*80)
        print("ANALYSIS COMPLETE")
        print("="*80)
        
        # Generate statistics
        if all_divergences:
            stats_df = self.generate_statistics(all_divergences)
            print("\n### STATISTICS ###")
            print(stats_df.to_string(index=False))
            
            # Save statistics
            stats_path = os.path.join(output_dir, 'smt_statistics.csv')
            stats_df.to_csv(stats_path, index=False)
            print(f"\n✓ Statistics saved to: {stats_path}")
            
            # Save detailed divergences
            divs_df = pd.DataFrame(all_divergences)
            divs_path = os.path.join(output_dir, 'smt_divergences_detailed.csv')
            divs_df.to_csv(divs_path, index=False)
            print(f"✓ Detailed divergences saved to: {divs_path}")
            
            # Leadership analysis
            print("\n### LEADERSHIP ANALYSIS ###")
            bullish_divs = divs_df[divs_df['type'] == 'bullish']
            bearish_divs = divs_df[divs_df['type'] == 'bearish']
            
            if len(bullish_divs) > 0:
                nq_bull_pct = (len(bullish_divs[bullish_divs['leader'] == 'NQ']) / len(bullish_divs)) * 100
                print(f"Bullish Leader: NQ {nq_bull_pct:.1f}% | ES {100-nq_bull_pct:.1f}%")
                
            if len(bearish_divs) > 0:
                nq_bear_pct = (len(bearish_divs[bearish_divs['leader'] == 'NQ']) / len(bearish_divs)) * 100
                print(f"Bearish Leader: NQ {nq_bear_pct:.1f}% | ES {100-nq_bear_pct:.1f}%")
            
            # Backtest statistics (standard entry)
            print("\n### BACKTEST RESULTS (Standard Entry) ###")
            backtest_stats = self.generate_backtest_statistics(all_divergences)
            if len(backtest_stats) > 0:
                print(backtest_stats.to_string(index=False))
                
                # Save backtest statistics
                backtest_path = os.path.join(output_dir, 'smt_backtest_statistics.csv')
                backtest_stats.to_csv(backtest_path, index=False)
                print(f"\n✓ Backtest statistics saved to: {backtest_path}")
            else:
                print("No backtest results available")
            
            # FVG Backtest statistics
            print("\n### BACKTEST RESULTS (FVG Confirmation Entry) ###")
            fvg_stats = self.generate_fvg_backtest_statistics(all_divergences)
            if len(fvg_stats) > 0:
                print(fvg_stats.to_string(index=False))
                
                # Save FVG backtest statistics
                fvg_path = os.path.join(output_dir, 'smt_fvg_backtest_statistics.csv')
                fvg_stats.to_csv(fvg_path, index=False)
                print(f"\n✓ FVG backtest statistics saved to: {fvg_path}")
                
                # Compare improvement
                print("\n### COMPARISON: FVG Filter vs Standard Entry ###")
                # Calculate overall improvements
                if len(backtest_stats) > 0 and len(fvg_stats) > 0:
                    std_overall = backtest_stats[backtest_stats['Type'] == 'ALL']
                    fvg_overall = fvg_stats[fvg_stats['Type'] == 'ALL']
                    
                    if len(std_overall) > 0 and len(fvg_overall) > 0:
                        for session in ['LONDON', 'NY']:
                            std_session = std_overall[std_overall['Session'] == session]
                            fvg_session = fvg_overall[fvg_overall['Session'] == session]
                            
                            if len(std_session) > 0 and len(fvg_session) > 0:
                                std_wr = std_session['Win Rate (%)'].values[0]
                                fvg_wr = fvg_session['Win Rate (%)'].values[0]
                                fvg_taken = fvg_session['Trades Taken'].values[0]
                                fvg_smt = fvg_session['Total SMT'].values[0]
                                
                                improvement = fvg_wr - std_wr
                                filter_rate = (fvg_taken / fvg_smt * 100) if fvg_smt > 0 else 0
                                
                                print(f"{session} Session:")
                                print(f"  Standard Entry Win Rate: {std_wr:.1f}%")
                                print(f"  FVG Entry Win Rate: {fvg_wr:.1f}%")
                                print(f"  Improvement: {improvement:+.1f}% {'✓' if improvement > 0 else ''}")
                                print(f"  Trade Filter Rate: {filter_rate:.1f}% ({fvg_taken}/{fvg_smt} trades taken)")
                                
                                if len(fvg_session) > 0 and 'Avg R:R' in fvg_session.columns:
                                    avg_rr = fvg_session['Avg R:R'].values[0]
                                    print(f"  Average R:R (wins): {avg_rr:.2f}")
                                print()
            else:
                print("No FVG backtest results available")
            
            # Multi-SL Backtest statistics
            print("\n### STOP LOSS COMPARISON (FVG Entry with 3 SL Strategies) ###")
            multi_sl_stats = self.generate_multi_sl_statistics(all_divergences)
            if len(multi_sl_stats) > 0:
                print(multi_sl_stats.to_string(index=False))
                
                # Save multi-SL backtest statistics
                multi_sl_path = os.path.join(output_dir, 'smt_multi_sl_backtest_statistics.csv')
                multi_sl_stats.to_csv(multi_sl_path, index=False)
                print(f"\n✓ Multi-SL backtest statistics saved to: {multi_sl_path}")
                
                # Summary of best SL strategy
                print("\n### BEST STOP LOSS STRATEGY ANALYSIS ###")
                for session in ['LONDON', 'NY']:
                    session_stats = multi_sl_stats[multi_sl_stats['Session'] == session]
                    if len(session_stats) > 0:
                        # Sort by expectancy (best overall metric)
                        best_by_expectancy = session_stats.sort_values('Expectancy (R)', ascending=False).iloc[0]
                        best_by_winrate = session_stats.sort_values('Win Rate (%)', ascending=False).iloc[0]
                        best_by_rr = session_stats.sort_values('Avg R:R', ascending=False).iloc[0]
                        
                        print(f"\n{session} Session:")
                        print(f"  Best Expectancy: {best_by_expectancy['SL Strategy']} ({best_by_expectancy['Expectancy (R)']:.2f}R)")
                        print(f"    Win Rate: {best_by_expectancy['Win Rate (%)']:.1f}% | Avg R:R: {best_by_expectancy['Avg R:R']:.2f}")
                        print(f"  Best Win Rate: {best_by_winrate['SL Strategy']} ({best_by_winrate['Win Rate (%)']:.1f}%)")
                        print(f"  Best R:R Ratio: {best_by_rr['SL Strategy']} ({best_by_rr['Avg R:R']:.2f})")
            else:
                print("No multi-SL backtest results available")
        else:
            print("\n⚠ No divergences detected")
        
        print("\n" + "="*80)
        print(f"Results saved to: {output_dir}/")
        print("="*80)


def main():
    """Main entry point for the script."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Detect SMT divergences between NQ and ES futures',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze all years (2018-today) with 5-minute timeframe (default)
  python smt_divergence_detector.py
  
  # Analyze specific year with 15-minute timeframe
  python smt_divergence_detector.py --years 2024 --timeframe 15m
  
  # Analyze multiple years with 15-minute timeframe
  python smt_divergence_detector.py --years 2023 2024 --timeframe 15m
  
  # Specify custom data directory
  python smt_divergence_detector.py --path /path/to/data
        """
    )
    
    parser.add_argument(
        '--years',
        type=int,
        nargs='+',
        default=list(range(2018, datetime.now().year + 1)),
        help='Years to analyze (default: 2018 to current year)'
    )
    
    parser.add_argument(
        '--timeframe',
        type=str,
        choices=['5m', '15m'],
        default='5m',
        help='Timeframe to analyze (default: 5m)'
    )
    
    parser.add_argument(
        '--path',
        type=str,
        default='.',
        help='Base path to CSV files (default: current directory)'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        default='smt_analysis_results',
        help='Output directory for results (default: smt_analysis_results)'
    )
    
    args = parser.parse_args()
    
    # Run analysis
    detector = SMTDivergenceDetector(base_path=args.path)
    detector.run_analysis(
        years=args.years,
        timeframe=args.timeframe,
        output_dir=args.output
    )


if __name__ == '__main__':
    main()

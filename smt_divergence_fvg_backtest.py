#!/usr/bin/env python3
"""
SMT Divergence with FVG Confirmation Backtest Strategy (NQ vs ES)

This script backtests a multi-timeframe strategy that:
1. Identifies SMT (Smart Money Tool) Divergence between NQ and ES on H1/M15
2. Validates with M5 FVG formation on NQ during the reversal leg
3. Enters when price tests/inverts the M5 FVG

SMT Divergence:
- Bearish SMT (SHORT): ES makes Higher High BUT NQ makes Lower High (NQ leads down)
- Bullish SMT (LONG): ES makes Lower Low BUT NQ makes Higher Low (NQ leads up)

Risk Management: SL at NQ swing, TP at RR 1/1.5/2
"""

import bisect
import glob
import os
import warnings
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

warnings.filterwarnings('ignore')


# ============================================================================
# DATA LOADING FUNCTIONS
# ============================================================================

def load_nq_data(base_path, timeframe):
    """
    Load NQ futures data for a specific timeframe across all years.
    
    Args:
        base_path: Base directory containing CSV files
        timeframe: '5m', '15m', or '1H'
    
    Returns:
        DataFrame with datetime index and OHLCV columns
    """
    pattern = os.path.join(base_path, f"*{timeframe}.csv")
    files = sorted(glob.glob(pattern))
    
    if not files:
        raise FileNotFoundError(f"No files found for timeframe {timeframe}")
    
    dfs = []
    for file in files:
        # Skip ES files - check only the filename, not the full path
        filename = os.path.basename(file)
        if filename.startswith('ES ') or filename.startswith('es '):
            continue
            
        try:
            df = pd.read_csv(
                file,
                sep=';',
                names=['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume'],
                skiprows=1
            )
            
            # Combine date and time
            df['Datetime'] = pd.to_datetime(
                df['Date'] + ' ' + df['Time'],
                format='%d/%m/%Y %H:%M:%S'
            )
            
            # Keep only OHLCV columns
            df = df[['Datetime', 'Open', 'High', 'Low', 'Close', 'Volume']].copy()
            df.set_index('Datetime', inplace=True)
            
            # Convert to numeric
            for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            
            dfs.append(df)
        except Exception as e:
            print(f"Error loading {file}: {e}")
            continue
    
    if not dfs:
        raise ValueError(f"No valid data loaded for timeframe {timeframe}")
    
    # Concatenate all years
    result = pd.concat(dfs)
    result.sort_index(inplace=True)
    result = result[~result.index.duplicated(keep='first')]
    
    print(f"Loaded NQ {len(result)} candles for {timeframe} from {result.index[0]} to {result.index[-1]}")
    
    return result


def load_es_data(base_path, timeframe):
    """
    Load ES (S&P 500) futures data for a specific timeframe.
    
    Args:
        base_path: Base directory containing CSV files
        timeframe: '5m', '15m', or '1h'
    
    Returns:
        DataFrame with datetime index and OHLCV columns
    """
    # ES files have different naming convention
    if timeframe == '1H':
        pattern = os.path.join(base_path, "ES 1h*.csv")
    else:
        pattern = os.path.join(base_path, f"ES {timeframe}*.csv")
    
    files = sorted(glob.glob(pattern))
    
    if not files:
        raise FileNotFoundError(f"No ES files found for timeframe {timeframe}")
    
    dfs = []
    for file in files:
        try:
            df = pd.read_csv(
                file,
                sep=';',
                names=['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume'],
                skiprows=1
            )
            
            # Combine date and time
            df['Datetime'] = pd.to_datetime(
                df['Date'] + ' ' + df['Time'],
                format='%d/%m/%Y %H:%M:%S'
            )
            
            # Keep only OHLCV columns
            df = df[['Datetime', 'Open', 'High', 'Low', 'Close', 'Volume']].copy()
            df.set_index('Datetime', inplace=True)
            
            # Convert to numeric
            for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            
            dfs.append(df)
        except Exception as e:
            print(f"Error loading {file}: {e}")
            continue
    
    if not dfs:
        raise ValueError(f"No valid ES data loaded for timeframe {timeframe}")
    
    # Concatenate all files
    result = pd.concat(dfs)
    result.sort_index(inplace=True)
    result = result[~result.index.duplicated(keep='first')]
    
    print(f"Loaded ES {len(result)} candles for {timeframe} from {result.index[0]} to {result.index[-1]}")
    
    return result


# ============================================================================
# FVG DETECTION (VECTORIZED)
# ============================================================================

def detect_fvgs_vectorized(df, fvg_type='both'):
    """
    Detect Fair Value Gaps (FVG) using vectorized operations.
    
    FVG Definition: 3-candle pattern where wicks of candle 1 and 3 don't overlap.
    - Bearish FVG: Low[i-2] > High[i]
    - Bullish FVG: High[i-2] < Low[i]
    
    Args:
        df: DataFrame with OHLC data
        fvg_type: 'bullish', 'bearish', or 'both'
    
    Returns:
        List of dictionaries with FVG information
    """
    fvgs = []
    
    # Get arrays for vectorized operations
    highs = df['High'].values
    lows = df['Low'].values
    times = df.index.values
    
    # Bearish FVG: candle1_low > candle3_high
    if fvg_type in ['bearish', 'both']:
        bearish_mask = lows[:-2] > highs[2:]
        bearish_indices = np.where(bearish_mask)[0] + 2  # Adjust index to candle 3
        
        for idx in bearish_indices:
            fvgs.append({
                'index': idx,
                'datetime': times[idx],
                'type': 'bearish',
                'top': lows[idx-2],
                'bottom': highs[idx],
                'middle': (lows[idx-2] + highs[idx]) / 2,
                'size': lows[idx-2] - highs[idx]
            })
    
    # Bullish FVG: candle1_high < candle3_low
    if fvg_type in ['bullish', 'both']:
        bullish_mask = highs[:-2] < lows[2:]
        bullish_indices = np.where(bullish_mask)[0] + 2
        
        for idx in bullish_indices:
            fvgs.append({
                'index': idx,
                'datetime': times[idx],
                'type': 'bullish',
                'top': lows[idx],
                'bottom': highs[idx-2],
                'middle': (lows[idx] + highs[idx-2]) / 2,
                'size': lows[idx] - highs[idx-2]
            })
    
    # Sort by datetime
    fvgs.sort(key=lambda x: x['datetime'])
    
    return fvgs


# ============================================================================
# SWING HIGH/LOW DETECTION (VECTORIZED)
# ============================================================================

def detect_swing_points_vectorized(df, lookback=5):
    """
    Detect Swing Highs and Lows using vectorized operations.
    
    Args:
        df: DataFrame with OHLC data
        lookback: Number of candles to look before and after
    
    Returns:
        List of dictionaries with swing point information
    """
    swings = []
    
    highs = df['High'].values
    lows = df['Low'].values
    times = df.index.values
    
    # Detect Swing Highs
    for i in range(lookback, len(highs) - lookback):
        current_high = highs[i]
        
        # Check if current is higher than lookback before and after
        before_max = np.max(highs[i-lookback:i])
        after_max = np.max(highs[i+1:i+lookback+1])
        
        if current_high > before_max and current_high > after_max:
            swings.append({
                'index': i,
                'datetime': times[i],
                'type': 'high',
                'price': current_high
            })
    
    # Detect Swing Lows
    for i in range(lookback, len(lows) - lookback):
        current_low = lows[i]
        
        # Check if current is lower than lookback before and after
        before_min = np.min(lows[i-lookback:i])
        after_min = np.min(lows[i+1:i+lookback+1])
        
        if current_low < before_min and current_low < after_min:
            swings.append({
                'index': i,
                'datetime': times[i],
                'type': 'low',
                'price': current_low
            })
    
    # Sort by datetime
    swings.sort(key=lambda x: x['datetime'])
    
    return swings


# ============================================================================
# SMT DIVERGENCE DETECTION
# ============================================================================

def detect_smt_divergences(nq_df, es_df, nq_swings, es_swings, lookback=10):
    """
    Detect SMT (Smart Money Tool) Divergences between NQ and ES.
    
    SMT Divergence occurs when one instrument makes a new high/low but the other doesn't,
    indicating relative strength or weakness.
    
    Bearish SMT (for SHORT): ES makes Higher High BUT NQ makes Lower High
    Bullish SMT (for LONG): ES makes Lower Low BUT NQ makes Higher Low
    
    Args:
        nq_df: NQ DataFrame
        es_df: ES DataFrame
        nq_swings: List of NQ swing points
        es_swings: List of ES swing points
        lookback: How many previous swings to compare
    
    Returns:
        List of SMT divergence setups
    """
    divergences = []
    
    # Separate swings by type
    nq_highs = [s for s in nq_swings if s['type'] == 'high']
    nq_lows = [s for s in nq_swings if s['type'] == 'low']
    es_highs = [s for s in es_swings if s['type'] == 'high']
    es_lows = [s for s in es_swings if s['type'] == 'low']
    
    print(f"  Analyzing {len(nq_highs)} NQ highs and {len(es_highs)} ES highs for bearish SMT...")
    
    # Detect Bearish SMT (ES Higher High + NQ Lower High)
    for i in range(1, min(len(nq_highs), 2000)):  # Limit for performance
        if i % 500 == 0:
            print(f"    Progress: {i}/{min(len(nq_highs), 2000)}")
        
        nq_curr_swing = nq_highs[i]
        nq_curr_time = pd.Timestamp(nq_curr_swing['datetime'])
        nq_curr_price = nq_curr_swing['price']
        
        # Find previous NQ high within lookback
        start_idx = max(0, i - lookback)
        if start_idx == i:
            continue
        
        nq_prev_price = nq_highs[start_idx]['price']
        
        # Check if NQ made Lower High
        if nq_curr_price < nq_prev_price:
            # Find ES swing around same time (binary search-like approach)
            time_window = pd.Timedelta(hours=5)
            es_candidates = [h for h in es_highs 
                           if abs((pd.Timestamp(h['datetime']) - nq_curr_time).total_seconds()) < time_window.total_seconds()]
            
            if es_candidates:
                es_curr = min(es_candidates, key=lambda x: abs((pd.Timestamp(x['datetime']) - nq_curr_time).total_seconds()))
                es_curr_time = pd.Timestamp(es_curr['datetime'])
                es_curr_price = es_curr['price']
                
                # Find previous ES high within time range
                prev_es_candidates = [h for h in es_highs 
                                    if pd.Timestamp(h['datetime']) < es_curr_time and
                                    pd.Timestamp(h['datetime']) >= (es_curr_time - pd.Timedelta(hours=lookback * 2))]
                
                if prev_es_candidates:
                    es_prev = prev_es_candidates[-1]  # Most recent before current
                    es_prev_price = es_prev['price']
                    
                    # Check if ES made Higher High
                    if es_curr_price > es_prev_price:
                        # SMT Bearish Divergence confirmed!
                        divergences.append({
                            'type': 'bearish_smt',
                            'datetime': nq_curr_time,
                            'nq_index': nq_curr_swing['index'],
                            'nq_high': nq_curr_price,
                            'nq_prev_high': nq_prev_price,
                            'es_high': es_curr_price,
                            'es_prev_high': es_prev_price,
                            'direction': 'short'
                        })
    
    print(f"  Analyzing {len(nq_lows)} NQ lows and {len(es_lows)} ES lows for bullish SMT...")
    
    # Detect Bullish SMT (ES Lower Low + NQ Higher Low)
    for i in range(1, min(len(nq_lows), 2000)):  # Limit for performance
        if i % 500 == 0:
            print(f"    Progress: {i}/{min(len(nq_lows), 2000)}")
        
        nq_curr_swing = nq_lows[i]
        nq_curr_time = pd.Timestamp(nq_curr_swing['datetime'])
        nq_curr_price = nq_curr_swing['price']
        
        # Find previous NQ low within lookback
        start_idx = max(0, i - lookback)
        if start_idx == i:
            continue
        
        nq_prev_price = nq_lows[start_idx]['price']
        
        # Check if NQ made Higher Low
        if nq_curr_price > nq_prev_price:
            # Find ES swing around same time
            time_window = pd.Timedelta(hours=5)
            es_candidates = [l for l in es_lows 
                           if abs((pd.Timestamp(l['datetime']) - nq_curr_time).total_seconds()) < time_window.total_seconds()]
            
            if es_candidates:
                es_curr = min(es_candidates, key=lambda x: abs((pd.Timestamp(x['datetime']) - nq_curr_time).total_seconds()))
                es_curr_time = pd.Timestamp(es_curr['datetime'])
                es_curr_price = es_curr['price']
                
                # Find previous ES low
                prev_es_candidates = [l for l in es_lows 
                                    if pd.Timestamp(l['datetime']) < es_curr_time and
                                    pd.Timestamp(l['datetime']) >= (es_curr_time - pd.Timedelta(hours=lookback * 2))]
                
                if prev_es_candidates:
                    es_prev = prev_es_candidates[-1]
                    es_prev_price = es_prev['price']
                    
                    # Check if ES made Lower Low
                    if es_curr_price < es_prev_price:
                        # SMT Bullish Divergence confirmed!
                        divergences.append({
                            'type': 'bullish_smt',
                            'datetime': nq_curr_time,
                            'nq_index': nq_curr_swing['index'],
                            'nq_low': nq_curr_price,
                            'nq_prev_low': nq_prev_price,
                            'es_low': es_curr_price,
                            'es_prev_low': es_prev_price,
                            'direction': 'long'
                        })
    
    return divergences


# ============================================================================
# STRATEGY LOGIC
# ============================================================================

class SMTDivergenceFVGStrategy:
    """
    SMT Divergence with FVG Confirmation Strategy
    
    Entry Rules:
    1. SMT Divergence Setup (H1 or M15):
       - Bearish SMT: ES Higher High + NQ Lower High (NQ leads down)
       - Bullish SMT: ES Lower Low + NQ Higher Low (NQ leads up)
    
    2. M5 FVG Validation:
       - During the reversal leg after SMT, a FVG forms on NQ M5
       - For SHORT: Bearish FVG on M5
       - For LONG: Bullish FVG on M5
    
    3. Entry Signal:
       - Price tests and inverts the FVG
       - For SHORT: Price rallies into FVG, then closes back below
       - For LONG: Price drops into FVG, then closes back above
    
    Risk Management:
       - SL: At NQ swing high/low that formed the divergence
       - TP: RR 1, 1.5, and 2
    """
    
    def __init__(self, nq_m5, nq_m15, nq_h1, es_m5, es_m15, es_h1):
        """Initialize the strategy with multi-timeframe data for both NQ and ES."""
        self.nq_m5 = nq_m5
        self.nq_m15 = nq_m15
        self.nq_h1 = nq_h1
        self.es_m5 = es_m5
        self.es_m15 = es_m15
        self.es_h1 = es_h1
        
        # Detect FVGs on NQ M5 only (for entry validation)
        print("Detecting FVGs on NQ M5 (vectorized)...")
        self.nq_m5_fvgs = detect_fvgs_vectorized(self.nq_m5)
        print(f"Found {len(self.nq_m5_fvgs)} FVGs on NQ M5")
        
        # Cache bullish and bearish FVGs separately
        self.nq_m5_bullish_fvgs = [fvg for fvg in self.nq_m5_fvgs if fvg['type'] == 'bullish']
        self.nq_m5_bearish_fvgs = [fvg for fvg in self.nq_m5_fvgs if fvg['type'] == 'bearish']
        print(f"  - {len(self.nq_m5_bullish_fvgs)} Bullish FVGs")
        print(f"  - {len(self.nq_m5_bearish_fvgs)} Bearish FVGs")
        
        # Detect swing points on both NQ and ES
        print("Detecting Swing Points on NQ M15...")
        self.nq_m15_swings = detect_swing_points_vectorized(self.nq_m15, lookback=5)
        print(f"Found {len(self.nq_m15_swings)} swing points on NQ M15")
        
        print("Detecting Swing Points on NQ H1...")
        self.nq_h1_swings = detect_swing_points_vectorized(self.nq_h1, lookback=5)
        print(f"Found {len(self.nq_h1_swings)} swing points on NQ H1")
        
        print("Detecting Swing Points on ES M15...")
        self.es_m15_swings = detect_swing_points_vectorized(self.es_m15, lookback=5)
        print(f"Found {len(self.es_m15_swings)} swing points on ES M15")
        
        print("Detecting Swing Points on ES H1...")
        self.es_h1_swings = detect_swing_points_vectorized(self.es_h1, lookback=5)
        print(f"Found {len(self.es_h1_swings)} swing points on ES H1")
        
        # Detect SMT Divergences
        print("\nDetecting SMT Divergences on H1...")
        self.h1_smt_divergences = detect_smt_divergences(
            self.nq_h1, self.es_h1,
            self.nq_h1_swings, self.es_h1_swings,
            lookback=50
        )
        print(f"Found {len(self.h1_smt_divergences)} SMT divergences on H1")
        
        print("Detecting SMT Divergences on M15...")
        self.m15_smt_divergences = detect_smt_divergences(
            self.nq_m15, self.es_m15,
            self.nq_m15_swings, self.es_m15_swings,
            lookback=100
        )
        print(f"Found {len(self.m15_smt_divergences)} SMT divergences on M15")
        
        # Pre-compute time arrays for binary search
        self.nq_m5_times = self.nq_m5.index.values
        
        # Results storage
        self.trades = []
    
    def find_nq_m5_fvgs_in_range(self, start_time, end_time, fvg_type='both'):
        """
        Find FVGs on NQ M5 that formed during a specific time range.
        Uses binary search for efficiency.
        
        Args:
            start_time: Start of range
            end_time: End of range
            fvg_type: 'bullish', 'bearish', or 'both'
        
        Returns:
            List of FVGs in the range
        """
        if fvg_type == 'bullish':
            fvgs_to_search = self.nq_m5_bullish_fvgs
        elif fvg_type == 'bearish':
            fvgs_to_search = self.nq_m5_bearish_fvgs
        else:
            fvgs_to_search = self.nq_m5_fvgs
        
        result_fvgs = []
        for fvg in fvgs_to_search:
            if fvg['datetime'] > end_time:
                break
            if start_time <= fvg['datetime'] <= end_time:
                result_fvgs.append(fvg)
        
        return result_fvgs
    
    def check_fvg_inversion(self, fvg, start_idx, direction, max_bars=50):
        """
        Check if price tests and inverts a FVG.
        
        For SHORT (bearish SMT): Look for price to rally into a bearish M5 FVG, then close below it
        For LONG (bullish SMT): Look for price to drop into a bullish M5 FVG, then close above it
        
        Args:
            fvg: The M5 FVG to check
            start_idx: M5 index to start checking from
            direction: 'short' or 'long'
            max_bars: Maximum bars to check
        
        Returns:
            Dictionary with entry information or None
        """
        # Find FVG index in M5
        fvg_time = pd.Timestamp(fvg['datetime'])
        
        try:
            fvg_m5_idx = self.nq_m5.index.searchsorted(fvg_time)
        except (KeyError, ValueError):
            return None
        
        # Look for inversion after FVG formation
        for i in range(max(fvg_m5_idx + 1, start_idx), min(fvg_m5_idx + max_bars, len(self.nq_m5))):
            high = self.nq_m5['High'].iloc[i]
            low = self.nq_m5['Low'].iloc[i]
            close = self.nq_m5['Close'].iloc[i]
            
            if direction == 'short':
                # For SHORT: Wait for price to test FVG from below, then close below FVG bottom
                # FVG should be bearish (formed during rally)
                if fvg['type'] == 'bearish':
                    # Check if price touched the FVG zone
                    if high >= fvg['bottom'] and low <= fvg['top']:
                        # Now look for close below FVG (inversion/rejection)
                        if close < fvg['bottom']:
                            return {
                                'entry_price': close,
                                'entry_time': self.nq_m5.index[i],
                                'entry_idx': i,
                                'fvg_top': fvg['top'],
                                'fvg_bottom': fvg['bottom']
                            }
            
            elif direction == 'long':
                # For LONG: Wait for price to test FVG from above, then close above FVG top
                # FVG should be bullish (formed during drop)
                if fvg['type'] == 'bullish':
                    # Check if price touched the FVG zone
                    if high >= fvg['bottom'] and low <= fvg['top']:
                        # Now look for close above FVG (inversion/rejection)
                        if close > fvg['top']:
                            return {
                                'entry_price': close,
                                'entry_time': self.nq_m5.index[i],
                                'entry_idx': i,
                                'fvg_top': fvg['top'],
                                'fvg_bottom': fvg['bottom']
                            }
        
        return None
    
    def run_backtest(self, start_date=None, end_date=None):
        """
        Run the complete SMT Divergence + FVG backtest.
        
        Process:
        1. Scan H1 and M15 for SMT Divergences
        2. For each divergence, check if M5 FVG formed during reversal
        3. Check if price inverted the FVG
        4. Calculate trade results with RR 1, 1.5, 2
        """
        print("\n" + "="*80)
        print("RUNNING SMT DIVERGENCE + FVG BACKTEST")
        print("="*80 + "\n")
        
        # Process H1 SMT Divergences
        print("Processing H1 SMT Divergences...")
        h1_processed = 0
        h1_with_fvg = 0
        h1_with_entry = 0
        
        for smt in self.h1_smt_divergences:
            # Filter by date if specified
            if start_date and smt['datetime'] < pd.Timestamp(start_date):
                continue
            if end_date and smt['datetime'] > pd.Timestamp(end_date):
                continue
            
            h1_processed += 1
            
            # Define reversal leg window (after SMT detected, look ahead)
            leg_start = smt['datetime']
            leg_end = leg_start + pd.Timedelta(hours=5)  # 5 hours window
            
            # Find M5 FVGs during reversal leg
            if smt['direction'] == 'short':
                # For SHORT, look for bearish FVGs (formed during rally before reversal)
                m5_fvgs = self.find_nq_m5_fvgs_in_range(leg_start, leg_end, fvg_type='bearish')
            else:
                # For LONG, look for bullish FVGs (formed during drop before reversal)
                m5_fvgs = self.find_nq_m5_fvgs_in_range(leg_start, leg_end, fvg_type='bullish')
            
            if m5_fvgs:
                h1_with_fvg += 1
                
                # Use the most recent FVG
                latest_fvg = max(m5_fvgs, key=lambda x: x['datetime'])
                
                # Find M5 index for SMT time
                try:
                    m5_start_idx = self.nq_m5.index.searchsorted(smt['datetime'])
                except (KeyError, ValueError):
                    continue
                
                # Check for FVG inversion
                entry = self.check_fvg_inversion(latest_fvg, m5_start_idx, smt['direction'])
                
                if entry:
                    h1_with_entry += 1
                    
                    # Calculate trade parameters
                    entry_price = entry['entry_price']
                    
                    if smt['direction'] == 'short':
                        sl_price = smt['nq_high']
                        risk = sl_price - entry_price
                        
                        if risk <= 0 or risk > 500:
                            continue
                        
                        tp1 = entry_price - risk * 1.0
                        tp2 = entry_price - risk * 1.5
                        tp3 = entry_price - risk * 2.0
                    else:  # long
                        sl_price = smt['nq_low']
                        risk = entry_price - sl_price
                        
                        if risk <= 0 or risk > 500:
                            continue
                        
                        tp1 = entry_price + risk * 1.0
                        tp2 = entry_price + risk * 1.5
                        tp3 = entry_price + risk * 2.0
                    
                    # Simulate trade
                    outcome = self.simulate_trade(
                        entry['entry_idx'],
                        entry_price,
                        sl_price,
                        tp1, tp2, tp3,
                        smt['direction']
                    )
                    
                    # Store trade
                    trade = {
                        'entry_date': entry['entry_time'],
                        'entry_price': entry_price,
                        'sl_price': sl_price,
                        'risk': risk,
                        'tp1': tp1,
                        'tp2': tp2,
                        'tp3': tp3,
                        'setup_type': smt['type'],
                        'direction': smt['direction'],
                        'timeframe': 'h1',
                        'nq_swing': smt.get('nq_high', smt.get('nq_low')),
                        'es_swing': smt.get('es_high', smt.get('es_low')),
                        'm5_fvg_bottom': latest_fvg['bottom'],
                        'm5_fvg_top': latest_fvg['top'],
                        'outcome_rr1': outcome['rr1'],
                        'outcome_rr1.5': outcome['rr1.5'],
                        'outcome_rr2': outcome['rr2'],
                        'exit_date_rr1': outcome['exit_date_rr1'],
                        'exit_date_rr1.5': outcome['exit_date_rr1.5'],
                        'exit_date_rr2': outcome['exit_date_rr2']
                    }
                    
                    self.trades.append(trade)
            
            if h1_processed % 100 == 0:
                print(f"  H1 Progress: {h1_processed}/{len(self.h1_smt_divergences)} - Trades: {len(self.trades)}")
        
        print(f"\nH1 Results: {h1_processed} SMT divergences, {h1_with_fvg} with M5 FVG, {h1_with_entry} with entry")
        
        # Process M15 SMT Divergences
        print("\nProcessing M15 SMT Divergences...")
        m15_processed = 0
        m15_with_fvg = 0
        m15_with_entry = 0
        
        for smt in self.m15_smt_divergences:
            # Filter by date
            if start_date and smt['datetime'] < pd.Timestamp(start_date):
                continue
            if end_date and smt['datetime'] > pd.Timestamp(end_date):
                continue
            
            m15_processed += 1
            
            # Define reversal leg window
            leg_start = smt['datetime']
            leg_end = leg_start + pd.Timedelta(hours=2)  # 2 hours for M15
            
            # Find M5 FVGs
            if smt['direction'] == 'short':
                m5_fvgs = self.find_nq_m5_fvgs_in_range(leg_start, leg_end, fvg_type='bearish')
            else:
                m5_fvgs = self.find_nq_m5_fvgs_in_range(leg_start, leg_end, fvg_type='bullish')
            
            if m5_fvgs:
                m15_with_fvg += 1
                
                latest_fvg = max(m5_fvgs, key=lambda x: x['datetime'])
                
                try:
                    m5_start_idx = self.nq_m5.index.searchsorted(smt['datetime'])
                except (KeyError, ValueError):
                    continue
                
                entry = self.check_fvg_inversion(latest_fvg, m5_start_idx, smt['direction'])
                
                if entry:
                    m15_with_entry += 1
                    
                    entry_price = entry['entry_price']
                    
                    if smt['direction'] == 'short':
                        sl_price = smt['nq_high']
                        risk = sl_price - entry_price
                        
                        if risk <= 0 or risk > 500:
                            continue
                        
                        tp1 = entry_price - risk * 1.0
                        tp2 = entry_price - risk * 1.5
                        tp3 = entry_price - risk * 2.0
                    else:
                        sl_price = smt['nq_low']
                        risk = entry_price - sl_price
                        
                        if risk <= 0 or risk > 500:
                            continue
                        
                        tp1 = entry_price + risk * 1.0
                        tp2 = entry_price + risk * 1.5
                        tp3 = entry_price + risk * 2.0
                    
                    outcome = self.simulate_trade(
                        entry['entry_idx'],
                        entry_price,
                        sl_price,
                        tp1, tp2, tp3,
                        smt['direction']
                    )
                    
                    trade = {
                        'entry_date': entry['entry_time'],
                        'entry_price': entry_price,
                        'sl_price': sl_price,
                        'risk': risk,
                        'tp1': tp1,
                        'tp2': tp2,
                        'tp3': tp3,
                        'setup_type': smt['type'],
                        'direction': smt['direction'],
                        'timeframe': 'm15',
                        'nq_swing': smt.get('nq_high', smt.get('nq_low')),
                        'es_swing': smt.get('es_high', smt.get('es_low')),
                        'm5_fvg_bottom': latest_fvg['bottom'],
                        'm5_fvg_top': latest_fvg['top'],
                        'outcome_rr1': outcome['rr1'],
                        'outcome_rr1.5': outcome['rr1.5'],
                        'outcome_rr2': outcome['rr2'],
                        'exit_date_rr1': outcome['exit_date_rr1'],
                        'exit_date_rr1.5': outcome['exit_date_rr1.5'],
                        'exit_date_rr2': outcome['exit_date_rr2']
                    }
                    
                    self.trades.append(trade)
            
            if m15_processed % 500 == 0:
                print(f"  M15 Progress: {m15_processed}/{len(self.m15_smt_divergences)} - Trades: {len(self.trades)}")
        
        print(f"\nM15 Results: {m15_processed} SMT divergences, {m15_with_fvg} with M5 FVG, {m15_with_entry} with entry")
        print(f"\nBacktest complete. Found {len(self.trades)} trades.")
        
        return self.trades
    
    def simulate_trade(self, entry_idx, entry_price, sl_price, tp1, tp2, tp3, direction, max_bars=100):
        """
        Simulate trade outcomes using vectorized operations.
        
        Args:
            entry_idx: M5 index of entry
            entry_price: Entry price
            sl_price: Stop loss price
            tp1, tp2, tp3: Take profit levels
            direction: 'short' or 'long'
            max_bars: Maximum bars to hold trade
        
        Returns:
            Dictionary with outcomes for each RR level
        """
        outcome = {
            'rr1': 'Loss',
            'rr1.5': 'Loss',
            'rr2': 'Loss',
            'exit_date_rr1': None,
            'exit_date_rr1.5': None,
            'exit_date_rr2': None
        }
        
        # Get price data slice
        end_idx = min(entry_idx + max_bars, len(self.nq_m5))
        highs = self.nq_m5['High'].iloc[entry_idx+1:end_idx].values
        lows = self.nq_m5['Low'].iloc[entry_idx+1:end_idx].values
        times = self.nq_m5.index[entry_idx+1:end_idx]
        
        if len(highs) == 0:
            return outcome
        
        if direction == 'short':
            # For SHORT: SL hit if high >= sl_price, TP hit if low <= tp_level
            sl_hits = highs >= sl_price
            tp1_hits = lows <= tp1
            tp2_hits = lows <= tp2
            tp3_hits = lows <= tp3
        else:  # long
            # For LONG: SL hit if low <= sl_price, TP hit if high >= tp_level
            sl_hits = lows <= sl_price
            tp1_hits = highs >= tp1
            tp2_hits = highs >= tp2
            tp3_hits = highs >= tp3
        
        # Find first hit for each level
        sl_idx = np.argmax(sl_hits) if np.any(sl_hits) else len(sl_hits)
        tp1_idx = np.argmax(tp1_hits) if np.any(tp1_hits) else len(tp1_hits)
        tp2_idx = np.argmax(tp2_hits) if np.any(tp2_hits) else len(tp2_hits)
        tp3_idx = np.argmax(tp3_hits) if np.any(tp3_hits) else len(tp3_hits)
        
        # Check TP1
        if tp1_idx < sl_idx:
            outcome['rr1'] = 'Win'
            outcome['exit_date_rr1'] = times[tp1_idx]
        elif sl_idx < len(sl_hits):
            outcome['exit_date_rr1'] = times[sl_idx]
        
        # Check TP2
        if tp2_idx < sl_idx:
            outcome['rr1.5'] = 'Win'
            outcome['exit_date_rr1.5'] = times[tp2_idx]
        elif sl_idx < len(sl_hits):
            outcome['exit_date_rr1.5'] = times[sl_idx]
        
        # Check TP3
        if tp3_idx < sl_idx:
            outcome['rr2'] = 'Win'
            outcome['exit_date_rr2'] = times[tp3_idx]
        elif sl_idx < len(sl_hits):
            outcome['exit_date_rr2'] = times[sl_idx]
        
        return outcome
    
    def get_results_dataframe(self):
        """Convert trades to DataFrame."""
        if not self.trades:
            return pd.DataFrame()
        
        return pd.DataFrame(self.trades)
    
    def calculate_statistics(self):
        """Calculate win rates and statistics."""
        if not self.trades:
            return {
                'total_trades': 0,
                'winrate_rr1': 0,
                'winrate_rr1.5': 0,
                'winrate_rr2': 0,
                'wins_rr1': 0,
                'wins_rr1.5': 0,
                'wins_rr2': 0
            }
        
        df = self.get_results_dataframe()
        
        total = len(df)
        wins_rr1 = len(df[df['outcome_rr1'] == 'Win'])
        wins_rr1_5 = len(df[df['outcome_rr1.5'] == 'Win'])
        wins_rr2 = len(df[df['outcome_rr2'] == 'Win'])
        
        return {
            'total_trades': total,
            'winrate_rr1': (wins_rr1 / total * 100) if total > 0 else 0,
            'winrate_rr1.5': (wins_rr1_5 / total * 100) if total > 0 else 0,
            'winrate_rr2': (wins_rr2 / total * 100) if total > 0 else 0,
            'wins_rr1': wins_rr1,
            'wins_rr1.5': wins_rr1_5,
            'wins_rr2': wins_rr2
        }


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main(base_path=None):
    """Main execution function."""
    print("="*80)
    print("SMT DIVERGENCE + FVG CONFIRMATION BACKTEST (NQ vs ES)")
    print("="*80)
    print()
    
    # Configuration
    if base_path is None:
        base_path = os.path.dirname(os.path.abspath(__file__))
    
    # Load NQ data
    print("Loading NQ data...")
    try:
        nq_m5 = load_nq_data(base_path, '5m')
        nq_m15 = load_nq_data(base_path, '15m')
        nq_h1 = load_nq_data(base_path, '1H')
    except Exception as e:
        print(f"Error loading NQ data: {e}")
        return
    
    # Load ES data
    print("\nLoading ES data...")
    try:
        es_m5 = load_es_data(base_path, '5m')
        es_m15 = load_es_data(base_path, '15m')
        es_h1 = load_es_data(base_path, '1h')
    except Exception as e:
        print(f"Error loading ES data: {e}")
        return
    
    print(f"\nData loaded successfully!")
    print(f"NQ M5: {len(nq_m5)} candles")
    print(f"NQ M15: {len(nq_m15)} candles")
    print(f"NQ H1: {len(nq_h1)} candles")
    print(f"ES M5: {len(es_m5)} candles")
    print(f"ES M15: {len(es_m15)} candles")
    print(f"ES H1: {len(es_h1)} candles")
    
    # Initialize strategy
    print("\n" + "="*80)
    print("INITIALIZING STRATEGY")
    print("="*80)
    strategy = SMTDivergenceFVGStrategy(nq_m5, nq_m15, nq_h1, es_m5, es_m15, es_h1)
    
    # Run backtest
    trades = strategy.run_backtest()
    
    # Get results
    results_df = strategy.get_results_dataframe()
    stats = strategy.calculate_statistics()
    
    # Display results
    print("\n" + "="*80)
    print("BACKTEST RESULTS")
    print("="*80)
    print(f"\nTotal Trades: {stats['total_trades']}")
    print(f"\nWin Rates:")
    print(f"  RR 1:1   - {stats['winrate_rr1']:.2f}% ({stats['wins_rr1']}/{stats['total_trades']})")
    print(f"  RR 1:1.5 - {stats['winrate_rr1.5']:.2f}% ({stats['wins_rr1.5']}/{stats['total_trades']})")
    print(f"  RR 1:2   - {stats['winrate_rr2']:.2f}% ({stats['wins_rr2']}/{stats['total_trades']})")
    
    # Save results
    if not results_df.empty:
        output_file = os.path.join(base_path, 'smt_divergence_fvg_results.csv')
        results_df.to_csv(output_file, index=False)
        print(f"\nResults saved to: {output_file}")
        
        # Display sample trades
        print("\n" + "="*80)
        print("SAMPLE TRADES (First 10)")
        print("="*80)
        print(results_df.head(10).to_string())
        
        # Show breakdown by direction
        print("\n" + "="*80)
        print("BREAKDOWN BY DIRECTION")
        print("="*80)
        direction_stats = results_df.groupby('direction').agg({
            'outcome_rr1': lambda x: f"{(x=='Win').sum()}/{len(x)} ({(x=='Win').mean()*100:.2f}%)",
            'risk': 'mean'
        })
        direction_stats.columns = ['Win Rate RR1', 'Avg Risk']
        print(direction_stats)
    else:
        print("\nNo trades found matching the strategy criteria.")
    
    print("\n" + "="*80)
    print("BACKTEST COMPLETE")
    print("="*80)


if __name__ == "__main__":
    import sys
    
    # Allow base_path to be passed as command line argument
    if len(sys.argv) > 1:
        main(base_path=sys.argv[1])
    else:
        main()

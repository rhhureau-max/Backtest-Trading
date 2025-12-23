#!/usr/bin/env python3
"""
Liquidity Sweep with FVG Confirmation Backtest Strategy (OPTIMIZED)

This script backtests a multi-timeframe strategy that:
1. Identifies Liquidity Sweeps (Type A) or FVG Mitigation (Type B) on H1/M15
2. Validates with M5 Bullish FVG formation during the sweep
3. Enters SHORT when price closes below the M5 FVG (inversion)

Risk Management: SL at sweep high, TP at RR 1/1.5/2

OPTIMIZATIONS:
- Vectorized swing detection and FVG detection
- Binary search for time-based lookups
- Pre-computed sweep/mitigation matrices
- Progress indicators for long-running operations
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
    
    print(f"Loaded {len(result)} candles for {timeframe} from {result.index[0]} to {result.index[-1]}")
    
    return result


# ============================================================================
# FVG DETECTION
# ============================================================================

def detect_fvgs_vectorized(df, fvg_type='both'):
    """
    Detect Fair Value Gaps (FVG) in the data using vectorized operations.
    
    FVG Definition: 3-candle pattern where wicks of candle 1 and 3 don't overlap.
    - Bearish FVG: Low[i-2] > High[i] (gap between candle 1's low and candle 3's high)
    - Bullish FVG: High[i-2] < Low[i] (gap between candle 1's high and candle 3's low)
    
    Args:
        df: DataFrame with OHLC data
        fvg_type: 'bullish', 'bearish', or 'both'
    
    Returns:
        List of dictionaries with FVG information
    """
    fvgs = []
    
    if len(df) < 3:
        return fvgs
    
    # Vectorized approach
    high = df['High'].values
    low = df['Low'].values
    
    # Shift arrays for 3-candle pattern
    candle1_high = high[:-2]
    candle1_low = low[:-2]
    candle3_high = high[2:]
    candle3_low = low[2:]
    
    # Bearish FVG detection
    if fvg_type in ['bearish', 'both']:
        bearish_mask = candle1_low > candle3_high
        bearish_indices = np.where(bearish_mask)[0] + 2  # Adjust index offset
        
        for idx in bearish_indices:
            fvgs.append({
                'index': int(idx),
                'datetime': df.index[idx],
                'type': 'bearish',
                'top': float(candle1_low[idx-2]),
                'bottom': float(candle3_high[idx-2]),
                'middle': float((candle1_low[idx-2] + candle3_high[idx-2]) / 2),
                'size': float(candle1_low[idx-2] - candle3_high[idx-2])
            })
    
    # Bullish FVG detection
    if fvg_type in ['bullish', 'both']:
        bullish_mask = candle1_high < candle3_low
        bullish_indices = np.where(bullish_mask)[0] + 2  # Adjust index offset
        
        for idx in bullish_indices:
            fvgs.append({
                'index': int(idx),
                'datetime': df.index[idx],
                'type': 'bullish',
                'top': float(candle3_low[idx-2]),
                'bottom': float(candle1_high[idx-2]),
                'middle': float((candle3_low[idx-2] + candle1_high[idx-2]) / 2),
                'size': float(candle3_low[idx-2] - candle1_high[idx-2])
            })
    
    # Sort by index for consistent ordering
    fvgs.sort(key=lambda x: x['index'])
    
    return fvgs


# ============================================================================
# SWING HIGH/LOW DETECTION
# ============================================================================

def detect_swing_points_vectorized(df, lookback=5):
    """
    Detect Swing Highs and Lows using vectorized operations with rolling windows.
    
    A Swing High is a point where the high is higher than N candles before and after.
    A Swing Low is a point where the low is lower than N candles before and after.
    
    Args:
        df: DataFrame with OHLC data
        lookback: Number of candles to look before and after
    
    Returns:
        List of dictionaries with swing point information
    """
    swings = []
    
    if len(df) < 2 * lookback + 1:
        return swings
    
    high = df['High'].values
    low = df['Low'].values
    
    # Pre-allocate arrays for swing detection
    n = len(df)
    is_swing_high = np.zeros(n, dtype=bool)
    is_swing_low = np.zeros(n, dtype=bool)
    
    # Check each potential swing point
    for i in range(lookback, n - lookback):
        # Swing High: current high > all highs in window
        left_max = np.max(high[i-lookback:i])
        right_max = np.max(high[i+1:i+lookback+1])
        if high[i] > left_max and high[i] > right_max:
            is_swing_high[i] = True
        
        # Swing Low: current low < all lows in window
        left_min = np.min(low[i-lookback:i])
        right_min = np.min(low[i+1:i+lookback+1])
        if low[i] < left_min and low[i] < right_min:
            is_swing_low[i] = True
    
    # Convert to list of dictionaries
    swing_high_indices = np.where(is_swing_high)[0]
    for idx in swing_high_indices:
        swings.append({
            'index': int(idx),
            'datetime': df.index[idx],
            'type': 'high',
            'price': float(high[idx])
        })
    
    swing_low_indices = np.where(is_swing_low)[0]
    for idx in swing_low_indices:
        swings.append({
            'index': int(idx),
            'datetime': df.index[idx],
            'type': 'low',
            'price': float(low[idx])
        })
    
    return swings


# ============================================================================
# MULTI-TIMEFRAME ALIGNMENT
# ============================================================================

def align_timeframes(m5_df, m15_df, h1_df):
    """
    Align multi-timeframe data to ensure proper synchronization.
    Each M5 candle is aligned with its corresponding M15 and H1 candles.
    
    Returns:
        DataFrame with aligned data
    """
    # Create a copy of M5 data
    aligned = m5_df.copy()
    
    # For each M5 candle, find the corresponding M15 and H1 candle
    # We'll use forward fill to propagate HTF values
    aligned['m15_open'] = np.nan
    aligned['m15_high'] = np.nan
    aligned['m15_low'] = np.nan
    aligned['m15_close'] = np.nan
    
    aligned['h1_open'] = np.nan
    aligned['h1_high'] = np.nan
    aligned['h1_low'] = np.nan
    aligned['h1_close'] = np.nan
    
    # Resample M5 to M15 and H1 levels
    for idx in aligned.index:
        # Find the M15 candle (round down to 15-minute boundary)
        m15_time = idx.replace(minute=(idx.minute // 15) * 15, second=0, microsecond=0)
        if m15_time in m15_df.index:
            aligned.loc[idx, 'm15_open'] = m15_df.loc[m15_time, 'Open']
            aligned.loc[idx, 'm15_high'] = m15_df.loc[m15_time, 'High']
            aligned.loc[idx, 'm15_low'] = m15_df.loc[m15_time, 'Low']
            aligned.loc[idx, 'm15_close'] = m15_df.loc[m15_time, 'Close']
        
        # Find the H1 candle (round down to hour boundary)
        h1_time = idx.replace(minute=0, second=0, microsecond=0)
        if h1_time in h1_df.index:
            aligned.loc[idx, 'h1_open'] = h1_df.loc[h1_time, 'Open']
            aligned.loc[idx, 'h1_high'] = h1_df.loc[h1_time, 'High']
            aligned.loc[idx, 'h1_low'] = h1_df.loc[h1_time, 'Low']
            aligned.loc[idx, 'h1_close'] = h1_df.loc[h1_time, 'Close']
    
    # Forward fill HTF data
    aligned['m15_open'] = aligned['m15_open'].ffill()
    aligned['m15_high'] = aligned['m15_high'].ffill()
    aligned['m15_low'] = aligned['m15_low'].ffill()
    aligned['m15_close'] = aligned['m15_close'].ffill()
    
    aligned['h1_open'] = aligned['h1_open'].ffill()
    aligned['h1_high'] = aligned['h1_high'].ffill()
    aligned['h1_low'] = aligned['h1_low'].ffill()
    aligned['h1_close'] = aligned['h1_close'].ffill()
    
    return aligned


# ============================================================================
# STRATEGY LOGIC
# ============================================================================

class LiquiditySweepFVGStrategy:
    """
    Liquidity Sweep with FVG Confirmation Strategy
    
    Entry Rules (SHORT setup):
    1. Context Setup (H1 or M15):
       - Type A: Price sweeps a previous Swing High (preferably with wick)
       - Type B: Price touches/tests an old Bearish FVG
    
    2. M5 Validation:
       - During the upward leg, a Bullish FVG forms on M5
    
    3. Entry Signal:
       - Price reverses and closes BELOW the M5 Bullish FVG
       - Entry at close of M5 candle that breaks the FVG
    
    Risk Management:
       - SL: Highest point of the sweep (absolute high)
       - TP: RR 1, 1.5, and 2
    """
    
    def __init__(self, m5_df, m15_df, h1_df):
        """Initialize the strategy with multi-timeframe data."""
        self.m5 = m5_df
        self.m15 = m15_df
        self.h1 = h1_df
        
        # Create index arrays for binary search
        self.m5_times = m5_df.index.values
        self.m15_times = m15_df.index.values
        self.h1_times = h1_df.index.values
        
        # Detect FVGs on all timeframes using vectorized operations
        print("Detecting FVGs on M5 (vectorized)...")
        self.m5_fvgs = detect_fvgs_vectorized(self.m5)
        print(f"Found {len(self.m5_fvgs)} FVGs on M5")
        
        # Cache bullish FVGs separately for faster lookups
        self.m5_bullish_fvgs_cache = [fvg for fvg in self.m5_fvgs if fvg['type'] == 'bullish']
        print(f"  - {len(self.m5_bullish_fvgs_cache)} Bullish FVGs on M5")
        
        # Build bullish FVG index arrays for faster searching
        self.m5_bullish_fvg_times = np.array([fvg['datetime'] for fvg in self.m5_bullish_fvgs_cache])
        
        print("Detecting FVGs on M15 (vectorized)...")
        self.m15_fvgs = detect_fvgs_vectorized(self.m15)
        print(f"Found {len(self.m15_fvgs)} FVGs on M15")
        
        # Cache bearish FVGs for faster lookups
        self.m15_bearish_fvgs_cache = [fvg for fvg in self.m15_fvgs if fvg['type'] == 'bearish']
        
        print("Detecting FVGs on H1 (vectorized)...")
        self.h1_fvgs = detect_fvgs_vectorized(self.h1)
        print(f"Found {len(self.h1_fvgs)} FVGs on H1")
        
        # Cache bearish FVGs for faster lookups
        self.h1_bearish_fvgs_cache = [fvg for fvg in self.h1_fvgs if fvg['type'] == 'bearish']
        
        # Detect swing points using vectorized operations
        print("Detecting Swing Points on M15 (vectorized)...")
        self.m15_swings = detect_swing_points_vectorized(self.m15, lookback=5)
        print(f"Found {len(self.m15_swings)} swing points on M15")
        
        # Cache swing highs for faster lookups
        self.m15_swing_highs = [s for s in self.m15_swings if s['type'] == 'high']
        
        print("Detecting Swing Points on H1 (vectorized)...")
        self.h1_swings = detect_swing_points_vectorized(self.h1, lookback=5)
        print(f"Found {len(self.h1_swings)} swing points on H1")
        
        # Cache swing highs for faster lookups
        self.h1_swing_highs = [s for s in self.h1_swings if s['type'] == 'high']
        
        # Results storage
        self.trades = []
    
    def check_swing_sweep(self, current_idx, timeframe='h1'):
        """
        Check if current price action represents a swing high sweep.
        
        Type A Setup: Price exceeds a previous Swing High.
        
        Returns:
            Dictionary with sweep information or None
        """
        if timeframe == 'h1':
            df = self.h1
            swings = self.h1_swing_highs
        else:  # m15
            df = self.m15
            swings = self.m15_swing_highs
        
        current_high = df['High'].iloc[current_idx]
        current_time = df.index[current_idx]
        
        # Only consider swings from the last N candles (adjustable)
        max_lookback = 50 if timeframe == 'h1' else 100
        min_idx = max(0, current_idx - max_lookback)
        
        # Look for previous swing highs that have been swept (reverse order for most recent)
        for swing in reversed(swings):
            if swing['index'] >= current_idx:
                continue  # Skip future swings
            if swing['index'] < min_idx:
                break  # Too far back
            
            # Check if we swept this swing high
            if current_high > swing['price']:
                return {
                    'type': 'swing_sweep',
                    'timeframe': timeframe,
                    'sweep_high': current_high,
                    'swept_level': swing['price'],
                    'datetime': current_time,
                    'index': current_idx
                }
        
        return None
    
    def check_fvg_mitigation(self, current_idx, timeframe='h1'):
        """
        Check if current price is touching/testing an old Bearish FVG.
        
        Type B Setup: Price touches old Bearish FVG.
        
        Returns:
            Dictionary with FVG mitigation information or None
        """
        if timeframe == 'h1':
            df = self.h1
            fvgs = self.h1_bearish_fvgs_cache
        else:  # m15
            df = self.m15
            fvgs = self.m15_bearish_fvgs_cache
        
        current_high = df['High'].iloc[current_idx]
        current_low = df['Low'].iloc[current_idx]
        current_time = df.index[current_idx]
        
        # Only consider FVGs from the last N candles
        max_lookback = 50 if timeframe == 'h1' else 100
        min_idx = max(0, current_idx - max_lookback)
        
        # Look for previous bearish FVGs that are being tested (reverse order)
        for fvg in reversed(fvgs):
            if fvg['index'] >= current_idx:
                continue  # Skip future FVGs
            if fvg['index'] < min_idx:
                break  # Too far back
            
            # Check if current candle touches the FVG zone
            if current_high >= fvg['bottom'] and current_low <= fvg['top']:
                return {
                    'type': 'fvg_mitigation',
                    'timeframe': timeframe,
                    'fvg_top': fvg['top'],
                    'fvg_bottom': fvg['bottom'],
                    'sweep_high': current_high,
                    'datetime': current_time,
                    'index': current_idx
                }
        
        return None
    
    def find_m5_bullish_fvg_in_range(self, start_time, end_time):
        """
        Find Bullish FVGs on M5 that formed during the upward leg using binary search.
        
        Args:
            start_time: Start of the range
            end_time: End of the range
        
        Returns:
            List of Bullish FVGs formed in the range
        """
        if len(self.m5_bullish_fvgs_cache) == 0:
            return []
        
        # Binary search for start and end indices
        start_idx = bisect.bisect_left(self.m5_bullish_fvg_times, start_time)
        end_idx = bisect.bisect_right(self.m5_bullish_fvg_times, end_time)
        
        return self.m5_bullish_fvgs_cache[start_idx:end_idx]
    
    def check_fvg_inversion(self, fvg, start_idx):
        """
        Check if price closes below a Bullish FVG (inversion) using binary search.
        
        Args:
            fvg: The M5 Bullish FVG to check
            start_idx: M5 index to start checking from
        
        Returns:
            Dictionary with entry information or None
        """
        # Use binary search to find FVG index in M5
        fvg_time = fvg['datetime']
        fvg_m5_idx = self.m5.index.get_loc(fvg_time) if fvg_time in self.m5.index else None
        
        if fvg_m5_idx is None:
            # Use binary search on index array
            idx = bisect.bisect_left(self.m5_times, fvg_time)
            if idx < len(self.m5_times) and self.m5_times[idx] == fvg_time:
                fvg_m5_idx = idx
            else:
                return None
        
        # Vectorized check for inversion
        end_idx = min(fvg_m5_idx + 50, len(self.m5))
        if fvg_m5_idx + 1 >= end_idx:
            return None
        
        close_prices = self.m5['Close'].iloc[fvg_m5_idx + 1:end_idx].values
        inversion_mask = close_prices < fvg['bottom']
        
        if np.any(inversion_mask):
            # Find first inversion
            first_inversion_offset = np.argmax(inversion_mask)
            inversion_idx = fvg_m5_idx + 1 + first_inversion_offset
            
            return {
                'entry_price': float(close_prices[first_inversion_offset]),
                'entry_time': self.m5.index[inversion_idx],
                'entry_idx': inversion_idx,
                'fvg_bottom': fvg['bottom'],
                'fvg_top': fvg['top']
            }
        
        return None
    
    def run_backtest(self, start_date=None, end_date=None):
        """
        Run the complete backtest strategy.
        
        Process:
        1. Scan H1 and M15 for Type A (Swing Sweep) or Type B (FVG Mitigation) setups
        2. For each setup, check if M5 Bullish FVG formed during the upward leg
        3. Check if price inverted (closed below) the M5 FVG
        4. Calculate trade results with RR 1, 1.5, 2
        """
        print("\n" + "="*80)
        print("RUNNING LIQUIDITY SWEEP WITH FVG BACKTEST")
        print("="*80 + "\n")
        
        # Use full data for scanning, just filter results by date
        h1_data = self.h1
        m15_data = self.m15
        m5_data = self.m5
        
        # Determine index ranges for date filtering
        start_idx_h1 = 10
        end_idx_h1 = len(h1_data)
        start_idx_m15 = 10
        end_idx_m15 = len(m15_data)
        
        if start_date:
            start_date = pd.Timestamp(start_date)
            start_idx_h1 = max(10, h1_data.index.get_indexer([start_date], method='bfill')[0])
            start_idx_m15 = max(10, m15_data.index.get_indexer([start_date], method='bfill')[0])
        
        if end_date:
            end_date = pd.Timestamp(end_date)
            end_idx_h1 = min(len(h1_data), h1_data.index.get_indexer([end_date], method='ffill')[0] + 1)
            end_idx_m15 = min(len(m15_data), m15_data.index.get_indexer([end_date], method='ffill')[0] + 1)
        
        print(f"Date range: {start_date if start_date else 'start'} to {end_date if end_date else 'end'}")
        print(f"H1 scan range: index {start_idx_h1} to {end_idx_h1} ({end_idx_h1 - start_idx_h1} candles)")
        print(f"M15 scan range: index {start_idx_m15} to {end_idx_m15} ({end_idx_m15 - start_idx_m15} candles)")
        
        # Scan through H1 timeframe
        print("\nScanning H1 for setups...")
        h1_setups_found = 0
        h1_with_m5_fvg = 0
        h1_with_inversion = 0
        h1_total = end_idx_h1 - start_idx_h1
        
        for i in range(start_idx_h1, end_idx_h1):
            # Progress indicator every 1000 candles
            if (i - start_idx_h1) % 1000 == 0 and i > start_idx_h1:
                progress_pct = ((i - start_idx_h1) / h1_total) * 100
                print(f"  H1 Progress: {i - start_idx_h1}/{h1_total} ({progress_pct:.1f}%) - Trades: {len(self.trades)}")
            
            # Check for Type A: Swing Sweep
            sweep = self.check_swing_sweep(i, timeframe='h1')
            
            # Check for Type B: FVG Mitigation
            fvg_mitig = self.check_fvg_mitigation(i, timeframe='h1')
            
            setup = sweep or fvg_mitig
            
            if setup:
                h1_setups_found += 1
                # Found a setup, now look for M5 validation
                setup_time = setup['datetime']
                sweep_high = setup['sweep_high']
                
                # Define the upward leg window (last 5 H1 candles = ~5 hours)
                leg_start = h1_data.index[max(0, i-5)]
                leg_end = setup_time
                
                # Find M5 Bullish FVGs in this range
                m5_fvgs = self.find_m5_bullish_fvg_in_range(leg_start, leg_end)
                
                if m5_fvgs:
                    h1_with_m5_fvg += 1
                    # Use the most recent Bullish FVG
                    latest_fvg = max(m5_fvgs, key=lambda x: x['datetime'])
                    
                    # Use binary search to find M5 index for the setup time
                    m5_idx = bisect.bisect_left(self.m5_times, setup_time)
                    
                    if m5_idx < len(self.m5_times):
                        # Check for FVG inversion
                        entry = self.check_fvg_inversion(latest_fvg, m5_idx)
                        
                        if entry:
                            h1_with_inversion += 1
                            # Calculate trade parameters
                            entry_price = entry['entry_price']
                            sl_price = sweep_high
                            risk = sl_price - entry_price
                            
                            # Skip if risk is negative or too large
                            if risk <= 0 or risk > 500:
                                continue
                            
                            # Calculate TP levels
                            tp1 = entry_price - risk * 1.0  # RR 1:1
                            tp2 = entry_price - risk * 1.5  # RR 1:1.5
                            tp3 = entry_price - risk * 2.0  # RR 1:2
                            
                            # Simulate trade outcomes
                            outcome = self.simulate_trade(
                                entry['entry_idx'],
                                entry_price,
                                sl_price,
                                tp1, tp2, tp3
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
                                'setup_type': setup['type'],
                                'timeframe': setup['timeframe'],
                                'sweep_high': sweep_high,
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
        
        print(f"\nH1 Results: {h1_setups_found} setups found, {h1_with_m5_fvg} with M5 FVG, {h1_with_inversion} with inversion")
        
        # Scan through M15 timeframe
        print("\nScanning M15 for setups...")
        m15_setups_found = 0
        m15_with_m5_fvg = 0
        m15_with_inversion = 0
        m15_total = end_idx_m15 - start_idx_m15
        
        for i in range(start_idx_m15, end_idx_m15):
            # Progress indicator every 1000 candles
            if (i - start_idx_m15) % 1000 == 0 and i > start_idx_m15:
                progress_pct = ((i - start_idx_m15) / m15_total) * 100
                print(f"  M15 Progress: {i - start_idx_m15}/{m15_total} ({progress_pct:.1f}%) - Trades: {len(self.trades)}")
            
            # Check for Type A: Swing Sweep
            sweep = self.check_swing_sweep(i, timeframe='m15')
            
            # Check for Type B: FVG Mitigation
            fvg_mitig = self.check_fvg_mitigation(i, timeframe='m15')
            
            setup = sweep or fvg_mitig
            
            if setup:
                m15_setups_found += 1
                # Found a setup, now look for M5 validation
                setup_time = setup['datetime']
                sweep_high = setup['sweep_high']
                
                # Define the upward leg window (last 10 M15 candles = ~2.5 hours)
                leg_start = m15_data.index[max(0, i-10)]
                leg_end = setup_time
                
                # Find M5 Bullish FVGs in this range
                m5_fvgs = self.find_m5_bullish_fvg_in_range(leg_start, leg_end)
                
                if m5_fvgs:
                    m15_with_m5_fvg += 1
                    # Use the most recent Bullish FVG
                    latest_fvg = max(m5_fvgs, key=lambda x: x['datetime'])
                    
                    # Use binary search to find M5 index for the setup time
                    m5_idx = bisect.bisect_left(self.m5_times, setup_time)
                    
                    if m5_idx < len(self.m5_times):
                        # Check for FVG inversion
                        entry = self.check_fvg_inversion(latest_fvg, m5_idx)
                        
                        if entry:
                            m15_with_inversion += 1
                            # Calculate trade parameters
                            entry_price = entry['entry_price']
                            sl_price = sweep_high
                            risk = sl_price - entry_price
                            
                            # Skip if risk is negative or too large
                            if risk <= 0 or risk > 500:
                                continue
                            
                            # Calculate TP levels
                            tp1 = entry_price - risk * 1.0  # RR 1:1
                            tp2 = entry_price - risk * 1.5  # RR 1:1.5
                            tp3 = entry_price - risk * 2.0  # RR 1:2
                            
                            # Simulate trade outcomes
                            outcome = self.simulate_trade(
                                entry['entry_idx'],
                                entry_price,
                                sl_price,
                                tp1, tp2, tp3
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
                                'setup_type': setup['type'],
                                'timeframe': setup['timeframe'],
                                'sweep_high': sweep_high,
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
        
        print(f"\nM15 Results: {m15_setups_found} setups found, {m15_with_m5_fvg} with M5 FVG, {m15_with_inversion} with inversion")
        print(f"\nBacktest complete. Found {len(self.trades)} trades.")
        
        return self.trades
    
    def simulate_trade(self, entry_idx, entry_price, sl_price, tp1, tp2, tp3, max_bars=100):
        """
        Simulate trade outcomes for SHORT position using vectorized operations.
        
        Args:
            entry_idx: M5 index of entry
            entry_price: Entry price
            sl_price: Stop loss price
            tp1, tp2, tp3: Take profit levels
            max_bars: Maximum bars to hold the trade
        
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
        
        # Get the price data for the trade period
        end_idx = min(entry_idx + max_bars, len(self.m5))
        if entry_idx + 1 >= end_idx:
            return outcome
        
        high = self.m5['High'].iloc[entry_idx + 1:end_idx].values
        low = self.m5['Low'].iloc[entry_idx + 1:end_idx].values
        
        # Find where SL is hit (price goes up for SHORT)
        sl_hit_mask = high >= sl_price
        sl_hit_idx = np.argmax(sl_hit_mask) if np.any(sl_hit_mask) else len(high)
        
        # Find where each TP is hit (price goes down for SHORT)
        tp1_hit_mask = low <= tp1
        tp2_hit_mask = low <= tp2
        tp3_hit_mask = low <= tp3
        
        tp1_hit_idx = np.argmax(tp1_hit_mask) if np.any(tp1_hit_mask) else len(low)
        tp2_hit_idx = np.argmax(tp2_hit_mask) if np.any(tp2_hit_mask) else len(low)
        tp3_hit_idx = np.argmax(tp3_hit_mask) if np.any(tp3_hit_mask) else len(low)
        
        # Check TP1
        if tp1_hit_idx < sl_hit_idx:
            outcome['rr1'] = 'Win'
            outcome['exit_date_rr1'] = self.m5.index[entry_idx + 1 + tp1_hit_idx]
        elif sl_hit_idx < len(high):
            outcome['exit_date_rr1'] = self.m5.index[entry_idx + 1 + sl_hit_idx]
        
        # Check TP1.5
        if tp2_hit_idx < sl_hit_idx:
            outcome['rr1.5'] = 'Win'
            outcome['exit_date_rr1.5'] = self.m5.index[entry_idx + 1 + tp2_hit_idx]
        elif sl_hit_idx < len(high):
            outcome['exit_date_rr1.5'] = self.m5.index[entry_idx + 1 + sl_hit_idx]
        
        # Check TP2
        if tp3_hit_idx < sl_hit_idx:
            outcome['rr2'] = 'Win'
            outcome['exit_date_rr2'] = self.m5.index[entry_idx + 1 + tp3_hit_idx]
        elif sl_hit_idx < len(high):
            outcome['exit_date_rr2'] = self.m5.index[entry_idx + 1 + sl_hit_idx]
        
        return outcome
    
    def get_results_dataframe(self):
        """
        Convert trades to DataFrame with results.
        
        Returns:
            DataFrame with trade details and outcomes
        """
        if not self.trades:
            return pd.DataFrame()
        
        df = pd.DataFrame(self.trades)
        
        return df
    
    def calculate_statistics(self):
        """
        Calculate win rates and other statistics.
        
        Returns:
            Dictionary with statistics
        """
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
        
        stats = {
            'total_trades': total,
            'winrate_rr1': (wins_rr1 / total * 100) if total > 0 else 0,
            'winrate_rr1.5': (wins_rr1_5 / total * 100) if total > 0 else 0,
            'winrate_rr2': (wins_rr2 / total * 100) if total > 0 else 0,
            'wins_rr1': wins_rr1,
            'wins_rr1.5': wins_rr1_5,
            'wins_rr2': wins_rr2
        }
        
        return stats


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main(base_path=None):
    """Main execution function.
    
    Args:
        base_path: Directory containing the CSV data files. 
                   Defaults to script directory if not specified.
    """
    print("="*80)
    print("LIQUIDITY SWEEP WITH FVG CONFIRMATION BACKTEST")
    print("="*80)
    print()
    
    # Configuration
    if base_path is None:
        base_path = os.path.dirname(os.path.abspath(__file__))
    
    # Load data
    print("Loading data...")
    try:
        m5_df = load_nq_data(base_path, '5m')
        m15_df = load_nq_data(base_path, '15m')
        h1_df = load_nq_data(base_path, '1H')
    except Exception as e:
        print(f"Error loading data: {e}")
        return
    
    print(f"\nData loaded successfully!")
    print(f"M5: {len(m5_df)} candles from {m5_df.index[0]} to {m5_df.index[-1]}")
    print(f"M15: {len(m15_df)} candles from {m15_df.index[0]} to {m15_df.index[-1]}")
    print(f"H1: {len(h1_df)} candles from {h1_df.index[0]} to {h1_df.index[-1]}")
    
    # For testing/faster results, optionally limit to a date range
    # Uncomment to test with smaller dataset
    # start_test = pd.Timestamp('2024-01-01')
    # end_test = pd.Timestamp('2024-12-31')
    # m5_df = m5_df[start_test:end_test]
    # m15_df = m15_df[start_test:end_test]
    # h1_df = h1_df[start_test:end_test]
    # print(f"\nUsing subset for testing: {start_test} to {end_test}")
    
    # Initialize strategy
    print("\n" + "="*80)
    print("INITIALIZING STRATEGY")
    print("="*80)
    strategy = LiquiditySweepFVGStrategy(m5_df, m15_df, h1_df)
    
    # Run backtest
    # For testing with specific date range, uncomment below:
    # trades = strategy.run_backtest(start_date='2024-01-01', end_date='2024-12-31')
    
    # Run full backtest (all available data)
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
    
    # Save results to CSV
    if not results_df.empty:
        output_file = os.path.join(base_path, 'liquidity_sweep_fvg_results.csv')
        results_df.to_csv(output_file, index=False)
        print(f"\nResults saved to: {output_file}")
        
        # Display first few trades
        print("\n" + "="*80)
        print("SAMPLE TRADES (First 10)")
        print("="*80)
        print(results_df.head(10).to_string())
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

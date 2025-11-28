"""
SMC Detectors Module

This module contains functions for detecting Smart Money Concepts patterns:
- Accumulation phases (consolidation zones)
- Liquidity sweeps (temporary breakouts)
- Fair Value Gaps (FVGs)
- FVG break confirmations
"""

import pandas as pd
import numpy as np
from typing import Tuple, Optional, List, Dict


def detect_accumulation(df: pd.DataFrame, lookback: int = 20, 
                        range_threshold_pct: float = 0.5,
                        min_candles: int = 10) -> pd.Series:
    """
    Detect accumulation zones (consolidation/range periods).
    
    An accumulation zone is identified when price moves within a tight range
    for a minimum number of candles.
    
    Args:
        df: DataFrame with OHLC data
        lookback: Number of candles to analyze
        range_threshold_pct: Maximum percentage range for consolidation
        min_candles: Minimum candles to confirm accumulation
        
    Returns:
        Series of boolean values indicating accumulation zones
    """
    accumulation = pd.Series(False, index=df.index)
    
    if len(df) < lookback:
        return accumulation
    
    # Calculate rolling high and low
    rolling_high = df['High'].rolling(window=lookback).max()
    rolling_low = df['Low'].rolling(window=lookback).min()
    
    # Calculate range as percentage of average price
    avg_price = (rolling_high + rolling_low) / 2
    range_pct = ((rolling_high - rolling_low) / avg_price) * 100
    
    # Identify accumulation zones
    accumulation = range_pct <= range_threshold_pct
    
    # Require minimum consecutive candles in range
    for i in range(len(accumulation)):
        if i < min_candles:
            accumulation.iloc[i] = False
        elif accumulation.iloc[i]:
            # Check if we've been in accumulation for min_candles
            consecutive = 0
            for j in range(max(0, i - min_candles + 1), i + 1):
                if accumulation.iloc[j]:
                    consecutive += 1
                else:
                    consecutive = 0
            if consecutive < min_candles:
                accumulation.iloc[i] = False
    
    return accumulation


def detect_swing_highs_lows(df: pd.DataFrame, lookback: int = 10) -> Tuple[pd.Series, pd.Series]:
    """
    Detect swing highs and swing lows.
    
    Args:
        df: DataFrame with OHLC data
        lookback: Number of candles on each side to confirm swing
        
    Returns:
        Tuple of (swing_highs, swing_lows) as Series
    """
    swing_highs = pd.Series(np.nan, index=df.index)
    swing_lows = pd.Series(np.nan, index=df.index)
    
    half_lookback = lookback // 2
    
    for i in range(half_lookback, len(df) - half_lookback):
        # Check for swing high
        left_highs = df['High'].iloc[i - half_lookback:i]
        right_highs = df['High'].iloc[i + 1:i + half_lookback + 1]
        current_high = df['High'].iloc[i]
        
        if current_high >= left_highs.max() and current_high >= right_highs.max():
            swing_highs.iloc[i] = current_high
        
        # Check for swing low
        left_lows = df['Low'].iloc[i - half_lookback:i]
        right_lows = df['Low'].iloc[i + 1:i + half_lookback + 1]
        current_low = df['Low'].iloc[i]
        
        if current_low <= left_lows.min() and current_low <= right_lows.min():
            swing_lows.iloc[i] = current_low
    
    return swing_highs, swing_lows


def detect_liquidity_sweep(df: pd.DataFrame, lookback: int = 10,
                           sweep_threshold_pct: float = 0.1,
                           max_close_beyond_pct: float = 0.05) -> Tuple[pd.Series, pd.Series]:
    """
    Detect liquidity sweeps (false breakouts beyond swing highs/lows).
    
    A liquidity sweep occurs when price temporarily breaks a key level
    but closes back within the range, trapping traders.
    
    Args:
        df: DataFrame with OHLC data
        lookback: Candles to look back for swing points
        sweep_threshold_pct: Minimum sweep beyond level (percentage)
        max_close_beyond_pct: Maximum close beyond level (percentage)
        
    Returns:
        Tuple of (bullish_sweeps, bearish_sweeps) as Series
    """
    bullish_sweeps = pd.Series(False, index=df.index)  # Sweep of lows (bullish signal)
    bearish_sweeps = pd.Series(False, index=df.index)  # Sweep of highs (bearish signal)
    
    swing_highs, swing_lows = detect_swing_highs_lows(df, lookback)
    
    for i in range(lookback, len(df)):
        current_candle = df.iloc[i]
        
        # Look for recent swing high
        recent_swing_high = swing_highs.iloc[max(0, i - lookback):i].dropna()
        if len(recent_swing_high) > 0:
            highest_swing = recent_swing_high.max()
            sweep_threshold = highest_swing * (1 + sweep_threshold_pct / 100)
            close_threshold = highest_swing * (1 + max_close_beyond_pct / 100)
            
            # Bearish sweep: wick goes above but closes below or near swing high
            if current_candle['High'] > sweep_threshold and current_candle['Close'] < close_threshold:
                bearish_sweeps.iloc[i] = True
        
        # Look for recent swing low
        recent_swing_low = swing_lows.iloc[max(0, i - lookback):i].dropna()
        if len(recent_swing_low) > 0:
            lowest_swing = recent_swing_low.min()
            sweep_threshold = lowest_swing * (1 - sweep_threshold_pct / 100)
            close_threshold = lowest_swing * (1 - max_close_beyond_pct / 100)
            
            # Bullish sweep: wick goes below but closes above or near swing low
            if current_candle['Low'] < sweep_threshold and current_candle['Close'] > close_threshold:
                bullish_sweeps.iloc[i] = True
    
    return bullish_sweeps, bearish_sweeps


def detect_fvg(df: pd.DataFrame, min_gap_pct: float = 0.05,
               max_gap_pct: float = 2.0) -> Tuple[List[Dict], List[Dict]]:
    """
    Detect Fair Value Gaps (FVGs).
    
    A FVG is a gap between candle 1's wick and candle 3's wick,
    where candle 2 creates the gap.
    
    Bullish FVG: Gap between candle 1's high and candle 3's low
    Bearish FVG: Gap between candle 1's low and candle 3's high
    
    Args:
        df: DataFrame with OHLC data
        min_gap_pct: Minimum gap size as percentage
        max_gap_pct: Maximum gap size as percentage
        
    Returns:
        Tuple of (bullish_fvgs, bearish_fvgs) as lists of dictionaries
    """
    bullish_fvgs = []  # Bullish FVG = gap to fill above (price should go up)
    bearish_fvgs = []  # Bearish FVG = gap to fill below (price should go down)
    
    for i in range(2, len(df)):
        candle_1 = df.iloc[i - 2]
        candle_2 = df.iloc[i - 1]
        candle_3 = df.iloc[i]
        
        avg_price = candle_2['Close']
        
        # Bullish FVG: candle 3's low is above candle 1's high
        if candle_3['Low'] > candle_1['High']:
            gap_size = candle_3['Low'] - candle_1['High']
            gap_pct = (gap_size / avg_price) * 100
            
            if min_gap_pct <= gap_pct <= max_gap_pct:
                bullish_fvgs.append({
                    'index': i,
                    'datetime': df.index[i],
                    'top': candle_3['Low'],
                    'bottom': candle_1['High'],
                    'gap_size': gap_size,
                    'gap_pct': gap_pct,
                    'type': 'bullish'
                })
        
        # Bearish FVG: candle 3's high is below candle 1's low
        if candle_3['High'] < candle_1['Low']:
            gap_size = candle_1['Low'] - candle_3['High']
            gap_pct = (gap_size / avg_price) * 100
            
            if min_gap_pct <= gap_pct <= max_gap_pct:
                bearish_fvgs.append({
                    'index': i,
                    'datetime': df.index[i],
                    'top': candle_1['Low'],
                    'bottom': candle_3['High'],
                    'gap_size': gap_size,
                    'gap_pct': gap_pct,
                    'type': 'bearish'
                })
    
    return bullish_fvgs, bearish_fvgs


def check_fvg_break(df: pd.DataFrame, fvg: Dict, 
                    confirmation_candles: int = 3) -> Optional[Dict]:
    """
    Check if an FVG has been broken with a closing confirmation.
    
    For a BUY signal: Price must close ABOVE a bearish FVG
    For a SELL signal: Price must close BELOW a bullish FVG
    
    Args:
        df: DataFrame with OHLC data
        fvg: FVG dictionary from detect_fvg
        confirmation_candles: Number of candles to check after FVG
        
    Returns:
        Dictionary with break details or None if no break
    """
    fvg_idx = fvg['index']
    end_idx = min(fvg_idx + confirmation_candles + 1, len(df))
    
    for i in range(fvg_idx + 1, end_idx):
        candle = df.iloc[i]
        
        if fvg['type'] == 'bearish':
            # For bearish FVG, check if price closes above the FVG top
            # This is a BUY signal
            if candle['Close'] > fvg['top']:
                return {
                    'break_index': i,
                    'break_datetime': df.index[i],
                    'break_price': candle['Close'],
                    'signal': 'BUY',
                    'fvg': fvg,
                    'confirmation_candle': candle
                }
        
        elif fvg['type'] == 'bullish':
            # For bullish FVG, check if price closes below the FVG bottom
            # This is a SELL signal
            if candle['Close'] < fvg['bottom']:
                return {
                    'break_index': i,
                    'break_datetime': df.index[i],
                    'break_price': candle['Close'],
                    'signal': 'SELL',
                    'fvg': fvg,
                    'confirmation_candle': candle
                }
    
    return None


def find_valid_entries(df_15m: pd.DataFrame, df_5m: pd.DataFrame,
                       config: Dict) -> List[Dict]:
    """
    Find valid trading entries based on SMC strategy.
    
    Strategy flow:
    1. Detect FVG on 5m (FVG must be formed FIRST)
    2. Detect liquidity sweep on 15m and 5m AFTER the FVG
    3. Confirm entry when FVG is broken AFTER the sweep
    
    Args:
        df_15m: 15-minute DataFrame
        df_5m: 5-minute DataFrame
        config: Configuration dictionary
        
    Returns:
        List of valid entry signals
    """
    entries = []
    
    # Get config parameters
    sweep_config = config.get('liquidity_sweep', {})
    fvg_config = config.get('fvg', {})
    
    # Detect liquidity sweeps on 15m
    bullish_sweeps_15m, bearish_sweeps_15m = detect_liquidity_sweep(
        df_15m,
        lookback=sweep_config.get('lookback_periods', 10),
        sweep_threshold_pct=sweep_config.get('sweep_threshold_pct', 0.1),
        max_close_beyond_pct=sweep_config.get('max_close_beyond_pct', 0.05)
    )
    
    # Detect liquidity sweeps on 5m
    bullish_sweeps_5m, bearish_sweeps_5m = detect_liquidity_sweep(
        df_5m,
        lookback=sweep_config.get('lookback_periods', 10),
        sweep_threshold_pct=sweep_config.get('sweep_threshold_pct', 0.1),
        max_close_beyond_pct=sweep_config.get('max_close_beyond_pct', 0.05)
    )
    
    # Detect FVGs on 5m
    bullish_fvgs, bearish_fvgs = detect_fvg(
        df_5m,
        min_gap_pct=fvg_config.get('min_gap_pct', 0.05),
        max_gap_pct=fvg_config.get('max_gap_pct', 2.0)
    )
    
    # NEW LOGIC: FVG must be formed BEFORE the liquidity sweep
    # After the sweep, if FVG is broken, we enter the position
    
    all_fvgs = bullish_fvgs + bearish_fvgs
    confirmation_candles = fvg_config.get('confirmation_candles', 3)
    
    for fvg in all_fvgs:
        fvg_time = fvg['datetime']
        fvg_idx = fvg['index']
        
        # Look for a liquidity sweep AFTER the FVG formation
        # Search in candles after FVG
        sweep_found_5m = False
        sweep_found_15m = False
        sweep_idx = None
        sweep_time = None
        sweep_type = None
        
        # Search for sweep in the 20 candles after FVG on 5m
        for i in range(fvg_idx + 1, min(fvg_idx + 21, len(df_5m))):
            if bullish_sweeps_5m.iloc[i]:
                sweep_found_5m = True
                sweep_idx = i
                sweep_time = df_5m.index[i]
                sweep_type = 'bullish'
                break
            elif bearish_sweeps_5m.iloc[i]:
                sweep_found_5m = True
                sweep_idx = i
                sweep_time = df_5m.index[i]
                sweep_type = 'bearish'
                break
        
        # Also check 15m sweeps after FVG
        if not sweep_found_5m:
            mask_15m_after = df_15m.index > fvg_time
            if mask_15m_after.any():
                for idx_15m in df_15m.index[mask_15m_after][:10]:  # Check next 10 15m candles
                    pos_15m = df_15m.index.get_loc(idx_15m)
                    if pos_15m < len(bullish_sweeps_15m):
                        if bullish_sweeps_15m.iloc[pos_15m]:
                            sweep_found_15m = True
                            sweep_time = idx_15m
                            sweep_type = 'bullish'
                            # Find corresponding 5m index
                            mask_5m = df_5m.index >= sweep_time
                            if mask_5m.any():
                                sweep_idx = df_5m.index.get_loc(df_5m.index[mask_5m][0])
                            break
                        elif bearish_sweeps_15m.iloc[pos_15m]:
                            sweep_found_15m = True
                            sweep_time = idx_15m
                            sweep_type = 'bearish'
                            # Find corresponding 5m index
                            mask_5m = df_5m.index >= sweep_time
                            if mask_5m.any():
                                sweep_idx = df_5m.index.get_loc(df_5m.index[mask_5m][0])
                            break
        
        if not (sweep_found_5m or sweep_found_15m) or sweep_idx is None:
            continue
        
        # Now look for FVG break AFTER the sweep
        # Check candles after the sweep for FVG break
        for i in range(sweep_idx + 1, min(sweep_idx + confirmation_candles + 5, len(df_5m))):
            candle = df_5m.iloc[i]
            
            if fvg['type'] == 'bearish':
                # For bearish FVG, check if price closes above the FVG top -> BUY signal
                if candle['Close'] > fvg['top']:
                    entry = {
                        'datetime': df_5m.index[i],
                        'signal': 'BUY',
                        'entry_price': candle['Close'],
                        'fvg': fvg,
                        'has_sweep_15m': sweep_found_15m,
                        'has_sweep_5m': sweep_found_5m,
                        'sweep_type': sweep_type,
                        'confirmation_candle': candle
                    }
                    entries.append(entry)
                    break
            
            elif fvg['type'] == 'bullish':
                # For bullish FVG, check if price closes below the FVG bottom -> SELL signal
                if candle['Close'] < fvg['bottom']:
                    entry = {
                        'datetime': df_5m.index[i],
                        'signal': 'SELL',
                        'entry_price': candle['Close'],
                        'fvg': fvg,
                        'has_sweep_15m': sweep_found_15m,
                        'has_sweep_5m': sweep_found_5m,
                        'sweep_type': sweep_type,
                        'confirmation_candle': candle
                    }
                    entries.append(entry)
                    break
    
    return entries

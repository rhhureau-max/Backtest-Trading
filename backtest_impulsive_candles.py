#!/usr/bin/env python3
"""
Backtest Impulsive Candles Analysis

Analyzes the probability of continuation after an impulsive candle
on 1m, 5m, and 15m timeframes.

An impulsive candle is defined as:
- A candle whose range (High - Low) OR body (|Close - Open|) is greater than
  the maximum of the previous 10 candles
- AND that breaks a previous FVG (Fair Value Gap) or a previous high/low
"""

import os
import zipfile
from collections import deque
from datetime import datetime
from typing import Dict, Optional
import pandas as pd
import numpy as np


def load_csv_file(filepath: str) -> pd.DataFrame:
    """Load a CSV file with semicolon delimiter."""
    df = pd.read_csv(
        filepath,
        sep=';',
        names=['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume'],
        skiprows=1  # Skip header row
    )
    return df


def decompress_zip_file(zip_path: str) -> str:
    """Decompress a zip file and return the path to the extracted CSV."""
    extract_dir = os.path.dirname(zip_path)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        # Get the list of files in the zip
        file_list = zip_ref.namelist()
        # Extract all files
        zip_ref.extractall(extract_dir)
        # Return the path to the first CSV file
        for filename in file_list:
            if filename.endswith('.csv'):
                return os.path.join(extract_dir, filename)
    return ""


def load_timeframe_data(base_dir: str, timeframe: str) -> pd.DataFrame:
    """Load all data files for a specific timeframe."""
    all_dfs = []
    current_year = datetime.now().year
    years = range(2018, current_year + 1)

    for year in years:
        # Try different file patterns
        csv_path = os.path.join(base_dir, f"{year} {timeframe}.csv")
        zip_path = os.path.join(base_dir, f"{year} {timeframe}.csv.zip")

        if os.path.exists(csv_path):
            try:
                df = load_csv_file(csv_path)
                df['Year'] = year
                all_dfs.append(df)
                print(f"  Loaded: {year} {timeframe}.csv ({len(df)} rows)")
            except Exception as e:
                print(f"  Error loading {csv_path}: {e}")
        elif os.path.exists(zip_path):
            try:
                extracted_path = decompress_zip_file(zip_path)
                if extracted_path and os.path.exists(extracted_path):
                    df = load_csv_file(extracted_path)
                    df['Year'] = year
                    all_dfs.append(df)
                    print(f"  Loaded: {year} {timeframe}.csv.zip ({len(df)} rows)")
                    # Clean up extracted file to save space
                    os.remove(extracted_path)
            except Exception as e:
                print(f"  Error loading {zip_path}: {e}")

    if all_dfs:
        combined_df = pd.concat(all_dfs, ignore_index=True)
        return combined_df
    return pd.DataFrame()


def calculate_candle_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate range, body, and direction for each candle."""
    df = df.copy()

    # Ensure numeric types
    df['Open'] = pd.to_numeric(df['Open'], errors='coerce')
    df['High'] = pd.to_numeric(df['High'], errors='coerce')
    df['Low'] = pd.to_numeric(df['Low'], errors='coerce')
    df['Close'] = pd.to_numeric(df['Close'], errors='coerce')

    # Calculate metrics
    df['Range'] = df['High'] - df['Low']
    df['Body'] = (df['Close'] - df['Open']).abs()

    # Direction: 1 for bullish, -1 for bearish, 0 for doji
    df['Direction'] = np.where(
        df['Close'] > df['Open'], 1,
        np.where(df['Close'] < df['Open'], -1, 0)
    )

    return df


def calculate_rolling_max(df: pd.DataFrame, lookback: int = 10) -> pd.DataFrame:
    """Calculate rolling max of range and body over the lookback period."""
    df = df.copy()

    # Shift by 1 to exclude current candle, then calculate rolling max
    df['Max_Range_10'] = df['Range'].shift(1).rolling(window=lookback, min_periods=1).max()
    df['Max_Body_10'] = df['Body'].shift(1).rolling(window=lookback, min_periods=1).max()

    return df


def identify_fvg(df: pd.DataFrame) -> pd.DataFrame:
    """
    Identify Fair Value Gaps (FVG).

    Bullish FVG: Gap between candle i-2's high and candle i's low (where i is current)
    Bearish FVG: Gap between candle i-2's low and candle i's high
    """
    df = df.copy()

    # Get previous candles
    high_2_back = df['High'].shift(2)
    low_2_back = df['Low'].shift(2)

    # Bullish FVG: Current low > High of 2 candles ago
    df['Bullish_FVG'] = df['Low'] > high_2_back
    df['Bullish_FVG_Top'] = np.where(df['Bullish_FVG'], df['Low'], np.nan)
    df['Bullish_FVG_Bottom'] = np.where(df['Bullish_FVG'], high_2_back, np.nan)

    # Bearish FVG: Current high < Low of 2 candles ago
    df['Bearish_FVG'] = df['High'] < low_2_back
    df['Bearish_FVG_Top'] = np.where(df['Bearish_FVG'], low_2_back, np.nan)
    df['Bearish_FVG_Bottom'] = np.where(df['Bearish_FVG'], df['High'], np.nan)

    return df


def track_unfilled_fvg(df: pd.DataFrame, lookback: int = 50) -> pd.DataFrame:
    """
    Track unfilled FVG zones and detect when they are broken.
    A FVG is considered broken when price moves through it.
    """
    df = df.copy()
    df['Breaks_Bullish_FVG'] = False
    df['Breaks_Bearish_FVG'] = False

    # Use deque for efficient fixed-size tracking
    bullish_fvg_zones = deque(maxlen=lookback)  # deque of (bottom, top) tuples
    bearish_fvg_zones = deque(maxlen=lookback)

    breaks_bullish = []
    breaks_bearish = []

    for i in range(len(df)):
        current_low = df.iloc[i]['Low']
        current_high = df.iloc[i]['High']

        # Check for breaks of existing FVG zones
        broke_bullish = False
        broke_bearish = False

        # Check if current candle breaks any bullish FVG (price drops into it)
        new_bullish_zones = deque(maxlen=lookback)
        for bottom, top in bullish_fvg_zones:
            if current_low <= top:  # Price entered or broke through bullish FVG
                broke_bullish = True
            if current_low >= bottom:  # FVG not completely filled, keep tracking
                new_bullish_zones.append((bottom, top))
        bullish_fvg_zones = new_bullish_zones

        # Check if current candle breaks any bearish FVG (price rises into it)
        new_bearish_zones = deque(maxlen=lookback)
        for bottom, top in bearish_fvg_zones:
            if current_high >= bottom:  # Price entered or broke through bearish FVG
                broke_bearish = True
            if current_high <= top:  # FVG not completely filled, keep tracking
                new_bearish_zones.append((bottom, top))
        bearish_fvg_zones = new_bearish_zones

        breaks_bullish.append(broke_bullish)
        breaks_bearish.append(broke_bearish)

        # Add new FVGs created at this candle
        if df.iloc[i]['Bullish_FVG']:
            bottom = df.iloc[i]['Bullish_FVG_Bottom']
            top = df.iloc[i]['Bullish_FVG_Top']
            if pd.notna(bottom) and pd.notna(top):
                bullish_fvg_zones.append((bottom, top))

        if df.iloc[i]['Bearish_FVG']:
            bottom = df.iloc[i]['Bearish_FVG_Bottom']
            top = df.iloc[i]['Bearish_FVG_Top']
            if pd.notna(bottom) and pd.notna(top):
                bearish_fvg_zones.append((bottom, top))

    df['Breaks_Bullish_FVG'] = breaks_bullish
    df['Breaks_Bearish_FVG'] = breaks_bearish

    return df


def detect_structure_breaks(df: pd.DataFrame, lookback: int = 20) -> pd.DataFrame:
    """
    Detect breaks of previous highs and lows.
    """
    df = df.copy()

    # Calculate rolling max high and min low (excluding current candle)
    df['Prev_High'] = df['High'].shift(1).rolling(window=lookback, min_periods=1).max()
    df['Prev_Low'] = df['Low'].shift(1).rolling(window=lookback, min_periods=1).min()

    # Detect breaks
    df['Breaks_Prev_High'] = df['High'] > df['Prev_High']
    df['Breaks_Prev_Low'] = df['Low'] < df['Prev_Low']

    return df


def identify_impulsive_candles(df: pd.DataFrame) -> pd.DataFrame:
    """
    Identify impulsive candles based on the criteria:
    - Range or body > max of previous 10 candles
    - AND breaks a FVG or previous high/low
    """
    df = df.copy()

    # Check if range or body exceeds previous 10 candles
    df['Is_Large_Candle'] = (df['Range'] > df['Max_Range_10']) | (df['Body'] > df['Max_Body_10'])

    # Check structure break (FVG or high/low)
    df['Breaks_Structure'] = (
        df['Breaks_Bullish_FVG'] |
        df['Breaks_Bearish_FVG'] |
        df['Breaks_Prev_High'] |
        df['Breaks_Prev_Low']
    )

    # Impulsive candle: large candle + structure break
    df['Is_Impulsive'] = df['Is_Large_Candle'] & df['Breaks_Structure']

    # Classify impulsive candles as bullish or bearish
    df['Is_Bullish_Impulsive'] = df['Is_Impulsive'] & (df['Direction'] == 1)
    df['Is_Bearish_Impulsive'] = df['Is_Impulsive'] & (df['Direction'] == -1)

    return df


def analyze_continuation(df: pd.DataFrame) -> Dict:
    """
    Analyze the probability of continuation after impulsive candles.
    """
    results = {
        'total_signals': 0,
        'bullish_signals': 0,
        'bearish_signals': 0,
        'bullish_continuation': 0,
        'bearish_continuation': 0,
        'bullish_reversal': 0,
        'bearish_reversal': 0,
        'bullish_neutral': 0,
        'bearish_neutral': 0,
    }

    # Get the next candle's direction for each impulsive candle
    df['Next_Direction'] = df['Direction'].shift(-1)

    # Filter impulsive candles
    impulsive = df[df['Is_Impulsive']].copy()

    results['total_signals'] = len(impulsive)
    results['bullish_signals'] = len(impulsive[impulsive['Direction'] == 1])
    results['bearish_signals'] = len(impulsive[impulsive['Direction'] == -1])

    # Analyze bullish impulsive candles
    bullish_impulsive = impulsive[impulsive['Direction'] == 1]
    if len(bullish_impulsive) > 0:
        # Continuation: next candle is also bullish
        results['bullish_continuation'] = len(
            bullish_impulsive[bullish_impulsive['Next_Direction'] == 1]
        )
        results['bullish_reversal'] = len(
            bullish_impulsive[bullish_impulsive['Next_Direction'] == -1]
        )
        results['bullish_neutral'] = len(
            bullish_impulsive[bullish_impulsive['Next_Direction'] == 0]
        )

    # Analyze bearish impulsive candles
    bearish_impulsive = impulsive[impulsive['Direction'] == -1]
    if len(bearish_impulsive) > 0:
        # Continuation: next candle is also bearish
        results['bearish_continuation'] = len(
            bearish_impulsive[bearish_impulsive['Next_Direction'] == -1]
        )
        results['bearish_reversal'] = len(
            bearish_impulsive[bearish_impulsive['Next_Direction'] == 1]
        )
        results['bearish_neutral'] = len(
            bearish_impulsive[bearish_impulsive['Next_Direction'] == 0]
        )

    return results


def calculate_probabilities(results: Dict) -> Dict:
    """Calculate continuation and reversal probabilities."""
    probs = {
        'total_signals': results['total_signals'],
        'bullish_signals': results['bullish_signals'],
        'bearish_signals': results['bearish_signals'],
        'bullish_continuation_pct': 0.0,
        'bullish_reversal_pct': 0.0,
        'bullish_neutral_pct': 0.0,
        'bearish_continuation_pct': 0.0,
        'bearish_reversal_pct': 0.0,
        'bearish_neutral_pct': 0.0,
        'overall_continuation_pct': 0.0,
        'overall_reversal_pct': 0.0,
    }

    if results['bullish_signals'] > 0:
        probs['bullish_continuation_pct'] = (
            results['bullish_continuation'] / results['bullish_signals'] * 100
        )
        probs['bullish_reversal_pct'] = (
            results['bullish_reversal'] / results['bullish_signals'] * 100
        )
        probs['bullish_neutral_pct'] = (
            results['bullish_neutral'] / results['bullish_signals'] * 100
        )

    if results['bearish_signals'] > 0:
        probs['bearish_continuation_pct'] = (
            results['bearish_continuation'] / results['bearish_signals'] * 100
        )
        probs['bearish_reversal_pct'] = (
            results['bearish_reversal'] / results['bearish_signals'] * 100
        )
        probs['bearish_neutral_pct'] = (
            results['bearish_neutral'] / results['bearish_signals'] * 100
        )

    total_continuation = results['bullish_continuation'] + results['bearish_continuation']
    total_reversal = results['bullish_reversal'] + results['bearish_reversal']
    total_neutral = results['bullish_neutral'] + results['bearish_neutral']
    total = total_continuation + total_reversal + total_neutral

    if total > 0:
        probs['overall_continuation_pct'] = total_continuation / total * 100
        probs['overall_reversal_pct'] = total_reversal / total * 100

    return probs


def print_results(timeframe: str, probs: Dict):
    """Print results for a timeframe."""
    print(f"\n{'=' * 60}")
    print(f"TIMEFRAME: {timeframe}")
    print(f"{'=' * 60}")
    print(f"Total Impulsive Signals: {probs['total_signals']}")
    print(f"  - Bullish Signals: {probs['bullish_signals']}")
    print(f"  - Bearish Signals: {probs['bearish_signals']}")
    print()
    print("BULLISH IMPULSIVE CANDLES:")
    print(f"  Continuation Probability: {probs['bullish_continuation_pct']:.2f}%")
    print(f"  Reversal Probability: {probs['bullish_reversal_pct']:.2f}%")
    print()
    print("BEARISH IMPULSIVE CANDLES:")
    print(f"  Continuation Probability: {probs['bearish_continuation_pct']:.2f}%")
    print(f"  Reversal Probability: {probs['bearish_reversal_pct']:.2f}%")
    print()
    print("OVERALL:")
    print(f"  Continuation Probability: {probs['overall_continuation_pct']:.2f}%")
    print(f"  Reversal Probability: {probs['overall_reversal_pct']:.2f}%")


def print_summary_table(all_results: Dict[str, Dict]):
    """Print a summary table comparing all timeframes."""
    print("\n" + "=" * 80)
    print("SUMMARY TABLE - CONTINUATION PROBABILITIES BY TIMEFRAME")
    print("=" * 80)

    # Header
    print(f"{'Timeframe':<10} | {'Signals':<10} | {'Bull Cont %':<12} | "
          f"{'Bear Cont %':<12} | {'Overall Cont %':<14}")
    print("-" * 80)

    for tf, probs in all_results.items():
        print(f"{tf:<10} | {probs['total_signals']:<10} | "
              f"{probs['bullish_continuation_pct']:<12.2f} | "
              f"{probs['bearish_continuation_pct']:<12.2f} | "
              f"{probs['overall_continuation_pct']:<14.2f}")

    print("-" * 80)


def analyze_timeframe(base_dir: str, timeframe: str) -> Optional[Dict]:
    """Complete analysis for a single timeframe."""
    print(f"\nLoading {timeframe} data...")
    df = load_timeframe_data(base_dir, timeframe)

    if df.empty:
        print(f"No data found for timeframe {timeframe}")
        return None

    print(f"Processing {len(df)} candles for {timeframe}...")

    # Calculate all metrics
    df = calculate_candle_metrics(df)
    df = calculate_rolling_max(df)
    df = identify_fvg(df)
    df = track_unfilled_fvg(df)
    df = detect_structure_breaks(df)
    df = identify_impulsive_candles(df)

    # Analyze continuation
    results = analyze_continuation(df)
    probs = calculate_probabilities(results)

    return probs


# =============================================================================
# 8:30 AM NEW YORK OPENING CANDLE ANALYSIS
# =============================================================================

# Time constant for the New York opening candle
NY_OPENING_TIME = '08:30:00'


def analyze_830_opening_candle(df: pd.DataFrame) -> Dict:
    """
    Analyze the 8:30 AM New York opening candle.

    When the 8:30 candle is bullish, calculate the probability that the next
    candle continues bullish. Same for bearish 8:30 candles.

    Args:
        df: DataFrame with OHLC data including Time column.
            Must have reset_index(drop=True) called to ensure consecutive indexing.

    Returns:
        Dictionary with continuation statistics
    """
    results = {
        'total_830_candles': 0,
        'bullish_830_candles': 0,
        'bearish_830_candles': 0,
        'doji_830_candles': 0,
        'bullish_830_next_bullish': 0,
        'bullish_830_next_bearish': 0,
        'bullish_830_next_doji': 0,
        'bearish_830_next_bearish': 0,
        'bearish_830_next_bullish': 0,
        'bearish_830_next_doji': 0,
    }

    # Filter for 8:30 AM candles
    df_830 = df[df['Time'] == NY_OPENING_TIME].copy()
    results['total_830_candles'] = len(df_830)

    if len(df_830) == 0:
        return results

    # Get indices of 8:30 candles in original dataframe
    indices_830 = df_830.index.tolist()

    for idx in indices_830:
        # Get current 8:30 candle direction
        current_direction = df.loc[idx, 'Direction']

        # Get next candle (if exists)
        next_idx = idx + 1
        if next_idx >= len(df):
            continue

        next_direction = df.loc[next_idx, 'Direction']

        if current_direction == 1:  # Bullish 8:30 candle
            results['bullish_830_candles'] += 1
            if next_direction == 1:
                results['bullish_830_next_bullish'] += 1
            elif next_direction == -1:
                results['bullish_830_next_bearish'] += 1
            else:
                results['bullish_830_next_doji'] += 1
        elif current_direction == -1:  # Bearish 8:30 candle
            results['bearish_830_candles'] += 1
            if next_direction == -1:
                results['bearish_830_next_bearish'] += 1
            elif next_direction == 1:
                results['bearish_830_next_bullish'] += 1
            else:
                results['bearish_830_next_doji'] += 1
        else:  # Doji
            results['doji_830_candles'] += 1

    return results


def calculate_830_probabilities(results: Dict) -> Dict:
    """
    Calculate continuation and reversal probabilities for 8:30 candles.

    Args:
        results: Dictionary from analyze_830_opening_candle() containing counts
                 of 8:30 candle directions and their next candle directions.

    Returns:
        Dict containing probability percentages for continuation and reversal
        after bullish and bearish 8:30 candles.
    """
    probs = {
        'total_830_candles': results['total_830_candles'],
        'bullish_830_candles': results['bullish_830_candles'],
        'bearish_830_candles': results['bearish_830_candles'],
        'doji_830_candles': results['doji_830_candles'],
        # Bullish 8:30 candle probabilities
        'bullish_continuation_pct': 0.0,
        'bullish_reversal_pct': 0.0,
        'bullish_neutral_pct': 0.0,
        # Bearish 8:30 candle probabilities
        'bearish_continuation_pct': 0.0,
        'bearish_reversal_pct': 0.0,
        'bearish_neutral_pct': 0.0,
    }

    if results['bullish_830_candles'] > 0:
        probs['bullish_continuation_pct'] = (
            results['bullish_830_next_bullish'] / results['bullish_830_candles'] * 100
        )
        probs['bullish_reversal_pct'] = (
            results['bullish_830_next_bearish'] / results['bullish_830_candles'] * 100
        )
        probs['bullish_neutral_pct'] = (
            results['bullish_830_next_doji'] / results['bullish_830_candles'] * 100
        )

    if results['bearish_830_candles'] > 0:
        probs['bearish_continuation_pct'] = (
            results['bearish_830_next_bearish'] / results['bearish_830_candles'] * 100
        )
        probs['bearish_reversal_pct'] = (
            results['bearish_830_next_bullish'] / results['bearish_830_candles'] * 100
        )
        probs['bearish_neutral_pct'] = (
            results['bearish_830_next_doji'] / results['bearish_830_candles'] * 100
        )

    return probs


def print_830_results(timeframe: str, probs: Dict):
    """Print 8:30 AM opening candle analysis results for a timeframe."""
    print(f"\n{'=' * 60}")
    print(f"TIMEFRAME: {timeframe}")
    print(f"{'=' * 60}")
    print(f"Total 8:30 AM Candles Analyzed: {probs['total_830_candles']}")
    print(f"  - Bullish 8:30 Candles: {probs['bullish_830_candles']}")
    print(f"  - Bearish 8:30 Candles: {probs['bearish_830_candles']}")
    print(f"  - Doji 8:30 Candles: {probs['doji_830_candles']}")
    print()
    print("BULLISH 8:30 CANDLE (Close > Open):")
    print(f"  Next Candle Bullish (Continuation): {probs['bullish_continuation_pct']:.2f}%")
    print(f"  Next Candle Bearish (Reversal):     {probs['bullish_reversal_pct']:.2f}%")
    print(f"  Next Candle Doji (Neutral):         {probs['bullish_neutral_pct']:.2f}%")
    print()
    print("BEARISH 8:30 CANDLE (Close < Open):")
    print(f"  Next Candle Bearish (Continuation): {probs['bearish_continuation_pct']:.2f}%")
    print(f"  Next Candle Bullish (Reversal):     {probs['bearish_reversal_pct']:.2f}%")
    print(f"  Next Candle Doji (Neutral):         {probs['bearish_neutral_pct']:.2f}%")


def print_830_summary_table(all_results: Dict[str, Dict]):
    """Print a summary table for 8:30 AM opening candle analysis."""
    print("\n" + "=" * 90)
    print("SUMMARY TABLE - 8:30 AM NEW YORK OPENING CANDLE CONTINUATION PROBABILITIES")
    print("=" * 90)

    # Header
    print(f"{'Timeframe':<10} | {'8:30 Candles':<13} | "
          f"{'Bull→Bull %':<12} | {'Bull→Bear %':<12} | "
          f"{'Bear→Bear %':<12} | {'Bear→Bull %':<12}")
    print("-" * 90)

    for tf, probs in all_results.items():
        print(f"{tf:<10} | {probs['total_830_candles']:<13} | "
              f"{probs['bullish_continuation_pct']:<12.2f} | "
              f"{probs['bullish_reversal_pct']:<12.2f} | "
              f"{probs['bearish_continuation_pct']:<12.2f} | "
              f"{probs['bearish_reversal_pct']:<12.2f}")

    print("-" * 90)


def analyze_830_timeframe(base_dir: str, timeframe: str) -> Optional[Dict]:
    """
    Complete 8:30 AM opening candle analysis for a single timeframe.

    Args:
        base_dir: Directory containing the OHLC data files.
        timeframe: Timeframe to analyze ('1m', '5m', or '15m').

    Returns:
        Dict with probability statistics, or None if no data found.
    """
    print(f"\nLoading {timeframe} data for 8:30 AM analysis...")
    df = load_timeframe_data(base_dir, timeframe)

    if df.empty:
        print(f"No data found for timeframe {timeframe}")
        return None

    print(f"Processing {len(df)} candles for {timeframe}...")

    # Calculate candle metrics (direction)
    df = calculate_candle_metrics(df)

    # Reset index to ensure proper indexing for next candle lookup
    df = df.reset_index(drop=True)

    # Analyze 8:30 candles
    results = analyze_830_opening_candle(df)
    probs = calculate_830_probabilities(results)

    return probs


def run_830_analysis(base_dir: str):
    """
    Run the 8:30 AM New York opening candle analysis.

    Analyzes the probability of continuation after bullish/bearish 8:30 AM
    candles across 1m, 5m, and 15m timeframes. Prints detailed results and
    a summary table.

    Args:
        base_dir: Directory containing the OHLC data files.
    """
    print("\n" + "=" * 60)
    print("8:30 AM NEW YORK OPENING CANDLE ANALYSIS")
    print("Analyzing probability of continuation after the 8:30 AM candle")
    print("=" * 60)

    timeframes = ['1m', '5m', '15m']
    all_results = {}

    for tf in timeframes:
        probs = analyze_830_timeframe(base_dir, tf)
        if probs:
            all_results[tf] = probs
            print_830_results(tf, probs)

    # Print summary table
    if all_results:
        print_830_summary_table(all_results)


# =============================================================================
# 8:30 AM CANDLE CONSECUTIVE CONTINUATION ANALYSIS WITH MINIMUM BODY FILTER
# =============================================================================

# Minimum body size thresholds by timeframe (in points)
MIN_BODY_THRESHOLDS = {
    '1m': 30,
    '5m': 75,
    '15m': 100
}


def analyze_830_consecutive_candles(df: pd.DataFrame, min_body: float, max_consecutive: int = 10) -> Dict:
    """
    Analyze 8:30 AM candles with minimum body size filter and calculate
    probability of N consecutive candles following in the same direction.

    Args:
        df: DataFrame with OHLC data including Time, Body, and Direction columns.
            Must have reset_index(drop=True) called for proper indexing.
        min_body: Minimum body size (|Close - Open|) in points.
        max_consecutive: Maximum number of consecutive candles to analyze (default 10).

    Returns:
        Dictionary with:
            - bullish_qualifying: count of bullish 8:30 candles meeting body threshold
            - bearish_qualifying: count of bearish 8:30 candles meeting body threshold
            - bullish_consecutive: dict with counts of N consecutive bullish candles (2-max)
            - bearish_consecutive: dict with counts of N consecutive bearish candles (2-max)
    """
    results = {
        'bullish_qualifying': 0,
        'bearish_qualifying': 0,
        'bullish_consecutive': {n: 0 for n in range(2, max_consecutive + 1)},
        'bearish_consecutive': {n: 0 for n in range(2, max_consecutive + 1)},
    }

    # Filter for 8:30 AM candles with minimum body size
    df_830 = df[(df['Time'] == NY_OPENING_TIME) & (df['Body'] >= min_body)].copy()

    if len(df_830) == 0:
        return results

    # Get indices of qualifying 8:30 candles
    indices_830 = df_830.index.tolist()

    for idx in indices_830:
        current_direction = df.loc[idx, 'Direction']

        if current_direction == 1:  # Bullish 8:30 candle
            results['bullish_qualifying'] += 1

            # Check N consecutive bullish candles after
            for n in range(2, max_consecutive + 1):
                all_bullish = True
                for offset in range(1, n + 1):
                    next_idx = idx + offset
                    if next_idx >= len(df):
                        all_bullish = False
                        break
                    if df.loc[next_idx, 'Direction'] != 1:
                        all_bullish = False
                        break
                if all_bullish:
                    results['bullish_consecutive'][n] += 1

        elif current_direction == -1:  # Bearish 8:30 candle
            results['bearish_qualifying'] += 1

            # Check N consecutive bearish candles after
            for n in range(2, max_consecutive + 1):
                all_bearish = True
                for offset in range(1, n + 1):
                    next_idx = idx + offset
                    if next_idx >= len(df):
                        all_bearish = False
                        break
                    if df.loc[next_idx, 'Direction'] != -1:
                        all_bearish = False
                        break
                if all_bearish:
                    results['bearish_consecutive'][n] += 1

    return results


def print_830_consecutive_results(timeframe: str, min_body: float, results: Dict):
    """
    Print consecutive candle analysis results for 8:30 candles.

    Args:
        timeframe: The timeframe being analyzed ('1m', '5m', '15m').
        min_body: Minimum body size threshold in points.
        results: Dictionary from analyze_830_consecutive_candles().
    """
    print(f"\n{'=' * 70}")
    print(f"BULLISH 8:30 CANDLES (body >= {int(min_body)} points) - {timeframe}")
    print(f"{'=' * 70}")
    print(f"Total qualifying signals: {results['bullish_qualifying']}")

    if results['bullish_qualifying'] > 0:
        print("Consecutive bullish candles after:")
        for n in sorted(results['bullish_consecutive'].keys()):
            count = results['bullish_consecutive'][n]
            pct = count / results['bullish_qualifying'] * 100
            print(f"  {n} candles: {count} ({pct:.2f}%)")
    else:
        print("  No qualifying bullish 8:30 candles found.")

    print(f"\n{'=' * 70}")
    print(f"BEARISH 8:30 CANDLES (body >= {int(min_body)} points) - {timeframe}")
    print(f"{'=' * 70}")
    print(f"Total qualifying signals: {results['bearish_qualifying']}")

    if results['bearish_qualifying'] > 0:
        print("Consecutive bearish candles after:")
        for n in sorted(results['bearish_consecutive'].keys()):
            count = results['bearish_consecutive'][n]
            pct = count / results['bearish_qualifying'] * 100
            print(f"  {n} candles: {count} ({pct:.2f}%)")
    else:
        print("  No qualifying bearish 8:30 candles found.")


def analyze_830_consecutive_timeframe(base_dir: str, timeframe: str) -> Optional[Dict]:
    """
    Complete 8:30 AM consecutive candle analysis for a single timeframe.

    Args:
        base_dir: Directory containing the OHLC data files.
        timeframe: Timeframe to analyze ('1m', '5m', or '15m').

    Returns:
        Dict with analysis results, or None if no data found.
    """
    min_body = MIN_BODY_THRESHOLDS.get(timeframe)
    if min_body is None:
        print(f"No minimum body threshold defined for timeframe {timeframe}")
        return None

    print(f"\nLoading {timeframe} data for 8:30 AM consecutive analysis...")
    df = load_timeframe_data(base_dir, timeframe)

    if df.empty:
        print(f"No data found for timeframe {timeframe}")
        return None

    print(f"Processing {len(df)} candles for {timeframe}...")

    # Calculate candle metrics (Body, Direction)
    df = calculate_candle_metrics(df)

    # Reset index for proper consecutive indexing
    df = df.reset_index(drop=True)

    # Analyze 8:30 candles with consecutive continuation
    results = analyze_830_consecutive_candles(df, min_body)
    results['min_body'] = min_body
    results['timeframe'] = timeframe

    return results


def run_830_consecutive_analysis(base_dir: str):
    """
    Run the 8:30 AM consecutive candle continuation analysis.

    Filters 8:30 candles by minimum body size and calculates the probability
    of 2-10 consecutive candles following in the same direction.

    Args:
        base_dir: Directory containing the OHLC data files.
    """
    print("\n" + "=" * 70)
    print("8:30 AM CANDLE CONSECUTIVE CONTINUATION ANALYSIS")
    print("Analyzing probability of N consecutive candles after qualifying")
    print("8:30 AM candles (filtered by minimum body size)")
    print("=" * 70)

    timeframes = ['1m', '5m', '15m']

    for tf in timeframes:
        results = analyze_830_consecutive_timeframe(base_dir, tf)
        if results:
            print_830_consecutive_results(tf, results['min_body'], results)


def main():
    """Main function to run the analysis."""
    print("=" * 60)
    print("IMPULSIVE CANDLE CONTINUATION ANALYSIS")
    print("Analyzing probability of continuation after impulsive candles")
    print("=" * 60)

    # Get the base directory (where the script is located)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    if not base_dir:
        base_dir = os.getcwd()

    print(f"\nData directory: {base_dir}")

    timeframes = ['1m', '5m', '15m']
    all_results = {}

    for tf in timeframes:
        probs = analyze_timeframe(base_dir, tf)
        if probs:
            all_results[tf] = probs
            print_results(tf, probs)

    # Print summary table
    if all_results:
        print_summary_table(all_results)

    # Run 8:30 AM New York opening candle analysis
    run_830_analysis(base_dir)

    # Run 8:30 AM consecutive candle continuation analysis
    run_830_consecutive_analysis(base_dir)

    print("\nAnalysis complete!")


if __name__ == "__main__":
    main()

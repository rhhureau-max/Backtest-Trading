#!/usr/bin/env python3
"""
Liquidity Sweep Detector for OHLCV Data

This script identifies "liquidity sweeps" in trading data.
A liquidity sweep occurs when:
1. Price breaks above a swing high (or below a swing low)
2. Price quickly reverses back into the previous range
3. Often accompanied by elevated volume

Usage:
    python liquidity_sweep_detector.py [--year YEAR] [--timeframe TIMEFRAME]
    
Example:
    python liquidity_sweep_detector.py --year 2025 --timeframe 15m
    python liquidity_sweep_detector.py  # Uses 2025 15m by default

Author: Trading Analysis Tool
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import List, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime
import argparse
import os


@dataclass
class SwingPoint:
    """Represents a swing high or swing low point"""
    index: int
    datetime: datetime
    price: float
    is_high: bool  # True for swing high, False for swing low
    
    
@dataclass
class LiquiditySweep:
    """Represents a detected liquidity sweep event"""
    sweep_datetime: datetime
    sweep_index: int
    sweep_type: str  # 'bullish' or 'bearish'
    swing_level: float
    sweep_price: float
    close_price: float
    volume: float
    volume_ratio: float  # Ratio compared to average volume
    reversal_candles: int  # Number of candles until reversal confirmed
    
    def __str__(self):
        return (f"[{self.sweep_datetime}] {self.sweep_type.upper()} sweep | "
                f"Level: {self.swing_level:.2f} | Swept to: {self.sweep_price:.2f} | "
                f"Close: {self.close_price:.2f} | Vol ratio: {self.volume_ratio:.2f}x")


class LiquiditySweepDetector:
    """
    Detects liquidity sweeps in OHLCV data.
    
    Parameters:
    -----------
    swing_lookback : int
        Number of candles to look back/forward to identify swing points
    sweep_threshold_pct : float
        Minimum percentage price must exceed swing level to count as sweep
    reversal_lookback : int
        Number of candles to check for price reversal after sweep
    volume_multiplier : float
        Minimum volume ratio (vs average) to confirm sweep with volume
    """
    
    def __init__(
        self,
        swing_lookback: int = 5,
        sweep_threshold_pct: float = 0.05,
        reversal_lookback: int = 3,
        volume_multiplier: float = 1.5,
        volume_avg_period: int = 20
    ):
        self.swing_lookback = swing_lookback
        self.sweep_threshold_pct = sweep_threshold_pct / 100
        self.reversal_lookback = reversal_lookback
        self.volume_multiplier = volume_multiplier
        self.volume_avg_period = volume_avg_period
        
    def load_data(self, filepath: str) -> pd.DataFrame:
        """
        Load CSV data with semicolon separator and proper column names.
        
        The CSV format is:
        Column1: Date (DD/MM/YYYY)
        Column2: Time (HH:MM:SS)
        Column3: Open
        Column4: High
        Column5: Low
        Column6: Close
        Column7: Volume
        """
        df = pd.read_csv(
            filepath, 
            sep=';',
            names=['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume'],
            skiprows=1  # Skip header row
        )
        
        # Combine date and time into datetime with error handling
        df['Datetime'] = pd.to_datetime(
            df['Date'] + ' ' + df['Time'], 
            format='%d/%m/%Y %H:%M:%S',
            errors='coerce'  # Convert invalid dates to NaT
        )
        
        # Convert numeric columns
        for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Set datetime as index
        df = df.set_index('Datetime')
        df = df.drop(['Date', 'Time'], axis=1)
        
        # Remove any rows with missing data
        df = df.dropna()
        
        return df
    
    def find_swing_highs(self, df: pd.DataFrame) -> List[SwingPoint]:
        """
        Identify swing highs in the data.
        A swing high is a point where High is higher than the N bars before and after.
        
        Note: Python/NumPy slicing is bounds-safe, returning empty arrays if indices
        exceed array length, so no explicit bounds checking is needed.
        """
        swing_highs = []
        highs = df['High'].values
        
        # Ensure we have enough data on both sides for swing detection
        for i in range(self.swing_lookback, len(highs) - self.swing_lookback):
            # Check if current high is the highest in the window
            window_before = highs[i - self.swing_lookback:i]
            window_after = highs[i + 1:i + self.swing_lookback + 1]
            
            # Skip if windows are empty (defensive check)
            if len(window_before) == 0 or len(window_after) == 0:
                continue
            
            if highs[i] > max(window_before) and highs[i] > max(window_after):
                swing_highs.append(SwingPoint(
                    index=i,
                    datetime=df.index[i],
                    price=highs[i],
                    is_high=True
                ))
        
        return swing_highs
    
    def find_swing_lows(self, df: pd.DataFrame) -> List[SwingPoint]:
        """
        Identify swing lows in the data.
        A swing low is a point where Low is lower than the N bars before and after.
        
        Note: Python/NumPy slicing is bounds-safe, returning empty arrays if indices
        exceed array length, so no explicit bounds checking is needed.
        """
        swing_lows = []
        lows = df['Low'].values
        
        # Ensure we have enough data on both sides for swing detection
        for i in range(self.swing_lookback, len(lows) - self.swing_lookback):
            # Check if current low is the lowest in the window
            window_before = lows[i - self.swing_lookback:i]
            window_after = lows[i + 1:i + self.swing_lookback + 1]
            
            # Skip if windows are empty (defensive check)
            if len(window_before) == 0 or len(window_after) == 0:
                continue
            
            if lows[i] < min(window_before) and lows[i] < min(window_after):
                swing_lows.append(SwingPoint(
                    index=i,
                    datetime=df.index[i],
                    price=lows[i],
                    is_high=False
                ))
        
        return swing_lows
    
    def calculate_volume_ratio(self, df: pd.DataFrame, index: int) -> float:
        """Calculate volume ratio compared to recent average.
        
        Uses the volume of bars before the current index to calculate average.
        Returns 1.0 if no historical data is available.
        """
        start_idx = max(0, index - self.volume_avg_period)
        # Ensure we have at least one bar of history
        if start_idx >= index:
            return 1.0
        avg_volume = df['Volume'].iloc[start_idx:index].mean()
        if pd.isna(avg_volume) or avg_volume <= 0:
            return 1.0
        return df['Volume'].iloc[index] / avg_volume
    
    def detect_bearish_sweep(
        self, 
        df: pd.DataFrame, 
        swing_high: SwingPoint
    ) -> Optional[LiquiditySweep]:
        """
        Detect a bearish liquidity sweep above a swing high.
        
        A bearish sweep occurs when:
        1. Price breaks above the swing high (wick above)
        2. Price closes below the swing high
        3. Price continues lower or reverses quickly
        """
        highs = df['High'].values
        closes = df['Close'].values
        lows = df['Low'].values
        volumes = df['Volume'].values
        
        # Look for sweeps after the swing high was formed
        search_start = swing_high.index + self.swing_lookback
        
        for i in range(search_start, len(highs)):
            # Check if price swept above the swing high
            sweep_amount = highs[i] - swing_high.price
            sweep_pct = sweep_amount / swing_high.price
            
            if sweep_pct > self.sweep_threshold_pct:
                # Price broke above swing high - check for reversal
                if closes[i] < swing_high.price:
                    # Closed back below swing high = potential sweep
                    volume_ratio = self.calculate_volume_ratio(df, i)
                    
                    # Check for continuation lower in next few candles
                    reversal_confirmed = False
                    reversal_candles = 0
                    
                    for j in range(1, min(self.reversal_lookback + 1, len(highs) - i)):
                        if closes[i + j] < swing_high.price:
                            reversal_confirmed = True
                            reversal_candles = j
                            break
                    
                    if reversal_confirmed or volume_ratio >= self.volume_multiplier:
                        return LiquiditySweep(
                            sweep_datetime=df.index[i],
                            sweep_index=i,
                            sweep_type='bearish',
                            swing_level=swing_high.price,
                            sweep_price=highs[i],
                            close_price=closes[i],
                            volume=volumes[i],
                            volume_ratio=volume_ratio,
                            reversal_candles=reversal_candles
                        )
        
        return None
    
    def detect_bullish_sweep(
        self, 
        df: pd.DataFrame, 
        swing_low: SwingPoint
    ) -> Optional[LiquiditySweep]:
        """
        Detect a bullish liquidity sweep below a swing low.
        
        A bullish sweep occurs when:
        1. Price breaks below the swing low (wick below)
        2. Price closes above the swing low
        3. Price continues higher or reverses quickly
        """
        highs = df['High'].values
        closes = df['Close'].values
        lows = df['Low'].values
        volumes = df['Volume'].values
        
        # Look for sweeps after the swing low was formed
        search_start = swing_low.index + self.swing_lookback
        
        for i in range(search_start, len(lows)):
            # Check if price swept below the swing low
            sweep_amount = swing_low.price - lows[i]
            sweep_pct = sweep_amount / swing_low.price
            
            if sweep_pct > self.sweep_threshold_pct:
                # Price broke below swing low - check for reversal
                if closes[i] > swing_low.price:
                    # Closed back above swing low = potential sweep
                    volume_ratio = self.calculate_volume_ratio(df, i)
                    
                    # Check for continuation higher in next few candles
                    reversal_confirmed = False
                    reversal_candles = 0
                    
                    for j in range(1, min(self.reversal_lookback + 1, len(lows) - i)):
                        if closes[i + j] > swing_low.price:
                            reversal_confirmed = True
                            reversal_candles = j
                            break
                    
                    if reversal_confirmed or volume_ratio >= self.volume_multiplier:
                        return LiquiditySweep(
                            sweep_datetime=df.index[i],
                            sweep_index=i,
                            sweep_type='bullish',
                            swing_level=swing_low.price,
                            sweep_price=lows[i],
                            close_price=closes[i],
                            volume=volumes[i],
                            volume_ratio=volume_ratio,
                            reversal_candles=reversal_candles
                        )
        
        return None
    
    def detect_all_sweeps(self, df: pd.DataFrame) -> List[LiquiditySweep]:
        """
        Detect all liquidity sweeps in the dataframe.
        
        Returns a list of LiquiditySweep objects sorted by datetime.
        """
        print(f"Analyzing {len(df)} candles...")
        
        # Find swing points
        swing_highs = self.find_swing_highs(df)
        swing_lows = self.find_swing_lows(df)
        
        print(f"Found {len(swing_highs)} swing highs and {len(swing_lows)} swing lows")
        
        sweeps = []
        
        # Detect bearish sweeps (sweeps of highs)
        print("Detecting bearish sweeps (above swing highs)...")
        for swing_high in swing_highs:
            sweep = self.detect_bearish_sweep(df, swing_high)
            if sweep:
                sweeps.append(sweep)
        
        # Detect bullish sweeps (sweeps of lows)
        print("Detecting bullish sweeps (below swing lows)...")
        for swing_low in swing_lows:
            sweep = self.detect_bullish_sweep(df, swing_low)
            if sweep:
                sweeps.append(sweep)
        
        # Sort by datetime
        sweeps.sort(key=lambda x: x.sweep_datetime)
        
        return sweeps
    
    def analyze_file(self, filepath: str) -> Tuple[pd.DataFrame, List[LiquiditySweep]]:
        """
        Load a file and detect all liquidity sweeps.
        
        Returns the dataframe and list of detected sweeps.
        """
        print(f"\n{'='*60}")
        print(f"Loading: {filepath}")
        print('='*60)
        
        df = self.load_data(filepath)
        print(f"Data range: {df.index.min()} to {df.index.max()}")
        
        sweeps = self.detect_all_sweeps(df)
        
        return df, sweeps


def get_available_files(base_path: str) -> dict:
    """Get all available CSV files organized by year and timeframe.
    
    Dynamically discovers available files by scanning the directory
    rather than using a hard-coded year range.
    """
    files = {}
    timeframes = ['1m', '5m', '15m', '1H', '4H', '1D']
    
    for tf in timeframes:
        files[tf] = []
    
    # Scan directory for matching files
    try:
        for filename in os.listdir(base_path):
            if filename.endswith('.csv'):
                # Parse filename format: "YEAR TIMEFRAME.csv"
                parts = filename.replace('.csv', '').split(' ')
                if len(parts) == 2:
                    try:
                        year = int(parts[0])
                        tf = parts[1]
                        if tf in timeframes:
                            filepath = os.path.join(base_path, filename)
                            files[tf].append((year, filepath))
                    except ValueError:
                        continue  # Skip files that don't match the expected format
    except OSError:
        pass  # Return empty dict if directory can't be read
    
    # Sort files by year for each timeframe
    for tf in timeframes:
        files[tf].sort(key=lambda x: x[0])
    
    return files


def print_sweep_summary(sweeps: List[LiquiditySweep], timeframe: str):
    """Print a summary of detected sweeps"""
    if not sweeps:
        print("\nNo liquidity sweeps detected with current parameters.")
        return
    
    print(f"\n{'='*60}")
    print(f"LIQUIDITY SWEEP SUMMARY - {timeframe}")
    print('='*60)
    
    bullish = [s for s in sweeps if s.sweep_type == 'bullish']
    bearish = [s for s in sweeps if s.sweep_type == 'bearish']
    
    print(f"\nTotal sweeps detected: {len(sweeps)}")
    print(f"  - Bullish sweeps (below swing lows): {len(bullish)}")
    print(f"  - Bearish sweeps (above swing highs): {len(bearish)}")
    
    # High volume sweeps
    high_vol_sweeps = [s for s in sweeps if s.volume_ratio >= 1.5]
    print(f"\nHigh volume sweeps (>1.5x avg): {len(high_vol_sweeps)}")
    
    # Print recent sweeps
    print(f"\n--- Last 10 Sweeps ---")
    for sweep in sweeps[-10:]:
        print(sweep)


def print_methodology():
    """Print the methodology explanation"""
    print("""
================================================================================
                        LIQUIDITY SWEEP DETECTION METHODOLOGY
================================================================================

WHAT IS A LIQUIDITY SWEEP?
--------------------------
A liquidity sweep (also called a "stop hunt" or "liquidity grab") is a price 
movement pattern where:

1. Price breaks beyond a key support/resistance level (swing high/low)
2. This triggers stop-loss orders and limit orders resting at that level
3. Price quickly reverses back into the previous range
4. Often accompanied by elevated trading volume

WHY DO LIQUIDITY SWEEPS OCCUR?
------------------------------
- Large players (institutions, market makers) need liquidity to fill orders
- Stop-loss orders and limit orders cluster around obvious swing points
- By pushing price through these levels, institutions access this liquidity
- The quick reversal happens once orders are filled

DETECTION ALGORITHM:
--------------------
1. IDENTIFY SWING POINTS
   - Swing High: A bar where High > High of N bars before AND after
   - Swing Low: A bar where Low < Low of N bars before AND after
   - Default lookback: 5 bars

2. DETECT SWEEP CONDITIONS
   For Bearish Sweep (above swing high):
   - Price's High exceeds the swing high by a threshold (0.05%)
   - Price closes BELOW the swing high (rejection)
   - Price continues lower in subsequent bars OR has high volume

   For Bullish Sweep (below swing low):
   - Price's Low exceeds below the swing low by a threshold (0.05%)
   - Price closes ABOVE the swing low (rejection)
   - Price continues higher in subsequent bars OR has high volume

3. VOLUME CONFIRMATION
   - Calculate average volume over last 20 bars
   - If current volume > 1.5x average, sweep is more significant
   - High volume confirms institutional activity

TIMEFRAME CONSIDERATIONS:
-------------------------
- 1m/5m: Very short-term sweeps, more noise, useful for scalping
- 15m/1H: Intraday sweeps, good for day trading
- 4H/1D: Swing trading levels, more significant moves

PARAMETERS (adjustable):
------------------------
- swing_lookback: Bars to look back/forward for swing identification (default: 5)
- sweep_threshold_pct: Min % price must exceed swing level (default: 0.05%)
- reversal_lookback: Bars to check for reversal after sweep (default: 3)
- volume_multiplier: Min volume ratio to confirm sweep (default: 1.5x)

================================================================================
""")


def main():
    """Main function to run the liquidity sweep detector"""
    parser = argparse.ArgumentParser(
        description='Detect liquidity sweeps in OHLCV trading data'
    )
    parser.add_argument(
        '--year', 
        type=int, 
        default=2025,
        help='Year of data to analyze (default: 2025)'
    )
    parser.add_argument(
        '--timeframe', 
        type=str, 
        default='15m',
        choices=['1m', '5m', '15m', '1H', '4H', '1D'],
        help='Timeframe to analyze (default: 15m)'
    )
    parser.add_argument(
        '--swing-lookback',
        type=int,
        default=5,
        help='Bars to look back/forward for swing points (default: 5)'
    )
    parser.add_argument(
        '--sweep-threshold',
        type=float,
        default=0.05,
        help='Min percentage to exceed swing level (default: 0.05)'
    )
    parser.add_argument(
        '--reversal-lookback',
        type=int,
        default=3,
        help='Bars to check for reversal (default: 3)'
    )
    parser.add_argument(
        '--volume-multiplier',
        type=float,
        default=1.5,
        help='Min volume ratio to confirm sweep (default: 1.5)'
    )
    parser.add_argument(
        '--methodology',
        action='store_true',
        help='Print methodology explanation and exit'
    )
    parser.add_argument(
        '--all-timeframes',
        action='store_true',
        help='Analyze all available timeframes for the given year'
    )
    
    args = parser.parse_args()
    
    if args.methodology:
        print_methodology()
        return
    
    # Get the base path (script directory or repository root)
    base_path = Path(__file__).parent
    
    # Initialize detector with parameters
    detector = LiquiditySweepDetector(
        swing_lookback=args.swing_lookback,
        sweep_threshold_pct=args.sweep_threshold,
        reversal_lookback=args.reversal_lookback,
        volume_multiplier=args.volume_multiplier
    )
    
    print_methodology()
    
    # Define available timeframes (1m excluded by default for performance)
    all_timeframes = ['1m', '5m', '15m', '1H', '4H', '1D']
    default_batch_timeframes = ['5m', '15m', '1H', '4H', '1D']  # Skip 1m for performance
    
    if args.all_timeframes:
        # Analyze all timeframes for the given year (excluding 1m for performance)
        for tf in default_batch_timeframes:
            filename = f"{args.year} {tf}.csv"
            filepath = base_path / filename
            
            if filepath.exists():
                try:
                    df, sweeps = detector.analyze_file(str(filepath))
                    print_sweep_summary(sweeps, tf)
                except Exception as e:
                    print(f"Error analyzing {filename}: {e}")
            else:
                print(f"\nFile not found: {filename}")
    else:
        # Analyze single timeframe
        filename = f"{args.year} {args.timeframe}.csv"
        filepath = base_path / filename
        
        if not filepath.exists():
            print(f"Error: File not found: {filepath}")
            print("\nAvailable files:")
            available = get_available_files(str(base_path))
            for tf, files in available.items():
                if files:
                    years = [str(y) for y, _ in files]
                    print(f"  {tf}: {', '.join(years)}")
            return
        
        df, sweeps = detector.analyze_file(str(filepath))
        print_sweep_summary(sweeps, args.timeframe)
        
        # Show some sample data around the first few sweeps
        if sweeps:
            print(f"\n{'='*60}")
            print("SAMPLE SWEEP DETAILS")
            print('='*60)
            
            for sweep in sweeps[:3]:  # Show first 3 sweeps
                print(f"\n{sweep.sweep_type.upper()} SWEEP at {sweep.sweep_datetime}")
                print("-" * 40)
                
                # Get candles around the sweep (safe bounds)
                start_idx = max(0, sweep.sweep_index - 5)
                end_idx = min(len(df), sweep.sweep_index + 5)
                
                # Only display if we have valid indices
                if start_idx < end_idx and end_idx <= len(df):
                    print(df.iloc[start_idx:end_idx].to_string())
                print()


if __name__ == "__main__":
    main()

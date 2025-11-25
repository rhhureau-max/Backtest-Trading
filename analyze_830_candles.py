#!/usr/bin/env python3
"""
Trading Backtest Script - Analyze 8:30 AM Paris Candle Continuation

This script analyzes the first candle at the European session opening (8:30 AM Paris time)
and calculates the probability of subsequent candles continuing in the same direction.

For bullish 8:30 candles: Calculates probability that subsequent candles are also bullish
For bearish 8:30 candles: Calculates probability that subsequent candles are also bearish

Minimum body size requirements:
- 1-minute timeframe: 30 points
- 5-minute timeframe: 75 points  
- 15-minute timeframe: 100 points
"""

import os
from typing import Dict, List


# Configuration
# DATA_DIR can be overridden by setting the BACKTEST_DATA_DIR environment variable
DATA_DIR = os.environ.get("BACKTEST_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))
TARGET_TIME = "08:30:00"  # 8:30 AM Paris time (European session opening)

# Consecutive candles range for analysis
MIN_CONSECUTIVE = 2
MAX_CONSECUTIVE = 10

# Minimum body size in points for each timeframe
MIN_BODY_SIZE = {
    "1m": 30,
    "5m": 75,
    "15m": 100
}

# Available files for each timeframe
AVAILABLE_FILES = {
    "1m": ["2025 1m.csv"],  # Only 2025 is CSV for 1-minute
    "5m": [f"{year} 5m.csv" for year in range(2018, 2026)],
    "15m": [f"{year} 15m.csv" for year in range(2018, 2026)]
}


def load_csv_data(filepath: str) -> List[Dict]:
    """
    Load CSV data from a semicolon-separated file.
    
    Returns a list of dictionaries with keys: date, time, open, high, low, close, volume
    """
    data = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        # Skip header line
        for line in lines[1:]:
            line = line.strip()
            if not line:
                continue
                
            parts = line.split(';')
            if len(parts) >= 7:
                try:
                    data.append({
                        'date': parts[0],
                        'time': parts[1],
                        'open': float(parts[2]),
                        'high': float(parts[3]),
                        'low': float(parts[4]),
                        'close': float(parts[5]),
                        'volume': int(parts[6])
                    })
                except ValueError:
                    # Skip lines with invalid data
                    continue
    except FileNotFoundError:
        print(f"Warning: File not found: {filepath}")
    except Exception as e:
        print(f"Warning: Error reading {filepath}: {e}")
    
    return data


def is_bullish(candle: Dict) -> bool:
    """Check if a candle is bullish (close > open)."""
    return candle['close'] > candle['open']


def is_bearish(candle: Dict) -> bool:
    """Check if a candle is bearish (close < open)."""
    return candle['close'] < candle['open']


def get_body_size(candle: Dict) -> float:
    """Calculate the body size (absolute difference between open and close)."""
    return abs(candle['close'] - candle['open'])


def analyze_timeframe(timeframe: str) -> Dict:
    """
    Analyze a specific timeframe for 8:30 candle continuation patterns.
    
    Returns a dictionary with statistics for bullish and bearish 8:30 candles.
    """
    print(f"\n{'='*60}")
    print(f"Analyzing {timeframe} timeframe...")
    print(f"{'='*60}")
    
    min_body = MIN_BODY_SIZE[timeframe]
    files = AVAILABLE_FILES[timeframe]
    
    # Load all data
    all_data = []
    for filename in files:
        filepath = os.path.join(DATA_DIR, filename)
        if os.path.exists(filepath):
            data = load_csv_data(filepath)
            all_data.extend(data)
            print(f"  Loaded {len(data):,} candles from {filename}")
    
    if not all_data:
        print(f"  No data found for {timeframe}")
        return {}
    
    print(f"  Total candles loaded: {len(all_data):,}")
    
    # Group data by date
    data_by_date: Dict[str, List[Dict]] = {}
    for candle in all_data:
        date = candle['date']
        if date not in data_by_date:
            data_by_date[date] = []
        data_by_date[date].append(candle)
    
    # Sort candles within each date by time
    for date in data_by_date:
        data_by_date[date].sort(key=lambda x: x['time'])
    
    # Find 8:30 candles and count consecutive same-direction candles
    # Note: The count includes the 8:30 candle itself plus subsequent candles
    # So "2 consecutive" means the 8:30 candle + 1 following candle in the same direction
    bullish_830_stats = {i: 0 for i in range(MIN_CONSECUTIVE, MAX_CONSECUTIVE + 1)}
    bearish_830_stats = {i: 0 for i in range(MIN_CONSECUTIVE, MAX_CONSECUTIVE + 1)}
    
    total_bullish_830 = 0
    total_bearish_830 = 0
    
    for date, candles in sorted(data_by_date.items()):
        # Find the 8:30 candle
        candle_830 = None
        candle_830_idx = -1
        
        for idx, candle in enumerate(candles):
            if candle['time'] == TARGET_TIME:
                candle_830 = candle
                candle_830_idx = idx
                break
        
        if candle_830 is None:
            continue
        
        # Check body size
        body_size = get_body_size(candle_830)
        if body_size < min_body:
            continue
        
        # Determine direction and count consecutive candles
        if is_bullish(candle_830):
            total_bullish_830 += 1
            
            # Count consecutive bullish candles after 8:30
            consecutive_bullish = 1  # Start with the 8:30 candle itself
            for i in range(candle_830_idx + 1, len(candles)):
                if is_bullish(candles[i]):
                    consecutive_bullish += 1
                else:
                    break
            
            # Update stats for each threshold
            for threshold in range(MIN_CONSECUTIVE, MAX_CONSECUTIVE + 1):
                if consecutive_bullish >= threshold:
                    bullish_830_stats[threshold] += 1
        
        elif is_bearish(candle_830):
            total_bearish_830 += 1
            
            # Count consecutive bearish candles after 8:30 (including the 8:30 candle)
            consecutive_bearish = 1  # Start with the 8:30 candle itself
            for i in range(candle_830_idx + 1, len(candles)):
                if is_bearish(candles[i]):
                    consecutive_bearish += 1
                else:
                    break
            
            # Update stats for each threshold
            for threshold in range(MIN_CONSECUTIVE, MAX_CONSECUTIVE + 1):
                if consecutive_bearish >= threshold:
                    bearish_830_stats[threshold] += 1
    
    return {
        'timeframe': timeframe,
        'min_body': min_body,
        'total_bullish_830': total_bullish_830,
        'total_bearish_830': total_bearish_830,
        'bullish_stats': bullish_830_stats,
        'bearish_stats': bearish_830_stats
    }


def print_results(results: Dict) -> None:
    """Print formatted results for a timeframe analysis."""
    if not results:
        return
    
    timeframe = results['timeframe']
    min_body = results['min_body']
    total_bullish = results['total_bullish_830']
    total_bearish = results['total_bearish_830']
    bullish_stats = results['bullish_stats']
    bearish_stats = results['bearish_stats']
    
    print(f"\n{'='*70}")
    print(f"RESULTS FOR {timeframe.upper()} TIMEFRAME")
    print(f"{'='*70}")
    print(f"Minimum body size: {min_body} points")
    print(f"Target time: {TARGET_TIME} (8:30 AM Paris / European session opening)")
    print()
    
    # Bullish results
    print(f"\n{'─'*70}")
    print(f"BULLISH 8:30 CANDLE ANALYSIS")
    print(f"{'─'*70}")
    print(f"Total bullish 8:30 candles with body >= {min_body} points: {total_bullish}")
    print()
    
    if total_bullish > 0:
        print(f"{'Consecutive':^15} {'Count':^15} {'Percentage':^15}")
        print(f"{'Bullish Candles':^15} {'':^15} {'':^15}")
        print(f"{'─'*45}")
        
        for n in range(MIN_CONSECUTIVE, MAX_CONSECUTIVE + 1):
            count = bullish_stats[n]
            pct = (count / total_bullish) * 100 if total_bullish > 0 else 0
            print(f"{n:^15} {count:^15} {pct:^14.2f}%")
    else:
        print("No qualifying bullish 8:30 candles found.")
    
    # Bearish results
    print(f"\n{'─'*70}")
    print(f"BEARISH 8:30 CANDLE ANALYSIS")
    print(f"{'─'*70}")
    print(f"Total bearish 8:30 candles with body >= {min_body} points: {total_bearish}")
    print()
    
    if total_bearish > 0:
        print(f"{'Consecutive':^15} {'Count':^15} {'Percentage':^15}")
        print(f"{'Bearish Candles':^15} {'':^15} {'':^15}")
        print(f"{'─'*45}")
        
        for n in range(MIN_CONSECUTIVE, MAX_CONSECUTIVE + 1):
            count = bearish_stats[n]
            pct = (count / total_bearish) * 100 if total_bearish > 0 else 0
            print(f"{n:^15} {count:^15} {pct:^14.2f}%")
    else:
        print("No qualifying bearish 8:30 candles found.")


def print_summary(all_results: List[Dict]) -> None:
    """Print a combined summary table for all timeframes."""
    print("\n")
    print("=" * 90)
    print("COMBINED SUMMARY - ALL TIMEFRAMES")
    print("=" * 90)
    print()
    
    # Bullish Summary
    print("BULLISH 8:30 CANDLE - CONSECUTIVE BULLISH PROBABILITY")
    print("-" * 90)
    
    header = f"{'Timeframe':^12} | {'Total':^8} |"
    for n in range(MIN_CONSECUTIVE, MAX_CONSECUTIVE + 1):
        header += f" {n} candles |"
    print(header)
    print("-" * 90)
    
    for results in all_results:
        if not results:
            continue
        tf = results['timeframe']
        total = results['total_bullish_830']
        row = f"{tf:^12} | {total:^8} |"
        for n in range(MIN_CONSECUTIVE, MAX_CONSECUTIVE + 1):
            count = results['bullish_stats'][n]
            pct = (count / total * 100) if total > 0 else 0
            row += f" {pct:>5.1f}%    |"
        print(row)
    
    print()
    
    # Bearish Summary
    print("BEARISH 8:30 CANDLE - CONSECUTIVE BEARISH PROBABILITY")
    print("-" * 90)
    
    header = f"{'Timeframe':^12} | {'Total':^8} |"
    for n in range(MIN_CONSECUTIVE, MAX_CONSECUTIVE + 1):
        header += f" {n} candles |"
    print(header)
    print("-" * 90)
    
    for results in all_results:
        if not results:
            continue
        tf = results['timeframe']
        total = results['total_bearish_830']
        row = f"{tf:^12} | {total:^8} |"
        for n in range(MIN_CONSECUTIVE, MAX_CONSECUTIVE + 1):
            count = results['bearish_stats'][n]
            pct = (count / total * 100) if total > 0 else 0
            row += f" {pct:>5.1f}%    |"
        print(row)
    
    print()
    print("=" * 90)


def main():
    """Main function to run the backtest analysis."""
    print("\n" + "=" * 70)
    print("TRADING BACKTEST - 8:30 AM PARIS CANDLE ANALYSIS")
    print("=" * 70)
    print()
    print("This script analyzes the 8:30 AM Paris (European session opening) candle")
    print("and calculates the probability of consecutive candles in the same direction.")
    print()
    print("Minimum body requirements:")
    for tf, min_body in MIN_BODY_SIZE.items():
        print(f"  - {tf}: {min_body} points")
    print()
    
    all_results = []
    
    # Analyze each timeframe
    for timeframe in ["1m", "5m", "15m"]:
        results = analyze_timeframe(timeframe)
        if results:
            all_results.append(results)
            print_results(results)
    
    # Print combined summary
    if all_results:
        print_summary(all_results)
    
    print("\nAnalysis complete!")


if __name__ == "__main__":
    main()

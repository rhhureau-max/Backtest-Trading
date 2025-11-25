#!/usr/bin/env python3
"""
Trading Backtest Script - Analyze 8:30 AM Paris Candle Continuation

This script analyzes the first candle at the European session opening (8:30 AM Paris time)
and calculates the probability of subsequent candles continuing in the same direction.

For bullish 8:30 candles: Calculates probability that subsequent candles are also bullish
For bearish 8:30 candles: Calculates probability that subsequent candles are also bearish

Also calculates the average body size of subsequent candles (from 2 to 5 candles).

Multiple threshold configurations are analyzed:
- Config 1: 1m: 20+ pts, 5m: 40+ pts, 15m: 80+ pts
- Config 2: 1m: 40+ pts, 5m: 100+ pts, 15m: 150+ pts
"""

import os
from typing import Dict, List


# Configuration
# DATA_DIR can be overridden by setting the BACKTEST_DATA_DIR environment variable
DATA_DIR = os.environ.get("BACKTEST_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))
TARGET_TIME = "08:30:00"  # 8:30 AM Paris time (European session opening)

# Consecutive candles range for analysis (2-5 as requested)
MIN_CONSECUTIVE = 2
MAX_CONSECUTIVE = 5

# Range for average body size calculation
AVG_BODY_MIN = 2
AVG_BODY_MAX = 5

# Multiple threshold configurations to analyze
THRESHOLD_CONFIGS = [
    {
        "name": "Config 1 (20/40/80 pts)",
        "thresholds": {"1m": 20, "5m": 40, "15m": 80}
    },
    {
        "name": "Config 2 (40/100/150 pts)",
        "thresholds": {"1m": 40, "5m": 100, "15m": 150}
    }
]

# Available files for each timeframe
# Note: 1-minute data for years prior to 2025 is stored in .zip or .xlsx format,
# only 2025 has an uncompressed .csv file available
AVAILABLE_FILES = {
    "1m": ["2025 1m.csv"],  # Only 2025 is available as CSV
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


def analyze_timeframe(timeframe: str, min_body: int) -> Dict:
    """
    Analyze a specific timeframe for 8:30 candle continuation patterns.
    
    Args:
        timeframe: The timeframe to analyze (1m, 5m, 15m)
        min_body: Minimum body size in points for the 8:30 candle
    
    Returns a dictionary with statistics for bullish and bearish 8:30 candles,
    including average body sizes of subsequent candles.
    """
    print(f"\n{'='*60}")
    print(f"Analyzing {timeframe} timeframe (min body: {min_body} pts)...")
    print(f"{'='*60}")
    
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
    # consecutive_count includes the 8:30 candle itself, so a count of 2 means
    # the 8:30 candle plus 1 subsequent candle in the same direction
    bullish_830_stats = {i: 0 for i in range(MIN_CONSECUTIVE, MAX_CONSECUTIVE + 1)}
    bearish_830_stats = {i: 0 for i in range(MIN_CONSECUTIVE, MAX_CONSECUTIVE + 1)}
    
    # Track body sizes of subsequent candles for average calculation
    # Key: number of candles (2-5), Value: list of body sizes
    bullish_body_sizes = {i: [] for i in range(AVG_BODY_MIN, AVG_BODY_MAX + 1)}
    bearish_body_sizes = {i: [] for i in range(AVG_BODY_MIN, AVG_BODY_MAX + 1)}
    
    # Track same-direction candles at each position (2nd, 3rd, 4th, 5th candle)
    # Key: position (2-5), Value: count of candles in same direction as 8:30
    bullish_same_direction = {i: 0 for i in range(AVG_BODY_MIN, AVG_BODY_MAX + 1)}
    bearish_same_direction = {i: 0 for i in range(AVG_BODY_MIN, AVG_BODY_MAX + 1)}
    # Track total available candles at each position
    bullish_position_total = {i: 0 for i in range(AVG_BODY_MIN, AVG_BODY_MAX + 1)}
    bearish_position_total = {i: 0 for i in range(AVG_BODY_MIN, AVG_BODY_MAX + 1)}
    
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
            
            # Collect body sizes of subsequent candles (for n candles after 8:30)
            for n in range(AVG_BODY_MIN, AVG_BODY_MAX + 1):
                # n represents total candles including 8:30, so we need n-1 subsequent candles
                subsequent_count = n - 1
                if candle_830_idx + subsequent_count < len(candles):
                    # Calculate average body size of the n-1 subsequent candles
                    total_body = sum(get_body_size(candles[candle_830_idx + j]) 
                                   for j in range(1, subsequent_count + 1))
                    avg_body = total_body / subsequent_count
                    bullish_body_sizes[n].append(avg_body)
            
            # Track same-direction candles at each position
            for pos in range(AVG_BODY_MIN, AVG_BODY_MAX + 1):
                candle_idx = candle_830_idx + (pos - 1)  # pos=2 means 1st candle after 8:30
                if candle_idx < len(candles):
                    bullish_position_total[pos] += 1
                    if is_bullish(candles[candle_idx]):
                        bullish_same_direction[pos] += 1
        
        elif is_bearish(candle_830):
            total_bearish_830 += 1
            
            # Count consecutive bearish candles starting from 8:30 (including the 8:30 candle)
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
            
            # Collect body sizes of subsequent candles (for n candles after 8:30)
            for n in range(AVG_BODY_MIN, AVG_BODY_MAX + 1):
                # n represents total candles including 8:30, so we need n-1 subsequent candles
                subsequent_count = n - 1
                if candle_830_idx + subsequent_count < len(candles):
                    # Calculate average body size of the n-1 subsequent candles
                    total_body = sum(get_body_size(candles[candle_830_idx + j]) 
                                   for j in range(1, subsequent_count + 1))
                    avg_body = total_body / subsequent_count
                    bearish_body_sizes[n].append(avg_body)
            
            # Track same-direction candles at each position
            for pos in range(AVG_BODY_MIN, AVG_BODY_MAX + 1):
                candle_idx = candle_830_idx + (pos - 1)  # pos=2 means 1st candle after 8:30
                if candle_idx < len(candles):
                    bearish_position_total[pos] += 1
                    if is_bearish(candles[candle_idx]):
                        bearish_same_direction[pos] += 1
    
    # Calculate overall averages for body sizes and count occurrences
    bullish_avg_body = {}
    bearish_avg_body = {}
    bullish_body_count = {}
    bearish_body_count = {}
    for n in range(AVG_BODY_MIN, AVG_BODY_MAX + 1):
        bullish_body_count[n] = len(bullish_body_sizes[n])
        bearish_body_count[n] = len(bearish_body_sizes[n])
        if bullish_body_sizes[n]:
            bullish_avg_body[n] = sum(bullish_body_sizes[n]) / len(bullish_body_sizes[n])
        else:
            bullish_avg_body[n] = 0
        if bearish_body_sizes[n]:
            bearish_avg_body[n] = sum(bearish_body_sizes[n]) / len(bearish_body_sizes[n])
        else:
            bearish_avg_body[n] = 0
    
    return {
        'timeframe': timeframe,
        'min_body': min_body,
        'total_bullish_830': total_bullish_830,
        'total_bearish_830': total_bearish_830,
        'bullish_stats': bullish_830_stats,
        'bearish_stats': bearish_830_stats,
        'bullish_avg_body': bullish_avg_body,
        'bearish_avg_body': bearish_avg_body,
        'bullish_body_count': bullish_body_count,
        'bearish_body_count': bearish_body_count,
        'bullish_same_direction': bullish_same_direction,
        'bearish_same_direction': bearish_same_direction,
        'bullish_position_total': bullish_position_total,
        'bearish_position_total': bearish_position_total
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
    bullish_avg_body = results.get('bullish_avg_body', {})
    bearish_avg_body = results.get('bearish_avg_body', {})
    bullish_body_count = results.get('bullish_body_count', {})
    bearish_body_count = results.get('bearish_body_count', {})
    bullish_same_dir = results.get('bullish_same_direction', {})
    bearish_same_dir = results.get('bearish_same_direction', {})
    
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
        print(f"{'Consecutive':^15} {'Count':^15} {'Probability':^15}")
        print(f"{'Candles':^15} {'':^15} {'(Ratio)':^15}")
        print(f"{'─'*45}")
        
        for n in range(MIN_CONSECUTIVE, MAX_CONSECUTIVE + 1):
            count = bullish_stats[n]
            pct = (count / total_bullish) * 100 if total_bullish > 0 else 0
            print(f"{n:^15} {count:^15} {pct:^14.2f}%")
        
        # Same direction candles at each position
        print(f"\n{'─'*70}")
        print(f"SAME DIRECTION CANDLES (% of total bullish 8:30)")
        print(f"{'─'*70}")
        print(f"{'Position':^15} {'Same Dir Count':^15} {'% of Total':^15}")
        print(f"{'─'*45}")
        for pos in range(AVG_BODY_MIN, AVG_BODY_MAX + 1):
            same_count = bullish_same_dir.get(pos, 0)
            pct = (same_count / total_bullish * 100) if total_bullish > 0 else 0
            print(f"{pos:^15} {same_count:^15} {pct:^14.2f}%")
        
        # Average body size of subsequent candles
        print(f"\n{'─'*70}")
        print(f"AVERAGE BODY SIZE OF SUBSEQUENT CANDLES (after bullish 8:30)")
        print(f"{'─'*70}")
        print(f"{'Nb Candles':^15} {'Count':^10} {'% of Total':^15} {'Avg Body (pts)':^20}")
        print(f"{'─'*60}")
        for n in range(AVG_BODY_MIN, AVG_BODY_MAX + 1):
            avg = bullish_avg_body.get(n, 0)
            count = bullish_body_count.get(n, 0)
            pct = (count / total_bullish * 100) if total_bullish > 0 else 0
            print(f"{n:^15} {count:^10} {pct:^14.2f}% {avg:^20.2f}")
    else:
        print("No qualifying bullish 8:30 candles found.")
    
    # Bearish results
    print(f"\n{'─'*70}")
    print(f"BEARISH 8:30 CANDLE ANALYSIS")
    print(f"{'─'*70}")
    print(f"Total bearish 8:30 candles with body >= {min_body} points: {total_bearish}")
    print()
    
    if total_bearish > 0:
        print(f"{'Consecutive':^15} {'Count':^15} {'Probability':^15}")
        print(f"{'Candles':^15} {'':^15} {'(Ratio)':^15}")
        print(f"{'─'*45}")
        
        for n in range(MIN_CONSECUTIVE, MAX_CONSECUTIVE + 1):
            count = bearish_stats[n]
            pct = (count / total_bearish) * 100 if total_bearish > 0 else 0
            print(f"{n:^15} {count:^15} {pct:^14.2f}%")
        
        # Same direction candles at each position
        print(f"\n{'─'*70}")
        print(f"SAME DIRECTION CANDLES (% of total bearish 8:30)")
        print(f"{'─'*70}")
        print(f"{'Position':^15} {'Same Dir Count':^15} {'% of Total':^15}")
        print(f"{'─'*45}")
        for pos in range(AVG_BODY_MIN, AVG_BODY_MAX + 1):
            same_count = bearish_same_dir.get(pos, 0)
            pct = (same_count / total_bearish * 100) if total_bearish > 0 else 0
            print(f"{pos:^15} {same_count:^15} {pct:^14.2f}%")
        
        # Average body size of subsequent candles
        print(f"\n{'─'*70}")
        print(f"AVERAGE BODY SIZE OF SUBSEQUENT CANDLES (after bearish 8:30)")
        print(f"{'─'*70}")
        print(f"{'Nb Candles':^15} {'Count':^10} {'% of Total':^15} {'Avg Body (pts)':^20}")
        print(f"{'─'*60}")
        for n in range(AVG_BODY_MIN, AVG_BODY_MAX + 1):
            avg = bearish_avg_body.get(n, 0)
            count = bearish_body_count.get(n, 0)
            pct = (count / total_bearish * 100) if total_bearish > 0 else 0
            print(f"{n:^15} {count:^10} {pct:^14.2f}% {avg:^20.2f}")
    else:
        print("No qualifying bearish 8:30 candles found.")


def print_summary(all_results: List[Dict]) -> None:
    """Print a combined summary table for all timeframes."""
    print("\n")
    print("=" * 90)
    print("COMBINED SUMMARY - ALL TIMEFRAMES")
    print("=" * 90)
    print()
    
    # Bullish Summary - Consecutive Probability (Ratio)
    print("BULLISH 8:30 CANDLE - PROBABILITY OF CONSECUTIVE BULLISH CANDLES")
    print("(Ratio of how many candles follow the same direction)")
    print("-" * 90)
    
    header = f"{'Timeframe':^12} | {'Total':^8} |"
    for n in range(MIN_CONSECUTIVE, MAX_CONSECUTIVE + 1):
        header += f" {n} consec  |"
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
            pct = ((count / total) * 100) if total > 0 else 0
            row += f" {pct:>5.1f}%    |"
        print(row)
    
    print()
    
    # Bearish Summary - Consecutive Probability (Ratio)
    print("BEARISH 8:30 CANDLE - PROBABILITY OF CONSECUTIVE BEARISH CANDLES")
    print("(Ratio of how many candles follow the same direction)")
    print("-" * 90)
    
    header = f"{'Timeframe':^12} | {'Total':^8} |"
    for n in range(MIN_CONSECUTIVE, MAX_CONSECUTIVE + 1):
        header += f" {n} consec  |"
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
            pct = ((count / total) * 100) if total > 0 else 0
            row += f" {pct:>5.1f}%    |"
        print(row)
    
    print()
    
    # Same Direction Summary
    print("=" * 80)
    print("SAME DIRECTION CANDLES (% of total first candles)")
    print("=" * 80)
    print()
    
    print("After BULLISH 8:30 candle (% bullish at each position):")
    print("-" * 80)
    header = f"{'Timeframe':^12} | {'Total':^6} |"
    for pos in range(AVG_BODY_MIN, AVG_BODY_MAX + 1):
        header += f"  Pos {pos} (%)  |"
    print(header)
    print("-" * 80)
    
    for results in all_results:
        if not results:
            continue
        tf = results['timeframe']
        total = results['total_bullish_830']
        bullish_same = results.get('bullish_same_direction', {})
        row = f"{tf:^12} | {total:^6} |"
        for pos in range(AVG_BODY_MIN, AVG_BODY_MAX + 1):
            same_count = bullish_same.get(pos, 0)
            pct = (same_count / total * 100) if total > 0 else 0
            row += f"  {pct:>6.1f}%   |"
        print(row)
    
    print()
    
    print("After BEARISH 8:30 candle (% bearish at each position):")
    print("-" * 80)
    header = f"{'Timeframe':^12} | {'Total':^6} |"
    for pos in range(AVG_BODY_MIN, AVG_BODY_MAX + 1):
        header += f"  Pos {pos} (%)  |"
    print(header)
    print("-" * 80)
    
    for results in all_results:
        if not results:
            continue
        tf = results['timeframe']
        total = results['total_bearish_830']
        bearish_same = results.get('bearish_same_direction', {})
        row = f"{tf:^12} | {total:^6} |"
        for pos in range(AVG_BODY_MIN, AVG_BODY_MAX + 1):
            same_count = bearish_same.get(pos, 0)
            pct = (same_count / total * 100) if total > 0 else 0
            row += f"  {pct:>6.1f}%   |"
        print(row)
    
    print()
    
    # Average Body Size Summary for Bullish
    print("=" * 100)
    print("AVERAGE BODY SIZE OF SUBSEQUENT CANDLES (with % of total first candles)")
    print("=" * 100)
    print()
    
    print("After BULLISH 8:30 candle:")
    print("-" * 100)
    header = f"{'Timeframe':^12} | {'Total':^6} |"
    for n in range(AVG_BODY_MIN, AVG_BODY_MAX + 1):
        header += f" {n} candles (avg/%)  |"
    print(header)
    print("-" * 100)
    
    for results in all_results:
        if not results:
            continue
        tf = results['timeframe']
        total = results['total_bullish_830']
        bullish_avg = results.get('bullish_avg_body', {})
        bullish_cnt = results.get('bullish_body_count', {})
        row = f"{tf:^12} | {total:^6} |"
        for n in range(AVG_BODY_MIN, AVG_BODY_MAX + 1):
            avg = bullish_avg.get(n, 0)
            cnt = bullish_cnt.get(n, 0)
            pct = (cnt / total * 100) if total > 0 else 0
            row += f" {avg:>5.1f} / {pct:>5.1f}%  |"
        print(row)
    
    print()
    
    print("After BEARISH 8:30 candle:")
    print("-" * 100)
    header = f"{'Timeframe':^12} | {'Total':^6} |"
    for n in range(AVG_BODY_MIN, AVG_BODY_MAX + 1):
        header += f" {n} candles (avg/%)  |"
    print(header)
    print("-" * 100)
    
    for results in all_results:
        if not results:
            continue
        tf = results['timeframe']
        total = results['total_bearish_830']
        bearish_avg = results.get('bearish_avg_body', {})
        bearish_cnt = results.get('bearish_body_count', {})
        row = f"{tf:^12} | {total:^6} |"
        for n in range(AVG_BODY_MIN, AVG_BODY_MAX + 1):
            avg = bearish_avg.get(n, 0)
            cnt = bearish_cnt.get(n, 0)
            pct = (cnt / total * 100) if total > 0 else 0
            row += f" {avg:>5.1f} / {pct:>5.1f}%  |"
        print(row)
    
    print()
    print("=" * 100)


def main():
    """Main function to run the backtest analysis."""
    print("\n" + "=" * 70)
    print("TRADING BACKTEST - 8:30 AM PARIS CANDLE ANALYSIS")
    print("=" * 70)
    print()
    print("This script analyzes the 8:30 AM Paris (European session opening) candle")
    print("and calculates the probability of consecutive candles in the same direction.")
    print()
    
    # Run analysis for each threshold configuration
    for config in THRESHOLD_CONFIGS:
        config_name = config["name"]
        thresholds = config["thresholds"]
        
        print("\n" + "#" * 80)
        print(f"## {config_name}")
        print("#" * 80)
        print()
        print("Minimum body requirements:")
        for tf, min_body in thresholds.items():
            print(f"  - {tf}: {min_body} points")
        print()
        
        all_results = []
        
        # Analyze each timeframe with the current threshold configuration
        for timeframe in ["1m", "5m", "15m"]:
            min_body = thresholds[timeframe]
            results = analyze_timeframe(timeframe, min_body)
            if results:
                all_results.append(results)
                print_results(results)
        
        # Print combined summary for this configuration
        if all_results:
            print_summary(all_results)
    
    print("\nAnalysis complete!")


if __name__ == "__main__":
    main()

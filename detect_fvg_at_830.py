#!/usr/bin/env python3
"""
Fair Value Gap (FVG) Detection Script

This script analyzes trading data to identify Fair Value Gaps (FVGs) that occur at 8:30:00.

A Fair Value Gap occurs when:
- Bullish FVG: The low of candle[i] > high of candle[i-2]
- Bearish FVG: The high of candle[i] < low of candle[i-2]
"""

import csv
import glob
from datetime import datetime

def detect_fvg(data):
    """
    Detect Fair Value Gaps in the data where the middle candle is at 8:30:00.
    
    Args:
        data: List of candle dictionaries with OHLC data
        
    Returns:
        List of FVG events with details (only those where middle candle is at 8:30:00)
    """
    fvgs = []
    
    # Loop so that the middle candle is at position i
    # Need at least 3 candles (previous, middle, next)
    for i in range(1, len(data) - 1):
        previous = data[i-1]
        middle = data[i]
        next_candle = data[i+1]
        
        # Only detect FVGs where the middle candle is at 8:30:00
        if middle['time'] != '08:30:00':
            continue
        
        # Bullish FVG: gap up (next low > previous high)
        if float(next_candle['low']) > float(previous['high']):
            fvg = {
                'date': middle['date'],
                'time': middle['time'],
                'type': 'Bullish',
                'gap_start': previous['high'],
                'gap_end': next_candle['low'],
                'gap_size': float(next_candle['low']) - float(previous['high']),
                'next_candle': {
                    'open': next_candle['open'],
                    'high': next_candle['high'],
                    'low': next_candle['low'],
                    'close': next_candle['close']
                },
                'middle_candle': {
                    'open': middle['open'],
                    'high': middle['high'],
                    'low': middle['low'],
                    'close': middle['close']
                },
                'previous_candle': {
                    'open': previous['open'],
                    'high': previous['high'],
                    'low': previous['low'],
                    'close': previous['close']
                }
            }
            fvgs.append(fvg)
        
        # Bearish FVG: gap down (next high < previous low)
        elif float(next_candle['high']) < float(previous['low']):
            fvg = {
                'date': middle['date'],
                'time': middle['time'],
                'type': 'Bearish',
                'gap_start': next_candle['high'],
                'gap_end': previous['low'],
                'gap_size': float(previous['low']) - float(next_candle['high']),
                'next_candle': {
                    'open': next_candle['open'],
                    'high': next_candle['high'],
                    'low': next_candle['low'],
                    'close': next_candle['close']
                },
                'middle_candle': {
                    'open': middle['open'],
                    'high': middle['high'],
                    'low': middle['low'],
                    'close': middle['close']
                },
                'previous_candle': {
                    'open': previous['open'],
                    'high': previous['high'],
                    'low': previous['low'],
                    'close': previous['close']
                }
            }
            fvgs.append(fvg)
    
    return fvgs

def load_csv_data(filename):
    """Load OHLC data from CSV file."""
    data = []
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=';')
        header = next(reader)  # Skip header
        
        for row in reader:
            if len(row) >= 7:
                data.append({
                    'date': row[0],
                    'time': row[1],
                    'open': row[2],
                    'high': row[3],
                    'low': row[4],
                    'close': row[5],
                    'volume': row[6]
                })
    
    return data

def main():
    """Main function to find all FVGs at 8:30:00 (as middle candle)."""
    print("=" * 80)
    print("Fair Value Gap (FVG) Detection at 8:30:00 (Middle Candle)")
    print("=" * 80)
    print()
    
    # Find all CSV files (exclude zip files)
    csv_files = sorted([f for f in glob.glob('*.csv') if not f.endswith('.zip')])
    
    all_fvgs_at_830 = []
    
    for filename in csv_files:
        print(f"Processing: {filename}")
        data = load_csv_data(filename)
        
        # Detect all FVGs (already filtered for 8:30:00 as middle candle)
        fvgs_at_830 = detect_fvg(data)
        
        if fvgs_at_830:
            print(f"  Found {len(fvgs_at_830)} FVG(s) at 8:30:00")
            all_fvgs_at_830.extend([(filename, fvg) for fvg in fvgs_at_830])
    
    print()
    print("=" * 80)
    print(f"SUMMARY: Found {len(all_fvgs_at_830)} FVG(s) at 8:30:00 across all files")
    print("=" * 80)
    print()
    
    if all_fvgs_at_830:
        print("Detailed FVG Information at 8:30:00:")
        print("-" * 80)
        
        for i, (filename, fvg) in enumerate(all_fvgs_at_830, 1):
            print(f"\n{i}. {filename}")
            print(f"   Date: {fvg['date']}")
            print(f"   Time: {fvg['time']}")
            print(f"   Type: {fvg['type']} FVG")
            print(f"   Gap Size: {fvg['gap_size']:.6f}")
            print(f"   Gap Range: {fvg['gap_start']} to {fvg['gap_end']}")
            print()
            print(f"   Previous Candle (8:15): O={fvg['previous_candle']['open']} H={fvg['previous_candle']['high']} L={fvg['previous_candle']['low']} C={fvg['previous_candle']['close']}")
            print(f"   Middle Candle   (8:30): O={fvg['middle_candle']['open']} H={fvg['middle_candle']['high']} L={fvg['middle_candle']['low']} C={fvg['middle_candle']['close']}")
            print(f"   Next Candle     (8:45): O={fvg['next_candle']['open']} H={fvg['next_candle']['high']} L={fvg['next_candle']['low']} C={fvg['next_candle']['close']}")
            print("-" * 80)
    else:
        print("No FVGs found at 8:30:00")

if __name__ == "__main__":
    main()

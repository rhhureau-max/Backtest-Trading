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
    Detect Fair Value Gaps in the data.
    
    Args:
        data: List of candle dictionaries with OHLC data
        
    Returns:
        List of FVG events with details
    """
    fvgs = []
    
    # Need at least 3 candles to detect FVG
    for i in range(2, len(data)):
        current = data[i]
        middle = data[i-1]
        previous = data[i-2]
        
        # Bullish FVG: gap up (current low > previous high)
        if float(current['low']) > float(previous['high']):
            fvg = {
                'date': current['date'],
                'time': current['time'],
                'type': 'Bullish',
                'gap_start': previous['high'],
                'gap_end': current['low'],
                'gap_size': float(current['low']) - float(previous['high']),
                'current_candle': {
                    'open': current['open'],
                    'high': current['high'],
                    'low': current['low'],
                    'close': current['close']
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
        
        # Bearish FVG: gap down (current high < previous low)
        elif float(current['high']) < float(previous['low']):
            fvg = {
                'date': current['date'],
                'time': current['time'],
                'type': 'Bearish',
                'gap_start': current['high'],
                'gap_end': previous['low'],
                'gap_size': float(previous['low']) - float(current['high']),
                'current_candle': {
                    'open': current['open'],
                    'high': current['high'],
                    'low': current['low'],
                    'close': current['close']
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
    """Main function to find all FVGs at 8:30:00."""
    print("=" * 80)
    print("Fair Value Gap (FVG) Detection at 8:30:00")
    print("=" * 80)
    print()
    
    # Find all CSV files (exclude zip files)
    csv_files = sorted([f for f in glob.glob('*.csv') if not f.endswith('.zip')])
    
    all_fvgs_at_830 = []
    
    for filename in csv_files:
        print(f"Processing: {filename}")
        data = load_csv_data(filename)
        
        # Detect all FVGs
        fvgs = detect_fvg(data)
        
        # Filter for 8:30:00 only
        fvgs_at_830 = [fvg for fvg in fvgs if fvg['time'] == '08:30:00']
        
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
            print(f"   Previous Candle (i-2): O={fvg['previous_candle']['open']} H={fvg['previous_candle']['high']} L={fvg['previous_candle']['low']} C={fvg['previous_candle']['close']}")
            print(f"   Middle Candle   (i-1): O={fvg['middle_candle']['open']} H={fvg['middle_candle']['high']} L={fvg['middle_candle']['low']} C={fvg['middle_candle']['close']}")
            print(f"   Current Candle  (i)  : O={fvg['current_candle']['open']} H={fvg['current_candle']['high']} L={fvg['current_candle']['low']} C={fvg['current_candle']['close']}")
            print("-" * 80)
    else:
        print("No FVGs found at 8:30:00")

if __name__ == "__main__":
    main()

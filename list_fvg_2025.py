#!/usr/bin/env python3
"""
FVG List for 2025 at 8:30:00

This script provides a list of all FVGs at 8:30:00 in 2025 only.
"""

import csv
import glob

def detect_fvg(data):
    """Detect Fair Value Gaps in the data."""
    fvgs = []
    
    for i in range(2, len(data)):
        current = data[i]
        previous = data[i-2]
        
        # Bullish FVG
        if float(current['low']) > float(previous['high']):
            fvgs.append({
                'date': current['date'],
                'time': current['time'],
                'type': 'Bullish',
                'gap_size': float(current['low']) - float(previous['high'])
            })
        
        # Bearish FVG
        elif float(current['high']) < float(previous['low']):
            fvgs.append({
                'date': current['date'],
                'time': current['time'],
                'type': 'Bearish',
                'gap_size': float(previous['low']) - float(current['high'])
            })
    
    return fvgs

def load_csv_data(filename):
    """Load OHLC data from CSV file."""
    data = []
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=';')
        next(reader)  # Skip header
        
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
    """Main function to list all FVGs at 8:30:00 in 2025."""
    print("=" * 100)
    print("FVG List at 8:30:00 - Year 2025")
    print("=" * 100)
    
    # Get only 2025 CSV files
    csv_files = sorted([f for f in glob.glob('2025*.csv') if not f.endswith('.zip')])
    
    all_fvgs_2025 = []
    
    for filename in csv_files:
        data = load_csv_data(filename)
        fvgs = detect_fvg(data)
        fvgs_at_830 = [fvg for fvg in fvgs if fvg['time'] == '08:30:00']
        
        if fvgs_at_830:
            all_fvgs_2025.extend([(filename, fvg) for fvg in fvgs_at_830])
    
    print(f"\nTotal FVGs at 8:30:00 in 2025: {len(all_fvgs_2025)}\n")
    
    # Print table header
    print(f"{'#':<5} {'File':<20} {'Date':<12} {'Time':<10} {'Type':<10} {'Gap Size':<15}")
    print("-" * 100)
    
    # Print table rows
    for i, (filename, fvg) in enumerate(all_fvgs_2025, 1):
        print(f"{i:<5} {filename:<20} {fvg['date']:<12} {fvg['time']:<10} {fvg['type']:<10} {fvg['gap_size']:<15.6f}")
    
    print("=" * 100)
    print(f"Total: {len(all_fvgs_2025)} FVGs in 2025")

if __name__ == "__main__":
    main()

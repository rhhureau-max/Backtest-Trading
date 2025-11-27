#!/usr/bin/env python3
"""
FVG (Fair Value Gap) Analysis Script

This script analyzes 5-minute candle data to find and count all FVG patterns 
that occur between 8:30 and 10:00.

A FVG (Fair Value Gap) is defined as:
- Bullish FVG: When the low of the current candle is higher than the high of the candle 2 positions before (gap up)
- Bearish FVG: When the high of the current candle is lower than the low of the candle 2 positions before (gap down)
"""

import csv
import os
from datetime import datetime
from collections import defaultdict


def parse_time(time_str):
    """Parse time string in HH:MM:SS format."""
    return datetime.strptime(time_str, "%H:%M:%S").time()


def is_time_in_range(time_str, start_time="08:30:00", end_time="10:00:00"):
    """Check if time is between 8:30 and 10:00 (inclusive)."""
    time_obj = parse_time(time_str)
    start = parse_time(start_time)
    end = parse_time(end_time)
    return start <= time_obj <= end


def load_csv_data(filepath):
    """Load and parse CSV data from file."""
    data = []
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=';')
        # Skip header
        next(reader)
        for row in reader:
            if len(row) >= 7:
                try:
                    data.append({
                        'date': row[0],
                        'time': row[1],
                        'open': float(row[2]),
                        'high': float(row[3]),
                        'low': float(row[4]),
                        'close': float(row[5]),
                        'volume': int(row[6])
                    })
                except ValueError:
                    # Skip rows with invalid numeric data
                    continue
    return data


def filter_by_time_range(data, start_time="08:30:00", end_time="10:00:00"):
    """Filter candles to only include those between specified times."""
    return [candle for candle in data if is_time_in_range(candle['time'], start_time, end_time)]


def group_by_date(data):
    """Group candles by date to ensure FVG detection doesn't cross days."""
    grouped = defaultdict(list)
    for candle in data:
        grouped[candle['date']].append(candle)
    return grouped


def detect_fvg(candles):
    """
    Detect Fair Value Gaps in a sequence of candles.
    
    Returns a list of FVG occurrences with type and details.
    """
    fvg_list = []
    
    for i in range(2, len(candles)):
        candle_current = candles[i]
        candle_two_before = candles[i - 2]
        
        # Bullish FVG: current low > 2-candles-ago high (gap up)
        if candle_current['low'] > candle_two_before['high']:
            fvg_list.append({
                'type': 'Bullish',
                'date': candle_current['date'],
                'time': candle_current['time'],
                'gap_size': candle_current['low'] - candle_two_before['high'],
                'current_low': candle_current['low'],
                'two_before_high': candle_two_before['high']
            })
        
        # Bearish FVG: current high < 2-candles-ago low (gap down)
        elif candle_current['high'] < candle_two_before['low']:
            fvg_list.append({
                'type': 'Bearish',
                'date': candle_current['date'],
                'time': candle_current['time'],
                'gap_size': candle_two_before['low'] - candle_current['high'],
                'current_high': candle_current['high'],
                'two_before_low': candle_two_before['low']
            })
    
    return fvg_list


def analyze_year(filepath, year):
    """Analyze a single year's CSV file for FVG patterns."""
    print(f"\nAnalyzing {year}...")
    
    # Load data
    data = load_csv_data(filepath)
    print(f"  Total candles loaded: {len(data)}")
    
    # Filter by time range
    filtered_data = filter_by_time_range(data)
    print(f"  Candles in 8:30-10:00 window: {len(filtered_data)}")
    
    # Group by date
    grouped = group_by_date(filtered_data)
    print(f"  Number of trading days: {len(grouped)}")
    
    # Detect FVG for each day
    all_fvg = []
    sorted_dates = sorted(grouped.keys(), key=lambda d: datetime.strptime(d, "%d/%m/%Y"))
    for date in sorted_dates:
        day_candles = grouped[date]
        fvg_for_day = detect_fvg(day_candles)
        all_fvg.extend(fvg_for_day)
    
    # Count by type
    bullish_count = sum(1 for fvg in all_fvg if fvg['type'] == 'Bullish')
    bearish_count = sum(1 for fvg in all_fvg if fvg['type'] == 'Bearish')
    
    return {
        'year': year,
        'total_candles': len(data),
        'filtered_candles': len(filtered_data),
        'trading_days': len(grouped),
        'bullish_fvg': bullish_count,
        'bearish_fvg': bearish_count,
        'total_fvg': len(all_fvg),
        'fvg_details': all_fvg
    }


def main():
    """Main function to run FVG analysis on all years."""
    base_path = os.path.dirname(os.path.abspath(__file__))
    
    years = [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]
    
    results = []
    all_fvg_details = []
    
    print("=" * 60)
    print("FVG (Fair Value Gap) Analysis")
    print("Time Window: 8:30 - 10:00")
    print("=" * 60)
    
    for year in years:
        filepath = os.path.join(base_path, f"{year} 5m.csv")
        if os.path.exists(filepath):
            year_result = analyze_year(filepath, year)
            results.append(year_result)
            all_fvg_details.extend(year_result['fvg_details'])
        else:
            print(f"\nWarning: File not found - {filepath}")
    
    # Print summary
    print("\n" + "=" * 60)
    print("SUMMARY BY YEAR")
    print("=" * 60)
    print(f"{'Year':<8} {'Bullish FVG':<15} {'Bearish FVG':<15} {'Total FVG':<12}")
    print("-" * 60)
    
    total_bullish = 0
    total_bearish = 0
    total_fvg = 0
    
    for r in results:
        print(f"{r['year']:<8} {r['bullish_fvg']:<15} {r['bearish_fvg']:<15} {r['total_fvg']:<12}")
        total_bullish += r['bullish_fvg']
        total_bearish += r['bearish_fvg']
        total_fvg += r['total_fvg']
    
    print("-" * 60)
    print(f"{'TOTAL':<8} {total_bullish:<15} {total_bearish:<15} {total_fvg:<12}")
    print("=" * 60)
    
    # Save results to file
    output_file = os.path.join(base_path, "fvg_analysis_results.txt")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("FVG (Fair Value Gap) Analysis Results\n")
        f.write("Time Window: 8:30 - 10:00\n")
        f.write("=" * 80 + "\n\n")
        
        f.write("SUMMARY BY YEAR\n")
        f.write("-" * 80 + "\n")
        f.write(f"{'Year':<8} {'Trading Days':<15} {'Bullish FVG':<15} {'Bearish FVG':<15} {'Total FVG':<12}\n")
        f.write("-" * 80 + "\n")
        
        for r in results:
            f.write(f"{r['year']:<8} {r['trading_days']:<15} {r['bullish_fvg']:<15} {r['bearish_fvg']:<15} {r['total_fvg']:<12}\n")
        
        f.write("-" * 80 + "\n")
        f.write(f"{'TOTAL':<8} {'':<15} {total_bullish:<15} {total_bearish:<15} {total_fvg:<12}\n")
        f.write("=" * 80 + "\n\n")
        
        # Write detailed FVG list
        f.write("DETAILED FVG LIST\n")
        f.write("-" * 80 + "\n")
        f.write(f"{'Date':<12} {'Time':<12} {'Type':<10} {'Gap Size':<15}\n")
        f.write("-" * 80 + "\n")
        
        for fvg in all_fvg_details:
            f.write(f"{fvg['date']:<12} {fvg['time']:<12} {fvg['type']:<10} {fvg['gap_size']:<15.4f}\n")
        
        f.write("-" * 80 + "\n")
        f.write(f"\nTotal FVG found: {len(all_fvg_details)}\n")
    
    print(f"\nResults saved to: {output_file}")
    
    return results


if __name__ == "__main__":
    main()

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
    Also checks if price returns to the FVG before 10:00.
    """
    fvg_list = []
    
    for i in range(2, len(candles)):
        candle_current = candles[i]
        candle_two_before = candles[i - 2]
        
        # Bullish FVG: current low > 2-candles-ago high (gap up)
        if candle_current['low'] > candle_two_before['high']:
            fvg_top = candle_current['low']
            fvg_bottom = candle_two_before['high']
            
            # Check if price returns to FVG (price goes down to touch the gap zone)
            filled = False
            for j in range(i + 1, len(candles)):
                # Price returns to FVG if the low of subsequent candle touches the FVG zone
                if candles[j]['low'] <= fvg_top:
                    filled = True
                    break
            
            fvg_list.append({
                'type': 'Bullish',
                'date': candle_current['date'],
                'time': candle_current['time'],
                'gap_size': fvg_top - fvg_bottom,
                'current_low': fvg_top,
                'two_before_high': fvg_bottom,
                'fvg_top': fvg_top,
                'fvg_bottom': fvg_bottom,
                'filled': filled
            })
        
        # Bearish FVG: current high < 2-candles-ago low (gap down)
        elif candle_current['high'] < candle_two_before['low']:
            fvg_top = candle_two_before['low']
            fvg_bottom = candle_current['high']
            
            # Check if price returns to FVG (price goes up to touch the gap zone)
            filled = False
            for j in range(i + 1, len(candles)):
                # Price returns to FVG if the high of subsequent candle touches the FVG zone
                if candles[j]['high'] >= fvg_bottom:
                    filled = True
                    break
            
            fvg_list.append({
                'type': 'Bearish',
                'date': candle_current['date'],
                'time': candle_current['time'],
                'gap_size': fvg_top - fvg_bottom,
                'current_high': fvg_bottom,
                'two_before_low': fvg_top,
                'fvg_top': fvg_top,
                'fvg_bottom': fvg_bottom,
                'filled': filled
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
    
    # Count filled FVGs
    filled_count = sum(1 for fvg in all_fvg if fvg['filled'])
    bullish_filled = sum(1 for fvg in all_fvg if fvg['type'] == 'Bullish' and fvg['filled'])
    bearish_filled = sum(1 for fvg in all_fvg if fvg['type'] == 'Bearish' and fvg['filled'])
    
    return {
        'year': year,
        'total_candles': len(data),
        'filtered_candles': len(filtered_data),
        'trading_days': len(grouped),
        'bullish_fvg': bullish_count,
        'bearish_fvg': bearish_count,
        'total_fvg': len(all_fvg),
        'filled_count': filled_count,
        'bullish_filled': bullish_filled,
        'bearish_filled': bearish_filled,
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
    total_filled = 0
    total_bullish_filled = 0
    total_bearish_filled = 0
    
    for r in results:
        print(f"{r['year']:<8} {r['bullish_fvg']:<15} {r['bearish_fvg']:<15} {r['total_fvg']:<12}")
        total_bullish += r['bullish_fvg']
        total_bearish += r['bearish_fvg']
        total_fvg += r['total_fvg']
        total_filled += r['filled_count']
        total_bullish_filled += r['bullish_filled']
        total_bearish_filled += r['bearish_filled']
    
    print("-" * 60)
    print(f"{'TOTAL':<8} {total_bullish:<15} {total_bearish:<15} {total_fvg:<12}")
    print("=" * 60)
    
    # Print FVG fill statistics
    print("\n" + "=" * 80)
    print("FVG FILL ANALYSIS - Price returns to FVG before 10:00")
    print("=" * 80)
    print(f"{'Year':<8} {'Total FVG':<12} {'Filled':<12} {'Fill %':<10} {'Bullish Filled':<18} {'Bearish Filled':<18}")
    print("-" * 80)
    
    for r in results:
        fill_pct = (r['filled_count'] / r['total_fvg'] * 100) if r['total_fvg'] > 0 else 0
        bull_fill_str = f"{r['bullish_filled']}/{r['bullish_fvg']}"
        bear_fill_str = f"{r['bearish_filled']}/{r['bearish_fvg']}"
        print(f"{r['year']:<8} {r['total_fvg']:<12} {r['filled_count']:<12} {fill_pct:<10.1f} {bull_fill_str:<18} {bear_fill_str:<18}")
    
    print("-" * 80)
    total_fill_pct = (total_filled / total_fvg * 100) if total_fvg > 0 else 0
    total_bull_str = f"{total_bullish_filled}/{total_bullish}"
    total_bear_str = f"{total_bearish_filled}/{total_bearish}"
    print(f"{'TOTAL':<8} {total_fvg:<12} {total_filled:<12} {total_fill_pct:<10.1f} {total_bull_str:<18} {total_bear_str:<18}")
    print("=" * 80)
    
    # Save results to file
    output_file = os.path.join(base_path, "fvg_analysis_results.txt")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("=" * 100 + "\n")
        f.write("FVG (Fair Value Gap) Analysis Results\n")
        f.write("Time Window: 8:30 - 10:00\n")
        f.write("=" * 100 + "\n\n")
        
        f.write("SUMMARY BY YEAR\n")
        f.write("-" * 100 + "\n")
        f.write(f"{'Year':<8} {'Trading Days':<15} {'Bullish FVG':<15} {'Bearish FVG':<15} {'Total FVG':<12}\n")
        f.write("-" * 100 + "\n")
        
        for r in results:
            f.write(f"{r['year']:<8} {r['trading_days']:<15} {r['bullish_fvg']:<15} {r['bearish_fvg']:<15} {r['total_fvg']:<12}\n")
        
        f.write("-" * 100 + "\n")
        f.write(f"{'TOTAL':<8} {'':<15} {total_bullish:<15} {total_bearish:<15} {total_fvg:<12}\n")
        f.write("=" * 100 + "\n\n")
        
        # FVG Fill Analysis section
        f.write("FVG FILL ANALYSIS - Price returns to FVG before 10:00\n")
        f.write("-" * 100 + "\n")
        f.write(f"{'Year':<8} {'Total FVG':<12} {'Filled':<12} {'Fill %':<10} {'Bullish Filled':<18} {'Bearish Filled':<18}\n")
        f.write("-" * 100 + "\n")
        
        for r in results:
            fill_pct = (r['filled_count'] / r['total_fvg'] * 100) if r['total_fvg'] > 0 else 0
            bull_fill_str = f"{r['bullish_filled']}/{r['bullish_fvg']}"
            bear_fill_str = f"{r['bearish_filled']}/{r['bearish_fvg']}"
            f.write(f"{r['year']:<8} {r['total_fvg']:<12} {r['filled_count']:<12} {fill_pct:<10.1f} {bull_fill_str:<18} {bear_fill_str:<18}\n")
        
        f.write("-" * 100 + "\n")
        f.write(f"{'TOTAL':<8} {total_fvg:<12} {total_filled:<12} {total_fill_pct:<10.1f} {total_bull_str:<18} {total_bear_str:<18}\n")
        f.write("=" * 100 + "\n\n")
        
        # Write detailed FVG list with fill status
        f.write("DETAILED FVG LIST\n")
        f.write("-" * 100 + "\n")
        f.write(f"{'Date':<12} {'Time':<12} {'Type':<10} {'Gap Size':<15} {'Filled':<10}\n")
        f.write("-" * 100 + "\n")
        
        for fvg in all_fvg_details:
            filled_str = "Yes" if fvg['filled'] else "No"
            f.write(f"{fvg['date']:<12} {fvg['time']:<12} {fvg['type']:<10} {fvg['gap_size']:<15.4f} {filled_str:<10}\n")
        
        f.write("-" * 100 + "\n")
        f.write(f"\nTotal FVG found: {len(all_fvg_details)}\n")
        f.write(f"Total FVG filled before 10:00: {total_filled} ({total_fill_pct:.1f}%)\n")
    
    print(f"\nResults saved to: {output_file}")
    
    return results


if __name__ == "__main__":
    main()

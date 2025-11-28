#!/usr/bin/env python3
"""
FVG (Fair Value Gap) Analysis Script

This script analyzes Fair Value Gaps on 15-minute candles at 08:30 AM for each trading day.

A FVG (imbalance) exists when there is a gap between:
- Bullish FVG: Low of n+1 (08:45) > High of n-1 (08:15) - gap upward
- Bearish FVG: High of n+1 (08:45) < Low of n-1 (08:15) - gap downward
"""

import os
import sys
import glob
from datetime import datetime
from typing import NamedTuple


class Candle(NamedTuple):
    """Represents a candlestick with OHLCV data."""
    date: str
    time: str
    open: float
    high: float
    low: float
    close: float
    volume: int


class FVG(NamedTuple):
    """Represents a Fair Value Gap."""
    date: str
    fvg_type: str  # 'bullish' or 'bearish'
    gap_size: float
    candle_n_minus_1_high: float
    candle_n_minus_1_low: float
    candle_n_high: float
    candle_n_low: float
    candle_n_plus_1_high: float
    candle_n_plus_1_low: float


def parse_csv_line(line: str) -> Candle:
    """Parse a CSV line and return a Candle object."""
    parts = line.strip().split(';')
    return Candle(
        date=parts[0],
        time=parts[1],
        open=float(parts[2]),
        high=float(parts[3]),
        low=float(parts[4]),
        close=float(parts[5]),
        volume=int(parts[6])
    )


def load_csv_data(filepath: str) -> dict:
    """
    Load CSV data and return a dictionary organized by date.
    Key: (date, time), Value: Candle
    """
    data = {}
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            next(f)  # Skip header
            for line in f:
                if line.strip():
                    candle = parse_csv_line(line)
                    key = (candle.date, candle.time)
                    data[key] = candle
    except FileNotFoundError:
        print(f"Error: File not found - {filepath}")
    except PermissionError:
        print(f"Error: Permission denied - {filepath}")
    except (ValueError, IndexError) as e:
        print(f"Error: Invalid data format in {filepath} - {e}")
    return data


def find_fvgs_at_0830(data: dict) -> list:
    """
    Find FVGs at 08:30 candles.
    
    For each 08:30 candle, check if:
    - Bullish FVG: Low of 08:45 (n+1) > High of 08:15 (n-1)
    - Bearish FVG: High of 08:45 (n+1) < Low of 08:15 (n-1)
    """
    fvgs = []
    
    # Get all unique dates
    dates = sorted(set(date for date, time in data.keys()))
    
    for date in dates:
        # Get the three candles needed
        candle_0815 = data.get((date, '08:15:00'))
        candle_0830 = data.get((date, '08:30:00'))
        candle_0845 = data.get((date, '08:45:00'))
        
        # Skip if any candle is missing
        if not all([candle_0815, candle_0830, candle_0845]):
            continue
        
        # Check for Bullish FVG: Low of n+1 > High of n-1
        if candle_0845.low > candle_0815.high:
            gap_size = candle_0845.low - candle_0815.high
            fvg = FVG(
                date=date,
                fvg_type='bullish',
                gap_size=gap_size,
                candle_n_minus_1_high=candle_0815.high,
                candle_n_minus_1_low=candle_0815.low,
                candle_n_high=candle_0830.high,
                candle_n_low=candle_0830.low,
                candle_n_plus_1_high=candle_0845.high,
                candle_n_plus_1_low=candle_0845.low
            )
            fvgs.append(fvg)
        
        # Check for Bearish FVG: High of n+1 < Low of n-1
        elif candle_0845.high < candle_0815.low:
            gap_size = candle_0815.low - candle_0845.high
            fvg = FVG(
                date=date,
                fvg_type='bearish',
                gap_size=gap_size,
                candle_n_minus_1_high=candle_0815.high,
                candle_n_minus_1_low=candle_0815.low,
                candle_n_high=candle_0830.high,
                candle_n_low=candle_0830.low,
                candle_n_plus_1_high=candle_0845.high,
                candle_n_plus_1_low=candle_0845.low
            )
            fvgs.append(fvg)
    
    return fvgs


def analyze_all_files(base_path: str) -> tuple:
    """
    Analyze all 15m CSV files and return FVGs and statistics.
    """
    all_fvgs = []
    files_processed = []
    total_days_analyzed = 0
    
    # Find all 15m CSV files
    pattern = os.path.join(base_path, "*15m.csv")
    csv_files = sorted(glob.glob(pattern))
    
    for filepath in csv_files:
        filename = os.path.basename(filepath)
        # Robustly extract year from filename (format: "YYYY 15m.csv")
        parts = filename.split()
        if not parts or not parts[0].isdigit():
            print(f"Skipping {filename}: unexpected filename format")
            continue
        year = parts[0]
        
        print(f"Processing {filename}...")
        data = load_csv_data(filepath)
        
        # Count days with 08:30 candles
        dates_with_0830 = set(
            date for date, time in data.keys() 
            if time == '08:30:00'
        )
        total_days_analyzed += len(dates_with_0830)
        
        fvgs = find_fvgs_at_0830(data)
        all_fvgs.extend(fvgs)
        
        files_processed.append({
            'filename': filename,
            'year': year,
            'days_analyzed': len(dates_with_0830),
            'fvgs_found': len(fvgs),
            'bullish': sum(1 for f in fvgs if f.fvg_type == 'bullish'),
            'bearish': sum(1 for f in fvgs if f.fvg_type == 'bearish')
        })
    
    return all_fvgs, files_processed, total_days_analyzed


def generate_report(fvgs: list, files_stats: list, total_days: int, output_path: str):
    """Generate a markdown report with FVG analysis results."""
    
    total_fvgs = len(fvgs)
    bullish_count = sum(1 for f in fvgs if f.fvg_type == 'bullish')
    bearish_count = sum(1 for f in fvgs if f.fvg_type == 'bearish')
    
    # Calculate average gap sizes
    bullish_fvgs = [f for f in fvgs if f.fvg_type == 'bullish']
    bearish_fvgs = [f for f in fvgs if f.fvg_type == 'bearish']
    
    avg_bullish_gap = sum(f.gap_size for f in bullish_fvgs) / len(bullish_fvgs) if bullish_fvgs else 0
    avg_bearish_gap = sum(f.gap_size for f in bearish_fvgs) / len(bearish_fvgs) if bearish_fvgs else 0
    
    # Find largest gaps
    largest_bullish = max(bullish_fvgs, key=lambda f: f.gap_size) if bullish_fvgs else None
    largest_bearish = max(bearish_fvgs, key=lambda f: f.gap_size) if bearish_fvgs else None
    
    report = f"""# FVG (Fair Value Gap) Analysis Results

## Analysis Summary

- **Analysis Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Data Range**: 2018 - 2025
- **Candle Timeframe**: 15 minutes
- **Target Time**: 08:30 (analyzed with 08:15 and 08:45 candles)

## FVG Definition

A **Fair Value Gap (FVG)** or imbalance at 08:30 exists when:
- **Bullish FVG**: Low of the 08:45 candle (n+1) > High of the 08:15 candle (n-1)
- **Bearish FVG**: High of the 08:45 candle (n+1) < Low of the 08:15 candle (n-1)

---

## Overall Results

| Metric | Value |
|--------|-------|
| **Total Days Analyzed** | {total_days:,} |
| **Total FVGs Found** | {total_fvgs:,} |
| **Bullish FVGs** | {bullish_count:,} ({bullish_count/total_fvgs*100:.1f}% of FVGs) |
| **Bearish FVGs** | {bearish_count:,} ({bearish_count/total_fvgs*100:.1f}% of FVGs) |
| **FVG Occurrence Rate** | {total_fvgs/total_days*100:.2f}% of trading days |

---

## FVG Statistics

### Gap Size Analysis

| Type | Average Gap Size | Largest Gap |
|------|-----------------|-------------|
| Bullish | {avg_bullish_gap:.2f} | {largest_bullish.gap_size:.2f} on {largest_bullish.date if largest_bullish else 'N/A'} |
| Bearish | {avg_bearish_gap:.2f} | {largest_bearish.gap_size:.2f} on {largest_bearish.date if largest_bearish else 'N/A'} |

---

## Results by Year

| Year | Days Analyzed | Total FVGs | Bullish | Bearish | FVG Rate |
|------|--------------|------------|---------|---------|----------|
"""
    
    for stat in files_stats:
        fvg_rate = stat['fvgs_found'] / stat['days_analyzed'] * 100 if stat['days_analyzed'] > 0 else 0
        report += f"| {stat['year']} | {stat['days_analyzed']:,} | {stat['fvgs_found']} | {stat['bullish']} | {stat['bearish']} | {fvg_rate:.2f}% |\n"

    report += f"""
---

## Detailed FVG List

### All FVGs Found ({total_fvgs} total)

| # | Date | Type | Gap Size | 08:15 High | 08:15 Low | 08:30 High | 08:30 Low | 08:45 High | 08:45 Low |
|---|------|------|----------|------------|-----------|------------|-----------|------------|-----------|
"""
    
    # Sort FVGs by date
    sorted_fvgs = sorted(fvgs, key=lambda f: datetime.strptime(f.date, '%d/%m/%Y'))
    
    for i, fvg in enumerate(sorted_fvgs, 1):
        report += f"| {i} | {fvg.date} | {fvg.fvg_type.capitalize()} | {fvg.gap_size:.2f} | {fvg.candle_n_minus_1_high:.2f} | {fvg.candle_n_minus_1_low:.2f} | {fvg.candle_n_high:.2f} | {fvg.candle_n_low:.2f} | {fvg.candle_n_plus_1_high:.2f} | {fvg.candle_n_plus_1_low:.2f} |\n"

    report += """
---

## Notes

- FVGs are identified using the 08:15 (n-1), 08:30 (n), and 08:45 (n+1) candles
- Days with missing candles at any of these times are excluded from analysis
- Gap size represents the absolute difference creating the imbalance
- All price values are from the source CSV files without modification
"""
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\nReport saved to: {output_path}")


def main():
    """Main function to run the FVG analysis."""
    # Allow configurable base path via command-line argument or use current directory
    if len(sys.argv) > 1:
        base_path = sys.argv[1]
    else:
        base_path = os.path.dirname(os.path.abspath(__file__)) or "."
    
    output_path = os.path.join(base_path, "FVG_ANALYSIS_RESULTS.md")
    
    print("=" * 60)
    print("FVG (Fair Value Gap) Analysis - 08:30 Candles")
    print("=" * 60)
    print()
    
    # Analyze all files
    fvgs, files_stats, total_days = analyze_all_files(base_path)
    
    print()
    print("=" * 60)
    print("ANALYSIS COMPLETE")
    print("=" * 60)
    print(f"Total days analyzed: {total_days:,}")
    print(f"Total FVGs found: {len(fvgs):,}")
    print(f"  - Bullish: {sum(1 for f in fvgs if f.fvg_type == 'bullish'):,}")
    print(f"  - Bearish: {sum(1 for f in fvgs if f.fvg_type == 'bearish'):,}")
    
    # Generate report
    generate_report(fvgs, files_stats, total_days, output_path)
    
    print()
    print("Analysis complete!")


if __name__ == "__main__":
    main()

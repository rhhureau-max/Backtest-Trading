#!/usr/bin/env python3
"""
FVG (Fair Value Gap) Retracement and Continuation Probability Analysis

This script analyzes OHLCV data to:
1. Detect Fair Value Gaps (FVGs)
2. Identify when FVGs are completely filled
3. Analyze continuation probability after FVG fill
"""

import os
import glob
import argparse
from datetime import datetime
from collections import defaultdict


def parse_csv_file(filepath):
    """Parse a semicolon-delimited CSV file and return list of candles."""
    candles = []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        # Skip header
        next(f, None)
        
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            parts = line.split(';')
            if len(parts) < 7:
                continue
            
            try:
                # Parse date (DD/MM/YYYY) and time (HH:MM:SS)
                date_str = parts[0]
                time_str = parts[1]
                datetime_str = f"{date_str} {time_str}"
                dt = datetime.strptime(datetime_str, "%d/%m/%Y %H:%M:%S")
                
                candle = {
                    'datetime': dt,
                    'open': float(parts[2]),
                    'high': float(parts[3]),
                    'low': float(parts[4]),
                    'close': float(parts[5]),
                    'volume': float(parts[6])
                }
                candles.append(candle)
            except (ValueError, IndexError):
                # Skip malformed rows
                continue
    
    return candles


def load_timeframe_data(base_dir, timeframe, years=None):
    """Load all data for a specific timeframe across multiple years."""
    if years is None:
        # Default to detecting available years dynamically
        years = detect_available_years(base_dir, timeframe) if 'detect_available_years' in dir() else range(2018, datetime.now().year + 2)
    
    all_candles = []
    
    for year in years:
        filepath = os.path.join(base_dir, f"{year} {timeframe}.csv")
        if os.path.exists(filepath):
            candles = parse_csv_file(filepath)
            all_candles.extend(candles)
            print(f"  Loaded {len(candles)} candles from {year} {timeframe}.csv")
    
    # Sort by datetime
    all_candles.sort(key=lambda x: x['datetime'])
    return all_candles


def detect_fvgs(candles):
    """
    Detect Fair Value Gaps in the candle data.
    
    Bullish FVG: candle[i].low > candle[i-2].high (gap up)
    Bearish FVG: candle[i].high < candle[i-2].low (gap down)
    
    Returns list of FVG dictionaries with:
    - type: 'bullish' or 'bearish'
    - index: index of the third candle (where FVG is confirmed)
    - gap_high: upper boundary of the gap
    - gap_low: lower boundary of the gap
    - datetime: datetime of the FVG formation
    """
    fvgs = []
    
    for i in range(2, len(candles)):
        candle_current = candles[i]
        candle_prev2 = candles[i - 2]
        
        # Check for bullish FVG (gap up)
        if candle_current['low'] > candle_prev2['high']:
            fvg = {
                'type': 'bullish',
                'index': i,
                'gap_high': candle_current['low'],
                'gap_low': candle_prev2['high'],
                'datetime': candle_current['datetime'],
                'filled': False,
                'fill_index': None
            }
            fvgs.append(fvg)
        
        # Check for bearish FVG (gap down)
        elif candle_current['high'] < candle_prev2['low']:
            fvg = {
                'type': 'bearish',
                'index': i,
                'gap_high': candle_prev2['low'],
                'gap_low': candle_current['high'],
                'datetime': candle_current['datetime'],
                'filled': False,
                'fill_index': None
            }
            fvgs.append(fvg)
    
    return fvgs


def check_fvg_fill(fvg, candle):
    """
    Check if a candle completely fills the FVG.
    
    For a bullish FVG: the candle must trade through the entire gap
    (candle.low <= gap_low means it went down to cover the gap)
    
    For a bearish FVG: the candle must trade through the entire gap
    (candle.high >= gap_high means it went up to cover the gap)
    """
    if fvg['type'] == 'bullish':
        # Bullish FVG is filled when price comes down and covers the gap
        # Candle must reach down to or below the gap_low
        return candle['low'] <= fvg['gap_low']
    else:
        # Bearish FVG is filled when price goes up and covers the gap
        # Candle must reach up to or above the gap_high
        return candle['high'] >= fvg['gap_high']


def check_candle_retraces_into_fvg(fvg, candle):
    """
    Check if a candle retraces INTO the FVG zone.
    """
    if fvg['type'] == 'bullish':
        # For bullish FVG, price needs to come down into the gap
        return candle['low'] <= fvg['gap_high']
    else:
        # For bearish FVG, price needs to go up into the gap
        return candle['high'] >= fvg['gap_low']


def is_continuation_candle(candle, fvg_type):
    """
    Check if a candle is a continuation candle based on FVG type.
    
    For bullish FVG: continuation = bullish candle (close > open)
    For bearish FVG: continuation = bearish candle (close < open)
    """
    if fvg_type == 'bullish':
        return candle['close'] > candle['open']
    else:
        return candle['close'] < candle['open']


def analyze_fvg_continuation(candles, fvgs):
    """
    Analyze continuation probability after FVG fill.
    
    Returns statistics for continuation at candle+1, +2, +3 after fill.
    """
    results = {
        'bullish': {
            'total_filled': 0,
            'continuation_1': 0,
            'continuation_2': 0,
            'continuation_3': 0,
            'samples_1': 0,
            'samples_2': 0,
            'samples_3': 0
        },
        'bearish': {
            'total_filled': 0,
            'continuation_1': 0,
            'continuation_2': 0,
            'continuation_3': 0,
            'samples_1': 0,
            'samples_2': 0,
            'samples_3': 0
        }
    }
    
    filled_fvgs = []
    
    for fvg in fvgs:
        fvg_index = fvg['index']
        fvg_type = fvg['type']
        
        # Look for the first candle that completely fills the FVG
        # Start from the candle after the FVG formation
        for j in range(fvg_index + 1, len(candles)):
            candle = candles[j]
            
            # Check if this candle completely fills the FVG
            # (filling implies retracement since price must cross the gap zone)
            if check_fvg_fill(fvg, candle):
                fvg['filled'] = True
                fvg['fill_index'] = j
                results[fvg_type]['total_filled'] += 1
                
                filled_fvg_info = {
                    'fvg': fvg,
                    'fill_index': j,
                    'fill_datetime': candle['datetime']
                }
                
                # Analyze continuation for candle+1, +2, +3
                for offset, key_cont, key_samp in [
                    (1, 'continuation_1', 'samples_1'),
                    (2, 'continuation_2', 'samples_2'),
                    (3, 'continuation_3', 'samples_3')
                ]:
                    if j + offset < len(candles):
                        results[fvg_type][key_samp] += 1
                        if is_continuation_candle(candles[j + offset], fvg_type):
                            results[fvg_type][key_cont] += 1
                
                filled_fvgs.append(filled_fvg_info)
                break  # Move to next FVG after finding first fill
    
    return results, filled_fvgs


def print_statistics(results, timeframe):
    """Print detailed statistics for a timeframe."""
    print(f"\n{'='*60}")
    print(f"  {timeframe} TIMEFRAME ANALYSIS")
    print(f"{'='*60}")
    
    for fvg_type in ['bullish', 'bearish']:
        data = results[fvg_type]
        print(f"\n{'-'*40}")
        print(f"  {fvg_type.upper()} FVG STATISTICS")
        print(f"{'-'*40}")
        print(f"  Total FVGs filled: {data['total_filled']}")
        
        for i in range(1, 4):
            samples = data[f'samples_{i}']
            continuations = data[f'continuation_{i}']
            
            if samples > 0:
                win_rate = (continuations / samples) * 100
                print(f"\n  Candle +{i} after fill:")
                print(f"    Samples: {samples}")
                print(f"    Continuations: {continuations}")
                print(f"    Win Rate: {win_rate:.2f}%")
            else:
                print(f"\n  Candle +{i} after fill:")
                print(f"    No samples available")


def generate_summary_report(all_results, output_path):
    """Generate a comprehensive summary report."""
    
    report_lines = []
    report_lines.append("="*70)
    report_lines.append("FVG (FAIR VALUE GAP) CONTINUATION ANALYSIS REPORT")
    report_lines.append("="*70)
    report_lines.append(f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append("\n" + "="*70)
    report_lines.append("METHODOLOGY")
    report_lines.append("="*70)
    report_lines.append("""
FVG Detection:
- Bullish FVG: candle[i].low > candle[i-2].high (gap up)
- Bearish FVG: candle[i].high < candle[i-2].low (gap down)

FVG Fill Detection:
- Bullish FVG filled: when a candle's low reaches or goes below gap_low
- Bearish FVG filled: when a candle's high reaches or goes above gap_high

Continuation Definition:
- After bullish FVG fill: continuation = bullish candle (close > open)
- After bearish FVG fill: continuation = bearish candle (close < open)
""")
    
    report_lines.append("\n" + "="*70)
    report_lines.append("DETAILED RESULTS")
    report_lines.append("="*70)
    
    # Summary table
    report_lines.append("\n" + "-"*70)
    report_lines.append(f"{'Timeframe':<10} {'FVG Type':<10} {'Filled':<8} "
                       f"{'C+1 Rate':<12} {'C+2 Rate':<12} {'C+3 Rate':<12}")
    report_lines.append("-"*70)
    
    for timeframe, results in all_results.items():
        for fvg_type in ['bullish', 'bearish']:
            data = results[fvg_type]
            filled = data['total_filled']
            
            rates = []
            for i in range(1, 4):
                samples = data[f'samples_{i}']
                cont = data[f'continuation_{i}']
                if samples > 0:
                    rate = (cont / samples) * 100
                    rates.append(f"{rate:.1f}% ({cont}/{samples})")
                else:
                    rates.append("N/A")
            
            report_lines.append(f"{timeframe:<10} {fvg_type.capitalize():<10} {filled:<8} "
                               f"{rates[0]:<12} {rates[1]:<12} {rates[2]:<12}")
    
    report_lines.append("-"*70)
    
    # Combined statistics
    report_lines.append("\n" + "="*70)
    report_lines.append("COMBINED STATISTICS (ALL TIMEFRAMES)")
    report_lines.append("="*70)
    
    combined = {
        'bullish': defaultdict(int),
        'bearish': defaultdict(int)
    }
    
    for timeframe, results in all_results.items():
        for fvg_type in ['bullish', 'bearish']:
            data = results[fvg_type]
            combined[fvg_type]['total_filled'] += data['total_filled']
            for i in range(1, 4):
                combined[fvg_type][f'continuation_{i}'] += data[f'continuation_{i}']
                combined[fvg_type][f'samples_{i}'] += data[f'samples_{i}']
    
    for fvg_type in ['bullish', 'bearish']:
        data = combined[fvg_type]
        report_lines.append(f"\n{fvg_type.upper()} FVG (Combined):")
        report_lines.append(f"  Total FVGs filled: {data['total_filled']}")
        
        for i in range(1, 4):
            samples = data[f'samples_{i}']
            cont = data[f'continuation_{i}']
            if samples > 0:
                rate = (cont / samples) * 100
                report_lines.append(f"  Candle +{i}: {rate:.2f}% win rate ({cont}/{samples})")
            else:
                report_lines.append(f"  Candle +{i}: N/A (no samples)")
    
    # Overall statistics
    report_lines.append("\n" + "="*70)
    report_lines.append("OVERALL STATISTICS (ALL FVG TYPES)")
    report_lines.append("="*70)
    
    overall = defaultdict(int)
    for fvg_type in ['bullish', 'bearish']:
        data = combined[fvg_type]
        overall['total_filled'] += data['total_filled']
        for i in range(1, 4):
            overall[f'continuation_{i}'] += data[f'continuation_{i}']
            overall[f'samples_{i}'] += data[f'samples_{i}']
    
    report_lines.append(f"\nTotal FVGs filled: {overall['total_filled']}")
    for i in range(1, 4):
        samples = overall[f'samples_{i}']
        cont = overall[f'continuation_{i}']
        if samples > 0:
            rate = (cont / samples) * 100
            report_lines.append(f"Candle +{i}: {rate:.2f}% win rate ({cont}/{samples})")
        else:
            report_lines.append(f"Candle +{i}: N/A (no samples)")
    
    report_lines.append("\n" + "="*70)
    report_lines.append("END OF REPORT")
    report_lines.append("="*70)
    
    # Write report to file
    report_text = "\n".join(report_lines)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report_text)
    
    return report_text


def detect_available_years(base_dir, timeframe):
    """Detect available years for a given timeframe based on existing CSV files."""
    years = []
    pattern = os.path.join(base_dir, f"* {timeframe}.csv")
    files = glob.glob(pattern)
    
    for filepath in files:
        filename = os.path.basename(filepath)
        # Extract year from filename like "2018 1H.csv"
        try:
            year = int(filename.split()[0])
            years.append(year)
        except (ValueError, IndexError):
            continue
    
    return sorted(years)


def main():
    """Main function to run the FVG continuation analysis."""
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description='FVG (Fair Value Gap) Retracement and Continuation Probability Analysis'
    )
    parser.add_argument(
        '--data-dir',
        type=str,
        default=os.path.dirname(os.path.abspath(__file__)),
        help='Directory containing the CSV data files (default: script directory)'
    )
    parser.add_argument(
        '--timeframes',
        type=str,
        nargs='+',
        default=['1H', '4H'],
        help='Timeframes to analyze (default: 1H 4H)'
    )
    parser.add_argument(
        '--output',
        type=str,
        default=None,
        help='Output report file path (default: <data-dir>/fvg_analysis_report.txt)'
    )
    
    args = parser.parse_args()
    
    base_dir = args.data_dir
    timeframes = args.timeframes
    
    print("="*60)
    print("FVG CONTINUATION ANALYSIS")
    print("="*60)
    print(f"\nData directory: {base_dir}")
    print(f"Analyzing timeframes: {', '.join(timeframes)}")
    
    all_results = {}
    
    for timeframe in timeframes:
        print(f"\n{'='*60}")
        print(f"Loading {timeframe} data...")
        print("="*60)
        
        # Detect available years for this timeframe
        years = detect_available_years(base_dir, timeframe)
        
        if not years:
            print(f"No data files found for {timeframe}")
            continue
        
        print(f"Detected years: {min(years)} - {max(years)}")
        
        # Load data
        candles = load_timeframe_data(base_dir, timeframe, years)
        
        if not candles:
            print(f"No data found for {timeframe}")
            continue
        
        print(f"\nTotal candles loaded: {len(candles)}")
        print(f"Date range: {candles[0]['datetime']} to {candles[-1]['datetime']}")
        
        # Detect FVGs
        print(f"\nDetecting FVGs...")
        fvgs = detect_fvgs(candles)
        bullish_count = sum(1 for f in fvgs if f['type'] == 'bullish')
        bearish_count = sum(1 for f in fvgs if f['type'] == 'bearish')
        print(f"  Total FVGs detected: {len(fvgs)}")
        print(f"    Bullish: {bullish_count}")
        print(f"    Bearish: {bearish_count}")
        
        # Analyze continuation
        print(f"\nAnalyzing FVG fills and continuations...")
        results, filled_fvgs = analyze_fvg_continuation(candles, fvgs)
        
        all_results[timeframe] = results
        
        # Print statistics for this timeframe
        print_statistics(results, timeframe)
    
    # Generate and save summary report
    report_path = args.output if args.output else os.path.join(base_dir, "fvg_analysis_report.txt")
    print(f"\n{'='*60}")
    print("GENERATING SUMMARY REPORT")
    print("="*60)
    
    report = generate_summary_report(all_results, report_path)
    print(report)
    
    print(f"\nReport saved to: {report_path}")
    print("\nAnalysis complete!")


if __name__ == "__main__":
    main()

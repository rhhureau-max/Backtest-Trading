#!/usr/bin/env python3
"""
FVG Breakout Strategy Backtest

This script backtests a strategy based on FVG (Fair Value Gap) breakouts:

For Bearish FVG:
- When price closes above the FVG (above the low wick of candle n+1), enter SHORT
- SL is placed above the broken bearish FVG (at fvg_top)
- Calculate probability of hitting TP at ratios 1:1, 1.5:1, 2:1, 2.5:1, 3:1, 3.5:1

For Bullish FVG:
- When price closes below the FVG (below the high wick of candle n+1), enter LONG
- SL is placed below the broken bullish FVG (at fvg_bottom)
- Calculate probability of hitting TP at ratios 1:1, 1.5:1, 2:1, 2.5:1, 3:1, 3.5:1
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
                    continue
    return data


def filter_by_time_range(data, start_time="08:30:00", end_time="10:00:00"):
    """Filter candles to only include those between specified times."""
    return [candle for candle in data if is_time_in_range(candle['time'], start_time, end_time)]


def group_by_date(data):
    """Group candles by date."""
    grouped = defaultdict(list)
    for candle in data:
        grouped[candle['date']].append(candle)
    return grouped


def detect_fvg_with_breakout(candles):
    """
    Detect FVG and check for breakout entries.
    
    For Bearish FVG (gap down):
    - FVG is formed at candle i (current high < 2-candles-ago low)
    - Candle n+1 is at index i-1 (the middle candle)
    - If price closes above the low of candle n+1, it's a breakout -> SHORT entry
    
    For Bullish FVG (gap up):
    - FVG is formed at candle i (current low > 2-candles-ago high)
    - Candle n+1 is at index i-1 (the middle candle)
    - If price closes below the high of candle n+1, it's a breakout -> LONG entry
    
    Returns trades with entry, SL, and TP hit results.
    """
    trades = []
    rr_ratios = [1.0, 1.5, 2.0, 2.5, 3.0, 3.5]
    
    for i in range(2, len(candles)):
        candle_current = candles[i]          # Candle n+2 (completes the FVG)
        candle_middle = candles[i - 1]       # Candle n+1 (middle candle)
        candle_two_before = candles[i - 2]   # Candle n (first candle)
        
        # Bearish FVG: current high < 2-candles-ago low (gap down)
        if candle_current['high'] < candle_two_before['low']:
            fvg_top = candle_two_before['low']
            fvg_bottom = candle_current['high']
            
            # Look for breakout: price closes above the FVG
            # (closes above the low of the middle candle n+1)
            for j in range(i + 1, len(candles)):
                breakout_candle = candles[j]
                
                # Check if price closes above the low of middle candle (breaking above FVG zone)
                if breakout_candle['close'] > candle_middle['low']:
                    # SHORT entry triggered
                    entry_price = breakout_candle['close']
                    sl_price = fvg_top  # SL above the FVG
                    risk = sl_price - entry_price
                    
                    if risk <= 0:
                        break  # Invalid trade setup
                    
                    # Check TP hit for each ratio
                    tp_results = {}
                    for ratio in rr_ratios:
                        tp_price = entry_price - (risk * ratio)
                        tp_hit = False
                        sl_hit_first = False
                        
                        # Check subsequent candles for TP or SL hit
                        for k in range(j + 1, len(candles)):
                            check_candle = candles[k]
                            
                            # Check if SL hit (price goes above SL)
                            if check_candle['high'] >= sl_price:
                                sl_hit_first = True
                                break
                            
                            # Check if TP hit (price goes below TP)
                            if check_candle['low'] <= tp_price:
                                tp_hit = True
                                break
                        
                        tp_results[ratio] = {
                            'hit': tp_hit,
                            'sl_hit_first': sl_hit_first
                        }
                    
                    trades.append({
                        'type': 'SHORT',
                        'fvg_type': 'Bearish',
                        'date': breakout_candle['date'],
                        'time': breakout_candle['time'],
                        'entry': entry_price,
                        'sl': sl_price,
                        'risk': risk,
                        'tp_results': tp_results
                    })
                    break  # Only take first breakout for this FVG
        
        # Bullish FVG: current low > 2-candles-ago high (gap up)
        elif candle_current['low'] > candle_two_before['high']:
            fvg_top = candle_current['low']
            fvg_bottom = candle_two_before['high']
            
            # Look for breakout: price closes below the FVG
            # (closes below the high of the middle candle n+1)
            for j in range(i + 1, len(candles)):
                breakout_candle = candles[j]
                
                # Check if price closes below the high of middle candle (breaking below FVG zone)
                if breakout_candle['close'] < candle_middle['high']:
                    # LONG entry triggered
                    entry_price = breakout_candle['close']
                    sl_price = fvg_bottom  # SL below the FVG
                    risk = entry_price - sl_price
                    
                    if risk <= 0:
                        break  # Invalid trade setup
                    
                    # Check TP hit for each ratio
                    tp_results = {}
                    for ratio in rr_ratios:
                        tp_price = entry_price + (risk * ratio)
                        tp_hit = False
                        sl_hit_first = False
                        
                        # Check subsequent candles for TP or SL hit
                        for k in range(j + 1, len(candles)):
                            check_candle = candles[k]
                            
                            # Check if SL hit (price goes below SL)
                            if check_candle['low'] <= sl_price:
                                sl_hit_first = True
                                break
                            
                            # Check if TP hit (price goes above TP)
                            if check_candle['high'] >= tp_price:
                                tp_hit = True
                                break
                        
                        tp_results[ratio] = {
                            'hit': tp_hit,
                            'sl_hit_first': sl_hit_first
                        }
                    
                    trades.append({
                        'type': 'LONG',
                        'fvg_type': 'Bullish',
                        'date': breakout_candle['date'],
                        'time': breakout_candle['time'],
                        'entry': entry_price,
                        'sl': sl_price,
                        'risk': risk,
                        'tp_results': tp_results
                    })
                    break  # Only take first breakout for this FVG
    
    return trades


def analyze_year(filepath, year):
    """Analyze a single year's CSV file for FVG breakout trades."""
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
    
    # Detect FVG breakouts for each day
    all_trades = []
    sorted_dates = sorted(grouped.keys(), key=lambda d: datetime.strptime(d, "%d/%m/%Y"))
    for date in sorted_dates:
        day_candles = grouped[date]
        trades_for_day = detect_fvg_with_breakout(day_candles)
        all_trades.extend(trades_for_day)
    
    return {
        'year': year,
        'trading_days': len(grouped),
        'trades': all_trades
    }


def main():
    """Main function to run FVG breakout backtest."""
    base_path = os.path.dirname(os.path.abspath(__file__))
    
    years = [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]
    rr_ratios = [1.0, 1.5, 2.0, 2.5, 3.0, 3.5]
    
    all_trades = []
    results_by_year = []
    
    print("=" * 80)
    print("FVG BREAKOUT STRATEGY BACKTEST")
    print("Time Window: 8:30 - 10:00")
    print("=" * 80)
    print("\nStrategy:")
    print("- SHORT when price closes above a Bearish FVG (SL above FVG)")
    print("- LONG when price closes below a Bullish FVG (SL below FVG)")
    print("=" * 80)
    
    for year in years:
        filepath = os.path.join(base_path, f"{year} 5m.csv")
        if os.path.exists(filepath):
            year_result = analyze_year(filepath, year)
            results_by_year.append(year_result)
            all_trades.extend(year_result['trades'])
        else:
            print(f"\nWarning: File not found - {filepath}")
    
    # Separate SHORT and LONG trades
    short_trades = [t for t in all_trades if t['type'] == 'SHORT']
    long_trades = [t for t in all_trades if t['type'] == 'LONG']
    
    print(f"\n{'=' * 100}")
    print("BACKTEST RESULTS SUMMARY")
    print("=" * 100)
    print(f"\nTotal trades: {len(all_trades)}")
    print(f"  SHORT trades (Bearish FVG breakout): {len(short_trades)}")
    print(f"  LONG trades (Bullish FVG breakout): {len(long_trades)}")
    
    # Calculate TP hit rates for each ratio
    print(f"\n{'=' * 100}")
    print("TP HIT PROBABILITY BY R:R RATIO")
    print("=" * 100)
    
    # Overall stats
    print(f"\n{'ALL TRADES':^100}")
    print("-" * 100)
    print(f"{'R:R Ratio':<15} {'TP Hit':<15} {'SL Hit':<15} {'Pending':<15} {'Win Rate':<15}")
    print("-" * 100)
    
    overall_stats = {}
    for ratio in rr_ratios:
        tp_hits = sum(1 for t in all_trades if t['tp_results'][ratio]['hit'])
        sl_hits = sum(1 for t in all_trades if t['tp_results'][ratio]['sl_hit_first'])
        pending = len(all_trades) - tp_hits - sl_hits
        win_rate = (tp_hits / len(all_trades) * 100) if len(all_trades) > 0 else 0
        overall_stats[ratio] = {'tp_hits': tp_hits, 'sl_hits': sl_hits, 'pending': pending, 'win_rate': win_rate}
        print(f"{ratio:<15.1f} {tp_hits:<15} {sl_hits:<15} {pending:<15} {win_rate:<15.1f}%")
    
    # SHORT trades stats
    print(f"\n{'SHORT TRADES (Bearish FVG Breakout)':^100}")
    print("-" * 100)
    print(f"{'R:R Ratio':<15} {'TP Hit':<15} {'SL Hit':<15} {'Pending':<15} {'Win Rate':<15}")
    print("-" * 100)
    
    short_stats = {}
    for ratio in rr_ratios:
        tp_hits = sum(1 for t in short_trades if t['tp_results'][ratio]['hit'])
        sl_hits = sum(1 for t in short_trades if t['tp_results'][ratio]['sl_hit_first'])
        pending = len(short_trades) - tp_hits - sl_hits
        win_rate = (tp_hits / len(short_trades) * 100) if len(short_trades) > 0 else 0
        short_stats[ratio] = {'tp_hits': tp_hits, 'sl_hits': sl_hits, 'pending': pending, 'win_rate': win_rate}
        print(f"{ratio:<15.1f} {tp_hits:<15} {sl_hits:<15} {pending:<15} {win_rate:<15.1f}%")
    
    # LONG trades stats
    print(f"\n{'LONG TRADES (Bullish FVG Breakout)':^100}")
    print("-" * 100)
    print(f"{'R:R Ratio':<15} {'TP Hit':<15} {'SL Hit':<15} {'Pending':<15} {'Win Rate':<15}")
    print("-" * 100)
    
    long_stats = {}
    for ratio in rr_ratios:
        tp_hits = sum(1 for t in long_trades if t['tp_results'][ratio]['hit'])
        sl_hits = sum(1 for t in long_trades if t['tp_results'][ratio]['sl_hit_first'])
        pending = len(long_trades) - tp_hits - sl_hits
        win_rate = (tp_hits / len(long_trades) * 100) if len(long_trades) > 0 else 0
        long_stats[ratio] = {'tp_hits': tp_hits, 'sl_hits': sl_hits, 'pending': pending, 'win_rate': win_rate}
        print(f"{ratio:<15.1f} {tp_hits:<15} {sl_hits:<15} {pending:<15} {win_rate:<15.1f}%")
    
    # Results by year
    print(f"\n{'=' * 100}")
    print("RESULTS BY YEAR")
    print("=" * 100)
    
    for year_result in results_by_year:
        year = year_result['year']
        year_trades = year_result['trades']
        year_short = [t for t in year_trades if t['type'] == 'SHORT']
        year_long = [t for t in year_trades if t['type'] == 'LONG']
        
        print(f"\n{year}: {len(year_trades)} trades ({len(year_short)} SHORT, {len(year_long)} LONG)")
        
        if len(year_trades) > 0:
            print(f"  {'R:R':<8} {'Win Rate':<12} {'SHORT Win%':<15} {'LONG Win%':<15}")
            print(f"  {'-' * 50}")
            for ratio in rr_ratios:
                total_win = sum(1 for t in year_trades if t['tp_results'][ratio]['hit'])
                total_rate = (total_win / len(year_trades) * 100) if year_trades else 0
                
                short_win = sum(1 for t in year_short if t['tp_results'][ratio]['hit'])
                short_rate = (short_win / len(year_short) * 100) if year_short else 0
                
                long_win = sum(1 for t in year_long if t['tp_results'][ratio]['hit'])
                long_rate = (long_win / len(year_long) * 100) if year_long else 0
                
                print(f"  {ratio:<8.1f} {total_rate:<12.1f}% {short_rate:<15.1f}% {long_rate:<15.1f}%")
    
    # Save results to file
    output_file = os.path.join(base_path, "fvg_backtest_results.txt")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("=" * 120 + "\n")
        f.write("FVG BREAKOUT STRATEGY BACKTEST RESULTS\n")
        f.write("Time Window: 8:30 - 10:00\n")
        f.write("=" * 120 + "\n\n")
        
        f.write("STRATEGY DESCRIPTION:\n")
        f.write("-" * 120 + "\n")
        f.write("SHORT Entry: When price closes above a Bearish FVG (above the low of candle n+1)\n")
        f.write("  - SL: Above the broken Bearish FVG (at fvg_top)\n")
        f.write("  - TP: Entry - (Risk * R:R ratio)\n\n")
        f.write("LONG Entry: When price closes below a Bullish FVG (below the high of candle n+1)\n")
        f.write("  - SL: Below the broken Bullish FVG (at fvg_bottom)\n")
        f.write("  - TP: Entry + (Risk * R:R ratio)\n")
        f.write("=" * 120 + "\n\n")
        
        f.write(f"TOTAL TRADES: {len(all_trades)}\n")
        f.write(f"  SHORT trades (Bearish FVG breakout): {len(short_trades)}\n")
        f.write(f"  LONG trades (Bullish FVG breakout): {len(long_trades)}\n\n")
        
        f.write("=" * 120 + "\n")
        f.write("TP HIT PROBABILITY BY R:R RATIO\n")
        f.write("=" * 120 + "\n\n")
        
        # Overall
        f.write("ALL TRADES\n")
        f.write("-" * 120 + "\n")
        f.write(f"{'R:R Ratio':<15} {'TP Hit':<15} {'SL Hit':<15} {'Pending':<15} {'Win Rate':<15}\n")
        f.write("-" * 120 + "\n")
        for ratio in rr_ratios:
            s = overall_stats[ratio]
            f.write(f"{ratio:<15.1f} {s['tp_hits']:<15} {s['sl_hits']:<15} {s['pending']:<15} {s['win_rate']:<15.1f}%\n")
        f.write("\n")
        
        # SHORT
        f.write("SHORT TRADES (Bearish FVG Breakout)\n")
        f.write("-" * 120 + "\n")
        f.write(f"{'R:R Ratio':<15} {'TP Hit':<15} {'SL Hit':<15} {'Pending':<15} {'Win Rate':<15}\n")
        f.write("-" * 120 + "\n")
        for ratio in rr_ratios:
            s = short_stats[ratio]
            f.write(f"{ratio:<15.1f} {s['tp_hits']:<15} {s['sl_hits']:<15} {s['pending']:<15} {s['win_rate']:<15.1f}%\n")
        f.write("\n")
        
        # LONG
        f.write("LONG TRADES (Bullish FVG Breakout)\n")
        f.write("-" * 120 + "\n")
        f.write(f"{'R:R Ratio':<15} {'TP Hit':<15} {'SL Hit':<15} {'Pending':<15} {'Win Rate':<15}\n")
        f.write("-" * 120 + "\n")
        for ratio in rr_ratios:
            s = long_stats[ratio]
            f.write(f"{ratio:<15.1f} {s['tp_hits']:<15} {s['sl_hits']:<15} {s['pending']:<15} {s['win_rate']:<15.1f}%\n")
        f.write("\n")
        
        # By year
        f.write("=" * 120 + "\n")
        f.write("RESULTS BY YEAR\n")
        f.write("=" * 120 + "\n\n")
        
        for year_result in results_by_year:
            year = year_result['year']
            year_trades = year_result['trades']
            year_short = [t for t in year_trades if t['type'] == 'SHORT']
            year_long = [t for t in year_trades if t['type'] == 'LONG']
            
            f.write(f"{year}: {len(year_trades)} trades ({len(year_short)} SHORT, {len(year_long)} LONG)\n")
            
            if len(year_trades) > 0:
                f.write(f"  {'R:R':<8} {'Win Rate':<12} {'SHORT Win%':<15} {'LONG Win%':<15}\n")
                f.write(f"  {'-' * 50}\n")
                for ratio in rr_ratios:
                    total_win = sum(1 for t in year_trades if t['tp_results'][ratio]['hit'])
                    total_rate = (total_win / len(year_trades) * 100) if year_trades else 0
                    
                    short_win = sum(1 for t in year_short if t['tp_results'][ratio]['hit'])
                    short_rate = (short_win / len(year_short) * 100) if year_short else 0
                    
                    long_win = sum(1 for t in year_long if t['tp_results'][ratio]['hit'])
                    long_rate = (long_win / len(year_long) * 100) if year_long else 0
                    
                    f.write(f"  {ratio:<8.1f} {total_rate:<12.1f}% {short_rate:<15.1f}% {long_rate:<15.1f}%\n")
            f.write("\n")
    
    print(f"\n{'=' * 80}")
    print(f"Results saved to: {output_file}")
    print("=" * 80)
    
    return all_trades


if __name__ == "__main__":
    main()

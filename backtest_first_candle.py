#!/usr/bin/env python3
"""
First Candle Strategy Backtest

This script backtests a strategy based on the first 5-minute candle at 8:30 NY time:

Strategy:
- If the 8:30 candle is impulsive (range > 25 points):
  - LONG if bullish candle (close > open)
  - SHORT if bearish candle (close < open)
- Entry = close of the 8:30 candle
- SL options:
  - 50% retracement: For LONG, SL = close - (range * 0.5). For SHORT, SL = close + (range * 0.5)
  - 100% retracement: For LONG, SL = low. For SHORT, SL = high
- TP at R:R ratios: 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0
"""

import csv
import os
from datetime import datetime
from collections import defaultdict


def parse_time(time_str):
    """Parse time string in HH:MM:SS format."""
    return datetime.strptime(time_str, "%H:%M:%S").time()


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


def group_by_date(data):
    """Group candles by date."""
    grouped = defaultdict(list)
    for candle in data:
        grouped[candle['date']].append(candle)
    return grouped


def analyze_first_candle_strategy(candles, min_range=25):
    """
    Analyze the first candle strategy for a single day.
    
    Args:
        candles: List of candles for the day
        min_range: Minimum range in points for the candle to be considered impulsive
    
    Returns:
        Trade result or None if no valid setup
    """
    rr_ratios = [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]
    sl_types = ['50%', '100%']
    
    # Find the 8:30 candle
    first_candle = None
    first_candle_idx = None
    for idx, candle in enumerate(candles):
        if candle['time'] == '08:30:00':
            first_candle = candle
            first_candle_idx = idx
            break
    
    if first_candle is None:
        return None
    
    # Calculate range
    candle_range = first_candle['high'] - first_candle['low']
    
    # Check if candle is impulsive (>25 points)
    if candle_range < min_range:
        return None
    
    # Determine direction
    is_bullish = first_candle['close'] > first_candle['open']
    trade_type = 'LONG' if is_bullish else 'SHORT'
    entry_price = first_candle['close']
    
    # Get subsequent candles for checking TP/SL
    subsequent_candles = candles[first_candle_idx + 1:]
    
    results = {
        'date': first_candle['date'],
        'type': trade_type,
        'entry': entry_price,
        'range': candle_range,
        'high': first_candle['high'],
        'low': first_candle['low'],
        'open': first_candle['open'],
        'close': first_candle['close'],
        'sl_results': {}
    }
    
    for sl_type in sl_types:
        # Calculate SL based on type
        if sl_type == '50%':
            if is_bullish:
                # LONG: SL at 50% retracement from close
                sl_price = entry_price - (candle_range * 0.5)
            else:
                # SHORT: SL at 50% retracement from close
                sl_price = entry_price + (candle_range * 0.5)
        else:  # 100%
            if is_bullish:
                # LONG: SL at low of candle
                sl_price = first_candle['low']
            else:
                # SHORT: SL at high of candle
                sl_price = first_candle['high']
        
        risk = abs(entry_price - sl_price)
        
        if risk <= 0:
            continue
        
        tp_results = {}
        for ratio in rr_ratios:
            if is_bullish:
                tp_price = entry_price + (risk * ratio)
            else:
                tp_price = entry_price - (risk * ratio)
            
            tp_hit = False
            sl_hit_first = False
            
            # Check subsequent candles
            for check_candle in subsequent_candles:
                if is_bullish:
                    # LONG: Check if SL hit (price goes below SL)
                    if check_candle['low'] <= sl_price:
                        sl_hit_first = True
                        break
                    # Check if TP hit (price goes above TP)
                    if check_candle['high'] >= tp_price:
                        tp_hit = True
                        break
                else:
                    # SHORT: Check if SL hit (price goes above SL)
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
        
        results['sl_results'][sl_type] = {
            'sl_price': sl_price,
            'risk': risk,
            'tp_results': tp_results
        }
    
    return results


def analyze_year(filepath, year, min_range=25):
    """Analyze a single year's CSV file."""
    print(f"\nAnalyzing {year}...")
    
    # Load data
    data = load_csv_data(filepath)
    print(f"  Total candles loaded: {len(data)}")
    
    # Group by date
    grouped = group_by_date(data)
    print(f"  Number of trading days: {len(grouped)}")
    
    # Analyze each day
    trades = []
    sorted_dates = sorted(grouped.keys(), key=lambda d: datetime.strptime(d, "%d/%m/%Y"))
    
    for date in sorted_dates:
        day_candles = grouped[date]
        result = analyze_first_candle_strategy(day_candles, min_range)
        if result:
            trades.append(result)
    
    print(f"  Impulsive 8:30 candles (>{min_range} pts): {len(trades)}")
    
    return {
        'year': year,
        'trading_days': len(grouped),
        'trades': trades
    }


def main():
    """Main function to run first candle strategy backtest."""
    base_path = os.path.dirname(os.path.abspath(__file__))
    
    years = [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]
    rr_ratios = [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]
    sl_types = ['50%', '100%']
    min_range = 25
    
    all_trades = []
    results_by_year = []
    
    print("=" * 100)
    print("FIRST CANDLE STRATEGY BACKTEST")
    print("=" * 100)
    print(f"\nStrategy:")
    print(f"- Entry: Close of 8:30 candle if range > {min_range} points")
    print(f"- LONG if bullish (close > open), SHORT if bearish (close < open)")
    print(f"- SL at 50% retracement or 100% retracement (candle extreme)")
    print(f"- TP at R:R ratios: {', '.join(str(r) for r in rr_ratios)}")
    print("=" * 100)
    
    for year in years:
        filepath = os.path.join(base_path, f"{year} 5m.csv")
        if os.path.exists(filepath):
            year_result = analyze_year(filepath, year, min_range)
            results_by_year.append(year_result)
            all_trades.extend(year_result['trades'])
        else:
            print(f"\nWarning: File not found - {filepath}")
    
    # Separate LONG and SHORT trades
    long_trades = [t for t in all_trades if t['type'] == 'LONG']
    short_trades = [t for t in all_trades if t['type'] == 'SHORT']
    
    print(f"\n{'=' * 100}")
    print("BACKTEST RESULTS SUMMARY")
    print("=" * 100)
    print(f"\nTotal impulsive 8:30 candles (>{min_range} pts): {len(all_trades)}")
    print(f"  LONG (Bullish candles): {len(long_trades)}")
    print(f"  SHORT (Bearish candles): {len(short_trades)}")
    
    # Calculate stats for each SL type
    for sl_type in sl_types:
        print(f"\n{'=' * 100}")
        print(f"RESULTS WITH SL AT {sl_type} RETRACEMENT")
        print("=" * 100)
        
        # Filter trades that have this SL type
        valid_trades = [t for t in all_trades if sl_type in t['sl_results']]
        valid_long = [t for t in long_trades if sl_type in t['sl_results']]
        valid_short = [t for t in short_trades if sl_type in t['sl_results']]
        
        # Overall stats
        print(f"\n{'ALL TRADES':^100}")
        print("-" * 100)
        print(f"{'R:R Ratio':<12} {'TP Hit':<12} {'SL Hit':<12} {'Pending':<12} {'Win Rate':<12}")
        print("-" * 100)
        
        overall_stats = {}
        for ratio in rr_ratios:
            tp_hits = sum(1 for t in valid_trades if t['sl_results'][sl_type]['tp_results'][ratio]['hit'])
            sl_hits = sum(1 for t in valid_trades if t['sl_results'][sl_type]['tp_results'][ratio]['sl_hit_first'])
            pending = len(valid_trades) - tp_hits - sl_hits
            win_rate = (tp_hits / len(valid_trades) * 100) if len(valid_trades) > 0 else 0
            overall_stats[ratio] = {'tp_hits': tp_hits, 'sl_hits': sl_hits, 'pending': pending, 'win_rate': win_rate}
            print(f"{ratio:<12.1f} {tp_hits:<12} {sl_hits:<12} {pending:<12} {win_rate:<12.1f}%")
        
        # LONG stats
        print(f"\n{'LONG TRADES (Bullish 8:30 Candle)':^100}")
        print("-" * 100)
        print(f"{'R:R Ratio':<12} {'TP Hit':<12} {'SL Hit':<12} {'Pending':<12} {'Win Rate':<12}")
        print("-" * 100)
        
        long_stats = {}
        for ratio in rr_ratios:
            tp_hits = sum(1 for t in valid_long if t['sl_results'][sl_type]['tp_results'][ratio]['hit'])
            sl_hits = sum(1 for t in valid_long if t['sl_results'][sl_type]['tp_results'][ratio]['sl_hit_first'])
            pending = len(valid_long) - tp_hits - sl_hits
            win_rate = (tp_hits / len(valid_long) * 100) if len(valid_long) > 0 else 0
            long_stats[ratio] = {'tp_hits': tp_hits, 'sl_hits': sl_hits, 'pending': pending, 'win_rate': win_rate}
            print(f"{ratio:<12.1f} {tp_hits:<12} {sl_hits:<12} {pending:<12} {win_rate:<12.1f}%")
        
        # SHORT stats
        print(f"\n{'SHORT TRADES (Bearish 8:30 Candle)':^100}")
        print("-" * 100)
        print(f"{'R:R Ratio':<12} {'TP Hit':<12} {'SL Hit':<12} {'Pending':<12} {'Win Rate':<12}")
        print("-" * 100)
        
        short_stats = {}
        for ratio in rr_ratios:
            tp_hits = sum(1 for t in valid_short if t['sl_results'][sl_type]['tp_results'][ratio]['hit'])
            sl_hits = sum(1 for t in valid_short if t['sl_results'][sl_type]['tp_results'][ratio]['sl_hit_first'])
            pending = len(valid_short) - tp_hits - sl_hits
            win_rate = (tp_hits / len(valid_short) * 100) if len(valid_short) > 0 else 0
            short_stats[ratio] = {'tp_hits': tp_hits, 'sl_hits': sl_hits, 'pending': pending, 'win_rate': win_rate}
            print(f"{ratio:<12.1f} {tp_hits:<12} {sl_hits:<12} {pending:<12} {win_rate:<12.1f}%")
    
    # Save results to file
    output_file = os.path.join(base_path, "first_candle_backtest_results.txt")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("=" * 120 + "\n")
        f.write("FIRST CANDLE STRATEGY BACKTEST RESULTS\n")
        f.write("=" * 120 + "\n\n")
        
        f.write("STRATEGY DESCRIPTION:\n")
        f.write("-" * 120 + "\n")
        f.write(f"- Entry: Close of 8:30 candle if range > {min_range} points\n")
        f.write("- LONG if bullish (close > open), SHORT if bearish (close < open)\n")
        f.write("- SL at 50% retracement: SL = entry - (range * 0.5) for LONG, entry + (range * 0.5) for SHORT\n")
        f.write("- SL at 100% retracement: SL = low for LONG, SL = high for SHORT\n")
        f.write(f"- TP at R:R ratios: {', '.join(str(r) for r in rr_ratios)}\n")
        f.write("=" * 120 + "\n\n")
        
        f.write(f"TOTAL IMPULSIVE 8:30 CANDLES (>{min_range} pts): {len(all_trades)}\n")
        f.write(f"  LONG (Bullish candles): {len(long_trades)}\n")
        f.write(f"  SHORT (Bearish candles): {len(short_trades)}\n\n")
        
        for sl_type in sl_types:
            f.write("=" * 120 + "\n")
            f.write(f"RESULTS WITH SL AT {sl_type} RETRACEMENT\n")
            f.write("=" * 120 + "\n\n")
            
            valid_trades = [t for t in all_trades if sl_type in t['sl_results']]
            valid_long = [t for t in long_trades if sl_type in t['sl_results']]
            valid_short = [t for t in short_trades if sl_type in t['sl_results']]
            
            # All trades
            f.write("ALL TRADES\n")
            f.write("-" * 120 + "\n")
            f.write(f"{'R:R Ratio':<12} {'TP Hit':<12} {'SL Hit':<12} {'Pending':<12} {'Win Rate':<12}\n")
            f.write("-" * 120 + "\n")
            for ratio in rr_ratios:
                tp_hits = sum(1 for t in valid_trades if t['sl_results'][sl_type]['tp_results'][ratio]['hit'])
                sl_hits = sum(1 for t in valid_trades if t['sl_results'][sl_type]['tp_results'][ratio]['sl_hit_first'])
                pending = len(valid_trades) - tp_hits - sl_hits
                win_rate = (tp_hits / len(valid_trades) * 100) if len(valid_trades) > 0 else 0
                f.write(f"{ratio:<12.1f} {tp_hits:<12} {sl_hits:<12} {pending:<12} {win_rate:<12.1f}%\n")
            f.write("\n")
            
            # LONG trades
            f.write("LONG TRADES (Bullish 8:30 Candle)\n")
            f.write("-" * 120 + "\n")
            f.write(f"{'R:R Ratio':<12} {'TP Hit':<12} {'SL Hit':<12} {'Pending':<12} {'Win Rate':<12}\n")
            f.write("-" * 120 + "\n")
            for ratio in rr_ratios:
                tp_hits = sum(1 for t in valid_long if t['sl_results'][sl_type]['tp_results'][ratio]['hit'])
                sl_hits = sum(1 for t in valid_long if t['sl_results'][sl_type]['tp_results'][ratio]['sl_hit_first'])
                pending = len(valid_long) - tp_hits - sl_hits
                win_rate = (tp_hits / len(valid_long) * 100) if len(valid_long) > 0 else 0
                f.write(f"{ratio:<12.1f} {tp_hits:<12} {sl_hits:<12} {pending:<12} {win_rate:<12.1f}%\n")
            f.write("\n")
            
            # SHORT trades
            f.write("SHORT TRADES (Bearish 8:30 Candle)\n")
            f.write("-" * 120 + "\n")
            f.write(f"{'R:R Ratio':<12} {'TP Hit':<12} {'SL Hit':<12} {'Pending':<12} {'Win Rate':<12}\n")
            f.write("-" * 120 + "\n")
            for ratio in rr_ratios:
                tp_hits = sum(1 for t in valid_short if t['sl_results'][sl_type]['tp_results'][ratio]['hit'])
                sl_hits = sum(1 for t in valid_short if t['sl_results'][sl_type]['tp_results'][ratio]['sl_hit_first'])
                pending = len(valid_short) - tp_hits - sl_hits
                win_rate = (tp_hits / len(valid_short) * 100) if len(valid_short) > 0 else 0
                f.write(f"{ratio:<12.1f} {tp_hits:<12} {sl_hits:<12} {pending:<12} {win_rate:<12.1f}%\n")
            f.write("\n")
        
        # Results by year
        f.write("=" * 120 + "\n")
        f.write("RESULTS BY YEAR\n")
        f.write("=" * 120 + "\n\n")
        
        for year_result in results_by_year:
            year = year_result['year']
            year_trades = year_result['trades']
            year_long = [t for t in year_trades if t['type'] == 'LONG']
            year_short = [t for t in year_trades if t['type'] == 'SHORT']
            
            f.write(f"{year}: {len(year_trades)} impulsive candles ({len(year_long)} LONG, {len(year_short)} SHORT)\n")
            
            if len(year_trades) > 0:
                for sl_type in sl_types:
                    valid_year = [t for t in year_trades if sl_type in t['sl_results']]
                    f.write(f"  SL {sl_type}:\n")
                    f.write(f"    {'R:R':<8} {'Win Rate':<12}\n")
                    f.write(f"    {'-' * 20}\n")
                    for ratio in [1.0, 2.0, 3.0, 5.0]:
                        if valid_year:
                            tp_hits = sum(1 for t in valid_year if t['sl_results'][sl_type]['tp_results'][ratio]['hit'])
                            win_rate = (tp_hits / len(valid_year) * 100)
                            f.write(f"    {ratio:<8.1f} {win_rate:<12.1f}%\n")
            f.write("\n")
    
    print(f"\n{'=' * 100}")
    print(f"Results saved to: {output_file}")
    print("=" * 100)
    
    return all_trades


if __name__ == "__main__":
    main()

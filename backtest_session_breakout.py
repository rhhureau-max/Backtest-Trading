#!/usr/bin/env python3
"""
Session Breakout Strategy Backtest

This script backtests a strategy based on breakout of the pre-market session (4:00-8:30) range:

Strategy:
- Calculate the high and low of the 4:00-8:30 session
- If the 8:30 candle closes below the session low: SHORT entry (bearish breakout)
- If the 8:30 candle closes above the session high: LONG entry (bullish breakout)
- Entry = close of the 8:30 candle
- SL options:
  - 50% retracement: For SHORT, SL = close + (range * 0.5). For LONG, SL = close - (range * 0.5)
  - 100% retracement: For SHORT, SL = high of 8:30 candle. For LONG, SL = low of 8:30 candle
- TP at R:R ratios: 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0
"""

import csv
import os
from datetime import datetime
from collections import defaultdict


def parse_time(time_str):
    """Parse time string in HH:MM:SS format."""
    return datetime.strptime(time_str, "%H:%M:%S").time()


def is_time_in_range(time_str, start_time, end_time):
    """Check if time is within range."""
    time_obj = parse_time(time_str)
    start = parse_time(start_time)
    end = parse_time(end_time)
    return start <= time_obj < end


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


def analyze_session_breakout(candles):
    """
    Analyze session breakout strategy for a single day.
    
    Args:
        candles: List of candles for the day
    
    Returns:
        Trade result or None if no valid setup
    """
    rr_ratios = [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]
    sl_types = ['50%', '100%']
    
    # Find pre-market candles (4:00 to 8:25) and the 8:30 candle
    pre_market_candles = []
    candle_830 = None
    candle_830_idx = None
    
    for idx, candle in enumerate(candles):
        # Pre-market session: 4:00 to 8:25 (before 8:30)
        if is_time_in_range(candle['time'], '04:00:00', '08:30:00'):
            pre_market_candles.append(candle)
        elif candle['time'] == '08:30:00':
            candle_830 = candle
            candle_830_idx = idx
    
    # Need pre-market data and 8:30 candle
    if not pre_market_candles or candle_830 is None:
        return None
    
    # Calculate session high and low (4:00 to 8:25)
    session_high = max(c['high'] for c in pre_market_candles)
    session_low = min(c['low'] for c in pre_market_candles)
    
    # Check for breakout
    close_830 = candle_830['close']
    
    # Determine trade direction
    trade_type = None
    if close_830 < session_low:
        trade_type = 'SHORT'  # Price closed below session low - bearish breakout
    elif close_830 > session_high:
        trade_type = 'LONG'   # Price closed above session high - bullish breakout
    else:
        return None  # No breakout
    
    entry_price = close_830
    candle_range = candle_830['high'] - candle_830['low']
    
    if candle_range <= 0:
        return None
    
    # Get subsequent candles for checking TP/SL
    subsequent_candles = candles[candle_830_idx + 1:]
    
    results = {
        'date': candle_830['date'],
        'type': trade_type,
        'entry': entry_price,
        'candle_range': candle_range,
        'candle_high': candle_830['high'],
        'candle_low': candle_830['low'],
        'session_high': session_high,
        'session_low': session_low,
        'breakout_distance': abs(close_830 - session_low) if trade_type == 'SHORT' else abs(close_830 - session_high),
        'sl_results': {}
    }
    
    for sl_type in sl_types:
        # Calculate SL based on type
        if sl_type == '50%':
            if trade_type == 'SHORT':
                # SHORT: SL at 50% retracement from close (above entry)
                sl_price = entry_price + (candle_range * 0.5)
            else:
                # LONG: SL at 50% retracement from close (below entry)
                sl_price = entry_price - (candle_range * 0.5)
        else:  # 100%
            if trade_type == 'SHORT':
                # SHORT: SL at high of 8:30 candle
                sl_price = candle_830['high']
            else:
                # LONG: SL at low of 8:30 candle
                sl_price = candle_830['low']
        
        risk = abs(entry_price - sl_price)
        
        if risk <= 0:
            continue
        
        tp_results = {}
        for ratio in rr_ratios:
            if trade_type == 'SHORT':
                tp_price = entry_price - (risk * ratio)
            else:
                tp_price = entry_price + (risk * ratio)
            
            tp_hit = False
            sl_hit_first = False
            
            # Check subsequent candles
            for check_candle in subsequent_candles:
                if trade_type == 'SHORT':
                    # SHORT: Check if SL hit (price goes above SL)
                    if check_candle['high'] >= sl_price:
                        sl_hit_first = True
                        break
                    # Check if TP hit (price goes below TP)
                    if check_candle['low'] <= tp_price:
                        tp_hit = True
                        break
                else:
                    # LONG: Check if SL hit (price goes below SL)
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
        
        results['sl_results'][sl_type] = {
            'sl_price': sl_price,
            'risk': risk,
            'tp_results': tp_results
        }
    
    return results


def analyze_year(filepath, year):
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
        result = analyze_session_breakout(day_candles)
        if result:
            trades.append(result)
    
    short_count = sum(1 for t in trades if t['type'] == 'SHORT')
    long_count = sum(1 for t in trades if t['type'] == 'LONG')
    print(f"  Session breakouts at 8:30: {len(trades)} ({short_count} SHORT, {long_count} LONG)")
    
    return {
        'year': year,
        'trading_days': len(grouped),
        'trades': trades
    }


def main():
    """Main function to run session breakout strategy backtest."""
    base_path = os.path.dirname(os.path.abspath(__file__))
    
    years = [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]
    rr_ratios = [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]
    sl_types = ['50%', '100%']
    
    all_trades = []
    results_by_year = []
    
    print("=" * 100)
    print("SESSION BREAKOUT STRATEGY BACKTEST")
    print("=" * 100)
    print(f"\nStrategy:")
    print(f"- Calculate high/low of 4:00-8:30 session")
    print(f"- If 8:30 candle closes BELOW session low: SHORT entry")
    print(f"- If 8:30 candle closes ABOVE session high: LONG entry")
    print(f"- SL at 50% retracement or 100% retracement (candle extreme)")
    print(f"- TP at R:R ratios: {', '.join(str(r) for r in rr_ratios)}")
    print("=" * 100)
    
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
    print(f"\nTotal session breakouts at 8:30: {len(all_trades)}")
    print(f"  SHORT (close below session low): {len(short_trades)}")
    print(f"  LONG (close above session high): {len(long_trades)}")
    
    # Calculate stats for each SL type
    for sl_type in sl_types:
        print(f"\n{'=' * 100}")
        print(f"RESULTS WITH SL AT {sl_type} RETRACEMENT")
        print("=" * 100)
        
        # Filter trades that have this SL type
        valid_trades = [t for t in all_trades if sl_type in t['sl_results']]
        valid_short = [t for t in short_trades if sl_type in t['sl_results']]
        valid_long = [t for t in long_trades if sl_type in t['sl_results']]
        
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
        
        # SHORT stats
        print(f"\n{'SHORT TRADES (Close Below Session Low)':^100}")
        print("-" * 100)
        print(f"{'R:R Ratio':<12} {'TP Hit':<12} {'SL Hit':<12} {'Pending':<12} {'Win Rate':<12}")
        print("-" * 100)
        
        short_stats = {}
        for ratio in rr_ratios:
            if valid_short:
                tp_hits = sum(1 for t in valid_short if t['sl_results'][sl_type]['tp_results'][ratio]['hit'])
                sl_hits = sum(1 for t in valid_short if t['sl_results'][sl_type]['tp_results'][ratio]['sl_hit_first'])
                pending = len(valid_short) - tp_hits - sl_hits
                win_rate = (tp_hits / len(valid_short) * 100)
            else:
                tp_hits, sl_hits, pending, win_rate = 0, 0, 0, 0
            short_stats[ratio] = {'tp_hits': tp_hits, 'sl_hits': sl_hits, 'pending': pending, 'win_rate': win_rate}
            print(f"{ratio:<12.1f} {tp_hits:<12} {sl_hits:<12} {pending:<12} {win_rate:<12.1f}%")
        
        # LONG stats
        print(f"\n{'LONG TRADES (Close Above Session High)':^100}")
        print("-" * 100)
        print(f"{'R:R Ratio':<12} {'TP Hit':<12} {'SL Hit':<12} {'Pending':<12} {'Win Rate':<12}")
        print("-" * 100)
        
        long_stats = {}
        for ratio in rr_ratios:
            if valid_long:
                tp_hits = sum(1 for t in valid_long if t['sl_results'][sl_type]['tp_results'][ratio]['hit'])
                sl_hits = sum(1 for t in valid_long if t['sl_results'][sl_type]['tp_results'][ratio]['sl_hit_first'])
                pending = len(valid_long) - tp_hits - sl_hits
                win_rate = (tp_hits / len(valid_long) * 100)
            else:
                tp_hits, sl_hits, pending, win_rate = 0, 0, 0, 0
            long_stats[ratio] = {'tp_hits': tp_hits, 'sl_hits': sl_hits, 'pending': pending, 'win_rate': win_rate}
            print(f"{ratio:<12.1f} {tp_hits:<12} {sl_hits:<12} {pending:<12} {win_rate:<12.1f}%")
    
    # Save results to file
    output_file = os.path.join(base_path, "session_breakout_results.txt")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("=" * 120 + "\n")
        f.write("SESSION BREAKOUT STRATEGY BACKTEST RESULTS\n")
        f.write("=" * 120 + "\n\n")
        
        f.write("STRATEGY DESCRIPTION:\n")
        f.write("-" * 120 + "\n")
        f.write("- Calculate high/low of 4:00-8:30 pre-market session\n")
        f.write("- If 8:30 candle closes BELOW session low: SHORT entry (bearish breakout)\n")
        f.write("- If 8:30 candle closes ABOVE session high: LONG entry (bullish breakout)\n")
        f.write("- SL at 50% retracement: SL = entry +/- (candle_range * 0.5)\n")
        f.write("- SL at 100% retracement: SL = candle high (SHORT) or candle low (LONG)\n")
        f.write(f"- TP at R:R ratios: {', '.join(str(r) for r in rr_ratios)}\n")
        f.write("=" * 120 + "\n\n")
        
        f.write(f"TOTAL SESSION BREAKOUTS AT 8:30: {len(all_trades)}\n")
        f.write(f"  SHORT (close below session low): {len(short_trades)}\n")
        f.write(f"  LONG (close above session high): {len(long_trades)}\n\n")
        
        for sl_type in sl_types:
            f.write("=" * 120 + "\n")
            f.write(f"RESULTS WITH SL AT {sl_type} RETRACEMENT\n")
            f.write("=" * 120 + "\n\n")
            
            valid_trades = [t for t in all_trades if sl_type in t['sl_results']]
            valid_short = [t for t in short_trades if sl_type in t['sl_results']]
            valid_long = [t for t in long_trades if sl_type in t['sl_results']]
            
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
            
            # SHORT trades
            f.write("SHORT TRADES (Close Below Session Low)\n")
            f.write("-" * 120 + "\n")
            f.write(f"{'R:R Ratio':<12} {'TP Hit':<12} {'SL Hit':<12} {'Pending':<12} {'Win Rate':<12}\n")
            f.write("-" * 120 + "\n")
            for ratio in rr_ratios:
                if valid_short:
                    tp_hits = sum(1 for t in valid_short if t['sl_results'][sl_type]['tp_results'][ratio]['hit'])
                    sl_hits = sum(1 for t in valid_short if t['sl_results'][sl_type]['tp_results'][ratio]['sl_hit_first'])
                    pending = len(valid_short) - tp_hits - sl_hits
                    win_rate = (tp_hits / len(valid_short) * 100)
                else:
                    tp_hits, sl_hits, pending, win_rate = 0, 0, 0, 0
                f.write(f"{ratio:<12.1f} {tp_hits:<12} {sl_hits:<12} {pending:<12} {win_rate:<12.1f}%\n")
            f.write("\n")
            
            # LONG trades
            f.write("LONG TRADES (Close Above Session High)\n")
            f.write("-" * 120 + "\n")
            f.write(f"{'R:R Ratio':<12} {'TP Hit':<12} {'SL Hit':<12} {'Pending':<12} {'Win Rate':<12}\n")
            f.write("-" * 120 + "\n")
            for ratio in rr_ratios:
                if valid_long:
                    tp_hits = sum(1 for t in valid_long if t['sl_results'][sl_type]['tp_results'][ratio]['hit'])
                    sl_hits = sum(1 for t in valid_long if t['sl_results'][sl_type]['tp_results'][ratio]['sl_hit_first'])
                    pending = len(valid_long) - tp_hits - sl_hits
                    win_rate = (tp_hits / len(valid_long) * 100)
                else:
                    tp_hits, sl_hits, pending, win_rate = 0, 0, 0, 0
                f.write(f"{ratio:<12.1f} {tp_hits:<12} {sl_hits:<12} {pending:<12} {win_rate:<12.1f}%\n")
            f.write("\n")
        
        # Results by year
        f.write("=" * 120 + "\n")
        f.write("RESULTS BY YEAR\n")
        f.write("=" * 120 + "\n\n")
        
        for year_result in results_by_year:
            year = year_result['year']
            year_trades = year_result['trades']
            year_short = [t for t in year_trades if t['type'] == 'SHORT']
            year_long = [t for t in year_trades if t['type'] == 'LONG']
            
            f.write(f"{year}: {len(year_trades)} breakouts ({len(year_short)} SHORT, {len(year_long)} LONG)\n")
            
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

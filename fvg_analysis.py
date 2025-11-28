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
from typing import NamedTuple, Optional

# Constants for backtest configuration
RR_VALUES = [1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]
SL_PERCENTAGES = [0.5, 0.75, 1.0]
WICK_SL_OFFSET_POINTS = 1  # Offset in points for wick-based SL strategy


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


class FVGWithContext(NamedTuple):
    """Represents a FVG with additional context for backtesting."""
    fvg: FVG
    candle_0845_open: float
    candle_0845_close: float
    candle_0900_open: float


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


def find_fvgs_with_context(data: dict) -> list:
    """
    Find FVGs at 08:30 candles with additional context for backtesting.
    
    Returns FVGWithContext objects that include:
    - The FVG itself
    - Open/Close of candle n+1 (08:45) for SL calculation
    - Open of candle n+2 (09:00) for entry
    """
    fvgs_with_context = []
    
    # Get all unique dates
    dates = sorted(set(date for date, time in data.keys()))
    
    for date in dates:
        # Get the four candles needed
        candle_0815 = data.get((date, '08:15:00'))
        candle_0830 = data.get((date, '08:30:00'))
        candle_0845 = data.get((date, '08:45:00'))
        candle_0900 = data.get((date, '09:00:00'))
        
        # Skip if any candle is missing
        if not all([candle_0815, candle_0830, candle_0845, candle_0900]):
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
            fvg_ctx = FVGWithContext(
                fvg=fvg,
                candle_0845_open=candle_0845.open,
                candle_0845_close=candle_0845.close,
                candle_0900_open=candle_0900.open
            )
            fvgs_with_context.append(fvg_ctx)
        
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
            fvg_ctx = FVGWithContext(
                fvg=fvg,
                candle_0845_open=candle_0845.open,
                candle_0845_close=candle_0845.close,
                candle_0900_open=candle_0900.open
            )
            fvgs_with_context.append(fvg_ctx)
    
    return fvgs_with_context


def get_candles_after_time(data: dict, date: str, start_time: str) -> list:
    """
    Get all candles for a specific date after a given time.
    Returns list of candles sorted by time.
    """
    candles = []
    for (candle_date, candle_time), candle in data.items():
        if candle_date == date and candle_time > start_time:
            candles.append(candle)
    return sorted(candles, key=lambda c: c.time)


def determine_exit_on_same_candle(candle: Candle, sl: float, tp: float, is_long: bool) -> str:
    """
    Determine which level was hit first when both SL and TP are breached on the same candle.
    
    Uses candle open price to infer likely direction:
    - If open is already beyond SL or TP, that level was hit first
    - Otherwise, we compare distances from open to estimate which was reached first
    
    Note: This is an approximation since we cannot know the exact intra-candle price
    movement. The assumption is that price is more likely to hit the closer level first
    when starting from the candle open. This may not always reflect actual market 
    execution and should be considered when interpreting backtest results.
    
    For LONG: SL is below entry, TP is above entry
    For SHORT: SL is above entry, TP is below entry
    
    Args:
        candle: The candlestick that hit both levels
        sl: Stop loss price level
        tp: Take profit price level
        is_long: True for LONG position, False for SHORT
        
    Returns:
        'win' if TP likely hit first, 'loss' if SL likely hit first
    """
    if is_long:
        # LONG: SL hit via Low, TP hit via High
        if candle.open <= sl:
            # Opened at or below SL, so SL hit first
            return 'loss'
        elif candle.open >= tp:
            # Opened at or above TP, so TP hit first
            return 'win'
        else:
            # Open is between SL and TP
            # The level that is closer to the open was likely hit first
            abs_dist_to_sl = candle.open - sl  # distance down to SL
            abs_dist_to_tp = tp - candle.open  # distance up to TP
            if abs_dist_to_sl <= abs_dist_to_tp:
                # SL is closer, was likely hit first
                return 'loss'
            else:
                # TP is closer, was likely hit first
                return 'win'
    else:
        # SHORT: SL hit via High, TP hit via Low
        if candle.open >= sl:
            # Opened at or above SL, so SL hit first
            return 'loss'
        elif candle.open <= tp:
            # Opened at or below TP, so TP hit first
            return 'win'
        else:
            # Open is between SL and TP
            # The level that is closer to the open was likely hit first
            abs_dist_to_sl = sl - candle.open  # distance up to SL
            abs_dist_to_tp = candle.open - tp  # distance down to TP
            if abs_dist_to_sl <= abs_dist_to_tp:
                # SL is closer, was likely hit first
                return 'loss'
            else:
                # TP is closer, was likely hit first
                return 'win'


def simulate_trade(fvg_ctx: FVGWithContext, data: dict, sl_pct: float, rr: float) -> Optional[str]:
    """
    Simulate a trade based on FVG and return the result.
    
    Args:
        fvg_ctx: FVG with context for entry/SL calculation
        data: Full dataset with keys as (date, time) tuples and values as Candle objects.
              Used to check subsequent candles for SL/TP hits.
        sl_pct: Stop loss as a fraction of the candle body (0.5 = 50%, 0.75 = 75%, 1.0 = 100%)
        rr: Risk-reward ratio (e.g., 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5)
        
    Returns:
        'win' if TP hit first, 'loss' if SL hit first, None if no exit found
    """
    fvg = fvg_ctx.fvg
    date = fvg.date
    
    # Calculate body of candle n+1 (08:45)
    body = abs(fvg_ctx.candle_0845_close - fvg_ctx.candle_0845_open)
    
    # Entry at open of 09:00
    entry = fvg_ctx.candle_0900_open
    
    # Calculate SL distance
    sl_distance = body * sl_pct
    
    is_long = fvg.fvg_type == 'bullish'
    
    if is_long:
        # LONG position
        sl = entry - sl_distance
        tp = entry + (sl_distance * rr)
    else:
        # SHORT position
        sl = entry + sl_distance
        tp = entry - (sl_distance * rr)
    
    # Get candles after 09:00 (starting from 09:15)
    subsequent_candles = get_candles_after_time(data, date, '09:00:00')
    
    for candle in subsequent_candles:
        if is_long:
            # LONG: TP hit if High >= TP, SL hit if Low <= SL
            tp_hit = candle.high >= tp
            sl_hit = candle.low <= sl
        else:
            # SHORT: TP hit if Low <= TP, SL hit if High >= SL
            tp_hit = candle.low <= tp
            sl_hit = candle.high >= sl
        
        if tp_hit and sl_hit:
            # Both hit on same candle - determine which first
            return determine_exit_on_same_candle(candle, sl, tp, is_long)
        elif tp_hit:
            return 'win'
        elif sl_hit:
            return 'loss'
    
    # No exit found within the day
    return None


def simulate_trade_wick_sl(fvg_ctx: FVGWithContext, data: dict, rr: float) -> Optional[str]:
    """
    Simulate a trade based on FVG using wick-based SL strategy.
    
    SL is based on the wick of candle n (08:30):
    - LONG: SL = Low of 08:30 candle - 1 point
    - SHORT: SL = High of 08:30 candle + 1 point
    
    Args:
        fvg_ctx: FVG with context for entry/SL calculation
        data: Full dataset with keys as (date, time) tuples and values as Candle objects.
              Used to check subsequent candles for SL/TP hits.
        rr: Risk-reward ratio (e.g., 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5)
        
    Returns:
        'win' if TP hit first, 'loss' if SL hit first, None if no exit found
    """
    fvg = fvg_ctx.fvg
    date = fvg.date
    
    # Entry at open of 09:00
    entry = fvg_ctx.candle_0900_open
    
    is_long = fvg.fvg_type == 'bullish'
    
    if is_long:
        # LONG position: SL = Low of 08:30 candle - offset
        sl = fvg.candle_n_low - WICK_SL_OFFSET_POINTS
        sl_distance = entry - sl
        # Skip trade if SL distance is invalid (entry already below SL)
        if sl_distance <= 0:
            return None
        tp = entry + (sl_distance * rr)
    else:
        # SHORT position: SL = High of 08:30 candle + offset
        sl = fvg.candle_n_high + WICK_SL_OFFSET_POINTS
        sl_distance = sl - entry
        # Skip trade if SL distance is invalid (entry already above SL)
        if sl_distance <= 0:
            return None
        tp = entry - (sl_distance * rr)
    
    # Get candles after 09:00 (starting from 09:15)
    subsequent_candles = get_candles_after_time(data, date, '09:00:00')
    
    for candle in subsequent_candles:
        if is_long:
            # LONG: TP hit if High >= TP, SL hit if Low <= SL
            tp_hit = candle.high >= tp
            sl_hit = candle.low <= sl
        else:
            # SHORT: TP hit if Low <= TP, SL hit if High >= SL
            tp_hit = candle.low <= tp
            sl_hit = candle.high >= sl
        
        if tp_hit and sl_hit:
            # Both hit on same candle - determine which first
            return determine_exit_on_same_candle(candle, sl, tp, is_long)
        elif tp_hit:
            return 'win'
        elif sl_hit:
            return 'loss'
    
    # No exit found within the day
    return None


def run_backtest(all_data: dict, fvgs_with_context: list) -> dict:
    """
    Run backtest for all FVGs with different SL% and RR combinations.
    
    Args:
        all_data: Dictionary with keys as (date, time) tuples and values as Candle objects.
                  Contains all candle data needed to simulate trades.
        fvgs_with_context: List of FVGWithContext objects containing FVGs with entry context.
    
    Returns:
        Dictionary with backtest results where:
        - Keys are tuples (sl_pct, rr) e.g., (0.5, 1.5) for 50% SL and 1.5 RR
        - Values are dicts with 'wins', 'losses', 'no_exit' counts
    """
    results = {}
    
    for sl_pct in SL_PERCENTAGES:
        for rr in RR_VALUES:
            wins = 0
            losses = 0
            no_exit = 0
            
            for fvg_ctx in fvgs_with_context:
                result = simulate_trade(fvg_ctx, all_data, sl_pct, rr)
                if result == 'win':
                    wins += 1
                elif result == 'loss':
                    losses += 1
                else:
                    no_exit += 1
            
            results[(sl_pct, rr)] = {
                'wins': wins,
                'losses': losses,
                'no_exit': no_exit
            }
    
    return results


def run_backtest_wick_sl(all_data: dict, fvgs_with_context: list) -> dict:
    """
    Run backtest for all FVGs using wick-based SL strategy with different RR values.
    
    SL Strategy:
    - LONG: SL = Low of 08:30 candle - offset (WICK_SL_OFFSET_POINTS)
    - SHORT: SL = High of 08:30 candle + offset (WICK_SL_OFFSET_POINTS)
    
    Args:
        all_data: Dictionary with keys as (date, time) tuples and values as Candle objects.
                  Contains all candle data needed to simulate trades.
        fvgs_with_context: List of FVGWithContext objects containing FVGs with entry context.
    
    Returns:
        Dictionary with backtest results where:
        - Keys are RR values (e.g., 1, 1.5, 2)
        - Values are dicts with 'wins', 'losses', 'no_exit' counts
    """
    results = {}
    
    for rr in RR_VALUES:
        wins = 0
        losses = 0
        no_exit = 0
        
        for fvg_ctx in fvgs_with_context:
            result = simulate_trade_wick_sl(fvg_ctx, all_data, rr)
            if result == 'win':
                wins += 1
            elif result == 'loss':
                losses += 1
            else:
                no_exit += 1
        
        results[rr] = {
            'wins': wins,
            'losses': losses,
            'no_exit': no_exit
        }
    
    return results


def analyze_all_files(base_path: str) -> tuple:
    """
    Analyze all 15m CSV files and return FVGs and statistics.
    """
    all_fvgs = []
    all_fvgs_with_context = []
    all_data = {}
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
        
        # Merge data into all_data for backtesting
        all_data.update(data)
        
        # Count days with 08:30 candles
        dates_with_0830 = set(
            date for date, time in data.keys() 
            if time == '08:30:00'
        )
        total_days_analyzed += len(dates_with_0830)
        
        fvgs = find_fvgs_at_0830(data)
        all_fvgs.extend(fvgs)
        
        # Get FVGs with context for backtesting
        fvgs_ctx = find_fvgs_with_context(data)
        all_fvgs_with_context.extend(fvgs_ctx)
        
        files_processed.append({
            'filename': filename,
            'year': year,
            'days_analyzed': len(dates_with_0830),
            'fvgs_found': len(fvgs),
            'bullish': sum(1 for f in fvgs if f.fvg_type == 'bullish'),
            'bearish': sum(1 for f in fvgs if f.fvg_type == 'bearish')
        })
    
    return all_fvgs, all_fvgs_with_context, all_data, files_processed, total_days_analyzed


def generate_report(fvgs: list, files_stats: list, total_days: int, backtest_results: dict, output_path: str):
    """Generate a markdown report with FVG analysis results and backtesting."""
    
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

## Backtesting Results

### Strategy Rules

1. **Entry**: At the open of candle n+2 (09:00), after FVG detection at 08:30
   - Bullish FVG → LONG position at 09:00 Open
   - Bearish FVG → SHORT position at 09:00 Open

2. **Stop Loss (SL)**: Based on the body of candle n+1 (08:45)
   - Body = |Close - Open| of the 08:45 candle
   - For LONG: SL = Entry - (Body × SL%)
   - For SHORT: SL = Entry + (Body × SL%)

3. **Take Profit (TP)**: Calculated using Risk-Reward ratio
   - Risk = Distance between Entry and SL
   - TP = Entry ± (Risk × RR)

4. **Exit**: Trade exits when price hits SL or TP on subsequent candles (starting 09:15)

---

"""
    
    # Add backtest results tables for each SL%
    for sl_pct in SL_PERCENTAGES:
        sl_label = f"{int(sl_pct * 100)}%"
        report += f"### SL = {sl_label} of Body\n\n"
        report += "| RR | Trades | Wins | Losses | Win Rate (%) |\n"
        report += "|-----|--------|------|--------|-------------|\n"
        
        for rr in RR_VALUES:
            result = backtest_results.get((sl_pct, rr), {'wins': 0, 'losses': 0, 'no_exit': 0})
            wins = result['wins']
            losses = result['losses']
            trades = wins + losses
            win_rate = (wins / trades * 100) if trades > 0 else 0
            report += f"| {rr} | {trades} | {wins} | {losses} | {win_rate:.2f}% |\n"
        
        report += "\n"

    report += """---

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
- Backtest trades that don't hit SL or TP within the same day are excluded from win rate calculation
"""
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\nReport saved to: {output_path}")


def generate_pnl_report(backtest_results: dict, output_path: str, risk_per_trade: float = 100.0):
    """
    Generate a detailed P&L report with monetary calculations.
    
    Args:
        backtest_results: Dictionary with backtest results from run_backtest()
        output_path: Path to save the markdown report
        risk_per_trade: Risk amount per trade in dollars (default: 100$)
    """
    # Calculate P&L metrics for all combinations
    pnl_data = {}
    for sl_pct in SL_PERCENTAGES:
        for rr in RR_VALUES:
            result = backtest_results.get((sl_pct, rr), {'wins': 0, 'losses': 0, 'no_exit': 0})
            wins = result['wins']
            losses = result['losses']
            trades = wins + losses
            
            # P&L calculations
            total_gain = wins * risk_per_trade * rr
            total_loss = losses * risk_per_trade
            net_pnl = total_gain - total_loss
            profit_factor = total_gain / total_loss if total_loss > 0 else float('inf') if total_gain > 0 else 0
            avg_trade = net_pnl / trades if trades > 0 else 0
            
            pnl_data[(sl_pct, rr)] = {
                'trades': trades,
                'wins': wins,
                'losses': losses,
                'total_gain': total_gain,
                'total_loss': total_loss,
                'net_pnl': net_pnl,
                'profit_factor': profit_factor,
                'avg_trade': avg_trade
            }
    
    # Find best combinations
    best_pnl = max(pnl_data.items(), key=lambda x: x[1]['net_pnl'])
    best_pf = max(pnl_data.items(), key=lambda x: x[1]['profit_factor'])
    best_avg = max(pnl_data.items(), key=lambda x: x[1]['avg_trade'])
    
    # Generate report
    report = f"""# Backtest P&L Results

## Configuration

- **Risk per Trade**: ${risk_per_trade:.0f}
- **Analysis Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## P&L Calculation Method

- **Win**: Gain of ${risk_per_trade:.0f} × RR (e.g., RR 2 = gain of ${risk_per_trade * 2:.0f})
- **Loss**: Loss of ${risk_per_trade:.0f}
- **Total P&L**: (Wins × ${risk_per_trade:.0f} × RR) - (Losses × ${risk_per_trade:.0f})
- **Profit Factor**: Total Gains / Total Losses
- **Average Trade**: Total P&L / Number of Trades

---

"""
    
    # Generate tables for each SL%
    for sl_pct in SL_PERCENTAGES:
        sl_label = f"{int(sl_pct * 100)}%"
        report += f"## SL = {sl_label} of Body\n\n"
        report += "| RR | Trades | Wins | Losses | Gain Total ($) | Perte Total ($) | P&L Net ($) | Profit Factor | Avg Trade ($) |\n"
        report += "|-----|--------|------|--------|----------------|-----------------|-------------|---------------|---------------|\n"
        
        for rr in RR_VALUES:
            data = pnl_data[(sl_pct, rr)]
            pf_str = f"{data['profit_factor']:.2f}" if data['profit_factor'] != float('inf') else "∞"
            report += f"| {rr} | {data['trades']} | {data['wins']} | {data['losses']} | {data['total_gain']:,.0f} | {data['total_loss']:,.0f} | {data['net_pnl']:+,.0f} | {pf_str} | {data['avg_trade']:+,.2f} |\n"
        
        report += "\n"
    
    # Summary section
    report += """---

## Résumé des Meilleures Combinaisons

"""
    
    # Best P&L Net
    best_pnl_key, best_pnl_data = best_pnl
    sl_pct_best_pnl = int(best_pnl_key[0] * 100)
    rr_best_pnl = best_pnl_key[1]
    pf_display_pnl = f"{best_pnl_data['profit_factor']:.2f}" if best_pnl_data['profit_factor'] != float('inf') else "∞"
    report += f"""### 🏆 Meilleure Combinaison (P&L Net le plus élevé)

| Paramètre | Valeur |
|-----------|--------|
| **SL%** | {sl_pct_best_pnl}% |
| **RR** | {rr_best_pnl} |
| **Trades** | {best_pnl_data['trades']} |
| **Wins** | {best_pnl_data['wins']} |
| **Losses** | {best_pnl_data['losses']} |
| **P&L Net** | ${best_pnl_data['net_pnl']:+,.0f} |
| **Profit Factor** | {pf_display_pnl} |
| **Avg Trade** | ${best_pnl_data['avg_trade']:+,.2f} |

"""
    
    # Best Profit Factor
    best_pf_key, best_pf_data = best_pf
    sl_pct_best_pf = int(best_pf_key[0] * 100)
    rr_best_pf = best_pf_key[1]
    pf_display = f"{best_pf_data['profit_factor']:.2f}" if best_pf_data['profit_factor'] != float('inf') else "∞"
    report += f"""### 📊 Meilleur Profit Factor

| Paramètre | Valeur |
|-----------|--------|
| **SL%** | {sl_pct_best_pf}% |
| **RR** | {rr_best_pf} |
| **Trades** | {best_pf_data['trades']} |
| **Wins** | {best_pf_data['wins']} |
| **Losses** | {best_pf_data['losses']} |
| **P&L Net** | ${best_pf_data['net_pnl']:+,.0f} |
| **Profit Factor** | {pf_display} |
| **Avg Trade** | ${best_pf_data['avg_trade']:+,.2f} |

"""
    
    # Best Average Trade
    best_avg_key, best_avg_data = best_avg
    sl_pct_best_avg = int(best_avg_key[0] * 100)
    rr_best_avg = best_avg_key[1]
    pf_display_avg = f"{best_avg_data['profit_factor']:.2f}" if best_avg_data['profit_factor'] != float('inf') else "∞"
    report += f"""### 💰 Meilleur Average Trade

| Paramètre | Valeur |
|-----------|--------|
| **SL%** | {sl_pct_best_avg}% |
| **RR** | {rr_best_avg} |
| **Trades** | {best_avg_data['trades']} |
| **Wins** | {best_avg_data['wins']} |
| **Losses** | {best_avg_data['losses']} |
| **P&L Net** | ${best_avg_data['net_pnl']:+,.0f} |
| **Profit Factor** | {pf_display_avg} |
| **Avg Trade** | ${best_avg_data['avg_trade']:+,.2f} |

---

## Notes

- Les résultats sont basés sur un risque fixe de ${risk_per_trade:.0f} par trade
- Les trades sans sortie (SL ou TP non atteints dans la journée) sont exclus des calculs
- Le Profit Factor "∞" indique qu'il n'y a eu aucune perte
"""
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"P&L Report saved to: {output_path}")


def calculate_pnl_metrics(wins: int, losses: int, rr: float, risk_per_trade: float) -> dict:
    """
    Calculate P&L metrics for a given set of trade results.
    
    Args:
        wins: Number of winning trades
        losses: Number of losing trades
        rr: Risk-reward ratio
        risk_per_trade: Risk amount per trade in dollars
        
    Returns:
        Dictionary with calculated P&L metrics
    """
    trades = wins + losses
    total_gain = wins * risk_per_trade * rr
    total_loss = losses * risk_per_trade
    net_pnl = total_gain - total_loss
    profit_factor = total_gain / total_loss if total_loss > 0 else float('inf') if total_gain > 0 else 0
    avg_trade = net_pnl / trades if trades > 0 else 0
    win_rate = (wins / trades * 100) if trades > 0 else 0
    
    return {
        'trades': trades,
        'wins': wins,
        'losses': losses,
        'total_gain': total_gain,
        'total_loss': total_loss,
        'net_pnl': net_pnl,
        'profit_factor': profit_factor,
        'avg_trade': avg_trade,
        'win_rate': win_rate
    }


def generate_wick_sl_pnl_report(wick_sl_results: dict, body_sl_results: dict, output_path: str, risk_per_trade: float = 100.0):
    """
    Generate a detailed P&L report for wick-based SL strategy with comparison to body-based SL.
    
    Args:
        wick_sl_results: Dictionary with wick SL backtest results from run_backtest_wick_sl()
        body_sl_results: Dictionary with body SL backtest results from run_backtest() for comparison
        output_path: Path to save the markdown report
        risk_per_trade: Risk amount per trade in dollars (default: 100$)
    """
    # Calculate P&L metrics for wick SL strategy
    wick_pnl_data = {}
    for rr in RR_VALUES:
        result = wick_sl_results.get(rr, {'wins': 0, 'losses': 0, 'no_exit': 0})
        wick_pnl_data[rr] = calculate_pnl_metrics(result['wins'], result['losses'], rr, risk_per_trade)
    
    # Calculate P&L metrics for body SL strategy (50% body for comparison - the best performer)
    body_pnl_data = {}
    for rr in RR_VALUES:
        result = body_sl_results.get((0.5, rr), {'wins': 0, 'losses': 0, 'no_exit': 0})
        body_pnl_data[rr] = calculate_pnl_metrics(result['wins'], result['losses'], rr, risk_per_trade)
    
    # Find best combinations for wick SL
    best_pnl = max(wick_pnl_data.items(), key=lambda x: x[1]['net_pnl'])
    best_pf = max(wick_pnl_data.items(), key=lambda x: x[1]['profit_factor'])
    best_avg = max(wick_pnl_data.items(), key=lambda x: x[1]['avg_trade'])
    
    # Generate report
    report = f"""# Wick-Based SL Backtest Results

## Configuration

- **Risk per Trade**: ${risk_per_trade:.0f}
- **Analysis Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Stratégie de SL (Wick-Based)

Cette stratégie utilise la mèche de la bougie 08:30 (candle n) pour calculer le Stop Loss:

- **Position LONG (FVG haussier)**: SL = Low de la bougie 08:30 - 1 point
- **Position SHORT (FVG baissier)**: SL = High de la bougie 08:30 + 1 point

### Différence avec la stratégie précédente

| Aspect | Stratégie Précédente (Body) | Nouvelle Stratégie (Wick) |
|--------|----------------------------|---------------------------|
| **Base du SL** | Corps de la bougie 08:45 | Mèche de la bougie 08:30 |
| **Calcul LONG** | Entry - (Body × SL%) | Low 08:30 - 1 point |
| **Calcul SHORT** | Entry + (Body × SL%) | High 08:30 + 1 point |

---

## P&L Calculation Method

- **Win**: Gain of ${risk_per_trade:.0f} × RR (e.g., RR 2 = gain of ${risk_per_trade * 2:.0f})
- **Loss**: Loss of ${risk_per_trade:.0f}
- **Total P&L**: (Wins × ${risk_per_trade:.0f} × RR) - (Losses × ${risk_per_trade:.0f})
- **Profit Factor**: Total Gains / Total Losses
- **Average Trade**: Total P&L / Number of Trades

---

## Résultats Wick-Based SL

| RR | Trades | Wins | Losses | Win Rate (%) | P&L Net ($) | Profit Factor | Avg Trade ($) |
|-----|--------|------|--------|--------------|-------------|---------------|---------------|
"""
    
    for rr in RR_VALUES:
        data = wick_pnl_data[rr]
        pf_str = f"{data['profit_factor']:.2f}" if data['profit_factor'] != float('inf') else "∞"
        report += f"| {rr} | {data['trades']} | {data['wins']} | {data['losses']} | {data['win_rate']:.2f}% | {data['net_pnl']:+,.0f} | {pf_str} | {data['avg_trade']:+,.2f} |\n"
    
    report += """
---

## Comparaison avec la Stratégie Précédente (Body 50% SL)

| RR | Wick SL P&L | Body SL P&L | Différence | Wick Win Rate | Body Win Rate |
|-----|-------------|-------------|------------|---------------|---------------|
"""
    
    for rr in RR_VALUES:
        wick_data = wick_pnl_data[rr]
        body_data = body_pnl_data[rr]
        diff = wick_data['net_pnl'] - body_data['net_pnl']
        report += f"| {rr} | {wick_data['net_pnl']:+,.0f} | {body_data['net_pnl']:+,.0f} | {diff:+,.0f} | {wick_data['win_rate']:.2f}% | {body_data['win_rate']:.2f}% |\n"
    
    report += """
---

## Résumé des Meilleures Combinaisons (Wick SL)

"""
    
    # Best P&L Net
    best_pnl_key, best_pnl_data = best_pnl
    pf_display_pnl = f"{best_pnl_data['profit_factor']:.2f}" if best_pnl_data['profit_factor'] != float('inf') else "∞"
    report += f"""### 🏆 Meilleure Combinaison (P&L Net le plus élevé)

| Paramètre | Valeur |
|-----------|--------|
| **RR** | {best_pnl_key} |
| **Trades** | {best_pnl_data['trades']} |
| **Wins** | {best_pnl_data['wins']} |
| **Losses** | {best_pnl_data['losses']} |
| **Win Rate** | {best_pnl_data['win_rate']:.2f}% |
| **P&L Net** | ${best_pnl_data['net_pnl']:+,.0f} |
| **Profit Factor** | {pf_display_pnl} |
| **Avg Trade** | ${best_pnl_data['avg_trade']:+,.2f} |

"""
    
    # Best Profit Factor
    best_pf_key, best_pf_data = best_pf
    pf_display = f"{best_pf_data['profit_factor']:.2f}" if best_pf_data['profit_factor'] != float('inf') else "∞"
    report += f"""### 📊 Meilleur Profit Factor

| Paramètre | Valeur |
|-----------|--------|
| **RR** | {best_pf_key} |
| **Trades** | {best_pf_data['trades']} |
| **Wins** | {best_pf_data['wins']} |
| **Losses** | {best_pf_data['losses']} |
| **Win Rate** | {best_pf_data['win_rate']:.2f}% |
| **P&L Net** | ${best_pf_data['net_pnl']:+,.0f} |
| **Profit Factor** | {pf_display} |
| **Avg Trade** | ${best_pf_data['avg_trade']:+,.2f} |

"""
    
    # Best Average Trade
    best_avg_key, best_avg_data = best_avg
    pf_display_avg = f"{best_avg_data['profit_factor']:.2f}" if best_avg_data['profit_factor'] != float('inf') else "∞"
    report += f"""### 💰 Meilleur Average Trade

| Paramètre | Valeur |
|-----------|--------|
| **RR** | {best_avg_key} |
| **Trades** | {best_avg_data['trades']} |
| **Wins** | {best_avg_data['wins']} |
| **Losses** | {best_avg_data['losses']} |
| **Win Rate** | {best_avg_data['win_rate']:.2f}% |
| **P&L Net** | ${best_avg_data['net_pnl']:+,.0f} |
| **Profit Factor** | {pf_display_avg} |
| **Avg Trade** | ${best_avg_data['avg_trade']:+,.2f} |

---

## Notes

- Les résultats sont basés sur un risque fixe de ${risk_per_trade:.0f} par trade
- Les trades sans sortie (SL ou TP non atteints dans la journée) sont exclus des calculs
- Le Profit Factor "∞" indique qu'il n'y a eu aucune perte
- La comparaison est faite avec la stratégie Body SL à 50% (meilleur performer de la stratégie précédente)
"""
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"Wick SL P&L Report saved to: {output_path}")


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
    fvgs, fvgs_with_context, all_data, files_stats, total_days = analyze_all_files(base_path)
    
    print()
    print("=" * 60)
    print("ANALYSIS COMPLETE")
    print("=" * 60)
    print(f"Total days analyzed: {total_days:,}")
    print(f"Total FVGs found: {len(fvgs):,}")
    print(f"  - Bullish: {sum(1 for f in fvgs if f.fvg_type == 'bullish'):,}")
    print(f"  - Bearish: {sum(1 for f in fvgs if f.fvg_type == 'bearish'):,}")
    
    # Run backtest
    print()
    print("=" * 60)
    print("RUNNING BACKTEST")
    print("=" * 60)
    print(f"FVGs with entry context: {len(fvgs_with_context):,}")
    
    backtest_results = run_backtest(all_data, fvgs_with_context)
    
    # Print summary of backtest results
    print()
    print("Backtest Results Summary:")
    
    for sl_pct in SL_PERCENTAGES:
        print(f"\n  SL = {int(sl_pct * 100)}% of Body:")
        for rr in RR_VALUES:
            result = backtest_results.get((sl_pct, rr), {'wins': 0, 'losses': 0, 'no_exit': 0})
            wins = result['wins']
            losses = result['losses']
            trades = wins + losses
            win_rate = (wins / trades * 100) if trades > 0 else 0
            print(f"    RR {rr}: {trades} trades, {wins} wins, {losses} losses ({win_rate:.2f}% WR)")
    
    # Generate report
    generate_report(fvgs, files_stats, total_days, backtest_results, output_path)
    
    # Generate P&L report
    pnl_output_path = os.path.join(base_path, "BACKTEST_PNL_RESULTS.md")
    generate_pnl_report(backtest_results, pnl_output_path, risk_per_trade=100.0)
    
    # Run Wick-Based SL Backtest
    print()
    print("=" * 60)
    print("RUNNING WICK-BASED SL BACKTEST")
    print("=" * 60)
    print(f"SL Strategy: LONG = Low 08:30 - {WICK_SL_OFFSET_POINTS} point, SHORT = High 08:30 + {WICK_SL_OFFSET_POINTS} point")
    
    wick_sl_results = run_backtest_wick_sl(all_data, fvgs_with_context)
    
    # Print summary of wick SL backtest results
    print()
    print("Wick SL Backtest Results Summary:")
    for rr in RR_VALUES:
        result = wick_sl_results.get(rr, {'wins': 0, 'losses': 0, 'no_exit': 0})
        wins = result['wins']
        losses = result['losses']
        trades = wins + losses
        win_rate = (wins / trades * 100) if trades > 0 else 0
        print(f"  RR {rr}: {trades} trades, {wins} wins, {losses} losses ({win_rate:.2f}% WR)")
    
    # Generate Wick SL P&L report
    wick_sl_output_path = os.path.join(base_path, "WICK_SL_BACKTEST_RESULTS.md")
    generate_wick_sl_pnl_report(wick_sl_results, backtest_results, wick_sl_output_path, risk_per_trade=100.0)
    
    print()
    print("Analysis complete!")


if __name__ == "__main__":
    main()

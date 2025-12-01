#!/usr/bin/env python3
"""
Trading Setup Detection System

This script implements a 3-step trading methodology:
1. Context Identification (H4 or H1 timeframe): Identify FVG with wick-only fill
2. 15-minute Confirmation: New FVG forms that will be used for entry signal
3. Entry Signal (5m or 15m): Price closes beyond the 15-min FVG

CSV Data Structure:
- Semicolon separator (;)
- Columns: Date, Time, Open, High, Low, Close, Volume
- Date format: DD/MM/YYYY
- Time format: HH:MM:SS
"""

import os
from datetime import datetime, time, timedelta
from enum import Enum
from typing import NamedTuple, Optional, Tuple
import pytz


# Configuration constants
MAX_CANDLES_FOR_ENTRY_CONFIRMATION = 50  # Max candles to check for entry signal
LOOKBACK_HOURS_FOR_M15_FVG = 4  # Hours to look back for 15m FVG
EXPECTED_CSV_COLUMNS = 7  # Number of expected columns in CSV file

# File naming patterns for different timeframes
FILE_PATTERN_4H = "{year} 4H.csv"
FILE_PATTERN_1H = "{year} 1H.csv"
FILE_PATTERN_15M = "{year} 15m.csv"
FILE_PATTERN_5M = "{year} 5m.csv"


class Direction(Enum):
    """Trading direction enum."""
    LONG = 'LONG'
    SHORT = 'SHORT'


class Candle(NamedTuple):
    """Represents a single OHLCV candle."""
    datetime: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int


class FVG(NamedTuple):
    """Represents a Fair Value Gap."""
    candle_index: int  # Index of the middle candle
    datetime: datetime
    is_bullish: bool
    top: float  # Upper boundary of the gap
    bottom: float  # Lower boundary of the gap
    filled: bool = False
    filled_by_wick_only: bool = False
    fill_candle_index: int = -1


class SwingPoint(NamedTuple):
    """Represents a swing high or swing low."""
    candle_index: int
    datetime: datetime
    is_swing_high: bool  # True for swing high, False for swing low
    price: float


class TradingSetup(NamedTuple):
    """Represents a complete trading setup."""
    entry_datetime: datetime
    direction: Direction
    h4_h1_fvg: FVG
    m15_fvg: FVG
    entry_price: float


def load_csv_data(filepath: str) -> list[Candle]:
    """Load CSV data and return list of Candle objects."""
    candles = []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        # Skip header
        next(f)
        
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            parts = line.split(';')
            if len(parts) < EXPECTED_CSV_COLUMNS:
                continue
            
            try:
                # Parse date (DD/MM/YYYY) and time (HH:MM:SS)
                date_parts = parts[0].split('/')
                time_parts = parts[1].split(':')
                
                dt = datetime(
                    year=int(date_parts[2]),
                    month=int(date_parts[1]),
                    day=int(date_parts[0]),
                    hour=int(time_parts[0]),
                    minute=int(time_parts[1]),
                    second=int(time_parts[2])
                )
                
                candle = Candle(
                    datetime=dt,
                    open=float(parts[2]),
                    high=float(parts[3]),
                    low=float(parts[4]),
                    close=float(parts[5]),
                    volume=int(parts[6])
                )
                candles.append(candle)
            except (ValueError, IndexError):
                continue
    
    return candles


def detect_fvg(candles: list[Candle]) -> list[FVG]:
    """
    Detect Fair Value Gaps in a list of candles.
    
    Bullish FVG: candle[i-1].high < candle[i+1].low (gap up)
    Bearish FVG: candle[i-1].low > candle[i+1].high (gap down)
    """
    fvgs = []
    
    for i in range(1, len(candles) - 1):
        prev_candle = candles[i - 1]
        middle_candle = candles[i]
        next_candle = candles[i + 1]
        
        # Check for bullish FVG (gap up)
        if prev_candle.high < next_candle.low:
            fvg = FVG(
                candle_index=i,
                datetime=middle_candle.datetime,
                is_bullish=True,
                top=next_candle.low,
                bottom=prev_candle.high,
                filled=False,
                filled_by_wick_only=False,
                fill_candle_index=-1
            )
            fvgs.append(fvg)
        
        # Check for bearish FVG (gap down)
        elif prev_candle.low > next_candle.high:
            fvg = FVG(
                candle_index=i,
                datetime=middle_candle.datetime,
                is_bullish=False,
                top=prev_candle.low,
                bottom=next_candle.high,
                filled=False,
                filled_by_wick_only=False,
                fill_candle_index=-1
            )
            fvgs.append(fvg)
    
    return fvgs


def detect_swing_points(candles: list[Candle]) -> list[SwingPoint]:
    """
    Detect swing highs and swing lows.
    
    Swing high: bullish candle followed by bearish candle
    Swing low: bearish candle followed by bullish candle
    
    Note: Doji candles (where open == close) are excluded from swing point detection
    as they do not clearly indicate bullish or bearish sentiment.
    """
    swing_points = []
    
    for i in range(len(candles) - 1):
        curr_candle = candles[i]
        next_candle = candles[i + 1]
        
        # Skip doji candles (where open equals close) as they're neutral
        is_curr_doji = curr_candle.close == curr_candle.open
        is_next_doji = next_candle.close == next_candle.open
        
        if is_curr_doji or is_next_doji:
            continue
        
        is_curr_bullish = curr_candle.close > curr_candle.open
        is_curr_bearish = curr_candle.close < curr_candle.open
        is_next_bullish = next_candle.close > next_candle.open
        is_next_bearish = next_candle.close < next_candle.open
        
        # Swing high: bullish candle followed by bearish candle
        if is_curr_bullish and is_next_bearish:
            swing_points.append(SwingPoint(
                candle_index=i,
                datetime=curr_candle.datetime,
                is_swing_high=True,
                price=curr_candle.high
            ))
        
        # Swing low: bearish candle followed by bullish candle
        elif is_curr_bearish and is_next_bullish:
            swing_points.append(SwingPoint(
                candle_index=i,
                datetime=curr_candle.datetime,
                is_swing_high=False,
                price=curr_candle.low
            ))
    
    return swing_points


def check_wick_only_fill(fvg: FVG, candle: Candle, candle_index: int) -> FVG:
    """
    Check if a candle fills the FVG with wick only (not body).
    
    For bullish FVG: high touches FVG zone but close stays below FVG zone
    For bearish FVG: low touches FVG zone but close stays above FVG zone
    
    Returns updated FVG with fill status.
    """
    if fvg.filled:
        return fvg
    
    def create_filled_fvg(filled_by_wick_only: bool) -> FVG:
        """Helper to create a filled FVG with given wick-only status."""
        return FVG(
            candle_index=fvg.candle_index,
            datetime=fvg.datetime,
            is_bullish=fvg.is_bullish,
            top=fvg.top,
            bottom=fvg.bottom,
            filled=True,
            filled_by_wick_only=filled_by_wick_only,
            fill_candle_index=candle_index
        )
    
    candle_body_top = max(candle.open, candle.close)
    candle_body_bottom = min(candle.open, candle.close)
    
    if fvg.is_bullish:
        # For bullish FVG: price should come down to fill it
        # Wick enters the FVG zone (low < top of FVG zone)
        # Body stays above FVG zone (body_bottom >= bottom of FVG zone)
        wick_enters_fvg = candle.low < fvg.top
        body_stays_above = candle_body_bottom >= fvg.bottom
        
        if wick_enters_fvg:
            if body_stays_above:
                # Wick only fill - wick enters FVG but body doesn't
                return create_filled_fvg(filled_by_wick_only=True)
            else:
                # Body also fills the FVG
                return create_filled_fvg(filled_by_wick_only=False)
    else:
        # For bearish FVG: price should come up to fill it
        # Wick enters the FVG zone (high > bottom of FVG zone)
        # Body stays below FVG zone (body_top <= top of FVG zone)
        wick_enters_fvg = candle.high > fvg.bottom
        body_stays_below = candle_body_top <= fvg.top
        
        if wick_enters_fvg:
            if body_stays_below:
                # Wick only fill - wick enters FVG but body doesn't
                return create_filled_fvg(filled_by_wick_only=True)
            else:
                # Body also fills the FVG
                return create_filled_fvg(filled_by_wick_only=False)
    
    return fvg


def find_wick_only_filled_fvgs(candles: list[Candle], fvgs: list[FVG]) -> list[FVG]:
    """
    Process FVGs to find those that were filled by wick only.
    """
    filled_fvgs = []
    
    for fvg in fvgs:
        updated_fvg = fvg
        # Check candles after the FVG formation
        for i in range(fvg.candle_index + 2, len(candles)):
            updated_fvg = check_wick_only_fill(updated_fvg, candles[i], i)
            if updated_fvg.filled:
                break
        
        if updated_fvg.filled and updated_fvg.filled_by_wick_only:
            filled_fvgs.append(updated_fvg)
    
    return filled_fvgs


def is_within_chicago_time_range(dt: datetime, start_hour: int = 2, end_hour: int = 12) -> bool:
    """
    Check if the datetime is within the specified Chicago time range.
    The data appears to be in UTC, so we need to convert.
    """
    chicago_tz = pytz.timezone('America/Chicago')
    utc_tz = pytz.UTC
    
    # Handle both timezone-aware and naive datetimes
    if dt.tzinfo is None:
        # Naive datetime - localize as UTC
        utc_dt = utc_tz.localize(dt)
    else:
        # Already timezone-aware - convert to UTC first
        utc_dt = dt.astimezone(utc_tz)
    
    chicago_dt = utc_dt.astimezone(chicago_tz)
    
    return start_hour <= chicago_dt.hour < end_hour


def find_m15_fvg_near_datetime(m15_fvgs: list[FVG], target_dt: datetime, 
                                direction: Direction, lookback_hours: int = LOOKBACK_HOURS_FOR_M15_FVG) -> Optional[FVG]:
    """
    Find a 15-minute FVG that formed near the target datetime.
    
    For SHORT: Look for a bullish FVG (price went up, then will reverse down)
    For LONG: Look for a bearish FVG (price went down, then will reverse up)
    """
    if direction == Direction.SHORT:
        # Need bullish FVG
        target_is_bullish = True
    else:
        # Need bearish FVG
        target_is_bullish = False
    
    # Look for FVGs in the time window before target (iterate backwards for efficiency)
    for i in range(len(m15_fvgs) - 1, -1, -1):
        fvg = m15_fvgs[i]
        time_diff = target_dt - fvg.datetime
        # FVG must have formed before target (time_diff > 0) and within lookback window
        if timedelta(0) < time_diff < timedelta(hours=lookback_hours):
            if fvg.is_bullish == target_is_bullish:
                return fvg
    
    return None


def find_entry_confirmation(candles: list[Candle], m15_fvg: FVG, 
                            direction: Direction, start_index: int,
                            max_candles: int = MAX_CANDLES_FOR_ENTRY_CONFIRMATION) -> Optional[Tuple[int, float]]:
    """
    Find entry confirmation on 5m or 15m timeframe.
    
    For SHORT: Wait for price to close BELOW the bullish 15-min FVG
    For LONG: Wait for price to close ABOVE the bearish 15-min FVG
    """
    for i in range(start_index, min(start_index + max_candles, len(candles))):
        candle = candles[i]
        
        if direction == Direction.SHORT:
            # Wait for close below bullish FVG bottom
            if candle.close < m15_fvg.bottom:
                return i, candle.close
        else:  # LONG
            # Wait for close above bearish FVG top
            if candle.close > m15_fvg.top:
                return i, candle.close
    
    return None


def detect_setups(h4_candles: list[Candle], h1_candles: list[Candle],
                  m15_candles: list[Candle], m5_candles: list[Candle]) -> list[TradingSetup]:
    """
    Implement the 3-step trading methodology to detect valid setups.
    """
    setups = []
    
    # Step 1: Detect FVGs on H4 and H1
    h4_fvgs = detect_fvg(h4_candles)
    h1_fvgs = detect_fvg(h1_candles)
    
    # Find wick-only filled FVGs with their source candles
    h4_wick_filled = find_wick_only_filled_fvgs(h4_candles, h4_fvgs)
    h1_wick_filled = find_wick_only_filled_fvgs(h1_candles, h1_fvgs)
    
    # Create list of (FVG, source_candles) tuples for proper fill datetime lookup
    context_fvgs_with_candles = [(fvg, h4_candles) for fvg in h4_wick_filled] + \
                                 [(fvg, h1_candles) for fvg in h1_wick_filled]
    
    # Detect FVGs on 15-minute timeframe for Step 2
    m15_fvgs = detect_fvg(m15_candles)
    
    # Process each context FVG
    for ctx_fvg, source_candles in context_fvgs_with_candles:
        if ctx_fvg.fill_candle_index < 0:
            continue
        
        # Determine direction based on FVG type
        # Bullish FVG filled by wick only -> price continues down -> SHORT
        # Bearish FVG filled by wick only -> price continues up -> LONG
        direction = Direction.SHORT if ctx_fvg.is_bullish else Direction.LONG
        
        # Get the actual fill datetime from the fill candle
        fill_datetime = source_candles[ctx_fvg.fill_candle_index].datetime
        
        # Find a 15m FVG near the context fill
        m15_fvg = find_m15_fvg_near_datetime(m15_fvgs, fill_datetime, direction)
        
        if m15_fvg is None:
            continue
        
        # Step 3: Find entry confirmation on 5m or 15m
        # Find the starting index in m15 candles after the FVG
        start_idx = m15_fvg.candle_index + 2
        
        entry_result = find_entry_confirmation(m15_candles, m15_fvg, direction, start_idx)
        
        if entry_result:
            entry_idx, entry_price = entry_result
            entry_datetime = m15_candles[entry_idx].datetime
            
            # Check if within Chicago time range
            if is_within_chicago_time_range(entry_datetime):
                setup = TradingSetup(
                    entry_datetime=entry_datetime,
                    direction=direction,
                    h4_h1_fvg=ctx_fvg,
                    m15_fvg=m15_fvg,
                    entry_price=entry_price
                )
                setups.append(setup)
    
    return setups


def load_yearly_data(base_path: str, year: int) -> tuple[list[Candle], list[Candle], list[Candle], list[Candle]]:
    """Load all timeframe data for a specific year."""
    h4_path = os.path.join(base_path, FILE_PATTERN_4H.format(year=year))
    h1_path = os.path.join(base_path, FILE_PATTERN_1H.format(year=year))
    m15_path = os.path.join(base_path, FILE_PATTERN_15M.format(year=year))
    m5_path = os.path.join(base_path, FILE_PATTERN_5M.format(year=year))
    
    h4_candles = load_csv_data(h4_path) if os.path.exists(h4_path) else []
    h1_candles = load_csv_data(h1_path) if os.path.exists(h1_path) else []
    m15_candles = load_csv_data(m15_path) if os.path.exists(m15_path) else []
    m5_candles = load_csv_data(m5_path) if os.path.exists(m5_path) else []
    
    return h4_candles, h1_candles, m15_candles, m5_candles


def main():
    """Main entry point."""
    base_path = os.path.dirname(os.path.abspath(__file__))
    years = range(2018, 2026)  # 2018 through 2025
    
    total_setups = 0
    long_setups = 0
    short_setups = 0
    yearly_setups = {}
    
    print("=" * 60)
    print("Trading Setup Detection System")
    print("=" * 60)
    print()
    print("Processing data for years 2018-2025...")
    print("Filtering setups between 2:00 and 12:00 Chicago time")
    print()
    
    all_setups = []
    
    for year in years:
        print(f"Processing year {year}...", end=" ")
        
        try:
            h4_candles, h1_candles, m15_candles, m5_candles = load_yearly_data(base_path, year)
            
            # Check if all required data files have data (empty files are invalid for processing)
            if (len(h4_candles) == 0 or len(h1_candles) == 0 or 
                len(m15_candles) == 0 or len(m5_candles) == 0):
                print(f"Incomplete data for {year}, skipping.")
                continue
            
            year_setups = detect_setups(h4_candles, h1_candles, m15_candles, m5_candles)
            
            year_count = len(year_setups)
            year_longs = sum(1 for s in year_setups if s.direction == Direction.LONG)
            year_shorts = sum(1 for s in year_setups if s.direction == Direction.SHORT)
            
            yearly_setups[year] = {
                'total': year_count,
                'long': year_longs,
                'short': year_shorts
            }
            
            total_setups += year_count
            long_setups += year_longs
            short_setups += year_shorts
            all_setups.extend(year_setups)
            
            print(f"Found {year_count} setups (Long: {year_longs}, Short: {year_shorts})")
            
        except FileNotFoundError as e:
            print(f"Data file not found for {year}: {e}")
        except Exception as e:
            print(f"Error processing {year}: {e}")
    
    print()
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print()
    print("Yearly Breakdown:")
    print("-" * 40)
    
    for year in sorted(yearly_setups.keys()):
        stats = yearly_setups[year]
        print(f"  {year}: {stats['total']:4d} total ({stats['long']:3d} LONG, {stats['short']:3d} SHORT)")
    
    print()
    print("-" * 40)
    print(f"TOTAL VALID SETUPS: {total_setups}")
    print(f"  - LONG setups:  {long_setups}")
    print(f"  - SHORT setups: {short_setups}")
    print("=" * 60)
    
    # Print some example setups if any were found
    if all_setups:
        print()
        print("Sample Setups (first 5):")
        print("-" * 40)
        for setup in all_setups[:5]:
            print(f"  {setup.entry_datetime.strftime('%Y-%m-%d %H:%M')} - "
                  f"{setup.direction.value} @ {setup.entry_price:.2f}")
            print(f"    H4/H1 FVG: {'Bullish' if setup.h4_h1_fvg.is_bullish else 'Bearish'} "
                  f"at {setup.h4_h1_fvg.datetime.strftime('%Y-%m-%d %H:%M')}")
            print(f"    15m FVG: {'Bullish' if setup.m15_fvg.is_bullish else 'Bearish'} "
                  f"at {setup.m15_fvg.datetime.strftime('%Y-%m-%d %H:%M')}")
            print()
    
    return total_setups


if __name__ == "__main__":
    main()

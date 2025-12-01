#!/usr/bin/env python3
"""
Trading Setup Detection System

This script implements a 3-step trading methodology:
1. Context Identification (H4 or H1 timeframe): Identify FVG with wick-only fill (liquidity sweep)
2. 5-minute FVG Analysis: 
   - For LONG: Detect bearish FVGs formed before price reaches the H4/H1 FVG
   - For SHORT: Detect bullish FVGs formed before price reaches the H4/H1 FVG
3. Entry Signal:
   - For LONG: Price closes ABOVE the bearish 5m FVG, SL options available, TP at RR 1:1
   - For SHORT: Price closes BELOW the bullish 5m FVG, SL options available, TP at RR 1:1

SL Placement Options:
1. Below/above the broken FVG
2. 100% retracement of entry candle + 1 point
3. Below/above the wick of entry candle

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
LOOKBACK_HOURS_FOR_M5_FVG = 4  # Hours to look back for 5m FVG
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


class SLType(Enum):
    """Stop Loss placement type."""
    FVG = 'FVG'  # Below/above the broken FVG
    RETRACEMENT = 'RETRACEMENT'  # 100% retracement of candle + 1 point
    WICK = 'WICK'  # Below/above the wick of entry candle


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


class TradeResult(Enum):
    """Trade outcome enum."""
    WIN = 'WIN'
    LOSS = 'LOSS'
    PENDING = 'PENDING'


class TradingSetup(NamedTuple):
    """Represents a complete trading setup."""
    entry_datetime: datetime
    direction: Direction
    h4_h1_fvg: FVG
    m5_fvg: FVG  # Changed from m15_fvg to m5_fvg
    entry_price: float
    stop_loss: float  # SL based on selected SL type
    take_profit: float  # TP with RR 1:1
    sl_type: SLType = SLType.FVG  # Type of SL placement used
    result: TradeResult = TradeResult.PENDING
    exit_datetime: Optional[datetime] = None


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


def find_m5_fvg_near_datetime(m5_fvgs: list[FVG], target_dt: datetime, 
                                direction: Direction, lookback_hours: int = LOOKBACK_HOURS_FOR_M5_FVG) -> Optional[FVG]:
    """
    Find a 5-minute FVG that formed near the target datetime.
    
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
    for i in range(len(m5_fvgs) - 1, -1, -1):
        fvg = m5_fvgs[i]
        time_diff = target_dt - fvg.datetime
        # FVG must have formed before target (time_diff > 0) and within lookback window
        if timedelta(0) < time_diff < timedelta(hours=lookback_hours):
            if fvg.is_bullish == target_is_bullish:
                return fvg
    
    return None


def calculate_stop_loss(candle: Candle, fvg: FVG, direction: Direction, sl_type: SLType) -> float:
    """
    Calculate stop loss based on the selected SL type.
    
    Args:
        candle: The entry candle
        fvg: The 5-minute FVG that was broken
        direction: LONG or SHORT
        sl_type: Type of SL placement
    
    Returns:
        Stop loss price
    """
    if sl_type == SLType.FVG:
        # SL at FVG boundary
        if direction == Direction.LONG:
            return fvg.bottom
        else:  # SHORT
            return fvg.top
    
    elif sl_type == SLType.RETRACEMENT:
        # 100% retracement of candle + 1 point
        candle_range = candle.high - candle.low
        if direction == Direction.LONG:
            # For LONG: SL at low - 1 point (100% retracement below)
            return candle.low - 1
        else:  # SHORT
            # For SHORT: SL at high + 1 point (100% retracement above)
            return candle.high + 1
    
    else:  # SLType.WICK
        # SL at the wick of the candle
        if direction == Direction.LONG:
            # For LONG: SL below the wick (low of candle)
            return candle.low
        else:  # SHORT
            # For SHORT: SL above the wick (high of candle)
            return candle.high


def find_entry_confirmation(candles: list[Candle], m5_fvg: FVG, 
                            direction: Direction, start_index: int, sl_type: SLType,
                            max_candles: int = MAX_CANDLES_FOR_ENTRY_CONFIRMATION) -> Optional[Tuple[int, float, float, float, SLType]]:
    """
    Find entry confirmation on 5m timeframe.
    
    For SHORT: Wait for price to close BELOW the bullish 5-min FVG
    For LONG: Wait for price to close ABOVE the bearish 5-min FVG
    
    SL Types:
    - FVG: Below/above the broken FVG
    - RETRACEMENT: 100% retracement of candle + 1 point
    - WICK: Below/above the wick of entry candle
    
    Returns: (candle_index, entry_price, stop_loss, take_profit, sl_type)
    """
    for i in range(start_index, min(start_index + max_candles, len(candles))):
        candle = candles[i]
        
        if direction == Direction.SHORT:
            # Wait for close below bullish FVG bottom
            if candle.close < m5_fvg.bottom:
                entry_price = candle.close
                stop_loss = calculate_stop_loss(candle, m5_fvg, direction, sl_type)
                # TP with RR 1:1
                risk = stop_loss - entry_price
                take_profit = entry_price - risk
                return i, entry_price, stop_loss, take_profit, sl_type
        else:  # LONG
            # Wait for close above bearish FVG top
            if candle.close > m5_fvg.top:
                entry_price = candle.close
                stop_loss = calculate_stop_loss(candle, m5_fvg, direction, sl_type)
                # TP with RR 1:1
                risk = entry_price - stop_loss
                take_profit = entry_price + risk
                return i, entry_price, stop_loss, take_profit, sl_type
    
    return None


def simulate_trade(setup: TradingSetup, candles: list[Candle], entry_candle_index: int) -> TradingSetup:
    """
    Simulate a trade by checking if SL or TP is hit first after entry.
    
    Args:
        setup: The trading setup to simulate
        candles: List of candles to check (should be same timeframe as entry)
        entry_candle_index: Index of the entry candle in the candles list
    
    Returns:
        Updated TradingSetup with result (WIN/LOSS) and exit_datetime
    """
    # Look at candles after entry to see if SL or TP is hit first
    for i in range(entry_candle_index + 1, len(candles)):
        candle = candles[i]
        
        if setup.direction == Direction.LONG:
            # For LONG: Check if high hits TP or low hits SL
            if candle.low <= setup.stop_loss:
                # SL hit first (or same candle) - LOSS
                return TradingSetup(
                    entry_datetime=setup.entry_datetime,
                    direction=setup.direction,
                    h4_h1_fvg=setup.h4_h1_fvg,
                    m5_fvg=setup.m5_fvg,
                    entry_price=setup.entry_price,
                    stop_loss=setup.stop_loss,
                    take_profit=setup.take_profit,
                    sl_type=setup.sl_type,
                    result=TradeResult.LOSS,
                    exit_datetime=candle.datetime
                )
            elif candle.high >= setup.take_profit:
                # TP hit - WIN
                return TradingSetup(
                    entry_datetime=setup.entry_datetime,
                    direction=setup.direction,
                    h4_h1_fvg=setup.h4_h1_fvg,
                    m5_fvg=setup.m5_fvg,
                    entry_price=setup.entry_price,
                    stop_loss=setup.stop_loss,
                    take_profit=setup.take_profit,
                    sl_type=setup.sl_type,
                    result=TradeResult.WIN,
                    exit_datetime=candle.datetime
                )
        else:  # SHORT
            # For SHORT: Check if low hits TP or high hits SL
            if candle.high >= setup.stop_loss:
                # SL hit first - LOSS
                return TradingSetup(
                    entry_datetime=setup.entry_datetime,
                    direction=setup.direction,
                    h4_h1_fvg=setup.h4_h1_fvg,
                    m5_fvg=setup.m5_fvg,
                    entry_price=setup.entry_price,
                    stop_loss=setup.stop_loss,
                    take_profit=setup.take_profit,
                    sl_type=setup.sl_type,
                    result=TradeResult.LOSS,
                    exit_datetime=candle.datetime
                )
            elif candle.low <= setup.take_profit:
                # TP hit - WIN
                return TradingSetup(
                    entry_datetime=setup.entry_datetime,
                    direction=setup.direction,
                    h4_h1_fvg=setup.h4_h1_fvg,
                    m5_fvg=setup.m5_fvg,
                    entry_price=setup.entry_price,
                    stop_loss=setup.stop_loss,
                    take_profit=setup.take_profit,
                    sl_type=setup.sl_type,
                    result=TradeResult.WIN,
                    exit_datetime=candle.datetime
                )
    
    # Trade still pending (no SL or TP hit yet)
    return setup


def detect_setups(h4_candles: list[Candle], h1_candles: list[Candle],
                  m15_candles: list[Candle], m5_candles: list[Candle], 
                  sl_type: SLType = SLType.FVG) -> list[TradingSetup]:
    """
    Implement the 3-step trading methodology to detect valid setups.
    
    Args:
        sl_type: Type of stop loss placement (FVG, RETRACEMENT, or WICK)
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
    
    # Detect FVGs on 5-minute timeframe for Step 2 (changed from 15m to 5m)
    m5_fvgs = detect_fvg(m5_candles)
    
    # Process each context FVG
    for ctx_fvg, source_candles in context_fvgs_with_candles:
        if ctx_fvg.fill_candle_index < 0:
            continue
        
        # Determine direction based on FVG type
        # Bullish FVG filled by wick only -> price retraced DOWN into FVG (liquidity sweep) -> LONG
        # Bearish FVG filled by wick only -> price retraced UP into FVG (liquidity sweep) -> SHORT
        direction = Direction.LONG if ctx_fvg.is_bullish else Direction.SHORT
        
        # Get the actual fill datetime from the fill candle
        fill_datetime = source_candles[ctx_fvg.fill_candle_index].datetime
        
        # Find a 5m FVG near the context fill (changed from 15m to 5m)
        m5_fvg = find_m5_fvg_near_datetime(m5_fvgs, fill_datetime, direction)
        
        if m5_fvg is None:
            continue
        
        # Step 3: Find entry confirmation on 5m timeframe
        # Find the starting index in m5 candles after the FVG
        start_idx = m5_fvg.candle_index + 2
        
        entry_result = find_entry_confirmation(m5_candles, m5_fvg, direction, start_idx, sl_type)
        
        if entry_result:
            entry_idx, entry_price, stop_loss, take_profit, used_sl_type = entry_result
            entry_datetime = m5_candles[entry_idx].datetime
            
            # Check if within Chicago time range
            if is_within_chicago_time_range(entry_datetime):
                setup = TradingSetup(
                    entry_datetime=entry_datetime,
                    direction=direction,
                    h4_h1_fvg=ctx_fvg,
                    m5_fvg=m5_fvg,
                    entry_price=entry_price,
                    stop_loss=stop_loss,
                    take_profit=take_profit,
                    sl_type=used_sl_type
                )
                # Simulate the trade to get result
                simulated_setup = simulate_trade(setup, m5_candles, entry_idx)
                setups.append(simulated_setup)
    
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


def run_analysis_for_sl_type(sl_type: SLType, base_path: str, years: range) -> dict:
    """Run analysis for a specific SL type and return results."""
    all_setups = []
    yearly_setups = {}
    
    for year in years:
        try:
            h4_candles, h1_candles, m15_candles, m5_candles = load_yearly_data(base_path, year)
            
            if (len(h4_candles) == 0 or len(h1_candles) == 0 or 
                len(m15_candles) == 0 or len(m5_candles) == 0):
                continue
            
            year_setups = detect_setups(h4_candles, h1_candles, m15_candles, m5_candles, sl_type)
            
            year_count = len(year_setups)
            year_longs = sum(1 for s in year_setups if s.direction == Direction.LONG)
            year_shorts = sum(1 for s in year_setups if s.direction == Direction.SHORT)
            year_wins = sum(1 for s in year_setups if s.result == TradeResult.WIN)
            year_losses = sum(1 for s in year_setups if s.result == TradeResult.LOSS)
            
            yearly_setups[year] = {
                'total': year_count,
                'long': year_longs,
                'short': year_shorts,
                'wins': year_wins,
                'losses': year_losses
            }
            
            all_setups.extend(year_setups)
            
        except Exception:
            continue
    
    # Calculate statistics
    total_wins = sum(1 for s in all_setups if s.result == TradeResult.WIN)
    total_losses = sum(1 for s in all_setups if s.result == TradeResult.LOSS)
    completed_trades = total_wins + total_losses
    overall_winrate = (total_wins / completed_trades * 100) if completed_trades > 0 else 0
    
    long_trades = [s for s in all_setups if s.direction == Direction.LONG]
    short_trades = [s for s in all_setups if s.direction == Direction.SHORT]
    
    long_wins = sum(1 for s in long_trades if s.result == TradeResult.WIN)
    long_losses = sum(1 for s in long_trades if s.result == TradeResult.LOSS)
    long_completed = long_wins + long_losses
    long_winrate = (long_wins / long_completed * 100) if long_completed > 0 else 0
    
    short_wins = sum(1 for s in short_trades if s.result == TradeResult.WIN)
    short_losses = sum(1 for s in short_trades if s.result == TradeResult.LOSS)
    short_completed = short_wins + short_losses
    short_winrate = (short_wins / short_completed * 100) if short_completed > 0 else 0
    
    return {
        'sl_type': sl_type,
        'all_setups': all_setups,
        'yearly_setups': yearly_setups,
        'total_trades': len(all_setups),
        'completed': completed_trades,
        'wins': total_wins,
        'losses': total_losses,
        'winrate': overall_winrate,
        'long_trades': len(long_trades),
        'long_wins': long_wins,
        'long_winrate': long_winrate,
        'short_trades': len(short_trades),
        'short_wins': short_wins,
        'short_winrate': short_winrate
    }


def main():
    """Main entry point."""
    base_path = os.path.dirname(os.path.abspath(__file__))
    years = range(2018, 2026)  # 2018 through 2025
    
    print("=" * 70)
    print("Trading Setup Detection System - 5-minute FVG Analysis")
    print("=" * 70)
    print()
    print("Processing data for years 2018-2025...")
    print("Filtering setups between 2:00 and 12:00 Chicago time")
    print("Using 5-minute FVG (instead of 15-minute)")
    print()
    
    # Run analysis for all three SL types
    sl_types = [SLType.FVG, SLType.RETRACEMENT, SLType.WICK]
    results = {}
    
    for sl_type in sl_types:
        print(f"Analyzing with SL Type: {sl_type.value}...", end=" ")
        results[sl_type] = run_analysis_for_sl_type(sl_type, base_path, years)
        print(f"Found {results[sl_type]['total_trades']} trades")
    
    print()
    print("=" * 70)
    print("COMPARISON OF SL TYPES")
    print("=" * 70)
    print()
    
    # Print comparison table
    print(f"{'SL Type':<15} {'Trades':>8} {'Wins':>8} {'Losses':>8} {'Win Rate':>10} {'LONG WR':>10} {'SHORT WR':>10}")
    print("-" * 70)
    
    for sl_type in sl_types:
        r = results[sl_type]
        print(f"{sl_type.value:<15} {r['total_trades']:>8} {r['wins']:>8} {r['losses']:>8} "
              f"{r['winrate']:>9.1f}% {r['long_winrate']:>9.1f}% {r['short_winrate']:>9.1f}%")
    
    print()
    
    # Detailed analysis for each SL type
    for sl_type in sl_types:
        r = results[sl_type]
        print()
        print("=" * 70)
        print(f"DETAILED ANALYSIS - SL Type: {sl_type.value}")
        print("=" * 70)
        
        if sl_type == SLType.FVG:
            print("SL: Below/above the broken FVG")
        elif sl_type == SLType.RETRACEMENT:
            print("SL: 100% retracement of candle + 1 point")
        else:
            print("SL: Below/above the wick of entry candle")
        
        print()
        print("OVERALL PERFORMANCE:")
        print("-" * 40)
        print(f"  Total Trades:    {r['total_trades']}")
        print(f"  Completed:       {r['completed']}")
        print(f"  Wins:            {r['wins']}")
        print(f"  Losses:          {r['losses']}")
        print(f"  WIN RATE:        {r['winrate']:.1f}%")
        print()
        
        print("BY DIRECTION:")
        print("-" * 40)
        print(f"  LONG Trades:     {r['long_trades']}")
        print(f"    Win Rate:      {r['long_winrate']:.1f}%")
        print(f"  SHORT Trades:    {r['short_trades']}")
        print(f"    Win Rate:      {r['short_winrate']:.1f}%")
        print()
        
        print("YEARLY WIN RATES:")
        print("-" * 40)
        for year in sorted(r['yearly_setups'].keys()):
            stats = r['yearly_setups'][year]
            completed = stats['wins'] + stats['losses']
            wr = (stats['wins'] / completed * 100) if completed > 0 else 0
            print(f"  {year}: {wr:5.1f}% ({stats['wins']} wins / {completed} trades)")
        
        # Print sample setups
        if r['all_setups']:
            print()
            print("Sample Setups (first 3):")
            print("-" * 40)
            for setup in r['all_setups'][:3]:
                result_str = setup.result.value if setup.result != TradeResult.PENDING else "PENDING"
                print(f"  {setup.entry_datetime.strftime('%Y-%m-%d %H:%M')} - "
                      f"{setup.direction.value} @ {setup.entry_price:.2f} [{result_str}]")
                print(f"    SL: {setup.stop_loss:.2f} | TP: {setup.take_profit:.2f} (RR 1:1)")
                print(f"    H4/H1 FVG: {'Bullish' if setup.h4_h1_fvg.is_bullish else 'Bearish'} "
                      f"at {setup.h4_h1_fvg.datetime.strftime('%Y-%m-%d %H:%M')}")
                print(f"    5m FVG: {'Bullish' if setup.m5_fvg.is_bullish else 'Bearish'} "
                      f"at {setup.m5_fvg.datetime.strftime('%Y-%m-%d %H:%M')}")
                print()
    
    return results


if __name__ == "__main__":
    main()

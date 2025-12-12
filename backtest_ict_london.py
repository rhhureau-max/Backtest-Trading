"""
ICT London Session Backtesting Script

This module provides a professional-grade backtesting framework for the ICT London
Session trading strategy on Nasdaq 100 (NQ) futures data.

Strategy Components:
1. London Silver Bullet (02:00-03:00 AM Chicago Time / 09:00-10:00 Paris Time)
2. 10AM Paris Continuation (03:00-04:00 AM Chicago Time / 10:00-11:00 Paris Time)

Data Requirements:
- 1m or 5m execution timeframe CSV files
- 1H and 4H timeframe CSV files for trend bias

Usage:
    python backtest_ict_london.py

Configuration:
    Modify the DATA_PATH and YEARS variables in the config section below.
"""

import os
import zipfile
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, time, timedelta
from typing import Optional, Tuple, List, Dict, Any
from dataclasses import dataclass, field
from backtesting import Backtest, Strategy
import warnings

warnings.filterwarnings('ignore')


# =============================================================================
# CONFIGURATION SECTION
# =============================================================================

# Path to the data files - modify this to point to your local data directory
DATA_PATH = "/home/runner/work/Backtest-Trading/Backtest-Trading"

# Years to include in the backtest
# Note: Adjust this list based on available data. Years with incomplete data
# (e.g., current year) will use whatever data is available.
YEARS = [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]

# Execution timeframe: '1m' or '5m'
EXECUTION_TIMEFRAME = '5m'

# Initial capital for backtesting
INITIAL_CAPITAL = 100000

# Position size (NQ futures micro contract = $2 per point)
CONTRACT_MULTIPLIER = 2  # $2 per point for Micro NQ

# Risk per trade as percentage of capital
RISK_PER_TRADE_PCT = 0.01  # 1% risk per trade

# =============================================================================
# DATA CLASSES
# =============================================================================


@dataclass
class TradeLog:
    """Data class to store individual trade information."""
    entry_time: datetime
    exit_time: Optional[datetime] = None
    direction: str = ""  # 'LONG' or 'SHORT'
    entry_price: float = 0.0
    exit_price: Optional[float] = None
    stop_loss: float = 0.0
    take_profit: float = 0.0
    pnl: float = 0.0
    pnl_pct: float = 0.0
    trade_duration: Optional[timedelta] = None
    setup_type: str = ""  # 'SILVER_BULLET' or 'OTE_CONTINUATION'
    notes: str = ""


@dataclass
class FairValueGap:
    """Data class to represent a Fair Value Gap."""
    start_time: datetime
    fvg_high: float
    fvg_low: float
    direction: str  # 'BULLISH' or 'BEARISH'
    displacement_candle_idx: int


@dataclass 
class LiquiditySweep:
    """Data class to represent a liquidity sweep event."""
    time: datetime
    direction: str  # 'BULLISH' (swept low) or 'BEARISH' (swept high)
    swept_level: float
    price: float


@dataclass
class PendingEntry:
    """Data class to represent a pending limit order entry."""
    direction: str  # 'LONG' or 'SHORT'
    entry_price: float
    stop_loss: float
    take_profit: float
    setup_time: datetime
    setup_type: str  # 'SILVER_BULLET' or 'OTE_CONTINUATION'
    fvg_high: Optional[float] = None
    fvg_low: Optional[float] = None


# =============================================================================
# DATA LOADING FUNCTIONS
# =============================================================================


def load_csv_file(filepath: str) -> pd.DataFrame:
    """
    Load a single CSV file with semicolon separator.
    
    Args:
        filepath: Path to the CSV file
        
    Returns:
        DataFrame with datetime index and OHLCV columns
    """
    df = pd.read_csv(
        filepath, 
        sep=';',
        names=['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume'],
        skiprows=1,  # Skip header row
        encoding='utf-8-sig'  # Handle BOM in some files
    )
    
    # Combine date and time into datetime
    # Use dayfirst=True since format appears to be DD/MM/YYYY in some files
    df['DateTime'] = pd.to_datetime(
        df['Date'] + ' ' + df['Time'], 
        dayfirst=True,
        format='mixed'
    )
    df.set_index('DateTime', inplace=True)
    
    # Keep only OHLCV columns
    df = df[['Open', 'High', 'Low', 'Close', 'Volume']].copy()
    
    # Convert to numeric
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    df.dropna(inplace=True)
    
    return df


def load_zipped_csv(filepath: str) -> pd.DataFrame:
    """
    Load a CSV file from a ZIP archive.
    
    Args:
        filepath: Path to the ZIP file
        
    Returns:
        DataFrame with datetime index and OHLCV columns
    """
    with zipfile.ZipFile(filepath, 'r') as z:
        # Get the first CSV file in the archive
        csv_name = [n for n in z.namelist() if n.endswith('.csv')][0]
        with z.open(csv_name) as f:
            df = pd.read_csv(
                f,
                sep=';',
                names=['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume'],
                skiprows=1,
                encoding='utf-8-sig'
            )
    
    df['DateTime'] = pd.to_datetime(
        df['Date'] + ' ' + df['Time'], 
        dayfirst=True,
        format='mixed'
    )
    df.set_index('DateTime', inplace=True)
    df = df[['Open', 'High', 'Low', 'Close', 'Volume']].copy()
    
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    df.dropna(inplace=True)
    
    return df


def load_multi_year_data(
    data_path: str, 
    years: List[int], 
    timeframe: str
) -> pd.DataFrame:
    """
    Load and concatenate data from multiple years for a specific timeframe.
    
    Args:
        data_path: Base path to data files
        years: List of years to load
        timeframe: Timeframe string ('1m', '5m', '1H', '4H', '1D', '15m')
        
    Returns:
        Concatenated DataFrame sorted by datetime index
    """
    all_data = []
    
    for year in years:
        # Try regular CSV first
        csv_path = os.path.join(data_path, f"{year} {timeframe}.csv")
        zip_path = os.path.join(data_path, f"{year} {timeframe}.csv.zip")
        
        if os.path.exists(csv_path):
            print(f"Loading {csv_path}...")
            df = load_csv_file(csv_path)
            all_data.append(df)
        elif os.path.exists(zip_path):
            print(f"Loading {zip_path}...")
            df = load_zipped_csv(zip_path)
            all_data.append(df)
        else:
            print(f"Warning: No data file found for {year} {timeframe}")
    
    if not all_data:
        raise ValueError(f"No data files found for timeframe {timeframe}")
    
    combined = pd.concat(all_data).sort_index()
    combined = combined[~combined.index.duplicated(keep='first')]
    
    print(f"Loaded {len(combined)} bars for {timeframe} timeframe")
    return combined


# =============================================================================
# TECHNICAL INDICATOR FUNCTIONS
# =============================================================================


def calculate_ema(series: pd.Series, period: int) -> pd.Series:
    """Calculate Exponential Moving Average."""
    return series.ewm(span=period, adjust=False).mean()


def calculate_atr(df: pd.DataFrame, period: int = 14) -> pd.Series:
    """Calculate Average True Range."""
    high = df['High']
    low = df['Low']
    close = df['Close']
    
    tr1 = high - low
    tr2 = abs(high - close.shift(1))
    tr3 = abs(low - close.shift(1))
    
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    atr = tr.rolling(window=period).mean()
    
    return atr


def find_fractal_highs(df: pd.DataFrame, lookback: int = 5) -> pd.Series:
    """
    Identify fractal highs (local maxima).
    
    A fractal high is a bar where the high is higher than the highs
    of the 'lookback' bars on both sides.
    """
    high = df['High']
    fractal_high = pd.Series(index=df.index, dtype=float)
    
    for i in range(lookback, len(df) - lookback):
        is_fractal = True
        current_high = high.iloc[i]
        
        for j in range(1, lookback + 1):
            if high.iloc[i - j] >= current_high or high.iloc[i + j] >= current_high:
                is_fractal = False
                break
        
        if is_fractal:
            fractal_high.iloc[i] = current_high
    
    return fractal_high


def find_fractal_lows(df: pd.DataFrame, lookback: int = 5) -> pd.Series:
    """
    Identify fractal lows (local minima).
    
    A fractal low is a bar where the low is lower than the lows
    of the 'lookback' bars on both sides.
    """
    low = df['Low']
    fractal_low = pd.Series(index=df.index, dtype=float)
    
    for i in range(lookback, len(df) - lookback):
        is_fractal = True
        current_low = low.iloc[i]
        
        for j in range(1, lookback + 1):
            if low.iloc[i - j] <= current_low or low.iloc[i + j] <= current_low:
                is_fractal = False
                break
        
        if is_fractal:
            fractal_low.iloc[i] = current_low
    
    return fractal_low


def detect_fair_value_gaps(
    df: pd.DataFrame, 
    atr: pd.Series, 
    displacement_threshold: float = 2.0
) -> List[FairValueGap]:
    """
    Detect Fair Value Gaps formed by displacement candles.
    
    A displacement candle has a body size > displacement_threshold * ATR.
    An FVG forms when there's a gap between candle 1's low/high and candle 3's high/low.
    
    Args:
        df: OHLCV DataFrame
        atr: ATR series
        displacement_threshold: Multiplier for ATR to identify displacement
        
    Returns:
        List of FairValueGap objects
    """
    fvgs = []
    
    for i in range(2, len(df)):
        body_size = abs(df['Close'].iloc[i-1] - df['Open'].iloc[i-1])
        
        if atr.iloc[i-1] > 0 and body_size > displacement_threshold * atr.iloc[i-1]:
            # Bullish displacement - FVG between candle 1 high and candle 3 low
            if df['Close'].iloc[i-1] > df['Open'].iloc[i-1]:  # Bullish candle
                fvg_low = df['High'].iloc[i-2]  # Candle 1 high
                fvg_high = df['Low'].iloc[i]    # Candle 3 low
                
                if fvg_high > fvg_low:  # Valid gap
                    fvgs.append(FairValueGap(
                        start_time=df.index[i],
                        fvg_high=fvg_high,
                        fvg_low=fvg_low,
                        direction='BULLISH',
                        displacement_candle_idx=i-1
                    ))
            
            # Bearish displacement - FVG between candle 1 low and candle 3 high
            else:  # Bearish candle
                fvg_high = df['Low'].iloc[i-2]   # Candle 1 low
                fvg_low = df['High'].iloc[i]     # Candle 3 high
                
                if fvg_high > fvg_low:  # Valid gap
                    fvgs.append(FairValueGap(
                        start_time=df.index[i],
                        fvg_high=fvg_high,
                        fvg_low=fvg_low,
                        direction='BEARISH',
                        displacement_candle_idx=i-1
                    ))
    
    return fvgs


def detect_liquidity_sweep(
    df: pd.DataFrame,
    fractal_highs: pd.Series,
    fractal_lows: pd.Series,
    current_idx: int,
    lookback_bars: int = 50
) -> Optional[LiquiditySweep]:
    """
    Detect if price has swept a recent fractal high or low.
    
    Args:
        df: OHLCV DataFrame
        fractal_highs: Series of fractal high levels
        fractal_lows: Series of fractal low levels
        current_idx: Current bar index
        lookback_bars: How many bars to look back for fractals
        
    Returns:
        LiquiditySweep object if detected, None otherwise
    """
    if current_idx < lookback_bars:
        return None
    
    current_high = df['High'].iloc[current_idx]
    current_low = df['Low'].iloc[current_idx]
    current_close = df['Close'].iloc[current_idx]
    
    # Check for bearish sweep (price breaks above fractal high then closes below)
    for i in range(current_idx - lookback_bars, current_idx):
        if pd.notna(fractal_highs.iloc[i]):
            frac_high = fractal_highs.iloc[i]
            if current_high > frac_high and current_close < frac_high:
                return LiquiditySweep(
                    time=df.index[current_idx],
                    direction='BEARISH',
                    swept_level=frac_high,
                    price=current_close
                )
    
    # Check for bullish sweep (price breaks below fractal low then closes above)
    for i in range(current_idx - lookback_bars, current_idx):
        if pd.notna(fractal_lows.iloc[i]):
            frac_low = fractal_lows.iloc[i]
            if current_low < frac_low and current_close > frac_low:
                return LiquiditySweep(
                    time=df.index[current_idx],
                    direction='BULLISH',
                    swept_level=frac_low,
                    price=current_close
                )
    
    return None


def get_swing_high(df: pd.DataFrame, start_idx: int, lookback: int = 10) -> float:
    """Get the highest high in the lookback period."""
    start = max(0, start_idx - lookback)
    return df['High'].iloc[start:start_idx + 1].max()


def get_swing_low(df: pd.DataFrame, start_idx: int, lookback: int = 10) -> float:
    """Get the lowest low in the lookback period."""
    start = max(0, start_idx - lookback)
    return df['Low'].iloc[start:start_idx + 1].min()


def calculate_ote_level(high: float, low: float, direction: str) -> float:
    """
    Calculate Optimal Trade Entry (OTE) level at 62% Fibonacci retracement.
    
    Args:
        high: Range high
        low: Range low
        direction: 'LONG' or 'SHORT'
        
    Returns:
        OTE price level
    """
    range_size = high - low
    if direction == 'LONG':
        # For longs, OTE is 62% retracement from high to low
        return high - (range_size * 0.618)
    else:
        # For shorts, OTE is 62% retracement from low to high
        return low + (range_size * 0.618)


# =============================================================================
# HIGHER TIMEFRAME ANALYSIS
# =============================================================================


def get_h4_bias(h4_data: pd.DataFrame, current_time: datetime, ema_period: int = 20) -> str:
    """
    Determine H4 trend bias based on EMA(20).
    
    Args:
        h4_data: H4 timeframe DataFrame
        current_time: Current execution bar time
        ema_period: EMA period (default 20)
        
    Returns:
        'BULLISH', 'BEARISH', or 'NEUTRAL'
    """
    # Get H4 data up to current time
    h4_filtered = h4_data[h4_data.index <= current_time]
    
    if len(h4_filtered) < ema_period:
        return 'NEUTRAL'
    
    ema20 = calculate_ema(h4_filtered['Close'], ema_period)
    
    last_close = h4_filtered['Close'].iloc[-1]
    last_ema = ema20.iloc[-1]
    
    if last_close > last_ema:
        return 'BULLISH'
    elif last_close < last_ema:
        return 'BEARISH'
    else:
        return 'NEUTRAL'


def get_h1_liquidity_pool(
    h1_data: pd.DataFrame, 
    current_time: datetime, 
    direction: str,
    lookback_bars: int = 24
) -> Optional[float]:
    """
    Find the next H1 liquidity pool (fractal high/low) for take profit targeting.
    
    Args:
        h1_data: H1 timeframe DataFrame
        current_time: Current execution bar time
        direction: 'LONG' or 'SHORT'
        lookback_bars: Number of H1 bars to look back
        
    Returns:
        Liquidity pool price level or None
    """
    h1_filtered = h1_data[h1_data.index <= current_time]
    
    if len(h1_filtered) < lookback_bars:
        return None
    
    recent_h1 = h1_filtered.tail(lookback_bars)
    
    if direction == 'LONG':
        # Look for fractal high as target
        fractal_highs = find_fractal_highs(recent_h1, lookback=3)
        valid_levels = fractal_highs.dropna()
        if len(valid_levels) > 0:
            return valid_levels.iloc[-1]
    else:
        # Look for fractal low as target
        fractal_lows = find_fractal_lows(recent_h1, lookback=3)
        valid_levels = fractal_lows.dropna()
        if len(valid_levels) > 0:
            return valid_levels.iloc[-1]
    
    return None


# =============================================================================
# ICT LONDON SESSION STRATEGY
# =============================================================================


class ICTLondonStrategy(Strategy):
    """
    ICT London Session Trading Strategy Implementation.
    
    This strategy implements:
    1. London Silver Bullet (02:00-03:00 AM Chicago)
    2. 10AM Paris Continuation (03:00-04:00 AM Chicago)
    
    Features:
    - H4 EMA(20) trend filter
    - Liquidity sweep detection
    - Fair Value Gap entries
    - OTE (62% retracement) entries
    - Fixed 2R take profit or H1 liquidity targeting
    - No trade zone after 04:30 AM Chicago
    """
    
    # Strategy parameters
    ema_period = 20
    atr_period = 14
    displacement_multiplier = 2.0
    fractal_lookback = 5
    swing_lookback = 10
    risk_reward = 2.0
    tick_buffer = 0.25  # 1 tick for NQ
    
    # External data references (set before running)
    h4_data = None
    h1_data = None
    
    def init(self):
        """Initialize strategy indicators."""
        # Calculate ATR on execution timeframe
        self.atr = self.I(calculate_atr, self.data.df, self.atr_period)
        
        # Calculate fractal levels
        self.fractal_highs = self.I(
            find_fractal_highs, 
            self.data.df, 
            self.fractal_lookback,
            overlay=True
        )
        self.fractal_lows = self.I(
            find_fractal_lows, 
            self.data.df, 
            self.fractal_lookback,
            overlay=True
        )
        
        # Trade tracking
        self.trade_logs: List[TradeLog] = []
        self.pending_fvg_entries: List[PendingEntry] = []
        self.pending_ote_entries: List[PendingEntry] = []
        
        # Session tracking
        self.silver_bullet_active = False
        self.ote_active = False
        self.liquidity_swept = False
        self.displacement_detected = False
        
        # Range tracking for OTE
        self.range_high = None
        self.range_low = None
        self.range_direction = None
    
    def _is_london_silver_bullet_time(self, dt: datetime) -> bool:
        """Check if current time is in Silver Bullet window (02:00-03:00 Chicago)."""
        t = dt.time()
        return time(2, 0) <= t < time(3, 0)
    
    def _is_ote_continuation_time(self, dt: datetime) -> bool:
        """Check if current time is in OTE Continuation window (03:00-04:00 Chicago)."""
        t = dt.time()
        return time(3, 0) <= t < time(4, 0)
    
    def _is_no_trade_zone(self, dt: datetime) -> bool:
        """Check if current time is in no-trade zone (after 04:30 Chicago)."""
        t = dt.time()
        return t >= time(4, 30)
    
    def _is_pre_london_session(self, dt: datetime) -> bool:
        """Check if current time is pre-London session (00:00-02:00 Chicago)."""
        t = dt.time()
        return time(0, 0) <= t < time(2, 0)
    
    def _get_h4_bias(self) -> str:
        """Get H4 trend bias at current bar."""
        if self.h4_data is None:
            return 'NEUTRAL'
        
        current_time = self.data.index[-1]
        return get_h4_bias(self.h4_data, current_time, self.ema_period)
    
    def _check_silver_bullet_setup(self):
        """
        Check for London Silver Bullet setup conditions.
        
        Requirements:
        1. Liquidity sweep detected
        2. Displacement candle (Body > 2x ATR)
        3. Fair Value Gap formed
        """
        idx = len(self.data) - 1
        if idx < 10:
            return
        
        current_time = self.data.index[-1]
        h4_bias = self._get_h4_bias()
        
        # Check for liquidity sweep
        sweep = detect_liquidity_sweep(
            self.data.df,
            pd.Series(self.fractal_highs, index=self.data.df.index),
            pd.Series(self.fractal_lows, index=self.data.df.index),
            idx,
            lookback_bars=50
        )
        
        if sweep is None:
            return
        
        # Verify sweep direction matches H4 bias
        if sweep.direction == 'BULLISH' and h4_bias != 'BULLISH':
            return
        if sweep.direction == 'BEARISH' and h4_bias != 'BEARISH':
            return
        
        # Check for displacement and FVG
        body_size = abs(self.data.Close[-1] - self.data.Open[-1])
        current_atr = self.atr[-1]
        
        if current_atr > 0 and body_size > self.displacement_multiplier * current_atr:
            # Displacement detected, look for FVG
            if len(self.data) >= 3:
                # Check for bullish FVG
                if sweep.direction == 'BULLISH':
                    fvg_low = self.data.High[-3]
                    fvg_high = self.data.Low[-1]
                    
                    if fvg_high > fvg_low:
                        # Valid bullish FVG - create entry
                        entry_price = fvg_low + self.tick_buffer
                        stop_loss = get_swing_low(
                            self.data.df, idx, self.swing_lookback
                        ) - self.tick_buffer
                        
                        # Validate: SL must be below entry for longs
                        if stop_loss >= entry_price:
                            return
                        
                        risk = entry_price - stop_loss
                        if risk <= 0:
                            return
                        
                        take_profit = entry_price + (risk * self.risk_reward)
                        
                        self.pending_fvg_entries.append(PendingEntry(
                            direction='LONG',
                            entry_price=entry_price,
                            stop_loss=stop_loss,
                            take_profit=take_profit,
                            fvg_high=fvg_high,
                            fvg_low=fvg_low,
                            setup_time=current_time,
                            setup_type='SILVER_BULLET'
                        ))
                
                # Check for bearish FVG
                elif sweep.direction == 'BEARISH':
                    fvg_high = self.data.Low[-3]
                    fvg_low = self.data.High[-1]
                    
                    if fvg_high > fvg_low:
                        # Valid bearish FVG - create entry
                        entry_price = fvg_high - self.tick_buffer
                        stop_loss = get_swing_high(
                            self.data.df, idx, self.swing_lookback
                        ) + self.tick_buffer
                        
                        # Validate: SL must be above entry for shorts
                        if stop_loss <= entry_price:
                            return
                        
                        risk = stop_loss - entry_price
                        if risk <= 0:
                            return
                        
                        take_profit = entry_price - (risk * self.risk_reward)
                        
                        self.pending_fvg_entries.append(PendingEntry(
                            direction='SHORT',
                            entry_price=entry_price,
                            stop_loss=stop_loss,
                            take_profit=take_profit,
                            fvg_high=fvg_high,
                            fvg_low=fvg_low,
                            setup_time=current_time,
                            setup_type='SILVER_BULLET'
                        ))
    
    def _track_silver_bullet_range(self):
        """Track the 02:00-03:00 range for OTE continuation."""
        idx = len(self.data) - 1
        current_time = self.data.index[-1]
        
        if self._is_london_silver_bullet_time(current_time):
            current_high = self.data.High[-1]
            current_low = self.data.Low[-1]
            
            if self.range_high is None or current_high > self.range_high:
                self.range_high = current_high
            if self.range_low is None or current_low < self.range_low:
                self.range_low = current_low
    
    def _check_ote_continuation_setup(self):
        """
        Check for OTE Continuation setup at 03:00-04:00 Chicago.
        
        If 02:00-03:00 range was bullish, place OTE limit buy at 62% retracement.
        """
        if self.range_high is None or self.range_low is None:
            return
        
        current_time = self.data.index[-1]
        h4_bias = self._get_h4_bias()
        
        # Determine range direction
        # Use close of 03:00 bar vs open of 02:00 bar
        range_close = self.data.Close[-1]
        
        # Check if range was bullish
        mid_point = (self.range_high + self.range_low) / 2
        
        if range_close > mid_point and h4_bias == 'BULLISH':
            # Bullish range - place OTE buy at 62% retracement
            ote_level = calculate_ote_level(
                self.range_high, self.range_low, 'LONG'
            )
            
            stop_loss = self.range_low - self.tick_buffer
            
            # Validate: SL must be below entry for longs
            if stop_loss >= ote_level:
                return
            
            risk = ote_level - stop_loss
            if risk <= 0:
                return
            
            take_profit = ote_level + (risk * self.risk_reward)
            
            self.pending_ote_entries.append(PendingEntry(
                direction='LONG',
                entry_price=ote_level,
                stop_loss=stop_loss,
                take_profit=take_profit,
                setup_time=current_time,
                setup_type='OTE_CONTINUATION'
            ))
        
        elif range_close < mid_point and h4_bias == 'BEARISH':
            # Bearish range - place OTE sell at 62% retracement
            ote_level = calculate_ote_level(
                self.range_high, self.range_low, 'SHORT'
            )
            
            stop_loss = self.range_high + self.tick_buffer
            
            # Validate: SL must be above entry for shorts
            if stop_loss <= ote_level:
                return
            
            risk = stop_loss - ote_level
            if risk <= 0:
                return
            
            take_profit = ote_level - (risk * self.risk_reward)
            
            self.pending_ote_entries.append(PendingEntry(
                direction='SHORT',
                entry_price=ote_level,
                stop_loss=stop_loss,
                take_profit=take_profit,
                setup_time=current_time,
                setup_type='OTE_CONTINUATION'
            ))
    
    def _check_pending_entries(self):
        """Check if price has reached any pending entry levels."""
        current_low = self.data.Low[-1]
        current_high = self.data.High[-1]
        current_close = self.data.Close[-1]
        current_time = self.data.index[-1]
        
        # Skip if in no trade zone
        if self._is_no_trade_zone(current_time):
            self.pending_fvg_entries.clear()
            self.pending_ote_entries.clear()
            return
        
        # Check FVG entries
        entries_to_remove = []
        for i, entry in enumerate(self.pending_fvg_entries):
            # Check if entry is still valid (within reasonable time)
            time_diff = (current_time - entry.setup_time).total_seconds() / 3600
            if time_diff > 2:  # Expire after 2 hours
                entries_to_remove.append(i)
                continue
            
            if entry.direction == 'LONG':
                # Check if price touched entry level
                if current_low <= entry.entry_price <= current_high:
                    if not self.position:
                        # Validate order: For LONG, SL < entry < TP
                        sl = entry.stop_loss
                        tp = entry.take_profit
                        # Validate that entry price is between SL and TP
                        if sl < entry.entry_price < tp:
                            # Also check current close for order execution validity
                            if sl < current_close < tp:
                                self.buy(sl=sl, tp=tp)
                                self.trade_logs.append(TradeLog(
                                    entry_time=current_time,
                                    direction='LONG',
                                    entry_price=current_close,
                                    stop_loss=sl,
                                    take_profit=tp,
                                    setup_type=entry.setup_type
                                ))
                                entries_to_remove.append(i)
                            # If current close not valid, keep entry for next bar
                        else:
                            # Invalid entry setup, remove it
                            entries_to_remove.append(i)
            
            elif entry.direction == 'SHORT':
                if current_low <= entry.entry_price <= current_high:
                    if not self.position:
                        # Validate order: For SHORT, TP < entry < SL
                        sl = entry.stop_loss
                        tp = entry.take_profit
                        # Validate that entry price is between TP and SL
                        if tp < entry.entry_price < sl:
                            # Also check current close for order execution validity
                            if tp < current_close < sl:
                                self.sell(sl=sl, tp=tp)
                                self.trade_logs.append(TradeLog(
                                    entry_time=current_time,
                                    direction='SHORT',
                                    entry_price=current_close,
                                    stop_loss=sl,
                                    take_profit=tp,
                                    setup_type=entry.setup_type
                                ))
                                entries_to_remove.append(i)
                            # If current close not valid, keep entry for next bar
                        else:
                            # Invalid entry setup, remove it
                            entries_to_remove.append(i)
        
        # Remove processed entries
        for i in sorted(entries_to_remove, reverse=True):
            self.pending_fvg_entries.pop(i)
        
        # Check OTE entries similarly
        entries_to_remove = []
        for i, entry in enumerate(self.pending_ote_entries):
            time_diff = (current_time - entry.setup_time).total_seconds() / 3600
            if time_diff > 1:  # Expire after 1 hour
                entries_to_remove.append(i)
                continue
            
            if entry.direction == 'LONG':
                if current_low <= entry.entry_price <= current_high:
                    if not self.position:
                        sl = entry.stop_loss
                        tp = entry.take_profit
                        # Validate that entry price is between SL and TP
                        if sl < entry.entry_price < tp:
                            if sl < current_close < tp:
                                self.buy(sl=sl, tp=tp)
                                self.trade_logs.append(TradeLog(
                                    entry_time=current_time,
                                    direction='LONG',
                                    entry_price=current_close,
                                    stop_loss=sl,
                                    take_profit=tp,
                                    setup_type=entry.setup_type
                                ))
                                entries_to_remove.append(i)
                            # If current close not valid, keep entry for next bar
                        else:
                            entries_to_remove.append(i)
            
            elif entry.direction == 'SHORT':
                if current_low <= entry.entry_price <= current_high:
                    if not self.position:
                        sl = entry.stop_loss
                        tp = entry.take_profit
                        # Validate that entry price is between TP and SL
                        if tp < entry.entry_price < sl:
                            if tp < current_close < sl:
                                self.sell(sl=sl, tp=tp)
                                self.trade_logs.append(TradeLog(
                                    entry_time=current_time,
                                    direction='SHORT',
                                    entry_price=current_close,
                                    stop_loss=sl,
                                    take_profit=tp,
                                    setup_type=entry.setup_type
                                ))
                                entries_to_remove.append(i)
                            # If current close not valid, keep entry for next bar
                        else:
                            entries_to_remove.append(i)
        
        for i in sorted(entries_to_remove, reverse=True):
            self.pending_ote_entries.pop(i)
    
    def _reset_daily_tracking(self):
        """Reset tracking variables at start of new trading day."""
        current_time = self.data.index[-1]
        prev_time = self.data.index[-2] if len(self.data) > 1 else current_time
        
        # Reset at midnight Chicago time
        if current_time.date() != prev_time.date():
            self.range_high = None
            self.range_low = None
            self.range_direction = None
            self.pending_fvg_entries.clear()
            self.pending_ote_entries.clear()
    
    def next(self):
        """Main strategy logic executed on each bar."""
        if len(self.data) < 10:
            return
        
        current_time = self.data.index[-1]
        
        # Reset at start of new day
        self._reset_daily_tracking()
        
        # Check for no trade zone
        if self._is_no_trade_zone(current_time):
            return
        
        # Track range during Silver Bullet window
        if self._is_london_silver_bullet_time(current_time):
            self._track_silver_bullet_range()
            self._check_silver_bullet_setup()
        
        # Check OTE setup at start of 03:00 hour
        if self._is_ote_continuation_time(current_time):
            # Only check once at the start of 03:00
            prev_time = self.data.index[-2] if len(self.data) > 1 else current_time
            if prev_time.hour == 2 and current_time.hour == 3:
                self._check_ote_continuation_setup()
        
        # Check pending entries
        self._check_pending_entries()


# =============================================================================
# BACKTESTING ENGINE
# =============================================================================


class BacktestEngine:
    """
    Main backtesting engine that orchestrates data loading and strategy execution.
    """
    
    def __init__(
        self,
        data_path: str,
        years: List[int],
        execution_tf: str = '5m',
        initial_capital: float = 100000,
        commission: float = 0.0002  # 0.02% commission
    ):
        """
        Initialize the backtesting engine.
        
        Args:
            data_path: Path to data files
            years: List of years to backtest
            execution_tf: Execution timeframe ('1m' or '5m')
            initial_capital: Starting capital
            commission: Commission per trade (as decimal)
        """
        self.data_path = data_path
        self.years = years
        self.execution_tf = execution_tf
        self.initial_capital = initial_capital
        self.commission = commission
        
        self.exec_data = None
        self.h1_data = None
        self.h4_data = None
        self.results = None
        self.stats = None
    
    def load_data(self):
        """Load all required data files."""
        print("\n" + "="*60)
        print("Loading Market Data")
        print("="*60)
        
        # Load execution timeframe
        self.exec_data = load_multi_year_data(
            self.data_path, self.years, self.execution_tf
        )
        
        # Load H1 data for liquidity targeting
        self.h1_data = load_multi_year_data(
            self.data_path, self.years, '1H'
        )
        
        # Load H4 data for trend bias
        self.h4_data = load_multi_year_data(
            self.data_path, self.years, '4H'
        )
        
        print(f"\nData loaded successfully!")
        print(f"Execution data range: {self.exec_data.index[0]} to {self.exec_data.index[-1]}")
    
    def run_backtest(self) -> dict:
        """
        Execute the backtest and return results.
        
        Returns:
            Dictionary containing backtest statistics
        """
        print("\n" + "="*60)
        print("Running Backtest")
        print("="*60)
        
        # Set higher timeframe data on strategy class
        ICTLondonStrategy.h4_data = self.h4_data
        ICTLondonStrategy.h1_data = self.h1_data
        
        # Create backtest instance
        bt = Backtest(
            self.exec_data,
            ICTLondonStrategy,
            cash=self.initial_capital,
            commission=self.commission,
            exclusive_orders=True,
            trade_on_close=False
        )
        
        # Run backtest
        self.stats = bt.run()
        self.results = bt
        
        return self.stats
    
    def get_trade_logs(self) -> List[TradeLog]:
        """Get the list of trade logs from the strategy."""
        if self.results is None:
            return []
        return self.results._strategy.trade_logs if hasattr(self.results._strategy, 'trade_logs') else []
    
    def export_trade_log(self, output_path: str = "trade_log.csv"):
        """
        Export trade log to CSV file.
        
        Args:
            output_path: Path for output CSV file
        """
        if self.stats is None:
            print("No backtest results available. Run backtest first.")
            return
        
        trades = self.stats._trades
        if trades is None or len(trades) == 0:
            print("No trades to export.")
            return
        
        trades.to_csv(output_path, index=False)
        print(f"Trade log exported to {output_path}")
    
    def generate_report(self, output_path: str = "backtest_report.md"):
        """
        Generate comprehensive backtest report as Markdown file.
        
        Args:
            output_path: Path for output report file
        """
        if self.stats is None:
            print("No backtest results available. Run backtest first.")
            return
        
        report = self._create_report_content()
        
        with open(output_path, 'w') as f:
            f.write(report)
        
        print(f"Report generated: {output_path}")
    
    def _create_report_content(self) -> str:
        """Create the markdown report content."""
        stats = self.stats
        
        report = f"""# ICT London Session Strategy Backtest Report

## Strategy Overview

**Strategy:** ICT London Session (Silver Bullet + OTE Continuation)  
**Execution Timeframe:** {self.execution_tf}  
**Data Range:** {self.exec_data.index[0].strftime('%Y-%m-%d')} to {self.exec_data.index[-1].strftime('%Y-%m-%d')}  
**Initial Capital:** ${self.initial_capital:,.2f}  

---

## Performance Summary

| Metric | Value |
|--------|-------|
| **Final Equity** | ${stats['Equity Final [$]']:,.2f} |
| **Total Return** | {stats['Return [%]']:.2f}% |
| **Max Drawdown** | {stats['Max. Drawdown [%]']:.2f}% |
| **Sharpe Ratio** | {stats.get('Sharpe Ratio', 'N/A')} |
| **Sortino Ratio** | {stats.get('Sortino Ratio', 'N/A')} |
| **Calmar Ratio** | {stats.get('Calmar Ratio', 'N/A')} |

---

## Trade Statistics

| Metric | Value |
|--------|-------|
| **Total Trades** | {stats['# Trades']} |
| **Win Rate** | {stats['Win Rate [%]']:.2f}% |
| **Best Trade** | {stats['Best Trade [%]']:.2f}% |
| **Worst Trade** | {stats['Worst Trade [%]']:.2f}% |
| **Avg Trade** | {stats['Avg. Trade [%]']:.2f}% |
| **Avg Trade Duration** | {stats['Avg. Trade Duration']} |

---

## Risk Metrics

| Metric | Value |
|--------|-------|
| **Exposure Time** | {stats['Exposure Time [%]']:.2f}% |
| **Profit Factor** | {stats.get('Profit Factor', 'N/A')} |
| **Expectancy** | {stats.get('Expectancy [%]', 'N/A')} |

---

## Equity Curve

See `equity_curve.png` for the visual representation.

---

## Strategy Rules Summary

### Entry Criteria

**London Silver Bullet (02:00-03:00 Chicago / 09:00-10:00 Paris)**
1. H4 Close > EMA(20) for longs, H4 Close < EMA(20) for shorts
2. Liquidity sweep of fractal high/low
3. Displacement candle (Body > 2x ATR)
4. Fair Value Gap formation
5. Entry at FVG Low (buy) or FVG High (sell) + 1 tick buffer

**OTE Continuation (03:00-04:00 Chicago / 10:00-11:00 Paris)**
1. 02:00-03:00 range determined as bullish/bearish
2. Entry at 62% Fibonacci retracement

### Exit Criteria
- Stop Loss: Below swing low (longs) or above swing high (shorts)
- Take Profit: Fixed 2R (Risk:Reward 1:2)

### No Trade Zone
- After 04:30 Chicago (11:30 Paris)

---

*Report generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        return report
    
    def plot_equity_curve(self, output_path: str = "equity_curve.png"):
        """
        Generate and save equity curve plot.
        
        Args:
            output_path: Path for output image file
        """
        if self.stats is None:
            print("No backtest results available. Run backtest first.")
            return
        
        equity_curve = self.stats._equity_curve
        
        fig, axes = plt.subplots(2, 1, figsize=(14, 10), height_ratios=[3, 1])
        
        # Equity curve
        ax1 = axes[0]
        ax1.plot(equity_curve.index, equity_curve['Equity'], 
                 color='#2E86AB', linewidth=1.5, label='Equity')
        ax1.fill_between(equity_curve.index, self.initial_capital, 
                         equity_curve['Equity'], alpha=0.3, color='#2E86AB')
        ax1.axhline(y=self.initial_capital, color='gray', linestyle='--', 
                    alpha=0.5, label='Initial Capital')
        ax1.set_title('ICT London Session Strategy - Equity Curve', 
                      fontsize=14, fontweight='bold')
        ax1.set_ylabel('Equity ($)')
        ax1.legend(loc='upper left')
        ax1.grid(True, alpha=0.3)
        
        # Format y-axis with dollar signs
        ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
        
        # Drawdown
        ax2 = axes[1]
        drawdown = (equity_curve['Equity'] / equity_curve['Equity'].cummax() - 1) * 100
        ax2.fill_between(drawdown.index, 0, drawdown, color='#E74C3C', alpha=0.7)
        ax2.set_title('Drawdown', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Drawdown (%)')
        ax2.set_xlabel('Date')
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        print(f"Equity curve saved to {output_path}")
    
    def plot_monthly_returns(self, output_path: str = "monthly_returns.png"):
        """
        Generate monthly returns heatmap.
        
        Args:
            output_path: Path for output image file
        """
        if self.stats is None:
            print("No backtest results available. Run backtest first.")
            return
        
        equity = self.stats._equity_curve['Equity']
        
        # Calculate monthly returns
        monthly = equity.resample('ME').last()
        monthly_returns = monthly.pct_change() * 100
        
        # Reshape for heatmap
        monthly_df = pd.DataFrame({
            'Year': monthly_returns.index.year,
            'Month': monthly_returns.index.month,
            'Return': monthly_returns.values
        }).dropna()
        
        pivot = monthly_df.pivot(index='Year', columns='Month', values='Return')
        
        # Create heatmap
        fig, ax = plt.subplots(figsize=(14, 8))
        
        # Custom colormap
        colors = ['#E74C3C', '#FADBD8', '#FFFFFF', '#D5F4E6', '#27AE60']
        from matplotlib.colors import LinearSegmentedColormap
        cmap = LinearSegmentedColormap.from_list('returns', colors)
        
        im = ax.imshow(pivot.values, cmap=cmap, aspect='auto', vmin=-10, vmax=10)
        
        # Add colorbar
        cbar = ax.figure.colorbar(im, ax=ax)
        cbar.ax.set_ylabel('Return (%)', rotation=-90, va="bottom")
        
        # Set ticks
        ax.set_xticks(range(12))
        ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                           'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
        ax.set_yticks(range(len(pivot.index)))
        ax.set_yticklabels(pivot.index)
        
        # Add text annotations
        for i in range(len(pivot.index)):
            for j in range(12):
                if j + 1 in pivot.columns:
                    val = pivot.iloc[i, pivot.columns.get_loc(j + 1)]
                    if not pd.isna(val):
                        text = ax.text(j, i, f'{val:.1f}%',
                                       ha="center", va="center", color="black", fontsize=8)
        
        ax.set_title('Monthly Returns Heatmap', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        print(f"Monthly returns heatmap saved to {output_path}")


# =============================================================================
# MAIN EXECUTION
# =============================================================================


def main():
    """Main entry point for the backtesting script."""
    print("="*60)
    print("ICT London Session Strategy Backtest")
    print("="*60)
    print(f"Data Path: {DATA_PATH}")
    print(f"Years: {YEARS}")
    print(f"Execution Timeframe: {EXECUTION_TIMEFRAME}")
    print(f"Initial Capital: ${INITIAL_CAPITAL:,}")
    
    # Initialize engine
    engine = BacktestEngine(
        data_path=DATA_PATH,
        years=YEARS,
        execution_tf=EXECUTION_TIMEFRAME,
        initial_capital=INITIAL_CAPITAL
    )
    
    # Load data
    engine.load_data()
    
    # Run backtest
    stats = engine.run_backtest()
    
    # Print summary
    print("\n" + "="*60)
    print("Backtest Results Summary")
    print("="*60)
    print(stats)
    
    # Generate outputs
    print("\n" + "="*60)
    print("Generating Outputs")
    print("="*60)
    
    # Generate report
    engine.generate_report("backtest_report.md")
    
    # Export trade log
    engine.export_trade_log("trade_log.csv")
    
    # Plot equity curve
    engine.plot_equity_curve("equity_curve.png")
    
    # Plot monthly returns
    engine.plot_monthly_returns("monthly_returns.png")
    
    print("\n" + "="*60)
    print("Backtest Complete!")
    print("="*60)
    print("\nGenerated Files:")
    print("  - backtest_report.md  (Comprehensive strategy report)")
    print("  - trade_log.csv       (Detailed trade log)")
    print("  - equity_curve.png    (Equity curve visualization)")
    print("  - monthly_returns.png (Monthly returns heatmap)")
    
    return stats


if __name__ == "__main__":
    main()

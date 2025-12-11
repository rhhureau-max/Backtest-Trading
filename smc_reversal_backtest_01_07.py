#!/usr/bin/env python3
"""
SMC Reversal Backtest Strategy: 01:00-07:00 Session - Multi-Target R:R Comparison
Smart Money Concepts (SMC) based reversal strategy with Sweeps, MSS, and Fibonacci entries.

Strategy Logic:
1. Identify Fractal Highs/Lows (swing structure)
2. Detect Liquidity Sweeps (price exceeds fractal but closes back or reverses)
3. Confirm MSS (Market Structure Shift - break of previous swing low after sweep)
4. Enter at 50% Fibonacci retracement of MSS leg
5. Test 3 R:R targets simultaneously: 1:1, 1.5:1, 2:1 (SL above sweep high)

Modified to test multiple R:R targets instead of FVG-based TP.

Author: Python Expert in Backtesting & SMC
Date: 2025-12-11
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import time
import os
import warnings
warnings.filterwarnings('ignore')

# Configuration
BASE_PATH = '/home/runner/work/Backtest-Trading/Backtest-Trading'
DATA_TIMEFRAME = '5m'
SESSION_START = time(1, 0)   # 01:00
SESSION_END = time(7, 0)     # 07:00
RISK_PER_TRADE = 0.01        # 1% risk per trade
INITIAL_CAPITAL = 100000     # Starting capital
FRACTAL_WINDOW = 1           # Number of candles each side for local comparison
FRACTAL_LOOKBACK = 6         # Rolling max/min period for significant fractals (changed from 12 to 6)
REVERSAL_WINDOW = 2          # Number of candles to check for bearish reversal
FIB_ENTRY_LEVEL = 0.5        # 50% Fibonacci retracement
MIN_FVG_SIZE = 5             # Minimum FVG size in points
DEBUG = False                # Enable debug output
RR_TARGETS = [1.0, 1.5, 2.0] # R:R targets to test simultaneously

# Set plotting style
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (16, 10)


def load_nq_data(years=None, limit_years=None):
    """
    Load NQ 5-minute data from CSV files.
    
    Args:
        years: List of years to load. If None, loads all available years.
        limit_years: Number of recent years to load (optional, for performance testing)
    
    Returns:
        DataFrame with combined data
    """
    if years is None:
        if limit_years is not None:
            # Load only recent years for performance testing
            current_year = 2025
            years = range(current_year - limit_years + 1, current_year + 1)
        else:
            # Load all years from 2018 to 2025
            years = range(2018, 2026)
    
    all_data = []
    
    for year in years:
        file_path = os.path.join(BASE_PATH, f"{year} {DATA_TIMEFRAME}.csv")
        if not os.path.exists(file_path):
            print(f"Warning: File not found for year {year}")
            continue
        
        print(f"Loading data for {year}...")
        df = pd.read_csv(file_path, sep=';')
        
        # Parse datetime
        df['datetime'] = pd.to_datetime(df['Column1'] + ' ' + df['Column2'], 
                                       format='%d/%m/%Y %H:%M:%S')
        
        # Rename columns
        df = df.rename(columns={
            'Column3': 'Open',
            'Column4': 'High',
            'Column5': 'Low',
            'Column6': 'Close',
            'Column7': 'Volume'
        })
        
        df['Date'] = df['datetime'].dt.date
        df['Time'] = df['datetime'].dt.time
        
        all_data.append(df[['datetime', 'Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']])
    
    if not all_data:
        raise ValueError("No data files found!")
    
    combined_df = pd.concat(all_data, ignore_index=True)
    combined_df = combined_df.sort_values('datetime').reset_index(drop=True)
    
    print(f"\nTotal records loaded: {len(combined_df):,}")
    print(f"Date range: {combined_df['datetime'].min()} to {combined_df['datetime'].max()}")
    
    return combined_df


def filter_session_data(df, start_time, end_time):
    """Filter data for the specified session time window."""
    session_df = df[(df['Time'] >= start_time) & (df['Time'] < end_time)].copy()
    print(f"Session records (01:00-07:00): {len(session_df):,}")
    return session_df


def detect_fractals(df, window=1, lookback=6):
    """
    Detect SIGNIFICANT fractal highs and lows using OPTIMIZED vectorized operations.
    
    Fractal High must satisfy TWO conditions:
    1. Surrounded by lower candles: High[i] > max(High[i-window:i]) AND High[i] > max(High[i+1:i+window+1])
    2. Highest point in last lookback candles: High[i] == max(High[i-lookback:i+1])
    
    Fractal Low must satisfy TWO conditions:
    1. Surrounded by higher candles: Low[i] < min(Low[i-window:i]) AND Low[i] < min(Low[i+1:i+window+1])
    2. Lowest point in last lookback candles: Low[i] == min(Low[i-lookback:i+1])
    
    Args:
        window: Number of candles on each side for local comparison (default=1)
        lookback: Number of periods for rolling max/min (default=6)
    
    Returns:
        DataFrame with fractal_high and fractal_low boolean columns
    """
    df = df.copy().reset_index(drop=True)
    
    # Initialize columns
    df['fractal_high'] = False
    df['fractal_low'] = False
    
    # Use rolling operations for faster computation
    df['rolling_max'] = df['High'].rolling(window=lookback+1, min_periods=lookback+1).max()
    df['rolling_min'] = df['Low'].rolling(window=lookback+1, min_periods=lookback+1).min()
    
    # Condition 2 (global): Is this the rolling max/min?
    df['is_rolling_max'] = df['High'] == df['rolling_max']
    df['is_rolling_min'] = df['Low'] == df['rolling_min']
    
    # For condition 1 (local), we need to check surrounding candles
    # Use shift to create comparison columns
    high_arr = df['High'].values
    low_arr = df['Low'].values
    n = len(df)
    
    # Pre-allocate boolean arrays
    local_high = np.zeros(n, dtype=bool)
    local_low = np.zeros(n, dtype=bool)
    
    # Vectorized comparison for window=1 (most common case, optimized)
    if window == 1:
        # For highs: check if High[i] > High[i-1] and High[i] > High[i+1]
        local_high[1:-1] = (high_arr[1:-1] > high_arr[:-2]) & (high_arr[1:-1] > high_arr[2:])
        # For lows: check if Low[i] < Low[i-1] and Low[i] < Low[i+1]
        local_low[1:-1] = (low_arr[1:-1] < low_arr[:-2]) & (low_arr[1:-1] < low_arr[2:])
    else:
        # For larger windows, use the loop (less common, still reasonably fast)
        start_idx = max(window, lookback)
        for i in range(start_idx, n - window):
            # Check local high
            left_highs = high_arr[i-window:i]
            right_highs = high_arr[i+1:i+window+1]
            local_high[i] = (high_arr[i] > np.max(left_highs)) and (high_arr[i] > np.max(right_highs))
            
            # Check local low
            left_lows = low_arr[i-window:i]
            right_lows = low_arr[i+1:i+window+1]
            local_low[i] = (low_arr[i] < np.min(left_lows)) and (low_arr[i] < np.min(right_lows))
    
    # Combine both conditions
    df['fractal_high'] = df['is_rolling_max'] & local_high
    df['fractal_low'] = df['is_rolling_min'] & local_low
    
    # Clean up temporary columns
    df = df.drop(columns=['rolling_max', 'rolling_min', 'is_rolling_max', 'is_rolling_min'])
    
    return df


def detect_fvg(df):
    """
    Detect Fair Value Gaps (FVG).
    
    Bearish FVG: Gap between Low[i] and High[i+2] when Low[i] > High[i+2]
    Bullish FVG: Gap between High[i] and Low[i+2] when High[i] < Low[i+2]
    
    Returns:
        DataFrame with FVG information
    """
    df = df.copy()
    df['bearish_fvg'] = False
    df['bullish_fvg'] = False
    df['fvg_top'] = np.nan
    df['fvg_bottom'] = np.nan
    
    for i in range(len(df) - 2):
        # Bearish FVG: Low[i] > High[i+2]
        if df.iloc[i]['Low'] > df.iloc[i+2]['High']:
            fvg_size = df.iloc[i]['Low'] - df.iloc[i+2]['High']
            if fvg_size >= MIN_FVG_SIZE:  # Only count significant FVGs
                df.loc[df.index[i+1], 'bearish_fvg'] = True
                df.loc[df.index[i+1], 'fvg_top'] = df.iloc[i]['Low']
                df.loc[df.index[i+1], 'fvg_bottom'] = df.iloc[i+2]['High']
        
        # Bullish FVG: High[i] < Low[i+2]
        if df.iloc[i]['High'] < df.iloc[i+2]['Low']:
            fvg_size = df.iloc[i+2]['Low'] - df.iloc[i]['High']
            if fvg_size >= MIN_FVG_SIZE:  # Only count significant FVGs
                df.loc[df.index[i+1], 'bullish_fvg'] = True
                df.loc[df.index[i+1], 'fvg_bottom'] = df.iloc[i]['High']
                df.loc[df.index[i+1], 'fvg_top'] = df.iloc[i+2]['Low']
    
    return df


def check_fvg_filled(df, fvg_idx, fvg_top, fvg_bottom, start_idx):
    """
    Check if an FVG has been filled by price action after a given index.
    
    Args:
        df: DataFrame with price data
        fvg_idx: Index where FVG was formed
        fvg_top: Top of FVG
        fvg_bottom: Bottom of FVG
        start_idx: Index to start checking from
    
    Returns:
        True if FVG is filled, False otherwise
    """
    for i in range(start_idx, len(df)):
        if df.iloc[i]['Low'] <= fvg_bottom or df.iloc[i]['High'] >= fvg_top:
            return True
    return False


def find_sweep_opportunities(session_df):
    """
    Identify STRICTER sweep opportunities in a session.
    
    A sweep occurs when:
    - Price exceeds a SIGNIFICANT fractal high (with wick above)
    - BUT closes BELOW the fractal high (rejection)
    - OR shows bearish engulfing/strong reversal within next 2 candles
    
    Returns:
        List of sweep opportunities with details
    """
    sweeps = []
    
    # Get fractal highs (now more significant with 12-period rolling max)
    fractal_highs = session_df[session_df['fractal_high']].copy()
    
    if len(fractal_highs) == 0:
        return sweeps
    
    for fh_idx, fh_row in fractal_highs.iterrows():
        fractal_high_price = fh_row['High']
        fractal_high_time = fh_row['datetime']
        
        # Look for sweeps after this fractal
        subsequent_candles = session_df[session_df['datetime'] > fractal_high_time]
        
        for sc_idx, sc_row in subsequent_candles.iterrows():
            # Check if high exceeded fractal (sweep condition)
            if sc_row['High'] > fractal_high_price:
                # CONDITION A: Close below fractal (wick rejection)
                wick_rejection = sc_row['Close'] < fractal_high_price
                
                # CONDITION B: Check for bearish reversal in next 2 candles
                next_idx = session_df.index.get_loc(sc_idx)
                reversal = False
                
                if next_idx + 2 < len(session_df):
                    next_candles = session_df.iloc[next_idx+1:next_idx+3]
                    
                    for nc_idx, nc_row in next_candles.iterrows():
                        # Bearish engulfing: Red candle that opens above and closes below previous
                        if nc_idx > 0:
                            prev_candle = session_df.iloc[session_df.index.get_loc(nc_idx) - 1]
                            bearish_engulfing = (
                                nc_row['Close'] < nc_row['Open'] and  # Bearish candle
                                nc_row['Open'] > prev_candle['Close'] and  # Opens higher
                                nc_row['Close'] < prev_candle['Open']  # Closes lower
                            )
                            
                            # Strong bearish reversal: Large red candle closing below fractal
                            strong_reversal = (
                                nc_row['Close'] < nc_row['Open'] and  # Bearish
                                nc_row['Close'] < fractal_high_price and  # Closes below fractal
                                (nc_row['Open'] - nc_row['Close']) > 10  # At least 10 points drop
                            )
                            
                            if bearish_engulfing or strong_reversal:
                                reversal = True
                                break
                
                # Accept sweep if either condition met
                if wick_rejection or reversal:
                    sweeps.append({
                        'fractal_idx': fh_idx,
                        'fractal_high': fractal_high_price,
                        'fractal_time': fractal_high_time,
                        'sweep_idx': sc_idx,
                        'sweep_high': sc_row['High'],
                        'sweep_time': sc_row['datetime'],
                        'sweep_close': sc_row['Close'],
                        'wick_rejection': wick_rejection,
                        'reversal': reversal
                    })
                    break  # Only one sweep per fractal
    
    return sweeps


def check_mss(session_df, sweep_info):
    """
    Check for Market Structure Shift (MSS) after a sweep.
    
    MSS: Price breaks the last significant fractal low that led to the sweep high.
    
    Returns:
        MSS info dict if MSS occurs, None otherwise
    """
    sweep_time = sweep_info['sweep_time']
    
    # Find fractal lows before the sweep
    fractals_before = session_df[
        (session_df['datetime'] < sweep_time) & 
        (session_df['fractal_low'])
    ].copy()
    
    if len(fractals_before) == 0:
        return None
    
    # Get the most recent fractal low before sweep
    last_fractal_low = fractals_before.iloc[-1]
    fractal_low_price = last_fractal_low['Low']
    
    # Look for MSS after sweep
    candles_after_sweep = session_df[session_df['datetime'] > sweep_time]
    
    for idx, row in candles_after_sweep.iterrows():
        # MSS: Close breaks below the fractal low
        if row['Close'] < fractal_low_price:
            return {
                'mss_idx': idx,
                'mss_time': row['datetime'],
                'mss_close': row['Close'],
                'mss_low': row['Low'],
                'fractal_low': fractal_low_price,
                'fractal_low_idx': last_fractal_low.name
            }
    
    return None


def calculate_fibonacci_entry(sweep_high, mss_low):
    """
    Calculate 50% Fibonacci retracement entry level.
    
    Args:
        sweep_high: High of the sweep
        mss_low: Low after MSS
    
    Returns:
        Entry price at 50% retracement
    """
    return mss_low + (sweep_high - mss_low) * FIB_ENTRY_LEVEL


def find_first_unfilled_fvg(session_df, sweep_info, mss_info, entry_time):
    """
    Find the first unfilled bearish FVG created during the bearish MSS leg.
    Look for FVGs between the sweep and the MSS confirmation.
    
    Args:
        session_df: Session data
        sweep_info: Sweep information
        mss_info: MSS information
        entry_time: Time of entry
    
    Returns:
        FVG bottom price (TP level) or None, or use mss_low if no FVG found
    """
    sweep_time = sweep_info['sweep_time']
    mss_time = mss_info['mss_time']
    
    # Look for FVGs created during the MSS leg (between sweep and MSS)
    fvgs_in_leg = session_df[
        (session_df['datetime'] > sweep_time) & 
        (session_df['datetime'] <= mss_time) &
        (session_df['bearish_fvg'])
    ].copy()
    
    if len(fvgs_in_leg) == 0:
        # No FVG found, use MSS low as conservative TP
        return mss_info['mss_low']
    
    # Get the first (highest) FVG in the leg
    # For a bearish move, we want the highest FVG created during the drop
    fvg_row = fvgs_in_leg.iloc[0]
    fvg_bottom = fvg_row['fvg_bottom']
    
    return fvg_bottom


def simulate_trade_multi_target(full_df, sweep_info, mss_info, entry_price, sl_price, entry_time, rr_targets):
    """
    Simulate trade execution with multiple R:R take profit targets.
    
    Args:
        full_df: Full dataframe (for exits after session)
        sweep_info: Sweep information
        mss_info: MSS information
        entry_price: Entry price
        sl_price: Stop loss price
        entry_time: Entry time
        rr_targets: List of R:R ratios to test (e.g., [1.0, 1.5, 2.0])
    
    Returns:
        Dict with results for each R:R target {RR_1.0: {...}, RR_1.5: {...}, RR_2.0: {...}}
    """
    # Find all candles after entry (including after session end)
    candles_after_entry = full_df[full_df['datetime'] > entry_time].copy()
    
    if len(candles_after_entry) == 0:
        return None  # No data after entry
    
    risk_points = sl_price - entry_price
    
    # Initialize results for each R:R target
    results = {}
    for rr in rr_targets:
        tp_price = entry_price - (risk_points * rr)  # For short position
        
        results[f'RR_{rr}'] = {
            'entry_time': entry_time,
            'entry_price': entry_price,
            'sl_price': sl_price,
            'tp_price': tp_price,
            'exit_time': None,
            'exit_price': None,
            'outcome': None,  # 'win' or 'loss'
            'pnl_points': 0,
            'risk_points': risk_points,
            'reward_points': risk_points * rr,
            'rr_ratio': rr
        }
    
    # Check each candle for SL or TP hits
    for idx, row in candles_after_entry.iterrows():
        # Check if SL hit (price goes above SL for short) - this affects ALL targets
        if row['High'] >= sl_price:
            for rr in rr_targets:
                key = f'RR_{rr}'
                if results[key]['outcome'] is None:
                    results[key]['exit_time'] = row['datetime']
                    results[key]['exit_price'] = sl_price
                    results[key]['outcome'] = 'loss'
                    results[key]['pnl_points'] = entry_price - sl_price  # Negative for loss
            break  # All targets stopped out
        
        # Check if TP hit for each target (price goes to or below TP for short)
        for rr in rr_targets:
            key = f'RR_{rr}'
            if results[key]['outcome'] is None:
                tp_price = results[key]['tp_price']
                if row['Low'] <= tp_price:
                    results[key]['exit_time'] = row['datetime']
                    results[key]['exit_price'] = tp_price
                    results[key]['outcome'] = 'win'
                    results[key]['pnl_points'] = entry_price - tp_price  # Positive for win
    
    # Filter out incomplete trades
    valid_results = {}
    for key, result in results.items():
        if result['outcome'] is not None:
            valid_results[key] = result
    
    return valid_results if valid_results else None


def backtest_session(full_df, session_date, session_df):
    """
    Backtest the SMC reversal strategy for a single session with multiple R:R targets.
    
    Args:
        full_df: Full dataframe (for exits after session)
        session_date: Date of the session
        session_df: Session data for this date
    
    Returns:
        Dict of trade lists for each R:R target
    """
    # Initialize trade lists for each target
    trades = {f'RR_{rr}': [] for rr in RR_TARGETS}
    
    # Add fractals and FVGs with new significant fractal detection
    session_df = detect_fractals(session_df, window=FRACTAL_WINDOW, lookback=FRACTAL_LOOKBACK)
    session_df = detect_fvg(session_df)
    
    # Find sweep opportunities
    sweeps = find_sweep_opportunities(session_df)
    
    if len(sweeps) == 0:
        return trades
    
    # For each sweep, check for MSS and potential trade
    for sweep in sweeps:
        mss_info = check_mss(session_df, sweep)
        
        if mss_info is None:
            continue
        
        # Calculate entry price (50% Fib retracement)
        entry_price = calculate_fibonacci_entry(sweep['sweep_high'], mss_info['mss_low'])
        
        # SL above sweep high
        sl_price = sweep['sweep_high'] + 5  # Small buffer above sweep
        
        # Check if entry price makes sense (should be between mss_low and sweep_high)
        if not (mss_info['mss_low'] < entry_price < sweep['sweep_high']):
            continue
        
        # Check minimum R:R ratio (at least 0.8:1)
        risk = sl_price - entry_price
        # For multi-target, we just need to check that the lowest R:R (1:1) is viable
        min_reward = risk * min(RR_TARGETS)
        tp_min = entry_price - min_reward
        
        if tp_min >= entry_price:  # TP must be below entry for short
            continue
        
        # Simulate trade execution with multiple targets
        entry_time = mss_info['mss_time']
        
        # Make sure entry is within session
        if entry_time.time() >= SESSION_END:
            continue
        
        trade_results = simulate_trade_multi_target(
            full_df, sweep, mss_info, 
            entry_price, sl_price, entry_time, RR_TARGETS
        )
        
        if trade_results is not None:
            for key, result in trade_results.items():
                result['session_date'] = session_date
                result['sweep_high'] = sweep['sweep_high']
                result['mss_low'] = mss_info['mss_low']
                trades[key].append(result)
    
    return trades


def run_backtest(df):
    """
    Run backtest across all sessions with multiple R:R targets.
    
    Args:
        df: Full dataframe with all data
    
    Returns:
        Dict of DataFrames with trades for each R:R target
    """
    print("\n" + "="*80)
    print("RUNNING SMC REVERSAL BACKTEST - MULTI-TARGET R:R COMPARISON")
    print(f"Testing R:R targets: {', '.join([f'{rr}:1' for rr in RR_TARGETS])}")
    print("="*80)
    
    # Filter for session times
    session_df = filter_session_data(df, SESSION_START, SESSION_END)
    
    # Initialize trade lists for each target
    all_trades = {f'RR_{rr}': [] for rr in RR_TARGETS}
    
    # Group by session date
    sessions = session_df.groupby('Date')
    total_sessions = len(sessions)
    
    print(f"\nProcessing {total_sessions} sessions...")
    
    for i, (session_date, session_data) in enumerate(sessions):
        if (i + 1) % 200 == 0:
            trades_found = sum(len(all_trades[k]) for k in all_trades.keys())
            print(f"  Processed {i+1}/{total_sessions} sessions... ({trades_found} total trades found)")
        
        session_trades = backtest_session(df, session_date, session_data)
        
        # Collect trades for each target
        for key in all_trades.keys():
            all_trades[key].extend(session_trades[key])
    
    print(f"\nBacktest complete!")
    print(f"\nTrades found per R:R target:")
    for rr in RR_TARGETS:
        key = f'RR_{rr}'
        print(f"  {rr}:1 - {len(all_trades[key])} trades")
    
    # Convert to DataFrames
    trades_dfs = {}
    for rr in RR_TARGETS:
        key = f'RR_{rr}'
        if len(all_trades[key]) > 0:
            trades_dfs[key] = pd.DataFrame(all_trades[key])
        else:
            print(f"\n⚠️ No trades found for R:R {rr}:1")
            trades_dfs[key] = pd.DataFrame()
    
    return trades_dfs


def calculate_performance_metrics(trades_df, rr_target):
    """
    Calculate performance metrics from trades for a specific R:R target.
    
    Args:
        trades_df: DataFrame with trades
        rr_target: R:R ratio (e.g., 1.0, 1.5, 2.0)
    
    Returns:
        Dictionary with performance metrics
    """
    if len(trades_df) == 0:
        return {
            'rr_target': rr_target,
            'total_trades': 0,
            'wins': 0,
            'losses': 0,
            'win_rate': 0,
            'total_pnl_points': 0,
            'avg_pnl_points': 0,
            'avg_win': 0,
            'avg_loss': 0,
            'avg_rr_ratio': rr_target,
            'profit_factor': 0,
            'gross_profit': 0,
            'gross_loss': 0
        }
    
    total_trades = len(trades_df)
    wins = len(trades_df[trades_df['outcome'] == 'win'])
    losses = len(trades_df[trades_df['outcome'] == 'loss'])
    
    win_rate = (wins / total_trades) * 100 if total_trades > 0 else 0
    
    total_pnl_points = trades_df['pnl_points'].sum()
    avg_pnl_points = trades_df['pnl_points'].mean()
    
    avg_win = trades_df[trades_df['outcome'] == 'win']['pnl_points'].mean() if wins > 0 else 0
    avg_loss = abs(trades_df[trades_df['outcome'] == 'loss']['pnl_points'].mean()) if losses > 0 else 0
    
    avg_rr_ratio = trades_df['rr_ratio'].mean()
    
    # Profit factor
    gross_profit = trades_df[trades_df['outcome'] == 'win']['pnl_points'].sum()
    gross_loss = abs(trades_df[trades_df['outcome'] == 'loss']['pnl_points'].sum())
    profit_factor = gross_profit / gross_loss if gross_loss > 0 else float('inf')
    
    metrics = {
        'rr_target': rr_target,
        'total_trades': total_trades,
        'wins': wins,
        'losses': losses,
        'win_rate': win_rate,
        'total_pnl_points': total_pnl_points,
        'avg_pnl_points': avg_pnl_points,
        'avg_win': avg_win,
        'avg_loss': avg_loss,
        'avg_rr_ratio': avg_rr_ratio,
        'profit_factor': profit_factor,
        'gross_profit': gross_profit,
        'gross_loss': gross_loss
    }
    
    return metrics


def calculate_cumulative_pnl(trades_df, risk_pct=RISK_PER_TRADE, initial_capital=INITIAL_CAPITAL):
    """
    Calculate cumulative P&L with risk management (1% risk per trade).
    
    Args:
        trades_df: DataFrame with trades
        risk_pct: Risk percentage per trade
        initial_capital: Starting capital
    
    Returns:
        DataFrame with cumulative equity
    """
    if len(trades_df) == 0:
        return pd.DataFrame()
    
    trades_df = trades_df.sort_values('entry_time').copy()
    
    equity = initial_capital
    equity_curve = [equity]
    
    for idx, trade in trades_df.iterrows():
        # Risk is fixed percentage of current equity
        risk_amount = equity * risk_pct
        
        # Position size based on risk
        risk_points = abs(trade['risk_points'])
        if risk_points > 0:
            # PnL = (pnl_points / risk_points) * risk_amount
            pnl = (trade['pnl_points'] / risk_points) * risk_amount
            equity += pnl
        
        equity_curve.append(equity)
    
    trades_df['equity'] = equity_curve[1:]
    trades_df['cumulative_pnl'] = trades_df['equity'] - initial_capital
    
    return trades_df


def plot_results(all_trades_dfs, all_metrics):
    """
    Create comprehensive visualization comparing all R:R targets.
    
    Args:
        all_trades_dfs: Dict of DataFrames for each R:R target
        all_metrics: Dict of metrics for each R:R target
    """
    fig = plt.figure(figsize=(20, 14))
    gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
    
    colors = ['#2E86AB', '#A23B72', '#F18F01']
    
    # 1. Equity Curves Comparison (Top - full width)
    ax1 = fig.add_subplot(gs[0, :])
    for i, rr in enumerate(RR_TARGETS):
        key = f'RR_{rr}'
        if len(all_trades_dfs[key]) > 0:
            trades_df = all_trades_dfs[key]
            trades_with_equity = calculate_cumulative_pnl(trades_df)
            ax1.plot(range(len(trades_with_equity)), 
                    trades_with_equity['cumulative_pnl'], 
                    label=f'R:R {rr}:1', color=colors[i], linewidth=2.5)
    
    ax1.axhline(y=0, color='gray', linestyle='--', alpha=0.5, label='Break Even')
    ax1.set_title('Equity Curves Comparison - All R:R Targets (2018-2025)', 
                 fontsize=14, fontweight='bold')
    ax1.set_xlabel('Trade Number', fontsize=12)
    ax1.set_ylabel('Cumulative P&L ($)', fontsize=12)
    ax1.legend(fontsize=11)
    ax1.grid(True, alpha=0.3)
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}K'))
    
    # 2. Win Rate Comparison
    ax2 = fig.add_subplot(gs[1, 0])
    win_rates = [all_metrics[f'RR_{rr}']['win_rate'] for rr in RR_TARGETS]
    bars = ax2.bar([f'{rr}:1' for rr in RR_TARGETS], win_rates, color=colors, alpha=0.8, edgecolor='black')
    ax2.set_title('Win Rate Comparison', fontsize=13, fontweight='bold')
    ax2.set_ylabel('Win Rate (%)', fontsize=11)
    ax2.set_ylim(0, 100)
    ax2.grid(axis='y', alpha=0.3)
    for bar, val in zip(bars, win_rates):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 2,
                f'{val:.1f}%', ha='center', va='bottom', fontweight='bold', fontsize=11)
    
    # 3. Profit Factor Comparison
    ax3 = fig.add_subplot(gs[1, 1])
    profit_factors = [all_metrics[f'RR_{rr}']['profit_factor'] for rr in RR_TARGETS]
    bars = ax3.bar([f'{rr}:1' for rr in RR_TARGETS], profit_factors, color=colors, alpha=0.8, edgecolor='black')
    ax3.set_title('Profit Factor Comparison', fontsize=13, fontweight='bold')
    ax3.set_ylabel('Profit Factor', fontsize=11)
    ax3.axhline(y=1.0, color='red', linestyle='--', alpha=0.5, label='Break Even')
    ax3.grid(axis='y', alpha=0.3)
    ax3.legend(fontsize=9)
    for bar, val in zip(bars, profit_factors):
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                f'{val:.2f}', ha='center', va='bottom', fontweight='bold', fontsize=11)
    
    # 4. Total Return Comparison
    ax4 = fig.add_subplot(gs[1, 2])
    returns = []
    for rr in RR_TARGETS:
        key = f'RR_{rr}'
        if len(all_trades_dfs[key]) > 0:
            trades_with_equity = calculate_cumulative_pnl(all_trades_dfs[key])
            final_equity = trades_with_equity.iloc[-1]['equity']
            total_return = ((final_equity - INITIAL_CAPITAL) / INITIAL_CAPITAL) * 100
            returns.append(total_return)
        else:
            returns.append(0)
    
    bars = ax4.bar([f'{rr}:1' for rr in RR_TARGETS], returns, color=colors, alpha=0.8, edgecolor='black')
    ax4.set_title('Total Return Comparison', fontsize=13, fontweight='bold')
    ax4.set_ylabel('Return (%)', fontsize=11)
    ax4.axhline(y=0, color='red', linestyle='--', alpha=0.5)
    ax4.grid(axis='y', alpha=0.3)
    for bar, val in zip(bars, returns):
        height = bar.get_height()
        y_pos = height + 1 if height >= 0 else height - 5
        ax4.text(bar.get_x() + bar.get_width()/2., y_pos,
                f'{val:+.1f}%', ha='center', va='bottom' if height >= 0 else 'top', 
                fontweight='bold', fontsize=11)
    
    # 5. Total Trades Comparison
    ax5 = fig.add_subplot(gs[2, 0])
    trade_counts = [len(all_trades_dfs[f'RR_{rr}']) for rr in RR_TARGETS]
    bars = ax5.bar([f'{rr}:1' for rr in RR_TARGETS], trade_counts, color=colors, alpha=0.8, edgecolor='black')
    ax5.set_title('Total Trades', fontsize=13, fontweight='bold')
    ax5.set_ylabel('Number of Trades', fontsize=11)
    ax5.grid(axis='y', alpha=0.3)
    for bar, val in zip(bars, trade_counts):
        height = bar.get_height()
        ax5.text(bar.get_x() + bar.get_width()/2., height,
                f'{val}', ha='center', va='bottom', fontweight='bold', fontsize=11)
    
    # 6. Average Win vs Loss
    ax6 = fig.add_subplot(gs[2, 1])
    x = np.arange(len(RR_TARGETS))
    width = 0.35
    
    avg_wins = [all_metrics[f'RR_{rr}']['avg_win'] for rr in RR_TARGETS]
    avg_losses = [all_metrics[f'RR_{rr}']['avg_loss'] for rr in RR_TARGETS]
    
    ax6.bar(x - width/2, avg_wins, width, label='Avg Win', color='#27AE60', alpha=0.8, edgecolor='black')
    ax6.bar(x + width/2, avg_losses, width, label='Avg Loss', color='#E74C3C', alpha=0.8, edgecolor='black')
    
    ax6.set_title('Average Win vs Loss', fontsize=13, fontweight='bold')
    ax6.set_ylabel('Points', fontsize=11)
    ax6.set_xticks(x)
    ax6.set_xticklabels([f'{rr}:1' for rr in RR_TARGETS])
    ax6.legend(fontsize=10)
    ax6.grid(axis='y', alpha=0.3)
    
    # 7. Total P&L (Points)
    ax7 = fig.add_subplot(gs[2, 2])
    total_pnls = [all_metrics[f'RR_{rr}']['total_pnl_points'] for rr in RR_TARGETS]
    bars = ax7.bar([f'{rr}:1' for rr in RR_TARGETS], total_pnls, color=colors, alpha=0.8, edgecolor='black')
    ax7.set_title('Total P&L (Points)', fontsize=13, fontweight='bold')
    ax7.set_ylabel('Total P&L (Points)', fontsize=11)
    ax7.axhline(y=0, color='red', linestyle='--', alpha=0.5)
    ax7.grid(axis='y', alpha=0.3)
    for bar, val in zip(bars, total_pnls):
        height = bar.get_height()
        y_pos = height + 20 if height >= 0 else height - 100
        ax7.text(bar.get_x() + bar.get_width()/2., y_pos,
                f'{val:+.0f}', ha='center', va='bottom' if height >= 0 else 'top', 
                fontweight='bold', fontsize=11)
    
    plt.suptitle('SMC Reversal Strategy: Multi-Target R:R Comparison (01:00-07:00)', 
                 fontsize=16, fontweight='bold', y=0.998)
    
    output_path = os.path.join(BASE_PATH, 'smc_reversal_backtest_results.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\n✓ Saved comparison chart: smc_reversal_backtest_results.png")
    plt.close()


def print_performance_report(all_metrics, all_trades_dfs):
    """
    Print detailed performance report comparing all R:R targets.
    
    Args:
        all_metrics: Dict of metrics for each R:R target
        all_trades_dfs: Dict of DataFrames for each R:R target
    """
    print("\n" + "="*100)
    print("MULTI-TARGET R:R COMPARISON - PERFORMANCE SUMMARY")
    print("="*100)
    
    # Summary comparison table
    print("\n📊 SUMMARY COMPARISON TABLE")
    print("-" * 100)
    print(f"{'R:R Target':<12} {'Trades':<10} {'Win Rate':<12} {'Profit Factor':<15} "
          f"{'Total P&L':<15} {'Return (%)':<12}")
    print("-" * 100)
    
    for rr in RR_TARGETS:
        key = f'RR_{rr}'
        m = all_metrics[key]
        
        # Calculate return
        if len(all_trades_dfs[key]) > 0:
            trades_with_equity = calculate_cumulative_pnl(all_trades_dfs[key])
            final_equity = trades_with_equity.iloc[-1]['equity']
            total_return = ((final_equity - INITIAL_CAPITAL) / INITIAL_CAPITAL) * 100
        else:
            total_return = 0.0
        
        print(f"{rr}:1{'':<9} {m['total_trades']:<10} {m['win_rate']:>6.2f}%{'':<5} "
              f"{m['profit_factor']:>8.2f}{'':<7} {m['total_pnl_points']:>+10.2f} pts{'':<2} "
              f"{total_return:>+8.2f}%")
    
    print("-" * 100)
    
    # Detailed breakdown for each target
    for rr in RR_TARGETS:
        key = f'RR_{rr}'
        m = all_metrics[key]
        trades_df = all_trades_dfs[key]
        
        print(f"\n{'='*100}")
        print(f"DETAILED RESULTS: R:R {rr}:1 TARGET")
        print(f"{'='*100}")
        
        if m['total_trades'] == 0:
            print("\n⚠️ No trades found for this R:R target.")
            continue
        
        print(f"\n📈 Performance Metrics:")
        print(f"  Total Trades: {m['total_trades']}")
        print(f"  Wins: {m['wins']} | Losses: {m['losses']}")
        print(f"  Win Rate: {m['win_rate']:.2f}%")
        print(f"  Profit Factor: {m['profit_factor']:.2f}")
        
        print(f"\n💰 P&L Analysis:")
        print(f"  Total P&L: {m['total_pnl_points']:+.2f} points")
        print(f"  Average P&L per Trade: {m['avg_pnl_points']:+.2f} points")
        print(f"  Average Win: +{m['avg_win']:.2f} points")
        print(f"  Average Loss: -{m['avg_loss']:.2f} points")
        print(f"  Gross Profit: {m['gross_profit']:.2f} points")
        print(f"  Gross Loss: {m['gross_loss']:.2f} points")
        
        # Calculate equity metrics
        trades_with_equity = calculate_cumulative_pnl(trades_df)
        final_equity = trades_with_equity.iloc[-1]['equity']
        total_return = ((final_equity - INITIAL_CAPITAL) / INITIAL_CAPITAL) * 100
        annual_return = total_return / 7  # 7 years of data
        
        print(f"\n📊 Account Performance (1% Risk per Trade):")
        print(f"  Initial Capital: ${INITIAL_CAPITAL:,.2f}")
        print(f"  Final Equity: ${final_equity:,.2f}")
        print(f"  Total Return: {total_return:+.2f}%")
        print(f"  Annual Return: {annual_return:+.2f}%")
    
    print("\n" + "="*100)


def print_detailed_trades(all_trades_dfs, year=2025, num_trades=5):
    """
    Print detailed information for the last N trades from a specific year for EACH R:R target.
    
    Args:
        all_trades_dfs: Dict of DataFrames with trades for each R:R target
        year: Year to filter trades from
        num_trades: Number of trades to display per target
    """
    for rr in RR_TARGETS:
        key = f'RR_{rr}'
        trades_df = all_trades_dfs[key]
        
        if len(trades_df) == 0:
            continue
        
        # Filter trades from specified year
        trades_df['year'] = pd.to_datetime(trades_df['entry_time']).dt.year
        year_trades = trades_df[trades_df['year'] == year].copy()
        
        if len(year_trades) == 0:
            print(f"\n⚠️ No trades found for year {year} with R:R {rr}:1")
            continue
        
        # Get last N trades
        last_trades = year_trades.tail(num_trades)
        
        print("\n" + "="*100)
        print(f"LAST {num_trades} TRADES FROM {year} - R:R {rr}:1 TARGET")
        print("="*100)
        
        for idx, (_, trade) in enumerate(last_trades.iterrows(), 1):
            print(f"\n{'='*100}")
            print(f"TRADE #{len(year_trades) - num_trades + idx} of {len(year_trades)} ({year}) - R:R {rr}:1")
            print(f"{'='*100}")
            
            print(f"\n📅 Session Date: {trade['session_date']}")
            print(f"⏰ Entry Time: {trade['entry_time']}")
            print(f"🚪 Exit Time: {trade['exit_time']}")
            
            print(f"\n💰 PRICES:")
            print(f"   Sweep High: {trade['sweep_high']:.2f}")
            print(f"   MSS Low: {trade['mss_low']:.2f}")
            print(f"   Entry Price (50% Fib): {trade['entry_price']:.2f}")
            print(f"   Stop Loss: {trade['sl_price']:.2f}")
            print(f"   Take Profit (R:R {rr}:1): {trade['tp_price']:.2f}")
            print(f"   Exit Price: {trade['exit_price']:.2f}")
            
            print(f"\n📊 TRADE METRICS:")
            outcome_emoji = '✅' if trade['outcome'] == 'win' else '❌'
            print(f"   Outcome: {outcome_emoji} {trade['outcome'].upper()}")
            print(f"   P&L: {trade['pnl_points']:+.2f} points")
            print(f"   Risk: {trade['risk_points']:.2f} points")
            print(f"   Reward: {trade['reward_points']:.2f} points")
            print(f"   R:R Ratio: {trade['rr_ratio']:.2f}")
        
        print("\n" + "="*100)
        print(f"\n📈 {year} YEAR SUMMARY - R:R {rr}:1:")
        print(f"   Total Trades: {len(year_trades)}")
        print(f"   Win Rate: {(year_trades['outcome'] == 'win').sum() / len(year_trades) * 100:.2f}%")
        print(f"   Total P&L: {year_trades['pnl_points'].sum():+.2f} points")
        print(f"   Average P&L: {year_trades['pnl_points'].mean():+.2f} points per trade")
        print("="*100)


def main():
    """
    Main execution function.
    """
    print("="*100)
    print("SMC REVERSAL BACKTEST: MULTI-TARGET R:R COMPARISON")
    print("Smart Money Concepts with Sweeps, MSS, and Fibonacci Entries")
    print(f"Testing R:R targets: {', '.join([f'{rr}:1' for rr in RR_TARGETS])}")
    print("="*100)
    
    # Load data from 2018 to today (all years)
    print("\n📊 Loading NQ 5-minute data from 2018 to 2025 (all available years)...\n")
    
    df = load_nq_data()  # No limit_years parameter = load all years
    
    # Run backtest with multiple R:R targets
    all_trades_dfs = run_backtest(df)
    
    # Check if any trades were found
    total_trades = sum(len(all_trades_dfs[k]) for k in all_trades_dfs.keys())
    if total_trades == 0:
        print("\n⚠️ No trades found for any R:R target. Strategy conditions may need adjustment.")
        print("\nPossible reasons:")
        print("- Fractal window too strict")
        print("- Sweep conditions too restrictive")
        print("- MSS not occurring frequently")
        return
    
    # Calculate performance metrics for each R:R target
    all_metrics = {}
    for rr in RR_TARGETS:
        key = f'RR_{rr}'
        all_metrics[key] = calculate_performance_metrics(all_trades_dfs[key], rr)
    
    # Calculate cumulative P&L with risk management (done inside plot/print functions)
    
    # Print performance report
    print_performance_report(all_metrics, all_trades_dfs)
    
    # Print detailed view of last 5 trades from 2025 for each R:R target
    print_detailed_trades(all_trades_dfs, year=2025, num_trades=5)
    
    # Create visualizations
    plot_results(all_trades_dfs, all_metrics)
    
    # Save trades to CSV for each R:R target
    for rr in RR_TARGETS:
        key = f'RR_{rr}'
        if len(all_trades_dfs[key]) > 0:
            output_file = os.path.join(BASE_PATH, f'smc_reversal_trades_RR_{rr}.csv')
            all_trades_dfs[key].to_csv(output_file, index=False)
            print(f"✓ Saved trades to: smc_reversal_trades_RR_{rr}.csv")
    
    print("\n✅ Multi-target R:R backtest complete!")
    print("="*100)


if __name__ == "__main__":
    main()

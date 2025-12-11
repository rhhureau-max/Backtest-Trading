#!/usr/bin/env python3
"""
SMC Reversal Backtest Strategy: 01:00-07:00 Session
Smart Money Concepts (SMC) based reversal strategy with Sweeps, MSS, FVG, and Fibonacci entries.

Strategy Logic:
1. Identify Fractal Highs/Lows (swing structure)
2. Detect Liquidity Sweeps (price exceeds fractal but closes back or reverses)
3. Confirm MSS (Market Structure Shift - break of previous swing low after sweep)
4. Enter at 50% Fibonacci retracement of MSS leg
5. TP at first unfilled FVG, SL above sweep high

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
FRACTAL_LOOKBACK = 12        # Rolling max/min period for significant fractals
REVERSAL_WINDOW = 2          # Number of candles to check for bearish reversal (reduced to 2)
FIB_ENTRY_LEVEL = 0.5        # 50% Fibonacci retracement
MIN_FVG_SIZE = 5             # Minimum FVG size in points
DEBUG = False                # Enable debug output

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


def detect_fractals(df, window=1, lookback=12):
    """
    Detect SIGNIFICANT fractal highs and lows using stricter criteria.
    
    Fractal High must satisfy TWO conditions:
    1. Surrounded by lower candles: High[i] > max(High[i-window:i]) AND High[i] > max(High[i+1:i+window+1])
    2. Highest point in last 12 candles: High[i] == max(High[i-12:i+1])
    
    Fractal Low must satisfy TWO conditions:
    1. Surrounded by higher candles: Low[i] < min(Low[i-window:i]) AND Low[i] < min(Low[i+1:i+window+1])
    2. Lowest point in last 12 candles: Low[i] == min(Low[i-12:i+1])
    
    Args:
        window: Number of candles on each side for local comparison (default=1)
        lookback: Number of periods for rolling max/min (default=12)
    
    Returns:
        DataFrame with fractal_high and fractal_low boolean columns
    """
    df = df.copy()
    df['fractal_high'] = False
    df['fractal_low'] = False
    
    # Vectorized fractal detection
    high_arr = df['High'].values
    low_arr = df['Low'].values
    
    # Start from lookback to ensure we have enough history
    start_idx = max(window, lookback)
    
    for i in range(start_idx, len(df) - window):
        # Check fractal high - TWO CONDITIONS
        left_highs = high_arr[i-window:i]
        right_highs = high_arr[i+1:i+window+1]
        
        # Condition 1: Surrounded by lower candles
        surrounded_high = high_arr[i] > np.max(left_highs) and high_arr[i] > np.max(right_highs)
        
        # Condition 2: Highest in last 12 candles (rolling max)
        rolling_window = high_arr[i-lookback:i+1]
        is_rolling_max = high_arr[i] == np.max(rolling_window)
        
        if surrounded_high and is_rolling_max:
            df.loc[df.index[i], 'fractal_high'] = True
        
        # Check fractal low - TWO CONDITIONS
        left_lows = low_arr[i-window:i]
        right_lows = low_arr[i+1:i+window+1]
        
        # Condition 1: Surrounded by higher candles
        surrounded_low = low_arr[i] < np.min(left_lows) and low_arr[i] < np.min(right_lows)
        
        # Condition 2: Lowest in last 12 candles (rolling min)
        rolling_window_low = low_arr[i-lookback:i+1]
        is_rolling_min = low_arr[i] == np.min(rolling_window_low)
        
        if surrounded_low and is_rolling_min:
            df.loc[df.index[i], 'fractal_low'] = True
    
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


def simulate_trade(full_df, session_df, sweep_info, mss_info, entry_price, sl_price, tp_price, entry_time):
    """
    Simulate trade execution and determine outcome.
    
    Args:
        full_df: Full dataframe (for exits after session)
        session_df: Session dataframe
        sweep_info: Sweep information
        mss_info: MSS information
        entry_price: Entry price
        sl_price: Stop loss price
        tp_price: Take profit price
        entry_time: Entry time
    
    Returns:
        Trade result dict
    """
    # Find all candles after entry (including after session end)
    candles_after_entry = full_df[full_df['datetime'] > entry_time].copy()
    
    if len(candles_after_entry) == 0:
        return None  # No data after entry
    
    trade_result = {
        'entry_time': entry_time,
        'entry_price': entry_price,
        'sl_price': sl_price,
        'tp_price': tp_price,
        'exit_time': None,
        'exit_price': None,
        'outcome': None,  # 'win' or 'loss'
        'pnl_points': 0,
        'risk_points': sl_price - entry_price,
        'reward_points': entry_price - tp_price,
        'rr_ratio': 0
    }
    
    # Check each candle for SL or TP hit
    for idx, row in candles_after_entry.iterrows():
        # Check if SL hit (price goes above SL for short)
        if row['High'] >= sl_price:
            trade_result['exit_time'] = row['datetime']
            trade_result['exit_price'] = sl_price
            trade_result['outcome'] = 'loss'
            trade_result['pnl_points'] = entry_price - sl_price  # Negative for loss
            break
        
        # Check if TP hit (price goes to or below TP for short)
        if row['Low'] <= tp_price:
            trade_result['exit_time'] = row['datetime']
            trade_result['exit_price'] = tp_price
            trade_result['outcome'] = 'win'
            trade_result['pnl_points'] = entry_price - tp_price  # Positive for win
            break
    
    # If still open after all data, mark as incomplete
    if trade_result['outcome'] is None:
        return None
    
    # Calculate RR ratio
    if trade_result['risk_points'] != 0:
        trade_result['rr_ratio'] = abs(trade_result['reward_points'] / trade_result['risk_points'])
    
    return trade_result


def backtest_session(full_df, session_date, session_df):
    """
    Backtest the SMC reversal strategy for a single session.
    
    Args:
        full_df: Full dataframe (for exits after session)
        session_date: Date of the session
        session_df: Session data for this date
    
    Returns:
        List of trade results
    """
    trades = []
    
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
        
        # TP at first unfilled FVG or MSS low
        tp_price = find_first_unfilled_fvg(session_df, sweep, mss_info, mss_info['mss_time'])
        
        # Check if entry price makes sense (should be between mss_low and sweep_high)
        if not (mss_info['mss_low'] < entry_price < sweep['sweep_high']):
            continue
        
        # Check if TP is below entry (for short)
        if tp_price >= entry_price:
            continue
        
        # Check minimum R:R ratio (at least 1:1)
        risk = sl_price - entry_price
        reward = entry_price - tp_price
        if reward / risk < 0.8:  # At least 0.8:1 R:R
            continue
        
        # Simulate trade execution
        # Entry time is after MSS confirmation
        entry_time = mss_info['mss_time']
        
        # Make sure entry is within session
        if entry_time.time() >= SESSION_END:
            continue
        
        trade_result = simulate_trade(
            full_df, session_df, sweep, mss_info, 
            entry_price, sl_price, tp_price, entry_time
        )
        
        if trade_result is not None:
            trade_result['session_date'] = session_date
            trade_result['sweep_high'] = sweep['sweep_high']
            trade_result['mss_low'] = mss_info['mss_low']
            trades.append(trade_result)
    
    return trades


def run_backtest(df):
    """
    Run backtest across all sessions.
    
    Args:
        df: Full dataframe with all data
    
    Returns:
        DataFrame with all trades
    """
    print("\n" + "="*80)
    print("RUNNING SMC REVERSAL BACKTEST")
    print("="*80)
    
    # Filter for session times
    session_df = filter_session_data(df, SESSION_START, SESSION_END)
    
    all_trades = []
    
    # Group by session date
    sessions = session_df.groupby('Date')
    total_sessions = len(sessions)
    
    print(f"\nProcessing {total_sessions} sessions...")
    
    for i, (session_date, session_data) in enumerate(sessions):
        if (i + 1) % 50 == 0:
            print(f"  Processed {i+1}/{total_sessions} sessions...")
        
        session_trades = backtest_session(df, session_date, session_data)
        all_trades.extend(session_trades)
    
    print(f"\nBacktest complete! Found {len(all_trades)} trades.")
    
    if len(all_trades) == 0:
        print("No trades found. Strategy conditions may be too strict.")
        return pd.DataFrame()
    
    trades_df = pd.DataFrame(all_trades)
    return trades_df


def calculate_performance_metrics(trades_df):
    """
    Calculate performance metrics from trades.
    
    Returns:
        Dictionary with performance metrics
    """
    if len(trades_df) == 0:
        return None
    
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


def plot_results(trades_df, metrics):
    """
    Create visualization of backtest results.
    """
    if len(trades_df) == 0:
        print("No trades to plot.")
        return
    
    fig, axes = plt.subplots(2, 2, figsize=(18, 12))
    fig.suptitle('SMC Reversal Backtest Results: 01:00-07:00 Session', 
                 fontsize=16, fontweight='bold')
    
    # Subplot 1: Cumulative P&L (Equity Curve)
    axes[0, 0].plot(range(len(trades_df)), trades_df['cumulative_pnl'], 
                    linewidth=2, color='blue')
    axes[0, 0].axhline(y=0, color='black', linestyle='--', alpha=0.5)
    axes[0, 0].fill_between(range(len(trades_df)), trades_df['cumulative_pnl'], 
                           0, alpha=0.3, color='blue')
    axes[0, 0].set_xlabel('Trade Number', fontsize=12)
    axes[0, 0].set_ylabel('Cumulative P&L ($)', fontsize=12)
    axes[0, 0].set_title('Equity Curve (1% Risk per Trade)', fontsize=13, fontweight='bold')
    axes[0, 0].grid(True, alpha=0.3)
    
    # Subplot 2: Win/Loss distribution
    outcomes = trades_df['outcome'].value_counts()
    colors = ['green' if x == 'win' else 'red' for x in outcomes.index]
    axes[0, 1].bar(outcomes.index, outcomes.values, color=colors, alpha=0.7, edgecolor='black')
    axes[0, 1].set_xlabel('Outcome', fontsize=12)
    axes[0, 1].set_ylabel('Number of Trades', fontsize=12)
    axes[0, 1].set_title(f'Win/Loss Distribution (WR: {metrics["win_rate"]:.2f}%)', 
                        fontsize=13, fontweight='bold')
    axes[0, 1].grid(True, alpha=0.3, axis='y')
    
    # Add count labels on bars
    for i, (outcome, count) in enumerate(outcomes.items()):
        axes[0, 1].text(i, count, str(count), ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    # Subplot 3: P&L distribution
    axes[1, 0].hist(trades_df['pnl_points'], bins=30, color='purple', alpha=0.7, edgecolor='black')
    axes[1, 0].axvline(x=0, color='black', linestyle='--', linewidth=2)
    axes[1, 0].axvline(x=trades_df['pnl_points'].mean(), color='red', linestyle='--', 
                      linewidth=2, label=f'Mean: {trades_df["pnl_points"].mean():.2f}')
    axes[1, 0].set_xlabel('P&L (Points)', fontsize=12)
    axes[1, 0].set_ylabel('Frequency', fontsize=12)
    axes[1, 0].set_title('P&L Distribution per Trade', fontsize=13, fontweight='bold')
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)
    
    # Subplot 4: R:R Ratio distribution
    axes[1, 1].hist(trades_df['rr_ratio'], bins=20, color='orange', alpha=0.7, edgecolor='black')
    axes[1, 1].axvline(x=trades_df['rr_ratio'].mean(), color='red', linestyle='--', 
                      linewidth=2, label=f'Mean: {trades_df["rr_ratio"].mean():.2f}')
    axes[1, 1].set_xlabel('Risk:Reward Ratio', fontsize=12)
    axes[1, 1].set_ylabel('Frequency', fontsize=12)
    axes[1, 1].set_title('Risk:Reward Ratio Distribution', fontsize=13, fontweight='bold')
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(BASE_PATH, 'smc_reversal_backtest_results.png'), 
                dpi=300, bbox_inches='tight')
    print("\n✓ Saved: smc_reversal_backtest_results.png")


def print_performance_report(metrics, trades_df):
    """
    Print detailed performance report.
    """
    print("\n" + "="*80)
    print("PERFORMANCE METRICS")
    print("="*80)
    
    print(f"\nTotal Trades: {metrics['total_trades']}")
    print(f"Winning Trades: {metrics['wins']}")
    print(f"Losing Trades: {metrics['losses']}")
    print(f"Win Rate: {metrics['win_rate']:.2f}%")
    
    print(f"\n--- P&L Analysis ---")
    print(f"Total P&L: {metrics['total_pnl_points']:.2f} points")
    print(f"Average P&L per Trade: {metrics['avg_pnl_points']:.2f} points")
    print(f"Average Winner: {metrics['avg_win']:.2f} points")
    print(f"Average Loser: {metrics['avg_loss']:.2f} points")
    
    print(f"\n--- Risk Management ---")
    print(f"Average R:R Ratio: {metrics['avg_rr_ratio']:.2f}")
    print(f"Profit Factor: {metrics['profit_factor']:.2f}")
    
    print(f"\n--- Gross Figures ---")
    print(f"Gross Profit: {metrics['gross_profit']:.2f} points")
    print(f"Gross Loss: {metrics['gross_loss']:.2f} points")
    
    if len(trades_df) > 0:
        final_equity = trades_df.iloc[-1]['equity']
        total_return = ((final_equity - INITIAL_CAPITAL) / INITIAL_CAPITAL) * 100
        print(f"\n--- Account Performance (1% Risk) ---")
        print(f"Initial Capital: ${INITIAL_CAPITAL:,.2f}")
        print(f"Final Equity: ${final_equity:,.2f}")
        print(f"Total Return: {total_return:.2f}%")
    
    print("\n" + "="*80)


def print_detailed_trades(trades_df, year=2025, num_trades=5):
    """
    Print detailed information for the last N trades from a specific year.
    
    Args:
        trades_df: DataFrame with all trades
        year: Year to filter trades from
        num_trades: Number of trades to display
    """
    # Filter trades from specified year
    trades_df['year'] = pd.to_datetime(trades_df['entry_time']).dt.year
    year_trades = trades_df[trades_df['year'] == year].copy()
    
    if len(year_trades) == 0:
        print(f"\n⚠️ No trades found for year {year}")
        return
    
    # Get last N trades
    last_trades = year_trades.tail(num_trades)
    
    print("\n" + "="*80)
    print(f"LAST {num_trades} TRADES FROM {year} - DETAILED VIEW")
    print("="*80)
    
    for idx, (_, trade) in enumerate(last_trades.iterrows(), 1):
        print(f"\n{'='*80}")
        print(f"TRADE #{len(year_trades) - num_trades + idx} of {len(year_trades)} ({year})")
        print(f"{'='*80}")
        
        print(f"\n📅 Session Date: {trade['session_date']}")
        print(f"⏰ Entry Time: {trade['entry_time']}")
        print(f"🚪 Exit Time: {trade['exit_time']}")
        
        print(f"\n💰 PRICES:")
        print(f"   Sweep High: {trade['sweep_high']:.2f}")
        print(f"   MSS Low: {trade['mss_low']:.2f}")
        print(f"   Entry Price (50% Fib): {trade['entry_price']:.2f}")
        print(f"   Stop Loss: {trade['sl_price']:.2f}")
        print(f"   Take Profit: {trade['tp_price']:.2f}")
        print(f"   Exit Price: {trade['exit_price']:.2f}")
        
        print(f"\n📊 TRADE METRICS:")
        print(f"   Outcome: {'✅ WIN' if trade['outcome'] == 'win' else '❌ LOSS'}")
        print(f"   P&L: {trade['pnl_points']:+.2f} points")
        print(f"   Risk: {trade['risk_points']:.2f} points")
        print(f"   Reward: {trade['reward_points']:.2f} points")
        print(f"   R:R Ratio: {trade['rr_ratio']:.2f}")
        
        print(f"\n💵 ACCOUNT IMPACT:")
        print(f"   Equity After Trade: ${trade['equity']:,.2f}")
        print(f"   Cumulative P&L: ${trade['cumulative_pnl']:,.2f}")
    
    print("\n" + "="*80)
    print(f"\n📈 {year} YEAR SUMMARY:")
    print(f"   Total Trades: {len(year_trades)}")
    print(f"   Win Rate: {(year_trades['outcome'] == 'win').sum() / len(year_trades) * 100:.2f}%")
    print(f"   Total P&L: {year_trades['pnl_points'].sum():+.2f} points")
    print(f"   Average P&L: {year_trades['pnl_points'].mean():+.2f} points per trade")
    print("="*80)


def main():
    """
    Main execution function.
    """
    print("="*80)
    print("SMC REVERSAL BACKTEST: 01:00-07:00 SESSION")
    print("Smart Money Concepts with Sweeps, MSS, FVG, and Fibonacci Entries")
    print("="*80)
    
    # Load data from 2018 to today (all years)
    print("\n📊 Loading NQ 5-minute data from 2018 to 2025 (all available years)...\n")
    
    df = load_nq_data()  # No limit_years parameter = load all years
    
    # Run backtest
    trades_df = run_backtest(df)
    
    if len(trades_df) == 0:
        print("\n⚠️ No trades found. Strategy conditions may need adjustment.")
        print("\nPossible reasons:")
        print("- Fractal window too strict")
        print("- Sweep conditions too restrictive")
        print("- MSS not occurring frequently")
        print("- FVG not being created during MSS legs")
        return
    
    # Calculate performance metrics
    metrics = calculate_performance_metrics(trades_df)
    
    # Calculate cumulative P&L with risk management
    trades_df = calculate_cumulative_pnl(trades_df)
    
    # Print performance report
    print_performance_report(metrics, trades_df)
    
    # Print detailed view of last 5 trades from 2025
    print_detailed_trades(trades_df, year=2025, num_trades=5)
    
    # Create visualizations
    plot_results(trades_df, metrics)
    
    # Save trades to CSV
    output_file = os.path.join(BASE_PATH, 'smc_reversal_trades.csv')
    trades_df.to_csv(output_file, index=False)
    print(f"\n✓ Saved trades to: smc_reversal_trades.csv")
    
    print("\n✅ Backtest complete!")


if __name__ == "__main__":
    main()

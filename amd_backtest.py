"""
London Session AMD (Power of 3) Backtest System
================================================
Quantitative Trading Strategy based on ICT Time & Price Theory

AMD: Accumulation, Manipulation, Distribution
- Accumulation: 00:00-01:00 (Pre-session range)
- Manipulation: 01:00-02:30 (Trap moves)
- Distribution: Post-manipulation (True move)

Author: Quantitative Senior Strategist - Time & Price Theory Specialist
Date: 2025
"""

import pandas as pd
import numpy as np
import glob
from datetime import datetime, time
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# CONFIGURATION SECTION
# ============================================================================

# AMD Entry Mode: Choose 'A', 'B', or 'C'
AMD_MODE = 'A'  # A: Time-Based Judas | B: Fixed Deviation Trap | C: Pre-Session Sweep

# Risk Profile: Choose 1, 2, or 3
RISK_PROFILE = 1  # 1: The Turtle | 2: The Scalper | 3: The Runner

# Data Configuration
DATA_TIMEFRAME = '5m'  # Options: '1m', '5m', '15m'
START_YEAR = 2018
END_YEAR = 2025

# Trading Window (NO TIMEZONE CONVERSION - Raw time)
PRE_SESSION_START = time(0, 0)   # 00:00 (for Mode C)
SESSION_START = time(1, 0)       # 01:00 (True Open)
MANIPULATION_END = time(2, 30)   # 02:30 (End of manipulation window)
TRADING_END = time(5, 0)         # 05:00 (Hard exit)

# Mode B Specific Parameters
DEVIATION_THRESHOLD = 25  # Points for Fixed Deviation Trap

# ATR Configuration for Profile 3
ATR_PERIOD = 14

# Capital & Position Sizing
INITIAL_CAPITAL = 100000
POSITION_SIZE = 1  # Number of contracts per trade

# ============================================================================
# DATA LOADING AND PREPROCESSING
# ============================================================================

def load_data(timeframe='5m', start_year=2018, end_year=2025):
    """
    Load and concatenate CSV files for the specified timeframe and year range.
    CSV format: Date;Time;Open;High;Low;Close;Volume
    """
    all_data = []
    
    for year in range(start_year, end_year + 1):
        pattern = f"*{year}*{timeframe}.csv"
        files = glob.glob(pattern)
        
        for file in files:
            try:
                # Read CSV with semicolon delimiter
                df = pd.read_csv(file, sep=';', header=0)
                
                # Rename columns
                df.columns = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
                
                # Combine Date and Time into DateTime
                df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], 
                                                format='%d/%m/%Y %H:%M:%S',
                                                errors='coerce')
                
                # Drop rows with invalid dates
                df = df.dropna(subset=['DateTime'])
                
                # Keep only necessary columns
                df = df[['DateTime', 'Open', 'High', 'Low', 'Close', 'Volume']]
                
                all_data.append(df)
                print(f"✓ Loaded {file}: {len(df)} rows")
                
            except Exception as e:
                print(f"✗ Error loading {file}: {e}")
    
    if not all_data:
        raise ValueError(f"No data files found for timeframe {timeframe}")
    
    # Concatenate all data
    data = pd.concat(all_data, ignore_index=True)
    
    # Sort by DateTime
    data = data.sort_values('DateTime').reset_index(drop=True)
    
    # Remove duplicates
    data = data.drop_duplicates(subset=['DateTime']).reset_index(drop=True)
    
    print(f"\n{'='*60}")
    print(f"Total data loaded: {len(data)} rows")
    print(f"Date range: {data['DateTime'].min()} to {data['DateTime'].max()}")
    print(f"{'='*60}\n")
    
    return data

# ============================================================================
# TECHNICAL INDICATORS
# ============================================================================

def calculate_atr(data, period=14):
    """Calculate Average True Range (ATR)"""
    high = data['High']
    low = data['Low']
    close = data['Close'].shift(1)
    
    tr1 = high - low
    tr2 = abs(high - close)
    tr3 = abs(low - close)
    
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    atr = tr.rolling(window=period).mean()
    
    return atr

def filter_trading_hours(data, include_pre_session=False):
    """Filter data to include trading window and optionally pre-session"""
    data['Time'] = data['DateTime'].dt.time
    
    if include_pre_session:
        # Include 00:00-05:00 for Mode C
        mask = (data['Time'] >= PRE_SESSION_START) & (data['Time'] <= TRADING_END)
    else:
        # Only 01:00-05:00
        mask = (data['Time'] >= SESSION_START) & (data['Time'] <= TRADING_END)
    
    return data[mask].copy()

# ============================================================================
# MODE A: TIME-BASED JUDAS (TEMPORAL)
# ============================================================================

def mode_a_time_based_judas(data):
    """
    Mode A: Time-Based Judas (01:00-02:30 window)
    
    Buy Signal: Price drops below 01:00 Open, makes a low, then a candle closes
                above 01:00 Open after 01:15 (bullish reintegration)
    Sell Signal: Price rises above 01:00 Open, then a candle closes below it
    """
    data = data.copy()
    data['Date'] = data['DateTime'].dt.date
    data['Time'] = data['DateTime'].dt.time
    data['Hour'] = data['DateTime'].dt.hour
    data['Minute'] = data['DateTime'].dt.minute
    
    # Get 01:00 Open price for each day
    session_open = data[data['Time'] == SESSION_START].groupby('Date')['Open'].first()
    session_open = session_open.rename('SessionOpen')
    
    # Merge back and forward fill
    data = data.merge(session_open, on='Date', how='left')
    data['SessionOpen'] = data.groupby('Date')['SessionOpen'].ffill()
    
    # Manipulation window: 01:00 to 02:30
    data['InManipWindow'] = (data['Time'] >= SESSION_START) & (data['Time'] <= MANIPULATION_END)
    data['AfterFirstCandle'] = (data['Hour'] == 1) & (data['Minute'] > 15) | (data['Hour'] >= 2)
    
    # Track if price went below/above SessionOpen
    data['WentBelow'] = data.groupby('Date')['Low'].transform(lambda x: (x < data.loc[x.index, 'SessionOpen']).cummax())
    data['WentAbove'] = data.groupby('Date')['High'].transform(lambda x: (x > data.loc[x.index, 'SessionOpen']).cummax())
    
    # Generate signals
    data['Signal'] = 0
    
    # Buy signal: Went below, now closes above SessionOpen (after 01:15, within manip window)
    buy_condition = (
        data['InManipWindow'] &
        data['AfterFirstCandle'] &
        data['WentBelow'] &
        (data['Close'] > data['SessionOpen']) &
        (data['Close'].shift(1) <= data['SessionOpen'])  # Just crossed back
    )
    
    # Sell signal: Went above, now closes below SessionOpen
    sell_condition = (
        data['InManipWindow'] &
        data['AfterFirstCandle'] &
        data['WentAbove'] &
        (data['Close'] < data['SessionOpen']) &
        (data['Close'].shift(1) >= data['SessionOpen'])  # Just crossed back
    )
    
    data.loc[buy_condition, 'Signal'] = 1   # Long
    data.loc[sell_condition, 'Signal'] = -1  # Short
    
    return data.reset_index(drop=True)

# ============================================================================
# MODE B: FIXED DEVIATION TRAP (THRESHOLD)
# ============================================================================

def mode_b_fixed_deviation_trap(data, threshold=25):
    """
    Mode B: Fixed Deviation Trap (25 points threshold)
    
    Buy Signal: Price moves at least 25 points below 01:00 Open (deep discount),
                then entry when price touches back to 01:00 Open
    Sell Signal: Price moves at least 25 points above 01:00 Open
    """
    data = data.copy()
    data['Date'] = data['DateTime'].dt.date
    data['Time'] = data['DateTime'].dt.time
    
    # Get 01:00 Open price for each day
    session_open = data[data['Time'] == SESSION_START].groupby('Date')['Open'].first()
    session_open = session_open.rename('SessionOpen')
    
    # Merge back and forward fill
    data = data.merge(session_open, on='Date', how='left')
    data['SessionOpen'] = data.groupby('Date')['SessionOpen'].ffill()
    
    # Calculate deviation from session open
    data['Deviation'] = data['Close'] - data['SessionOpen']
    
    # Track if we've reached the threshold (vectorized)
    data['BuyThresholdMet'] = data['Low'] <= (data['SessionOpen'] - threshold)
    data['SellThresholdMet'] = data['High'] >= (data['SessionOpen'] + threshold)
    
    # Use cummax within each date group
    data['ReachedBuyThreshold'] = data.groupby('Date')['BuyThresholdMet'].cummax()
    data['ReachedSellThreshold'] = data.groupby('Date')['SellThresholdMet'].cummax()
    
    # Generate signals
    data['Signal'] = 0
    
    # Buy signal: Reached buy threshold, now price touches SessionOpen from below
    buy_condition = (
        (data['Time'] >= SESSION_START) &
        (data['Time'] <= TRADING_END) &
        data['ReachedBuyThreshold'] &
        (data['High'] >= data['SessionOpen']) &  # Touches or crosses open
        (data['Low'].shift(1) < data['SessionOpen'])  # Was below
    )
    
    # Sell signal: Reached sell threshold, now price touches SessionOpen from above
    sell_condition = (
        (data['Time'] >= SESSION_START) &
        (data['Time'] <= TRADING_END) &
        data['ReachedSellThreshold'] &
        (data['Low'] <= data['SessionOpen']) &  # Touches or crosses open
        (data['High'].shift(1) > data['SessionOpen'])  # Was above
    )
    
    data.loc[buy_condition, 'Signal'] = 1   # Long
    data.loc[sell_condition, 'Signal'] = -1  # Short
    
    return data.reset_index(drop=True)

# ============================================================================
# MODE C: PRE-SESSION SWEEP (STOP HUNT)
# ============================================================================

def mode_c_pre_session_sweep(data):
    """
    Mode C: Pre-Session Sweep (00:00-01:00 range)
    
    Finds High/Low of 00:00-01:00 period
    Buy Signal: Price breaks below pre-session Low but closes above it (SFP - Swing Failure Pattern)
    Sell Signal: Price breaks above pre-session High but closes below it
    """
    data = data.copy()
    data['Date'] = data['DateTime'].dt.date
    data['Time'] = data['DateTime'].dt.time
    data['Hour'] = data['DateTime'].dt.hour
    
    # Identify pre-session period (00:00-01:00)
    data['PreSession'] = (data['Time'] >= PRE_SESSION_START) & (data['Time'] < SESSION_START)
    
    # Calculate pre-session High/Low for each day
    pre_session_stats = data[data['PreSession']].groupby('Date').agg({
        'High': 'max',
        'Low': 'min'
    }).rename(columns={'High': 'PreSessionHigh', 'Low': 'PreSessionLow'})
    
    # Merge back to main data
    data = data.merge(pre_session_stats, on='Date', how='left')
    
    # Forward fill the pre-session levels
    data['PreSessionHigh'] = data.groupby('Date')['PreSessionHigh'].ffill()
    data['PreSessionLow'] = data.groupby('Date')['PreSessionLow'].ffill()
    
    # Generate signals (only after 01:00)
    data['Signal'] = 0
    data['AfterSession'] = data['Time'] >= SESSION_START
    
    # Buy signal: Low breaks below PreSessionLow but Close is above it (SFP)
    buy_condition = (
        data['AfterSession'] &
        (data['Low'] < data['PreSessionLow']) &
        (data['Close'] > data['PreSessionLow']) &
        (data['Time'] <= TRADING_END)
    )
    
    # Sell signal: High breaks above PreSessionHigh but Close is below it (SFP)
    sell_condition = (
        data['AfterSession'] &
        (data['High'] > data['PreSessionHigh']) &
        (data['Close'] < data['PreSessionHigh']) &
        (data['Time'] <= TRADING_END)
    )
    
    data.loc[buy_condition, 'Signal'] = 1   # Long
    data.loc[sell_condition, 'Signal'] = -1  # Short
    
    return data.reset_index(drop=True)

# ============================================================================
# BACKTESTING ENGINE WITH RISK PROFILES
# ============================================================================

def calculate_manipulation_extreme(data, entry_idx, direction):
    """
    Calculate the extreme (High/Low) during manipulation phase for Profile 1
    """
    entry_date = data.loc[entry_idx, 'Date']
    entry_time = data.loc[entry_idx, 'DateTime']
    
    # Get all rows for this date up to entry time, starting from 01:00
    session_start_time = pd.Timestamp.combine(entry_date, SESSION_START)
    
    mask = (
        (data['Date'] == entry_date) &
        (data['DateTime'] >= session_start_time) &
        (data['DateTime'] <= entry_time)
    )
    
    manipulation_data = data[mask]
    
    if direction == 1:  # Long - use the low extreme
        return manipulation_data['Low'].min()
    else:  # Short - use the high extreme
        return manipulation_data['High'].max()

def backtest_amd(data, amd_mode, risk_profile):
    """
    Backtest with AMD mode and risk profile
    """
    data = data.copy()
    data = data.reset_index(drop=True)
    
    # Calculate ATR if needed
    if risk_profile == 3:
        data['ATR'] = calculate_atr(data, ATR_PERIOD)
    
    # Initialize tracking columns
    data['Position'] = 0
    data['EntryPrice'] = 0.0
    data['StopLoss'] = 0.0
    data['TakeProfit'] = 0.0
    data['PnL'] = 0.0
    data['Trade'] = 0
    data['TradeExit'] = ''
    
    # Trading state variables
    position = 0
    entry_price = 0.0
    stop_loss = 0.0
    take_profit = 0.0
    trade_count = 0
    equity = INITIAL_CAPITAL
    equity_curve = []
    trades = []
    entry_idx = None
    
    for i in range(len(data)):
        current_time = data.loc[i, 'DateTime'].time()
        current_price = data.loc[i, 'Close']
        current_high = data.loc[i, 'High']
        current_low = data.loc[i, 'Low']
        signal = data.loc[i, 'Signal']
        
        # Hard exit at 05:00
        if current_time >= TRADING_END and position != 0:
            pnl = (current_price - entry_price) * position * POSITION_SIZE
            equity += pnl
            
            trades.append({
                'EntryTime': data.loc[entry_idx, 'DateTime'],
                'ExitTime': data.loc[i, 'DateTime'],
                'Direction': 'Long' if position == 1 else 'Short',
                'EntryPrice': entry_price,
                'ExitPrice': current_price,
                'StopLoss': stop_loss,
                'TakeProfit': take_profit if risk_profile != 3 else 'Runner',
                'PnL': pnl,
                'ExitReason': 'HardExit'
            })
            
            data.loc[i, 'PnL'] = pnl
            data.loc[i, 'TradeExit'] = 'HardExit'
            position = 0
            entry_price = 0.0
            entry_idx = None
        
        # Check for stop-loss or take-profit if in a position
        if position != 0:
            # Long position checks
            if position == 1:
                # Check stop-loss
                if current_low <= stop_loss:
                    pnl = (stop_loss - entry_price) * POSITION_SIZE
                    equity += pnl
                    
                    trades.append({
                        'EntryTime': data.loc[entry_idx, 'DateTime'],
                        'ExitTime': data.loc[i, 'DateTime'],
                        'Direction': 'Long',
                        'EntryPrice': entry_price,
                        'ExitPrice': stop_loss,
                        'StopLoss': stop_loss,
                        'TakeProfit': take_profit if risk_profile != 3 else 'Runner',
                        'PnL': pnl,
                        'ExitReason': 'StopLoss'
                    })
                    
                    data.loc[i, 'PnL'] = pnl
                    data.loc[i, 'TradeExit'] = 'StopLoss'
                    position = 0
                    entry_price = 0.0
                    entry_idx = None
                
                # Check take-profit (not for Profile 3 - The Runner)
                elif risk_profile != 3 and current_high >= take_profit:
                    pnl = (take_profit - entry_price) * POSITION_SIZE
                    equity += pnl
                    
                    trades.append({
                        'EntryTime': data.loc[entry_idx, 'DateTime'],
                        'ExitTime': data.loc[i, 'DateTime'],
                        'Direction': 'Long',
                        'EntryPrice': entry_price,
                        'ExitPrice': take_profit,
                        'StopLoss': stop_loss,
                        'TakeProfit': take_profit,
                        'PnL': pnl,
                        'ExitReason': 'TakeProfit'
                    })
                    
                    data.loc[i, 'PnL'] = pnl
                    data.loc[i, 'TradeExit'] = 'TakeProfit'
                    position = 0
                    entry_price = 0.0
                    entry_idx = None
            
            # Short position checks
            elif position == -1:
                # Check stop-loss
                if current_high >= stop_loss:
                    pnl = (entry_price - stop_loss) * POSITION_SIZE
                    equity += pnl
                    
                    trades.append({
                        'EntryTime': data.loc[entry_idx, 'DateTime'],
                        'ExitTime': data.loc[i, 'DateTime'],
                        'Direction': 'Short',
                        'EntryPrice': entry_price,
                        'ExitPrice': stop_loss,
                        'StopLoss': stop_loss,
                        'TakeProfit': take_profit if risk_profile != 3 else 'Runner',
                        'PnL': pnl,
                        'ExitReason': 'StopLoss'
                    })
                    
                    data.loc[i, 'PnL'] = pnl
                    data.loc[i, 'TradeExit'] = 'StopLoss'
                    position = 0
                    entry_price = 0.0
                    entry_idx = None
                
                # Check take-profit (not for Profile 3)
                elif risk_profile != 3 and current_low <= take_profit:
                    pnl = (entry_price - take_profit) * POSITION_SIZE
                    equity += pnl
                    
                    trades.append({
                        'EntryTime': data.loc[entry_idx, 'DateTime'],
                        'ExitTime': data.loc[i, 'DateTime'],
                        'Direction': 'Short',
                        'EntryPrice': entry_price,
                        'ExitPrice': take_profit,
                        'StopLoss': stop_loss,
                        'TakeProfit': take_profit,
                        'PnL': pnl,
                        'ExitReason': 'TakeProfit'
                    })
                    
                    data.loc[i, 'PnL'] = pnl
                    data.loc[i, 'TradeExit'] = 'TakeProfit'
                    position = 0
                    entry_price = 0.0
                    entry_idx = None
        
        # Enter new position if flat and signal present
        if position == 0 and signal != 0:
            trade_count += 1
            position = signal
            entry_price = current_price
            entry_idx = i
            
            # Calculate stop-loss and take-profit based on risk profile
            if risk_profile == 1:  # The Turtle - Structural
                # Stop at manipulation extreme
                extreme = calculate_manipulation_extreme(data, i, position)
                
                if position == 1:  # Long
                    stop_loss = extreme
                    sl_distance = entry_price - stop_loss
                    take_profit = entry_price + (2.5 * sl_distance)
                else:  # Short
                    stop_loss = extreme
                    sl_distance = stop_loss - entry_price
                    take_profit = entry_price - (2.5 * sl_distance)
                    
            elif risk_profile == 2:  # The Scalper - Fixed
                if position == 1:  # Long
                    stop_loss = entry_price - 20
                    take_profit = entry_price + 50
                else:  # Short
                    stop_loss = entry_price + 20
                    take_profit = entry_price - 50
                    
            elif risk_profile == 3:  # The Runner - ATR, no TP
                atr_value = data.loc[i, 'ATR']
                if pd.notna(atr_value):
                    if position == 1:  # Long
                        stop_loss = entry_price - (1 * atr_value)
                    else:  # Short
                        stop_loss = entry_price + (1 * atr_value)
                else:
                    # Fallback to Profile 2 if ATR not available
                    if position == 1:
                        stop_loss = entry_price - 20
                    else:
                        stop_loss = entry_price + 20
                
                take_profit = 0  # No TP for runner - runs until hard exit
            
            data.loc[i, 'Trade'] = trade_count
            data.loc[i, 'EntryPrice'] = entry_price
            data.loc[i, 'StopLoss'] = stop_loss
            data.loc[i, 'TakeProfit'] = take_profit if risk_profile != 3 else 0
        
        # Update position tracking
        data.loc[i, 'Position'] = position
        equity_curve.append(equity)
    
    # Convert trades list to DataFrame
    trades_df = pd.DataFrame(trades)
    
    return data, trades_df, equity_curve

# ============================================================================
# PERFORMANCE METRICS
# ============================================================================

def calculate_metrics(trades_df, equity_curve, initial_capital):
    """Calculate performance metrics including Max Drawdown"""
    if len(trades_df) == 0:
        return {
            'Total Trades': 0,
            'Win Rate (%)': 0,
            'Profit Factor': 0,
            'Total PnL': 0,
            'Final Equity': initial_capital,
            'Return (%)': 0,
            'Max Drawdown (%)': 0
        }
    
    # Basic metrics
    total_trades = len(trades_df)
    winning_trades = len(trades_df[trades_df['PnL'] > 0])
    losing_trades = len(trades_df[trades_df['PnL'] < 0])
    
    win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
    
    # Profit factor
    gross_profit = trades_df[trades_df['PnL'] > 0]['PnL'].sum()
    gross_loss = abs(trades_df[trades_df['PnL'] < 0]['PnL'].sum())
    profit_factor = (gross_profit / gross_loss) if gross_loss > 0 else 0
    
    # Total PnL
    total_pnl = trades_df['PnL'].sum()
    final_equity = equity_curve[-1] if equity_curve else initial_capital
    total_return = ((final_equity - initial_capital) / initial_capital * 100)
    
    # Max Drawdown
    equity_series = pd.Series(equity_curve)
    running_max = equity_series.expanding().max()
    drawdown = (equity_series - running_max) / running_max * 100
    max_drawdown = drawdown.min()
    
    metrics = {
        'Total Trades': total_trades,
        'Winning Trades': winning_trades,
        'Losing Trades': losing_trades,
        'Win Rate (%)': round(win_rate, 2),
        'Profit Factor': round(profit_factor, 2),
        'Total PnL': round(total_pnl, 2),
        'Gross Profit': round(gross_profit, 2),
        'Gross Loss': round(gross_loss, 2),
        'Initial Capital': initial_capital,
        'Final Equity': round(final_equity, 2),
        'Return (%)': round(total_return, 2),
        'Max Drawdown (%)': round(max_drawdown, 2)
    }
    
    return metrics

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main execution function"""
    print("\n" + "="*70)
    print("LONDON SESSION AMD (POWER OF 3) BACKTEST SYSTEM")
    print("Time & Price Theory - ICT Strategy")
    print("="*70)
    
    # Display configuration
    mode_names = {
        'A': 'Time-Based Judas (Temporal)',
        'B': 'Fixed Deviation Trap (25 points)',
        'C': 'Pre-Session Sweep (Stop Hunt)'
    }
    
    profile_names = {
        1: 'The Turtle (Structural SL, 1:2.5 ratio)',
        2: 'The Scalper (Fixed 20/50 points)',
        3: 'The Runner (ATR-based, runs to 05:00)'
    }
    
    print(f"\n📊 CONFIGURATION:")
    print(f"  AMD Mode: {AMD_MODE} - {mode_names[AMD_MODE]}")
    print(f"  Risk Profile: {RISK_PROFILE} - {profile_names[RISK_PROFILE]}")
    print(f"  Timeframe: {DATA_TIMEFRAME}")
    print(f"  Years: {START_YEAR} - {END_YEAR}")
    print(f"  Session Start: {SESSION_START} (True Open)")
    print(f"  Manipulation Window: {SESSION_START} - {MANIPULATION_END}")
    print(f"  Hard Exit: {TRADING_END}")
    print(f"  Initial Capital: ${INITIAL_CAPITAL:,}")
    print()
    
    # Load data
    print("📂 Loading data...")
    data = load_data(DATA_TIMEFRAME, START_YEAR, END_YEAR)
    
    # Filter to trading hours (include pre-session for Mode C)
    include_pre = (AMD_MODE == 'C')
    print(f"🕐 Filtering to trading hours {'(including 00:00-01:00 pre-session)' if include_pre else '(01:00-05:00)'}...")
    data = filter_trading_hours(data, include_pre_session=include_pre)
    print(f"  Rows after filtering: {len(data)}")
    print()
    
    # Apply selected AMD mode
    print(f"🎯 Applying AMD Mode {AMD_MODE}: {mode_names[AMD_MODE]}...")
    
    if AMD_MODE == 'A':
        data = mode_a_time_based_judas(data)
    elif AMD_MODE == 'B':
        data = mode_b_fixed_deviation_trap(data, DEVIATION_THRESHOLD)
    elif AMD_MODE == 'C':
        data = mode_c_pre_session_sweep(data)
    else:
        raise ValueError(f"Invalid AMD mode: {AMD_MODE}")
    
    signals_count = len(data[data['Signal'] != 0])
    print(f"  Generated {signals_count} signals")
    print()
    
    # Run backtest
    print(f"⚙️  Running backtest with Risk Profile {RISK_PROFILE}: {profile_names[RISK_PROFILE]}...")
    data, trades_df, equity_curve = backtest_amd(data, AMD_MODE, RISK_PROFILE)
    print(f"  Completed {len(trades_df)} trades")
    print()
    
    # Calculate metrics
    print("📈 Calculating performance metrics...")
    metrics = calculate_metrics(trades_df, equity_curve, INITIAL_CAPITAL)
    print()
    
    # Display results
    print("="*70)
    print("BACKTEST RESULTS - AMD STRATEGY")
    print("="*70)
    
    for key, value in metrics.items():
        if isinstance(value, float):
            print(f"  {key:.<40} {value:>25,.2f}")
        else:
            print(f"  {key:.<40} {value:>25,}")
    
    print("="*70)
    
    # Display sample trades
    if len(trades_df) > 0:
        print("\n📋 Sample Trades (First 10):")
        display_cols = ['EntryTime', 'ExitTime', 'Direction', 'EntryPrice', 
                       'ExitPrice', 'PnL', 'ExitReason']
        print(trades_df[display_cols].head(10).to_string(index=False))
        
        # Save results to CSV
        output_file = f"amd_results_mode{AMD_MODE}_profile{RISK_PROFILE}_{DATA_TIMEFRAME}.csv"
        trades_df.to_csv(output_file, index=False)
        print(f"\n💾 Full results saved to: {output_file}")
    
    print("\n✅ AMD Backtest complete!\n")
    
    return data, trades_df, equity_curve, metrics


if __name__ == "__main__":
    data, trades_df, equity_curve, metrics = main()

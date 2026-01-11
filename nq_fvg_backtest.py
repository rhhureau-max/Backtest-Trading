#!/usr/bin/env python3
"""
NQ Futures FVG Inversion Strategy Backtest
===========================================

Strategy: Fair Value Gap (FVG) Inversion
Timeframe: 5 Minutes
Data: NQ Futures (2018-2024)
Sessions: London (01:00-04:00 CT) and New York (08:30-11:00 CT)

Strategy Rules:
1. Bearish FVG: Created when Low[i-2] > High[i]. Gap between High[i] and Low[i-2].
2. Bullish FVG: Created when High[i-2] < Low[i]. Gap between High[i-2] and Low[i].
3. LONG Signal: Price creates Bearish FVG, later candle closes ABOVE its top.
4. SHORT Signal: Price creates Bullish FVG, later candle closes BELOW its bottom.
5. One Bullet Rule: Only ONE trade per session (London or New York).
6. Risk Management: 1:1 RR, SL at signal candle's low (LONG) or high (SHORT).

Author: Senior Quantitative Trader
Date: 2026-01-11
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, time
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# DATA LOADING AND PREPROCESSING
# ============================================================================

def load_data(filepath):
    """
    Load NQ 5-minute data from CSV file.
    
    Args:
        filepath: Path to the CSV file
        
    Returns:
        DataFrame with OHLCV data and datetime index
    """
    print("Loading data...")
    df = pd.read_csv(filepath, sep=';')
    
    # Combine Date and Time columns into a single datetime column
    df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%d/%m/%Y %H:%M:%S')
    
    # Convert price columns to float
    df['Open'] = df['Open'].astype(float)
    df['High'] = df['High'].astype(float)
    df['Low'] = df['Low'].astype(float)
    df['Close'] = df['Close'].astype(float)
    df['Volume'] = df['Volume'].astype(float)
    
    # Set datetime as index and sort
    df.set_index('Datetime', inplace=True)
    df.sort_index(inplace=True)
    
    print(f"Loaded {len(df)} candles from {df.index[0]} to {df.index[-1]}")
    return df

# ============================================================================
# FVG DETECTION
# ============================================================================

def detect_fvgs(df):
    """
    Detect Fair Value Gaps (FVGs) in the price data.
    
    Bearish FVG: Low[i-2] > High[i] -> Gap from High[i] to Low[i-2]
    Bullish FVG: High[i-2] < Low[i] -> Gap from High[i-2] to Low[i]
    
    Args:
        df: DataFrame with OHLC data
        
    Returns:
        DataFrame with FVG columns added
    """
    df = df.copy()
    
    # Initialize FVG columns
    df['Bearish_FVG'] = False
    df['Bearish_FVG_Top'] = np.nan
    df['Bearish_FVG_Bottom'] = np.nan
    df['Bullish_FVG'] = False
    df['Bullish_FVG_Top'] = np.nan
    df['Bullish_FVG_Bottom'] = np.nan
    
    # Detect FVGs (need at least 3 candles)
    for i in range(2, len(df)):
        # Bearish FVG: Low[i-2] > High[i]
        if df['Low'].iloc[i-2] > df['High'].iloc[i]:
            df['Bearish_FVG'].iloc[i] = True
            df['Bearish_FVG_Top'].iloc[i] = df['Low'].iloc[i-2]  # Top of the gap
            df['Bearish_FVG_Bottom'].iloc[i] = df['High'].iloc[i]  # Bottom of the gap
        
        # Bullish FVG: High[i-2] < Low[i]
        if df['High'].iloc[i-2] < df['Low'].iloc[i]:
            df['Bullish_FVG'].iloc[i] = True
            df['Bullish_FVG_Top'].iloc[i] = df['Low'].iloc[i]  # Top of the gap
            df['Bullish_FVG_Bottom'].iloc[i] = df['High'].iloc[i-2]  # Bottom of the gap
    
    return df

# ============================================================================
# SESSION MANAGEMENT
# ============================================================================

def identify_sessions(df):
    """
    Identify London and New York trading sessions.
    
    London: 01:00 - 04:00 CT
    New York: 08:30 - 11:00 CT
    
    Args:
        df: DataFrame with datetime index
        
    Returns:
        DataFrame with session columns added
    """
    df = df.copy()
    
    # Extract time component
    df['Time'] = df.index.time
    
    # Define session times
    london_start = time(1, 0)
    london_end = time(4, 0)
    ny_start = time(8, 30)
    ny_end = time(11, 0)
    
    # Identify sessions
    df['London_Session'] = df['Time'].apply(
        lambda t: london_start <= t < london_end
    )
    df['NY_Session'] = df['Time'].apply(
        lambda t: ny_start <= t < ny_end
    )
    df['In_Session'] = df['London_Session'] | df['NY_Session']
    
    # Identify session type
    df['Session_Type'] = 'None'
    df.loc[df['London_Session'], 'Session_Type'] = 'London'
    df.loc[df['NY_Session'], 'Session_Type'] = 'New York'
    
    return df

# ============================================================================
# SIGNAL GENERATION - FVG INVERSION
# ============================================================================

def generate_signals(df):
    """
    Generate trading signals based on FVG Inversion strategy.
    
    LONG Signal: Price creates Bearish FVG, later candle closes ABOVE its top
    SHORT Signal: Price creates Bullish FVG, later candle closes BELOW its bottom
    
    Args:
        df: DataFrame with FVG data
        
    Returns:
        DataFrame with signal columns added
    """
    df = df.copy()
    
    # Initialize signal columns
    df['Signal'] = 'None'
    df['Signal_Price'] = np.nan
    df['FVG_Level'] = np.nan
    
    # Use numpy arrays for faster access
    close_prices = df['Close'].values
    bearish_fvg = df['Bearish_FVG'].values
    bearish_fvg_top = df['Bearish_FVG_Top'].values
    bullish_fvg = df['Bullish_FVG'].values
    bullish_fvg_bottom = df['Bullish_FVG_Bottom'].values
    
    signals = ['None'] * len(df)
    
    # Track active FVGs (FVGs that haven't been inverted yet)
    active_bearish_fvgs = []  # List of (index, top)
    active_bullish_fvgs = []  # List of (index, bottom)
    
    for i in range(len(df)):
        # Add new FVGs to active lists
        if bearish_fvg[i]:
            active_bearish_fvgs.append((i, bearish_fvg_top[i]))
        
        if bullish_fvg[i]:
            active_bullish_fvgs.append((i, bullish_fvg_bottom[i]))
        
        # Check for LONG signals (close above Bearish FVG top)
        for idx, (fvg_idx, fvg_top) in enumerate(active_bearish_fvgs):
            if close_prices[i] > fvg_top:
                signals[i] = 'LONG'
                df.loc[df.index[i], 'Signal_Price'] = close_prices[i]
                df.loc[df.index[i], 'FVG_Level'] = fvg_top
                # Remove this FVG as it's been inverted
                active_bearish_fvgs.pop(idx)
                break  # Only one signal per candle
        
        # Check for SHORT signals (close below Bullish FVG bottom)
        if signals[i] == 'None':  # Only if no LONG signal
            for idx, (fvg_idx, fvg_bottom) in enumerate(active_bullish_fvgs):
                if close_prices[i] < fvg_bottom:
                    signals[i] = 'SHORT'
                    df.loc[df.index[i], 'Signal_Price'] = close_prices[i]
                    df.loc[df.index[i], 'FVG_Level'] = fvg_bottom
                    # Remove this FVG as it's been inverted
                    active_bullish_fvgs.pop(idx)
                    break  # Only one signal per candle
    
    df['Signal'] = signals
    return df

# ============================================================================
# BACKTEST ENGINE - ONE BULLET RULE
# ============================================================================

class Trade:
    """Simple trade class to track trade details."""
    def __init__(self, entry_time, direction, entry_price, sl_price, tp_price, session):
        self.entry_time = entry_time
        self.direction = direction
        self.entry_price = entry_price
        self.sl_price = sl_price
        self.tp_price = tp_price
        self.session = session
        self.exit_time = None
        self.exit_price = None
        self.exit_reason = None
        self.pnl = 0
        self.is_winner = False
        
    def close_trade(self, exit_time, exit_price, exit_reason):
        """Close the trade and calculate P&L."""
        self.exit_time = exit_time
        self.exit_price = exit_price
        self.exit_reason = exit_reason
        
        # Calculate P&L in points
        if self.direction == 'LONG':
            self.pnl = exit_price - self.entry_price
        else:  # SHORT
            self.pnl = self.entry_price - exit_price
        
        self.is_winner = self.pnl > 0

def run_backtest(df):
    """
    Run the backtest with "One Bullet Rule" - only one trade per session.
    
    Args:
        df: DataFrame with signals and session data
        
    Returns:
        List of Trade objects
    """
    print("\nRunning backtest...")
    
    trades = []
    current_trade = None
    
    # Track if we've taken a trade in the current session
    trade_taken_today = {'London': False, 'New York': False}
    current_date = None
    
    # Use numpy arrays for faster access
    highs = df['High'].values
    lows = df['Low'].values
    closes = df['Close'].values
    in_session = df['In_Session'].values
    signals = df['Signal'].values
    session_types = df['Session_Type'].values
    datetimes = df.index.values
    
    for i in range(len(df)):
        current_datetime = pd.Timestamp(datetimes[i])
        
        # Reset trade_taken flags at the start of a new day
        if current_date is None or current_datetime.date() != current_date:
            current_date = current_datetime.date()
            trade_taken_today = {'London': False, 'New York': False}
        
        # Check if we have an open trade
        if current_trade is not None:
            # Check for Stop Loss hit
            if current_trade.direction == 'LONG':
                if lows[i] <= current_trade.sl_price:
                    current_trade.close_trade(current_datetime, current_trade.sl_price, 'SL')
                    trades.append(current_trade)
                    current_trade = None
                    continue
                # Check for Take Profit hit
                elif highs[i] >= current_trade.tp_price:
                    current_trade.close_trade(current_datetime, current_trade.tp_price, 'TP')
                    trades.append(current_trade)
                    current_trade = None
                    continue
            
            else:  # SHORT
                if highs[i] >= current_trade.sl_price:
                    current_trade.close_trade(current_datetime, current_trade.sl_price, 'SL')
                    trades.append(current_trade)
                    current_trade = None
                    continue
                elif lows[i] <= current_trade.tp_price:
                    current_trade.close_trade(current_datetime, current_trade.tp_price, 'TP')
                    trades.append(current_trade)
                    current_trade = None
                    continue
        
        # Look for new signals (only if not in a trade and in a session)
        if current_trade is None and in_session[i] and signals[i] != 'None':
            session_type = session_types[i]
            
            # Check if we haven't taken a trade in this session today
            if not trade_taken_today[session_type]:
                # Enter trade at the close of the signal candle
                entry_price = closes[i]
                
                if signals[i] == 'LONG':
                    # Stop Loss just below the low of the signal candle
                    sl_price = lows[i] - 0.25  # Small buffer
                    risk = entry_price - sl_price
                    tp_price = entry_price + risk  # 1:1 RR
                    
                    current_trade = Trade(
                        entry_time=current_datetime,
                        direction='LONG',
                        entry_price=entry_price,
                        sl_price=sl_price,
                        tp_price=tp_price,
                        session=session_type
                    )
                
                elif signals[i] == 'SHORT':
                    # Stop Loss just above the high of the signal candle
                    sl_price = highs[i] + 0.25  # Small buffer
                    risk = sl_price - entry_price
                    tp_price = entry_price - risk  # 1:1 RR
                    
                    current_trade = Trade(
                        entry_time=current_datetime,
                        direction='SHORT',
                        entry_price=entry_price,
                        sl_price=sl_price,
                        tp_price=tp_price,
                        session=session_type
                    )
                
                # Mark that we've taken a trade in this session
                trade_taken_today[session_type] = True
        
        # Progress indicator every 50000 candles
        if (i + 1) % 50000 == 0:
            print(f"  Processed {i+1}/{len(df)} candles...")
    
    # Close any remaining open trade at the end
    if current_trade is not None:
        current_trade.close_trade(pd.Timestamp(datetimes[-1]), closes[-1], 'EOD')
        trades.append(current_trade)
    
    print(f"Backtest complete. Total trades: {len(trades)}")
    return trades

# ============================================================================
# PERFORMANCE ANALYSIS
# ============================================================================

def analyze_performance(trades):
    """
    Analyze trading performance and generate statistics.
    
    Args:
        trades: List of Trade objects
        
    Returns:
        Dictionary with performance metrics by session
    """
    if len(trades) == 0:
        print("No trades to analyze!")
        return None
    
    # Convert trades to DataFrame for easier analysis
    trade_data = []
    for trade in trades:
        trade_data.append({
            'Entry_Time': trade.entry_time,
            'Direction': trade.direction,
            'Entry_Price': trade.entry_price,
            'Exit_Time': trade.exit_time,
            'Exit_Price': trade.exit_price,
            'Exit_Reason': trade.exit_reason,
            'PnL': trade.pnl,
            'Is_Winner': trade.is_winner,
            'Session': trade.session
        })
    
    df_trades = pd.DataFrame(trade_data)
    
    # Calculate metrics by session
    sessions = ['London', 'New York', 'Overall']
    results = {}
    
    for session in sessions:
        if session == 'Overall':
            session_trades = df_trades
        else:
            session_trades = df_trades[df_trades['Session'] == session]
        
        if len(session_trades) == 0:
            results[session] = {
                'Total_Trades': 0,
                'Winners': 0,
                'Losers': 0,
                'Win_Rate': 0,
                'Total_PnL': 0,
                'Avg_Win': 0,
                'Avg_Loss': 0,
                'Profit_Factor': 0
            }
            continue
        
        winners = session_trades[session_trades['Is_Winner'] == True]
        losers = session_trades[session_trades['Is_Winner'] == False]
        
        total_trades = len(session_trades)
        num_winners = len(winners)
        num_losers = len(losers)
        win_rate = (num_winners / total_trades * 100) if total_trades > 0 else 0
        
        total_pnl = session_trades['PnL'].sum()
        avg_win = winners['PnL'].mean() if len(winners) > 0 else 0
        avg_loss = losers['PnL'].mean() if len(losers) > 0 else 0
        
        gross_profit = winners['PnL'].sum() if len(winners) > 0 else 0
        gross_loss = abs(losers['PnL'].sum()) if len(losers) > 0 else 0
        profit_factor = (gross_profit / gross_loss) if gross_loss > 0 else 0
        
        results[session] = {
            'Total_Trades': total_trades,
            'Winners': num_winners,
            'Losers': num_losers,
            'Win_Rate': win_rate,
            'Total_PnL': total_pnl,
            'Avg_Win': avg_win,
            'Avg_Loss': avg_loss,
            'Profit_Factor': profit_factor,
            'Gross_Profit': gross_profit,
            'Gross_Loss': gross_loss
        }
    
    return results, df_trades

def print_performance_summary(results):
    """
    Print performance summary table.
    
    Args:
        results: Dictionary with performance metrics by session
    """
    print("\n" + "="*80)
    print("PERFORMANCE SUMMARY - FVG INVERSION STRATEGY")
    print("="*80)
    print(f"\n{'Session':<15} {'Total Trades':<15} {'Win Rate %':<15} {'Profit Factor':<15} {'Net P&L (pts)':<15}")
    print("-"*80)
    
    for session in ['London', 'New York', 'Overall']:
        metrics = results[session]
        print(f"{session:<15} {metrics['Total_Trades']:<15} "
              f"{metrics['Win_Rate']:<15.2f} {metrics['Profit_Factor']:<15.2f} "
              f"{metrics['Total_PnL']:<15.2f}")
    
    print("-"*80)
    print("\nDETAILED METRICS:")
    print("-"*80)
    
    for session in ['London', 'New York', 'Overall']:
        metrics = results[session]
        print(f"\n{session} Session:")
        print(f"  Total Trades:    {metrics['Total_Trades']}")
        print(f"  Winners:         {metrics['Winners']}")
        print(f"  Losers:          {metrics['Losers']}")
        print(f"  Win Rate:        {metrics['Win_Rate']:.2f}%")
        print(f"  Gross Profit:    {metrics['Gross_Profit']:.2f} pts")
        print(f"  Gross Loss:      {metrics['Gross_Loss']:.2f} pts")
        print(f"  Net P&L:         {metrics['Total_PnL']:.2f} pts")
        print(f"  Avg Win:         {metrics['Avg_Win']:.2f} pts")
        print(f"  Avg Loss:        {metrics['Avg_Loss']:.2f} pts")
        print(f"  Profit Factor:   {metrics['Profit_Factor']:.2f}")

# ============================================================================
# VISUALIZATION
# ============================================================================

def plot_equity_curve(df_trades):
    """
    Plot cumulative equity curve.
    
    Args:
        df_trades: DataFrame with trade results
    """
    # Calculate cumulative P&L
    df_trades['Cumulative_PnL'] = df_trades['PnL'].cumsum()
    
    # Create figure
    plt.figure(figsize=(14, 7))
    
    # Plot overall equity curve
    plt.subplot(2, 1, 1)
    plt.plot(df_trades['Exit_Time'], df_trades['Cumulative_PnL'], 
             linewidth=2, color='blue', label='Overall')
    plt.title('Cumulative Equity Curve - Overall', fontsize=14, fontweight='bold')
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Cumulative P&L (Points)', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # Plot by session
    plt.subplot(2, 1, 2)
    
    for session, color in [('London', 'green'), ('New York', 'red')]:
        session_trades = df_trades[df_trades['Session'] == session].copy()
        if len(session_trades) > 0:
            session_trades['Cumulative_PnL'] = session_trades['PnL'].cumsum()
            plt.plot(session_trades['Exit_Time'], session_trades['Cumulative_PnL'], 
                    linewidth=2, color=color, label=session, alpha=0.7)
    
    plt.title('Cumulative Equity Curve - By Session', fontsize=14, fontweight='bold')
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Cumulative P&L (Points)', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    plt.tight_layout()
    plt.savefig('nq_fvg_equity_curve.png', dpi=300, bbox_inches='tight')
    print("\nEquity curve saved as 'nq_fvg_equity_curve.png'")
    plt.close()

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main execution function."""
    
    print("="*80)
    print("NQ FUTURES - FVG INVERSION STRATEGY BACKTEST")
    print("="*80)
    print("\nStrategy Configuration:")
    print("  - Timeframe: 5 Minutes")
    print("  - Sessions: London (01:00-04:00 CT), New York (08:30-11:00 CT)")
    print("  - Entry Rule: FVG Inversion (close above/below FVG)")
    print("  - Risk Management: 1:1 Risk-to-Reward Ratio")
    print("  - One Bullet Rule: Maximum 1 trade per session per day")
    print("="*80)
    
    # Load data
    df = load_data('NQ_5min_2018_2024.csv')
    
    # Detect FVGs
    print("\nDetecting Fair Value Gaps...")
    df = detect_fvgs(df)
    bearish_fvgs = df['Bearish_FVG'].sum()
    bullish_fvgs = df['Bullish_FVG'].sum()
    print(f"Detected {bearish_fvgs} Bearish FVGs and {bullish_fvgs} Bullish FVGs")
    
    # Identify sessions
    print("\nIdentifying trading sessions...")
    df = identify_sessions(df)
    london_candles = df['London_Session'].sum()
    ny_candles = df['NY_Session'].sum()
    print(f"London session candles: {london_candles}")
    print(f"New York session candles: {ny_candles}")
    
    # Generate signals
    print("\nGenerating FVG Inversion signals...")
    df = generate_signals(df)
    long_signals = (df['Signal'] == 'LONG').sum()
    short_signals = (df['Signal'] == 'SHORT').sum()
    print(f"Generated {long_signals} LONG signals and {short_signals} SHORT signals")
    
    # Run backtest
    trades = run_backtest(df)
    
    # Analyze performance
    if len(trades) > 0:
        results, df_trades = analyze_performance(trades)
        print_performance_summary(results)
        
        # Plot equity curve
        print("\nGenerating equity curve...")
        plot_equity_curve(df_trades)
        
        # Save trade log
        df_trades.to_csv('nq_fvg_trade_log.csv', index=False)
        print("Trade log saved as 'nq_fvg_trade_log.csv'")
    else:
        print("\nNo trades were executed during the backtest period.")
    
    print("\n" + "="*80)
    print("BACKTEST COMPLETE")
    print("="*80)

if __name__ == "__main__":
    main()

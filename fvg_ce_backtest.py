"""
FVG Consequent Encroachment (C.E.) Limit Order Backtesting Script
==================================================================

Strategy: Fair Value Gap (FVG) with Consequent Encroachment entry
Author: Senior Quantitative Developer
Date: 2025-12-25

This script implements a complete backtesting system for the FVG C.E. strategy
with three different risk management models.
"""

import pandas as pd
import numpy as np
import glob
import matplotlib.pyplot as plt
from datetime import datetime, time
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# CONFIGURATION SECTION
# ============================================================================

# Risk Model Selection: 1, 2, or 3
RISK_MODEL = 2  # Change this to test different risk models

# Trading Session Times (NO TIMEZONE CONVERSION - use raw time)
SESSION_START = time(1, 0, 0)   # 01:00:00 - Start accepting new positions
SESSION_END = time(5, 0, 0)     # 05:00:00 - Stop accepting new positions
HARD_EXIT_TIME = time(8, 0, 0)  # 08:00:00 - Force close all positions

# Data Configuration
DATA_PATH = '/home/runner/work/Backtest-Trading/Backtest-Trading/'
TIMEFRAME = '5m'  # Options: '1m', '5m', '15m'
YEARS = [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]  # Years to include

# Risk Model Parameters
FVG_MARGIN = 2  # Points margin for Model 1 stops
MODEL2_TP = 40  # Fixed TP for Model 2
ATR_PERIOD = 14  # ATR period for Model 3
ATR_SL_MULT = 1.5  # ATR multiplier for SL in Model 3
ATR_TP_MULT = 3.0  # ATR multiplier for TP in Model 3

# Position Sizing
POSITION_SIZE = 1  # Number of contracts per trade

# ============================================================================
# DATA LOADING FUNCTIONS
# ============================================================================

def load_csv_data(filepath):
    """
    Load a single CSV file with the specific format.
    
    CSV Format:
    - Semicolon separated
    - Column1: Date (DD/MM/YYYY)
    - Column2: Time (HH:MM:SS)
    - Column3: Open
    - Column4: High
    - Column5: Low
    - Column6: Close
    - Column7: Volume
    """
    try:
        df = pd.read_csv(
            filepath,
            sep=';',
            skiprows=1,  # Skip header row with "Column1;Column2;..."
            names=['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
        )
        
        # Combine Date and Time into datetime
        df['DateTime'] = pd.to_datetime(
            df['Date'] + ' ' + df['Time'],
            format='%d/%m/%Y %H:%M:%S',
            errors='coerce'
        )
        
        # Drop rows with invalid datetime
        df = df.dropna(subset=['DateTime'])
        
        # Extract time component for session filtering
        df['TimeOnly'] = df['DateTime'].dt.time
        
        # Sort by datetime
        df = df.sort_values('DateTime').reset_index(drop=True)
        
        # Convert OHLC to numeric
        for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Drop any rows with NaN in OHLC
        df = df.dropna(subset=['Open', 'High', 'Low', 'Close'])
        
        return df
    
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return None


def load_multiple_years(timeframe, years):
    """
    Load and combine multiple year CSV files for a given timeframe.
    """
    all_data = []
    
    for year in years:
        pattern = f"{DATA_PATH}{year} {timeframe}.csv"
        files = glob.glob(pattern)
        
        for filepath in files:
            print(f"Loading: {filepath}")
            df = load_csv_data(filepath)
            if df is not None and len(df) > 0:
                all_data.append(df)
    
    if not all_data:
        raise ValueError(f"No data loaded for timeframe {timeframe}")
    
    # Combine all dataframes
    combined = pd.concat(all_data, ignore_index=True)
    combined = combined.sort_values('DateTime').reset_index(drop=True)
    
    # Remove duplicates based on DateTime
    combined = combined.drop_duplicates(subset=['DateTime'], keep='first')
    
    print(f"\nTotal rows loaded: {len(combined)}")
    print(f"Date range: {combined['DateTime'].min()} to {combined['DateTime'].max()}")
    
    return combined


# ============================================================================
# INDICATOR CALCULATIONS
# ============================================================================

def calculate_atr(df, period=14):
    """
    Calculate Average True Range (ATR) for dynamic risk management.
    """
    high = df['High']
    low = df['Low']
    close = df['Close'].shift(1)
    
    tr1 = high - low
    tr2 = abs(high - close)
    tr3 = abs(low - close)
    
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    atr = tr.rolling(window=period).mean()
    
    return atr


# ============================================================================
# FVG DETECTION
# ============================================================================

def identify_fvg(df):
    """
    Identify Fair Value Gaps (FVG) in the data.
    
    Bullish FVG: High[i-2] < Low[i] (gap between candle i-2 high and candle i low)
    Bearish FVG: Low[i-2] > High[i] (gap between candle i-2 low and candle i high)
    
    Returns:
    - DataFrame with FVG signals and C.E. levels
    """
    # Shift data to access i-2 and i-1 candles
    df['High_i2'] = df['High'].shift(2)
    df['Low_i2'] = df['Low'].shift(2)
    df['High_i1'] = df['High'].shift(1)
    df['Low_i1'] = df['Low'].shift(1)
    
    # Bullish FVG: High[i-2] < Low[i]
    df['Bullish_FVG'] = (df['High_i2'] < df['Low']).astype(int)
    
    # Bearish FVG: Low[i-2] > High[i]
    df['Bearish_FVG'] = (df['Low_i2'] > df['High']).astype(int)
    
    # Calculate Consequent Encroachment (C.E.) - 50% midpoint of FVG
    # Long C.E. = (High[i-2] + Low[i]) / 2
    df['Long_CE'] = np.where(
        df['Bullish_FVG'] == 1,
        (df['High_i2'] + df['Low']) / 2,
        np.nan
    )
    
    # Short C.E. = (Low[i-2] + High[i]) / 2
    df['Short_CE'] = np.where(
        df['Bearish_FVG'] == 1,
        (df['Low_i2'] + df['High']) / 2,
        np.nan
    )
    
    # Store reference candle data for risk calculations
    df['FVG_Candle_High'] = np.where(df['Bullish_FVG'] == 1, df['High'], np.nan)
    df['FVG_Candle_Low'] = np.where(df['Bullish_FVG'] == 1, df['Low'], np.nan)
    df['FVG_Candle_High_Short'] = np.where(df['Bearish_FVG'] == 1, df['High'], np.nan)
    df['FVG_Candle_Low_Short'] = np.where(df['Bearish_FVG'] == 1, df['Low'], np.nan)
    
    return df


# ============================================================================
# RISK MODEL CALCULATIONS
# ============================================================================

def calculate_risk_levels(df, risk_model):
    """
    Calculate Stop Loss and Take Profit levels based on the selected risk model.
    
    MODEL 1: "The Aggressive Sniper" (FVG Border-based Risk)
    - SL Long: Below "Distal Line" (High[i-2]) - 2 points
    - SL Short: Above "Distal Line" (Low[i-2]) + 2 points
    - TP: 3x the risk distance
    
    MODEL 2: "The Structural Defender" (Swing Candle-based Risk)
    - SL Long: Below Low of candle [i] (FVG completion candle)
    - SL Short: Above High of candle [i]
    - TP: Fixed 40 points
    
    MODEL 3: "The Volatility Adapter" (ATR-based Dynamic Risk)
    - SL: 1.5 * ATR(14)
    - TP: 3.0 * ATR(14)
    """
    if risk_model == 1:
        # MODEL 1: FVG Border-based Risk
        # Long positions
        df['Long_SL'] = np.where(
            df['Bullish_FVG'] == 1,
            df['High_i2'] - FVG_MARGIN,  # Below distal line
            np.nan
        )
        df['Long_TP_temp'] = np.where(
            df['Bullish_FVG'] == 1,
            df['Long_CE'] + 3 * (df['Long_CE'] - df['Long_SL']),  # 3x risk
            np.nan
        )
        
        # Short positions
        df['Short_SL'] = np.where(
            df['Bearish_FVG'] == 1,
            df['Low_i2'] + FVG_MARGIN,  # Above distal line
            np.nan
        )
        df['Short_TP_temp'] = np.where(
            df['Bearish_FVG'] == 1,
            df['Short_CE'] - 3 * (df['Short_SL'] - df['Short_CE']),  # 3x risk
            np.nan
        )
    
    elif risk_model == 2:
        # MODEL 2: Structural Defender - Swing Candle-based
        # Long positions - SL below Low of candle [i]
        df['Long_SL'] = np.where(
            df['Bullish_FVG'] == 1,
            df['Low'] - FVG_MARGIN,  # Below current candle's low
            np.nan
        )
        df['Long_TP_temp'] = np.where(
            df['Bullish_FVG'] == 1,
            df['Long_CE'] + MODEL2_TP,  # Fixed 40 points
            np.nan
        )
        
        # Short positions - SL above High of candle [i]
        df['Short_SL'] = np.where(
            df['Bearish_FVG'] == 1,
            df['High'] + FVG_MARGIN,  # Above current candle's high
            np.nan
        )
        df['Short_TP_temp'] = np.where(
            df['Bearish_FVG'] == 1,
            df['Short_CE'] - MODEL2_TP,  # Fixed 40 points
            np.nan
        )
    
    elif risk_model == 3:
        # MODEL 3: Volatility Adapter - ATR-based
        df['ATR'] = calculate_atr(df, ATR_PERIOD)
        
        # Long positions
        df['Long_SL'] = np.where(
            df['Bullish_FVG'] == 1,
            df['Long_CE'] - ATR_SL_MULT * df['ATR'],
            np.nan
        )
        df['Long_TP_temp'] = np.where(
            df['Bullish_FVG'] == 1,
            df['Long_CE'] + ATR_TP_MULT * df['ATR'],
            np.nan
        )
        
        # Short positions
        df['Short_SL'] = np.where(
            df['Bearish_FVG'] == 1,
            df['Short_CE'] + ATR_SL_MULT * df['ATR'],
            np.nan
        )
        df['Short_TP_temp'] = np.where(
            df['Bearish_FVG'] == 1,
            df['Short_CE'] - ATR_TP_MULT * df['ATR'],
            np.nan
        )
    
    return df


# ============================================================================
# SETUP MANAGEMENT AND ENTRY LOGIC
# ============================================================================

def manage_setups_and_entries(df):
    """
    Manage FVG setups using forward fill and detect limit order entries.
    
    Logic:
    1. Propagate C.E. levels and SL levels forward until hit or cancelled
    2. Cancel setup if price breaks through theoretical SL BEFORE triggering entry
    3. Entry triggers when price touches C.E. level (limit order simulation)
    4. Only during trading session (01:00 to 05:00)
    """
    # Initialize columns for active setups and entries
    df['Active_Long_CE'] = df['Long_CE']
    df['Active_Long_SL'] = df['Long_SL']
    df['Active_Long_TP'] = df['Long_TP_temp']
    
    df['Active_Short_CE'] = df['Short_CE']
    df['Active_Short_SL'] = df['Short_SL']
    df['Active_Short_TP'] = df['Short_TP_temp']
    
    df['Long_Entry'] = 0
    df['Short_Entry'] = 0
    df['Long_Entry_Price'] = np.nan
    df['Short_Entry_Price'] = np.nan
    
    # Check if within trading session
    df['In_Session'] = df['TimeOnly'].apply(
        lambda t: SESSION_START <= t <= SESSION_END
    )
    
    # Iterate through data to manage setups
    for i in range(3, len(df)):
        # Long Setup Management
        if pd.notna(df.at[i-1, 'Active_Long_CE']):
            ce = df.at[i-1, 'Active_Long_CE']
            sl = df.at[i-1, 'Active_Long_SL']
            tp = df.at[i-1, 'Active_Long_TP']
            
            # Check if SL broken before entry (cancel setup)
            if df.at[i, 'Low'] <= sl:
                # Setup cancelled
                df.at[i, 'Active_Long_CE'] = np.nan
                df.at[i, 'Active_Long_SL'] = np.nan
                df.at[i, 'Active_Long_TP'] = np.nan
            
            # Check if C.E. level touched (entry triggered) and in session
            elif df.at[i, 'Low'] <= ce <= df.at[i, 'High'] and df.at[i, 'In_Session']:
                # Entry triggered at C.E. price
                df.at[i, 'Long_Entry'] = 1
                df.at[i, 'Long_Entry_Price'] = ce
                df.at[i, 'Active_Long_CE'] = np.nan  # Clear setup after entry
                df.at[i, 'Active_Long_SL'] = sl  # Keep SL for position management
                df.at[i, 'Active_Long_TP'] = tp  # Keep TP for position management
            
            else:
                # Propagate setup forward
                df.at[i, 'Active_Long_CE'] = ce
                df.at[i, 'Active_Long_SL'] = sl
                df.at[i, 'Active_Long_TP'] = tp
        
        # Short Setup Management
        if pd.notna(df.at[i-1, 'Active_Short_CE']):
            ce = df.at[i-1, 'Active_Short_CE']
            sl = df.at[i-1, 'Active_Short_SL']
            tp = df.at[i-1, 'Active_Short_TP']
            
            # Check if SL broken before entry (cancel setup)
            if df.at[i, 'High'] >= sl:
                # Setup cancelled
                df.at[i, 'Active_Short_CE'] = np.nan
                df.at[i, 'Active_Short_SL'] = np.nan
                df.at[i, 'Active_Short_TP'] = np.nan
            
            # Check if C.E. level touched (entry triggered) and in session
            elif df.at[i, 'Low'] <= ce <= df.at[i, 'High'] and df.at[i, 'In_Session']:
                # Entry triggered at C.E. price
                df.at[i, 'Short_Entry'] = 1
                df.at[i, 'Short_Entry_Price'] = ce
                df.at[i, 'Active_Short_CE'] = np.nan  # Clear setup after entry
                df.at[i, 'Active_Short_SL'] = sl  # Keep SL for position management
                df.at[i, 'Active_Short_TP'] = tp  # Keep TP for position management
            
            else:
                # Propagate setup forward
                df.at[i, 'Active_Short_CE'] = ce
                df.at[i, 'Active_Short_SL'] = sl
                df.at[i, 'Active_Short_TP'] = tp
    
    return df


# ============================================================================
# POSITION MANAGEMENT AND EXIT LOGIC
# ============================================================================

def manage_positions(df):
    """
    Manage open positions: track SL, TP, and hard exit at 08:00.
    """
    df['Position'] = 0  # 1 = Long, -1 = Short, 0 = Flat
    df['Position_Entry_Price'] = np.nan
    df['Position_SL'] = np.nan
    df['Position_TP'] = np.nan
    df['Exit_Price'] = np.nan
    df['Exit_Reason'] = ''
    df['PnL'] = 0.0
    
    current_position = 0
    entry_price = 0
    sl_level = 0
    tp_level = 0
    
    for i in range(len(df)):
        # Check hard exit time (08:00)
        if df.at[i, 'TimeOnly'] >= HARD_EXIT_TIME and current_position != 0:
            # Force close at current close price
            exit_price = df.at[i, 'Close']
            
            if current_position == 1:  # Long
                pnl = (exit_price - entry_price) * POSITION_SIZE
            else:  # Short
                pnl = (entry_price - exit_price) * POSITION_SIZE
            
            df.at[i, 'Exit_Price'] = exit_price
            df.at[i, 'Exit_Reason'] = 'Hard_Exit_08:00'
            df.at[i, 'PnL'] = pnl
            
            current_position = 0
            entry_price = 0
            sl_level = 0
            tp_level = 0
        
        # Check for new entries (only if flat)
        if current_position == 0:
            # Long entry
            if df.at[i, 'Long_Entry'] == 1:
                current_position = 1
                entry_price = df.at[i, 'Long_Entry_Price']
                sl_level = df.at[i, 'Active_Long_SL']
                tp_level = df.at[i, 'Active_Long_TP']
                df.at[i, 'Position'] = 1
                df.at[i, 'Position_Entry_Price'] = entry_price
                df.at[i, 'Position_SL'] = sl_level
                df.at[i, 'Position_TP'] = tp_level
            
            # Short entry
            elif df.at[i, 'Short_Entry'] == 1:
                current_position = -1
                entry_price = df.at[i, 'Short_Entry_Price']
                sl_level = df.at[i, 'Active_Short_SL']
                tp_level = df.at[i, 'Active_Short_TP']
                df.at[i, 'Position'] = -1
                df.at[i, 'Position_Entry_Price'] = entry_price
                df.at[i, 'Position_SL'] = sl_level
                df.at[i, 'Position_TP'] = tp_level
        
        # Manage existing position
        elif current_position == 1:  # Long position
            df.at[i, 'Position'] = 1
            df.at[i, 'Position_Entry_Price'] = entry_price
            df.at[i, 'Position_SL'] = sl_level
            df.at[i, 'Position_TP'] = tp_level
            
            # Check for SL hit
            if df.at[i, 'Low'] <= sl_level:
                exit_price = sl_level
                pnl = (exit_price - entry_price) * POSITION_SIZE
                df.at[i, 'Exit_Price'] = exit_price
                df.at[i, 'Exit_Reason'] = 'Stop_Loss'
                df.at[i, 'PnL'] = pnl
                current_position = 0
            
            # Check for TP hit
            elif df.at[i, 'High'] >= tp_level:
                exit_price = tp_level
                pnl = (exit_price - entry_price) * POSITION_SIZE
                df.at[i, 'Exit_Price'] = exit_price
                df.at[i, 'Exit_Reason'] = 'Take_Profit'
                df.at[i, 'PnL'] = pnl
                current_position = 0
        
        elif current_position == -1:  # Short position
            df.at[i, 'Position'] = -1
            df.at[i, 'Position_Entry_Price'] = entry_price
            df.at[i, 'Position_SL'] = sl_level
            df.at[i, 'Position_TP'] = tp_level
            
            # Check for SL hit
            if df.at[i, 'High'] >= sl_level:
                exit_price = sl_level
                pnl = (entry_price - exit_price) * POSITION_SIZE
                df.at[i, 'Exit_Price'] = exit_price
                df.at[i, 'Exit_Reason'] = 'Stop_Loss'
                df.at[i, 'PnL'] = pnl
                current_position = 0
            
            # Check for TP hit
            elif df.at[i, 'Low'] <= tp_level:
                exit_price = tp_level
                pnl = (entry_price - exit_price) * POSITION_SIZE
                df.at[i, 'Exit_Price'] = exit_price
                df.at[i, 'Exit_Reason'] = 'Take_Profit'
                df.at[i, 'PnL'] = pnl
                current_position = 0
    
    return df


# ============================================================================
# PERFORMANCE METRICS
# ============================================================================

def calculate_performance_metrics(df):
    """
    Calculate and display comprehensive performance metrics.
    """
    # Filter completed trades
    trades = df[df['PnL'] != 0].copy()
    
    if len(trades) == 0:
        print("\n" + "="*80)
        print("NO TRADES EXECUTED")
        print("="*80)
        return None
    
    # Calculate cumulative PnL
    trades['Cumulative_PnL'] = trades['PnL'].cumsum()
    
    # Calculate metrics
    total_trades = len(trades)
    winning_trades = len(trades[trades['PnL'] > 0])
    losing_trades = len(trades[trades['PnL'] < 0])
    win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
    
    total_pnl = trades['PnL'].sum()
    avg_win = trades[trades['PnL'] > 0]['PnL'].mean() if winning_trades > 0 else 0
    avg_loss = trades[trades['PnL'] < 0]['PnL'].mean() if losing_trades > 0 else 0
    
    # Maximum Drawdown
    cumulative = trades['Cumulative_PnL']
    running_max = cumulative.cummax()
    drawdown = cumulative - running_max
    max_drawdown = drawdown.min()
    
    # Print results
    print("\n" + "="*80)
    print(f"BACKTEST RESULTS - RISK MODEL {RISK_MODEL}")
    print("="*80)
    
    if RISK_MODEL == 1:
        print("Model: The Aggressive Sniper (FVG Border-based Risk)")
    elif RISK_MODEL == 2:
        print("Model: The Structural Defender (Swing Candle-based Risk)")
    elif RISK_MODEL == 3:
        print("Model: The Volatility Adapter (ATR-based Dynamic Risk)")
    
    print(f"\nTimeframe: {TIMEFRAME}")
    print(f"Date Range: {df['DateTime'].min()} to {df['DateTime'].max()}")
    print(f"Trading Session: {SESSION_START} to {SESSION_END}")
    print(f"Hard Exit Time: {HARD_EXIT_TIME}")
    
    print("\n" + "-"*80)
    print("TRADE STATISTICS")
    print("-"*80)
    print(f"Total Trades:        {total_trades}")
    print(f"Winning Trades:      {winning_trades}")
    print(f"Losing Trades:       {losing_trades}")
    print(f"Win Rate:            {win_rate:.2f}%")
    
    print("\n" + "-"*80)
    print("PROFIT & LOSS")
    print("-"*80)
    print(f"Total PnL:           {total_pnl:.2f} points")
    print(f"Average Win:         {avg_win:.2f} points")
    print(f"Average Loss:        {avg_loss:.2f} points")
    print(f"Profit Factor:       {abs(avg_win / avg_loss) if avg_loss != 0 else 0:.2f}")
    
    print("\n" + "-"*80)
    print("RISK METRICS")
    print("-"*80)
    print(f"Maximum Drawdown:    {max_drawdown:.2f} points")
    
    print("\n" + "-"*80)
    print("EXIT BREAKDOWN")
    print("-"*80)
    exit_counts = trades['Exit_Reason'].value_counts()
    for reason, count in exit_counts.items():
        print(f"{reason:20s} {count:5d} ({count/total_trades*100:.1f}%)")
    
    print("\n" + "="*80 + "\n")
    
    return trades


# ============================================================================
# VISUALIZATION
# ============================================================================

def plot_performance(trades):
    """
    Plot cumulative PnL curve.
    """
    if trades is None or len(trades) == 0:
        print("No trades to plot.")
        return
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
    
    # Cumulative PnL
    ax1.plot(trades.index, trades['Cumulative_PnL'], linewidth=2, color='blue')
    ax1.axhline(y=0, color='black', linestyle='--', linewidth=1)
    ax1.fill_between(trades.index, trades['Cumulative_PnL'], 0, 
                     where=(trades['Cumulative_PnL'] >= 0), alpha=0.3, color='green')
    ax1.fill_between(trades.index, trades['Cumulative_PnL'], 0, 
                     where=(trades['Cumulative_PnL'] < 0), alpha=0.3, color='red')
    ax1.set_title(f'Cumulative PnL - FVG C.E. Strategy (Risk Model {RISK_MODEL})', 
                  fontsize=14, fontweight='bold')
    ax1.set_xlabel('Trade Number')
    ax1.set_ylabel('Cumulative PnL (points)')
    ax1.grid(True, alpha=0.3)
    
    # Drawdown
    cumulative = trades['Cumulative_PnL']
    running_max = cumulative.cummax()
    drawdown = cumulative - running_max
    
    ax2.fill_between(trades.index, drawdown, 0, alpha=0.5, color='red')
    ax2.set_title('Drawdown', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Trade Number')
    ax2.set_ylabel('Drawdown (points)')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # Save figure
    filename = f'fvg_ce_backtest_model{RISK_MODEL}_{TIMEFRAME}.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"Performance chart saved as: {filename}")
    
    plt.show()


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """
    Main execution function.
    """
    print("\n" + "="*80)
    print("FVG CONSEQUENT ENCROACHMENT BACKTESTING SYSTEM")
    print("="*80)
    print(f"\nRisk Model: {RISK_MODEL}")
    print(f"Timeframe: {TIMEFRAME}")
    print(f"Years: {YEARS}")
    
    # Step 1: Load Data
    print("\n[1/7] Loading data...")
    df = load_multiple_years(TIMEFRAME, YEARS)
    
    # Step 2: Identify FVGs
    print("[2/7] Identifying Fair Value Gaps...")
    df = identify_fvg(df)
    print(f"  Bullish FVGs detected: {df['Bullish_FVG'].sum()}")
    print(f"  Bearish FVGs detected: {df['Bearish_FVG'].sum()}")
    
    # Step 3: Calculate Risk Levels
    print(f"[3/7] Calculating risk levels (Model {RISK_MODEL})...")
    df = calculate_risk_levels(df, RISK_MODEL)
    
    # Step 4: Manage Setups and Entries
    print("[4/7] Managing setups and detecting entries...")
    df = manage_setups_and_entries(df)
    print(f"  Long entries: {df['Long_Entry'].sum()}")
    print(f"  Short entries: {df['Short_Entry'].sum()}")
    
    # Step 5: Manage Positions
    print("[5/7] Managing positions and exits...")
    df = manage_positions(df)
    
    # Step 6: Calculate Performance
    print("[6/7] Calculating performance metrics...")
    trades = calculate_performance_metrics(df)
    
    # Step 7: Visualize Results
    print("[7/7] Generating performance charts...")
    plot_performance(trades)
    
    # Save detailed trade log
    if trades is not None and len(trades) > 0:
        trade_columns = ['DateTime', 'Position', 'Position_Entry_Price', 
                        'Exit_Price', 'Exit_Reason', 'PnL', 'Cumulative_PnL']
        trade_log = trades[trade_columns].copy()
        filename = f'trade_log_model{RISK_MODEL}_{TIMEFRAME}.csv'
        trade_log.to_csv(filename, index=False)
        print(f"Trade log saved as: {filename}")
    
    print("\n" + "="*80)
    print("BACKTEST COMPLETE")
    print("="*80 + "\n")
    
    return df, trades


# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    df, trades = main()

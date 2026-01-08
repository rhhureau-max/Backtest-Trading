"""
Fair Value Gap (FVG) Trading Strategy Backtest
===============================================
This script backtests an FVG trading strategy on NQ 1-minute data from 2018-2025.

Strategy Rules:
- Trading window: 08:30 to 11:00 each day
- Detect Bearish FVG: Low[i-2] > High[i]
- Detect Bullish FVG: High[i-2] < Low[i]
- One trade per day maximum (first valid FVG)
- Risk:Reward ratio 1:1.5
"""

import pandas as pd
import numpy as np
import zipfile
import os
from datetime import datetime, time
import warnings
warnings.filterwarnings('ignore')

# Configuration
DATA_DIR = "/home/runner/work/Backtest-Trading/Backtest-Trading"
TRADE_START_TIME = time(8, 30, 0)
TRADE_END_TIME = time(11, 0, 0)
STOP_BUFFER = 0.5  # Stop loss buffer in points
RISK_REWARD_RATIO = 1.5

def load_and_combine_data():
    """
    Load all 1-minute CSV files (2018-2025) and combine them into a single DataFrame.
    Handles both zipped and unzipped files.
    """
    print("Loading data files...")
    all_data = []
    
    # Years to process
    years = list(range(2018, 2026))
    
    for year in years:
        print(f"Processing {year}...")
        
        # Check for zipped file first
        zip_file = os.path.join(DATA_DIR, f"{year} 1m.csv.zip")
        csv_file = os.path.join(DATA_DIR, f"{year} 1m.csv")
        
        df = None
        
        if os.path.exists(zip_file):
            # Extract and read from zip
            try:
                with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                    # Get the CSV filename inside the zip
                    csv_name = f"{year} 1m.csv"
                    with zip_ref.open(csv_name) as csv_in_zip:
                        df = pd.read_csv(csv_in_zip, sep=';')
            except Exception as e:
                print(f"  Error reading {zip_file}: {e}")
                continue
        elif os.path.exists(csv_file):
            # Read directly from CSV
            try:
                df = pd.read_csv(csv_file, sep=';')
            except Exception as e:
                print(f"  Error reading {csv_file}: {e}")
                continue
        else:
            print(f"  File not found for {year}, skipping...")
            continue
        
        if df is not None and not df.empty:
            print(f"  Loaded {len(df)} rows for {year}")
            all_data.append(df)
    
    if not all_data:
        raise ValueError("No data files could be loaded!")
    
    # Combine all dataframes
    print("\nCombining all data...")
    combined_df = pd.concat(all_data, ignore_index=True)
    print(f"Total rows: {len(combined_df)}")
    
    return combined_df

def preprocess_data(df):
    """
    Clean and preprocess the data:
    - Parse date/time columns
    - Rename columns
    - Sort by datetime
    - Filter for trading hours
    """
    print("\nPreprocessing data...")
    
    # Rename columns
    df.columns = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
    
    # Parse datetime (DD/MM/YYYY HH:MM:SS)
    df['DateTime'] = pd.to_datetime(
        df['Date'] + ' ' + df['Time'], 
        format='%d/%m/%Y %H:%M:%S'
    )
    
    # Extract date and time separately
    df['DateOnly'] = df['DateTime'].dt.date
    df['TimeOnly'] = df['DateTime'].dt.time
    
    # Sort by datetime
    df = df.sort_values('DateTime').reset_index(drop=True)
    
    # Convert OHLC to numeric
    for col in ['Open', 'High', 'Low', 'Close']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Remove any rows with missing data
    df = df.dropna(subset=['Open', 'High', 'Low', 'Close']).reset_index(drop=True)
    
    print(f"Data range: {df['DateTime'].min()} to {df['DateTime'].max()}")
    print(f"Total candles after preprocessing: {len(df)}")
    
    return df

def detect_fvg(df):
    """
    Detect Fair Value Gaps (FVG) in the data.
    
    Bearish FVG: Low[i-2] > High[i] (gap between bottom of i-2 and top of i)
    Bullish FVG: High[i-2] < Low[i] (gap between top of i-2 and bottom of i)
    
    Returns DataFrame with FVG signals.
    """
    print("\nDetecting Fair Value Gaps...")
    
    # Create shifted columns for i-2 and i-1
    df['High_i2'] = df['High'].shift(2)
    df['Low_i2'] = df['Low'].shift(2)
    df['High_i1'] = df['High'].shift(1)
    df['Low_i1'] = df['Low'].shift(1)
    
    # Detect FVGs
    # Bearish FVG: Low[i-2] > High[i]
    df['Bearish_FVG'] = df['Low_i2'] > df['High']
    
    # Bullish FVG: High[i-2] < Low[i]
    df['Bullish_FVG'] = df['High_i2'] < df['Low']
    
    # Store FVG entry prices and stop losses
    # For Bearish FVG (Short): Entry = High[i], SL = High[i-2] + 0.5
    df.loc[df['Bearish_FVG'], 'FVG_Entry'] = df.loc[df['Bearish_FVG'], 'High']
    df.loc[df['Bearish_FVG'], 'FVG_StopLoss'] = df.loc[df['Bearish_FVG'], 'High_i2'] + STOP_BUFFER
    
    # For Bullish FVG (Long): Entry = Low[i], SL = Low[i-2] - 0.5
    df.loc[df['Bullish_FVG'], 'FVG_Entry'] = df.loc[df['Bullish_FVG'], 'Low']
    df.loc[df['Bullish_FVG'], 'FVG_StopLoss'] = df.loc[df['Bullish_FVG'], 'Low_i2'] - STOP_BUFFER
    
    # Calculate Take Profit
    # TP = Entry +/- (SL distance) * 1.5
    df.loc[df['Bearish_FVG'], 'FVG_TakeProfit'] = (
        df.loc[df['Bearish_FVG'], 'FVG_Entry'] - 
        (df.loc[df['Bearish_FVG'], 'FVG_StopLoss'] - df.loc[df['Bearish_FVG'], 'FVG_Entry']) * RISK_REWARD_RATIO
    )
    
    df.loc[df['Bullish_FVG'], 'FVG_TakeProfit'] = (
        df.loc[df['Bullish_FVG'], 'FVG_Entry'] + 
        (df.loc[df['Bullish_FVG'], 'FVG_Entry'] - df.loc[df['Bullish_FVG'], 'FVG_StopLoss']) * RISK_REWARD_RATIO
    )
    
    # Mark FVG type
    df.loc[df['Bearish_FVG'], 'FVG_Type'] = 'Short'
    df.loc[df['Bullish_FVG'], 'FVG_Type'] = 'Long'
    
    bearish_count = df['Bearish_FVG'].sum()
    bullish_count = df['Bullish_FVG'].sum()
    print(f"Detected {bearish_count} Bearish FVGs and {bullish_count} Bullish FVGs")
    
    return df

def backtest_strategy(df):
    """
    Execute the backtest with the following rules:
    - Only trade during 08:30-11:00 killzone
    - One trade per day maximum (first valid FVG)
    - Order placed at close of FVG candle
    - Order triggered when price touches entry level
    - Exit at Stop Loss or Take Profit
    - Cancel order if not triggered by 11:00
    """
    print("\nRunning backtest...")
    
    trades = []
    
    # Get unique trading days
    trading_days = df['DateOnly'].unique()
    print(f"Trading days: {len(trading_days)}")
    
    for day_idx, day in enumerate(trading_days):
        if (day_idx + 1) % 100 == 0:
            print(f"  Processing day {day_idx + 1}/{len(trading_days)}...")
        
        # Get data for this day
        day_data = df[df['DateOnly'] == day].copy()
        
        # Filter for trading window (08:30-11:00)
        trading_window = day_data[
            (day_data['TimeOnly'] >= TRADE_START_TIME) & 
            (day_data['TimeOnly'] <= TRADE_END_TIME)
        ].copy()
        
        if len(trading_window) < 3:
            # Not enough data for this day
            continue
        
        # Look for the first valid FVG in the trading window
        fvg_signals = trading_window[
            (trading_window['Bearish_FVG'] == True) | 
            (trading_window['Bullish_FVG'] == True)
        ]
        
        if len(fvg_signals) == 0:
            # No FVG detected this day
            continue
        
        # Take the first FVG
        first_fvg = fvg_signals.iloc[0]
        fvg_index = first_fvg.name
        
        # Order details
        fvg_type = first_fvg['FVG_Type']
        entry_price = first_fvg['FVG_Entry']
        stop_loss = first_fvg['FVG_StopLoss']
        take_profit = first_fvg['FVG_TakeProfit']
        fvg_datetime = first_fvg['DateTime']
        
        # Look for order execution in subsequent candles
        # Get all candles after the FVG (including outside trading window)
        remaining_candles = df[
            (df['DateOnly'] == day) & 
            (df['DateTime'] > fvg_datetime)
        ].copy()
        
        if len(remaining_candles) == 0:
            # No candles after FVG
            continue
        
        # Check if order should be cancelled (not triggered by 11:00)
        candles_before_cutoff = remaining_candles[
            remaining_candles['TimeOnly'] <= TRADE_END_TIME
        ]
        
        # Track if order was triggered
        order_triggered = False
        entry_time = None
        exit_time = None
        exit_price = None
        exit_reason = None
        
        # Check each candle for order trigger
        for idx, candle in remaining_candles.iterrows():
            # Check if order is triggered
            if not order_triggered:
                # Check if we're still within order placement window (by 11:00)
                if candle['TimeOnly'] > TRADE_END_TIME:
                    # Order expired without being triggered
                    break
                
                # Check if price touches entry level
                if fvg_type == 'Short':
                    # For short, we need price to go up to entry (High >= Entry)
                    if candle['High'] >= entry_price:
                        order_triggered = True
                        entry_time = candle['DateTime']
                else:  # Long
                    # For long, we need price to go down to entry (Low <= Entry)
                    if candle['Low'] <= entry_price:
                        order_triggered = True
                        entry_time = candle['DateTime']
            else:
                # Order is triggered, check for exit
                if fvg_type == 'Short':
                    # Check Stop Loss (price goes up to SL)
                    if candle['High'] >= stop_loss:
                        exit_price = stop_loss
                        exit_time = candle['DateTime']
                        exit_reason = 'Stop Loss'
                        break
                    # Check Take Profit (price goes down to TP)
                    elif candle['Low'] <= take_profit:
                        exit_price = take_profit
                        exit_time = candle['DateTime']
                        exit_reason = 'Take Profit'
                        break
                else:  # Long
                    # Check Stop Loss (price goes down to SL)
                    if candle['Low'] <= stop_loss:
                        exit_price = stop_loss
                        exit_time = candle['DateTime']
                        exit_reason = 'Stop Loss'
                        break
                    # Check Take Profit (price goes up to TP)
                    elif candle['High'] >= take_profit:
                        exit_price = take_profit
                        exit_time = candle['DateTime']
                        exit_reason = 'Take Profit'
                        break
        
        # Record trade if it was triggered and exited
        if order_triggered and exit_time is not None:
            # Calculate PnL
            if fvg_type == 'Short':
                pnl = entry_price - exit_price
            else:  # Long
                pnl = exit_price - entry_price
            
            # Calculate duration
            duration = exit_time - entry_time
            duration_minutes = duration.total_seconds() / 60
            
            trades.append({
                'Date': day,
                'FVG_Time': fvg_datetime,
                'Entry_Time': entry_time,
                'Exit_Time': exit_time,
                'Type': fvg_type,
                'Entry_Price': entry_price,
                'Exit_Price': exit_price,
                'Stop_Loss': stop_loss,
                'Take_Profit': take_profit,
                'PnL': pnl,
                'Duration_Minutes': duration_minutes,
                'Exit_Reason': exit_reason
            })
    
    print(f"Total trades executed: {len(trades)}")
    
    return pd.DataFrame(trades)

def calculate_statistics(trades_df):
    """
    Calculate and display trading statistics.
    """
    print("\n" + "="*60)
    print("BACKTEST RESULTS")
    print("="*60)
    
    if len(trades_df) == 0:
        print("No trades executed!")
        return
    
    # Basic metrics
    total_trades = len(trades_df)
    winning_trades = len(trades_df[trades_df['PnL'] > 0])
    losing_trades = len(trades_df[trades_df['PnL'] < 0])
    breakeven_trades = len(trades_df[trades_df['PnL'] == 0])
    
    # Winrate
    winrate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
    
    # Total PnL
    total_pnl = trades_df['PnL'].sum()
    
    # Profit Factor
    gross_profit = trades_df[trades_df['PnL'] > 0]['PnL'].sum()
    gross_loss = abs(trades_df[trades_df['PnL'] < 0]['PnL'].sum())
    profit_factor = gross_profit / gross_loss if gross_loss > 0 else np.inf
    
    # Maximum Drawdown
    trades_df['Cumulative_PnL'] = trades_df['PnL'].cumsum()
    trades_df['Running_Max'] = trades_df['Cumulative_PnL'].cummax()
    trades_df['Drawdown'] = trades_df['Cumulative_PnL'] - trades_df['Running_Max']
    max_drawdown = trades_df['Drawdown'].min()
    
    # Average trade
    avg_win = trades_df[trades_df['PnL'] > 0]['PnL'].mean() if winning_trades > 0 else 0
    avg_loss = trades_df[trades_df['PnL'] < 0]['PnL'].mean() if losing_trades > 0 else 0
    avg_trade = trades_df['PnL'].mean()
    
    # Duration
    avg_duration = trades_df['Duration_Minutes'].mean()
    
    # Print results
    print(f"\nTotal Trades:          {total_trades}")
    print(f"Winning Trades:        {winning_trades}")
    print(f"Losing Trades:         {losing_trades}")
    print(f"Breakeven Trades:      {breakeven_trades}")
    print(f"\nWinrate:               {winrate:.2f}%")
    print(f"Profit Factor:         {profit_factor:.2f}")
    print(f"Maximum Drawdown:      {max_drawdown:.2f} points")
    print(f"Total Net Profit:      {total_pnl:.2f} points")
    print(f"\nAverage Win:           {avg_win:.2f} points")
    print(f"Average Loss:          {avg_loss:.2f} points")
    print(f"Average Trade:         {avg_trade:.2f} points")
    print(f"Average Duration:      {avg_duration:.1f} minutes")
    
    # Trade distribution by exit reason
    print("\nExit Reason Distribution:")
    exit_counts = trades_df['Exit_Reason'].value_counts()
    for reason, count in exit_counts.items():
        print(f"  {reason}: {count} ({count/total_trades*100:.1f}%)")
    
    # Trade distribution by type
    print("\nTrade Type Distribution:")
    type_counts = trades_df['Type'].value_counts()
    for trade_type, count in type_counts.items():
        print(f"  {trade_type}: {count} ({count/total_trades*100:.1f}%)")
    
    print("="*60)

def main():
    """
    Main function to run the backtest.
    """
    print("="*60)
    print("Fair Value Gap (FVG) Trading Strategy Backtest")
    print("="*60)
    
    try:
        # Load data
        df = load_and_combine_data()
        
        # Preprocess data
        df = preprocess_data(df)
        
        # Detect FVGs
        df = detect_fvg(df)
        
        # Run backtest
        trades_df = backtest_strategy(df)
        
        # Calculate statistics
        calculate_statistics(trades_df)
        
        # Save results
        if len(trades_df) > 0:
            # Create output DataFrame with required columns
            output_df = trades_df[[
                'Date', 
                'Entry_Price', 
                'Exit_Price', 
                'PnL', 
                'Duration_Minutes'
            ]].copy()
            output_df.columns = ['Date', 'Entry Price', 'Exit Price', 'PnL', 'Duration']
            
            # Save to CSV
            output_file = os.path.join(DATA_DIR, 'trades_results.csv')
            output_df.to_csv(output_file, index=False)
            print(f"\nTrades saved to: {output_file}")
            
            # Also save detailed trades
            detailed_file = os.path.join(DATA_DIR, 'trades_detailed.csv')
            trades_df.to_csv(detailed_file, index=False)
            print(f"Detailed trades saved to: {detailed_file}")
        else:
            print("\nNo trades to save!")
        
        print("\nBacktest completed successfully!")
        
    except Exception as e:
        print(f"\nError during backtest: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

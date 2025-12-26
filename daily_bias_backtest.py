"""
Backtest Script for NQ Daily Bias Methods
Author: Quantitative Researcher
Description: Backtests 4 methods to predict daily candle direction (Green/Red)
"""

import pandas as pd
import numpy as np
from datetime import datetime
import glob
import warnings
warnings.filterwarnings('ignore')


def load_and_prepare_data(pattern, name):
    """
    Load CSV files matching pattern and combine them into a single DataFrame
    
    Args:
        pattern: Glob pattern to match files
        name: Name of the timeframe for logging
    
    Returns:
        DataFrame with Date as index
    """
    files = sorted(glob.glob(pattern))
    if not files:
        raise ValueError(f"No files found for pattern: {pattern}")
    
    dfs = []
    for file in files:
        df = pd.read_csv(file, sep=';', header=0)
        dfs.append(df)
    
    combined = pd.concat(dfs, ignore_index=True)
    
    # Parse the date columns - they are in two columns: Column1 (date) and Column2 (time)
    # Format: DD/MM/YYYY HH:MM:SS
    combined['Date'] = pd.to_datetime(
        combined['Column1'] + ' ' + combined['Column2'],
        format='%d/%m/%Y %H:%M:%S'
    )
    
    # Rename columns to standard names
    combined = combined.rename(columns={
        'Column3': 'Open',
        'Column4': 'High',
        'Column5': 'Low',
        'Column6': 'Close',
        'Column7': 'Volume'
    })
    
    # Keep only relevant columns
    combined = combined[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
    
    # Sort by date and remove duplicates
    combined = combined.sort_values('Date').drop_duplicates(subset=['Date'])
    
    # Set Date as index
    combined.set_index('Date', inplace=True)
    
    print(f"Loaded {name}: {len(combined)} records from {combined.index[0]} to {combined.index[-1]}")
    
    return combined


def calculate_ema(series, period):
    """Calculate Exponential Moving Average"""
    return series.ewm(span=period, adjust=False).mean()


def calculate_rsi(close, period=14):
    """Calculate RSI (Relative Strength Index)"""
    delta = close.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi


def identify_swing_high(df, window=3):
    """
    Identify swing highs: High is higher than window candles on each side
    
    Args:
        df: DataFrame with High column
        window: Number of candles on each side
    
    Returns:
        Series with swing high values (NaN where no swing high)
    """
    swing_highs = pd.Series(index=df.index, dtype=float)
    
    for i in range(window, len(df) - window):
        current_high = df['High'].iloc[i]
        
        # Check if current high is higher than all candles in window on both sides
        left_highs = df['High'].iloc[i-window:i]
        right_highs = df['High'].iloc[i+1:i+window+1]
        
        if (current_high > left_highs.max()) and (current_high > right_highs.max()):
            swing_highs.iloc[i] = current_high
    
    return swing_highs


def identify_swing_low(df, window=3):
    """
    Identify swing lows: Low is lower than window candles on each side
    
    Args:
        df: DataFrame with Low column
        window: Number of candles on each side
    
    Returns:
        Series with swing low values (NaN where no swing low)
    """
    swing_lows = pd.Series(index=df.index, dtype=float)
    
    for i in range(window, len(df) - window):
        current_low = df['Low'].iloc[i]
        
        # Check if current low is lower than all candles in window on both sides
        left_lows = df['Low'].iloc[i-window:i]
        right_lows = df['Low'].iloc[i+1:i+window+1]
        
        if (current_low < left_lows.min()) and (current_low < right_lows.min()):
            swing_lows.iloc[i] = current_low
    
    return swing_lows


def calculate_indicators(df_d1, df_h4, df_h1):
    """
    Calculate all necessary indicators for the three timeframes
    
    Args:
        df_d1: Daily DataFrame
        df_h4: 4-hour DataFrame
        df_h1: 1-hour DataFrame (not used but kept for future extensions)
    
    Returns:
        Tuple of DataFrames with indicators
    """
    # D1 indicators
    df_d1 = df_d1.copy()
    df_d1['EMA20'] = calculate_ema(df_d1['Close'], 20)
    df_d1['EMA50'] = calculate_ema(df_d1['Close'], 50)
    df_d1['Prev_High'] = df_d1['High'].shift(1)
    df_d1['Prev_Low'] = df_d1['Low'].shift(1)
    df_d1['Prev_Close'] = df_d1['Close'].shift(1)
    df_d1['Prev_EMA20'] = df_d1['EMA20'].shift(1)
    df_d1['Prev_EMA50'] = df_d1['EMA50'].shift(1)
    
    # H4 indicators
    df_h4 = df_h4.copy()
    df_h4['RSI'] = calculate_rsi(df_h4['Close'], 14)
    df_h4['Swing_High'] = identify_swing_high(df_h4, window=3)
    df_h4['Swing_Low'] = identify_swing_low(df_h4, window=3)
    
    # Forward fill swing highs and lows to get the "last known" swing point
    df_h4['Last_Swing_High'] = df_h4['Swing_High'].fillna(method='ffill')
    df_h4['Last_Swing_Low'] = df_h4['Swing_Low'].fillna(method='ffill')
    
    print(f"\nD1 Indicators calculated: EMA20, EMA50, Prev_High, Prev_Low")
    print(f"H4 Indicators calculated: RSI, Swing_High, Swing_Low")
    
    return df_d1, df_h4, df_h1


def get_h4_data_before_date(df_h4, target_date):
    """
    Get the last H4 candle before the target date (before daily open)
    
    Args:
        df_h4: 4-hour DataFrame
        target_date: The date to look before
    
    Returns:
        The last H4 row before target_date, or None if not found
    """
    before_data = df_h4[df_h4.index < target_date]
    if len(before_data) > 0:
        return before_data.iloc[-1]
    return None


def method1_price_action_h4(df_d1, df_h4, current_date, current_row):
    """
    Method 1: Price Action H4
    If current price > last Swing High H4 = LONG
    If current price < last Swing Low H4 = SHORT
    Otherwise = NEUTRAL
    
    Args:
        df_d1: Daily DataFrame
        df_h4: 4-hour DataFrame
        current_date: Current date being analyzed
        current_row: Current D1 row
    
    Returns:
        Signal: 1 (LONG), -1 (SHORT), 0 (NEUTRAL)
    """
    # Get last H4 candle before current day opens
    last_h4 = get_h4_data_before_date(df_h4, current_date)
    
    if last_h4 is None:
        return 0
    
    current_price = current_row['Open']  # Price at the open of the day
    last_swing_high = last_h4['Last_Swing_High']
    last_swing_low = last_h4['Last_Swing_Low']
    
    if pd.isna(last_swing_high) or pd.isna(last_swing_low):
        return 0
    
    if current_price > last_swing_high:
        return 1  # LONG
    elif current_price < last_swing_low:
        return -1  # SHORT
    else:
        return 0  # NEUTRAL


def method2_trend_d1(current_row):
    """
    Method 2: Trend D1
    If Close(J-1) > EMA20(J-1) > EMA50(J-1) = LONG
    If Close(J-1) < EMA20(J-1) < EMA50(J-1) = SHORT
    Otherwise = NEUTRAL
    
    Args:
        current_row: Current D1 row (contains previous day's data via shift)
    
    Returns:
        Signal: 1 (LONG), -1 (SHORT), 0 (NEUTRAL)
    """
    prev_close = current_row['Prev_Close']
    prev_ema20 = current_row['Prev_EMA20']
    prev_ema50 = current_row['Prev_EMA50']
    
    if pd.isna(prev_close) or pd.isna(prev_ema20) or pd.isna(prev_ema50):
        return 0
    
    # LONG: Close > EMA20 > EMA50
    if prev_close > prev_ema20 and prev_ema20 > prev_ema50:
        return 1
    # SHORT: Close < EMA20 < EMA50
    elif prev_close < prev_ema20 and prev_ema20 < prev_ema50:
        return -1
    else:
        return 0


def method3_open_vs_prev(current_row):
    """
    Method 3: Open vs Previous Value
    If Open(J) > High(J-1) = LONG
    If Open(J) < Low(J-1) = SHORT
    Otherwise = NEUTRAL
    
    Args:
        current_row: Current D1 row (contains previous day's data via shift)
    
    Returns:
        Signal: 1 (LONG), -1 (SHORT), 0 (NEUTRAL)
    """
    current_open = current_row['Open']
    prev_high = current_row['Prev_High']
    prev_low = current_row['Prev_Low']
    
    if pd.isna(prev_high) or pd.isna(prev_low):
        return 0
    
    if current_open > prev_high:
        return 1  # LONG
    elif current_open < prev_low:
        return -1  # SHORT
    else:
        return 0  # NEUTRAL


def method4_triple_screen(df_h4, current_date, current_row):
    """
    Method 4: Triple Screen
    LONG if Close(J-1) > EMA20(J-1) AND RSI_H4(last candle J-1) > 50
    SHORT if Close(J-1) < EMA20(J-1) AND RSI_H4(last candle J-1) < 50
    Otherwise = NEUTRAL
    
    Args:
        df_h4: 4-hour DataFrame
        current_date: Current date being analyzed
        current_row: Current D1 row
    
    Returns:
        Signal: 1 (LONG), -1 (SHORT), 0 (NEUTRAL)
    """
    prev_close = current_row['Prev_Close']
    prev_ema20 = current_row['Prev_EMA20']
    
    if pd.isna(prev_close) or pd.isna(prev_ema20):
        return 0
    
    # Get last H4 candle from previous day
    last_h4 = get_h4_data_before_date(df_h4, current_date)
    
    if last_h4 is None or pd.isna(last_h4['RSI']):
        return 0
    
    last_rsi_h4 = last_h4['RSI']
    
    # LONG conditions
    if prev_close > prev_ema20 and last_rsi_h4 > 50:
        return 1
    # SHORT conditions
    elif prev_close < prev_ema20 and last_rsi_h4 < 50:
        return -1
    else:
        return 0


def run_backtest(df_d1, df_h4, df_h1):
    """
    Run backtest for all 4 methods
    
    Args:
        df_d1: Daily DataFrame with indicators
        df_h4: 4-hour DataFrame with indicators
        df_h1: 1-hour DataFrame (not used currently)
    
    Returns:
        DataFrame with results for each method
    """
    results = []
    
    # Start from a row where we have enough data for indicators
    start_idx = 60  # To ensure we have enough data for EMA50 and other indicators
    
    for i in range(start_idx, len(df_d1)):
        current_date = df_d1.index[i]
        current_row = df_d1.iloc[i]
        
        # Skip if we don't have complete data
        if pd.isna(current_row['Open']) or pd.isna(current_row['Close']):
            continue
        
        # Calculate actual outcome: Green (1) if Close > Open, Red (-1) if Close < Open
        actual_direction = 1 if current_row['Close'] > current_row['Open'] else -1
        
        # Calculate signals for each method
        signal_m1 = method1_price_action_h4(df_d1, df_h4, current_date, current_row)
        signal_m2 = method2_trend_d1(current_row)
        signal_m3 = method3_open_vs_prev(current_row)
        signal_m4 = method4_triple_screen(df_h4, current_date, current_row)
        
        # Calculate P&L for each method (absolute value of daily move)
        daily_move = abs(current_row['Close'] - current_row['Open'])
        
        results.append({
            'Date': current_date,
            'Actual': actual_direction,
            'Signal_M1': signal_m1,
            'Signal_M2': signal_m2,
            'Signal_M3': signal_m3,
            'Signal_M4': signal_m4,
            'Daily_Move': daily_move,
            'Open': current_row['Open'],
            'Close': current_row['Close']
        })
    
    return pd.DataFrame(results)


def calculate_performance_metrics(results_df):
    """
    Calculate performance metrics for each method
    
    Args:
        results_df: DataFrame with backtest results
    
    Returns:
        DataFrame with performance metrics
    """
    methods = ['M1', 'M2', 'M3', 'M4']
    metrics = []
    
    for method in methods:
        signal_col = f'Signal_{method}'
        
        # Filter only trades where signal is not neutral (0)
        trades = results_df[results_df[signal_col] != 0].copy()
        
        if len(trades) == 0:
            metrics.append({
                'Method': method,
                'Total_Trades': 0,
                'Win_Rate_%': 0.0,
                'Wins': 0,
                'Losses': 0,
                'Profit_Factor': 0.0,
                'Total_Wins_Move': 0.0,
                'Total_Losses_Move': 0.0
            })
            continue
        
        # Determine if trade was a win
        trades['Win'] = trades['Actual'] == trades[signal_col]
        
        # Calculate wins and losses
        wins = trades[trades['Win'] == True]
        losses = trades[trades['Win'] == False]
        
        num_wins = len(wins)
        num_losses = len(losses)
        total_trades = len(trades)
        win_rate = (num_wins / total_trades * 100) if total_trades > 0 else 0
        
        # Calculate profit factor (sum of winning moves / sum of losing moves)
        total_wins_move = wins['Daily_Move'].sum() if num_wins > 0 else 0
        total_losses_move = losses['Daily_Move'].sum() if num_losses > 0 else 0
        profit_factor = (total_wins_move / total_losses_move) if total_losses_move > 0 else float('inf')
        
        metrics.append({
            'Method': method,
            'Total_Trades': total_trades,
            'Win_Rate_%': round(win_rate, 2),
            'Wins': num_wins,
            'Losses': num_losses,
            'Profit_Factor': round(profit_factor, 2),
            'Total_Wins_Move': round(total_wins_move, 2),
            'Total_Losses_Move': round(total_losses_move, 2)
        })
    
    return pd.DataFrame(metrics)


def print_detailed_method_descriptions():
    """Print detailed descriptions of each method"""
    print("\n" + "="*80)
    print("METHOD DESCRIPTIONS")
    print("="*80)
    
    print("\nMethod 1 - Price Action H4 (Swing High/Low):")
    print("  LONG:    Current price > Last known Swing High on H4")
    print("  SHORT:   Current price < Last known Swing Low on H4")
    print("  NEUTRAL: Price between last swing high and swing low")
    
    print("\nMethod 2 - Trend D1 (EMA Alignment):")
    print("  LONG:    Close(J-1) > EMA20(J-1) > EMA50(J-1)")
    print("  SHORT:   Close(J-1) < EMA20(J-1) < EMA50(J-1)")
    print("  NEUTRAL: EMAs not aligned")
    
    print("\nMethod 3 - Open vs Previous Value:")
    print("  LONG:    Open(J) > High(J-1)")
    print("  SHORT:   Open(J) < Low(J-1)")
    print("  NEUTRAL: Open(J) within previous day's range")
    
    print("\nMethod 4 - Triple Screen (EMA + RSI):")
    print("  LONG:    Close(J-1) > EMA20(J-1) AND RSI_H4(last) > 50")
    print("  SHORT:   Close(J-1) < EMA20(J-1) AND RSI_H4(last) < 50")
    print("  NEUTRAL: Conditions not met")
    
    print("\n" + "="*80)


def main():
    """Main execution function"""
    print("="*80)
    print("NQ DAILY BIAS BACKTEST - 4 METHODS COMPARISON")
    print("="*80)
    print("\nData: Nasdaq (NQ) from 2018 to 2025")
    print("Timezone: UTC-6 (Chicago Time) - NO CONVERSION NEEDED")
    print("Objective: Predict daily candle direction (Green/Red)")
    
    # Load data
    print("\n" + "-"*80)
    print("LOADING DATA")
    print("-"*80)
    
    base_path = '/home/runner/work/Backtest-Trading/Backtest-Trading'
    
    df_d1 = load_and_prepare_data(f'{base_path}/*1D.csv', 'Daily (D1)')
    df_h4 = load_and_prepare_data(f'{base_path}/*4H.csv', '4-Hour (H4)')
    df_h1 = load_and_prepare_data(f'{base_path}/*1H.csv', '1-Hour (H1)')
    
    # Calculate indicators
    print("\n" + "-"*80)
    print("CALCULATING INDICATORS")
    print("-"*80)
    
    df_d1, df_h4, df_h1 = calculate_indicators(df_d1, df_h4, df_h1)
    
    # Print method descriptions
    print_detailed_method_descriptions()
    
    # Run backtest
    print("\n" + "-"*80)
    print("RUNNING BACKTEST")
    print("-"*80)
    
    results_df = run_backtest(df_d1, df_h4, df_h1)
    
    print(f"\nBacktest completed: {len(results_df)} days analyzed")
    print(f"Period: {results_df['Date'].min()} to {results_df['Date'].max()}")
    
    # Calculate performance metrics
    print("\n" + "-"*80)
    print("PERFORMANCE METRICS")
    print("-"*80)
    
    metrics_df = calculate_performance_metrics(results_df)
    
    # Display results
    print("\n" + "="*80)
    print("COMPARATIVE RESULTS TABLE")
    print("="*80)
    print("\n" + metrics_df.to_string(index=False))
    
    # Summary statistics
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    
    best_win_rate = metrics_df.loc[metrics_df['Win_Rate_%'].idxmax()]
    best_profit_factor = metrics_df.loc[metrics_df['Profit_Factor'].idxmax()]
    most_trades = metrics_df.loc[metrics_df['Total_Trades'].idxmax()]
    
    print(f"\nBest Win Rate:      Method {best_win_rate['Method']} ({best_win_rate['Win_Rate_%']}%)")
    print(f"Best Profit Factor: Method {best_profit_factor['Method']} ({best_profit_factor['Profit_Factor']})")
    print(f"Most Active:        Method {most_trades['Method']} ({most_trades['Total_Trades']} trades)")
    
    print("\n" + "="*80)
    print("NOTES")
    print("="*80)
    print("- Win: Signal matches actual direction (Long+Green or Short+Red)")
    print("- Profit Factor: Sum of winning moves / Sum of losing moves")
    print("- Higher Profit Factor indicates better risk/reward performance")
    print("- Neutral signals (0) are excluded from trade counts")
    print("="*80)
    
    # Save results to CSV
    output_file = f'{base_path}/backtest_results.csv'
    results_df.to_csv(output_file, index=False)
    print(f"\nDetailed results saved to: {output_file}")
    
    metrics_file = f'{base_path}/backtest_metrics.csv'
    metrics_df.to_csv(metrics_file, index=False)
    print(f"Performance metrics saved to: {metrics_file}")


if __name__ == "__main__":
    main()

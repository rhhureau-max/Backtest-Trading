#!/usr/bin/env python3
"""
London Continuation Backtesting Strategy for NQ Futures

Strategy Logic:
1. Asian Range (19:00 CST D-1 to 00:00 CST D): Establish High/Low reference
2. London Killzone (01:00-04:00 CST): Only entry window
3. Breakout Detection: Price closes above Asian_High or below Asian_Low
4. Continuation Validation: 
   - No retracement below 50% of Asian Range (for bullish)
   - Volume > 20-period MA
5. Exit: 07:00 CST (before NY open)

Data is already in Chicago Time (CST/CDT) - NO timezone conversion needed.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')


def load_nq_data(years=None, timeframe='15m', base_path=None):
    """
    Load NQ futures data from CSV files.
    
    Parameters:
    -----------
    years : list, optional
        List of years to load. If None, loads 2018-2025.
    timeframe : str
        Timeframe to use: '15m' or '1H'
    base_path : Path or str, optional
        Base directory containing CSV files. If None, uses current directory.
    
    Returns:
    --------
    pd.DataFrame with datetime index and OHLCV columns
    """
    if years is None:
        years = list(range(2018, 2026))
    
    if base_path is None:
        base_path = Path.cwd()
    else:
        base_path = Path(base_path)
    dfs = []
    
    for year in years:
        filename = f"{year} {timeframe}.csv"
        filepath = base_path / filename
        
        if not filepath.exists():
            print(f"Warning: {filename} not found, skipping...")
            continue
        
        try:
            # Read CSV with semicolon delimiter
            df = pd.read_csv(filepath, sep=';', encoding='utf-8-sig')
            
            # Handle column names (remove BOM if present)
            df.columns = df.columns.str.replace('\ufeff', '').str.strip()
            
            # Rename columns to standard names
            if len(df.columns) >= 7:
                df.columns = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
            
            # Combine date and time into datetime
            df['DateTime'] = pd.to_datetime(
                df['Date'] + ' ' + df['Time'],
                format='%d/%m/%Y %H:%M:%S'
            )
            
            # Set datetime as index
            df.set_index('DateTime', inplace=True)
            
            # Keep only OHLCV columns
            df = df[['Open', 'High', 'Low', 'Close', 'Volume']]
            
            # Convert to numeric
            for col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            
            dfs.append(df)
            print(f"Loaded {year} {timeframe}: {len(df)} bars")
            
        except Exception as e:
            print(f"Error loading {filename}: {e}")
            continue
    
    if not dfs:
        raise ValueError("No data loaded!")
    
    # Concatenate all dataframes
    data = pd.concat(dfs)
    data.sort_index(inplace=True)
    
    # Remove duplicates
    data = data[~data.index.duplicated(keep='first')]
    
    print(f"\nTotal data loaded: {len(data)} bars from {data.index[0]} to {data.index[-1]}")
    
    return data


def identify_asian_range(df, date):
    """
    Identify Asian Range for a given date.
    Asian Range: 19:00 (D-1) to 00:00 (D) Chicago Time
    
    Parameters:
    -----------
    df : pd.DataFrame
        OHLCV data with datetime index
    date : datetime.date
        The target date
    
    Returns:
    --------
    dict with asian_high, asian_low, asian_range, or None if insufficient data
    """
    # Asian session starts at 19:00 on previous day
    prev_date = date - timedelta(days=1)
    
    # Define time range
    start_time = pd.Timestamp(year=prev_date.year, month=prev_date.month, 
                              day=prev_date.day, hour=19, minute=0)
    end_time = pd.Timestamp(year=date.year, month=date.month, 
                           day=date.day, hour=0, minute=0)
    
    # Filter data for Asian session
    asian_data = df[(df.index >= start_time) & (df.index < end_time)]
    
    if len(asian_data) < 5:  # Require at least 5 bars
        return None
    
    asian_high = asian_data['High'].max()
    asian_low = asian_data['Low'].min()
    asian_range = asian_high - asian_low
    asian_mid = (asian_high + asian_low) / 2
    
    return {
        'asian_high': asian_high,
        'asian_low': asian_low,
        'asian_range': asian_range,
        'asian_mid': asian_mid,
        'start_time': start_time,
        'end_time': end_time,
        'bars_count': len(asian_data)
    }


def calculate_volume_ma(df, periods=20):
    """Calculate rolling volume moving average."""
    return df['Volume'].rolling(window=periods, min_periods=1).mean()


def detect_breakout_in_london_killzone(df, date, asian_info):
    """
    Detect breakout during London Killzone (01:00-04:00 CST).
    
    Returns:
    --------
    dict with breakout info or None
    """
    asian_high = asian_info['asian_high']
    asian_low = asian_info['asian_low']
    
    # London Killzone: 01:00 to 04:00
    start_time = pd.Timestamp(year=date.year, month=date.month, 
                              day=date.day, hour=1, minute=0)
    end_time = pd.Timestamp(year=date.year, month=date.month, 
                           day=date.day, hour=4, minute=0)
    
    # Filter data for London Killzone
    london_data = df[(df.index >= start_time) & (df.index <= end_time)].copy()
    
    if len(london_data) == 0:
        return None
    
    # Calculate volume MA for the entire dataset up to this point
    vol_ma = calculate_volume_ma(df)
    
    # Check each bar for breakout
    for idx, row in london_data.iterrows():
        close_price = row['Close']
        volume = row['Volume']
        
        # Get volume MA at this timestamp
        vol_ma_value = vol_ma.loc[idx] if idx in vol_ma.index else None
        
        # Check for bullish breakout (close above Asian High)
        if close_price > asian_high:
            if vol_ma_value is not None and volume > vol_ma_value:
                return {
                    'entry_time': idx,
                    'entry_price': close_price,
                    'direction': 'LONG',
                    'asian_high': asian_high,
                    'asian_low': asian_low,
                    'asian_mid': asian_info['asian_mid'],
                    'volume': volume,
                    'volume_ma': vol_ma_value,
                    'breakout_bar': row.to_dict()
                }
        
        # Check for bearish breakout (close below Asian Low)
        elif close_price < asian_low:
            if vol_ma_value is not None and volume > vol_ma_value:
                return {
                    'entry_time': idx,
                    'entry_price': close_price,
                    'direction': 'SHORT',
                    'asian_high': asian_high,
                    'asian_low': asian_low,
                    'asian_mid': asian_info['asian_mid'],
                    'volume': volume,
                    'volume_ma': vol_ma_value,
                    'breakout_bar': row.to_dict()
                }
    
    return None


def validate_continuation(df, breakout_info):
    """
    Validate continuation after breakout (anti-fakeout filter).
    
    For bullish breakout: Price should not drop below Asian_Mid in next 2 hours
    For bearish breakout: Price should not rise above Asian_Mid in next 2 hours
    
    Returns:
    --------
    bool: True if continuation is valid, False otherwise
    """
    entry_time = breakout_info['entry_time']
    direction = breakout_info['direction']
    asian_mid = breakout_info['asian_mid']
    
    # Check next 2 hours after entry
    validation_end = entry_time + timedelta(hours=2)
    
    # Get data in validation window
    validation_data = df[(df.index > entry_time) & (df.index <= validation_end)]
    
    if len(validation_data) == 0:
        return False
    
    if direction == 'LONG':
        # For longs, price should not drop below Asian_Mid (50% retracement)
        min_low = validation_data['Low'].min()
        if min_low < asian_mid:
            return False
    
    elif direction == 'SHORT':
        # For shorts, price should not rise above Asian_Mid (50% retracement)
        max_high = validation_data['High'].max()
        if max_high > asian_mid:
            return False
    
    return True


def calculate_exit_result(df, breakout_info, date):
    """
    Calculate trade result at 07:00 CST exit.
    
    Returns:
    --------
    dict with exit info
    """
    entry_price = breakout_info['entry_price']
    direction = breakout_info['direction']
    
    # Exit at 07:00 CST
    exit_time = pd.Timestamp(year=date.year, month=date.month, 
                            day=date.day, hour=7, minute=0)
    
    # Find the closest bar at or after 07:00
    exit_data = df[df.index >= exit_time]
    
    if len(exit_data) == 0:
        return None
    
    # Use the first available bar's close price
    exit_bar = exit_data.iloc[0]
    exit_price = exit_bar['Close']
    actual_exit_time = exit_data.index[0]
    
    # Calculate P&L in points
    if direction == 'LONG':
        pnl_points = exit_price - entry_price
    else:  # SHORT
        pnl_points = entry_price - exit_price
    
    # Determine Win/Loss
    result = 'WIN' if pnl_points > 0 else 'LOSS'
    
    return {
        'exit_time': actual_exit_time,
        'exit_price': exit_price,
        'pnl_points': pnl_points,
        'result': result
    }


def run_backtest(df, start_year=2018, end_year=2025):
    """
    Run the complete London Continuation backtest.
    
    Returns:
    --------
    pd.DataFrame with all trades
    """
    trades = []
    
    # Get unique dates in the dataset
    dates = df.index.date
    unique_dates = sorted(set(dates))
    
    print(f"\nBacktesting from {unique_dates[0]} to {unique_dates[-1]}")
    print(f"Total trading days to analyze: {len(unique_dates)}\n")
    
    # Iterate through each date
    for i, date in enumerate(unique_dates[1:], 1):  # Skip first date (need D-1 for Asian)
        
        # Progress indicator
        if i % 100 == 0:
            print(f"Processing: {date} ({i}/{len(unique_dates)-1})")
        
        # Step 1: Identify Asian Range
        asian_info = identify_asian_range(df, date)
        if asian_info is None:
            continue
        
        # Step 2: Detect breakout in London Killzone
        breakout_info = detect_breakout_in_london_killzone(df, date, asian_info)
        if breakout_info is None:
            continue
        
        # Step 3: Validate continuation (anti-fakeout)
        is_valid = validate_continuation(df, breakout_info)
        if not is_valid:
            continue
        
        # Step 4: Calculate exit result at 07:00 CST
        exit_info = calculate_exit_result(df, breakout_info, date)
        if exit_info is None:
            continue
        
        # Compile trade information
        trade = {
            'Date': date,
            'Entry_Time': breakout_info['entry_time'],
            'Direction': breakout_info['direction'],
            'Entry_Price': breakout_info['entry_price'],
            'Exit_Time': exit_info['exit_time'],
            'Exit_Price': exit_info['exit_price'],
            'PnL_Points': exit_info['pnl_points'],
            'Result': exit_info['result'],
            'Asian_High': breakout_info['asian_high'],
            'Asian_Low': breakout_info['asian_low'],
            'Asian_Range': breakout_info['asian_high'] - breakout_info['asian_low'],
            'Volume': breakout_info['volume'],
            'Volume_MA_20': breakout_info['volume_ma']
        }
        
        trades.append(trade)
    
    # Create DataFrame from trades
    trades_df = pd.DataFrame(trades)
    
    return trades_df


def analyze_results(trades_df):
    """
    Analyze and print backtest results.
    """
    if len(trades_df) == 0:
        print("No trades found!")
        return
    
    print("\n" + "="*80)
    print("LONDON CONTINUATION BACKTEST RESULTS")
    print("="*80)
    
    # Overall statistics
    total_trades = len(trades_df)
    win_mask = trades_df['Result'] == 'WIN'
    loss_mask = trades_df['Result'] == 'LOSS'
    wins = win_mask.sum()
    losses = loss_mask.sum()
    win_rate = (wins / total_trades * 100) if total_trades > 0 else 0
    
    total_pnl = trades_df['PnL_Points'].sum()
    avg_win = trades_df.loc[win_mask, 'PnL_Points'].mean() if wins > 0 else 0
    avg_loss = trades_df.loc[loss_mask, 'PnL_Points'].mean() if losses > 0 else 0
    
    # Calculate profit factor
    profit_mask = trades_df['PnL_Points'] > 0
    loss_pnl_mask = trades_df['PnL_Points'] < 0
    gross_profit = trades_df.loc[profit_mask, 'PnL_Points'].sum()
    gross_loss = abs(trades_df.loc[loss_pnl_mask, 'PnL_Points'].sum())
    
    if gross_loss > 0:
        profit_factor = gross_profit / gross_loss
    elif gross_profit > 0:
        profit_factor = float('inf')  # All wins, no losses
    else:
        profit_factor = 0.0  # No profit at all
    
    print(f"\nTotal Trades: {total_trades}")
    print(f"Wins: {wins} | Losses: {losses}")
    print(f"Win Rate: {win_rate:.2f}%")
    print(f"\nTotal P&L: {total_pnl:.2f} points")
    print(f"Average Win: {avg_win:.2f} points")
    print(f"Average Loss: {avg_loss:.2f} points")
    print(f"Profit Factor: {profit_factor:.2f}")
    
    # Direction breakdown
    print(f"\n--- Direction Breakdown ---")
    long_mask = trades_df['Direction'] == 'LONG'
    short_mask = trades_df['Direction'] == 'SHORT'
    long_trades = trades_df[long_mask]
    short_trades = trades_df[short_mask]
    
    long_wr = (len(long_trades[long_trades['Result'] == 'WIN']) / len(long_trades) * 100) if len(long_trades) > 0 else 0
    short_wr = (len(short_trades[short_trades['Result'] == 'WIN']) / len(short_trades) * 100) if len(short_trades) > 0 else 0
    
    print(f"LONG Trades: {len(long_trades)} | Win Rate: {long_wr:.2f}% | P&L: {long_trades['PnL_Points'].sum():.2f}")
    print(f"SHORT Trades: {len(short_trades)} | Win Rate: {short_wr:.2f}% | P&L: {short_trades['PnL_Points'].sum():.2f}")
    
    # Yearly breakdown
    print(f"\n--- Yearly Breakdown ---")
    trades_df['Year'] = trades_df['Date'].apply(lambda x: x.year)
    for year in sorted(trades_df['Year'].unique()):
        year_trades = trades_df[trades_df['Year'] == year]
        year_wins = len(year_trades[year_trades['Result'] == 'WIN'])
        year_wr = (year_wins / len(year_trades) * 100) if len(year_trades) > 0 else 0
        year_pnl = year_trades['PnL_Points'].sum()
        print(f"{year}: {len(year_trades)} trades | WR: {year_wr:.2f}% | P&L: {year_pnl:.2f}")
    
    print("\n" + "="*80)


def main(output_file=None):
    """
    Main execution function.
    
    Parameters:
    -----------
    output_file : str, optional
        Path to save results CSV. If None, saves to current directory.
    """
    print("="*80)
    print("LONDON CONTINUATION BACKTEST - NQ Futures")
    print("="*80)
    print("\nStrategy Parameters:")
    print("- Asian Range: 19:00 (D-1) to 00:00 (D) CST")
    print("- London Killzone: 01:00 to 04:00 CST (Entry Window)")
    print("- Breakout: Close above Asian_High (Long) or below Asian_Low (Short)")
    print("- Volume Filter: Volume > 20-period MA")
    print("- Continuation: No 50% retracement in 2 hours")
    print("- Exit: 07:00 CST (before NY open)")
    print("="*80)
    
    # Load data
    print("\nLoading NQ data...")
    df = load_nq_data(timeframe='15m')  # Use 15-minute bars
    
    # Run backtest
    print("\nRunning backtest...")
    trades_df = run_backtest(df)
    
    # Analyze results
    analyze_results(trades_df)
    
    # Save results to CSV
    if output_file is None:
        output_file = Path.cwd() / 'london_continuation_results.csv'
    else:
        output_file = Path(output_file)
    
    trades_df.to_csv(output_file, index=False)
    print(f"\nResults saved to: {output_file}")
    
    # Display first few trades
    print(f"\nFirst 10 trades:")
    print(trades_df.head(10).to_string())
    
    return trades_df


if __name__ == "__main__":
    trades_df = main()

#!/usr/bin/env python3
"""
Impulsive 8:30 Candle Strategy Backtest

This script analyzes the 8:30 impulsive candle strategy across multiple years of data.
It tests various risk-reward ratios with both 50% and 100% retracement stop-loss settings.
"""

import os
import glob
import pandas as pd
import numpy as np

# Configuration
DATA_DIR = os.path.dirname(os.path.abspath(__file__))
MIN_CANDLE_RANGE = 50  # Minimum points for impulsive candle
TARGET_TIME = "08:30:00"
RR_RATIOS = [1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]
MAX_CANDLES_LOOKAHEAD = 500  # Maximum candles to look ahead for trade resolution


def load_15m_data(data_dir):
    """Load all 15-minute CSV files from the data directory."""
    pattern = os.path.join(data_dir, "*15m.csv")
    files = sorted(glob.glob(pattern))
    
    all_data = []
    
    for filepath in files:
        filename = os.path.basename(filepath)
        print(f"Loading {filename}...")
        
        # Read CSV with semicolon delimiter
        df = pd.read_csv(
            filepath,
            sep=';',
            names=['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume'],
            skiprows=1  # Skip header row
        )
        
        # Parse datetime
        df['DateTime'] = pd.to_datetime(
            df['Date'] + ' ' + df['Time'],
            format='%d/%m/%Y %H:%M:%S'
        )
        
        # Sort by datetime
        df = df.sort_values('DateTime').reset_index(drop=True)
        
        all_data.append(df)
    
    combined = pd.concat(all_data, ignore_index=True)
    combined = combined.sort_values('DateTime').reset_index(drop=True)
    
    print(f"\nTotal rows loaded: {len(combined):,}")
    return combined


def find_impulsive_candles(df, target_time=TARGET_TIME, min_range=MIN_CANDLE_RANGE):
    """Find all 8:30 candles with range > min_range points."""
    # Filter for target time
    target_candles = df[df['Time'] == target_time].copy()
    
    # Calculate candle range
    target_candles['Range'] = target_candles['High'] - target_candles['Low']
    
    # Filter for impulsive candles (range > min_range)
    impulsive = target_candles[target_candles['Range'] > min_range].copy()
    
    # Determine direction
    impulsive['Direction'] = np.where(
        impulsive['Close'] > impulsive['Open'], 'LONG', 'SHORT'
    )
    
    print(f"Found {len(impulsive)} impulsive {target_time} candles (range > {min_range} points)")
    
    return impulsive


def simulate_trade_fast(highs, lows, entry, sl, tp, direction):
    """
    Fast trade simulation using numpy arrays.
    Returns: 'TP_HIT', 'SL_HIT', or 'NO_RESULT'
    """
    if len(highs) == 0:
        return 'NO_RESULT'
    
    if direction == 'LONG':
        # Find first candle where SL is hit (low <= sl)
        sl_hits = np.where(lows <= sl)[0]
        # Find first candle where TP is hit (high >= tp)
        tp_hits = np.where(highs >= tp)[0]
    else:  # SHORT
        # Find first candle where SL is hit (high >= sl)
        sl_hits = np.where(highs >= sl)[0]
        # Find first candle where TP is hit (low <= tp)
        tp_hits = np.where(lows <= tp)[0]
    
    sl_idx = sl_hits[0] if len(sl_hits) > 0 else float('inf')
    tp_idx = tp_hits[0] if len(tp_hits) > 0 else float('inf')
    
    if sl_idx == float('inf') and tp_idx == float('inf'):
        return 'NO_RESULT'
    elif sl_idx < tp_idx:
        return 'SL_HIT'
    elif tp_idx < sl_idx:
        return 'TP_HIT'
    else:  # Same candle - assume SL hit first (conservative)
        return 'SL_HIT'


def backtest_strategy(df, impulsive_candles):
    """Run the backtest for all impulsive candles with different SL and TP settings."""
    results = []
    
    # Convert to numpy arrays for fast access
    df_indexed = df.reset_index(drop=True)
    all_highs = df_indexed['High'].values
    all_lows = df_indexed['Low'].values
    
    # Create index mapping
    datetime_to_idx = {dt: idx for idx, dt in enumerate(df_indexed['DateTime'])}
    
    total_candles = len(impulsive_candles)
    max_idx = len(df_indexed)
    
    for i, (_, candle) in enumerate(impulsive_candles.iterrows()):
        if (i + 1) % 100 == 0:
            print(f"Processing candle {i + 1}/{total_candles}...")
        
        entry_dt = candle['DateTime']
        entry_idx = datetime_to_idx.get(entry_dt)
        
        if entry_idx is None:
            continue
        
        direction = candle['Direction']
        entry = candle['Close']
        high = candle['High']
        low = candle['Low']
        candle_range = candle['Range']
        
        if direction == 'LONG':
            # 50% retracement SL
            sl_50 = entry - 0.5 * (entry - low)
            risk_50 = entry - sl_50
            
            # 100% retracement SL
            sl_100 = low
            risk_100 = entry - sl_100
        else:  # SHORT
            # 50% retracement SL
            sl_50 = entry + 0.5 * (high - entry)
            risk_50 = sl_50 - entry
            
            # 100% retracement SL
            sl_100 = high
            risk_100 = sl_100 - entry
        
        # Get subsequent candle data (limited lookahead for performance)
        start_idx = entry_idx + 1
        end_idx = min(entry_idx + 1 + MAX_CANDLES_LOOKAHEAD, max_idx)
        
        subsequent_highs = all_highs[start_idx:end_idx]
        subsequent_lows = all_lows[start_idx:end_idx]
        
        # Test each R:R ratio for each SL setting
        for rr in RR_RATIOS:
            for sl_type, sl, risk in [('50%', sl_50, risk_50), ('100%', sl_100, risk_100)]:
                if direction == 'LONG':
                    tp = entry + risk * rr
                else:  # SHORT
                    tp = entry - risk * rr
                
                result = simulate_trade_fast(subsequent_highs, subsequent_lows, entry, sl, tp, direction)
                
                results.append({
                    'Date': candle['Date'],
                    'Time': candle['Time'],
                    'DateTime': entry_dt,
                    'Direction': direction,
                    'Entry': round(entry, 2),
                    'High': round(high, 2),
                    'Low': round(low, 2),
                    'CandleRange': round(candle_range, 2),
                    'SL_Type': sl_type,
                    'SL': round(sl, 2),
                    'Risk': round(risk, 2),
                    'RR_Ratio': rr,
                    'TP': round(tp, 2),
                    'Result': result
                })
    
    return pd.DataFrame(results)


def calculate_statistics(results_df):
    """Calculate summary statistics for the backtest results."""
    summary_data = []
    
    # Group by SL_Type, Direction, and RR_Ratio
    for sl_type in ['50%', '100%']:
        for direction in ['LONG', 'SHORT', 'ALL']:
            for rr in RR_RATIOS:
                if direction == 'ALL':
                    subset = results_df[
                        (results_df['SL_Type'] == sl_type) &
                        (results_df['RR_Ratio'] == rr)
                    ]
                else:
                    subset = results_df[
                        (results_df['SL_Type'] == sl_type) &
                        (results_df['Direction'] == direction) &
                        (results_df['RR_Ratio'] == rr)
                    ]
                
                total_trades = len(subset)
                tp_hits = len(subset[subset['Result'] == 'TP_HIT'])
                sl_hits = len(subset[subset['Result'] == 'SL_HIT'])
                no_results = len(subset[subset['Result'] == 'NO_RESULT'])
                
                if total_trades > 0:
                    # Win rate based on completed trades (excluding NO_RESULT)
                    completed_trades = tp_hits + sl_hits
                    win_rate = (tp_hits / completed_trades * 100) if completed_trades > 0 else 0
                    
                    # Net R per trade: (tp_wins * rr - sl_losses) / total_completed_trades
                    if completed_trades > 0:
                        expected_r = ((tp_hits * rr) - sl_hits) / completed_trades
                    else:
                        expected_r = 0
                else:
                    win_rate = 0
                    expected_r = 0
                
                summary_data.append({
                    'SL_Type': sl_type,
                    'Direction': direction,
                    'RR_Ratio': rr,
                    'Total_Trades': total_trades,
                    'TP_Hits': tp_hits,
                    'SL_Hits': sl_hits,
                    'No_Result': no_results,
                    'Completed_Trades': tp_hits + sl_hits,
                    'Win_Rate_%': round(win_rate, 2),
                    'Expected_R': round(expected_r, 4)
                })
    
    return pd.DataFrame(summary_data)


def print_results(summary_df):
    """Print formatted results to console."""
    print("\n" + "=" * 100)
    print("IMPULSIVE 8:30 CANDLE STRATEGY BACKTEST RESULTS")
    print("=" * 100)
    
    for sl_type in ['50%', '100%']:
        print(f"\n{'=' * 50}")
        print(f"STOP LOSS: {sl_type} RETRACEMENT")
        print(f"{'=' * 50}")
        
        for direction in ['LONG', 'SHORT', 'ALL']:
            subset = summary_df[
                (summary_df['SL_Type'] == sl_type) &
                (summary_df['Direction'] == direction)
            ]
            
            print(f"\n--- {direction} Trades ---")
            print(f"{'R:R Ratio':<12} {'Total':<8} {'TP Hits':<10} {'SL Hits':<10} {'Win Rate':<12} {'Expected R':<12}")
            print("-" * 64)
            
            for _, row in subset.iterrows():
                print(f"{row['RR_Ratio']:<12} {row['Completed_Trades']:<8} {row['TP_Hits']:<10} {row['SL_Hits']:<10} {row['Win_Rate_%']:<12.2f}% {row['Expected_R']:<12.4f}")


def main():
    print("=" * 60)
    print("Impulsive 8:30 Candle Strategy Backtest")
    print("=" * 60)
    
    # Load data
    print("\n[1/4] Loading 15-minute data...")
    df = load_15m_data(DATA_DIR)
    
    # Find impulsive candles
    print("\n[2/4] Finding impulsive 8:30 candles...")
    impulsive_candles = find_impulsive_candles(df)
    
    # Count by direction
    long_count = len(impulsive_candles[impulsive_candles['Direction'] == 'LONG'])
    short_count = len(impulsive_candles[impulsive_candles['Direction'] == 'SHORT'])
    print(f"  - LONG: {long_count}")
    print(f"  - SHORT: {short_count}")
    
    # Run backtest
    print("\n[3/4] Running backtest simulations...")
    results_df = backtest_strategy(df, impulsive_candles)
    
    # Save detailed results
    results_path = os.path.join(DATA_DIR, 'impulsive_candle_results.csv')
    results_df.to_csv(results_path, index=False)
    print(f"\nDetailed results saved to: {results_path}")
    
    # Calculate and save summary statistics
    print("\n[4/4] Calculating summary statistics...")
    summary_df = calculate_statistics(results_df)
    
    summary_path = os.path.join(DATA_DIR, 'impulsive_candle_summary.csv')
    summary_df.to_csv(summary_path, index=False)
    print(f"Summary statistics saved to: {summary_path}")
    
    # Print results
    print_results(summary_df)
    
    print("\n" + "=" * 60)
    print("Backtest Complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()

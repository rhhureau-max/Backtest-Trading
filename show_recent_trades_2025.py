"""
Show Recent 2025 Trades for Top Win Rate Scenarios
===================================================

This script displays the most recent trades from 2025 for the two scenarios
with the highest win rates:
1. Gap Up Continuation (75% WR)
2. Inside Day Expansion (71% WR)

Author: Senior Quant Analyst
Date: 2025-12-10
"""

import pandas as pd
import numpy as np
from datetime import datetime
import os
import warnings
warnings.filterwarnings('ignore')


def load_nq_data(csv_dir='.'):
    """Load NQ daily and hourly data from CSV files."""
    
    # Load daily data
    daily_files = []
    for year in range(2018, 2026):
        filepath = os.path.join(csv_dir, f'{year} 1D.csv')
        if os.path.exists(filepath):
            daily_files.append(filepath)
    
    if not daily_files:
        raise FileNotFoundError("No daily CSV files found")
    
    dfs_1d = []
    for file in daily_files:
        df = pd.read_csv(file, sep=';', skiprows=1, header=None,
                        names=['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume'])
        df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%d/%m/%Y %H:%M:%S')
        dfs_1d.append(df)
    
    df_1d = pd.concat(dfs_1d, ignore_index=True)
    df_1d = df_1d.sort_values('Datetime').reset_index(drop=True)
    
    # Load hourly data
    hourly_files = []
    for year in range(2018, 2026):
        filepath = os.path.join(csv_dir, f'{year} 1H.csv')
        if os.path.exists(filepath):
            hourly_files.append(filepath)
    
    if not hourly_files:
        raise FileNotFoundError("No hourly CSV files found")
    
    dfs_1h = []
    for file in hourly_files:
        df = pd.read_csv(file, sep=';', skiprows=1, header=None,
                        names=['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume'])
        df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%d/%m/%Y %H:%M:%S')
        dfs_1h.append(df)
    
    df_1h = pd.concat(dfs_1h, ignore_index=True)
    df_1h = df_1h.sort_values('Datetime').reset_index(drop=True)
    
    return df_1d, df_1h


def analyze_gap_up_continuation(df_1d, df_1h):
    """Analyze Gap Up Continuation scenario and return 2025 trades."""
    
    trades = []
    
    for i in range(1, len(df_1d)):
        current = df_1d.iloc[i]
        prev = df_1d.iloc[i-1]
        
        # Calculate gap
        gap_pct = ((current['Open'] - prev['Close']) / prev['Close']) * 100
        
        if gap_pct > 0.3:  # Gap up > 0.3%
            # Check if gap filled in first hour
            current_date = current['Datetime'].date()
            hourly_session = df_1h[df_1h['Datetime'].dt.date == current_date]
            
            if len(hourly_session) > 0:
                first_hour_candles = hourly_session.head(1)
                gap_filled = first_hour_candles['Low'].min() < prev['Close']
                
                if not gap_filled:  # Gap not filled
                    # Determine if finished higher than open
                    finished_higher = current['Close'] > current['Open']
                    return_pts = current['Close'] - current['Open']
                    
                    trades.append({
                        'Date': current['Datetime'].strftime('%Y-%m-%d'),
                        'Gap_Size': f"{gap_pct:.2f}%",
                        'Open': f"{current['Open']:.2f}",
                        'Close': f"{current['Close']:.2f}",
                        'Return_pts': f"{return_pts:.2f}",
                        'Win': '✅' if finished_higher else '❌',
                        'Result': 'WIN' if finished_higher else 'LOSS'
                    })
    
    return trades


def analyze_inside_day_expansion(df_1d):
    """Analyze Inside Day Expansion scenario and return 2025 trades."""
    
    trades = []
    
    for i in range(1, len(df_1d) - 1):
        current = df_1d.iloc[i]
        prev = df_1d.iloc[i-1]
        next_day = df_1d.iloc[i+1]
        
        # Check if current day is Inside Day
        is_inside = (current['High'] < prev['High'] and 
                     current['Low'] > prev['Low'])
        
        if is_inside:
            # Check if next day breaks out bullishly
            breakout = next_day['High'] > current['High']
            
            if breakout:
                # Check if finished green
                finished_green = next_day['Close'] > next_day['Open']
                return_pts = next_day['Close'] - next_day['Open']
                
                trades.append({
                    'Inside_Day': current['Datetime'].strftime('%Y-%m-%d'),
                    'Breakout_Day': next_day['Datetime'].strftime('%Y-%m-%d'),
                    'Inside_High': f"{current['High']:.2f}",
                    'Break_High': f"{next_day['High']:.2f}",
                    'Open': f"{next_day['Open']:.2f}",
                    'Close': f"{next_day['Close']:.2f}",
                    'Return_pts': f"{return_pts:.2f}",
                    'Win': '✅' if finished_green else '❌',
                    'Result': 'WIN' if finished_green else 'LOSS'
                })
    
    return trades


def main():
    print("=" * 80)
    print("🚀 RECENT 2025 TRADES - TOP WIN RATE SCENARIOS")
    print("=" * 80)
    print()
    print("Loading NQ data...")
    
    df_1d, df_1h = load_nq_data()
    
    # Filter for 2025 only
    df_1d_2025 = df_1d[df_1d['Datetime'].dt.year == 2025].copy()
    df_1h_2025 = df_1h[df_1h['Datetime'].dt.year == 2025].copy()
    
    print(f"✅ Loaded {len(df_1d_2025)} daily candles from 2025")
    print()
    
    # Scenario 1: Gap Up Continuation (75% WR)
    print("=" * 80)
    print("📈 SCENARIO 1: Gap Up Continuation (75% Win Rate)")
    print("=" * 80)
    print()
    print("Condition: Gap up >0.3% that doesn't fill in first hour")
    print("Signal: BULLISH CONTINUATION (finish higher than open)")
    print()
    
    # Get full dataset for context (need previous day)
    gap_trades_all = analyze_gap_up_continuation(df_1d, df_1h)
    gap_trades_2025 = [t for t in gap_trades_all if t['Date'].startswith('2025')]
    
    if gap_trades_2025:
        print(f"📊 Found {len(gap_trades_2025)} trades in 2025:")
        print()
        df_gap = pd.DataFrame(gap_trades_2025)
        print(df_gap.to_string(index=False))
        print()
        wins = sum(1 for t in gap_trades_2025 if t['Result'] == 'WIN')
        print(f"2025 Performance: {wins}/{len(gap_trades_2025)} = {wins/len(gap_trades_2025)*100:.1f}% Win Rate")
    else:
        print("❌ No Gap Up Continuation trades found in 2025")
    
    print()
    print()
    
    # Scenario 2: Inside Day Expansion (71% WR)
    print("=" * 80)
    print("📈 SCENARIO 2: Inside Day Expansion (71% Win Rate)")
    print("=" * 80)
    print()
    print("Condition: Inside Day (high<prev_high AND low>prev_low)")
    print("Signal: BULLISH EXPANSION when next day breaks inside high")
    print()
    
    # Get full dataset for context
    inside_trades_all = analyze_inside_day_expansion(df_1d)
    inside_trades_2025 = [t for t in inside_trades_all if t['Breakout_Day'].startswith('2025')]
    
    if inside_trades_2025:
        print(f"📊 Found {len(inside_trades_2025)} trades in 2025:")
        print()
        df_inside = pd.DataFrame(inside_trades_2025)
        print(df_inside.to_string(index=False))
        print()
        wins = sum(1 for t in inside_trades_2025 if t['Result'] == 'WIN')
        print(f"2025 Performance: {wins}/{len(inside_trades_2025)} = {wins/len(inside_trades_2025)*100:.1f}% Win Rate")
    else:
        print("❌ No Inside Day Expansion trades found in 2025")
    
    print()
    print("=" * 80)
    print("✅ ANALYSIS COMPLETE")
    print("=" * 80)
    print()
    print("💡 These are the most recent trades from 2025 for the two scenarios")
    print("   with the highest historical win rates (75% and 71%).")
    print()


if __name__ == "__main__":
    main()

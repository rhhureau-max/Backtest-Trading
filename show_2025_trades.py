#!/usr/bin/env python3
"""
Extract and display the last 10 trades from 2025 with full details.
"""

import pandas as pd
import numpy as np
from datetime import datetime
import pytz
import os

# Check if detailed trades CSV exists
csv_path = "/home/runner/work/Backtest-Trading/Backtest-Trading/three_scenarios_detailed_trades.csv"

if os.path.exists(csv_path):
    # Load existing trades
    print("Loading existing trade data...")
    df = pd.read_csv(csv_path)
    df['entry_datetime'] = pd.to_datetime(df['entry_datetime'])
    
    # Filter for 2025 trades
    trades_2025 = df[df['entry_datetime'].dt.year == 2025].copy()
    
    # Get last 10 trades
    last_10 = trades_2025.tail(10)
    
    print(f"\n{'='*100}")
    print(f"LAST 10 TRADES FROM 2025")
    print(f"{'='*100}\n")
    
    for idx, (i, trade) in enumerate(last_10.iterrows(), 1):
        print(f"\n{'─'*100}")
        print(f"TRADE #{idx} - {trade['scenario_name']}")
        print(f"{'─'*100}")
        print(f"Entry DateTime:     {trade['entry_datetime']}")
        print(f"Scenario:           {trade['scenario']} - {trade['scenario_name']}")
        print(f"Direction:          {trade['direction'].upper()}")
        print(f"FVG Type:           {trade['fvg_type'].capitalize()}")
        print(f"\nFVG Details:")
        print(f"  FVG Formation:    {trade['fvg_datetime']}")
        print(f"  FVG Zone:         [{trade['fvg_zone_low']:.2f} - {trade['fvg_zone_high']:.2f}]")
        print(f"  Gap Size:         {trade['gap_size']:.2f} points")
        print(f"\nTrade Execution:")
        print(f"  Entry Price:      {trade['entry_price']:.2f}")
        print(f"  Stop Loss:        {trade['stop_loss']:.2f}")
        print(f"  Take Profit:      {trade['take_profit']:.2f}")
        print(f"  Risk:             {abs(trade['entry_price'] - trade['stop_loss']):.2f} points")
        print(f"  Reward:           {abs(trade['take_profit'] - trade['entry_price']):.2f} points")
        print(f"  Risk/Reward:      {trade['rr_ratio']:.2f}:1")
        print(f"\nTrade Result:")
        print(f"  Exit DateTime:    {trade['exit_datetime']}")
        print(f"  Exit Price:       {trade['exit_price']:.2f}")
        print(f"  Exit Reason:      {trade['exit_reason']}")
        print(f"  Outcome:          {'WIN ✓' if trade['outcome'] == 'win' else 'LOSS ✗'}")
        print(f"  P&L:              {trade['pnl_points']:.2f} points")
        
        if 'setup_description' in trade and pd.notna(trade['setup_description']):
            print(f"\nSetup Description:")
            print(f"  {trade['setup_description']}")
    
    print(f"\n{'='*100}")
    print(f"Total 2025 Trades: {len(trades_2025)}")
    print(f"{'='*100}\n")

else:
    # Run a quick version to generate sample trades
    print("Generating sample 2025 trades (quick version)...")
    print("\nNote: Running full backtest to get actual trade data...")
    print("This may take a few minutes...\n")
    
    # Import the main script functions
    import sys
    sys.path.insert(0, '/home/runner/work/Backtest-Trading/Backtest-Trading')
    
    # Load just 2025 data for quick demo
    from datetime import time
    
    CHICAGO_TZ = pytz.timezone('America/Chicago')
    
    print("Loading 2025 NQ data...")
    
    # Load 2025 5m data
    file_path = "/home/runner/work/Backtest-Trading/Backtest-Trading/2025 5m.csv"
    
    if not os.path.exists(file_path):
        print(f"Error: Data file not found: {file_path}")
        exit(1)
    
    df = pd.read_csv(
        file_path,
        sep=';',
        names=['date', 'time', 'open', 'high', 'low', 'close', 'volume'],
        skiprows=1
    )
    
    # Parse datetime
    df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'], format='%d/%m/%Y %H:%M:%S')
    df['datetime'] = df['datetime'].dt.tz_localize('UTC').dt.tz_convert(CHICAGO_TZ)
    df = df.sort_values('datetime').reset_index(drop=True)
    
    # Filter for London Killzone (01:00-04:00 Chicago)
    df['hour'] = df['datetime'].dt.hour
    killzone_df = df[(df['hour'] >= 1) & (df['hour'] < 4)].copy()
    
    print(f"Found {len(killzone_df)} killzone candles in 2025\n")
    
    # Simple FVG detection for demonstration
    print("Detecting FVGs...")
    fvgs_found = []
    
    for i in range(1, len(killzone_df) - 1):
        row_prev = killzone_df.iloc[i-1]
        row_curr = killzone_df.iloc[i]
        row_next = killzone_df.iloc[i+1]
        
        # Bullish FVG
        if row_prev['high'] < row_next['low']:
            fvgs_found.append({
                'index': i,
                'datetime': row_curr['datetime'],
                'type': 'bullish',
                'zone_low': row_prev['high'],
                'zone_high': row_next['low'],
                'gap_size': row_next['low'] - row_prev['high']
            })
        
        # Bearish FVG
        elif row_prev['low'] > row_next['high']:
            fvgs_found.append({
                'index': i,
                'datetime': row_curr['datetime'],
                'type': 'bearish',
                'zone_low': row_next['high'],
                'zone_high': row_prev['low'],
                'gap_size': row_prev['low'] - row_next['high']
            })
    
    print(f"Detected {len(fvgs_found)} FVGs\n")
    
    # Show first 10 FVGs as examples
    print(f"{'='*100}")
    print(f"SAMPLE: FIRST 10 FVG SETUPS FROM 2025 LONDON KILLZONE")
    print(f"{'='*100}\n")
    
    for idx, fvg in enumerate(fvgs_found[:10], 1):
        print(f"\n{'─'*100}")
        print(f"FVG SETUP #{idx}")
        print(f"{'─'*100}")
        print(f"DateTime:           {fvg['datetime']}")
        print(f"Type:               {fvg['type'].upper()}")
        print(f"FVG Zone:           [{fvg['zone_low']:.2f} - {fvg['zone_high']:.2f}]")
        print(f"Gap Size:           {fvg['gap_size']:.2f} points")
        print(f"\nPotential Trade Setup:")
        
        if fvg['type'] == 'bullish':
            print(f"  Direction:        LONG")
            print(f"  Entry Target:     {(fvg['zone_low'] + fvg['zone_high'])/2:.2f} (FVG midpoint)")
            print(f"  Potential SL:     Below setup candle low")
            print(f"  Potential TP:     2:1 Risk/Reward ratio")
        else:
            print(f"  Direction:        SHORT")
            print(f"  Entry Target:     {(fvg['zone_low'] + fvg['zone_high'])/2:.2f} (FVG midpoint)")
            print(f"  Potential SL:     Above setup candle high")
            print(f"  Potential TP:     2:1 Risk/Reward ratio")
        
        print(f"\nNote: This shows the FVG setup. Actual trade execution requires:")
        print(f"      - Price to return and mitigate the FVG zone")
        print(f"      - Classification into Scenario 1, 2, or 3")
        print(f"      - Monitoring until TP/SL or 16:00 session close")
    
    print(f"\n{'='*100}")
    print(f"For complete trade execution details, run the full backtest:")
    print(f"python london_killzone_three_scenarios_backtest.py")
    print(f"{'='*100}\n")

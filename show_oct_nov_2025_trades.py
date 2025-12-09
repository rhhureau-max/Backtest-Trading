#!/usr/bin/env python3
"""
Extract and display trades from October and November 2025 with full details.
"""

import pandas as pd
import numpy as np
from datetime import datetime, time
import pytz
import os

CHICAGO_TZ = pytz.timezone('America/Chicago')

print("="*100)
print("LOADING 2025 NQ DATA FOR OCTOBER & NOVEMBER")
print("="*100)

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

# Filter for October and November 2025
df['month'] = df['datetime'].dt.month
oct_nov_df = df[(df['month'] == 10) | (df['month'] == 11)].copy()

print(f"Total candles in Oct-Nov 2025: {len(oct_nov_df)}")

# Filter for London Killzone (01:00-04:00 Chicago)
oct_nov_df['hour'] = oct_nov_df['datetime'].dt.hour
killzone_df = oct_nov_df[(oct_nov_df['hour'] >= 1) & (oct_nov_df['hour'] < 4)].copy()

print(f"Killzone candles in Oct-Nov 2025: {len(killzone_df)}")

# Simple FVG detection
print("\nDetecting FVGs in October-November 2025 Killzone...")
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
            'gap_size': row_next['low'] - row_prev['high'],
            'candle_prev_low': row_prev['low'],
            'candle_prev_high': row_prev['high'],
            'candle_curr_open': row_curr['open'],
            'candle_curr_close': row_curr['close'],
            'candle_next_low': row_next['low'],
            'candle_next_high': row_next['high']
        })
    
    # Bearish FVG
    elif row_prev['low'] > row_next['high']:
        fvgs_found.append({
            'index': i,
            'datetime': row_curr['datetime'],
            'type': 'bearish',
            'zone_low': row_next['high'],
            'zone_high': row_prev['low'],
            'gap_size': row_prev['low'] - row_next['high'],
            'candle_prev_low': row_prev['low'],
            'candle_prev_high': row_prev['high'],
            'candle_curr_open': row_curr['open'],
            'candle_curr_close': row_curr['close'],
            'candle_next_low': row_next['low'],
            'candle_next_high': row_next['high']
        })

print(f"Detected {len(fvgs_found)} FVGs in Oct-Nov 2025 Killzone\n")

# Get last 10 FVGs
last_10_fvgs = fvgs_found[-10:] if len(fvgs_found) >= 10 else fvgs_found

print(f"{'='*100}")
print(f"LAST 10 FVG SETUPS FROM OCTOBER-NOVEMBER 2025 LONDON KILLZONE")
print(f"{'='*100}\n")

for idx, fvg in enumerate(last_10_fvgs, 1):
    print(f"\n{'─'*100}")
    print(f"TRADE EXEMPLE #{idx}")
    print(f"{'─'*100}")
    
    # Basic info
    print(f"📅 Date/Heure:        {fvg['datetime'].strftime('%Y-%m-%d %H:%M:%S %Z')}")
    print(f"📊 Type de FVG:       {fvg['type'].upper()}")
    print(f"📏 Zone FVG:          [{fvg['zone_low']:.2f} - {fvg['zone_high']:.2f}]")
    print(f"📐 Taille du Gap:     {fvg['gap_size']:.2f} points")
    
    # FVG formation details
    print(f"\n🔍 Détails de Formation du FVG:")
    print(f"  Bougie n-1 (prev):  Low={fvg['candle_prev_low']:.2f}, High={fvg['candle_prev_high']:.2f}")
    print(f"  Bougie n (curr):    Open={fvg['candle_curr_open']:.2f}, Close={fvg['candle_curr_close']:.2f}")
    print(f"  Bougie n+1 (next):  Low={fvg['candle_next_low']:.2f}, High={fvg['candle_next_high']:.2f}")
    
    # Trade setup
    entry_price = (fvg['zone_low'] + fvg['zone_high']) / 2
    
    print(f"\n💼 Configuration du Trade:")
    print(f"  Direction:          {'LONG (Achat)' if fvg['type'] == 'bullish' else 'SHORT (Vente)'}")
    print(f"  Prix d'Entrée:      {entry_price:.2f} (midpoint du FVG)")
    
    if fvg['type'] == 'bullish':
        stop_loss = fvg['candle_prev_low'] - 1.0  # Below previous candle low
        risk = entry_price - stop_loss
        take_profit = entry_price + (risk * 2.0)  # 2:1 RR
        
        print(f"  Stop Loss:          {stop_loss:.2f} (sous le bas de la bougie n-1)")
        print(f"  Risque:             {risk:.2f} points")
        print(f"  Take Profit:        {take_profit:.2f} (2:1 RR)")
        print(f"  Reward:             {risk * 2.0:.2f} points")
    else:
        stop_loss = fvg['candle_prev_high'] + 1.0  # Above previous candle high
        risk = stop_loss - entry_price
        take_profit = entry_price - (risk * 2.0)  # 2:1 RR
        
        print(f"  Stop Loss:          {stop_loss:.2f} (au-dessus du haut de la bougie n-1)")
        print(f"  Risque:             {risk:.2f} points")
        print(f"  Take Profit:        {take_profit:.2f} (2:1 RR)")
        print(f"  Reward:             {risk * 2.0:.2f} points")
    
    print(f"  Ratio R:R:          2.00:1")
    
    # Scenario classification
    print(f"\n🎯 Classification du Scénario:")
    print(f"  À déterminer par analyse complète:")
    print(f"    - Scénario 1: Liquidity Sweep + FVG (Turtle Soup)")
    print(f"    - Scénario 2: Inverted FVG (IFVG)")
    print(f"    - Scénario 3: Continuation FVG (MSS Simple)")
    
    # Execution process
    print(f"\n📋 Processus d'Exécution:")
    print(f"  1. Détection:      FVG détecté à {fvg['datetime'].strftime('%H:%M:%S')}")
    print(f"  2. Classification: Analyser le contexte des 12 bougies précédentes")
    print(f"  3. Attente:        Surveiller la mitigation de la zone FVG")
    print(f"  4. Entrée:         Si le prix touche {entry_price:.2f}, activer le trade")
    print(f"  5. Gestion:        Surveiller TP ({take_profit:.2f}) et SL ({stop_loss:.2f})")
    print(f"  6. Sortie:         Premier touché entre TP, SL, ou 16:00 Chicago time")

print(f"\n{'='*100}")
print(f"RÉSUMÉ DES {len(last_10_fvgs)} DERNIERS FVG")
print(f"{'='*100}")

bullish_count = sum(1 for fvg in last_10_fvgs if fvg['type'] == 'bullish')
bearish_count = sum(1 for fvg in last_10_fvgs if fvg['type'] == 'bearish')
avg_gap = sum(fvg['gap_size'] for fvg in last_10_fvgs) / len(last_10_fvgs)
min_gap = min(fvg['gap_size'] for fvg in last_10_fvgs)
max_gap = max(fvg['gap_size'] for fvg in last_10_fvgs)

print(f"\nFVG Bullish:        {bullish_count} ({bullish_count/len(last_10_fvgs)*100:.1f}%)")
print(f"FVG Bearish:        {bearish_count} ({bearish_count/len(last_10_fvgs)*100:.1f}%)")
print(f"Gap Moyen:          {avg_gap:.2f} points")
print(f"Gap Minimum:        {min_gap:.2f} points")
print(f"Gap Maximum:        {max_gap:.2f} points")

# Show date range
first_date = last_10_fvgs[0]['datetime'].strftime('%Y-%m-%d')
last_date = last_10_fvgs[-1]['datetime'].strftime('%Y-%m-%d')
print(f"\nPériode couverte:   {first_date} à {last_date}")

print(f"\n{'='*100}")
print(f"Pour le backtest complet avec tous les scénarios:")
print(f"python london_killzone_three_scenarios_backtest.py")
print(f"{'='*100}\n")

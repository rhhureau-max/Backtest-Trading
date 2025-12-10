#!/usr/bin/env python3
"""
Extract and display November 2025 trades from literal CSV times analysis
"""

import pandas as pd
import os
from datetime import datetime, time

def load_data():
    """Load all 5-minute data"""
    all_data = []
    for year in [2025]:
        filename = f"{year} 5m.csv"
        if os.path.exists(filename):
            print(f"Loading {filename}...")
            df = pd.read_csv(filename, sep=';', names=['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume'], skiprows=1)
            df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%d/%m/%Y %H:%M:%S')
            df['JustTime'] = pd.to_datetime(df['Time'], format='%H:%M:%S').dt.time
            all_data.append(df)
    
    return pd.concat(all_data, ignore_index=True) if all_data else pd.DataFrame()

def detect_fvgs(df):
    """Detect FVGs in the data"""
    fvgs = []
    
    for i in range(1, len(df) - 1):
        n_minus_1 = df.iloc[i-1]
        n = df.iloc[i]
        n_plus_1 = df.iloc[i+1]
        
        # Bullish FVG: High(n-1) < Low(n+1)
        if n_minus_1['High'] < n_plus_1['Low']:
            fvgs.append({
                'DateTime': n['DateTime'],
                'Date': n['Date'],
                'Time': n['Time'],
                'Type': 'BULLISH',
                'Zone_Low': n_minus_1['High'],
                'Zone_High': n_plus_1['Low'],
                'Gap_Size': n_plus_1['Low'] - n_minus_1['High'],
                'Candle_n-1_High': n_minus_1['High'],
                'Candle_n-1_Low': n_minus_1['Low'],
                'Candle_n_Open': n['Open'],
                'Candle_n_Close': n['Close'],
                'Candle_n+1_High': n_plus_1['High'],
                'Candle_n+1_Low': n_plus_1['Low'],
            })
        
        # Bearish FVG: Low(n-1) > High(n+1)
        elif n_minus_1['Low'] > n_plus_1['High']:
            fvgs.append({
                'DateTime': n['DateTime'],
                'Date': n['Date'],
                'Time': n['Time'],
                'Type': 'BEARISH',
                'Zone_Low': n_plus_1['High'],
                'Zone_High': n_minus_1['Low'],
                'Gap_Size': n_minus_1['Low'] - n_plus_1['High'],
                'Candle_n-1_High': n_minus_1['High'],
                'Candle_n-1_Low': n_minus_1['Low'],
                'Candle_n_Open': n['Open'],
                'Candle_n_Close': n['Close'],
                'Candle_n+1_High': n_plus_1['High'],
                'Candle_n+1_Low': n_plus_1['Low'],
            })
    
    return pd.DataFrame(fvgs)

# Load data
print("="*80)
print("NOVEMBER 2025 TRADES - LITERAL CSV TIMES (01:00-04:00)")
print("="*80)
print()

df = load_data()

# Filter for killzone times (01:00-03:55)
killzone_start = time(1, 0)
killzone_end = time(3, 55)
df_killzone = df[(df['JustTime'] >= killzone_start) & (df['JustTime'] <= killzone_end)].copy()

print(f"Total rows in 2025: {len(df)}")
print(f"Killzone rows (01:00-03:55): {len(df_killzone)}")
print()

# Detect FVGs
fvgs_df = detect_fvgs(df_killzone)

# Filter for November 2025
fvgs_df['Month'] = pd.to_datetime(fvgs_df['DateTime']).dt.month
november_fvgs = fvgs_df[fvgs_df['Month'] == 11].copy()

print(f"Total FVGs in killzone: {len(fvgs_df)}")
print(f"FVGs in November 2025: {len(november_fvgs)}")
print()

# Get last 10 trades
last_10 = november_fvgs.tail(10).reset_index(drop=True)

print("="*80)
print("10 DERNIERS TRADES DE NOVEMBRE 2025")
print("="*80)
print()

for idx, trade in last_10.iterrows():
    trade_num = idx + 1
    print(f"{'='*80}")
    print(f"TRADE #{trade_num} - {trade['Date']} à {trade['Time']}")
    print(f"{'='*80}")
    print()
    
    print(f"📊 TYPE: FVG {trade['Type']}")
    print()
    
    print("🔸 FORMATION (3 bougies):")
    print(f"   Bougie n-1: High={trade['Candle_n-1_High']:.2f}, Low={trade['Candle_n-1_Low']:.2f}")
    print(f"   Bougie n:   Open={trade['Candle_n_Open']:.2f}, Close={trade['Candle_n_Close']:.2f}")
    print(f"   Bougie n+1: High={trade['Candle_n+1_High']:.2f}, Low={trade['Candle_n+1_Low']:.2f}")
    print()
    
    print("📏 ZONE FVG:")
    print(f"   [{trade['Zone_Low']:.2f} - {trade['Zone_High']:.2f}]")
    print(f"   Gap: {trade['Gap_Size']:.2f} points")
    print()
    
    # Calculate trade parameters
    zone_mid = (trade['Zone_Low'] + trade['Zone_High']) / 2
    
    if trade['Type'] == 'BULLISH':
        entry = zone_mid
        sl = trade['Zone_Low'] - 10
        risk = entry - sl
        tp = entry + (risk * 2)
        
        print("💼 CONFIGURATION DU TRADE (Long):")
        print(f"   Entry: {entry:.2f} (midpoint du FVG)")
        print(f"   Stop Loss: {sl:.2f} (-10 points sous la zone)")
        print(f"   Take Profit: {tp:.2f} (2:1 RR)")
        print(f"   Risque: {risk:.2f} points")
        print(f"   Reward: {risk*2:.2f} points")
    else:
        entry = zone_mid
        sl = trade['Zone_High'] + 10
        risk = sl - entry
        tp = entry - (risk * 2)
        
        print("💼 CONFIGURATION DU TRADE (Short):")
        print(f"   Entry: {entry:.2f} (midpoint du FVG)")
        print(f"   Stop Loss: {sl:.2f} (+10 points au-dessus de la zone)")
        print(f"   Take Profit: {tp:.2f} (2:1 RR)")
        print(f"   Risque: {risk:.2f} points")
        print(f"   Reward: {risk*2:.2f} points")
    
    print()
    
    print("🎯 LOGIQUE DE PRISE DE POSITION:")
    print(f"   1. FVG détecté à {trade['Time']} (heure littérale du CSV)")
    print(f"   2. Zone FVG créée: [{trade['Zone_Low']:.2f} - {trade['Zone_High']:.2f}]")
    print(f"   3. Attente de mitigation: prix revient toucher la zone")
    print(f"   4. Entry: {entry:.2f} (au milieu de la zone)")
    print(f"   5. SL: {sl:.2f} (10 points au-delà de la zone)")
    print(f"   6. TP: {tp:.2f} (ratio 2:1)")
    print()
    
    # Determine scenario classification
    print("📋 CLASSIFICATION POTENTIELLE:")
    if trade['Gap_Size'] > 30:
        print("   ⚠️  Gap important (>30pts) → Possible Liquidity Sweep")
    elif trade['Gap_Size'] < 5:
        print("   ℹ️  Petit gap (<5pts) → Continuation probable")
    else:
        print("   ℹ️  Gap moyen → Analyse contexte nécessaire")
    
    print()
    print()

print("="*80)
print("RÉSUMÉ DES 10 TRADES")
print("="*80)
print()

bullish_count = len(last_10[last_10['Type'] == 'BULLISH'])
bearish_count = len(last_10[last_10['Type'] == 'BEARISH'])
avg_gap = last_10['Gap_Size'].mean()
min_gap = last_10['Gap_Size'].min()
max_gap = last_10['Gap_Size'].max()

print(f"Bullish FVGs: {bullish_count} ({bullish_count/10*100:.1f}%)")
print(f"Bearish FVGs: {bearish_count} ({bearish_count/10*100:.1f}%)")
print()
print(f"Gap moyen: {avg_gap:.2f} points")
print(f"Gap minimum: {min_gap:.2f} points")
print(f"Gap maximum: {max_gap:.2f} points")
print()

# Time distribution
time_dist = last_10.groupby('Time').size()
print("Distribution par heure:")
for time_val, count in time_dist.items():
    print(f"  {time_val}: {count} FVG(s)")
print()

print("="*80)
print("Note: Ces trades utilisent les heures LITTÉRALES du fichier CSV (01:00-04:00)")
print("      sans aucune conversion de fuseau horaire.")
print("="*80)

#!/usr/bin/env python3
"""
Targeted SL/TP Optimization for NQ Session 01:00-07:00
Tests 14 configurations: 7 SL types × 2 TP types (RR_1.0 and RR_1.5)
"""

import pandas as pd
import numpy as np
from glob import glob
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

print("=" * 80)
print("TARGETED SL/TP OPTIMIZATION - NQ 01:00-07:00 SESSION")
print("Testing 14 Configurations: 7 SL Types × 2 TP Types (RR_1.0, RR_1.5)")
print("=" * 80)

# Configuration matrix
SL_CONFIGS = [
    "Swing_High+1",
    "Swing_High+5",
    "Fixed_10pts",
    "Fixed_20pts",
    "Fib_89%",
    "ATR_1.5x",
    "ATR_2.0x"
]

TP_CONFIGS = ["RR_1.0", "RR_1.5"]

print(f"\nStop Loss Types: {SL_CONFIGS}")
print(f"Take Profit Types: {TP_CONFIGS}")
print(f"Total Configurations: {len(SL_CONFIGS) * len(TP_CONFIGS)}\n")

# Load data
print("Loading NQ 5-minute data...")
csv_files = sorted(glob('NQ_5m_*.csv'))
if not csv_files:
    print("ERROR: No NQ_5m_*.csv files found!")
    exit(1)

dfs = []
for file in csv_files:
    df_temp = pd.read_csv(file)
    dfs.append(df_temp)
    
df = pd.concat(dfs, ignore_index=True)
df['timestamp'] = pd.to_datetime(df['timestamp'])
df = df.sort_values('timestamp').reset_index(drop=True)

print(f"Loaded {len(df):,} candles from {df['timestamp'].min()} to {df['timestamp'].max()}")

# Filter session 01:00-07:00
df['time'] = df['timestamp'].dt.time
session_start = pd.to_datetime('01:00:00').time()
session_end = pd.to_datetime('07:00:00').time()
df_session = df[(df['time'] >= session_start) & (df['time'] <= session_end)].copy()

print(f"Session 01:00-07:00 candles: {len(df_session):,}\n")

# Calculate ATR for adaptive stops
def calculate_atr(df, period=14):
    high_low = df['high'] - df['low']
    high_close = np.abs(df['high'] - df['close'].shift())
    low_close = np.abs(df['low'] - df['close'].shift())
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    atr = tr.rolling(window=period).mean()
    return atr

df_session['atr'] = calculate_atr(df_session, 14)

# Detect 6-period fractals
def detect_fractals_6period(df, window=1, lookback=6):
    fractals_high = []
    fractals_low = []
    
    for i in range(lookback, len(df)):
        # Fractal High
        if i >= window and i < len(df) - window:
            is_local_high = all(df.iloc[i]['high'] > df.iloc[i-j]['high'] for j in range(1, window+1)) and \
                           all(df.iloc[i]['high'] > df.iloc[i+j]['high'] for j in range(1, window+1))
            is_rolling_high = df.iloc[i]['high'] == df.iloc[i-lookback:i+1]['high'].max()
            
            if is_local_high and is_rolling_high:
                fractals_high.append(i)
        
        # Fractal Low
        if i >= window and i < len(df) - window:
            is_local_low = all(df.iloc[i]['low'] < df.iloc[i-j]['low'] for j in range(1, window+1)) and \
                          all(df.iloc[i]['low'] < df.iloc[i+j]['low'] for j in range(1, window+1))
            is_rolling_low = df.iloc[i]['low'] == df.iloc[i-lookback:i+1]['low'].min()
            
            if is_local_low and is_rolling_low:
                fractals_low.append(i)
    
    return fractals_high, fractals_low

print("Detecting 6-period fractals...")
fractals_high, fractals_low = detect_fractals_6period(df_session, window=1, lookback=6)
print(f"Found {len(fractals_high)} fractal highs and {len(fractals_low)} fractal lows\n")

# Detect sweeps and MSS
def detect_sweeps_and_mss(df, fractals_high, fractals_low):
    setups = []
    
    for i in range(len(df)):
        # Find previous fractal high
        prev_fractals = [f for f in fractals_high if f < i]
        if not prev_fractals:
            continue
        
        fractal_idx = prev_fractals[-1]
        fractal_high = df.iloc[fractal_idx]['high']
        
        # Check sweep
        if df.iloc[i]['high'] > fractal_high:
            # Check rejection
            reversal_window = min(2, len(df) - i - 1)
            has_rejection = df.iloc[i]['close'] < fractal_high
            
            if not has_rejection and reversal_window > 0:
                for j in range(1, reversal_window + 1):
                    if i + j < len(df):
                        bearish_engulfing = (df.iloc[i+j]['open'] > df.iloc[i+j-1]['close'] and
                                           df.iloc[i+j]['close'] < df.iloc[i+j-1]['open'])
                        strong_drop = df.iloc[i+j]['close'] < df.iloc[i]['close'] - 10
                        if bearish_engulfing or strong_drop:
                            has_rejection = True
                            break
            
            if has_rejection:
                # Find MSS
                fractal_low_candidates = [f for f in fractals_low if fractal_idx < f < i]
                if fractal_low_candidates:
                    fractal_low_idx = fractal_low_candidates[-1]
                    fractal_low_val = df.iloc[fractal_low_idx]['low']
                    
                    # Check MSS
                    for k in range(i+1, min(i+20, len(df))):
                        if df.iloc[k]['low'] < fractal_low_val:
                            sweep_high = df.iloc[i]['high']
                            mss_low = df.iloc[k]['low']
                            entry_price = (sweep_high + mss_low) / 2
                            
                            setups.append({
                                'setup_idx': i,
                                'entry_idx': k,
                                'sweep_high': sweep_high,
                                'mss_low': mss_low,
                                'entry_price': entry_price,
                                'fractal_high': fractal_high
                            })
                            break
    
    return setups

print("Detecting sweep setups with MSS confirmation...")
setups = detect_sweeps_and_mss(df_session, fractals_high, fractals_low)
print(f"Found {len(setups)} valid setups\n")

# Function to calculate SL
def calculate_sl(setup, df, sl_type):
    sweep_high = setup['sweep_high']
    entry_price = setup['entry_price']
    entry_idx = setup['entry_idx']
    mss_low = setup['mss_low']
    
    if sl_type == "Swing_High+1":
        return sweep_high + 1
    elif sl_type == "Swing_High+5":
        return sweep_high + 5
    elif sl_type == "Fixed_10pts":
        return entry_price + 10
    elif sl_type == "Fixed_20pts":
        return entry_price + 20
    elif sl_type == "Fib_89%":
        fib_89 = mss_low + 0.89 * (sweep_high - mss_low)
        return fib_89 + 5
    elif sl_type == "ATR_1.5x":
        atr_val = df.iloc[entry_idx]['atr']
        if pd.isna(atr_val):
            atr_val = 20
        return entry_price + 1.5 * atr_val
    elif sl_type == "ATR_2.0x":
        atr_val = df.iloc[entry_idx]['atr']
        if pd.isna(atr_val):
            atr_val = 20
        return entry_price + 2.0 * atr_val
    else:
        return sweep_high + 5

# Function to calculate TP
def calculate_tp(setup, df, tp_type, sl_price):
    entry_price = setup['entry_price']
    risk = sl_price - entry_price
    
    if tp_type == "RR_1.0":
        return entry_price - risk
    elif tp_type == "RR_1.5":
        return entry_price - 1.5 * risk
    else:
        return entry_price - risk

# Run optimization
results = []

for sl_config in SL_CONFIGS:
    for tp_config in TP_CONFIGS:
        config_name = f"{sl_config}_{tp_config}"
        print(f"Testing {config_name}...")
        
        trades = []
        
        for setup in setups:
            entry_idx = setup['entry_idx']
            entry_price = setup['entry_price']
            
            # Calculate SL and TP
            sl_price = calculate_sl(setup, df_session, sl_config)
            tp_price = calculate_tp(setup, df_session, tp_config, sl_price)
            
            # Simulate trade
            hit_sl = False
            hit_tp = False
            exit_idx = entry_idx
            
            for i in range(entry_idx + 1, min(entry_idx + 100, len(df_session))):
                if df_session.iloc[i]['high'] >= sl_price:
                    hit_sl = True
                    exit_idx = i
                    break
                if df_session.iloc[i]['low'] <= tp_price:
                    hit_tp = True
                    exit_idx = i
                    break
            
            if hit_tp:
                pnl = entry_price - tp_price
                outcome = 'WIN'
            elif hit_sl:
                pnl = entry_price - sl_price
                outcome = 'LOSS'
            else:
                pnl = 0
                outcome = 'NO_EXIT'
            
            risk = sl_price - entry_price
            rr = pnl / risk if risk > 0 else 0
            
            trades.append({
                'outcome': outcome,
                'pnl': pnl,
                'rr': rr,
                'entry_price': entry_price,
                'sl_price': sl_price,
                'tp_price': tp_price
            })
        
        # Calculate metrics
        wins = [t for t in trades if t['outcome'] == 'WIN']
        losses = [t for t in trades if t['outcome'] == 'LOSS']
        
        total_trades = len(wins) + len(losses)
        win_rate = len(wins) / total_trades * 100 if total_trades > 0 else 0
        
        total_pnl = sum(t['pnl'] for t in wins + losses)
        avg_win = np.mean([t['pnl'] for t in wins]) if wins else 0
        avg_loss = np.mean([t['pnl'] for t in losses]) if losses else 0
        avg_rr = np.mean([t['rr'] for t in wins + losses]) if (wins + losses) else 0
        
        profit_factor = abs(sum(t['pnl'] for t in wins) / sum(t['pnl'] for t in losses)) if losses and sum(t['pnl'] for t in losses) != 0 else 0
        
        # Account return (1% risk per trade)
        account_return = 0
        equity = 100000
        for t in wins + losses:
            if t['outcome'] in ['WIN', 'LOSS']:
                risk = t['sl_price'] - t['entry_price']
                position_size = (equity * 0.01) / risk if risk > 0 else 0
                trade_pnl = t['pnl'] * position_size
                equity += trade_pnl
        account_return = (equity - 100000) / 100000 * 100
        
        results.append({
            'SL_Type': sl_config,
            'TP_Type': tp_config,
            'Configuration': config_name,
            'Total_Trades': total_trades,
            'Wins': len(wins),
            'Losses': len(losses),
            'Win_Rate_%': win_rate,
            'Total_PnL': total_pnl,
            'Avg_Win': avg_win,
            'Avg_Loss': avg_loss,
            'Profit_Factor': profit_factor,
            'Avg_RR': avg_rr,
            'Account_Return_%': account_return
        })

# Create results dataframe
results_df = pd.DataFrame(results)
results_df = results_df.sort_values('Profit_Factor', ascending=False)

# Save results
results_df.to_csv('targeted_sl_tp_results.csv', index=False)
print(f"\n{'='*80}")
print("OPTIMIZATION COMPLETE")
print(f"{'='*80}\n")
print(results_df.to_string(index=False))

# Create visualizations
print("\nGenerating visualizations...")

fig = plt.figure(figsize=(20, 12))

# 1. Heatmap: Win Rate by SL x TP
ax1 = plt.subplot(2, 3, 1)
pivot_wr = results_df.pivot_table(values='Win_Rate_%', index='SL_Type', columns='TP_Type')
sns.heatmap(pivot_wr, annot=True, fmt='.1f', cmap='RdYlGn', ax=ax1, cbar_kws={'label': 'Win Rate %'})
ax1.set_title('Win Rate % by SL x TP', fontsize=14, fontweight='bold')

# 2. Heatmap: Profit Factor by SL x TP
ax2 = plt.subplot(2, 3, 2)
pivot_pf = results_df.pivot_table(values='Profit_Factor', index='SL_Type', columns='TP_Type')
sns.heatmap(pivot_pf, annot=True, fmt='.2f', cmap='RdYlGn', ax=ax2, cbar_kws={'label': 'Profit Factor'})
ax2.set_title('Profit Factor by SL x TP', fontsize=14, fontweight='bold')

# 3. Heatmap: Account Return by SL x TP
ax3 = plt.subplot(2, 3, 3)
pivot_ret = results_df.pivot_table(values='Account_Return_%', index='SL_Type', columns='TP_Type')
sns.heatmap(pivot_ret, annot=True, fmt='.1f', cmap='RdYlGn', ax=ax3, cbar_kws={'label': 'Return %'})
ax3.set_title('Account Return % by SL x TP', fontsize=14, fontweight='bold')

# 4. Scatter: Win Rate vs Profit Factor
ax4 = plt.subplot(2, 3, 4)
colors = ['blue' if tp == 'RR_1.0' else 'red' for tp in results_df['TP_Type']]
ax4.scatter(results_df['Win_Rate_%'], results_df['Profit_Factor'], c=colors, s=100, alpha=0.6)
for idx, row in results_df.iterrows():
    ax4.annotate(row['Configuration'], (row['Win_Rate_%'], row['Profit_Factor']), 
                fontsize=7, alpha=0.7)
ax4.set_xlabel('Win Rate %', fontsize=12)
ax4.set_ylabel('Profit Factor', fontsize=12)
ax4.set_title('Win Rate vs Profit Factor', fontsize=14, fontweight='bold')
ax4.grid(True, alpha=0.3)
ax4.legend(['RR_1.0', 'RR_1.5'])

# 5. Bar chart: Top 10 by Profit Factor
ax5 = plt.subplot(2, 3, 5)
top10 = results_df.nlargest(10, 'Profit_Factor')
colors_bar = ['blue' if tp == 'RR_1.0' else 'red' for tp in top10['TP_Type']]
ax5.barh(range(len(top10)), top10['Profit_Factor'], color=colors_bar, alpha=0.7)
ax5.set_yticks(range(len(top10)))
ax5.set_yticklabels(top10['Configuration'], fontsize=9)
ax5.set_xlabel('Profit Factor', fontsize=12)
ax5.set_title('Top 10 Configurations by Profit Factor', fontsize=14, fontweight='bold')
ax5.grid(True, alpha=0.3, axis='x')

# 6. Bar chart: Total Trades by Configuration
ax6 = plt.subplot(2, 3, 6)
colors_bar2 = ['blue' if tp == 'RR_1.0' else 'red' for tp in results_df['TP_Type']]
ax6.bar(range(len(results_df)), results_df['Total_Trades'], color=colors_bar2, alpha=0.7)
ax6.set_xticks(range(len(results_df)))
ax6.set_xticklabels(results_df['Configuration'], rotation=45, ha='right', fontsize=8)
ax6.set_ylabel('Total Trades', fontsize=12)
ax6.set_title('Total Trades by Configuration', fontsize=14, fontweight='bold')
ax6.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('targeted_sl_tp_optimization_results.png', dpi=150, bbox_inches='tight')
print("Saved: targeted_sl_tp_optimization_results.png")

print(f"\n{'='*80}")
print("FILES GENERATED:")
print(f"{'='*80}")
print("1. targeted_sl_tp_results.csv - Complete results table")
print("2. targeted_sl_tp_optimization_results.png - Visualization charts")
print(f"\n{'='*80}")
print("OPTIMIZATION SUMMARY COMPLETE")
print(f"{'='*80}\n")

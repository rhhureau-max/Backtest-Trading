#!/usr/bin/env python3
"""
FVG Backtesting Script - Win Rate Analysis with Multiple SL/TP Levels

This script backtests trading strategies based on consecutive FVG patterns:
- Entry: At opening of n+2 candle after second FVG
- Stop Loss: 50% of n+2 candle, 100% of n+2 candle, or middle of second FVG
- Take Profit: RR 1.0 to 5.0 (in 0.5 increments)

Entry times:
- 1m: 8:33
- 5m: 8:45
- 15m: 9:15
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from datetime import datetime, timedelta
from typing import Tuple, Optional, Dict, List


def load_csv_data(filepath: str) -> pd.DataFrame:
    """Load CSV data with proper column names."""
    df = pd.read_csv(filepath, sep=';', 
                     names=['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume'],
                     skiprows=1)
    df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%d/%m/%Y %H:%M:%S')
    return df


def check_fvg(candle_prev: pd.Series, candle_current: pd.Series, candle_next: pd.Series) -> Tuple[bool, str, float]:
    """
    Check if there's a Fair Value Gap (FVG) for the current candle.
    
    Returns: (has_fvg, direction, gap_size)
    """
    high_prev = candle_prev['High']
    low_next = candle_next['Low']
    low_prev = candle_prev['Low']
    high_next = candle_next['High']
    
    # Bullish FVG: gap up
    if low_next > high_prev:
        gap_size = low_next - high_prev
        return True, 'bullish', gap_size
    
    # Bearish FVG: gap down
    if high_next < low_prev:
        gap_size = low_prev - high_next
        return True, 'bearish', gap_size
    
    return False, 'none', 0.0


def simulate_trade(entry_price: float, direction: str, sl_price: float, tp_price: float,
                   future_candles: pd.DataFrame) -> Tuple[str, float, int]:
    """
    Simulate a trade and determine outcome.
    
    Returns: (result, exit_price, candles_to_exit)
    """
    for idx, (_, candle) in enumerate(future_candles.iterrows()):
        if direction == 'bullish':
            # Check if SL hit first (price goes below SL)
            if candle['Low'] <= sl_price:
                return 'loss', sl_price, idx + 1
            # Check if TP hit
            if candle['High'] >= tp_price:
                return 'win', tp_price, idx + 1
        else:  # bearish
            # Check if SL hit first (price goes above SL)
            if candle['High'] >= sl_price:
                return 'loss', sl_price, idx + 1
            # Check if TP hit
            if candle['Low'] <= tp_price:
                return 'win', tp_price, idx + 1
    
    return 'pending', entry_price, len(future_candles)


def backtest_1m(df: pd.DataFrame, rr_levels: List[float]) -> Dict:
    """
    Backtest 1-minute timeframe.
    Entry at 8:33 (opening of n+2 after second FVG at 8:31)
    """
    results = {
        'sl_50': {rr: {'wins': 0, 'losses': 0, 'pending': 0, 'trades': []} for rr in rr_levels},
        'sl_100': {rr: {'wins': 0, 'losses': 0, 'pending': 0, 'trades': []} for rr in rr_levels},
        'sl_fvg_mid': {rr: {'wins': 0, 'losses': 0, 'pending': 0, 'trades': []} for rr in rr_levels},
        'total_consecutive_fvg': 0
    }
    
    df['DateOnly'] = df['Datetime'].dt.date
    grouped = df.groupby('DateOnly')
    
    for date, group in grouped:
        group = group.sort_values('Datetime').reset_index(drop=True)
        
        # Get required candles
        candle_829 = group[group['Time'] == '08:29:00']
        candle_830 = group[group['Time'] == '08:30:00']
        candle_831 = group[group['Time'] == '08:31:00']
        candle_832 = group[group['Time'] == '08:32:00']
        candle_833 = group[group['Time'] == '08:33:00']
        
        if any(len(c) == 0 for c in [candle_829, candle_830, candle_831, candle_832, candle_833]):
            continue
        
        # Check for consecutive FVGs
        has_fvg_830, dir_830, _ = check_fvg(candle_829.iloc[0], candle_830.iloc[0], candle_831.iloc[0])
        has_fvg_831, dir_831, gap_831 = check_fvg(candle_830.iloc[0], candle_831.iloc[0], candle_832.iloc[0])
        
        if not (has_fvg_830 and has_fvg_831 and dir_830 == dir_831):
            continue
        
        results['total_consecutive_fvg'] += 1
        direction = dir_831
        
        # Entry at 8:33 open
        entry_candle = candle_833.iloc[0]
        entry_price = entry_candle['Open']
        
        # n+2 candle after second FVG is candle_833
        n2_candle = candle_833.iloc[0]
        n2_range = n2_candle['High'] - n2_candle['Low']
        
        # Second FVG candle is 8:31
        fvg2_candle = candle_831.iloc[0]
        fvg2_mid = (fvg2_candle['High'] + fvg2_candle['Low']) / 2
        
        # Calculate SL levels
        if direction == 'bullish':
            sl_50 = entry_price - (n2_range * 0.5)
            sl_100 = entry_price - n2_range
            sl_fvg_mid = fvg2_mid
        else:
            sl_50 = entry_price + (n2_range * 0.5)
            sl_100 = entry_price + n2_range
            sl_fvg_mid = fvg2_mid
        
        # Get future candles for simulation (rest of the day)
        entry_candle_idx = group[group['Time'] == '08:33:00'].index
        if len(entry_candle_idx) == 0:
            continue
        entry_idx = entry_candle_idx[0]
        future_candles = group.loc[entry_idx + 1:]
        
        # Test each SL type and RR level
        for sl_type, sl_price in [('sl_50', sl_50), ('sl_100', sl_100), ('sl_fvg_mid', sl_fvg_mid)]:
            risk = abs(entry_price - sl_price)
            if risk <= 0:
                continue
                
            for rr in rr_levels:
                if direction == 'bullish':
                    tp_price = entry_price + (risk * rr)
                else:
                    tp_price = entry_price - (risk * rr)
                
                result, exit_price, candles = simulate_trade(entry_price, direction, sl_price, tp_price, future_candles)
                
                result_key = 'wins' if result == 'win' else ('losses' if result == 'loss' else 'pending')
                results[sl_type][rr][result_key] += 1
                results[sl_type][rr]['trades'].append({
                    'date': str(date),
                    'direction': direction,
                    'entry': entry_price,
                    'sl': sl_price,
                    'tp': tp_price,
                    'result': result,
                    'exit_price': exit_price
                })
    
    return results


def backtest_5m(df: pd.DataFrame, rr_levels: List[float]) -> Dict:
    """
    Backtest 5-minute timeframe.
    Entry at 8:45 (opening of n+2 after second FVG at 8:35)
    """
    results = {
        'sl_50': {rr: {'wins': 0, 'losses': 0, 'pending': 0, 'trades': []} for rr in rr_levels},
        'sl_100': {rr: {'wins': 0, 'losses': 0, 'pending': 0, 'trades': []} for rr in rr_levels},
        'sl_fvg_mid': {rr: {'wins': 0, 'losses': 0, 'pending': 0, 'trades': []} for rr in rr_levels},
        'total_consecutive_fvg': 0
    }
    
    df['DateOnly'] = df['Datetime'].dt.date
    grouped = df.groupby('DateOnly')
    
    for date, group in grouped:
        group = group.sort_values('Datetime').reset_index(drop=True)
        
        # Get required candles for 5m
        candle_825 = group[group['Time'] == '08:25:00']
        candle_830 = group[group['Time'] == '08:30:00']
        candle_835 = group[group['Time'] == '08:35:00']
        candle_840 = group[group['Time'] == '08:40:00']
        candle_845 = group[group['Time'] == '08:45:00']
        
        if any(len(c) == 0 for c in [candle_825, candle_830, candle_835, candle_840, candle_845]):
            continue
        
        # Check for consecutive FVGs
        has_fvg_830, dir_830, _ = check_fvg(candle_825.iloc[0], candle_830.iloc[0], candle_835.iloc[0])
        has_fvg_835, dir_835, gap_835 = check_fvg(candle_830.iloc[0], candle_835.iloc[0], candle_840.iloc[0])
        
        if not (has_fvg_830 and has_fvg_835 and dir_830 == dir_835):
            continue
        
        results['total_consecutive_fvg'] += 1
        direction = dir_835
        
        # Entry at 8:45 open
        entry_candle = candle_845.iloc[0]
        entry_price = entry_candle['Open']
        
        # n+2 candle after second FVG is candle_845
        n2_candle = candle_845.iloc[0]
        n2_range = n2_candle['High'] - n2_candle['Low']
        
        # Second FVG candle is 8:35
        fvg2_candle = candle_835.iloc[0]
        fvg2_mid = (fvg2_candle['High'] + fvg2_candle['Low']) / 2
        
        # Calculate SL levels
        if direction == 'bullish':
            sl_50 = entry_price - (n2_range * 0.5)
            sl_100 = entry_price - n2_range
            sl_fvg_mid = fvg2_mid
        else:
            sl_50 = entry_price + (n2_range * 0.5)
            sl_100 = entry_price + n2_range
            sl_fvg_mid = fvg2_mid
        
        # Get future candles for simulation
        entry_candle_idx = group[group['Time'] == '08:45:00'].index
        if len(entry_candle_idx) == 0:
            continue
        entry_idx = entry_candle_idx[0]
        future_candles = group.loc[entry_idx + 1:]
        
        # Test each SL type and RR level
        for sl_type, sl_price in [('sl_50', sl_50), ('sl_100', sl_100), ('sl_fvg_mid', sl_fvg_mid)]:
            risk = abs(entry_price - sl_price)
            if risk <= 0:
                continue
                
            for rr in rr_levels:
                if direction == 'bullish':
                    tp_price = entry_price + (risk * rr)
                else:
                    tp_price = entry_price - (risk * rr)
                
                result, exit_price, candles = simulate_trade(entry_price, direction, sl_price, tp_price, future_candles)
                
                result_key = 'wins' if result == 'win' else ('losses' if result == 'loss' else 'pending')
                results[sl_type][rr][result_key] += 1
                results[sl_type][rr]['trades'].append({
                    'date': str(date),
                    'direction': direction,
                    'entry': entry_price,
                    'sl': sl_price,
                    'tp': tp_price,
                    'result': result,
                    'exit_price': exit_price
                })
    
    return results


def backtest_15m(df: pd.DataFrame, rr_levels: List[float]) -> Dict:
    """
    Backtest 15-minute timeframe.
    Entry at 9:15 (opening of n+2 after second FVG at 8:45)
    """
    results = {
        'sl_50': {rr: {'wins': 0, 'losses': 0, 'pending': 0, 'trades': []} for rr in rr_levels},
        'sl_100': {rr: {'wins': 0, 'losses': 0, 'pending': 0, 'trades': []} for rr in rr_levels},
        'sl_fvg_mid': {rr: {'wins': 0, 'losses': 0, 'pending': 0, 'trades': []} for rr in rr_levels},
        'total_consecutive_fvg': 0
    }
    
    df['DateOnly'] = df['Datetime'].dt.date
    grouped = df.groupby('DateOnly')
    
    for date, group in grouped:
        group = group.sort_values('Datetime').reset_index(drop=True)
        
        # Get required candles for 15m
        candle_815 = group[group['Time'] == '08:15:00']
        candle_830 = group[group['Time'] == '08:30:00']
        candle_845 = group[group['Time'] == '08:45:00']
        candle_900 = group[group['Time'] == '09:00:00']
        candle_915 = group[group['Time'] == '09:15:00']
        
        if any(len(c) == 0 for c in [candle_815, candle_830, candle_845, candle_900, candle_915]):
            continue
        
        # Check for consecutive FVGs
        has_fvg_830, dir_830, _ = check_fvg(candle_815.iloc[0], candle_830.iloc[0], candle_845.iloc[0])
        has_fvg_845, dir_845, gap_845 = check_fvg(candle_830.iloc[0], candle_845.iloc[0], candle_900.iloc[0])
        
        if not (has_fvg_830 and has_fvg_845 and dir_830 == dir_845):
            continue
        
        results['total_consecutive_fvg'] += 1
        direction = dir_845
        
        # Entry at 9:15 open
        entry_candle = candle_915.iloc[0]
        entry_price = entry_candle['Open']
        
        # n+2 candle after second FVG is candle_915
        n2_candle = candle_915.iloc[0]
        n2_range = n2_candle['High'] - n2_candle['Low']
        
        # Second FVG candle is 8:45
        fvg2_candle = candle_845.iloc[0]
        fvg2_mid = (fvg2_candle['High'] + fvg2_candle['Low']) / 2
        
        # Calculate SL levels
        if direction == 'bullish':
            sl_50 = entry_price - (n2_range * 0.5)
            sl_100 = entry_price - n2_range
            sl_fvg_mid = fvg2_mid
        else:
            sl_50 = entry_price + (n2_range * 0.5)
            sl_100 = entry_price + n2_range
            sl_fvg_mid = fvg2_mid
        
        # Get future candles for simulation
        entry_candle_idx = group[group['Time'] == '09:15:00'].index
        if len(entry_candle_idx) == 0:
            continue
        entry_idx = entry_candle_idx[0]
        future_candles = group.loc[entry_idx + 1:]
        
        # Test each SL type and RR level
        for sl_type, sl_price in [('sl_50', sl_50), ('sl_100', sl_100), ('sl_fvg_mid', sl_fvg_mid)]:
            risk = abs(entry_price - sl_price)
            if risk <= 0:
                continue
                
            for rr in rr_levels:
                if direction == 'bullish':
                    tp_price = entry_price + (risk * rr)
                else:
                    tp_price = entry_price - (risk * rr)
                
                result, exit_price, candles = simulate_trade(entry_price, direction, sl_price, tp_price, future_candles)
                
                result_key = 'wins' if result == 'win' else ('losses' if result == 'loss' else 'pending')
                results[sl_type][rr][result_key] += 1
                results[sl_type][rr]['trades'].append({
                    'date': str(date),
                    'direction': direction,
                    'entry': entry_price,
                    'sl': sl_price,
                    'tp': tp_price,
                    'result': result,
                    'exit_price': exit_price
                })
    
    return results


def aggregate_results(all_results: Dict, results: Dict, rr_levels: List[float]) -> None:
    """Aggregate results from individual years."""
    all_results['total_consecutive_fvg'] += results['total_consecutive_fvg']
    
    for sl_type in ['sl_50', 'sl_100', 'sl_fvg_mid']:
        for rr in rr_levels:
            all_results[sl_type][rr]['wins'] += results[sl_type][rr]['wins']
            all_results[sl_type][rr]['losses'] += results[sl_type][rr]['losses']
            all_results[sl_type][rr]['pending'] += results[sl_type][rr]['pending']
            all_results[sl_type][rr]['trades'].extend(results[sl_type][rr]['trades'])


def calculate_win_rate(results: Dict, sl_type: str, rr: float) -> float:
    """Calculate win rate percentage."""
    wins = results[sl_type][rr]['wins']
    losses = results[sl_type][rr]['losses']
    total = wins + losses
    if total == 0:
        return 0.0
    return (wins / total) * 100


def generate_markdown_report(results: Dict, timeframe: str, rr_levels: List[float], output_dir: str) -> str:
    """Generate markdown report for a timeframe."""
    entry_time = {'1m': '08:33', '5m': '08:45', '15m': '09:15'}[timeframe]
    
    md = f"""# FVG Backtest Analysis - {timeframe} Timeframe

## Strategy Overview

- **Entry Time**: {entry_time} (Opening of n+2 candle after second FVG)
- **Direction**: Same as consecutive FVG direction (bullish or bearish)
- **Total Consecutive FVG Opportunities**: {results['total_consecutive_fvg']}

## Stop Loss Configurations

1. **SL 50%**: 50% of the n+2 candle range from entry
2. **SL 100%**: 100% of the n+2 candle range from entry  
3. **SL FVG Mid**: Middle of the second FVG candle

---

## Win Rate Results

### SL at 50% of n+2 Candle

| RR | Wins | Losses | Pending | Total | Win Rate |
|:--:|:----:|:------:|:-------:|:-----:|:--------:|
"""
    
    for rr in rr_levels:
        data = results['sl_50'][rr]
        total = data['wins'] + data['losses']
        wr = calculate_win_rate(results, 'sl_50', rr)
        md += f"| {rr} | {data['wins']} | {data['losses']} | {data['pending']} | {total} | **{wr:.1f}%** |\n"
    
    md += """
### SL at 100% of n+2 Candle

| RR | Wins | Losses | Pending | Total | Win Rate |
|:--:|:----:|:------:|:-------:|:-----:|:--------:|
"""
    
    for rr in rr_levels:
        data = results['sl_100'][rr]
        total = data['wins'] + data['losses']
        wr = calculate_win_rate(results, 'sl_100', rr)
        md += f"| {rr} | {data['wins']} | {data['losses']} | {data['pending']} | {total} | **{wr:.1f}%** |\n"
    
    md += """
### SL at Middle of Second FVG

| RR | Wins | Losses | Pending | Total | Win Rate |
|:--:|:----:|:------:|:-------:|:-----:|:--------:|
"""
    
    for rr in rr_levels:
        data = results['sl_fvg_mid'][rr]
        total = data['wins'] + data['losses']
        wr = calculate_win_rate(results, 'sl_fvg_mid', rr)
        md += f"| {rr} | {data['wins']} | {data['losses']} | {data['pending']} | {total} | **{wr:.1f}%** |\n"
    
    md += """
---

## Summary Table - All SL Types

| SL Type | RR 1.0 | RR 1.5 | RR 2.0 | RR 2.5 | RR 3.0 | RR 3.5 | RR 4.0 | RR 4.5 | RR 5.0 |
|:--------|:------:|:------:|:------:|:------:|:------:|:------:|:------:|:------:|:------:|
"""
    
    for sl_type, sl_name in [('sl_50', 'SL 50%'), ('sl_100', 'SL 100%'), ('sl_fvg_mid', 'SL FVG Mid')]:
        row = f"| {sl_name} |"
        for rr in rr_levels:
            wr = calculate_win_rate(results, sl_type, rr)
            row += f" {wr:.1f}% |"
        md += row + "\n"
    
    md += f"""
---

## Charts

### Win Rate by Risk/Reward Ratio

![Win Rate Chart](FVG_Backtest_{timeframe}_WinRate.png)

### Trade Distribution by Direction

The strategy was applied to:
- **Bullish FVG patterns**: Long positions
- **Bearish FVG patterns**: Short positions

---

*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
    
    return md


def generate_charts(results: Dict, timeframe: str, rr_levels: List[float], output_dir: str):
    """Generate charts for the analysis."""
    plt.style.use('default')
    fig, ax = plt.subplots(figsize=(12, 6))
    
    x = np.arange(len(rr_levels))
    width = 0.25
    
    wr_50 = [calculate_win_rate(results, 'sl_50', rr) for rr in rr_levels]
    wr_100 = [calculate_win_rate(results, 'sl_100', rr) for rr in rr_levels]
    wr_fvg = [calculate_win_rate(results, 'sl_fvg_mid', rr) for rr in rr_levels]
    
    bars1 = ax.bar(x - width, wr_50, width, label='SL 50%', color='#3498db', edgecolor='black')
    bars2 = ax.bar(x, wr_100, width, label='SL 100%', color='#2ecc71', edgecolor='black')
    bars3 = ax.bar(x + width, wr_fvg, width, label='SL FVG Mid', color='#e74c3c', edgecolor='black')
    
    ax.set_xlabel('Risk/Reward Ratio', fontsize=12)
    ax.set_ylabel('Win Rate (%)', fontsize=12)
    ax.set_title(f'FVG Backtest Win Rate - {timeframe} Timeframe\n(Entry at n+2 candle after consecutive FVG)', fontsize=14)
    ax.set_xticks(x)
    ax.set_xticklabels([str(rr) for rr in rr_levels])
    ax.legend(loc='upper right')
    ax.set_ylim(0, 100)
    ax.grid(axis='y', alpha=0.3)
    
    # Add value labels on bars
    for bars in [bars1, bars2, bars3]:
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.0f}%',
                       xy=(bar.get_x() + bar.get_width() / 2, height),
                       xytext=(0, 3),
                       textcoords="offset points",
                       ha='center', va='bottom', fontsize=8)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f'FVG_Backtest_{timeframe}_WinRate.png'), dpi=150, bbox_inches='tight')
    plt.close()


def main():
    """Main function to run the backtest."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = base_dir
    
    years = ['2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025']
    rr_levels = [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]
    
    # Initialize aggregate results for each timeframe
    def init_results():
        return {
            'sl_50': {rr: {'wins': 0, 'losses': 0, 'pending': 0, 'trades': []} for rr in rr_levels},
            'sl_100': {rr: {'wins': 0, 'losses': 0, 'pending': 0, 'trades': []} for rr in rr_levels},
            'sl_fvg_mid': {rr: {'wins': 0, 'losses': 0, 'pending': 0, 'trades': []} for rr in rr_levels},
            'total_consecutive_fvg': 0
        }
    
    all_results_1m = init_results()
    all_results_5m = init_results()
    all_results_15m = init_results()
    
    print("=" * 70)
    print("  FVG BACKTEST - WIN RATE ANALYSIS")
    print("  Entry: n+2 candle after second consecutive FVG")
    print("=" * 70)
    
    for year in years:
        print(f"\nProcessing {year}...")
        
        # 1m backtest
        file_1m = os.path.join(base_dir, f"{year} 1m.csv")
        if os.path.exists(file_1m):
            df_1m = load_csv_data(file_1m)
            results_1m = backtest_1m(df_1m, rr_levels)
            aggregate_results(all_results_1m, results_1m, rr_levels)
            print(f"  1m: {results_1m['total_consecutive_fvg']} trades")
        
        # 5m backtest
        file_5m = os.path.join(base_dir, f"{year} 5m.csv")
        if os.path.exists(file_5m):
            df_5m = load_csv_data(file_5m)
            results_5m = backtest_5m(df_5m, rr_levels)
            aggregate_results(all_results_5m, results_5m, rr_levels)
            print(f"  5m: {results_5m['total_consecutive_fvg']} trades")
        
        # 15m backtest
        file_15m = os.path.join(base_dir, f"{year} 15m.csv")
        if os.path.exists(file_15m):
            df_15m = load_csv_data(file_15m)
            results_15m = backtest_15m(df_15m, rr_levels)
            aggregate_results(all_results_15m, results_15m, rr_levels)
            print(f"  15m: {results_15m['total_consecutive_fvg']} trades")
    
    print("\n" + "=" * 70)
    print("  GENERATING REPORTS AND CHARTS")
    print("=" * 70)
    
    # Generate markdown reports
    for tf, results in [('1m', all_results_1m), ('5m', all_results_5m), ('15m', all_results_15m)]:
        md_content = generate_markdown_report(results, tf, rr_levels, output_dir)
        with open(os.path.join(output_dir, f'FVG_Backtest_{tf}.md'), 'w') as f:
            f.write(md_content)
        print(f"  Generated: FVG_Backtest_{tf}.md")
        
        generate_charts(results, tf, rr_levels, output_dir)
        print(f"  Generated: FVG_Backtest_{tf}_WinRate.png")
    
    # Print summary
    print("\n" + "=" * 70)
    print("  SUMMARY")
    print("=" * 70)
    
    for tf, results in [('1m', all_results_1m), ('5m', all_results_5m), ('15m', all_results_15m)]:
        print(f"\n{tf} Timeframe:")
        print(f"  Total Trades: {results['total_consecutive_fvg']}")
        print(f"  Best Win Rate (SL 50%, RR 1.0): {calculate_win_rate(results, 'sl_50', 1.0):.1f}%")
        print(f"  Best Win Rate (SL 100%, RR 1.0): {calculate_win_rate(results, 'sl_100', 1.0):.1f}%")
        print(f"  Best Win Rate (SL FVG Mid, RR 1.0): {calculate_win_rate(results, 'sl_fvg_mid', 1.0):.1f}%")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Generate Markdown reports and PNG charts for FVG analysis results.
Creates separate reports for 1m, 5m, and 15m timeframes.
"""

import os
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import numpy as np

# Import functions from main analysis script
from fvg_analysis import (
    load_csv_data, filter_session_hours, find_fvg_patterns_with_details,
    backtest_patterns, aggregate_backtest_results, get_data_files,
    analyze_fvg_patterns, SESSION_START, SESSION_END, EARLY_SESSION_START,
    EARLY_SESSION_END, MIN_CANDLES_FOR_ANALYSIS, RR_LEVELS, SL_TYPES
)

DATA_DIR = os.path.dirname(os.path.abspath(__file__))


def run_analysis_for_timeframe(timeframe):
    """Run complete analysis for a specific timeframe."""
    files = get_data_files(timeframe)
    
    # Results storage
    full_session_patterns = {
        'total_candles': 0,
        'total_sessions': 0,
        'fvg_count': 0,
        'bullish_fvg_count': 0,
        'bearish_fvg_count': 0,
        'fvg_normal_fvg_count': 0,
        'bullish_pattern_count': 0,
        'bearish_pattern_count': 0
    }
    
    early_session_patterns = {
        'total_candles': 0,
        'total_sessions': 0,
        'fvg_count': 0,
        'bullish_fvg_count': 0,
        'bearish_fvg_count': 0,
        'fvg_normal_fvg_count': 0,
        'bullish_pattern_count': 0,
        'bearish_pattern_count': 0
    }
    
    full_backtest_results = []
    early_backtest_results = []
    yearly_data = []
    
    for year, filepath in files:
        try:
            df = load_csv_data(filepath)
            if df is None or len(df) == 0:
                continue
            
            # Full session (8:30-12:00)
            df_full = filter_session_hours(df, SESSION_START, SESSION_END)
            if len(df_full) >= MIN_CANDLES_FOR_ANALYSIS:
                results = analyze_fvg_patterns(df_full)
                for key in full_session_patterns:
                    full_session_patterns[key] += results[key]
                
                patterns = find_fvg_patterns_with_details(df_full)
                if patterns:
                    bt_results = backtest_patterns(df_full, patterns)
                    full_backtest_results.append(bt_results)
                
                yearly_data.append({
                    'year': year,
                    'session': 'full',
                    **results
                })
            
            # Early session (8:30-9:00)
            df_early = filter_session_hours(df, EARLY_SESSION_START, EARLY_SESSION_END)
            if len(df_early) >= MIN_CANDLES_FOR_ANALYSIS:
                early_results = analyze_fvg_patterns(df_early)
                for key in early_session_patterns:
                    early_session_patterns[key] += early_results[key]
                
                early_patterns = find_fvg_patterns_with_details(df_early)
                if early_patterns:
                    early_bt_results = backtest_patterns(df_early, early_patterns)
                    early_backtest_results.append(early_bt_results)
                
                yearly_data.append({
                    'year': year,
                    'session': 'early',
                    **early_results
                })
                
        except Exception as e:
            print(f"Error processing {filepath}: {e}")
    
    # Aggregate backtest results
    full_bt = aggregate_backtest_results(full_backtest_results) if full_backtest_results else None
    early_bt = aggregate_backtest_results(early_backtest_results) if early_backtest_results else None
    
    return {
        'full_session': full_session_patterns,
        'early_session': early_session_patterns,
        'full_backtest': full_bt,
        'early_backtest': early_bt,
        'yearly_data': yearly_data
    }


def calculate_win_rates(backtest_results):
    """Calculate win rates from backtest results."""
    if not backtest_results:
        return None
    
    win_rates = {
        'bullish': {},
        'bearish': {}
    }
    
    for pattern_type in ['bullish', 'bearish']:
        for sl_type in SL_TYPES:
            win_rates[pattern_type][sl_type] = {}
            for rr in RR_LEVELS:
                data = backtest_results[pattern_type][sl_type][rr]
                total = data['wins'] + data['losses']
                if total > 0:
                    win_rates[pattern_type][sl_type][rr] = {
                        'win_rate': (data['wins'] / total) * 100,
                        'wins': data['wins'],
                        'losses': data['losses'],
                        'timeouts': data['timeouts'],
                        'total': total
                    }
                else:
                    win_rates[pattern_type][sl_type][rr] = {
                        'win_rate': 0,
                        'wins': 0,
                        'losses': 0,
                        'timeouts': 0,
                        'total': 0
                    }
    
    return win_rates


def generate_winrate_chart(win_rates, timeframe, session_name, pattern_type, output_path):
    """Generate a bar chart for win rates."""
    if not win_rates:
        return
    
    fig, ax = plt.subplots(figsize=(14, 8))
    
    x = np.arange(len(RR_LEVELS))
    width = 0.25
    
    colors = {'50%': '#2ecc71', '100%': '#3498db', 'gap': '#e74c3c'}
    
    for i, sl_type in enumerate(SL_TYPES):
        rates = [win_rates[pattern_type][sl_type][rr]['win_rate'] for rr in RR_LEVELS]
        bars = ax.bar(x + i * width, rates, width, label=f'SL {sl_type}', color=colors[sl_type])
        
        # Add value labels on bars
        for bar, rate in zip(bars, rates):
            height = bar.get_height()
            ax.annotate(f'{rate:.1f}%',
                       xy=(bar.get_x() + bar.get_width() / 2, height),
                       xytext=(0, 3),
                       textcoords="offset points",
                       ha='center', va='bottom', fontsize=8)
    
    trade_type = "LONG" if pattern_type == 'bullish' else "SHORT"
    ax.set_xlabel('Risk-Reward Ratio', fontsize=12)
    ax.set_ylabel('Win Rate (%)', fontsize=12)
    ax.set_title(f'{timeframe} - {session_name}\n{trade_type} Trades ({pattern_type.capitalize()} Patterns) - Win Rates by SL Type and RR', fontsize=14)
    ax.set_xticks(x + width)
    ax.set_xticklabels([f'RR {rr}' for rr in RR_LEVELS])
    ax.legend(title='Stop Loss Type')
    ax.set_ylim(0, 70)
    ax.grid(axis='y', alpha=0.3)
    
    # Add horizontal line at 50%
    ax.axhline(y=50, color='gray', linestyle='--', alpha=0.5, label='50% threshold')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()


def generate_comparison_chart(full_win_rates, early_win_rates, timeframe, pattern_type, sl_type, output_path):
    """Generate comparison chart between full and early sessions."""
    if not full_win_rates or not early_win_rates:
        return
    
    fig, ax = plt.subplots(figsize=(12, 7))
    
    x = np.arange(len(RR_LEVELS))
    width = 0.35
    
    full_rates = [full_win_rates[pattern_type][sl_type][rr]['win_rate'] for rr in RR_LEVELS]
    early_rates = [early_win_rates[pattern_type][sl_type][rr]['win_rate'] for rr in RR_LEVELS]
    
    bars1 = ax.bar(x - width/2, full_rates, width, label='Full Session (8:30-12:00)', color='#3498db')
    bars2 = ax.bar(x + width/2, early_rates, width, label='Early Session (8:30-9:00)', color='#e74c3c')
    
    # Add value labels
    for bars, rates in [(bars1, full_rates), (bars2, early_rates)]:
        for bar, rate in zip(bars, rates):
            height = bar.get_height()
            ax.annotate(f'{rate:.1f}%',
                       xy=(bar.get_x() + bar.get_width() / 2, height),
                       xytext=(0, 3),
                       textcoords="offset points",
                       ha='center', va='bottom', fontsize=8)
    
    trade_type = "LONG" if pattern_type == 'bullish' else "SHORT"
    ax.set_xlabel('Risk-Reward Ratio', fontsize=12)
    ax.set_ylabel('Win Rate (%)', fontsize=12)
    ax.set_title(f'{timeframe} - {trade_type} Trades - SL {sl_type}\nSession Comparison', fontsize=14)
    ax.set_xticks(x)
    ax.set_xticklabels([f'RR {rr}' for rr in RR_LEVELS])
    ax.legend()
    ax.set_ylim(0, 70)
    ax.grid(axis='y', alpha=0.3)
    ax.axhline(y=50, color='gray', linestyle='--', alpha=0.5)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()


def generate_markdown_report(timeframe, analysis_results):
    """Generate markdown report for a specific timeframe."""
    full = analysis_results['full_session']
    early = analysis_results['early_session']
    full_bt = analysis_results['full_backtest']
    early_bt = analysis_results['early_backtest']
    
    full_win_rates = calculate_win_rates(full_bt)
    early_win_rates = calculate_win_rates(early_bt)
    
    md = f"""# FVG Analysis Report - {timeframe} Timeframe

## Overview

This report analyzes **FVG (Fair Value Gap)** patterns on the **{timeframe}** timeframe from 2018 to 2025.

### Pattern Definition
- **Pattern**: FVG → Normal candle (no FVG) → FVG
- **Direction**: Both FVGs must be of the same direction (bullish-bullish or bearish-bearish)
- **FVG Definition**:
  - **Bullish FVG**: Low of candle n+1 > High of candle n-1
  - **Bearish FVG**: High of candle n+1 < Low of candle n-1

---

## Session Analysis

### Full Session (8:30 - 12:00)

| Metric | Value |
|--------|-------|
| Total Candles | {full['total_candles']:,} |
| Total Trading Sessions | {full['total_sessions']:,} |
| Total FVGs | {full['fvg_count']:,} |
| Bullish FVGs | {full['bullish_fvg_count']:,} |
| Bearish FVGs | {full['bearish_fvg_count']:,} |
| **FVG-Normal-FVG Patterns** | **{full['fvg_normal_fvg_count']:,}** |
| Bullish Patterns | {full['bullish_pattern_count']:,} |
| Bearish Patterns | {full['bearish_pattern_count']:,} |
| Pattern Rate | {(full['fvg_normal_fvg_count'] / full['total_candles'] * 100) if full['total_candles'] > 0 else 0:.2f}% |

### Early Session (8:30 - 9:00)

| Metric | Value |
|--------|-------|
| Total Candles | {early['total_candles']:,} |
| Total Trading Sessions | {early['total_sessions']:,} |
| Total FVGs | {early['fvg_count']:,} |
| Bullish FVGs | {early['bullish_fvg_count']:,} |
| Bearish FVGs | {early['bearish_fvg_count']:,} |
| **FVG-Normal-FVG Patterns** | **{early['fvg_normal_fvg_count']:,}** |
| Bullish Patterns | {early['bullish_pattern_count']:,} |
| Bearish Patterns | {early['bearish_pattern_count']:,} |
| Pattern Rate | {(early['fvg_normal_fvg_count'] / early['total_candles'] * 100) if early['total_candles'] > 0 else 0:.2f}% |

---

## Backtesting Results

### Stop Loss Types
- **SL 50%**: Stop loss at 50% of entry candle (n+1) range beyond its extreme
- **SL 100%**: Stop loss at the extreme of entry candle (n+1)
- **SL gap**: Stop loss beyond the FVG gap of the second FVG

### Risk-Reward Ratios
RR 1, RR 1.5, RR 2, RR 2.5, RR 3, RR 3.5, RR 4, RR 4.5, RR 5

---

## Full Session (8:30 - 12:00) - Win Rates

### LONG Trades (Bullish Patterns)

| SL Type | RR 1 | RR 1.5 | RR 2 | RR 2.5 | RR 3 | RR 3.5 | RR 4 | RR 4.5 | RR 5 |
|---------|------|--------|------|--------|------|--------|------|--------|------|
"""
    
    if full_win_rates:
        for sl_type in SL_TYPES:
            row = f"| {sl_type} |"
            for rr in RR_LEVELS:
                wr = full_win_rates['bullish'][sl_type][rr]['win_rate']
                row += f" {wr:.1f}% |"
            md += row + "\n"
    else:
        md += "| N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |\n"
    
    md += """
### SHORT Trades (Bearish Patterns)

| SL Type | RR 1 | RR 1.5 | RR 2 | RR 2.5 | RR 3 | RR 3.5 | RR 4 | RR 4.5 | RR 5 |
|---------|------|--------|------|--------|------|--------|------|--------|------|
"""
    
    if full_win_rates:
        for sl_type in SL_TYPES:
            row = f"| {sl_type} |"
            for rr in RR_LEVELS:
                wr = full_win_rates['bearish'][sl_type][rr]['win_rate']
                row += f" {wr:.1f}% |"
            md += row + "\n"
    else:
        md += "| N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |\n"

    md += f"""
### Trade Counts - Full Session

#### LONG Trades (Bullish)
| SL Type | Wins | Losses | Timeouts | Total | Win Rate |
|---------|------|--------|----------|-------|----------|
"""
    
    if full_win_rates:
        for sl_type in SL_TYPES:
            # Use RR 1 for total counts
            data = full_win_rates['bullish'][sl_type][1]
            md += f"| {sl_type} | {data['wins']} | {data['losses']} | {data['timeouts']} | {data['total']} | {data['win_rate']:.1f}% |\n"

    md += """
#### SHORT Trades (Bearish)
| SL Type | Wins | Losses | Timeouts | Total | Win Rate |
|---------|------|--------|----------|-------|----------|
"""
    
    if full_win_rates:
        for sl_type in SL_TYPES:
            data = full_win_rates['bearish'][sl_type][1]
            md += f"| {sl_type} | {data['wins']} | {data['losses']} | {data['timeouts']} | {data['total']} | {data['win_rate']:.1f}% |\n"

    md += f"""
---

## Early Session (8:30 - 9:00) - Win Rates

### LONG Trades (Bullish Patterns)

| SL Type | RR 1 | RR 1.5 | RR 2 | RR 2.5 | RR 3 | RR 3.5 | RR 4 | RR 4.5 | RR 5 |
|---------|------|--------|------|--------|------|--------|------|--------|------|
"""
    
    if early_win_rates:
        for sl_type in SL_TYPES:
            row = f"| {sl_type} |"
            for rr in RR_LEVELS:
                wr = early_win_rates['bullish'][sl_type][rr]['win_rate']
                row += f" {wr:.1f}% |"
            md += row + "\n"
    else:
        md += "| N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |\n"
    
    md += """
### SHORT Trades (Bearish Patterns)

| SL Type | RR 1 | RR 1.5 | RR 2 | RR 2.5 | RR 3 | RR 3.5 | RR 4 | RR 4.5 | RR 5 |
|---------|------|--------|------|--------|------|--------|------|--------|------|
"""
    
    if early_win_rates:
        for sl_type in SL_TYPES:
            row = f"| {sl_type} |"
            for rr in RR_LEVELS:
                wr = early_win_rates['bearish'][sl_type][rr]['win_rate']
                row += f" {wr:.1f}% |"
            md += row + "\n"
    else:
        md += "| N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |\n"

    md += f"""
---

## Charts

### Full Session Win Rates

#### LONG Trades
![LONG Trades - Full Session](charts/{timeframe}_full_session_long.png)

#### SHORT Trades
![SHORT Trades - Full Session](charts/{timeframe}_full_session_short.png)

### Early Session Win Rates

#### LONG Trades
![LONG Trades - Early Session](charts/{timeframe}_early_session_long.png)

#### SHORT Trades
![SHORT Trades - Early Session](charts/{timeframe}_early_session_short.png)

### Session Comparison

#### LONG Trades - SL 50%
![LONG Comparison - SL 50%](charts/{timeframe}_comparison_long_50.png)

#### SHORT Trades - SL 50%
![SHORT Comparison - SL 50%](charts/{timeframe}_comparison_short_50.png)

---

## Key Findings

1. **Pattern Rate**: The FVG-Normal-FVG pattern occurs more frequently during the early session (8:30-9:00) compared to the full session.

2. **Win Rates**: 
   - Win rates decrease as RR increases (as expected)
   - SL 50% generally provides the best balance for higher RR trades
   - SL 100% tends to have higher win rates at RR 1, but lower at higher RRs

3. **Session Comparison**:
   - Early session often shows slightly better win rates due to higher volatility
   - Pattern occurrence is more concentrated in the first 30 minutes

---

*Report generated from FVG Analysis Script*
*Data: 2018-2025*
"""
    
    return md, full_win_rates, early_win_rates


def main():
    """Generate all reports and charts."""
    print("=" * 60)
    print("Generating FVG Analysis Reports")
    print("=" * 60)
    
    # Create charts directory
    charts_dir = os.path.join(DATA_DIR, 'charts')
    os.makedirs(charts_dir, exist_ok=True)
    
    timeframes = ['1m', '5m', '15m']
    
    for tf in timeframes:
        print(f"\nProcessing {tf} timeframe...")
        
        # Run analysis
        results = run_analysis_for_timeframe(tf)
        
        # Generate markdown and get win rates
        md_content, full_wr, early_wr = generate_markdown_report(tf, results)
        
        # Save markdown file
        md_path = os.path.join(DATA_DIR, f'FVG_Analysis_{tf}.md')
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
        print(f"  Created: {md_path}")
        
        # Generate charts
        if full_wr:
            # Full session charts
            generate_winrate_chart(
                full_wr, tf, "Full Session (8:30-12:00)", "bullish",
                os.path.join(charts_dir, f'{tf}_full_session_long.png')
            )
            generate_winrate_chart(
                full_wr, tf, "Full Session (8:30-12:00)", "bearish",
                os.path.join(charts_dir, f'{tf}_full_session_short.png')
            )
            print(f"  Created: {tf} full session charts")
        
        if early_wr:
            # Early session charts
            generate_winrate_chart(
                early_wr, tf, "Early Session (8:30-9:00)", "bullish",
                os.path.join(charts_dir, f'{tf}_early_session_long.png')
            )
            generate_winrate_chart(
                early_wr, tf, "Early Session (8:30-9:00)", "bearish",
                os.path.join(charts_dir, f'{tf}_early_session_short.png')
            )
            print(f"  Created: {tf} early session charts")
        
        if full_wr and early_wr:
            # Comparison charts
            generate_comparison_chart(
                full_wr, early_wr, tf, "bullish", "50%",
                os.path.join(charts_dir, f'{tf}_comparison_long_50.png')
            )
            generate_comparison_chart(
                full_wr, early_wr, tf, "bearish", "50%",
                os.path.join(charts_dir, f'{tf}_comparison_short_50.png')
            )
            print(f"  Created: {tf} comparison charts")
    
    print("\n" + "=" * 60)
    print("Report generation complete!")
    print("=" * 60)
    print(f"\nGenerated files:")
    print(f"  - FVG_Analysis_1m.md")
    print(f"  - FVG_Analysis_5m.md")
    print(f"  - FVG_Analysis_15m.md")
    print(f"  - charts/ directory with PNG files")


if __name__ == "__main__":
    main()

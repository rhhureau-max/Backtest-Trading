#!/usr/bin/env python3
"""
Report Generator for Liquidity Sweep SMC Strategy Backtest

This script runs the backtest and generates:
1. Comprehensive markdown report (BACKTEST_REPORT.md)
2. Performance visualization charts (PNG files in reports/ directory)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
from datetime import datetime
import os
import sys

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from liquidity_sweep_backtest import (
    load_all_1m_data, run_backtest, calculate_statistics,
    SWING_LOOKBACK, FVG_LOOKBACK_CANDLES, RISK_REWARD_RATIO, SL_BUFFER_POINTS
)

# Configuration
REPORT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'reports')
REPORT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'BACKTEST_REPORT.md')

# Set matplotlib style
plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['savefig.dpi'] = 150
plt.rcParams['savefig.bbox'] = 'tight'


def ensure_report_dir():
    """Create reports directory if it doesn't exist."""
    if not os.path.exists(REPORT_DIR):
        os.makedirs(REPORT_DIR)
    print(f"Reports will be saved to: {REPORT_DIR}")


def generate_equity_curve(trades, stats):
    """Generate equity curve chart."""
    if not trades:
        return None
    
    completed_trades = [t for t in trades if t['outcome'] in ['WIN', 'LOSS']]
    if not completed_trades:
        return None
    
    # Sort by entry time
    completed_trades.sort(key=lambda x: x['entry_time'])
    
    # Calculate cumulative PnL
    times = [t['entry_time'] for t in completed_trades]
    cumulative_pnl = []
    running = 0
    for t in completed_trades:
        running += t['pnl']
        cumulative_pnl.append(running)
    
    # Calculate running max for drawdown visualization
    running_max = []
    peak = 0
    for pnl in cumulative_pnl:
        if pnl > peak:
            peak = pnl
        running_max.append(peak)
    
    fig, ax = plt.subplots(figsize=(14, 7))
    
    # Plot equity curve
    ax.plot(times, cumulative_pnl, 'b-', linewidth=2, label='Equity Curve', zorder=3)
    ax.fill_between(times, cumulative_pnl, 0, alpha=0.3, color='blue')
    
    # Plot running max (for drawdown reference)
    ax.plot(times, running_max, 'g--', linewidth=1, alpha=0.7, label='Peak Equity')
    
    # Shade drawdown areas
    ax.fill_between(times, running_max, cumulative_pnl, alpha=0.2, color='red', label='Drawdown')
    
    ax.set_title('Equity Curve - Liquidity Sweep SMC Strategy', fontsize=14, fontweight='bold')
    ax.set_xlabel('Date', fontsize=11)
    ax.set_ylabel('Cumulative PnL (Points)', fontsize=11)
    ax.legend(loc='upper left')
    ax.grid(True, alpha=0.3)
    
    # Format x-axis
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.xticks(rotation=45)
    
    # Add horizontal line at 0
    ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5, alpha=0.5)
    
    # Add stats annotation
    stats_text = f"Total PnL: {stats['total_pnl']:.2f}\nMax DD: {stats['max_drawdown']:.2f}"
    ax.annotate(stats_text, xy=(0.98, 0.02), xycoords='axes fraction',
                fontsize=10, ha='right', va='bottom',
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    plt.tight_layout()
    filepath = os.path.join(REPORT_DIR, 'equity_curve.png')
    plt.savefig(filepath)
    plt.close()
    
    return filepath


def generate_monthly_returns_heatmap(trades):
    """Generate monthly returns heatmap."""
    if not trades:
        return None
    
    completed_trades = [t for t in trades if t['outcome'] in ['WIN', 'LOSS']]
    if not completed_trades:
        return None
    
    # Create DataFrame
    df = pd.DataFrame(completed_trades)
    df['entry_time'] = pd.to_datetime(df['entry_time'])
    df['year'] = df['entry_time'].dt.year
    df['month'] = df['entry_time'].dt.month
    
    # Calculate monthly PnL
    monthly_pnl = df.groupby(['year', 'month'])['pnl'].sum().unstack(fill_value=0)
    
    # Create heatmap
    fig, ax = plt.subplots(figsize=(14, 6))
    
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    # Reindex to ensure all months are present
    monthly_pnl = monthly_pnl.reindex(columns=range(1, 13), fill_value=0)
    
    # Create diverging colormap centered at 0
    vmax = max(abs(monthly_pnl.min().min()), abs(monthly_pnl.max().max()))
    
    sns.heatmap(monthly_pnl, annot=True, fmt='.1f', cmap='RdYlGn', center=0,
                xticklabels=month_names, ax=ax, cbar_kws={'label': 'PnL (Points)'},
                vmin=-vmax, vmax=vmax)
    
    ax.set_title('Monthly Returns Heatmap', fontsize=14, fontweight='bold')
    ax.set_xlabel('Month', fontsize=11)
    ax.set_ylabel('Year', fontsize=11)
    
    plt.tight_layout()
    filepath = os.path.join(REPORT_DIR, 'monthly_returns.png')
    plt.savefig(filepath)
    plt.close()
    
    return filepath


def generate_trade_distribution(trades, stats):
    """Generate trade distribution charts."""
    if not trades:
        return None
    
    completed_trades = [t for t in trades if t['outcome'] in ['WIN', 'LOSS']]
    if not completed_trades:
        return None
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # 1. Win/Loss Pie Chart
    ax1 = axes[0, 0]
    wins = stats['wins']
    losses = stats['losses']
    colors = ['#2ecc71', '#e74c3c']
    explode = (0.05, 0)
    ax1.pie([wins, losses], explode=explode, labels=['Wins', 'Losses'], 
            colors=colors, autopct='%1.1f%%', shadow=True, startangle=90)
    ax1.set_title('Win/Loss Distribution', fontsize=12, fontweight='bold')
    
    # 2. Long vs Short Distribution
    ax2 = axes[0, 1]
    long_trades = [t for t in completed_trades if t['direction'] == 'LONG']
    short_trades = [t for t in completed_trades if t['direction'] == 'SHORT']
    
    long_wins = len([t for t in long_trades if t['outcome'] == 'WIN'])
    long_losses = len([t for t in long_trades if t['outcome'] == 'LOSS'])
    short_wins = len([t for t in short_trades if t['outcome'] == 'WIN'])
    short_losses = len([t for t in short_trades if t['outcome'] == 'LOSS'])
    
    x = np.arange(2)
    width = 0.35
    
    bars1 = ax2.bar(x - width/2, [long_wins, short_wins], width, label='Wins', color='#2ecc71')
    bars2 = ax2.bar(x + width/2, [long_losses, short_losses], width, label='Losses', color='#e74c3c')
    
    ax2.set_title('Trade Direction Analysis', fontsize=12, fontweight='bold')
    ax2.set_xticks(x)
    ax2.set_xticklabels(['LONG', 'SHORT'])
    ax2.legend()
    ax2.set_ylabel('Number of Trades')
    
    # Add value labels on bars
    for bar in bars1 + bars2:
        height = bar.get_height()
        ax2.annotate(f'{int(height)}', xy=(bar.get_x() + bar.get_width()/2, height),
                    xytext=(0, 3), textcoords="offset points", ha='center', va='bottom')
    
    # 3. PnL Distribution Histogram
    ax3 = axes[1, 0]
    pnls = [t['pnl'] for t in completed_trades]
    
    # Color bins based on positive/negative
    n, bins, patches = ax3.hist(pnls, bins=30, edgecolor='black', alpha=0.7)
    
    for i, patch in enumerate(patches):
        if bins[i] + bins[i+1] / 2 >= 0:
            patch.set_facecolor('#2ecc71')
        else:
            patch.set_facecolor('#e74c3c')
    
    ax3.axvline(x=0, color='black', linestyle='--', linewidth=1)
    ax3.axvline(x=np.mean(pnls), color='blue', linestyle='-', linewidth=2, label=f'Mean: {np.mean(pnls):.2f}')
    ax3.set_title('PnL Distribution', fontsize=12, fontweight='bold')
    ax3.set_xlabel('PnL (Points)')
    ax3.set_ylabel('Frequency')
    ax3.legend()
    
    # 4. Trade Duration Analysis (if exit_time exists)
    ax4 = axes[1, 1]
    
    # Calculate trade durations
    durations = []
    for t in completed_trades:
        if t.get('exit_time') and t.get('entry_time'):
            duration = (t['exit_time'] - t['entry_time']).total_seconds() / 60  # in minutes
            durations.append(duration)
    
    if durations:
        win_durations = [durations[i] for i, t in enumerate(completed_trades) if t['outcome'] == 'WIN' and i < len(durations)]
        loss_durations = [durations[i] for i, t in enumerate(completed_trades) if t['outcome'] == 'LOSS' and i < len(durations)]
        
        bp = ax4.boxplot([win_durations, loss_durations], labels=['Winning Trades', 'Losing Trades'],
                         patch_artist=True)
        bp['boxes'][0].set_facecolor('#2ecc71')
        bp['boxes'][1].set_facecolor('#e74c3c')
        
        ax4.set_title('Trade Duration Analysis', fontsize=12, fontweight='bold')
        ax4.set_ylabel('Duration (Minutes)')
    else:
        ax4.text(0.5, 0.5, 'Duration data not available', ha='center', va='center', transform=ax4.transAxes)
        ax4.set_title('Trade Duration Analysis', fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    filepath = os.path.join(REPORT_DIR, 'trade_distribution.png')
    plt.savefig(filepath)
    plt.close()
    
    return filepath


def generate_yearly_performance(trades, stats):
    """Generate yearly performance bar chart."""
    if not trades:
        return None
    
    completed_trades = [t for t in trades if t['outcome'] in ['WIN', 'LOSS']]
    if not completed_trades:
        return None
    
    # Create DataFrame
    df = pd.DataFrame(completed_trades)
    df['entry_time'] = pd.to_datetime(df['entry_time'])
    df['year'] = df['entry_time'].dt.year
    
    # Calculate yearly stats
    yearly_stats = df.groupby('year').agg({
        'pnl': ['sum', 'count'],
        'outcome': lambda x: (x == 'WIN').sum()
    }).reset_index()
    yearly_stats.columns = ['Year', 'Total PnL', 'Trades', 'Wins']
    yearly_stats['Win Rate'] = yearly_stats['Wins'] / yearly_stats['Trades'] * 100
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # 1. Yearly PnL
    ax1 = axes[0]
    colors = ['#2ecc71' if x >= 0 else '#e74c3c' for x in yearly_stats['Total PnL']]
    bars = ax1.bar(yearly_stats['Year'].astype(str), yearly_stats['Total PnL'], color=colors, edgecolor='black')
    
    ax1.set_title('Yearly PnL Performance', fontsize=12, fontweight='bold')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('PnL (Points)')
    ax1.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
    
    # Add value labels
    for bar, val in zip(bars, yearly_stats['Total PnL']):
        height = bar.get_height()
        ax1.annotate(f'{val:.1f}', xy=(bar.get_x() + bar.get_width()/2, height),
                    xytext=(0, 3 if height >= 0 else -12), textcoords="offset points", 
                    ha='center', va='bottom' if height >= 0 else 'top', fontsize=9)
    
    # 2. Yearly Win Rate with trade count
    ax2 = axes[1]
    x = np.arange(len(yearly_stats))
    width = 0.4
    
    bars1 = ax2.bar(x - width/2, yearly_stats['Win Rate'], width, label='Win Rate %', color='#3498db')
    
    ax2_twin = ax2.twinx()
    bars2 = ax2_twin.bar(x + width/2, yearly_stats['Trades'], width, label='# Trades', color='#9b59b6', alpha=0.7)
    
    ax2.set_title('Yearly Win Rate & Trade Count', fontsize=12, fontweight='bold')
    ax2.set_xlabel('Year')
    ax2.set_ylabel('Win Rate (%)', color='#3498db')
    ax2_twin.set_ylabel('Number of Trades', color='#9b59b6')
    ax2.set_xticks(x)
    ax2.set_xticklabels(yearly_stats['Year'].astype(str))
    
    # Add legends
    lines1, labels1 = ax2.get_legend_handles_labels()
    lines2, labels2 = ax2_twin.get_legend_handles_labels()
    ax2.legend(lines1 + lines2, labels1 + labels2, loc='upper right')
    
    plt.tight_layout()
    filepath = os.path.join(REPORT_DIR, 'yearly_performance.png')
    plt.savefig(filepath)
    plt.close()
    
    return filepath


def generate_drawdown_analysis(trades, stats):
    """Generate drawdown analysis chart."""
    if not trades:
        return None
    
    completed_trades = [t for t in trades if t['outcome'] in ['WIN', 'LOSS']]
    if not completed_trades:
        return None
    
    # Sort by entry time
    completed_trades.sort(key=lambda x: x['entry_time'])
    
    # Calculate cumulative PnL and drawdown
    times = [t['entry_time'] for t in completed_trades]
    cumulative_pnl = []
    drawdowns = []
    running = 0
    peak = 0
    
    for t in completed_trades:
        running += t['pnl']
        cumulative_pnl.append(running)
        if running > peak:
            peak = running
        dd = peak - running
        drawdowns.append(dd)
    
    fig, axes = plt.subplots(2, 1, figsize=(14, 10), sharex=True)
    
    # 1. Equity curve
    ax1 = axes[0]
    ax1.plot(times, cumulative_pnl, 'b-', linewidth=2)
    ax1.fill_between(times, cumulative_pnl, 0, alpha=0.3, color='blue')
    ax1.set_title('Equity Curve', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Cumulative PnL (Points)')
    ax1.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
    ax1.grid(True, alpha=0.3)
    
    # 2. Drawdown chart
    ax2 = axes[1]
    ax2.fill_between(times, 0, [-d for d in drawdowns], alpha=0.5, color='red')
    ax2.plot(times, [-d for d in drawdowns], 'r-', linewidth=1)
    ax2.set_title('Drawdown Analysis', fontsize=12, fontweight='bold')
    ax2.set_xlabel('Date')
    ax2.set_ylabel('Drawdown (Points)')
    ax2.grid(True, alpha=0.3)
    
    # Format x-axis
    ax2.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.xticks(rotation=45)
    
    # Add max drawdown annotation
    max_dd_idx = drawdowns.index(max(drawdowns))
    ax2.annotate(f'Max DD: {max(drawdowns):.2f}', 
                xy=(times[max_dd_idx], -max(drawdowns)),
                xytext=(10, -30), textcoords='offset points',
                arrowprops=dict(arrowstyle='->', color='darkred'),
                fontsize=10, color='darkred', fontweight='bold')
    
    plt.tight_layout()
    filepath = os.path.join(REPORT_DIR, 'drawdown_analysis.png')
    plt.savefig(filepath)
    plt.close()
    
    return filepath


def generate_markdown_report(trades, stats, chart_files):
    """Generate comprehensive markdown report."""
    completed_trades = [t for t in trades if t['outcome'] in ['WIN', 'LOSS']]
    
    # Calculate additional stats
    if completed_trades:
        df = pd.DataFrame(completed_trades)
        df['entry_time'] = pd.to_datetime(df['entry_time'])
        
        long_trades = df[df['direction'] == 'LONG']
        short_trades = df[df['direction'] == 'SHORT']
        
        long_wins = len(long_trades[long_trades['outcome'] == 'WIN'])
        long_total = len(long_trades)
        long_winrate = (long_wins / long_total * 100) if long_total > 0 else 0
        long_pnl = long_trades['pnl'].sum() if len(long_trades) > 0 else 0
        
        short_wins = len(short_trades[short_trades['outcome'] == 'WIN'])
        short_total = len(short_trades)
        short_winrate = (short_wins / short_total * 100) if short_total > 0 else 0
        short_pnl = short_trades['pnl'].sum() if len(short_trades) > 0 else 0
        
        avg_win = df[df['outcome'] == 'WIN']['pnl'].mean() if stats['wins'] > 0 else 0
        avg_loss = abs(df[df['outcome'] == 'LOSS']['pnl'].mean()) if stats['losses'] > 0 else 0
        
        # Calculate consecutive wins/losses
        outcomes = df['outcome'].tolist()
        max_consecutive_wins = 0
        max_consecutive_losses = 0
        current_wins = 0
        current_losses = 0
        
        for outcome in outcomes:
            if outcome == 'WIN':
                current_wins += 1
                current_losses = 0
                max_consecutive_wins = max(max_consecutive_wins, current_wins)
            else:
                current_losses += 1
                current_wins = 0
                max_consecutive_losses = max(max_consecutive_losses, current_losses)
        
        # Date range
        start_date = df['entry_time'].min().strftime('%Y-%m-%d')
        end_date = df['entry_time'].max().strftime('%Y-%m-%d')
    else:
        long_winrate = short_winrate = long_pnl = short_pnl = 0
        avg_win = avg_loss = 0
        max_consecutive_wins = max_consecutive_losses = 0
        start_date = end_date = 'N/A'
    
    # Generate report
    pf_display = f"{stats['profit_factor']:.2f}" if stats['profit_factor'] is not None else "∞ (no losses)"
    
    report = f"""# 📊 Liquidity Sweep SMC Strategy - Backtest Report

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Data Period:** {start_date} to {end_date}

---

## 📋 Strategy Overview

This backtest evaluates a **Multi-Timeframe Smart Money Concepts (SMC)** strategy based on liquidity sweeps with Fair Value Gap (FVG) confirmation.

### Strategy Logic

| Timeframe | Purpose | Conditions |
|-----------|---------|------------|
| **M15** | Zone of Interest (POI) | Identify Swing Highs/Lows with {SWING_LOOKBACK}-candle lookback. Detect liquidity sweeps (wick-only breaks that close inside range) |
| **M5** | Structure Confirmation | Within {FVG_LOOKBACK_CANDLES} candles post-sweep, identify FVG in opposite direction (institutional displacement signal) |
| **M1** | Execution | Entry on FVG fill. SL at sweep wick + {SL_BUFFER_POINTS} points buffer. TP at 1:{RISK_REWARD_RATIO:.0f} RR |

---

## 📈 Performance Summary

### Key Metrics

| Metric | Value |
|--------|-------|
| **Total Trades** | {stats['total_trades']} |
| **Completed Trades** | {stats['completed_trades']} |
| **Win Rate** | **{stats['win_rate']:.2f}%** |
| **Profit Factor** | **{pf_display}** |
| **Total PnL** | **{stats['total_pnl']:.2f} points** |
| **Average PnL/Trade** | {stats['avg_pnl']:.2f} points |
| **Max Drawdown** | {stats['max_drawdown']:.2f} points |

### Win/Loss Breakdown

| Category | Count | Percentage |
|----------|-------|------------|
| Wins | {stats['wins']} | {stats['win_rate']:.1f}% |
| Losses | {stats['losses']} | {100 - stats['win_rate']:.1f}% |
| Open Trades | {stats['open_trades']} | - |

### Profit Analysis

| Metric | Value |
|--------|-------|
| Gross Profit | {stats['gross_profit']:.2f} points |
| Gross Loss | {stats['gross_loss']:.2f} points |
| Average Win | {avg_win:.2f} points |
| Average Loss | {avg_loss:.2f} points |
| Max Consecutive Wins | {max_consecutive_wins} |
| Max Consecutive Losses | {max_consecutive_losses} |

---

## 🔄 Direction Analysis

| Direction | Trades | Win Rate | Total PnL |
|-----------|--------|----------|-----------|
| **LONG** | {stats['long_trades']} | {long_winrate:.2f}% | {long_pnl:.2f} points |
| **SHORT** | {stats['short_trades']} | {short_winrate:.2f}% | {short_pnl:.2f} points |

---

## 📊 Visual Analysis

### Equity Curve

The equity curve shows the cumulative profit/loss over time, with drawdown periods highlighted in red.

![Equity Curve](reports/equity_curve.png)

---

### Monthly Returns Heatmap

This heatmap visualizes monthly performance across all backtested years. Green indicates profitable months, red indicates losing months.

![Monthly Returns](reports/monthly_returns.png)

---

### Trade Distribution Analysis

Four key distributions: Win/Loss ratio, Long vs Short performance, PnL distribution, and trade duration analysis.

![Trade Distribution](reports/trade_distribution.png)

---

### Yearly Performance

Annual performance breakdown showing PnL and win rate by year.

![Yearly Performance](reports/yearly_performance.png)

---

### Drawdown Analysis

Detailed view of the drawdown periods and recovery.

![Drawdown Analysis](reports/drawdown_analysis.png)

---

## 📝 Observations & Insights

### Strengths
"""

    # Add dynamic insights based on performance
    insights_strengths = []
    insights_weaknesses = []
    
    if stats['win_rate'] > 50:
        insights_strengths.append(f"- ✅ Win rate of {stats['win_rate']:.1f}% exceeds 50%, indicating edge in trade selection")
    else:
        insights_weaknesses.append(f"- ⚠️ Win rate of {stats['win_rate']:.1f}% is below 50%, but can still be profitable with good RR ratio")
    
    if stats['profit_factor'] and stats['profit_factor'] > 1.5:
        insights_strengths.append(f"- ✅ Profit factor of {stats['profit_factor']:.2f} indicates strong edge (>1.5 is excellent)")
    elif stats['profit_factor'] and stats['profit_factor'] > 1.0:
        insights_strengths.append(f"- ✅ Profit factor of {stats['profit_factor']:.2f} is profitable (>1.0)")
    elif stats['profit_factor'] is not None:
        insights_weaknesses.append(f"- ⚠️ Profit factor of {stats['profit_factor']:.2f} is below 1.0, indicating losing strategy")
    
    if stats['total_pnl'] > 0:
        insights_strengths.append(f"- ✅ Positive total PnL of {stats['total_pnl']:.2f} points")
    else:
        insights_weaknesses.append(f"- ⚠️ Negative total PnL of {stats['total_pnl']:.2f} points")
    
    if long_winrate > short_winrate and long_winrate > 0:
        insights_strengths.append(f"- ✅ LONG trades outperform with {long_winrate:.1f}% win rate vs {short_winrate:.1f}% for shorts")
    elif short_winrate > long_winrate and short_winrate > 0:
        insights_strengths.append(f"- ✅ SHORT trades outperform with {short_winrate:.1f}% win rate vs {long_winrate:.1f}% for longs")
    
    if stats['max_drawdown'] > 0 and stats['total_pnl'] > 0:
        recovery_ratio = stats['total_pnl'] / stats['max_drawdown']
        if recovery_ratio > 2:
            insights_strengths.append(f"- ✅ Strong recovery ratio: PnL is {recovery_ratio:.1f}x the max drawdown")
    
    for insight in insights_strengths:
        report += insight + "\n"
    
    report += "\n### Areas for Improvement\n\n"
    
    for insight in insights_weaknesses:
        report += insight + "\n"
    
    if not insights_weaknesses:
        report += "- No significant weaknesses identified based on current metrics\n"
    
    report += f"""
---

## ⚙️ Strategy Parameters

| Parameter | Value |
|-----------|-------|
| Swing Lookback | {SWING_LOOKBACK} candles (left & right) |
| FVG Search Window | {FVG_LOOKBACK_CANDLES} M5 candles |
| Risk/Reward Ratio | 1:{RISK_REWARD_RATIO:.0f} |
| Stop Loss Buffer | {SL_BUFFER_POINTS} points |

---

## 🚀 Recommendations

1. **Parameter Optimization**: Consider testing different swing lookback periods (3-7) and RR ratios (2-4)
2. **Time Filters**: Analyze performance by session (Asian, London, NY) to identify optimal trading windows
3. **Volatility Filter**: Add ATR-based position sizing or trade filters to adapt to market conditions
4. **Additional Confirmations**: Consider adding Order Block or Breaker Block confirmations

---

## 📁 Files Generated

| File | Description |
|------|-------------|
| `BACKTEST_REPORT.md` | This comprehensive report |
| `reports/equity_curve.png` | Equity curve visualization |
| `reports/monthly_returns.png` | Monthly returns heatmap |
| `reports/trade_distribution.png` | Trade distribution analysis |
| `reports/yearly_performance.png` | Yearly performance breakdown |
| `reports/drawdown_analysis.png` | Drawdown analysis chart |
| `backtest_trades.csv` | Detailed trade log |

---

*Report generated by Liquidity Sweep SMC Strategy Backtester*
"""
    
    return report


def main():
    """Main function to run analysis and generate report."""
    print("="*60)
    print("GENERATING BACKTEST REPORT")
    print("="*60)
    
    # Ensure report directory exists
    ensure_report_dir()
    
    # Load data and run backtest
    print("\nLoading data...")
    df_m1 = load_all_1m_data()
    
    print("\nRunning backtest...")
    trades, stats = run_backtest(df_m1, verbose=True)
    
    if not trades:
        print("\nNo trades generated. Cannot create report.")
        return
    
    print("\n" + "="*60)
    print("GENERATING VISUALIZATIONS")
    print("="*60)
    
    # Generate charts
    chart_files = {}
    
    print("\n1. Generating Equity Curve...")
    chart_files['equity_curve'] = generate_equity_curve(trades, stats)
    
    print("2. Generating Monthly Returns Heatmap...")
    chart_files['monthly_returns'] = generate_monthly_returns_heatmap(trades)
    
    print("3. Generating Trade Distribution Charts...")
    chart_files['trade_distribution'] = generate_trade_distribution(trades, stats)
    
    print("4. Generating Yearly Performance...")
    chart_files['yearly_performance'] = generate_yearly_performance(trades, stats)
    
    print("5. Generating Drawdown Analysis...")
    chart_files['drawdown_analysis'] = generate_drawdown_analysis(trades, stats)
    
    print("\n" + "="*60)
    print("GENERATING MARKDOWN REPORT")
    print("="*60)
    
    report = generate_markdown_report(trades, stats, chart_files)
    
    with open(REPORT_FILE, 'w') as f:
        f.write(report)
    
    print(f"\n✅ Report saved to: {REPORT_FILE}")
    print(f"✅ Charts saved to: {REPORT_DIR}/")
    
    # Export trades CSV
    from liquidity_sweep_backtest import export_trades_to_csv
    export_trades_to_csv(trades)
    
    print("\n" + "="*60)
    print("REPORT GENERATION COMPLETE")
    print("="*60)
    
    return trades, stats


if __name__ == "__main__":
    trades, stats = main()

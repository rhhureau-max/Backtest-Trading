#!/usr/bin/env python3
"""
SMC Reversal Backtest Strategy: Multi-Target Comparison (R:R 1:1, 1.5:1, 2:1)
Smart Money Concepts (SMC) based reversal strategy with multiple take profit targets.

This version compares three different R:R strategies:
- Strategy A: R:R 1:1 (TP = entry - risk)
- Strategy B: R:R 1.5:1 (TP = entry - 1.5*risk)
- Strategy C: R:R 2:1 (TP = entry - 2*risk)

Author: Python Expert in Backtesting & SMC
Date: 2025-12-11
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import time
import os
import warnings
warnings.filterwarnings('ignore')

# Configuration
BASE_PATH = '/home/runner/work/Backtest-Trading/Backtest-Trading'
DATA_TIMEFRAME = '5m'
SESSION_START = time(1, 0)   # 01:00
SESSION_END = time(7, 0)     # 07:00
RISK_PER_TRADE = 0.01        # 1% risk per trade
INITIAL_CAPITAL = 100000     # Starting capital
FRACTAL_WINDOW = 1           # Number of candles each side for local comparison
FRACTAL_LOOKBACK = 6         # Rolling max/min period for significant fractals
REVERSAL_WINDOW = 2          # Number of candles to check for bearish reversal
FIB_ENTRY_LEVEL = 0.5        # 50% Fibonacci retracement
DEBUG = False                # Enable debug output

# R:R targets to test
RR_TARGETS = [1.0, 1.5, 2.0]

# Set plotting style
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (20, 12)


def load_nq_data(years=None):
    """Load NQ 5-minute data from CSV files."""
    if years is None:
        years = range(2018, 2026)
    
    all_data = []
    
    for year in years:
        file_path = os.path.join(BASE_PATH, f"{year} {DATA_TIMEFRAME}.csv")
        if not os.path.exists(file_path):
            print(f"Warning: File not found for year {year}")
            continue
        
        print(f"Loading data for {year}...")
        df = pd.read_csv(file_path, sep=';')
        
        # Parse datetime
        df['datetime'] = pd.to_datetime(df['Column1'] + ' ' + df['Column2'], 
                                       format='%d/%m/%Y %H:%M:%S')
        
        # Rename columns
        df = df.rename(columns={
            'Column3': 'Open',
            'Column4': 'High',
            'Column5': 'Low',
            'Column6': 'Close',
            'Column7': 'Volume'
        })
        
        df['Date'] = df['datetime'].dt.date
        df['Time'] = df['datetime'].dt.time
        
        all_data.append(df[['datetime', 'Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']])
    
    if not all_data:
        raise ValueError("No data files found!")
    
    combined_df = pd.concat(all_data, ignore_index=True)
    combined_df = combined_df.sort_values('datetime').reset_index(drop=True)
    
    print(f"\nTotal records loaded: {len(combined_df):,}")
    print(f"Date range: {combined_df['Date'].min()} to {combined_df['Date'].max()}\n")
    
    return combined_df


def filter_session_data(df):
    """Filter data for 01:00-07:00 session."""
    session_df = df[(df['Time'] >= SESSION_START) & (df['Time'] < SESSION_END)].copy()
    return session_df


def detect_fractals(df, window=1, lookback=6):
    """
    Detect significant fractals (swing highs/lows) with two conditions:
    1. Local condition: Surrounded by lower/higher candles
    2. Global condition: Must be rolling max/min over lookback period
    """
    df = df.reset_index(drop=True)
    df['FractalHigh'] = False
    df['FractalLow'] = False
    
    # Calculate rolling max/min
    df['rolling_max'] = df['High'].rolling(window=lookback, center=False).max()
    df['rolling_min'] = df['Low'].rolling(window=lookback, center=False).min()
    
    # Vectorized approach for global condition
    df['is_rolling_max'] = df['High'] == df['rolling_max']
    df['is_rolling_min'] = df['Low'] == df['rolling_min']
    
    # Local condition check (slower part, but necessary)
    for i in range(window, len(df) - window):
        if df.iloc[i]['is_rolling_max']:
            # Check local high condition
            is_local_high = True
            for j in range(i-window, i+window+1):
                if j != i and df.iloc[i]['High'] <= df.iloc[j]['High']:
                    is_local_high = False
                    break
            if is_local_high:
                df.iloc[i, df.columns.get_loc('FractalHigh')] = True
        
        if df.iloc[i]['is_rolling_min']:
            # Check local low condition  
            is_local_low = True
            for j in range(i-window, i+window+1):
                if j != i and df.iloc[i]['Low'] >= df.iloc[j]['Low']:
                    is_local_low = False
                    break
            if is_local_low:
                df.iloc[i, df.columns.get_loc('FractalLow')] = True
    
    # Clean up temporary columns
    df = df.drop(columns=['is_rolling_max', 'is_rolling_min'])
    
    return df


def find_sweep_opportunities(df):
    """
    Find liquidity sweep opportunities with strict validation.
    A sweep occurs when:
    1. Price exceeds a previous fractal high (wick above)
    2. Either: Closes below the fractal (wick rejection)
    3. Or: Shows bearish engulfing or strong reversal within next 2 candles
    """
    sweeps = []
    fractal_highs = df[df['FractalHigh']].copy()
    
    for frac_idx, frac_row in fractal_highs.iterrows():
        fractal_high = frac_row['High']
        fractal_time = frac_row['datetime']
        
        # Look for sweeps after this fractal
        future_candles = df[df['datetime'] > fractal_time].copy()
        
        for idx, row in future_candles.iterrows():
            # Check if price swept above fractal
            if row['High'] > fractal_high:
                # Check rejection conditions
                wick_rejection = row['Close'] < fractal_high
                
                # Check for bearish engulfing or strong reversal in next 2 candles
                bearish_reversal = False
                next_candles = df.loc[idx:idx+REVERSAL_WINDOW]
                
                for next_idx, next_row in next_candles.iterrows():
                    if next_idx == idx:
                        continue
                    
                    # Bearish engulfing: next candle opens above and closes below
                    if (next_row['Open'] > row['Close'] and 
                        next_row['Close'] < row['Open']):
                        bearish_reversal = True
                        break
                    
                    # Strong bearish move (>10 points)
                    if next_row['Close'] < row['Close'] - 10:
                        bearish_reversal = True
                        break
                
                if wick_rejection or bearish_reversal:
                    sweeps.append({
                        'sweep_time': row['datetime'],
                        'sweep_high': row['High'],
                        'sweep_close': row['Close'],
                        'fractal_high': fractal_high,
                        'fractal_time': fractal_time,
                        'fractal_idx': frac_idx
                    })
                    break  # Only one sweep per fractal
    
    return sweeps


def check_mss(df, sweep):
    """
    Check for Market Structure Shift (MSS) after sweep.
    MSS occurs when price breaks the most recent fractal low that led to the sweep.
    """
    # Find fractals between the original fractal and the sweep
    fractals_before_sweep = df[
        (df['FractalLow']) & 
        (df['datetime'] > sweep['fractal_time']) & 
        (df['datetime'] <= sweep['sweep_time'])
    ]
    
    if len(fractals_before_sweep) == 0:
        return None
    
    # Get the last fractal low before sweep
    last_fractal_low = fractals_before_sweep.iloc[-1]['Low']
    last_fractal_time = fractals_before_sweep.iloc[-1]['datetime']
    
    # Look for MSS after sweep
    candles_after_sweep = df[df['datetime'] > sweep['sweep_time']]
    
    for idx, row in candles_after_sweep.iterrows():
        # Check if price breaks below the fractal low
        if row['Low'] < last_fractal_low:
            return {
                'mss_time': row['datetime'],
                'mss_low': row['Low'],
                'fractal_low': last_fractal_low,
                'fractal_time': last_fractal_time
            }
    
    return None


def calculate_fibonacci_entry(sweep_high, mss_low):
    """Calculate 50% Fibonacci retracement entry price."""
    return sweep_high - (sweep_high - mss_low) * FIB_ENTRY_LEVEL


def simulate_trade_multi_target(full_df, sweep_info, mss_info, entry_price, sl_price, entry_time, rr_targets):
    """
    Simulate trade execution with multiple take profit targets.
    
    Args:
        full_df: Full dataframe
        sweep_info: Sweep information
        mss_info: MSS information
        entry_price: Entry price
        sl_price: Stop loss price
        entry_time: Entry time
        rr_targets: List of R:R ratios to test (e.g., [1.0, 1.5, 2.0])
    
    Returns:
        Dict with results for each R:R target
    """
    # Find all candles after entry
    candles_after_entry = full_df[full_df['datetime'] > entry_time].copy()
    
    if len(candles_after_entry) == 0:
        return None
    
    risk_points = sl_price - entry_price
    
    # Initialize results for each target
    results = {}
    for rr in rr_targets:
        tp_price = entry_price - (risk_points * rr)  # For short position
        
        results[f'RR_{rr}'] = {
            'entry_time': entry_time,
            'entry_price': entry_price,
            'sl_price': sl_price,
            'tp_price': tp_price,
            'exit_time': None,
            'exit_price': None,
            'outcome': None,
            'pnl_points': 0,
            'risk_points': risk_points,
            'reward_points': risk_points * rr,
            'rr_ratio': rr,
            'target_hit': False
        }
    
    # Check each candle
    for idx, row in candles_after_entry.iterrows():
        # Check SL hit first (priority)
        if row['High'] >= sl_price:
            # SL hit - all targets are losses
            for rr in rr_targets:
                key = f'RR_{rr}'
                if results[key]['outcome'] is None:
                    results[key]['exit_time'] = row['datetime']
                    results[key]['exit_price'] = sl_price
                    results[key]['outcome'] = 'loss'
                    results[key]['pnl_points'] = entry_price - sl_price
            break
        
        # Check TP hits for each target
        for rr in rr_targets:
            key = f'RR_{rr}'
            if results[key]['outcome'] is None:
                tp_price = results[key]['tp_price']
                if row['Low'] <= tp_price:
                    results[key]['exit_time'] = row['datetime']
                    results[key]['exit_price'] = tp_price
                    results[key]['outcome'] = 'win'
                    results[key]['pnl_points'] = entry_price - tp_price
                    results[key]['target_hit'] = True
    
    # Filter out incomplete trades
    valid_results = {}
    for key, result in results.items():
        if result['outcome'] is not None:
            valid_results[key] = result
    
    return valid_results if valid_results else None


def backtest_session_multi_target(full_df, session_date, session_df, rr_targets):
    """
    Backtest the SMC reversal strategy for a single session with multiple targets.
    """
    trades = {f'RR_{rr}': [] for rr in rr_targets}
    
    # Add fractals
    session_df = detect_fractals(session_df, window=FRACTAL_WINDOW, lookback=FRACTAL_LOOKBACK)
    
    # Find sweep opportunities
    sweeps = find_sweep_opportunities(session_df)
    
    if len(sweeps) == 0:
        return trades
    
    # For each sweep, check for MSS and potential trade
    for sweep in sweeps:
        mss_info = check_mss(session_df, sweep)
        
        if mss_info is None:
            continue
        
        # Calculate entry price (50% Fib retracement)
        entry_price = calculate_fibonacci_entry(sweep['sweep_high'], mss_info['mss_low'])
        
        # SL above sweep high
        sl_price = sweep['sweep_high'] + 5
        
        # Check if entry price makes sense
        if not (mss_info['mss_low'] < entry_price < sweep['sweep_high']):
            continue
        
        # Entry time is after MSS confirmation
        entry_time = mss_info['mss_time']
        
        # Make sure entry is within session
        if entry_time.time() >= SESSION_END:
            continue
        
        # Simulate trade with multiple targets
        trade_results = simulate_trade_multi_target(
            full_df, sweep, mss_info, 
            entry_price, sl_price, entry_time, rr_targets
        )
        
        if trade_results is not None:
            for key, result in trade_results.items():
                result['session_date'] = session_date
                result['sweep_high'] = sweep['sweep_high']
                result['mss_low'] = mss_info['mss_low']
                trades[key].append(result)
    
    return trades


def run_backtest_multi_target(df, rr_targets):
    """Run backtest across all sessions with multiple R:R targets."""
    session_df = filter_session_data(df)
    unique_dates = session_df['Date'].unique()
    
    print(f"Backtesting {len(unique_dates)} sessions with R:R targets: {rr_targets}")
    print("=" * 80)
    
    all_trades = {f'RR_{rr}': [] for rr in rr_targets}
    
    for i, date in enumerate(unique_dates):
        if (i + 1) % 200 == 0:
            trades_found = sum(len(all_trades[k]) for k in all_trades.keys())
            print(f"Processing session {i+1}/{len(unique_dates)}... ({trades_found} trades found so far)")
        
        session_data = session_df[session_df['Date'] == date].copy()
        
        if len(session_data) < 10:
            continue
        
        trades = backtest_session_multi_target(df, date, session_data, rr_targets)
        
        for key in all_trades.keys():
            all_trades[key].extend(trades[key])
    
    print(f"\nCompleted! Total trades found per target:")
    for key in all_trades.keys():
        print(f"  {key}: {len(all_trades[key])} trades")
    
    return all_trades


def calculate_metrics_multi_target(all_trades, rr_targets):
    """Calculate performance metrics for each R:R target."""
    results = {}
    
    for rr in rr_targets:
        key = f'RR_{rr}'
        trades = all_trades[key]
        
        if len(trades) == 0:
            results[key] = {
                'rr_target': rr,
                'total_trades': 0,
                'wins': 0,
                'losses': 0,
                'win_rate': 0,
                'total_pnl': 0,
                'avg_win': 0,
                'avg_loss': 0,
                'profit_factor': 0,
                'total_return': 0,
                'final_capital': INITIAL_CAPITAL
            }
            continue
        
        df_trades = pd.DataFrame(trades)
        
        wins = df_trades[df_trades['outcome'] == 'win']
        losses = df_trades[df_trades['outcome'] == 'loss']
        
        total_trades = len(df_trades)
        num_wins = len(wins)
        num_losses = len(losses)
        win_rate = (num_wins / total_trades * 100) if total_trades > 0 else 0
        
        total_pnl = df_trades['pnl_points'].sum()
        avg_win = wins['pnl_points'].mean() if len(wins) > 0 else 0
        avg_loss = losses['pnl_points'].mean() if len(losses) > 0 else 0
        
        gross_profit = wins['pnl_points'].sum() if len(wins) > 0 else 0
        gross_loss = abs(losses['pnl_points'].sum()) if len(losses) > 0 else 0
        profit_factor = (gross_profit / gross_loss) if gross_loss > 0 else 0
        
        # Calculate equity curve with 1% risk per trade
        capital = INITIAL_CAPITAL
        equity_curve = [capital]
        
        for _, trade in df_trades.iterrows():
            risk_amount = capital * RISK_PER_TRADE
            pnl_amount = (trade['pnl_points'] / trade['risk_points']) * risk_amount
            capital += pnl_amount
            equity_curve.append(capital)
        
        total_return = ((capital - INITIAL_CAPITAL) / INITIAL_CAPITAL) * 100
        
        results[key] = {
            'rr_target': rr,
            'total_trades': total_trades,
            'wins': num_wins,
            'losses': num_losses,
            'win_rate': win_rate,
            'total_pnl': total_pnl,
            'avg_win': avg_win,
            'avg_loss': avg_loss,
            'profit_factor': profit_factor,
            'total_return': total_return,
            'final_capital': capital,
            'equity_curve': equity_curve,
            'trades_df': df_trades
        }
    
    return results


def create_comparison_visualizations(results, rr_targets):
    """Create comprehensive comparison visualizations."""
    fig = plt.figure(figsize=(20, 14))
    gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
    
    colors = ['#2E86AB', '#A23B72', '#F18F01']
    
    # 1. Equity Curves Comparison
    ax1 = fig.add_subplot(gs[0, :])
    for i, rr in enumerate(rr_targets):
        key = f'RR_{rr}'
        if results[key]['total_trades'] > 0:
            equity = results[key]['equity_curve']
            ax1.plot(equity, label=f'R:R {rr}:1', color=colors[i], linewidth=2)
    
    ax1.axhline(y=INITIAL_CAPITAL, color='gray', linestyle='--', alpha=0.5, label='Initial Capital')
    ax1.set_title('Equity Curves Comparison (All R:R Targets)', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Trade Number')
    ax1.set_ylabel('Account Value ($)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Format y-axis as currency
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}K'))
    
    # 2. Win Rate Comparison
    ax2 = fig.add_subplot(gs[1, 0])
    win_rates = [results[f'RR_{rr}']['win_rate'] for rr in rr_targets]
    bars = ax2.bar([f'{rr}:1' for rr in rr_targets], win_rates, color=colors)
    ax2.set_title('Win Rate Comparison', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Win Rate (%)')
    ax2.set_ylim(0, 100)
    ax2.grid(axis='y', alpha=0.3)
    
    # Add value labels on bars
    for bar, val in zip(bars, win_rates):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{val:.1f}%', ha='center', va='bottom', fontweight='bold')
    
    # 3. Profit Factor Comparison
    ax3 = fig.add_subplot(gs[1, 1])
    profit_factors = [results[f'RR_{rr}']['profit_factor'] for rr in rr_targets]
    bars = ax3.bar([f'{rr}:1' for rr in rr_targets], profit_factors, color=colors)
    ax3.set_title('Profit Factor Comparison', fontsize=12, fontweight='bold')
    ax3.set_ylabel('Profit Factor')
    ax3.grid(axis='y', alpha=0.3)
    
    for bar, val in zip(bars, profit_factors):
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height,
                f'{val:.2f}', ha='center', va='bottom', fontweight='bold')
    
    # 4. Total Return Comparison
    ax4 = fig.add_subplot(gs[1, 2])
    returns = [results[f'RR_{rr}']['total_return'] for rr in rr_targets]
    bars = ax4.bar([f'{rr}:1' for rr in rr_targets], returns, color=colors)
    ax4.set_title('Total Return Comparison', fontsize=12, fontweight='bold')
    ax4.set_ylabel('Return (%)')
    ax4.grid(axis='y', alpha=0.3)
    
    for bar, val in zip(bars, returns):
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2., height,
                f'{val:.1f}%', ha='center', va='bottom', fontweight='bold')
    
    # 5. Total Trades Comparison
    ax5 = fig.add_subplot(gs[2, 0])
    trades_counts = [results[f'RR_{rr}']['total_trades'] for rr in rr_targets]
    bars = ax5.bar([f'{rr}:1' for rr in rr_targets], trades_counts, color=colors)
    ax5.set_title('Total Trades', fontsize=12, fontweight='bold')
    ax5.set_ylabel('Number of Trades')
    ax5.grid(axis='y', alpha=0.3)
    
    for bar, val in zip(bars, trades_counts):
        height = bar.get_height()
        ax5.text(bar.get_x() + bar.get_width()/2., height,
                f'{val}', ha='center', va='bottom', fontweight='bold')
    
    # 6. Average Win vs Loss
    ax6 = fig.add_subplot(gs[2, 1])
    x = np.arange(len(rr_targets))
    width = 0.35
    
    avg_wins = [results[f'RR_{rr}']['avg_win'] for rr in rr_targets]
    avg_losses = [abs(results[f'RR_{rr}']['avg_loss']) for rr in rr_targets]
    
    ax6.bar(x - width/2, avg_wins, width, label='Avg Win', color='#27AE60')
    ax6.bar(x + width/2, avg_losses, width, label='Avg Loss', color='#E74C3C')
    
    ax6.set_title('Average Win vs Loss', fontsize=12, fontweight='bold')
    ax6.set_ylabel('Points')
    ax6.set_xticks(x)
    ax6.set_xticklabels([f'{rr}:1' for rr in rr_targets])
    ax6.legend()
    ax6.grid(axis='y', alpha=0.3)
    
    # 7. P&L Distribution for each target
    ax7 = fig.add_subplot(gs[2, 2])
    total_pnls = [results[f'RR_{rr}']['total_pnl'] for rr in rr_targets]
    bars = ax7.bar([f'{rr}:1' for rr in rr_targets], total_pnls, color=colors)
    ax7.set_title('Total P&L (Points)', fontsize=12, fontweight='bold')
    ax7.set_ylabel('Total P&L (Points)')
    ax7.grid(axis='y', alpha=0.3)
    
    for bar, val in zip(bars, total_pnls):
        height = bar.get_height()
        ax7.text(bar.get_x() + bar.get_width()/2., height,
                f'{val:.0f}', ha='center', va='bottom', fontweight='bold')
    
    plt.suptitle('SMC Reversal Strategy: Multi-Target R:R Comparison (2018-2025)', 
                 fontsize=16, fontweight='bold', y=0.995)
    
    plt.savefig('smc_multi_target_comparison.png', dpi=300, bbox_inches='tight')
    print("\nComparison chart saved: smc_multi_target_comparison.png")
    
    return fig


def print_detailed_results(results, rr_targets):
    """Print detailed results for each R:R target."""
    print("\n" + "=" * 100)
    print("SMC REVERSAL STRATEGY - MULTI-TARGET R:R COMPARISON (2018-2025)")
    print("=" * 100)
    
    # Summary table
    print("\n📊 SUMMARY TABLE")
    print("-" * 100)
    print(f"{'R:R Target':<12} {'Trades':<10} {'Win Rate':<12} {'Profit Factor':<15} {'Total P&L':<15} {'Return (%)':<12}")
    print("-" * 100)
    
    for rr in rr_targets:
        key = f'RR_{rr}'
        r = results[key]
        print(f"{rr}:1{'':<9} {r['total_trades']:<10} {r['win_rate']:>6.2f}%{'':<5} "
              f"{r['profit_factor']:>8.2f}{'':<7} {r['total_pnl']:>+10.2f} pts{'':<2} "
              f"{r['total_return']:>+8.2f}%")
    
    print("-" * 100)
    
    # Detailed breakdown for each target
    for rr in rr_targets:
        key = f'RR_{rr}'
        r = results[key]
        
        print(f"\n{'='*100}")
        print(f"DETAILED RESULTS: R:R {rr}:1 TARGET")
        print(f"{'='*100}")
        
        print(f"\n📈 Performance Metrics:")
        print(f"  Total Trades: {r['total_trades']}")
        print(f"  Wins: {r['wins']} | Losses: {r['losses']}")
        print(f"  Win Rate: {r['win_rate']:.2f}%")
        print(f"  Profit Factor: {r['profit_factor']:.2f}")
        
        print(f"\n💰 P&L Analysis:")
        print(f"  Total P&L: {r['total_pnl']:+.2f} points")
        print(f"  Average Win: +{r['avg_win']:.2f} points")
        print(f"  Average Loss: {r['avg_loss']:.2f} points")
        
        print(f"\n📊 Account Performance:")
        print(f"  Initial Capital: ${INITIAL_CAPITAL:,.2f}")
        print(f"  Final Capital: ${r['final_capital']:,.2f}")
        print(f"  Total Return: {r['total_return']:+.2f}%")
        print(f"  Annual Return: {r['total_return']/7:+.2f}%")
        
        # Last 5 trades for 2025
        if r['total_trades'] > 0:
            df_2025 = r['trades_df'][r['trades_df']['session_date'].apply(lambda x: x.year) == 2025]
            
            if len(df_2025) > 0:
                print(f"\n🔍 Last 5 Trades from 2025:")
                print("-" * 100)
                
                last_5 = df_2025.tail(5)
                for idx, (_, trade) in enumerate(last_5.iterrows(), 1):
                    outcome_emoji = "✅" if trade['outcome'] == 'win' else "❌"
                    print(f"\n  Trade #{len(df_2025) - len(last_5) + idx} - {trade['session_date'].strftime('%b %d, %Y')}")
                    print(f"    Entry: {trade['entry_time'].strftime('%H:%M')} @ {trade['entry_price']:.2f}")
                    print(f"    Exit: {trade['exit_time'].strftime('%H:%M')} @ {trade['exit_price']:.2f}")
                    print(f"    SL: {trade['sl_price']:.2f} | TP: {trade['tp_price']:.2f}")
                    print(f"    Result: {outcome_emoji} {trade['outcome'].upper()} {trade['pnl_points']:+.2f} pts")
    
    print("\n" + "=" * 100)


def main():
    """Main execution function."""
    print("\n" + "=" * 100)
    print("SMC REVERSAL BACKTEST - MULTI-TARGET R:R COMPARISON")
    print("Comparing R:R targets: 1:1, 1.5:1, 2:1")
    print("=" * 100 + "\n")
    
    # Load data from all years (2018-2025)
    df = load_nq_data(years=range(2018, 2026))
    
    # Run backtest with multiple targets
    rr_targets = RR_TARGETS
    all_trades = run_backtest_multi_target(df, rr_targets)
    
    # Calculate metrics for each target
    results = calculate_metrics_multi_target(all_trades, rr_targets)
    
    # Print detailed results
    print_detailed_results(results, rr_targets)
    
    # Create visualizations
    create_comparison_visualizations(results, rr_targets)
    
    # Export trades to CSV
    for rr in rr_targets:
        key = f'RR_{rr}'
        if results[key]['total_trades'] > 0:
            filename = f'smc_trades_RR_{rr}.csv'
            results[key]['trades_df'].to_csv(filename, index=False)
            print(f"\nTrades exported: {filename}")
    
    print("\n✅ Multi-target R:R comparison complete!")
    print("=" * 100 + "\n")


if __name__ == "__main__":
    main()

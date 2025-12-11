#!/usr/bin/env python3
"""
SMC Reversal Strategy: SL/TP Optimization Matrix
Comprehensive testing of 7 SL types × 4 TP types = 28 configurations

SL Configurations:
1. Swing_High + 1 pt
2. Swing_High + 5 pts
3. Fixed 10 pts
4. Fixed 20 pts
5. Fib 89% retracement
6. ATR 1.5x
7. ATR 2.0x

TP Configurations:
1. FVG (current strategy)
2. R:R 1.0
3. R:R 1.5
4. R:R 2.0

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
SESSION_START = time(1, 0)
SESSION_END = time(7, 0)
RISK_PER_TRADE = 0.01
INITIAL_CAPITAL = 100000
FRACTAL_WINDOW = 1
FRACTAL_LOOKBACK = 6
REVERSAL_WINDOW = 2
FIB_ENTRY_LEVEL = 0.5
MIN_FVG_SIZE = 5
DEBUG = False

# SL and TP configurations to test
SL_CONFIGS = [
    "Swing_High+1",
    "Swing_High+5",
    "Fixed_10pts",
    "Fixed_20pts",
    "Fib_89%",
    "ATR_1.5x",
    "ATR_2.0x"
]

TP_CONFIGS = ["FVG", "RR_1.0", "RR_1.5", "RR_2.0"]

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
        
        df['datetime'] = pd.to_datetime(df['Column1'] + ' ' + df['Column2'], 
                                       format='%d/%m/%Y %H:%M:%S')
        
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
    
    # Calculate ATR for ATR-based SL
    combined_df['TR'] = np.maximum(
        combined_df['High'] - combined_df['Low'],
        np.maximum(
            abs(combined_df['High'] - combined_df['Close'].shift(1)),
            abs(combined_df['Low'] - combined_df['Close'].shift(1))
        )
    )
    combined_df['ATR_14'] = combined_df['TR'].rolling(window=14).mean()
    
    print(f"\nTotal candles loaded: {len(combined_df):,}")
    print(f"Date range: {combined_df['datetime'].min()} to {combined_df['datetime'].max()}")
    
    return combined_df


def filter_session_data(df):
    """Filter data for 01:00-07:00 session."""
    session_mask = (df['Time'] >= SESSION_START) & (df['Time'] <= SESSION_END)
    return df[session_mask].copy()


def detect_fractals(df, window=FRACTAL_WINDOW, lookback=FRACTAL_LOOKBACK):
    """
    Detect significant fractals:
    1. Local condition: Surrounded by lower/higher candles
    2. Global condition: Highest/lowest in lookback period (rolling max/min)
    """
    df = df.copy().reset_index(drop=True)
    
    # Local condition: surrounded by lower/higher candles
    df['fractal_high_local'] = False
    df['fractal_low_local'] = False
    
    for i in range(window, len(df) - window):
        # Check if surrounded by lower highs
        if all(df.iloc[i]['High'] > df.iloc[i-j]['High'] for j in range(1, window+1)) and \
           all(df.iloc[i]['High'] > df.iloc[i+j]['High'] for j in range(1, window+1)):
            df.loc[i, 'fractal_high_local'] = True
        
        # Check if surrounded by higher lows
        if all(df.iloc[i]['Low'] < df.iloc[i-j]['Low'] for j in range(1, window+1)) and \
           all(df.iloc[i]['Low'] < df.iloc[i+j]['Low'] for j in range(1, window+1)):
            df.loc[i, 'fractal_low_local'] = True
    
    # Global condition: rolling max/min
    df['rolling_high'] = df['High'].rolling(window=lookback, center=False).max()
    df['rolling_low'] = df['Low'].rolling(window=lookback, center=False).min()
    
    # Combine conditions
    df['fractal_high'] = df['fractal_high_local'] & (df['High'] == df['rolling_high'])
    df['fractal_low'] = df['fractal_low_local'] & (df['Low'] == df['rolling_low'])
    
    return df


def detect_sweeps(df, reversal_window=REVERSAL_WINDOW):
    """
    Detect liquidity sweeps with strict validation:
    - Price exceeds fractal high (wick above)
    - Closes below fractal (wick rejection) OR
    - Bearish engulfing/strong reversal within reversal_window candles
    """
    sweeps = []
    fractal_highs = df[df['fractal_high']].copy()
    
    for idx, fractal_row in fractal_highs.iterrows():
        fractal_high = fractal_row['High']
        fractal_time = fractal_row['datetime']
        
        # Look for sweep in subsequent candles
        future_data = df[df['datetime'] > fractal_time].head(50)
        
        for sweep_idx, sweep_row in future_data.iterrows():
            # Check if price exceeded fractal high
            if sweep_row['High'] > fractal_high:
                # Validation 1: Close below fractal (wick rejection)
                if sweep_row['Close'] < fractal_high:
                    sweeps.append({
                        'fractal_idx': idx,
                        'fractal_high': fractal_high,
                        'sweep_idx': sweep_idx,
                        'sweep_high': sweep_row['High'],
                        'sweep_time': sweep_row['datetime']
                    })
                    break
                
                # Validation 2: Bearish engulfing or strong reversal in next reversal_window candles
                next_candles = df.loc[sweep_idx:sweep_idx+reversal_window]
                
                for check_idx, check_row in next_candles.iterrows():
                    if check_idx == sweep_idx:
                        continue
                    
                    # Bearish engulfing: Close below previous open and lower by >10 points
                    if check_row['Close'] < sweep_row['Open'] and \
                       (sweep_row['Close'] - check_row['Close']) > 10:
                        sweeps.append({
                            'fractal_idx': idx,
                            'fractal_high': fractal_high,
                            'sweep_idx': sweep_idx,
                            'sweep_high': sweep_row['High'],
                            'sweep_time': sweep_row['datetime']
                        })
                        break
                else:
                    continue
                break
    
    return pd.DataFrame(sweeps)


def confirm_mss(df, sweep_info):
    """Confirm Market Structure Shift (break of previous swing low)."""
    mss_confirmations = []
    
    for _, sweep in sweep_info.iterrows():
        sweep_idx = sweep['sweep_idx']
        sweep_time = sweep['sweep_time']
        
        # Find fractal lows before the sweep
        prior_lows = df[(df['fractal_low'] == True) & (df['datetime'] < sweep_time)]
        
        if len(prior_lows) == 0:
            continue
        
        # Get the most recent fractal low before sweep
        last_fractal_low = prior_lows.iloc[-1]
        fractal_low_level = last_fractal_low['Low']
        
        # Check if price breaks below this fractal low after sweep
        future_data = df[df['datetime'] > sweep_time].head(50)
        
        for mss_idx, mss_row in future_data.iterrows():
            if mss_row['Low'] < fractal_low_level:
                mss_confirmations.append({
                    'sweep_idx': sweep_idx,
                    'sweep_high': sweep['sweep_high'],
                    'sweep_time': sweep_time,
                    'mss_idx': mss_idx,
                    'mss_low': mss_row['Low'],
                    'mss_time': mss_row['datetime'],
                    'fractal_low': fractal_low_level
                })
                break
    
    return pd.DataFrame(mss_confirmations)


def detect_fvg(df, mss_start_idx, mss_end_idx, min_size=MIN_FVG_SIZE):
    """Detect Fair Value Gaps during MSS leg."""
    mss_data = df.loc[mss_start_idx:mss_end_idx]
    
    for i in range(len(mss_data) - 2):
        idx_n = mss_data.index[i]
        idx_n2 = mss_data.index[i + 2]
        
        low_n = mss_data.loc[idx_n, 'Low']
        high_n2 = mss_data.loc[idx_n2, 'High']
        
        # Bearish FVG: gap between Low[n] and High[n+2]
        if low_n > high_n2:
            fvg_size = low_n - high_n2
            if fvg_size >= min_size:
                return {
                    'fvg_top': low_n,
                    'fvg_bottom': high_n2,
                    'fvg_size': fvg_size
                }
    
    return None


def calculate_stop_loss(sweep_high, entry_price, sl_config, atr_value, mss_low):
    """
    Calculate stop loss based on configuration.
    
    Args:
        sweep_high: The high of the sweep
        entry_price: Entry price
        sl_config: SL configuration string
        atr_value: Current ATR value
        mss_low: MSS low price (for Fib 89% calculation)
    
    Returns:
        Stop loss price
    """
    if sl_config == "Swing_High+1":
        return sweep_high + 1
    elif sl_config == "Swing_High+5":
        return sweep_high + 5
    elif sl_config == "Fixed_10pts":
        return entry_price + 10
    elif sl_config == "Fixed_20pts":
        return entry_price + 20
    elif sl_config == "Fib_89%":
        # 89% retracement from MSS low to sweep high
        fib_89_level = mss_low + 0.89 * (sweep_high - mss_low)
        return fib_89_level + 5  # Add 5 pt buffer
    elif sl_config == "ATR_1.5x":
        return entry_price + (1.5 * atr_value)
    elif sl_config == "ATR_2.0x":
        return entry_price + (2.0 * atr_value)
    else:
        # Default: Swing High + 5
        return sweep_high + 5


def calculate_take_profit(entry_price, stop_loss, tp_config, fvg_target=None):
    """
    Calculate take profit based on configuration.
    
    Args:
        entry_price: Entry price
        stop_loss: Stop loss price
        tp_config: TP configuration string
        fvg_target: FVG target price (if available)
    
    Returns:
        Take profit price
    """
    risk = stop_loss - entry_price
    
    if tp_config == "FVG" and fvg_target is not None:
        return fvg_target
    elif tp_config == "RR_1.0":
        return entry_price - (1.0 * risk)
    elif tp_config == "RR_1.5":
        return entry_price - (1.5 * risk)
    elif tp_config == "RR_2.0":
        return entry_price - (2.0 * risk)
    else:
        # Default: RR 1.0
        return entry_price - (1.0 * risk)


def simulate_trade(df, setup, sl_config, tp_config):
    """
    Simulate trade execution with given SL/TP configuration.
    
    Returns:
        Trade result dictionary or None if trade not valid
    """
    sweep_high = setup['sweep_high']
    sweep_idx = setup['sweep_idx']
    sweep_time = setup['sweep_time']
    mss_low = setup['mss_low']
    mss_idx = setup['mss_idx']
    mss_time = setup['mss_time']
    
    # Calculate entry price (50% Fibonacci)
    entry_price = sweep_high - FIB_ENTRY_LEVEL * (sweep_high - mss_low)
    
    # Get ATR at entry
    entry_row = df.loc[mss_idx]
    atr_value = entry_row['ATR_14']
    
    if pd.isna(atr_value):
        atr_value = 50  # Default ATR if not available
    
    # Detect FVG (for FVG TP configuration)
    fvg_info = detect_fvg(df, sweep_idx, mss_idx)
    fvg_target = fvg_info['fvg_bottom'] if fvg_info else None
    
    # Calculate SL and TP
    stop_loss = calculate_stop_loss(sweep_high, entry_price, sl_config, atr_value, mss_low)
    take_profit = calculate_take_profit(entry_price, stop_loss, tp_config, fvg_target)
    
    # Validate setup
    risk = stop_loss - entry_price
    reward = entry_price - take_profit
    
    if risk <= 0 or reward <= 0:
        return None
    
    rr_ratio = reward / risk
    
    # Check if entry happened within session (01:00-07:00)
    if entry_row['Time'] < SESSION_START or entry_row['Time'] > SESSION_END:
        return None
    
    # Simulate price movement after entry
    future_data = df[df['datetime'] > mss_time].head(200)
    
    exit_price = None
    exit_time = None
    exit_reason = None
    
    for idx, row in future_data.iterrows():
        # Check SL hit
        if row['High'] >= stop_loss:
            exit_price = stop_loss
            exit_time = row['datetime']
            exit_reason = 'SL'
            break
        
        # Check TP hit
        if row['Low'] <= take_profit:
            exit_price = take_profit
            exit_time = row['datetime']
            exit_reason = 'TP'
            break
    
    # If no exit, consider it a loss (didn't reach target)
    if exit_price is None:
        exit_price = stop_loss
        exit_time = future_data.iloc[-1]['datetime'] if len(future_data) > 0 else mss_time
        exit_reason = 'Timeout'
    
    # Calculate P&L
    pnl = entry_price - exit_price
    win = 1 if exit_reason == 'TP' else 0
    
    return {
        'date': sweep_time.date(),
        'entry_time': mss_time,
        'entry_price': entry_price,
        'stop_loss': stop_loss,
        'take_profit': take_profit,
        'exit_price': exit_price,
        'exit_time': exit_time,
        'exit_reason': exit_reason,
        'sweep_high': sweep_high,
        'mss_low': mss_low,
        'pnl': pnl,
        'risk': risk,
        'reward': reward,
        'rr_ratio': rr_ratio,
        'win': win,
        'sl_config': sl_config,
        'tp_config': tp_config,
        'atr': atr_value,
        'has_fvg': fvg_target is not None
    }


def run_backtest_for_config(df, sl_config, tp_config):
    """Run complete backtest for a specific SL/TP configuration."""
    print(f"\n{'='*80}")
    print(f"Testing Configuration: SL={sl_config}, TP={tp_config}")
    print(f"{'='*80}")
    
    # Filter session data
    session_df = filter_session_data(df)
    print(f"Session candles (01:00-07:00): {len(session_df):,}")
    
    # Detect fractals
    session_df = detect_fractals(session_df)
    fractal_high_count = session_df['fractal_high'].sum()
    print(f"Fractal highs detected: {fractal_high_count}")
    
    # Detect sweeps
    sweeps_df = detect_sweeps(session_df)
    print(f"Liquidity sweeps detected: {len(sweeps_df)}")
    
    if len(sweeps_df) == 0:
        return None
    
    # Confirm MSS
    mss_df = confirm_mss(session_df, sweeps_df)
    print(f"MSS confirmations: {len(mss_df)}")
    
    if len(mss_df) == 0:
        return None
    
    # Simulate trades
    trades = []
    for _, setup in mss_df.iterrows():
        trade = simulate_trade(session_df, setup, sl_config, tp_config)
        if trade:
            trades.append(trade)
    
    if not trades:
        return None
    
    trades_df = pd.DataFrame(trades)
    
    # Calculate metrics
    total_trades = len(trades_df)
    wins = trades_df['win'].sum()
    losses = total_trades - wins
    win_rate = (wins / total_trades * 100) if total_trades > 0 else 0
    
    total_pnl = trades_df['pnl'].sum()
    avg_win = trades_df[trades_df['win'] == 1]['pnl'].mean() if wins > 0 else 0
    avg_loss = trades_df[trades_df['win'] == 0]['pnl'].mean() if losses > 0 else 0
    
    gross_profit = trades_df[trades_df['win'] == 1]['pnl'].sum() if wins > 0 else 0
    gross_loss = abs(trades_df[trades_df['win'] == 0]['pnl'].sum()) if losses > 0 else 0
    profit_factor = (gross_profit / gross_loss) if gross_loss > 0 else 0
    
    avg_rr = trades_df['rr_ratio'].mean()
    
    # Calculate equity curve with risk management
    trades_df = trades_df.sort_values('entry_time').reset_index(drop=True)
    equity = INITIAL_CAPITAL
    equity_curve = [equity]
    
    for _, trade in trades_df.iterrows():
        risk_amount = equity * RISK_PER_TRADE
        position_size = risk_amount / trade['risk']
        trade_pnl = trade['pnl'] * position_size
        equity += trade_pnl
        equity_curve.append(equity)
    
    trades_df['equity'] = equity_curve[1:]
    final_return = ((equity - INITIAL_CAPITAL) / INITIAL_CAPITAL) * 100
    
    # Print summary
    print(f"\n--- Results Summary ---")
    print(f"Total Trades: {total_trades}")
    print(f"Wins: {wins} | Losses: {losses}")
    print(f"Win Rate: {win_rate:.2f}%")
    print(f"Profit Factor: {profit_factor:.2f}")
    print(f"Total P&L: {total_pnl:+.2f} points")
    print(f"Avg Win: {avg_win:+.2f} pts | Avg Loss: {avg_loss:+.2f} pts")
    print(f"Avg R:R: {avg_rr:.2f}:1")
    print(f"Final Return: {final_return:+.2f}%")
    
    return {
        'sl_config': sl_config,
        'tp_config': tp_config,
        'total_trades': total_trades,
        'wins': wins,
        'losses': losses,
        'win_rate': win_rate,
        'profit_factor': profit_factor,
        'total_pnl': total_pnl,
        'avg_win': avg_win,
        'avg_loss': avg_loss,
        'avg_rr': avg_rr,
        'final_return': final_return,
        'final_equity': equity,
        'trades_df': trades_df
    }


def run_optimization():
    """Run optimization across all SL/TP configurations."""
    print("="*80)
    print("SMC REVERSAL STRATEGY: SL/TP OPTIMIZATION MATRIX")
    print("Testing 7 SL Types × 4 TP Types = 28 Configurations")
    print("="*80)
    
    # Load data
    df = load_nq_data()
    
    # Run all configurations
    results = []
    all_trades = {}
    
    for sl_config in SL_CONFIGS:
        for tp_config in TP_CONFIGS:
            result = run_backtest_for_config(df, sl_config, tp_config)
            if result:
                results.append(result)
                config_key = f"{sl_config}_{tp_config}"
                all_trades[config_key] = result['trades_df']
    
    if not results:
        print("\nNo valid results generated!")
        return
    
    # Create summary dataframe
    summary_df = pd.DataFrame([{k: v for k, v in r.items() if k != 'trades_df'} for r in results])
    
    # Sort by profit factor
    summary_df = summary_df.sort_values('profit_factor', ascending=False)
    
    # Save results
    summary_df.to_csv(os.path.join(BASE_PATH, 'sl_tp_optimization_summary.csv'), index=False)
    
    # Save detailed trades for top 5 configurations
    top_5 = summary_df.head(5)
    for _, row in top_5.iterrows():
        config_key = f"{row['sl_config']}_{row['tp_config']}"
        if config_key in all_trades:
            filename = f"trades_{row['sl_config']}_{row['tp_config']}.csv"
            all_trades[config_key].to_csv(os.path.join(BASE_PATH, filename), index=False)
    
    # Generate visualizations
    generate_optimization_charts(summary_df, results)
    
    # Print final summary
    print("\n" + "="*80)
    print("OPTIMIZATION COMPLETE - TOP 10 CONFIGURATIONS")
    print("="*80)
    print(summary_df.head(10).to_string(index=False))
    
    # Best overall
    best = summary_df.iloc[0]
    print(f"\n{'='*80}")
    print("🏆 BEST CONFIGURATION:")
    print(f"{'='*80}")
    print(f"SL: {best['sl_config']}")
    print(f"TP: {best['tp_config']}")
    print(f"Win Rate: {best['win_rate']:.2f}%")
    print(f"Profit Factor: {best['profit_factor']:.2f}")
    print(f"Total Return: {best['final_return']:+.2f}%")
    print(f"Avg R:R: {best['avg_rr']:.2f}:1")
    
    return summary_df, results


def generate_optimization_charts(summary_df, results):
    """Generate comprehensive visualization charts."""
    fig = plt.figure(figsize=(20, 16))
    
    # 1. Heatmap: Profit Factor by SL/TP
    ax1 = plt.subplot(3, 3, 1)
    pivot_pf = summary_df.pivot_table(values='profit_factor', 
                                       index='sl_config', 
                                       columns='tp_config',
                                       aggfunc='mean')
    sns.heatmap(pivot_pf, annot=True, fmt='.2f', cmap='RdYlGn', center=1.0, ax=ax1)
    ax1.set_title('Profit Factor by Configuration', fontsize=14, fontweight='bold')
    
    # 2. Heatmap: Win Rate by SL/TP
    ax2 = plt.subplot(3, 3, 2)
    pivot_wr = summary_df.pivot_table(values='win_rate', 
                                       index='sl_config', 
                                       columns='tp_config',
                                       aggfunc='mean')
    sns.heatmap(pivot_wr, annot=True, fmt='.1f', cmap='RdYlGn', center=70, ax=ax2)
    ax2.set_title('Win Rate (%) by Configuration', fontsize=14, fontweight='bold')
    
    # 3. Heatmap: Total Return by SL/TP
    ax3 = plt.subplot(3, 3, 3)
    pivot_ret = summary_df.pivot_table(values='final_return', 
                                        index='sl_config', 
                                        columns='tp_config',
                                        aggfunc='mean')
    sns.heatmap(pivot_ret, annot=True, fmt='.1f', cmap='RdYlGn', center=0, ax=ax3)
    ax3.set_title('Total Return (%) by Configuration', fontsize=14, fontweight='bold')
    
    # 4. Scatter: Win Rate vs Profit Factor
    ax4 = plt.subplot(3, 3, 4)
    scatter = ax4.scatter(summary_df['win_rate'], summary_df['profit_factor'], 
                          c=summary_df['final_return'], cmap='RdYlGn', s=100, alpha=0.6)
    ax4.set_xlabel('Win Rate (%)', fontsize=12)
    ax4.set_ylabel('Profit Factor', fontsize=12)
    ax4.set_title('Win Rate vs Profit Factor', fontsize=14, fontweight='bold')
    ax4.grid(True, alpha=0.3)
    plt.colorbar(scatter, ax=ax4, label='Return (%)')
    
    # 5. Bar chart: Top 10 by Profit Factor
    ax5 = plt.subplot(3, 3, 5)
    top10 = summary_df.head(10).copy()
    top10['config'] = top10['sl_config'] + '\n' + top10['tp_config']
    ax5.barh(range(len(top10)), top10['profit_factor'], color='steelblue')
    ax5.set_yticks(range(len(top10)))
    ax5.set_yticklabels(top10['config'], fontsize=9)
    ax5.set_xlabel('Profit Factor', fontsize=12)
    ax5.set_title('Top 10 Configurations by Profit Factor', fontsize=14, fontweight='bold')
    ax5.grid(True, axis='x', alpha=0.3)
    
    # 6. Bar chart: Top 10 by Win Rate
    ax6 = plt.subplot(3, 3, 6)
    top10_wr = summary_df.nlargest(10, 'win_rate').copy()
    top10_wr['config'] = top10_wr['sl_config'] + '\n' + top10_wr['tp_config']
    ax6.barh(range(len(top10_wr)), top10_wr['win_rate'], color='green')
    ax6.set_yticks(range(len(top10_wr)))
    ax6.set_yticklabels(top10_wr['config'], fontsize=9)
    ax6.set_xlabel('Win Rate (%)', fontsize=12)
    ax6.set_title('Top 10 Configurations by Win Rate', fontsize=14, fontweight='bold')
    ax6.grid(True, axis='x', alpha=0.3)
    
    # 7. Equity curves for top 5
    ax7 = plt.subplot(3, 3, 7)
    for i, result in enumerate(results[:5]):
        if 'trades_df' in result:
            ax7.plot(result['trades_df']['equity'], 
                    label=f"{result['sl_config']} / {result['tp_config']}", 
                    linewidth=2, alpha=0.7)
    ax7.set_xlabel('Trade Number', fontsize=12)
    ax7.set_ylabel('Equity ($)', fontsize=12)
    ax7.set_title('Equity Curves - Top 5 Configurations', fontsize=14, fontweight='bold')
    ax7.legend(fontsize=9, loc='best')
    ax7.grid(True, alpha=0.3)
    
    # 8. Box plot: Profit Factor by TP config
    ax8 = plt.subplot(3, 3, 8)
    summary_df.boxplot(column='profit_factor', by='tp_config', ax=ax8)
    ax8.set_xlabel('TP Configuration', fontsize=12)
    ax8.set_ylabel('Profit Factor', fontsize=12)
    ax8.set_title('Profit Factor Distribution by TP Type', fontsize=14, fontweight='bold')
    plt.sca(ax8)
    plt.xticks(rotation=45)
    
    # 9. Box plot: Win Rate by SL config
    ax9 = plt.subplot(3, 3, 9)
    summary_df.boxplot(column='win_rate', by='sl_config', ax=ax9)
    ax9.set_xlabel('SL Configuration', fontsize=12)
    ax9.set_ylabel('Win Rate (%)', fontsize=12)
    ax9.set_title('Win Rate Distribution by SL Type', fontsize=14, fontweight='bold')
    plt.sca(ax9)
    plt.xticks(rotation=45, ha='right')
    
    plt.tight_layout()
    plt.savefig(os.path.join(BASE_PATH, 'sl_tp_optimization_results.png'), dpi=150, bbox_inches='tight')
    print(f"\nVisualization saved: sl_tp_optimization_results.png")
    plt.close()


def generate_markdown_report(summary_df):
    """Generate detailed markdown report."""
    report = []
    report.append("# SMC Reversal Strategy: SL/TP Optimization Results\n")
    report.append("**Complete analysis of 28 configurations (7 SL types × 4 TP types)**\n")
    report.append(f"**Analysis Period:** 2018-2025 (7+ years)\n")
    report.append(f"**Initial Capital:** ${INITIAL_CAPITAL:,}\n")
    report.append(f"**Risk Per Trade:** {RISK_PER_TRADE*100}%\n\n")
    
    report.append("---\n\n")
    report.append("## 🏆 Best Overall Configuration\n\n")
    
    best = summary_df.iloc[0]
    report.append(f"**Stop Loss:** {best['sl_config']}  \n")
    report.append(f"**Take Profit:** {best['tp_config']}  \n\n")
    report.append(f"### Performance Metrics\n")
    report.append(f"- **Total Trades:** {int(best['total_trades'])}\n")
    report.append(f"- **Win Rate:** {best['win_rate']:.2f}% ({int(best['wins'])} wins, {int(best['losses'])} losses)\n")
    report.append(f"- **Profit Factor:** {best['profit_factor']:.2f}\n")
    report.append(f"- **Total P&L:** {best['total_pnl']:+.2f} points\n")
    report.append(f"- **Average Win:** {best['avg_win']:+.2f} pts\n")
    report.append(f"- **Average Loss:** {best['avg_loss']:+.2f} pts\n")
    report.append(f"- **Average R:R:** {best['avg_rr']:.2f}:1\n")
    report.append(f"- **Final Return:** {best['final_return']:+.2f}%\n")
    report.append(f"- **Final Equity:** ${best['final_equity']:,.2f}\n\n")
    
    report.append("---\n\n")
    report.append("## 📊 Top 10 Configurations by Profit Factor\n\n")
    report.append("| Rank | SL Config | TP Config | Trades | Win Rate | Profit Factor | Return % | Avg R:R |\n")
    report.append("|------|-----------|-----------|--------|----------|---------------|----------|----------|\n")
    
    for i, row in summary_df.head(10).iterrows():
        report.append(f"| {i+1} | {row['sl_config']} | {row['tp_config']} | "
                     f"{int(row['total_trades'])} | {row['win_rate']:.1f}% | "
                     f"{row['profit_factor']:.2f} | {row['final_return']:+.1f}% | "
                     f"{row['avg_rr']:.2f} |\n")
    
    report.append("\n---\n\n")
    report.append("## 📈 Analysis by Stop Loss Type\n\n")
    
    for sl_config in SL_CONFIGS:
        sl_results = summary_df[summary_df['sl_config'] == sl_config]
        if len(sl_results) == 0:
            continue
        
        report.append(f"### {sl_config}\n\n")
        report.append(f"**Configurations tested:** {len(sl_results)}  \n")
        report.append(f"**Best TP:** {sl_results.iloc[0]['tp_config']}  \n")
        report.append(f"**Best Profit Factor:** {sl_results.iloc[0]['profit_factor']:.2f}  \n")
        report.append(f"**Avg Win Rate:** {sl_results['win_rate'].mean():.1f}%  \n\n")
    
    report.append("---\n\n")
    report.append("## 🎯 Analysis by Take Profit Type\n\n")
    
    for tp_config in TP_CONFIGS:
        tp_results = summary_df[summary_df['tp_config'] == tp_config]
        if len(tp_results) == 0:
            continue
        
        report.append(f"### {tp_config}\n\n")
        report.append(f"**Configurations tested:** {len(tp_results)}  \n")
        report.append(f"**Best SL:** {tp_results.iloc[0]['sl_config']}  \n")
        report.append(f"**Best Profit Factor:** {tp_results.iloc[0]['profit_factor']:.2f}  \n")
        report.append(f"**Avg Win Rate:** {tp_results['win_rate'].mean():.1f}%  \n\n")
    
    report.append("---\n\n")
    report.append("## 💡 Key Insights\n\n")
    
    # Best SL type
    sl_avg = summary_df.groupby('sl_config')['profit_factor'].mean().sort_values(ascending=False)
    report.append(f"1. **Best SL Type Overall:** {sl_avg.index[0]} (Avg PF: {sl_avg.iloc[0]:.2f})\n")
    
    # Best TP type
    tp_avg = summary_df.groupby('tp_config')['profit_factor'].mean().sort_values(ascending=False)
    report.append(f"2. **Best TP Type Overall:** {tp_avg.index[0]} (Avg PF: {tp_avg.iloc[0]:.2f})\n")
    
    # Win rate analysis
    report.append(f"3. **Highest Win Rate:** {summary_df.iloc[summary_df['win_rate'].argmax()]['sl_config']} / "
                 f"{summary_df.iloc[summary_df['win_rate'].argmax()]['tp_config']} "
                 f"({summary_df['win_rate'].max():.2f}%)\n")
    
    # Return analysis
    report.append(f"4. **Highest Return:** {summary_df.iloc[summary_df['final_return'].argmax()]['sl_config']} / "
                 f"{summary_df.iloc[summary_df['final_return'].argmax()]['tp_config']} "
                 f"({summary_df['final_return'].max():+.2f}%)\n")
    
    report.append("\n---\n\n")
    report.append("## 🔍 Recommendations\n\n")
    report.append(f"Based on the analysis of {len(summary_df)} configurations:\n\n")
    report.append(f"- **For Maximum Profit Factor:** Use {best['sl_config']} with {best['tp_config']}\n")
    
    best_wr = summary_df.iloc[summary_df['win_rate'].argmax()]
    report.append(f"- **For Highest Win Rate:** Use {best_wr['sl_config']} with {best_wr['tp_config']}\n")
    
    best_return = summary_df.iloc[summary_df['final_return'].argmax()]
    report.append(f"- **For Maximum Returns:** Use {best_return['sl_config']} with {best_return['tp_config']}\n\n")
    
    report.append("---\n\n")
    report.append("*Analysis generated by SMC SL/TP Optimization Engine*\n")
    report.append(f"*Date: 2025-12-11*\n")
    
    # Save report
    report_text = ''.join(report)
    with open(os.path.join(BASE_PATH, 'SL_TP_OPTIMIZATION_REPORT.md'), 'w') as f:
        f.write(report_text)
    
    print("\nMarkdown report saved: SL_TP_OPTIMIZATION_REPORT.md")
    
    return report_text


if __name__ == "__main__":
    print("\n" + "="*80)
    print("SMC REVERSAL STRATEGY: COMPREHENSIVE SL/TP OPTIMIZATION")
    print("="*80)
    print("\nThis script will test 28 different configurations:")
    print(f"- SL Types: {len(SL_CONFIGS)}")
    print(f"- TP Types: {len(TP_CONFIGS)}")
    print(f"- Total Combinations: {len(SL_CONFIGS) * len(TP_CONFIGS)}")
    print("\nEstimated runtime: 10-15 minutes")
    print("="*80)
    
    # Run optimization
    summary_df, results = run_optimization()
    
    # Generate markdown report
    if summary_df is not None:
        generate_markdown_report(summary_df)
    
    print("\n" + "="*80)
    print("✅ OPTIMIZATION COMPLETE!")
    print("="*80)
    print("\nGenerated files:")
    print("1. sl_tp_optimization_summary.csv - Complete results table")
    print("2. sl_tp_optimization_results.png - Visualization charts")
    print("3. SL_TP_OPTIMIZATION_REPORT.md - Detailed markdown report")
    print("4. trades_[CONFIG].csv - Detailed trades for top 5 configurations")
    print("\n" + "="*80)

"""
IFVG Strategy - Stop Loss & Take Profit Analysis
Author: Backtest Script
Date: 2025-12-22

This script tests multiple Stop Loss and Take Profit configurations
to find the optimal parameters for the IFVG strategy.

Stop Loss Types:
1. At candle low/high (0 points buffer)
2. At swing low/high of 5 previous candles
3. 20 points from candle
4. 15 points from candle
5. 30 points from candle

Risk/Reward Ratios: 1.0, 1.5, 2.0, 2.5
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, time
import os
import warnings
warnings.filterwarnings('ignore')

# Configuration
DATA_DIR = "/home/runner/work/Backtest-Trading/Backtest-Trading"
YEARS = range(2018, 2026)  # 2018 to 2025
TRADE_START_TIME = time(2, 0, 0)  # 02:00:00
TRADE_END_TIME = time(6, 0, 0)    # 06:00:00
INITIAL_CAPITAL = 100000
POSITION_SIZE = 1  # 1 contract per trade
LOOKBACK_CANDLES = 12  # 60 minutes = 12 candles for liquidity sweep
STRONG_CLOSE_THRESHOLD = 0.15  # 15% of FVG range for strong close filter

# Stop Loss configurations to test
SL_CONFIGS = [
    {'name': 'SL at candle', 'type': 'candle', 'points': 0},
    {'name': 'SL at swing (5 candles)', 'type': 'swing', 'points': 0},
    {'name': 'SL +20 points', 'type': 'candle', 'points': 20},
    {'name': 'SL +15 points', 'type': 'candle', 'points': 15},
    {'name': 'SL +30 points', 'type': 'candle', 'points': 30},
]

# Risk/Reward ratios to test
RR_RATIOS = [1.0, 1.5, 2.0, 2.5]

print("=" * 80)
print("IFVG Strategy - Stop Loss & Take Profit Analysis")
print("=" * 80)
print(f"Testing {len(SL_CONFIGS)} SL types × {len(RR_RATIOS)} RR ratios = {len(SL_CONFIGS) * len(RR_RATIOS)} configurations")
print("=" * 80)

def load_all_data():
    """Load and combine all 5-minute NQ data from 2018 to 2025"""
    all_data = []
    
    for year in YEARS:
        filename = f"{year} 5m.csv"
        filepath = os.path.join(DATA_DIR, filename)
        
        if not os.path.exists(filepath):
            print(f"Warning: {filename} not found, skipping...")
            continue
        
        print(f"Loading {filename}...")
        
        # Read CSV with semicolon delimiter
        df = pd.read_csv(filepath, sep=';', header=0)
        
        # Rename columns for easier access
        df.columns = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
        
        # Combine Date and Time into datetime (no timezone conversion)
        df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%d/%m/%Y %H:%M:%S')
        
        # Extract time for filtering
        df['TimeOnly'] = df['DateTime'].dt.time
        
        # Keep only necessary columns
        df = df[['DateTime', 'TimeOnly', 'Open', 'High', 'Low', 'Close', 'Volume']]
        
        all_data.append(df)
    
    # Combine all years
    combined_df = pd.concat(all_data, ignore_index=True)
    combined_df = combined_df.sort_values('DateTime').reset_index(drop=True)
    
    print(f"\nTotal candles loaded: {len(combined_df)}")
    print(f"Date range: {combined_df['DateTime'].min()} to {combined_df['DateTime'].max()}")
    
    return combined_df

def detect_fractal_high(df, i, lookback=2):
    """Detect if index i is a fractal high (5-period fractal)"""
    if i < lookback or i >= len(df) - lookback:
        return False
    
    high = df.loc[i, 'High']
    
    # Check if current high is greater than lookback periods before and after
    for j in range(1, lookback + 1):
        if high <= df.loc[i - j, 'High'] or high <= df.loc[i + j, 'High']:
            return False
    
    return True

def detect_fractal_low(df, i, lookback=2):
    """Detect if index i is a fractal low (5-period fractal)"""
    if i < lookback or i >= len(df) - lookback:
        return False
    
    low = df.loc[i, 'Low']
    
    # Check if current low is less than lookback periods before and after
    for j in range(1, lookback + 1):
        if low >= df.loc[i - j, 'Low'] or low >= df.loc[i + j, 'Low']:
            return False
    
    return True

def check_liquidity_sweep(df, current_idx, direction, lookback_candles=12):
    """
    Check if there was a liquidity sweep in the last N candles before current_idx
    For Long: Check if price swept a fractal high
    For Short: Check if price swept a fractal low
    """
    start_idx = max(0, current_idx - lookback_candles)
    
    if direction == 'long':
        # Look for fractal highs that were swept
        for i in range(start_idx, current_idx):
            if detect_fractal_high(df, i):
                fractal_high = df.loc[i, 'High']
                # Check if any subsequent candle swept above this high
                for j in range(i + 1, current_idx + 1):
                    if df.loc[j, 'High'] > fractal_high:
                        return True
        return False
    
    elif direction == 'short':
        # Look for fractal lows that were swept
        for i in range(start_idx, current_idx):
            if detect_fractal_low(df, i):
                fractal_low = df.loc[i, 'Low']
                # Check if any subsequent candle swept below this low
                for j in range(i + 1, current_idx + 1):
                    if df.loc[j, 'Low'] < fractal_low:
                        return True
        return False
    
    return False

def get_swing_low(df, idx, lookback=5):
    """Get the swing low of the previous N candles"""
    start_idx = max(0, idx - lookback)
    return df.loc[start_idx:idx-1, 'Low'].min() if start_idx < idx else df.loc[idx, 'Low']

def get_swing_high(df, idx, lookback=5):
    """Get the swing high of the previous N candles"""
    start_idx = max(0, idx - lookback)
    return df.loc[start_idx:idx-1, 'High'].max() if start_idx < idx else df.loc[idx, 'High']

def calculate_stop_loss(df, idx, direction, sl_config):
    """Calculate stop loss based on configuration"""
    sl_type = sl_config['type']
    points = sl_config['points']
    
    if direction == 'long':
        if sl_type == 'candle':
            return df.loc[idx, 'Low'] - points
        elif sl_type == 'swing':
            swing_low = get_swing_low(df, idx, lookback=5)
            return swing_low - points
    else:  # short
        if sl_type == 'candle':
            return df.loc[idx, 'High'] + points
        elif sl_type == 'swing':
            swing_high = get_swing_high(df, idx, lookback=5)
            return swing_high + points
    
    return None

def detect_fvg_and_ifvg(df):
    """
    Detect FVG and IFVG setups
    Returns a list of trade signals with entry details
    """
    signals = []
    
    # We need at least 3 candles to detect FVG
    for i in range(2, len(df)):
        # Only consider candles within trading hours
        if not (TRADE_START_TIME <= df.loc[i, 'TimeOnly'] <= TRADE_END_TIME):
            continue
        
        # Get the three consecutive candles for FVG detection
        # N-2, N-1, N where N is current candle (i)
        n_minus_2 = i - 2
        n_minus_1 = i - 1
        n = i
        
        # Bearish FVG: Low[N-2] > High[N]
        if df.loc[n_minus_2, 'Low'] > df.loc[n, 'High']:
            bearish_fvg_low = df.loc[n, 'High']
            bearish_fvg_high = df.loc[n_minus_2, 'Low']
            
            # Now look for inversion (bullish breakout above the FVG)
            # Check subsequent candles for IFVG signal (long setup)
            for j in range(i + 1, len(df)):
                # Must be within trading hours
                if not (TRADE_START_TIME <= df.loc[j, 'TimeOnly'] <= TRADE_END_TIME):
                    continue
                
                # Check if close is STRICTLY ABOVE the FVG high
                if df.loc[j, 'Close'] > bearish_fvg_high:
                    # Filter 1: Check liquidity sweep
                    if not check_liquidity_sweep(df, j, 'long', LOOKBACK_CANDLES):
                        break  # No liquidity sweep, skip this FVG
                    
                    # Filter 2: Check strong close
                    fvg_range = bearish_fvg_high - bearish_fvg_low
                    close_distance = df.loc[j, 'Close'] - bearish_fvg_high
                    
                    if close_distance < (fvg_range * STRONG_CLOSE_THRESHOLD):
                        break  # Weak close, skip this setup
                    
                    # Valid IFVG long setup
                    signals.append({
                        'entry_idx': j,
                        'entry_datetime': df.loc[j, 'DateTime'],
                        'direction': 'long',
                        'entry_price': df.loc[j, 'Close'],
                        'candle_low': df.loc[j, 'Low'],
                        'candle_high': df.loc[j, 'High'],
                        'fvg_low': bearish_fvg_low,
                        'fvg_high': bearish_fvg_high
                    })
                    break  # Found signal, move to next potential FVG
                
                # If we've gone too far past the FVG without inversion, stop looking
                if j - i > 20:  # Look ahead max 20 candles (100 minutes)
                    break
        
        # Bullish FVG: High[N-2] < Low[N]
        if df.loc[n_minus_2, 'High'] < df.loc[n, 'Low']:
            bullish_fvg_high = df.loc[n_minus_2, 'High']
            bullish_fvg_low = df.loc[n, 'Low']
            
            # Now look for inversion (bearish breakdown below the FVG)
            # Check subsequent candles for IFVG signal (short setup)
            for j in range(i + 1, len(df)):
                # Must be within trading hours
                if not (TRADE_START_TIME <= df.loc[j, 'TimeOnly'] <= TRADE_END_TIME):
                    continue
                
                # Check if close is STRICTLY BELOW the FVG low
                if df.loc[j, 'Close'] < bullish_fvg_low:
                    # Filter 1: Check liquidity sweep
                    if not check_liquidity_sweep(df, j, 'short', LOOKBACK_CANDLES):
                        break  # No liquidity sweep, skip this FVG
                    
                    # Filter 2: Check strong close
                    fvg_range = bullish_fvg_high - bullish_fvg_low
                    close_distance = bullish_fvg_low - df.loc[j, 'Close']
                    
                    if close_distance < (fvg_range * STRONG_CLOSE_THRESHOLD):
                        break  # Weak close, skip this setup
                    
                    # Valid IFVG short setup
                    signals.append({
                        'entry_idx': j,
                        'entry_datetime': df.loc[j, 'DateTime'],
                        'direction': 'short',
                        'entry_price': df.loc[j, 'Close'],
                        'candle_low': df.loc[j, 'Low'],
                        'candle_high': df.loc[j, 'High'],
                        'fvg_low': bullish_fvg_low,
                        'fvg_high': bullish_fvg_high
                    })
                    break  # Found signal, move to next potential FVG
                
                # If we've gone too far past the FVG without inversion, stop looking
                if j - i > 20:  # Look ahead max 20 candles (100 minutes)
                    break
    
    return signals

def execute_trades(df, signals, sl_config, rr_ratio):
    """Execute trades based on signals and track results"""
    trades = []
    
    for signal in signals:
        entry_idx = signal['entry_idx']
        direction = signal['direction']
        entry_price = signal['entry_price']
        entry_datetime = signal['entry_datetime']
        
        # Calculate stop loss based on configuration
        stop_loss = calculate_stop_loss(df, entry_idx, direction, sl_config)
        
        # Calculate risk and take profit
        if direction == 'long':
            risk = entry_price - stop_loss
        else:  # short
            risk = stop_loss - entry_price
        
        # Calculate take profit based on RR ratio
        if direction == 'long':
            take_profit = entry_price + (risk * rr_ratio)
        else:  # short
            take_profit = entry_price - (risk * rr_ratio)
        
        # Track the trade from entry to exit
        exit_price = None
        exit_datetime = None
        exit_reason = None
        
        # Look forward from entry to find exit
        for j in range(entry_idx + 1, len(df)):
            candle_high = df.loc[j, 'High']
            candle_low = df.loc[j, 'Low']
            candle_close = df.loc[j, 'Close']
            candle_datetime = df.loc[j, 'DateTime']
            
            if direction == 'long':
                # Check if TP hit
                if candle_high >= take_profit:
                    exit_price = take_profit
                    exit_datetime = candle_datetime
                    exit_reason = 'TP'
                    break
                # Check if SL hit
                if candle_low <= stop_loss:
                    exit_price = stop_loss
                    exit_datetime = candle_datetime
                    exit_reason = 'SL'
                    break
            
            elif direction == 'short':
                # Check if TP hit
                if candle_low <= take_profit:
                    exit_price = take_profit
                    exit_datetime = candle_datetime
                    exit_reason = 'TP'
                    break
                # Check if SL hit
                if candle_high >= stop_loss:
                    exit_price = stop_loss
                    exit_datetime = candle_datetime
                    exit_reason = 'SL'
                    break
            
            # Max holding period: 100 candles (8+ hours)
            if j - entry_idx > 100:
                exit_price = candle_close
                exit_datetime = candle_datetime
                exit_reason = 'Timeout'
                break
        
        # If no exit found (end of data), close at last available price
        if exit_price is None:
            exit_price = df.loc[len(df) - 1, 'Close']
            exit_datetime = df.loc[len(df) - 1, 'DateTime']
            exit_reason = 'EOD'
        
        # Calculate PnL
        if direction == 'long':
            pnl = (exit_price - entry_price) * POSITION_SIZE
        else:  # short
            pnl = (entry_price - exit_price) * POSITION_SIZE
        
        # Determine win/loss
        result = 'Win' if pnl > 0 else 'Loss'
        
        trades.append({
            'entry_datetime': entry_datetime,
            'exit_datetime': exit_datetime,
            'direction': direction,
            'entry_price': entry_price,
            'stop_loss': stop_loss,
            'take_profit': take_profit,
            'exit_price': exit_price,
            'pnl': pnl,
            'result': result,
            'exit_reason': exit_reason,
            'risk': risk
        })
    
    return trades

def calculate_statistics(trades):
    """Calculate performance statistics"""
    if len(trades) == 0:
        return None
    
    total_trades = len(trades)
    winning_trades = [t for t in trades if t['result'] == 'Win']
    losing_trades = [t for t in trades if t['result'] == 'Loss']
    
    num_wins = len(winning_trades)
    num_losses = len(losing_trades)
    win_rate = (num_wins / total_trades * 100) if total_trades > 0 else 0
    
    gross_profit = sum([t['pnl'] for t in winning_trades])
    gross_loss = abs(sum([t['pnl'] for t in losing_trades]))
    
    profit_factor = (gross_profit / gross_loss) if gross_loss > 0 else float('inf')
    
    total_return = sum([t['pnl'] for t in trades])
    total_return_pct = (total_return / INITIAL_CAPITAL) * 100
    
    # Calculate max drawdown
    equity_curve = []
    running_balance = INITIAL_CAPITAL
    for trade in trades:
        running_balance += trade['pnl']
        equity_curve.append(running_balance)
    
    peak = INITIAL_CAPITAL
    max_drawdown = 0
    for equity in equity_curve:
        if equity > peak:
            peak = equity
        drawdown = ((peak - equity) / peak) * 100
        if drawdown > max_drawdown:
            max_drawdown = drawdown
    
    # Calculate average risk
    avg_risk = sum([t['risk'] for t in trades]) / len(trades) if trades else 0
    
    return {
        'total_trades': total_trades,
        'winning_trades': num_wins,
        'losing_trades': num_losses,
        'win_rate': win_rate,
        'profit_factor': profit_factor,
        'total_return': total_return,
        'total_return_pct': total_return_pct,
        'max_drawdown': max_drawdown,
        'gross_profit': gross_profit,
        'gross_loss': gross_loss,
        'avg_risk': avg_risk
    }

def run_backtest_configuration(df, signals, sl_config, rr_ratio):
    """Run backtest for a specific SL/TP configuration"""
    trades = execute_trades(df, signals, sl_config, rr_ratio)
    stats = calculate_statistics(trades)
    return stats

def create_comparison_table(results):
    """Create a comparison table of all results"""
    print("\n" + "=" * 120)
    print("RESULTS COMPARISON - ALL CONFIGURATIONS")
    print("=" * 120)
    
    # Header
    header = f"{'SL Type':<30} {'RR':<6} {'Trades':<8} {'Win%':<8} {'PF':<8} {'Return%':<10} {'MaxDD%':<10} {'AvgRisk':<10}"
    print(header)
    print("-" * 120)
    
    # Sort by return percentage (descending)
    sorted_results = sorted(results, key=lambda x: x['stats']['total_return_pct'] if x['stats'] else -999, reverse=True)
    
    for result in sorted_results:
        if result['stats'] is None:
            continue
        
        sl_name = result['sl_name']
        rr = result['rr_ratio']
        stats = result['stats']
        
        line = f"{sl_name:<30} {rr:<6.1f} {stats['total_trades']:<8} "
        line += f"{stats['win_rate']:<8.2f} {stats['profit_factor']:<8.2f} "
        line += f"{stats['total_return_pct']:<10.2f} {stats['max_drawdown']:<10.2f} "
        line += f"{stats['avg_risk']:<10.2f}"
        print(line)
    
    print("=" * 120)

def create_summary_by_sl_type(results):
    """Create summary grouped by SL type"""
    print("\n" + "=" * 120)
    print("SUMMARY BY STOP LOSS TYPE")
    print("=" * 120)
    
    # Group by SL type
    sl_types = {}
    for result in results:
        if result['stats'] is None:
            continue
        sl_name = result['sl_name']
        if sl_name not in sl_types:
            sl_types[sl_name] = []
        sl_types[sl_name].append(result)
    
    for sl_name, sl_results in sl_types.items():
        print(f"\n{sl_name}:")
        print("-" * 80)
        
        best_rr = max(sl_results, key=lambda x: x['stats']['total_return_pct'])
        print(f"  Best RR Ratio: {best_rr['rr_ratio']} (Return: {best_rr['stats']['total_return_pct']:.2f}%)")
        
        avg_return = sum([r['stats']['total_return_pct'] for r in sl_results]) / len(sl_results)
        avg_winrate = sum([r['stats']['win_rate'] for r in sl_results]) / len(sl_results)
        avg_pf = sum([r['stats']['profit_factor'] for r in sl_results]) / len(sl_results)
        
        print(f"  Average Return: {avg_return:.2f}%")
        print(f"  Average Win Rate: {avg_winrate:.2f}%")
        print(f"  Average Profit Factor: {avg_pf:.2f}")

def plot_results_comparison(results, filename='sl_tp_comparison.png'):
    """Create visualization comparing all configurations"""
    # Prepare data for plotting
    plot_data = []
    for result in results:
        if result['stats'] is None:
            continue
        plot_data.append({
            'config': f"{result['sl_name'][:15]} RR{result['rr_ratio']}",
            'return_pct': result['stats']['total_return_pct'],
            'win_rate': result['stats']['win_rate'],
            'profit_factor': result['stats']['profit_factor'],
            'max_dd': result['stats']['max_drawdown']
        })
    
    df_plot = pd.DataFrame(plot_data)
    
    # Sort by return
    df_plot = df_plot.sort_values('return_pct', ascending=False)
    
    # Create subplots
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('IFVG Strategy - SL/TP Configuration Comparison', fontsize=16, fontweight='bold')
    
    # Plot 1: Return %
    axes[0, 0].barh(range(len(df_plot)), df_plot['return_pct'])
    axes[0, 0].set_yticks(range(len(df_plot)))
    axes[0, 0].set_yticklabels(df_plot['config'], fontsize=7)
    axes[0, 0].set_xlabel('Return %')
    axes[0, 0].set_title('Total Return by Configuration')
    axes[0, 0].grid(True, alpha=0.3)
    axes[0, 0].axvline(x=0, color='red', linestyle='--', linewidth=1)
    
    # Plot 2: Win Rate
    axes[0, 1].barh(range(len(df_plot)), df_plot['win_rate'])
    axes[0, 1].set_yticks(range(len(df_plot)))
    axes[0, 1].set_yticklabels(df_plot['config'], fontsize=7)
    axes[0, 1].set_xlabel('Win Rate %')
    axes[0, 1].set_title('Win Rate by Configuration')
    axes[0, 1].grid(True, alpha=0.3)
    
    # Plot 3: Profit Factor
    axes[1, 0].barh(range(len(df_plot)), df_plot['profit_factor'])
    axes[1, 0].set_yticks(range(len(df_plot)))
    axes[1, 0].set_yticklabels(df_plot['config'], fontsize=7)
    axes[1, 0].set_xlabel('Profit Factor')
    axes[1, 0].set_title('Profit Factor by Configuration')
    axes[1, 0].grid(True, alpha=0.3)
    axes[1, 0].axvline(x=1.0, color='red', linestyle='--', linewidth=1)
    
    # Plot 4: Max Drawdown
    axes[1, 1].barh(range(len(df_plot)), df_plot['max_dd'])
    axes[1, 1].set_yticks(range(len(df_plot)))
    axes[1, 1].set_yticklabels(df_plot['config'], fontsize=7)
    axes[1, 1].set_xlabel('Max Drawdown %')
    axes[1, 1].set_title('Maximum Drawdown by Configuration')
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    filepath = os.path.join(DATA_DIR, filename)
    plt.savefig(filepath, dpi=150, bbox_inches='tight')
    print(f"\nComparison chart saved to: {filepath}")
    plt.close()

def save_detailed_results(results, filename='sl_tp_analysis_results.csv'):
    """Save detailed results to CSV"""
    data = []
    for result in results:
        if result['stats'] is None:
            continue
        
        row = {
            'SL_Type': result['sl_name'],
            'RR_Ratio': result['rr_ratio'],
            'Total_Trades': result['stats']['total_trades'],
            'Winning_Trades': result['stats']['winning_trades'],
            'Losing_Trades': result['stats']['losing_trades'],
            'Win_Rate_%': result['stats']['win_rate'],
            'Profit_Factor': result['stats']['profit_factor'],
            'Total_Return_$': result['stats']['total_return'],
            'Total_Return_%': result['stats']['total_return_pct'],
            'Max_Drawdown_%': result['stats']['max_drawdown'],
            'Gross_Profit': result['stats']['gross_profit'],
            'Gross_Loss': result['stats']['gross_loss'],
            'Avg_Risk_Points': result['stats']['avg_risk']
        }
        data.append(row)
    
    df_results = pd.DataFrame(data)
    df_results = df_results.sort_values('Total_Return_%', ascending=False)
    
    filepath = os.path.join(DATA_DIR, filename)
    df_results.to_csv(filepath, index=False)
    print(f"Detailed results saved to: {filepath}")

def main():
    """Main execution function"""
    # Load data
    print("\n" + "=" * 80)
    print("Loading Data...")
    print("=" * 80)
    df = load_all_data()
    
    print("\n" + "=" * 80)
    print("Detecting IFVG Setups...")
    print("=" * 80)
    
    # Detect FVG and IFVG signals (same for all configurations)
    signals = detect_fvg_and_ifvg(df)
    print(f"\nFound {len(signals)} IFVG signals")
    
    if len(signals) == 0:
        print("No valid IFVG setups found!")
        return
    
    # Test all configurations
    print("\n" + "=" * 80)
    print("Testing All SL/TP Configurations...")
    print("=" * 80)
    
    results = []
    total_configs = len(SL_CONFIGS) * len(RR_RATIOS)
    current = 0
    
    for sl_config in SL_CONFIGS:
        for rr_ratio in RR_RATIOS:
            current += 1
            print(f"\n[{current}/{total_configs}] Testing: {sl_config['name']} with RR {rr_ratio}...")
            
            stats = run_backtest_configuration(df, signals, sl_config, rr_ratio)
            
            results.append({
                'sl_name': sl_config['name'],
                'sl_config': sl_config,
                'rr_ratio': rr_ratio,
                'stats': stats
            })
            
            if stats:
                print(f"  → Trades: {stats['total_trades']}, Win Rate: {stats['win_rate']:.2f}%, "
                      f"PF: {stats['profit_factor']:.2f}, Return: {stats['total_return_pct']:.2f}%")
    
    # Display results
    create_comparison_table(results)
    create_summary_by_sl_type(results)
    
    # Save outputs
    print("\n" + "=" * 80)
    print("Saving Outputs...")
    print("=" * 80)
    plot_results_comparison(results)
    save_detailed_results(results)
    
    # Find and highlight best configuration
    print("\n" + "=" * 80)
    print("BEST CONFIGURATIONS")
    print("=" * 80)
    
    best_return = max(results, key=lambda x: x['stats']['total_return_pct'] if x['stats'] else -999)
    best_winrate = max(results, key=lambda x: x['stats']['win_rate'] if x['stats'] else -999)
    best_pf = max(results, key=lambda x: x['stats']['profit_factor'] if x['stats'] else -999)
    best_dd = min(results, key=lambda x: x['stats']['max_drawdown'] if x['stats'] else 999)
    
    print(f"\n🏆 Best Return: {best_return['sl_name']} with RR {best_return['rr_ratio']}")
    print(f"   Return: {best_return['stats']['total_return_pct']:.2f}%, "
          f"Win Rate: {best_return['stats']['win_rate']:.2f}%, "
          f"PF: {best_return['stats']['profit_factor']:.2f}")
    
    print(f"\n🎯 Best Win Rate: {best_winrate['sl_name']} with RR {best_winrate['rr_ratio']}")
    print(f"   Win Rate: {best_winrate['stats']['win_rate']:.2f}%, "
          f"Return: {best_winrate['stats']['total_return_pct']:.2f}%, "
          f"PF: {best_winrate['stats']['profit_factor']:.2f}")
    
    print(f"\n💰 Best Profit Factor: {best_pf['sl_name']} with RR {best_pf['rr_ratio']}")
    print(f"   PF: {best_pf['stats']['profit_factor']:.2f}, "
          f"Win Rate: {best_pf['stats']['win_rate']:.2f}%, "
          f"Return: {best_pf['stats']['total_return_pct']:.2f}%")
    
    print(f"\n🛡️  Best Risk Control (Lowest DD): {best_dd['sl_name']} with RR {best_dd['rr_ratio']}")
    print(f"   Max DD: {best_dd['stats']['max_drawdown']:.2f}%, "
          f"Return: {best_dd['stats']['total_return_pct']:.2f}%, "
          f"Win Rate: {best_dd['stats']['win_rate']:.2f}%")
    
    print("\n" + "=" * 80)
    print("Analysis Complete!")
    print("=" * 80)

if __name__ == "__main__":
    main()

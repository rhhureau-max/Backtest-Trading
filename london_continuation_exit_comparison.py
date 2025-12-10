#!/usr/bin/env python3
"""
London Continuation - Exit Strategy Comparison
Compare 3 exit management approaches on the same entry signals:
A) Pure Time Exit (07:00 CST) - No SL
B) Time Exit + Catastrophe SL (-100pts)
C) Structure SL + R:R TP

All use the same entry logic: Asian Range breakout during London Killzone
with volume and continuation filters.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')


def load_nq_data(years=None, timeframe='15m', base_path=None):
    """Load NQ futures data from CSV files."""
    if years is None:
        years = list(range(2018, 2026))
    
    if base_path is None:
        base_path = Path.cwd()
    else:
        base_path = Path(base_path)
    
    dfs = []
    
    for year in years:
        filename = f"{year} {timeframe}.csv"
        filepath = base_path / filename
        
        if not filepath.exists():
            continue
        
        try:
            df = pd.read_csv(filepath, sep=';', encoding='utf-8-sig')
            df.columns = df.columns.str.replace('\ufeff', '').str.strip()
            
            if len(df.columns) >= 7:
                df.columns = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
            
            df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%d/%m/%Y %H:%M:%S')
            df.set_index('DateTime', inplace=True)
            df = df[['Open', 'High', 'Low', 'Close', 'Volume']]
            
            for col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            
            dfs.append(df)
            print(f"Loaded {year} {timeframe}: {len(df)} bars")
            
        except Exception as e:
            print(f"Error loading {filename}: {e}")
            continue
    
    if not dfs:
        raise ValueError(f"No {timeframe} data loaded!")
    
    data = pd.concat(dfs)
    data.sort_index(inplace=True)
    data = data[~data.index.duplicated(keep='first')]
    
    print(f"Total {timeframe} data: {len(data)} bars from {data.index[0]} to {data.index[-1]}")
    
    return data


def identify_asian_range(df, date):
    """Identify Asian Range: 18:00 (D-1) to 00:00 (D) CST."""
    prev_date = date - timedelta(days=1)
    
    start_time = pd.Timestamp(year=prev_date.year, month=prev_date.month, 
                              day=prev_date.day, hour=18, minute=0)
    end_time = pd.Timestamp(year=date.year, month=date.month, 
                           day=date.day, hour=0, minute=0)
    
    asian_data = df[(df.index >= start_time) & (df.index < end_time)]
    
    if len(asian_data) < 5:
        return None
    
    asian_high = asian_data['High'].max()
    asian_low = asian_data['Low'].min()
    asian_mid = (asian_high + asian_low) / 2
    
    return {
        'asian_high': asian_high,
        'asian_low': asian_low,
        'asian_mid': asian_mid
    }


def calculate_volume_ma(df, periods=20):
    """Calculate rolling volume MA."""
    return df['Volume'].rolling(window=periods, min_periods=1).mean()


def detect_breakout(df, date, asian_info):
    """
    Detect breakout during London Killzone (01:00-04:00 CST).
    Returns first valid breakout with volume filter.
    """
    asian_high = asian_info['asian_high']
    asian_low = asian_info['asian_low']
    
    start_time = pd.Timestamp(year=date.year, month=date.month, 
                              day=date.day, hour=1, minute=0)
    end_time = pd.Timestamp(year=date.year, month=date.month, 
                           day=date.day, hour=4, minute=0)
    
    killzone_data = df[(df.index >= start_time) & (df.index <= end_time)]
    
    if len(killzone_data) == 0:
        return None
    
    vol_ma = calculate_volume_ma(df)
    
    for idx, row in killzone_data.iterrows():
        close_price = row['Close']
        volume = row['Volume']
        vol_ma_value = vol_ma.loc[idx] if idx in vol_ma.index else 0
        
        # Volume filter
        if volume <= vol_ma_value:
            continue
        
        # Bullish breakout
        if close_price > asian_high:
            return {
                'entry_time': idx,
                'entry_price': close_price,
                'direction': 'LONG',
                'asian_high': asian_high,
                'asian_low': asian_low,
                'asian_mid': asian_info['asian_mid']
            }
        
        # Bearish breakout
        elif close_price < asian_low:
            return {
                'entry_time': idx,
                'entry_price': close_price,
                'direction': 'SHORT',
                'asian_high': asian_high,
                'asian_low': asian_low,
                'asian_mid': asian_info['asian_mid']
            }
    
    return None


def validate_continuation(df, breakout_info):
    """
    Validate no >50% retracement in 2 hours after entry.
    This filters out fake breakouts.
    """
    entry_time = breakout_info['entry_time']
    direction = breakout_info['direction']
    asian_mid = breakout_info['asian_mid']
    
    validation_end = entry_time + timedelta(hours=2)
    validation_data = df[(df.index > entry_time) & (df.index <= validation_end)]
    
    if len(validation_data) == 0:
        return False
    
    if direction == 'LONG':
        min_low = validation_data['Low'].min()
        if min_low < asian_mid:
            return False
    else:  # SHORT
        max_high = validation_data['High'].max()
        if max_high > asian_mid:
            return False
    
    return True


def execute_variant_a(df, breakout_info):
    """
    Variant A: Pure Time Exit at 07:00 CST
    No SL, No TP - just exit at 07:00
    """
    entry_price = breakout_info['entry_price']
    entry_time = breakout_info['entry_time']
    direction = breakout_info['direction']
    date = entry_time.date()
    
    # Exit at 07:00 CST
    exit_time = pd.Timestamp(year=date.year, month=date.month, 
                            day=date.day, hour=7, minute=0)
    
    exit_data = df[df.index >= exit_time]
    
    if len(exit_data) == 0:
        return None
    
    exit_price = exit_data.iloc[0]['Close']
    actual_exit_time = exit_data.index[0]
    
    if direction == 'LONG':
        pnl_points = exit_price - entry_price
    else:
        pnl_points = entry_price - exit_price
    
    return {
        'exit_time': actual_exit_time,
        'exit_price': exit_price,
        'exit_type': 'TIME_EXIT',
        'pnl_points': pnl_points
    }


def execute_variant_b(df, breakout_info):
    """
    Variant B: Time Exit + Catastrophe SL (-100 points)
    Check M1 data for -100pt SL hit, otherwise exit at 07:00
    """
    entry_price = breakout_info['entry_price']
    entry_time = breakout_info['entry_time']
    direction = breakout_info['direction']
    date = entry_time.date()
    
    # Catastrophe SL: -100 points from entry
    if direction == 'LONG':
        catastrophe_sl = entry_price - 100.0
    else:
        catastrophe_sl = entry_price + 100.0
    
    # Time exit at 07:00
    exit_time = pd.Timestamp(year=date.year, month=date.month, 
                            day=date.day, hour=7, minute=0)
    
    # Check all bars between entry and 07:00 for catastrophe SL hit
    check_data = df[(df.index > entry_time) & (df.index <= exit_time)]
    
    for bar_time, bar in check_data.iterrows():
        if direction == 'LONG':
            if bar['Low'] <= catastrophe_sl:
                # SL hit
                return {
                    'exit_time': bar_time,
                    'exit_price': catastrophe_sl,
                    'exit_type': 'CATASTROPHE_SL',
                    'pnl_points': -100.0
                }
        else:  # SHORT
            if bar['High'] >= catastrophe_sl:
                # SL hit
                return {
                    'exit_time': bar_time,
                    'exit_price': catastrophe_sl,
                    'exit_type': 'CATASTROPHE_SL',
                    'pnl_points': -100.0
                }
    
    # No SL hit, exit at 07:00
    exit_data = df[df.index >= exit_time]
    
    if len(exit_data) == 0:
        return None
    
    exit_price = exit_data.iloc[0]['Close']
    actual_exit_time = exit_data.index[0]
    
    if direction == 'LONG':
        pnl_points = exit_price - entry_price
    else:
        pnl_points = entry_price - exit_price
    
    return {
        'exit_time': actual_exit_time,
        'exit_price': exit_price,
        'exit_type': 'TIME_EXIT',
        'pnl_points': pnl_points
    }


def execute_variant_c(df, breakout_info, tp_r_multiple=1.5):
    """
    Variant C: Structure SL + R:R TP
    SL at Asian_Low-2 (LONG) or Asian_High+2 (SHORT)
    TP at tp_r_multiple * R
    If neither hit by 07:00, force close
    """
    entry_price = breakout_info['entry_price']
    entry_time = breakout_info['entry_time']
    direction = breakout_info['direction']
    asian_high = breakout_info['asian_high']
    asian_low = breakout_info['asian_low']
    date = entry_time.date()
    
    # Calculate SL
    if direction == 'LONG':
        sl_price = asian_low - 2.0
    else:
        sl_price = asian_high + 2.0
    
    # Calculate Risk (R)
    risk_r = abs(entry_price - sl_price)
    
    # Calculate TP
    if direction == 'LONG':
        tp_price = entry_price + (risk_r * tp_r_multiple)
    else:
        tp_price = entry_price - (risk_r * tp_r_multiple)
    
    # Force close time
    force_close_time = pd.Timestamp(year=date.year, month=date.month, 
                                    day=date.day, hour=7, minute=0)
    
    # Check bars for SL or TP hit
    check_data = df[(df.index > entry_time) & (df.index <= force_close_time)]
    
    for bar_time, bar in check_data.iterrows():
        if direction == 'LONG':
            # Check SL first (more conservative)
            if bar['Low'] <= sl_price:
                pnl_points = sl_price - entry_price
                return {
                    'exit_time': bar_time,
                    'exit_price': sl_price,
                    'exit_type': 'SL',
                    'pnl_points': pnl_points,
                    'risk_r': risk_r
                }
            # Check TP
            if bar['High'] >= tp_price:
                pnl_points = tp_price - entry_price
                return {
                    'exit_time': bar_time,
                    'exit_price': tp_price,
                    'exit_type': 'TP',
                    'pnl_points': pnl_points,
                    'risk_r': risk_r
                }
        else:  # SHORT
            # Check SL first
            if bar['High'] >= sl_price:
                pnl_points = entry_price - sl_price
                return {
                    'exit_time': bar_time,
                    'exit_price': sl_price,
                    'exit_type': 'SL',
                    'pnl_points': pnl_points,
                    'risk_r': risk_r
                }
            # Check TP
            if bar['Low'] <= tp_price:
                pnl_points = entry_price - tp_price
                return {
                    'exit_time': bar_time,
                    'exit_price': tp_price,
                    'exit_type': 'TP',
                    'pnl_points': pnl_points,
                    'risk_r': risk_r
                }
    
    # Neither hit, force close at 07:00
    exit_data = df[df.index >= force_close_time]
    
    if len(exit_data) == 0:
        return None
    
    exit_price = exit_data.iloc[0]['Close']
    actual_exit_time = exit_data.index[0]
    
    if direction == 'LONG':
        pnl_points = exit_price - entry_price
    else:
        pnl_points = entry_price - exit_price
    
    return {
        'exit_time': actual_exit_time,
        'exit_price': exit_price,
        'exit_type': 'FORCE_CLOSE',
        'pnl_points': pnl_points,
        'risk_r': risk_r
    }


def run_comparison_backtest(df):
    """
    Run backtest comparing all 3 exit variants on the same entry signals.
    """
    dates = df.index.date
    unique_dates = sorted(set(dates))
    
    print(f"\n{'='*80}")
    print(f"Running comparison backtest from {unique_dates[0]} to {unique_dates[-1]}")
    print(f"Total trading days: {len(unique_dates)}")
    print(f"{'='*80}\n")
    
    # Store results for each variant
    results = {
        'A_Pure_Time': [],
        'B_Time_Catastrophe_SL': [],
        'C_Structure_SL_1.5R': [],
        'C_Structure_SL_2R': []
    }
    
    for i, date in enumerate(unique_dates[1:], 1):
        
        if i % 100 == 0:
            print(f"Processing: {date} ({i}/{len(unique_dates)-1})")
        
        # Step 1: Identify Asian Range
        asian_info = identify_asian_range(df, date)
        if asian_info is None:
            continue
        
        # Step 2: Detect breakout
        breakout_info = detect_breakout(df, date, asian_info)
        if breakout_info is None:
            continue
        
        # Step 3: Validate continuation (filter fake breakouts)
        if not validate_continuation(df, breakout_info):
            continue
        
        # Now we have a valid entry signal - test all 3 exit variants
        
        # Variant A: Pure Time Exit
        result_a = execute_variant_a(df, breakout_info)
        if result_a:
            trade_a = {
                'Date': date,
                'Entry_Time': breakout_info['entry_time'],
                'Direction': breakout_info['direction'],
                'Entry_Price': breakout_info['entry_price'],
                'Exit_Time': result_a['exit_time'],
                'Exit_Price': result_a['exit_price'],
                'Exit_Type': result_a['exit_type'],
                'PnL_Points': result_a['pnl_points']
            }
            results['A_Pure_Time'].append(trade_a)
        
        # Variant B: Time Exit + Catastrophe SL
        result_b = execute_variant_b(df, breakout_info)
        if result_b:
            trade_b = {
                'Date': date,
                'Entry_Time': breakout_info['entry_time'],
                'Direction': breakout_info['direction'],
                'Entry_Price': breakout_info['entry_price'],
                'Exit_Time': result_b['exit_time'],
                'Exit_Price': result_b['exit_price'],
                'Exit_Type': result_b['exit_type'],
                'PnL_Points': result_b['pnl_points']
            }
            results['B_Time_Catastrophe_SL'].append(trade_b)
        
        # Variant C1: Structure SL + 1.5R TP
        result_c15 = execute_variant_c(df, breakout_info, tp_r_multiple=1.5)
        if result_c15:
            trade_c15 = {
                'Date': date,
                'Entry_Time': breakout_info['entry_time'],
                'Direction': breakout_info['direction'],
                'Entry_Price': breakout_info['entry_price'],
                'Exit_Time': result_c15['exit_time'],
                'Exit_Price': result_c15['exit_price'],
                'Exit_Type': result_c15['exit_type'],
                'PnL_Points': result_c15['pnl_points'],
                'Risk_R': result_c15.get('risk_r', 0)
            }
            results['C_Structure_SL_1.5R'].append(trade_c15)
        
        # Variant C2: Structure SL + 2R TP
        result_c2 = execute_variant_c(df, breakout_info, tp_r_multiple=2.0)
        if result_c2:
            trade_c2 = {
                'Date': date,
                'Entry_Time': breakout_info['entry_time'],
                'Direction': breakout_info['direction'],
                'Entry_Price': breakout_info['entry_price'],
                'Exit_Time': result_c2['exit_time'],
                'Exit_Price': result_c2['exit_price'],
                'Exit_Type': result_c2['exit_type'],
                'PnL_Points': result_c2['pnl_points'],
                'Risk_R': result_c2.get('risk_r', 0)
            }
            results['C_Structure_SL_2R'].append(trade_c2)
    
    # Convert to DataFrames
    results_dfs = {}
    for variant, trades in results.items():
        if len(trades) > 0:
            results_dfs[variant] = pd.DataFrame(trades)
            print(f"\n{variant}: {len(trades)} trades")
        else:
            results_dfs[variant] = pd.DataFrame()
            print(f"\n{variant}: No trades")
    
    return results_dfs


def calculate_metrics(df_trades, variant_name):
    """Calculate comprehensive metrics for a variant."""
    if len(df_trades) == 0:
        return None
    
    total_trades = len(df_trades)
    wins = len(df_trades[df_trades['PnL_Points'] > 0])
    losses = len(df_trades[df_trades['PnL_Points'] < 0])
    breakevens = len(df_trades[df_trades['PnL_Points'] == 0])
    
    win_rate = (wins / total_trades * 100) if total_trades > 0 else 0
    
    total_pnl = df_trades['PnL_Points'].sum()
    avg_win = df_trades[df_trades['PnL_Points'] > 0]['PnL_Points'].mean() if wins > 0 else 0
    avg_loss = df_trades[df_trades['PnL_Points'] < 0]['PnL_Points'].mean() if losses > 0 else 0
    
    # Calculate max drawdown
    cumulative_pnl = df_trades['PnL_Points'].cumsum()
    running_max = cumulative_pnl.expanding().max()
    drawdown = cumulative_pnl - running_max
    max_drawdown_pts = drawdown.min()
    max_drawdown_pct = (max_drawdown_pts / running_max.max() * 100) if running_max.max() > 0 else 0
    
    # Profit factor
    gross_profit = df_trades[df_trades['PnL_Points'] > 0]['PnL_Points'].sum()
    gross_loss = abs(df_trades[df_trades['PnL_Points'] < 0]['PnL_Points'].sum())
    
    if gross_loss > 0:
        profit_factor = gross_profit / gross_loss
    elif gross_profit > 0:
        profit_factor = 999.0
    else:
        profit_factor = 0.0
    
    # Sharpe Ratio (simplified - using daily returns)
    daily_returns = df_trades['PnL_Points']
    if len(daily_returns) > 1 and daily_returns.std() > 0:
        sharpe_ratio = (daily_returns.mean() / daily_returns.std()) * np.sqrt(252)
    else:
        sharpe_ratio = 0.0
    
    # Expectancy
    expectancy = total_pnl / total_trades if total_trades > 0 else 0
    
    return {
        'Variant': variant_name,
        'Total_Trades': total_trades,
        'Wins': wins,
        'Losses': losses,
        'Breakevens': breakevens,
        'Win_Rate_%': round(win_rate, 2),
        'Net_Profit_Pts': round(total_pnl, 2),
        'Avg_Win_Pts': round(avg_win, 2),
        'Avg_Loss_Pts': round(avg_loss, 2),
        'Profit_Factor': round(profit_factor, 2),
        'Expectancy_Pts': round(expectancy, 2),
        'Max_DD_Pts': round(max_drawdown_pts, 2),
        'Max_DD_%': round(max_drawdown_pct, 2),
        'Sharpe_Ratio': round(sharpe_ratio, 2)
    }


def create_comparison_table(results_dfs):
    """Create comparison table for all variants."""
    comparison = []
    
    variant_names = {
        'A_Pure_Time': 'A) Pure Time Exit (07:00)',
        'B_Time_Catastrophe_SL': 'B) Time + Catastrophe SL (-100pts)',
        'C_Structure_SL_1.5R': 'C) Structure SL + 1.5R TP',
        'C_Structure_SL_2R': 'C) Structure SL + 2R TP'
    }
    
    for variant_key, df in results_dfs.items():
        variant_name = variant_names.get(variant_key, variant_key)
        metrics = calculate_metrics(df, variant_name)
        if metrics:
            comparison.append(metrics)
    
    if len(comparison) > 0:
        comparison_df = pd.DataFrame(comparison)
        return comparison_df
    else:
        return None


def plot_equity_curves(results_dfs):
    """Plot equity curves for all variants on same chart."""
    try:
        import matplotlib.pyplot as plt
        
        plt.figure(figsize=(14, 8))
        
        colors = {
            'A_Pure_Time': '#2E86AB',  # Blue
            'B_Time_Catastrophe_SL': '#A23B72',  # Purple
            'C_Structure_SL_1.5R': '#F18F01',  # Orange
            'C_Structure_SL_2R': '#C73E1D'  # Red
        }
        
        labels = {
            'A_Pure_Time': 'A) Pure Time Exit',
            'B_Time_Catastrophe_SL': 'B) Time + Catastrophe SL',
            'C_Structure_SL_1.5R': 'C) Structure SL + 1.5R',
            'C_Structure_SL_2R': 'C) Structure SL + 2R'
        }
        
        for variant_key, df in results_dfs.items():
            if len(df) > 0:
                cumulative_pnl = df['PnL_Points'].cumsum().values
                plt.plot(cumulative_pnl, 
                        label=labels.get(variant_key, variant_key),
                        color=colors.get(variant_key, 'black'),
                        linewidth=2.5,
                        alpha=0.9)
        
        plt.title('London Continuation - Exit Strategy Comparison\nCumulative P&L Over Time', 
                 fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Trade Number', fontsize=13)
        plt.ylabel('Cumulative P&L (Points)', fontsize=13)
        plt.legend(fontsize=11, loc='best', framealpha=0.9)
        plt.grid(True, alpha=0.3, linestyle='--')
        plt.axhline(y=0, color='black', linestyle='-', linewidth=0.8, alpha=0.5)
        
        # Add annotations
        plt.text(0.02, 0.98, 'Same Entry Signals\nDifferent Exit Management', 
                transform=plt.gca().transAxes,
                fontsize=10, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        plt.tight_layout()
        
        plot_file = Path.cwd() / 'london_exit_comparison_equity.png'
        plt.savefig(plot_file, dpi=150, bbox_inches='tight')
        print(f"\nEquity curve plot saved to: {plot_file}")
        
        return plot_file
        
    except ImportError:
        print("\nMatplotlib not available. Skipping equity curve plot.")
        return None


def main():
    """Main execution function."""
    print("="*80)
    print("LONDON CONTINUATION - EXIT STRATEGY COMPARISON")
    print("="*80)
    print("\nComparing 3 exit management approaches:")
    print("A) Pure Time Exit (07:00 CST) - No SL")
    print("B) Time Exit + Catastrophe SL (-100 pts)")
    print("C) Structure SL (Asian±2) + R:R TP (1.5R & 2R)")
    print("\nAll use SAME entry signals:")
    print("- Asian Range breakout during London Killzone (01:00-04:00)")
    print("- Volume > 20-period MA")
    print("- No >50% retracement validation")
    print("="*80)
    
    # Load data
    print("\nLoading NQ 15m data...")
    df = load_nq_data(timeframe='15m')
    
    # Run comparison backtest
    print("\nRunning comparison backtest...")
    results_dfs = run_comparison_backtest(df)
    
    # Create comparison table
    print("\n" + "="*80)
    print("PERFORMANCE COMPARISON")
    print("="*80)
    comparison_df = create_comparison_table(results_dfs)
    
    if comparison_df is not None:
        print("\n" + comparison_df.to_string(index=False))
        
        # Save comparison to CSV
        comparison_file = Path.cwd() / 'london_exit_comparison_table.csv'
        comparison_df.to_csv(comparison_file, index=False)
        print(f"\nComparison table saved to: {comparison_file}")
    else:
        print("\nNo results to compare.")
    
    # Save detailed results for each variant
    for variant, df in results_dfs.items():
        if len(df) > 0:
            output_file = Path.cwd() / f'london_exit_{variant}_results.csv'
            df.to_csv(output_file, index=False)
            print(f"Detailed {variant} results saved to: {output_file}")
    
    # Create equity curve comparison
    print("\n" + "="*80)
    print("EQUITY CURVES")
    print("="*80)
    plot_equity_curves(results_dfs)
    
    print("\n" + "="*80)
    print("COMPARISON COMPLETE")
    print("="*80)
    
    return results_dfs, comparison_df


if __name__ == "__main__":
    results_dfs, comparison_df = main()

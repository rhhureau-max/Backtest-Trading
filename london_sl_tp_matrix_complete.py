#!/usr/bin/env python3
"""
London Continuation - Complete SL/TP Matrix Backtest
Test 12 configurations: 3 Stop Loss × 4 Take Profit levels

Entry: Breakout of Asian Range (18:00-00:00 CST) during London Killzone (01:00-04:00 CST)
       with volume filter > MA(20)
       
Stop Loss variants:
1. Tokyo Equilibrium (Asian Mid)
2. -100 points
3. -50 points

Take Profit variants:
1. +50 points
2. +100 points
3. +150 points
4. +200 points

Exit: SL OR TP OR 08:00 CST (whichever comes first)
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
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


def check_continuation(df, entry_time, asian_range, direction):
    """Check if price stays on the correct side of Asian mid for 2 hours."""
    check_until = entry_time + timedelta(hours=2)
    check_data = df[(df.index > entry_time) & (df.index <= check_until)]
    
    if len(check_data) == 0:
        return True
    
    asian_mid = asian_range['asian_mid']
    
    if direction == 'LONG':
        if (check_data['Low'] < asian_mid).any():
            return False
    else:
        if (check_data['High'] > asian_mid).any():
            return False
    
    return True


def simulate_trade_sl_tp(df, entry_time, entry_price, direction, sl_price, tp_price, exit_time):
    """
    Simulate trade with both SL and TP.
    Returns (exit_price, exit_time, exit_type, pnl)
    """
    trade_data = df[(df.index > entry_time) & (df.index <= exit_time)]
    
    if len(trade_data) == 0:
        return entry_price, exit_time, 'TIME_EXIT', 0.0
    
    # Check each bar for SL or TP hit
    for idx, row in trade_data.iterrows():
        if direction == 'LONG':
            # Check TP first (favorable exit)
            if row['High'] >= tp_price:
                pnl = tp_price - entry_price
                return tp_price, idx, 'TAKE_PROFIT', pnl
            # Check SL
            if row['Low'] <= sl_price:
                pnl = sl_price - entry_price
                return sl_price, idx, 'STOP_LOSS', pnl
        else:  # SHORT
            # Check TP first (favorable exit)
            if row['Low'] <= tp_price:
                pnl = entry_price - tp_price
                return tp_price, idx, 'TAKE_PROFIT', pnl
            # Check SL
            if row['High'] >= sl_price:
                pnl = entry_price - sl_price
                return sl_price, idx, 'STOP_LOSS', pnl
    
    # Time exit at 08:00 CST
    exit_bar = trade_data.iloc[-1]
    exit_price = exit_bar['Close']
    
    if direction == 'LONG':
        pnl = exit_price - entry_price
    else:
        pnl = entry_price - exit_price
    
    return exit_price, exit_time, 'TIME_EXIT', pnl


def run_matrix_backtest(df):
    """
    Run backtest for all 12 SL/TP combinations.
    """
    df_sorted = df.sort_index()
    volume_ma = calculate_volume_ma(df_sorted)
    
    # Define SL and TP configurations
    sl_configs = {
        'Tokyo_EQ': 'tokyo_eq',
        '100pts': 100,
        '50pts': 50
    }
    
    tp_configs = {
        '50pts': 50,
        '100pts': 100,
        '150pts': 150,
        '200pts': 200
    }
    
    # Storage for all configurations
    all_results = {}
    
    for sl_name, sl_value in sl_configs.items():
        for tp_name, tp_value in tp_configs.items():
            config_name = f"SL_{sl_name}_TP_{tp_name}"
            all_results[config_name] = []
    
    dates = pd.date_range(start=df.index[0].date(), end=df.index[-1].date(), freq='D')
    
    print(f"\nAnalyzing {len(dates)} days for 12 configurations...")
    total_setups = 0
    
    for date in dates:
        # Identify Asian Range
        asian_range = identify_asian_range(df_sorted, date)
        if asian_range is None:
            continue
        
        # London Killzone: 01:00 - 04:00
        killzone_start = pd.Timestamp(year=date.year, month=date.month, day=date.day, hour=1, minute=0)
        killzone_end = pd.Timestamp(year=date.year, month=date.month, day=date.day, hour=4, minute=0)
        
        killzone_data = df_sorted[(df_sorted.index >= killzone_start) & (df_sorted.index <= killzone_end)]
        
        if len(killzone_data) == 0:
            continue
        
        # Check for breakout
        direction = None
        entry_time = None
        entry_price = None
        
        for idx, row in killzone_data.iterrows():
            if row['Volume'] <= volume_ma.loc[idx]:
                continue
            
            if row['Close'] > asian_range['asian_high']:
                direction = 'LONG'
                entry_time = idx
                entry_price = row['Close']
                break
            
            if row['Close'] < asian_range['asian_low']:
                direction = 'SHORT'
                entry_time = idx
                entry_price = row['Close']
                break
        
        if direction is None:
            continue
        
        # Check continuation validation
        if not check_continuation(df_sorted, entry_time, asian_range, direction):
            continue
        
        total_setups += 1
        
        # Exit time at 08:00 CST
        exit_time = pd.Timestamp(year=date.year, month=date.month, day=date.day, hour=8, minute=0)
        
        # Test all 12 configurations for this setup
        for sl_name, sl_value in sl_configs.items():
            # Calculate SL level
            if sl_value == 'tokyo_eq':
                sl_level = asian_range['asian_mid']
                sl_distance = abs(entry_price - sl_level)
            else:
                sl_distance = sl_value
                if direction == 'LONG':
                    sl_level = entry_price - sl_value
                else:
                    sl_level = entry_price + sl_value
            
            for tp_name, tp_value in tp_configs.items():
                # Calculate TP level
                if direction == 'LONG':
                    tp_level = entry_price + tp_value
                else:
                    tp_level = entry_price - tp_value
                
                # Simulate trade
                exit_price, actual_exit_time, exit_type, pnl = simulate_trade_sl_tp(
                    df_sorted, entry_time, entry_price, direction, sl_level, tp_level, exit_time
                )
                
                # Store trade result
                config_name = f"SL_{sl_name}_TP_{tp_name}"
                trade = {
                    'Date': date,
                    'Direction': direction,
                    'Entry_Time': entry_time,
                    'Entry_Price': entry_price,
                    'SL_Level': sl_level,
                    'SL_Distance': sl_distance,
                    'TP_Level': tp_level,
                    'TP_Distance': tp_value,
                    'Exit_Time': actual_exit_time,
                    'Exit_Price': exit_price,
                    'Exit_Type': exit_type,
                    'PnL_Points': pnl,
                    'Result': 'WIN' if pnl > 0 else 'LOSS',
                    'Asian_High': asian_range['asian_high'],
                    'Asian_Low': asian_range['asian_low'],
                    'Asian_Mid': asian_range['asian_mid']
                }
                all_results[config_name].append(trade)
    
    print(f"\nTotal valid setups: {total_setups}")
    
    return all_results


def calculate_metrics(trades_df):
    """Calculate performance metrics for a configuration."""
    if len(trades_df) == 0:
        return {}
    
    total_trades = len(trades_df)
    winning_trades = len(trades_df[trades_df['Result'] == 'WIN'])
    losing_trades = len(trades_df[trades_df['Result'] == 'LOSS'])
    
    win_rate = winning_trades / total_trades * 100 if total_trades > 0 else 0
    
    total_pnl = trades_df['PnL_Points'].sum()
    avg_win = trades_df[trades_df['Result'] == 'WIN']['PnL_Points'].mean() if winning_trades > 0 else 0
    avg_loss = trades_df[trades_df['Result'] == 'LOSS']['PnL_Points'].mean() if losing_trades > 0 else 0
    
    gross_profit = trades_df[trades_df['PnL_Points'] > 0]['PnL_Points'].sum()
    gross_loss = abs(trades_df[trades_df['PnL_Points'] < 0]['PnL_Points'].sum())
    profit_factor = gross_profit / gross_loss if gross_loss > 0 else float('inf')
    
    # Calculate equity curve for drawdown and Sharpe
    trades_df = trades_df.sort_values('Entry_Time')
    cumulative_pnl = trades_df['PnL_Points'].cumsum()
    
    # Max drawdown
    running_max = cumulative_pnl.cummax()
    drawdown = running_max - cumulative_pnl
    max_dd = drawdown.max()
    
    # Sharpe ratio (annualized, assuming ~250 trading days)
    if len(trades_df) > 1:
        returns = trades_df['PnL_Points']
        sharpe = (returns.mean() / returns.std() * np.sqrt(250)) if returns.std() > 0 else 0
    else:
        sharpe = 0
    
    # Exit type breakdown
    sl_exits = len(trades_df[trades_df['Exit_Type'] == 'STOP_LOSS'])
    tp_exits = len(trades_df[trades_df['Exit_Type'] == 'TAKE_PROFIT'])
    time_exits = len(trades_df[trades_df['Exit_Type'] == 'TIME_EXIT'])
    
    pct_sl = sl_exits / total_trades * 100 if total_trades > 0 else 0
    pct_tp = tp_exits / total_trades * 100 if total_trades > 0 else 0
    pct_time = time_exits / total_trades * 100 if total_trades > 0 else 0
    
    return {
        'Total_Trades': total_trades,
        'Winning_Trades': winning_trades,
        'Losing_Trades': losing_trades,
        'Win_Rate': win_rate,
        'Total_PnL': total_pnl,
        'Avg_Win': avg_win,
        'Avg_Loss': avg_loss,
        'Profit_Factor': profit_factor,
        'Max_Drawdown': max_dd,
        'Sharpe_Ratio': sharpe,
        'SL_Exits': sl_exits,
        'TP_Exits': tp_exits,
        'Time_Exits': time_exits,
        'Pct_SL': pct_sl,
        'Pct_TP': pct_tp,
        'Pct_Time': pct_time
    }


def generate_comparison_table(all_results):
    """Generate comparison table for all configurations."""
    comparison_data = []
    
    for config_name, trades in all_results.items():
        if len(trades) == 0:
            continue
        
        trades_df = pd.DataFrame(trades)
        metrics = calculate_metrics(trades_df)
        
        # Parse config name
        parts = config_name.split('_')
        sl_type = parts[1]
        tp_value = parts[3]
        
        row = {
            'Configuration': config_name,
            'SL_Type': sl_type,
            'TP_Value': tp_value,
            **metrics
        }
        comparison_data.append(row)
    
    comparison_df = pd.DataFrame(comparison_data)
    
    # Sort by Total PnL descending
    comparison_df = comparison_df.sort_values('Total_PnL', ascending=False)
    
    return comparison_df


def plot_equity_curves(all_results, output_file='sl_tp_matrix_equity.png'):
    """Plot equity curves for all 12 configurations."""
    fig, ax = plt.subplots(figsize=(16, 10))
    
    # Color mapping for SL types
    sl_colors = {
        'Tokyo': '#1f77b4',
        '100pts': '#ff7f0e',
        '50pts': '#2ca02c'
    }
    
    # Line styles for TP values
    tp_styles = {
        '50pts': '-',
        '100pts': '--',
        '150pts': '-.',
        '200pts': ':'
    }
    
    for config_name, trades in all_results.items():
        if len(trades) == 0:
            continue
        
        trades_df = pd.DataFrame(trades)
        trades_df = trades_df.sort_values('Entry_Time')
        
        cumulative_pnl = trades_df['PnL_Points'].cumsum()
        
        # Parse config for styling
        parts = config_name.split('_')
        sl_type = parts[1]
        tp_value = parts[3]
        
        color = sl_colors.get(sl_type, '#000000')
        linestyle = tp_styles.get(tp_value, '-')
        
        ax.plot(range(len(cumulative_pnl)), cumulative_pnl.values, 
                label=config_name, color=color, linestyle=linestyle, linewidth=1.5, alpha=0.8)
    
    ax.axhline(y=0, color='red', linestyle='--', linewidth=1, alpha=0.5)
    ax.set_xlabel('Trade Number', fontsize=12, fontweight='bold')
    ax.set_ylabel('Cumulative P&L (Points)', fontsize=12, fontweight='bold')
    ax.set_title('London Continuation - SL/TP Matrix Equity Curves', fontsize=14, fontweight='bold')
    ax.legend(loc='best', fontsize=8, ncol=2)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"\nEquity curves saved to: {output_file}")
    plt.close()


def generate_markdown_report(comparison_df, all_results, output_file='SL_TP_MATRIX_RESULTS.md'):
    """Generate comprehensive markdown report."""
    
    with open(output_file, 'w') as f:
        f.write("# London Continuation - SL/TP Matrix Complete Results\n\n")
        f.write("**Strategy:** London Continuation with Volume Filter\n\n")
        f.write("**Entry:** Breakout of Asian Range (18:00-00:00 CST) during London Killzone (01:00-04:00 CST) with Volume > MA(20)\n\n")
        f.write("**Exit:** Stop Loss OR Take Profit OR 08:00 CST (whichever comes first)\n\n")
        f.write(f"**Period:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("---\n\n")
        
        f.write("## Executive Summary\n\n")
        
        # Top 3 configurations
        top3 = comparison_df.head(3)
        f.write("### Top 3 Configurations (by Total P&L)\n\n")
        
        for idx, row in top3.iterrows():
            f.write(f"**{idx + 1}. {row['Configuration']}**\n")
            f.write(f"- Total P&L: **{row['Total_PnL']:.2f} points**\n")
            f.write(f"- Win Rate: {row['Win_Rate']:.2f}%\n")
            f.write(f"- Profit Factor: {row['Profit_Factor']:.2f}\n")
            f.write(f"- Sharpe Ratio: {row['Sharpe_Ratio']:.2f}\n")
            f.write(f"- Max Drawdown: {row['Max_Drawdown']:.2f} points\n")
            f.write(f"- Exit Distribution: TP={row['Pct_TP']:.1f}% | SL={row['Pct_SL']:.1f}% | Time={row['Pct_Time']:.1f}%\n\n")
        
        f.write("---\n\n")
        
        f.write("## Complete Performance Matrix\n\n")
        
        # Full comparison table
        f.write("| Configuration | Trades | Win Rate | Total P&L | Avg Win | Avg Loss | Profit Factor | Sharpe | Max DD | TP% | SL% | Time% |\n")
        f.write("|--------------|--------|----------|-----------|---------|----------|---------------|--------|--------|-----|-----|-------|\n")
        
        for idx, row in comparison_df.iterrows():
            f.write(f"| {row['Configuration']} | {row['Total_Trades']} | ")
            f.write(f"{row['Win_Rate']:.1f}% | {row['Total_PnL']:.1f} | ")
            f.write(f"{row['Avg_Win']:.1f} | {row['Avg_Loss']:.1f} | ")
            f.write(f"{row['Profit_Factor']:.2f} | {row['Sharpe_Ratio']:.2f} | ")
            f.write(f"{row['Max_Drawdown']:.1f} | ")
            f.write(f"{row['Pct_TP']:.1f}% | {row['Pct_SL']:.1f}% | {row['Pct_Time']:.1f}% |\n")
        
        f.write("\n---\n\n")
        
        f.write("## Analysis by Stop Loss Type\n\n")
        
        # Group by SL type
        for sl_type in ['Tokyo', '100pts', '50pts']:
            sl_configs = comparison_df[comparison_df['SL_Type'] == sl_type]
            if len(sl_configs) == 0:
                continue
            
            f.write(f"### Stop Loss: {sl_type}\n\n")
            
            avg_pnl = sl_configs['Total_PnL'].mean()
            avg_wr = sl_configs['Win_Rate'].mean()
            avg_pf = sl_configs['Profit_Factor'].mean()
            
            f.write(f"**Average Performance across all TP levels:**\n")
            f.write(f"- Average Total P&L: {avg_pnl:.2f} points\n")
            f.write(f"- Average Win Rate: {avg_wr:.2f}%\n")
            f.write(f"- Average Profit Factor: {avg_pf:.2f}\n\n")
            
            f.write("| TP Level | Total P&L | Win Rate | Profit Factor | Max DD |\n")
            f.write("|----------|-----------|----------|---------------|--------|\n")
            
            for idx, row in sl_configs.iterrows():
                f.write(f"| {row['TP_Value']} | {row['Total_PnL']:.1f} | ")
                f.write(f"{row['Win_Rate']:.1f}% | {row['Profit_Factor']:.2f} | ")
                f.write(f"{row['Max_Drawdown']:.1f} |\n")
            
            f.write("\n")
        
        f.write("---\n\n")
        
        f.write("## Analysis by Take Profit Level\n\n")
        
        # Group by TP level
        for tp_value in ['50pts', '100pts', '150pts', '200pts']:
            tp_configs = comparison_df[comparison_df['TP_Value'] == tp_value]
            if len(tp_configs) == 0:
                continue
            
            f.write(f"### Take Profit: {tp_value}\n\n")
            
            avg_pnl = tp_configs['Total_PnL'].mean()
            avg_wr = tp_configs['Win_Rate'].mean()
            avg_pf = tp_configs['Profit_Factor'].mean()
            
            f.write(f"**Average Performance across all SL types:**\n")
            f.write(f"- Average Total P&L: {avg_pnl:.2f} points\n")
            f.write(f"- Average Win Rate: {avg_wr:.2f}%\n")
            f.write(f"- Average Profit Factor: {avg_pf:.2f}\n\n")
            
            f.write("| SL Type | Total P&L | Win Rate | Profit Factor | Max DD |\n")
            f.write("|---------|-----------|----------|---------------|--------|\n")
            
            for idx, row in tp_configs.iterrows():
                f.write(f"| {row['SL_Type']} | {row['Total_PnL']:.1f} | ")
                f.write(f"{row['Win_Rate']:.1f}% | {row['Profit_Factor']:.2f} | ")
                f.write(f"{row['Max_Drawdown']:.1f} |\n")
            
            f.write("\n")
        
        f.write("---\n\n")
        
        f.write("## Key Insights\n\n")
        
        best_config = comparison_df.iloc[0]
        worst_config = comparison_df.iloc[-1]
        
        f.write(f"1. **Best Configuration:** {best_config['Configuration']} with {best_config['Total_PnL']:.2f} points total P&L\n")
        f.write(f"2. **Worst Configuration:** {worst_config['Configuration']} with {worst_config['Total_PnL']:.2f} points total P&L\n")
        f.write(f"3. **Performance Range:** {best_config['Total_PnL'] - worst_config['Total_PnL']:.2f} points difference between best and worst\n")
        
        # Calculate averages by SL
        sl_avg_pnl = comparison_df.groupby('SL_Type')['Total_PnL'].mean().sort_values(ascending=False)
        f.write(f"4. **Best SL Type (by avg P&L):** {sl_avg_pnl.index[0]} ({sl_avg_pnl.iloc[0]:.2f} points avg)\n")
        
        # Calculate averages by TP
        tp_avg_pnl = comparison_df.groupby('TP_Value')['Total_PnL'].mean().sort_values(ascending=False)
        f.write(f"5. **Best TP Level (by avg P&L):** {tp_avg_pnl.index[0]} ({tp_avg_pnl.iloc[0]:.2f} points avg)\n")
        
        f.write("\n---\n\n")
        f.write("## Files Generated\n\n")
        f.write("- `SL_TP_MATRIX_RESULTS.md` - This comprehensive report\n")
        f.write("- `sl_tp_matrix_equity.png` - Equity curves for all 12 configurations\n")
        f.write("- `SL_<type>_TP_<value>_trades.csv` - Detailed trade logs for each configuration (12 files)\n")
        
    print(f"\nMarkdown report saved to: {output_file}")


def main():
    """Main execution function."""
    print("=" * 80)
    print("LONDON CONTINUATION - COMPLETE SL/TP MATRIX BACKTEST")
    print("=" * 80)
    print("\nTesting 12 configurations: 3 Stop Loss × 4 Take Profit levels")
    print("\nStop Loss variants:")
    print("  1. Tokyo Equilibrium (Asian Mid)")
    print("  2. -100 points")
    print("  3. -50 points")
    print("\nTake Profit variants:")
    print("  1. +50 points")
    print("  2. +100 points")
    print("  3. +150 points")
    print("  4. +200 points")
    print("\nExit: SL OR TP OR 08:00 CST (whichever comes first)")
    print("=" * 80)
    
    # Load data
    print("\nLoading NQ 15m data...")
    base_path = Path('/home/runner/work/Backtest-Trading/Backtest-Trading')
    df = load_nq_data(years=range(2018, 2026), timeframe='15m', base_path=base_path)
    
    # Run matrix backtest
    print("\n" + "=" * 80)
    print("RUNNING MATRIX BACKTEST...")
    print("=" * 80)
    all_results = run_matrix_backtest(df)
    
    # Save individual CSV files
    print("\n" + "=" * 80)
    print("SAVING DETAILED TRADE FILES...")
    print("=" * 80)
    for config_name, trades in all_results.items():
        if len(trades) > 0:
            trades_df = pd.DataFrame(trades)
            csv_filename = f"{config_name}_trades.csv"
            trades_df.to_csv(csv_filename, index=False)
            print(f"Saved: {csv_filename} ({len(trades)} trades)")
    
    # Generate comparison table
    print("\n" + "=" * 80)
    print("GENERATING COMPARISON TABLE...")
    print("=" * 80)
    comparison_df = generate_comparison_table(all_results)
    comparison_df.to_csv('sl_tp_matrix_comparison.csv', index=False)
    print("\nComparison table saved to: sl_tp_matrix_comparison.csv")
    
    # Print summary to console
    print("\n" + "=" * 80)
    print("PERFORMANCE SUMMARY")
    print("=" * 80)
    print("\nTop 5 Configurations by Total P&L:")
    print("-" * 80)
    for idx, row in comparison_df.head(5).iterrows():
        print(f"{idx + 1}. {row['Configuration']}")
        print(f"   Total P&L: {row['Total_PnL']:.2f} pts | Win Rate: {row['Win_Rate']:.1f}% | " +
              f"PF: {row['Profit_Factor']:.2f} | Sharpe: {row['Sharpe_Ratio']:.2f}")
        print(f"   Exits: TP={row['Pct_TP']:.1f}% SL={row['Pct_SL']:.1f}% Time={row['Pct_Time']:.1f}%")
        print()
    
    # Generate equity curve plot
    print("=" * 80)
    print("GENERATING EQUITY CURVES...")
    print("=" * 80)
    plot_equity_curves(all_results)
    
    # Generate markdown report
    print("\n" + "=" * 80)
    print("GENERATING MARKDOWN REPORT...")
    print("=" * 80)
    generate_markdown_report(comparison_df, all_results)
    
    print("\n" + "=" * 80)
    print("BACKTEST COMPLETE!")
    print("=" * 80)
    print("\nAll files generated successfully:")
    print("  ✓ SL_TP_MATRIX_RESULTS.md - Comprehensive analysis report")
    print("  ✓ sl_tp_matrix_equity.png - Equity curves visualization")
    print("  ✓ sl_tp_matrix_comparison.csv - Comparison table")
    print("  ✓ 12 detailed trade CSV files")
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()

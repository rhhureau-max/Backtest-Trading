#!/usr/bin/env python3
"""
London Continuation - Stop Loss Comparison Analysis
Compare 3 different Stop Loss placements with the same exit time (07:00 CST):
1) SL at Tokyo Equilibrium (50% of Asian Range)
2) SL at -100 points (Catastrophe SL)
3) SL at -50 points (Intermediate SL)

All use the same entry logic and exit at 07:00 CST unless SL is hit.
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
        # For LONG, price should NOT go below Asian mid
        if (check_data['Low'] < asian_mid).any():
            return False
    else:
        # For SHORT, price should NOT go above Asian mid
        if (check_data['High'] > asian_mid).any():
            return False
    
    return True


def simulate_trade_with_sl(df, entry_time, entry_price, direction, sl_price, exit_time):
    """
    Simulate trade execution from entry to exit or SL hit.
    Returns (exit_price, exit_time, exit_type, pnl)
    """
    # Get data from entry to planned exit
    trade_data = df[(df.index > entry_time) & (df.index <= exit_time)]
    
    if len(trade_data) == 0:
        # No data, assume time exit
        return entry_price, exit_time, 'TIME_EXIT', 0.0
    
    # Check each bar to see if SL is hit
    for idx, row in trade_data.iterrows():
        if direction == 'LONG':
            # Check if Low touches SL
            if row['Low'] <= sl_price:
                pnl = sl_price - entry_price
                return sl_price, idx, 'STOP_LOSS', pnl
        else:  # SHORT
            # Check if High touches SL
            if row['High'] >= sl_price:
                pnl = entry_price - sl_price
                return sl_price, idx, 'STOP_LOSS', pnl
    
    # If we reach here, SL was not hit, exit at planned time
    exit_bar = trade_data.iloc[-1]
    exit_price = exit_bar['Close']
    
    if direction == 'LONG':
        pnl = exit_price - entry_price
    else:
        pnl = entry_price - exit_price
    
    return exit_price, exit_time, 'TIME_EXIT', pnl


def run_backtest_with_sl_variants(df):
    """
    Run backtest comparing 3 SL variants:
    1) Tokyo Equilibrium SL
    2) -100 points SL
    3) -50 points SL
    """
    df_sorted = df.sort_index()
    volume_ma = calculate_volume_ma(df_sorted)
    
    trades_eq = []    # Tokyo Equilibrium SL
    trades_100 = []   # -100 points SL
    trades_50 = []    # -50 points SL
    
    dates = pd.date_range(start=df.index[0].date(), end=df.index[-1].date(), freq='D')
    
    print(f"\nAnalyzing {len(dates)} days...")
    
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
            # Check volume filter
            if row['Volume'] <= volume_ma.loc[idx]:
                continue
            
            # Check bullish breakout
            if row['Close'] > asian_range['asian_high']:
                direction = 'LONG'
                entry_time = idx
                entry_price = row['Close']
                break
            
            # Check bearish breakout
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
        
        # Define exit time (07:00 CST)
        exit_time = pd.Timestamp(year=date.year, month=date.month, day=date.day, hour=7, minute=0)
        
        # Calculate SL levels for each variant
        # Variant 1: Tokyo Equilibrium (Asian Mid)
        sl_eq = asian_range['asian_mid']
        
        # Variant 2: -100 points
        if direction == 'LONG':
            sl_100 = entry_price - 100
        else:
            sl_100 = entry_price + 100
        
        # Variant 3: -50 points
        if direction == 'LONG':
            sl_50 = entry_price - 50
        else:
            sl_50 = entry_price + 50
        
        # Simulate trade for each variant
        exit_price_eq, exit_time_eq, exit_type_eq, pnl_eq = simulate_trade_with_sl(
            df_sorted, entry_time, entry_price, direction, sl_eq, exit_time
        )
        
        exit_price_100, exit_time_100, exit_type_100, pnl_100 = simulate_trade_with_sl(
            df_sorted, entry_time, entry_price, direction, sl_100, exit_time
        )
        
        exit_price_50, exit_time_50, exit_type_50, pnl_50 = simulate_trade_with_sl(
            df_sorted, entry_time, entry_price, direction, sl_50, exit_time
        )
        
        # Store results
        base_trade = {
            'Date': date,
            'Direction': direction,
            'Entry_Time': entry_time,
            'Entry_Price': entry_price,
            'Asian_High': asian_range['asian_high'],
            'Asian_Low': asian_range['asian_low'],
            'Asian_Mid': asian_range['asian_mid'],
        }
        
        # Tokyo Equilibrium variant
        trade_eq = base_trade.copy()
        trade_eq.update({
            'SL_Level': sl_eq,
            'SL_Distance': abs(entry_price - sl_eq),
            'Exit_Time': exit_time_eq,
            'Exit_Price': exit_price_eq,
            'Exit_Type': exit_type_eq,
            'PnL_Points': pnl_eq,
            'Result': 'WIN' if pnl_eq > 0 else 'LOSS'
        })
        trades_eq.append(trade_eq)
        
        # -100 points variant
        trade_100 = base_trade.copy()
        trade_100.update({
            'SL_Level': sl_100,
            'SL_Distance': 100.0,
            'Exit_Time': exit_time_100,
            'Exit_Price': exit_price_100,
            'Exit_Type': exit_type_100,
            'PnL_Points': pnl_100,
            'Result': 'WIN' if pnl_100 > 0 else 'LOSS'
        })
        trades_100.append(trade_100)
        
        # -50 points variant
        trade_50 = base_trade.copy()
        trade_50.update({
            'SL_Level': sl_50,
            'SL_Distance': 50.0,
            'Exit_Time': exit_time_50,
            'Exit_Price': exit_price_50,
            'Exit_Type': exit_type_50,
            'PnL_Points': pnl_50,
            'Result': 'WIN' if pnl_50 > 0 else 'LOSS'
        })
        trades_50.append(trade_50)
    
    df_eq = pd.DataFrame(trades_eq)
    df_100 = pd.DataFrame(trades_100)
    df_50 = pd.DataFrame(trades_50)
    
    return df_eq, df_100, df_50


def calculate_metrics(df_trades, variant_name):
    """Calculate performance metrics for a trading variant."""
    if len(df_trades) == 0:
        return None
    
    total_trades = len(df_trades)
    wins = df_trades[df_trades['Result'] == 'WIN']
    losses = df_trades[df_trades['Result'] == 'LOSS']
    
    num_wins = len(wins)
    num_losses = len(losses)
    win_rate = (num_wins / total_trades * 100) if total_trades > 0 else 0
    
    total_pnl = df_trades['PnL_Points'].sum()
    
    avg_win = wins['PnL_Points'].mean() if len(wins) > 0 else 0
    avg_loss = losses['PnL_Points'].mean() if len(losses) > 0 else 0
    
    gross_profit = wins['PnL_Points'].sum() if len(wins) > 0 else 0
    gross_loss = abs(losses['PnL_Points'].sum()) if len(losses) > 0 else 0
    
    profit_factor = (gross_profit / gross_loss) if gross_loss > 0 else float('inf')
    
    expectancy = total_pnl / total_trades if total_trades > 0 else 0
    
    # Calculate drawdown
    df_trades_sorted = df_trades.sort_values('Entry_Time')
    cumulative_pnl = df_trades_sorted['PnL_Points'].cumsum()
    running_max = cumulative_pnl.expanding().max()
    drawdown = cumulative_pnl - running_max
    max_dd = drawdown.min()
    max_dd_pct = (max_dd / running_max.max() * 100) if running_max.max() > 0 else 0
    
    # Sharpe Ratio approximation
    returns = df_trades_sorted['PnL_Points']
    sharpe = (returns.mean() / returns.std() * np.sqrt(252)) if returns.std() > 0 else 0
    
    # SL hit statistics
    sl_hits = len(df_trades[df_trades['Exit_Type'] == 'STOP_LOSS'])
    time_exits = len(df_trades[df_trades['Exit_Type'] == 'TIME_EXIT'])
    
    sl_hit_rate = (sl_hits / total_trades * 100) if total_trades > 0 else 0
    
    # Average SL distance
    avg_sl_distance = df_trades['SL_Distance'].mean()
    
    return {
        'Variant': variant_name,
        'Total_Trades': total_trades,
        'Wins': num_wins,
        'Losses': num_losses,
        'Win_Rate_%': round(win_rate, 2),
        'Total_PnL_Points': round(total_pnl, 2),
        'Avg_Win': round(avg_win, 2),
        'Avg_Loss': round(avg_loss, 2),
        'Profit_Factor': round(profit_factor, 2),
        'Expectancy': round(expectancy, 2),
        'Max_DD_Points': round(max_dd, 2),
        'Max_DD_%': round(max_dd_pct, 2),
        'Sharpe_Ratio': round(sharpe, 2),
        'SL_Hits': sl_hits,
        'Time_Exits': time_exits,
        'SL_Hit_Rate_%': round(sl_hit_rate, 2),
        'Avg_SL_Distance': round(avg_sl_distance, 2)
    }


def plot_equity_curves(df_eq, df_100, df_50):
    """Plot equity curves for all 3 SL variants."""
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Sort by entry time
    df_eq_sorted = df_eq.sort_values('Entry_Time')
    df_100_sorted = df_100.sort_values('Entry_Time')
    df_50_sorted = df_50.sort_values('Entry_Time')
    
    # Calculate cumulative P&L
    cum_pnl_eq = df_eq_sorted['PnL_Points'].cumsum()
    cum_pnl_100 = df_100_sorted['PnL_Points'].cumsum()
    cum_pnl_50 = df_50_sorted['PnL_Points'].cumsum()
    
    # Plot
    ax.plot(range(len(cum_pnl_eq)), cum_pnl_eq.values, label='1) Tokyo Equilibrium SL', linewidth=2)
    ax.plot(range(len(cum_pnl_100)), cum_pnl_100.values, label='2) -100 Points SL', linewidth=2)
    ax.plot(range(len(cum_pnl_50)), cum_pnl_50.values, label='3) -50 Points SL', linewidth=2)
    
    ax.set_xlabel('Trade Number', fontsize=12)
    ax.set_ylabel('Cumulative P&L (Points)', fontsize=12)
    ax.set_title('London Continuation - Stop Loss Comparison\nSame Entry Signals, Different SL Placement', fontsize=14, fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('london_sl_comparison_equity.png', dpi=150, bbox_inches='tight')
    print("\nEquity curve saved: london_sl_comparison_equity.png")
    
    return fig


def main():
    """Main execution function."""
    print("=" * 80)
    print("LONDON CONTINUATION - STOP LOSS COMPARISON ANALYSIS")
    print("=" * 80)
    print("\nComparing 3 Stop Loss placements:")
    print("1) Tokyo Equilibrium (Asian Mid)")
    print("2) -100 Points (Catastrophe SL)")
    print("3) -50 Points (Intermediate SL)")
    print("\nAll exit at 07:00 CST unless SL is hit first")
    print("=" * 80)
    
    # Load data
    print("\n📊 Loading NQ 15m data...")
    df = load_nq_data(timeframe='15m')
    
    # Run backtest
    print("\n🔄 Running backtest for all 3 SL variants...")
    df_eq, df_100, df_50 = run_backtest_with_sl_variants(df)
    
    print(f"\n✅ Found {len(df_eq)} valid setups")
    
    # Calculate metrics
    print("\n📈 Calculating performance metrics...")
    metrics_eq = calculate_metrics(df_eq, "1) Tokyo Equilibrium SL")
    metrics_100 = calculate_metrics(df_100, "2) -100 Points SL")
    metrics_50 = calculate_metrics(df_50, "3) -50 Points SL")
    
    # Create comparison table
    comparison_df = pd.DataFrame([metrics_eq, metrics_100, metrics_50])
    
    # Display results
    print("\n" + "=" * 120)
    print("PERFORMANCE COMPARISON - ALL 3 SL VARIANTS")
    print("=" * 120)
    print(comparison_df.to_string(index=False))
    print("=" * 120)
    
    # Save results
    comparison_df.to_csv('london_sl_comparison_table.csv', index=False)
    print("\n💾 Comparison table saved: london_sl_comparison_table.csv")
    
    df_eq.to_csv('london_sl_1_Tokyo_EQ_results.csv', index=False)
    print("💾 Detailed results saved: london_sl_1_Tokyo_EQ_results.csv")
    
    df_100.to_csv('london_sl_2_100pts_results.csv', index=False)
    print("💾 Detailed results saved: london_sl_2_100pts_results.csv")
    
    df_50.to_csv('london_sl_3_50pts_results.csv', index=False)
    print("💾 Detailed results saved: london_sl_3_50pts_results.csv")
    
    # Plot equity curves
    print("\n📊 Generating equity curves...")
    plot_equity_curves(df_eq, df_100, df_50)
    
    # Print key insights
    print("\n" + "=" * 80)
    print("🔍 KEY INSIGHTS")
    print("=" * 80)
    
    best_pnl = max(metrics_eq['Total_PnL_Points'], metrics_100['Total_PnL_Points'], metrics_50['Total_PnL_Points'])
    if metrics_eq['Total_PnL_Points'] == best_pnl:
        best = "Tokyo Equilibrium"
    elif metrics_100['Total_PnL_Points'] == best_pnl:
        best = "-100 Points"
    else:
        best = "-50 Points"
    
    print(f"\n✅ Best P&L: {best} SL with {best_pnl:+.2f} points")
    
    print(f"\n📊 SL Hit Rates:")
    print(f"   - Tokyo Equilibrium: {metrics_eq['SL_Hit_Rate_%']:.1f}% ({metrics_eq['SL_Hits']} hits)")
    print(f"   - 100 Points: {metrics_100['SL_Hit_Rate_%']:.1f}% ({metrics_100['SL_Hits']} hits)")
    print(f"   - 50 Points: {metrics_50['SL_Hit_Rate_%']:.1f}% ({metrics_50['SL_Hits']} hits)")
    
    print(f"\n📊 Average SL Distances:")
    print(f"   - Tokyo Equilibrium: {metrics_eq['Avg_SL_Distance']:.2f} points")
    print(f"   - 100 Points: {metrics_100['Avg_SL_Distance']:.2f} points")
    print(f"   - 50 Points: {metrics_50['Avg_SL_Distance']:.2f} points")
    
    print("\n" + "=" * 80)
    print("✅ Analysis complete!")
    print("=" * 80)


if __name__ == "__main__":
    main()

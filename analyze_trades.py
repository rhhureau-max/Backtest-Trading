"""
Trade Analysis Utilities

This script provides additional analysis tools for the backtest results.
"""

import pandas as pd
import numpy as np
from nq_backtest_strategy import FVGBacktester


def analyze_by_time_of_day(backtester):
    """Analyze performance by time of day"""
    if not backtester.trades:
        print("No trades to analyze")
        return
    
    trades_df = pd.DataFrame(backtester.trades)
    trades_df['entry_hour'] = pd.to_datetime(trades_df['entry_time']).dt.hour
    
    print("\n" + "="*60)
    print("PERFORMANCE BY HOUR OF ENTRY")
    print("="*60)
    
    hourly_stats = trades_df.groupby('entry_hour').agg({
        'pnl': ['count', 'sum', 'mean'],
        'bars_in_trade': 'mean'
    }).round(2)
    
    print(hourly_stats)
    
    # Calculate win rate by hour
    win_rate_by_hour = trades_df.groupby('entry_hour').apply(
        lambda x: (x['pnl'] > 0).sum() / len(x) * 100
    )
    
    print("\nWin Rate by Hour:")
    for hour, rate in win_rate_by_hour.items():
        print(f"  {hour:02d}:00 - {rate:.2f}%")


def analyze_consecutive_wins_losses(backtester):
    """Analyze streaks of consecutive wins/losses"""
    if not backtester.trades:
        print("No trades to analyze")
        return
    
    trades_df = pd.DataFrame(backtester.trades)
    trades_df['win'] = trades_df['pnl'] > 0
    
    # Find streaks
    streaks = []
    current_streak = 1
    current_type = trades_df['win'].iloc[0]
    
    for i in range(1, len(trades_df)):
        if trades_df['win'].iloc[i] == current_type:
            current_streak += 1
        else:
            streaks.append((current_type, current_streak))
            current_streak = 1
            current_type = trades_df['win'].iloc[i]
    
    streaks.append((current_type, current_streak))
    
    winning_streaks = [s[1] for s in streaks if s[0]]
    losing_streaks = [s[1] for s in streaks if not s[0]]
    
    print("\n" + "="*60)
    print("STREAK ANALYSIS")
    print("="*60)
    print(f"Longest winning streak: {max(winning_streaks) if winning_streaks else 0} trades")
    print(f"Average winning streak: {np.mean(winning_streaks) if winning_streaks else 0:.2f} trades")
    print(f"Longest losing streak: {max(losing_streaks) if losing_streaks else 0} trades")
    print(f"Average losing streak: {np.mean(losing_streaks) if losing_streaks else 0:.2f} trades")


def analyze_monthly_performance(backtester):
    """Analyze performance by month and year"""
    if not backtester.trades:
        print("No trades to analyze")
        return
    
    trades_df = pd.DataFrame(backtester.trades)
    trades_df['entry_time'] = pd.to_datetime(trades_df['entry_time'])
    trades_df['year_month'] = trades_df['entry_time'].dt.to_period('M')
    
    print("\n" + "="*60)
    print("MONTHLY PERFORMANCE")
    print("="*60)
    
    monthly_stats = trades_df.groupby('year_month').agg({
        'pnl': ['count', 'sum', 'mean']
    }).round(2)
    
    print(monthly_stats)
    
    # Calculate cumulative PnL by month
    monthly_cumsum = trades_df.groupby('year_month')['pnl'].sum().cumsum()
    
    print("\n" + "="*60)
    print("CUMULATIVE PNL BY MONTH")
    print("="*60)
    for period, cum_pnl in monthly_cumsum.items():
        print(f"{period}: {cum_pnl:.2f} points")


def analyze_trade_duration(backtester):
    """Analyze trade duration patterns"""
    if not backtester.trades:
        print("No trades to analyze")
        return
    
    trades_df = pd.DataFrame(backtester.trades)
    
    print("\n" + "="*60)
    print("TRADE DURATION ANALYSIS")
    print("="*60)
    
    # Duration in minutes (each bar is 5 minutes)
    trades_df['duration_minutes'] = trades_df['bars_in_trade'] * 5
    
    print(f"Minimum duration: {trades_df['duration_minutes'].min()} minutes")
    print(f"Maximum duration: {trades_df['duration_minutes'].max()} minutes")
    print(f"Average duration: {trades_df['duration_minutes'].mean():.2f} minutes")
    print(f"Median duration: {trades_df['duration_minutes'].median()} minutes")
    
    # Correlation between duration and PnL
    correlation = trades_df['duration_minutes'].corr(trades_df['pnl'])
    print(f"\nCorrelation between duration and PnL: {correlation:.3f}")
    
    # Average PnL by duration buckets
    trades_df['duration_bucket'] = pd.cut(
        trades_df['duration_minutes'],
        bins=[0, 30, 60, 120, 240, float('inf')],
        labels=['0-30min', '30-60min', '1-2hr', '2-4hr', '4hr+']
    )
    
    print("\nPnL by duration bucket:")
    duration_stats = trades_df.groupby('duration_bucket').agg({
        'pnl': ['count', 'mean', 'sum']
    }).round(2)
    print(duration_stats)


def full_analysis(data_dir, tp_strategy='2R'):
    """Run complete analysis on a strategy"""
    print(f"\n{'='*80}")
    print(f"COMPREHENSIVE ANALYSIS FOR {tp_strategy} STRATEGY")
    print(f"{'='*80}")
    
    # Run backtest
    backtester = FVGBacktester(data_dir, tp_multiplier=tp_strategy)
    backtester.load_data()
    backtester.run_backtest()
    stats = backtester.calculate_statistics()
    backtester.print_results(stats)
    
    # Additional analyses
    analyze_by_time_of_day(backtester)
    analyze_consecutive_wins_losses(backtester)
    analyze_trade_duration(backtester)
    analyze_monthly_performance(backtester)


if __name__ == "__main__":
    # Run full analysis on 2R strategy (best performer)
    data_dir = "/home/runner/work/Backtest-Trading/Backtest-Trading"
    full_analysis(data_dir, tp_strategy='2R')

"""
Quick Statistics Summary for FVG Inversion Backtest
Provides additional insights without requiring matplotlib
"""

import pandas as pd
from datetime import datetime

def analyze_trades(csv_file='fvg_inversion_trades.csv'):
    """
    Analyze the trades CSV and provide detailed insights
    """
    # Load trades
    df = pd.read_csv(csv_file)
    
    # Convert dates
    df['Entry Date'] = pd.to_datetime(df['Entry Date'])
    df['Exit Date'] = pd.to_datetime(df['Exit Date'])
    
    # Add year column
    df['Year'] = df['Entry Date'].dt.year
    
    # Add trade duration in minutes
    df['Duration (min)'] = (df['Exit Date'] - df['Entry Date']).dt.total_seconds() / 60
    
    print("="*80)
    print("ADDITIONAL STATISTICS - FVG INVERSION BACKTEST")
    print("="*80)
    
    # Performance by Year
    print("\n" + "-"*80)
    print("PERFORMANCE BY YEAR")
    print("-"*80)
    yearly = df.groupby('Year').agg({
        'PnL': ['count', 'sum', 'mean'],
        'Type': lambda x: (x == 'LONG').sum()
    })
    yearly.columns = ['Trades', 'Total PnL', 'Avg PnL', 'Long Trades']
    yearly['Short Trades'] = df.groupby('Year')['Type'].apply(lambda x: (x == 'SHORT').sum())
    yearly['Win Rate %'] = df.groupby('Year').apply(
        lambda x: (x['PnL'] > 0).sum() / len(x) * 100
    )
    print(yearly.to_string())
    
    # Performance by Trade Type
    print("\n" + "-"*80)
    print("PERFORMANCE BY TRADE TYPE")
    print("-"*80)
    type_stats = df.groupby('Type').agg({
        'PnL': ['count', 'sum', 'mean', 'median', 'std'],
        'Duration (min)': ['mean', 'median']
    })
    type_stats.columns = ['Trades', 'Total PnL', 'Avg PnL', 'Median PnL', 'Std Dev', 'Avg Duration', 'Median Duration']
    
    # Calculate win rate by type
    long_wins = df[(df['Type'] == 'LONG') & (df['PnL'] > 0)]
    short_wins = df[(df['Type'] == 'SHORT') & (df['PnL'] > 0)]
    long_total = len(df[df['Type'] == 'LONG'])
    short_total = len(df[df['Type'] == 'SHORT'])
    
    type_stats['Win Rate %'] = [
        len(long_wins) / long_total * 100 if long_total > 0 else 0,
        len(short_wins) / short_total * 100 if short_total > 0 else 0
    ]
    print(type_stats.to_string())
    
    # Exit Reason Analysis
    print("\n" + "-"*80)
    print("EXIT REASON ANALYSIS")
    print("-"*80)
    exit_stats = df.groupby('Exit Reason').agg({
        'PnL': ['count', 'sum', 'mean']
    })
    exit_stats.columns = ['Count', 'Total PnL', 'Avg PnL']
    exit_stats['Percentage'] = exit_stats['Count'] / len(df) * 100
    print(exit_stats.to_string())
    
    # Trade Duration Analysis
    print("\n" + "-"*80)
    print("TRADE DURATION ANALYSIS")
    print("-"*80)
    print(f"Average Duration:     {df['Duration (min)'].mean():.2f} minutes ({df['Duration (min)'].mean()/60:.2f} hours)")
    print(f"Median Duration:      {df['Duration (min)'].median():.2f} minutes ({df['Duration (min)'].median()/60:.2f} hours)")
    print(f"Min Duration:         {df['Duration (min)'].min():.2f} minutes")
    print(f"Max Duration:         {df['Duration (min)'].max():.2f} minutes ({df['Duration (min)'].max()/60:.2f} hours)")
    
    # Best and Worst Trades
    print("\n" + "-"*80)
    print("TOP 5 BEST TRADES")
    print("-"*80)
    best_trades = df.nlargest(5, 'PnL')[['Entry Date', 'Exit Date', 'Type', 'Entry Price', 'Exit Price', 'PnL']]
    print(best_trades.to_string(index=False))
    
    print("\n" + "-"*80)
    print("TOP 5 WORST TRADES")
    print("-"*80)
    worst_trades = df.nsmallest(5, 'PnL')[['Entry Date', 'Exit Date', 'Type', 'Entry Price', 'Exit Price', 'PnL']]
    print(worst_trades.to_string(index=False))
    
    # Consecutive Wins/Losses Analysis
    print("\n" + "-"*80)
    print("CONSECUTIVE WINS/LOSSES ANALYSIS")
    print("-"*80)
    
    df['Win'] = df['PnL'] > 0
    df['Streak'] = (df['Win'] != df['Win'].shift()).cumsum()
    streak_stats = df.groupby(['Streak', 'Win']).size()
    
    max_win_streak = streak_stats[True].max() if True in streak_stats else 0
    max_loss_streak = streak_stats[False].max() if False in streak_stats else 0
    
    print(f"Max Consecutive Wins:   {max_win_streak}")
    print(f"Max Consecutive Losses: {max_loss_streak}")
    
    # Monthly Performance (for most recent year)
    print("\n" + "-"*80)
    print("MONTHLY PERFORMANCE - 2025")
    print("-"*80)
    df_2025 = df[df['Year'] == 2025].copy()
    if len(df_2025) > 0:
        df_2025['Month'] = df_2025['Entry Date'].dt.month
        monthly = df_2025.groupby('Month').agg({
            'PnL': ['count', 'sum', 'mean']
        })
        monthly.columns = ['Trades', 'Total PnL', 'Avg PnL']
        monthly['Win Rate %'] = df_2025.groupby('Month').apply(
            lambda x: (x['PnL'] > 0).sum() / len(x) * 100
        )
        monthly.index.name = 'Month'
        print(monthly.to_string())
    
    # Risk-Reward Analysis
    print("\n" + "-"*80)
    print("RISK-REWARD ANALYSIS")
    print("-"*80)
    df['Risk'] = abs(df['Entry Price'] - df['Stop Loss']) * 20  # NQ multiplier
    df['Reward'] = abs(df['Take Profit'] - df['Entry Price']) * 20
    df['RR Ratio'] = df['Reward'] / df['Risk']
    
    print(f"Average Risk per Trade:   ${df['Risk'].mean():.2f}")
    print(f"Average Reward per Trade: ${df['Reward'].mean():.2f}")
    print(f"Average RR Ratio:         {df['RR Ratio'].mean():.2f}:1")
    
    print("\n" + "="*80)


if __name__ == "__main__":
    analyze_trades()

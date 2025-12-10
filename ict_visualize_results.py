#!/usr/bin/env python3
"""
ICT London Silver Bullet - Results Visualization & Analysis
===========================================================

Generate visual charts and detailed analysis from backtest results.
"""

import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

def load_results():
    """Load the backtest results"""
    print("Loading backtest results...")
    df = pd.read_csv('ict_london_silver_bullet_results.csv')
    df['Entry_Time'] = pd.to_datetime(df['Entry_Time'])
    df['Exit_Time'] = pd.to_datetime(df['Exit_Time'])
    df['Date'] = pd.to_datetime(df['Date'])
    print(f"  Loaded {len(df)} trades")
    return df

def analyze_consecutive_wins_losses(df):
    """Analyze consecutive wins and losses (drawdown streaks)"""
    print("\n" + "="*80)
    print("CONSECUTIVE WINS/LOSSES ANALYSIS")
    print("="*80)
    
    outcomes = df.sort_values('Entry_Time')['Outcome'].values
    
    current_streak = 1
    max_win_streak = 0
    max_loss_streak = 0
    current_type = outcomes[0]
    
    win_streaks = []
    loss_streaks = []
    
    for outcome in outcomes[1:]:
        if outcome == current_type:
            current_streak += 1
        else:
            if current_type == 'Win':
                win_streaks.append(current_streak)
                max_win_streak = max(max_win_streak, current_streak)
            else:
                loss_streaks.append(current_streak)
                max_loss_streak = max(max_loss_streak, current_streak)
            current_streak = 1
            current_type = outcome
    
    # Handle last streak
    if current_type == 'Win':
        win_streaks.append(current_streak)
        max_win_streak = max(max_win_streak, current_streak)
    else:
        loss_streaks.append(current_streak)
        max_loss_streak = max(max_loss_streak, current_streak)
    
    print(f"\n📊 Streak Statistics:")
    print(f"  Max Consecutive Wins:   {max_win_streak}")
    print(f"  Max Consecutive Losses: {max_loss_streak}")
    print(f"  Avg Win Streak:         {np.mean(win_streaks):.2f}")
    print(f"  Avg Loss Streak:        {np.mean(loss_streaks):.2f}")
    
    # Distribution of loss streaks
    print(f"\n📉 Loss Streak Distribution:")
    for i in range(1, min(16, max_loss_streak + 1)):
        count = sum(1 for s in loss_streaks if s == i)
        if count > 0:
            print(f"  {i} consecutive losses: {count} times")

def analyze_monthly_performance(df):
    """Analyze performance by month"""
    print("\n" + "="*80)
    print("MONTHLY PERFORMANCE ANALYSIS")
    print("="*80)
    
    df['YearMonth'] = df['Entry_Time'].dt.to_period('M')
    monthly = df.groupby('YearMonth').agg({
        'PnL': ['count', 'sum', lambda x: (x > 0).sum() / len(x) * 100 if len(x) > 0 else 0]
    })
    monthly.columns = ['Trades', 'Net_Profit', 'Win_Rate']
    
    # Calculate cumulative P&L
    monthly['Cumulative_PnL'] = monthly['Net_Profit'].cumsum()
    
    print(f"\n📅 Top 10 Best Months:")
    top_months = monthly.nlargest(10, 'Net_Profit')
    for period, row in top_months.iterrows():
        print(f"  {period}: {row['Net_Profit']:+.2f} pts ({int(row['Trades'])} trades, {row['Win_Rate']:.1f}% WR)")
    
    print(f"\n📅 Top 10 Worst Months:")
    worst_months = monthly.nsmallest(10, 'Net_Profit')
    for period, row in worst_months.iterrows():
        print(f"  {period}: {row['Net_Profit']:+.2f} pts ({int(row['Trades'])} trades, {row['Win_Rate']:.1f}% WR)")

def analyze_trade_duration(df):
    """Analyze how long trades are held"""
    print("\n" + "="*80)
    print("TRADE DURATION ANALYSIS")
    print("="*80)
    
    wins = df[df['Outcome'] == 'Win']
    losses = df[df['Outcome'] == 'Loss']
    
    print(f"\n⏱️ Bars Held (5-minute bars):")
    print(f"  All Trades:")
    print(f"    Avg: {df['Bars_Held'].mean():.1f} bars ({df['Bars_Held'].mean() * 5:.0f} minutes)")
    print(f"    Min: {df['Bars_Held'].min()} bars ({df['Bars_Held'].min() * 5} minutes)")
    print(f"    Max: {df['Bars_Held'].max()} bars ({df['Bars_Held'].max() * 5} minutes)")
    
    if len(wins) > 0:
        print(f"\n  Winning Trades:")
        print(f"    Avg: {wins['Bars_Held'].mean():.1f} bars ({wins['Bars_Held'].mean() * 5:.0f} minutes)")
        print(f"    Min: {wins['Bars_Held'].min()} bars ({wins['Bars_Held'].min() * 5} minutes)")
        print(f"    Max: {wins['Bars_Held'].max()} bars ({wins['Bars_Held'].max() * 5} minutes)")
    
    if len(losses) > 0:
        print(f"\n  Losing Trades:")
        print(f"    Avg: {losses['Bars_Held'].mean():.1f} bars ({losses['Bars_Held'].mean() * 5:.0f} minutes)")
        print(f"    Min: {losses['Bars_Held'].min()} bars ({losses['Bars_Held'].min() * 5} minutes)")
        print(f"    Max: {losses['Bars_Held'].max()} bars ({losses['Bars_Held'].max() * 5} minutes)")

def analyze_risk_reward_distribution(df):
    """Analyze the distribution of realized vs expected risk/reward"""
    print("\n" + "="*80)
    print("RISK/REWARD ANALYSIS")
    print("="*80)
    
    # Actual RR achieved
    df['Actual_RR'] = df['PnL'] / df['Risk']
    
    wins = df[df['Outcome'] == 'Win']
    losses = df[df['Outcome'] == 'Loss']
    
    print(f"\n📊 Expected vs Actual R:")
    print(f"  Expected RR Ratio: {df['RR_Ratio'].mean():.2f}:1")
    print(f"  Actual RR (Winners): {wins['Actual_RR'].mean():.2f}R")
    print(f"  Actual RR (Losers): {losses['Actual_RR'].mean():.2f}R")
    print(f"  Overall Actual RR: {df['Actual_RR'].mean():.2f}R")
    
    # Check if winners hit full TP
    winners_at_tp = len(wins[abs(wins['Exit_Price'] - wins['TP_Price']) < 1.0])
    print(f"\n🎯 Target Achievement:")
    print(f"  Winners hitting TP exactly: {winners_at_tp}/{len(wins)} ({winners_at_tp/len(wins)*100:.1f}%)")
    
    # Check if losers hit full SL
    losers_at_sl = len(losses[abs(losses['Exit_Price'] - losses['SL_Price']) < 1.0])
    print(f"  Losers hitting SL exactly: {losers_at_sl}/{len(losses)} ({losers_at_sl/len(losses)*100:.1f}%)")

def analyze_fvg_impact(df):
    """Analyze the impact of having FVG in the displacement"""
    print("\n" + "="*80)
    print("FVG IMPACT ANALYSIS")
    print("="*80)
    
    with_fvg = df[df['Has_FVG'] == True]
    without_fvg = df[df['Has_FVG'] == False]
    
    print(f"\n🔥 Setups WITH Bullish FVG:")
    print(f"  Count: {len(with_fvg)}")
    print(f"  Win Rate: {(with_fvg['Outcome'] == 'Win').sum() / len(with_fvg) * 100:.2f}%")
    print(f"  Net Profit: {with_fvg['PnL'].sum():.2f} points")
    
    # Calculate profit factor for FVG setups
    gross_profit_fvg = with_fvg[with_fvg['PnL'] > 0]['PnL'].sum()
    gross_loss_fvg = abs(with_fvg[with_fvg['PnL'] < 0]['PnL'].sum())
    pf_fvg = gross_profit_fvg / gross_loss_fvg if gross_loss_fvg != 0 else 0
    print(f"  Profit Factor: {pf_fvg:.2f}")
    
    print(f"\n❄️ Setups WITHOUT Bullish FVG:")
    print(f"  Count: {len(without_fvg)}")
    print(f"  Win Rate: {(without_fvg['Outcome'] == 'Win').sum() / len(without_fvg) * 100:.2f}%")
    print(f"  Net Profit: {without_fvg['PnL'].sum():.2f} points")
    
    # Calculate profit factor for non-FVG setups
    gross_profit_no_fvg = without_fvg[without_fvg['PnL'] > 0]['PnL'].sum()
    gross_loss_no_fvg = abs(without_fvg[without_fvg['PnL'] < 0]['PnL'].sum())
    pf_no_fvg = gross_profit_no_fvg / gross_loss_no_fvg if gross_loss_no_fvg != 0 else 0
    print(f"  Profit Factor: {pf_no_fvg:.2f}")

def analyze_day_of_week(df):
    """Analyze performance by day of week"""
    print("\n" + "="*80)
    print("DAY OF WEEK ANALYSIS")
    print("="*80)
    
    df['DayOfWeek'] = df['Entry_Time'].dt.day_name()
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    daily = df.groupby('DayOfWeek').agg({
        'PnL': ['count', 'sum', lambda x: (x > 0).sum() / len(x) * 100 if len(x) > 0 else 0]
    })
    daily.columns = ['Trades', 'Net_Profit', 'Win_Rate']
    
    # Reorder by day of week
    daily = daily.reindex([day for day in day_order if day in daily.index])
    
    print(f"\n📅 Performance by Day:")
    for day, row in daily.iterrows():
        print(f"  {day:10s}: {int(row['Trades']):3d} trades | {row['Net_Profit']:+8.2f} pts | {row['Win_Rate']:5.1f}% WR")

def analyze_range_size_impact(df):
    """Analyze if Tokyo range size impacts performance"""
    print("\n" + "="*80)
    print("TOKYO RANGE SIZE IMPACT")
    print("="*80)
    
    df['Tokyo_Range'] = df['Tokyo_High'] - df['Tokyo_Low']
    
    # Quartile analysis
    quartiles = df['Tokyo_Range'].quantile([0, 0.25, 0.5, 0.75, 1.0])
    
    print(f"\n📏 Tokyo Range Statistics:")
    print(f"  Min:  {quartiles[0.0]:.2f} points")
    print(f"  Q1:   {quartiles[0.25]:.2f} points")
    print(f"  Med:  {quartiles[0.5]:.2f} points")
    print(f"  Q3:   {quartiles[0.75]:.2f} points")
    print(f"  Max:  {quartiles[1.0]:.2f} points")
    
    print(f"\n📊 Performance by Range Size:")
    
    # Small ranges
    small = df[df['Tokyo_Range'] <= quartiles[0.25]]
    print(f"  Small Ranges (≤ {quartiles[0.25]:.0f} pts):")
    print(f"    Trades: {len(small)}")
    print(f"    Win Rate: {(small['Outcome'] == 'Win').sum() / len(small) * 100:.2f}%")
    print(f"    Net Profit: {small['PnL'].sum():.2f} pts")
    
    # Medium ranges
    medium = df[(df['Tokyo_Range'] > quartiles[0.25]) & (df['Tokyo_Range'] <= quartiles[0.75])]
    print(f"  Medium Ranges ({quartiles[0.25]:.0f}-{quartiles[0.75]:.0f} pts):")
    print(f"    Trades: {len(medium)}")
    print(f"    Win Rate: {(medium['Outcome'] == 'Win').sum() / len(medium) * 100:.2f}%")
    print(f"    Net Profit: {medium['PnL'].sum():.2f} pts")
    
    # Large ranges
    large = df[df['Tokyo_Range'] > quartiles[0.75]]
    print(f"  Large Ranges (> {quartiles[0.75]:.0f} pts):")
    print(f"    Trades: {len(large)}")
    print(f"    Win Rate: {(large['Outcome'] == 'Win').sum() / len(large) * 100:.2f}%")
    print(f"    Net Profit: {large['PnL'].sum():.2f} pts")

def create_equity_curve(df):
    """Create and display equity curve data"""
    print("\n" + "="*80)
    print("EQUITY CURVE DATA")
    print("="*80)
    
    df_sorted = df.sort_values('Entry_Time').copy()
    df_sorted['Cumulative_PnL'] = df_sorted['PnL'].cumsum()
    df_sorted['Running_Max'] = df_sorted['Cumulative_PnL'].cummax()
    df_sorted['Drawdown'] = df_sorted['Cumulative_PnL'] - df_sorted['Running_Max']
    
    print(f"\n📈 Equity Curve Summary:")
    print(f"  Starting: 0 points")
    print(f"  Ending: {df_sorted['Cumulative_PnL'].iloc[-1]:.2f} points")
    print(f"  Peak: {df_sorted['Running_Max'].max():.2f} points")
    print(f"  Max Drawdown: {df_sorted['Drawdown'].min():.2f} points")
    print(f"  Max Drawdown %: {(df_sorted['Drawdown'].min() / df_sorted['Running_Max'].max() * 100):.2f}%")
    
    # Find worst drawdown period
    worst_dd_idx = df_sorted['Drawdown'].idxmin()
    worst_dd_date = df_sorted.loc[worst_dd_idx, 'Entry_Time']
    print(f"  Worst Drawdown Date: {worst_dd_date.strftime('%Y-%m-%d')}")
    
    # Sample of equity curve (first 10, last 10)
    print(f"\n📊 Sample Equity Curve (First 10 trades):")
    for i, row in df_sorted.head(10).iterrows():
        print(f"  {row['Entry_Time'].strftime('%Y-%m-%d %H:%M')} | PnL: {row['PnL']:+7.2f} | Cum: {row['Cumulative_PnL']:+8.2f} | DD: {row['Drawdown']:+7.2f}")
    
    print(f"\n📊 Sample Equity Curve (Last 10 trades):")
    for i, row in df_sorted.tail(10).iterrows():
        print(f"  {row['Entry_Time'].strftime('%Y-%m-%d %H:%M')} | PnL: {row['PnL']:+7.2f} | Cum: {row['Cumulative_PnL']:+8.2f} | DD: {row['Drawdown']:+7.2f}")

def main():
    print("="*80)
    print("ICT LONDON SILVER BULLET - DETAILED ANALYSIS")
    print("="*80)
    
    # Load results
    df = load_results()
    
    # Run all analyses
    analyze_consecutive_wins_losses(df)
    analyze_monthly_performance(df)
    analyze_trade_duration(df)
    analyze_risk_reward_distribution(df)
    analyze_fvg_impact(df)
    analyze_day_of_week(df)
    analyze_range_size_impact(df)
    create_equity_curve(df)
    
    print("\n" + "="*80)
    print("ANALYSIS COMPLETE")
    print("="*80)

if __name__ == "__main__":
    main()

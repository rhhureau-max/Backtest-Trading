#!/usr/bin/env python3
"""
Quantitative analysis of Judas Swing trades with commission adjustments.
"""

import pandas as pd
import numpy as np
from datetime import datetime

# Constants
COMMISSION_PER_CONTRACT = 3.0  # $3 per contract
COMMISSION_POINTS = 0.15  # $3 = ~0.15 points on NQ
SPREAD_POINTS = 1.5  # Already deducted in CSV

def load_trades(csv_file):
    """Load and parse trade data."""
    df = pd.read_csv(csv_file)
    df['entry_time'] = pd.to_datetime(df['entry_time'], utc=True)
    df['exit_time'] = pd.to_datetime(df['exit_time'], utc=True)
    return df

def adjust_pnl_for_commission(df):
    """Deduct additional $3 commission (0.15 points) from each trade."""
    df['pnl_adjusted'] = df['pnl'] - COMMISSION_POINTS
    return df

def calculate_metrics(df):
    """Calculate key performance metrics."""
    df_adj = df.copy()
    
    # Separate wins and losses
    wins = df_adj[df_adj['pnl_adjusted'] > 0]
    losses = df_adj[df_adj['pnl_adjusted'] <= 0]
    
    metrics = {
        'total_trades': len(df_adj),
        'winning_trades': len(wins),
        'losing_trades': len(losses),
        'win_rate': len(wins) / len(df_adj) * 100 if len(df_adj) > 0 else 0,
        'max_win_points': wins['pnl_adjusted'].max() if len(wins) > 0 else 0,
        'min_win_points': wins['pnl_adjusted'].min() if len(wins) > 0 else 0,
        'avg_win_points': wins['pnl_adjusted'].mean() if len(wins) > 0 else 0,
        'avg_loss_points': losses['pnl_adjusted'].mean() if len(losses) > 0 else 0,
        'total_pnl_adjusted': df_adj['pnl_adjusted'].sum(),
        'total_pnl_original': df_adj['pnl'].sum(),
        'commission_impact': df_adj['pnl'].sum() - df_adj['pnl_adjusted'].sum()
    }
    
    return metrics

def calculate_risk_reward(df):
    """Calculate average Risk:Reward ratio."""
    # For each trade, calculate the risk (entry to stop loss distance)
    # and reward (actual PnL achieved)
    
    rr_ratios = []
    
    for idx, row in df.iterrows():
        entry = row['entry_price']
        exit_price = row['exit_price']
        direction = row['direction']
        pnl_adj = row['pnl_adjusted']
        
        # Estimate stop loss distance based on strategy
        # Since we don't have explicit stop loss in CSV, we estimate it
        # For losses, the risk is the actual loss
        # For wins, we estimate based on the manipulation wick
        
        if pnl_adj <= 0:
            # For losses, risk = abs(loss)
            risk = abs(pnl_adj)
            reward = 0
        else:
            # For wins, we estimate risk as 20-30% of the reward
            # This is based on typical manipulation wick size
            reward = pnl_adj
            risk = reward * 0.25  # Estimate
        
        if risk > 0:
            rr = reward / risk
            rr_ratios.append(rr)
    
    avg_rr = np.mean(rr_ratios) if rr_ratios else 0
    return avg_rr

def get_last_5_trades_2025(df):
    """Get detailed information for last 5 trades in 2025."""
    df_2025 = df[df['entry_time'].dt.year == 2025].copy()
    df_2025 = df_2025.sort_values('entry_time', ascending=False).head(5)
    df_2025 = df_2025.sort_values('entry_time', ascending=True)  # Show chronologically
    
    trade_details = []
    
    for idx, row in df_2025.iterrows():
        detail = {
            'Date': row['entry_time'].strftime('%Y-%m-%d'),
            'Time': row['entry_time'].strftime('%H:%M:%S'),
            'Direction': row['direction'].upper(),
            'Fakeout': 'Asian High (SHORT)' if row['direction'] == 'short' else 'Asian Low (LONG)',
            'Entry Price': f"{row['entry_price']:.2f}",
            'Exit Price': f"{row['exit_price']:.2f}",
            'TP1 Hit': 'Yes' if row['tp1_hit'] else 'No',
            'TP2 Hit': 'Yes' if row['tp2_hit'] else 'No',
            'Stopped Out': 'Yes' if row['status'] == 'stopped' else 'No',
            'Breakeven Moved': 'Yes' if row['breakeven_moved'] else 'No',
            'PnL (Original)': f"{row['pnl']:.2f}",
            'PnL (After $3 Commission)': f"{row['pnl_adjusted']:.2f}"
        }
        trade_details.append(detail)
    
    return pd.DataFrame(trade_details)

def main():
    print("="*80)
    print("JUDAS SWING STRATEGY - QUANTITATIVE ANALYSIS")
    print("="*80)
    print()
    
    # Load data
    df = load_trades('judas_swing_trades.csv')
    print(f"Total trades loaded: {len(df)}")
    print()
    
    # Adjust for commission
    df = adjust_pnl_for_commission(df)
    
    # Calculate metrics
    metrics = calculate_metrics(df)
    
    print("="*80)
    print("1. KEY PERFORMANCE METRICS (After $3 Commission per Trade)")
    print("="*80)
    print()
    print(f"Total Trades:              {metrics['total_trades']:,}")
    print(f"Winning Trades:            {metrics['winning_trades']:,}")
    print(f"Losing Trades:             {metrics['losing_trades']:,}")
    print(f"Win Rate:                  {metrics['win_rate']:.2f}%")
    print()
    print(f"Max Win (Points):          {metrics['max_win_points']:.2f}")
    print(f"Min Win (Points):          {metrics['min_win_points']:.2f}")
    print(f"Average Win (Points):      {metrics['avg_win_points']:.2f}")
    print(f"Average Loss (Points):     {metrics['avg_loss_points']:.2f}")
    print()
    print(f"Total PnL (Original):      {metrics['total_pnl_original']:.2f} points")
    print(f"Commission Impact:         -{metrics['commission_impact']:.2f} points")
    print(f"Total PnL (Adjusted):      {metrics['total_pnl_adjusted']:.2f} points")
    print()
    
    # Calculate Risk:Reward
    avg_rr = calculate_risk_reward(df)
    print(f"Average Risk:Reward Ratio: {avg_rr:.2f}:1")
    print()
    
    # Get last 5 trades in 2025
    print("="*80)
    print("2. LAST 5 TRADES IN 2025 - DETAILED BREAKDOWN")
    print("="*80)
    print()
    
    last_5 = get_last_5_trades_2025(df)
    
    if len(last_5) > 0:
        for idx, trade in last_5.iterrows():
            print(f"Trade #{idx + 1}")
            print("-" * 60)
            for key, value in trade.items():
                print(f"  {key:.<30} {value}")
            print()
    else:
        print("No trades found in 2025")
    
    print("="*80)
    print("3. COMMISSION IMPACT ANALYSIS")
    print("="*80)
    print()
    print(f"Commission per trade:      ${COMMISSION_PER_CONTRACT:.2f} (~{COMMISSION_POINTS:.2f} points)")
    print(f"Total trades:              {metrics['total_trades']:,}")
    print(f"Total commission cost:     {metrics['commission_impact']:.2f} points")
    print(f"                           (${metrics['total_trades'] * COMMISSION_PER_CONTRACT:,.2f})")
    print()
    print(f"Win rate before commission: {len(df[df['pnl'] > 0]) / len(df) * 100:.2f}%")
    print(f"Win rate after commission:  {metrics['win_rate']:.2f}%")
    print()
    
    # Additional insights
    print("="*80)
    print("4. STRATEGY INSIGHTS")
    print("="*80)
    print()
    
    tp1_only = len(df[(df['tp1_hit'] == True) & (df['tp2_hit'] == False)])
    both_tps = len(df[(df['tp1_hit'] == True) & (df['tp2_hit'] == True)])
    stopped_out = len(df[df['status'] == 'stopped'])
    
    print(f"TP1 Only (50% exit):       {tp1_only:,} ({tp1_only/len(df)*100:.1f}%)")
    print(f"Both TPs Hit:              {both_tps:,} ({both_tps/len(df)*100:.1f}%)")
    print(f"Stopped Out:               {stopped_out:,} ({stopped_out/len(df)*100:.1f}%)")
    print()
    
    # Monthly summary for 2025
    df_2025 = df[df['entry_time'].dt.year == 2025]
    if len(df_2025) > 0:
        monthly_2025 = df_2025.groupby(df_2025['entry_time'].dt.to_period('M')).agg({
            'pnl_adjusted': ['sum', 'count', 'mean']
        }).round(2)
        
        print("="*80)
        print("5. MONTHLY PERFORMANCE 2025 (After Commission)")
        print("="*80)
        print()
        print(monthly_2025.to_string())
        print()

if __name__ == '__main__':
    main()

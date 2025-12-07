#!/usr/bin/env python3
"""
Sample Trade Viewer for ICT 2022 Model
Shows details of sample winning and losing trades
"""

import pandas as pd
from ict_2022_london_continuation import ICT2022Model

def main():
    print("="*80)
    print("ICT 2022 Model - Sample Trade Analysis")
    print("="*80)
    
    # Run backtest
    backtest = ICT2022Model()
    backtest.load_data()
    backtest.calculate_ema()
    
    print("\nRunning backtest to collect trade samples...")
    setups, entries, trades = backtest.run_backtest_mss_method(use_method1=True)
    
    # Show sample winning trades
    print("\n" + "="*80)
    print("SAMPLE WINNING TRADES (First 5)")
    print("="*80)
    
    winning_trades = [t for t in trades if t['points'] > 0][:5]
    
    for i, trade in enumerate(winning_trades, 1):
        print(f"\n--- Trade #{i} ---")
        print(f"Date: {trade['date']}")
        print(f"Entry Time: {trade['entry_time']}")
        print(f"Entry Price: {trade['entry_price']:.2f}")
        print(f"Stop Loss: {trade['stop_loss']:.2f}")
        print(f"Exit Type: {trade['exit_type']}")
        print(f"Exit Price: {trade['exit_price']:.2f}")
        print(f"Exit Time: {trade['exit_time']}")
        print(f"Points Gained: +{trade['points']:.2f}")
        print(f"Risk/Reward: {trade['rr_ratio']:.2f}:1")
        print(f"Duration: {trade['duration_minutes']:.1f} minutes")
        print(f"Tokyo Range: {trade['tokyo_low']:.2f} - {trade['tokyo_high']:.2f} (EQ: {trade['tokyo_eq']:.2f})")
        print(f"Midnight Open: {trade['midnight_open']:.2f}")
        print(f"Sweep Low: {trade['sweep_low']:.2f}")
    
    # Show sample losing trades
    print("\n" + "="*80)
    print("SAMPLE LOSING TRADES (First 5)")
    print("="*80)
    
    losing_trades = [t for t in trades if t['points'] < 0][:5]
    
    for i, trade in enumerate(losing_trades, 1):
        print(f"\n--- Trade #{i} ---")
        print(f"Date: {trade['date']}")
        print(f"Entry Time: {trade['entry_time']}")
        print(f"Entry Price: {trade['entry_price']:.2f}")
        print(f"Stop Loss: {trade['stop_loss']:.2f}")
        print(f"Exit Type: {trade['exit_type']}")
        print(f"Exit Price: {trade['exit_price']:.2f}")
        print(f"Exit Time: {trade['exit_time']}")
        print(f"Points Lost: {trade['points']:.2f}")
        print(f"Duration: {trade['duration_minutes']:.1f} minutes")
        print(f"Tokyo Range: {trade['tokyo_low']:.2f} - {trade['tokyo_high']:.2f} (EQ: {trade['tokyo_eq']:.2f})")
        print(f"Midnight Open: {trade['midnight_open']:.2f}")
        print(f"Sweep Low: {trade['sweep_low']:.2f}")
    
    # Show sample trades that hit Tokyo_High (TP2)
    print("\n" + "="*80)
    print("SAMPLE TRADES HITTING TOKYO_HIGH (TP2) - The Key Target")
    print("="*80)
    
    tp2_trades = [t for t in trades if t['exit_type'] in ['TP2', 'TP3']][:5]
    
    if len(tp2_trades) > 0:
        for i, trade in enumerate(tp2_trades, 1):
            print(f"\n--- Trade #{i} ---")
            print(f"Date: {trade['date']}")
            print(f"Entry Time: {trade['entry_time']}")
            print(f"Entry Price: {trade['entry_price']:.2f}")
            print(f"Tokyo High Target: {trade['tokyo_high']:.2f}")
            print(f"Distance to Target: {trade['tokyo_high'] - trade['entry_price']:.2f} points")
            print(f"Exit Type: {trade['exit_type']}")
            print(f"Exit Price: {trade['exit_price']:.2f}")
            print(f"Points Gained: +{trade['points']:.2f}")
            print(f"Risk/Reward: {trade['rr_ratio']:.2f}:1")
            print(f"Duration: {trade['duration_minutes']:.1f} minutes")
            print(f"Sweep Low: {trade['sweep_low']:.2f}")
            print(f"Risk (Entry - SL): {trade['entry_price'] - trade['stop_loss']:.2f} points")
    else:
        print("\nNo trades hit Tokyo_High in this sample!")
    
    print("\n" + "="*80)
    print("Monthly Breakdown")
    print("="*80)
    
    # Group trades by month
    trade_df = pd.DataFrame(trades)
    trade_df['month'] = pd.to_datetime(trade_df['date']).dt.to_period('M')
    
    monthly_stats = trade_df.groupby('month').agg({
        'points': ['sum', 'mean', 'count'],
        'exit_type': lambda x: (x.isin(['TP2', 'TP3'])).sum()
    }).round(2)
    
    print("\nTop 10 Most Profitable Months:")
    monthly_stats.columns = ['Total Points', 'Avg Points', 'Trade Count', 'TP2+ Hits']
    top_months = monthly_stats.nlargest(10, 'Total Points')
    print(top_months)
    
    print("\n" + "="*80)


if __name__ == "__main__":
    main()

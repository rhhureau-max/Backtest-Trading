#!/usr/bin/env python3
"""
Quick viewer for best performing RR strategies.
Displays the top strategies sorted by various metrics.
"""

import pandas as pd
import sys


def view_best_strategies(summary_file='rr_analysis_summary.csv', top_n=10):
    """
    Display best performing strategies from summary file.
    
    Args:
        summary_file: Path to the summary CSV file
        top_n: Number of top strategies to display
    """
    try:
        df = pd.read_csv(summary_file)
    except FileNotFoundError:
        print(f"Error: {summary_file} not found!")
        print("Please run rr_analysis.py first to generate the summary.")
        return 1
    
    print("=" * 100)
    print("BEST PERFORMING RR STRATEGIES")
    print("=" * 100)
    
    # Filter only completed trades (exclude pending)
    df_completed = df[df['total_trades'] > 0].copy()
    
    # Top by Expectancy
    print(f"\n{'='*100}")
    print(f"TOP {top_n} STRATEGIES BY EXPECTANCY (Expected profit per trade)")
    print('='*100)
    top_expectancy = df_completed.nlargest(top_n, 'expectancy')[
        ['SL_Placement', 'RR_Ratio', 'win_rate', 'expectancy', 'profit_factor', 'total_pnl', 'total_trades']
    ]
    top_expectancy['win_rate'] = top_expectancy['win_rate'].apply(lambda x: f"{x:.2f}%")
    top_expectancy['expectancy'] = top_expectancy['expectancy'].apply(lambda x: f"${x:.2f}")
    top_expectancy['profit_factor'] = top_expectancy['profit_factor'].apply(lambda x: f"{x:.2f}")
    top_expectancy['total_pnl'] = top_expectancy['total_pnl'].apply(lambda x: f"${x:,.2f}")
    print(top_expectancy.to_string(index=False))
    
    # Top by Win Rate
    print(f"\n{'='*100}")
    print(f"TOP {top_n} STRATEGIES BY WIN RATE")
    print('='*100)
    top_winrate = df_completed.nlargest(top_n, 'win_rate')[
        ['SL_Placement', 'RR_Ratio', 'win_rate', 'expectancy', 'profit_factor', 'total_pnl', 'total_trades']
    ]
    top_winrate['win_rate'] = top_winrate['win_rate'].apply(lambda x: f"{x:.2f}%")
    top_winrate['expectancy'] = top_winrate['expectancy'].apply(lambda x: f"${x:.2f}")
    top_winrate['profit_factor'] = top_winrate['profit_factor'].apply(lambda x: f"{x:.2f}")
    top_winrate['total_pnl'] = top_winrate['total_pnl'].apply(lambda x: f"${x:,.2f}")
    print(top_winrate.to_string(index=False))
    
    # Top by Total PnL
    print(f"\n{'='*100}")
    print(f"TOP {top_n} STRATEGIES BY TOTAL P&L")
    print('='*100)
    top_pnl = df_completed.nlargest(top_n, 'total_pnl')[
        ['SL_Placement', 'RR_Ratio', 'win_rate', 'expectancy', 'profit_factor', 'total_pnl', 'total_trades']
    ]
    top_pnl['win_rate'] = top_pnl['win_rate'].apply(lambda x: f"{x:.2f}%")
    top_pnl['expectancy'] = top_pnl['expectancy'].apply(lambda x: f"${x:.2f}")
    top_pnl['profit_factor'] = top_pnl['profit_factor'].apply(lambda x: f"{x:.2f}")
    top_pnl['total_pnl'] = top_pnl['total_pnl'].apply(lambda x: f"${x:,.2f}")
    print(top_pnl.to_string(index=False))
    
    # Top by Profit Factor
    print(f"\n{'='*100}")
    print(f"TOP {top_n} STRATEGIES BY PROFIT FACTOR")
    print('='*100)
    top_pf = df_completed.nlargest(top_n, 'profit_factor')[
        ['SL_Placement', 'RR_Ratio', 'win_rate', 'expectancy', 'profit_factor', 'total_pnl', 'total_trades']
    ]
    top_pf['win_rate'] = top_pf['win_rate'].apply(lambda x: f"{x:.2f}%")
    top_pf['expectancy'] = top_pf['expectancy'].apply(lambda x: f"${x:.2f}")
    top_pf['profit_factor'] = top_pf['profit_factor'].apply(lambda x: f"{x:.2f}")
    top_pf['total_pnl'] = top_pf['total_pnl'].apply(lambda x: f"${x:,.2f}")
    print(top_pf.to_string(index=False))
    
    # Comparison by SL Placement
    print(f"\n{'='*100}")
    print("AVERAGE PERFORMANCE BY SL PLACEMENT")
    print('='*100)
    sl_avg = df_completed.groupby('SL_Placement').agg({
        'win_rate': 'mean',
        'expectancy': 'mean',
        'profit_factor': 'mean',
        'total_pnl': 'sum'
    }).round(2)
    sl_avg.columns = ['Avg Win Rate (%)', 'Avg Expectancy ($)', 'Avg Profit Factor', 'Total PnL ($)']
    print(sl_avg)
    
    # Comparison by RR Ratio
    print(f"\n{'='*100}")
    print("AVERAGE PERFORMANCE BY RR RATIO")
    print('='*100)
    rr_avg = df_completed.groupby('RR_Ratio').agg({
        'win_rate': 'mean',
        'expectancy': 'mean',
        'profit_factor': 'mean',
        'total_pnl': 'sum'
    }).round(2)
    rr_avg.columns = ['Avg Win Rate (%)', 'Avg Expectancy ($)', 'Avg Profit Factor', 'Total PnL ($)']
    print(rr_avg)
    
    print(f"\n{'='*100}")
    print("\nFor detailed analysis, see:")
    print("  - rr_analysis_summary.csv (all statistics)")
    print("  - rr_analysis_complete.csv (individual trade results)")
    print("  - RR_ANALYSIS_README.md (comprehensive documentation)")
    print('='*100)
    
    return 0


if __name__ == "__main__":
    exit(view_best_strategies())

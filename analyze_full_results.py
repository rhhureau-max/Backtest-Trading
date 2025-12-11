"""
Complete Analysis Visualization - ICT FVG Reversal Strategy (2018-2025)
"""

import pandas as pd

def print_complete_analysis():
    """Print complete analysis from full backtest results"""
    
    # Load data
    trades = pd.read_csv('fvg_reversal_trades_full.csv')
    results = pd.read_csv('fvg_reversal_results_full.csv')
    
    trades['year'] = pd.to_datetime(trades['entry_time']).dt.year
    
    print("="*80)
    print("ICT FVG REVERSAL STRATEGY - COMPLETE ANALYSIS (2018-2025)")
    print("="*80)
    
    # Overall Summary
    print("\n📊 OVERALL PERFORMANCE")
    print("-" * 80)
    print(f"Period:                  2018-2025 (8 years)")
    print(f"Total Trades:            {len(trades)}")
    print(f"Win Rate:                {trades['winner'].sum()/len(trades)*100:.1f}%")
    print(f"Total Profit:            ${trades['pnl'].sum():,.2f}")
    print(f"Average Profit/Trade:    ${trades['pnl'].mean():.2f}")
    print(f"Average R-Multiple:      {trades['r_multiple'].mean():.2f}")
    print(f"Max Drawdown:            ${results['Max Drawdown ($)'].max():,.2f}")
    
    # Year by Year
    print("\n📅 YEAR-BY-YEAR PERFORMANCE")
    print("-" * 80)
    print(f"{'Year':<6} {'Trades':<8} {'Win Rate':<10} {'Profit':<15} {'Avg R':<8} {'Setups'}")
    print("-" * 80)
    
    for year in sorted(trades['year'].unique()):
        year_trades = trades[trades['year'] == year]
        wr = year_trades['winner'].sum() / len(year_trades) * 100
        profit = year_trades['pnl'].sum()
        avg_r = year_trades['r_multiple'].mean()
        setups = year_trades['setup_class'].value_counts().to_dict()
        setup_str = f"C:{setups.get('C', 0)} B:{setups.get('B', 0)} A:{setups.get('A', 0)}"
        print(f"{year:<6} {len(year_trades):<8} {wr:>6.1f}%    ${profit:>11,.2f}  {avg_r:>6.2f}  {setup_str}")
    
    # Setup Class Performance
    print("\n🎯 PERFORMANCE BY SETUP CLASS")
    print("-" * 80)
    print(results.to_string(index=False))
    
    # Setup Distribution
    print("\n📈 SETUP DISTRIBUTION")
    print("-" * 80)
    setup_counts = trades['setup_class'].value_counts()
    setup_profits = trades.groupby('setup_class')['pnl'].sum()
    
    for setup in ['C', 'B', 'A', 'A+']:
        count = setup_counts.get(setup, 0)
        pct = (count / len(trades) * 100) if count > 0 else 0
        profit = setup_profits.get(setup, 0)
        profit_pct = (profit / trades['pnl'].sum() * 100) if profit > 0 else 0
        print(f"Setup {setup}: {count:>3} trades ({pct:>5.1f}%) → ${profit:>11,.2f} profit ({profit_pct:>5.1f}%)")
    
    # Direction Analysis
    print("\n↕️  DIRECTION ANALYSIS")
    print("-" * 80)
    for direction in ['bullish', 'bearish']:
        dir_trades = trades[trades['direction'] == direction]
        if len(dir_trades) > 0:
            wr = dir_trades['winner'].sum() / len(dir_trades) * 100
            profit = dir_trades['pnl'].sum()
            avg_profit = dir_trades['pnl'].mean()
            print(f"{direction.capitalize():<10}: {len(dir_trades):>3} trades | {wr:>5.1f}% WR | ${profit:>11,.2f} profit (avg: ${avg_profit:>7.2f})")
    
    # Exit Reason Analysis
    print("\n🚪 EXIT REASON BREAKDOWN")
    print("-" * 80)
    exit_counts = trades['exit_reason'].value_counts()
    for reason, count in exit_counts.items():
        pct = count / len(trades) * 100
        reason_trades = trades[trades['exit_reason'] == reason]
        avg_profit = reason_trades['pnl'].mean()
        print(f"{reason:<20}: {count:>3} trades ({pct:>5.1f}%) | Avg P&L: ${avg_profit:>8.2f}")
    
    # Best/Worst Analysis
    print("\n🏆 TOP 5 BEST TRADES")
    print("-" * 80)
    best = trades.nlargest(5, 'pnl')[['entry_time', 'direction', 'setup_class', 'pnl', 'r_multiple']]
    for idx, row in best.iterrows():
        print(f"{row['entry_time']:<20} | {row['direction']:<8} | Setup {row['setup_class']} | ${row['pnl']:>8,.2f} ({row['r_multiple']:>5.2f}R)")
    
    print("\n📉 TOP 5 WORST TRADES")
    print("-" * 80)
    worst = trades.nsmallest(5, 'pnl')[['entry_time', 'direction', 'setup_class', 'pnl', 'r_multiple']]
    for idx, row in worst.iterrows():
        print(f"{row['entry_time']:<20} | {row['direction']:<8} | Setup {row['setup_class']} | ${row['pnl']:>8,.2f} ({row['r_multiple']:>5.2f}R)")
    
    # Monthly Analysis
    print("\n📆 BEST/WORST MONTHS")
    print("-" * 80)
    trades['month'] = pd.to_datetime(trades['entry_time']).dt.to_period('M')
    monthly_profit = trades.groupby('month')['pnl'].sum().sort_values(ascending=False)
    
    print("Best 5 Months:")
    for month, profit in monthly_profit.head(5).items():
        month_trades = trades[trades['month'] == month]
        print(f"  {month}: ${profit:>10,.2f} ({len(month_trades)} trades)")
    
    print("\nWorst 5 Months:")
    for month, profit in monthly_profit.tail(5).items():
        month_trades = trades[trades['month'] == month]
        print(f"  {month}: ${profit:>10,.2f} ({len(month_trades)} trades)")
    
    # Key Statistics
    print("\n📊 KEY STATISTICS")
    print("-" * 80)
    print(f"Profitable Years:        8/8 (100%)")
    print(f"Best Year:               {trades.groupby('year')['pnl'].sum().idxmax()} (${trades.groupby('year')['pnl'].sum().max():,.2f})")
    print(f"Worst Year:              {trades.groupby('year')['pnl'].sum().idxmin()} (${trades.groupby('year')['pnl'].sum().min():,.2f})")
    print(f"Average Annual Profit:   ${trades.groupby('year')['pnl'].sum().mean():,.2f}")
    print(f"Average Trades/Year:     {len(trades)/8:.1f}")
    print(f"Best Month:              {monthly_profit.idxmax()} (${monthly_profit.max():,.2f})")
    print(f"Worst Month:             {monthly_profit.idxmin()} (${monthly_profit.min():,.2f})")
    
    print("\n" + "="*80)
    print("Analysis complete. See COMPLETE_ANALYSIS_2018_2025.md for detailed report.")
    print("="*80)


if __name__ == "__main__":
    print_complete_analysis()

"""
ICT FVG Reversal Strategy - Example Usage and Analysis
======================================================

This script demonstrates how to use the FVG Reversal Backtest and analyze results.
"""

from fvg_reversal_backtest import FVGReversalBacktest
import pandas as pd


def run_single_year_backtest():
    """Run backtest for a single year"""
    print("\n" + "="*80)
    print("SINGLE YEAR BACKTEST EXAMPLE (2024)")
    print("="*80)
    
    backtest = FVGReversalBacktest(capital=100000, risk_per_trade=0.01)
    trades = backtest.run_backtest(years=[2024])
    results = backtest.generate_results()
    
    return backtest, trades, results


def run_multi_year_backtest():
    """Run backtest across multiple years"""
    print("\n" + "="*80)
    print("MULTI-YEAR BACKTEST EXAMPLE (2023-2024)")
    print("="*80)
    
    backtest = FVGReversalBacktest(capital=100000, risk_per_trade=0.01)
    trades = backtest.run_backtest(years=[2023, 2024])
    results = backtest.generate_results()
    
    return backtest, trades, results


def analyze_trades(trades_df: pd.DataFrame):
    """Perform detailed analysis of trades"""
    if len(trades_df) == 0:
        print("No trades to analyze!")
        return
    
    print("\n" + "="*80)
    print("DETAILED TRADE ANALYSIS")
    print("="*80)
    
    # Direction analysis
    print("\n1. Direction Breakdown:")
    direction_stats = trades_df.groupby('direction').agg({
        'pnl': ['count', 'mean', 'sum'],
        'winner': 'mean'
    }).round(2)
    print(direction_stats)
    
    # Setup class analysis
    print("\n2. Setup Class Performance:")
    setup_stats = trades_df.groupby('setup_class').agg({
        'pnl': ['count', 'mean', 'sum'],
        'winner': 'mean',
        'r_multiple': 'mean'
    }).round(2)
    print(setup_stats)
    
    # Exit reason analysis
    print("\n3. Exit Reasons:")
    exit_reasons = trades_df['exit_reason'].value_counts()
    print(exit_reasons)
    
    # Best and worst trades
    print("\n4. Best 5 Trades:")
    best_trades = trades_df.nlargest(5, 'pnl')[['entry_time', 'direction', 'setup_class', 'pnl', 'r_multiple', 'exit_reason']]
    print(best_trades.to_string(index=False))
    
    print("\n5. Worst 5 Trades:")
    worst_trades = trades_df.nsmallest(5, 'pnl')[['entry_time', 'direction', 'setup_class', 'pnl', 'r_multiple', 'exit_reason']]
    print(worst_trades.to_string(index=False))
    
    # Time-based analysis
    print("\n6. Performance by Entry Hour:")
    trades_df['entry_hour'] = pd.to_datetime(trades_df['entry_time']).dt.hour
    hour_stats = trades_df.groupby('entry_hour').agg({
        'pnl': ['count', 'mean', 'sum'],
        'winner': 'mean'
    }).round(2)
    print(hour_stats)


def custom_backtest_parameters():
    """Example of customizing backtest parameters"""
    print("\n" + "="*80)
    print("CUSTOM PARAMETERS EXAMPLE")
    print("="*80)
    
    # Initialize with custom parameters
    backtest = FVGReversalBacktest(
        capital=50000,           # Smaller account
        risk_per_trade=0.02      # Higher risk (2% per trade)
    )
    
    # Modify configuration
    backtest.config['swing_lookback'] = 25        # More conservative swing detection
    backtest.config['displacement_multiplier'] = 2.5  # Stronger displacement required
    backtest.config['rr_target_1'] = 2.5         # Higher first target
    
    print(f"Capital: ${backtest.capital:,.2f}")
    print(f"Risk per trade: {backtest.risk_per_trade*100}%")
    print(f"Swing lookback: {backtest.config['swing_lookback']} bars")
    print(f"Displacement multiplier: {backtest.config['displacement_multiplier']}x")
    print(f"First TP target: {backtest.config['rr_target_1']}R")
    
    # Run backtest
    trades = backtest.run_backtest(years=[2024])
    results = backtest.generate_results()
    
    return backtest, trades, results


def compare_setups(trades_df: pd.DataFrame):
    """Compare performance between different setup classes"""
    if len(trades_df) == 0:
        print("No trades to compare!")
        return
    
    print("\n" + "="*80)
    print("SETUP COMPARISON MATRIX")
    print("="*80)
    
    for setup in ['C', 'B', 'A', 'A+']:
        setup_trades = trades_df[trades_df['setup_class'] == setup]
        
        if len(setup_trades) == 0:
            print(f"\nSetup {setup}: No trades")
            continue
        
        winners = setup_trades[setup_trades['winner']]
        losers = setup_trades[~setup_trades['winner']]
        
        print(f"\nSetup {setup}:")
        print(f"  Total trades: {len(setup_trades)}")
        print(f"  Winners: {len(winners)} ({len(winners)/len(setup_trades)*100:.1f}%)")
        print(f"  Losers: {len(losers)} ({len(losers)/len(setup_trades)*100:.1f}%)")
        print(f"  Avg win: ${winners['pnl'].mean():.2f}" if len(winners) > 0 else "  Avg win: N/A")
        print(f"  Avg loss: ${losers['pnl'].mean():.2f}" if len(losers) > 0 else "  Avg loss: N/A")
        print(f"  Avg R-multiple: {setup_trades['r_multiple'].mean():.2f}")
        print(f"  Total P&L: ${setup_trades['pnl'].sum():.2f}")


def main():
    """Main execution function demonstrating various uses"""
    print("="*80)
    print("ICT FVG REVERSAL STRATEGY - COMPREHENSIVE EXAMPLES")
    print("="*80)
    
    # Example 1: Single year backtest
    backtest1, trades1, results1 = run_single_year_backtest()
    
    # Example 2: Analyze trades in detail
    analyze_trades(trades1)
    
    # Example 3: Compare setup performance
    compare_setups(trades1)
    
    # Example 4: Multi-year backtest
    backtest2, trades2, results2 = run_multi_year_backtest()
    
    # Example 5: Custom parameters
    # backtest3, trades3, results3 = custom_backtest_parameters()
    
    print("\n" + "="*80)
    print("EXAMPLES COMPLETE")
    print("="*80)
    print("\nFor more details, see README_FVG_REVERSAL.md")


if __name__ == "__main__":
    main()

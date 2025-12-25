#!/usr/bin/env python3
"""
Example Usage of the Backtest Strategy Script

This script demonstrates how to use the backtesting engine
with different strategies and configurations.
"""

from backtest_strategy import BacktestStrategy


def example_1_basic_usage():
    """
    Example 1: Basic usage with ORB strategy
    """
    print("\n" + "="*70)
    print("EXAMPLE 1: Basic Usage - ORB Strategy")
    print("="*70)
    
    # Initialize backtest with ORB strategy
    backtest = BacktestStrategy(
        csv_file_path='/home/runner/work/Backtest-Trading/Backtest-Trading/2025 5m.csv',
        strategy='ORB'
    )
    
    # Run the backtest
    df_results, metrics = backtest.run()
    
    return df_results, metrics


def example_2_compare_strategies():
    """
    Example 2: Compare all three strategies
    """
    print("\n" + "="*70)
    print("EXAMPLE 2: Comparing All Strategies")
    print("="*70)
    
    csv_file = '/home/runner/work/Backtest-Trading/Backtest-Trading/2025 5m.csv'
    strategies = ['ORB', 'RSI', 'EMA']
    
    results = {}
    
    for strat in strategies:
        print(f"\n--- Testing {strat} Strategy ---")
        backtest = BacktestStrategy(csv_file_path=csv_file, strategy=strat)
        df, metrics = backtest.run()
        results[strat] = metrics
    
    # Print comparison table
    print("\n" + "="*70)
    print("STRATEGY COMPARISON")
    print("="*70)
    print(f"{'Strategy':<15} {'Return':<15} {'Max DD':<15} {'Sharpe':<15}")
    print("-"*70)
    
    for strat, metrics in results.items():
        print(f"{strat:<15} {metrics['Total_Return']*100:>6.2f}%      "
              f"{metrics['Max_Drawdown']*100:>6.2f}%      "
              f"{metrics['Sharpe_Ratio']:>6.2f}")
    
    return results


def example_3_different_timeframe():
    """
    Example 3: Using different timeframe (15m instead of 5m)
    """
    print("\n" + "="*70)
    print("EXAMPLE 3: Different Timeframe - 15 Minute Data")
    print("="*70)
    
    backtest = BacktestStrategy(
        csv_file_path='/home/runner/work/Backtest-Trading/Backtest-Trading/2025 15m.csv',
        strategy='ORB'
    )
    
    df_results, metrics = backtest.run()
    
    return df_results, metrics


def example_4_save_results():
    """
    Example 4: Run backtest and save results to CSV
    """
    print("\n" + "="*70)
    print("EXAMPLE 4: Save Results to CSV")
    print("="*70)
    
    backtest = BacktestStrategy(
        csv_file_path='/home/runner/work/Backtest-Trading/Backtest-Trading/2025 5m.csv',
        strategy='EMA'
    )
    
    df_results, metrics = backtest.run()
    
    # Save to CSV
    output_file = 'backtest_results_ema.csv'
    df_results.to_csv(output_file, index=False)
    print(f"\n✓ Results saved to: {output_file}")
    
    # Also save just the important columns
    important_cols = ['DateTime', 'Close', 'Signal', 'Returns', 'Strategy_Return', 'Cumulative_Return']
    df_results[important_cols].to_csv('backtest_summary.csv', index=False)
    print(f"✓ Summary saved to: backtest_summary.csv")
    
    return df_results, metrics


if __name__ == "__main__":
    # Choose which example to run (uncomment the one you want)
    
    # Example 1: Basic usage
    example_1_basic_usage()
    
    # Example 2: Compare all strategies (uncomment to run)
    # example_2_compare_strategies()
    
    # Example 3: Different timeframe (uncomment to run)
    # example_3_different_timeframe()
    
    # Example 4: Save results (uncomment to run)
    # example_4_save_results()
    
    print("\n" + "="*70)
    print("EXAMPLES COMPLETED")
    print("="*70)

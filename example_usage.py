"""
Example Usage of NQ Backtesting Strategy

This file demonstrates different ways to use the FVGBacktester class.
"""

from nq_backtest_strategy import FVGBacktester, run_all_strategies


def example_single_strategy():
    """Run a single strategy and get detailed results"""
    print("Example 1: Running single strategy (2R)")
    print("="*60)
    
    # Initialize backtester with 2R take profit
    backtester = FVGBacktester(
        data_dir="/home/runner/work/Backtest-Trading/Backtest-Trading",
        tp_multiplier='2R'
    )
    
    # Load data from all years
    backtester.load_data()
    
    # Run the backtest
    trades = backtester.run_backtest()
    
    # Calculate and print statistics
    stats = backtester.calculate_statistics()
    backtester.print_results(stats)
    
    # Access individual trades
    print(f"\nFirst 5 trades:")
    for i, trade in enumerate(trades[:5]):
        print(f"Trade {i+1}: {trade['direction']} - "
              f"Entry: {trade['entry_price']:.2f}, "
              f"Exit: {trade['exit_price']:.2f}, "
              f"PnL: {trade['pnl']:.2f}")


def example_specific_years():
    """Run backtest for specific years only"""
    print("\n\nExample 2: Running backtest for years 2023-2025 only")
    print("="*60)
    
    backtester = FVGBacktester(
        data_dir="/home/runner/work/Backtest-Trading/Backtest-Trading",
        tp_multiplier='1.5R'
    )
    
    # Load only specific years
    backtester.load_data(years=[2023, 2024, 2025])
    
    # Run backtest
    backtester.run_backtest()
    stats = backtester.calculate_statistics()
    backtester.print_results(stats)


def example_compare_strategies():
    """Compare all strategies"""
    print("\n\nExample 3: Comparing all strategies")
    print("="*60)
    
    # This runs all 4 strategies and prints comparison
    run_all_strategies("/home/runner/work/Backtest-Trading/Backtest-Trading")


def example_export_trades():
    """Export trades to CSV for further analysis"""
    print("\n\nExample 4: Exporting trades to CSV")
    print("="*60)
    
    import pandas as pd
    
    backtester = FVGBacktester(
        data_dir="/home/runner/work/Backtest-Trading/Backtest-Trading",
        tp_multiplier='2R'
    )
    
    backtester.load_data()
    trades = backtester.run_backtest()
    
    # Convert to DataFrame and save
    trades_df = pd.DataFrame(trades)
    output_file = "nq_trades_2R.csv"
    trades_df.to_csv(output_file, index=False)
    
    print(f"Exported {len(trades)} trades to {output_file}")
    print(f"\nColumns: {list(trades_df.columns)}")


if __name__ == "__main__":
    # Choose which example to run
    
    # Example 1: Single strategy
    # example_single_strategy()
    
    # Example 2: Specific years
    # example_specific_years()
    
    # Example 3: Compare all strategies (this is the default)
    example_compare_strategies()
    
    # Example 4: Export trades
    # example_export_trades()

"""
Quick test to verify the backtesting system works
"""
from nq_backtest_strategy import FVGBacktester

# Quick test with 2023 data only
print("Running quick verification test with 2023 data...")
print("="*60)

backtester = FVGBacktester(
    data_dir="/home/runner/work/Backtest-Trading/Backtest-Trading",
    tp_multiplier='1R'
)

# Load only 2023 data for quick test
backtester.load_data(years=[2023])

# Run backtest
backtester.run_backtest()

# Show results
stats = backtester.calculate_statistics()
backtester.print_results(stats)

print("\n✅ Verification test completed successfully!")
print(f"✅ Processed {len(backtester.df)} candles")
print(f"✅ Detected {len(backtester.fvg_list)} FVGs")
print(f"✅ Executed {len(backtester.trades)} trades")

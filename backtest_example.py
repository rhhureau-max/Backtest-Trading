"""
Example script demonstrating how to use the London Killzone strategies.

This script shows how to:
1. Load historical NQ data
2. Run backtests for all three strategies
3. Generate performance reports
4. Compare strategy results
"""

import os
import pandas as pd
from london_killzone_strategies import (
    DataLoader,
    TimeManager,
    StrategyA_JudasSwing,
    StrategyB_ORBRetest,
    StrategyC_HTFContinuation,
    BacktestEngine,
    create_comparison_table
)


def main():
    """Main execution function."""
    
    print("="*80)
    print("LONDON KILLZONE STRATEGIES - BACKTEST EXAMPLE")
    print("="*80)
    
    # Define data files to load
    # Adjust these paths based on your data availability
    base_path = "/home/runner/work/Backtest-Trading/Backtest-Trading"
    
    # For this example, we'll use 5-minute data from 2024
    # You can add more years as needed
    files_5m = [
        os.path.join(base_path, "2024 5m.csv"),
        # Add more files as needed:
        # os.path.join(base_path, "2023 5m.csv"),
        # os.path.join(base_path, "2022 5m.csv"),
    ]
    
    files_h4 = [
        os.path.join(base_path, "2024 4H.csv"),
    ]
    
    # Load data
    print("\n" + "="*80)
    print("LOADING DATA")
    print("="*80)
    
    print("\nLoading 5-minute data...")
    df_5m = DataLoader.load_multiple_files(files_5m)
    
    if len(df_5m) == 0:
        print("ERROR: No 5-minute data loaded. Please check file paths.")
        return
    
    print(f"\nTotal 5m candles loaded: {len(df_5m)}")
    print(f"Date range: {df_5m.index.min()} to {df_5m.index.max()}")
    
    print("\nLoading 4-hour data...")
    df_4h = DataLoader.load_multiple_files(files_h4)
    
    if len(df_4h) == 0:
        print("WARNING: No 4H data loaded. Strategy C will use fallback bias detection.")
        df_4h = None
    else:
        print(f"Total 4H candles loaded: {len(df_4h)}")
    
    # Convert to Paris timezone (assuming data is in UTC)
    print("\nConverting to Paris timezone...")
    try:
        df_5m = TimeManager.convert_to_paris_time(df_5m)
        if df_4h is not None:
            df_4h = TimeManager.convert_to_paris_time(df_4h)
        print("Timezone conversion successful")
    except Exception as e:
        print(f"Note: {e}")
        print("Proceeding with original timezone...")
    
    # Initialize backtest engine
    engine = BacktestEngine(df_5m, df_4h)
    
    # Define backtest period (optional - remove to test all data)
    # start_date = "2024-01-01"
    # end_date = "2024-12-31"
    start_date = None
    end_date = None
    
    # =========================================================================
    # STRATEGY A: JUDAS SWING
    # =========================================================================
    print("\n" + "="*80)
    print("STRATEGY A: JUDAS SWING")
    print("="*80)
    
    strategy_a = StrategyA_JudasSwing(points_offset=5.0, risk_reward=3.0)
    trades_a = engine.run_strategy(strategy_a, start_date, end_date)
    
    if trades_a:
        # Display first few trades
        print("\nSample trades:")
        df_trades_a = pd.DataFrame(trades_a)
        print(df_trades_a[['date', 'direction', 'entry_price', 'result', 'pnl_points']].head(10))
    
    perf_a = engine.generate_performance_report(trades_a, "Judas Swing")
    
    # =========================================================================
    # STRATEGY B: ORB RETEST
    # =========================================================================
    print("\n" + "="*80)
    print("STRATEGY B: ORB RETEST")
    print("="*80)
    
    strategy_b = StrategyB_ORBRetest(retest_window_hours=2)
    trades_b = engine.run_strategy(strategy_b, start_date, end_date)
    
    if trades_b:
        print("\nSample trades:")
        df_trades_b = pd.DataFrame(trades_b)
        print(df_trades_b[['date', 'direction', 'entry_price', 'result', 'pnl_points']].head(10))
    
    perf_b = engine.generate_performance_report(trades_b, "ORB Retest")
    
    # =========================================================================
    # STRATEGY C: HTF CONTINUATION
    # =========================================================================
    print("\n" + "="*80)
    print("STRATEGY C: HTF CONTINUATION (FIBONACCI OTE)")
    print("="*80)
    
    strategy_c = StrategyC_HTFContinuation(ote_low=0.618, ote_high=0.79)
    trades_c = engine.run_strategy(strategy_c, start_date, end_date)
    
    if trades_c:
        print("\nSample trades:")
        df_trades_c = pd.DataFrame(trades_c)
        print(df_trades_c[['date', 'direction', 'entry_price', 'result', 'pnl_points']].head(10))
    
    perf_c = engine.generate_performance_report(trades_c, "HTF Continuation")
    
    # =========================================================================
    # PERFORMANCE COMPARISON
    # =========================================================================
    print("\n" + "="*80)
    print("PERFORMANCE COMPARISON")
    print("="*80 + "\n")
    
    # Create performance comparison DataFrame
    performance_df = pd.DataFrame([perf_a, perf_b, perf_c])
    
    print(performance_df.to_string(index=False))
    
    # =========================================================================
    # STRATEGY CHARACTERISTICS COMPARISON
    # =========================================================================
    print("\n" + "="*80)
    print("STRATEGY CHARACTERISTICS COMPARISON")
    print("="*80 + "\n")
    
    comparison_table = create_comparison_table()
    print(comparison_table.to_string(index=False))
    
    # =========================================================================
    # KEY INSIGHTS
    # =========================================================================
    print("\n" + "="*80)
    print("KEY INSIGHTS")
    print("="*80 + "\n")
    
    # Find best strategy by different metrics
    if perf_a['total_trades'] > 0 or perf_b['total_trades'] > 0 or perf_c['total_trades'] > 0:
        best_win_rate = max(perf_a['win_rate'], perf_b['win_rate'], perf_c['win_rate'])
        best_profit_factor = max(perf_a['profit_factor'], perf_b['profit_factor'], perf_c['profit_factor'])
        best_total_pnl = max(perf_a['total_pnl'], perf_b['total_pnl'], perf_c['total_pnl'])
        
        print(f"Best Win Rate: {best_win_rate}%")
        print(f"Best Profit Factor: {best_profit_factor}")
        print(f"Best Total P&L: {best_total_pnl} points")
        
        print("\nStrategy Recommendations:")
        print("- Judas Swing: Best for volatile, choppy market opens")
        print("- ORB Retest: Best for trending days with clear direction")
        print("- HTF Continuation: Best when strong higher timeframe trend exists")
    
    print("\n" + "="*80)
    print("BACKTEST COMPLETE")
    print("="*80)
    
    # Optional: Save results to CSV
    save_results = input("\nDo you want to save detailed trade results to CSV? (y/n): ")
    if save_results.lower() == 'y':
        if trades_a:
            pd.DataFrame(trades_a).to_csv('strategy_a_trades.csv', index=False)
            print("Strategy A trades saved to: strategy_a_trades.csv")
        
        if trades_b:
            pd.DataFrame(trades_b).to_csv('strategy_b_trades.csv', index=False)
            print("Strategy B trades saved to: strategy_b_trades.csv")
        
        if trades_c:
            pd.DataFrame(trades_c).to_csv('strategy_c_trades.csv', index=False)
            print("Strategy C trades saved to: strategy_c_trades.csv")
        
        performance_df.to_csv('strategy_performance_summary.csv', index=False)
        print("Performance summary saved to: strategy_performance_summary.csv")


if __name__ == "__main__":
    main()

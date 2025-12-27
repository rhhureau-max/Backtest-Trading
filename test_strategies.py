"""
Quick validation test for London Killzone Strategies
"""

from london_killzone_strategies import (
    DataLoader,
    TimeManager,
    StrategyA_JudasSwing,
    StrategyB_ORBRetest,
    StrategyC_HTFContinuation,
    BacktestEngine,
    create_comparison_table
)
import pandas as pd

def test_basic_functionality():
    """Test basic functionality of the strategies."""
    
    print("="*80)
    print("VALIDATION TEST - LONDON KILLZONE STRATEGIES")
    print("="*80)
    
    # Test 1: Load data
    print("\n[TEST 1] Loading data...")
    try:
        df = DataLoader.load_csv('2024 5m.csv')
        print(f"✓ Successfully loaded {len(df)} rows")
        print(f"  Date range: {df.index.min()} to {df.index.max()}")
    except Exception as e:
        print(f"✗ Failed to load data: {e}")
        return False
    
    # Test 2: Initialize strategies
    print("\n[TEST 2] Initializing strategies...")
    try:
        strategy_a = StrategyA_JudasSwing()
        strategy_b = StrategyB_ORBRetest()
        strategy_c = StrategyC_HTFContinuation()
        print("✓ All strategies initialized successfully")
    except Exception as e:
        print(f"✗ Failed to initialize strategies: {e}")
        return False
    
    # Test 3: Initialize backtest engine
    print("\n[TEST 3] Initializing backtest engine...")
    try:
        engine = BacktestEngine(df, None)
        print("✓ Backtest engine initialized successfully")
    except Exception as e:
        print(f"✗ Failed to initialize engine: {e}")
        return False
    
    # Test 4: Test Strategy A on limited dataset
    print("\n[TEST 4] Testing Strategy A (Judas Swing) on sample data...")
    try:
        # Test on first 30 days only
        trades_a = engine.run_strategy(strategy_a, "2024-01-01", "2024-01-30")
        print(f"✓ Strategy A executed successfully")
        print(f"  Found {len(trades_a)} trades")
        if trades_a:
            perf_a = engine.generate_performance_report(trades_a, "Judas Swing")
            print(f"  Win Rate: {perf_a['win_rate']}%")
            print(f"  Total P&L: {perf_a['total_pnl']} points")
    except Exception as e:
        print(f"✗ Strategy A failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test 5: Test Strategy B
    print("\n[TEST 5] Testing Strategy B (ORB Retest) on sample data...")
    try:
        trades_b = engine.run_strategy(strategy_b, "2024-01-01", "2024-01-30")
        print(f"✓ Strategy B executed successfully")
        print(f"  Found {len(trades_b)} trades")
        if trades_b:
            perf_b = engine.generate_performance_report(trades_b, "ORB Retest")
            print(f"  Win Rate: {perf_b['win_rate']}%")
            print(f"  Total P&L: {perf_b['total_pnl']} points")
    except Exception as e:
        print(f"✗ Strategy B failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test 6: Test Strategy C
    print("\n[TEST 6] Testing Strategy C (HTF Continuation) on sample data...")
    try:
        trades_c = engine.run_strategy(strategy_c, "2024-01-01", "2024-01-30")
        print(f"✓ Strategy C executed successfully")
        print(f"  Found {len(trades_c)} trades")
        if trades_c:
            perf_c = engine.generate_performance_report(trades_c, "HTF Continuation")
            print(f"  Win Rate: {perf_c['win_rate']}%")
            print(f"  Total P&L: {perf_c['total_pnl']} points")
    except Exception as e:
        print(f"✗ Strategy C failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test 7: Generate comparison table
    print("\n[TEST 7] Generating strategy comparison table...")
    try:
        comparison = create_comparison_table()
        print("✓ Comparison table generated successfully")
        print("\n" + comparison.to_string(index=False))
    except Exception as e:
        print(f"✗ Failed to generate comparison: {e}")
        return False
    
    print("\n" + "="*80)
    print("ALL TESTS PASSED ✓")
    print("="*80)
    return True


if __name__ == "__main__":
    success = test_basic_functionality()
    exit(0 if success else 1)

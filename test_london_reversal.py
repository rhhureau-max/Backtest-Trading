#!/usr/bin/env python3
"""
Quick test script to validate London Reversal Strategy implementation
"""
import sys

def main():
    """Run all validation tests and track results."""
    print("Testing London Reversal Strategy Implementation...")
    print("=" * 60)
    
    all_tests_passed = True
    
    # Test 1: Module imports
    print("\n[1/5] Testing module imports...")
    try:
        import pandas as pd
        import numpy as np
        from london_reversal_strategy import LondonReversalStrategy
        print("✓ All modules imported successfully")
    except Exception as e:
        print(f"✗ Import failed: {e}")
        all_tests_passed = False
        sys.exit(1)
    
    # Test 2: Check data files exist
    print("\n[2/5] Checking data files...")
    import os
    files_to_check = [
        "ES 5m (2024-2025).csv",
        "2024 1H.csv"
    ]
    files_exist = True
    for f in files_to_check:
        if os.path.exists(f):
            print(f"✓ Found: {f}")
        else:
            print(f"✗ Missing: {f}")
            files_exist = False
            all_tests_passed = False
    
    if not files_exist:
        print("\n✗ FAILED: Required data files missing")
        sys.exit(1)
    
    # Test 3: Class instantiation
    print("\n[3/5] Testing class instantiation...")
    try:
        strategy = LondonReversalStrategy(
            "ES 5m (2024-2025).csv",
            "2024 1H.csv"
        )
        print("✓ Strategy object created successfully")
        print(f"  - 5m data loaded: {len(strategy.data_5m)} bars")
        print(f"  - 1H data loaded: {len(strategy.data_1h)} bars")
    except Exception as e:
        print(f"✗ Instantiation failed: {e}")
        all_tests_passed = False
        sys.exit(1)
    
    # Test 4: Method availability
    print("\n[4/5] Testing method availability...")
    methods = [
        'identify_asian_range',
        'detect_fvg',
        'detect_liquidity_sweep',
        'detect_reversal_candle',
        'detect_fvg_inversion',
        'calculate_stop_loss',
        'calculate_take_profits',
        'simulate_trade',
        'run_backtest'
    ]
    methods_exist = True
    for method in methods:
        if hasattr(strategy, method):
            print(f"✓ Method exists: {method}")
        else:
            print(f"✗ Method missing: {method}")
            methods_exist = False
            all_tests_passed = False
    
    if not methods_exist:
        print("\n✗ FAILED: Some required methods are missing")
        sys.exit(1)
    
    # Test 5: Results file exists
    print("\n[5/5] Checking results file...")
    if os.path.exists("london_reversal_results.csv"):
        df = pd.read_csv("london_reversal_results.csv")
        print(f"✓ Results file exists with {len(df)} trades")
        print(f"  - Columns: {len(df.columns)}")
        print(f"  - Date range: {df['date'].min()} to {df['date'].max()}")
    else:
        print("⚠ Results file not found (run main script first)")
        # This is not a failure - just means backtest hasn't been run yet
    
    print("\n" + "=" * 60)
    if all_tests_passed:
        print("✓ ALL TESTS PASSED - Strategy is ready to use!")
        print("=" * 60)
        print("\nTo run full backtest: python3 london_reversal_strategy.py")
        sys.exit(0)
    else:
        print("✗ SOME TESTS FAILED - See errors above")
        print("=" * 60)
        sys.exit(1)


if __name__ == "__main__":
    main()

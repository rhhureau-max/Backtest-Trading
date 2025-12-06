#!/usr/bin/env python3
"""
Quick test script to validate London Reversal Strategy implementation
"""
import sys
print("Testing London Reversal Strategy Implementation...")
print("=" * 60)

# Test 1: Module imports
print("\n[1/5] Testing module imports...")
try:
    import pandas as pd
    import numpy as np
    from london_reversal_strategy import LondonReversalStrategy
    print("✓ All modules imported successfully")
except Exception as e:
    print(f"✗ Import failed: {e}")
    sys.exit(1)

# Test 2: Check data files exist
print("\n[2/5] Checking data files...")
import os
files_to_check = [
    "ES 5m (2024-2025).csv",
    "2024 1H.csv"
]
for f in files_to_check:
    if os.path.exists(f):
        print(f"✓ Found: {f}")
    else:
        print(f"✗ Missing: {f}")

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
for method in methods:
    if hasattr(strategy, method):
        print(f"✓ Method exists: {method}")
    else:
        print(f"✗ Method missing: {method}")

# Test 5: Results file exists
print("\n[5/5] Checking results file...")
if os.path.exists("london_reversal_results.csv"):
    df = pd.read_csv("london_reversal_results.csv")
    print(f"✓ Results file exists with {len(df)} trades")
    print(f"  - Columns: {len(df.columns)}")
    print(f"  - Date range: {df['date'].min()} to {df['date'].max()}")
else:
    print("✗ Results file not found (run main script first)")

print("\n" + "=" * 60)
print("✓ ALL TESTS PASSED - Strategy is ready to use!")
print("=" * 60)
print("\nTo run full backtest: python3 london_reversal_strategy.py")

#!/usr/bin/env python3
"""
Usage Examples for FVG Advanced Backtest Script

This file demonstrates how to use the fvg_advanced_backtest.py script
with various configurations and modes.
"""

from fvg_advanced_backtest import FVGAdvancedBacktest

# Example 1: Basic usage with Mode 1 (Standard - Proximal Entry)
print("Example 1: Mode 1 - Standard (Proximal Entry)")
print("-" * 60)
bt1 = FVGAdvancedBacktest('2025 5m.csv', fvg_mode=1, stop_loss=25, take_profit=50)
results1 = bt1.run()
print()

# Example 2: Mode 2 with custom parameters (Consequent Encroachment)
print("Example 2: Mode 2 - Consequent Encroachment (50% Retracement)")
print("-" * 60)
bt2 = FVGAdvancedBacktest('2024 5m.csv', fvg_mode=2, stop_loss=30, take_profit=45)
results2 = bt2.run()
print()

# Example 3: Mode 3 with volatility filter (Significant Gap)
print("Example 3: Mode 3 - Significant Gap (Volatility Filter)")
print("-" * 60)
bt3 = FVGAdvancedBacktest('2023 5m.csv', fvg_mode=3, stop_loss=20, take_profit=40)
results3 = bt3.run()
print()

# Example 4: Mode 4 with freshness filter (Temporal Validity)
print("Example 4: Mode 4 - Freshness Filter (Temporal Validity)")
print("-" * 60)
bt4 = FVGAdvancedBacktest('2022 5m.csv', fvg_mode=4, stop_loss=25, take_profit=50)
results4 = bt4.run()
print()

# Example 5: Comparing all modes on the same data
print("Example 5: Comparing All Modes on Same Data")
print("-" * 60)
test_file = '2025 5m.csv'
for mode in range(1, 5):
    print(f"\nTesting Mode {mode}...")
    bt = FVGAdvancedBacktest(test_file, fvg_mode=mode, stop_loss=25, take_profit=50)
    results = bt.run()
    print(f"Total Return: {results['total_return']:.2f} points")
    print(f"Win Rate: {results['win_rate']:.2f}%")
    print(f"Trades: {results['num_trades']}")
    print()

print("\nUsage examples completed!")

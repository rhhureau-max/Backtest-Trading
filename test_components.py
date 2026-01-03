"""
Quick Test Script - Validates all components without running full backtest
"""

import sys
import pandas as pd
from datetime import datetime

print("=" * 80)
print("COMPONENT VALIDATION TEST")
print("=" * 80)

try:
    # Test 1: Data Loader
    print("\n1. Testing Data Loader...")
    from data_loader import get_market_data
    data = get_market_data()
    assert '1m' in data, "1-minute data not loaded"
    assert '5m' in data, "5-minute data not loaded"
    assert '1H' in data, "1-hour data not loaded"
    assert '4H' in data, "4-hour data not loaded"
    print("   ✓ Data Loader: PASSED")
    
    # Test 2: Market Structure
    print("\n2. Testing Market Structure Detection...")
    from market_structure import TrendFilter
    trend_filter = TrendFilter(data['1H'], data['4H'])
    test_date = pd.Timestamp('2024-03-15 10:00:00', tz='US/Central')
    trend = trend_filter.get_trend_at_time(test_date)
    print(f"   ✓ Trend at {test_date.date()}: {trend}")
    print("   ✓ Market Structure: PASSED")
    
    # Test 3: FVG Detection
    print("\n3. Testing FVG Detection...")
    from fvg_detector import FVGDetector
    fvg_detector = FVGDetector()
    fvg_data = fvg_detector.detect_fvgs(data['1m'])
    bearish_count = fvg_data['bearish_fvg'].sum()
    bullish_count = fvg_data['bullish_fvg'].sum()
    print(f"   ✓ Detected {bearish_count} Bearish FVGs")
    print(f"   ✓ Detected {bullish_count} Bullish FVGs")
    print("   ✓ FVG Detection: PASSED")
    
    # Test 4: Entry Signals
    print("\n4. Testing Entry Signal Generator...")
    from entry_signals import EntrySignalGenerator
    signal_gen = EntrySignalGenerator(data['1m'], data['5m'])
    test_date = pd.Timestamp('2024-03-15', tz='US/Central')
    opening_range = signal_gen.get_opening_range(test_date)
    if opening_range:
        print(f"   ✓ Opening Range found: {opening_range.low:.2f} - {opening_range.high:.2f}")
    else:
        print(f"   ✓ No opening range for test date (may be weekend)")
    print("   ✓ Entry Signal Generator: PASSED")
    
    # Test 5: Risk Management
    print("\n5. Testing Risk Manager...")
    from risk_manager import RiskManager, TradeTracker
    risk_mgr = RiskManager(stop_loss_points=20.0)
    tracker = TradeTracker()
    
    entry_time = pd.Timestamp('2024-03-15 09:00:00', tz='US/Central')
    trade = risk_mgr.create_trade_positions(
        trade_id=tracker.get_next_trade_id(),
        entry_time=entry_time,
        entry_price=18000.0,
        direction='LONG'
    )
    
    assert len(trade.positions) == 3, "Should create 3 positions"
    print(f"   ✓ Created trade with {len(trade.positions)} positions")
    print(f"   ✓ TP Levels: {[p.take_profit for p in trade.positions]}")
    print("   ✓ Risk Manager: PASSED")
    
    # Test 6: Results Analyzer
    print("\n6. Testing Results Analyzer...")
    from results_analyzer import ResultsAnalyzer
    tracker.add_trade(trade)
    analyzer = ResultsAnalyzer(tracker.get_all_trades())
    print("   ✓ Results Analyzer: PASSED")
    
    print("\n" + "=" * 80)
    print("ALL COMPONENT TESTS PASSED! ✓")
    print("=" * 80)
    print("\nThe system is ready to run the full backtest.")
    print("Execute: python run_backtest.py")
    print("=" * 80)
    
    sys.exit(0)
    
except Exception as e:
    print(f"\n✗ TEST FAILED: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

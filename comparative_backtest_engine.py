"""
Comparative Backtest Engine
Runs three risk management strategies on the same entry signals
"""

import pandas as pd
import numpy as np
from typing import Dict, List
from datetime import datetime
from tqdm import tqdm

from data_loader import get_market_data
from ema_trend_filter import EMATrendFilter
from fvg_detector import FVGDetector
from simplified_entry_signals import SimplifiedEntrySignalGenerator
from comparative_risk_strategies import (
    StrategyAManager, StrategyBManager, StrategyCManager,
    StrategyAResult, StrategyBResult, StrategyCResult
)


class ComparativeBacktestEngine:
    """Runs comparative backtest with 3 risk strategies"""
    
    def __init__(self, data: Dict[str, pd.DataFrame], min_fvg_size: float = 2.0):
        """
        Args:
            data: Dictionary with '1m', '5m', '1H' DataFrames
            min_fvg_size: Minimum FVG size in points
        """
        print("\n" + "=" * 80)
        print("INITIALIZING COMPARATIVE BACKTEST ENGINE")
        print("=" * 80)
        
        self.data = data
        
        # Initialize trend filter
        print("\n1. Setting up EMA Trend Filter (H1 with EMA 200)...")
        self.trend_filter = EMATrendFilter(data['1H'], ema_period=200)
        
        # Detect FVGs
        print("\n2. Detecting Fair Value Gaps (1-minute)...")
        self.fvg_detector = FVGDetector()
        self.fvg_data = self.fvg_detector.detect_fvgs(data['1m'])
        
        # Entry signal generator
        print(f"\n3. Setting up Entry Signal Generator (min FVG size: {min_fvg_size} points)...")
        self.signal_generator = SimplifiedEntrySignalGenerator(
            data['1m'], 
            data['5m'],
            min_fvg_size=min_fvg_size
        )
        
        # Initialize three risk managers
        print("\n4. Initializing Three Risk Management Strategies...")
        self.strategy_a = StrategyAManager()
        print("   ✓ Strategy A: Scalper Fixe (SL 20pts, TP 25pts)")
        self.strategy_b = StrategyBManager()
        print("   ✓ Strategy B: ICT Liquidité Range (SL candle±2pts, TP range)")
        self.strategy_c = StrategyCManager()
        print("   ✓ Strategy C: Standard Deviation (SL 20pts, TP 2x/4x H_Range)")
        
        # Results storage
        self.results_a: List[StrategyAResult] = []
        self.results_b: List[StrategyBResult] = []
        self.results_c: List[StrategyCResult] = []
        self.entry_signals = []
        
        print("\n" + "=" * 80)
        print("ENGINE INITIALIZATION COMPLETE")
        print("=" * 80)
    
    def find_entry_signals(self) -> List[Dict]:
        """Find all entry signals across all days"""
        print("\n" + "=" * 80)
        print("FINDING ENTRY SIGNALS")
        print("=" * 80)
        
        # Get all unique trading dates
        if isinstance(self.fvg_data.index, pd.DatetimeIndex):
            dates = self.fvg_data.index.normalize().unique()
        else:
            dates = pd.to_datetime(self.fvg_data.index).normalize().unique()
        dates = sorted(dates)
        
        print(f"\nScanning {len(dates)} trading days for entry signals...")
        
        signals = []
        
        for date in tqdm(dates, desc="Scanning", unit="day"):
            # Get opening range
            opening_range = self.signal_generator.get_opening_range(date)
            if opening_range is None:
                continue
            
            # Get trend
            market_open = date.replace(hour=9, minute=30, second=0, microsecond=0)
            trend = self.trend_filter.get_trend_at_time(market_open)
            if trend is None:
                continue
            
            # Trading window: 08:35 - 11:30
            start_time = date.replace(hour=8, minute=35, second=0, microsecond=0)
            end_time = date.replace(hour=11, minute=30, second=0, microsecond=0)
            
            mask = (self.fvg_data.index >= start_time) & (self.fvg_data.index <= end_time)
            day_data = self.fvg_data[mask]
            
            if len(day_data) == 0:
                continue
            
            liquidity_status = None
            
            # Look for entry signal
            for idx, row in day_data.iterrows():
                current_time = idx
                
                # Check liquidity grab
                if liquidity_status is None:
                    liquidity_status = self.signal_generator.check_liquidity_grab(
                        opening_range, current_time
                    )
                
                # Check for entry
                entry_signal = None
                if trend == 'bullish' and liquidity_status == 'grabbed_low':
                    entry_signal = self.signal_generator.check_long_setup(
                        opening_range=opening_range,
                        current_time=current_time,
                        current_candle=row,
                        fvg_data=self.fvg_data,
                        liquidity_status=liquidity_status
                    )
                elif trend == 'bearish' and liquidity_status == 'grabbed_high':
                    entry_signal = self.signal_generator.check_short_setup(
                        opening_range=opening_range,
                        current_time=current_time,
                        current_candle=row,
                        fvg_data=self.fvg_data,
                        liquidity_status=liquidity_status
                    )
                
                if entry_signal:
                    signals.append({
                        'date': date,
                        'entry_time': entry_signal.timestamp,
                        'entry_price': entry_signal.entry_price,
                        'direction': entry_signal.direction,
                        'opening_range_high': opening_range.high,
                        'opening_range_low': opening_range.low,
                        'signal_candle': row,
                        'trend': trend
                    })
                    break  # One signal per day
        
        print(f"\n✓ Found {len(signals)} entry signals")
        return signals
    
    def run_comparative_backtest(self):
        """Run backtest with all three strategies"""
        print("\n" + "=" * 80)
        print("RUNNING COMPARATIVE BACKTEST")
        print("=" * 80)
        
        # Find entry signals
        self.entry_signals = self.find_entry_signals()
        
        if not self.entry_signals:
            print("\n⚠️ No entry signals found!")
            return
        
        print(f"\nSimulating {len(self.entry_signals)} trades with 3 strategies...")
        
        # Session close time
        session_close_hour = 15
        session_close_minute = 45
        
        for signal in tqdm(self.entry_signals, desc="Simulating", unit="trade"):
            # Get price data for simulation (until session close)
            session_close = signal['date'].replace(
                hour=session_close_hour, 
                minute=session_close_minute, 
                second=0, 
                microsecond=0
            )
            
            mask = (self.data['1m'].index >= signal['entry_time']) & \
                   (self.data['1m'].index <= session_close)
            price_data = self.data['1m'][mask]
            
            if len(price_data) == 0:
                continue
            
            # Strategy A
            result_a = self.strategy_a.simulate_trade(
                entry_time=signal['entry_time'],
                entry_price=signal['entry_price'],
                direction=signal['direction'],
                price_data=price_data
            )
            self.results_a.append(result_a)
            
            # Strategy B
            result_b = self.strategy_b.simulate_trade(
                entry_time=signal['entry_time'],
                entry_price=signal['entry_price'],
                direction=signal['direction'],
                price_data=price_data,
                signal_candle=signal['signal_candle'],
                opening_range_high=signal['opening_range_high'],
                opening_range_low=signal['opening_range_low']
            )
            self.results_b.append(result_b)
            
            # Strategy C
            result_c = self.strategy_c.simulate_trade(
                entry_time=signal['entry_time'],
                entry_price=signal['entry_price'],
                direction=signal['direction'],
                price_data=price_data,
                opening_range_high=signal['opening_range_high'],
                opening_range_low=signal['opening_range_low']
            )
            self.results_c.append(result_c)
        
        print(f"\n✓ Simulation complete!")
        print(f"   Strategy A: {len(self.results_a)} trades")
        print(f"   Strategy B: {len([r for r in self.results_b if not r.skipped])} trades ({len([r for r in self.results_b if r.skipped])} skipped)")
        print(f"   Strategy C: {len(self.results_c)} trades")
    
    def get_results(self) -> Dict:
        """Get comparative results"""
        return {
            'strategy_a': self.results_a,
            'strategy_b': self.results_b,
            'strategy_c': self.results_c,
            'entry_signals': self.entry_signals
        }


def run_comparative_backtest(data: Dict[str, pd.DataFrame], min_fvg_size: float = 2.0) -> Dict:
    """
    Convenience function to run comparative backtest
    
    Args:
        data: Dictionary with market data
        min_fvg_size: Minimum FVG size in points
        
    Returns:
        Dictionary with results for all three strategies
    """
    engine = ComparativeBacktestEngine(data, min_fvg_size)
    engine.run_comparative_backtest()
    return engine.get_results()


if __name__ == "__main__":
    print("Testing Comparative Backtest Engine...")
    data = get_market_data()
    results = run_comparative_backtest(data, min_fvg_size=2.0)
    
    print(f"\n✓ Backtest complete")
    print(f"Entry signals: {len(results['entry_signals'])}")
    print(f"Strategy A results: {len(results['strategy_a'])}")
    print(f"Strategy B results: {len([r for r in results['strategy_b'] if not r.skipped])}")
    print(f"Strategy C results: {len(results['strategy_c'])}")

"""
Backtesting Engine
Main execution engine that orchestrates the entire backtest
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from datetime import time, datetime
from tqdm import tqdm

from market_structure import TrendFilter
from fvg_detector import FVGDetector
from entry_signals import EntrySignalGenerator, EntrySignal
from risk_manager import RiskManager, TradeTracker, Trade


class BacktestEngine:
    """Main backtesting engine"""
    
    def __init__(
        self,
        data: Dict[str, pd.DataFrame],
        stop_loss_points: float = 20.0
    ):
        """
        Args:
            data: Dictionary with '1m', '5m', '1H', '4H' DataFrames
            stop_loss_points: Fixed stop loss in points
        """
        print("\n" + "=" * 80)
        print("INITIALIZING BACKTEST ENGINE")
        print("=" * 80)
        
        self.data = data
        self.stop_loss_points = stop_loss_points
        
        # Initialize components
        print("\n1. Setting up Trend Filter (H1 & H4)...")
        self.trend_filter = TrendFilter(data['1H'], data['4H'])
        
        print("\n2. Detecting Fair Value Gaps (1-minute)...")
        self.fvg_detector = FVGDetector()
        self.fvg_data = self.fvg_detector.detect_fvgs(data['1m'])
        
        print("\n3. Setting up Entry Signal Generator...")
        self.signal_generator = EntrySignalGenerator(data['1m'], data['5m'])
        
        print("\n4. Initializing Risk Manager...")
        self.risk_manager = RiskManager(stop_loss_points=stop_loss_points)
        
        print("\n5. Setting up Trade Tracker...")
        self.trade_tracker = TradeTracker()
        
        # Active trades
        self.active_trades: List[Trade] = []
        
        print("\n" + "=" * 80)
        print("ENGINE INITIALIZATION COMPLETE")
        print("=" * 80)
    
    def process_day(self, date: pd.Timestamp) -> int:
        """
        Process a single trading day
        
        Args:
            date: Date to process
            
        Returns:
            Number of new trades opened
        """
        # Get opening range for this day
        opening_range = self.signal_generator.get_opening_range(date)
        
        if opening_range is None:
            return 0
        
        # Get trend for this day (check at market open)
        market_open = date.replace(hour=9, minute=30, second=0, microsecond=0)
        trend = self.trend_filter.get_trend_at_time(market_open)
        
        if trend is None:
            # No clear trend, skip this day
            return 0
        
        # Get 1-minute data for this day's trading window (08:35 - 11:00)
        start_time = date.replace(hour=8, minute=35, second=0, microsecond=0)
        end_time = date.replace(hour=11, minute=0, second=0, microsecond=0)
        
        # Get bars in trading window
        mask = (self.fvg_data.index >= start_time) & (self.fvg_data.index <= end_time)
        day_data = self.fvg_data[mask]
        
        if len(day_data) == 0:
            return 0
        
        new_trades = 0
        entry_taken = False  # Only one entry per day
        
        # Iterate through each 1-minute bar
        for idx, row in day_data.iterrows():
            current_time = idx
            
            # Update active trades
            self._update_active_trades(row, current_time)
            
            # Check for entry signal (only if no entry taken today)
            if not entry_taken:
                entry_signal = self._check_entry_signal(
                    opening_range=opening_range,
                    current_time=current_time,
                    trend=trend
                )
                
                if entry_signal:
                    # Create new trade
                    trade = self.risk_manager.create_trade_positions(
                        trade_id=self.trade_tracker.get_next_trade_id(),
                        entry_time=entry_signal.timestamp,
                        entry_price=entry_signal.entry_price,
                        direction=entry_signal.direction
                    )
                    
                    self.trade_tracker.add_trade(trade)
                    self.active_trades.append(trade)
                    new_trades += 1
                    entry_taken = True
        
        # End of day: close any remaining open positions
        if day_data.index.size > 0:
            eod_time = day_data.index[-1]
            eod_close = day_data.iloc[-1]['Close']
            self._close_positions_eod(eod_time, eod_close)
        
        return new_trades
    
    def _check_entry_signal(
        self,
        opening_range,
        current_time: pd.Timestamp,
        trend: str
    ) -> Optional[EntrySignal]:
        """Check for entry signal based on trend and setup"""
        
        if trend == 'bullish':
            # Only look for LONG setups
            signal = self.signal_generator.check_long_setup(
                opening_range=opening_range,
                current_time=current_time,
                fvg_data=self.fvg_data
            )
            return signal
        
        elif trend == 'bearish':
            # Only look for SHORT setups
            signal = self.signal_generator.check_short_setup(
                opening_range=opening_range,
                current_time=current_time,
                fvg_data=self.fvg_data
            )
            return signal
        
        return None
    
    def _update_active_trades(self, bar: pd.Series, current_time: pd.Timestamp):
        """Update all active trades with current bar data"""
        for trade in self.active_trades:
            for position in trade.positions:
                if not position.is_closed():
                    self.risk_manager.update_position(
                        position=position,
                        current_time=current_time,
                        current_high=bar['High'],
                        current_low=bar['Low'],
                        current_close=bar['Close']
                    )
    
    def _close_positions_eod(self, eod_time: pd.Timestamp, eod_close: float):
        """Close all open positions at end of day"""
        for trade in self.active_trades:
            for position in trade.positions:
                if not position.is_closed():
                    self.risk_manager.close_position_eod(
                        position=position,
                        exit_time=eod_time,
                        exit_price=eod_close
                    )
        
        # Remove fully closed trades from active list
        self.active_trades = [t for t in self.active_trades if not t.is_fully_closed()]
    
    def run(self) -> TradeTracker:
        """
        Run the complete backtest
        
        Returns:
            TradeTracker with all trades
        """
        print("\n" + "=" * 80)
        print("STARTING BACKTEST EXECUTION")
        print("=" * 80)
        
        # Get all unique trading dates from 1-minute data
        dates = self.fvg_data.index.normalize().unique()
        dates = sorted(dates)
        
        print(f"\nProcessing {len(dates)} trading days...")
        print(f"Date range: {dates[0].date()} to {dates[-1].date()}")
        print("\nRunning backtest...")
        
        total_trades = 0
        
        # Process each day with progress bar
        for date in tqdm(dates, desc="Backtesting", unit="day"):
            new_trades = self.process_day(date)
            total_trades += new_trades
        
        print(f"\n\n" + "=" * 80)
        print("BACKTEST EXECUTION COMPLETE")
        print("=" * 80)
        print(f"Total trades executed: {total_trades}")
        print(f"Closed trades: {len(self.trade_tracker.get_closed_trades())}")
        
        return self.trade_tracker


def run_backtest(
    data: Dict[str, pd.DataFrame],
    stop_loss_points: float = 20.0
) -> TradeTracker:
    """
    Convenience function to run backtest
    
    Args:
        data: Market data dictionary
        stop_loss_points: Stop loss in points
        
    Returns:
        TradeTracker with results
    """
    engine = BacktestEngine(data, stop_loss_points)
    return engine.run()


if __name__ == "__main__":
    # Test the backtest engine
    from data_loader import get_market_data
    
    print("Loading data...")
    data = get_market_data()
    
    print("\nRunning backtest...")
    tracker = run_backtest(data)
    
    print("\nBacktest complete!")
    metrics = tracker.get_performance_metrics()
    print(f"Total trades: {metrics['total_trades']}")
    print(f"Win rate: {metrics['win_rate']:.2f}%")
    print(f"Total PnL: {metrics['total_pnl']:.2f} points")

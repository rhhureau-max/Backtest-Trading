"""
Updated Backtesting Engine
Implements simplified ICT strategy with EMA filter and permissive FVG entries
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from datetime import time, datetime
from tqdm import tqdm

from ema_trend_filter import EMATrendFilter
from fvg_detector import FVGDetector
from simplified_entry_signals import SimplifiedEntrySignalGenerator, EntrySignal
from updated_risk_manager import UpdatedRiskManager, TradeTracker, Trade


class UpdatedBacktestEngine:
    """Updated backtesting engine with simplified logic"""
    
    def __init__(
        self,
        data: Dict[str, pd.DataFrame],
        stop_loss_points: float = 25.0,
        min_fvg_size: float = 2.0
    ):
        """
        Args:
            data: Dictionary with '1m', '5m', '1H' DataFrames
            stop_loss_points: Fixed stop loss in points (default: 25)
            min_fvg_size: Minimum FVG size in points (default: 2.0)
        """
        print("\n" + "=" * 80)
        print("INITIALIZING UPDATED BACKTEST ENGINE")
        print("=" * 80)
        
        self.data = data
        self.stop_loss_points = stop_loss_points
        self.min_fvg_size = min_fvg_size
        
        # Initialize components
        print("\n1. Setting up EMA Trend Filter (H1 with EMA 200)...")
        self.trend_filter = EMATrendFilter(data['1H'], ema_period=200)
        
        print("\n2. Detecting Fair Value Gaps (1-minute)...")
        self.fvg_detector = FVGDetector()
        self.fvg_data = self.fvg_detector.detect_fvgs(data['1m'])
        
        print(f"\n3. Setting up Entry Signal Generator (min FVG size: {min_fvg_size} points)...")
        self.signal_generator = SimplifiedEntrySignalGenerator(
            data['1m'], 
            data['5m'],
            min_fvg_size=min_fvg_size
        )
        
        print("\n4. Initializing Risk Manager (SL: 25 points, TPs: 20/40 + runner)...")
        self.risk_manager = UpdatedRiskManager(stop_loss_points=stop_loss_points)
        
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
        
        # Trading window: 08:35 - 11:30 (extended from 11:00)
        start_time = date.replace(hour=8, minute=35, second=0, microsecond=0)
        end_time = date.replace(hour=11, minute=30, second=0, microsecond=0)
        
        # Session close time: 15:45
        session_close = date.replace(hour=15, minute=45, second=0, microsecond=0)
        
        # Get bars for the full day (to manage open positions until session close)
        day_start = date.replace(hour=8, minute=35, second=0, microsecond=0)
        day_end = session_close
        
        mask = (self.fvg_data.index >= day_start) & (self.fvg_data.index <= day_end)
        day_data = self.fvg_data[mask]
        
        if len(day_data) == 0:
            return 0
        
        new_trades = 0
        entry_taken = False  # Only one entry per day
        liquidity_status = None  # Track liquidity grab
        
        # Iterate through each 1-minute bar
        for idx, row in day_data.iterrows():
            current_time = idx
            
            # Update active trades first
            self._update_active_trades(row, current_time)
            
            # Check for entry signal (only if no entry taken today and within entry window)
            if not entry_taken and current_time <= end_time:
                # Check for liquidity grab if not already grabbed
                if liquidity_status is None:
                    liquidity_status = self.signal_generator.check_liquidity_grab(
                        opening_range, current_time
                    )
                
                # Check for entry signal based on trend and liquidity
                entry_signal = self._check_entry_signal(
                    opening_range=opening_range,
                    current_time=current_time,
                    current_candle=row,
                    trend=trend,
                    liquidity_status=liquidity_status
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
            
            # Close all positions at session end
            if current_time >= session_close:
                self._close_all_at_eod(row, current_time)
        
        return new_trades
    
    def _check_entry_signal(
        self,
        opening_range,
        current_time: pd.Timestamp,
        current_candle: pd.Series,
        trend: str,
        liquidity_status: Optional[str]
    ) -> Optional[EntrySignal]:
        """
        Check for entry signal based on trend and liquidity
        
        Args:
            opening_range: Opening range object
            current_time: Current timestamp
            current_candle: Current 1-minute candle
            trend: 'bullish' or 'bearish'
            liquidity_status: Current liquidity grab status
            
        Returns:
            EntrySignal if valid setup exists
        """
        # LONG setups (bullish trend + grabbed low liquidity)
        if trend == 'bullish':
            return self.signal_generator.check_long_setup(
                opening_range=opening_range,
                current_time=current_time,
                current_candle=current_candle,
                fvg_data=self.fvg_data,
                liquidity_status=liquidity_status
            )
        
        # SHORT setups (bearish trend + grabbed high liquidity)
        elif trend == 'bearish':
            return self.signal_generator.check_short_setup(
                opening_range=opening_range,
                current_time=current_time,
                current_candle=current_candle,
                fvg_data=self.fvg_data,
                liquidity_status=liquidity_status
            )
        
        return None
    
    def _update_active_trades(self, candle: pd.Series, current_time: pd.Timestamp):
        """Update all active trades"""
        for trade in self.active_trades:
            for position in trade.get_open_positions():
                self.risk_manager.update_position(position, candle, current_time)
        
        # Remove fully closed trades from active list
        self.active_trades = [t for t in self.active_trades if not t.is_fully_closed()]
    
    def _close_all_at_eod(self, candle: pd.Series, current_time: pd.Timestamp):
        """Close all open positions at end of day"""
        exit_price = candle['Close']
        
        for trade in self.active_trades:
            for position in trade.get_open_positions():
                self.risk_manager.close_position_at_eod(position, exit_price, current_time)
        
        # Clear active trades
        self.active_trades = []
    
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
        if isinstance(self.fvg_data.index, pd.DatetimeIndex):
            dates = self.fvg_data.index.normalize().unique()
        else:
            dates = pd.to_datetime(self.fvg_data.index).normalize().unique()
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


def run_backtest(data: Dict[str, pd.DataFrame], stop_loss_points: float = 25.0, min_fvg_size: float = 2.0) -> TradeTracker:
    """
    Convenience function to run backtest
    
    Args:
        data: Dictionary with market data
        stop_loss_points: Stop loss in points
        min_fvg_size: Minimum FVG size in points
        
    Returns:
        TradeTracker with results
    """
    engine = UpdatedBacktestEngine(data, stop_loss_points, min_fvg_size)
    return engine.run()


if __name__ == "__main__":
    from data_loader import get_market_data
    
    print("Testing Updated Backtest Engine...")
    data = get_market_data()
    
    tracker = run_backtest(data, stop_loss_points=25.0, min_fvg_size=2.0)
    
    print(f"\nTotal trades: {len(tracker.get_all_trades())}")
    print(f"Total PnL: {tracker.get_total_pnl():.2f} points")

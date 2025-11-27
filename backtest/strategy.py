"""
Strategy module implementing the FVG + Liquidity Sweep trading strategy.

Strategy Logic:
1. Check if current time is within a trading session
2. Check for HTF context (FVG in H1/M15 or liquidity sweep)
3. Look for M5 FVG formation and fill with reversal
4. Execute trade with proper SL/TP management
"""
import pandas as pd
import numpy as np
from datetime import datetime, time, timedelta
from typing import Optional, Tuple, List, Dict
import logging

from config import BacktestConfig, SessionConfig
from fvg_detector import FVG, detect_fvg, detect_m5_fvg_for_entry
from liquidity_detector import (
    detect_fractals, find_active_liquidity_zone, get_htf_context
)
from trade_manager import (
    TradeManager, Trade, TradeDirection, TradeStatus,
    find_swing_for_stop_loss
)

logger = logging.getLogger(__name__)


def is_within_session(current_time: datetime, sessions: Tuple[SessionConfig, ...]) -> Optional[str]:
    """
    Check if current time is within any trading session.
    
    Args:
        current_time: Current datetime (assumed UTC)
        sessions: Tuple of SessionConfig objects
        
    Returns:
        Session name if within a session, None otherwise
    """
    current_time_only = current_time.time()
    
    for session in sessions:
        if session.start <= current_time_only < session.end:
            return session.name
    
    return None


def check_htf_context(
    h1_data: pd.DataFrame,
    m15_data: pd.DataFrame,
    current_time: datetime,
    config: BacktestConfig
) -> Optional[Tuple[str, str]]:
    """
    Check for valid HTF trading context.
    
    Only uses liquidity sweeps for HTF context (no FVG).
    
    Returns:
        Tuple of (trade_direction, context_type) if valid context found, None otherwise
    """
    # Check for liquidity sweep only
    liq_zone = find_active_liquidity_zone(
        h1_data, m15_data, current_time,
        lookback_hours=48,
        fractal_lookback=config.fractal_lookback,
        sweep_buffer_pct=config.liquidity_sweep_buffer_pct
    )
    
    if liq_zone:
        direction, price, sweep_time = liq_zone
        logger.debug(f"Found liquidity sweep at {current_time}: {direction} at {price:.2f}")
        return (direction, 'liquidity_sweep')
    
    return None


def find_m5_entry_signal(
    m5_data: pd.DataFrame,
    current_time: datetime,
    trade_direction: str,
    config: BacktestConfig
) -> Optional[Tuple[FVG, datetime, pd.Series, float]]:
    """
    Look for M5 FVG formation, fill, and reversal for entry signal.
    
    Args:
        m5_data: 5-minute OHLC data
        current_time: Current time to start looking
        trade_direction: Expected trade direction ('bullish' or 'bearish')
        config: Backtest configuration
        
    Returns:
        Tuple of (fvg, entry_time, entry_candle, swing_for_sl) if signal found, None otherwise
    """
    result = detect_m5_fvg_for_entry(
        m5_data, current_time, trade_direction,
        max_candles=config.max_fvg_fill_candles,
        min_gap_pct=config.fvg_min_gap_pct
    )
    
    if result:
        fvg, entry_time, entry_candle = result
        
        # Find swing for stop loss placement
        swing_price = find_swing_for_stop_loss(
            m5_data, entry_time,
            TradeDirection.LONG if trade_direction == 'bullish' else TradeDirection.SHORT,
            fvg.timestamp
        )
        
        return (fvg, entry_time, entry_candle, swing_price)
    
    return None


class Strategy:
    """
    Main strategy class that coordinates the backtest.
    """
    
    def __init__(self, config: BacktestConfig):
        """Initialize the strategy."""
        self.config = config
        self.trade_manager = TradeManager(
            risk_reward_ratio=config.risk_reward_ratio,
            stop_loss_buffer_pct=config.stop_loss_buffer_pct
        )
        
        # Track session entries to avoid multiple entries in same session
        self._last_session_entry: Dict[str, datetime] = {}
    
    def run_backtest(
        self,
        h1_data: pd.DataFrame,
        m15_data: pd.DataFrame,
        m5_data: pd.DataFrame
    ) -> List[Trade]:
        """
        Run the complete backtest.
        
        Args:
            h1_data: 1-hour OHLC data
            m15_data: 15-minute OHLC data
            m5_data: 5-minute OHLC data
            
        Returns:
            List of all trades executed
        """
        logger.info("Starting backtest...")
        logger.info(f"Data range: {m5_data.index.min()} to {m5_data.index.max()}")
        logger.info(f"Total M5 candles: {len(m5_data)}")
        
        # Get unique dates for progress tracking
        unique_dates = m5_data.index.date
        total_days = len(set(unique_dates))
        processed_days = 0
        last_date = None
        
        # Iterate through M5 candles
        for i, (current_time, candle) in enumerate(m5_data.iterrows()):
            # Progress logging
            current_date = current_time.date()
            if current_date != last_date:
                last_date = current_date
                processed_days += 1
                if processed_days % 100 == 0:
                    logger.info(f"Progress: {processed_days}/{total_days} days, "
                              f"{len(self.trade_manager.trades)} trades")
            
            # Update any open trade first
            if self.trade_manager.has_open_trade():
                self.trade_manager.update_trade(current_time, candle)
                continue  # Don't look for new entries while in a trade
            
            # Check if we're in a trading session
            session_name = is_within_session(current_time, self.config.sessions)
            if not session_name:
                continue
            
            # Check if we already entered in this session today
            session_key = (current_date, session_name)
            if session_key in self._last_session_entry:
                continue
            
            # Check for HTF context
            htf_context = check_htf_context(h1_data, m15_data, current_time, self.config)
            if not htf_context:
                continue
            
            trade_direction, context_type = htf_context
            
            # Look for M5 entry signal
            entry_signal = find_m5_entry_signal(
                m5_data, current_time, trade_direction, self.config
            )
            
            if not entry_signal:
                continue
            
            fvg, entry_time, entry_candle, swing_price = entry_signal
            
            # Check that entry time is still within session
            entry_session = is_within_session(entry_time, self.config.sessions)
            if entry_session != session_name:
                continue
            
            # Execute trade
            direction = TradeDirection.LONG if trade_direction == 'bullish' else TradeDirection.SHORT
            entry_price = entry_candle['Close']
            
            trade = self.trade_manager.open_trade(
                entry_time=entry_time,
                entry_price=entry_price,
                direction=direction,
                swing_price=swing_price,
                session=session_name,
                htf_context=context_type
            )
            
            if trade:
                self._last_session_entry[session_key] = entry_time
                logger.debug(
                    f"Entry signal: {trade_direction} at {entry_time}, "
                    f"price: {entry_price:.2f}, context: {context_type}"
                )
        
        # Close any remaining open trade at end of data
        if self.trade_manager.has_open_trade():
            last_candle = m5_data.iloc[-1]
            last_time = m5_data.index[-1]
            self.trade_manager.current_trade.close(last_time, last_candle['Close'])
            logger.info("Closed remaining open trade at end of data")
        
        logger.info(f"Backtest complete. Total trades: {len(self.trade_manager.trades)}")
        
        return self.trade_manager.get_all_trades()
    
    def get_trades(self) -> List[Trade]:
        """Get all trades from the backtest."""
        return self.trade_manager.get_all_trades()
    
    def get_closed_trades(self) -> List[Trade]:
        """Get only closed trades."""
        return self.trade_manager.get_closed_trades()

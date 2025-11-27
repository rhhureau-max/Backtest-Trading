"""
Trade manager module for handling entry, exit, stop loss, and take profit calculations.
"""
import pandas as pd
from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class TradeStatus(Enum):
    """Trade status enumeration."""
    PENDING = "pending"
    OPEN = "open"
    CLOSED_WIN = "closed_win"
    CLOSED_LOSS = "closed_loss"
    CANCELLED = "cancelled"


class TradeDirection(Enum):
    """Trade direction enumeration."""
    LONG = "long"
    SHORT = "short"


@dataclass
class Trade:
    """Represents a single trade."""
    id: int
    entry_time: datetime
    entry_price: float
    direction: TradeDirection
    stop_loss: float
    take_profit: float
    session: str  # "Session 1" or "Session 2"
    htf_context: str  # "fvg" or "liquidity_sweep"
    
    # Exit details (filled when trade closes)
    exit_time: Optional[datetime] = None
    exit_price: Optional[float] = None
    status: TradeStatus = TradeStatus.OPEN
    
    # Additional metadata
    year: int = 0
    pnl: float = 0.0
    risk: float = 0.0
    reward: float = 0.0
    actual_rr: float = 0.0
    
    def __post_init__(self):
        """Calculate initial risk."""
        if self.direction == TradeDirection.LONG:
            self.risk = abs(self.entry_price - self.stop_loss)
            self.reward = abs(self.take_profit - self.entry_price)
        else:
            self.risk = abs(self.stop_loss - self.entry_price)
            self.reward = abs(self.entry_price - self.take_profit)
        
        self.year = self.entry_time.year
    
    def close(self, exit_time: datetime, exit_price: float):
        """Close the trade at given price."""
        self.exit_time = exit_time
        self.exit_price = exit_price
        
        if self.direction == TradeDirection.LONG:
            self.pnl = exit_price - self.entry_price
            if self.pnl > 0:
                self.status = TradeStatus.CLOSED_WIN
            else:
                self.status = TradeStatus.CLOSED_LOSS
        else:
            self.pnl = self.entry_price - exit_price
            if self.pnl > 0:
                self.status = TradeStatus.CLOSED_WIN
            else:
                self.status = TradeStatus.CLOSED_LOSS
        
        # Calculate actual R:R
        if self.risk > 0:
            self.actual_rr = abs(self.pnl) / self.risk
            if self.pnl < 0:
                self.actual_rr = -self.actual_rr
    
    def check_exit(self, candle: pd.Series) -> Optional[float]:
        """
        Check if trade should exit based on candle OHLC.
        
        Returns exit price if trade should close, None otherwise.
        """
        if self.status != TradeStatus.OPEN:
            return None
        
        high = candle['High']
        low = candle['Low']
        
        if self.direction == TradeDirection.LONG:
            # Check stop loss first (assume worst case)
            if low <= self.stop_loss:
                return self.stop_loss
            # Check take profit
            if high >= self.take_profit:
                return self.take_profit
        else:  # SHORT
            # Check stop loss first
            if high >= self.stop_loss:
                return self.stop_loss
            # Check take profit
            if low <= self.take_profit:
                return self.take_profit
        
        return None
    
    def to_dict(self) -> dict:
        """Convert trade to dictionary."""
        return {
            'id': self.id,
            'entry_time': self.entry_time,
            'entry_price': self.entry_price,
            'direction': self.direction.value,
            'stop_loss': self.stop_loss,
            'take_profit': self.take_profit,
            'exit_time': self.exit_time,
            'exit_price': self.exit_price,
            'status': self.status.value,
            'session': self.session,
            'htf_context': self.htf_context,
            'year': self.year,
            'pnl': self.pnl,
            'risk': self.risk,
            'reward': self.reward,
            'actual_rr': self.actual_rr,
        }


@dataclass
class TradeManager:
    """Manages trade execution and tracking."""
    risk_reward_ratio: float = 2.0
    stop_loss_buffer_pct: float = 0.0001
    
    trades: List[Trade] = field(default_factory=list)
    current_trade: Optional[Trade] = None
    trade_counter: int = 0
    
    def has_open_trade(self) -> bool:
        """Check if there's currently an open trade."""
        return self.current_trade is not None and self.current_trade.status == TradeStatus.OPEN
    
    def open_trade(
        self,
        entry_time: datetime,
        entry_price: float,
        direction: TradeDirection,
        swing_price: float,  # Last swing high/low for stop loss placement
        session: str,
        htf_context: str
    ) -> Optional[Trade]:
        """
        Open a new trade.
        
        Args:
            entry_time: Entry timestamp
            entry_price: Entry price
            direction: Trade direction (LONG or SHORT)
            swing_price: Price level for stop loss placement
            session: Trading session name
            htf_context: HTF context type
            
        Returns:
            Trade object if opened successfully, None otherwise
        """
        if self.has_open_trade():
            logger.warning(f"Cannot open trade - already have open trade {self.current_trade.id}")
            return None
        
        self.trade_counter += 1
        
        # Calculate stop loss with buffer
        buffer = entry_price * self.stop_loss_buffer_pct
        
        if direction == TradeDirection.LONG:
            stop_loss = swing_price - buffer
            risk = entry_price - stop_loss
            take_profit = entry_price + (risk * self.risk_reward_ratio)
        else:
            stop_loss = swing_price + buffer
            risk = stop_loss - entry_price
            take_profit = entry_price - (risk * self.risk_reward_ratio)
        
        trade = Trade(
            id=self.trade_counter,
            entry_time=entry_time,
            entry_price=entry_price,
            direction=direction,
            stop_loss=stop_loss,
            take_profit=take_profit,
            session=session,
            htf_context=htf_context,
        )
        
        self.current_trade = trade
        self.trades.append(trade)
        
        logger.info(
            f"Opened trade #{trade.id}: {direction.value} at {entry_price:.2f}, "
            f"SL: {stop_loss:.2f}, TP: {take_profit:.2f}"
        )
        
        return trade
    
    def update_trade(self, candle_time: datetime, candle: pd.Series) -> Optional[Trade]:
        """
        Update current trade with new candle data.
        
        Args:
            candle_time: Candle timestamp
            candle: OHLC candle data
            
        Returns:
            Trade if it was closed, None otherwise
        """
        if not self.has_open_trade():
            return None
        
        exit_price = self.current_trade.check_exit(candle)
        
        if exit_price is not None:
            self.current_trade.close(candle_time, exit_price)
            closed_trade = self.current_trade
            self.current_trade = None
            
            logger.info(
                f"Closed trade #{closed_trade.id}: {closed_trade.status.value} at {exit_price:.2f}, "
                f"PnL: {closed_trade.pnl:.2f}, RR: {closed_trade.actual_rr:.2f}"
            )
            
            return closed_trade
        
        return None
    
    def get_all_trades(self) -> List[Trade]:
        """Get all trades (open and closed)."""
        return self.trades
    
    def get_closed_trades(self) -> List[Trade]:
        """Get only closed trades."""
        return [t for t in self.trades if t.status in [TradeStatus.CLOSED_WIN, TradeStatus.CLOSED_LOSS]]
    
    def get_trades_dataframe(self) -> pd.DataFrame:
        """Convert all trades to a DataFrame."""
        if not self.trades:
            return pd.DataFrame()
        return pd.DataFrame([t.to_dict() for t in self.trades])


def calculate_stop_loss(
    entry_price: float,
    direction: TradeDirection,
    m5_data: pd.DataFrame,
    entry_time: datetime,
    lookback_candles: int = 10,
    buffer_pct: float = 0.0001
) -> float:
    """
    Calculate stop loss based on recent swing high/low.
    
    Args:
        entry_price: Entry price
        direction: Trade direction
        m5_data: 5-minute OHLC data
        entry_time: Entry timestamp
        lookback_candles: Number of candles to look back
        buffer_pct: Buffer percentage to add to stop loss
        
    Returns:
        Stop loss price
    """
    # Get recent candles before entry
    recent = m5_data[m5_data.index < entry_time].tail(lookback_candles)
    
    if len(recent) == 0:
        # Fallback: use percentage-based stop
        if direction == TradeDirection.LONG:
            return entry_price * 0.995  # 0.5% below
        else:
            return entry_price * 1.005  # 0.5% above
    
    buffer = entry_price * buffer_pct
    
    if direction == TradeDirection.LONG:
        # Stop below recent low
        stop_loss = recent['Low'].min() - buffer
    else:
        # Stop above recent high
        stop_loss = recent['High'].max() + buffer
    
    return stop_loss


def find_swing_for_stop_loss(
    m5_data: pd.DataFrame,
    entry_time: datetime,
    direction: TradeDirection,
    fvg_time: datetime,
    lookback_candles: int = 15
) -> float:
    """
    Find the swing high/low created during FVG rejection for stop loss placement.
    
    Args:
        m5_data: 5-minute OHLC data
        entry_time: Entry timestamp
        direction: Trade direction
        fvg_time: Time when the FVG was created
        lookback_candles: Number of candles to look back from entry
        
    Returns:
        Swing price for stop loss placement
    """
    # Get candles between FVG creation and entry
    window = m5_data[(m5_data.index >= fvg_time) & (m5_data.index <= entry_time)]
    
    if len(window) == 0:
        # Fallback to recent candles
        window = m5_data[m5_data.index <= entry_time].tail(lookback_candles)
    
    if len(window) == 0:
        # Fallback: use entry price with a fixed percentage buffer
        fallback_buffer = 0.002  # 0.2% from entry price
        if direction == TradeDirection.LONG:
            return entry_price * (1 - fallback_buffer)
        else:
            return entry_price * (1 + fallback_buffer)
    
    if direction == TradeDirection.LONG:
        # For long, stop below the low created during rejection
        return window['Low'].min()
    else:
        # For short, stop above the high created during rejection
        return window['High'].max()

"""
Base strategy class for all trading strategies.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, List, Dict
import pandas as pd


@dataclass
class Trade:
    """Represents a single trade."""
    entry_time: pd.Timestamp
    entry_price: float
    direction: str  # 'long' or 'short'
    stop_loss: float
    take_profit_1: Optional[float] = None
    take_profit_2: Optional[float] = None
    tp1_percentage: float = 0.5  # Percentage of position to close at TP1
    tp2_percentage: float = 0.5  # Percentage of position to close at TP2
    
    # Trade results
    exit_time: Optional[pd.Timestamp] = None
    exit_price: Optional[float] = None
    pnl: float = 0.0
    status: str = 'open'  # 'open', 'closed', 'stopped'
    
    # Partial exits
    tp1_hit: bool = False
    tp1_exit_time: Optional[pd.Timestamp] = None
    tp1_exit_price: Optional[float] = None
    tp1_pnl: float = 0.0
    
    tp2_hit: bool = False
    tp2_exit_time: Optional[pd.Timestamp] = None
    tp2_exit_price: Optional[float] = None
    tp2_pnl: float = 0.0
    
    # Tracking
    breakeven_moved: bool = False
    trailing_stop: Optional[float] = None
    
    def __repr__(self):
        return (f"Trade(entry={self.entry_time}, direction={self.direction}, "
                f"entry_price={self.entry_price:.2f}, pnl={self.pnl:.2f}, status={self.status})")


class BaseStrategy(ABC):
    """
    Abstract base class for all trading strategies.
    """
    
    def __init__(self, name: str, spread_points: float = 1.5):
        self.name = name
        self.spread_points = spread_points
        self.trades: List[Trade] = []
    
    @abstractmethod
    def generate_signals(self, data: Dict[str, pd.DataFrame], date: pd.Timestamp) -> Optional[Trade]:
        """
        Generate trading signal for a specific date.
        
        Args:
            data: Dictionary of DataFrames for different timeframes
            date: Trading date
        
        Returns:
            Trade object if signal generated, None otherwise
        """
        pass
    
    @abstractmethod
    def update_trade(self, trade: Trade, data: Dict[str, pd.DataFrame], current_time: pd.Timestamp) -> Trade:
        """
        Update an open trade (check for exits, trailing stops, etc.).
        
        Args:
            trade: Current open trade
            data: Dictionary of DataFrames for different timeframes
            current_time: Current timestamp
        
        Returns:
            Updated trade object
        """
        pass
    
    def calculate_pnl(self, entry_price: float, exit_price: float, direction: str, position_size: float = 1.0) -> float:
        """
        Calculate PnL for a trade including spread.
        
        Args:
            entry_price: Entry price
            exit_price: Exit price
            direction: 'long' or 'short'
            position_size: Position size (for partial exits)
        
        Returns:
            PnL in points
        """
        if direction == 'long':
            # Long: buy at ask (entry + spread), sell at bid (exit)
            pnl = (exit_price - (entry_price + self.spread_points)) * position_size
        else:  # short
            # Short: sell at bid (entry), buy at ask (exit + spread)
            pnl = ((entry_price - self.spread_points) - exit_price) * position_size
        
        return pnl
    
    def check_stop_loss(self, trade: Trade, current_candle: pd.Series) -> bool:
        """
        Check if stop loss is hit.
        
        Args:
            trade: Current trade
            current_candle: Current candle data
        
        Returns:
            True if stop loss is hit
        """
        if trade.direction == 'long':
            return current_candle['Low'] <= trade.stop_loss
        else:  # short
            return current_candle['High'] >= trade.stop_loss
    
    def check_take_profit(self, trade: Trade, current_candle: pd.Series, tp_level: float) -> bool:
        """
        Check if take profit level is hit.
        
        Args:
            trade: Current trade
            current_candle: Current candle data
            tp_level: Take profit level
        
        Returns:
            True if take profit is hit
        """
        if trade.direction == 'long':
            return current_candle['High'] >= tp_level
        else:  # short
            return current_candle['Low'] <= tp_level
    
    def get_all_trades(self) -> List[Trade]:
        """Get all trades."""
        return self.trades
    
    def get_closed_trades(self) -> List[Trade]:
        """Get only closed trades."""
        return [t for t in self.trades if t.status == 'closed' or t.status == 'stopped']
    
    def reset(self):
        """Reset strategy state."""
        self.trades = []

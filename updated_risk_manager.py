"""
Updated Risk Management Module
25-point SL, TPs at 20/40 points + runner until session end or signal
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Optional
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class TradePosition:
    """Represents a single trade position (1/3 of full position)"""
    entry_time: pd.Timestamp
    entry_price: float
    direction: str  # 'LONG' or 'SHORT'
    stop_loss: float
    take_profit: Optional[float]  # None for runner
    position_size: float  # Fraction of full position (1/3 = 0.333)
    tp_level: int  # 1, 2, or 3 (runner)
    
    exit_time: Optional[pd.Timestamp] = None
    exit_price: Optional[float] = None
    exit_reason: Optional[str] = None  # 'TP', 'SL', 'EOD', 'SIGNAL'
    pnl: Optional[float] = None
    
    def is_closed(self) -> bool:
        """Check if position is closed"""
        return self.exit_time is not None
    
    def calculate_pnl(self) -> float:
        """Calculate PnL in points"""
        if not self.is_closed():
            return 0.0
        
        if self.direction == 'LONG':
            return self.exit_price - self.entry_price
        else:  # SHORT
            return self.entry_price - self.exit_price
    
    def __repr__(self):
        status = "CLOSED" if self.is_closed() else "OPEN"
        tp_str = f"TP{self.tp_level}" if self.tp_level < 3 else "RUNNER"
        return f"Position({self.direction}, {tp_str}, {status})"


@dataclass
class Trade:
    """Represents a complete trade with 3 positions"""
    trade_id: int
    entry_time: pd.Timestamp
    direction: str
    entry_price: float
    positions: List[TradePosition] = field(default_factory=list)
    
    def is_fully_closed(self) -> bool:
        """Check if all positions are closed"""
        return all(pos.is_closed() for pos in self.positions)
    
    def get_total_pnl(self) -> float:
        """Get total PnL across all positions"""
        return sum(pos.calculate_pnl() for pos in self.positions if pos.is_closed())
    
    def get_open_positions(self) -> List[TradePosition]:
        """Get list of open positions"""
        return [pos for pos in self.positions if not pos.is_closed()]
    
    def __repr__(self):
        status = "CLOSED" if self.is_fully_closed() else "OPEN"
        return f"Trade #{self.trade_id} ({self.direction}, {status}, PnL: {self.get_total_pnl():.2f})"


class UpdatedRiskManager:
    """Manages risk with 25-point SL and updated TP structure"""
    
    def __init__(self, stop_loss_points: float = 25.0):
        """
        Args:
            stop_loss_points: Fixed stop loss in points (default: 25)
        """
        self.stop_loss_points = stop_loss_points
        self.tp1_points = 20.0
        self.tp2_points = 40.0
        # TP3 is a runner (no fixed target)
        
    def create_trade_positions(
        self,
        trade_id: int,
        entry_time: pd.Timestamp,
        entry_price: float,
        direction: str
    ) -> Trade:
        """
        Create a new trade with 3 positions
        
        Args:
            trade_id: Unique trade identifier
            entry_time: Entry timestamp
            entry_price: Entry price
            direction: 'LONG' or 'SHORT'
            
        Returns:
            Trade object with 3 positions
        """
        positions = []
        position_size = 1.0 / 3.0  # Each position is 1/3 of total
        
        if direction == 'LONG':
            stop_loss = entry_price - self.stop_loss_points
            tp1 = entry_price + self.tp1_points
            tp2 = entry_price + self.tp2_points
            tp3 = None  # Runner
            
        else:  # SHORT
            stop_loss = entry_price + self.stop_loss_points
            tp1 = entry_price - self.tp1_points
            tp2 = entry_price - self.tp2_points
            tp3 = None  # Runner
        
        # Create 3 positions
        positions.append(TradePosition(
            entry_time=entry_time,
            entry_price=entry_price,
            direction=direction,
            stop_loss=stop_loss,
            take_profit=tp1,
            position_size=position_size,
            tp_level=1
        ))
        
        positions.append(TradePosition(
            entry_time=entry_time,
            entry_price=entry_price,
            direction=direction,
            stop_loss=stop_loss,
            take_profit=tp2,
            position_size=position_size,
            tp_level=2
        ))
        
        positions.append(TradePosition(
            entry_time=entry_time,
            entry_price=entry_price,
            direction=direction,
            stop_loss=stop_loss,
            take_profit=tp3,  # None - runner
            position_size=position_size,
            tp_level=3
        ))
        
        return Trade(
            trade_id=trade_id,
            entry_time=entry_time,
            direction=direction,
            entry_price=entry_price,
            positions=positions
        )
    
    def update_position(
        self,
        position: TradePosition,
        current_candle: pd.Series,
        current_time: pd.Timestamp
    ) -> bool:
        """
        Update a position based on current price action
        
        Args:
            position: Position to update
            current_candle: Current OHLC candle
            current_time: Current timestamp
            
        Returns:
            True if position was closed, False otherwise
        """
        if position.is_closed():
            return False
        
        high = current_candle['High']
        low = current_candle['Low']
        close = current_candle['Close']
        
        if position.direction == 'LONG':
            # Check stop loss
            if low <= position.stop_loss:
                position.exit_time = current_time
                position.exit_price = position.stop_loss
                position.exit_reason = 'SL'
                position.pnl = position.calculate_pnl()
                return True
            
            # Check take profit (if not runner)
            if position.take_profit is not None and high >= position.take_profit:
                position.exit_time = current_time
                position.exit_price = position.take_profit
                position.exit_reason = 'TP'
                position.pnl = position.calculate_pnl()
                return True
        
        else:  # SHORT
            # Check stop loss
            if high >= position.stop_loss:
                position.exit_time = current_time
                position.exit_price = position.stop_loss
                position.exit_reason = 'SL'
                position.pnl = position.calculate_pnl()
                return True
            
            # Check take profit (if not runner)
            if position.take_profit is not None and low <= position.take_profit:
                position.exit_time = current_time
                position.exit_price = position.take_profit
                position.exit_reason = 'TP'
                position.pnl = position.calculate_pnl()
                return True
        
        return False
    
    def close_position_at_eod(
        self,
        position: TradePosition,
        exit_price: float,
        exit_time: pd.Timestamp
    ):
        """
        Close position at end of day
        
        Args:
            position: Position to close
            exit_price: Exit price
            exit_time: Exit timestamp
        """
        if not position.is_closed():
            position.exit_time = exit_time
            position.exit_price = exit_price
            position.exit_reason = 'EOD'
            position.pnl = position.calculate_pnl()


class TradeTracker:
    """Tracks all trades and provides reporting"""
    
    def __init__(self):
        self.trades: List[Trade] = []
        self.next_trade_id = 1
    
    def add_trade(self, trade: Trade):
        """Add a trade to tracking"""
        self.trades.append(trade)
    
    def get_next_trade_id(self) -> int:
        """Get next trade ID and increment"""
        trade_id = self.next_trade_id
        self.next_trade_id += 1
        return trade_id
    
    def get_all_trades(self) -> List[Trade]:
        """Get all trades"""
        return self.trades
    
    def get_open_trades(self) -> List[Trade]:
        """Get trades with open positions"""
        return [t for t in self.trades if not t.is_fully_closed()]
    
    def get_closed_trades(self) -> List[Trade]:
        """Get fully closed trades"""
        return [t for t in self.trades if t.is_fully_closed()]
    
    def get_total_pnl(self) -> float:
        """Get total PnL across all trades"""
        return sum(t.get_total_pnl() for t in self.trades)


if __name__ == "__main__":
    # Test the risk manager
    print("Testing Updated Risk Manager...")
    
    manager = UpdatedRiskManager(stop_loss_points=25.0)
    
    # Create a test trade
    trade = manager.create_trade_positions(
        trade_id=1,
        entry_time=pd.Timestamp('2024-01-17 08:35:00', tz='US/Central'),
        entry_price=17973.63,
        direction='SHORT'
    )
    
    print(f"\n{trade}")
    print(f"Positions: {len(trade.positions)}")
    for pos in trade.positions:
        print(f"  {pos}")
        print(f"    SL: {pos.stop_loss:.2f}, TP: {pos.take_profit if pos.take_profit else 'Runner'}")

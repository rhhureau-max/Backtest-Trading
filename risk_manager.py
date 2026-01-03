"""
Risk Management Module
Handles position sizing, stop losses, and take profits
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
    take_profit: float
    position_size: float  # Fraction of full position (1/3 = 0.333)
    tp_level: int  # 1, 2, or 3
    
    exit_time: Optional[pd.Timestamp] = None
    exit_price: Optional[float] = None
    exit_reason: Optional[str] = None  # 'TP', 'SL', 'EOD'
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
        return f"Position({self.direction}, TP{self.tp_level}, {status})"


@dataclass
class Trade:
    """Represents a complete trade with 3 positions"""
    trade_id: int
    entry_signal_time: pd.Timestamp
    direction: str
    entry_price: float
    
    positions: List[TradePosition] = field(default_factory=list)
    
    def add_position(self, position: TradePosition):
        """Add a position to this trade"""
        self.positions.append(position)
    
    def is_fully_closed(self) -> bool:
        """Check if all positions are closed"""
        return all(pos.is_closed() for pos in self.positions)
    
    def get_total_pnl(self) -> float:
        """Get total PnL across all positions"""
        return sum(pos.calculate_pnl() for pos in self.positions)
    
    def get_winning_positions(self) -> int:
        """Count positions that hit TP"""
        return sum(1 for pos in self.positions if pos.exit_reason == 'TP')
    
    def get_summary(self) -> Dict:
        """Get trade summary"""
        return {
            'trade_id': self.trade_id,
            'entry_time': self.entry_signal_time,
            'direction': self.direction,
            'entry_price': self.entry_price,
            'total_pnl': self.get_total_pnl(),
            'winning_positions': self.get_winning_positions(),
            'is_winner': self.get_total_pnl() > 0,
            'fully_closed': self.is_fully_closed()
        }


class RiskManager:
    """Manages trade risk with fixed stop loss and multiple take profits"""
    
    def __init__(self, stop_loss_points: float = 20.0):
        """
        Args:
            stop_loss_points: Fixed stop loss in points (default: 20)
        """
        self.stop_loss_points = stop_loss_points
        self.tp_levels = [20, 30, 40]  # TP1, TP2, TP3 in points
        self.position_sizes = [1/3, 1/3, 1/3]  # Equal split
    
    def create_trade_positions(
        self,
        trade_id: int,
        entry_time: pd.Timestamp,
        entry_price: float,
        direction: str
    ) -> Trade:
        """
        Create a trade with 3 positions (for 3 TPs)
        
        Args:
            trade_id: Unique trade identifier
            entry_time: Entry timestamp
            entry_price: Entry price
            direction: 'LONG' or 'SHORT'
            
        Returns:
            Trade object with 3 positions
        """
        trade = Trade(
            trade_id=trade_id,
            entry_signal_time=entry_time,
            direction=direction,
            entry_price=entry_price
        )
        
        if direction == 'LONG':
            stop_loss = entry_price - self.stop_loss_points
            
            for i, (tp_points, size) in enumerate(zip(self.tp_levels, self.position_sizes)):
                position = TradePosition(
                    entry_time=entry_time,
                    entry_price=entry_price,
                    direction=direction,
                    stop_loss=stop_loss,
                    take_profit=entry_price + tp_points,
                    position_size=size,
                    tp_level=i + 1
                )
                trade.add_position(position)
        
        else:  # SHORT
            stop_loss = entry_price + self.stop_loss_points
            
            for i, (tp_points, size) in enumerate(zip(self.tp_levels, self.position_sizes)):
                position = TradePosition(
                    entry_time=entry_time,
                    entry_price=entry_price,
                    direction=direction,
                    stop_loss=stop_loss,
                    take_profit=entry_price - tp_points,
                    position_size=size,
                    tp_level=i + 1
                )
                trade.add_position(position)
        
        return trade
    
    def update_position(
        self,
        position: TradePosition,
        current_time: pd.Timestamp,
        current_high: float,
        current_low: float,
        current_close: float
    ) -> bool:
        """
        Update position status based on current price action
        
        Args:
            position: Position to update
            current_time: Current bar timestamp
            current_high: Current bar high
            current_low: Current bar low
            current_close: Current bar close
            
        Returns:
            True if position was closed
        """
        if position.is_closed():
            return False
        
        if position.direction == 'LONG':
            # Check stop loss hit
            if current_low <= position.stop_loss:
                position.exit_time = current_time
                position.exit_price = position.stop_loss
                position.exit_reason = 'SL'
                position.pnl = position.calculate_pnl()
                return True
            
            # Check take profit hit
            if current_high >= position.take_profit:
                position.exit_time = current_time
                position.exit_price = position.take_profit
                position.exit_reason = 'TP'
                position.pnl = position.calculate_pnl()
                return True
        
        else:  # SHORT
            # Check stop loss hit
            if current_high >= position.stop_loss:
                position.exit_time = current_time
                position.exit_price = position.stop_loss
                position.exit_reason = 'SL'
                position.pnl = position.calculate_pnl()
                return True
            
            # Check take profit hit
            if current_low <= position.take_profit:
                position.exit_time = current_time
                position.exit_price = position.take_profit
                position.exit_reason = 'TP'
                position.pnl = position.calculate_pnl()
                return True
        
        return False
    
    def close_position_eod(
        self,
        position: TradePosition,
        exit_time: pd.Timestamp,
        exit_price: float
    ):
        """
        Force close position at end of day
        
        Args:
            position: Position to close
            exit_time: Exit timestamp
            exit_price: Exit price
        """
        if not position.is_closed():
            position.exit_time = exit_time
            position.exit_price = exit_price
            position.exit_reason = 'EOD'
            position.pnl = position.calculate_pnl()


class TradeTracker:
    """Tracks all trades and provides performance metrics"""
    
    def __init__(self):
        self.trades: List[Trade] = []
        self.next_trade_id = 1
    
    def add_trade(self, trade: Trade):
        """Add a trade to tracking"""
        self.trades.append(trade)
        self.next_trade_id += 1
    
    def get_next_trade_id(self) -> int:
        """Get next available trade ID"""
        return self.next_trade_id
    
    def get_all_trades(self) -> List[Trade]:
        """Get all trades"""
        return self.trades
    
    def get_closed_trades(self) -> List[Trade]:
        """Get only fully closed trades"""
        return [t for t in self.trades if t.is_fully_closed()]
    
    def get_trade_summaries(self) -> List[Dict]:
        """Get summaries of all trades"""
        return [trade.get_summary() for trade in self.trades]
    
    def get_performance_metrics(self) -> Dict:
        """Calculate overall performance metrics"""
        closed_trades = self.get_closed_trades()
        
        if not closed_trades:
            return {
                'total_trades': 0,
                'winning_trades': 0,
                'losing_trades': 0,
                'win_rate': 0.0,
                'total_pnl': 0.0,
                'avg_win': 0.0,
                'avg_loss': 0.0,
                'profit_factor': 0.0
            }
        
        winning_trades = [t for t in closed_trades if t.get_total_pnl() > 0]
        losing_trades = [t for t in closed_trades if t.get_total_pnl() <= 0]
        
        total_wins = sum(t.get_total_pnl() for t in winning_trades)
        total_losses = abs(sum(t.get_total_pnl() for t in losing_trades))
        
        return {
            'total_trades': len(closed_trades),
            'winning_trades': len(winning_trades),
            'losing_trades': len(losing_trades),
            'win_rate': len(winning_trades) / len(closed_trades) * 100 if closed_trades else 0,
            'total_pnl': sum(t.get_total_pnl() for t in closed_trades),
            'avg_win': total_wins / len(winning_trades) if winning_trades else 0,
            'avg_loss': total_losses / len(losing_trades) if losing_trades else 0,
            'profit_factor': total_wins / total_losses if total_losses > 0 else float('inf')
        }


if __name__ == "__main__":
    # Test risk management
    import pandas as pd
    
    print("Testing Risk Management...")
    
    risk_mgr = RiskManager()
    tracker = TradeTracker()
    
    # Create a sample trade
    entry_time = pd.Timestamp('2024-03-15 09:00:00', tz='US/Central')
    trade = risk_mgr.create_trade_positions(
        trade_id=tracker.get_next_trade_id(),
        entry_time=entry_time,
        entry_price=18000.0,
        direction='LONG'
    )
    
    tracker.add_trade(trade)
    
    print(f"\nCreated trade: {trade.direction} @ {trade.entry_price}")
    for pos in trade.positions:
        print(f"  Position TP{pos.tp_level}: SL={pos.stop_loss:.2f}, TP={pos.take_profit:.2f}")
    
    # Simulate price movement hitting TP1
    risk_mgr.update_position(
        trade.positions[0],
        pd.Timestamp('2024-03-15 09:30:00', tz='US/Central'),
        18025.0, 17990.0, 18020.0
    )
    
    print(f"\nAfter TP1 hit:")
    print(f"  Position 1: {trade.positions[0].exit_reason}, PnL: {trade.positions[0].pnl:.2f}")
    
    metrics = tracker.get_performance_metrics()
    print(f"\nPerformance: {metrics}")

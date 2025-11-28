"""
Trade Manager Module

This module handles trade management including:
- Stop-Loss calculation
- Take Profit calculation (multiple RR ratios)
- Position tracking
- Trade result recording
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


class TradeStatus(Enum):
    """Trade status enumeration."""
    OPEN = "open"
    TP1_HIT = "tp1_hit"
    TP2_HIT = "tp2_hit"
    TP3_HIT = "tp3_hit"
    SL_HIT = "sl_hit"
    CLOSED = "closed"


@dataclass
class Trade:
    """Represents a single trade."""
    entry_datetime: pd.Timestamp
    signal: str  # 'BUY' or 'SELL'
    entry_price: float
    stop_loss: float
    take_profits: List[float]
    risk_amount: float
    status: TradeStatus = TradeStatus.OPEN
    exit_datetime: Optional[pd.Timestamp] = None
    exit_price: Optional[float] = None
    pnl: float = 0.0
    rr_achieved: float = 0.0
    tp_levels_hit: List[bool] = field(default_factory=list)
    
    def __post_init__(self):
        if not self.tp_levels_hit:
            self.tp_levels_hit = [False] * len(self.take_profits)


def calculate_stop_loss(entry: Dict, buffer_pct: float = 0.02) -> float:
    """
    Calculate stop-loss level based on confirmation candle.
    
    For BUY: SL is placed below the confirmation candle's low or FVG bottom
    For SELL: SL is placed above the confirmation candle's high or FVG top
    
    Args:
        entry: Entry signal dictionary from detectors
        buffer_pct: Buffer percentage to add to SL
        
    Returns:
        Stop-loss price level
    """
    signal = entry['signal']
    candle = entry['confirmation_candle']
    fvg = entry['fvg']
    
    if signal == 'BUY':
        # For BUY, SL is below the candle low or FVG bottom
        sl_base = min(candle['Low'], fvg['bottom'])
        stop_loss = sl_base * (1 - buffer_pct / 100)
    else:  # SELL
        # For SELL, SL is above the candle high or FVG top
        sl_base = max(candle['High'], fvg['top'])
        stop_loss = sl_base * (1 + buffer_pct / 100)
    
    return stop_loss


def calculate_take_profits(entry_price: float, stop_loss: float, 
                           signal: str, rr_ratios: List[float] = None) -> List[float]:
    """
    Calculate take profit levels based on Risk/Reward ratios.
    
    Args:
        entry_price: Entry price
        stop_loss: Stop-loss price
        signal: Trade direction ('BUY' or 'SELL')
        rr_ratios: List of RR ratios (default: [1.0, 1.5, 2.0])
        
    Returns:
        List of take profit price levels
    """
    if rr_ratios is None:
        rr_ratios = [1.0, 1.5, 2.0]
    
    risk = abs(entry_price - stop_loss)
    take_profits = []
    
    for rr in rr_ratios:
        if signal == 'BUY':
            tp = entry_price + (risk * rr)
        else:  # SELL
            tp = entry_price - (risk * rr)
        take_profits.append(tp)
    
    return take_profits


class TradeManager:
    """Manages trades and tracks positions."""
    
    def __init__(self, config: Dict):
        """
        Initialize the trade manager.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.risk_config = config.get('risk_management', {})
        self.rr_ratios = self.risk_config.get('risk_reward_ratios', [1.0, 1.5, 2.0])
        self.sl_buffer = self.risk_config.get('stop_loss_buffer_pct', 0.02)
        self.max_trades_per_day = self.risk_config.get('max_trades_per_day', 3)
        
        self.trades: List[Trade] = []
        self.open_trades: List[Trade] = []
        self.trades_today: Dict[str, int] = {}  # Date -> count
    
    def open_trade(self, entry: Dict) -> Optional[Trade]:
        """
        Open a new trade based on entry signal.
        
        Args:
            entry: Entry signal dictionary
            
        Returns:
            Trade object if trade was opened, None otherwise
        """
        entry_datetime = entry['datetime']
        date_str = str(entry_datetime.date())
        
        # Check max trades per day
        self.trades_today.setdefault(date_str, 0)
        if self.trades_today[date_str] >= self.max_trades_per_day:
            return None
        
        # Calculate SL and TPs
        entry_price = entry['entry_price']
        stop_loss = calculate_stop_loss(entry, self.sl_buffer)
        take_profits = calculate_take_profits(
            entry_price, stop_loss, 
            entry['signal'], self.rr_ratios
        )
        
        # Calculate risk amount
        risk_amount = abs(entry_price - stop_loss)
        
        # Create trade
        trade = Trade(
            entry_datetime=entry_datetime,
            signal=entry['signal'],
            entry_price=entry_price,
            stop_loss=stop_loss,
            take_profits=take_profits,
            risk_amount=risk_amount
        )
        
        self.trades.append(trade)
        self.open_trades.append(trade)
        self.trades_today[date_str] += 1
        
        return trade
    
    def update_trade(self, trade: Trade, candle: pd.Series) -> bool:
        """
        Update trade status based on current candle.
        
        Args:
            trade: Trade to update
            candle: Current price candle
            
        Returns:
            True if trade was closed, False otherwise
        """
        if trade.status != TradeStatus.OPEN:
            return False
        
        high = candle['High']
        low = candle['Low']
        
        # Check for stop-loss hit
        if trade.signal == 'BUY':
            if low <= trade.stop_loss:
                trade.status = TradeStatus.SL_HIT
                trade.exit_price = trade.stop_loss
                trade.exit_datetime = candle.name
                trade.pnl = trade.stop_loss - trade.entry_price
                trade.rr_achieved = -1.0
                self._close_trade(trade)
                return True
        else:  # SELL
            if high >= trade.stop_loss:
                trade.status = TradeStatus.SL_HIT
                trade.exit_price = trade.stop_loss
                trade.exit_datetime = candle.name
                trade.pnl = trade.entry_price - trade.stop_loss
                trade.rr_achieved = -1.0
                self._close_trade(trade)
                return True
        
        # Check for take profit hits
        for i, tp in enumerate(trade.take_profits):
            if trade.tp_levels_hit[i]:
                continue
            
            if trade.signal == 'BUY':
                if high >= tp:
                    trade.tp_levels_hit[i] = True
                    # Close on highest TP hit
                    if i == len(trade.take_profits) - 1:
                        trade.status = TradeStatus.TP3_HIT
                        trade.exit_price = tp
                        trade.exit_datetime = candle.name
                        trade.pnl = tp - trade.entry_price
                        trade.rr_achieved = self.rr_ratios[i]
                        self._close_trade(trade)
                        return True
            else:  # SELL
                if low <= tp:
                    trade.tp_levels_hit[i] = True
                    if i == len(trade.take_profits) - 1:
                        trade.status = TradeStatus.TP3_HIT
                        trade.exit_price = tp
                        trade.exit_datetime = candle.name
                        trade.pnl = trade.entry_price - tp
                        trade.rr_achieved = self.rr_ratios[i]
                        self._close_trade(trade)
                        return True
        
        # Check if lower TPs were hit but not the highest
        if any(trade.tp_levels_hit):
            # Find highest TP hit
            for i in range(len(trade.tp_levels_hit) - 1, -1, -1):
                if trade.tp_levels_hit[i]:
                    if i == 0:
                        trade.status = TradeStatus.TP1_HIT
                    elif i == 1:
                        trade.status = TradeStatus.TP2_HIT
                    trade.exit_price = trade.take_profits[i]
                    trade.exit_datetime = candle.name
                    if trade.signal == 'BUY':
                        trade.pnl = trade.take_profits[i] - trade.entry_price
                    else:
                        trade.pnl = trade.entry_price - trade.take_profits[i]
                    trade.rr_achieved = self.rr_ratios[i]
                    self._close_trade(trade)
                    return True
        
        return False
    
    def _close_trade(self, trade: Trade):
        """Remove trade from open trades list."""
        if trade in self.open_trades:
            self.open_trades.remove(trade)
    
    def process_candle(self, candle: pd.Series):
        """
        Process a price candle and update all open trades.
        
        Args:
            candle: Price candle (OHLC)
        """
        trades_to_process = self.open_trades.copy()
        for trade in trades_to_process:
            self.update_trade(trade, candle)
    
    def get_results(self) -> Dict:
        """
        Get trading results summary.
        
        Returns:
            Dictionary with trading statistics
        """
        if not self.trades:
            return {
                'total_trades': 0,
                'winning_trades': 0,
                'losing_trades': 0,
                'win_rate': 0.0,
                'profit_factor': 0.0
            }
        
        closed_trades = [t for t in self.trades if t.status != TradeStatus.OPEN]
        
        winning_trades = [t for t in closed_trades 
                         if t.status in [TradeStatus.TP1_HIT, TradeStatus.TP2_HIT, TradeStatus.TP3_HIT]]
        losing_trades = [t for t in closed_trades if t.status == TradeStatus.SL_HIT]
        
        total_wins = sum(t.pnl for t in winning_trades)
        total_losses = abs(sum(t.pnl for t in losing_trades))
        
        results = {
            'total_trades': len(closed_trades),
            'winning_trades': len(winning_trades),
            'losing_trades': len(losing_trades),
            'win_rate': len(winning_trades) / len(closed_trades) * 100 if closed_trades else 0.0,
            'profit_factor': total_wins / total_losses if total_losses > 0 else float('inf') if total_wins > 0 else 0.0,
            'total_pnl': sum(t.pnl for t in closed_trades),
            'avg_win': total_wins / len(winning_trades) if winning_trades else 0.0,
            'avg_loss': total_losses / len(losing_trades) if losing_trades else 0.0,
            'tp1_count': len([t for t in closed_trades if t.status == TradeStatus.TP1_HIT]),
            'tp2_count': len([t for t in closed_trades if t.status == TradeStatus.TP2_HIT]),
            'tp3_count': len([t for t in closed_trades if t.status == TradeStatus.TP3_HIT]),
            'sl_count': len(losing_trades)
        }
        
        # RR distribution
        for i, rr in enumerate(self.rr_ratios):
            tp_status = [TradeStatus.TP1_HIT, TradeStatus.TP2_HIT, TradeStatus.TP3_HIT][i] if i < 3 else None
            if tp_status:
                tp_trades = [t for t in closed_trades if t.status == tp_status]
                results[f'rr_{rr}_count'] = len(tp_trades)
                results[f'rr_{rr}_rate'] = len(tp_trades) / len(closed_trades) * 100 if closed_trades else 0.0
        
        return results
    
    def get_results_by_year(self) -> Dict[int, Dict]:
        """
        Get trading results grouped by year.
        
        Returns:
            Dictionary with year -> statistics mapping
        """
        results_by_year = {}
        
        for trade in self.trades:
            if trade.status == TradeStatus.OPEN:
                continue
            
            year = trade.entry_datetime.year
            if year not in results_by_year:
                results_by_year[year] = {
                    'trades': [],
                    'winning_trades': 0,
                    'losing_trades': 0,
                    'tp1_count': 0,
                    'tp2_count': 0,
                    'tp3_count': 0,
                    'sl_count': 0
                }
            
            results_by_year[year]['trades'].append(trade)
            
            if trade.status in [TradeStatus.TP1_HIT, TradeStatus.TP2_HIT, TradeStatus.TP3_HIT]:
                results_by_year[year]['winning_trades'] += 1
                if trade.status == TradeStatus.TP1_HIT:
                    results_by_year[year]['tp1_count'] += 1
                elif trade.status == TradeStatus.TP2_HIT:
                    results_by_year[year]['tp2_count'] += 1
                else:
                    results_by_year[year]['tp3_count'] += 1
            elif trade.status == TradeStatus.SL_HIT:
                results_by_year[year]['losing_trades'] += 1
                results_by_year[year]['sl_count'] += 1
        
        # Calculate rates
        for year, data in results_by_year.items():
            total = len(data['trades'])
            data['total_trades'] = total
            data['win_rate'] = data['winning_trades'] / total * 100 if total > 0 else 0.0
        
        return results_by_year
    
    def get_results_by_type(self) -> Dict[str, Dict]:
        """
        Get trading results grouped by trade type (Long/Short).
        
        Returns:
            Dictionary with type -> statistics mapping
        """
        results_by_type = {
            'LONG': {'trades': [], 'wins': 0, 'losses': 0},
            'SHORT': {'trades': [], 'wins': 0, 'losses': 0}
        }
        
        for trade in self.trades:
            if trade.status == TradeStatus.OPEN:
                continue
            
            trade_type = 'LONG' if trade.signal == 'BUY' else 'SHORT'
            results_by_type[trade_type]['trades'].append(trade)
            
            if trade.status in [TradeStatus.TP1_HIT, TradeStatus.TP2_HIT, TradeStatus.TP3_HIT]:
                results_by_type[trade_type]['wins'] += 1
            else:
                results_by_type[trade_type]['losses'] += 1
        
        for trade_type, data in results_by_type.items():
            total = len(data['trades'])
            data['total_trades'] = total
            data['win_rate'] = data['wins'] / total * 100 if total > 0 else 0.0
        
        return results_by_type
    
    def export_trades_to_df(self) -> pd.DataFrame:
        """
        Export all trades to a DataFrame.
        
        Returns:
            DataFrame with all trade details
        """
        trades_data = []
        
        for trade in self.trades:
            trades_data.append({
                'entry_datetime': trade.entry_datetime,
                'exit_datetime': trade.exit_datetime,
                'signal': trade.signal,
                'entry_price': trade.entry_price,
                'stop_loss': trade.stop_loss,
                'tp1': trade.take_profits[0] if len(trade.take_profits) > 0 else None,
                'tp2': trade.take_profits[1] if len(trade.take_profits) > 1 else None,
                'tp3': trade.take_profits[2] if len(trade.take_profits) > 2 else None,
                'exit_price': trade.exit_price,
                'status': trade.status.value,
                'pnl': trade.pnl,
                'rr_achieved': trade.rr_achieved,
                'year': trade.entry_datetime.year
            })
        
        return pd.DataFrame(trades_data)

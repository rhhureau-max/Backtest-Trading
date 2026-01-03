"""
Comparative Risk Management Strategies
Tests 3 different exit strategies on the same entry signals
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime


@dataclass
class RiskStrategy:
    """Base class for risk management strategy"""
    name: str
    description: str


@dataclass
class StrategyAResult:
    """Strategy A: Scalper Fixe"""
    entry_price: float
    stop_loss: float
    take_profit: float
    exit_price: float
    exit_reason: str
    pnl: float
    duration_minutes: int


@dataclass
class StrategyBResult:
    """Strategy B: ICT Liquidité Range"""
    entry_price: float
    stop_loss: float
    take_profit: float
    exit_price: float
    exit_reason: str
    pnl: float
    duration_minutes: int
    skipped: bool = False
    skip_reason: str = ""


@dataclass
class StrategyCResult:
    """Strategy C: Standard Deviation"""
    entry_price: float
    stop_loss: float
    take_profit_1: float
    take_profit_2: float
    exit_price_1: Optional[float]
    exit_price_2: Optional[float]
    exit_reason_1: str
    exit_reason_2: str
    pnl_1: float
    pnl_2: float
    total_pnl: float
    duration_minutes: int
    breakeven_activated: bool = False


class StrategyAManager:
    """Strategy A: Scalper Fixe - Mécanique"""
    
    def __init__(self):
        self.sl_points = 20.0
        self.tp_points = 25.0
    
    def calculate_levels(
        self, 
        entry_price: float, 
        direction: str,
        **kwargs
    ) -> Tuple[float, float]:
        """Calculate SL and TP levels"""
        if direction == 'LONG':
            sl = entry_price - self.sl_points
            tp = entry_price + self.tp_points
        else:  # SHORT
            sl = entry_price + self.sl_points
            tp = entry_price - self.tp_points
        
        return sl, tp
    
    def simulate_trade(
        self,
        entry_time: pd.Timestamp,
        entry_price: float,
        direction: str,
        price_data: pd.DataFrame,
        **kwargs
    ) -> StrategyAResult:
        """Simulate trade with Strategy A rules"""
        sl, tp = self.calculate_levels(entry_price, direction)
        
        # Get data after entry
        mask = price_data.index > entry_time
        future_data = price_data[mask]
        
        exit_price = None
        exit_reason = None
        exit_time = None
        
        for idx, row in future_data.iterrows():
            if direction == 'LONG':
                if row['Low'] <= sl:
                    exit_price = sl
                    exit_reason = 'SL'
                    exit_time = idx
                    break
                elif row['High'] >= tp:
                    exit_price = tp
                    exit_reason = 'TP'
                    exit_time = idx
                    break
            else:  # SHORT
                if row['High'] >= sl:
                    exit_price = sl
                    exit_reason = 'SL'
                    exit_time = idx
                    break
                elif row['Low'] <= tp:
                    exit_price = tp
                    exit_reason = 'TP'
                    exit_time = idx
                    break
        
        # If no exit, close at end of data
        if exit_price is None:
            exit_price = future_data.iloc[-1]['Close']
            exit_reason = 'EOD'
            exit_time = future_data.index[-1]
        
        # Calculate PnL
        if direction == 'LONG':
            pnl = exit_price - entry_price
        else:
            pnl = entry_price - exit_price
        
        duration = int((exit_time - entry_time).total_seconds() / 60)
        
        return StrategyAResult(
            entry_price=entry_price,
            stop_loss=sl,
            take_profit=tp,
            exit_price=exit_price,
            exit_reason=exit_reason,
            pnl=pnl,
            duration_minutes=duration
        )


class StrategyBManager:
    """Strategy B: ICT Liquidité Range - Structurelle"""
    
    def __init__(self):
        self.sl_buffer = 2.0  # Points beyond signal candle
        self.min_rr_distance = 10.0  # Minimum TP distance
    
    def calculate_levels(
        self,
        entry_price: float,
        direction: str,
        signal_candle: pd.Series,
        opening_range_high: float,
        opening_range_low: float
    ) -> Tuple[Optional[float], Optional[float], bool, str]:
        """Calculate SL and TP levels, return skip flag if R:R insufficient"""
        
        if direction == 'LONG':
            # SL 2 points below signal candle low
            sl = signal_candle['Low'] - self.sl_buffer
            # TP at opening range high
            tp = opening_range_high
        else:  # SHORT
            # SL 2 points above signal candle high
            sl = signal_candle['High'] + self.sl_buffer
            # TP at opening range low
            tp = opening_range_low
        
        # Check if TP distance is sufficient
        tp_distance = abs(tp - entry_price)
        if tp_distance < self.min_rr_distance:
            return None, None, True, f"R:R insufficient ({tp_distance:.1f} < {self.min_rr_distance})"
        
        return sl, tp, False, ""
    
    def simulate_trade(
        self,
        entry_time: pd.Timestamp,
        entry_price: float,
        direction: str,
        price_data: pd.DataFrame,
        signal_candle: pd.Series,
        opening_range_high: float,
        opening_range_low: float,
        **kwargs
    ) -> StrategyBResult:
        """Simulate trade with Strategy B rules"""
        
        sl, tp, skip, skip_reason = self.calculate_levels(
            entry_price, direction, signal_candle,
            opening_range_high, opening_range_low
        )
        
        if skip:
            return StrategyBResult(
                entry_price=entry_price,
                stop_loss=0,
                take_profit=0,
                exit_price=entry_price,
                exit_reason='SKIPPED',
                pnl=0,
                duration_minutes=0,
                skipped=True,
                skip_reason=skip_reason
            )
        
        # Get data after entry
        mask = price_data.index > entry_time
        future_data = price_data[mask]
        
        exit_price = None
        exit_reason = None
        exit_time = None
        
        for idx, row in future_data.iterrows():
            if direction == 'LONG':
                if row['Low'] <= sl:
                    exit_price = sl
                    exit_reason = 'SL'
                    exit_time = idx
                    break
                elif row['High'] >= tp:
                    exit_price = tp
                    exit_reason = 'TP'
                    exit_time = idx
                    break
            else:  # SHORT
                if row['High'] >= sl:
                    exit_price = sl
                    exit_reason = 'SL'
                    exit_time = idx
                    break
                elif row['Low'] <= tp:
                    exit_price = tp
                    exit_reason = 'TP'
                    exit_time = idx
                    break
        
        # If no exit, close at end of data
        if exit_price is None:
            exit_price = future_data.iloc[-1]['Close']
            exit_reason = 'EOD'
            exit_time = future_data.index[-1]
        
        # Calculate PnL
        if direction == 'LONG':
            pnl = exit_price - entry_price
        else:
            pnl = entry_price - exit_price
        
        duration = int((exit_time - entry_time).total_seconds() / 60)
        
        return StrategyBResult(
            entry_price=entry_price,
            stop_loss=sl,
            take_profit=tp,
            exit_price=exit_price,
            exit_reason=exit_reason,
            pnl=pnl,
            duration_minutes=duration,
            skipped=False
        )


class StrategyCManager:
    """Strategy C: Standard Deviation - Expansion Volatilité"""
    
    def __init__(self):
        self.sl_points = 20.0
    
    def calculate_levels(
        self,
        entry_price: float,
        direction: str,
        opening_range_high: float,
        opening_range_low: float
    ) -> Tuple[float, float, float]:
        """Calculate SL, TP1, and TP2 levels"""
        
        # Calculate H_Range
        h_range = opening_range_high - opening_range_low
        
        if direction == 'LONG':
            sl = entry_price - self.sl_points
            tp1 = entry_price + (2 * h_range)
            tp2 = entry_price + (4 * h_range)
        else:  # SHORT
            sl = entry_price + self.sl_points
            tp1 = entry_price - (2 * h_range)
            tp2 = entry_price - (4 * h_range)
        
        return sl, tp1, tp2
    
    def simulate_trade(
        self,
        entry_time: pd.Timestamp,
        entry_price: float,
        direction: str,
        price_data: pd.DataFrame,
        opening_range_high: float,
        opening_range_low: float,
        **kwargs
    ) -> StrategyCResult:
        """Simulate trade with Strategy C rules"""
        
        sl, tp1, tp2 = self.calculate_levels(
            entry_price, direction, opening_range_high, opening_range_low
        )
        
        # Get data after entry
        mask = price_data.index > entry_time
        future_data = price_data[mask]
        
        # Track state
        position_1_open = True
        position_2_open = True
        current_sl = sl
        breakeven_activated = False
        
        exit_price_1 = None
        exit_price_2 = None
        exit_reason_1 = None
        exit_reason_2 = None
        exit_time_1 = None
        exit_time_2 = None
        
        for idx, row in future_data.iterrows():
            if direction == 'LONG':
                # Check Position 1
                if position_1_open:
                    if row['Low'] <= current_sl:
                        exit_price_1 = current_sl
                        exit_reason_1 = 'SL'
                        exit_time_1 = idx
                        position_1_open = False
                    elif row['High'] >= tp1:
                        exit_price_1 = tp1
                        exit_reason_1 = 'TP1'
                        exit_time_1 = idx
                        position_1_open = False
                        # Move SL to breakeven for position 2
                        current_sl = entry_price
                        breakeven_activated = True
                
                # Check Position 2
                if position_2_open:
                    if row['Low'] <= current_sl:
                        exit_price_2 = current_sl
                        exit_reason_2 = 'BE' if breakeven_activated else 'SL'
                        exit_time_2 = idx
                        position_2_open = False
                    elif row['High'] >= tp2:
                        exit_price_2 = tp2
                        exit_reason_2 = 'TP2'
                        exit_time_2 = idx
                        position_2_open = False
            
            else:  # SHORT
                # Check Position 1
                if position_1_open:
                    if row['High'] >= current_sl:
                        exit_price_1 = current_sl
                        exit_reason_1 = 'SL'
                        exit_time_1 = idx
                        position_1_open = False
                    elif row['Low'] <= tp1:
                        exit_price_1 = tp1
                        exit_reason_1 = 'TP1'
                        exit_time_1 = idx
                        position_1_open = False
                        # Move SL to breakeven for position 2
                        current_sl = entry_price
                        breakeven_activated = True
                
                # Check Position 2
                if position_2_open:
                    if row['High'] >= current_sl:
                        exit_price_2 = current_sl
                        exit_reason_2 = 'BE' if breakeven_activated else 'SL'
                        exit_time_2 = idx
                        position_2_open = False
                    elif row['Low'] <= tp2:
                        exit_price_2 = tp2
                        exit_reason_2 = 'TP2'
                        exit_time_2 = idx
                        position_2_open = False
            
            # Both positions closed
            if not position_1_open and not position_2_open:
                break
        
        # Close any remaining open positions at end of data
        if position_1_open:
            exit_price_1 = future_data.iloc[-1]['Close']
            exit_reason_1 = 'EOD'
            exit_time_1 = future_data.index[-1]
        
        if position_2_open:
            exit_price_2 = future_data.iloc[-1]['Close']
            exit_reason_2 = 'EOD'
            exit_time_2 = future_data.index[-1]
        
        # Calculate PnL for each position (50% each)
        if direction == 'LONG':
            pnl_1 = (exit_price_1 - entry_price) * 0.5
            pnl_2 = (exit_price_2 - entry_price) * 0.5
        else:
            pnl_1 = (entry_price - exit_price_1) * 0.5
            pnl_2 = (entry_price - exit_price_2) * 0.5
        
        total_pnl = pnl_1 + pnl_2
        
        # Duration is until last position closes
        final_exit_time = max(exit_time_1, exit_time_2)
        duration = int((final_exit_time - entry_time).total_seconds() / 60)
        
        return StrategyCResult(
            entry_price=entry_price,
            stop_loss=sl,
            take_profit_1=tp1,
            take_profit_2=tp2,
            exit_price_1=exit_price_1,
            exit_price_2=exit_price_2,
            exit_reason_1=exit_reason_1,
            exit_reason_2=exit_reason_2,
            pnl_1=pnl_1,
            pnl_2=pnl_2,
            total_pnl=total_pnl,
            duration_minutes=duration,
            breakeven_activated=breakeven_activated
        )


if __name__ == "__main__":
    print("Risk Management Strategies Comparison Module")
    print("=" * 60)
    print("Strategy A: Scalper Fixe (SL 20pts, TP 25pts)")
    print("Strategy B: ICT Liquidité Range (SL candle±2pts, TP range)")
    print("Strategy C: Standard Deviation (SL 20pts, TP 2x/4x H_Range)")

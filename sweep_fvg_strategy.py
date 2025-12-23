#!/usr/bin/env python3
"""
Liquidity Sweep + FVG Multi-Timeframe Trading Strategy

Strategy Logic:
1. Detect liquidity sweep on 15m (swing high/low where only the wick breaks the level)
2. Find the FVG on 5m that was created BEFORE the sweep (during the trend move)
3. After the sweep, wait for price to reverse and BREAK the previous FVG
4. Entry on 1m when price closes beyond the FVG (breaking it)
5. Stop Loss: Above/below the FVG that was broken
6. Take Profits: 1RR, 1.5RR, 2RR, 2.5RR, 3RR, 3.5RR, 4RR, 4.5RR, 5RR

Author: Trading Analysis Tool
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import List, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime
import argparse
from enum import Enum


class TradeDirection(Enum):
    LONG = "long"
    SHORT = "short"


@dataclass
class FVG:
    """Fair Value Gap"""
    datetime: datetime
    index: int
    fvg_type: str  # 'bullish' or 'bearish'
    gap_high: float
    gap_low: float
    gap_size: float
    is_filled: bool = False
    filled_datetime: Optional[datetime] = None
    filled_index: Optional[int] = None
    
    def __str__(self):
        return f"[{self.datetime}] {self.fvg_type.upper()} FVG: {self.gap_low:.2f} - {self.gap_high:.2f}"


@dataclass
class LiquiditySweep:
    """Liquidity Sweep Event"""
    datetime: datetime
    index: int
    sweep_type: str  # 'bullish' or 'bearish'
    swing_level: float
    sweep_price: float
    close_price: float
    
    def __str__(self):
        return f"[{self.datetime}] {self.sweep_type.upper()} Sweep @ {self.swing_level:.2f}"


@dataclass
class TradeSetup:
    """Complete trade setup with entry, SL, and TPs"""
    setup_id: int
    sweep: LiquiditySweep
    fvg_5m: FVG
    direction: TradeDirection
    entry_datetime: datetime
    entry_price: float
    stop_loss: float
    risk_points: float
    tp_1rr: float
    tp_1_5rr: float
    tp_2rr: float
    tp_2_5rr: float
    tp_3rr: float
    tp_3_5rr: float
    tp_4rr: float
    tp_4_5rr: float
    tp_5rr: float
    
    def __str__(self):
        return (f"Setup #{self.setup_id} | {self.direction.value.upper()} | "
                f"Entry: {self.entry_price:.2f} | SL: {self.stop_loss:.2f} | "
                f"Risk: {self.risk_points:.2f}pts")


@dataclass 
class TradeResult:
    """Result of a backtested trade"""
    setup: TradeSetup
    tp1_hit: bool = False
    tp1_5_hit: bool = False
    tp2_hit: bool = False
    tp2_5_hit: bool = False
    tp3_hit: bool = False
    tp3_5_hit: bool = False
    tp4_hit: bool = False
    tp4_5_hit: bool = False
    tp5_hit: bool = False
    sl_hit: bool = False
    tp1_datetime: Optional[datetime] = None
    tp1_5_datetime: Optional[datetime] = None
    tp2_datetime: Optional[datetime] = None
    tp2_5_datetime: Optional[datetime] = None
    tp3_datetime: Optional[datetime] = None
    tp3_5_datetime: Optional[datetime] = None
    tp4_datetime: Optional[datetime] = None
    tp4_5_datetime: Optional[datetime] = None
    tp5_datetime: Optional[datetime] = None
    sl_datetime: Optional[datetime] = None
    max_favorable_excursion: float = 0.0
    max_adverse_excursion: float = 0.0
    exit_price: float = 0.0
    exit_datetime: Optional[datetime] = None
    pnl_points: float = 0.0
    
    def get_rr_achieved(self) -> float:
        """Calculate the R:R ratio achieved"""
        if self.setup.risk_points == 0:
            return 0.0
        return self.pnl_points / self.setup.risk_points


class SweepFVGStrategy:
    """
    Multi-timeframe strategy combining liquidity sweeps with FVG entries.
    
    Strategy Flow:
    1. Identify liquidity sweep on 15m (or higher TF)
    2. On 5m, wait for retracement that creates an FVG
    3. Wait for reversal back toward original trend direction
    4. On 1m, enter when price fills and closes beyond the 5m FVG
    5. SL above/below the FVG that was filled
    6. TPs at 1RR, 1.5RR, 2RR, 2.5RR, 3RR, 3.5RR, 4RR, 4.5RR, 5RR
    """
    
    def __init__(
        self,
        swing_lookback: int = 5,
        sweep_threshold_pct: float = 0.05,
        fvg_min_size_pct: float = 0.01,
        max_retracement_candles: int = 30,  # Max 5m candles to wait for FVG
        max_entry_wait_candles: int = 60,   # Max 1m candles to wait for entry
        sl_buffer_pct: float = 0.05,  # Stop loss buffer percentage (0.05 = 0.05%)
    ):
        self.swing_lookback = swing_lookback
        self.sweep_threshold_pct = sweep_threshold_pct / 100
        self.fvg_min_size_pct = fvg_min_size_pct / 100
        self.max_retracement_candles = max_retracement_candles
        self.max_entry_wait_candles = max_entry_wait_candles
        self.sl_buffer_pct = sl_buffer_pct / 100
        
    def load_data(self, filepath: str) -> pd.DataFrame:
        """Load CSV data with semicolon separator"""
        df = pd.read_csv(
            filepath, 
            sep=';',
            names=['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume'],
            skiprows=1
        )
        
        df['Datetime'] = pd.to_datetime(
            df['Date'] + ' ' + df['Time'], 
            format='%d/%m/%Y %H:%M:%S',
            errors='coerce'
        )
        
        for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        df = df.set_index('Datetime')
        df = df.drop(['Date', 'Time'], axis=1)
        df = df.dropna()
        
        return df
    
    def find_swing_highs(self, df: pd.DataFrame) -> List[Tuple[int, datetime, float]]:
        """Find swing highs in the data"""
        swing_highs = []
        highs = df['High'].values
        
        for i in range(self.swing_lookback, len(highs) - self.swing_lookback):
            window_before = highs[i - self.swing_lookback:i]
            window_after = highs[i + 1:i + self.swing_lookback + 1]
            
            if len(window_before) == 0 or len(window_after) == 0:
                continue
            
            if highs[i] > max(window_before) and highs[i] > max(window_after):
                swing_highs.append((i, df.index[i], highs[i]))
        
        return swing_highs
    
    def find_swing_lows(self, df: pd.DataFrame) -> List[Tuple[int, datetime, float]]:
        """Find swing lows in the data"""
        swing_lows = []
        lows = df['Low'].values
        
        for i in range(self.swing_lookback, len(lows) - self.swing_lookback):
            window_before = lows[i - self.swing_lookback:i]
            window_after = lows[i + 1:i + self.swing_lookback + 1]
            
            if len(window_before) == 0 or len(window_after) == 0:
                continue
            
            if lows[i] < min(window_before) and lows[i] < min(window_after):
                swing_lows.append((i, df.index[i], lows[i]))
        
        return swing_lows
    
    def detect_sweeps_15m(self, df_15m: pd.DataFrame) -> List[LiquiditySweep]:
        """Detect liquidity sweeps on 15m timeframe"""
        sweeps = []
        
        swing_highs = self.find_swing_highs(df_15m)
        swing_lows = self.find_swing_lows(df_15m)
        
        highs = df_15m['High'].values
        lows = df_15m['Low'].values
        closes = df_15m['Close'].values
        
        # Detect bearish sweeps (above swing highs)
        for swing_idx, swing_dt, swing_price in swing_highs:
            search_start = swing_idx + self.swing_lookback
            
            for i in range(search_start, len(highs)):
                sweep_amount = highs[i] - swing_price
                sweep_pct = sweep_amount / swing_price if swing_price > 0 else 0
                
                if sweep_pct > self.sweep_threshold_pct:
                    if closes[i] < swing_price:
                        sweeps.append(LiquiditySweep(
                            datetime=df_15m.index[i],
                            index=i,
                            sweep_type='bearish',
                            swing_level=swing_price,
                            sweep_price=highs[i],
                            close_price=closes[i]
                        ))
                        break
        
        # Detect bullish sweeps (below swing lows)
        for swing_idx, swing_dt, swing_price in swing_lows:
            search_start = swing_idx + self.swing_lookback
            
            for i in range(search_start, len(lows)):
                sweep_amount = swing_price - lows[i]
                sweep_pct = sweep_amount / swing_price if swing_price > 0 else 0
                
                if sweep_pct > self.sweep_threshold_pct:
                    if closes[i] > swing_price:
                        sweeps.append(LiquiditySweep(
                            datetime=df_15m.index[i],
                            index=i,
                            sweep_type='bullish',
                            swing_level=swing_price,
                            sweep_price=lows[i],
                            close_price=closes[i]
                        ))
                        break
        
        sweeps.sort(key=lambda x: x.datetime)
        return sweeps
    
    def detect_fvg_before_sweep(
        self, 
        df_5m: pd.DataFrame, 
        sweep_time: datetime,
        sweep_type: str
    ) -> Optional[FVG]:
        """
        Detect FVG on 5m timeframe BEFORE a sweep.
        
        Logic according to user specification:
        - When price goes UP, it creates a BULLISH FVG
        - After a BEARISH liquidity sweep, the price reverses and BREAKS the previous bullish FVG
        - Entry when 1m candle closes BELOW the previous bullish FVG
        
        For bearish sweep: Look for BULLISH FVG created before the sweep (during the up move)
        For bullish sweep: Look for BEARISH FVG created before the sweep (during the down move)
        """
        # Filter data before sweep time (look for FVG created in the move before the sweep)
        df_before = df_5m[df_5m.index < sweep_time]
        
        if len(df_before) < 3:
            return None
        
        highs = df_before['High'].values
        lows = df_before['Low'].values
        
        # Look back for FVG in the last N candles before sweep
        lookback_start = max(0, len(df_before) - self.max_retracement_candles)
        
        # For bearish sweep: look for BULLISH FVG (created during the up move before sweep)
        # For bullish sweep: look for BEARISH FVG (created during the down move before sweep)
        expected_fvg_type = 'bullish' if sweep_type == 'bearish' else 'bearish'
        
        # Store found FVGs and return the most recent one
        found_fvg = None
        
        for i in range(lookback_start + 2, len(df_before)):
            candle1_high = highs[i - 2]
            candle1_low = lows[i - 2]
            candle3_high = highs[i]
            candle3_low = lows[i]
            
            # Check for Bullish FVG (gap up) - created during UP move
            if expected_fvg_type == 'bullish' and candle1_high < candle3_low:
                gap_low = candle1_high
                gap_high = candle3_low
                gap_size = gap_high - gap_low
                gap_size_pct = gap_size / gap_low if gap_low > 0 else 0
                
                if gap_size_pct >= self.fvg_min_size_pct:
                    found_fvg = FVG(
                        datetime=df_before.index[i - 1],
                        index=i - 1,
                        fvg_type='bullish',
                        gap_high=gap_high,
                        gap_low=gap_low,
                        gap_size=gap_size
                    )
            
            # Check for Bearish FVG (gap down) - created during DOWN move
            elif expected_fvg_type == 'bearish' and candle1_low > candle3_high:
                gap_low = candle3_high
                gap_high = candle1_low
                gap_size = gap_high - gap_low
                gap_size_pct = gap_size / gap_low if gap_low > 0 else 0
                
                if gap_size_pct >= self.fvg_min_size_pct:
                    found_fvg = FVG(
                        datetime=df_before.index[i - 1],
                        index=i - 1,
                        fvg_type='bearish',
                        gap_high=gap_high,
                        gap_low=gap_low,
                        gap_size=gap_size
                    )
        
        return found_fvg
    
    def find_entry_1m(
        self,
        df_1m: pd.DataFrame,
        fvg: FVG,
        sweep: LiquiditySweep
    ) -> Optional[Tuple[datetime, float, int]]:
        """
        Find entry point on 1m when price BREAKS and closes beyond the previous FVG.
        
        Logic according to user specification:
        - For bearish sweep: Previous BULLISH FVG exists
          - Entry when candle closes BELOW the bullish FVG (breaking it)
        
        - For bullish sweep: Previous BEARISH FVG exists
          - Entry when candle closes ABOVE the bearish FVG (breaking it)
        """
        # Filter data after sweep time (entry happens after the sweep)
        df_after = df_1m[df_1m.index > sweep.datetime]
        
        if len(df_after) < 1:
            return None
        
        closes = df_after['Close'].values
        
        max_candles = min(len(df_after), self.max_entry_wait_candles)
        
        for i in range(max_candles):
            # For bearish sweep: look for close BELOW the bullish FVG (breaking it down)
            if sweep.sweep_type == 'bearish':
                # Entry when price closes below FVG gap_low (breaks the bullish FVG)
                if closes[i] < fvg.gap_low:
                    return (df_after.index[i], closes[i], i)
            
            # For bullish sweep: look for close ABOVE the bearish FVG (breaking it up)
            else:
                # Entry when price closes above FVG gap_high (breaks the bearish FVG)
                if closes[i] > fvg.gap_high:
                    return (df_after.index[i], closes[i], i)
        
        return None
    
    def calculate_trade_levels(
        self,
        entry_price: float,
        fvg: FVG,
        direction: TradeDirection
    ) -> Tuple[float, float, float, float, float, float, float, float, float, float, float]:
        """
        Calculate SL and TP levels.
        
        SL: Above FVG gap_high for shorts, below FVG gap_low for longs
        TPs: 1RR, 1.5RR, 2RR, 2.5RR, 3RR, 3.5RR, 4RR, 4.5RR, 5RR from entry
        """
        if direction == TradeDirection.SHORT:
            # SL above the FVG gap_high with buffer
            stop_loss = fvg.gap_high + (fvg.gap_high * self.sl_buffer_pct)
            risk_points = stop_loss - entry_price
            
            tp_1rr = entry_price - risk_points * 1
            tp_1_5rr = entry_price - risk_points * 1.5
            tp_2rr = entry_price - risk_points * 2
            tp_2_5rr = entry_price - risk_points * 2.5
            tp_3rr = entry_price - risk_points * 3
            tp_3_5rr = entry_price - risk_points * 3.5
            tp_4rr = entry_price - risk_points * 4
            tp_4_5rr = entry_price - risk_points * 4.5
            tp_5rr = entry_price - risk_points * 5
        else:
            # SL below the FVG gap_low with buffer
            stop_loss = fvg.gap_low - (fvg.gap_low * self.sl_buffer_pct)
            risk_points = entry_price - stop_loss
            
            tp_1rr = entry_price + risk_points * 1
            tp_1_5rr = entry_price + risk_points * 1.5
            tp_2rr = entry_price + risk_points * 2
            tp_2_5rr = entry_price + risk_points * 2.5
            tp_3rr = entry_price + risk_points * 3
            tp_3_5rr = entry_price + risk_points * 3.5
            tp_4rr = entry_price + risk_points * 4
            tp_4_5rr = entry_price + risk_points * 4.5
            tp_5rr = entry_price + risk_points * 5
        
        return (stop_loss, risk_points, tp_1rr, tp_1_5rr, tp_2rr, tp_2_5rr, 
                tp_3rr, tp_3_5rr, tp_4rr, tp_4_5rr, tp_5rr)
    
    def backtest_trade(
        self,
        df_1m: pd.DataFrame,
        setup: TradeSetup
    ) -> TradeResult:
        """Backtest a single trade setup"""
        result = TradeResult(setup=setup)
        
        # Get data after entry
        df_after = df_1m[df_1m.index > setup.entry_datetime]
        
        if len(df_after) == 0:
            return result
        
        highs = df_after['High'].values
        lows = df_after['Low'].values
        
        for i in range(len(df_after)):
            current_high = highs[i]
            current_low = lows[i]
            current_time = df_after.index[i]
            
            if setup.direction == TradeDirection.SHORT:
                # Track MFE/MAE
                result.max_favorable_excursion = max(
                    result.max_favorable_excursion,
                    setup.entry_price - current_low
                )
                result.max_adverse_excursion = max(
                    result.max_adverse_excursion,
                    current_high - setup.entry_price
                )
                
                # Check SL
                if current_high >= setup.stop_loss and not result.sl_hit:
                    result.sl_hit = True
                    result.sl_datetime = current_time
                    result.exit_price = setup.stop_loss
                    result.exit_datetime = current_time
                    result.pnl_points = setup.entry_price - setup.stop_loss
                    break
                
                # Check TPs
                if current_low <= setup.tp_1rr and not result.tp1_hit:
                    result.tp1_hit = True
                    result.tp1_datetime = current_time
                
                if current_low <= setup.tp_1_5rr and not result.tp1_5_hit:
                    result.tp1_5_hit = True
                    result.tp1_5_datetime = current_time
                
                if current_low <= setup.tp_2rr and not result.tp2_hit:
                    result.tp2_hit = True
                    result.tp2_datetime = current_time
                
                if current_low <= setup.tp_2_5rr and not result.tp2_5_hit:
                    result.tp2_5_hit = True
                    result.tp2_5_datetime = current_time
                
                if current_low <= setup.tp_3rr and not result.tp3_hit:
                    result.tp3_hit = True
                    result.tp3_datetime = current_time
                
                if current_low <= setup.tp_3_5rr and not result.tp3_5_hit:
                    result.tp3_5_hit = True
                    result.tp3_5_datetime = current_time
                
                if current_low <= setup.tp_4rr and not result.tp4_hit:
                    result.tp4_hit = True
                    result.tp4_datetime = current_time
                
                if current_low <= setup.tp_4_5rr and not result.tp4_5_hit:
                    result.tp4_5_hit = True
                    result.tp4_5_datetime = current_time
                
                if current_low <= setup.tp_5rr and not result.tp5_hit:
                    result.tp5_hit = True
                    result.tp5_datetime = current_time
                    result.exit_price = setup.tp_5rr
                    result.exit_datetime = current_time
                    result.pnl_points = setup.entry_price - setup.tp_5rr
                    break
                    
            else:  # LONG
                # Track MFE/MAE
                result.max_favorable_excursion = max(
                    result.max_favorable_excursion,
                    current_high - setup.entry_price
                )
                result.max_adverse_excursion = max(
                    result.max_adverse_excursion,
                    setup.entry_price - current_low
                )
                
                # Check SL
                if current_low <= setup.stop_loss and not result.sl_hit:
                    result.sl_hit = True
                    result.sl_datetime = current_time
                    result.exit_price = setup.stop_loss
                    result.exit_datetime = current_time
                    result.pnl_points = setup.stop_loss - setup.entry_price
                    break
                
                # Check TPs
                if current_high >= setup.tp_1rr and not result.tp1_hit:
                    result.tp1_hit = True
                    result.tp1_datetime = current_time
                
                if current_high >= setup.tp_1_5rr and not result.tp1_5_hit:
                    result.tp1_5_hit = True
                    result.tp1_5_datetime = current_time
                
                if current_high >= setup.tp_2rr and not result.tp2_hit:
                    result.tp2_hit = True
                    result.tp2_datetime = current_time
                
                if current_high >= setup.tp_2_5rr and not result.tp2_5_hit:
                    result.tp2_5_hit = True
                    result.tp2_5_datetime = current_time
                
                if current_high >= setup.tp_3rr and not result.tp3_hit:
                    result.tp3_hit = True
                    result.tp3_datetime = current_time
                
                if current_high >= setup.tp_3_5rr and not result.tp3_5_hit:
                    result.tp3_5_hit = True
                    result.tp3_5_datetime = current_time
                
                if current_high >= setup.tp_4rr and not result.tp4_hit:
                    result.tp4_hit = True
                    result.tp4_datetime = current_time
                
                if current_high >= setup.tp_4_5rr and not result.tp4_5_hit:
                    result.tp4_5_hit = True
                    result.tp4_5_datetime = current_time
                
                if current_high >= setup.tp_5rr and not result.tp5_hit:
                    result.tp5_hit = True
                    result.tp5_datetime = current_time
                    result.exit_price = setup.tp_5rr
                    result.exit_datetime = current_time
                    result.pnl_points = setup.tp_5rr - setup.entry_price
                    break
        
        return result
    
    def run_backtest(
        self,
        df_15m: pd.DataFrame,
        df_5m: pd.DataFrame,
        df_1m: pd.DataFrame
    ) -> Tuple[List[TradeSetup], List[TradeResult]]:
        """
        Run the complete backtest strategy.
        """
        print("="*60)
        print("SWEEP + FVG MULTI-TIMEFRAME STRATEGY BACKTEST")
        print("="*60)
        
        # Step 1: Detect sweeps on 15m
        print("\n[1/4] Detecting liquidity sweeps on 15m...")
        sweeps = self.detect_sweeps_15m(df_15m)
        print(f"Found {len(sweeps)} sweeps")
        
        bullish_sweeps = [s for s in sweeps if s.sweep_type == 'bullish']
        bearish_sweeps = [s for s in sweeps if s.sweep_type == 'bearish']
        print(f"  - Bullish: {len(bullish_sweeps)}")
        print(f"  - Bearish: {len(bearish_sweeps)}")
        
        setups = []
        results = []
        setup_id = 0
        
        # Step 2-4: For each sweep, look for FVG BEFORE the sweep and entry
        print("\n[2/4] Scanning for FVG created BEFORE each sweep on 5m...")
        print("[3/4] Finding entries on 1m when FVG is broken...")
        
        for sweep in sweeps:
            # Look for FVG on 5m BEFORE the sweep (the FVG that will be broken)
            fvg = self.detect_fvg_before_sweep(df_5m, sweep.datetime, sweep.sweep_type)
            
            if fvg is None:
                continue
            
            # Look for entry on 1m when FVG is broken
            entry_result = self.find_entry_1m(df_1m, fvg, sweep)
            
            if entry_result is None:
                continue
            
            entry_datetime, entry_price, entry_idx = entry_result
            
            # Determine direction
            direction = TradeDirection.SHORT if sweep.sweep_type == 'bearish' else TradeDirection.LONG
            
            # Calculate levels - SL based on the FVG that was broken
            (sl, risk, tp1, tp1_5, tp2, tp2_5, tp3, tp3_5, tp4, tp4_5, tp5) = self.calculate_trade_levels(
                entry_price, fvg, direction
            )
            
            # Skip if risk is too small or negative
            if risk <= 0:
                continue
            
            setup_id += 1
            setup = TradeSetup(
                setup_id=setup_id,
                sweep=sweep,
                fvg_5m=fvg,
                direction=direction,
                entry_datetime=entry_datetime,
                entry_price=entry_price,
                stop_loss=sl,
                risk_points=risk,
                tp_1rr=tp1,
                tp_1_5rr=tp1_5,
                tp_2rr=tp2,
                tp_2_5rr=tp2_5,
                tp_3rr=tp3,
                tp_3_5rr=tp3_5,
                tp_4rr=tp4,
                tp_4_5rr=tp4_5,
                tp_5rr=tp5
            )
            setups.append(setup)
        
        print(f"\nFound {len(setups)} valid setups")
        
        # Step 4: Backtest each setup
        print("\n[4/4] Backtesting trades...")
        
        for setup in setups:
            result = self.backtest_trade(df_1m, setup)
            results.append(result)
        
        return setups, results
    
    def generate_report(
        self,
        setups: List[TradeSetup],
        results: List[TradeResult]
    ) -> str:
        """Generate a detailed analysis report in Markdown format"""
        
        report = []
        report.append("# 📊 Analyse Détaillée: Stratégie Sweep + FVG Multi-Timeframe\n")
        report.append("---\n")
        
        # Strategy Overview
        report.append("## 🎯 Vue d'Ensemble de la Stratégie\n")
        report.append("""
Cette stratégie combine la détection de **Liquidity Sweeps** sur le timeframe 15 minutes 
avec les **Fair Value Gaps (FVG)** sur 5 minutes pour trouver des entrées précises sur 1 minute.

### Logique de la Stratégie

1. **Détection du Sweep (15m)**: Un swing high (mouvement haussier puis baissier) ou swing low. Seule la mèche casse le swing pour prendre la liquidité.
2. **FVG Précédent (5m)**: Identifier le FVG créé AVANT le sweep (FVG haussier créé pendant la montée, ou FVG baissier créé pendant la descente)
3. **Cassure du FVG (1m)**: Après le sweep, le prix revient et CASSE le FVG précédent
4. **Entrée (1m)**: Entrer quand la bougie 1m clôture au-delà du FVG (en-dessous pour short, au-dessus pour long)
5. **Stop Loss**: Au-dessus du FVG cassé (short) / En-dessous du FVG cassé (long)
6. **Take Profits**: 1RR, 1.5RR, 2RR, 2.5RR, 3RR, 3.5RR, 4RR, 4.5RR, 5RR
""")
        
        # Results Summary
        report.append("\n## 📈 Résumé des Résultats\n")
        
        if not results:
            report.append("*Aucun trade trouvé avec les paramètres actuels.*\n")
            return "\n".join(report)
        
        total_trades = len(results)
        winners = [r for r in results if r.pnl_points > 0]
        losers = [r for r in results if r.pnl_points < 0]
        breakeven = [r for r in results if r.pnl_points == 0]
        
        win_rate = (len(winners) / total_trades * 100) if total_trades > 0 else 0
        
        # TP hit rates
        tp1_hits = sum(1 for r in results if r.tp1_hit)
        tp1_5_hits = sum(1 for r in results if r.tp1_5_hit)
        tp2_hits = sum(1 for r in results if r.tp2_hit)
        tp2_5_hits = sum(1 for r in results if r.tp2_5_hit)
        tp3_hits = sum(1 for r in results if r.tp3_hit)
        tp3_5_hits = sum(1 for r in results if r.tp3_5_hit)
        tp4_hits = sum(1 for r in results if r.tp4_hit)
        tp4_5_hits = sum(1 for r in results if r.tp4_5_hit)
        tp5_hits = sum(1 for r in results if r.tp5_hit)
        sl_hits = sum(1 for r in results if r.sl_hit)
        
        total_pnl = sum(r.pnl_points for r in results)
        avg_winner = sum(r.pnl_points for r in winners) / len(winners) if winners else 0
        avg_loser = sum(r.pnl_points for r in losers) / len(losers) if losers else 0
        
        report.append(f"| Métrique | Valeur |")
        report.append(f"|----------|--------|")
        report.append(f"| Nombre total de trades | {total_trades} |")
        report.append(f"| Trades gagnants | {len(winners)} |")
        report.append(f"| Trades perdants | {len(losers)} |")
        report.append(f"| Win Rate | {win_rate:.1f}% |")
        report.append(f"| PnL Total (points) | {total_pnl:.2f} |")
        report.append(f"| Gain moyen | {avg_winner:.2f} pts |")
        report.append(f"| Perte moyenne | {avg_loser:.2f} pts |")
        report.append("")
        
        # TP Analysis
        report.append("\n### 🎯 Analyse des Take Profits (Win Rate par RR)\n")
        report.append(f"| RR | Atteints | Win Rate |")
        report.append(f"|----|----------|----------|")
        report.append(f"| 1 RR | {tp1_hits} | {tp1_hits/total_trades*100:.1f}% |")
        report.append(f"| 1.5 RR | {tp1_5_hits} | {tp1_5_hits/total_trades*100:.1f}% |")
        report.append(f"| 2 RR | {tp2_hits} | {tp2_hits/total_trades*100:.1f}% |")
        report.append(f"| 2.5 RR | {tp2_5_hits} | {tp2_5_hits/total_trades*100:.1f}% |")
        report.append(f"| 3 RR | {tp3_hits} | {tp3_hits/total_trades*100:.1f}% |")
        report.append(f"| 3.5 RR | {tp3_5_hits} | {tp3_5_hits/total_trades*100:.1f}% |")
        report.append(f"| 4 RR | {tp4_hits} | {tp4_hits/total_trades*100:.1f}% |")
        report.append(f"| 4.5 RR | {tp4_5_hits} | {tp4_5_hits/total_trades*100:.1f}% |")
        report.append(f"| 5 RR | {tp5_hits} | {tp5_hits/total_trades*100:.1f}% |")
        report.append(f"| **Stop Loss** | {sl_hits} | {sl_hits/total_trades*100:.1f}% |")
        report.append("")
        
        # Direction Analysis
        report.append("\n### 📊 Analyse par Direction\n")
        
        longs = [r for r in results if r.setup.direction == TradeDirection.LONG]
        shorts = [r for r in results if r.setup.direction == TradeDirection.SHORT]
        
        long_winners = [r for r in longs if r.pnl_points > 0]
        short_winners = [r for r in shorts if r.pnl_points > 0]
        
        report.append(f"| Direction | Trades | Gagnants | Win Rate |")
        report.append(f"|-----------|--------|----------|----------|")
        if longs:
            report.append(f"| LONG | {len(longs)} | {len(long_winners)} | {len(long_winners)/len(longs)*100:.1f}% |")
        if shorts:
            report.append(f"| SHORT | {len(shorts)} | {len(short_winners)} | {len(short_winners)/len(shorts)*100:.1f}% |")
        report.append("")
        
        # Trade Details
        report.append("\n## 📝 Détail des Trades\n")
        
        for i, (setup, result) in enumerate(zip(setups, results)):
            status = "✅ GAGNANT" if result.pnl_points > 0 else "❌ PERDANT" if result.pnl_points < 0 else "➖ BE"
            rr_achieved = result.get_rr_achieved()
            
            report.append(f"### Trade #{setup.setup_id} - {status}\n")
            report.append(f"- **Direction**: {setup.direction.value.upper()}")
            report.append(f"- **Sweep**: {setup.sweep.sweep_type.upper()} @ {setup.sweep.datetime}")
            report.append(f"- **FVG 5m**: {setup.fvg_5m.gap_low:.2f} - {setup.fvg_5m.gap_high:.2f} @ {setup.fvg_5m.datetime}")
            report.append(f"- **Entrée**: {setup.entry_price:.2f} @ {setup.entry_datetime}")
            report.append(f"- **Stop Loss**: {setup.stop_loss:.2f}")
            report.append(f"- **Risk**: {setup.risk_points:.2f} points")
            report.append(f"- **TP 1RR**: {setup.tp_1rr:.2f} {'✅' if result.tp1_hit else '❌'}")
            report.append(f"- **TP 1.5RR**: {setup.tp_1_5rr:.2f} {'✅' if result.tp1_5_hit else '❌'}")
            report.append(f"- **TP 2RR**: {setup.tp_2rr:.2f} {'✅' if result.tp2_hit else '❌'}")
            report.append(f"- **TP 2.5RR**: {setup.tp_2_5rr:.2f} {'✅' if result.tp2_5_hit else '❌'}")
            report.append(f"- **TP 3RR**: {setup.tp_3rr:.2f} {'✅' if result.tp3_hit else '❌'}")
            report.append(f"- **TP 3.5RR**: {setup.tp_3_5rr:.2f} {'✅' if result.tp3_5_hit else '❌'}")
            report.append(f"- **TP 4RR**: {setup.tp_4rr:.2f} {'✅' if result.tp4_hit else '❌'}")
            report.append(f"- **TP 4.5RR**: {setup.tp_4_5rr:.2f} {'✅' if result.tp4_5_hit else '❌'}")
            report.append(f"- **TP 5RR**: {setup.tp_5rr:.2f} {'✅' if result.tp5_hit else '❌'}")
            report.append(f"- **PnL**: {result.pnl_points:.2f} points ({rr_achieved:.1f}R)")
            report.append(f"- **MFE**: {result.max_favorable_excursion:.2f} points")
            report.append(f"- **MAE**: {result.max_adverse_excursion:.2f} points")
            report.append("")
        
        # Strategy Rules
        report.append("\n## 📋 Règles de la Stratégie\n")
        report.append("""
### Conditions d'Entrée

1. **Sweep 15m détecté**:
   - Bullish: Prix casse sous un swing low puis clôture au-dessus
   - Bearish: Prix casse au-dessus d'un swing high puis clôture en-dessous

2. **FVG 5m formé** (dans les 30 bougies suivantes):
   - Pour sweep bullish: FVG bullish (gap up)
   - Pour sweep bearish: FVG bearish (gap down)

3. **Entrée 1m** (dans les 60 bougies suivantes):
   - Le prix doit toucher la zone FVG
   - Puis clôturer au-delà du FVG dans le sens du trade

### Gestion du Trade

| Élément | Placement |
|---------|-----------|
| **Stop Loss** | Au-dessus du FVG comblé (short) / En-dessous du FVG comblé (long) |
| **TP 1** | 1x le risque |
| **TP 1.5** | 1.5x le risque |
| **TP 2** | 2x le risque |
| **TP 2.5** | 2.5x le risque |
| **TP 3** | 3x le risque |
| **TP 3.5** | 3.5x le risque |
| **TP 4** | 4x le risque |
| **TP 4.5** | 4.5x le risque |
| **TP 5** | 5x le risque |

### Gestion de Position Suggérée

Exemple avec sortie progressive:
- **10%** à TP1 (1RR)
- **10%** à TP2 (2RR)
- **20%** à TP3 (3RR)
- **30%** à TP4 (4RR)
- **30%** à TP5 (5RR)
""")
        
        # Recommendations
        report.append("\n## 💡 Recommandations\n")
        
        if win_rate >= 50:
            report.append("✅ La stratégie montre un win rate positif.\n")
        else:
            report.append("⚠️ Le win rate est inférieur à 50%. Considérer des filtres supplémentaires.\n")
        
        if tp2_hits / total_trades > 0.3 if total_trades > 0 else False:
            report.append("✅ Bon taux d'atteinte du TP2 - la stratégie capture bien les mouvements.\n")
        
        if sl_hits / total_trades > 0.5 if total_trades > 0 else False:
            report.append("⚠️ Taux de SL élevé. Suggestions:")
            report.append("   - Augmenter le buffer du SL")
            report.append("   - Filtrer les setups par volume")
            report.append("   - Attendre confirmation supplémentaire\n")
        
        report.append("""
### Filtres Additionnels Suggérés

1. **Volume**: N'entrer que si le volume du sweep est > 1.5x la moyenne
2. **Session**: Privilégier les sessions Londres et New York
3. **Trend**: Trader dans le sens de la tendance HTF (4H/Daily)
4. **News**: Éviter les 30 minutes avant/après les annonces majeures
""")
        
        report.append("\n---\n")
        report.append(f"*Rapport généré le {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")
        
        return "\n".join(report)


def main():
    """Main function to run the strategy backtest"""
    parser = argparse.ArgumentParser(
        description='Sweep + FVG Multi-Timeframe Strategy Backtest'
    )
    parser.add_argument(
        '--year', 
        type=int, 
        default=2025,
        help='Year of data to analyze (default: 2025)'
    )
    parser.add_argument(
        '--swing-lookback',
        type=int,
        default=5,
        help='Bars for swing detection (default: 5)'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='STRATEGY_ANALYSIS.md',
        help='Output file for analysis report (default: STRATEGY_ANALYSIS.md)'
    )
    
    args = parser.parse_args()
    
    base_path = Path(__file__).parent
    
    # Load data files
    file_15m = base_path / f"{args.year} 15m.csv"
    file_5m = base_path / f"{args.year} 5m.csv"
    file_1m = base_path / f"{args.year} 1m.csv"
    
    # Check for 1m data - might be zipped
    if not file_1m.exists():
        file_1m_zip = base_path / f"{args.year} 1m.csv.zip"
        if file_1m_zip.exists():
            print(f"Note: 1m data is zipped. Please unzip {file_1m_zip} first.")
            return
        else:
            print(f"Error: 1m data not found for {args.year}")
            return
    
    for f in [file_15m, file_5m, file_1m]:
        if not f.exists():
            print(f"Error: File not found: {f}")
            return
    
    # Initialize strategy
    strategy = SweepFVGStrategy(
        swing_lookback=args.swing_lookback
    )
    
    # Load data
    print("Loading data...")
    df_15m = strategy.load_data(str(file_15m))
    df_5m = strategy.load_data(str(file_5m))
    df_1m = strategy.load_data(str(file_1m))
    
    print(f"15m: {len(df_15m)} candles ({df_15m.index.min()} to {df_15m.index.max()})")
    print(f"5m: {len(df_5m)} candles")
    print(f"1m: {len(df_1m)} candles")
    
    # Run backtest
    setups, results = strategy.run_backtest(df_15m, df_5m, df_1m)
    
    # Generate report
    report = strategy.generate_report(setups, results)
    
    # Save report
    output_path = base_path / args.output
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n✅ Report saved to: {output_path}")
    
    # Print summary
    if results:
        total_trades = len(results)
        winners = sum(1 for r in results if r.pnl_points > 0)
        total_pnl = sum(r.pnl_points for r in results)
        
        print(f"\n📊 SUMMARY:")
        print(f"   Total trades: {total_trades}")
        print(f"   Win rate: {winners/total_trades*100:.1f}%")
        print(f"   Total PnL: {total_pnl:.2f} points")


if __name__ == "__main__":
    main()

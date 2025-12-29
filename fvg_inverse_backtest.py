#!/usr/bin/env python3
"""
FVG Inverse Trading Strategy Backtest
======================================
This script implements a Fair Value Gap (FVG) inverse trading strategy
on NQ futures data with the following rules:

Time Rules:
- Single session: 01:00 - 05:00 daily
- FVG detection only within session window
- Daily reset: All FVGs erased at 01:00

Trading Rules:
- Bearish FVG: candle[i-2].Low > candle[i].High -> LONG when price closes above High_Zone
- Bullish FVG: candle[i-2].High < candle[i].Low -> SHORT when price closes below Low_Zone
- Single position at a time
- Stop Loss at signal candle low (LONG) or high (SHORT)
- Take Profit at 1:2 ratio
- Session close at 05:00 if position still open
"""

import pandas as pd
import numpy as np
import glob
from datetime import datetime, time
from typing import List, Dict, Tuple, Optional


class FVGZone:
    """Represents a Fair Value Gap zone"""
    def __init__(self, zone_type: str, high_zone: float, low_zone: float, creation_candle_idx: int):
        self.zone_type = zone_type  # 'bearish' or 'bullish'
        self.high_zone = high_zone
        self.low_zone = low_zone
        self.creation_candle_idx = creation_candle_idx
        self.triggered = False


class Position:
    """Represents an open trading position"""
    def __init__(self, position_type: str, entry_price: float, entry_idx: int, 
                 stop_loss: float, take_profit: float, entry_time: datetime):
        self.position_type = position_type  # 'LONG' or 'SHORT'
        self.entry_price = entry_price
        self.entry_idx = entry_idx
        self.stop_loss = stop_loss
        self.take_profit = take_profit
        self.entry_time = entry_time
        self.exit_price = None
        self.exit_idx = None
        self.exit_time = None
        self.exit_reason = None  # 'TP', 'SL', or 'SESSION_CLOSE'
        self.pnl = 0.0


class FVGInverseBacktester:
    """Main backtester for FVG inverse strategy"""
    
    def __init__(self, df: pd.DataFrame, timeframe: str):
        self.df = df.copy()
        self.timeframe = timeframe
        self.session_start = time(1, 0)  # 01:00
        self.session_end = time(5, 0)    # 05:00
        
        # Trading state
        self.fvg_zones: List[FVGZone] = []
        self.current_position: Optional[Position] = None
        self.closed_positions: List[Position] = []
        
        # Prepare data
        self._prepare_data()
    
    def _prepare_data(self):
        """Prepare and clean the data"""
        # Parse datetime
        self.df['DateTime'] = pd.to_datetime(
            self.df['Date'] + ' ' + self.df['Time'],
            format='%d/%m/%Y %H:%M:%S'
        )
        
        # Extract date and time components
        self.df['Date_Only'] = self.df['DateTime'].dt.date
        self.df['Time_Only'] = self.df['DateTime'].dt.time
        
        # Sort by datetime
        self.df = self.df.sort_values('DateTime').reset_index(drop=True)
    
    def _is_in_session(self, current_time: time) -> bool:
        """Check if current time is within trading session"""
        return self.session_start <= current_time <= self.session_end
    
    def _detect_fvg(self, i: int) -> Optional[FVGZone]:
        """
        Detect FVG at current candle index i
        Returns FVGZone if detected, None otherwise
        """
        if i < 2:
            return None
        
        # Get candles
        candle_i_minus_2 = self.df.iloc[i - 2]
        candle_i = self.df.iloc[i]
        current_time = self.df.iloc[i]['Time_Only']
        
        # Only detect FVG within session
        if not self._is_in_session(current_time):
            return None
        
        # Bearish FVG: candle[i-2].Low > candle[i].High
        if candle_i_minus_2['Low'] > candle_i['High']:
            return FVGZone(
                zone_type='bearish',
                high_zone=candle_i_minus_2['Low'],
                low_zone=candle_i['High'],
                creation_candle_idx=i
            )
        
        # Bullish FVG: candle[i-2].High < candle[i].Low
        elif candle_i_minus_2['High'] < candle_i['Low']:
            return FVGZone(
                zone_type='bullish',
                high_zone=candle_i['Low'],
                low_zone=candle_i_minus_2['High'],
                creation_candle_idx=i
            )
        
        return None
    
    def _check_entry_signal(self, i: int) -> Optional[Tuple[str, FVGZone, float, float, float]]:
        """
        Check for entry signals at current candle
        Returns (position_type, zone, entry_price, stop_loss, take_profit) or None
        """
        if self.current_position is not None:
            return None  # Already in position
        
        candle = self.df.iloc[i]
        current_time = candle['Time_Only']
        
        # Only check signals within session
        if not self._is_in_session(current_time):
            return None
        
        close_price = candle['Close']
        
        # Check all active FVG zones
        for zone in self.fvg_zones:
            if zone.triggered:
                continue
            
            # LONG signal: Close above High_Zone of Bearish FVG
            if zone.zone_type == 'bearish' and close_price > zone.high_zone:
                zone.triggered = True
                entry_price = close_price
                stop_loss = candle['Low']  # Signal candle low
                risk = entry_price - stop_loss
                take_profit = entry_price + (2 * risk)  # 1:2 ratio
                return ('LONG', zone, entry_price, stop_loss, take_profit)
            
            # SHORT signal: Close below Low_Zone of Bullish FVG
            elif zone.zone_type == 'bullish' and close_price < zone.low_zone:
                zone.triggered = True
                entry_price = close_price
                stop_loss = candle['High']  # Signal candle high
                risk = stop_loss - entry_price
                take_profit = entry_price - (2 * risk)  # 1:2 ratio
                return ('SHORT', zone, entry_price, stop_loss, take_profit)
        
        return None
    
    def _check_exit(self, i: int) -> Optional[Tuple[str, float]]:
        """
        Check if current position should be exited
        Returns (exit_reason, exit_price) or None
        """
        if self.current_position is None:
            return None
        
        candle = self.df.iloc[i]
        current_time = candle['Time_Only']
        
        # Check session close
        if current_time == self.session_end:
            return ('SESSION_CLOSE', candle['Close'])
        
        position = self.current_position
        
        if position.position_type == 'LONG':
            # Check TP and SL
            if candle['High'] >= position.take_profit:
                return ('TP', position.take_profit)
            elif candle['Low'] <= position.stop_loss:
                return ('SL', position.stop_loss)
        
        elif position.position_type == 'SHORT':
            # Check TP and SL
            if candle['Low'] <= position.take_profit:
                return ('TP', position.take_profit)
            elif candle['High'] >= position.stop_loss:
                return ('SL', position.stop_loss)
        
        return None
    
    def _close_position(self, i: int, exit_reason: str, exit_price: float):
        """Close the current position"""
        if self.current_position is None:
            return
        
        position = self.current_position
        position.exit_price = exit_price
        position.exit_idx = i
        position.exit_time = self.df.iloc[i]['DateTime']
        position.exit_reason = exit_reason
        
        # Calculate PnL in points
        if position.position_type == 'LONG':
            position.pnl = exit_price - position.entry_price
        else:  # SHORT
            position.pnl = position.entry_price - exit_price
        
        self.closed_positions.append(position)
        self.current_position = None
    
    def _reset_daily_state(self):
        """Reset FVG zones at start of new trading day"""
        self.fvg_zones = []
    
    def run_backtest(self) -> Dict:
        """
        Run the complete backtest
        Returns dictionary with performance metrics
        """
        print(f"\nRunning backtest for {self.timeframe}...")
        
        current_date = None
        
        for i in range(len(self.df)):
            candle = self.df.iloc[i]
            candle_date = candle['Date_Only']
            candle_time = candle['Time_Only']
            
            # Daily reset at 01:00
            if candle_time == self.session_start and candle_date != current_date:
                self._reset_daily_state()
                current_date = candle_date
            
            # Detect new FVG zones
            new_fvg = self._detect_fvg(i)
            if new_fvg is not None:
                self.fvg_zones.append(new_fvg)
            
            # Check for exit first (if in position)
            exit_signal = self._check_exit(i)
            if exit_signal is not None:
                exit_reason, exit_price = exit_signal
                self._close_position(i, exit_reason, exit_price)
            
            # Check for entry signal (if not in position)
            entry_signal = self._check_entry_signal(i)
            if entry_signal is not None:
                position_type, zone, entry_price, stop_loss, take_profit = entry_signal
                self.current_position = Position(
                    position_type=position_type,
                    entry_price=entry_price,
                    entry_idx=i,
                    stop_loss=stop_loss,
                    take_profit=take_profit,
                    entry_time=candle['DateTime']
                )
        
        # Close any remaining position at end of data
        if self.current_position is not None:
            last_idx = len(self.df) - 1
            self._close_position(last_idx, 'END_OF_DATA', self.df.iloc[last_idx]['Close'])
        
        # Calculate metrics
        return self._calculate_metrics()
    
    def _calculate_metrics(self) -> Dict:
        """Calculate performance metrics"""
        if len(self.closed_positions) == 0:
            return {
                'timeframe': self.timeframe,
                'total_trades': 0,
                'winning_trades': 0,
                'losing_trades': 0,
                'winrate': 0.0,
                'total_pnl': 0.0,
                'gross_profit': 0.0,
                'gross_loss': 0.0,
                'profit_factor': 0.0,
                'avg_win': 0.0,
                'avg_loss': 0.0
            }
        
        total_trades = len(self.closed_positions)
        winning_trades = sum(1 for p in self.closed_positions if p.pnl > 0)
        losing_trades = sum(1 for p in self.closed_positions if p.pnl < 0)
        
        winrate = (winning_trades / total_trades * 100) if total_trades > 0 else 0.0
        
        total_pnl = sum(p.pnl for p in self.closed_positions)
        gross_profit = sum(p.pnl for p in self.closed_positions if p.pnl > 0)
        gross_loss = abs(sum(p.pnl for p in self.closed_positions if p.pnl < 0))
        
        profit_factor = (gross_profit / gross_loss) if gross_loss > 0 else 0.0
        
        wins = [p.pnl for p in self.closed_positions if p.pnl > 0]
        losses = [p.pnl for p in self.closed_positions if p.pnl < 0]
        
        avg_win = np.mean(wins) if wins else 0.0
        avg_loss = np.mean(losses) if losses else 0.0
        
        return {
            'timeframe': self.timeframe,
            'total_trades': total_trades,
            'winning_trades': winning_trades,
            'losing_trades': losing_trades,
            'winrate': winrate,
            'total_pnl': total_pnl,
            'gross_profit': gross_profit,
            'gross_loss': gross_loss,
            'profit_factor': profit_factor,
            'avg_win': avg_win,
            'avg_loss': avg_loss
        }
    
    def get_trade_log(self) -> pd.DataFrame:
        """Return detailed trade log as DataFrame"""
        if not self.closed_positions:
            return pd.DataFrame()
        
        trades = []
        for pos in self.closed_positions:
            trades.append({
                'Entry Time': pos.entry_time,
                'Exit Time': pos.exit_time,
                'Type': pos.position_type,
                'Entry Price': pos.entry_price,
                'Exit Price': pos.exit_price,
                'Stop Loss': pos.stop_loss,
                'Take Profit': pos.take_profit,
                'Exit Reason': pos.exit_reason,
                'PnL (points)': pos.pnl
            })
        
        return pd.DataFrame(trades)


def load_csv_data(file_pattern: str) -> pd.DataFrame:
    """Load and combine CSV files matching the pattern"""
    files = sorted(glob.glob(file_pattern))
    
    if not files:
        raise FileNotFoundError(f"No files found matching pattern: {file_pattern}")
    
    print(f"Loading files: {files}")
    
    dfs = []
    for file in files:
        df = pd.read_csv(file, sep=';')
        # Skip header row if it contains 'Column1'
        if df.iloc[0, 0] == 'Column1':
            df = df.iloc[1:].reset_index(drop=True)
        
        # Rename columns
        df.columns = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
        
        # Convert price columns to float
        for col in ['Open', 'High', 'Low', 'Close']:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        dfs.append(df)
    
    combined_df = pd.concat(dfs, ignore_index=True)
    
    # Remove any rows with NaN values
    combined_df = combined_df.dropna(subset=['Open', 'High', 'Low', 'Close'])
    
    print(f"Loaded {len(combined_df)} candles from {len(files)} file(s)")
    
    return combined_df


def print_comparison_table(results_5m: Dict, results_15m: Dict):
    """Print formatted comparison table"""
    print("\n" + "="*80)
    print("FVG INVERSE STRATEGY BACKTEST RESULTS")
    print("="*80)
    print(f"\n{'Metric':<30} {'5-Minute':<20} {'15-Minute':<20}")
    print("-"*80)
    print(f"{'Total Trades':<30} {results_5m['total_trades']:<20} {results_15m['total_trades']:<20}")
    print(f"{'Winning Trades':<30} {results_5m['winning_trades']:<20} {results_15m['winning_trades']:<20}")
    print(f"{'Losing Trades':<30} {results_5m['losing_trades']:<20} {results_15m['losing_trades']:<20}")
    print(f"{'Winrate (%)':<30} {results_5m['winrate']:<20.2f} {results_15m['winrate']:<20.2f}")
    print(f"{'Total P&L (points)':<30} {results_5m['total_pnl']:<20.2f} {results_15m['total_pnl']:<20.2f}")
    print(f"{'Gross Profit (points)':<30} {results_5m['gross_profit']:<20.2f} {results_15m['gross_profit']:<20.2f}")
    print(f"{'Gross Loss (points)':<30} {results_5m['gross_loss']:<20.2f} {results_15m['gross_loss']:<20.2f}")
    print(f"{'Profit Factor':<30} {results_5m['profit_factor']:<20.2f} {results_15m['profit_factor']:<20.2f}")
    print(f"{'Average Win (points)':<30} {results_5m['avg_win']:<20.2f} {results_15m['avg_win']:<20.2f}")
    print(f"{'Average Loss (points)':<30} {results_5m['avg_loss']:<20.2f} {results_15m['avg_loss']:<20.2f}")
    print("="*80)


def main():
    """Main execution function"""
    import os
    
    # Set working directory to script location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    print("FVG Inverse Trading Strategy Backtest")
    print("="*80)
    
    # Load 5-minute data
    print("\n[1/4] Loading 5-minute data...")
    df_5m = load_csv_data("[0-9][0-9][0-9][0-9] 5m.csv")
    
    # Load 15-minute data
    print("\n[2/4] Loading 15-minute data...")
    df_15m = load_csv_data("[0-9][0-9][0-9][0-9] 15m.csv")
    
    # Run backtest on 5-minute data
    print("\n[3/4] Running backtest on 5-minute data...")
    backtester_5m = FVGInverseBacktester(df_5m, "5-Minute")
    results_5m = backtester_5m.run_backtest()
    
    # Run backtest on 15-minute data
    print("\n[4/4] Running backtest on 15-minute data...")
    backtester_15m = FVGInverseBacktester(df_15m, "15-Minute")
    results_15m = backtester_15m.run_backtest()
    
    # Print comparison table
    print_comparison_table(results_5m, results_15m)
    
    # Optional: Save trade logs
    print("\nSaving trade logs...")
    trade_log_5m = backtester_5m.get_trade_log()
    trade_log_15m = backtester_15m.get_trade_log()
    
    if not trade_log_5m.empty:
        trade_log_5m.to_csv('fvg_inverse_trades_5m.csv', index=False)
        print(f"5-minute trade log saved to 'fvg_inverse_trades_5m.csv' ({len(trade_log_5m)} trades)")
    
    if not trade_log_15m.empty:
        trade_log_15m.to_csv('fvg_inverse_trades_15m.csv', index=False)
        print(f"15-minute trade log saved to 'fvg_inverse_trades_15m.csv' ({len(trade_log_15m)} trades)")
    
    print("\nBacktest complete!")


if __name__ == "__main__":
    main()

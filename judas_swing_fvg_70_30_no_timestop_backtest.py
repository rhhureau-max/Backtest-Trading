"""
Judas Swing + FVG Inversion Backtesting Script - 70/30 Partial Exit Strategy (NO TIME STOP)
============================================================================================
This script backtests the "Judas Swing + FVG Inversion" strategy with 70/30 partial exits:
- SL: 0.5 points beyond Tokyo (Asia) levels
- TP Strategy: 70% at Equilibrium + 30% at Opposite (with breakeven SL after first TP)
- NO TIME STOP: Trades run until they hit TP or SL (no 12:00 exit)

Strategy Overview:
- Identifies Asia session highs/lows (18:00-23:00 previous day) - "Tokyo session"
- During London Killzone (01:00-04:00), looks for:
  * LONG: Price breaks below Asia_Low, bearish FVG forms, then price closes above FVG high
  * SHORT: Price breaks above Asia_High, bullish FVG forms, then price closes below FVG low
- One trade per day maximum
- 70% exits at equilibrium, 30% aims for opposite level with breakeven protection
- Trades continue until TP1, TP2, SL, or breakeven hit (no time-based exit)
"""

import pandas as pd
import numpy as np
from datetime import datetime, time, timedelta
from typing import Dict, List, Tuple
import warnings

warnings.filterwarnings('ignore')


class JudasSwingFVG70_30NoTimestopBacktest:
    """Backtesting class with 70/30 partial exit strategy - NO TIME STOP"""
    
    def __init__(self, csv_file: str):
        """
        Initialize the backtest
        
        Args:
            csv_file: Path to CSV file with 5-minute OHLCV data
        """
        self.csv_file = csv_file
        self.df = None
        
    def load_data(self) -> bool:
        """Load and prepare the CSV data"""
        try:
            self.df = pd.read_csv(
                self.csv_file,
                sep=';',
                header=0,
                names=['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
            )
            
            self.df['Date'] = pd.to_datetime(self.df['Date'], format='%d/%m/%Y', errors='coerce')
            self.df['Time'] = pd.to_datetime(self.df['Time'], format='%H:%M:%S', errors='coerce').dt.time
            self.df['DateTime'] = pd.to_datetime(
                self.df['Date'].astype(str) + ' ' + self.df['Time'].astype(str)
            )
            
            for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
                self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
            
            self.df = self.df.dropna()
            self.df = self.df.sort_values('DateTime').reset_index(drop=True)
            
            print(f"✓ Loaded {len(self.df)} candles from {self.csv_file}")
            print(f"  Date range: {self.df['Date'].min()} to {self.df['Date'].max()}")
            
            return len(self.df) > 0
            
        except Exception as e:
            print(f"✗ Error loading data: {e}")
            return False
    
    def identify_asia_session(self, current_date: pd.Timestamp) -> Tuple[float, float]:
        """Identify Asia session high and low"""
        prev_date = current_date - timedelta(days=1)
        
        asia_mask = (
            (self.df['Date'] == prev_date) &
            (self.df['Time'] >= time(18, 0)) &
            (self.df['Time'] <= time(23, 0))
        )
        
        asia_candles = self.df[asia_mask]
        
        if len(asia_candles) == 0:
            return None, None
        
        asia_high = asia_candles['High'].max()
        asia_low = asia_candles['Low'].min()
        
        return asia_high, asia_low
    
    def detect_bearish_fvg(self, idx: int) -> Tuple[bool, float, float]:
        """Detect bearish Fair Value Gap"""
        if idx < 2:
            return False, None, None
        
        high_n_minus_2 = self.df.loc[idx - 2, 'High']
        low_n = self.df.loc[idx, 'Low']
        
        if high_n_minus_2 < low_n:
            return True, low_n, high_n_minus_2
        
        return False, None, None
    
    def detect_bullish_fvg(self, idx: int) -> Tuple[bool, float, float]:
        """Detect bullish Fair Value Gap"""
        if idx < 2:
            return False, None, None
        
        low_n_minus_2 = self.df.loc[idx - 2, 'Low']
        high_n = self.df.loc[idx, 'High']
        
        if low_n_minus_2 > high_n:
            return True, low_n_minus_2, high_n
        
        return False, None, None
    
    def manage_trade_70_30_partial(self, entry_idx: int, entry_price: float, direction: str,
                                   sl_level: float, tp1_level: float, tp2_level: float) -> Dict:
        """Manage trade with 70/30 partial exits (70% at TP1, 30% at TP2, breakeven after TP1) - NO TIME STOP"""
        if direction == 'LONG':
            sl_points = entry_price - sl_level
            tp1_points = tp1_level - entry_price
            tp2_points = tp2_level - entry_price
        else:
            sl_points = sl_level - entry_price
            tp1_points = entry_price - tp1_level
            tp2_points = entry_price - tp2_level
        
        tp1_hit = False
        tp1_pnl = 0
        current_sl = sl_level
        
        for idx in range(entry_idx + 1, len(self.df)):
            candle = self.df.loc[idx]
            
            # Check TP1 first (equilibrium) - 70% exit
            if not tp1_hit:
                if direction == 'LONG':
                    if candle['High'] >= tp1_level:
                        # 70% exit at TP1
                        tp1_pnl = tp1_points * 0.7
                        tp1_hit = True
                        current_sl = entry_price  # Move SL to breakeven
                        continue
                else:  # SHORT
                    if candle['Low'] <= tp1_level:
                        tp1_pnl = tp1_points * 0.7
                        tp1_hit = True
                        current_sl = entry_price
                        continue
            
            # Check SL (breakeven after TP1 hit)
            if direction == 'LONG':
                if candle['Low'] <= current_sl:
                    if tp1_hit:
                        # 70% already closed at TP1, remaining 30% at breakeven
                        total_pnl = tp1_pnl + 0  # Breakeven on remaining
                    else:
                        # Full position stopped out
                        total_pnl = -sl_points
                    
                    return {
                        'exit_type': 'SL' + (' (Breakeven)' if tp1_hit else ''),
                        'exit_price': current_sl,
                        'pnl': total_pnl,
                        'sl_points': sl_points,
                        'tp_points': (tp1_points + tp2_points) / 2,
                        'tp1_hit': tp1_hit
                    }
            else:  # SHORT
                if candle['High'] >= current_sl:
                    if tp1_hit:
                        total_pnl = tp1_pnl + 0
                    else:
                        total_pnl = -sl_points
                    
                    return {
                        'exit_type': 'SL' + (' (Breakeven)' if tp1_hit else ''),
                        'exit_price': current_sl,
                        'pnl': total_pnl,
                        'sl_points': sl_points,
                        'tp_points': (tp1_points + tp2_points) / 2,
                        'tp1_hit': tp1_hit
                    }
            
            # Check TP2 (opposite level) - 30% exit
            if tp1_hit:
                if direction == 'LONG':
                    if candle['High'] >= tp2_level:
                        # 70% already at TP1, 30% at TP2
                        tp2_pnl = tp2_points * 0.3
                        total_pnl = tp1_pnl + tp2_pnl
                        return {
                            'exit_type': 'TP2',
                            'exit_price': tp2_level,
                            'pnl': total_pnl,
                            'sl_points': sl_points,
                            'tp_points': (tp1_points + tp2_points) / 2,
                            'tp1_hit': True
                        }
                else:  # SHORT
                    if candle['Low'] <= tp2_level:
                        tp2_pnl = tp2_points * 0.3
                        total_pnl = tp1_pnl + tp2_pnl
                        return {
                            'exit_type': 'TP2',
                            'exit_price': tp2_level,
                            'pnl': total_pnl,
                            'sl_points': sl_points,
                            'tp_points': (tp1_points + tp2_points) / 2,
                            'tp1_hit': True
                        }
        
        # Close at last candle if end of data reached (shouldn't happen with NO TIME STOP)
        last_candle = self.df.iloc[-1]
        exit_price = last_candle['Close']
        if tp1_hit:
            remaining_pnl = ((exit_price - entry_price) if direction == 'LONG' else (entry_price - exit_price)) * 0.3
            total_pnl = tp1_pnl + remaining_pnl
        else:
            total_pnl = (exit_price - entry_price) if direction == 'LONG' else (entry_price - exit_price)
        
        return {
            'exit_type': 'END_OF_DATA' + (' (Partial)' if tp1_hit else ''),
            'exit_price': exit_price,
            'pnl': total_pnl,
            'sl_points': sl_points,
            'tp_points': (tp1_points + tp2_points) / 2,
            'tp1_hit': tp1_hit
        }
    
    def run_backtest(self) -> Dict:
        """Run the complete backtest"""
        trades = []
        traded_dates = set()
        
        unique_dates = self.df['Date'].unique()
        
        for current_date in unique_dates:
            if current_date in traded_dates:
                continue
            
            asia_high, asia_low = self.identify_asia_session(current_date)
            
            if asia_high is None or asia_low is None:
                continue
            
            equilibrium = (asia_high + asia_low) / 2
            
            london_mask = (
                (self.df['Date'] == current_date) &
                (self.df['Time'] >= time(1, 0)) &
                (self.df['Time'] <= time(4, 0))
            )
            
            london_indices = self.df[london_mask].index.tolist()
            
            if len(london_indices) == 0:
                continue
            
            breached_asia_low = False
            breached_asia_high = False
            
            for idx in london_indices:
                if idx < 2:
                    continue
                
                candle = self.df.loc[idx]
                
                if candle['Low'] < asia_low:
                    breached_asia_low = True
                
                if candle['High'] > asia_high:
                    breached_asia_high = True
                
                # LONG Setup
                if breached_asia_low and not breached_asia_high:
                    fvg_exists, fvg_high, fvg_low = self.detect_bearish_fvg(idx)
                    
                    if fvg_exists and candle['Close'] > fvg_high:
                        entry_price = candle['Close']
                        sl_level = asia_low - 0.5
                        tp1_level = equilibrium
                        tp2_level = asia_high
                        
                        trade_result = self.manage_trade_70_30_partial(idx, entry_price, 'LONG', sl_level, tp1_level, tp2_level)
                        
                        trades.append({
                            'date': current_date,
                            'entry_time': candle['Time'],
                            'direction': 'LONG',
                            'entry_price': entry_price,
                            'asia_high': asia_high,
                            'asia_low': asia_low,
                            'equilibrium': equilibrium,
                            'fvg_high': fvg_high,
                            'fvg_low': fvg_low,
                            'sl_level': sl_level,
                            **trade_result
                        })
                        
                        traded_dates.add(current_date)
                        break
                
                # SHORT Setup
                if breached_asia_high and not breached_asia_low:
                    fvg_exists, fvg_high, fvg_low = self.detect_bullish_fvg(idx)
                    
                    if fvg_exists and candle['Close'] < fvg_low:
                        entry_price = candle['Close']
                        sl_level = asia_high + 0.5
                        tp1_level = equilibrium
                        tp2_level = asia_low
                        
                        trade_result = self.manage_trade_70_30_partial(idx, entry_price, 'SHORT', sl_level, tp1_level, tp2_level)
                        
                        trades.append({
                            'date': current_date,
                            'entry_time': candle['Time'],
                            'direction': 'SHORT',
                            'entry_price': entry_price,
                            'asia_high': asia_high,
                            'asia_low': asia_low,
                            'equilibrium': equilibrium,
                            'fvg_high': fvg_high,
                            'fvg_low': fvg_low,
                            'sl_level': sl_level,
                            **trade_result
                        })
                        
                        traded_dates.add(current_date)
                        break
        
        # Calculate statistics
        if len(trades) == 0:
            return {
                'total_trades': 0,
                'win_rate': 0,
                'net_profit': 0,
                'profit_factor': 0,
                'max_drawdown': 0,
                'trades': []
            }
        
        trades_df = pd.DataFrame(trades)
        
        total_trades = len(trades_df)
        winning_trades = trades_df[trades_df['pnl'] > 0]
        losing_trades = trades_df[trades_df['pnl'] < 0]
        
        win_rate = (len(winning_trades) / total_trades * 100) if total_trades > 0 else 0
        
        gross_profit = winning_trades['pnl'].sum() if len(winning_trades) > 0 else 0
        gross_loss = abs(losing_trades['pnl'].sum()) if len(losing_trades) > 0 else 0
        net_profit = trades_df['pnl'].sum()
        
        profit_factor = (gross_profit / gross_loss) if gross_loss > 0 else 0
        
        cumulative_pnl = trades_df['pnl'].cumsum()
        running_max = cumulative_pnl.cummax()
        drawdown = running_max - cumulative_pnl
        max_drawdown = drawdown.max()
        
        return {
            'total_trades': total_trades,
            'win_rate': win_rate,
            'net_profit': net_profit,
            'profit_factor': profit_factor,
            'max_drawdown': max_drawdown,
            'trades': trades_df.to_dict('records')
        }


def run_backtest(csv_file: str) -> Dict:
    """Convenience function to run backtest"""
    backtest = JudasSwingFVG70_30NoTimestopBacktest(csv_file)
    
    if not backtest.load_data():
        return None
    
    results = backtest.run_backtest()
    
    return results


def main():
    """Main function to run backtest and display results"""
    import glob
    
    csv_files = sorted(glob.glob("*5m.csv"))
    
    if not csv_files:
        print("No 5m CSV files found in current directory")
        return
    
    print("="*80)
    print("JUDAS SWING + FVG INVERSION - 70/30 PARTIAL EXIT (NO TIME STOP)")
    print("="*80)
    print()
    print("Strategy Configuration:")
    print("  - SL: 0.5 points beyond Tokyo levels")
    print("  - TP Strategy: 70% at Equilibrium + 30% at Opposite")
    print("  - Breakeven: SL moves to entry price after 70% exits at equilibrium")
    print("  - NO TIME STOP: Trades run until TP or SL hit")
    print()
    print("="*80)
    print()
    
    test_file = csv_files[0] if len(csv_files) > 0 else None
    
    if test_file:
        print(f"Testing file: {test_file}\n")
        
        results = run_backtest(test_file)
        
        if results:
            print()
            print(f"Total Trades: {results['total_trades']}")
            print(f"Win Rate: {results['win_rate']:.2f}%")
            print(f"Net Profit: {results['net_profit']:.2f} points")
            print(f"Profit Factor: {results['profit_factor']:.2f}")
            print(f"Max Drawdown: {results['max_drawdown']:.2f} points")


if __name__ == "__main__":
    main()

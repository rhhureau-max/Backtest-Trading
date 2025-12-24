"""
Judas Swing + FVG Inversion Backtesting Script - Multiple TP Strategies
=======================================================================
This script backtests the "Judas Swing + FVG Inversion" strategy with different TP strategies:
- SL: 0.5 points beyond Tokyo (Asia) levels (same as fixed R:R)
- TP Options:
  1. 100% at Equilibrium
  2. 100% at Opposite Tokyo level
  3. 50% at Equilibrium + 50% at Opposite (with breakeven SL after first TP)

Strategy Overview:
- Identifies Asia session highs/lows (18:00-23:00 previous day) - "Tokyo session"
- During London Killzone (01:00-04:00), looks for:
  * LONG: Price breaks below Asia_Low, bearish FVG forms, then price closes above FVG high
  * SHORT: Price breaks above Asia_High, bullish FVG forms, then price closes below FVG low
- One trade per day maximum
"""

import pandas as pd
import numpy as np
from datetime import datetime, time, timedelta
from typing import Dict, List, Tuple
import warnings

warnings.filterwarnings('ignore')


class JudasSwingFVGMultiTPBacktest:
    """Backtesting class with multiple TP strategies"""
    
    def __init__(self, csv_file: str, tp_strategy: str = 'equilibrium'):
        """
        Initialize the backtest
        
        Args:
            csv_file: Path to CSV file with 5-minute OHLCV data
            tp_strategy: TP strategy ('equilibrium', 'opposite', 'partial')
        """
        self.csv_file = csv_file
        self.tp_strategy = tp_strategy
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
    
    def manage_trade_full_exit(self, entry_idx: int, entry_price: float, direction: str, 
                               sl_level: float, tp_level: float) -> Dict:
        """Manage trade with single full exit at TP"""
        if direction == 'LONG':
            sl_points = entry_price - sl_level
            tp_points = tp_level - entry_price
        else:
            sl_points = sl_level - entry_price
            tp_points = entry_price - tp_level
        
        entry_date = self.df.loc[entry_idx, 'Date']
        time_stop = time(12, 0)
        
        for idx in range(entry_idx + 1, len(self.df)):
            candle = self.df.loc[idx]
            current_date = candle['Date']
            current_time = candle['Time']
            
            # Time stop check
            if current_date == entry_date and current_time >= time_stop:
                exit_price = candle['Close']
                pnl = (exit_price - entry_price) if direction == 'LONG' else (entry_price - exit_price)
                return {
                    'exit_type': 'TIME_STOP',
                    'exit_price': exit_price,
                    'pnl': pnl,
                    'sl_points': sl_points,
                    'tp_points': tp_points
                }
            
            if current_date > entry_date:
                exit_price = candle['Close']
                pnl = (exit_price - entry_price) if direction == 'LONG' else (entry_price - exit_price)
                return {
                    'exit_type': 'TIME_STOP',
                    'exit_price': exit_price,
                    'pnl': pnl,
                    'sl_points': sl_points,
                    'tp_points': tp_points
                }
            
            # Check SL and TP
            if direction == 'LONG':
                if candle['Low'] <= sl_level:
                    return {
                        'exit_type': 'SL',
                        'exit_price': sl_level,
                        'pnl': -sl_points,
                        'sl_points': sl_points,
                        'tp_points': tp_points
                    }
                if candle['High'] >= tp_level:
                    return {
                        'exit_type': 'TP',
                        'exit_price': tp_level,
                        'pnl': tp_points,
                        'sl_points': sl_points,
                        'tp_points': tp_points
                    }
            else:  # SHORT
                if candle['High'] >= sl_level:
                    return {
                        'exit_type': 'SL',
                        'exit_price': sl_level,
                        'pnl': -sl_points,
                        'sl_points': sl_points,
                        'tp_points': tp_points
                    }
                if candle['Low'] <= tp_level:
                    return {
                        'exit_type': 'TP',
                        'exit_price': tp_level,
                        'pnl': tp_points,
                        'sl_points': sl_points,
                        'tp_points': tp_points
                    }
        
        # Close at last candle
        last_candle = self.df.iloc[-1]
        exit_price = last_candle['Close']
        pnl = (exit_price - entry_price) if direction == 'LONG' else (entry_price - exit_price)
        
        return {
            'exit_type': 'TIME_STOP',
            'exit_price': exit_price,
            'pnl': pnl,
            'sl_points': sl_points,
            'tp_points': tp_points
        }
    
    def manage_trade_partial_exit(self, entry_idx: int, entry_price: float, direction: str,
                                  sl_level: float, tp1_level: float, tp2_level: float) -> Dict:
        """Manage trade with partial exits (50% at TP1, 50% at TP2, breakeven after TP1)"""
        if direction == 'LONG':
            sl_points = entry_price - sl_level
            tp1_points = tp1_level - entry_price
            tp2_points = tp2_level - entry_price
        else:
            sl_points = sl_level - entry_price
            tp1_points = entry_price - tp1_level
            tp2_points = entry_price - tp2_level
        
        entry_date = self.df.loc[entry_idx, 'Date']
        time_stop = time(12, 0)
        
        tp1_hit = False
        tp1_pnl = 0
        current_sl = sl_level
        
        for idx in range(entry_idx + 1, len(self.df)):
            candle = self.df.loc[idx]
            current_date = candle['Date']
            current_time = candle['Time']
            
            # Time stop check
            if current_date == entry_date and current_time >= time_stop:
                exit_price = candle['Close']
                if tp1_hit:
                    # 50% already closed at TP1, close remaining 50%
                    remaining_pnl = ((exit_price - entry_price) if direction == 'LONG' else (entry_price - exit_price)) * 0.5
                    total_pnl = tp1_pnl + remaining_pnl
                else:
                    # No TP hit, close 100%
                    total_pnl = (exit_price - entry_price) if direction == 'LONG' else (entry_price - exit_price)
                
                return {
                    'exit_type': 'TIME_STOP' + (' (Partial)' if tp1_hit else ''),
                    'exit_price': exit_price,
                    'pnl': total_pnl,
                    'sl_points': sl_points,
                    'tp_points': (tp1_points + tp2_points) / 2,
                    'tp1_hit': tp1_hit
                }
            
            if current_date > entry_date:
                exit_price = candle['Close']
                if tp1_hit:
                    remaining_pnl = ((exit_price - entry_price) if direction == 'LONG' else (entry_price - exit_price)) * 0.5
                    total_pnl = tp1_pnl + remaining_pnl
                else:
                    total_pnl = (exit_price - entry_price) if direction == 'LONG' else (entry_price - exit_price)
                
                return {
                    'exit_type': 'TIME_STOP' + (' (Partial)' if tp1_hit else ''),
                    'exit_price': exit_price,
                    'pnl': total_pnl,
                    'sl_points': sl_points,
                    'tp_points': (tp1_points + tp2_points) / 2,
                    'tp1_hit': tp1_hit
                }
            
            # Check TP1 first (equilibrium)
            if not tp1_hit:
                if direction == 'LONG':
                    if candle['High'] >= tp1_level:
                        # 50% exit at TP1
                        tp1_pnl = tp1_points * 0.5
                        tp1_hit = True
                        current_sl = entry_price  # Move SL to breakeven
                        continue
                else:  # SHORT
                    if candle['Low'] <= tp1_level:
                        tp1_pnl = tp1_points * 0.5
                        tp1_hit = True
                        current_sl = entry_price
                        continue
            
            # Check SL (breakeven after TP1 hit)
            if direction == 'LONG':
                if candle['Low'] <= current_sl:
                    if tp1_hit:
                        # 50% already closed at TP1, remaining 50% at breakeven
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
            
            # Check TP2 (opposite level)
            if tp1_hit:
                if direction == 'LONG':
                    if candle['High'] >= tp2_level:
                        # 50% already at TP1, 50% at TP2
                        tp2_pnl = tp2_points * 0.5
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
                        tp2_pnl = tp2_points * 0.5
                        total_pnl = tp1_pnl + tp2_pnl
                        return {
                            'exit_type': 'TP2',
                            'exit_price': tp2_level,
                            'pnl': total_pnl,
                            'sl_points': sl_points,
                            'tp_points': (tp1_points + tp2_points) / 2,
                            'tp1_hit': True
                        }
        
        # Close at last candle
        last_candle = self.df.iloc[-1]
        exit_price = last_candle['Close']
        if tp1_hit:
            remaining_pnl = ((exit_price - entry_price) if direction == 'LONG' else (entry_price - exit_price)) * 0.5
            total_pnl = tp1_pnl + remaining_pnl
        else:
            total_pnl = (exit_price - entry_price) if direction == 'LONG' else (entry_price - exit_price)
        
        return {
            'exit_type': 'TIME_STOP' + (' (Partial)' if tp1_hit else ''),
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
                        
                        if self.tp_strategy == 'equilibrium':
                            tp_level = equilibrium
                            trade_result = self.manage_trade_full_exit(idx, entry_price, 'LONG', sl_level, tp_level)
                        elif self.tp_strategy == 'opposite':
                            tp_level = asia_high
                            trade_result = self.manage_trade_full_exit(idx, entry_price, 'LONG', sl_level, tp_level)
                        else:  # partial
                            tp1_level = equilibrium
                            tp2_level = asia_high
                            trade_result = self.manage_trade_partial_exit(idx, entry_price, 'LONG', sl_level, tp1_level, tp2_level)
                        
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
                            'tp_strategy': self.tp_strategy,
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
                        
                        if self.tp_strategy == 'equilibrium':
                            tp_level = equilibrium
                            trade_result = self.manage_trade_full_exit(idx, entry_price, 'SHORT', sl_level, tp_level)
                        elif self.tp_strategy == 'opposite':
                            tp_level = asia_low
                            trade_result = self.manage_trade_full_exit(idx, entry_price, 'SHORT', sl_level, tp_level)
                        else:  # partial
                            tp1_level = equilibrium
                            tp2_level = asia_low
                            trade_result = self.manage_trade_partial_exit(idx, entry_price, 'SHORT', sl_level, tp1_level, tp2_level)
                        
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
                            'tp_strategy': self.tp_strategy,
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
                'tp_strategy': self.tp_strategy,
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
            'tp_strategy': self.tp_strategy,
            'trades': trades_df.to_dict('records')
        }


def run_backtest(csv_file: str, tp_strategy: str) -> Dict:
    """Convenience function to run backtest"""
    backtest = JudasSwingFVGMultiTPBacktest(csv_file, tp_strategy)
    
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
    print("JUDAS SWING + FVG INVERSION - MULTIPLE TP STRATEGIES BACKTEST")
    print("="*80)
    print()
    print("Strategy Configuration:")
    print("  - SL: 0.5 points beyond Tokyo levels (same as before)")
    print("  - TP Strategies:")
    print("    1. Equilibrium: 100% exit at equilibrium")
    print("    2. Opposite: 100% exit at opposite Tokyo level")
    print("    3. Partial: 50% at equilibrium, 50% at opposite (SL to breakeven after first TP)")
    print()
    print("="*80)
    print()
    
    test_file = csv_files[0] if len(csv_files) > 0 else None
    
    if test_file:
        print(f"Testing file: {test_file}\n")
        
        strategies = ['equilibrium', 'opposite', 'partial']
        strategy_names = {
            'equilibrium': '100% at Equilibrium',
            'opposite': '100% at Opposite Tokyo Level',
            'partial': '50% Equilibrium + 50% Opposite'
        }
        
        for strategy in strategies:
            print(f"\n{'─'*80}")
            print(f"Testing Strategy: {strategy_names[strategy]}")
            print('─'*80)
            
            results = run_backtest(test_file, strategy)
            
            if results:
                print()
                print(f"Total Trades: {results['total_trades']}")
                print(f"Win Rate: {results['win_rate']:.2f}%")
                print(f"Net Profit: {results['net_profit']:.2f} points")
                print(f"Profit Factor: {results['profit_factor']:.2f}")
                print(f"Max Drawdown: {results['max_drawdown']:.2f} points")


if __name__ == "__main__":
    main()

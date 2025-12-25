"""
Judas Swing + FVG Inversion Backtesting Script - Fixed R:R Version
==================================================================
This script backtests the "Judas Swing + FVG Inversion" strategy with fixed risk/reward ratios:
- SL placed 0.5 points beyond Asia High (for SHORT) or below Asia Low (for LONG)
- TP calculated based on fixed R:R ratios: 1:1, 1:1.5, and 1:2

Strategy Overview:
- Identifies Asia session highs/lows (18:00-23:00 previous day) - "Tokyo session"
- During London Killzone (01:00-04:00), looks for:
  * LONG: Price breaks below Asia_Low, bearish FVG forms, then price closes above FVG high
  * SHORT: Price breaks above Asia_High, bullish FVG forms, then price closes below FVG low
- One trade per day maximum
- SL: 0.5 points beyond Asia levels, TP: Based on fixed R:R ratios
"""

import pandas as pd
import numpy as np
from datetime import datetime, time, timedelta
from typing import Dict, List, Tuple
import warnings

warnings.filterwarnings('ignore')


class JudasSwingFVGFixedRRBacktest:
    """Backtesting class with fixed R:R ratios"""
    
    def __init__(self, csv_file: str, rr_ratio: float = 1.0):
        """
        Initialize the backtest
        
        Args:
            csv_file: Path to CSV file with 5-minute OHLCV data
            rr_ratio: Risk/Reward ratio (1.0, 1.5, or 2.0)
        """
        self.csv_file = csv_file
        self.rr_ratio = rr_ratio
        self.df = None
        
    def load_data(self) -> bool:
        """
        Load and prepare the CSV data
        
        Returns:
            True if data loaded successfully, False otherwise
        """
        try:
            # Load CSV with semicolon separator
            self.df = pd.read_csv(
                self.csv_file,
                sep=';',
                header=0,
                names=['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
            )
            
            # Convert data types
            self.df['Date'] = pd.to_datetime(self.df['Date'], format='%d/%m/%Y', errors='coerce')
            self.df['Time'] = pd.to_datetime(self.df['Time'], format='%H:%M:%S', errors='coerce').dt.time
            
            # Create datetime column
            self.df['DateTime'] = pd.to_datetime(
                self.df['Date'].astype(str) + ' ' + self.df['Time'].astype(str)
            )
            
            # Convert OHLC to numeric
            for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
                self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
            
            # Remove rows with missing data
            self.df = self.df.dropna()
            
            # Sort by datetime
            self.df = self.df.sort_values('DateTime').reset_index(drop=True)
            
            print(f"✓ Loaded {len(self.df)} candles from {self.csv_file}")
            print(f"  Date range: {self.df['Date'].min()} to {self.df['Date'].max()}")
            
            return len(self.df) > 0
            
        except Exception as e:
            print(f"✗ Error loading data: {e}")
            return False
    
    def identify_asia_session(self, current_date: pd.Timestamp) -> Tuple[float, float]:
        """
        Identify Asia session high and low for a given date
        Asia session: 18:00 (previous day) to 23:00 (previous day) Chicago time
        
        Args:
            current_date: The current trading date
            
        Returns:
            Tuple of (asia_high, asia_low)
        """
        # Get previous day
        prev_date = current_date - timedelta(days=1)
        
        # Filter Asia session candles (18:00 to 23:00 on previous day)
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
        """
        Detect bearish Fair Value Gap (FVG)
        Bearish FVG: Gap between high of candle n-2 and low of candle n
        
        Args:
            idx: Current candle index
            
        Returns:
            Tuple of (fvg_exists, fvg_high, fvg_low)
        """
        if idx < 2:
            return False, None, None
        
        # Bearish FVG: high[n-2] < low[n]
        high_n_minus_2 = self.df.loc[idx - 2, 'High']
        low_n = self.df.loc[idx, 'Low']
        
        if high_n_minus_2 < low_n:
            # Gap exists
            return True, low_n, high_n_minus_2
        
        return False, None, None
    
    def detect_bullish_fvg(self, idx: int) -> Tuple[bool, float, float]:
        """
        Detect bullish Fair Value Gap (FVG)
        Bullish FVG: Gap between low of candle n-2 and high of candle n
        
        Args:
            idx: Current candle index
            
        Returns:
            Tuple of (fvg_exists, fvg_high, fvg_low)
        """
        if idx < 2:
            return False, None, None
        
        # Bullish FVG: low[n-2] > high[n]
        low_n_minus_2 = self.df.loc[idx - 2, 'Low']
        high_n = self.df.loc[idx, 'High']
        
        if low_n_minus_2 > high_n:
            # Gap exists
            return True, low_n_minus_2, high_n
        
        return False, None, None
    
    def manage_trade(self, entry_idx: int, entry_price: float, direction: str, 
                     sl_level: float, tp_level: float) -> Dict:
        """
        Manage an open trade until exit
        
        Args:
            entry_idx: Index of entry candle
            entry_price: Entry price
            direction: 'LONG' or 'SHORT'
            sl_level: Stop loss price level
            tp_level: Take profit price level
            
        Returns:
            Dictionary with trade results
        """
        # Calculate SL and TP distances
        if direction == 'LONG':
            sl_points = entry_price - sl_level
            tp_points = tp_level - entry_price
        else:  # SHORT
            sl_points = sl_level - entry_price
            tp_points = entry_price - tp_level
        
        # Get entry date for time stop (12:00 Chicago)
        entry_date = self.df.loc[entry_idx, 'Date']
        time_stop = time(12, 0)
        
        # Scan subsequent candles
        for idx in range(entry_idx + 1, len(self.df)):
            candle = self.df.loc[idx]
            current_date = candle['Date']
            current_time = candle['Time']
            
            # Check time stop (12:00 on same day)
            if current_date == entry_date and current_time >= time_stop:
                exit_price = candle['Close']
                if direction == 'LONG':
                    pnl = exit_price - entry_price
                else:
                    pnl = entry_price - exit_price
                
                return {
                    'exit_type': 'TIME_STOP',
                    'exit_price': exit_price,
                    'exit_idx': idx,
                    'pnl': pnl,
                    'sl_points': sl_points,
                    'tp_points': tp_points
                }
            
            # Check if we moved to next day (shouldn't happen before time stop)
            if current_date > entry_date:
                exit_price = candle['Close']
                if direction == 'LONG':
                    pnl = exit_price - entry_price
                else:
                    pnl = entry_price - exit_price
                
                return {
                    'exit_type': 'TIME_STOP',
                    'exit_price': exit_price,
                    'exit_idx': idx,
                    'pnl': pnl,
                    'sl_points': sl_points,
                    'tp_points': tp_points
                }
            
            # Check SL and TP hits
            if direction == 'LONG':
                # Check SL hit
                if candle['Low'] <= sl_level:
                    return {
                        'exit_type': 'SL',
                        'exit_price': sl_level,
                        'exit_idx': idx,
                        'pnl': -sl_points,
                        'sl_points': sl_points,
                        'tp_points': tp_points
                    }
                # Check TP hit
                if candle['High'] >= tp_level:
                    return {
                        'exit_type': 'TP',
                        'exit_price': tp_level,
                        'exit_idx': idx,
                        'pnl': tp_points,
                        'sl_points': sl_points,
                        'tp_points': tp_points
                    }
            else:  # SHORT
                # Check SL hit
                if candle['High'] >= sl_level:
                    return {
                        'exit_type': 'SL',
                        'exit_price': sl_level,
                        'exit_idx': idx,
                        'pnl': -sl_points,
                        'sl_points': sl_points,
                        'tp_points': tp_points
                    }
                # Check TP hit
                if candle['Low'] <= tp_level:
                    return {
                        'exit_type': 'TP',
                        'exit_price': tp_level,
                        'exit_idx': idx,
                        'pnl': tp_points,
                        'sl_points': sl_points,
                        'tp_points': tp_points
                    }
        
        # If we reach here, close at last candle
        last_candle = self.df.iloc[-1]
        exit_price = last_candle['Close']
        if direction == 'LONG':
            pnl = exit_price - entry_price
        else:
            pnl = entry_price - exit_price
        
        return {
            'exit_type': 'TIME_STOP',
            'exit_price': exit_price,
            'exit_idx': len(self.df) - 1,
            'pnl': pnl,
            'sl_points': sl_points,
            'tp_points': tp_points
        }
    
    def run_backtest(self) -> Dict:
        """
        Run the complete backtest with fixed R:R ratio
        
        Returns:
            Dictionary with backtest results
        """
        trades = []
        traded_dates = set()  # Track dates we've already traded
        
        # Get unique trading dates
        unique_dates = self.df['Date'].unique()
        
        for current_date in unique_dates:
            # Skip if already traded this date
            if current_date in traded_dates:
                continue
            
            # Get Asia session levels
            asia_high, asia_low = self.identify_asia_session(current_date)
            
            if asia_high is None or asia_low is None:
                continue
            
            # Filter London Killzone candles (01:00 to 04:00 on current date)
            london_mask = (
                (self.df['Date'] == current_date) &
                (self.df['Time'] >= time(1, 0)) &
                (self.df['Time'] <= time(4, 0))
            )
            
            london_indices = self.df[london_mask].index.tolist()
            
            if len(london_indices) == 0:
                continue
            
            # Track if price has breached Asia levels
            breached_asia_low = False
            breached_asia_high = False
            
            # Scan London session for entry signals
            for idx in london_indices:
                if idx < 2:  # Need at least 2 previous candles for FVG
                    continue
                
                candle = self.df.loc[idx]
                
                # Check for Asia low breach
                if candle['Low'] < asia_low:
                    breached_asia_low = True
                
                # Check for Asia high breach
                if candle['High'] > asia_high:
                    breached_asia_high = True
                
                # LONG Setup
                if breached_asia_low and not breached_asia_high:
                    # Check for bearish FVG
                    fvg_exists, fvg_high, fvg_low = self.detect_bearish_fvg(idx)
                    
                    if fvg_exists and candle['Close'] > fvg_high:
                        # Enter LONG
                        entry_price = candle['Close']
                        
                        # SL: 0.5 points below Asia Low
                        sl_level = asia_low - 0.5
                        
                        # Calculate SL distance
                        sl_distance = entry_price - sl_level
                        
                        # TP: Based on R:R ratio
                        tp_level = entry_price + (sl_distance * self.rr_ratio)
                        
                        # Manage trade
                        trade_result = self.manage_trade(idx, entry_price, 'LONG', sl_level, tp_level)
                        
                        # Record trade
                        trades.append({
                            'date': current_date,
                            'entry_time': candle['Time'],
                            'direction': 'LONG',
                            'entry_price': entry_price,
                            'asia_high': asia_high,
                            'asia_low': asia_low,
                            'fvg_high': fvg_high,
                            'fvg_low': fvg_low,
                            'sl_level': sl_level,
                            'tp_level': tp_level,
                            'rr_ratio': self.rr_ratio,
                            **trade_result
                        })
                        
                        traded_dates.add(current_date)
                        break  # Only one trade per day
                
                # SHORT Setup
                if breached_asia_high and not breached_asia_low:
                    # Check for bullish FVG
                    fvg_exists, fvg_high, fvg_low = self.detect_bullish_fvg(idx)
                    
                    if fvg_exists and candle['Close'] < fvg_low:
                        # Enter SHORT
                        entry_price = candle['Close']
                        
                        # SL: 0.5 points above Asia High
                        sl_level = asia_high + 0.5
                        
                        # Calculate SL distance
                        sl_distance = sl_level - entry_price
                        
                        # TP: Based on R:R ratio
                        tp_level = entry_price - (sl_distance * self.rr_ratio)
                        
                        # Manage trade
                        trade_result = self.manage_trade(idx, entry_price, 'SHORT', sl_level, tp_level)
                        
                        # Record trade
                        trades.append({
                            'date': current_date,
                            'entry_time': candle['Time'],
                            'direction': 'SHORT',
                            'entry_price': entry_price,
                            'asia_high': asia_high,
                            'asia_low': asia_low,
                            'fvg_high': fvg_high,
                            'fvg_low': fvg_low,
                            'sl_level': sl_level,
                            'tp_level': tp_level,
                            'rr_ratio': self.rr_ratio,
                            **trade_result
                        })
                        
                        traded_dates.add(current_date)
                        break  # Only one trade per day
        
        # Calculate statistics
        if len(trades) == 0:
            return {
                'total_trades': 0,
                'win_rate': 0,
                'net_profit': 0,
                'profit_factor': 0,
                'max_drawdown': 0,
                'rr_ratio': self.rr_ratio,
                'trades': []
            }
        
        trades_df = pd.DataFrame(trades)
        
        # Calculate metrics
        total_trades = len(trades_df)
        winning_trades = trades_df[trades_df['pnl'] > 0]
        losing_trades = trades_df[trades_df['pnl'] < 0]
        
        win_rate = (len(winning_trades) / total_trades * 100) if total_trades > 0 else 0
        
        gross_profit = winning_trades['pnl'].sum() if len(winning_trades) > 0 else 0
        gross_loss = abs(losing_trades['pnl'].sum()) if len(losing_trades) > 0 else 0
        net_profit = trades_df['pnl'].sum()
        
        profit_factor = (gross_profit / gross_loss) if gross_loss > 0 else 0
        
        # Calculate drawdown
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
            'rr_ratio': self.rr_ratio,
            'trades': trades_df.to_dict('records')
        }


def run_backtest(csv_file: str, rr_ratio: float) -> Dict:
    """
    Convenience function to run backtest with fixed R:R ratio
    
    Args:
        csv_file: Path to CSV file with 5-minute data
        rr_ratio: Risk/Reward ratio (1.0, 1.5, or 2.0)
        
    Returns:
        Dictionary with backtest results
    """
    backtest = JudasSwingFVGFixedRRBacktest(csv_file, rr_ratio)
    
    if not backtest.load_data():
        return None
    
    results = backtest.run_backtest()
    
    return results


def main():
    """Main function to run backtest and display results"""
    import glob
    
    # Find all 5m CSV files
    csv_files = sorted(glob.glob("*5m.csv"))
    
    if not csv_files:
        print("No 5m CSV files found in current directory")
        return
    
    print("="*80)
    print("JUDAS SWING + FVG INVERSION - FIXED R:R STRATEGY BACKTEST")
    print("="*80)
    print()
    print("Strategy Configuration:")
    print("  - SL: 0.5 points beyond Asia High/Low")
    print("  - TP: Based on fixed R:R ratios (1:1, 1:1.5, 1:2)")
    print("  - Time Stop: 12:00 Chicago if neither SL nor TP hit")
    print()
    print("="*80)
    print()
    
    # Test with first available file
    test_file = csv_files[0] if len(csv_files) > 0 else None
    
    if test_file:
        print(f"Testing file: {test_file}\n")
        
        # Test all 3 R:R ratios
        rr_ratios = [1.0, 1.5, 2.0]
        
        for rr in rr_ratios:
            print(f"\n{'─'*80}")
            print(f"Testing R:R Ratio 1:{rr}")
            print('─'*80)
            
            results = run_backtest(test_file, rr)
            
            if results:
                print()
                print(f"Total Trades: {results['total_trades']}")
                print(f"Win Rate: {results['win_rate']:.2f}%")
                print(f"Net Profit: {results['net_profit']:.2f} points")
                print(f"Profit Factor: {results['profit_factor']:.2f}")
                print(f"Max Drawdown: {results['max_drawdown']:.2f} points")


if __name__ == "__main__":
    main()

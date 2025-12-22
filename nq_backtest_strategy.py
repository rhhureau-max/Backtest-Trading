"""
NQ (Nasdaq) 5-Minute Backtesting Strategy
==========================================

Strategy based on Fair Value Gaps (FVG) with swing point-based stops
Active trading window: 02:00:00 to 06:00:00
Data period: 2018 to 2025
"""

import pandas as pd
import numpy as np
from datetime import datetime, time
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')


class FVGBacktester:
    """Backtester for Fair Value Gap strategy on NQ 5-minute data"""
    
    def __init__(self, data_dir, tp_multiplier='1R'):
        """
        Initialize the backtester
        
        Parameters:
        -----------
        data_dir : str
            Directory containing the CSV files
        tp_multiplier : str
            Take profit strategy: '1R', '1.5R', '2R', or 'Structural'
        """
        self.data_dir = Path(data_dir)
        self.tp_multiplier = tp_multiplier
        self.df = None
        self.trades = []
        self.fvg_list = []  # Store all FVGs with used flag
        
    def load_data(self, years=None):
        """Load and concatenate 5-minute data from multiple years"""
        if years is None:
            years = list(range(2018, 2026))  # 2018-2025
            
        all_data = []
        
        for year in years:
            file_path = self.data_dir / f"{year} 5m.csv"
            if file_path.exists():
                print(f"Loading {year} data...")
                df_year = pd.read_csv(
                    file_path,
                    delimiter=';',
                    names=['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume'],
                    skiprows=1
                )
                all_data.append(df_year)
            else:
                print(f"Warning: File not found for {year}")
        
        if not all_data:
            raise ValueError("No data files found!")
            
        # Concatenate all years
        self.df = pd.concat(all_data, ignore_index=True)
        
        # Create datetime column (NO timezone conversion)
        self.df['Datetime'] = pd.to_datetime(
            self.df['Date'] + ' ' + self.df['Time'],
            format='%d/%m/%Y %H:%M:%S'
        )
        
        # Convert OHLC to numeric
        for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
            self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
        
        # Sort by datetime
        self.df = self.df.sort_values('Datetime').reset_index(drop=True)
        
        # Extract time component for filtering
        self.df['TimeOnly'] = self.df['Time'].apply(
            lambda x: datetime.strptime(x, '%H:%M:%S').time()
        )
        
        print(f"\nTotal candles loaded: {len(self.df)}")
        print(f"Date range: {self.df['Datetime'].min()} to {self.df['Datetime'].max()}")
        
        return self.df
    
    def is_trading_hours(self, time_obj):
        """Check if time is within trading window (02:00 to 06:00)"""
        start_time = time(2, 0, 0)
        end_time = time(6, 0, 0)
        return start_time <= time_obj <= end_time
    
    def detect_fvg(self, idx):
        """
        Detect Fair Value Gap at given index
        
        FVG uses wicks (high/low), not just bodies:
        - Bullish FVG: low[n+1] > high[n-1] (gap upward)
        - Bearish FVG: high[n+1] < low[n-1] (gap downward)
        
        Returns:
        --------
        dict or None: FVG information if detected
        """
        if idx < 1 or idx >= len(self.df) - 1:
            return None
        
        # Get three consecutive candles
        candle_prev = self.df.iloc[idx - 1]  # n-1
        candle_curr = self.df.iloc[idx]      # n
        candle_next = self.df.iloc[idx + 1]  # n+1
        
        # Check if middle candle is in trading hours
        if not self.is_trading_hours(candle_curr['TimeOnly']):
            return None
        
        # Bullish FVG: low[n+1] > high[n-1]
        if candle_next['Low'] > candle_prev['High']:
            return {
                'type': 'bullish',
                'upper_bound': candle_next['Low'],
                'lower_bound': candle_prev['High'],
                'datetime': candle_curr['Datetime'],
                'index': idx,
                'used': False
            }
        
        # Bearish FVG: high[n+1] < low[n-1]
        if candle_next['High'] < candle_prev['Low']:
            return {
                'type': 'bearish',
                'upper_bound': candle_prev['Low'],
                'lower_bound': candle_next['High'],
                'datetime': candle_curr['Datetime'],
                'index': idx,
                'used': False
            }
        
        return None
    
    def find_swing_low(self, current_idx, lookback=10):
        """
        Find the last swing low before current index
        Swing Low: local low surrounded by higher lows
        """
        for i in range(current_idx - 2, max(0, current_idx - lookback - 2), -1):
            if i < 1 or i >= len(self.df) - 1:
                continue
            
            prev_low = self.df.iloc[i - 1]['Low']
            curr_low = self.df.iloc[i]['Low']
            next_low = self.df.iloc[i + 1]['Low']
            
            # Check if it's a swing low
            if curr_low < prev_low and curr_low < next_low:
                return curr_low
        
        # If no swing found, return recent low
        return self.df.iloc[max(0, current_idx - lookback):current_idx]['Low'].min()
    
    def find_swing_high(self, current_idx, lookback=10):
        """
        Find the last swing high before current index
        Swing High: local high surrounded by lower highs
        """
        for i in range(current_idx - 2, max(0, current_idx - lookback - 2), -1):
            if i < 1 or i >= len(self.df) - 1:
                continue
            
            prev_high = self.df.iloc[i - 1]['High']
            curr_high = self.df.iloc[i]['High']
            next_high = self.df.iloc[i + 1]['High']
            
            # Check if it's a swing high
            if curr_high > prev_high and curr_high > next_high:
                return curr_high
        
        # If no swing found, return recent high
        return self.df.iloc[max(0, current_idx - lookback):current_idx]['High'].max()
    
    def check_long_entry(self, idx):
        """
        Check for long entry conditions:
        - Current candle closes bullish (close > open)
        - Close is above upper bound of a previous bearish FVG
        - The bearish FVG was created during 02:00-06:00
        - No trade has been taken on this FVG yet
        """
        candle = self.df.iloc[idx]
        
        # Must be in trading hours
        if not self.is_trading_hours(candle['TimeOnly']):
            return None
        
        # Check if candle is bullish
        if candle['Close'] <= candle['Open']:
            return None
        
        # Look for unused bearish FVGs
        for fvg in self.fvg_list:
            if fvg['type'] == 'bearish' and not fvg['used'] and fvg['index'] < idx:
                # Check if close is above upper bound
                if candle['Close'] > fvg['upper_bound']:
                    return fvg
        
        return None
    
    def check_short_entry(self, idx):
        """
        Check for short entry conditions:
        - Current candle closes bearish (close < open)
        - Close is below lower bound of a previous bullish FVG
        - The bullish FVG was created during 02:00-06:00
        - No trade has been taken on this FVG yet
        """
        candle = self.df.iloc[idx]
        
        # Must be in trading hours
        if not self.is_trading_hours(candle['TimeOnly']):
            return None
        
        # Check if candle is bearish
        if candle['Close'] >= candle['Open']:
            return None
        
        # Look for unused bullish FVGs
        for fvg in self.fvg_list:
            if fvg['type'] == 'bullish' and not fvg['used'] and fvg['index'] < idx:
                # Check if close is below lower bound
                if candle['Close'] < fvg['lower_bound']:
                    return fvg
        
        return None
    
    def calculate_take_profit(self, entry_price, stop_loss, direction, entry_idx):
        """
        Calculate take profit based on strategy type
        
        Parameters:
        -----------
        entry_price : float
        stop_loss : float
        direction : str ('long' or 'short')
        entry_idx : int
        """
        risk = abs(entry_price - stop_loss)
        
        if self.tp_multiplier == '1R':
            if direction == 'long':
                return entry_price + 1.0 * risk
            else:
                return entry_price - 1.0 * risk
                
        elif self.tp_multiplier == '1.5R':
            if direction == 'long':
                return entry_price + 1.5 * risk
            else:
                return entry_price - 1.5 * risk
                
        elif self.tp_multiplier == '2R':
            if direction == 'long':
                return entry_price + 2.0 * risk
            else:
                return entry_price - 2.0 * risk
                
        elif self.tp_multiplier == 'Structural':
            if direction == 'long':
                return self.find_swing_high(entry_idx)
            else:
                return self.find_swing_low(entry_idx)
        
        else:
            raise ValueError(f"Unknown TP multiplier: {self.tp_multiplier}")
    
    def simulate_trade(self, entry_idx, direction, fvg, stop_loss, take_profit):
        """
        Simulate a trade from entry to exit
        
        Returns:
        --------
        dict: Trade result
        """
        entry_candle = self.df.iloc[entry_idx]
        entry_price = entry_candle['Close']
        entry_time = entry_candle['Datetime']
        
        # Iterate through subsequent candles to find exit
        for i in range(entry_idx + 1, len(self.df)):
            candle = self.df.iloc[i]
            
            if direction == 'long':
                # Check stop loss hit (low touches or breaks below SL)
                if candle['Low'] <= stop_loss:
                    return {
                        'entry_time': entry_time,
                        'exit_time': candle['Datetime'],
                        'entry_price': entry_price,
                        'exit_price': stop_loss,
                        'direction': direction,
                        'pnl': stop_loss - entry_price,
                        'exit_type': 'Stop Loss',
                        'bars_in_trade': i - entry_idx
                    }
                
                # Check take profit hit (high touches or breaks above TP)
                if candle['High'] >= take_profit:
                    return {
                        'entry_time': entry_time,
                        'exit_time': candle['Datetime'],
                        'entry_price': entry_price,
                        'exit_price': take_profit,
                        'direction': direction,
                        'pnl': take_profit - entry_price,
                        'exit_type': 'Take Profit',
                        'bars_in_trade': i - entry_idx
                    }
            
            else:  # short
                # Check stop loss hit (high touches or breaks above SL)
                if candle['High'] >= stop_loss:
                    return {
                        'entry_time': entry_time,
                        'exit_time': candle['Datetime'],
                        'entry_price': entry_price,
                        'exit_price': stop_loss,
                        'direction': direction,
                        'pnl': entry_price - stop_loss,
                        'exit_type': 'Stop Loss',
                        'bars_in_trade': i - entry_idx
                    }
                
                # Check take profit hit (low touches or breaks below TP)
                if candle['Low'] <= take_profit:
                    return {
                        'entry_time': entry_time,
                        'exit_time': candle['Datetime'],
                        'entry_price': entry_price,
                        'exit_price': take_profit,
                        'direction': direction,
                        'pnl': entry_price - take_profit,
                        'exit_type': 'Take Profit',
                        'bars_in_trade': i - entry_idx
                    }
        
        # If we reach end of data without exit, close at last candle
        last_candle = self.df.iloc[-1]
        exit_price = last_candle['Close']
        pnl = (exit_price - entry_price) if direction == 'long' else (entry_price - exit_price)
        
        return {
            'entry_time': entry_time,
            'exit_time': last_candle['Datetime'],
            'entry_price': entry_price,
            'exit_price': exit_price,
            'direction': direction,
            'pnl': pnl,
            'exit_type': 'End of Data',
            'bars_in_trade': len(self.df) - 1 - entry_idx
        }
    
    def run_backtest(self):
        """Execute the complete backtest"""
        print(f"\n{'='*60}")
        print(f"Running backtest with TP strategy: {self.tp_multiplier}")
        print(f"{'='*60}")
        
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")
        
        # Reset state
        self.trades = []
        self.fvg_list = []
        in_trade = False
        
        # First pass: Detect all FVGs
        print("Detecting Fair Value Gaps...")
        for i in range(1, len(self.df) - 1):
            fvg = self.detect_fvg(i)
            if fvg is not None:
                self.fvg_list.append(fvg)
        
        print(f"Total FVGs detected: {len(self.fvg_list)}")
        bullish_fvgs = sum(1 for fvg in self.fvg_list if fvg['type'] == 'bullish')
        bearish_fvgs = sum(1 for fvg in self.fvg_list if fvg['type'] == 'bearish')
        print(f"  - Bullish FVGs: {bullish_fvgs}")
        print(f"  - Bearish FVGs: {bearish_fvgs}")
        
        # Second pass: Check for entries
        print("\nProcessing entries...")
        for i in range(len(self.df)):
            if in_trade:
                continue
            
            # Check long entry
            fvg_long = self.check_long_entry(i)
            if fvg_long is not None:
                # Calculate stop loss and take profit
                stop_loss = self.find_swing_low(i)
                take_profit = self.calculate_take_profit(
                    self.df.iloc[i]['Close'],
                    stop_loss,
                    'long',
                    i
                )
                
                # Validate stop loss and take profit
                if stop_loss >= self.df.iloc[i]['Close']:
                    continue  # Invalid stop loss
                
                if self.tp_multiplier == 'Structural' and take_profit <= self.df.iloc[i]['Close']:
                    continue  # Invalid structural TP for long
                
                # Mark FVG as used
                fvg_long['used'] = True
                
                # Simulate trade
                trade = self.simulate_trade(i, 'long', fvg_long, stop_loss, take_profit)
                self.trades.append(trade)
                in_trade = True
                
                # Skip to exit candle
                exit_idx = self.df[self.df['Datetime'] == trade['exit_time']].index[0]
                i = exit_idx
                in_trade = False
                continue
            
            # Check short entry
            fvg_short = self.check_short_entry(i)
            if fvg_short is not None:
                # Calculate stop loss and take profit
                stop_loss = self.find_swing_high(i)
                take_profit = self.calculate_take_profit(
                    self.df.iloc[i]['Close'],
                    stop_loss,
                    'short',
                    i
                )
                
                # Validate stop loss and take profit
                if stop_loss <= self.df.iloc[i]['Close']:
                    continue  # Invalid stop loss
                
                if self.tp_multiplier == 'Structural' and take_profit >= self.df.iloc[i]['Close']:
                    continue  # Invalid structural TP for short
                
                # Mark FVG as used
                fvg_short['used'] = True
                
                # Simulate trade
                trade = self.simulate_trade(i, 'short', fvg_short, stop_loss, take_profit)
                self.trades.append(trade)
                in_trade = True
                
                # Skip to exit candle
                exit_idx = self.df[self.df['Datetime'] == trade['exit_time']].index[0]
                i = exit_idx
                in_trade = False
                continue
        
        print(f"Total trades executed: {len(self.trades)}")
        
        return self.trades
    
    def calculate_statistics(self):
        """Calculate and display backtest statistics"""
        if not self.trades:
            print("No trades to analyze!")
            return None
        
        trades_df = pd.DataFrame(self.trades)
        
        # Basic statistics
        total_trades = len(trades_df)
        winning_trades = len(trades_df[trades_df['pnl'] > 0])
        losing_trades = len(trades_df[trades_df['pnl'] < 0])
        breakeven_trades = len(trades_df[trades_df['pnl'] == 0])
        
        win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
        
        # PnL statistics
        total_pnl = trades_df['pnl'].sum()
        avg_win = trades_df[trades_df['pnl'] > 0]['pnl'].mean() if winning_trades > 0 else 0
        avg_loss = trades_df[trades_df['pnl'] < 0]['pnl'].mean() if losing_trades > 0 else 0
        
        gross_profit = trades_df[trades_df['pnl'] > 0]['pnl'].sum()
        gross_loss = abs(trades_df[trades_df['pnl'] < 0]['pnl'].sum())
        profit_factor = (gross_profit / gross_loss) if gross_loss > 0 else float('inf')
        
        # Drawdown calculation
        cumulative_pnl = trades_df['pnl'].cumsum()
        running_max = cumulative_pnl.cummax()
        drawdown = running_max - cumulative_pnl
        max_drawdown = drawdown.max()
        
        # Trade duration
        avg_bars = trades_df['bars_in_trade'].mean()
        
        # Results by exit type
        exit_type_stats = trades_df.groupby('exit_type').agg({
            'pnl': ['count', 'sum', 'mean']
        }).round(2)
        
        # Results by direction
        direction_stats = trades_df.groupby('direction').agg({
            'pnl': ['count', 'sum', 'mean']
        }).round(2)
        
        stats = {
            'tp_strategy': self.tp_multiplier,
            'total_trades': total_trades,
            'winning_trades': winning_trades,
            'losing_trades': losing_trades,
            'breakeven_trades': breakeven_trades,
            'win_rate': win_rate,
            'total_pnl': total_pnl,
            'avg_win': avg_win,
            'avg_loss': avg_loss,
            'gross_profit': gross_profit,
            'gross_loss': gross_loss,
            'profit_factor': profit_factor,
            'max_drawdown': max_drawdown,
            'avg_bars_in_trade': avg_bars,
            'exit_type_stats': exit_type_stats,
            'direction_stats': direction_stats
        }
        
        return stats
    
    def print_results(self, stats):
        """Print formatted backtest results"""
        if stats is None:
            return
        
        print(f"\n{'='*60}")
        print(f"BACKTEST RESULTS - TP Strategy: {stats['tp_strategy']}")
        print(f"{'='*60}")
        
        print(f"\n--- Trade Statistics ---")
        print(f"Total Trades:          {stats['total_trades']}")
        print(f"Winning Trades:        {stats['winning_trades']}")
        print(f"Losing Trades:         {stats['losing_trades']}")
        print(f"Breakeven Trades:      {stats['breakeven_trades']}")
        print(f"Win Rate:              {stats['win_rate']:.2f}%")
        
        print(f"\n--- Profit/Loss ---")
        print(f"Total PnL:             {stats['total_pnl']:.2f} points")
        print(f"Gross Profit:          {stats['gross_profit']:.2f} points")
        print(f"Gross Loss:            {stats['gross_loss']:.2f} points")
        print(f"Average Win:           {stats['avg_win']:.2f} points")
        print(f"Average Loss:          {stats['avg_loss']:.2f} points")
        print(f"Profit Factor:         {stats['profit_factor']:.2f}")
        
        print(f"\n--- Risk Metrics ---")
        print(f"Max Drawdown:          {stats['max_drawdown']:.2f} points")
        print(f"Avg Bars in Trade:     {stats['avg_bars_in_trade']:.1f}")
        
        print(f"\n--- Exit Type Breakdown ---")
        print(stats['exit_type_stats'])
        
        print(f"\n--- Direction Breakdown ---")
        print(stats['direction_stats'])
        
        print(f"\n{'='*60}\n")


def run_all_strategies(data_dir):
    """Run backtest with all 4 TP strategies and compare results"""
    
    tp_strategies = ['1R', '1.5R', '2R', 'Structural']
    all_results = []
    
    print("="*80)
    print("NQ 5-MINUTE BACKTESTING - ALL STRATEGIES COMPARISON")
    print("="*80)
    
    for tp_strategy in tp_strategies:
        backtester = FVGBacktester(data_dir, tp_multiplier=tp_strategy)
        backtester.load_data()
        backtester.run_backtest()
        stats = backtester.calculate_statistics()
        backtester.print_results(stats)
        
        if stats:
            all_results.append(stats)
    
    # Comparison table
    print("\n" + "="*80)
    print("STRATEGY COMPARISON SUMMARY")
    print("="*80)
    print(f"\n{'Strategy':<12} {'Trades':<8} {'Win Rate':<10} {'Total PnL':<12} {'Profit Factor':<15} {'Max DD':<10}")
    print("-"*80)
    
    for stats in all_results:
        print(f"{stats['tp_strategy']:<12} "
              f"{stats['total_trades']:<8} "
              f"{stats['win_rate']:<10.2f} "
              f"{stats['total_pnl']:<12.2f} "
              f"{stats['profit_factor']:<15.2f} "
              f"{stats['max_drawdown']:<10.2f}")
    
    print("="*80)


if __name__ == "__main__":
    # Set data directory
    data_dir = "/home/runner/work/Backtest-Trading/Backtest-Trading"
    
    # Run all strategies
    run_all_strategies(data_dir)

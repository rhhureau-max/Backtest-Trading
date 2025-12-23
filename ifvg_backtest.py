#!/usr/bin/env python3
"""
IFVG (Inverse Fair Value Gap) Backtest Script
================================================
Backtests an inversion strategy on Fair Value Gaps with strict wick rules
Data: Nasdaq (NQ) 5-minute data from 2018 to 2025
Author: Senior Quantitative Analyst
"""

import pandas as pd
import numpy as np
from datetime import datetime, time
from typing import List, Tuple, Optional, Dict
import os
import glob


class IFVGBacktest:
    """
    Inverse Fair Value Gap Backtest Engine
    
    Strategy:
    - Identifies FVG using strict wick rules (High/Low, not just bodies)
    - Trades inversions of FVGs during 02:00-06:00 time window
    - Uses swing highs/lows for SL/TP placement
    """
    
    def __init__(self, data_dir: str):
        """
        Initialize the backtest engine
        
        Args:
            data_dir: Directory containing CSV files
        """
        self.data_dir = data_dir
        self.df = None
        self.trades = []
        self.swing_window = 12  # Window for swing detection
        
    def load_data(self) -> pd.DataFrame:
        """
        Load all CSV files from 2018 to 2025
        
        Returns:
            Combined DataFrame with all data
        """
        print("📊 Loading data files...")
        
        # Define file patterns
        years = [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]
        all_data = []
        
        for year in years:
            filepath = os.path.join(self.data_dir, f"{year} 5m.csv")
            
            if not os.path.exists(filepath):
                print(f"⚠️  Warning: File not found - {filepath}")
                continue
            
            print(f"  Loading {year} 5m.csv...")
            
            # Read CSV with semicolon separator
            df_year = pd.read_csv(
                filepath,
                sep=';',
                names=['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume'],
                skiprows=1  # Skip header row
            )
            
            # Parse datetime
            df_year['Datetime'] = pd.to_datetime(
                df_year['Date'] + ' ' + df_year['Time'],
                format='%d/%m/%Y %H:%M:%S'
            )
            
            # Extract time only for filtering
            df_year['TimeOnly'] = df_year['Datetime'].dt.time
            
            # Convert price columns to float
            for col in ['Open', 'High', 'Low', 'Close']:
                df_year[col] = pd.to_numeric(df_year[col], errors='coerce')
            
            df_year['Volume'] = pd.to_numeric(df_year['Volume'], errors='coerce')
            
            all_data.append(df_year)
        
        # Combine all years
        self.df = pd.concat(all_data, ignore_index=True)
        self.df = self.df.sort_values('Datetime').reset_index(drop=True)
        
        print(f"✅ Loaded {len(self.df):,} candles from {len(all_data)} files")
        print(f"   Date range: {self.df['Datetime'].min()} to {self.df['Datetime'].max()}")
        
        return self.df
    
    def identify_fvg(self, i: int) -> Optional[Dict]:
        """
        Identify Fair Value Gap using STRICT wick rules
        
        A FVG requires 3 consecutive candles with a physical gap between candle 1 and 3
        
        Args:
            i: Index of the middle candle (candle 2)
            
        Returns:
            Dictionary with FVG info or None
        """
        if i < 1 or i >= len(self.df) - 1:
            return None
        
        # Get the 3 candles
        candle1 = self.df.iloc[i - 1]
        candle2 = self.df.iloc[i]
        candle3 = self.df.iloc[i + 1]
        
        # BEARISH FVG: Low of candle 1 > High of candle 3 (gap down)
        if candle1['Low'] > candle3['High']:
            return {
                'type': 'bearish',
                'upper_bound': candle1['Low'],      # Top of the gap
                'lower_bound': candle3['High'],     # Bottom of the gap
                'candle1_idx': i - 1,
                'candle2_idx': i,
                'candle3_idx': i + 1,
                'datetime': candle3['Datetime']
            }
        
        # BULLISH FVG: High of candle 1 < Low of candle 3 (gap up)
        if candle1['High'] < candle3['Low']:
            return {
                'type': 'bullish',
                'upper_bound': candle3['Low'],      # Top of the gap
                'lower_bound': candle1['High'],     # Bottom of the gap
                'candle1_idx': i - 1,
                'candle2_idx': i,
                'candle3_idx': i + 1,
                'datetime': candle3['Datetime']
            }
        
        return None
    
    def is_valid_entry_time(self, candle_time: time) -> bool:
        """
        Check if the candle's close time is within the entry window (02:00 - 06:00 inclusive)
        
        Args:
            candle_time: Time object
            
        Returns:
            True if within entry window
        """
        start_time = time(2, 0, 0)   # 02:00:00
        end_time = time(6, 0, 0)     # 06:00:00
        
        return start_time <= candle_time <= end_time
    
    def find_swing_high(self, end_idx: int, lookback: int = None) -> Optional[float]:
        """
        Find the most recent significant swing high (optimized)
        
        Args:
            end_idx: Index to look back from
            lookback: Number of candles to look back (default: self.swing_window)
            
        Returns:
            Price of swing high or None
        """
        if lookback is None:
            lookback = self.swing_window
        
        start_idx = max(0, end_idx - lookback)
        
        if start_idx >= end_idx or end_idx - start_idx < 3:
            return None
        
        # Simply return the highest high in the lookback window
        return self.df.iloc[start_idx:end_idx]['High'].max()
    
    def find_swing_low(self, end_idx: int, lookback: int = None) -> Optional[float]:
        """
        Find the most recent significant swing low (optimized)
        
        Args:
            end_idx: Index to look back from
            lookback: Number of candles to look back (default: self.swing_window)
            
        Returns:
            Price of swing low or None
        """
        if lookback is None:
            lookback = self.swing_window
        
        start_idx = max(0, end_idx - lookback)
        
        if start_idx >= end_idx or end_idx - start_idx < 3:
            return None
        
        # Simply return the lowest low in the lookback window
        return self.df.iloc[start_idx:end_idx]['Low'].min()
    
    def check_long_entry(self, fvg: Dict, current_idx: int) -> bool:
        """
        Check if current candle triggers a LONG entry (inversion of bearish FVG)
        
        Long Entry: Close above the upper bound of a bearish FVG
        
        Args:
            fvg: Bearish FVG dictionary
            current_idx: Current candle index
            
        Returns:
            True if entry condition met
        """
        if fvg['type'] != 'bearish':
            return False
        
        current_candle = self.df.iloc[current_idx]
        
        # Check time filter
        if not self.is_valid_entry_time(current_candle['TimeOnly']):
            return False
        
        # Check if close is ABOVE the upper bound (inversion)
        if current_candle['Close'] > fvg['upper_bound']:
            return True
        
        return False
    
    def check_short_entry(self, fvg: Dict, current_idx: int) -> bool:
        """
        Check if current candle triggers a SHORT entry (inversion of bullish FVG)
        
        Short Entry: Close below the lower bound of a bullish FVG
        
        Args:
            fvg: Bullish FVG dictionary
            current_idx: Current candle index
            
        Returns:
            True if entry condition met
        """
        if fvg['type'] != 'bullish':
            return False
        
        current_candle = self.df.iloc[current_idx]
        
        # Check time filter
        if not self.is_valid_entry_time(current_candle['TimeOnly']):
            return False
        
        # Check if close is BELOW the lower bound (inversion)
        if current_candle['Close'] < fvg['lower_bound']:
            return True
        
        return False
    
    def run_backtest(self) -> List[Dict]:
        """
        Main backtest loop - Only one trade at a time
        
        Returns:
            List of all trades
        """
        print("\n🚀 Running IFVG Backtest...")
        print("=" * 70)
        
        if self.df is None or len(self.df) == 0:
            print("❌ No data loaded!")
            return []
        
        self.trades = []
        active_fvgs = []  # Store recent FVGs that haven't been traded yet
        max_fvg_age = 50  # Max candles to keep an FVG active
        
        # Track current open trade
        current_trade = None
        trade_entry_idx = -1
        
        # Start from index 2 (need at least 3 candles for FVG)
        for i in range(2, len(self.df) - 1):
            
            # Progress indicator
            if i % 10000 == 0:
                progress = (i / len(self.df)) * 100
                print(f"  Progress: {progress:.1f}% ({i:,}/{len(self.df):,} candles)", end='\r')
            
            # If we have an open trade, check for exit
            if current_trade is not None:
                candle = self.df.iloc[i]
                exit_triggered = False
                
                if current_trade['direction'] == 'long':
                    # Check Stop Loss
                    if candle['Low'] <= current_trade['stop_loss']:
                        current_trade['exit_idx'] = i
                        current_trade['exit_price'] = current_trade['stop_loss']
                        current_trade['exit_reason'] = 'SL'
                        current_trade['exit_time'] = candle['Datetime']
                        exit_triggered = True
                    # Check Take Profit
                    elif candle['High'] >= current_trade['take_profit']:
                        current_trade['exit_idx'] = i
                        current_trade['exit_price'] = current_trade['take_profit']
                        current_trade['exit_reason'] = 'TP'
                        current_trade['exit_time'] = candle['Datetime']
                        exit_triggered = True
                else:  # short
                    # Check Stop Loss
                    if candle['High'] >= current_trade['stop_loss']:
                        current_trade['exit_idx'] = i
                        current_trade['exit_price'] = current_trade['stop_loss']
                        current_trade['exit_reason'] = 'SL'
                        current_trade['exit_time'] = candle['Datetime']
                        exit_triggered = True
                    # Check Take Profit
                    elif candle['Low'] <= current_trade['take_profit']:
                        current_trade['exit_idx'] = i
                        current_trade['exit_price'] = current_trade['take_profit']
                        current_trade['exit_reason'] = 'TP'
                        current_trade['exit_time'] = candle['Datetime']
                        exit_triggered = True
                
                if exit_triggered:
                    # Calculate P&L
                    if current_trade['direction'] == 'long':
                        current_trade['pnl'] = current_trade['exit_price'] - current_trade['entry_price']
                    else:
                        current_trade['pnl'] = current_trade['entry_price'] - current_trade['exit_price']
                    
                    self.trades.append(current_trade)
                    current_trade = None  # Close the trade
                    continue  # Move to next candle
            
            # Only look for new entries if no trade is open
            if current_trade is None:
                # Identify new FVG at current position
                fvg = self.identify_fvg(i)
                if fvg is not None:
                    active_fvgs.append(fvg)
                
                # Clean up old FVGs
                active_fvgs = [f for f in active_fvgs if (i - f['candle3_idx']) < max_fvg_age]
                
                # Check for entry signals on active FVGs
                for fvg in active_fvgs[:]:  # Iterate over copy
                    
                    # Check LONG entry (inversion of bearish FVG)
                    if fvg['type'] == 'bearish' and self.check_long_entry(fvg, i):
                        current_trade = self._create_trade_entry(i, 'long', fvg)
                        active_fvgs.remove(fvg)  # Remove FVG after trade
                        break  # Only one trade at a time
                    
                    # Check SHORT entry (inversion of bullish FVG)
                    elif fvg['type'] == 'bullish' and self.check_short_entry(fvg, i):
                        current_trade = self._create_trade_entry(i, 'short', fvg)
                        active_fvgs.remove(fvg)  # Remove FVG after trade
                        break  # Only one trade at a time
        
        # Close any remaining open trade at end of data
        if current_trade is not None:
            exit_candle = self.df.iloc[-1]
            current_trade['exit_idx'] = len(self.df) - 1
            current_trade['exit_price'] = exit_candle['Close']
            current_trade['exit_reason'] = 'EOD'
            current_trade['exit_time'] = exit_candle['Datetime']
            
            if current_trade['direction'] == 'long':
                current_trade['pnl'] = current_trade['exit_price'] - current_trade['entry_price']
            else:
                current_trade['pnl'] = current_trade['entry_price'] - current_trade['exit_price']
            
            self.trades.append(current_trade)
        
        print(f"\n✅ Backtest complete! {len(self.trades)} trades executed")
        
        return self.trades
    
    def _create_trade_entry(self, entry_idx: int, direction: str, fvg: Dict) -> Dict:
        """
        Create a trade entry with SL/TP levels
        
        Args:
            entry_idx: Index of entry candle
            direction: 'long' or 'short'
            fvg: FVG that triggered the trade
            
        Returns:
            Trade dictionary (without exit info)
        """
        entry_candle = self.df.iloc[entry_idx]
        entry_price = entry_candle['Close']
        entry_time = entry_candle['Datetime']
        
        # Set Stop Loss and Take Profit with fixed 1.5 Risk/Reward ratio
        if direction == 'long':
            # SL: Below recent swing low - 0.5 points
            swing_low = self.find_swing_low(entry_idx, lookback=15)
            if swing_low is None:
                swing_low = entry_price - 50  # Fallback: 50 points below entry
            stop_loss = swing_low - 0.5
            
            # Calculate risk
            risk = entry_price - stop_loss
            
            # TP: Entry + (Risk * 1.5) for 1.5 RR ratio
            take_profit = entry_price + (risk * 1.5)
        
        else:  # short
            # SL: Above recent swing high + 0.5 points
            swing_high = self.find_swing_high(entry_idx, lookback=15)
            if swing_high is None:
                swing_high = entry_price + 50  # Fallback: 50 points above entry
            stop_loss = swing_high + 0.5
            
            # Calculate risk
            risk = stop_loss - entry_price
            
            # TP: Entry - (Risk * 1.5) for 1.5 RR ratio
            take_profit = entry_price - (risk * 1.5)
        
        return {
            'direction': direction,
            'entry_time': entry_time,
            'entry_price': entry_price,
            'stop_loss': stop_loss,
            'take_profit': take_profit,
            'fvg_type': fvg['type'],
            'year': entry_time.year,
            # Exit info will be filled when trade closes
            'exit_time': None,
            'exit_price': None,
            'exit_reason': None,
            'exit_idx': None,
            'pnl': None
        }
    
    def _get_trade_exit_idx(self, trade: Dict) -> int:
        """
        Helper to get the exit index of a trade
        
        Args:
            trade: Trade dictionary
            
        Returns:
            Index of exit candle
        """
        return trade.get('exit_idx', len(self.df) - 1)
    
    def calculate_metrics(self) -> Dict:
        """
        Calculate comprehensive performance metrics
        
        Returns:
            Dictionary of performance metrics
        """
        if not self.trades:
            return {
                'total_trades': 0,
                'win_rate': 0,
                'total_pnl': 0,
                'profit_factor': 0,
                'max_drawdown': 0,
                'avg_win': 0,
                'avg_loss': 0,
                'largest_win': 0,
                'largest_loss': 0
            }
        
        df_trades = pd.DataFrame(self.trades)
        
        # Basic metrics
        total_trades = len(df_trades)
        winning_trades = df_trades[df_trades['pnl'] > 0]
        losing_trades = df_trades[df_trades['pnl'] <= 0]
        
        num_wins = len(winning_trades)
        num_losses = len(losing_trades)
        win_rate = (num_wins / total_trades * 100) if total_trades > 0 else 0
        
        # P&L metrics
        total_pnl = df_trades['pnl'].sum()
        gross_profit = winning_trades['pnl'].sum() if num_wins > 0 else 0
        gross_loss = abs(losing_trades['pnl'].sum()) if num_losses > 0 else 0
        profit_factor = (gross_profit / gross_loss) if gross_loss > 0 else 0
        
        # Average win/loss
        avg_win = winning_trades['pnl'].mean() if num_wins > 0 else 0
        avg_loss = losing_trades['pnl'].mean() if num_losses > 0 else 0
        
        # Largest win/loss
        largest_win = winning_trades['pnl'].max() if num_wins > 0 else 0
        largest_loss = losing_trades['pnl'].min() if num_losses > 0 else 0
        
        # Drawdown calculation
        cumulative_pnl = df_trades['pnl'].cumsum()
        running_max = cumulative_pnl.cummax()
        drawdown = cumulative_pnl - running_max
        max_drawdown = drawdown.min()
        
        # Yearly breakdown
        yearly_stats = {}
        for year in df_trades['year'].unique():
            year_trades = df_trades[df_trades['year'] == year]
            year_wins = len(year_trades[year_trades['pnl'] > 0])
            year_total = len(year_trades)
            year_pnl = year_trades['pnl'].sum()
            year_wr = (year_wins / year_total * 100) if year_total > 0 else 0
            
            yearly_stats[year] = {
                'trades': year_total,
                'wins': year_wins,
                'losses': year_total - year_wins,
                'win_rate': year_wr,
                'pnl': year_pnl
            }
        
        return {
            'total_trades': total_trades,
            'winning_trades': num_wins,
            'losing_trades': num_losses,
            'win_rate': win_rate,
            'total_pnl': total_pnl,
            'gross_profit': gross_profit,
            'gross_loss': gross_loss,
            'profit_factor': profit_factor,
            'max_drawdown': max_drawdown,
            'avg_win': avg_win,
            'avg_loss': avg_loss,
            'largest_win': largest_win,
            'largest_loss': largest_loss,
            'yearly_stats': yearly_stats
        }
    
    def print_report(self, metrics: Dict):
        """
        Print comprehensive backtest report
        
        Args:
            metrics: Performance metrics dictionary
        """
        print("\n" + "=" * 70)
        print("📈 IFVG BACKTEST RESULTS")
        print("=" * 70)
        
        print("\n🎯 OVERALL PERFORMANCE")
        print("-" * 70)
        print(f"Total Trades:        {metrics['total_trades']:,}")
        print(f"Winning Trades:      {metrics['winning_trades']:,}")
        print(f"Losing Trades:       {metrics['losing_trades']:,}")
        print(f"Win Rate:            {metrics['win_rate']:.2f}%")
        print()
        print(f"Total P&L:           {metrics['total_pnl']:.2f} points")
        print(f"Gross Profit:        {metrics['gross_profit']:.2f} points")
        print(f"Gross Loss:          {metrics['gross_loss']:.2f} points")
        print(f"Profit Factor:       {metrics['profit_factor']:.2f}")
        print(f"Max Drawdown:        {metrics['max_drawdown']:.2f} points")
        print()
        print(f"Average Win:         {metrics['avg_win']:.2f} points")
        print(f"Average Loss:        {metrics['avg_loss']:.2f} points")
        print(f"Largest Win:         {metrics['largest_win']:.2f} points")
        print(f"Largest Loss:        {metrics['largest_loss']:.2f} points")
        
        print("\n📅 YEARLY BREAKDOWN")
        print("-" * 70)
        print(f"{'Year':<8} {'Trades':<10} {'Wins':<8} {'Losses':<8} {'Win Rate':<12} {'P&L (pts)':<15}")
        print("-" * 70)
        
        if 'yearly_stats' in metrics:
            for year in sorted(metrics['yearly_stats'].keys()):
                stats = metrics['yearly_stats'][year]
                print(f"{year:<8} {stats['trades']:<10} {stats['wins']:<8} "
                      f"{stats['losses']:<8} {stats['win_rate']:<11.2f}% "
                      f"{stats['pnl']:<14.2f}")
        
        print("=" * 70)
        
        # Additional trade statistics
        if self.trades:
            df_trades = pd.DataFrame(self.trades)
            
            print("\n📊 ADDITIONAL STATISTICS")
            print("-" * 70)
            
            # Direction breakdown
            long_trades = df_trades[df_trades['direction'] == 'long']
            short_trades = df_trades[df_trades['direction'] == 'short']
            
            print(f"\nLong Trades:  {len(long_trades):,} "
                  f"(Win Rate: {(len(long_trades[long_trades['pnl'] > 0]) / len(long_trades) * 100):.2f}%)")
            print(f"Short Trades: {len(short_trades):,} "
                  f"(Win Rate: {(len(short_trades[short_trades['pnl'] > 0]) / len(short_trades) * 100):.2f}%)")
            
            # Exit reason breakdown
            print(f"\nExit Reasons:")
            exit_counts = df_trades['exit_reason'].value_counts()
            for reason, count in exit_counts.items():
                pct = (count / len(df_trades)) * 100
                print(f"  {reason}: {count:,} ({pct:.1f}%)")
            
            print("=" * 70)


def main():
    """
    Main execution function
    """
    print("=" * 70)
    print("🔥 IFVG BACKTEST - INVERSE FAIR VALUE GAP STRATEGY")
    print("=" * 70)
    print()
    print("Strategy Details:")
    print("  • Fair Value Gap detection using strict wick rules")
    print("  • Entry on FVG inversions during 02:00-06:00 window")
    print("  • Stop Loss: Swing low/high ± 0.5 points")
    print("  • Take Profit: 1.5 Risk/Reward ratio")
    print("  • Only one trade at a time")
    print("  • Data: NQ 5-minute (2018-2025)")
    print()
    
    # Initialize backtest
    data_dir = "/home/runner/work/Backtest-Trading/Backtest-Trading"
    backtest = IFVGBacktest(data_dir)
    
    # Load data
    backtest.load_data()
    
    # Run backtest
    trades = backtest.run_backtest()
    
    # Calculate metrics
    metrics = backtest.calculate_metrics()
    
    # Print report
    backtest.print_report(metrics)
    
    # Save trades to CSV for further analysis
    if trades:
        trades_df = pd.DataFrame(trades)
        output_file = os.path.join(data_dir, "ifvg_trades_results.csv")
        trades_df.to_csv(output_file, index=False)
        print(f"\n💾 Trade results saved to: {output_file}")
    
    print("\n✨ Backtest completed successfully!")


if __name__ == "__main__":
    main()

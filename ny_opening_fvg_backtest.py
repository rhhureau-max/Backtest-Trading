#!/usr/bin/env python3
"""
Fair Value Gap (FVG) Backtest Strategy - NY Opening
====================================================
This script backtests an FVG strategy focused on the New York opening session (08:30-09:00 ET).
It loads 1-minute NQ futures data from 2018-2025 and simulates trades based on FVG breakouts.

Strategy Rules:
- Identify FVGs between 08:30-09:00 NY time (first valid FVG only)
- Enter on FVG breakout (reversal/breakdown)
- Use dynamic stop loss based on trigger candle
- Three take profit levels: 1.0R, 1.5R, 2.0R

Author: Quantitative Trading System
"""

import pandas as pd
import numpy as np
from datetime import datetime, time
import pytz
import glob
import os
from typing import Tuple, Optional, Dict, List
import warnings

warnings.filterwarnings('ignore')


class NYOpeningFVGBacktest:
    """Backtest engine for NY Opening FVG strategy."""
    
    def __init__(self, data_directory: str):
        """
        Initialize the backtest engine.
        
        Args:
            data_directory: Path to directory containing CSV files
        """
        self.data_directory = data_directory
        self.ny_tz = pytz.timezone('America/New_York')
        self.utc_tz = pytz.UTC
        self.df_all = None
        self.trades = []
        
    def load_data(self) -> pd.DataFrame:
        """
        Load all 1-minute CSV files from 2018 to 2025.
        
        Returns:
            Combined DataFrame with datetime index in NY timezone
        """
        print("Loading data files...")
        all_data = []
        
        for year in range(2018, 2026):
            filename = os.path.join(self.data_directory, f"{year} 1m.csv")
            if not os.path.exists(filename):
                print(f"  Warning: {filename} not found, skipping...")
                continue
                
            print(f"  Loading {year} data...")
            
            # Read CSV with semicolon delimiter, skip header row
            df = pd.read_csv(
                filename,
                sep=';',
                header=0,
                names=['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
            )
            
            # Parse datetime - combine Date and Time columns
            df['DateTime'] = pd.to_datetime(
                df['Date'] + ' ' + df['Time'],
                format='%d/%m/%Y %H:%M:%S'
            )
            
            # Convert to NY timezone
            # First assume UTC, then convert to NY time
            df['DateTime'] = df['DateTime'].dt.tz_localize('UTC').dt.tz_convert(self.ny_tz)
            
            # Keep only OHLC columns
            df = df[['DateTime', 'Open', 'High', 'Low', 'Close', 'Volume']]
            
            all_data.append(df)
        
        # Combine all years
        self.df_all = pd.concat(all_data, ignore_index=True)
        self.df_all = self.df_all.sort_values('DateTime').reset_index(drop=True)
        
        print(f"\nLoaded {len(self.df_all):,} bars from {self.df_all['DateTime'].min()} to {self.df_all['DateTime'].max()}")
        
        return self.df_all
    
    def detect_fvg(self, candle_1: pd.Series, candle_2: pd.Series, candle_3: pd.Series) -> Optional[Dict]:
        """
        Detect Fair Value Gap (FVG) pattern.
        
        Args:
            candle_1: First candle (n-1)
            candle_2: Middle candle (n)
            candle_3: Third candle (n+1)
            
        Returns:
            Dictionary with FVG info or None if no FVG detected
            {
                'type': 'bullish' or 'bearish',
                'upper_bound': float,
                'lower_bound': float,
                'trigger_candle_idx': int
            }
        """
        # Bullish FVG: High of candle_1 < Low of candle_3
        if candle_1['High'] < candle_3['Low']:
            return {
                'type': 'bullish',
                'upper_bound': candle_3['Low'],
                'lower_bound': candle_1['High'],
                'trigger_candle_idx': candle_1.name  # Index of first candle
            }
        
        # Bearish FVG: Low of candle_1 > High of candle_3
        if candle_1['Low'] > candle_3['High']:
            return {
                'type': 'bearish',
                'upper_bound': candle_1['Low'],
                'lower_bound': candle_3['High'],
                'trigger_candle_idx': candle_1.name  # Index of first candle
            }
        
        return None
    
    def find_daily_fvg(self, day_data: pd.DataFrame) -> Optional[Dict]:
        """
        Find the first FVG between 08:30 and 09:00 NY time.
        
        Args:
            day_data: DataFrame containing one day's data
            
        Returns:
            FVG dictionary or None
        """
        # Filter data between 08:30 and 09:00
        search_window = day_data[
            (day_data['DateTime'].dt.time >= time(8, 30)) &
            (day_data['DateTime'].dt.time < time(9, 0))
        ].copy()
        
        if len(search_window) < 3:
            return None
        
        # Search for first FVG in this window
        for i in range(len(search_window) - 2):
            candle_1 = search_window.iloc[i]
            candle_2 = search_window.iloc[i + 1]
            candle_3 = search_window.iloc[i + 2]
            
            fvg = self.detect_fvg(candle_1, candle_2, candle_3)
            if fvg:
                fvg['detection_time'] = candle_3['DateTime']
                fvg['detection_idx'] = candle_3.name
                return fvg
        
        return None
    
    def find_entry_signal(self, day_data: pd.DataFrame, fvg: Dict, start_idx: int) -> Optional[Dict]:
        """
        Find entry signal after FVG detection (breakout/reversal).
        
        Args:
            day_data: DataFrame containing one day's data
            fvg: FVG dictionary
            start_idx: Index to start looking for entry (after FVG detection)
            
        Returns:
            Entry signal dictionary or None
        """
        # Get data after FVG detection
        after_fvg = day_data[day_data.index > start_idx].copy()
        
        if len(after_fvg) == 0:
            return None
        
        for idx, candle in after_fvg.iterrows():
            if fvg['type'] == 'bullish':
                # SHORT entry: Candle closes BELOW lower bound of FVG
                if candle['Close'] < fvg['lower_bound']:
                    return {
                        'type': 'SHORT',
                        'entry_price': candle['Close'],
                        'entry_time': candle['DateTime'],
                        'entry_idx': idx,
                        'trigger_high': candle['High'],
                        'trigger_low': candle['Low'],
                        'stop_loss': candle['High'] + 0.5
                    }
            
            elif fvg['type'] == 'bearish':
                # LONG entry: Candle closes ABOVE upper bound of FVG
                if candle['Close'] > fvg['upper_bound']:
                    return {
                        'type': 'LONG',
                        'entry_price': candle['Close'],
                        'entry_time': candle['DateTime'],
                        'entry_idx': idx,
                        'trigger_high': candle['High'],
                        'trigger_low': candle['Low'],
                        'stop_loss': candle['Low'] - 0.5
                    }
        
        return None
    
    def simulate_trade(self, day_data: pd.DataFrame, entry: Dict) -> Dict:
        """
        Simulate trade execution with stop loss and take profit levels.
        
        Args:
            day_data: DataFrame containing one day's data
            entry: Entry signal dictionary
            
        Returns:
            Trade result dictionary
        """
        entry_price = entry['entry_price']
        stop_loss = entry['stop_loss']
        trade_type = entry['type']
        
        # Calculate risk
        risk = abs(entry_price - stop_loss)
        
        # Calculate take profit levels
        if trade_type == 'LONG':
            tp1_price = entry_price + (1.0 * risk)
            tp2_price = entry_price + (1.5 * risk)
            tp3_price = entry_price + (2.0 * risk)
        else:  # SHORT
            tp1_price = entry_price - (1.0 * risk)
            tp2_price = entry_price - (1.5 * risk)
            tp3_price = entry_price - (2.0 * risk)
        
        # Initialize result
        result = {
            'date': entry['entry_time'].date(),
            'type': trade_type,
            'entry_price': entry_price,
            'stop_loss': stop_loss,
            'risk': risk,
            'tp1_price': tp1_price,
            'tp2_price': tp2_price,
            'tp3_price': tp3_price,
            'tp1_hit': False,
            'tp2_hit': False,
            'tp3_hit': False,
            'sl_hit': False,
            'tp1_pnl': 0.0,
            'tp2_pnl': 0.0,
            'tp3_pnl': 0.0,
            'total_pnl': 0.0
        }
        
        # Remaining position sizes
        positions = {
            'tp1': 0.33,
            'tp2': 0.33,
            'tp3': 0.34
        }
        
        # Get bars after entry
        after_entry = day_data[day_data.index > entry['entry_idx']].copy()
        
        # Simulate bar by bar
        for idx, candle in after_entry.iterrows():
            high = candle['High']
            low = candle['Low']
            
            if trade_type == 'LONG':
                # Check stop loss first
                if low <= stop_loss and not result['sl_hit']:
                    result['sl_hit'] = True
                    # Calculate loss for remaining positions
                    remaining = positions['tp1'] + positions['tp2'] + positions['tp3']
                    result['total_pnl'] = (stop_loss - entry_price) * remaining
                    break
                
                # Check take profits (in order)
                if high >= tp1_price and not result['tp1_hit']:
                    result['tp1_hit'] = True
                    result['tp1_pnl'] = (tp1_price - entry_price) * positions['tp1']
                    positions['tp1'] = 0
                
                if high >= tp2_price and not result['tp2_hit']:
                    result['tp2_hit'] = True
                    result['tp2_pnl'] = (tp2_price - entry_price) * positions['tp2']
                    positions['tp2'] = 0
                
                if high >= tp3_price and not result['tp3_hit']:
                    result['tp3_hit'] = True
                    result['tp3_pnl'] = (tp3_price - entry_price) * positions['tp3']
                    positions['tp3'] = 0
                    break  # All positions closed
            
            else:  # SHORT
                # Check stop loss first
                if high >= stop_loss and not result['sl_hit']:
                    result['sl_hit'] = True
                    # Calculate loss for remaining positions
                    remaining = positions['tp1'] + positions['tp2'] + positions['tp3']
                    result['total_pnl'] = (entry_price - stop_loss) * remaining
                    break
                
                # Check take profits (in order)
                if low <= tp1_price and not result['tp1_hit']:
                    result['tp1_hit'] = True
                    result['tp1_pnl'] = (entry_price - tp1_price) * positions['tp1']
                    positions['tp1'] = 0
                
                if low <= tp2_price and not result['tp2_hit']:
                    result['tp2_hit'] = True
                    result['tp2_pnl'] = (entry_price - tp2_price) * positions['tp2']
                    positions['tp2'] = 0
                
                if low <= tp3_price and not result['tp3_hit']:
                    result['tp3_hit'] = True
                    result['tp3_pnl'] = (entry_price - tp3_price) * positions['tp3']
                    positions['tp3'] = 0
                    break  # All positions closed
        
        # Calculate total PnL (only if not already set by stop loss)
        if not result['sl_hit']:
            result['total_pnl'] = result['tp1_pnl'] + result['tp2_pnl'] + result['tp3_pnl']
        
        return result
    
    def run_backtest(self):
        """Execute the complete backtest."""
        print("\n" + "="*80)
        print("Starting NY Opening FVG Backtest")
        print("="*80)
        
        if self.df_all is None:
            self.load_data()
        
        # Group by date
        self.df_all['Date'] = self.df_all['DateTime'].dt.date
        dates = self.df_all['Date'].unique()
        
        print(f"\nProcessing {len(dates):,} trading days...")
        
        trade_count = 0
        no_fvg_count = 0
        no_entry_count = 0
        
        for date in dates:
            day_data = self.df_all[self.df_all['Date'] == date].copy()
            
            # Step 1: Find FVG between 08:30 and 09:00
            fvg = self.find_daily_fvg(day_data)
            if not fvg:
                no_fvg_count += 1
                continue
            
            # Step 2: Find entry signal (after FVG detection)
            entry = self.find_entry_signal(day_data, fvg, fvg['detection_idx'])
            if not entry:
                no_entry_count += 1
                continue
            
            # Step 3: Simulate trade
            result = self.simulate_trade(day_data, entry)
            self.trades.append(result)
            trade_count += 1
            
            if trade_count % 10 == 0:
                print(f"  Processed {trade_count} trades...")
        
        print(f"\n✓ Backtest completed!")
        print(f"  Total days analyzed: {len(dates):,}")
        print(f"  Days with no FVG: {no_fvg_count:,}")
        print(f"  Days with FVG but no entry: {no_entry_count:,}")
        print(f"  Trades executed: {trade_count:,}")
        
        return self.trades
    
    def calculate_statistics(self) -> Dict:
        """
        Calculate comprehensive backtest statistics.
        
        Returns:
            Dictionary containing all statistics
        """
        if not self.trades:
            print("No trades to analyze!")
            return {}
        
        df_trades = pd.DataFrame(self.trades)
        
        # Overall statistics
        total_trades = len(df_trades)
        winning_trades = len(df_trades[df_trades['total_pnl'] > 0])
        losing_trades = len(df_trades[df_trades['total_pnl'] <= 0])
        
        overall_win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
        
        # TP-specific win rates
        tp1_hit_count = df_trades['tp1_hit'].sum()
        tp2_hit_count = df_trades['tp2_hit'].sum()
        tp3_hit_count = df_trades['tp3_hit'].sum()
        
        tp1_win_rate = (tp1_hit_count / total_trades * 100) if total_trades > 0 else 0
        tp2_win_rate = (tp2_hit_count / total_trades * 100) if total_trades > 0 else 0
        tp3_win_rate = (tp3_hit_count / total_trades * 100) if total_trades > 0 else 0
        
        # PnL statistics
        total_pnl = df_trades['total_pnl'].sum()
        avg_pnl = df_trades['total_pnl'].mean()
        avg_winning_trade = df_trades[df_trades['total_pnl'] > 0]['total_pnl'].mean() if winning_trades > 0 else 0
        avg_losing_trade = df_trades[df_trades['total_pnl'] <= 0]['total_pnl'].mean() if losing_trades > 0 else 0
        
        # Profit factor
        gross_profit = df_trades[df_trades['total_pnl'] > 0]['total_pnl'].sum()
        gross_loss = abs(df_trades[df_trades['total_pnl'] <= 0]['total_pnl'].sum())
        profit_factor = (gross_profit / gross_loss) if gross_loss > 0 else float('inf')
        
        # Maximum drawdown
        df_trades['cumulative_pnl'] = df_trades['total_pnl'].cumsum()
        df_trades['running_max'] = df_trades['cumulative_pnl'].cummax()
        df_trades['drawdown'] = df_trades['cumulative_pnl'] - df_trades['running_max']
        max_drawdown = df_trades['drawdown'].min()
        
        # Risk metrics
        avg_risk = df_trades['risk'].mean()
        
        # Trade type breakdown
        long_trades = len(df_trades[df_trades['type'] == 'LONG'])
        short_trades = len(df_trades[df_trades['type'] == 'SHORT'])
        long_win_rate = (len(df_trades[(df_trades['type'] == 'LONG') & (df_trades['total_pnl'] > 0)]) / long_trades * 100) if long_trades > 0 else 0
        short_win_rate = (len(df_trades[(df_trades['type'] == 'SHORT') & (df_trades['total_pnl'] > 0)]) / short_trades * 100) if short_trades > 0 else 0
        
        stats = {
            'total_trades': total_trades,
            'winning_trades': winning_trades,
            'losing_trades': losing_trades,
            'overall_win_rate': overall_win_rate,
            'tp1_hit_count': tp1_hit_count,
            'tp2_hit_count': tp2_hit_count,
            'tp3_hit_count': tp3_hit_count,
            'tp1_win_rate': tp1_win_rate,
            'tp2_win_rate': tp2_win_rate,
            'tp3_win_rate': tp3_win_rate,
            'total_pnl': total_pnl,
            'avg_pnl': avg_pnl,
            'avg_winning_trade': avg_winning_trade,
            'avg_losing_trade': avg_losing_trade,
            'gross_profit': gross_profit,
            'gross_loss': gross_loss,
            'profit_factor': profit_factor,
            'max_drawdown': max_drawdown,
            'avg_risk': avg_risk,
            'long_trades': long_trades,
            'short_trades': short_trades,
            'long_win_rate': long_win_rate,
            'short_win_rate': short_win_rate
        }
        
        return stats
    
    def display_results(self):
        """Display backtest results and statistics."""
        if not self.trades:
            print("\nNo trades to display!")
            return
        
        # Create results DataFrame
        df_results = pd.DataFrame(self.trades)
        
        # Calculate statistics
        stats = self.calculate_statistics()
        
        print("\n" + "="*80)
        print("BACKTEST RESULTS")
        print("="*80)
        
        print("\n📊 OVERALL STATISTICS")
        print("-" * 80)
        print(f"Total Trades:              {stats['total_trades']:,}")
        print(f"Winning Trades:            {stats['winning_trades']:,}")
        print(f"Losing Trades:             {stats['losing_trades']:,}")
        print(f"Overall Win Rate:          {stats['overall_win_rate']:.2f}%")
        
        print("\n🎯 TAKE PROFIT ANALYSIS")
        print("-" * 80)
        print(f"TP1 Hit Count:             {stats['tp1_hit_count']:,} ({stats['tp1_win_rate']:.2f}%)")
        print(f"TP2 Hit Count:             {stats['tp2_hit_count']:,} ({stats['tp2_win_rate']:.2f}%)")
        print(f"TP3 Hit Count:             {stats['tp3_hit_count']:,} ({stats['tp3_win_rate']:.2f}%)")
        
        print("\n💰 PROFIT & LOSS")
        print("-" * 80)
        print(f"Total PnL:                 {stats['total_pnl']:.2f} points")
        print(f"Average PnL per Trade:     {stats['avg_pnl']:.2f} points")
        print(f"Average Winning Trade:     {stats['avg_winning_trade']:.2f} points")
        print(f"Average Losing Trade:      {stats['avg_losing_trade']:.2f} points")
        print(f"Gross Profit:              {stats['gross_profit']:.2f} points")
        print(f"Gross Loss:                {stats['gross_loss']:.2f} points")
        print(f"Profit Factor:             {stats['profit_factor']:.2f}")
        
        print("\n📉 RISK METRICS")
        print("-" * 80)
        print(f"Maximum Drawdown:          {stats['max_drawdown']:.2f} points")
        print(f"Average Risk per Trade:    {stats['avg_risk']:.2f} points")
        
        print("\n📈 TRADE TYPE BREAKDOWN")
        print("-" * 80)
        print(f"Long Trades:               {stats['long_trades']:,} (Win Rate: {stats['long_win_rate']:.2f}%)")
        print(f"Short Trades:              {stats['short_trades']:,} (Win Rate: {stats['short_win_rate']:.2f}%)")
        
        # Display sample trades
        print("\n📋 SAMPLE TRADES (First 10)")
        print("-" * 80)
        display_cols = ['date', 'type', 'entry_price', 'stop_loss', 'tp1_hit', 'tp2_hit', 'tp3_hit', 'total_pnl']
        print(df_results[display_cols].head(10).to_string(index=False))
        
        print("\n📋 SAMPLE TRADES (Last 10)")
        print("-" * 80)
        print(df_results[display_cols].tail(10).to_string(index=False))
        
        # Save to CSV
        output_file = os.path.join(self.data_directory, 'ny_opening_fvg_results.csv')
        df_results.to_csv(output_file, index=False)
        print(f"\n✅ Results saved to: {output_file}")
        
        return df_results, stats


def main():
    """Main execution function."""
    # Set data directory
    data_dir = "/home/runner/work/Backtest-Trading/Backtest-Trading"
    
    print("\n" + "="*80)
    print("NY OPENING FVG BACKTEST")
    print("Strategy: Fair Value Gap Breakout (NY Session 08:30-09:00)")
    print("="*80)
    
    # Initialize backtest
    backtest = NYOpeningFVGBacktest(data_dir)
    
    # Run backtest
    trades = backtest.run_backtest()
    
    # Display results
    if trades:
        backtest.display_results()
    else:
        print("\n⚠️ No trades were executed. Check data and FVG detection logic.")
    
    print("\n" + "="*80)
    print("Backtest completed successfully!")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Fair Value Gap (FVG) Backtest Strategy - NY Opening (ALL FVGs, Multiple RR Levels)
===================================================================================
This script backtests an FVG strategy focused on the New York opening session (08:30-09:00 ET).
It tests ALL FVGs found in the window and provides separate results for 1R, 1.5R, and 2R targets.

Strategy Rules:
- Identify ALL FVGs between 08:30-09:00 NY time
- Enter on FVG breakout (reversal/breakdown)
- Use dynamic stop loss based on trigger candle
- Test separately: 1R, 1.5R, and 2R take profit levels

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
    """Backtest engine for NY Opening FVG strategy with multiple RR levels."""
    
    def __init__(self, data_directory: str, rr_level: float = 1.0):
        """
        Initialize the backtest engine.
        
        Args:
            data_directory: Path to directory containing CSV files
            rr_level: Risk-Reward ratio (1.0, 1.5, or 2.0)
        """
        self.data_directory = data_directory
        self.rr_level = rr_level
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
        print(f"\n📂 Loading 1-minute data files...")
        
        # Pattern to match year files
        file_pattern = os.path.join(self.data_directory, "*1m.csv")
        csv_files = sorted(glob.glob(file_pattern))
        
        if not csv_files:
            raise FileNotFoundError(f"No 1-minute CSV files found in {self.data_directory}")
        
        print(f"   Found {len(csv_files)} files")
        
        dfs = []
        for file in csv_files:
            print(f"   Loading: {os.path.basename(file)}")
            df = pd.read_csv(file, sep=';', header=0)
            
            # Parse datetime (columns are: Date, Time, Open, High, Low, Close, Volume)
            df['DateTime'] = pd.to_datetime(
                df.iloc[:, 0] + ' ' + df.iloc[:, 1],
                format='%d/%m/%Y %H:%M:%S',
                errors='coerce'
            )
            
            # Extract OHLC
            df['Open'] = pd.to_numeric(df.iloc[:, 2], errors='coerce')
            df['High'] = pd.to_numeric(df.iloc[:, 3], errors='coerce')
            df['Low'] = pd.to_numeric(df.iloc[:, 4], errors='coerce')
            df['Close'] = pd.to_numeric(df.iloc[:, 5], errors='coerce')
            
            # Keep only needed columns
            df = df[['DateTime', 'Open', 'High', 'Low', 'Close']].copy()
            df = df.dropna()
            
            dfs.append(df)
        
        # Combine all data
        df_combined = pd.concat(dfs, ignore_index=True)
        df_combined = df_combined.sort_values('DateTime').reset_index(drop=True)
        
        # Convert to NY timezone
        df_combined['DateTime'] = pd.to_datetime(df_combined['DateTime'])
        df_combined['DateTime'] = df_combined['DateTime'].dt.tz_localize('UTC').dt.tz_convert(self.ny_tz)
        
        print(f"\n✅ Loaded {len(df_combined):,} candles from {df_combined['DateTime'].min()} to {df_combined['DateTime'].max()}")
        
        self.df_all = df_combined
        return df_combined
    
    def detect_fvg(self, candle_1: pd.Series, candle_2: pd.Series, candle_3: pd.Series) -> Optional[Dict]:
        """
        Detect Fair Value Gap (FVG) between three consecutive candles.
        
        Args:
            candle_1: First candle (n-1)
            candle_2: Middle candle (n)
            candle_3: Third candle (n+1)
            
        Returns:
            FVG dictionary or None
        """
        # Bullish FVG: High of candle_1 < Low of candle_3
        if candle_1['High'] < candle_3['Low']:
            return {
                'type': 'BULLISH',
                'lower_bound': candle_1['High'],
                'upper_bound': candle_3['Low'],
                'gap_size': candle_3['Low'] - candle_1['High']
            }
        
        # Bearish FVG: Low of candle_1 > High of candle_3
        if candle_1['Low'] > candle_3['High']:
            return {
                'type': 'BEARISH',
                'lower_bound': candle_3['High'],
                'upper_bound': candle_1['Low'],
                'gap_size': candle_1['Low'] - candle_3['High']
            }
        
        return None
    
    def find_all_daily_fvgs(self, day_data: pd.DataFrame) -> List[Dict]:
        """
        Find ALL FVGs between 08:30 and 09:00 NY time.
        
        Args:
            day_data: DataFrame containing one day's data
            
        Returns:
            List of FVG dictionaries
        """
        # Filter data between 08:30 and 09:00
        search_window = day_data[
            (day_data['DateTime'].dt.time >= time(8, 30)) &
            (day_data['DateTime'].dt.time < time(9, 0))
        ].copy()
        
        if len(search_window) < 3:
            return []
        
        fvgs = []
        
        # Search for ALL FVGs in this window
        for i in range(len(search_window) - 2):
            candle_1 = search_window.iloc[i]
            candle_2 = search_window.iloc[i + 1]
            candle_3 = search_window.iloc[i + 2]
            
            fvg = self.detect_fvg(candle_1, candle_2, candle_3)
            if fvg:
                fvg['detection_time'] = candle_3['DateTime']
                fvg['detection_idx'] = candle_3.name
                fvgs.append(fvg)
        
        return fvgs
    
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
        
        # Look for entry trigger
        for idx, candle in after_fvg.iterrows():
            if fvg['type'] == 'BULLISH':
                # SHORT entry: Close below lower bound of FVG (High of n-1)
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
            
            elif fvg['type'] == 'BEARISH':
                # LONG entry: Close above upper bound of FVG (Low of n-1)
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
        Simulate trade execution with stop loss and single take profit level.
        
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
        
        # Calculate take profit based on RR level
        if trade_type == 'LONG':
            tp_price = entry_price + (self.rr_level * risk)
        else:  # SHORT
            tp_price = entry_price - (self.rr_level * risk)
        
        # Initialize result
        result = {
            'date': entry['entry_time'].date(),
            'type': trade_type,
            'entry_price': entry_price,
            'stop_loss': stop_loss,
            'risk': risk,
            'rr_level': self.rr_level,
            'tp_price': tp_price,
            'tp_hit': False,
            'sl_hit': False,
            'pnl': 0.0,
            'exit_price': 0.0,
            'exit_reason': ''
        }
        
        # Get bars after entry
        after_entry = day_data[day_data.index > entry['entry_idx']].copy()
        
        # Simulate bar by bar
        for idx, candle in after_entry.iterrows():
            high = candle['High']
            low = candle['Low']
            
            if trade_type == 'LONG':
                # Check stop loss first
                if low <= stop_loss:
                    result['sl_hit'] = True
                    result['pnl'] = stop_loss - entry_price
                    result['exit_price'] = stop_loss
                    result['exit_reason'] = 'SL'
                    break
                
                # Check take profit
                if high >= tp_price:
                    result['tp_hit'] = True
                    result['pnl'] = tp_price - entry_price
                    result['exit_price'] = tp_price
                    result['exit_reason'] = f'TP{self.rr_level}R'
                    break
            
            else:  # SHORT
                # Check stop loss first
                if high >= stop_loss:
                    result['sl_hit'] = True
                    result['pnl'] = entry_price - stop_loss
                    result['exit_price'] = stop_loss
                    result['exit_reason'] = 'SL'
                    break
                
                # Check take profit
                if low <= tp_price:
                    result['tp_hit'] = True
                    result['pnl'] = entry_price - tp_price
                    result['exit_price'] = tp_price
                    result['exit_reason'] = f'TP{self.rr_level}R'
                    break
        
        # If neither TP nor SL hit, close at end of day
        if not result['tp_hit'] and not result['sl_hit']:
            last_close = after_entry.iloc[-1]['Close'] if len(after_entry) > 0 else entry_price
            if trade_type == 'LONG':
                result['pnl'] = last_close - entry_price
            else:
                result['pnl'] = entry_price - last_close
            result['exit_price'] = last_close
            result['exit_reason'] = 'EOD'
        
        return result
    
    def run_backtest(self) -> List[Dict]:
        """
        Run the complete backtest on all data.
        
        Returns:
            List of trade results
        """
        if self.df_all is None:
            self.load_data()
        
        print(f"\n🔍 Running backtest with {self.rr_level}R take profit level...")
        print(f"   Looking for ALL FVGs in 08:30-09:00 window")
        
        # Group by date
        self.df_all['Date'] = self.df_all['DateTime'].dt.date
        grouped = self.df_all.groupby('Date')
        
        total_days = len(grouped)
        total_fvgs = 0
        days_with_fvgs = 0
        
        print(f"   Processing {total_days} trading days...")
        
        # Process each day
        for date, day_data in grouped:
            day_data = day_data.reset_index(drop=True)
            
            # Find ALL FVGs for this day
            fvgs = self.find_all_daily_fvgs(day_data)
            
            if fvgs:
                days_with_fvgs += 1
                total_fvgs += len(fvgs)
                
                # Process each FVG
                for fvg in fvgs:
                    # Look for entry signal
                    entry = self.find_entry_signal(day_data, fvg, fvg['detection_idx'])
                    
                    if entry:
                        # Simulate trade
                        result = self.simulate_trade(day_data, entry)
                        self.trades.append(result)
        
        print(f"\n✅ Backtest complete!")
        print(f"   Total days analyzed: {total_days}")
        print(f"   Days with FVGs: {days_with_fvgs}")
        print(f"   Total FVGs found: {total_fvgs}")
        print(f"   Trades executed: {len(self.trades)}")
        
        return self.trades
    
    def calculate_statistics(self) -> Dict:
        """
        Calculate comprehensive backtest statistics.
        
        Returns:
            Dictionary of statistics
        """
        if not self.trades:
            return {}
        
        df = pd.DataFrame(self.trades)
        
        # Overall metrics
        total_trades = len(df)
        winning_trades = len(df[df['pnl'] > 0])
        losing_trades = len(df[df['pnl'] < 0])
        overall_win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
        
        # TP/SL metrics
        tp_hit_count = df['tp_hit'].sum()
        sl_hit_count = df['sl_hit'].sum()
        tp_win_rate = (tp_hit_count / total_trades * 100) if total_trades > 0 else 0
        
        # PnL metrics
        total_pnl = df['pnl'].sum()
        avg_pnl = df['pnl'].mean()
        
        winning_pnl = df[df['pnl'] > 0]['pnl']
        losing_pnl = df[df['pnl'] < 0]['pnl']
        
        avg_winning_trade = winning_pnl.mean() if len(winning_pnl) > 0 else 0
        avg_losing_trade = losing_pnl.mean() if len(losing_pnl) > 0 else 0
        
        gross_profit = winning_pnl.sum() if len(winning_pnl) > 0 else 0
        gross_loss = abs(losing_pnl.sum()) if len(losing_pnl) > 0 else 0
        
        profit_factor = (gross_profit / gross_loss) if gross_loss > 0 else 0
        
        # Drawdown
        cumulative_pnl = df['pnl'].cumsum()
        running_max = cumulative_pnl.expanding().max()
        drawdown = cumulative_pnl - running_max
        max_drawdown = abs(drawdown.min())
        
        # Risk metrics
        avg_risk = df['risk'].mean()
        
        # Trade type breakdown
        long_trades = len(df[df['type'] == 'LONG'])
        short_trades = len(df[df['type'] == 'SHORT'])
        
        long_wins = len(df[(df['type'] == 'LONG') & (df['pnl'] > 0)])
        short_wins = len(df[(df['type'] == 'SHORT') & (df['pnl'] > 0)])
        
        long_win_rate = (long_wins / long_trades * 100) if long_trades > 0 else 0
        short_win_rate = (short_wins / short_trades * 100) if short_trades > 0 else 0
        
        # Expectancy
        expectancy = avg_pnl
        
        stats = {
            'rr_level': self.rr_level,
            'total_trades': total_trades,
            'winning_trades': winning_trades,
            'losing_trades': losing_trades,
            'overall_win_rate': overall_win_rate,
            'tp_hit_count': tp_hit_count,
            'sl_hit_count': sl_hit_count,
            'tp_win_rate': tp_win_rate,
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
            'short_win_rate': short_win_rate,
            'expectancy': expectancy
        }
        
        return stats
    
    def display_results(self):
        """Display backtest results and statistics."""
        if not self.trades:
            print("\nNo trades to display!")
            return None
        
        # Create results DataFrame
        df_results = pd.DataFrame(self.trades)
        
        # Calculate statistics
        stats = self.calculate_statistics()
        
        print("\n" + "="*80)
        print(f"BACKTEST RESULTS - {self.rr_level}R TAKE PROFIT")
        print("="*80)
        
        print("\n📊 OVERALL STATISTICS")
        print("-" * 80)
        print(f"Total Trades:              {stats['total_trades']:,}")
        print(f"Winning Trades:            {stats['winning_trades']:,}")
        print(f"Losing Trades:             {stats['losing_trades']:,}")
        print(f"Overall Win Rate:          {stats['overall_win_rate']:.2f}%")
        
        print("\n🎯 TARGET ANALYSIS")
        print("-" * 80)
        print(f"TP ({self.rr_level}R) Hit Count:      {stats['tp_hit_count']:,} ({stats['tp_win_rate']:.2f}%)")
        print(f"SL Hit Count:              {stats['sl_hit_count']:,}")
        
        print("\n💰 PROFIT & LOSS")
        print("-" * 80)
        print(f"Total PnL:                 {stats['total_pnl']:.2f} points")
        print(f"Average PnL per Trade:     {stats['avg_pnl']:.2f} points")
        print(f"Expectancy:                {stats['expectancy']:.2f} points")
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
        
        return df_results, stats


def run_comparative_backtest():
    """Run backtest for all RR levels and compare results."""
    
    data_dir = "/home/runner/work/Backtest-Trading/Backtest-Trading"
    rr_levels = [1.0, 1.5, 2.0]
    
    print("\n" + "="*80)
    print("NY OPENING FVG BACKTEST - ALL FVGs, MULTIPLE RR LEVELS")
    print("Strategy: Fair Value Gap Breakout (NY Session 08:30-09:00)")
    print("Testing ALL FVGs found in the window")
    print("="*80)
    
    all_results = {}
    all_stats = {}
    
    # Run backtest for each RR level
    for rr in rr_levels:
        print(f"\n\n{'='*80}")
        print(f"RUNNING BACKTEST FOR {rr}R TAKE PROFIT")
        print('='*80)
        
        backtest = NYOpeningFVGBacktest(data_dir, rr_level=rr)
        trades = backtest.run_backtest()
        
        if trades:
            df_results, stats = backtest.display_results()
            all_results[rr] = df_results
            all_stats[rr] = stats
            
            # Save individual results
            output_file = os.path.join(data_dir, f'ny_opening_fvg_all_{rr}R_results.csv')
            df_results.to_csv(output_file, index=False)
            print(f"\n✅ Results saved to: {output_file}")
        else:
            print(f"\n⚠️ No trades for {rr}R level")
    
    # Display comparative summary
    print("\n\n" + "="*80)
    print("COMPARATIVE SUMMARY - ALL RR LEVELS")
    print("="*80)
    
    if all_stats:
        print("\n📊 KEY METRICS COMPARISON")
        print("-" * 80)
        print(f"{'Metric':<30} {'1.0R':>15} {'1.5R':>15} {'2.0R':>15}")
        print("-" * 80)
        
        metrics = [
            ('Total Trades', 'total_trades', ',.0f'),
            ('Win Rate (%)', 'overall_win_rate', '.2f'),
            ('TP Hit Rate (%)', 'tp_win_rate', '.2f'),
            ('Total PnL (pts)', 'total_pnl', '.2f'),
            ('Avg PnL (pts)', 'avg_pnl', '.2f'),
            ('Expectancy (pts)', 'expectancy', '.2f'),
            ('Profit Factor', 'profit_factor', '.2f'),
            ('Max DD (pts)', 'max_drawdown', '.2f'),
            ('Avg Risk (pts)', 'avg_risk', '.2f'),
        ]
        
        for label, key, fmt in metrics:
            values = [all_stats.get(rr, {}).get(key, 0) for rr in rr_levels]
            print(f"{label:<30} {values[0]:>15{fmt}} {values[1]:>15{fmt}} {values[2]:>15{fmt}}")
        
        print("-" * 80)
        
        # Best performer analysis
        print("\n🏆 BEST PERFORMERS")
        print("-" * 80)
        
        best_win_rate = max(rr_levels, key=lambda x: all_stats.get(x, {}).get('overall_win_rate', 0))
        best_pnl = max(rr_levels, key=lambda x: all_stats.get(x, {}).get('total_pnl', 0))
        best_expectancy = max(rr_levels, key=lambda x: all_stats.get(x, {}).get('expectancy', 0))
        best_pf = max(rr_levels, key=lambda x: all_stats.get(x, {}).get('profit_factor', 0))
        
        print(f"Best Win Rate:             {best_win_rate}R ({all_stats[best_win_rate]['overall_win_rate']:.2f}%)")
        print(f"Best Total PnL:            {best_pnl}R ({all_stats[best_pnl]['total_pnl']:.2f} pts)")
        print(f"Best Expectancy:           {best_expectancy}R ({all_stats[best_expectancy]['expectancy']:.2f} pts)")
        print(f"Best Profit Factor:        {best_pf}R ({all_stats[best_pf]['profit_factor']:.2f})")
    
    print("\n" + "="*80)
    print("BACKTEST COMPLETED SUCCESSFULLY!")
    print("="*80 + "\n")
    
    return all_results, all_stats


def main():
    """Main execution function."""
    run_comparative_backtest()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
NQ Futures - First FVG Inversion Backtesting Strategy
======================================================
Strategy: First FVG Inversion with "One Bullet" rule per session
Timeframe: 1-minute data
Sessions: London (01:00-04:00 CT) and New York (08:30-11:00 CT)
Author: Senior Quantitative Trader
"""

import pandas as pd
import numpy as np
import zipfile
import os
from datetime import datetime, time
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')


class FVGInversionBacktest:
    """Backtesting engine for FVG Inversion strategy on NQ Futures"""
    
    # Maximum candles to look ahead for trade exit (~8 hours at 1-min timeframe)
    MAX_TRADE_DURATION = 500
    
    # Profit factor value when there are no losses (all winning trades)
    INFINITE_PROFIT_FACTOR = 9999.99
    
    def __init__(self, data_path='/home/runner/work/Backtest-Trading/Backtest-Trading'):
        self.data_path = data_path
        self.df = None
        self.trades = []
        
        # Session definitions (Chicago Time)
        self.london_start = time(1, 0)
        self.london_end = time(4, 0)
        self.ny_start = time(8, 30)
        self.ny_end = time(11, 0)
        
    def load_data(self):
        """Load and combine 1-minute data from 2018-2024 (zip files) and 2025 (CSV)"""
        print("Loading data files...")
        all_data = []
        
        # Load zip files for 2018-2024
        for year in range(2018, 2025):
            zip_file = os.path.join(self.data_path, f'{year} 1m.csv.zip')
            if os.path.exists(zip_file):
                print(f"  Loading {year} data from zip...")
                with zipfile.ZipFile(zip_file, 'r') as z:
                    csv_name = f'{year} 1m.csv'
                    with z.open(csv_name) as f:
                        df_year = pd.read_csv(f, sep=';')
                        all_data.append(df_year)
            else:
                print(f"  Warning: {zip_file} not found, skipping...")
        
        # Load 2025 CSV (unzipped)
        csv_2025 = os.path.join(self.data_path, '2025 1m.csv')
        if os.path.exists(csv_2025):
            print(f"  Loading 2025 data from CSV...")
            df_2025 = pd.read_csv(csv_2025, sep=';')
            all_data.append(df_2025)
        
        # Combine all dataframes
        print("Combining all data...")
        self.df = pd.concat(all_data, ignore_index=True)
        
        # Rename columns
        self.df.columns = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
        
        # Create datetime column (data is already in Chicago Time)
        # Use dayfirst=False to prioritize MM/DD/YYYY format
        self.df['DateTime'] = pd.to_datetime(
            self.df['Date'] + ' ' + self.df['Time'], 
            format='mixed',
            dayfirst=False
        )
        
        # Sort by datetime
        self.df = self.df.sort_values('DateTime').reset_index(drop=True)
        
        # Extract time for session filtering
        self.df['TimeOnly'] = self.df['DateTime'].dt.time
        
        print(f"Data loaded: {len(self.df):,} rows from {self.df['DateTime'].min()} to {self.df['DateTime'].max()}")
        print(f"Columns: {list(self.df.columns)}")
        
        return self.df
    
    def identify_fvg(self):
        """
        Identify Fair Value Gaps (FVGs)
        - Bearish FVG: Low[i-2] > High[i] (gap between High[i] and Low[i-2])
        - Bullish FVG: High[i-2] < Low[i] (gap between High[i-2] and Low[i])
        """
        print("\nIdentifying FVGs...")
        
        # Initialize columns
        self.df['FVG_Type'] = None  # 'Bearish' or 'Bullish'
        self.df['FVG_Top'] = np.nan
        self.df['FVG_Bottom'] = np.nan
        
        # Need at least 3 candles to form an FVG
        for i in range(2, len(self.df)):
            high_i = self.df.loc[i, 'High']
            low_i = self.df.loc[i, 'Low']
            high_i2 = self.df.loc[i-2, 'High']
            low_i2 = self.df.loc[i-2, 'Low']
            
            # Bearish FVG: Low[i-2] > High[i]
            if low_i2 > high_i:
                self.df.loc[i, 'FVG_Type'] = 'Bearish'
                self.df.loc[i, 'FVG_Top'] = low_i2
                self.df.loc[i, 'FVG_Bottom'] = high_i
            
            # Bullish FVG: High[i-2] < Low[i]
            elif high_i2 < low_i:
                self.df.loc[i, 'FVG_Type'] = 'Bullish'
                self.df.loc[i, 'FVG_Top'] = low_i
                self.df.loc[i, 'FVG_Bottom'] = high_i2
        
        bearish_count = (self.df['FVG_Type'] == 'Bearish').sum()
        bullish_count = (self.df['FVG_Type'] == 'Bullish').sum()
        print(f"  Bearish FVGs: {bearish_count:,}")
        print(f"  Bullish FVGs: {bullish_count:,}")
        
    def get_session(self, time_val):
        """Determine which session a given time belongs to"""
        if self.london_start <= time_val < self.london_end:
            return 'London'
        elif self.ny_start <= time_val < self.ny_end:
            return 'New York'
        else:
            return None
    
    def backtest_strategy(self):
        """
        Execute the FVG Inversion backtest with "One Bullet" rule
        Entry Logic:
        - LONG: Bearish FVG created, later candle closes ABOVE FVG top
        - SHORT: Bullish FVG created, later candle closes BELOW FVG bottom
        """
        print("\nRunning backtest...")
        
        self.trades = []
        active_fvgs = []  # Store FVGs that haven't been triggered yet
        current_session = None
        session_date = None
        trade_taken_in_session = False
        
        for i in range(len(self.df)):
            row = self.df.iloc[i]
            current_time = row['TimeOnly']
            current_date = row['DateTime'].date()
            session = self.get_session(current_time)
            
            # Check if we're in a new session (reset trade flag)
            if session is not None:
                if session != current_session or current_date != session_date:
                    # New session started
                    current_session = session
                    session_date = current_date
                    trade_taken_in_session = False
                    # Clear FVGs from previous session
                    active_fvgs = []
            
            # Add new FVG to active list if in session
            if session is not None and pd.notna(row['FVG_Type']):
                fvg = {
                    'type': row['FVG_Type'],
                    'top': row['FVG_Top'],
                    'bottom': row['FVG_Bottom'],
                    'created_at': row['DateTime'],
                    'created_index': i
                }
                active_fvgs.append(fvg)
            
            # Check for inversion signals (only if no trade taken in current session)
            if session is not None and not trade_taken_in_session:
                for fvg in active_fvgs:
                    # Skip if FVG was just created (need at least next candle)
                    if fvg['created_index'] >= i:
                        continue
                    
                    # LONG Signal: Bearish FVG + Close above FVG top
                    if fvg['type'] == 'Bearish' and row['Close'] > fvg['top']:
                        entry_price = row['Close']
                        stop_loss = row['Low']
                        risk = entry_price - stop_loss
                        take_profit = entry_price + risk
                        
                        trade = {
                            'entry_time': row['DateTime'],
                            'entry_price': entry_price,
                            'direction': 'LONG',
                            'stop_loss': stop_loss,
                            'take_profit': take_profit,
                            'session': session,
                            'fvg_created_at': fvg['created_at'],
                            'entry_index': i
                        }
                        self.trades.append(trade)
                        trade_taken_in_session = True
                        active_fvgs = []  # Clear FVGs after taking trade
                        break
                    
                    # SHORT Signal: Bullish FVG + Close below FVG bottom
                    elif fvg['type'] == 'Bullish' and row['Close'] < fvg['bottom']:
                        entry_price = row['Close']
                        stop_loss = row['High']
                        risk = stop_loss - entry_price
                        take_profit = entry_price - risk
                        
                        trade = {
                            'entry_time': row['DateTime'],
                            'entry_price': entry_price,
                            'direction': 'SHORT',
                            'stop_loss': stop_loss,
                            'take_profit': take_profit,
                            'session': session,
                            'fvg_created_at': fvg['created_at'],
                            'entry_index': i
                        }
                        self.trades.append(trade)
                        trade_taken_in_session = True
                        active_fvgs = []  # Clear FVGs after taking trade
                        break
        
        print(f"Total trades executed: {len(self.trades)}")
        
    def evaluate_trades(self):
        """Evaluate trade outcomes (win/loss) based on subsequent price action"""
        print("\nEvaluating trade outcomes...")
        
        for trade in self.trades:
            entry_idx = trade['entry_index']
            direction = trade['direction']
            stop_loss = trade['stop_loss']
            take_profit = trade['take_profit']
            
            # Look at subsequent candles to determine win/loss
            trade['outcome'] = None
            trade['exit_time'] = None
            trade['exit_price'] = None
            trade['pnl'] = 0
            
            # Scan subsequent candles (limit to MAX_TRADE_DURATION candles ~ 8 hours)
            max_look_ahead = min(entry_idx + self.MAX_TRADE_DURATION, len(self.df))
            
            for j in range(entry_idx + 1, max_look_ahead):
                candle = self.df.iloc[j]
                
                if direction == 'LONG':
                    # Check if stop loss hit
                    if candle['Low'] <= stop_loss:
                        trade['outcome'] = 'Loss'
                        trade['exit_time'] = candle['DateTime']
                        trade['exit_price'] = stop_loss
                        trade['pnl'] = stop_loss - trade['entry_price']
                        break
                    # Check if take profit hit
                    elif candle['High'] >= take_profit:
                        trade['outcome'] = 'Win'
                        trade['exit_time'] = candle['DateTime']
                        trade['exit_price'] = take_profit
                        trade['pnl'] = take_profit - trade['entry_price']
                        break
                
                elif direction == 'SHORT':
                    # Check if stop loss hit
                    if candle['High'] >= stop_loss:
                        trade['outcome'] = 'Loss'
                        trade['exit_time'] = candle['DateTime']
                        trade['exit_price'] = stop_loss
                        trade['pnl'] = trade['entry_price'] - stop_loss
                        break
                    # Check if take profit hit
                    elif candle['Low'] <= take_profit:
                        trade['outcome'] = 'Win'
                        trade['exit_time'] = candle['DateTime']
                        trade['exit_price'] = take_profit
                        trade['pnl'] = trade['entry_price'] - take_profit
                        break
            
            # If no outcome determined, mark as open/unresolved
            if trade['outcome'] is None:
                trade['outcome'] = 'Open'
                trade['exit_time'] = self.df.iloc[-1]['DateTime']
                trade['exit_price'] = self.df.iloc[-1]['Close']
                if direction == 'LONG':
                    trade['pnl'] = trade['exit_price'] - trade['entry_price']
                else:
                    trade['pnl'] = trade['entry_price'] - trade['exit_price']
        
        wins = sum(1 for t in self.trades if t['outcome'] == 'Win')
        losses = sum(1 for t in self.trades if t['outcome'] == 'Loss')
        open_trades = sum(1 for t in self.trades if t['outcome'] == 'Open')
        
        print(f"  Wins: {wins}")
        print(f"  Losses: {losses}")
        print(f"  Open/Unresolved: {open_trades}")
    
    def calculate_metrics(self, trades_subset, label=""):
        """Calculate performance metrics for a subset of trades"""
        if len(trades_subset) == 0:
            return None
        
        wins = [t for t in trades_subset if t['outcome'] == 'Win']
        losses = [t for t in trades_subset if t['outcome'] == 'Loss']
        
        total_trades = len(trades_subset)
        num_wins = len(wins)
        num_losses = len(losses)
        
        win_rate = (num_wins / total_trades * 100) if total_trades > 0 else 0
        
        gross_profit = sum(t['pnl'] for t in wins)
        gross_loss = abs(sum(t['pnl'] for t in losses))
        
        # Handle profit factor calculation
        # Profit Factor = Gross Profit / Gross Loss
        if gross_loss > 0:
            profit_factor = gross_profit / gross_loss
        elif gross_profit > 0:
            # All winning trades, no losses - use very large number
            profit_factor = self.INFINITE_PROFIT_FACTOR
        else:
            # No profit or loss
            profit_factor = 0
        
        net_profit = sum(t['pnl'] for t in trades_subset)
        
        # Calculate max drawdown
        cumulative = [0]
        for t in trades_subset:
            cumulative.append(cumulative[-1] + t['pnl'])
        
        peak = cumulative[0]
        max_dd = 0
        for val in cumulative:
            if val > peak:
                peak = val
            dd = peak - val
            if dd > max_dd:
                max_dd = dd
        
        metrics = {
            'label': label,
            'total_trades': total_trades,
            'wins': num_wins,
            'losses': num_losses,
            'win_rate': win_rate,
            'gross_profit': gross_profit,
            'gross_loss': gross_loss,
            'profit_factor': profit_factor,
            'net_profit': net_profit,
            'max_drawdown': max_dd
        }
        
        return metrics
    
    def generate_report(self):
        """Generate comprehensive performance report"""
        print("\n" + "="*80)
        print("PERFORMANCE REPORT - FVG INVERSION STRATEGY")
        print("="*80)
        
        # Overall metrics
        overall = self.calculate_metrics(self.trades, "Overall")
        
        # London session metrics
        london_trades = [t for t in self.trades if t['session'] == 'London']
        london = self.calculate_metrics(london_trades, "London Session")
        
        # New York session metrics
        ny_trades = [t for t in self.trades if t['session'] == 'New York']
        ny = self.calculate_metrics(ny_trades, "New York Session")
        
        # Print reports
        for metrics in [overall, london, ny]:
            if metrics:
                print(f"\n{metrics['label']}")
                print("-" * 80)
                print(f"  Total Trades:      {metrics['total_trades']}")
                print(f"  Wins:              {metrics['wins']}")
                print(f"  Losses:            {metrics['losses']}")
                print(f"  Win Rate:          {metrics['win_rate']:.2f}%")
                print(f"  Gross Profit:      ${metrics['gross_profit']:.2f}")
                print(f"  Gross Loss:        ${metrics['gross_loss']:.2f}")
                print(f"  Profit Factor:     {metrics['profit_factor']:.2f}")
                print(f"  Net Profit:        ${metrics['net_profit']:.2f}")
                print(f"  Max Drawdown:      ${metrics['max_drawdown']:.2f}")
        
        print("\n" + "="*80)
        
        return overall, london, ny
    
    def plot_equity_curve(self):
        """Plot cumulative equity curve"""
        print("\nGenerating equity curve plot...")
        
        # Calculate cumulative equity
        cumulative_equity = [0]
        dates = [self.trades[0]['entry_time'] if self.trades else datetime.now()]
        
        for trade in self.trades:
            cumulative_equity.append(cumulative_equity[-1] + trade['pnl'])
            dates.append(trade['exit_time'] if trade['exit_time'] else trade['entry_time'])
        
        # Create plot
        fig, axes = plt.subplots(2, 1, figsize=(14, 10))
        
        # Overall equity curve
        axes[0].plot(dates, cumulative_equity, linewidth=2, color='blue')
        axes[0].axhline(y=0, color='black', linestyle='--', alpha=0.3)
        axes[0].set_title('Cumulative Equity Curve - FVG Inversion Strategy', fontsize=14, fontweight='bold')
        axes[0].set_xlabel('Date')
        axes[0].set_ylabel('Cumulative P&L ($)')
        axes[0].grid(True, alpha=0.3)
        axes[0].tick_params(axis='x', rotation=45)
        
        # Session-separated equity curves
        london_trades = [t for t in self.trades if t['session'] == 'London']
        ny_trades = [t for t in self.trades if t['session'] == 'New York']
        
        # London cumulative
        london_cum = [0]
        london_dates = [london_trades[0]['entry_time'] if london_trades else datetime.now()]
        for trade in london_trades:
            london_cum.append(london_cum[-1] + trade['pnl'])
            london_dates.append(trade['exit_time'] if trade['exit_time'] else trade['entry_time'])
        
        # NY cumulative
        ny_cum = [0]
        ny_dates = [ny_trades[0]['entry_time'] if ny_trades else datetime.now()]
        for trade in ny_trades:
            ny_cum.append(ny_cum[-1] + trade['pnl'])
            ny_dates.append(trade['exit_time'] if trade['exit_time'] else trade['entry_time'])
        
        axes[1].plot(london_dates, london_cum, linewidth=2, color='green', label='London (01:00-04:00 CT)')
        axes[1].plot(ny_dates, ny_cum, linewidth=2, color='red', label='New York (08:30-11:00 CT)')
        axes[1].axhline(y=0, color='black', linestyle='--', alpha=0.3)
        axes[1].set_title('Cumulative Equity by Session', fontsize=14, fontweight='bold')
        axes[1].set_xlabel('Date')
        axes[1].set_ylabel('Cumulative P&L ($)')
        axes[1].legend(loc='best')
        axes[1].grid(True, alpha=0.3)
        axes[1].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        
        # Save plot
        output_file = os.path.join(self.data_path, 'fvg_inversion_equity_curve.png')
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Equity curve saved to: {output_file}")
        
        plt.close()
    
    def save_trades_to_csv(self):
        """Save all trades to CSV for further analysis"""
        if not self.trades:
            print("No trades to save.")
            return
        
        trades_df = pd.DataFrame(self.trades)
        output_file = os.path.join(self.data_path, 'fvg_inversion_trades.csv')
        trades_df.to_csv(output_file, index=False)
        print(f"\nTrades saved to: {output_file}")
    
    def run(self):
        """Execute the complete backtesting process"""
        print("\n" + "="*80)
        print("NQ FUTURES - FVG INVERSION BACKTEST")
        print("="*80)
        
        # Load data
        self.load_data()
        
        # Identify FVGs
        self.identify_fvg()
        
        # Run backtest
        self.backtest_strategy()
        
        # Evaluate trades
        self.evaluate_trades()
        
        # Generate report
        self.generate_report()
        
        # Plot equity curve
        self.plot_equity_curve()
        
        # Save trades
        self.save_trades_to_csv()
        
        print("\n" + "="*80)
        print("BACKTEST COMPLETE")
        print("="*80)


if __name__ == "__main__":
    # Initialize and run backtest
    backtest = FVGInversionBacktest()
    backtest.run()

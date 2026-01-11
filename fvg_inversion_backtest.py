#!/usr/bin/env python3
"""
FVG Inversion Backtesting System for NQ (Nasdaq 100) Futures
Strategy: Fair Value Gap (FVG) Inversion on 1-minute data
Sessions: London (01:00-04:00 CT) and New York (08:30-11:00 CT)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, time
import os

class FVGInversionBacktest:
    """
    Backtesting engine for FVG Inversion strategy.
    
    FVG Definitions:
    - Bearish FVG: Low[i-2] > High[i]. Gap between High[i] and Low[i-2]
    - Bullish FVG: High[i-2] < Low[i]. Gap between High[i-2] and Low[i]
    
    Entry Triggers (Inversion):
    - LONG: Bearish FVG created, later candle closes ABOVE top of Bearish FVG
    - SHORT: Bullish FVG created, later candle closes BELOW bottom of Bullish FVG
    
    One Bullet Rule: Only first signal per session is taken
    """
    
    def __init__(self, data_file):
        """Initialize the backtester with data file."""
        print(f"Loading data from {data_file}...")
        self.df = pd.read_csv(data_file)
        self.df['Datetime'] = pd.to_datetime(self.df['Datetime'])
        self.df['Time'] = self.df['Datetime'].dt.time
        self.df['Date'] = self.df['Datetime'].dt.date
        
        print(f"✓ Loaded {len(self.df)} rows")
        print(f"  Date range: {self.df['Datetime'].min()} to {self.df['Datetime'].max()}")
        
        # Sessions (Chicago Time)
        self.london_start = time(1, 0)   # 01:00
        self.london_end = time(4, 0)     # 04:00
        self.ny_start = time(8, 30)      # 08:30
        self.ny_end = time(11, 0)        # 11:00
        
        # Results storage
        self.trades = []
        self.equity_curve = []
        
    def identify_fvgs(self):
        """
        Identify Fair Value Gaps in the data.
        Returns dataframe with FVG information.
        """
        print("\nIdentifying Fair Value Gaps...")
        
        fvgs = []
        
        for i in range(2, len(self.df)):
            # Get relevant candles
            current = self.df.iloc[i]
            prev1 = self.df.iloc[i-1]
            prev2 = self.df.iloc[i-2]
            
            # Bearish FVG: Low[i-2] > High[i]
            if prev2['Low'] > current['High']:
                fvgs.append({
                    'index': i,
                    'datetime': current['Datetime'],
                    'type': 'bearish',
                    'top': prev2['Low'],
                    'bottom': current['High'],
                    'used': False
                })
            
            # Bullish FVG: High[i-2] < Low[i]
            elif prev2['High'] < current['Low']:
                fvgs.append({
                    'index': i,
                    'datetime': current['Datetime'],
                    'type': 'bullish',
                    'top': current['Low'],
                    'bottom': prev2['High'],
                    'used': False
                })
        
        print(f"✓ Found {len(fvgs)} FVGs")
        return fvgs
    
    def get_session(self, time_obj):
        """Determine which session a time belongs to."""
        if self.london_start <= time_obj < self.london_end:
            return 'London'
        elif self.ny_start <= time_obj < self.ny_end:
            return 'New York'
        return None
    
    def run_backtest(self):
        """
        Execute the FVG Inversion backtest with One Bullet rule.
        """
        print("\n" + "="*60)
        print("STARTING FVG INVERSION BACKTEST")
        print("="*60)
        
        # Identify all FVGs
        fvgs = self.identify_fvgs()
        
        if not fvgs:
            print("No FVGs found. Exiting.")
            return
        
        print("\nExecuting backtest with One Bullet rule...")
        
        # Track trades per session
        current_date = None
        london_trade_taken = False
        ny_trade_taken = False
        
        # For each potential signal candle
        for i in range(len(self.df)):
            candle = self.df.iloc[i]
            candle_time = candle['Time']
            candle_date = candle['Date']
            session = self.get_session(candle_time)
            
            # Reset daily flags at start of new day
            if candle_date != current_date:
                current_date = candle_date
                london_trade_taken = False
                ny_trade_taken = False
            
            # Reset NY flag when NY session starts
            if session == 'New York' and candle_time == self.ny_start:
                ny_trade_taken = False
            
            # Skip if not in a valid session
            if session is None:
                continue
            
            # Check One Bullet rule
            if session == 'London' and london_trade_taken:
                continue
            if session == 'New York' and ny_trade_taken:
                continue
            
            # Check for signal: Look for FVG inversions
            for fvg in fvgs:
                # Skip if FVG is after current candle or already used
                if fvg['index'] >= i or fvg['used']:
                    continue
                
                signal = None
                
                # LONG Signal: Bearish FVG + Close ABOVE top
                if fvg['type'] == 'bearish' and candle['Close'] > fvg['top']:
                    signal = 'LONG'
                    entry_price = candle['Close']
                    stop_loss = candle['Low']
                    risk = entry_price - stop_loss
                    take_profit = entry_price + risk  # 1:1 RR
                
                # SHORT Signal: Bullish FVG + Close BELOW bottom
                elif fvg['type'] == 'bullish' and candle['Close'] < fvg['bottom']:
                    signal = 'SHORT'
                    entry_price = candle['Close']
                    stop_loss = candle['High']
                    risk = stop_loss - entry_price
                    take_profit = entry_price - risk  # 1:1 RR
                
                # If valid signal, execute trade
                if signal:
                    # Mark FVG as used
                    fvg['used'] = True
                    
                    # Execute trade
                    trade_result = self.execute_trade(
                        entry_idx=i,
                        signal=signal,
                        entry_price=entry_price,
                        stop_loss=stop_loss,
                        take_profit=take_profit,
                        session=session
                    )
                    
                    if trade_result:
                        self.trades.append(trade_result)
                        
                        # Mark session trade as taken (One Bullet)
                        if session == 'London':
                            london_trade_taken = True
                        else:
                            ny_trade_taken = True
                        
                        # Break to avoid multiple trades on same candle
                        break
        
        print(f"\n✓ Backtest complete. Total trades: {len(self.trades)}")
    
    def execute_trade(self, entry_idx, signal, entry_price, stop_loss, take_profit, session):
        """
        Simulate trade execution and find exit.
        """
        entry_candle = self.df.iloc[entry_idx]
        
        # Look for exit in subsequent candles
        for j in range(entry_idx + 1, len(self.df)):
            exit_candle = self.df.iloc[j]
            
            if signal == 'LONG':
                # Check for stop loss hit
                if exit_candle['Low'] <= stop_loss:
                    pnl = stop_loss - entry_price
                    exit_price = stop_loss
                    exit_reason = 'Stop Loss'
                    exit_datetime = exit_candle['Datetime']
                    break
                # Check for take profit hit
                elif exit_candle['High'] >= take_profit:
                    pnl = take_profit - entry_price
                    exit_price = take_profit
                    exit_reason = 'Take Profit'
                    exit_datetime = exit_candle['Datetime']
                    break
            
            else:  # SHORT
                # Check for stop loss hit
                if exit_candle['High'] >= stop_loss:
                    pnl = entry_price - stop_loss
                    exit_price = stop_loss
                    exit_reason = 'Stop Loss'
                    exit_datetime = exit_candle['Datetime']
                    break
                # Check for take profit hit
                elif exit_candle['Low'] <= take_profit:
                    pnl = entry_price - take_profit
                    exit_price = take_profit
                    exit_reason = 'Take Profit'
                    exit_datetime = exit_candle['Datetime']
                    break
        else:
            # Trade didn't exit (end of data)
            return None
        
        return {
            'entry_datetime': entry_candle['Datetime'],
            'exit_datetime': exit_datetime,
            'session': session,
            'signal': signal,
            'entry_price': entry_price,
            'exit_price': exit_price,
            'stop_loss': stop_loss,
            'take_profit': take_profit,
            'pnl': pnl,
            'exit_reason': exit_reason,
            'win': pnl > 0
        }
    
    def calculate_metrics(self, trades_subset, session_name):
        """Calculate performance metrics for a subset of trades."""
        if not trades_subset:
            return {
                'session': session_name,
                'total_trades': 0,
                'win_rate': 0,
                'profit_factor': 0,
                'max_drawdown': 0,
                'net_profit': 0
            }
        
        total_trades = len(trades_subset)
        wins = sum(1 for t in trades_subset if t['win'])
        losses = total_trades - wins
        win_rate = (wins / total_trades * 100) if total_trades > 0 else 0
        
        # Calculate profit factor
        gross_profit = sum(t['pnl'] for t in trades_subset if t['pnl'] > 0)
        gross_loss = abs(sum(t['pnl'] for t in trades_subset if t['pnl'] < 0))
        profit_factor = (gross_profit / gross_loss) if gross_loss > 0 else 0
        
        # Calculate max drawdown
        cumulative = 0
        peak = 0
        max_dd = 0
        for trade in trades_subset:
            cumulative += trade['pnl']
            if cumulative > peak:
                peak = cumulative
            drawdown = peak - cumulative
            if drawdown > max_dd:
                max_dd = drawdown
        
        net_profit = sum(t['pnl'] for t in trades_subset)
        
        return {
            'session': session_name,
            'total_trades': total_trades,
            'wins': wins,
            'losses': losses,
            'win_rate': win_rate,
            'profit_factor': profit_factor,
            'max_drawdown': max_dd,
            'net_profit': net_profit,
            'gross_profit': gross_profit,
            'gross_loss': gross_loss
        }
    
    def generate_report(self):
        """Generate detailed performance report."""
        print("\n" + "="*60)
        print("PERFORMANCE REPORT")
        print("="*60)
        
        if not self.trades:
            print("No trades executed.")
            return
        
        # Overall metrics
        overall = self.calculate_metrics(self.trades, 'Overall')
        
        # London session metrics
        london_trades = [t for t in self.trades if t['session'] == 'London']
        london = self.calculate_metrics(london_trades, 'London')
        
        # New York session metrics
        ny_trades = [t for t in self.trades if t['session'] == 'New York']
        ny = self.calculate_metrics(ny_trades, 'New York')
        
        # Print overall
        print("\n--- OVERALL PERFORMANCE ---")
        print(f"Total Trades:    {overall['total_trades']}")
        print(f"Wins / Losses:   {overall['wins']} / {overall['losses']}")
        print(f"Win Rate:        {overall['win_rate']:.2f}%")
        print(f"Profit Factor:   {overall['profit_factor']:.2f}")
        print(f"Net Profit:      ${overall['net_profit']:.2f}")
        print(f"Gross Profit:    ${overall['gross_profit']:.2f}")
        print(f"Gross Loss:      ${overall['gross_loss']:.2f}")
        print(f"Max Drawdown:    ${overall['max_drawdown']:.2f}")
        
        # Print London
        print("\n--- LONDON SESSION (01:00-04:00 CT) ---")
        print(f"Total Trades:    {london['total_trades']}")
        if london['total_trades'] > 0:
            print(f"Wins / Losses:   {london['wins']} / {london['losses']}")
            print(f"Win Rate:        {london['win_rate']:.2f}%")
            print(f"Profit Factor:   {london['profit_factor']:.2f}")
            print(f"Net Profit:      ${london['net_profit']:.2f}")
            print(f"Gross Profit:    ${london['gross_profit']:.2f}")
            print(f"Gross Loss:      ${london['gross_loss']:.2f}")
            print(f"Max Drawdown:    ${london['max_drawdown']:.2f}")
        
        # Print New York
        print("\n--- NEW YORK SESSION (08:30-11:00 CT) ---")
        print(f"Total Trades:    {ny['total_trades']}")
        if ny['total_trades'] > 0:
            print(f"Wins / Losses:   {ny['wins']} / {ny['losses']}")
            print(f"Win Rate:        {ny['win_rate']:.2f}%")
            print(f"Profit Factor:   {ny['profit_factor']:.2f}")
            print(f"Net Profit:      ${ny['net_profit']:.2f}")
            print(f"Gross Profit:    ${ny['gross_profit']:.2f}")
            print(f"Gross Loss:      ${ny['gross_loss']:.2f}")
            print(f"Max Drawdown:    ${ny['max_drawdown']:.2f}")
        
        print("\n" + "="*60)
        
        # Save detailed trades to CSV
        self.save_trades_to_csv()
        
        return overall, london, ny
    
    def save_trades_to_csv(self):
        """Save all trades to CSV file."""
        trades_df = pd.DataFrame(self.trades)
        filename = "fvg_inversion_trades.csv"
        trades_df.to_csv(filename, index=False)
        print(f"\n✓ Detailed trades saved to: {filename}")
    
    def plot_equity_curve(self):
        """Plot cumulative equity curve."""
        print("\nGenerating equity curve plot...")
        
        if not self.trades:
            print("No trades to plot.")
            return
        
        # Calculate cumulative P&L
        cumulative_pnl = []
        cumulative = 0
        dates = []
        
        for trade in self.trades:
            cumulative += trade['pnl']
            cumulative_pnl.append(cumulative)
            dates.append(trade['exit_datetime'])
        
        # Create plot
        plt.figure(figsize=(14, 7))
        plt.plot(dates, cumulative_pnl, linewidth=2, color='#2E86AB')
        plt.axhline(y=0, color='red', linestyle='--', alpha=0.5)
        plt.title('FVG Inversion Strategy - Cumulative Equity Curve', fontsize=16, fontweight='bold')
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Cumulative P&L ($)', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        # Save plot
        filename = "fvg_inversion_equity_curve.png"
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"✓ Equity curve saved to: {filename}")
        
        # Also create session comparison
        self.plot_session_comparison()
    
    def plot_session_comparison(self):
        """Plot session-by-session comparison."""
        london_trades = [t for t in self.trades if t['session'] == 'London']
        ny_trades = [t for t in self.trades if t['session'] == 'New York']
        
        # Calculate cumulative for each session
        london_cum = []
        london_dates = []
        cum = 0
        for t in london_trades:
            cum += t['pnl']
            london_cum.append(cum)
            london_dates.append(t['exit_datetime'])
        
        ny_cum = []
        ny_dates = []
        cum = 0
        for t in ny_trades:
            cum += t['pnl']
            ny_cum.append(cum)
            ny_dates.append(t['exit_datetime'])
        
        # Create plot
        fig, axes = plt.subplots(2, 1, figsize=(14, 10))
        
        # London
        if london_cum:
            axes[0].plot(london_dates, london_cum, linewidth=2, color='#A23B72')
            axes[0].axhline(y=0, color='red', linestyle='--', alpha=0.5)
            axes[0].set_title('London Session (01:00-04:00 CT)', fontsize=14, fontweight='bold')
            axes[0].set_ylabel('Cumulative P&L ($)', fontsize=11)
            axes[0].grid(True, alpha=0.3)
        
        # New York
        if ny_cum:
            axes[1].plot(ny_dates, ny_cum, linewidth=2, color='#F18F01')
            axes[1].axhline(y=0, color='red', linestyle='--', alpha=0.5)
            axes[1].set_title('New York Session (08:30-11:00 CT)', fontsize=14, fontweight='bold')
            axes[1].set_ylabel('Cumulative P&L ($)', fontsize=11)
            axes[1].set_xlabel('Date', fontsize=11)
            axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        filename = "fvg_inversion_session_comparison.png"
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"✓ Session comparison saved to: {filename}")


def main():
    """Main execution function."""
    print("="*60)
    print("FVG INVERSION BACKTESTING SYSTEM")
    print("NQ (Nasdaq 100) Futures - 1-Minute Data (2018-2024)")
    print("="*60)
    
    # Check if combined data file exists
    data_file = "NQ_1min_2018_2024.csv"
    
    if not os.path.exists(data_file):
        print(f"\n✗ Data file '{data_file}' not found.")
        print("Please run 'combine_data.py' first to create the combined dataset.")
        return
    
    # Initialize backtester
    backtester = FVGInversionBacktest(data_file)
    
    # Run backtest
    backtester.run_backtest()
    
    # Generate report
    backtester.generate_report()
    
    # Plot equity curve
    backtester.plot_equity_curve()
    
    print("\n" + "="*60)
    print("BACKTEST COMPLETE")
    print("="*60)
    print("\nGenerated files:")
    print("  - fvg_inversion_trades.csv (detailed trade list)")
    print("  - fvg_inversion_equity_curve.png (cumulative equity)")
    print("  - fvg_inversion_session_comparison.png (session breakdown)")
    print("\n")


if __name__ == "__main__":
    main()

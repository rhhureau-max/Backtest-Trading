"""
London Manipulation Strategy Backtest for NQ Futures
=====================================================

This script implements a complete backtest for the "London Manipulation" strategy
on NQ (Nasdaq 100 futures) from January 2018 to present.

Strategy Overview:
-----------------
1. Identify Asian Session Low (18:00 previous day to 02:00 EST)
2. Detect liquidity sweep below Asian Low during London Open (02:00-05:00 EST)
3. Identify Bearish Fair Value Gap (FVG) during sweep
4. Confirm inversion when price closes above FVG high
5. Enter LONG at next candle open
6. Risk Management: SL 1 tick below swing low, TP at 1:1 RR

Author: Backtest Trading System
Date: December 2025
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Constants
NQ_TICK_SIZE = 0.25  # 1 tick for NQ = 0.25 points
DATA_FILES = [
    "2018 5m.csv",
    "2019 5m.csv", 
    "2020 5m.csv",
    "2021 5m.csv",
    "2022 5m.csv",
    "2023 5m.csv",
    "2024 5m.csv",
    "2025 5m.csv"
]

class LondonManipulationBacktest:
    """Main backtest class for the London Manipulation strategy"""
    
    def __init__(self, data_directory="."):
        """
        Initialize the backtest
        
        Parameters:
        -----------
        data_directory : str
            Path to directory containing CSV data files
        """
        self.data_directory = data_directory
        self.data = None
        self.trades = []
        self.stats = {}
        
    def load_data(self):
        """Load and process all 5-minute NQ data files"""
        print("Loading data files...")
        all_data = []
        
        for filename in DATA_FILES:
            filepath = os.path.join(self.data_directory, filename)
            if not os.path.exists(filepath):
                print(f"Warning: {filename} not found, skipping...")
                continue
                
            print(f"  Loading {filename}...")
            df = pd.read_csv(filepath, sep=';', header=0, encoding='utf-8-sig')
            
            # The CSV has columns: Column1, Column2, ..., Column7
            # Which map to: Date, Time, Open, High, Low, Close, Volume
            df.columns = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
            
            # Combine Date and Time into datetime
            df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], 
                                           format='%d/%m/%Y %H:%M:%S')
            
            all_data.append(df)
        
        # Concatenate all data
        self.data = pd.concat(all_data, ignore_index=True)
        self.data = self.data.sort_values('DateTime').reset_index(drop=True)
        
        # Convert to EST timezone (assuming data is in UTC or needs timezone handling)
        # Note: We'll treat the times as EST since futures data is typically in exchange time
        self.data['EST_DateTime'] = self.data['DateTime']
        
        # Extract date and time components
        self.data['Date'] = self.data['EST_DateTime'].dt.date
        self.data['Time'] = self.data['EST_DateTime'].dt.time
        self.data['Hour'] = self.data['EST_DateTime'].dt.hour
        self.data['Minute'] = self.data['EST_DateTime'].dt.minute
        
        print(f"Total data loaded: {len(self.data)} rows")
        print(f"Date range: {self.data['EST_DateTime'].min()} to {self.data['EST_DateTime'].max()}")
        
        return self.data
    
    def get_time_in_minutes(self, hour, minute):
        """Convert hour and minute to minutes since midnight"""
        return hour * 60 + minute
    
    def is_asian_session(self, hour, minute):
        """
        Check if time is in Asian session (18:00 to 02:00 EST)
        Asian session spans from 18:00 previous day to 02:00
        """
        time_minutes = self.get_time_in_minutes(hour, minute)
        # 18:00 (1080 min) to 23:59 or 00:00 to 02:00 (120 min)
        return time_minutes >= 1080 or time_minutes < 120
    
    def is_london_open(self, hour, minute):
        """
        Check if time is in London Open window (02:00 to 05:00 EST)
        """
        time_minutes = self.get_time_in_minutes(hour, minute)
        # 02:00 (120 min) to 05:00 (300 min)
        return 120 <= time_minutes < 300
    
    def find_asian_low(self, date):
        """
        Find the Asian Low for a given trading date
        
        Asian session: 18:00 (previous day) to 02:00 (current day) EST
        
        Parameters:
        -----------
        date : datetime.date
            The trading date
            
        Returns:
        --------
        float or None : The Asian Low price, or None if not found
        """
        # Get previous date
        prev_date = date - timedelta(days=1)
        
        # Filter data for Asian session
        # Previous day 18:00 onwards
        prev_day_data = self.data[
            (self.data['Date'] == prev_date) & 
            (self.data['Hour'] >= 18)
        ]
        
        # Current day until 02:00
        curr_day_data = self.data[
            (self.data['Date'] == date) & 
            (self.data['Hour'] < 2)
        ]
        
        # Combine both
        asian_data = pd.concat([prev_day_data, curr_day_data])
        
        if len(asian_data) == 0:
            return None
        
        # Return the lowest Low during Asian session
        asian_low = asian_data['Low'].min()
        return asian_low
    
    def detect_bearish_fvg(self, df, start_idx, end_idx):
        """
        Detect Bearish Fair Value Gap (FVG)
        
        Bearish FVG: High[i] < Low[i-2]
        
        Parameters:
        -----------
        df : DataFrame
            The data
        start_idx : int
            Start index for search
        end_idx : int
            End index for search
            
        Returns:
        --------
        list : List of tuples (index, fvg_high, fvg_low) for each FVG found
        """
        fvgs = []
        
        for i in range(start_idx + 2, end_idx + 1):
            if i >= len(df):
                break
                
            # Bearish FVG: High[i] < Low[i-2]
            if df.loc[i, 'High'] < df.loc[i-2, 'Low']:
                fvg_high = df.loc[i-2, 'Low']
                fvg_low = df.loc[i, 'High']
                fvgs.append((i, fvg_high, fvg_low))
        
        return fvgs
    
    def run_backtest(self):
        """Execute the complete backtest strategy"""
        print("\nStarting backtest execution...")
        print("=" * 80)
        
        if self.data is None:
            raise ValueError("Data not loaded. Call load_data() first.")
        
        # Get unique trading dates
        unique_dates = sorted(self.data['Date'].unique())
        print(f"Processing {len(unique_dates)} trading days...")
        
        trade_id = 0
        
        for date_idx, current_date in enumerate(unique_dates):
            # Skip first few days to ensure we have Asian session data
            if date_idx < 3:
                continue
            
            # Find Asian Low for this date
            asian_low = self.find_asian_low(current_date)
            
            if asian_low is None:
                continue
            
            # Get London Open session data for this date
            london_data = self.data[
                (self.data['Date'] == current_date) & 
                (self.data['Hour'] >= 2) & 
                (self.data['Hour'] < 5)
            ].copy()
            
            if len(london_data) == 0:
                continue
            
            london_data = london_data.reset_index(drop=False)
            london_data.rename(columns={'index': 'original_idx'}, inplace=True)
            
            # Check for sweep below Asian Low
            sweep_occurred = False
            sweep_low = None
            sweep_start_idx = None
            sweep_end_idx = None
            
            for i in range(len(london_data)):
                if london_data.loc[i, 'Low'] < asian_low:
                    if not sweep_occurred:
                        sweep_occurred = True
                        sweep_start_idx = i
                        sweep_low = london_data.loc[i, 'Low']
                    else:
                        # Update sweep low if we go lower
                        if london_data.loc[i, 'Low'] < sweep_low:
                            sweep_low = london_data.loc[i, 'Low']
                    sweep_end_idx = i
            
            if not sweep_occurred:
                continue
            
            # Detect Bearish FVGs during the sweep
            fvgs = self.detect_bearish_fvg(london_data, sweep_start_idx, sweep_end_idx)
            
            if len(fvgs) == 0:
                continue
            
            # Check for inversion (price closes above FVG high)
            for fvg_idx, fvg_high, fvg_low in fvgs:
                inversion_confirmed = False
                inversion_candle_idx = None
                
                # Look for candles after FVG formation that close above FVG high
                for j in range(fvg_idx + 1, len(london_data)):
                    if london_data.loc[j, 'Close'] > fvg_high:
                        inversion_confirmed = True
                        inversion_candle_idx = j
                        break
                
                if not inversion_confirmed:
                    continue
                
                # Entry at next candle open
                entry_candle_idx = inversion_candle_idx + 1
                
                if entry_candle_idx >= len(london_data):
                    # Entry would be outside London session, skip
                    continue
                
                entry_price = london_data.loc[entry_candle_idx, 'Open']
                entry_time = london_data.loc[entry_candle_idx, 'EST_DateTime']
                
                # Stop Loss: 1 tick below swing low
                stop_loss = sweep_low - NQ_TICK_SIZE
                
                # Take Profit: 1:1 RR
                risk = entry_price - stop_loss
                take_profit = entry_price + risk
                
                # Simulate trade execution
                original_entry_idx = london_data.loc[entry_candle_idx, 'original_idx']
                
                # Look forward from entry to find exit
                exit_price = None
                exit_time = None
                exit_type = None
                
                # Search through data after entry
                for k in range(original_entry_idx, len(self.data)):
                    candle = self.data.loc[k]
                    
                    # Check if SL hit
                    if candle['Low'] <= stop_loss:
                        exit_price = stop_loss
                        exit_time = candle['EST_DateTime']
                        exit_type = 'SL'
                        break
                    
                    # Check if TP hit
                    if candle['High'] >= take_profit:
                        exit_price = take_profit
                        exit_time = candle['EST_DateTime']
                        exit_type = 'TP'
                        break
                    
                    # If we've gone too far (e.g., 2 days), close at market
                    if (candle['EST_DateTime'] - entry_time).days >= 2:
                        exit_price = candle['Close']
                        exit_time = candle['EST_DateTime']
                        exit_type = 'TIMEOUT'
                        break
                
                if exit_price is None:
                    # Trade still open (end of data)
                    exit_price = self.data.loc[len(self.data)-1, 'Close']
                    exit_time = self.data.loc[len(self.data)-1, 'EST_DateTime']
                    exit_type = 'EOD'
                
                # Calculate P&L
                pnl = exit_price - entry_price
                pnl_percent = (pnl / entry_price) * 100
                
                trade_id += 1
                
                # Record trade
                trade = {
                    'trade_id': trade_id,
                    'date': current_date,
                    'asian_low': asian_low,
                    'sweep_low': sweep_low,
                    'fvg_high': fvg_high,
                    'fvg_low': fvg_low,
                    'entry_time': entry_time,
                    'entry_price': entry_price,
                    'stop_loss': stop_loss,
                    'take_profit': take_profit,
                    'exit_time': exit_time,
                    'exit_price': exit_price,
                    'exit_type': exit_type,
                    'pnl': pnl,
                    'pnl_percent': pnl_percent,
                    'risk': risk,
                    'reward': risk,  # 1:1 RR
                    'winner': pnl > 0
                }
                
                self.trades.append(trade)
                
                # Only take first valid setup per day
                break
            
            # Progress indicator
            if (date_idx + 1) % 100 == 0:
                print(f"  Processed {date_idx + 1}/{len(unique_dates)} days, {len(self.trades)} trades found")
        
        print(f"\nBacktest complete! Total trades: {len(self.trades)}")
        return self.trades
    
    def calculate_statistics(self):
        """Calculate comprehensive trading statistics"""
        print("\nCalculating statistics...")
        
        if len(self.trades) == 0:
            print("No trades to analyze!")
            return None
        
        trades_df = pd.DataFrame(self.trades)
        
        # Basic metrics
        total_trades = len(trades_df)
        winning_trades = len(trades_df[trades_df['winner'] == True])
        losing_trades = len(trades_df[trades_df['winner'] == False])
        
        win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
        
        total_pnl = trades_df['pnl'].sum()
        avg_pnl = trades_df['pnl'].mean()
        
        avg_win = trades_df[trades_df['winner'] == True]['pnl'].mean() if winning_trades > 0 else 0
        avg_loss = trades_df[trades_df['winner'] == False]['pnl'].mean() if losing_trades > 0 else 0
        
        # Profit factor
        gross_profit = trades_df[trades_df['pnl'] > 0]['pnl'].sum()
        gross_loss = abs(trades_df[trades_df['pnl'] < 0]['pnl'].sum())
        profit_factor = (gross_profit / gross_loss) if gross_loss > 0 else 0
        
        # Expectancy
        expectancy = avg_pnl
        
        # Drawdown calculation
        trades_df['cumulative_pnl'] = trades_df['pnl'].cumsum()
        trades_df['running_max'] = trades_df['cumulative_pnl'].cummax()
        trades_df['drawdown'] = trades_df['cumulative_pnl'] - trades_df['running_max']
        max_drawdown = trades_df['drawdown'].min()
        
        # Monthly breakdown
        trades_df['year_month'] = pd.to_datetime(trades_df['entry_time']).dt.to_period('M')
        monthly_stats = trades_df.groupby('year_month').agg({
            'pnl': ['sum', 'count', 'mean'],
            'winner': lambda x: (x.sum() / len(x) * 100) if len(x) > 0 else 0
        }).round(2)
        
        # Yearly breakdown
        trades_df['year'] = pd.to_datetime(trades_df['entry_time']).dt.year
        yearly_stats = trades_df.groupby('year').agg({
            'pnl': ['sum', 'count', 'mean'],
            'winner': lambda x: (x.sum() / len(x) * 100) if len(x) > 0 else 0
        }).round(2)
        
        # Best and worst trades
        best_trade = trades_df.loc[trades_df['pnl'].idxmax()]
        worst_trade = trades_df.loc[trades_df['pnl'].idxmin()]
        
        # Consecutive wins/losses
        trades_df['streak'] = (trades_df['winner'] != trades_df['winner'].shift()).cumsum()
        win_streaks = trades_df[trades_df['winner'] == True].groupby('streak').size()
        loss_streaks = trades_df[trades_df['winner'] == False].groupby('streak').size()
        
        max_consecutive_wins = win_streaks.max() if len(win_streaks) > 0 else 0
        max_consecutive_losses = loss_streaks.max() if len(loss_streaks) > 0 else 0
        
        # Store statistics
        self.stats = {
            'total_trades': total_trades,
            'winning_trades': winning_trades,
            'losing_trades': losing_trades,
            'win_rate': win_rate,
            'total_pnl': total_pnl,
            'avg_pnl': avg_pnl,
            'avg_win': avg_win,
            'avg_loss': avg_loss,
            'gross_profit': gross_profit,
            'gross_loss': gross_loss,
            'profit_factor': profit_factor,
            'expectancy': expectancy,
            'max_drawdown': max_drawdown,
            'best_trade': best_trade['pnl'],
            'worst_trade': worst_trade['pnl'],
            'max_consecutive_wins': max_consecutive_wins,
            'max_consecutive_losses': max_consecutive_losses,
            'monthly_stats': monthly_stats,
            'yearly_stats': yearly_stats,
            'trades_df': trades_df
        }
        
        return self.stats
    
    def print_statistics(self):
        """Print comprehensive statistics to console"""
        if not self.stats:
            print("No statistics available. Run calculate_statistics() first.")
            return
        
        print("\n" + "=" * 80)
        print("LONDON MANIPULATION STRATEGY - BACKTEST RESULTS")
        print("=" * 80)
        
        print("\n📊 OVERALL PERFORMANCE")
        print("-" * 80)
        print(f"Total Trades:              {self.stats['total_trades']}")
        print(f"Winning Trades:            {self.stats['winning_trades']}")
        print(f"Losing Trades:             {self.stats['losing_trades']}")
        print(f"Win Rate:                  {self.stats['win_rate']:.2f}%")
        print(f"")
        print(f"Total P&L:                 {self.stats['total_pnl']:.2f} points")
        print(f"Average P&L per Trade:     {self.stats['avg_pnl']:.2f} points")
        print(f"Average Win:               {self.stats['avg_win']:.2f} points")
        print(f"Average Loss:              {self.stats['avg_loss']:.2f} points")
        print(f"")
        print(f"Gross Profit:              {self.stats['gross_profit']:.2f} points")
        print(f"Gross Loss:                {self.stats['gross_loss']:.2f} points")
        print(f"Profit Factor:             {self.stats['profit_factor']:.2f}")
        print(f"Expectancy per Trade:      {self.stats['expectancy']:.2f} points")
        print(f"")
        print(f"Maximum Drawdown:          {self.stats['max_drawdown']:.2f} points")
        print(f"Best Trade:                {self.stats['best_trade']:.2f} points")
        print(f"Worst Trade:               {self.stats['worst_trade']:.2f} points")
        print(f"")
        print(f"Max Consecutive Wins:      {self.stats['max_consecutive_wins']}")
        print(f"Max Consecutive Losses:    {self.stats['max_consecutive_losses']}")
        
        print("\n📅 YEARLY BREAKDOWN")
        print("-" * 80)
        yearly_df = self.stats['yearly_stats'].copy()
        yearly_df.columns = ['Total P&L', 'Trade Count', 'Avg P&L', 'Win Rate %']
        print(yearly_df.to_string())
        
        print("\n📈 MONTHLY BREAKDOWN (Last 24 months)")
        print("-" * 80)
        monthly_df = self.stats['monthly_stats'].tail(24).copy()
        monthly_df.columns = ['Total P&L', 'Trade Count', 'Avg P&L', 'Win Rate %']
        print(monthly_df.to_string())
        
        print("\n" + "=" * 80)
    
    def export_trades_to_csv(self, filename='london_manipulation_trades.csv'):
        """Export all trades to CSV file"""
        if len(self.trades) == 0:
            print("No trades to export!")
            return
        
        trades_df = pd.DataFrame(self.trades)
        filepath = os.path.join(self.data_directory, filename)
        trades_df.to_csv(filepath, index=False)
        print(f"\n✅ Trades exported to: {filepath}")
        
        return filepath
    
    def generate_markdown_report(self, filename='london_manipulation_report.md'):
        """Generate a comprehensive markdown report"""
        if not self.stats:
            print("No statistics available. Run calculate_statistics() first.")
            return
        
        filepath = os.path.join(self.data_directory, filename)
        
        with open(filepath, 'w') as f:
            f.write("# London Manipulation Strategy - Backtest Report\n\n")
            f.write("## Strategy Overview\n\n")
            f.write("**Instrument:** NQ (Nasdaq 100 Futures)\n\n")
            f.write("**Timeframe:** 5-minute chart\n\n")
            f.write("**Period:** January 2018 - Present\n\n")
            f.write("**Strategy Logic:**\n")
            f.write("1. Identify Asian Session Low (18:00-02:00 EST)\n")
            f.write("2. Detect liquidity sweep below Asian Low during London Open (02:00-05:00 EST)\n")
            f.write("3. Identify Bearish Fair Value Gap (FVG) during sweep\n")
            f.write("4. Confirm inversion when price closes above FVG high\n")
            f.write("5. Enter LONG at next candle open\n")
            f.write("6. Stop Loss: 1 tick (0.25 points) below swing low\n")
            f.write("7. Take Profit: 1:1 Risk/Reward ratio\n\n")
            
            f.write("---\n\n")
            f.write("## Overall Performance\n\n")
            f.write(f"| Metric | Value |\n")
            f.write(f"|--------|-------|\n")
            f.write(f"| Total Trades | {self.stats['total_trades']} |\n")
            f.write(f"| Winning Trades | {self.stats['winning_trades']} |\n")
            f.write(f"| Losing Trades | {self.stats['losing_trades']} |\n")
            f.write(f"| Win Rate | {self.stats['win_rate']:.2f}% |\n")
            f.write(f"| Total P&L | {self.stats['total_pnl']:.2f} points |\n")
            f.write(f"| Average P&L per Trade | {self.stats['avg_pnl']:.2f} points |\n")
            f.write(f"| Average Win | {self.stats['avg_win']:.2f} points |\n")
            f.write(f"| Average Loss | {self.stats['avg_loss']:.2f} points |\n")
            f.write(f"| Profit Factor | {self.stats['profit_factor']:.2f} |\n")
            f.write(f"| Expectancy per Trade | {self.stats['expectancy']:.2f} points |\n")
            f.write(f"| Maximum Drawdown | {self.stats['max_drawdown']:.2f} points |\n")
            f.write(f"| Best Trade | {self.stats['best_trade']:.2f} points |\n")
            f.write(f"| Worst Trade | {self.stats['worst_trade']:.2f} points |\n")
            f.write(f"| Max Consecutive Wins | {self.stats['max_consecutive_wins']} |\n")
            f.write(f"| Max Consecutive Losses | {self.stats['max_consecutive_losses']} |\n\n")
            
            f.write("---\n\n")
            f.write("## Yearly Performance\n\n")
            yearly_df = self.stats['yearly_stats'].copy()
            yearly_df.columns = ['Total P&L', 'Trade Count', 'Avg P&L', 'Win Rate %']
            f.write(yearly_df.to_markdown())
            f.write("\n\n")
            
            f.write("---\n\n")
            f.write("## Monthly Performance\n\n")
            monthly_df = self.stats['monthly_stats'].copy()
            monthly_df.columns = ['Total P&L', 'Trade Count', 'Avg P&L', 'Win Rate %']
            f.write(monthly_df.to_markdown())
            f.write("\n\n")
            
            f.write("---\n\n")
            f.write("## Strategy Notes\n\n")
            f.write("- All times are in EST (New York time zone)\n")
            f.write("- Asian session spans from 18:00 (previous day) to 02:00\n")
            f.write("- London Open window is 02:00 to 05:00\n")
            f.write("- Bearish FVG detected when High[i] < Low[i-2]\n")
            f.write("- Inversion confirmed when candle closes ABOVE FVG high\n")
            f.write("- NQ tick size: 0.25 points\n")
            f.write("- Risk/Reward: 1:1 (fixed)\n")
            f.write("- No breakeven adjustment during trade\n\n")
            
            f.write("---\n\n")
            f.write(f"*Report generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")
        
        print(f"✅ Markdown report generated: {filepath}")
        return filepath


def main():
    """Main execution function"""
    print("=" * 80)
    print("LONDON MANIPULATION STRATEGY BACKTEST")
    print("=" * 80)
    print("\nNQ (Nasdaq 100 Futures) - 5 Minute Timeframe")
    print("Period: January 2018 - Present")
    print()
    
    # Initialize backtest
    backtest = LondonManipulationBacktest(data_directory="/home/runner/work/Backtest-Trading/Backtest-Trading")
    
    # Load data
    backtest.load_data()
    
    # Run backtest
    backtest.run_backtest()
    
    # Calculate statistics
    backtest.calculate_statistics()
    
    # Print results
    backtest.print_statistics()
    
    # Export results
    backtest.export_trades_to_csv()
    backtest.generate_markdown_report()
    
    print("\n" + "=" * 80)
    print("✅ BACKTEST COMPLETE!")
    print("=" * 80)
    print("\nGenerated files:")
    print("  - london_manipulation_trades.csv (detailed trade log)")
    print("  - london_manipulation_report.md (summary report)")
    print()


if __name__ == "__main__":
    main()

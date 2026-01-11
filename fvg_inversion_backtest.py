#!/usr/bin/env python3
"""
NQ Futures - First FVG Inversion Strategy Backtest
===================================================
Author: Senior Quantitative Trader
Strategy: First FVG Inversion on 3-minute timeframe
Data: 1-minute raw data resampled to 3-minute bars
Timeframe: 2018-2024
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import zipfile
import os
from datetime import datetime, time
import warnings
warnings.filterwarnings('ignore')

class FVGInversionBacktest:
    """
    Backtest engine for First FVG Inversion strategy on NQ Futures
    """
    
    def __init__(self, data_dir='/home/runner/work/Backtest-Trading/Backtest-Trading'):
        """
        Initialize the backtest engine
        
        Parameters:
        -----------
        data_dir : str
            Path to the directory containing the data files
        """
        self.data_dir = data_dir
        self.df_1m = None
        self.df_3m = None
        self.trades = []
        
        # Session definitions (Chicago Time)
        self.london_start = time(1, 0)
        self.london_end = time(4, 0)
        self.ny_start = time(8, 30)
        self.ny_end = time(11, 0)
        
    def load_and_combine_data(self):
        """
        Load all 1-minute data files from 2018-2024 and combine them
        """
        print("=" * 70)
        print("STEP 1: LOADING 1-MINUTE DATA")
        print("=" * 70)
        
        all_data = []
        years = [2018, 2019, 2020, 2021, 2022, 2023, 2024]
        
        for year in years:
            zip_file = os.path.join(self.data_dir, f'{year} 1m.csv.zip')
            
            if os.path.exists(zip_file):
                print(f"Loading {year} data from zip file...")
                try:
                    with zipfile.ZipFile(zip_file, 'r') as z:
                        # Get the name of the CSV file inside the zip
                        csv_filename = z.namelist()[0]
                        with z.open(csv_filename) as f:
                            df = pd.read_csv(f, sep=';', header=0)
                            all_data.append(df)
                            print(f"  ✓ Loaded {len(df):,} rows from {year}")
                except Exception as e:
                    print(f"  ✗ Error loading {year}: {e}")
            else:
                print(f"  ✗ File not found: {zip_file}")
        
        if not all_data:
            raise ValueError("No data files were loaded successfully!")
        
        # Combine all data
        print("\nCombining all data...")
        self.df_1m = pd.concat(all_data, ignore_index=True)
        print(f"✓ Total rows loaded: {len(self.df_1m):,}")
        
        # Clean and prepare the data
        self._prepare_dataframe()
        
    def _prepare_dataframe(self):
        """
        Clean and prepare the 1-minute dataframe
        """
        print("\nPreparing data...")
        
        # Rename columns
        self.df_1m.columns = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
        
        # Combine Date and Time into a single datetime column
        self.df_1m['Datetime'] = pd.to_datetime(
            self.df_1m['Date'] + ' ' + self.df_1m['Time'],
            format='%d/%m/%Y %H:%M:%S'
        )
        
        # Set Datetime as index
        self.df_1m.set_index('Datetime', inplace=True)
        
        # Convert price columns to numeric
        for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
            self.df_1m[col] = pd.to_numeric(self.df_1m[col], errors='coerce')
        
        # Remove any rows with NaN values
        initial_len = len(self.df_1m)
        self.df_1m.dropna(inplace=True)
        if initial_len > len(self.df_1m):
            print(f"  Removed {initial_len - len(self.df_1m)} rows with missing data")
        
        # Sort by datetime
        self.df_1m.sort_index(inplace=True)
        
        print(f"✓ Data prepared: {len(self.df_1m):,} rows")
        print(f"  Date range: {self.df_1m.index[0]} to {self.df_1m.index[-1]}")
        
    def resample_to_3min(self):
        """
        Resample 1-minute data to 3-minute bars
        """
        print("\n" + "=" * 70)
        print("STEP 2: RESAMPLING TO 3-MINUTE TIMEFRAME")
        print("=" * 70)
        
        # Resample to 3-minute bars
        self.df_3m = self.df_1m.resample('3T').agg({
            'Open': 'first',
            'High': 'max',
            'Low': 'min',
            'Close': 'last',
            'Volume': 'sum'
        })
        
        # Remove any rows with NaN (incomplete bars)
        self.df_3m.dropna(inplace=True)
        
        print(f"✓ Resampled to 3-minute bars: {len(self.df_3m):,} rows")
        print(f"  Date range: {self.df_3m.index[0]} to {self.df_3m.index[-1]}")
        
        # Add time components for session filtering
        self.df_3m['Time'] = self.df_3m.index.time
        self.df_3m['Date'] = self.df_3m.index.date
        
    def identify_fvgs(self):
        """
        Identify Fair Value Gaps (FVGs) in the 3-minute data
        
        Bearish FVG: Low[i-2] > High[i]
        Bullish FVG: High[i-2] < Low[i]
        """
        print("\n" + "=" * 70)
        print("STEP 3: IDENTIFYING FAIR VALUE GAPS")
        print("=" * 70)
        
        # Initialize columns for FVG tracking
        self.df_3m['Bearish_FVG'] = False
        self.df_3m['Bullish_FVG'] = False
        self.df_3m['FVG_Top'] = np.nan
        self.df_3m['FVG_Bottom'] = np.nan
        
        # Need at least 3 candles to identify FVG
        for i in range(2, len(self.df_3m)):
            # Bearish FVG: Low[i-2] > High[i]
            if self.df_3m.iloc[i-2]['Low'] > self.df_3m.iloc[i]['High']:
                self.df_3m.iloc[i, self.df_3m.columns.get_loc('Bearish_FVG')] = True
                self.df_3m.iloc[i, self.df_3m.columns.get_loc('FVG_Top')] = self.df_3m.iloc[i-2]['Low']
                self.df_3m.iloc[i, self.df_3m.columns.get_loc('FVG_Bottom')] = self.df_3m.iloc[i]['High']
            
            # Bullish FVG: High[i-2] < Low[i]
            elif self.df_3m.iloc[i-2]['High'] < self.df_3m.iloc[i]['Low']:
                self.df_3m.iloc[i, self.df_3m.columns.get_loc('Bullish_FVG')] = True
                self.df_3m.iloc[i, self.df_3m.columns.get_loc('FVG_Top')] = self.df_3m.iloc[i]['Low']
                self.df_3m.iloc[i, self.df_3m.columns.get_loc('FVG_Bottom')] = self.df_3m.iloc[i-2]['High']
        
        bearish_count = self.df_3m['Bearish_FVG'].sum()
        bullish_count = self.df_3m['Bullish_FVG'].sum()
        
        print(f"✓ Bearish FVGs identified: {bearish_count:,}")
        print(f"✓ Bullish FVGs identified: {bullish_count:,}")
        print(f"✓ Total FVGs: {bearish_count + bullish_count:,}")
        
    def is_in_session(self, time_val, session):
        """
        Check if a time is within a trading session
        
        Parameters:
        -----------
        time_val : datetime.time
            Time to check
        session : str
            'london' or 'ny'
        """
        if session == 'london':
            return self.london_start <= time_val < self.london_end
        elif session == 'ny':
            return self.ny_start <= time_val < self.ny_end
        return False
    
    def execute_backtest(self):
        """
        Execute the FVG Inversion backtest with "One Bullet" rule
        """
        print("\n" + "=" * 70)
        print("STEP 4: EXECUTING BACKTEST")
        print("=" * 70)
        
        # Track active FVGs and session states
        active_bearish_fvgs = []  # List of tuples: (creation_idx, top, bottom)
        active_bullish_fvgs = []  # List of tuples: (creation_idx, top, bottom)
        
        london_traded_today = False
        ny_traded_today = False
        current_date = None
        
        for i in range(len(self.df_3m)):
            row = self.df_3m.iloc[i]
            current_time = row['Time']
            current_date_val = row['Date']
            
            # Reset daily flags at the start of a new day
            if current_date != current_date_val:
                current_date = current_date_val
                london_traded_today = False
                ny_traded_today = False
            
            # Determine current session
            in_london = self.is_in_session(current_time, 'london')
            in_ny = self.is_in_session(current_time, 'ny')
            
            # Reset NY flag when entering NY session
            if in_ny and not self.is_in_session(self.df_3m.iloc[i-1]['Time'] if i > 0 else time(0, 0), 'ny'):
                ny_traded_today = False
            
            # Add new FVGs to the active list
            if row['Bearish_FVG']:
                active_bearish_fvgs.append((i, row['FVG_Top'], row['FVG_Bottom']))
            
            if row['Bullish_FVG']:
                active_bullish_fvgs.append((i, row['FVG_Top'], row['FVG_Bottom']))
            
            # Check for LONG signals (Bearish FVG Inversion)
            if not in_london and not in_ny:
                continue  # Only trade during killzones
            
            session_name = 'London' if in_london else 'New York'
            
            # Check if we can trade in this session
            if (in_london and london_traded_today) or (in_ny and ny_traded_today):
                continue
            
            # LONG SIGNAL: Close above Bearish FVG top
            for fvg_idx, fvg_top, fvg_bottom in active_bearish_fvgs[:]:
                if row['Close'] > fvg_top:
                    # Valid LONG signal
                    entry_price = row['Close']
                    stop_loss = row['Low']
                    risk = entry_price - stop_loss
                    take_profit = entry_price + risk  # 1:1 RR
                    
                    # Find exit
                    exit_info = self._find_exit(i, entry_price, stop_loss, take_profit, 'LONG')
                    
                    # Record trade
                    trade = {
                        'Entry_Time': self.df_3m.index[i],
                        'Entry_Price': entry_price,
                        'Direction': 'LONG',
                        'Stop_Loss': stop_loss,
                        'Take_Profit': take_profit,
                        'Risk': risk,
                        'Session': session_name,
                        'FVG_Type': 'Bearish',
                        'Exit_Time': exit_info['exit_time'],
                        'Exit_Price': exit_info['exit_price'],
                        'Exit_Reason': exit_info['exit_reason'],
                        'PnL': exit_info['pnl'],
                        'PnL_Points': exit_info['pnl_points'],
                        'Win': exit_info['win']
                    }
                    
                    self.trades.append(trade)
                    
                    # Set session flag
                    if in_london:
                        london_traded_today = True
                    else:
                        ny_traded_today = True
                    
                    # Remove this FVG from active list
                    active_bearish_fvgs.remove((fvg_idx, fvg_top, fvg_bottom))
                    break  # Only take first signal
            
            # SHORT SIGNAL: Close below Bullish FVG bottom
            if (in_london and not london_traded_today) or (in_ny and not ny_traded_today):
                for fvg_idx, fvg_top, fvg_bottom in active_bullish_fvgs[:]:
                    if row['Close'] < fvg_bottom:
                        # Valid SHORT signal
                        entry_price = row['Close']
                        stop_loss = row['High']
                        risk = stop_loss - entry_price
                        take_profit = entry_price - risk  # 1:1 RR
                        
                        # Find exit
                        exit_info = self._find_exit(i, entry_price, stop_loss, take_profit, 'SHORT')
                        
                        # Record trade
                        trade = {
                            'Entry_Time': self.df_3m.index[i],
                            'Entry_Price': entry_price,
                            'Direction': 'SHORT',
                            'Stop_Loss': stop_loss,
                            'Take_Profit': take_profit,
                            'Risk': risk,
                            'Session': session_name,
                            'FVG_Type': 'Bullish',
                            'Exit_Time': exit_info['exit_time'],
                            'Exit_Price': exit_info['exit_price'],
                            'Exit_Reason': exit_info['exit_reason'],
                            'PnL': exit_info['pnl'],
                            'PnL_Points': exit_info['pnl_points'],
                            'Win': exit_info['win']
                        }
                        
                        self.trades.append(trade)
                        
                        # Set session flag
                        if in_london:
                            london_traded_today = True
                        else:
                            ny_traded_today = True
                        
                        # Remove this FVG from active list
                        active_bullish_fvgs.remove((fvg_idx, fvg_top, fvg_bottom))
                        break  # Only take first signal
            
            # Clean up old FVGs (optional: keep only recent ones to improve performance)
            # For simplicity, we'll keep all FVGs active
        
        print(f"✓ Backtest complete: {len(self.trades)} trades executed")
        
    def _find_exit(self, entry_idx, entry_price, stop_loss, take_profit, direction):
        """
        Find the exit point for a trade
        
        Returns:
        --------
        dict with exit_time, exit_price, exit_reason, pnl, pnl_points, win
        """
        # Look forward from entry to find exit
        for j in range(entry_idx + 1, len(self.df_3m)):
            bar = self.df_3m.iloc[j]
            
            if direction == 'LONG':
                # Check if stop loss hit
                if bar['Low'] <= stop_loss:
                    return {
                        'exit_time': self.df_3m.index[j],
                        'exit_price': stop_loss,
                        'exit_reason': 'Stop Loss',
                        'pnl': stop_loss - entry_price,
                        'pnl_points': stop_loss - entry_price,
                        'win': False
                    }
                # Check if take profit hit
                elif bar['High'] >= take_profit:
                    return {
                        'exit_time': self.df_3m.index[j],
                        'exit_price': take_profit,
                        'exit_reason': 'Take Profit',
                        'pnl': take_profit - entry_price,
                        'pnl_points': take_profit - entry_price,
                        'win': True
                    }
            
            else:  # SHORT
                # Check if stop loss hit
                if bar['High'] >= stop_loss:
                    return {
                        'exit_time': self.df_3m.index[j],
                        'exit_price': stop_loss,
                        'exit_reason': 'Stop Loss',
                        'pnl': entry_price - stop_loss,
                        'pnl_points': entry_price - stop_loss,
                        'win': False
                    }
                # Check if take profit hit
                elif bar['Low'] <= take_profit:
                    return {
                        'exit_time': self.df_3m.index[j],
                        'exit_price': take_profit,
                        'exit_reason': 'Take Profit',
                        'pnl': entry_price - take_profit,
                        'pnl_points': entry_price - take_profit,
                        'win': True
                    }
        
        # If we reach here, trade never exited (end of data)
        # Close at last available price
        last_bar = self.df_3m.iloc[-1]
        exit_price = last_bar['Close']
        
        if direction == 'LONG':
            pnl = exit_price - entry_price
        else:
            pnl = entry_price - exit_price
        
        return {
            'exit_time': self.df_3m.index[-1],
            'exit_price': exit_price,
            'exit_reason': 'End of Data',
            'pnl': pnl,
            'pnl_points': pnl,
            'win': pnl > 0
        }
    
    def generate_report(self):
        """
        Generate comprehensive trading report
        """
        print("\n" + "=" * 70)
        print("STEP 5: GENERATING PERFORMANCE REPORT")
        print("=" * 70)
        
        if not self.trades:
            print("No trades to report!")
            return
        
        # Convert trades to DataFrame
        trades_df = pd.DataFrame(self.trades)
        
        # Overall statistics
        print("\n" + "=" * 70)
        print("OVERALL PERFORMANCE")
        print("=" * 70)
        self._print_statistics(trades_df, "ALL SESSIONS")
        
        # London statistics
        print("\n" + "=" * 70)
        print("LONDON SESSION PERFORMANCE (01:00 - 04:00 CT)")
        print("=" * 70)
        london_trades = trades_df[trades_df['Session'] == 'London']
        if len(london_trades) > 0:
            self._print_statistics(london_trades, "LONDON")
        else:
            print("No trades in London session")
        
        # New York statistics
        print("\n" + "=" * 70)
        print("NEW YORK SESSION PERFORMANCE (08:30 - 11:00 CT)")
        print("=" * 70)
        ny_trades = trades_df[trades_df['Session'] == 'New York']
        if len(ny_trades) > 0:
            self._print_statistics(ny_trades, "NEW YORK")
        else:
            print("No trades in New York session")
        
        # Save detailed trade log
        trades_df.to_csv(
            os.path.join(self.data_dir, 'trade_log.csv'),
            index=False
        )
        print(f"\n✓ Detailed trade log saved to: trade_log.csv")
        
        # Generate markdown report
        self._generate_markdown_report(trades_df)
        
        return trades_df
    
    def _print_statistics(self, trades_df, label):
        """
        Print statistics for a set of trades
        """
        total_trades = len(trades_df)
        winning_trades = trades_df['Win'].sum()
        losing_trades = total_trades - winning_trades
        
        win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
        
        total_pnl = trades_df['PnL_Points'].sum()
        
        winning_pnl = trades_df[trades_df['Win'] == True]['PnL_Points'].sum()
        losing_pnl = abs(trades_df[trades_df['Win'] == False]['PnL_Points'].sum())
        
        profit_factor = (winning_pnl / losing_pnl) if losing_pnl > 0 else float('inf')
        
        avg_win = trades_df[trades_df['Win'] == True]['PnL_Points'].mean() if winning_trades > 0 else 0
        avg_loss = trades_df[trades_df['Win'] == False]['PnL_Points'].mean() if losing_trades > 0 else 0
        
        print(f"\n{label}:")
        print(f"  Total Trades:        {total_trades:>6}")
        print(f"  Winning Trades:      {winning_trades:>6}")
        print(f"  Losing Trades:       {losing_trades:>6}")
        print(f"  Win Rate:            {win_rate:>6.2f}%")
        print(f"  Profit Factor:       {profit_factor:>6.2f}")
        print(f"  Net Profit (Points): {total_pnl:>6.2f}")
        print(f"  Average Win:         {avg_win:>6.2f}")
        print(f"  Average Loss:        {avg_loss:>6.2f}")
        
        # Additional metrics
        if total_trades > 0:
            max_win = trades_df['PnL_Points'].max()
            max_loss = trades_df['PnL_Points'].min()
            print(f"  Largest Win:         {max_win:>6.2f}")
            print(f"  Largest Loss:        {max_loss:>6.2f}")
    
    def _generate_markdown_report(self, trades_df):
        """
        Generate a markdown file with backtest results
        """
        md_path = os.path.join(self.data_dir, 'backtest_results.md')
        
        with open(md_path, 'w') as f:
            # Header
            f.write("# NQ Futures - First FVG Inversion Strategy Backtest Results\n\n")
            f.write("## Strategy Overview\n\n")
            f.write("- **Strategy:** First FVG Inversion (One Bullet Rule)\n")
            f.write("- **Timeframe:** 3-Minute (resampled from 1-Minute data)\n")
            f.write("- **Period:** 2018-2024\n")
            f.write("- **Sessions:** London (01:00-04:00 CT) & New York (08:30-11:00 CT)\n")
            f.write("- **Risk Management:** 1:1 Risk-to-Reward Ratio\n\n")
            
            f.write("---\n\n")
            
            # Overall Performance
            f.write("## Overall Performance\n\n")
            self._write_statistics_to_md(f, trades_df, "All Sessions")
            
            # London Performance
            f.write("\n---\n\n")
            f.write("## London Session Performance (01:00 - 04:00 CT)\n\n")
            london_trades = trades_df[trades_df['Session'] == 'London']
            if len(london_trades) > 0:
                self._write_statistics_to_md(f, london_trades, "London")
            else:
                f.write("*No trades executed in London session*\n\n")
            
            # New York Performance
            f.write("\n---\n\n")
            f.write("## New York Session Performance (08:30 - 11:00 CT)\n\n")
            ny_trades = trades_df[trades_df['Session'] == 'New York']
            if len(ny_trades) > 0:
                self._write_statistics_to_md(f, ny_trades, "New York")
            else:
                f.write("*No trades executed in New York session*\n\n")
            
            # Trade Distribution
            f.write("\n---\n\n")
            f.write("## Trade Distribution\n\n")
            f.write("| Session | Total Trades | Winning | Losing | Win Rate |\n")
            f.write("|---------|--------------|---------|--------|----------|\n")
            
            for session in ['London', 'New York']:
                session_trades = trades_df[trades_df['Session'] == session]
                if len(session_trades) > 0:
                    total = len(session_trades)
                    wins = session_trades['Win'].sum()
                    losses = total - wins
                    win_rate = (wins / total * 100) if total > 0 else 0
                    f.write(f"| {session} | {total} | {wins} | {losses} | {win_rate:.2f}% |\n")
            
            # Add direction distribution
            f.write("\n### Direction Distribution\n\n")
            f.write("| Direction | Total Trades | Winning | Losing | Win Rate |\n")
            f.write("|-----------|--------------|---------|--------|----------|\n")
            
            for direction in ['LONG', 'SHORT']:
                dir_trades = trades_df[trades_df['Direction'] == direction]
                if len(dir_trades) > 0:
                    total = len(dir_trades)
                    wins = dir_trades['Win'].sum()
                    losses = total - wins
                    win_rate = (wins / total * 100) if total > 0 else 0
                    f.write(f"| {direction} | {total} | {wins} | {losses} | {win_rate:.2f}% |\n")
            
            # Equity Curve Reference
            f.write("\n---\n\n")
            f.write("## Equity Curve\n\n")
            f.write("![Equity Curve](equity_curve.png)\n\n")
            f.write("*The equity curve visualization shows the cumulative profit/loss over time for both trading sessions.*\n\n")
            
            # Footer
            f.write("\n---\n\n")
            f.write("## Additional Information\n\n")
            f.write("- **Detailed Trade Log:** See `trade_log.csv` for complete trade details\n")
            f.write(f"- **Total Trades Executed:** {len(trades_df)}\n")
            f.write(f"- **Report Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        print(f"\n✓ Markdown report saved to: backtest_results.md")
    
    def _write_statistics_to_md(self, f, trades_df, label):
        """
        Write statistics to markdown file
        """
        total_trades = len(trades_df)
        winning_trades = trades_df['Win'].sum()
        losing_trades = total_trades - winning_trades
        
        win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
        
        total_pnl = trades_df['PnL_Points'].sum()
        
        winning_pnl = trades_df[trades_df['Win'] == True]['PnL_Points'].sum()
        losing_pnl = abs(trades_df[trades_df['Win'] == False]['PnL_Points'].sum())
        
        profit_factor = (winning_pnl / losing_pnl) if losing_pnl > 0 else float('inf')
        
        avg_win = trades_df[trades_df['Win'] == True]['PnL_Points'].mean() if winning_trades > 0 else 0
        avg_loss = trades_df[trades_df['Win'] == False]['PnL_Points'].mean() if losing_trades > 0 else 0
        
        # Write as table
        f.write("| Metric | Value |\n")
        f.write("|--------|-------|\n")
        f.write(f"| **Total Trades** | {total_trades} |\n")
        f.write(f"| **Winning Trades** | {winning_trades} |\n")
        f.write(f"| **Losing Trades** | {losing_trades} |\n")
        f.write(f"| **Win Rate** | {win_rate:.2f}% |\n")
        f.write(f"| **Profit Factor** | {profit_factor:.2f} |\n")
        f.write(f"| **Net Profit (Points)** | {total_pnl:.2f} |\n")
        f.write(f"| **Average Win** | {avg_win:.2f} |\n")
        f.write(f"| **Average Loss** | {avg_loss:.2f} |\n")
        
        if total_trades > 0:
            max_win = trades_df['PnL_Points'].max()
            max_loss = trades_df['PnL_Points'].min()
            f.write(f"| **Largest Win** | {max_win:.2f} |\n")
            f.write(f"| **Largest Loss** | {max_loss:.2f} |\n")
        
        f.write("\n")
    
    def plot_equity_curve(self, trades_df):
        """
        Plot the cumulative equity curve
        """
        print("\n" + "=" * 70)
        print("STEP 6: GENERATING EQUITY CURVE")
        print("=" * 70)
        
        if trades_df is None or len(trades_df) == 0:
            print("No trades to plot!")
            return
        
        # Calculate cumulative PnL
        trades_df = trades_df.sort_values('Entry_Time')
        trades_df['Cumulative_PnL'] = trades_df['PnL_Points'].cumsum()
        
        # Create figure with subplots
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
        
        # Plot 1: Overall equity curve
        ax1.plot(trades_df['Entry_Time'], trades_df['Cumulative_PnL'], 
                linewidth=2, color='#2E86AB', label='Cumulative PnL')
        ax1.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
        ax1.set_title('NQ Futures - First FVG Inversion Strategy\nCumulative Equity Curve (2018-2024)', 
                     fontsize=14, fontweight='bold')
        ax1.set_xlabel('Date', fontsize=11)
        ax1.set_ylabel('Cumulative Profit/Loss (Points)', fontsize=11)
        ax1.grid(True, alpha=0.3)
        ax1.legend(fontsize=10)
        
        # Plot 2: Equity curve by session
        london_trades = trades_df[trades_df['Session'] == 'London'].copy()
        ny_trades = trades_df[trades_df['Session'] == 'New York'].copy()
        
        if len(london_trades) > 0:
            london_trades['Cumulative_PnL_London'] = london_trades['PnL_Points'].cumsum()
            ax2.plot(london_trades['Entry_Time'], london_trades['Cumulative_PnL_London'], 
                    linewidth=2, color='#A23B72', label='London Session', marker='o', markersize=3)
        
        if len(ny_trades) > 0:
            ny_trades['Cumulative_PnL_NY'] = ny_trades['PnL_Points'].cumsum()
            ax2.plot(ny_trades['Entry_Time'], ny_trades['Cumulative_PnL_NY'], 
                    linewidth=2, color='#F18F01', label='New York Session', marker='s', markersize=3)
        
        ax2.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
        ax2.set_title('Cumulative Equity by Trading Session', fontsize=12, fontweight='bold')
        ax2.set_xlabel('Date', fontsize=11)
        ax2.set_ylabel('Cumulative Profit/Loss (Points)', fontsize=11)
        ax2.grid(True, alpha=0.3)
        ax2.legend(fontsize=10)
        
        plt.tight_layout()
        
        # Save the plot
        output_path = os.path.join(self.data_dir, 'equity_curve.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"✓ Equity curve saved to: equity_curve.png")
        
        plt.close()
    
    def run(self):
        """
        Run the complete backtest pipeline
        """
        print("\n" + "=" * 70)
        print("NQ FUTURES - FIRST FVG INVERSION BACKTEST")
        print("=" * 70)
        print("Strategy: First FVG Inversion (One Bullet Rule)")
        print("Timeframe: 3-Minute (from 1-Minute data)")
        print("Period: 2018-2024")
        print("Sessions: London (01:00-04:00 CT) & New York (08:30-11:00 CT)")
        print("=" * 70)
        
        # Step 1: Load data
        self.load_and_combine_data()
        
        # Step 2: Resample to 3-minute
        self.resample_to_3min()
        
        # Step 3: Identify FVGs
        self.identify_fvgs()
        
        # Step 4: Execute backtest
        self.execute_backtest()
        
        # Step 5: Generate report
        trades_df = self.generate_report()
        
        # Step 6: Plot equity curve
        if trades_df is not None and len(trades_df) > 0:
            self.plot_equity_curve(trades_df)
        
        print("\n" + "=" * 70)
        print("BACKTEST COMPLETED SUCCESSFULLY!")
        print("=" * 70)


def main():
    """
    Main execution function
    """
    try:
        # Initialize backtest
        backtest = FVGInversionBacktest()
        
        # Run the complete backtest
        backtest.run()
        
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())

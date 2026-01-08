"""
NQ Futures FVG (Fair Value Gap) Backtest Strategy

This script implements a complete backtest for NQ futures trading based on FVG detection.
Time zone: Chicago Exchange Time (no conversion needed)
Killzone: 08:30 to 11:00
Data: 1-minute timeframe from 2018-2025

Author: Automated Backtest System
Date: 2026-01-08
"""

import pandas as pd
import numpy as np
from datetime import datetime, time, timedelta
import zipfile
import os
import warnings
warnings.filterwarnings('ignore')


class NQFVGBacktest:
    """
    FVG (Fair Value Gap) Backtest Strategy for NQ Futures
    """
    
    def __init__(self, data_directory):
        """
        Initialize the backtest system
        
        Args:
            data_directory: Path to the directory containing CSV files
        """
        self.data_directory = data_directory
        self.killzone_start = time(8, 30)  # 08:30
        self.killzone_end = time(11, 0)    # 11:00
        self.sl_offset = 0.5  # Stop loss offset in points
        self.tp_multiplier = 1.5  # Take profit multiplier
        self.trades = []
        self.all_data = None
        
    def unzip_data_files(self):
        """
        Unzip all compressed CSV files in the data directory
        """
        print("Unzipping compressed data files...")
        zip_files = [
            "2018 1m.csv.zip",
            "2019 1m.csv.zip",
            "2020 1m.csv.zip",
            "2021 1m.csv.zip",
            "2022 1m.csv.zip",
            "2023 1m.csv.zip",
            "2024 1m.csv.zip"
        ]
        
        for zip_file in zip_files:
            zip_path = os.path.join(self.data_directory, zip_file)
            if os.path.exists(zip_path):
                csv_name = zip_file.replace('.zip', '')
                csv_path = os.path.join(self.data_directory, csv_name)
                
                # Skip if CSV already exists
                if os.path.exists(csv_path):
                    print(f"  {csv_name} already exists, skipping...")
                    continue
                
                try:
                    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                        zip_ref.extractall(self.data_directory)
                    print(f"  Extracted: {csv_name}")
                except Exception as e:
                    print(f"  Error extracting {zip_file}: {str(e)}")
            else:
                print(f"  {zip_file} not found, skipping...")
    
    def load_data(self):
        """
        Load and combine all 1-minute CSV data files
        
        Returns:
            pd.DataFrame: Combined dataframe with all data
        """
        print("\nLoading data files...")
        
        # List of CSV files to load
        csv_files = [
            "2018 1m.csv",
            "2019 1m.csv",
            "2020 1m.csv",
            "2021 1m.csv",
            "2022 1m.csv",
            "2023 1m.csv",
            "2024 1m.csv",
            "2025 1m.csv"
        ]
        
        dataframes = []
        
        for csv_file in csv_files:
            csv_path = os.path.join(self.data_directory, csv_file)
            
            if not os.path.exists(csv_path):
                print(f"  Warning: {csv_file} not found, skipping...")
                continue
            
            try:
                # Read CSV with semicolon separator
                df = pd.read_csv(
                    csv_path,
                    sep=';',
                    parse_dates=False  # We'll parse dates manually
                )
                
                # Rename columns for easier access
                df.columns = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
                
                # Combine Date and Time into DateTime
                df['DateTime'] = pd.to_datetime(
                    df['Date'] + ' ' + df['Time'],
                    format='%d/%m/%Y %H:%M:%S'
                )
                
                # Extract date and time separately for filtering
                df['DateOnly'] = df['DateTime'].dt.date
                df['TimeOnly'] = df['DateTime'].dt.time
                
                # Convert OHLC to float
                df['Open'] = df['Open'].astype(float)
                df['High'] = df['High'].astype(float)
                df['Low'] = df['Low'].astype(float)
                df['Close'] = df['Close'].astype(float)
                df['Volume'] = df['Volume'].astype(float)
                
                dataframes.append(df)
                print(f"  Loaded: {csv_file} ({len(df)} rows)")
                
            except Exception as e:
                print(f"  Error loading {csv_file}: {str(e)}")
        
        if not dataframes:
            raise ValueError("No data files could be loaded!")
        
        # Combine all dataframes
        combined_df = pd.concat(dataframes, ignore_index=True)
        combined_df = combined_df.sort_values('DateTime').reset_index(drop=True)
        
        print(f"\nTotal data loaded: {len(combined_df)} rows")
        print(f"Date range: {combined_df['DateTime'].min()} to {combined_df['DateTime'].max()}")
        
        self.all_data = combined_df
        return combined_df
    
    def detect_fvg(self, i, df):
        """
        Detect Fair Value Gap at candle index i
        
        Args:
            i: Current candle index (just closed)
            df: DataFrame with OHLC data
        
        Returns:
            tuple: (fvg_type, entry_price, stop_loss, take_profit)
                   fvg_type: 'bullish', 'bearish', or None
        """
        # Need at least 3 candles (i-2, i-1, i)
        if i < 2:
            return None, None, None, None
        
        # Get candle data
        candle_i_minus_2 = df.iloc[i - 2]
        candle_i_minus_1 = df.iloc[i - 1]
        candle_i = df.iloc[i]
        
        # Bearish FVG: Low[i-2] > High[i]
        if candle_i_minus_2['Low'] > candle_i['High']:
            entry_price = candle_i['High']
            stop_loss = candle_i_minus_2['High'] + self.sl_offset
            risk = stop_loss - entry_price
            take_profit = entry_price - (risk * self.tp_multiplier)
            return 'bearish', entry_price, stop_loss, take_profit
        
        # Bullish FVG: High[i-2] < Low[i]
        if candle_i_minus_2['High'] < candle_i['Low']:
            entry_price = candle_i['Low']
            stop_loss = candle_i_minus_2['Low'] - self.sl_offset
            risk = entry_price - stop_loss
            take_profit = entry_price + (risk * self.tp_multiplier)
            return 'bullish', entry_price, stop_loss, take_profit
        
        return None, None, None, None
    
    def check_order_trigger(self, entry_price, fvg_type, candle):
        """
        Check if order gets triggered by the candle
        
        Args:
            entry_price: Limit order entry price
            fvg_type: 'bullish' or 'bearish'
            candle: Current candle data
        
        Returns:
            bool: True if order triggered, False otherwise
        """
        if fvg_type == 'bullish':
            # Long order triggers if price touches entry (Low <= entry)
            return candle['Low'] <= entry_price
        elif fvg_type == 'bearish':
            # Short order triggers if price touches entry (High >= entry)
            return candle['High'] >= entry_price
        return False
    
    def simulate_trade(self, entry_candle_idx, entry_price, stop_loss, take_profit, fvg_type, df):
        """
        Simulate a trade from entry to exit
        
        Args:
            entry_candle_idx: Index where order was placed (candle i)
            entry_price: Entry price
            stop_loss: Stop loss price
            take_profit: Take profit price
            fvg_type: 'bullish' or 'bearish'
            df: DataFrame with OHLC data
        
        Returns:
            dict: Trade result or None if not triggered
        """
        entry_date = df.iloc[entry_candle_idx]['DateOnly']
        entry_datetime = df.iloc[entry_candle_idx]['DateTime']
        
        # Look for order trigger in subsequent candles
        triggered = False
        trigger_candle_idx = None
        
        # Check candles after order placement (i+1, i+2, ...)
        for j in range(entry_candle_idx + 1, len(df)):
            candle = df.iloc[j]
            candle_date = candle['DateOnly']
            candle_time = candle['TimeOnly']
            
            # Stop checking if we're past killzone end time or different day
            if candle_date != entry_date or candle_time >= self.killzone_end:
                break
            
            # Check if order triggers
            if self.check_order_trigger(entry_price, fvg_type, candle):
                triggered = True
                trigger_candle_idx = j
                break
        
        # If order not triggered by killzone end, return None
        if not triggered:
            return None
        
        # Order triggered - simulate trade execution
        entry_time = df.iloc[trigger_candle_idx]['DateTime']
        
        # Now check for TP or SL hit
        exit_price = None
        exit_time = None
        exit_reason = None
        
        for k in range(trigger_candle_idx, len(df)):
            candle = df.iloc[k]
            candle_date = candle['DateOnly']
            
            # Continue checking even after killzone if trade is active
            # Only stop at end of day
            if candle_date != entry_date:
                break
            
            if fvg_type == 'bullish':
                # Long trade: Check for TP or SL
                if candle['High'] >= take_profit:
                    exit_price = take_profit
                    exit_time = candle['DateTime']
                    exit_reason = 'TP'
                    break
                elif candle['Low'] <= stop_loss:
                    exit_price = stop_loss
                    exit_time = candle['DateTime']
                    exit_reason = 'SL'
                    break
            
            elif fvg_type == 'bearish':
                # Short trade: Check for TP or SL
                if candle['Low'] <= take_profit:
                    exit_price = take_profit
                    exit_time = candle['DateTime']
                    exit_reason = 'TP'
                    break
                elif candle['High'] >= stop_loss:
                    exit_price = stop_loss
                    exit_time = candle['DateTime']
                    exit_reason = 'SL'
                    break
        
        # If no exit by end of day, close at last candle's close
        if exit_price is None:
            last_candle = df[df['DateOnly'] == entry_date].iloc[-1]
            exit_price = last_candle['Close']
            exit_time = last_candle['DateTime']
            exit_reason = 'EOD'
        
        # Calculate PnL
        if fvg_type == 'bullish':
            pnl = exit_price - entry_price
        else:  # bearish
            pnl = entry_price - exit_price
        
        # Calculate duration
        duration = (exit_time - entry_time).total_seconds() / 60  # in minutes
        
        return {
            'Date': entry_date,
            'Entry_Time': entry_time,
            'Exit_Time': exit_time,
            'Type': 'Long' if fvg_type == 'bullish' else 'Short',
            'Entry_Price': entry_price,
            'Exit_Price': exit_price,
            'Stop_Loss': stop_loss,
            'Take_Profit': take_profit,
            'PnL': pnl,
            'Exit_Reason': exit_reason,
            'Duration_Minutes': duration
        }
    
    def run_backtest(self):
        """
        Run the complete backtest
        
        Returns:
            pd.DataFrame: DataFrame with all trades
        """
        print("\n" + "="*70)
        print("RUNNING BACKTEST")
        print("="*70)
        
        if self.all_data is None:
            raise ValueError("Data not loaded. Call load_data() first.")
        
        df = self.all_data
        trades_per_day = {}  # Track if we already have a trade for each day
        
        # Iterate through each candle
        for i in range(2, len(df)):
            candle = df.iloc[i]
            candle_date = candle['DateOnly']
            candle_time = candle['TimeOnly']
            
            # Skip if outside killzone
            if candle_time < self.killzone_start or candle_time >= self.killzone_end:
                continue
            
            # Skip if already traded today (one trade per day maximum)
            if candle_date in trades_per_day:
                continue
            
            # Detect FVG
            fvg_type, entry_price, stop_loss, take_profit = self.detect_fvg(i, df)
            
            if fvg_type is not None:
                # FVG detected - mark this day as having an FVG (even if not triggered)
                trades_per_day[candle_date] = True
                
                # Simulate trade
                trade_result = self.simulate_trade(
                    i, entry_price, stop_loss, take_profit, fvg_type, df
                )
                
                if trade_result is not None:
                    self.trades.append(trade_result)
                    
                    # Print progress every 50 trades
                    if len(self.trades) % 50 == 0:
                        print(f"  Processed {len(self.trades)} trades...")
        
        print(f"\nBacktest completed: {len(self.trades)} trades executed")
        
        if not self.trades:
            print("No trades were executed!")
            return pd.DataFrame()
        
        # Convert to DataFrame
        trades_df = pd.DataFrame(self.trades)
        return trades_df
    
    def calculate_metrics(self, trades_df):
        """
        Calculate backtest performance metrics
        
        Args:
            trades_df: DataFrame with trade results
        
        Returns:
            dict: Dictionary with performance metrics
        """
        if len(trades_df) == 0:
            return {
                'Total_Trades': 0,
                'Winning_Trades': 0,
                'Losing_Trades': 0,
                'Win_Rate': 0.0,
                'Total_PnL': 0.0,
                'Avg_Win': 0.0,
                'Avg_Loss': 0.0,
                'Profit_Factor': 0.0,
                'Max_Drawdown': 0.0,
                'Max_Drawdown_Pct': 0.0
            }
        
        # Basic statistics
        total_trades = len(trades_df)
        winning_trades = len(trades_df[trades_df['PnL'] > 0])
        losing_trades = len(trades_df[trades_df['PnL'] < 0])
        win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
        
        # PnL statistics
        total_pnl = trades_df['PnL'].sum()
        wins = trades_df[trades_df['PnL'] > 0]['PnL']
        losses = trades_df[trades_df['PnL'] < 0]['PnL']
        
        avg_win = wins.mean() if len(wins) > 0 else 0
        avg_loss = losses.mean() if len(losses) > 0 else 0
        
        gross_profit = wins.sum() if len(wins) > 0 else 0
        gross_loss = abs(losses.sum()) if len(losses) > 0 else 0
        profit_factor = (gross_profit / gross_loss) if gross_loss > 0 else float('inf')
        
        # Drawdown calculation
        trades_df = trades_df.copy()
        trades_df['Cumulative_PnL'] = trades_df['PnL'].cumsum()
        trades_df['Peak'] = trades_df['Cumulative_PnL'].cummax()
        trades_df['Drawdown'] = trades_df['Peak'] - trades_df['Cumulative_PnL']
        
        max_drawdown = trades_df['Drawdown'].max()
        
        # Max drawdown percentage (relative to peak)
        peak_at_max_dd = trades_df.loc[trades_df['Drawdown'].idxmax(), 'Peak']
        max_drawdown_pct = (max_drawdown / peak_at_max_dd * 100) if peak_at_max_dd > 0 else 0
        
        return {
            'Total_Trades': total_trades,
            'Winning_Trades': winning_trades,
            'Losing_Trades': losing_trades,
            'Win_Rate': win_rate,
            'Total_PnL': total_pnl,
            'Gross_Profit': gross_profit,
            'Gross_Loss': gross_loss,
            'Avg_Win': avg_win,
            'Avg_Loss': avg_loss,
            'Profit_Factor': profit_factor,
            'Max_Drawdown': max_drawdown,
            'Max_Drawdown_Pct': max_drawdown_pct,
            'Avg_Duration_Minutes': trades_df['Duration_Minutes'].mean()
        }
    
    def print_summary(self, metrics):
        """
        Print backtest summary statistics
        
        Args:
            metrics: Dictionary with performance metrics
        """
        print("\n" + "="*70)
        print("BACKTEST SUMMARY")
        print("="*70)
        print(f"\nTrading Period: {self.all_data['DateTime'].min().date()} to {self.all_data['DateTime'].max().date()}")
        print(f"Killzone: {self.killzone_start.strftime('%H:%M')} to {self.killzone_end.strftime('%H:%M')}")
        print(f"\n{'PERFORMANCE METRICS':-^70}")
        print(f"\nTotal Trades:          {metrics['Total_Trades']}")
        print(f"Winning Trades:        {metrics['Winning_Trades']}")
        print(f"Losing Trades:         {metrics['Losing_Trades']}")
        print(f"Win Rate:              {metrics['Win_Rate']:.2f}%")
        print(f"\nTotal Net P&L:         {metrics['Total_PnL']:.2f} points")
        print(f"Gross Profit:          {metrics['Gross_Profit']:.2f} points")
        print(f"Gross Loss:            {metrics['Gross_Loss']:.2f} points")
        print(f"Average Win:           {metrics['Avg_Win']:.2f} points")
        print(f"Average Loss:          {metrics['Avg_Loss']:.2f} points")
        print(f"Profit Factor:         {metrics['Profit_Factor']:.2f}")
        print(f"\nMax Drawdown:          {metrics['Max_Drawdown']:.2f} points")
        print(f"Max Drawdown %:        {metrics['Max_Drawdown_Pct']:.2f}%")
        print(f"\nAvg Trade Duration:    {metrics['Avg_Duration_Minutes']:.1f} minutes")
        print("\n" + "="*70)
    
    def save_results(self, trades_df, output_file='nq_fvg_backtest_results.csv'):
        """
        Save backtest results to CSV
        
        Args:
            trades_df: DataFrame with trade results
            output_file: Output CSV filename
        """
        output_path = os.path.join(self.data_directory, output_file)
        
        # Prepare output DataFrame
        output_df = trades_df[[
            'Date', 'Entry_Time', 'Exit_Time', 'Type',
            'Entry_Price', 'Exit_Price', 'Stop_Loss', 'Take_Profit',
            'PnL', 'Exit_Reason', 'Duration_Minutes'
        ]].copy()
        
        output_df.to_csv(output_path, index=False)
        print(f"\nResults saved to: {output_path}")


def main():
    """
    Main execution function
    """
    # Set data directory
    data_directory = '/home/runner/work/Backtest-Trading/Backtest-Trading/'
    
    print("="*70)
    print("NQ FUTURES FVG BACKTEST STRATEGY")
    print("="*70)
    print("\nStrategy Parameters:")
    print("  - Killzone: 08:30 to 11:00 (Chicago Time)")
    print("  - FVG Detection: 3-candle pattern (i-2, i-1, i)")
    print("  - Stop Loss Offset: 0.5 points")
    print("  - Take Profit: 1.5x Risk")
    print("  - Max Trades per Day: 1")
    print("="*70)
    
    try:
        # Initialize backtest
        backtest = NQFVGBacktest(data_directory)
        
        # Unzip data files
        backtest.unzip_data_files()
        
        # Load data
        backtest.load_data()
        
        # Run backtest
        trades_df = backtest.run_backtest()
        
        if len(trades_df) > 0:
            # Calculate metrics
            metrics = backtest.calculate_metrics(trades_df)
            
            # Print summary
            backtest.print_summary(metrics)
            
            # Save results
            backtest.save_results(trades_df)
            
            print("\nFirst 10 trades:")
            print(trades_df.head(10).to_string())
            
            print("\nLast 10 trades:")
            print(trades_df.tail(10).to_string())
        else:
            print("\nNo trades were executed during the backtest period.")
    
    except Exception as e:
        print(f"\nError during backtest: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

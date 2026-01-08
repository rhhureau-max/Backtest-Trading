#!/usr/bin/env python3
"""
Fair Value Gap (FVG) Trading Strategy Backtest
Author: AI Trading System
Description: Complete backtest implementation for FVG strategy on NQ 1-minute data
"""

import pandas as pd
import numpy as np
from datetime import datetime, time
import glob
import zipfile
import os
from typing import List, Dict, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')


class FVGBacktest:
    """
    Fair Value Gap (FVG) Trading Strategy Backtest Engine
    
    This class implements a complete backtesting system for FVG-based trading
    on 1-minute Nasdaq futures data.
    """
    
    def __init__(self, data_dir: str = '.'):
        """
        Initialize the backtest engine.
        
        Args:
            data_dir: Directory containing the CSV files
        """
        self.data_dir = data_dir
        self.trades = []
        self.daily_trades = {}  # Track trades per day
        
        # Trading parameters
        self.killzone_start = time(8, 30)  # 08:30
        self.killzone_end = time(11, 0)    # 11:00
        self.sl_offset = 0.5  # Stop loss offset in points
        self.risk_reward = 1.5  # Risk-reward ratio for take profit
        
    def load_data(self) -> pd.DataFrame:
        """
        Load all 1-minute CSV files from 2018 to 2025.
        Handles both .csv and .csv.zip formats.
        
        Returns:
            Combined DataFrame with all data
        """
        print("Loading data files...")
        all_data = []
        
        # Look for 1m files (both .csv and .csv.zip)
        csv_files = sorted(glob.glob(os.path.join(self.data_dir, '*1m.csv')))
        zip_files = sorted(glob.glob(os.path.join(self.data_dir, '*1m.csv.zip')))
        
        # Load CSV files
        for file_path in csv_files:
            year = file_path.split('/')[-1].split()[0]
            print(f"  Loading {year} from CSV...")
            try:
                df = pd.read_csv(file_path, sep=';', header=0)
                all_data.append(df)
            except Exception as e:
                print(f"  Warning: Could not load {file_path}: {e}")
        
        # Load ZIP files
        for zip_path in zip_files:
            year = zip_path.split('/')[-1].split()[0]
            print(f"  Loading {year} from ZIP...")
            try:
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    # Get the first CSV file in the zip
                    csv_name = [name for name in zip_ref.namelist() if name.endswith('.csv')][0]
                    with zip_ref.open(csv_name) as csv_file:
                        df = pd.read_csv(csv_file, sep=';', header=0)
                        all_data.append(df)
            except Exception as e:
                print(f"  Warning: Could not load {zip_path}: {e}")
        
        if not all_data:
            raise ValueError("No data files found!")
        
        # Combine all data
        print("Combining data...")
        combined_df = pd.concat(all_data, ignore_index=True)
        
        # Process the data
        print("Processing timestamps...")
        combined_df = self._process_timestamps(combined_df)
        
        # Sort by datetime
        combined_df = combined_df.sort_values('datetime').reset_index(drop=True)
        
        print(f"Loaded {len(combined_df):,} rows from {combined_df['datetime'].min()} to {combined_df['datetime'].max()}")
        
        return combined_df
    
    def _process_timestamps(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Process timestamps and convert to Chicago timezone.
        
        Args:
            df: Raw DataFrame with Column1 (Date) and Column2 (Time)
        
        Returns:
            DataFrame with processed datetime column
        """
        # Rename columns for easier access
        df.columns = ['date', 'time', 'open', 'high', 'low', 'close', 'volume']
        
        # Combine date and time
        df['datetime'] = pd.to_datetime(
            df['date'] + ' ' + df['time'],
            format='%d/%m/%Y %H:%M:%S'
        )
        
        # Convert to Chicago timezone (America/Chicago)
        # Assuming the data is already in Chicago time based on requirements
        df['datetime'] = df['datetime'].dt.tz_localize('America/Chicago', ambiguous='infer', nonexistent='shift_forward')
        
        # Extract date and time components
        df['date_only'] = df['datetime'].dt.date
        df['time_only'] = df['datetime'].dt.time
        
        return df
    
    def identify_fvg(self, df: pd.DataFrame, idx: int) -> Optional[Dict]:
        """
        Identify Fair Value Gap at given index.
        
        Args:
            df: DataFrame with OHLC data
            idx: Current candle index (i)
        
        Returns:
            Dictionary with FVG details or None if no FVG found
        """
        # Need at least 3 candles
        if idx < 2:
            return None
        
        i = idx
        i_minus_1 = idx - 1
        i_minus_2 = idx - 2
        
        # Get candle data
        low_i = df.loc[i, 'low']
        high_i = df.loc[i, 'high']
        low_i_minus_2 = df.loc[i_minus_2, 'low']
        high_i_minus_2 = df.loc[i_minus_2, 'high']
        
        # Check for Bearish FVG (Short setup)
        # Condition: Low[i-2] > High[i]
        if low_i_minus_2 > high_i:
            gap = low_i_minus_2 - high_i
            entry_price = high_i + (gap * 0.5)  # 50% entry
            stop_loss = high_i_minus_2 + self.sl_offset
            risk = stop_loss - entry_price
            take_profit = entry_price - (risk * self.risk_reward)
            
            return {
                'type': 'SHORT',
                'entry_price': entry_price,
                'stop_loss': stop_loss,
                'take_profit': take_profit,
                'gap_high': low_i_minus_2,
                'gap_low': high_i,
                'signal_time': df.loc[i, 'datetime'],
                'signal_index': i
            }
        
        # Check for Bullish FVG (Long setup)
        # Condition: High[i-2] < Low[i]
        elif high_i_minus_2 < low_i:
            gap = low_i - high_i_minus_2
            entry_price = high_i_minus_2 + (gap * 0.5)  # 50% entry
            stop_loss = low_i_minus_2 - self.sl_offset
            risk = entry_price - stop_loss
            take_profit = entry_price + (risk * self.risk_reward)
            
            return {
                'type': 'LONG',
                'entry_price': entry_price,
                'stop_loss': stop_loss,
                'take_profit': take_profit,
                'gap_high': low_i,
                'gap_low': high_i_minus_2,
                'signal_time': df.loc[i, 'datetime'],
                'signal_index': i
            }
        
        return None
    
    def execute_trade(self, df: pd.DataFrame, setup: Dict, start_idx: int) -> Optional[Dict]:
        """
        Execute trade based on FVG setup.
        Check tick-by-tick if limit order gets filled and then if SL/TP is hit.
        
        Args:
            df: DataFrame with OHLC data
            setup: FVG setup dictionary
            start_idx: Index to start checking from
        
        Returns:
            Trade result dictionary or None if order not filled
        """
        entry_price = setup['entry_price']
        stop_loss = setup['stop_loss']
        take_profit = setup['take_profit']
        trade_type = setup['type']
        
        # Get the date for this trade
        trade_date = df.loc[start_idx, 'date_only']
        
        # Look forward from signal to find if entry is touched
        max_idx = len(df) - 1
        
        # Find the end of killzone (11:00) for this day
        killzone_end_idx = start_idx
        for idx in range(start_idx, max_idx + 1):
            current_time = df.loc[idx, 'time_only']
            current_date = df.loc[idx, 'date_only']
            
            # If we move to next day, stop
            if current_date != trade_date:
                break
            
            # If we reach 11:00, mark it and break
            if current_time >= self.killzone_end:
                killzone_end_idx = idx
                break
            
            killzone_end_idx = idx
        
        # Check each candle for entry fill
        for idx in range(start_idx + 1, killzone_end_idx + 1):
            candle_low = df.loc[idx, 'low']
            candle_high = df.loc[idx, 'high']
            
            # Check if limit order is filled (price touches entry level)
            entry_filled = False
            
            if trade_type == 'LONG':
                # For long, entry is at lower price, so high must reach entry
                if candle_high >= entry_price >= candle_low:
                    entry_filled = True
            else:  # SHORT
                # For short, entry is at higher price, so low must reach entry
                if candle_high >= entry_price >= candle_low:
                    entry_filled = True
            
            if entry_filled:
                # Entry filled! Now check for SL/TP from this candle onwards
                entry_time = df.loc[idx, 'datetime']
                entry_idx = idx
                
                # Check subsequent candles for SL or TP
                for exit_idx in range(entry_idx, killzone_end_idx + 1):
                    candle_low = df.loc[exit_idx, 'low']
                    candle_high = df.loc[exit_idx, 'high']
                    
                    if trade_type == 'LONG':
                        # Check if SL hit first (low touches or breaks SL)
                        if candle_low <= stop_loss:
                            return {
                                'type': trade_type,
                                'entry_price': entry_price,
                                'exit_price': stop_loss,
                                'stop_loss': stop_loss,
                                'take_profit': take_profit,
                                'entry_time': entry_time,
                                'exit_time': df.loc[exit_idx, 'datetime'],
                                'result': 'LOSS',
                                'pnl': stop_loss - entry_price,
                                'signal_time': setup['signal_time']
                            }
                        # Check if TP hit first (high touches or exceeds TP)
                        elif candle_high >= take_profit:
                            return {
                                'type': trade_type,
                                'entry_price': entry_price,
                                'exit_price': take_profit,
                                'stop_loss': stop_loss,
                                'take_profit': take_profit,
                                'entry_time': entry_time,
                                'exit_time': df.loc[exit_idx, 'datetime'],
                                'result': 'WIN',
                                'pnl': take_profit - entry_price,
                                'signal_time': setup['signal_time']
                            }
                    
                    else:  # SHORT
                        # Check if SL hit first (high touches or exceeds SL)
                        if candle_high >= stop_loss:
                            return {
                                'type': trade_type,
                                'entry_price': entry_price,
                                'exit_price': stop_loss,
                                'stop_loss': stop_loss,
                                'take_profit': take_profit,
                                'entry_time': entry_time,
                                'exit_time': df.loc[exit_idx, 'datetime'],
                                'result': 'LOSS',
                                'pnl': entry_price - stop_loss,
                                'signal_time': setup['signal_time']
                            }
                        # Check if TP hit first (low touches or goes below TP)
                        elif candle_low <= take_profit:
                            return {
                                'type': trade_type,
                                'entry_price': entry_price,
                                'exit_price': take_profit,
                                'stop_loss': stop_loss,
                                'take_profit': take_profit,
                                'entry_time': entry_time,
                                'exit_time': df.loc[exit_idx, 'datetime'],
                                'result': 'WIN',
                                'pnl': entry_price - take_profit,
                                'signal_time': setup['signal_time']
                            }
                
                # If we reach here, neither SL nor TP was hit before killzone ended
                # Close at market (we'll skip this scenario as per typical limit order behavior)
                return None
        
        # Limit order not filled before killzone ended
        return None
    
    def run_backtest(self) -> List[Dict]:
        """
        Run the complete backtest.
        
        Returns:
            List of all trades executed
        """
        print("\n" + "="*80)
        print("STARTING FVG BACKTEST")
        print("="*80)
        
        # Load data
        df = self.load_data()
        
        print("\n" + "="*80)
        print("SCANNING FOR FVG SIGNALS")
        print("="*80)
        
        # Filter data to killzone only for scanning
        df_killzone = df[
            (df['time_only'] >= self.killzone_start) &
            (df['time_only'] <= self.killzone_end)
        ].copy()
        
        print(f"Total candles in killzone: {len(df_killzone):,}")
        
        # Reset index for easier iteration
        df_killzone = df_killzone.reset_index(drop=True)
        
        # Track processed days
        processed_days = set()
        
        # Iterate through killzone candles
        for idx in range(len(df_killzone)):
            current_date = df_killzone.loc[idx, 'date_only']
            current_time = df_killzone.loc[idx, 'time_only']
            
            # Skip if we already have a trade for this day
            if current_date in processed_days:
                continue
            
            # Only start scanning from 08:30 close (i.e., from 08:31 onwards)
            if current_time < time(8, 31):
                continue
            
            # Look for FVG
            fvg_setup = self.identify_fvg(df_killzone, idx)
            
            if fvg_setup:
                # Found a valid FVG setup!
                # Now try to execute the trade
                original_idx = df_killzone.loc[idx, 'datetime']
                
                # Find the index in the full dataframe
                full_df_idx = df[df['datetime'] == original_idx].index[0]
                
                # Execute trade
                trade_result = self.execute_trade(df, fvg_setup, full_df_idx)
                
                if trade_result:
                    # Trade was executed
                    self.trades.append(trade_result)
                    processed_days.add(current_date)
                    
                    if len(self.trades) % 100 == 0:
                        print(f"  Processed {len(processed_days)} days, {len(self.trades)} trades executed...")
        
        print(f"\nBacktest complete!")
        print(f"Total days scanned: {len(processed_days)}")
        print(f"Total trades executed: {len(self.trades)}")
        
        return self.trades
    
    def calculate_metrics(self) -> Dict:
        """
        Calculate performance metrics for the backtest.
        
        Returns:
            Dictionary with all performance metrics
        """
        if not self.trades:
            return {
                'total_trades': 0,
                'winning_trades': 0,
                'losing_trades': 0,
                'win_rate': 0.0,
                'total_pnl': 0.0,
                'avg_win': 0.0,
                'avg_loss': 0.0,
                'profit_factor': 0.0,
                'max_drawdown': 0.0,
                'sharpe_ratio': 0.0
            }
        
        # Convert trades to DataFrame for easier analysis
        trades_df = pd.DataFrame(self.trades)
        
        # Basic metrics
        total_trades = len(trades_df)
        winning_trades = len(trades_df[trades_df['result'] == 'WIN'])
        losing_trades = len(trades_df[trades_df['result'] == 'LOSS'])
        win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0.0
        
        # PnL metrics
        total_pnl = trades_df['pnl'].sum()
        wins = trades_df[trades_df['result'] == 'WIN']['pnl']
        losses = trades_df[trades_df['result'] == 'LOSS']['pnl']
        
        avg_win = wins.mean() if len(wins) > 0 else 0.0
        avg_loss = losses.mean() if len(losses) > 0 else 0.0
        
        # Profit factor
        gross_profit = wins.sum() if len(wins) > 0 else 0.0
        gross_loss = abs(losses.sum()) if len(losses) > 0 else 0.0
        profit_factor = (gross_profit / gross_loss) if gross_loss > 0 else float('inf')
        
        # Maximum drawdown
        trades_df['cumulative_pnl'] = trades_df['pnl'].cumsum()
        trades_df['cumulative_max'] = trades_df['cumulative_pnl'].cummax()
        trades_df['drawdown'] = trades_df['cumulative_max'] - trades_df['cumulative_pnl']
        max_drawdown = trades_df['drawdown'].max()
        
        # Sharpe ratio (assuming 252 trading days per year)
        if len(trades_df) > 1:
            returns = trades_df['pnl']
            sharpe_ratio = (returns.mean() / returns.std()) * np.sqrt(252) if returns.std() > 0 else 0.0
        else:
            sharpe_ratio = 0.0
        
        return {
            'total_trades': total_trades,
            'winning_trades': winning_trades,
            'losing_trades': losing_trades,
            'win_rate': win_rate,
            'total_pnl': total_pnl,
            'avg_win': avg_win,
            'avg_loss': avg_loss,
            'profit_factor': profit_factor,
            'max_drawdown': max_drawdown,
            'sharpe_ratio': sharpe_ratio,
            'gross_profit': gross_profit,
            'gross_loss': gross_loss
        }
    
    def save_results(self, output_file: str = 'fvg_backtest_results.csv'):
        """
        Save trade log to CSV file.
        
        Args:
            output_file: Output CSV filename
        """
        if not self.trades:
            print("No trades to save!")
            return
        
        trades_df = pd.DataFrame(self.trades)
        
        # Format datetime columns
        trades_df['signal_time'] = pd.to_datetime(trades_df['signal_time']).dt.strftime('%Y-%m-%d %H:%M:%S')
        trades_df['entry_time'] = pd.to_datetime(trades_df['entry_time']).dt.strftime('%Y-%m-%d %H:%M:%S')
        trades_df['exit_time'] = pd.to_datetime(trades_df['exit_time']).dt.strftime('%Y-%m-%d %H:%M:%S')
        
        # Save to CSV
        trades_df.to_csv(output_file, index=False)
        print(f"\nTrade log saved to: {output_file}")
    
    def print_summary(self):
        """
        Print summary statistics to console.
        """
        metrics = self.calculate_metrics()
        
        print("\n" + "="*80)
        print("BACKTEST RESULTS SUMMARY")
        print("="*80)
        print(f"\nTotal Trades:           {metrics['total_trades']}")
        print(f"Winning Trades:         {metrics['winning_trades']}")
        print(f"Losing Trades:          {metrics['losing_trades']}")
        print(f"Win Rate:               {metrics['win_rate']:.2f}%")
        print(f"\nTotal PnL:              {metrics['total_pnl']:.2f} points")
        print(f"Gross Profit:           {metrics['gross_profit']:.2f} points")
        print(f"Gross Loss:             {metrics['gross_loss']:.2f} points")
        print(f"\nAverage Win:            {metrics['avg_win']:.2f} points")
        print(f"Average Loss:           {metrics['avg_loss']:.2f} points")
        print(f"\nProfit Factor:          {metrics['profit_factor']:.2f}")
        print(f"Maximum Drawdown:       {metrics['max_drawdown']:.2f} points")
        print(f"Sharpe Ratio:           {metrics['sharpe_ratio']:.2f}")
        print("="*80)


def main():
    """
    Main execution function.
    """
    print("""
    ╔════════════════════════════════════════════════════════════════════════╗
    ║                                                                        ║
    ║           FAIR VALUE GAP (FVG) BACKTEST - NQ 1-MINUTE DATA           ║
    ║                                                                        ║
    ║  Strategy: FVG 50% Entry with 1.5 Risk-Reward                        ║
    ║  Timeframe: 1-minute                                                  ║
    ║  Killzone: 08:30 - 11:00 Chicago Time                                ║
    ║  Data: 2018 - 2025                                                    ║
    ║                                                                        ║
    ╚════════════════════════════════════════════════════════════════════════╝
    """)
    
    # Initialize backtest
    backtest = FVGBacktest(data_dir='/home/runner/work/Backtest-Trading/Backtest-Trading')
    
    # Run backtest
    trades = backtest.run_backtest()
    
    # Calculate and print results
    backtest.print_summary()
    
    # Save results
    backtest.save_results('fvg_backtest_results.csv')
    
    print("\n✓ Backtest completed successfully!")
    print("\nFiles generated:")
    print("  - fvg_backtest_results.csv (detailed trade log)")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Advanced Fair Value Gap (FVG) Backtesting Script
Author: Trading Analysis System
Date: 2025

This script implements an advanced FVG (Fair Value Gap) strategy with 4 configurable modes:
1. Standard (Proximal Entry)
2. Consequent Encroachment (50% Retracement)
3. Significant Gap (Volatility Filter)
4. Freshness Filter (Temporal Validity)

All operations are vectorized using pandas/numpy for optimal performance.
"""

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')


class FVGAdvancedBacktest:
    """
    Advanced FVG backtesting engine with 4 configurable modes.
    """
    
    def __init__(self, csv_file_path, fvg_mode=1, stop_loss=25, take_profit=50):
        """
        Initialize the FVG advanced backtesting engine.
        
        Parameters:
        -----------
        csv_file_path : str
            Path to the CSV file with trading data
        fvg_mode : int
            FVG mode to use (1-4):
            1 = Standard (Proximal Entry)
            2 = Consequent Encroachment (50% Retracement)
            3 = Significant Gap (Volatility Filter)
            4 = Freshness Filter (Temporal Validity)
        stop_loss : float
            Stop loss in points (default: 25)
        take_profit : float
            Take profit in points (default: 50)
        """
        self.csv_file_path = csv_file_path
        self.fvg_mode = fvg_mode
        self.stop_loss = stop_loss
        self.take_profit = take_profit
        self.df = None
        self.results = {}
        
        # Validate mode
        if self.fvg_mode not in [1, 2, 3, 4]:
            raise ValueError("fvg_mode must be 1, 2, 3, or 4")
        
    def load_data(self):
        """
        Load and prepare the data from CSV file.
        """
        print(f"Loading data from: {self.csv_file_path}")
        
        # Load CSV with semicolon separator, skip header row
        self.df = pd.read_csv(
            self.csv_file_path,
            sep=';',
            names=['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume'],
            skiprows=1  # Skip the header row
        )
        
        # Convert Date and Time to appropriate formats
        self.df['Date'] = pd.to_datetime(self.df['Date'], format='%d/%m/%Y')
        
        # Create a datetime column for easier filtering (no timezone conversion)
        self.df['DateTime'] = pd.to_datetime(
            self.df['Date'].astype(str) + ' ' + self.df['Time'],
            format='%Y-%m-%d %H:%M:%S'
        )
        
        # Convert price columns to numeric
        for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
            self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
        
        # Sort by datetime
        self.df = self.df.sort_values('DateTime').reset_index(drop=True)
        
        print(f"Loaded {len(self.df)} rows of data")
        print(f"Date range: {self.df['Date'].min()} to {self.df['Date'].max()}")
        
    def filter_session(self):
        """
        Filter data to keep only the session between 01:00:00 and 05:00:00 (inclusive).
        """
        print("\nFiltering data for session 01:00:00 to 05:00:00...")
        
        # Extract time as string for comparison
        time_str = self.df['Time'].astype(str)
        
        # Filter between 01:00:00 and 05:00:00 (inclusive)
        mask = (time_str >= '01:00:00') & (time_str <= '05:00:00')
        self.df = self.df[mask].reset_index(drop=True)
        
        print(f"Filtered to {len(self.df)} rows within session time")
        
    def detect_fvg(self):
        """
        Detect Fair Value Gaps (FVG) using vectorized operations.
        
        FVG Definition:
        - Bullish FVG: Created when High[i-2] < Low[i]. Zone = [High[i-2], Low[i]]
        - Bearish FVG: Created when Low[i-2] > High[i]. Zone = [High[i], Low[i-2]]
        """
        print(f"\nDetecting Fair Value Gaps (FVG) with Mode {self.fvg_mode}...")
        
        # Calculate ATR(14) for mode 3
        if self.fvg_mode == 3:
            high_low = self.df['High'] - self.df['Low']
            high_close = np.abs(self.df['High'] - self.df['Close'].shift(1))
            low_close = np.abs(self.df['Low'] - self.df['Close'].shift(1))
            true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
            self.df['ATR'] = true_range.rolling(window=14).mean()
        
        # Initialize FVG columns
        self.df['Bull_FVG_Low'] = np.nan
        self.df['Bull_FVG_High'] = np.nan
        self.df['Bear_FVG_Low'] = np.nan
        self.df['Bear_FVG_High'] = np.nan
        self.df['Bull_FVG_Bar'] = np.nan
        self.df['Bear_FVG_Bar'] = np.nan
        
        # Group by date for vectorized operations
        for date in self.df['Date'].unique():
            date_mask = self.df['Date'] == date
            date_indices = self.df[date_mask].index.tolist()
            
            if len(date_indices) < 3:
                continue
            
            # Get arrays for this date
            high = self.df.loc[date_indices, 'High'].values
            low = self.df.loc[date_indices, 'Low'].values
            
            # Vectorized FVG detection (starting from i=2)
            for i in range(2, len(date_indices)):
                idx = date_indices[i]
                
                # Bullish FVG: High[i-2] < Low[i]
                if high[i-2] < low[i]:
                    fvg_low = high[i-2]
                    fvg_high = low[i]
                    fvg_size = fvg_high - fvg_low
                    
                    # Apply mode 3 filter: Significant Gap (Volatility Filter)
                    if self.fvg_mode == 3:
                        atr_value = self.df.loc[idx, 'ATR']
                        if pd.notna(atr_value) and fvg_size <= 0.5 * atr_value:
                            continue  # Skip if gap is too small
                    
                    self.df.loc[idx, 'Bull_FVG_Low'] = fvg_low
                    self.df.loc[idx, 'Bull_FVG_High'] = fvg_high
                    self.df.loc[idx, 'Bull_FVG_Bar'] = i
                
                # Bearish FVG: Low[i-2] > High[i]
                if low[i-2] > high[i]:
                    fvg_high = low[i-2]
                    fvg_low = high[i]
                    fvg_size = fvg_high - fvg_low
                    
                    # Apply mode 3 filter: Significant Gap (Volatility Filter)
                    if self.fvg_mode == 3:
                        atr_value = self.df.loc[idx, 'ATR']
                        if pd.notna(atr_value) and fvg_size <= 0.5 * atr_value:
                            continue  # Skip if gap is too small
                    
                    self.df.loc[idx, 'Bear_FVG_Low'] = fvg_low
                    self.df.loc[idx, 'Bear_FVG_High'] = fvg_high
                    self.df.loc[idx, 'Bear_FVG_Bar'] = i
        
        # Forward fill the last active FVG
        self.df['Last_Bull_FVG_Low'] = self.df['Bull_FVG_Low'].ffill()
        self.df['Last_Bull_FVG_High'] = self.df['Bull_FVG_High'].ffill()
        self.df['Last_Bull_FVG_Bar'] = self.df['Bull_FVG_Bar'].ffill()
        
        self.df['Last_Bear_FVG_Low'] = self.df['Bear_FVG_Low'].ffill()
        self.df['Last_Bear_FVG_High'] = self.df['Bear_FVG_High'].ffill()
        self.df['Last_Bear_FVG_Bar'] = self.df['Bear_FVG_Bar'].ffill()
        
        # Count detected FVGs
        bull_fvg_count = self.df['Bull_FVG_Low'].notna().sum()
        bear_fvg_count = self.df['Bear_FVG_Low'].notna().sum()
        print(f"Detected {bull_fvg_count} Bullish FVGs and {bear_fvg_count} Bearish FVGs")
        
    def apply_mode_filter(self):
        """
        Apply the selected mode filter to generate trading signals.
        
        Mode 1: Standard (Proximal Entry)
        Mode 2: Consequent Encroachment (50% Retracement)
        Mode 3: Significant Gap (already applied in detect_fvg)
        Mode 4: Freshness Filter (Temporal Validity)
        """
        print(f"\nApplying Mode {self.fvg_mode} filter...")
        
        # Initialize signal columns
        self.df['Bull_Signal_Candidate'] = False
        self.df['Bear_Signal_Candidate'] = False
        
        for date in self.df['Date'].unique():
            date_mask = self.df['Date'] == date
            date_indices = self.df[date_mask].index.tolist()
            
            if len(date_indices) < 3:
                continue
            
            # Track the bar number within the day
            for bar_num, idx in enumerate(date_indices):
                # Get current candle data
                current_low = self.df.loc[idx, 'Low']
                current_high = self.df.loc[idx, 'High']
                current_close = self.df.loc[idx, 'Close']
                
                # Check Bullish FVG
                bull_fvg_low = self.df.loc[idx, 'Last_Bull_FVG_Low']
                bull_fvg_high = self.df.loc[idx, 'Last_Bull_FVG_High']
                bull_fvg_bar = self.df.loc[idx, 'Last_Bull_FVG_Bar']
                
                if pd.notna(bull_fvg_low) and pd.notna(bull_fvg_high):
                    # Mode 4: Freshness Filter (check age)
                    if self.fvg_mode == 4:
                        fvg_age = bar_num - bull_fvg_bar
                        if fvg_age > 15:
                            bull_fvg_low = np.nan  # Expire the FVG
                    
                    if pd.notna(bull_fvg_low):
                        # Mode 1: Standard (Proximal Entry)
                        if self.fvg_mode == 1:
                            # Price touches proximal line (bottom of bullish FVG)
                            # Low touches zone but Close doesn't traverse completely
                            if current_low <= bull_fvg_low and current_close >= bull_fvg_low:
                                self.df.loc[idx, 'Bull_Signal_Candidate'] = True
                        
                        # Mode 2: Consequent Encroachment (50% Retracement)
                        elif self.fvg_mode == 2:
                            fvg_median = (bull_fvg_low + bull_fvg_high) / 2
                            # Price must cross the median level
                            if current_low <= fvg_median and current_close >= fvg_median:
                                self.df.loc[idx, 'Bull_Signal_Candidate'] = True
                        
                        # Mode 3: Significant Gap (use standard proximal entry)
                        elif self.fvg_mode == 3:
                            if current_low <= bull_fvg_low and current_close >= bull_fvg_low:
                                self.df.loc[idx, 'Bull_Signal_Candidate'] = True
                        
                        # Mode 4: Freshness Filter (use standard proximal entry)
                        elif self.fvg_mode == 4:
                            if current_low <= bull_fvg_low and current_close >= bull_fvg_low:
                                self.df.loc[idx, 'Bull_Signal_Candidate'] = True
                
                # Check Bearish FVG
                bear_fvg_low = self.df.loc[idx, 'Last_Bear_FVG_Low']
                bear_fvg_high = self.df.loc[idx, 'Last_Bear_FVG_High']
                bear_fvg_bar = self.df.loc[idx, 'Last_Bear_FVG_Bar']
                
                if pd.notna(bear_fvg_low) and pd.notna(bear_fvg_high):
                    # Mode 4: Freshness Filter (check age)
                    if self.fvg_mode == 4:
                        fvg_age = bar_num - bear_fvg_bar
                        if fvg_age > 15:
                            bear_fvg_low = np.nan  # Expire the FVG
                    
                    if pd.notna(bear_fvg_low):
                        # Mode 1: Standard (Proximal Entry)
                        if self.fvg_mode == 1:
                            # Price touches proximal line (top of bearish FVG)
                            # High touches zone but Close doesn't traverse completely
                            if current_high >= bear_fvg_high and current_close <= bear_fvg_high:
                                self.df.loc[idx, 'Bear_Signal_Candidate'] = True
                        
                        # Mode 2: Consequent Encroachment (50% Retracement)
                        elif self.fvg_mode == 2:
                            fvg_median = (bear_fvg_low + bear_fvg_high) / 2
                            # Price must cross the median level
                            if current_high >= fvg_median and current_close <= fvg_median:
                                self.df.loc[idx, 'Bear_Signal_Candidate'] = True
                        
                        # Mode 3: Significant Gap (use standard proximal entry)
                        elif self.fvg_mode == 3:
                            if current_high >= bear_fvg_high and current_close <= bear_fvg_high:
                                self.df.loc[idx, 'Bear_Signal_Candidate'] = True
                        
                        # Mode 4: Freshness Filter (use standard proximal entry)
                        elif self.fvg_mode == 4:
                            if current_high >= bear_fvg_high and current_close <= bear_fvg_high:
                                self.df.loc[idx, 'Bear_Signal_Candidate'] = True
        
        bull_signals = self.df['Bull_Signal_Candidate'].sum()
        bear_signals = self.df['Bear_Signal_Candidate'].sum()
        print(f"Generated {bull_signals} bullish and {bear_signals} bearish signal candidates")
        
    def calculate_signals(self):
        """
        Calculate final trading signals ensuring only one position at a time.
        """
        print("\nCalculating final trading signals...")
        
        # Initialize signal columns
        self.df['Signal'] = 0  # 1 = Long, -1 = Short, 0 = No position
        self.df['Entry_Price'] = np.nan
        self.df['Stop_Loss'] = np.nan
        self.df['Take_Profit'] = np.nan
        self.df['Exit_Price'] = np.nan
        self.df['Exit_Reason'] = ''
        
        # Process signals day by day
        for date in self.df['Date'].unique():
            date_mask = self.df['Date'] == date
            date_indices = self.df[date_mask].index.tolist()
            
            in_position = False
            position_type = 0  # 1 = Long, -1 = Short
            entry_price = 0
            stop_loss = 0
            take_profit = 0
            entry_idx = None
            
            for idx in date_indices:
                current_time = self.df.loc[idx, 'Time']
                current_high = self.df.loc[idx, 'High']
                current_low = self.df.loc[idx, 'Low']
                current_close = self.df.loc[idx, 'Close']
                
                # Hard exit at 05:00:00
                if current_time == '05:00:00' and in_position:
                    self.df.loc[idx, 'Signal'] = 0
                    self.df.loc[idx, 'Exit_Price'] = current_close
                    self.df.loc[idx, 'Exit_Reason'] = 'Session End'
                    in_position = False
                    position_type = 0
                    continue
                
                # Manage existing position
                if in_position:
                    # Check stop loss and take profit
                    if position_type == 1:  # Long position
                        if current_low <= stop_loss:
                            # Stop loss hit
                            self.df.loc[idx, 'Signal'] = 0
                            self.df.loc[idx, 'Exit_Price'] = stop_loss
                            self.df.loc[idx, 'Exit_Reason'] = 'Stop Loss'
                            in_position = False
                            position_type = 0
                        elif current_high >= take_profit:
                            # Take profit hit
                            self.df.loc[idx, 'Signal'] = 0
                            self.df.loc[idx, 'Exit_Price'] = take_profit
                            self.df.loc[idx, 'Exit_Reason'] = 'Take Profit'
                            in_position = False
                            position_type = 0
                        else:
                            # Still in position
                            self.df.loc[idx, 'Signal'] = 1
                    
                    elif position_type == -1:  # Short position
                        if current_high >= stop_loss:
                            # Stop loss hit
                            self.df.loc[idx, 'Signal'] = 0
                            self.df.loc[idx, 'Exit_Price'] = stop_loss
                            self.df.loc[idx, 'Exit_Reason'] = 'Stop Loss'
                            in_position = False
                            position_type = 0
                        elif current_low <= take_profit:
                            # Take profit hit
                            self.df.loc[idx, 'Signal'] = 0
                            self.df.loc[idx, 'Exit_Price'] = take_profit
                            self.df.loc[idx, 'Exit_Reason'] = 'Take Profit'
                            in_position = False
                            position_type = 0
                        else:
                            # Still in position
                            self.df.loc[idx, 'Signal'] = -1
                
                # Check for new entries (only if not in position)
                if not in_position:
                    bull_signal = self.df.loc[idx, 'Bull_Signal_Candidate']
                    bear_signal = self.df.loc[idx, 'Bear_Signal_Candidate']
                    
                    # Prioritize bullish signals
                    if bull_signal:
                        # Enter long position
                        entry_price = current_close
                        stop_loss = entry_price - self.stop_loss
                        take_profit = entry_price + self.take_profit
                        
                        self.df.loc[idx, 'Signal'] = 1
                        self.df.loc[idx, 'Entry_Price'] = entry_price
                        self.df.loc[idx, 'Stop_Loss'] = stop_loss
                        self.df.loc[idx, 'Take_Profit'] = take_profit
                        
                        in_position = True
                        position_type = 1
                        entry_idx = idx
                    
                    elif bear_signal:
                        # Enter short position
                        entry_price = current_close
                        stop_loss = entry_price + self.stop_loss
                        take_profit = entry_price - self.take_profit
                        
                        self.df.loc[idx, 'Signal'] = -1
                        self.df.loc[idx, 'Entry_Price'] = entry_price
                        self.df.loc[idx, 'Stop_Loss'] = stop_loss
                        self.df.loc[idx, 'Take_Profit'] = take_profit
                        
                        in_position = True
                        position_type = -1
                        entry_idx = idx
        
        # Count trades
        entries = (self.df['Entry_Price'].notna()).sum()
        print(f"Generated {entries} trade entries")
        
    def apply_risk_management(self):
        """
        Apply risk management rules (Stop Loss and Take Profit).
        This is already integrated in calculate_signals() method.
        """
        print("\nRisk management applied:")
        print(f"  Stop Loss: {self.stop_loss} points")
        print(f"  Take Profit: {self.take_profit} points")
        
    def calculate_performance(self):
        """
        Calculate performance metrics for the backtest.
        """
        print("\nCalculating performance metrics...")
        
        # Find all completed trades
        trade_entries = self.df[self.df['Entry_Price'].notna()].copy()
        
        if len(trade_entries) == 0:
            print("No trades executed")
            self.results = {
                'total_return': 0,
                'win_rate': 0,
                'max_drawdown': 0,
                'num_trades': 0,
                'avg_trade_duration': 0,
                'winning_trades': 0,
                'losing_trades': 0
            }
            return
        
        # Calculate P&L for each trade
        trade_pnl = []
        trade_durations = []
        
        for entry_idx in trade_entries.index:
            entry_price = self.df.loc[entry_idx, 'Entry_Price']
            position_type = self.df.loc[entry_idx, 'Signal']
            
            # Find exit
            date = self.df.loc[entry_idx, 'Date']
            date_mask = self.df['Date'] == date
            date_indices = self.df[date_mask].index.tolist()
            
            # Find the next exit after entry
            exit_idx = None
            for idx in date_indices:
                if idx > entry_idx and self.df.loc[idx, 'Exit_Price'] > 0:
                    exit_idx = idx
                    break
            
            if exit_idx is not None:
                exit_price = self.df.loc[exit_idx, 'Exit_Price']
                
                # Calculate P&L in points
                if position_type == 1:  # Long
                    pnl = exit_price - entry_price
                else:  # Short
                    pnl = entry_price - exit_price
                
                trade_pnl.append(pnl)
                
                # Calculate duration (number of bars)
                duration = exit_idx - entry_idx
                trade_durations.append(duration)
        
        # Calculate metrics
        total_return = sum(trade_pnl)
        num_trades = len(trade_pnl)
        
        if num_trades > 0:
            winning_trades = sum(1 for pnl in trade_pnl if pnl > 0)
            losing_trades = sum(1 for pnl in trade_pnl if pnl < 0)
            win_rate = (winning_trades / num_trades) * 100
            avg_trade_duration = np.mean(trade_durations) if trade_durations else 0
            
            # Calculate max drawdown
            cumulative_pnl = np.cumsum(trade_pnl)
            running_max = np.maximum.accumulate(cumulative_pnl)
            drawdown = running_max - cumulative_pnl
            max_drawdown = np.max(drawdown) if len(drawdown) > 0 else 0
        else:
            winning_trades = 0
            losing_trades = 0
            win_rate = 0
            avg_trade_duration = 0
            max_drawdown = 0
        
        self.results = {
            'total_return': total_return,
            'win_rate': win_rate,
            'max_drawdown': max_drawdown,
            'num_trades': num_trades,
            'avg_trade_duration': avg_trade_duration,
            'winning_trades': winning_trades,
            'losing_trades': losing_trades
        }
        
    def print_performance_report(self):
        """
        Print a detailed performance report.
        """
        print("\n" + "="*60)
        print("ADVANCED FVG BACKTEST PERFORMANCE REPORT")
        print("="*60)
        print(f"\nFile: {self.csv_file_path}")
        print(f"FVG Mode: {self.fvg_mode}")
        
        mode_names = {
            1: "Standard (Proximal Entry)",
            2: "Consequent Encroachment (50% Retracement)",
            3: "Significant Gap (Volatility Filter)",
            4: "Freshness Filter (Temporal Validity)"
        }
        print(f"Mode Description: {mode_names[self.fvg_mode]}")
        
        print(f"\nRisk Management:")
        print(f"  Stop Loss: {self.stop_loss} points")
        print(f"  Take Profit: {self.take_profit} points")
        
        print(f"\nPerformance Metrics:")
        print(f"  Total Return: {self.results['total_return']:.2f} points")
        print(f"  Number of Trades: {self.results['num_trades']}")
        print(f"  Winning Trades: {self.results['winning_trades']}")
        print(f"  Losing Trades: {self.results['losing_trades']}")
        print(f"  Win Rate: {self.results['win_rate']:.2f}%")
        print(f"  Max Drawdown: {self.results['max_drawdown']:.2f} points")
        print(f"  Avg Trade Duration: {self.results['avg_trade_duration']:.2f} bars")
        
        if self.results['num_trades'] > 0:
            avg_return_per_trade = self.results['total_return'] / self.results['num_trades']
            print(f"  Avg Return per Trade: {avg_return_per_trade:.2f} points")
        
        print("="*60)
        
    def run(self):
        """
        Main execution method to run the backtest.
        
        Returns:
        --------
        dict : Performance results
        """
        print(f"\n{'='*60}")
        print(f"STARTING ADVANCED FVG BACKTEST - MODE {self.fvg_mode}")
        print(f"{'='*60}")
        
        # Step 1: Load data
        self.load_data()
        
        # Step 2: Filter session
        self.filter_session()
        
        # Step 3: Detect FVG
        self.detect_fvg()
        
        # Step 4: Apply mode filter
        self.apply_mode_filter()
        
        # Step 5: Calculate signals
        self.calculate_signals()
        
        # Step 6: Apply risk management (already done in calculate_signals)
        self.apply_risk_management()
        
        # Step 7: Calculate performance
        self.calculate_performance()
        
        # Step 8: Print report
        self.print_performance_report()
        
        return self.results


def main():
    """
    Demonstration of all 4 FVG modes with sample data.
    """
    import os
    
    print("\n" + "="*80)
    print("ADVANCED FVG BACKTEST - DEMONSTRATION OF ALL 4 MODES")
    print("="*80)
    
    # Find a sample CSV file
    sample_files = []
    base_path = '/home/runner/work/Backtest-Trading/Backtest-Trading'
    
    for year in range(2018, 2026):
        csv_file = os.path.join(base_path, f"{year} 5m.csv")
        if os.path.exists(csv_file):
            sample_files.append(csv_file)
    
    if not sample_files:
        print("No CSV files found. Please ensure data files are present.")
        return
    
    # Use the most recent file
    test_file = sample_files[-1] if sample_files else None
    
    if test_file:
        print(f"\nUsing test file: {test_file}\n")
        
        # Test all 4 modes
        for mode in range(1, 5):
            print(f"\n{'#'*80}")
            print(f"# TESTING MODE {mode}")
            print(f"{'#'*80}\n")
            
            bt = FVGAdvancedBacktest(
                test_file,
                fvg_mode=mode,
                stop_loss=25,
                take_profit=50
            )
            
            results = bt.run()
            
            print(f"\n{'='*80}\n")
    
    print("\n" + "="*80)
    print("DEMONSTRATION COMPLETE")
    print("="*80)


if __name__ == "__main__":
    main()

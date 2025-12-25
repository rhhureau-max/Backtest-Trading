#!/usr/bin/env python3
"""
Vectorized Backtesting Script for Nasdaq (NQ) Trading Strategies
Author: Trading Analysis System
Date: 2025

This script implements three trading strategies:
1. Opening Range Breakout (ORB)
2. Mean Reversion (RSI)
3. Trend Following (EMA Cross)

All operations are vectorized using pandas for optimal performance.
"""

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')


class BacktestStrategy:
    """
    Vectorized backtesting engine for trading strategies.
    """
    
    def __init__(self, csv_file_path, strategy='ORB'):
        """
        Initialize the backtesting engine.
        
        Parameters:
        -----------
        csv_file_path : str
            Path to the CSV file with trading data
        strategy : str
            Strategy to use: 'ORB', 'RSI', or 'EMA'
        """
        self.csv_file_path = csv_file_path
        self.strategy = strategy.upper()
        self.df = None
        self.results = {}
        
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
        
    def calculate_returns(self):
        """
        Calculate simple returns for the close prices.
        """
        self.df['Returns'] = self.df['Close'].pct_change()
        
    def strategy_orb(self):
        """
        Strategy 1: Opening Range Breakout (ORB)
        - Calculate High and Low of the first candle available after 01:00:00
        - If price breaks above High → Buy (long)
        - If price breaks below Low → Sell (short)
        """
        print("\nApplying Opening Range Breakout (ORB) Strategy...")
        
        # Initialize signal column
        self.df['Signal'] = 0
        
        # Group by date to find the first candle of each day
        for date in self.df['Date'].unique():
            date_mask = self.df['Date'] == date
            date_indices = self.df[date_mask].index
            
            if len(date_indices) == 0:
                continue
            
            # Get the first candle (opening range)
            first_idx = date_indices[0]
            or_high = self.df.loc[first_idx, 'High']
            or_low = self.df.loc[first_idx, 'Low']
            
            # For all subsequent candles in the day
            for idx in date_indices[1:]:
                current_close = self.df.loc[idx, 'Close']
                
                # Breakout above opening range high → Long
                if current_close > or_high:
                    self.df.loc[idx, 'Signal'] = 1
                # Breakout below opening range low → Short
                elif current_close < or_low:
                    self.df.loc[idx, 'Signal'] = -1
                else:
                    # No signal, maintain previous signal if any
                    if idx > date_indices[1]:
                        self.df.loc[idx, 'Signal'] = self.df.loc[idx - 1, 'Signal']
        
        # Force close all positions at 05:00:00
        self.force_close_at_session_end()
        
    def strategy_rsi(self, period=14):
        """
        Strategy 2: Mean Reversion (RSI)
        - If RSI(14) < 30 → Buy (long)
        - If RSI(14) > 70 → Sell (short)
        """
        print("\nApplying Mean Reversion (RSI) Strategy...")
        
        # Calculate RSI using vectorized operations
        delta = self.df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        
        rs = gain / loss
        self.df['RSI'] = 100 - (100 / (1 + rs))
        
        # Generate signals based on RSI
        self.df['Signal'] = 0
        self.df.loc[self.df['RSI'] < 30, 'Signal'] = 1   # Oversold → Buy
        self.df.loc[self.df['RSI'] > 70, 'Signal'] = -1  # Overbought → Sell
        
        # Forward fill signals (maintain position until new signal)
        self.df['Signal'] = self.df['Signal'].replace(0, np.nan).ffill().fillna(0)
        
        # Force close all positions at 05:00:00
        self.force_close_at_session_end()
        
    def strategy_ema(self, fast_period=9, slow_period=21):
        """
        Strategy 3: Trend Following (EMA Cross)
        - Buy when EMA(9) crosses above EMA(21)
        - Sell when EMA(9) crosses below EMA(21)
        """
        print("\nApplying Trend Following (EMA Cross) Strategy...")
        
        # Calculate EMAs
        self.df['EMA_Fast'] = self.df['Close'].ewm(span=fast_period, adjust=False).mean()
        self.df['EMA_Slow'] = self.df['Close'].ewm(span=slow_period, adjust=False).mean()
        
        # Initialize signal
        self.df['Signal'] = 0
        
        # Detect crossovers vectorized
        self.df['EMA_Diff'] = self.df['EMA_Fast'] - self.df['EMA_Slow']
        self.df['EMA_Diff_Prev'] = self.df['EMA_Diff'].shift(1)
        
        # Bullish crossover (EMA_Fast crosses above EMA_Slow)
        bullish_cross = (self.df['EMA_Diff'] > 0) & (self.df['EMA_Diff_Prev'] <= 0)
        # Bearish crossover (EMA_Fast crosses below EMA_Slow)
        bearish_cross = (self.df['EMA_Diff'] < 0) & (self.df['EMA_Diff_Prev'] >= 0)
        
        self.df.loc[bullish_cross, 'Signal'] = 1   # Long
        self.df.loc[bearish_cross, 'Signal'] = -1  # Short
        
        # Forward fill signals (maintain position until crossover)
        self.df['Signal'] = self.df['Signal'].replace(0, np.nan).ffill().fillna(0)
        
        # Force close all positions at 05:00:00
        self.force_close_at_session_end()
        
    def force_close_at_session_end(self):
        """
        Force close all positions at 05:00:00.
        """
        # Find all rows where time is 05:00:00
        end_session_mask = self.df['Time'] == '05:00:00'
        
        # Set signal to 0 for these rows (close position)
        # But we need to make sure we capture the last return before closing
        for idx in self.df[end_session_mask].index:
            # If this is not the last row in dataframe
            if idx < len(self.df) - 1:
                # Set next row signal to 0 to close position
                self.df.loc[idx + 1, 'Signal'] = 0
            # For the 05:00:00 row itself, we keep the signal to capture returns
            # Then we'll zero out after calculating strategy returns
        
    def calculate_strategy_returns(self):
        """
        Calculate strategy returns based on signals.
        Strategy returns = Signal(t-1) * Returns(t)
        """
        # Shift signal by 1 to avoid look-ahead bias
        # We use yesterday's signal to calculate today's return
        self.df['Signal_Shifted'] = self.df['Signal'].shift(1).fillna(0)
        
        # Calculate strategy returns
        self.df['Strategy_Return'] = self.df['Signal_Shifted'] * self.df['Returns']
        
        # Fill NaN values with 0
        self.df['Strategy_Return'] = self.df['Strategy_Return'].fillna(0)
        
        # Ensure positions are closed at 05:00:00
        # After 05:00:00, set strategy return to 0
        end_session_mask = self.df['Time'] == '05:00:00'
        for idx in self.df[end_session_mask].index:
            if idx < len(self.df) - 1:
                self.df.loc[idx + 1, 'Strategy_Return'] = 0
        
    def calculate_performance_metrics(self):
        """
        Calculate performance metrics for the strategy.
        """
        print("\n" + "=" * 60)
        print(f"PERFORMANCE REPORT - {self.strategy} STRATEGY")
        print("=" * 60)
        
        # Cumulative returns
        self.df['Cumulative_Return'] = (1 + self.df['Strategy_Return']).cumprod()
        total_return = self.df['Cumulative_Return'].iloc[-1] - 1
        
        print(f"\nTotal Cumulative Return: {total_return * 100:.2f}%")
        
        # Maximum Drawdown
        cumulative = self.df['Cumulative_Return']
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max) / running_max
        max_drawdown = drawdown.min()
        
        print(f"Maximum Drawdown: {max_drawdown * 100:.2f}%")
        
        # Sharpe Ratio (simplified - annualized)
        # Assuming 252 trading days per year
        strategy_returns = self.df['Strategy_Return']
        mean_return = strategy_returns.mean()
        std_return = strategy_returns.std()
        
        if std_return != 0:
            # Annualization factor depends on data frequency
            # For intraday data, we need to estimate trades per year
            sharpe_ratio = (mean_return / std_return) * np.sqrt(252)
        else:
            sharpe_ratio = 0
            
        print(f"Sharpe Ratio (Annualized): {sharpe_ratio:.2f}")
        
        # Additional metrics
        total_trades = (self.df['Signal'] != self.df['Signal'].shift(1)).sum()
        winning_trades = (self.df['Strategy_Return'] > 0).sum()
        losing_trades = (self.df['Strategy_Return'] < 0).sum()
        
        print(f"\nTotal Signal Changes: {total_trades}")
        print(f"Winning Periods: {winning_trades}")
        print(f"Losing Periods: {losing_trades}")
        
        if winning_trades + losing_trades > 0:
            win_rate = winning_trades / (winning_trades + losing_trades) * 100
            print(f"Win Rate: {win_rate:.2f}%")
        
        # Store results
        self.results = {
            'Total_Return': total_return,
            'Max_Drawdown': max_drawdown,
            'Sharpe_Ratio': sharpe_ratio,
            'Total_Trades': total_trades,
            'Winning_Trades': winning_trades,
            'Losing_Trades': losing_trades
        }
        
        print("=" * 60)
        
    def run(self):
        """
        Execute the complete backtesting workflow.
        """
        print(f"\n{'*' * 60}")
        print(f"STARTING BACKTEST - {self.strategy} STRATEGY")
        print(f"{'*' * 60}")
        
        # Step 1: Load data
        self.load_data()
        
        # Step 2: Filter session
        self.filter_session()
        
        # Step 3: Calculate returns
        self.calculate_returns()
        
        # Step 4: Apply strategy
        if self.strategy == 'ORB':
            self.strategy_orb()
        elif self.strategy == 'RSI':
            self.strategy_rsi()
        elif self.strategy == 'EMA':
            self.strategy_ema()
        else:
            raise ValueError(f"Unknown strategy: {self.strategy}. Choose 'ORB', 'RSI', or 'EMA'")
        
        # Step 5: Calculate strategy returns
        self.calculate_strategy_returns()
        
        # Step 6: Calculate performance metrics
        self.calculate_performance_metrics()
        
        return self.df, self.results


def main():
    """
    Main function to run the backtesting script.
    """
    # ========================================================================
    # CONFIGURATION - Modify these parameters
    # ========================================================================
    
    # Path to your CSV file - REPLACE WITH YOUR FILE PATH
    csv_file = '/home/runner/work/Backtest-Trading/Backtest-Trading/2025 5m.csv'
    
    # Choose strategy: 'ORB', 'RSI', or 'EMA'
    strategy = 'ORB'  # Change this to test different strategies
    
    # ========================================================================
    
    # Initialize and run backtest
    backtest = BacktestStrategy(csv_file_path=csv_file, strategy=strategy)
    df_results, metrics = backtest.run()
    
    # Optional: Save results to CSV
    # df_results.to_csv('backtest_results.csv', index=False)
    # print("\nResults saved to 'backtest_results.csv'")
    
    # Optional: Display first few rows of results
    print("\nFirst 10 rows of results:")
    print(df_results[['DateTime', 'Close', 'Signal', 'Returns', 'Strategy_Return']].head(10))
    
    print("\n" + "=" * 60)
    print("BACKTEST COMPLETED SUCCESSFULLY")
    print("=" * 60)


if __name__ == "__main__":
    main()

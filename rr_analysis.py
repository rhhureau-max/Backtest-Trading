#!/usr/bin/env python3
"""
Risk/Reward (RR) Analysis for Backtest Trading Strategy
Analyzes trades from backtest_results.csv with different stop-loss placements and RR ratios.
"""

import pandas as pd
import numpy as np
import os
import zipfile
import tempfile
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')


class RRAnalysis:
    """
    Risk/Reward analysis for identified trades.
    Tests multiple SL placements and RR ratios for each trade.
    """
    
    def __init__(self, base_path: str, results_file: str = 'backtest_results.csv'):
        """
        Initialize the RR analysis.
        
        Args:
            base_path: Base directory containing the CSV files
            results_file: Path to the backtest results CSV file
        """
        self.base_path = base_path
        self.results_file = os.path.join(base_path, results_file)
        
        # RR ratios to test
        self.rr_ratios = [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]
        
        # SL placement percentages (percentage of candle body retracement)
        self.sl_placements = {
            'SL_100': 1.00,  # Full body retracement
            'SL_75': 0.75,   # 75% retracement (SL at 25% from open)
            'SL_50': 0.50,   # 50% retracement (middle)
            'SL_25': 0.25    # 25% retracement (SL at 75% from open)
        }
        
        self.trade_results = []
        self.summary_stats = {}
        
        # Cache for loaded data files
        self.data_cache = {}
        
    def read_csv_file(self, filepath: str) -> pd.DataFrame:
        """
        Read CSV file, handling both zipped and regular files.
        
        Args:
            filepath: Path to the CSV file (can be .csv or .csv.zip)
            
        Returns:
            DataFrame containing the data
        """
        try:
            if filepath.endswith('.zip'):
                with zipfile.ZipFile(filepath, 'r') as zip_ref:
                    csv_filename = zip_ref.namelist()[0]
                    with tempfile.TemporaryDirectory() as temp_dir:
                        zip_ref.extract(csv_filename, temp_dir)
                        temp_csv_path = os.path.join(temp_dir, csv_filename)
                        df = pd.read_csv(
                            temp_csv_path,
                            sep=';',
                            names=['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume'],
                            skiprows=1
                        )
            else:
                df = pd.read_csv(
                    filepath,
                    sep=';',
                    names=['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume'],
                    skiprows=1
                )
            
            # Convert data types
            df['Open'] = pd.to_numeric(df['Open'], errors='coerce')
            df['High'] = pd.to_numeric(df['High'], errors='coerce')
            df['Low'] = pd.to_numeric(df['Low'], errors='coerce')
            df['Close'] = pd.to_numeric(df['Close'], errors='coerce')
            df['Volume'] = pd.to_numeric(df['Volume'], errors='coerce')
            
            # Parse datetime
            df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%d/%m/%Y %H:%M:%S')
            df = df.sort_values('DateTime').reset_index(drop=True)
            
            return df
            
        except Exception as e:
            print(f"Error reading {filepath}: {e}")
            return pd.DataFrame()
    
    def load_backtest_results(self) -> pd.DataFrame:
        """Load the backtest results from CSV file."""
        if not os.path.exists(self.results_file):
            raise FileNotFoundError(
                f"Backtest results file not found: {self.results_file}\n"
                f"Please run backtest_strategy.py first to generate the results."
            )
        
        df = pd.read_csv(self.results_file)
        print(f"Loaded {len(df)} trades from backtest results")
        return df
    
    def calculate_sl_levels(self, open_price: float, close_price: float, 
                           candle_type: str) -> Dict[str, float]:
        """
        Calculate stop-loss levels based on candle body retracement.
        
        Args:
            open_price: Open price of the candle
            close_price: Close price of the candle
            candle_type: 'BULLISH' or 'BEARISH'
            
        Returns:
            Dictionary with SL levels for each placement
        """
        sl_levels = {}
        body_size = abs(close_price - open_price)
        
        if candle_type == 'BULLISH':
            # For bullish candles: SL moves down from close towards open
            for sl_name, retracement in self.sl_placements.items():
                sl_levels[sl_name] = open_price + (1 - retracement) * body_size
        else:  # BEARISH
            # For bearish candles: SL moves up from close towards open
            for sl_name, retracement in self.sl_placements.items():
                sl_levels[sl_name] = open_price - (1 - retracement) * body_size
        
        return sl_levels
    
    def calculate_tp_level(self, entry: float, sl: float, rr_ratio: float, 
                          candle_type: str) -> float:
        """
        Calculate take profit level based on entry, SL, and RR ratio.
        
        Args:
            entry: Entry price
            sl: Stop loss price
            rr_ratio: Risk/reward ratio
            candle_type: 'BULLISH' or 'BEARISH'
            
        Returns:
            Take profit price level
        """
        risk = abs(entry - sl)
        reward = risk * rr_ratio
        
        if candle_type == 'BULLISH':
            return entry + reward
        else:  # BEARISH
            return entry - reward
    
    def simulate_trade_outcome(self, entry_datetime: datetime, entry_price: float,
                              sl_price: float, tp_price: float, candle_type: str,
                              timeframe: str, year: int, 
                              subsequent_candles: pd.DataFrame) -> Dict:
        """
        Simulate a trade to determine if SL or TP was hit first.
        
        Args:
            entry_datetime: Entry datetime
            entry_price: Entry price
            sl_price: Stop loss price
            tp_price: Take profit price
            candle_type: 'BULLISH' or 'BEARISH'
            timeframe: Timeframe
            year: Year
            subsequent_candles: DataFrame of candles after entry
            
        Returns:
            Dictionary with trade outcome details
        """
        outcome = {
            'sl_hit': False,
            'tp_hit': False,
            'result': 'PENDING',
            'exit_price': None,
            'exit_datetime': None,
            'bars_in_trade': 0,
            'mae': 0.0,  # Maximum Adverse Excursion
            'mfe': 0.0   # Maximum Favorable Excursion
        }
        
        if subsequent_candles.empty:
            return outcome
        
        max_adverse = 0.0
        max_favorable = 0.0
        
        for idx, candle in subsequent_candles.iterrows():
            outcome['bars_in_trade'] += 1
            
            # Calculate adverse and favorable excursions for this candle
            if candle_type == 'BULLISH':
                adverse = entry_price - candle['Low']
                favorable = candle['High'] - entry_price
                
                # Check if SL was hit (price went down to SL)
                if candle['Low'] <= sl_price:
                    outcome['sl_hit'] = True
                    outcome['result'] = 'LOSS'
                    outcome['exit_price'] = sl_price
                    outcome['exit_datetime'] = candle['DateTime']
                    break
                
                # Check if TP was hit (price went up to TP)
                if candle['High'] >= tp_price:
                    outcome['tp_hit'] = True
                    outcome['result'] = 'WIN'
                    outcome['exit_price'] = tp_price
                    outcome['exit_datetime'] = candle['DateTime']
                    break
                    
            else:  # BEARISH
                adverse = candle['High'] - entry_price
                favorable = entry_price - candle['Low']
                
                # Check if SL was hit (price went up to SL)
                if candle['High'] >= sl_price:
                    outcome['sl_hit'] = True
                    outcome['result'] = 'LOSS'
                    outcome['exit_price'] = sl_price
                    outcome['exit_datetime'] = candle['DateTime']
                    break
                
                # Check if TP was hit (price went down to TP)
                if candle['Low'] <= tp_price:
                    outcome['tp_hit'] = True
                    outcome['result'] = 'WIN'
                    outcome['exit_price'] = tp_price
                    outcome['exit_datetime'] = candle['DateTime']
                    break
            
            # Track MAE and MFE
            max_adverse = max(max_adverse, adverse)
            max_favorable = max(max_favorable, favorable)
        
        outcome['mae'] = max_adverse
        outcome['mfe'] = max_favorable
        
        return outcome
    
    def load_data_file(self, timeframe: str, year: int) -> pd.DataFrame:
        """
        Load a data file with caching.
        
        Args:
            timeframe: Timeframe (1m, 5m, 15m)
            year: Year
            
        Returns:
            DataFrame containing the data
        """
        cache_key = f"{year}_{timeframe}"
        
        # Return from cache if already loaded
        if cache_key in self.data_cache:
            return self.data_cache[cache_key]
        
        filename = f"{year} {timeframe}.csv"
        filepath = os.path.join(self.base_path, filename)
        
        # Check if zipped version exists
        if not os.path.exists(filepath):
            filepath = os.path.join(self.base_path, f"{filename}.zip")
        
        if not os.path.exists(filepath):
            self.data_cache[cache_key] = pd.DataFrame()
            return pd.DataFrame()
        
        # Read the data
        df = self.read_csv_file(filepath)
        
        # Cache the data
        self.data_cache[cache_key] = df
        
        return df
    
    def get_subsequent_candles(self, entry_datetime: datetime, timeframe: str, 
                              year: int, max_candles: int = 500) -> pd.DataFrame:
        """
        Get subsequent candles after the entry datetime.
        
        Args:
            entry_datetime: Entry datetime
            timeframe: Timeframe (1m, 5m, 15m)
            year: Year
            max_candles: Maximum number of candles to retrieve
            
        Returns:
            DataFrame of subsequent candles
        """
        # Load the data (from cache if available)
        df = self.load_data_file(timeframe, year)
        
        if df.empty:
            return pd.DataFrame()
        
        # Get candles after entry datetime
        subsequent = df[df['DateTime'] > entry_datetime].head(max_candles)
        
        return subsequent
    
    def analyze_trade(self, trade: pd.Series) -> List[Dict]:
        """
        Analyze a single trade with all SL/RR combinations.
        
        Args:
            trade: Series containing trade information
            
        Returns:
            List of dictionaries containing results for each combination
        """
        results = []
        
        # Parse entry datetime
        entry_datetime = pd.to_datetime(trade['Date'] + ' ' + trade['Time'], 
                                       format='%d/%m/%Y %H:%M:%S')
        
        entry_price = trade['Close']
        open_price = trade['Open']
        candle_type = trade['Candle_Type']
        timeframe = trade['Timeframe']
        
        # Extract year from date
        year = pd.to_datetime(trade['Date'], format='%d/%m/%Y').year
        
        # Calculate all SL levels
        sl_levels = self.calculate_sl_levels(open_price, entry_price, candle_type)
        
        # Get subsequent candles for simulation
        subsequent_candles = self.get_subsequent_candles(entry_datetime, timeframe, year)
        
        if subsequent_candles.empty:
            return results
        
        # Test each SL placement
        for sl_name, sl_price in sl_levels.items():
            # Test each RR ratio
            for rr_ratio in self.rr_ratios:
                # Calculate TP level
                tp_price = self.calculate_tp_level(entry_price, sl_price, rr_ratio, candle_type)
                
                # Simulate trade outcome
                outcome = self.simulate_trade_outcome(
                    entry_datetime, entry_price, sl_price, tp_price,
                    candle_type, timeframe, year, subsequent_candles
                )
                
                # Calculate P&L
                risk_amount = abs(entry_price - sl_price)
                
                if outcome['result'] == 'WIN':
                    pnl = risk_amount * rr_ratio
                elif outcome['result'] == 'LOSS':
                    pnl = -risk_amount
                else:
                    pnl = 0.0
                
                # Store result
                result = {
                    'Date': trade['Date'],
                    'Time': trade['Time'],
                    'Timeframe': timeframe,
                    'Candle_Type': candle_type,
                    'Entry_Price': entry_price,
                    'Open_Price': open_price,
                    'SL_Placement': sl_name,
                    'SL_Price': sl_price,
                    'RR_Ratio': rr_ratio,
                    'TP_Price': tp_price,
                    'Risk_Amount': risk_amount,
                    'Potential_Reward': risk_amount * rr_ratio,
                    'Outcome': outcome['result'],
                    'Exit_Price': outcome['exit_price'],
                    'Exit_DateTime': outcome['exit_datetime'],
                    'Bars_In_Trade': outcome['bars_in_trade'],
                    'PnL': pnl,
                    'MAE': outcome['mae'],
                    'MFE': outcome['mfe']
                }
                
                results.append(result)
        
        return results
    
    def preload_data_files(self, trades_df: pd.DataFrame):
        """
        Preload all required data files into cache.
        
        Args:
            trades_df: DataFrame containing trades to analyze
        """
        print("Preloading data files...")
        
        # Get unique timeframe/year combinations
        unique_combos = trades_df[['Timeframe', 'Date']].drop_duplicates()
        unique_combos['Year'] = pd.to_datetime(unique_combos['Date'], format='%d/%m/%Y').dt.year
        
        files_to_load = unique_combos[['Timeframe', 'Year']].drop_duplicates()
        
        print(f"Loading {len(files_to_load)} unique data files...")
        
        for idx, row in files_to_load.iterrows():
            timeframe = row['Timeframe']
            year = row['Year']
            self.load_data_file(timeframe, year)
            if (idx + 1) % 5 == 0:
                print(f"  Loaded {idx + 1}/{len(files_to_load)} files...")
        
        print(f"Data preloading complete! {len(self.data_cache)} files cached.\n")
    
    def run_analysis(self) -> pd.DataFrame:
        """
        Run the complete RR analysis on all trades.
        
        Returns:
            DataFrame containing all trade results
        """
        print("=" * 80)
        print("RISK/REWARD ANALYSIS")
        print("=" * 80)
        print(f"\nRR Ratios to test: {', '.join(map(str, self.rr_ratios))}")
        print(f"SL Placements to test: {', '.join(self.sl_placements.keys())}")
        print(f"Total combinations per trade: {len(self.sl_placements) * len(self.rr_ratios)}")
        print("=" * 80)
        print()
        
        # Load backtest results
        trades_df = self.load_backtest_results()
        
        # Preload all required data files
        self.preload_data_files(trades_df)
        
        print(f"Analyzing {len(trades_df)} trades...")
        print()
        
        all_results = []
        
        # Analyze each trade
        for idx, trade in trades_df.iterrows():
            if (idx + 1) % 100 == 0:
                progress = (idx + 1) / len(trades_df) * 100
                print(f"Processing trade {idx + 1}/{len(trades_df)} ({progress:.1f}%)...")
            
            trade_results = self.analyze_trade(trade)
            all_results.extend(trade_results)
        
        print(f"\nAnalysis complete! Generated {len(all_results)} trade scenarios.")
        
        # Convert to DataFrame
        results_df = pd.DataFrame(all_results)
        self.trade_results = results_df
        
        return results_df
    
    def calculate_statistics(self, df: pd.DataFrame) -> Dict:
        """
        Calculate comprehensive statistics for a set of trades.
        
        Args:
            df: DataFrame containing trade results
            
        Returns:
            Dictionary with statistics
        """
        if df.empty or len(df) == 0:
            return {
                'total_trades': 0,
                'wins': 0,
                'losses': 0,
                'pending': 0,
                'win_rate': 0.0,
                'avg_win': 0.0,
                'avg_loss': 0.0,
                'avg_pnl': 0.0,
                'total_pnl': 0.0,
                'profit_factor': 0.0,
                'expectancy': 0.0,
                'avg_bars_in_trade': 0.0,
                'avg_mae': 0.0,
                'avg_mfe': 0.0
            }
        
        wins = df[df['Outcome'] == 'WIN']
        losses = df[df['Outcome'] == 'LOSS']
        pending = df[df['Outcome'] == 'PENDING']
        
        completed = df[df['Outcome'].isin(['WIN', 'LOSS'])]
        
        total_wins = len(wins)
        total_losses = len(losses)
        total_completed = len(completed)
        
        win_rate = (total_wins / total_completed * 100) if total_completed > 0 else 0.0
        
        avg_win = wins['PnL'].mean() if len(wins) > 0 else 0.0
        avg_loss = losses['PnL'].mean() if len(losses) > 0 else 0.0
        
        total_win_amount = wins['PnL'].sum() if len(wins) > 0 else 0.0
        total_loss_amount = abs(losses['PnL'].sum()) if len(losses) > 0 else 0.0
        
        profit_factor = (total_win_amount / total_loss_amount) if total_loss_amount > 0 else 0.0
        
        avg_pnl = completed['PnL'].mean() if len(completed) > 0 else 0.0
        total_pnl = completed['PnL'].sum() if len(completed) > 0 else 0.0
        
        expectancy = (win_rate/100 * avg_win) + ((1 - win_rate/100) * avg_loss)
        
        avg_bars = completed['Bars_In_Trade'].mean() if len(completed) > 0 else 0.0
        avg_mae = completed['MAE'].mean() if len(completed) > 0 else 0.0
        avg_mfe = completed['MFE'].mean() if len(completed) > 0 else 0.0
        
        return {
            'total_trades': len(df),
            'wins': total_wins,
            'losses': total_losses,
            'pending': len(pending),
            'win_rate': win_rate,
            'avg_win': avg_win,
            'avg_loss': avg_loss,
            'avg_pnl': avg_pnl,
            'total_pnl': total_pnl,
            'profit_factor': profit_factor,
            'expectancy': expectancy,
            'avg_bars_in_trade': avg_bars,
            'avg_mae': avg_mae,
            'avg_mfe': avg_mfe
        }
    
    def generate_summary_report(self, results_df: pd.DataFrame):
        """
        Generate and print comprehensive summary report.
        
        Args:
            results_df: DataFrame containing all trade results
        """
        print("\n" + "=" * 80)
        print("SUMMARY REPORT - ALL COMBINATIONS")
        print("=" * 80)
        
        # Overall statistics
        overall_stats = self.calculate_statistics(results_df)
        
        print(f"\nTotal Trade Scenarios: {overall_stats['total_trades']}")
        print(f"Wins: {overall_stats['wins']}")
        print(f"Losses: {overall_stats['losses']}")
        print(f"Pending: {overall_stats['pending']}")
        print(f"Win Rate: {overall_stats['win_rate']:.2f}%")
        print(f"Average Win: ${overall_stats['avg_win']:.2f}")
        print(f"Average Loss: ${overall_stats['avg_loss']:.2f}")
        print(f"Profit Factor: {overall_stats['profit_factor']:.2f}")
        print(f"Expectancy: ${overall_stats['expectancy']:.2f}")
        
        # Summary by SL placement and RR ratio
        print("\n" + "=" * 80)
        print("WIN RATE BY SL PLACEMENT AND RR RATIO")
        print("=" * 80)
        
        completed_df = results_df[results_df['Outcome'].isin(['WIN', 'LOSS'])]
        
        # Create pivot table for win rates
        pivot_data = []
        for sl_name in sorted(self.sl_placements.keys()):
            row_data = {'SL_Placement': sl_name}
            for rr_ratio in self.rr_ratios:
                subset = completed_df[
                    (completed_df['SL_Placement'] == sl_name) & 
                    (completed_df['RR_Ratio'] == rr_ratio)
                ]
                if len(subset) > 0:
                    wins = len(subset[subset['Outcome'] == 'WIN'])
                    win_rate = (wins / len(subset)) * 100
                    row_data[f'RR_{rr_ratio}'] = f"{win_rate:.1f}%"
                else:
                    row_data[f'RR_{rr_ratio}'] = "N/A"
            pivot_data.append(row_data)
        
        win_rate_df = pd.DataFrame(pivot_data)
        print("\n", win_rate_df.to_string(index=False))
        
        # Summary by SL placement and RR ratio - Expectancy
        print("\n" + "=" * 80)
        print("EXPECTANCY BY SL PLACEMENT AND RR RATIO")
        print("=" * 80)
        
        pivot_data = []
        for sl_name in sorted(self.sl_placements.keys()):
            row_data = {'SL_Placement': sl_name}
            for rr_ratio in self.rr_ratios:
                subset = completed_df[
                    (completed_df['SL_Placement'] == sl_name) & 
                    (completed_df['RR_Ratio'] == rr_ratio)
                ]
                stats = self.calculate_statistics(subset)
                row_data[f'RR_{rr_ratio}'] = f"${stats['expectancy']:.2f}"
            pivot_data.append(row_data)
        
        expectancy_df = pd.DataFrame(pivot_data)
        print("\n", expectancy_df.to_string(index=False))
        
        # Best performing combinations
        print("\n" + "=" * 80)
        print("TOP 10 BEST PERFORMING COMBINATIONS")
        print("=" * 80)
        
        combo_stats = []
        for sl_name in self.sl_placements.keys():
            for rr_ratio in self.rr_ratios:
                subset = completed_df[
                    (completed_df['SL_Placement'] == sl_name) & 
                    (completed_df['RR_Ratio'] == rr_ratio)
                ]
                stats = self.calculate_statistics(subset)
                combo_stats.append({
                    'SL_Placement': sl_name,
                    'RR_Ratio': rr_ratio,
                    'Trades': stats['total_trades'],
                    'Win_Rate': stats['win_rate'],
                    'Expectancy': stats['expectancy'],
                    'Profit_Factor': stats['profit_factor'],
                    'Total_PnL': stats['total_pnl']
                })
        
        combo_df = pd.DataFrame(combo_stats)
        combo_df = combo_df.sort_values('Expectancy', ascending=False).head(10)
        print("\n", combo_df.to_string(index=False))
        
        print("\n" + "=" * 80)
    
    def save_results(self, results_df: pd.DataFrame, output_dir: str = None):
        """
        Save detailed results to CSV files.
        
        Args:
            results_df: DataFrame containing all trade results
            output_dir: Directory to save results (defaults to base_path)
        """
        if output_dir is None:
            output_dir = self.base_path
        
        print("\n" + "=" * 80)
        print("SAVING RESULTS")
        print("=" * 80)
        
        # Save complete results
        main_output = os.path.join(output_dir, 'rr_analysis_complete.csv')
        results_df.to_csv(main_output, index=False)
        print(f"\nComplete results saved to: {main_output}")
        
        # Save results by SL placement
        for sl_name in self.sl_placements.keys():
            sl_df = results_df[results_df['SL_Placement'] == sl_name]
            sl_output = os.path.join(output_dir, f'rr_analysis_{sl_name}.csv')
            sl_df.to_csv(sl_output, index=False)
            print(f"Results for {sl_name} saved to: {sl_output}")
        
        # Save summary statistics
        completed_df = results_df[results_df['Outcome'].isin(['WIN', 'LOSS'])]
        
        summary_data = []
        for sl_name in self.sl_placements.keys():
            for rr_ratio in self.rr_ratios:
                subset = completed_df[
                    (completed_df['SL_Placement'] == sl_name) & 
                    (completed_df['RR_Ratio'] == rr_ratio)
                ]
                stats = self.calculate_statistics(subset)
                stats['SL_Placement'] = sl_name
                stats['RR_Ratio'] = rr_ratio
                summary_data.append(stats)
        
        summary_df = pd.DataFrame(summary_data)
        summary_output = os.path.join(output_dir, 'rr_analysis_summary.csv')
        summary_df.to_csv(summary_output, index=False)
        print(f"Summary statistics saved to: {summary_output}")
        
        print("\n" + "=" * 80)


def main():
    """Main execution function."""
    # Set the base path to the repository
    base_path = '/home/runner/work/Backtest-Trading/Backtest-Trading'
    
    # Initialize the RR analysis
    print("Initializing Risk/Reward Analysis...")
    rr_analyzer = RRAnalysis(base_path)
    
    try:
        # Run the analysis
        results_df = rr_analyzer.run_analysis()
        
        # Generate and print summary report
        rr_analyzer.generate_summary_report(results_df)
        
        # Save results
        rr_analyzer.save_results(results_df)
        
        print("\n" + "=" * 80)
        print("Risk/Reward Analysis Complete!")
        print("=" * 80)
        
    except FileNotFoundError as e:
        print(f"\nError: {e}")
        print("\nPlease run backtest_strategy.py first to generate the backtest results.")
        return 1
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())

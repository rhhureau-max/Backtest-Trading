"""
NQ (Nasdaq) Trading Strategy Matrix Backtest
=============================================
This script implements a comprehensive matrix backtest analyzing:
- 4 Stop Loss placement strategies
- 5 Take Profit targets
- 20 total combinations (4 SL x 5 TP)

Strategy based on Tokyo Session reference levels and London Killzone execution
with Fair Value Gap (FVG) inversions.
"""

import pandas as pd
import numpy as np
from datetime import datetime, time, timedelta
import os
from typing import List, Dict, Tuple, Optional
import warnings

warnings.filterwarnings('ignore')


class NQMatrixBacktester:
    """Matrix backtesting class for NQ trading strategy with multiple SL/TP combinations"""
    
    # Constants
    MAX_BARS_LOOKAHEAD = 1000  # Maximum bars to check for TP/SL (about 3.5 days on 5m data)
    SL_BUFFER = 2.0  # Buffer in points for SL1
    
    def __init__(self, data_directory: str):
        """
        Initialize the matrix backtester
        
        Args:
            data_directory: Path to directory containing CSV files
        """
        self.data_directory = data_directory
        self.df = None
        self.setups = []  # Store all valid setups
        
    def load_data(self) -> pd.DataFrame:
        """Load all 5-minute CSV files from 2018-2025"""
        print("Loading data files...")
        all_data = []
        
        for year in range(2018, 2026):
            filename = f"{year} 5m.csv"
            filepath = os.path.join(self.data_directory, filename)
            
            if os.path.exists(filepath):
                print(f"  Loading {filename}...")
                df = pd.read_csv(
                    filepath,
                    sep=';',
                    names=['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume'],
                    skiprows=1
                )
                all_data.append(df)
            else:
                print(f"  Warning: {filename} not found")
        
        if not all_data:
            raise FileNotFoundError("No data files found!")
        
        # Combine all data
        combined_df = pd.concat(all_data, ignore_index=True)
        
        # Parse datetime - format is DD/MM/YYYY and HH:MM:SS
        combined_df['DateTime'] = pd.to_datetime(
            combined_df['Date'] + ' ' + combined_df['Time'],
            format='%d/%m/%Y %H:%M:%S'
        )
        
        # Convert price columns to float
        for col in ['Open', 'High', 'Low', 'Close']:
            combined_df[col] = pd.to_numeric(combined_df[col], errors='coerce')
        
        # Sort by datetime
        combined_df = combined_df.sort_values('DateTime').reset_index(drop=True)
        
        # Extract time components
        combined_df['Date_only'] = combined_df['DateTime'].dt.date
        combined_df['Time_only'] = combined_df['DateTime'].dt.time
        combined_df['Hour'] = combined_df['DateTime'].dt.hour
        combined_df['Minute'] = combined_df['DateTime'].dt.minute
        
        print(f"Total records loaded: {len(combined_df)}")
        print(f"Date range: {combined_df['DateTime'].min()} to {combined_df['DateTime'].max()}")
        
        self.df = combined_df
        return combined_df
    
    def identify_tokyo_session(self, date) -> Optional[Dict]:
        """
        Identify Tokyo session for a given date (19:00-23:00 previous day)
        
        Args:
            date: The current trading date (Day N)
            
        Returns:
            Dictionary with Tokyo_High, Tokyo_Low, Tokyo_EQ, or None if not found
        """
        # Tokyo session is on the previous day (N-1)
        previous_date = date - timedelta(days=1)
        
        # Filter data for Tokyo session (19:00-23:00)
        tokyo_data = self.df[
            (self.df['Date_only'] == previous_date) &
            (self.df['Hour'] >= 19) &
            (self.df['Hour'] < 24)
        ]
        
        if len(tokyo_data) == 0:
            return None
        
        tokyo_high = tokyo_data['High'].max()
        tokyo_low = tokyo_data['Low'].min()
        tokyo_eq = (tokyo_high + tokyo_low) / 2
        
        return {
            'Tokyo_High': tokyo_high,
            'Tokyo_Low': tokyo_low,
            'Tokyo_EQ': tokyo_eq
        }
    
    def detect_fvg(self, df_slice: pd.DataFrame, fvg_type: str) -> List[Dict]:
        """
        Detect Fair Value Gaps in the data
        
        Args:
            df_slice: DataFrame slice to analyze
            fvg_type: 'bullish' or 'bearish'
            
        Returns:
            List of FVG dictionaries with start_idx, gap_low, gap_high
        """
        fvgs = []
        
        if len(df_slice) < 3:
            return fvgs
        
        df_slice = df_slice.reset_index(drop=True)
        
        for i in range(2, len(df_slice)):
            if fvg_type == 'bullish':
                # Bullish FVG: Low of candle (i-2) > High of candle (i)
                if df_slice.loc[i-2, 'Low'] > df_slice.loc[i, 'High']:
                    fvgs.append({
                        'idx': i,
                        'gap_low': df_slice.loc[i, 'High'],
                        'gap_high': df_slice.loc[i-2, 'Low'],
                        'datetime': df_slice.loc[i, 'DateTime'],
                        'candle_i_high': df_slice.loc[i, 'High'],
                        'candle_i_low': df_slice.loc[i, 'Low']
                    })
            elif fvg_type == 'bearish':
                # Bearish FVG: Low of candle (i) > High of candle (i-2)
                if df_slice.loc[i, 'Low'] > df_slice.loc[i-2, 'High']:
                    fvgs.append({
                        'idx': i,
                        'gap_low': df_slice.loc[i-2, 'High'],
                        'gap_high': df_slice.loc[i, 'Low'],
                        'datetime': df_slice.loc[i, 'DateTime'],
                        'candle_i_high': df_slice.loc[i, 'High'],
                        'candle_i_low': df_slice.loc[i, 'Low']
                    })
        
        return fvgs
    
    def check_sweep(self, killzone_data: pd.DataFrame, tokyo_high: float, tokyo_low: float) -> Dict:
        """
        Check if price sweeps Tokyo_High or Tokyo_Low during killzone
        
        Returns:
            Dictionary with sweep_type ('high', 'low', or None) and sweep_extreme
        """
        high_swept = False
        low_swept = False
        sweep_high_extreme = None
        sweep_low_extreme = None
        first_high_sweep_idx = None
        first_low_sweep_idx = None
        
        for idx, row in killzone_data.iterrows():
            # Check if high was swept
            if row['High'] > tokyo_high:
                high_swept = True
                if sweep_high_extreme is None or row['High'] > sweep_high_extreme:
                    sweep_high_extreme = row['High']
                if first_high_sweep_idx is None:
                    first_high_sweep_idx = idx
            
            # Check if low was swept
            if row['Low'] < tokyo_low:
                low_swept = True
                if sweep_low_extreme is None or row['Low'] < sweep_low_extreme:
                    sweep_low_extreme = row['Low']
                if first_low_sweep_idx is None:
                    first_low_sweep_idx = idx
        
        # Determine which sweep happened first
        if high_swept and low_swept:
            if first_high_sweep_idx < first_low_sweep_idx:
                return {'sweep_type': 'high', 'sweep_extreme': sweep_high_extreme}
            else:
                return {'sweep_type': 'low', 'sweep_extreme': sweep_low_extreme}
        elif high_swept:
            return {'sweep_type': 'high', 'sweep_extreme': sweep_high_extreme}
        elif low_swept:
            return {'sweep_type': 'low', 'sweep_extreme': sweep_low_extreme}
        
        return {'sweep_type': None, 'sweep_extreme': None}
    
    def find_entry_signal(self, killzone_data: pd.DataFrame, sweep_info: Dict, 
                          trade_type: str) -> Optional[Dict]:
        """
        Find entry signal based on FVG inversion
        
        Args:
            killzone_data: Data during killzone period
            sweep_info: Information about the sweep
            trade_type: 'short' or 'long'
            
        Returns:
            Entry information including signal candle details
        """
        killzone_data = killzone_data.reset_index(drop=True)
        
        if trade_type == 'short':
            # Look for bullish FVG during/after sweep, then candle closing below it
            fvgs = self.detect_fvg(killzone_data, 'bullish')
            
            for fvg in fvgs:
                # Check subsequent candles for close below FVG
                for i in range(fvg['idx'] + 1, len(killzone_data)):
                    if killzone_data.loc[i, 'Close'] < fvg['gap_low']:
                        return {
                            'entry_idx': i,
                            'entry_price': killzone_data.loc[i, 'Close'],
                            'entry_datetime': killzone_data.loc[i, 'DateTime'],
                            'signal_candle_high': killzone_data.loc[i, 'High'],
                            'signal_candle_low': killzone_data.loc[i, 'Low'],
                            'fvg': fvg
                        }
        
        elif trade_type == 'long':
            # Look for bearish FVG during/after sweep, then candle closing above it
            fvgs = self.detect_fvg(killzone_data, 'bearish')
            
            for fvg in fvgs:
                # Check subsequent candles for close above FVG
                for i in range(fvg['idx'] + 1, len(killzone_data)):
                    if killzone_data.loc[i, 'Close'] > fvg['gap_high']:
                        return {
                            'entry_idx': i,
                            'entry_price': killzone_data.loc[i, 'Close'],
                            'entry_datetime': killzone_data.loc[i, 'DateTime'],
                            'signal_candle_high': killzone_data.loc[i, 'High'],
                            'signal_candle_low': killzone_data.loc[i, 'Low'],
                            'fvg': fvg
                        }
        
        return None
    
    def calculate_stop_losses(self, entry_info: Dict, trade_type: str, 
                            sweep_extreme: float) -> Dict:
        """
        Calculate all 4 types of stop losses
        
        Args:
            entry_info: Entry signal information
            trade_type: 'short' or 'long'
            sweep_extreme: The extreme price during sweep
            
        Returns:
            Dictionary with SL1, SL2, SL3, SL4
        """
        entry_price = entry_info['entry_price']
        fvg = entry_info['fvg']
        
        if trade_type == 'short':
            # SL1: Swing Extreme + Buffer (Conservative)
            sl1 = sweep_extreme + self.SL_BUFFER
            
            # SL2: FVG Upper Border (Technical)
            sl2 = fvg['gap_high']
            
            # SL3: Signal Candle High + small buffer (Aggressive)
            sl3 = max(entry_info['signal_candle_high'], entry_price) + 0.25
            
            # SL4: Mean Threshold (Institutional) - 50% between entry and SL1
            sl4 = entry_price + (sl1 - entry_price) * 0.5
            
        else:  # long
            # SL1: Swing Extreme - Buffer (Conservative)
            sl1 = sweep_extreme - self.SL_BUFFER
            
            # SL2: FVG Lower Border (Technical)
            sl2 = fvg['gap_low']
            
            # SL3: Signal Candle Low - small buffer (Aggressive)
            sl3 = min(entry_info['signal_candle_low'], entry_price) - 0.25
            
            # SL4: Mean Threshold (Institutional) - 50% between entry and SL1
            sl4 = entry_price - (entry_price - sl1) * 0.5
        
        return {
            'SL1': sl1,
            'SL2': sl2,
            'SL3': sl3,
            'SL4': sl4
        }
    
    def calculate_take_profits(self, entry_price: float, stop_loss: float, 
                              trade_type: str, tokyo_levels: Dict) -> Dict:
        """
        Calculate all 5 types of take profits for a given stop loss
        
        Args:
            entry_price: Entry price
            stop_loss: Stop loss level
            trade_type: 'short' or 'long'
            tokyo_levels: Tokyo High, Low, EQ
            
        Returns:
            Dictionary with TP1, TP2, TP3, TP4, TP5
        """
        risk = abs(entry_price - stop_loss)
        
        if trade_type == 'short':
            tp1 = entry_price - (risk * 1.0)
            tp2 = entry_price - (risk * 1.5)
            tp3 = entry_price - (risk * 2.0)
            tp4 = tokyo_levels['Tokyo_Low']
            tp5 = tokyo_levels['Tokyo_EQ']
        else:  # long
            tp1 = entry_price + (risk * 1.0)
            tp2 = entry_price + (risk * 1.5)
            tp3 = entry_price + (risk * 2.0)
            tp4 = tokyo_levels['Tokyo_High']
            tp5 = tokyo_levels['Tokyo_EQ']
        
        return {
            'TP1': tp1,
            'TP2': tp2,
            'TP3': tp3,
            'TP4': tp4,
            'TP5': tp5
        }
    
    def simulate_trade(self, entry_info: Dict, trade_type: str, 
                      stop_loss: float, take_profit: float, 
                      start_idx: int) -> str:
        """
        Simulate a single trade with specific SL and TP
        
        Returns:
            'win' or 'loss'
        """
        # Get subsequent data after entry
        end_idx = min(start_idx + self.MAX_BARS_LOOKAHEAD, len(self.df))
        future_data = self.df.iloc[start_idx:end_idx]
        
        if len(future_data) == 0:
            return 'loss'  # Default to loss if no data
        
        # Use vectorized operations for better performance
        highs = future_data['High'].values
        lows = future_data['Low'].values
        
        for i in range(len(future_data)):
            high = highs[i]
            low = lows[i]
            
            if trade_type == 'short':
                # Check if stop loss is hit first
                if high >= stop_loss:
                    return 'loss'
                # Check if take profit is hit
                if low <= take_profit:
                    return 'win'
            else:  # long
                # Check if stop loss is hit first
                if low <= stop_loss:
                    return 'loss'
                # Check if take profit is hit
                if high >= take_profit:
                    return 'win'
        
        # If neither SL nor TP hit within lookahead period
        return 'loss'
    
    def identify_setups(self):
        """
        Identify all valid trading setups (entry signals)
        This is done once, then each setup is evaluated with all SL/TP combinations
        """
        print("\n" + "="*70)
        print("IDENTIFYING TRADING SETUPS")
        print("="*70)
        
        self.setups = []
        
        # Get unique dates for iteration
        unique_dates = sorted(self.df['Date_only'].unique())
        
        print(f"\nAnalyzing {len(unique_dates)} trading days...")
        
        # Progress counter
        processed = 0
        
        for current_date in unique_dates:
            processed += 1
            if processed % 100 == 0:
                print(f"  Processed {processed}/{len(unique_dates)} days... ({processed/len(unique_dates)*100:.1f}%)")
            
            # Get Tokyo session reference levels (from previous day)
            tokyo_levels = self.identify_tokyo_session(current_date)
            
            if tokyo_levels is None:
                continue
            
            # Get killzone data (01:00-04:00 on current date)
            killzone_data = self.df[
                (self.df['Date_only'] == current_date) &
                (self.df['Hour'] >= 1) &
                (self.df['Hour'] < 4)
            ].copy()
            
            if len(killzone_data) == 0:
                continue
            
            # Check for sweep of Tokyo levels
            sweep_info = self.check_sweep(
                killzone_data,
                tokyo_levels['Tokyo_High'],
                tokyo_levels['Tokyo_Low']
            )
            
            if sweep_info['sweep_type'] is None:
                continue
            
            # Determine trade type based on sweep
            if sweep_info['sweep_type'] == 'high':
                trade_type = 'short'
            else:
                trade_type = 'long'
            
            # Find entry signal
            entry_info = self.find_entry_signal(killzone_data, sweep_info, trade_type)
            
            if entry_info is None:
                continue
            
            # Calculate the index in the main dataframe
            entry_datetime = entry_info['entry_datetime']
            main_df_idx = self.df[self.df['DateTime'] == entry_datetime].index[0]
            
            # Store the setup
            setup = {
                'date': current_date,
                'type': trade_type,
                'entry_info': entry_info,
                'sweep_extreme': sweep_info['sweep_extreme'],
                'tokyo_levels': tokyo_levels,
                'main_df_idx': main_df_idx
            }
            
            self.setups.append(setup)
        
        print(f"\nTotal setups identified: {len(self.setups)}")
        return self.setups
    
    def run_matrix_backtest(self) -> pd.DataFrame:
        """
        Run backtest for all 20 combinations (4 SL x 5 TP)
        
        Returns:
            DataFrame with performance metrics for each combination
        """
        print("\n" + "="*70)
        print("RUNNING MATRIX BACKTEST (4 SL x 5 TP = 20 combinations)")
        print("="*70)
        
        results = []
        
        sl_types = ['SL1', 'SL2', 'SL3', 'SL4']
        tp_types = ['TP1', 'TP2', 'TP3', 'TP4', 'TP5']
        tp_labels = ['1R', '1.5R', '2R', 'Range', 'EQ']
        
        total_combinations = len(sl_types) * len(tp_types)
        processed = 0
        
        for sl_type in sl_types:
            for tp_idx, tp_type in enumerate(tp_types):
                processed += 1
                tp_label = tp_labels[tp_idx]
                
                print(f"  Processing {sl_type} + {tp_type} ({processed}/{total_combinations})...")
                
                wins = 0
                losses = 0
                total_points = 0.0
                realized_rr_list = []
                consecutive_losses = []
                current_streak = 0
                
                for setup in self.setups:
                    trade_type = setup['type']
                    entry_info = setup['entry_info']
                    entry_price = entry_info['entry_price']
                    
                    # Calculate all SL levels for this setup
                    stop_losses = self.calculate_stop_losses(
                        entry_info,
                        trade_type,
                        setup['sweep_extreme']
                    )
                    
                    # Get the specific SL for this combination
                    stop_loss = stop_losses[sl_type]
                    risk = abs(entry_price - stop_loss)
                    
                    # Calculate all TP levels for this SL
                    take_profits = self.calculate_take_profits(
                        entry_price,
                        stop_loss,
                        trade_type,
                        setup['tokyo_levels']
                    )
                    
                    # Get the specific TP for this combination
                    take_profit = take_profits[tp_type]
                    
                    # Simulate the trade
                    outcome = self.simulate_trade(
                        entry_info,
                        trade_type,
                        stop_loss,
                        take_profit,
                        setup['main_df_idx']
                    )
                    
                    if outcome == 'win':
                        wins += 1
                        current_streak = 0
                        
                        # Calculate points gained
                        if trade_type == 'short':
                            points_gained = entry_price - take_profit
                        else:
                            points_gained = take_profit - entry_price
                        
                        total_points += points_gained
                        
                        # Calculate realized RR
                        realized_rr = points_gained / risk if risk > 0 else 0
                        realized_rr_list.append(realized_rr)
                    else:
                        losses += 1
                        current_streak += 1
                        consecutive_losses.append(current_streak)
                        
                        # Calculate points lost (risk)
                        total_points -= risk
                        realized_rr_list.append(-1.0)
                
                # Calculate metrics
                total_trades = wins + losses
                winrate = (wins / total_trades * 100) if total_trades > 0 else 0
                avg_rr_realized = np.mean(realized_rr_list) if realized_rr_list else 0
                max_dd = max(consecutive_losses) if consecutive_losses else 0
                
                results.append({
                    'Type_SL': sl_type,
                    'Type_TP': tp_label,
                    'Nb_Trades': total_trades,
                    'Winrate_%': round(winrate, 2),
                    'Net_Profit_Points': round(total_points, 2),
                    'Avg_RR_Realized': round(avg_rr_realized, 2),
                    'Max_Drawdown_Points': max_dd
                })
        
        results_df = pd.DataFrame(results)
        return results_df
    
    def run_full_backtest(self):
        """Run the complete backtest process"""
        print("""
    ╔══════════════════════════════════════════════════════════════════╗
    ║        NQ (NASDAQ) MATRIX BACKTEST                               ║
    ║        4 Stop Loss Types x 5 Take Profit Types                   ║
    ║        Tokyo Session + London Killzone + FVG Strategy            ║
    ╚══════════════════════════════════════════════════════════════════╝
    """)
        
        # Load data
        self.load_data()
        
        # Identify all setups
        self.identify_setups()
        
        if len(self.setups) == 0:
            print("\nNo valid setups found!")
            return None
        
        # Run matrix backtest
        results_df = self.run_matrix_backtest()
        
        # Print results
        print("\n" + "="*70)
        print("MATRIX BACKTEST RESULTS")
        print("="*70)
        print("\nPerformance Comparison (4 SL x 5 TP = 20 combinations):\n")
        print(results_df.to_string(index=False))
        
        # Export to CSV
        output_file = 'nq_matrix_results.csv'
        results_df.to_csv(output_file, index=False)
        print(f"\n{'='*70}")
        print(f"Results exported to: {os.path.abspath(output_file)}")
        print("="*70)
        
        # Analysis and recommendation
        self.print_analysis(results_df)
        
        return results_df
    
    def print_analysis(self, results_df: pd.DataFrame):
        """Print analysis and recommendations"""
        print("\n" + "="*70)
        print("ANALYSIS AND RECOMMENDATIONS")
        print("="*70)
        
        # Filter for combinations with winrate > 40%
        profitable = results_df[results_df['Winrate_%'] >= 40.0]
        
        if len(profitable) > 0:
            print("\n1. Combinations with Win Rate >= 40%:")
            print(profitable[['Type_SL', 'Type_TP', 'Winrate_%', 'Net_Profit_Points']].to_string(index=False))
            
            # Find best by net profit among profitable
            best_profit = profitable.loc[profitable['Net_Profit_Points'].idxmax()]
            print(f"\n2. Best Combination (High Win Rate + Best Profit):")
            print(f"   {best_profit['Type_SL']} + {best_profit['Type_TP']}")
            print(f"   Win Rate: {best_profit['Winrate_%']:.2f}%")
            print(f"   Net Profit: {best_profit['Net_Profit_Points']:.2f} points")
            print(f"   Avg RR: {best_profit['Avg_RR_Realized']:.2f}")
            print(f"   Max Drawdown: {best_profit['Max_Drawdown_Points']} consecutive losses")
        else:
            print("\nNo combinations achieved Win Rate >= 40%")
            
            # Show top 5 by win rate
            top_5 = results_df.nlargest(5, 'Winrate_%')
            print("\nTop 5 combinations by Win Rate:")
            print(top_5[['Type_SL', 'Type_TP', 'Winrate_%', 'Net_Profit_Points']].to_string(index=False))
        
        # Best by profit regardless of winrate
        best_overall = results_df.loc[results_df['Net_Profit_Points'].idxmax()]
        print(f"\n3. Highest Net Profit (any win rate):")
        print(f"   {best_overall['Type_SL']} + {best_overall['Type_TP']}")
        print(f"   Win Rate: {best_overall['Winrate_%']:.2f}%")
        print(f"   Net Profit: {best_overall['Net_Profit_Points']:.2f} points")
        print(f"   Avg RR: {best_overall['Avg_RR_Realized']:.2f}")
        
        # Best by drawdown
        best_dd = results_df.loc[results_df['Max_Drawdown_Points'].idxmin()]
        print(f"\n4. Best Risk Management (Lowest Drawdown):")
        print(f"   {best_dd['Type_SL']} + {best_dd['Type_TP']}")
        print(f"   Win Rate: {best_dd['Winrate_%']:.2f}%")
        print(f"   Net Profit: {best_dd['Net_Profit_Points']:.2f} points")
        print(f"   Max Drawdown: {best_dd['Max_Drawdown_Points']} consecutive losses")
        
        print("\n" + "="*70)
        print("BACKTEST COMPLETE")
        print("="*70)


if __name__ == "__main__":
    # Set data directory - use current directory or environment variable
    data_directory = os.environ.get('NQ_DATA_DIR', os.path.dirname(os.path.abspath(__file__)))
    
    # Initialize and run backtester
    backtester = NQMatrixBacktester(data_directory)
    results = backtester.run_full_backtest()

"""
NQ (Nasdaq) Trading Strategy Backtest
======================================
This script implements a comprehensive backtest for an NQ trading strategy based on:
- Tokyo Session (19:00-23:00 previous day) reference levels
- London Killzone (01:00-04:00 current day) for trade execution
- Fair Value Gap (FVG) detection and inversion
- Multiple Take Profit targets with detailed performance metrics
"""

import pandas as pd
import numpy as np
from datetime import datetime, time, timedelta
import os
from typing import List, Dict, Tuple, Optional
import warnings

warnings.filterwarnings('ignore')


class NQBacktester:
    """Main backtesting class for NQ trading strategy"""
    
    def __init__(self, data_directory: str):
        """
        Initialize the backtester
        
        Args:
            data_directory: Path to directory containing CSV files
        """
        self.data_directory = data_directory
        self.df = None
        self.trades = []
        
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
            (self.df['Hour'] < 23)
        ]
        
        if len(tokyo_data) == 0:
            return None
        
        tokyo_high = tokyo_data['High'].max()
        tokyo_low = tokyo_data['Low'].min()
        tokyo_eq = (tokyo_high + tokyo_low) / 2
        
        return {
            'Tokyo_High': tokyo_high,
            'Tokyo_Low': tokyo_low,
            'Tokyo_EQ': tokyo_eq,
            'session_date': previous_date
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
                        'datetime': df_slice.loc[i, 'DateTime']
                    })
            elif fvg_type == 'bearish':
                # Bearish FVG: Low of candle (i) > High of candle (i-2)
                if df_slice.loc[i, 'Low'] > df_slice.loc[i-2, 'High']:
                    fvgs.append({
                        'idx': i,
                        'gap_low': df_slice.loc[i-2, 'High'],
                        'gap_high': df_slice.loc[i, 'Low'],
                        'datetime': df_slice.loc[i, 'DateTime']
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
        
        for idx, row in killzone_data.iterrows():
            # Check if high was swept
            if row['High'] > tokyo_high:
                high_swept = True
                if sweep_high_extreme is None or row['High'] > sweep_high_extreme:
                    sweep_high_extreme = row['High']
            
            # Check if low was swept
            if row['Low'] < tokyo_low:
                low_swept = True
                if sweep_low_extreme is None or row['Low'] < sweep_low_extreme:
                    sweep_low_extreme = row['Low']
        
        # Determine which sweep occurred first
        if high_swept and not low_swept:
            return {'sweep_type': 'high', 'sweep_extreme': sweep_high_extreme}
        elif low_swept and not high_swept:
            return {'sweep_type': 'low', 'sweep_extreme': sweep_low_extreme}
        elif high_swept and low_swept:
            # Find which happened first
            first_high_sweep_idx = None
            first_low_sweep_idx = None
            
            for idx, row in killzone_data.iterrows():
                if first_high_sweep_idx is None and row['High'] > tokyo_high:
                    first_high_sweep_idx = idx
                if first_low_sweep_idx is None and row['Low'] < tokyo_low:
                    first_low_sweep_idx = idx
                if first_high_sweep_idx is not None and first_low_sweep_idx is not None:
                    break
            
            if first_high_sweep_idx < first_low_sweep_idx:
                return {'sweep_type': 'high', 'sweep_extreme': sweep_high_extreme}
            else:
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
            Entry information or None
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
                            'fvg': fvg
                        }
        
        return None
    
    def simulate_trade(self, entry_info: Dict, trade_type: str, 
                       stop_loss: float, take_profits: Dict, 
                       start_idx: int) -> Dict:
        """
        Simulate a trade and determine which TP or SL is hit first
        
        Returns:
            Trade result with outcome for each TP
        """
        results = {
            'TP1_1R': None,
            'TP2_1.5R': None,
            'TP3_2R': None,
            'TP4_Tokyo_Range': None,
            'TP5_Tokyo_EQ': None
        }
        
        # Get subsequent data after entry - limit to next 1000 bars (about 3.5 days)
        end_idx = min(start_idx + 1000, len(self.df))
        future_data = self.df.iloc[start_idx:end_idx]
        
        if len(future_data) == 0:
            return results
        
        # Use vectorized operations for better performance
        highs = future_data['High'].values
        lows = future_data['Low'].values
        
        for i in range(len(future_data)):
            high = highs[i]
            low = lows[i]
            
            # Check if stop loss is hit
            if trade_type == 'short':
                if high >= stop_loss:
                    # Stop loss hit - all TPs are losses
                    for key in results:
                        if results[key] is None:
                            results[key] = 'loss'
                    return results
                
                # Check each TP
                if results['TP1_1R'] is None and low <= take_profits['TP1_1R']:
                    results['TP1_1R'] = 'win'
                if results['TP2_1.5R'] is None and low <= take_profits['TP2_1.5R']:
                    results['TP2_1.5R'] = 'win'
                if results['TP3_2R'] is None and low <= take_profits['TP3_2R']:
                    results['TP3_2R'] = 'win'
                if results['TP4_Tokyo_Range'] is None and low <= take_profits['TP4_Tokyo_Range']:
                    results['TP4_Tokyo_Range'] = 'win'
                if results['TP5_Tokyo_EQ'] is None and low <= take_profits['TP5_Tokyo_EQ']:
                    results['TP5_Tokyo_EQ'] = 'win'
            
            else:  # long
                if low <= stop_loss:
                    # Stop loss hit - all TPs are losses
                    for key in results:
                        if results[key] is None:
                            results[key] = 'loss'
                    return results
                
                # Check each TP
                if results['TP1_1R'] is None and high >= take_profits['TP1_1R']:
                    results['TP1_1R'] = 'win'
                if results['TP2_1.5R'] is None and high >= take_profits['TP2_1.5R']:
                    results['TP2_1.5R'] = 'win'
                if results['TP3_2R'] is None and high >= take_profits['TP3_2R']:
                    results['TP3_2R'] = 'win'
                if results['TP4_Tokyo_Range'] is None and high >= take_profits['TP4_Tokyo_Range']:
                    results['TP4_Tokyo_Range'] = 'win'
                if results['TP5_Tokyo_EQ'] is None and high >= take_profits['TP5_Tokyo_EQ']:
                    results['TP5_Tokyo_EQ'] = 'win'
            
            # Check if all TPs have been determined
            if all(v is not None for v in results.values()):
                return results
        
        # If we exit the loop without hitting all TPs, mark remaining as not reached
        for key in results:
            if results[key] is None:
                results[key] = 'not_reached'
        
        return results
    
    def run_backtest(self):
        """Main backtest execution logic"""
        print("\n" + "="*70)
        print("STARTING BACKTEST")
        print("="*70)
        
        if self.df is None:
            self.load_data()
        
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
                stop_loss = sweep_info['sweep_extreme']
            else:
                trade_type = 'long'
                stop_loss = sweep_info['sweep_extreme']
            
            # Find entry signal
            entry_info = self.find_entry_signal(killzone_data, sweep_info, trade_type)
            
            if entry_info is None:
                continue
            
            # Calculate risk
            entry_price = entry_info['entry_price']
            risk = abs(entry_price - stop_loss)
            
            # Calculate take profits
            if trade_type == 'short':
                take_profits = {
                    'TP1_1R': entry_price - (risk * 1.0),
                    'TP2_1.5R': entry_price - (risk * 1.5),
                    'TP3_2R': entry_price - (risk * 2.0),
                    'TP4_Tokyo_Range': tokyo_levels['Tokyo_Low'],
                    'TP5_Tokyo_EQ': tokyo_levels['Tokyo_EQ']
                }
            else:  # long
                take_profits = {
                    'TP1_1R': entry_price + (risk * 1.0),
                    'TP2_1.5R': entry_price + (risk * 1.5),
                    'TP3_2R': entry_price + (risk * 2.0),
                    'TP4_Tokyo_Range': tokyo_levels['Tokyo_High'],
                    'TP5_Tokyo_EQ': tokyo_levels['Tokyo_EQ']
                }
            
            # Get the index in the full dataframe where entry occurred
            entry_datetime = entry_info['entry_datetime']
            start_idx = self.df[self.df['DateTime'] == entry_datetime].index[0] + 1
            
            # Simulate trade
            trade_results = self.simulate_trade(
                entry_info, trade_type, stop_loss, take_profits, start_idx
            )
            
            # Store trade - rename TP keys to avoid conflict with results
            trade = {
                'date': current_date,
                'type': trade_type,
                'entry_price': entry_price,
                'stop_loss': stop_loss,
                'risk': risk,
                'tokyo_high': tokyo_levels['Tokyo_High'],
                'tokyo_low': tokyo_levels['Tokyo_Low'],
                'tokyo_eq': tokyo_levels['Tokyo_EQ'],
                'entry_datetime': entry_datetime,
                'TP1_1R_price': take_profits['TP1_1R'],
                'TP2_1.5R_price': take_profits['TP2_1.5R'],
                'TP3_2R_price': take_profits['TP3_2R'],
                'TP4_Tokyo_Range_price': take_profits['TP4_Tokyo_Range'],
                'TP5_Tokyo_EQ_price': take_profits['TP5_Tokyo_EQ'],
                **trade_results
            }
            
            self.trades.append(trade)
        
        print(f"\nTotal trades identified: {len(self.trades)}")
    
    def calculate_statistics(self) -> Dict:
        """Calculate comprehensive statistics for all TP types"""
        if not self.trades:
            return {}
        
        stats = {}
        tp_types = ['TP1_1R', 'TP2_1.5R', 'TP3_2R', 'TP4_Tokyo_Range', 'TP5_Tokyo_EQ']
        
        for tp_type in tp_types:
            wins = sum(1 for t in self.trades if t[tp_type] == 'win')
            losses = sum(1 for t in self.trades if t[tp_type] == 'loss')
            not_reached = sum(1 for t in self.trades if t[tp_type] == 'not_reached')
            total_trades = len(self.trades)
            
            # Win rate calculation (excluding not_reached)
            decided_trades = wins + losses
            win_rate = (wins / decided_trades * 100) if decided_trades > 0 else 0
            
            # Net profitability (assuming 1R risk per trade)
            if tp_type == 'TP1_1R':
                reward_ratio = 1.0
            elif tp_type == 'TP2_1.5R':
                reward_ratio = 1.5
            elif tp_type == 'TP3_2R':
                reward_ratio = 2.0
            else:
                # For Tokyo Range and EQ, calculate average reward
                rewards = []
                tp_price_key = tp_type + '_price'  # TP prices are stored with _price suffix
                for t in self.trades:
                    if t[tp_type] == 'win':
                        if t['type'] == 'short':
                            reward = (t['entry_price'] - t[tp_price_key]) / t['risk']
                        else:
                            reward = (t[tp_price_key] - t['entry_price']) / t['risk']
                        rewards.append(reward)
                reward_ratio = np.mean(rewards) if rewards else 0
            
            net_profit = wins * reward_ratio - losses * 1.0
            
            # Calculate max consecutive drawdown
            max_consecutive_losses = 0
            current_consecutive_losses = 0
            
            for t in self.trades:
                if t[tp_type] == 'loss':
                    current_consecutive_losses += 1
                    max_consecutive_losses = max(max_consecutive_losses, current_consecutive_losses)
                elif t[tp_type] == 'win':
                    current_consecutive_losses = 0
            
            # Trade distribution
            longs = sum(1 for t in self.trades if t['type'] == 'long')
            shorts = sum(1 for t in self.trades if t['type'] == 'short')
            
            stats[tp_type] = {
                'total_trades': total_trades,
                'wins': wins,
                'losses': losses,
                'not_reached': not_reached,
                'win_rate': win_rate,
                'net_profit_R': net_profit,
                'avg_reward_ratio': reward_ratio,
                'max_consecutive_losses': max_consecutive_losses,
                'longs': longs,
                'shorts': shorts
            }
        
        return stats
    
    def print_results(self):
        """Print comprehensive backtest results"""
        print("\n" + "="*70)
        print("BACKTEST RESULTS")
        print("="*70)
        
        if not self.trades:
            print("No trades were executed during the backtest period.")
            return
        
        stats = self.calculate_statistics()
        
        # Print summary table
        print("\n" + "="*70)
        print("PERFORMANCE SUMMARY BY TAKE PROFIT TYPE")
        print("="*70)
        
        # Header
        print(f"\n{'TP Type':<20} {'Trades':<10} {'Wins':<8} {'Losses':<8} {'Win%':<10} {'Net R':<12} {'Avg RR':<10} {'Max DD':<10}")
        print("-" * 106)
        
        for tp_name, tp_stats in stats.items():
            tp_label = tp_name.replace('_', ' ')
            print(f"{tp_label:<20} {tp_stats['total_trades']:<10} {tp_stats['wins']:<8} "
                  f"{tp_stats['losses']:<8} {tp_stats['win_rate']:<10.2f} "
                  f"{tp_stats['net_profit_R']:<12.2f} {tp_stats['avg_reward_ratio']:<10.2f} "
                  f"{tp_stats['max_consecutive_losses']:<10}")
        
        # Print detailed statistics for each TP
        print("\n" + "="*70)
        print("DETAILED STATISTICS BY TAKE PROFIT TYPE")
        print("="*70)
        
        for tp_name, tp_stats in stats.items():
            tp_label = tp_name.replace('_', ' ')
            print(f"\n{tp_label}:")
            print(f"  Total Trades: {tp_stats['total_trades']}")
            print(f"  Wins: {tp_stats['wins']}")
            print(f"  Losses: {tp_stats['losses']}")
            print(f"  Not Reached: {tp_stats['not_reached']}")
            print(f"  Win Rate: {tp_stats['win_rate']:.2f}%")
            print(f"  Net Profitability: {tp_stats['net_profit_R']:.2f}R")
            print(f"  Average Reward Ratio: {tp_stats['avg_reward_ratio']:.2f}")
            print(f"  Max Consecutive Losses: {tp_stats['max_consecutive_losses']}")
            print(f"  Longs: {tp_stats['longs']} ({tp_stats['longs']/tp_stats['total_trades']*100:.1f}%)")
            print(f"  Shorts: {tp_stats['shorts']} ({tp_stats['shorts']/tp_stats['total_trades']*100:.1f}%)")
        
        # Export trades to CSV
        self.export_trades()
    
    def export_trades(self):
        """Export all trades to CSV file"""
        trades_df = pd.DataFrame(self.trades)
        output_file = os.path.join(self.data_directory, 'backtest_trades.csv')
        trades_df.to_csv(output_file, index=False)
        print(f"\n" + "="*70)
        print(f"Trade details exported to: {output_file}")
        print("="*70)


def main():
    """Main execution function"""
    print("""
    ╔══════════════════════════════════════════════════════════════════╗
    ║        NQ (NASDAQ) TRADING STRATEGY BACKTEST                     ║
    ║        Tokyo Session + London Killzone + FVG Strategy            ║
    ╚══════════════════════════════════════════════════════════════════╝
    """)
    
    # Set data directory
    data_directory = '/home/runner/work/Backtest-Trading/Backtest-Trading'
    
    # Initialize backtester
    backtester = NQBacktester(data_directory)
    
    # Load data
    backtester.load_data()
    
    # Run backtest
    backtester.run_backtest()
    
    # Print results
    backtester.print_results()
    
    print("\n" + "="*70)
    print("BACKTEST COMPLETE")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()

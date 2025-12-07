"""
NQ (Nasdaq) Daily Trend Filter Backtest
========================================
This script tests lightweight daily trend filters on the London Manipulation strategy
to improve trade quality by filtering with daily timeframe structure.

Filters tested:
1. Baseline (No Filter) - All trades taken
2. Previous Day Color - Filter based on prior day's candle direction
3. Weekly Open - Filter based on current price vs weekly open

Strategy:
- Entry: Setup Inversion FVG during London Killzone (1:00-4:00 Chicago)
- Stop Loss: SL3 (Signal candle high/low + buffer)
- Take Profit: 1R (Risk = Entry - SL3)
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
from typing import List, Dict, Tuple, Optional
import warnings

warnings.filterwarnings('ignore')


class NQDailyFilterBacktester:
    """Daily trend filter backtesting class for NQ trading strategy"""
    
    # Constants
    MAX_BARS_LOOKAHEAD = 1000  # Maximum bars to check for TP/SL
    SL3_BUFFER = 0.25  # Small buffer in points for SL3 (aggressive)
    START_YEAR = 2018
    END_YEAR = 2026
    
    def __init__(self, data_directory: str):
        """
        Initialize the daily filter backtester
        
        Args:
            data_directory: Path to directory containing CSV files
        """
        self.data_directory = data_directory
        self.df_5m = None
        self.df_1d = None
        self.setups = []
        
    def load_5m_data(self) -> pd.DataFrame:
        """Load all 5-minute CSV files"""
        print("Loading 5-minute data files...")
        all_data = []
        
        for year in range(self.START_YEAR, self.END_YEAR):
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
        
        if not all_data:
            raise FileNotFoundError("No 5m data files found!")
        
        combined_df = pd.concat(all_data, ignore_index=True)
        combined_df['DateTime'] = pd.to_datetime(
            combined_df['Date'] + ' ' + combined_df['Time'],
            format='%d/%m/%Y %H:%M:%S'
        )
        
        for col in ['Open', 'High', 'Low', 'Close']:
            combined_df[col] = pd.to_numeric(combined_df[col], errors='coerce')
        
        combined_df = combined_df.sort_values('DateTime').reset_index(drop=True)
        combined_df['Date_only'] = combined_df['DateTime'].dt.date
        combined_df['Hour'] = combined_df['DateTime'].dt.hour
        combined_df['Minute'] = combined_df['DateTime'].dt.minute
        combined_df['DayOfWeek'] = combined_df['DateTime'].dt.dayofweek  # Monday=0, Sunday=6
        
        print(f"Total 5m records loaded: {len(combined_df)}")
        print(f"Date range: {combined_df['DateTime'].min()} to {combined_df['DateTime'].max()}")
        
        self.df_5m = combined_df
        return combined_df
    
    def load_1d_data(self) -> pd.DataFrame:
        """Load all 1-day (daily) CSV files"""
        print("\nLoading daily (1D) data files...")
        all_data = []
        
        for year in range(self.START_YEAR, self.END_YEAR):
            filename = f"{year} 1D.csv"
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
        
        if not all_data:
            raise FileNotFoundError("No 1D data files found!")
        
        combined_df = pd.concat(all_data, ignore_index=True)
        combined_df['DateTime'] = pd.to_datetime(
            combined_df['Date'] + ' ' + combined_df['Time'],
            format='%d/%m/%Y %H:%M:%S'
        )
        
        for col in ['Open', 'High', 'Low', 'Close']:
            combined_df[col] = pd.to_numeric(combined_df[col], errors='coerce')
        
        combined_df = combined_df.sort_values('DateTime').reset_index(drop=True)
        combined_df['Date_only'] = combined_df['DateTime'].dt.date
        
        print(f"Total 1D records loaded: {len(combined_df)}")
        
        self.df_1d = combined_df
        return combined_df
    
    def get_previous_day_color(self, current_date) -> Optional[str]:
        """
        Get the previous day's candle color (bullish/bearish)
        
        Returns:
            'bullish' if prev day closed higher than open (green candle)
            'bearish' if prev day closed lower than open (red candle)
            None if no data available
        """
        previous_date = current_date - timedelta(days=1)
        
        # Look back up to 5 days to account for weekends
        for i in range(1, 6):
            check_date = current_date - timedelta(days=i)
            prev_day_data = self.df_1d[self.df_1d['Date_only'] == check_date]
            
            if len(prev_day_data) > 0:
                prev_day = prev_day_data.iloc[0]
                if prev_day['Close'] > prev_day['Open']:
                    return 'bullish'
                elif prev_day['Close'] < prev_day['Open']:
                    return 'bearish'
                else:
                    return None  # Doji - no clear direction
        
        return None
    
    def get_weekly_open(self, target_datetime: datetime) -> Optional[float]:
        """
        Get the weekly open price (Monday 00:00 or Sunday 17:00)
        
        In futures markets, weekly open is often Sunday 17:00 (start of trading week)
        or Monday 00:00. We'll use the earliest open of the current week.
        
        Returns:
            Weekly open price or None if not found
        """
        # Get the start of the current week (Monday)
        current_date = target_datetime.date()
        days_since_monday = target_datetime.weekday()  # Monday=0
        
        # Go back to Monday 00:00 of current week
        monday_date = current_date - timedelta(days=days_since_monday)
        
        # Check Sunday evening (previous day at 17:00+)
        sunday_date = monday_date - timedelta(days=1)
        
        # Try to find Sunday 17:00+ candle
        sunday_evening = self.df_5m[
            (self.df_5m['Date_only'] == sunday_date) &
            (self.df_5m['Hour'] >= 17)
        ]
        
        if len(sunday_evening) > 0:
            return sunday_evening.iloc[0]['Open']
        
        # Fall back to Monday 00:00
        monday_morning = self.df_5m[
            (self.df_5m['Date_only'] == monday_date) &
            (self.df_5m['Hour'] == 0) &
            (self.df_5m['Minute'] == 0)
        ]
        
        if len(monday_morning) > 0:
            return monday_morning.iloc[0]['Open']
        
        # Fall back to first available price on Monday
        monday_any = self.df_5m[self.df_5m['Date_only'] == monday_date]
        
        if len(monday_any) > 0:
            return monday_any.iloc[0]['Open']
        
        return None
    
    def identify_tokyo_session(self, date) -> Optional[Dict]:
        """Identify Tokyo session for a given date"""
        previous_date = date - timedelta(days=1)
        
        tokyo_data = self.df_5m[
            (self.df_5m['Date_only'] == previous_date) &
            (self.df_5m['Hour'] >= 19) &
            (self.df_5m['Hour'] < 24)
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
        """Detect Fair Value Gaps"""
        fvgs = []
        
        if len(df_slice) < 3:
            return fvgs
        
        df_slice = df_slice.reset_index(drop=True)
        
        for i in range(2, len(df_slice)):
            if fvg_type == 'bullish':
                if df_slice.loc[i-2, 'Low'] > df_slice.loc[i, 'High']:
                    fvgs.append({
                        'idx': i,
                        'gap_low': df_slice.loc[i, 'High'],
                        'gap_high': df_slice.loc[i-2, 'Low'],
                        'datetime': df_slice.loc[i, 'DateTime']
                    })
            elif fvg_type == 'bearish':
                if df_slice.loc[i, 'Low'] > df_slice.loc[i-2, 'High']:
                    fvgs.append({
                        'idx': i,
                        'gap_low': df_slice.loc[i-2, 'High'],
                        'gap_high': df_slice.loc[i, 'Low'],
                        'datetime': df_slice.loc[i, 'DateTime']
                    })
        
        return fvgs
    
    def check_sweep(self, killzone_data: pd.DataFrame, tokyo_high: float, tokyo_low: float) -> Dict:
        """Check if price sweeps Tokyo levels"""
        high_swept = False
        low_swept = False
        sweep_high_extreme = None
        sweep_low_extreme = None
        first_high_sweep_idx = None
        first_low_sweep_idx = None
        
        for idx, row in killzone_data.iterrows():
            if row['High'] > tokyo_high:
                high_swept = True
                if sweep_high_extreme is None or row['High'] > sweep_high_extreme:
                    sweep_high_extreme = row['High']
                if first_high_sweep_idx is None:
                    first_high_sweep_idx = idx
            
            if row['Low'] < tokyo_low:
                low_swept = True
                if sweep_low_extreme is None or row['Low'] < sweep_low_extreme:
                    sweep_low_extreme = row['Low']
                if first_low_sweep_idx is None:
                    first_low_sweep_idx = idx
        
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
    
    def find_entry_signal(self, killzone_data: pd.DataFrame, sweep_info: Dict, trade_type: str) -> Optional[Dict]:
        """Find entry signal based on FVG inversion"""
        killzone_data = killzone_data.reset_index(drop=True)
        
        if trade_type == 'short':
            fvgs = self.detect_fvg(killzone_data, 'bullish')
            
            for fvg in fvgs:
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
            fvgs = self.detect_fvg(killzone_data, 'bearish')
            
            for fvg in fvgs:
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
    
    def calculate_sl3(self, entry_info: Dict, trade_type: str) -> float:
        """Calculate SL3 (Signal Candle stop loss)"""
        entry_price = entry_info['entry_price']
        
        if trade_type == 'short':
            sl3 = max(entry_info['signal_candle_high'], entry_price) + self.SL3_BUFFER
        else:
            sl3 = min(entry_info['signal_candle_low'], entry_price) - self.SL3_BUFFER
        
        return sl3
    
    def simulate_trade(self, entry_info: Dict, trade_type: str, sl3: float, start_idx: int) -> str:
        """Simulate trade with SL3 and TP at 1R"""
        entry_price = entry_info['entry_price']
        risk = abs(entry_price - sl3)
        
        if trade_type == 'short':
            tp = entry_price - risk
        else:
            tp = entry_price + risk
        
        end_idx = min(start_idx + self.MAX_BARS_LOOKAHEAD, len(self.df_5m))
        future_data = self.df_5m.iloc[start_idx:end_idx]
        
        if len(future_data) == 0:
            return 'loss'
        
        highs = future_data['High'].values
        lows = future_data['Low'].values
        
        for i in range(len(future_data)):
            if trade_type == 'short':
                if highs[i] >= sl3:
                    return 'loss'
                if lows[i] <= tp:
                    return 'win'
            else:
                if lows[i] <= sl3:
                    return 'loss'
                if highs[i] >= tp:
                    return 'win'
        
        return 'loss'
    
    def identify_all_setups(self):
        """Identify all valid trading setups without filters"""
        print("\n" + "="*70)
        print("IDENTIFYING ALL TRADING SETUPS (SL3 + 1R Strategy)")
        print("="*70)
        
        self.setups = []
        unique_dates = sorted(self.df_5m['Date_only'].unique())
        
        print(f"\nAnalyzing {len(unique_dates)} trading days...")
        processed = 0
        
        for current_date in unique_dates:
            processed += 1
            if processed % 100 == 0:
                print(f"  Processed {processed}/{len(unique_dates)} days... ({processed/len(unique_dates)*100:.1f}%)")
            
            tokyo_levels = self.identify_tokyo_session(current_date)
            if tokyo_levels is None:
                continue
            
            killzone_data = self.df_5m[
                (self.df_5m['Date_only'] == current_date) &
                (self.df_5m['Hour'] >= 1) &
                (self.df_5m['Hour'] < 4)
            ].copy()
            
            if len(killzone_data) == 0:
                continue
            
            sweep_info = self.check_sweep(killzone_data, tokyo_levels['Tokyo_High'], tokyo_levels['Tokyo_Low'])
            if sweep_info['sweep_type'] is None:
                continue
            
            trade_type = 'short' if sweep_info['sweep_type'] == 'high' else 'long'
            entry_info = self.find_entry_signal(killzone_data, sweep_info, trade_type)
            
            if entry_info is None:
                continue
            
            sl3 = self.calculate_sl3(entry_info, trade_type)
            entry_datetime = entry_info['entry_datetime']
            main_df_idx = self.df_5m[self.df_5m['DateTime'] == entry_datetime].index[0]
            
            # Get daily filters
            prev_day_color = self.get_previous_day_color(current_date)
            weekly_open = self.get_weekly_open(entry_datetime)
            
            setup = {
                'date': current_date,
                'type': trade_type,
                'entry_info': entry_info,
                'sweep_extreme': sweep_info['sweep_extreme'],
                'tokyo_levels': tokyo_levels,
                'sl3': sl3,
                'main_df_idx': main_df_idx,
                'prev_day_color': prev_day_color,
                'weekly_open': weekly_open,
                'entry_price': entry_info['entry_price'],
                'entry_datetime': entry_datetime
            }
            
            self.setups.append(setup)
        
        print(f"\nTotal setups identified: {len(self.setups)}")
        return self.setups
    
    def run_filter_comparison(self) -> pd.DataFrame:
        """Run backtest with different daily trend filters"""
        print("\n" + "="*70)
        print("RUNNING DAILY TREND FILTER COMPARISON")
        print("="*70)
        
        results = []
        
        # Case 1: Baseline - No Filter
        print("\n  Processing Case 1: Baseline (No Filter)...")
        filtered_setups_1 = self.setups
        results.append(self.calculate_metrics(filtered_setups_1, "1_Baseline_No_Filter"))
        
        # Case 2: Previous Day Color Filter
        print("  Processing Case 2: Previous Day Color Filter...")
        filtered_setups_2 = []
        for setup in self.setups:
            prev_day_color = setup['prev_day_color']
            trade_type = setup['type']
            
            # Long only if previous day was bullish (green)
            # Short only if previous day was bearish (red)
            if prev_day_color == 'bullish' and trade_type == 'long':
                filtered_setups_2.append(setup)
            elif prev_day_color == 'bearish' and trade_type == 'short':
                filtered_setups_2.append(setup)
        
        results.append(self.calculate_metrics(filtered_setups_2, "2_PrevDay_Color"))
        
        # Case 3: Weekly Open Filter
        print("  Processing Case 3: Weekly Open Filter...")
        filtered_setups_3 = []
        for setup in self.setups:
            weekly_open = setup['weekly_open']
            trade_type = setup['type']
            entry_price = setup['entry_price']
            
            if weekly_open is None:
                continue
            
            # Long only if current price > weekly open
            # Short only if current price < weekly open
            if trade_type == 'long' and entry_price > weekly_open:
                filtered_setups_3.append(setup)
            elif trade_type == 'short' and entry_price < weekly_open:
                filtered_setups_3.append(setup)
        
        results.append(self.calculate_metrics(filtered_setups_3, "3_Weekly_Open"))
        
        results_df = pd.DataFrame(results)
        return results_df
    
    def calculate_metrics(self, setups: List[Dict], filter_name: str) -> Dict:
        """Calculate performance metrics for a filtered set of setups"""
        if len(setups) == 0:
            return {
                'Filter_Name': filter_name,
                'Num_Trades': 0,
                'Winrate_%': 0.0,
                'Net_Profit_Points': 0.0,
                'Gross_Win_Points': 0.0,
                'Gross_Loss_Points': 0.0,
                'Profit_Factor': 0.0,
                'Max_Consecutive_Losses': 0,
                'Avg_Risk_Points': 0.0
            }
        
        wins = 0
        losses = 0
        gross_win = 0.0
        gross_loss = 0.0
        total_risk = 0.0
        
        for setup in setups:
            result = self.simulate_trade(
                setup['entry_info'],
                setup['type'],
                setup['sl3'],
                setup['main_df_idx']
            )
            
            entry_price = setup['entry_price']
            sl3 = setup['sl3']
            risk = abs(entry_price - sl3)
            total_risk += risk
            
            if result == 'win':
                wins += 1
                gross_win += risk  # 1R profit
            else:
                losses += 1
                gross_loss += risk  # 1R loss
        
        total_trades = wins + losses
        winrate = (wins / total_trades * 100) if total_trades > 0 else 0
        net_profit = gross_win - gross_loss
        profit_factor = (gross_win / gross_loss) if gross_loss > 0 else 0
        avg_risk = total_risk / total_trades if total_trades > 0 else 0
        
        # Calculate max consecutive losses
        consecutive_losses = []
        current_streak = 0
        
        for setup in setups:
            result = self.simulate_trade(
                setup['entry_info'],
                setup['type'],
                setup['sl3'],
                setup['main_df_idx']
            )
            
            if result == 'loss':
                current_streak += 1
            else:
                if current_streak > 0:
                    consecutive_losses.append(current_streak)
                current_streak = 0
        
        if current_streak > 0:
            consecutive_losses.append(current_streak)
        
        max_consecutive_losses = max(consecutive_losses) if consecutive_losses else 0
        
        return {
            'Filter_Name': filter_name,
            'Num_Trades': total_trades,
            'Winrate_%': round(winrate, 2),
            'Net_Profit_Points': round(net_profit, 2),
            'Gross_Win_Points': round(gross_win, 2),
            'Gross_Loss_Points': round(gross_loss, 2),
            'Profit_Factor': round(profit_factor, 2),
            'Max_Consecutive_Losses': max_consecutive_losses,
            'Avg_Risk_Points': round(avg_risk, 2)
        }
    
    def run_full_backtest(self):
        """Run the complete daily filter backtest"""
        print("""
    ╔══════════════════════════════════════════════════════════════════╗
    ║        NQ DAILY TREND FILTER BACKTEST                            ║
    ║        Testing Lightweight Daily Filters                         ║
    ╚══════════════════════════════════════════════════════════════════╝
    """)
        
        # Load data
        self.load_5m_data()
        self.load_1d_data()
        
        # Identify all setups
        self.identify_all_setups()
        
        if len(self.setups) == 0:
            print("\nNo valid setups found!")
            return None
        
        # Run filter comparison
        results_df = self.run_filter_comparison()
        
        # Print results
        print("\n" + "="*70)
        print("DAILY TREND FILTER COMPARISON RESULTS")
        print("="*70)
        print("\nPerformance Comparison Across 3 Filter Cases:\n")
        print(results_df.to_string(index=False))
        
        # Export to CSV
        output_file = 'nq_daily_filter_results.csv'
        results_df.to_csv(output_file, index=False)
        print(f"\n{'='*70}")
        print(f"Results exported to: {os.path.abspath(output_file)}")
        print("="*70)
        
        # Analysis
        self.print_analysis(results_df)
        
        return results_df
    
    def print_analysis(self, results_df: pd.DataFrame):
        """Print detailed analysis and recommendations"""
        print("\n" + "="*70)
        print("DETAILED ANALYSIS AND RECOMMENDATIONS")
        print("="*70)
        
        baseline = results_df[results_df['Filter_Name'] == '1_Baseline_No_Filter'].iloc[0]
        
        print(f"\n1. Baseline Performance (No Filter):")
        print(f"   Trades: {baseline['Num_Trades']}")
        print(f"   Win Rate: {baseline['Winrate_%']:.2f}%")
        print(f"   Net Profit: {baseline['Net_Profit_Points']:.2f} points")
        print(f"   Profit Factor: {baseline['Profit_Factor']:.2f}")
        print(f"   Max Consecutive Losses: {baseline['Max_Consecutive_Losses']}")
        print(f"   Avg Risk per Trade: {baseline['Avg_Risk_Points']:.2f} points")
        
        print(f"\n2. Filter Effectiveness Comparison:")
        print(f"\n   {'Filter':<25} {'Trades':<8} {'Change':<12} {'WR%':<8} {'Change':<12} {'PF':<6}")
        print(f"   {'-'*80}")
        
        for idx, row in results_df.iterrows():
            if row['Filter_Name'] != '1_Baseline_No_Filter':
                trade_reduction = baseline['Num_Trades'] - row['Num_Trades']
                trade_reduction_pct = (trade_reduction / baseline['Num_Trades'] * 100) if baseline['Num_Trades'] > 0 else 0
                winrate_improvement = row['Winrate_%'] - baseline['Winrate_%']
                
                print(f"   {row['Filter_Name']:<25} {row['Num_Trades']:<8} "
                      f"{trade_reduction_pct:>5.1f}% ({trade_reduction:>+3})  "
                      f"{row['Winrate_%']:>6.2f}  {winrate_improvement:>6.2f}pp     "
                      f"{row['Profit_Factor']:>5.2f}")
        
        print(f"\n3. Best Performing Filters:")
        
        # Best by winrate
        best_winrate_idx = results_df['Winrate_%'].idxmax()
        best_winrate = results_df.loc[best_winrate_idx]
        
        print(f"\n   a) Highest Win Rate: {best_winrate['Filter_Name']}")
        print(f"      Win Rate: {best_winrate['Winrate_%']:.2f}%")
        print(f"      Trades: {best_winrate['Num_Trades']}")
        print(f"      Net Profit: {best_winrate['Net_Profit_Points']:.2f} points")
        print(f"      Profit Factor: {best_winrate['Profit_Factor']:.2f}")
        print(f"      Max Consecutive Losses: {best_winrate['Max_Consecutive_Losses']}")
        
        # Best by profit factor
        best_pf_idx = results_df['Profit_Factor'].idxmax()
        best_pf = results_df.loc[best_pf_idx]
        
        if best_pf['Filter_Name'] != best_winrate['Filter_Name']:
            print(f"\n   b) Highest Profit Factor: {best_pf['Filter_Name']}")
            print(f"      Profit Factor: {best_pf['Profit_Factor']:.2f}")
            print(f"      Win Rate: {best_pf['Winrate_%']:.2f}%")
            print(f"      Trades: {best_pf['Num_Trades']}")
            print(f"      Net Profit: {best_pf['Net_Profit_Points']:.2f} points")
        
        # Best balance (trade frequency + quality)
        print(f"\n4. Trade Frequency vs Quality Analysis:")
        
        for idx, row in results_df.iterrows():
            if row['Filter_Name'] != '1_Baseline_No_Filter':
                trades_per_year = row['Num_Trades'] / 7  # Approximate years 2018-2025
                print(f"\n   {row['Filter_Name']}:")
                print(f"     • Approx {trades_per_year:.1f} trades/year")
                print(f"     • {row['Winrate_%']:.2f}% win rate")
                print(f"     • {row['Profit_Factor']:.2f} profit factor")
                
                # Assess filter restrictiveness
                retention_rate = (row['Num_Trades'] / baseline['Num_Trades'] * 100) if baseline['Num_Trades'] > 0 else 0
                if retention_rate > 80:
                    restrictiveness = "Very Light"
                elif retention_rate > 60:
                    restrictiveness = "Light"
                elif retention_rate > 40:
                    restrictiveness = "Moderate"
                elif retention_rate > 20:
                    restrictiveness = "Restrictive"
                else:
                    restrictiveness = "Very Restrictive"
                
                print(f"     • Restrictiveness: {restrictiveness} ({retention_rate:.1f}% of trades retained)")
        
        print(f"\n5. Final Recommendation:")
        
        # Find filters with good balance
        good_filters = results_df[
            (results_df['Winrate_%'] >= 60) &
            (results_df['Profit_Factor'] >= 1.5) &
            (results_df['Num_Trades'] > baseline['Num_Trades'] * 0.3)  # At least 30% of baseline trades
        ]
        
        if len(good_filters) > 0:
            # Prefer highest profit factor among good filters
            best_overall = good_filters.loc[good_filters['Profit_Factor'].idxmax()]
            print(f"   ✅ RECOMMENDED FILTER: {best_overall['Filter_Name'].upper()}")
            print(f"\n   Reasoning:")
            print(f"   • Achieves {best_overall['Winrate_%']:.2f}% win rate (target: 60-70%)")
            print(f"   • {best_overall['Profit_Factor']:.2f} profit factor (healthy edge)")
            print(f"   • {best_overall['Num_Trades']} trades (good frequency)")
            print(f"   • Max {best_overall['Max_Consecutive_Losses']} consecutive losses (manageable)")
            
            # Compare to H1 MSS reference
            print(f"\n   Comparison to H1 MSS Filter (24 trades):")
            if best_overall['Num_Trades'] > 24:
                print(f"   ✓ {best_overall['Num_Trades'] - 24} MORE trades than H1 MSS")
                print(f"   ✓ Less restrictive, better trade frequency")
            
        else:
            print(f"   ⚠️  NO FILTER FULLY MEETS TARGETS")
            print(f"   (60-70% winrate, PF>1.5, >30% trade retention)")
            print(f"\n   Best available options:")
            
            # Show top 2 by profit factor
            top_filters = results_df.nlargest(2, 'Profit_Factor')
            for idx, row in top_filters.iterrows():
                if row['Filter_Name'] != '1_Baseline_No_Filter':
                    print(f"\n   • {row['Filter_Name']}")
                    print(f"     WR: {row['Winrate_%']:.2f}%, PF: {row['Profit_Factor']:.2f}, "
                          f"Trades: {row['Num_Trades']}")
        
        print(f"\n6. Key Insights:")
        
        # Compare filters to baseline
        prev_day_filter = results_df[results_df['Filter_Name'] == '2_PrevDay_Color'].iloc[0]
        weekly_open_filter = results_df[results_df['Filter_Name'] == '3_Weekly_Open'].iloc[0]
        
        print(f"\n   Previous Day Color Filter:")
        if prev_day_filter['Num_Trades'] > 0:
            print(f"   • Retains {prev_day_filter['Num_Trades']/baseline['Num_Trades']*100:.1f}% of trades")
            print(f"   • Improves winrate by {prev_day_filter['Winrate_%'] - baseline['Winrate_%']:+.2f}pp")
            if prev_day_filter['Profit_Factor'] > baseline['Profit_Factor']:
                print(f"   • ✓ Better profit factor ({prev_day_filter['Profit_Factor']:.2f} vs {baseline['Profit_Factor']:.2f})")
            else:
                print(f"   • ✗ Lower profit factor ({prev_day_filter['Profit_Factor']:.2f} vs {baseline['Profit_Factor']:.2f})")
        
        print(f"\n   Weekly Open Filter:")
        if weekly_open_filter['Num_Trades'] > 0:
            print(f"   • Retains {weekly_open_filter['Num_Trades']/baseline['Num_Trades']*100:.1f}% of trades")
            print(f"   • Improves winrate by {weekly_open_filter['Winrate_%'] - baseline['Winrate_%']:+.2f}pp")
            if weekly_open_filter['Profit_Factor'] > baseline['Profit_Factor']:
                print(f"   • ✓ Better profit factor ({weekly_open_filter['Profit_Factor']:.2f} vs {baseline['Profit_Factor']:.2f})")
            else:
                print(f"   • ✗ Lower profit factor ({weekly_open_filter['Profit_Factor']:.2f} vs {baseline['Profit_Factor']:.2f})")
        
        print("\n" + "="*70)
        print("BACKTEST COMPLETE")
        print("="*70)


if __name__ == "__main__":
    data_directory = os.environ.get('NQ_DATA_DIR', os.path.dirname(os.path.abspath(__file__)))
    
    backtester = NQDailyFilterBacktester(data_directory)
    results = backtester.run_full_backtest()

"""
NQ (Nasdaq) Daily Bias Filter Backtest
=======================================
This script tests two new daily bias filters on the London Manipulation strategy:
1. 3Day_PD_Array (Premium/Discount)
2. Daily_Flow (Liquidity Sequence)

Both filters provide directional bias every single day, maintaining high trade volume.

Filters tested:
1. Baseline (No Filter) - All trades taken
2. 3Day_PD_Array - Price position relative to 3-day equilibrium
3. Daily_Flow - Liquidity sequence based on J-1 vs J-2 extremes
4. COMBO - Both filters must agree on bias

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


class NQBiasFilterBacktester:
    """Daily bias filter backtesting class for NQ trading strategy"""
    
    # Constants
    MAX_BARS_LOOKAHEAD = 1000  # Maximum bars to check for TP/SL
    SL3_BUFFER = 0.25  # Small buffer in points for SL3 (aggressive)
    START_YEAR = 2018
    END_YEAR = 2026
    
    # Filter quality thresholds
    MIN_WINRATE_TARGET = 60  # Minimum win rate % target
    MIN_PROFIT_FACTOR_TARGET = 1.5  # Minimum profit factor target
    MIN_TRADE_RETENTION = 0.3  # Minimum 30% of baseline trades retained
    
    def __init__(self, data_directory: str):
        """
        Initialize the bias filter backtester
        
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
    
    def get_3day_pd_array_bias(self, current_date, london_open_price: float) -> Optional[str]:
        """
        Calculate 3Day Premium/Discount Array bias
        
        Logic:
        - Get max high and min low from days J-1, J-2, J-3
        - Calculate equilibrium = (Max_High_3day + Min_Low_3day) / 2
        - At London open (01:00), check if price < equilibrium (Discount) or > equilibrium (Premium)
        - If Discount (price < EQ): LONG bias only
        - If Premium (price > EQ): SHORT bias only
        
        Args:
            current_date: The current trading day (day J)
            london_open_price: Price at London open (01:00)
        
        Returns:
            'long' if in discount zone (below EQ)
            'short' if in premium zone (above EQ)
            None if insufficient data
        """
        # Get the 3 previous days (J-1, J-2, J-3)
        lookback_days = []
        for i in range(1, 10):  # Look back up to 10 days to find 3 trading days
            check_date = current_date - timedelta(days=i)
            day_data = self.df_1d[self.df_1d['Date_only'] == check_date]
            if len(day_data) > 0:
                lookback_days.append(day_data.iloc[0])
                if len(lookback_days) == 3:
                    break
        
        if len(lookback_days) < 3:
            return None
        
        # Calculate 3-day max high and min low
        max_high_3day = max([day['High'] for day in lookback_days])
        min_low_3day = min([day['Low'] for day in lookback_days])
        
        # Calculate equilibrium
        equilibrium_3day = (max_high_3day + min_low_3day) / 2
        
        # Determine bias based on London open price position
        if london_open_price < equilibrium_3day:
            return 'long'  # Discount zone
        elif london_open_price > equilibrium_3day:
            return 'short'  # Premium zone
        else:
            return None  # Exactly at equilibrium (rare)
    
    def get_daily_flow_bias(self, current_date) -> Optional[str]:
        """
        Calculate Daily Flow (Liquidity Sequence) bias
        
        Logic:
        - Check if yesterday (J-1) broke the high of J-2: High(J-1) > High(J-2) → BULLISH (Long only)
        - Check if yesterday (J-1) broke the low of J-2: Low(J-1) < Low(J-2) → BEARISH (Short only)
        - Inside bar: If J-1 didn't break either extreme, keep previous day's bias
        
        Args:
            current_date: The current trading day (day J)
        
        Returns:
            'long' for bullish bias
            'short' for bearish bias
            None if insufficient data or ambiguous
        """
        # Get J-1 and J-2
        lookback_days = []
        for i in range(1, 10):  # Look back up to 10 days to find 2 trading days
            check_date = current_date - timedelta(days=i)
            day_data = self.df_1d[self.df_1d['Date_only'] == check_date]
            if len(day_data) > 0:
                lookback_days.append({
                    'date': check_date,
                    'high': day_data.iloc[0]['High'],
                    'low': day_data.iloc[0]['Low']
                })
                if len(lookback_days) == 2:
                    break
        
        if len(lookback_days) < 2:
            return None
        
        j_minus_1 = lookback_days[0]  # Yesterday
        j_minus_2 = lookback_days[1]  # Day before yesterday
        
        # Check if J-1 broke J-2 high (Bullish)
        if j_minus_1['high'] > j_minus_2['high']:
            return 'long'
        
        # Check if J-1 broke J-2 low (Bearish)
        if j_minus_1['low'] < j_minus_2['low']:
            return 'short'
        
        # Inside bar case - need to look at previous bias
        # For simplicity, we'll look further back to find the last break
        for i in range(2, len(lookback_days) + 5):
            check_date = current_date - timedelta(days=i)
            day_data = self.df_1d[self.df_1d['Date_only'] == check_date]
            if len(day_data) > 0:
                day_info = {
                    'high': day_data.iloc[0]['High'],
                    'low': day_data.iloc[0]['Low']
                }
                
                # Check if this day broke the previous day's extremes
                if len(lookback_days) > i - 1:
                    prev_day = lookback_days[min(i - 1, len(lookback_days) - 1)]
                    if day_info['high'] > prev_day['high']:
                        return 'long'
                    if day_info['low'] < prev_day['low']:
                        return 'short'
        
        # If we can't determine, return None
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
        """Identify all valid trading setups with bias filter values"""
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
            
            # Get London open price (01:00) for 3Day_PD_Array calculation
            london_open_data = killzone_data[
                (killzone_data['Hour'] == 1) &
                (killzone_data['Minute'] == 0)
            ]
            
            london_open_price = None
            if len(london_open_data) > 0:
                london_open_price = london_open_data.iloc[0]['Open']
            else:
                # Fallback to first available price in killzone
                london_open_price = killzone_data.iloc[0]['Open']
            
            # Calculate bias filters
            pd_array_bias = self.get_3day_pd_array_bias(current_date, london_open_price)
            daily_flow_bias = self.get_daily_flow_bias(current_date)
            
            setup = {
                'date': current_date,
                'type': trade_type,
                'entry_info': entry_info,
                'sweep_extreme': sweep_info['sweep_extreme'],
                'tokyo_levels': tokyo_levels,
                'sl3': sl3,
                'main_df_idx': main_df_idx,
                'entry_price': entry_info['entry_price'],
                'entry_datetime': entry_datetime,
                'london_open_price': london_open_price,
                '3day_pd_array_bias': pd_array_bias,
                'daily_flow_bias': daily_flow_bias
            }
            
            self.setups.append(setup)
        
        print(f"\nTotal setups identified: {len(self.setups)}")
        return self.setups
    
    def run_filter_comparison(self) -> pd.DataFrame:
        """Run backtest with different daily bias filters"""
        print("\n" + "="*70)
        print("RUNNING DAILY BIAS FILTER COMPARISON")
        print("="*70)
        
        results = []
        
        # Case 1: Baseline - No Filter
        print("\n  Processing Case 1: Baseline (No Filter)...")
        filtered_setups_1 = self.setups
        results.append(self.calculate_metrics(filtered_setups_1, "1_Baseline_No_Filter"))
        
        # Case 2: 3Day_PD_Array Filter
        print("  Processing Case 2: 3Day_PD_Array (Premium/Discount)...")
        filtered_setups_2 = []
        for setup in self.setups:
            pd_bias = setup['3day_pd_array_bias']
            trade_type = setup['type']
            
            # Only take trade if bias agrees with setup direction
            if pd_bias == trade_type:
                filtered_setups_2.append(setup)
        
        results.append(self.calculate_metrics(filtered_setups_2, "2_3Day_PD_Array"))
        
        # Case 3: Daily_Flow Filter
        print("  Processing Case 3: Daily_Flow (Liquidity Sequence)...")
        filtered_setups_3 = []
        for setup in self.setups:
            flow_bias = setup['daily_flow_bias']
            trade_type = setup['type']
            
            # Only take trade if bias agrees with setup direction
            if flow_bias == trade_type:
                filtered_setups_3.append(setup)
        
        results.append(self.calculate_metrics(filtered_setups_3, "3_Daily_Flow"))
        
        # Case 4: COMBO - Both filters must agree
        print("  Processing Case 4: COMBO (Both filters agree)...")
        filtered_setups_4 = []
        for setup in self.setups:
            pd_bias = setup['3day_pd_array_bias']
            flow_bias = setup['daily_flow_bias']
            trade_type = setup['type']
            
            # Both filters must agree with setup direction
            if pd_bias == trade_type and flow_bias == trade_type:
                filtered_setups_4.append(setup)
        
        results.append(self.calculate_metrics(filtered_setups_4, "4_COMBO_Both_Agree"))
        
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
        """Run the complete bias filter backtest"""
        print("""
    ╔══════════════════════════════════════════════════════════════════╗
    ║        NQ DAILY BIAS FILTER BACKTEST                             ║
    ║        Testing 3Day_PD_Array & Daily_Flow Filters                ║
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
        print("DAILY BIAS FILTER COMPARISON RESULTS")
        print("="*70)
        print("\nPerformance Comparison Across 4 Filter Cases:\n")
        print(results_df.to_string(index=False))
        
        # Export to CSV
        output_file = 'nq_bias_filter_results.csv'
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
        
        print(f"\n2. NEW BIAS FILTERS PERFORMANCE:")
        print(f"\n   {'Filter':<25} {'Trades':<8} {'Retention':<12} {'WR%':<8} {'Change':<12} {'PF':<8} {'Net Pts':<10}")
        print(f"   {'-'*95}")
        
        for idx, row in results_df.iterrows():
            if row['Filter_Name'] != '1_Baseline_No_Filter':
                retention_pct = (row['Num_Trades'] / baseline['Num_Trades'] * 100) if baseline['Num_Trades'] > 0 else 0
                winrate_improvement = row['Winrate_%'] - baseline['Winrate_%']
                
                print(f"   {row['Filter_Name']:<25} {row['Num_Trades']:<8} "
                      f"{retention_pct:>6.1f}%      "
                      f"{row['Winrate_%']:>6.2f}  {winrate_improvement:>6.2f}pp     "
                      f"{row['Profit_Factor']:>5.2f}   {row['Net_Profit_Points']:>8.2f}")
        
        print(f"\n3. Filter Behavior Analysis:")
        
        # Analyze 3Day_PD_Array
        pd_array_filter = results_df[results_df['Filter_Name'] == '2_3Day_PD_Array'].iloc[0]
        print(f"\n   a) 3Day_PD_Array (Premium/Discount Zone):")
        print(f"      • Logic: Takes LONG in discount zone (price < 3-day EQ), SHORT in premium zone")
        print(f"      • Trades: {pd_array_filter['Num_Trades']} ({pd_array_filter['Num_Trades']/baseline['Num_Trades']*100:.1f}% retention)")
        print(f"      • Win Rate: {pd_array_filter['Winrate_%']:.2f}% (Change: {pd_array_filter['Winrate_%'] - baseline['Winrate_%']:+.2f}pp)")
        print(f"      • Profit Factor: {pd_array_filter['Profit_Factor']:.2f}")
        print(f"      • Net Profit: {pd_array_filter['Net_Profit_Points']:.2f} points")
        print(f"      • Max Consecutive Losses: {pd_array_filter['Max_Consecutive_Losses']}")
        
        if pd_array_filter['Winrate_%'] > baseline['Winrate_%']:
            print(f"      ✓ IMPROVES win rate by filtering against premium/discount zones")
        else:
            print(f"      ✗ Does NOT improve win rate - may need refinement")
        
        if pd_array_filter['Num_Trades'] > baseline['Num_Trades'] * 0.5:
            print(f"      ✓ MAINTAINS good trade frequency (50%+ retention)")
        else:
            print(f"      ⚠ Reduces trade frequency significantly")
        
        # Analyze Daily_Flow
        daily_flow_filter = results_df[results_df['Filter_Name'] == '3_Daily_Flow'].iloc[0]
        print(f"\n   b) Daily_Flow (Liquidity Sequence):")
        print(f"      • Logic: Follows liquidity breaks - bullish if J-1 breaks J-2 high, bearish if breaks J-2 low")
        print(f"      • Trades: {daily_flow_filter['Num_Trades']} ({daily_flow_filter['Num_Trades']/baseline['Num_Trades']*100:.1f}% retention)")
        print(f"      • Win Rate: {daily_flow_filter['Winrate_%']:.2f}% (Change: {daily_flow_filter['Winrate_%'] - baseline['Winrate_%']:+.2f}pp)")
        print(f"      • Profit Factor: {daily_flow_filter['Profit_Factor']:.2f}")
        print(f"      • Net Profit: {daily_flow_filter['Net_Profit_Points']:.2f} points")
        print(f"      • Max Consecutive Losses: {daily_flow_filter['Max_Consecutive_Losses']}")
        
        if daily_flow_filter['Winrate_%'] > baseline['Winrate_%']:
            print(f"      ✓ IMPROVES win rate by following liquidity continuation")
        else:
            print(f"      ✗ Does NOT improve win rate - may need refinement")
        
        if daily_flow_filter['Num_Trades'] > baseline['Num_Trades'] * 0.5:
            print(f"      ✓ MAINTAINS good trade frequency (50%+ retention)")
        else:
            print(f"      ⚠ Reduces trade frequency significantly")
        
        # Analyze COMBO
        combo_filter = results_df[results_df['Filter_Name'] == '4_COMBO_Both_Agree'].iloc[0]
        print(f"\n   c) COMBO (Both Filters Must Agree):")
        print(f"      • Logic: Takes trade ONLY when BOTH filters agree on bias direction")
        print(f"      • Trades: {combo_filter['Num_Trades']} ({combo_filter['Num_Trades']/baseline['Num_Trades']*100:.1f}% retention)")
        print(f"      • Win Rate: {combo_filter['Winrate_%']:.2f}% (Change: {combo_filter['Winrate_%'] - baseline['Winrate_%']:+.2f}pp)")
        print(f"      • Profit Factor: {combo_filter['Profit_Factor']:.2f}")
        print(f"      • Net Profit: {combo_filter['Net_Profit_Points']:.2f} points")
        print(f"      • Max Consecutive Losses: {combo_filter['Max_Consecutive_Losses']}")
        
        if combo_filter['Winrate_%'] > baseline['Winrate_%']:
            print(f"      ✓ IMPROVES win rate - confluence provides stronger confirmation")
        else:
            print(f"      ✗ Does NOT improve win rate despite confluence")
        
        if combo_filter['Num_Trades'] > baseline['Num_Trades'] * 0.3:
            print(f"      ✓ MAINTAINS reasonable trade frequency (30%+ retention)")
        else:
            print(f"      ⚠ Very restrictive - may be too selective")
        
        print(f"\n4. Best Performing Filter:")
        
        # Find best by profit factor (excluding baseline)
        filtered_results = results_df[results_df['Filter_Name'] != '1_Baseline_No_Filter']
        if len(filtered_results) > 0:
            best_pf_idx = filtered_results['Profit_Factor'].idxmax()
            best_pf = filtered_results.loc[best_pf_idx]
            
            print(f"\n   WINNER: {best_pf['Filter_Name'].upper()}")
            print(f"   ├─ Win Rate: {best_pf['Winrate_%']:.2f}%")
            print(f"   ├─ Profit Factor: {best_pf['Profit_Factor']:.2f}")
            print(f"   ├─ Net Profit: {best_pf['Net_Profit_Points']:.2f} points")
            print(f"   ├─ Trades: {best_pf['Num_Trades']}")
            print(f"   └─ Max Consecutive Losses: {best_pf['Max_Consecutive_Losses']}")
            
            years_span = self.END_YEAR - self.START_YEAR
            trades_per_year = best_pf['Num_Trades'] / years_span
            print(f"\n   Trade Frequency: ~{trades_per_year:.1f} trades/year")
        
        print(f"\n5. Comparative Summary:")
        print(f"\n   Filter Quality Matrix:")
        print(f"   {'Filter':<25} {'Trade Freq':<15} {'Quality':<15} {'Verdict':<20}")
        print(f"   {'-'*75}")
        
        for idx, row in results_df.iterrows():
            if row['Filter_Name'] != '1_Baseline_No_Filter':
                retention = row['Num_Trades'] / baseline['Num_Trades'] if baseline['Num_Trades'] > 0 else 0
                
                # Assess trade frequency
                if retention > 0.6:
                    freq_rating = "High"
                elif retention > 0.4:
                    freq_rating = "Medium"
                elif retention > 0.2:
                    freq_rating = "Low"
                else:
                    freq_rating = "Very Low"
                
                # Assess quality
                if row['Profit_Factor'] >= 1.5 and row['Winrate_%'] >= 60:
                    quality_rating = "Excellent"
                elif row['Profit_Factor'] >= 1.3 and row['Winrate_%'] >= 55:
                    quality_rating = "Good"
                elif row['Profit_Factor'] >= 1.1:
                    quality_rating = "Fair"
                else:
                    quality_rating = "Poor"
                
                # Overall verdict
                if row['Profit_Factor'] > baseline['Profit_Factor'] and retention > 0.3:
                    verdict = "✓ Recommended"
                elif row['Profit_Factor'] > baseline['Profit_Factor']:
                    verdict = "⚠ Good but restrictive"
                else:
                    verdict = "✗ Not recommended"
                
                print(f"   {row['Filter_Name']:<25} {freq_rating:<15} {quality_rating:<15} {verdict:<20}")
        
        print(f"\n6. Final Recommendation:")
        
        # Find filter that meets targets
        good_filters = results_df[
            (results_df['Filter_Name'] != '1_Baseline_No_Filter') &
            (results_df['Winrate_%'] >= self.MIN_WINRATE_TARGET) &
            (results_df['Profit_Factor'] >= self.MIN_PROFIT_FACTOR_TARGET) &
            (results_df['Num_Trades'] >= baseline['Num_Trades'] * self.MIN_TRADE_RETENTION)
        ]
        
        if len(good_filters) > 0:
            best_overall = good_filters.loc[good_filters['Profit_Factor'].idxmax()]
            print(f"   ✅ RECOMMENDED: {best_overall['Filter_Name'].upper()}")
            print(f"\n   This filter achieves the best balance of:")
            print(f"   • {best_overall['Winrate_%']:.2f}% win rate (Target: 60%+)")
            print(f"   • {best_overall['Profit_Factor']:.2f} profit factor (Target: 1.5+)")
            print(f"   • {best_overall['Num_Trades']} trades (Maintains frequency)")
            print(f"   • {best_overall['Max_Consecutive_Losses']} max consecutive losses (Manageable drawdown)")
            
            improvement_wr = best_overall['Winrate_%'] - baseline['Winrate_%']
            improvement_pf = best_overall['Profit_Factor'] - baseline['Profit_Factor']
            print(f"\n   Improvements over baseline:")
            print(f"   • Win Rate: {improvement_wr:+.2f} percentage points")
            print(f"   • Profit Factor: {improvement_pf:+.2f}")
            
        else:
            print(f"   ⚠️  NO FILTER FULLY MEETS ALL TARGETS")
            print(f"      (WR≥60%, PF≥1.5, Trades≥{baseline['Num_Trades']*self.MIN_TRADE_RETENTION:.0f})")
            print(f"\n   Best available option by Profit Factor:")
            
            if len(filtered_results) > 0:
                best_available = filtered_results.loc[filtered_results['Profit_Factor'].idxmax()]
                print(f"   • {best_available['Filter_Name']}")
                print(f"     WR: {best_available['Winrate_%']:.2f}%, PF: {best_available['Profit_Factor']:.2f}, "
                      f"Trades: {best_available['Num_Trades']}")
                
                if best_available['Winrate_%'] < self.MIN_WINRATE_TARGET:
                    print(f"     ⚠ Win rate below target ({self.MIN_WINRATE_TARGET}%)")
                if best_available['Profit_Factor'] < self.MIN_PROFIT_FACTOR_TARGET:
                    print(f"     ⚠ Profit factor below target ({self.MIN_PROFIT_FACTOR_TARGET})")
                if best_available['Num_Trades'] < baseline['Num_Trades'] * self.MIN_TRADE_RETENTION:
                    print(f"     ⚠ Trade count below minimum retention")
        
        print(f"\n7. Key Insights:")
        print(f"\n   3Day_PD_Array Filter:")
        if pd_array_filter['Num_Trades'] > 0:
            print(f"   • Filters setups based on price position in 3-day range")
            print(f"   • {'Improves' if pd_array_filter['Profit_Factor'] > baseline['Profit_Factor'] else 'Does not improve'} overall profitability")
            print(f"   • Retains {pd_array_filter['Num_Trades']/baseline['Num_Trades']*100:.1f}% of baseline trades")
            if pd_array_filter['Winrate_%'] > baseline['Winrate_%'] + 5:
                print(f"   • ✓ Significantly improves win rate (+{pd_array_filter['Winrate_%'] - baseline['Winrate_%']:.2f}pp)")
        
        print(f"\n   Daily_Flow Filter:")
        if daily_flow_filter['Num_Trades'] > 0:
            print(f"   • Follows liquidity continuation principle")
            print(f"   • {'Improves' if daily_flow_filter['Profit_Factor'] > baseline['Profit_Factor'] else 'Does not improve'} overall profitability")
            print(f"   • Retains {daily_flow_filter['Num_Trades']/baseline['Num_Trades']*100:.1f}% of baseline trades")
            if daily_flow_filter['Winrate_%'] > baseline['Winrate_%'] + 5:
                print(f"   • ✓ Significantly improves win rate (+{daily_flow_filter['Winrate_%'] - baseline['Winrate_%']:.2f}pp)")
        
        print(f"\n   COMBO Filter:")
        if combo_filter['Num_Trades'] > 0:
            print(f"   • Requires confluence of both filters")
            print(f"   • {'Improves' if combo_filter['Profit_Factor'] > baseline['Profit_Factor'] else 'Does not improve'} overall profitability")
            print(f"   • Retains {combo_filter['Num_Trades']/baseline['Num_Trades']*100:.1f}% of baseline trades")
            if combo_filter['Winrate_%'] > baseline['Winrate_%'] + 5:
                print(f"   • ✓ Significantly improves win rate (+{combo_filter['Winrate_%'] - baseline['Winrate_%']:.2f}pp)")
            if combo_filter['Num_Trades'] < baseline['Num_Trades'] * 0.3:
                print(f"   • ⚠ Very selective - may miss opportunities")
        
        print("\n" + "="*70)
        print("BACKTEST COMPLETE")
        print("="*70)


if __name__ == "__main__":
    data_directory = os.environ.get('NQ_DATA_DIR', os.path.dirname(os.path.abspath(__file__)))
    
    backtester = NQBiasFilterBacktester(data_directory)
    results = backtester.run_full_backtest()

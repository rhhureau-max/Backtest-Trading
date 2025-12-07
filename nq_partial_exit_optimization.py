"""
NQ (Nasdaq) Partial Exit Position Management Optimization
==========================================================
This script tests dynamic position management strategies with partial exits
to optimize the SL3 + 1R baseline strategy.

Compares 3 scenarios:
- Scenario A: Full exit at 1R (baseline)
- Scenario B: 50% exit at 1R, 50% runner to 2R with SL at breakeven
- Scenario C: 50% exit at 1R, 50% runner to Tokyo EQ with SL at breakeven
"""

import pandas as pd
import numpy as np
from datetime import timedelta
import os
from typing import List, Dict, Tuple, Optional
import warnings

warnings.filterwarnings('ignore')


class NQPartialExitOptimizer:
    """Position management optimizer for NQ trading strategy"""
    
    # Constants
    MAX_BARS_LOOKAHEAD = 1000  # Maximum bars to check for TP/SL (about 3.5 days on 5m data)
    SL_BUFFER = 2.0  # Buffer in points for SL1
    SL3_BUFFER = 0.25  # Small buffer in points for SL3 (aggressive)
    START_YEAR = 2018  # First year of data to load
    END_YEAR = 2026  # Last year to attempt loading (exclusive)
    
    def __init__(self, data_directory: str):
        """
        Initialize the optimizer
        
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
            List of FVG dictionaries
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
            Dictionary with sweep_type and sweep_extreme
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
    
    def calculate_sl3(self, entry_info: Dict, trade_type: str, sweep_extreme: float) -> float:
        """
        Calculate SL3 (Signal Candle stop loss)
        
        Args:
            entry_info: Entry signal information
            trade_type: 'short' or 'long'
            sweep_extreme: The extreme price during sweep
            
        Returns:
            SL3 price level
        """
        entry_price = entry_info['entry_price']
        
        if trade_type == 'short':
            # SL3: Signal Candle High + small buffer (Aggressive)
            sl3 = max(entry_info['signal_candle_high'], entry_price) + self.SL3_BUFFER
        else:  # long
            # SL3: Signal Candle Low - small buffer (Aggressive)
            sl3 = min(entry_info['signal_candle_low'], entry_price) - self.SL3_BUFFER
        
        return sl3
    
    def simulate_scenario_a(self, setup: Dict) -> Dict:
        """
        Scenario A: Full exit at 1R (baseline)
        
        Returns:
            Dictionary with trade results
        """
        trade_type = setup['type']
        entry_info = setup['entry_info']
        entry_price = entry_info['entry_price']
        sl3 = setup['sl3']
        
        risk = abs(entry_price - sl3)
        
        if trade_type == 'short':
            tp1 = entry_price - risk
        else:
            tp1 = entry_price + risk
        
        # Simulate the trade
        start_idx = setup['main_df_idx']
        end_idx = min(start_idx + self.MAX_BARS_LOOKAHEAD, len(self.df))
        future_data = self.df.iloc[start_idx:end_idx]
        
        if len(future_data) == 0:
            return {'result': 'loss', 'r_gained': -1.0, 'points': -risk}
        
        highs = future_data['High'].values
        lows = future_data['Low'].values
        
        for i in range(len(future_data)):
            high = highs[i]
            low = lows[i]
            
            if trade_type == 'short':
                # Check SL first
                if high >= sl3:
                    return {'result': 'loss', 'r_gained': -1.0, 'points': -risk}
                # Check TP
                if low <= tp1:
                    return {'result': 'win', 'r_gained': 1.0, 'points': risk}
            else:  # long
                # Check SL first
                if low <= sl3:
                    return {'result': 'loss', 'r_gained': -1.0, 'points': -risk}
                # Check TP
                if high >= tp1:
                    return {'result': 'win', 'r_gained': 1.0, 'points': risk}
        
        # Neither hit
        return {'result': 'loss', 'r_gained': -1.0, 'points': -risk}
    
    def simulate_scenario_b(self, setup: Dict) -> Dict:
        """
        Scenario B: 50% exit at 1R, 50% runner to 2R with SL at breakeven
        
        Returns:
            Dictionary with trade results
        """
        trade_type = setup['type']
        entry_info = setup['entry_info']
        entry_price = entry_info['entry_price']
        sl3 = setup['sl3']
        
        risk = abs(entry_price - sl3)
        
        if trade_type == 'short':
            tp1 = entry_price - risk
            tp2 = entry_price - (risk * 2)
        else:
            tp1 = entry_price + risk
            tp2 = entry_price + (risk * 2)
        
        # Simulate the trade
        start_idx = setup['main_df_idx']
        end_idx = min(start_idx + self.MAX_BARS_LOOKAHEAD, len(self.df))
        future_data = self.df.iloc[start_idx:end_idx]
        
        if len(future_data) == 0:
            return {'result': 'loss', 'r_gained': -1.0, 'points': -risk, 'tp1_hit': False, 'runner_success': False}
        
        highs = future_data['High'].values
        lows = future_data['Low'].values
        
        tp1_hit = False
        
        for i in range(len(future_data)):
            high = highs[i]
            low = lows[i]
            
            if not tp1_hit:
                # Phase 1: Before TP1
                if trade_type == 'short':
                    # Check SL first
                    if high >= sl3:
                        return {'result': 'loss', 'r_gained': -1.0, 'points': -risk, 'tp1_hit': False, 'runner_success': False}
                    # Check TP1
                    if low <= tp1:
                        tp1_hit = True
                        # 50% closed at 1R, continue with remaining 50%
                else:  # long
                    # Check SL first
                    if low <= sl3:
                        return {'result': 'loss', 'r_gained': -1.0, 'points': -risk, 'tp1_hit': False, 'runner_success': False}
                    # Check TP1
                    if high >= tp1:
                        tp1_hit = True
                        # 50% closed at 1R, continue with remaining 50%
            else:
                # Phase 2: After TP1, SL moved to breakeven
                if trade_type == 'short':
                    # Check breakeven first
                    if high >= entry_price:
                        # Runner stopped at breakeven
                        return {'result': 'partial_win', 'r_gained': 0.5, 'points': risk * 0.5, 'tp1_hit': True, 'runner_success': False}
                    # Check TP2
                    if low <= tp2:
                        # Runner hits TP2
                        return {'result': 'full_win', 'r_gained': 1.5, 'points': risk * 1.5, 'tp1_hit': True, 'runner_success': True}
                else:  # long
                    # Check breakeven first
                    if low <= entry_price:
                        # Runner stopped at breakeven
                        return {'result': 'partial_win', 'r_gained': 0.5, 'points': risk * 0.5, 'tp1_hit': True, 'runner_success': False}
                    # Check TP2
                    if high >= tp2:
                        # Runner hits TP2
                        return {'result': 'full_win', 'r_gained': 1.5, 'points': risk * 1.5, 'tp1_hit': True, 'runner_success': True}
        
        # If TP1 was hit but neither BE nor TP2 hit in lookahead
        if tp1_hit:
            return {'result': 'partial_win', 'r_gained': 0.5, 'points': risk * 0.5, 'tp1_hit': True, 'runner_success': False}
        else:
            return {'result': 'loss', 'r_gained': -1.0, 'points': -risk, 'tp1_hit': False, 'runner_success': False}
    
    def simulate_scenario_c(self, setup: Dict) -> Dict:
        """
        Scenario C: 50% exit at 1R, 50% runner to Tokyo EQ with SL at breakeven
        
        Returns:
            Dictionary with trade results
        """
        trade_type = setup['type']
        entry_info = setup['entry_info']
        entry_price = entry_info['entry_price']
        sl3 = setup['sl3']
        tokyo_eq = setup['tokyo_levels']['Tokyo_EQ']
        
        risk = abs(entry_price - sl3)
        
        if trade_type == 'short':
            tp1 = entry_price - risk
            tp2 = tokyo_eq
            
            # Check if Tokyo EQ is closer than 1R (inconsistent scenario)
            if tokyo_eq >= tp1:
                # Tokyo EQ is above TP1 or equal, treat as Scenario A
                return self.simulate_scenario_a(setup)
        else:
            tp1 = entry_price + risk
            tp2 = tokyo_eq
            
            # Check if Tokyo EQ is closer than 1R (inconsistent scenario)
            if tokyo_eq <= tp1:
                # Tokyo EQ is below TP1 or equal, treat as Scenario A
                return self.simulate_scenario_a(setup)
        
        # Simulate the trade
        start_idx = setup['main_df_idx']
        end_idx = min(start_idx + self.MAX_BARS_LOOKAHEAD, len(self.df))
        future_data = self.df.iloc[start_idx:end_idx]
        
        if len(future_data) == 0:
            return {'result': 'loss', 'r_gained': -1.0, 'points': -risk, 'tp1_hit': False, 'runner_success': False}
        
        highs = future_data['High'].values
        lows = future_data['Low'].values
        
        tp1_hit = False
        
        for i in range(len(future_data)):
            high = highs[i]
            low = lows[i]
            
            if not tp1_hit:
                # Phase 1: Before TP1
                if trade_type == 'short':
                    # Check SL first
                    if high >= sl3:
                        return {'result': 'loss', 'r_gained': -1.0, 'points': -risk, 'tp1_hit': False, 'runner_success': False}
                    # Check TP1
                    if low <= tp1:
                        tp1_hit = True
                        # 50% closed at 1R, continue with remaining 50%
                else:  # long
                    # Check SL first
                    if low <= sl3:
                        return {'result': 'loss', 'r_gained': -1.0, 'points': -risk, 'tp1_hit': False, 'runner_success': False}
                    # Check TP1
                    if high >= tp1:
                        tp1_hit = True
                        # 50% closed at 1R, continue with remaining 50%
            else:
                # Phase 2: After TP1, SL moved to breakeven
                if trade_type == 'short':
                    # Check breakeven first
                    if high >= entry_price:
                        # Runner stopped at breakeven
                        return {'result': 'partial_win', 'r_gained': 0.5, 'points': risk * 0.5, 'tp1_hit': True, 'runner_success': False}
                    # Check TP2 (Tokyo EQ)
                    if low <= tp2:
                        # Runner hits Tokyo EQ
                        points_gained = entry_price - tp2
                        r_gained = 0.5 * 1.0 + 0.5 * (points_gained / risk)
                        return {'result': 'full_win', 'r_gained': r_gained, 'points': risk * 0.5 + points_gained * 0.5, 'tp1_hit': True, 'runner_success': True}
                else:  # long
                    # Check breakeven first
                    if low <= entry_price:
                        # Runner stopped at breakeven
                        return {'result': 'partial_win', 'r_gained': 0.5, 'points': risk * 0.5, 'tp1_hit': True, 'runner_success': False}
                    # Check TP2 (Tokyo EQ)
                    if high >= tp2:
                        # Runner hits Tokyo EQ
                        points_gained = tp2 - entry_price
                        r_gained = 0.5 * 1.0 + 0.5 * (points_gained / risk)
                        return {'result': 'full_win', 'r_gained': r_gained, 'points': risk * 0.5 + points_gained * 0.5, 'tp1_hit': True, 'runner_success': True}
        
        # If TP1 was hit but neither BE nor TP2 hit in lookahead
        if tp1_hit:
            return {'result': 'partial_win', 'r_gained': 0.5, 'points': risk * 0.5, 'tp1_hit': True, 'runner_success': False}
        else:
            return {'result': 'loss', 'r_gained': -1.0, 'points': -risk, 'tp1_hit': False, 'runner_success': False}
    
    def identify_setups(self):
        """
        Identify all valid trading setups using SL3
        """
        print("\n" + "="*70)
        print("IDENTIFYING TRADING SETUPS (SL3 Strategy)")
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
            
            # Calculate SL3
            sl3 = self.calculate_sl3(entry_info, trade_type, sweep_info['sweep_extreme'])
            
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
                'sl3': sl3,
                'main_df_idx': main_df_idx
            }
            
            self.setups.append(setup)
        
        print(f"\nTotal setups identified: {len(self.setups)}")
        return self.setups
    
    def run_optimization(self) -> pd.DataFrame:
        """
        Run all 3 scenarios and compare results
        
        Returns:
            DataFrame with comparative metrics
        """
        print("\n" + "="*70)
        print("RUNNING POSITION MANAGEMENT OPTIMIZATION")
        print("="*70)
        
        results_a = []
        results_b = []
        results_c = []
        
        print("\nProcessing all setups across 3 scenarios...")
        
        for i, setup in enumerate(self.setups):
            if (i + 1) % 100 == 0:
                print(f"  Processed {i + 1}/{len(self.setups)} setups...")
            
            # Simulate each scenario
            result_a = self.simulate_scenario_a(setup)
            result_b = self.simulate_scenario_b(setup)
            result_c = self.simulate_scenario_c(setup)
            
            results_a.append(result_a)
            results_b.append(result_b)
            results_c.append(result_c)
        
        # Calculate metrics for each scenario
        metrics = []
        
        # Scenario A metrics
        wins_a = sum(1 for r in results_a if r['result'] == 'win')
        total_r_a = sum(r['r_gained'] for r in results_a)
        total_points_a = sum(r['points'] for r in results_a)
        winrate_a = (wins_a / len(results_a) * 100) if results_a else 0
        avg_r_a = total_r_a / len(results_a) if results_a else 0
        
        # Calculate max drawdown for Scenario A
        dd_a = []
        streak = 0
        for r in results_a:
            if r['result'] == 'loss':
                streak += 1
            else:
                dd_a.append(streak)
                streak = 0
        max_dd_a = max(dd_a) if dd_a else 0
        
        metrics.append({
            'Scenario': 'A (Full Exit 1R)',
            'Total_Net_Points': round(total_points_a, 2),
            'Winrate_Global_%': round(winrate_a, 2),
            'Runner_Success_%': 'N/A',
            'Avg_R_Per_Trade': round(avg_r_a, 2),
            'Max_Drawdown_Points': max_dd_a
        })
        
        # Scenario B metrics
        wins_b = sum(1 for r in results_b if r['result'] in ['partial_win', 'full_win'])
        runner_hits_b = sum(1 for r in results_b if r.get('runner_success', False))
        tp1_hits_b = sum(1 for r in results_b if r.get('tp1_hit', False))
        total_r_b = sum(r['r_gained'] for r in results_b)
        total_points_b = sum(r['points'] for r in results_b)
        winrate_b = (wins_b / len(results_b) * 100) if results_b else 0
        runner_success_b = (runner_hits_b / tp1_hits_b * 100) if tp1_hits_b > 0 else 0
        avg_r_b = total_r_b / len(results_b) if results_b else 0
        
        # Calculate max drawdown for Scenario B
        dd_b = []
        streak = 0
        for r in results_b:
            if r['result'] == 'loss':
                streak += 1
            else:
                dd_b.append(streak)
                streak = 0
        max_dd_b = max(dd_b) if dd_b else 0
        
        metrics.append({
            'Scenario': 'B (Hybrid 2R)',
            'Total_Net_Points': round(total_points_b, 2),
            'Winrate_Global_%': round(winrate_b, 2),
            'Runner_Success_%': round(runner_success_b, 2),
            'Avg_R_Per_Trade': round(avg_r_b, 2),
            'Max_Drawdown_Points': max_dd_b
        })
        
        # Scenario C metrics
        wins_c = sum(1 for r in results_c if r['result'] in ['partial_win', 'full_win'])
        runner_hits_c = sum(1 for r in results_c if r.get('runner_success', False))
        tp1_hits_c = sum(1 for r in results_c if r.get('tp1_hit', False))
        total_r_c = sum(r['r_gained'] for r in results_c)
        total_points_c = sum(r['points'] for r in results_c)
        winrate_c = (wins_c / len(results_c) * 100) if results_c else 0
        runner_success_c = (runner_hits_c / tp1_hits_c * 100) if tp1_hits_c > 0 else 0
        avg_r_c = total_r_c / len(results_c) if results_c else 0
        
        # Calculate max drawdown for Scenario C
        dd_c = []
        streak = 0
        for r in results_c:
            if r['result'] == 'loss':
                streak += 1
            else:
                dd_c.append(streak)
                streak = 0
        max_dd_c = max(dd_c) if dd_c else 0
        
        metrics.append({
            'Scenario': 'C (Hybrid EQ)',
            'Total_Net_Points': round(total_points_c, 2),
            'Winrate_Global_%': round(winrate_c, 2),
            'Runner_Success_%': round(runner_success_c, 2),
            'Avg_R_Per_Trade': round(avg_r_c, 2),
            'Max_Drawdown_Points': max_dd_c
        })
        
        results_df = pd.DataFrame(metrics)
        return results_df
    
    def run_full_optimization(self):
        """Run the complete optimization process"""
        print("""
    ╔══════════════════════════════════════════════════════════════════╗
    ║        NQ PARTIAL EXIT POSITION MANAGEMENT OPTIMIZATION          ║
    ║        Testing 3 Scenarios for SL3 Strategy                      ║
    ╚══════════════════════════════════════════════════════════════════╝
    """)
        
        # Load data
        self.load_data()
        
        # Identify all setups
        self.identify_setups()
        
        if len(self.setups) == 0:
            print("\nNo valid setups found!")
            return None
        
        # Run optimization
        results_df = self.run_optimization()
        
        # Print results
        print("\n" + "="*70)
        print("OPTIMIZATION RESULTS")
        print("="*70)
        print("\nComparative Analysis of 3 Position Management Scenarios:\n")
        print(results_df.to_string(index=False))
        
        # Export to CSV
        output_file = 'nq_partial_exit_results.csv'
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
        
        # Find best by net profit
        best_profit_idx = results_df['Total_Net_Points'].idxmax()
        best_profit = results_df.loc[best_profit_idx]
        
        print(f"\n1. Best Total Net Profit:")
        print(f"   Scenario: {best_profit['Scenario']}")
        print(f"   Net Profit: {best_profit['Total_Net_Points']:.2f} points")
        print(f"   Winrate: {best_profit['Winrate_Global_%']:.2f}%")
        print(f"   Avg R: {best_profit['Avg_R_Per_Trade']:.2f}")
        
        # Find best by avg R per trade
        best_r_idx = results_df['Avg_R_Per_Trade'].idxmax()
        best_r = results_df.loc[best_r_idx]
        
        print(f"\n2. Best Average R Per Trade:")
        print(f"   Scenario: {best_r['Scenario']}")
        print(f"   Avg R: {best_r['Avg_R_Per_Trade']:.2f}")
        print(f"   Net Profit: {best_r['Total_Net_Points']:.2f} points")
        print(f"   Winrate: {best_r['Winrate_Global_%']:.2f}%")
        
        # Find best by drawdown
        best_dd_idx = results_df['Max_Drawdown_Points'].idxmin()
        best_dd = results_df.loc[best_dd_idx]
        
        print(f"\n3. Best Risk Management (Lowest Drawdown):")
        print(f"   Scenario: {best_dd['Scenario']}")
        print(f"   Max Drawdown: {best_dd['Max_Drawdown_Points']} consecutive losses")
        print(f"   Net Profit: {best_dd['Total_Net_Points']:.2f} points")
        print(f"   Winrate: {best_dd['Winrate_Global_%']:.2f}%")
        
        # Runner analysis for B and C
        print(f"\n4. Runner Analysis:")
        for idx, row in results_df.iterrows():
            if row['Scenario'] in ['B (Hybrid 2R)', 'C (Hybrid EQ)']:
                print(f"   {row['Scenario']}:")
                print(f"     Runner Success Rate: {row['Runner_Success_%']}%")
                print(f"     Impact: {'Positive' if row['Total_Net_Points'] > results_df.loc[0, 'Total_Net_Points'] else 'Negative'} compared to baseline")
        
        # Final recommendation
        print(f"\n5. Final Recommendation:")
        if best_profit_idx == 0:
            print("   ✅ KEEP BASELINE (Scenario A - Full Exit 1R)")
            print("   Reason: Full exit at 1R provides the best overall performance.")
            print("   Runners do not add enough value to justify the complexity.")
        else:
            print(f"   ✅ OPTIMIZE WITH {best_profit['Scenario'].upper()}")
            print(f"   Reason: Partial exit strategy improves profitability by")
            improvement = best_profit['Total_Net_Points'] - results_df.loc[0, 'Total_Net_Points']
            improvement_pct = (improvement / abs(results_df.loc[0, 'Total_Net_Points'])) * 100 if results_df.loc[0, 'Total_Net_Points'] != 0 else 0
            print(f"   {improvement:.2f} points ({improvement_pct:.1f}% improvement)")
            print(f"   Runners successfully reach target {best_profit['Runner_Success_%']:.1f}% of the time.")
        
        print("\n" + "="*70)
        print("OPTIMIZATION COMPLETE")
        print("="*70)


if __name__ == "__main__":
    # Set data directory - use current directory or environment variable
    data_directory = os.environ.get('NQ_DATA_DIR', os.path.dirname(os.path.abspath(__file__)))
    
    # Initialize and run optimizer
    optimizer = NQPartialExitOptimizer(data_directory)
    results = optimizer.run_full_optimization()

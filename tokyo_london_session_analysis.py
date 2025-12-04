#!/usr/bin/env python3
"""
Tokyo and London Session Analysis for Nasdaq Futures (NQ)
Analyzes market structure and manipulation patterns across trading sessions
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import glob
import os

class TokyoLondonAnalyzer:
    def __init__(self, data_directory):
        self.data_directory = data_directory
        self.results = []
        self.fvg_results = []
        
    def load_data(self):
        """Load all 5-minute CSV files from 2018 to 2025"""
        # Only get 5m files, not 15m files
        all_files = glob.glob(os.path.join(self.data_directory, "*.csv"))
        files = sorted([f for f in all_files if "5m.csv" in f and "15m" not in f])
        
        all_data = []
        for file in files:
            print(f"Loading {os.path.basename(file)}...")
            try:
                df = pd.read_csv(file, sep=';', header=0)
                # Rename columns for easier access
                df.columns = ['Column1', 'Column2', 'Column3', 'Column4', 'Column5', 'Column6', 'Column7']
                df.columns = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
                
                # Parse datetime
                df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%d/%m/%Y %H:%M:%S')
                df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')
                df['Time'] = pd.to_datetime(df['Time'], format='%H:%M:%S').dt.time
                
                all_data.append(df)
            except Exception as e:
                print(f"Error loading {file}: {e}")
        
        if not all_data:
            raise ValueError("No data files found!")
            
        self.data = pd.concat(all_data, ignore_index=True)
        self.data = self.data.sort_values('DateTime').reset_index(drop=True)
        print(f"Total records loaded: {len(self.data)}")
        
    def get_time_range_data(self, df, start_time, end_time):
        """Extract data for a specific time range, handling midnight crossover"""
        if start_time <= end_time:
            # Simple case: within same day
            mask = (df['Time'] >= start_time) & (df['Time'] < end_time)
        else:
            # Crosses midnight
            mask = (df['Time'] >= start_time) | (df['Time'] < end_time)
        
        return df[mask]
    
    def detect_fvg(self, candles_df, fvg_type='bearish'):
        """
        Detect Fair Value Gaps (FVG) in the data
        
        FVG Baissier (Bearish): Low(n-2) > High(n) → Gap zone: [High(n), Low(n-2)]
        FVG Haussier (Bullish): High(n-2) < Low(n) → Gap zone: [High(n-2), Low(n)]
        
        Args:
            candles_df: DataFrame with OHLC data
            fvg_type: 'bearish' or 'bullish'
        
        Returns:
            List of FVG dictionaries with {timestamp, upper_bound, lower_bound}
        """
        fvgs = []
        
        if len(candles_df) < 3:
            return fvgs
        
        # Reset index to ensure we can iterate properly
        candles = candles_df.reset_index(drop=True)
        
        for i in range(2, len(candles)):
            candle_n = candles.iloc[i]
            candle_n_minus_2 = candles.iloc[i-2]
            
            if fvg_type == 'bearish':
                # Bearish FVG: Low(n-2) > High(n)
                if candle_n_minus_2['Low'] > candle_n['High']:
                    fvgs.append({
                        'timestamp': candle_n['DateTime'],
                        'candle_index': i,
                        'upper_bound': candle_n_minus_2['Low'],
                        'lower_bound': candle_n['High'],
                        'type': 'bearish'
                    })
            elif fvg_type == 'bullish':
                # Bullish FVG: High(n-2) < Low(n)
                if candle_n_minus_2['High'] < candle_n['Low']:
                    fvgs.append({
                        'timestamp': candle_n['DateTime'],
                        'candle_index': i,
                        'upper_bound': candle_n['Low'],
                        'lower_bound': candle_n_minus_2['High'],
                        'type': 'bullish'
                    })
        
        return fvgs
    
    def validate_fvg_entry(self, candles_df, fvg, setup_type, cutoff_time):
        """
        Validate if a candle closes above/below a FVG to trigger entry
        
        Setup Achat (Buy): Close > FVG_Bearish.upper_bound
        Setup Vente (Sell): Close < FVG_Bullish.lower_bound
        
        Args:
            candles_df: DataFrame with OHLC data
            fvg: FVG dictionary
            setup_type: 'buy' or 'sell'
            cutoff_time: Don't look for entries after this time
        
        Returns:
            Dictionary with validation info or None
        """
        # Get candles after FVG creation and before cutoff
        candles_after_fvg = candles_df[
            (candles_df['DateTime'] > fvg['timestamp']) &
            (candles_df['DateTime'] < cutoff_time)
        ].copy()
        
        if len(candles_after_fvg) == 0:
            return None
        
        for idx, candle in candles_after_fvg.iterrows():
            if setup_type == 'buy':
                # Looking for close above bearish FVG upper bound
                if candle['Close'] > fvg['upper_bound']:
                    return {
                        'validated': True,
                        'entry_timestamp': candle['DateTime'],
                        'entry_price': candle['Close'],
                        'fvg_upper': fvg['upper_bound'],
                        'fvg_lower': fvg['lower_bound']
                    }
            elif setup_type == 'sell':
                # Looking for close below bullish FVG lower bound
                if candle['Close'] < fvg['lower_bound']:
                    return {
                        'validated': True,
                        'entry_timestamp': candle['DateTime'],
                        'entry_price': candle['Close'],
                        'fvg_upper': fvg['upper_bound'],
                        'fvg_lower': fvg['lower_bound']
                    }
        
        return None
    
    def calculate_trade_outcome(self, candles_df, entry_info, stop_loss, target_equilibrium, target_full_range, setup_type):
        """
        Calculate if targets are hit before stop loss
        
        Args:
            candles_df: DataFrame with OHLC data after entry
            entry_info: Entry validation info
            stop_loss: Stop loss level
            target_equilibrium: Equilibrium target
            target_full_range: Full range target (Tokyo High for buy, Tokyo Low for sell)
            setup_type: 'buy' or 'sell'
        
        Returns:
            Dictionary with trade outcome
        """
        outcome = {
            'hit_equilibrium_before_stop': False,
            'hit_full_range_before_stop': False,
            'stop_hit': False,
            'equilibrium_hit_timestamp': pd.NaT,
            'full_range_hit_timestamp': pd.NaT,
            'stop_hit_timestamp': pd.NaT
        }
        
        # Get candles after entry
        candles_after_entry = candles_df[
            candles_df['DateTime'] > entry_info['entry_timestamp']
        ].copy()
        
        if len(candles_after_entry) == 0:
            return outcome
        
        for idx, candle in candles_after_entry.iterrows():
            if setup_type == 'buy':
                # Check stop loss (price goes down to stop)
                if not outcome['stop_hit'] and candle['Low'] <= stop_loss:
                    outcome['stop_hit'] = True
                    outcome['stop_hit_timestamp'] = candle['DateTime']
                
                # Check equilibrium target (price goes up to equilibrium)
                if not outcome['hit_equilibrium_before_stop'] and pd.isna(outcome['equilibrium_hit_timestamp']):
                    if candle['High'] >= target_equilibrium:
                        outcome['equilibrium_hit_timestamp'] = candle['DateTime']
                        # Only count as success if stop wasn't hit yet
                        if not outcome['stop_hit']:
                            outcome['hit_equilibrium_before_stop'] = True
                
                # Check full range target (price goes up to Tokyo High)
                if not outcome['hit_full_range_before_stop'] and pd.isna(outcome['full_range_hit_timestamp']):
                    if candle['High'] >= target_full_range:
                        outcome['full_range_hit_timestamp'] = candle['DateTime']
                        # Only count as success if stop wasn't hit yet
                        if not outcome['stop_hit']:
                            outcome['hit_full_range_before_stop'] = True
                
            elif setup_type == 'sell':
                # Check stop loss (price goes up to stop)
                if not outcome['stop_hit'] and candle['High'] >= stop_loss:
                    outcome['stop_hit'] = True
                    outcome['stop_hit_timestamp'] = candle['DateTime']
                
                # Check equilibrium target (price goes down to equilibrium)
                if not outcome['hit_equilibrium_before_stop'] and pd.isna(outcome['equilibrium_hit_timestamp']):
                    if candle['Low'] <= target_equilibrium:
                        outcome['equilibrium_hit_timestamp'] = candle['DateTime']
                        # Only count as success if stop wasn't hit yet
                        if not outcome['stop_hit']:
                            outcome['hit_equilibrium_before_stop'] = True
                
                # Check full range target (price goes down to Tokyo Low)
                if not outcome['hit_full_range_before_stop'] and pd.isna(outcome['full_range_hit_timestamp']):
                    if candle['Low'] <= target_full_range:
                        outcome['full_range_hit_timestamp'] = candle['DateTime']
                        # Only count as success if stop wasn't hit yet
                        if not outcome['stop_hit']:
                            outcome['hit_full_range_before_stop'] = True
            
            # Early exit if all outcomes determined
            if outcome['stop_hit'] and (pd.notna(outcome['equilibrium_hit_timestamp']) or outcome['hit_equilibrium_before_stop']):
                break
        
        return outcome
    
    def analyze_trading_day(self, date):
        """Analyze a single trading day following the specified algorithm"""
        from datetime import time
        
        result = {
            'london_date': date,
            'tokyo_high': np.nan,
            'tokyo_low': np.nan,
            'equilibrium': np.nan,
            'manipulation_type': 'None',
            'manipulation_occurred': False,
            'retest_low_count': 0,
            'retest_high_count': 0,
            'retest_equilibrium_count': 0,
            'break_timestamp': pd.NaT,
            'equilibrium_reach_timestamp': pd.NaT,
            'opposite_level_reach_timestamp': pd.NaT,
            'time_to_equilibrium_minutes': np.nan,
            'time_to_opposite_level_minutes': np.nan
        }
        
        # Tokyo session: 19:00 (J-1) to 01:00 (J)
        # We need data from previous day 19:00 to current day 01:00
        tokyo_start_date = date - timedelta(days=1)
        tokyo_end_date = date
        
        # Get Tokyo session data (19:00 previous day to 01:00 current day)
        tokyo_data = self.data[
            ((self.data['Date'] == tokyo_start_date) & (self.data['Time'] >= time(19, 0))) |
            ((self.data['Date'] == tokyo_end_date) & (self.data['Time'] < time(1, 0)))
        ]
        
        if len(tokyo_data) < 5:  # Need sufficient data
            return None
        
        # Calculate Tokyo Range
        tokyo_high = tokyo_data['High'].max()
        tokyo_low = tokyo_data['Low'].min()
        equilibrium = (tokyo_high + tokyo_low) / 2
        
        result['tokyo_high'] = tokyo_high
        result['tokyo_low'] = tokyo_low
        result['equilibrium'] = equilibrium
        
        # Manipulation window: 02:00 to 02:45 (current day)
        manipulation_data = self.data[
            (self.data['Date'] == date) &
            (self.data['Time'] >= time(2, 0)) &
            (self.data['Time'] < time(2, 45))
        ]
        
        if len(manipulation_data) == 0:
            return result
        
        # Detect manipulation and capture break timestamp
        manip_low = manipulation_data['Low'].min()
        manip_high = manipulation_data['High'].max()
        
        broke_below = manip_low < tokyo_low
        broke_above = manip_high > tokyo_high
        
        # Track first break timestamp
        break_timestamp_low = pd.NaT
        break_timestamp_high = pd.NaT
        
        if broke_below:
            # Find first candle that broke below Tokyo Low
            for idx, row in manipulation_data.iterrows():
                if row['Low'] < tokyo_low:
                    break_timestamp_low = row['DateTime']
                    break
        
        if broke_above:
            # Find first candle that broke above Tokyo High
            for idx, row in manipulation_data.iterrows():
                if row['High'] > tokyo_high:
                    break_timestamp_high = row['DateTime']
                    break
        
        if broke_below and broke_above:
            result['manipulation_type'] = 'Volatile/Both'
            result['manipulation_occurred'] = True
            # Use the earlier break
            if pd.notna(break_timestamp_low) and pd.notna(break_timestamp_high):
                result['break_timestamp'] = min(break_timestamp_low, break_timestamp_high)
            else:
                result['break_timestamp'] = break_timestamp_low if pd.notna(break_timestamp_low) else break_timestamp_high
        elif broke_below:
            result['manipulation_type'] = 'Bullish'  # Buy setup
            result['manipulation_occurred'] = True
            result['break_timestamp'] = break_timestamp_low
        elif broke_above:
            result['manipulation_type'] = 'Bearish'  # Sell setup
            result['manipulation_occurred'] = True
            result['break_timestamp'] = break_timestamp_high
        
        # Distribution phase: 02:45 to 05:00 (but we need data from break_timestamp onwards)
        if result['manipulation_occurred'] and pd.notna(result['break_timestamp']):
            # Get data from after break to 05:00 for velocity tracking
            post_break_data = self.data[
                (self.data['DateTime'] > result['break_timestamp']) &
                (self.data['Date'] == date) &
                (self.data['Time'] < time(5, 0))
            ]
            
            # Also get distribution data for retest counting (02:45 to 05:00)
            distribution_data = self.data[
                (self.data['Date'] == date) &
                (self.data['Time'] >= time(2, 45)) &
                (self.data['Time'] < time(5, 0))
            ]
            
            if len(distribution_data) > 0:
                # Count retests based on manipulation type
                if result['manipulation_type'] == 'Bullish':
                    # After breaking below Tokyo Low, count revisits to Low and Equilibrium
                    # Track velocity: find first touch of equilibrium and tokyo high
                    for idx, row in post_break_data.iterrows():
                        # Check for equilibrium reach
                        if pd.isna(result['equilibrium_reach_timestamp']):
                            if row['Low'] <= equilibrium <= row['High']:
                                result['equilibrium_reach_timestamp'] = row['DateTime']
                        
                        # Check for opposite level (Tokyo High) reach
                        if pd.isna(result['opposite_level_reach_timestamp']):
                            if row['High'] >= tokyo_high:
                                result['opposite_level_reach_timestamp'] = row['DateTime']
                    
                    # Count retests for distribution data
                    for idx, row in distribution_data.iterrows():
                        # Price touches or crosses Tokyo Low
                        if row['Low'] <= tokyo_low <= row['High']:
                            result['retest_low_count'] += 1
                        # Price touches or crosses Equilibrium
                        if row['Low'] <= equilibrium <= row['High']:
                            result['retest_equilibrium_count'] += 1
                
                elif result['manipulation_type'] == 'Bearish':
                    # After breaking above Tokyo High, count revisits to High and Equilibrium
                    # Track velocity: find first touch of equilibrium and tokyo low
                    for idx, row in post_break_data.iterrows():
                        # Check for equilibrium reach
                        if pd.isna(result['equilibrium_reach_timestamp']):
                            if row['Low'] <= equilibrium <= row['High']:
                                result['equilibrium_reach_timestamp'] = row['DateTime']
                        
                        # Check for opposite level (Tokyo Low) reach
                        if pd.isna(result['opposite_level_reach_timestamp']):
                            if row['Low'] <= tokyo_low:
                                result['opposite_level_reach_timestamp'] = row['DateTime']
                    
                    # Count retests for distribution data
                    for idx, row in distribution_data.iterrows():
                        # Price touches or crosses Tokyo High
                        if row['Low'] <= tokyo_high <= row['High']:
                            result['retest_high_count'] += 1
                        # Price touches or crosses Equilibrium
                        if row['Low'] <= equilibrium <= row['High']:
                            result['retest_equilibrium_count'] += 1
                
                elif result['manipulation_type'] == 'Volatile/Both':
                    # For volatile days, track based on which break happened first
                    # This is a simplified approach - we track to equilibrium from the first break
                    for idx, row in post_break_data.iterrows():
                        if pd.isna(result['equilibrium_reach_timestamp']):
                            if row['Low'] <= equilibrium <= row['High']:
                                result['equilibrium_reach_timestamp'] = row['DateTime']
                    
                    # Count all retests for volatile days
                    for idx, row in distribution_data.iterrows():
                        if row['Low'] <= tokyo_low <= row['High']:
                            result['retest_low_count'] += 1
                        if row['Low'] <= tokyo_high <= row['High']:
                            result['retest_high_count'] += 1
                        if row['Low'] <= equilibrium <= row['High']:
                            result['retest_equilibrium_count'] += 1
            
            # Calculate time durations in minutes
            if pd.notna(result['equilibrium_reach_timestamp']):
                time_diff = result['equilibrium_reach_timestamp'] - result['break_timestamp']
                result['time_to_equilibrium_minutes'] = time_diff.total_seconds() / 60.0
            
            if pd.notna(result['opposite_level_reach_timestamp']):
                time_diff = result['opposite_level_reach_timestamp'] - result['break_timestamp']
                result['time_to_opposite_level_minutes'] = time_diff.total_seconds() / 60.0
        
        return result
    
    def analyze_trading_day_with_fvg(self, date):
        """
        Analyze a single trading day with FVG validation strategy
        
        Algorithm:
        1. Identify manipulation (02:00-02:45) - Tokyo High/Low break
        2. Detect FVG during manipulation window (02:00-03:00)
        3. Validate entry (candle closes above/below FVG before 05:00)
        4. Calculate trade outcome (Target vs Stop)
        """
        from datetime import time
        
        # Get base result from existing results instead of recalculating
        base_result = None
        for result in self.results:
            if result['london_date'] == date:
                base_result = result
                break
        
        if base_result is None:
            return None
        
        # Initialize FVG-specific fields
        fvg_result = base_result.copy()
        fvg_result.update({
            'fvg_detected': False,
            'fvg_validated': False,
            'fvg_type': None,
            'fvg_upper_bound': np.nan,
            'fvg_lower_bound': np.nan,
            'fvg_creation_timestamp': pd.NaT,
            'fvg_entry_timestamp': pd.NaT,
            'fvg_entry_price': np.nan,
            'stop_loss': np.nan,
            'target_equilibrium': np.nan,
            'target_full_range': np.nan,
            'hit_equilibrium_before_stop': False,
            'hit_full_range_before_stop': False,
            'setup_type': None
        })
        
        # Only proceed if manipulation occurred
        if not base_result['manipulation_occurred']:
            return fvg_result
        
        manipulation_type = base_result['manipulation_type']
        tokyo_high = base_result['tokyo_high']
        tokyo_low = base_result['tokyo_low']
        equilibrium = base_result['equilibrium']
        
        # Get manipulation window data (02:00-03:00) for FVG detection
        manipulation_window = self.data[
            (self.data['Date'] == date) &
            (self.data['Time'] >= time(2, 0)) &
            (self.data['Time'] < time(3, 0))
        ].copy()
        
        if len(manipulation_window) < 3:
            return fvg_result
        
        # Determine setup type and detect appropriate FVG
        setup_type = None
        fvg_type = None
        fvgs = []
        
        if manipulation_type == 'Bullish':
            # Break below Tokyo Low → Look for Bearish FVG → Buy setup
            setup_type = 'buy'
            fvg_type = 'bearish'
            fvgs = self.detect_fvg(manipulation_window, fvg_type='bearish')
            fvg_result['stop_loss'] = manipulation_window['Low'].min()
            fvg_result['target_equilibrium'] = equilibrium
            fvg_result['target_full_range'] = tokyo_high
            
        elif manipulation_type == 'Bearish':
            # Break above Tokyo High → Look for Bullish FVG → Sell setup
            setup_type = 'sell'
            fvg_type = 'bullish'
            fvgs = self.detect_fvg(manipulation_window, fvg_type='bullish')
            fvg_result['stop_loss'] = manipulation_window['High'].max()
            fvg_result['target_equilibrium'] = equilibrium
            fvg_result['target_full_range'] = tokyo_low
            
        elif manipulation_type == 'Volatile/Both':
            # For volatile days, try both directions
            # Use the first break to determine primary setup
            first_break_time = base_result['break_timestamp']
            
            # Check which level broke first
            manip_data_before_break = manipulation_window[
                manipulation_window['DateTime'] <= first_break_time
            ]
            
            if len(manip_data_before_break) > 0:
                broke_low_first = manip_data_before_break['Low'].min() < tokyo_low
                broke_high_first = manip_data_before_break['High'].max() > tokyo_high
                
                if broke_low_first:
                    setup_type = 'buy'
                    fvg_type = 'bearish'
                    fvgs = self.detect_fvg(manipulation_window, fvg_type='bearish')
                    fvg_result['stop_loss'] = manipulation_window['Low'].min()
                    fvg_result['target_equilibrium'] = equilibrium
                    fvg_result['target_full_range'] = tokyo_high
                elif broke_high_first:
                    setup_type = 'sell'
                    fvg_type = 'bullish'
                    fvgs = self.detect_fvg(manipulation_window, fvg_type='bullish')
                    fvg_result['stop_loss'] = manipulation_window['High'].max()
                    fvg_result['target_equilibrium'] = equilibrium
                    fvg_result['target_full_range'] = tokyo_low
        
        fvg_result['setup_type'] = setup_type
        
        # Check if any FVG was detected
        if len(fvgs) > 0:
            fvg_result['fvg_detected'] = True
            
            # Use the first FVG detected (earliest in time)
            first_fvg = fvgs[0]
            fvg_result['fvg_type'] = fvg_type
            fvg_result['fvg_upper_bound'] = first_fvg['upper_bound']
            fvg_result['fvg_lower_bound'] = first_fvg['lower_bound']
            fvg_result['fvg_creation_timestamp'] = first_fvg['timestamp']
            
            # Validate entry (look for candle closing above/below FVG before 05:00)
            validation_cutoff = pd.Timestamp(date) + pd.Timedelta(hours=5)
            
            # Get data after FVG creation until 05:00
            post_fvg_data = self.data[
                (self.data['DateTime'] > first_fvg['timestamp']) &
                (self.data['DateTime'] < validation_cutoff)
            ].copy()
            
            if len(post_fvg_data) > 0:
                entry_validation = self.validate_fvg_entry(
                    post_fvg_data, 
                    first_fvg, 
                    setup_type, 
                    validation_cutoff
                )
                
                if entry_validation is not None:
                    fvg_result['fvg_validated'] = True
                    fvg_result['fvg_entry_timestamp'] = entry_validation['entry_timestamp']
                    fvg_result['fvg_entry_price'] = entry_validation['entry_price']
                    
                    # Calculate trade outcome
                    # Get data after entry until end of data for this day or reasonable time window
                    trade_window_end = validation_cutoff + pd.Timedelta(hours=5)  # Look up to 10:00
                    
                    post_entry_data = self.data[
                        (self.data['DateTime'] > entry_validation['entry_timestamp']) &
                        (self.data['DateTime'] < trade_window_end)
                    ].copy()
                    
                    if len(post_entry_data) > 0:
                        trade_outcome = self.calculate_trade_outcome(
                            post_entry_data,
                            entry_validation,
                            fvg_result['stop_loss'],
                            fvg_result['target_equilibrium'],
                            fvg_result['target_full_range'],
                            setup_type
                        )
                        
                        fvg_result['hit_equilibrium_before_stop'] = trade_outcome['hit_equilibrium_before_stop']
                        fvg_result['hit_full_range_before_stop'] = trade_outcome['hit_full_range_before_stop']
        
        return fvg_result
    
    def run_analysis(self):
        """Run the complete analysis across all trading days"""
        print("\n" + "="*60)
        print("Starting Tokyo-London Session Analysis")
        print("="*60 + "\n")
        
        # Get unique dates (for London session, which is the reference day J)
        # Start from 2nd day of data to ensure we have J-1 for Tokyo session
        unique_dates = sorted(self.data['Date'].unique())
        
        if len(unique_dates) < 2:
            raise ValueError("Not enough data days for analysis")
        
        # Skip first date since we need J-1 for Tokyo session
        analysis_dates = unique_dates[1:]
        
        print(f"Analyzing {len(analysis_dates)} trading days...")
        print(f"Date range: {analysis_dates[0]} to {analysis_dates[-1]}\n")
        
        # Process in batches with progress indicator
        total = len(analysis_dates)
        for i, date in enumerate(analysis_dates):
            if i % 200 == 0 and i > 0:
                print(f"  Progress: {i}/{total} days ({i/total*100:.1f}%)...")
            result = self.analyze_trading_day(date)
            if result is not None:
                self.results.append(result)
        
        print(f"Successfully analyzed {len(self.results)} trading days\n")
        
    def generate_statistics(self):
        """Generate summary statistics"""
        if not self.results:
            print("No results to analyze!")
            return
        
        df_results = pd.DataFrame(self.results)
        
        print("\n" + "="*60)
        print("STATISTICAL SUMMARY - TOKYO & LONDON SESSION ANALYSIS")
        print("="*60 + "\n")
        
        # 1. Total days analyzed
        total_days = len(df_results)
        print(f"1. TOTAL TRADING DAYS ANALYZED: {total_days}")
        print("-" * 60)
        
        # 2. Manipulation frequency
        days_with_manipulation = df_results['manipulation_occurred'].sum()
        manipulation_rate = (days_with_manipulation / total_days) * 100
        
        print(f"\n2. MANIPULATION FREQUENCY (02:00-02:45 window)")
        print("-" * 60)
        print(f"   Days with manipulation: {days_with_manipulation} ({manipulation_rate:.2f}%)")
        print(f"   Days without manipulation: {total_days - days_with_manipulation} ({100 - manipulation_rate:.2f}%)")
        
        # Breakdown by manipulation type
        manip_types = df_results['manipulation_type'].value_counts()
        print(f"\n   Manipulation Type Breakdown:")
        for manip_type, count in manip_types.items():
            if manip_type != 'None':
                pct = (count / total_days) * 100
                print(f"   - {manip_type}: {count} days ({pct:.2f}%)")
        
        # Bullish vs Bearish comparison
        bullish_days = (df_results['manipulation_type'] == 'Bullish').sum()
        bearish_days = (df_results['manipulation_type'] == 'Bearish').sum()
        volatile_days = (df_results['manipulation_type'] == 'Volatile/Both').sum()
        
        if days_with_manipulation > 0:
            print(f"\n   Among manipulated days:")
            print(f"   - Bullish (Low broken): {bullish_days} ({bullish_days/days_with_manipulation*100:.2f}%)")
            print(f"   - Bearish (High broken): {bearish_days} ({bearish_days/days_with_manipulation*100:.2f}%)")
            print(f"   - Volatile/Both: {volatile_days} ({volatile_days/days_with_manipulation*100:.2f}%)")
        
        # 3. Post-manipulation behavior
        print(f"\n3. POST-MANIPULATION BEHAVIOR (02:45-05:00 window)")
        print("-" * 60)
        
        # Bullish manipulation (Low broken)
        bullish_manip = df_results[df_results['manipulation_type'] == 'Bullish']
        if len(bullish_manip) > 0:
            eq_retest_bullish = (bullish_manip['retest_equilibrium_count'] > 0).sum()
            eq_retest_pct = (eq_retest_bullish / len(bullish_manip)) * 100
            
            low_retest_bullish = (bullish_manip['retest_low_count'] > 0).sum()
            low_retest_pct = (low_retest_bullish / len(bullish_manip)) * 100
            
            avg_eq_retests = bullish_manip['retest_equilibrium_count'].mean()
            avg_low_retests = bullish_manip['retest_low_count'].mean()
            
            print(f"\n   BULLISH MANIPULATION (Tokyo Low broken):")
            print(f"   - Sample size: {len(bullish_manip)} days")
            print(f"   - Days with Equilibrium retest: {eq_retest_bullish} ({eq_retest_pct:.2f}%)")
            print(f"   - Average Equilibrium retests: {avg_eq_retests:.2f}")
            print(f"   - Days with Tokyo Low retest: {low_retest_bullish} ({low_retest_pct:.2f}%)")
            print(f"   - Average Tokyo Low retests: {avg_low_retests:.2f}")
        
        # Bearish manipulation (High broken)
        bearish_manip = df_results[df_results['manipulation_type'] == 'Bearish']
        if len(bearish_manip) > 0:
            eq_retest_bearish = (bearish_manip['retest_equilibrium_count'] > 0).sum()
            eq_retest_pct = (eq_retest_bearish / len(bearish_manip)) * 100
            
            high_retest_bearish = (bearish_manip['retest_high_count'] > 0).sum()
            high_retest_pct = (high_retest_bearish / len(bearish_manip)) * 100
            
            avg_eq_retests = bearish_manip['retest_equilibrium_count'].mean()
            avg_high_retests = bearish_manip['retest_high_count'].mean()
            
            print(f"\n   BEARISH MANIPULATION (Tokyo High broken):")
            print(f"   - Sample size: {len(bearish_manip)} days")
            print(f"   - Days with Equilibrium retest: {eq_retest_bearish} ({eq_retest_pct:.2f}%)")
            print(f"   - Average Equilibrium retests: {avg_eq_retests:.2f}")
            print(f"   - Days with Tokyo High retest: {high_retest_bearish} ({high_retest_pct:.2f}%)")
            print(f"   - Average Tokyo High retests: {avg_high_retests:.2f}")
        
        # Volatile days
        volatile_manip = df_results[df_results['manipulation_type'] == 'Volatile/Both']
        if len(volatile_manip) > 0:
            print(f"\n   VOLATILE DAYS (Both High and Low broken):")
            print(f"   - Sample size: {len(volatile_manip)} days")
            print(f"   - Average Equilibrium retests: {volatile_manip['retest_equilibrium_count'].mean():.2f}")
            print(f"   - Average Tokyo Low retests: {volatile_manip['retest_low_count'].mean():.2f}")
            print(f"   - Average Tokyo High retests: {volatile_manip['retest_high_count'].mean():.2f}")
        
        print("\n" + "="*60)
        
        return df_results
    
    def generate_velocity_statistics(self, df_results):
        """Generate velocity analysis statistics for movement speed"""
        if df_results is None or len(df_results) == 0:
            print("No results to analyze for velocity!")
            return
        
        print("\n" + "="*60)
        print("VELOCITY ANALYSIS - MOVEMENT SPEED TO TARGETS")
        print("="*60 + "\n")
        
        # Filter for days where manipulation occurred
        df_manip = df_results[df_results['manipulation_occurred'] == True].copy()
        
        if len(df_manip) == 0:
            print("No manipulation days found for velocity analysis.")
            return
        
        print(f"Analyzing velocity for {len(df_manip)} days with manipulation\n")
        
        # Scenario A: Bullish Manipulation (Break Low)
        df_bullish = df_manip[df_manip['manipulation_type'] == 'Bullish'].copy()
        
        print("="*60)
        print("SCENARIO A: BULLISH MANIPULATION (Break Below Tokyo Low)")
        print("="*60 + "\n")
        
        if len(df_bullish) > 0:
            # A1: Time to Equilibrium
            eq_times = df_bullish['time_to_equilibrium_minutes'].dropna()
            
            print(f"A1. TIME TO REACH EQUILIBRIUM (after breaking Tokyo Low)")
            print("-" * 60)
            if len(eq_times) > 0:
                print(f"   Sample size: {len(eq_times)} days (out of {len(df_bullish)} bullish days)")
                print(f"   Mean duration: {eq_times.mean():.2f} minutes")
                print(f"   Median duration: {eq_times.median():.2f} minutes")
                print(f"   Min duration: {eq_times.min():.2f} minutes")
                print(f"   Max duration: {eq_times.max():.2f} minutes")
                
                # Success rate within 30 minutes
                within_30min = (eq_times <= 30).sum()
                success_rate_30 = (within_30min / len(eq_times)) * 100
                print(f"   Reached in ≤30 min: {within_30min}/{len(eq_times)} ({success_rate_30:.1f}%)")
                
                # Distribution histogram
                print(f"\n   Distribution Histogram:")
                self._print_histogram(eq_times, "Time to Equilibrium")
            else:
                print(f"   No valid data (equilibrium never reached)")
            
            # A2: Time to Tokyo High
            high_times = df_bullish['time_to_opposite_level_minutes'].dropna()
            
            print(f"\nA2. TIME TO REACH TOKYO HIGH (opposite level)")
            print("-" * 60)
            if len(high_times) > 0:
                print(f"   Sample size: {len(high_times)} days (out of {len(df_bullish)} bullish days)")
                print(f"   Mean duration: {high_times.mean():.2f} minutes")
                print(f"   Median duration: {high_times.median():.2f} minutes")
                print(f"   Min duration: {high_times.min():.2f} minutes")
                print(f"   Max duration: {high_times.max():.2f} minutes")
                
                within_30min = (high_times <= 30).sum()
                success_rate_30 = (within_30min / len(high_times)) * 100
                print(f"   Reached in ≤30 min: {within_30min}/{len(high_times)} ({success_rate_30:.1f}%)")
                
                print(f"\n   Distribution Histogram:")
                self._print_histogram(high_times, "Time to Tokyo High")
            else:
                print(f"   No valid data (Tokyo High never reached)")
        else:
            print("No bullish manipulation days found.\n")
        
        # Scenario B: Bearish Manipulation (Break High)
        df_bearish = df_manip[df_manip['manipulation_type'] == 'Bearish'].copy()
        
        print("\n" + "="*60)
        print("SCENARIO B: BEARISH MANIPULATION (Break Above Tokyo High)")
        print("="*60 + "\n")
        
        if len(df_bearish) > 0:
            # B1: Time to Equilibrium
            eq_times = df_bearish['time_to_equilibrium_minutes'].dropna()
            
            print(f"B1. TIME TO REACH EQUILIBRIUM (after breaking Tokyo High)")
            print("-" * 60)
            if len(eq_times) > 0:
                print(f"   Sample size: {len(eq_times)} days (out of {len(df_bearish)} bearish days)")
                print(f"   Mean duration: {eq_times.mean():.2f} minutes")
                print(f"   Median duration: {eq_times.median():.2f} minutes")
                print(f"   Min duration: {eq_times.min():.2f} minutes")
                print(f"   Max duration: {eq_times.max():.2f} minutes")
                
                within_30min = (eq_times <= 30).sum()
                success_rate_30 = (within_30min / len(eq_times)) * 100
                print(f"   Reached in ≤30 min: {within_30min}/{len(eq_times)} ({success_rate_30:.1f}%)")
                
                print(f"\n   Distribution Histogram:")
                self._print_histogram(eq_times, "Time to Equilibrium")
            else:
                print(f"   No valid data (equilibrium never reached)")
            
            # B2: Time to Tokyo Low
            low_times = df_bearish['time_to_opposite_level_minutes'].dropna()
            
            print(f"\nB2. TIME TO REACH TOKYO LOW (opposite level)")
            print("-" * 60)
            if len(low_times) > 0:
                print(f"   Sample size: {len(low_times)} days (out of {len(df_bearish)} bearish days)")
                print(f"   Mean duration: {low_times.mean():.2f} minutes")
                print(f"   Median duration: {low_times.median():.2f} minutes")
                print(f"   Min duration: {low_times.min():.2f} minutes")
                print(f"   Max duration: {low_times.max():.2f} minutes")
                
                within_30min = (low_times <= 30).sum()
                success_rate_30 = (within_30min / len(low_times)) * 100
                print(f"   Reached in ≤30 min: {within_30min}/{len(low_times)} ({success_rate_30:.1f}%)")
                
                print(f"\n   Distribution Histogram:")
                self._print_histogram(low_times, "Time to Tokyo Low")
            else:
                print(f"   No valid data (Tokyo Low never reached)")
        else:
            print("No bearish manipulation days found.\n")
        
        # Summary insights
        print("\n" + "="*60)
        print("VELOCITY SUMMARY - KEY INSIGHTS")
        print("="*60 + "\n")
        
        all_eq_times = df_manip['time_to_equilibrium_minutes'].dropna()
        if len(all_eq_times) > 0:
            print(f"Overall Equilibrium Reach Statistics:")
            print(f"  - {len(all_eq_times)}/{len(df_manip)} manipulation days reached equilibrium ({len(all_eq_times)/len(df_manip)*100:.1f}%)")
            print(f"  - Average time: {all_eq_times.mean():.2f} minutes")
            print(f"  - Median time: {all_eq_times.median():.2f} minutes")
            
            within_30 = (all_eq_times <= 30).sum()
            print(f"  - Within 30 minutes: {within_30}/{len(all_eq_times)} ({within_30/len(all_eq_times)*100:.1f}%)")
        
        all_opposite_times = df_manip['time_to_opposite_level_minutes'].dropna()
        if len(all_opposite_times) > 0:
            print(f"\nOverall Opposite Level Reach Statistics:")
            print(f"  - {len(all_opposite_times)}/{len(df_manip)} manipulation days reached opposite level ({len(all_opposite_times)/len(df_manip)*100:.1f}%)")
            print(f"  - Average time: {all_opposite_times.mean():.2f} minutes")
            print(f"  - Median time: {all_opposite_times.median():.2f} minutes")
        
        print("\n" + "="*60 + "\n")
        
        # Save velocity data to CSV
        velocity_output = os.path.join(self.data_directory, 'tokyo_london_velocity_analysis.csv')
        df_manip.to_csv(velocity_output, index=False)
        print(f"Velocity analysis data saved to: {velocity_output}\n")
    
    def run_fvg_analysis(self):
        """Run FVG-based trading analysis across all trading days"""
        print("\n" + "="*60)
        print("Starting FVG (Fair Value Gap) Analysis")
        print("="*60 + "\n")
        
        # Get unique dates (same as regular analysis)
        unique_dates = sorted(self.data['Date'].unique())
        
        if len(unique_dates) < 2:
            raise ValueError("Not enough data days for analysis")
        
        # Skip first date since we need J-1 for Tokyo session
        analysis_dates = unique_dates[1:]
        
        print(f"Analyzing {len(analysis_dates)} trading days with FVG validation...")
        print(f"Date range: {analysis_dates[0]} to {analysis_dates[-1]}\n")
        
        # Process in batches with progress indicator
        total = len(analysis_dates)
        for i, date in enumerate(analysis_dates):
            if i % 200 == 0 and i > 0:
                print(f"  Progress: {i}/{total} days ({i/total*100:.1f}%)...")
            result = self.analyze_trading_day_with_fvg(date)
            if result is not None:
                self.fvg_results.append(result)
        
        print(f"Successfully analyzed {len(self.fvg_results)} trading days with FVG\n")
    
    def generate_fvg_statistics(self):
        """Generate FVG validation statistics and winrates"""
        if not self.fvg_results:
            print("No FVG results to analyze!")
            return None
        
        df_fvg = pd.DataFrame(self.fvg_results)
        
        print("\n" + "="*60)
        print("FVG (FAIR VALUE GAP) VALIDATION ANALYSIS")
        print("="*60 + "\n")
        
        # 1. Filtrage Statistics
        print("1. FILTRAGE - IMPACT DU CRITÈRE FVG")
        print("-" * 60)
        
        total_days = len(df_fvg)
        days_with_manipulation = df_fvg['manipulation_occurred'].sum()
        days_with_fvg_detected = df_fvg['fvg_detected'].sum()
        days_with_fvg_validated = df_fvg['fvg_validated'].sum()
        
        print(f"Total jours analysés: {total_days}")
        print(f"Jours avec manipulation (02:00-02:45): {days_with_manipulation} ({days_with_manipulation/total_days*100:.2f}%)")
        print(f"Jours avec FVG détecté (02:00-03:00): {days_with_fvg_detected} ({days_with_fvg_detected/total_days*100:.2f}%)")
        print(f"Jours avec FVG validé (entry < 05:00): {days_with_fvg_validated} ({days_with_fvg_validated/total_days*100:.2f}%)")
        
        # Calculate filtering impact
        if days_with_manipulation > 0:
            filter_rate = ((days_with_manipulation - days_with_fvg_validated) / days_with_manipulation) * 100
            print(f"\n→ Le filtre FVG élimine: {days_with_manipulation - days_with_fvg_validated} trades ({filter_rate:.2f}%)")
            print(f"→ Trades validés par FVG: {days_with_fvg_validated} ({days_with_fvg_validated/days_with_manipulation*100:.2f}% des manipulations)")
        
        # Breakdown by setup type
        print(f"\nRépartition des setups validés:")
        if days_with_fvg_validated > 0:
            validated_trades = df_fvg[df_fvg['fvg_validated'] == True]
            setup_counts = validated_trades['setup_type'].value_counts()
            for setup, count in setup_counts.items():
                print(f"  - Setup {setup.upper()}: {count} trades ({count/days_with_fvg_validated*100:.2f}%)")
        
        # 2. Winrate Statistics
        print(f"\n2. WINRATE - RÉSULTATS DES TRADES VALIDÉS")
        print("-" * 60)
        
        if days_with_fvg_validated > 0:
            validated_trades = df_fvg[df_fvg['fvg_validated'] == True].copy()
            
            # Equilibrium Winrate
            eq_winners = validated_trades['hit_equilibrium_before_stop'].sum()
            eq_winrate = (eq_winners / days_with_fvg_validated) * 100
            
            print(f"\nA. WINRATE EQUILIBRIUM (Target 1):")
            print(f"   Trades atteignant l'Equilibrium avant Stop: {eq_winners}/{days_with_fvg_validated}")
            print(f"   Winrate: {eq_winrate:.2f}%")
            
            # Full Range Winrate
            full_winners = validated_trades['hit_full_range_before_stop'].sum()
            full_winrate = (full_winners / days_with_fvg_validated) * 100
            
            print(f"\nB. WINRATE FULL RANGE (Target 2):")
            print(f"   Trades traversant tout le range avant Stop: {full_winners}/{days_with_fvg_validated}")
            print(f"   Winrate: {full_winrate:.2f}%")
            
            # Breakdown by setup type
            print(f"\nC. WINRATE PAR TYPE DE SETUP:")
            for setup_type in validated_trades['setup_type'].unique():
                if pd.notna(setup_type):
                    setup_trades = validated_trades[validated_trades['setup_type'] == setup_type]
                    n_trades = len(setup_trades)
                    
                    eq_wins = setup_trades['hit_equilibrium_before_stop'].sum()
                    eq_wr = (eq_wins / n_trades) * 100 if n_trades > 0 else 0
                    
                    full_wins = setup_trades['hit_full_range_before_stop'].sum()
                    full_wr = (full_wins / n_trades) * 100 if n_trades > 0 else 0
                    
                    print(f"\n   Setup {setup_type.upper()} ({n_trades} trades):")
                    print(f"   - Equilibrium Winrate: {eq_wins}/{n_trades} ({eq_wr:.2f}%)")
                    print(f"   - Full Range Winrate: {full_wins}/{n_trades} ({full_wr:.2f}%)")
        else:
            print("\n   Aucun trade validé avec FVG.")
        
        # 3. Summary Comparison
        print(f"\n3. COMPARAISON - AVANT/APRÈS FILTRE FVG")
        print("-" * 60)
        
        print(f"\nSANS filtre FVG:")
        print(f"  - Nombre de setups: {days_with_manipulation}")
        print(f"  - Taux de filtrage: 0%")
        
        if days_with_manipulation > 0:
            print(f"\nAVEC filtre FVG:")
            print(f"  - Nombre de setups: {days_with_fvg_validated}")
            print(f"  - Taux de filtrage: {filter_rate:.2f}%")
            print(f"  - Winrate Equilibrium: {eq_winrate:.2f}%")
            print(f"  - Winrate Full Range: {full_winrate:.2f}%")
        
        print("\n" + "="*60 + "\n")
        
        return df_fvg
    
    def _print_histogram(self, data, title, bins=10):
        """Print an ASCII histogram of the data distribution"""
        if len(data) == 0:
            return
        
        # Create bins
        min_val = data.min()
        max_val = data.max()
        bin_edges = np.linspace(min_val, max_val, bins + 1)
        
        # Count values in each bin
        hist, _ = np.histogram(data, bins=bin_edges)
        
        # Find max count for scaling
        max_count = hist.max()
        
        # Print histogram
        bar_width = 40  # max width of bars
        for i in range(len(hist)):
            bin_start = bin_edges[i]
            bin_end = bin_edges[i + 1]
            count = hist[i]
            
            # Scale bar
            if max_count > 0:
                bar_len = int((count / max_count) * bar_width)
            else:
                bar_len = 0
            
            bar = '█' * bar_len
            pct = (count / len(data)) * 100
            
            print(f"   {bin_start:6.1f}-{bin_end:6.1f} min | {bar} {count} ({pct:.1f}%)")
    
    def save_results(self, df_results, output_file='tokyo_london_analysis_results.csv'):
        """Save detailed results to CSV"""
        output_path = os.path.join(self.data_directory, output_file)
        df_results.to_csv(output_path, index=False)
        print(f"\nDetailed results saved to: {output_path}")
        
        # Also save a summary text file
        summary_file = output_file.replace('.csv', '_summary.txt')
        summary_path = os.path.join(self.data_directory, summary_file)
        
        with open(summary_path, 'w') as f:
            f.write("TOKYO & LONDON SESSION ANALYSIS - SUMMARY REPORT\n")
            f.write("="*60 + "\n\n")
            f.write(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Trading Days Analyzed: {len(df_results)}\n\n")
            
            days_with_manipulation = df_results['manipulation_occurred'].sum()
            f.write(f"Days with Manipulation: {days_with_manipulation} ({days_with_manipulation/len(df_results)*100:.2f}%)\n")
            
            manip_types = df_results['manipulation_type'].value_counts()
            f.write("\nManipulation Type Distribution:\n")
            for manip_type, count in manip_types.items():
                f.write(f"  {manip_type}: {count} ({count/len(df_results)*100:.2f}%)\n")
            
            f.write("\n" + "="*60 + "\n")
        
        print(f"Summary report saved to: {summary_path}")
    
    def save_fvg_results(self, df_fvg):
        """Save FVG analysis results to CSV"""
        output_file = 'tokyo_london_fvg_analysis.csv'
        output_path = os.path.join(self.data_directory, output_file)
        df_fvg.to_csv(output_path, index=False)
        print(f"\nFVG analysis results saved to: {output_path}")
    
    def backtest_trade(self, entry_timestamp, entry_price, stop_loss, take_profits, setup_type, cutoff_time):
        """
        Backtest a single trade with multiple take profit levels
        
        Args:
            entry_timestamp: Entry timestamp
            entry_price: Entry price
            stop_loss: Stop loss level
            take_profits: Dictionary of TP names and levels {'1R': price, '1.5R': price, ...}
            setup_type: 'buy' or 'sell'
            cutoff_time: Maximum time to check (05:00 UTC)
        
        Returns:
            Dictionary with results for each TP level
        """
        from datetime import time
        
        results = {}
        
        # Get candles after entry until cutoff (05:00)
        post_entry_data = self.data[
            (self.data['DateTime'] > entry_timestamp) &
            (self.data['DateTime'] < cutoff_time)
        ].copy()
        
        if len(post_entry_data) == 0:
            # No data to backtest
            for tp_name in take_profits.keys():
                results[tp_name] = {
                    'outcome': 'NO_DATA',
                    'hit_timestamp': pd.NaT,
                    'bars_to_outcome': 0
                }
            return results
        
        # For each TP level, check if it's hit before SL
        for tp_name, tp_level in take_profits.items():
            hit_tp = False
            hit_sl = False
            hit_timestamp = pd.NaT
            bars_counted = 0
            
            for idx, candle in post_entry_data.iterrows():
                bars_counted += 1
                
                if setup_type == 'buy':
                    # Check SL first (CRITICAL: SL must be checked before TP)
                    if candle['Low'] <= stop_loss:
                        hit_sl = True
                        break
                    # Then check TP
                    elif candle['High'] >= tp_level:
                        hit_tp = True
                        hit_timestamp = candle['DateTime']
                        break
                        
                elif setup_type == 'sell':
                    # Check SL first
                    if candle['High'] >= stop_loss:
                        hit_sl = True
                        break
                    # Then check TP
                    elif candle['Low'] <= tp_level:
                        hit_tp = True
                        hit_timestamp = candle['DateTime']
                        break
            
            # Record outcome
            if hit_tp:
                results[tp_name] = {
                    'outcome': 'WIN',
                    'hit_timestamp': hit_timestamp,
                    'bars_to_outcome': bars_counted
                }
            elif hit_sl:
                results[tp_name] = {
                    'outcome': 'LOSS',
                    'hit_timestamp': pd.NaT,
                    'bars_to_outcome': bars_counted
                }
            else:
                results[tp_name] = {
                    'outcome': 'NO_TOUCH',
                    'hit_timestamp': pd.NaT,
                    'bars_to_outcome': bars_counted
                }
        
        return results
    
    def calculate_risk_reward(self, entry_price, target_price, stop_loss, setup_type):
        """
        Calculate Risk:Reward ratio
        
        Args:
            entry_price: Entry price
            target_price: Target price
            stop_loss: Stop loss price
            setup_type: 'buy' or 'sell'
        
        Returns:
            Risk:Reward ratio as float
        """
        risk = abs(entry_price - stop_loss)
        
        if risk == 0:
            return 0.0
        
        reward = abs(target_price - entry_price)
        
        return reward / risk
    
    def run_comprehensive_backtest(self):
        """
        Run comprehensive backtest comparing Swing SL vs Bougie SL strategies
        with multiple Take Profit targets (1R, 1.5R, 2R, 2.5R, Equilibrium, Full Range)
        """
        from datetime import time
        
        print("\n" + "="*70)
        print("COMPREHENSIVE BACKTEST - SWING SL vs BOUGIE SL")
        print("="*70 + "\n")
        
        # Load FVG validated trades
        fvg_file = os.path.join(self.data_directory, 'tokyo_london_fvg_analysis.csv')
        
        if not os.path.exists(fvg_file):
            print(f"ERROR: FVG analysis file not found: {fvg_file}")
            print("Please run FVG analysis first.")
            return None
        
        df_fvg = pd.read_csv(fvg_file, parse_dates=['london_date', 'break_timestamp', 
                                                      'equilibrium_reach_timestamp', 
                                                      'opposite_level_reach_timestamp',
                                                      'fvg_creation_timestamp', 
                                                      'fvg_entry_timestamp'])
        
        # Filter for validated FVG trades only
        validated_trades = df_fvg[df_fvg['fvg_validated'] == True].copy()
        
        print(f"Total validated FVG trades: {len(validated_trades)}")
        
        if len(validated_trades) == 0:
            print("No validated trades to backtest!")
            return None
        
        # Initialize results storage
        swing_results = []
        bougie_results = []
        
        # Process each validated trade
        print("Processing trades...")
        
        for idx, trade in validated_trades.iterrows():
            # Skip if essential data is missing
            if pd.isna(trade['fvg_entry_timestamp']) or pd.isna(trade['fvg_entry_price']):
                continue
            
            entry_timestamp = trade['fvg_entry_timestamp']
            entry_price = trade['fvg_entry_price']
            setup_type = trade['setup_type']
            
            # Get the date for this trade
            trade_date = trade['london_date']
            
            # Get manipulation window data to find signal candle
            manipulation_start = pd.Timestamp(trade_date) + pd.Timedelta(hours=2)
            manipulation_end = pd.Timestamp(trade_date) + pd.Timedelta(hours=3)
            
            manipulation_data = self.data[
                (self.data['DateTime'] >= manipulation_start) &
                (self.data['DateTime'] < manipulation_end)
            ].copy()
            
            # Find signal candle (the one with entry_timestamp)
            signal_candle = self.data[self.data['DateTime'] == entry_timestamp]
            
            if len(signal_candle) == 0:
                continue
            
            signal_candle = signal_candle.iloc[0]
            
            # Calculate Stop Losses
            # Swing SL: Absolute extreme of manipulation
            if setup_type == 'buy':
                swing_sl = manipulation_data['Low'].min() if len(manipulation_data) > 0 else trade['stop_loss']
                bougie_sl = signal_candle['Low']
            else:  # sell
                swing_sl = manipulation_data['High'].max() if len(manipulation_data) > 0 else trade['stop_loss']
                bougie_sl = signal_candle['High']
            
            # Skip if SL is too close to entry (< 5 points)
            if abs(entry_price - bougie_sl) < 5:
                continue
            
            # Skip if swing_sl is invalid
            if pd.isna(swing_sl) or abs(entry_price - swing_sl) < 1:
                continue
            
            # Define cutoff time (05:00 UTC same day)
            cutoff_time = pd.Timestamp(trade_date) + pd.Timedelta(hours=5)
            
            # ===== SWING SL STRATEGY =====
            swing_risk = abs(entry_price - swing_sl)
            
            # Calculate Take Profit levels for Swing SL
            swing_tps = {}
            if setup_type == 'buy':
                swing_tps['1R'] = entry_price + (1.0 * swing_risk)
                swing_tps['1.5R'] = entry_price + (1.5 * swing_risk)
                swing_tps['2R'] = entry_price + (2.0 * swing_risk)
                swing_tps['2.5R'] = entry_price + (2.5 * swing_risk)
                swing_tps['Equilibrium'] = trade['target_equilibrium']
                swing_tps['Full_Range'] = trade['target_full_range']
            else:  # sell
                swing_tps['1R'] = entry_price - (1.0 * swing_risk)
                swing_tps['1.5R'] = entry_price - (1.5 * swing_risk)
                swing_tps['2R'] = entry_price - (2.0 * swing_risk)
                swing_tps['2.5R'] = entry_price - (2.5 * swing_risk)
                swing_tps['Equilibrium'] = trade['target_equilibrium']
                swing_tps['Full_Range'] = trade['target_full_range']
            
            # Backtest Swing SL
            swing_outcomes = self.backtest_trade(
                entry_timestamp, entry_price, swing_sl, 
                swing_tps, setup_type, cutoff_time
            )
            
            # Store Swing SL results
            swing_result = {
                'trade_id': idx,
                'date': trade_date,
                'setup_type': setup_type,
                'entry_price': entry_price,
                'stop_loss': swing_sl,
                'risk': swing_risk,
                'strategy': 'Swing_SL'
            }
            
            # Add outcomes for each TP
            for tp_name, outcome_data in swing_outcomes.items():
                swing_result[f'{tp_name}_outcome'] = outcome_data['outcome']
                swing_result[f'{tp_name}_level'] = swing_tps[tp_name]
                
                # Calculate actual RR for dynamic targets
                if tp_name in ['Equilibrium', 'Full_Range']:
                    swing_result[f'{tp_name}_RR'] = self.calculate_risk_reward(
                        entry_price, swing_tps[tp_name], swing_sl, setup_type
                    )
            
            swing_results.append(swing_result)
            
            # ===== BOUGIE SL STRATEGY =====
            bougie_risk = abs(entry_price - bougie_sl)
            
            # Calculate Take Profit levels for Bougie SL
            bougie_tps = {}
            if setup_type == 'buy':
                bougie_tps['1R'] = entry_price + (1.0 * bougie_risk)
                bougie_tps['1.5R'] = entry_price + (1.5 * bougie_risk)
                bougie_tps['2R'] = entry_price + (2.0 * bougie_risk)
                bougie_tps['2.5R'] = entry_price + (2.5 * bougie_risk)
                bougie_tps['Equilibrium'] = trade['target_equilibrium']
                bougie_tps['Full_Range'] = trade['target_full_range']
            else:  # sell
                bougie_tps['1R'] = entry_price - (1.0 * bougie_risk)
                bougie_tps['1.5R'] = entry_price - (1.5 * bougie_risk)
                bougie_tps['2R'] = entry_price - (2.0 * bougie_risk)
                bougie_tps['2.5R'] = entry_price - (2.5 * bougie_risk)
                bougie_tps['Equilibrium'] = trade['target_equilibrium']
                bougie_tps['Full_Range'] = trade['target_full_range']
            
            # Backtest Bougie SL
            bougie_outcomes = self.backtest_trade(
                entry_timestamp, entry_price, bougie_sl, 
                bougie_tps, setup_type, cutoff_time
            )
            
            # Store Bougie SL results
            bougie_result = {
                'trade_id': idx,
                'date': trade_date,
                'setup_type': setup_type,
                'entry_price': entry_price,
                'stop_loss': bougie_sl,
                'risk': bougie_risk,
                'strategy': 'Bougie_SL'
            }
            
            # Add outcomes for each TP
            for tp_name, outcome_data in bougie_outcomes.items():
                bougie_result[f'{tp_name}_outcome'] = outcome_data['outcome']
                bougie_result[f'{tp_name}_level'] = bougie_tps[tp_name]
                
                # Calculate actual RR for dynamic targets
                if tp_name in ['Equilibrium', 'Full_Range']:
                    bougie_result[f'{tp_name}_RR'] = self.calculate_risk_reward(
                        entry_price, bougie_tps[tp_name], bougie_sl, setup_type
                    )
            
            bougie_results.append(bougie_result)
        
        print(f"Backtest completed: {len(swing_results)} trades processed\n")
        
        # Convert to DataFrames
        df_swing = pd.DataFrame(swing_results)
        df_bougie = pd.DataFrame(bougie_results)
        
        return df_swing, df_bougie
    
    def generate_backtest_statistics(self, df_swing, df_bougie):
        """
        Generate comprehensive statistics comparing Swing SL vs Bougie SL strategies
        
        Args:
            df_swing: DataFrame with Swing SL backtest results
            df_bougie: DataFrame with Bougie SL backtest results
        
        Returns:
            Dictionary with statistics for both strategies
        """
        if df_swing is None or df_bougie is None or len(df_swing) == 0 or len(df_bougie) == 0:
            print("No backtest results to analyze!")
            return None
        
        stats = {
            'swing': {},
            'bougie': {}
        }
        
        # Process both strategies
        for strategy_name, df in [('swing', df_swing), ('bougie', df_bougie)]:
            n_trades = len(df)
            
            # Basic statistics
            stats[strategy_name]['total_trades'] = n_trades
            stats[strategy_name]['avg_risk'] = df['risk'].mean()
            stats[strategy_name]['median_risk'] = df['risk'].median()
            stats[strategy_name]['min_risk'] = df['risk'].min()
            stats[strategy_name]['max_risk'] = df['risk'].max()
            
            # Fixed R:R winrates
            rr_targets = ['1R', '1.5R', '2R', '2.5R']
            stats[strategy_name]['fixed_rr'] = {}
            
            for rr in rr_targets:
                outcome_col = f'{rr}_outcome'
                if outcome_col in df.columns:
                    wins = (df[outcome_col] == 'WIN').sum()
                    winrate = (wins / n_trades) * 100 if n_trades > 0 else 0
                    stats[strategy_name]['fixed_rr'][rr] = {
                        'wins': wins,
                        'total': n_trades,
                        'winrate': winrate
                    }
            
            # Dynamic targets (Equilibrium & Full Range)
            dynamic_targets = ['Equilibrium', 'Full_Range']
            stats[strategy_name]['dynamic'] = {}
            
            for target in dynamic_targets:
                outcome_col = f'{target}_outcome'
                rr_col = f'{target}_RR'
                
                if outcome_col in df.columns:
                    wins = (df[outcome_col] == 'WIN').sum()
                    winrate = (wins / n_trades) * 100 if n_trades > 0 else 0
                    
                    # Calculate average and median RR for winning trades
                    winning_trades = df[df[outcome_col] == 'WIN']
                    if len(winning_trades) > 0 and rr_col in winning_trades.columns:
                        avg_rr = winning_trades[rr_col].mean()
                        median_rr = winning_trades[rr_col].median()
                    else:
                        # Calculate from all trades
                        if rr_col in df.columns:
                            avg_rr = df[rr_col].mean()
                            median_rr = df[rr_col].median()
                        else:
                            avg_rr = 0.0
                            median_rr = 0.0
                    
                    stats[strategy_name]['dynamic'][target] = {
                        'wins': wins,
                        'total': n_trades,
                        'winrate': winrate,
                        'avg_rr': avg_rr,
                        'median_rr': median_rr
                    }
        
        return stats
    
    def save_backtest_results(self, df_swing, df_bougie, stats):
        """
        Save backtest results to CSV and generate comparison report
        
        Args:
            df_swing: Swing SL backtest results
            df_bougie: Bougie SL backtest results
            stats: Statistics dictionary
        """
        if df_swing is None or df_bougie is None:
            print("No results to save!")
            return
        
        # Save detailed results to CSV
        results_file = os.path.join(self.data_directory, 'tokyo_london_backtest_results.csv')
        
        # Combine both strategies
        df_combined = pd.concat([df_swing, df_bougie], ignore_index=True)
        df_combined.to_csv(results_file, index=False)
        
        print(f"Detailed backtest results saved to: {results_file}")
        
        # Generate comparison report
        report_file = os.path.join(self.data_directory, 'BACKTEST_COMPARISON_REPORT.md')
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("# BACKTEST COMPARISON: SWING SL vs BOUGIE SL\n\n")
            f.write("="*70 + "\n\n")
            
            f.write(f"**Dataset:** 2018-2025 NQ Futures (5-minute data)\n\n")
            f.write(f"**Total Validated FVG Trades:** {stats['swing']['total_trades']}\n\n")
            
            f.write("---\n\n")
            
            # Strategy 1: Swing SL
            f.write("## STRATEGY 1: SWING SL (Conservative)\n\n")
            f.write("**Stop Loss Placement:** Under/above absolute manipulation extreme\n\n")
            
            swing = stats['swing']
            f.write(f"- **Total Trades:** {swing['total_trades']}\n")
            f.write(f"- **Average Risk:** {swing['avg_risk']:.2f} points\n")
            f.write(f"- **Median Risk:** {swing['median_risk']:.2f} points\n")
            f.write(f"- **Risk Range:** {swing['min_risk']:.2f} - {swing['max_risk']:.2f} points\n\n")
            
            f.write("### Fixed R:R Targets\n\n")
            f.write("| Target | Winrate | Wins/Total |\n")
            f.write("|--------|---------|------------|\n")
            for rr, data in swing['fixed_rr'].items():
                f.write(f"| {rr} | {data['winrate']:.2f}% | {data['wins']}/{data['total']} |\n")
            
            f.write("\n### Dynamic Targets\n\n")
            f.write("| Target | Success Rate | Wins/Total | Avg RR | Median RR |\n")
            f.write("|--------|--------------|------------|--------|------------|\n")
            for target, data in swing['dynamic'].items():
                f.write(f"| {target} | {data['winrate']:.2f}% | {data['wins']}/{data['total']} | "
                       f"{data['avg_rr']:.2f} | {data['median_rr']:.2f} |\n")
            
            f.write("\n---\n\n")
            
            # Strategy 2: Bougie SL
            f.write("## STRATEGY 2: BOUGIE SL (Aggressive)\n\n")
            f.write("**Stop Loss Placement:** Under/above signal candle Low/High\n\n")
            
            bougie = stats['bougie']
            f.write(f"- **Total Trades:** {bougie['total_trades']}\n")
            f.write(f"- **Average Risk:** {bougie['avg_risk']:.2f} points\n")
            f.write(f"- **Median Risk:** {bougie['median_risk']:.2f} points\n")
            f.write(f"- **Risk Range:** {bougie['min_risk']:.2f} - {bougie['max_risk']:.2f} points\n\n")
            
            f.write("### Fixed R:R Targets\n\n")
            f.write("| Target | Winrate | Wins/Total |\n")
            f.write("|--------|---------|------------|\n")
            for rr, data in bougie['fixed_rr'].items():
                f.write(f"| {rr} | {data['winrate']:.2f}% | {data['wins']}/{data['total']} |\n")
            
            f.write("\n### Dynamic Targets\n\n")
            f.write("| Target | Success Rate | Wins/Total | Avg RR | Median RR |\n")
            f.write("|--------|--------------|------------|--------|------------|\n")
            for target, data in bougie['dynamic'].items():
                f.write(f"| {target} | {data['winrate']:.2f}% | {data['wins']}/{data['total']} | "
                       f"{data['avg_rr']:.2f} | {data['median_rr']:.2f} |\n")
            
            f.write("\n---\n\n")
            
            # Comparison & Recommendations
            f.write("## COMPARISON & RECOMMENDATIONS\n\n")
            
            f.write("### Risk Analysis\n\n")
            risk_reduction = ((swing['avg_risk'] - bougie['avg_risk']) / swing['avg_risk']) * 100
            f.write(f"- Bougie SL reduces average risk by **{abs(risk_reduction):.1f}%** ")
            f.write(f"({swing['avg_risk']:.2f} → {bougie['avg_risk']:.2f} points)\n")
            f.write(f"- Risk reduction allows for better position sizing and risk management\n\n")
            
            f.write("### Winrate Comparison\n\n")
            
            f.write("**Fixed R:R Targets:**\n\n")
            for rr in ['1R', '1.5R', '2R', '2.5R']:
                swing_wr = swing['fixed_rr'][rr]['winrate']
                bougie_wr = bougie['fixed_rr'][rr]['winrate']
                diff = bougie_wr - swing_wr
                
                winner = "🟢 Bougie" if diff > 0 else "🔴 Swing" if diff < 0 else "🟡 Tie"
                f.write(f"- **{rr}:** Swing {swing_wr:.2f}% vs Bougie {bougie_wr:.2f}% "
                       f"({diff:+.2f}%) - {winner}\n")
            
            f.write("\n**Dynamic Targets:**\n\n")
            for target in ['Equilibrium', 'Full_Range']:
                swing_wr = swing['dynamic'][target]['winrate']
                bougie_wr = bougie['dynamic'][target]['winrate']
                diff = bougie_wr - swing_wr
                
                winner = "🟢 Bougie" if diff > 0 else "🔴 Swing" if diff < 0 else "🟡 Tie"
                f.write(f"- **{target}:** Swing {swing_wr:.2f}% vs Bougie {bougie_wr:.2f}% "
                       f"({diff:+.2f}%) - {winner}\n")
            
            f.write("\n### Key Insights\n\n")
            
            # Determine which strategy is better
            avg_swing_wr = np.mean([swing['fixed_rr'][rr]['winrate'] for rr in ['1R', '1.5R', '2R', '2.5R']])
            avg_bougie_wr = np.mean([bougie['fixed_rr'][rr]['winrate'] for rr in ['1R', '1.5R', '2R', '2.5R']])
            
            if avg_bougie_wr > avg_swing_wr:
                f.write("1. **Bougie SL strategy outperforms Swing SL** with higher winrates across most targets\n")
                f.write("2. Tighter stop loss (Bougie) improves win probability while reducing capital at risk\n")
                f.write("3. Recommended approach: **Use Bougie SL** for better risk-adjusted returns\n\n")
            else:
                f.write("1. **Swing SL strategy provides more security** with wider stop loss\n")
                f.write("2. Conservative approach reduces false stop-outs during manipulation\n")
                f.write("3. Recommended approach: **Use Swing SL** for more reliable entries\n\n")
            
            # Best target recommendation
            best_rr_swing = max(swing['fixed_rr'].items(), key=lambda x: x[1]['winrate'])
            best_rr_bougie = max(bougie['fixed_rr'].items(), key=lambda x: x[1]['winrate'])
            
            f.write(f"4. **Optimal Take Profit:**\n")
            f.write(f"   - Swing SL: {best_rr_swing[0]} ({best_rr_swing[1]['winrate']:.2f}% winrate)\n")
            f.write(f"   - Bougie SL: {best_rr_bougie[0]} ({best_rr_bougie[1]['winrate']:.2f}% winrate)\n\n")
            
            f.write("5. **Dynamic Targets Analysis:**\n")
            eq_swing = swing['dynamic']['Equilibrium']
            eq_bougie = bougie['dynamic']['Equilibrium']
            f.write(f"   - Equilibrium target offers {eq_swing['avg_rr']:.2f}R average return (Swing) "
                   f"vs {eq_bougie['avg_rr']:.2f}R (Bougie)\n")
            
            fr_swing = swing['dynamic']['Full_Range']
            fr_bougie = bougie['dynamic']['Full_Range']
            f.write(f"   - Full Range target provides {fr_swing['avg_rr']:.2f}R average return (Swing) "
                   f"vs {fr_bougie['avg_rr']:.2f}R (Bougie)\n\n")
            
            f.write("---\n\n")
            f.write("*Report generated by Tokyo-London Session Analysis System*\n")
        
        print(f"Comparison report saved to: {report_file}")
        print("\nBacktest completed successfully!")

def main(run_backtest=False):
    """
    Main execution function
    
    Args:
        run_backtest: If True, runs comprehensive backtest after analysis
    """
    data_dir = "/home/runner/work/Backtest-Trading/Backtest-Trading"
    
    print("\n" + "="*60)
    print("NQ FUTURES - TOKYO & LONDON SESSION ANALYZER")
    print("="*60 + "\n")
    
    try:
        analyzer = TokyoLondonAnalyzer(data_dir)
        analyzer.load_data()
        
        # Check if we should skip analysis and just run backtest
        fvg_file = os.path.join(data_dir, 'tokyo_london_fvg_analysis.csv')
        
        if run_backtest and os.path.exists(fvg_file):
            print("FVG analysis file found. Skipping analysis and running backtest...\n")
        else:
            # Run standard analysis
            analyzer.run_analysis()
            df_results = analyzer.generate_statistics()
            analyzer.generate_velocity_statistics(df_results)
            analyzer.save_results(df_results)
            
            # Run FVG analysis
            analyzer.run_fvg_analysis()
            df_fvg = analyzer.generate_fvg_statistics()
            if df_fvg is not None:
                analyzer.save_fvg_results(df_fvg)
        
        # Run comprehensive backtest if requested
        if run_backtest:
            print("\n" + "="*70)
            print("STARTING COMPREHENSIVE BACKTEST")
            print("="*70 + "\n")
            
            df_swing, df_bougie = analyzer.run_comprehensive_backtest()
            
            if df_swing is not None and df_bougie is not None:
                stats = analyzer.generate_backtest_statistics(df_swing, df_bougie)
                
                if stats is not None:
                    analyzer.save_backtest_results(df_swing, df_bougie, stats)
                    
                    # Print summary to console
                    print("\n" + "="*70)
                    print("BACKTEST SUMMARY")
                    print("="*70 + "\n")
                    
                    print(f"SWING SL Strategy:")
                    print(f"  Total Trades: {stats['swing']['total_trades']}")
                    print(f"  Average Risk: {stats['swing']['avg_risk']:.2f} points")
                    print(f"  1R Winrate: {stats['swing']['fixed_rr']['1R']['winrate']:.2f}%")
                    print(f"  2R Winrate: {stats['swing']['fixed_rr']['2R']['winrate']:.2f}%")
                    print(f"  Equilibrium: {stats['swing']['dynamic']['Equilibrium']['winrate']:.2f}% "
                          f"(Avg RR: {stats['swing']['dynamic']['Equilibrium']['avg_rr']:.2f})")
                    
                    print(f"\nBOUGIE SL Strategy:")
                    print(f"  Total Trades: {stats['bougie']['total_trades']}")
                    print(f"  Average Risk: {stats['bougie']['avg_risk']:.2f} points")
                    print(f"  1R Winrate: {stats['bougie']['fixed_rr']['1R']['winrate']:.2f}%")
                    print(f"  2R Winrate: {stats['bougie']['fixed_rr']['2R']['winrate']:.2f}%")
                    print(f"  Equilibrium: {stats['bougie']['dynamic']['Equilibrium']['winrate']:.2f}% "
                          f"(Avg RR: {stats['bougie']['dynamic']['Equilibrium']['avg_rr']:.2f})")
        
        print("\n" + "="*60)
        print("ANALYSIS COMPLETED SUCCESSFULLY!")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    import sys
    
    # Check if --backtest flag is provided
    run_backtest = '--backtest' in sys.argv
    
    exit(main(run_backtest=run_backtest))

"""
Judas Swing ICT Analysis Script with "Return to Equilibrium" Validation
Analyzes NASDAQ 100 (NQ) historical data to detect "Judas Swing" patterns
according to ICT (Inner Circle Trader) methodology.

This version implements strict validation: the price must return to touch
the Asian Equilibrium level after reaching peak/trough during London Killzone.
"""

import pandas as pd
import os
from datetime import datetime, time, timedelta
import numpy as np

class JudasSwingAnalyzer:
    """
    Analyzer for Judas Swing patterns in NQ futures data.
    """
    
    def __init__(self, base_path):
        """
        Initialize the analyzer with the base path to CSV files.
        
        Args:
            base_path (str): Directory containing the 5-minute CSV files
        """
        self.base_path = base_path
        self.years = range(2018, 2026)  # 2018-2025
        self.data = None
        self.judas_swings = []
        
    def load_data(self):
        """
        Load all 5-minute CSV files from 2018-2025.
        """
        all_data = []
        
        for year in self.years:
            file_path = os.path.join(self.base_path, f"{year} 5m.csv")
            
            if not os.path.exists(file_path):
                print(f"Warning: File not found - {file_path}")
                continue
                
            try:
                # Read CSV with semicolon delimiter, skip header row
                df = pd.read_csv(
                    file_path, 
                    sep=';',
                    skiprows=1,
                    names=['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
                )
                
                # Convert Date and Time to datetime
                df['DateTime'] = pd.to_datetime(
                    df['Date'] + ' ' + df['Time'], 
                    format='%d/%m/%Y %H:%M:%S'
                )
                
                # Convert OHLC to numeric
                df['Open'] = pd.to_numeric(df['Open'])
                df['High'] = pd.to_numeric(df['High'])
                df['Low'] = pd.to_numeric(df['Low'])
                df['Close'] = pd.to_numeric(df['Close'])
                
                all_data.append(df)
                print(f"Loaded {len(df)} rows from {year}")
                
            except Exception as e:
                print(f"Error loading {file_path}: {e}")
                continue
        
        if all_data:
            self.data = pd.concat(all_data, ignore_index=True)
            self.data = self.data.sort_values('DateTime').reset_index(drop=True)
            print(f"\nTotal rows loaded: {len(self.data)}")
        else:
            raise ValueError("No data loaded. Please check file paths.")
    
    def get_session_data(self, date):
        """
        Extract Asian Range, Midnight Open, and London Killzone data for a given trading day.
        
        Args:
            date (datetime.date): The trading day (J)
            
        Returns:
            dict: Session data including Asian range, midnight open, and London killzone
        """
        # Previous day (J-1) for Asian Range and Midnight Open
        prev_date = date - timedelta(days=1)
        
        # Asian Range: 18:00 (J-1) to 23:00 (J-1)
        asian_start = datetime.combine(prev_date, time(18, 0, 0))
        asian_end = datetime.combine(prev_date, time(23, 0, 0))
        
        # Midnight Open: 23:00 (J-1)
        midnight_time = datetime.combine(prev_date, time(23, 0, 0))
        
        # London Killzone: 01:00 (J) to 04:00 (J)
        london_start = datetime.combine(date, time(1, 0, 0))
        london_end = datetime.combine(date, time(4, 0, 0))
        
        # Extract data for each period
        asian_data = self.data[
            (self.data['DateTime'] >= asian_start) & 
            (self.data['DateTime'] < asian_end)
        ].copy()
        
        midnight_data = self.data[self.data['DateTime'] == midnight_time]
        
        london_data = self.data[
            (self.data['DateTime'] >= london_start) & 
            (self.data['DateTime'] <= london_end)
        ].copy()
        
        # Check if we have all required data
        if len(asian_data) == 0 or len(midnight_data) == 0 or len(london_data) == 0:
            return None
        
        # Calculate Asian range
        asian_high = asian_data['High'].max()
        asian_low = asian_data['Low'].min()
        
        # Get Midnight Open
        midnight_open = midnight_data.iloc[0]['Open']
        
        # Get London Killzone data
        london_high = london_data['High'].max()
        london_low = london_data['Low'].min()
        
        # Get the 04:00 close (last candle in London Killzone)
        london_close = london_data.iloc[-1]['Close']
        
        return {
            'date': date,
            'asian_high': asian_high,
            'asian_low': asian_low,
            'midnight_open': midnight_open,
            'london_high': london_high,
            'london_low': london_low,
            'london_close': london_close,
            'london_data': london_data
        }
    
    def detect_judas_swing(self, session_data):
        """
        Detect if a Judas Swing occurred in the given session with "Return to Equilibrium" validation.
        
        Args:
            session_data (dict): Session data from get_session_data()
            
        Returns:
            dict or None: Judas Swing details if detected, None otherwise
        """
        if session_data is None:
            return None
        
        asian_high = session_data['asian_high']
        asian_low = session_data['asian_low']
        midnight_open = session_data['midnight_open']
        london_data = session_data['london_data']
        date = session_data['date']
        
        # Calculate Asian Equilibrium (The Pivot)
        asian_equilibrium = (asian_high + asian_low) / 2
        
        # Skip if Asian Range is zero or too small
        if abs(asian_high - asian_low) < 0.01:
            return None
        
        # Check for Bearish Judas Swing (Bull Trap / Short Setup)
        # 1. Price exceeds Asian High during London Killzone
        # 2. Find the peak (KZ High) with its timestamp
        # 3. After peak, price must return to touch/cross Asian Equilibrium before 04:00
        
        breakout_above = london_data[london_data['High'] > asian_high]
        
        if len(breakout_above) > 0:
            # Find when breakout occurred (T1)
            breakout_time = breakout_above.iloc[0]['DateTime']
            
            # Find the peak after breakout (T2 >= T1)
            data_after_breakout = london_data[london_data['DateTime'] >= breakout_time]
            peak_idx = data_after_breakout['High'].idxmax()
            peak_high = data_after_breakout.loc[peak_idx, 'High']
            peak_time = data_after_breakout.loc[peak_idx, 'DateTime']
            
            # Check if price returns to equilibrium after peak (T > T2)
            data_after_peak = london_data[london_data['DateTime'] > peak_time]
            
            if len(data_after_peak) > 0:
                # Check if any candle touches or crosses equilibrium
                returns_to_eq = data_after_peak[data_after_peak['Low'] <= asian_equilibrium]
                
                if len(returns_to_eq) > 0:
                    # Valid Bearish Judas Swing detected
                    eq_touch_time = returns_to_eq.iloc[0]['DateTime']
                    
                    # Calculate timing metrics (in minutes)
                    london_start = datetime.combine(date, time(1, 0, 0))
                    time_to_peak = (peak_time - london_start).total_seconds() / 60
                    time_to_equilibrium = (eq_touch_time - peak_time).total_seconds() / 60
                    
                    raid_magnitude = peak_high - asian_high
                    
                    return {
                        'date': date,
                        'type': 'Bearish',
                        'direction': 'Short',
                        'asian_high': asian_high,
                        'asian_low': asian_low,
                        'asian_equilibrium': asian_equilibrium,
                        'midnight_open': midnight_open,
                        'kz_extreme': peak_high,
                        'raid_magnitude': raid_magnitude,
                        'time_to_peak': time_to_peak,
                        'time_to_equilibrium': time_to_equilibrium,
                        'peak_time': peak_time,
                        'eq_touch_time': eq_touch_time
                    }
        
        # Check for Bullish Judas Swing (Bear Trap / Long Setup)
        # 1. Price breaks below Asian Low during London Killzone
        # 2. Find the trough (KZ Low) with its timestamp
        # 3. After trough, price must return to touch/cross Asian Equilibrium before 04:00
        
        breakout_below = london_data[london_data['Low'] < asian_low]
        
        if len(breakout_below) > 0:
            # Find when breakout occurred (T1)
            breakout_time = breakout_below.iloc[0]['DateTime']
            
            # Find the trough after breakout (T2 >= T1)
            data_after_breakout = london_data[london_data['DateTime'] >= breakout_time]
            trough_idx = data_after_breakout['Low'].idxmin()
            trough_low = data_after_breakout.loc[trough_idx, 'Low']
            trough_time = data_after_breakout.loc[trough_idx, 'DateTime']
            
            # Check if price returns to equilibrium after trough (T > T2)
            data_after_trough = london_data[london_data['DateTime'] > trough_time]
            
            if len(data_after_trough) > 0:
                # Check if any candle touches or crosses equilibrium
                returns_to_eq = data_after_trough[data_after_trough['High'] >= asian_equilibrium]
                
                if len(returns_to_eq) > 0:
                    # Valid Bullish Judas Swing detected
                    eq_touch_time = returns_to_eq.iloc[0]['DateTime']
                    
                    # Calculate timing metrics (in minutes)
                    london_start = datetime.combine(date, time(1, 0, 0))
                    time_to_peak = (trough_time - london_start).total_seconds() / 60
                    time_to_equilibrium = (eq_touch_time - trough_time).total_seconds() / 60
                    
                    raid_magnitude = asian_low - trough_low
                    
                    return {
                        'date': date,
                        'type': 'Bullish',
                        'direction': 'Long',
                        'asian_high': asian_high,
                        'asian_low': asian_low,
                        'asian_equilibrium': asian_equilibrium,
                        'midnight_open': midnight_open,
                        'kz_extreme': trough_low,
                        'raid_magnitude': raid_magnitude,
                        'time_to_peak': time_to_peak,
                        'time_to_equilibrium': time_to_equilibrium,
                        'peak_time': trough_time,
                        'eq_touch_time': eq_touch_time
                    }
        
        return None
    
    def analyze(self):
        """
        Analyze all trading sessions and detect Judas Swings.
        """
        if self.data is None:
            raise ValueError("No data loaded. Call load_data() first.")
        
        # Get unique trading dates (from the London Killzone perspective, day J)
        # We need dates where we have London Killzone data (01:00-04:00)
        london_dates = self.data[
            (self.data['DateTime'].dt.time >= time(1, 0, 0)) &
            (self.data['DateTime'].dt.time <= time(4, 0, 0))
        ]['DateTime'].dt.date.unique()
        
        print(f"\nAnalyzing {len(london_dates)} trading sessions...")
        
        sessions_analyzed = 0
        
        for date in sorted(london_dates):
            # Skip weekends (Saturday = 5, Sunday = 6)
            if pd.Timestamp(date).dayofweek >= 5:
                continue
            
            try:
                session_data = self.get_session_data(date)
                
                if session_data is None:
                    continue
                
                sessions_analyzed += 1
                
                judas_swing = self.detect_judas_swing(session_data)
                
                if judas_swing is not None:
                    self.judas_swings.append(judas_swing)
                    
            except Exception as e:
                # Skip sessions with errors (likely incomplete data)
                continue
        
        print(f"Sessions analyzed: {sessions_analyzed}")
        print(f"Judas Swings detected: {len(self.judas_swings)}")
    
    def generate_report(self):
        """
        Generate and print a comprehensive analysis report with "Return to Equilibrium" metrics.
        """
        if len(self.judas_swings) == 0:
            print("\nNo Judas Swings detected in the analyzed period.")
            return
        
        # Convert to DataFrame for easier analysis
        df = pd.DataFrame(self.judas_swings)
        df['year'] = pd.to_datetime(df['date']).dt.year
        
        # Calculate statistics
        total_sessions = len(self.data['DateTime'].dt.date.unique())
        total_judas = len(df)
        occurrence_rate = (total_judas / total_sessions * 100) if total_sessions > 0 else 0
        
        long_count = len(df[df['direction'] == 'Long'])
        short_count = len(df[df['direction'] == 'Short'])
        
        avg_raid_magnitude = df['raid_magnitude'].mean()
        max_raid_magnitude = df['raid_magnitude'].max()
        
        # Timing metrics
        avg_time_to_peak = df['time_to_peak'].mean()
        avg_time_to_eq = df['time_to_equilibrium'].mean()
        
        # Yearly analysis
        yearly_stats = df.groupby('year').agg({
            'date': 'count',
            'raid_magnitude': 'mean'
        }).rename(columns={'date': 'count', 'raid_magnitude': 'avg_raid'})
        
        # Print report
        print("\n" + "="*80)
        print(" JUDAS SWING ICT ANALYSIS REPORT - NASDAQ 100 (NQ)")
        print(" WITH 'RETURN TO EQUILIBRIUM' VALIDATION")
        print("="*80)
        
        print("\n1. VALIDATION STATISTICS (Return to Equilibrium)")
        print("-" * 80)
        print(f"   Total Trading Sessions Analyzed:       {total_sessions:,}")
        print(f"   Judas Swings with Eq Return:           {total_judas:,}")
        print(f"   Success Rate 'Return to Eq':           {occurrence_rate:.2f}%")
        print(f"\n   Distribution:")
        print(f"      - Long Setups (Bear Trap):          {long_count:,} ({long_count/total_judas*100:.1f}%)")
        print(f"      - Short Setups (Bull Trap):         {short_count:,} ({short_count/total_judas*100:.1f}%)")
        
        print("\n2. AMPLITUDE ANALYSIS (Stop Run)")
        print("-" * 80)
        print(f"   Average Extension (Raid):              {avg_raid_magnitude:.2f} NQ points")
        print(f"   Maximum Extension:                     {max_raid_magnitude:.2f} NQ points")
        print(f"\n   By Direction:")
        if long_count > 0:
            long_avg = df[df['direction'] == 'Long']['raid_magnitude'].mean()
            long_max = df[df['direction'] == 'Long']['raid_magnitude'].max()
            print(f"      - Bullish (Long) Average:          {long_avg:.2f} points")
            print(f"      - Bullish (Long) Maximum:          {long_max:.2f} points")
        if short_count > 0:
            short_avg = df[df['direction'] == 'Short']['raid_magnitude'].mean()
            short_max = df[df['direction'] == 'Short']['raid_magnitude'].max()
            print(f"      - Bearish (Short) Average:         {short_avg:.2f} points")
            print(f"      - Bearish (Short) Maximum:         {short_max:.2f} points")
        
        print("\n3. TEMPORAL ANALYSIS (Timing)")
        print("-" * 80)
        print(f"   Average Time to Peak:                  {avg_time_to_peak:.1f} minutes")
        print(f"   Average Time to Equilibrium:           {avg_time_to_eq:.1f} minutes")
        print(f"   (Time from peak/trough to Eq touch indicates rejection speed)")
        
        print("\n4. YEARLY BREAKDOWN")
        print("-" * 80)
        print(f"   {'Year':<10} {'Count':<12} {'Rate (%)':<15} {'Avg Raid (pts)':<15}")
        print(f"   {'-'*10} {'-'*12} {'-'*15} {'-'*15}")
        
        # Calculate sessions per year for accurate yearly rates
        for year in sorted(yearly_stats.index):
            count = yearly_stats.loc[year, 'count']
            avg_raid = yearly_stats.loc[year, 'avg_raid']
            
            # Calculate sessions for this year
            year_dates = self.data[
                self.data['DateTime'].dt.year.isin([year, year-1])
            ]['DateTime'].dt.date.unique()
            year_sessions = len([d for d in year_dates if pd.Timestamp(d).year == year])
            
            year_rate = (count / year_sessions * 100) if year_sessions > 0 else 0
            
            print(f"   {year:<10} {int(count):<12} {year_rate:<15.2f} {avg_raid:<15.2f}")
        
        print("\n" + "="*80)
        print(" END OF REPORT")
        print("="*80 + "\n")
    
    def save_results(self, output_file='judas_swing_results.csv'):
        """
        Save detected Judas Swings to a CSV file.
        
        Args:
            output_file (str): Output CSV filename
        """
        if len(self.judas_swings) > 0:
            df = pd.DataFrame(self.judas_swings)
            output_path = os.path.join(self.base_path, output_file)
            df.to_csv(output_path, index=False)
            print(f"Results saved to: {output_path}")
        else:
            print("No results to save.")


def main():
    """
    Main execution function.
    """
    # Set the base path to the directory containing CSV files
    base_path = os.path.dirname(os.path.abspath(__file__))
    
    print("="*80)
    print(" JUDAS SWING ICT ANALYSIS - 'RETURN TO EQUILIBRIUM' VALIDATION")
    print("="*80)
    print(f"\nData Directory: {base_path}")
    print(f"Time Period: 2018-2025")
    print(f"Timeframe: 5-minute")
    print(f"Instrument: NASDAQ 100 (NQ)")
    print("\nTime Periods (Chicago Time / UTC-5):")
    print("  - Asian Session:    18:00 (J-1) to 23:00 (J-1)")
    print("  - London Killzone:  01:00 (J) to 04:00 (J)")
    print("\nValidation Logic:")
    print("  1. Asian Equilibrium = (Asian High + Asian Low) / 2")
    print("  2. Price raids beyond Asian High/Low during London Killzone")
    print("  3. After reaching peak/trough, price MUST return to touch Equilibrium")
    print("  4. Return to Equilibrium must occur BEFORE 04:00")
    print("\n" + "="*80 + "\n")
    
    # Initialize analyzer
    analyzer = JudasSwingAnalyzer(base_path)
    
    # Load data
    print("Loading data...")
    analyzer.load_data()
    
    # Analyze for Judas Swings
    print("\nStarting analysis...")
    analyzer.analyze()
    
    # Generate report
    analyzer.generate_report()
    
    # Save results
    analyzer.save_results()


if __name__ == "__main__":
    main()

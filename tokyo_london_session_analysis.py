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
            'retest_equilibrium_count': 0
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
        
        # Detect manipulation
        manip_low = manipulation_data['Low'].min()
        manip_high = manipulation_data['High'].max()
        
        broke_below = manip_low < tokyo_low
        broke_above = manip_high > tokyo_high
        
        if broke_below and broke_above:
            result['manipulation_type'] = 'Volatile/Both'
            result['manipulation_occurred'] = True
        elif broke_below:
            result['manipulation_type'] = 'Bullish'  # Buy setup
            result['manipulation_occurred'] = True
        elif broke_above:
            result['manipulation_type'] = 'Bearish'  # Sell setup
            result['manipulation_occurred'] = True
        
        # Distribution phase: 02:45 to 05:00
        if result['manipulation_occurred']:
            distribution_data = self.data[
                (self.data['Date'] == date) &
                (self.data['Time'] >= time(2, 45)) &
                (self.data['Time'] < time(5, 0))
            ]
            
            if len(distribution_data) > 0:
                # Count retests based on manipulation type
                if result['manipulation_type'] == 'Bullish':
                    # After breaking below Tokyo Low, count revisits to Low and Equilibrium
                    # Retest of Tokyo Low (support)
                    for idx, row in distribution_data.iterrows():
                        # Price touches or crosses Tokyo Low
                        if row['Low'] <= tokyo_low <= row['High']:
                            result['retest_low_count'] += 1
                        # Price touches or crosses Equilibrium
                        if row['Low'] <= equilibrium <= row['High']:
                            result['retest_equilibrium_count'] += 1
                
                elif result['manipulation_type'] == 'Bearish':
                    # After breaking above Tokyo High, count revisits to High and Equilibrium
                    # Retest of Tokyo High (resistance)
                    for idx, row in distribution_data.iterrows():
                        # Price touches or crosses Tokyo High
                        if row['Low'] <= tokyo_high <= row['High']:
                            result['retest_high_count'] += 1
                        # Price touches or crosses Equilibrium
                        if row['Low'] <= equilibrium <= row['High']:
                            result['retest_equilibrium_count'] += 1
                
                elif result['manipulation_type'] == 'Volatile/Both':
                    # Count all retests for volatile days
                    for idx, row in distribution_data.iterrows():
                        if row['Low'] <= tokyo_low <= row['High']:
                            result['retest_low_count'] += 1
                        if row['Low'] <= tokyo_high <= row['High']:
                            result['retest_high_count'] += 1
                        if row['Low'] <= equilibrium <= row['High']:
                            result['retest_equilibrium_count'] += 1
        
        return result
    
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

def main():
    """Main execution function"""
    data_dir = "/home/runner/work/Backtest-Trading/Backtest-Trading"
    
    print("\n" + "="*60)
    print("NQ FUTURES - TOKYO & LONDON SESSION ANALYZER")
    print("="*60 + "\n")
    
    try:
        analyzer = TokyoLondonAnalyzer(data_dir)
        analyzer.load_data()
        analyzer.run_analysis()
        df_results = analyzer.generate_statistics()
        analyzer.save_results(df_results)
        
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
    exit(main())

#!/usr/bin/env python3
"""
Tokyo Session Trading Strategy Analysis
========================================
Analyzes trading data from 2018-2025 to calculate the probability of price
returning to Tokyo session 50% equilibrium after a breakout during London manipulation zone.

Strategy Rules:
1. Tokyo Session: 19:00 - 00:00 (note High and Low)
2. Equilibrium: 50% of Tokyo range = (High + Low) / 2
3. Manipulation Zone: 02:00 - 02:30 (London session)
4. Trigger Condition: Price breaks Tokyo High or Low during manipulation zone
5. Objective: Calculate probability of price touching 50% level within 6 hours
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import glob
import os
from pathlib import Path

class TokyoSessionAnalyzer:
    def __init__(self, data_directory):
        """Initialize the analyzer with the data directory."""
        self.data_directory = data_directory
        self.all_data = []
        self.results = []
        
    def load_data(self, years=None, timeframes=None):
        """
        Load CSV files for specified years and timeframes.
        
        Args:
            years: List of years to load (default: 2018-2025)
            timeframes: List of timeframes to load (default: ['5m', '15m', '1H'])
        """
        if years is None:
            years = range(2018, 2026)  # 2018-2025
        if timeframes is None:
            timeframes = ['5m', '15m', '1H']
        
        print("Loading data files...")
        for year in years:
            for tf in timeframes:
                filename = f"{year} {tf}.csv"
                filepath = os.path.join(self.data_directory, filename)
                
                if os.path.exists(filepath):
                    print(f"Loading {filename}...")
                    try:
                        df = pd.read_csv(filepath, sep=';', header=0)
                        
                        # Rename columns if they have generic names
                        if 'Column1' in df.columns:
                            df.columns = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
                        
                        # Parse datetime
                        df['DateTime'] = pd.to_datetime(
                            df['Date'] + ' ' + df['Time'], 
                            format='%d/%m/%Y %H:%M:%S',
                            errors='coerce'
                        )
                        
                        # Drop rows with invalid datetime
                        df = df.dropna(subset=['DateTime'])
                        
                        # Sort by datetime
                        df = df.sort_values('DateTime')
                        
                        # Add metadata
                        df['Year'] = year
                        df['Timeframe'] = tf
                        
                        self.all_data.append(df)
                        print(f"  Loaded {len(df)} rows from {filename}")
                        
                    except Exception as e:
                        print(f"  Error loading {filename}: {e}")
                else:
                    print(f"  File not found: {filename}")
        
        if self.all_data:
            # Combine all dataframes
            self.combined_data = pd.concat(self.all_data, ignore_index=True)
            self.combined_data = self.combined_data.sort_values('DateTime')
            print(f"\nTotal data loaded: {len(self.combined_data)} rows")
            print(f"Date range: {self.combined_data['DateTime'].min()} to {self.combined_data['DateTime'].max()}")
        else:
            print("No data loaded!")
            self.combined_data = pd.DataFrame()
    
    def identify_tokyo_session(self, date):
        """
        Identify Tokyo session (19:00-00:00) for a given date.
        Returns High, Low, and Equilibrium of the Tokyo session.
        
        Args:
            date: The date to find Tokyo session for
            
        Returns:
            dict with tokyo_high, tokyo_low, tokyo_eq, start_time, end_time
        """
        # Tokyo session: 19:00 on the given date to 00:00 next day
        tokyo_start = pd.Timestamp(date) + pd.Timedelta(hours=19)
        tokyo_end = tokyo_start + pd.Timedelta(hours=5)  # 19:00 + 5h = 00:00 next day
        
        # Filter data for Tokyo session
        tokyo_data = self.combined_data[
            (self.combined_data['DateTime'] >= tokyo_start) &
            (self.combined_data['DateTime'] <= tokyo_end)
        ]
        
        if len(tokyo_data) == 0:
            return None
        
        tokyo_high = tokyo_data['High'].max()
        tokyo_low = tokyo_data['Low'].min()
        tokyo_eq = (tokyo_high + tokyo_low) / 2
        
        return {
            'tokyo_high': tokyo_high,
            'tokyo_low': tokyo_low,
            'tokyo_eq': tokyo_eq,
            'start_time': tokyo_start,
            'end_time': tokyo_end,
            'data_points': len(tokyo_data)
        }
    
    def identify_manipulation_zone(self, date):
        """
        Identify manipulation zone (02:00-02:30 London session) for the day after Tokyo session.
        
        Args:
            date: The date of Tokyo session
            
        Returns:
            DataFrame with manipulation zone data
        """
        # Manipulation zone is on the next day (after Tokyo session ends)
        next_day = pd.Timestamp(date) + pd.Timedelta(days=1)
        manip_start = next_day + pd.Timedelta(hours=2)  # 02:00
        manip_end = manip_start + pd.Timedelta(minutes=30)  # 02:30
        
        # Filter data for manipulation zone
        manip_data = self.combined_data[
            (self.combined_data['DateTime'] >= manip_start) &
            (self.combined_data['DateTime'] <= manip_end)
        ]
        
        return manip_data, manip_start, manip_end
    
    def check_breakout(self, manip_data, tokyo_high, tokyo_low):
        """
        Check if price breaks Tokyo high or low during manipulation zone.
        
        Args:
            manip_data: DataFrame with manipulation zone data
            tokyo_high: Tokyo session high
            tokyo_low: Tokyo session low
            
        Returns:
            dict with breakout info or None
        """
        if len(manip_data) == 0:
            return None
        
        # Check for high breakout
        high_break = manip_data[manip_data['High'] > tokyo_high]
        # Check for low breakout
        low_break = manip_data[manip_data['Low'] < tokyo_low]
        
        breakout_type = None
        breakout_time = None
        breakout_price = None
        
        if len(high_break) > 0 and len(low_break) > 0:
            # Both breaks occurred - take the first one
            first_high = high_break.iloc[0]['DateTime']
            first_low = low_break.iloc[0]['DateTime']
            
            if first_high < first_low:
                breakout_type = 'HIGH'
                breakout_time = first_high
                breakout_price = high_break.iloc[0]['High']
            else:
                breakout_type = 'LOW'
                breakout_time = first_low
                breakout_price = low_break.iloc[0]['Low']
        elif len(high_break) > 0:
            breakout_type = 'HIGH'
            breakout_time = high_break.iloc[0]['DateTime']
            breakout_price = high_break.iloc[0]['High']
        elif len(low_break) > 0:
            breakout_type = 'LOW'
            breakout_time = low_break.iloc[0]['DateTime']
            breakout_price = low_break.iloc[0]['Low']
        
        if breakout_type:
            return {
                'type': breakout_type,
                'time': breakout_time,
                'price': breakout_price
            }
        
        return None
    
    def check_return_to_equilibrium(self, breakout_time, tokyo_eq, hours=6):
        """
        Check if price returns to touch Tokyo equilibrium within specified hours.
        
        Args:
            breakout_time: Time of breakout
            tokyo_eq: Tokyo equilibrium level (50%)
            hours: Number of hours to check (default: 6)
            
        Returns:
            dict with return info or None
        """
        end_time = breakout_time + pd.Timedelta(hours=hours)
        
        # Get data after breakout within the time window
        future_data = self.combined_data[
            (self.combined_data['DateTime'] > breakout_time) &
            (self.combined_data['DateTime'] <= end_time)
        ]
        
        if len(future_data) == 0:
            return None
        
        # Check if any candle touched the equilibrium
        # Price touches equilibrium if Low <= tokyo_eq <= High
        touches = future_data[
            (future_data['Low'] <= tokyo_eq) &
            (future_data['High'] >= tokyo_eq)
        ]
        
        if len(touches) > 0:
            first_touch = touches.iloc[0]
            time_to_touch = (first_touch['DateTime'] - breakout_time).total_seconds() / 3600
            
            return {
                'touched': True,
                'time': first_touch['DateTime'],
                'time_to_touch_hours': time_to_touch,
                'data_points_checked': len(future_data)
            }
        
        return {
            'touched': False,
            'data_points_checked': len(future_data)
        }
    
    def analyze(self):
        """
        Main analysis function - processes all data and generates results.
        """
        if len(self.combined_data) == 0:
            print("No data to analyze!")
            return
        
        print("\n" + "="*80)
        print("Starting Tokyo Session Analysis")
        print("="*80)
        
        # Get unique dates from the data
        self.combined_data['Date_Only'] = self.combined_data['DateTime'].dt.date
        unique_dates = sorted(self.combined_data['Date_Only'].unique())
        
        print(f"\nAnalyzing {len(unique_dates)} unique dates...")
        
        total_breakouts = 0
        successful_returns = 0
        
        for i, date in enumerate(unique_dates):
            if (i + 1) % 100 == 0:
                print(f"Progress: {i+1}/{len(unique_dates)} dates processed...")
            
            # Step 1: Identify Tokyo session
            tokyo_session = self.identify_tokyo_session(date)
            
            if tokyo_session is None or tokyo_session['data_points'] < 2:
                continue
            
            # Step 2: Identify manipulation zone (next day)
            manip_data, manip_start, manip_end = self.identify_manipulation_zone(date)
            
            if len(manip_data) == 0:
                continue
            
            # Step 3: Check for breakout
            breakout = self.check_breakout(
                manip_data,
                tokyo_session['tokyo_high'],
                tokyo_session['tokyo_low']
            )
            
            if breakout is None:
                continue
            
            total_breakouts += 1
            
            # Step 4: Check if price returns to equilibrium within 6 hours
            return_info = self.check_return_to_equilibrium(
                breakout['time'],
                tokyo_session['tokyo_eq'],
                hours=6
            )
            
            if return_info and return_info['touched']:
                successful_returns += 1
            
            # Store result
            result = {
                'date': date,
                'tokyo_start': tokyo_session['start_time'],
                'tokyo_end': tokyo_session['end_time'],
                'tokyo_high': tokyo_session['tokyo_high'],
                'tokyo_low': tokyo_session['tokyo_low'],
                'tokyo_eq': tokyo_session['tokyo_eq'],
                'tokyo_range': tokyo_session['tokyo_high'] - tokyo_session['tokyo_low'],
                'breakout_type': breakout['type'],
                'breakout_time': breakout['time'],
                'breakout_price': breakout['price'],
                'returned_to_eq': return_info['touched'] if return_info else False,
                'return_time': return_info.get('time') if return_info and return_info['touched'] else None,
                'time_to_return_hours': return_info.get('time_to_touch_hours') if return_info and return_info['touched'] else None
            }
            
            self.results.append(result)
        
        print(f"\nAnalysis complete!")
        print(f"Total dates analyzed: {len(unique_dates)}")
        print(f"Total breakouts detected: {total_breakouts}")
        print(f"Successful returns to equilibrium: {successful_returns}")
        
        if total_breakouts > 0:
            probability = (successful_returns / total_breakouts) * 100
            print(f"\n{'='*80}")
            print(f"PROBABILITY: {probability:.2f}%")
            print(f"{'='*80}")
    
    def generate_report(self, output_file='tokyo_analysis_report.txt'):
        """
        Generate a detailed analysis report.
        
        Args:
            output_file: Name of the output report file
        """
        if not self.results:
            print("No results to report!")
            return
        
        results_df = pd.DataFrame(self.results)
        
        # Calculate statistics
        total_signals = len(results_df)
        successful_returns = results_df['returned_to_eq'].sum()
        probability = (successful_returns / total_signals) * 100 if total_signals > 0 else 0
        
        # Breakdown by breakout type
        high_breaks = results_df[results_df['breakout_type'] == 'HIGH']
        low_breaks = results_df[results_df['breakout_type'] == 'LOW']
        
        high_success = high_breaks['returned_to_eq'].sum()
        low_success = low_breaks['returned_to_eq'].sum()
        
        high_prob = (high_success / len(high_breaks) * 100) if len(high_breaks) > 0 else 0
        low_prob = (low_success / len(low_breaks) * 100) if len(low_breaks) > 0 else 0
        
        # Time to return statistics
        returns_with_time = results_df[results_df['returned_to_eq'] == True]['time_to_return_hours']
        
        # Breakdown by year
        results_df['year'] = pd.to_datetime(results_df['date']).dt.year
        yearly_stats = results_df.groupby('year').agg({
            'returned_to_eq': ['count', 'sum', 'mean']
        })
        
        # Generate report
        report_path = os.path.join(self.data_directory, output_file)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("="*80 + "\n")
            f.write("TOKYO SESSION TRADING STRATEGY ANALYSIS REPORT\n")
            f.write("="*80 + "\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Analysis Period: {results_df['date'].min()} to {results_df['date'].max()}\n")
            f.write("="*80 + "\n\n")
            
            f.write("STRATEGY RULES:\n")
            f.write("-" * 80 + "\n")
            f.write("1. Tokyo Session: 19:00 - 00:00 (identify High and Low)\n")
            f.write("2. Equilibrium: 50% level = (Tokyo High + Tokyo Low) / 2\n")
            f.write("3. Manipulation Zone: 02:00 - 02:30 (London session, next day)\n")
            f.write("4. Trigger: Price breaks Tokyo High or Low during manipulation zone\n")
            f.write("5. Objective: Price returns to touch 50% equilibrium within 6 hours\n")
            f.write("\n" + "="*80 + "\n\n")
            
            f.write("OVERALL RESULTS:\n")
            f.write("-" * 80 + "\n")
            f.write(f"Total Breakout Signals: {total_signals}\n")
            f.write(f"Successful Returns to 50%: {successful_returns}\n")
            f.write(f"Failed Returns: {total_signals - successful_returns}\n")
            f.write(f"\n>>> OVERALL PROBABILITY: {probability:.2f}% <<<\n")
            f.write("\n" + "="*80 + "\n\n")
            
            f.write("BREAKDOWN BY BREAKOUT TYPE:\n")
            f.write("-" * 80 + "\n")
            f.write(f"HIGH Breakouts:\n")
            f.write(f"  Total: {len(high_breaks)}\n")
            f.write(f"  Successful: {high_success}\n")
            f.write(f"  Probability: {high_prob:.2f}%\n\n")
            f.write(f"LOW Breakouts:\n")
            f.write(f"  Total: {len(low_breaks)}\n")
            f.write(f"  Successful: {low_success}\n")
            f.write(f"  Probability: {low_prob:.2f}%\n")
            f.write("\n" + "="*80 + "\n\n")
            
            f.write("TIME TO RETURN STATISTICS (for successful returns):\n")
            f.write("-" * 80 + "\n")
            if len(returns_with_time) > 0:
                f.write(f"Average time to return: {returns_with_time.mean():.2f} hours\n")
                f.write(f"Median time to return: {returns_with_time.median():.2f} hours\n")
                f.write(f"Min time to return: {returns_with_time.min():.2f} hours\n")
                f.write(f"Max time to return: {returns_with_time.max():.2f} hours\n")
                f.write(f"Std deviation: {returns_with_time.std():.2f} hours\n")
            else:
                f.write("No successful returns to calculate statistics.\n")
            f.write("\n" + "="*80 + "\n\n")
            
            f.write("YEARLY BREAKDOWN:\n")
            f.write("-" * 80 + "\n")
            f.write(f"{'Year':<10} {'Total':<10} {'Success':<10} {'Probability':<15}\n")
            f.write("-" * 80 + "\n")
            for year in yearly_stats.index:
                total = int(yearly_stats.loc[year, ('returned_to_eq', 'count')])
                success = int(yearly_stats.loc[year, ('returned_to_eq', 'sum')])
                prob = yearly_stats.loc[year, ('returned_to_eq', 'mean')] * 100
                f.write(f"{year:<10} {total:<10} {success:<10} {prob:.2f}%\n")
            f.write("\n" + "="*80 + "\n\n")
            
            f.write("SAMPLE SIGNALS (First 20):\n")
            f.write("-" * 80 + "\n")
            sample_size = min(20, len(results_df))
            for idx, row in results_df.head(sample_size).iterrows():
                f.write(f"\nSignal #{idx+1}:\n")
                f.write(f"  Date: {row['date']}\n")
                f.write(f"  Tokyo Range: {row['tokyo_low']:.2f} - {row['tokyo_high']:.2f}\n")
                f.write(f"  Tokyo 50% Equilibrium: {row['tokyo_eq']:.2f}\n")
                f.write(f"  Breakout Type: {row['breakout_type']}\n")
                f.write(f"  Breakout Time: {row['breakout_time']}\n")
                f.write(f"  Breakout Price: {row['breakout_price']:.2f}\n")
                f.write(f"  Returned to 50%: {'YES' if row['returned_to_eq'] else 'NO'}\n")
                if row['returned_to_eq']:
                    f.write(f"  Return Time: {row['return_time']}\n")
                    f.write(f"  Time to Return: {row['time_to_return_hours']:.2f} hours\n")
            
            f.write("\n" + "="*80 + "\n")
            f.write("END OF REPORT\n")
            f.write("="*80 + "\n")
        
        print(f"\nDetailed report saved to: {report_path}")
        
        # Also save results to CSV
        csv_path = os.path.join(self.data_directory, 'tokyo_analysis_results.csv')
        results_df.to_csv(csv_path, index=False)
        print(f"Results data saved to: {csv_path}")
        
        # Print summary to console
        print("\n" + "="*80)
        print("SUMMARY")
        print("="*80)
        print(f"Total Signals: {total_signals}")
        print(f"Successful Returns: {successful_returns}")
        print(f"Overall Probability: {probability:.2f}%")
        print(f"\nHigh Breakouts: {len(high_breaks)} (Success: {high_prob:.2f}%)")
        print(f"Low Breakouts: {len(low_breaks)} (Success: {low_prob:.2f}%)")
        
        if len(returns_with_time) > 0:
            print(f"\nAverage time to return: {returns_with_time.mean():.2f} hours")
        print("="*80)


def main():
    """Main execution function."""
    print("="*80)
    print("Tokyo Session Trading Strategy Analyzer")
    print("="*80)
    print("\nThis script analyzes trading data from 2018-2025 to calculate the")
    print("probability of price returning to Tokyo session 50% equilibrium after")
    print("a breakout during the London manipulation zone.")
    print()
    
    # Initialize analyzer
    data_dir = "/home/runner/work/Backtest-Trading/Backtest-Trading"
    analyzer = TokyoSessionAnalyzer(data_dir)
    
    # Load data
    analyzer.load_data(years=range(2018, 2026), timeframes=['5m', '15m', '1H'])
    
    if len(analyzer.combined_data) == 0:
        print("\nERROR: No data loaded. Please check the data files.")
        return
    
    # Run analysis
    analyzer.analyze()
    
    # Generate report
    analyzer.generate_report()
    
    print("\n" + "="*80)
    print("Analysis Complete!")
    print("="*80)


if __name__ == "__main__":
    main()

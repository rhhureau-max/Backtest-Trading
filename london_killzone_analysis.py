#!/usr/bin/env python3
"""
London Killzone Analysis - Judas Swing vs Continuation Pattern Detection

This script analyzes the "London Killzone" (01:00-05:00) behavior to determine
probabilities of "Judas Swing" (false breakout) vs "Continuation" (true breakout) patterns.

Author: Quantitative Trading Analysis
Date: 2025-12-25
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, time, timedelta
import os
import glob
from collections import defaultdict
import warnings

warnings.filterwarnings('ignore')

# Configuration
TIMEFRAME = '5m'  # Using 5-minute data for precision
ASIAN_START = time(19, 0, 0)  # 19:00 previous day
ASIAN_END = time(0, 0, 0)     # 00:00 midnight
MIDNIGHT = time(0, 0, 0)
LONDON_START = time(1, 0, 0)  # 01:00
LONDON_END = time(5, 0, 0)    # 05:00
CONTINUATION_THRESHOLD = 20   # points
REVERSAL_WINDOW = 60          # minutes


class LondonKillzoneAnalyzer:
    """Analyzes London Killzone patterns for Judas Swing and Continuation detection."""
    
    def __init__(self, data_dir='.'):
        """
        Initialize the analyzer.
        
        Args:
            data_dir: Directory containing the CSV files
        """
        self.data_dir = data_dir
        self.results = []
        self.all_data = {}
        
    def load_data(self):
        """Load all 5m CSV files from 2018-2025."""
        print("Loading data files...")
        
        for year in range(2018, 2026):
            filename = os.path.join(self.data_dir, f"{year} {TIMEFRAME}.csv")
            if os.path.exists(filename):
                try:
                    df = pd.read_csv(filename, sep=';', encoding='utf-8')
                    
                    # Parse datetime
                    df['datetime'] = pd.to_datetime(
                        df['Column1'] + ' ' + df['Column2'],
                        format='%d/%m/%Y %H:%M:%S'
                    )
                    
                    # Rename columns for easier access
                    df = df.rename(columns={
                        'Column3': 'Open',
                        'Column4': 'High',
                        'Column5': 'Low',
                        'Column6': 'Close',
                        'Column7': 'Volume'
                    })
                    
                    # Extract time and date
                    df['time'] = df['datetime'].dt.time
                    df['date'] = df['datetime'].dt.date
                    
                    self.all_data[year] = df.sort_values('datetime').reset_index(drop=True)
                    print(f"  Loaded {year}: {len(df)} rows")
                    
                except Exception as e:
                    print(f"  Error loading {year}: {e}")
            else:
                print(f"  File not found: {filename}")
        
        print(f"\nTotal years loaded: {len(self.all_data)}")
        
    def get_asian_range(self, df, target_date):
        """
        Calculate Asian Range (High and Low between 19:00 previous day and 00:00).
        
        Args:
            df: DataFrame with OHLC data
            target_date: The date for which to calculate the Asian range
            
        Returns:
            dict with asian_high, asian_low, midnight_open, or None if insufficient data
        """
        # Get previous day
        prev_date = target_date - timedelta(days=1)
        
        # Filter for Asian session: 19:00 of prev_date to 00:00 of target_date
        asian_mask = (
            ((df['date'] == prev_date) & (df['time'] >= ASIAN_START)) |
            ((df['date'] == target_date) & (df['time'] < LONDON_START) & (df['time'] <= ASIAN_END))
        )
        
        asian_data = df[asian_mask]
        
        if len(asian_data) == 0:
            return None
        
        asian_high = asian_data['High'].max()
        asian_low = asian_data['Low'].min()
        
        # Get midnight open (00:00)
        midnight_mask = (df['date'] == target_date) & (df['time'] == MIDNIGHT)
        midnight_data = df[midnight_mask]
        
        if len(midnight_data) == 0:
            midnight_open = None
        else:
            midnight_open = midnight_data.iloc[0]['Open']
        
        return {
            'asian_high': asian_high,
            'asian_low': asian_low,
            'midnight_open': midnight_open
        }
    
    def get_london_data(self, df, target_date):
        """
        Get London session data (01:00 to 05:00).
        
        Args:
            df: DataFrame with OHLC data
            target_date: The date for which to get London data
            
        Returns:
            DataFrame with London session data
        """
        london_mask = (
            (df['date'] == target_date) &
            (df['time'] >= LONDON_START) &
            (df['time'] < LONDON_END)
        )
        
        return df[london_mask].copy()
    
    def analyze_breakout(self, london_data, asian_high, asian_low):
        """
        Analyze the first breakout during London session.
        
        Args:
            london_data: DataFrame with London session data
            asian_high: Asian range high
            asian_low: Asian range low
            
        Returns:
            dict with analysis results or None
        """
        if len(london_data) == 0:
            return None
        
        # Find first breakout
        breakout_idx = None
        breakout_type = None  # 'high' or 'low'
        
        for idx, row in london_data.iterrows():
            if row['High'] > asian_high and breakout_type is None:
                breakout_idx = idx
                breakout_type = 'high'
                break
            elif row['Low'] < asian_low and breakout_type is None:
                breakout_idx = idx
                breakout_type = 'low'
                break
        
        if breakout_idx is None:
            return None  # No breakout during London session
        
        breakout_row = london_data.loc[breakout_idx]
        breakout_time = breakout_row['time']
        breakout_datetime = breakout_row['datetime']
        
        # Get data for next 60 minutes
        end_time = breakout_datetime + timedelta(minutes=REVERSAL_WINDOW)
        next_hour_mask = (
            (london_data['datetime'] > breakout_datetime) &
            (london_data['datetime'] <= end_time)
        )
        next_hour_data = london_data[next_hour_mask]
        
        if len(next_hour_data) == 0:
            return None  # Not enough data after breakout
        
        # Analyze the pattern
        pattern_type = None
        extension = 0
        reversal_time = None
        
        if breakout_type == 'high':
            # Track how far price went above asian_high
            max_extension = next_hour_data['High'].max() - asian_high
            extension = max_extension
            
            # Check if price returned below asian_high
            returned_below = (next_hour_data['Low'] < asian_high).any()
            
            # Check if price continued for at least 20 points
            sustained_breakout = (next_hour_data['Low'].min() >= asian_high - CONTINUATION_THRESHOLD) and (max_extension >= CONTINUATION_THRESHOLD)
            
            if returned_below:
                pattern_type = 'judas_swing'
                # Find when it returned
                return_idx = next_hour_data[next_hour_data['Low'] < asian_high].index[0]
                reversal_time = london_data.loc[return_idx, 'time']
            elif sustained_breakout:
                pattern_type = 'continuation'
            else:
                pattern_type = 'unclear'
                
        else:  # breakout_type == 'low'
            # Track how far price went below asian_low
            max_extension = asian_low - next_hour_data['Low'].min()
            extension = max_extension
            
            # Check if price returned above asian_low
            returned_above = (next_hour_data['High'] > asian_low).any()
            
            # Check if price continued for at least 20 points
            sustained_breakout = (next_hour_data['High'].max() <= asian_low + CONTINUATION_THRESHOLD) and (max_extension >= CONTINUATION_THRESHOLD)
            
            if returned_above:
                pattern_type = 'judas_swing'
                # Find when it returned
                return_idx = next_hour_data[next_hour_data['High'] > asian_low].index[0]
                reversal_time = london_data.loc[return_idx, 'time']
            elif sustained_breakout:
                pattern_type = 'continuation'
            else:
                pattern_type = 'unclear'
        
        return {
            'breakout_type': breakout_type,
            'breakout_time': breakout_time,
            'pattern_type': pattern_type,
            'extension': extension,
            'reversal_time': reversal_time
        }
    
    def analyze_all_days(self):
        """Analyze all days across all loaded years."""
        print("\nAnalyzing London Killzone patterns...")
        
        for year, df in self.all_data.items():
            print(f"\nProcessing {year}...")
            
            # Get unique dates
            unique_dates = df['date'].unique()
            
            for target_date in unique_dates:
                # Get Asian range
                asian_range = self.get_asian_range(df, target_date)
                
                if asian_range is None:
                    continue
                
                # Get London data
                london_data = self.get_london_data(df, target_date)
                
                if len(london_data) == 0:
                    continue
                
                # Analyze breakout
                analysis = self.analyze_breakout(
                    london_data,
                    asian_range['asian_high'],
                    asian_range['asian_low']
                )
                
                if analysis is None:
                    continue
                
                # Store results
                result = {
                    'year': year,
                    'date': target_date,
                    'asian_high': asian_range['asian_high'],
                    'asian_low': asian_range['asian_low'],
                    'midnight_open': asian_range['midnight_open'],
                    'breakout_type': analysis['breakout_type'],
                    'breakout_time': analysis['breakout_time'],
                    'pattern_type': analysis['pattern_type'],
                    'extension': analysis['extension'],
                    'reversal_time': analysis['reversal_time']
                }
                
                self.results.append(result)
            
            print(f"  Found {len([r for r in self.results if r['year'] == year])} breakout days")
        
        print(f"\nTotal breakout days analyzed: {len(self.results)}")
    
    def calculate_statistics(self):
        """Calculate and display statistics."""
        if len(self.results) == 0:
            print("No results to analyze!")
            return
        
        df_results = pd.DataFrame(self.results)
        
        print("\n" + "=" * 80)
        print("LONDON KILLZONE ANALYSIS - JUDAS SWING vs CONTINUATION")
        print("=" * 80)
        
        # Overall statistics
        print("\n1. OVERALL STATISTICS")
        print("-" * 80)
        
        total_breakouts = len(df_results)
        judas_count = len(df_results[df_results['pattern_type'] == 'judas_swing'])
        continuation_count = len(df_results[df_results['pattern_type'] == 'continuation'])
        unclear_count = len(df_results[df_results['pattern_type'] == 'unclear'])
        
        print(f"Total Breakouts Analyzed: {total_breakouts}")
        print(f"\nJudas Swings: {judas_count} ({judas_count/total_breakouts*100:.1f}%)")
        print(f"Continuations: {continuation_count} ({continuation_count/total_breakouts*100:.1f}%)")
        print(f"Unclear: {unclear_count} ({unclear_count/total_breakouts*100:.1f}%)")
        
        # Statistics by year
        print("\n2. STATISTICS BY YEAR")
        print("-" * 80)
        
        yearly_stats = []
        for year in sorted(df_results['year'].unique()):
            year_data = df_results[df_results['year'] == year]
            total = len(year_data)
            judas = len(year_data[year_data['pattern_type'] == 'judas_swing'])
            cont = len(year_data[year_data['pattern_type'] == 'continuation'])
            unclear = len(year_data[year_data['pattern_type'] == 'unclear'])
            
            yearly_stats.append({
                'Year': year,
                'Total': total,
                'Judas Swing': judas,
                'Judas %': f"{judas/total*100:.1f}%",
                'Continuation': cont,
                'Continuation %': f"{cont/total*100:.1f}%",
                'Unclear': unclear
            })
        
        yearly_df = pd.DataFrame(yearly_stats)
        print(yearly_df.to_string(index=False))
        
        # Judas Swing timing analysis
        print("\n3. JUDAS SWING TIMING ANALYSIS")
        print("-" * 80)
        
        judas_data = df_results[df_results['pattern_type'] == 'judas_swing']
        if len(judas_data) > 0 and judas_data['reversal_time'].notna().any():
            reversal_times = judas_data['reversal_time'].dropna()
            
            # Convert times to hours for analysis
            reversal_hours = [t.hour + t.minute/60 for t in reversal_times]
            
            if len(reversal_hours) > 0:
                print(f"Average Reversal Time: {np.mean(reversal_hours):.2f} hours (24h format)")
                print(f"Most Common Reversal Hour: {pd.Series([t.hour for t in reversal_times]).mode().values[0]:02d}:00")
                
                # Distribution by half-hour
                reversal_bins = defaultdict(int)
                for t in reversal_times:
                    hour = t.hour
                    half = "00" if t.minute < 30 else "30"
                    reversal_bins[f"{hour:02d}:{half}"] += 1
                
                print("\nReversal Time Distribution:")
                for time_bin in sorted(reversal_bins.keys()):
                    count = reversal_bins[time_bin]
                    pct = count / len(reversal_times) * 100
                    print(f"  {time_bin}: {count} ({pct:.1f}%)")
        
        # Extension analysis
        print("\n4. EXTENSION ANALYSIS")
        print("-" * 80)
        
        for pattern in ['judas_swing', 'continuation']:
            pattern_data = df_results[df_results['pattern_type'] == pattern]
            if len(pattern_data) > 0:
                extensions = pattern_data['extension']
                print(f"\n{pattern.replace('_', ' ').title()}:")
                print(f"  Average Extension: {extensions.mean():.2f} points")
                print(f"  Std Dev: {extensions.std():.2f} points")
                print(f"  Min Extension: {extensions.min():.2f} points")
                print(f"  Max Extension: {extensions.max():.2f} points")
                print(f"  Median Extension: {extensions.median():.2f} points")
        
        # Breakout direction analysis
        print("\n5. BREAKOUT DIRECTION ANALYSIS")
        print("-" * 80)
        
        high_breaks = len(df_results[df_results['breakout_type'] == 'high'])
        low_breaks = len(df_results[df_results['breakout_type'] == 'low'])
        
        print(f"High Breakouts: {high_breaks} ({high_breaks/total_breakouts*100:.1f}%)")
        print(f"Low Breakouts: {low_breaks} ({low_breaks/total_breakouts*100:.1f}%)")
        
        # Pattern by breakout direction
        for direction in ['high', 'low']:
            dir_data = df_results[df_results['breakout_type'] == direction]
            if len(dir_data) > 0:
                judas = len(dir_data[dir_data['pattern_type'] == 'judas_swing'])
                cont = len(dir_data[dir_data['pattern_type'] == 'continuation'])
                print(f"\n{direction.title()} Breakouts:")
                print(f"  Judas Swing: {judas} ({judas/len(dir_data)*100:.1f}%)")
                print(f"  Continuation: {cont} ({cont/len(dir_data)*100:.1f}%)")
        
        return df_results
    
    def create_visualizations(self, df_results):
        """Create visualization charts."""
        print("\n6. GENERATING VISUALIZATIONS")
        print("-" * 80)
        
        if len(df_results) == 0:
            print("No data to visualize!")
            return
        
        # Set style
        sns.set_style("whitegrid")
        
        # Create figure with subplots
        fig = plt.figure(figsize=(16, 12))
        
        # 1. Yearly Pattern Distribution
        ax1 = plt.subplot(2, 3, 1)
        yearly_data = df_results.groupby(['year', 'pattern_type']).size().unstack(fill_value=0)
        yearly_data.plot(kind='bar', stacked=False, ax=ax1, 
                        color=['#e74c3c', '#2ecc71', '#95a5a6'])
        ax1.set_title('Pattern Distribution by Year', fontsize=12, fontweight='bold')
        ax1.set_xlabel('Year')
        ax1.set_ylabel('Count')
        ax1.legend(title='Pattern Type', labels=['Continuation', 'Judas Swing', 'Unclear'])
        ax1.tick_params(axis='x', rotation=45)
        
        # 2. Overall Pattern Percentage
        ax2 = plt.subplot(2, 3, 2)
        pattern_counts = df_results['pattern_type'].value_counts()
        colors = {'judas_swing': '#e74c3c', 'continuation': '#2ecc71', 'unclear': '#95a5a6'}
        colors_list = [colors.get(x, '#95a5a6') for x in pattern_counts.index]
        ax2.pie(pattern_counts.values, labels=[x.replace('_', ' ').title() for x in pattern_counts.index],
               autopct='%1.1f%%', colors=colors_list, startangle=90)
        ax2.set_title('Overall Pattern Distribution', fontsize=12, fontweight='bold')
        
        # 3. Reversal Time Distribution (for Judas Swings)
        ax3 = plt.subplot(2, 3, 3)
        judas_data = df_results[df_results['pattern_type'] == 'judas_swing']
        if len(judas_data) > 0 and judas_data['reversal_time'].notna().any():
            reversal_times = judas_data['reversal_time'].dropna()
            reversal_hours = [t.hour + t.minute/60 for t in reversal_times]
            ax3.hist(reversal_hours, bins=20, color='#e74c3c', edgecolor='black', alpha=0.7)
            ax3.set_title('Judas Swing Reversal Time Distribution', fontsize=12, fontweight='bold')
            ax3.set_xlabel('Hour of Day (24h)')
            ax3.set_ylabel('Frequency')
            ax3.axvline(np.mean(reversal_hours), color='red', linestyle='--', 
                       label=f'Mean: {np.mean(reversal_hours):.2f}h')
            ax3.legend()
        else:
            ax3.text(0.5, 0.5, 'No reversal time data', ha='center', va='center')
            ax3.set_title('Judas Swing Reversal Time Distribution', fontsize=12, fontweight='bold')
        
        # 4. Extension Distribution
        ax4 = plt.subplot(2, 3, 4)
        judas_ext = df_results[df_results['pattern_type'] == 'judas_swing']['extension']
        cont_ext = df_results[df_results['pattern_type'] == 'continuation']['extension']
        
        if len(judas_ext) > 0:
            ax4.hist(judas_ext, bins=30, alpha=0.6, label='Judas Swing', color='#e74c3c', edgecolor='black')
        if len(cont_ext) > 0:
            ax4.hist(cont_ext, bins=30, alpha=0.6, label='Continuation', color='#2ecc71', edgecolor='black')
        
        ax4.set_title('Extension Distribution (Points)', fontsize=12, fontweight='bold')
        ax4.set_xlabel('Extension (Points)')
        ax4.set_ylabel('Frequency')
        ax4.legend()
        ax4.axvline(CONTINUATION_THRESHOLD, color='blue', linestyle='--', 
                   label=f'Threshold: {CONTINUATION_THRESHOLD}pts')
        
        # 5. Breakout Direction vs Pattern
        ax5 = plt.subplot(2, 3, 5)
        direction_pattern = df_results.groupby(['breakout_type', 'pattern_type']).size().unstack(fill_value=0)
        direction_pattern.plot(kind='bar', ax=ax5, color=['#e74c3c', '#2ecc71', '#95a5a6'])
        ax5.set_title('Pattern Type by Breakout Direction', fontsize=12, fontweight='bold')
        ax5.set_xlabel('Breakout Direction')
        ax5.set_ylabel('Count')
        ax5.legend(title='Pattern', labels=['Continuation', 'Judas Swing', 'Unclear'])
        ax5.tick_params(axis='x', rotation=0)
        
        # 6. Monthly Pattern Distribution
        ax6 = plt.subplot(2, 3, 6)
        df_results['month'] = pd.to_datetime(df_results['date']).dt.month
        monthly_pattern = df_results.groupby('month')['pattern_type'].value_counts().unstack(fill_value=0)
        monthly_pattern.plot(kind='bar', stacked=True, ax=ax6, 
                            color=['#e74c3c', '#2ecc71', '#95a5a6'])
        ax6.set_title('Pattern Distribution by Month', fontsize=12, fontweight='bold')
        ax6.set_xlabel('Month')
        ax6.set_ylabel('Count')
        ax6.legend(title='Pattern', labels=['Continuation', 'Judas Swing', 'Unclear'])
        ax6.tick_params(axis='x', rotation=0)
        
        plt.tight_layout()
        
        # Save figure
        output_file = os.path.join(self.data_dir, 'london_killzone_analysis.png')
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Visualization saved to: {output_file}")
        
        # Show plot
        # plt.show()  # Commented out for automated runs
        plt.close()
    
    def save_results(self, df_results):
        """Save results to CSV."""
        print("\n7. SAVING RESULTS")
        print("-" * 80)
        
        output_file = os.path.join(self.data_dir, 'london_killzone_results.csv')
        df_results.to_csv(output_file, index=False)
        print(f"Results saved to: {output_file}")
        
        # Save summary statistics
        summary_file = os.path.join(self.data_dir, 'london_killzone_summary.csv')
        
        summary_data = []
        for year in sorted(df_results['year'].unique()):
            year_data = df_results[df_results['year'] == year]
            total = len(year_data)
            judas = len(year_data[year_data['pattern_type'] == 'judas_swing'])
            cont = len(year_data[year_data['pattern_type'] == 'continuation'])
            unclear = len(year_data[year_data['pattern_type'] == 'unclear'])
            
            summary_data.append({
                'Year': year,
                'Total_Breakouts': total,
                'Judas_Swing_Count': judas,
                'Judas_Swing_Percentage': f"{judas/total*100:.1f}",
                'Continuation_Count': cont,
                'Continuation_Percentage': f"{cont/total*100:.1f}",
                'Unclear_Count': unclear,
                'Unclear_Percentage': f"{unclear/total*100:.1f}"
            })
        
        summary_df = pd.DataFrame(summary_data)
        summary_df.to_csv(summary_file, index=False)
        print(f"Summary statistics saved to: {summary_file}")
    
    def run_analysis(self):
        """Run the complete analysis pipeline."""
        print("=" * 80)
        print("LONDON KILLZONE ANALYSIS")
        print("Judas Swing vs Continuation Pattern Detection")
        print("=" * 80)
        
        # Load data
        self.load_data()
        
        if len(self.all_data) == 0:
            print("\nERROR: No data loaded! Please check the data directory.")
            return
        
        # Analyze all days
        self.analyze_all_days()
        
        if len(self.results) == 0:
            print("\nWARNING: No breakout patterns found!")
            return
        
        # Calculate statistics
        df_results = self.calculate_statistics()
        
        # Create visualizations
        self.create_visualizations(df_results)
        
        # Save results
        self.save_results(df_results)
        
        print("\n" + "=" * 80)
        print("ANALYSIS COMPLETE")
        print("=" * 80)


def main():
    """Main entry point."""
    # Set data directory (repository root)
    data_dir = '/home/runner/work/Backtest-Trading/Backtest-Trading'
    
    # Create analyzer
    analyzer = LondonKillzoneAnalyzer(data_dir)
    
    # Run analysis
    analyzer.run_analysis()


if __name__ == '__main__':
    main()

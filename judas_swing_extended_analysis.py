#!/usr/bin/env python3
"""
Additional Analysis: Generate summary statistics and visualizations for Judas Swings
"""

import pandas as pd
import numpy as np
from datetime import datetime

def analyze_by_year():
    """Analyze Judas Swings by year"""
    df = pd.read_csv('judas_swing_results.csv')
    df['year'] = pd.to_datetime(df['date']).dt.year
    
    print("\n" + "="*80)
    print("YEARLY BREAKDOWN OF JUDAS SWINGS")
    print("="*80)
    
    for year in sorted(df['year'].unique()):
        year_data = df[df['year'] == year]
        bullish = year_data[year_data['direction'] == 'bullish']
        bearish = year_data[year_data['direction'] == 'bearish']
        
        print(f"\n{year}:")
        print(f"  Total Swings: {len(year_data)}")
        print(f"  Bullish: {len(bullish)} ({len(bullish)/len(year_data)*100:.1f}%)")
        print(f"  Bearish: {len(bearish)} ({len(bearish)/len(year_data)*100:.1f}%)")
        print(f"  Avg Amplitude: {year_data['amplitude'].mean():.2f} points")
        print(f"  Median Amplitude: {year_data['amplitude'].median():.2f} points")
        print(f"  Max Amplitude: {year_data['amplitude'].max():.2f} points")


def analyze_by_month():
    """Analyze patterns by month"""
    df = pd.read_csv('judas_swing_results.csv')
    df['datetime'] = pd.to_datetime(df['date'])
    df['month'] = df['datetime'].dt.month
    df['month_name'] = df['datetime'].dt.month_name()
    
    print("\n" + "="*80)
    print("MONTHLY PATTERNS (All Years Combined)")
    print("="*80)
    
    for month in range(1, 13):
        month_data = df[df['month'] == month]
        if len(month_data) > 0:
            month_name = month_data.iloc[0]['month_name']
            bullish = month_data[month_data['direction'] == 'bullish']
            
            print(f"\n{month_name}:")
            print(f"  Total Swings: {len(month_data)}")
            print(f"  Bullish: {len(bullish)} ({len(bullish)/len(month_data)*100:.1f}%)")
            print(f"  Avg Amplitude: {month_data['amplitude'].mean():.2f} points")


def analyze_amplitude_percentiles():
    """Analyze amplitude percentiles"""
    df = pd.read_csv('judas_swing_results.csv')
    
    print("\n" + "="*80)
    print("AMPLITUDE PERCENTILES (NQ Points)")
    print("="*80)
    
    percentiles = [10, 25, 50, 75, 90, 95, 99]
    
    print("\nAll Swings:")
    for p in percentiles:
        value = np.percentile(df['amplitude'], p)
        print(f"  {p}th percentile: {value:.2f} points")
    
    bullish = df[df['direction'] == 'bullish']
    if len(bullish) > 0:
        print("\nBullish Manipulations:")
        for p in percentiles:
            value = np.percentile(bullish['amplitude'], p)
            print(f"  {p}th percentile: {value:.2f} points")
    
    bearish = df[df['direction'] == 'bearish']
    if len(bearish) > 0:
        print("\nBearish Manipulations:")
        for p in percentiles:
            value = np.percentile(bearish['amplitude'], p)
            print(f"  {p}th percentile: {value:.2f} points")


def analyze_tokyo_range_correlation():
    """Analyze correlation between Tokyo Range and manipulation amplitude"""
    df = pd.read_csv('judas_swing_results.csv')
    
    print("\n" + "="*80)
    print("TOKYO RANGE vs MANIPULATION AMPLITUDE")
    print("="*80)
    
    correlation = df['tokyo_range'].corr(df['amplitude'])
    print(f"\nCorrelation coefficient: {correlation:.4f}")
    
    # Group by Tokyo Range buckets
    range_buckets = [0, 10, 20, 30, 40, 50, 100, float('inf')]
    range_labels = ['0-10', '10-20', '20-30', '30-40', '40-50', '50-100', '100+']
    
    df['range_bucket'] = pd.cut(df['tokyo_range'], bins=range_buckets, labels=range_labels)
    
    print("\nAverage Manipulation Amplitude by Tokyo Range:")
    for bucket in range_labels:
        bucket_data = df[df['range_bucket'] == bucket]
        if len(bucket_data) > 0:
            avg_amp = bucket_data['amplitude'].mean()
            print(f"  Tokyo Range {bucket:>8} points: Avg manipulation {avg_amp:6.2f} points ({len(bucket_data)} swings)")


def main():
    """Run all additional analyses"""
    print("="*80)
    print("JUDAS SWING EXTENDED ANALYSIS")
    print("Additional Statistical Insights")
    print("="*80)
    
    analyze_by_year()
    analyze_by_month()
    analyze_amplitude_percentiles()
    analyze_tokyo_range_correlation()
    
    print("\n" + "="*80)
    print("Extended analysis complete.")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Analysis script for backtest results.
This script provides additional analysis and visualizations of the backtest results.
"""

import pandas as pd
import os


def load_results(results_file='backtest_results.csv'):
    """Load the backtest results."""
    if not os.path.exists(results_file):
        print(f"Results file not found: {results_file}")
        print("Please run backtest_strategy.py first to generate results.")
        return None
    
    return pd.read_csv(results_file)


def analyze_by_year(df):
    """Analyze results by year."""
    df['Year'] = pd.to_datetime(df['Date'], format='%d/%m/%Y').dt.year
    
    print("\n" + "="*80)
    print("ANALYSIS BY YEAR")
    print("="*80)
    
    year_summary = df.groupby(['Year', 'Timeframe', 'Candle_Type']).size().unstack(fill_value=0)
    print("\nTrades per Year by Timeframe and Type:")
    print(year_summary)
    
    print("\nTotal trades per year:")
    print(df.groupby('Year').size())


def analyze_by_month(df):
    """Analyze results by month."""
    df['Date_parsed'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')
    df['Month'] = df['Date_parsed'].dt.month
    df['MonthName'] = df['Date_parsed'].dt.strftime('%B')
    
    print("\n" + "="*80)
    print("ANALYSIS BY MONTH")
    print("="*80)
    
    monthly_summary = df.groupby(['MonthName', 'Candle_Type']).size().unstack(fill_value=0)
    print("\nTrades per Month:")
    print(monthly_summary)
    
    # Sort by month number for correct ordering
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
                   'July', 'August', 'September', 'October', 'November', 'December']
    monthly_summary = monthly_summary.reindex([m for m in month_order if m in monthly_summary.index])
    
    print("\nTotal trades per month (ordered):")
    print(monthly_summary.sum(axis=1))


def analyze_price_levels(df):
    """Analyze price levels and breakout magnitudes."""
    print("\n" + "="*80)
    print("PRICE LEVEL ANALYSIS")
    print("="*80)
    
    # Calculate breakout magnitude
    df['Breakout_Magnitude'] = abs(df['Close'] - df['Reference_Level'])
    df['Breakout_Percentage'] = (df['Breakout_Magnitude'] / df['Reference_Level']) * 100
    
    print("\nAverage Breakout Magnitude by Timeframe and Type:")
    breakout_stats = df.groupby(['Timeframe', 'Candle_Type'])['Breakout_Magnitude'].agg(['mean', 'median', 'max'])
    print(breakout_stats)
    
    print("\nAverage Breakout Percentage by Timeframe and Type:")
    breakout_pct_stats = df.groupby(['Timeframe', 'Candle_Type'])['Breakout_Percentage'].agg(['mean', 'median', 'max'])
    print(breakout_pct_stats)


def analyze_candle_characteristics(df):
    """Analyze candle characteristics."""
    print("\n" + "="*80)
    print("CANDLE CHARACTERISTICS")
    print("="*80)
    
    # Calculate candle range
    df['Candle_Range'] = df['High'] - df['Low']
    df['Body_Size'] = abs(df['Close'] - df['Open'])
    df['Body_to_Range_Ratio'] = df['Body_Size'] / df['Candle_Range']
    
    print("\nAverage Candle Range by Timeframe:")
    print(df.groupby('Timeframe')['Candle_Range'].agg(['mean', 'median']))
    
    print("\nAverage Body-to-Range Ratio by Candle Type:")
    print(df.groupby('Candle_Type')['Body_to_Range_Ratio'].agg(['mean', 'median']))


def generate_summary_report(df):
    """Generate a comprehensive summary report."""
    print("\n" + "="*80)
    print("COMPREHENSIVE SUMMARY REPORT")
    print("="*80)
    
    print(f"\nTotal Trades Analyzed: {len(df)}")
    print(f"Date Range: {df['Date'].min()} to {df['Date'].max()}")
    
    print("\n" + "-"*80)
    print("Distribution Summary:")
    print("-"*80)
    print(f"\nTimeframes analyzed: {', '.join(df['Timeframe'].unique())}")
    print(f"Bullish trades: {len(df[df['Candle_Type'] == 'BULLISH'])} ({len(df[df['Candle_Type'] == 'BULLISH'])/len(df)*100:.1f}%)")
    print(f"Bearish trades: {len(df[df['Candle_Type'] == 'BEARISH'])} ({len(df[df['Candle_Type'] == 'BEARISH'])/len(df)*100:.1f}%)")
    
    print("\n" + "-"*80)
    print("Price Statistics:")
    print("-"*80)
    print(f"\nPrice range: {df['Close'].min():.2f} to {df['Close'].max():.2f}")
    print(f"Average close price: {df['Close'].mean():.2f}")
    print(f"Median close price: {df['Close'].median():.2f}")


def main():
    """Main execution function."""
    print("="*80)
    print("BACKTEST RESULTS ANALYSIS")
    print("="*80)
    
    # Load results
    df = load_results()
    
    if df is None:
        return
    
    print(f"\nLoaded {len(df)} trades from backtest results")
    
    # Run analyses
    analyze_by_year(df)
    analyze_by_month(df)
    analyze_price_levels(df)
    analyze_candle_characteristics(df)
    generate_summary_report(df)
    
    print("\n" + "="*80)
    print("Analysis complete!")
    print("="*80)


if __name__ == "__main__":
    main()

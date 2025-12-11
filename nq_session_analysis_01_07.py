#!/usr/bin/env python3
"""
NQ Session Analysis: 01:00-07:00 Time Window
Analyzes price action and volatility for the 01:00-07:00 session on NQ futures.

Author: Quantitative Analyst Senior
Date: 2025-12-11
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, time
import glob
import os

# Configuration
DATA_TIMEFRAME = '5m'  # Using 5-minute data for precision
SESSION_START = time(1, 0)  # 01:00
SESSION_END = time(7, 0)    # 07:00
BASE_PATH = '/home/runner/work/Backtest-Trading/Backtest-Trading'

# Set plotting style
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (14, 8)


def load_nq_data(years=None):
    """
    Load NQ 5-minute data from CSV files.
    
    Args:
        years: List of years to load. If None, loads all available years.
    
    Returns:
        DataFrame with combined data from all years
    """
    if years is None:
        # Load all years from 2018 to 2025
        years = range(2018, 2026)
    
    all_data = []
    
    for year in years:
        file_path = os.path.join(BASE_PATH, f"{year} {DATA_TIMEFRAME}.csv")
        if not os.path.exists(file_path):
            print(f"Warning: File not found for year {year}")
            continue
        
        print(f"Loading data for {year}...")
        df = pd.read_csv(file_path, sep=';')
        
        # Parse datetime from Column1 (date) and Column2 (time)
        df['datetime'] = pd.to_datetime(df['Column1'] + ' ' + df['Column2'], 
                                       format='%d/%m/%Y %H:%M:%S')
        
        # Rename columns to standard names
        df = df.rename(columns={
            'Column3': 'Open',
            'Column4': 'High',
            'Column5': 'Low',
            'Column6': 'Close',
            'Column7': 'Volume'
        })
        
        df['Date'] = df['datetime'].dt.date
        df['Time'] = df['datetime'].dt.time
        df['Year'] = df['datetime'].dt.year
        df['DayOfWeek'] = df['datetime'].dt.day_name()
        
        all_data.append(df[['datetime', 'Date', 'Time', 'Year', 'DayOfWeek', 
                            'Open', 'High', 'Low', 'Close', 'Volume']])
    
    if not all_data:
        raise ValueError("No data files found!")
    
    combined_df = pd.concat(all_data, ignore_index=True)
    combined_df = combined_df.sort_values('datetime').reset_index(drop=True)
    
    print(f"\nTotal records loaded: {len(combined_df):,}")
    print(f"Date range: {combined_df['datetime'].min()} to {combined_df['datetime'].max()}")
    
    return combined_df


def filter_session_data(df, start_time, end_time):
    """
    Filter data for the specified session time window (01:00 to 07:00).
    
    Args:
        df: DataFrame with NQ data
        start_time: Session start time
        end_time: Session end time
    
    Returns:
        DataFrame filtered for session times only
    """
    # Filter for times within the session window
    session_df = df[(df['Time'] >= start_time) & (df['Time'] < end_time)].copy()
    
    print(f"\nSession records (01:00-07:00): {len(session_df):,}")
    
    return session_df


def create_session_aggregates(session_df):
    """
    Aggregate 5-minute data into daily sessions (01:00-07:00).
    
    For each session:
    - Open: First candle's open (01:00)
    - High: Highest high of all candles
    - Low: Lowest low of all candles
    - Close: Last candle's close (06:55 or nearest to 07:00)
    - Track when High and Low occurred
    
    Returns:
        DataFrame with one row per session
    """
    sessions = []
    
    for date, group in session_df.groupby('Date'):
        if len(group) == 0:
            continue
        
        # Sort by time to ensure correct ordering
        group = group.sort_values('datetime')
        
        # Session OHLC
        session_open = group.iloc[0]['Open']
        session_high = group['High'].max()
        session_low = group['Low'].min()
        session_close = group.iloc[-1]['Close']
        session_volume = group['Volume'].sum()
        
        # Find when high and low occurred
        high_idx = group['High'].idxmax()
        low_idx = group['Low'].idxmin()
        high_time = group.loc[high_idx, 'Time']
        low_time = group.loc[low_idx, 'Time']
        
        # Get first candle info (01:00 candle)
        first_candle_bullish = group.iloc[0]['Close'] > group.iloc[0]['Open']
        
        sessions.append({
            'Date': date,
            'Year': group.iloc[0]['Year'],
            'DayOfWeek': group.iloc[0]['DayOfWeek'],
            'Session_Open': session_open,
            'Session_High': session_high,
            'Session_Low': session_low,
            'Session_Close': session_close,
            'Session_Volume': session_volume,
            'High_Time': high_time,
            'Low_Time': low_time,
            'First_Candle_Bullish': first_candle_bullish,
            'Num_Candles': len(group)
        })
    
    sessions_df = pd.DataFrame(sessions)
    
    # Calculate derived metrics
    sessions_df['Range'] = sessions_df['Session_High'] - sessions_df['Session_Low']
    sessions_df['Session_Return'] = sessions_df['Session_Close'] - sessions_df['Session_Open']
    sessions_df['Is_Bullish'] = sessions_df['Session_Return'] > 0
    
    print(f"\nTotal sessions analyzed: {len(sessions_df)}")
    
    return sessions_df


def analyze_directionality(sessions_df):
    """
    Analysis 1: Return Distribution (Directionality)
    """
    print("\n" + "="*80)
    print("ANALYSIS 1: RETURN DISTRIBUTION (DIRECTIONALITY)")
    print("="*80)
    
    total_sessions = len(sessions_df)
    bullish_sessions = sessions_df['Is_Bullish'].sum()
    bearish_sessions = total_sessions - bullish_sessions
    
    pct_bullish = (bullish_sessions / total_sessions) * 100
    pct_bearish = (bearish_sessions / total_sessions) * 100
    
    avg_return = sessions_df['Session_Return'].mean()
    avg_bullish_return = sessions_df[sessions_df['Is_Bullish']]['Session_Return'].mean()
    avg_bearish_return = sessions_df[~sessions_df['Is_Bullish']]['Session_Return'].mean()
    
    print(f"\nTotal Sessions: {total_sessions}")
    print(f"Bullish Sessions (Close > Open): {bullish_sessions} ({pct_bullish:.2f}%)")
    print(f"Bearish Sessions (Close < Open): {bearish_sessions} ({pct_bearish:.2f}%)")
    print(f"\nAverage Session Performance: {avg_return:.2f} points")
    print(f"Average Bullish Session: {avg_bullish_return:.2f} points")
    print(f"Average Bearish Session: {avg_bearish_return:.2f} points")
    
    return {
        'total_sessions': total_sessions,
        'bullish_sessions': bullish_sessions,
        'bearish_sessions': bearish_sessions,
        'pct_bullish': pct_bullish,
        'pct_bearish': pct_bearish,
        'avg_return': avg_return,
        'avg_bullish_return': avg_bullish_return,
        'avg_bearish_return': avg_bearish_return
    }


def analyze_volatility(sessions_df):
    """
    Analysis 2: Volatility and Range
    """
    print("\n" + "="*80)
    print("ANALYSIS 2: VOLATILITY AND RANGE")
    print("="*80)
    
    avg_range = sessions_df['Range'].mean()
    median_range = sessions_df['Range'].median()
    std_range = sessions_df['Range'].std()
    
    print(f"\nAverage Session Range: {avg_range:.2f} points")
    print(f"Median Session Range: {median_range:.2f} points")
    print(f"Std Dev Range: {std_range:.2f} points")
    
    # Volatility evolution by year
    print("\n--- Volatility Evolution by Year ---")
    yearly_stats = sessions_df.groupby('Year').agg({
        'Range': ['mean', 'median', 'std', 'count']
    }).round(2)
    yearly_stats.columns = ['Avg Range', 'Median Range', 'Std Dev', 'Sessions']
    print(yearly_stats)
    
    return {
        'avg_range': avg_range,
        'median_range': median_range,
        'std_range': std_range,
        'yearly_stats': yearly_stats
    }


def time_to_minutes_since_start(t):
    """Convert time to minutes since 01:00"""
    return (t.hour - 1) * 60 + t.minute


def analyze_extreme_timing(sessions_df):
    """
    Analysis 3: Extreme Timing (When do Highs and Lows occur?)
    """
    print("\n" + "="*80)
    print("ANALYSIS 3: EXTREME TIMING (HIGH/LOW OCCURRENCE)")
    print("="*80)
    
    # Convert times to minutes since session start (01:00 = 0 minutes)
    sessions_df['High_Minutes'] = sessions_df['High_Time'].apply(time_to_minutes_since_start)
    sessions_df['Low_Minutes'] = sessions_df['Low_Time'].apply(time_to_minutes_since_start)
    
    # Create 15-minute bins
    bins = list(range(0, 361, 15))  # 0 to 360 minutes (6 hours) in 15-minute intervals
    bin_labels = [f"{1 + i//60:02d}:{i%60:02d}" for i in bins[:-1]]
    
    high_bins = pd.cut(sessions_df['High_Minutes'], bins=bins, labels=bin_labels, right=False)
    low_bins = pd.cut(sessions_df['Low_Minutes'], bins=bins, labels=bin_labels, right=False)
    
    high_counts = high_bins.value_counts().sort_index()
    low_counts = low_bins.value_counts().sort_index()
    
    print("\n--- High Occurrence by 15-Minute Bin ---")
    high_pct = (high_counts / len(sessions_df) * 100).round(2)
    high_summary = pd.DataFrame({
        'Count': high_counts,
        'Percentage': high_pct
    })
    print(high_summary)
    
    print("\n--- Low Occurrence by 15-Minute Bin ---")
    low_pct = (low_counts / len(sessions_df) * 100).round(2)
    low_summary = pd.DataFrame({
        'Count': low_counts,
        'Percentage': low_pct
    })
    print(low_summary)
    
    # Most common times
    most_common_high = high_counts.idxmax()
    most_common_low = low_counts.idxmax()
    
    print(f"\n✓ Session HIGH most often occurs around: {most_common_high} ({high_counts.max()} times, {high_pct.max():.2f}%)")
    print(f"✓ Session LOW most often occurs around: {most_common_low} ({low_counts.max()} times, {low_pct.max():.2f}%)")
    
    return {
        'high_counts': high_counts,
        'low_counts': low_counts,
        'high_summary': high_summary,
        'low_summary': low_summary,
        'most_common_high': most_common_high,
        'most_common_low': most_common_low
    }


def analyze_day_of_week(sessions_df):
    """
    Analysis 4: Day of Week Effect
    """
    print("\n" + "="*80)
    print("ANALYSIS 4: DAY OF WEEK EFFECT")
    print("="*80)
    
    # Define day order
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    weekday_stats = sessions_df.groupby('DayOfWeek').agg({
        'Range': ['mean', 'median'],
        'Is_Bullish': ['sum', 'count'],
        'Session_Return': 'mean'
    }).round(2)
    
    # Calculate percentage bullish
    weekday_stats['Pct_Bullish'] = (weekday_stats[('Is_Bullish', 'sum')] / 
                                     weekday_stats[('Is_Bullish', 'count')] * 100).round(2)
    
    # Flatten columns and reorder
    weekday_stats.columns = ['Avg_Range', 'Median_Range', 'Bullish_Count', 'Total_Count', 
                              'Avg_Return', 'Pct_Bullish']
    
    # Reorder by day of week
    weekday_stats = weekday_stats.reindex([day for day in day_order if day in weekday_stats.index])
    
    print("\n--- Statistics by Day of Week ---")
    print(weekday_stats)
    
    return weekday_stats


def analyze_open_drive_correlation(sessions_df):
    """
    Analysis 5: Open Drive Correlation
    If the 01:00 candle is bullish, what's the probability the session closes bullish?
    """
    print("\n" + "="*80)
    print("ANALYSIS 5: OPEN DRIVE CORRELATION")
    print("="*80)
    
    # Sessions where first candle is bullish
    first_bullish = sessions_df[sessions_df['First_Candle_Bullish']]
    first_bearish = sessions_df[~sessions_df['First_Candle_Bullish']]
    
    # Of those, how many closed bullish?
    first_bullish_session_bullish = first_bullish['Is_Bullish'].sum()
    first_bearish_session_bullish = first_bearish['Is_Bullish'].sum()
    
    prob_bullish_given_first_bullish = (first_bullish_session_bullish / len(first_bullish) * 100) if len(first_bullish) > 0 else 0
    prob_bullish_given_first_bearish = (first_bearish_session_bullish / len(first_bearish) * 100) if len(first_bearish) > 0 else 0
    
    print(f"\nFirst Candle (01:00) Bullish: {len(first_bullish)} sessions")
    print(f"  → Session Closed Bullish: {first_bullish_session_bullish} ({prob_bullish_given_first_bullish:.2f}%)")
    print(f"  → Session Closed Bearish: {len(first_bullish) - first_bullish_session_bullish} ({100-prob_bullish_given_first_bullish:.2f}%)")
    
    print(f"\nFirst Candle (01:00) Bearish: {len(first_bearish)} sessions")
    print(f"  → Session Closed Bullish: {first_bearish_session_bullish} ({prob_bullish_given_first_bearish:.2f}%)")
    print(f"  → Session Closed Bearish: {len(first_bearish) - first_bearish_session_bullish} ({100-prob_bullish_given_first_bearish:.2f}%)")
    
    return {
        'first_bullish_count': len(first_bullish),
        'prob_session_bullish_given_first_bullish': prob_bullish_given_first_bullish,
        'first_bearish_count': len(first_bearish),
        'prob_session_bullish_given_first_bearish': prob_bullish_given_first_bearish
    }


def create_visualizations(sessions_df, extreme_timing_results):
    """
    Create visualizations for the analysis.
    """
    print("\n" + "="*80)
    print("CREATING VISUALIZATIONS")
    print("="*80)
    
    # Figure 1: Range Distribution
    fig1, axes1 = plt.subplots(2, 2, figsize=(16, 12))
    fig1.suptitle('NQ Session 01:00-07:00: Range Analysis', fontsize=16, fontweight='bold')
    
    # Subplot 1: Range distribution histogram
    axes1[0, 0].hist(sessions_df['Range'], bins=50, color='steelblue', alpha=0.7, edgecolor='black')
    axes1[0, 0].axvline(sessions_df['Range'].mean(), color='red', linestyle='--', 
                        linewidth=2, label=f'Mean: {sessions_df["Range"].mean():.2f}')
    axes1[0, 0].axvline(sessions_df['Range'].median(), color='green', linestyle='--', 
                        linewidth=2, label=f'Median: {sessions_df["Range"].median():.2f}')
    axes1[0, 0].set_xlabel('Session Range (points)', fontsize=12)
    axes1[0, 0].set_ylabel('Frequency', fontsize=12)
    axes1[0, 0].set_title('Distribution of Session Ranges', fontsize=13, fontweight='bold')
    axes1[0, 0].legend()
    axes1[0, 0].grid(True, alpha=0.3)
    
    # Subplot 2: Range by Year
    yearly_range = sessions_df.groupby('Year')['Range'].mean()
    axes1[0, 1].bar(yearly_range.index, yearly_range.values, color='coral', alpha=0.7, edgecolor='black')
    axes1[0, 1].set_xlabel('Year', fontsize=12)
    axes1[0, 1].set_ylabel('Average Range (points)', fontsize=12)
    axes1[0, 1].set_title('Average Session Range by Year', fontsize=13, fontweight='bold')
    axes1[0, 1].grid(True, alpha=0.3, axis='y')
    
    # Subplot 3: Range by Day of Week
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    weekday_range = sessions_df.groupby('DayOfWeek')['Range'].mean().reindex(
        [day for day in day_order if day in sessions_df['DayOfWeek'].unique()])
    axes1[1, 0].bar(range(len(weekday_range)), weekday_range.values, 
                    color='lightgreen', alpha=0.7, edgecolor='black')
    axes1[1, 0].set_xticks(range(len(weekday_range)))
    axes1[1, 0].set_xticklabels(weekday_range.index, rotation=45, ha='right')
    axes1[1, 0].set_xlabel('Day of Week', fontsize=12)
    axes1[1, 0].set_ylabel('Average Range (points)', fontsize=12)
    axes1[1, 0].set_title('Average Session Range by Day of Week', fontsize=13, fontweight='bold')
    axes1[1, 0].grid(True, alpha=0.3, axis='y')
    
    # Subplot 4: Session Return Distribution
    axes1[1, 1].hist(sessions_df['Session_Return'], bins=50, color='purple', alpha=0.7, edgecolor='black')
    axes1[1, 1].axvline(0, color='black', linestyle='-', linewidth=2, label='Zero Line')
    axes1[1, 1].axvline(sessions_df['Session_Return'].mean(), color='red', linestyle='--', 
                        linewidth=2, label=f'Mean: {sessions_df["Session_Return"].mean():.2f}')
    axes1[1, 1].set_xlabel('Session Return (points)', fontsize=12)
    axes1[1, 1].set_ylabel('Frequency', fontsize=12)
    axes1[1, 1].set_title('Distribution of Session Returns (Close - Open)', fontsize=13, fontweight='bold')
    axes1[1, 1].legend()
    axes1[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/home/runner/work/Backtest-Trading/Backtest-Trading/nq_session_range_analysis.png', 
                dpi=300, bbox_inches='tight')
    print("✓ Saved: nq_session_range_analysis.png")
    
    # Figure 2: High/Low Timing
    fig2, axes2 = plt.subplots(2, 1, figsize=(16, 12))
    fig2.suptitle('NQ Session 01:00-07:00: High/Low Timing Analysis', fontsize=16, fontweight='bold')
    
    # Subplot 1: When High occurs
    high_counts = extreme_timing_results['high_counts']
    axes2[0].bar(range(len(high_counts)), high_counts.values, color='green', alpha=0.7, edgecolor='black')
    axes2[0].set_xticks(range(len(high_counts)))
    axes2[0].set_xticklabels(high_counts.index, rotation=45, ha='right')
    axes2[0].set_xlabel('Time (15-minute bins)', fontsize=12)
    axes2[0].set_ylabel('Frequency', fontsize=12)
    axes2[0].set_title('When Does the Session HIGH Occur?', fontsize=13, fontweight='bold')
    axes2[0].grid(True, alpha=0.3, axis='y')
    
    # Add percentage labels on bars
    for i, (count, pct) in enumerate(zip(high_counts.values, 
                                         (high_counts / len(sessions_df) * 100).values)):
        if count > 0:
            axes2[0].text(i, count, f'{pct:.1f}%', ha='center', va='bottom', fontsize=9)
    
    # Subplot 2: When Low occurs
    low_counts = extreme_timing_results['low_counts']
    axes2[1].bar(range(len(low_counts)), low_counts.values, color='red', alpha=0.7, edgecolor='black')
    axes2[1].set_xticks(range(len(low_counts)))
    axes2[1].set_xticklabels(low_counts.index, rotation=45, ha='right')
    axes2[1].set_xlabel('Time (15-minute bins)', fontsize=12)
    axes2[1].set_ylabel('Frequency', fontsize=12)
    axes2[1].set_title('When Does the Session LOW Occur?', fontsize=13, fontweight='bold')
    axes2[1].grid(True, alpha=0.3, axis='y')
    
    # Add percentage labels on bars
    for i, (count, pct) in enumerate(zip(low_counts.values, 
                                         (low_counts / len(sessions_df) * 100).values)):
        if count > 0:
            axes2[1].text(i, count, f'{pct:.1f}%', ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    plt.savefig('/home/runner/work/Backtest-Trading/Backtest-Trading/nq_session_timing_analysis.png', 
                dpi=300, bbox_inches='tight')
    print("✓ Saved: nq_session_timing_analysis.png")
    
    plt.close('all')


def print_conclusion(all_results):
    """
    Print a synthesized conclusion about recurring biases during the 01:00-07:00 session.
    """
    print("\n" + "="*80)
    print("CONCLUSION: RECURRING BIASES IN THE 01:00-07:00 SESSION")
    print("="*80)
    
    dir_results = all_results['directionality']
    vol_results = all_results['volatility']
    timing_results = all_results['extreme_timing']
    dow_results = all_results['day_of_week']
    open_results = all_results['open_drive']
    
    print("\n📊 KEY FINDINGS:")
    print("-" * 80)
    
    # Bias 1: Directionality
    if dir_results['pct_bullish'] > 52:
        print(f"\n1. BULLISH BIAS: {dir_results['pct_bullish']:.2f}% of sessions close bullish")
        print(f"   → Average bullish session: +{dir_results['avg_bullish_return']:.2f} points")
        print(f"   → This session shows a slight bullish tendency")
    elif dir_results['pct_bearish'] > 52:
        print(f"\n1. BEARISH BIAS: {dir_results['pct_bearish']:.2f}% of sessions close bearish")
        print(f"   → Average bearish session: {dir_results['avg_bearish_return']:.2f} points")
        print(f"   → This session shows a slight bearish tendency")
    else:
        print(f"\n1. NEUTRAL BIAS: Nearly balanced at {dir_results['pct_bullish']:.2f}% bullish vs {dir_results['pct_bearish']:.2f}% bearish")
        print(f"   → No strong directional bias")
    
    # Bias 2: Volatility
    print(f"\n2. VOLATILITY: Average session range is {vol_results['avg_range']:.2f} points")
    yearly_stats = vol_results['yearly_stats']
    if len(yearly_stats) >= 2:
        recent_vol = yearly_stats.iloc[-1]['Avg Range']
        early_vol = yearly_stats.iloc[0]['Avg Range']
        if recent_vol > early_vol * 1.2:
            print(f"   → Volatility has INCREASED over time (2018: {early_vol:.2f} → Recent: {recent_vol:.2f})")
        elif recent_vol < early_vol * 0.8:
            print(f"   → Volatility has DECREASED over time (2018: {early_vol:.2f} → Recent: {recent_vol:.2f})")
        else:
            print(f"   → Volatility remains relatively stable")
    
    # Bias 3: Timing of Extremes
    print(f"\n3. TIMING OF EXTREMES:")
    print(f"   → Session HIGH most often occurs at: {timing_results['most_common_high']}")
    print(f"   → Session LOW most often occurs at: {timing_results['most_common_low']}")
    
    # Check if extremes happen early vs late
    high_time = timing_results['most_common_high']
    low_time = timing_results['most_common_low']
    
    if high_time < '02:00':
        print(f"   → HIGH tends to form EARLY in the session (near open)")
    elif high_time > '06:00':
        print(f"   → HIGH tends to form LATE in the session (near close)")
    else:
        print(f"   → HIGH tends to form MID-SESSION")
    
    if low_time < '02:00':
        print(f"   → LOW tends to form EARLY in the session (near open)")
    elif low_time > '06:00':
        print(f"   → LOW tends to form LATE in the session (near close)")
    else:
        print(f"   → LOW tends to form MID-SESSION")
    
    # Bias 4: Day of Week
    print(f"\n4. DAY OF WEEK EFFECT:")
    best_day = dow_results['Avg_Range'].idxmax()
    worst_day = dow_results['Avg_Range'].idxmin()
    most_bullish_day = dow_results['Pct_Bullish'].idxmax()
    
    print(f"   → Highest volatility: {best_day} ({dow_results.loc[best_day, 'Avg_Range']:.2f} points)")
    print(f"   → Lowest volatility: {worst_day} ({dow_results.loc[worst_day, 'Avg_Range']:.2f} points)")
    print(f"   → Most bullish day: {most_bullish_day} ({dow_results.loc[most_bullish_day, 'Pct_Bullish']:.2f}% bullish)")
    
    # Bias 5: Open Drive
    print(f"\n5. OPEN DRIVE CORRELATION (01:00 Candle → Session Close):")
    prob_bull = open_results['prob_session_bullish_given_first_bullish']
    prob_bear = open_results['prob_session_bullish_given_first_bearish']
    
    if prob_bull > 55:
        print(f"   → STRONG positive correlation: If 01:00 candle is bullish, {prob_bull:.2f}% chance session closes bullish")
        print(f"   → The opening candle direction is a RELIABLE indicator")
    elif prob_bull < 45:
        print(f"   → REVERSAL tendency: If 01:00 candle is bullish, only {prob_bull:.2f}% chance session closes bullish")
        print(f"   → The opening candle may indicate a FADE opportunity")
    else:
        print(f"   → WEAK correlation: 01:00 candle direction has limited predictive value ({prob_bull:.2f}%)")
    
    print("\n" + "="*80)
    print("🎯 TRADING IMPLICATIONS:")
    print("="*80)
    
    # Summary recommendations
    print("\nBased on the data analysis, consider the following for the 01:00-07:00 session:")
    
    if dir_results['pct_bullish'] > 52:
        print("• Slight bullish bias suggests looking for long opportunities")
    elif dir_results['pct_bearish'] > 52:
        print("• Slight bearish bias suggests looking for short opportunities")
    
    print(f"• Average range of {vol_results['avg_range']:.2f} points can inform stop-loss placement")
    print(f"• {best_day} offers the most volatility and potential profit")
    print(f"• Monitor price action around {timing_results['most_common_high']} and {timing_results['most_common_low']} for potential reversals")
    
    if prob_bull > 55:
        print(f"• Strong open drive: Trade in the direction of the 01:00 candle ({prob_bull:.2f}% success)")
    elif prob_bull < 45:
        print(f"• Reversal pattern: Consider fading the 01:00 candle direction")
    
    print("\n" + "="*80 + "\n")


def main():
    """
    Main execution function.
    """
    print("="*80)
    print("NQ SESSION ANALYSIS: 01:00-07:00 TIME WINDOW")
    print("Quantitative Analysis of Price Action and Volatility")
    print("="*80)
    
    # Load data
    df = load_nq_data()
    
    # Filter for session times
    session_df = filter_session_data(df, SESSION_START, SESSION_END)
    
    # Create session aggregates
    sessions_df = create_session_aggregates(session_df)
    
    # Run all analyses
    all_results = {}
    
    all_results['directionality'] = analyze_directionality(sessions_df)
    all_results['volatility'] = analyze_volatility(sessions_df)
    all_results['extreme_timing'] = analyze_extreme_timing(sessions_df)
    all_results['day_of_week'] = analyze_day_of_week(sessions_df)
    all_results['open_drive'] = analyze_open_drive_correlation(sessions_df)
    
    # Create visualizations
    create_visualizations(sessions_df, all_results['extreme_timing'])
    
    # Print conclusion
    print_conclusion(all_results)
    
    print("✓ Analysis complete!")
    print("\nGenerated files:")
    print("  - nq_session_range_analysis.png")
    print("  - nq_session_timing_analysis.png")


if __name__ == "__main__":
    main()

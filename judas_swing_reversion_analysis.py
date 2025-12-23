#!/usr/bin/env python3
"""
Post-Judas Swing Reversion & Reversal Analysis for NQ (Nasdaq Futures)

This script analyzes price behavior AFTER a Judas Swing manipulation is confirmed.
It measures reversion to Tokyo Equilibrium and reversal to Opposing Liquidity.

Extends the original Judas Swing Analysis with post-manipulation tracking.
"""

import pandas as pd
from pathlib import Path
from datetime import time

# Constants
TOKYO_START = time(19, 0)  # 19:00
TOKYO_END = time(0, 0)     # 00:00 (midnight)
LONDON_START = time(1, 0)   # 01:00
LONDON_END = time(5, 0)     # 05:00
EOD_TIME = time(23, 0)      # End of day for search window


def load_nq_data(base_path, years, timeframe='15m'):
    """Load NQ futures data from CSV files"""
    all_data = []
    
    for year in years:
        file_pattern = f"{year} {timeframe}.csv"
        file_path = Path(base_path) / file_pattern
        
        if not file_path.exists():
            print(f"Warning: File not found: {file_path}")
            continue
        
        print(f"Loading {file_path}...")
        
        df = pd.read_csv(
            file_path,
            sep=';',
            header=0,
            names=['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume'],
            skiprows=1
        )
        
        df['DateTime'] = pd.to_datetime(
            df['Date'] + ' ' + df['Time'],
            format='%d/%m/%Y %H:%M:%S'
        )
        
        all_data.append(df)
    
    if not all_data:
        raise ValueError("No data loaded. Check file paths and years.")
    
    combined_df = pd.concat(all_data, ignore_index=True)
    combined_df = combined_df.sort_values('DateTime').reset_index(drop=True)
    
    print(f"\nTotal records loaded: {len(combined_df)}")
    print(f"Date range: {combined_df['DateTime'].min()} to {combined_df['DateTime'].max()}")
    
    return combined_df


def find_manipulation_extreme_time(df, swing_date, direction, tokyo_high, tokyo_low, manip_high, manip_low):
    """
    Find the exact timestamp when the manipulation extreme occurred during London session.
    
    Args:
        df: DataFrame with market data
        swing_date: Date of the Judas Swing
        direction: 'bullish' or 'bearish'
        tokyo_high, tokyo_low: Tokyo session levels
        manip_high, manip_low: Manipulation extreme levels
    
    Returns:
        Timestamp of manipulation extreme or None
    """
    swing_date_obj = pd.Timestamp(swing_date).date()
    
    # Get London session data for this date
    london_data = df[
        (df['DateTime'].dt.date == swing_date_obj) &
        (df['DateTime'].dt.time >= LONDON_START) &
        (df['DateTime'].dt.time < LONDON_END)
    ].copy()
    
    if london_data.empty:
        return None
    
    if direction == 'bullish':
        # Find when the high was reached
        extreme_rows = london_data[london_data['High'] == manip_high]
        if not extreme_rows.empty:
            return extreme_rows.iloc[0]['DateTime']
    else:  # bearish
        # Find when the low was reached
        extreme_rows = london_data[london_data['Low'] == manip_low]
        if not extreme_rows.empty:
            return extreme_rows.iloc[0]['DateTime']
    
    return None


def analyze_reversion(df, swing_date, extreme_time, tokyo_high, tokyo_low, direction):
    """
    Analyze price reversion after manipulation extreme.
    
    Targets:
    - Tokyo Equilibrium: (Tokyo High + Tokyo Low) / 2
    - Opposing Liquidity: Tokyo Low for bullish, Tokyo High for bearish
    
    Args:
        df: DataFrame with market data
        swing_date: Date of the swing
        extreme_time: Timestamp of manipulation extreme
        tokyo_high, tokyo_low: Tokyo session levels
        direction: 'bullish' or 'bearish'
    
    Returns:
        dict with reversion metrics
    """
    if extreme_time is None:
        return None
    
    swing_date_obj = pd.Timestamp(swing_date).date()
    
    # Calculate targets
    tokyo_eq = (tokyo_high + tokyo_low) / 2
    opposing_liq = tokyo_low if direction == 'bullish' else tokyo_high
    
    # Define search window: from extreme_time until 23:00 on the same day
    eod_datetime = pd.Timestamp.combine(swing_date_obj, EOD_TIME)
    
    # Get data after manipulation extreme until end of day
    search_data = df[
        (df['DateTime'] > extreme_time) &
        (df['DateTime'] <= eod_datetime)
    ].copy()
    
    if search_data.empty:
        return {
            'tokyo_eq': tokyo_eq,
            'opposing_liq': opposing_liq,
            'eq_hit': False,
            'eq_duration_minutes': None,
            'opposing_hit': False,
            'opposing_duration_minutes': None
        }
    
    # Check for Tokyo Equilibrium hit
    eq_hit = False
    eq_duration = None
    
    if direction == 'bullish':
        # Price needs to come back down to Eq
        eq_rows = search_data[search_data['Low'] <= tokyo_eq]
    else:  # bearish
        # Price needs to come back up to Eq
        eq_rows = search_data[search_data['High'] >= tokyo_eq]
    
    if not eq_rows.empty:
        eq_hit = True
        eq_time = eq_rows.iloc[0]['DateTime']
        eq_duration = (eq_time - extreme_time).total_seconds() / 60  # in minutes
    
    # Check for Opposing Liquidity hit
    opposing_hit = False
    opposing_duration = None
    
    if direction == 'bullish':
        # Price needs to reach Tokyo Low
        opposing_rows = search_data[search_data['Low'] <= opposing_liq]
    else:  # bearish
        # Price needs to reach Tokyo High
        opposing_rows = search_data[search_data['High'] >= opposing_liq]
    
    if not opposing_rows.empty:
        opposing_hit = True
        opposing_time = opposing_rows.iloc[0]['DateTime']
        opposing_duration = (opposing_time - extreme_time).total_seconds() / 60  # in minutes
    
    return {
        'tokyo_eq': tokyo_eq,
        'opposing_liq': opposing_liq,
        'eq_hit': eq_hit,
        'eq_duration_minutes': eq_duration,
        'opposing_hit': opposing_hit,
        'opposing_duration_minutes': opposing_duration
    }


def analyze_all_reversions(df, swings_df):
    """
    Analyze reversion for all Judas Swings.
    
    Args:
        df: DataFrame with market data
        swings_df: DataFrame with detected Judas Swings
    
    Returns:
        DataFrame with reversion analysis
    """
    print(f"\nAnalyzing post-manipulation behavior for {len(swings_df)} Judas Swings...")
    
    results = []
    
    for idx, row in swings_df.iterrows():
        if idx % 100 == 0:
            print(f"  Processing swing {idx + 1}/{len(swings_df)}...")
        
        # Find manipulation extreme time
        extreme_time = find_manipulation_extreme_time(
            df,
            row['date'],
            row['direction'],
            row['tokyo_high'],
            row['tokyo_low'],
            row['manipulation_high'],
            row['manipulation_low']
        )
        
        # Analyze reversion
        reversion = analyze_reversion(
            df,
            row['date'],
            extreme_time,
            row['tokyo_high'],
            row['tokyo_low'],
            row['direction']
        )
        
        if reversion is not None:
            result = {
                'date': row['date'],
                'direction': row['direction'],
                'amplitude': row['amplitude'],
                'extreme_time': extreme_time,
                'tokyo_eq': reversion['tokyo_eq'],
                'opposing_liq': reversion['opposing_liq'],
                'eq_hit': reversion['eq_hit'],
                'eq_duration_minutes': reversion['eq_duration_minutes'],
                'opposing_hit': reversion['opposing_hit'],
                'opposing_duration_minutes': reversion['opposing_duration_minutes']
            }
            results.append(result)
    
    return pd.DataFrame(results)


def calculate_statistics(reversion_df):
    """
    Calculate comprehensive statistics on reversion behavior.
    
    Args:
        reversion_df: DataFrame with reversion analysis results
    
    Returns:
        dict with statistics
    """
    if reversion_df.empty:
        return None
    
    stats = {}
    
    # Overall statistics
    total_swings = len(reversion_df)
    
    # Equilibrium statistics
    eq_hits = reversion_df[reversion_df['eq_hit'] == True]
    stats['eq_hit_count'] = len(eq_hits)
    stats['eq_hit_rate'] = len(eq_hits) / total_swings * 100
    
    if len(eq_hits) > 0:
        durations = eq_hits['eq_duration_minutes'].dropna()
        stats['eq_mean_duration'] = durations.mean()
        stats['eq_median_duration'] = durations.median()
        stats['eq_min_duration'] = durations.min()
        stats['eq_max_duration'] = durations.max()
        stats['eq_std_duration'] = durations.std()
    
    # Opposing Liquidity statistics
    opp_hits = reversion_df[reversion_df['opposing_hit'] == True]
    stats['opposing_hit_count'] = len(opp_hits)
    stats['opposing_hit_rate'] = len(opp_hits) / total_swings * 100
    
    if len(opp_hits) > 0:
        durations = opp_hits['opposing_duration_minutes'].dropna()
        stats['opposing_mean_duration'] = durations.mean()
        stats['opposing_median_duration'] = durations.median()
        stats['opposing_min_duration'] = durations.min()
        stats['opposing_max_duration'] = durations.max()
        stats['opposing_std_duration'] = durations.std()
    
    # Directional breakdown
    bullish = reversion_df[reversion_df['direction'] == 'bullish']
    bearish = reversion_df[reversion_df['direction'] == 'bearish']
    
    # Bullish statistics
    if len(bullish) > 0:
        bull_eq = bullish[bullish['eq_hit'] == True]
        stats['bullish_eq_hit_rate'] = len(bull_eq) / len(bullish) * 100
        if len(bull_eq) > 0:
            stats['bullish_eq_mean_duration'] = bull_eq['eq_duration_minutes'].mean()
            stats['bullish_eq_median_duration'] = bull_eq['eq_duration_minutes'].median()
        
        bull_opp = bullish[bullish['opposing_hit'] == True]
        stats['bullish_opposing_hit_rate'] = len(bull_opp) / len(bullish) * 100
        if len(bull_opp) > 0:
            stats['bullish_opposing_mean_duration'] = bull_opp['opposing_duration_minutes'].mean()
            stats['bullish_opposing_median_duration'] = bull_opp['opposing_duration_minutes'].median()
    
    # Bearish statistics
    if len(bearish) > 0:
        bear_eq = bearish[bearish['eq_hit'] == True]
        stats['bearish_eq_hit_rate'] = len(bear_eq) / len(bearish) * 100
        if len(bear_eq) > 0:
            stats['bearish_eq_mean_duration'] = bear_eq['eq_duration_minutes'].mean()
            stats['bearish_eq_median_duration'] = bear_eq['eq_duration_minutes'].median()
        
        bear_opp = bearish[bearish['opposing_hit'] == True]
        stats['bearish_opposing_hit_rate'] = len(bear_opp) / len(bearish) * 100
        if len(bear_opp) > 0:
            stats['bearish_opposing_mean_duration'] = bear_opp['opposing_duration_minutes'].mean()
            stats['bearish_opposing_median_duration'] = bear_opp['opposing_duration_minutes'].median()
    
    return stats


def print_report(reversion_df, stats):
    """Print comprehensive reversion analysis report"""
    print("\n" + "="*80)
    print("POST-JUDAS SWING REVERSION & REVERSAL ANALYSIS")
    print("NQ Futures - Price Behavior After Manipulation")
    print("="*80)
    
    if reversion_df.empty or stats is None:
        print("\nNo reversion data available.")
        return
    
    total_swings = len(reversion_df)
    
    print("\n" + "-"*80)
    print("OVERVIEW")
    print("-"*80)
    print(f"Total Judas Swings Analyzed: {total_swings}")
    print(f"Bullish Swings: {len(reversion_df[reversion_df['direction'] == 'bullish'])}")
    print(f"Bearish Swings: {len(reversion_df[reversion_df['direction'] == 'bearish'])}")
    
    # REVERSION TO EQUILIBRIUM
    print("\n" + "-"*80)
    print("1. REVERSION TO TOKYO EQUILIBRIUM (50%)")
    print("-"*80)
    print(f"Hit Rate: {stats['eq_hit_rate']:.2f}% ({stats['eq_hit_count']}/{total_swings} swings)")
    
    if stats['eq_hit_count'] > 0:
        print(f"\nDuration Statistics (minutes):")
        print(f"  Mean: {stats['eq_mean_duration']:.2f} minutes ({stats['eq_mean_duration']/60:.2f} hours)")
        print(f"  Median: {stats['eq_median_duration']:.2f} minutes ({stats['eq_median_duration']/60:.2f} hours)")
        print(f"  Min: {stats['eq_min_duration']:.2f} minutes")
        print(f"  Max: {stats['eq_max_duration']:.2f} minutes ({stats['eq_max_duration']/60:.2f} hours)")
        print(f"  Std Dev: {stats['eq_std_duration']:.2f} minutes")
    
    # REVERSAL TO OPPOSING LIQUIDITY
    print("\n" + "-"*80)
    print("2. FULL REVERSAL TO OPPOSING LIQUIDITY")
    print("-"*80)
    print(f"Hit Rate: {stats['opposing_hit_rate']:.2f}% ({stats['opposing_hit_count']}/{total_swings} swings)")
    
    if stats['opposing_hit_count'] > 0:
        print(f"\nDuration Statistics (minutes):")
        print(f"  Mean: {stats['opposing_mean_duration']:.2f} minutes ({stats['opposing_mean_duration']/60:.2f} hours)")
        print(f"  Median: {stats['opposing_median_duration']:.2f} minutes ({stats['opposing_median_duration']/60:.2f} hours)")
        print(f"  Min: {stats['opposing_min_duration']:.2f} minutes")
        print(f"  Max: {stats['opposing_max_duration']:.2f} minutes ({stats['opposing_max_duration']/60:.2f} hours)")
        print(f"  Std Dev: {stats['opposing_std_duration']:.2f} minutes")
    
    # DIRECTIONAL COMPARISON
    print("\n" + "-"*80)
    print("3. SEGMENTATION BY DIRECTION")
    print("-"*80)
    
    print("\nBULLISH MANIPULATIONS (Tokyo High Breaks):")
    if 'bullish_eq_hit_rate' in stats:
        print(f"  Reversion to Equilibrium:")
        print(f"    Hit Rate: {stats['bullish_eq_hit_rate']:.2f}%")
        if 'bullish_eq_mean_duration' in stats:
            print(f"    Mean Duration: {stats['bullish_eq_mean_duration']:.2f} minutes ({stats['bullish_eq_mean_duration']/60:.2f} hours)")
            print(f"    Median Duration: {stats['bullish_eq_median_duration']:.2f} minutes ({stats['bullish_eq_median_duration']/60:.2f} hours)")
    
    if 'bullish_opposing_hit_rate' in stats:
        print(f"  Full Reversal to Tokyo Low:")
        print(f"    Hit Rate: {stats['bullish_opposing_hit_rate']:.2f}%")
        if 'bullish_opposing_mean_duration' in stats:
            print(f"    Mean Duration: {stats['bullish_opposing_mean_duration']:.2f} minutes ({stats['bullish_opposing_mean_duration']/60:.2f} hours)")
            print(f"    Median Duration: {stats['bullish_opposing_median_duration']:.2f} minutes ({stats['bullish_opposing_median_duration']/60:.2f} hours)")
    
    print("\nBEARISH MANIPULATIONS (Tokyo Low Breaks):")
    if 'bearish_eq_hit_rate' in stats:
        print(f"  Reversion to Equilibrium:")
        print(f"    Hit Rate: {stats['bearish_eq_hit_rate']:.2f}%")
        if 'bearish_eq_mean_duration' in stats:
            print(f"    Mean Duration: {stats['bearish_eq_mean_duration']:.2f} minutes ({stats['bearish_eq_mean_duration']/60:.2f} hours)")
            print(f"    Median Duration: {stats['bearish_eq_median_duration']:.2f} minutes ({stats['bearish_eq_median_duration']/60:.2f} hours)")
    
    if 'bearish_opposing_hit_rate' in stats:
        print(f"  Full Reversal to Tokyo High:")
        print(f"    Hit Rate: {stats['bearish_opposing_hit_rate']:.2f}%")
        if 'bearish_opposing_mean_duration' in stats:
            print(f"    Mean Duration: {stats['bearish_opposing_mean_duration']:.2f} minutes ({stats['bearish_opposing_mean_duration']/60:.2f} hours)")
            print(f"    Median Duration: {stats['bearish_opposing_median_duration']:.2f} minutes ({stats['bearish_opposing_median_duration']/60:.2f} hours)")
    
    print("\n" + "="*80)
    print("Analysis complete. Statistical data only - no trading logic applied.")
    print("="*80 + "\n")


def save_results(reversion_df, output_path='judas_swing_reversion_results.csv'):
    """Save detailed reversion results to CSV"""
    if not reversion_df.empty:
        reversion_df.to_csv(output_path, index=False)
        print(f"\nDetailed reversion results saved to: {output_path}")


def main():
    """Main execution function"""
    print("="*80)
    print("POST-JUDAS SWING REVERSION & REVERSAL ANALYSIS")
    print("Analyzing price behavior after NQ manipulation")
    print("="*80)
    
    # Configuration
    base_path = '/home/runner/work/Backtest-Trading/Backtest-Trading'
    years = list(range(2018, 2026))
    timeframe = '15m'
    
    # Load original Judas Swing results
    print("\nLoading existing Judas Swing results...")
    swings_df = pd.read_csv(f"{base_path}/judas_swing_results.csv")
    print(f"Loaded {len(swings_df)} Judas Swings from previous analysis")
    
    # Load market data
    print(f"\nLoading {timeframe} market data for years: {years}")
    df = load_nq_data(base_path, years, timeframe)
    
    # Analyze reversions
    reversion_df = analyze_all_reversions(df, swings_df)
    
    # Calculate statistics
    if not reversion_df.empty:
        stats = calculate_statistics(reversion_df)
        
        # Print report
        print_report(reversion_df, stats)
        
        # Save results
        save_results(reversion_df)
    else:
        print("\nNo reversion data could be generated.")


if __name__ == "__main__":
    main()

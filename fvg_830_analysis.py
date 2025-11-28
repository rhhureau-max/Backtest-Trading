#!/usr/bin/env python3
"""
FVG (Fair Value Gap) Analysis at 8:30 AM New York Opening Candle

This script analyzes 1-minute data from 2018 to 2025 to find FVGs
(Fair Value Gaps) on the 8:30 AM candle.

An FVG occurs when there's an imbalance between candle n-1 and n+1:
- Bullish FVG: Low of n+1 > High of n-1 (gap up)
- Bearish FVG: High of n+1 < Low of n-1 (gap down)
"""

import pandas as pd
import os
from datetime import datetime

# Directory containing the data files
DATA_DIR = os.path.dirname(os.path.abspath(__file__))

# Expected column configuration for the CSV files
# Format: Date;Time;Open;High;Low;Close;Volume
EXPECTED_COLUMNS = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
DATE_FORMAT = '%d/%m/%Y %H:%M:%S'


def load_1m_data(year):
    """Load 1-minute data for a given year."""
    filepath = os.path.join(DATA_DIR, f"{year} 1m.csv")
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return None
    
    df = pd.read_csv(filepath, sep=';', names=EXPECTED_COLUMNS, skiprows=1)
    
    # Validate required columns exist
    missing_cols = [col for col in ['Date', 'Time', 'High', 'Low', 'Open', 'Close'] if col not in df.columns]
    if missing_cols:
        print(f"Error: Missing required columns {missing_cols} in {filepath}")
        return None
    
    # Parse datetime with error handling
    try:
        df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format=DATE_FORMAT)
    except (ValueError, TypeError) as e:
        print(f"Error parsing dates in {filepath}. Expected format: {DATE_FORMAT}")
        print(f"  Details: {e}")
        return None
    
    return df


def extract_candle_values(candle):
    """Extract High and Low values from a candle row."""
    return float(candle['High'].iloc[0]), float(candle['Low'].iloc[0])


def detect_fvg_at_830(df):
    """
    Detect FVGs at the 8:30 AM candle.
    
    For each 8:30 candle, we check if there's an FVG by comparing:
    - Candle at 8:29 (n-1)
    - Candle at 8:30 (n) - the target candle
    - Candle at 8:31 (n+1)
    
    Bullish FVG: Low of 8:31 > High of 8:29
    Bearish FVG: High of 8:31 < Low of 8:29
    """
    fvg_results = []
    
    # Filter to get 8:29, 8:30, and 8:31 candles
    df_filtered = df[df['Time'].isin(['08:29:00', '08:30:00', '08:31:00'])].copy()
    
    # Group by date
    df_filtered['DateOnly'] = df_filtered['DateTime'].dt.date
    
    for date_val, group in df_filtered.groupby('DateOnly'):
        candle_829 = group[group['Time'] == '08:29:00']
        candle_830 = group[group['Time'] == '08:30:00']
        candle_831 = group[group['Time'] == '08:31:00']
        
        # We need all 3 candles to detect an FVG
        if len(candle_829) != 1 or len(candle_830) != 1 or len(candle_831) != 1:
            continue
        
        high_829, low_829 = extract_candle_values(candle_829)
        high_830, low_830 = extract_candle_values(candle_830)
        high_831, low_831 = extract_candle_values(candle_831)
        open_830 = float(candle_830['Open'].iloc[0])
        close_830 = float(candle_830['Close'].iloc[0])
        
        fvg_type = None
        fvg_size = 0
        
        # Bullish FVG: gap up - low of n+1 is higher than high of n-1
        if low_831 > high_829:
            fvg_type = 'Bullish'
            fvg_size = low_831 - high_829
        
        # Bearish FVG: gap down - high of n+1 is lower than low of n-1
        elif high_831 < low_829:
            fvg_type = 'Bearish'
            fvg_size = low_829 - high_831
        
        fvg_results.append({
            'Date': date_val,
            'High_829': high_829,
            'Low_829': low_829,
            'Open_830': open_830,
            'High_830': high_830,
            'Low_830': low_830,
            'Close_830': close_830,
            'High_831': high_831,
            'Low_831': low_831,
            'FVG_Type': fvg_type,
            'FVG_Size': fvg_size
        })
    
    return fvg_results


def main():
    """Main function to run the FVG analysis."""
    all_results = []
    years = range(2018, 2026)  # 2018 to 2025
    
    print("=" * 80)
    print("FVG Analysis at 8:30 AM New York Opening Candle (1-minute data)")
    print("=" * 80)
    print()
    
    for year in years:
        print(f"Processing year {year}...")
        df = load_1m_data(year)
        
        if df is not None:
            results = detect_fvg_at_830(df)
            all_results.extend(results)
            
            # Count FVGs for this year
            fvg_count = sum(1 for r in results if r['FVG_Type'] is not None)
            bullish_count = sum(1 for r in results if r['FVG_Type'] == 'Bullish')
            bearish_count = sum(1 for r in results if r['FVG_Type'] == 'Bearish')
            total_days = len(results)
            
            print(f"  - Total trading days with 8:30 data: {total_days}")
            print(f"  - Total FVGs: {fvg_count}")
            print(f"  - Bullish FVGs: {bullish_count}")
            print(f"  - Bearish FVGs: {bearish_count}")
            print()
    
    # Convert to DataFrame for analysis
    results_df = pd.DataFrame(all_results)
    
    # Summary statistics
    print("=" * 80)
    print("SUMMARY STATISTICS (2018 - 2025)")
    print("=" * 80)
    print()
    
    total_days = len(results_df)
    total_fvgs = results_df[results_df['FVG_Type'].notna()].shape[0]
    bullish_fvgs = results_df[results_df['FVG_Type'] == 'Bullish'].shape[0]
    bearish_fvgs = results_df[results_df['FVG_Type'] == 'Bearish'].shape[0]
    no_fvg_days = results_df[results_df['FVG_Type'].isna()].shape[0]
    
    print(f"Total trading days analyzed: {total_days}")
    print(f"Days with FVG at 8:30: {total_fvgs} ({100*total_fvgs/total_days:.2f}%)")
    print(f"  - Bullish FVGs: {bullish_fvgs} ({100*bullish_fvgs/total_days:.2f}%)")
    print(f"  - Bearish FVGs: {bearish_fvgs} ({100*bearish_fvgs/total_days:.2f}%)")
    print(f"Days without FVG at 8:30: {no_fvg_days} ({100*no_fvg_days/total_days:.2f}%)")
    print()
    
    # FVG size statistics
    fvg_df = results_df[results_df['FVG_Type'].notna()]
    if len(fvg_df) > 0:
        print("FVG Size Statistics (in points):")
        print(f"  - Mean: {fvg_df['FVG_Size'].mean():.2f}")
        print(f"  - Median: {fvg_df['FVG_Size'].median():.2f}")
        print(f"  - Min: {fvg_df['FVG_Size'].min():.2f}")
        print(f"  - Max: {fvg_df['FVG_Size'].max():.2f}")
        print()
    
    # Yearly breakdown
    print("=" * 80)
    print("YEARLY BREAKDOWN")
    print("=" * 80)
    print()
    
    results_df['Year'] = pd.to_datetime(results_df['Date']).dt.year
    
    # Calculate yearly statistics using a more compatible approach
    def calc_yearly_stats(x):
        return pd.Series({
            'Total_Days': len(x),
            'FVG_Count': x['FVG_Type'].notna().sum(),
            'Bullish_FVGs': (x['FVG_Type'] == 'Bullish').sum(),
            'Bearish_FVGs': (x['FVG_Type'] == 'Bearish').sum(),
            'FVG_Percentage': 100 * x['FVG_Type'].notna().sum() / len(x) if len(x) > 0 else 0
        })
    
    yearly_stats = results_df.groupby('Year')[['FVG_Type', 'FVG_Size']].apply(calc_yearly_stats)
    
    print(yearly_stats.to_string())
    print()
    
    # Save detailed results to CSV
    output_path = os.path.join(DATA_DIR, 'fvg_830_analysis_results.csv')
    results_df.to_csv(output_path, index=False, sep=';')
    print(f"Detailed results saved to: {output_path}")
    
    # Save summary to markdown
    summary_path = os.path.join(DATA_DIR, 'FVG_830_ANALYSIS_REPORT.md')
    with open(summary_path, 'w') as f:
        f.write("# FVG (Fair Value Gap) Analysis at 8:30 AM New York Opening\n\n")
        f.write("## Methodology\n\n")
        f.write("This analysis examines 1-minute candles from 2018 to 2025 to detect Fair Value Gaps (FVG) at the 8:30 AM New York opening candle.\n\n")
        f.write("An FVG occurs when there is an imbalance between the candle before (n-1) and the candle after (n+1):\n\n")
        f.write("- **Bullish FVG**: Low of candle at 8:31 > High of candle at 8:29 (gap up)\n")
        f.write("- **Bearish FVG**: High of candle at 8:31 < Low of candle at 8:29 (gap down)\n\n")
        f.write("## Summary Statistics\n\n")
        f.write(f"| Metric | Value |\n")
        f.write(f"|--------|-------|\n")
        f.write(f"| Total trading days analyzed | {total_days} |\n")
        f.write(f"| Days with FVG at 8:30 | {total_fvgs} ({100*total_fvgs/total_days:.2f}%) |\n")
        f.write(f"| Bullish FVGs | {bullish_fvgs} ({100*bullish_fvgs/total_days:.2f}%) |\n")
        f.write(f"| Bearish FVGs | {bearish_fvgs} ({100*bearish_fvgs/total_days:.2f}%) |\n")
        f.write(f"| Days without FVG | {no_fvg_days} ({100*no_fvg_days/total_days:.2f}%) |\n\n")
        
        if len(fvg_df) > 0:
            f.write("## FVG Size Statistics (in points)\n\n")
            f.write(f"| Statistic | Value |\n")
            f.write(f"|-----------|-------|\n")
            f.write(f"| Mean | {fvg_df['FVG_Size'].mean():.2f} |\n")
            f.write(f"| Median | {fvg_df['FVG_Size'].median():.2f} |\n")
            f.write(f"| Min | {fvg_df['FVG_Size'].min():.2f} |\n")
            f.write(f"| Max | {fvg_df['FVG_Size'].max():.2f} |\n\n")
        
        f.write("## Yearly Breakdown\n\n")
        f.write("| Year | Total Days | FVG Count | Bullish FVGs | Bearish FVGs | FVG % |\n")
        f.write("|------|------------|-----------|--------------|--------------|-------|\n")
        for year_idx, row in yearly_stats.iterrows():
            f.write(f"| {int(year_idx)} | {int(row['Total_Days'])} | {int(row['FVG_Count'])} | {int(row['Bullish_FVGs'])} | {int(row['Bearish_FVGs'])} | {row['FVG_Percentage']:.2f}% |\n")
        
        f.write("\n## Data Files\n\n")
        f.write("- `fvg_830_analysis_results.csv`: Detailed daily results with all candle data\n")
        f.write("- `fvg_830_analysis.py`: Python script used for this analysis\n")
    
    print(f"Summary report saved to: {summary_path}")
    
    return results_df


if __name__ == "__main__":
    main()

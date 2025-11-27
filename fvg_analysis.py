"""
Fair Value Gap (FVG) Analysis Script
Analyzes 1-minute candlestick data from 2018 to 2025 to count FVGs between 8:30 and 10:00 (NY Time)

A Fair Value Gap (FVG) occurs when:
- Bullish FVG: High of candle N-2 < Low of candle N (gap up)
- Bearish FVG: Low of candle N-2 > High of candle N (gap down)
"""

import pandas as pd
from datetime import datetime, time
import os
import sys

def load_data(data_dir):
    """Load all 1-minute data files from 2018 to 2025"""
    all_data = []
    
    years = range(2018, 2026)  # 2018 to 2025
    
    for year in years:
        filepath = os.path.join(data_dir, f"{year} 1m.csv")
        
        if os.path.exists(filepath):
            print(f"Loading {filepath}...")
            df = pd.read_csv(filepath, sep=';', skiprows=1, header=None,
                           names=['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume'])
            df['Year'] = year
            all_data.append(df)
            print(f"  Loaded {len(df):,} candles for {year}")
        else:
            print(f"  Warning: File not found: {filepath}")
    
    if all_data:
        combined = pd.concat(all_data, ignore_index=True)
        print(f"\nTotal candles loaded: {len(combined):,}")
        return combined
    return pd.DataFrame()

def filter_time_range(df, start_time='08:30:00', end_time='10:00:00'):
    """Filter data to only include candles between 8:30 and 10:00 NY time"""
    
    # Convert time strings to time objects for proper comparison
    start = datetime.strptime(start_time, '%H:%M:%S').time()
    end = datetime.strptime(end_time, '%H:%M:%S').time()
    
    # Parse Time column to time objects
    df['TimeObj'] = df['Time'].apply(lambda x: datetime.strptime(x, '%H:%M:%S').time())
    
    # Filter by time range
    mask = (df['TimeObj'] >= start) & (df['TimeObj'] <= end)
    filtered = df[mask].copy()
    filtered = filtered.drop(columns=['TimeObj'])
    
    print(f"Candles between {start_time} and {end_time}: {len(filtered):,}")
    return filtered

def detect_fvg(df):
    """
    Detect Fair Value Gaps in the data
    
    Bullish FVG: High of candle N-2 < Low of candle N
    Bearish FVG: Low of candle N-2 > High of candle N
    """
    
    bullish_fvg_count = 0
    bearish_fvg_count = 0
    fvg_details = []
    
    # We need to be careful to only detect FVGs within the same day's session
    # Group by Date first
    df['Date_Time'] = df['Date'] + ' ' + df['Time']
    
    # Sort by Date and Time to ensure proper order
    df_sorted = df.sort_values(['Date', 'Time']).reset_index(drop=True)
    
    # Group by Date
    for date, group in df_sorted.groupby('Date'):
        group = group.reset_index(drop=True)
        
        # We need at least 3 candles to detect FVG
        if len(group) < 3:
            continue
        
        for i in range(2, len(group)):
            candle_n_minus_2_high = group.loc[i-2, 'High']
            candle_n_minus_2_low = group.loc[i-2, 'Low']
            candle_n_high = group.loc[i, 'High']
            candle_n_low = group.loc[i, 'Low']
            
            # Bullish FVG: Gap up - High of N-2 < Low of N
            if candle_n_minus_2_high < candle_n_low:
                bullish_fvg_count += 1
                fvg_details.append({
                    'Date': date,
                    'Time': group.loc[i, 'Time'],
                    'Type': 'Bullish',
                    'Gap_Size': candle_n_low - candle_n_minus_2_high,
                    'Candle_N2_High': candle_n_minus_2_high,
                    'Candle_N_Low': candle_n_low
                })
            
            # Bearish FVG: Gap down - Low of N-2 > High of N
            elif candle_n_minus_2_low > candle_n_high:
                bearish_fvg_count += 1
                fvg_details.append({
                    'Date': date,
                    'Time': group.loc[i, 'Time'],
                    'Type': 'Bearish',
                    'Gap_Size': candle_n_minus_2_low - candle_n_high,
                    'Candle_N2_Low': candle_n_minus_2_low,
                    'Candle_N_High': candle_n_high
                })
    
    return bullish_fvg_count, bearish_fvg_count, fvg_details

def main():
    # Get the directory where the script is located, or use command line argument
    if len(sys.argv) > 1:
        data_dir = sys.argv[1]
    else:
        data_dir = os.path.dirname(os.path.abspath(__file__))
    
    print("=" * 60)
    print("Fair Value Gap (FVG) Analysis")
    print("Time Window: 08:30 - 10:00 (New York Opening Time)")
    print("Data Range: 2018 - 2025")
    print("=" * 60)
    print()
    
    # Load all data
    print("Step 1: Loading data...")
    df = load_data(data_dir)
    
    if df.empty:
        print("No data loaded. Exiting.")
        return
    
    # Filter by time range
    print("\nStep 2: Filtering by time range (08:30 - 10:00)...")
    df_filtered = filter_time_range(df)
    
    if df_filtered.empty:
        print("No data in the specified time range. Exiting.")
        return
    
    # Detect FVGs
    print("\nStep 3: Detecting Fair Value Gaps...")
    bullish_count, bearish_count, fvg_details = detect_fvg(df_filtered)
    
    total_fvg = bullish_count + bearish_count
    
    # Summary
    print("\n" + "=" * 60)
    print("RESULTS SUMMARY")
    print("=" * 60)
    print(f"\nTotal Fair Value Gaps Found: {total_fvg:,}")
    print(f"  - Bullish FVGs: {bullish_count:,}")
    print(f"  - Bearish FVGs: {bearish_count:,}")
    print()
    
    # Create FVG details dataframe
    if fvg_details:
        fvg_df = pd.DataFrame(fvg_details)
        
        # Yearly breakdown
        print("Yearly Breakdown:")
        print("-" * 40)
        
        # Extract year from date (format: DD/MM/YYYY)
        fvg_df['Year'] = fvg_df['Date'].apply(lambda x: x.split('/')[2])
        yearly_summary = fvg_df.groupby(['Year', 'Type']).size().unstack(fill_value=0)
        
        if 'Bullish' not in yearly_summary.columns:
            yearly_summary['Bullish'] = 0
        if 'Bearish' not in yearly_summary.columns:
            yearly_summary['Bearish'] = 0
            
        yearly_summary['Total'] = yearly_summary['Bullish'] + yearly_summary['Bearish']
        print(yearly_summary.to_string())
        
        # Save to CSV
        output_file = os.path.join(data_dir, "fvg_analysis_results.csv")
        fvg_df.to_csv(output_file, index=False)
        print(f"\nDetailed FVG data saved to: {output_file}")
        
        # Save summary to text file
        summary_file = os.path.join(data_dir, "fvg_analysis_summary.txt")
        with open(summary_file, 'w') as f:
            f.write("=" * 60 + "\n")
            f.write("Fair Value Gap (FVG) Analysis Summary\n")
            f.write("Time Window: 08:30 - 10:00 (New York Opening Time)\n")
            f.write("Data Range: 2018 - 2025\n")
            f.write("=" * 60 + "\n\n")
            f.write(f"Total Fair Value Gaps Found: {total_fvg:,}\n")
            f.write(f"  - Bullish FVGs: {bullish_count:,}\n")
            f.write(f"  - Bearish FVGs: {bearish_count:,}\n\n")
            f.write("Yearly Breakdown:\n")
            f.write("-" * 40 + "\n")
            f.write(yearly_summary.to_string())
            f.write("\n")
        print(f"Summary saved to: {summary_file}")
    
    print("\n" + "=" * 60)
    print("Analysis Complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()

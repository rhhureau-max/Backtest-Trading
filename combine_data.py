#!/usr/bin/env python3
"""
Script to combine all 1-minute NQ Futures CSV files (2018-2024) into a single dataset.
Data files: "2018 1m.csv", "2019 1m.csv", ..., "2024 1m.csv"
Format: Date;Time;Open;High;Low;Close;Volume (semicolon delimiter)
"""

import pandas as pd
import os
from datetime import datetime

def combine_csv_files():
    """
    Combines individual year CSV files into one consolidated dataset.
    Saves output as "NQ_1min_2018_2024.csv"
    """
    print("Starting data combination process...")
    
    # Years to process
    years = range(2018, 2025)  # 2018 to 2024 inclusive
    
    all_data = []
    
    for year in years:
        filename = f"{year} 1m.csv"
        
        if not os.path.exists(filename):
            print(f"WARNING: {filename} not found, skipping...")
            continue
        
        print(f"Reading {filename}...")
        
        # Read CSV with semicolon delimiter
        df = pd.read_csv(
            filename,
            sep=';',
            header=0,
            names=['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
        )
        
        # Create datetime column
        df['Datetime'] = pd.to_datetime(
            df['Date'] + ' ' + df['Time'],
            format='%d/%m/%Y %H:%M:%S'
        )
        
        print(f"  Loaded {len(df)} rows from {year}")
        all_data.append(df)
    
    # Combine all dataframes
    print("\nCombining all data...")
    combined_df = pd.concat(all_data, ignore_index=True)
    
    # Sort by datetime
    combined_df.sort_values('Datetime', inplace=True)
    combined_df.reset_index(drop=True, inplace=True)
    
    # Save to output file
    output_filename = "NQ_1min_2018_2024.csv"
    print(f"\nSaving combined data to {output_filename}...")
    combined_df.to_csv(output_filename, index=False)
    
    print(f"\n✓ Successfully combined {len(combined_df)} rows")
    print(f"✓ Date range: {combined_df['Datetime'].min()} to {combined_df['Datetime'].max()}")
    print(f"✓ Output file: {output_filename}")
    
    return output_filename

if __name__ == "__main__":
    combine_csv_files()

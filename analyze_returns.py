#!/usr/bin/env python3
"""
Analyze 1-minute trading data files from 2018 to 2025
Calculate annual and overall returns
"""

import pandas as pd
import os
from datetime import datetime

def load_data_file(filename):
    """Load a data file (XLSX or CSV)"""
    if filename.endswith('.xlsx'):
        return pd.read_excel(filename)
    elif filename.endswith('.csv'):
        # CSV files in this dataset use semicolon as delimiter
        return pd.read_csv(filename, sep=';')
    else:
        raise ValueError(f"Unsupported file format: {filename}")

def calculate_returns(df, year):
    """Calculate returns for a given year's data
    
    Expected columns (OHLCV format):
    Column1: Date
    Column2: Time  
    Column3: Open
    Column4: High
    Column5: Low
    Column6: Close (used for return calculation)
    Column7: Volume
    """
    # Ensure we have data
    if len(df) == 0:
        raise ValueError("DataFrame is empty")
    
    # Validate we have sufficient columns
    if len(df.columns) < 6:
        raise ValueError(f"Expected at least 6 columns, but found {len(df.columns)}")
    
    # Get first and last close prices
    # Handle both column index and column name
    if 'Column6' in df.columns:
        close_col = 'Column6'
    else:
        close_col = df.columns[5]  # 6th column (0-indexed) is Close price
    
    first_close = float(df[close_col].iloc[0])
    last_close = float(df[close_col].iloc[-1])
    
    # Calculate return
    annual_return = ((last_close - first_close) / first_close) * 100
    
    return {
        'year': year,
        'first_close': first_close,
        'last_close': last_close,
        'return_pct': annual_return,
        'num_records': len(df)
    }

def main():
    """Main analysis function"""
    print("=" * 80)
    print("ANALYSIS OF 1-MINUTE TRADING DATA (2018-2025)")
    print("=" * 80)
    print()
    
    # Years to analyze
    years = [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]
    results = []
    
    # Analyze each year
    for year in years:
        # Try XLSX first, then CSV
        xlsx_file = f'{year} 1m.xlsx'
        csv_file = f'{year} 1m.csv'
        
        if os.path.exists(xlsx_file):
            filename = xlsx_file
        elif os.path.exists(csv_file):
            filename = csv_file
        else:
            print(f"⚠️  No data file found for {year}")
            continue
        
        print(f"Loading {filename}...")
        try:
            df = load_data_file(filename)
            result = calculate_returns(df, year)
            results.append(result)
            
            print(f"✓ {year}: {result['return_pct']:.2f}% return")
            print(f"  First close: {result['first_close']:.2f}")
            print(f"  Last close: {result['last_close']:.2f}")
            print(f"  Records: {result['num_records']:,}")
            print()
        except Exception as e:
            print(f"✗ Error processing {year}: {e}")
            print()
    
    # Calculate overall returns
    if results:
        print("=" * 80)
        print("ANNUAL RETURNS SUMMARY")
        print("=" * 80)
        print()
        print(f"{'Year':<10} {'Return %':<15} {'First Close':<15} {'Last Close':<15}")
        print("-" * 80)
        
        for result in results:
            print(f"{result['year']:<10} {result['return_pct']:>12.2f}%  "
                  f"{result['first_close']:>12.2f}  {result['last_close']:>12.2f}")
        
        # Calculate overall return from first year to last year
        first_year_start = results[0]['first_close']
        last_year_end = results[-1]['last_close']
        overall_return = ((last_year_end - first_year_start) / first_year_start) * 100
        
        print("-" * 80)
        print(f"{'OVERALL':<10} {overall_return:>12.2f}%  "
              f"{first_year_start:>12.2f}  {last_year_end:>12.2f}")
        print()
        
        # Calculate average annual return
        avg_annual_return = sum(r['return_pct'] for r in results) / len(results)
        print(f"Average Annual Return: {avg_annual_return:.2f}%")
        print()
        
        # Calculate compound annual growth rate (CAGR)
        # Number of complete years from first year start to last year end
        years_elapsed = len(results)
        if years_elapsed > 1:
            cagr = (((last_year_end / first_year_start) ** (1 / years_elapsed)) - 1) * 100
            print(f"Compound Annual Growth Rate (CAGR): {cagr:.2f}%")
            print(f"(Based on {years_elapsed} year periods from {results[0]['year']} to {results[-1]['year']})")
        print()
        
        print("=" * 80)
        
        # Save results to a file
        with open('returns_analysis.txt', 'w') as f:
            f.write("=" * 80 + "\n")
            f.write("ANALYSIS OF 1-MINUTE TRADING DATA (2018-2025)\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("ANNUAL RETURNS SUMMARY\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"{'Year':<10} {'Return %':<15} {'First Close':<15} {'Last Close':<15}\n")
            f.write("-" * 80 + "\n")
            
            for result in results:
                f.write(f"{result['year']:<10} {result['return_pct']:>12.2f}%  "
                       f"{result['first_close']:>12.2f}  {result['last_close']:>12.2f}\n")
            
            f.write("-" * 80 + "\n")
            f.write(f"{'OVERALL':<10} {overall_return:>12.2f}%  "
                   f"{first_year_start:>12.2f}  {last_year_end:>12.2f}\n\n")
            
            f.write(f"Average Annual Return: {avg_annual_return:.2f}%\n")
            
            if years_elapsed > 1:
                f.write(f"Compound Annual Growth Rate (CAGR): {cagr:.2f}%\n")
                f.write(f"(Based on {years_elapsed} year periods from {results[0]['year']} to {results[-1]['year']})\n")
            
            f.write("\n" + "=" * 80 + "\n")
        
        print(f"Results saved to 'returns_analysis.txt'")
    else:
        print("No data files could be processed.")

if __name__ == '__main__':
    main()

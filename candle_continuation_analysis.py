#!/usr/bin/env python3
"""
Candle Continuation Probability Analysis

Analyzes historical trading data to calculate the probability of candle continuation
based on wick-less candles meeting minimum body size requirements.
"""

import os
import zipfile
import pandas as pd
from datetime import datetime
from typing import Dict

# Configuration - use script directory as default data directory
DATA_DIR = os.environ.get("DATA_DIR", os.path.dirname(os.path.abspath(__file__)))
START_YEAR = int(os.environ.get("START_YEAR", "2018"))
END_YEAR = int(os.environ.get("END_YEAR", str(datetime.now().year)))
YEARS = range(START_YEAR, END_YEAR + 1)
TIME_FILTER_START = "02:00:00"
TIME_FILTER_END = "12:00:00"

# Minimum body size in points for each timeframe
MIN_BODY_SIZE = {
    "1m": 5,
    "5m": 20,
    "15m": 40
}


def extract_zip_if_needed(zip_path: str, extract_to: str) -> str:
    """Extract a zip file if needed and return the path to the CSV file."""
    csv_name = os.path.basename(zip_path).replace(".zip", "")
    csv_path = os.path.join(extract_to, csv_name)
    
    if not os.path.exists(csv_path):
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # Extract only the CSV file, not macOS metadata
            for file_info in zip_ref.filelist:
                if file_info.filename.endswith('.csv') and not file_info.filename.startswith('__MACOSX'):
                    # Security: Validate filename to prevent path traversal
                    # Normalize the path and check if it would escape the target directory
                    safe_name = os.path.basename(file_info.filename)
                    if not safe_name:
                        print(f"  Warning: Skipping empty filename")
                        continue
                    
                    # Resolve the full path and verify it's within extract_to
                    target_path = os.path.normpath(os.path.join(extract_to, file_info.filename))
                    if not target_path.startswith(os.path.normpath(extract_to) + os.sep) and target_path != os.path.normpath(extract_to):
                        print(f"  Warning: Skipping potentially unsafe file: {file_info.filename}")
                        continue
                    
                    # Read and write to safe location using csv_path (derived from zip filename)
                    with zip_ref.open(file_info) as source:
                        with open(csv_path, 'wb') as target:
                            target.write(source.read())
                    break
    
    return csv_path


def load_csv_data(file_path: str) -> pd.DataFrame:
    """Load a CSV file with the trading data format."""
    try:
        df = pd.read_csv(
            file_path,
            sep=';',
            names=['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume'],
            skiprows=1  # Skip header row
        )
    except (OSError, pd.errors.EmptyDataError, pd.errors.ParserError) as e:
        print(f"  Error loading {file_path}: {e}")
        return pd.DataFrame()
    
    # Convert columns to appropriate types
    df['Open'] = pd.to_numeric(df['Open'], errors='coerce')
    df['High'] = pd.to_numeric(df['High'], errors='coerce')
    df['Low'] = pd.to_numeric(df['Low'], errors='coerce')
    df['Close'] = pd.to_numeric(df['Close'], errors='coerce')
    df['Volume'] = pd.to_numeric(df['Volume'], errors='coerce')
    
    # Create datetime column - try multiple formats
    df['DateTime'] = pd.to_datetime(
        df['Date'] + ' ' + df['Time'], 
        format='%d/%m/%Y %H:%M:%S', 
        errors='coerce'
    )
    # Fallback format if first fails
    mask = df['DateTime'].isna()
    if mask.any():
        df.loc[mask, 'DateTime'] = pd.to_datetime(
            df.loc[mask, 'Date'] + ' ' + df.loc[mask, 'Time'],
            format='%Y-%m-%d %H:%M:%S',
            errors='coerce'
        )
    
    return df


def filter_by_time(df: pd.DataFrame, start_time: str, end_time: str) -> pd.DataFrame:
    """Filter dataframe to only include rows within the time range."""
    start = datetime.strptime(start_time, "%H:%M:%S").time()
    end = datetime.strptime(end_time, "%H:%M:%S").time()
    
    df = df.dropna(subset=['DateTime'])
    df['TimeOnly'] = df['DateTime'].dt.time
    
    return df[(df['TimeOnly'] >= start) & (df['TimeOnly'] <= end)].copy()


def is_bullish_wickless(row: pd.Series) -> bool:
    """Check if a candle is bullish with no upper wick."""
    return row['Close'] > row['Open'] and row['High'] == row['Close']


def is_bearish_wickless(row: pd.Series) -> bool:
    """Check if a candle is bearish with no lower wick."""
    return row['Close'] < row['Open'] and row['Low'] == row['Close']


def has_min_body_size(row: pd.Series, min_size: float) -> bool:
    """Check if candle body meets minimum size requirement."""
    return abs(row['Close'] - row['Open']) >= min_size


def analyze_continuation(df: pd.DataFrame, min_body_size: float) -> Dict:
    """Analyze candle continuation for wickless candles."""
    results = {
        'total_candles': len(df),
        'bullish_wickless': 0,
        'bearish_wickless': 0,
        'bullish_continuation': 0,
        'bearish_continuation': 0,
    }
    
    # Sort by datetime to ensure proper sequence
    df = df.sort_values('DateTime').reset_index(drop=True)
    
    for i in range(len(df) - 1):
        current = df.iloc[i]
        next_candle = df.iloc[i + 1]
        
        # Check if body size meets minimum requirement
        if not has_min_body_size(current, min_body_size):
            continue
        
        # Check for bullish wickless candle
        if is_bullish_wickless(current):
            results['bullish_wickless'] += 1
            # Check continuation: next close > current close
            if next_candle['Close'] > current['Close']:
                results['bullish_continuation'] += 1
        
        # Check for bearish wickless candle
        elif is_bearish_wickless(current):
            results['bearish_wickless'] += 1
            # Check continuation: next close < current close
            if next_candle['Close'] < current['Close']:
                results['bearish_continuation'] += 1
    
    # Calculate probabilities
    results['total_wickless'] = results['bullish_wickless'] + results['bearish_wickless']
    results['total_continuation'] = results['bullish_continuation'] + results['bearish_continuation']
    
    if results['total_wickless'] > 0:
        results['continuation_probability'] = results['total_continuation'] / results['total_wickless'] * 100
    else:
        results['continuation_probability'] = 0
    
    if results['bullish_wickless'] > 0:
        results['bullish_continuation_probability'] = results['bullish_continuation'] / results['bullish_wickless'] * 100
    else:
        results['bullish_continuation_probability'] = 0
    
    if results['bearish_wickless'] > 0:
        results['bearish_continuation_probability'] = results['bearish_continuation'] / results['bearish_wickless'] * 100
    else:
        results['bearish_continuation_probability'] = 0
    
    return results


def get_file_path(year: int, timeframe: str) -> str:
    """Get the file path for a given year and timeframe."""
    csv_path = os.path.join(DATA_DIR, f"{year} {timeframe}.csv")
    zip_path = os.path.join(DATA_DIR, f"{year} {timeframe}.csv.zip")
    
    if os.path.exists(csv_path):
        return csv_path
    elif os.path.exists(zip_path):
        return extract_zip_if_needed(zip_path, DATA_DIR)
    else:
        return None


def load_all_data_for_timeframe(timeframe: str) -> pd.DataFrame:
    """Load all data for a given timeframe across all years."""
    all_data = []
    
    for year in YEARS:
        file_path = get_file_path(year, timeframe)
        if file_path and os.path.exists(file_path):
            print(f"  Loading {year} {timeframe}...")
            df = load_csv_data(file_path)
            all_data.append(df)
        else:
            print(f"  Warning: File not found for {year} {timeframe}")
    
    if all_data:
        return pd.concat(all_data, ignore_index=True)
    return pd.DataFrame()


def print_results(timeframe: str, results: Dict):
    """Print analysis results in a formatted way."""
    print(f"\n{'='*60}")
    print(f"TIMEFRAME: {timeframe.upper()}")
    print(f"{'='*60}")
    print(f"Minimum body size: {MIN_BODY_SIZE[timeframe]} points")
    print(f"\n📊 Analysis Results:")
    print(f"  Total candles analyzed: {results['total_candles']:,}")
    print(f"\n🕯️ Wickless Candles Found:")
    print(f"  • Bullish (no upper wick): {results['bullish_wickless']:,}")
    print(f"  • Bearish (no lower wick): {results['bearish_wickless']:,}")
    print(f"  • Total wickless candles: {results['total_wickless']:,}")
    print(f"\n✅ Continuation Candles:")
    print(f"  • Bullish continuation: {results['bullish_continuation']:,}")
    print(f"  • Bearish continuation: {results['bearish_continuation']:,}")
    print(f"  • Total continuation: {results['total_continuation']:,}")
    print(f"\n📈 Continuation Probabilities:")
    print(f"  • Overall probability: {results['continuation_probability']:.2f}%")
    print(f"  • Bullish continuation: {results['bullish_continuation_probability']:.2f}%")
    print(f"  • Bearish continuation: {results['bearish_continuation_probability']:.2f}%")


def main():
    """Main function to run the analysis."""
    print("=" * 60)
    print("CANDLE CONTINUATION PROBABILITY ANALYSIS")
    print("=" * 60)
    print(f"\nAnalysis Period: {min(YEARS)} - {max(YEARS)}")
    print(f"Time Filter: {TIME_FILTER_START} - {TIME_FILTER_END} (New York time)")
    print("\nCriteria:")
    print("  • Bullish wickless: Close > Open AND High == Close")
    print("  • Bearish wickless: Close < Open AND Low == Close")
    print("  • Bullish continuation: Next Close > Current Close")
    print("  • Bearish continuation: Next Close < Current Close")
    
    all_results = {}
    
    for timeframe in ['1m', '5m', '15m']:
        print(f"\n{'='*60}")
        print(f"Processing {timeframe} data...")
        print(f"{'='*60}")
        
        # Load all data for this timeframe
        df = load_all_data_for_timeframe(timeframe)
        
        if df.empty:
            print(f"No data found for {timeframe}")
            continue
        
        # Filter by time
        print(f"  Filtering data between {TIME_FILTER_START} and {TIME_FILTER_END}...")
        df_filtered = filter_by_time(df, TIME_FILTER_START, TIME_FILTER_END)
        print(f"  Candles in time range: {len(df_filtered):,} / {len(df):,}")
        
        # Analyze continuation
        print(f"  Analyzing continuation patterns...")
        results = analyze_continuation(df_filtered, MIN_BODY_SIZE[timeframe])
        all_results[timeframe] = results
        
        # Print results
        print_results(timeframe, results)
    
    # Print summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    print(f"\n{'Timeframe':<12} {'Wickless':<12} {'Continuation':<15} {'Probability':<12}")
    print("-" * 55)
    for tf, res in all_results.items():
        wickless_str = f"{res['total_wickless']:,}"
        continuation_str = f"{res['total_continuation']:,}"
        print(f"{tf:<12} {wickless_str:<12} {continuation_str:<15} {res['continuation_probability']:.2f}%")
    
    print("\n✅ Analysis complete!")


if __name__ == "__main__":
    main()

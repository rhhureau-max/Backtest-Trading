#!/usr/bin/env python3
"""
FVG (Fair Value Gap) Analysis Script for Nasdaq Mini Futures
Analyzes 8:30 AM Chicago candle FVGs across multiple timeframes (1m, 5m, 15m)
"""

import os
import zipfile
import io
import pandas as pd


def load_csv_data(filepath: str) -> pd.DataFrame:
    """Load CSV data from a file, handling both regular CSV and zipped CSV files."""
    if filepath.endswith('.zip'):
        with zipfile.ZipFile(filepath, 'r') as z:
            # Get the first CSV file in the archive
            csv_names = [n for n in z.namelist() if n.endswith('.csv')]
            if not csv_names:
                raise ValueError(f"No CSV file found in {filepath}")
            with z.open(csv_names[0]) as f:
                df = pd.read_csv(io.BytesIO(f.read()), sep=';')
    else:
        df = pd.read_csv(filepath, sep=';')
    
    return df


def prepare_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Parse dates and times, and prepare the dataframe for analysis."""
    # Rename columns to meaningful names
    df.columns = ['date', 'time', 'open', 'high', 'low', 'close', 'volume']
    
    # Parse datetime
    df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'], format='%d/%m/%Y %H:%M:%S')
    
    # Sort by datetime
    df = df.sort_values('datetime').reset_index(drop=True)
    
    return df


def load_all_data_for_timeframe(data_dir: str, timeframe: str, years: range) -> pd.DataFrame:
    """Load all data for a specific timeframe across multiple years."""
    all_data = []
    
    for year in years:
        # Determine file path
        if timeframe == '1m':
            if year == 2025:
                filepath = os.path.join(data_dir, f'{year} 1m.csv')
            else:
                filepath = os.path.join(data_dir, f'{year} 1m.csv.zip')
        else:
            filepath = os.path.join(data_dir, f'{year} {timeframe}.csv')
        
        # Check if file exists
        if not os.path.exists(filepath):
            print(f"Warning: File not found: {filepath}")
            continue
        
        try:
            df = load_csv_data(filepath)
            df = prepare_dataframe(df)
            all_data.append(df)
            print(f"  Loaded: {filepath} ({len(df)} rows)")
        except Exception as e:
            print(f"  Error loading {filepath}: {e}")
    
    if not all_data:
        return pd.DataFrame()
    
    # Concatenate all data
    combined = pd.concat(all_data, ignore_index=True)
    combined = combined.sort_values('datetime').reset_index(drop=True)
    
    return combined


def identify_fvg(df: pd.DataFrame, target_time: str = '08:30:00') -> pd.DataFrame:
    """
    Identify Fair Value Gaps (FVG) at a specific candle time.
    
    FVG Definition:
    - BULLISH FVG: LOW of candle N+1 > HIGH of candle N-1 (gap up)
    - BEARISH FVG: HIGH of candle N+1 < LOW of candle N-1 (gap down)
    
    The target candle is candle N (the 8:30:00 candle).
    
    Non-return criteria:
    - BULLISH FVG: Price does NOT go below LOW of N+1
    - BEARISH FVG: Price does NOT go above HIGH of N+1
    
    Note: df must have a sequential integer index (0, 1, 2, ...) as produced by
    reset_index(drop=True) in load_all_data_for_timeframe().
    """
    # Filter for target time candles - indices are positions in df
    target_candles = df[df['time'] == target_time].copy()
    
    fvg_data = []
    
    for idx in target_candles.index:
        # idx is a position in df (since df has sequential integer index)
        # We need idx-1 (N-1), idx (N), and idx+1 (N+1) to be valid positions
        if idx < 1 or idx >= len(df) - 1:
            continue
        
        # Get the three consecutive candles using positional indexing
        candle_n_minus_1 = df.iloc[idx - 1]
        candle_n = df.iloc[idx]
        candle_n_plus_1 = df.iloc[idx + 1]
        
        # Check for FVG
        high_n_minus_1 = candle_n_minus_1['high']
        low_n_minus_1 = candle_n_minus_1['low']
        low_n_plus_1 = candle_n_plus_1['low']
        high_n_plus_1 = candle_n_plus_1['high']
        
        fvg_type = None
        fvg_level = None
        
        # BULLISH FVG: LOW of N+1 > HIGH of N-1
        if low_n_plus_1 > high_n_minus_1:
            fvg_type = 'BULLISH'
            fvg_level = low_n_plus_1  # Non-return: price must not go below LOW of N+1
        # BEARISH FVG: HIGH of N+1 < LOW of N-1
        elif high_n_plus_1 < low_n_minus_1:
            fvg_type = 'BEARISH'
            fvg_level = high_n_plus_1  # Non-return: price must not go above HIGH of N+1
        
        if fvg_type:
            fvg_data.append({
                'datetime': candle_n['datetime'],
                'date': candle_n['date'],
                'fvg_type': fvg_type,
                'fvg_level': fvg_level,
                'high_n_minus_1': high_n_minus_1,
                'low_n_minus_1': low_n_minus_1,
                'open_n': candle_n['open'],
                'high_n': candle_n['high'],
                'low_n': candle_n['low'],
                'close_n': candle_n['close'],
                'low_n_plus_1': low_n_plus_1,
                'high_n_plus_1': high_n_plus_1,
                'idx_n': idx
            })
    
    return pd.DataFrame(fvg_data)


def calculate_non_return_probability(df: pd.DataFrame, fvg_df: pd.DataFrame, 
                                       horizons: list, entry_offset: int = 2) -> dict:
    """
    Calculate non-return probability for each horizon.
    
    Entry is at OPEN of candle N+entry_offset.
    - For 1m and 5m: entry_offset=2 (entry at 8h32 and 8h40 respectively)
    - For 15m: entry_offset=2 (entry at 9h00, i.e. 2 candles after 8h30)
    
    Non-return criteria:
    - BULLISH: Price does NOT go below LOW of N+1 (fvg_level)
    - BEARISH: Price does NOT go above HIGH of N+1 (fvg_level)
    """
    results = {
        'global': {h: {'non_return': 0, 'total': 0} for h in horizons},
        'bullish': {h: {'non_return': 0, 'total': 0} for h in horizons},
        'bearish': {h: {'non_return': 0, 'total': 0} for h in horizons}
    }
    
    for _, fvg in fvg_df.iterrows():
        idx_n = fvg['idx_n']
        fvg_type = fvg['fvg_type']
        fvg_level = fvg['fvg_level']
        
        # Entry at candle N+2
        entry_idx = idx_n + 2
        
        if entry_idx >= len(df):
            continue
        
        for horizon in horizons:
            # Check 'horizon' candles starting from entry (N+2)
            # iloc[entry_idx:entry_idx+horizon] gives exactly 'horizon' candles
            end_idx = entry_idx + horizon
            
            if end_idx > len(df):
                continue
            
            # Get price data for the horizon period
            horizon_data = df.iloc[entry_idx:end_idx]
            
            if len(horizon_data) == 0:
                continue
            
            # Check non-return condition
            non_return = False
            
            if fvg_type == 'BULLISH':
                # Price should NOT go below fvg_level (high of N-1)
                min_low = horizon_data['low'].min()
                non_return = min_low >= fvg_level
            else:  # BEARISH
                # Price should NOT go above fvg_level (low of N-1)
                max_high = horizon_data['high'].max()
                non_return = max_high <= fvg_level
            
            # Update counts
            results['global'][horizon]['total'] += 1
            results[fvg_type.lower()][horizon]['total'] += 1
            
            if non_return:
                results['global'][horizon]['non_return'] += 1
                results[fvg_type.lower()][horizon]['non_return'] += 1
    
    return results


def format_percentage(non_return: int, total: int) -> str:
    """Format percentage with proper handling of zero cases."""
    if total == 0:
        return "  N/A  "
    pct = (non_return / total) * 100
    return f"{pct:6.2f}%"


def print_results(timeframe: str, fvg_df: pd.DataFrame, results: dict, horizons: list):
    """Print formatted results for a timeframe."""
    total_fvg = len(fvg_df)
    bullish_count = len(fvg_df[fvg_df['fvg_type'] == 'BULLISH'])
    bearish_count = len(fvg_df[fvg_df['fvg_type'] == 'BEARISH'])
    
    # Format timeframe display
    if timeframe == '1m':
        tf_display = "1 MINUTE"
    elif timeframe == '5m':
        tf_display = "5 MINUTES"
    elif timeframe == '15m':
        tf_display = "15 MINUTES"
    else:
        tf_display = timeframe.upper()
    
    print(f"\nTIMEFRAME {tf_display}:")
    print(f"Total FVG détectés: {total_fvg} (Haussiers: {bullish_count}, Baissiers: {bearish_count})")
    print()
    print("Probabilité de NON-RETOUR dans le FVG:")
    print("Bougies |  Global  | Haussier | Baissier")
    print("--------|----------|----------|----------")
    
    for h in horizons:
        global_pct = format_percentage(
            results['global'][h]['non_return'],
            results['global'][h]['total']
        )
        bullish_pct = format_percentage(
            results['bullish'][h]['non_return'],
            results['bullish'][h]['total']
        )
        bearish_pct = format_percentage(
            results['bearish'][h]['non_return'],
            results['bearish'][h]['total']
        )
        
        print(f"   {h:2d}   | {global_pct} | {bullish_pct} | {bearish_pct}")


def main():
    """Main function to run the FVG analysis."""
    # Configuration
    data_dir = os.path.dirname(os.path.abspath(__file__))
    years = range(2018, 2026)
    timeframes = ['1m', '5m', '15m']
    horizons = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    target_time = '08:30:00'
    
    print("=" * 50)
    print("=== ANALYSE FVG 8h30 - Nasdaq Mini Futures ===")
    print("=" * 50)
    print(f"Période : {years.start}-{years.stop - 1}")
    print(f"Bougie cible : {target_time} (Chicago Time)")
    print()
    
    for timeframe in timeframes:
        print(f"\nChargement des données {timeframe}...")
        
        # Load data
        df = load_all_data_for_timeframe(data_dir, timeframe, years)
        
        if df.empty:
            print(f"Aucune donnée disponible pour le timeframe {timeframe}")
            continue
        
        print(f"Total: {len(df)} lignes chargées")
        
        # Identify FVGs
        fvg_df = identify_fvg(df, target_time)
        
        if fvg_df.empty:
            print(f"Aucun FVG détecté pour le timeframe {timeframe}")
            continue
        
        # Calculate non-return probabilities
        results = calculate_non_return_probability(df, fvg_df, horizons)
        
        # Print results
        print_results(timeframe, fvg_df, results, horizons)
    
    print("\n" + "=" * 50)
    print("Analyse terminée.")
    print("=" * 50)


if __name__ == "__main__":
    main()

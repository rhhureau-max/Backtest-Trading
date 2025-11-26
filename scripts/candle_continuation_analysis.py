#!/usr/bin/env python3
"""
Candle Continuation Analysis Script

This script analyzes candle continuations in the same direction after the 8:30 candle
for 1-minute, 5-minute, and 15-minute timeframes on data from 2018 to 2025.
"""

import os
import zipfile
from pathlib import Path
from collections import defaultdict

import pandas as pd


# Configuration
TIMEFRAME_CONFIG = {
    "1m": {"amplitude_threshold": 20, "suffix": "1m"},
    "5m": {"amplitude_threshold": 50, "suffix": "5m"},
    "15m": {"amplitude_threshold": 100, "suffix": "15m"},
}

YEARS = range(2018, 2026)  # 2018 to 2025 inclusive
TARGET_TIME = "08:30:00"
MAX_CONTINUATIONS = 5


def get_repo_root() -> Path:
    """Get the repository root directory."""
    script_dir = Path(__file__).resolve().parent
    return script_dir.parent


def find_data_file(repo_root: Path, year: int, timeframe: str) -> Path | None:
    """Find the data file for a given year and timeframe."""
    suffix = TIMEFRAME_CONFIG[timeframe]["suffix"]
    
    # Try uncompressed CSV first
    csv_path = repo_root / f"{year} {suffix}.csv"
    if csv_path.exists():
        return csv_path
    
    # Try compressed ZIP
    zip_path = repo_root / f"{year} {suffix}.csv.zip"
    if zip_path.exists():
        return zip_path
    
    return None


def load_data(file_path: Path) -> pd.DataFrame:
    """Load data from CSV or ZIP file."""
    if file_path.suffix == ".zip":
        with zipfile.ZipFile(file_path, 'r') as z:
            # Get the first CSV file in the archive
            csv_files = [f for f in z.namelist() if f.endswith('.csv')]
            if not csv_files:
                raise ValueError(f"No CSV file found in {file_path}")
            with z.open(csv_files[0]) as f:
                df = pd.read_csv(f, sep=';', header=0)
    else:
        df = pd.read_csv(file_path, sep=';', header=0)
    
    # Rename columns for clarity
    df.columns = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
    
    return df


def filter_trading_days(df: pd.DataFrame) -> pd.DataFrame:
    """Filter to only include rows where 8:30 candle exists."""
    # Convert Date and Time to proper format
    df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%d/%m/%Y %H:%M:%S')
    df['TimeOnly'] = df['Time']
    return df


def analyze_continuations(
    df: pd.DataFrame, 
    timeframe: str
) -> dict:
    """
    Analyze candle continuations for a given dataframe and timeframe.
    
    Returns a dictionary with results for bullish and bearish first candles.
    """
    threshold = TIMEFRAME_CONFIG[timeframe]["amplitude_threshold"]
    
    results = {
        "bullish": {
            "total_qualified": 0,
            "continuations": {i: {"count": 0, "total_points": 0.0} for i in range(1, MAX_CONTINUATIONS + 1)}
        },
        "bearish": {
            "total_qualified": 0,
            "continuations": {i: {"count": 0, "total_points": 0.0} for i in range(1, MAX_CONTINUATIONS + 1)}
        }
    }
    
    # Filter for 8:30 candles
    df_830 = df[df['TimeOnly'] == TARGET_TIME].copy()
    
    if df_830.empty:
        return results
    
    # Get all unique dates with 8:30 candles
    for _, row_830 in df_830.iterrows():
        open_price = row_830['Open']
        close_price = row_830['Close']
        amplitude = abs(close_price - open_price)
        
        # Check if candle qualifies based on amplitude
        if amplitude < threshold:
            continue
        
        # Determine direction
        if close_price > open_price:
            direction = "bullish"
        elif close_price < open_price:
            direction = "bearish"
        else:
            continue  # Skip doji candles
        
        results[direction]["total_qualified"] += 1
        
        # Get subsequent candles on the same day
        current_datetime = row_830['DateTime']
        current_date = current_datetime.date()
        
        # Find subsequent candles after 8:30 on the same day
        subsequent = df[
            (df['DateTime'] > current_datetime) & 
            (df['DateTime'].dt.date == current_date)
        ].sort_values('DateTime').head(MAX_CONTINUATIONS)
        
        if subsequent.empty:
            continue
        
        # Analyze continuations
        reference_close = close_price
        consecutive_count = 0
        
        for idx, (_, next_candle) in enumerate(subsequent.iterrows(), 1):
            next_open = next_candle['Open']
            next_close = next_candle['Close']
            
            # Check if candle continues in the same direction
            if direction == "bullish":
                continues = next_close > next_open  # Bullish continuation
            else:
                continues = next_close < next_open  # Bearish continuation
            
            if continues:
                consecutive_count = idx
                # Calculate points from original 8:30 close to current close
                if direction == "bullish":
                    points = next_close - reference_close
                else:
                    points = reference_close - next_close
                
                results[direction]["continuations"][idx]["count"] += 1
                results[direction]["continuations"][idx]["total_points"] += points
            else:
                break  # Stop counting on first non-continuation
    
    return results


def aggregate_results(all_results: list[dict]) -> dict:
    """Aggregate results from multiple years."""
    aggregated = {
        "bullish": {
            "total_qualified": 0,
            "continuations": {i: {"count": 0, "total_points": 0.0} for i in range(1, MAX_CONTINUATIONS + 1)}
        },
        "bearish": {
            "total_qualified": 0,
            "continuations": {i: {"count": 0, "total_points": 0.0} for i in range(1, MAX_CONTINUATIONS + 1)}
        }
    }
    
    for result in all_results:
        for direction in ["bullish", "bearish"]:
            aggregated[direction]["total_qualified"] += result[direction]["total_qualified"]
            for i in range(1, MAX_CONTINUATIONS + 1):
                aggregated[direction]["continuations"][i]["count"] += result[direction]["continuations"][i]["count"]
                aggregated[direction]["continuations"][i]["total_points"] += result[direction]["continuations"][i]["total_points"]
    
    return aggregated


def format_results(results: dict, direction: str, direction_label: str) -> str:
    """Format results for display."""
    output = []
    total = results[direction]["total_qualified"]
    
    output.append(f"\n  {direction_label}:")
    output.append(f"    Total premières bougies 8h30 qualifiées: {total}")
    
    if total == 0:
        output.append("    Aucune donnée disponible")
        return "\n".join(output)
    
    output.append("    Continuations:")
    for i in range(1, MAX_CONTINUATIONS + 1):
        count = results[direction]["continuations"][i]["count"]
        total_points = results[direction]["continuations"][i]["total_points"]
        ratio = (count / total) * 100 if total > 0 else 0
        avg_points = total_points / count if count > 0 else 0
        
        output.append(f"      {i} bougie(s): {count} fois ({ratio:.1f}%) - Moyenne: {avg_points:.2f} points")
    
    return "\n".join(output)


def main():
    """Main function to run the analysis."""
    repo_root = get_repo_root()
    
    print("=" * 80)
    print("ANALYSE DES CONTINUATIONS DE BOUGIES APRÈS 8H30")
    print("=" * 80)
    
    for timeframe in TIMEFRAME_CONFIG:
        print(f"\n{'=' * 80}")
        print(f"TIMEFRAME: {timeframe.upper()}")
        print(f"Seuil d'amplitude: >= {TIMEFRAME_CONFIG[timeframe]['amplitude_threshold']} points")
        print("=" * 80)
        
        yearly_results = []
        
        for year in YEARS:
            file_path = find_data_file(repo_root, year, timeframe)
            
            if file_path is None:
                print(f"\n  Année {year}: Fichier non trouvé")
                continue
            
            try:
                df = load_data(file_path)
                df = filter_trading_days(df)
                results = analyze_continuations(df, timeframe)
                yearly_results.append(results)
                
                print(f"\n--- Année {year} ---")
                print(format_results(results, "bullish", "Haussières"))
                print(format_results(results, "bearish", "Baissières"))
                
            except Exception as e:
                print(f"\n  Année {year}: Erreur lors du traitement - {e}")
        
        # Aggregate all years
        if yearly_results:
            print(f"\n{'=' * 60}")
            print(f"RÉSUMÉ GLOBAL {timeframe.upper()} (2018-2025)")
            print("=" * 60)
            
            aggregated = aggregate_results(yearly_results)
            print(format_results(aggregated, "bullish", "Haussières"))
            print(format_results(aggregated, "bearish", "Baissières"))
    
    print("\n" + "=" * 80)
    print("ANALYSE TERMINÉE")
    print("=" * 80)


if __name__ == "__main__":
    main()

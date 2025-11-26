#!/usr/bin/env python3
"""
Breakout Strategy Analysis Script (RR 1:1)

This script analyzes a breakout strategy based on the 8:30 candle:
- Entry: If 8:30 candle closes above/below the previous 5 candles, enter at close
- Stop Loss: At the middle of the 8:30 candle body
- Take Profit: Same distance as SL (Risk-Reward 1:1)

Analyzes win rate and qualification rate for 1-minute, 5-minute, and 15-minute timeframes.
"""

import zipfile
from pathlib import Path

import pandas as pd


YEARS = range(2018, 2026)
TARGET_TIME = "08:30:00"

# Timeframes to analyze
TIMEFRAMES = ["1m", "5m", "15m"]


def get_repo_root() -> Path:
    script_dir = Path(__file__).resolve().parent
    return script_dir.parent


def find_data_file(repo_root: Path, year: int, suffix: str) -> Path | None:
    csv_path = repo_root / f"{year} {suffix}.csv"
    if csv_path.exists():
        return csv_path
    zip_path = repo_root / f"{year} {suffix}.csv.zip"
    if zip_path.exists():
        return zip_path
    return None


def load_data(file_path: Path) -> pd.DataFrame:
    if file_path.suffix == ".zip":
        with zipfile.ZipFile(file_path, 'r') as z:
            csv_files = [f for f in z.namelist() if f.endswith('.csv')]
            if not csv_files:
                raise ValueError(f"No CSV file found in {file_path}")
            with z.open(csv_files[0]) as f:
                df = pd.read_csv(f, sep=';', header=0)
    else:
        df = pd.read_csv(file_path, sep=';', header=0)
    
    df.columns = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
    df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%d/%m/%Y %H:%M:%S')
    df['TimeOnly'] = df['Time']
    return df


def get_previous_candles(df: pd.DataFrame, current_idx: int, count: int = 5) -> pd.DataFrame:
    """Get the previous N candles before the current index."""
    start_idx = max(0, current_idx - count)
    return df.iloc[start_idx:current_idx]


def check_breakout(candle_830: pd.Series, prev_candles: pd.DataFrame) -> str | None:
    """
    Check if the 8:30 candle closes above or below all previous 5 candles.
    Returns 'bullish', 'bearish', or None.
    """
    if len(prev_candles) < 5:
        return None
    
    close_830 = candle_830['Close']
    
    # Get the highest high and lowest low of previous 5 candles
    prev_highest_close = prev_candles['Close'].max()
    prev_lowest_close = prev_candles['Close'].min()
    
    # Bullish breakout: close above all previous closes
    if close_830 > prev_highest_close:
        return 'bullish'
    
    # Bearish breakout: close below all previous closes
    if close_830 < prev_lowest_close:
        return 'bearish'
    
    return None


def simulate_trade(df: pd.DataFrame, entry_idx: int, direction: str, 
                   entry_price: float, sl_distance: float) -> dict:
    """
    Simulate a trade with RR 1:1.
    Returns trade result with outcome (win/loss/pending).
    """
    tp_distance = sl_distance  # RR = 1:1
    
    if direction == 'bullish':
        sl_price = entry_price - sl_distance
        tp_price = entry_price + tp_distance
    else:  # bearish
        sl_price = entry_price + sl_distance
        tp_price = entry_price - tp_distance
    
    # Get subsequent candles on the same day
    entry_datetime = df.iloc[entry_idx]['DateTime']
    entry_date = entry_datetime.date()
    
    subsequent = df.iloc[entry_idx + 1:]
    subsequent = subsequent[subsequent['DateTime'].dt.date == entry_date]
    
    for _, candle in subsequent.iterrows():
        high = candle['High']
        low = candle['Low']
        
        if direction == 'bullish':
            # Check if TP hit first (optimistic assumption: if both hit same candle, TP wins)
            if high >= tp_price:
                return {'outcome': 'win', 'hit_price': tp_price}
            if low <= sl_price:
                return {'outcome': 'loss', 'hit_price': sl_price}
        else:  # bearish
            if low <= tp_price:
                return {'outcome': 'win', 'hit_price': tp_price}
            if high >= sl_price:
                return {'outcome': 'loss', 'hit_price': sl_price}
    
    # If we reach end of day without hitting either
    return {'outcome': 'pending', 'hit_price': None}


def analyze_breakout_strategy(df: pd.DataFrame) -> dict:
    """
    Analyze the breakout strategy for a given dataframe.
    """
    results = {
        'bullish': {
            'qualified': 0,
            'wins': 0,
            'losses': 0,
            'pending': 0,
            'total_points_won': 0.0,
            'total_points_lost': 0.0
        },
        'bearish': {
            'qualified': 0,
            'wins': 0,
            'losses': 0,
            'pending': 0,
            'total_points_won': 0.0,
            'total_points_lost': 0.0
        },
        'total_830_candles': 0
    }
    
    # Find all 8:30 candles
    df_830_indices = df[df['TimeOnly'] == TARGET_TIME].index.tolist()
    
    for idx in df_830_indices:
        results['total_830_candles'] += 1
        
        candle_830 = df.loc[idx]
        
        # Get the actual position in the dataframe
        pos = df.index.get_loc(idx)
        prev_candles = get_previous_candles(df, pos, 5)
        
        # Check if this is a breakout candle
        direction = check_breakout(candle_830, prev_candles)
        
        if direction is None:
            continue
        
        results[direction]['qualified'] += 1
        
        # Calculate SL distance (half of candle body)
        open_price = candle_830['Open']
        close_price = candle_830['Close']
        body_size = abs(close_price - open_price)
        sl_distance = body_size / 2
        
        if sl_distance == 0:
            continue  # Skip doji candles
        
        # Simulate the trade
        trade_result = simulate_trade(df, pos, direction, close_price, sl_distance)
        
        if trade_result['outcome'] == 'win':
            results[direction]['wins'] += 1
            results[direction]['total_points_won'] += sl_distance
        elif trade_result['outcome'] == 'loss':
            results[direction]['losses'] += 1
            results[direction]['total_points_lost'] += sl_distance
        else:
            results[direction]['pending'] += 1
    
    return results


def aggregate_results(all_results: list[dict]) -> dict:
    """Aggregate results from multiple years."""
    aggregated = {
        'bullish': {
            'qualified': 0,
            'wins': 0,
            'losses': 0,
            'pending': 0,
            'total_points_won': 0.0,
            'total_points_lost': 0.0
        },
        'bearish': {
            'qualified': 0,
            'wins': 0,
            'losses': 0,
            'pending': 0,
            'total_points_won': 0.0,
            'total_points_lost': 0.0
        },
        'total_830_candles': 0
    }
    
    for result in all_results:
        aggregated['total_830_candles'] += result['total_830_candles']
        for direction in ['bullish', 'bearish']:
            for key in ['qualified', 'wins', 'losses', 'pending', 'total_points_won', 'total_points_lost']:
                aggregated[direction][key] += result[direction][key]
    
    return aggregated


def format_results(results: dict) -> str:
    """Format results for display."""
    output = []
    
    total_830 = results['total_830_candles']
    
    for direction, label in [('bullish', 'Haussier'), ('bearish', 'Baissier')]:
        data = results[direction]
        qualified = data['qualified']
        wins = data['wins']
        losses = data['losses']
        pending = data['pending']
        completed = wins + losses
        
        output.append(f"\n  {label}:")
        output.append(f"    Bougies 8h30 qualifiées (breakout): {qualified}")
        
        if total_830 > 0:
            qualification_rate = (qualified / total_830) * 100
            output.append(f"    Taux de qualification: {qualification_rate:.1f}% ({qualified}/{total_830})")
        
        if completed > 0:
            win_rate = (wins / completed) * 100
            output.append(f"    Trades complétés: {completed}")
            output.append(f"    Gains (TP touché): {wins} ({win_rate:.1f}%)")
            output.append(f"    Pertes (SL touché): {losses} ({100-win_rate:.1f}%)")
            
            if pending > 0:
                output.append(f"    En attente (fin de journée): {pending}")
            
            avg_points_won = data['total_points_won'] / wins if wins > 0 else 0
            avg_points_lost = data['total_points_lost'] / losses if losses > 0 else 0
            output.append(f"    Points moyens gagnés: {avg_points_won:.2f}")
            output.append(f"    Points moyens perdus: {avg_points_lost:.2f}")
        else:
            output.append("    Aucun trade complété")
    
    return "\n".join(output)


def main():
    repo_root = get_repo_root()
    
    print("=" * 100)
    print("ANALYSE DE LA STRATÉGIE BREAKOUT 8H30 (RR 1:1)")
    print("=" * 100)
    print("\nConditions:")
    print("  - Entrée: Si la bougie 8h30 clôture AU-DESSUS ou EN-DESSOUS des 5 bougies précédentes")
    print("  - Stop Loss: Au milieu du corps de la bougie 8h30")
    print("  - Take Profit: Même distance que le SL (RR = 1:1)")
    print("=" * 100)
    
    for timeframe in TIMEFRAMES:
        print(f"\n{'=' * 80}")
        print(f"TIMEFRAME: {timeframe.upper()}")
        print("=" * 80)
        
        yearly_results = []
        
        for year in YEARS:
            file_path = find_data_file(repo_root, year, timeframe)
            
            if file_path is None:
                print(f"\n  Année {year}: Fichier non trouvé")
                continue
            
            try:
                df = load_data(file_path)
                results = analyze_breakout_strategy(df)
                yearly_results.append(results)
                
                print(f"\n--- Année {year} ---")
                print(format_results(results))
                
            except Exception as e:
                print(f"\n  Année {year}: Erreur lors du traitement - {e}")
        
        # Aggregate all years
        if yearly_results:
            print(f"\n{'=' * 60}")
            print(f"RÉSUMÉ GLOBAL {timeframe.upper()} (2018-2025)")
            print("=" * 60)
            
            aggregated = aggregate_results(yearly_results)
            print(format_results(aggregated))
    
    print("\n" + "=" * 100)
    print("ANALYSE TERMINÉE")
    print("=" * 100)


if __name__ == "__main__":
    main()

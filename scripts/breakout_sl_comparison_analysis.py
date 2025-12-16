#!/usr/bin/env python3
"""
Breakout Strategy Analysis Script - SL Placement Comparison

This script analyzes a breakout strategy with different Stop Loss placements:
- 100% (SL at the full body of the 8h30 candle)
- 25% retracement (SL at 25% of body from entry)
- 75% retracement (SL at 75% of body from entry)

Analyzes RR from 1.0 to 5.0 for all 3 timeframes (1M, 5M, 15M).
"""

import zipfile
from pathlib import Path

import pandas as pd


YEARS = range(2018, 2026)
TARGET_TIME = "08:30:00"
TIMEFRAMES = ["1m", "5m", "15m"]
RR_RATIOS = [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]
SL_PLACEMENTS = {
    '100%': 1.0,   # SL at full body (under/above the whole candle body)
    '25%': 0.25,   # SL at 25% retracement
    '75%': 0.75    # SL at 75% retracement
}
LOOKBACK = 5


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
    start_idx = max(0, current_idx - count)
    return df.iloc[start_idx:current_idx]


def check_breakout(candle_830: pd.Series, prev_candles: pd.DataFrame) -> str | None:
    if len(prev_candles) < LOOKBACK:
        return None
    
    close_830 = candle_830['Close']
    prev_highest_close = prev_candles['Close'].max()
    prev_lowest_close = prev_candles['Close'].min()
    
    if close_830 > prev_highest_close:
        return 'bullish'
    if close_830 < prev_lowest_close:
        return 'bearish'
    return None


def simulate_trade(df: pd.DataFrame, entry_idx: int, direction: str, 
                   entry_price: float, sl_distance: float, rr_ratio: float) -> dict:
    tp_distance = sl_distance * rr_ratio
    
    if direction == 'bullish':
        sl_price = entry_price - sl_distance
        tp_price = entry_price + tp_distance
    else:
        sl_price = entry_price + sl_distance
        tp_price = entry_price - tp_distance
    
    entry_datetime = df.iloc[entry_idx]['DateTime']
    entry_date = entry_datetime.date()
    
    subsequent = df.iloc[entry_idx + 1:]
    subsequent = subsequent[subsequent['DateTime'].dt.date == entry_date]
    
    for _, candle in subsequent.iterrows():
        high = candle['High']
        low = candle['Low']
        
        if direction == 'bullish':
            if high >= tp_price:
                return {'outcome': 'win', 'points': tp_distance}
            if low <= sl_price:
                return {'outcome': 'loss', 'points': sl_distance}
        else:
            if low <= tp_price:
                return {'outcome': 'win', 'points': tp_distance}
            if high >= sl_price:
                return {'outcome': 'loss', 'points': sl_distance}
    
    return {'outcome': 'pending', 'points': 0}


def analyze_breakout_strategy(df: pd.DataFrame, rr_ratio: float, sl_percent: float) -> dict:
    results = {
        'bullish': {
            'qualified': 0, 'wins': 0, 'losses': 0, 'pending': 0,
            'total_points_won': 0.0, 'total_points_lost': 0.0
        },
        'bearish': {
            'qualified': 0, 'wins': 0, 'losses': 0, 'pending': 0,
            'total_points_won': 0.0, 'total_points_lost': 0.0
        },
        'total_830_candles': 0
    }
    
    df_830_indices = df[df['TimeOnly'] == TARGET_TIME].index.tolist()
    
    for idx in df_830_indices:
        results['total_830_candles'] += 1
        candle_830 = df.loc[idx]
        pos = df.index.get_loc(idx)
        prev_candles = get_previous_candles(df, pos, LOOKBACK)
        direction = check_breakout(candle_830, prev_candles)
        
        if direction is None:
            continue
        
        results[direction]['qualified'] += 1
        
        open_price = candle_830['Open']
        close_price = candle_830['Close']
        body_size = abs(close_price - open_price)
        
        # SL distance based on placement percentage
        sl_distance = body_size * sl_percent
        
        if sl_distance == 0:
            continue
        
        trade_result = simulate_trade(df, pos, direction, close_price, sl_distance, rr_ratio)
        
        if trade_result['outcome'] == 'win':
            results[direction]['wins'] += 1
            results[direction]['total_points_won'] += trade_result['points']
        elif trade_result['outcome'] == 'loss':
            results[direction]['losses'] += 1
            results[direction]['total_points_lost'] += trade_result['points']
        else:
            results[direction]['pending'] += 1
    
    return results


def aggregate_results(all_results: list[dict]) -> dict:
    aggregated = {
        'bullish': {
            'qualified': 0, 'wins': 0, 'losses': 0, 'pending': 0,
            'total_points_won': 0.0, 'total_points_lost': 0.0
        },
        'bearish': {
            'qualified': 0, 'wins': 0, 'losses': 0, 'pending': 0,
            'total_points_won': 0.0, 'total_points_lost': 0.0
        },
        'total_830_candles': 0
    }
    
    for result in all_results:
        aggregated['total_830_candles'] += result['total_830_candles']
        for direction in ['bullish', 'bearish']:
            for key in ['qualified', 'wins', 'losses', 'pending', 'total_points_won', 'total_points_lost']:
                aggregated[direction][key] += result[direction][key]
    
    return aggregated


def calculate_win_rate(results: dict) -> tuple:
    total_wins = results['bullish']['wins'] + results['bearish']['wins']
    total_losses = results['bullish']['losses'] + results['bearish']['losses']
    total = total_wins + total_losses
    
    if total > 0:
        win_rate = (total_wins / total) * 100
        return win_rate, total
    return 0.0, 0


def calculate_expectancy(results: dict, rr_ratio: float) -> float:
    total_wins = results['bullish']['wins'] + results['bearish']['wins']
    total_losses = results['bullish']['losses'] + results['bearish']['losses']
    total = total_wins + total_losses
    
    if total == 0:
        return 0.0
    
    total_points_won = results['bullish']['total_points_won'] + results['bearish']['total_points_won']
    total_points_lost = results['bullish']['total_points_lost'] + results['bearish']['total_points_lost']
    
    avg_win = total_points_won / total_wins if total_wins > 0 else 0
    avg_loss = total_points_lost / total_losses if total_losses > 0 else 0
    
    expectancy = (total_wins * avg_win - total_losses * avg_loss) / total
    return expectancy


def main():
    repo_root = get_repo_root()
    
    print("=" * 120)
    print("ANALYSE DE LA STRATÉGIE BREAKOUT 8H30 - COMPARAISON DES PLACEMENTS DE STOP LOSS")
    print("=" * 120)
    print("\nConditions:")
    print("  - Entrée: Si la bougie 8h30 clôture AU-DESSUS ou EN-DESSOUS des 5 bougies précédentes")
    print("  - Placements SL testés:")
    print("    * 100% : SL sous/dessus le corps entier de la bougie 8h30")
    print("    * 25%  : SL à 25% du corps (retracement court)")
    print("    * 75%  : SL à 75% du corps (retracement long)")
    print("  - RR testés: 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0")
    print("=" * 120)
    
    # Store all results: {sl_placement: {rr: {timeframe: results}}}
    all_results = {sl_name: {rr: {} for rr in RR_RATIOS} for sl_name in SL_PLACEMENTS}
    
    for sl_name, sl_percent in SL_PLACEMENTS.items():
        print(f"\n{'#' * 120}")
        print(f"# PLACEMENT SL: {sl_name} du corps de la bougie")
        print('#' * 120)
        
        for timeframe in TIMEFRAMES:
            print(f"\n{'=' * 80}")
            print(f"TIMEFRAME: {timeframe.upper()} | SL: {sl_name}")
            print("=" * 80)
            
            # Load data once per timeframe
            all_dfs = []
            for year in YEARS:
                file_path = find_data_file(repo_root, year, timeframe)
                if file_path is not None:
                    try:
                        df = load_data(file_path)
                        all_dfs.append((year, df))
                    except Exception as e:
                        print(f"  Année {year}: Erreur - {e}")
            
            for rr in RR_RATIOS:
                yearly_results = []
                
                for year, df in all_dfs:
                    try:
                        results = analyze_breakout_strategy(df, rr, sl_percent)
                        yearly_results.append(results)
                    except Exception as e:
                        pass
                
                if yearly_results:
                    aggregated = aggregate_results(yearly_results)
                    all_results[sl_name][rr][timeframe] = aggregated
                    
                    win_rate, total = calculate_win_rate(aggregated)
                    expectancy = calculate_expectancy(aggregated, rr)
                    print(f"  RR {rr}: Win Rate = {win_rate:.1f}% ({total} trades), Espérance = {expectancy:.2f} pts")
    
    # Print comparison tables
    print("\n" + "=" * 120)
    print("TABLEAUX COMPARATIFS - WIN RATE PAR PLACEMENT SL, RR ET TIMEFRAME")
    print("=" * 120)
    
    for sl_name in SL_PLACEMENTS:
        print(f"\n{'=' * 100}")
        print(f"PLACEMENT SL: {sl_name}")
        print("=" * 100)
        
        header = f"{'TF':<6} |"
        for rr in RR_RATIOS:
            header += f" RR {rr:>3} |"
        print(header)
        print("-" * (8 + 10 * len(RR_RATIOS)))
        
        for tf in TIMEFRAMES:
            row = f"{tf.upper():<6} |"
            for rr in RR_RATIOS:
                if tf in all_results[sl_name][rr]:
                    win_rate, total = calculate_win_rate(all_results[sl_name][rr][tf])
                    row += f" {win_rate:>5.1f}% |"
                else:
                    row += f" {'N/A':>6} |"
            print(row)
    
    # Print expectancy comparison
    print("\n" + "=" * 120)
    print("TABLEAUX COMPARATIFS - ESPÉRANCE PAR TRADE (pts)")
    print("=" * 120)
    
    for sl_name in SL_PLACEMENTS:
        print(f"\n{'=' * 100}")
        print(f"PLACEMENT SL: {sl_name}")
        print("=" * 100)
        
        header = f"{'TF':<6} |"
        for rr in RR_RATIOS:
            header += f" RR {rr:>3} |"
        print(header)
        print("-" * (8 + 10 * len(RR_RATIOS)))
        
        for tf in TIMEFRAMES:
            row = f"{tf.upper():<6} |"
            for rr in RR_RATIOS:
                if tf in all_results[sl_name][rr]:
                    expectancy = calculate_expectancy(all_results[sl_name][rr][tf], rr)
                    row += f" {expectancy:>+6.1f} |"
                else:
                    row += f" {'N/A':>7} |"
            print(row)
    
    # Best configuration summary
    print("\n" + "=" * 120)
    print("MEILLEURE CONFIGURATION PAR TIMEFRAME")
    print("=" * 120)
    
    for tf in TIMEFRAMES:
        best_config = None
        best_expectancy = float('-inf')
        
        for sl_name in SL_PLACEMENTS:
            for rr in RR_RATIOS:
                if tf in all_results[sl_name][rr]:
                    exp = calculate_expectancy(all_results[sl_name][rr][tf], rr)
                    if exp > best_expectancy:
                        best_expectancy = exp
                        win_rate, total = calculate_win_rate(all_results[sl_name][rr][tf])
                        best_config = (sl_name, rr, win_rate, total, exp)
        
        if best_config:
            sl_name, rr, win_rate, total, exp = best_config
            print(f"\n{tf.upper()}:")
            print(f"  Meilleur: SL {sl_name} avec RR {rr}")
            print(f"  Win Rate: {win_rate:.1f}% ({total} trades)")
            print(f"  Espérance: {exp:+.2f} pts/trade")
    
    print("\n" + "=" * 120)
    print("ANALYSE TERMINÉE")
    print("=" * 120)


if __name__ == "__main__":
    main()

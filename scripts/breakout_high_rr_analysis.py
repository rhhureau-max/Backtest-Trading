#!/usr/bin/env python3
"""
Breakout Strategy Analysis Script (High RR: 3.0, 3.5, 4.0, 4.5, 5.0)

This script analyzes a breakout strategy based on the 8:30 candle with high RR ratios:
- Entry: If 8:30 candle closes above/below the previous 5 candles, enter at close
- Stop Loss: At the middle of the 8:30 candle body
- Take Profit: Variable based on RR (3.0, 3.5, 4.0, 4.5, 5.0)

Analyzes win rate and qualification rate for 1-minute, 5-minute, and 15-minute timeframes.
"""

import zipfile
from pathlib import Path

import pandas as pd


YEARS = range(2018, 2026)
TARGET_TIME = "08:30:00"
TIMEFRAMES = ["1m", "5m", "15m"]
RR_RATIOS = [3.0, 3.5, 4.0, 4.5, 5.0]
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


def analyze_breakout_strategy(df: pd.DataFrame, rr_ratio: float) -> dict:
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
        sl_distance = body_size / 2
        
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


def format_results(results: dict, rr_ratio: float) -> str:
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
            output.append(f"    Taux de qualification: {qualification_rate:.1f}%")
        
        if completed > 0:
            win_rate = (wins / completed) * 100
            output.append(f"    Trades complétés: {completed}")
            output.append(f"    Gains (TP touché): {wins} ({win_rate:.1f}%)")
            output.append(f"    Pertes (SL touché): {losses} ({100-win_rate:.1f}%)")
            
            if pending > 0:
                output.append(f"    En attente (fin de journée): {pending}")
            
            avg_points_won = data['total_points_won'] / wins if wins > 0 else 0
            avg_points_lost = data['total_points_lost'] / losses if losses > 0 else 0
            output.append(f"    Points moyens gagnés: {avg_points_won:.2f} (RR {rr_ratio})")
            output.append(f"    Points moyens perdus: {avg_points_lost:.2f}")
            
            # Calculate expectancy
            if completed > 0:
                expectancy = (wins * avg_points_won - losses * avg_points_lost) / completed
                output.append(f"    Espérance par trade: {expectancy:.2f} pts")
        else:
            output.append("    Aucun trade complété")
    
    return "\n".join(output)


def main():
    repo_root = get_repo_root()
    
    print("=" * 100)
    print("ANALYSE DE LA STRATÉGIE BREAKOUT 8H30 - HIGH RR (3.0, 3.5, 4.0, 4.5, 5.0)")
    print("=" * 100)
    print("\nConditions:")
    print("  - Entrée: Si la bougie 8h30 clôture AU-DESSUS ou EN-DESSOUS des 5 bougies précédentes")
    print("  - Stop Loss: Au milieu du corps de la bougie 8h30")
    print("  - Take Profit: Variable selon le RR (3x, 3.5x, 4x, 4.5x, 5x le SL)")
    print("=" * 100)
    
    all_global_results = {}
    
    for rr in RR_RATIOS:
        all_global_results[rr] = {}
        
        print(f"\n{'#' * 100}")
        print(f"# RR = {rr}")
        print('#' * 100)
        
        for timeframe in TIMEFRAMES:
            print(f"\n{'=' * 80}")
            print(f"TIMEFRAME: {timeframe.upper()} | RR: {rr}")
            print("=" * 80)
            
            yearly_results = []
            
            for year in YEARS:
                file_path = find_data_file(repo_root, year, timeframe)
                
                if file_path is None:
                    continue
                
                try:
                    df = load_data(file_path)
                    results = analyze_breakout_strategy(df, rr)
                    yearly_results.append(results)
                    
                    print(f"\n--- Année {year} ---")
                    print(format_results(results, rr))
                    
                except Exception as e:
                    print(f"\n  Année {year}: Erreur - {e}")
            
            if yearly_results:
                print(f"\n{'=' * 60}")
                print(f"RÉSUMÉ GLOBAL {timeframe.upper()} | RR: {rr} (2018-2025)")
                print("=" * 60)
                
                aggregated = aggregate_results(yearly_results)
                all_global_results[rr][timeframe] = aggregated
                print(format_results(aggregated, rr))
    
    # Print comparison summary
    print("\n" + "=" * 100)
    print("TABLEAU COMPARATIF - WIN RATE PAR RR ET TIMEFRAME")
    print("=" * 100)
    
    print(f"\n{'Timeframe':<12} | {'RR 3.0':^20} | {'RR 3.5':^20} | {'RR 4.0':^20} | {'RR 4.5':^20} | {'RR 5.0':^20}")
    print("-" * 120)
    
    for tf in TIMEFRAMES:
        row = f"{tf.upper():<12} |"
        for rr in RR_RATIOS:
            if tf in all_global_results[rr]:
                data = all_global_results[rr][tf]
                total_wins = data['bullish']['wins'] + data['bearish']['wins']
                total_losses = data['bullish']['losses'] + data['bearish']['losses']
                total = total_wins + total_losses
                if total > 0:
                    win_rate = (total_wins / total) * 100
                    row += f" {win_rate:>5.1f}% ({total:>4}) |"
                else:
                    row += f" {'N/A':^18} |"
            else:
                row += f" {'N/A':^18} |"
        print(row)
    
    print("\n" + "=" * 100)
    print("ANALYSE TERMINÉE")
    print("=" * 100)


if __name__ == "__main__":
    main()

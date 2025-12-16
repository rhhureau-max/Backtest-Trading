#!/usr/bin/env python3
"""
Breakout Strategy Analysis - Multiple Entry Conditions

This script analyzes a breakout strategy with different entry conditions:
- Entry: If 8:30 candle closes above/below the previous N candles (5, 6, 7, 8, 9, 10, 15)
- Stop Loss: At the middle of the 8:30 candle body
- Take Profit: Variable based on RR (1.0, 1.5, 2.0, 2.5)

Compares win rates across different lookback periods and RR ratios.
"""

import zipfile
from pathlib import Path

import pandas as pd


YEARS = range(2018, 2026)
TARGET_TIME = "08:30:00"
TIMEFRAMES = ["1m", "5m", "15m"]
RR_RATIOS = [1.0, 1.5, 2.0, 2.5]
LOOKBACK_PERIODS = [5, 6, 7, 8, 9, 10, 15]


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


def get_previous_candles(df: pd.DataFrame, current_idx: int, count: int) -> pd.DataFrame:
    start_idx = max(0, current_idx - count)
    return df.iloc[start_idx:current_idx]


def check_breakout(candle_830: pd.Series, prev_candles: pd.DataFrame, lookback: int) -> str | None:
    if len(prev_candles) < lookback:
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


def analyze_breakout_strategy(df: pd.DataFrame, lookback: int, rr_ratio: float) -> dict:
    results = {
        'qualified': 0,
        'wins': 0,
        'losses': 0,
        'pending': 0,
        'total_830_candles': 0
    }
    
    df_830_indices = df[df['TimeOnly'] == TARGET_TIME].index.tolist()
    
    for idx in df_830_indices:
        results['total_830_candles'] += 1
        candle_830 = df.loc[idx]
        pos = df.index.get_loc(idx)
        prev_candles = get_previous_candles(df, pos, lookback)
        direction = check_breakout(candle_830, prev_candles, lookback)
        
        if direction is None:
            continue
        
        results['qualified'] += 1
        
        open_price = candle_830['Open']
        close_price = candle_830['Close']
        body_size = abs(close_price - open_price)
        sl_distance = body_size / 2
        
        if sl_distance == 0:
            continue
        
        trade_result = simulate_trade(df, pos, direction, close_price, sl_distance, rr_ratio)
        
        if trade_result['outcome'] == 'win':
            results['wins'] += 1
        elif trade_result['outcome'] == 'loss':
            results['losses'] += 1
        else:
            results['pending'] += 1
    
    return results


def aggregate_results(all_results: list[dict]) -> dict:
    aggregated = {
        'qualified': 0,
        'wins': 0,
        'losses': 0,
        'pending': 0,
        'total_830_candles': 0
    }
    
    for result in all_results:
        for key in aggregated:
            aggregated[key] += result[key]
    
    return aggregated


def main():
    repo_root = get_repo_root()
    
    print("=" * 120)
    print("ANALYSE DE LA STRATÉGIE BREAKOUT 8H30 - COMPARAISON LOOKBACK PERIODS")
    print("=" * 120)
    print("\nConditions:")
    print("  - Entrée: Si la bougie 8h30 clôture AU-DESSUS ou EN-DESSOUS des N bougies précédentes")
    print("  - Lookback testés: 5, 6, 7, 8, 9, 10, 15 bougies")
    print("  - Stop Loss: Au milieu du corps de la bougie 8h30")
    print("  - RR testés: 1.0, 1.5, 2.0, 2.5")
    print("=" * 120)
    
    # Store all results for final comparison
    all_global_results = {}
    
    for timeframe in TIMEFRAMES:
        all_global_results[timeframe] = {}
        
        print(f"\n{'#' * 120}")
        print(f"# TIMEFRAME: {timeframe.upper()}")
        print('#' * 120)
        
        # Load all data for this timeframe
        all_dfs = []
        for year in YEARS:
            file_path = find_data_file(repo_root, year, timeframe)
            if file_path:
                try:
                    df = load_data(file_path)
                    all_dfs.append(df)
                except Exception as e:
                    print(f"  Erreur année {year}: {e}")
        
        if not all_dfs:
            print("  Aucune donnée disponible")
            continue
        
        combined_df = pd.concat(all_dfs, ignore_index=True)
        
        # Test each lookback period and RR
        for lookback in LOOKBACK_PERIODS:
            all_global_results[timeframe][lookback] = {}
            
            for rr in RR_RATIOS:
                results = analyze_breakout_strategy(combined_df, lookback, rr)
                all_global_results[timeframe][lookback][rr] = results
        
        # Print results for this timeframe
        print(f"\n{'=' * 100}")
        print(f"RÉSULTATS {timeframe.upper()}")
        print('=' * 100)
        
        # Table header
        header = f"{'Lookback':<10} | {'Qualif.':<10}"
        for rr in RR_RATIOS:
            header += f" | RR {rr} Win%"
        print(header)
        print("-" * 100)
        
        for lookback in LOOKBACK_PERIODS:
            row = f"{lookback} bougies | "
            
            # Get qualified count (same for all RR)
            qualified = all_global_results[timeframe][lookback][1.0]['qualified']
            total = all_global_results[timeframe][lookback][1.0]['total_830_candles']
            qual_rate = (qualified / total * 100) if total > 0 else 0
            row += f"{qualified:>4} ({qual_rate:>4.1f}%)"
            
            for rr in RR_RATIOS:
                data = all_global_results[timeframe][lookback][rr]
                wins = data['wins']
                losses = data['losses']
                total_trades = wins + losses
                if total_trades > 0:
                    win_rate = (wins / total_trades) * 100
                    row += f" | {win_rate:>10.1f}%"
                else:
                    row += f" | {'N/A':>10}"
            
            print(row)
    
    # Final summary comparison
    print("\n" + "=" * 120)
    print("TABLEAU COMPARATIF FINAL - WIN RATE PAR LOOKBACK ET RR")
    print("=" * 120)
    
    for timeframe in TIMEFRAMES:
        print(f"\n### {timeframe.upper()} ###")
        
        # Header
        header = f"{'Lookback':<12}"
        for rr in RR_RATIOS:
            header += f" | {'RR '+str(rr):^12}"
        print(header)
        print("-" * 80)
        
        for lookback in LOOKBACK_PERIODS:
            row = f"{lookback} bougies  "
            for rr in RR_RATIOS:
                if lookback in all_global_results[timeframe] and rr in all_global_results[timeframe][lookback]:
                    data = all_global_results[timeframe][lookback][rr]
                    wins = data['wins']
                    losses = data['losses']
                    total = wins + losses
                    if total > 0:
                        win_rate = (wins / total) * 100
                        row += f" | {win_rate:>10.1f}%"
                    else:
                        row += f" | {'N/A':>10}"
                else:
                    row += f" | {'N/A':>10}"
            print(row)
        
        # Find best lookback for each RR
        print(f"\n  🏆 Meilleur Lookback par RR :")
        for rr in RR_RATIOS:
            best_lookback = None
            best_win_rate = 0
            for lookback in LOOKBACK_PERIODS:
                if lookback in all_global_results[timeframe] and rr in all_global_results[timeframe][lookback]:
                    data = all_global_results[timeframe][lookback][rr]
                    wins = data['wins']
                    losses = data['losses']
                    total = wins + losses
                    if total > 0:
                        win_rate = (wins / total) * 100
                        if win_rate > best_win_rate:
                            best_win_rate = win_rate
                            best_lookback = lookback
            if best_lookback:
                print(f"     RR {rr}: {best_lookback} bougies ({best_win_rate:.1f}%)")
    
    # Qualification rate comparison
    print("\n" + "=" * 120)
    print("TAUX DE QUALIFICATION PAR LOOKBACK (% de journées avec signal)")
    print("=" * 120)
    
    header = f"{'Lookback':<12}"
    for tf in TIMEFRAMES:
        header += f" | {tf.upper():^15}"
    print(header)
    print("-" * 80)
    
    for lookback in LOOKBACK_PERIODS:
        row = f"{lookback} bougies  "
        for tf in TIMEFRAMES:
            if lookback in all_global_results[tf] and 1.0 in all_global_results[tf][lookback]:
                data = all_global_results[tf][lookback][1.0]
                qualified = data['qualified']
                total = data['total_830_candles']
                if total > 0:
                    qual_rate = (qualified / total) * 100
                    row += f" | {qualified:>4} ({qual_rate:>5.1f}%)"
                else:
                    row += f" | {'N/A':^15}"
            else:
                row += f" | {'N/A':^15}"
        print(row)
    
    print("\n" + "=" * 120)
    print("ANALYSE TERMINÉE")
    print("=" * 120)


if __name__ == "__main__":
    main()

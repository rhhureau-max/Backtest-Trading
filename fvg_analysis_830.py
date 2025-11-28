#!/usr/bin/env python3
"""
Script d'analyse des FVG (Fair Value Gaps / Imbalances) sur les bougies de 8h30 (15:30 UTC)

Ce script analyse les données 5 minutes de 2018 à 2025 pour trouver et compter 
les FVG (Fair Value Gaps) qui se produisent sur les bougies d'ouverture de New York (8h30 EST = 15:30 UTC).

Un FVG haussier se produit quand: Low de bougie n-1 > High de bougie n+1
Un FVG baissier se produit quand: High de bougie n-1 < Low de bougie n+1

Bougies utilisées pour la détection des FVG:
- Bougie n-1: 15:25:00 (8:25 NY)
- Bougie n: 15:30:00 (8:30 NY)
- Bougie n+1: 15:35:00 (8:35 NY)

Backtesting des trades FVG:
- Entrée à 15:40:00 (bougie n+2)
- FVG haussier → SHORT, FVG baissier → LONG
- Stop Loss basé sur le corps de la bougie n (50%, 75%, 100%)
- Take Profit selon ratios Risk/Reward (1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5)
"""

import os
import csv
from collections import defaultdict

# Constants
EXPECTED_CSV_COLUMNS = 7
ENTRY_TIME = '15:40:00'
END_OF_DAY_TIME = '21:55:00'
SL_PERCENTAGES = [0.5, 0.75, 1.0]
RR_RATIOS = [1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]
FLOAT_COMPARISON_EPSILON = 1e-6  # Tolérance pour les comparaisons de nombres flottants
MAX_PROFIT_FACTOR = 999.99  # Valeur finie maximale pour le profit factor (remplace l'infini)


def parse_csv_file(filepath):
    """Parse un fichier CSV et retourne les données organisées par date."""
    data_by_date = defaultdict(dict)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=';')
        header = next(reader)  # Skip header
        
        for row in reader:
            if len(row) < EXPECTED_CSV_COLUMNS:
                continue
            
            date_str = row[0]  # DD/MM/YYYY
            time_str = row[1]  # HH:MM:SS
            open_price = float(row[2])
            high_price = float(row[3])
            low_price = float(row[4])
            close_price = float(row[5])
            volume = int(row[6])
            
            data_by_date[date_str][time_str] = {
                'open': open_price,
                'high': high_price,
                'low': low_price,
                'close': close_price,
                'volume': volume
            }
    
    return data_by_date


def check_fvg(candle_n_minus_1, candle_n_plus_1):
    """
    Check if there is an FVG between candles n-1 and n+1.
    
    Bullish FVG: Low of n-1 > High of n+1 (gap upward)
    Bearish FVG: High of n-1 < Low of n+1 (gap downward)
    
    Returns:
        tuple: ('bullish', gap_size), ('bearish', gap_size), or (None, 0)
    """
    if candle_n_minus_1 is None or candle_n_plus_1 is None:
        return None, 0
    
    low_n_minus_1 = candle_n_minus_1['low']
    high_n_minus_1 = candle_n_minus_1['high']
    low_n_plus_1 = candle_n_plus_1['low']
    high_n_plus_1 = candle_n_plus_1['high']
    
    # FVG haussier: gap vers le haut (le low de la bougie précédente est au-dessus du high de la bougie suivante)
    if low_n_minus_1 > high_n_plus_1:
        gap_size = low_n_minus_1 - high_n_plus_1
        return 'bullish', gap_size
    
    # FVG baissier: gap vers le bas (le high de la bougie précédente est en-dessous du low de la bougie suivante)
    if high_n_minus_1 < low_n_plus_1:
        gap_size = low_n_plus_1 - high_n_minus_1
        return 'bearish', gap_size
    
    return None, 0


def time_to_minutes(time_str):
    """Convertit un temps HH:MM:SS en minutes depuis minuit."""
    parts = time_str.split(':')
    return int(parts[0]) * 60 + int(parts[1])


def get_sorted_candle_times_after(candles, start_time, end_time):
    """Retourne les temps de bougies triés entre start_time et end_time (inclus)."""
    start_minutes = time_to_minutes(start_time)
    end_minutes = time_to_minutes(end_time)
    
    valid_times = []
    for time_str in candles.keys():
        time_minutes = time_to_minutes(time_str)
        if start_minutes <= time_minutes <= end_minutes:
            valid_times.append(time_str)
    
    return sorted(valid_times, key=time_to_minutes)


def backtest_trade(candles, fvg_type, candle_n, sl_pct, rr_ratio):
    """
    Backteste un trade FVG avec les paramètres donnés.
    
    Args:
        candles: dict des bougies pour la journée
        fvg_type: 'bullish' ou 'bearish'
        candle_n: bougie centrale (15:30:00)
        sl_pct: pourcentage du corps pour le SL (0.5, 0.75, 1.0)
        rr_ratio: ratio Risk/Reward pour le TP
    
    Returns:
        'win', 'loss', ou 'unresolved'
    """
    # Vérifier que la bougie d'entrée existe (15:40:00)
    if ENTRY_TIME not in candles:
        return 'unresolved'
    
    entry_candle = candles[ENTRY_TIME]
    entry_price = entry_candle['open']
    
    # Calculer le corps de la bougie n
    body = abs(candle_n['close'] - candle_n['open'])
    if body < FLOAT_COMPARISON_EPSILON:
        return 'unresolved'
    
    # Calculer la distance SL
    distance_sl = body * sl_pct
    
    # Calculer la distance TP
    distance_tp = distance_sl * rr_ratio
    
    # Définir SL et TP selon la direction du trade
    if fvg_type == 'bullish':
        # FVG haussier → SHORT
        sl_price = entry_price + distance_sl
        tp_price = entry_price - distance_tp
    else:
        # FVG baissier → LONG
        sl_price = entry_price - distance_sl
        tp_price = entry_price + distance_tp
    
    # Parcourir les bougies après l'entrée jusqu'à la fin de la journée
    sorted_times = get_sorted_candle_times_after(candles, ENTRY_TIME, END_OF_DAY_TIME)
    
    for time_str in sorted_times:
        candle = candles[time_str]
        high = candle['high']
        low = candle['low']
        
        if fvg_type == 'bullish':
            # SHORT: on gagne si le low atteint TP, on perd si le high atteint SL
            tp_hit = low <= tp_price
            sl_hit = high >= sl_price
        else:
            # LONG: on gagne si le high atteint TP, on perd si le low atteint SL
            tp_hit = high >= tp_price
            sl_hit = low <= sl_price
        
        # Vérifier lequel est atteint en premier
        if tp_hit and sl_hit:
            # Les deux sont touchés dans la même bougie
            # On utilise la distance depuis l'open pour déterminer la priorité
            candle_open = candle['open']
            
            if fvg_type == 'bullish':
                # SHORT: TP vers le bas, SL vers le haut
                # Si l'open est déjà au-delà d'un niveau, c'est atteint immédiatement
                if candle_open <= tp_price:
                    return 'win'
                elif candle_open >= sl_price:
                    return 'loss'
                else:
                    # Les deux niveaux sont à l'extérieur de l'open
                    # Utiliser la distance pour estimer lequel est atteint en premier
                    dist_to_tp = candle_open - tp_price
                    dist_to_sl = sl_price - candle_open
                    if dist_to_tp <= dist_to_sl:
                        return 'win'
                    else:
                        return 'loss'
            else:
                # LONG: TP vers le haut, SL vers le bas
                if candle_open >= tp_price:
                    return 'win'
                elif candle_open <= sl_price:
                    return 'loss'
                else:
                    # Les deux niveaux sont à l'extérieur de l'open
                    dist_to_tp = tp_price - candle_open
                    dist_to_sl = candle_open - sl_price
                    if dist_to_tp <= dist_to_sl:
                        return 'win'
                    else:
                        return 'loss'
        elif tp_hit:
            return 'win'
        elif sl_hit:
            return 'loss'
    
    return 'unresolved'


def analyze_year(filepath, year):
    """Analyse les données d'une année et retourne les statistiques FVG."""
    if not os.path.exists(filepath):
        print(f"Fichier non trouvé: {filepath}")
        return None
    
    data_by_date = parse_csv_file(filepath)
    
    bullish_fvg_count = 0
    bearish_fvg_count = 0
    total_trading_days = 0
    fvg_details = []
    backtest_data = []  # Pour stocker les données nécessaires au backtesting
    
    # Pour chaque date avec des données à 15:30
    for date_str, candles in sorted(data_by_date.items()):
        # Vérifier si on a la bougie de 15:30:00
        if '15:30:00' not in candles:
            continue
        
        total_trading_days += 1
        
        # Bougie centrale (n) à 15:30:00
        candle_n = candles.get('15:30:00')
        
        # Bougie précédente (n-1) à 15:25:00 (8:25 NY)
        candle_n_minus_1 = candles.get('15:25:00')
        
        # Bougie suivante (n+1) à 15:35:00
        candle_n_plus_1 = candles.get('15:35:00')
        
        # Vérifier le FVG
        fvg_type, gap_size = check_fvg(candle_n_minus_1, candle_n_plus_1)
        
        if fvg_type == 'bullish':
            bullish_fvg_count += 1
            fvg_details.append({
                'date': date_str,
                'type': 'bullish',
                'gap_size': gap_size,
                'n_minus_1_low': candle_n_minus_1['low'],
                'n_plus_1_high': candle_n_plus_1['high']
            })
            backtest_data.append({
                'date': date_str,
                'type': 'bullish',
                'candle_n': candle_n,
                'candles': candles
            })
        elif fvg_type == 'bearish':
            bearish_fvg_count += 1
            fvg_details.append({
                'date': date_str,
                'type': 'bearish',
                'gap_size': gap_size,
                'n_minus_1_high': candle_n_minus_1['high'],
                'n_plus_1_low': candle_n_plus_1['low']
            })
            backtest_data.append({
                'date': date_str,
                'type': 'bearish',
                'candle_n': candle_n,
                'candles': candles
            })
    
    return {
        'year': year,
        'total_trading_days': total_trading_days,
        'bullish_fvg_count': bullish_fvg_count,
        'bearish_fvg_count': bearish_fvg_count,
        'total_fvg_count': bullish_fvg_count + bearish_fvg_count,
        'fvg_details': fvg_details,
        'backtest_data': backtest_data
    }


def run_backtesting(all_backtest_data):
    """
    Exécute le backtesting sur toutes les données FVG.
    
    Returns:
        dict: Résultats du backtesting pour chaque combinaison SL%/RR
    """
    # Initialiser les résultats
    results = {}
    for sl_pct in SL_PERCENTAGES:
        for rr in RR_RATIOS:
            key = (sl_pct, rr)
            results[key] = {'wins': 0, 'losses': 0, 'unresolved': 0}
    
    # Exécuter le backtesting pour chaque FVG
    for data in all_backtest_data:
        fvg_type = data['type']
        candle_n = data['candle_n']
        candles = data['candles']
        
        for sl_pct in SL_PERCENTAGES:
            for rr in RR_RATIOS:
                key = (sl_pct, rr)
                outcome = backtest_trade(candles, fvg_type, candle_n, sl_pct, rr)
                
                if outcome == 'win':
                    results[key]['wins'] += 1
                elif outcome == 'loss':
                    results[key]['losses'] += 1
                else:
                    results[key]['unresolved'] += 1
    
    return results


def calculate_metrics(results):
    """
    Calcule les métriques de performance pour chaque combinaison.
    
    Returns:
        list: Liste de dictionnaires avec les métriques
    """
    metrics = []
    
    for (sl_pct, rr), counts in sorted(results.items()):
        wins = counts['wins']
        losses = counts['losses']
        total_resolved = wins + losses
        
        if total_resolved > 0:
            winrate = (wins / total_resolved) * 100
        else:
            winrate = 0
        
        # Profit Factor = (Gains totaux) / (Pertes totales)
        # Gains = wins * rr (chaque win rapporte RR fois le risque)
        # Pertes = losses * 1 (chaque loss coûte 1 fois le risque)
        total_gains = wins * rr
        total_losses = losses * 1.0
        
        if total_losses > 0:
            profit_factor = total_gains / total_losses
        else:
            profit_factor = MAX_PROFIT_FACTOR if total_gains > 0 else 0
        
        # Espérance mathématique (expectancy) par trade
        if total_resolved > 0:
            expectancy = ((wins * rr) - losses) / total_resolved
        else:
            expectancy = 0
        
        metrics.append({
            'sl_pct': sl_pct,
            'rr': rr,
            'wins': wins,
            'losses': losses,
            'unresolved': counts['unresolved'],
            'total_resolved': total_resolved,
            'winrate': winrate,
            'profit_factor': profit_factor,
            'expectancy': expectancy
        })
    
    return metrics


def print_backtest_results(metrics):
    """Affiche les résultats du backtesting sous forme de tableau."""
    print()
    print("=" * 100)
    print("RÉSULTATS DU BACKTESTING FVG")
    print("=" * 100)
    print()
    print("Règles de trading:")
    print("- Entrée à 15:40:00 (bougie n+2)")
    print("- FVG haussier → SHORT, FVG baissier → LONG")
    print("- Stop Loss basé sur le corps de la bougie n (15:30:00)")
    print("- Vérification jusqu'à 21:55:00")
    print()
    
    # Afficher le tableau
    header = f"{'SL%':>6} | {'R:R':>5} | {'Wins':>6} | {'Losses':>7} | {'Unres.':>7} | {'Total':>6} | {'Winrate':>8} | {'PF':>8} | {'Expect.':>8}"
    print("-" * len(header))
    print(header)
    print("-" * len(header))
    
    for m in metrics:
        sl_str = f"{int(m['sl_pct']*100)}%"
        pf_str = f"{m['profit_factor']:.2f}" if m['profit_factor'] < MAX_PROFIT_FACTOR else "∞"
        print(f"{sl_str:>6} | {m['rr']:>5.1f} | {m['wins']:>6} | {m['losses']:>7} | {m['unresolved']:>7} | {m['total_resolved']:>6} | {m['winrate']:>7.1f}% | {pf_str:>8} | {m['expectancy']:>+8.2f}")
    
    print("-" * len(header))
    print()
    
    # Afficher un tableau récapitulatif par SL%
    print("=" * 60)
    print("TABLEAU RÉCAPITULATIF PAR STOP LOSS %")
    print("=" * 60)
    
    for sl_pct in SL_PERCENTAGES:
        sl_metrics = [m for m in metrics if m['sl_pct'] == sl_pct]
        print(f"\n--- Stop Loss = {int(sl_pct*100)}% du corps ---")
        print(f"{'R:R':>5} | {'Winrate':>8} | {'Profit Factor':>13} | {'Expectancy':>10}")
        print("-" * 45)
        for m in sl_metrics:
            pf_str = f"{m['profit_factor']:.2f}" if m['profit_factor'] < MAX_PROFIT_FACTOR else "∞"
            print(f"{m['rr']:>5.1f} | {m['winrate']:>7.1f}% | {pf_str:>13} | {m['expectancy']:>+10.2f}")


def save_backtest_results(metrics, base_dir):
    """Sauvegarde les résultats du backtesting dans des fichiers."""
    
    # Fichier texte détaillé
    txt_file = os.path.join(base_dir, "fvg_backtest_results.txt")
    with open(txt_file, 'w', encoding='utf-8') as f:
        f.write("=" * 100 + "\n")
        f.write("RÉSULTATS DU BACKTESTING FVG - 2018 À 2025\n")
        f.write("=" * 100 + "\n\n")
        
        f.write("PARAMÈTRES:\n")
        f.write("- Bougies analysées: 5 minutes\n")
        f.write("- Bougie n-1: 15:25:00 (8:25 NY)\n")
        f.write("- Bougie n (centrale): 15:30:00 (8:30 NY)\n")
        f.write("- Bougie n+1: 15:35:00 (8:35 NY)\n")
        f.write("- Entrée: 15:40:00 (ouverture de bougie n+2)\n")
        f.write("- Fin de journée: 21:55:00\n\n")
        
        f.write("RÈGLES DE TRADING:\n")
        f.write("- FVG haussier (Low n-1 > High n+1) → Position SHORT\n")
        f.write("- FVG baissier (High n-1 < Low n+1) → Position LONG\n")
        f.write("- Stop Loss: basé sur le corps de la bougie n (|Close - Open|)\n")
        f.write("- Take Profit: SL * Ratio Risk/Reward\n\n")
        
        f.write("=" * 100 + "\n")
        f.write("RÉSULTATS DÉTAILLÉS\n")
        f.write("=" * 100 + "\n\n")
        
        header = f"{'SL%':>6} | {'R:R':>5} | {'Wins':>6} | {'Losses':>7} | {'Unres.':>7} | {'Total':>6} | {'Winrate':>8} | {'PF':>8} | {'Expect.':>8}\n"
        f.write("-" * 100 + "\n")
        f.write(header)
        f.write("-" * 100 + "\n")
        
        for m in metrics:
            sl_str = f"{int(m['sl_pct']*100)}%"
            pf_str = f"{m['profit_factor']:.2f}" if m['profit_factor'] < MAX_PROFIT_FACTOR else "INF"
            f.write(f"{sl_str:>6} | {m['rr']:>5.1f} | {m['wins']:>6} | {m['losses']:>7} | {m['unresolved']:>7} | {m['total_resolved']:>6} | {m['winrate']:>7.1f}% | {pf_str:>8} | {m['expectancy']:>+8.2f}\n")
        
        f.write("-" * 100 + "\n\n")
        
        # Tableaux récapitulatifs par SL%
        f.write("=" * 60 + "\n")
        f.write("TABLEAUX RÉCAPITULATIFS PAR STOP LOSS %\n")
        f.write("=" * 60 + "\n")
        
        for sl_pct in SL_PERCENTAGES:
            sl_metrics = [m for m in metrics if m['sl_pct'] == sl_pct]
            f.write(f"\n--- Stop Loss = {int(sl_pct*100)}% du corps ---\n")
            f.write(f"{'R:R':>5} | {'Winrate':>8} | {'Profit Factor':>13} | {'Expectancy':>10}\n")
            f.write("-" * 45 + "\n")
            for m in sl_metrics:
                pf_str = f"{m['profit_factor']:.2f}" if m['profit_factor'] < MAX_PROFIT_FACTOR else "INF"
                f.write(f"{m['rr']:>5.1f} | {m['winrate']:>7.1f}% | {pf_str:>13} | {m['expectancy']:>+10.2f}\n")
        
        # Meilleurs résultats
        f.write("\n" + "=" * 60 + "\n")
        f.write("MEILLEURES CONFIGURATIONS\n")
        f.write("=" * 60 + "\n\n")
        
        # Meilleur winrate
        best_winrate = max(metrics, key=lambda x: x['winrate'])
        f.write(f"Meilleur Winrate: {best_winrate['winrate']:.1f}%\n")
        f.write(f"  → SL = {int(best_winrate['sl_pct']*100)}%, R:R = {best_winrate['rr']}\n\n")
        
        # Meilleur profit factor (en excluant les valeurs spéciales)
        valid_pf = [m for m in metrics if m['profit_factor'] < MAX_PROFIT_FACTOR and m['profit_factor'] > 0]
        if valid_pf:
            best_pf = max(valid_pf, key=lambda x: x['profit_factor'])
            f.write(f"Meilleur Profit Factor: {best_pf['profit_factor']:.2f}\n")
            f.write(f"  → SL = {int(best_pf['sl_pct']*100)}%, R:R = {best_pf['rr']}\n\n")
        
        # Meilleure espérance
        best_expect = max(metrics, key=lambda x: x['expectancy'])
        f.write(f"Meilleure Espérance: {best_expect['expectancy']:+.2f}R\n")
        f.write(f"  → SL = {int(best_expect['sl_pct']*100)}%, R:R = {best_expect['rr']}\n")
    
    print(f"Résultats backtesting sauvegardés dans: {txt_file}")
    
    # Fichier CSV
    csv_file = os.path.join(base_dir, "fvg_backtest_results.csv")
    with open(csv_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(['SL_Pct', 'RR_Ratio', 'Wins', 'Losses', 'Unresolved', 'Total_Resolved', 'Winrate', 'Profit_Factor', 'Expectancy'])
        
        for m in metrics:
            pf_str = f"{m['profit_factor']:.4f}" if m['profit_factor'] < MAX_PROFIT_FACTOR else "INF"
            writer.writerow([
                m['sl_pct'],
                m['rr'],
                m['wins'],
                m['losses'],
                m['unresolved'],
                m['total_resolved'],
                f"{m['winrate']:.2f}",
                pf_str,
                f"{m['expectancy']:.4f}"
            ])
    
    print(f"Données CSV backtesting sauvegardées dans: {csv_file}")


def main():
    """Fonction principale pour analyser toutes les années."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    years = ['2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025']
    all_results = []
    
    print("=" * 80)
    print("ANALYSE DES FVG SUR LES BOUGIES DE 8H30 (15:30 UTC) - 2018 À 2025")
    print("=" * 80)
    print()
    
    total_bullish = 0
    total_bearish = 0
    total_trading_days = 0
    all_fvg_details = []
    all_backtest_data = []
    
    for year in years:
        filepath = os.path.join(base_dir, f"{year} 5m.csv")
        result = analyze_year(filepath, year)
        
        if result:
            all_results.append(result)
            total_bullish += result['bullish_fvg_count']
            total_bearish += result['bearish_fvg_count']
            total_trading_days += result['total_trading_days']
            all_fvg_details.extend(result['fvg_details'])
            all_backtest_data.extend(result['backtest_data'])
            
            print(f"Année {year}:")
            print(f"  - Jours de trading analysés: {result['total_trading_days']}")
            print(f"  - FVG haussiers: {result['bullish_fvg_count']}")
            print(f"  - FVG baissiers: {result['bearish_fvg_count']}")
            print(f"  - Total FVG: {result['total_fvg_count']}")
            if result['total_trading_days'] > 0:
                fvg_rate = (result['total_fvg_count'] / result['total_trading_days']) * 100
                print(f"  - Taux de FVG: {fvg_rate:.1f}%")
            print()
    
    # Résumé global
    print("=" * 80)
    print("RÉSUMÉ GLOBAL (2018-2025)")
    print("=" * 80)
    print(f"Total jours de trading analysés: {total_trading_days}")
    print(f"Total FVG haussiers: {total_bullish}")
    print(f"Total FVG baissiers: {total_bearish}")
    print(f"Total FVG (tous types): {total_bullish + total_bearish}")
    if total_trading_days > 0:
        global_fvg_rate = ((total_bullish + total_bearish) / total_trading_days) * 100
        print(f"Taux global de FVG: {global_fvg_rate:.1f}%")
    print()
    
    # Sauvegarder les résultats dans un fichier
    output_file = os.path.join(base_dir, "fvg_analysis_results.txt")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("ANALYSE DES FVG SUR LES BOUGIES DE 8H30 (15:30 UTC) - 2018 À 2025\n")
        f.write("=" * 80 + "\n\n")
        f.write("Définitions:\n")
        f.write("- FVG haussier: Low de bougie n-1 (15:25) > High de bougie n+1 (15:35)\n")
        f.write("- FVG baissier: High de bougie n-1 (15:25) < Low de bougie n+1 (15:35)\n")
        f.write("- Bougie centrale (n): 15:30:00 (8h30 EST = Ouverture de New York)\n\n")
        
        f.write("=" * 80 + "\n")
        f.write("STATISTIQUES PAR ANNÉE\n")
        f.write("=" * 80 + "\n\n")
        
        for result in all_results:
            f.write(f"Année {result['year']}:\n")
            f.write(f"  - Jours de trading analysés: {result['total_trading_days']}\n")
            f.write(f"  - FVG haussiers: {result['bullish_fvg_count']}\n")
            f.write(f"  - FVG baissiers: {result['bearish_fvg_count']}\n")
            f.write(f"  - Total FVG: {result['total_fvg_count']}\n")
            if result['total_trading_days'] > 0:
                fvg_rate = (result['total_fvg_count'] / result['total_trading_days']) * 100
                f.write(f"  - Taux de FVG: {fvg_rate:.1f}%\n")
            f.write("\n")
        
        f.write("=" * 80 + "\n")
        f.write("RÉSUMÉ GLOBAL (2018-2025)\n")
        f.write("=" * 80 + "\n")
        f.write(f"Total jours de trading analysés: {total_trading_days}\n")
        f.write(f"Total FVG haussiers: {total_bullish}\n")
        f.write(f"Total FVG baissiers: {total_bearish}\n")
        f.write(f"Total FVG (tous types): {total_bullish + total_bearish}\n")
        if total_trading_days > 0:
            global_fvg_rate = ((total_bullish + total_bearish) / total_trading_days) * 100
            f.write(f"Taux global de FVG: {global_fvg_rate:.1f}%\n")
        f.write("\n")
        
        # Détails des FVG
        f.write("=" * 80 + "\n")
        f.write("LISTE DÉTAILLÉE DES FVG\n")
        f.write("=" * 80 + "\n\n")
        
        for fvg in all_fvg_details:
            if fvg['type'] == 'bullish':
                f.write(f"{fvg['date']} - FVG HAUSSIER - Gap: {fvg['gap_size']:.2f} points\n")
                f.write(f"  Low n-1 (15:25): {fvg['n_minus_1_low']:.2f} > High n+1 (15:35): {fvg['n_plus_1_high']:.2f}\n")
            else:
                f.write(f"{fvg['date']} - FVG BAISSIER - Gap: {fvg['gap_size']:.2f} points\n")
                f.write(f"  High n-1 (15:25): {fvg['n_minus_1_high']:.2f} < Low n+1 (15:35): {fvg['n_plus_1_low']:.2f}\n")
    
    print(f"Résultats sauvegardés dans: {output_file}")
    
    # Créer aussi un fichier CSV avec les détails
    csv_output_file = os.path.join(base_dir, "fvg_analysis_results.csv")
    with open(csv_output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(['Date', 'Type', 'Gap_Size', 'N_minus_1_Value', 'N_plus_1_Value'])
        
        for fvg in all_fvg_details:
            if fvg['type'] == 'bullish':
                writer.writerow([
                    fvg['date'],
                    'Bullish',
                    f"{fvg['gap_size']:.2f}",
                    f"{fvg['n_minus_1_low']:.2f}",
                    f"{fvg['n_plus_1_high']:.2f}"
                ])
            else:
                writer.writerow([
                    fvg['date'],
                    'Bearish',
                    f"{fvg['gap_size']:.2f}",
                    f"{fvg['n_minus_1_high']:.2f}",
                    f"{fvg['n_plus_1_low']:.2f}"
                ])
    
    print(f"Données CSV sauvegardées dans: {csv_output_file}")
    
    # ========================================================================
    # BACKTESTING DES TRADES FVG
    # ========================================================================
    print()
    print("=" * 80)
    print("EXÉCUTION DU BACKTESTING...")
    print("=" * 80)
    print(f"Nombre de FVG à backtester: {len(all_backtest_data)}")
    
    if all_backtest_data:
        # Exécuter le backtesting
        backtest_results = run_backtesting(all_backtest_data)
        
        # Calculer les métriques
        metrics = calculate_metrics(backtest_results)
        
        # Afficher les résultats
        print_backtest_results(metrics)
        
        # Sauvegarder les résultats
        save_backtest_results(metrics, base_dir)
    else:
        print("Aucun FVG à backtester.")


if __name__ == "__main__":
    main()

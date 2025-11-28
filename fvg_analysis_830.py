#!/usr/bin/env python3
"""
Script d'analyse des FVG (Fair Value Gaps / Imbalances) sur les bougies de 8h30 (15:30 UTC)

Ce script analyse les données 5 minutes de 2018 à 2025 pour trouver et compter 
les FVG (Fair Value Gaps) qui se produisent sur les bougies d'ouverture de New York (8h30 EST = 15:30 UTC).

Un FVG haussier se produit quand: Low de bougie n-1 > High de bougie n+1
Un FVG baissier se produit quand: High de bougie n-1 < Low de bougie n+1

Les données ont un gap entre 15:10 et 15:30 (pause CME), donc:
- Bougie n-1: 15:10:00
- Bougie n: 15:30:00  
- Bougie n+1: 15:35:00
"""

import os
import csv
from datetime import datetime
from collections import defaultdict


def parse_csv_file(filepath):
    """Parse un fichier CSV et retourne les données organisées par date."""
    data_by_date = defaultdict(dict)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=';')
        header = next(reader)  # Skip header
        
        for row in reader:
            if len(row) < 7:
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
    Vérifie s'il y a un FVG entre les bougies n-1 et n+1.
    
    FVG haussier: Low de n-1 > High de n+1 (gap vers le haut)
    FVG baissier: High de n-1 < Low de n+1 (gap vers le bas)
    
    Returns:
        'bullish', 'bearish', ou None
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
    
    # Pour chaque date avec des données à 15:30
    for date_str, candles in sorted(data_by_date.items()):
        # Vérifier si on a la bougie de 15:30:00
        if '15:30:00' not in candles:
            continue
        
        total_trading_days += 1
        
        # Bougie centrale (n) à 15:30:00
        candle_n = candles.get('15:30:00')
        
        # Bougie précédente (n-1) à 15:10:00 (car gap de 15:10 à 15:30)
        candle_n_minus_1 = candles.get('15:10:00')
        
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
        elif fvg_type == 'bearish':
            bearish_fvg_count += 1
            fvg_details.append({
                'date': date_str,
                'type': 'bearish',
                'gap_size': gap_size,
                'n_minus_1_high': candle_n_minus_1['high'],
                'n_plus_1_low': candle_n_plus_1['low']
            })
    
    return {
        'year': year,
        'total_trading_days': total_trading_days,
        'bullish_fvg_count': bullish_fvg_count,
        'bearish_fvg_count': bearish_fvg_count,
        'total_fvg_count': bullish_fvg_count + bearish_fvg_count,
        'fvg_details': fvg_details
    }


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
    
    for year in years:
        filepath = os.path.join(base_dir, f"{year} 5m.csv")
        result = analyze_year(filepath, year)
        
        if result:
            all_results.append(result)
            total_bullish += result['bullish_fvg_count']
            total_bearish += result['bearish_fvg_count']
            total_trading_days += result['total_trading_days']
            all_fvg_details.extend(result['fvg_details'])
            
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
        f.write("- FVG haussier: Low de bougie n-1 (15:10) > High de bougie n+1 (15:35)\n")
        f.write("- FVG baissier: High de bougie n-1 (15:10) < Low de bougie n+1 (15:35)\n")
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
                f.write(f"  Low n-1 (15:10): {fvg['n_minus_1_low']:.2f} > High n+1 (15:35): {fvg['n_plus_1_high']:.2f}\n")
            else:
                f.write(f"{fvg['date']} - FVG BAISSIER - Gap: {fvg['gap_size']:.2f} points\n")
                f.write(f"  High n-1 (15:10): {fvg['n_minus_1_high']:.2f} < Low n+1 (15:35): {fvg['n_plus_1_low']:.2f}\n")
    
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


if __name__ == "__main__":
    main()

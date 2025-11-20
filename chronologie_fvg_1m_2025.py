#!/usr/bin/env python3
"""
Chronologie des FVG à 8:30:00 sur 1 minute - Année 2025

Ce script affiche une chronologie des Fair Value Gaps détectés dans les données
1 minute pour l'année 2025, à 8:30:00 exactement.
"""

import csv

def detect_fvg(data):
    """Détecte les Fair Value Gaps dans les données."""
    fvgs = []
    
    for i in range(2, len(data)):
        current = data[i]
        previous = data[i-2]
        middle = data[i-1]
        
        # FVG Bullish
        if float(current['low']) > float(previous['high']):
            fvgs.append({
                'date': current['date'],
                'time': current['time'],
                'type': 'Bullish',
                'gap_size': float(current['low']) - float(previous['high']),
                'gap_start': previous['high'],
                'gap_end': current['low'],
                'prev_candle': previous,
                'middle_candle': middle,
                'curr_candle': current
            })
        
        # FVG Bearish
        elif float(current['high']) < float(previous['low']):
            fvgs.append({
                'date': current['date'],
                'time': current['time'],
                'type': 'Bearish',
                'gap_size': float(previous['low']) - float(current['high']),
                'gap_start': current['high'],
                'gap_end': previous['low'],
                'prev_candle': previous,
                'middle_candle': middle,
                'curr_candle': current
            })
    
    return fvgs

def load_csv_data(filename):
    """Charge les données OHLC depuis un fichier CSV."""
    data = []
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=';')
        next(reader)  # Ignorer l'en-tête
        
        for row in reader:
            if len(row) >= 7:
                data.append({
                    'date': row[0],
                    'time': row[1],
                    'open': row[2],
                    'high': row[3],
                    'low': row[4],
                    'close': row[5],
                    'volume': row[6]
                })
    
    return data

def main():
    """Fonction principale pour afficher la chronologie des FVGs 1m en 2025."""
    print("=" * 100)
    print("Chronologie des FVG à 8:30:00 - 1 minute - Année 2025")
    print("=" * 100)
    
    # Charger les données 1 minute de 2025
    data = load_csv_data('2025 1m.csv')
    fvgs = detect_fvg(data)
    
    # Filtrer pour 8:30:00 uniquement
    fvgs_at_830 = [fvg for fvg in fvgs if fvg['time'] == '08:30:00']
    
    print(f"\nTotal: {len(fvgs_at_830)} FVGs détectés à 8:30:00\n")
    
    # Afficher la chronologie
    print("Chronologie (ordre chronologique):")
    print("-" * 100)
    print(f"{'#':<4} {'Date':<12} {'Type':<10} {'Taille Gap':<15} {'De':<15} {'À':<15}")
    print("-" * 100)
    
    for i, fvg in enumerate(fvgs_at_830, 1):
        print(f"{i:<4} {fvg['date']:<12} {fvg['type']:<10} {fvg['gap_size']:<15.6f} {fvg['gap_start']:<15} {fvg['gap_end']:<15}")
    
    print("=" * 100)
    
    # Afficher les détails OHLC
    print("\nDétails complets avec données OHLC:")
    print("=" * 100)
    
    for i, fvg in enumerate(fvgs_at_830, 1):
        print(f"\n{i}. {fvg['date']} à {fvg['time']} - FVG {fvg['type']}")
        print(f"   Taille du gap: {fvg['gap_size']:.6f}")
        print(f"   Plage du gap: {fvg['gap_start']} à {fvg['gap_end']}")
        print(f"   ")
        print(f"   Bougie précédente (i-2): O={fvg['prev_candle']['open']} H={fvg['prev_candle']['high']} L={fvg['prev_candle']['low']} C={fvg['prev_candle']['close']}")
        print(f"   Bougie milieu    (i-1): O={fvg['middle_candle']['open']} H={fvg['middle_candle']['high']} L={fvg['middle_candle']['low']} C={fvg['middle_candle']['close']}")
        print(f"   Bougie actuelle  (i)  : O={fvg['curr_candle']['open']} H={fvg['curr_candle']['high']} L={fvg['curr_candle']['low']} C={fvg['curr_candle']['close']}")
        print("-" * 100)
    
    print(f"\nTotal: {len(fvgs_at_830)} FVGs en 2025 sur timeframe 1 minute")

if __name__ == "__main__":
    main()

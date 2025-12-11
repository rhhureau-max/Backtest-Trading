#!/usr/bin/env python3
"""
Chronologie des FVG à 8:30:00 sur 1 minute - Année 2025

Ce script affiche une chronologie des Fair Value Gaps détectés dans les données
1 minute pour l'année 2025, à 8:30:00 exactement.
"""

import csv

def detect_fvg(data):
    """Détecte les Fair Value Gaps où la bougie du milieu est à 8:30."""
    fvgs = []
    
    for i in range(1, len(data) - 1):
        previous = data[i-1]
        middle = data[i]
        next_candle = data[i+1]
        
        # Seulement si la bougie du milieu est à 8:30:00
        if middle['time'] != '08:30:00':
            continue
        
        # FVG Bullish
        if float(next_candle['low']) > float(previous['high']):
            fvgs.append({
                'date': middle['date'],
                'time': middle['time'],
                'type': 'Bullish',
                'gap_size': float(next_candle['low']) - float(previous['high']),
                'gap_start': previous['high'],
                'gap_end': next_candle['low'],
                'prev_candle': previous,
                'middle_candle': middle,
                'next_candle': next_candle
            })
        
        # FVG Bearish
        elif float(next_candle['high']) < float(previous['low']):
            fvgs.append({
                'date': middle['date'],
                'time': middle['time'],
                'type': 'Bearish',
                'gap_size': float(previous['low']) - float(next_candle['high']),
                'gap_start': next_candle['high'],
                'gap_end': previous['low'],
                'prev_candle': previous,
                'middle_candle': middle,
                'next_candle': next_candle
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
    """Fonction principale pour afficher la chronologie des FVGs 1m en 2025 (8:30 = bougie du milieu)."""
    print("=" * 100)
    print("Chronologie des FVG à 8:30:00 (Bougie du Milieu) - 1 minute - Année 2025")
    print("=" * 100)
    
    # Charger les données 1 minute de 2025
    data = load_csv_data('2025 1m.csv')
    # detect_fvg filtre déjà pour 8:30:00 comme bougie du milieu
    fvgs_at_830 = detect_fvg(data)
    
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
        print(f"   Bougie précédente (8:29): O={fvg['prev_candle']['open']} H={fvg['prev_candle']['high']} L={fvg['prev_candle']['low']} C={fvg['prev_candle']['close']}")
        print(f"   Bougie milieu     (8:30): O={fvg['middle_candle']['open']} H={fvg['middle_candle']['high']} L={fvg['middle_candle']['low']} C={fvg['middle_candle']['close']}")
        print(f"   Bougie suivante   (8:31): O={fvg['next_candle']['open']} H={fvg['next_candle']['high']} L={fvg['next_candle']['low']} C={fvg['next_candle']['close']}")
        print("-" * 100)
    
    print(f"\nTotal: {len(fvgs_at_830)} FVGs en 2025 sur timeframe 1 minute")

if __name__ == "__main__":
    main()

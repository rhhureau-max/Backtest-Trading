#!/usr/bin/env python3
"""
Liste complète de tous les FVG en 15 minutes pour 2025

Ce script détecte tous les Fair Value Gaps dans les données 15 minutes de 2025.
"""

import csv

def detect_all_fvg(data):
    """Détecte tous les Fair Value Gaps dans les données."""
    fvgs = []
    
    for i in range(1, len(data) - 1):
        previous = data[i-1]
        middle = data[i]
        next_candle = data[i+1]
        
        # FVG Bullish
        if float(next_candle['low']) > float(previous['high']):
            fvgs.append({
                'date': middle['date'],
                'time': middle['time'],
                'type': 'Bullish',
                'gap_size': float(next_candle['low']) - float(previous['high']),
                'gap_start': previous['high'],
                'gap_end': next_candle['low']
            })
        
        # FVG Bearish
        elif float(next_candle['high']) < float(previous['low']):
            fvgs.append({
                'date': middle['date'],
                'time': middle['time'],
                'type': 'Bearish',
                'gap_size': float(previous['low']) - float(next_candle['high']),
                'gap_start': next_candle['high'],
                'gap_end': previous['low']
            })
    
    return fvgs

def load_csv_data(filename):
    """Charge les données OHLC depuis un fichier CSV."""
    data = []
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=';')
        next(reader)
        
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
    """Fonction principale pour lister tous les FVGs 15m en 2025."""
    print("=" * 100)
    print("Liste complète des FVG - 15 minutes - Année 2025")
    print("=" * 100)
    
    # Charger les données 15 minutes de 2025
    data = load_csv_data('2025 15m.csv')
    fvgs = detect_all_fvg(data)
    
    print(f"\nTotal: {len(fvgs)} FVGs détectés\n")
    
    # Statistiques
    bullish = [f for f in fvgs if f['type'] == 'Bullish']
    bearish = [f for f in fvgs if f['type'] == 'Bearish']
    
    print(f"Statistiques:")
    print(f"  - Bullish: {len(bullish)} ({len(bullish)/len(fvgs)*100:.1f}%)")
    print(f"  - Bearish: {len(bearish)} ({len(bearish)/len(fvgs)*100:.1f}%)")
    print(f"  - Gap moyen: {sum(f['gap_size'] for f in fvgs) / len(fvgs):.2f}")
    print(f"  - Gap max: {max(f['gap_size'] for f in fvgs):.2f}")
    print(f"  - Gap min: {min(f['gap_size'] for f in fvgs):.6f}")
    print()
    
    # Afficher les premiers et derniers FVGs
    print("Premiers 20 FVGs:")
    print("-" * 100)
    print(f"{'#':<6} {'Date':<12} {'Heure':<10} {'Type':<10} {'Taille Gap':<15}")
    print("-" * 100)
    
    for i, fvg in enumerate(fvgs[:20], 1):
        print(f"{i:<6} {fvg['date']:<12} {fvg['time']:<10} {fvg['type']:<10} {fvg['gap_size']:<15.6f}")
    
    print("\n...")
    print(f"\nDerniers 20 FVGs:")
    print("-" * 100)
    
    for i, fvg in enumerate(fvgs[-20:], len(fvgs)-19):
        print(f"{i:<6} {fvg['date']:<12} {fvg['time']:<10} {fvg['type']:<10} {fvg['gap_size']:<15.6f}")
    
    print("=" * 100)
    print(f"\nPour sauvegarder dans un fichier: python3 {__file__} > fvg_15m_2025_complet.txt")

if __name__ == "__main__":
    main()

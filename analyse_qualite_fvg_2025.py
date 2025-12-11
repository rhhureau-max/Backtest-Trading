#!/usr/bin/env python3
"""
Analyse de la qualité des FVG à 8:30:00 pour 2025

Ce script analyse si les FVGs sont "bons" ou "mauvais" selon le critère:
- Bon FVG: Le prix ne revient PAS dans la zone FVG après 5 bougies
- Mauvais FVG: Le prix revient dans la zone FVG après 5 bougies

Pour 1 minute: vérifie jusqu'à 8:35 (5 bougies après 8:30)
Pour 15 minutes: vérifie jusqu'à 9:45 (5 bougies après 8:30)
"""

import csv

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

def detect_fvg_with_quality(data):
    """Détecte les FVGs à 8:30 et évalue leur qualité."""
    fvgs = []
    
    for i in range(1, len(data) - 6):  # Besoin d'au moins 5 bougies après
        previous = data[i-1]
        middle = data[i]
        next_candle = data[i+1]
        
        # Filtrer pour 8:30:00 uniquement
        if middle['time'] != '08:30:00':
            continue
        
        fvg = None
        
        # FVG Bullish
        if float(next_candle['low']) > float(previous['high']):
            gap_low = float(previous['high'])
            gap_high = float(next_candle['low'])
            fvg = {
                'date': middle['date'],
                'time': middle['time'],
                'type': 'Bullish',
                'gap_low': gap_low,
                'gap_high': gap_high,
                'gap_size': gap_high - gap_low,
                'previous_candle': previous,
                'middle_candle': middle,
                'next_candle': next_candle
            }
        
        # FVG Bearish
        elif float(next_candle['high']) < float(previous['low']):
            gap_low = float(next_candle['high'])
            gap_high = float(previous['low'])
            fvg = {
                'date': middle['date'],
                'time': middle['time'],
                'type': 'Bearish',
                'gap_low': gap_low,
                'gap_high': gap_high,
                'gap_size': gap_high - gap_low,
                'previous_candle': previous,
                'middle_candle': middle,
                'next_candle': next_candle
            }
        
        if fvg:
            # Vérifier les 5 bougies suivantes
            revisited = False
            revisit_candle = None
            
            for j in range(i+2, min(i+7, len(data))):
                candle = data[j]
                candle_high = float(candle['high'])
                candle_low = float(candle['low'])
                
                # Le prix entre dans la zone FVG
                if candle_low <= fvg['gap_high'] and candle_high >= fvg['gap_low']:
                    revisited = True
                    revisit_candle = candle
                    break
            
            fvg['is_good'] = not revisited
            fvg['revisited'] = revisited
            if revisit_candle:
                fvg['revisit_date'] = revisit_candle['date']
                fvg['revisit_time'] = revisit_candle['time']
            
            fvgs.append(fvg)
    
    return fvgs

def main():
    """Fonction principale pour analyser la qualité des FVGs."""
    print("=" * 80)
    print("Analyse de la qualité des FVG à 8:30:00 - Année 2025")
    print("=" * 80)
    print()
    print("Critères:")
    print("  - BON FVG: Le prix ne revient PAS dans la zone FVG après 5 bougies")
    print("  - MAUVAIS FVG: Le prix revient dans la zone FVG après 5 bougies")
    print()
    
    # 1 minute
    print("Analyse 1 MINUTE (vérification jusqu'à 8:35)...")
    data_1m = load_csv_data('2025 1m.csv')
    fvgs_1m = detect_fvg_with_quality(data_1m)
    good_1m = [f for f in fvgs_1m if f['is_good']]
    bad_1m = [f for f in fvgs_1m if not f['is_good']]
    
    print("=" * 80)
    print(f"1 MINUTE - {len(fvgs_1m)} FVGs analysés:")
    print("-" * 80)
    print(f"  Bons FVGs (prix ne revient pas):  {len(good_1m):3d} ({len(good_1m)/len(fvgs_1m)*100:5.1f}%)")
    print(f"  Mauvais FVGs (prix revient):      {len(bad_1m):3d} ({len(bad_1m)/len(fvgs_1m)*100:5.1f}%)")
    print()
    
    # Statistiques détaillées 1m
    good_bullish_1m = [f for f in good_1m if f['type'] == 'Bullish']
    good_bearish_1m = [f for f in good_1m if f['type'] == 'Bearish']
    bad_bullish_1m = [f for f in bad_1m if f['type'] == 'Bullish']
    bad_bearish_1m = [f for f in bad_1m if f['type'] == 'Bearish']
    
    print("  Détail par type:")
    print(f"    Bons Bullish:    {len(good_bullish_1m):3d} ({len(good_bullish_1m)/len(fvgs_1m)*100:5.1f}%)")
    print(f"    Bons Bearish:    {len(good_bearish_1m):3d} ({len(good_bearish_1m)/len(fvgs_1m)*100:5.1f}%)")
    print(f"    Mauvais Bullish: {len(bad_bullish_1m):3d} ({len(bad_bullish_1m)/len(fvgs_1m)*100:5.1f}%)")
    print(f"    Mauvais Bearish: {len(bad_bearish_1m):3d} ({len(bad_bearish_1m)/len(fvgs_1m)*100:5.1f}%)")
    print()
    
    # 15 minutes
    print("Analyse 15 MINUTES (vérification jusqu'à 9:45)...")
    data_15m = load_csv_data('2025 15m.csv')
    fvgs_15m = detect_fvg_with_quality(data_15m)
    good_15m = [f for f in fvgs_15m if f['is_good']]
    bad_15m = [f for f in fvgs_15m if not f['is_good']]
    
    print("=" * 80)
    print(f"15 MINUTES - {len(fvgs_15m)} FVGs analysés:")
    print("-" * 80)
    print(f"  Bons FVGs (prix ne revient pas):  {len(good_15m):3d} ({len(good_15m)/len(fvgs_15m)*100:5.1f}%)")
    print(f"  Mauvais FVGs (prix revient):      {len(bad_15m):3d} ({len(bad_15m)/len(fvgs_15m)*100:5.1f}%)")
    print()
    
    # Statistiques détaillées 15m
    good_bullish_15m = [f for f in good_15m if f['type'] == 'Bullish']
    good_bearish_15m = [f for f in good_15m if f['type'] == 'Bearish']
    bad_bullish_15m = [f for f in bad_15m if f['type'] == 'Bullish']
    bad_bearish_15m = [f for f in bad_15m if f['type'] == 'Bearish']
    
    print("  Détail par type:")
    print(f"    Bons Bullish:    {len(good_bullish_15m):3d} ({len(good_bullish_15m)/len(fvgs_15m)*100:5.1f}%)")
    print(f"    Bons Bearish:    {len(good_bearish_15m):3d} ({len(good_bearish_15m)/len(fvgs_15m)*100:5.1f}%)")
    print(f"    Mauvais Bullish: {len(bad_bullish_15m):3d} ({len(bad_bullish_15m)/len(fvgs_15m)*100:5.1f}%)")
    print(f"    Mauvais Bearish: {len(bad_bearish_15m):3d} ({len(bad_bearish_15m)/len(fvgs_15m)*100:5.1f}%)")
    print()
    
    # Total
    total_fvgs = len(fvgs_1m) + len(fvgs_15m)
    total_good = len(good_1m) + len(good_15m)
    total_bad = len(bad_1m) + len(bad_15m)
    
    print("=" * 80)
    print(f"TOTAL - {total_fvgs} FVGs analysés:")
    print("-" * 80)
    print(f"  Bons FVGs:     {total_good:3d} ({total_good/total_fvgs*100:5.1f}%)")
    print(f"  Mauvais FVGs:  {total_bad:3d} ({total_bad/total_fvgs*100:5.1f}%)")
    print("=" * 80)
    
    # Afficher quelques exemples
    print()
    print("Exemples de BONS FVGs (1m):")
    print("-" * 80)
    for fvg in good_1m[:5]:
        print(f"  {fvg['date']} - {fvg['type']} - Gap: {fvg['gap_size']:.2f}")
    
    print()
    print("Exemples de MAUVAIS FVGs (1m):")
    print("-" * 80)
    for fvg in bad_1m[:5]:
        revisit_info = f" (revisité le {fvg.get('revisit_date', 'N/A')} à {fvg.get('revisit_time', 'N/A')})"
        print(f"  {fvg['date']} - {fvg['type']} - Gap: {fvg['gap_size']:.2f}{revisit_info}")

if __name__ == "__main__":
    main()

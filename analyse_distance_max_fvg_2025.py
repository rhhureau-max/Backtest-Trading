#!/usr/bin/env python3
"""
Analyse de la distance maximale (en ticks) depuis la clôture de la 3ème bougie
pour les FVG à 8:30:00 en 2025

Pour chaque période (5, 10, 15, 20, 25, 30 bougies), calcule la distance moyenne
maximale que le prix atteint par rapport à la clôture de la 3ème bougie (8:31 pour 1m).

Un tick Nasdaq = 0.25 points
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

def detect_fvg_with_max_distance(data, periods=[5, 10, 15, 20, 25, 30]):
    """Détecte les FVGs à 8:30 et calcule la distance max pour chaque période."""
    fvgs = []
    
    max_period = max(periods)
    
    for i in range(1, len(data) - max_period - 1):
        previous = data[i-1]
        middle = data[i]
        next_candle = data[i+1]  # 3ème bougie (8:31 pour 1m)
        
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
                'index': i,
                'third_candle_close': float(next_candle['close'])
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
                'index': i,
                'third_candle_close': float(next_candle['close'])
            }
        
        if fvg:
            # Analyser la distance max pour chaque période
            distance_by_period = {}
            
            for period in periods:
                max_distance = 0.0
                max_distance_candle = None
                revisited = False
                
                # La 3ème bougie est à i+1, on commence à i+2
                for j in range(i+2, min(i+2+period, len(data))):
                    candle = data[j]
                    candle_high = float(candle['high'])
                    candle_low = float(candle['low'])
                    
                    # Calculer la distance max depuis la clôture de la 3ème bougie
                    if fvg['type'] == 'Bullish':
                        # Pour Bullish, on regarde la distance vers le haut
                        distance = candle_high - fvg['third_candle_close']
                    else:  # Bearish
                        # Pour Bearish, on regarde la distance vers le bas (en valeur absolue)
                        distance = fvg['third_candle_close'] - candle_low
                    
                    if distance > max_distance:
                        max_distance = distance
                        max_distance_candle = {
                            'candle_number': j - i - 1,
                            'date': candle['date'],
                            'time': candle['time'],
                            'high': candle_high,
                            'low': candle_low
                        }
                    
                    # Vérifier si revisité (pour contexte)
                    if candle_low <= fvg['gap_high'] and candle_high >= fvg['gap_low']:
                        revisited = True
                
                # Convertir en ticks (0.25 point = 1 tick)
                max_distance_ticks = max_distance / 0.25
                
                distance_by_period[period] = {
                    'max_distance_points': max_distance,
                    'max_distance_ticks': max_distance_ticks,
                    'max_distance_candle': max_distance_candle,
                    'revisited': revisited
                }
            
            fvg['distance_by_period'] = distance_by_period
            fvgs.append(fvg)
    
    return fvgs

def analyze_avg_max_distance(fvgs, periods):
    """Calcule la distance maximale moyenne pour chaque période."""
    results = {}
    
    for period in periods:
        # Tous les FVGs
        all_distances = [f['distance_by_period'][period]['max_distance_ticks'] for f in fvgs]
        
        # Bons FVGs (non revisités)
        good_fvgs = [f for f in fvgs if not f['distance_by_period'][period]['revisited']]
        good_distances = [f['distance_by_period'][period]['max_distance_ticks'] for f in good_fvgs]
        
        # Mauvais FVGs (revisités)
        bad_fvgs = [f for f in fvgs if f['distance_by_period'][period]['revisited']]
        bad_distances = [f['distance_by_period'][period]['max_distance_ticks'] for f in bad_fvgs]
        
        # Par type
        bullish_distances = [f['distance_by_period'][period]['max_distance_ticks'] 
                            for f in fvgs if f['type'] == 'Bullish']
        bearish_distances = [f['distance_by_period'][period]['max_distance_ticks'] 
                            for f in fvgs if f['type'] == 'Bearish']
        
        results[period] = {
            'avg_all': sum(all_distances) / len(all_distances) if all_distances else 0,
            'avg_good': sum(good_distances) / len(good_distances) if good_distances else 0,
            'avg_bad': sum(bad_distances) / len(bad_distances) if bad_distances else 0,
            'avg_bullish': sum(bullish_distances) / len(bullish_distances) if bullish_distances else 0,
            'avg_bearish': sum(bearish_distances) / len(bearish_distances) if bearish_distances else 0,
            'max_distance': max(all_distances) if all_distances else 0,
            'min_distance': min(all_distances) if all_distances else 0,
            'count_total': len(fvgs),
            'count_good': len(good_fvgs),
            'count_bad': len(bad_fvgs)
        }
    
    return results

def main():
    """Fonction principale pour analyser les distances maximales."""
    periods = [5, 10, 15, 20, 25, 30]
    
    print("=" * 80)
    print("Analyse de la Distance Maximale (en ticks) depuis la Clôture de la 3ème Bougie")
    print("FVG à 8:30:00 - Année 2025")
    print("=" * 80)
    print()
    print("Note: 1 tick Nasdaq = 0.25 points")
    print()
    
    # Analyse 1 minute
    print("Chargement et analyse 1 MINUTE...")
    data_1m = load_csv_data('2025 1m.csv')
    fvgs_1m = detect_fvg_with_max_distance(data_1m, periods)
    results_1m = analyze_avg_max_distance(fvgs_1m, periods)
    
    print(f"  {len(fvgs_1m)} FVGs détectés à 8:30:00")
    print()
    
    # Analyse 5 minutes
    print("Chargement et analyse 5 MINUTES...")
    data_5m = load_csv_data('2025 5m.csv')
    fvgs_5m = detect_fvg_with_max_distance(data_5m, periods)
    results_5m = analyze_avg_max_distance(fvgs_5m, periods)
    
    print(f"  {len(fvgs_5m)} FVGs détectés à 8:30:00")
    print()
    
    # Analyse 15 minutes
    print("Chargement et analyse 15 MINUTES...")
    data_15m = load_csv_data('2025 15m.csv')
    fvgs_15m = detect_fvg_with_max_distance(data_15m, periods)
    results_15m = analyze_avg_max_distance(fvgs_15m, periods)
    
    print(f"  {len(fvgs_15m)} FVGs détectés à 8:30:00")
    print()
    
    # Afficher les résultats pour 1 minute
    print("=" * 80)
    print("RÉSULTATS 1 MINUTE (8:31 = clôture 3ème bougie)")
    print("=" * 80)
    print()
    print(f"{'Période':<12} {'Moy Tous':<12} {'Moy Bons':<12} {'Moy Mauvais':<14} {'Moy Bullish':<14} {'Moy Bearish':<12}")
    print(f"{'(bougies)':<12} {'(ticks)':<12} {'(ticks)':<12} {'(ticks)':<14} {'(ticks)':<14} {'(ticks)':<12}")
    print("-" * 80)
    
    for period in periods:
        r = results_1m[period]
        print(f"{period:2d}           {r['avg_all']:8.1f}    {r['avg_good']:8.1f}    "
              f"{r['avg_bad']:10.1f}    {r['avg_bullish']:10.1f}    {r['avg_bearish']:8.1f}")
    
    print()
    print("Distance maximale observée:")
    for period in periods:
        r = results_1m[period]
        print(f"  {period:2d} bougies: {r['max_distance']:8.1f} ticks ({r['max_distance']*0.25:.2f} points)")
    
    print()
    
    # Afficher les résultats pour 5 minutes
    print("=" * 80)
    print("RÉSULTATS 5 MINUTES (8:35 = clôture 3ème bougie)")
    print("=" * 80)
    print()
    print(f"{'Période':<12} {'Moy Tous':<12} {'Moy Bons':<12} {'Moy Mauvais':<14} {'Moy Bullish':<14} {'Moy Bearish':<12}")
    print(f"{'(bougies)':<12} {'(ticks)':<12} {'(ticks)':<12} {'(ticks)':<14} {'(ticks)':<14} {'(ticks)':<12}")
    print("-" * 80)
    
    for period in periods:
        r = results_5m[period]
        print(f"{period:2d}           {r['avg_all']:8.1f}    {r['avg_good']:8.1f}    "
              f"{r['avg_bad']:10.1f}    {r['avg_bullish']:10.1f}    {r['avg_bearish']:8.1f}")
    
    print()
    print("Distance maximale observée:")
    for period in periods:
        r = results_5m[period]
        print(f"  {period:2d} bougies: {r['max_distance']:8.1f} ticks ({r['max_distance']*0.25:.2f} points)")
    
    print()
    
    # Afficher les résultats pour 15 minutes
    print("=" * 80)
    print("RÉSULTATS 15 MINUTES (8:45 = clôture 3ème bougie)")
    print("=" * 80)
    print()
    print(f"{'Période':<12} {'Moy Tous':<12} {'Moy Bons':<12} {'Moy Mauvais':<14} {'Moy Bullish':<14} {'Moy Bearish':<12}")
    print(f"{'(bougies)':<12} {'(ticks)':<12} {'(ticks)':<12} {'(ticks)':<14} {'(ticks)':<14} {'(ticks)':<12}")
    print("-" * 80)
    
    for period in periods:
        r = results_15m[period]
        print(f"{period:2d}           {r['avg_all']:8.1f}    {r['avg_good']:8.1f}    "
              f"{r['avg_bad']:10.1f}    {r['avg_bullish']:10.1f}    {r['avg_bearish']:8.1f}")
    
    print()
    print("Distance maximale observée:")
    for period in periods:
        r = results_15m[period]
        print(f"  {period:2d} bougies: {r['max_distance']:8.1f} ticks ({r['max_distance']*0.25:.2f} points)")
    
    print()
    
    # Résumé comparatif
    print("=" * 80)
    print("RÉSUMÉ COMPARATIF - DISTANCE MOYENNE MAXIMALE (tous FVGs)")
    print("=" * 80)
    print()
    print(f"{'Période':<15} {'1m (ticks)':<15} {'5m (ticks)':<15} {'15m (ticks)':<15}")
    print("-" * 80)
    
    for period in periods:
        print(f"{period:2d} bougies     {results_1m[period]['avg_all']:8.1f}      "
              f"{results_5m[period]['avg_all']:8.1f}      {results_15m[period]['avg_all']:8.1f}")
    
    print()
    print("=" * 80)
    print("OBSERVATIONS CLÉS")
    print("=" * 80)
    print()
    
    # Comparaison bons vs mauvais FVGs
    print("1. Comparaison Bons vs Mauvais FVGs (5 bougies):")
    print()
    print("   1 MINUTE:")
    print(f"     - Bons FVGs:    {results_1m[5]['avg_good']:6.1f} ticks ({results_1m[5]['avg_good']*0.25:.2f} points)")
    print(f"     - Mauvais FVGs: {results_1m[5]['avg_bad']:6.1f} ticks ({results_1m[5]['avg_bad']*0.25:.2f} points)")
    print(f"     - Différence:   {results_1m[5]['avg_good'] - results_1m[5]['avg_bad']:6.1f} ticks")
    print()
    print("   5 MINUTES:")
    print(f"     - Bons FVGs:    {results_5m[5]['avg_good']:6.1f} ticks ({results_5m[5]['avg_good']*0.25:.2f} points)")
    print(f"     - Mauvais FVGs: {results_5m[5]['avg_bad']:6.1f} ticks ({results_5m[5]['avg_bad']*0.25:.2f} points)")
    print(f"     - Différence:   {results_5m[5]['avg_good'] - results_5m[5]['avg_bad']:6.1f} ticks")
    print()
    print("   15 MINUTES:")
    print(f"     - Bons FVGs:    {results_15m[5]['avg_good']:6.1f} ticks ({results_15m[5]['avg_good']*0.25:.2f} points)")
    print(f"     - Mauvais FVGs: {results_15m[5]['avg_bad']:6.1f} ticks ({results_15m[5]['avg_bad']*0.25:.2f} points)")
    print(f"     - Différence:   {results_15m[5]['avg_good'] - results_15m[5]['avg_bad']:6.1f} ticks")
    print()
    
    # Évolution dans le temps
    print("2. Évolution de la distance moyenne (tous FVGs):")
    print()
    for results, label in [
        (results_1m, '1 minute'),
        (results_5m, '5 minutes'),
        (results_15m, '15 minutes')
    ]:
        print(f"   {label.upper()}:")
        print(f"     - 5 bougies:  {results[5]['avg_all']:6.1f} ticks")
        print(f"     - 30 bougies: {results[30]['avg_all']:6.1f} ticks")
        evolution = results[30]['avg_all'] - results[5]['avg_all']
        evolution_pct = (evolution / results[5]['avg_all'] * 100) if results[5]['avg_all'] else 0
        print(f"     - Évolution:  {'+' if evolution >= 0 else ''}{evolution:.1f} ticks ({'+' if evolution_pct >= 0 else ''}{evolution_pct:.1f}%)")
        print()
    
    print("=" * 80)

if __name__ == "__main__":
    main()

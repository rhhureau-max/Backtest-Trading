#!/usr/bin/env python3
"""
Analyse temporelle de la qualité des FVG à 8:30:00 pour 2025

Ce script analyse comment la qualité des FVGs évolue sur différentes périodes:
- 5 bougies (analyse originale)
- 10 bougies
- 15 bougies
- 20 bougies
- 25 bougies
- 30 bougies

Un "bon" FVG reste valide si le prix ne revient pas dans la zone FVG
pendant la période analysée.
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

def detect_fvg_with_temporal_quality(data, periods=[5, 10, 15, 20, 25, 30]):
    """Détecte les FVGs à 8:30 et évalue leur qualité sur différentes périodes."""
    fvgs = []
    
    max_period = max(periods)
    
    for i in range(1, len(data) - max_period - 1):
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
                'index': i
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
                'index': i
            }
        
        if fvg:
            # Analyser pour chaque période
            quality_by_period = {}
            
            for period in periods:
                revisited = False
                first_revisit = None
                
                for j in range(i+2, min(i+2+period, len(data))):
                    candle = data[j]
                    candle_high = float(candle['high'])
                    candle_low = float(candle['low'])
                    
                    # Le prix entre dans la zone FVG
                    if candle_low <= fvg['gap_high'] and candle_high >= fvg['gap_low']:
                        revisited = True
                        if first_revisit is None:
                            first_revisit = {
                                'candle_number': j - i - 1,  # Nombre de bougies après FVG
                                'date': candle['date'],
                                'time': candle['time']
                            }
                        break
                
                quality_by_period[period] = {
                    'is_good': not revisited,
                    'revisited': revisited,
                    'first_revisit': first_revisit
                }
            
            fvg['quality_by_period'] = quality_by_period
            fvgs.append(fvg)
    
    return fvgs

def analyze_temporal_evolution(fvgs, periods):
    """Analyse l'évolution de la qualité dans le temps."""
    results = {}
    
    for period in periods:
        good_fvgs = [f for f in fvgs if f['quality_by_period'][period]['is_good']]
        bad_fvgs = [f for f in fvgs if not f['quality_by_period'][period]['is_good']]
        
        good_bullish = [f for f in good_fvgs if f['type'] == 'Bullish']
        good_bearish = [f for f in good_fvgs if f['type'] == 'Bearish']
        
        results[period] = {
            'total': len(fvgs),
            'good': len(good_fvgs),
            'bad': len(bad_fvgs),
            'good_percent': len(good_fvgs) / len(fvgs) * 100 if fvgs else 0,
            'good_bullish': len(good_bullish),
            'good_bearish': len(good_bearish)
        }
    
    return results

def main():
    """Fonction principale pour analyser l'évolution temporelle de la qualité des FVGs."""
    periods = [5, 10, 15, 20, 25, 30]
    
    print("=" * 80)
    print("Analyse Temporelle de la Qualité des FVG à 8:30:00 - Année 2025")
    print("=" * 80)
    print()
    print("Analyse de la qualité des FVGs sur différentes périodes:")
    print(f"  Périodes analysées: {', '.join([str(p) + ' bougies' for p in periods])}")
    print()
    
    # Analyse 1 minute
    print("Chargement et analyse 1 MINUTE...")
    data_1m = load_csv_data('2025 1m.csv')
    fvgs_1m = detect_fvg_with_temporal_quality(data_1m, periods)
    results_1m = analyze_temporal_evolution(fvgs_1m, periods)
    
    print(f"  {len(fvgs_1m)} FVGs détectés à 8:30:00")
    print()
    
    # Analyse 15 minutes
    print("Chargement et analyse 15 MINUTES...")
    data_15m = load_csv_data('2025 15m.csv')
    fvgs_15m = detect_fvg_with_temporal_quality(data_15m, periods)
    results_15m = analyze_temporal_evolution(fvgs_15m, periods)
    
    print(f"  {len(fvgs_15m)} FVGs détectés à 8:30:00")
    print()
    
    # Afficher les résultats pour 1 minute
    print("=" * 80)
    print("RÉSULTATS 1 MINUTE")
    print("=" * 80)
    print()
    print(f"{'Période':<12} {'Total':<8} {'Bons':<8} {'Mauvais':<10} {'% Bons':<10} {'Bullish':<10} {'Bearish':<10}")
    print("-" * 80)
    
    for period in periods:
        r = results_1m[period]
        print(f"{period:2d} bougies   {r['total']:<8} {r['good']:<8} {r['bad']:<10} "
              f"{r['good_percent']:6.1f}%    {r['good_bullish']:<10} {r['good_bearish']:<10}")
    
    print()
    print("Évolution:")
    prev_good = None
    for period in periods:
        current_good = results_1m[period]['good']
        if prev_good is not None:
            change = current_good - prev_good
            change_str = f"({'+'if change >= 0 else ''}{change})"
        else:
            change_str = ""
        print(f"  {period:2d} bougies: {current_good:3d} bons FVGs {change_str}")
        prev_good = current_good
    
    print()
    
    # Afficher les résultats pour 15 minutes
    print("=" * 80)
    print("RÉSULTATS 15 MINUTES")
    print("=" * 80)
    print()
    print(f"{'Période':<12} {'Total':<8} {'Bons':<8} {'Mauvais':<10} {'% Bons':<10} {'Bullish':<10} {'Bearish':<10}")
    print("-" * 80)
    
    for period in periods:
        r = results_15m[period]
        print(f"{period:2d} bougies   {r['total']:<8} {r['good']:<8} {r['bad']:<10} "
              f"{r['good_percent']:6.1f}%    {r['good_bullish']:<10} {r['good_bearish']:<10}")
    
    print()
    print("Évolution:")
    prev_good = None
    for period in periods:
        current_good = results_15m[period]['good']
        if prev_good is not None:
            change = current_good - prev_good
            change_str = f"({'+'if change >= 0 else ''}{change})"
        else:
            change_str = ""
        print(f"  {period:2d} bougies: {current_good:3d} bons FVGs {change_str}")
        prev_good = current_good
    
    print()
    
    # Résumé comparatif
    print("=" * 80)
    print("COMPARAISON GLOBALE")
    print("=" * 80)
    print()
    print(f"{'Période':<15} {'1m - % Bons':<15} {'15m - % Bons':<15} {'Total - % Bons':<15}")
    print("-" * 80)
    
    for period in periods:
        total_good = results_1m[period]['good'] + results_15m[period]['good']
        total_all = results_1m[period]['total'] + results_15m[period]['total']
        total_percent = total_good / total_all * 100 if total_all else 0
        
        print(f"{period:2d} bougies     {results_1m[period]['good_percent']:6.1f}%         "
              f"{results_15m[period]['good_percent']:6.1f}%         {total_percent:6.1f}%")
    
    print()
    print("=" * 80)
    print("OBSERVATIONS")
    print("=" * 80)
    print()
    
    # Calculer la dégradation
    total_initial = results_1m[5]['good'] + results_15m[5]['good']
    total_final = results_1m[30]['good'] + results_15m[30]['good']
    total_fvgs = len(fvgs_1m) + len(fvgs_15m)
    
    degradation = total_initial - total_final
    degradation_percent = (degradation / total_initial * 100) if total_initial else 0
    
    print(f"1. Dégradation de 5 à 30 bougies:")
    print(f"   - Bons FVGs à 5 bougies:  {total_initial}/{total_fvgs} ({total_initial/total_fvgs*100:.1f}%)")
    print(f"   - Bons FVGs à 30 bougies: {total_final}/{total_fvgs} ({total_final/total_fvgs*100:.1f}%)")
    print(f"   - Perte de {degradation} FVGs ({degradation_percent:.1f}% de dégradation)")
    print()
    
    # Taux de survie
    survival_rate = (total_final / total_initial * 100) if total_initial else 0
    print(f"2. Taux de survie:")
    print(f"   - {survival_rate:.1f}% des FVGs 'bons' à 5 bougies restent 'bons' à 30 bougies")
    print()
    
    # Analyse des périodes critiques
    print("3. Périodes critiques (plus grande dégradation):")
    max_degradation = 0
    critical_period = None
    
    for i in range(len(periods)-1):
        current_period = periods[i]
        next_period = periods[i+1]
        
        current_good = results_1m[current_period]['good'] + results_15m[current_period]['good']
        next_good = results_1m[next_period]['good'] + results_15m[next_period]['good']
        
        degradation_step = current_good - next_good
        
        if degradation_step > max_degradation:
            max_degradation = degradation_step
            critical_period = (current_period, next_period)
    
    if critical_period:
        print(f"   - Entre {critical_period[0]} et {critical_period[1]} bougies: perte de {max_degradation} FVGs")
    
    print()
    print("=" * 80)

if __name__ == "__main__":
    main()

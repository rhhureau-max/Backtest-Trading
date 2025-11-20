#!/usr/bin/env python3
"""
Analyse de la qualité des FVGs par timeframe pour 2025
Compare les bons vs mauvais FVGs pour 1m, 5m et 15m séparément
"""

import csv
from datetime import datetime

def detect_fvgs_at_830(csv_file):
    """Détecte les FVGs où 8:30 est la bougie du milieu"""
    fvgs = []
    
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f, delimiter=';', fieldnames=['date', 'time', 'open', 'high', 'low', 'close', 'volume'])
        next(reader)  # Skip header row
        rows = list(reader)
    
    for i in range(1, len(rows) - 1):
        middle = rows[i]
        
        # Vérifier si c'est 8:30
        if middle['time'] != '08:30:00':
            continue
            
        previous = rows[i-1]
        next_candle = rows[i+1]
        
        prev_high = float(previous['high'])
        prev_low = float(previous['low'])
        next_high = float(next_candle['high'])
        next_low = float(next_candle['low'])
        
        # Bullish FVG: next low > previous high
        if next_low > prev_high:
            gap_size = next_low - prev_high
            fvg_zone = (prev_high, next_low)
            fvgs.append({
                'date': middle['date'],
                'time': middle['time'],
                'type': 'Bullish',
                'gap_size': gap_size,
                'fvg_zone': fvg_zone,
                'index': i,
                'rows': rows
            })
        # Bearish FVG: next high < previous low
        elif next_high < prev_low:
            gap_size = prev_low - next_high
            fvg_zone = (next_high, prev_low)
            fvgs.append({
                'date': middle['date'],
                'time': middle['time'],
                'type': 'Bearish',
                'gap_size': gap_size,
                'fvg_zone': fvg_zone,
                'index': i,
                'rows': rows
            })
    
    return fvgs

def check_fvg_quality(fvg, num_candles):
    """Vérifie si le FVG est bon (pas revisité) après num_candles bougies"""
    rows = fvg['rows']
    fvg_index = fvg['index']
    fvg_zone_low, fvg_zone_high = fvg['fvg_zone']
    
    # Vérifier les N bougies suivantes (après la bougie next)
    start_index = fvg_index + 2  # On commence après la bougie "next"
    end_index = min(start_index + num_candles, len(rows))
    
    for i in range(start_index, end_index):
        candle = rows[i]
        candle_high = float(candle['high'])
        candle_low = float(candle['low'])
        
        # Vérifier si le prix revient dans la zone FVG
        if candle_low <= fvg_zone_high and candle_high >= fvg_zone_low:
            return False  # Mauvais FVG (revisité)
    
    return True  # Bon FVG (pas revisité)

def analyze_timeframe(csv_file, timeframe_name):
    """Analyse un timeframe spécifique"""
    print(f"\n{'='*80}")
    print(f"ANALYSE TIMEFRAME: {timeframe_name}")
    print(f"{'='*80}")
    
    fvgs = detect_fvgs_at_830(csv_file)
    
    if not fvgs:
        print(f"Aucun FVG trouvé à 8:30 pour {timeframe_name}")
        return None
    
    print(f"\nTotal FVGs à 8:30:00: {len(fvgs)}")
    
    # Compter par type
    bullish_count = sum(1 for f in fvgs if f['type'] == 'Bullish')
    bearish_count = sum(1 for f in fvgs if f['type'] == 'Bearish')
    print(f"  - Bullish: {bullish_count}")
    print(f"  - Bearish: {bearish_count}")
    
    # Analyser la qualité à différentes périodes
    periods = [5, 10, 15, 20, 25, 30]
    results = {}
    
    for period in periods:
        good_fvgs = []
        good_bullish = 0
        good_bearish = 0
        
        for fvg in fvgs:
            if check_fvg_quality(fvg, period):
                good_fvgs.append(fvg)
                if fvg['type'] == 'Bullish':
                    good_bullish += 1
                else:
                    good_bearish += 1
        
        results[period] = {
            'total': len(good_fvgs),
            'bullish': good_bullish,
            'bearish': good_bearish,
            'percentage': (len(good_fvgs) / len(fvgs) * 100) if fvgs else 0
        }
    
    # Afficher le tableau des résultats
    print(f"\n{'-'*80}")
    print(f"ÉVOLUTION DE LA QUALITÉ POUR {timeframe_name}")
    print(f"{'-'*80}")
    print(f"{'Période':<15} {'Bons FVGs':<15} {'% Bons':<15} {'Bullish':<15} {'Bearish':<15}")
    print(f"{'-'*80}")
    
    for period in periods:
        r = results[period]
        print(f"{period:>2} bougies      {r['total']:>3}/{len(fvgs):<7}  {r['percentage']:>6.1f}%        {r['bullish']:>3}             {r['bearish']:>3}")
    
    print(f"{'-'*80}")
    
    # Calcul de la dégradation
    initial = results[5]['total']
    final = results[30]['total']
    degradation = initial - final
    survival_rate = (final / initial * 100) if initial > 0 else 0
    
    print(f"\nSTATISTIQUES DE DÉGRADATION:")
    print(f"  - Bons FVGs à 5 bougies: {initial}")
    print(f"  - Bons FVGs à 30 bougies: {final}")
    print(f"  - Dégradation totale: {degradation} FVGs perdus (-{initial - final} soit {(degradation/initial*100):.1f}%)")
    print(f"  - Taux de survie: {survival_rate:.1f}% des FVGs bons à 5 restent bons à 30")
    
    # Trouver la période avec la plus grande perte
    max_loss = 0
    max_loss_period = None
    for i in range(len(periods) - 1):
        loss = results[periods[i]]['total'] - results[periods[i+1]]['total']
        if loss > max_loss:
            max_loss = loss
            max_loss_period = (periods[i], periods[i+1])
    
    if max_loss_period:
        print(f"  - Plus grande perte: {max_loss} FVGs entre {max_loss_period[0]} et {max_loss_period[1]} bougies")
    
    return {
        'timeframe': timeframe_name,
        'total_fvgs': len(fvgs),
        'bullish': bullish_count,
        'bearish': bearish_count,
        'results': results
    }

def main():
    print("="*80)
    print("ANALYSE DE LA QUALITÉ DES FVGs PAR TIMEFRAME (2025)")
    print("Analyse des FVGs à 8:30:00 pour 1m, 5m et 15m")
    print("="*80)
    
    # Analyser chaque timeframe
    results_1m = analyze_timeframe('./2025 1m.csv', '1 MINUTE')
    results_5m = analyze_timeframe('./2025 5m.csv', '5 MINUTES')
    results_15m = analyze_timeframe('./2025 15m.csv', '15 MINUTES')
    
    # Tableau comparatif global
    print(f"\n{'='*80}")
    print("COMPARAISON GLOBALE PAR TIMEFRAME")
    print(f"{'='*80}")
    
    all_results = []
    if results_1m:
        all_results.append(results_1m)
    if results_5m:
        all_results.append(results_5m)
    if results_15m:
        all_results.append(results_15m)
    
    if not all_results:
        print("Aucun résultat à afficher")
        return
    
    # Tableau par période
    periods = [5, 10, 15, 20, 25, 30]
    
    print(f"\n{'-'*100}")
    print(f"COMPARAISON DES BONS FVGs PAR PÉRIODE")
    print(f"{'-'*100}")
    print(f"{'Période':<15} {'1m':<25} {'5m':<25} {'15m':<25}")
    print(f"{'-'*100}")
    
    for period in periods:
        row = f"{period:>2} bougies     "
        
        for result in all_results:
            if result:
                r = result['results'][period]
                total = result['total_fvgs']
                pct = r['percentage']
                row += f"{r['total']:>3}/{total:<3} ({pct:>5.1f}%)       "
        
        print(row)
    
    print(f"{'-'*100}")
    
    # Résumé final
    print(f"\n{'='*80}")
    print("RÉSUMÉ PAR TIMEFRAME")
    print(f"{'='*80}")
    
    for result in all_results:
        if result:
            tf = result['timeframe']
            total = result['total_fvgs']
            r5 = result['results'][5]
            r30 = result['results'][30]
            
            print(f"\n{tf}:")
            print(f"  - Total FVGs: {total}")
            print(f"  - Bullish: {result['bullish']} | Bearish: {result['bearish']}")
            print(f"  - Bons FVGs à 5 bougies: {r5['total']} ({r5['percentage']:.1f}%)")
            print(f"  - Bons FVGs à 30 bougies: {r30['total']} ({r30['percentage']:.1f}%)")
            print(f"  - Dégradation: {r5['total'] - r30['total']} FVGs ({(r5['total'] - r30['total'])/r5['total']*100:.1f}%)")
    
    # Observations
    print(f"\n{'='*80}")
    print("OBSERVATIONS CLÉS")
    print(f"{'='*80}")
    
    print("\n1. TAUX DE SUCCÈS INITIAL (5 bougies):")
    for result in all_results:
        if result:
            r5 = result['results'][5]
            print(f"   - {result['timeframe']}: {r5['percentage']:.1f}%")
    
    print("\n2. TAUX DE SURVIE (5 → 30 bougies):")
    for result in all_results:
        if result:
            r5 = result['results'][5]
            r30 = result['results'][30]
            survival = (r30['total'] / r5['total'] * 100) if r5['total'] > 0 else 0
            print(f"   - {result['timeframe']}: {survival:.1f}% des FVGs bons à 5 restent bons à 30")
    
    print("\n3. PERFORMANCE BULLISH vs BEARISH (à 5 bougies):")
    for result in all_results:
        if result:
            r5 = result['results'][5]
            bull_pct = (r5['bullish'] / result['bullish'] * 100) if result['bullish'] > 0 else 0
            bear_pct = (r5['bearish'] / result['bearish'] * 100) if result['bearish'] > 0 else 0
            print(f"   - {result['timeframe']}: Bullish {bull_pct:.1f}% | Bearish {bear_pct:.1f}%")

if __name__ == '__main__':
    main()

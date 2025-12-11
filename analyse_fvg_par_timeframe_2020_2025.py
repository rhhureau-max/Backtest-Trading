#!/usr/bin/env python3
"""
Analyse des FVGs par timeframe pour 2020-2025
Compare la qualité des FVGs à 8:30:00 entre 1m, 5m et 15m
"""

import csv
from datetime import datetime
import os

# Définir le tick pour Nasdaq (0.25 = 1 tick)
TICK_SIZE = 0.25

def detect_fvgs_at_830(csv_file, timeframe):
    """Détecte les FVGs où 8:30:00 est la bougie du milieu"""
    fvgs = []
    
    with open(csv_file, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f, delimiter=';')
        rows = list(reader)
    
    # Renommer les colonnes si nécessaire
    for row in rows:
        if 'Column1' in row:
            row['date'] = row['Column1']
            row['time'] = row['Column1'] + ' ' + row['Column2']
            row['open'] = row['Column3']
            row['high'] = row['Column4']
            row['low'] = row['Column5']
            row['close'] = row['Column6']
    
    for i in range(1, len(rows) - 1):
        prev = rows[i-1]
        middle = rows[i]
        next_candle = rows[i+1]
        
        # Filtrer pour 8:30:00 comme bougie du milieu
        middle_time = middle.get('time', '') or (middle.get('Column1', '') + ' ' + middle.get('Column2', ''))
        if '08:30:00' not in middle_time and '8:30:00' not in middle_time:
            continue
        
        # Extraire les valeurs OHLC
        if 'high' not in middle:
            middle['time'] = middle_time
            middle['date'] = middle_time.split()[0]
        
        prev_high = float(prev.get('high') or prev.get('Column4', 0))
        prev_low = float(prev.get('low') or prev.get('Column5', 0))
        next_high = float(next_candle.get('high') or next_candle.get('Column4', 0))
        next_low = float(next_candle.get('low') or next_candle.get('Column5', 0))
        
        # Détection FVG
        fvg_type = None
        gap_size = 0
        
        if next_low > prev_high:  # Bullish FVG
            fvg_type = 'Bullish'
            gap_size = next_low - prev_high
        elif next_high < prev_low:  # Bearish FVG
            fvg_type = 'Bearish'
            gap_size = prev_low - next_high
        
        if fvg_type:
            fvgs.append({
                'date': middle['time'].split()[0],
                'time': middle['time'],
                'type': fvg_type,
                'gap_size': gap_size,
                'prev_index': i-1,
                'middle_index': i,
                'next_index': i+1,
                'fvg_low': prev_high if fvg_type == 'Bullish' else next_high,
                'fvg_high': next_low if fvg_type == 'Bullish' else prev_low,
                'third_candle_close': float(next_candle.get('close') or next_candle.get('Column6', 0))
            })
    
    return fvgs, rows

def check_fvg_quality(fvg, rows, period):
    """Vérifie si le FVG est 'bon' (non revisité) après X bougies"""
    start_idx = fvg['next_index'] + 1
    end_idx = min(start_idx + period, len(rows))
    
    fvg_low = fvg['fvg_low']
    fvg_high = fvg['fvg_high']
    
    for idx in range(start_idx, end_idx):
        candle_high = float(rows[idx].get('high') or rows[idx].get('Column4', 0))
        candle_low = float(rows[idx].get('low') or rows[idx].get('Column5', 0))
        
        # Vérifier si le prix revisite la zone FVG
        if candle_low <= fvg_high and candle_high >= fvg_low:
            return False  # Mauvais FVG
    
    return True  # Bon FVG

def calculate_max_distance(fvg, rows, period):
    """Calcule la distance maximale depuis la clôture de la 3ème bougie"""
    start_idx = fvg['next_index']
    end_idx = min(start_idx + period + 1, len(rows))
    
    third_close = fvg['third_candle_close']
    max_dist = 0
    
    for idx in range(start_idx, end_idx):
        high = float(rows[idx].get('high') or rows[idx].get('Column4', 0))
        low = float(rows[idx].get('low') or rows[idx].get('Column5', 0))
        
        dist_high = abs(high - third_close)
        dist_low = abs(low - third_close)
        max_dist = max(max_dist, dist_high, dist_low)
    
    return max_dist

def analyze_timeframe(years, timeframe):
    """Analyse un timeframe pour plusieurs années"""
    all_fvgs = []
    
    for year in years:
        csv_file = f'/home/runner/work/Backtest-Trading/Backtest-Trading/{year} {timeframe}.csv'
        if not os.path.exists(csv_file):
            continue
        
        fvgs, rows = detect_fvgs_at_830(csv_file, timeframe)
        
        # Ajouter l'analyse de qualité et distance pour chaque FVG
        for fvg in fvgs:
            fvg['year'] = year
            fvg['rows'] = rows
            all_fvgs.append(fvg)
    
    return all_fvgs

def main():
    years_5m_15m = [2020, 2021, 2022, 2023, 2024, 2025]
    years_1m = [2025]  # Seul 2025 a les données 1m
    
    print("="*80)
    print("ANALYSE DES FVGs PAR TIMEFRAME (2020-2025)")
    print("Bougie du milieu à 8:30:00")
    print("="*80)
    print()
    
    # Analyser chaque timeframe
    results = {}
    
    print("Analyse en cours...")
    print()
    
    # 1 minute (2025 seulement)
    print("Analyse 1 minute (2025)...")
    fvgs_1m = analyze_timeframe(years_1m, '1m')
    results['1m'] = fvgs_1m
    print(f"  Trouvé: {len(fvgs_1m)} FVGs")
    
    # 5 minutes
    print("Analyse 5 minutes (2020-2025)...")
    fvgs_5m = analyze_timeframe(years_5m_15m, '5m')
    results['5m'] = fvgs_5m
    print(f"  Trouvé: {len(fvgs_5m)} FVGs")
    
    # 15 minutes
    print("Analyse 15 minutes (2020-2025)...")
    fvgs_15m = analyze_timeframe(years_5m_15m, '15m')
    results['15m'] = fvgs_15m
    print(f"  Trouvé: {len(fvgs_15m)} FVGs")
    
    print()
    print("="*80)
    print("RÉSUMÉ PAR TIMEFRAME")
    print("="*80)
    print()
    
    periods = [5, 10, 15, 20, 25, 30]
    
    for tf, fvgs in results.items():
        if not fvgs:
            continue
        
        print(f"\n{'='*80}")
        print(f"TIMEFRAME: {tf.upper()}")
        if tf == '1m':
            print("Période: 2025 uniquement")
        else:
            print("Période: 2020-2025")
        print(f"{'='*80}\n")
        
        total_fvgs = len(fvgs)
        bullish = [f for f in fvgs if f['type'] == 'Bullish']
        bearish = [f for f in fvgs if f['type'] == 'Bearish']
        
        print(f"Total FVGs: {total_fvgs}")
        print(f"  Bullish: {len(bullish)} ({len(bullish)/total_fvgs*100:.1f}%)")
        print(f"  Bearish: {len(bearish)} ({len(bearish)/total_fvgs*100:.1f}%)")
        print()
        
        # Analyse de qualité par période
        print("QUALITÉ DES FVGs PAR PÉRIODE:")
        print("-" * 60)
        print(f"{'Période':<12} {'Bons':<8} {'%':<8} {'Bull Good':<12} {'Bear Good':<12}")
        print("-" * 60)
        
        for period in periods:
            good_count = 0
            good_bull = 0
            good_bear = 0
            
            for fvg in fvgs:
                if check_fvg_quality(fvg, fvg['rows'], period):
                    good_count += 1
                    if fvg['type'] == 'Bullish':
                        good_bull += 1
                    else:
                        good_bear += 1
            
            pct = good_count / total_fvgs * 100 if total_fvgs > 0 else 0
            bull_pct = good_bull / len(bullish) * 100 if bullish else 0
            bear_pct = good_bear / len(bearish) * 100 if bearish else 0
            
            print(f"{period:2d} bougies  {good_count:3d}     {pct:5.1f}%  "
                  f"{good_bull}/{len(bullish)} ({bull_pct:4.1f}%)  "
                  f"{good_bear}/{len(bearish)} ({bear_pct:4.1f}%)")
        
        print()
        
        # Analyse de distance
        print("DISTANCE MAXIMALE MOYENNE (en ticks):")
        print("-" * 80)
        print(f"{'Période':<12} {'Tous':<12} {'Bons':<12} {'Mauvais':<12} {'Diff %':<10}")
        print("-" * 80)
        
        for period in periods:
            all_distances = []
            good_distances = []
            bad_distances = []
            
            for fvg in fvgs:
                dist = calculate_max_distance(fvg, fvg['rows'], period)
                dist_ticks = dist / TICK_SIZE
                all_distances.append(dist_ticks)
                
                if check_fvg_quality(fvg, fvg['rows'], 5):  # Bon à 5 bougies
                    good_distances.append(dist_ticks)
                else:
                    bad_distances.append(dist_ticks)
            
            avg_all = sum(all_distances) / len(all_distances) if all_distances else 0
            avg_good = sum(good_distances) / len(good_distances) if good_distances else 0
            avg_bad = sum(bad_distances) / len(bad_distances) if bad_distances else 0
            diff_pct = ((avg_good - avg_bad) / avg_bad * 100) if avg_bad > 0 else 0
            
            print(f"{period:2d} bougies  {avg_all:8.1f}    {avg_good:8.1f}    "
                  f"{avg_bad:8.1f}    {diff_pct:+6.1f}%")
        
        print()
    
    # Comparaison finale
    print("\n" + "="*80)
    print("COMPARAISON GLOBALE DES TIMEFRAMES")
    print("="*80)
    print()
    
    print(f"{'Timeframe':<12} {'Période':<12} {'Total FVGs':<12} {'% Bons (5)':<15} "
          f"{'Dist Bons':<15} {'Dist Diff %':<12}")
    print("-" * 90)
    
    for tf in ['1m', '5m', '15m']:
        fvgs = results[tf]
        if not fvgs:
            continue
        
        total = len(fvgs)
        
        # Qualité à 5 bougies
        good_5 = sum(1 for f in fvgs if check_fvg_quality(f, f['rows'], 5))
        pct_5 = good_5 / total * 100 if total > 0 else 0
        
        # Distance moyenne pour bons FVGs
        good_dists = []
        bad_dists = []
        for fvg in fvgs:
            dist = calculate_max_distance(fvg, fvg['rows'], 5)
            dist_ticks = dist / TICK_SIZE
            if check_fvg_quality(fvg, fvg['rows'], 5):
                good_dists.append(dist_ticks)
            else:
                bad_dists.append(dist_ticks)
        
        avg_good_dist = sum(good_dists) / len(good_dists) if good_dists else 0
        avg_bad_dist = sum(bad_dists) / len(bad_dists) if bad_dists else 0
        diff_pct = ((avg_good_dist - avg_bad_dist) / avg_bad_dist * 100) if avg_bad_dist > 0 else 0
        
        period_str = "2025" if tf == '1m' else "2020-2025"
        
        print(f"{tf:<12} {period_str:<12} {total:<12} {pct_5:5.1f}% ({good_5})    "
              f"{avg_good_dist:8.1f} ticks {diff_pct:+6.1f}%")
    
    print()
    print("="*80)
    print("Note: 0.25 points = 1 tick Nasdaq")
    print("="*80)

if __name__ == '__main__':
    main()

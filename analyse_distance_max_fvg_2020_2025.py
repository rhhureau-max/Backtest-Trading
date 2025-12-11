#!/usr/bin/env python3
"""
Analyse de distance maximale des FVGs pour 2020-2025
Mesure la distance maximale depuis la clôture de la 3ème bougie
"""

import csv
from datetime import datetime
import os

# Définir le tick pour Nasdaq (0.25 = 1 tick)
TICK_SIZE = 0.25

def detect_fvgs_at_830(csv_file, timeframe):
    """Détecte les FVGs où 8:30:00 est la bougie du milieu"""
    fvgs = []
    
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    for i in range(1, len(rows) - 1):
        prev = rows[i-1]
        middle = rows[i]
        next_candle = rows[i+1]
        
        # Filtrer pour 8:30:00 comme bougie du milieu
        middle_time = middle['time']
        if '08:30:00' not in middle_time and '8:30:00' not in middle_time:
            continue
        
        prev_high = float(prev['high'])
        prev_low = float(prev['low'])
        next_high = float(next_candle['high'])
        next_low = float(next_candle['low'])
        
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
                'third_candle_close': float(next_candle['close'])
            })
    
    return fvgs, rows

def check_fvg_quality(fvg, rows, period):
    """Vérifie si le FVG est 'bon' (non revisité) après X bougies"""
    start_idx = fvg['next_index'] + 1
    end_idx = min(start_idx + period, len(rows))
    
    fvg_low = fvg['fvg_low']
    fvg_high = fvg['fvg_high']
    
    for idx in range(start_idx, end_idx):
        candle_high = float(rows[idx]['high'])
        candle_low = float(rows[idx]['low'])
        
        if candle_low <= fvg_high and candle_high >= fvg_low:
            return False
    
    return True

def calculate_max_distance(fvg, rows, period):
    """Calcule la distance maximale depuis la clôture de la 3ème bougie"""
    start_idx = fvg['next_index']
    end_idx = min(start_idx + period + 1, len(rows))
    
    third_close = fvg['third_candle_close']
    max_dist = 0
    
    for idx in range(start_idx, end_idx):
        high = float(rows[idx]['high'])
        low = float(rows[idx]['low'])
        
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
        
        for fvg in fvgs:
            fvg['year'] = year
            fvg['rows'] = rows
            all_fvgs.append(fvg)
    
    return all_fvgs

def main():
    years_5m_15m = [2020, 2021, 2022, 2023, 2024, 2025]
    years_1m = [2025]
    
    print("="*80)
    print("ANALYSE DE DISTANCE MAXIMALE DES FVGs (2020-2025)")
    print("Distance depuis la clôture de la 3ème bougie")
    print("="*80)
    print()
    
    results = {}
    
    print("Analyse en cours...")
    
    fvgs_1m = analyze_timeframe(years_1m, '1m')
    results['1m'] = fvgs_1m
    print(f"1 minute (2025): {len(fvgs_1m)} FVGs")
    
    fvgs_5m = analyze_timeframe(years_5m_15m, '5m')
    results['5m'] = fvgs_5m
    print(f"5 minutes (2020-2025): {len(fvgs_5m)} FVGs")
    
    fvgs_15m = analyze_timeframe(years_5m_15m, '15m')
    results['15m'] = fvgs_15m
    print(f"15 minutes (2020-2025): {len(fvgs_15m)} FVGs")
    
    print()
    print("="*80)
    print("DISTANCE MAXIMALE PAR TIMEFRAME ET PÉRIODE")
    print("="*80)
    print()
    
    periods = [5, 10, 15, 20, 25, 30]
    
    for tf, fvgs in results.items():
        if not fvgs:
            continue
        
        print(f"\n{'='*80}")
        print(f"TIMEFRAME: {tf.upper()}")
        if tf == '1m':
            print("Période: 2025")
        else:
            print("Période: 2020-2025")
        print(f"Total FVGs: {len(fvgs)}")
        print(f"{'='*80}\n")
        
        print("DISTANCE MAXIMALE MOYENNE (en ticks) :")
        print("-" * 100)
        print(f"{'Période':<12} {'Tous FVGs':<15} {'Bons FVGs':<15} {'Mauvais FVGs':<15} "
              f"{'Diff':<15} {'Diff %':<10}")
        print("-" * 100)
        
        for period in periods:
            all_distances = []
            good_distances = []
            bad_distances = []
            
            for fvg in fvgs:
                dist = calculate_max_distance(fvg, fvg['rows'], period)
                dist_ticks = dist / TICK_SIZE
                all_distances.append(dist_ticks)
                
                if check_fvg_quality(fvg, fvg['rows'], 5):
                    good_distances.append(dist_ticks)
                else:
                    bad_distances.append(dist_ticks)
            
            avg_all = sum(all_distances) / len(all_distances) if all_distances else 0
            avg_good = sum(good_distances) / len(good_distances) if good_distances else 0
            avg_bad = sum(bad_distances) / len(bad_distances) if bad_distances else 0
            diff = avg_good - avg_bad
            diff_pct = (diff / avg_bad * 100) if avg_bad > 0 else 0
            
            print(f"{period:2d} bougies  {avg_all:10.1f}      {avg_good:10.1f}      "
                  f"{avg_bad:10.1f}      {diff:+10.1f}      {diff_pct:+6.1f}%")
        
        print()
        
        # Distance en points
        print("DISTANCE MAXIMALE MOYENNE (en points) :")
        print("-" * 100)
        print(f"{'Période':<12} {'Tous FVGs':<15} {'Bons FVGs':<15} {'Mauvais FVGs':<15} "
              f"{'Diff':<15}")
        print("-" * 100)
        
        for period in periods:
            all_distances = []
            good_distances = []
            bad_distances = []
            
            for fvg in fvgs:
                dist = calculate_max_distance(fvg, fvg['rows'], period)
                all_distances.append(dist)
                
                if check_fvg_quality(fvg, fvg['rows'], 5):
                    good_distances.append(dist)
                else:
                    bad_distances.append(dist)
            
            avg_all = sum(all_distances) / len(all_distances) if all_distances else 0
            avg_good = sum(good_distances) / len(good_distances) if good_distances else 0
            avg_bad = sum(bad_distances) / len(bad_distances) if bad_distances else 0
            diff = avg_good - avg_bad
            
            print(f"{period:2d} bougies  {avg_all:10.2f}      {avg_good:10.2f}      "
                  f"{avg_bad:10.2f}      {diff:+10.2f}")
        
        print()
    
    # Comparaison globale
    print("\n" + "="*80)
    print("COMPARAISON GLOBALE @ 5 BOUGIES")
    print("="*80)
    print()
    
    print(f"{'Timeframe':<15} {'Période':<15} {'Tous':<15} {'Bons':<15} {'Mauvais':<15} {'Diff %':<10}")
    print("-" * 95)
    
    for tf in ['1m', '5m', '15m']:
        fvgs = results[tf]
        if not fvgs:
            continue
        
        all_distances = []
        good_distances = []
        bad_distances = []
        
        for fvg in fvgs:
            dist = calculate_max_distance(fvg, fvg['rows'], 5)
            dist_ticks = dist / TICK_SIZE
            all_distances.append(dist_ticks)
            
            if check_fvg_quality(fvg, fvg['rows'], 5):
                good_distances.append(dist_ticks)
            else:
                bad_distances.append(dist_ticks)
        
        avg_all = sum(all_distances) / len(all_distances) if all_distances else 0
        avg_good = sum(good_distances) / len(good_distances) if good_distances else 0
        avg_bad = sum(bad_distances) / len(bad_distances) if bad_distances else 0
        diff_pct = ((avg_good - avg_bad) / avg_bad * 100) if avg_bad > 0 else 0
        
        period_str = "2025" if tf == '1m' else "2020-2025"
        
        print(f"{tf:<15} {period_str:<15} {avg_all:10.1f}      {avg_good:10.1f}      "
              f"{avg_bad:10.1f}      {diff_pct:+6.1f}%")
    
    print()
    
    # Recommandations de trading
    print("\n" + "="*80)
    print("RECOMMANDATIONS DE PROFIT TARGET (basé sur distance moyenne @ 5 bougies)")
    print("="*80)
    print()
    
    for tf in ['1m', '5m', '15m']:
        fvgs = results[tf]
        if not fvgs:
            continue
        
        good_distances = []
        for fvg in fvgs:
            if check_fvg_quality(fvg, fvg['rows'], 5):
                dist = calculate_max_distance(fvg, fvg['rows'], 5)
                good_distances.append(dist)
        
        avg_good_dist = sum(good_distances) / len(good_distances) if good_distances else 0
        
        period_str = "2025" if tf == '1m' else "2020-2025"
        
        print(f"\n{tf.upper()} ({period_str}):")
        print(f"  Distance moyenne bons FVGs: {avg_good_dist:.2f} points")
        print(f"  Profit target conseillé: {avg_good_dist * 0.7:.2f} - {avg_good_dist * 0.85:.2f} points (70-85% de la distance)")
        print(f"  Stop si distance < {avg_good_dist * 0.5:.2f} points après 5 bougies")
    
    print()
    print("="*80)
    print("Note: 0.25 points = 1 tick Nasdaq")
    print("="*80)

if __name__ == '__main__':
    main()

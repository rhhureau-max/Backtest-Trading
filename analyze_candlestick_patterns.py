#!/usr/bin/env python3
"""
Analyse des configurations de chandeliers (Marteau et Étoile Filante) sur NQ
Période: 01/01/2018 à aujourd'hui
Timeframes: 5min, 15min, 1 heure
Plages horaires: 02:00-05:00 et 08:30-11:00
"""

import pandas as pd
import numpy as np
import glob
import os

def load_nq_data():
    """Charge toutes les données NQ 5min à partir des fichiers CSV"""
    # Utilise le répertoire actuel ou celui du script
    base_path = os.path.dirname(os.path.abspath(__file__)) if __file__ else os.getcwd()
    files = glob.glob(os.path.join(base_path, "* 5m.csv"))
    files = sorted([f for f in files if any(str(year) in f for year in range(2018, 2026))])
    
    dfs = []
    for file in files:
        print(f"Chargement: {os.path.basename(file)}")
        # Les colonnes sont séparées par des point-virgules
        # On lit avec header=0 pour utiliser la première ligne comme header
        df = pd.read_csv(file, sep=';', header=0, encoding='utf-8-sig')
        dfs.append(df)
    
    # Concaténer tous les DataFrames
    data = pd.concat(dfs, ignore_index=True)
    
    # Renommer les colonnes (il y a 7 colonnes: Date, Time, Open, High, Low, Close, Volume)
    data.columns = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
    
    # Créer une colonne DateTime
    data['DateTime'] = pd.to_datetime(data['Date'] + ' ' + data['Time'], format='%d/%m/%Y %H:%M:%S')
    
    # Convertir les prix en float
    for col in ['Open', 'High', 'Low', 'Close']:
        data[col] = data[col].astype(float)
    
    # Trier par DateTime
    data = data.sort_values('DateTime').reset_index(drop=True)
    
    # Filtrer à partir du 01/01/2018
    data = data[data['DateTime'] >= '2018-01-01'].reset_index(drop=True)
    
    return data[['DateTime', 'Open', 'High', 'Low', 'Close', 'Volume']]

def resample_to_timeframe(data, timeframe):
    """Rééchantillonne les données vers un timeframe différent"""
    data_copy = data.copy()
    data_copy.set_index('DateTime', inplace=True)
    
    resampled = data_copy.resample(timeframe).agg({
        'Open': 'first',
        'High': 'max',
        'Low': 'min',
        'Close': 'last',
        'Volume': 'sum'
    }).dropna().reset_index()
    
    return resampled

def filter_by_time_ranges(data):
    """
    Filtre les données pour ne garder que les bougies dont l'heure d'ouverture
    est dans les plages 02:00-05:00 ou 08:30-11:00
    """
    data_copy = data.copy()
    data_copy['Hour'] = data_copy['DateTime'].dt.hour
    data_copy['Minute'] = data_copy['DateTime'].dt.minute
    
    # Créer un temps en minutes depuis minuit pour faciliter le filtrage
    data_copy['TimeInMinutes'] = data_copy['Hour'] * 60 + data_copy['Minute']
    
    # Plage 1: 02:00 à 05:00 (120 à 300 minutes)
    # Plage 2: 08:30 à 11:00 (510 à 660 minutes)
    mask = (
        ((data_copy['TimeInMinutes'] >= 120) & (data_copy['TimeInMinutes'] <= 300)) |
        ((data_copy['TimeInMinutes'] >= 510) & (data_copy['TimeInMinutes'] <= 660))
    )
    
    filtered_data = data_copy[mask].copy()
    return filtered_data[['DateTime', 'Open', 'High', 'Low', 'Close', 'Volume']]

def calculate_candlestick_metrics(row):
    """
    Calcule les métriques d'une bougie
    Retourne: (body, upper_wick, lower_wick, total_size)
    """
    body = abs(row['Close'] - row['Open'])
    upper_wick = row['High'] - max(row['Open'], row['Close'])
    lower_wick = min(row['Open'], row['Close']) - row['Low']
    total_size = row['High'] - row['Low']
    return body, upper_wick, lower_wick, total_size

def detect_hammer(row):
    """
    Détecte un marteau (Hammer)
    Conditions:
    - Mèche_Basse > 3 * Corps (au moins 3 fois la taille du corps)
    - Mèche_Haute < 0.1 * Taille_Totale (inexistante ou minuscule)
    """
    body, upper_wick, lower_wick, total_size = calculate_candlestick_metrics(row)
    
    # Éviter la division par zéro
    if total_size == 0:
        return False
    
    is_hammer = (lower_wick > 3 * body) and (upper_wick < 0.1 * total_size)
    return is_hammer

def detect_shooting_star(row):
    """
    Détecte une étoile filante (Shooting Star)
    Conditions:
    - Mèche_Haute > 3 * Corps (au moins 3 fois la taille du corps)
    - Mèche_Basse < 0.1 * Taille_Totale (inexistante ou minuscule)
    """
    body, upper_wick, lower_wick, total_size = calculate_candlestick_metrics(row)
    
    # Éviter la division par zéro
    if total_size == 0:
        return False
    
    is_shooting_star = (upper_wick > 3 * body) and (lower_wick < 0.1 * total_size)
    return is_shooting_star

def count_patterns(data):
    """Compte les marteaux et les étoiles filantes dans les données"""
    hammers = data.apply(detect_hammer, axis=1).sum()
    shooting_stars = data.apply(detect_shooting_star, axis=1).sum()
    return hammers, shooting_stars

def detect_swing_high(data, idx, lookback=5):
    """
    Détecte si l'indice est un swing high (pivot haut)
    Un swing high a un high supérieur aux 'lookback' bougies de chaque côté
    """
    if idx < lookback or idx >= len(data) - lookback:
        return False
    
    current_high = data.loc[idx, 'High']
    
    # Vérifier que le high est supérieur aux bougies avant et après
    for i in range(1, lookback + 1):
        if idx - i >= 0 and data.loc[idx - i, 'High'] >= current_high:
            return False
        if idx + i < len(data) and data.loc[idx + i, 'High'] >= current_high:
            return False
    
    return True

def detect_swing_low(data, idx, lookback=5):
    """
    Détecte si l'indice est un swing low (pivot bas)
    Un swing low a un low inférieur aux 'lookback' bougies de chaque côté
    """
    if idx < lookback or idx >= len(data) - lookback:
        return False
    
    current_low = data.loc[idx, 'Low']
    
    # Vérifier que le low est inférieur aux bougies avant et après
    for i in range(1, lookback + 1):
        if idx - i >= 0 and data.loc[idx - i, 'Low'] <= current_low:
            return False
        if idx + i < len(data) and data.loc[idx + i, 'Low'] <= current_low:
            return False
    
    return True

def detect_liquidity_sweep(data, pattern_idx, is_hammer, lookback_candles=50, sweep_threshold=0.1):
    """
    Détecte si un pattern a effectué un liquidity sweep
    
    Pour Hammer: La mèche basse doit dépasser un swing low précédent
    Pour Shooting Star: La mèche haute doit dépasser un swing high précédent
    
    Args:
        data: DataFrame complet
        pattern_idx: Index du pattern (Hammer ou Shooting Star)
        is_hammer: True si c'est un Hammer, False si c'est une Shooting Star
        lookback_candles: Nombre de bougies à regarder en arrière
        sweep_threshold: Combien de points la mèche doit dépasser le swing
    
    Returns:
        Boolean indiquant si un sweep a été détecté
    """
    if pattern_idx < lookback_candles:
        return False
    
    pattern_row = data.loc[pattern_idx]
    
    if is_hammer:
        # Pour un Hammer, on cherche un swing low que la mèche basse a dépassé
        pattern_low = pattern_row['Low']
        
        # Chercher les swing lows dans le lookback
        for i in range(pattern_idx - lookback_candles, pattern_idx):
            if i < 0:
                continue
            if detect_swing_low(data, i, lookback=5):
                swing_low_value = data.loc[i, 'Low']
                # Vérifier si la mèche du hammer a dépassé ce swing low
                if pattern_low <= swing_low_value - sweep_threshold:
                    return True
    else:
        # Pour une Shooting Star, on cherche un swing high que la mèche haute a dépassé
        pattern_high = pattern_row['High']
        
        # Chercher les swing highs dans le lookback
        for i in range(pattern_idx - lookback_candles, pattern_idx):
            if i < 0:
                continue
            if detect_swing_high(data, i, lookback=5):
                swing_high_value = data.loc[i, 'High']
                # Vérifier si la mèche de la shooting star a dépassé ce swing high
                if pattern_high >= swing_high_value + sweep_threshold:
                    return True
    
    return False

def analyze_pattern_predictive_power(data, time_filtered_indices):
    """
    Analyse le pouvoir prédictif des patterns en vérifiant le prix sur les 3 bougies suivantes.
    
    Args:
        data: DataFrame complet avec toutes les bougies (non filtré par temps)
        time_filtered_indices: Indices des bougies qui passent le filtre horaire
    
    Returns:
        dict avec les statistiques pour hammers et shooting stars
    """
    # Détecter les patterns sans modifier le DataFrame original
    is_hammer = data.apply(detect_hammer, axis=1)
    is_shooting_star = data.apply(detect_shooting_star, axis=1)
    
    # Filtrer pour ne garder que les patterns dans les plages horaires
    hammer_indices = data.index[is_hammer & data.index.isin(time_filtered_indices)].tolist()
    star_indices = data.index[is_shooting_star & data.index.isin(time_filtered_indices)].tolist()
    
    # Analyser les hammers (signal achat)
    hammer_stats = {
        't+1': {'wins': 0, 'total': 0},
        't+2': {'wins': 0, 'total': 0},
        't+3': {'wins': 0, 'total': 0}
    }
    
    for idx in hammer_indices:
        hammer_close = data.loc[idx, 'Close']
        
        # Vérifier t+1, t+2, t+3
        for n in [1, 2, 3]:
            future_idx = idx + n
            if future_idx < len(data):
                future_close = data.loc[future_idx, 'Close']
                hammer_stats[f't+{n}']['total'] += 1
                if future_close > hammer_close:
                    hammer_stats[f't+{n}']['wins'] += 1
    
    # Analyser les étoiles filantes (signal vente)
    star_stats = {
        't+1': {'wins': 0, 'total': 0},
        't+2': {'wins': 0, 'total': 0},
        't+3': {'wins': 0, 'total': 0}
    }
    
    for idx in star_indices:
        star_close = data.loc[idx, 'Close']
        
        # Vérifier t+1, t+2, t+3
        for n in [1, 2, 3]:
            future_idx = idx + n
            if future_idx < len(data):
                future_close = data.loc[future_idx, 'Close']
                star_stats[f't+{n}']['total'] += 1
                if future_close < star_close:
                    star_stats[f't+{n}']['wins'] += 1
    
    # Calculer les win rates
    for stats in [hammer_stats, star_stats]:
        for key in stats:
            if stats[key]['total'] > 0:
                stats[key]['win_rate'] = (stats[key]['wins'] / stats[key]['total']) * 100
            else:
                stats[key]['win_rate'] = 0.0
    
    return {
        'hammers': hammer_stats,
        'shooting_stars': star_stats,
        'hammer_count': len(hammer_indices),
        'star_count': len(star_indices)
    }

def analyze_follow_through(data, time_filtered_indices):
    """
    Analyse la force du mouvement (Follow-through) - capacité à générer une tendance consécutive.
    
    Pour Hammers (Haussier):
    - T+1: Close(t+1) > Close(t)
    - T+2: T+1 validé ET Close(t+2) > Close(t+1) 
    - T+3: T+2 validé ET Close(t+3) > Close(t+2)
    
    Pour Shooting Stars (Baissier):
    - T+1: Close(t+1) < Close(t)
    - T+2: T+1 validé ET Close(t+2) < Close(t+1)
    - T+3: T+2 validé ET Close(t+3) < Close(t+2)
    
    Args:
        data: DataFrame complet avec toutes les bougies (non filtré par temps)
        time_filtered_indices: Indices des bougies qui passent le filtre horaire
    
    Returns:
        dict avec les statistiques de follow-through pour hammers et shooting stars
    """
    # Détecter les patterns sans modifier le DataFrame original
    is_hammer = data.apply(detect_hammer, axis=1)
    is_shooting_star = data.apply(detect_shooting_star, axis=1)
    
    # Filtrer pour ne garder que les patterns dans les plages horaires
    hammer_indices = data.index[is_hammer & data.index.isin(time_filtered_indices)].tolist()
    star_indices = data.index[is_shooting_star & data.index.isin(time_filtered_indices)].tolist()
    
    # Analyser les hammers (signal haussier) - mouvement consécutif
    hammer_followthrough = {
        't+1': {'success': 0, 'total': 0},  # Rebond initial
        't+2': {'success': 0, 'total': 0},  # Confirmation (T+1 validé ET T+2 > T+1)
        't+3': {'success': 0, 'total': 0}   # Tendance forte (T+2 validé ET T+3 > T+2)
    }
    
    for idx in hammer_indices:
        # Vérifier que nous avons 3 bougies futures disponibles
        if idx + 3 >= len(data):
            continue
            
        close_t = data.loc[idx, 'Close']
        close_t1 = data.loc[idx + 1, 'Close']
        close_t2 = data.loc[idx + 2, 'Close']
        close_t3 = data.loc[idx + 3, 'Close']
        
        # T+1: Rebond initial
        hammer_followthrough['t+1']['total'] += 1
        t1_valid = close_t1 > close_t
        if t1_valid:
            hammer_followthrough['t+1']['success'] += 1
        
        # T+2: Confirmation (nécessite T+1 validé ET continuité)
        if t1_valid:
            hammer_followthrough['t+2']['total'] += 1
            t2_valid = close_t2 > close_t1
            if t2_valid:
                hammer_followthrough['t+2']['success'] += 1
                
                # T+3: Tendance forte (nécessite T+2 validé ET continuité)
                hammer_followthrough['t+3']['total'] += 1
                if close_t3 > close_t2:
                    hammer_followthrough['t+3']['success'] += 1
    
    # Analyser les étoiles filantes (signal baissier) - mouvement consécutif
    star_followthrough = {
        't+1': {'success': 0, 'total': 0},  # Rejet initial
        't+2': {'success': 0, 'total': 0},  # Confirmation (T+1 validé ET T+2 < T+1)
        't+3': {'success': 0, 'total': 0}   # Tendance forte (T+2 validé ET T+3 < T+2)
    }
    
    for idx in star_indices:
        # Vérifier que nous avons 3 bougies futures disponibles
        if idx + 3 >= len(data):
            continue
            
        close_t = data.loc[idx, 'Close']
        close_t1 = data.loc[idx + 1, 'Close']
        close_t2 = data.loc[idx + 2, 'Close']
        close_t3 = data.loc[idx + 3, 'Close']
        
        # T+1: Rejet initial
        star_followthrough['t+1']['total'] += 1
        t1_valid = close_t1 < close_t
        if t1_valid:
            star_followthrough['t+1']['success'] += 1
        
        # T+2: Confirmation (nécessite T+1 validé ET continuité)
        if t1_valid:
            star_followthrough['t+2']['total'] += 1
            t2_valid = close_t2 < close_t1
            if t2_valid:
                star_followthrough['t+2']['success'] += 1
                
                # T+3: Tendance forte (nécessite T+2 validé ET continuité)
                star_followthrough['t+3']['total'] += 1
                if close_t3 < close_t2:
                    star_followthrough['t+3']['success'] += 1
    
    # Calculer les pourcentages
    for stats in [hammer_followthrough, star_followthrough]:
        for key in stats:
            if stats[key]['total'] > 0:
                stats[key]['percentage'] = (stats[key]['success'] / stats[key]['total']) * 100
            else:
                stats[key]['percentage'] = 0.0
    
    return {
        'hammers': hammer_followthrough,
        'shooting_stars': star_followthrough,
        'hammer_count': len(hammer_indices),
        'star_count': len(star_indices)
    }

def get_time_filtered_indices(data):
    """
    Retourne les indices des bougies qui passent le filtre horaire
    sans créer une nouvelle dataframe
    """
    hour = data['DateTime'].dt.hour
    minute = data['DateTime'].dt.minute
    time_in_minutes = hour * 60 + minute
    
    # Plage 1: 02:00 à 05:00 (120 à 300 minutes)
    # Plage 2: 08:30 à 11:00 (510 à 660 minutes)
    mask = (
        ((time_in_minutes >= 120) & (time_in_minutes <= 300)) |
        ((time_in_minutes >= 510) & (time_in_minutes <= 660))
    )
    
    return data.index[mask]

def analyze_liquidity_sweep_impact(data, time_filtered_indices, lookback=50):
    """
    Analyse l'impact des liquidity sweeps sur le pouvoir prédictif des patterns.
    
    Compare les win rates des patterns AVEC vs SANS liquidity sweep.
    
    Args:
        data: DataFrame complet avec toutes les bougies
        time_filtered_indices: Indices des bougies qui passent le filtre horaire
        lookback: Nombre de bougies à regarder en arrière pour détecter les swings
    
    Returns:
        dict avec statistiques séparées pour patterns avec et sans sweep
    """
    # Détecter les patterns
    is_hammer = data.apply(detect_hammer, axis=1)
    is_shooting_star = data.apply(detect_shooting_star, axis=1)
    
    # Filtrer pour ne garder que les patterns dans les plages horaires
    hammer_indices = data.index[is_hammer & data.index.isin(time_filtered_indices)].tolist()
    star_indices = data.index[is_shooting_star & data.index.isin(time_filtered_indices)].tolist()
    
    # Séparer les patterns avec et sans liquidity sweep
    hammers_with_sweep = []
    hammers_without_sweep = []
    
    for idx in hammer_indices:
        if detect_liquidity_sweep(data, idx, is_hammer=True, lookback_candles=lookback):
            hammers_with_sweep.append(idx)
        else:
            hammers_without_sweep.append(idx)
    
    stars_with_sweep = []
    stars_without_sweep = []
    
    for idx in star_indices:
        if detect_liquidity_sweep(data, idx, is_hammer=False, lookback_candles=lookback):
            stars_with_sweep.append(idx)
        else:
            stars_without_sweep.append(idx)
    
    # Fonction helper pour calculer win rates
    def calculate_win_rates(indices, is_hammer_pattern):
        stats = {
            't+1': {'wins': 0, 'total': 0},
            't+2': {'wins': 0, 'total': 0},
            't+3': {'wins': 0, 'total': 0}
        }
        
        for idx in indices:
            if idx + 3 >= len(data):
                continue
                
            pattern_close = data.loc[idx, 'Close']
            
            for n in [1, 2, 3]:
                future_idx = idx + n
                if future_idx < len(data):
                    future_close = data.loc[future_idx, 'Close']
                    stats[f't+{n}']['total'] += 1
                    
                    if is_hammer_pattern:
                        if future_close > pattern_close:
                            stats[f't+{n}']['wins'] += 1
                    else:
                        if future_close < pattern_close:
                            stats[f't+{n}']['wins'] += 1
        
        # Calculer les win rates
        for key in stats:
            if stats[key]['total'] > 0:
                stats[key]['win_rate'] = (stats[key]['wins'] / stats[key]['total']) * 100
            else:
                stats[key]['win_rate'] = 0.0
        
        return stats
    
    # Calculer les statistiques
    results = {
        'hammers': {
            'with_sweep': {
                'count': len(hammers_with_sweep),
                'stats': calculate_win_rates(hammers_with_sweep, True)
            },
            'without_sweep': {
                'count': len(hammers_without_sweep),
                'stats': calculate_win_rates(hammers_without_sweep, True)
            }
        },
        'shooting_stars': {
            'with_sweep': {
                'count': len(stars_with_sweep),
                'stats': calculate_win_rates(stars_with_sweep, False)
            },
            'without_sweep': {
                'count': len(stars_without_sweep),
                'stats': calculate_win_rates(stars_without_sweep, False)
            }
        }
    }
    
    return results

def print_pattern_summary(timeframe_name, stats):
    """Affiche un tableau récapitulatif pour un timeframe"""
    print(f"\n{timeframe_name}:")
    print("-" * 80)
    
    # Tableau pour les Marteaux
    print("\nMarteaux (Signal Achat):")
    print("| Horizon | Nombre de Signaux | Signaux Gagnants | Win Rate |")
    print("|---------|-------------------|------------------|----------|")
    for horizon in ['t+1', 't+2', 't+3']:
        total = stats['hammers'][horizon]['total']
        wins = stats['hammers'][horizon]['wins']
        win_rate = stats['hammers'][horizon]['win_rate']
        print(f"| {horizon:7} | {total:17} | {wins:16} | {win_rate:7.2f}% |")
    
    # Tableau pour les Étoiles Filantes
    print("\nÉtoiles Filantes (Signal Vente):")
    print("| Horizon | Nombre de Signaux | Signaux Gagnants | Win Rate |")
    print("|---------|-------------------|------------------|----------|")
    for horizon in ['t+1', 't+2', 't+3']:
        total = stats['shooting_stars'][horizon]['total']
        wins = stats['shooting_stars'][horizon]['wins']
        win_rate = stats['shooting_stars'][horizon]['win_rate']
        print(f"| {horizon:7} | {total:17} | {wins:16} | {win_rate:7.2f}% |")

def print_followthrough_summary(timeframe_name, stats):
    """Affiche un tableau récapitulatif de Follow-through pour un timeframe"""
    print(f"\n{timeframe_name}:")
    print("-" * 100)
    
    # Tableau pour les Marteaux (Haussier)
    print("\nMarteaux (Signal Haussier) - Follow-through:")
    print("| Étape | Description                    | Nb Eligible | Nb Succès | Taux Réussite |")
    print("|-------|--------------------------------|-------------|-----------|---------------|")
    
    descriptions = {
        't+1': 'Rebond initial',
        't+2': 'Confirmation (2 bougies ↑)',
        't+3': 'Tendance forte (3 bougies ↑)'
    }
    
    for horizon in ['t+1', 't+2', 't+3']:
        desc = descriptions[horizon]
        total = stats['hammers'][horizon]['total']
        success = stats['hammers'][horizon]['success']
        percentage = stats['hammers'][horizon]['percentage']
        print(f"| {horizon:5} | {desc:30} | {total:11} | {success:9} | {percentage:12.2f}% |")
    
    # Tableau pour les Étoiles Filantes (Baissier)
    print("\nÉtoiles Filantes (Signal Baissier) - Follow-through:")
    print("| Étape | Description                    | Nb Eligible | Nb Succès | Taux Réussite |")
    print("|-------|--------------------------------|-------------|-----------|---------------|")
    
    descriptions_star = {
        't+1': 'Rejet initial',
        't+2': 'Confirmation (2 bougies ↓)',
        't+3': 'Tendance forte (3 bougies ↓)'
    }
    
    for horizon in ['t+1', 't+2', 't+3']:
        desc = descriptions_star[horizon]
        total = stats['shooting_stars'][horizon]['total']
        success = stats['shooting_stars'][horizon]['success']
        percentage = stats['shooting_stars'][horizon]['percentage']
        print(f"| {horizon:5} | {desc:30} | {total:11} | {success:9} | {percentage:12.2f}% |")

def print_liquidity_sweep_summary(timeframe_name, results):
    """Affiche un tableau comparatif des patterns avec et sans liquidity sweep"""
    print(f"\n{timeframe_name}:")
    print("-" * 100)
    
    # Marteaux
    print("\nMarteaux - Impact du Liquidity Sweep:")
    print("| Type              | Nombre | Win Rate t+1 | Win Rate t+2 | Win Rate t+3 |")
    print("|-------------------|--------|--------------|--------------|--------------|")
    
    with_sweep = results['hammers']['with_sweep']
    without_sweep = results['hammers']['without_sweep']
    
    if with_sweep['count'] > 0:
        wr_t1 = with_sweep['stats']['t+1']['win_rate']
        wr_t2 = with_sweep['stats']['t+2']['win_rate']
        wr_t3 = with_sweep['stats']['t+3']['win_rate']
        print(f"| AVEC Sweep        | {with_sweep['count']:6} | {wr_t1:11.2f}% | {wr_t2:11.2f}% | {wr_t3:11.2f}% |")
    else:
        print(f"| AVEC Sweep        | {with_sweep['count']:6} |         N/A |         N/A |         N/A |")
    
    if without_sweep['count'] > 0:
        wr_t1 = without_sweep['stats']['t+1']['win_rate']
        wr_t2 = without_sweep['stats']['t+2']['win_rate']
        wr_t3 = without_sweep['stats']['t+3']['win_rate']
        print(f"| SANS Sweep        | {without_sweep['count']:6} | {wr_t1:11.2f}% | {wr_t2:11.2f}% | {wr_t3:11.2f}% |")
    else:
        print(f"| SANS Sweep        | {without_sweep['count']:6} |         N/A |         N/A |         N/A |")
    
    # Étoiles Filantes
    print("\nÉtoiles Filantes - Impact du Liquidity Sweep:")
    print("| Type              | Nombre | Win Rate t+1 | Win Rate t+2 | Win Rate t+3 |")
    print("|-------------------|--------|--------------|--------------|--------------|")
    
    with_sweep = results['shooting_stars']['with_sweep']
    without_sweep = results['shooting_stars']['without_sweep']
    
    if with_sweep['count'] > 0:
        wr_t1 = with_sweep['stats']['t+1']['win_rate']
        wr_t2 = with_sweep['stats']['t+2']['win_rate']
        wr_t3 = with_sweep['stats']['t+3']['win_rate']
        print(f"| AVEC Sweep        | {with_sweep['count']:6} | {wr_t1:11.2f}% | {wr_t2:11.2f}% | {wr_t3:11.2f}% |")
    else:
        print(f"| AVEC Sweep        | {with_sweep['count']:6} |         N/A |         N/A |         N/A |")
    
    if without_sweep['count'] > 0:
        wr_t1 = without_sweep['stats']['t+1']['win_rate']
        wr_t2 = without_sweep['stats']['t+2']['win_rate']
        wr_t3 = without_sweep['stats']['t+3']['win_rate']
        print(f"| SANS Sweep        | {without_sweep['count']:6} | {wr_t1:11.2f}% | {wr_t2:11.2f}% | {wr_t3:11.2f}% |")
    else:
        print(f"| SANS Sweep        | {without_sweep['count']:6} |         N/A |         N/A |         N/A |")

def main():
    print("=" * 80)
    print("ANALYSE DES CONFIGURATIONS DE CHANDELIERS - NQ (NASDAQ)")
    print("=" * 80)
    print()
    
    # Charger les données 5min
    print("Chargement des données 5min...")
    data_5m = load_nq_data()
    print(f"Total de bougies 5min chargées: {len(data_5m)}")
    print(f"Période: {data_5m['DateTime'].min()} à {data_5m['DateTime'].max()}")
    print()
    
    # Créer les différents timeframes
    print("Création des timeframes...")
    data_15m = resample_to_timeframe(data_5m, '15min')
    data_1h = resample_to_timeframe(data_5m, '1h')
    print(f"Bougies 15min créées: {len(data_15m)}")
    print(f"Bougies 1H créées: {len(data_1h)}")
    print()
    
    # Obtenir les indices filtrés par plages horaires (SANS créer de nouvelles DataFrames)
    print("Identification des plages horaires (02:00-05:00 et 08:30-11:00)...")
    indices_5m = get_time_filtered_indices(data_5m)
    indices_15m = get_time_filtered_indices(data_15m)
    indices_1h = get_time_filtered_indices(data_1h)
    print(f"Bougies 5min dans les plages horaires: {len(indices_5m)}")
    print(f"Bougies 15min dans les plages horaires: {len(indices_15m)}")
    print(f"Bougies 1H dans les plages horaires: {len(indices_1h)}")
    print()
    
    # Analyse du pouvoir prédictif des patterns
    print("Analyse du pouvoir prédictif des patterns...")
    print("(Calcul sur données complètes pour avoir accès aux bougies futures)")
    print()
    
    stats_5m = analyze_pattern_predictive_power(data_5m, indices_5m)
    stats_15m = analyze_pattern_predictive_power(data_15m, indices_15m)
    stats_1h = analyze_pattern_predictive_power(data_1h, indices_1h)
    
    # Analyse Follow-through (Force du mouvement)
    print("Analyse Follow-through (Force du Mouvement)...")
    print("(Mesure la capacité à générer une tendance consécutive)")
    print()
    
    followthrough_5m = analyze_follow_through(data_5m, indices_5m)
    followthrough_15m = analyze_follow_through(data_15m, indices_15m)
    followthrough_1h = analyze_follow_through(data_1h, indices_1h)
    
    # Analyse Liquidity Sweep (sur 15min uniquement comme demandé)
    print("Analyse Liquidity Sweep (15 minutes)...")
    print("(Impact des sweeps de swing highs/lows avec lookback de 50 bougies)")
    print()
    
    sweep_15m = analyze_liquidity_sweep_impact(data_15m, indices_15m, lookback=50)
    
    # Afficher le résumé des patterns détectés
    print("=" * 80)
    print("NOMBRE DE PATTERNS DÉTECTÉS")
    print("=" * 80)
    print()
    print("| Timeframe | Nombre de Marteaux | Nombre d'Étoiles Filantes |")
    print("|-----------|--------------------|-----------------------------|")
    print(f"| 5 min     | {stats_5m['hammer_count']:18} | {stats_5m['star_count']:27} |")
    print(f"| 15 min    | {stats_15m['hammer_count']:18} | {stats_15m['star_count']:27} |")
    print(f"| 1 Heure   | {stats_1h['hammer_count']:18} | {stats_1h['star_count']:27} |")
    
    # Afficher l'analyse du pouvoir prédictif
    print()
    print("=" * 80)
    print("ANALYSE DU POUVOIR PRÉDICTIF DES PATTERNS")
    print("=" * 80)
    
    print_pattern_summary("Timeframe: 5 minutes", stats_5m)
    print_pattern_summary("Timeframe: 15 minutes", stats_15m)
    print_pattern_summary("Timeframe: 1 Heure", stats_1h)
    
    print()
    print("=" * 80)
    print("Notes:")
    print("- Pour les Marteaux: Signal gagnant si Close(t+n) > Close(marteau)")
    print("- Pour les Étoiles Filantes: Signal gagnant si Close(t+n) < Close(étoile)")
    print("- Les calculs sont effectués AVANT le filtrage horaire pour accéder aux bougies futures")
    print("=" * 80)
    
    # Afficher l'analyse Follow-through
    print()
    print("=" * 100)
    print("ANALYSE FOLLOW-THROUGH - FORCE DU MOUVEMENT (BOUGIES CONSÉCUTIVES)")
    print("=" * 100)
    print()
    print("Cette analyse mesure la capacité des patterns à générer une tendance avec bougies")
    print("consécutives dans la même direction (séquentiel, pas juste comparaison au pattern).")
    print()
    
    print_followthrough_summary("Timeframe: 5 minutes", followthrough_5m)
    print_followthrough_summary("Timeframe: 15 minutes", followthrough_15m)
    print_followthrough_summary("Timeframe: 1 Heure", followthrough_1h)
    
    print()
    print("=" * 100)
    print("Notes Follow-through:")
    print("- T+1: Première bougie va dans le bon sens")
    print("- T+2: T+1 validé ET deuxième bougie continue (2 bougies consécutives)")
    print("- T+3: T+2 validé ET troisième bougie continue (3 bougies consécutives)")
    print("- Le nombre 'Eligible' diminue car on ne compte que les cas où l'étape précédente est validée")
    print("=" * 100)
    
    # Afficher l'analyse Liquidity Sweep
    print()
    print("=" * 100)
    print("ANALYSE LIQUIDITY SWEEP - IMPACT SUR LE WIN RATE (15 MINUTES)")
    print("=" * 100)
    print()
    print("Cette analyse compare les patterns qui ont effectué un liquidity sweep")
    print("(mèche dépasse un swing high/low précédent dans les 50 bougies précédentes)")
    print("versus ceux qui n'ont pas de sweep.")
    print()
    
    print_liquidity_sweep_summary("Timeframe: 15 minutes", sweep_15m)
    
    print()
    print("=" * 100)
    print("Notes Liquidity Sweep:")
    print("- Marteaux: La mèche basse doit dépasser un swing LOW précédent (dans les 50 dernières bougies)")
    print("- Étoiles Filantes: La mèche haute doit dépasser un swing HIGH précédent")
    print("- Swing détection: 5 bougies de chaque côté pour définir un pivot")
    print("- Sweep threshold: La mèche doit dépasser le swing d'au moins 0.1 point")
    print("=" * 100)

if __name__ == "__main__":
    main()

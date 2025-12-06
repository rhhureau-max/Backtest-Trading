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
    - Mèche_Basse > 2 * Corps
    - Mèche_Haute < 0.1 * Taille_Totale
    """
    body, upper_wick, lower_wick, total_size = calculate_candlestick_metrics(row)
    
    # Éviter la division par zéro
    if total_size == 0:
        return False
    
    is_hammer = (lower_wick > 2 * body) and (upper_wick < 0.1 * total_size)
    return is_hammer

def detect_shooting_star(row):
    """
    Détecte une étoile filante (Shooting Star)
    Conditions:
    - Mèche_Haute > 2 * Corps
    - Mèche_Basse < 0.1 * Taille_Totale
    """
    body, upper_wick, lower_wick, total_size = calculate_candlestick_metrics(row)
    
    # Éviter la division par zéro
    if total_size == 0:
        return False
    
    is_shooting_star = (upper_wick > 2 * body) and (lower_wick < 0.1 * total_size)
    return is_shooting_star

def count_patterns(data):
    """Compte les marteaux et les étoiles filantes dans les données"""
    hammers = data.apply(detect_hammer, axis=1).sum()
    shooting_stars = data.apply(detect_shooting_star, axis=1).sum()
    return hammers, shooting_stars

def analyze_pattern_predictive_power(data, time_filtered_indices):
    """
    Analyse le pouvoir prédictif des patterns en vérifiant le prix sur les 3 bougies suivantes.
    
    Args:
        data: DataFrame complet avec toutes les bougies (non filtré par temps)
        time_filtered_indices: Indices des bougies qui passent le filtre horaire
    
    Returns:
        dict avec les statistiques pour hammers et shooting stars
    """
    # Détecter les patterns sur les bougies filtrées
    data['is_hammer'] = data.apply(detect_hammer, axis=1)
    data['is_shooting_star'] = data.apply(detect_shooting_star, axis=1)
    
    # Filtrer pour ne garder que les patterns dans les plages horaires
    hammer_indices = data.index[data['is_hammer'] & data.index.isin(time_filtered_indices)].tolist()
    star_indices = data.index[data['is_shooting_star'] & data.index.isin(time_filtered_indices)].tolist()
    
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
    
    stats_5m = analyze_pattern_predictive_power(data_5m.copy(), indices_5m)
    stats_15m = analyze_pattern_predictive_power(data_15m.copy(), indices_15m)
    stats_1h = analyze_pattern_predictive_power(data_1h.copy(), indices_1h)
    
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

if __name__ == "__main__":
    main()

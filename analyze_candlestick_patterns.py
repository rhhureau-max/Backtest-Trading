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

def main():
    print("=" * 70)
    print("ANALYSE DES CONFIGURATIONS DE CHANDELIERS - NQ (NASDAQ)")
    print("=" * 70)
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
    
    # Filtrer par plages horaires
    print("Filtrage par plages horaires (02:00-05:00 et 08:30-11:00)...")
    filtered_5m = filter_by_time_ranges(data_5m)
    filtered_15m = filter_by_time_ranges(data_15m)
    filtered_1h = filter_by_time_ranges(data_1h)
    print(f"Bougies 5min après filtrage: {len(filtered_5m)}")
    print(f"Bougies 15min après filtrage: {len(filtered_15m)}")
    print(f"Bougies 1H après filtrage: {len(filtered_1h)}")
    print()
    
    # Compter les patterns
    print("Détection des configurations de chandeliers...")
    hammers_5m, stars_5m = count_patterns(filtered_5m)
    hammers_15m, stars_15m = count_patterns(filtered_15m)
    hammers_1h, stars_1h = count_patterns(filtered_1h)
    print()
    
    # Afficher les résultats
    print("=" * 70)
    print("RÉSULTATS DE L'ANALYSE")
    print("=" * 70)
    print()
    print("| Timeframe | Nombre de Marteaux | Nombre d'Étoiles Filantes |")
    print("|-----------|--------------------|-----------------------------|")
    print(f"| 5 min     | {hammers_5m:18} | {stars_5m:27} |")
    print(f"| 15 min    | {hammers_15m:18} | {stars_15m:27} |")
    print(f"| 1 Heure   | {hammers_1h:18} | {stars_1h:27} |")
    print()
    print("=" * 70)

if __name__ == "__main__":
    main()

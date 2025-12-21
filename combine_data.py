#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de consolidation des données NQ 5 minutes
Combine tous les fichiers CSV annuels en un seul fichier consolidé
"""

import pandas as pd
import os
from datetime import datetime

def combine_nq_data():
    """
    Combine tous les fichiers CSV 5 minutes du NQ (2018-2025)
    en un seul fichier consolidé 'NQ_5min.csv'
    """
    # Répertoire de travail
    base_dir = '/home/runner/work/Backtest-Trading/Backtest-Trading'
    
    # Liste des fichiers à charger
    files = [
        '2018 5m.csv',
        '2019 5m.csv',
        '2020 5m.csv',
        '2021 5m.csv',
        '2022 5m.csv',
        '2023 5m.csv',
        '2024 5m.csv',
        '2025 5m.csv'
    ]
    
    print("=== Consolidation des données NQ 5 minutes ===\n")
    
    all_data = []
    
    # Charger et combiner tous les fichiers
    for filename in files:
        filepath = os.path.join(base_dir, filename)
        
        if not os.path.exists(filepath):
            print(f"⚠️  Fichier non trouvé: {filename}")
            continue
        
        print(f"📂 Chargement de {filename}...")
        
        # Charger le CSV avec le séparateur point-virgule
        df = pd.read_csv(
            filepath,
            sep=';',
            encoding='utf-8'
        )
        
        # Renommer les colonnes pour faciliter l'utilisation
        df.columns = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
        
        # Sélectionner uniquement les colonnes nécessaires
        df = df[['Date', 'Time', 'Open', 'High', 'Low', 'Close']]
        
        print(f"   ✓ {len(df)} lignes chargées")
        
        all_data.append(df)
    
    # Combiner tous les DataFrames
    if all_data:
        combined_df = pd.concat(all_data, ignore_index=True)
        
        print(f"\n📊 Total de lignes combinées: {len(combined_df)}")
        
        # Créer une colonne datetime pour faciliter le tri
        combined_df['DateTime'] = pd.to_datetime(
            combined_df['Date'] + ' ' + combined_df['Time'],
            format='%d/%m/%Y %H:%M:%S',
            errors='coerce'
        )
        
        # Supprimer les lignes avec des dates invalides
        invalid_dates = combined_df['DateTime'].isna().sum()
        if invalid_dates > 0:
            print(f"⚠️  {invalid_dates} lignes avec dates invalides supprimées")
            combined_df = combined_df.dropna(subset=['DateTime'])
        
        # Trier par date/heure
        combined_df = combined_df.sort_values('DateTime')
        
        # Supprimer les doublons
        before_dedup = len(combined_df)
        combined_df = combined_df.drop_duplicates(subset=['DateTime'], keep='first')
        duplicates_removed = before_dedup - len(combined_df)
        if duplicates_removed > 0:
            print(f"⚠️  {duplicates_removed} doublons supprimés")
        
        # Supprimer la colonne DateTime temporaire
        combined_df = combined_df.drop('DateTime', axis=1)
        
        # Réinitialiser l'index
        combined_df = combined_df.reset_index(drop=True)
        
        # Sauvegarder le fichier consolidé
        output_file = os.path.join(base_dir, 'NQ_5min.csv')
        combined_df.to_csv(output_file, index=False, encoding='utf-8')
        
        print(f"\n✅ Fichier consolidé créé: NQ_5min.csv")
        print(f"📊 Nombre total de lignes: {len(combined_df)}")
        print(f"📅 Période: {combined_df['Date'].iloc[0]} - {combined_df['Date'].iloc[-1]}")
        print(f"🕒 Première heure: {combined_df['Time'].iloc[0]}")
        print(f"🕒 Dernière heure: {combined_df['Time'].iloc[-1]}")
        
        # Afficher quelques statistiques
        print(f"\n📈 Statistiques des prix:")
        print(f"   Min Close: {combined_df['Close'].min():.2f}")
        print(f"   Max Close: {combined_df['Close'].max():.2f}")
        print(f"   Moyenne Close: {combined_df['Close'].mean():.2f}")
        
        return combined_df
    else:
        print("❌ Aucun fichier n'a pu être chargé!")
        return None

if __name__ == "__main__":
    start_time = datetime.now()
    print(f"Début: {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    result = combine_nq_data()
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    print(f"\n⏱️  Temps d'exécution: {duration:.2f} secondes")
    
    if result is not None:
        print("\n✅ Consolidation terminée avec succès!")
    else:
        print("\n❌ Échec de la consolidation!")

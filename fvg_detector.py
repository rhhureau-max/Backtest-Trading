#!/usr/bin/env python3
"""
Script d'analyse de Fair Value Gaps (FVG) pour le trading du Nasdaq (NQ)
Optimisé pour traiter de gros volumes de données (2018-2025)

Ce script effectue :
1. Génération de données mock 1 minute
2. Resampling en bougies de 3 minutes
3. Détection des FVG haussiers et baissiers
4. Affichage des 5 derniers FVG détectés
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')


def generate_mock_data(num_candles=10000, start_date='2024-01-01 09:30:00', random_seed=42):
    """
    Génère des données mock OHLC 1 minute pour tester le code.
    
    Parameters:
    -----------
    num_candles : int
        Nombre de bougies 1 minute à générer
    start_date : str
        Date et heure de début
    random_seed : int or None
        Seed pour la génération aléatoire (None pour des données non reproductibles)
    
    Returns:
    --------
    pd.DataFrame
        DataFrame avec colonnes Date, Open, High, Low, Close
    """
    print(f"Génération de {num_candles} bougies 1 minute...")
    
    # Créer une série de dates (1 minute d'intervalle)
    start = pd.to_datetime(start_date)
    dates = [start + timedelta(minutes=i) for i in range(num_candles)]
    
    # Prix initial autour de 18000 (typique pour NQ)
    base_price = 18000.0
    
    # Générer des mouvements de prix réalistes
    if random_seed is not None:
        np.random.seed(random_seed)
    
    # Utiliser une marche aléatoire pour le prix de clôture
    returns = np.random.normal(0, 0.0005, num_candles)  # Petits mouvements
    close_prices = base_price * (1 + returns).cumprod()
    
    data = []
    for i in range(num_candles):
        close = close_prices[i]
        
        # Open est le close précédent (ou proche)
        if i == 0:
            open_price = base_price
        else:
            open_price = close_prices[i-1] + np.random.normal(0, 1)
        
        # High et Low autour de l'open et close
        high = max(open_price, close) + abs(np.random.normal(0, 5))
        low = min(open_price, close) - abs(np.random.normal(0, 5))
        
        data.append({
            'Date': dates[i],
            'Open': round(open_price, 2),
            'High': round(high, 2),
            'Low': round(low, 2),
            'Close': round(close, 2)
        })
    
    df = pd.DataFrame(data)
    print(f"✓ Données générées: {len(df)} lignes")
    print(f"  Plage de dates: {df['Date'].min()} à {df['Date'].max()}")
    print(f"  Plage de prix: {df['Low'].min():.2f} à {df['High'].max():.2f}")
    
    return df


def resample_to_3min(df_1min):
    """
    Convertit les données 1 minute en bougies de 3 minutes.
    
    Règles d'agrégation:
    - Open: Premier open de la période
    - High: Maximum des highs
    - Low: Minimum des lows
    - Close: Dernier close de la période
    
    Parameters:
    -----------
    df_1min : pd.DataFrame
        DataFrame avec données 1 minute
    
    Returns:
    --------
    pd.DataFrame
        DataFrame avec données 3 minutes
    """
    print("\nResampling des données 1m vers 3m...")
    
    # Créer une copie pour ne pas modifier l'original
    df = df_1min.copy()
    
    # S'assurer que Date est un datetime et est l'index
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    
    # Resampling avec les règles OHLC appropriées
    df_3min = df.resample('3T').agg({
        'Open': 'first',   # Premier open de la période
        'High': 'max',     # Maximum des highs
        'Low': 'min',      # Minimum des lows
        'Close': 'last'    # Dernier close de la période
    })
    
    # Supprimer les lignes avec NaN (début/fin incomplets)
    df_3min.dropna(inplace=True)
    
    # Réinitialiser l'index pour avoir Date comme colonne
    df_3min.reset_index(inplace=True)
    
    print(f"✓ Resampling terminé: {len(df_3min)} bougies 3m")
    print(f"  Ratio de compression: {len(df_1min)} → {len(df_3min)} (facteur {len(df_1min)/len(df_3min):.2f})")
    
    return df_3min


def detect_fvg(df_3min):
    """
    Détecte les Fair Value Gaps (FVG) sur les données 3 minutes.
    
    Logique de détection:
    - FVG Haussier (Bullish): Low[i] > High[i-2]
    - FVG Baissier (Bearish): High[i] < Low[i-2]
    
    Parameters:
    -----------
    df_3min : pd.DataFrame
        DataFrame avec données 3 minutes
    
    Returns:
    --------
    pd.DataFrame
        DataFrame avec colonne is_FVG ajoutée et informations sur les FVG
    """
    print("\nDétection des Fair Value Gaps (FVG)...")
    
    # Créer une copie pour ne pas modifier l'original
    df = df_3min.copy()
    
    # Initialiser les colonnes pour les FVG
    df['is_FVG'] = None
    df['FVG_Type'] = None
    df['FVG_Top'] = None
    df['FVG_Bottom'] = None
    
    # Optimisation: utiliser shift pour accéder à i-2 sans boucle
    # Cela est beaucoup plus rapide sur de gros datasets
    df['High_i_minus_2'] = df['High'].shift(2)
    df['Low_i_minus_2'] = df['Low'].shift(2)
    
    # Détection des FVG Haussiers (Bullish)
    # Condition: Low[i] > High[i-2]
    bullish_fvg = df['Low'] > df['High_i_minus_2']
    
    # Détection des FVG Baissiers (Bearish)
    # Condition: High[i] < Low[i-2]
    bearish_fvg = df['High'] < df['Low_i_minus_2']
    
    # Marquer les FVG
    df.loc[bullish_fvg, 'is_FVG'] = True
    df.loc[bullish_fvg, 'FVG_Type'] = 'Bullish'
    df.loc[bullish_fvg, 'FVG_Top'] = df.loc[bullish_fvg, 'Low']
    df.loc[bullish_fvg, 'FVG_Bottom'] = df.loc[bullish_fvg, 'High_i_minus_2']
    
    df.loc[bearish_fvg, 'is_FVG'] = True
    df.loc[bearish_fvg, 'FVG_Type'] = 'Bearish'
    df.loc[bearish_fvg, 'FVG_Top'] = df.loc[bearish_fvg, 'Low_i_minus_2']
    df.loc[bearish_fvg, 'FVG_Bottom'] = df.loc[bearish_fvg, 'High']
    
    # Supprimer les colonnes temporaires
    df.drop(['High_i_minus_2', 'Low_i_minus_2'], axis=1, inplace=True)
    
    # Compter les FVG détectés
    total_fvg = df['is_FVG'].sum()
    bullish_count = (df['FVG_Type'] == 'Bullish').sum()
    bearish_count = (df['FVG_Type'] == 'Bearish').sum()
    
    print(f"✓ Détection terminée:")
    print(f"  Total FVG: {total_fvg}")
    print(f"  FVG Haussiers (Bullish): {bullish_count}")
    print(f"  FVG Baissiers (Bearish): {bearish_count}")
    
    return df


def display_last_fvgs(df, n=5):
    """
    Affiche les n derniers FVG détectés avec leurs informations.
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame avec détection FVG
    n : int
        Nombre de FVG à afficher (par défaut 5)
    """
    print(f"\n{'='*80}")
    print(f"DERNIERS {n} FVG DÉTECTÉS")
    print(f"{'='*80}\n")
    
    # Filtrer les FVG
    fvg_df = df[df['is_FVG'] == True].copy()
    
    if len(fvg_df) == 0:
        print("Aucun FVG détecté dans les données.")
        return
    
    # Prendre les n derniers
    last_fvgs = fvg_df.tail(n)
    
    # Afficher chaque FVG
    for idx, row in last_fvgs.iterrows():
        fvg_type = row['FVG_Type']
        date = row['Date']
        top = row['FVG_Top']
        bottom = row['FVG_Bottom']
        gap_size = abs(top - bottom)
        
        print(f"FVG #{idx + 1}")
        print(f"  Type: {fvg_type}")
        print(f"  Date: {date}")
        print(f"  Top: {top:.2f}")
        print(f"  Bottom: {bottom:.2f}")
        print(f"  Gap Size: {gap_size:.2f} points")
        print(f"  OHLC: O={row['Open']:.2f} H={row['High']:.2f} L={row['Low']:.2f} C={row['Close']:.2f}")
        print("-" * 80)
    
    print(f"\nRésumé:")
    print(f"  Total FVG affichés: {len(last_fvgs)}")
    print(f"  Taille moyenne du gap: {(last_fvgs['FVG_Top'] - last_fvgs['FVG_Bottom']).abs().mean():.2f} points")


def load_real_data(filepath, delimiter=';'):
    """
    Charge des données réelles depuis un fichier CSV.
    
    Parameters:
    -----------
    filepath : str
        Chemin vers le fichier CSV
    delimiter : str
        Délimiteur du CSV (par défaut ';')
    
    Returns:
    --------
    pd.DataFrame
        DataFrame avec colonnes Date, Open, High, Low, Close
    
    Raises:
    -------
    FileNotFoundError
        Si le fichier n'existe pas
    ValueError
        Si le format du fichier n'est pas valide
    """
    print(f"Chargement des données depuis {filepath}...")
    
    try:
        # Charger le CSV
        df = pd.read_csv(filepath, delimiter=delimiter, encoding='utf-8-sig')
    except FileNotFoundError:
        raise FileNotFoundError(f"Le fichier '{filepath}' n'a pas été trouvé. Vérifiez le chemin.")
    except PermissionError:
        raise PermissionError(f"Permissions insuffisantes pour lire le fichier '{filepath}'.")
    except Exception as e:
        raise ValueError(f"Erreur lors de la lecture du fichier '{filepath}': {str(e)}")
    
    # Identifier les colonnes (adapter selon le format du fichier)
    # Format attendu: Date;Time;Open;High;Low;Close;Volume
    try:
        if len(df.columns) >= 7:
            df.columns = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
            
            # Combiner Date et Time avec format flexible
            try:
                df['Date'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%d/%m/%Y %H:%M:%S')
            except:
                # Essayer avec infer_datetime_format si le format par défaut échoue
                df['Date'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], infer_datetime_format=True)
            
            df = df[['Date', 'Open', 'High', 'Low', 'Close']]
        else:
            # Format simplifié
            df.columns = ['Date', 'Open', 'High', 'Low', 'Close']
            df['Date'] = pd.to_datetime(df['Date'], infer_datetime_format=True)
        
        # Trier par date
        df.sort_values('Date', inplace=True)
        df.reset_index(drop=True, inplace=True)
        
        print(f"✓ Données chargées: {len(df)} lignes")
        print(f"  Plage de dates: {df['Date'].min()} à {df['Date'].max()}")
        
        return df
        
    except Exception as e:
        raise ValueError(f"Format de données invalide dans '{filepath}': {str(e)}")


def main():
    """
    Fonction principale pour exécuter l'analyse FVG.
    """
    print("="*80)
    print("ANALYSE DES FAIR VALUE GAPS (FVG) - NASDAQ (NQ)")
    print("="*80)
    print()
    
    # Option 1: Utiliser des données mock pour tester
    print("Mode: Génération de données mock")
    df_1min = generate_mock_data(num_candles=10000)
    
    # Option 2: Décommenter pour charger des données réelles
    # print("Mode: Chargement de données réelles")
    # df_1min = load_real_data('2025 1m.csv')
    
    # Resampling vers 3 minutes
    df_3min = resample_to_3min(df_1min)
    
    # Détection des FVG
    df_result = detect_fvg(df_3min)
    
    # Affichage des derniers FVG
    display_last_fvgs(df_result, n=5)
    
    # Sauvegarder les résultats (optionnel)
    output_file = 'fvg_results_3min.csv'
    df_result.to_csv(output_file, index=False)
    print(f"\n✓ Résultats sauvegardés dans: {output_file}")
    
    # Statistiques finales
    print(f"\n{'='*80}")
    print("STATISTIQUES FINALES")
    print(f"{'='*80}")
    print(f"Bougies 1m traitées: {len(df_1min):,}")
    print(f"Bougies 3m générées: {len(df_3min):,}")
    print(f"FVG détectés: {df_result['is_FVG'].sum()}")
    print(f"Taux de FVG: {(df_result['is_FVG'].sum() / len(df_3min) * 100):.2f}%")
    print("="*80)


if __name__ == "__main__":
    main()

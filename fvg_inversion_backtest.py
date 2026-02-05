"""
Backtest de la stratégie FVG Inversion sur NQ (Nasdaq) - Données 1 minute
Auteur: Trading Strategy Backtest
Date: 2025
"""

import pandas as pd
import numpy as np
import zipfile
import os
from datetime import datetime, time
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# SECTION 1: CHARGEMENT ET PRÉPARATION DES DONNÉES
# ============================================================================

def load_data_files(base_path):
    """
    Charge tous les fichiers de données 1 minute (2018-2025)
    Extrait les fichiers zip si nécessaire et combine toutes les données
    """
    print("Chargement des données...")
    
    all_data = []
    years = ['2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025']
    
    for year in years:
        filename = f"{year} 1m.csv"
        zip_filename = f"{year} 1m.csv.zip"
        
        filepath = os.path.join(base_path, filename)
        zippath = os.path.join(base_path, zip_filename)
        
        try:
            # Si le fichier CSV existe directement
            if os.path.exists(filepath):
                print(f"  Chargement de {filename}...")
                df = pd.read_csv(filepath, sep=';', skiprows=1, 
                               names=['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume'])
                all_data.append(df)
            
            # Si le fichier est compressé
            elif os.path.exists(zippath):
                print(f"  Extraction et chargement de {zip_filename}...")
                with zipfile.ZipFile(zippath, 'r') as zip_ref:
                    # Lire directement depuis le zip
                    with zip_ref.open(filename) as file:
                        df = pd.read_csv(file, sep=';', skiprows=1,
                                       names=['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume'])
                        all_data.append(df)
            else:
                print(f"  Attention: {filename} non trouvé")
                
        except Exception as e:
            print(f"  Erreur lors du chargement de {filename}: {e}")
    
    if not all_data:
        raise Exception("Aucune donnée n'a pu être chargée!")
    
    # Combiner toutes les données
    print("Combinaison des données...")
    data = pd.concat(all_data, ignore_index=True)
    
    return data


def prepare_dataframe(data):
    """
    Prépare le dataframe: conversion des types, création de la colonne datetime, tri
    """
    print("Préparation du dataframe...")
    
    # Conversion du format date DD/MM/YYYY vers datetime
    data['DateTime'] = pd.to_datetime(data['Date'] + ' ' + data['Time'], 
                                     format='%d/%m/%Y %H:%M:%S')
    
    # Tri par date
    data = data.sort_values('DateTime').reset_index(drop=True)
    
    # Conversion des colonnes OHLC en float
    data['Open'] = data['Open'].astype(float)
    data['High'] = data['High'].astype(float)
    data['Low'] = data['Low'].astype(float)
    data['Close'] = data['Close'].astype(float)
    
    # Ajout d'une colonne Date simple pour regroupement
    data['DateOnly'] = data['DateTime'].dt.date
    
    # Ajout d'une colonne Time simple
    data['TimeOnly'] = data['DateTime'].dt.time
    
    print(f"  Total de lignes: {len(data):,}")
    print(f"  Période: {data['DateTime'].min()} à {data['DateTime'].max()}")
    
    return data


# ============================================================================
# SECTION 2: DÉTECTION DES FVG (FAIR VALUE GAPS)
# ============================================================================

def detect_fvg(df, start_idx=0):
    """
    Détecte le premier FVG à partir d'un index donné
    
    Règles:
    - Bearish FVG: Low[i-2] > High[i] → niveau clé = Low[i-2] (haut du gap)
    - Bullish FVG: High[i-2] < Low[i] → niveau clé = High[i-2] (bas du gap)
    
    Returns:
        tuple: (type_fvg, key_level, index) ou (None, None, None) si aucun FVG trouvé
    """
    # On commence à i=2 pour avoir accès à i-2
    for i in range(max(2, start_idx), len(df)):
        # Bearish FVG
        if df.loc[i-2, 'Low'] > df.loc[i, 'High']:
            return ('bearish', df.loc[i-2, 'Low'], i)
        
        # Bullish FVG
        if df.loc[i-2, 'High'] < df.loc[i, 'Low']:
            return ('bullish', df.loc[i-2, 'High'], i)
    
    return (None, None, None)


# ============================================================================
# SECTION 3: DÉTECTION DU SIGNAL D'INVERSION
# ============================================================================

def detect_inversion_signal(df, fvg_type, key_level, start_idx, end_time):
    """
    Détecte le signal d'inversion d'un FVG
    
    Règles:
    - Pour Bearish FVG: Attendre qu'une bougie CLOSE au-dessus de Low[i-2] → Signal LONG
    - Pour Bullish FVG: Attendre qu'une bougie CLOSE en-dessous de High[i-2] → Signal SHORT
    
    Returns:
        tuple: (signal_type, signal_idx) ou (None, None) si aucun signal
    """
    for i in range(start_idx, len(df)):
        # Vérifier qu'on est avant 11:00
        if df.loc[i, 'TimeOnly'] >= end_time:
            return (None, None)
        
        # Bearish FVG → Signal LONG si close au-dessus du niveau clé
        if fvg_type == 'bearish' and df.loc[i, 'Close'] > key_level:
            return ('LONG', i)
        
        # Bullish FVG → Signal SHORT si close en-dessous du niveau clé
        if fvg_type == 'bullish' and df.loc[i, 'Close'] < key_level:
            return ('SHORT', i)
    
    return (None, None)


# ============================================================================
# SECTION 4: EXÉCUTION DU TRADE
# ============================================================================

def execute_trade(df, signal_type, signal_idx):
    """
    Exécute un trade basé sur le signal
    
    Paramètres:
    - Entry: Open de la bougie suivante (ou Close de la bougie signal)
    - Stop Loss: 100 ticks = 25 points (1 tick = 0.25 sur NQ)
    - Take Profit: 100 ticks = 25 points
    
    Returns:
        dict: Informations sur le trade (résultat, prix, etc.)
    """
    # Si on est à la dernière bougie, on ne peut pas trader
    if signal_idx >= len(df) - 1:
        return None
    
    # Prix d'entrée: Open de la bougie suivante
    entry_price = df.loc[signal_idx + 1, 'Open']
    entry_time = df.loc[signal_idx + 1, 'DateTime']
    
    # Définir SL et TP
    if signal_type == 'LONG':
        stop_loss = entry_price - 25
        take_profit = entry_price + 25
    else:  # SHORT
        stop_loss = entry_price + 25
        take_profit = entry_price - 25
    
    # Chercher le résultat du trade
    for i in range(signal_idx + 1, len(df)):
        current_high = df.loc[i, 'High']
        current_low = df.loc[i, 'Low']
        current_time = df.loc[i, 'DateTime']
        
        if signal_type == 'LONG':
            # Vérifier si TP touché
            if current_high >= take_profit:
                return {
                    'type': 'LONG',
                    'entry_price': entry_price,
                    'entry_time': entry_time,
                    'exit_price': take_profit,
                    'exit_time': current_time,
                    'result': 'WIN',
                    'pnl': 25,
                    'stop_loss': stop_loss,
                    'take_profit': take_profit
                }
            # Vérifier si SL touché
            if current_low <= stop_loss:
                return {
                    'type': 'LONG',
                    'entry_price': entry_price,
                    'entry_time': entry_time,
                    'exit_price': stop_loss,
                    'exit_time': current_time,
                    'result': 'LOSS',
                    'pnl': -25,
                    'stop_loss': stop_loss,
                    'take_profit': take_profit
                }
        else:  # SHORT
            # Vérifier si TP touché
            if current_low <= take_profit:
                return {
                    'type': 'SHORT',
                    'entry_price': entry_price,
                    'entry_time': entry_time,
                    'exit_price': take_profit,
                    'exit_time': current_time,
                    'result': 'WIN',
                    'pnl': 25,
                    'stop_loss': stop_loss,
                    'take_profit': take_profit
                }
            # Vérifier si SL touché
            if current_high >= stop_loss:
                return {
                    'type': 'SHORT',
                    'entry_price': entry_price,
                    'entry_time': entry_time,
                    'exit_price': stop_loss,
                    'exit_time': current_time,
                    'result': 'LOSS',
                    'pnl': -25,
                    'stop_loss': stop_loss,
                    'take_profit': take_profit
                }
    
    # Si on arrive ici, le trade n'a pas touché ni TP ni SL (fin des données)
    return None


# ============================================================================
# SECTION 5: BACKTEST PRINCIPAL
# ============================================================================

def run_backtest(data):
    """
    Exécute le backtest complet sur toutes les données
    """
    print("\nDémarrage du backtest...")
    print("=" * 80)
    
    # Fenêtre de trading
    start_time = time(8, 30)  # 08:30
    end_time = time(11, 0)    # 11:00
    
    # Regrouper par jour
    grouped = data.groupby('DateOnly')
    
    trades = []
    days_processed = 0
    days_with_fvg = 0
    days_with_signal = 0
    
    for date, day_df in grouped:
        days_processed += 1
        
        # Réinitialiser l'index pour ce jour
        day_df = day_df.reset_index(drop=True)
        
        # Filtrer pour la fenêtre de trading (08:30 - 11:00)
        trading_window = day_df[
            (day_df['TimeOnly'] >= start_time) & 
            (day_df['TimeOnly'] <= end_time)
        ].copy()
        
        if len(trading_window) < 3:
            # Pas assez de données pour ce jour
            continue
        
        # Réinitialiser l'index de la fenêtre de trading
        trading_window = trading_window.reset_index(drop=True)
        
        # Étape 1: Détecter le premier FVG après 08:30
        fvg_type, key_level, fvg_idx = detect_fvg(trading_window, start_idx=0)
        
        if fvg_type is None:
            # Pas de FVG ce jour
            continue
        
        days_with_fvg += 1
        
        # Étape 2: Détecter le signal d'inversion
        signal_type, signal_idx = detect_inversion_signal(
            trading_window, fvg_type, key_level, fvg_idx + 1, end_time
        )
        
        if signal_type is None:
            # Pas de signal d'inversion avant 11:00
            continue
        
        days_with_signal += 1
        
        # Étape 3: Exécuter le trade
        trade = execute_trade(trading_window, signal_type, signal_idx)
        
        if trade is not None:
            trade['date'] = date
            trades.append(trade)
    
    print(f"\nJours analysés: {days_processed}")
    print(f"Jours avec FVG détecté: {days_with_fvg}")
    print(f"Jours avec signal d'inversion: {days_with_signal}")
    print(f"Trades exécutés: {len(trades)}")
    print("=" * 80)
    
    return trades


# ============================================================================
# SECTION 6: CALCUL DES MÉTRIQUES DE PERFORMANCE
# ============================================================================

def calculate_metrics(trades):
    """
    Calcule toutes les métriques de performance du backtest
    """
    if not trades:
        print("\nAucun trade à analyser!")
        return
    
    # Conversion en DataFrame pour faciliter l'analyse
    df_trades = pd.DataFrame(trades)
    
    # Métriques de base
    total_trades = len(df_trades)
    winning_trades = len(df_trades[df_trades['result'] == 'WIN'])
    losing_trades = len(df_trades[df_trades['result'] == 'LOSS'])
    
    # Winrate
    winrate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
    
    # P&L
    gross_profit = df_trades[df_trades['pnl'] > 0]['pnl'].sum()
    gross_loss = abs(df_trades[df_trades['pnl'] < 0]['pnl'].sum())
    net_profit = df_trades['pnl'].sum()
    
    # Profit Factor
    profit_factor = (gross_profit / gross_loss) if gross_loss > 0 else float('inf')
    
    # Maximum Drawdown
    cumulative_pnl = df_trades['pnl'].cumsum()
    running_max = cumulative_pnl.cummax()
    drawdown = running_max - cumulative_pnl
    max_drawdown = drawdown.max()
    
    # Répartition LONG/SHORT
    long_trades = len(df_trades[df_trades['type'] == 'LONG'])
    short_trades = len(df_trades[df_trades['type'] == 'SHORT'])
    
    long_wins = len(df_trades[(df_trades['type'] == 'LONG') & (df_trades['result'] == 'WIN')])
    short_wins = len(df_trades[(df_trades['type'] == 'SHORT') & (df_trades['result'] == 'WIN')])
    
    # Affichage des résultats
    print("\n" + "=" * 80)
    print("RÉSULTATS DU BACKTEST - STRATÉGIE FVG INVERSION")
    print("=" * 80)
    
    print(f"\n📊 STATISTIQUES GÉNÉRALES:")
    print(f"  • Total de trades: {total_trades}")
    print(f"  • Trades gagnants: {winning_trades}")
    print(f"  • Trades perdants: {losing_trades}")
    print(f"  • Winrate: {winrate:.2f}%")
    
    print(f"\n💰 PERFORMANCE FINANCIÈRE:")
    print(f"  • Profit brut: ${gross_profit:,.2f}")
    print(f"  • Perte brute: ${gross_loss:,.2f}")
    print(f"  • Profit net: ${net_profit:,.2f}")
    print(f"  • Profit Factor: {profit_factor:.2f}")
    print(f"  • Maximum Drawdown: ${max_drawdown:,.2f}")
    
    print(f"\n📈 RÉPARTITION DES TRADES:")
    print(f"  • Trades LONG: {long_trades} (Gagnants: {long_wins}, WR: {(long_wins/long_trades*100) if long_trades > 0 else 0:.2f}%)")
    print(f"  • Trades SHORT: {short_trades} (Gagnants: {short_wins}, WR: {(short_wins/short_trades*100) if short_trades > 0 else 0:.2f}%)")
    
    print("\n" + "=" * 80)
    
    # Statistiques additionnelles
    print(f"\n📅 ANALYSE TEMPORELLE:")
    print(f"  • Première trade: {df_trades['entry_time'].min()}")
    print(f"  • Dernière trade: {df_trades['entry_time'].max()}")
    
    # Performance mensuelle
    df_trades['month'] = pd.to_datetime(df_trades['entry_time']).dt.to_period('M')
    monthly_pnl = df_trades.groupby('month')['pnl'].sum()
    
    print(f"\n📆 MEILLEURS ET PIRES MOIS:")
    print(f"  • Meilleur mois: {monthly_pnl.idxmax()} avec ${monthly_pnl.max():,.2f}")
    print(f"  • Pire mois: {monthly_pnl.idxmin()} avec ${monthly_pnl.min():,.2f}")
    
    print("\n" + "=" * 80)
    
    return {
        'total_trades': total_trades,
        'winning_trades': winning_trades,
        'losing_trades': losing_trades,
        'winrate': winrate,
        'gross_profit': gross_profit,
        'gross_loss': gross_loss,
        'net_profit': net_profit,
        'profit_factor': profit_factor,
        'max_drawdown': max_drawdown,
        'trades_df': df_trades
    }


# ============================================================================
# SECTION 7: FONCTION PRINCIPALE
# ============================================================================

def main():
    """
    Fonction principale qui orchestre tout le backtest
    """
    print("\n" + "=" * 80)
    print("BACKTEST FVG INVERSION - NQ 1 MINUTE")
    print("=" * 80)
    
    # Chemin vers les données
    base_path = "/home/runner/work/Backtest-Trading/Backtest-Trading"
    
    try:
        # 1. Charger les données
        data = load_data_files(base_path)
        
        # 2. Préparer le dataframe
        data = prepare_dataframe(data)
        
        # 3. Exécuter le backtest
        trades = run_backtest(data)
        
        # 4. Calculer et afficher les métriques
        if trades:
            metrics = calculate_metrics(trades)
            
            # Sauvegarder les trades dans un CSV
            trades_df = pd.DataFrame(trades)
            output_file = os.path.join(base_path, "fvg_inversion_trades.csv")
            trades_df.to_csv(output_file, index=False)
            print(f"\n✅ Trades sauvegardés dans: {output_file}")
        else:
            print("\n⚠️  Aucun trade n'a été généré par le backtest.")
        
        print("\n✅ Backtest terminé avec succès!")
        
    except Exception as e:
        print(f"\n❌ Erreur lors du backtest: {e}")
        import traceback
        traceback.print_exc()


# ============================================================================
# EXÉCUTION
# ============================================================================

if __name__ == "__main__":
    main()

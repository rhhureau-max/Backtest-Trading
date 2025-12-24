#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Backtest de la stratégie "Judas Swing & Inversion" sur le Nasdaq 100 (NQ)
Timeframe: 5 minutes
Période: 2018-2025
Timezone: Chicago (UTC-5) - Pas de conversion de timezone
"""

import pandas as pd
import numpy as np
from datetime import datetime, time
import glob
import os

# Configuration
BASE_DIR = "/home/runner/work/Backtest-Trading/Backtest-Trading/"
CSV_PATTERN = "20[0-9][0-9] 5m.csv"  # Pattern pour matcher uniquement les fichiers 5m (ex: 2018 5m.csv)

# Horaires des sessions (Heure de Chicago)
ASIA_START = time(18, 0)  # 18:00 Chicago
ASIA_END = time(23, 0)    # 23:00 Chicago
LONDON_START = time(1, 0) # 01:00 Chicago
LONDON_END = time(4, 0)   # 04:00 Chicago
EXIT_TIME = time(11, 0)   # 11:00 Chicago - Sortie forcée


def load_data():
    """
    Charge tous les fichiers CSV 5m et les fusionne en un seul DataFrame.
    """
    print("=" * 80)
    print("CHARGEMENT DES DONNÉES")
    print("=" * 80)
    
    csv_files = sorted(glob.glob(os.path.join(BASE_DIR, CSV_PATTERN)))
    print(f"\nFichiers trouvés: {len(csv_files)}")
    for f in csv_files:
        print(f"  - {os.path.basename(f)}")
    
    all_data = []
    
    for file_path in csv_files:
        try:
            # Lecture du CSV avec point-virgule comme séparateur
            df = pd.read_csv(file_path, sep=';')
            
            # Nettoyage des noms de colonnes
            df.columns = df.columns.str.strip()
            
            # Renommer les colonnes pour faciliter la manipulation
            df.rename(columns={
                'Column1': 'Date',
                'Column2': 'Time',
                'Column3': 'Open',
                'Column4': 'High',
                'Column5': 'Low',
                'Column6': 'Close',
                'Column7': 'Volume'
            }, inplace=True)
            
            # Création de la colonne DateTime
            df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], 
                                           format='%d/%m/%Y %H:%M:%S')
            
            # Conversion des colonnes de prix en float
            for col in ['Open', 'High', 'Low', 'Close']:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            
            all_data.append(df)
            print(f"  ✓ {os.path.basename(file_path)}: {len(df)} lignes")
            
        except Exception as e:
            print(f"  ✗ Erreur lors du chargement de {os.path.basename(file_path)}: {e}")
    
    # Fusion de toutes les données
    full_data = pd.concat(all_data, ignore_index=True)
    full_data = full_data.sort_values('DateTime').reset_index(drop=True)
    
    # Suppression des doublons
    full_data = full_data.drop_duplicates(subset=['DateTime'], keep='first')
    
    # Suppression des lignes avec des valeurs nulles
    full_data = full_data.dropna(subset=['Open', 'High', 'Low', 'Close'])
    
    print(f"\n✓ Données totales chargées: {len(full_data)} lignes")
    print(f"  Période: {full_data['DateTime'].min()} à {full_data['DateTime'].max()}")
    
    return full_data


def calculate_asia_session_levels(df):
    """
    Calcule les niveaux de la session Asia pour chaque jour:
    - Asia_High: Plus haut de 18:00 à 23:00
    - Asia_Low: Plus bas de 18:00 à 23:00
    - Asia_EQ: Equilibrium (moyenne High/Low)
    """
    print("\n" + "=" * 80)
    print("CALCUL DES NIVEAUX ASIA SESSION")
    print("=" * 80)
    
    df['Date_Only'] = df['DateTime'].dt.date
    df['Time_Only'] = df['DateTime'].dt.time
    
    # Identifier les bougies de la session Asia
    # Note: La session Asia peut commencer un jour et finir le lendemain
    # On va traiter jour par jour en considérant que l'Asia commence à 18h et va jusqu'à 23h
    
    asia_levels = {}
    
    for date in df['Date_Only'].unique():
        # Pour chaque date, on cherche les bougies entre 18:00 et 23:00
        mask_asia = (df['Date_Only'] == date) & \
                    (df['Time_Only'] >= ASIA_START) & \
                    (df['Time_Only'] <= ASIA_END)
        
        asia_data = df[mask_asia]
        
        if len(asia_data) > 0:
            asia_high = asia_data['High'].max()
            asia_low = asia_data['Low'].min()
            asia_eq = (asia_high + asia_low) / 2
            
            asia_levels[date] = {
                'Asia_High': asia_high,
                'Asia_Low': asia_low,
                'Asia_EQ': asia_eq
            }
    
    print(f"\n✓ Niveaux calculés pour {len(asia_levels)} jours")
    
    return asia_levels


def detect_fvg_bearish(df, start_idx, end_idx):
    """
    Détecte les Fair Value Gaps (FVG) baissiers entre start_idx et end_idx.
    Un FVG baissier se forme quand:
    - Le Low de la bougie N-1 est supérieur au High de la bougie N+1
    - Cela crée un gap (espace non comblé) pendant un mouvement baissier
    
    Retourne une liste de dictionnaires avec les informations des FVG trouvés.
    """
    fvg_list = []
    
    # On commence à l'index start_idx + 1 et on finit à end_idx - 1
    # pour avoir accès aux bougies N-1 et N+1
    for i in range(start_idx + 1, end_idx):
        if i < 1 or i >= len(df) - 1:
            continue
        
        # Bougie N-1 (précédente)
        low_prev = df.iloc[i - 1]['Low']
        
        # Bougie N (actuelle)
        # On peut aussi regarder le high/low de la bougie N pour plus de contexte
        
        # Bougie N+1 (suivante)
        high_next = df.iloc[i + 1]['High']
        
        # Vérification du FVG baissier: gap entre Low(N-1) et High(N+1)
        if low_prev > high_next:
            fvg = {
                'idx': i,
                'datetime': df.iloc[i]['DateTime'],
                'fvg_high': low_prev,  # Bord haut du FVG
                'fvg_low': high_next,  # Bord bas du FVG
            }
            fvg_list.append(fvg)
    
    return fvg_list


def find_signal_candle(df, fvg, start_idx, end_idx):
    """
    Cherche une bougie qui clôture au-dessus du bord haut du FVG (fvg_high).
    Retourne l'index de la première bougie qui remplit cette condition, ou None.
    """
    fvg_high = fvg['fvg_high']
    fvg_idx = fvg['idx']
    
    # On cherche après la formation du FVG (fvg_idx + 2, car le FVG se forme sur N+1)
    for i in range(fvg_idx + 2, end_idx + 1):
        if i >= len(df):
            break
        
        close = df.iloc[i]['Close']
        
        # Signal: la bougie clôture strictement au-dessus du bord haut du FVG
        if close > fvg_high:
            return i
    
    return None


def backtest_strategy(df, asia_levels):
    """
    Backtest de la stratégie Judas Swing & Inversion.
    
    Pour chaque jour:
    1. Vérifie s'il y a un sweep sous Asia_Low pendant la session London (01:00-04:00)
    2. Détecte les FVG baissiers formés pendant/avant le sweep
    3. Cherche un signal (clôture au-dessus du FVG)
    4. Entre en position et gère le trade (SL, TP, sortie temporelle)
    """
    print("\n" + "=" * 80)
    print("BACKTEST DE LA STRATÉGIE")
    print("=" * 80)
    
    trades = []
    
    # Pour chaque jour où on a des niveaux Asia
    for date, levels in asia_levels.items():
        asia_low = levels['Asia_Low']
        asia_eq = levels['Asia_EQ']
        
        # On cherche les bougies du lendemain pour la session London
        # La session London commence à 01:00, donc on regarde le jour suivant
        next_date = pd.Timestamp(date) + pd.Timedelta(days=1)
        next_date = next_date.date()
        
        # Filtrer les bougies de la session London (01:00-04:00)
        mask_london = (df['Date_Only'] == next_date) & \
                      (df['Time_Only'] >= LONDON_START) & \
                      (df['Time_Only'] <= LONDON_END)
        
        london_data = df[mask_london]
        
        if len(london_data) == 0:
            continue
        
        london_start_idx = london_data.index[0]
        london_end_idx = london_data.index[-1]
        
        # === CONDITION A: Vérifier s'il y a un sweep sous Asia_Low ===
        sweep_detected = False
        sweep_idx = None
        
        for idx in range(london_start_idx, london_end_idx + 1):
            if df.iloc[idx]['Low'] < asia_low:
                sweep_detected = True
                sweep_idx = idx
                break
        
        if not sweep_detected:
            continue
        
        # === CONDITION B: Détecter les FVG baissiers ===
        # On cherche les FVG depuis le début de London jusqu'au sweep (et un peu après)
        search_end_idx = min(sweep_idx + 10, london_end_idx)
        fvg_list = detect_fvg_bearish(df, london_start_idx, search_end_idx)
        
        if len(fvg_list) == 0:
            continue
        
        # === CONDITION C: Chercher le signal (clôture au-dessus du FVG) ===
        # On cherche le signal après le sweep, jusqu'à la fin de la journée ou un peu après London
        signal_search_end = london_end_idx + 20  # On étend un peu après London
        
        trade_taken = False
        
        for fvg in fvg_list:
            signal_idx = find_signal_candle(df, fvg, sweep_idx, signal_search_end)
            
            if signal_idx is not None:
                # On a un signal! Entrer en position
                entry_price = df.iloc[signal_idx]['Close']
                entry_time = df.iloc[signal_idx]['DateTime']
                
                # Stop Loss au niveau de Asia_Low
                stop_loss = asia_low
                
                # Take Profit au niveau de Asia_EQ
                take_profit = asia_eq
                
                # Vérifier que le trade a du sens (TP > Entry > SL)
                if not (take_profit > entry_price > stop_loss):
                    continue
                
                # === GESTION DU TRADE ===
                # On parcourt les bougies suivantes jusqu'à toucher SL, TP ou sortie temporelle
                exit_price = None
                exit_time = None
                exit_reason = None
                
                # Chercher les bougies après l'entrée
                for i in range(signal_idx + 1, len(df)):
                    candle = df.iloc[i]
                    candle_time = candle['DateTime']
                    
                    # Vérifier la sortie temporelle (11:00)
                    if candle_time.time() >= EXIT_TIME and candle_time.date() == next_date:
                        exit_price = candle['Close']
                        exit_time = candle_time
                        exit_reason = 'Time Exit'
                        break
                    
                    # Vérifier le Stop Loss
                    if candle['Low'] <= stop_loss:
                        exit_price = stop_loss
                        exit_time = candle_time
                        exit_reason = 'Stop Loss'
                        break
                    
                    # Vérifier le Take Profit
                    if candle['High'] >= take_profit:
                        exit_price = take_profit
                        exit_time = candle_time
                        exit_reason = 'Take Profit'
                        break
                
                # Si on n'a pas trouvé de sortie (fin des données), on skip ce trade
                if exit_price is None:
                    continue
                
                # Calculer le PnL
                pnl = exit_price - entry_price
                risk = entry_price - stop_loss
                reward = take_profit - entry_price
                rr_ratio = reward / risk if risk > 0 else 0
                
                # Enregistrer le trade
                trade = {
                    'Date': next_date,
                    'Entry_Time': entry_time,
                    'Entry_Price': entry_price,
                    'Exit_Time': exit_time,
                    'Exit_Price': exit_price,
                    'Exit_Reason': exit_reason,
                    'Stop_Loss': stop_loss,
                    'Take_Profit': take_profit,
                    'PnL': pnl,
                    'Risk': risk,
                    'Reward': reward,
                    'RR_Ratio': rr_ratio,
                    'Asia_Low': asia_low,
                    'Asia_EQ': asia_eq,
                    'FVG_High': fvg['fvg_high'],
                    'FVG_Low': fvg['fvg_low']
                }
                
                trades.append(trade)
                trade_taken = True
                break  # Un seul trade par jour
        
        if trade_taken:
            pass  # Trade enregistré
    
    print(f"\n✓ Backtest terminé: {len(trades)} trades détectés")
    
    return trades


def calculate_performance(trades):
    """
    Calcule les métriques de performance du backtest.
    """
    print("\n" + "=" * 80)
    print("ANALYSE DE LA PERFORMANCE")
    print("=" * 80)
    
    if len(trades) == 0:
        print("\n❌ Aucun trade détecté. Impossible de calculer les performances.")
        return
    
    df_trades = pd.DataFrame(trades)
    
    # Nombre total de trades
    total_trades = len(df_trades)
    
    # Trades gagnants et perdants
    winning_trades = df_trades[df_trades['PnL'] > 0]
    losing_trades = df_trades[df_trades['PnL'] < 0]
    breakeven_trades = df_trades[df_trades['PnL'] == 0]
    
    num_wins = len(winning_trades)
    num_losses = len(losing_trades)
    num_breakeven = len(breakeven_trades)
    
    # Win Rate
    win_rate = (num_wins / total_trades * 100) if total_trades > 0 else 0
    
    # Somme des gains et pertes
    total_gains = winning_trades['PnL'].sum() if num_wins > 0 else 0
    total_losses = abs(losing_trades['PnL'].sum()) if num_losses > 0 else 0
    
    # Profit Factor
    profit_factor = (total_gains / total_losses) if total_losses > 0 else float('inf')
    
    # Performance totale en points
    total_pnl = df_trades['PnL'].sum()
    
    # Average R:R
    avg_rr = df_trades['RR_Ratio'].mean() if total_trades > 0 else 0
    
    # Moyenne des gains et pertes
    avg_win = winning_trades['PnL'].mean() if num_wins > 0 else 0
    avg_loss = losing_trades['PnL'].mean() if num_losses > 0 else 0
    
    # Top 5 meilleurs trades
    top_5_trades = df_trades.nlargest(5, 'PnL')
    
    # Affichage du rapport
    print(f"\n📊 RAPPORT DE PERFORMANCE")
    print("-" * 80)
    print(f"Nombre total de trades        : {total_trades}")
    print(f"  • Trades gagnants           : {num_wins}")
    print(f"  • Trades perdants           : {num_losses}")
    print(f"  • Trades breakeven          : {num_breakeven}")
    print()
    print(f"Win Rate                      : {win_rate:.2f}%")
    print()
    print(f"Ratio Gain/Perte moyen (R:R)  : {avg_rr:.2f}")
    print()
    print(f"Profit Factor                 : {profit_factor:.2f}" if profit_factor != float('inf') else "Profit Factor                 : ∞ (aucune perte)")
    print()
    print(f"Performance totale (points)   : {total_pnl:.2f}")
    print(f"  • Total des gains           : +{total_gains:.2f}")
    print(f"  • Total des pertes          : -{total_losses:.2f}")
    print()
    print(f"Moyenne par trade gagnant     : {avg_win:.2f} points")
    print(f"Moyenne par trade perdant     : {avg_loss:.2f} points")
    
    # Distribution des sorties
    print("\n" + "-" * 80)
    print("DISTRIBUTION DES SORTIES")
    print("-" * 80)
    exit_reasons = df_trades['Exit_Reason'].value_counts()
    for reason, count in exit_reasons.items():
        percentage = (count / total_trades * 100)
        print(f"  • {reason:20s} : {count:3d} trades ({percentage:5.1f}%)")
    
    # Top 5 meilleurs trades
    print("\n" + "-" * 80)
    print("TOP 5 MEILLEURS TRADES")
    print("-" * 80)
    print(f"{'#':<4} {'Date':<12} {'Entrée':<10} {'Sortie':<10} {'PnL':<12} {'Raison':<15}")
    print("-" * 80)
    
    for idx, (i, trade) in enumerate(top_5_trades.iterrows(), 1):
        date_str = str(trade['Date'])
        entry_str = f"{trade['Entry_Price']:.2f}"
        exit_str = f"{trade['Exit_Price']:.2f}"
        pnl_str = f"+{trade['PnL']:.2f}" if trade['PnL'] > 0 else f"{trade['PnL']:.2f}"
        reason_str = trade['Exit_Reason']
        
        print(f"{idx:<4} {date_str:<12} {entry_str:<10} {exit_str:<10} {pnl_str:<12} {reason_str:<15}")
    
    # Pire 5 trades
    print("\n" + "-" * 80)
    print("PIRE 5 TRADES")
    print("-" * 80)
    bottom_5_trades = df_trades.nsmallest(5, 'PnL')
    print(f"{'#':<4} {'Date':<12} {'Entrée':<10} {'Sortie':<10} {'PnL':<12} {'Raison':<15}")
    print("-" * 80)
    
    for idx, (i, trade) in enumerate(bottom_5_trades.iterrows(), 1):
        date_str = str(trade['Date'])
        entry_str = f"{trade['Entry_Price']:.2f}"
        exit_str = f"{trade['Exit_Price']:.2f}"
        pnl_str = f"{trade['PnL']:.2f}"
        reason_str = trade['Exit_Reason']
        
        print(f"{idx:<4} {date_str:<12} {entry_str:<10} {exit_str:<10} {pnl_str:<12} {reason_str:<15}")
    
    print("\n" + "=" * 80)
    
    return df_trades


def save_trades_to_csv(df_trades, filename='judas_swing_trades.csv'):
    """
    Sauvegarde les trades dans un fichier CSV pour analyse ultérieure.
    """
    if df_trades is not None and len(df_trades) > 0:
        output_path = os.path.join(BASE_DIR, filename)
        df_trades.to_csv(output_path, index=False, sep=';')
        print(f"\n💾 Trades sauvegardés dans: {filename}")
        return output_path
    return None


def main():
    """
    Fonction principale du backtest.
    """
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 78 + "║")
    print("║" + "  BACKTEST STRATÉGIE: JUDAS SWING & INVERSION".center(78) + "║")
    print("║" + "  Nasdaq 100 (NQ) - Timeframe 5 minutes".center(78) + "║")
    print("║" + "  Période: 2018-2025".center(78) + "║")
    print("║" + " " * 78 + "║")
    print("╚" + "=" * 78 + "╝")
    
    # Étape 1: Chargement des données
    df = load_data()
    
    # Étape 2: Calcul des niveaux Asia Session
    asia_levels = calculate_asia_session_levels(df)
    
    # Étape 3: Backtest de la stratégie
    trades = backtest_strategy(df, asia_levels)
    
    # Étape 4: Analyse de la performance
    df_trades = calculate_performance(trades)
    
    # Étape 5: Sauvegarde des résultats
    if df_trades is not None:
        save_trades_to_csv(df_trades)
    
    print("\n✅ Backtest terminé avec succès!\n")


if __name__ == "__main__":
    main()

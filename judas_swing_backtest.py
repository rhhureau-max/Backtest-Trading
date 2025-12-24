#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Backtest de la stratégie "Judas Swing & Inversion FVG" sur le Nasdaq 100 (NQ)
Version LONG & SHORT
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

# Paramètres de gestion du capital
INITIAL_CAPITAL = 100000  # 100k$
RISK_PER_TRADE = 0.01     # 1% de risque par trade


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
    
    for i in range(start_idx + 1, end_idx):
        if i < 1 or i >= len(df) - 1:
            continue
        
        # Bougie N-1 (précédente)
        low_prev = df.iloc[i - 1]['Low']
        
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


def detect_fvg_bullish(df, start_idx, end_idx):
    """
    Détecte les Fair Value Gaps (FVG) haussiers entre start_idx et end_idx.
    Un FVG haussier se forme quand:
    - Le High de la bougie N-1 est inférieur au Low de la bougie N+1
    - Cela crée un gap (espace non comblé) pendant un mouvement haussier
    
    Retourne une liste de dictionnaires avec les informations des FVG trouvés.
    """
    fvg_list = []
    
    for i in range(start_idx + 1, end_idx):
        if i < 1 or i >= len(df) - 1:
            continue
        
        # Bougie N-1 (précédente)
        high_prev = df.iloc[i - 1]['High']
        
        # Bougie N+1 (suivante)
        low_next = df.iloc[i + 1]['Low']
        
        # Vérification du FVG haussier: gap entre High(N-1) et Low(N+1)
        if high_prev < low_next:
            fvg = {
                'idx': i,
                'datetime': df.iloc[i]['DateTime'],
                'fvg_high': low_next,  # Bord haut du FVG
                'fvg_low': high_prev,  # Bord bas du FVG
            }
            fvg_list.append(fvg)
    
    return fvg_list


def find_long_signal_candle(df, fvg, start_idx, end_idx):
    """
    Cherche une bougie qui clôture strictement au-dessus du bord haut du FVG (fvg_high).
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


def find_short_signal_candle(df, fvg, start_idx, end_idx):
    """
    Cherche une bougie qui clôture strictement en dessous du bord bas du FVG (fvg_low).
    Retourne l'index de la première bougie qui remplit cette condition, ou None.
    """
    fvg_low = fvg['fvg_low']
    fvg_idx = fvg['idx']
    
    # On cherche après la formation du FVG (fvg_idx + 2, car le FVG se forme sur N+1)
    for i in range(fvg_idx + 2, end_idx + 1):
        if i >= len(df):
            break
        
        close = df.iloc[i]['Close']
        
        # Signal: la bougie clôture strictement en dessous du bord bas du FVG
        if close < fvg_low:
            return i
    
    return None


def backtest_strategy(df, asia_levels):
    """
    Backtest de la stratégie Judas Swing & Inversion (LONG & SHORT).
    
    Pour chaque jour:
    1. Vérifie les sweeps (sous Asia_Low pour LONG, au-dessus Asia_High pour SHORT)
    2. Détecte les FVG correspondants
    3. Cherche les signaux (inversions)
    4. Entre en position et gère le trade (SL, TP, sortie temporelle)
    5. Prend le premier signal chronologique si conflit LONG/SHORT
    """
    print("\n" + "=" * 80)
    print("BACKTEST DE LA STRATÉGIE (LONG & SHORT)")
    print("=" * 80)
    
    trades = []
    
    # Pour chaque jour où on a des niveaux Asia
    for date, levels in asia_levels.items():
        asia_high = levels['Asia_High']
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
        
        # === DÉTECTION DES SIGNAUX LONG ET SHORT ===
        
        # Variables pour stocker les signaux potentiels
        long_signal = None
        short_signal = None
        
        # === STRATÉGIE LONG ===
        # Condition A: Vérifier s'il y a un sweep sous Asia_Low
        sweep_low_detected = False
        sweep_low_idx = None
        
        for idx in range(london_start_idx, london_end_idx + 1):
            if df.iloc[idx]['Low'] < asia_low:
                sweep_low_detected = True
                sweep_low_idx = idx
                break
        
        if sweep_low_detected:
            # Condition B: Détecter les FVG baissiers
            search_end_idx = min(sweep_low_idx + 10, london_end_idx)
            fvg_bearish_list = detect_fvg_bearish(df, london_start_idx, search_end_idx)
            
            if len(fvg_bearish_list) > 0:
                # Condition C: Chercher le signal LONG (clôture au-dessus du FVG)
                signal_search_end = london_end_idx + 20
                
                for fvg in fvg_bearish_list:
                    signal_idx = find_long_signal_candle(df, fvg, sweep_low_idx, signal_search_end)
                    
                    if signal_idx is not None:
                        entry_price = df.iloc[signal_idx]['Close']
                        entry_time = df.iloc[signal_idx]['DateTime']
                        
                        # Stop Loss: Sous le low de la bougie de signal
                        stop_loss = df.iloc[signal_idx]['Low']
                        
                        # Take Profit: Asia_EQ
                        take_profit = asia_eq
                        
                        # Vérifier que le trade a du sens (TP > Entry > SL)
                        if take_profit > entry_price > stop_loss:
                            long_signal = {
                                'direction': 'LONG',
                                'signal_idx': signal_idx,
                                'entry_price': entry_price,
                                'entry_time': entry_time,
                                'stop_loss': stop_loss,
                                'take_profit': take_profit,
                                'fvg_high': fvg['fvg_high'],
                                'fvg_low': fvg['fvg_low']
                            }
                            break
        
        # === STRATÉGIE SHORT ===
        # Condition A: Vérifier s'il y a un sweep au-dessus de Asia_High
        sweep_high_detected = False
        sweep_high_idx = None
        
        for idx in range(london_start_idx, london_end_idx + 1):
            if df.iloc[idx]['High'] > asia_high:
                sweep_high_detected = True
                sweep_high_idx = idx
                break
        
        if sweep_high_detected:
            # Condition B: Détecter les FVG haussiers
            search_end_idx = min(sweep_high_idx + 10, london_end_idx)
            fvg_bullish_list = detect_fvg_bullish(df, london_start_idx, search_end_idx)
            
            if len(fvg_bullish_list) > 0:
                # Condition C: Chercher le signal SHORT (clôture en dessous du FVG)
                signal_search_end = london_end_idx + 20
                
                for fvg in fvg_bullish_list:
                    signal_idx = find_short_signal_candle(df, fvg, sweep_high_idx, signal_search_end)
                    
                    if signal_idx is not None:
                        entry_price = df.iloc[signal_idx]['Close']
                        entry_time = df.iloc[signal_idx]['DateTime']
                        
                        # Stop Loss: Au-dessus du high de la bougie de signal
                        stop_loss = df.iloc[signal_idx]['High']
                        
                        # Take Profit: Asia_EQ
                        take_profit = asia_eq
                        
                        # Vérifier que le trade a du sens (Entry > TP et SL > Entry)
                        if entry_price > take_profit and stop_loss > entry_price:
                            short_signal = {
                                'direction': 'SHORT',
                                'signal_idx': signal_idx,
                                'entry_price': entry_price,
                                'entry_time': entry_time,
                                'stop_loss': stop_loss,
                                'take_profit': take_profit,
                                'fvg_high': fvg['fvg_high'],
                                'fvg_low': fvg['fvg_low']
                            }
                            break
        
        # === GESTION DES CONFLITS: Prendre le premier signal chronologique ===
        selected_signal = None
        
        if long_signal and short_signal:
            # Les deux signaux sont présents, prendre le premier chronologiquement
            if long_signal['signal_idx'] < short_signal['signal_idx']:
                selected_signal = long_signal
            else:
                selected_signal = short_signal
        elif long_signal:
            selected_signal = long_signal
        elif short_signal:
            selected_signal = short_signal
        
        # === EXÉCUTION DU TRADE ===
        if selected_signal:
            direction = selected_signal['direction']
            entry_price = selected_signal['entry_price']
            entry_time = selected_signal['entry_time']
            stop_loss = selected_signal['stop_loss']
            take_profit = selected_signal['take_profit']
            signal_idx = selected_signal['signal_idx']
            
            # Gestion du trade
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
                
                if direction == 'LONG':
                    # Vérifier le Stop Loss (LONG)
                    if candle['Low'] <= stop_loss:
                        exit_price = stop_loss
                        exit_time = candle_time
                        exit_reason = 'Stop Loss'
                        break
                    
                    # Vérifier le Take Profit (LONG)
                    if candle['High'] >= take_profit:
                        exit_price = take_profit
                        exit_time = candle_time
                        exit_reason = 'Take Profit'
                        break
                
                elif direction == 'SHORT':
                    # Vérifier le Stop Loss (SHORT)
                    if candle['High'] >= stop_loss:
                        exit_price = stop_loss
                        exit_time = candle_time
                        exit_reason = 'Stop Loss'
                        break
                    
                    # Vérifier le Take Profit (SHORT)
                    if candle['Low'] <= take_profit:
                        exit_price = take_profit
                        exit_time = candle_time
                        exit_reason = 'Take Profit'
                        break
            
            # Si on n'a pas trouvé de sortie (fin des données), on skip ce trade
            if exit_price is None:
                continue
            
            # Calculer le PnL
            if direction == 'LONG':
                pnl = exit_price - entry_price
                risk = entry_price - stop_loss
                reward = take_profit - entry_price
            else:  # SHORT
                pnl = entry_price - exit_price
                risk = stop_loss - entry_price
                reward = entry_price - take_profit
            
            rr_ratio = reward / risk if risk > 0 else 0
            
            # Enregistrer le trade
            trade = {
                'Date': next_date,
                'Direction': direction,
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
                'Asia_High': asia_high,
                'Asia_Low': asia_low,
                'Asia_EQ': asia_eq,
                'FVG_High': selected_signal['fvg_high'],
                'FVG_Low': selected_signal['fvg_low']
            }
            
            trades.append(trade)
    
    print(f"\n✓ Backtest terminé: {len(trades)} trades détectés")
    
    return trades


def simulate_capital(df_trades, initial_capital=INITIAL_CAPITAL, risk_per_trade=RISK_PER_TRADE):
    """
    Simule l'évolution du capital avec un risque fixe par trade.
    Retourne un DataFrame avec l'évolution du capital.
    """
    capital = initial_capital
    capital_history = [capital]
    
    for idx, trade in df_trades.iterrows():
        risk_points = trade['Risk']
        pnl_points = trade['PnL']
        
        # Calculer la taille de position basée sur le risque
        # Risque $ = capital * risk_per_trade
        # Position size = Risque $ / risk_points
        risk_amount = capital * risk_per_trade
        
        if risk_points > 0:
            position_size = risk_amount / risk_points
        else:
            position_size = 0
        
        # PnL en dollars = PnL en points * position size
        pnl_dollars = pnl_points * position_size
        
        # Mise à jour du capital
        capital += pnl_dollars
        capital_history.append(capital)
        
        # Ajouter les informations au DataFrame
        df_trades.at[idx, 'Position_Size'] = position_size
        df_trades.at[idx, 'Risk_Amount'] = risk_amount
        df_trades.at[idx, 'PnL_Dollars'] = pnl_dollars
        df_trades.at[idx, 'Capital'] = capital
    
    return df_trades, capital_history


def calculate_performance(trades):
    """
    Calcule les métriques de performance du backtest.
    """
    print("\n" + "=" * 80)
    print("ANALYSE DE LA PERFORMANCE")
    print("=" * 80)
    
    if len(trades) == 0:
        print("\n❌ Aucun trade détecté. Impossible de calculer les performances.")
        return None
    
    df_trades = pd.DataFrame(trades)
    
    # Simulation du capital
    df_trades, capital_history = simulate_capital(df_trades)
    
    # Nombre total de trades
    total_trades = len(df_trades)
    
    # Trades par direction
    long_trades = df_trades[df_trades['Direction'] == 'LONG']
    short_trades = df_trades[df_trades['Direction'] == 'SHORT']
    
    num_long = len(long_trades)
    num_short = len(short_trades)
    
    # Trades gagnants et perdants (globaux)
    winning_trades = df_trades[df_trades['PnL'] > 0]
    losing_trades = df_trades[df_trades['PnL'] < 0]
    breakeven_trades = df_trades[df_trades['PnL'] == 0]
    
    num_wins = len(winning_trades)
    num_losses = len(losing_trades)
    num_breakeven = len(breakeven_trades)
    
    # Win Rate global
    win_rate = (num_wins / total_trades * 100) if total_trades > 0 else 0
    
    # Somme des gains et pertes
    total_gains = winning_trades['PnL'].sum() if num_wins > 0 else 0
    total_losses = abs(losing_trades['PnL'].sum()) if num_losses > 0 else 0
    
    # Profit Factor
    profit_factor = (total_gains / total_losses) if total_losses > 0 else float('inf')
    
    # Performance totale en points
    total_pnl_points = df_trades['PnL'].sum()
    
    # Performance totale en dollars
    total_pnl_dollars = df_trades['PnL_Dollars'].sum()
    final_capital = capital_history[-1]
    
    # Average R:R
    avg_rr = df_trades['RR_Ratio'].mean() if total_trades > 0 else 0
    
    # Moyenne des gains et pertes
    avg_win = winning_trades['PnL'].mean() if num_wins > 0 else 0
    avg_loss = losing_trades['PnL'].mean() if num_losses > 0 else 0
    
    # === PERFORMANCE PAR DIRECTION ===
    
    # LONG
    long_wins = long_trades[long_trades['PnL'] > 0]
    long_losses = long_trades[long_trades['PnL'] < 0]
    long_win_rate = (len(long_wins) / num_long * 100) if num_long > 0 else 0
    long_total_pnl = long_trades['PnL'].sum() if num_long > 0 else 0
    long_avg_rr = long_trades['RR_Ratio'].mean() if num_long > 0 else 0
    
    long_total_gains = long_wins['PnL'].sum() if len(long_wins) > 0 else 0
    long_total_losses = abs(long_losses['PnL'].sum()) if len(long_losses) > 0 else 0
    long_profit_factor = (long_total_gains / long_total_losses) if long_total_losses > 0 else float('inf')
    
    # SHORT
    short_wins = short_trades[short_trades['PnL'] > 0]
    short_losses = short_trades[short_trades['PnL'] < 0]
    short_win_rate = (len(short_wins) / num_short * 100) if num_short > 0 else 0
    short_total_pnl = short_trades['PnL'].sum() if num_short > 0 else 0
    short_avg_rr = short_trades['RR_Ratio'].mean() if num_short > 0 else 0
    
    short_total_gains = short_wins['PnL'].sum() if len(short_wins) > 0 else 0
    short_total_losses = abs(short_losses['PnL'].sum()) if len(short_losses) > 0 else 0
    short_profit_factor = (short_total_gains / short_total_losses) if short_total_losses > 0 else float('inf')
    
    # Top 5 meilleurs trades
    top_5_trades = df_trades.nlargest(5, 'PnL_Dollars')
    
    # === AFFICHAGE DU RAPPORT ===
    
    print(f"\n📊 RAPPORT DE PERFORMANCE GLOBAL")
    print("-" * 80)
    print(f"Nombre total de trades        : {total_trades}")
    print(f"  • Trades LONG               : {num_long}")
    print(f"  • Trades SHORT              : {num_short}")
    print()
    print(f"Trades gagnants               : {num_wins}")
    print(f"Trades perdants               : {num_losses}")
    print(f"Trades breakeven              : {num_breakeven}")
    print()
    print(f"Win Rate Global               : {win_rate:.2f}%")
    print()
    print(f"Ratio Gain/Perte moyen (R:R)  : {avg_rr:.2f}")
    print()
    if profit_factor == float('inf'):
        print(f"Profit Factor                 : ∞ (aucune perte)")
    else:
        print(f"Profit Factor                 : {profit_factor:.2f}")
    print()
    print(f"Performance totale (points)   : {total_pnl_points:.2f}")
    print(f"  • Total des gains           : +{total_gains:.2f}")
    print(f"  • Total des pertes          : -{total_losses:.2f}")
    print()
    print(f"Moyenne par trade gagnant     : {avg_win:.2f} points")
    print(f"Moyenne par trade perdant     : {avg_loss:.2f} points")
    
    # === SIMULATION DE CAPITAL ===
    print("\n" + "-" * 80)
    print("SIMULATION DE CAPITAL")
    print("-" * 80)
    print(f"Capital initial               : ${INITIAL_CAPITAL:,.2f}")
    print(f"Capital final                 : ${final_capital:,.2f}")
    print(f"Performance totale            : ${total_pnl_dollars:,.2f}")
    print(f"Rendement                     : {((final_capital - INITIAL_CAPITAL) / INITIAL_CAPITAL * 100):.2f}%")
    print(f"Risque par trade              : {RISK_PER_TRADE * 100:.1f}% du capital")
    
    # === COMPARAISON LONG vs SHORT ===
    print("\n" + "-" * 80)
    print("COMPARAISON LONG vs SHORT")
    print("-" * 80)
    print(f"\n{'Métrique':<30} {'LONG':<20} {'SHORT':<20}")
    print("-" * 70)
    print(f"{'Nombre de trades':<30} {num_long:<20} {num_short:<20}")
    print(f"{'Win Rate':<30} {long_win_rate:.2f}%{'':<14} {short_win_rate:.2f}%")
    print(f"{'Profit Factor':<30} ", end='')
    if long_profit_factor == float('inf'):
        print(f"{'∞':<20}", end='')
    else:
        print(f"{long_profit_factor:.2f}{'':<16}", end='')
    if short_profit_factor == float('inf'):
        print(f"∞")
    else:
        print(f"{short_profit_factor:.2f}")
    print(f"{'R:R Moyen':<30} {long_avg_rr:.2f}{'':<16} {short_avg_rr:.2f}")
    print(f"{'Performance (points)':<30} {long_total_pnl:.2f}{'':<16} {short_total_pnl:.2f}")
    
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
    print(f"{'#':<4} {'Date':<12} {'Dir':<6} {'Entrée':<10} {'Sortie':<10} {'PnL ($)':<15} {'Raison':<15}")
    print("-" * 80)
    
    for idx, (i, trade) in enumerate(top_5_trades.iterrows(), 1):
        date_str = str(trade['Date'])
        direction = trade['Direction']
        entry_str = f"{trade['Entry_Price']:.2f}"
        exit_str = f"{trade['Exit_Price']:.2f}"
        pnl_str = f"+${trade['PnL_Dollars']:,.2f}" if trade['PnL_Dollars'] > 0 else f"-${abs(trade['PnL_Dollars']):,.2f}"
        reason_str = trade['Exit_Reason']
        
        print(f"{idx:<4} {date_str:<12} {direction:<6} {entry_str:<10} {exit_str:<10} {pnl_str:<15} {reason_str:<15}")
    
    # Pire 5 trades
    print("\n" + "-" * 80)
    print("PIRE 5 TRADES")
    print("-" * 80)
    bottom_5_trades = df_trades.nsmallest(5, 'PnL_Dollars')
    print(f"{'#':<4} {'Date':<12} {'Dir':<6} {'Entrée':<10} {'Sortie':<10} {'PnL ($)':<15} {'Raison':<15}")
    print("-" * 80)
    
    for idx, (i, trade) in enumerate(bottom_5_trades.iterrows(), 1):
        date_str = str(trade['Date'])
        direction = trade['Direction']
        entry_str = f"{trade['Entry_Price']:.2f}"
        exit_str = f"{trade['Exit_Price']:.2f}"
        pnl_str = f"-${abs(trade['PnL_Dollars']):,.2f}"
        reason_str = trade['Exit_Reason']
        
        print(f"{idx:<4} {date_str:<12} {direction:<6} {entry_str:<10} {exit_str:<10} {pnl_str:<15} {reason_str:<15}")
    
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


def save_report_to_file(df_trades, filename='RESULTATS_BACKTEST.txt'):
    """
    Sauvegarde un rapport détaillé dans un fichier texte.
    """
    if df_trades is None or len(df_trades) == 0:
        return None
    
    output_path = os.path.join(BASE_DIR, filename)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("RAPPORT DE BACKTEST - STRATÉGIE JUDAS SWING & INVERSION FVG\n")
        f.write("Version LONG & SHORT\n")
        f.write("=" * 80 + "\n\n")
        
        f.write(f"Date du rapport: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Période analysée: {df_trades['Date'].min()} à {df_trades['Date'].max()}\n")
        f.write(f"Timeframe: 5 minutes\n")
        f.write(f"Timezone: Chicago (UTC-5)\n\n")
        
        # Statistiques globales
        total_trades = len(df_trades)
        num_long = len(df_trades[df_trades['Direction'] == 'LONG'])
        num_short = len(df_trades[df_trades['Direction'] == 'SHORT'])
        
        winning_trades = df_trades[df_trades['PnL'] > 0]
        losing_trades = df_trades[df_trades['PnL'] < 0]
        
        num_wins = len(winning_trades)
        num_losses = len(losing_trades)
        
        win_rate = (num_wins / total_trades * 100) if total_trades > 0 else 0
        
        total_gains = winning_trades['PnL'].sum() if num_wins > 0 else 0
        total_losses = abs(losing_trades['PnL'].sum()) if num_losses > 0 else 0
        profit_factor = (total_gains / total_losses) if total_losses > 0 else float('inf')
        
        total_pnl_points = df_trades['PnL'].sum()
        total_pnl_dollars = df_trades['PnL_Dollars'].sum()
        final_capital = df_trades['Capital'].iloc[-1]
        
        avg_rr = df_trades['RR_Ratio'].mean()
        
        f.write("MÉTRIQUES GLOBALES\n")
        f.write("-" * 80 + "\n")
        f.write(f"Nombre total de trades: {total_trades}\n")
        f.write(f"  - Trades LONG: {num_long}\n")
        f.write(f"  - Trades SHORT: {num_short}\n\n")
        
        f.write(f"Trades gagnants: {num_wins}\n")
        f.write(f"Trades perdants: {num_losses}\n\n")
        
        f.write(f"Win Rate Global: {win_rate:.2f}%\n\n")
        
        if profit_factor == float('inf'):
            f.write(f"Profit Factor: ∞ (aucune perte)\n\n")
        else:
            f.write(f"Profit Factor: {profit_factor:.2f}\n\n")
        
        f.write(f"R:R Moyen: {avg_rr:.2f}\n\n")
        
        f.write(f"Performance totale (points): {total_pnl_points:.2f}\n")
        f.write(f"Performance totale (dollars): ${total_pnl_dollars:,.2f}\n\n")
        
        f.write("SIMULATION DE CAPITAL\n")
        f.write("-" * 80 + "\n")
        f.write(f"Capital initial: ${INITIAL_CAPITAL:,.2f}\n")
        f.write(f"Capital final: ${final_capital:,.2f}\n")
        f.write(f"Rendement: {((final_capital - INITIAL_CAPITAL) / INITIAL_CAPITAL * 100):.2f}%\n")
        f.write(f"Risque par trade: {RISK_PER_TRADE * 100:.1f}% du capital\n\n")
        
        # Comparaison LONG vs SHORT
        long_trades = df_trades[df_trades['Direction'] == 'LONG']
        short_trades = df_trades[df_trades['Direction'] == 'SHORT']
        
        long_wins = long_trades[long_trades['PnL'] > 0]
        long_losses = long_trades[long_trades['PnL'] < 0]
        long_win_rate = (len(long_wins) / num_long * 100) if num_long > 0 else 0
        long_total_pnl = long_trades['PnL'].sum() if num_long > 0 else 0
        long_avg_rr = long_trades['RR_Ratio'].mean() if num_long > 0 else 0
        
        long_total_gains = long_wins['PnL'].sum() if len(long_wins) > 0 else 0
        long_total_losses = abs(long_losses['PnL'].sum()) if len(long_losses) > 0 else 0
        long_profit_factor = (long_total_gains / long_total_losses) if long_total_losses > 0 else float('inf')
        
        short_wins = short_trades[short_trades['PnL'] > 0]
        short_losses = short_trades[short_trades['PnL'] < 0]
        short_win_rate = (len(short_wins) / num_short * 100) if num_short > 0 else 0
        short_total_pnl = short_trades['PnL'].sum() if num_short > 0 else 0
        short_avg_rr = short_trades['RR_Ratio'].mean() if num_short > 0 else 0
        
        short_total_gains = short_wins['PnL'].sum() if len(short_wins) > 0 else 0
        short_total_losses = abs(short_losses['PnL'].sum()) if len(short_losses) > 0 else 0
        short_profit_factor = (short_total_gains / short_total_losses) if short_total_losses > 0 else float('inf')
        
        f.write("COMPARAISON LONG vs SHORT\n")
        f.write("-" * 80 + "\n")
        f.write(f"{'Métrique':<30} {'LONG':<20} {'SHORT':<20}\n")
        f.write("-" * 70 + "\n")
        f.write(f"{'Nombre de trades':<30} {num_long:<20} {num_short:<20}\n")
        f.write(f"{'Win Rate':<30} {long_win_rate:.2f}%{'':<14} {short_win_rate:.2f}%\n")
        
        pf_long = '∞' if long_profit_factor == float('inf') else f"{long_profit_factor:.2f}"
        pf_short = '∞' if short_profit_factor == float('inf') else f"{short_profit_factor:.2f}"
        f.write(f"{'Profit Factor':<30} {pf_long:<20} {pf_short:<20}\n")
        
        f.write(f"{'R:R Moyen':<30} {long_avg_rr:.2f}{'':<16} {short_avg_rr:.2f}\n")
        f.write(f"{'Performance (points)':<30} {long_total_pnl:.2f}{'':<16} {short_total_pnl:.2f}\n\n")
        
        # Distribution des sorties
        f.write("DISTRIBUTION DES SORTIES\n")
        f.write("-" * 80 + "\n")
        exit_reasons = df_trades['Exit_Reason'].value_counts()
        for reason, count in exit_reasons.items():
            percentage = (count / total_trades * 100)
            f.write(f"  • {reason:20s} : {count:3d} trades ({percentage:5.1f}%)\n")
        
        f.write("\n" + "=" * 80 + "\n")
    
    print(f"📄 Rapport détaillé sauvegardé dans: {filename}")
    return output_path


def main():
    """
    Fonction principale du backtest.
    """
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 78 + "║")
    print("║" + "  BACKTEST STRATÉGIE: JUDAS SWING & INVERSION FVG".center(78) + "║")
    print("║" + "  Version LONG & SHORT".center(78) + "║")
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
        save_report_to_file(df_trades)
    
    print("\n✅ Backtest terminé avec succès!\n")


if __name__ == "__main__":
    main()

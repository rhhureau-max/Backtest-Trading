#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Backtest de la stratégie Fair Value Gap (FVG) sur le NQ
Timeframe: 5 minutes
Période: 2018-2025
"""

import pandas as pd
import numpy as np
from datetime import datetime, time
import os

class FVGBacktester:
    """
    Classe pour backtester la stratégie Fair Value Gap (FVG)
    """
    
    def __init__(self, data_file, tick_value=0.25, sl_ticks=5):
        """
        Initialisation du backtester
        
        Args:
            data_file: Chemin vers le fichier de données consolidé
            tick_value: Valeur d'un tick (0.25 pour le NQ)
            sl_ticks: Nombre de ticks pour le Stop Loss (5 par défaut)
        """
        self.data_file = data_file
        self.tick_value = tick_value
        self.sl_ticks = sl_ticks
        self.sl_distance = sl_ticks * tick_value
        
        # Scénarios de Risk/Reward à tester
        self.rr_scenarios = [1.0, 1.5, 2.0, 2.5]
        
        # Fenêtre horaire pour la détection des FVG (02:00 - 06:00)
        self.fvg_start_time = time(2, 0)
        self.fvg_end_time = time(6, 0)
        
        # Chargement des données
        self.df = None
        self.trades = []
        
    def load_data(self):
        """
        Charge les données depuis le fichier CSV consolidé
        """
        print("📂 Chargement des données...")
        
        self.df = pd.read_csv(self.data_file, encoding='utf-8')
        
        # Créer une colonne datetime complète
        self.df['DateTime'] = pd.to_datetime(
            self.df['Date'] + ' ' + self.df['Time'],
            format='%d/%m/%Y %H:%M:%S'
        )
        
        # Extraire l'heure seule pour les filtres
        self.df['TimeOnly'] = self.df['DateTime'].dt.time
        
        # Extraire la date seule pour grouper par session
        self.df['DateOnly'] = self.df['DateTime'].dt.date
        
        print(f"✅ {len(self.df)} bougies chargées")
        print(f"📅 Période: {self.df['DateTime'].min()} - {self.df['DateTime'].max()}")
        
    def identify_fvg(self, i):
        """
        Identifie si un Fair Value Gap est formé à l'index i
        
        Args:
            i: Index de la bougie actuelle
            
        Returns:
            dict: {'type': 'bullish'/'bearish'/None, 'upper': float, 'lower': float}
        """
        if i < 2:
            return None
        
        # Récupération des bougies
        candle_i_minus_2 = self.df.iloc[i - 2]
        candle_i = self.df.iloc[i]
        
        # FVG Haussier: Low[i] > High[i-2]
        if candle_i['Low'] > candle_i_minus_2['High']:
            return {
                'type': 'bullish',
                'upper': candle_i['Low'],
                'lower': candle_i_minus_2['High'],
                'index': i,
                'datetime': candle_i['DateTime']
            }
        
        # FVG Baissier: High[i] < Low[i-2]
        elif candle_i['High'] < candle_i_minus_2['Low']:
            return {
                'type': 'bearish',
                'upper': candle_i_minus_2['Low'],
                'lower': candle_i['High'],
                'index': i,
                'datetime': candle_i['DateTime']
            }
        
        return None
    
    def is_in_fvg_window(self, candle_time):
        """
        Vérifie si l'heure de la bougie est dans la fenêtre FVG (02:00 - 06:00)
        
        Args:
            candle_time: Objet time de la bougie
            
        Returns:
            bool: True si dans la fenêtre
        """
        return self.fvg_start_time <= candle_time < self.fvg_end_time
    
    def check_entry_signal(self, fvg, current_idx):
        """
        Vérifie si une bougie déclenche un signal d'entrée pour un FVG donné
        
        Args:
            fvg: Dictionnaire du FVG
            current_idx: Index de la bougie actuelle
            
        Returns:
            dict ou None: Signal d'entrée avec les détails
        """
        if current_idx >= len(self.df):
            return None
        
        candle = self.df.iloc[current_idx]
        
        # Pour un FVG Haussier (Long)
        if fvg['type'] == 'bullish':
            # Le prix entre dans le FVG (Low <= upper et High >= lower)
            price_in_gap = candle['Low'] <= fvg['upper'] and candle['High'] >= fvg['lower']
            
            # La bougie clôture au-dessus de la borne haute du FVG
            close_above = candle['Close'] > fvg['upper']
            
            if price_in_gap and close_above:
                # Entry à l'ouverture de la bougie suivante
                if current_idx + 1 < len(self.df):
                    next_candle = self.df.iloc[current_idx + 1]
                    
                    return {
                        'type': 'LONG',
                        'signal_candle_idx': current_idx,
                        'signal_candle_low': candle['Low'],
                        'entry_idx': current_idx + 1,
                        'entry_price': next_candle['Open'],
                        'entry_datetime': next_candle['DateTime'],
                        'fvg': fvg
                    }
        
        # Pour un FVG Baissier (Short)
        elif fvg['type'] == 'bearish':
            # Le prix entre dans le FVG
            price_in_gap = candle['Low'] <= fvg['upper'] and candle['High'] >= fvg['lower']
            
            # La bougie clôture en-dessous de la borne basse du FVG
            close_below = candle['Close'] < fvg['lower']
            
            if price_in_gap and close_below:
                # Entry à l'ouverture de la bougie suivante
                if current_idx + 1 < len(self.df):
                    next_candle = self.df.iloc[current_idx + 1]
                    
                    return {
                        'type': 'SHORT',
                        'signal_candle_idx': current_idx,
                        'signal_candle_high': candle['High'],
                        'entry_idx': current_idx + 1,
                        'entry_price': next_candle['Open'],
                        'entry_datetime': next_candle['DateTime'],
                        'fvg': fvg
                    }
        
        return None
    
    def calculate_exit_levels(self, signal):
        """
        Calcule les niveaux de Stop Loss et Take Profit pour tous les scénarios RR
        
        Args:
            signal: Dictionnaire du signal d'entrée
            
        Returns:
            dict: {'sl': float, 'tp_1R': float, 'tp_1.5R': float, ...}
        """
        entry_price = signal['entry_price']
        
        if signal['type'] == 'LONG':
            # SL quelques ticks sous le Low de la signal candle
            sl_price = signal['signal_candle_low'] - self.sl_distance
            risk = entry_price - sl_price
            
            # TPs pour chaque scénario RR
            tps = {f'tp_{rr}R': entry_price + (risk * rr) for rr in self.rr_scenarios}
            
        else:  # SHORT
            # SL quelques ticks au-dessus du High de la signal candle
            sl_price = signal['signal_candle_high'] + self.sl_distance
            risk = sl_price - entry_price
            
            # TPs pour chaque scénario RR
            tps = {f'tp_{rr}R': entry_price - (risk * rr) for rr in self.rr_scenarios}
        
        return {'sl': sl_price, **tps}
    
    def simulate_trade(self, signal, exit_levels):
        """
        Simule un trade depuis l'entrée jusqu'à la sortie (SL ou TP)
        
        Args:
            signal: Signal d'entrée
            exit_levels: Niveaux de sortie (SL et TPs)
            
        Returns:
            dict: Résultats du trade pour chaque scénario RR
        """
        entry_idx = signal['entry_idx']
        entry_price = signal['entry_price']
        sl_price = exit_levels['sl']
        trade_type = signal['type']
        
        # Initialiser les résultats pour chaque RR
        results = {
            'entry_date': signal['entry_datetime'].strftime('%d/%m/%Y'),
            'entry_time': signal['entry_datetime'].strftime('%H:%M:%S'),
            'entry_price': entry_price,
            'type': trade_type,
            'sl_price': sl_price
        }
        
        # Pour chaque scénario RR, suivre le trade
        for rr in self.rr_scenarios:
            tp_key = f'tp_{rr}R'
            tp_price = exit_levels[tp_key]
            
            results[tp_key] = tp_price
            
            # Parcourir les bougies suivantes pour trouver la sortie
            exit_found = False
            
            for i in range(entry_idx, len(self.df)):
                candle = self.df.iloc[i]
                
                if trade_type == 'LONG':
                    # Vérifier si le SL est touché
                    if candle['Low'] <= sl_price:
                        results[f'result_{rr}R'] = 'LOSS'
                        results[f'exit_price_{rr}R'] = sl_price
                        results[f'exit_date_{rr}R'] = candle['DateTime'].strftime('%d/%m/%Y')
                        results[f'exit_time_{rr}R'] = candle['DateTime'].strftime('%H:%M:%S')
                        results[f'pnl_{rr}R'] = sl_price - entry_price
                        exit_found = True
                        break
                    
                    # Vérifier si le TP est touché
                    elif candle['High'] >= tp_price:
                        results[f'result_{rr}R'] = 'WIN'
                        results[f'exit_price_{rr}R'] = tp_price
                        results[f'exit_date_{rr}R'] = candle['DateTime'].strftime('%d/%m/%Y')
                        results[f'exit_time_{rr}R'] = candle['DateTime'].strftime('%H:%M:%S')
                        results[f'pnl_{rr}R'] = tp_price - entry_price
                        exit_found = True
                        break
                
                else:  # SHORT
                    # Vérifier si le SL est touché
                    if candle['High'] >= sl_price:
                        results[f'result_{rr}R'] = 'LOSS'
                        results[f'exit_price_{rr}R'] = sl_price
                        results[f'exit_date_{rr}R'] = candle['DateTime'].strftime('%d/%m/%Y')
                        results[f'exit_time_{rr}R'] = candle['DateTime'].strftime('%H:%M:%S')
                        results[f'pnl_{rr}R'] = entry_price - sl_price
                        exit_found = True
                        break
                    
                    # Vérifier si le TP est touché
                    elif candle['Low'] <= tp_price:
                        results[f'result_{rr}R'] = 'WIN'
                        results[f'exit_price_{rr}R'] = tp_price
                        results[f'exit_date_{rr}R'] = candle['DateTime'].strftime('%d/%m/%Y')
                        results[f'exit_time_{rr}R'] = candle['DateTime'].strftime('%H:%M:%S')
                        results[f'pnl_{rr}R'] = entry_price - tp_price
                        exit_found = True
                        break
            
            # Si aucune sortie n'est trouvée (trade toujours ouvert)
            if not exit_found:
                results[f'result_{rr}R'] = 'OPEN'
                results[f'exit_price_{rr}R'] = np.nan
                results[f'exit_date_{rr}R'] = ''
                results[f'exit_time_{rr}R'] = ''
                results[f'pnl_{rr}R'] = 0.0
        
        return results
    
    def run_backtest(self):
        """
        Exécute le backtest complet
        """
        print("\n🔍 Démarrage du backtest...")
        print(f"   Fenêtre de détection FVG: {self.fvg_start_time} - {self.fvg_end_time}")
        print(f"   Stop Loss: {self.sl_ticks} ticks ({self.sl_distance} points)")
        print(f"   Scénarios RR: {self.rr_scenarios}\n")
        
        # Dictionnaire pour stocker les FVG actifs par session
        active_fvgs = {}  # key: date, value: list of FVGs
        
        # Parcourir toutes les bougies
        for i in range(2, len(self.df)):
            current_candle = self.df.iloc[i]
            current_time = current_candle['TimeOnly']
            current_date = current_candle['DateOnly']
            
            # Initialiser la liste des FVG pour cette date si nécessaire
            if current_date not in active_fvgs:
                active_fvgs[current_date] = []
            
            # 1. Identifier les nouveaux FVG dans la fenêtre horaire
            if self.is_in_fvg_window(current_time):
                fvg = self.identify_fvg(i)
                if fvg is not None:
                    active_fvgs[current_date].append(fvg)
                    # print(f"✓ FVG {fvg['type']} détecté à {current_candle['DateTime']}")
            
            # 2. Vérifier les signaux d'entrée pour les FVG actifs de la session en cours
            if current_date in active_fvgs and len(active_fvgs[current_date]) > 0:
                fvgs_to_remove = []
                
                for fvg in active_fvgs[current_date]:
                    # Vérifier le signal d'entrée
                    signal = self.check_entry_signal(fvg, i)
                    
                    if signal is not None:
                        # Calculer les niveaux de sortie
                        exit_levels = self.calculate_exit_levels(signal)
                        
                        # Simuler le trade
                        trade_result = self.simulate_trade(signal, exit_levels)
                        
                        # Enregistrer le trade
                        self.trades.append(trade_result)
                        
                        # Marquer ce FVG comme utilisé
                        fvgs_to_remove.append(fvg)
                        
                        # print(f"📈 Trade {trade_type} ouvert à {signal['entry_datetime']}")
                
                # Retirer les FVG qui ont généré un trade
                for fvg in fvgs_to_remove:
                    active_fvgs[current_date].remove(fvg)
            
            # Afficher la progression tous les 10000 bougies
            if i % 10000 == 0:
                print(f"   Progression: {i}/{len(self.df)} bougies analysées...")
        
        print(f"\n✅ Backtest terminé!")
        print(f"📊 Nombre total de trades: {len(self.trades)}")
    
    def calculate_performance_metrics(self):
        """
        Calcule les métriques de performance pour chaque scénario RR
        
        Returns:
            dict: Métriques par scénario RR
        """
        if len(self.trades) == 0:
            print("⚠️  Aucun trade à analyser!")
            return {}
        
        metrics = {}
        
        for rr in self.rr_scenarios:
            rr_key = f'{rr}R'
            result_key = f'result_{rr_key}'
            pnl_key = f'pnl_{rr_key}'
            
            # Extraire les résultats pour ce RR
            results = [trade[result_key] for trade in self.trades]
            pnls = [trade[pnl_key] for trade in self.trades if trade[result_key] in ['WIN', 'LOSS']]
            
            wins = results.count('WIN')
            losses = results.count('LOSS')
            open_trades = results.count('OPEN')
            closed_trades = wins + losses
            
            # Calcul des métriques
            if closed_trades > 0:
                winrate = (wins / closed_trades) * 100
                
                winning_pnls = [pnl for trade, pnl in zip(self.trades, pnls) 
                                if trade[result_key] == 'WIN']
                losing_pnls = [pnl for trade, pnl in zip(self.trades, pnls) 
                               if trade[result_key] == 'LOSS']
                
                avg_win = np.mean(winning_pnls) if winning_pnls else 0
                avg_loss = np.mean(losing_pnls) if losing_pnls else 0
                
                # Profit Factor
                total_wins = sum(winning_pnls) if winning_pnls else 0
                total_losses = abs(sum(losing_pnls)) if losing_pnls else 0
                profit_factor = total_wins / total_losses if total_losses > 0 else float('inf')
                
                # PnL net et cumulé
                net_pnl = sum(pnls)
                
                # Calcul du drawdown maximum
                cumulative_pnl = []
                cumsum = 0
                for pnl in pnls:
                    cumsum += pnl
                    cumulative_pnl.append(cumsum)
                
                if cumulative_pnl:
                    running_max = np.maximum.accumulate(cumulative_pnl)
                    drawdown = running_max - cumulative_pnl
                    max_drawdown = np.max(drawdown)
                else:
                    max_drawdown = 0
                
            else:
                winrate = 0
                avg_win = 0
                avg_loss = 0
                profit_factor = 0
                net_pnl = 0
                max_drawdown = 0
            
            metrics[rr_key] = {
                'total_trades': len(self.trades),
                'closed_trades': closed_trades,
                'open_trades': open_trades,
                'wins': wins,
                'losses': losses,
                'winrate': winrate,
                'avg_win': avg_win,
                'avg_loss': avg_loss,
                'profit_factor': profit_factor,
                'net_pnl': net_pnl,
                'max_drawdown': max_drawdown
            }
        
        return metrics
    
    def print_performance_report(self, metrics):
        """
        Affiche un rapport de performance formaté
        
        Args:
            metrics: Dictionnaire des métriques par RR
        """
        print("\n" + "="*70)
        print("📊 RAPPORT DE PERFORMANCE - STRATÉGIE FVG NQ")
        print("="*70)
        
        for rr_key, stats in metrics.items():
            print(f"\n{'─'*70}")
            print(f"💰 Scénario Risk/Reward: {rr_key}")
            print(f"{'─'*70}")
            print(f"  Nombre total de trades:    {stats['total_trades']}")
            print(f"  Trades clôturés:           {stats['closed_trades']}")
            print(f"  Trades ouverts:            {stats['open_trades']}")
            print(f"  Trades gagnants:           {stats['wins']}")
            print(f"  Trades perdants:           {stats['losses']}")
            print(f"  Winrate:                   {stats['winrate']:.2f}%")
            print(f"  Gain moyen:                {stats['avg_win']:.2f} points")
            print(f"  Perte moyenne:             {stats['avg_loss']:.2f} points")
            print(f"  Profit Factor:             {stats['profit_factor']:.2f}")
            print(f"  PnL Net:                   {stats['net_pnl']:.2f} points")
            print(f"  Drawdown Maximum:          {stats['max_drawdown']:.2f} points")
        
        print("\n" + "="*70 + "\n")
    
    def save_results(self, metrics, base_dir):
        """
        Sauvegarde les résultats dans des fichiers
        
        Args:
            metrics: Dictionnaire des métriques
            base_dir: Répertoire de base pour sauvegarder les fichiers
        """
        # 1. Sauvegarder les trades dans un CSV
        trades_df = pd.DataFrame(self.trades)
        
        # Réorganiser les colonnes pour une meilleure lisibilité
        base_cols = ['entry_date', 'entry_time', 'entry_price', 'type', 'sl_price']
        
        # Ajouter les colonnes spécifiques à chaque RR
        rr_cols = []
        for rr in self.rr_scenarios:
            rr_key = f'{rr}R'
            rr_cols.extend([
                f'tp_{rr_key}',
                f'result_{rr_key}',
                f'exit_price_{rr_key}',
                f'exit_date_{rr_key}',
                f'exit_time_{rr_key}',
                f'pnl_{rr_key}'
            ])
        
        all_cols = base_cols + rr_cols
        trades_df = trades_df[all_cols]
        
        trades_file = os.path.join(base_dir, 'backtest_results.csv')
        trades_df.to_csv(trades_file, index=False, encoding='utf-8')
        print(f"✅ Trades sauvegardés dans: backtest_results.csv")
        
        # 2. Sauvegarder le rapport de performance
        report_file = os.path.join(base_dir, 'performance_report.txt')
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("="*70 + "\n")
            f.write("RAPPORT DE PERFORMANCE - STRATÉGIE FVG NQ\n")
            f.write("="*70 + "\n")
            f.write(f"\nBacktest réalisé le: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Période analysée: {self.df['DateTime'].min()} - {self.df['DateTime'].max()}\n")
            f.write(f"Nombre de bougies: {len(self.df)}\n")
            f.write(f"Fenêtre FVG: {self.fvg_start_time} - {self.fvg_end_time}\n")
            f.write(f"Stop Loss: {self.sl_ticks} ticks ({self.sl_distance} points)\n")
            f.write(f"\n")
            
            for rr_key, stats in metrics.items():
                f.write(f"\n{'─'*70}\n")
                f.write(f"Scénario Risk/Reward: {rr_key}\n")
                f.write(f"{'─'*70}\n")
                f.write(f"  Nombre total de trades:    {stats['total_trades']}\n")
                f.write(f"  Trades clôturés:           {stats['closed_trades']}\n")
                f.write(f"  Trades ouverts:            {stats['open_trades']}\n")
                f.write(f"  Trades gagnants:           {stats['wins']}\n")
                f.write(f"  Trades perdants:           {stats['losses']}\n")
                f.write(f"  Winrate:                   {stats['winrate']:.2f}%\n")
                f.write(f"  Gain moyen:                {stats['avg_win']:.2f} points\n")
                f.write(f"  Perte moyenne:             {stats['avg_loss']:.2f} points\n")
                f.write(f"  Profit Factor:             {stats['profit_factor']:.2f}\n")
                f.write(f"  PnL Net:                   {stats['net_pnl']:.2f} points\n")
                f.write(f"  Drawdown Maximum:          {stats['max_drawdown']:.2f} points\n")
            
            f.write("\n" + "="*70 + "\n")
        
        print(f"✅ Rapport sauvegardé dans: performance_report.txt")


def main():
    """
    Fonction principale
    """
    print("\n" + "="*70)
    print("🚀 BACKTEST STRATÉGIE FVG - NQ FUTURES (5 minutes)")
    print("="*70 + "\n")
    
    start_time = datetime.now()
    
    # Répertoire de travail
    base_dir = '/home/runner/work/Backtest-Trading/Backtest-Trading'
    data_file = os.path.join(base_dir, 'NQ_5min.csv')
    
    # Vérifier si le fichier de données existe
    if not os.path.exists(data_file):
        print(f"❌ Fichier de données non trouvé: {data_file}")
        print("⚠️  Veuillez d'abord exécuter 'combine_data.py' pour créer le fichier consolidé.")
        return
    
    # Initialiser le backtester
    backtester = FVGBacktester(
        data_file=data_file,
        tick_value=0.25,
        sl_ticks=5
    )
    
    # Charger les données
    backtester.load_data()
    
    # Exécuter le backtest
    backtester.run_backtest()
    
    # Calculer les métriques de performance
    metrics = backtester.calculate_performance_metrics()
    
    # Afficher le rapport
    backtester.print_performance_report(metrics)
    
    # Sauvegarder les résultats
    backtester.save_results(metrics, base_dir)
    
    # Temps d'exécution
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    print(f"⏱️  Temps d'exécution total: {duration:.2f} secondes")
    
    print("\n✅ Backtest terminé avec succès!\n")


if __name__ == "__main__":
    main()

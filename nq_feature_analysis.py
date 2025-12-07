"""
NQ Feature Analysis - Manipulation vs Continuation/Breakout
===========================================================
This script analyzes trades from the NQ Tokyo-London FVG Inversion strategy
to distinguish "Manipulation" (winning trades) from "Continuation/Breakout" (losing trades)
using statistical feature engineering.

Strategy: SL3 (Signal Candle) + TP 1R
Baseline: 1,618 trades, 64.46% winrate, +557.68 points

Features Extracted:
1. Sweep_Depth: Distance swept beyond Tokyo level (points)
2. Time_Outside: Duration outside Tokyo range (M5 candles)
3. Tokyo_Range_Size: Tokyo session range (points)

Filters Tested:
A. Max Extension Filter (Sweep_Depth)
B. Quick Reversal Filter (Time_Outside)
C. Tokyo Compression Filter (Tokyo_Range_Size)
D. COMBO Filter (all three combined)
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
from typing import List, Dict, Tuple, Optional
import warnings

warnings.filterwarnings('ignore')


class NQFeatureAnalyzer:
    """Feature analysis class for NQ trading strategy"""
    
    # Constantes
    MAX_BARS_LOOKAHEAD = 1000  # Maximum bars pour vérifier TP/SL
    SL3_BUFFER = 0.25  # Buffer en points pour SL3
    START_YEAR = 2018
    END_YEAR = 2026
    
    def __init__(self, data_directory: str):
        """
        Initialiser l'analyseur de features
        
        Args:
            data_directory: Chemin vers le dossier contenant les fichiers CSV
        """
        self.data_directory = data_directory
        self.df = None
        self.all_trades = []
        
    def load_data(self) -> pd.DataFrame:
        """Charger tous les fichiers CSV 5-minute de 2018-2025"""
        print("Chargement des données...")
        all_data = []
        
        for year in range(self.START_YEAR, self.END_YEAR):
            filename = f"{year} 5m.csv"
            filepath = os.path.join(self.data_directory, filename)
            
            if os.path.exists(filepath):
                print(f"  Chargement {filename}...")
                df = pd.read_csv(
                    filepath,
                    sep=';',
                    names=['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume'],
                    skiprows=1,
                    encoding='utf-8-sig'
                )
                all_data.append(df)
            else:
                print(f"  Attention: {filename} non trouvé")
        
        if not all_data:
            raise FileNotFoundError("Aucun fichier de données trouvé!")
        
        # Combiner toutes les données
        combined_df = pd.concat(all_data, ignore_index=True)
        
        # Parser datetime - format DD/MM/YYYY et HH:MM:SS
        combined_df['DateTime'] = pd.to_datetime(
            combined_df['Date'] + ' ' + combined_df['Time'],
            format='%d/%m/%Y %H:%M:%S'
        )
        
        # Convertir les colonnes de prix en float
        for col in ['Open', 'High', 'Low', 'Close']:
            combined_df[col] = pd.to_numeric(combined_df[col], errors='coerce')
        
        # Trier par datetime
        combined_df = combined_df.sort_values('DateTime').reset_index(drop=True)
        
        # Extraire les composants de temps
        combined_df['Date_only'] = combined_df['DateTime'].dt.date
        combined_df['Hour'] = combined_df['DateTime'].dt.hour
        combined_df['Minute'] = combined_df['DateTime'].dt.minute
        
        print(f"Total d'enregistrements chargés: {len(combined_df)}")
        print(f"Plage de dates: {combined_df['DateTime'].min()} to {combined_df['DateTime'].max()}")
        
        self.df = combined_df
        return combined_df
    
    def identify_tokyo_session(self, date) -> Optional[Dict]:
        """
        Identifier la session de Tokyo pour une date donnée (19:00-23:00 jour précédent)
        
        Args:
            date: La date de trading actuelle (Jour N)
            
        Returns:
            Dictionnaire avec Tokyo_High, Tokyo_Low, Tokyo_EQ, ou None si non trouvé
        """
        previous_date = date - timedelta(days=1)
        
        tokyo_data = self.df[
            (self.df['Date_only'] == previous_date) &
            (self.df['Hour'] >= 19) &
            (self.df['Hour'] < 24)
        ]
        
        if len(tokyo_data) == 0:
            return None
        
        tokyo_high = tokyo_data['High'].max()
        tokyo_low = tokyo_data['Low'].min()
        tokyo_eq = (tokyo_high + tokyo_low) / 2
        
        return {
            'Tokyo_High': tokyo_high,
            'Tokyo_Low': tokyo_low,
            'Tokyo_EQ': tokyo_eq,
            'session_date': previous_date
        }
    
    def detect_fvg(self, df_slice: pd.DataFrame, fvg_type: str) -> List[Dict]:
        """
        Détecter les Fair Value Gaps dans les données
        
        Args:
            df_slice: Tranche de DataFrame à analyser
            fvg_type: 'bullish' ou 'bearish'
            
        Returns:
            Liste de dictionnaires FVG avec start_idx, gap_low, gap_high
        """
        fvgs = []
        
        if len(df_slice) < 3:
            return fvgs
        
        df_slice = df_slice.reset_index(drop=True)
        
        for i in range(2, len(df_slice)):
            if fvg_type == 'bullish':
                # Bullish FVG: Low de la bougie (i-2) > High de la bougie (i)
                if df_slice.loc[i-2, 'Low'] > df_slice.loc[i, 'High']:
                    fvgs.append({
                        'idx': i,
                        'gap_low': df_slice.loc[i, 'High'],
                        'gap_high': df_slice.loc[i-2, 'Low'],
                        'datetime': df_slice.loc[i, 'DateTime']
                    })
            elif fvg_type == 'bearish':
                # Bearish FVG: Low de la bougie (i) > High de la bougie (i-2)
                if df_slice.loc[i, 'Low'] > df_slice.loc[i-2, 'High']:
                    fvgs.append({
                        'idx': i,
                        'gap_low': df_slice.loc[i-2, 'High'],
                        'gap_high': df_slice.loc[i, 'Low'],
                        'datetime': df_slice.loc[i, 'DateTime']
                    })
        
        return fvgs
    
    def check_sweep(self, killzone_data: pd.DataFrame, tokyo_high: float, tokyo_low: float) -> Dict:
        """
        Vérifier si le prix balaye Tokyo_High ou Tokyo_Low pendant la killzone
        
        Returns:
            Dictionnaire avec sweep_type ('high', 'low', ou None), sweep_extreme, et sweep_bar_idx
        """
        high_swept = False
        low_swept = False
        sweep_high_extreme = None
        sweep_low_extreme = None
        first_high_sweep_idx = None
        first_low_sweep_idx = None
        
        for idx, row in killzone_data.iterrows():
            # Vérifier si high a été balayé
            if row['High'] > tokyo_high:
                high_swept = True
                if sweep_high_extreme is None or row['High'] > sweep_high_extreme:
                    sweep_high_extreme = row['High']
                if first_high_sweep_idx is None:
                    first_high_sweep_idx = idx
            
            # Vérifier si low a été balayé
            if row['Low'] < tokyo_low:
                low_swept = True
                if sweep_low_extreme is None or row['Low'] < sweep_low_extreme:
                    sweep_low_extreme = row['Low']
                if first_low_sweep_idx is None:
                    first_low_sweep_idx = idx
        
        # Déterminer quel balayage s'est produit en premier
        if high_swept and not low_swept:
            return {
                'sweep_type': 'high',
                'sweep_extreme': sweep_high_extreme,
                'sweep_bar_idx': first_high_sweep_idx
            }
        elif low_swept and not high_swept:
            return {
                'sweep_type': 'low',
                'sweep_extreme': sweep_low_extreme,
                'sweep_bar_idx': first_low_sweep_idx
            }
        elif high_swept and low_swept:
            if first_high_sweep_idx < first_low_sweep_idx:
                return {
                    'sweep_type': 'high',
                    'sweep_extreme': sweep_high_extreme,
                    'sweep_bar_idx': first_high_sweep_idx
                }
            else:
                return {
                    'sweep_type': 'low',
                    'sweep_extreme': sweep_low_extreme,
                    'sweep_bar_idx': first_low_sweep_idx
                }
        
        return {
            'sweep_type': None,
            'sweep_extreme': None,
            'sweep_bar_idx': None
        }
    
    def find_entry_signal(self, killzone_data: pd.DataFrame, sweep_info: Dict, 
                          trade_type: str) -> Optional[Dict]:
        """
        Trouver le signal d'entrée basé sur l'inversion FVG
        
        Args:
            killzone_data: Données pendant la période killzone
            sweep_info: Information sur le balayage
            trade_type: 'short' ou 'long'
            
        Returns:
            Information d'entrée ou None
        """
        killzone_data = killzone_data.reset_index(drop=True)
        
        if trade_type == 'short':
            # Chercher un FVG haussier pendant/après le balayage, puis une bougie fermant en dessous
            fvgs = self.detect_fvg(killzone_data, 'bullish')
            
            for fvg in fvgs:
                # Vérifier les bougies suivantes pour une clôture en dessous du FVG
                for i in range(fvg['idx'] + 1, len(killzone_data)):
                    if killzone_data.loc[i, 'Close'] < fvg['gap_low']:
                        return {
                            'entry_idx': i,
                            'entry_price': killzone_data.loc[i, 'Close'],
                            'entry_datetime': killzone_data.loc[i, 'DateTime'],
                            'signal_candle_high': killzone_data.loc[i, 'High'],
                            'signal_candle_low': killzone_data.loc[i, 'Low'],
                            'fvg': fvg
                        }
        
        elif trade_type == 'long':
            # Chercher un FVG baissier pendant/après le balayage, puis une bougie fermant au-dessus
            fvgs = self.detect_fvg(killzone_data, 'bearish')
            
            for fvg in fvgs:
                # Vérifier les bougies suivantes pour une clôture au-dessus du FVG
                for i in range(fvg['idx'] + 1, len(killzone_data)):
                    if killzone_data.loc[i, 'Close'] > fvg['gap_high']:
                        return {
                            'entry_idx': i,
                            'entry_price': killzone_data.loc[i, 'Close'],
                            'entry_datetime': killzone_data.loc[i, 'DateTime'],
                            'signal_candle_high': killzone_data.loc[i, 'High'],
                            'signal_candle_low': killzone_data.loc[i, 'Low'],
                            'fvg': fvg
                        }
        
        return None
    
    def calculate_sl3(self, entry_info: Dict, trade_type: str) -> float:
        """
        Calculer SL3 (Stop Loss Signal Candle)
        
        Args:
            entry_info: Information d'entrée
            trade_type: 'short' ou 'long'
            
        Returns:
            Niveau de prix SL3
        """
        entry_price = entry_info['entry_price']
        
        if trade_type == 'short':
            # SL3: Signal Candle High + petit buffer
            sl3 = max(entry_info['signal_candle_high'], entry_price) + self.SL3_BUFFER
        else:
            # SL3: Signal Candle Low - petit buffer
            sl3 = min(entry_info['signal_candle_low'], entry_price) - self.SL3_BUFFER
        
        return sl3
    
    def extract_trade_features(self, setup_info: Dict, entry_info: Dict, 
                               killzone_data: pd.DataFrame, trade_type: str) -> Dict:
        """
        Extraire les features pour un trade
        
        Features:
        1. Sweep_Depth: Distance balayée au-delà du niveau Tokyo (points)
        2. Time_Outside: Durée en dehors de la range Tokyo (nombre de bougies M5)
        3. Tokyo_Range_Size: Taille de la range Tokyo (points)
        
        Args:
            setup_info: Information sur le setup (Tokyo levels, sweep info)
            entry_info: Information d'entrée du trade
            killzone_data: Données de la killzone
            trade_type: 'short' ou 'long'
            
        Returns:
            Dictionnaire avec les features extraites
        """
        tokyo_high = setup_info['Tokyo_High']
        tokyo_low = setup_info['Tokyo_Low']
        sweep_extreme = setup_info['sweep_extreme']
        sweep_bar_idx = setup_info['sweep_bar_idx']
        entry_idx = entry_info['entry_idx']
        
        # Feature 1: Sweep_Depth (points)
        if trade_type == 'short':
            # Pour SHORT: Distance entre Tokyo_High et le plus haut atteint pendant le sweep
            sweep_depth = sweep_extreme - tokyo_high
        else:  # long
            # Pour LONG: Distance entre Tokyo_Low et le plus bas atteint pendant le sweep
            sweep_depth = tokyo_low - sweep_extreme
        
        # Feature 2: Time_Outside (nombre de bougies M5)
        # Compter les bougies entre la rupture du niveau Tokyo et la clôture de la bougie signal
        # sweep_bar_idx est l'index dans killzone_data où le sweep a commencé
        # entry_idx est l'index dans killzone_data où l'entrée s'est produite
        time_outside = entry_idx - sweep_bar_idx
        
        # Feature 3: Tokyo_Range_Size (points)
        tokyo_range_size = tokyo_high - tokyo_low
        
        return {
            'Sweep_Depth': round(sweep_depth, 2),
            'Time_Outside': time_outside,
            'Tokyo_Range_Size': round(tokyo_range_size, 2)
        }
    
    def simulate_trade(self, entry_info: Dict, trade_type: str, sl3: float, start_idx: int) -> str:
        """
        Simuler un trade avec SL3 et TP à 1R
        
        Args:
            entry_info: Information d'entrée
            trade_type: 'short' ou 'long'
            sl3: Niveau de stop loss
            start_idx: Index de début dans le DataFrame complet
            
        Returns:
            Résultat: 'win' ou 'loss'
        """
        entry_price = entry_info['entry_price']
        risk = abs(entry_price - sl3)
        
        # Calculer TP à 1R
        if trade_type == 'short':
            tp = entry_price - risk
        else:
            tp = entry_price + risk
        
        # Obtenir les données futures après l'entrée
        end_idx = min(start_idx + self.MAX_BARS_LOOKAHEAD, len(self.df))
        future_data = self.df.iloc[start_idx:end_idx]
        
        if len(future_data) == 0:
            return 'loss'
        
        # Utiliser des opérations vectorisées pour de meilleures performances
        highs = future_data['High'].values
        lows = future_data['Low'].values
        
        for i in range(len(future_data)):
            high = highs[i]
            low = lows[i]
            
            if trade_type == 'short':
                # Vérifier si le stop loss est touché
                if high >= sl3:
                    return 'loss'
                # Vérifier si TP est touché
                if low <= tp:
                    return 'win'
            else:  # long
                # Vérifier si le stop loss est touché
                if low <= sl3:
                    return 'loss'
                # Vérifier si TP est touché
                if high >= tp:
                    return 'win'
        
        # Si on sort de la boucle sans toucher TP ou SL
        return 'loss'
    
    def identify_all_setups(self):
        """
        Identifier tous les setups valides et extraire les features
        """
        print("\n" + "="*70)
        print("IDENTIFICATION DE TOUS LES SETUPS DE TRADING (SL3 + 1R)")
        print("="*70)
        
        if self.df is None:
            self.load_data()
        
        # Obtenir les dates uniques pour l'itération
        unique_dates = sorted(self.df['Date_only'].unique())
        
        print(f"\nAnalyse de {len(unique_dates)} jours de trading...")
        
        processed = 0
        
        for current_date in unique_dates:
            processed += 1
            if processed % 100 == 0:
                print(f"  Traité {processed}/{len(unique_dates)} jours... ({processed/len(unique_dates)*100:.1f}%)")
            
            # Obtenir les niveaux de référence de la session Tokyo (du jour précédent)
            tokyo_levels = self.identify_tokyo_session(current_date)
            
            if tokyo_levels is None:
                continue
            
            # Obtenir les données de la killzone (01:00-04:00 à la date actuelle)
            killzone_data = self.df[
                (self.df['Date_only'] == current_date) &
                (self.df['Hour'] >= 1) &
                (self.df['Hour'] < 4)
            ].copy()
            
            if len(killzone_data) == 0:
                continue
            
            # Vérifier le balayage des niveaux Tokyo
            sweep_info = self.check_sweep(
                killzone_data,
                tokyo_levels['Tokyo_High'],
                tokyo_levels['Tokyo_Low']
            )
            
            if sweep_info['sweep_type'] is None:
                continue
            
            # Déterminer le type de trade basé sur le balayage
            if sweep_info['sweep_type'] == 'high':
                trade_type = 'short'
            else:
                trade_type = 'long'
            
            # Trouver le signal d'entrée
            entry_info = self.find_entry_signal(killzone_data, sweep_info, trade_type)
            
            if entry_info is None:
                continue
            
            # Calculer SL3
            sl3 = self.calculate_sl3(entry_info, trade_type)
            
            # Obtenir l'index dans le DataFrame complet où l'entrée s'est produite
            entry_datetime = entry_info['entry_datetime']
            start_idx = self.df[self.df['DateTime'] == entry_datetime].index[0] + 1
            
            # Simuler le trade
            outcome = self.simulate_trade(entry_info, trade_type, sl3, start_idx)
            
            # Extraire les features
            setup_full_info = {
                'Tokyo_High': tokyo_levels['Tokyo_High'],
                'Tokyo_Low': tokyo_levels['Tokyo_Low'],
                'Tokyo_EQ': tokyo_levels['Tokyo_EQ'],
                'sweep_extreme': sweep_info['sweep_extreme'],
                'sweep_bar_idx': sweep_info['sweep_bar_idx']
            }
            
            # Convertir sweep_bar_idx de l'index global au local dans killzone_data
            killzone_data_reset = killzone_data.reset_index(drop=True)
            global_sweep_idx = sweep_info['sweep_bar_idx']
            local_sweep_idx = None
            for local_idx in range(len(killzone_data_reset)):
                if killzone_data.iloc[local_idx].name == global_sweep_idx:
                    local_sweep_idx = local_idx
                    break
            
            if local_sweep_idx is None:
                local_sweep_idx = 0
            
            setup_full_info['sweep_bar_idx'] = local_sweep_idx
            
            features = self.extract_trade_features(
                setup_full_info,
                entry_info,
                killzone_data_reset,
                trade_type
            )
            
            # Calculer le risque et le profit
            entry_price = entry_info['entry_price']
            risk = abs(entry_price - sl3)
            
            if outcome == 'win':
                profit_points = risk  # 1R
            else:
                profit_points = -risk  # -1R
            
            # Stocker le trade avec les features
            trade = {
                'date': current_date,
                'type': trade_type,
                'entry_price': entry_price,
                'stop_loss': sl3,
                'risk': risk,
                'tokyo_high': tokyo_levels['Tokyo_High'],
                'tokyo_low': tokyo_levels['Tokyo_Low'],
                'tokyo_eq': tokyo_levels['Tokyo_EQ'],
                'entry_datetime': entry_datetime,
                'outcome': outcome,
                'profit_points': profit_points,
                **features
            }
            
            self.all_trades.append(trade)
        
        print(f"\nTotal de trades identifiés: {len(self.all_trades)}")
    
    def analyze_features_by_outcome(self) -> pd.DataFrame:
        """
        Analyser les features par résultat (Winners vs Losers)
        
        Returns:
            DataFrame avec les statistiques comparatives
        """
        print("\n" + "="*70)
        print("ANALYSE STATISTIQUE DES FEATURES")
        print("="*70)
        
        if not self.all_trades:
            print("Aucun trade à analyser!")
            return pd.DataFrame()
        
        df_trades = pd.DataFrame(self.all_trades)
        
        # Séparer winners et losers
        winners = df_trades[df_trades['outcome'] == 'win']
        losers = df_trades[df_trades['outcome'] == 'loss']
        
        print(f"\nWinners: {len(winners)}")
        print(f"Losers: {len(losers)}")
        
        # Calculer les statistiques pour chaque feature
        features = ['Sweep_Depth', 'Time_Outside', 'Tokyo_Range_Size']
        
        stats_data = []
        
        for feature in features:
            # Winners stats
            winners_mean = winners[feature].mean()
            winners_median = winners[feature].median()
            winners_std = winners[feature].std()
            winners_q25 = winners[feature].quantile(0.25)
            winners_q75 = winners[feature].quantile(0.75)
            
            # Losers stats
            losers_mean = losers[feature].mean()
            losers_median = losers[feature].median()
            losers_std = losers[feature].std()
            losers_q25 = losers[feature].quantile(0.25)
            losers_q75 = losers[feature].quantile(0.75)
            
            # Correlation avec outcome (Win=1, Loss=0)
            df_trades['outcome_binary'] = (df_trades['outcome'] == 'win').astype(int)
            correlation = df_trades[feature].corr(df_trades['outcome_binary'])
            
            stats_data.append({
                'Feature': feature,
                'Winners_Mean': round(winners_mean, 2),
                'Winners_Median': round(winners_median, 2),
                'Winners_Std': round(winners_std, 2),
                'Winners_Q25': round(winners_q25, 2),
                'Winners_Q75': round(winners_q75, 2),
                'Losers_Mean': round(losers_mean, 2),
                'Losers_Median': round(losers_median, 2),
                'Losers_Std': round(losers_std, 2),
                'Losers_Q25': round(losers_q25, 2),
                'Losers_Q75': round(losers_q75, 2),
                'Correlation': round(correlation, 4)
            })
        
        stats_df = pd.DataFrame(stats_data)
        
        # Afficher le tableau
        print("\n" + "="*70)
        print("COMPARAISON STATISTIQUE: WINNERS vs LOSERS")
        print("="*70)
        print(stats_df.to_string(index=False))
        
        return stats_df
    
    def test_filters(self, filter_configs: List[Dict]) -> pd.DataFrame:
        """
        Tester différentes configurations de filtres
        
        Args:
            filter_configs: Liste de configurations de filtres à tester
            
        Returns:
            DataFrame avec les résultats de performance pour chaque filtre
        """
        print("\n" + "="*70)
        print("TEST DES FILTRES D'EXCLUSION")
        print("="*70)
        
        if not self.all_trades:
            print("Aucun trade à analyser!")
            return pd.DataFrame()
        
        df_trades = pd.DataFrame(self.all_trades)
        baseline_trades = len(df_trades)
        baseline_wins = len(df_trades[df_trades['outcome'] == 'win'])
        baseline_losses = len(df_trades[df_trades['outcome'] == 'loss'])
        baseline_winrate = (baseline_wins / baseline_trades * 100) if baseline_trades > 0 else 0
        baseline_profit = df_trades['profit_points'].sum()
        
        # Calculer Profit Factor baseline
        gross_profit = df_trades[df_trades['outcome'] == 'win']['profit_points'].sum()
        gross_loss = abs(df_trades[df_trades['outcome'] == 'loss']['profit_points'].sum())
        baseline_pf = (gross_profit / gross_loss) if gross_loss > 0 else 0
        
        # Calculer Max Consecutive Losses baseline
        baseline_max_consec_losses = self._calculate_max_consecutive_losses(df_trades)
        
        results_data = []
        
        # Baseline (sans filtre)
        results_data.append({
            'Filter_Name': 'Baseline (No Filter)',
            'Filter_Threshold': 'N/A',
            'Trades': baseline_trades,
            'Winrate_%': round(baseline_winrate, 2),
            'Net_Profit_Points': round(baseline_profit, 2),
            'Profit_Factor': round(baseline_pf, 2),
            'Max_Consec_Losses': baseline_max_consec_losses,
            'Trade_Retention_%': 100.0,
            'Avg_Sweep_Depth': round(df_trades['Sweep_Depth'].mean(), 2),
            'Avg_Time_Outside': round(df_trades['Time_Outside'].mean(), 2),
            'Avg_Tokyo_Range': round(df_trades['Tokyo_Range_Size'].mean(), 2)
        })
        
        # Tester chaque configuration de filtre
        for config in filter_configs:
            filter_name = config['name']
            filter_type = config['type']
            threshold = config['threshold']
            
            # Appliquer le filtre
            if filter_type == 'max_extension':
                # Exclure si Sweep_Depth > threshold
                filtered_df = df_trades[df_trades['Sweep_Depth'] <= threshold]
            elif filter_type == 'quick_reversal':
                # Exclure si Time_Outside > threshold
                filtered_df = df_trades[df_trades['Time_Outside'] <= threshold]
            elif filter_type == 'tokyo_compression':
                # Exclure si Tokyo_Range_Size < threshold
                filtered_df = df_trades[df_trades['Tokyo_Range_Size'] >= threshold]
            elif filter_type == 'combo':
                # Appliquer les 3 filtres simultanément
                filtered_df = df_trades[
                    (df_trades['Sweep_Depth'] <= config['max_extension']) &
                    (df_trades['Time_Outside'] <= config['quick_reversal']) &
                    (df_trades['Tokyo_Range_Size'] >= config['tokyo_compression'])
                ]
            else:
                continue
            
            # Calculer les statistiques
            num_trades = len(filtered_df)
            if num_trades == 0:
                continue
            
            num_wins = len(filtered_df[filtered_df['outcome'] == 'win'])
            num_losses = len(filtered_df[filtered_df['outcome'] == 'loss'])
            winrate = (num_wins / num_trades * 100) if num_trades > 0 else 0
            net_profit = filtered_df['profit_points'].sum()
            
            # Profit Factor
            gross_profit_f = filtered_df[filtered_df['outcome'] == 'win']['profit_points'].sum()
            gross_loss_f = abs(filtered_df[filtered_df['outcome'] == 'loss']['profit_points'].sum())
            pf = (gross_profit_f / gross_loss_f) if gross_loss_f > 0 else 0
            
            # Max Consecutive Losses
            max_consec_losses = self._calculate_max_consecutive_losses(filtered_df)
            
            # Trade retention
            trade_retention = (num_trades / baseline_trades * 100) if baseline_trades > 0 else 0
            
            # Moyennes des features
            avg_sweep_depth = filtered_df['Sweep_Depth'].mean()
            avg_time_outside = filtered_df['Time_Outside'].mean()
            avg_tokyo_range = filtered_df['Tokyo_Range_Size'].mean()
            
            results_data.append({
                'Filter_Name': filter_name,
                'Filter_Threshold': str(threshold),
                'Trades': num_trades,
                'Winrate_%': round(winrate, 2),
                'Net_Profit_Points': round(net_profit, 2),
                'Profit_Factor': round(pf, 2),
                'Max_Consec_Losses': max_consec_losses,
                'Trade_Retention_%': round(trade_retention, 2),
                'Avg_Sweep_Depth': round(avg_sweep_depth, 2),
                'Avg_Time_Outside': round(avg_time_outside, 2),
                'Avg_Tokyo_Range': round(avg_tokyo_range, 2)
            })
        
        results_df = pd.DataFrame(results_data)
        
        # Afficher le tableau
        print("\n" + "="*70)
        print("RÉSULTATS DE PERFORMANCE PAR FILTRE")
        print("="*70)
        print(results_df.to_string(index=False))
        
        return results_df
    
    def _calculate_max_consecutive_losses(self, df: pd.DataFrame) -> int:
        """
        Calculer le nombre maximum de pertes consécutives
        
        Args:
            df: DataFrame avec les trades
            
        Returns:
            Nombre maximum de pertes consécutives
        """
        max_consecutive = 0
        current_consecutive = 0
        
        for _, row in df.iterrows():
            if row['outcome'] == 'loss':
                current_consecutive += 1
                max_consecutive = max(max_consecutive, current_consecutive)
            else:
                current_consecutive = 0
        
        return max_consecutive
    
    def export_results(self, stats_df: pd.DataFrame, filter_results_df: pd.DataFrame):
        """
        Exporter les résultats vers des fichiers CSV
        
        Args:
            stats_df: DataFrame avec les statistiques des features
            filter_results_df: DataFrame avec les résultats des filtres
        """
        print("\n" + "="*70)
        print("EXPORTATION DES RÉSULTATS")
        print("="*70)
        
        # Exporter les statistiques des features
        stats_output = os.path.join(self.data_directory, 'nq_feature_analysis_statistics.csv')
        stats_df.to_csv(stats_output, index=False, encoding='utf-8-sig')
        print(f"Statistiques des features exportées vers: {stats_output}")
        
        # Exporter les résultats des filtres
        filter_output = os.path.join(self.data_directory, 'nq_feature_filter_results.csv')
        filter_results_df.to_csv(filter_output, index=False, encoding='utf-8-sig')
        print(f"Résultats des filtres exportés vers: {filter_output}")
        
        # Exporter tous les trades avec features
        trades_df = pd.DataFrame(self.all_trades)
        trades_output = os.path.join(self.data_directory, 'nq_feature_analysis_trades.csv')
        trades_df.to_csv(trades_output, index=False, encoding='utf-8-sig')
        print(f"Tous les trades avec features exportés vers: {trades_output}")
    
    def generate_documentation(self, stats_df: pd.DataFrame, filter_results_df: pd.DataFrame):
        """
        Générer la documentation markdown
        
        Args:
            stats_df: DataFrame avec les statistiques des features
            filter_results_df: DataFrame avec les résultats des filtres
        """
        doc_path = os.path.join(self.data_directory, 'FEATURE_ANALYSIS_README.md')
        
        with open(doc_path, 'w', encoding='utf-8') as f:
            f.write("# NQ Feature Analysis - Manipulation vs Continuation/Breakout\n\n")
            f.write("## Overview\n\n")
            f.write("This document presents the results of a comprehensive feature analysis ")
            f.write("to distinguish winning trades (\"Manipulation\") from losing trades ")
            f.write("(\"Continuation/Breakout\") in the NQ Tokyo-London FVG Inversion strategy.\n\n")
            
            f.write("## Strategy Baseline\n\n")
            f.write("- **Strategy**: SL3 (Signal Candle) + TP 1R\n")
            f.write(f"- **Total Trades**: {len(self.all_trades)}\n")
            
            if self.all_trades:
                df_trades = pd.DataFrame(self.all_trades)
                wins = len(df_trades[df_trades['outcome'] == 'win'])
                winrate = (wins / len(self.all_trades) * 100)
                net_profit = df_trades['profit_points'].sum()
                f.write(f"- **Winrate**: {winrate:.2f}%\n")
                f.write(f"- **Net Profit**: {net_profit:.2f} points\n\n")
            
            f.write("## Features Analyzed\n\n")
            f.write("### 1. Sweep_Depth (points)\n")
            f.write("- **Definition**: Distance swept beyond Tokyo level\n")
            f.write("- **For SHORTS**: Distance between Tokyo_High and highest high during sweep\n")
            f.write("- **For LONGS**: Distance between Tokyo_Low and lowest low during sweep\n")
            f.write("- **Hypothesis**: Deep sweeps (>20-30pts) indicate breakout/continuation, not manipulation\n\n")
            
            f.write("### 2. Time_Outside (number of M5 candles)\n")
            f.write("- **Definition**: Count of M5 candles between Tokyo level break and inversion signal candle close\n")
            f.write("- **Hypothesis**: True manipulations are quick (\"Turtle Soup\"). ")
            f.write("Long duration (>12 candles = 1 hour) suggests price acceptance/continuation\n\n")
            
            f.write("### 3. Tokyo_Range_Size (points)\n")
            f.write("- **Definition**: Tokyo session range size (Tokyo_High - Tokyo_Low)\n")
            f.write("- **Hypothesis**: Tiny Tokyo range (<20pts) leads to expansion/continuation. ")
            f.write("Larger Tokyo range more likely to produce manipulation\n\n")
            
            f.write("## Statistical Analysis: Winners vs Losers\n\n")
            f.write("```\n")
            f.write(stats_df.to_string(index=False))
            f.write("\n```\n\n")
            
            f.write("### Key Insights\n\n")
            
            # Analyser les insights basés sur les corrélations
            for _, row in stats_df.iterrows():
                feature = row['Feature']
                corr = row['Correlation']
                winners_mean = row['Winners_Mean']
                losers_mean = row['Losers_Mean']
                
                f.write(f"#### {feature}\n")
                f.write(f"- **Correlation with Win**: {corr:.4f}\n")
                f.write(f"- **Winners Average**: {winners_mean:.2f}\n")
                f.write(f"- **Losers Average**: {losers_mean:.2f}\n")
                
                if corr < -0.05:
                    f.write(f"- **Interpretation**: Negative correlation suggests higher {feature} ")
                    f.write("is associated with losing trades (continuations)\n")
                elif corr > 0.05:
                    f.write(f"- **Interpretation**: Positive correlation suggests higher {feature} ")
                    f.write("is associated with winning trades (manipulations)\n")
                else:
                    f.write("- **Interpretation**: Weak correlation, feature may not be decisive\n")
                f.write("\n")
            
            f.write("## Filter Testing Results\n\n")
            f.write("The following filters were tested to remove \"Continuation\" trades:\n\n")
            f.write("```\n")
            f.write(filter_results_df.to_string(index=False))
            f.write("\n```\n\n")
            
            f.write("### Filter Definitions\n\n")
            f.write("- **Filter A (Max Extension)**: Exclude if Sweep_Depth > X points\n")
            f.write("- **Filter B (Quick Reversal)**: Exclude if Time_Outside > Y candles\n")
            f.write("- **Filter C (Tokyo Compression)**: Exclude if Tokyo_Range_Size < Z points\n")
            f.write("- **Filter D (COMBO)**: Apply best threshold from each of A, B, C simultaneously\n\n")
            
            f.write("## Recommendations\n\n")
            
            # Identifier le meilleur filtre basé sur le profit net
            if len(filter_results_df) > 1:
                best_filter = filter_results_df.iloc[1:].sort_values('Net_Profit_Points', ascending=False).iloc[0]
                f.write(f"### Best Performing Filter\n\n")
                f.write(f"- **Filter**: {best_filter['Filter_Name']}\n")
                f.write(f"- **Threshold**: {best_filter['Filter_Threshold']}\n")
                f.write(f"- **Trades**: {best_filter['Trades']}\n")
                f.write(f"- **Winrate**: {best_filter['Winrate_%']:.2f}%\n")
                f.write(f"- **Net Profit**: {best_filter['Net_Profit_Points']:.2f} points\n")
                f.write(f"- **Profit Factor**: {best_filter['Profit_Factor']:.2f}\n")
                f.write(f"- **Trade Retention**: {best_filter['Trade_Retention_%']:.2f}%\n\n")
            
            f.write("## Data Files Generated\n\n")
            f.write("1. **nq_feature_analysis_statistics.csv**: Feature statistics by outcome (Winners vs Losers)\n")
            f.write("2. **nq_feature_filter_results.csv**: Filter performance comparison\n")
            f.write("3. **nq_feature_analysis_trades.csv**: All trades with extracted features\n")
            f.write("4. **FEATURE_ANALYSIS_README.md**: This documentation file\n\n")
            
            f.write("## Usage\n\n")
            f.write("To run this analysis:\n\n")
            f.write("```bash\n")
            f.write("python nq_feature_analysis.py\n")
            f.write("```\n\n")
            f.write("The script will:\n")
            f.write("1. Load NQ 5-minute data from 2018-2025\n")
            f.write("2. Detect all valid trading setups\n")
            f.write("3. Extract features for each trade\n")
            f.write("4. Perform statistical analysis\n")
            f.write("5. Test multiple filter configurations\n")
            f.write("6. Generate comprehensive reports\n\n")
            
            f.write("## Technical Details\n\n")
            f.write("- **Timezone**: Chicago time (no conversion needed)\n")
            f.write("- **CSV Format**: Semicolon delimiter, DD/MM/YYYY date format, UTF-8-sig encoding\n")
            f.write("- **Tokyo Session**: 19:00-23:00 (previous day)\n")
            f.write("- **London Killzone**: 01:00-04:00 (current day)\n")
            f.write("- **SL3 Buffer**: 0.25 points\n")
            f.write("- **Max Lookahead**: 1000 bars (~3.5 days)\n")
        
        print(f"Documentation générée: {doc_path}")


def main():
    """Fonction d'exécution principale"""
    print("""
    ╔══════════════════════════════════════════════════════════════════╗
    ║     NQ FEATURE ANALYSIS - MANIPULATION vs CONTINUATION           ║
    ║     Tokyo-London FVG Inversion Strategy                          ║
    ╚══════════════════════════════════════════════════════════════════╝
    """)
    
    # Définir le répertoire de données
    data_directory = os.environ.get('NQ_DATA_DIR', os.path.dirname(os.path.abspath(__file__)))
    
    # Initialiser l'analyseur
    analyzer = NQFeatureAnalyzer(data_directory)
    
    # Charger les données
    analyzer.load_data()
    
    # Identifier tous les setups et extraire les features
    analyzer.identify_all_setups()
    
    # Analyser les features par résultat
    stats_df = analyzer.analyze_features_by_outcome()
    
    # Définir les configurations de filtres à tester
    filter_configs = []
    
    # Filter A: Max Extension Filter (Sweep_Depth)
    for threshold in [15, 20, 25, 30]:
        filter_configs.append({
            'name': f'Filter A - Max Extension',
            'type': 'max_extension',
            'threshold': threshold
        })
    
    # Filter B: Quick Reversal Filter (Time_Outside)
    for threshold in [6, 9, 12, 15]:
        filter_configs.append({
            'name': f'Filter B - Quick Reversal',
            'type': 'quick_reversal',
            'threshold': threshold
        })
    
    # Filter C: Tokyo Compression Filter (Tokyo_Range_Size)
    for threshold in [15, 20, 25, 30]:
        filter_configs.append({
            'name': f'Filter C - Tokyo Compression',
            'type': 'tokyo_compression',
            'threshold': threshold
        })
    
    # Filter D: COMBO Filter (best thresholds from each)
    # On va tester quelques combinaisons raisonnables
    combo_configs = [
        {'max_extension': 20, 'quick_reversal': 9, 'tokyo_compression': 20},
        {'max_extension': 25, 'quick_reversal': 12, 'tokyo_compression': 20},
        {'max_extension': 20, 'quick_reversal': 9, 'tokyo_compression': 25},
    ]
    
    for combo in combo_configs:
        filter_configs.append({
            'name': f'Filter D - COMBO',
            'type': 'combo',
            'threshold': f"SD<={combo['max_extension']}, TO<={combo['quick_reversal']}, TR>={combo['tokyo_compression']}",
            **combo
        })
    
    # Tester les filtres
    filter_results_df = analyzer.test_filters(filter_configs)
    
    # Exporter les résultats
    analyzer.export_results(stats_df, filter_results_df)
    
    # Générer la documentation
    analyzer.generate_documentation(stats_df, filter_results_df)
    
    print("\n" + "="*70)
    print("ANALYSE COMPLÈTE")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()

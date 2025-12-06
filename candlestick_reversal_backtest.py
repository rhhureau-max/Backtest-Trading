#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Backtesting - Analyse des Retournements de Tendance
Patterns: Marteau (Hammer) et Étoile Filante (Shooting Star)
Instruments: NQ et ES
Timeframes: 5m et 15m
"""

import pandas as pd
import numpy as np
import os
import json
from datetime import datetime
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')


class CandlestickReversalBacktest:
    """
    Classe principale pour le backtesting des patterns de retournement
    """
    
    def __init__(self, base_path: str = '.'):
        """
        Initialisation du backtester
        
        Args:
            base_path: Chemin vers le répertoire contenant les fichiers CSV
        """
        self.base_path = base_path
        self.results = {
            'NQ': {'5m': {}, '15m': {}},
            'ES': {'5m': {}, '15m': {}}
        }
        
        # Paramètres des patterns
        self.body_position_threshold = 0.3  # 30% du range
        self.wick_to_body_ratio = 2.0  # Mèche au moins 2x le corps
        self.small_wick_threshold = 0.1  # Petite mèche < 10% du range
        
        # Paramètres de tendance
        self.ema_period = 9  # EMA pour la tendance court terme
        self.volume_ma_period = 20  # Moyenne mobile du volume
        self.support_resistance_lookback = 20  # Périodes pour S/R
        
    def load_data(self, instrument: str, timeframe: str, year: int = None) -> pd.DataFrame:
        """
        Charge les données depuis les fichiers CSV
        
        Args:
            instrument: 'NQ' ou 'ES'
            timeframe: '5m' ou '15m'
            year: Année spécifique ou None pour tout charger
            
        Returns:
            DataFrame avec les données OHLCV
        """
        dfs = []
        
        if instrument == 'NQ':
            if year:
                files = [f"{year} {timeframe}.csv"]
            else:
                files = [f"{y} {timeframe}.csv" for y in range(2018, 2026)]
        else:  # ES
            if timeframe == '5m':
                files = ["ES 5m (2018-2020).csv", "ES 5m (2021-2023).csv", "ES 5m (2024-2025).csv"]
            else:  # 15m
                files = ["ES 15m (2018-2025).csv"]
        
        for file in files:
            filepath = os.path.join(self.base_path, file)
            if os.path.exists(filepath):
                try:
                    df = pd.read_csv(filepath, sep=';', encoding='utf-8')
                    
                    # Renommer les colonnes
                    df.columns = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
                    
                    # Créer datetime
                    df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], 
                                                    format='%d/%m/%Y %H:%M:%S')
                    
                    # Convertir en numérique
                    for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
                        df[col] = pd.to_numeric(df[col], errors='coerce')
                    
                    # Supprimer les lignes avec des NaN
                    df = df.dropna()
                    
                    # Garder uniquement les colonnes nécessaires
                    df = df[['DateTime', 'Open', 'High', 'Low', 'Close', 'Volume']]
                    
                    dfs.append(df)
                    print(f"✓ Chargé: {file} ({len(df)} bougies)")
                    
                except Exception as e:
                    print(f"✗ Erreur lors du chargement de {file}: {e}")
        
        if not dfs:
            raise ValueError(f"Aucune donnée trouvée pour {instrument} {timeframe}")
        
        # Combiner tous les DataFrames
        combined_df = pd.concat(dfs, ignore_index=True)
        combined_df = combined_df.sort_values('DateTime').reset_index(drop=True)
        
        # Supprimer les doublons
        combined_df = combined_df.drop_duplicates(subset=['DateTime'], keep='first')
        
        print(f"Total: {len(combined_df)} bougies pour {instrument} {timeframe}")
        
        return combined_df
    
    def calculate_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calcule les indicateurs techniques nécessaires
        
        Args:
            df: DataFrame avec les données OHLCV
            
        Returns:
            DataFrame avec les indicateurs ajoutés
        """
        df = df.copy()
        
        # EMA pour la tendance
        df['EMA'] = df['Close'].ewm(span=self.ema_period, adjust=False).mean()
        
        # Pente de l'EMA (tendance)
        df['EMA_Slope'] = df['EMA'].diff()
        
        # Moyenne mobile du volume
        df['Volume_MA'] = df['Volume'].rolling(window=self.volume_ma_period).mean()
        
        # Support et Résistance (highs/lows récents)
        df['Resistance'] = df['High'].rolling(window=self.support_resistance_lookback).max()
        df['Support'] = df['Low'].rolling(window=self.support_resistance_lookback).min()
        
        # Calcul des composants de la bougie
        df['Body'] = abs(df['Close'] - df['Open'])
        df['Range'] = df['High'] - df['Low']
        df['Upper_Wick'] = df['High'] - df[['Open', 'Close']].max(axis=1)
        df['Lower_Wick'] = df[['Open', 'Close']].min(axis=1) - df['Low']
        
        # Position du corps dans le range
        df['Body_Position'] = (df[['Open', 'Close']].min(axis=1) - df['Low']) / df['Range']
        
        return df
    
    def detect_hammer(self, row: pd.Series) -> bool:
        """
        Détecte un pattern Marteau (Hammer)
        
        Critères:
        - Petit corps situé en haut du range (dans les 30% supérieurs)
        - Longue mèche basse (au moins 2x la taille du corps)
        - Peu ou pas de mèche haute (< 10% du range)
        
        Args:
            row: Ligne du DataFrame
            
        Returns:
            True si c'est un marteau
        """
        if row['Range'] == 0 or row['Body'] == 0:
            return False
        
        # Le corps doit être dans les 30% supérieurs (Body_Position > 0.7)
        body_in_upper = row['Body_Position'] > (1 - self.body_position_threshold)
        
        # Longue mèche basse
        long_lower_wick = row['Lower_Wick'] >= self.wick_to_body_ratio * row['Body']
        
        # Petite mèche haute
        small_upper_wick = row['Upper_Wick'] < self.small_wick_threshold * row['Range']
        
        return body_in_upper and long_lower_wick and small_upper_wick
    
    def detect_shooting_star(self, row: pd.Series) -> bool:
        """
        Détecte un pattern Étoile Filante (Shooting Star)
        
        Critères:
        - Petit corps situé en bas du range (dans les 30% inférieurs)
        - Longue mèche haute (au moins 2x la taille du corps)
        - Peu ou pas de mèche basse (< 10% du range)
        
        Args:
            row: Ligne du DataFrame
            
        Returns:
            True si c'est une étoile filante
        """
        if row['Range'] == 0 or row['Body'] == 0:
            return False
        
        # Le corps doit être dans les 30% inférieurs (Body_Position < 0.3)
        body_in_lower = row['Body_Position'] < self.body_position_threshold
        
        # Longue mèche haute
        long_upper_wick = row['Upper_Wick'] >= self.wick_to_body_ratio * row['Body']
        
        # Petite mèche basse
        small_lower_wick = row['Lower_Wick'] < self.small_wick_threshold * row['Range']
        
        return body_in_lower and long_upper_wick and small_lower_wick
    
    def detect_trend(self, row: pd.Series) -> str:
        """
        Détecte la tendance court terme
        
        Args:
            row: Ligne du DataFrame
            
        Returns:
            'bullish', 'bearish', ou 'neutral'
        """
        if pd.isna(row['EMA']) or pd.isna(row['EMA_Slope']):
            return 'neutral'
        
        # Tendance haussière: prix au-dessus de l'EMA et EMA montante
        if row['Close'] > row['EMA'] and row['EMA_Slope'] > 0:
            return 'bullish'
        
        # Tendance baissière: prix en-dessous de l'EMA et EMA descendante
        elif row['Close'] < row['EMA'] and row['EMA_Slope'] < 0:
            return 'bearish'
        
        return 'neutral'
    
    def is_near_support_resistance(self, row: pd.Series, tolerance: float = 0.005) -> Dict[str, bool]:
        """
        Vérifie si le prix est proche d'un support ou résistance
        
        Args:
            row: Ligne du DataFrame
            tolerance: Tolérance en pourcentage (0.005 = 0.5%)
            
        Returns:
            Dict avec 'near_support' et 'near_resistance'
        """
        near_support = False
        near_resistance = False
        
        if not pd.isna(row['Support']) and not pd.isna(row['Resistance']):
            price = row['Close']
            
            # Proche du support
            if abs(price - row['Support']) / price < tolerance:
                near_support = True
            
            # Proche de la résistance
            if abs(price - row['Resistance']) / price < tolerance:
                near_resistance = True
        
        return {'near_support': near_support, 'near_resistance': near_resistance}
    
    def analyze_reversal(self, df: pd.DataFrame, idx: int, pattern_type: str) -> Dict:
        """
        Analyse le succès d'un retournement après un pattern
        
        Args:
            df: DataFrame complet
            idx: Index du pattern détecté
            pattern_type: 'hammer' ou 'shooting_star'
            
        Returns:
            Dict avec les résultats de l'analyse
        """
        result = {
            'datetime': df.iloc[idx]['DateTime'],
            'pattern': pattern_type,
            'trend': self.detect_trend(df.iloc[idx]),
            'close': df.iloc[idx]['Close'],
            'volume': df.iloc[idx]['Volume'],
            'volume_above_avg': df.iloc[idx]['Volume'] > df.iloc[idx]['Volume_MA'] if not pd.isna(df.iloc[idx]['Volume_MA']) else False,
            'wick_to_body_ratio': df.iloc[idx]['Lower_Wick'] / df.iloc[idx]['Body'] if pattern_type == 'hammer' else df.iloc[idx]['Upper_Wick'] / df.iloc[idx]['Body'],
            'immediate_success': False,
            'two_candle_success': False,
            'three_candle_success': False,
        }
        
        # Vérifier support/résistance
        sr_info = self.is_near_support_resistance(df.iloc[idx])
        result.update(sr_info)
        
        # Analyser les bougies suivantes
        if idx + 1 < len(df):
            next_candle = df.iloc[idx + 1]
            
            if pattern_type == 'hammer':
                # On attend une bougie haussière (retournement à la hausse)
                result['immediate_success'] = next_candle['Close'] > next_candle['Open']
                result['next_candle_gain'] = (next_candle['Close'] - df.iloc[idx]['Close']) / df.iloc[idx]['Close'] * 100
            else:  # shooting_star
                # On attend une bougie baissière (retournement à la baisse)
                result['immediate_success'] = next_candle['Close'] < next_candle['Open']
                result['next_candle_gain'] = (df.iloc[idx]['Close'] - next_candle['Close']) / df.iloc[idx]['Close'] * 100
        
        # Vérifier les 2 bougies suivantes
        if idx + 2 < len(df):
            if pattern_type == 'hammer':
                # Les 2 bougies suivantes doivent être majoritairement haussières
                bullish_count = sum([
                    df.iloc[idx + 1]['Close'] > df.iloc[idx + 1]['Open'],
                    df.iloc[idx + 2]['Close'] > df.iloc[idx + 2]['Open']
                ])
                result['two_candle_success'] = bullish_count >= 1
                result['two_candle_gain'] = (df.iloc[idx + 2]['Close'] - df.iloc[idx]['Close']) / df.iloc[idx]['Close'] * 100
            else:
                # Les 2 bougies suivantes doivent être majoritairement baissières
                bearish_count = sum([
                    df.iloc[idx + 1]['Close'] < df.iloc[idx + 1]['Open'],
                    df.iloc[idx + 2]['Close'] < df.iloc[idx + 2]['Open']
                ])
                result['two_candle_success'] = bearish_count >= 1
                result['two_candle_gain'] = (df.iloc[idx]['Close'] - df.iloc[idx + 2]['Close']) / df.iloc[idx]['Close'] * 100
        
        # Vérifier les 3 bougies suivantes
        if idx + 3 < len(df):
            if pattern_type == 'hammer':
                bullish_count = sum([
                    df.iloc[idx + 1]['Close'] > df.iloc[idx + 1]['Open'],
                    df.iloc[idx + 2]['Close'] > df.iloc[idx + 2]['Open'],
                    df.iloc[idx + 3]['Close'] > df.iloc[idx + 3]['Open']
                ])
                result['three_candle_success'] = bullish_count >= 2
                result['three_candle_gain'] = (df.iloc[idx + 3]['Close'] - df.iloc[idx]['Close']) / df.iloc[idx]['Close'] * 100
            else:
                bearish_count = sum([
                    df.iloc[idx + 1]['Close'] < df.iloc[idx + 1]['Open'],
                    df.iloc[idx + 2]['Close'] < df.iloc[idx + 2]['Open'],
                    df.iloc[idx + 3]['Close'] < df.iloc[idx + 3]['Open']
                ])
                result['three_candle_success'] = bearish_count >= 2
                result['three_candle_gain'] = (df.iloc[idx]['Close'] - df.iloc[idx + 3]['Close']) / df.iloc[idx]['Close'] * 100
        
        return result
    
    def run_backtest(self, instrument: str, timeframe: str) -> Dict:
        """
        Exécute le backtest pour un instrument et timeframe donnés
        
        Args:
            instrument: 'NQ' ou 'ES'
            timeframe: '5m' ou '15m'
            
        Returns:
            Dict avec les résultats du backtest
        """
        print(f"\n{'='*60}")
        print(f"Backtest: {instrument} {timeframe}")
        print(f"{'='*60}")
        
        # Charger les données
        df = self.load_data(instrument, timeframe)
        
        # Calculer les indicateurs
        print("Calcul des indicateurs...")
        df = self.calculate_indicators(df)
        
        # Détection des patterns
        print("Détection des patterns...")
        hammer_signals = []
        shooting_star_signals = []
        
        # Reset index to ensure continuous integer index
        df = df.reset_index(drop=True)
        
        # On commence après la période de warm-up pour les indicateurs
        start_idx = max(self.ema_period, self.volume_ma_period, self.support_resistance_lookback)
        
        for idx in range(start_idx, len(df) - 3):  # -3 pour pouvoir analyser les 3 bougies suivantes
            row = df.iloc[idx]
            trend = self.detect_trend(row)
            
            # Scénario Baissier: Tendance baissière + Marteau
            if trend == 'bearish' and self.detect_hammer(row):
                analysis = self.analyze_reversal(df, idx, 'hammer')
                hammer_signals.append(analysis)
            
            # Scénario Haussier: Tendance haussière + Shooting Star
            if trend == 'bullish' and self.detect_shooting_star(row):
                analysis = self.analyze_reversal(df, idx, 'shooting_star')
                shooting_star_signals.append(analysis)
        
        print(f"✓ Marteaux détectés: {len(hammer_signals)}")
        print(f"✓ Étoiles Filantes détectées: {len(shooting_star_signals)}")
        
        # Calculer les statistiques
        results = {
            'instrument': instrument,
            'timeframe': timeframe,
            'total_candles': len(df),
            'date_range': {
                'start': df['DateTime'].min().strftime('%Y-%m-%d'),
                'end': df['DateTime'].max().strftime('%Y-%m-%d')
            },
            'hammer': self.calculate_statistics(hammer_signals, 'Marteau'),
            'shooting_star': self.calculate_statistics(shooting_star_signals, 'Étoile Filante'),
            'yearly_stats': self.calculate_yearly_statistics(df, hammer_signals, shooting_star_signals)
        }
        
        return results
    
    def calculate_statistics(self, signals: List[Dict], pattern_name: str) -> Dict:
        """
        Calcule les statistiques pour un type de pattern
        
        Args:
            signals: Liste des signaux détectés
            pattern_name: Nom du pattern
            
        Returns:
            Dict avec les statistiques
        """
        if not signals:
            return {
                'total_detected': 0,
                'immediate_success_rate': 0,
                'two_candle_success_rate': 0,
                'three_candle_success_rate': 0
            }
        
        total = len(signals)
        
        # Taux de réussite
        immediate_success = sum(1 for s in signals if s['immediate_success'])
        two_candle_success = sum(1 for s in signals if s.get('two_candle_success', False))
        three_candle_success = sum(1 for s in signals if s.get('three_candle_success', False))
        
        # Avec volume élevé
        high_volume_signals = [s for s in signals if s['volume_above_avg']]
        high_volume_success = sum(1 for s in high_volume_signals if s['immediate_success']) if high_volume_signals else 0
        
        # Près de support/résistance
        near_sr_signals = [s for s in signals if s['near_support'] or s['near_resistance']]
        near_sr_success = sum(1 for s in near_sr_signals if s['immediate_success']) if near_sr_signals else 0
        
        # Wick/Body ratio élevé
        high_ratio_signals = [s for s in signals if s['wick_to_body_ratio'] > 3]
        high_ratio_success = sum(1 for s in high_ratio_signals if s['immediate_success']) if high_ratio_signals else 0
        
        # Gains moyens
        avg_immediate_gain = np.mean([s.get('next_candle_gain', 0) for s in signals if 'next_candle_gain' in s])
        avg_two_candle_gain = np.mean([s.get('two_candle_gain', 0) for s in signals if 'two_candle_gain' in s])
        avg_three_candle_gain = np.mean([s.get('three_candle_gain', 0) for s in signals if 'three_candle_gain' in s])
        
        stats = {
            'pattern_name': pattern_name,
            'total_detected': total,
            'immediate_success': {
                'count': immediate_success,
                'rate': (immediate_success / total * 100) if total > 0 else 0,
                'avg_gain': float(avg_immediate_gain)
            },
            'two_candle_success': {
                'count': two_candle_success,
                'rate': (two_candle_success / total * 100) if total > 0 else 0,
                'avg_gain': float(avg_two_candle_gain)
            },
            'three_candle_success': {
                'count': three_candle_success,
                'rate': (three_candle_success / total * 100) if total > 0 else 0,
                'avg_gain': float(avg_three_candle_gain)
            },
            'context_analysis': {
                'high_volume': {
                    'total': len(high_volume_signals),
                    'success': high_volume_success,
                    'rate': (high_volume_success / len(high_volume_signals) * 100) if high_volume_signals else 0
                },
                'near_support_resistance': {
                    'total': len(near_sr_signals),
                    'success': near_sr_success,
                    'rate': (near_sr_success / len(near_sr_signals) * 100) if near_sr_signals else 0
                },
                'high_wick_ratio': {
                    'total': len(high_ratio_signals),
                    'success': high_ratio_success,
                    'rate': (high_ratio_success / len(high_ratio_signals) * 100) if high_ratio_signals else 0
                }
            }
        }
        
        return stats
    
    def calculate_yearly_statistics(self, df: pd.DataFrame, hammer_signals: List[Dict], 
                                    shooting_star_signals: List[Dict]) -> Dict:
        """
        Calcule les statistiques par année
        
        Args:
            df: DataFrame complet
            hammer_signals: Liste des signaux Marteau
            shooting_star_signals: Liste des signaux Shooting Star
            
        Returns:
            Dict avec les statistiques annuelles
        """
        yearly_stats = {}
        
        # Extraire l'année de chaque signal
        for signal in hammer_signals:
            year = signal['datetime'].year
            if year not in yearly_stats:
                yearly_stats[year] = {'hammer': 0, 'hammer_success': 0, 
                                     'shooting_star': 0, 'shooting_star_success': 0}
            yearly_stats[year]['hammer'] += 1
            if signal['immediate_success']:
                yearly_stats[year]['hammer_success'] += 1
        
        for signal in shooting_star_signals:
            year = signal['datetime'].year
            if year not in yearly_stats:
                yearly_stats[year] = {'hammer': 0, 'hammer_success': 0, 
                                     'shooting_star': 0, 'shooting_star_success': 0}
            yearly_stats[year]['shooting_star'] += 1
            if signal['immediate_success']:
                yearly_stats[year]['shooting_star_success'] += 1
        
        # Calculer les taux de réussite
        for year in yearly_stats:
            stats = yearly_stats[year]
            stats['hammer_rate'] = (stats['hammer_success'] / stats['hammer'] * 100) if stats['hammer'] > 0 else 0
            stats['shooting_star_rate'] = (stats['shooting_star_success'] / stats['shooting_star'] * 100) if stats['shooting_star'] > 0 else 0
        
        return yearly_stats
    
    def run_full_analysis(self):
        """
        Exécute l'analyse complète sur tous les instruments et timeframes
        """
        print("\n" + "="*60)
        print("ANALYSE COMPLÈTE DES RETOURNEMENTS DE TENDANCE")
        print("="*60)
        
        instruments = ['NQ', 'ES']
        timeframes = ['5m', '15m']
        
        for instrument in instruments:
            for timeframe in timeframes:
                try:
                    results = self.run_backtest(instrument, timeframe)
                    self.results[instrument][timeframe] = results
                except Exception as e:
                    print(f"✗ Erreur pour {instrument} {timeframe}: {e}")
                    import traceback
                    traceback.print_exc()
        
        # Générer le rapport
        self.generate_report()
    
    def generate_report(self):
        """
        Génère un rapport détaillé des résultats
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Rapport texte
        report_path = os.path.join(self.base_path, 'backtest_results.txt')
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("="*80 + "\n")
            f.write("RAPPORT D'ANALYSE - RETOURNEMENTS DE TENDANCE\n")
            f.write("Patterns: Marteau (Hammer) et Étoile Filante (Shooting Star)\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*80 + "\n\n")
            
            for instrument in ['NQ', 'ES']:
                f.write(f"\n{'#'*80}\n")
                f.write(f"# INSTRUMENT: {instrument}\n")
                f.write(f"{'#'*80}\n\n")
                
                for timeframe in ['5m', '15m']:
                    if not self.results[instrument][timeframe]:
                        continue
                    
                    results = self.results[instrument][timeframe]
                    
                    f.write(f"\n{'-'*80}\n")
                    f.write(f"TIMEFRAME: {timeframe}\n")
                    f.write(f"{'-'*80}\n")
                    f.write(f"Période: {results['date_range']['start']} à {results['date_range']['end']}\n")
                    f.write(f"Total bougies analysées: {results['total_candles']:,}\n\n")
                    
                    # Statistiques Marteau
                    hammer = results['hammer']
                    f.write(f"\n{'*'*60}\n")
                    f.write(f"PATTERN: {hammer.get('pattern_name', 'Marteau')}\n")
                    f.write(f"{'*'*60}\n")
                    f.write(f"Total détecté: {hammer['total_detected']}\n\n")
                    
                    if hammer['total_detected'] > 0:
                        f.write("TAUX DE RÉUSSITE:\n")
                        f.write(f"  • Immédiat (1 bougie):  {hammer['immediate_success']['rate']:.2f}% "
                               f"({hammer['immediate_success']['count']}/{hammer['total_detected']}) "
                               f"- Gain moyen: {hammer['immediate_success']['avg_gain']:.3f}%\n")
                        f.write(f"  • 2 bougies:            {hammer['two_candle_success']['rate']:.2f}% "
                               f"({hammer['two_candle_success']['count']}/{hammer['total_detected']}) "
                               f"- Gain moyen: {hammer['two_candle_success']['avg_gain']:.3f}%\n")
                        f.write(f"  • 3 bougies:            {hammer['three_candle_success']['rate']:.2f}% "
                               f"({hammer['three_candle_success']['count']}/{hammer['total_detected']}) "
                               f"- Gain moyen: {hammer['three_candle_success']['avg_gain']:.3f}%\n")
                        
                        f.write("\nANALYSE DU CONTEXTE:\n")
                        ctx = hammer['context_analysis']
                        f.write(f"  • Volume élevé:         {ctx['high_volume']['rate']:.2f}% "
                               f"({ctx['high_volume']['success']}/{ctx['high_volume']['total']})\n")
                        f.write(f"  • Près S/R:             {ctx['near_support_resistance']['rate']:.2f}% "
                               f"({ctx['near_support_resistance']['success']}/{ctx['near_support_resistance']['total']})\n")
                        f.write(f"  • Ratio mèche/corps >3: {ctx['high_wick_ratio']['rate']:.2f}% "
                               f"({ctx['high_wick_ratio']['success']}/{ctx['high_wick_ratio']['total']})\n")
                    
                    # Statistiques Shooting Star
                    star = results['shooting_star']
                    f.write(f"\n{'*'*60}\n")
                    f.write(f"PATTERN: {star.get('pattern_name', 'Étoile Filante')}\n")
                    f.write(f"{'*'*60}\n")
                    f.write(f"Total détecté: {star['total_detected']}\n\n")
                    
                    if star['total_detected'] > 0:
                        f.write("TAUX DE RÉUSSITE:\n")
                        f.write(f"  • Immédiat (1 bougie):  {star['immediate_success']['rate']:.2f}% "
                               f"({star['immediate_success']['count']}/{star['total_detected']}) "
                               f"- Gain moyen: {star['immediate_success']['avg_gain']:.3f}%\n")
                        f.write(f"  • 2 bougies:            {star['two_candle_success']['rate']:.2f}% "
                               f"({star['two_candle_success']['count']}/{star['total_detected']}) "
                               f"- Gain moyen: {star['two_candle_success']['avg_gain']:.3f}%\n")
                        f.write(f"  • 3 bougies:            {star['three_candle_success']['rate']:.2f}% "
                               f"({star['three_candle_success']['count']}/{star['total_detected']}) "
                               f"- Gain moyen: {star['three_candle_success']['avg_gain']:.3f}%\n")
                        
                        f.write("\nANALYSE DU CONTEXTE:\n")
                        ctx = star['context_analysis']
                        f.write(f"  • Volume élevé:         {ctx['high_volume']['rate']:.2f}% "
                               f"({ctx['high_volume']['success']}/{ctx['high_volume']['total']})\n")
                        f.write(f"  • Près S/R:             {ctx['near_support_resistance']['rate']:.2f}% "
                               f"({ctx['near_support_resistance']['success']}/{ctx['near_support_resistance']['total']})\n")
                        f.write(f"  • Ratio mèche/corps >3: {ctx['high_wick_ratio']['rate']:.2f}% "
                               f"({ctx['high_wick_ratio']['success']}/{ctx['high_wick_ratio']['total']})\n")
                    
                    # Statistiques annuelles
                    f.write(f"\n{'*'*60}\n")
                    f.write("STATISTIQUES PAR ANNÉE\n")
                    f.write(f"{'*'*60}\n")
                    for year in sorted(results['yearly_stats'].keys()):
                        stats = results['yearly_stats'][year]
                        f.write(f"\n{year}:\n")
                        f.write(f"  Marteau:        {stats['hammer']:3d} détectés, "
                               f"{stats['hammer_success']:3d} réussis ({stats['hammer_rate']:.1f}%)\n")
                        f.write(f"  Étoile Filante: {stats['shooting_star']:3d} détectés, "
                               f"{stats['shooting_star_success']:3d} réussis ({stats['shooting_star_rate']:.1f}%)\n")
            
            # Comparaisons
            f.write(f"\n\n{'='*80}\n")
            f.write("COMPARAISONS\n")
            f.write(f"{'='*80}\n")
            
            # NQ vs ES
            f.write("\nNQ vs ES (5m):\n")
            f.write("-" * 80 + "\n")
            if self.results['NQ']['5m'] and self.results['ES']['5m']:
                nq_5m = self.results['NQ']['5m']
                es_5m = self.results['ES']['5m']
                
                f.write(f"Marteau - Taux de réussite immédiat:\n")
                f.write(f"  NQ: {nq_5m['hammer']['immediate_success']['rate']:.2f}%\n")
                f.write(f"  ES: {es_5m['hammer']['immediate_success']['rate']:.2f}%\n\n")
                
                f.write(f"Étoile Filante - Taux de réussite immédiat:\n")
                f.write(f"  NQ: {nq_5m['shooting_star']['immediate_success']['rate']:.2f}%\n")
                f.write(f"  ES: {es_5m['shooting_star']['immediate_success']['rate']:.2f}%\n")
            
            # 5m vs 15m
            f.write("\n5m vs 15m (NQ):\n")
            f.write("-" * 80 + "\n")
            if self.results['NQ']['5m'] and self.results['NQ']['15m']:
                nq_5m = self.results['NQ']['5m']
                nq_15m = self.results['NQ']['15m']
                
                f.write(f"Marteau - Taux de réussite immédiat:\n")
                f.write(f"  5m:  {nq_5m['hammer']['immediate_success']['rate']:.2f}%\n")
                f.write(f"  15m: {nq_15m['hammer']['immediate_success']['rate']:.2f}%\n\n")
                
                f.write(f"Étoile Filante - Taux de réussite immédiat:\n")
                f.write(f"  5m:  {nq_5m['shooting_star']['immediate_success']['rate']:.2f}%\n")
                f.write(f"  15m: {nq_15m['shooting_star']['immediate_success']['rate']:.2f}%\n")
            
            f.write("\n" + "="*80 + "\n")
            f.write("FIN DU RAPPORT\n")
            f.write("="*80 + "\n")
        
        print(f"\n✓ Rapport texte généré: {report_path}")
        
        # Rapport JSON
        json_path = os.path.join(self.base_path, 'backtest_results.json')
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, default=str)
        
        print(f"✓ Rapport JSON généré: {json_path}")


def main():
    """
    Fonction principale
    """
    print("\n" + "="*80)
    print("BACKTESTING - ANALYSE DES RETOURNEMENTS DE TENDANCE")
    print("Patterns: Marteau (Hammer) et Étoile Filante (Shooting Star)")
    print("="*80 + "\n")
    
    # Créer l'instance du backtester
    backtester = CandlestickReversalBacktest(base_path='.')
    
    # Exécuter l'analyse complète
    backtester.run_full_analysis()
    
    print("\n" + "="*80)
    print("✓ ANALYSE TERMINÉE")
    print("="*80)
    print("\nFichiers générés:")
    print("  • backtest_results.txt  (rapport détaillé)")
    print("  • backtest_results.json (données brutes)")
    print("\n")


if __name__ == "__main__":
    main()

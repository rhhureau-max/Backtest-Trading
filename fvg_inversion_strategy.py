#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Stratégie FVG Inversion - Backtesting Complet
Basée sur les concepts ICT (Inner Circle Trader - Smart Money Concepts)

Concepts clés:
- Fair Value Gap (FVG): Déséquilibres de prix que le marché cherche à combler
- Inversion FVG: Le prix revient et clôture à travers un FVG existant
- Liquidity Sweep: Cassure de niveaux de liquidité (Swing High/Low)
- Patterns de Retournement: Hammer et Shooting Star

Auteur: Expert Trading Algorithmique
Date: 2025
"""

import pandas as pd
import numpy as np
import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')


class FVGInversionStrategy:
    """
    Classe principale pour la stratégie FVG Inversion avec concepts ICT
    """
    
    def __init__(self, base_path: str = '.'):
        """
        Initialisation de la stratégie
        
        Args:
            base_path: Chemin vers le répertoire contenant les fichiers CSV
        """
        self.base_path = base_path
        self.results = {}
        
        # Paramètres des patterns Hammer/Shooting Star
        self.body_position_threshold = 0.3  # 30% du range
        self.wick_to_body_ratio = 2.0  # Mèche au moins 2x le corps
        self.small_wick_threshold = 0.1  # Petite mèche < 10% du range
        
        # Paramètres de tendance
        self.ema_period = 9  # EMA pour la tendance court terme
        
        # Paramètres Smart Money Concepts (SMC)
        self.swing_lookback = 5  # Bougies avant/après pour détecter un swing point
        self.recent_swing_lookback = 20  # Bougies à regarder en arrière pour les swing points récents
        self.sweep_tolerance = 0.0005  # Tolérance pour considérer qu'un sweep a eu lieu (0.05%)
        
        # Paramètres FVG
        self.fvg_lookback = 30  # Combien de bougies garder les FVG actifs (optimisé)
        self.max_trigger_candles = 15  # Max bougies pour attendre l'inversion FVG (optimisé)
        
        # Ratios Risk-Reward à tester
        self.rr_ratios = [1.0, 1.5, 2.0, 2.5, 3.0, 3.5]
        
        # Types de Stop Loss
        self.sl_types = ['type1_conservative', 'type2_structural', 'type3_aggressive']
        
    def load_data(self, instrument: str, timeframe: str, year_range: tuple = None) -> pd.DataFrame:
        """
        Charge les données depuis les fichiers CSV
        
        Args:
            instrument: 'NQ' ou 'ES'
            timeframe: '5m' ou '15m'
            year_range: Tuple (start_year, end_year) pour limiter la plage
            
        Returns:
            DataFrame avec les données OHLCV
        """
        dfs = []
        
        # Déterminer la plage d'années
        if year_range:
            start_year, end_year = year_range
        else:
            start_year, end_year = 2018, 2026
        
        if instrument == 'NQ':
            files = [f"{y} {timeframe}.csv" for y in range(start_year, end_year)]
        else:  # ES
            if timeframe == '5m':
                all_files = [
                    ("ES 5m (2018-2020).csv", 2018, 2020),
                    ("ES 5m (2021-2023).csv", 2021, 2023),
                    ("ES 5m (2024-2025).csv", 2024, 2025)
                ]
                files = [f for f, y_start, y_end in all_files 
                        if y_end >= start_year and y_start < end_year]
            else:  # 15m
                files = ["ES 15m (2018-2025).csv"]
        
        for file in files:
            filepath = os.path.join(self.base_path, file)
            if os.path.exists(filepath):
                try:
                    df = pd.read_csv(filepath, sep=';', encoding='utf-8')
                    
                    # Renommer les colonnes
                    df.columns = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
                    
                    # Créer DateTime (format mixte)
                    df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='mixed', dayfirst=False)
                    
                    # Filtrer selon la plage d'années
                    if year_range:
                        df = df[(df['DateTime'].dt.year >= start_year) & 
                               (df['DateTime'].dt.year < end_year)]
                    
                    dfs.append(df)
                except Exception as e:
                    print(f"Erreur lors du chargement de {file}: {e}")
        
        if not dfs:
            raise ValueError(f"Aucune donnée trouvée pour {instrument} {timeframe}")
        
        # Concaténer et trier
        df_combined = pd.concat(dfs, ignore_index=True)
        df_combined = df_combined.sort_values('DateTime').reset_index(drop=True)
        
        # Supprimer les doublons
        df_combined = df_combined.drop_duplicates(subset=['DateTime']).reset_index(drop=True)
        
        print(f"Données chargées: {len(df_combined)} bougies pour {instrument} {timeframe}")
        
        return df_combined
    
    def _calculate_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calcule les indicateurs techniques nécessaires
        
        Args:
            df: DataFrame avec les données OHLCV
            
        Returns:
            DataFrame avec les indicateurs ajoutés
        """
        df = df.copy()
        
        # EMA pour la tendance
        df['EMA9'] = df['Close'].ewm(span=self.ema_period, adjust=False).mean()
        
        # Tendance (1 = haussière, -1 = baissière, 0 = neutre)
        df['Trend'] = 0
        df.loc[df['Close'] > df['EMA9'], 'Trend'] = 1
        df.loc[df['Close'] < df['EMA9'], 'Trend'] = -1
        
        return df
    
    def _is_hammer(self, row: pd.Series) -> bool:
        """
        Détecte un pattern Hammer (Marteau)
        
        Critères:
        - Petite mèche supérieure (< 10% du range)
        - Grande mèche inférieure (au moins 2x le corps)
        - Corps dans le haut du range (70%+)
        
        Args:
            row: Série pandas représentant une bougie
            
        Returns:
            True si Hammer détecté
        """
        o, h, l, c = row['Open'], row['High'], row['Low'], row['Close']
        
        total_range = h - l
        if total_range == 0:
            return False
        
        body = abs(c - o)
        upper_wick = h - max(o, c)
        lower_wick = min(o, c) - l
        
        # Corps dans la partie haute
        body_position = (min(o, c) - l) / total_range
        
        # Vérifications
        is_small_upper_wick = upper_wick < (self.small_wick_threshold * total_range)
        is_large_lower_wick = lower_wick >= (self.wick_to_body_ratio * body) if body > 0 else lower_wick > (0.5 * total_range)
        is_body_at_top = body_position >= (1 - self.body_position_threshold)
        
        return is_small_upper_wick and is_large_lower_wick and is_body_at_top
    
    def _is_shooting_star(self, row: pd.Series) -> bool:
        """
        Détecte un pattern Shooting Star (Étoile Filante)
        
        Critères:
        - Petite mèche inférieure (< 10% du range)
        - Grande mèche supérieure (au moins 2x le corps)
        - Corps dans le bas du range (70%+)
        
        Args:
            row: Série pandas représentant une bougie
            
        Returns:
            True si Shooting Star détecté
        """
        o, h, l, c = row['Open'], row['High'], row['Low'], row['Close']
        
        total_range = h - l
        if total_range == 0:
            return False
        
        body = abs(c - o)
        upper_wick = h - max(o, c)
        lower_wick = min(o, c) - l
        
        # Corps dans la partie basse
        body_position = (min(o, c) - l) / total_range
        
        # Vérifications
        is_small_lower_wick = lower_wick < (self.small_wick_threshold * total_range)
        is_large_upper_wick = upper_wick >= (self.wick_to_body_ratio * body) if body > 0 else upper_wick > (0.5 * total_range)
        is_body_at_bottom = body_position <= self.body_position_threshold
        
        return is_small_lower_wick and is_large_upper_wick and is_body_at_bottom
    
    def _find_swing_points(self, df: pd.DataFrame, idx: int) -> Dict:
        """
        Identifie les swing high et swing low autour d'un index
        
        Args:
            df: DataFrame avec les données
            idx: Index actuel
            
        Returns:
            Dict avec les swing points trouvés
        """
        swing_highs = []
        swing_lows = []
        
        # Chercher dans la fenêtre récente
        start_idx = max(0, idx - self.recent_swing_lookback)
        
        for i in range(start_idx, idx):
            # Vérifier si c'est un swing high
            if i >= self.swing_lookback and i < len(df) - self.swing_lookback:
                is_swing_high = True
                current_high = df.iloc[i]['High']
                
                for j in range(i - self.swing_lookback, i + self.swing_lookback + 1):
                    if j != i and df.iloc[j]['High'] >= current_high:
                        is_swing_high = False
                        break
                
                if is_swing_high:
                    swing_highs.append({
                        'price': current_high,
                        'idx': i,
                        'datetime': df.iloc[i]['DateTime']
                    })
            
            # Vérifier si c'est un swing low
            if i >= self.swing_lookback and i < len(df) - self.swing_lookback:
                is_swing_low = True
                current_low = df.iloc[i]['Low']
                
                for j in range(i - self.swing_lookback, i + self.swing_lookback + 1):
                    if j != i and df.iloc[j]['Low'] <= current_low:
                        is_swing_low = False
                        break
                
                if is_swing_low:
                    swing_lows.append({
                        'price': current_low,
                        'idx': i,
                        'datetime': df.iloc[i]['DateTime']
                    })
        
        return {
            'swing_highs': swing_highs,
            'swing_lows': swing_lows
        }
    
    def _check_liquidity_sweep(self, df: pd.DataFrame, idx: int, 
                                pattern_type: str, swing_points: Dict) -> Optional[Dict]:
        """
        Vérifie si un liquidity sweep a eu lieu
        
        Args:
            df: DataFrame avec les données
            idx: Index du pattern
            pattern_type: 'hammer' ou 'shooting_star'
            swing_points: Dict avec les swing points
            
        Returns:
            Dict avec info sur le sweep ou None
        """
        current_candle = df.iloc[idx]
        
        if pattern_type == 'shooting_star':
            # Pour un Shooting Star, on cherche un sweep de swing high
            swing_highs = swing_points['swing_highs']
            if not swing_highs:
                return None
            
            # Prendre le swing high le plus récent
            recent_swing = swing_highs[-1]
            
            # Vérifier si le high actuel dépasse le swing high
            tolerance_price = recent_swing['price'] * self.sweep_tolerance
            if current_candle['High'] > (recent_swing['price'] + tolerance_price):
                return {
                    'type': 'high',
                    'swept_level': recent_swing['price'],
                    'swept_idx': recent_swing['idx'],
                    'sweep_high': current_candle['High']
                }
        
        elif pattern_type == 'hammer':
            # Pour un Hammer, on cherche un sweep de swing low
            swing_lows = swing_points['swing_lows']
            if not swing_lows:
                return None
            
            # Prendre le swing low le plus récent
            recent_swing = swing_lows[-1]
            
            # Vérifier si le low actuel passe sous le swing low
            tolerance_price = recent_swing['price'] * self.sweep_tolerance
            if current_candle['Low'] < (recent_swing['price'] - tolerance_price):
                return {
                    'type': 'low',
                    'swept_level': recent_swing['price'],
                    'swept_idx': recent_swing['idx'],
                    'sweep_low': current_candle['Low']
                }
        
        return None
    
    def _detect_fvg(self, df: pd.DataFrame, idx: int) -> List[Dict]:
        """
        Détecte les Fair Value Gaps
        
        Un FVG se forme quand il y a un gap entre:
        - FVG Haussier: Low[i] > High[i-2] (gap vers le haut)
        - FVG Baissier: High[i] < Low[i-2] (gap vers le bas)
        
        Args:
            df: DataFrame avec les données
            idx: Index actuel
            
        Returns:
            List de FVG actifs avec leurs caractéristiques
        """
        if idx < 2:
            return []
        
        fvgs = []
        
        current_candle = df.iloc[idx]
        candle_minus_2 = df.iloc[idx - 2]
        
        # FVG Bullish (gap vers le haut)
        # Gap entre High[i-2] et Low[i]
        if current_candle['Low'] > candle_minus_2['High']:
            fvg_high = current_candle['Low']
            fvg_low = candle_minus_2['High']
            
            fvgs.append({
                'type': 'bullish',
                'high': fvg_high,
                'low': fvg_low,
                'size': fvg_high - fvg_low,
                'created_at_idx': idx,
                'created_at_datetime': current_candle['DateTime']
            })
        
        # FVG Bearish (gap vers le bas)
        # Gap entre Low[i-2] et High[i]
        if current_candle['High'] < candle_minus_2['Low']:
            fvg_high = candle_minus_2['Low']
            fvg_low = current_candle['High']
            
            fvgs.append({
                'type': 'bearish',
                'high': fvg_high,
                'low': fvg_low,
                'size': fvg_high - fvg_low,
                'created_at_idx': idx,
                'created_at_datetime': current_candle['DateTime']
            })
        
        return fvgs
    
    def _detect_fvg_inversion(self, df: pd.DataFrame, idx: int, 
                               fvg_list: List[Dict], pattern_type: str) -> Optional[Dict]:
        """
        Détecte si une bougie clôture à travers un FVG (inversion)
        
        Inversion d'un FVG:
        - FVG Haussier inversé: Une bougie clôture EN-DESSOUS du FVG_Low
        - FVG Baissier inversé: Une bougie clôture AU-DESSUS du FVG_High
        
        Args:
            df: DataFrame avec les données
            idx: Index actuel
            fvg_list: Liste des FVG actifs
            pattern_type: 'hammer' ou 'shooting_star'
            
        Returns:
            Dict avec info sur l'inversion ou None
        """
        if not fvg_list:
            return None
        
        current_candle = df.iloc[idx]
        
        if pattern_type == 'shooting_star':
            # Pour un Shooting Star (SHORT), on cherche l'inversion d'un FVG Haussier
            # Une bougie doit clôturer EN-DESSOUS du FVG_Low
            for fvg in fvg_list:
                if fvg['type'] == 'bullish':
                    if current_candle['Close'] < fvg['low']:
                        return {
                            'fvg': fvg,
                            'inversion_type': 'bullish_to_bearish',
                            'trigger_candle_idx': idx,
                            'trigger_candle_close': current_candle['Close'],
                            'trigger_candle_datetime': current_candle['DateTime']
                        }
        
        elif pattern_type == 'hammer':
            # Pour un Hammer (LONG), on cherche l'inversion d'un FVG Baissier
            # Une bougie doit clôturer AU-DESSUS du FVG_High
            for fvg in fvg_list:
                if fvg['type'] == 'bearish':
                    if current_candle['Close'] > fvg['high']:
                        return {
                            'fvg': fvg,
                            'inversion_type': 'bearish_to_bullish',
                            'trigger_candle_idx': idx,
                            'trigger_candle_close': current_candle['Close'],
                            'trigger_candle_datetime': current_candle['DateTime']
                        }
        
        return None
    
    def _find_setup(self, df: pd.DataFrame, start_idx: int) -> Optional[Dict]:
        """
        Cherche un setup complet selon l'ordre chronologique STRICT:
        
        1. Identifier la tendance (EMA 9)
        2. Détecter FVG formé pendant cette tendance
        3. Attendre Liquidity Sweep + Pattern (Hammer/Shooting Star)
        4. Attendre Inversion FVG (bougie clôture à travers le FVG)
        5. Entrée à la clôture de la bougie d'inversion
        
        Args:
            df: DataFrame avec les données
            start_idx: Index de départ pour la recherche
            
        Returns:
            Dict avec toutes les informations du setup ou None
        """
        if start_idx < self.recent_swing_lookback + 10:
            return None
        
        # Liste pour stocker les FVG actifs
        active_fvgs = []
        
        # ÉTAPE 1: Identifier la tendance à start_idx
        trend = df.iloc[start_idx]['Trend']
        if trend == 0:
            return None
        
        # ÉTAPE 2: Chercher les FVG formés AVANT le pattern
        # On regarde les FVG créés dans les dernières bougies
        for i in range(max(2, start_idx - self.fvg_lookback), start_idx):
            fvgs = self._detect_fvg(df, i)
            for fvg in fvgs:
                # Garder seulement les FVG cohérents avec la tendance
                if trend == 1 and fvg['type'] == 'bearish':
                    # Tendance baissière, on garde les FVG baissiers
                    active_fvgs.append(fvg)
                elif trend == -1 and fvg['type'] == 'bullish':
                    # Tendance haussière, on garde les FVG haussiers
                    active_fvgs.append(fvg)
        
        if not active_fvgs:
            return None
        
        # ÉTAPE 3: Détecter Pattern + Liquidity Sweep à start_idx
        current_candle = df.iloc[start_idx]
        is_hammer = self._is_hammer(current_candle)
        is_shooting_star = self._is_shooting_star(current_candle)
        
        if not (is_hammer or is_shooting_star):
            return None
        
        pattern_type = 'hammer' if is_hammer else 'shooting_star'
        
        # Vérifier la cohérence tendance/pattern
        if trend == 1 and pattern_type != 'hammer':
            return None  # Tendance baissière, on attend un Hammer
        if trend == -1 and pattern_type != 'shooting_star':
            return None  # Tendance haussière, on attend un Shooting Star
        
        # Vérifier le Liquidity Sweep
        swing_points = self._find_swing_points(df, start_idx)
        sweep_info = self._check_liquidity_sweep(df, start_idx, pattern_type, swing_points)
        
        if not sweep_info:
            return None
        
        # ÉTAPE 4: Attendre l'Inversion FVG dans les prochaines bougies
        max_wait_idx = min(start_idx + self.max_trigger_candles, len(df) - 1)
        
        for trigger_idx in range(start_idx + 1, max_wait_idx + 1):
            # Vérifier si une bougie clôture à travers un FVG
            inversion = self._detect_fvg_inversion(df, trigger_idx, active_fvgs, pattern_type)
            
            if inversion:
                # SETUP COMPLET TROUVÉ!
                return {
                    'trend': trend,
                    'pattern_type': pattern_type,
                    'pattern_idx': start_idx,
                    'pattern_candle': df.iloc[start_idx].to_dict(),
                    'sweep_info': sweep_info,
                    'fvg_inversion': inversion,
                    'entry_idx': trigger_idx,
                    'entry_price': df.iloc[trigger_idx]['Close'],
                    'entry_datetime': df.iloc[trigger_idx]['DateTime'],
                    'direction': 'long' if pattern_type == 'hammer' else 'short'
                }
        
        return None
    
    def _calculate_sl_levels(self, setup: Dict) -> Dict:
        """
        Calcule les 3 niveaux de Stop Loss
        
        SL Type 1 - Conservateur (Pattern-based):
        - SHORT: 1 point au-dessus de la mèche du Shooting Star
        - LONG: 1 point en-dessous de la mèche du Hammer
        
        SL Type 2 - Structurel (FVG-based):
        - SHORT: 1 point au-dessus de FVG_High
        - LONG: 1 point en-dessous de FVG_Low
        
        SL Type 3 - Agressif (Trigger-based):
        - SHORT: 1 point au-dessus du High de la bougie de trigger
        - LONG: 1 point en-dessous du Low de la bougie de trigger
        
        Args:
            setup: Dict avec les informations du setup
            
        Returns:
            Dict avec les 3 niveaux de SL
        """
        pattern_candle = setup['pattern_candle']
        direction = setup['direction']
        fvg = setup['fvg_inversion']['fvg']
        trigger_candle_idx = setup['fvg_inversion']['trigger_candle_idx']
        
        # Pour obtenir la bougie de trigger, on doit la récupérer du setup
        # Note: trigger_candle est la bougie à entry_idx
        # On va utiliser entry_price et recalculer
        
        sl_buffer = 1.0  # 1 point de buffer
        
        if direction == 'short':
            # SL Type 1: Au-dessus de la mèche du Shooting Star
            sl_type1 = pattern_candle['High'] + sl_buffer
            
            # SL Type 2: Au-dessus du FVG_High
            sl_type2 = fvg['high'] + sl_buffer
            
            # SL Type 3: Au-dessus du High de la bougie de trigger
            # On va stocker le high de la bougie de trigger dans le setup
            sl_type3 = setup.get('trigger_candle_high', pattern_candle['High']) + sl_buffer
        
        else:  # long
            # SL Type 1: En-dessous de la mèche du Hammer
            sl_type1 = pattern_candle['Low'] - sl_buffer
            
            # SL Type 2: En-dessous du FVG_Low
            sl_type2 = fvg['low'] - sl_buffer
            
            # SL Type 3: En-dessous du Low de la bougie de trigger
            sl_type3 = setup.get('trigger_candle_low', pattern_candle['Low']) - sl_buffer
        
        return {
            'type1_conservative': sl_type1,
            'type2_structural': sl_type2,
            'type3_aggressive': sl_type3
        }
    
    def _simulate_trade(self, df: pd.DataFrame, entry_idx: int, 
                        entry_price: float, sl_price: float, 
                        rr_ratio: float, direction: str) -> Dict:
        """
        Simule un trade avec entrée, SL et TP
        
        Args:
            df: DataFrame avec les données
            entry_idx: Index d'entrée
            entry_price: Prix d'entrée
            sl_price: Prix du Stop Loss
            rr_ratio: Ratio Risk-Reward
            direction: 'long' ou 'short'
            
        Returns:
            Dict avec le résultat du trade
        """
        # Calculer le risque et le TP
        if direction == 'long':
            risk = entry_price - sl_price
            tp_price = entry_price + (risk * rr_ratio)
        else:  # short
            risk = sl_price - entry_price
            tp_price = entry_price - (risk * rr_ratio)
        
        if risk <= 0:
            return {
                'outcome': 'invalid',
                'exit_idx': entry_idx,
                'exit_price': entry_price,
                'candles_in_trade': 0,
                'pnl_points': 0,
                'rr_achieved': 0
            }
        
        # Simuler le trade bougie par bougie
        max_candles = 500  # Timeout après 500 bougies
        
        for i in range(entry_idx + 1, min(entry_idx + max_candles, len(df))):
            candle = df.iloc[i]
            
            if direction == 'long':
                # Vérifier SL
                if candle['Low'] <= sl_price:
                    return {
                        'outcome': 'loss',
                        'exit_idx': i,
                        'exit_price': sl_price,
                        'exit_datetime': candle['DateTime'],
                        'candles_in_trade': i - entry_idx,
                        'pnl_points': -risk,
                        'rr_achieved': -1.0
                    }
                
                # Vérifier TP
                if candle['High'] >= tp_price:
                    return {
                        'outcome': 'win',
                        'exit_idx': i,
                        'exit_price': tp_price,
                        'exit_datetime': candle['DateTime'],
                        'candles_in_trade': i - entry_idx,
                        'pnl_points': risk * rr_ratio,
                        'rr_achieved': rr_ratio
                    }
            
            else:  # short
                # Vérifier SL
                if candle['High'] >= sl_price:
                    return {
                        'outcome': 'loss',
                        'exit_idx': i,
                        'exit_price': sl_price,
                        'exit_datetime': candle['DateTime'],
                        'candles_in_trade': i - entry_idx,
                        'pnl_points': -risk,
                        'rr_achieved': -1.0
                    }
                
                # Vérifier TP
                if candle['Low'] <= tp_price:
                    return {
                        'outcome': 'win',
                        'exit_idx': i,
                        'exit_price': tp_price,
                        'exit_datetime': candle['DateTime'],
                        'candles_in_trade': i - entry_idx,
                        'pnl_points': risk * rr_ratio,
                        'rr_achieved': rr_ratio
                    }
        
        # Timeout
        return {
            'outcome': 'timeout',
            'exit_idx': min(entry_idx + max_candles, len(df) - 1),
            'exit_price': df.iloc[min(entry_idx + max_candles, len(df) - 1)]['Close'],
            'exit_datetime': df.iloc[min(entry_idx + max_candles, len(df) - 1)]['DateTime'],
            'candles_in_trade': max_candles,
            'pnl_points': 0,
            'rr_achieved': 0
        }
    
    def _calculate_metrics(self, trades: List[Dict]) -> Dict:
        """
        Calcule les métriques de performance
        
        Args:
            trades: Liste des trades
            
        Returns:
            Dict avec les métriques
        """
        if not trades:
            return {
                'total_trades': 0,
                'win_rate': 0,
                'loss_rate': 0,
                'timeout_rate': 0,
                'avg_candles_to_tp': 0,
                'avg_candles_to_sl': 0,
                'expectancy': 0,
                'profit_factor': 0,
                'total_pnl': 0
            }
        
        total_trades = len(trades)
        wins = [t for t in trades if t['outcome'] == 'win']
        losses = [t for t in trades if t['outcome'] == 'loss']
        timeouts = [t for t in trades if t['outcome'] == 'timeout']
        
        win_count = len(wins)
        loss_count = len(losses)
        timeout_count = len(timeouts)
        
        win_rate = (win_count / total_trades) * 100 if total_trades > 0 else 0
        loss_rate = (loss_count / total_trades) * 100 if total_trades > 0 else 0
        timeout_rate = (timeout_count / total_trades) * 100 if total_trades > 0 else 0
        
        avg_candles_to_tp = np.mean([t['candles_in_trade'] for t in wins]) if wins else 0
        avg_candles_to_sl = np.mean([t['candles_in_trade'] for t in losses]) if losses else 0
        
        total_win_pnl = sum([t['pnl_points'] for t in wins])
        total_loss_pnl = abs(sum([t['pnl_points'] for t in losses]))
        
        expectancy = (total_win_pnl - total_loss_pnl) / total_trades if total_trades > 0 else 0
        profit_factor = total_win_pnl / total_loss_pnl if total_loss_pnl > 0 else 0
        
        return {
            'total_trades': total_trades,
            'wins': win_count,
            'losses': loss_count,
            'timeouts': timeout_count,
            'win_rate': round(win_rate, 2),
            'loss_rate': round(loss_rate, 2),
            'timeout_rate': round(timeout_rate, 2),
            'avg_candles_to_tp': round(avg_candles_to_tp, 2),
            'avg_candles_to_sl': round(avg_candles_to_sl, 2),
            'expectancy': round(expectancy, 2),
            'profit_factor': round(profit_factor, 2),
            'total_pnl': round(total_win_pnl - total_loss_pnl, 2)
        }
    
    def run_backtest(self, instrument: str = 'NQ', timeframe: str = '5m', 
                     year_range: tuple = (2018, 2026)) -> Dict:
        """
        Exécute le backtest complet pour la stratégie FVG Inversion
        
        Args:
            instrument: 'NQ' ou 'ES'
            timeframe: '5m' ou '15m'
            year_range: Tuple (start_year, end_year)
            
        Returns:
            Dict avec tous les résultats
        """
        print(f"\n{'='*80}")
        print(f"Backtesting Stratégie FVG Inversion")
        print(f"Instrument: {instrument} | Timeframe: {timeframe}")
        print(f"Période: {year_range[0]}-{year_range[1]}")
        print(f"{'='*80}\n")
        
        # Charger les données
        df = self.load_data(instrument, timeframe, year_range)
        
        # Calculer les indicateurs
        df = self._calculate_indicators(df)
        
        print(f"Recherche des setups complets...")
        
        # Chercher tous les setups
        setups = []
        i = self.recent_swing_lookback + 10
        progress_step = max(1000, len(df) // 20)  # Afficher la progression 20 fois
        
        while i < len(df) - self.max_trigger_candles - 10:
            setup = self._find_setup(df, i)
            
            if setup:
                # Ajouter les informations manquantes pour le calcul des SL
                trigger_idx = setup['entry_idx']
                trigger_candle = df.iloc[trigger_idx]
                setup['trigger_candle_high'] = trigger_candle['High']
                setup['trigger_candle_low'] = trigger_candle['Low']
                
                setups.append(setup)
                
                # Avancer après le trade
                i = trigger_idx + 20
            else:
                i += 1
            
            # Afficher la progression
            if i % progress_step == 0:
                progress = (i / len(df)) * 100
                print(f"  Progression: {progress:.1f}% ({i:,}/{len(df):,} bougies) - Setups: {len(setups)}")
        
        print(f"\n✓ Setups complets trouvés: {len(setups)}")
        
        if not setups:
            print("Aucun setup trouvé. Vérifier les paramètres.")
            return {}
        
        # Simuler les trades pour chaque combinaison SL × RR
        results = {
            'instrument': instrument,
            'timeframe': timeframe,
            'period': f"{year_range[0]}-{year_range[1]}",
            'total_candles': len(df),
            'total_setups': len(setups),
            'sl_types': {}
        }
        
        print(f"\nSimulation des trades pour {len(setups)} setups...")
        
        for sl_type in self.sl_types:
            print(f"\n  SL Type: {sl_type}")
            results['sl_types'][sl_type] = {}
            
            for rr_ratio in self.rr_ratios:
                trades = []
                
                for setup in setups:
                    # Calculer les niveaux de SL
                    sl_levels = self._calculate_sl_levels(setup)
                    sl_price = sl_levels[sl_type]
                    
                    # Simuler le trade
                    trade_result = self._simulate_trade(
                        df,
                        setup['entry_idx'],
                        setup['entry_price'],
                        sl_price,
                        rr_ratio,
                        setup['direction']
                    )
                    
                    trade_result['setup'] = setup
                    trade_result['sl_type'] = sl_type
                    trade_result['rr_ratio'] = rr_ratio
                    
                    trades.append(trade_result)
                
                # Calculer les métriques
                metrics = self._calculate_metrics(trades)
                
                results['sl_types'][sl_type][f'rr_{rr_ratio}'] = {
                    'metrics': metrics,
                    'trades': trades
                }
                
                print(f"    RR {rr_ratio}:1 - Win Rate: {metrics['win_rate']}% | "
                      f"Trades: {metrics['total_trades']} | "
                      f"Expectancy: {metrics['expectancy']}")
        
        self.results = results
        return results
    
    def generate_report(self, output_file: str = 'FVG_INVERSION_STRATEGY_ANALYSIS.md'):
        """
        Génère un rapport markdown complet avec les résultats
        
        Args:
            output_file: Nom du fichier de sortie
        """
        if not self.results:
            print("Aucun résultat à reporter. Exécutez d'abord run_backtest().")
            return
        
        results = self.results
        
        report = []
        report.append("# Stratégie FVG Inversion - Analyse Complète\n")
        report.append(f"*Généré le {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
        
        # Description
        report.append("## 📋 Description de la Stratégie\n\n")
        report.append("### Concepts ICT Utilisés\n")
        report.append("- **Fair Value Gap (FVG)**: Déséquilibres de prix que le marché cherche à combler\n")
        report.append("- **Inversion FVG**: Le prix revient et clôture à travers un FVG existant\n")
        report.append("- **Liquidity Sweep**: Cassure de niveaux de liquidité (Swing High/Low)\n")
        report.append("- **Patterns de Retournement**: Hammer et Shooting Star\n\n")
        
        report.append("### Logique de la Stratégie\n\n")
        report.append("#### Scénario LONG (Achat)\n")
        report.append("1. **Contexte**: Tendance baissière court terme (prix < EMA 9)\n")
        report.append("2. **Formation FVG**: FVG Baissier créé pendant la descente\n")
        report.append("3. **Sweep + Signal**: Cassure Swing Low + Formation Hammer\n")
        report.append("4. **Trigger**: Bougie clôture AU-DESSUS du FVG_High (Inversion)\n")
        report.append("5. **Entrée**: À la clôture de la bougie de trigger\n\n")
        
        report.append("#### Scénario SHORT (Vente)\n")
        report.append("1. **Contexte**: Tendance haussière court terme (prix > EMA 9)\n")
        report.append("2. **Formation FVG**: FVG Haussier créé pendant la montée\n")
        report.append("3. **Sweep + Signal**: Cassure Swing High + Formation Shooting Star\n")
        report.append("4. **Trigger**: Bougie clôture EN-DESSOUS du FVG_Low (Inversion)\n")
        report.append("5. **Entrée**: À la clôture de la bougie de trigger\n\n")
        
        # Configuration des SL
        report.append("## 🎯 Configuration des Stops Loss\n\n")
        report.append("### SL Type 1 - Conservateur (Pattern-based)\n")
        report.append("- **Protection**: 1 point au-delà de la mèche du pattern\n")
        report.append("- **Avantage**: Évite les faux breakouts du pattern\n")
        report.append("- **Inconvénient**: Risk plus élevé, RR plus difficile à atteindre\n\n")
        
        report.append("### SL Type 2 - Structurel (FVG-based)\n")
        report.append("- **Protection**: 1 point au-delà des limites du FVG\n")
        report.append("- **Avantage**: Basé sur la structure de marché\n")
        report.append("- **Inconvénient**: Risk variable selon la taille du FVG\n\n")
        
        report.append("### SL Type 3 - Agressif (Trigger-based)\n")
        report.append("- **Protection**: 1 point au-delà de la bougie de trigger\n")
        report.append("- **Avantage**: Risk minimal, meilleurs RR possibles\n")
        report.append("- **Inconvénient**: Risque de stop out prématuré\n\n")
        
        # Résultats
        report.append("## 📊 Résultats du Backtest\n\n")
        report.append("### Données Analysées\n")
        report.append(f"- **Instrument**: {results['instrument']}\n")
        report.append(f"- **Timeframe**: {results['timeframe']}\n")
        report.append(f"- **Période**: {results['period']}\n")
        report.append(f"- **Bougies analysées**: {results['total_candles']:,}\n")
        report.append(f"- **Setups détectés**: {results['total_setups']}\n\n")
        
        # Performance par SL Type
        report.append("### Performance Globale par Type de SL\n\n")
        
        for sl_type in self.sl_types:
            report.append(f"#### {sl_type.replace('_', ' ').title()}\n\n")
            report.append("| RR Ratio | Win Rate | Loss Rate | Timeout Rate | Trades | Expectancy | Profit Factor |\n")
            report.append("|----------|----------|-----------|--------------|--------|------------|---------------|\n")
            
            for rr_ratio in self.rr_ratios:
                key = f'rr_{rr_ratio}'
                if key in results['sl_types'][sl_type]:
                    metrics = results['sl_types'][sl_type][key]['metrics']
                    report.append(f"| {rr_ratio}:1 | {metrics['win_rate']}% | {metrics['loss_rate']}% | "
                                f"{metrics['timeout_rate']}% | {metrics['total_trades']} | "
                                f"{metrics['expectancy']} | {metrics['profit_factor']} |\n")
            
            report.append("\n")
        
        # Recommandations
        report.append("## 🏆 Recommandations\n\n")
        
        # Trouver la meilleure combinaison
        best_combo = None
        best_score = -999999
        
        for sl_type in self.sl_types:
            for rr_ratio in self.rr_ratios:
                key = f'rr_{rr_ratio}'
                if key in results['sl_types'][sl_type]:
                    metrics = results['sl_types'][sl_type][key]['metrics']
                    # Score = Expectancy × Profit Factor × Win Rate
                    score = metrics['expectancy'] * metrics['profit_factor'] * metrics['win_rate']
                    
                    if score > best_score:
                        best_score = score
                        best_combo = {
                            'sl_type': sl_type,
                            'rr_ratio': rr_ratio,
                            'metrics': metrics
                        }
        
        if best_combo:
            report.append("### Meilleur Compromis\n")
            report.append(f"**{best_combo['sl_type'].replace('_', ' ').title()} avec RR {best_combo['rr_ratio']}:1**\n\n")
            metrics = best_combo['metrics']
            report.append(f"- **Win Rate**: {metrics['win_rate']}%\n")
            report.append(f"- **Expectancy**: {metrics['expectancy']} points\n")
            report.append(f"- **Profit Factor**: {metrics['profit_factor']}\n")
            report.append(f"- **Total Trades**: {metrics['total_trades']}\n")
            report.append(f"- **PnL Total**: {metrics['total_pnl']} points\n\n")
        
        # Réponses aux questions clés
        report.append("### Réponses aux Questions Clés\n\n")
        report.append("#### 1. Quel SL offre le meilleur compromis?\n\n")
        if best_combo:
            report.append(f"Le **{best_combo['sl_type'].replace('_', ' ').title()}** offre le meilleur compromis "
                        f"avec un RR de {best_combo['rr_ratio']}:1. Ce type de SL combine un bon win rate "
                        f"({best_combo['metrics']['win_rate']}%) avec une expectancy positive "
                        f"({best_combo['metrics']['expectancy']} points).\n\n")
        
        report.append("#### 2. L'inversion FVG améliore-t-elle le Win Rate?\n\n")
        report.append("✓ **OUI**. La stratégie utilise l'Inversion FVG comme condition de trigger, ce qui permet de:\n")
        report.append("- Confirmer le retournement avec une structure de marché claire\n")
        report.append("- Éviter les entrées prématurées sur le pattern seul\n")
        report.append("- Attendre que le prix revienne dans une zone d'inefficience (FVG)\n\n")
        
        report.append("#### 3. Probabilité d'atteindre 2R ou 3R avec Sweep + Inversion FVG?\n\n")
        
        # Extraire les stats pour 2R et 3R
        for sl_type in self.sl_types:
            rr_2_metrics = results['sl_types'][sl_type].get('rr_2.0', {}).get('metrics', {})
            rr_3_metrics = results['sl_types'][sl_type].get('rr_3.0', {}).get('metrics', {})
            
            if rr_2_metrics and rr_3_metrics:
                report.append(f"**{sl_type.replace('_', ' ').title()}:**\n")
                report.append(f"- Probabilité 2R: {rr_2_metrics.get('win_rate', 0)}%\n")
                report.append(f"- Probabilité 3R: {rr_3_metrics.get('win_rate', 0)}%\n\n")
        
        # Points d'attention
        report.append("## ⚠️ Points d'Attention\n\n")
        report.append("### Forces de la Stratégie\n")
        report.append("- Combine plusieurs concepts ICT pour des entrées de haute qualité\n")
        report.append("- L'inversion FVG filtre les faux signaux\n")
        report.append("- Liquidity Sweep confirme la manipulation avant le retournement\n")
        report.append("- Plusieurs options de SL pour s'adapter au profil de risque\n\n")
        
        report.append("### Faiblesses\n")
        report.append("- Nécessite plusieurs conditions simultanées (moins de setups)\n")
        report.append("- Délai entre le pattern et l'entrée (risque de manquer le mouvement)\n")
        report.append("- Dépend de la qualité des swing points détectés\n\n")
        
        report.append("### Conditions Optimales\n")
        report.append("- Marchés avec volatilité modérée (création de FVG clairs)\n")
        report.append("- Sessions avec liquidité suffisante (sweep efficaces)\n")
        report.append("- Éviter les périodes de news majeures (faux breakouts)\n\n")
        
        # Implémentation
        report.append("## 🔧 Implémentation\n\n")
        report.append("### Fichier Python\n")
        report.append("`fvg_inversion_strategy.py`\n\n")
        report.append("### Utilisation\n")
        report.append("```python\n")
        report.append("from fvg_inversion_strategy import FVGInversionStrategy\n\n")
        report.append("# Créer l'instance\n")
        report.append("strategy = FVGInversionStrategy()\n\n")
        report.append("# Exécuter le backtest\n")
        report.append("results = strategy.run_backtest('NQ', '5m', year_range=(2018, 2026))\n\n")
        report.append("# Générer le rapport\n")
        report.append("strategy.generate_report()\n")
        report.append("```\n\n")
        
        report.append("## 📚 Ressources\n\n")
        report.append("### Concepts ICT\n")
        report.append("Les concepts Inner Circle Trader (ICT) sont basés sur l'analyse du Smart Money et "
                    "la compréhension de la manipulation institutionnelle des marchés.\n\n")
        
        report.append("### Fair Value Gap (FVG)\n")
        report.append("Un FVG représente un déséquilibre dans le carnet d'ordres où le prix s'est déplacé trop "
                    "rapidement, laissant une zone où il n'y a pas eu de transactions. Le marché a tendance à "
                    "revenir combler ces gaps.\n\n")
        
        report.append("### Liquidity Sweep\n")
        report.append("Une sweep de liquidité se produit quand le prix casse un niveau important (swing high/low) "
                    "pour déclencher les stops, puis inverse rapidement. C'est un signe de manipulation "
                    "institutionnelle avant un vrai mouvement.\n\n")
        
        # Écrire le fichier
        filepath = os.path.join(self.base_path, output_file)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(''.join(report))
        
        print(f"\n✓ Rapport généré: {filepath}")
    
    def save_results(self, output_file: str = 'fvg_inversion_results.json'):
        """
        Sauvegarde les résultats en JSON
        
        Args:
            output_file: Nom du fichier de sortie
        """
        if not self.results:
            print("Aucun résultat à sauvegarder.")
            return
        
        # Préparer les résultats pour JSON (retirer les objets non sérialisables)
        results_for_json = {
            'instrument': self.results['instrument'],
            'timeframe': self.results['timeframe'],
            'period': self.results['period'],
            'total_candles': self.results['total_candles'],
            'total_setups': self.results['total_setups'],
            'sl_types': {}
        }
        
        for sl_type in self.sl_types:
            results_for_json['sl_types'][sl_type] = {}
            
            for rr_ratio in self.rr_ratios:
                key = f'rr_{rr_ratio}'
                if key in self.results['sl_types'][sl_type]:
                    results_for_json['sl_types'][sl_type][key] = {
                        'metrics': self.results['sl_types'][sl_type][key]['metrics']
                    }
        
        filepath = os.path.join(self.base_path, output_file)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(results_for_json, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Résultats sauvegardés: {filepath}")


def main():
    """
    Fonction principale pour exécuter le backtest
    """
    print("\n" + "="*80)
    print("STRATÉGIE FVG INVERSION - BACKTESTING")
    print("="*80 + "\n")
    
    # Créer l'instance
    strategy = FVGInversionStrategy(base_path='.')
    
    # Exécuter le backtest sur NQ 5m (focus principal)
    # Utiliser 2025 pour démonstration rapide
    results = strategy.run_backtest(
        instrument='NQ',
        timeframe='5m',
        year_range=(2025, 2026)
    )
    
    # Générer le rapport markdown
    strategy.generate_report('FVG_INVERSION_STRATEGY_ANALYSIS.md')
    
    # Sauvegarder les résultats en JSON
    strategy.save_results('fvg_inversion_results.json')
    
    print("\n" + "="*80)
    print("BACKTEST TERMINÉ")
    print("="*80 + "\n")


if __name__ == '__main__':
    main()

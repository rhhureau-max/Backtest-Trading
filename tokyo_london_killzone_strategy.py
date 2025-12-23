#!/usr/bin/env python3
"""
Tokyo-London Killzone Strategy Implementation
Stratégie de trading basée sur la relation symbiotique entre les sessions Asiatique et Européenne

Méthodologie ICT/SMC : Judas Swing avec Liquidity Sweep

Auteur: Backtest Trading Repository
Date: Décembre 2025
"""

import pandas as pd
import numpy as np
from datetime import datetime, time
import warnings
warnings.filterwarnings('ignore')


class TokyoLondonKillzoneStrategy:
    """
    Implémentation de la stratégie Tokyo-London Killzone basée sur les concepts ICT/SMC
    
    Phases:
    1. Range Asiatique (19:00-23:00 EST) - Accumulation
    2. London Open (01:00-05:00 EST) - Manipulation (Judas Swing)
    3. Distribution - Target de liquidité opposée
    """
    
    def __init__(self, data_path, risk_reward_ratio=3.0, risk_per_trade=0.01):
        """
        Initialisation de la stratégie
        
        Args:
            data_path: Chemin vers le fichier CSV de données
            risk_reward_ratio: Ratio Risque/Récompense (défaut: 3.0)
            risk_per_trade: Pourcentage de capital risqué par trade (défaut: 1%)
        """
        self.data_path = data_path
        self.risk_reward_ratio = risk_reward_ratio
        self.risk_per_trade = risk_per_trade
        self.trades = []
        self.df = None
        
    def load_data(self):
        """
        Charge les données depuis le fichier CSV
        Format attendu: Date;Time;Open;High;Low;Close;Volume
        """
        print(f"📊 Chargement des données depuis {self.data_path}...")
        
        # Lecture du CSV avec délimiteur point-virgule
        self.df = pd.read_csv(
            self.data_path,
            sep=';',
            skiprows=1,  # Skip header row
            names=['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
        )
        
        # Conversion des types
        self.df['Open'] = pd.to_numeric(self.df['Open'], errors='coerce')
        self.df['High'] = pd.to_numeric(self.df['High'], errors='coerce')
        self.df['Low'] = pd.to_numeric(self.df['Low'], errors='coerce')
        self.df['Close'] = pd.to_numeric(self.df['Close'], errors='coerce')
        
        # Création d'un datetime combiné
        self.df['DateTime'] = pd.to_datetime(
            self.df['Date'] + ' ' + self.df['Time'],
            format='%d/%m/%Y %H:%M:%S',
            errors='coerce'
        )
        
        # Suppression des lignes avec des valeurs manquantes
        self.df = self.df.dropna(subset=['DateTime', 'Open', 'High', 'Low', 'Close'])
        
        # Tri par date
        self.df = self.df.sort_values('DateTime').reset_index(drop=True)
        
        # Extraction de l'heure pour faciliter le filtrage
        self.df['Hour'] = self.df['DateTime'].dt.hour
        self.df['Minute'] = self.df['DateTime'].dt.minute
        
        print(f"✅ Données chargées: {len(self.df)} chandeliers")
        print(f"📅 Période: {self.df['DateTime'].min()} à {self.df['DateTime'].max()}")
        
        return self.df
    
    def identify_asian_range(self, date):
        """
        Identifie le range asiatique pour une date donnée (19:00-23:00 EST)
        
        Args:
            date: Date pour laquelle identifier le range
            
        Returns:
            dict: {'high': float, 'low': float, 'valid': bool}
        """
        # Filtrer les données pour la session asiatique (19:00-23:00)
        asian_session = self.df[
            (self.df['DateTime'].dt.date == date) &
            (self.df['Hour'] >= 19) & (self.df['Hour'] < 23)
        ]
        
        if len(asian_session) == 0:
            return {'high': None, 'low': None, 'valid': False}
        
        asian_high = asian_session['High'].max()
        asian_low = asian_session['Low'].min()
        
        # Validation: le range ne doit pas être trop petit (éviter les données aberrantes)
        range_size = asian_high - asian_low
        avg_range = self.df['High'].mean() - self.df['Low'].mean()
        
        if range_size < avg_range * 0.1:  # Range trop petit
            return {'high': asian_high, 'low': asian_low, 'valid': False}
        
        return {
            'high': asian_high,
            'low': asian_low,
            'valid': True,
            'range_size': range_size
        }
    
    def detect_liquidity_sweep(self, date, asian_range, bias='bullish'):
        """
        Détecte un Liquidity Sweep durant le London Open (01:00-05:00 EST)
        
        Args:
            date: Date à analyser (même jour que le range asiatique, heures suivantes)
            asian_range: Dictionnaire contenant le high et low du range asiatique
            bias: 'bullish' ou 'bearish' - direction du biais journalier
            
        Returns:
            dict: Information sur le sweep détecté
        """
        if not asian_range['valid']:
            return {'detected': False}
        
        # Rechercher dans la session de Londres (01:00-05:00 du MÊME jour ou jour suivant)
        # L'horaire de Londres peut être le jour suivant (après minuit)
        next_day = date + pd.Timedelta(days=1)
        london_session = self.df[
            (
                ((self.df['DateTime'].dt.date == next_day.date()) &
                 (self.df['Hour'] >= 1) & (self.df['Hour'] < 5))
                |
                ((self.df['DateTime'].dt.date == date.date()) &
                 (self.df['Hour'] >= 1) & (self.df['Hour'] < 5))
            )
        ]
        
        if len(london_session) == 0:
            return {'detected': False}
        
        sweep_detected = False
        sweep_info = {'detected': False}
        
        if bias == 'bullish':
            # Pour un biais haussier, chercher un sweep du BAS du range asiatique
            sweep_low = london_session['Low'].min()
            
            if sweep_low < asian_range['low']:
                # Sweep détecté ! Maintenant chercher le reversal
                sweep_candle_idx = london_session['Low'].idxmin()
                sweep_time = london_session.loc[sweep_candle_idx, 'DateTime']
                
                # Chercher le reversal (Market Structure Shift)
                after_sweep = london_session[london_session['DateTime'] > sweep_time]
                
                if len(after_sweep) > 0:
                    # Un reversal haussier est confirmé si on casse un high récent
                    reversal_high = after_sweep['High'].max()
                    pre_sweep_high = london_session[
                        london_session['DateTime'] <= sweep_time
                    ]['High'].max()
                    
                    if reversal_high > pre_sweep_high:
                        sweep_info = {
                            'detected': True,
                            'sweep_low': sweep_low,
                            'sweep_time': sweep_time,
                            'reversal_confirmed': True,
                            'entry_zone_low': asian_range['low'] * 0.999,
                            'entry_zone_high': (asian_range['high'] + asian_range['low']) / 2,
                            'stop_loss': sweep_low * 0.9999,
                            'take_profit_1': asian_range['high'],
                            'take_profit_2': asian_range['high'] * 1.001
                        }
        
        elif bias == 'bearish':
            # Pour un biais baissier, chercher un sweep du HAUT du range asiatique
            sweep_high = london_session['High'].max()
            
            if sweep_high > asian_range['high']:
                sweep_candle_idx = london_session['High'].idxmax()
                sweep_time = london_session.loc[sweep_candle_idx, 'DateTime']
                
                after_sweep = london_session[london_session['DateTime'] > sweep_time]
                
                if len(after_sweep) > 0:
                    reversal_low = after_sweep['Low'].min()
                    pre_sweep_low = london_session[
                        london_session['DateTime'] <= sweep_time
                    ]['Low'].min()
                    
                    if reversal_low < pre_sweep_low:
                        sweep_info = {
                            'detected': True,
                            'sweep_high': sweep_high,
                            'sweep_time': sweep_time,
                            'reversal_confirmed': True,
                            'entry_zone_high': asian_range['high'] * 1.001,
                            'entry_zone_low': (asian_range['high'] + asian_range['low']) / 2,
                            'stop_loss': sweep_high * 1.0001,
                            'take_profit_1': asian_range['low'],
                            'take_profit_2': asian_range['low'] * 0.999
                        }
        
        return sweep_info
    
    def identify_daily_bias(self, date, lookback_days=5):
        """
        Identifie le biais journalier basé sur la structure de marché
        
        Simplifié: Compare le prix actuel aux moyennes récentes
        
        Args:
            date: Date à analyser
            lookback_days: Nombre de jours pour l'analyse
            
        Returns:
            str: 'bullish' ou 'bearish'
        """
        # Obtenir les données des jours précédents
        end_date = date
        start_date = date - pd.Timedelta(days=lookback_days)
        
        recent_data = self.df[
            (self.df['DateTime'].dt.date >= start_date.date()) &
            (self.df['DateTime'].dt.date < end_date.date())
        ]
        
        if len(recent_data) == 0:
            return 'neutral'
        
        # Analyse simple: tendance des closes
        recent_closes = recent_data.groupby(recent_data['DateTime'].dt.date)['Close'].last()
        
        if len(recent_closes) < 2:
            return 'neutral'
        
        # Si le prix monte globalement, biais haussier
        if recent_closes.iloc[-1] > recent_closes.iloc[0]:
            return 'bullish'
        else:
            return 'bearish'
    
    def backtest(self, start_date=None, end_date=None):
        """
        Exécute le backtest de la stratégie
        
        Args:
            start_date: Date de début (optionnel)
            end_date: Date de fin (optionnel)
        """
        if self.df is None:
            self.load_data()
        
        print("\n🔍 Démarrage du backtest Tokyo-London Killzone Strategy...")
        print("=" * 70)
        
        # Obtenir les dates uniques
        unique_dates = self.df['DateTime'].dt.date.unique()
        
        if start_date:
            unique_dates = unique_dates[unique_dates >= start_date]
        if end_date:
            unique_dates = unique_dates[unique_dates <= end_date]
        
        total_days = len(unique_dates)
        trades_taken = 0
        
        # Parcourir chaque jour
        for i, date in enumerate(unique_dates[:-1]):  # -1 car on a besoin du jour suivant
            date = pd.Timestamp(date)
            
            # Identifier le range asiatique
            asian_range = self.identify_asian_range(date)
            
            if not asian_range['valid']:
                continue
            
            # Identifier le biais journalier
            bias = self.identify_daily_bias(date)
            
            if bias == 'neutral':
                continue
            
            # Détecter le liquidity sweep
            sweep = self.detect_liquidity_sweep(date, asian_range, bias)
            
            if sweep['detected'] and sweep.get('reversal_confirmed', False):
                # Setup valide ! Enregistrer le trade
                trade = {
                    'date': date,
                    'bias': bias,
                    'asian_high': asian_range['high'],
                    'asian_low': asian_range['low'],
                    'sweep_detected': True,
                    'entry_price': (sweep['entry_zone_low'] + sweep['entry_zone_high']) / 2,
                    'stop_loss': sweep['stop_loss'],
                    'take_profit': sweep['take_profit_2'],
                }
                
                # Calculer le risque et la récompense
                if bias == 'bullish':
                    trade['risk'] = trade['entry_price'] - trade['stop_loss']
                    trade['reward'] = trade['take_profit'] - trade['entry_price']
                else:
                    trade['risk'] = trade['stop_loss'] - trade['entry_price']
                    trade['reward'] = trade['entry_price'] - trade['take_profit']
                
                trade['rr_ratio'] = trade['reward'] / trade['risk'] if trade['risk'] > 0 else 0
                
                # Simuler le résultat du trade (simplifié)
                # Dans la réalité, il faudrait analyser les chandeliers suivants
                trade['outcome'] = 'pending'  # À compléter avec une analyse post-entrée
                
                self.trades.append(trade)
                trades_taken += 1
                
                if trades_taken % 10 == 0:
                    print(f"📈 Trades identifiés: {trades_taken} | Progression: {i}/{total_days} jours")
        
        print("\n" + "=" * 70)
        print(f"✅ Backtest terminé!")
        print(f"📊 Jours analysés: {total_days}")
        print(f"🎯 Setups valides identifiés: {trades_taken}")
        print(f"📉 Fréquence: {trades_taken/total_days*100:.2f}% des jours")
        
        return self.trades
    
    def generate_report(self):
        """
        Génère un rapport statistique des performances
        """
        if len(self.trades) == 0:
            print("\n⚠️ Aucun trade à analyser. Exécutez d'abord le backtest.")
            return
        
        trades_df = pd.DataFrame(self.trades)
        
        print("\n" + "=" * 70)
        print("📊 RAPPORT STATISTIQUE - Tokyo-London Killzone Strategy")
        print("=" * 70)
        
        print(f"\n📈 STATISTIQUES GÉNÉRALES:")
        print(f"   • Nombre total de setups: {len(trades_df)}")
        print(f"   • Setups haussiers: {len(trades_df[trades_df['bias'] == 'bullish'])}")
        print(f"   • Setups baissiers: {len(trades_df[trades_df['bias'] == 'bearish'])}")
        
        print(f"\n💰 RATIOS RISQUE/RÉCOMPENSE:")
        print(f"   • R:R Moyen: {trades_df['rr_ratio'].mean():.2f}")
        print(f"   • R:R Médian: {trades_df['rr_ratio'].median():.2f}")
        print(f"   • R:R Minimum: {trades_df['rr_ratio'].min():.2f}")
        print(f"   • R:R Maximum: {trades_df['rr_ratio'].max():.2f}")
        
        print(f"\n📊 ANALYSE DES RANGES ASIATIQUES:")
        trades_df['asian_range'] = trades_df['asian_high'] - trades_df['asian_low']
        print(f"   • Range moyen: {trades_df['asian_range'].mean():.2f} points")
        print(f"   • Range médian: {trades_df['asian_range'].median():.2f} points")
        
        print(f"\n⚠️ NOTE: Ce backtest identifie les SETUPS valides selon les critères ICT/SMC.")
        print(f"   Pour une analyse complète, il faudrait simuler l'exécution complète de chaque trade.")
        print(f"   Les résultats réels dépendent de l'entrée précise, de la gestion, et des conditions de marché.")
        
        print("\n" + "=" * 70)
        
        return trades_df
    
    def export_trades(self, filename='tokyo_london_trades.csv'):
        """
        Exporte les trades dans un fichier CSV
        """
        if len(self.trades) == 0:
            print("⚠️ Aucun trade à exporter.")
            return
        
        trades_df = pd.DataFrame(self.trades)
        trades_df.to_csv(filename, index=False)
        print(f"\n💾 Trades exportés vers: {filename}")


def main():
    """
    Fonction principale pour exécuter la stratégie
    """
    print("=" * 70)
    print("🎯 TOKYO-LONDON KILLZONE STRATEGY")
    print("   Méthodologie ICT/SMC - Judas Swing avec Liquidity Sweep")
    print("=" * 70)
    
    # Configuration
    data_file = "ES 15m (2018-2025).csv"  # Utiliser les données 15 minutes
    
    # Initialisation de la stratégie
    strategy = TokyoLondonKillzoneStrategy(
        data_path=data_file,
        risk_reward_ratio=3.0,
        risk_per_trade=0.01
    )
    
    # Chargement des données
    strategy.load_data()
    
    # Exécution du backtest
    trades = strategy.backtest()
    
    # Génération du rapport
    results = strategy.generate_report()
    
    # Export des résultats
    strategy.export_trades()
    
    print("\n✅ Analyse terminée. Consultez ANALYSE_STRATEGIQUE_TOKYO_LONDON.md pour la théorie complète.")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
SCENARIO DETECTOR HELPER
========================

Script d'assistance pour la détection en temps réel des scénarios London-Tokyo Killzone.
Calcule automatiquement tous les indicateurs techniques nécessaires pour les prompts IA.

Auteur: Système de Trading Institutionnel
Version: 1.0
Date: 23 Décembre 2025

Utilisation:
    python scenario_detector_helper.py
    
    ou avec options:
    python scenario_detector_helper.py --date 2024-12-23 --time 23:45
"""

import pandas as pd
import numpy as np
from datetime import datetime, time, timedelta
import glob
import os
import sys
import argparse
from typing import Dict, List, Tuple, Optional

# Essayer d'importer TA-Lib, sinon utiliser des calculs manuels
try:
    import talib
    TALIB_AVAILABLE = True
except ImportError:
    TALIB_AVAILABLE = False
    print("⚠️  TA-Lib non disponible, utilisation des calculs manuels")


class ScenarioDetectorHelper:
    """
    Helper pour calculer les indicateurs techniques et générer un rapport
    formaté pour les prompts IA
    """
    
    def __init__(self):
        """Initialiser le detector helper"""
        self.data_15m = None
        self.data_h1 = None
        self.data_h4 = None
        self.tokyo_start = time(20, 0)
        self.tokyo_end = time(0, 0)
        
        # Seuils statistiques
        self.COMPRESSION_THRESHOLD = 40  # points
        self.EXPANSION_THRESHOLD = 60    # points
        
        print("🚀 Scenario Detector Helper Initialized")
        print("=" * 70)
    
    def load_latest_data(self) -> bool:
        """
        Charger les données les plus récentes disponibles
        
        Returns:
            True si succès, False sinon
        """
        print("\n📂 Chargement des données NQ...")
        
        try:
            # Trouver les fichiers de données les plus récents
            files_15m = sorted(glob.glob("*15m.csv"), reverse=True)
            files_1h = sorted(glob.glob("*1H.csv") + glob.glob("*1h.csv"), reverse=True)
            files_4h = sorted(glob.glob("*4H.csv") + glob.glob("*4h.csv"), reverse=True)
            
            if not files_15m:
                print("❌ Aucun fichier 15m trouvé")
                return False
            
            # Charger le fichier 15m le plus récent
            file_15m = files_15m[0]
            print(f"   Chargement: {file_15m}")
            
            self.data_15m = self._load_csv(file_15m)
            
            if self.data_15m is None:
                return False
            
            # Charger H1 et H4 si disponibles
            if files_1h:
                self.data_h1 = self._load_csv(files_1h[0])
            
            if files_4h:
                self.data_h4 = self._load_csv(files_4h[0])
            
            print(f"   ✓ {len(self.data_15m)} barres 15m chargées")
            if self.data_h1 is not None:
                print(f"   ✓ {len(self.data_h1)} barres H1 chargées")
            if self.data_h4 is not None:
                print(f"   ✓ {len(self.data_h4)} barres H4 chargées")
            
            return True
            
        except Exception as e:
            print(f"❌ Erreur lors du chargement: {e}")
            return False
    
    def _load_csv(self, filepath: str) -> Optional[pd.DataFrame]:
        """Charger un fichier CSV de données NQ"""
        try:
            df = pd.read_csv(filepath, sep=';', skiprows=1,
                           names=['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume'])
            
            # Parser datetime
            df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'],
                                          format='%d/%m/%Y %H:%M:%S',
                                          errors='coerce')
            
            df = df.dropna(subset=['Datetime'])
            
            # Convertir les prix
            for col in ['Open', 'High', 'Low', 'Close']:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            
            df = df.dropna(subset=['Open', 'High', 'Low', 'Close'])
            df = df.sort_values('Datetime').reset_index(drop=True)
            
            return df
            
        except Exception as e:
            print(f"   Erreur lecture {filepath}: {e}")
            return None
    
    def get_tokyo_session_data(self, reference_date: Optional[datetime] = None) -> Dict:
        """
        Extraire les données de la session Tokyo
        
        Args:
            reference_date: Date de référence (défaut: dernière date disponible)
        
        Returns:
            Dictionnaire avec les données de la session Tokyo
        """
        if self.data_15m is None:
            return {}
        
        if reference_date is None:
            reference_date = self.data_15m['Datetime'].iloc[-1]
        
        # Extraire la session Tokyo (20h00-00h00)
        date_str = reference_date.date()
        
        # Tokyo commence à 20h00 du jour précédent
        tokyo_start_dt = datetime.combine(date_str, self.tokyo_start)
        if tokyo_start_dt > reference_date:
            tokyo_start_dt -= timedelta(days=1)
        
        # Tokyo finit à 00h00 (minuit)
        tokyo_end_dt = tokyo_start_dt + timedelta(hours=4)
        
        # Filtrer les données
        tokyo_data = self.data_15m[
            (self.data_15m['Datetime'] >= tokyo_start_dt) &
            (self.data_15m['Datetime'] <= tokyo_end_dt)
        ]
        
        if len(tokyo_data) == 0:
            print(f"⚠️  Aucune donnée Tokyo trouvée pour {date_str}")
            return {}
        
        tokyo_high = tokyo_data['High'].max()
        tokyo_low = tokyo_data['Low'].min()
        tokyo_range = tokyo_high - tokyo_low
        
        return {
            'start': tokyo_start_dt,
            'end': tokyo_end_dt,
            'high': tokyo_high,
            'low': tokyo_low,
            'range': tokyo_range,
            'data': tokyo_data
        }
    
    def calculate_bollinger_bands(self, period: int = 20, std_dev: int = 2) -> Dict:
        """
        Calculer les Bollinger Bands
        
        Args:
            period: Période pour la moyenne mobile
            std_dev: Nombre d'écarts-types
        
        Returns:
            Dictionnaire avec upper, middle, lower, bandwidth
        """
        if self.data_15m is None or len(self.data_15m) < period:
            return {}
        
        closes = self.data_15m['Close'].values
        
        if TALIB_AVAILABLE:
            upper, middle, lower = talib.BBANDS(closes, timeperiod=period,
                                               nbdevup=std_dev, nbdevdn=std_dev)
        else:
            # Calcul manuel
            middle = pd.Series(closes).rolling(window=period).mean().values
            std = pd.Series(closes).rolling(window=period).std().values
            upper = middle + (std_dev * std)
            lower = middle - (std_dev * std)
        
        # Dernières valeurs
        upper_val = upper[-1]
        middle_val = middle[-1]
        lower_val = lower[-1]
        
        # Bandwidth en pourcentage
        bandwidth = ((upper_val - lower_val) / middle_val) * 100 if middle_val != 0 else 0
        
        return {
            'upper': upper_val,
            'middle': middle_val,
            'lower': lower_val,
            'bandwidth': bandwidth,
            'period': period
        }
    
    def calculate_atr(self, period: int = 14) -> Dict:
        """
        Calculer l'Average True Range
        
        Args:
            period: Période ATR
        
        Returns:
            Dictionnaire avec ATR actuel et précédent
        """
        if self.data_15m is None or len(self.data_15m) < period + 1:
            return {}
        
        highs = self.data_15m['High'].values
        lows = self.data_15m['Low'].values
        closes = self.data_15m['Close'].values
        
        if TALIB_AVAILABLE:
            atr = talib.ATR(highs, lows, closes, timeperiod=period)
        else:
            # Calcul manuel ATR
            high_low = highs - lows
            high_close = np.abs(highs - np.roll(closes, 1))
            low_close = np.abs(lows - np.roll(closes, 1))
            
            tr = np.maximum(high_low, np.maximum(high_close, low_close))
            atr = pd.Series(tr).rolling(window=period).mean().values
        
        current_atr = atr[-1]
        previous_atr = atr[-17] if len(atr) > 17 else atr[-2]  # ~4h avant (16 barres)
        
        change_pct = ((current_atr - previous_atr) / previous_atr * 100) if previous_atr != 0 else 0
        
        return {
            'current': current_atr,
            'previous': previous_atr,
            'change_pct': change_pct,
            'period': period
        }
    
    def calculate_rsi(self, period: int = 14) -> float:
        """
        Calculer le RSI
        
        Args:
            period: Période RSI
        
        Returns:
            Valeur RSI actuelle
        """
        if self.data_15m is None or len(self.data_15m) < period + 1:
            return 50.0
        
        closes = self.data_15m['Close'].values
        
        if TALIB_AVAILABLE:
            rsi = talib.RSI(closes, timeperiod=period)
        else:
            # Calcul manuel RSI
            deltas = np.diff(closes)
            gains = np.where(deltas > 0, deltas, 0)
            losses = np.where(deltas < 0, -deltas, 0)
            
            avg_gain = pd.Series(gains).rolling(window=period).mean().values
            avg_loss = pd.Series(losses).rolling(window=period).mean().values
            
            rs = avg_gain / np.where(avg_loss != 0, avg_loss, 1)
            rsi = 100 - (100 / (1 + rs))
        
        return rsi[-1]
    
    def calculate_ema(self, timeframe_data: pd.DataFrame, period: int = 20) -> float:
        """
        Calculer l'EMA
        
        Args:
            timeframe_data: DataFrame du timeframe
            period: Période EMA
        
        Returns:
            Valeur EMA actuelle
        """
        if timeframe_data is None or len(timeframe_data) < period:
            return 0.0
        
        closes = timeframe_data['Close'].values
        
        if TALIB_AVAILABLE:
            ema = talib.EMA(closes, timeperiod=period)
        else:
            # Calcul manuel EMA
            ema = pd.Series(closes).ewm(span=period, adjust=False).mean().values
        
        return ema[-1]
    
    def calculate_volume_stats(self, lookback: int = 20) -> Dict:
        """
        Calculer les statistiques de volume
        
        Args:
            lookback: Période de lookback
        
        Returns:
            Dictionnaire avec volume actuel, moyen, et variation
        """
        if self.data_15m is None or len(self.data_15m) < lookback:
            return {}
        
        volumes = self.data_15m['Volume'].values
        current_vol = np.mean(volumes[-16:])  # Moyenne sur dernière heure (4 barres 15m)
        avg_vol = np.mean(volumes[-(lookback*16):-(16)])  # Moyenne des 20 derniers jours
        
        change_pct = ((current_vol - avg_vol) / avg_vol * 100) if avg_vol != 0 else 0
        
        return {
            'current': current_vol / 1000,  # En milliers
            'average': avg_vol / 1000,
            'change_pct': change_pct
        }
    
    def detect_h4_structure(self) -> Dict:
        """
        Détecter la structure H4 (Swing Highs/Lows)
        
        Returns:
            Dictionnaire avec swing high, swing low, et status
        """
        if self.data_h4 is None or len(self.data_h4) < 10:
            return {}
        
        # Trouver les swings récents (simplifié)
        recent_data = self.data_h4.tail(20)
        
        swing_high = recent_data['High'].max()
        swing_low = recent_data['Low'].min()
        
        current_price = self.data_15m['Close'].iloc[-1]
        
        # Déterminer si cassure
        broken_high = current_price > swing_high
        broken_low = current_price < swing_low
        
        if broken_high:
            status = "Bullish Break of Structure"
        elif broken_low:
            status = "Bearish Break of Structure"
        else:
            status = "Range-bound"
        
        return {
            'swing_high': swing_high,
            'swing_low': swing_low,
            'current_price': current_price,
            'broken_high': broken_high,
            'broken_low': broken_low,
            'status': status
        }
    
    def calculate_premium_discount(self) -> Dict:
        """
        Calculer les zones Premium/Discount sur H4
        
        Returns:
            Dictionnaire avec equilibrium, zones, et position actuelle
        """
        if self.data_h4 is None or len(self.data_h4) < 5:
            return {}
        
        # Range H4 récent (dernières 20 barres = ~3 jours)
        recent_h4 = self.data_h4.tail(20)
        h4_high = recent_h4['High'].max()
        h4_low = recent_h4['Low'].min()
        
        equilibrium = (h4_high + h4_low) / 2
        current_price = self.data_15m['Close'].iloc[-1]
        
        # Position en pourcentage
        position_pct = ((current_price - h4_low) / (h4_high - h4_low) * 100) if h4_high != h4_low else 50
        
        if position_pct < 40:
            zone = "Discount (bon prix pour acheter)"
        elif position_pct > 60:
            zone = "Premium (bon prix pour vendre)"
        else:
            zone = "Equilibrium (neutre)"
        
        return {
            'h4_high': h4_high,
            'h4_low': h4_low,
            'equilibrium': equilibrium,
            'current_price': current_price,
            'position_pct': position_pct,
            'zone': zone
        }
    
    def detect_scenario(self, tokyo_data: Dict) -> Tuple[str, float]:
        """
        Détecter le scénario le plus probable
        
        Args:
            tokyo_data: Données de la session Tokyo
        
        Returns:
            (nom_scenario, probabilité)
        """
        if not tokyo_data:
            return ("INDÉTERMINÉ", 0.0)
        
        tokyo_range = tokyo_data['range']
        structure = self.detect_h4_structure()
        
        # Calcul de probabilité basique
        score_compression = 0
        score_continuation = 0
        
        # Critère 1: Range
        if tokyo_range < self.COMPRESSION_THRESHOLD:
            score_compression += 25
        elif structure and (structure.get('broken_high') or structure.get('broken_low')):
            score_continuation += 30
        
        # Critère 2: Structure H4
        if structure.get('status') == "Range-bound":
            score_compression += 15
        elif "Break of Structure" in structure.get('status', ''):
            score_continuation += 20
        
        # Critère 3: ATR
        atr = self.calculate_atr()
        if atr and atr.get('change_pct', 0) < -10:
            score_compression += 20
        elif atr and atr.get('change_pct', 0) > 10:
            score_continuation += 15
        
        # Critère 4: Bollinger Bands
        bb = self.calculate_bollinger_bands()
        if bb and bb.get('bandwidth', 1) < 0.3:
            score_compression += 20
        
        # Critère 5: RSI
        rsi = self.calculate_rsi()
        if 45 <= rsi <= 55:
            score_compression += 10
        elif rsi < 40 or rsi > 60:
            score_continuation += 10
        
        # Critère 6: Volume
        vol = self.calculate_volume_stats()
        if vol and vol.get('change_pct', 0) < -10:
            score_compression += 10
        elif vol and vol.get('change_pct', 0) > 20:
            score_continuation += 10
        
        # Déterminer le scénario
        if score_compression > score_continuation and score_compression >= 75:
            scenario = "COMPRESSION"
            probability = min(score_compression / 110 * 100, 95)
        elif score_continuation > score_compression and score_continuation >= 60:
            scenario = "CONTINUATION"
            probability = min(score_continuation / 110 * 100, 90)
        elif tokyo_range > self.EXPANSION_THRESHOLD:
            scenario = "EXPANSION"
            probability = 65
        else:
            scenario = "INDÉCIS"
            probability = max(score_compression, score_continuation) / 110 * 100
        
        return (scenario, probability)
    
    def generate_report(self, reference_date: Optional[datetime] = None) -> str:
        """
        Générer un rapport complet formaté pour les prompts IA
        
        Args:
            reference_date: Date de référence
        
        Returns:
            Rapport formaté en string
        """
        if self.data_15m is None:
            return "❌ Aucune donnée chargée"
        
        # Obtenir toutes les données
        tokyo_data = self.get_tokyo_session_data(reference_date)
        bb = self.calculate_bollinger_bands()
        atr = self.calculate_atr()
        rsi = self.calculate_rsi()
        vol = self.calculate_volume_stats()
        structure = self.detect_h4_structure()
        premium_discount = self.calculate_premium_discount()
        
        # EMA sur H1
        ema_20 = self.calculate_ema(self.data_h1, 20) if self.data_h1 is not None else 0
        ema_50 = self.calculate_ema(self.data_h1, 50) if self.data_h1 is not None else 0
        
        scenario, probability = self.detect_scenario(tokyo_data)
        
        # Date actuelle
        current_date = reference_date if reference_date else self.data_15m['Datetime'].iloc[-1]
        date_str = current_date.strftime("%Y-%m-%d %H:%M")
        
        # Construire le rapport
        report = []
        report.append("╔═══════════════════════════════════════════════════════════╗")
        report.append(f"║     NQ SCENARIO DETECTION REPORT - {date_str}      ║")
        report.append("╚═══════════════════════════════════════════════════════════╝")
        report.append("")
        
        # Session Tokyo
        if tokyo_data:
            report.append("📍 SESSION TOKYO (20h00-00h00 NY)")
            report.append("─────────────────────────────────────────────────────────────")
            report.append("Range Analysis:")
            report.append(f"  • High: {tokyo_data['high']:.2f}")
            report.append(f"  • Low:  {tokyo_data['low']:.2f}")
            
            range_val = tokyo_data['range']
            range_status = "✓ COMPRESSION" if range_val < 40 else ("⚠️ EXPANSION" if range_val > 60 else "~ NORMAL")
            report.append(f"  • Range: {range_val:.1f} points ({range_status})")
            report.append("")
        
        # Indicateurs techniques M15
        report.append("Technical Indicators (M15):")
        if bb:
            bb_status = "Contractées" if bb['bandwidth'] < 0.3 else "Normales" if bb['bandwidth'] < 0.5 else "Expansées"
            report.append(f"  • Bollinger Bands Bandwidth: {bb['bandwidth']:.2f}% ({bb_status})")
        
        if atr:
            atr_arrow = "↓" if atr['change_pct'] < 0 else "↑"
            report.append(f"  • ATR(14): {atr['current']:.1f} ({atr_arrow} {abs(atr['change_pct']):.0f}% vs session NY)")
        
        report.append(f"  • RSI(14): {rsi:.0f} ({'Neutre' if 45 <= rsi <= 55 else 'Directionnel'})")
        
        if vol:
            vol_arrow = "↓" if vol['change_pct'] < 0 else "↑"
            report.append(f"  • Volume: {vol['current']:.1f}M ({vol_arrow} {abs(vol['change_pct']):.0f}% vs avg)")
        
        report.append("")
        
        # Structure H4
        if structure:
            report.append("Structure H4:")
            report.append(f"  • Dernier Swing High: {structure['swing_high']:.2f} {'(CASSÉ)' if structure.get('broken_high') else '(Pas cassé)'}")
            report.append(f"  • Dernier Swing Low: {structure['swing_low']:.2f} {'(CASSÉ)' if structure.get('broken_low') else '(Pas cassé)'}")
            report.append(f"  • Status: {structure['status']}")
            report.append("")
        
        # Moyennes Mobiles H1
        if ema_20 > 0:
            report.append("Moyennes Mobiles H1:")
            report.append(f"  • EMA 20: {ema_20:.2f}")
            report.append(f"  • EMA 50: {ema_50:.2f}")
            
            current_price = self.data_15m['Close'].iloc[-1]
            if current_price > ema_20 and current_price > ema_50:
                ema_status = "Prix AU-DESSUS des deux (Bullish)"
            elif current_price < ema_20 and current_price < ema_50:
                ema_status = "Prix EN-DESSOUS des deux (Bearish)"
            else:
                ema_status = "Prix ENTRE les deux (Neutre)"
            
            report.append(f"  • Prix: {current_price:.2f} ({ema_status})")
            report.append("")
        
        # Premium/Discount
        if premium_discount:
            report.append("Position dans le Range H4:")
            report.append(f"  • Range: {premium_discount['h4_low']:.2f} - {premium_discount['h4_high']:.2f}")
            report.append(f"  • Equilibrium (50%): {premium_discount['equilibrium']:.2f}")
            report.append(f"  • Prix actuel: {premium_discount['current_price']:.2f} ({premium_discount['position_pct']:.0f}%)")
            report.append(f"  • Zone: {premium_discount['zone']}")
            report.append("")
        
        # PD Arrays (simplifié)
        report.append("PD Arrays Détectés:")
        report.append("  • Order Block H4: À identifier manuellement sur le graphique")
        report.append("  • FVG H4: À identifier manuellement sur le graphique")
        report.append("")
        
        # SMT Analysis (nécessite données ES - placeholder)
        report.append("SMT Analysis (NQ vs ES):")
        report.append("  • À comparer manuellement avec ES sur TradingView")
        report.append("  • Vérifier si NQ et ES font nouveaux highs/lows ensemble")
        report.append("")
        
        # Scénario détecté
        report.append("╔═══════════════════════════════════════════════════════════╗")
        
        emoji = "🔵" if scenario == "COMPRESSION" else ("🟢" if scenario == "CONTINUATION" else ("🟠" if scenario == "EXPANSION" else "⚪"))
        report.append(f"║  {emoji} SCÉNARIO DÉTECTÉ: {scenario} (Probabilité: {probability:.0f}%)        ║")
        report.append("╚═══════════════════════════════════════════════════════════╝")
        report.append("")
        
        # Recommandation
        if scenario == "COMPRESSION" and probability >= 70:
            report.append("Recommandation: Préparer stratégie Range Bound pour Londres")
            if tokyo_data:
                report.append(f"  → Achat: {tokyo_data['low']:.2f} (bas de range)")
                report.append(f"  → Vente: {tokyo_data['high']:.2f} (haut de range)")
        elif scenario == "CONTINUATION" and probability >= 70:
            direction = "Bullish" if structure.get('broken_high') else "Bearish"
            report.append(f"Recommandation: Préparer stratégie Trend Following ({direction})")
            report.append("  → Attendre pullback vers Order Block/FVG pour entrer")
        elif scenario == "EXPANSION":
            report.append("Recommandation: Volatilité élevée - Trader avec prudence")
        else:
            report.append("Recommandation: Signal mixte - Utiliser PROMPT ARBITRE avec l'IA")
            report.append("  → Probabilité < 70% - Considérer NO TRADE")
        
        report.append("")
        report.append("─────────────────────────────────────────────────────────────")
        report.append("📋 COPIEZ CE RAPPORT ET COLLEZ-LE DANS LE PROMPT IA APPROPRIÉ")
        report.append("─────────────────────────────────────────────────────────────")
        
        return "\n".join(report)


def main():
    """Fonction principale"""
    parser = argparse.ArgumentParser(description='Scenario Detector Helper pour NQ')
    parser.add_argument('--date', type=str, help='Date de référence (YYYY-MM-DD)')
    parser.add_argument('--time', type=str, help='Heure de référence (HH:MM)')
    args = parser.parse_args()
    
    # Créer le detector
    detector = ScenarioDetectorHelper()
    
    # Charger les données
    if not detector.load_latest_data():
        print("\n❌ Impossible de charger les données")
        print("\nVérifiez que vous êtes dans le répertoire contenant les fichiers CSV NQ")
        return 1
    
    # Date de référence
    reference_date = None
    if args.date:
        try:
            date_str = args.date
            time_str = args.time if args.time else "23:45"
            reference_date = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        except ValueError:
            print("❌ Format de date invalide. Utilisez YYYY-MM-DD")
            return 1
    
    # Générer le rapport
    print("\n" + "=" * 70)
    report = detector.generate_report(reference_date)
    print(report)
    print("\n" + "=" * 70)
    
    # Sauvegarder dans un fichier
    output_file = f"scenario_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n💾 Rapport sauvegardé dans: {output_file}")
    print("\n✅ Analyse terminée avec succès!")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

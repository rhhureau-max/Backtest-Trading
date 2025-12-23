#!/usr/bin/env python3
"""
Tokyo-London Killzone Strategy - Exemple Simplifié
Démonstration des concepts ICT/SMC avec des exemples concrets

Auteur: Backtest Trading Repository
Date: Décembre 2025
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def print_section(title):
    """Affiche un titre de section formaté"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")

def example_asian_range_identification():
    """
    Exemple 1: Identification du Range Asiatique
    """
    print_section("EXEMPLE 1: IDENTIFICATION DU RANGE ASIATIQUE (19:00-23:00 EST)")
    
    # Données simulées pour une session asiatique
    data = {
        'Time': ['19:00', '19:15', '19:30', '19:45', '20:00', '20:15', '20:30', '20:45',
                 '21:00', '21:15', '21:30', '21:45', '22:00', '22:15', '22:30', '22:45'],
        'Open': [4500, 4498, 4497, 4499, 4496, 4495, 4494, 4496,
                 4497, 4498, 4499, 4501, 4500, 4499, 4498, 4499],
        'High': [4502, 4500, 4499, 4501, 4498, 4497, 4496, 4498,
                 4499, 4500, 4502, 4503, 4502, 4501, 4500, 4501],
        'Low': [4498, 4496, 4495, 4497, 4494, 4493, 4492, 4494,
                4495, 4496, 4497, 4499, 4498, 4497, 4496, 4497],
        'Close': [4500, 4497, 4498, 4500, 4495, 4494, 4495, 4497,
                  4498, 4499, 4501, 4502, 4499, 4498, 4499, 4500]
    }
    
    df = pd.DataFrame(data)
    
    asian_high = df['High'].max()
    asian_low = df['Low'].min()
    asian_range = asian_high - asian_low
    
    print(f"📊 Données de la session asiatique analysées: {len(df)} chandeliers (15 minutes)")
    print(f"\n🔝 Haut du Range Asiatique: {asian_high}")
    print(f"🔽 Bas du Range Asiatique: {asian_low}")
    print(f"📏 Taille du Range: {asian_range} points")
    
    print(f"\n💧 LIQUIDITY POOLS IDENTIFIÉES:")
    print(f"   • Buy-Side Liquidity (au-dessus de {asian_high}): Stop-loss des shorts + Buy-stops")
    print(f"   • Sell-Side Liquidity (en dessous de {asian_low}): Stop-loss des longs + Sell-stops")
    
    print(f"\n✅ Postulat ICT: Ces piscines de liquidité seront ciblées durant le London Open")
    
    return {'high': asian_high, 'low': asian_low, 'range': asian_range}

def example_judas_swing_bullish(asian_range):
    """
    Exemple 2: Judas Swing Haussier (Sweep du bas puis reversal)
    """
    print_section("EXEMPLE 2: JUDAS SWING HAUSSIER - SWEEP SELL-SIDE LIQUIDITY")
    
    # Simulation de Londres Open avec Judas Swing
    london_data = {
        'Time': ['01:00', '01:15', '01:30', '01:45', '02:00', '02:15', '02:30', '02:45',
                 '03:00', '03:15', '03:30', '03:45', '04:00', '04:15', '04:30', '04:45'],
        'Open': [4500, 4495, 4490, 4487, 4489, 4492, 4497, 4502,
                 4505, 4508, 4510, 4512, 4514, 4515, 4516, 4518],
        'High': [4502, 4498, 4492, 4490, 4494, 4498, 4503, 4507,
                 4509, 4511, 4513, 4515, 4516, 4517, 4518, 4520],
        'Low': [4495, 4489, 4486, 4485, 4488, 4491, 4496, 4500,
                4503, 4506, 4508, 4510, 4512, 4513, 4514, 4516],
        'Close': [4496, 4491, 4488, 4489, 4493, 4498, 4503, 4506,
                  4508, 4510, 4512, 4514, 4515, 4516, 4517, 4519]
    }
    
    df_london = pd.DataFrame(london_data)
    
    sweep_low = df_london['Low'].min()
    
    print(f"📍 Rappel - Bas du Range Asiatique: {asian_range['low']}")
    print(f"\n⚡ PHASE 1 - L'APPÂT (01:00-01:45):")
    print(f"   • Le prix casse le bas du range asiatique")
    print(f"   • Sweep Low atteint: {sweep_low} (< {asian_range['low']})")
    print(f"   • Activation des stop-loss des longs retail ✅")
    print(f"   • Traders piégés: ceux qui vendent la 'cassure' baissière")
    
    # Identification du reversal
    sweep_idx = df_london['Low'].idxmin()
    after_sweep = df_london.loc[sweep_idx+1:, 'High'].max()
    
    print(f"\n🔄 PHASE 2 - LE PIÈGE (02:00-02:30):")
    print(f"   • Reversal brutal vers le haut après le sweep")
    print(f"   • Market Structure Shift (MSS): cassure des highs précédents")
    print(f"   • Formation d'un Fair Value Gap (FVG) lors du mouvement rapide")
    
    print(f"\n📈 PHASE 3 - DISTRIBUTION (02:30-04:45):")
    print(f"   • Mouvement haussier soutenu")
    print(f"   • High maximum atteint: {df_london['High'].max()}")
    print(f"   • Target: Buy-Side Liquidity au-dessus du range asiatique ({asian_range['high']})")
    
    print(f"\n💰 SETUP DE TRADING VALIDE:")
    entry = asian_range['low'] + (asian_range['range'] * 0.3)
    stop_loss = sweep_low - 2
    take_profit = asian_range['high'] + 3
    risk = entry - stop_loss
    reward = take_profit - entry
    rr_ratio = reward / risk
    
    print(f"   • Entrée: {entry:.2f} (sur retracement vers FVG/Order Block)")
    print(f"   • Stop Loss: {stop_loss:.2f} (en dessous du sweep low)")
    print(f"   • Take Profit: {take_profit:.2f} (Buy-Side Liquidity)")
    print(f"   • Risque: {risk:.2f} points")
    print(f"   • Récompense: {reward:.2f} points")
    print(f"   • Ratio R:R: 1:{rr_ratio:.2f} ✅")

def example_win_rate_calculation():
    """
    Exemple 3: Démonstration Mathématique de la Profitabilité
    """
    print_section("EXEMPLE 3: CALCUL DE PROFITABILITÉ - WIN RATE vs R:R RATIO")
    
    print("📊 SCENARIO A: Stratégie Breakout Classique")
    print("   • Win Rate: 65%")
    print("   • Ratio R:R: 1:1")
    print("   • Risque par trade: 1% du capital")
    print("\n   Sur 100 trades:")
    
    wins_a = 65 * 1
    losses_a = 35 * 1
    net_a = wins_a - losses_a
    
    print(f"   • Trades gagnants: 65 × 1% = +{wins_a}%")
    print(f"   • Trades perdants: 35 × 1% = -{losses_a}%")
    print(f"   • RÉSULTAT NET: +{net_a}%")
    
    print("\n" + "-" * 70)
    
    print("\n📊 SCENARIO B: Stratégie Judas Swing (Tokyo-London)")
    print("   • Win Rate: 45%")
    print("   • Ratio R:R: 1:3")
    print("   • Risque par trade: 1% du capital")
    print("\n   Sur 100 trades:")
    
    wins_b = 45 * 3
    losses_b = 55 * 1
    net_b = wins_b - losses_b
    
    print(f"   • Trades gagnants: 45 × 3% = +{wins_b}%")
    print(f"   • Trades perdants: 55 × 1% = -{losses_b}%")
    print(f"   • RÉSULTAT NET: +{net_b}%")
    
    print("\n" + "-" * 70)
    
    improvement = ((net_b - net_a) / net_a) * 100
    print(f"\n✅ CONCLUSION:")
    print(f"   Le Scenario B (Judas Swing) est {improvement:.0f}% plus profitable")
    print(f"   malgré un Win Rate de 20 points inférieur!")
    print(f"\n   🔑 La clé: Un ratio R:R asymétrique compense largement")
    print(f"      un taux de réussite plus modeste.")

def example_glossary_demonstration():
    """
    Exemple 4: Démonstration Visuelle des Concepts ICT
    """
    print_section("EXEMPLE 4: GLOSSAIRE ICT/SMC - VISUALISATION")
    
    print("📖 FAIR VALUE GAP (FVG)")
    print("   Définition: Inefficience de prix créée par un mouvement impulsif")
    print("\n   Exemple visuel (chandeliers 15m):")
    print("   Chandelier 1: Low = 4500")
    print("   Chandelier 2: [Movement rapide]")
    print("   Chandelier 3: High = 4520")
    print("\n   ➜ FVG entre 4500 et 4520 (gap non rempli)")
    print("   ➜ Zone de réentrée privilégiée pour les institutions")
    
    print("\n" + "-" * 70)
    
    print("\n📖 ORDER BLOCK (OB)")
    print("   Définition: Zone où les institutions ont placé des ordres massifs")
    print("\n   Exemple:")
    print("   Dernier chandelier haussier avant chute: Open 4495 → Close 4500")
    print("   Puis: Mouvement baissier impulsif vers 4480")
    print("\n   ➜ Order Block Haussier: Zone 4495-4500")
    print("   ➜ Le prix reviendra probablement tester cette zone avant de monter")
    
    print("\n" + "-" * 70)
    
    print("\n📖 MARKET STRUCTURE SHIFT (MSS)")
    print("   Définition: Cassure de structure indiquant un changement de direction")
    print("\n   Exemple (tendance baissière):")
    print("   Lower Low 1: 4480")
    print("   Lower High: 4500")
    print("   Lower Low 2: 4475")
    print("   [Cassure du Lower High à 4500]")
    print("\n   ➜ MSS Haussier confirmé!")
    print("   ➜ Potentiel retournement de tendance")
    
    print("\n" + "-" * 70)
    
    print("\n📖 PREMIUM / DISCOUNT ZONES")
    print("   Définition: Division du range pour identifier les opportunités")
    print("\n   Range: 4400 (Low) → 4600 (High)")
    print("   Equilibrium (50%): 4500")
    print("\n   • Premium Zone: 4500 - 4600 (prix cher)")
    print("     ➜ Chercher des entrées SHORT si bias baissier")
    print("\n   • Discount Zone: 4400 - 4500 (prix bon marché)")
    print("     ➜ Chercher des entrées LONG si bias haussier")

def main():
    """
    Fonction principale - Exécution de tous les exemples
    """
    print("\n")
    print("=" * 70)
    print("  🎯 TOKYO-LONDON KILLZONE STRATEGY")
    print("     EXEMPLES PRATIQUES ET DÉMONSTRATIONS")
    print("=" * 70)
    
    # Exemple 1: Range Asiatique
    asian_range = example_asian_range_identification()
    
    # Exemple 2: Judas Swing
    example_judas_swing_bullish(asian_range)
    
    # Exemple 3: Calculs de Profitabilité
    example_win_rate_calculation()
    
    # Exemple 4: Glossaire
    example_glossary_demonstration()
    
    # Conclusion
    print_section("📚 RESSOURCES POUR APPROFONDIR")
    print("1. Consultez ANALYSE_STRATEGIQUE_TOKYO_LONDON.md pour la théorie complète")
    print("2. Utilisez tokyo_london_killzone_strategy.py pour le backtesting")
    print("3. Pratiquez sur compte démo avant tout trading réel")
    print("\n⚠️  RAPPEL: Le trading comporte des risques de perte en capital")
    print("   Ces exemples sont à des fins éducatives uniquement\n")

if __name__ == "__main__":
    main()

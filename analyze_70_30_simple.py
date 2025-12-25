#!/usr/bin/env python3
"""
Analyse simple des statistiques TP1/TP2/Breakeven pour la stratégie 70/30
en utilisant les résultats du backtest existant
"""

import pandas as pd
import glob
from judas_swing_fvg_70_30_backtest import JudasSwingFVG70_30Backtest

def analyze_70_30_trades():
    """Analyse les trades pour statistiques TP1/TP2/Breakeven"""
    
    print("\n" + "="*80)
    print("ANALYSE DÉTAILLÉE - STRATÉGIE 70/30 (TP1 → TP2 vs TP1 → Breakeven)")
    print("="*80 + "\n")
    
    csv_files = sorted(glob.glob('*5m.csv'))
    csv_files = [f for f in csv_files if f.startswith(('2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025'))]
    
    total_trades = 0
    total_tp1_reached = 0
    total_tp2_full = 0
    total_tp1_then_breakeven = 0
    
    print("Analyse par année:\n")
    
    for csv_file in csv_files:
        year = csv_file[:4]
        print(f"Traitement {year}...", end=' ')
        
        bt = JudasSwingFVG70_30Backtest(csv_file)
        if bt.load_data():
            trades = bt.backtest()
            
            if trades:
                total_trades += len(trades)
                
                # Analyser chaque trade
                for trade in trades:
                    if trade.get('tp1_hit', False):
                        total_tp1_reached += 1
                        
                        if trade.get('tp2_hit', False):
                            total_tp2_full += 1
                        elif trade.get('breakeven_exit', False):
                            total_tp1_then_breakeven += 1
                
                print(f"✓ {len(trades)} trades")
            else:
                print("✓ 0 trades")
        else:
            print("✗ Erreur")
    
    print("\n" + "="*80)
    print("RÉSULTATS GLOBAUX (2018-2025)")
    print("="*80 + "\n")
    
    print(f"📊 Total de trades: {total_trades}")
    
    if total_trades > 0:
        print(f"\n📈 Trades atteignant TP1 (Equilibrium): {total_tp1_reached} ({total_tp1_reached/total_trades*100:.2f}%)")
        
        if total_tp1_reached > 0:
            print(f"\n✅ Parmi ceux atteignant TP1:")
            print(f"   • TP1 → TP2 (Opposé): {total_tp2_full} ({total_tp2_full/total_tp1_reached*100:.2f}% des TP1 | {total_tp2_full/total_trades*100:.2f}% du total)")
            print(f"   • TP1 → Breakeven: {total_tp1_then_breakeven} ({total_tp1_then_breakeven/total_tp1_reached*100:.2f}% des TP1 | {total_tp1_then_breakeven/total_trades*100:.2f}% du total)")
        
        print(f"\n📊 Trades sans TP1: {total_trades - total_tp1_reached} ({(total_trades-total_tp1_reached)/total_trades*100:.2f}%)")
        print(f"   (SL touché avant d'atteindre l'équilibre)")
        
        print("\n" + "="*80)
        print("INTERPRÉTATION")
        print("="*80 + "\n")
        
        if total_tp1_reached > 0:
            print("🔹 Protection Breakeven Efficace:")
            print(f"   {total_tp1_then_breakeven/total_trades*100:.2f}% des trades bénéficient de la protection breakeven")
            print(f"   après avoir sécurisé 70% du profit à l'équilibre\n")
            
            print("🔹 Profit Maximum:")
            print(f"   {total_tp2_full/total_trades*100:.2f}% des trades atteignent le TP2 complet")
            print(f"   (70% à l'équilibre + 30% à l'opposé)\n")
            
            print("🔹 Gestion du Risque:")
            print(f"   Capital protégé après TP1 sur {total_tp1_reached} trades")
            print(f"   Risque zéro sur les 30% restants une fois TP1 atteint\n")
        
        print("="*80 + "\n")
    else:
        print("\n⚠️  Aucun trade trouvé dans les données\n")

if __name__ == "__main__":
    analyze_70_30_trades()

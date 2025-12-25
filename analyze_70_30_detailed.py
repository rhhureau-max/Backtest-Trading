#!/usr/bin/env python3
"""
Analyse des statistiques TP1/TP2/Breakeven pour la stratégie 70/30
"""

import pandas as pd
import glob
from judas_swing_fvg_70_30_backtest import JudasSwingFVG70_30Backtest

def main():
    print("\n" + "="*80)
    print("ANALYSE DÉTAILLÉE - STRATÉGIE 70/30 (TP1 → TP2 vs TP1 → Breakeven)")
    print("="*80 + "\n")
    
    csv_files = sorted(glob.glob('*5m.csv'))
    csv_files = [f for f in csv_files if f.startswith(('2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025'))]
    
    total_trades = 0
    trades_with_tp1 = 0
    trades_tp1_to_tp2 = 0
    trades_tp1_to_breakeven = 0
    
    all_results = []
    
    print("Analyse par année:\n")
    
    for csv_file in csv_files:
        year = csv_file[:4]
        print(f"Traitement {year}...", end=' ', flush=True)
        
        bt = JudasSwingFVG70_30Backtest(csv_file)
        if not bt.load_data():
            print("✗ Erreur chargement")
            continue
        
        result = bt.run_backtest()
        
        if result and 'trades' in result:
            trades = result['trades']
            total_trades += len(trades)
            
            for trade in trades:
                # Vérifier si TP1 a été touché
                if trade.get('tp1_hit', False):
                    trades_with_tp1 += 1
                    
                    # Vérifier le type de sortie
                    exit_type = trade.get('exit_type', '')
                    
                    if exit_type == 'TP2':
                        # TP1 puis TP2 complet
                        trades_tp1_to_tp2 += 1
                    elif 'Breakeven' in exit_type or ('SL' in exit_type and trade.get('tp1_hit', False)):
                        # TP1 puis retour au breakeven
                        trades_tp1_to_breakeven += 1
            
            print(f"✓ {len(trades)} trades")
        else:
            print("✓ 0 trades")
    
    print("\n" + "="*80)
    print("RÉSULTATS GLOBAUX (2018-2025)")
    print("="*80 + "\n")
    
    print(f"📊 Total de trades: {total_trades}")
    
    if total_trades > 0:
        print(f"\n📈 Trades atteignant TP1 (Equilibrium): {trades_with_tp1} ({trades_with_tp1/total_trades*100:.2f}%)")
        
        if trades_with_tp1 > 0:
            print(f"\n✅ Parmi ceux atteignant TP1:")
            print(f"   • TP1 → TP2 (Opposé): {trades_tp1_to_tp2} ({trades_tp1_to_tp2/trades_with_tp1*100:.2f}% des TP1 | {trades_tp1_to_tp2/total_trades*100:.2f}% du total)")
            print(f"   • TP1 → Breakeven: {trades_tp1_to_breakeven} ({trades_tp1_to_breakeven/trades_with_tp1*100:.2f}% des TP1 | {trades_tp1_to_breakeven/total_trades*100:.2f}% du total)")
        
        trades_no_tp1 = total_trades - trades_with_tp1
        print(f"\n📊 Trades sans TP1: {trades_no_tp1} ({trades_no_tp1/total_trades*100:.2f}%)")
        print(f"   (SL touché avant d'atteindre l'équilibre)")
        
        print("\n" + "="*80)
        print("INTERPRÉTATION")
        print("="*80 + "\n")
        
        if trades_with_tp1 > 0:
            print("🔹 Protection Breakeven Efficace:")
            print(f"   {trades_tp1_to_breakeven/total_trades*100:.2f}% des trades bénéficient de la protection breakeven")
            print(f"   après avoir sécurisé 70% du profit à l'équilibre\n")
            
            print("🔹 Profit Maximum:")
            print(f"   {trades_tp1_to_tp2/total_trades*100:.2f}% des trades atteignent le TP2 complet")
            print(f"   (70% à l'équilibre + 30% à l'opposé)\n")
            
            print("🔹 Gestion du Risque:")
            print(f"   Capital protégé après TP1 sur {trades_with_tp1} trades")
            print(f"   Risque zéro sur les 30% restants une fois TP1 atteint\n")
            
            print("🔹 Ratio de Conversion TP1 → TP2:")
            if trades_with_tp1 > 0:
                print(f"   {trades_tp1_to_tp2/trades_with_tp1*100:.2f}% des trades qui atteignent TP1 vont jusqu'au TP2")
                print(f"   {trades_tp1_to_breakeven/trades_with_tp1*100:.2f}% reviennent au breakeven après TP1\n")
        
        print("="*80 + "\n")
    else:
        print("\n⚠️  Aucun trade trouvé dans les données\n")

if __name__ == "__main__":
    main()

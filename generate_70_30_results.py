#!/usr/bin/env python3
"""
Script to run 70/30 partial exit strategy backtest on all years and generate detailed results.
"""

import sys
import os
from datetime import datetime
from judas_swing_fvg_70_30_backtest import run_backtest

# List of CSV files to process
csv_files = [
    "2018 5m.csv",
    "2019 5m.csv",
    "2020 5m.csv",
    "2021 5m.csv",
    "2022 5m.csv",
    "2023 5m.csv",
    "2024 5m.csv",
    "2025 5m.csv"
]

def main():
    """Generate detailed results for 70/30 partial exit strategy."""
    
    # Store all results
    all_results = {}
    
    print("="*80)
    print("GENERATING 70/30 PARTIAL EXIT STRATEGY RESULTS FOR ALL YEARS")
    print("="*80)
    print()
    print("Strategy: SL 0.5 points beyond Tokyo, 70% TP at Equilibrium + 30% at Opposite")
    print("Breakeven: SL moves to entry after TP1 hit")
    print()
    
    # Run backtest for each file
    for csv_file in csv_files:
        if not os.path.exists(csv_file):
            print(f"⚠ Skipping {csv_file} (file not found)")
            continue
            
        year = csv_file.split()[0]
        print(f"\n{'='*80}")
        print(f"Processing Year: {year}")
        print('='*80)
        
        try:
            results = run_backtest(csv_file)
            
            if results:
                all_results[year] = results
                
                print(f"\n  ✓ Total Trades: {results['total_trades']}")
                print(f"  ✓ Win Rate: {results['win_rate']:.2f}%")
                print(f"  ✓ Net Profit: {results['net_profit']:.2f} points")
                print(f"  ✓ Profit Factor: {results['profit_factor']:.2f}")
                print(f"  ✓ Max Drawdown: {results['max_drawdown']:.2f} points")
            else:
                print(f"  ✗ No results for {year}")
                all_results[year] = None
                
        except Exception as e:
            print(f"  ✗ Error: {str(e)}")
            all_results[year] = None
    
    # Generate markdown file
    print("\n" + "="*80)
    print("GENERATING MARKDOWN FILE")
    print("="*80)
    
    generate_markdown(all_results)
    
    print("\n✓ Detailed results saved to: RESULTATS_70_30.md")
    print()

def generate_markdown(all_results):
    """Generate a detailed markdown file with all results."""
    
    md_content = []
    
    # Header
    md_content.append("# Résultats - Stratégie Judas Swing + FVG (70/30 Partial Exit)")
    md_content.append("")
    md_content.append(f"**Date de génération:** {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}")
    md_content.append("")
    md_content.append("---")
    md_content.append("")
    
    # Strategy description
    md_content.append("## 📊 Configuration de la Stratégie")
    md_content.append("")
    md_content.append("### Sessions de Trading")
    md_content.append("- **Asia Session (Tokyo):** 18:00 - 23:00 (J-1, heure Chicago)")
    md_content.append("- **London Killzone:** 01:00 - 04:00 (J, heure Chicago)")
    md_content.append("")
    md_content.append("### Logique d'Entrée")
    md_content.append("")
    md_content.append("**LONG Setup:**")
    md_content.append("1. Prix passe sous Asia_Low")
    md_content.append("2. Formation d'un FVG Baissier")
    md_content.append("3. Clôture de bougie > Haut du FVG")
    md_content.append("")
    md_content.append("**SHORT Setup:**")
    md_content.append("1. Prix passe au-dessus d'Asia_High")
    md_content.append("2. Formation d'un FVG Haussier")
    md_content.append("3. Clôture de bougie < Bas du FVG")
    md_content.append("")
    md_content.append("### Gestion du Risque - 70/30 PARTIAL EXIT")
    md_content.append("- **Stop Loss:** Placé 0.5 points au-delà des niveaux Tokyo/Asia")
    md_content.append("  - LONG: SL = Asia_Low - 0.5 points")
    md_content.append("  - SHORT: SL = Asia_High + 0.5 points")
    md_content.append("")
    md_content.append("### Stratégie de Take Profit (70/30)")
    md_content.append("")
    md_content.append("**Sortie en 2 étapes:**")
    md_content.append("1. **70% de la position** fermée à l'équilibre")
    md_content.append("   - Equilibrium = (Asia_High + Asia_Low) / 2")
    md_content.append("   - Sécurise rapidement la majorité du profit")
    md_content.append("")
    md_content.append("2. **SL déplacé au breakeven** (prix d'entrée) après TP1")
    md_content.append("   - Élimine tout risque sur les 30% restants")
    md_content.append("")
    md_content.append("3. **30% restants** visent le niveau Tokyo opposé")
    md_content.append("   - LONG: TP2 à Asia_High")
    md_content.append("   - SHORT: TP2 à Asia_Low")
    md_content.append("   - Si pas atteint: sortie au breakeven ou time stop")
    md_content.append("")
    md_content.append("- **Time Stop:** 12:00 Chicago si ni SL ni TP touché")
    md_content.append("")
    md_content.append("---")
    md_content.append("")
    
    # Summary table
    md_content.append("## 📈 Résumé Global")
    md_content.append("")
    md_content.append("| Année | Total Trades | Win Rate (%) | Net Profit (pts) | Profit Factor | Max Drawdown (pts) |")
    md_content.append("|-------|--------------|--------------|------------------|---------------|---------------------|")
    
    total_trades_all = 0
    total_wins_all = 0
    total_profit_all = 0.0
    total_gross_profit = 0.0
    total_gross_loss = 0.0
    max_dd_all = 0.0
    
    for year in sorted(all_results.keys()):
        if all_results[year] and all_results[year]['total_trades'] > 0:
            r = all_results[year]
            md_content.append(f"| {year} | {r['total_trades']} | {r['win_rate']:.2f}% | {r['net_profit']:.2f} | {r['profit_factor']:.2f} | {r['max_drawdown']:.2f} |")
            
            # Accumulate totals
            total_trades_all += r['total_trades']
            total_wins_all += int(r['total_trades'] * r['win_rate'] / 100)
            total_profit_all += r['net_profit']
            
            # Calculate gross profit and loss
            if r['profit_factor'] > 0 and r['profit_factor'] != float('inf'):
                if r['profit_factor'] > 1:
                    gross_loss = r['net_profit'] / (r['profit_factor'] - 1) if r['profit_factor'] > 1 else 0
                    gross_profit = r['net_profit'] + gross_loss
                    total_gross_profit += gross_profit
                    total_gross_loss += gross_loss
            
            max_dd_all = max(max_dd_all, r['max_drawdown'])
        else:
            md_content.append(f"| {year} | N/A | N/A | N/A | N/A | N/A |")
    
    # Calculate overall metrics
    overall_win_rate = (total_wins_all / total_trades_all * 100) if total_trades_all > 0 else 0
    overall_pf = (total_gross_profit / total_gross_loss) if total_gross_loss > 0 else 0
    
    md_content.append(f"| **TOTAL** | **{total_trades_all}** | **{overall_win_rate:.2f}%** | **{total_profit_all:.2f}** | **{overall_pf:.2f}** | **{max_dd_all:.2f}** |")
    md_content.append("")
    md_content.append("---")
    md_content.append("")
    
    # Analysis and conclusions
    md_content.append("## 💡 Analyse et Conclusions")
    md_content.append("")
    md_content.append("### Performance Globale 70/30")
    md_content.append("")
    md_content.append(f"- **Total Trades:** {total_trades_all}")
    md_content.append(f"- **Win Rate Global:** {overall_win_rate:.2f}%")
    md_content.append(f"- **Profit Net Total:** {total_profit_all:.2f} points")
    md_content.append(f"- **Profit Factor Global:** {overall_pf:.2f}")
    md_content.append(f"- **Max Drawdown:** {max_dd_all:.2f} points")
    md_content.append("")
    
    md_content.append("### Avantages de la Stratégie 70/30")
    md_content.append("")
    md_content.append("1. **Sécurisation Rapide Optimisée:** 70% du profit sécurisé rapidement à l'équilibre")
    md_content.append("2. **Protection Maximale:** SL au breakeven après TP1 = zéro risque sur 30% restants")
    md_content.append("3. **Potentiel Conservé:** 30% reste en position pour capturer le mouvement complet")
    md_content.append("4. **Meilleur Ratio Sécurité/Potentiel:** Plus de profit sécurisé qu'avec 50/50")
    md_content.append("5. **Psychologie:** Encore moins de stress avec 70% du profit déjà sécurisé")
    md_content.append("")
    
    md_content.append("### Comparaison avec Autres Stratégies")
    md_content.append("")
    md_content.append("**vs 50/50 Partial:**")
    md_content.append("- Plus conservateur (70% vs 50% sécurisé)")
    md_content.append("- Moins de potentiel sur TP2 (30% vs 50%)")
    md_content.append("- Meilleure protection du capital")
    md_content.append("")
    md_content.append("**vs 100% Equilibrium:**")
    md_content.append("- Garde un potentiel de profit supplémentaire avec les 30%")
    md_content.append("- Protection breakeven après TP1")
    md_content.append("")
    md_content.append("**vs 100% Opposite:**")
    md_content.append("- Sécurise 70% du profit rapidement")
    md_content.append("- Réduit le risque de reversal")
    md_content.append("")
    
    md_content.append("### Recommandations")
    md_content.append("")
    md_content.append("1. **Idéal pour traders conservateurs:** Maximise la sécurisation du profit")
    md_content.append("2. **Gestion émotionnelle:** 70% sécurisé réduit significativement le stress")
    md_content.append("3. **Marchés volatils:** Protection optimale avec breakeven sur 30% restants")
    md_content.append("4. **Profil risque/rendement:** Excellent compromis entre sécurité et potentiel")
    md_content.append("")
    md_content.append("---")
    md_content.append("")
    md_content.append("## 📝 Notes Techniques")
    md_content.append("")
    md_content.append("- **Données:** Nasdaq 100 (NQ) en 5 minutes, timezone Chicago (UTC-5)")
    md_content.append("- **Période de Test:** 2018-2025")
    md_content.append("- **Une seule entrée par jour:** Premier signal valide dans la fenêtre 01:00-04:00")
    md_content.append("- **FVG (Fair Value Gap):** Écart entre le haut de la bougie n-2 et le bas de la bougie n (ou inverse)")
    md_content.append("- **Buffer SL:** 0.5 points pour éviter les stops sur les niveaux exacts")
    md_content.append("- **Breakeven:** SL déplacé au prix d'entrée après 70% sortis à TP1")
    md_content.append("- **Ratio 70/30:** Optimise sécurisation du profit tout en conservant un potentiel")
    md_content.append("")
    md_content.append("---")
    md_content.append("")
    md_content.append("*Rapport généré automatiquement par le script judas_swing_fvg_70_30_backtest.py*")
    
    # Write to file
    with open("RESULTATS_70_30.md", "w", encoding="utf-8") as f:
        f.write("\n".join(md_content))

if __name__ == "__main__":
    main()

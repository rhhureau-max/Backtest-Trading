#!/usr/bin/env python3
"""
Script to run fixed R:R backtest on all years and generate detailed results markdown file.
"""

import sys
import os
from datetime import datetime
from judas_swing_fvg_fixed_rr_backtest import run_backtest

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

# R:R ratios to test
rr_ratios = [1.0, 1.5, 2.0]
rr_names = {1.0: "A (1:1)", 1.5: "B (1:1.5)", 2.0: "C (1:2)"}

def main():
    """Generate detailed results for all years with fixed R:R strategy."""
    
    # Store all results
    all_results = {}
    
    print("="*80)
    print("GENERATING FIXED R:R STRATEGY RESULTS FOR ALL YEARS")
    print("="*80)
    print()
    print("Strategy: SL 0.5 points beyond Asia levels, TP based on R:R ratios")
    print()
    
    # Run backtest for each file and R:R ratio
    for csv_file in csv_files:
        if not os.path.exists(csv_file):
            print(f"⚠ Skipping {csv_file} (file not found)")
            continue
            
        year = csv_file.split()[0]
        print(f"\n{'='*80}")
        print(f"Processing Year: {year}")
        print('='*80)
        
        all_results[year] = {}
        
        for rr in rr_ratios:
            rr_name = rr_names[rr]
            print(f"\n  → Running R:R {rr_name}...")
            
            try:
                results = run_backtest(csv_file, rr)
                
                if results:
                    all_results[year][rr] = results
                    
                    print(f"    ✓ Total Trades: {results['total_trades']}")
                    print(f"    ✓ Win Rate: {results['win_rate']:.2f}%")
                    print(f"    ✓ Net Profit: {results['net_profit']:.2f} points")
                    print(f"    ✓ Profit Factor: {results['profit_factor']:.2f}")
                    print(f"    ✓ Max Drawdown: {results['max_drawdown']:.2f} points")
                else:
                    print(f"    ✗ No results for {year}")
                    all_results[year][rr] = None
                    
            except Exception as e:
                print(f"    ✗ Error: {str(e)}")
                all_results[year][rr] = None
    
    # Generate markdown file
    print("\n" + "="*80)
    print("GENERATING MARKDOWN FILE")
    print("="*80)
    
    generate_markdown(all_results)
    
    print("\n✓ Detailed results saved to: RESULTATS_FIXED_RR.md")
    print()

def generate_markdown(all_results):
    """Generate a detailed markdown file with all results."""
    
    md_content = []
    
    # Header
    md_content.append("# Résultats - Stratégie Judas Swing + FVG (SL Tokyo +/- 0.5pts, TP R:R fixe)")
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
    md_content.append("### Gestion du Risque - R:R FIXE")
    md_content.append("- **Stop Loss:** Placé 0.5 points au-delà des niveaux Tokyo/Asia")
    md_content.append("  - LONG: SL = Asia_Low - 0.5 points")
    md_content.append("  - SHORT: SL = Asia_High + 0.5 points")
    md_content.append("- **Take Profit:** Calculé selon le ratio R:R fixe")
    md_content.append("  - Scénario A (1:1): TP = Entry ± (SL_Distance × 1.0)")
    md_content.append("  - Scénario B (1:1.5): TP = Entry ± (SL_Distance × 1.5)")
    md_content.append("  - Scénario C (1:2): TP = Entry ± (SL_Distance × 2.0)")
    md_content.append("- **Time Stop:** 12:00 Chicago si ni SL ni TP touché")
    md_content.append("")
    md_content.append("---")
    md_content.append("")
    
    # Summary table for all years by R:R
    md_content.append("## 📈 Résumé Global par Scénario R:R")
    md_content.append("")
    
    for rr in rr_ratios:
        rr_name = rr_names[rr]
        md_content.append(f"### Scénario {rr_name}")
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
            if rr in all_results[year] and all_results[year][rr] and all_results[year][rr]['total_trades'] > 0:
                r = all_results[year][rr]
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
    
    # Detailed results per year
    md_content.append("## 📅 Résultats Détaillés par Année")
    md_content.append("")
    
    for year in sorted(all_results.keys()):
        md_content.append(f"### Année {year}")
        md_content.append("")
        md_content.append("| Scénario | Total Trades | Win Rate (%) | Net Profit (pts) | Profit Factor | Max Drawdown (pts) |")
        md_content.append("|----------|--------------|--------------|------------------|---------------|---------------------|")
        
        for rr in rr_ratios:
            rr_name = rr_names[rr]
            if rr in all_results[year] and all_results[year][rr] and all_results[year][rr]['total_trades'] > 0:
                r = all_results[year][rr]
                md_content.append(f"| Scénario {rr_name} | {r['total_trades']} | {r['win_rate']:.2f}% | {r['net_profit']:.2f} | {r['profit_factor']:.2f} | {r['max_drawdown']:.2f} |")
            else:
                md_content.append(f"| Scénario {rr_name} | N/A | N/A | N/A | N/A | N/A |")
        
        md_content.append("")
    
    md_content.append("---")
    md_content.append("")
    
    # Analysis and conclusions
    md_content.append("## 💡 Analyse et Conclusions")
    md_content.append("")
    md_content.append("### Performance Globale")
    md_content.append("")
    
    # Find best scenario
    best_scenario = None
    best_profit = -float('inf')
    
    for rr in rr_ratios:
        total_profit = sum(
            all_results[year][rr]['net_profit'] 
            for year in all_results 
            if rr in all_results[year] and all_results[year][rr] and all_results[year][rr]['total_trades'] > 0
        )
        if total_profit > best_profit:
            best_profit = total_profit
            best_scenario = rr_names[rr]
    
    if best_scenario:
        md_content.append(f"- **Meilleur Scénario:** Scénario {best_scenario} avec un profit net total de {best_profit:.2f} points")
        md_content.append("")
    
    md_content.append("### Observations Clés")
    md_content.append("")
    md_content.append("1. **SL Buffer:** Le buffer de 0.5 points permet d'éviter les stop loss prématurés sur les niveaux exacts")
    md_content.append("2. **R:R Adaptatif au Setup:** Chaque trade a un R:R fixe basé sur la distance du SL calculée")
    md_content.append("3. **Win Rate vs Profit:** Un R:R plus élevé diminue le win rate mais peut augmenter la rentabilité")
    md_content.append("4. **Simplicité:** Approche systématique et reproductible sans zones subjectives")
    md_content.append("")
    md_content.append("### Recommandations")
    md_content.append("")
    md_content.append("1. **Choix du R:R:** Adapter selon la volatilité du marché et les objectifs")
    md_content.append("2. **Gestion de Position:** Le R:R fixe simplifie le calcul de la taille de position")
    md_content.append("3. **Backtesting Continu:** Vérifier la robustesse sur nouvelles données")
    md_content.append("4. **Combinaison:** Possibilité de combiner avec des filtres de volatilité")
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
    md_content.append("")
    md_content.append("---")
    md_content.append("")
    md_content.append("*Rapport généré automatiquement par le script judas_swing_fvg_fixed_rr_backtest.py*")
    
    # Write to file
    with open("RESULTATS_FIXED_RR.md", "w", encoding="utf-8") as f:
        f.write("\n".join(md_content))

if __name__ == "__main__":
    main()

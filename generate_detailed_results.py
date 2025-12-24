#!/usr/bin/env python3
"""
Script to run backtests on all years and generate detailed results markdown file.
"""

import sys
import os
from datetime import datetime
from judas_swing_fvg_backtest import run_backtest

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

# TP scenarios to test
tp_scenarios = [20, 30, 40]
scenario_names = {20: "A (1:1)", 30: "B (1:1.5)", 40: "C (1:2)"}

def main():
    """Generate detailed results for all years."""
    
    # Store all results
    all_results = {}
    
    print("="*80)
    print("GENERATING DETAILED BACKTEST RESULTS FOR ALL YEARS")
    print("="*80)
    print()
    
    # Run backtest for each file and scenario
    for csv_file in csv_files:
        if not os.path.exists(csv_file):
            print(f"⚠ Skipping {csv_file} (file not found)")
            continue
            
        year = csv_file.split()[0]
        print(f"\n{'='*80}")
        print(f"Processing Year: {year}")
        print('='*80)
        
        all_results[year] = {}
        
        for tp_points in tp_scenarios:
            scenario_name = scenario_names[tp_points]
            print(f"\n  → Running Scenario {scenario_name} (TP={tp_points} pts)...")
            
            try:
                results = run_backtest(csv_file, tp_points)
                all_results[year][tp_points] = results
                
                print(f"    ✓ Total Trades: {results['total_trades']}")
                print(f"    ✓ Win Rate: {results['win_rate']:.2f}%")
                print(f"    ✓ Net Profit: {results['net_profit']:.2f} points")
                print(f"    ✓ Profit Factor: {results['profit_factor']:.2f}")
                print(f"    ✓ Max Drawdown: {results['max_drawdown']:.2f} points")
                
            except Exception as e:
                print(f"    ✗ Error: {str(e)}")
                all_results[year][tp_points] = None
    
    # Generate markdown file
    print("\n" + "="*80)
    print("GENERATING MARKDOWN FILE")
    print("="*80)
    
    generate_markdown(all_results)
    
    print("\n✓ Detailed results saved to: RESULTATS_DETAILLES.md")
    print()

def generate_markdown(all_results):
    """Generate a detailed markdown file with all results."""
    
    md_content = []
    
    # Header
    md_content.append("# Résultats Détaillés - Stratégie Judas Swing + FVG Inversion")
    md_content.append("")
    md_content.append(f"**Date de génération:** {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}")
    md_content.append("")
    md_content.append("---")
    md_content.append("")
    
    # Strategy description
    md_content.append("## 📊 Description de la Stratégie")
    md_content.append("")
    md_content.append("### Sessions de Trading")
    md_content.append("- **Asia Session:** 18:00 - 23:00 (J-1, heure Chicago)")
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
    md_content.append("### Gestion du Risque")
    md_content.append("- **Stop Loss Fixe:** 20 points")
    md_content.append("- **Scénario A:** TP = 20 points (Ratio 1:1)")
    md_content.append("- **Scénario B:** TP = 30 points (Ratio 1:1.5)")
    md_content.append("- **Scénario C:** TP = 40 points (Ratio 1:2)")
    md_content.append("- **Time Stop:** 12:00 Chicago si ni SL ni TP touché")
    md_content.append("")
    md_content.append("---")
    md_content.append("")
    
    # Summary table for all years
    md_content.append("## 📈 Résumé Global par Scénario")
    md_content.append("")
    
    for tp_points in [20, 30, 40]:
        scenario_name = scenario_names[tp_points]
        md_content.append(f"### Scénario {scenario_name} - TP = {tp_points} points")
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
            if tp_points in all_results[year] and all_results[year][tp_points]:
                r = all_results[year][tp_points]
                md_content.append(f"| {year} | {r['total_trades']} | {r['win_rate']:.2f}% | {r['net_profit']:.2f} | {r['profit_factor']:.2f} | {r['max_drawdown']:.2f} |")
                
                # Accumulate totals
                total_trades_all += r['total_trades']
                total_wins_all += int(r['total_trades'] * r['win_rate'] / 100)
                total_profit_all += r['net_profit']
                
                # Calculate gross profit and loss from profit factor
                if r['profit_factor'] > 0:
                    # profit_factor = gross_profit / abs(gross_loss)
                    # net_profit = gross_profit + gross_loss (where gross_loss is negative)
                    # So: gross_profit = net_profit + abs(gross_loss)
                    #     profit_factor = (net_profit + abs(gross_loss)) / abs(gross_loss)
                    #     profit_factor * abs(gross_loss) = net_profit + abs(gross_loss)
                    #     abs(gross_loss) * (profit_factor - 1) = net_profit
                    #     abs(gross_loss) = net_profit / (profit_factor - 1)
                    if r['profit_factor'] > 1:
                        gross_loss = r['net_profit'] / (r['profit_factor'] - 1)
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
        
        for tp_points in [20, 30, 40]:
            scenario_name = scenario_names[tp_points]
            if tp_points in all_results[year] and all_results[year][tp_points]:
                r = all_results[year][tp_points]
                md_content.append(f"| Scénario {scenario_name} | {r['total_trades']} | {r['win_rate']:.2f}% | {r['net_profit']:.2f} | {r['profit_factor']:.2f} | {r['max_drawdown']:.2f} |")
            else:
                md_content.append(f"| Scénario {scenario_name} | N/A | N/A | N/A | N/A | N/A |")
        
        md_content.append("")
    
    md_content.append("---")
    md_content.append("")
    
    # Analysis and conclusions
    md_content.append("## 💡 Analyse et Conclusions")
    md_content.append("")
    md_content.append("### Points Clés")
    md_content.append("")
    
    # Find best scenario
    best_scenario = None
    best_profit = -float('inf')
    
    for tp_points in [20, 30, 40]:
        total_profit = sum(
            all_results[year][tp_points]['net_profit'] 
            for year in all_results 
            if tp_points in all_results[year] and all_results[year][tp_points]
        )
        if total_profit > best_profit:
            best_profit = total_profit
            best_scenario = scenario_names[tp_points]
    
    md_content.append(f"- **Meilleur Scénario:** Scénario {best_scenario} avec un profit net total de {best_profit:.2f} points")
    md_content.append("")
    md_content.append("### Observations")
    md_content.append("")
    md_content.append("1. **Ratio Risk/Reward:** Les différents ratios (1:1, 1:1.5, 1:2) montrent des performances variables selon les années")
    md_content.append("2. **Win Rate:** Comme attendu, le win rate diminue avec l'augmentation du TP")
    md_content.append("3. **Profit Factor:** Un profit factor > 1 indique que la stratégie est rentable")
    md_content.append("4. **Drawdown:** Le drawdown maximum augmente avec des TP plus élevés")
    md_content.append("")
    md_content.append("### Recommandations")
    md_content.append("")
    md_content.append("1. **Optimisation:** Considérer l'ajout de filtres supplémentaires pour améliorer le win rate")
    md_content.append("2. **Gestion du Risque:** Adapter la taille de position en fonction du drawdown maximum")
    md_content.append("3. **Conditions de Marché:** Analyser les performances selon la volatilité du marché")
    md_content.append("4. **Time Stop:** Évaluer l'impact du time stop à 12:00 sur les résultats")
    md_content.append("")
    md_content.append("---")
    md_content.append("")
    md_content.append("## 📝 Notes Techniques")
    md_content.append("")
    md_content.append("- **Données:** Nasdaq 100 (NQ) en 5 minutes, timezone Chicago (UTC-5)")
    md_content.append("- **Période de Test:** 2018-2025")
    md_content.append("- **Une seule entrée par jour:** Premier signal valide dans la fenêtre 01:00-04:00")
    md_content.append("- **FVG (Fair Value Gap):** Écart entre le haut de la bougie n-2 et le bas de la bougie n (ou inverse)")
    md_content.append("")
    md_content.append("---")
    md_content.append("")
    md_content.append("*Rapport généré automatiquement par le script judas_swing_fvg_backtest.py*")
    
    # Write to file
    with open("RESULTATS_DETAILLES.md", "w", encoding="utf-8") as f:
        f.write("\n".join(md_content))

if __name__ == "__main__":
    main()

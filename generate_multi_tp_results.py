#!/usr/bin/env python3
"""
Script to run multiple TP strategies backtest on all years and generate detailed results.
"""

import sys
import os
from datetime import datetime
from judas_swing_fvg_multi_tp_backtest import run_backtest

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

# TP strategies to test
strategies = ['equilibrium', 'opposite', 'partial']
strategy_names = {
    'equilibrium': 'A (100% Equilibrium)',
    'opposite': 'B (100% Opposite)',
    'partial': 'C (50/50 Partial)'
}

def main():
    """Generate detailed results for all years with multiple TP strategies."""
    
    # Store all results
    all_results = {}
    
    print("="*80)
    print("GENERATING MULTIPLE TP STRATEGIES RESULTS FOR ALL YEARS")
    print("="*80)
    print()
    print("Strategy: SL 0.5 points beyond Tokyo, Multiple TP strategies")
    print()
    
    # Run backtest for each file and strategy
    for csv_file in csv_files:
        if not os.path.exists(csv_file):
            print(f"⚠ Skipping {csv_file} (file not found)")
            continue
            
        year = csv_file.split()[0]
        print(f"\n{'='*80}")
        print(f"Processing Year: {year}")
        print('='*80)
        
        all_results[year] = {}
        
        for strategy in strategies:
            strategy_name = strategy_names[strategy]
            print(f"\n  → Running Strategy {strategy_name}...")
            
            try:
                results = run_backtest(csv_file, strategy)
                
                if results:
                    all_results[year][strategy] = results
                    
                    print(f"    ✓ Total Trades: {results['total_trades']}")
                    print(f"    ✓ Win Rate: {results['win_rate']:.2f}%")
                    print(f"    ✓ Net Profit: {results['net_profit']:.2f} points")
                    print(f"    ✓ Profit Factor: {results['profit_factor']:.2f}")
                    print(f"    ✓ Max Drawdown: {results['max_drawdown']:.2f} points")
                else:
                    print(f"    ✗ No results for {year}")
                    all_results[year][strategy] = None
                    
            except Exception as e:
                print(f"    ✗ Error: {str(e)}")
                all_results[year][strategy] = None
    
    # Generate markdown file
    print("\n" + "="*80)
    print("GENERATING MARKDOWN FILE")
    print("="*80)
    
    generate_markdown(all_results)
    
    print("\n✓ Detailed results saved to: RESULTATS_MULTI_TP.md")
    print()

def generate_markdown(all_results):
    """Generate a detailed markdown file with all results."""
    
    md_content = []
    
    # Header
    md_content.append("# Résultats - Stratégie Judas Swing + FVG (SL Tokyo +/- 0.5pts, TP Multiples)")
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
    md_content.append("### Gestion du Risque - MULTIPLE TP")
    md_content.append("- **Stop Loss:** Placé 0.5 points au-delà des niveaux Tokyo/Asia")
    md_content.append("  - LONG: SL = Asia_Low - 0.5 points")
    md_content.append("  - SHORT: SL = Asia_High + 0.5 points")
    md_content.append("")
    md_content.append("### Stratégies de Take Profit")
    md_content.append("")
    md_content.append("**Stratégie A - 100% à l'Equilibrium:**")
    md_content.append("- Position complète fermée à l'équilibre")
    md_content.append("- Equilibrium = (Asia_High + Asia_Low) / 2")
    md_content.append("")
    md_content.append("**Stratégie B - 100% au niveau Opposé:**")
    md_content.append("- Position complète fermée au niveau Tokyo opposé")
    md_content.append("- LONG: TP à Asia_High")
    md_content.append("- SHORT: TP à Asia_Low")
    md_content.append("")
    md_content.append("**Stratégie C - 50% Equilibrium + 50% Opposé:**")
    md_content.append("- 50% de la position fermée à l'équilibre")
    md_content.append("- SL déplacé au breakeven (prix d'entrée) après premier TP")
    md_content.append("- 50% restant vise le niveau opposé ou breakeven")
    md_content.append("")
    md_content.append("- **Time Stop:** 12:00 Chicago si ni SL ni TP touché")
    md_content.append("")
    md_content.append("---")
    md_content.append("")
    
    # Summary table for all years by strategy
    md_content.append("## 📈 Résumé Global par Stratégie TP")
    md_content.append("")
    
    for strategy in strategies:
        strategy_name = strategy_names[strategy]
        md_content.append(f"### Stratégie {strategy_name}")
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
            if strategy in all_results[year] and all_results[year][strategy] and all_results[year][strategy]['total_trades'] > 0:
                r = all_results[year][strategy]
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
        md_content.append("| Stratégie | Total Trades | Win Rate (%) | Net Profit (pts) | Profit Factor | Max Drawdown (pts) |")
        md_content.append("|-----------|--------------|--------------|------------------|---------------|---------------------|")
        
        for strategy in strategies:
            strategy_name = strategy_names[strategy]
            if strategy in all_results[year] and all_results[year][strategy] and all_results[year][strategy]['total_trades'] > 0:
                r = all_results[year][strategy]
                md_content.append(f"| Stratégie {strategy_name} | {r['total_trades']} | {r['win_rate']:.2f}% | {r['net_profit']:.2f} | {r['profit_factor']:.2f} | {r['max_drawdown']:.2f} |")
            else:
                md_content.append(f"| Stratégie {strategy_name} | N/A | N/A | N/A | N/A | N/A |")
        
        md_content.append("")
    
    md_content.append("---")
    md_content.append("")
    
    # Analysis and conclusions
    md_content.append("## 💡 Analyse et Conclusions")
    md_content.append("")
    md_content.append("### Performance Globale")
    md_content.append("")
    
    # Find best strategy
    best_strategy = None
    best_profit = -float('inf')
    
    for strategy in strategies:
        total_profit = sum(
            all_results[year][strategy]['net_profit'] 
            for year in all_results 
            if strategy in all_results[year] and all_results[year][strategy] and all_results[year][strategy]['total_trades'] > 0
        )
        if total_profit > best_profit:
            best_profit = total_profit
            best_strategy = strategy_names[strategy]
    
    if best_strategy:
        md_content.append(f"- **Meilleure Stratégie:** Stratégie {best_strategy} avec un profit net total de {best_profit:.2f} points")
        md_content.append("")
    
    md_content.append("### Observations Clés")
    md_content.append("")
    md_content.append("1. **Stratégie Equilibrium:** Plus conservative, TP plus proche, win rate potentiellement plus élevé")
    md_content.append("2. **Stratégie Opposite:** TP plus ambitieux au niveau Tokyo opposé, R:R plus élevé")
    md_content.append("3. **Stratégie Partial:** Combine les avantages des deux avec gestion du risque optimisée")
    md_content.append("4. **Breakeven Management:** La stratégie partielle protège 50% du profit après premier TP")
    md_content.append("")
    md_content.append("### Avantages de la Stratégie Partielle")
    md_content.append("")
    md_content.append("- **Sécurisation rapide:** 50% du profit sécurisé à l'équilibre")
    md_content.append("- **Protection:** SL au breakeven après premier TP élimine le risque sur les 50% restants")
    md_content.append("- **Potentiel:** 50% reste en position pour capturer le mouvement complet")
    md_content.append("- **Psychologie:** Réduction du stress avec profit partiel sécurisé")
    md_content.append("")
    md_content.append("### Recommandations")
    md_content.append("")
    md_content.append("1. **Adaptabilité:** Choisir la stratégie selon les conditions de marché")
    md_content.append("2. **Volatilité:** En haute volatilité, privilégier la stratégie partielle")
    md_content.append("3. **Trending Markets:** En marchés directionnels forts, stratégie opposite peut être optimale")
    md_content.append("4. **Risk Management:** La stratégie partielle offre le meilleur compromis risque/rendement")
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
    md_content.append("- **Breakeven:** Dans la stratégie partielle, SL déplacé au prix d'entrée après premier TP")
    md_content.append("")
    md_content.append("---")
    md_content.append("")
    md_content.append("*Rapport généré automatiquement par le script judas_swing_fvg_multi_tp_backtest.py*")
    
    # Write to file
    with open("RESULTATS_MULTI_TP.md", "w", encoding="utf-8") as f:
        f.write("\n".join(md_content))

if __name__ == "__main__":
    main()

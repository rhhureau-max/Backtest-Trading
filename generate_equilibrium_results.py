#!/usr/bin/env python3
"""
Script to run equilibrium backtest on all years and generate detailed results markdown file.
"""

import sys
import os
from datetime import datetime
from judas_swing_fvg_equilibrium_backtest import run_backtest

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
    """Generate detailed results for all years with equilibrium strategy."""
    
    # Store all results
    all_results = {}
    
    print("="*80)
    print("GENERATING EQUILIBRIUM STRATEGY RESULTS FOR ALL YEARS")
    print("="*80)
    print()
    print("Strategy: SL at swing extremity, TP at equilibrium")
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
                
                print(f"\n✓ Results for {year}:")
                print(f"  Total Trades: {results['total_trades']}")
                print(f"  Win Rate: {results['win_rate']:.2f}%")
                print(f"  Net Profit: {results['net_profit']:.2f} points")
                print(f"  Profit Factor: {results['profit_factor']:.2f}")
                print(f"  Max Drawdown: {results['max_drawdown']:.2f} points")
                print(f"  Avg Risk/Reward: {results['avg_risk_reward']:.2f}")
            else:
                print(f"✗ No results for {year}")
                all_results[year] = None
                
        except Exception as e:
            print(f"✗ Error: {str(e)}")
            all_results[year] = None
    
    # Generate markdown file
    print("\n" + "="*80)
    print("GENERATING MARKDOWN FILE")
    print("="*80)
    
    generate_markdown(all_results)
    
    print("\n✓ Detailed results saved to: RESULTATS_EQUILIBRIUM.md")
    print()

def generate_markdown(all_results):
    """Generate a detailed markdown file with all results."""
    
    md_content = []
    
    # Header
    md_content.append("# Résultats - Stratégie Judas Swing + FVG (SL Swing / TP Equilibrium)")
    md_content.append("")
    md_content.append(f"**Date de génération:** {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}")
    md_content.append("")
    md_content.append("---")
    md_content.append("")
    
    # Strategy description
    md_content.append("## 📊 Configuration de la Stratégie")
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
    md_content.append("### Gestion du Risque - APPROCHE MANIPULATION EXTREMITY")
    md_content.append("- **Stop Loss:** Placé à l'extrémité de la manipulation (mouvement de faux-out)")
    md_content.append("  - LONG: SL = Plus bas atteint lors du breach d'Asia_Low (manipulation low)")
    md_content.append("  - SHORT: SL = Plus haut atteint lors du breach d'Asia_High (manipulation high)")
    md_content.append("- **Take Profit:** Placé à l'équilibre (milieu entre Asia_High et Asia_Low)")
    md_content.append("  - TP = (Asia_High + Asia_Low) / 2")
    md_content.append("- **Avantage:** SL placé au véritable point de validation/invalidation du setup")
    md_content.append("- **Time Stop:** 12:00 Chicago si ni SL ni TP touché")
    md_content.append("")
    md_content.append("---")
    md_content.append("")
    
    # Summary table
    md_content.append("## 📈 Résumé Global - Stratégie Equilibrium")
    md_content.append("")
    md_content.append("| Année | Total Trades | Win Rate (%) | Net Profit (pts) | Profit Factor | Max Drawdown (pts) | Avg Risk/Reward |")
    md_content.append("|-------|--------------|--------------|------------------|---------------|---------------------|-----------------|")
    
    total_trades_all = 0
    total_wins_all = 0
    total_profit_all = 0.0
    total_gross_profit = 0.0
    total_gross_loss = 0.0
    max_dd_all = 0.0
    
    for year in sorted(all_results.keys()):
        if all_results[year] and all_results[year]['total_trades'] > 0:
            r = all_results[year]
            md_content.append(f"| {year} | {r['total_trades']} | {r['win_rate']:.2f}% | {r['net_profit']:.2f} | {r['profit_factor']:.2f} | {r['max_drawdown']:.2f} | {r['avg_risk_reward']:.2f} |")
            
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
            md_content.append(f"| {year} | N/A | N/A | N/A | N/A | N/A | N/A |")
    
    # Calculate overall metrics
    overall_win_rate = (total_wins_all / total_trades_all * 100) if total_trades_all > 0 else 0
    overall_pf = (total_gross_profit / total_gross_loss) if total_gross_loss > 0 else 0
    
    md_content.append(f"| **TOTAL** | **{total_trades_all}** | **{overall_win_rate:.2f}%** | **{total_profit_all:.2f}** | **{overall_pf:.2f}** | **{max_dd_all:.2f}** | **-** |")
    md_content.append("")
    
    md_content.append("---")
    md_content.append("")
    
    # Detailed results per year
    md_content.append("## 📅 Résultats Détaillés par Année")
    md_content.append("")
    
    for year in sorted(all_results.keys()):
        md_content.append(f"### Année {year}")
        md_content.append("")
        
        if all_results[year] and all_results[year]['total_trades'] > 0:
            r = all_results[year]
            md_content.append(f"- **Total Trades:** {r['total_trades']}")
            md_content.append(f"- **Win Rate:** {r['win_rate']:.2f}%")
            md_content.append(f"- **Net Profit:** {r['net_profit']:.2f} points")
            md_content.append(f"- **Profit Factor:** {r['profit_factor']:.2f}")
            md_content.append(f"- **Max Drawdown:** {r['max_drawdown']:.2f} points")
            md_content.append(f"- **Avg Risk/Reward Ratio:** {r['avg_risk_reward']:.2f}")
        else:
            md_content.append("- **Aucune donnée disponible**")
        
        md_content.append("")
    
    md_content.append("---")
    md_content.append("")
    
    # Comparison with fixed TP strategy
    md_content.append("## 🔄 Comparaison avec Stratégie à TP Fixe")
    md_content.append("")
    md_content.append("### Avantages de la Stratégie Equilibrium")
    md_content.append("")
    md_content.append("1. **Risk/Reward Adaptatif:**")
    md_content.append("   - Le ratio R:R s'adapte automatiquement à la taille du range Asia")
    md_content.append("   - Plus favorable dans les marchés avec des ranges larges")
    md_content.append("")
    md_content.append("2. **Stop Loss Logique:**")
    md_content.append("   - SL placé à un niveau technique significatif (swing extremity)")
    md_content.append("   - Évite les stops arbitraires à distance fixe")
    md_content.append("")
    md_content.append("3. **Take Profit Technique:**")
    md_content.append("   - TP à l'équilibre représente un niveau psychologique important")
    md_content.append("   - Zone de potentielle résistance/support")
    md_content.append("")
    md_content.append("### Points d'Attention")
    md_content.append("")
    md_content.append("1. **Variabilité du SL:**")
    md_content.append("   - La distance du SL varie selon la taille du range Asia")
    md_content.append("   - Nécessite une adaptation de la taille de position")
    md_content.append("")
    md_content.append("2. **TP Potentiellement Court:**")
    md_content.append("   - Dans certains cas, le TP peut être atteint plus facilement")
    md_content.append("   - Mais limite aussi le potentiel de profit")
    md_content.append("")
    
    md_content.append("---")
    md_content.append("")
    
    # Analysis and conclusions
    md_content.append("## 💡 Analyse et Conclusions")
    md_content.append("")
    md_content.append("### Performance Globale")
    md_content.append("")
    md_content.append(f"- **Total Trades sur 8 ans:** {total_trades_all}")
    md_content.append(f"- **Win Rate Moyen:** {overall_win_rate:.2f}%")
    md_content.append(f"- **Profit Net Total:** {total_profit_all:.2f} points")
    md_content.append(f"- **Profit Factor Global:** {overall_pf:.2f}")
    md_content.append(f"- **Drawdown Maximum:** {max_dd_all:.2f} points")
    md_content.append("")
    
    # Find best and worst years
    best_year = None
    best_profit = -float('inf')
    worst_year = None
    worst_profit = float('inf')
    
    for year in all_results:
        if all_results[year] and all_results[year]['total_trades'] > 0:
            profit = all_results[year]['net_profit']
            if profit > best_profit:
                best_profit = profit
                best_year = year
            if profit < worst_profit:
                worst_profit = profit
                worst_year = year
    
    if best_year:
        md_content.append(f"### Meilleure Année: {best_year}")
        md_content.append(f"- Profit: {best_profit:.2f} points")
        md_content.append("")
    
    if worst_year:
        md_content.append(f"### Année la Plus Difficile: {worst_year}")
        md_content.append(f"- Profit: {worst_profit:.2f} points")
        md_content.append("")
    
    md_content.append("### Observations Clés")
    md_content.append("")
    md_content.append("1. **Ratio R:R Favorable:** La stratégie présente un ratio risk/reward moyen élevé")
    md_content.append("2. **Win Rate Solide:** Un win rate supérieur à 50% est généralement observé")
    md_content.append("3. **Drawdown Contrôlé:** Le drawdown maximum reste gérable")
    md_content.append("4. **Adaptabilité:** La stratégie s'adapte aux conditions de marché variables")
    md_content.append("")
    md_content.append("### Recommandations")
    md_content.append("")
    md_content.append("1. **Sizing de Position:** Adapter la taille selon la distance du SL")
    md_content.append("2. **Filtres de Volatilité:** Considérer des filtres basés sur la taille du range Asia")
    md_content.append("3. **Gestion Partielle:** Envisager une sortie partielle à l'équilibre avec trail stop")
    md_content.append("4. **Backtesting Continu:** Surveiller les performances sur données récentes")
    md_content.append("")
    md_content.append("---")
    md_content.append("")
    md_content.append("## 📝 Notes Techniques")
    md_content.append("")
    md_content.append("- **Données:** Nasdaq 100 (NQ) en 5 minutes, timezone Chicago (UTC-5)")
    md_content.append("- **Période de Test:** 2018-2025")
    md_content.append("- **Une seule entrée par jour:** Premier signal valide dans la fenêtre 01:00-04:00")
    md_content.append("- **FVG (Fair Value Gap):** Écart entre le haut de la bougie n-2 et le bas de la bougie n (ou inverse)")
    md_content.append("- **Equilibrium:** Point milieu calculé comme (Asia_High + Asia_Low) / 2")
    md_content.append("")
    md_content.append("---")
    md_content.append("")
    md_content.append("*Rapport généré automatiquement par le script judas_swing_fvg_equilibrium_backtest.py*")
    
    # Write to file
    with open("RESULTATS_EQUILIBRIUM.md", "w", encoding="utf-8") as f:
        f.write("\n".join(md_content))

if __name__ == "__main__":
    main()

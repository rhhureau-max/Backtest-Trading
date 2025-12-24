#!/usr/bin/env python3
"""
Script to generate a markdown file with detailed information about the last trades from 2025.
"""

import pandas as pd
from datetime import datetime
from judas_swing_fvg_equilibrium_backtest import run_backtest

def format_time(time_obj):
    """Format time object for display"""
    if hasattr(time_obj, 'strftime'):
        return time_obj.strftime('%H:%M:%S')
    return str(time_obj)

def main():
    """Extract and display last trades from 2025"""
    
    # Run backtest on 2025 data
    csv_file = "2025 5m.csv"
    results = run_backtest(csv_file)
    
    if not results or not results['trades']:
        print("Aucun trade trouvé pour 2025")
        return
    
    # Get last 10 trades
    all_trades = results['trades']
    last_trades = all_trades[-10:] if len(all_trades) >= 10 else all_trades
    
    # Generate markdown content
    md_content = []
    
    md_content.append("# Derniers Trades de 2025 - Stratégie Equilibrium")
    md_content.append("")
    md_content.append(f"**Date de génération:** {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}")
    md_content.append("")
    md_content.append(f"Affichage des **{len(last_trades)} derniers trades** sur **{results['total_trades']} trades au total** en 2025")
    md_content.append("")
    md_content.append("---")
    md_content.append("")
    
    for i, trade in enumerate(last_trades, 1):
        trade_num = len(all_trades) - len(last_trades) + i
        
        md_content.append(f"## Trade #{trade_num} - {trade['date'].strftime('%d/%m/%Y')}")
        md_content.append("")
        
        # Setup & Logic
        md_content.append("### 📊 Setup & Logique")
        md_content.append("")
        md_content.append(f"**Direction:** `{trade['direction']}`")
        md_content.append("")
        
        if trade['direction'] == 'LONG':
            md_content.append("**Logique d'entrée:**")
            md_content.append("1. Prix a cassé **Asia_Low** vers le bas")
            md_content.append("2. Formation d'un **FVG Baissier** (Fair Value Gap)")
            md_content.append("3. Prix revient et clôture **au-dessus du haut du FVG**")
            md_content.append("")
            md_content.append("**Détails du setup:**")
            md_content.append(f"- Asia_Low breached: `{trade['asia_low']:.2f}`")
            md_content.append(f"- FVG Baissier: `[{trade['fvg_low']:.2f} - {trade['fvg_high']:.2f}]`")
            md_content.append(f"- Clôture d'entrée > `{trade['fvg_high']:.2f}` ✓")
        else:
            md_content.append("**Logique d'entrée:**")
            md_content.append("1. Prix a cassé **Asia_High** vers le haut")
            md_content.append("2. Formation d'un **FVG Haussier** (Fair Value Gap)")
            md_content.append("3. Prix revient et clôture **en-dessous du bas du FVG**")
            md_content.append("")
            md_content.append("**Détails du setup:**")
            md_content.append(f"- Asia_High breached: `{trade['asia_high']:.2f}`")
            md_content.append(f"- FVG Haussier: `[{trade['fvg_low']:.2f} - {trade['fvg_high']:.2f}]`")
            md_content.append(f"- Clôture d'entrée < `{trade['fvg_low']:.2f}` ✓")
        
        md_content.append("")
        
        # Asia Session Levels
        md_content.append("### 📈 Niveaux Asia Session")
        md_content.append("")
        md_content.append("| Niveau | Prix |")
        md_content.append("|--------|------|")
        md_content.append(f"| **Asia High** | {trade['asia_high']:.2f} |")
        md_content.append(f"| **Asia Low** | {trade['asia_low']:.2f} |")
        md_content.append(f"| **Range Asia** | {trade['asia_high'] - trade['asia_low']:.2f} points |")
        md_content.append(f"| **Equilibrium** | {trade['equilibrium']:.2f} |")
        md_content.append("")
        
        # Entry Details
        md_content.append("### 🎯 Entrée en Position")
        md_content.append("")
        md_content.append(f"- **Heure d'entrée:** `{format_time(trade['entry_time'])}` (heure Chicago)")
        md_content.append(f"- **Prix d'entrée:** `{trade['entry_price']:.2f}`")
        md_content.append("")
        
        # Risk Management
        md_content.append("### ⚠️ Gestion du Risque")
        md_content.append("")
        md_content.append("| Paramètre | Valeur |")
        md_content.append("|-----------|--------|")
        md_content.append(f"| **Stop Loss (SL)** | {trade['sl_level']:.2f} |")
        md_content.append(f"| **Take Profit (TP)** | {trade['tp_level']:.2f} |")
        md_content.append(f"| **Distance SL** | {abs(trade['sl_points']):.2f} points |")
        md_content.append(f"| **Distance TP** | {abs(trade['tp_points']):.2f} points |")
        
        # Calculate proper R:R
        sl_dist = abs(trade['entry_price'] - trade['sl_level'])
        tp_dist = abs(trade['tp_level'] - trade['entry_price'])
        rr_ratio = tp_dist / sl_dist if sl_dist > 0 else 0
        
        md_content.append(f"| **Ratio R:R** | 1:{rr_ratio:.2f} |")
        md_content.append("")
        
        # Exit Details
        md_content.append("### 🏁 Sortie de Position")
        md_content.append("")
        
        exit_icon = ""
        exit_status = ""
        if trade['exit_type'] == 'TP':
            exit_icon = "✅"
            exit_status = "**Take Profit touché!**"
        elif trade['exit_type'] == 'SL':
            exit_icon = "❌"
            exit_status = "**Stop Loss touché!**"
        else:
            exit_icon = "⏰"
            exit_status = "**Time Stop (12:00 Chicago)**"
        
        md_content.append(f"- **Type de sortie:** {exit_icon} {exit_status}")
        md_content.append(f"- **Prix de sortie:** `{trade['exit_price']:.2f}`")
        md_content.append("")
        
        # Result
        md_content.append("### 💰 Résultat")
        md_content.append("")
        pnl_sign = "+" if trade['pnl'] > 0 else ""
        pnl_emoji = "✅" if trade['pnl'] > 0 else "❌" if trade['pnl'] < 0 else "➖"
        md_content.append(f"**P&L:** {pnl_emoji} **{pnl_sign}{trade['pnl']:.2f} points**")
        md_content.append("")
        
        # Visual representation
        md_content.append("### 📊 Représentation Visuelle")
        md_content.append("")
        md_content.append("```")
        if trade['direction'] == 'LONG':
            md_content.append(f"Asia High ────────────── {trade['asia_high']:.2f}")
            md_content.append(f"                         ↑")
            md_content.append(f"TP (Equilibrium) ─────── {trade['tp_level']:.2f} ← 🎯 TARGET")
            md_content.append(f"                         ↑")
            md_content.append(f"Prix d'entrée ────────── {trade['entry_price']:.2f} ← 📍 ENTRY")
            md_content.append(f"                         ↓")
            md_content.append(f"SL (Asia Low) ────────── {trade['sl_level']:.2f} ← 🛑 STOP")
        else:
            md_content.append(f"SL (Asia High) ───────── {trade['sl_level']:.2f} ← 🛑 STOP")
            md_content.append(f"                         ↓")
            md_content.append(f"Prix d'entrée ────────── {trade['entry_price']:.2f} ← 📍 ENTRY")
            md_content.append(f"                         ↓")
            md_content.append(f"TP (Equilibrium) ─────── {trade['tp_level']:.2f} ← 🎯 TARGET")
            md_content.append(f"                         ↓")
            md_content.append(f"Asia Low ─────────────── {trade['asia_low']:.2f}")
        md_content.append("```")
        md_content.append("")
        md_content.append("---")
        md_content.append("")
    
    # Summary statistics
    md_content.append("## 📊 Statistiques des Derniers Trades")
    md_content.append("")
    
    trades_df = pd.DataFrame(last_trades)
    winning_trades = len(trades_df[trades_df['pnl'] > 0])
    losing_trades = len(trades_df[trades_df['pnl'] < 0])
    win_rate = (winning_trades / len(trades_df) * 100) if len(trades_df) > 0 else 0
    total_pnl = trades_df['pnl'].sum()
    avg_win = trades_df[trades_df['pnl'] > 0]['pnl'].mean() if winning_trades > 0 else 0
    avg_loss = trades_df[trades_df['pnl'] < 0]['pnl'].mean() if losing_trades > 0 else 0
    
    md_content.append("| Métrique | Valeur |")
    md_content.append("|----------|--------|")
    md_content.append(f"| **Nombre de trades** | {len(trades_df)} |")
    md_content.append(f"| **Trades gagnants** | {winning_trades} |")
    md_content.append(f"| **Trades perdants** | {losing_trades} |")
    md_content.append(f"| **Win Rate** | {win_rate:.2f}% |")
    md_content.append(f"| **P&L Total** | {total_pnl:+.2f} points |")
    md_content.append(f"| **Gain moyen** | +{avg_win:.2f} points |")
    md_content.append(f"| **Perte moyenne** | {avg_loss:.2f} points |")
    md_content.append("")
    
    md_content.append("---")
    md_content.append("")
    md_content.append("## 📝 Notes")
    md_content.append("")
    md_content.append("- **Stratégie:** Judas Swing + FVG Inversion avec gestion du risque à l'équilibre")
    md_content.append("- **SL Placement:** À l'extrémité du swing (Asia_Low pour LONG, Asia_High pour SHORT)")
    md_content.append("- **TP Placement:** À l'équilibre = (Asia_High + Asia_Low) / 2")
    md_content.append("- **Time Stop:** 12:00 Chicago si ni SL ni TP touché avant")
    md_content.append("- **Timezone:** Chicago (UTC-5)")
    md_content.append("")
    md_content.append("*Rapport généré automatiquement*")
    
    # Write to file
    with open("DERNIERS_TRADES_2025.md", "w", encoding="utf-8") as f:
        f.write("\n".join(md_content))
    
    print("✓ Fichier DERNIERS_TRADES_2025.md créé avec succès!")
    print(f"  {len(last_trades)} trades détaillés")
    print(f"  Win Rate: {win_rate:.2f}%")
    print(f"  P&L Total: {total_pnl:+.2f} points")

if __name__ == "__main__":
    main()

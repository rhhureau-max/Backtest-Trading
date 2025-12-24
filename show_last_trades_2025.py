#!/usr/bin/env python3
"""
Script to display detailed information about the last trades from 2025
with entry/exit times, logic, and SL/TP placements.
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
    
    print("="*100)
    print("DERNIERS TRADES DE 2025 - STRATÉGIE EQUILIBRIUM")
    print("="*100)
    print()
    
    # Run backtest on 2025 data
    csv_file = "2025 5m.csv"
    results = run_backtest(csv_file)
    
    if not results or not results['trades']:
        print("Aucun trade trouvé pour 2025")
        return
    
    # Get last 10 trades
    all_trades = results['trades']
    last_trades = all_trades[-10:] if len(all_trades) >= 10 else all_trades
    
    print(f"Affichage des {len(last_trades)} derniers trades sur {results['total_trades']} trades au total\n")
    print("="*100)
    
    for i, trade in enumerate(last_trades, 1):
        print(f"\n{'='*100}")
        print(f"TRADE #{len(all_trades) - len(last_trades) + i} - {trade['date'].strftime('%d/%m/%Y')}")
        print(f"{'='*100}")
        
        # Trade direction and setup
        print(f"\n📊 SETUP & LOGIQUE:")
        print(f"  Direction: {trade['direction']}")
        
        if trade['direction'] == 'LONG':
            print(f"  Logique: Prix a cassé Asia_Low → FVG Baissier formé → Clôture > Haut FVG")
            print(f"  ├─ Asia_Low breached: {trade['asia_low']:.2f}")
            print(f"  ├─ FVG Baissier: [{trade['fvg_low']:.2f} - {trade['fvg_high']:.2f}]")
            print(f"  └─ Clôture de la bougie d'entrée > {trade['fvg_high']:.2f}")
        else:
            print(f"  Logique: Prix a cassé Asia_High → FVG Haussier formé → Clôture < Bas FVG")
            print(f"  ├─ Asia_High breached: {trade['asia_high']:.2f}")
            print(f"  ├─ FVG Haussier: [{trade['fvg_low']:.2f} - {trade['fvg_high']:.2f}]")
            print(f"  └─ Clôture de la bougie d'entrée < {trade['fvg_low']:.2f}")
        
        # Asia session levels
        print(f"\n📈 NIVEAUX ASIA SESSION:")
        print(f"  Asia High: {trade['asia_high']:.2f}")
        print(f"  Asia Low:  {trade['asia_low']:.2f}")
        print(f"  Range Asia: {trade['asia_high'] - trade['asia_low']:.2f} points")
        print(f"  Equilibrium: {trade['equilibrium']:.2f}")
        
        # Entry details
        print(f"\n🎯 ENTRÉE EN POSITION:")
        print(f"  Heure d'entrée: {format_time(trade['entry_time'])} (Chicago)")
        print(f"  Prix d'entrée: {trade['entry_price']:.2f}")
        
        # Risk management
        print(f"\n⚠️  GESTION DU RISQUE:")
        print(f"  Stop Loss (SL): {trade['sl_level']:.2f}")
        print(f"  Take Profit (TP): {trade['tp_level']:.2f}")
        print(f"  Distance SL: {trade['sl_points']:.2f} points")
        print(f"  Distance TP: {trade['tp_points']:.2f} points")
        print(f"  Ratio R:R: 1:{trade['tp_points']/trade['sl_points']:.2f}")
        
        # Exit details
        print(f"\n🏁 SORTIE DE POSITION:")
        print(f"  Type de sortie: {trade['exit_type']}")
        
        if trade['exit_type'] == 'TP':
            print(f"  ✅ Take Profit touché!")
        elif trade['exit_type'] == 'SL':
            print(f"  ❌ Stop Loss touché!")
        else:
            print(f"  ⏰ Time Stop (12:00 Chicago)")
        
        print(f"  Prix de sortie: {trade['exit_price']:.2f}")
        
        # Result
        print(f"\n💰 RÉSULTAT:")
        pnl_sign = "+" if trade['pnl'] > 0 else ""
        pnl_emoji = "✅" if trade['pnl'] > 0 else "❌" if trade['pnl'] < 0 else "➖"
        print(f"  P&L: {pnl_emoji} {pnl_sign}{trade['pnl']:.2f} points")
        
        # Visual representation
        print(f"\n📊 REPRÉSENTATION VISUELLE:")
        if trade['direction'] == 'LONG':
            print(f"  Asia High ────────────── {trade['asia_high']:.2f}")
            print(f"  TP (Equilibrium) ─────── {trade['tp_level']:.2f} ← TARGET")
            print(f"  Prix d'entrée ────────── {trade['entry_price']:.2f} ← ENTRY")
            print(f"  SL (Asia Low) ────────── {trade['sl_level']:.2f} ← STOP")
        else:
            print(f"  SL (Asia High) ───────── {trade['sl_level']:.2f} ← STOP")
            print(f"  Prix d'entrée ────────── {trade['entry_price']:.2f} ← ENTRY")
            print(f"  TP (Equilibrium) ─────── {trade['tp_level']:.2f} ← TARGET")
            print(f"  Asia Low ─────────────── {trade['asia_low']:.2f}")
    
    print("\n" + "="*100)
    print("FIN DES DERNIERS TRADES")
    print("="*100)
    
    # Summary statistics for these trades
    trades_df = pd.DataFrame(last_trades)
    winning_trades = len(trades_df[trades_df['pnl'] > 0])
    losing_trades = len(trades_df[trades_df['pnl'] < 0])
    win_rate = (winning_trades / len(trades_df) * 100) if len(trades_df) > 0 else 0
    total_pnl = trades_df['pnl'].sum()
    
    print(f"\n📊 STATISTIQUES DES {len(last_trades)} DERNIERS TRADES:")
    print(f"  Trades gagnants: {winning_trades}")
    print(f"  Trades perdants: {losing_trades}")
    print(f"  Win Rate: {win_rate:.2f}%")
    print(f"  P&L Total: {total_pnl:+.2f} points")
    print()

if __name__ == "__main__":
    main()

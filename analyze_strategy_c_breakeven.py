#!/usr/bin/env python3
"""
Script to analyze Strategy C (50/50 Partial) breakeven statistics.
"""

import pandas as pd
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

def main():
    """Analyze Strategy C breakeven statistics."""
    
    print("="*80)
    print("STRATEGY C (50/50 PARTIAL) - ANALYSE BREAKEVEN")
    print("="*80)
    print()
    
    all_trades = []
    
    # Run backtest for each file
    for csv_file in csv_files:
        try:
            year = csv_file.split()[0]
            print(f"Processing {year}...")
            
            results = run_backtest(csv_file, 'partial')
            
            if results and results['trades']:
                all_trades.extend(results['trades'])
                
        except Exception as e:
            print(f"Error processing {csv_file}: {e}")
    
    if not all_trades:
        print("No trades found!")
        return
    
    # Convert to DataFrame
    trades_df = pd.DataFrame(all_trades)
    
    # Analyze trades
    total_trades = len(trades_df)
    
    # Count trades that hit TP1 (equilibrium)
    tp1_hit_trades = trades_df[trades_df.get('tp1_hit', False) == True]
    tp1_hit_count = len(tp1_hit_trades)
    
    # Among trades that hit TP1, count exit types
    if tp1_hit_count > 0:
        # Trades stopped at breakeven
        breakeven_trades = tp1_hit_trades[tp1_hit_trades['exit_type'].str.contains('Breakeven', na=False)]
        breakeven_count = len(breakeven_trades)
        
        # Trades that hit TP2 (full profit)
        tp2_trades = tp1_hit_trades[tp1_hit_trades['exit_type'] == 'TP2']
        tp2_count = len(tp2_trades)
        
        # Trades that hit time stop after TP1
        time_stop_partial = tp1_hit_trades[tp1_hit_trades['exit_type'].str.contains('TIME_STOP.*Partial', na=False)]
        time_stop_partial_count = len(time_stop_partial)
    else:
        breakeven_count = 0
        tp2_count = 0
        time_stop_partial_count = 0
    
    # Trades that never hit TP1 (full SL or time stop)
    no_tp1_trades = trades_df[trades_df.get('tp1_hit', False) == False]
    no_tp1_count = len(no_tp1_trades)
    
    # Full SL (never hit TP1)
    full_sl_trades = no_tp1_trades[no_tp1_trades['exit_type'] == 'SL']
    full_sl_count = len(full_sl_trades)
    
    # Time stop without TP1
    time_stop_full = no_tp1_trades[no_tp1_trades['exit_type'] == 'TIME_STOP']
    time_stop_full_count = len(time_stop_full)
    
    # Display results
    print()
    print("="*80)
    print("RÉSULTATS DÉTAILLÉS")
    print("="*80)
    print()
    
    print(f"TOTAL TRADES: {total_trades}")
    print()
    
    print("─" * 80)
    print("RÉPARTITION DES TRADES")
    print("─" * 80)
    print()
    
    print(f"1. Trades ayant atteint TP1 (Equilibrium):")
    print(f"   - Nombre: {tp1_hit_count}")
    print(f"   - Pourcentage: {tp1_hit_count/total_trades*100:.2f}%")
    print()
    
    if tp1_hit_count > 0:
        print(f"   Parmi ces trades:")
        print(f"   a) Stoppés au BREAKEVEN: {breakeven_count} ({breakeven_count/tp1_hit_count*100:.2f}% des TP1 atteints)")
        print(f"      → 50% profit à l'équilibre, 50% à breakeven = Profit partiel")
        print()
        print(f"   b) TP2 atteint (Opposé): {tp2_count} ({tp2_count/tp1_hit_count*100:.2f}% des TP1 atteints)")
        print(f"      → 50% profit à l'équilibre + 50% profit à l'opposé = Profit complet")
        print()
        print(f"   c) Time Stop après TP1: {time_stop_partial_count} ({time_stop_partial_count/tp1_hit_count*100:.2f}% des TP1 atteints)")
        print(f"      → 50% profit à l'équilibre + 50% au prix du marché à 12:00")
        print()
    
    print(f"2. Trades N'AYANT PAS atteint TP1:")
    print(f"   - Nombre: {no_tp1_count}")
    print(f"   - Pourcentage: {no_tp1_count/total_trades*100:.2f}%")
    print()
    
    if no_tp1_count > 0:
        print(f"   Parmi ces trades:")
        print(f"   a) Stop Loss complet: {full_sl_count} ({full_sl_count/no_tp1_count*100:.2f}% des non-TP1)")
        print(f"      → Perte complète")
        print()
        print(f"   b) Time Stop sans TP1: {time_stop_full_count} ({time_stop_full_count/no_tp1_count*100:.2f}% des non-TP1)")
        print(f"      → Sortie au prix du marché à 12:00")
        print()
    
    print("="*80)
    print("RATIOS GLOBAUX")
    print("="*80)
    print()
    
    print(f"Sur {total_trades} trades au total:")
    print()
    print(f"• Trades avec TP1 atteint: {tp1_hit_count} ({tp1_hit_count/total_trades*100:.2f}%)")
    print(f"  ├─ Dont breakeven sur 50% restant: {breakeven_count} ({breakeven_count/total_trades*100:.2f}% du total)")
    print(f"  ├─ Dont TP2 complet: {tp2_count} ({tp2_count/total_trades*100:.2f}% du total)")
    print(f"  └─ Dont time stop partiel: {time_stop_partial_count} ({time_stop_partial_count/total_trades*100:.2f}% du total)")
    print()
    print(f"• Trades sans TP1: {no_tp1_count} ({no_tp1_count/total_trades*100:.2f}%)")
    print(f"  ├─ Dont SL complet: {full_sl_count} ({full_sl_count/total_trades*100:.2f}% du total)")
    print(f"  └─ Dont time stop complet: {time_stop_full_count} ({time_stop_full_count/total_trades*100:.2f}% du total)")
    print()
    
    print("="*80)
    print("INTERPRÉTATION")
    print("="*80)
    print()
    
    if tp1_hit_count > 0:
        breakeven_ratio = breakeven_count / tp1_hit_count * 100
        print(f"🔹 Parmi les trades ayant sécurisé 50% à l'équilibre:")
        print(f"   {breakeven_ratio:.1f}% sont revenus au breakeven sur les 50% restants")
        print(f"   → Cela représente {breakeven_count} trades avec profit partiel protégé")
        print()
        
        tp2_ratio = tp2_count / tp1_hit_count * 100
        print(f"🔹 {tp2_ratio:.1f}% ont atteint le TP2 complet (profit maximum)")
        print()
        
        protected_ratio = (breakeven_count + tp2_count + time_stop_partial_count) / total_trades * 100
        print(f"🔹 Au total, {protected_ratio:.1f}% des trades ont bénéficié de la protection breakeven")
        print(f"   → Capital protégé après avoir sécurisé 50% du profit!")
        print()
    
    print("="*80)
    
    # Calculate P&L breakdown
    print()
    print("ANALYSE P&L")
    print("="*80)
    print()
    
    if tp1_hit_count > 0:
        breakeven_pnl = breakeven_trades['pnl'].sum() if len(breakeven_trades) > 0 else 0
        tp2_pnl = tp2_trades['pnl'].sum() if len(tp2_trades) > 0 else 0
        time_stop_partial_pnl = time_stop_partial['pnl'].sum() if len(time_stop_partial) > 0 else 0
        
        print(f"P&L des trades avec TP1:")
        print(f"  - Breakeven (50% profit + 50% breakeven): {breakeven_pnl:.2f} points")
        print(f"  - TP2 complet: {tp2_pnl:.2f} points")
        print(f"  - Time stop partiel: {time_stop_partial_pnl:.2f} points")
        print(f"  → Total P&L positif: {breakeven_pnl + tp2_pnl + time_stop_partial_pnl:.2f} points")
        print()
    
    if no_tp1_count > 0:
        full_sl_pnl = full_sl_trades['pnl'].sum() if len(full_sl_trades) > 0 else 0
        time_stop_full_pnl = time_stop_full['pnl'].sum() if len(time_stop_full) > 0 else 0
        
        print(f"P&L des trades sans TP1:")
        print(f"  - SL complet: {full_sl_pnl:.2f} points")
        print(f"  - Time stop complet: {time_stop_full_pnl:.2f} points")
        print(f"  → Total P&L négatif/neutre: {full_sl_pnl + time_stop_full_pnl:.2f} points")
        print()
    
    total_pnl = trades_df['pnl'].sum()
    print(f"P&L NET TOTAL: {total_pnl:.2f} points")
    print()

if __name__ == "__main__":
    main()

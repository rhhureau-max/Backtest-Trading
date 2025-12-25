"""
Analyze Exit Statistics for 70/30 No-Timestop Strategy
========================================================
This script analyzes how trades exit in the 70/30 no-timestop strategy:
- How many reach TP1 (Equilibrium)
- How many reach TP2 (Opposite)
- How many hit Breakeven after TP1
- How many hit SL without reaching TP1
"""

import pandas as pd
import glob
from judas_swing_fvg_70_30_no_timestop_backtest import JudasSwingFVG70_30NoTimestopBacktest


def analyze_all_years():
    """Analyze exit statistics across all years"""
    
    # Get all 5m CSV files (not 15m)
    csv_files = sorted([f for f in glob.glob('*5m.csv') if '15m' not in f])
    
    print("=" * 80)
    print("EXIT ANALYSIS - 70/30 NO-TIMESTOP STRATEGY")
    print("=" * 80)
    print()
    
    # Global counters
    tp1_reached = 0  # Trades that reached equilibrium (TP1)
    tp2_full = 0  # Trades that reached TP2 (opposite) after TP1
    breakeven_after_tp1 = 0  # Trades that hit breakeven after TP1
    sl_before_tp1 = 0  # Trades that hit SL without reaching TP1
    total_trades = 0
    
    # Process each year
    for csv_file in csv_files:
        year = csv_file.split()[0]  # Extract year from filename
        
        bt = JudasSwingFVG70_30NoTimestopBacktest(csv_file)
        if not bt.load_data():
            continue
        
        results = bt.run_backtest()
        
        if results['total_trades'] == 0:
            continue
        
        # Analyze each trade
        for trade in results['trades']:
            total_trades += 1
            exit_type = trade.get('exit_type', '')
            tp1_hit = trade.get('tp1_hit', False)
            
            if tp1_hit:
                tp1_reached += 1
                
                if exit_type == 'TP2':
                    tp2_full += 1
                elif 'Breakeven' in exit_type or exit_type == 'SL (Breakeven)':
                    breakeven_after_tp1 += 1
            else:
                # Trade exited via SL without reaching TP1
                if exit_type == 'SL':
                    sl_before_tp1 += 1
    
    # Print results
    print(f"\n📊 GLOBAL STATISTICS (2018-2025)")
    print("=" * 80)
    print(f"Total trades analyzed: {total_trades}")
    print()
    
    print("🎯 TP1 (EQUILIBRIUM) REACHED:")
    print(f"  {tp1_reached:,} trades ({tp1_reached/total_trades*100:.2f}% of all trades)")
    print()
    
    if tp1_reached > 0:
        print("  After reaching TP1:")
        print(f"    → TP2 (Opposite): {tp2_full:,} trades")
        print(f"       • {tp2_full/tp1_reached*100:.2f}% of TP1 trades")
        print(f"       • {tp2_full/total_trades*100:.2f}% of all trades")
        print()
        print(f"    → Breakeven: {breakeven_after_tp1:,} trades")
        print(f"       • {breakeven_after_tp1/tp1_reached*100:.2f}% of TP1 trades")
        print(f"       • {breakeven_after_tp1/total_trades*100:.2f}% of all trades")
        print()
    
    print("❌ SL HIT (without reaching TP1):")
    print(f"  {sl_before_tp1:,} trades ({sl_before_tp1/total_trades*100:.2f}% of all trades)")
    print()
    
    # Summary
    print("=" * 80)
    print("📈 SUMMARY:")
    print("=" * 80)
    print(f"• {tp1_reached:,} trades secured 70% profit at equilibrium")
    print(f"• {tp2_full:,} trades achieved full profit (70% + 30%)")
    print(f"• {breakeven_after_tp1:,} trades protected capital after TP1 (70% profit + 30% breakeven)")
    print(f"• {sl_before_tp1:,} trades hit SL before TP1")
    print()
    
    # Key insight
    if tp1_reached > 0:
        tp2_conversion = tp2_full / tp1_reached * 100
        breakeven_rate = breakeven_after_tp1 / tp1_reached * 100
        
        print("🔑 KEY INSIGHT:")
        print(f"Among trades reaching TP1:")
        print(f"  • {tp2_conversion:.1f}% convert to full TP2")
        print(f"  • {breakeven_rate:.1f}% return to breakeven (capital protected)")
        print()


if __name__ == "__main__":
    analyze_all_years()

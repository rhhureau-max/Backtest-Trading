#!/usr/bin/env python3
"""
Analyse détaillée des trades pour la stratégie 70/30:
- Trades atteignant TP1 puis TP2
- Trades atteignant TP1 puis retournant au breakeven
"""

import pandas as pd
import glob
from datetime import datetime, time, timedelta

def is_asia_session(dt, date):
    """Vérifie si l'heure est dans la session Asia (18:00-23:00 J-1)"""
    asia_start = time(18, 0)
    asia_end = time(23, 0)
    
    if dt.time() >= asia_start and dt.time() <= asia_end:
        return dt.date() == (date - timedelta(days=1))
    return False

def is_london_killzone(dt, date):
    """Vérifie si l'heure est dans London Killzone (01:00-04:00 J)"""
    lk_start = time(1, 0)
    lk_end = time(4, 0)
    return dt.date() == date and lk_start <= dt.time() <= lk_end

def detect_fvg_bearish(high_prev, low_prev, high_curr, low_curr, high_next, low_next):
    """Détecte un FVG baissier"""
    if low_prev > high_next:
        return True, high_next, low_prev
    return False, None, None

def detect_fvg_bullish(high_prev, low_prev, high_curr, low_curr, high_next, low_next):
    """Détecte un FVG haussier"""
    if high_prev < low_next:
        return True, high_prev, low_next
    return False, None, None

def run_backtest_with_tracking(csv_file):
    """Backteste avec tracking détaillé des TP1/TP2/Breakeven"""
    try:
        df = pd.read_csv(csv_file, sep=';', encoding='utf-8')
    except:
        try:
            df = pd.read_csv(csv_file, sep=';', encoding='latin-1')
        except Exception as e:
            print(f"Erreur lecture {csv_file}: {e}")
            return None
    
    # Renommer les colonnes si nécessaire
    if 'Column1' in df.columns:
        df.columns = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
    
    df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%d/%m/%Y %H:%M:%S')
    df = df.sort_values('DateTime').reset_index(drop=True)
    
    trades_with_tp1 = 0
    trades_with_tp1_and_tp2 = 0
    trades_with_tp1_then_breakeven = 0
    total_trades = 0
    
    current_date = None
    trade_taken = False
    
    for i in range(len(df)):
        row = df.iloc[i]
        dt = row['DateTime']
        
        if dt.date() != current_date:
            current_date = dt.date()
            trade_taken = False
            
            # Calculer Asia High/Low
            asia_data = df[(df['DateTime'].apply(lambda x: is_asia_session(x, current_date)))]
            
            if len(asia_data) == 0:
                continue
                
            asia_high = asia_data['High'].max()
            asia_low = asia_data['Low'].min()
            equilibrium = (asia_high + asia_low) / 2.0
        
        if trade_taken or not is_london_killzone(dt, current_date):
            continue
        
        if i < 2 or i >= len(df) - 1:
            continue
        
        prev2 = df.iloc[i-2]
        prev1 = df.iloc[i-1]
        curr = row
        
        # Détecter setup LONG
        if prev1['Low'] < asia_low:
            has_fvg, fvg_low, fvg_high = detect_fvg_bearish(
                prev2['High'], prev2['Low'],
                prev1['High'], prev1['Low'],
                curr['High'], curr['Low']
            )
            
            if has_fvg and curr['Close'] > fvg_high:
                # Trade LONG détecté
                entry_price = curr['Close']
                sl_price = asia_low - 0.5
                tp1_price = equilibrium
                tp2_price = asia_high
                
                total_trades += 1
                trade_taken = True
                
                # Simuler la suite du trade
                tp1_hit = False
                tp2_hit = False
                sl_hit = False
                breakeven_hit = False
                
                for j in range(i+1, len(df)):
                    future_row = df.iloc[j]
                    future_dt = future_row['DateTime']
                    
                    # Time stop à 12:00
                    if future_dt.date() > current_date or future_dt.time() >= time(12, 0):
                        break
                    
                    # Vérifier SL initial
                    if not tp1_hit and future_row['Low'] <= sl_price:
                        sl_hit = True
                        break
                    
                    # Vérifier TP1
                    if not tp1_hit and future_row['High'] >= tp1_price:
                        tp1_hit = True
                        trades_with_tp1 += 1
                        # Après TP1, le SL devient breakeven
                        continue
                    
                    # Après TP1, vérifier breakeven ou TP2
                    if tp1_hit:
                        # Vérifier TP2
                        if future_row['High'] >= tp2_price:
                            tp2_hit = True
                            trades_with_tp1_and_tp2 += 1
                            break
                        
                        # Vérifier breakeven
                        if future_row['Low'] <= entry_price:
                            breakeven_hit = True
                            trades_with_tp1_then_breakeven += 1
                            break
        
        # Détecter setup SHORT
        elif prev1['High'] > asia_high:
            has_fvg, fvg_low, fvg_high = detect_fvg_bullish(
                prev2['High'], prev2['Low'],
                prev1['High'], prev1['Low'],
                curr['High'], curr['Low']
            )
            
            if has_fvg and curr['Close'] < fvg_low:
                # Trade SHORT détecté
                entry_price = curr['Close']
                sl_price = asia_high + 0.5
                tp1_price = equilibrium
                tp2_price = asia_low
                
                total_trades += 1
                trade_taken = True
                
                # Simuler la suite du trade
                tp1_hit = False
                tp2_hit = False
                sl_hit = False
                breakeven_hit = False
                
                for j in range(i+1, len(df)):
                    future_row = df.iloc[j]
                    future_dt = future_row['DateTime']
                    
                    # Time stop à 12:00
                    if future_dt.date() > current_date or future_dt.time() >= time(12, 0):
                        break
                    
                    # Vérifier SL initial
                    if not tp1_hit and future_row['High'] >= sl_price:
                        sl_hit = True
                        break
                    
                    # Vérifier TP1
                    if not tp1_hit and future_row['Low'] <= tp1_price:
                        tp1_hit = True
                        trades_with_tp1 += 1
                        # Après TP1, le SL devient breakeven
                        continue
                    
                    # Après TP1, vérifier breakeven ou TP2
                    if tp1_hit:
                        # Vérifier TP2
                        if future_row['Low'] <= tp2_price:
                            tp2_hit = True
                            trades_with_tp1_and_tp2 += 1
                            break
                        
                        # Vérifier breakeven
                        if future_row['High'] >= entry_price:
                            breakeven_hit = True
                            trades_with_tp1_then_breakeven += 1
                            break
    
    return {
        'total_trades': total_trades,
        'trades_with_tp1': trades_with_tp1,
        'trades_with_tp1_and_tp2': trades_with_tp1_and_tp2,
        'trades_with_tp1_then_breakeven': trades_with_tp1_then_breakeven
    }

def main():
    print("\n" + "="*80)
    print("ANALYSE DÉTAILLÉE - STRATÉGIE 70/30 (TP1 → TP2 vs TP1 → Breakeven)")
    print("="*80 + "\n")
    
    csv_files = sorted(glob.glob('*5m.csv'))
    csv_files = [f for f in csv_files if f.startswith(('2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025'))]
    
    total_trades = 0
    total_tp1 = 0
    total_tp2 = 0
    total_breakeven = 0
    
    print("Analyse par année:\n")
    
    for csv_file in csv_files:
        year = csv_file[:4]
        print(f"Traitement {year}...", end=' ')
        
        result = run_backtest_with_tracking(csv_file)
        
        if result:
            total_trades += result['total_trades']
            total_tp1 += result['trades_with_tp1']
            total_tp2 += result['trades_with_tp1_and_tp2']
            total_breakeven += result['trades_with_tp1_then_breakeven']
            print(f"✓ {result['total_trades']} trades")
        else:
            print("✗ Erreur")
    
    print("\n" + "="*80)
    print("RÉSULTATS GLOBAUX (2018-2025)")
    print("="*80 + "\n")
    
    print(f"📊 Total de trades: {total_trades}")
    print(f"\n📈 Trades atteignant TP1 (Equilibrium): {total_tp1} ({total_tp1/total_trades*100:.2f}%)")
    
    print(f"\n✅ Parmi ceux atteignant TP1:")
    print(f"   • TP1 → TP2 (Opposé): {total_tp2} ({total_tp2/total_tp1*100:.2f}% des TP1 | {total_tp2/total_trades*100:.2f}% du total)")
    print(f"   • TP1 → Breakeven: {total_breakeven} ({total_breakeven/total_tp1*100:.2f}% des TP1 | {total_breakeven/total_trades*100:.2f}% du total)")
    
    print(f"\n📊 Trades sans TP1: {total_trades - total_tp1} ({(total_trades-total_tp1)/total_trades*100:.2f}%)")
    print(f"   (SL touché avant d'atteindre l'équilibre)")
    
    print("\n" + "="*80)
    print("INTERPRÉTATION")
    print("="*80 + "\n")
    
    print("🔹 Protection Breakeven Efficace:")
    print(f"   {total_breakeven/total_trades*100:.2f}% des trades bénéficient de la protection breakeven")
    print(f"   après avoir sécurisé 70% du profit à l'équilibre\n")
    
    print("🔹 Profit Maximum:")
    print(f"   {total_tp2/total_trades*100:.2f}% des trades atteignent le TP2 complet")
    print(f"   (70% à l'équilibre + 30% à l'opposé)\n")
    
    print("🔹 Gestion du Risque:")
    print(f"   Capital protégé après TP1 sur {total_tp1} trades")
    print(f"   Risque zéro sur les 30% restants une fois TP1 atteint\n")
    
    print("="*80 + "\n")

if __name__ == "__main__":
    main()

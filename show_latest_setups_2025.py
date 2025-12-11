#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour afficher les derniers setups FVG Inversion de 2025
"""

import sys
sys.path.insert(0, '/home/runner/work/Backtest-Trading/Backtest-Trading')

from fvg_inversion_strategy import FVGInversionStrategy

def show_latest_2025_setups():
    """Affiche les derniers setups détectés en 2025"""
    
    print("=" * 80)
    print("DERNIERS SETUPS FVG INVERSION - ANNÉE 2025")
    print("=" * 80)
    
    # Analyser NQ et ES pour 2025
    for instrument in ['NQ', 'ES']:
        print(f"\n{'='*80}")
        print(f"INSTRUMENT: {instrument}")
        print(f"{'='*80}\n")
        
        try:
            strategy = FVGInversionStrategy()
            
            # Charger les données 2025
            df = strategy.load_data(instrument, '5m', year_range=(2025, 2026))
            
            if df.empty:
                print(f"⚠️  Aucune donnée disponible pour {instrument} en 2025")
                continue
            
            print(f"Période: {df.iloc[0]['DateTime']} à {df.iloc[-1]['DateTime']}")
            
            # Calculer les indicateurs
            df = strategy._calculate_indicators(df)
            
            print(f"Recherche des setups FVG Inversion...")
            
            # Chercher tous les setups
            setups_found = []
            i = strategy.recent_swing_lookback + 10
            
            while i < len(df) - strategy.max_trigger_candles - 10:
                setup = strategy._find_setup(df, i)
                
                if setup:
                    # Ajouter les informations supplémentaires
                    trigger_idx = setup['entry_idx']
                    trigger_candle = df.iloc[trigger_idx]
                    pattern_candle = df.iloc[setup['pattern_idx']]
                    
                    setup_info = {
                        'entry_datetime': str(setup['entry_datetime']),
                        'pattern_datetime': str(pattern_candle['DateTime']),
                        'pattern_type': setup['pattern_type'],
                        'direction': setup['direction'],
                        'entry_price': setup['entry_price'],
                        'pattern_high': pattern_candle['High'],
                        'pattern_low': pattern_candle['Low'],
                        'pattern_close': pattern_candle['Close'],
                        'fvg_high': setup['fvg_inversion']['fvg']['high'],
                        'fvg_low': setup['fvg_inversion']['fvg']['low'],
                        'fvg_created_datetime': str(setup['fvg_inversion']['fvg']['created_at_datetime']),
                        'swept_level': setup['sweep_info']['swept_level'],
                        'candles_after_pattern': trigger_idx - setup['pattern_idx']
                    }
                    setups_found.append(setup_info)
                    
                    # Avancer après le trade
                    i = trigger_idx + 20
                else:
                    i += 1
            
            # Afficher les setups
            if setups_found:
                print(f"\n✅ {len(setups_found)} setup(s) détecté(s) en 2025\n")
                
                for i, setup in enumerate(setups_found, 1):
                    print(f"\n{'─'*80}")
                    print(f"SETUP #{i}")
                    print(f"{'─'*80}")
                    print(f"📅 Date d'Entrée:        {setup['entry_datetime']}")
                    print(f"📅 Date du Pattern:      {setup['pattern_datetime']}")
                    print(f"📊 Type de Pattern:      {setup['pattern_type'].upper()}")
                    print(f"📈 Direction:            {setup['direction'].upper()}")
                    
                    print(f"\n💰 PRIX:")
                    print(f"   Entry Price:          {setup['entry_price']:.2f}")
                    print(f"   Pattern High:         {setup['pattern_high']:.2f}")
                    print(f"   Pattern Low:          {setup['pattern_low']:.2f}")
                    print(f"   Pattern Close:        {setup['pattern_close']:.2f}")
                    
                    print(f"\n📦 FAIR VALUE GAP (FVG):")
                    print(f"   FVG High:             {setup['fvg_high']:.2f}")
                    print(f"   FVG Low:              {setup['fvg_low']:.2f}")
                    print(f"   FVG Créé le:          {setup['fvg_created_datetime']}")
                    
                    print(f"\n💧 LIQUIDITY SWEEP:")
                    print(f"   Niveau Sweepé:        {setup['swept_level']:.2f}")
                    
                    print(f"\n⏱️  TIMING:")
                    print(f"   Bougies après pattern: {setup['candles_after_pattern']}")
                    
                    # Calculer les SL et TP possibles
                    if setup['direction'] == 'long':
                        sl1 = setup['pattern_low'] - 1
                        sl2 = setup['fvg_low'] - 1
                        risk1 = setup['entry_price'] - sl1
                        risk2 = setup['entry_price'] - sl2
                        
                        print(f"\n🛡️  STOP LOSS OPTIONS (LONG):")
                        print(f"   SL Type 1 (Pattern):  {sl1:.2f} (Risk: {risk1:.2f} pts)")
                        print(f"   SL Type 2 (FVG):      {sl2:.2f} (Risk: {risk2:.2f} pts)")
                        
                        print(f"\n🎯 TAKE PROFIT TARGETS (RR basé sur SL Type 2):")
                        print(f"   TP 1:1   = {setup['entry_price'] + risk2:.2f}")
                        print(f"   TP 1.5:1 = {setup['entry_price'] + risk2*1.5:.2f}")
                        print(f"   TP 2:1   = {setup['entry_price'] + risk2*2:.2f}")
                        print(f"   TP 2.5:1 = {setup['entry_price'] + risk2*2.5:.2f}")
                    else:
                        sl1 = setup['pattern_high'] + 1
                        sl2 = setup['fvg_high'] + 1
                        risk1 = sl1 - setup['entry_price']
                        risk2 = sl2 - setup['entry_price']
                        
                        print(f"\n🛡️  STOP LOSS OPTIONS (SHORT):")
                        print(f"   SL Type 1 (Pattern):  {sl1:.2f} (Risk: {risk1:.2f} pts)")
                        print(f"   SL Type 2 (FVG):      {sl2:.2f} (Risk: {sl2:.2f} pts)")
                        
                        print(f"\n🎯 TAKE PROFIT TARGETS (RR basé sur SL Type 2):")
                        print(f"   TP 1:1   = {setup['entry_price'] - risk2:.2f}")
                        print(f"   TP 1.5:1 = {setup['entry_price'] - risk2*1.5:.2f}")
                        print(f"   TP 2:1   = {setup['entry_price'] - risk2*2:.2f}")
                        print(f"   TP 2.5:1 = {setup['entry_price'] - risk2*2.5:.2f}")
                
            else:
                print(f"\n❌ Aucun setup complet détecté en 2025 pour {instrument}")
                print(f"   (Les setups nécessitent: Tendance + FVG + Sweep + Pattern + Inversion FVG)")
        
        except Exception as e:
            print(f"❌ Erreur lors de l'analyse de {instrument}: {e}")
            import traceback
            traceback.print_exc()
    
    print(f"\n{'='*80}")
    print("FIN DE L'ANALYSE")
    print(f"{'='*80}\n")

if __name__ == "__main__":
    show_latest_2025_setups()

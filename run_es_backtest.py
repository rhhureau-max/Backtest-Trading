#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour exécuter uniquement le backtest ES
"""

from fvg_inversion_strategy import FVGInversionStrategy

if __name__ == '__main__':
    print("\n" + "="*80)
    print("BACKTEST ES UNIQUEMENT")
    print("="*80 + "\n")
    
    strategy = FVGInversionStrategy(base_path='.')
    
    results_es = strategy.run_backtest(
        instrument='ES',
        timeframe='5m',
        year_range=(2024, 2026)
    )
    
    strategy.save_results('fvg_inversion_results_ES.json')
    
    print("\n" + "="*80)
    print("BACKTEST ES TERMINÉ")
    print("="*80 + "\n")

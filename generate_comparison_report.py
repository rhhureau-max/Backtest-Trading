#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour générer le rapport comparatif à partir des résultats existants
"""

import json
import os
from datetime import datetime
from fvg_inversion_strategy import FVGInversionStrategy

if __name__ == '__main__':
    print("\n" + "="*80)
    print("GÉNÉRATION DU RAPPORT COMPARATIF NQ vs ES")
    print("="*80 + "\n")
    
    # Charger les résultats
    with open('fvg_inversion_results_NQ.json', 'r', encoding='utf-8') as f:
        results_nq = json.load(f)
    
    with open('fvg_inversion_results_ES.json', 'r', encoding='utf-8') as f:
        results_es = json.load(f)
    
    print("✓ Résultats NQ chargés")
    print("✓ Résultats ES chargés")
    
    # Créer l'instance de stratégie
    strategy = FVGInversionStrategy(base_path='.')
    
    # Générer le rapport comparatif
    strategy.generate_comparative_report(results_nq, results_es)
    
    # Sauvegarder la comparaison JSON
    comparison_json = {
        'NQ': results_nq,
        'ES': results_es,
        'comparison_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    filepath = 'fvg_inversion_results_comparison.json'
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(comparison_json, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Comparaison sauvegardée: {filepath}")
    
    print("\n" + "="*80)
    print("RAPPORT COMPARATIF GÉNÉRÉ")
    print("="*80 + "\n")
    print(f"✓ Rapport markdown: FVG_INVERSION_STRATEGY_ANALYSIS.md")
    print(f"✓ Comparaison JSON: {filepath}")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test automatisé pour le système de backtesting FVG
Lance tous les tests et valide le bon fonctionnement du système
"""

import os
import sys
import subprocess
from datetime import datetime

def print_header(title):
    """Affiche un en-tête formaté"""
    print("\n" + "="*70)
    print(title)
    print("="*70 + "\n")

def test_dependencies():
    """Teste que les dépendances sont installées"""
    print("📦 Test des dépendances...")
    try:
        import pandas
        import numpy
        print("  ✓ pandas installé (version {})".format(pandas.__version__))
        print("  ✓ numpy installé (version {})".format(numpy.__version__))
        return True
    except ImportError as e:
        print(f"  ✗ Erreur: {e}")
        print("  → Exécutez: pip install -r requirements.txt")
        return False

def test_data_files():
    """Vérifie que les fichiers de données source existent"""
    print("\n📂 Test des fichiers de données source...")
    years = [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]
    missing_files = []
    
    for year in years:
        filename = f"{year} 5m.csv"
        if os.path.exists(filename):
            size = os.path.getsize(filename) / (1024*1024)
            print(f"  ✓ {filename} ({size:.2f} MB)")
        else:
            print(f"  ✗ {filename} - MANQUANT")
            missing_files.append(filename)
    
    if missing_files:
        print(f"\n  ⚠️  {len(missing_files)} fichier(s) manquant(s)")
        return False
    return True

def test_consolidation():
    """Teste le script de consolidation"""
    print("\n🔧 Test du script de consolidation...")
    
    if not os.path.exists('combine_data.py'):
        print("  ✗ combine_data.py non trouvé")
        return False
    
    print("  ⏳ Exécution de combine_data.py...")
    try:
        result = subprocess.run(
            ['python3', 'combine_data.py'],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            print("  ✓ Script exécuté avec succès")
            
            # Vérifier que le fichier consolidé existe
            if os.path.exists('NQ_5min.csv'):
                size = os.path.getsize('NQ_5min.csv') / (1024*1024)
                print(f"  ✓ NQ_5min.csv créé ({size:.2f} MB)")
                return True
            else:
                print("  ✗ NQ_5min.csv non créé")
                return False
        else:
            print(f"  ✗ Erreur lors de l'exécution")
            print(f"  Sortie: {result.stderr[:200]}")
            return False
            
    except subprocess.TimeoutExpired:
        print("  ✗ Timeout (>60s)")
        return False
    except Exception as e:
        print(f"  ✗ Erreur: {e}")
        return False

def test_backtest():
    """Teste le script de backtesting"""
    print("\n📈 Test du script de backtesting...")
    
    if not os.path.exists('backtest_fvg_strategy.py'):
        print("  ✗ backtest_fvg_strategy.py non trouvé")
        return False
    
    if not os.path.exists('NQ_5min.csv'):
        print("  ✗ NQ_5min.csv non trouvé")
        print("  → Exécutez d'abord combine_data.py")
        return False
    
    print("  ⏳ Exécution de backtest_fvg_strategy.py (peut prendre ~1 minute)...")
    try:
        result = subprocess.run(
            ['python3', 'backtest_fvg_strategy.py'],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        if result.returncode == 0:
            print("  ✓ Script exécuté avec succès")
            
            # Vérifier les fichiers de sortie
            success = True
            
            if os.path.exists('backtest_results.csv'):
                size = os.path.getsize('backtest_results.csv') / (1024*1024)
                print(f"  ✓ backtest_results.csv créé ({size:.2f} MB)")
            else:
                print("  ✗ backtest_results.csv non créé")
                success = False
            
            if os.path.exists('performance_report.txt'):
                print(f"  ✓ performance_report.txt créé")
            else:
                print("  ✗ performance_report.txt non créé")
                success = False
            
            return success
        else:
            print(f"  ✗ Erreur lors de l'exécution")
            print(f"  Sortie: {result.stderr[:200]}")
            return False
            
    except subprocess.TimeoutExpired:
        print("  ✗ Timeout (>120s)")
        return False
    except Exception as e:
        print(f"  ✗ Erreur: {e}")
        return False

def test_results_validity():
    """Valide le contenu des résultats"""
    print("\n✅ Test de validité des résultats...")
    
    try:
        import pandas as pd
        
        # Test du fichier consolidé
        if os.path.exists('NQ_5min.csv'):
            df = pd.read_csv('NQ_5min.csv')
            print(f"  ✓ NQ_5min.csv - {len(df)} lignes")
            
            # Vérifier les colonnes
            expected_cols = ['Date', 'Time', 'Open', 'High', 'Low', 'Close']
            if all(col in df.columns for col in expected_cols):
                print(f"  ✓ Colonnes valides: {expected_cols}")
            else:
                print(f"  ✗ Colonnes manquantes")
                return False
        
        # Test des résultats de backtest
        if os.path.exists('backtest_results.csv'):
            results = pd.read_csv('backtest_results.csv')
            print(f"  ✓ backtest_results.csv - {len(results)} trades")
            
            # Vérifier les types de résultats
            if 'result_1.0R' in results.columns:
                result_types = results['result_1.0R'].unique()
                print(f"  ✓ Types de résultats: {list(result_types)}")
            
            # Vérifier les types de trades
            if 'type' in results.columns:
                trade_types = results['type'].unique()
                print(f"  ✓ Types de trades: {list(trade_types)}")
        
        return True
        
    except Exception as e:
        print(f"  ✗ Erreur: {e}")
        return False

def main():
    """Fonction principale"""
    start_time = datetime.now()
    
    print_header("🧪 SUITE DE TESTS - SYSTÈME DE BACKTESTING FVG")
    
    # Exécuter les tests
    tests = [
        ("Dépendances Python", test_dependencies),
        ("Fichiers de données", test_data_files),
        ("Consolidation", test_consolidation),
        ("Backtesting", test_backtest),
        ("Validité des résultats", test_results_validity)
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"\n❌ Erreur inattendue dans '{test_name}': {e}")
            results[test_name] = False
    
    # Résumé
    print_header("📊 RÉSUMÉ DES TESTS")
    
    passed = sum(1 for r in results.values() if r)
    total = len(results)
    
    for test_name, success in results.items():
        status = "✅ RÉUSSI" if success else "❌ ÉCHOUÉ"
        print(f"  {status} - {test_name}")
    
    print(f"\n  Total: {passed}/{total} tests réussis")
    
    # Temps d'exécution
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    print(f"\n⏱️  Temps d'exécution: {duration:.2f} secondes")
    
    # Code de sortie
    if passed == total:
        print("\n🎉 Tous les tests sont passés avec succès!")
        return 0
    else:
        print("\n⚠️  Certains tests ont échoué. Vérifiez les erreurs ci-dessus.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

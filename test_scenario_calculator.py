"""
Tests unitaires pour le calculateur de probabilités de scénarios de trading.
"""

import sys
import os

# Ajouter le répertoire parent au path pour l'import
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from scenario_probability_calculator import (
    ScenarioProbabilityCalculator,
    AsianRangeState,
    HTFTrendBias,
    LondonInitialAction,
    ScenarioType
)


def test_classify_asian_range():
    """Test de la classification du range asiatique."""
    calculator = ScenarioProbabilityCalculator()
    
    # Test range compressé
    assert calculator.classify_asian_range(15.0) == AsianRangeState.COMPRESSED
    assert calculator.classify_asian_range(29.9) == AsianRangeState.COMPRESSED
    
    # Test range standard
    assert calculator.classify_asian_range(30.0) == AsianRangeState.STANDARD
    assert calculator.classify_asian_range(40.0) == AsianRangeState.STANDARD
    assert calculator.classify_asian_range(50.0) == AsianRangeState.STANDARD
    
    # Test range étendu
    assert calculator.classify_asian_range(50.1) == AsianRangeState.EXTENDED
    assert calculator.classify_asian_range(100.0) == AsianRangeState.EXTENDED
    
    print("✓ Test classify_asian_range: PASSED")


def test_configuration_a_bullish():
    """Test Configuration A: Range Standard + Cassure Contre-Tendance (Haussier)."""
    calculator = ScenarioProbabilityCalculator()
    
    # Range standard (40 pips) + Tendance haussière + Cassure du bas
    scenario, prob_range, justification, analysis = calculator.analyze_scenario(
        AsianRangeState.STANDARD,
        HTFTrendBias.BULLISH,
        LondonInitialAction.BREAKOUT_LOW
    )
    
    assert scenario == ScenarioType.REVERSAL
    assert prob_range == (65.0, 75.0)
    assert "chasse aux stops" in justification.lower()
    assert "discount" in analysis.lower() and "basse" in analysis.lower()
    
    print("✓ Test configuration_a_bullish: PASSED")


def test_configuration_a_bearish():
    """Test Configuration A: Range Standard + Cassure Contre-Tendance (Baissier)."""
    calculator = ScenarioProbabilityCalculator()
    
    # Range standard + Tendance baissière + Cassure du haut
    scenario, prob_range, justification, analysis = calculator.analyze_scenario(
        AsianRangeState.STANDARD,
        HTFTrendBias.BEARISH,
        LondonInitialAction.BREAKOUT_HIGH
    )
    
    assert scenario == ScenarioType.REVERSAL
    assert prob_range == (65.0, 75.0)
    assert "chasse aux stops" in justification.lower()
    assert "premium" in analysis.lower() and "haute" in analysis.lower()
    
    print("✓ Test configuration_a_bearish: PASSED")


def test_configuration_b_bullish():
    """Test Configuration B: Range Compressé + Cassure Alignée (Haussier)."""
    calculator = ScenarioProbabilityCalculator()
    
    # Range compressé (20 pips) + Tendance haussière + Cassure du haut
    scenario, prob_range, justification, analysis = calculator.analyze_scenario(
        AsianRangeState.COMPRESSED,
        HTFTrendBias.BULLISH,
        LondonInitialAction.BREAKOUT_HIGH
    )
    
    assert scenario == ScenarioType.CONTINUATION
    assert prob_range == (50.0, 60.0)
    assert "expansion" in justification.lower()
    assert "trend day" in analysis.lower()
    
    print("✓ Test configuration_b_bullish: PASSED")


def test_configuration_b_bearish():
    """Test Configuration B: Range Compressé + Cassure Alignée (Baissier)."""
    calculator = ScenarioProbabilityCalculator()
    
    # Range compressé + Tendance baissière + Cassure du bas
    scenario, prob_range, justification, analysis = calculator.analyze_scenario(
        AsianRangeState.COMPRESSED,
        HTFTrendBias.BEARISH,
        LondonInitialAction.BREAKOUT_LOW
    )
    
    assert scenario == ScenarioType.CONTINUATION
    assert prob_range == (50.0, 60.0)
    assert "expansion" in justification.lower()
    
    print("✓ Test configuration_b_bearish: PASSED")


def test_configuration_c():
    """Test Configuration C: Range Étendu."""
    calculator = ScenarioProbabilityCalculator()
    
    # Range étendu (60 pips)
    scenario, prob_range, justification, analysis = calculator.analyze_scenario(
        AsianRangeState.EXTENDED,
        HTFTrendBias.NEUTRAL,
        LondonInitialAction.INTERNAL
    )
    
    assert scenario == ScenarioType.CONSOLIDATION
    assert prob_range == (40.0, 50.0)
    assert "atr" in justification.lower()
    assert "intérieur" in analysis.lower() or "faux breakout" in analysis.lower()
    
    print("✓ Test configuration_c: PASSED")


def test_non_matching_configuration():
    """Test d'une configuration qui ne correspond à aucune configuration standard."""
    calculator = ScenarioProbabilityCalculator()
    
    # Range standard + Tendance neutre + Action interne
    scenario, prob_range, justification, analysis = calculator.analyze_scenario(
        AsianRangeState.STANDARD,
        HTFTrendBias.NEUTRAL,
        LondonInitialAction.INTERNAL
    )
    
    # Devrait retourner un scénario par défaut
    assert scenario == ScenarioType.CONSOLIDATION
    assert prob_range == (40.0, 50.0)
    
    print("✓ Test non_matching_configuration: PASSED")


def test_format_analysis_output():
    """Test du formatage de la sortie d'analyse."""
    calculator = ScenarioProbabilityCalculator()
    
    output = calculator.format_analysis_output(
        asian_range_pips=40.0,
        htf_trend=HTFTrendBias.BULLISH,
        london_action=LondonInitialAction.BREAKOUT_LOW,
        scenario=ScenarioType.REVERSAL,
        probability_range=(65.0, 75.0),
        justification="Test justification",
        session_analysis="Test analysis"
    )
    
    assert "PHASE 1" in output
    assert "PHASE 2" in output
    assert "40.0 pips" in output
    assert "Haussier" in output
    assert "Cassure Bas" in output
    assert "RETOURNEMENT" in output
    assert "65%" in output
    assert "75%" in output
    
    print("✓ Test format_analysis_output: PASSED")


def run_all_tests():
    """Exécute tous les tests."""
    print("=" * 75)
    print("EXÉCUTION DES TESTS UNITAIRES")
    print("=" * 75)
    print()
    
    try:
        test_classify_asian_range()
        test_configuration_a_bullish()
        test_configuration_a_bearish()
        test_configuration_b_bullish()
        test_configuration_b_bearish()
        test_configuration_c()
        test_non_matching_configuration()
        test_format_analysis_output()
        
        print()
        print("=" * 75)
        print("✓ TOUS LES TESTS ONT RÉUSSI!")
        print("=" * 75)
        return True
        
    except AssertionError as e:
        print()
        print("=" * 75)
        print("✗ ÉCHEC DES TESTS!")
        print(f"Erreur: {e}")
        print("=" * 75)
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

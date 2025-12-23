"""
Trading Scenario Probability Calculator

This module implements a probability analysis system for trading scenarios
based on Asian range characteristics, HTF (Higher Time Frame) trend bias,
and London session initial action.

The algorithm answers the question: "What is the probability percentage
that scenario X will occur today, given conditions Y?"
"""

from enum import Enum
from typing import Dict, Tuple


class AsianRangeState(Enum):
    """État du Range Asiatique (ERA)"""
    COMPRESSED = "compressed"  # < 30 pips
    STANDARD = "standard"      # 30-50 pips
    EXTENDED = "extended"      # > 50 pips


class HTFTrendBias(Enum):
    """Biais de Tendance HTF (Daily/4H)"""
    BULLISH = "bullish"    # Haussier
    BEARISH = "bearish"    # Baissier
    NEUTRAL = "neutral"    # Neutre


class LondonInitialAction(Enum):
    """Action Initiale de Londres (07:00-09:00 GMT)"""
    BREAKOUT_HIGH = "breakout_high"  # Cassure Haut
    BREAKOUT_LOW = "breakout_low"    # Cassure Bas
    INTERNAL = "internal"            # Interne


class ScenarioType(Enum):
    """Types de scénarios probables"""
    REVERSAL = "reversal"           # Retournement (Scénario I)
    CONTINUATION = "continuation"   # Continuation (Scénario II)
    CONSOLIDATION = "consolidation" # Consolidation/Retracement (Scénario III)


class ScenarioProbabilityCalculator:
    """
    Calculateur de probabilités pour les scénarios de trading.
    
    PHASE 1 : COLLECTE DES VARIABLES D'ENTRÉE (INPUT)
    PHASE 2 : MATRICE DE SCÉNARIOS ET PROBABILITÉS (OUTPUT)
    """
    
    def __init__(self):
        """Initialize the probability calculator with configuration rules."""
        pass
    
    @staticmethod
    def classify_asian_range(range_pips: float) -> AsianRangeState:
        """
        Classifie l'état du range asiatique en fonction de sa taille en pips.
        
        Args:
            range_pips: Taille du range asiatique en pips
            
        Returns:
            AsianRangeState: Classification du range
        """
        if range_pips < 30:
            return AsianRangeState.COMPRESSED
        elif range_pips <= 50:
            return AsianRangeState.STANDARD
        else:
            return AsianRangeState.EXTENDED
    
    def analyze_scenario(
        self,
        asian_range_state: AsianRangeState,
        htf_trend: HTFTrendBias,
        london_action: LondonInitialAction
    ) -> Tuple[ScenarioType, Tuple[float, float], str, str]:
        """
        Analyse le scénario et retourne la probabilité associée.
        
        Args:
            asian_range_state: État du range asiatique
            htf_trend: Biais de tendance HTF
            london_action: Action initiale de Londres
            
        Returns:
            Tuple contenant:
            - ScenarioType: Type de scénario probable
            - Tuple[float, float]: Fourchette de probabilité (min, max) en %
            - str: Justification basée sur les données
            - str: Analyse de session
        """
        
        # Configuration A: Range Asiatique Standard + Cassure Contre-Tendance
        if self._is_configuration_a(asian_range_state, htf_trend, london_action):
            return self._configuration_a_analysis(htf_trend, london_action)
        
        # Configuration B: Range Asiatique Compressé + Cassure Tendance Alignée
        elif self._is_configuration_b(asian_range_state, htf_trend, london_action):
            return self._configuration_b_analysis(htf_trend)
        
        # Configuration C: Range Asiatique Étendu ou Contexte News
        elif self._is_configuration_c(asian_range_state):
            return self._configuration_c_analysis()
        
        # Cas par défaut (scénario neutre)
        else:
            return (
                ScenarioType.CONSOLIDATION,
                (40.0, 50.0),
                "Configuration non standard - probabilités neutres",
                "Surveiller l'évolution du marché"
            )
    
    def _is_configuration_a(
        self,
        asian_range: AsianRangeState,
        htf_trend: HTFTrendBias,
        london_action: LondonInitialAction
    ) -> bool:
        """
        Configuration A: Range Asiatique Standard + Cassure Contre-Tendance
        Exemple: Tendance Daily Haussière + Cassure du Bas Asiatique à 08:30 GMT
        """
        if asian_range != AsianRangeState.STANDARD:
            return False
        
        # Vérifier la cassure contre-tendance
        is_counter_trend = (
            (htf_trend == HTFTrendBias.BULLISH and london_action == LondonInitialAction.BREAKOUT_LOW) or
            (htf_trend == HTFTrendBias.BEARISH and london_action == LondonInitialAction.BREAKOUT_HIGH)
        )
        
        return is_counter_trend
    
    def _configuration_a_analysis(
        self,
        htf_trend: HTFTrendBias,
        london_action: LondonInitialAction
    ) -> Tuple[ScenarioType, Tuple[float, float], str, str]:
        """Analyse pour Configuration A: RETOURNEMENT (SCÉNARIO I)"""
        
        direction = "hausse" if htf_trend == HTFTrendBias.BULLISH else "baisse"
        zone = "Discount (basse)" if htf_trend == HTFTrendBias.BULLISH else "Premium (haute)"
        
        return (
            ScenarioType.REVERSAL,
            (65.0, 75.0),
            (
                "La chasse aux stops est le comportement par défaut "
                "(70% invalidation HOD/LOD). La tendance de fond agit comme "
                "un aimant de rappel."
            ),
            (
                f"Le marché cherche la liquidité {zone} pour alimenter la {direction}."
            )
        )
    
    def _is_configuration_b(
        self,
        asian_range: AsianRangeState,
        htf_trend: HTFTrendBias,
        london_action: LondonInitialAction
    ) -> bool:
        """
        Configuration B: Range Asiatique Compressé + Cassure Tendance Alignée
        Exemple: Tendance Daily Baissière + Range Asie 20 pips + Cassure du Bas Asiatique
        """
        if asian_range != AsianRangeState.COMPRESSED:
            return False
        
        # Vérifier la cassure alignée avec la tendance
        is_aligned = (
            (htf_trend == HTFTrendBias.BULLISH and london_action == LondonInitialAction.BREAKOUT_HIGH) or
            (htf_trend == HTFTrendBias.BEARISH and london_action == LondonInitialAction.BREAKOUT_LOW)
        )
        
        return is_aligned
    
    def _configuration_b_analysis(
        self,
        htf_trend: HTFTrendBias
    ) -> Tuple[ScenarioType, Tuple[float, float], str, str]:
        """Analyse pour Configuration B: CONTINUATION (SCÉNARIO II)"""
        
        return (
            ScenarioType.CONTINUATION,
            (50.0, 60.0),
            (
                "L'expansion de range est nécessaire après une compression. "
                "L'alignement HTF réduit la friction. Le taux d'échec "
                "(faux breakout) diminue sur les ranges très compressés."
            ),
            (
                "\"Trend Day\" classique. Pas de retour à la moyenne immédiat."
            )
        )
    
    def _is_configuration_c(self, asian_range: AsianRangeState) -> bool:
        """
        Configuration C: Range Asiatique Étendu (> 50 pips) ou Contexte News
        """
        return asian_range == AsianRangeState.EXTENDED
    
    def _configuration_c_analysis(
        self
    ) -> Tuple[ScenarioType, Tuple[float, float], str, str]:
        """Analyse pour Configuration C: CONSOLIDATION / RETRACEMENT (SCÉNARIO III)"""
        
        return (
            ScenarioType.CONSOLIDATION,
            (40.0, 50.0),
            (
                "Si l'Asie a déjà consommé l'ATR (Average True Range) moyen, "
                "le potentiel d'expansion de Londres est limité statistiquement."
            ),
            (
                "Londres va probablement rester à l'intérieur ou faire un "
                "faux breakout marginal."
            )
        )
    
    def format_analysis_output(
        self,
        asian_range_pips: float,
        htf_trend: HTFTrendBias,
        london_action: LondonInitialAction,
        scenario: ScenarioType,
        probability_range: Tuple[float, float],
        justification: str,
        session_analysis: str
    ) -> str:
        """
        Formate la sortie de l'analyse en texte lisible.
        
        Args:
            asian_range_pips: Taille du range asiatique en pips
            htf_trend: Biais de tendance HTF
            london_action: Action initiale de Londres
            scenario: Type de scénario probable
            probability_range: Fourchette de probabilité
            justification: Justification basée sur les données
            session_analysis: Analyse de session
            
        Returns:
            str: Rapport formaté de l'analyse
        """
        asian_state = self.classify_asian_range(asian_range_pips)
        
        # Traductions pour l'affichage
        trend_labels = {
            HTFTrendBias.BULLISH: "Haussier",
            HTFTrendBias.BEARISH: "Baissier",
            HTFTrendBias.NEUTRAL: "Neutre"
        }
        
        action_labels = {
            LondonInitialAction.BREAKOUT_HIGH: "Cassure Haut",
            LondonInitialAction.BREAKOUT_LOW: "Cassure Bas",
            LondonInitialAction.INTERNAL: "Interne"
        }
        
        range_labels = {
            AsianRangeState.COMPRESSED: f"Compressé ({asian_range_pips:.1f} pips < 30)",
            AsianRangeState.STANDARD: f"Standard ({asian_range_pips:.1f} pips entre 30-50)",
            AsianRangeState.EXTENDED: f"Étendu ({asian_range_pips:.1f} pips > 50)"
        }
        
        scenario_labels = {
            ScenarioType.REVERSAL: "RETOURNEMENT (SCÉNARIO I)",
            ScenarioType.CONTINUATION: "CONTINUATION (SCÉNARIO II)",
            ScenarioType.CONSOLIDATION: "CONSOLIDATION / RETRACEMENT (SCÉNARIO III)"
        }
        
        output = f"""
╔════════════════════════════════════════════════════════════════════════╗
║        ANALYSE DE PROBABILITÉ - SCÉNARIO DE TRADING                    ║
╚════════════════════════════════════════════════════════════════════════╝

PHASE 1 : VARIABLES D'ENTRÉE (INPUT)
─────────────────────────────────────────────────────────────────────────
  • État du Range Asiatique : {range_labels[asian_state]}
  • Biais de Tendance HTF    : {trend_labels[htf_trend]}
  • Action Initiale Londres  : {action_labels[london_action]}

PHASE 2 : MATRICE DE SCÉNARIOS ET PROBABILITÉS (OUTPUT)
─────────────────────────────────────────────────────────────────────────
  ► Scénario Probable         : {scenario_labels[scenario]}
  
  ► Pourcentage Estimé        : {probability_range[0]:.0f}% - {probability_range[1]:.0f}%
  
  ► Justification Données     :
    {justification}
  
  ► Analyse de Session        :
    {session_analysis}

═════════════════════════════════════════════════════════════════════════
"""
        return output


def main():
    """
    Exemple d'utilisation du calculateur de probabilités de scénarios.
    """
    calculator = ScenarioProbabilityCalculator()
    
    print("═" * 75)
    print("    CALCULATEUR DE PROBABILITÉS DE SCÉNARIOS DE TRADING")
    print("═" * 75)
    print()
    
    # Exemple 1: Configuration A - Range Standard + Cassure Contre-Tendance
    print("EXEMPLE 1 : Configuration A")
    print("-" * 75)
    asian_range_pips = 40.0
    htf_trend = HTFTrendBias.BULLISH
    london_action = LondonInitialAction.BREAKOUT_LOW
    
    asian_state = calculator.classify_asian_range(asian_range_pips)
    scenario, prob_range, justification, analysis = calculator.analyze_scenario(
        asian_state, htf_trend, london_action
    )
    
    output = calculator.format_analysis_output(
        asian_range_pips, htf_trend, london_action,
        scenario, prob_range, justification, analysis
    )
    print(output)
    
    # Exemple 2: Configuration B - Range Compressé + Cassure Alignée
    print("\nEXEMPLE 2 : Configuration B")
    print("-" * 75)
    asian_range_pips = 20.0
    htf_trend = HTFTrendBias.BEARISH
    london_action = LondonInitialAction.BREAKOUT_LOW
    
    asian_state = calculator.classify_asian_range(asian_range_pips)
    scenario, prob_range, justification, analysis = calculator.analyze_scenario(
        asian_state, htf_trend, london_action
    )
    
    output = calculator.format_analysis_output(
        asian_range_pips, htf_trend, london_action,
        scenario, prob_range, justification, analysis
    )
    print(output)
    
    # Exemple 3: Configuration C - Range Étendu
    print("\nEXEMPLE 3 : Configuration C")
    print("-" * 75)
    asian_range_pips = 60.0
    htf_trend = HTFTrendBias.NEUTRAL
    london_action = LondonInitialAction.INTERNAL
    
    asian_state = calculator.classify_asian_range(asian_range_pips)
    scenario, prob_range, justification, analysis = calculator.analyze_scenario(
        asian_state, htf_trend, london_action
    )
    
    output = calculator.format_analysis_output(
        asian_range_pips, htf_trend, london_action,
        scenario, prob_range, justification, analysis
    )
    print(output)


if __name__ == "__main__":
    main()

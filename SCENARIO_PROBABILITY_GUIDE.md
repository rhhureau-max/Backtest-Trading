# Calculateur de Probabilités de Scénarios de Trading

## Description

Ce module implémente un système d'analyse de probabilités pour les scénarios de trading basé sur:
- Les caractéristiques du range asiatique
- Le biais de tendance HTF (Higher Time Frame - Daily/4H)
- L'action initiale de la session de Londres

Le système répond à la question: **"Quel est le pourcentage de chance que le scénario X se produise aujourd'hui, étant donné les conditions Y?"**

## Structure de l'Algorithme

### PHASE 1 : COLLECTE DES VARIABLES D'ENTRÉE (INPUT)

#### 1. État du Range Asiatique (ERA)
- **Compressé** : < 30 pips
- **Standard** : 30-50 pips
- **Étendu** : > 50 pips

#### 2. Biais de Tendance HTF (Daily/4H)
- **Haussier** : Tendance haussière sur le Daily ou 4H
- **Baissier** : Tendance baissière sur le Daily ou 4H
- **Neutre** : Pas de tendance claire

#### 3. Action Initiale de Londres (07:00-09:00 GMT)
- **Cassure Haut** : Le prix casse le haut du range asiatique
- **Cassure Bas** : Le prix casse le bas du range asiatique
- **Interne** : Le prix reste à l'intérieur du range asiatique

### PHASE 2 : MATRICE DE SCÉNARIOS ET PROBABILITÉS (OUTPUT)

#### Configuration A : Range Asiatique Standard + Cassure Contre-Tendance
**Exemple** : Tendance Daily Haussière + Cassure du Bas Asiatique à 08:30 GMT

- **Scénario Probable** : RETOURNEMENT (SCÉNARIO I)
- **Pourcentage Estimé d'Occurrence** : 65% - 75%
- **Justification** : La chasse aux stops est le comportement par défaut (70% invalidation HOD/LOD). La tendance de fond agit comme un aimant de rappel.
- **Analyse de Session** : Le marché cherche la liquidité "Discount" (basse) pour alimenter la hausse.

#### Configuration B : Range Asiatique Compressé + Cassure Tendance Alignée
**Exemple** : Tendance Daily Baissière + Range Asie 20 pips + Cassure du Bas Asiatique

- **Scénario Probable** : CONTINUATION (SCÉNARIO II)
- **Pourcentage Estimé d'Occurrence** : 50% - 60%
- **Justification** : L'expansion de range est nécessaire après une compression. L'alignement HTF réduit la friction. Le taux d'échec (faux breakout) diminue sur les ranges très compressés.
- **Analyse de Session** : "Trend Day" classique. Pas de retour à la moyenne immédiat.

#### Configuration C : Range Asiatique Étendu ou Contexte News
**Exemple** : Asie très volatile ou attente NFP

- **Scénario Probable** : CONSOLIDATION / RETRACEMENT (SCÉNARIO III)
- **Pourcentage Estimé d'Occurrence** : 40% - 50%
- **Justification** : Si l'Asie a déjà consommé l'ATR (Average True Range) moyen, le potentiel d'expansion de Londres est limité statistiquement.
- **Analyse de Session** : Londres va probablement rester à l'intérieur ou faire un faux breakout marginal.

## Installation

Aucune dépendance externe n'est requise. Le script utilise uniquement la bibliothèque standard Python.

```bash
# Python 3.6+ requis
python3 scenario_probability_calculator.py
```

## Utilisation

### Utilisation en Ligne de Commande

Exécutez le script directement pour voir des exemples:

```bash
python3 scenario_probability_calculator.py
```

### Utilisation Programmatique

```python
from scenario_probability_calculator import (
    ScenarioProbabilityCalculator,
    AsianRangeState,
    HTFTrendBias,
    LondonInitialAction
)

# Créer une instance du calculateur
calculator = ScenarioProbabilityCalculator()

# Exemple: Analyser un scénario spécifique
asian_range_pips = 40.0  # Range asiatique de 40 pips
htf_trend = HTFTrendBias.BULLISH  # Tendance haussière
london_action = LondonInitialAction.BREAKOUT_LOW  # Cassure du bas

# Classifier le range asiatique
asian_state = calculator.classify_asian_range(asian_range_pips)

# Analyser le scénario
scenario, prob_range, justification, analysis = calculator.analyze_scenario(
    asian_state, 
    htf_trend, 
    london_action
)

# Formater et afficher les résultats
output = calculator.format_analysis_output(
    asian_range_pips, 
    htf_trend, 
    london_action,
    scenario, 
    prob_range, 
    justification, 
    analysis
)
print(output)
```

## Exemples de Résultats

### Exemple 1: Configuration A - Retournement Probable

```
PHASE 1 : VARIABLES D'ENTRÉE (INPUT)
─────────────────────────────────────────────────────────────────────────
  • État du Range Asiatique : Standard (40.0 pips entre 30-50)
  • Biais de Tendance HTF    : Haussier
  • Action Initiale Londres  : Cassure Bas

PHASE 2 : MATRICE DE SCÉNARIOS ET PROBABILITÉS (OUTPUT)
─────────────────────────────────────────────────────────────────────────
  ► Scénario Probable         : RETOURNEMENT (SCÉNARIO I)
  ► Pourcentage Estimé        : 65% - 75%
```

### Exemple 2: Configuration B - Continuation Probable

```
PHASE 1 : VARIABLES D'ENTRÉE (INPUT)
─────────────────────────────────────────────────────────────────────────
  • État du Range Asiatique : Compressé (20.0 pips < 30)
  • Biais de Tendance HTF    : Baissier
  • Action Initiale Londres  : Cassure Bas

PHASE 2 : MATRICE DE SCÉNARIOS ET PROBABILITÉS (OUTPUT)
─────────────────────────────────────────────────────────────────────────
  ► Scénario Probable         : CONTINUATION (SCÉNARIO II)
  ► Pourcentage Estimé        : 50% - 60%
```

### Exemple 3: Configuration C - Consolidation Probable

```
PHASE 1 : VARIABLES D'ENTRÉE (INPUT)
─────────────────────────────────────────────────────────────────────────
  • État du Range Asiatique : Étendu (60.0 pips > 50)
  • Biais de Tendance HTF    : Neutre
  • Action Initiale Londres  : Interne

PHASE 2 : MATRICE DE SCÉNARIOS ET PROBABILITÉS (OUTPUT)
─────────────────────────────────────────────────────────────────────────
  ► Scénario Probable         : CONSOLIDATION / RETRACEMENT (SCÉNARIO III)
  ► Pourcentage Estimé        : 40% - 50%
```

## API Reference

### Classes Principales

#### `ScenarioProbabilityCalculator`
Classe principale pour calculer les probabilités de scénarios.

**Méthodes:**
- `classify_asian_range(range_pips: float) -> AsianRangeState`: Classifie le range asiatique
- `analyze_scenario(asian_range_state, htf_trend, london_action) -> Tuple`: Analyse le scénario et retourne les probabilités
- `format_analysis_output(...)` -> str: Formate les résultats pour l'affichage

#### Enums

**`AsianRangeState`**
- `COMPRESSED`: < 30 pips
- `STANDARD`: 30-50 pips
- `EXTENDED`: > 50 pips

**`HTFTrendBias`**
- `BULLISH`: Tendance haussière
- `BEARISH`: Tendance baissière
- `NEUTRAL`: Tendance neutre

**`LondonInitialAction`**
- `BREAKOUT_HIGH`: Cassure du haut
- `BREAKOUT_LOW`: Cassure du bas
- `INTERNAL`: Mouvement interne

**`ScenarioType`**
- `REVERSAL`: Retournement (Scénario I)
- `CONTINUATION`: Continuation (Scénario II)
- `CONSOLIDATION`: Consolidation/Retracement (Scénario III)

## Intégration avec les Données de Backtest

Ce calculateur peut être intégré avec les données historiques CSV présentes dans le repository pour:
1. Valider les probabilités énoncées sur des données réelles
2. Affiner les seuils de probabilité par instrument (ES, NQ, etc.)
3. Créer des rapports de performance historique des scénarios

## Notes Importantes

- Les probabilités fournies sont basées sur des analyses de microstructure de marché et des données de backtest
- Ces probabilités sont des estimations statistiques et ne garantissent pas le résultat d'un trade spécifique
- Il est recommandé d'utiliser cet outil en combinaison avec d'autres analyses techniques et fondamentales
- Les configurations peuvent être affinées en fonction de l'instrument tradé et des conditions de marché

## Licence

Ce projet fait partie du repository Backtest-Trading.

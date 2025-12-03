# Tokyo Session Trading Strategy Analysis

## Vue d'ensemble

Ce projet analyse une stratégie de trading basée sur la session de Tokyo et la zone de manipulation de Londres. L'objectif est de calculer la probabilité que le prix revienne toucher le niveau d'équilibre (50%) de la session de Tokyo après une cassure pendant la zone de manipulation.

## Résultats Principaux

### 📊 Probabilité Globale: **68.47%**

**Période d'analyse:** 2018-2025 (1478 signaux analysés)

- **Cassures du HIGH Tokyo:** 64.29% de succès (515/801)
- **Cassures du LOW Tokyo:** 73.41% de succès (497/677)
- **Temps moyen de retour:** 2.11 heures
- **Temps médian de retour:** 1.00 heure

## Règles de la Stratégie

### 1. Session Tokyo (19:00 - 00:00)
- Identifier le **Plus Haut (High)** de la session
- Identifier le **Plus Bas (Low)** de la session
- Calculer la **Range** = High - Low

### 2. Niveau d'Équilibre
```
Équilibre (50%) = (Tokyo High + Tokyo Low) / 2
```

### 3. Zone de Manipulation (02:00 - 02:30 Londres)
- Session suivant la session de Tokyo
- Zone critique pour identifier les cassures

### 4. Condition de Déclenchement
Le signal est activé lorsque le prix **casse** (transperce) le High ou le Low de Tokyo pendant la zone de manipulation (02:00-02:30).

### 5. Objectif
Mesurer la probabilité que le prix revienne **toucher le niveau des 50%** de la session Tokyo dans les **6 heures** suivant la cassure.

## Résultats Détaillés par Année

| Année | Total Signaux | Succès | Probabilité |
|-------|---------------|--------|-------------|
| 2018  | 175           | 117    | 66.86%      |
| 2019  | 169           | 113    | 66.86%      |
| 2020  | 178           | 83     | 46.63%      |
| 2021  | 188           | 136    | 72.34%      |
| 2022  | 191           | 144    | 75.39%      |
| 2023  | 223           | 171    | 76.68%      |
| 2024  | 198           | 142    | 71.72%      |
| 2025  | 156           | 106    | 67.95%      |

### Observations
- L'année 2020 montre une probabilité plus faible (46.63%), possiblement due à la volatilité du COVID-19
- Les années 2022-2023 montrent les meilleures performances (>75%)
- La stratégie est cohérente sur la période 2018-2025

## Statistiques de Temps de Retour

Pour les signaux qui ont réussi à toucher le niveau 50%:

- **Minimum:** 0.08 heures (~5 minutes)
- **Maximum:** 6.00 heures
- **Moyenne:** 2.11 heures
- **Médiane:** 1.00 heure
- **Écart-type:** 2.13 heures

**Interprétation:** La moitié des retours se produisent en moins d'1 heure, ce qui suggère que la réaction est souvent rapide.

## Structure des Fichiers

### Fichiers de Données
Les données sont organisées par année et par timeframe:
```
[ANNÉE] 5m.csv   - Données 5 minutes
[ANNÉE] 15m.csv  - Données 15 minutes
[ANNÉE] 1H.csv   - Données 1 heure
```

Format CSV: `Date;Time;Open;High;Low;Close;Volume`

### Fichiers Générés

#### 1. `tokyo_session_analysis.py`
Script Python principal qui effectue l'analyse complète.

#### 2. `tokyo_analysis_report.txt`
Rapport détaillé incluant:
- Statistiques globales
- Décomposition par type de cassure (HIGH/LOW)
- Statistiques temporelles
- Répartition annuelle
- Exemples de signaux

#### 3. `tokyo_analysis_results.csv`
Fichier CSV avec tous les signaux détectés, incluant:
- Date et horaires
- Niveaux Tokyo (High, Low, Equilibrium)
- Type et moment de cassure
- Résultat (retour ou non au 50%)
- Temps de retour si applicable

## Installation et Utilisation

### Prérequis
```bash
pip install pandas numpy
```

### Exécution
```bash
python3 tokyo_session_analysis.py
```

Le script va:
1. Charger tous les fichiers CSV de 2018 à 2025
2. Analyser chaque journée selon les règles de la stratégie
3. Générer les rapports d'analyse

### Personnalisation

Vous pouvez modifier les paramètres dans le script:

```python
# Modifier les années à analyser
analyzer.load_data(years=range(2018, 2026), timeframes=['5m', '15m', '1H'])

# Modifier la fenêtre de temps pour le retour
return_info = analyzer.check_return_to_equilibrium(
    breakout_time,
    tokyo_eq,
    hours=6  # Modifier ici
)
```

## Interprétation des Résultats

### Points Forts de la Stratégie

1. **Probabilité élevée (68.47%):** La stratégie montre une forte tendance du prix à revenir vers l'équilibre.

2. **Asymétrie intéressante:** 
   - Les cassures du LOW (73.41%) sont plus fiables que celles du HIGH (64.29%)
   - Suggère que les mouvements baissiers ont tendance à créer de meilleurs retracements

3. **Réaction rapide:** 
   - 50% des retours en moins d'1 heure
   - Opportunités de trading à court terme

4. **Cohérence temporelle:** 
   - La stratégie fonctionne sur 8 ans
   - Performance stable malgré différents environnements de marché

### Considérations

1. **Volatilité du marché:** L'année 2020 montre que les périodes de haute volatilité peuvent affecter la stratégie.

2. **Gestion du risque:** Même avec 68% de probabilité, 32% des signaux ne reviennent pas au niveau 50% dans les 6 heures.

3. **Timeframes multiples:** L'analyse utilise des données de 5m, 15m et 1H pour plus de précision.

## Code Source Principal

Le script `tokyo_session_analysis.py` est organisé en classe avec les méthodes suivantes:

- `load_data()`: Charge les fichiers CSV
- `identify_tokyo_session()`: Identifie les sessions Tokyo
- `identify_manipulation_zone()`: Identifie les zones de manipulation
- `check_breakout()`: Détecte les cassures
- `check_return_to_equilibrium()`: Vérifie le retour au 50%
- `analyze()`: Exécute l'analyse complète
- `generate_report()`: Génère les rapports

## Visualisation des Données

Le fichier CSV `tokyo_analysis_results.csv` peut être importé dans Excel, Python (pandas), ou tout autre outil d'analyse pour créer des visualisations personnalisées.

Exemple avec pandas:
```python
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('tokyo_analysis_results.csv')

# Distribution des temps de retour
df[df['returned_to_eq']]['time_to_return_hours'].hist(bins=20)
plt.xlabel('Heures')
plt.ylabel('Fréquence')
plt.title('Distribution du temps de retour au 50%')
plt.show()
```

## Conclusion

Cette stratégie basée sur la session de Tokyo et la zone de manipulation de Londres démontre une **probabilité significative (68.47%)** que le prix revienne toucher le niveau d'équilibre 50% dans les 6 heures suivant une cassure.

Les cassures du LOW de Tokyo sont particulièrement fiables (73.41%), et la majorité des retours se produisent rapidement (médiane: 1 heure).

**Note:** Ces résultats sont basés sur des données historiques et ne garantissent pas les performances futures. Toujours effectuer vos propres analyses et gérer le risque de manière appropriée.

---

**Date d'analyse:** Décembre 2025  
**Période couverte:** 2018-2025  
**Total de signaux:** 1478

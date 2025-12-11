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

## 💥 Amplitude de Manipulation (02:00-02:30)

L'amplitude de manipulation mesure **jusqu'où le prix va au-delà du range Tokyo** pendant la zone de manipulation (02:00-02:30) avant de potentiellement revenir vers l'équilibre.

### Calcul de l'Amplitude

- **Pour cassures HAUSSIÈRES (HIGH):** `Amplitude = (Plus haut 02:00-02:30) - (Tokyo High)`
- **Pour cassures BAISSIÈRES (LOW):** `Amplitude = (Tokyo Low) - (Plus bas 02:00-02:30)`

### Statistiques Globales

| Métrique | Valeur (points) |
|----------|-----------------|
| **Moyenne globale** | 29.49 |
| **Médiane globale** | 20.06 |
| **Minimum** | 0.27 |
| **Maximum** | 374.89 |
| **Écart-type** | 31.48 |

### Par Type de Cassure

#### Cassures HAUSSIÈRES (HIGH)
- **Moyenne:** 27.67 points
- **Médiane:** 19.43 points
- **Min/Max:** 0.28 / 374.89 points

#### Cassures BAISSIÈRES (LOW)
- **Moyenne:** 31.64 points
- **Médiane:** 20.90 points
- **Min/Max:** 0.27 / 280.27 points

### Interprétation

1. **Dépassement modéré:** En médiane, le prix dépasse le range Tokyo d'environ **20 points** pendant la manipulation
2. **Asymétrie:** Les cassures LOW tendent à aller légèrement plus loin (31.64 vs 27.67 points en moyenne)
3. **Variabilité importante:** L'écart-type de 31.48 points indique une forte variabilité selon les conditions de marché
4. **Extremes rares:** Les dépassements de plus de 100 points sont exceptionnels mais possibles (max 374.89 points)

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
- **Amplitude de manipulation** (nouveau)
- Résultat (retour ou non au 50%)
- Temps de retour si applicable

#### 4. `visualize_results.py`
Script de visualisation qui génère:
- `tokyo_statistics.png` - Statistiques globales
- `tokyo_time_series.png` - Analyse temporelle
- `tokyo_range_analysis.png` - Analyse de la range Tokyo
- `tokyo_manipulation_amplitude.png` - **Analyse de l'amplitude de manipulation** (nouveau)

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

4. **Amplitude de manipulation:** Connaître l'amplitude moyenne (~20-30 points) permet de:
   - Placer des stop-loss adaptés
   - Identifier les manipulations extrêmes (>100 points)
   - Estimer le potentiel risque/récompense avant le retour à l'équilibre

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

### Génération Automatique des Graphiques

Exécutez le script de visualisation pour générer automatiquement tous les graphiques:

```bash
pip install matplotlib
python3 visualize_results.py
```

Cela génère 4 fichiers PNG:
1. **tokyo_statistics.png** - Vue d'ensemble des statistiques (taux de succès, types de cassures, temps de retour, performance annuelle)
2. **tokyo_time_series.png** - Évolution temporelle des performances
3. **tokyo_range_analysis.png** - Analyse de la range Tokyo et son impact
4. **tokyo_manipulation_amplitude.png** - Distribution et analyse de l'amplitude de manipulation

### Analyse Personnalisée

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

# Analyse de l'amplitude de manipulation
df['manipulation_amplitude'].hist(bins=30)
plt.xlabel('Amplitude (points)')
plt.ylabel('Fréquence')
plt.title('Distribution de l\'amplitude de manipulation')
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

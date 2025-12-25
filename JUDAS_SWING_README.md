# London Killzone Judas Swing Backtest

## Description

Ce script Python réalise un backtest complet sur le NQ (Nasdaq Futures) avec des données 1 minute de 2018 à aujourd'hui, en analysant la stratégie basée sur la **London Killzone** et le concept ICT de **Judas Swing**.

## Concept ICT : Judas Swing

Le **Judas Swing** est un concept de trading développé par Inner Circle Trader (ICT) qui identifie les manipulations de marché avant un mouvement directionnel. 

### Principe

1. **Session de Tokyo (17:00-24:00 veille)** : Définit les niveaux clés
   - Tokyo High : Le plus haut de la session
   - Tokyo Low : Le plus bas de la session  
   - Tokyo EQ (Equilibrium) : Point d'équilibre = (High + Low) / 2

2. **London Killzone (01:00-05:00)** : Fenêtre d'analyse principale
   - Zone de volatilité élevée lors de l'ouverture de Londres
   - Période où se produisent les manipulations de marché

3. **Détection du Judas Swing** :
   - **Manipulation** : Le prix casse Tokyo_High OU Tokyo_Low (fausse cassure)
   - **Retracement** : Le prix revient toucher le Tokyo_EQ avant 05:00 (retournement confirmé)
   - Cette séquence indique une manipulation des traders retail suivie d'un retournement

## Prérequis

```bash
pip install pandas numpy
```

## Utilisation

### Exécution Simple

```bash
python3 london_killzone_judas_swing_backtest.py
```

### Structure des Données

Le script charge automatiquement les fichiers de données 1 minute :
- Format : CSV avec délimiteur point-virgule (;)
- Colonnes : Date, Time, Open, High, Low, Close, Volume
- Formats supportés : `.csv` et `.csv.zip`

### Fichiers de Données Requis

```
2018 1m.csv.zip
2019 1m.csv.zip
2020 1m.csv.zip
2021 1m.csv.zip
2022 1m.csv.zip
2023 1m.csv.zip
2024 1m.csv.zip
2025 1m.csv
```

## Résultats du Backtest (2018-2025)

### Statistiques Globales

- **Sessions Analysées** : 2,034 jours de trading
- **Judas Swings Détectés** : 284 occurrences
- **Ratio de Succès** : 13.96%

### Métriques de Performance

#### Taille du Peak (Distance de Manipulation)
- **Moyenne** : 21.00 points
- **Médiane** : 13.12 points

La médiane inférieure à la moyenne suggère que la plupart des manipulations sont relativement petites (13 points), avec quelques grandes manipulations qui augmentent la moyenne.

#### Temps jusqu'au Peak
- **Moyenne** : 62.43 minutes (≈ 1.04 heures)

En moyenne, le peak de manipulation se produit environ 1 heure après le début de la London Killzone (01:00).

## Interprétation des Résultats

### Ratio de 13.96%

Ce ratio indique qu'environ **1 jour sur 7** présente un pattern de Judas Swing complet. C'est une fréquence significative pour un pattern spécifique, suggérant :
- Le pattern est suffisamment récurrent pour être tradable
- Il ne se produit pas trop souvent (évite le sur-trading)
- Reste sélectif et nécessite patience

### Directions Observées

- **Bearish Reversal** : Break du Tokyo_High → Reversal vers le bas
- **Bullish Reversal** : Break du Tokyo_Low → Reversal vers le haut

### Applications Trading

1. **Setup d'Entrée** :
   - Attendre la cassure de Tokyo High/Low dans la Killzone
   - Confirmer le retournement vers Tokyo_EQ
   - Entrer sur le retracement vers EQ

2. **Gestion du Risque** :
   - Stop-loss au-delà du peak de manipulation
   - Distance moyenne : ~21 points
   - Distance médiane : ~13 points

3. **Timing** :
   - Window optimal : 01:00 - 03:00 (peak moyen à 62 min)
   - Surveiller activement les 2 premières heures de la Killzone

## Exemples de Détections

```
Date         Direction           Peak (pts)  Temps (min)
2018-02-05   bearish_reversal    4.69        37.0
2018-03-01   bearish_reversal    13.18       100.0
2018-03-16   bullish_reversal    4.38        105.0
2018-04-13   bearish_reversal    2.63        51.0
2018-04-16   bullish_reversal    10.80       78.0
```

## Architecture du Code

### Fonctions Principales

- `load_csv_data()` : Charge les données CSV ou ZIP
- `prepare_dataframe()` : Prépare et nettoie les données
- `load_all_data()` : Combine toutes les années de données
- `get_tokyo_session()` : Calcule les niveaux de Tokyo
- `detect_judas_swing()` : Détecte le pattern Judas Swing
- `run_backtest()` : Exécute l'analyse complète
- `print_report()` : Affiche le rapport formaté

### Gestion des Erreurs

Le script gère automatiquement :
- Fichiers manquants (affiche un avertissement)
- Jours sans données Tokyo (ignorés)
- Sessions incomplètes de Killzone
- Formats de données multiples (CSV et ZIP)

## Modifications Possibles

### Ajuster les Paramètres

```python
# Dans la fonction get_tokyo_session() - modifier les heures
tokyo_start = pd.Timestamp(prev_date.date()) + pd.Timedelta(hours=17)
tokyo_end = pd.Timestamp(prev_date.date()) + pd.Timedelta(hours=24)

# Dans la fonction detect_judas_swing() - modifier la Killzone
killzone_start = pd.Timestamp(date.date()) + pd.Timedelta(hours=1)
killzone_end = pd.Timestamp(date.date()) + pd.Timedelta(hours=5)
```

### Ajouter des Filtres

```python
# Exemple : Filtrer par taille minimale de manipulation
if result['peak_size'] < 10:  # Ignorer les peaks < 10 points
    result['detected'] = False
```

### Export des Résultats

```python
# Ajouter à la fin de main()
import pandas as pd
results_df = pd.DataFrame(stats['detailed_results'])
results_df.to_csv('judas_swing_results.csv', index=False)
```

## Limitations

1. **Heures Fixées** : Le script assume que les heures sont déjà correctes (pas de conversion de fuseau horaire)
2. **Pattern Strict** : Détecte uniquement les swings "purs" (cassure d'un seul côté)
3. **Données Requises** : Nécessite les données de la veille pour Tokyo session

## Développements Futurs

- [ ] Analyse des performances par année
- [ ] Corrélation avec la volatilité du marché
- [ ] Filtres de contexte macro (tendance long terme)
- [ ] Optimisation des seuils de détection
- [ ] Visualisations graphiques des patterns

## Auteur

Développé en tant qu'expert en Quantitative Trading et Python.

## Licence

Ce script est fourni à des fins éducatives et de recherche.

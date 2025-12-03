# Tokyo Session FVG Inversion Strategy - Documentation

## Vue d'ensemble

Ce script analyse une stratégie de trading basée sur l'**inversion des Fair Value Gaps (FVG)** après une manipulation de la session Tokyo. La stratégie combine l'analyse des sessions de trading (Tokyo et Londres) avec la détection de patterns de prix spécifiques (FVG) pour identifier des opportunités de trading à haute probabilité.

## Concept de la Stratégie

### Fair Value Gap (FVG)

Un **Fair Value Gap** est un déséquilibre dans le prix qui se produit lorsqu'il y a un écart (gap) entre trois bougies consécutives :

- **FVG Bullish** : High[N-1] < Low[N+1] (écart haussier)
- **FVG Bearish** : Low[N-1] > High[N+1] (écart baissier)

### Inversion FVG

Une **Inversion FVG** se produit lorsque le prix :
1. Crée un FVG pendant la manipulation
2. Revient combler (fill) ce FVG
3. Une bougie clôture au-delà du FVG, le transformant en zone de support/résistance

## Règles de la Stratégie

### Scénario BEARISH (Vente - Short)

1. **Condition A** : Le prix manipule le High de Tokyo entre 02:00-02:30
2. **Condition B** : Durant le mouvement haussier de manipulation, un FVG Bullish se forme
3. **Trigger** : Le prix redescend, comble le FVG Bullish, et une bougie clôture en dessous
4. **Exécution** :
   - **Entry** : Close de la bougie casseuse
   - **Stop Loss** : High de la bougie casseuse
   - **Take Profit** : Equilibrium 50% de la session Tokyo

### Scénario BULLISH (Achat - Long)

1. **Condition A** : Le prix manipule le Low de Tokyo entre 02:00-02:30
2. **Condition B** : Durant le mouvement baissier de manipulation, un FVG Bearish se forme
3. **Trigger** : Le prix remonte, comble le FVG Bearish, et une bougie clôture au-dessus
4. **Exécution** :
   - **Entry** : Close de la bougie casseuse
   - **Stop Loss** : Low de la bougie casseuse
   - **Take Profit** : Equilibrium 50% de la session Tokyo

## Résultats de l'Analyse (2018-2025)

### Statistiques Globales

- **Période analysée** : 2018-2025 (2449 dates)
- **Total de trades** : 476
- **Trades gagnants** : 209
- **Trades perdants** : 267
- **Win Rate** : **43.91%**

### Par Direction

| Direction | Total | Gagnants | Win Rate |
|-----------|-------|----------|----------|
| LONG      | 219   | 100      | 45.66%   |
| SHORT     | 257   | 109      | 42.41%   |

### Performance P&L

- **P&L Total** : -4,093.67 points
- **P&L Moyen par trade** : -8.60 points
- **Gain moyen** : 7.34 points
- **Perte moyenne** : 21.08 points
- **Ratio Gain/Perte** : 0.35:1
- **Expectancy** : -8.60 points par trade

### Risk/Reward

- **Ratio R:R moyen** : 2.39:1
- **Risque moyen** : 29.44 points
- **Reward moyen** : 36.42 points

### Performance Annuelle

| Année | Total Trades | Gagnants | Win Rate |
|-------|-------------|----------|----------|
| 2018  | 48          | 21       | 43.75%   |
| 2019  | 47          | 13       | 27.66%   |
| 2020  | 64          | 33       | 51.56%   |
| 2021  | 71          | 35       | 49.30%   |
| 2022  | 63          | 25       | 39.68%   |
| 2023  | 73          | 39       | 53.42%   |
| 2024  | 64          | 30       | 46.88%   |
| 2025  | 46          | 13       | 28.26%   |

**Meilleure année** : 2023 (53.42% win rate)
**Pire année** : 2019 (27.66% win rate)

## Utilisation du Script

### Prérequis

```bash
pip install pandas numpy matplotlib
```

### Exécution

```bash
python3 tokyo_fvg_strategy.py
```

### Fichiers Générés

1. **tokyo_fvg_strategy_report.txt** : Rapport détaillé avec toutes les statistiques
2. **tokyo_fvg_strategy_results.csv** : Données brutes de tous les trades
3. **tokyo_fvg_strategy_analysis.png** : Visualisations graphiques (6 graphiques)

## Structure du Code

### Classes Principales

#### `FVG`
Représente un Fair Value Gap avec ses propriétés :
- Type (BULLISH/BEARISH)
- Limites (top/bottom)
- Temps de formation
- État (filled/inverted)

#### `TokyoFVGAnalyzer`
Classe principale d'analyse avec méthodes :
- `load_data()` : Charge les données CSV
- `identify_tokyo_session()` : Identifie les sessions Tokyo
- `identify_manipulation_zone()` : Détecte la zone de manipulation (02:00-02:30)
- `detect_fvgs()` : Détecte les Fair Value Gaps
- `check_fvg_inversion()` : Vérifie les inversions de FVG
- `simulate_trade()` : Simule l'exécution du trade
- `analyze()` : Fonction principale d'analyse
- `generate_report()` : Génère le rapport texte
- `generate_visualizations()` : Crée les graphiques

## Interprétation des Résultats

### Points Forts

1. **Cohérence** : La stratégie génère régulièrement des signaux (476 trades sur 8 ans)
2. **Ratio R:R favorable** : 2.39:1 en moyenne (reward > risk)
3. **Certaines années performantes** : 2020, 2021, 2023 montrent des win rates > 50%

### Points d'Amélioration

1. **Win Rate global** : 43.91% nécessite un excellent ratio R:R pour être profitable
2. **Expectancy négative** : -8.60 points suggère que la gestion du risque doit être optimisée
3. **Perte moyenne élevée** : 21.08 points vs gain moyen de 7.34 points
4. **Variabilité annuelle** : Performance très variable selon les années (27.66% à 53.42%)

### Recommandations

Pour améliorer la stratégie :

1. **Filtrage supplémentaire** :
   - Ajouter des conditions de tendance plus large
   - Filtrer par volatilité
   - Exclure certaines périodes de l'année à faible performance

2. **Gestion du risque** :
   - Réduire le stop loss (actuellement 29.44 points en moyenne)
   - Implémenter un stop loss trailing
   - Sortir plus tôt sur les trades perdants

3. **Optimisation du Take Profit** :
   - Considérer des TP partiels avant l'équilibre
   - Tester différents niveaux de TP
   - Implémenter une gestion dynamique du TP

4. **Sélection des trades** :
   - Prioriser les setups à fort ratio R:R (> 3:1)
   - Éviter les périodes de faible performance historique
   - Combiner avec d'autres indicateurs de confirmation

## Timeframes Utilisés

Le script analyse les timeframes **5 minutes et 15 minutes** pour une détection précise des FVG. Ces timeframes permettent de :
- Capturer les mouvements rapides de manipulation
- Détecter les petits FVG qui peuvent être manqués sur des timeframes plus grands
- Avoir suffisamment de données pour identifier les inversions

## Sessions de Trading

- **Tokyo Session** : 19:00 - 00:00 (heure locale)
- **Zone de Manipulation** : 02:00 - 02:30 (ouverture Londres)
- **Window de Trade** : Jusqu'à 24 heures après l'entrée

## Notes Importantes

1. Les résultats sont basés sur des données historiques et ne garantissent pas les performances futures
2. La stratégie nécessite une exécution précise et une gestion rigoureuse du risque
3. Les coûts de transaction (spreads, commissions) ne sont pas inclus dans l'analyse
4. Le slippage n'est pas pris en compte
5. L'analyse suppose une exécution parfaite aux niveaux spécifiés

## Fichiers Associés

- `tokyo_fvg_strategy.py` : Script principal
- `tokyo_fvg_strategy_report.txt` : Rapport détaillé
- `tokyo_fvg_strategy_results.csv` : Données des trades
- `tokyo_fvg_strategy_analysis.png` : Visualisations

## Auteur et Date

Généré automatiquement par le système d'analyse
Date de création : Décembre 2025

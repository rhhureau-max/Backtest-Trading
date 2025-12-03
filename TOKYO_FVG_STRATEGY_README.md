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

### Filtre Risk/Reward (R/R)

⚠️ **FILTRE OBLIGATOIRE** : Un trade n'est exécuté que si son ratio Risk/Reward est ≥ 1.0

- **Risk** = |Entry - Stop Loss|
- **Reward** = |Take Profit - Entry|
- **R/R Ratio** = Reward / Risk

**Si R/R < 1.0**, le trade est **complètement ignoré** et n'apparaît pas dans les statistiques.

## Résultats de l'Analyse (2018-2025)

### Impact du Filtre Risk/Reward

🔍 **Analyse avec filtre R/R ≥ 1.0** :

- **Trades potentiels** (avant filtre) : 476
- **Trades filtrés** (R/R < 1.0) : 203 (42.65%)
- **Trades conservés** (R/R ≥ 1.0) : 273 (57.35%)

✅ **Le filtre R/R élimine 42.65% des trades à faible potentiel de gain**

### Statistiques Globales (APRÈS FILTRE R/R)

- **Période analysée** : 2018-2025 (2449 dates)
- **Total de trades exécutés** : 273
- **Trades gagnants** : 62
- **Trades perdants** : 211
- **Win Rate** : **22.71%**

### Par Direction

| Direction | Total | Gagnants | Win Rate |
|-----------|-------|----------|----------|
| LONG      | 123   | 31       | 25.20%   |
| SHORT     | 150   | 31       | 20.67%   |

### Performance P&L

- **P&L Total** : -1,271.34 points
- **P&L Moyen par trade** : -4.66 points
- **Gain moyen** : 36.78 points
- **Perte moyenne** : 16.83 points
- **Ratio Gain/Perte** : 2.19:1
- **Expectancy** : -4.66 points par trade

### Risk/Reward

- **Ratio R:R moyen** : **3.85:1** ⬆️ (excellent ratio grâce au filtre)
- **Risque moyen** : 16.71 points ⬇️ (réduit de 43% vs sans filtre)
- **Reward moyen** : 48.53 points ⬆️ (augmenté de 33% vs sans filtre)

### Performance Annuelle

| Année | Total Trades | Gagnants | Win Rate |
|-------|-------------|----------|----------|
| 2018  | 35          | 9        | 25.71%   |
| 2019  | 34          | 5        | 14.71%   |
| 2020  | 35          | 8        | 22.86%   |
| 2021  | 42          | 12       | 28.57%   |
| 2022  | 29          | 3        | 10.34%   |
| 2023  | 41          | 13       | 31.71%   |
| 2024  | 27          | 7        | 25.93%   |
| 2025  | 30          | 5        | 16.67%   |

**Meilleure année** : 2023 (31.71% win rate)
**Pire année** : 2022 (10.34% win rate)

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

1. **Filtre R/R efficace** : Élimine 42.65% des trades à faible potentiel
2. **Excellent ratio R:R** : 3.85:1 en moyenne (reward nettement > risk)
3. **Risque réduit** : 16.71 points en moyenne (43% de réduction vs sans filtre)
4. **Gains importants** : Gain moyen de 36.78 points (5x plus qu'avant filtre)
5. **Ratio Gain/Perte favorable** : 2.19:1 (les gains sont 2x plus grands que les pertes)

### Points d'Amélioration

1. **Win Rate faible** : 22.71% nécessite un très bon ratio R:R pour être profitable
2. **Expectancy négative** : -4.66 points suggère que la gestion du risque doit être optimisée
3. **Taux de réussite insuffisant** : Même avec le filtre R/R, moins de 1 trade sur 4 est gagnant
4. **Variabilité annuelle** : Performance très variable selon les années (10.34% à 31.71%)

### Recommandations

Pour améliorer la stratégie :

1. **Filtrage supplémentaire** :
   - ✅ **FAIT** : Filtre R/R ≥ 1.0 implémenté (élimine 42.65% des trades)
   - Ajouter des conditions de tendance plus large
   - Filtrer par volatilité
   - Exclure certaines périodes de l'année à faible performance (2019, 2022)
   - Considérer un filtre R/R plus strict (≥ 2.0 ou ≥ 3.0)

2. **Amélioration du Win Rate** :
   - Le filtre R/R améliore le ratio gain/perte mais réduit le win rate
   - Ajouter des confirmations supplémentaires avant l'entrée
   - Analyser pourquoi 77% des trades échouent
   - Considérer des filtres de tendance ou de structure de marché

3. **Optimisation du Take Profit** :
   - Avec un R:R de 3.85:1, le TP semble bien placé
   - Considérer des TP partiels (50% au 1:1, 50% au 3:1)
   - Tester différents niveaux de TP
   - Implémenter un trailing stop pour capturer plus de mouvement

4. **Sélection des trades** :
   - ✅ **FAIT** : Priorisation automatique des setups à R:R ≥ 1.0
   - Éviter les années historiquement faibles (2019: 14.71%, 2022: 10.34%)
   - Combiner avec d'autres indicateurs de confirmation
   - Analyser les caractéristiques des trades gagnants vs perdants

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

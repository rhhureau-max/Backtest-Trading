# Analyse des Retournements de Tendance - Backtesting

## Vue d'ensemble

Ce projet contient un script Python complet pour analyser les probabilités de retournement de tendance à court terme en utilisant deux patterns classiques de chandeliers japonais :
- **Marteau (Hammer)** : Signal de retournement haussier dans une tendance baissière
- **Étoile Filante (Shooting Star)** : Signal de retournement baissier dans une tendance haussière

## Fichiers du Projet

- **`candlestick_reversal_backtest.py`** : Script Python principal contenant toute la logique d'analyse
- **`backtest_results.txt`** : Rapport détaillé en format texte avec toutes les statistiques
- **`backtest_results.json`** : Données brutes au format JSON pour une analyse plus approfondie

## Données Analysées

### Instruments
- **NQ (Nasdaq 100 E-mini)** : 2018-2025
- **ES (S&P 500 E-mini)** : 2018-2025

### Timeframes
- **5 minutes** : ~554,000 bougies (NQ) et ~559,000 bougies (ES)
- **15 minutes** : ~185,000 bougies (NQ et ES)

### Période Totale
Du 1er janvier 2018 au 11 novembre 2025 (7+ années de données)

## Méthodologie

### 🆕 Smart Money Concepts (SMC) - Liquidity Sweeps

Cette version améliorée intègre l'analyse des **Liquidity Sweeps** (chasses aux stops), un concept clé du Smart Money Trading. L'analyse compare les patterns qui "sweepent" la liquidité versus les patterns "flottants".

### 🎯 Analyse Risk-Reward (RR)

Cette version inclut également une **analyse complète des ratios Risk-Reward** avec simulation de trades réels incluant Stop Loss et Take Profit. Cette analyse permet de déterminer le ratio RR optimal pour chaque type de pattern dans différents contextes.

#### Qu'est-ce qu'un Liquidity Sweep ?

Un **Liquidity Sweep** se produit lorsque le prix :
1. Casse un niveau clé (Swing High ou Swing Low) pour déclencher les stop loss
2. Capture la liquidité des traders piégés
3. Rejette immédiatement ce niveau et inverse sa direction

#### Types de Sweeps Analysés

**Bullish Reversal Sweep (Marteau avec Sweep)**
- Tendance baissière en cours
- La mèche basse du Marteau **casse un Swing Low récent**
- Le corps de la bougie **clôture au-dessus** du Swing Low (rejet)
- Signal : La Smart Money a chassé les stops avant de renverser le prix

**Bearish Reversal Sweep (Shooting Star avec Sweep)**  
- Tendance haussière en cours
- La mèche haute du Shooting Star **casse un Swing High récent**
- Le corps de la bougie **clôture en-dessous** du Swing High (rejet)
- Signal : La Smart Money a piégé les acheteurs (bull trap)

#### Détection des Swing Points

**Swing High** : Un sommet plus élevé que les **5 bougies avant et après**  
**Swing Low** : Un creux plus bas que les **5 bougies avant et après**

Les swing points récents sont recherchés sur les **20 dernières bougies**.

### Définition des Patterns

#### Marteau (Hammer)
Critères stricts pour identifier un marteau valide :
- ✓ Petit corps situé dans les **30% supérieurs** du range de la bougie
- ✓ Longue mèche basse : **au moins 2x la taille du corps**
- ✓ Petite mèche haute : **moins de 10% du range total**

#### Étoile Filante (Shooting Star)
Critères stricts pour identifier une étoile filante valide :
- ✓ Petit corps situé dans les **30% inférieurs** du range de la bougie
- ✓ Longue mèche haute : **au moins 2x la taille du corps**
- ✓ Petite mèche basse : **moins de 10% du range total**

### Détection de Tendance

La tendance court terme est détectée avec une **EMA à 9 périodes** :
- **Tendance haussière** : Prix au-dessus de l'EMA ET EMA montante (pente positive)
- **Tendance baissière** : Prix en-dessous de l'EMA ET EMA descendante (pente négative)

### Scénarios Testés

1. **Scénario Baissier** : 
   - Tendance baissière court terme → Marteau détecté 
   - → Vérification si la bougie suivante est haussière (Close > Open)

2. **Scénario Haussier** : 
   - Tendance haussière court terme → Shooting Star détectée 
   - → Vérification si la bougie suivante est baissière (Close < Open)

### Métriques Calculées

Pour chaque pattern détecté, nous calculons :
- **Taux de réussite immédiat** : La bougie suivante va-t-elle dans le sens du retournement ?
- **Taux de réussite à 2 bougies** : Au moins 1 des 2 bougies suivantes confirme le retournement
- **Taux de réussite à 3 bougies** : Au moins 2 des 3 bougies suivantes confirment le retournement
- **Gain moyen** : Performance moyenne après le pattern

### 🆕 Métriques SMC Additionnelles

Pour chaque pattern, l'analyse SMC ajoute :

#### Classification des Patterns
- **Avec Liquidity Sweep** : Pattern qui a sweepé un swing point
- **Sans Liquidity Sweep** : Pattern "flottant" sans sweep

#### Analyse Post-Sweep
- **Force du mouvement** : Nombre de points gagnés sur 1, 2, 3 bougies après le sweep
- **Ratio de vitesse** : Mouvement total / range moyen des bougies (mesure l'impulsion)
- **Taux de mouvement impulsif** : % de mouvements rapides et directionnels

#### Timing d'Entrée (pour patterns avec sweep)
- **Entrée Agressive** : Entrée à la clôture du pattern de sweep (taux de réussite)
- **Entrée avec Confirmation** : Attente de la bougie suivante de confirmation
  - Taux de réussite amélioré
  - Coût de l'attente en points (opportunité manquée)

#### Comparaison et Recommandations
- **Delta de performance** : Amélioration du taux de réussite avec sweep vs sans sweep
- **Ratio de force** : Combien de fois les mouvements avec sweep sont plus forts
- **Recommandation automatique** : Basée sur les données statistiques

### Facteurs Contextuels Analysés

1. **Volume élevé** : Volume supérieur à la moyenne mobile sur 20 périodes
2. **Proximité Support/Résistance** : Pattern se formant à ±0.5% d'un haut/bas récent (20 périodes)
3. **Ratio Mèche/Corps élevé** : Ratio > 3 (mèche très longue par rapport au corps)

## 🎯 Analyse Risk-Reward (RR)

Le script simule des trades réels avec gestion de Stop Loss et Take Profit pour déterminer le ratio RR optimal.

### Configuration des Stops

**Hammer (Bullish Reversal):**
- **Entry**: Prix de clôture du pattern
- **Stop Loss**: 1 point sous la mèche basse (Low du pattern)
- **Risk**: Distance entre Entry et SL
- **Take Profit**: Entry + (Risk × RR ratio)

**Shooting Star (Bearish Reversal):**
- **Entry**: Prix de clôture du pattern
- **Stop Loss**: 1 point au-dessus de la mèche haute (High du pattern)
- **Risk**: Distance entre Entry et SL
- **Take Profit**: Entry - (Risk × RR ratio)

### Ratios Testés

Le script teste 4 ratios Risk-Reward différents :
- **RR 1:1** - Risque 1 pour gagner 1
- **RR 1:1.5** - Risque 1 pour gagner 1.5
- **RR 1:2** - Risque 1 pour gagner 2
- **RR 1:2.5** - Risque 1 pour gagner 2.5

### Simulation de Trade

Pour chaque pattern détecté, le script simule un trade complet :

1. **Entry** à la clôture du pattern
2. **Monitoring** des 50 bougies suivantes maximum
3. **Exit** dès qu'un des niveaux est touché :
   - ✅ **WIN**: Take Profit atteint
   - ❌ **LOSS**: Stop Loss touché (priorité si touché dans la même bougie que TP)
   - ⏱️ **TIMEOUT**: Ni SL ni TP touché après 50 bougies

### Métriques Calculées

Pour chaque ratio RR et contexte (avec/sans liquidity sweep), le script calcule :

- **Win Rate**: Pourcentage de trades gagnants
- **Loss Rate**: Pourcentage de trades perdants
- **Timeout Rate**: Pourcentage de trades qui n'ont pas atteint SL ou TP
- **Bougies moyennes pour TP**: Durée moyenne pour atteindre le Take Profit
- **Bougies moyennes pour SL**: Durée moyenne pour toucher le Stop Loss
- **Expectancy**: (Win Rate × RR) - (Loss Rate × 1) - Gain moyen attendu par trade
- **Profit Factor**: (Total Wins × RR) / Total Losses - Ratio gains/pertes
- **MFE (Max Favorable Excursion)**: Meilleur point atteint avant exit
- **MAE (Max Adverse Excursion)**: Pire point atteint avant exit

### Comparaison par Contexte

Les statistiques RR sont calculées pour :
- **Avec Liquidity Sweep**: Patterns qui ont sweepé un swing point
- **Sans Liquidity Sweep**: Patterns "flottants"
- **Overall**: Tous les patterns combinés

Cette analyse permet de déterminer :
- Quel ratio RR est optimal pour chaque pattern
- Si les liquidity sweeps améliorent les performances RR
- Quel timing d'exit maximise les gains

## Résultats Clés

### 🆕 Résultats Smart Money Concepts (15 minutes - NQ)

#### Analyse des Liquidity Sweeps - Marteau

**Patterns avec Liquidity Sweep** : 144 détectés  
- Taux de réussite 1 bougie : **47.22%**
- Taux de réussite 2 bougies : **77.78%**
- Taux de réussite 3 bougies : **52.08%**
- Mouvement moyen post-sweep : **-4.02 points**
- Taux de mouvement impulsif : **43.06%**

**Timing d'Entrée** :
- Entrée Agressive : 47.22% de réussite
- Entrée Confirmation : 22.22% de réussite (coût : 5.65 points)

**Patterns sans Liquidity Sweep** : 1,753 détectés  
- Taux de réussite 1 bougie : **51.91%**
- Taux de réussite 2 bougies : **77.58%**
- Taux de réussite 3 bougies : **53.68%**

**Amélioration avec Sweep** :
- Delta 1 bougie : **-4.69%** (patterns sans sweep légèrement meilleurs)
- Delta 2 bougies : **+0.20%**
- Delta 3 bougies : **-1.60%**

**Recommandation** : FAIBLE - Pas d'amélioration claire avec les liquidity sweeps pour les marteaux.

#### Analyse des Liquidity Sweeps - Étoile Filante

**Patterns avec Liquidity Sweep** : 166 détectés  
- Taux de réussite 1 bougie : **51.81%**
- Taux de réussite 2 bougies : **79.52%**
- Taux de réussite 3 bougies : **49.40%**
- Mouvement moyen post-sweep : **3.74 points**
- Taux de mouvement impulsif : **40.36%**

**Timing d'Entrée** :
- Entrée Agressive : 51.81% de réussite
- Entrée Confirmation : 22.29% de réussite (coût : 8.68 points)

**Patterns sans Liquidity Sweep** : 2,530 détectés  
- Taux de réussite 1 bougie : **48.10%**
- Taux de réussite 2 bougies : **74.55%**
- Taux de réussite 3 bougies : **48.85%**

**Amélioration avec Sweep** :
- Delta 1 bougie : **+3.70%**
- Delta 2 bougies : **+4.97%**
- Delta 3 bougies : **+0.54%**

**Recommandation** : FAIBLE - Légère amélioration avec les liquidity sweeps sur les Shooting Stars.

#### Conclusions SMC

1. **Les Liquidity Sweeps sont rares** : Seulement 7-8% des patterns impliquent un sweep
2. **Impact modéré** : L'amélioration du taux de réussite est faible (+3-5% maximum)
3. **Shooting Stars > Hammers** : Les sweeps fonctionnent mieux sur les retournements baissiers
4. **Entrée Agressive recommandée** : L'attente de confirmation réduit la performance

### Synthèse Globale (5 minutes - NQ)

#### Marteau (5,834 patterns détectés)
- ✓ **50.38%** de réussite immédiate (1 bougie)
- ✓ **76.35%** de réussite sur 2 bougies
- ✓ **51.20%** de réussite sur 3 bougies

**Impact du contexte :**
- Volume élevé : **50.90%** de réussite
- Près Support/Résistance : **50.45%** de réussite
- Ratio mèche/corps >3 : **50.38%** de réussite

#### Étoile Filante (8,286 patterns détectés)
- ✓ **47.95%** de réussite immédiate (1 bougie)
- ✓ **74.20%** de réussite sur 2 bougies
- ✓ **48.67%** de réussite sur 3 bougies

**Impact du contexte :**
- Volume élevé : **48.71%** de réussite
- Près Support/Résistance : **47.95%** de réussite
- Ratio mèche/corps >3 : **48.42%** de réussite

### Comparaisons Importantes

#### NQ vs ES (Timeframe 5m)
| Pattern | NQ | ES | Différence |
|---------|----|----|------------|
| Marteau | 50.38% | 47.33% | +3.05% pour NQ |
| Étoile Filante | 47.95% | 45.14% | +2.81% pour NQ |

**Conclusion** : Le NQ montre une légère supériorité dans la fiabilité des patterns.

#### 5m vs 15m (NQ)
| Pattern | 5m | 15m | Différence |
|---------|-----|-----|------------|
| Marteau | 50.38% | 51.56% | +1.18% pour 15m |
| Étoile Filante | 47.95% | 48.33% | +0.38% pour 15m |

**Conclusion** : Les timeframes plus longs (15m) montrent une très légère amélioration de la fiabilité.

### Évolution Annuelle (NQ 5m)

#### Marteau
| Année | Détectés | Réussis | Taux |
|-------|----------|---------|------|
| 2018 | 792 | 387 | 48.9% |
| 2019 | 766 | 393 | 51.3% |
| 2020 | 691 | 372 | **53.8%** |
| 2021 | 767 | 377 | 49.2% |
| 2022 | 665 | 324 | 48.7% |
| 2023 | 714 | 346 | 48.5% |
| 2024 | 763 | 395 | 51.8% |
| 2025 | 676 | 345 | 51.0% |

#### Étoile Filante
| Année | Détectés | Réussis | Taux |
|-------|----------|---------|------|
| 2018 | 1239 | 587 | 47.4% |
| 2019 | 1160 | 526 | 45.3% |
| 2020 | 1001 | 500 | **50.0%** |
| 2021 | 1076 | 518 | 48.1% |
| 2022 | 974 | 480 | 49.3% |
| 2023 | 1019 | 480 | 47.1% |
| 2024 | 957 | 453 | 47.3% |
| 2025 | 860 | 429 | **49.9%** |

**Observation** : La performance des patterns reste relativement stable d'une année à l'autre, avec 2020 montrant les meilleurs résultats pour les deux patterns.

## Interprétation et Utilisation

### Points Importants

1. **Pas de Signal Miracle** : Les taux de réussite de ~50% indiquent que ces patterns seuls ne garantissent pas un retournement. Ils doivent être utilisés en complément d'autres analyses.

2. **Meilleure Performance sur 2-3 Bougies** : Le taux de réussite sur 2 bougies (75%+) montre que même si la bougie immédiate ne confirme pas, le mouvement se réalise souvent dans les bougies suivantes.

3. **Contexte Important** : Les facteurs comme le volume élevé ou la proximité de S/R n'améliorent que légèrement la performance, suggérant que ces patterns fonctionnent de manière similaire dans différents contextes.

4. **Cohérence Multi-Instruments** : Les résultats similaires entre NQ et ES renforcent la validité de l'analyse.

### Recommandations pour le Trading

- ✓ **Combiner avec d'autres indicateurs** : Ne pas se fier uniquement au pattern
- ✓ **Attendre la confirmation** : Observer les 2-3 bougies suivantes avant d'agir
- ✓ **Gestion du risque** : Toujours utiliser des stops appropriés
- ✓ **Préférer les timeframes plus longs** : Les patterns 15m sont légèrement plus fiables
- ✓ **Éviter de sur-trader** : ~5,000-8,000 patterns sur 7 ans = sélectivité importante

## Utilisation du Script

### Prérequis
```bash
pip install pandas numpy
```

### Exécution
```bash
python3 candlestick_reversal_backtest.py
```

### Sorties Générées
1. **Console** : Progression en temps réel de l'analyse
2. **backtest_results.txt** : Rapport détaillé formaté
3. **backtest_results.json** : Données structurées pour analyse approfondie

### Personnalisation

Les paramètres peuvent être ajustés dans la classe `CandlestickReversalBacktest` :

```python
# Paramètres des patterns
self.body_position_threshold = 0.3  # Position du corps (30%)
self.wick_to_body_ratio = 2.0       # Ratio mèche/corps minimum
self.small_wick_threshold = 0.1     # Seuil petite mèche (10%)

# Paramètres de tendance
self.ema_period = 9                 # Période EMA
self.volume_ma_period = 20          # Période MA volume
self.support_resistance_lookback = 20  # Lookback S/R

# Paramètres Smart Money Concepts (SMC)
self.swing_lookback = 5             # Bougies avant/après pour swing point
self.recent_swing_lookback = 20     # Recherche des swing points récents
self.sweep_tolerance = 0.0005       # Tolérance sweep (0.05%)
```

## Architecture du Code

Le script est organisé en une classe principale `CandlestickReversalBacktest` avec les méthodes suivantes :

- **`load_data()`** : Charge et combine les fichiers CSV
- **`calculate_indicators()`** : Calcule EMA, volume MA, S/R, etc.
- **`detect_hammer()`** : Détecte les patterns Marteau
- **`detect_shooting_star()`** : Détecte les patterns Étoile Filante
- **`detect_trend()`** : Identifie la tendance court terme
- **`analyze_reversal()`** : Analyse le succès du retournement
- **`calculate_statistics()`** : Calcule toutes les métriques
- **`generate_report()`** : Génère les fichiers de rapport

### 🆕 Nouvelles Méthodes SMC

- **`_detect_swing_high()`** : Détecte les Swing Highs (sommets locaux)
- **`_detect_swing_low()`** : Détecte les Swing Lows (creux locaux)
- **`_find_recent_swing_lows()`** : Trouve les Swing Lows des 20 dernières bougies
- **`_find_recent_swing_highs()`** : Trouve les Swing Highs des 20 dernières bougies
- **`_detect_liquidity_sweep()`** : Détecte si un pattern a sweepé un swing point
- **`_analyze_post_sweep_behavior()`** : Analyse le mouvement après un sweep
- **`_calculate_move_strength()`** : Calcule la force d'un mouvement directionnel
- **`_calculate_sweep_statistics()`** : Calcule les stats pour patterns avec/sans sweep
- **`_write_smc_section()`** : Génère la section SMC dans le rapport

### 🎯 Nouvelles Méthodes Risk-Reward

- **`_calculate_risk_reward_trade()`** : Simule un trade complet avec SL/TP pour un ratio RR donné
- **`_calculate_rr_statistics()`** : Calcule les statistiques RR pour tous les ratios testés
- **`_calculate_rr_group_statistics()`** : Calcule les stats RR pour un groupe de signaux (avec/sans sweep)
- **`_write_rr_section()`** : Génère la section Risk-Reward dans le rapport
- **`_write_rr_recommendations()`** : Génère les recommandations basées sur l'analyse RR

## Limitations et Améliorations Futures

### Limitations Actuelles
- Pas de prise en compte du contexte macro (événements économiques)
- Pas d'analyse intraday (sessions de trading)
- Pas de tests de robustesse statistique (p-values, etc.)
- Pas de visualisations graphiques

### Améliorations Possibles
1. Ajouter des graphiques de visualisation des patterns
2. Analyser l'impact des sessions de trading (Asie, Europe, US)
3. Tester d'autres périodes EMA pour la détection de tendance
4. Implémenter un système de scoring composite
5. ✅ ~~Ajouter des backtests de stratégies complètes avec entrée/sortie et calcul de P&L~~ (Implémenté avec analyse RR)
6. Tests statistiques de significativité
7. Ajouter trailing stop et breakeven dans l'analyse RR
8. Tester différents placements de SL (ATR-based, swing-based, etc.)

## Conclusion

Cette analyse exhaustive de 7+ années de données sur NQ et ES démontre que :

1. Les patterns de chandeliers japonais (Marteau et Étoile Filante) ont une **efficacité proche de 50%** pour prédire les retournements immédiats
2. La **confirmation sur 2-3 bougies** améliore significativement la fiabilité (75%+)
3. Ces patterns fonctionnent de manière **cohérente** entre instruments et timeframes
4. Ils doivent être utilisés comme **un élément parmi d'autres** dans une stratégie de trading complète

### 🆕 Conclusions Smart Money Concepts

L'analyse des **Liquidity Sweeps** révèle des insights importants :

1. **Rareté des Sweeps** : Seulement 7-8% des patterns impliquent un sweep réel de swing points
2. **Impact Modéré** : L'amélioration du taux de réussite est limitée (+3-5% au mieux)
3. **Asymétrie Directionnelle** : Les sweeps fonctionnent mieux sur les Shooting Stars (bearish) que sur les Hammers (bullish)
4. **Timing Optimal** : L'entrée agressive (à la clôture du pattern) performe mieux que l'attente de confirmation
5. **Concept Valide mais Subtil** : Les sweeps existent et ont un effet, mais ne sont pas un "saint graal" - ils doivent être combinés avec d'autres facteurs

### Recommandations Finales pour le Trading SMC

- ✓ **Privilégier les Shooting Stars avec sweep** : Meilleure performance (+4.97% sur 2 bougies)
- ✓ **Entrée agressive sur les sweeps** : Ne pas attendre la confirmation qui réduit les gains
- ✓ **Combiner avec d'autres facteurs** : Volume, S/R, timeframe pour maximiser les probabilités
- ⚠️ **Ne pas se fier uniquement aux sweeps** : Ils restent rares et l'amélioration est modeste
- ⚠️ **Être sélectif** : Tous les sweeps ne sont pas égaux - privilégier ceux avec fort volume et S/R

---

**Créé le** : 6 décembre 2025  
**Dernière mise à jour** : 6 décembre 2025 (Ajout analyse SMC + Risk-Reward)  
**Auteur** : Backtest Trading Analysis  
**Version** : 3.0 (avec Smart Money Concepts + Analyse Risk-Reward complète)

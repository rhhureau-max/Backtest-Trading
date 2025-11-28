# 📊 Rapport d'Analyse des FVG (Fair Value Gaps) - 8h30 NY

## 1. Introduction

### Qu'est-ce qu'un FVG (Fair Value Gap) ?

Un **FVG (Fair Value Gap)**, aussi appelé **Imbalance**, est un déséquilibre de prix créé par un mouvement violent du marché. Ce déséquilibre se caractérise par un "trou" dans la structure du prix où aucune transaction n'a eu lieu entre deux bougies non-adjacentes.

Le FVG est un concept clé du **Smart Money Concept (SMC)** et de l'**ICT (Inner Circle Trader)** methodology. Il représente une zone où le prix a été "inefficient" et où le marché a tendance à revenir pour "combler" ce gap.

### Méthodologie

Cette analyse recherche les FVG qui se forment autour de la bougie de **8h30 heure de New York** (15:30 UTC), moment crucial correspondant à l'ouverture officielle de la session de trading américaine. Cette heure est caractérisée par:
- L'arrivée de la liquidité institutionnelle américaine
- La publication de données économiques importantes
- Une volatilité accrue sur les marchés

### Stratégie de Trading

La stratégie testée est un **fade du FVG**:
- **FVG haussier** → On prend une position **SHORT** (on anticipe que le prix va redescendre)
- **FVG baissier** → On prend une position **LONG** (on anticipe que le prix va remonter)

---

## 2. Paramètres d'Analyse

| Paramètre | Valeur |
|-----------|--------|
| **Période d'analyse** | 2018 - 2025 (8 ans) |
| **Timeframe** | 5 minutes |
| **Horaire analysé** | 8h30 NY (15:30 UTC) |
| **Instrument** | NQ (Nasdaq 100 Futures) |
| **Source des données** | Fichiers CSV 5 minutes |

### Bougies utilisées pour la détection

| Bougie | Horaire UTC | Description |
|--------|-------------|-------------|
| **n-1** | 15:10:00 | Dernière bougie avant le gap CME |
| **n** | 15:30:00 | Bougie centrale (ouverture NY) |
| **n+1** | 15:35:00 | Bougie suivante |
| **n+2** | 15:40:00 | Bougie d'entrée en position |

> **Note**: Il existe un gap naturel dans les données entre 15:10 et 15:30 (pause CME).

---

## 3. Définition des FVG (Fair Value Gaps)

### ⚠️ Important: Utilisation des Mèches (High/Low)

Cette analyse utilise la **définition correcte des FVG** qui prend en compte les **mèches** des bougies (High et Low), et non pas seulement les corps (Open et Close).

### FVG Haussier (Bullish FVG) 📈

```
Condition: Low de la bougie n-1 (15:10) > High de la bougie n+1 (15:35)
```

Un FVG haussier se produit lorsqu'il y a un **gap vers le haut** entre:
- Le point le plus bas (Low/mèche basse) de la bougie précédente
- Le point le plus haut (High/mèche haute) de la bougie suivante

```
        ┌──┐ n-1
        │  │
    ────┴──┴──── Low n-1  ← Point de référence
    
        ▓▓▓▓▓▓▓▓ GAP (FVG Zone)
    
    ────┬──┬──── High n+1 ← Point de référence
        │  │
        └──┘ n+1
```

**Interprétation**: Le marché a monté tellement vite qu'il a laissé un "trou" non négocié.

### FVG Baissier (Bearish FVG) 📉

```
Condition: High de la bougie n-1 (15:10) < Low de la bougie n+1 (15:35)
```

Un FVG baissier se produit lorsqu'il y a un **gap vers le bas** entre:
- Le point le plus haut (High/mèche haute) de la bougie précédente
- Le point le plus bas (Low/mèche basse) de la bougie suivante

```
        ┌──┐ n-1
        │  │
    ────┴──┴──── High n-1 ← Point de référence
    
        ▓▓▓▓▓▓▓▓ GAP (FVG Zone)
    
    ────┬──┬──── Low n+1  ← Point de référence
        │  │
        └──┘ n+1
```

**Interprétation**: Le marché a chuté tellement vite qu'il a laissé un "trou" non négocié.

---

## 4. Statistiques par Année

### Tableau Récapitulatif

| Année | Jours de Trading | FVG Haussiers | FVG Baissiers | Total FVG | Taux de FVG |
|-------|------------------|---------------|---------------|-----------|-------------|
| 2018 | 248 | 28 | 34 | 62 | 25.0% |
| 2019 | 249 | 22 | 47 | 69 | 27.7% |
| 2020 | 251 | 19 | 38 | 57 | 22.7% |
| 2021 | 251 | 25 | 41 | 66 | 26.3% |
| 2022 | 250 | 41 | 51 | 92 | 36.8% |
| 2023 | 248 | 40 | 54 | 94 | 37.9% |
| 2024 | 249 | 47 | 61 | 108 | 43.4% |
| 2025 | 215 | 33 | 47 | 80 | 37.2% |

### Résumé Global (2018-2025)

| Métrique | Valeur |
|----------|--------|
| **Total jours de trading analysés** | 1961 |
| **Total FVG haussiers** | 255 |
| **Total FVG baissiers** | 373 |
| **Total FVG (tous types)** | 628 |
| **Taux global de FVG** | 32.0% |

### Observations

- Les **FVG baissiers sont plus fréquents** (373 vs 255), ce qui suggère que l'ouverture de New York génère plus souvent des gaps vers le bas
- Le taux de FVG a **augmenté au fil des années**: de ~25% en 2018 à ~40%+ en 2024
- En moyenne, **environ 1 jour sur 3** présente un FVG à 8h30 NY

---

## 5. Résultats du Backtesting

### Règles de Trading

| Paramètre | Règle |
|-----------|-------|
| **Entrée** | À l'ouverture de la bougie n+2 (15:40:00 UTC) |
| **Direction FVG haussier** | SHORT (vente) |
| **Direction FVG baissier** | LONG (achat) |
| **Stop Loss** | Basé sur le corps de la bougie n (15:30:00): `abs(Close - Open)` |
| **Take Profit** | Distance SL × Ratio Risk/Reward |
| **Fin de session** | 21:55:00 UTC |

### Paramètres testés

- **Stop Loss %**: 50%, 75%, 100% du corps de la bougie n
- **Risk/Reward**: 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5

### Tableau Complet des Résultats

| SL% | R:R | Wins | Losses | Non Résolus | Total | Winrate | Profit Factor | Espérance |
|-----|-----|------|--------|-------------|-------|---------|---------------|-----------|
| 50% | 1.0 | 407 | 210 | 11 | 617 | **66.0%** | **1.94** | **+0.32R** |
| 50% | 1.5 | 191 | 422 | 15 | 613 | 31.2% | 0.68 | -0.22R |
| 50% | 2.0 | 157 | 449 | 22 | 606 | 25.9% | 0.70 | -0.22R |
| 50% | 2.5 | 136 | 466 | 26 | 602 | 22.6% | 0.73 | -0.21R |
| 50% | 3.0 | 125 | 477 | 26 | 602 | 20.8% | 0.79 | -0.17R |
| 50% | 3.5 | 119 | 482 | 27 | 601 | 19.8% | 0.86 | -0.11R |
| 50% | 4.0 | 105 | 492 | 31 | 597 | 17.6% | 0.85 | -0.12R |
| 50% | 4.5 | 92 | 505 | 31 | 597 | 15.4% | 0.82 | -0.15R |
| 50% | 5.0 | 84 | 512 | 32 | 596 | 14.1% | 0.82 | -0.15R |
| 75% | 1.0 | 374 | 233 | 21 | 607 | 61.6% | 1.61 | +0.23R |
| 75% | 1.5 | 202 | 393 | 33 | 595 | 33.9% | 0.77 | -0.15R |
| 75% | 2.0 | 173 | 419 | 36 | 592 | 29.2% | 0.83 | -0.12R |
| 75% | 2.5 | 157 | 429 | 42 | 586 | 26.8% | 0.91 | -0.06R |
| 75% | 3.0 | 131 | 449 | 48 | 580 | 22.6% | 0.88 | -0.10R |
| 75% | 3.5 | 120 | 459 | 49 | 579 | 20.7% | 0.92 | -0.07R |
| 75% | 4.0 | 104 | 471 | 53 | 575 | 18.1% | 0.88 | -0.10R |
| 75% | 4.5 | 95 | 477 | 56 | 572 | 16.6% | 0.90 | -0.09R |
| 75% | 5.0 | 85 | 485 | 58 | 570 | 14.9% | 0.88 | -0.11R |
| 100% | 1.0 | 350 | 243 | 35 | 593 | 59.0% | 1.44 | +0.18R |
| 100% | 1.5 | 206 | 379 | 43 | 585 | 35.2% | 0.82 | -0.12R |
| 100% | 2.0 | 176 | 399 | 53 | 575 | 30.6% | 0.88 | -0.08R |
| 100% | 2.5 | 140 | 430 | 58 | 570 | 24.6% | 0.81 | -0.14R |
| 100% | 3.0 | 119 | 446 | 63 | 565 | 21.1% | 0.80 | -0.16R |
| 100% | 3.5 | 103 | 458 | 67 | 561 | 18.4% | 0.79 | -0.17R |
| 100% | 4.0 | 90 | 466 | 72 | 556 | 16.2% | 0.77 | -0.19R |
| 100% | 4.5 | 78 | 474 | 76 | 552 | 14.1% | 0.74 | -0.22R |
| 100% | 5.0 | 70 | 477 | 81 | 547 | 12.8% | 0.73 | -0.23R |

### 🏆 Meilleures Configurations

| Métrique | Valeur | Configuration |
|----------|--------|---------------|
| **Meilleur Winrate** | 66.0% | SL = 50%, R:R = 1 |
| **Meilleur Profit Factor** | 1.94 | SL = 50%, R:R = 1 |
| **Meilleure Espérance** | +0.32R | SL = 50%, R:R = 1 |

### Analyse par Stop Loss %

#### SL = 50% du corps

| R:R | Winrate | Profit Factor | Espérance |
|-----|---------|---------------|-----------|
| 1.0 | 66.0% | 1.94 | +0.32R |
| 1.5 | 31.2% | 0.68 | -0.22R |
| 2.0 | 25.9% | 0.70 | -0.22R |
| 2.5 | 22.6% | 0.73 | -0.21R |
| 3.0 | 20.8% | 0.79 | -0.17R |

#### SL = 75% du corps

| R:R | Winrate | Profit Factor | Espérance |
|-----|---------|---------------|-----------|
| 1.0 | 61.6% | 1.61 | +0.23R |
| 1.5 | 33.9% | 0.77 | -0.15R |
| 2.0 | 29.2% | 0.83 | -0.12R |
| 2.5 | 26.8% | 0.91 | -0.06R |
| 3.0 | 22.6% | 0.88 | -0.10R |

#### SL = 100% du corps

| R:R | Winrate | Profit Factor | Espérance |
|-----|---------|---------------|-----------|
| 1.0 | 59.0% | 1.44 | +0.18R |
| 1.5 | 35.2% | 0.82 | -0.12R |
| 2.0 | 30.6% | 0.88 | -0.08R |
| 2.5 | 24.6% | 0.81 | -0.14R |
| 3.0 | 21.1% | 0.80 | -0.16R |

---

## 6. Les 20 Derniers FVG (Ordre Chronologique)

Les FVG les plus récents détectés dans les données:

| # | Date | Type | Taille du Gap | Valeur N-1 | Valeur N+1 |
|---|------|------|---------------|------------|------------|
| 1 | 07/11/2025 | 📉 Bearish | 11.25 pts | 25201.50 (High) | 25212.75 (Low) |
| 2 | 04/11/2025 | 📈 Bullish | 18.50 pts | 25554.75 (Low) | 25536.25 (High) |
| 3 | 30/10/2025 | 📉 Bearish | 23.00 pts | 26006.00 (High) | 26029.00 (Low) |
| 4 | 28/10/2025 | 📉 Bearish | 7.25 pts | 26161.25 (High) | 26168.50 (Low) |
| 5 | 27/10/2025 | 📉 Bearish | 21.50 pts | 25975.50 (High) | 25997.00 (Low) |
| 6 | 24/10/2025 | 📉 Bearish | 4.75 pts | 25516.00 (High) | 25520.75 (Low) |
| 7 | 23/10/2025 | 📉 Bearish | 9.25 pts | 25273.50 (High) | 25282.75 (Low) |
| 8 | 22/10/2025 | 📈 Bullish | 5.50 pts | 25049.25 (Low) | 25043.75 (High) |
| 9 | 21/10/2025 | 📉 Bearish | 11.75 pts | 25246.50 (High) | 25258.25 (Low) |
| 10 | 17/10/2025 | 📉 Bearish | 11.50 pts | 25014.25 (High) | 25025.75 (Low) |
| 11 | 15/10/2025 | 📈 Bullish | 1.25 pts | 24935.25 (Low) | 24934.00 (High) |
| 12 | 13/10/2025 | 📈 Bullish | 4.25 pts | 24913.75 (Low) | 24909.50 (High) |
| 13 | 09/10/2025 | 📈 Bullish | 4.00 pts | 25283.25 (Low) | 25279.25 (High) |
| 14 | 08/10/2025 | 📉 Bearish | 22.00 pts | 25334.50 (High) | 25356.50 (Low) |
| 15 | 02/10/2025 | 📈 Bullish | 8.50 pts | 25117.75 (Low) | 25109.25 (High) |
| 16 | 01/10/2025 | 📉 Bearish | 8.00 pts | 24998.50 (High) | 25006.50 (Low) |
| 17 | 30/09/2025 | 📈 Bullish | 8.50 pts | 24856.50 (Low) | 24848.00 (High) |
| 18 | 25/09/2025 | 📉 Bearish | 7.50 pts | 24626.50 (High) | 24634.00 (Low) |
| 19 | 22/09/2025 | 📉 Bearish | 2.75 pts | 24987.75 (High) | 24990.50 (Low) |
| 20 | 18/09/2025 | 📉 Bearish | 3.00 pts | 24711.00 (High) | 24714.00 (Low) |

**Légende:**
- 📈 **Bullish**: N-1 Value = Low (mèche basse), N+1 Value = High (mèche haute)
- 📉 **Bearish**: N-1 Value = High (mèche haute), N+1 Value = Low (mèche basse)

---

## 7. Conclusions et Observations

### Résumé des Findings

1. **Fréquence des FVG**
   - Les FVG se produisent sur environ **32% des jours de trading** à l'heure d'ouverture de New York
   - La fréquence a **augmenté ces dernières années** (22.7% en 2020 vs 43.4% en 2024)
   - Les **FVG baissiers sont 46% plus fréquents** que les FVG haussiers (373 vs 255)

2. **Performance du Backtesting**
   - **Seules les configurations R:R = 1 sont rentables** sur l'ensemble de la période
   - La meilleure configuration est **SL = 50%, R:R = 1** avec un Profit Factor de 1.94
   - Les ratios R:R supérieurs à 1 **ne sont pas rentables** avec cette stratégie

3. **Recommandations**
   - Si vous tradez les FVG à 8h30 NY, privilégiez un **R:R de 1:1** avec un SL serré (50% du corps)
   - Les R:R élevés (>1.5) ne fonctionnent pas car le **fade est généralement de courte durée**
   - Le marché a tendance à **combler rapidement les FVG** puis à reprendre sa direction initiale

### Limites de l'Analyse

- Cette analyse ne prend pas en compte les **spreads et commissions**
- Les résultats peuvent varier selon les **conditions de marché**
- La période analysée (2018-2025) peut ne pas être représentative des conditions futures
- Le **slippage** à l'entrée n'est pas modélisé

### Fichiers de Résultats Générés

| Fichier | Description |
|---------|-------------|
| `fvg_analysis_results.txt` | Rapport détaillé en texte |
| `fvg_analysis_results.csv` | Liste complète des FVG détectés |
| `fvg_backtest_results.txt` | Résultats du backtesting en texte |
| `fvg_backtest_results.csv` | Résultats du backtesting en CSV |

---

*Rapport basé sur les données analysées par `fvg_analysis_830.py`*

*Dernière mise à jour: Novembre 2025*

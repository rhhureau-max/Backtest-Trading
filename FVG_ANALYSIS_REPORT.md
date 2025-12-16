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

La stratégie testée est une **continuation du FVG**:
- **FVG haussier** → On prend une position **LONG** (on anticipe que le prix va continuer vers le haut)
- **FVG baissier** → On prend une position **SHORT** (on anticipe que le prix va continuer vers le bas)

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

| Bougie | Horaire UTC | Horaire NY | Description |
|--------|-------------|------------|-------------|
| **n-1** | 15:25:00 | 8:25 | Bougie précédente |
| **n** | 15:30:00 | 8:30 | Bougie centrale (ouverture NY) |
| **n+1** | 15:35:00 | 8:35 | Bougie suivante |
| **n+2** | 15:40:00 | 8:40 | Bougie d'entrée en position |

---

## 3. Définition des FVG (Fair Value Gaps)

### ⚠️ Important: Utilisation des Mèches (High/Low)

Cette analyse utilise la **définition correcte des FVG** qui prend en compte les **mèches** des bougies (High et Low), et non pas seulement les corps (Open et Close).

### FVG Haussier (Bullish FVG) 📈

```
Condition: Low de la bougie n-1 (15:25) > High de la bougie n+1 (15:35)
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
Condition: High de la bougie n-1 (15:25) < Low de la bougie n+1 (15:35)
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
| 2018 | 248 | 0 | 0 | 0 | 0.0% |
| 2019 | 249 | 0 | 0 | 0 | 0.0% |
| 2020 | 251 | 0 | 0 | 0 | 0.0% |
| 2021 | 251 | 16 | 16 | 32 | 12.7% |
| 2022 | 250 | 15 | 34 | 49 | 19.6% |
| 2023 | 248 | 23 | 27 | 50 | 20.2% |
| 2024 | 249 | 27 | 20 | 47 | 18.9% |
| 2025 | 215 | 20 | 25 | 45 | 20.9% |

### Résumé Global (2018-2025)

| Métrique | Valeur |
|----------|--------|
| **Total jours de trading analysés** | 1961 |
| **Total FVG haussiers** | 101 |
| **Total FVG baissiers** | 122 |
| **Total FVG (tous types)** | 223 |
| **Taux global de FVG** | 11.4% |

### Observations

- Les **FVG baissiers sont légèrement plus fréquents** (122 vs 101)
- Les FVG sont **beaucoup plus rares** avec la bougie n-1 à 15:25:00 (11.4% vs ~32% avec 15:10:00)
- Les données de 2018 à 2020 ne contiennent pas de bougie à 15:25:00 (format de données différent ou horaires de marché), d'où l'absence de FVG pour ces années
- À partir de 2021, les FVG se produisent sur environ **1 jour sur 5**

---

## 5. Résultats du Backtesting

### Règles de Trading

| Paramètre | Règle |
|-----------|-------|
| **Entrée** | À l'ouverture de la bougie n+2 (15:40:00 UTC) |
| **Direction FVG haussier** | LONG (achat) - continuation vers le haut |
| **Direction FVG baissier** | SHORT (vente) - continuation vers le bas |
| **Stop Loss** | Basé sur le corps de la bougie n (15:30:00): `abs(Close - Open)` |
| **Take Profit** | Distance SL × Ratio Risk/Reward |
| **Fin de session** | 21:55:00 UTC |

### Paramètres testés

- **Stop Loss %**: 50%, 75%, 100% du corps de la bougie n
- **Risk/Reward**: 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5

### Tableau Complet des Résultats

| SL% | R:R | Wins | Losses | Non Résolus | Total | Winrate | Profit Factor | Espérance |
|-----|-----|------|--------|-------------|-------|---------|---------------|-----------|
| 50% | 1.0 | 120 | 102 | 1 | 222 | **54.1%** | **1.18** | **+0.08R** |
| 50% | 1.5 | 69 | 150 | 4 | 219 | 31.5% | 0.69 | -0.21R |
| 50% | 2.0 | 59 | 157 | 7 | 216 | 27.3% | 0.75 | -0.18R |
| 50% | 2.5 | 49 | 165 | 9 | 214 | 22.9% | 0.74 | -0.20R |
| 50% | 3.0 | 45 | 167 | 11 | 212 | 21.2% | 0.81 | -0.15R |
| 50% | 3.5 | 40 | 172 | 11 | 212 | 18.9% | 0.81 | -0.15R |
| 50% | 4.0 | 34 | 176 | 13 | 210 | 16.2% | 0.77 | -0.19R |
| 50% | 4.5 | 29 | 180 | 14 | 209 | 13.9% | 0.72 | -0.24R |
| 50% | 5.0 | 26 | 183 | 14 | 209 | 12.4% | 0.71 | -0.25R |
| 75% | 1.0 | 104 | 115 | 4 | 219 | 47.5% | 0.90 | -0.05R |
| 75% | 1.5 | 71 | 143 | 9 | 214 | 33.2% | 0.74 | -0.17R |
| 75% | 2.0 | 58 | 151 | 14 | 209 | 27.8% | 0.77 | -0.17R |
| 75% | 2.5 | 48 | 159 | 16 | 207 | 23.2% | 0.75 | -0.19R |
| 75% | 3.0 | 39 | 166 | 18 | 205 | 19.0% | 0.70 | -0.24R |
| 75% | 3.5 | 34 | 171 | 18 | 205 | 16.6% | 0.70 | -0.25R |
| 75% | 4.0 | 29 | 176 | 18 | 205 | 14.1% | 0.66 | -0.29R |
| 75% | 4.5 | 27 | 177 | 19 | 204 | 13.2% | 0.69 | -0.27R |
| 75% | 5.0 | 21 | 182 | 20 | 203 | 10.3% | 0.58 | -0.38R |
| 100% | 1.0 | 98 | 114 | 11 | 212 | 46.2% | 0.86 | -0.08R |
| 100% | 1.5 | 71 | 135 | 17 | 206 | 34.5% | 0.79 | -0.14R |
| 100% | 2.0 | 56 | 145 | 22 | 201 | 27.9% | 0.77 | -0.16R |
| 100% | 2.5 | 45 | 154 | 24 | 199 | 22.6% | 0.73 | -0.21R |
| 100% | 3.0 | 38 | 160 | 25 | 198 | 19.2% | 0.71 | -0.23R |
| 100% | 3.5 | 35 | 162 | 26 | 197 | 17.8% | 0.76 | -0.20R |
| 100% | 4.0 | 25 | 170 | 28 | 195 | 12.8% | 0.59 | -0.36R |
| 100% | 4.5 | 23 | 172 | 28 | 195 | 11.8% | 0.60 | -0.35R |
| 100% | 5.0 | 22 | 172 | 29 | 194 | 11.3% | 0.64 | -0.32R |

### 🏆 Meilleures Configurations

| Métrique | Valeur | Configuration |
|----------|--------|---------------|
| **Meilleur Winrate** | 54.1% | SL = 50%, R:R = 1 |
| **Meilleur Profit Factor** | 1.18 | SL = 50%, R:R = 1 |
| **Meilleure Espérance** | +0.08R | SL = 50%, R:R = 1 |

### Analyse par Stop Loss %

#### SL = 50% du corps

| R:R | Winrate | Profit Factor | Espérance |
|-----|---------|---------------|-----------|
| 1.0 | 54.1% | 1.18 | +0.08R |
| 1.5 | 31.5% | 0.69 | -0.21R |
| 2.0 | 27.3% | 0.75 | -0.18R |
| 2.5 | 22.9% | 0.74 | -0.20R |
| 3.0 | 21.2% | 0.81 | -0.15R |

#### SL = 75% du corps

| R:R | Winrate | Profit Factor | Espérance |
|-----|---------|---------------|-----------|
| 1.0 | 47.5% | 0.90 | -0.05R |
| 1.5 | 33.2% | 0.74 | -0.17R |
| 2.0 | 27.8% | 0.77 | -0.17R |
| 2.5 | 23.2% | 0.75 | -0.19R |
| 3.0 | 19.0% | 0.70 | -0.24R |

#### SL = 100% du corps

| R:R | Winrate | Profit Factor | Espérance |
|-----|---------|---------------|-----------|
| 1.0 | 46.2% | 0.86 | -0.08R |
| 1.5 | 34.5% | 0.79 | -0.14R |
| 2.0 | 27.9% | 0.77 | -0.16R |
| 2.5 | 22.6% | 0.73 | -0.21R |
| 3.0 | 19.2% | 0.71 | -0.23R |

---

## 6. Les 20 Derniers FVG (Ordre Chronologique)

Les FVG les plus récents détectés dans les données:

| # | Date | Type | Taille du Gap | Valeur N-1 | Valeur N+1 |
|---|------|------|---------------|------------|------------|
| 1 | 07/11/2025 | 📉 Bearish | 4.00 pts | 25208.75 (High) | 25212.75 (Low) |
| 2 | 28/10/2025 | 📉 Bearish | 1.00 pts | 26167.50 (High) | 26168.50 (Low) |
| 3 | 23/10/2025 | 📉 Bearish | 7.50 pts | 25275.25 (High) | 25282.75 (Low) |
| 4 | 14/10/2025 | 📉 Bearish | 3.50 pts | 24721.50 (High) | 24725.00 (Low) |
| 5 | 13/10/2025 | 📈 Bullish | 2.25 pts | 24911.75 (Low) | 24909.50 (High) |
| 6 | 02/10/2025 | 📈 Bullish | 3.00 pts | 25112.25 (Low) | 25109.25 (High) |
| 7 | 01/10/2025 | 📉 Bearish | 5.00 pts | 25001.50 (High) | 25006.50 (Low) |
| 8 | 30/09/2025 | 📈 Bullish | 4.75 pts | 24852.75 (Low) | 24848.00 (High) |
| 9 | 29/09/2025 | 📈 Bullish | 1.75 pts | 24828.00 (Low) | 24826.25 (High) |
| 10 | 25/09/2025 | 📉 Bearish | 8.00 pts | 24626.00 (High) | 24634.00 (Low) |
| 11 | 18/09/2025 | 📉 Bearish | 2.50 pts | 24711.50 (High) | 24714.00 (Low) |
| 12 | 04/08/2025 | 📉 Bearish | 3.03 pts | 23569.14 (High) | 23572.17 (Low) |
| 13 | 31/07/2025 | 📉 Bearish | 7.83 pts | 23555.76 (High) | 23563.58 (Low) |
| 14 | 25/07/2025 | 📉 Bearish | 3.53 pts | 23669.62 (High) | 23673.16 (Low) |
| 15 | 23/07/2025 | 📉 Bearish | 8.08 pts | 23604.99 (High) | 23613.07 (Low) |
| 16 | 18/07/2025 | 📉 Bearish | 2.02 pts | 23452.74 (High) | 23454.76 (Low) |
| 17 | 10/07/2025 | 📉 Bearish | 7.83 pts | 23236.63 (High) | 23244.45 (Low) |
| 18 | 08/07/2025 | 📈 Bullish | 1.51 pts | 23131.34 (Low) | 23129.83 (High) |
| 19 | 07/07/2025 | 📈 Bullish | 1.51 pts | 23084.38 (Low) | 23082.87 (High) |
| 20 | 02/07/2025 | 📉 Bearish | 1.01 pts | 23062.16 (High) | 23063.17 (Low) |

**Légende:**
- 📈 **Bullish**: N-1 Value = Low (mèche basse), N+1 Value = High (mèche haute)
- 📉 **Bearish**: N-1 Value = High (mèche haute), N+1 Value = Low (mèche basse)

---

## 7. Conclusions et Observations

### Résumé des Findings

1. **Fréquence des FVG**
   - Les FVG se produisent sur environ **11.4% des jours de trading** à l'heure d'ouverture de New York avec la bougie n-1 à 15:25:00
   - Les données de 2018 à 2020 ne contiennent pas de bougie à 15:25:00, d'où l'absence de FVG pour ces années
   - Les **FVG baissiers sont légèrement plus fréquents** (122 vs 101)

2. **Performance du Backtesting (Stratégie de Continuation)**
   - **La configuration R:R = 1 avec SL = 50% est la seule rentable** avec un Profit Factor de 1.18
   - La meilleure configuration est **SL = 50%, R:R = 1** avec un winrate de 54.1% et une espérance de +0.08R
   - Toutes les autres configurations montrent des résultats négatifs (PF < 1)

3. **Recommandations**
   - La stratégie de continuation FVG à 8h30 NY montre des résultats mitigés
   - Seule la configuration **SL = 50%, R:R = 1** est marginalement profitable
   - Le marché a tendance à **retracer après les FVG** plutôt qu'à continuer dans la direction initiale

### Limites de l'Analyse

- Cette analyse ne prend pas en compte les **spreads et commissions**
- Les résultats peuvent varier selon les **conditions de marché**
- La période analysée (2018-2025) peut ne pas être représentative des conditions futures
- Le **slippage** à l'entrée n'est pas modélisé
- Les données de 2018-2020 ne contiennent pas de bougie à 15:25:00 (format de données différent), ce qui limite l'analyse historique à 2021-2025

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

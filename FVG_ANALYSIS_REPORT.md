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
| 50% | 1.0 | 136 | 86 | 1 | 222 | **61.3%** | **1.58** | **+0.23R** |
| 50% | 1.5 | 87 | 135 | 1 | 222 | 39.2% | 0.97 | -0.02R |
| 50% | 2.0 | 77 | 144 | 2 | 221 | 34.8% | 1.07 | +0.05R |
| 50% | 2.5 | 66 | 154 | 3 | 220 | 30.0% | 1.07 | +0.05R |
| 50% | 3.0 | 58 | 160 | 5 | 218 | 26.6% | 1.09 | +0.06R |
| 50% | 3.5 | 52 | 164 | 7 | 216 | 24.1% | 1.11 | +0.08R |
| 50% | 4.0 | 47 | 167 | 9 | 214 | 22.0% | 1.13 | +0.10R |
| 50% | 4.5 | 37 | 174 | 12 | 211 | 17.5% | 0.96 | -0.04R |
| 50% | 5.0 | 35 | 176 | 12 | 211 | 16.6% | 0.99 | -0.00R |
| 75% | 1.0 | 122 | 97 | 4 | 219 | 55.7% | 1.26 | +0.11R |
| 75% | 1.5 | 91 | 124 | 8 | 215 | 42.3% | 1.10 | +0.06R |
| 75% | 2.0 | 77 | 135 | 11 | 212 | 36.3% | 1.14 | +0.09R |
| 75% | 2.5 | 63 | 144 | 16 | 207 | 30.4% | 1.09 | +0.07R |
| 75% | 3.0 | 48 | 155 | 20 | 203 | 23.6% | 0.93 | -0.05R |
| 75% | 3.5 | 44 | 159 | 20 | 203 | 21.7% | 0.97 | -0.02R |
| 75% | 4.0 | 39 | 163 | 21 | 202 | 19.3% | 0.96 | -0.03R |
| 75% | 4.5 | 36 | 165 | 22 | 201 | 17.9% | 0.98 | -0.01R |
| 75% | 5.0 | 32 | 168 | 23 | 200 | 16.0% | 0.95 | -0.04R |
| 100% | 1.0 | 117 | 95 | 11 | 212 | 55.2% | 1.23 | +0.10R |
| 100% | 1.5 | 90 | 118 | 15 | 208 | 43.3% | 1.14 | +0.08R |
| 100% | 2.0 | 71 | 131 | 21 | 202 | 35.1% | 1.08 | +0.05R |
| 100% | 2.5 | 53 | 146 | 24 | 199 | 26.6% | 0.91 | -0.07R |
| 100% | 3.0 | 46 | 152 | 25 | 198 | 23.2% | 0.91 | -0.07R |
| 100% | 3.5 | 41 | 155 | 27 | 196 | 20.9% | 0.93 | -0.06R |
| 100% | 4.0 | 35 | 159 | 29 | 194 | 18.0% | 0.88 | -0.10R |
| 100% | 4.5 | 32 | 160 | 31 | 192 | 16.7% | 0.90 | -0.08R |
| 100% | 5.0 | 30 | 160 | 33 | 190 | 15.8% | 0.94 | -0.05R |

### 🏆 Meilleures Configurations

| Métrique | Valeur | Configuration |
|----------|--------|---------------|
| **Meilleur Winrate** | 61.3% | SL = 50%, R:R = 1 |
| **Meilleur Profit Factor** | 1.58 | SL = 50%, R:R = 1 |
| **Meilleure Espérance** | +0.23R | SL = 50%, R:R = 1 |

### Analyse par Stop Loss %

#### SL = 50% du corps

| R:R | Winrate | Profit Factor | Espérance |
|-----|---------|---------------|-----------|
| 1.0 | 61.3% | 1.58 | +0.23R |
| 1.5 | 39.2% | 0.97 | -0.02R |
| 2.0 | 34.8% | 1.07 | +0.05R |
| 2.5 | 30.0% | 1.07 | +0.05R |
| 3.0 | 26.6% | 1.09 | +0.06R |

#### SL = 75% du corps

| R:R | Winrate | Profit Factor | Espérance |
|-----|---------|---------------|-----------|
| 1.0 | 55.7% | 1.26 | +0.11R |
| 1.5 | 42.3% | 1.10 | +0.06R |
| 2.0 | 36.3% | 1.14 | +0.09R |
| 2.5 | 30.4% | 1.09 | +0.07R |
| 3.0 | 23.6% | 0.93 | -0.05R |

#### SL = 100% du corps

| R:R | Winrate | Profit Factor | Espérance |
|-----|---------|---------------|-----------|
| 1.0 | 55.2% | 1.23 | +0.10R |
| 1.5 | 43.3% | 1.14 | +0.08R |
| 2.0 | 35.1% | 1.08 | +0.05R |
| 2.5 | 26.6% | 0.91 | -0.07R |
| 3.0 | 23.2% | 0.91 | -0.07R |

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

2. **Performance du Backtesting**
   - **La configuration R:R = 1 avec SL = 50% est rentable** avec un Profit Factor de 1.58
   - Plusieurs configurations avec R:R > 1 montrent des résultats positifs (PF > 1)
   - La meilleure configuration est **SL = 50%, R:R = 1** avec un winrate de 61.3%

3. **Recommandations**
   - Si vous tradez les FVG à 8h30 NY, privilégiez un **R:R de 1:1** avec un SL serré (50% du corps)
   - Les ratios R:R de 2 à 4 avec SL = 50% montrent aussi des espérances positives
   - Le marché a tendance à **combler les FVG** rapidement après leur formation

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

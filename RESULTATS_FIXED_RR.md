# Résultats - Stratégie Judas Swing + FVG (SL Tokyo +/- 0.5pts, TP R:R fixe)

**Date de génération:** 24/12/2025 à 11:02:53

---

## 📊 Configuration de la Stratégie

### Sessions de Trading
- **Asia Session (Tokyo):** 18:00 - 23:00 (J-1, heure Chicago)
- **London Killzone:** 01:00 - 04:00 (J, heure Chicago)

### Logique d'Entrée

**LONG Setup:**
1. Prix passe sous Asia_Low
2. Formation d'un FVG Baissier
3. Clôture de bougie > Haut du FVG

**SHORT Setup:**
1. Prix passe au-dessus d'Asia_High
2. Formation d'un FVG Haussier
3. Clôture de bougie < Bas du FVG

### Gestion du Risque - R:R FIXE
- **Stop Loss:** Placé 0.5 points au-delà des niveaux Tokyo/Asia
  - LONG: SL = Asia_Low - 0.5 points
  - SHORT: SL = Asia_High + 0.5 points
- **Take Profit:** Calculé selon le ratio R:R fixe
  - Scénario A (1:1): TP = Entry ± (SL_Distance × 1.0)
  - Scénario B (1:1.5): TP = Entry ± (SL_Distance × 1.5)
  - Scénario C (1:2): TP = Entry ± (SL_Distance × 2.0)
- **Time Stop:** 12:00 Chicago si ni SL ni TP touché

---

## 📈 Résumé Global par Scénario R:R

### Scénario A (1:1)

| Année | Total Trades | Win Rate (%) | Net Profit (pts) | Profit Factor | Max Drawdown (pts) |
|-------|--------------|--------------|------------------|---------------|---------------------|
| 2018 | 178 | 71.91% | 1080.08 | 4.00 | 108.02 |
| 2019 | 178 | 66.29% | 683.44 | 2.70 | 40.19 |
| 2020 | 179 | 70.39% | 2310.02 | 3.26 | 145.99 |
| 2021 | 203 | 71.92% | 2764.71 | 4.53 | 143.20 |
| 2022 | 217 | 66.36% | 2841.05 | 2.79 | 158.79 |
| 2023 | 215 | 71.63% | 2205.17 | 4.33 | 71.25 |
| 2024 | 209 | 76.08% | 2989.39 | 5.71 | 67.55 |
| 2025 | 178 | 71.91% | 2743.38 | 3.96 | 157.31 |
| **TOTAL** | **1557** | **70.84%** | **17617.24** | **3.76** | **158.79** |

### Scénario B (1:1.5)

| Année | Total Trades | Win Rate (%) | Net Profit (pts) | Profit Factor | Max Drawdown (pts) |
|-------|--------------|--------------|------------------|---------------|---------------------|
| 2018 | 178 | 67.42% | 1049.55 | 3.38 | 108.02 |
| 2019 | 178 | 61.24% | 568.36 | 2.08 | 95.28 |
| 2020 | 179 | 66.48% | 2311.16 | 2.97 | 145.99 |
| 2021 | 203 | 66.01% | 2752.67 | 3.83 | 143.20 |
| 2022 | 217 | 58.06% | 2204.98 | 2.04 | 158.79 |
| 2023 | 215 | 65.58% | 2090.21 | 3.39 | 100.14 |
| 2024 | 209 | 70.33% | 2709.53 | 3.94 | 96.87 |
| 2025 | 178 | 66.85% | 2845.79 | 3.68 | 157.31 |
| **TOTAL** | **1557** | **65.06%** | **16532.25** | **3.04** | **158.79** |

### Scénario C (1:2)

| Année | Total Trades | Win Rate (%) | Net Profit (pts) | Profit Factor | Max Drawdown (pts) |
|-------|--------------|--------------|------------------|---------------|---------------------|
| 2018 | 178 | 64.61% | 1053.82 | 3.19 | 108.02 |
| 2019 | 178 | 58.43% | 625.76 | 2.14 | 95.28 |
| 2020 | 179 | 62.01% | 2074.00 | 2.54 | 154.47 |
| 2021 | 203 | 63.55% | 2749.97 | 3.51 | 187.93 |
| 2022 | 217 | 54.84% | 1977.93 | 1.84 | 188.84 |
| 2023 | 215 | 63.26% | 2226.03 | 3.39 | 100.14 |
| 2024 | 209 | 68.90% | 2928.75 | 4.07 | 96.87 |
| 2025 | 178 | 64.61% | 3021.12 | 3.70 | 157.31 |
| **TOTAL** | **1557** | **62.49%** | **16657.39** | **2.89** | **188.84** |

---

## 📅 Résultats Détaillés par Année

### Année 2018

| Scénario | Total Trades | Win Rate (%) | Net Profit (pts) | Profit Factor | Max Drawdown (pts) |
|----------|--------------|--------------|------------------|---------------|---------------------|
| Scénario A (1:1) | 178 | 71.91% | 1080.08 | 4.00 | 108.02 |
| Scénario B (1:1.5) | 178 | 67.42% | 1049.55 | 3.38 | 108.02 |
| Scénario C (1:2) | 178 | 64.61% | 1053.82 | 3.19 | 108.02 |

### Année 2019

| Scénario | Total Trades | Win Rate (%) | Net Profit (pts) | Profit Factor | Max Drawdown (pts) |
|----------|--------------|--------------|------------------|---------------|---------------------|
| Scénario A (1:1) | 178 | 66.29% | 683.44 | 2.70 | 40.19 |
| Scénario B (1:1.5) | 178 | 61.24% | 568.36 | 2.08 | 95.28 |
| Scénario C (1:2) | 178 | 58.43% | 625.76 | 2.14 | 95.28 |

### Année 2020

| Scénario | Total Trades | Win Rate (%) | Net Profit (pts) | Profit Factor | Max Drawdown (pts) |
|----------|--------------|--------------|------------------|---------------|---------------------|
| Scénario A (1:1) | 179 | 70.39% | 2310.02 | 3.26 | 145.99 |
| Scénario B (1:1.5) | 179 | 66.48% | 2311.16 | 2.97 | 145.99 |
| Scénario C (1:2) | 179 | 62.01% | 2074.00 | 2.54 | 154.47 |

### Année 2021

| Scénario | Total Trades | Win Rate (%) | Net Profit (pts) | Profit Factor | Max Drawdown (pts) |
|----------|--------------|--------------|------------------|---------------|---------------------|
| Scénario A (1:1) | 203 | 71.92% | 2764.71 | 4.53 | 143.20 |
| Scénario B (1:1.5) | 203 | 66.01% | 2752.67 | 3.83 | 143.20 |
| Scénario C (1:2) | 203 | 63.55% | 2749.97 | 3.51 | 187.93 |

### Année 2022

| Scénario | Total Trades | Win Rate (%) | Net Profit (pts) | Profit Factor | Max Drawdown (pts) |
|----------|--------------|--------------|------------------|---------------|---------------------|
| Scénario A (1:1) | 217 | 66.36% | 2841.05 | 2.79 | 158.79 |
| Scénario B (1:1.5) | 217 | 58.06% | 2204.98 | 2.04 | 158.79 |
| Scénario C (1:2) | 217 | 54.84% | 1977.93 | 1.84 | 188.84 |

### Année 2023

| Scénario | Total Trades | Win Rate (%) | Net Profit (pts) | Profit Factor | Max Drawdown (pts) |
|----------|--------------|--------------|------------------|---------------|---------------------|
| Scénario A (1:1) | 215 | 71.63% | 2205.17 | 4.33 | 71.25 |
| Scénario B (1:1.5) | 215 | 65.58% | 2090.21 | 3.39 | 100.14 |
| Scénario C (1:2) | 215 | 63.26% | 2226.03 | 3.39 | 100.14 |

### Année 2024

| Scénario | Total Trades | Win Rate (%) | Net Profit (pts) | Profit Factor | Max Drawdown (pts) |
|----------|--------------|--------------|------------------|---------------|---------------------|
| Scénario A (1:1) | 209 | 76.08% | 2989.39 | 5.71 | 67.55 |
| Scénario B (1:1.5) | 209 | 70.33% | 2709.53 | 3.94 | 96.87 |
| Scénario C (1:2) | 209 | 68.90% | 2928.75 | 4.07 | 96.87 |

### Année 2025

| Scénario | Total Trades | Win Rate (%) | Net Profit (pts) | Profit Factor | Max Drawdown (pts) |
|----------|--------------|--------------|------------------|---------------|---------------------|
| Scénario A (1:1) | 178 | 71.91% | 2743.38 | 3.96 | 157.31 |
| Scénario B (1:1.5) | 178 | 66.85% | 2845.79 | 3.68 | 157.31 |
| Scénario C (1:2) | 178 | 64.61% | 3021.12 | 3.70 | 157.31 |

---

## 💡 Analyse et Conclusions

### Performance Globale

- **Meilleur Scénario:** Scénario A (1:1) avec un profit net total de 17617.24 points

### Observations Clés

1. **SL Buffer:** Le buffer de 0.5 points permet d'éviter les stop loss prématurés sur les niveaux exacts
2. **R:R Adaptatif au Setup:** Chaque trade a un R:R fixe basé sur la distance du SL calculée
3. **Win Rate vs Profit:** Un R:R plus élevé diminue le win rate mais peut augmenter la rentabilité
4. **Simplicité:** Approche systématique et reproductible sans zones subjectives

### Recommandations

1. **Choix du R:R:** Adapter selon la volatilité du marché et les objectifs
2. **Gestion de Position:** Le R:R fixe simplifie le calcul de la taille de position
3. **Backtesting Continu:** Vérifier la robustesse sur nouvelles données
4. **Combinaison:** Possibilité de combiner avec des filtres de volatilité

---

## 📝 Notes Techniques

- **Données:** Nasdaq 100 (NQ) en 5 minutes, timezone Chicago (UTC-5)
- **Période de Test:** 2018-2025
- **Une seule entrée par jour:** Premier signal valide dans la fenêtre 01:00-04:00
- **FVG (Fair Value Gap):** Écart entre le haut de la bougie n-2 et le bas de la bougie n (ou inverse)
- **Buffer SL:** 0.5 points pour éviter les stops sur les niveaux exacts

---

*Rapport généré automatiquement par le script judas_swing_fvg_fixed_rr_backtest.py*
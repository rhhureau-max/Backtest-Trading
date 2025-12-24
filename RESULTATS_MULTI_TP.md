# Résultats - Stratégie Judas Swing + FVG (SL Tokyo +/- 0.5pts, TP Multiples)

**Date de génération:** 24/12/2025 à 11:14:29

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

### Gestion du Risque - MULTIPLE TP
- **Stop Loss:** Placé 0.5 points au-delà des niveaux Tokyo/Asia
  - LONG: SL = Asia_Low - 0.5 points
  - SHORT: SL = Asia_High + 0.5 points

### Stratégies de Take Profit

**Stratégie A - 100% à l'Equilibrium:**
- Position complète fermée à l'équilibre
- Equilibrium = (Asia_High + Asia_Low) / 2

**Stratégie B - 100% au niveau Opposé:**
- Position complète fermée au niveau Tokyo opposé
- LONG: TP à Asia_High
- SHORT: TP à Asia_Low

**Stratégie C - 50% Equilibrium + 50% Opposé:**
- 50% de la position fermée à l'équilibre
- SL déplacé au breakeven (prix d'entrée) après premier TP
- 50% restant vise le niveau opposé ou breakeven

- **Time Stop:** 12:00 Chicago si ni SL ni TP touché

---

## 📈 Résumé Global par Stratégie TP

### Stratégie A (100% Equilibrium)

| Année | Total Trades | Win Rate (%) | Net Profit (pts) | Profit Factor | Max Drawdown (pts) |
|-------|--------------|--------------|------------------|---------------|---------------------|
| 2018 | 178 | 67.98% | 1046.33 | 4.01 | 114.38 |
| 2019 | 178 | 55.62% | 640.27 | 2.66 | 51.65 |
| 2020 | 179 | 67.04% | 2407.16 | 4.17 | 77.60 |
| 2021 | 203 | 63.55% | 2516.42 | 4.38 | 149.48 |
| 2022 | 217 | 58.99% | 2562.94 | 3.00 | 102.14 |
| 2023 | 215 | 67.44% | 2150.23 | 5.27 | 32.62 |
| 2024 | 209 | 67.94% | 2769.63 | 5.81 | 56.06 |
| 2025 | 178 | 62.36% | 2615.40 | 4.07 | 144.10 |
| **TOTAL** | **1557** | **63.84%** | **16708.39** | **4.07** | **149.48** |

### Stratégie B (100% Opposite)

| Année | Total Trades | Win Rate (%) | Net Profit (pts) | Profit Factor | Max Drawdown (pts) |
|-------|--------------|--------------|------------------|---------------|---------------------|
| 2018 | 178 | 61.24% | 962.16 | 2.96 | 108.02 |
| 2019 | 178 | 48.31% | 671.46 | 2.18 | 98.98 |
| 2020 | 179 | 60.89% | 2421.36 | 3.03 | 154.47 |
| 2021 | 203 | 59.61% | 2937.79 | 3.85 | 196.93 |
| 2022 | 217 | 54.38% | 2075.31 | 1.95 | 199.51 |
| 2023 | 215 | 60.93% | 2320.70 | 3.91 | 62.03 |
| 2024 | 209 | 61.72% | 2684.99 | 3.72 | 154.07 |
| 2025 | 178 | 56.18% | 2791.40 | 3.17 | 180.61 |
| **TOTAL** | **1557** | **57.87%** | **16865.17** | **2.98** | **199.51** |

### Stratégie C (50/50 Partial)

| Année | Total Trades | Win Rate (%) | Net Profit (pts) | Profit Factor | Max Drawdown (pts) |
|-------|--------------|--------------|------------------|---------------|---------------------|
| 2018 | 178 | 68.54% | 975.90 | 3.87 | 108.02 |
| 2019 | 178 | 55.62% | 685.06 | 2.83 | 47.07 |
| 2020 | 179 | 67.04% | 2420.50 | 4.40 | 77.60 |
| 2021 | 203 | 64.53% | 2627.59 | 4.69 | 162.06 |
| 2022 | 217 | 59.91% | 2469.82 | 3.10 | 110.35 |
| 2023 | 215 | 68.37% | 2261.58 | 6.36 | 32.62 |
| 2024 | 209 | 68.42% | 2737.20 | 6.16 | 56.06 |
| 2025 | 178 | 62.36% | 2642.67 | 4.24 | 132.17 |
| **TOTAL** | **1557** | **64.29%** | **16820.32** | **4.31** | **162.06** |

---

## 📅 Résultats Détaillés par Année

### Année 2018

| Stratégie | Total Trades | Win Rate (%) | Net Profit (pts) | Profit Factor | Max Drawdown (pts) |
|-----------|--------------|--------------|------------------|---------------|---------------------|
| Stratégie A (100% Equilibrium) | 178 | 67.98% | 1046.33 | 4.01 | 114.38 |
| Stratégie B (100% Opposite) | 178 | 61.24% | 962.16 | 2.96 | 108.02 |
| Stratégie C (50/50 Partial) | 178 | 68.54% | 975.90 | 3.87 | 108.02 |

### Année 2019

| Stratégie | Total Trades | Win Rate (%) | Net Profit (pts) | Profit Factor | Max Drawdown (pts) |
|-----------|--------------|--------------|------------------|---------------|---------------------|
| Stratégie A (100% Equilibrium) | 178 | 55.62% | 640.27 | 2.66 | 51.65 |
| Stratégie B (100% Opposite) | 178 | 48.31% | 671.46 | 2.18 | 98.98 |
| Stratégie C (50/50 Partial) | 178 | 55.62% | 685.06 | 2.83 | 47.07 |

### Année 2020

| Stratégie | Total Trades | Win Rate (%) | Net Profit (pts) | Profit Factor | Max Drawdown (pts) |
|-----------|--------------|--------------|------------------|---------------|---------------------|
| Stratégie A (100% Equilibrium) | 179 | 67.04% | 2407.16 | 4.17 | 77.60 |
| Stratégie B (100% Opposite) | 179 | 60.89% | 2421.36 | 3.03 | 154.47 |
| Stratégie C (50/50 Partial) | 179 | 67.04% | 2420.50 | 4.40 | 77.60 |

### Année 2021

| Stratégie | Total Trades | Win Rate (%) | Net Profit (pts) | Profit Factor | Max Drawdown (pts) |
|-----------|--------------|--------------|------------------|---------------|---------------------|
| Stratégie A (100% Equilibrium) | 203 | 63.55% | 2516.42 | 4.38 | 149.48 |
| Stratégie B (100% Opposite) | 203 | 59.61% | 2937.79 | 3.85 | 196.93 |
| Stratégie C (50/50 Partial) | 203 | 64.53% | 2627.59 | 4.69 | 162.06 |

### Année 2022

| Stratégie | Total Trades | Win Rate (%) | Net Profit (pts) | Profit Factor | Max Drawdown (pts) |
|-----------|--------------|--------------|------------------|---------------|---------------------|
| Stratégie A (100% Equilibrium) | 217 | 58.99% | 2562.94 | 3.00 | 102.14 |
| Stratégie B (100% Opposite) | 217 | 54.38% | 2075.31 | 1.95 | 199.51 |
| Stratégie C (50/50 Partial) | 217 | 59.91% | 2469.82 | 3.10 | 110.35 |

### Année 2023

| Stratégie | Total Trades | Win Rate (%) | Net Profit (pts) | Profit Factor | Max Drawdown (pts) |
|-----------|--------------|--------------|------------------|---------------|---------------------|
| Stratégie A (100% Equilibrium) | 215 | 67.44% | 2150.23 | 5.27 | 32.62 |
| Stratégie B (100% Opposite) | 215 | 60.93% | 2320.70 | 3.91 | 62.03 |
| Stratégie C (50/50 Partial) | 215 | 68.37% | 2261.58 | 6.36 | 32.62 |

### Année 2024

| Stratégie | Total Trades | Win Rate (%) | Net Profit (pts) | Profit Factor | Max Drawdown (pts) |
|-----------|--------------|--------------|------------------|---------------|---------------------|
| Stratégie A (100% Equilibrium) | 209 | 67.94% | 2769.63 | 5.81 | 56.06 |
| Stratégie B (100% Opposite) | 209 | 61.72% | 2684.99 | 3.72 | 154.07 |
| Stratégie C (50/50 Partial) | 209 | 68.42% | 2737.20 | 6.16 | 56.06 |

### Année 2025

| Stratégie | Total Trades | Win Rate (%) | Net Profit (pts) | Profit Factor | Max Drawdown (pts) |
|-----------|--------------|--------------|------------------|---------------|---------------------|
| Stratégie A (100% Equilibrium) | 178 | 62.36% | 2615.40 | 4.07 | 144.10 |
| Stratégie B (100% Opposite) | 178 | 56.18% | 2791.40 | 3.17 | 180.61 |
| Stratégie C (50/50 Partial) | 178 | 62.36% | 2642.67 | 4.24 | 132.17 |

---

## 💡 Analyse et Conclusions

### Performance Globale

- **Meilleure Stratégie:** Stratégie B (100% Opposite) avec un profit net total de 16865.17 points

### Observations Clés

1. **Stratégie Equilibrium:** Plus conservative, TP plus proche, win rate potentiellement plus élevé
2. **Stratégie Opposite:** TP plus ambitieux au niveau Tokyo opposé, R:R plus élevé
3. **Stratégie Partial:** Combine les avantages des deux avec gestion du risque optimisée
4. **Breakeven Management:** La stratégie partielle protège 50% du profit après premier TP

### Avantages de la Stratégie Partielle

- **Sécurisation rapide:** 50% du profit sécurisé à l'équilibre
- **Protection:** SL au breakeven après premier TP élimine le risque sur les 50% restants
- **Potentiel:** 50% reste en position pour capturer le mouvement complet
- **Psychologie:** Réduction du stress avec profit partiel sécurisé

### Recommandations

1. **Adaptabilité:** Choisir la stratégie selon les conditions de marché
2. **Volatilité:** En haute volatilité, privilégier la stratégie partielle
3. **Trending Markets:** En marchés directionnels forts, stratégie opposite peut être optimale
4. **Risk Management:** La stratégie partielle offre le meilleur compromis risque/rendement

---

## 📝 Notes Techniques

- **Données:** Nasdaq 100 (NQ) en 5 minutes, timezone Chicago (UTC-5)
- **Période de Test:** 2018-2025
- **Une seule entrée par jour:** Premier signal valide dans la fenêtre 01:00-04:00
- **FVG (Fair Value Gap):** Écart entre le haut de la bougie n-2 et le bas de la bougie n (ou inverse)
- **Buffer SL:** 0.5 points pour éviter les stops sur les niveaux exacts
- **Breakeven:** Dans la stratégie partielle, SL déplacé au prix d'entrée après premier TP

---

*Rapport généré automatiquement par le script judas_swing_fvg_multi_tp_backtest.py*
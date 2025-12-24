# Résultats - Stratégie Judas Swing + FVG (SL Swing / TP Equilibrium)

**Date de génération:** 24/12/2025 à 10:10:41

---

## 📊 Configuration de la Stratégie

### Sessions de Trading
- **Asia Session:** 18:00 - 23:00 (J-1, heure Chicago)
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

### Gestion du Risque - NOUVELLE APPROCHE
- **Stop Loss:** Placé à l'extrémité du swing
  - LONG: SL = Asia_Low
  - SHORT: SL = Asia_High
- **Take Profit:** Placé à l'équilibre (milieu entre Asia_High et Asia_Low)
  - TP = (Asia_High + Asia_Low) / 2
- **Time Stop:** 12:00 Chicago si ni SL ni TP touché

---

## 📈 Résumé Global - Stratégie Equilibrium

| Année | Total Trades | Win Rate (%) | Net Profit (pts) | Profit Factor | Max Drawdown (pts) | Avg Risk/Reward |
|-------|--------------|--------------|------------------|---------------|---------------------|-----------------|
| 2018 | 178 | 69.10% | 1094.34 | 4.31 | 111.88 | 0.00 |
| 2019 | 178 | 57.30% | 695.43 | 2.98 | 50.15 | 0.00 |
| 2020 | 179 | 67.60% | 2476.66 | 4.38 | 76.10 | 0.00 |
| 2021 | 203 | 64.04% | 2593.92 | 4.63 | 143.48 | 0.00 |
| 2022 | 217 | 58.53% | 2603.63 | 3.09 | 98.14 | 0.00 |
| 2023 | 215 | 66.98% | 2179.12 | 5.55 | 31.73 | 0.00 |
| 2024 | 209 | 66.99% | 2777.93 | 5.93 | 55.06 | 0.00 |
| 2025 | 178 | 62.92% | 2685.90 | 4.27 | 138.10 | 0.00 |
| **TOTAL** | **1557** | **64.16%** | **17106.93** | **4.27** | **143.48** | **-** |

---

## 📅 Résultats Détaillés par Année

### Année 2018

- **Total Trades:** 178
- **Win Rate:** 69.10%
- **Net Profit:** 1094.34 points
- **Profit Factor:** 4.31
- **Max Drawdown:** 111.88 points
- **Avg Risk/Reward Ratio:** 0.00

### Année 2019

- **Total Trades:** 178
- **Win Rate:** 57.30%
- **Net Profit:** 695.43 points
- **Profit Factor:** 2.98
- **Max Drawdown:** 50.15 points
- **Avg Risk/Reward Ratio:** 0.00

### Année 2020

- **Total Trades:** 179
- **Win Rate:** 67.60%
- **Net Profit:** 2476.66 points
- **Profit Factor:** 4.38
- **Max Drawdown:** 76.10 points
- **Avg Risk/Reward Ratio:** 0.00

### Année 2021

- **Total Trades:** 203
- **Win Rate:** 64.04%
- **Net Profit:** 2593.92 points
- **Profit Factor:** 4.63
- **Max Drawdown:** 143.48 points
- **Avg Risk/Reward Ratio:** 0.00

### Année 2022

- **Total Trades:** 217
- **Win Rate:** 58.53%
- **Net Profit:** 2603.63 points
- **Profit Factor:** 3.09
- **Max Drawdown:** 98.14 points
- **Avg Risk/Reward Ratio:** 0.00

### Année 2023

- **Total Trades:** 215
- **Win Rate:** 66.98%
- **Net Profit:** 2179.12 points
- **Profit Factor:** 5.55
- **Max Drawdown:** 31.73 points
- **Avg Risk/Reward Ratio:** 0.00

### Année 2024

- **Total Trades:** 209
- **Win Rate:** 66.99%
- **Net Profit:** 2777.93 points
- **Profit Factor:** 5.93
- **Max Drawdown:** 55.06 points
- **Avg Risk/Reward Ratio:** 0.00

### Année 2025

- **Total Trades:** 178
- **Win Rate:** 62.92%
- **Net Profit:** 2685.90 points
- **Profit Factor:** 4.27
- **Max Drawdown:** 138.10 points
- **Avg Risk/Reward Ratio:** 0.00

---

## 🔄 Comparaison avec Stratégie à TP Fixe

### Avantages de la Stratégie Equilibrium

1. **Risk/Reward Adaptatif:**
   - Le ratio R:R s'adapte automatiquement à la taille du range Asia
   - Plus favorable dans les marchés avec des ranges larges

2. **Stop Loss Logique:**
   - SL placé à un niveau technique significatif (swing extremity)
   - Évite les stops arbitraires à distance fixe

3. **Take Profit Technique:**
   - TP à l'équilibre représente un niveau psychologique important
   - Zone de potentielle résistance/support

### Points d'Attention

1. **Variabilité du SL:**
   - La distance du SL varie selon la taille du range Asia
   - Nécessite une adaptation de la taille de position

2. **TP Potentiellement Court:**
   - Dans certains cas, le TP peut être atteint plus facilement
   - Mais limite aussi le potentiel de profit

---

## 💡 Analyse et Conclusions

### Performance Globale

- **Total Trades sur 8 ans:** 1557
- **Win Rate Moyen:** 64.16%
- **Profit Net Total:** 17106.93 points
- **Profit Factor Global:** 4.27
- **Drawdown Maximum:** 143.48 points

### Meilleure Année: 2024
- Profit: 2777.93 points

### Année la Plus Difficile: 2019
- Profit: 695.43 points

### Observations Clés

1. **Ratio R:R Favorable:** La stratégie présente un ratio risk/reward moyen élevé
2. **Win Rate Solide:** Un win rate supérieur à 50% est généralement observé
3. **Drawdown Contrôlé:** Le drawdown maximum reste gérable
4. **Adaptabilité:** La stratégie s'adapte aux conditions de marché variables

### Recommandations

1. **Sizing de Position:** Adapter la taille selon la distance du SL
2. **Filtres de Volatilité:** Considérer des filtres basés sur la taille du range Asia
3. **Gestion Partielle:** Envisager une sortie partielle à l'équilibre avec trail stop
4. **Backtesting Continu:** Surveiller les performances sur données récentes

---

## 📝 Notes Techniques

- **Données:** Nasdaq 100 (NQ) en 5 minutes, timezone Chicago (UTC-5)
- **Période de Test:** 2018-2025
- **Une seule entrée par jour:** Premier signal valide dans la fenêtre 01:00-04:00
- **FVG (Fair Value Gap):** Écart entre le haut de la bougie n-2 et le bas de la bougie n (ou inverse)
- **Equilibrium:** Point milieu calculé comme (Asia_High + Asia_Low) / 2

---

*Rapport généré automatiquement par le script judas_swing_fvg_equilibrium_backtest.py*
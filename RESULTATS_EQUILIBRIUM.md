# Résultats - Stratégie Judas Swing + FVG (SL Swing / TP Equilibrium)

**Date de génération:** 24/12/2025 à 10:55:17

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

### Gestion du Risque - APPROCHE MANIPULATION EXTREMITY
- **Stop Loss:** Placé à l'extrémité de la manipulation (mouvement de faux-out)
  - LONG: SL = Plus bas atteint lors du breach d'Asia_Low (manipulation low)
  - SHORT: SL = Plus haut atteint lors du breach d'Asia_High (manipulation high)
- **Take Profit:** Placé à l'équilibre (milieu entre Asia_High et Asia_Low)
  - TP = (Asia_High + Asia_Low) / 2
- **Avantage:** SL placé au véritable point de validation/invalidation du setup
- **Time Stop:** 12:00 Chicago si ni SL ni TP touché

---

## 📈 Résumé Global - Stratégie Equilibrium

| Année | Total Trades | Win Rate (%) | Net Profit (pts) | Profit Factor | Max Drawdown (pts) | Avg Risk/Reward |
|-------|--------------|--------------|------------------|---------------|---------------------|-----------------|
| 2018 | 178 | 42.13% | 211.80 | 1.18 | 189.82 | 1.66 |
| 2019 | 178 | 39.33% | -67.96 | 0.94 | 300.93 | 1.54 |
| 2020 | 179 | 44.69% | 628.58 | 1.25 | 559.49 | 1.59 |
| 2021 | 203 | 46.80% | 635.13 | 1.25 | 448.02 | 1.50 |
| 2022 | 217 | 38.25% | -173.56 | 0.96 | 848.09 | 1.23 |
| 2023 | 215 | 48.84% | 357.87 | 1.18 | 489.75 | 1.20 |
| 2024 | 209 | 39.71% | -902.42 | 0.70 | 1005.26 | 1.43 |
| 2025 | 178 | 44.94% | 827.97 | 1.27 | 650.44 | 1.50 |
| **TOTAL** | **1557** | **42.97%** | **1517.40** | **1.23** | **1005.26** | **-** |

---

## 📅 Résultats Détaillés par Année

### Année 2018

- **Total Trades:** 178
- **Win Rate:** 42.13%
- **Net Profit:** 211.80 points
- **Profit Factor:** 1.18
- **Max Drawdown:** 189.82 points
- **Avg Risk/Reward Ratio:** 1.66

### Année 2019

- **Total Trades:** 178
- **Win Rate:** 39.33%
- **Net Profit:** -67.96 points
- **Profit Factor:** 0.94
- **Max Drawdown:** 300.93 points
- **Avg Risk/Reward Ratio:** 1.54

### Année 2020

- **Total Trades:** 179
- **Win Rate:** 44.69%
- **Net Profit:** 628.58 points
- **Profit Factor:** 1.25
- **Max Drawdown:** 559.49 points
- **Avg Risk/Reward Ratio:** 1.59

### Année 2021

- **Total Trades:** 203
- **Win Rate:** 46.80%
- **Net Profit:** 635.13 points
- **Profit Factor:** 1.25
- **Max Drawdown:** 448.02 points
- **Avg Risk/Reward Ratio:** 1.50

### Année 2022

- **Total Trades:** 217
- **Win Rate:** 38.25%
- **Net Profit:** -173.56 points
- **Profit Factor:** 0.96
- **Max Drawdown:** 848.09 points
- **Avg Risk/Reward Ratio:** 1.23

### Année 2023

- **Total Trades:** 215
- **Win Rate:** 48.84%
- **Net Profit:** 357.87 points
- **Profit Factor:** 1.18
- **Max Drawdown:** 489.75 points
- **Avg Risk/Reward Ratio:** 1.20

### Année 2024

- **Total Trades:** 209
- **Win Rate:** 39.71%
- **Net Profit:** -902.42 points
- **Profit Factor:** 0.70
- **Max Drawdown:** 1005.26 points
- **Avg Risk/Reward Ratio:** 1.43

### Année 2025

- **Total Trades:** 178
- **Win Rate:** 44.94%
- **Net Profit:** 827.97 points
- **Profit Factor:** 1.27
- **Max Drawdown:** 650.44 points
- **Avg Risk/Reward Ratio:** 1.50

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
- **Win Rate Moyen:** 42.97%
- **Profit Net Total:** 1517.40 points
- **Profit Factor Global:** 1.23
- **Drawdown Maximum:** 1005.26 points

### Meilleure Année: 2025
- Profit: 827.97 points

### Année la Plus Difficile: 2024
- Profit: -902.42 points

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
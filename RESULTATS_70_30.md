# Résultats - Stratégie Judas Swing + FVG (70/30 Partial Exit)

**Date de génération:** 24/12/2025 à 13:03:41

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

### Gestion du Risque - 70/30 PARTIAL EXIT
- **Stop Loss:** Placé 0.5 points au-delà des niveaux Tokyo/Asia
  - LONG: SL = Asia_Low - 0.5 points
  - SHORT: SL = Asia_High + 0.5 points

### Stratégie de Take Profit (70/30)

**Sortie en 2 étapes:**
1. **70% de la position** fermée à l'équilibre
   - Equilibrium = (Asia_High + Asia_Low) / 2
   - Sécurise rapidement la majorité du profit

2. **SL déplacé au breakeven** (prix d'entrée) après TP1
   - Élimine tout risque sur les 30% restants

3. **30% restants** visent le niveau Tokyo opposé
   - LONG: TP2 à Asia_High
   - SHORT: TP2 à Asia_Low
   - Si pas atteint: sortie au breakeven ou time stop

- **Time Stop:** 12:00 Chicago si ni SL ni TP touché

---

## 📈 Résumé Global

| Année | Total Trades | Win Rate (%) | Net Profit (pts) | Profit Factor | Max Drawdown (pts) |
|-------|--------------|--------------|------------------|---------------|---------------------|
| 2018 | 178 | 68.54% | 1004.07 | 3.93 | 110.34 |
| 2019 | 178 | 55.62% | 667.15 | 2.76 | 48.90 |
| 2020 | 179 | 67.04% | 2415.16 | 4.30 | 77.60 |
| 2021 | 203 | 64.04% | 2583.12 | 4.57 | 157.03 |
| 2022 | 217 | 59.91% | 2507.07 | 3.07 | 107.07 |
| 2023 | 215 | 67.91% | 2229.04 | 6.03 | 32.62 |
| 2024 | 209 | 68.42% | 2754.70 | 6.08 | 56.06 |
| 2025 | 178 | 62.36% | 2631.76 | 4.17 | 136.94 |
| **TOTAL** | **1557** | **64.10%** | **16792.08** | **4.23** | **157.03** |

---

## 💡 Analyse et Conclusions

### Performance Globale 70/30

- **Total Trades:** 1557
- **Win Rate Global:** 64.10%
- **Profit Net Total:** 16792.08 points
- **Profit Factor Global:** 4.23
- **Max Drawdown:** 157.03 points

### Avantages de la Stratégie 70/30

1. **Sécurisation Rapide Optimisée:** 70% du profit sécurisé rapidement à l'équilibre
2. **Protection Maximale:** SL au breakeven après TP1 = zéro risque sur 30% restants
3. **Potentiel Conservé:** 30% reste en position pour capturer le mouvement complet
4. **Meilleur Ratio Sécurité/Potentiel:** Plus de profit sécurisé qu'avec 50/50
5. **Psychologie:** Encore moins de stress avec 70% du profit déjà sécurisé

### Comparaison avec Autres Stratégies

**vs 50/50 Partial:**
- Plus conservateur (70% vs 50% sécurisé)
- Moins de potentiel sur TP2 (30% vs 50%)
- Meilleure protection du capital

**vs 100% Equilibrium:**
- Garde un potentiel de profit supplémentaire avec les 30%
- Protection breakeven après TP1

**vs 100% Opposite:**
- Sécurise 70% du profit rapidement
- Réduit le risque de reversal

### Recommandations

1. **Idéal pour traders conservateurs:** Maximise la sécurisation du profit
2. **Gestion émotionnelle:** 70% sécurisé réduit significativement le stress
3. **Marchés volatils:** Protection optimale avec breakeven sur 30% restants
4. **Profil risque/rendement:** Excellent compromis entre sécurité et potentiel

---

## 📝 Notes Techniques

- **Données:** Nasdaq 100 (NQ) en 5 minutes, timezone Chicago (UTC-5)
- **Période de Test:** 2018-2025
- **Une seule entrée par jour:** Premier signal valide dans la fenêtre 01:00-04:00
- **FVG (Fair Value Gap):** Écart entre le haut de la bougie n-2 et le bas de la bougie n (ou inverse)
- **Buffer SL:** 0.5 points pour éviter les stops sur les niveaux exacts
- **Breakeven:** SL déplacé au prix d'entrée après 70% sortis à TP1
- **Ratio 70/30:** Optimise sécurisation du profit tout en conservant un potentiel

---

*Rapport généré automatiquement par le script judas_swing_fvg_70_30_backtest.py*
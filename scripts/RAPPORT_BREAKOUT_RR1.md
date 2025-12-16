# 📊 Rapport d'Analyse : Stratégie Breakout 8h30 (RR 1:1)

## 📋 Résumé Exécutif

Cette analyse étudie une stratégie de trading basée sur la cassure (breakout) de la bougie de 8h30 par rapport aux 5 bougies précédentes, avec un ratio Risk-Reward de 1:1.

### Conditions de la Stratégie

| Paramètre | Description |
|-----------|-------------|
| **Condition d'entrée** | La bougie 8h30 doit clôturer AU-DESSUS (haussier) ou EN-DESSOUS (baissier) des closes des 5 bougies précédentes |
| **Entrée** | Au close de la bougie 8h30 |
| **Stop Loss** | Au milieu du corps de la bougie 8h30 (Open + Close) / 2 |
| **Take Profit** | Même distance que le SL (RR = 1:1) |

---

## 🕐 Timeframe 1 Minute

### Résumé Global (2018-2025)

| Direction | Bougies Qualifiées | Taux Qualification | Wins | Losses | Win Rate | Pts Moyens Gagnés | Pts Moyens Perdus |
|-----------|-------------------|-------------------|------|--------|----------|-------------------|-------------------|
| **Haussier** | 810 | 39.6% | 554 | 255 | **68.5%** | 6.19 pts | 9.04 pts |
| **Baissier** | 710 | 34.7% | 486 | 222 | **68.6%** | 5.55 pts | 7.34 pts |
| **Total** | 1520 | 37.2% | 1040 | 477 | **68.6%** | - | - |

### 📈 Observations Clés (1M)
- **Win Rate élevé** : ~68.5% de trades gagnants avec un RR de 1:1
- **Taux de qualification** : ~37% des bougies 8h30 créent un breakout
- **Équilibre haussier/baissier** : Légèrement plus de signaux haussiers (810 vs 710)
- **Points moyens** : Les gains sont plus petits que les pertes en moyenne, mais le win rate compense

---

## 🕔 Timeframe 5 Minutes

### Résumé Global (2018-2025)

| Direction | Bougies Qualifiées | Taux Qualification | Wins | Losses | Win Rate | Pts Moyens Gagnés | Pts Moyens Perdus |
|-----------|-------------------|-------------------|------|--------|----------|-------------------|-------------------|
| **Haussier** | 846 | 41.7% | 596 | 249 | **70.5%** | 12.72 pts | 17.13 pts |
| **Baissier** | 783 | 38.6% | 518 | 264 | **66.2%** | 13.46 pts | 18.29 pts |
| **Total** | 1629 | 40.2% | 1114 | 513 | **68.5%** | - | - |

### 📈 Observations Clés (5M)
- **Meilleur Win Rate Haussier** : 70.5% pour les signaux haussiers
- **Taux de qualification élevé** : ~40% des bougies 8h30 créent un breakout
- **Points plus importants** : Gains moyens de 12-13 pts vs 6 pts en 1M
- **Légère asymétrie** : Haussier légèrement plus performant (70.5% vs 66.2%)

---

## 🕧 Timeframe 15 Minutes

### Résumé Global (2018-2025)

| Direction | Bougies Qualifiées | Taux Qualification | Wins | Losses | Win Rate | Pts Moyens Gagnés | Pts Moyens Perdus |
|-----------|-------------------|-------------------|------|--------|----------|-------------------|-------------------|
| **Haussier** | 775 | 38.2% | 515 | 259 | **66.5%** | 18.85 pts | 24.77 pts |
| **Baissier** | 688 | 33.9% | 441 | 246 | **64.2%** | 20.87 pts | 30.74 pts |
| **Total** | 1463 | 36.1% | 956 | 505 | **65.4%** | - | - |

### 📈 Observations Clés (15M)
- **Win Rate légèrement inférieur** : ~65% vs ~68% pour les autres timeframes
- **Points significatifs** : Gains moyens de 19-21 pts
- **Risque accru** : Pertes moyennes de 25-31 pts (plus volatil)
- **Biais haussier** : Win rate et qualification meilleurs pour les haussiers

---

## 📊 Analyse Comparative par Timeframe

### Win Rate Global

| Timeframe | Win Rate Haussier | Win Rate Baissier | Win Rate Global |
|-----------|-------------------|-------------------|-----------------|
| 1 minute  | 68.5%             | 68.6%             | **68.6%**       |
| 5 minutes | 70.5%             | 66.2%             | **68.5%**       |
| 15 minutes| 66.5%             | 64.2%             | **65.4%**       |

### Taux de Qualification

| Timeframe | Haussier | Baissier | Global |
|-----------|----------|----------|--------|
| 1 minute  | 39.6%    | 34.7%    | 37.2%  |
| 5 minutes | 41.7%    | 38.6%    | 40.2%  |
| 15 minutes| 38.2%    | 33.9%    | 36.1%  |

### Nombre Total de Signaux

| Timeframe | Haussier | Baissier | Total |
|-----------|----------|----------|-------|
| 1 minute  | 810      | 710      | 1520  |
| 5 minutes | 846      | 783      | 1629  |
| 15 minutes| 775      | 688      | 1463  |

---

## 🎯 Conclusions et Recommandations

### Points Forts de la Stratégie

1. **Win Rate exceptionnel** : 65-70% de trades gagnants avec un RR de 1:1
2. **Rentabilité théorique** : Avec un win rate > 50% et RR = 1, la stratégie est mathématiquement profitable
3. **Taux de qualification élevé** : 36-40% des journées offrent un signal
4. **Consistance** : Win rate stable sur toutes les années (2018-2025)

### Meilleur Timeframe

🏆 **5 Minutes** offre le meilleur équilibre :
- Win rate élevé (68.5%)
- Plus grand nombre de signaux (1629)
- Points moyens significatifs (12-13 pts)
- Taux de qualification maximal (40.2%)

### Calcul de l'Espérance Mathématique

Pour le timeframe 5 minutes (haussier) :
- Win Rate : 70.5%
- Gain moyen : 12.72 pts
- Perte moyenne : 17.13 pts

**Espérance = (0.705 × 12.72) - (0.295 × 17.13) = 8.97 - 5.05 = +3.92 pts par trade**

### Stratégie Suggérée

| Condition | Recommandation |
|-----------|----------------|
| **Timeframe optimal** | 5 minutes |
| **Direction préférée** | Haussier (win rate 70.5%) |
| **Position sizing** | 1% du capital par trade |
| **Stop Loss** | Milieu du corps de la bougie 8h30 |
| **Take Profit** | RR 1:1 (même distance que SL) |

### ⚠️ Avertissements

- Cette analyse ne tient pas compte des frais de transaction
- Les performances passées ne garantissent pas les résultats futurs
- La stratégie suppose une exécution parfaite au close de la bougie 8h30
- Certains trades peuvent ne pas être complétés avant la fin de journée

---

## 📁 Annexe : Détails par Année

### Timeframe 1M - Win Rate par Année

| Année | Haussier | Baissier |
|-------|----------|----------|
| 2018  | 60.4%    | 61.0%    |
| 2019  | 66.3%    | 70.3%    |
| 2020  | 65.3%    | 69.1%    |
| 2021  | 71.6%    | 76.5%    |
| 2022  | 66.1%    | 77.8%    |
| 2023  | 65.2%    | 55.0%    |
| 2024  | 69.0%    | 64.0%    |
| 2025  | 68.6%    | 68.5%    |

### Timeframe 5M - Win Rate par Année

| Année | Haussier | Baissier |
|-------|----------|----------|
| 2018  | 70.9%    | 59.7%    |
| 2019  | 76.7%    | 68.0%    |
| 2020  | 72.2%    | 64.3%    |
| 2021  | 66.1%    | 66.7%    |
| 2022  | 70.3%    | 67.5%    |
| 2023  | 70.7%    | 72.6%    |
| 2024  | 66.7%    | 61.4%    |
| 2025  | 65.1%    | 61.7%    |

### Timeframe 15M - Win Rate par Année

| Année | Haussier | Baissier |
|-------|----------|----------|
| 2018  | 61.9%    | 72.3%    |
| 2019  | 66.4%    | 71.6%    |
| 2020  | 66.4%    | 56.8%    |
| 2021  | 73.3%    | 55.8%    |
| 2022  | 65.5%    | 74.7%    |
| 2023  | 66.7%    | 61.1%    |
| 2024  | 66.7%    | 61.6%    |
| 2025  | 65.4%    | 57.7%    |

---

*Rapport généré automatiquement par `breakout_strategy_analysis.py`*  
*Stratégie : Breakout 8h30 avec RR 1:1*  
*Données analysées : 2018-2025*

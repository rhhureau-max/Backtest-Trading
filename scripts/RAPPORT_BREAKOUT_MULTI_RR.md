# 📊 Rapport d'Analyse : Stratégie Breakout 8h30 - Multi RR (1.5, 2.0, 2.5)

## 📋 Résumé Exécutif

Cette analyse compare les performances de la stratégie de breakout 8h30 avec différents ratios Risk-Reward (1.5, 2.0, 2.5).

### Conditions de la Stratégie

| Paramètre | Description |
|-----------|-------------|
| **Condition d'entrée** | La bougie 8h30 doit clôturer AU-DESSUS ou EN-DESSOUS des closes des 5 bougies précédentes |
| **Entrée** | Au close de la bougie 8h30 |
| **Stop Loss** | Au milieu du corps de la bougie 8h30 |
| **Take Profit** | Variable : 1.5x, 2x, ou 2.5x la distance du SL |

---

## 📈 Tableau Comparatif Global

### Win Rate par RR et Timeframe

| Timeframe | RR 1.5 | RR 2.0 | RR 2.5 |
|-----------|--------|--------|--------|
| **1 Minute** | 56.4% (1508 trades) | 48.1% (1508 trades) | 43.2% (1508 trades) |
| **5 Minutes** | 57.8% (1626 trades) | 50.9% (1626 trades) | 44.5% (1626 trades) |
| **15 Minutes** | 54.6% (1459 trades) | 47.7% (1456 trades) | 41.8% (1450 trades) |

### Comparaison avec RR 1.0 (référence)

| Timeframe | RR 1.0 | RR 1.5 | RR 2.0 | RR 2.5 |
|-----------|--------|--------|--------|--------|
| **1M** | 68.6% | 56.4% | 48.1% | 43.2% |
| **5M** | 68.5% | 57.8% | 50.9% | 44.5% |
| **15M** | 65.4% | 54.6% | 47.7% | 41.8% |

---

## 🎯 Analyse par Ratio Risk-Reward

### RR 1.5 (TP = 1.5 × SL)

#### Résumé Global

| Timeframe | Direction | Trades | Win Rate | Espérance/Trade |
|-----------|-----------|--------|----------|-----------------|
| **1M** | Haussier | 809 | 56.9% | +3.72 pts |
| **1M** | Baissier | 699 | 55.8% | +3.47 pts |
| **5M** | Haussier | 844 | 58.8% | +6.59 pts |
| **5M** | Baissier | 782 | 56.8% | +6.51 pts |
| **15M** | Haussier | 769 | 55.7% | +8.48 pts |
| **15M** | Baissier | 681 | 53.5% | +5.50 pts |

**Observations RR 1.5 :**
- Win rate encore solide (~55-59%)
- Espérance positive sur tous les timeframes
- Le 5M haussier offre le meilleur équilibre (58.8% win rate, +6.59 pts)

---

### RR 2.0 (TP = 2 × SL)

#### Résumé Global

| Timeframe | Direction | Trades | Win Rate | Espérance/Trade |
|-----------|-----------|--------|----------|-----------------|
| **1M** | Haussier | 809 | 48.6% | +3.88 pts |
| **1M** | Baissier | 699 | 47.5% | +3.47 pts |
| **5M** | Haussier | 844 | 51.8% | +6.53 pts |
| **5M** | Baissier | 782 | 50.0% | +6.27 pts |
| **15M** | Haussier | 769 | 49.3% | +8.64 pts |
| **15M** | Baissier | 681 | 46.0% | +4.56 pts |

**Observations RR 2.0 :**
- Win rate autour de 50% (équilibre)
- Espérance toujours positive grâce au RR favorable
- Le 15M haussier offre la meilleure espérance (+8.64 pts)

---

### RR 2.5 (TP = 2.5 × SL)

#### Résumé Global

| Timeframe | Direction | Trades | Win Rate | Espérance/Trade |
|-----------|-----------|--------|----------|-----------------|
| **1M** | Haussier | 809 | 43.4% | +3.57 pts |
| **1M** | Baissier | 699 | 42.9% | +3.33 pts |
| **5M** | Haussier | 844 | 45.1% | +4.24 pts |
| **5M** | Baissier | 782 | 43.7% | +4.05 pts |
| **15M** | Haussier | 769 | 42.9% | +6.19 pts |
| **15M** | Baissier | 681 | 40.5% | +2.46 pts |

**Observations RR 2.5 :**
- Win rate plus faible (~40-45%)
- Espérance reste positive malgré le win rate < 50%
- Le 15M haussier conserve la meilleure espérance (+6.19 pts)

---

## 📊 Analyse Comparative

### Win Rate en fonction du RR

```
RR        1.0     1.5     2.0     2.5
        ┌─────────────────────────────┐
1M      │ 68.6%   56.4%   48.1%   43.2%
5M      │ 68.5%   57.8%   50.9%   44.5%
15M     │ 65.4%   54.6%   47.7%   41.8%
        └─────────────────────────────┘
```

### Seuil de Rentabilité Théorique

Pour un RR donné, le win rate minimum requis pour être profitable est :

| RR | Win Rate Min | Statut 1M | Statut 5M | Statut 15M |
|----|--------------|-----------|-----------|------------|
| 1.0 | 50.0% | ✅ 68.6% | ✅ 68.5% | ✅ 65.4% |
| 1.5 | 40.0% | ✅ 56.4% | ✅ 57.8% | ✅ 54.6% |
| 2.0 | 33.3% | ✅ 48.1% | ✅ 50.9% | ✅ 47.7% |
| 2.5 | 28.6% | ✅ 43.2% | ✅ 44.5% | ✅ 41.8% |

**✅ Tous les ratios sont au-dessus du seuil de rentabilité !**

---

## 🏆 Conclusions et Recommandations

### Quel RR Choisir ?

| Profil | RR Recommandé | Raison |
|--------|---------------|--------|
| **Conservateur** | RR 1.0 | Win rate élevé (68%), psychologiquement plus facile |
| **Équilibré** | RR 1.5 | Bon compromis win rate/gain (~57%, espérance solide) |
| **Agressif** | RR 2.0+ | Gain plus important par trade, mais plus de pertes consécutives |

### Meilleure Configuration par Objectif

| Objectif | Timeframe | RR | Win Rate | Espérance |
|----------|-----------|-----|----------|-----------|
| **Max Win Rate** | 5M | 1.0 | 68.5% | ~3.92 pts |
| **Équilibre** | 5M | 1.5 | 57.8% | ~6.55 pts |
| **Max Espérance** | 15M | 2.0 | 49.3% | ~8.64 pts |
| **Max RR** | 15M | 2.5 | 42.9% | ~6.19 pts |

### Stratégie Optimale Suggérée

🏆 **RR 1.5 sur le timeframe 5 Minutes** offre le meilleur équilibre :
- Win rate solide de **57.8%**
- Espérance de **+6.55 pts** par trade
- Nombre de signaux suffisant (**1626 trades** sur 8 ans ≈ 203/an)
- Marge de sécurité confortable au-dessus du seuil de rentabilité (57.8% vs 40% requis)

### ⚠️ Avertissements

- L'augmentation du RR diminue mécaniquement le win rate
- Un win rate plus faible signifie des séries de pertes plus longues (impact psychologique)
- Les résultats passés ne garantissent pas les performances futures
- Cette analyse ne tient pas compte des frais de transaction

---

## 📁 Annexe : Données Détaillées

### Timeframe 1M - Win Rate par Année et RR

| Année | RR 1.5 H | RR 1.5 B | RR 2.0 H | RR 2.0 B | RR 2.5 H | RR 2.5 B |
|-------|----------|----------|----------|----------|----------|----------|
| 2018  | 49.0%    | 49.4%    | 40.6%    | 42.9%    | 38.5%    | 39.0%    |
| 2019  | 52.5%    | 54.9%    | 45.5%    | 49.5%    | 39.6%    | 42.9%    |
| 2020  | 59.0%    | 55.3%    | 49.5%    | 51.1%    | 44.2%    | 46.8%    |
| 2021  | 61.5%    | 65.3%    | 55.0%    | 57.1%    | 50.5%    | 54.1%    |
| 2022  | 54.5%    | 60.5%    | 46.3%    | 51.9%    | 42.1%    | 45.7%    |
| 2023  | 55.4%    | 50.0%    | 48.2%    | 43.8%    | 43.8%    | 40.0%    |
| 2024  | 54.8%    | 48.0%    | 45.2%    | 43.0%    | 42.9%    | 41.0%    |
| 2025  | 56.8%    | 52.8%    | 44.3%    | 40.4%    | 36.4%    | 37.1%    |

### Timeframe 5M - Win Rate par Année et RR

| Année | RR 1.5 H | RR 1.5 B | RR 2.0 H | RR 2.0 B | RR 2.5 H | RR 2.5 B |
|-------|----------|----------|----------|----------|----------|----------|
| 2018  | 62.8%    | 50.6%    | 52.3%    | 45.5%    | 45.3%    | 37.7%    |
| 2019  | 66.0%    | 59.8%    | 57.3%    | 54.6%    | 52.4%    | 49.5%    |
| 2020  | 61.7%    | 56.1%    | 53.0%    | 52.0%    | 49.6%    | 46.9%    |
| 2021  | 58.7%    | 57.8%    | 47.7%    | 51.0%    | 43.1%    | 41.2%    |
| 2022  | 58.2%    | 55.3%    | 48.4%    | 46.5%    | 41.8%    | 44.7%    |
| 2023  | 56.9%    | 59.5%    | 51.7%    | 53.6%    | 43.1%    | 48.8%    |
| 2024  | 50.0%    | 51.5%    | 43.1%    | 45.5%    | 35.3%    | 43.6%    |
| 2025  | 54.7%    | 55.3%    | 48.8%    | 46.8%    | 48.8%    | 43.6%    |

### Timeframe 15M - Win Rate par Année et RR

| Année | RR 1.5 H | RR 1.5 B | RR 2.0 H | RR 2.0 B | RR 2.5 H | RR 2.5 B |
|-------|----------|----------|----------|----------|----------|----------|
| 2018  | 50.5%    | 62.2%    | 39.4%    | 52.4%    | 28.8%    | 46.3%    |
| 2019  | 55.7%    | 55.2%    | 48.1%    | 47.1%    | 47.2%    | 41.4%    |
| 2020  | 56.2%    | 49.5%    | 47.6%    | 40.0%    | 38.1%    | 36.8%    |
| 2021  | 60.0%    | 49.4%    | 52.0%    | 43.5%    | 46.0%    | 36.5%    |
| 2022  | 52.4%    | 59.6%    | 48.8%    | 47.5%    | 47.6%    | 42.4%    |
| 2023  | 55.0%    | 52.1%    | 49.5%    | 46.5%    | 42.3%    | 39.4%    |
| 2024  | 56.8%    | 49.4%    | 54.3%    | 43.5%    | 53.1%    | 43.5%    |
| 2025  | 55.1%    | 49.4%    | 48.7%    | 41.6%    | 43.6%    | 37.7%    |

---

*Rapport généré automatiquement par `breakout_multi_rr_analysis.py`*  
*Stratégie : Breakout 8h30 avec RR 1.5, 2.0, 2.5*  
*Données analysées : 2018-2025*

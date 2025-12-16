# 📊 Rapport d'Analyse : Continuations de Bougies après 8h30

## 📋 Résumé Exécutif

Cette analyse étudie le comportement des bougies consécutives après une bougie significative à 8h30 (heure de New York - ouverture du marché) sur les données de 2018 à 2025.

### Méthodologie

| Timeframe | Seuil d'amplitude | Période analysée |
|-----------|-------------------|------------------|
| 1 minute  | ≥ 15 points      | 2018-2025        |
| 5 minutes | ≥ 80 points      | 2018-2025        |
| 15 minutes| ≥ 150 points     | 2018-2025        |

L'analyse compte le nombre de bougies consécutives qui continuent dans la même direction que la bougie de 8h30 (de 1 à 5 bougies).

---

## 🕐 Timeframe 1 Minute (Seuil ≥ 15 points)

### Synthèse Globale (2018-2025)

#### Bougies Haussières
- **Total bougies 8h30 qualifiées : 335**

| Continuations | Occurrences | Ratio | Ratio Consécutif | Points Moyens |
|---------------|-------------|-------|------------------|---------------|
| 1 bougie     | 171         | 51.0% | 51.0%           | 14.78 pts     |
| 2 bougies    | 96          | 28.7% | 56.1%           | 26.95 pts     |
| 3 bougies    | 53          | 15.8% | 55.2%           | 37.34 pts     |
| 4 bougies    | 28          | 8.4%  | 52.8%           | 42.23 pts     |
| 5 bougies    | 18          | 5.4%  | 64.3%           | 52.80 pts     |

#### Bougies Baissières
- **Total bougies 8h30 qualifiées : 291**

| Continuations | Occurrences | Ratio | Ratio Consécutif | Points Moyens |
|---------------|-------------|-------|------------------|---------------|
| 1 bougie     | 154         | 52.9% | 52.9%           | 14.66 pts     |
| 2 bougies    | 77          | 26.5% | 50.0%           | 25.25 pts     |
| 3 bougies    | 43          | 14.8% | 55.8%           | 33.61 pts     |
| 4 bougies    | 18          | 6.2%  | 41.9%           | 50.58 pts     |
| 5 bougies    | 7           | 2.4%  | 38.9%           | 61.68 pts     |

> **Note** : Le "Ratio Consécutif" représente le pourcentage de bougies qui continuent par rapport au niveau précédent

### 📈 Observations Clés (1M)
- **Échantillon solide** : 626 bougies qualifiées au total (335 haussières + 291 baissières)
- **Probabilité stable** : ~51-53% de continuation à la 1ère bougie
- **Persistance haussière** : Les haussières montrent une meilleure persistance (64.3% arrivent à 5 bougies si elles ont 4)
- **Gain progressif** : Les points moyens triplent entre 1 et 5 bougies (15→53 pts haussier, 15→62 pts baissier)

---

## 🕔 Timeframe 5 Minutes (Seuil ≥ 80 points)

### Synthèse Globale (2018-2025)

#### Bougies Haussières
- **Total bougies 8h30 qualifiées : 28**

| Continuations | Occurrences | Ratio | Ratio Consécutif | Points Moyens |
|---------------|-------------|-------|------------------|---------------|
| 1 bougie     | 17          | 60.7% | 60.7%           | 43.87 pts     |
| 2 bougies    | 6           | 21.4% | 35.3%           | 72.27 pts     |
| 3 bougies    | 3           | 10.7% | 50.0%           | 114.77 pts    |
| 4 bougies    | 1           | 3.6%  | 33.3%           | 59.43 pts     |
| 5 bougies    | 0           | 0.0%  | 0.0%            | 0.00 pts      |

#### Bougies Baissières
- **Total bougies 8h30 qualifiées : 31**

| Continuations | Occurrences | Ratio | Ratio Consécutif | Points Moyens |
|---------------|-------------|-------|------------------|---------------|
| 1 bougie     | 18          | 58.1% | 58.1%           | 42.91 pts     |
| 2 bougies    | 10          | 32.3% | 55.6%           | 44.93 pts     |
| 3 bougies    | 4           | 12.9% | 40.0%           | 83.82 pts     |
| 4 bougies    | 1           | 3.2%  | 25.0%           | 109.34 pts    |
| 5 bougies    | 1           | 3.2%  | 100.0%          | 120.17 pts    |

### 📈 Observations Clés (5M)
- **Échantillon limité** : 59 bougies qualifiées (seuil élevé de 80 pts)
- **Forte probabilité initiale** : 60.7% haussier, 58.1% baissier pour la 1ère continuation
- **Baissières plus persistantes** : Meilleures continuations au niveau 2 (55.6% vs 35.3%)
- **Gains importants** : Jusqu'à 115 pts en moyenne après 3 bougies haussières, 120 pts après 5 baissières

---

## 🕧 Timeframe 15 Minutes (Seuil ≥ 150 points)

### Synthèse Globale (2018-2025)

#### Bougies Haussières
- **Total bougies 8h30 qualifiées : 10**

| Continuations | Occurrences | Ratio | Ratio Consécutif | Points Moyens |
|---------------|-------------|-------|------------------|---------------|
| 1 bougie     | 6           | 60.0% | 60.0%           | 86.66 pts     |
| 2 bougies    | 3           | 30.0% | 50.0%           | 161.30 pts    |
| 3 bougies    | 1           | 10.0% | 33.3%           | 136.07 pts    |
| 4 bougies    | 1           | 10.0% | 100.0%          | 146.05 pts    |
| 5 bougies    | 0           | 0.0%  | 0.0%            | 0.00 pts      |

#### Bougies Baissières
- **Total bougies 8h30 qualifiées : 22**

| Continuations | Occurrences | Ratio | Ratio Consécutif | Points Moyens |
|---------------|-------------|-------|------------------|---------------|
| 1 bougie     | 10          | 45.5% | 45.5%           | 51.69 pts     |
| 2 bougies    | 3           | 13.6% | 30.0%           | 103.03 pts    |
| 3 bougies    | 1           | 4.5%  | 33.3%           | 201.15 pts    |
| 4 bougies    | 0           | 0.0%  | 0.0%            | 0.00 pts      |
| 5 bougies    | 0           | 0.0%  | 0.0%            | 0.00 pts      |

### 📈 Observations Clés (15M)
- **Échantillon très limité** : Seulement 32 bougies qualifiées (seuil très élevé de 150 pts)
- **Biais baissier** : 22 baissières vs 10 haussières (69% baissières)
- **Haussières plus efficaces** : 60% de continuation vs 45.5% pour les baissières
- **Gains exceptionnels** : Jusqu'à 161 pts après 2 bougies haussières, 201 pts après 3 baissières

---

## 📊 Analyse Comparative par Timeframe

### Probabilité de 1ère Continuation

| Timeframe | Haussier | Baissier | Moyenne |
|-----------|----------|----------|---------|
| 1 minute  | 51.0%    | 52.9%    | 52.0%   |
| 5 minutes | 60.7%    | 58.1%    | 59.4%   |
| 15 minutes| 60.0%    | 45.5%    | 52.8%   |

### Points Moyens à la 3ème Continuation

| Timeframe | Haussier | Baissier | 
|-----------|----------|----------|
| 1 minute  | 37.34 pts| 33.61 pts|
| 5 minutes | 114.77 pts| 83.82 pts|
| 15 minutes| 136.07 pts| 201.15 pts|

### Nombre Total de Signaux Qualifiés

| Timeframe | Haussier | Baissier | Total |
|-----------|----------|----------|-------|
| 1 minute  | 335      | 291      | 626   |
| 5 minutes | 28       | 31       | 59    |
| 15 minutes| 10       | 22       | 32    |

---

## 🎯 Conclusions et Recommandations Trading

### Points Forts Identifiés

1. **Meilleur Équilibre Fréquence/Qualité** : 1 minute (≥15 pts)
   - 626 signaux sur 8 ans (≈78/an)
   - Probabilité de continuation stable (~52%)
   - Gains progressifs prévisibles

2. **Meilleure Probabilité Initiale** : 5 minutes (≥80 pts)
   - ~60% de probabilité de 1ère continuation
   - Gains substantiels (44-115 pts)
   - Échantillon modéré (59 signaux)

3. **Signal le Plus Rentable** : Bougies extrêmes 15M (≥150 pts)
   - Haussières : 60% continuation, gains jusqu'à 161 pts
   - Baissières : Potentiel de 201 pts après 3 continuations
   - ⚠️ Échantillon limité (32 signaux)

### Stratégie Suggérée

| Condition | Action | Target | Stop |
|-----------|--------|--------|------|
| 1M >= 15 pts | Scalping | 25-35 pts | 12 pts |
| 5M >= 80 pts | Day trade | 70-100 pts | 40 pts |
| 15M >= 150 pts | Swing trade | 130-160 pts | 75 pts |

### Ratio Consécutif - Interprétation

Le **ratio consécutif** est un indicateur clé pour comprendre la persistance du mouvement :
- **> 55%** : Forte tendance à continuer
- **45-55%** : Zone neutre, probabilité équilibrée
- **< 45%** : Tendance à s'essouffler

### ⚠️ Avertissements

- Les seuils élevés (80 pts 5M, 150 pts 15M) réduisent significativement le nombre de signaux
- Les performances passées ne garantissent pas les résultats futurs
- Cette analyse est basée sur des données historiques de 2018 à 2025
- Toujours utiliser une gestion de risque appropriée

---

## 📁 Annexe : Détails par Année

### Timeframe 1 Minute (≥15 pts) - Détails Annuels

| Année | Haussières | Baissières | Total |
|-------|------------|------------|-------|
| 2018  | 7          | 9          | 16    |
| 2019  | 6          | 3          | 9     |
| 2020  | 38         | 36         | 74    |
| 2021  | 49         | 39         | 88    |
| 2022  | 82         | 42         | 124   |
| 2023  | 61         | 44         | 105   |
| 2024  | 40         | 55         | 95    |
| 2025  | 52         | 63         | 115   |
| **Total** | **335** | **291**   | **626** |

### Timeframe 5 Minutes (≥80 pts) - Détails Annuels

| Année | Haussières | Baissières | Total |
|-------|------------|------------|-------|
| 2018  | 0          | 0          | 0     |
| 2019  | 0          | 0          | 0     |
| 2020  | 3          | 3          | 6     |
| 2021  | 2          | 4          | 6     |
| 2022  | 10         | 8          | 18    |
| 2023  | 3          | 1          | 4     |
| 2024  | 2          | 5          | 7     |
| 2025  | 8          | 10         | 18    |
| **Total** | **28**  | **31**    | **59** |

### Timeframe 15 Minutes (≥150 pts) - Détails Annuels

| Année | Haussières | Baissières | Total |
|-------|------------|------------|-------|
| 2018  | 0          | 0          | 0     |
| 2019  | 0          | 0          | 0     |
| 2020  | 1          | 2          | 3     |
| 2021  | 0          | 2          | 2     |
| 2022  | 5          | 6          | 11    |
| 2023  | 0          | 0          | 0     |
| 2024  | 1          | 3          | 4     |
| 2025  | 3          | 9          | 12    |
| **Total** | **10**  | **22**    | **32** |

---

*Rapport généré automatiquement par `candle_continuation_analysis.py`*  
*Seuils : 15 pts (1M), 80 pts (5M), 150 pts (15M)*  
*Données analysées : 2018-2025*

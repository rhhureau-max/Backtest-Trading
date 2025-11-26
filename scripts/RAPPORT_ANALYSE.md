# 📊 Rapport d'Analyse : Continuations de Bougies après 8h30

## 📋 Résumé Exécutif

Cette analyse étudie le comportement des bougies consécutives après une bougie significative à 8h30 (heure de New York - ouverture du marché) sur les données de 2018 à 2025.

### Méthodologie

| Timeframe | Seuil d'amplitude | Période analysée |
|-----------|-------------------|------------------|
| 1 minute  | ≥ 10 points      | 2018-2025        |
| 5 minutes | ≥ 30 points      | 2018-2025        |
| 15 minutes| ≥ 80 points      | 2018-2025        |

L'analyse compte le nombre de bougies consécutives qui continuent dans la même direction que la bougie de 8h30 (de 1 à 5 bougies).

---

## 🕐 Timeframe 1 Minute (Seuil ≥ 10 points)

### Synthèse Globale (2018-2025)

#### Bougies Haussières
- **Total bougies 8h30 qualifiées : 498**

| Continuations | Occurrences | Ratio | Ratio Consécutif | Points Moyens |
|---------------|-------------|-------|------------------|---------------|
| 1 bougie     | 260         | 52.2% | 52.2%           | 13.38 pts     |
| 2 bougies    | 148         | 29.7% | 56.9%           | 24.42 pts     |
| 3 bougies    | 77          | 15.5% | 52.0%           | 33.54 pts     |
| 4 bougies    | 41          | 8.2%  | 53.2%           | 37.23 pts     |
| 5 bougies    | 29          | 5.8%  | 70.7%           | 44.46 pts     |

#### Bougies Baissières
- **Total bougies 8h30 qualifiées : 444**

| Continuations | Occurrences | Ratio | Ratio Consécutif | Points Moyens |
|---------------|-------------|-------|------------------|---------------|
| 1 bougie     | 224         | 50.5% | 50.5%           | 14.07 pts     |
| 2 bougies    | 111         | 25.0% | 49.6%           | 24.53 pts     |
| 3 bougies    | 57          | 12.8% | 51.4%           | 33.36 pts     |
| 4 bougies    | 28          | 6.3%  | 49.1%           | 47.67 pts     |
| 5 bougies    | 10          | 2.3%  | 35.7%           | 57.08 pts     |

> **Note** : Le "Ratio Consécutif" représente le pourcentage de bougies qui continuent par rapport au niveau précédent (ex: parmi les 260 qui ont eu 1 continuation, 148 ont eu une 2ème soit 56.9%)

### 📈 Observations Clés (1M)
- **Échantillon important** : 942 bougies qualifiées au total (498 haussières + 444 baissières)
- **Probabilité stable** : ~50-52% de continuation à chaque étape
- **Persistance haussière** : Les haussières montrent une meilleure persistance (70.7% arrivent à 5 bougies si elles ont 4)
- **Gain progressif** : Les points moyens doublent environ entre 1 et 5 bougies (13→44 pts)

---

## 🕔 Timeframe 5 Minutes (Seuil ≥ 30 points)

### Synthèse Globale (2018-2025)

#### Bougies Haussières
- **Total bougies 8h30 qualifiées : 322**

| Continuations | Occurrences | Ratio | Ratio Consécutif | Points Moyens |
|---------------|-------------|-------|------------------|---------------|
| 1 bougie     | 181         | 56.2% | 56.2%           | 26.96 pts     |
| 2 bougies    | 81          | 25.2% | 44.8%           | 42.97 pts     |
| 3 bougies    | 43          | 13.4% | 53.1%           | 63.76 pts     |
| 4 bougies    | 18          | 5.6%  | 41.9%           | 77.91 pts     |
| 5 bougies    | 8           | 2.5%  | 44.4%           | 87.98 pts     |

#### Bougies Baissières
- **Total bougies 8h30 qualifiées : 328**

| Continuations | Occurrences | Ratio | Ratio Consécutif | Points Moyens |
|---------------|-------------|-------|------------------|---------------|
| 1 bougie     | 167         | 50.9% | 50.9%           | 29.49 pts     |
| 2 bougies    | 85          | 25.9% | 50.9%           | 54.39 pts     |
| 3 bougies    | 40          | 12.2% | 47.1%           | 79.84 pts     |
| 4 bougies    | 18          | 5.5%  | 45.0%           | 101.08 pts    |
| 5 bougies    | 8           | 2.4%  | 44.4%           | 106.11 pts    |

### 📈 Observations Clés (5M)
- **Équilibre parfait** : 322 haussières vs 328 baissières
- **Meilleure probabilité initiale haussière** : 56.2% vs 50.9% pour la 1ère continuation
- **Gains significatifs** : 80-100 pts atteints en moyenne après 3-4 bougies
- **Ratio consécutif stable** : ~45-50% à chaque niveau de continuation

---

## 🕧 Timeframe 15 Minutes (Seuil ≥ 80 points)

### Synthèse Globale (2018-2025)

#### Bougies Haussières
- **Total bougies 8h30 qualifiées : 101**

| Continuations | Occurrences | Ratio | Ratio Consécutif | Points Moyens |
|---------------|-------------|-------|------------------|---------------|
| 1 bougie     | 57          | 56.4% | 56.4%           | 40.54 pts     |
| 2 bougies    | 32          | 31.7% | 56.1%           | 79.83 pts     |
| 3 bougies    | 17          | 16.8% | 53.1%           | 113.01 pts    |
| 4 bougies    | 7           | 6.9%  | 41.2%           | 149.81 pts    |
| 5 bougies    | 2           | 2.0%  | 28.6%           | 80.14 pts     |

#### Bougies Baissières
- **Total bougies 8h30 qualifiées : 145**

| Continuations | Occurrences | Ratio | Ratio Consécutif | Points Moyens |
|---------------|-------------|-------|------------------|---------------|
| 1 bougie     | 66          | 45.5% | 45.5%           | 44.51 pts     |
| 2 bougies    | 36          | 24.8% | 54.5%           | 101.72 pts    |
| 3 bougies    | 16          | 11.0% | 44.4%           | 144.76 pts    |
| 4 bougies    | 12          | 8.3%  | 75.0%           | 179.32 pts    |
| 5 bougies    | 10          | 6.9%  | 83.3%           | 213.72 pts    |

### 📈 Observations Clés (15M)
- **Biais baissier prononcé** : 145 baissières vs 101 haussières (59% baissières)
- **Forte persistance baissière** : 83.3% des 4 continuations arrivent à 5 continuations
- **Gains exceptionnels baissiers** : 180-215 pts après 4-5 bougies
- **Ratio consécutif remarquable** : Les baissières montrent une accélération de continuation (45%→55%→44%→75%→83%)

---

## 📊 Analyse Comparative par Timeframe

### Probabilité de 1ère Continuation

| Timeframe | Haussier | Baissier | Moyenne |
|-----------|----------|----------|---------|
| 1 minute  | 52.2%    | 50.5%    | 51.4%   |
| 5 minutes | 56.2%    | 50.9%    | 53.6%   |
| 15 minutes| 56.4%    | 45.5%    | 51.0%   |

### Points Moyens à la 3ème Continuation

| Timeframe | Haussier | Baissier | 
|-----------|----------|----------|
| 1 minute  | 33.54 pts| 33.36 pts|
| 5 minutes | 63.76 pts| 79.84 pts|
| 15 minutes| 113.01 pts| 144.76 pts|

### Nombre Total de Signaux Qualifiés

| Timeframe | Haussier | Baissier | Total |
|-----------|----------|----------|-------|
| 1 minute  | 498      | 444      | 942   |
| 5 minutes | 322      | 328      | 650   |
| 15 minutes| 101      | 145      | 246   |

---

## 🎯 Conclusions et Recommandations Trading

### Points Forts Identifiés

1. **Meilleur Timeframe pour la Fréquence** : 1 minute
   - 942 signaux sur 8 ans (≈118/an)
   - Probabilité de continuation stable (~50%)
   - Gains modérés mais réguliers

2. **Meilleur Équilibre** : 5 minutes
   - 650 signaux (≈81/an)
   - Bonne probabilité haussière (56.2%)
   - Gains significatifs (80-100 pts après 3-4 bougies)

3. **Signal le Plus Profitable** : Bougie baissière de 80+ pts à 8h30 en 15M
   - Ratio consécutif exceptionnel après 3 bougies (75%→83%)
   - Potentiel de 180-215 pts si la continuation persiste
   - Momentum baissier auto-entretenu

### Stratégie Suggérée

| Condition | Action | Target | Stop |
|-----------|--------|--------|------|
| 1M >= 10 pts | Scalping | 15-25 pts | 8 pts |
| 5M >= 30 pts | Day trade | 45-65 pts | 20 pts |
| 15M >= 80 pts | Swing trade | 100-150 pts | 40 pts |

### Ratio Consécutif - Interprétation

Le **ratio consécutif** est un indicateur clé pour comprendre la persistance du mouvement :
- **> 55%** : Forte tendance à continuer
- **45-55%** : Zone neutre, probabilité équilibrée
- **< 45%** : Tendance à s'essouffler

### ⚠️ Avertissements

- Les performances passées ne garantissent pas les résultats futurs
- Cette analyse est basée sur des données historiques de 2018 à 2025
- Les conditions de marché peuvent varier significativement
- Toujours utiliser une gestion de risque appropriée

---

## 📁 Annexe : Détails par Année

### Timeframe 1 Minute (≥10 pts) - Détails Annuels

| Année | Haussières | Baissières | Total |
|-------|------------|------------|-------|
| 2018  | 22         | 23         | 45    |
| 2019  | 21         | 13         | 34    |
| 2020  | 62         | 54         | 116   |
| 2021  | 78         | 61         | 139   |
| 2022  | 102        | 63         | 165   |
| 2023  | 83         | 66         | 149   |
| 2024  | 61         | 85         | 146   |
| 2025  | 69         | 79         | 148   |
| **Total** | **498** | **444**   | **942** |

### Timeframe 5 Minutes (≥30 pts) - Détails Annuels

| Année | Haussières | Baissières | Total |
|-------|------------|------------|-------|
| 2018  | 11         | 4          | 15    |
| 2019  | 10         | 6          | 16    |
| 2020  | 34         | 45         | 79    |
| 2021  | 41         | 37         | 78    |
| 2022  | 68         | 71         | 139   |
| 2023  | 52         | 32         | 84    |
| 2024  | 47         | 56         | 103   |
| 2025  | 54         | 63         | 117   |
| **Total** | **322** | **328**   | **650** |

### Timeframe 15 Minutes (≥80 pts) - Détails Annuels

| Année | Haussières | Baissières | Total |
|-------|------------|------------|-------|
| 2018  | 3          | 1          | 4     |
| 2019  | 0          | 0          | 0     |
| 2020  | 10         | 18         | 28    |
| 2021  | 16         | 17         | 33    |
| 2022  | 31         | 41         | 72    |
| 2023  | 6          | 14         | 20    |
| 2024  | 12         | 25         | 37    |
| 2025  | 23         | 29         | 52    |
| **Total** | **101** | **145**   | **246** |

---

*Rapport généré automatiquement par `candle_continuation_analysis.py`*  
*Seuils : 10 pts (1M), 30 pts (5M), 80 pts (15M)*  
*Données analysées : 2018-2025*

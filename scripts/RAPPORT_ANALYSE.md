# 📊 Rapport d'Analyse : Continuations de Bougies après 8h30

## 📋 Résumé Exécutif

Cette analyse étudie le comportement des bougies consécutives après une bougie significative à 8h30 (heure de New York - ouverture du marché) sur les données de 2018 à 2025.

### Méthodologie

| Timeframe | Seuil d'amplitude | Période analysée |
|-----------|-------------------|------------------|
| 1 minute  | ≥ 20 points      | 2018-2025        |
| 5 minutes | ≥ 50 points      | 2018-2025        |
| 15 minutes| ≥ 100 points     | 2018-2025        |

L'analyse compte le nombre de bougies consécutives qui continuent dans la même direction que la bougie de 8h30 (de 1 à 5 bougies).

---

## 🕐 Timeframe 1 Minute (Seuil ≥ 20 points)

### Synthèse Globale (2018-2025)

#### Bougies Haussières
- **Total bougies 8h30 qualifiées : 225**

| Continuations | Occurrences | Ratio | Points Moyens |
|---------------|-------------|-------|---------------|
| 1 bougie     | 115         | 51.1% | 15.32 pts     |
| 2 bougies    | 65          | 28.9% | 28.91 pts     |
| 3 bougies    | 36          | 16.0% | 40.69 pts     |
| 4 bougies    | 18          | 8.0%  | 42.97 pts     |
| 5 bougies    | 12          | 5.3%  | 54.78 pts     |

#### Bougies Baissières
- **Total bougies 8h30 qualifiées : 186**

| Continuations | Occurrences | Ratio | Points Moyens |
|---------------|-------------|-------|---------------|
| 1 bougie     | 97          | 52.2% | 16.60 pts     |
| 2 bougies    | 44          | 23.7% | 26.57 pts     |
| 3 bougies    | 24          | 12.9% | 36.54 pts     |
| 4 bougies    | 10          | 5.4%  | 51.50 pts     |
| 5 bougies    | 5           | 2.7%  | 60.23 pts     |

### 📈 Observations Clés (1M)
- **Probabilité de continuation** : ~51% pour la première bougie suivante
- **Décroissance progressive** : Le ratio diminue d'environ 50% à chaque bougie supplémentaire
- **Gain moyen progressif** : Les points moyens augmentent linéairement (≈15 pts par bougie de continuation)
- **Symétrie haussier/baissier** : Comportement très similaire entre les deux directions

---

## 🕔 Timeframe 5 Minutes (Seuil ≥ 50 points)

### Synthèse Globale (2018-2025)

#### Bougies Haussières
- **Total bougies 8h30 qualifiées : 111**

| Continuations | Occurrences | Ratio | Points Moyens |
|---------------|-------------|-------|---------------|
| 1 bougie     | 68          | 61.3% | 32.99 pts     |
| 2 bougies    | 18          | 16.2% | 51.35 pts     |
| 3 bougies    | 9           | 8.1%  | 84.24 pts     |
| 4 bougies    | 4           | 3.6%  | 116.91 pts    |
| 5 bougies    | 1           | 0.9%  | 151.77 pts    |

#### Bougies Baissières
- **Total bougies 8h30 qualifiées : 133**

| Continuations | Occurrences | Ratio | Points Moyens |
|---------------|-------------|-------|---------------|
| 1 bougie     | 77          | 57.9% | 33.95 pts     |
| 2 bougies    | 41          | 30.8% | 58.85 pts     |
| 3 bougies    | 18          | 13.5% | 91.91 pts     |
| 4 bougies    | 6           | 4.5%  | 138.85 pts    |
| 5 bougies    | 2           | 1.5%  | 120.37 pts    |

### 📈 Observations Clés (5M)
- **Probabilité plus élevée** : ~60% pour la première continuation (vs 51% en 1M)
- **Biais baissier** : Plus de bougies baissières qualifiées (133 vs 111)
- **Meilleure continuation baissière** : 30.8% pour 2 bougies (vs 16.2% haussier)
- **Gain substantiel** : Les mouvements atteignent facilement 80-140 pts après 3-4 bougies

---

## 🕧 Timeframe 15 Minutes (Seuil ≥ 100 points)

### Synthèse Globale (2018-2025)

#### Bougies Haussières
- **Total bougies 8h30 qualifiées : 50**

| Continuations | Occurrences | Ratio | Points Moyens |
|---------------|-------------|-------|---------------|
| 1 bougie     | 28          | 56.0% | 46.12 pts     |
| 2 bougies    | 11          | 22.0% | 95.11 pts     |
| 3 bougies    | 5           | 10.0% | 119.89 pts    |
| 4 bougies    | 3           | 6.0%  | 138.47 pts    |
| 5 bougies    | 1           | 2.0%  | 96.22 pts     |

#### Bougies Baissières
- **Total bougies 8h30 qualifiées : 82**

| Continuations | Occurrences | Ratio | Points Moyens |
|---------------|-------------|-------|---------------|
| 1 bougie     | 37          | 45.1% | 50.68 pts     |
| 2 bougies    | 18          | 22.0% | 112.44 pts    |
| 3 bougies    | 7           | 8.5%  | 174.79 pts    |
| 4 bougies    | 5           | 6.1%  | 209.26 pts    |
| 5 bougies    | 5           | 6.1%  | 226.29 pts    |

### 📈 Observations Clés (15M)
- **Forte asymétrie** : 82 baissières vs 50 haussières (biais baissier de 64%)
- **Gains importants** : Les continuations baissières atteignent 200+ pts après 4-5 bougies
- **Persistance baissière** : Les mouvements baissiers continuent plus longtemps (6.1% atteignent 5 bougies vs 2% haussier)
- **Opportunité majeure** : Les bougies baissières de 100+ pts à 8h30 offrent le meilleur potentiel de continuation

---

## 📊 Analyse Comparative par Timeframe

### Probabilité de 1ère Continuation

| Timeframe | Haussier | Baissier | Moyenne |
|-----------|----------|----------|---------|
| 1 minute  | 51.1%    | 52.2%    | 51.7%   |
| 5 minutes | 61.3%    | 57.9%    | 59.6%   |
| 15 minutes| 56.0%    | 45.1%    | 50.6%   |

### Points Moyens à la 3ème Continuation

| Timeframe | Haussier | Baissier | 
|-----------|----------|----------|
| 1 minute  | 40.69 pts| 36.54 pts|
| 5 minutes | 84.24 pts| 91.91 pts|
| 15 minutes| 119.89 pts| 174.79 pts|

---

## 🎯 Conclusions et Recommandations Trading

### Points Forts Identifiés

1. **Meilleur Timeframe pour le Trading** : 5 minutes
   - Probabilité de continuation élevée (~60%)
   - Bon équilibre entre fréquence des signaux et amplitude des mouvements

2. **Signal le Plus Fiable** : Bougie baissière de 50+ pts à 8h30 en 5M
   - 57.9% de chance de continuation immédiate
   - 30.8% de chance d'avoir 2 bougies consécutives dans la même direction
   - Potentiel de 50-90 pts de gain

3. **Signal le Plus Profitable** : Bougie baissière de 100+ pts à 8h30 en 15M
   - Potentiel de 175-225 pts si la continuation atteint 3-5 bougies
   - Risque/Récompense favorable malgré une probabilité plus faible

### Stratégie Suggérée

| Condition | Action | Target | Stop |
|-----------|--------|--------|------|
| 1M >= 20 pts | Trade court terme | 15-30 pts | 10 pts |
| 5M >= 50 pts | Trade moyen terme | 50-80 pts | 25 pts |
| 15M >= 100 pts | Position swing | 100-150 pts | 50 pts |

### ⚠️ Avertissements

- Les performances passées ne garantissent pas les résultats futurs
- Cette analyse est basée sur des données historiques de 2018 à 2025
- Les conditions de marché peuvent varier significativement
- Toujours utiliser une gestion de risque appropriée

---

## 📁 Annexe : Détails par Année

### Timeframe 1 Minute - Détails Annuels

| Année | Haussières | Baissières | Total |
|-------|------------|------------|-------|
| 2018  | 3          | 4          | 7     |
| 2019  | 1          | 0          | 1     |
| 2020  | 26         | 18         | 44    |
| 2021  | 32         | 21         | 53    |
| 2022  | 62         | 27         | 89    |
| 2023  | 40         | 28         | 68    |
| 2024  | 24         | 36         | 60    |
| 2025  | 37         | 52         | 89    |

### Timeframe 5 Minutes - Détails Annuels

| Année | Haussières | Baissières | Total |
|-------|------------|------------|-------|
| 2018  | 2          | 0          | 2     |
| 2019  | 0          | 0          | 0     |
| 2020  | 13         | 16         | 29    |
| 2021  | 13         | 14         | 27    |
| 2022  | 41         | 39         | 80    |
| 2023  | 13         | 10         | 23    |
| 2024  | 8          | 24         | 32    |
| 2025  | 21         | 30         | 51    |

### Timeframe 15 Minutes - Détails Annuels

| Année | Haussières | Baissières | Total |
|-------|------------|------------|-------|
| 2018  | 1          | 0          | 1     |
| 2019  | 0          | 0          | 0     |
| 2020  | 5          | 10         | 15    |
| 2021  | 6          | 11         | 17    |
| 2022  | 22         | 22         | 44    |
| 2023  | 1          | 6          | 7     |
| 2024  | 3          | 12         | 15    |
| 2025  | 12         | 21         | 33    |

---

*Rapport généré automatiquement par `candle_continuation_analysis.py`*  
*Données analysées : 2018-2025*

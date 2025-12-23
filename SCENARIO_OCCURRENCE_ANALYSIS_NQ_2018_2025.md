# SCENARIO OCCURRENCE ANALYSIS - NQ 2018-2025

**PURE STATISTICAL ANALYSIS - Pattern Frequency Detection**

*This is NOT a trading backtest. This analysis counts how often specific patterns occur in historical data.*

---

## 1. VUE D'ENSEMBLE

**Période Analysée:** 2018-01-01 à 2025-11-11

**Nombre Total de Jours de Trading:** 1627

**Années Couvertes:** 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025

### Résumé des 3 Scénarios Analysés

| Scénario | Description | Critère de Détection |
|----------|-------------|---------------------|
| **1. COMPRESSION** | Range asiatique étroit | Range < 40 points |
| **2. EXPANSION** | Range asiatique large avec tendance | Range > 60 points + mouvement directionnel |
| **3. CONTINUATION** | Cassure de structure pendant Tokyo | Break de high/low H4 significatif |

**Session Tokyo:** 20h00-00h00 (heure NY)

**Session Londres:** 02h00-05h00 (heure NY)

---

## 2. RÉSULTATS PAR SCÉNARIO

### 🔵 SCÉNARIO 1: LA COMPRESSION

**Condition:** Range asiatique < 40 points

- **Nombre d'occurrences:** 736
- **Pourcentage du total:** 45.24%
- **Range moyen quand détecté:** 26.15 points
- **Range médian quand détecté:** 26.03 points

#### Distribution par Année

| Année | Occurrences | % de l'année |
|-------|-------------|--------------|
| 2018 | 154 | 74.76% |
| 2019 | 175 | 84.95% |
| 2020 | 44 | 21.26% |
| 2021 | 77 | 37.20% |
| 2022 | 37 | 17.87% |
| 2023 | 126 | 60.58% |
| 2024 | 96 | 46.38% |
| 2025 | 27 | 15.08% |

#### Distribution par Mois

| Mois | Occurrences | % du mois |
|------|-------------|-----------|
| Janvier | 74 | 51.39% |
| Février | 63 | 48.84% |
| Mars | 48 | 34.78% |
| Avril | 61 | 45.52% |
| Mai | 60 | 42.25% |
| Juin | 70 | 51.47% |
| Juillet | 65 | 45.45% |
| Août | 58 | 41.13% |
| Septembre | 54 | 39.42% |
| Octobre | 53 | 37.06% |
| Novembre | 59 | 46.83% |
| Décembre | 71 | 62.28% |

#### Distribution par Jour de la Semaine

| Jour | Occurrences | % du jour |
|------|-------------|-----------|
| Lundi | 193 | 47.19% |
| Mardi | 202 | 49.63% |
| Mercredi | 165 | 40.24% |
| Jeudi | 176 | 43.89% |

**Graphique:** Voir `annual_scenario_frequency.png` et `monthly_scenario_frequency.png`

---

### 🟠 SCÉNARIO 2: L'EXPANSION

**Condition:** Range asiatique > 60 points avec tendance directionnelle

- **Nombre d'occurrences:** 59
- **Pourcentage du total:** 3.63%
- **Range moyen quand détecté:** 115.48 points
- **Range médian quand détecté:** 89.04 points

#### Distribution par Année

| Année | Occurrences | % de l'année |
|-------|-------------|--------------|
| 2018 | 2 | 0.97% |
| 2019 | 4 | 1.94% |
| 2020 | 6 | 2.90% |
| 2021 | 8 | 3.86% |
| 2022 | 13 | 6.28% |
| 2023 | 6 | 2.88% |
| 2024 | 8 | 3.86% |
| 2025 | 12 | 6.70% |

#### Distribution par Mois

| Mois | Occurrences | % du mois |
|------|-------------|-----------|
| Janvier | 9 | 6.25% |
| Février | 5 | 3.88% |
| Mars | 6 | 4.35% |
| Avril | 6 | 4.48% |
| Mai | 3 | 2.11% |
| Juin | 8 | 5.88% |
| Juillet | 2 | 1.40% |
| Août | 5 | 3.55% |
| Septembre | 6 | 4.38% |
| Octobre | 3 | 2.10% |
| Novembre | 2 | 1.59% |
| Décembre | 4 | 3.51% |

#### Distribution par Jour de la Semaine

| Jour | Occurrences | % du jour |
|------|-------------|-----------|
| Lundi | 18 | 4.40% |
| Mardi | 9 | 2.21% |
| Mercredi | 18 | 4.39% |
| Jeudi | 14 | 3.49% |

**Graphique:** Voir `annual_scenario_frequency.png` et `monthly_scenario_frequency.png`

---

### 🟢 SCÉNARIO 3: LA CONTINUATION

**Condition:** Tokyo casse un niveau de structure H4 ou D1 important

- **Nombre d'occurrences:** 544
- **Pourcentage du total:** 33.44%
- **Range moyen quand détecté:** 63.51 points
- **Range médian quand détecté:** 45.98 points

**Critère de détection:**
- Break du high/low H4 des 5 jours précédents avec marge de > 10 points

#### Distribution par Année

| Année | Occurrences | % de l'année |
|-------|-------------|--------------|
| 2018 | 60 | 29.13% |
| 2019 | 64 | 31.07% |
| 2020 | 81 | 39.13% |
| 2021 | 71 | 34.30% |
| 2022 | 69 | 33.33% |
| 2023 | 64 | 30.77% |
| 2024 | 74 | 35.75% |
| 2025 | 61 | 34.08% |

#### Distribution par Mois

| Mois | Occurrences | % du mois |
|------|-------------|-----------|
| Janvier | 51 | 35.42% |
| Février | 40 | 31.01% |
| Mars | 39 | 28.26% |
| Avril | 43 | 32.09% |
| Mai | 41 | 28.87% |
| Juin | 52 | 38.24% |
| Juillet | 50 | 34.97% |
| Août | 56 | 39.72% |
| Septembre | 41 | 29.93% |
| Octobre | 45 | 31.47% |
| Novembre | 44 | 34.92% |
| Décembre | 42 | 36.84% |

#### Distribution par Jour de la Semaine

| Jour | Occurrences | % du jour |
|------|-------------|-----------|
| Lundi | 130 | 31.78% |
| Mardi | 119 | 29.24% |
| Mercredi | 150 | 36.59% |
| Jeudi | 145 | 36.16% |

**Graphique:** Voir `annual_scenario_frequency.png` et `monthly_scenario_frequency.png`

---

## 3. ANALYSE CROISÉE

### Co-occurrence des Scénarios

| Nombre de Scénarios | Jours | Pourcentage |
|---------------------|-------|-------------|
| 0 scénario | 550 | 33.80% |
| 1 scénario | 815 | 50.09% |
| 2 scénarios | 262 | 16.10% |
| 3 scénarios | 0 | 0.00% |

### Matrice de Co-occurrence

Nombre de jours où deux scénarios se produisent simultanément:

| Combinaison | Occurrences |
|-------------|-------------|
| Compression + Expansion | 0 |
| Compression + Continuation | 236 |
| Expansion + Continuation | 26 |

*Note: Il est théoriquement impossible d'avoir Compression (< 40 pts) ET Expansion (> 60 pts) simultanément. Les rares cas détectés sont dus à l'arrondi ou aux critères additionnels.*

---

## 4. PATTERNS TEMPORELS

### Évolution Annuelle

| Année | S1: Compression | S2: Expansion | S3: Continuation | Jours Totaux |
|-------|----------------|---------------|------------------|--------------|
| 2018 | 154 (74.8%) | 2 (1.0%) | 60 (29.1%) | 206 |
| 2019 | 175 (85.0%) | 4 (1.9%) | 64 (31.1%) | 206 |
| 2020 | 44 (21.3%) | 6 (2.9%) | 81 (39.1%) | 207 |
| 2021 | 77 (37.2%) | 8 (3.9%) | 71 (34.3%) | 207 |
| 2022 | 37 (17.9%) | 13 (6.3%) | 69 (33.3%) | 207 |
| 2023 | 126 (60.6%) | 6 (2.9%) | 64 (30.8%) | 208 |
| 2024 | 96 (46.4%) | 8 (3.9%) | 74 (35.7%) | 207 |
| 2025 | 27 (15.1%) | 12 (6.7%) | 61 (34.1%) | 179 |

### Jours de la Semaine les Plus Fréquents

| Jour | S1: Compression | S2: Expansion | S3: Continuation |
|------|----------------|---------------|------------------|
| Lundi | 193 (47.2%) | 18 (4.4%) | 130 (31.8%) |
| Mardi | 202 (49.6%) | 9 (2.2%) | 119 (29.2%) |
| Mercredi | 165 (40.2%) | 18 (4.4%) | 150 (36.6%) |
| Jeudi | 176 (43.9%) | 14 (3.5%) | 145 (36.2%) |

### Observations sur les Clusters Temporels

*Analyser les graphiques pour identifier des patterns saisonniers:*

- **Compressions:** Vérifier si plus fréquentes en été (juillet-août) lors de faible volatilité
- **Expansions:** Potentiellement plus fréquentes en début/fin de mois ou lors d'annonces macro
- **Continuations:** Possiblement corrélées aux périodes de forte volatilité (début de trimestre)

**Graphiques associés:**
- `monthly_scenario_frequency.png` - Distribution mensuelle
- `annual_scenario_frequency.png` - Évolution annuelle
- `day_of_week_scenario_frequency.png` - Répartition par jour de semaine

---

## 5. STATISTIQUES DESCRIPTIVES

### Range Asiatique - Statistiques Globales

| Métrique | Valeur |
|----------|--------|
| Moyenne | 57.29 points |
| Médiane | 43.50 points |
| Écart-type | 49.71 points |
| Minimum | 5.99 points |
| Maximum | 522.03 points |
| 25ème percentile | 27.42 points |
| 50ème percentile (Médiane) | 43.50 points |
| 75ème percentile | 68.48 points |

### Seuils Utilisés vs Réalité des Données

| Seuil | Valeur | Pourcentage des Jours |
|-------|--------|----------------------|
| Range < 40 pts (Compression) | < 40 | 45.24% |
| Range entre 40-60 pts | 40-60 | 21.94% |
| Range > 60 pts (Expansion) | > 60 | 32.82% |

### Distribution des Ranges (Histogramme)

Voir le graphique `asian_range_distribution.png` pour la distribution complète.

**Interprétation:**

- La majorité des jours (21.94%) présentent un range entre 40 et 60 points
- Les compressions (< 40 pts) représentent 45.24% des jours
- Les expansions (> 60 pts) représentent 32.82% des jours

---

## 6. CONCLUSION

### Synthèse des Résultats (sur 1627 jours de trading)

| Scénario | Occurrences | Fréquence | Caractéristique |
|----------|-------------|-----------|-----------------|
| 🔵 **COMPRESSION** | 736 | 45.24% | Setup principal le plus fréquent |
| 🟠 **EXPANSION** | 59 | 3.63% | Setup modéré, nécessite vigilance |
| 🟢 **CONTINUATION** | 544 | 33.44% | Setup rare mais haute qualité |

### Points Clés

1. **Pattern le plus fréquent:** Scénario 1 (Compression) avec 45.24% des jours
2. **Jours sans scénario clair:** 33.80% des jours ne correspondent à aucun des 3 scénarios
3. **Range asiatique typique:** 43.50 points (médiane)
4. **Années les plus volatiles:** Analyser les années avec plus d'expansions dans les graphiques

### Recommandations pour l'Utilisation

Ces statistiques de fréquence permettent de:

- **Comprendre la probabilité a priori** de chaque setup avant l'ouverture de Londres
- **Identifier les périodes favorables** (mois, jours de semaine) pour chaque scénario
- **Calibrer les attentes** : ne pas forcer un trade si aucun scénario n'est présent
- **Adapter la stratégie** selon la saisonnalité observée

---

## 📊 GRAPHIQUES GÉNÉRÉS

1. **`asian_range_distribution.png`** - Distribution des ranges asiatiques (histogramme)
2. **`annual_scenario_frequency.png`** - Fréquence annuelle de chaque scénario
3. **`monthly_scenario_frequency.png`** - Fréquence mensuelle de chaque scénario
4. **`day_of_week_scenario_frequency.png`** - Répartition par jour de la semaine

---

*Rapport généré le 2025-12-23 17:06:48*

*Analyse réalisée avec Python - pandas, numpy, matplotlib, seaborn*

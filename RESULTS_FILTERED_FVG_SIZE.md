# NY Opening FVG Backtest - Filtered by Size

## Vue d'ensemble

Ce backtest teste TOUS les FVGs trouvés dans la fenêtre 08:30-09:00, avec filtrage par taille:
- **< 15 points**: FVGs de taille inférieure à 15 points
- **< 10 points**: FVGs de taille inférieure à 10 points

Pour chaque filtre de taille, on teste les niveaux de take profit de 1R, 1.5R et 2R.

## Données analysées
- **Période:** 2018-2025
- **Jours de trading:** 2,450

---

## 📊 Résultats: FVG < 15 Points

### Statistiques Générales
- **FVGs détectés:** 10,513
- **Trades exécutés:** 9,392
- **Taille moyenne FVG:** 2.81 points

### Résultats par niveau RR

| Métrique | 1.0R | 1.5R | 2.0R |
|----------|------|------|------|
| **Total Trades** | 9,392 | 9,392 | 9,392 |
| **Win Rate** | 49.57% | 39.31% | 33.19% |
| **TP Hit Rate** | 49.47% | 39.16% | 32.84% |
| **Total PnL (pts)** | -1,893.12 | -2,440.43 | -2,171.24 |
| **Avg PnL (pts)** | -0.20 | -0.26 | -0.23 |
| **Expectancy (pts)** | -0.20 | -0.26 | -0.23 |
| **Trade Gagnant Moyen** | +10.38 pts | +15.60 pts | +20.53 pts |
| **Trade Perdant Moyen** | -10.60 pts | -10.53 pts | -10.54 pts |
| **Profit Factor** | 0.96 | 0.96 | **0.97** |
| **Max Drawdown** | -3,224.93 pts | -3,129.99 pts | **-3,058.96 pts** |
| **Long Trades** | 4,475 (49.43%) | 4,475 (39.17%) | 4,475 (33.09%) |
| **Short Trades** | 4,917 (49.71%) | 4,917 (39.43%) | 4,917 (33.27%) |

### 🏆 Meilleur Performer (< 15 pts)
- **Best Win Rate:** 1.0R (49.57%)
- **Best Total PnL:** 1.0R (-1,893.12 pts)
- **Best Expectancy:** 1.0R (-0.20 pts)
- **Best Profit Factor:** 2.0R (0.97)

---

## 📊 Résultats: FVG < 10 Points

### Statistiques Générales
- **FVGs détectés:** 10,119
- **Trades exécutés:** 9,071
- **Taille moyenne FVG:** 2.49 points

### Résultats par niveau RR

| Métrique | 1.0R | 1.5R | 2.0R |
|----------|------|------|------|
| **Total Trades** | 9,071 | 9,071 | 9,071 |
| **Win Rate** | 49.58% | 39.25% | 33.09% |
| **TP Hit Rate** | 49.47% | 39.09% | 32.73% |
| **Total PnL (pts)** | -1,678.76 | -2,202.78 | -2,086.50 |
| **Avg PnL (pts)** | -0.19 | -0.24 | -0.23 |
| **Expectancy (pts)** | -0.19 | -0.24 | -0.23 |
| **Trade Gagnant Moyen** | +10.12 pts | +15.24 pts | +20.04 pts |
| **Trade Perdant Moyen** | -10.32 pts | -10.24 pts | -10.26 pts |
| **Profit Factor** | 0.96 | 0.96 | **0.97** |
| **Max Drawdown** | -3,038.39 pts | -3,039.81 pts | **-3,087.50 pts** |
| **Long Trades** | 4,319 (49.36%) | 4,319 (39.08%) | 4,319 (32.92%) |
| **Short Trades** | 4,752 (49.77%) | 4,752 (39.39%) | 4,752 (33.25%) |

### 🏆 Meilleur Performer (< 10 pts)
- **Best Win Rate:** 1.0R (49.58%)
- **Best Total PnL:** 1.0R (-1,678.76 pts)
- **Best Expectancy:** 1.0R (-0.19 pts)
- **Best Profit Factor:** 2.0R (0.97)

---

## 🔍 Comparaison Entre Filtres

### Impact du Filtrage par Taille

| Métrique | < 15 pts (meilleur RR) | < 10 pts (meilleur RR) | Différence |
|----------|------------------------|------------------------|------------|
| **FVGs Détectés** | 10,513 | 10,119 | -394 (-3.7%) |
| **Trades Exécutés** | 9,392 | 9,071 | -321 (-3.4%) |
| **Meilleur RR Level** | 2.0R | 2.0R | - |
| **Meilleur Win Rate** | 49.57% (1.0R) | 49.58% (1.0R) | +0.01% |
| **Meilleur Total PnL** | -1,893.12 pts (1.0R) | -1,678.76 pts (1.0R) | **+214.36 pts** |
| **Meilleur Expectancy** | -0.20 pts (1.0R) | -0.19 pts (1.0R) | **+0.01 pts** |
| **Meilleur Profit Factor** | 0.97 (2.0R) | 0.97 (2.0R) | Égal |
| **Taille Moyenne FVG** | 2.81 pts | 2.49 pts | -0.32 pts |

### 📊 Meilleurs Résultats par Filtre

| Filtre | RR | Trades | Win Rate | Total PnL | Profit Factor |
|--------|----|---------:|----------:|-----------:|---------------:|
| **< 15 pts** | 2.0R | 9,392 | 33.19% | -2,171.24 pts | 0.97 |
| **< 10 pts** | 2.0R | 9,071 | 33.09% | -2,086.50 pts | 0.97 |

---

## 📈 Observations Clés

### 1. Impact du Filtrage < 10 pts vs < 15 pts

✅ **Avantages du filtre < 10 pts:**
- Légèrement meilleure expectancy: -0.19 vs -0.20 pts avec 1.0R
- Meilleur total PnL avec 1.0R: -1,678.76 vs -1,893.12 pts (+214 pts)
- Taille moyenne de FVG plus petite: 2.49 vs 2.81 pts
- Trades légèrement plus fiables sur les petits mouvements

⚠️ **Inconvénients:**
- Moins de trades: 9,071 vs 9,392 (-3.4%)
- Performance similaire globale (PF identique: 0.97)
- Win rates très proches sur tous les RR

### 2. Comparaison avec les FVGs Non-Filtrés

**Rappel des résultats ALL FVGs (sans filtre de taille):**
- Trades: 9,571
- Best PF: 0.97 (2.0R)
- Total PnL: -2,326.56 pts (2.0R)

**Avec filtre < 10 pts:**
- Trades: 9,071 (-5.2%)
- Best PF: 0.97 (2.0R) - identique
- Total PnL: -2,086.50 pts (2.0R) - **meilleur de 240 pts**

**Conclusion:** Le filtrage < 10 pts améliore légèrement les résultats mais la différence reste marginale.

### 3. Consistance des Résultats

- Les profit factors sont identiques (0.97) pour 2.0R sur tous les filtres
- Le pattern win rate décroissant est cohérent: 49-50% (1R) → 39-40% (1.5R) → 33% (2R)
- Long vs Short: performance équilibrée sur tous les filtres

### 4. Taille Moyenne des FVGs

- **< 15 pts:** Taille moyenne 2.81 points
- **< 10 pts:** Taille moyenne 2.49 points
- La plupart des FVGs sont déjà petits (< 5 pts en moyenne)
- Le filtrage élimine principalement les outliers (FVGs > 10 ou > 15 pts)

---

## 🎯 Recommandations

### Meilleure Configuration Globale

**Configuration Recommandée:**
- **Filtre de Taille:** < 10 points
- **RR Level:** 1.0R (pour maximiser win rate et minimiser les pertes)
- **Expectancy:** -0.19 points par trade
- **Total PnL:** -1,678.76 points sur 2018-2025

**Raisons:**
1. ✅ Meilleur total PnL (-1,678 pts vs -1,893 pts avec < 15)
2. ✅ Meilleure expectancy (-0.19 vs -0.20)
3. ✅ Win rate le plus élevé (49.58%)
4. ✅ FVGs plus "propres" (taille moyenne 2.49 pts)

### Pour Améliorer la Stratégie

La stratégie reste légèrement négative sur tous les filtres. Pour améliorer:

1. **Filtrage supplémentaire:**
   - Contexte de marché (tendance, volatilité)
   - Volume au moment du FVG
   - Position du FVG dans la session
   - Confluence avec d'autres niveaux (support/résistance)

2. **Optimisation de l'entrée:**
   - Attendre une confirmation (retest, volume)
   - Entrée partielle ou à limite
   - Éviter les FVGs formés dans les premières minutes (08:30-08:35)

3. **Gestion du risque:**
   - SL plus serré pour les petits FVGs
   - Trailing stop après TP1
   - Break-even après 0.5R

4. **Sélection temporelle:**
   - Analyser la performance par jour de la semaine
   - Éviter certaines sessions (faible volume, high impact news)

---

## 📁 Fichiers Générés

### FVG < 15 points
- `ny_opening_fvg_filtered_15.0pts_1.0R_results.csv`
- `ny_opening_fvg_filtered_15.0pts_1.5R_results.csv`
- `ny_opening_fvg_filtered_15.0pts_2.0R_results.csv`

### FVG < 10 points
- `ny_opening_fvg_filtered_10.0pts_1.0R_results.csv`
- `ny_opening_fvg_filtered_10.0pts_1.5R_results.csv`
- `ny_opening_fvg_filtered_10.0pts_2.0R_results.csv`

## 🔧 Exécution du Script

```bash
python3 ny_opening_fvg_filtered_backtest.py
```

Le script:
1. Charge automatiquement toutes les données 2018-2025
2. Teste avec filtre < 15 points pour 1R, 1.5R, 2R
3. Teste avec filtre < 10 points pour 1R, 1.5R, 2R
4. Génère les statistiques comparatives
5. Sauvegarde les résultats en CSV

---

**Date de génération:** 2025-12-09
**Script:** `ny_opening_fvg_filtered_backtest.py`

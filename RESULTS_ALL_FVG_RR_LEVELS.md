# NY Opening FVG Backtest - ALL FVGs, Multiple RR Levels

## Vue d'ensemble

Ce backtest teste **TOUS les FVGs** trouvés dans la fenêtre 08:30-09:00 (pas seulement le premier) avec des niveaux de take profit séparés de 1R, 1.5R et 2R.

## Données analysées
- **Période:** 2018-2025
- **Jours de trading:** 2,450
- **Jours avec FVGs:** 1,957 (79.88%)
- **Total FVGs détectés:** 10,748
- **Trades exécutés:** 9,571

## Résultats par niveau RR

### 📊 1.0R Take Profit

| Métrique | Valeur |
|----------|--------|
| **Total Trades** | 9,571 |
| **Trades Gagnants** | 4,738 (49.50%) |
| **Trades Perdants** | 4,833 (50.50%) |
| **TP Hit Rate** | 49.40% |
| **SL Hit** | 4,829 |
| **Total PnL** | -2,345.01 points |
| **PnL Moyen** | -0.25 points |
| **Expectancy** | -0.25 points |
| **Trade Gagnant Moyen** | +10.68 points |
| **Trade Perdant Moyen** | -10.96 points |
| **Gross Profit** | 50,621.26 points |
| **Gross Loss** | -52,966.26 points |
| **Profit Factor** | 0.96 |
| **Max Drawdown** | -3,652.01 points |
| **Risque Moyen** | 10.85 points |
| **Long Trades** | 4,564 (WR: 49.32%) |
| **Short Trades** | 5,007 (WR: 49.67%) |

---

### 📊 1.5R Take Profit

| Métrique | Valeur |
|----------|--------|
| **Total Trades** | 9,571 |
| **Trades Gagnants** | 3,757 (39.25%) |
| **Trades Perdants** | 5,814 (60.75%) |
| **TP Hit Rate** | 39.11% |
| **SL Hit** | 5,810 |
| **Total PnL** | -2,867.82 points |
| **PnL Moyen** | -0.30 points |
| **Expectancy** | -0.30 points |
| **Trade Gagnant Moyen** | +16.07 points |
| **Trade Perdant Moyen** | -10.88 points |
| **Gross Profit** | 60,361.19 points |
| **Gross Loss** | -63,229.00 points |
| **Profit Factor** | 0.95 |
| **Max Drawdown** | -3,526.62 points |
| **Risque Moyen** | 10.85 points |
| **Long Trades** | 4,564 (WR: 39.09%) |
| **Short Trades** | 5,007 (WR: 39.40%) |

---

### 📊 2.0R Take Profit

| Métrique | Valeur |
|----------|--------|
| **Total Trades** | 9,571 |
| **Trades Gagnants** | 3,175 (33.17%) |
| **Trades Perdants** | 6,396 (66.83%) |
| **TP Hit Rate** | 32.82% |
| **SL Hit** | 6,391 |
| **Total PnL** | -2,326.56 points |
| **PnL Moyen** | -0.24 points |
| **Expectancy** | -0.24 points |
| **Trade Gagnant Moyen** | +21.17 points |
| **Trade Perdant Moyen** | -10.87 points |
| **Gross Profit** | 67,224.56 points |
| **Gross Loss** | -69,551.12 points |
| **Profit Factor** | 0.97 |
| **Max Drawdown** | -3,197.65 points |
| **Risque Moyen** | 10.85 points |
| **Long Trades** | 4,564 (WR: 33.06%) |
| **Short Trades** | 5,007 (WR: 33.27%) |

---

## 🏆 Comparaison des Niveaux RR

| Métrique | 1.0R | 1.5R | 2.0R | **Meilleur** |
|----------|------|------|------|--------------|
| **Win Rate** | 49.50% | 39.25% | 33.17% | **1.0R** |
| **TP Hit Rate** | 49.40% | 39.11% | 32.82% | **1.0R** |
| **Total PnL** | -2,345 pts | -2,868 pts | -2,327 pts | **2.0R** |
| **Expectancy** | -0.25 pts | -0.30 pts | -0.24 pts | **2.0R** |
| **Profit Factor** | 0.96 | 0.95 | 0.97 | **2.0R** |
| **Max Drawdown** | -3,652 pts | -3,527 pts | -3,198 pts | **2.0R** |
| **Trade Gagnant Moyen** | +10.68 pts | +16.07 pts | +21.17 pts | **2.0R** |

## 📈 Observations Clés

### 1. Win Rate vs RR
- Plus le niveau RR augmente, plus le win rate diminue (attendu)
- 1.0R: 49.50% → 1.5R: 39.25% → 2.0R: 33.17%
- Diminution de ~10% par palier de 0.5R

### 2. Profit Factor
- **2.0R a le meilleur Profit Factor (0.97)**, proche de 1.0
- Tous les niveaux sont légèrement négatifs (PF < 1.0)
- 2.0R offre le meilleur ratio risque/récompense

### 3. Expectancy
- **2.0R a la meilleure expectancy (-0.24 pts)**, la moins négative
- La stratégie est légèrement négative sur tous les niveaux
- Perte moyenne par trade très faible

### 4. Drawdown
- **2.0R a le drawdown le plus faible (-3,197.65 pts)**
- 2.0R montre plus de stabilité dans les pertes

### 5. Long vs Short
- Performance équilibrée entre Long et Short sur tous les niveaux
- Légère préférence pour les Short trades (plus nombreux)

## 🎯 Recommandations

### Meilleur Niveau: **2.0R**
Raisons:
1. ✅ Meilleur Profit Factor (0.97)
2. ✅ Meilleure Expectancy (-0.24 pts)
3. ✅ Total PnL le moins négatif (-2,327 pts)
4. ✅ Drawdown le plus faible (-3,198 pts)
5. ✅ Trades gagnants moyens les plus élevés (+21.17 pts)

### Améliorations Possibles
1. **Filtrage supplémentaire:** Ajouter des conditions de confirmation (volume, volatilité, contexte de marché)
2. **Optimisation de l'entrée:** Tester des entrées partielles ou à limite
3. **Gestion du SL:** Tester un trailing stop ou SL dynamique
4. **Sélection des FVGs:** Ne trader que certains types de FVGs (taille minimale, timing)
5. **Sessions de marché:** Analyser les performances par session (ouverture NY, milieu de journée)

## 📁 Fichiers Générés

- `ny_opening_fvg_all_1.0R_results.csv` - Résultats détaillés 1.0R
- `ny_opening_fvg_all_1.5R_results.csv` - Résultats détaillés 1.5R
- `ny_opening_fvg_all_2.0R_results.csv` - Résultats détaillés 2.0R

## 🔧 Exécution du Script

```bash
python3 ny_opening_fvg_all_rr_backtest.py
```

Le script:
1. Charge automatiquement toutes les données 2018-2025
2. Extrait TOUS les FVGs de 08:30-09:00 NY
3. Exécute 3 backtests séparés (1R, 1.5R, 2R)
4. Génère les statistiques comparatives
5. Sauvegarde les résultats en CSV

---

**Date de génération:** 2025-12-09
**Script:** `ny_opening_fvg_all_rr_backtest.py`

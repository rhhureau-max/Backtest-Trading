# 🚀 Guide de Démarrage Rapide - Backtest FVG NQ

## Installation en 2 minutes

### 1. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 2. Consolider les données
```bash
python3 combine_data.py
```
➜ Crée `NQ_5min.csv` (~38 MB, 554k bougies)

### 3. Lancer le backtest
```bash
python3 backtest_fvg_strategy.py
```
➜ Génère `backtest_results.csv` et `performance_report.txt`

## 🧪 Tests Automatisés

Pour valider l'installation complète :
```bash
python3 run_tests.py
```

## 📊 Résultats

Après l'exécution, vous obtiendrez :

1. **`backtest_results.csv`**
   - Détails de tous les trades (19k+ lignes)
   - Colonnes : date, heure, prix, type, SL, TP, résultat, PnL
   - Un résultat par scénario R/R (1R, 1.5R, 2R, 2.5R)

2. **`performance_report.txt`**
   - Métriques de performance par scénario R/R
   - Winrate, Profit Factor, PnL Net, Drawdown
   - Nombre de trades gagnants/perdants

## 📖 Documentation Complète

- **`README_BACKTEST.md`** - Guide détaillé de la stratégie
- **`SUMMARY.md`** - Résumé du projet et résultats

## ⚙️ Personnalisation

Éditez `backtest_fvg_strategy.py` pour modifier :

```python
# Fenêtre horaire FVG
self.fvg_start_time = time(2, 0)  # 02:00
self.fvg_end_time = time(6, 0)    # 06:00

# Stop Loss
self.sl_ticks = 5  # 5 ticks = 1.25 points

# Scénarios Risk/Reward
self.rr_scenarios = [1.0, 1.5, 2.0, 2.5]
```

## 🎯 Stratégie FVG en Bref

### Fair Value Gap (FVG)
- **Haussier** : Low[i] > High[i-2] → Zone = [High[i-2], Low[i]]
- **Baissier** : High[i] < Low[i-2] → Zone = [Low[i-2], High[i]]

### Règles d'Entrée
1. FVG détecté entre 02:00-06:00
2. Prix entre dans le FVG
3. Bougie clôture au-dessus/en-dessous du FVG
4. Entrée à l'ouverture de la bougie suivante

### Gestion du Risque
- **SL** : ±5 ticks depuis la signal candle
- **TP** : 4 scénarios testés (1R, 1.5R, 2R, 2.5R)

## 📈 Performance (2018-2025)

| R/R  | Trades | Winrate | PnL Net   | Profit Factor |
|------|--------|---------|-----------|---------------|
| 1.0R | 19,222 | 44.96%  | -9,242 pt | 0.90          |
| 1.5R | 19,222 | 36.99%  | -9,139 pt | 0.91          |
| 2.0R | 19,222 | 31.56%  | -7,618 pt | 0.93          |
| 2.5R | 19,222 | 27.60%  | -6,614 pt | 0.95          |

## ⚡ Performance Système

- **Consolidation** : ~4 secondes
- **Backtest** : ~50 secondes (554k bougies)
- **Total** : ~1 minute pour une analyse complète de 7+ années

## 📁 Structure du Projet

```
.
├── combine_data.py           # Script de consolidation
├── backtest_fvg_strategy.py  # Script de backtesting
├── run_tests.py              # Tests automatisés
├── requirements.txt          # Dépendances Python
├── README_BACKTEST.md        # Documentation détaillée
├── SUMMARY.md                # Résumé du projet
├── QUICKSTART.md            # Ce fichier
└── .gitignore               # Fichiers à ignorer

# Fichiers générés (non versionnés)
├── NQ_5min.csv              # Données consolidées
├── backtest_results.csv     # Résultats détaillés
└── performance_report.txt   # Rapport de performance
```

## 🤝 Support

Pour toute question sur :
- La stratégie FVG → Voir `README_BACKTEST.md`
- Les résultats → Voir `SUMMARY.md`
- Les tests → Exécuter `run_tests.py`

---

**Temps total estimé** : 5 minutes (installation + exécution)
**Prérequis** : Python 3.8+, pandas, numpy

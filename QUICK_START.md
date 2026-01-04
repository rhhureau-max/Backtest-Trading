# Guide d'Exécution Rapide - FVG Inversion Backtest

## 🚀 Démarrage Rapide

### 1. Installation des Dépendances

```bash
pip install -r requirements.txt
```

### 2. Exécuter le Backtest

```bash
python fvg_inversion_backtest.py
```

**Sortie attendue:**
- Résultats détaillés dans la console
- Fichier `fvg_inversion_trades.csv` généré avec 6,933 trades

### 3. Analyser les Résultats en Détail

```bash
python analyze_trades.py
```

**Analyses supplémentaires:**
- Performance par année (2018-2025)
- Performance par type de trade (LONG vs SHORT)
- Analyse des durées de trades
- Top 5 meilleurs et pires trades
- Performance mensuelle 2025
- Statistiques de risque-récompense

## 📊 Fichiers Générés

| Fichier | Description | Taille |
|---------|-------------|--------|
| `fvg_inversion_trades.csv` | Liste complète des 6,933 trades | ~725 KB |
| `backtest_output.log` | Log complet du backtest | Variable |

## 📈 Résultats Clés

### Performance Globale
```
Capital Initial:  $100,000.00
Capital Final:    $56,917.10
PnL Total:        -$43,082.71
Rendement:        -43.08%
```

### Statistiques de Trading
```
Total Trades:     6,933
Win Rate:         47.41%
Profit Factor:    0.95
Max Drawdown:     -64.72%
```

### Performance par Année
```
2018: -$6,290    (Win Rate: 45.65%)
2019: +$65       (Win Rate: 47.38%)
2020: -$11,520   (Win Rate: 46.67%)
2021: -$13,331   (Win Rate: 44.82%)
2022: -$31,525   (Win Rate: 45.78%)
2023: +$7,230    (Win Rate: 50.33%)
2024: +$866      (Win Rate: 48.35%)
2025: +$11,423   (Win Rate: 50.59%)
```

## 🔧 Personnalisation

### Modifier le Capital Initial

Éditez `fvg_inversion_backtest.py` ligne 556:
```python
backtest = FVGInversionBacktest(initial_capital=50000)  # Changez à votre capital
```

### Modifier la Fenêtre de Trading

Éditez la méthode `is_london_killzone` (ligne 85):
```python
def is_london_killzone(self, dt: datetime) -> bool:
    hour = dt.hour
    return 1 <= hour <= 4  # Modifiez ces heures
```

### Modifier le Ratio Risk-Reward

Éditez la méthode `open_position` (ligne 264):
```python
# Pour RR 1:1.5
take_profit = entry_price + (risk_per_contract * 1.5)  # LONG
take_profit = entry_price - (risk_per_contract * 1.5)  # SHORT
```

## 📁 Structure des Fichiers du Projet

```
Backtest-Trading/
│
├── fvg_inversion_backtest.py      # Script principal du backtest
├── analyze_trades.py              # Script d'analyse détaillée
├── requirements.txt               # Dépendances Python
├── README_FVG_STRATEGY.md        # Documentation complète
├── QUICK_START.md                # Ce guide
│
├── fvg_inversion_trades.csv      # Résultats (généré)
├── backtest_output.log           # Log (généré)
│
└── Data Files/
    ├── 2018 5m.csv               # Données 2018
    ├── 2019 5m.csv               # Données 2019
    ├── 2020 5m.csv               # Données 2020
    ├── 2021 5m.csv               # Données 2021
    ├── 2022 5m.csv               # Données 2022
    ├── 2023 5m.csv               # Données 2023
    ├── 2024 5m.csv               # Données 2024
    └── 2025 5m.csv               # Données 2025
```

## 💡 Prochaines Étapes Suggérées

1. **Analyser les résultats par année** pour identifier les meilleures périodes
2. **Tester différents ratios RR** (1:1.5, 1:2, 1:3)
3. **Ajouter des filtres** (tendance, volume, momentum)
4. **Optimiser la fenêtre de trading** (tester d'autres sessions)
5. **Implémenter un trailing stop** pour protéger les profits

## ⚠️ Notes Importantes

- **Données**: Le backtest utilise 554,518 bougies de 5 minutes (2018-2025)
- **Timezone**: Toutes les données sont en timezone Chicago (pas de conversion nécessaire)
- **Position Size**: 1 contrat NQ par trade ($20 par point)
- **Frais**: Les frais de trading ne sont PAS inclus dans ce backtest

## 📞 Support Technique

Pour toute question:
1. Consultez `README_FVG_STRATEGY.md` pour la documentation complète
2. Vérifiez que toutes les dépendances sont installées
3. Assurez-vous que tous les fichiers CSV sont présents

---

**Bon Trading! 🚀**

# FVG Inversion Strategy Backtest - Nasdaq (NQ)

## 📊 Vue d'ensemble

Ce projet implémente un backtest complet de la stratégie **FVG Inversion** (Fair Value Gap Inversion) sur le Nasdaq (NQ) avec une période de données de 2018 à 2025.

## 🎯 Stratégie

### Instrument & Timeframe
- **Instrument**: Nasdaq (NQ) Futures
- **Timeframe**: 5 minutes
- **Période**: 2018 - 2025
- **Capital initial**: $100,000
- **Multiplicateur NQ**: $20 par point

### Fenêtre de Trading (Time Filter)
La stratégie ne prend des trades **QUE** pendant la **London Killzone**:
- **Horaires**: 01:00 à 04:00 (Chicago time, inclus)
- Tous les trades en dehors de cette fenêtre sont ignorés

### Logique de la Stratégie

#### 1. Identification des FVG (Fair Value Gaps)

**FVG Baissier** (Bearish FVG):
- Il y a un écart entre le Low de la bougie i-2 et le High de la bougie i
- Condition: `Low[i-2] > High[i]`
- L'écart créé représente une zone de "fair value" non comblée

**FVG Haussier** (Bullish FVG):
- Il y a un écart entre le High de la bougie i-2 et le Low de la bougie i
- Condition: `High[i-2] < Low[i]`
- L'écart créé représente une zone de "fair value" non comblée

#### 2. Signaux d'Entrée (Inversion)

**Signal LONG** (Inversion d'un FVG Baissier):
- Le prix a récemment créé un FVG Baissier
- Une bougie de 5 minutes clôture **au-dessus** du haut du FVG Baissier
- Condition: `Close > Low[i-2]` (qui a initié le gap)
- Entrée: À la clôture de cette bougie de signal

**Signal SHORT** (Inversion d'un FVG Haussier):
- Le prix a récemment créé un FVG Haussier
- Une bougie de 5 minutes clôture **en-dessous** du bas du FVG Haussier
- Condition: `Close < High[i-2]` (qui a initié le gap)
- Entrée: À la clôture de cette bougie de signal

#### 3. Gestion du Trade

**Stop Loss**:
- **Pour un LONG**: Placé sous le Low de la bougie de signal
- **Pour un SHORT**: Placé au-dessus du High de la bougie de signal

**Take Profit**:
- Ratio Risque/Rendement (RR) fixe de **1:1**
- TP = Entry ± (Entry - SL)

**Règles de Position**:
- Une seule position ouverte à la fois
- Taille de position: 1 contrat par trade

## 📈 Résultats du Backtest

### Performance Globale

| Métrique | Valeur |
|----------|--------|
| **Capital Initial** | $100,000.00 |
| **Capital Final** | $56,917.10 |
| **PnL Total** | **-$43,082.71** |
| **Rendement Total** | **-43.08%** |

### Statistiques des Trades

| Métrique | Valeur |
|----------|--------|
| **Total Trades** | 6,933 |
| **Trades Gagnants** | 3,287 (47.41%) |
| **Trades Perdants** | 3,622 (52.59%) |
| **Win Rate** | **47.41%** |

### Métriques de Performance

| Métrique | Valeur |
|----------|--------|
| **Gain Moyen** | $240.50 |
| **Perte Moyenne** | -$230.15 |
| **Profit Factor** | **0.95** |
| **Max Drawdown** | -$64,721.43 |
| **Max Drawdown (%)** | **-64.72%** |

## 📁 Structure des Fichiers

```
├── fvg_inversion_backtest.py    # Script principal du backtest
├── fvg_inversion_trades.csv     # Fichier CSV avec tous les trades (6,933 trades)
├── requirements.txt             # Dépendances Python
├── backtest_output.log          # Log complet du backtest
└── README_FVG_STRATEGY.md      # Cette documentation
```

## 🚀 Installation et Exécution

### Prérequis
- Python 3.8 ou supérieur
- pandas >= 2.0.0
- numpy >= 1.24.0

### Installation

```bash
# Installer les dépendances
pip install -r requirements.txt
```

### Exécution

```bash
# Exécuter le backtest
python fvg_inversion_backtest.py
```

Le script va:
1. Charger et combiner tous les fichiers CSV de 2018 à 2025
2. Exécuter le backtest avec la stratégie FVG Inversion
3. Afficher les résultats dans la console
4. Générer un fichier `fvg_inversion_trades.csv` avec la liste complète des trades

## 📊 Données

### Source des Données
Les fichiers CSV contiennent des données de chandelier de 5 minutes pour le Nasdaq (NQ):
- Format: CSV avec séparateur point-virgule (;)
- Colonnes: Date, Time, Open, High, Low, Close, Volume
- Timezone: Chicago (déjà en timezone correcte)
- Fichiers: `2018 5m.csv` à `2025 5m.csv`

### Volume de Données
- Total de bougies: **554,518** (environ 8 ans de données)
- Période: 2018-01-01 à 2025-12-10

## 📝 Format du Fichier de Trades

Le fichier `fvg_inversion_trades.csv` contient les colonnes suivantes:

| Colonne | Description |
|---------|-------------|
| Entry Date | Date et heure d'entrée du trade |
| Exit Date | Date et heure de sortie du trade |
| Type | Type de trade (LONG ou SHORT) |
| Entry Price | Prix d'entrée |
| Exit Price | Prix de sortie |
| Stop Loss | Niveau de stop loss |
| Take Profit | Niveau de take profit |
| Exit Reason | Raison de sortie (Stop Loss / Take Profit / End of Data) |
| PnL | Profit ou perte du trade ($) |
| Capital | Capital total après le trade |

## 🔍 Analyse des Résultats

### Points Forts
- ✅ Volume élevé de trades (6,933) permettant une validation statistique robuste
- ✅ Gain moyen légèrement supérieur à la perte moyenne ($240.50 vs $230.15)
- ✅ Stratégie systématique et objective, facile à automatiser

### Points à Améliorer
- ⚠️ Win rate inférieur à 50% (47.41%)
- ⚠️ Profit Factor < 1.0 (0.95) indiquant une légère perte nette
- ⚠️ Drawdown important (64.72%)
- ⚠️ Performance négative sur la période (-43.08%)

### Suggestions d'Optimisation

1. **Filtres additionnels**:
   - Ajouter un filtre de tendance (EMA, SMA)
   - Vérifier le volume sur les bougies de signal
   - Utiliser la confluence avec d'autres niveaux (support/résistance)

2. **Gestion du risque**:
   - Tester différents ratios RR (1:1.5, 1:2)
   - Implémenter un trailing stop
   - Ajuster la taille de position selon la volatilité

3. **Fenêtre de trading**:
   - Tester d'autres sessions (New York, Asian)
   - Analyser les performances par jour de la semaine
   - Éviter les périodes de faible liquidité

4. **Validation des FVG**:
   - Exiger une taille minimale de gap
   - Vérifier le momentum lors de l'inversion
   - Attendre une confirmation supplémentaire

## 🛠️ Personnalisation

Le script peut être facilement personnalisé:

```python
# Dans la fonction main()

# Modifier le capital initial
backtest = FVGInversionBacktest(initial_capital=50000)

# Modifier la fenêtre de trading (méthode is_london_killzone)
def is_london_killzone(self, dt: datetime) -> bool:
    hour = dt.hour
    return 1 <= hour <= 4  # Modifier ces valeurs

# Modifier le ratio RR (méthode open_position)
take_profit = entry_price + (risk_per_contract * 1.5)  # RR 1:1.5
```

## 📧 Support

Pour toute question ou amélioration, veuillez consulter la documentation du code ou créer une issue.

---

**Note**: Ce backtest est fourni à des fins éducatives uniquement. Les performances passées ne garantissent pas les résultats futurs. Tradez à vos propres risques.

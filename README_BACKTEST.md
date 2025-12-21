# Backtest Stratégie FVG - NQ Futures

## Description

Système complet de backtesting pour une stratégie de trading basée sur les **Fair Value Gaps (FVG)** sur le **NQ (Nasdaq Futures)** en timeframe 5 minutes.

## 📋 Contenu du Repository

### Scripts Principaux

1. **`combine_data.py`** - Script de consolidation des données
   - Combine tous les fichiers CSV 5 minutes (2018-2025)
   - Crée le fichier `NQ_5min.csv` avec les données consolidées
   - Nettoie et formate les données pour le backtesting

2. **`backtest_fvg_strategy.py`** - Script de backtesting principal
   - Implémente la stratégie FVG complète
   - Teste 4 scénarios de Risk/Reward simultanément (1R, 1.5R, 2R, 2.5R)
   - Génère les rapports de performance détaillés

## 🚀 Installation

### Prérequis

- Python 3.8 ou supérieur
- Bibliothèques Python : `pandas`, `numpy`

### Installation des dépendances

```bash
pip install pandas numpy
```

## 📊 Utilisation

### Étape 1 : Consolidation des données

Avant de lancer le backtest, vous devez d'abord consolider les données :

```bash
python3 combine_data.py
```

Cette commande va :
- Charger tous les fichiers `YYYY 5m.csv` (2018 à 2025)
- Les combiner en un seul fichier `NQ_5min.csv`
- Afficher des statistiques sur les données chargées

**Sortie attendue :**
- Fichier `NQ_5min.csv` (environ 38 MB)
- Plus de 554 000 bougies de 5 minutes

### Étape 2 : Exécution du Backtest

Une fois les données consolidées, lancez le backtest :

```bash
python3 backtest_fvg_strategy.py
```

**Sortie attendue :**
- `backtest_results.csv` - Détails de tous les trades
- `performance_report.txt` - Rapport de performance résumé

## 📈 Stratégie FVG

### Définition du Fair Value Gap

Un **Fair Value Gap (FVG)** est une zone de déséquilibre de prix :

- **FVG Haussier** : `Low[i] > High[i-2]`
  - Zone du FVG : `[High[i-2], Low[i]]`

- **FVG Baissier** : `High[i] < Low[i-2]`
  - Zone du FVG : `[Low[i-2], High[i]]`

### Filtres de la Stratégie

- **Fenêtre horaire** : Les FVG sont détectés uniquement entre **02:00 et 06:00** (heure du fichier)
- **Session** : Les FVG sont stockés pour la session en cours uniquement

### Signaux d'Entrée

#### Position LONG (FVG Haussier)
1. Le prix entre dans la zone du FVG haussier
2. Une bougie de 5 minutes **clôture au-dessus** de la borne haute du FVG
3. Entrée à l'**ouverture de la bougie suivante**

#### Position SHORT (FVG Baissier)
1. Le prix entre dans la zone du FVG baissier
2. Une bougie de 5 minutes **clôture en-dessous** de la borne basse du FVG
3. Entrée à l'**ouverture de la bougie suivante**

### Gestion du Risque

#### Stop Loss (SL)
- **Pour un LONG** : SL = Low de la Signal Candle - (5 ticks × 0.25)
- **Pour un SHORT** : SL = High de la Signal Candle + (5 ticks × 0.25)

#### Take Profit (TP)
Le backtest teste **4 scénarios de Risk/Reward** :
- **1R** : TP = Entry ± 1 × Risk
- **1.5R** : TP = Entry ± 1.5 × Risk
- **2R** : TP = Entry ± 2 × Risk
- **2.5R** : TP = Entry ± 2.5 × Risk

## 📊 Résultats du Backtest

### Exemple de Sortie (2018-2025)

```
======================================================================
📊 RAPPORT DE PERFORMANCE - STRATÉGIE FVG NQ
======================================================================

Scénario Risk/Reward: 1.0R
  Nombre total de trades:    19222
  Trades clôturés:           19222
  Winrate:                   44.96%
  Profit Factor:             0.90
  PnL Net:                   -9242.24 points
  Drawdown Maximum:          9478.48 points

Scénario Risk/Reward: 2.5R
  Nombre total de trades:    19222
  Trades clôturés:           19222
  Winrate:                   27.60%
  Profit Factor:             0.95
  PnL Net:                   -6613.59 points
  Drawdown Maximum:          9542.22 points
```

### Interprétation des Résultats

- **Winrate** : Pourcentage de trades gagnants
- **Profit Factor** : Ratio gains totaux / pertes totales
- **PnL Net** : Profit/Loss net en points
- **Drawdown Maximum** : Perte maximale depuis un pic

## 📁 Format des Fichiers

### Fichiers d'Entrée (CSV 5 minutes)

```
Column1;Column2;Column3;Column4;Column5;Column6;Column7
01/01/2018;17:00:00;7503.74;7511.94;7499.64;7511.35;1451
```

- **Column1** : Date (DD/MM/YYYY)
- **Column2** : Heure (HH:MM:SS)
- **Column3** : Open
- **Column4** : High
- **Column5** : Low
- **Column6** : Close
- **Column7** : Volume

### Fichier de Sortie (backtest_results.csv)

Colonnes principales :
- `entry_date`, `entry_time` : Date/heure d'entrée
- `entry_price` : Prix d'entrée
- `type` : LONG ou SHORT
- `sl_price` : Prix du Stop Loss
- `tp_1.0R`, `tp_1.5R`, etc. : Prix des Take Profits
- `result_1.0R`, `result_1.5R`, etc. : WIN, LOSS ou OPEN
- `pnl_1.0R`, `pnl_1.5R`, etc. : Profit/Loss en points

## 🔧 Personnalisation

### Modifier les Paramètres

Dans `backtest_fvg_strategy.py`, vous pouvez ajuster :

```python
# Fenêtre horaire pour la détection des FVG
self.fvg_start_time = time(2, 0)   # Heure de début
self.fvg_end_time = time(6, 0)     # Heure de fin

# Distance du Stop Loss
self.sl_ticks = 5                  # Nombre de ticks

# Scénarios de Risk/Reward
self.rr_scenarios = [1.0, 1.5, 2.0, 2.5]
```

## ⚠️ Notes Importantes

1. **Pas de conversion de timezone** : Les horaires sont utilisés tels quels depuis les fichiers CSV
2. **Performance** : Le backtest analyse plus de 554 000 bougies en environ 50 secondes
3. **Mémoire** : Assurez-vous d'avoir suffisamment de RAM (environ 500 MB nécessaires)

## 📝 License

Ce projet est fourni à des fins éducatives et de recherche.

## 🤝 Contribution

Pour toute question ou suggestion d'amélioration, n'hésitez pas à ouvrir une issue.

---

**Développé avec ❤️ pour l'analyse quantitative du trading**

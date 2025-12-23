# NQ Fair Value Gap Backtesting System

Système de backtesting complet pour une stratégie de trading basée sur les Fair Value Gaps (FVG) sur le NQ (Nasdaq 100 Futures).

## 📊 Description de la Stratégie

### Qu'est-ce qu'un Fair Value Gap (FVG) ?

Un **Fair Value Gap** (ou "gap de juste valeur") est un déséquilibre dans le carnet d'ordres qui crée un espace non comblé entre trois bougies consécutives :

- **FVG Bearish** : Gap entre le bas de la bougie N-2 et le haut de la bougie N (la bougie N-1 ne couvre pas cet espace)
- **FVG Bullish** : Gap entre le haut de la bougie N-2 et le bas de la bougie N (la bougie N-1 ne couvre pas cet espace)

### Règles de Trading

**Conditions d'entrée :**
- **LONG** : Après un FVG bearish, attendre qu'une bougie bullish comble complètement le FVG et clôture au-delà (au-dessus) du haut du FVG
- **SHORT** : Après un FVG bullish, attendre qu'une bougie bearish comble complètement le FVG et clôture au-delà (en dessous) du bas du FVG

**Important** : Seul le PREMIER FVG de chaque session de trading (2h-6h) est considéré pour le trading.

**Gestion du risque :**
- **Stop Loss** : Placé au swing low/high des 5 dernières bougies avant l'entrée
- **Take Profit** : Ratio Risk/Reward de 1:1

## 🚀 Installation

### Prérequis
- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### Étapes d'installation

1. Cloner le dépôt :
```bash
git clone https://github.com/rhhureau-max/Backtest-Trading.git
cd Backtest-Trading
```

2. Installer les dépendances :
```bash
pip install -r requirements.txt
```

## 📖 Utilisation

### Lancer le backtest

Pour exécuter le backtest avec les paramètres par défaut :

```bash
python main.py
```

### Configuration des paramètres

Les paramètres du backtest peuvent être modifiés dans le fichier `main.py` :

```python
# Période du backtest
START_YEAR = 2018
END_YEAR = 2025

# Session de trading (heure UTC des données)
SESSION_START_HOUR = 2
SESSION_START_MINUTE = 0
SESSION_END_HOUR = 6
SESSION_END_MINUTE = 0

# Paramètres de la stratégie
RISK_REWARD_RATIO = 1.0      # Ratio Risk/Reward
SWING_LOOKBACK = 5            # Nombre de bougies pour swing points

# Capital initial
INITIAL_CAPITAL = 100000
```

## 📁 Structure du Projet

```
Backtest-Trading/
├── main.py                  # Point d'entrée principal
├── data_loader.py           # Chargement et filtrage des données
├── strategy.py              # Logique de la stratégie FVG
├── backtest.py              # Moteur de backtesting
├── visualization.py         # Génération de graphiques
├── requirements.txt         # Dépendances Python
├── README.md               # Documentation
│
├── 2018 5m.csv             # Données historiques NQ 5 minutes
├── 2019 5m.csv
├── ...
└── 2025 5m.csv
```

## 📊 Fichiers de Sortie

Le système génère automatiquement plusieurs fichiers :

1. **trade_journal.csv** : Journal détaillé de tous les trades
   - Date/heure d'entrée et sortie
   - Prix d'entrée, stop loss, take profit
   - Type de position (long/short)
   - P&L de chaque trade

2. **equity_curve.png** : Courbe d'équité au fil du temps
3. **trade_distribution.png** : Distribution des trades et statistiques
4. **monthly_returns.png** : Rendements mensuels
5. **sample_trades.png** : Exemples de trades avec niveaux visualisés

## 📈 Statistiques de Performance

Le système calcule automatiquement :

- Nombre total de trades
- Taux de réussite (win rate)
- Profit/Loss total et moyen
- Profit factor
- Drawdown maximum
- Sharpe ratio
- Rendements mensuels

## 🔧 Architecture Modulaire

Le code est organisé en modules pour faciliter la maintenance et les modifications :

### `data_loader.py`
- Chargement des fichiers CSV (format séparé par point-virgule)
- Filtrage des données pour la session 2h-6h
- Identification des sessions de trading

### `strategy.py`
- Détection des Fair Value Gaps (bearish et bullish)
- Identification du premier FVG par session
- Détection des signaux d'inversion et de remplissage du FVG
- Calcul des swing points pour stop loss

### `backtest.py`
- Moteur de backtesting
- Gestion des positions (entrée, sortie)
- Vérification des stop loss et take profit
- Calcul des statistiques de performance

### `visualization.py`
- Génération de graphiques (equity curve, distribution, etc.)
- Visualisation des trades avec niveaux

## 📝 Format des Données

Les fichiers CSV doivent avoir le format suivant (séparateur point-virgule) :

```
Column1;Column2;Column3;Column4;Column5;Column6;Column7
01/01/2018;17:00:00;7503.74;7511.94;7499.64;7511.35;1451
```

Colonnes : Date;Heure;Open;High;Low;Close;Volume

## ⚙️ Personnalisation

### Modifier la session de trading

Éditez les variables dans `main.py` :
```python
SESSION_START_HOUR = 2    # Heure de début
SESSION_END_HOUR = 6      # Heure de fin
```

### Modifier le ratio Risk/Reward

```python
RISK_REWARD_RATIO = 1.5   # Pour un ratio 1:1.5
```

### Modifier le calcul des swing points

```python
SWING_LOOKBACK = 10       # Pour utiliser 10 bougies
```

## 🐛 Dépannage

### Erreur "File not found"
- Assurez-vous que les fichiers CSV sont dans le même répertoire que les scripts
- Vérifiez que les noms de fichiers correspondent au format : `YYYY 5m.csv`

### Erreur d'importation de modules
- Exécutez : `pip install -r requirements.txt`
- Vérifiez que vous utilisez Python 3.8+

### Aucun trade généré
- Vérifiez que vos données contiennent bien des bougies dans la plage horaire 2h-6h
- Augmentez la période du backtest
- Vérifiez le format des données CSV

## 📄 Licence

Ce projet est un outil de backtesting éducatif. Utilisez-le à vos propres risques.

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- Signaler des bugs
- Proposer des améliorations
- Ajouter de nouvelles fonctionnalités

## ⚠️ Avertissement

Ce système est fourni à des fins éducatives et de recherche uniquement. Le trading de futures comporte des risques importants. Les performances passées ne garantissent pas les résultats futurs. Effectuez toujours vos propres recherches avant de prendre des décisions de trading.
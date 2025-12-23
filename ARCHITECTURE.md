# Architecture du Système de Backtesting

## Vue d'ensemble

```
┌─────────────────────────────────────────────────────────────────┐
│                    NQ FVG Backtesting System                    │
└─────────────────────────────────────────────────────────────────┘

┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   main.py    │────▶│ main_config  │────▶│   demo.py    │
│              │     │     .py      │     │              │
│ Entry Point  │     │  (with INI)  │     │ Quick Test   │
└──────┬───────┘     └──────┬───────┘     └──────┬───────┘
       │                    │                    │
       └────────────────────┼────────────────────┘
                            ▼
                   ┌────────────────┐
                   │   config.ini   │
                   │  Configuration │
                   └────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                         Core Modules                             │
├──────────────┬──────────────┬──────────────┬───────────────────┤
│data_loader.py│ strategy.py  │ backtest.py  │visualization.py   │
│              │              │              │                   │
│• Load CSV    │• Detect FVG  │• Run trades  │• Equity curve     │
│• Filter 2-6h │• First FVG   │• Position    │• Distribution     │
│• Sessions    │• Entry signal│  management  │• Monthly returns  │
│              │• Swing calc  │• Calculate   │• Sample trades    │
│              │              │  statistics  │                   │
└──────┬───────┴──────┬───────┴──────┬───────┴─────┬─────────────┘
       │              │              │             │
       ▼              ▼              ▼             ▼
┌─────────────────────────────────────────────────────────────────┐
│                            Data Flow                             │
└─────────────────────────────────────────────────────────────────┘

1. DATA LOADING (data_loader.py)
   ┌─────────────────┐
   │ 2018-2025 5m.csv│
   └────────┬────────┘
            │ Load & Parse
            ▼
   ┌─────────────────┐
   │  DataFrame      │
   │  OHLCV + Time   │
   └────────┬────────┘
            │ Filter 2h-6h
            ▼
   ┌─────────────────┐
   │  Filtered DF    │
   │  + session_id   │
   └────────┬────────┘

2. STRATEGY (strategy.py)
            │
            ▼
   ┌─────────────────┐
   │  Detect FVGs    │
   │  (3-candle)     │
   └────────┬────────┘
            │
            ▼
   ┌─────────────────┐
   │  Mark 1st FVG   │
   │  per session    │
   └────────┬────────┘
            │
            ▼
   ┌─────────────────┐
   │  Check Fill &   │
   │  Reversal       │
   └────────┬────────┘
            │
            ▼
   ┌─────────────────┐
   │  Entry Signals  │
   │  (long/short)   │
   └────────┬────────┘

3. BACKTEST (backtest.py)
            │
            ▼
   ┌─────────────────┐
   │  For each bar   │
   │  Check SL/TP    │
   └────────┬────────┘
            │
            ▼
   ┌─────────────────┐
   │  New signal?    │
   │  Enter position │
   └────────┬────────┘
            │
            ▼
   ┌─────────────────┐
   │  List of Trades │
   │  (Entry/Exit)   │
   └────────┬────────┘

4. OUTPUT (visualization.py)
            │
            ▼
   ┌────────┬────────┬────────┬────────┐
   │ CSV    │ Equity │ Dist.  │ Monthly│
   │ Journal│ Curve  │ Charts │ Returns│
   └────────┴────────┴────────┴────────┘
```

## Flux de Données Détaillé

### 1. Chargement des Données
```
CSV Files (2018-2025)
    │
    ├─→ read_csv() avec séparateur ';'
    │
    ├─→ Parse datetime (date + time)
    │
    ├─→ Filter session (2h-6h)
    │
    └─→ Add session_id (one per day)
```

### 2. Détection des Signaux
```
DataFrame avec OHLCV
    │
    ├─→ detect_fvg()
    │   └─→ Pour chaque triplet de bougies (N-2, N-1, N)
    │       ├─→ Bearish: low(N-2) > high(N) & low(N-1) > high(N)
    │       └─→ Bullish: high(N-2) < low(N) & high(N-1) < low(N)
    │
    ├─→ get_first_fvg_per_session()
    │   └─→ Marque seulement le 1er FVG de chaque session
    │
    └─→ check_fvg_fill_and_reversal()
        └─→ Pour chaque FVG actif:
            ├─→ LONG: bougie bullish comble et clôture > FVG top
            └─→ SHORT: bougie bearish comble et clôture < FVG bottom
```

### 3. Backtesting
```
Pour chaque barre:
    │
    ├─→ Position active?
    │   ├─→ OUI: Vérifier SL/TP
    │   │   ├─→ SL touché? → Fermer position (perte)
    │   │   └─→ TP touché? → Fermer position (gain)
    │   │
    │   └─→ NON: Signal d'entrée?
    │       ├─→ OUI: Calculer swing high/low (5 bougies)
    │       │   ├─→ LONG: SL = swing low, TP = entry + (entry - SL) * RR
    │       │   └─→ SHORT: SL = swing high, TP = entry - (SL - entry) * RR
    │       │
    │       └─→ Ouvrir nouvelle position
    │
    └─→ Enregistrer tous les trades
```

### 4. Statistiques et Visualisation
```
Liste de Trades
    │
    ├─→ calculate_statistics()
    │   ├─→ Win rate
    │   ├─→ Profit factor
    │   ├─→ Max drawdown
    │   └─→ Sharpe ratio
    │
    ├─→ export_trades() → CSV
    │
    └─→ Visualizer
        ├─→ plot_equity_curve()
        ├─→ plot_trade_distribution()
        ├─→ plot_monthly_returns()
        └─→ plot_sample_trades()
```

## Classes Principales

### DataLoader
- **load_data()**: Charge et concatène tous les fichiers CSV
- **filter_trading_session()**: Filtre pour 2h-6h uniquement
- **add_session_markers()**: Ajoute un ID par session de trading

### FVGStrategy
- **detect_fvg()**: Détecte tous les FVG (bearish et bullish)
- **get_first_fvg_per_session()**: Identifie le 1er FVG de chaque session
- **check_fvg_fill_and_reversal()**: Détecte les signaux d'entrée
- **calculate_swing_levels()**: Calcule swing high/low pour SL
- **calculate_position_levels()**: Calcule TP basé sur RR

### Backtest
- **run()**: Exécute le backtest barre par barre
- **calculate_statistics()**: Calcule toutes les métriques de performance
- **export_trades()**: Exporte le journal de trading en CSV
- **print_statistics()**: Affiche les résultats

### Visualizer
- **plot_equity_curve()**: Courbe d'équité avec marqueurs win/loss
- **plot_trade_distribution()**: 4 graphiques (P&L, win/loss, cumul, long/short)
- **plot_monthly_returns()**: Barres de rendement mensuel
- **plot_sample_trades()**: Graphiques détaillés de trades individuels

## Configuration

### Via config.ini
```ini
[data]
start_year = 2018
end_year = 2025
session_start_hour = 2
session_end_hour = 6

[strategy]
risk_reward_ratio = 1.0
swing_lookback = 5

[backtest]
initial_capital = 100000
```

### Via main.py (inline)
```python
START_YEAR = 2018
END_YEAR = 2025
SESSION_START_HOUR = 2
SESSION_END_HOUR = 6
RISK_REWARD_RATIO = 1.0
SWING_LOOKBACK = 5
INITIAL_CAPITAL = 100000
```

## Points d'Extension

### Ajouter un nouveau filtre
1. Modifier `strategy.py` → Ajouter méthode dans `FVGStrategy`
2. Appeler dans `main.py` après `detect_fvg()`

### Changer le calcul du stop loss
1. Modifier `strategy.py` → `calculate_swing_levels()`
2. Ajuster `SWING_LOOKBACK` dans config

### Ajouter une nouvelle métrique
1. Modifier `backtest.py` → `calculate_statistics()`
2. Ajouter dans `print_statistics()`

### Créer un nouveau graphique
1. Ajouter méthode dans `visualization.py`
2. Appeler dans `main.py` Step 11

## Performance

- **Temps de chargement**: ~10-15 secondes (554k bougies)
- **Temps de backtest**: ~30-40 secondes
- **Temps total**: ~60-90 secondes pour backtest complet
- **Mémoire utilisée**: ~200-300 MB

## Dépendances

- **pandas** ≥ 2.0.0: Manipulation de données
- **numpy** ≥ 1.24.0: Calculs numériques
- **matplotlib** ≥ 3.7.0: Visualisations

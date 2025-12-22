# IFVG Strategy Backtest - Documentation

## Vue d'ensemble

Ce repository contient une implémentation complète de backtesting pour une stratégie de trading basée sur les **Inversion Fair Value Gaps (IFVG)**, un concept clé du **Smart Money Concepts (ICT)**. La stratégie a été testée sur les données historiques du NQ (Nasdaq 100) de 2018 à 2025.

## Fichiers principaux

- **`backtest_ifvg_strategy.py`** - Script Python complet de backtesting
- **`equity_curve.png`** - Courbe d'équité visuelle montrant la progression du capital
- **`trade_log.csv`** - Journal détaillé de tous les trades exécutés (4,828 trades)

## Description de la Stratégie

### Concepts Clés

#### 1. Fair Value Gap (FVG)
Un FVG est un "gap" ou zone de déséquilibre créé par trois bougies consécutives :
- **FVG Baissier** : Bas[N-2] > Haut[N] (zone de résistance)
- **FVG Haussier** : Haut[N-2] < Bas[N] (zone de support)

#### 2. Inversion FVG (IFVG)
L'inversion se produit quand le prix revient dans le FVG et le traverse avec force :
- **Setup Long** : Un FVG baissier devient support quand le prix clôture au-dessus du Haut du FVG
- **Setup Short** : Un FVG haussier devient résistance quand le prix clôture en dessous du Bas du FVG

### Règles de Trading Implémentées

#### Filtre Temporel (CRITIQUE)
- **Fenêtre de trading** : 02:00 - 06:00 (heure du fichier, sans conversion de fuseau horaire)
- Seules les bougies de signal formées dans cette fenêtre sont considérées

#### Filtres de Qualité

**Filtre 1 : Balayage de Liquidité (Liquidity Sweep)**
- Dans les 60 minutes (12 bougies de 5min) précédant le signal
- Le prix doit avoir balayé un plus haut ou plus bas local (fractale de 5 périodes)
- Confirme que le mouvement a piégé la liquidité avant l'inversion

**Filtre 2 : Clôture Forte (Strong Close)**
- La bougie d'inversion doit clôturer avec force au-delà du FVG
- Seuil : La clôture doit être au moins 15% de la taille du FVG au-delà de sa limite
- Évite les clôtures faibles/millimétriques qui ne montrent pas de conviction

#### Gestion du Trade

**Entrée**
- À la clôture de la bougie qui valide l'inversion
- Doit se produire entre 02:00 et 06:00

**Stop Loss**
- Long : 10 points sous le plus bas de la bougie d'inversion
- Short : 10 points au-dessus du plus haut de la bougie d'inversion

**Take Profit**
- Ratio Risque/Récompense fixe de **2:1**
- TP = Entrée + (2 × Risque)

## Résultats du Backtest

### Performance Globale (2018-2025)

```
Total Trades         : 4,828
Winning Trades       : 1,665 (34.49%)
Losing Trades        : 3,163 (65.51%)
Win Rate             : 34.49%
Profit Factor        : 1.02
Total Return         : $1,453.59 (1.45%)
Maximum Drawdown     : 3.54%
Gross Profit         : $78,991.20
Gross Loss           : $77,537.61
```

### Performance Année par Année

| Année | Trades | Win Rate | Profit Factor | Return % |
|-------|--------|----------|---------------|----------|
| 2018  | 698    | 35.5%    | 1.07          | 2.9%     |
| 2019  | 695    | 36.5%    | 1.12          | 3.5%     |
| 2020  | 706    | 34.7%    | 1.03          | 0.8%     |
| 2021  | 672    | 33.2%    | 0.96          | -1.0%    |
| 2022  | 652    | 32.4%    | 0.93          | -1.9%    |
| 2023  | 641    | 34.3%    | 1.02          | 0.7%     |
| 2024  | 645    | 34.9%    | 1.06          | 1.9%     |
| 2025  | 119    | 33.6%    | 1.01          | 0.1%     |

### Observations Clés

1. **Consistance** : La stratégie génère un nombre élevé de signaux (≈640-700 trades/an)
2. **Win Rate Modeste** : ~34% de trades gagnants, compensé par le ratio RR de 2:1
3. **Profit Factor Stable** : Proche de 1.0, indiquant une stratégie équilibrée
4. **Drawdown Contrôlé** : 3.54% maximum, montrant une bonne gestion du risque
5. **Variabilité Annuelle** : Performance variable selon les années (2019 meilleure, 2022 la pire)

## Utilisation du Script

### Prérequis

```bash
pip install pandas numpy matplotlib
```

### Exécution

```bash
python backtest_ifvg_strategy.py
```

### Sorties Générées

1. **Console** : Statistiques détaillées affichées pendant l'exécution
2. **equity_curve.png** : Graphique de la courbe d'équité
3. **trade_log.csv** : Fichier CSV avec tous les détails des trades

### Structure du Trade Log

Le fichier `trade_log.csv` contient les colonnes suivantes :
- `entry_datetime` : Date/heure d'entrée
- `exit_datetime` : Date/heure de sortie
- `direction` : 'long' ou 'short'
- `entry_price` : Prix d'entrée
- `stop_loss` : Niveau du stop loss
- `take_profit` : Niveau du take profit
- `exit_price` : Prix de sortie effectif
- `pnl` : Profit/Perte du trade
- `result` : 'Win' ou 'Loss'
- `exit_reason` : 'TP', 'SL', 'Timeout', ou 'EOD'

## Configuration et Paramètres

Les paramètres suivants peuvent être ajustés dans le script :

```python
TRADE_START_TIME = time(2, 0, 0)     # Début fenêtre trading
TRADE_END_TIME = time(6, 0, 0)       # Fin fenêtre trading
STOP_LOSS_POINTS = 10                # Points pour le SL
RISK_REWARD_RATIO = 2.0              # Ratio R:R
INITIAL_CAPITAL = 100000             # Capital initial
POSITION_SIZE = 1                    # Taille de position (contrats)
LOOKBACK_CANDLES = 12                # Bougies pour liquidity sweep
STRONG_CLOSE_THRESHOLD = 0.15        # 15% du FVG pour close forte
```

## Structure du Code

Le script est organisé en fonctions modulaires :

1. **`load_all_data()`** : Charge et combine toutes les données 5min
2. **`detect_fractal_high/low()`** : Détecte les fractales de 5 périodes
3. **`check_liquidity_sweep()`** : Vérifie le balayage de liquidité
4. **`detect_fvg_and_ifvg()`** : Détecte les FVG et signaux d'inversion
5. **`execute_trades()`** : Exécute les trades et suit les sorties
6. **`calculate_statistics()`** : Calcule les métriques de performance
7. **`calculate_yearly_statistics()`** : Décompose par année
8. **`plot_equity_curve()`** : Génère le graphique d'équité
9. **`save_trade_log()`** : Sauvegarde le journal des trades

## Données Requises

Le script attend des fichiers CSV 5min nommés :
- `2018 5m.csv`
- `2019 5m.csv`
- ...
- `2025 5m.csv`

Format CSV attendu (délimiteur `;`) :
```
Column1;Column2;Column3;Column4;Column5;Column6;Column7
DD/MM/YYYY;HH:MM:SS;Open;High;Low;Close;Volume
```

## Améliorations Possibles

1. **Optimisation des Paramètres** : Tester différents seuils pour les filtres
2. **Gestion de Position Dynamique** : Ajuster la taille selon la volatilité
3. **Filtres Additionnels** : Ajouter des filtres de tendance ou de volatilité
4. **Multiple Timeframes** : Confirmer les signaux sur des TF supérieurs
5. **Stop Loss Dynamique** : Utiliser un trailing stop ou ATR-based stop

## Conclusion

Cette stratégie IFVG démontre une approche systématique du trading basée sur les concepts Smart Money. Bien que le Profit Factor soit proche de 1.0, la stratégie montre :

✅ **Avantages** :
- Génération régulière de signaux
- Drawdown contrôlé (3.54%)
- Consistance sur 7+ années
- Règles claires et objectives

⚠️ **Limitations** :
- Win Rate relativement faible (34%)
- Return total modeste (1.45%)
- Performance variable selon les années
- Nécessite un RR strict pour être profitable

La stratégie pourrait servir de base pour des développements ultérieurs avec des filtres additionnels ou une gestion de risque plus sophistiquée.

---

**Note** : Ce backtest est fourni à des fins éducatives. Les performances passées ne garantissent pas les résultats futurs. Toujours tester en paper trading avant le live trading.

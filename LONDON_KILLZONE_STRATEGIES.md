# London Killzone Trading Strategies - Documentation

## Vue d'ensemble

Ce projet implémente trois stratégies de trading algorithmique spécifiquement conçues pour la **London Killzone** (08:00-12:00 heure de Paris) sur le Nasdaq 100 (NQ) futures.

**Contrainte principale:** Maximum **un seul trade par jour** pendant la fenêtre de trading spécifiée.

## Stratégies Implémentées

### Stratégie A : Le "Judas Swing" (Chasse aux Liquidités)

**Objectif:** Capturer le retournement après une fausse cassure du range asiatique.

**Logique détaillée:**
1. **Calcul du Range Asiatique:** High et Low entre 00:00 et 08:00 (Paris)
2. **Trigger:** Cassure du High ou Low asiatique après 08:00
3. **Condition d'entrée:**
   - Cassure High → Attendre clôture sous le High (réintégration) → LONG
   - Cassure Low → Attendre clôture au-dessus du Low (réintégration) → SHORT
4. **Stop Loss:** 5 points au-delà du plus haut/bas de la mèche de fausse cassure
5. **Take Profit:** Liquidité opposée (range opposé) OU ratio fixe 1:3

**Paramètres configurables:**
- `points_offset`: Offset du SL (défaut: 5.0 points)
- `risk_reward`: Ratio risque/rendement (défaut: 3.0)

**Cas d'usage:**
- Marchés volatils avec whipsaws fréquents
- Opens chahutés
- Chasses de liquidités evidentes

---

### Stratégie B : Le Retest de l'ORB (Opening Range Breakout)

**Objectif:** Capturer la continuation du momentum après l'ouverture officielle.

**Logique détaillée:**
1. **Définition de la Boîte:** High et Low entre 08:00 et 09:00 (Pre-market London)
2. **Trigger:** Clôture hors de la boîte après 09:00
3. **Condition d'entrée:**
   - Ordre limite placé sur le niveau cassé (retest)
   - Ordre valide jusqu'à 11:00
   - Si non déclenché → annuler
4. **Stop Loss:** Milieu de la boîte (50% du range)
5. **Take Profit:** 200% de l'amplitude de la boîte (extension Fibonacci)

**Paramètres configurables:**
- `retest_window_hours`: Fenêtre pour le retest (défaut: 2 heures, jusqu'à 11:00)

**Cas d'usage:**
- Jours de tendance claire
- Momentum fort dès l'ouverture
- Breakouts authentiques

---

### Stratégie C : La Continuation de Tendance HTF (Fibonacci OTE)

**Objectif:** Rejoindre la tendance de fond sur un repli matinal.

**Logique détaillée:**
1. **Biais Directionnel:**
   - Bougie D1 précédente (Verte=Bullish, Rouge=Bearish)
   - Alternative: MA50 sur H4
2. **Trigger:**
   - Bullish: Prix recule sous ouverture de 08:00
   - Bearish: Prix monte au-dessus ouverture de 08:00
3. **Zone d'Entrée OTE:** 61.8% à 79% de retracement Fibonacci
4. **Condition d'entrée:**
   - Prix touche la zone OTE
   - Pattern de retournement (Pinbar ou Engulfing) sur M5
5. **Stop Loss:** Sous le Swing Low (point 0 Fibonacci) + 5 points buffer
6. **Take Profit:** Extension -0.27 du Fibonacci

**Paramètres configurables:**
- `ote_low`: Niveau bas de la zone OTE (défaut: 0.618)
- `ote_high`: Niveau haut de la zone OTE (défaut: 0.79)

**Cas d'usage:**
- Tendances HTF fortes et claires
- Pullbacks dans la direction du trend
- Alignement multi-timeframes

---

## Structure du Code

### Modules Principaux

```
london_killzone_strategies.py
├── DataLoader              # Chargement et preprocessing des données CSV
├── TimeManager            # Gestion des timezones et sessions
├── StrategyA_JudasSwing   # Implémentation Stratégie A
├── StrategyB_ORBRetest    # Implémentation Stratégie B
├── StrategyC_HTFContinuation # Implémentation Stratégie C
├── BacktestEngine         # Moteur de backtest
└── create_comparison_table # Table de comparaison théorique
```

---

## Installation et Dépendances

### Prérequis

```bash
pip install pandas numpy pytz
```

Ou utilisez le fichier `requirements.txt`:

```bash
pip install -r requirements.txt
```

### Format des Données CSV

Les fichiers CSV doivent avoir le format suivant (séparateur `;`):

```
Column1;Column2;Column3;Column4;Column5;Column6;Column7
01/01/2024;17:00:00;18244.57923;18248.331274;18238.951165;18241.631196;1308
...
```

Colonnes:
1. Date (DD/MM/YYYY)
2. Time (HH:MM:SS)
3. Open
4. High
5. Low
6. Close
7. Volume

---

## Utilisation

### Exemple Basique

```python
from london_killzone_strategies import (
    DataLoader,
    StrategyA_JudasSwing,
    BacktestEngine
)

# Charger les données
df_5m = DataLoader.load_csv("2024 5m.csv")

# Initialiser le moteur de backtest
engine = BacktestEngine(df_5m)

# Créer et exécuter la stratégie
strategy = StrategyA_JudasSwing(points_offset=5.0, risk_reward=3.0)
trades = engine.run_strategy(strategy)

# Générer le rapport de performance
performance = engine.generate_performance_report(trades, "Judas Swing")
print(performance)
```

### Script d'Exemple Complet

Le script `backtest_example.py` fournit un exemple complet:

```bash
python backtest_example.py
```

Ce script:
1. Charge les données historiques
2. Exécute les trois stratégies
3. Génère des rapports de performance
4. Affiche une table de comparaison
5. Sauvegarde les résultats en CSV (optionnel)

---

## Gestion des Incohérences de Données

### Jours Fériés

Les jours sans données (fériés, weekends) sont automatiquement ignorés par le moteur de backtest. Aucune action manuelle requise.

### Gaps de Prix

**Traitement:**
- Les gaps sont considérés comme faisant partie de la structure du marché
- Le SL et TP sont vérifiés sur chaque bougie
- Si un gap saute le SL, le trade est fermé au niveau du SL spécifié
- Si un gap saute le TP, le trade est fermé au niveau du TP spécifié

**Recommandation:**
Pour une simulation plus réaliste, vous pouvez implémenter une logique de "slippage" dans la méthode `execute_trade()`.

### Données Manquantes

```python
# Vérifier les données manquantes
df_clean = df.dropna()

# Ou interpoler (avec précaution)
df_filled = df.fillna(method='ffill')
```

**Note:** L'interpolation n'est pas recommandée pour les données OHLCV car elle peut créer des prix artificiels.

### Timezone

Les données sont automatiquement converties en heure de Paris (Europe/Paris) via `TimeManager.convert_to_paris_time()`.

Si vos données sont déjà en heure de Paris, vous pouvez ignorer cette étape.

---

## Tableau Comparatif des Stratégies

| Critère | Judas Swing | ORB Retest | HTF Continuation |
|---------|-------------|------------|------------------|
| **Type de Setup** | Reversal (False Breakout) | Continuation (Breakout + Retest) | Trend Following (Fibonacci) |
| **Style d'Entrée** | Market Order | Limit Order | Market Order |
| **Risk/Reward** | 1:3 (Fixe) | 1:4 (Variable) | 1:2-1:3 (HTF dependent) |
| **Win Rate Attendu** | 45-55% | 50-60% | 55-65% |
| **Meilleur pour NQ quand** | Haute volatilité, opens chaotiques | Jours de tendance, direction claire | Forte tendance HTF alignée |
| **Faiblesses** | Peut rater si pas de false breakout | Nécessite patience pour retest | Complexe, besoin données HTF |
| **Forces** | Capture les reversals tôt | Meilleur R:R, niveaux clairs | Haute probabilité avec trend |
| **Préférence Volatilité** | Haute (whipsaw markets) | Moyenne-Haute (momentum) | Moyenne (trending markets) |

---

## Métriques de Performance

Le `BacktestEngine` génère les métriques suivantes:

- **Total Trades:** Nombre total de trades exécutés
- **Winning Trades:** Nombre de trades gagnants
- **Losing Trades:** Nombre de trades perdants
- **Win Rate:** Pourcentage de trades gagnants
- **Average Win:** Points gagnés moyens par trade gagnant
- **Average Loss:** Points perdus moyens par trade perdant
- **Profit Factor:** Ratio profits/pertes (>1 = profitable)
- **Total P&L:** P&L total en points
- **Max Consecutive Losses:** Plus longue série de pertes consécutives
- **Avg Risk/Reward:** Ratio risque/rendement moyen réalisé

---

## Optimisation et Personnalisation

### Ajuster les Paramètres

```python
# Strategy A
strategy_a = StrategyA_JudasSwing(
    points_offset=10.0,    # Plus conservateur
    risk_reward=2.0        # Plus agressif
)

# Strategy B
strategy_b = StrategyB_ORBRetest(
    retest_window_hours=3  # Fenêtre plus large
)

# Strategy C
strategy_c = StrategyC_HTFContinuation(
    ote_low=0.5,          # Zone OTE plus large
    ote_high=0.85
)
```

### Filtres Additionnels

Vous pouvez ajouter des filtres personnalisés avant l'exécution:

```python
# Filtre par volume
if signal and current['Volume'] > volume_threshold:
    # Exécuter le trade
    
# Filtre par range de la bougie
if signal and (signal['asian_high'] - signal['asian_low']) > min_range:
    # Exécuter le trade

# Filtre par heure
if signal and signal['entry_time'].hour >= 9:
    # Exécuter le trade uniquement après 09:00
```

---

## Structure de Répertoire Recommandée

```
Backtest-Trading/
├── london_killzone_strategies.py    # Module principal
├── backtest_example.py              # Script d'exemple
├── requirements.txt                 # Dépendances
├── LONDON_KILLZONE_STRATEGIES.md    # Cette documentation
├── data/                            # Dossier pour les données
│   ├── 2024 5m.csv
│   ├── 2024 4H.csv
│   └── ...
└── results/                         # Dossier pour les résultats
    ├── strategy_a_trades.csv
    ├── strategy_b_trades.csv
    ├── strategy_c_trades.csv
    └── strategy_performance_summary.csv
```

---

## Tests et Validation

### Test Manuel

```python
# Tester sur une journée spécifique
from datetime import datetime

date = pd.Timestamp("2024-06-15")
signal = strategy.find_signal(df, date)

if signal:
    print(f"Signal trouvé: {signal}")
    result = strategy.execute_trade(df, signal)
    print(f"Résultat: {result}")
```

### Backtesting Walk-Forward

```python
# Diviser les données en périodes
train_start, train_end = "2024-01-01", "2024-06-30"
test_start, test_end = "2024-07-01", "2024-12-31"

# Train sur première période
trades_train = engine.run_strategy(strategy, train_start, train_end)
perf_train = engine.generate_performance_report(trades_train, "Train")

# Test sur deuxième période
trades_test = engine.run_strategy(strategy, test_start, test_end)
perf_test = engine.generate_performance_report(trades_test, "Test")

# Comparer les résultats
print("Train:", perf_train)
print("Test:", perf_test)
```

---

## Limitations et Avertissements

1. **Slippage non inclus:** Les résultats supposent une exécution parfaite aux prix spécifiés
2. **Commissions non incluses:** Pas de frais de courtage dans les calculs
3. **Liquidité:** Le script suppose une liquidité suffisante pour tous les trades
4. **Données de qualité:** Les résultats dépendent de la qualité des données historiques
5. **Overfitting:** Évitez de sur-optimiser les paramètres sur des données historiques

**AVERTISSEMENT:** Ces stratégies sont fournies à des fins éducatives. Le trading comporte des risques significatifs. Testez toujours en paper trading avant d'utiliser de l'argent réel.

---

## Pseudo-Code des Stratégies

### Strategy A: Judas Swing

```
POUR chaque jour de trading:
    asian_high, asian_low = RANGE(00:00 à 08:00)
    
    POUR chaque bougie de 08:00 à 12:00:
        SI prix casse asian_low ET bougie suivante clôture > asian_low:
            ENTRER LONG au prix de clôture
            SL = plus_bas_de_la_fausse_cassure - 5 points
            TP = asian_high OU (entry + 3 * risque)
            SORTIR
        
        SI prix casse asian_high ET bougie suivante clôture < asian_high:
            ENTRER SHORT au prix de clôture
            SL = plus_haut_de_la_fausse_cassure + 5 points
            TP = asian_low OU (entry - 3 * risque)
            SORTIR
```

### Strategy B: ORB Retest

```
POUR chaque jour de trading:
    box_high, box_low = RANGE(08:00 à 09:00)
    box_mid = (box_high + box_low) / 2
    
    POUR chaque bougie de 09:00 à 11:00:
        SI bougie clôture > box_high:
            breakout = "BULLISH"
            CONTINUER
        
        SI breakout == "BULLISH" ET bougie touche box_high:
            ENTRER LONG à box_high (ordre limite)
            SL = box_mid
            TP = box_high + 2 * (box_high - box_low)
            SORTIR
        
        SI bougie clôture < box_low:
            breakout = "BEARISH"
            CONTINUER
        
        SI breakout == "BEARISH" ET bougie touche box_low:
            ENTRER SHORT à box_low (ordre limite)
            SL = box_mid
            TP = box_low - 2 * (box_high - box_low)
            SORTIR
```

### Strategy C: HTF Continuation

```
POUR chaque jour de trading:
    bias = DETECTER_BIAS(bougie_D1_precedente OU MA50_H4)
    
    POUR chaque bougie de 08:00 à 12:00:
        SI bias == "BULLISH":
            swing_low = MIN(low) dans session
            swing_high = MAX(high) dans session
            fib_618 = swing_low + 0.618 * (swing_high - swing_low)
            fib_79 = swing_low + 0.79 * (swing_high - swing_low)
            
            SI prix dans zone [fib_618, fib_79] ET pattern_de_reversal_bullish:
                ENTRER LONG au prix de clôture
                SL = swing_low - 5 points
                TP = swing_high + 0.27 * (swing_high - swing_low)
                SORTIR
        
        SI bias == "BEARISH":
            # Logique similaire inversée
```

---

## Support et Contribution

Pour des questions ou améliorations:
1. Ouvrir une issue sur GitHub
2. Proposer une pull request avec des modifications
3. Contacter l'équipe de développement

---

## Changelog

**Version 1.0.0** (2024-12-27)
- Implémentation initiale des trois stratégies
- Moteur de backtest complet
- Documentation en français
- Script d'exemple fonctionnel
- Support multi-années et multi-timeframes

---

## Licence

Ce projet est fourni "tel quel" sans garantie d'aucune sorte. Utilisez-le à vos propres risques.

---

**Bon trading et bon backtesting! 📈🚀**

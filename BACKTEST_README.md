# Backtest FVG Inversion Strategy - Nasdaq (NQ)

Script de backtest pour la stratégie d'inversion FVG avec filtre de tendance multi-timeframe sur le Nasdaq (NQ).

## Stratégie

### Données
- **Timeframe principal**: 3 minutes (généré à partir de données 1 minute)
- **Filtre de tendance**: EMA 50 sur 1 heure
- **Fenêtre de trading**: London Killzone (01:00-04:00 Chicago time)

### Indicateurs
- **FVG Baissier**: Gap entre Low[i-2] et High[i]
- **FVG Haussier**: Gap entre High[i-2] et Low[i]
- **EMA 50 H1**: Moyenne Mobile Exponentielle 50 périodes sur 1 heure

### Conditions d'entrée

#### LONG (AND logic)
1. **FVG**: Prix comble un FVG Baissier récent (Close > Bottom du FVG)
2. **Tendance**: H1 Close > EMA 50 H1 (tendance haussière)
3. **Fenêtre**: London Killzone (01:00-04:00)
4. **Entrée**: À la clôture de la bougie 3m de signal

#### SHORT (AND logic)
1. **FVG**: Prix comble un FVG Haussier récent (Close < Top du FVG)
2. **Tendance**: H1 Close < EMA 50 H1 (tendance baissière)
3. **Fenêtre**: London Killzone (01:00-04:00)
4. **Entrée**: À la clôture de la bougie 3m de signal

### Gestion du Trade

- **Stop Loss (SL)**:
  - LONG: Sous le Low de la bougie signal
  - SHORT: Au-dessus du High de la bougie signal

- **Take Profit (TP)**: Ratio Risque/Rendement (RR) fixe de 1:1

- **Position**: Une seule position active à la fois (pas de cumul)

## Installation

```bash
pip install pandas numpy
```

## Utilisation

### Mode Démo (échantillon de données)

Par défaut, le script utilise un échantillon de 50,000 bougies 1m pour une exécution rapide:

```bash
python3 backtest_fvg_strategy.py
```

### Mode Complet (2018-2025)

Pour backtester sur toutes les données historiques, modifiez la fonction `main()` dans `backtest_fvg_strategy.py`:

```python
def main():
    # Charger tous les fichiers 1m de 2018 à 2025
    df_list = []
    for year in range(2018, 2026):
        try:
            # Certaines années sont en .zip, d'autres en .csv
            df = load_data_1min(f'{year} 1m.csv')
            df_list.append(df)
        except:
            pass
    
    df_1min = pd.concat(df_list, ignore_index=True)
    df_1min = df_1min.sort_values('DateTime').reset_index(drop=True)
    
    # Charger tous les fichiers 1H
    df_1h_list = []
    for year in range(2018, 2026):
        try:
            df = load_data_1h(f'{year} 1H.csv')
            df_1h_list.append(df)
        except:
            pass
    
    df_1h = pd.concat(df_1h_list, ignore_index=True)
    df_1h = df_1h.sort_values('DateTime').reset_index(drop=True)
    
    # Suite du code...
```

## Output

### Console
Le script affiche:
- Capital Initial et Final
- Rendement Total (%)
- Nombre de Trades (total, gagnants, perdants)
- Winrate (%)
- Profit Factor
- Drawdown Maximum (%)
- Détails des 5 premiers trades

### Fichier CSV
Les trades sont sauvegardés dans `backtest_trades.csv` avec les colonnes:
- `entry_time`: Date/heure d'entrée
- `exit_time`: Date/heure de sortie
- `type`: LONG ou SHORT
- `entry_price`: Prix d'entrée
- `exit_price`: Prix de sortie
- `pnl`: Profit & Loss
- `result`: WIN ou LOSS

## Exemple de Résultats

```
================================================================================
RÉSULTATS DU BACKTEST
================================================================================

Capital Initial:       $100,000.00
Capital Final:         $99,716.23
Rendement Total:       -0.28%

Nombre de Trades:      557
Trades Gagnants:       219
Trades Perdants:       338
Winrate:               39.32%
Profit Factor:         0.85
Drawdown Maximum:      0.35%
================================================================================
```

## Personnalisation

### Modifier le capital initial

```python
results = backtest_strategy(df_3min, initial_capital=50000)
```

### Modifier la fenêtre de trading

Modifiez la fonction `is_london_killzone()`:

```python
def is_london_killzone(dt):
    hour = dt.hour
    return 1 <= hour < 4  # Modifier les heures ici
```

### Modifier le ratio Risk/Reward

Dans la fonction `backtest_strategy()`, modifiez le calcul du TP:

```python
# Pour un RR de 1:2
take_profit = entry_price + (risk * 2)  # LONG
take_profit = entry_price - (risk * 2)  # SHORT
```

### Modifier le lookback des FVG

Dans la fonction `backtest_strategy()`, modifiez:

```python
# Garder seulement les 20 derniers FVG
if len(recent_fvg_bearish) > 20:  # Changer 20 ici
```

## Optimisation des Paramètres

Pour optimiser la stratégie, vous pouvez tester:
- Différentes périodes d'EMA (30, 50, 100, 200)
- Différentes fenêtres de trading (New York, Asia session)
- Différents ratios Risk/Reward (1:1.5, 1:2, 1:3)
- Différents lookback de FVG (10, 20, 30)

## Notes Importantes

### Lookahead Bias
Le script utilise `pd.merge_asof()` avec `direction='backward'` pour mapper les données H1 aux timestamps 3m sans lookahead bias. Cela garantit que seules les données disponibles au moment du trade sont utilisées.

### Timezone
Les données sont en timezone Chicago. Aucune conversion n'est nécessaire puisque la fenêtre de trading (01:00-04:00) est déjà dans cette timezone.

### FVG Récents
Le script garde les 20 derniers FVG détectés pour vérifier si le prix les comble. Cela évite de chercher dans tous les FVG historiques et améliore les performances.

### Slippage et Commission
Le script ne prend pas en compte le slippage ni les commissions. Pour un backtest plus réaliste, ajoutez ces coûts:

```python
commission = 4.0  # $ par trade
slippage = 2.0   # points de slippage

# Dans backtest_strategy():
pnl = (exit_price - entry_price) - slippage - commission
```

## Dépendances

- Python 3.8+
- pandas >= 2.0.0
- numpy >= 1.24.0

## Support

Pour toute question ou amélioration, consultez le code source avec les commentaires détaillés ou créez une issue sur GitHub.

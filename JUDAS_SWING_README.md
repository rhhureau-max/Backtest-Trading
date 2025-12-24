# Backtest Stratégie "Judas Swing & Inversion"

## Description

Ce script Python effectue un backtest complet de la stratégie de trading "Judas Swing & Inversion" sur le Nasdaq 100 (NQ) en timeframe 5 minutes, sur la période 2018-2025.

## Stratégie

### Sessions (Heure de Chicago - UTC-5)

- **Asia Session** : 18:00 - 23:00 (zone de calcul des niveaux)
- **London Open** : 01:00 - 04:00 (zone de trade)

### Logique du Setup

Le setup recherche une séquence chronologique précise pendant la session London :

1. **Condition A (Sweep)** : Le prix casse sous le `Asia_Low`

2. **Condition B (FVG Baissier)** : Formation d'un Fair Value Gap baissier
   - Gap entre le Low de la bougie N-1 et le High de la bougie N+1
   - Se produit pendant le mouvement baissier

3. **Condition C (Signal)** : Une bougie ultérieure clôture strictement au-dessus du bord haut du FVG
   - C'est le signal d'entrée (inversion)

### Gestion du Trade

- **Entrée** : Prix de clôture de la bougie de signal
- **Stop Loss** : Placé au niveau du `Asia_Low`
- **Take Profit** : Placé au niveau du `Asia_EQ` (Equilibrium = moyenne High/Low)
- **Sortie Temporelle** : Clôture forcée à 11:00 si ni SL ni TP touchés

## Prérequis

```bash
pip install pandas numpy
```

## Utilisation

```bash
python3 judas_swing_backtest.py
```

Le script va :
1. Charger tous les fichiers CSV 5m (2018-2025)
2. Calculer les niveaux Asia Session pour chaque jour
3. Détecter les setups valides
4. Simuler les trades avec gestion du risque
5. Générer un rapport de performance détaillé
6. Sauvegarder tous les trades dans `judas_swing_trades.csv`

## Format des Données CSV

Les fichiers CSV doivent suivre ce format :
- **Séparateur** : point-virgule (;)
- **Colonnes** :
  - Column1 : Date (DD/MM/YYYY)
  - Column2 : Heure (HH:MM:SS)
  - Column3 : Open
  - Column4 : High
  - Column5 : Low
  - Column6 : Close
  - Column7 : Volume

## Résultats

Le script génère :

### Rapport Console
- Nombre total de trades
- Win Rate (%)
- Ratio Gain/Perte moyen (R:R)
- Profit Factor
- Performance totale en points
- Distribution des sorties (TP/SL/Time)
- Top 5 meilleurs trades
- Pire 5 trades

### Fichier CSV (`judas_swing_trades.csv`)
Contient tous les détails de chaque trade :
- Date et heures d'entrée/sortie
- Prix d'entrée/sortie
- Raison de sortie
- Niveaux de SL/TP
- PnL, Risk, Reward
- Ratio R:R
- Niveaux Asia (Low, EQ)
- Niveaux FVG (High, Low)

## Exemple de Résultats

```
📊 RAPPORT DE PERFORMANCE
--------------------------------------------------------------------------------
Nombre total de trades        : 417
  • Trades gagnants           : 198
  • Trades perdants           : 219
  • Trades breakeven          : 0

Win Rate                      : 47.48%
Ratio Gain/Perte moyen (R:R)  : 2.52
Profit Factor                 : 0.66
Performance totale (points)   : -1138.54
```

## Notes Importantes

- **Timezone** : Les données CSV sont en heure de Chicago (UTC-5). Le script n'effectue aucune conversion de fuseau horaire.
- **Un seul trade par jour** : Le script ne prend qu'un seul setup par jour pour éviter le sur-trading.
- **Données historiques** : Le script traite environ 554,000 bougies de 5 minutes sur 8 années.

## Structure du Code

Le script est organisé en fonctions modulaires :
- `load_data()` : Chargement et fusion des CSV
- `calculate_asia_session_levels()` : Calcul des niveaux Asia
- `detect_fvg_bearish()` : Détection des Fair Value Gaps baissiers
- `find_signal_candle()` : Recherche du signal d'entrée
- `backtest_strategy()` : Logique principale du backtest
- `calculate_performance()` : Calcul et affichage des métriques
- `save_trades_to_csv()` : Export des résultats

## Personnalisation

Vous pouvez facilement modifier :
- Les horaires des sessions (variables `ASIA_START`, `ASIA_END`, etc.)
- Les conditions d'entrée dans la fonction `backtest_strategy()`
- Les critères de détection des FVG dans `detect_fvg_bearish()`
- La gestion du risque (SL/TP)

## Auteur

Script créé pour le backtesting algorithmique avec Python.

## Licence

Libre d'utilisation pour usage personnel et éducatif.

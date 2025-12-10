# Liquidity Sweep with FVG Confirmation Backtest Strategy

## Vue d'ensemble

Cette stratégie backteste un setup de trading multi-timeframe basé sur le concept de "Liquidity Sweep" (balayage de liquidité) avec confirmation par Fair Value Gap (FVG). La stratégie cherche à capturer les retournements de marché après que le prix ait balayé des niveaux clés.

## Définitions Techniques

### Fair Value Gap (FVG)
Un pattern de 3 bougies où les mèches des bougies extérieures ne se chevauchent pas, laissant un vide. En considérant 3 bougies consécutives aux indices i-2, i-1, et i:

- **FVG Baissier (Bearish)**: `Low[i-2] > High[i]` - Un vide entre le bas de la bougie à l'indice i-2 et le haut de la bougie à l'indice i
- **FVG Haussier (Bullish)**: `High[i-2] < Low[i]` - Un vide entre le haut de la bougie à l'indice i-2 et le bas de la bougie à l'indice i

*Note*: La bougie du milieu (i-1) crée le mouvement qui génère le vide, tandis que les bougies i-2 et i définissent les limites du FVG.

### Swing High/Low
Un point haut (Swing High) est un sommet entouré de points plus bas. Un point bas (Swing Low) est un creux entouré de points plus hauts. La détection utilise une fenêtre de lookback de 5 bougies.

## Règles de la Stratégie (Setup SHORT)

### 1. Setup de Contexte (Timeframe H1 ou M15)

Il y a deux types de setups possibles:

#### Type A: Swing Sweep (Balayage de Swing)
- Le prix dépasse (sweep) un précédent Swing High important en H1 ou M15
- La bougie ne clôture pas nécessairement loin au-dessus (mèche préférentielle)
- Indique une possible liquidation des stops au-dessus du niveau

#### Type B: FVG Mitigation (Test de FVG)
- La mèche de la bougie vient toucher/tester un ancien FVG Baissier ouvert en H1 ou M15
- Le FVG doit avoir été formé précédemment (dans les 50 dernières bougies)
- Indique un retour vers une zone de déséquilibre

### 2. Trigger de Validation (Timeframe M5)

Une fois le setup de contexte identifié:

1. **Formation de FVG Haussier M5**: Pendant le mouvement de hausse (la "leg" qui crée le sweep ou le test du FVG H1/M15), un FVG Haussier (Bullish FVG) doit s'être formé en M5
2. **Inversion du FVG**: Le prix doit se retourner et clôturer EN DESSOUS de ce FVG Haussier M5

### 3. Signal d'Entrée

- **Entrée**: À la clôture de la bougie M5 qui casse (clôture en dessous) le FVG Haussier M5
- **Direction**: Position SHORT (vente)

### 4. Gestion du Risque

- **Stop Loss (SL)**: Placé au plus haut absolu du mouvement (le sommet de la mèche du Sweep)
- **Take Profit (TP)**: Trois niveaux avec différents ratios Risque/Récompense (RR):
  - TP1: RR 1:1 (risque = récompense)
  - TP2: RR 1:1.5 (récompense = 1.5x le risque)
  - TP3: RR 1:2 (récompense = 2x le risque)

## Structure du Code

### Fonctions Principales

1. **`load_nq_data()`**: Charge les données OHLCV pour un timeframe donné
2. **`detect_fvgs()`**: Détecte les Fair Value Gaps sur n'importe quel timeframe
3. **`detect_swing_points()`**: Identifie les Swing Highs et Swing Lows
4. **`align_timeframes()`**: Aligne les données multi-timeframe

### Classe LiquiditySweepFVGStrategy

Méthodes clés:
- **`check_swing_sweep()`**: Vérifie si un Swing High a été balayé (Type A)
- **`check_fvg_mitigation()`**: Vérifie si un FVG ancien est testé (Type B)
- **`find_m5_bullish_fvg_in_range()`**: Trouve les FVG Haussiers M5 dans une plage de temps
- **`check_fvg_inversion()`**: Vérifie si le prix a inversé (clôturé en dessous) un FVG
- **`simulate_trade()`**: Simule les résultats d'un trade avec les 3 niveaux de TP
- **`run_backtest()`**: Exécute le backtest complet
- **`calculate_statistics()`**: Calcule les win rates pour chaque RR

## Format des Données

Les fichiers CSV utilisent le séparateur point-virgule (`;`) avec le format suivant:
```
Date;Time;Open;High;Low;Close;Volume
01/01/2018;17:00:00;7503.74;7511.94;7499.64;7511.35;1451
```

## Résultats

Le script génère un fichier `liquidity_sweep_fvg_results.csv` contenant:

- **entry_date**: Date et heure d'entrée
- **entry_price**: Prix d'entrée
- **sl_price**: Prix du Stop Loss
- **risk**: Montant du risque (SL - Entry)
- **tp1, tp2, tp3**: Niveaux de Take Profit
- **setup_type**: Type de setup (swing_sweep ou fvg_mitigation)
- **timeframe**: Timeframe du setup (h1 ou m15)
- **sweep_high**: Plus haut point du sweep
- **m5_fvg_bottom, m5_fvg_top**: Zone du FVG M5 utilisé pour validation
- **outcome_rr1, outcome_rr1.5, outcome_rr2**: Résultat pour chaque RR (Win/Loss)
- **exit_date_rr1, exit_date_rr1.5, exit_date_rr2**: Date de sortie pour chaque RR

### Statistiques Affichées

- **Total Trades**: Nombre total de trades exécutés
- **Win Rate RR 1:1**: Pourcentage de trades gagnants avec TP1
- **Win Rate RR 1:1.5**: Pourcentage de trades gagnants avec TP2
- **Win Rate RR 1:2**: Pourcentage de trades gagnants avec TP3

## Utilisation

```bash
python liquidity_sweep_fvg_backtest.py
```

Le script:
1. Charge les données NQ pour les timeframes 5m, 15m et 1H
2. Détecte les FVGs et Swing Points sur chaque timeframe
3. Scanne les setups H1 et M15
4. Valide avec les FVGs M5
5. Simule les trades et calcule les résultats
6. Affiche les statistiques et sauvegarde les résultats en CSV

## Paramètres Ajustables

Dans le code, vous pouvez modifier:
- **`lookback`**: Fenêtre de détection des Swing Points (défaut: 5)
- **`max_lookback`**: Nombre de bougies à considérer pour les setups passés (défaut: 50 H1, 100 M15)
- **`max_bars`**: Durée maximale d'un trade en barres M5 (défaut: 100)
- **`start_date/end_date`**: Période de backtest

## Notes Importantes

1. **Synchronisation Multi-Timeframe**: Le script aligne correctement les données M5 avec M15 et H1
2. **Validation Stricte**: Un trade n'est pris que si TOUS les critères sont remplis (setup + validation + inversion)
3. **Gestion du Risque**: Le SL est toujours placé au-dessus du point le plus haut du sweep
4. **Simulation Réaliste**: Les trades sont simulés barre par barre pour détecter l'ordre d'atteinte des niveaux (SL vs TP)

## Améliorations Possibles

- Ajouter des filtres de session (London, New York)
- Implémenter des setups LONG (inverser la logique)
- Ajouter des critères de confluence (volume, SMT, etc.)
- Optimiser les paramètres de lookback
- Ajouter des métriques de performance (Profit Factor, Drawdown, etc.)

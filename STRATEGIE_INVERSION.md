# Stratégie FVG INVERSION - Documentation

## Vue d'ensemble

Ce document décrit la stratégie d'INVERSION des Fair Value Gaps (FVG) implémentée dans le script `backtest_fvg_strategy.py`.

## Type de Stratégie

**CONTRA-TENDANCE (Inversion)** - Cette stratégie cherche à profiter des inversions de prix lorsque le marché casse des zones de support ou de résistance créées par les FVG.

## Définition des FVG

### FVG Haussier (Bullish)
- **Formation**: Quand `Low[i] > High[i-2]`
- **Zone créée**: ZONE DE SUPPORT entre `High[i-2]` (borne basse) et `Low[i]` (borne haute)
- **Signal trading**: Trade SHORT si le prix casse cette zone PAR LE BAS

### FVG Baissier (Bearish)
- **Formation**: Quand `High[i] < Low[i-2]`
- **Zone créée**: ZONE DE RÉSISTANCE entre `High[i]` (borne basse) et `Low[i-2]` (borne haute)
- **Signal trading**: Trade LONG si le prix casse cette zone PAR LE HAUT

## Règles de Trading

### Filtre Temporel
- **Fenêtre de détection FVG**: 02:00 - 06:00 du matin (heure du marché)
- Les FVG détectés dans cette fenêtre sont conservés pour la journée de trading

### Conditions d'Entrée

#### Signal LONG (Achat)
1. Un FVG **Baissier** (zone de RÉSISTANCE) doit être détecté entre 02:00-06:00
2. Une bougie de 5 minutes doit clôturer **STRICTEMENT AU-DESSUS** de la borne haute du FVG (`Close > upper`)
3. Entrée à l'**ouverture** de la bougie suivante

#### Signal SHORT (Vente)
1. Un FVG **Haussier** (zone de SUPPORT) doit être détecté entre 02:00-06:00
2. Une bougie de 5 minutes doit clôturer **STRICTEMENT EN-DESSOUS** de la borne basse du FVG (`Close < lower`)
3. Entrée à l'**ouverture** de la bougie suivante

### Gestion du Risque

#### Stop Loss (SL)
- **LONG**: Placé juste sous le `Low` de la bougie de signal (moins 5 ticks = 1.25 points)
- **SHORT**: Placé juste au-dessus du `High` de la bougie de signal (plus 5 ticks = 1.25 points)

#### Take Profit (TP)
Le backtest teste simultanément 4 scénarios Risk/Reward:
- **1R**: TP = Entry ± (Distance au SL × 1.0)
- **1.5R**: TP = Entry ± (Distance au SL × 1.5)
- **2R**: TP = Entry ± (Distance au SL × 2.0)
- **2.5R**: TP = Entry ± (Distance au SL × 2.5)

### Gestion des Positions
- **1 trade à la fois**: Le système ignore tous les nouveaux signaux tant qu'une position est ouverte
- Une fois le trade fermé (SL ou TP touché), le système peut prendre un nouveau signal

## Résultats du Backtest (2018-2025)

### Statistiques Globales
- **Période**: 01/01/2018 - 11/11/2025 (7 ans, 10 mois)
- **Nombre de bougies**: 554,518 (5 minutes)
- **Total de trades**: 16,880
- **Trades LONG**: 8,168 (48.4%)
- **Trades SHORT**: 8,712 (51.6%)

### Performance par Scénario RR

#### RR 1.0 (Risk/Reward 1:1)
- Trades gagnants: 7,910 (46.86%)
- Trades perdants: 8,970 (53.14%)
- Profit Factor: 0.92
- PnL Net: -9,926.95 points
- Drawdown Max: 10,404.92 points

#### RR 1.5 (Risk/Reward 1:1.5)
- Trades gagnants: 6,447 (38.19%)
- Trades perdants: 10,433 (61.81%)
- Profit Factor: 0.95
- PnL Net: -7,274.61 points
- Drawdown Max: 8,279.29 points

#### RR 2.0 (Risk/Reward 1:2)
- Trades gagnants: 5,482 (32.48%)
- Trades perdants: 11,398 (67.52%)
- Profit Factor: 0.98
- PnL Net: -2,787.42 points
- Drawdown Max: 6,478.33 points

#### RR 2.5 (Risk/Reward 1:2.5) ⭐
- Trades gagnants: 4,799 (28.43%)
- Trades perdants: 12,081 (71.57%)
- **Profit Factor: 1.01**
- **PnL Net: +1,819.83 points** ✅
- Drawdown Max: 5,099.27 points

## Interprétation des Résultats

### Points Clés
1. **Stratégie profitable uniquement en RR 2.5**: Seul le scénario 2.5R génère un profit net positif (+1,819.83 points)
2. **Winrate décroissant avec RR**: Plus le ratio RR est élevé, plus le winrate diminue (de 46.86% à 28.43%)
3. **Profit Factor proche de 1**: Le PF de 1.01 en RR 2.5 indique une rentabilité marginale
4. **Volume de trading**: ~2.4 trades par jour en moyenne sur 7+ ans

### Recommandations
- Cette stratégie d'inversion fonctionne mieux avec des objectifs de profit élevés (RR 2.5)
- Un winrate de 28% peut être acceptable si le RR est supérieur à 2.5:1
- Envisager des filtres additionnels pour améliorer la sélection des trades:
  - Conditions de marché (volatilité)
  - Confluence avec d'autres niveaux techniques
  - Volume ou momentum

## Fichiers Générés

### backtest_results.csv
Contient tous les trades avec:
- Date et heure d'entrée
- Prix d'entrée et SL
- Type (LONG/SHORT)
- Résultats pour chaque scénario RR (WIN/LOSS)
- Prix et dates de sortie
- PnL par trade

### performance_report.txt
Rapport détaillé des performances par scénario RR

## Utilisation

```bash
# 1. Consolider les données
python combine_data.py

# 2. Exécuter le backtest
python backtest_fvg_strategy.py

# 3. Consulter les résultats
cat performance_report.txt
```

## Code Source

Fichier principal: `backtest_fvg_strategy.py`

### Fonctions Clés
- `identify_fvg()`: Détecte les FVG (zones de support/résistance)
- `check_entry_signal()`: Vérifie les cassures de zones (logique d'INVERSION)
- `calculate_exit_levels()`: Calcule SL et TPs pour tous les RR
- `simulate_trade()`: Simule le déroulement complet d'un trade
- `run_backtest()`: Orchestre le backtest complet avec gestion "1 trade à la fois"

## Notes Importantes

⚠️ **Différence avec stratégie de CONTINUATION**:
- **Continuation**: Entrer dans le sens du FVG (FVG Bullish → LONG)
- **Inversion** (cette stratégie): Entrer contre le FVG après cassure (FVG Bullish → SHORT après cassure)

🎯 **Points d'amélioration possibles**:
- Optimiser la fenêtre horaire de détection
- Tester différentes distances de SL
- Ajouter des filtres de contexte de marché
- Implémenter un trailing stop
- Considérer les spreads et commissions réels

---
*Document créé le 21/12/2025*
*Stratégie: FVG INVERSION (Contra-tendance)*
*Instrument: NQ Futures*
*Timeframe: 5 minutes*

# SMT Divergence with FVG Confirmation Backtest Strategy

## Vue d'ensemble

Cette stratégie backteste un setup avancé basé sur la **SMT Divergence** (Smart Money Tool) entre le NQ (Nasdaq) et l'ES (S&P 500), avec confirmation par Fair Value Gap (FVG) sur le NQ en 5 minutes.

## Concept de SMT Divergence

La SMT Divergence est un outil d'analyse multi-instruments qui identifie les divergences de force relative entre deux marchés corrélés (NQ et ES). Le NQ agit comme indicateur avancé (leading indicator).

### Définition technique

**Bearish SMT (Setup SHORT)**:
- L'ES fait un Plus Haut Plus Haut (Higher High)
- MAIS le NQ échoue et fait un Plus Haut Plus Bas (Lower High)
- **Interprétation**: Le NQ montre une faiblesse relative → il "lead" la baisse

**Bullish SMT (Setup LONG)**:
- L'ES fait un Plus Bas Plus Bas (Lower Low)
- MAIS le NQ fait un Plus Bas Plus Haut (Higher Low)
- **Interprétation**: Le NQ montre une force relative → il "lead" la hausse

## Règles de la Stratégie

### 1. Détection de SMT Divergence (Timeframe H1 ou M15)

Le script compare les Swing Highs et Swing Lows du NQ et de l'ES aux mêmes timestamps (avec une tolérance de ±5 heures pour le matching).

**Paramètres**:
- Lookback pour swings: 5 bougies
- Lookback pour comparaison prix: 10-50 swings précédents
- Tolérance temporelle: 5 heures entre NQ et ES swings

### 2. Validation FVG (Timeframe M5 sur NQ)

Une fois la divergence SMT identifiée:
1. On zoome sur le NQ en 5 minutes
2. Pendant le mouvement de retournement (la "leg" qui suit la divergence), un FVG doit se former
3. **Pour SHORT (Bearish SMT)**: On cherche un FVG Baissier (bearish) formé pendant le rally
4. **Pour LONG (Bullish SMT)**: On cherche un FVG Haussier (bullish) formé pendant la baisse

**Fenêtre temporelle**:
- H1 SMT: On regarde les 5 heures suivant la divergence
- M15 SMT: On regarde les 2 heures suivantes

### 3. Trigger d'Entrée (Inversion FVG)

**Pour SHORT**:
- Le prix remonte et touche le FVG Baissier M5
- Entrée: Quand le prix clôture EN DESSOUS du FVG bottom (inversion/rejet)

**Pour LONG**:
- Le prix descend et touche le FVG Haussier M5
- Entrée: Quand le prix clôture AU-DESSUS du FVG top (inversion/rejet)

### 4. Gestion du Risque

**Stop Loss**:
- SHORT: Au-dessus du NQ High qui a formé la divergence SMT
- LONG: En-dessous du NQ Low qui a formé la divergence SMT

**Take Profit**:
- TP1: RR 1:1
- TP2: RR 1:1.5
- TP3: RR 1:2

## Structure du Code

### Fonctions Principales

1. **`load_nq_data()`** et **`load_es_data()`**: Chargent les données NQ et ES
2. **`detect_fvgs_vectorized()`**: Détecte les Fair Value Gaps (vectorisé)
3. **`detect_swing_points_vectorized()`**: Identifie les Swing Highs/Lows (vectorisé)
4. **`detect_smt_divergences()`**: Compare NQ et ES pour détecter les SMT Divergences

### Classe SMTDivergenceFVGStrategy

Méthodes clés:
- **`find_nq_m5_fvgs_in_range()`**: Trouve les FVGs NQ M5 dans une plage de temps
- **`check_fvg_inversion()`**: Vérifie si le prix a inversé un FVG
- **`simulate_trade()`**: Simule les résultats avec les 3 niveaux de TP
- **`run_backtest()`**: Exécute le backtest complet
- **`calculate_statistics()`**: Calcule les win rates

## Format des Données

### NQ (Nasdaq)
Fichiers: `YYYY 5m.csv`, `YYYY 15m.csv`, `YYYY 1H.csv`

### ES (S&P 500)
Fichiers: `ES 5m*.csv`, `ES 15m*.csv`, `ES 1h*.csv`

Format commun:
```
Date;Time;Open;High;Low;Close;Volume
01/01/2018;17:00:00;7503.74;7511.94;7499.64;7511.35;1451
```

## Résultats (Backtest Complet 2018-2025)

Le script génère un fichier `smt_divergence_fvg_results.csv` contenant:

### Colonnes du fichier résultats

- **entry_date**: Date et heure d'entrée
- **entry_price**: Prix d'entrée
- **sl_price**: Prix du Stop Loss
- **risk**: Montant du risque (distance entre Entry et SL)
- **tp1, tp2, tp3**: Niveaux de Take Profit pour RR 1, 1.5 et 2
- **setup_type**: Type de divergence (`bearish_smt` ou `bullish_smt`)
- **direction**: Direction du trade (`short` ou `long`)
- **timeframe**: Timeframe de la divergence (`h1` ou `m15`)
- **nq_swing**: Prix du swing NQ qui a créé la divergence
- **es_swing**: Prix du swing ES correspondant
- **m5_fvg_bottom, m5_fvg_top**: Zone du FVG M5 utilisé pour validation
- **outcome_rr1, outcome_rr1.5, outcome_rr2**: Résultat (Win/Loss) pour chaque RR
- **exit_date_rr1, exit_date_rr1.5, exit_date_rr2**: Date de sortie pour chaque niveau

### Statistiques

**Exemple de résultats** (données complètes 2018-2025):
- **Total Trades**: 1,376
- **Win Rate RR 1:1**: ~27%
- **Win Rate RR 1:1.5**: ~17%
- **Win Rate RR 1:2**: ~11%

**Breakdown par Direction**:
- **LONG**: ~26% WR (853 trades)
- **SHORT**: ~30% WR (523 trades)

**Détection SMT**:
- **H1**: 788 divergences détectées (98% avec M5 FVG, 84% avec entrée)
- **M15**: 912 divergences détectées (90% avec M5 FVG, 79% avec entrée)

## Utilisation

```bash
python smt_divergence_fvg_backtest.py
```

Le script:
1. Charge les données NQ et ES pour 5m, 15m et 1H
2. Détecte les FVGs sur NQ M5
3. Détecte les Swing Points sur NQ et ES (M15 et H1)
4. Identifie les SMT Divergences entre NQ et ES
5. Valide chaque divergence avec FVG M5
6. Simule les trades et calcule les résultats
7. Affiche les statistiques et sauvegarde les résultats en CSV

### Utilisation avec répertoire personnalisé

```bash
python smt_divergence_fvg_backtest.py /chemin/vers/donnees
```

## Performance

**Temps d'exécution**: ~3-4 minutes pour le dataset complet (2018-2025)

**Optimisations**:
- Détection vectorisée des FVGs et Swings
- Limite à 2000 swings pour la détection SMT (pour la performance)
- Progress indicators tous les 100/500 trades

## Paramètres Ajustables

Dans le code, vous pouvez modifier:

**Lookback Swings** (défaut: 5):
```python
nq_m15_swings = detect_swing_points_vectorized(self.nq_m15, lookback=5)
```

**Lookback Comparaison SMT** (défaut: 50 H1, 100 M15):
```python
self.h1_smt_divergences = detect_smt_divergences(..., lookback=50)
```

**Fenêtre Temporelle Reversal Leg**:
```python
leg_end = leg_start + pd.Timedelta(hours=5)  # H1
leg_end = leg_start + pd.Timedelta(hours=2)  # M15
```

**Tolérance Matching NQ/ES** (défaut: 5 heures):
```python
time_window = pd.Timedelta(hours=5)
```

**Durée Max Trade** (défaut: 50 barres M5):
```python
entry = self.check_fvg_inversion(latest_fvg, m5_start_idx, smt['direction'], max_bars=50)
```

## Notes Importantes

1. **Synchronisation Multi-Instruments**: Le script aligne correctement les timestamps NQ et ES avec une tolérance de ±5 heures
2. **NQ comme Leading Indicator**: Les trades sont exécutés sur NQ uniquement, ES sert de comparateur
3. **Validation Stricte**: Un trade n'est pris que si TOUS les critères sont remplis (SMT + FVG + Inversion)
4. **Limite de Performance**: Pour optimiser les temps d'exécution, la détection SMT est limitée aux 2000 premiers swings

## Différences avec Liquidity Sweep Strategy

| Caractéristique | Liquidity Sweep | SMT Divergence |
|-----------------|-----------------|----------------|
| **Setup Context** | Sweep de Swing High/Low OU FVG Mitigation | Divergence entre NQ et ES |
| **Instruments** | NQ uniquement | NQ + ES (comparaison) |
| **Validation M5** | FVG Haussier pendant le sweep | FVG aligné avec direction SMT |
| **Entrée** | Close sous FVG (SHORT) | Inversion du FVG |
| **Win Rate** | ~31% (RR 1:1) | ~27% (RR 1:1) |
| **Nombre de Trades** | 125,642 trades | 1,376 trades |
| **Selectivité** | Moins sélective | Plus sélective (confluence multi-instruments) |

## Améliorations Possibles

- Ajouter des filtres de session (London, New York killzones)
- Implémenter une fenêtre de matching dynamique NQ/ES
- Ajouter des métriques de corrélation NQ/ES en temps réel
- Optimiser le lookback pour améliorer le ratio trades/selectivité
- Ajouter des niveaux de TP intermédiaires
- Calculer le Profit Factor et Max Drawdown

## Références

- **SMT (Smart Money Tool)**: Concept d'analyse multi-instruments popularisé par ICT (Inner Circle Trader)
- **Fair Value Gap (FVG)**: Pattern de déséquilibre de prix utilisé pour identifier les zones de retournement

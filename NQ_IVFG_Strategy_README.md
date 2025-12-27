# NQ IVFG Strategy - Pine Script v5

## 📊 Vue d'ensemble

Stratégie de trading complète pour le **Nasdaq 100 (NQ)** utilisant l'analyse multi-timeframe et la détection des **IVFG (Inverted Fair Value Gaps)** pour identifier des points d'entrée à forte probabilité.

## 🎯 Caractéristiques Principales

### Configuration de Base
- **Instrument**: NQ (Nasdaq 100 E-mini Futures)
- **Timeframe Principal**: 5 minutes
- **Timeframe Secondaire**: 4 heures
- **Période de Backtest**: 2018 à aujourd'hui
- **Capital Initial**: 100,000 USD
- **Commission**: 2.50 USD par contrat
- **Slippage**: 2 ticks

### Filtres de Trading

#### 1. Filtre Temporel (London Killzone)
- **Fenêtre de Trading**: 01:00 - 05:00
- Utilise l'heure brute du graphique (sans conversion de fuseau horaire)
- Paramètre activable/désactivable via les inputs

#### 2. Filtre de Tendance Multi-Timeframe
- **Indicateur**: EMA 20 sur timeframe 4 heures
- **Méthode**: `request.security()` avec `lookahead=barmerge.lookahead_on` (anti-repainting)
- **Conditions**:
  - 🟢 **Long**: Prix actuel > EMA 20 (4H)
  - 🔴 **Short**: Prix actuel < EMA 20 (4H)

### Signaux d'Entrée: IVFG avec Mémoire

#### Détection des FVG (Fair Value Gaps)
Un **FVG** se forme quand il y a un "gap" entre trois bougies consécutives:

**FVG Haussier** (Bullish):
```
low[2] > high[0]
```
Gap entre le bas de la bougie [2] et le haut de la bougie [0]

**FVG Baissier** (Bearish):
```
high[2] < low[0]
```
Gap entre le haut de la bougie [2] et le bas de la bougie [0]

#### Système de Mémoire
- Stocke les FVG détectés dans les **12 dernières bougies** (configurable)
- Utilise des arrays pour maintenir une liste active des FVG récents
- Supprime automatiquement les FVG trop anciens

#### Signal IVFG (Inversion)

**Signal LONG**:
1. Tendance baissière détectée (Close < EMA 20 4H)
2. Un FVG baissier existe dans les 12 dernières bougies
3. Le prix **clôture au-dessus** du haut du FVG baissier
4. ✅ = Inversion de la tendance confirmée

**Signal SHORT**:
1. Tendance haussière détectée (Close > EMA 20 4H)
2. Un FVG haussier existe dans les 12 dernières bougies
3. Le prix **clôture en-dessous** du bas du FVG haussier
4. ✅ = Inversion de la tendance confirmée

## 🛡️ Gestion du Risque - 3 Modes Flexibles

### Mode A: Structurel (Recommandé)
**Principe**: SL basé sur la structure de la bougie de signal

- **Stop Loss**:
  - Long: Sous le bas de la bougie de signal + buffer (ticks)
  - Short: Au-dessus du haut de la bougie de signal + buffer (ticks)
  
- **Take Profit**: 
  - Calculé selon un ratio Risque/Récompense (ex: 1:2)
  - TP = Entry + (Risk × RR_Ratio)

**Paramètres**:
- Buffer SL: 5 ticks (défaut)
- Ratio R:R: 2.0 (défaut)

**Avantages**: 
- ✅ S'adapte à la volatilité de chaque setup
- ✅ Respecte la structure du marché
- ✅ SL logique et naturel

### Mode B: Points Fixes
**Principe**: SL et TP en nombre de points fixes

- **Stop Loss**: Distance fixe en points (ex: 20 points)
- **Take Profit**: Distance fixe en points (ex: 40 points)

**Paramètres**:
- SL Points: 20 (défaut)
- TP Points: 40 (défaut)

**Avantages**:
- ✅ Simple et prévisible
- ✅ Facile à backtester
- ✅ Gestion uniforme du risque

**Inconvénients**:
- ❌ Ne s'adapte pas à la volatilité
- ❌ Peut être trop serré ou trop large

### Mode C: Basé sur l'ATR (Volatilité)
**Principe**: SL et TP proportionnels à la volatilité (ATR)

- **Stop Loss**: ATR × Multiplier SL (ex: 1.5 × ATR)
- **Take Profit**: ATR × Multiplier TP (ex: 3.0 × ATR)

**Paramètres**:
- ATR Length: 14 (défaut)
- SL Multiplier: 1.5 (défaut)
- TP Multiplier: 3.0 (défaut)

**Avantages**:
- ✅ S'adapte automatiquement à la volatilité
- ✅ Plus large en périodes volatiles
- ✅ Plus serré en périodes calmes

## 📈 Visualisation

### Éléments Affichés sur le Graphique

1. **EMA 20 (4H)** - Ligne jaune épaisse
   - Indique la tendance du timeframe supérieur

2. **Boîtes FVG**
   - 🟢 **Vert**: FVG Haussier (Bullish)
   - 🔴 **Rouge**: FVG Baissier (Bearish)
   - Transparence: 90%
   - Durée: Visible pendant la période de mémoire (12 bars)

3. **Signaux d'Entrée**
   - 🔺 **Triangle Vert**: Signal LONG
   - 🔻 **Triangle Rouge**: Signal SHORT

4. **Niveaux SL/TP**
   - Lignes rouges: Stop Loss
   - Lignes vertes: Take Profit
   - Style: Lignes pointillées

### Tableau de Statistiques (Coin Inférieur Droit)

```
┌──────────────────┬──────────┐
│ Metric           │ Value    │
├──────────────────┼──────────┤
│ Win Rate         │ XX.XX%   │
│ Profit Factor    │ X.XX     │
│ Max Drawdown     │ $XXXX.XX │
│ Total Trades     │ XXX      │
└──────────────────┴──────────┘
```

**Métriques Expliquées**:
- **Win Rate**: % de trades gagnants (Vert si ≥50%, Rouge si <50%)
- **Profit Factor**: Profit brut / Perte brute (Vert si ≥1.5, Jaune si ≥1, Rouge si <1)
- **Max Drawdown**: Perte maximale depuis un pic (en USD)
- **Total Trades**: Nombre total de positions fermées

## 🚀 Installation et Utilisation

### Étape 1: Importer dans TradingView

1. Ouvrir TradingView.com
2. Aller dans l'éditeur Pine Script (Pine Editor)
3. Créer un nouveau script
4. Copier tout le contenu de `NQ_IVFG_Strategy.pine`
5. Coller dans l'éditeur
6. Cliquer sur "Save" puis "Add to Chart"

### Étape 2: Configuration du Graphique

1. **Symbole**: NQ1! ou NQU2024 (selon votre broker)
2. **Timeframe**: 5 minutes
3. **Période**: Depuis 2018 ou plus récent
4. **Type de graphique**: Chandeliers japonais (recommandé)

### Étape 3: Paramétrage de la Stratégie

#### Panneau des Inputs (Stratégie Settings)

**Time Filter**:
- ✅ Enable Time Filter: Activé
- Session Start Hour: 1
- Session End Hour: 5

**Trend Filter**:
- Higher Timeframe: 240 (4 heures)
- EMA Length: 20

**IVFG Settings**:
- FVG Memory: 12 bars
- Minimum FVG Size: 0.0 points

**Risk Management**:
- Risk/Reward Mode: Choisir entre Mode A, B ou C
- Configurer les paramètres selon le mode choisi

**Display Settings**:
- ✅ Show FVG Boxes
- ✅ Show HTF EMA
- ✅ Show Statistics Table

### Étape 4: Lancer le Backtest

1. Ouvrir l'onglet "Strategy Tester" (en bas de l'écran)
2. Vérifier les performances:
   - Net Profit
   - Total Closed Trades
   - Percent Profitable
   - Profit Factor
   - Max Drawdown
3. Analyser l'equity curve
4. Examiner la liste des trades

## 🔧 Optimisation et Personnalisation

### Paramètres à Optimiser

1. **FVG Memory (Lookback)**
   - Plage: 8-20 bars
   - Impact: Plus long = plus de signaux mais moins précis

2. **Risk/Reward Ratio (Mode A)**
   - Plage: 1.5 - 3.0
   - Impact: Plus élevé = TP plus loin, Win Rate plus bas

3. **ATR Multipliers (Mode C)**
   - SL Mult: 1.0 - 2.5
   - TP Mult: 2.0 - 4.0
   - Impact: Ajuste à la volatilité souhaitée

4. **Time Filter**
   - Tester différentes sessions (New York, Asian, etc.)
   - Comparer les performances

### Tips d'Optimisation

1. **Ne pas sur-optimiser**: 
   - Éviter de chercher les paramètres "parfaits"
   - Privilégier la robustesse sur plusieurs périodes

2. **Walk-Forward Analysis**:
   - Optimiser sur 70% des données
   - Tester sur les 30% restants (out-of-sample)

3. **Tester sur Différents Marchés**:
   - Si ça marche sur NQ, tester sur ES, RTY
   - Vérifier la robustesse du système

## 📊 Performance Attendue

### Caractéristiques Typiques (à titre indicatif)

- **Win Rate**: 45-55%
- **Profit Factor**: 1.5-2.5+
- **Ratio Sharpe**: Variable selon le mode de gestion
- **Max Drawdown**: 10-20% du capital
- **Nombre de Trades/an**: 50-200 (selon timeframe et filtres)

**Note**: Ces chiffres sont indicatifs et varient selon les paramètres et la période de test.

## ⚠️ Avertissements et Limitations

### Points Importants

1. **Repainting**: 
   - ✅ Stratégie conçue pour éviter le repainting
   - `lookahead=barmerge.lookahead_on` utilisé correctement
   - Signaux basés sur clôture de bougie

2. **Slippage et Commissions**:
   - Inclus dans le backtest (2.50$ par contrat)
   - Ajuster selon votre broker

3. **Données Historiques**:
   - Qualité des données critique
   - Utiliser des données de qualité institutionnelle

4. **Trading en Temps Réel**:
   - Backtesting ≠ Performance réelle
   - Toujours tester en Paper Trading d'abord
   - Gérer les émotions et la discipline

5. **Gestion du Capital**:
   - Ne pas risquer plus de 1-2% par trade
   - Utiliser un money management strict

## 📚 Concepts Clés

### Fair Value Gap (FVG)

Un FVG représente une zone d'inefficience du marché où le prix a bougé trop rapidement, laissant un "gap" entre les bougies. Le marché a tendance à revenir "remplir" ces gaps.

### Inverted FVG (IVFG)

L'IVFG se produit quand le prix inverse et traverse un FVG dans la direction opposée à sa formation initiale. C'est un signal fort d'inversion de tendance.

### Multi-Timeframe Analysis

Utiliser plusieurs timeframes permet de:
- Identifier la tendance principale (4H)
- Trouver des points d'entrée précis (5m)
- Réduire les faux signaux

## 🛠️ Support Technique

### Problèmes Courants

**1. Pas de signaux générés**
- Vérifier que le time filter est correct
- Vérifier la période de données
- S'assurer que les FVG se forment sur le graphique

**2. Trop de signaux**
- Réduire le FVG Lookback
- Augmenter le Minimum FVG Size
- Ajouter des filtres supplémentaires

**3. Performance faible**
- Tester différents modes de Risk Management
- Optimiser les paramètres R:R
- Vérifier la qualité des données

### Modifications Possibles

Le code est modulaire et peut être étendu avec:
- Filtres de volatilité supplémentaires
- Trailing Stop Loss
- Gestion de position partielle
- Filtres de news/événements
- Signaux de confluence supplémentaires

## 📄 Licence et Utilisation

Ce script est fourni à des fins éducatives et de recherche.

**Disclaimer**: 
- Le trading comporte des risques de perte en capital
- Les performances passées ne garantissent pas les résultats futurs
- Utilisez ce script à vos propres risques
- Consultez un conseiller financier avant de trader

## 🤝 Contribution

Pour toute amélioration ou suggestion:
1. Testez d'abord la modification
2. Documentez les changements
3. Partagez les résultats de backtest

---

**Version**: 1.0
**Date**: 2024
**Pine Script**: Version 5
**Auteur**: Trading Strategy Development

*"Trade what you see, not what you think."*

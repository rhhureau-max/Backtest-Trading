# NQ IVFG Strategy - Documentation Complète

## Vue d'ensemble

Cette stratégie Pine Script v5 est conçue pour trader le Nasdaq 100 (NQ) en utilisant des Inverted Fair Value Gaps (IVFG) avec un filtre de tendance multi-timeframe et une fenêtre temporelle stricte.

## Caractéristiques Principales

### 1. Configuration de Base
- **Instrument**: NQ (Nasdaq 100)
- **Timeframe Principal**: 5 minutes
- **Timeframe Secondaire**: 4 heures (pour filtre de tendance)
- **Période de Test**: 2018 à aujourd'hui
- **Capital Initial**: 100,000 USD
- **Commission**: 2.50 USD par contrat
- **Slippage**: 2 ticks

### 2. Filtre Temporel (London Killzone)

La stratégie ne trade que pendant la fenêtre horaire spécifiée:
- **Heure de début**: 01:00 (par défaut)
- **Heure de fin**: 05:00 (par défaut)
- **Fuseau horaire**: UTC/GMT (pas de conversion)

**Note importante**: Le script utilise l'heure brute du graphique sans conversion de fuseau horaire. Assurez-vous que votre graphique TradingView est configuré sur le fuseau horaire souhaité.

### 3. Filtre de Tendance Multi-Timeframe

- **Indicateur**: EMA 20 sur le timeframe 4 heures
- **Fonction**: `request.security()` avec `lookahead=barmerge.lookahead_on`
- **Avantage**: Évite le repainting en utilisant les données closes de la bougie 4H précédente

**Conditions**:
- **Long**: Close actuel > EMA 20 (4H)
- **Short**: Close actuel < EMA 20 (4H)

### 4. Détection IVFG avec Mémoire

#### Qu'est-ce qu'un Fair Value Gap (FVG)?

Un FVG est un écart de prix qui indique un déséquilibre entre acheteurs et vendeurs:
- **FVG Haussier**: Écart entre high[2] et low[0] (quand low[0] > high[2])
- **FVG Baissier**: Écart entre low[2] et high[0] (quand high[0] < low[2])

#### Logique IVFG (Inverted FVG)

La stratégie inverse la logique traditionnelle des FVG:
- **Signal LONG**: Le prix clôture au-dessus du sommet d'un FVG Baissier (dans les 12 dernières bougies)
- **Signal SHORT**: Le prix clôture en-dessous du bas d'un FVG Haussier (dans les 12 dernières bougies)

#### Mémoire (Lookback)

- **Période par défaut**: 12 bougies
- **Fonctionnement**: Le script mémorise tous les FVG détectés dans les N dernières bougies
- **Nettoyage automatique**: Les FVG plus anciens sont supprimés automatiquement

### 5. Gestion du Risque - 3 Modes Flexibles

#### Mode A - Structurel (Recommandé)

Ce mode utilise la structure du marché pour définir les niveaux:

**Stop Loss**:
- Long: Juste sous le bas de la bougie de signal + buffer (en ticks)
- Short: Juste au-dessus du haut de la bougie de signal + buffer (en ticks)

**Take Profit**:
- Basé sur un ratio Risque/Récompense fixe (ex: 1:2)
- Si le risque est de 10 points, le profit sera de 20 points

**Paramètres**:
- Safety Buffer: 5 ticks (par défaut)
- Risk/Reward Ratio: 2.0 (par défaut)

**Avantages**:
- S'adapte à la volatilité de chaque trade
- Respect la structure du marché
- Stops logiques et moins susceptibles d'être touchés

#### Mode B - Points Fixes

Ce mode utilise des valeurs fixes en points:

**Stop Loss**: 20 points (par défaut)
**Take Profit**: 40 points (par défaut)

**Paramètres ajustables**:
- Fixed SL: Nombre de points pour le stop loss
- Fixed TP: Nombre de points pour le take profit

**Avantages**:
- Simple et prévisible
- Facile à backtester
- Gestion du risque constante

**Inconvénients**:
- Ne s'adapte pas à la volatilité
- Peut être trop serré ou trop large selon les conditions

#### Mode C - Basé sur l'ATR (Volatilité)

Ce mode s'adapte dynamiquement à la volatilité du marché:

**Stop Loss**: ATR(14) × 1.5 (par défaut)
**Take Profit**: ATR(14) × 3.0 (par défaut)

**Paramètres**:
- ATR Length: 14 périodes (par défaut)
- ATR SL Multiplier: 1.5 (par défaut)
- ATR TP Multiplier: 3.0 (par défaut)

**Avantages**:
- S'adapte automatiquement à la volatilité
- Plus larges stops durant les périodes volatiles
- Plus serrés durant les périodes calmes

**Recommandation**: Idéal pour les marchés avec volatilité variable

### 6. Tableau de Performance en Temps Réel

Le tableau affiche les métriques suivantes en bas à droite de l'écran:

1. **Total Trades**: Nombre total de trades fermés
2. **Win Rate**: Pourcentage de trades gagnants (vert si ≥ 50%, rouge sinon)
3. **Profit Factor**: Ratio profit brut / perte brute (vert si ≥ 1, rouge sinon)
4. **Max Drawdown**: Drawdown maximum en USD
5. **Net Profit**: Profit net total en USD (vert si positif, rouge sinon)
6. **Risk Mode**: Mode de gestion du risque actuellement utilisé

## Installation et Utilisation

### Sur TradingView

1. **Ouvrir TradingView**
   - Allez sur [TradingView](https://www.tradingview.com/)
   - Connectez-vous à votre compte

2. **Créer un nouveau script**
   - Cliquez sur "Pine Editor" en bas de l'écran
   - Créez un nouveau script (bouton "New")

3. **Copier le code**
   - Ouvrez le fichier `NQ_IVFG_Strategy.pine`
   - Copiez tout le contenu
   - Collez-le dans l'éditeur Pine

4. **Sauvegarder et appliquer**
   - Cliquez sur "Save" (ou Ctrl+S)
   - Cliquez sur "Add to Chart"

5. **Configuration du graphique**
   - Symbole: Cherchez "NQ" ou "NQ1!" (Nasdaq 100 Futures)
   - Timeframe: Réglez sur 5 minutes
   - Plage de dates: 2018 à aujourd'hui

### Configuration Initiale Recommandée

#### Pour commencer:
1. **Mode de risque**: Mode A - Structurel
2. **Filtre de tendance**: Activé
3. **Fenêtre temporelle**: 01:00 - 05:00
4. **Lookback bars**: 12

#### Optimisation:

Testez différentes combinaisons:
- Modes de risque différents
- Ratios R/R différents (Mode A)
- Multiplicateurs ATR différents (Mode C)
- Fenêtres temporelles différentes

## Paramètres Détaillés

### Time Window Filter
- `Start Hour`: Heure de début (0-23)
- `Start Minute`: Minute de début (0-59)
- `End Hour`: Heure de fin (0-23)
- `End Minute`: Minute de fin (0-59)

### Multi-Timeframe Trend Filter
- `Higher Timeframe`: "240" pour 4 heures (peut être modifié)
- `EMA Length`: Longueur de l'EMA (défaut: 20)
- `Use Trend Filter`: Active/désactive le filtre de tendance

### IVFG Signal Parameters
- `FVG Memory (Lookback Bars)`: Nombre de bougies à mémoriser (1-50)
- `Minimum FVG Size`: Taille minimale d'un FVG (0 = pas de minimum)

### Risk Management Mode
- Sélection du mode via menu déroulant
- Chaque mode a ses propres paramètres

### Display Options
- `Show FVG Boxes`: Affiche les boîtes FVG sur le graphique
- `Show 4H EMA`: Affiche l'EMA 4H sur le graphique 5m
- `Show Performance Table`: Affiche le tableau de performance

## Interprétation des Signaux

### Signal d'Entrée Long (Flèche verte)
Conditions remplies:
1. Un FVG Baissier existe dans les 12 dernières bougies
2. Le prix clôture au-dessus du sommet de ce FVG
3. La tendance 4H est haussière (Close > EMA 20)
4. L'heure est dans la fenêtre de trading (01:00-05:00)

### Signal d'Entrée Short (Flèche rouge)
Conditions remplies:
1. Un FVG Haussier existe dans les 12 dernières bougies
2. Le prix clôture en-dessous du bas de ce FVG
3. La tendance 4H est baissière (Close < EMA 20)
4. L'heure est dans la fenêtre de trading (01:00-05:00)

## Visualisation

### Éléments sur le graphique:
- **Ligne jaune**: EMA 20 du timeframe 4H
- **Boîtes vertes**: FVG Haussiers (semi-transparentes)
- **Boîtes rouges**: FVG Baissiers (semi-transparentes)
- **Flèches vertes**: Points d'entrée Long
- **Flèches rouges**: Points d'entrée Short
- **Tableau**: Métriques de performance en temps réel

## Conseils d'Optimisation

### 1. Période de Test
- Utilisez une période suffisamment longue (minimum 2-3 ans)
- Incluez différentes conditions de marché (bull, bear, range)

### 2. Walk-Forward Analysis
- Optimisez sur une période
- Testez sur la période suivante
- Validez la robustesse de la stratégie

### 3. Paramètres à Tester
- **Lookback period**: 8, 10, 12, 15, 20
- **EMA Length**: 15, 20, 25, 30
- **RR Ratio**: 1.5, 2.0, 2.5, 3.0
- **Time Windows**: Différentes sessions (Tokyo, London, New York)

### 4. Combinaisons de Modes
Testez les 3 modes de risque:
- Mode A avec RR 1.5, 2.0, 2.5
- Mode B avec différents points fixes
- Mode C avec différents multiplicateurs ATR

## Limitations et Considérations

### 1. Repainting
Le script utilise `lookahead=barmerge.lookahead_on` pour éviter le repainting sur le filtre de tendance. Les signaux FVG sont calculés sur les bougies closes, donc pas de repainting.

### 2. Slippage et Commissions
La stratégie inclut:
- Commissions: 2.50 USD par contrat
- Slippage: 2 ticks

Ajustez ces valeurs selon votre broker.

### 3. Conditions de Marché
Cette stratégie fonctionne mieux dans:
- Marchés tendanciels
- Périodes de volatilité moyenne
- Sessions spécifiques (London Killzone)

### 4. Gestion du Capital
Le script utilise 100% du capital par trade. Pour un money management plus prudent:
- Modifiez `default_qty_value` dans les paramètres strategy()
- Utilisez un pourcentage plus faible (ex: 10-20%)

## Support et Modifications

### Pour modifier la stratégie:

1. **Changer le timeframe secondaire**:
```pinescript
htfTimeframe = input.timeframe("240", "Higher Timeframe (4H)", group=trendFilterGroup)
```

2. **Ajouter d'autres filtres**:
Ajoutez vos propres conditions dans les sections:
```pinescript
longCondition = longSignal and (not useTrendFilter or isBullishTrend) and isInTimeWindow() and [votre_filtre]
```

3. **Modifier les visuels**:
Ajustez les couleurs et styles dans les sections `plot()` et `plotshape()`

## Avertissements

⚠️ **Trading à Risque**:
- Les performances passées ne garantissent pas les résultats futurs
- Testez toujours en compte démo avant d'utiliser de l'argent réel
- Ne risquez jamais plus que ce que vous pouvez vous permettre de perdre
- Cette stratégie est fournie à des fins éducatives uniquement

⚠️ **Backtesting vs Trading Réel**:
- Le backtesting peut ne pas refléter exactement les conditions réelles
- Le slippage réel peut être plus important
- Les conditions de marché peuvent changer

## Changelog

### Version 1.0 (2025-12-27)
- Implémentation initiale
- 3 modes de gestion du risque
- Filtre multi-timeframe avec EMA 20
- Détection IVFG avec mémoire (12 bougies)
- Fenêtre temporelle London Killzone
- Tableau de performance en temps réel
- Visualisation des FVG

## Contact et Support

Pour toute question ou amélioration, veuillez ouvrir une issue sur le dépôt GitHub.

---

**Bonne chance avec votre trading! 📈**

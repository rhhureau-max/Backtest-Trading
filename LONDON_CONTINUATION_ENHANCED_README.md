# London Continuation Enhanced - Avec SL/TP et Précision M1

## Vue d'ensemble

Version améliorée de la stratégie London Continuation avec gestion rigoureuse du risque (Stop Loss et Take Profit) et exécution ultra-précise sur données 1 minute pour éviter le look-ahead bias.

## Différences avec la Version Originale

| Aspect | Version Originale | Version Enhanced |
|--------|------------------|------------------|
| **Timeframe Exécution** | 15m uniquement | 15m pour setup + 1m pour exécution |
| **Stop Loss** | Aucun (exit temporel) | SL basé sur Asian Range |
| **Take Profit** | Exit fixe 07:00 CST | 3 scénarios (1R, 1.5R, 2R) |
| **Précision** | Look-ahead bias possible | Évite le look-ahead bias |
| **Asian Range** | 19:00-00:00 | 18:00-00:00 (6h au lieu de 5h) |
| **Force Close** | 07:00 CST | 15:15 CST |

## Paramètres de la Stratégie Enhanced

### 1. Configuration Temporelle (Chicago Time - CST)

**Asian Session (Range de référence)** : 18:00 (Jour-1) à 00:00 (Jour)
- Calcule `Asian_High` et `Asian_Low`
- Établit les bornes de référence pour le setup

**London Killzone (Fenêtre de tir)** : 01:00 à 04:00 CST
- Détection du setup sur données 15m
- Première clôture cassant la Asian Range = déclenchement

**Force Close** : 15:15 CST
- Si ni SL ni TP touché, clôture forcée en fin de journée

### 2. Règles d'Entrée (Setup)

Le script surveille les clôtures sur timeframe 15m pendant la London Killzone :

- **LONG** : Première clôture 15m > `Asian_High`
- **SHORT** : Première clôture 15m < `Asian_Low`

Le prix de clôture devient le **Prix d'Entrée**.

### 3. Gestion du Risque (Stop Loss)

**Calcul du Stop Loss** :
```
LONG  : SL = Asian_Low - 2 points
SHORT : SL = Asian_High + 2 points
```

**Définition du Risque (R)** :
```
R = |Entry_Price - SL_Price|
```

Cette distance représente 1R (1 unité de risque).

### 4. Objectifs (Take Profits)

Le script simule **3 scénarios distincts** pour chaque trade :

1. **TP1 (1R)** : Sortie à 1 fois le risque
   - LONG: `Entry + R`
   - SHORT: `Entry - R`

2. **TP2 (1.5R)** : Sortie à 1.5 fois le risque
   - LONG: `Entry + 1.5 * R`
   - SHORT: `Entry - 1.5 * R`

3. **TP3 (2R)** : Sortie à 2 fois le risque
   - LONG: `Entry + 2 * R`
   - SHORT: `Entry - 2 * R`

### 5. Exécution Précise (M1)

**CRUCIAL** : Une fois le setup déclenché sur 15m, le script itère sur les données **1 minute (M1)** pour vérifier ce qui est touché en premier : le SL ou le TP.

Cela évite le **look-ahead bias** où une bougie H1/H4 touche à la fois le high et le low, créant une illusion de précision.

**Logique d'exécution M1** :
```python
Pour chaque bougie M1 après l'entrée:
    Si direction == LONG:
        Si Low <= SL_Price -> Exit au SL (perte)
        Si High >= TP_Price -> Exit au TP (gain)
    
    Si direction == SHORT:
        Si High >= SL_Price -> Exit au SL (perte)
        Si Low <= TP_Price -> Exit au TP (gain)
```

Si ni SL ni TP touché avant 15:15 → **Force Close** au dernier prix.

## Résultats du Backtest (2018-2025)

### Statistiques Comparatives - 3 Scénarios

| Scénario | Trades | Win Rate % | Total P&L | Profit Factor | Expectancy | Avg R |
|----------|--------|------------|-----------|---------------|------------|-------|
| **1.0R** | 1,595 | 50.41% | -2,353.71 | 0.96 | -1.48 | 0.01 |
| **1.5R** | 1,595 | 42.45% | -3,393.56 | 0.95 | -2.13 | 0.00 |
| **2.0R** | 1,595 | 38.31% | -3,109.38 | 0.96 | -1.95 | 0.01 |

### Analyse Détaillée par Scénario

#### Scénario 1R (Take Profit Conservateur)
- **Wins**: 804 trades (50.41%)
- **Losses**: 791 trades
- **Avg Win**: +76.40 points
- **Avg Loss**: -80.63 points
- **Total P&L**: -2,353.71 points

#### Scénario 1.5R (Take Profit Modéré)
- **Wins**: 677 trades (42.45%)
- **Losses**: 918 trades
- **Avg Win**: +101.56 points
- **Avg Loss**: -78.60 points
- **Total P&L**: -3,393.56 points

#### Scénario 2R (Take Profit Agressif)
- **Wins**: 611 trades (38.31%)
- **Losses**: 984 trades
- **Avg Win**: +119.06 points
- **Avg Loss**: -77.09 points
- **Total P&L**: -3,109.38 points

## Observations Clés

### 1. Impact du SL Fixe
L'implémentation d'un **Stop Loss fixe** (Asian_Low/High ± 2pts) change radicalement la performance par rapport à la version originale :

- **Version Originale** (exit temporel à 07:00) : 59.95% WR, +14,583 pts
- **Version Enhanced** (SL fixe) : ~50% WR, P&L négatif

**Pourquoi ?** 
- Le SL fixe est souvent trop serré durant la volatilité de Londres
- La moyenne des pertes (-77 à -81 pts) est proche de la moyenne des gains (+76 à +119 pts)
- Le ratio Risk/Reward n'est pas favorable avec ce placement de SL

### 2. Trade-off Win Rate vs R-Multiple

Plus le TP est agressif (2R), plus le win rate diminue :
- **1R** : 50.41% WR mais petits gains
- **2R** : 38.31% WR mais gains plus importants

**Problème** : Le profit factor reste sous 1.0 dans tous les cas.

### 3. Leçons pour l'Amélioration

Pour rendre cette stratégie profitable avec SL/TP fixes, il faudrait :

1. **Repositionner le SL** : Plus loin (ex: Asian_Low - 10pts au lieu de -2pts)
2. **Ajouter des filtres** : Structure H4/Daily, volume profile
3. **Timing d'entrée** : Attendre un pullback après cassure
4. **Partial exits** : Prendre 50% à 1R, laisser courir le reste
5. **Trailing stop** : Déplacer le SL au breakeven après +0.5R

## Structure des Fichiers

### Fichiers d'Entrée
- **Setup Detection** : `YYYY 15m.csv` (timeframe 15 minutes)
- **Execution** : `YYYY 1m.csv.zip` ou `YYYY 1m.csv` (timeframe 1 minute)
- Format : CSV avec délimiteur `;`

### Fichiers de Sortie

1. **london_continuation_comparison.csv**
   - Tableau comparatif des 3 scénarios
   - Métriques : Win Rate, PF, Expectancy, etc.

2. **london_continuation_1.0R_results.csv**
   - Détails complets de tous les trades 1R
   - Colonnes : Date, Entry, Exit, SL, TP, Direction, P&L, etc.

3. **london_continuation_1.5R_results.csv**
   - Détails complets de tous les trades 1.5R

4. **london_continuation_2.0R_results.csv**
   - Détails complets de tous les trades 2R

5. **london_continuation_equity_curves.csv**
   - Courbes d'équité cumulatives pour les 3 scénarios

6. **london_continuation_equity_curves.png**
   - Graphique visuel des courbes d'équité

## Utilisation

### Installation
```bash
pip install pandas numpy matplotlib
```

### Exécution
```bash
python3 london_continuation_enhanced.py
```

Le script :
1. Charge automatiquement les données 15m et 1m
2. Détecte les setups sur 15m
3. Exécute avec précision M1
4. Génère les rapports pour les 3 scénarios
5. Crée les courbes d'équité

### Temps d'Exécution
- Données : ~2.77 millions de bougies 1m
- Durée : ~3-5 minutes sur machine standard

## Comparaison Version Originale vs Enhanced

| Métrique | Originale (Exit Temporel) | Enhanced (SL/TP Fixe) |
|----------|---------------------------|----------------------|
| **Timeframe** | 15m uniquement | 15m + 1m |
| **Total Trades** | 1,186 | 1,595 |
| **Win Rate** | 59.95% | ~40-50% |
| **Total P&L** | +14,583 pts | -2,353 à -3,393 pts |
| **Profit Factor** | 1.80 | 0.95-0.96 |
| **Avantage** | Profitabilité prouvée | Gestion du risque claire |
| **Inconvénient** | Pas de SL défini | Nécessite optimisation SL |

## Recommandations

### Pour Usage en Trading Réel

**Option 1 - Hybride** : Utiliser la version originale (exit temporel) mais avec un **SL catastrophe** très large (ex: -100 pts) pour éviter les crashs.

**Option 2 - Enhanced Optimisé** : Travailler sur l'optimisation du placement SL :
- Backtester avec SL = Asian_Low - [5, 10, 15, 20] points
- Tester des SL adaptatifs basés sur l'ATR
- Implémenter un trailing stop

**Option 3 - Filtrage** : N'activer le trade que si :
- H4 est aligné avec la direction
- Volume > seuil significatif
- Pas d'annonce macro dans l'heure

## Avertissements

⚠️ **Performance Négative**
- La version Enhanced avec SL fixe montre une performance négative
- **NE PAS TRADER EN RÉEL** sans optimisation supplémentaire
- Ces résultats démontrent l'importance du placement du Stop Loss

⚠️ **Données & Slippage**
- Les résultats supposent une exécution parfaite au prix exact
- En réel : slippage de 1-2 points sur NQ pendant Londres
- Frais de courtage : ~$0.50-1.00 par aller-retour

⚠️ **Look-Ahead Bias Éliminé**
- Version Enhanced élimine le look-ahead bias via M1
- Les résultats sont plus réalistes (mais négatifs !)
- Cela valide l'importance de tester avec données tick/M1

## Conclusion

Cette version Enhanced démontre que :
1. ✅ La précision M1 est essentielle pour éviter le look-ahead bias
2. ❌ Un SL fixe trop serré détruit la profitabilité
3. 📊 La version originale (exit temporel) reste supérieure
4. 🔧 Des optimisations sont nécessaires pour rendre les SL/TP fixes rentables

Le code est production-ready et peut servir de base pour :
- Optimiser les niveaux SL/TP
- Tester d'autres filtres d'entrée
- Implémenter des exits partiels
- Comparer d'autres stratégies avec rigueur

## Support

Pour questions ou améliorations, créer une issue dans le repository GitHub.

## Licence

Code fourni à des fins éducatives. Utilisez à vos propres risques.

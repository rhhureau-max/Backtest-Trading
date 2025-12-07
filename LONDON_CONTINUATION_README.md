# London Continuation Backtesting Strategy

## Vue d'ensemble

Cette stratégie de backtesting identifie les opportunités de "London Continuation" sur les Futures Nasdaq (NQ) en utilisant les Killzones temporelles institutionnelles et les concepts de Market Microstructure.

## Paramètres de la Stratégie

### Fuseaux Horaires
**IMPORTANT**: Toutes les données sont déjà en heure de Chicago (CST/CDT). Aucune conversion de fuseau horaire n'est effectuée.

### Plages Horaires Clés

1. **Asian Range (Référence)**: 
   - Période: 19:00 (Jour-1) à 00:00 (Jour) CST
   - Objectif: Établir les niveaux High/Low de référence
   - Utilisation: Ces niveaux servent de bornes pour détecter les cassures

2. **London Killzone (Zone d'Entrée)**:
   - Période: 01:00 à 04:00 CST
   - Objectif: Fenêtre exclusive pour les prises de position
   - Importance: Les mouvements institutionnels se produisent durant cette période

3. **Exit Time (Sortie)**:
   - Heure: 07:00 CST
   - Raison: Juste avant l'ouverture de New York pour capturer le mouvement pur de Londres

## Logique Algorithmique

### 1. Calcul de la Asian Range
```
Asian_High = Maximum des High entre 19:00 (J-1) et 00:00 (J)
Asian_Low = Minimum des Low entre 19:00 (J-1) et 00:00 (J)
Asian_Mid = (Asian_High + Asian_Low) / 2
```

### 2. Détection de Cassure (Breakout)

**Conditions d'Entrée LONG**:
- La bougie doit **clôturer** au-dessus du `Asian_High`
- Doit se produire entre 01:00 et 04:00 CST (London Killzone)
- Volume > Moyenne Mobile 20 périodes

**Conditions d'Entrée SHORT**:
- La bougie doit **clôturer** en-dessous du `Asian_Low`
- Doit se produire entre 01:00 et 04:00 CST (London Killzone)
- Volume > Moyenne Mobile 20 périodes

### 3. Validation de Continuation (Anti-Fakeout)

**Pour les positions LONG**:
- Le prix ne doit **PAS** redescendre sous `Asian_Mid` dans les 2 heures suivant l'entrée
- Évite les fausses cassures haussières

**Pour les positions SHORT**:
- Le prix ne doit **PAS** remonter au-dessus de `Asian_Mid` dans les 2 heures suivant l'entrée
- Évite les fausses cassures baissières

### 4. Sortie
- Exit systématique à 07:00 CST
- Calcul du P&L en points NQ

## Résultats du Backtest (2018-2025)

### Statistiques Globales
```
Période: 2018-2025 (7+ ans)
Total Trades: 1,186 setups
Win Rate: 59.95%
Total P&L: +14,583.32 points
Profit Factor: 1.80

Moyenne Win: +45.99 points
Moyenne Loss: -38.14 points
Ratio W/L: 1.21
```

### Performance par Direction
```
LONG Trades:  678 trades | 61.80% WR | +7,684.06 points
SHORT Trades: 508 trades | 57.48% WR | +6,899.26 points
```

### Performance Annuelle
| Année | Trades | Win Rate | P&L (points) |
|-------|--------|----------|--------------|
| 2018  | 163    | 58.28%   | +463.73      |
| 2019  | 149    | 61.74%   | +1,012.99    |
| 2020  | 150    | 62.00%   | +2,980.55    |
| 2021  | 150    | 55.33%   | +1,435.30    |
| 2022  | 146    | 63.01%   | +3,659.91    |
| 2023  | 141    | 68.09%   | +2,316.00    |
| 2024  | 147    | 59.18%   | +2,047.79    |
| 2025  | 140    | 52.14%   | +667.05      |

## Structure des Données

### Fichiers d'Entrée
- Timeframe utilisé: **15 minutes** (fichiers `YYYY 15m.csv`)
- Format: CSV avec délimiteur point-virgule (`;`)
- Colonnes: Date, Time, Open, High, Low, Close, Volume
- Format de date: `DD/MM/YYYY HH:MM:SS`

### Fichier de Sortie
`london_continuation_results.csv` contient:
- **Date**: Date du trade
- **Entry_Time**: Heure d'entrée précise
- **Direction**: LONG ou SHORT
- **Entry_Price**: Prix d'entrée
- **Exit_Time**: Heure de sortie (généralement 07:00)
- **Exit_Price**: Prix de sortie
- **PnL_Points**: Résultat en points NQ
- **Result**: WIN ou LOSS
- **Asian_High**: Niveau haut de la range asiatique
- **Asian_Low**: Niveau bas de la range asiatique
- **Asian_Range**: Amplitude de la range
- **Volume**: Volume de la bougie d'entrée
- **Volume_MA_20**: Moyenne mobile du volume (20 périodes)

## Utilisation du Script

### Installation
```bash
pip install pandas numpy
```

### Exécution
```bash
python3 london_continuation_backtest.py
```

### Options
Le script charge automatiquement toutes les données disponibles de 2018 à 2025. Pour modifier le timeframe ou les années, éditer la fonction `main()`:

```python
# Utiliser 1H au lieu de 15m
df = load_nq_data(timeframe='1H')

# Charger seulement certaines années
df = load_nq_data(years=[2022, 2023, 2024], timeframe='15m')
```

## Interprétation des Résultats

### Points Forts de la Stratégie
1. **Win Rate Solide**: ~60% de taux de réussite sur 7+ années
2. **Cohérence**: Profitabilité sur toutes les années (sauf 2025 partiel)
3. **Biais Long Efficace**: Les LONG ont un meilleur win rate (61.80%)
4. **Profit Factor Sain**: 1.80 indique un ratio risque/récompense favorable

### Points d'Amélioration Potentiels
1. **Taille de Position**: Le script simule 1 contrat. Adapter selon le capital
2. **Stop Loss**: Actuellement exit fixe à 07:00. Pourrait ajouter des stops dynamiques
3. **Take Profit**: Pourrait implémenter des niveaux de TP partiels
4. **Filtres Additionnels**: 
   - Structure H4/Daily pour biais directionnel
   - Sessions de volatilité (NFP, FOMC)
   - Gap d'ouverture asiatique

## Avertissements

⚠️ **Backtesting vs Trading Réel**
- Les résultats passés ne garantissent pas les performances futures
- Le slippage et les frais de courtage ne sont pas inclus
- L'exécution en temps réel peut différer

⚠️ **Risques**
- Cette stratégie nécessite une surveillance active pendant la session de Londres
- Les périodes de faible volatilité peuvent réduire les opportunités
- Les annonces macroéconomiques peuvent créer des faux signaux

## Support et Contact

Pour des questions ou des améliorations, veuillez créer une issue dans le repository GitHub.

## Licence

Ce code est fourni à des fins éducatives. Utilisez-le à vos propres risques.

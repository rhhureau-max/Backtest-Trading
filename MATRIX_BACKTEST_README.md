# NQ Matrix Backtest - Documentation

## Vue d'Ensemble

Ce script implémente un backtest matriciel exhaustif d'une stratégie de trading NQ avec analyse comparative de **4 types de Stop Loss** contre **5 types de Take Profit**, générant **20 combinaisons** différentes.

## Stratégie d'Entrée (Identique pour toutes les simulations)

### Sessions Définies (Timezone Chicago)
- **Référence (Tokyo, J-1)**: 19:00 à 23:00 (jour précédent)
- **Fenêtre de tir (London, J)**: 01:00 à 04:00 (jour actuel)

### Conditions d'Entrée

1. **Sweep**: Le prix doit casser le Tokyo High ou Tokyo Low
2. **Création FVG**:
   - **Setup Short**: Après cassure du Tokyo High, un FVG Haussier se forme
   - **Setup Long**: Après cassure du Tokyo Low, un FVG Baissier se forme
3. **Trigger Inversion**:
   - **Entrée Short**: Une bougie clôture SOUS le FVG Haussier
   - **Entrée Long**: Une bougie clôture AU-DESSUS du FVG Baissier

**Prix d'entrée**: Prix de clôture de la bougie signal

## Définition des 4 Variantes de Stop Loss

### SL1 - Swing Extreme (Conservateur)
- **Short**: Plus haut atteint durant le sweep + 2 points de buffer
- **Long**: Plus bas atteint durant le sweep - 2 points de buffer
- **Caractéristique**: Maximum de protection, risque le plus élevé

### SL2 - Inversion Border (Technique)
- **Short**: Borne supérieure du FVG Haussier cassé
- **Long**: Borne inférieure du FVG Baissier cassé
- **Caractéristique**: Placement technique basé sur la structure du FVG

### SL3 - Signal Candle (Agressif)
- **Short**: High de la bougie signal + 0.25 points
- **Long**: Low de la bougie signal - 0.25 points
- **Caractéristique**: Risque le plus faible, mais plus facilement touché

### SL4 - Mean Threshold (Institutionnel)
- **Calcul**: 50% entre le prix d'entrée et SL1
- **Caractéristique**: Compromis entre protection et risque

## Définition des 5 Objectifs (Take Profit)

### TP1 - 1R (Risk/Reward 1:1)
- Distance Entrée ↔ SL choisie × 1.0

### TP2 - 1.5R (Risk/Reward 1:1.5)
- Distance Entrée ↔ SL choisie × 1.5

### TP3 - 2R (Risk/Reward 1:2)
- Distance Entrée ↔ SL choisie × 2.0

### TP4 - Range (Retour à l'extrémité opposée)
- **Short**: Tokyo Low
- **Long**: Tokyo High

### TP5 - EQ (Equilibrium)
- Retour au Tokyo Equilibrium ((High + Low) / 2)

## Résultats du Backtest (2018-2025)

### Statistiques Globales
- **Période analysée**: 2018-2025 (7+ ans)
- **Jours de trading**: 2,449
- **Setups identifiés**: 1,618
- **Combinaisons testées**: 20 (4 SL × 5 TP)

### Top 3 Meilleures Combinaisons

#### 🥇 **SL3 + TP1 (1R)** - MEILLEURE COMBINAISON
- **Win Rate**: 64.46%
- **Net Profit**: +557.68 points
- **Avg RR Realized**: 0.29
- **Max Drawdown**: 5 pertes consécutives
- **Caractéristique**: SL agressif avec TP proche = haute probabilité

#### 🥈 **SL1 + TP5 (EQ)** - MEILLEURE GESTION DU RISQUE
- **Win Rate**: 70.58%
- **Net Profit**: -1,181.14 points
- **Avg RR Realized**: 0.12
- **Max Drawdown**: 5 pertes consécutives
- **Caractéristique**: Très haut winrate mais RR faible

#### 🥉 **SL3 + TP2 (1.5R)** - BON COMPROMIS
- **Win Rate**: 51.48%
- **Net Profit**: -238.21 points
- **Avg RR Realized**: 0.29
- **Max Drawdown**: 9 pertes consécutives
- **Caractéristique**: Balance entre winrate et RR

### Tableau Complet des Résultats

| Type_SL | Type_TP | Nb_Trades | Winrate_% | Net_Profit_Points | Avg_RR | Max_DD |
|---------|---------|-----------|-----------|-------------------|--------|--------|
| SL1 | 1R | 1618 | 50.80 | -15034.13 | 0.02 | 9 |
| SL1 | 1.5R | 1618 | 42.21 | -12150.43 | 0.06 | 13 |
| SL1 | 2R | 1618 | 36.28 | -10145.17 | 0.09 | 16 |
| SL1 | Range | 1618 | 43.14 | -11261.85 | 0.10 | 10 |
| SL1 | EQ | 1618 | 70.58 | -1181.14 | 0.12 | 5 |
| SL2 | 1R | 1618 | 42.09 | -3101.46 | -0.16 | 10 |
| SL2 | 1.5R | 1618 | 30.78 | -4486.75 | -0.23 | 20 |
| SL2 | 2R | 1618 | 24.60 | -4727.37 | -0.26 | 20 |
| SL2 | Range | 1618 | 13.35 | -6746.21 | -0.43 | 42 |
| SL2 | EQ | 1618 | 37.64 | -5417.12 | -0.38 | 12 |
| **SL3** | **1R** | **1618** | **64.46** | **+557.68** | **0.29** | **5** ⭐ |
| SL3 | 1.5R | 1618 | 51.48 | -238.21 | 0.29 | 9 |
| SL3 | 2R | 1618 | 43.14 | -636.12 | 0.29 | 11 |
| SL3 | Range | 1618 | 10.75 | -3343.67 | -0.17 | 53 |
| SL3 | EQ | 1618 | 38.57 | -4201.71 | -0.45 | 20 |
| SL4 | 1R | 1618 | 35.91 | -17695.05 | -0.28 | 19 |
| SL4 | 1.5R | 1618 | 28.62 | -18450.57 | -0.28 | 24 |
| SL4 | 2R | 1618 | 23.18 | -19255.11 | -0.30 | 24 |
| SL4 | Range | 1618 | 17.61 | -19739.80 | -0.30 | 29 |
| SL4 | EQ | 1618 | 47.96 | -10505.70 | -0.18 | 10 |

## Analyse et Recommandations

### ✅ Combinaisons avec Win Rate ≥ 40%

9 combinaisons atteignent ce seuil, avec **SL3 + 1R** en tête.

### 🎯 Meilleur Compromis Sécurité/Profitabilité

**SL3 (Signal Candle) + TP1 (1R)** offre:
- ✅ Win Rate élevé (64.46%)
- ✅ Seule combinaison avec profit net positif (+557.68 points)
- ✅ Drawdown minimal (5 pertes consécutives)
- ✅ RR réalisé acceptable (0.29)

### 📊 Insights Clés

1. **SL3 (Agressif)** fonctionne mieux avec des TP courts (1R, 1.5R, 2R)
2. **SL1 (Conservateur)** a un winrate élevé avec TP5 (EQ) mais RR faible
3. **SL2 (FVG Border)** performe mal, probablement trop invalidé par le retracement
4. **SL4 (Mean Threshold)** ne montre aucune combinaison profitable
5. **TP Range et TP EQ** fonctionnent mieux avec SL1 qu'avec des SL plus serrés

### 🚀 Recommandation de Trading

**Configuration optimale**: **SL3 + TP1**
- Placement: Signal Candle High/Low + 0.25 points
- Objectif: 1:1 Risk/Reward
- Gestion: Sortie immédiate à 1R, pas de trailing stop

## Utilisation

```bash
# Installer les dépendances
pip install pandas numpy

# Exécuter le backtest
python nq_matrix_backtest.py
```

## Outputs

1. **Console**: Tableau comparatif complet des 20 combinaisons
2. **CSV**: `nq_matrix_results.csv` avec tous les résultats détaillés

## Notes Techniques

- **Données**: 5 minutes, timezone Chicago (CST/CDT)
- **Format CSV**: Délimiteur point-virgule (;)
- **Date Format**: DD/MM/YYYY
- **Lookahead**: Maximum 1000 barres (~3.5 jours)
- **Exclusion**: Trades sans SL/TP touchés dans la fenêtre = considérés comme pertes

## Avertissements

⚠️ **Disclaimer**: Ce backtest est fourni à des fins éducatives et de recherche. Les performances passées ne garantissent pas les résultats futurs. Toujours tester en simulation avant le trading réel.

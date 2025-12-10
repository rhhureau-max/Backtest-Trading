# NQ Partial Exit Position Management - Documentation

## Vue d'Ensemble

Ce script teste des stratégies de gestion de position avec sortie partielle pour optimiser la stratégie SL3 + TP1 (1R) qui est actuellement la meilleure configuration identifiée dans l'analyse matricielle.

## Objectif

Tester si une sortie partielle (50% à 1R + 50% runner) permet de **garder le taux de réussite élevé tout en capturant plus de profit** sur les gros mouvements.

## Stratégie d'Entrée (Identique pour tous les scénarios)

### Configuration
- **Stop Loss**: SL3 (Signal Candle High/Low + 0.25pt buffer)
- **Setup**: Inversion FVG sur session Tokyo-London
- **Timeframe**: 5 minutes
- **Sessions**: Tokyo (19:00-23:00 J-1) + London Killzone (01:00-04:00 J)

## 3 Scénarios Testés

### Scénario A - Full Exit 1R (Baseline)
**Configuration**:
- 100% de la position clôturée à 1R
- Pas de runner
- C'est notre référence actuelle

**Caractéristique**: Simplicité maximale, capture systématique de 1R quand le trade est gagnant.

### Scénario B - Hybrid 2R
**Configuration**:
1. **Premier Objectif (TP1 à 1R)**:
   - Si touché → Clôture 50% de la position
   - SL des 50% restants déplacé au prix d'entrée (Break-Even)
   
2. **Second Objectif (TP2 à 2R)**:
   - Les 50% restants visent 2R
   - Si prix revient au Break-Even → Gain total = 0.5R
   - Si TP2 touché → Gain total = 1.5R (0.5R + 1R)

**Calcul PnL**:
- SL initial touché avant TP1: **-1R**
- TP1 touché puis retour à BE: **+0.5R**
- TP1 touché puis TP2 touché: **+1.5R**

### Scénario C - Hybrid EQ (Tokyo Equilibrium)
**Configuration**:
1. **Premier Objectif (TP1 à 1R)**:
   - Si touché → Clôture 50% de la position
   - SL des 50% restants déplacé au prix d'entrée (Break-Even)
   
2. **Second Objectif (TP2 au Tokyo EQ)**:
   - Les 50% restants visent le Tokyo Equilibrium
   - Si prix revient au Break-Even → Gain total = 0.5R
   - Si TP2 touché → Gain calculé dynamiquement selon distance

**Note importante**: Si Tokyo EQ est plus proche que 1R (incohérence), le trade est traité comme un Scénario A standard.

**Calcul PnL**:
- Distance TP2 variable selon la distance entre Entry et Tokyo EQ
- Gain total = 0.5R (de TP1) + 0.5 × (Distance_EQ / Risk)

## Logique de Simulation

### Chronologie Intra-Bougie
Pour chaque bougie de 5 minutes après l'entrée:

1. **Phase 1** (Avant TP1):
   - Vérifier si SL initial touché → Trade perdu
   - Vérifier si TP1 touché → Passer en Phase 2

2. **Phase 2** (Après TP1, pour Scénarios B et C):
   - Vérifier si Break-Even touché → Gain partiel (0.5R)
   - Vérifier si TP2 touché → Gain complet (variable selon scénario)

### Règle du "Pire Cas"
Si une bougie contient à la fois le TP et le SL, on considère que le SL est touché en premier (approche conservatrice).

## Résultats du Backtest (2018-2025)

### Statistiques Globales
- **Période analysée**: 2018-2025 (7+ ans)
- **Setups identifiés**: 1,618
- **Scénarios testés**: 3

### Tableau Comparatif

| Scénario | Net Profit (pts) | Winrate % | Runner Success % | Avg R | Max DD |
|----------|------------------|-----------|------------------|-------|--------|
| **A (Full Exit 1R)** | **+557.68** ✅ | **64.46** | N/A | **0.29** | **5** |
| B (Hybrid 2R) | -494.92 | 64.46 | 21.48 | 0.11 | 5 |
| C (Hybrid EQ) | -283.36 | 49.07 | 13.60 | 0.17 | 5 |

### Analyse Détaillée

#### 🏆 Meilleur Scénario: A (Full Exit 1R)
- **Net Profit**: +557.68 points (SEUL scenario profitable!)
- **Winrate**: 64.46%
- **Avg R**: 0.29
- **Max Drawdown**: 5 pertes consécutives

#### Scénario B (Hybrid 2R)
- **Performance**: -494.92 points (-1,052.60 pts vs baseline)
- **Runner Success**: Seulement 21.48% des runners atteignent 2R
- **Problème**: 78.52% des runners reviennent au Break-Even, annulant le gain potentiel
- **Winrate**: Identique à baseline (64.46%) car TP1 touché au même taux
- **Conclusion**: Les retours au BE sabotent la profitabilité

#### Scénario C (Hybrid EQ)
- **Performance**: -283.36 points (-841.04 pts vs baseline)
- **Runner Success**: Seulement 13.60% des runners atteignent Tokyo EQ
- **Problème**: 86.40% des runners reviennent au Break-Even
- **Winrate**: Chute à 49.07% (car certains trades passent en "loss" total)
- **Conclusion**: Tokyo EQ trop éloigné, runners inefficaces

## Insights Clés

### 1. Pourquoi les Runners Échouent?
- **Taux de retour au BE élevé**: 78-86% des runners reviennent au Break-Even
- **Pression vendeur/acheteur**: Après 1R, le marché manque de momentum pour continuer
- **Structure ICT**: Le setup "Inversion FVG" est conçu pour des mouvements rapides et courts

### 2. Le Piège du "Laisser Courir"
- **Théorie**: Capturer les gros mouvements semble attrayant
- **Réalité**: Sur ce setup spécifique, cela détruit la profitabilité
- **Mathématique**: 0.5R de gain partiel < 1R de gain full exit

### 3. Force de la Simplicité
Le Scénario A performe mieux car:
- ✅ Capture systématique 1R à chaque win
- ✅ Pas de décisions complexes intra-trade
- ✅ Momentum short-term optimal pour cette structure

## Recommandation Finale

### ✅ GARDER LE BASELINE (Scénario A - Full Exit 1R)

**Raisons**:
1. **Seul scénario rentable** sur 7+ ans de données
2. **Simplicité d'exécution** (pas de gestion complexe)
3. **Runners ajoutent zéro valeur** (21% success rate insuffisant)
4. **Winrate optimal** maintenu sans compromis

**Ne PAS utiliser**:
- ❌ Partial exits avec runners
- ❌ Break-even stops après TP1
- ❌ Objectifs à 2R ou Tokyo EQ

**Configuration optimale confirmée**:
- **SL**: SL3 (Signal Candle + 0.25pt)
- **TP**: 1R (Risk/Reward 1:1)
- **Exit**: 100% de la position à TP1

## Utilisation

```bash
# Installer les dépendances
pip install pandas numpy

# Exécuter l'optimisation
python nq_partial_exit_optimization.py
```

## Outputs

1. **Console**: Tableau comparatif des 3 scénarios avec métriques détaillées
2. **CSV**: `nq_partial_exit_results.csv` avec résultats exportés

## Leçon Stratégique

> **"On trading, simpler is often better."**

Cette analyse démontre qu'optimiser au-delà de la configuration de base peut être contre-productif. Le setup SL3 + 1R Full Exit est optimal car il **s'aligne avec la nature du mouvement** (rapide, précis, limité dans le temps).

Essayer de "faire mieux" avec des runners détruit l'edge statistique en introduisant:
- Variance supplémentaire (retours au BE)
- Complexité d'exécution
- Opportunités d'erreurs

## Notes Techniques

- **Chronologie conservatrice**: Si SL et TP sur même bougie → SL touché en premier
- **Tokyo EQ inconsistent**: Si EQ plus proche que 1R → Fallback sur Scénario A
- **Lookahead**: Maximum 1000 barres (~3.5 jours) pour chaque simulation
- **Runner tracking**: Success rate calculé uniquement sur trades ayant atteint TP1

## Avertissements

⚠️ **Disclaimer**: Ce backtest est fourni à des fins éducatives et de recherche. Les performances passées ne garantissent pas les résultats futurs. Toujours tester en simulation avant le trading réel.

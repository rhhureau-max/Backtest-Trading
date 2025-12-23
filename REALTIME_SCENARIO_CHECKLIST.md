# ✅ CHECKLISTS TEMPS RÉEL - SCÉNARIOS LONDON-TOKYO KILLZONE

## 📋 GUIDE D'UTILISATION

Ces checklists sont conçues pour être **imprimées** et utilisées pendant la session de trading pour valider manuellement les scénarios détectés par l'IA.

**Horaire d'utilisation:** 23h45 NY (fin de session Tokyo)

**Instructions:**
1. Imprimez cette page
2. Cochez chaque critère en temps réel
3. Calculez le score de probabilité
4. Comparez avec la prédiction de l'IA
5. Prenez votre décision finale

---

## 🔵 CHECKLIST SCÉNARIO 1: COMPRESSION

**Critère Principal:** Range Tokyo < 40 points → Consolidation attendue pendant Londres

### 📊 DONNÉES À COLLECTER

**Date:** __________ **Heure:** __________

#### 1. RANGE ASIATIQUE (20h00-00h00 NY)

```
High Tokyo: _____________ points
Low Tokyo:  _____________ points
Range:      _____________ points

[ ] Range < 40 points (CRITÈRE ESSENTIEL)
```

**Points:** ☐ 0 pts (Range ≥ 40) ☐ 25 pts (Range < 40)

---

#### 2. BOLLINGER BANDS (M15, période 20)

```
Upper Band:  _____________
Middle Band: _____________
Lower Band:  _____________
Bandwidth:   _____________% (Upper-Lower)/Middle × 100
```

☐ Bands très plates (largeur < 0.2%) → **20 points**  
☐ Bands contractées (largeur 0.2-0.3%) → **15 points**  
☐ Bands normales (largeur 0.3-0.5%) → **5 points**  
☐ Bands expansées (largeur > 0.5%) → **0 points**

**Points:** _______

---

#### 3. ATR (Average True Range, période 14)

```
ATR actuel:    _____________ points
ATR session NY précédente: _____________ points
Variation:     _____________% (hausse/baisse)
```

☐ ATR en baisse > 15% → **20 points**  
☐ ATR en baisse 10-15% → **15 points**  
☐ ATR en baisse 5-10% → **10 points**  
☐ ATR stable ou en hausse → **0 points**

**Points:** _______

---

#### 4. STRUCTURE H4

```
Dernier Swing High H4: _____________ (cassé: Oui/Non)
Dernier Swing Low H4:  _____________ (cassé: Oui/Non)
Prix actuel:           _____________
Position:              [ ] Range-bound [ ] Près d'un extrême
```

☐ Aucune cassure de structure H4 → **15 points**  
☐ Prix au milieu du range H4 (40-60%) → **10 points**  
☐ Cassure récente ou prix à l'extrême → **0 points**

**Points:** _______

---

#### 5. RSI (Relative Strength Index, période 14, M15)

```
RSI actuel: _____________
```

☐ RSI entre 45-55 (zone morte neutre) → **10 points**  
☐ RSI entre 40-45 ou 55-60 (légèrement hors neutre) → **5 points**  
☐ RSI < 40 ou > 60 (momentum directionnel) → **0 points**

**Points:** _______

---

#### 6. VOLUME

```
Volume moyen 20 jours: _____________ K
Volume session Tokyo:  _____________ K
Écart:                 _____________% (hausse/baisse)
```

☐ Volume en baisse > 15% → **10 points**  
☐ Volume en baisse 5-15% → **5 points**  
☐ Volume stable ou en hausse → **0 points**

**Points:** _______

---

#### 7. CALENDRIER ÉCONOMIQUE

```
News à venir session Londres (02h00-05h00 NY):
[ ] Aucune news majeure
[ ] News mineures (yellow folder)
[ ] NEWS MAJEURES (RED FOLDER) ⚠️
```

☐ Aucune red folder news → **10 points**  
☐ News mineures uniquement → **5 points**  
☐ Red folder news prévue → **0 points** (ABORT TRADE)

**Points:** _______

---

### 📈 CALCUL DU SCORE

| Critère | Points Obtenus | Points Max |
|---------|----------------|------------|
| 1. Range < 40 pts | _______ | 25 |
| 2. Bollinger Bands | _______ | 20 |
| 3. ATR en baisse | _______ | 20 |
| 4. Structure H4 | _______ | 15 |
| 5. RSI neutre | _______ | 10 |
| 6. Volume faible | _______ | 10 |
| 7. Pas de news | _______ | 10 |
| **TOTAL** | **_______** | **110** |

### 🎯 INTERPRÉTATION

**Score Final:** _______ / 110 = _______% 

☐ **90-110 pts (82-100%)** → COMPRESSION TRÈS PROBABLE  
   → ✅ **TRADER** avec position NORMALE  
   → Stratégie: Range Bound (achat bas / vente haut)

☐ **75-89 pts (68-81%)** → COMPRESSION PROBABLE  
   → ⚠️ **TRADER** avec position RÉDUITE (50%)  
   → Stratégie: Range Bound prudent

☐ **60-74 pts (55-67%)** → COMPRESSION POSSIBLE  
   → ❌ **NE PAS TRADER** - Signal trop faible

☐ **< 60 pts (< 55%)** → COMPRESSION IMPROBABLE  
   → ❌ **NE PAS TRADER** - Utiliser Checklist Continuation

### 💼 PLAN DE TRADING (si score ≥ 75)

```
LONG (Achat au bas du range):
Entry:       _____________ (près du Low Tokyo)
Stop Loss:   _____________ (Low - 10 points)
Target:      _____________ (milieu du range ou High)
Risk/Reward: _____________

SHORT (Vente au haut du range):
Entry:       _____________ (près du High Tokyo)
Stop Loss:   _____________ (High + 10 points)
Target:      _____________ (milieu du range ou Low)
Risk/Reward: _____________
```

**Taille de position:** _______ contrats (Max 1-2% du capital)

---

## 🟢 CHECKLIST SCÉNARIO 2: CONTINUATION

**Critère Principal:** Cassure H4 confirmée → Momentum fort attendu pendant Londres

### 📊 DONNÉES À COLLECTER

**Date:** __________ **Heure:** __________

#### 1. CASSURE DE STRUCTURE H4 (CRITÈRE VITAL)

```
Type de structure: [ ] Bullish [ ] Bearish

BULLISH:
Ancien Swing High H4: _____________ points
Prix actuel:          _____________ points
Cassure de:           _____________ points au-dessus

BEARISH:
Ancien Swing Low H4:  _____________ points
Prix actuel:          _____________ points
Cassure de:           _____________ points en-dessous
```

☐ Cassure > 30 points au-delà du swing → **40 points** (ESSENTIEL)  
☐ Cassure 15-30 points → **20 points**  
☐ Cassure < 15 points ou aucune cassure → **0 points** (ABORT)

**Points:** _______

**⚠️ SI 0 POINTS ICI → NE PAS CONTINUER, UTILISER AUTRE CHECKLIST**

---

#### 2. POSITION VS MOYENNES MOBILES H1

```
Prix actuel: _____________ points
EMA 20 (H1): _____________ points
EMA 50 (H1): _____________ points

Bullish: Prix > EMA 20 ET Prix > EMA 50
Bearish: Prix < EMA 20 ET Prix < EMA 50
```

☐ Prix CLAIREMENT au-dessus/en-dessous des 2 EMA (> 20 pts) → **20 points**  
☐ Prix au-dessus/en-dessous mais proche (10-20 pts) → **10 points**  
☐ Prix entre les EMA ou très proche → **0 points**

**Points:** _______

---

#### 3. ANALYSE SMT (Smart Money Technique)

```
Mouvement NQ: _____________% (depuis 16h00 NY)
Mouvement ES: _____________% (depuis 16h00 NY)

NQ fait nouveau high/low: [ ] Oui [ ] Non
ES fait nouveau high/low: [ ] Oui [ ] Non
```

☐ Les DEUX font nouveau high/low ensemble (symétrie) → **15 points**  
☐ Un seul fait nouveau high/low (divergence) → **0 points** ⚠️

**Points:** _______

---

#### 4. PD ARRAYS (Order Blocks / FVG)

```
Order Block H4 identifié:
Zone: _____________ à _____________ points
Réaction: [ ] Oui (prix a rebondi dessus) [ ] Non

Fair Value Gap H4:
Zone: _____________ à _____________ points
Status: [ ] Comblé [ ] Partiellement comblé [ ] Non comblé
```

☐ Réaction claire sur Order Block avant cassure → **15 points**  
☐ Order Block présent mais réaction faible → **7 points**  
☐ Pas d'Order Block clair → **0 points**

**Points:** _______

---

#### 5. MOMENTUM ET VOLUME

```
Range Tokyo: _____________ points
Volume Tokyo vs moyenne: _____________% (hausse/baisse)
ATR(14): _____________ (vs session NY: _______%)
```

☐ Volume en hausse > 20% ET ATR en hausse → **10 points**  
☐ Volume ou ATR en hausse (pas les deux) → **5 points**  
☐ Volume et ATR stables ou en baisse → **0 points**

**Points:** _______

---

#### 6. DRAW ON LIQUIDITY (Cible)

```
Direction de la cassure: [ ] Bullish [ ] Bearish

Prochain niveau de liquidité:
Buy Side (au-dessus): _____________ points (distance: _____pts)
Sell Side (en-dessous): _____________ points (distance: _____pts)

Cible identifiée: [ ] Oui [ ] Non
Distance: _____________ points
```

☐ Cible claire à 30-80 points de distance → **10 points**  
☐ Cible lointaine (> 80 pts) ou trop proche (< 30 pts) → **5 points**  
☐ Pas de cible claire → **0 points**

**Points:** _______

---

### 📈 CALCUL DU SCORE

| Critère | Points Obtenus | Points Max |
|---------|----------------|------------|
| 1. Cassure H4 | _______ | 40 |
| 2. Position vs EMA | _______ | 20 |
| 3. SMT symétrique | _______ | 15 |
| 4. PD Arrays | _______ | 15 |
| 5. Momentum/Volume | _______ | 10 |
| 6. Draw on Liquidity | _______ | 10 |
| **TOTAL** | **_______** | **110** |

### 🎯 INTERPRÉTATION

**Score Final:** _______ / 110 = _______% 

☐ **90-110 pts (82-100%)** → CONTINUATION TRÈS PROBABLE  
   → ✅ **TRADER** avec position NORMALE  
   → Stratégie: Trend Following (acheter pullbacks / vendre rallies)

☐ **75-89 pts (68-81%)** → CONTINUATION PROBABLE  
   → ⚠️ **TRADER** avec position RÉDUITE (50%)  
   → Stratégie: Suivre la tendance avec prudence

☐ **60-74 pts (55-67%)** → CONTINUATION POSSIBLE  
   → ❌ **NE PAS TRADER** - Signal trop faible

☐ **< 60 pts (< 55%)** → CONTINUATION IMPROBABLE  
   → ❌ **NE PAS TRADER**

### 💼 PLAN DE TRADING (si score ≥ 75)

```
Direction: [ ] LONG [ ] SHORT

OPTION 1 - Entrée au Pullback (Préférée):
Entry:       _____________ (zone Order Block / FVG / EMA)
Stop Loss:   _____________ (sous/sur structure cassée)
Target 1:    _____________ (premier niveau liquidité)
Target 2:    _____________ (draw on liquidity principal)
Risk/Reward: _____________

OPTION 2 - Entrée Agressive (si pas de pullback à 02h30):
Entry:       _____________ (au marché)
Stop Loss:   _____________ (serré, 15-20 points)
Target:      _____________ (draw on liquidity)
Risk/Reward: _____________
```

**Taille de position:** _______ contrats (Max 1-2% du capital)

---

## ⚖️ CHECKLIST SCÉNARIO 3: ARBITRE (SIGNAUX MIXTES)

**Utilisation:** Quand les signaux sont contradictoires ou borderline

### 📊 DONNÉES À COLLECTER

**Date:** __________ **Heure:** __________

#### ÉVALUATION RAPIDE

```
Range Tokyo: _____________ points

[ ] < 35 points → Clairement COMPRESSION → Utiliser Checklist 1
[ ] > 45 points + cassure H4 → Clairement CONTINUATION → Utiliser Checklist 2
[ ] Entre 35-45 points OU signaux contradictoires → CONTINUER ICI
```

---

#### 1. SCORE COMPRESSION

Remplir rapidement la Checklist 1 (Compression):

**Score Compression:** _______ / 110 = _______% 

---

#### 2. SCORE CONTINUATION

Remplir rapidement la Checklist 2 (Continuation):

**Score Continuation:** _______ / 110 = _______% 

---

#### 3. INDICATEURS DÉTERMINANTS

**RSI M15:**
```
RSI actuel: _____________

[ ] 45-55 (neutre) → Favorise COMPRESSION
[ ] < 40 ou > 60 (directionnel) → Favorise CONTINUATION
```

**Fair Value Gaps:**
```
Nombre de FVG non comblés: _____________
Taille moyenne des FVG: _____________ points

[ ] Plusieurs FVG larges → Favorise CONTINUATION
[ ] FVG mineurs ou comblés → Favorise COMPRESSION
```

**Volume:**
```
Volume actuel vs moyenne: _____________% 

[ ] Volume < -10% → Favorise COMPRESSION
[ ] Volume > +10% → Favorise CONTINUATION
```

---

### 🎯 DÉCISION FINALE

```
Score Compression: _______% 
Score Continuation: _______% 
Écart: _____________%

Indicateurs RSI/FVG/Volume favorisent: [ ] COMPRESSION [ ] CONTINUATION
```

#### RÈGLE DE DÉCISION:

☐ **Écart > 20% entre les scores** → Prendre le scénario dominant  
☐ **Écart 10-20%** → Prendre le scénario dominant MAIS position réduite  
☐ **Écart < 10%** → **NE PAS TRADER** (trop incertain)

**Scénario sélectionné:** ___________________

**Probabilité ajustée:** _______%

### 💼 ACTION

☐ ✅ **TRADER** (probabilité ≥ 70% et écart > 10%)  
   → Utiliser le plan de trading du scénario sélectionné  
   → Position RÉDUITE (50% de la taille normale)  
   → Stops SERRÉS (ajuster à -20%)

☐ ❌ **NE PAS TRADER** (probabilité < 70% ou écart < 10%)  
   → Rester à l'écart  
   → Observer uniquement  
   → Journaliser pour apprentissage

---

## 📊 TABLEAU DE BORD STATISTIQUES

### Fréquences Historiques par Contexte

#### Par Jour de Semaine

| Jour | Compression | Continuation | Expansion |
|------|-------------|--------------|-----------|
| Lundi | 47.19% | 40.64% | 3.19% |
| Mardi | 49.63% | 38.92% | 2.95% |
| Mercredi | 40.24% | 48.17% | 4.39% |
| Jeudi | 43.89% | 44.26% | 3.99% |

**Aujourd'hui (________):** Compression _____% | Continuation _____% 

---

#### Par Mois

| Mois | Compression | Continuation | Expansion |
|------|-------------|--------------|-----------|
| Janvier | 51.39% | 37.50% | 4.86% |
| Février | 48.84% | 38.37% | 3.10% |
| Mars | 34.78% | 52.90% | 5.07% |
| Avril | 45.52% | 41.04% | 4.48% |
| Mai | 42.25% | 45.07% | 3.52% |
| Juin | 51.47% | 35.29% | 2.94% |
| Juillet | 45.45% | 41.26% | 3.50% |
| Août | 41.13% | 48.23% | 2.84% |
| Septembre | 39.42% | 49.64% | 3.65% |
| Octobre | 37.06% | 51.05% | 4.20% |
| Novembre | 46.83% | 39.68% | 2.38% |
| Décembre | 62.28% | 27.19% | 1.75% |

**Ce mois-ci (________):** Compression _____% | Continuation _____% 

---

### Ajustement Contextuel

```
Scénario détecté: ___________________
Probabilité brute: _______%

Contexte jour: Favorise [ ] Compression [ ] Continuation [ ] Neutre
Contexte mois: Favorise [ ] Compression [ ] Continuation [ ] Neutre

Ajustement: ☐ +5% ☐ 0% ☐ -5%

PROBABILITÉ FINALE: _______%
```

---

## ✅ VALIDATION FINALE PRÉ-TRADE

**Avant d'exécuter un trade, TOUS ces points doivent être validés:**

### Checklist Obligatoire

```
[ ] Score de probabilité ≥ 70%
[ ] Pas de red folder news dans les 4 prochaines heures
[ ] Capital disponible suffisant
[ ] Stop loss défini et accepté mentalement
[ ] Take profit défini
[ ] Risk ≤ 2% du capital total
[ ] Position sizing calculée (contrats: _______)
[ ] Setup cohérent avec statistiques jour/mois
[ ] Pas de FOMO ou émotion négative
[ ] Mental clair et repos suffisant
[ ] Journal de trading prêt à être rempli
[ ] Pas d'autre trade ouvert en conflit
```

**Nombre de cases cochées:** _______ / 12

☐ **12/12** → ✅ FEU VERT - Exécuter le trade  
☐ **10-11/12** → ⚠️ PRUDENCE - Réévaluer les points manquants  
☐ **< 10/12** → ❌ STOP - Ne pas trader

---

## 📝 JOURNAL DE PRÉDICTION

**À remplir après la décision:**

```
Date: __________
Heure de l'analyse: __________
Scénario prédit: ___________________
Probabilité: _______%
Score checklist: _______ / 110
Prédiction IA (si utilisée): _______% ___________________

Décision finale: [ ] TRADE [ ] NO TRADE

Si TRADE:
Type: [ ] LONG [ ] SHORT
Entry: _____________
Stop: _____________
Target: _____________
Taille: _____________ contrats
```

**À remplir après la session de Londres (05h30 NY):**

```
Résultat réel: [ ] Scénario correct [ ] Scénario incorrect
Prix High Londres: _____________
Prix Low Londres: _____________
Range Londres: _____________ points

Trade exécuté: [ ] Oui [ ] Non
Si oui, résultat: [ ] Gain: _____pts [ ] Perte: _____pts [ ] Breakeven

Commentaires:
_____________________________________________
_____________________________________________
_____________________________________________

Leçons apprises:
_____________________________________________
_____________________________________________
_____________________________________________
```

---

## 🎯 STATISTIQUES PERSONNELLES

**Tenir à jour sur une feuille séparée:**

### Taux de Réussite des Prédictions

```
Mois: __________

Scénario COMPRESSION:
Prédictions: _____ | Correctes: _____ | Taux: _____% 

Scénario CONTINUATION:
Prédictions: _____ | Correctes: _____ | Taux: _____%

Scénario ARBITRE:
Prédictions: _____ | Correctes: _____ | Taux: _____%

TOTAL:
Prédictions: _____ | Correctes: _____ | Taux: _____% 
```

### Performance Trading

```
Trades exécutés: _____
Trades gagnants: _____
Trades perdants: _____
Win Rate: _____%

Profit/Loss total: _________ points
Profit moyen: _________ points/trade
Perte moyenne: _________ points/trade
```

### Insights

```
Meilleur jour de la semaine: __________
Meilleur mois: __________
Scénario le plus profitable: __________
Erreurs récurrentes: 
_____________________________________________
_____________________________________________
```

---

## 📞 NOTES ET AMÉLIORATIONS

**Espace libre pour vos annotations:**

```
_____________________________________________
_____________________________________________
_____________________________________________
_____________________________________________
_____________________________________________
_____________________________________________
_____________________________________________
_____________________________________________
```

---

## 🔗 RESSOURCES COMPLÉMENTAIRES

- **Guide complet:** `AI_ASSISTED_SCENARIO_DETECTION_GUIDE.md`
- **Script automatique:** `scenario_detector_helper.py`
- **Glossaire ICT:** `ICT_CONCEPTS_GLOSSARY.md`
- **Statistiques:** `SCENARIO_OCCURRENCE_ANALYSIS_NQ_2018_2025.md`

---

**Version:** 1.0  
**Date:** 23 Décembre 2025  
**Format:** Imprimable A4 / Lettre

**Bon trading! 🚀📈**

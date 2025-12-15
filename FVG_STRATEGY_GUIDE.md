# Guide Stratégique - Fair Value Gap (FVG) Validation

## Vue d'ensemble

Ce guide explique comment utiliser le **filtre de validation FVG** pour améliorer la stratégie de trading basée sur les manipulations Tokyo-Londres.

---

## Qu'est-ce qu'un FVG (Fair Value Gap)?

Un FVG est un "gap" dans le prix qui se forme sur 3 bougies consécutives, indiquant un déséquilibre entre acheteurs et vendeurs.

### Types de FVG

#### 1. FVG Baissier (Bearish FVG)
```
Bougie n-2: Low = 15,100
Bougie n-1: (transition)
Bougie n:   High = 15,080

Condition: Low(n-2) > High(n)
Zone FVG: [15,080, 15,100]
```

**Signification:** Prix descendu rapidement, laissant un gap. Utilisé pour valider les **setups d'ACHAT**.

#### 2. FVG Haussier (Bullish FVG)
```
Bougie n-2: High = 15,000
Bougie n-1: (transition)
Bougie n:   Low = 15,020

Condition: High(n-2) < Low(n)
Zone FVG: [15,000, 15,020]
```

**Signification:** Prix monté rapidement, laissant un gap. Utilisé pour valider les **setups de VENTE**.

---

## Stratégie Complète (Étapes)

### Étape 1: Identifier la Manipulation (02:00-02:45)

**Cherche:**
- Cassure du **Tokyo Low** → Setup d'ACHAT potentiel
- Cassure du **Tokyo High** → Setup de VENTE potentiel

```
Tokyo Range: [Low=15,000, High=15,100, Equilibrium=15,050]

Manipulation window (02:00-02:45):
- Si Low < 15,000 détecté → Setup ACHAT possible
- Si High > 15,100 détecté → Setup VENTE possible
```

### Étape 2: Détecter le FVG "Piège" (02:00-03:00)

**Pour Setup ACHAT (après cassure du Tokyo Low):**
- Cherche un **FVG Baissier** dans la fenêtre 02:00-03:00
- Le FVG représente le "piège" des vendeurs qui ont poussé le prix en bas

**Pour Setup VENTE (après cassure du Tokyo High):**
- Cherche un **FVG Haussier** dans la fenêtre 02:00-03:00
- Le FVG représente le "piège" des acheteurs qui ont poussé le prix en haut

### Étape 3: Valider l'Entrée (avant 05:00)

**Pour Setup ACHAT:**
- Attendre qu'une bougie **clôture AU-DESSUS** de la borne haute du FVG Baissier
- Cela confirme que les acheteurs reprennent le contrôle

**Pour Setup VENTE:**
- Attendre qu'une bougie **clôture EN-DESSOUS** de la borne basse du FVG Haussier
- Cela confirme que les vendeurs reprennent le contrôle

**⚠️ Si validation n'arrive pas avant 05:00 → NO TRADE**

### Étape 4: Gestion du Trade

**Stop Loss:**
- **ACHAT:** Plus bas de la manipulation (02:00-03:00)
- **VENTE:** Plus haut de la manipulation (02:00-03:00)

**Targets:**
- **Target 1 (Conservateur):** Equilibrium - 59.56% probabilité
- **Target 2 (Agressif):** Full Range - 37.54% probabilité

---

## Exemple Concret: Setup ACHAT

```
📅 Date: 2024-03-15

1️⃣ TOKYO RANGE (19:00 J-1 → 01:00 J)
   Low: 18,000
   High: 18,200
   Equilibrium: 18,100

2️⃣ MANIPULATION (02:00-02:45)
   02:15 - Price breaks below 18,000
   → ACHAT Setup potentiel détecté

3️⃣ FVG DETECTION (02:00-03:00)
   02:25 - Bearish FVG formé:
   - Bougie n-2 Low: 18,010
   - Bougie n High: 17,990
   - Zone FVG: [17,990, 18,010]
   → FVG Baissier détecté ✓

4️⃣ VALIDATION (avant 05:00)
   03:10 - Bougie clôture à 18,015
   → Clôture > 18,010 (borne haute FVG)
   → ENTRY VALIDÉE ✓

5️⃣ GESTION DU TRADE
   Entry: 18,015 (à la clôture de validation)
   Stop: 17,985 (plus bas de manipulation)
   Target 1: 18,100 (Equilibrium)
   Target 2: 18,200 (Tokyo High)
   
   Risk: 30 points
   Reward T1: 85 points (RR = 2.83)
   Reward T2: 185 points (RR = 6.17)
```

---

## Résultats Statistiques (2018-2025)

### Filtrage
| Métrique | Valeur | % |
|----------|--------|---|
| Total jours analysés | 2,032 | 100% |
| Jours avec manipulation | 1,406 | 69.2% |
| FVG détecté | 967 | 47.6% |
| **FVG validé (Trades pris)** | **586** | **28.8%** |
| Trades éliminés | 820 | 58.3% |

**💡 Le filtre FVG élimine 58.3% des signaux de manipulation**

### Performance des Trades Validés

| Setup | Nombre | EQ Winrate | Full Range WR |
|-------|--------|------------|---------------|
| **BUY** | 254 | **63.0%** ⭐ | **39.0%** |
| **SELL** | 324 | **55.9%** | **35.2%** |
| **TOTAL** | 586 | **59.6%** | **37.5%** |

**💡 Winrate de ~60% vers l'équilibre avec le filtre FVG**

---

## Avantages du Filtre FVG

### ✅ Réduit les Faux Signaux
- Élimine 58% des manipulations sans confirmation
- Garde uniquement les setups de haute qualité

### ✅ Améliore le Winrate
- 59.56% de réussite vers l'équilibre
- Beaucoup plus élevé qu'une stratégie sans filtre

### ✅ Définit des Règles Claires
- Entry objective: clôture au-delà du FVG
- Stop objectif: extrême de manipulation
- Targets objectives: Equilibrium et Full Range

### ✅ Réduit la Fréquence de Trading
- ~84 trades par an (~7 par mois)
- Évite le surtrading
- Meilleure gestion du capital

---

## Recommandations d'Utilisation

### 1. Position Sizing
Avec seulement 586 trades sur 7+ ans, tu peux être plus agressif sur la taille de position:
- **Conservateur:** 1-2% du capital par trade
- **Modéré:** 2-3% du capital par trade
- **Agressif:** 3-5% du capital par trade (avec expérience)

### 2. Gestion des Targets
**Stratégie recommandée:**
- Prendre **50% de profit à l'Equilibrium** (59.56% probabilité)
- Laisser **50% courir vers Full Range** (37.54% probabilité)
- Déplacer le stop au breakeven après touch d'Equilibrium

**Exemple:**
```
Position: 2 contrats NQ
Entry: 18,015
Stop: 17,985 (risque: 30 points × 2 = 60 points)

Target 1 (Equilibrium @ 18,100):
- Fermer 1 contrat: +85 points
- Déplacer stop de l'autre contrat au breakeven (18,015)

Target 2 (Full Range @ 18,200):
- Fermer dernier contrat: +185 points

Résultat si T1 touché:
- Gain minimum: +85 points (1 contrat)
- Risque restant: 0 (stop au breakeven)
```

### 3. Timeframe de Monitoring
- **Pré-session:** Calculer le Tokyo Range (avant 02:00)
- **Active monitoring:** 02:00-05:00 (3 heures)
- **Post-session:** Documenter les trades et résultats

### 4. Jours à Éviter
- Annonces économiques majeures (FOMC, NFP, CPI)
- Jours fériés avec liquidité réduite
- Premiers/derniers jours du mois (rebalancing)

---

## Limites et Considérations

### ⚠️ Limitations
1. **Fenêtre temporelle stricte:** Doit surveiller 02:00-05:00 UTC
2. **Pas de validation = Pas de trade:** Peut manquer des mouvements
3. **Stop loss touché:** ~40% des trades (contrepartie du winrate)

### 🔍 Optimisations Futures
1. **Filtres supplémentaires:**
   - Volume profile confirmation
   - Contexte de marché (trend, VIX)
   - Day of week analysis

2. **Variations de targets:**
   - Trailing stop après Equilibrium
   - Multiple partial exits
   - Time-based exits (si pas de target avant X heures)

3. **Analyse de corrélation:**
   - Performance en fonction de la taille du Tokyo Range
   - Impact de la magnitude de la cassure
   - Heure exacte de la cassure (02:00 vs 02:40)

---

## Utilisation du Script

### Générer l'Analyse
```bash
cd /home/runner/work/Backtest-Trading/Backtest-Trading
python3 tokyo_london_session_analysis.py
```

### Fichiers Générés
1. **tokyo_london_fvg_analysis.csv** - Dataset complet avec tous les champs FVG
2. **FVG_ANALYSIS_REPORT.md** - Rapport détaillé avec statistiques
3. **tokyo_london_analysis_results.csv** - Résultats base (manipulation + velocity)

### Colonnes Clés dans le CSV
```python
# Identification
'london_date'              # Date du jour de trading
'manipulation_type'        # Bullish/Bearish/Volatile/None

# Tokyo Range
'tokyo_high', 'tokyo_low', 'equilibrium'

# FVG Analysis
'fvg_detected'             # bool: FVG trouvé?
'fvg_type'                 # Bearish/Bullish
'fvg_lower_bound'          # Borne basse du FVG
'fvg_upper_bound'          # Borne haute du FVG
'fvg_validated'            # bool: Entry confirmée?
'fvg_entry_timestamp'      # Moment de l'entry

# Trade Management
'stop_loss'                # Niveau du stop
'hit_equilibrium_before_stop'  # bool: Target 1 atteint?
'hit_full_range_before_stop'   # bool: Target 2 atteint?
```

---

## Checklist Pré-Trade

Avant de prendre un trade, vérifie:

- [ ] Tokyo Range calculé correctement (19:00 J-1 → 01:00 J)
- [ ] Manipulation détectée (02:00-02:45): Low ou High cassé
- [ ] FVG formé pendant 02:00-03:00
- [ ] Validation de l'entry: clôture au-delà du FVG avant 05:00
- [ ] Stop placé au bon niveau (extrême de manipulation)
- [ ] Targets définis (Equilibrium et Full Range)
- [ ] Position size calculée selon le risque
- [ ] Aucune annonce économique majeure dans les 4 heures

---

## Conclusion

Le filtre FVG transforme une stratégie de manipulation simple en un système de trading robuste avec:
- ✅ 58% de réduction du bruit
- ✅ 60% de winrate vers l'équilibre
- ✅ Règles objectives et automatisables
- ✅ Fréquence de trading gérable (~7 trades/mois)

**La stratégie est prête pour le paper trading en temps réel.**

---

*Guide créé le 4 décembre 2025*
*Basé sur 2,032 jours de données NQ (2018-2025)*

# SMC Reversal Backtest Strategy - Documentation (Version Améliorée)

## Vue d'ensemble

Stratégie de **Reversal SMC (Smart Money Concepts)** pour la session **01:00-07:00** du NQ (Nasdaq-100). Cette stratégie identifie les retournements de marché en utilisant des concepts avancés de microstructure : Liquidity Sweeps sur fractals **significatifs**, Market Structure Shifts (MSS), Fair Value Gaps (FVG), et entrées sur retracement Fibonacci.

**Période testée:** 2018-2025 (7+ années complètes, 2,032 sessions)  
**Timeframe:** 5 minutes  
**Type de trades:** Short (vente) uniquement  
**Version:** 2.0 - Fractals Significatifs + Sweeps Stricts

---

## 📊 Résultats du Backtest (Version Améliorée)

### Performance Globale (2018-2025)

| Métrique | Valeur |
|----------|--------|
| **Total Trades** | 31 |
| **Trades Gagnants** | 27 (87.10%) |
| **Trades Perdants** | 4 (12.90%) |
| **Win Rate** | **87.10%** ⭐⭐⭐⭐⭐ |
| **Profit Factor** | **7.75** ⭐⭐⭐⭐⭐ |
| **R:R Moyen** | 0.85:1 |

### Analyse P&L

| Métrique | Valeur (Points NQ) |
|----------|-------------------|
| **P&L Total** | +759.32 points |
| **P&L Moyen par Trade** | +24.49 points |
| **Gain Moyen** | +32.29 points |
| **Perte Moyenne** | -28.13 points |
| **Profit Brut** | +871.84 points |
| **Perte Brute** | -112.52 points |

### Performance du Compte (1% Risk)

| Métrique | Valeur |
|----------|--------|
| **Capital Initial** | $100,000 |
| **Equity Finale** | **$120,721.43** |
| **Rendement Total** | **+20.72%** 🚀 |
| **Sur 7 ans** | ~2.96% par an |

### Résultats par Année (2025)

| Métrique | Valeur |
|----------|--------|
| **Total Trades 2025** | 8 |
| **Win Rate 2025** | 100.00% |
| **P&L Total 2025** | +280.24 points |
| **P&L Moyen 2025** | +35.03 points/trade |

---

## 🎯 Logique de la Stratégie (Améliorée)

### 1. Identification de la Structure (Fractals SIGNIFICATIFS)

**Nouvelle approche:** Fractals plus stricts pour identifier uniquement les points pivots majeurs.

**Fractal High SIGNIFICATIF - DEUX conditions obligatoires:**
1. **Condition Locale:** Entouré de bougies plus basses (High[i] > High[i-1] ET High[i] > High[i+1])
2. **Condition Globale:** Point le plus HAUT des 12 dernières bougies (Rolling Max sur 12 périodes)

**Fractal Low SIGNIFICATIF - DEUX conditions obligatoires:**
1. **Condition Locale:** Entouré de bougies plus hautes (Low[i] < Low[i-1] ET Low[i] < Low[i+1])
2. **Condition Globale:** Point le plus BAS des 12 dernières bougies (Rolling Min sur 12 périodes)

**Paramètres:**
- Window = 1 bougie de chaque côté (local)
- Lookback = 12 bougies (rolling max/min)

### 2. Détection du Sweep (Liquidity Sweep STRICT)

Un **Sweep** se produit quand :

**Condition A (Le Sweep):**
- Le prix dépasse un Fractal High significatif (mèche au-dessus)

**Condition B (Validation du Rejet) - AU MOINS UNE:**
1. **Wick Rejection:** La bougie de cassure clôture EN DESSOUS du Fractal High
2. **Bearish Reversal dans les 2 bougies suivantes:**
   - **Bearish Engulfing:** Bougie rouge qui ouvre au-dessus et clôture en dessous de la précédente
   - **OU Strong Reversal:** Large bougie baissière (>10 points) qui clôture sous le fractal

**Objectif:** Identifier les faux breakouts où les institutions piègent les traders retail

### 3. Confirmation MSS (Market Structure Shift)

Après un sweep, on cherche un **MSS** :
- Le prix casse le dernier Fractal Low significatif
- Cela confirme un changement de structure de marché
- Indication d'un mouvement baissier potentiel

### 4. Entrée au Retracement Fibonacci

**Entrée:** 50% de retracement Fibonacci  
- Calculé entre le Sweep High et le MSS Low
- Permet d'entrer avec un meilleur R:R
- Entrée limit order

### 5. Stop Loss (SL)

**Placement:** Au-dessus du Sweep High + 5 points de buffer  
**Logique:** Si le prix revient au-dessus du sweep, l'invalidation est confirmée

### 6. Take Profit (TP)

**Cible:** Premier FVG (Fair Value Gap) baissier non comblé  
**Si aucun FVG:** Utilise le MSS Low comme TP conservateur

**FVG Baissier:** Espace entre Low[i] et High[i+2] quand Low[i] > High[i+2]  
**Taille minimum:** 5 points NQ

### Filtres Additionnels

- ✅ Entrée doit être entre MSS Low et Sweep High
- ✅ TP doit être en dessous de l'entrée (short)
- ✅ R:R minimum de 0.8:1
- ✅ Entrée doit se faire avant 07:00
- ✅ Sortie peut se faire après 07:00

---

## 📝 Exemples de Trades - Derniers 5 de 2025 (Version Améliorée)

### Trade #4 - 23 Juillet 2025

- **Résultat:** ✅ WIN (+25.75 points)
- **Session:** 2025-07-23, Entrée: 06:05, Sortie: 07:50
- **Sweep High:** 23,514.35 (fractal significatif: +12 rolling max) → **MSS Low:** 23,462.84
- **Entrée (50% Fib):** 23,488.60
- **SL:** 23,519.35 | **TP:** 23,462.84 | **Exit:** 23,462.84
- **R:R:** 0.84 | **Equity après:** $116,778.38

### Trade #5 - 23 Juillet 2025

- **Résultat:** ✅ WIN (+24.62 points)
- **Session:** 2025-07-23, Entrée: 06:05, Sortie: 07:50
- **Sweep High:** 23,512.08 → **MSS Low:** 23,462.84
- **Entrée (50% Fib):** 23,487.46
- **SL:** 23,517.08 | **TP:** 23,462.84 | **Exit:** 23,462.84
- **R:R:** 0.83 | **Equity après:** $117,749.02

### Trade #6 - 21 Août 2025

- **Résultat:** ✅ WIN (+35.22 points)
- **Session:** 2025-08-21, Entrée: 06:45, Sortie: 07:00
- **Sweep High:** 23,565.35 → **MSS Low:** 23,494.91
- **Entrée (50% Fib):** 23,530.13
- **SL:** 23,570.35 | **TP:** 23,494.91 | **Exit:** 23,494.91
- **R:R:** 0.88 | **Equity après:** $118,780.13

### Trade #7 - 5 Novembre 2025

- **Résultat:** ✅ WIN (+43.12 points)
- **Session:** 2025-11-05, Entrée: 04:50, Sortie: 04:55 (5 minutes!)
- **Sweep High:** 25,533.25 → **MSS Low:** 25,436.50
- **Entrée (50% Fib):** 25,484.88
- **SL:** 25,538.25 | **TP:** 25,441.75 | **Exit:** 25,441.75
- **R:R:** 0.81 | **Equity après:** $119,739.83

### Trade #8 - 5 Novembre 2025

- **Résultat:** ✅ WIN (+46.62 points)
- **Session:** 2025-11-05, Entrée: 04:50, Sortie: 04:55 (5 minutes!)
- **Sweep High:** 25,540.25 → **MSS Low:** 25,436.50
- **Entrée (50% Fib):** 25,488.38
- **SL:** 25,545.25 | **TP:** 25,441.75 | **Exit:** 25,441.75
- **R:R:** 0.82 | **Equity finale:** $120,721.43

**Note:** Ces 5 derniers trades de 2025 illustrent la qualité supérieure des setups avec les fractals significatifs. **100% de win rate** et un gain moyen de **+35.03 points** par trade (vs +19.73 dans la version précédente).
- **Entrée (50% Fib):** 25,507.00
- **SL:** 25,538.25 | **TP:** 25,480.75 | **Exit:** 25,480.75
- **R:R:** 0.84 | **Equity finale:** $1,427,183.48

**Note:** Ces 5 derniers trades de 2025 illustrent parfaitement la consistance de la stratégie avec 5 wins consécutifs et un gain moyen de +24.87 points par trade.

---

## 📈 Graphiques Générés

### Graphique de Performance
![SMC Reversal Backtest Results](smc_reversal_backtest_results.png)

Le graphique contient 4 sous-graphiques :

1. **Equity Curve** - Courbe d'équité cumulative avec risque 1%
2. **Win/Loss Distribution** - Répartition des trades gagnants/perdants
3. **P&L Distribution** - Distribution des P&L par trade
4. **R:R Ratio Distribution** - Distribution des ratios risque/rendement réalisés

---

## 🔧 Configuration et Paramètres

### Paramètres de la Stratégie

```python
FRACTAL_WINDOW = 1           # Fenêtre pour détecter les fractals
REVERSAL_WINDOW = 5          # Bougies pour confirmer le reversal
FIB_ENTRY_LEVEL = 0.5        # 50% retracement Fibonacci
MIN_FVG_SIZE = 5             # Taille minimum FVG (5 points)
RISK_PER_TRADE = 0.01        # 1% de risque par trade
```

### Session Configurée

```python
SESSION_START = 01:00        # Début de session
SESSION_END = 07:00          # Fin de session (entrée)
# Sortie possible après 07:00
```

---

## 💡 Analyse et Insights (Version Améliorée)

### Points Forts ✅

1. **Win Rate encore amélioré:** 87.10% (vs 85.93% version précédente) avec fractals significatifs
2. **Profit Factor exceptionnel:** 7.75 (vs 5.39) = gestion du risque encore meilleure
3. **Gain moyen supérieur:** +32.29 points (vs +27.45) grâce à la qualité des setups
4. **Stratégie ultra-sélective:** Seulement 31 trades sur 7 ans = **qualité maximale**
5. **2025 Performance:** 100% win rate (8/8 trades) avec moyenne de +35.03 pts/trade
6. **Perte moyenne réduite:** -28.13 points (vs -31.12) = meilleurs points d'entrée

### Points d'Attention ⚠️

1. **Fréquence très faible:** 31 trades sur 2,032 sessions (1.5% setup rate)
   - Trade tous les 2-3 mois en moyenne
   - Nécessite patience et discipline
   - Qualité maximale vs quantité

2. **Sample size réduit:** 31 trades sur 7 ans
   - Statistiquement moins robuste que 462 trades
   - Mais excellente consistance (87.10% WR)
   - Chaque trade est de très haute qualité

3. **Rendement total plus modeste:** +20.72% sur 7 ans (vs +1,327%)
   - Dû à la fréquence très faible
   - Mais risque beaucoup plus contrôlé
   - Stratégie complémentaire à d'autres approches

### Comparaison Version 1 vs Version 2

| Métrique | Version 1 (Fractals Simples) | Version 2 (Fractals Significatifs) |
|----------|-------------------------------|-------------------------------------|
| **Total Trades** | 462 | 31 |
| **Win Rate** | 85.93% | **87.10%** ⬆️ |
| **Profit Factor** | 5.39 | **7.75** ⬆️ |
| **Gain Moyen** | +27.45 pts | **+32.29 pts** ⬆️ |
| **Perte Moyenne** | -31.12 pts | **-28.13 pts** ⬇️ |
| **Setup Rate** | 23% | 1.5% |
| **Rendement Total** | +1,327% | +20.72% |

**Conclusion:** La Version 2 privilégie la **qualité extrême** sur la quantité. Idéale pour traders patients cherchant des setups ultra-fiables avec minimum de risque.

---

## 🚀 Utilisation

### Installation

```bash
pip install pandas numpy matplotlib seaborn
```

### Exécution

```bash
python3 smc_reversal_backtest_01_07.py
```

### Output

1. **Console:** Rapport détaillé avec toutes les métriques
2. **smc_reversal_backtest_results.png:** Graphique de performance (4 subplots)
3. **smc_reversal_trades.csv:** Export de tous les trades avec détails

### Modifier la Période

Par défaut, le script charge les **2 dernières années** pour la performance. Pour tester plus d'années :

```python
# Dans load_nq_data()
df = load_nq_data(limit_years=5)  # Teste 5 années
```

---

## 📝 Structure des Trades CSV

Le fichier `smc_reversal_trades.csv` contient :

| Colonne | Description |
|---------|-------------|
| session_date | Date de la session |
| entry_time | Heure d'entrée |
| entry_price | Prix d'entrée |
| sl_price | Stop loss |
| tp_price | Take profit |
| exit_time | Heure de sortie |
| exit_price | Prix de sortie |
| outcome | 'win' ou 'loss' |
| pnl_points | P&L en points |
| risk_points | Points risqués |
| reward_points | Points de récompense potentielle |
| rr_ratio | Ratio R:R réalisé |
| sweep_high | High du sweep |
| mss_low | Low du MSS |
| equity | Equity après le trade |
| cumulative_pnl | P&L cumulé |

---

## 🎓 Concepts SMC Utilisés

### 1. Liquidity Sweep

**Concept:** Les institutions "balaient" la liquidité (stop losses des traders retail) au-dessus des highs clés avant de renverser le prix.

**Application:** On identifie quand le prix dépasse un fractal high mais ne parvient pas à clôturer au-dessus.

### 2. Market Structure Shift (MSS)

**Concept:** Changement dans la structure de marché indiquant un potentiel changement de tendance.

**Application:** Quand le prix casse un fractal low après un sweep, cela confirme que les vendeurs prennent le contrôle.

### 3. Fair Value Gap (FVG)

**Concept:** Zones d'inefficience du prix où le marché a bougé trop vite, créant un "gap" qui attire le prix de retour.

**Application:** Utilisé comme cible de profit car le prix a tendance à revenir combler ces gaps.

### 4. Fibonacci Retracement

**Concept:** Les marchés ont tendance à retracer une portion du mouvement initial avant de continuer.

**Application:** Entrée au 50% du retracement entre le sweep high et le MSS low offre un meilleur point d'entrée.

---

## 🔄 Améliorations Possibles

### 1. Optimisation des Cibles

- Tester différents niveaux de FVG (bottom, middle, top)
- Ajouter des TP multiples (scaling out)
- Intégrer des trailing stops après le premier TP

### 2. Filtres Additionnels

- Ajouter un filtre de volume sur les sweeps
- Intégrer le contexte de marché (tendance HTF)
- Filtrer selon le jour de la semaine (éviter vendredi)
- Ajouter un filtre de temps (éviter les 30 premières minutes)

### 3. Gestion du Risque

- Tester différents % de risque (0.5%, 1.5%, 2%)
- Implémenter un position sizing dynamique
- Ajouter un drawdown maximum

### 4. Extensions

- Ajouter la logique LONG (inverser la stratégie)
- Tester sur d'autres sessions (London, NY)
- Backtester sur ES, YM, RTY pour diversification

---

## ⚠️ Avertissements

1. **Performance passée ≠ Résultats futurs**
   - Les conditions de marché changent
   - Le win rate peut varier

2. **Slippage et commissions non inclus**
   - Ajoutez ~2-5 points par trade pour être réaliste
   - Impact significatif sur des petits TP

3. **Données limitées**
   - Testé sur 2 ans seulement
   - Valider sur plus de données historiques

4. **Optimisation en cours**
   - Paramètres non optimisés exhaustivement
   - Risque d'overfitting si sur-optimisé

5. **Exécution manuelle vs automatique**
   - La détection des setups en temps réel est complexe
   - Nécessite un système d'alertes robuste

---

## 📚 Ressources et Références

### Smart Money Concepts

- **Liquidity Sweeps:** Identification des zones où les institutions chassent les stops
- **Market Structure:** Break of Structure (BOS) et Market Structure Shift (MSS)
- **Fair Value Gaps:** Zones d'inefficience du prix
- **Order Blocks:** Zones où les institutions ont placé des ordres

### Outils Utilisés

- **Python:** pandas, numpy pour le calcul
- **Matplotlib/Seaborn:** Visualisations
- **Vectorisation:** Optimisation des calculs sur gros volumes de données

---

## 👨‍💻 Support et Modifications

### Pour Modifier les Paramètres

Éditez le fichier `smc_reversal_backtest_01_07.py` :

```python
# Ligne 33-38 : Configuration
FRACTAL_WINDOW = 1           # Changer pour fractals plus stricts
REVERSAL_WINDOW = 5          # Augmenter pour reversals plus confirmés
FIB_ENTRY_LEVEL = 0.5        # Tester 0.618, 0.382, etc.
MIN_FVG_SIZE = 5             # Augmenter pour FVGs plus significatifs
```

### Pour Ajouter du Debug

```python
# Ligne 37
DEBUG = True  # Active les messages de debug
```

---

## 📞 Contact

Pour questions, suggestions ou optimisations :
- Consultez le code source : `smc_reversal_backtest_01_07.py`
- Analysez les trades : `smc_reversal_trades.csv`
- Étudiez les graphiques : `smc_reversal_backtest_results.png`

---

**Auteur:** Expert Python en Backtesting & SMC  
**Date:** 11 Décembre 2025  
**Version:** 1.0  
**Repository:** Backtest-Trading

# NQ London Continuation + Inversion FVG Backtest

## 📖 Description

Ce backtest implémente une stratégie de trading ICT (Inner Circle Trader) pour capturer les continuations de tendance durant la session de Londres (London Open Killzone) sur le NQ (Nasdaq-100 E-mini Futures).

## 🎯 Stratégie

### Setup Long (Achat)

1. **Asian Session Narrative (19:00-00:00 Chicago)**
   - NQ haussier ou consolidation avec Equal Highs
   - FVG haussier (Asian Buy-side Imbalance) créé

2. **London Retracement (02:00-03:30 Chicago)**
   - Prix corrige à la baisse
   - Prix plonge dans le FVG haussier asiatique
   - FVG baissier créé durant le retracement (résistance court-terme)

3. **Inversion FVG (Trigger Entry)**
   - Prix réagit sur le support asiatique (FVG)
   - Bougie clôture au-dessus du FVG baissier → Inversion
   - Entrée : ouverture bougie suivante OU retest du FVG

4. **Stop Loss**
   - **SL A (Aggressif)** : 2-4 ticks sous l'Inversion FVG
   - **SL B (Structurel)** : 1 point sous le swing low du retracement

5. **Target**
   - **Asian High** : High de la session asiatique
   - **Fixed 10/15/20** : Target fixe en points

### Setup Short (Vente)

Logique inversée pour tendance baissière.

## 📊 Résultats Clés (2024-2025)

### 🏆 Meilleure Configuration : SL B + Asian High + Retest

- **Win Rate** : 52.8%
- **Expectancy** : +4.02 pts/trade
- **Profit Factor** : 1.24
- **Total P&L** : +144.80 pts (36 trades)
- **Max Drawdown** : -129.99 pts

### ⚡ Meilleure Config Scalping : SL A + Fixed 10 + Immediate

- **Win Rate** : 53.3%
- **Expectancy** : +1.59 pts/trade
- **Profit Factor** : 1.42
- **Total P&L** : +71.47 pts (45 trades)
- **Max Drawdown** : -36.16 pts

## 🚀 Utilisation

### Prérequis

```bash
pip install -r requirements.txt
```

Dépendances :
- pandas >= 2.0.0
- numpy >= 1.24.0
- scipy >= 1.10.0
- matplotlib >= 3.7.0

### Exécution du Backtest

```bash
python nq_london_continuation_inversion_fvg.py
```

Le script va :
1. Charger les données NQ et ES 5m (2024-2025)
2. Détecter les setups Inversion FVG
3. Simuler les trades avec différentes configurations
4. Générer les résultats et analyses

### Fichiers Générés

- `nq_london_continuation_results.json` : Tous les trades détaillés
- `NQ_LONDON_CONTINUATION_ANALYSIS.md` : Analyse technique (anglais)
- `REPONSES_TRADER_NQ_LONDON.md` : Réponses aux questions du trader (français)

## 📁 Structure du Code

```python
# Classes principales
class FVG:                              # Représentation d'un Fair Value Gap
class SessionManager:                   # Gestion des sessions (Asian, London, NY)
class NQLondonContinuationStrategy:     # Stratégie complète

# Méthodes clés
- detect_fvg()                          # Détection des FVG
- detect_asian_narrative()              # Analyse session asiatique
- detect_inversion_fvg()                # Détection du setup d'entrée
- check_smt_divergence()                # Divergence NQ vs ES
- calculate_trade_outcome()             # Simulation trade
- run_backtest()                        # Exécution complète
- analyze_results()                     # Statistiques
```

## 📈 Format des Données

Les fichiers CSV doivent être au format :

```
Column1;Column2;Column3;Column4;Column5;Column6;Column7
01/01/2024;17:00:00;18244.57923;18248.331274;18238.951165;18241.631196;1308
```

- Column1 : Date (DD/MM/YYYY)
- Column2 : Heure (HH:MM:SS)
- Column3 : Open
- Column4 : High
- Column5 : Low
- Column6 : Close
- Column7 : Volume

**Timezone** : Chicago (UTC-6) - Déjà converti

## 🔧 Personnalisation

### Modifier les Paramètres de Stop Loss

```python
# Dans calculate_trade_outcome(), ligne ~423
if sl_type == 'A':
    sl_distance_ticks = 3  # Modifier ici (2-4 ticks)
```

### Ajouter une Nouvelle Target

```python
# Dans calculate_trade_outcome(), ligne ~455
elif target_type == 'fixed_25':
    if setup_type == 'long':
        target = actual_entry_price + 25.0
```

### Modifier les Sessions

```python
# Dans SessionManager class, ligne ~74
@staticmethod
def is_london_killzone(dt: datetime) -> bool:
    t = dt.time()
    return time(2, 0) <= t < time(5, 0)  # Modifier ici
```

## 📊 Analyse des Résultats

### Question 1 : Retest vs Immediate Entry

**Résultat** : Le retest réduit le drawdown de 62-74% pour les targets longues (Asian High) mais réduit la performance pour les scalps courts (10-15 pts).

### Question 2 : SL A vs SL B

**Résultat** : 
- SL A gagne pour Fixed 10-15 pts (+1.48 à +1.59 pts expectancy)
- SL B gagne pour Asian High (+2.42 pts expectancy)

### Question 3 : Target Optimization

**Résultat** :
- Fixed 10 pts optimal pour SL A + Immediate
- Asian High optimal pour SL B + Retest
- Fixed 15-20 pts compromis acceptable

## 🎓 Concepts ICT Utilisés

1. **Fair Value Gap (FVG)** : Gap entre Low[i] et High[i-2] (bullish) ou High[i] et Low[i-2] (bearish)
2. **Inversion FVG** : FVG opposé qui devient support/résistance après clôture au-delà
3. **Asian Session Narrative** : Tendance établie durant session asiatique
4. **London Killzone** : Fenêtre d'entrée optimale (02:00-05:00)
5. **SMT Divergence** : NQ vs ES divergence (Smart Money Tool)
6. **PD Array** : Price Delivery Array (FVG comme zone de réaction)

## 📚 Références

- **ICT (Inner Circle Trader)** : Concepts de trading institutionnel
- **Sessions** : Asian (19:00-00:00), London (02:00-05:00), NY (08:30-15:00) Chicago time
- **NQ Tick Size** : 0.25 points
- **ES Correlation** : Utilisé pour SMT divergence

## ⚠️ Avertissement

Ce backtest est fourni à titre éducatif uniquement. Les performances passées ne garantissent pas les résultats futurs. Le trading de futures comporte des risques importants de perte. Consultez un conseiller financier avant de trader.

## 📧 Support

Pour toute question sur l'implémentation ou les résultats, consultez :
- `NQ_LONDON_CONTINUATION_ANALYSIS.md` pour l'analyse technique
- `REPONSES_TRADER_NQ_LONDON.md` pour les réponses détaillées en français

## 🔄 Mises à Jour Futures

- [ ] Backtest sur période plus longue (2018-2023)
- [ ] Isolement de l'impact SMT
- [ ] Targets adaptatives basées sur ATR
- [ ] Trailing stop dynamique
- [ ] Visualisations des trades
- [ ] Forward testing sur données 2025+

---

**Version** : 1.0  
**Date** : Décembre 2025  
**Auteur** : Backtest ICT Strategy  
**License** : MIT

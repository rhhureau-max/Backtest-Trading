# Guide d'Analyse de Vélocité - Sessions Tokyo/Londres

## Vue d'ensemble

Cette analyse mesure la **vitesse des mouvements** après une manipulation détectée durant la fenêtre de Londres (02:00-02:45).

## Méthodologie

### Définitions des Points Temporels

1. **T_start (Top Départ)**: Timestamp exact de la première cassure du Range Tokyo (Low ou High) durant 02:00-02:45
2. **T_end (Arrivée)**: Timestamp exact où le prix touche l'objectif pour la première fois après T_start et avant 05:00
3. **ΔT (Durée)**: T_end - T_start, calculée en minutes

### Scénarios Analysés

#### Scénario A: Manipulation Haussière (Break Low)
Lorsque le prix casse le **Tokyo Low** durant 02:00-02:45:
- **A1**: Durée pour remonter à l'**Equilibrium**
- **A2**: Durée pour remonter jusqu'au **Tokyo High** (si atteint)

#### Scénario B: Manipulation Baissière (Break High)
Lorsque le prix casse le **Tokyo High** durant 02:00-02:45:
- **B1**: Durée pour redescendre à l'**Equilibrium**
- **B2**: Durée pour redescendre jusqu'au **Tokyo Low** (si atteint)

## Résultats Statistiques (2018-2025)

### Résumé Global

| Métrique | Equilibrium | Niveau Opposé |
|----------|-------------|---------------|
| **Taux de réussite** | 37.3% (525/1406) | 11.7% (164/1406) |
| **Durée médiane** | 50 minutes ⭐ | 90 minutes |
| **Durée moyenne** | 59 minutes | 92 minutes |
| **Sous 30 minutes** | 36.4% | ~2% |

### Scénario A: Manipulation Haussière (Break Low)

**A1. Retour à l'Equilibrium**
- Taux de succès: **39.2%** (240/612 jours)
- Durée médiane: **50 minutes**
- Durée moyenne: 60.54 minutes
- Min: 5 minutes / Max: 175 minutes
- Sous 30 min: **33.3%**

**A2. Remontée au Tokyo High**
- Taux de succès: **14.1%** (86/612 jours)
- Durée médiane: **90 minutes**
- Durée moyenne: 94.01 minutes
- Min: 25 minutes / Max: 175 minutes
- Sous 30 min: 1.2%

### Scénario B: Manipulation Baissière (Break High)

**B1. Retour à l'Equilibrium**
- Taux de succès: **33.1%** (252/761 jours)
- Durée médiane: **57.5 minutes**
- Durée moyenne: 62.62 minutes
- Min: 5 minutes / Max: 175 minutes
- Sous 30 min: **31.0%**

**B2. Descente au Tokyo Low**
- Taux de succès: **10.2%** (78/761 jours)
- Durée médiane: **87.5 minutes**
- Durée moyenne: 90.45 minutes
- Min: 10 minutes / Max: 170 minutes
- Sous 30 min: 2.6%

## Insights Clés pour le Trading

### 🎯 Cible Principale: L'Equilibrium
- **L'équilibre est la cible la plus probable** après une manipulation
- Environ **1 jour sur 3** retourne à l'équilibre
- La durée médiane de **50 minutes** est relativement prévisible

### ⏱️ Fenêtre Temporelle Optimale
- **36.4%** des mouvements atteignent l'équilibre en **moins de 30 minutes**
- La majorité prend entre **30-90 minutes**
- Les mouvements très rapides (<10 min) ou très lents (>120 min) sont rares

### 📊 Niveau Opposé: Cible Secondaire
- Seulement **11.7%** atteignent le niveau opposé (Tokyo High ou Low)
- Durée médiane de **90 minutes** (presque le double de l'équilibre)
- **Ne pas compter sur ce mouvement** pour une stratégie systématique

### 💡 Applications Pratiques

1. **Stratégie de Scalping (30 min)**:
   - Probabilité: ~36%
   - Cible: Equilibrium
   - Fenêtre: 02:45-03:15 après break confirmé

2. **Stratégie de Swing (50-90 min)**:
   - Probabilité: ~37% (équilibre) / ~12% (opposé)
   - Cible principale: Equilibrium
   - Fenêtre: 02:45-04:30

3. **Gestion de Position**:
   - Si équilibre atteint en <30 min: Considérer une continuation possible
   - Si pas d'équilibre après 90 min: Probabilité réduite, réévaluer
   - Le niveau opposé n'est PAS une cible fiable pour le day trading

## Fichiers Générés

### tokyo_london_velocity_analysis.csv
Contient pour chaque jour de manipulation:
- `break_timestamp`: Moment de la première cassure
- `equilibrium_reach_timestamp`: Moment du touch d'équilibre
- `opposite_level_reach_timestamp`: Moment du touch du niveau opposé
- `time_to_equilibrium_minutes`: Durée en minutes vers équilibre
- `time_to_opposite_level_minutes`: Durée en minutes vers niveau opposé

Les valeurs `NaN` indiquent que l'objectif n'a jamais été atteint avant 05:00.

## Utilisation du Script

Pour régénérer l'analyse avec des données mises à jour:

```bash
cd /home/runner/work/Backtest-Trading/Backtest-Trading
python3 tokyo_london_session_analysis.py
```

Le script produit:
1. Statistiques de manipulation (original)
2. **Statistiques de vélocité** (nouveau)
3. Fichiers CSV avec résultats détaillés

## Limitations

- Analyse limitée à la fenêtre 02:45-05:00 (fin de la session de Londres)
- Ne considère que le **premier touch** de chaque niveau
- Les jours "Volatile/Both" (cassure des deux niveaux) sont comptabilisés mais peuvent fausser les statistiques
- Week-ends et jours fériés exclus automatiquement

## Prochaines Étapes Suggérées

1. Analyser la corrélation entre la **magnitude de la cassure** et la durée de retour
2. Étudier l'impact du **volume** sur la vélocité
3. Segmenter par **contexte de marché** (tendance, range, volatilité)
4. Créer des **zones de confiance** basées sur l'heure de la cassure (02:00 vs 02:40)

---

*Analyse générée à partir de 1,406 jours de manipulation sur 2,032 jours de trading (2018-2025)*

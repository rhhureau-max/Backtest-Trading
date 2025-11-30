# Guide de Détection des Liquidity Sweeps & Fair Value Gaps (FVG)

## 📊 Qu'est-ce qu'un Liquidity Sweep?

Un **liquidity sweep** (balayage de liquidité), également appelé "stop hunt" ou "liquidity grab", est un pattern de prix caractéristique où :

1. **Le prix franchit** un niveau clé de support/résistance (swing high/low précédent)
2. **Déclenchement des ordres** : Les stop-loss et ordres limites placés à ce niveau sont exécutés
3. **Retour rapide** : Le prix revient rapidement dans la zone précédente
4. **Volume élevé** : Souvent accompagné d'une augmentation significative du volume

### 🎯 Pourquoi les Liquidity Sweeps se produisent-ils?

Les grands acteurs du marché (institutions, market makers) ont besoin de liquidité pour exécuter leurs ordres importants. Les ordres stop-loss et limites se concentrent autour des niveaux de prix évidents (swing highs/lows). En poussant le prix à travers ces niveaux, les institutions accèdent à cette liquidité, puis le prix revient une fois les ordres remplis.

---

## 📈 Qu'est-ce qu'un Fair Value Gap (FVG)?

Un **Fair Value Gap** (FVG), également appelé "imbalance" ou "inefficiency", est un déséquilibre de prix entre 3 bougies consécutives :

### Types de FVG

| Type | Description | Formation |
|------|-------------|-----------|
| **Bullish FVG** | Gap haussier | High de bougie 1 < Low de bougie 3 |
| **Bearish FVG** | Gap baissier | Low de bougie 1 > High de bougie 3 |

### Pourquoi les FVG sont importants?

1. **Zones d'ordres non remplis** : Le prix a bougé trop vite, laissant des ordres non exécutés
2. **Aimants pour le prix** : Le marché tend à revenir "remplir" ces gaps
3. **Zones d'entrée institutionnelles** : Les smart money utilisent souvent ces zones pour leurs entrées
4. **Confirmation des setups** : Un sweep + FVG = setup à haute probabilité

---

## 🔥 Combiner Sweeps + FVG (Setup Optimal)

La combinaison d'un liquidity sweep avec un FVG crée un setup de trading puissant :

### Setup Bullish (Achat)
```
1. Bullish sweep (prix casse sous un swing low puis remonte)
2. Bullish FVG existe au-dessus du point de sweep
3. Entrée : Après le sweep, en visant le remplissage du FVG
```

### Setup Bearish (Vente)
```
1. Bearish sweep (prix casse au-dessus d'un swing high puis redescend)
2. Bearish FVG existe en-dessous du point de sweep
3. Entrée : Après le sweep, en visant le remplissage du FVG
```

---

## 📁 Structure des Données du Repository

### Format des fichiers CSV

| Colonne | Nom    | Format/Description |
|---------|--------|-------------------|
| 1       | Date   | DD/MM/YYYY        |
| 2       | Time   | HH:MM:SS          |
| 3       | Open   | Prix d'ouverture  |
| 4       | High   | Plus haut         |
| 5       | Low    | Plus bas          |
| 6       | Close  | Prix de clôture   |
| 7       | Volume | Volume échangé    |

**Séparateur** : Point-virgule (`;`)

### Timeframes disponibles

- `1m` - 1 minute (données compressées en .zip pour les anciennes années)
- `5m` - 5 minutes
- `15m` - 15 minutes
- `1H` - 1 heure
- `4H` - 4 heures
- `1D` - 1 jour

### Nommage des fichiers
```
ANNÉE TIMEFRAME.csv
Exemples: "2025 15m.csv", "2024 1H.csv", "2023 4H.csv"
```

---

## 🔍 Algorithme de Détection

### Étape 1: Identification des Points de Swing

**Swing High (Sommet local)**
```
Un point où: High[i] > max(High[i-n:i]) ET High[i] > max(High[i+1:i+n+1])
```

**Swing Low (Creux local)**
```
Un point où: Low[i] < min(Low[i-n:i]) ET Low[i] < min(Low[i+1:i+n+1])
```

Où `n` est le lookback (par défaut: 5 bougies)

### Étape 2: Détection des Fair Value Gaps (FVG)

#### Bullish FVG (Gap haussier)
```python
# Conditions pour un bullish FVG:
if candle1_high < candle3_low:
    gap_low = candle1_high
    gap_high = candle3_low
    # Le FVG est la zone entre gap_low et gap_high
```

#### Bearish FVG (Gap baissier)
```python
# Conditions pour un bearish FVG:
if candle1_low > candle3_high:
    gap_low = candle3_high
    gap_high = candle1_low
    # Le FVG est la zone entre gap_low et gap_high
```

### Étape 3: Détection des Sweeps

#### Bearish Sweep (au-dessus d'un swing high)
```python
# Conditions pour un bearish sweep:
1. High[sweep] > swing_high.price * (1 + threshold)  # Prix dépasse le swing high
2. Close[sweep] < swing_high.price                   # Clôture sous le swing high
3. Close[sweep+1..3] < swing_high.price              # Continuation baissière
   OU Volume[sweep] > avg_volume * multiplier        # Volume élevé
```

#### Bullish Sweep (en-dessous d'un swing low)
```python
# Conditions pour un bullish sweep:
1. Low[sweep] < swing_low.price * (1 - threshold)    # Prix dépasse le swing low
2. Close[sweep] > swing_low.price                    # Clôture au-dessus du swing low
3. Close[sweep+1..3] > swing_low.price               # Continuation haussière
   OU Volume[sweep] > avg_volume * multiplier        # Volume élevé
```

### Étape 4: Combinaison Sweep + FVG

Pour chaque sweep détecté, le script recherche un FVG correspondant dans les N bougies précédentes :
- **Bullish sweep** → Recherche un **Bullish FVG** au-dessus du prix actuel
- **Bearish sweep** → Recherche un **Bearish FVG** en-dessous du prix actuel

---

## 🛠️ Utilisation du Script Python

### Installation des dépendances
```bash
pip install pandas numpy
```

### Commandes de base

```bash
# Analyser 2025 sur timeframe 15m (défaut)
python liquidity_sweep_detector.py

# Analyser une année/timeframe spécifique
python liquidity_sweep_detector.py --year 2024 --timeframe 1H

# Afficher la méthodologie
python liquidity_sweep_detector.py --methodology

# Analyser tous les timeframes pour une année
python liquidity_sweep_detector.py --year 2025 --all-timeframes
```

### Paramètres avancés

| Paramètre | Défaut | Description |
|-----------|--------|-------------|
| `--swing-lookback` | 5 | Nombre de bougies pour identifier les swing points |
| `--sweep-threshold` | 0.05 | Pourcentage minimum de dépassement du swing level |
| `--reversal-lookback` | 3 | Nombre de bougies pour confirmer le retournement |
| `--volume-multiplier` | 1.5 | Ratio de volume minimum pour confirmation |
| `--fvg-min-size` | 0.01 | Taille minimum du FVG en % du prix |
| `--fvg-lookback` | 20 | Nombre de bougies pour chercher les FVG proches |
| `--no-fvg` | - | Désactiver la détection des FVG (sweeps uniquement) |

```bash
# Exemple avec paramètres personnalisés (Sweep + FVG)
python liquidity_sweep_detector.py \
    --year 2025 \
    --timeframe 4H \
    --swing-lookback 7 \
    --volume-multiplier 2.0 \
    --fvg-min-size 0.02

# Analyser sans les FVG (sweeps uniquement)
python liquidity_sweep_detector.py --year 2025 --timeframe 1H --no-fvg
```

---

## 📈 Considérations par Timeframe

### 1m / 5m - Scalping
- **Caractéristiques** : Sweeps très fréquents, plus de bruit
- **Usage** : Scalping, entrées précises
- **Recommandation** : Augmenter `swing-lookback` à 7-10

### 15m / 1H - Day Trading
- **Caractéristiques** : Bon équilibre signal/bruit
- **Usage** : Day trading, swing court terme
- **Recommandation** : Paramètres par défaut

### 4H / 1D - Swing Trading
- **Caractéristiques** : Signaux plus significatifs, moins fréquents
- **Usage** : Swing trading, positions moyen terme
- **Recommandation** : Réduire `sweep-threshold` à 0.02-0.03

---

## 📊 Interprétation des Résultats

### Types de Sweeps

| Type | Description | Implication |
|------|-------------|-------------|
| **Bullish Sweep** | Balayage sous un swing low | Signal d'achat potentiel |
| **Bearish Sweep** | Balayage au-dessus d'un swing high | Signal de vente potentiel |

### Types de FVG

| Type | Description | Implication |
|------|-------------|-------------|
| **Bullish FVG** | Gap haussier (non rempli) | Zone cible pour entrée long |
| **Bearish FVG** | Gap baissier (non rempli) | Zone cible pour entrée short |
| **Filled FVG** | FVG déjà rempli par le prix | Zone déjà utilisée |

### Indicateurs de qualité

1. **Volume Ratio > 1.5x** : Sweep confirmé par le volume
2. **Reversal Candles ≤ 3** : Retournement rapide (plus significatif)
3. **Sweep + FVG** : Combinaison = setup haute probabilité
4. **FVG Size** : Plus le gap est grand, plus il est significatif

### Exemple de sortie
```
📊 SWEEPS:
Total sweeps detected: 45
  - Bullish sweeps (below swing lows): 22
  - Bearish sweeps (above swing highs): 23
  - High volume sweeps (>1.5x avg): 18
  - Sweeps with nearby FVG: 12

📈 FAIR VALUE GAPS (FVG):
Total FVGs detected: 156
  - Bullish FVGs: 78
  - Bearish FVGs: 78
  - Filled: 142
  - Still open: 14

--- Last 10 Sweeps (with FVG info) ---
[2025-11-11 08:45:00] BULLISH sweep | Level: 25596.25 | Swept to: 25560.25 | Close: 25627.00 | Vol ratio: 7.23x | FVG: 25650.00-25680.00
```

Interprétation :
- **Date/Heure** : Le sweep s'est produit le 11/11/2025 à 08:45
- **Type** : Bullish (balayage sous un support)
- **Level** : Le swing low était à 25596.25
- **Swept to** : Le prix est descendu jusqu'à 25560.25 (36 points sous le level)
- **Close** : La bougie a clôturé à 25627.00 (au-dessus du level = retournement)
- **Vol ratio** : Volume 7.23x supérieur à la moyenne (très significatif)
- **FVG** : Un FVG bullish existe entre 25650 et 25680 (zone cible potentielle)

---

## 🔧 Personnalisation du Code

### Importer le détecteur dans votre propre script

```python
from liquidity_sweep_detector import LiquiditySweepDetector

# Créer une instance avec paramètres personnalisés
detector = LiquiditySweepDetector(
    swing_lookback=5,
    sweep_threshold_pct=0.05,
    reversal_lookback=3,
    volume_multiplier=1.5,
    fvg_min_size_pct=0.01,
    fvg_lookback=20
)

# Charger et analyser les données (avec FVG)
df, sweeps, fvgs = detector.analyze_file("2025 15m.csv")

# Filtrer les sweeps avec un FVG associé
sweeps_with_fvg = [s for s in sweeps if s.nearby_fvg is not None]
print(f"Sweeps avec FVG: {len(sweeps_with_fvg)}")

# Afficher les setups bullish (sweep + FVG)
for sweep in sweeps_with_fvg:
    if sweep.sweep_type == 'bullish':
        print(f"SETUP BULLISH: {sweep}")
        print(f"  → Cible FVG: {sweep.nearby_fvg.gap_low:.2f} - {sweep.nearby_fvg.gap_high:.2f}")

# Filtrer les FVG non remplis (zones cibles potentielles)
open_fvgs = [f for f in fvgs if not f.is_filled]
print(f"\nFVG ouverts (cibles potentielles): {len(open_fvgs)}")
for fvg in open_fvgs[-5:]:
    print(fvg)
```

### Exporter les résultats en CSV

```python
import pandas as pd
from liquidity_sweep_detector import LiquiditySweepDetector

detector = LiquiditySweepDetector()
df, sweeps, fvgs = detector.analyze_file("2025 15m.csv")

# Exporter les sweeps avec info FVG
sweep_data = [{
    'datetime': s.sweep_datetime,
    'type': s.sweep_type,
    'level': s.swing_level,
    'sweep_price': s.sweep_price,
    'close': s.close_price,
    'volume': s.volume,
    'volume_ratio': s.volume_ratio,
    'has_fvg': s.nearby_fvg is not None,
    'fvg_low': s.nearby_fvg.gap_low if s.nearby_fvg else None,
    'fvg_high': s.nearby_fvg.gap_high if s.nearby_fvg else None
} for s in sweeps]

sweep_df = pd.DataFrame(sweep_data)
sweep_df.to_csv('detected_sweeps.csv', index=False)

# Exporter les FVG
fvg_data = [{
    'datetime': f.datetime,
    'type': f.fvg_type,
    'gap_low': f.gap_low,
    'gap_high': f.gap_high,
    'gap_size': f.gap_size,
    'gap_size_pct': f.gap_size_pct,
    'is_filled': f.is_filled,
    'filled_datetime': f.filled_datetime
} for f in fvgs]

fvg_df = pd.DataFrame(fvg_data)
fvg_df.to_csv('detected_fvgs.csv', index=False)
```

---

## ⚠️ Limitations et Avertissements

1. **Pas un conseil d'investissement** : Ce script est un outil d'analyse technique, pas une recommandation de trading
2. **Faux positifs** : Certains sweeps détectés peuvent ne pas être significatifs
3. **Contexte nécessaire** : Les sweeps doivent être analysés dans le contexte du marché global
4. **Confirmation requise** : Utilisez d'autres indicateurs pour confirmer les signaux

---

## 📚 Ressources Complémentaires

Pour approfondir votre compréhension des concepts liés aux liquidity sweeps :

- **Smart Money Concepts (SMC)** : Théorie expliquant comment les institutions manipulent les prix pour accéder à la liquidité. Recherchez des tutoriels sur YouTube ou des articles spécialisés sur le trading institutionnel.

- **Order Flow Trading** : Analyse du flux d'ordres pour comprendre les mouvements de prix. Cette approche complète l'analyse des liquidity sweeps en révélant les intentions des gros acteurs.

- **Volume Profile Analysis** : Technique d'analyse du volume par niveau de prix, utile pour identifier où se concentre la liquidité.

- **Market Structure** : Comprendre la structure du marché (higher highs, lower lows, break of structure) est essentiel pour contextualiser les liquidity sweeps.

---

## 📝 Changelog

- **v2.0** - Ajout de la détection des Fair Value Gaps (FVG)
  - Détection automatique des FVG bullish et bearish
  - Suivi du remplissage des FVG
  - Combinaison Sweep + FVG pour des setups optimaux
  - Nouveaux paramètres: `--fvg-min-size`, `--fvg-lookback`, `--no-fvg`
  - Documentation mise à jour avec la méthodologie FVG

- **v1.0** - Première version avec détection de base des liquidity sweeps
  - Support multi-timeframe (1m, 5m, 15m, 1H, 4H, 1D)
  - Confirmation par volume
  - Paramètres configurables

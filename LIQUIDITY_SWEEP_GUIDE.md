# Guide de Détection des Liquidity Sweeps (Balayages de Liquidité)

## 📊 Qu'est-ce qu'un Liquidity Sweep?

Un **liquidity sweep** (balayage de liquidité), également appelé "stop hunt" ou "liquidity grab", est un pattern de prix caractéristique où :

1. **Le prix franchit** un niveau clé de support/résistance (swing high/low précédent)
2. **Déclenchement des ordres** : Les stop-loss et ordres limites placés à ce niveau sont exécutés
3. **Retour rapide** : Le prix revient rapidement dans la zone précédente
4. **Volume élevé** : Souvent accompagné d'une augmentation significative du volume

### 🎯 Pourquoi les Liquidity Sweeps se produisent-ils?

Les grands acteurs du marché (institutions, market makers) ont besoin de liquidité pour exécuter leurs ordres importants. Les ordres stop-loss et limites se concentrent autour des niveaux de prix évidents (swing highs/lows). En poussant le prix à travers ces niveaux, les institutions accèdent à cette liquidité, puis le prix revient une fois les ordres remplis.

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

### Étape 2: Détection des Sweeps

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

```bash
# Exemple avec paramètres personnalisés
python liquidity_sweep_detector.py \
    --year 2025 \
    --timeframe 4H \
    --swing-lookback 7 \
    --volume-multiplier 2.0
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

### Indicateurs de qualité

1. **Volume Ratio > 1.5x** : Sweep confirmé par le volume
2. **Reversal Candles ≤ 3** : Retournement rapide (plus significatif)
3. **Sweep Amount** : Plus le dépassement est important, plus le sweep est significatif

### Exemple de sortie
```
[2025-11-11 08:45:00] BULLISH sweep | Level: 25596.25 | Swept to: 25560.25 | Close: 25627.00 | Vol ratio: 7.23x
```

Interprétation :
- **Date/Heure** : Le sweep s'est produit le 11/11/2025 à 08:45
- **Type** : Bullish (balayage sous un support)
- **Level** : Le swing low était à 25596.25
- **Swept to** : Le prix est descendu jusqu'à 25560.25 (36 points sous le level)
- **Close** : La bougie a clôturé à 25627.00 (au-dessus du level = retournement)
- **Vol ratio** : Volume 7.23x supérieur à la moyenne (très significatif)

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
    volume_multiplier=1.5
)

# Charger et analyser les données
df, sweeps = detector.analyze_file("2025 15m.csv")

# Filtrer les sweeps à haut volume
high_volume_sweeps = [s for s in sweeps if s.volume_ratio >= 2.0]

# Afficher les bullish sweeps uniquement
bullish_sweeps = [s for s in sweeps if s.sweep_type == 'bullish']
for sweep in bullish_sweeps:
    print(sweep)
```

### Exporter les résultats en CSV

```python
import pandas as pd
from liquidity_sweep_detector import LiquiditySweepDetector

detector = LiquiditySweepDetector()
df, sweeps = detector.analyze_file("2025 15m.csv")

# Convertir en DataFrame
sweep_data = [{
    'datetime': s.sweep_datetime,
    'type': s.sweep_type,
    'level': s.swing_level,
    'sweep_price': s.sweep_price,
    'close': s.close_price,
    'volume': s.volume,
    'volume_ratio': s.volume_ratio
} for s in sweeps]

sweep_df = pd.DataFrame(sweep_data)
sweep_df.to_csv('detected_sweeps.csv', index=False)
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

- **v1.0** - Première version avec détection de base des liquidity sweeps
  - Support multi-timeframe (1m, 5m, 15m, 1H, 4H, 1D)
  - Confirmation par volume
  - Paramètres configurables

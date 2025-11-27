# Analyse des Fair Value Gaps (FVG) - Bougie 8h30 Chicago

## 📊 Résumé de l'analyse

**Instrument:** Nasdaq Mini Futures  
**Période analysée:** 2018-2025  
**Bougie cible:** 08:30:00 (Heure Chicago) / 15:30:00 (Heure Paris)

---

## 📈 Définition du FVG

Un **Fair Value Gap (FVG)** est identifié lorsque la mèche (high) de la bougie N-1 et la mèche (low) de la bougie N+1 ne se chevauchent pas sur la bougie N:

- **FVG Haussier:** Le LOW de la bougie N+1 est supérieur au HIGH de la bougie N-1
- **FVG Baissier:** Le HIGH de la bougie N+1 est inférieur au LOW de la bougie N-1

### Stratégie d'entrée
- Entrée en position à l'ouverture de la bougie N+2
  - 1 minute: entrée à 8h32
  - 5 minutes: entrée à 8h40
  - 15 minutes: entrée à 8h45

### Critère de non-retour
- **FVG Haussier:** Le prix ne descend pas en dessous du HIGH de N-1
- **FVG Baissier:** Le prix ne monte pas au-dessus du LOW de N-1

---

## 📉 Résultats par Timeframe

### ⏱️ Timeframe 1 Minute

**Total FVG détectés:** 817
- Haussiers: 461
- Baissiers: 356

#### Probabilité de NON-RETOUR dans le FVG

| Bougies | Global | Haussier | Baissier |
|:-------:|:------:|:--------:|:--------:|
| 5 | 58.75% | 60.30% | 56.74% |
| 6 | 56.06% | 57.70% | 53.93% |
| 7 | 53.98% | 55.75% | 51.69% |
| 8 | 52.39% | 54.45% | 49.72% |
| 9 | 49.57% | 51.41% | 47.19% |
| 10 | 48.47% | 50.11% | 46.35% |
| 11 | 47.49% | 49.24% | 45.22% |
| 12 | 46.51% | 47.94% | 44.66% |
| 13 | 45.53% | 47.29% | 43.26% |
| 14 | 44.06% | 45.77% | 41.85% |
| 15 | 42.72% | 44.03% | 41.01% |

---

### ⏱️ Timeframe 5 Minutes

**Total FVG détectés:** 925
- Haussiers: 498
- Baissiers: 427

#### Probabilité de NON-RETOUR dans le FVG

| Bougies | Global | Haussier | Baissier |
|:-------:|:------:|:--------:|:--------:|
| 5 | 58.27% | 57.03% | 59.72% |
| 6 | 55.46% | 54.02% | 57.14% |
| 7 | 53.41% | 52.41% | 54.57% |
| 8 | 51.24% | 50.60% | 51.99% |
| 9 | 50.16% | 50.00% | 50.35% |
| 10 | 48.97% | 49.20% | 48.71% |
| 11 | 48.43% | 48.39% | 48.48% |
| 12 | 47.03% | 46.18% | 48.01% |
| 13 | 45.84% | 45.18% | 46.60% |
| 14 | 44.86% | 44.58% | 45.20% |
| 15 | 44.22% | 43.37% | 45.20% |

---

### ⏱️ Timeframe 15 Minutes

**Total FVG détectés:** 892
- Haussiers: 466
- Baissiers: 426

#### Probabilité de NON-RETOUR dans le FVG

| Bougies | Global | Haussier | Baissier |
|:-------:|:------:|:--------:|:--------:|
| 5 | 62.22% | 65.24% | 58.92% |
| 6 | 59.19% | 61.37% | 56.81% |
| 7 | 57.85% | 60.09% | 55.40% |
| 8 | 56.50% | 59.01% | 53.76% |
| 9 | 55.49% | 57.73% | 53.05% |
| 10 | 54.48% | 56.87% | 51.88% |
| 11 | 53.70% | 56.22% | 50.94% |
| 12 | 52.80% | 55.15% | 50.23% |
| 13 | 51.35% | 53.43% | 49.06% |
| 14 | 50.45% | 52.36% | 48.36% |
| 15 | 49.22% | 50.64% | 47.65% |

---

## 🔍 Observations clés

### Par Timeframe

1. **15 minutes** présente les meilleures probabilités de non-retour:
   - À 5 bougies: 62.22% global
   - Les FVG haussiers performent mieux (65.24% à 5 bougies)

2. **1 minute** et **5 minutes** ont des performances similaires:
   - Environ 58% de non-retour à 5 bougies
   - Décroissance progressive vers ~43-44% à 15 bougies

### Par Type de FVG

- **Timeframe 1m:** Les FVG haussiers ont une meilleure performance (+3-4% vs baissiers)
- **Timeframe 5m:** Les FVG baissiers performent légèrement mieux (+1-2% vs haussiers)
- **Timeframe 15m:** Les FVG haussiers ont un net avantage (+5-7% vs baissiers)

### Tendance générale

- La probabilité de non-retour diminue avec le temps (ce qui est logique)
- Le timeframe 15 minutes maintient les meilleures probabilités même à l'horizon 15 bougies (49.22%)
- Les FVG haussiers ont globalement une meilleure tenue que les FVG baissiers

---

## 📋 Méthodologie

- **Données:** Fichiers CSV de 2018 à 2025
- **Échantillon total:** 
  - 1m: ~2.77 millions de bougies
  - 5m: ~554k bougies
  - 15m: ~185k bougies
- **Script:** `fvg_analysis.py`
- **Dépendances:** pandas

---

*Analyse générée automatiquement par le script `fvg_analysis.py`*

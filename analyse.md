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
  - 15 minutes: entrée à 9h00

### Critère de non-retour
- **FVG Haussier:** Le prix ne descend pas en dessous du LOW de N+1
- **FVG Baissier:** Le prix ne monte pas au-dessus du HIGH de N+1

---

## 📉 Résultats par Timeframe

### ⏱️ Timeframe 1 Minute

**Total FVG détectés:** 817
- Haussiers: 461
- Baissiers: 356

#### Probabilité de NON-RETOUR dans le FVG

| Bougies | Global | Haussier | Baissier |
|:-------:|:------:|:--------:|:--------:|
| 5 | 38.80% | 41.21% | 35.67% |
| 6 | 36.84% | 39.48% | 33.43% |
| 7 | 35.99% | 38.61% | 32.58% |
| 8 | 34.39% | 37.09% | 30.90% |
| 9 | 32.68% | 35.14% | 29.49% |
| 10 | 32.07% | 34.27% | 29.21% |
| 11 | 30.84% | 33.19% | 27.81% |
| 12 | 30.23% | 32.32% | 27.53% |
| 13 | 29.74% | 31.89% | 26.97% |
| 14 | 28.89% | 31.02% | 26.12% |
| 15 | 27.78% | 29.28% | 25.84% |

---

### ⏱️ Timeframe 5 Minutes

**Total FVG détectés:** 925
- Haussiers: 498
- Baissiers: 427

#### Probabilité de NON-RETOUR dans le FVG

| Bougies | Global | Haussier | Baissier |
|:-------:|:------:|:--------:|:--------:|
| 5 | 40.43% | 40.96% | 39.81% |
| 6 | 37.84% | 38.35% | 37.24% |
| 7 | 36.11% | 37.35% | 34.66% |
| 8 | 34.70% | 35.94% | 33.26% |
| 9 | 33.84% | 35.54% | 31.85% |
| 10 | 32.65% | 34.14% | 30.91% |
| 11 | 31.68% | 32.93% | 30.21% |
| 12 | 31.14% | 32.53% | 29.51% |
| 13 | 30.70% | 32.13% | 29.04% |
| 14 | 29.95% | 31.53% | 28.10% |
| 15 | 28.97% | 29.92% | 27.87% |

---

### ⏱️ Timeframe 15 Minutes

**Total FVG détectés:** 892
- Haussiers: 466
- Baissiers: 426

#### Probabilité de NON-RETOUR dans le FVG

| Bougies | Global | Haussier | Baissier |
|:-------:|:------:|:--------:|:--------:|
| 5 | 41.59% | 46.35% | 36.38% |
| 6 | 39.35% | 43.99% | 34.27% |
| 7 | 37.89% | 42.49% | 32.86% |
| 8 | 37.22% | 42.06% | 31.92% |
| 9 | 35.99% | 40.77% | 30.75% |
| 10 | 35.09% | 39.70% | 30.05% |
| 11 | 34.42% | 38.84% | 29.58% |
| 12 | 33.52% | 37.77% | 28.87% |
| 13 | 33.07% | 37.34% | 28.40% |
| 14 | 32.06% | 36.05% | 27.70% |
| 15 | 30.94% | 34.55% | 27.00% |

---

## 🔍 Observations clés

### Par Timeframe

1. **15 minutes** présente les meilleures probabilités de non-retour pour les FVG haussiers:
   - À 5 bougies: 46.35% pour les haussiers
   - Les FVG haussiers performent nettement mieux que les baissiers (+10% en moyenne)

2. **5 minutes** montre des performances équilibrées:
   - Environ 40% de non-retour à 5 bougies
   - Performance similaire entre haussiers et baissiers

3. **1 minute** a les résultats les plus serrés:
   - 38.80% global à 5 bougies
   - Les haussiers conservent un léger avantage (+5-6% vs baissiers)

### Par Type de FVG

- **Timeframe 1m:** Les FVG haussiers ont une meilleure performance (+5-6% vs baissiers)
- **Timeframe 5m:** Performances relativement équilibrées (+1-2% pour haussiers)
- **Timeframe 15m:** Les FVG haussiers ont un net avantage (+8-10% vs baissiers)

### Tendance générale

- La probabilité de non-retour diminue avec le temps (ce qui est logique)
- Le timeframe 15 minutes maintient les meilleures probabilités pour les FVG haussiers
- Les FVG haussiers ont globalement une meilleure tenue que les FVG baissiers sur tous les timeframes

---

## 📋 Méthodologie

- **Données:** Fichiers CSV de 2018 à 2025
- **Échantillon total:** 
  - 1m: ~2.77 millions de bougies
  - 5m: ~554k bougies
  - 15m: ~185k bougies
- **Script:** `fvg_analysis.py`
- **Dépendances:** pandas

### Critère de non-retour utilisé
- **FVG Haussier:** Le prix ne descend pas en dessous du LOW de la bougie N+1
- **FVG Baissier:** Le prix ne monte pas au-dessus du HIGH de la bougie N+1

---

*Analyse générée automatiquement par le script `fvg_analysis.py`*

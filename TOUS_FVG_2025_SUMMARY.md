# Tous les FVG de l'année 2025 - Résumé

## Vue d'ensemble

Cette analyse répertorie **TOUS** les Fair Value Gaps (FVG) détectés dans les données de trading pour l'année 2025, sur les timeframes 1 minute et 15 minutes.

## Résultats globaux

| Timeframe | Nombre total de FVGs | Bullish | Bearish | Gap moyen |
|-----------|---------------------|---------|---------|-----------|
| 1 minute | 68 894 | 35 705 (51.8%) | 33 189 (48.2%) | 3.66 points |
| 15 minutes | 4 084 | 2 280 (55.8%) | 1 804 (44.2%) | 16.26 points |
| **TOTAL** | **72 978** | **37 985 (52.0%)** | **34 993 (48.0%)** | **4.21 points** |

## Statistiques détaillées

### 1 Minute (68 894 FVGs)

- **Type de mouvement:**
  - Bullish: 35 705 FVGs (51.8%)
  - Bearish: 33 189 FVGs (48.2%)

- **Taille des gaps:**
  - Gap moyen: 3.66 points
  - Gap maximum: 798.23 points
  - Gap minimum: 0.25 points

- **Période:**
  - Premier FVG: 01/01/2025 à 17:02
  - Dernier FVG: 12/11/2025 à 23:59

### 15 Minutes (4 084 FVGs)

- **Type de mouvement:**
  - Bullish: 2 280 FVGs (55.8%)
  - Bearish: 1 804 FVGs (44.2%)

- **Taille des gaps:**
  - Gap moyen: 16.26 points
  - Gap maximum: 697.24 points
  - Gap minimum: 0.25 points

- **Période:**
  - Premier FVG: 01/01/2025 à 17:30
  - Dernier FVG: 11/11/2025 à 23:00

## Observations

1. **Fréquence élevée**: Plus de 72 000 FVGs détectés en 2025, indiquant une forte volatilité sur les marchés

2. **Distribution équilibrée**: Les FVGs Bullish et Bearish sont presque équilibrés (52% vs 48%), suggérant un marché sans tendance dominante claire

3. **Échelle de temps**: 
   - Les FVGs sur 1m sont beaucoup plus fréquents (68 894) que sur 15m (4 084)
   - Les gaps moyens sont plus larges sur 15m (16.26 points) que sur 1m (3.66 points)

4. **Volatilité extrême**: Le gap maximum de 798.23 points (1m) indique des mouvements de prix très rapides et significatifs

## Scripts d'analyse

Pour générer la liste complète des FVGs:

### 1 Minute
```bash
python3 list_all_fvg_1m_2025.py
```

Pour sauvegarder dans un fichier:
```bash
python3 list_all_fvg_1m_2025.py > fvg_1m_2025_complet.txt
```

### 15 Minutes
```bash
python3 list_all_fvg_15m_2025.py
```

Pour sauvegarder dans un fichier:
```bash
python3 list_all_fvg_15m_2025.py > fvg_15m_2025_complet.txt
```

## Note importante

Ces scripts détectent **tous** les FVGs dans les données, pas seulement ceux à 8:30:00. Pour les FVGs spécifiques à 8:30:00, utilisez les scripts:
- `chronologie_fvg_1m_2025.py` pour 1 minute à 8:30
- `chronologie_fvg_15m_2025.py` pour 15 minutes à 8:30

## Format de sortie

Les scripts affichent:
- Le nombre total de FVGs
- Des statistiques (Bullish/Bearish, gaps moyens, min, max)
- Les 20 premiers FVGs chronologiquement
- Les 20 derniers FVGs chronologiquement

Pour voir tous les FVGs, redirigez la sortie vers un fichier texte.

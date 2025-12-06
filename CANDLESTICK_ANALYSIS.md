# Analyse des Configurations de Chandeliers - NQ (NASDAQ)

Ce document explique comment utiliser le script d'analyse des configurations de chandeliers (Marteau et Étoile Filante) sur les données NQ.

## Description

Le script `analyze_candlestick_patterns.py` analyse les données historiques du NQ (Nasdaq) pour détecter deux configurations de chandeliers spécifiques :

1. **Le Marteau (Hammer)** : Une bougie avec une longue mèche basse et une petite mèche haute
2. **L'Étoile Filante (Shooting Star)** : Une bougie avec une longue mèche haute et une petite mèche basse

## Paramètres de l'Analyse

### Période Globale
- Du 01/01/2018 à aujourd'hui
- Utilise les fichiers CSV disponibles dans le répertoire

### Timeframes Analysés
- **5 minutes** : Données d'origine
- **15 minutes** : Rééchantillonnage des données 5min
- **1 heure** : Rééchantillonnage des données 5min

### Filtrage Horaire
Seules les bougies dont l'heure d'ouverture se situe dans ces plages sont analysées :
- **Plage 1** : 02:00 à 05:00 (inclus)
- **Plage 2** : 08:30 à 11:00 (inclus)

## Définitions Techniques

Pour chaque bougie, le script calcule :

- **Corps** = |Close - Open|
- **Mèche_Haute** = High - max(Open, Close)
- **Mèche_Basse** = min(Open, Close) - Low
- **Taille_Totale** = High - Low

### Configuration 1 : Le Marteau (Hammer)
Une bougie est considérée comme un marteau si :
- **Mèche_Basse > 2 × Corps** (La mèche basse est au moins 2 fois plus grande que le corps)
- **Mèche_Haute < 0.1 × Taille_Totale** (La mèche haute est minuscule, max 10% de la bougie)

### Configuration 2 : L'Étoile Filante (Shooting Star)
Une bougie est considérée comme une étoile filante si :
- **Mèche_Haute > 2 × Corps** (La mèche haute est au moins 2 fois plus grande que le corps)
- **Mèche_Basse < 0.1 × Taille_Totale** (La mèche basse est minuscule, max 10% de la bougie)

## Installation

### Prérequis
```bash
pip install pandas numpy
```

## Utilisation

### Exécution du Script
```bash
python3 analyze_candlestick_patterns.py
```

### Sortie Attendue
Le script affiche un tableau avec les résultats :

```
======================================================================
RÉSULTATS DE L'ANALYSE
======================================================================

| Timeframe | Nombre de Marteaux | Nombre d'Étoiles Filantes |
|-----------|--------------------|-----------------------------|
| 5 min     |               3850 |                        3464 |
| 15 min    |               1409 |                        1090 |
| 1 Heure   |                503 |                         287 |

======================================================================
```

## Résultats Actuels

### Nombre de Patterns Détectés

Basé sur les données disponibles du 01/01/2018 à aujourd'hui :

- **5 minutes** : 3,850 Marteaux et 3,464 Étoiles Filantes détectés
- **15 minutes** : 1,409 Marteaux et 1,090 Étoiles Filantes détectés
- **1 heure** : 503 Marteaux et 287 Étoiles Filantes détectés

### Analyse du Pouvoir Prédictif

Le script analyse également si ces patterns sont prédictifs d'un retournement en vérifiant le prix sur les 3 bougies suivantes (t+1, t+2, t+3).

**Timeframe 5 minutes:**
- Marteaux: Win Rate de 48.55% (t+1) à 49.66% (t+2)
- Étoiles Filantes: Win Rate de 46.68% (t+1) à 47.55% (t+3)

**Timeframe 15 minutes:**
- Marteaux: Win Rate de 49.04% (t+1) à 50.75% (t+2)
- Étoiles Filantes: Win Rate de 46.33% (t+3) à 48.17% (t+1)

**Timeframe 1 heure:**
- Marteaux: Win Rate de 53.48% (t+1) à 57.46% (t+3) - Performance supérieure
- Étoiles Filantes: Win Rate de 45.99% (t+1) à 47.04% (t+2)

**Critères de Succès:**
- Pour les Marteaux (signal achat): Signal gagnant si Close(t+n) > Close(marteau)
- Pour les Étoiles Filantes (signal vente): Signal gagnant si Close(t+n) < Close(étoile)

## Structure du Code

Le script est organisé en plusieurs fonctions principales :

1. `load_nq_data()` : Charge toutes les données 5min des fichiers CSV
2. `resample_to_timeframe()` : Rééchantillonne vers 15min ou 1h
3. `filter_by_time_ranges()` : Filtre par plages horaires spécifiques
4. `calculate_candlestick_metrics()` : Calcule les métriques d'une bougie (corps, mèches)
5. `detect_hammer()` : Détecte les marteaux
6. `detect_shooting_star()` : Détecte les étoiles filantes
7. `count_patterns()` : Compte les patterns dans un dataset
8. `get_time_filtered_indices()` : Retourne les indices des bougies dans les plages horaires
9. `analyze_pattern_predictive_power()` : Analyse le pouvoir prédictif des patterns sur t+1, t+2, t+3
10. `print_pattern_summary()` : Affiche les tableaux récapitulatifs
11. `main()` : Orchestre l'analyse complète

## Fichiers de Données

Le script lit automatiquement tous les fichiers CSV 5min du format :
- `YYYY 5m.csv` (où YYYY est l'année de 2018 à 2025)

Format attendu des fichiers CSV :
```
Column1;Column2;Column3;Column4;Column5;Column6;Column7
01/01/2018;17:00:00;7503.739664;7511.940473;7499.63926;7511.3547;1451
```

Les colonnes représentent : Date, Time, Open, High, Low, Close, Volume

## Notes Importantes

- Le script utilise l'encodage UTF-8 avec BOM pour gérer correctement les fichiers CSV
- Les bougies avec une taille totale de 0 sont automatiquement exclues de l'analyse
- Le rééchantillonnage utilise : Open=first, High=max, Low=min, Close=last
- Les heures sont traitées en temps local (selon les données du fichier CSV)
- **Important**: L'analyse du pouvoir prédictif est calculée AVANT le filtrage par plages horaires pour avoir accès aux bougies futures (t+1, t+2, t+3), même si elles dépassent les limites horaires (05:00 ou 11:00)

# Fair Value Gap (FVG) Detector for Nasdaq Trading

Ce script Python permet d'analyser les données historiques du Nasdaq (NQ) pour détecter les Fair Value Gaps (FVG) - zones d'imbalance dans le marché.

## Fonctionnalités

1. **Génération de données mock** : Crée des données OHLC 1 minute pour tester le script
2. **Resampling** : Convertit les données 1 minute en bougies de 3 minutes avec agrégation correcte OHLC
3. **Détection FVG** : Identifie les zones d'imbalance (Fair Value Gaps) haussières et baissières
4. **Optimisé** : Utilise les opérations vectorisées de Pandas pour traiter de gros volumes de données (2018-2025)

## Installation

### Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de packages Python)

### Installation des dépendances

```bash
pip install -r requirements.txt
```

## Utilisation

### Mode Mock Data (par défaut)

Pour tester le script avec des données générées automatiquement :

```bash
python3 fvg_detector.py
```

### Mode Données Réelles

Pour analyser vos propres données historiques :

1. Ouvrez le fichier `fvg_detector.py`
2. Dans la fonction `main()`, commentez la ligne de génération de mock data
3. Décommentez et modifiez la ligne de chargement de données réelles :

```python
# Commenter cette ligne
# df_1min = generate_mock_data(num_candles=10000)

# Décommenter et modifier le chemin vers votre fichier
df_1min = load_real_data('2025 1m.csv')
```

## Format des Données

Le script supporte les fichiers CSV avec les formats suivants :

### Format 1 (avec colonnes séparées)
```
Date;Time;Open;High;Low;Close;Volume
01/01/2025;17:00:00;21927.62;21941.80;21911.64;21919.63;444
```

### Format 2 (simplifié)
```
Date,Open,High,Low,Close
2024-01-01 09:30:00,18000.0,18014.06,17997.24,18009.06
```

## Logique de Détection des FVG

### FVG Haussier (Bullish)
Un FVG haussier est détecté quand :
- `Low[i] > High[i-2]`
- Indique un mouvement haussier rapide avec un "gap" dans le prix

### FVG Baissier (Bearish)
Un FVG baissier est détecté quand :
- `High[i] < Low[i-2]`
- Indique un mouvement baissier rapide avec un "gap" dans le prix

## Resampling 1m → 3m

Le resampling suit les règles OHLC standard :
- **Open** : Premier prix d'ouverture de la période (1ère minute)
- **High** : Prix le plus haut des 3 minutes
- **Low** : Prix le plus bas des 3 minutes
- **Close** : Dernier prix de clôture de la période (3ème minute)

## Output

### Fichier CSV
Le script génère un fichier `fvg_results_3min.csv` contenant :
- Toutes les bougies 3 minutes
- Colonne `is_FVG` : True si un FVG est détecté
- Colonne `FVG_Type` : "Bullish" ou "Bearish"
- Colonnes `FVG_Top` et `FVG_Bottom` : Limites du gap

### Console
Le script affiche :
- Statistiques de génération/chargement des données
- Statistiques de resampling
- Nombre de FVG détectés (total, haussiers, baissiers)
- Les 5 derniers FVG avec leurs caractéristiques détaillées
- Statistiques finales

## Exemple de Sortie

```
================================================================================
DERNIERS 5 FVG DÉTECTÉS
================================================================================

FVG #3331
  Type: Bearish
  Date: 2024-01-08 08:00:00
  Top: 17796.11
  Bottom: 17793.44
  Gap Size: 2.67 points
  OHLC: O=17771.44 H=17793.44 L=17763.13 C=17791.45
--------------------------------------------------------------------------------

Résumé:
  Total FVG affichés: 5
  Taille moyenne du gap: 6.51 points
```

## Performance

Le script est optimisé pour traiter de gros volumes de données :
- Utilise les opérations vectorisées de Pandas (shift, masques booléens)
- Évite les boucles Python explicites
- Peut traiter plusieurs années de données 1 minute (2018-2025)

### Benchmark indicatif
- 10,000 bougies 1m → ~3,334 bougies 3m en < 1 seconde
- 250,000 bougies 1m (1 an environ) → traité en quelques secondes

## Structure du Code

- `generate_mock_data()` : Génère des données de test réalistes
- `resample_to_3min()` : Convertit 1m en 3m avec agrégation OHLC
- `detect_fvg()` : Détecte les FVG avec logique vectorisée
- `display_last_fvgs()` : Affiche les derniers FVG détectés
- `load_real_data()` : Charge des données depuis CSV
- `main()` : Orchestre l'ensemble du processus

## Personnalisation

### Changer le nombre de bougies mock
```python
df_1min = generate_mock_data(num_candles=50000)
```

### Changer le nombre de FVG affichés
```python
display_last_fvgs(df_result, n=10)
```

### Changer l'intervalle de resampling
Modifier la fonction `resample_to_3min()` :
```python
df_3min = df.resample('5T').agg({...})  # Pour 5 minutes
```

## Support

Pour toute question ou amélioration, ouvrez une issue sur GitHub.

## Licence

Ce projet est open source et disponible pour usage personnel et commercial.

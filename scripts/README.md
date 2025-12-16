# Scripts de Backtest Trading

## candle_continuation_analysis.py

Ce script analyse les continuations de bougies dans la même direction après la bougie de 8h30.

### Prérequis

```bash
pip install -r scripts/requirements.txt
```

### Utilisation

Exécuter depuis la racine du repository :

```bash
python scripts/candle_continuation_analysis.py
```

### Description

Le script analyse les données de 2018 à 2025 pour trois timeframes (1 minute, 5 minutes, 15 minutes) et calcule :

1. **Sélection de la première bougie (8h30)** :
   - Timeframe 1 minute : amplitude >= 20 points
   - Timeframe 5 minutes : amplitude >= 50 points
   - Timeframe 15 minutes : amplitude >= 100 points

2. **Analyse des continuations** :
   - Compte le nombre de bougies consécutives dans la même direction (1 à 5)
   - Sépare les analyses pour les bougies haussières et baissières

3. **Statistiques calculées** :
   - Nombre de fois où N bougies consécutives vont dans la même direction
   - Ratio en pourcentage par rapport au total des premières bougies qualifiées
   - Nombre moyen de points atteints à la clôture de la N-ième bougie

### Format des données

Les fichiers CSV doivent être au format suivant :
- Colonnes séparées par `;`
- Column1 : date (DD/MM/YYYY)
- Column2 : heure (HH:MM:SS)
- Column3 : Open
- Column4 : High
- Column5 : Low
- Column6 : Close
- Column7 : Volume

### Gestion des fichiers

- Les fichiers `.csv.zip` sont automatiquement décompressés
- Le script recherche les fichiers dans le répertoire racine du repository

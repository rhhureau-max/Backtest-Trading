# Backtest-Trading

Ce repository contient des données historiques de trading et un système d'analyse de probabilités de scénarios.

## Contenu

### Données Historiques
Le repository inclut des données de prix historiques pour différents instruments et timeframes (1m, 5m, 15m, 1H, 4H, 1D) de 2018 à 2025.

### Calculateur de Probabilités de Scénarios

Un outil d'analyse qui calcule les probabilités de différents scénarios de trading basés sur:
- L'état du range asiatique (compressé, standard, étendu)
- Le biais de tendance HTF (Daily/4H)
- L'action initiale de la session de Londres

**Utilisation rapide:**
```bash
python3 scenario_probability_calculator.py
```

Pour plus de détails, consultez le [Guide du Calculateur de Probabilités](SCENARIO_PROBABILITY_GUIDE.md).

## Documentation

- [SCENARIO_PROBABILITY_GUIDE.md](SCENARIO_PROBABILITY_GUIDE.md) - Guide complet d'utilisation du calculateur de probabilités
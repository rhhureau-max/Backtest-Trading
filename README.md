# Backtest-Trading

## 📊 Repository de Backtesting de Stratégies de Trading

Ce repository contient des données historiques de marché et des stratégies de trading quantitatives pour le backtesting.

### 📁 Contenu

- **Données Historiques** : Données OHLCV (Open, High, Low, Close, Volume) pour ES et NQ
  - Timeframes: 1m, 5m, 15m, 1H, 4H, 1D, 1W
  - Période: 2018-2025

### 🎯 Stratégies Disponibles

#### 1. Tokyo-London Killzone Strategy (ICT/SMC)

Stratégie avancée basée sur la relation symbiotique entre la session asiatique (Tokyo) et la session européenne (Londres), utilisant les concepts de Smart Money Concepts (SMC) et Inner Circle Trader (ICT).

**Fichiers** :
- `ANALYSE_STRATEGIQUE_TOKYO_LONDON.md` - Analyse stratégique complète et cadre théorique
- `GUIDE_REFERENCE_RAPIDE.md` - Guide de référence rapide avec checklist et mémo
- `tokyo_london_killzone_strategy.py` - Implémentation Python de la stratégie
- `exemples_tokyo_london.py` - Exemples pratiques et démonstrations

**Concepts Clés** :
- Range Asiatique (19:00-23:00 EST) - Phase d'Accumulation
- London Open (01:00-05:00 EST) - Phase de Manipulation (Judas Swing)
- Liquidity Sweep et Market Structure Shift
- Fair Value Gaps et Order Blocks
- Ratio Risque/Récompense asymétrique (1:3+)

**Utilisation** :
```bash
python tokyo_london_killzone_strategy.py
```

La stratégie analyse les données historiques et identifie les setups valides selon les critères ICT/SMC.

**Documentation Complète** : Consultez `ANALYSE_STRATEGIQUE_TOKYO_LONDON.md` pour une analyse approfondie incluant :
- Cadre théorique détaillé
- Algorithmes stratégiques
- Analyse statistique et gestion des risques
- Glossaire de terminologie ICT (IPDA, FVG, MSS, Order Blocks)

### 🚀 Comment Utiliser

1. **Cloner le repository**
```bash
git clone https://github.com/rhhureau-max/Backtest-Trading.git
cd Backtest-Trading
```

2. **Installer les dépendances** (pour les scripts Python)
```bash
pip install pandas numpy
```

3. **Exécuter une stratégie**
```bash
# Pour voir des exemples pratiques et démonstrations
python exemples_tokyo_london.py

# Pour lancer le backtest complet
python tokyo_london_killzone_strategy.py
```

### 📈 Format des Données

Les fichiers CSV utilisent le format suivant :
```
Column1;Column2;Column3;Column4;Column5;Column6;Column7
Date;Time;Open;High;Low;Close;Volume
```

Exemple :
```
01/01/2018;17:00:00;2675.25;2679.25;2674.5;2679.25;10374
```

### ⚠️ Avertissement

Le trading comporte des risques de perte en capital. Les stratégies présentées dans ce repository sont à des fins éducatives et de recherche uniquement. Les performances passées ne garantissent pas les résultats futurs.

- **Ne tradez jamais avec de l'argent que vous ne pouvez pas vous permettre de perdre**
- **Testez toujours une stratégie en mode démo avant de l'utiliser en réel**
- **Comprenez pleinement les risques avant de trader**

### 📚 Ressources

- [Inner Circle Trader (ICT) - YouTube](https://www.youtube.com/@InnerCircleTrader)
- Documentation ICT/SMC incluse dans les fichiers d'analyse stratégique

### 📝 Licence

Ce projet est fourni "tel quel" sans garantie d'aucune sorte. Utilisez à vos propres risques.
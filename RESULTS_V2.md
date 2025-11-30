# PBTrading Silver Bullet & IFVG V2 Backtest Results

## Strategy Updates (V2)

**Nouvelles conditions:**
- **Liquidity Sweep sur 15m** - Recherche de swing high/low dans les 50 dernières bougies
- **FVG sur 5m** - Création d'un FVG puis violation pour devenir IFVG
- **Entrée** - Lorsque le prix clôture en ayant comblé l'IFVG
- **Deux options de SL testées:**
  1. SL sous la bougie qui a comblé le FVG
  2. SL sous l'IFVG

**Instrument:** NQ Futures (Nasdaq 100)  
**Période:** 2025 (293,508 bars @ 1-minute)  
**Fenêtre de Trading:** 9:00 - 10:00 Chicago Time

---

## Test 1: SL sous la bougie qui a comblé l'IFVG

| RR Target | Win Rate (%) | Profit Factor | Max Drawdown (%) | Sharpe Ratio | Total Trades |
|-----------|--------------|---------------|------------------|--------------|--------------|
| 1.0       | 46.71        | 0.57          | 15.59            | -2.31        | 563          |
| 1.5       | 42.94        | 0.62          | 13.02            | -1.87        | 489          |
| 2.0       | 40.09        | 0.67          | 11.36            | -1.52        | 459          |
| **2.5**   | **37.41**    | **0.70**      | **10.01**        | **-1.24**    | 433          |
| 3.0       | 35.51        | 0.65          | 11.30            | -1.46        | 428          |
| 3.5       | 34.20        | 0.60          | 13.38            | -1.67        | 424          |
| 4.0       | 32.36        | 0.61          | 13.13            | -1.51        | 411          |
| 4.5       | 31.00        | 0.57          | 13.52            | -1.60        | 400          |
| 5.0       | 30.13        | 0.55          | 13.90            | -1.62        | 395          |

**Meilleure configuration:** RR 2.5 (Profit Factor: 0.70, Max DD: 10.01%, Sharpe: -1.24)

---

## Test 2: SL sous l'IFVG

| RR Target | Win Rate (%) | Profit Factor | Max Drawdown (%) | Sharpe Ratio | Total Trades |
|-----------|--------------|---------------|------------------|--------------|--------------|
| 1.0       | 44.80        | 0.66          | 13.67            | -1.26        | 433          |
| 1.5       | 39.61        | 0.64          | 14.03            | -1.31        | 409          |
| **2.0**   | **35.85**    | **0.65**      | **12.51**        | **-1.17**    | 371          |
| 2.5       | 31.36        | 0.56          | 14.13            | -1.38        | 354          |
| 3.0       | 28.45        | 0.55          | 14.94            | -1.41        | 348          |
| 3.5       | 26.38        | 0.56          | 14.53            | -1.31        | 345          |
| 4.0       | 26.05        | 0.57          | 13.48            | -1.23        | 334          |
| 4.5       | 25.91        | 0.55          | 13.68            | -1.24        | 328          |
| 5.0       | 25.68        | 0.57          | 13.24            | -1.23        | 331          |

**Meilleure configuration:** RR 2.0 (Profit Factor: 0.65, Max DD: 12.51%, Sharpe: -1.17)

---

## Comparaison des deux approches de SL

| Métrique | SL Fill Candle (RR 2.5) | SL IFVG (RR 2.0) |
|----------|-------------------------|------------------|
| Win Rate | 37.41% | 35.85% |
| Profit Factor | 0.70 | 0.65 |
| Max Drawdown | 10.01% | 12.51% |
| Sharpe Ratio | -1.24 | -1.17 |
| Total Trades | 433 | 371 |

**Conclusion:** Le SL sous la bougie de fill offre un meilleur Profit Factor et un Drawdown plus faible.

---

## Logique d'Entrée V2

### LONG Entry
1. **Sweep de liquidité Sell-Side sur 15m** (mèche sous le fractal low des 50 dernières bougies)
2. **Création d'un FVG baissier sur 5m**
3. **Violation du FVG** (le prix clôture au-dessus → devient IFVG haussier)
4. **Le prix comble l'IFVG** → Entrée LONG

### SHORT Entry
1. **Sweep de liquidité Buy-Side sur 15m** (mèche au-dessus du fractal high des 50 dernières bougies)
2. **Création d'un FVG haussier sur 5m**
3. **Violation du FVG** (le prix clôture en dessous → devient IFVG baissier)
4. **Le prix comble l'IFVG** → Entrée SHORT

### Gestion du Risque
- **Stop Loss Option 1:** Sous la bougie qui a comblé l'IFVG
- **Stop Loss Option 2:** Sous la zone IFVG
- **Take Profit:** Multiple RR (1 à 5)
- **Break-Even:** SL déplacé à l'entrée à 1R de profit
- **Sortie forcée:** 15:00 CT

---

*Généré le 2025-11-30 | Données: NQ Futures 2025*

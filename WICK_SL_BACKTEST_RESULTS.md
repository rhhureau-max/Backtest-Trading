# Wick-Based SL Backtest Results

## Configuration

- **Risk per Trade**: $100
- **Analysis Date**: 2025-11-28 16:46:28

## Stratégie de SL (Wick-Based)

Cette stratégie utilise la mèche de la bougie 08:30 (candle n) pour calculer le Stop Loss:

- **Position LONG (FVG haussier)**: SL = Low de la bougie 08:30 - 1 point
- **Position SHORT (FVG baissier)**: SL = High de la bougie 08:30 + 1 point

### Différence avec la stratégie précédente

| Aspect | Stratégie Précédente (Body) | Nouvelle Stratégie (Wick) |
|--------|----------------------------|---------------------------|
| **Base du SL** | Corps de la bougie 08:45 | Mèche de la bougie 08:30 |
| **Calcul LONG** | Entry - (Body × SL%) | Low 08:30 - 1 point |
| **Calcul SHORT** | Entry + (Body × SL%) | High 08:30 + 1 point |

---

## P&L Calculation Method

- **Win**: Gain of $100 × RR (e.g., RR 2 = gain of $200)
- **Loss**: Loss of $100
- **Total P&L**: (Wins × $100 × RR) - (Losses × $100)
- **Profit Factor**: Total Gains / Total Losses
- **Average Trade**: Total P&L / Number of Trades

---

## Résultats Wick-Based SL

| RR | Trades | Wins | Losses | Win Rate (%) | P&L Net ($) | Profit Factor | Avg Trade ($) |
|-----|--------|------|--------|--------------|-------------|---------------|---------------|
| 1 | 756 | 412 | 344 | 54.50% | +6,800 | 1.20 | +8.99 |
| 1.5 | 663 | 275 | 388 | 41.48% | +2,450 | 1.06 | +3.70 |
| 2 | 595 | 191 | 404 | 32.10% | -2,200 | 0.95 | -3.70 |
| 2.5 | 543 | 134 | 409 | 24.68% | -7,400 | 0.82 | -13.63 |
| 3 | 505 | 89 | 416 | 17.62% | -14,900 | 0.64 | -29.50 |
| 3.5 | 481 | 61 | 420 | 12.68% | -20,650 | 0.51 | -42.93 |
| 4 | 469 | 48 | 421 | 10.23% | -22,900 | 0.46 | -48.83 |
| 4.5 | 457 | 34 | 423 | 7.44% | -27,000 | 0.36 | -59.08 |
| 5 | 450 | 27 | 423 | 6.00% | -28,800 | 0.32 | -64.00 |

---

## Comparaison avec la Stratégie Précédente (Body 50% SL)

| RR | Wick SL P&L | Body SL P&L | Différence | Wick Win Rate | Body Win Rate |
|-----|-------------|-------------|------------|---------------|---------------|
| 1 | +6,800 | +9,600 | -2,800 | 54.50% | 55.39% |
| 1.5 | +2,450 | +25,850 | -23,400 | 41.48% | 51.63% |
| 2 | -2,200 | +40,100 | -42,300 | 32.10% | 48.37% |
| 2.5 | -7,400 | +50,950 | -58,350 | 24.68% | 44.98% |
| 3 | -14,900 | +65,000 | -79,900 | 17.62% | 43.34% |
| 3.5 | -20,650 | +75,400 | -96,050 | 12.68% | 41.18% |
| 4 | -22,900 | +85,100 | -108,000 | 10.23% | 39.25% |
| 4.5 | -27,000 | +91,500 | -118,500 | 7.44% | 37.13% |
| 5 | -28,800 | +102,000 | -130,800 | 6.00% | 36.07% |

---

## Résumé des Meilleures Combinaisons (Wick SL)

### 🏆 Meilleure Combinaison (P&L Net le plus élevé)

| Paramètre | Valeur |
|-----------|--------|
| **RR** | 1 |
| **Trades** | 756 |
| **Wins** | 412 |
| **Losses** | 344 |
| **Win Rate** | 54.50% |
| **P&L Net** | $+6,800 |
| **Profit Factor** | 1.20 |
| **Avg Trade** | $+8.99 |

### 📊 Meilleur Profit Factor

| Paramètre | Valeur |
|-----------|--------|
| **RR** | 1 |
| **Trades** | 756 |
| **Wins** | 412 |
| **Losses** | 344 |
| **Win Rate** | 54.50% |
| **P&L Net** | $+6,800 |
| **Profit Factor** | 1.20 |
| **Avg Trade** | $+8.99 |

### 💰 Meilleur Average Trade

| Paramètre | Valeur |
|-----------|--------|
| **RR** | 1 |
| **Trades** | 756 |
| **Wins** | 412 |
| **Losses** | 344 |
| **Win Rate** | 54.50% |
| **P&L Net** | $+6,800 |
| **Profit Factor** | 1.20 |
| **Avg Trade** | $+8.99 |

---

## Notes

- Les résultats sont basés sur un risque fixe de $100 par trade
- Les trades sans sortie (SL ou TP non atteints dans la journée) sont exclus des calculs
- Le Profit Factor "∞" indique qu'il n'y a eu aucune perte
- La comparaison est faite avec la stratégie Body SL à 50% (meilleur performer de la stratégie précédente)

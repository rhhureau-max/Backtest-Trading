# Opening Range Breakout (ORB) Backtest Report
## Candle-Based Stop Loss with R:R Analysis (1:1 to 1:5)

---

## Strategy Overview

This report presents the backtesting results of an Opening Range Breakout (ORB) strategy
with **candle-based stop loss** placement, testing multiple R:R targets from 1:1 to 1:5.

### Strategy Rules
- **Opening Range**: High/Low of 08:30-08:45 CT (14:30-14:45 UTC)
- **Long Signal**: 5-minute candle closes above the range high
- **Short Signal**: 5-minute candle closes below the range low
- **Stop Loss**: Under the LOW of breakout candle (Long) / Above the HIGH (Short)
- **Take Profit**: Variable R:R ratios tested (1:1, 1:2, 1:3, 1:4, 1:5)
- **Filter**: Skip days with opening range < 20 points

---

## R:R Comparison Summary

| R:R Target | Win Rate | Profit Factor | Total P&L (pts) | Max Drawdown (pts) | Avg P&L |
|------------|----------|---------------|-----------------|--------------------|---------| 
| **1:1** | 48.10% | 1.20 | 3291.58 | 1042.00 | 2.40 |
| **1:2** | 7.43% | 1.35 | 5621.23 | 795.03 | 4.10 |
| **1:3** | 1.90% | 1.37 | 6006.93 | 740.76 | 4.38 |
| **1:4** | 0.73% | 1.38 | 6161.65 | 722.50 | 4.49 |
| **1:5** | 0.44% | 1.38 | 6223.05 | 704.23 | 4.54 |

---

## Detailed Results: R:R 1:1

| Metric | Value |
|--------|-------|
| Total Trades | 1372 |
| Winning Trades | 660 |
| Losing Trades | 712 |
| **Win Rate** | **48.10%** |
| **Profit Factor** | **1.20** |
| Total P&L (points) | 3291.58 |
| Average P&L per Trade | 2.40 |
| **Max Drawdown (points)** | **1042.00** |
| Long Trades | 721 (47.9% win) |
| Short Trades | 651 (48.4% win) |

### Exit Distribution (1:1 Target)

| Exit Type | Count | Percentage |
|-----------|-------|------------|
| EOD | 138 | 10.1% |
| SL | 574 | 41.8% |
| TP1 | 660 | 48.1% |

---

## Detailed Results: R:R 1:2

| Metric | Value |
|--------|-------|
| Total Trades | 1372 |
| Winning Trades | 102 |
| Losing Trades | 1270 |
| **Win Rate** | **7.43%** |
| **Profit Factor** | **1.35** |
| Total P&L (points) | 5621.23 |
| Average P&L per Trade | 4.10 |
| **Max Drawdown (points)** | **795.03** |
| Long Trades | 721 (7.9% win) |
| Short Trades | 651 (6.9% win) |

### Exit Distribution (1:2 Target)

| Exit Type | Count | Percentage |
|-----------|-------|------------|
| EOD | 696 | 50.7% |
| SL | 574 | 41.8% |
| TP2 | 102 | 7.4% |

---

## Detailed Results: R:R 1:3

| Metric | Value |
|--------|-------|
| Total Trades | 1372 |
| Winning Trades | 26 |
| Losing Trades | 1346 |
| **Win Rate** | **1.90%** |
| **Profit Factor** | **1.37** |
| Total P&L (points) | 6006.93 |
| Average P&L per Trade | 4.38 |
| **Max Drawdown (points)** | **740.76** |
| Long Trades | 721 (1.8% win) |
| Short Trades | 651 (2.0% win) |

### Exit Distribution (1:3 Target)

| Exit Type | Count | Percentage |
|-----------|-------|------------|
| EOD | 772 | 56.3% |
| SL | 574 | 41.8% |
| TP3 | 26 | 1.9% |

---

## Detailed Results: R:R 1:4

| Metric | Value |
|--------|-------|
| Total Trades | 1372 |
| Winning Trades | 10 |
| Losing Trades | 1362 |
| **Win Rate** | **0.73%** |
| **Profit Factor** | **1.38** |
| Total P&L (points) | 6161.65 |
| Average P&L per Trade | 4.49 |
| **Max Drawdown (points)** | **722.50** |
| Long Trades | 721 (0.4% win) |
| Short Trades | 651 (1.1% win) |

### Exit Distribution (1:4 Target)

| Exit Type | Count | Percentage |
|-----------|-------|------------|
| EOD | 788 | 57.4% |
| SL | 574 | 41.8% |
| TP4 | 10 | 0.7% |

---

## Detailed Results: R:R 1:5

| Metric | Value |
|--------|-------|
| Total Trades | 1372 |
| Winning Trades | 6 |
| Losing Trades | 1366 |
| **Win Rate** | **0.44%** |
| **Profit Factor** | **1.38** |
| Total P&L (points) | 6223.05 |
| Average P&L per Trade | 4.54 |
| **Max Drawdown (points)** | **704.23** |
| Long Trades | 721 (0.3% win) |
| Short Trades | 651 (0.6% win) |

### Exit Distribution (1:5 Target)

| Exit Type | Count | Percentage |
|-----------|-------|------------|
| EOD | 792 | 57.7% |
| SL | 574 | 41.8% |
| TP5 | 6 | 0.4% |

---

## Annual Performance Breakdown

| Year | Trades | Long | Short | SL | TP1 | TP2 | TP3 | TP4 | TP5 | EOD |
|------|--------|------|-------|----|----|----|----|----|----|-----|
| 2018 | 89 | 44 | 45 | 35 | 41 | 2 | 1 | 0 | 1 | 9 |
| 2019 | 55 | 25 | 30 | 22 | 26 | 2 | 1 | 1 | 0 | 3 |
| 2020 | 200 | 111 | 89 | 79 | 95 | 12 | 1 | 0 | 0 | 13 |
| 2021 | 198 | 89 | 109 | 95 | 69 | 13 | 1 | 0 | 2 | 18 |
| 2022 | 235 | 120 | 115 | 78 | 107 | 9 | 2 | 2 | 0 | 37 |
| 2023 | 194 | 108 | 86 | 80 | 76 | 16 | 1 | 1 | 0 | 20 |
| 2024 | 211 | 112 | 99 | 103 | 67 | 10 | 4 | 0 | 2 | 25 |
| 2025 | 190 | 112 | 78 | 82 | 77 | 12 | 5 | 0 | 1 | 13 |

---

## Risk Analysis

| Metric | Value |
|--------|-------|
| Average Range Size | 46.33 points |
| Average Risk (SL Distance) | 29.30 points |

### Key Insights

- **Best P&L Performance**: R:R 1:5 with 6223.05 points
- **Best Profit Factor**: R:R 1:5 with 1.38
- **Highest Win Rate**: R:R 1:1 typically has the highest win rate as targets are closer

---

## Notes

- **Stop Loss Placement**: Under the LOW of the breakout 5-minute candle (for longs)
- **Risk Calculation**: Entry price minus Stop Loss price = Risk in points
- All P&L values are in NQ Futures points (1 point = $20 per contract)
- Time zone: Data is in UTC, strategy uses New York (CT) session times
- Opening Range: 08:30-08:45 CT = 14:30-14:45 UTC
- Regular session end: 15:00 CT = 21:00 UTC

---

*Report generated on: 2025-11-27 18:30:06*
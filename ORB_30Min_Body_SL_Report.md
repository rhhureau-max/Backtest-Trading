# Opening Range Breakout (ORB) Backtest Report
## 30-Minute Opening Range with Body-Based Stop Loss
## R:R Analysis (1:1 to 1:5)

---

## Strategy Overview

This report presents the backtesting results of an Opening Range Breakout (ORB) strategy
with a **30-minute opening range** and **body-based stop loss** placement.

### Strategy Rules
- **Opening Range**: High/Low of **08:30-09:00 CT** (14:30-15:00 UTC) - **30 minutes**
- **Entry Signal**: After 09:00 CT, first 5-min candle that closes above/below the range
- **Long Signal**: 5-minute candle closes above the range high
- **Short Signal**: 5-minute candle closes below the range low
- **Stop Loss**: Under the **BODY** of breakout candle (not the wick)
  - Long: min(Open, Close) of breakout candle
  - Short: max(Open, Close) of breakout candle
- **Take Profit**: Variable R:R ratios tested (1:1, 1:2, 1:3, 1:4, 1:5)
- **Filter**: Skip days with opening range < 20 points

---

## R:R Comparison Summary

| R:R Target | Win Rate | Profit Factor | Total P&L (pts) | Max Drawdown (pts) | Avg P&L |
|------------|----------|---------------|-----------------|--------------------|---------| 
| **1:1** | 47.21% | 1.16 | 1596.29 | 536.77 | 1.14 |
| **1:2** | 8.44% | 1.25 | 2490.20 | 481.08 | 1.78 |
| **1:3** | 3.93% | 1.28 | 2877.40 | 457.43 | 2.06 |
| **1:4** | 1.72% | 1.30 | 3036.25 | 438.09 | 2.17 |
| **1:5** | 1.00% | 1.30 | 3095.18 | 431.49 | 2.21 |

---

## Detailed Results: R:R 1:1

| Metric | Value |
|--------|-------|
| Total Trades | 1398 |
| Winning Trades | 660 |
| Losing Trades | 738 |
| **Win Rate** | **47.21%** |
| **Profit Factor** | **1.16** |
| Total P&L (points) | 1596.29 |
| Average P&L per Trade | 1.14 |
| **Max Drawdown (points)** | **536.77** |
| Long Trades | 769 (48.0% win) |
| Short Trades | 629 (46.3% win) |

### Exit Distribution (1:1 Target)

| Exit Type | Count | Percentage |
|-----------|-------|------------|
| EOD | 122 | 8.7% |
| SL | 616 | 44.1% |
| TP1 | 660 | 47.2% |

---

## Detailed Results: R:R 1:2

| Metric | Value |
|--------|-------|
| Total Trades | 1398 |
| Winning Trades | 118 |
| Losing Trades | 1280 |
| **Win Rate** | **8.44%** |
| **Profit Factor** | **1.25** |
| Total P&L (points) | 2490.20 |
| Average P&L per Trade | 1.78 |
| **Max Drawdown (points)** | **481.08** |
| Long Trades | 769 (9.4% win) |
| Short Trades | 629 (7.3% win) |

### Exit Distribution (1:2 Target)

| Exit Type | Count | Percentage |
|-----------|-------|------------|
| EOD | 664 | 47.5% |
| SL | 616 | 44.1% |
| TP2 | 118 | 8.4% |

---

## Detailed Results: R:R 1:3

| Metric | Value |
|--------|-------|
| Total Trades | 1398 |
| Winning Trades | 55 |
| Losing Trades | 1343 |
| **Win Rate** | **3.93%** |
| **Profit Factor** | **1.28** |
| Total P&L (points) | 2877.40 |
| Average P&L per Trade | 2.06 |
| **Max Drawdown (points)** | **457.43** |
| Long Trades | 769 (4.4% win) |
| Short Trades | 629 (3.3% win) |

### Exit Distribution (1:3 Target)

| Exit Type | Count | Percentage |
|-----------|-------|------------|
| EOD | 727 | 52.0% |
| SL | 616 | 44.1% |
| TP3 | 55 | 3.9% |

---

## Detailed Results: R:R 1:4

| Metric | Value |
|--------|-------|
| Total Trades | 1398 |
| Winning Trades | 24 |
| Losing Trades | 1374 |
| **Win Rate** | **1.72%** |
| **Profit Factor** | **1.30** |
| Total P&L (points) | 3036.25 |
| Average P&L per Trade | 2.17 |
| **Max Drawdown (points)** | **438.09** |
| Long Trades | 769 (2.0% win) |
| Short Trades | 629 (1.4% win) |

### Exit Distribution (1:4 Target)

| Exit Type | Count | Percentage |
|-----------|-------|------------|
| EOD | 758 | 54.2% |
| SL | 616 | 44.1% |
| TP4 | 24 | 1.7% |

---

## Detailed Results: R:R 1:5

| Metric | Value |
|--------|-------|
| Total Trades | 1398 |
| Winning Trades | 14 |
| Losing Trades | 1384 |
| **Win Rate** | **1.00%** |
| **Profit Factor** | **1.30** |
| Total P&L (points) | 3095.18 |
| Average P&L per Trade | 2.21 |
| **Max Drawdown (points)** | **431.49** |
| Long Trades | 769 (1.0% win) |
| Short Trades | 629 (1.0% win) |

### Exit Distribution (1:5 Target)

| Exit Type | Count | Percentage |
|-----------|-------|------------|
| EOD | 768 | 54.9% |
| SL | 616 | 44.1% |
| TP5 | 14 | 1.0% |

---

## Annual Performance Breakdown

| Year | Trades | Long | Short | SL | TP1 | TP2 | TP3 | TP4 | TP5 | EOD |
|------|--------|------|-------|----|----|----|----|----|----|-----|
| 2018 | 124 | 73 | 51 | 55 | 41 | 11 | 2 | 1 | 2 | 12 |
| 2019 | 130 | 77 | 53 | 52 | 51 | 7 | 2 | 2 | 2 | 14 |
| 2020 | 193 | 112 | 81 | 86 | 71 | 10 | 8 | 2 | 2 | 14 |
| 2021 | 194 | 105 | 89 | 89 | 83 | 6 | 3 | 0 | 1 | 12 |
| 2022 | 200 | 106 | 94 | 81 | 86 | 6 | 3 | 2 | 2 | 20 |
| 2023 | 178 | 100 | 78 | 87 | 58 | 12 | 4 | 0 | 2 | 15 |
| 2024 | 195 | 95 | 100 | 86 | 81 | 7 | 3 | 2 | 1 | 15 |
| 2025 | 184 | 101 | 83 | 80 | 71 | 4 | 6 | 1 | 2 | 20 |

---

## Risk Analysis

| Metric | Value |
|--------|-------|
| Average Range Size (30 min) | 65.80 points |
| Average Risk (SL Distance) | 18.15 points |

### Key Insights

- **Best P&L Performance**: R:R 1:5 with 3095.18 points
- **Best Profit Factor**: R:R 1:5 with 1.30
- **Highest Win Rate**: R:R 1:1 with 47.21%

### Strategy Differences from Previous Versions

| Parameter | 15-min Range + Candle Low SL | 30-min Range + Body SL |
|-----------|------------------------------|------------------------|
| Opening Range | 08:30-08:45 (15 min) | **08:30-09:00 (30 min)** |
| Breakout After | 08:45 | **09:00** |
| Stop Loss Placement | Under candle LOW | **Under candle BODY** |
| Risk Size | Larger (full wick) | Smaller (body only) |

---

## Notes

- **Opening Range**: 30-minute range from 08:30-09:00 CT (14:30-15:00 UTC)
- **Stop Loss Placement**: Under the BODY of the breakout candle
  - For LONG: Stop = min(Open, Close)
  - For SHORT: Stop = max(Open, Close)
- **Risk Calculation**: Entry price minus Body Bottom (for longs)
- All P&L values are in NQ Futures points (1 point = $20 per contract)
- Time zone: Data is in UTC, strategy uses New York (CT) session times
- Regular session end: 15:00 CT = 21:00 UTC

---

*Report generated on: 2025-11-27 18:28:36*
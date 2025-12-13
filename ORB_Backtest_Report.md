# Opening Range Breakout (ORB) Backtest Report

## Strategy Overview

This report presents the backtesting results of an Opening Range Breakout (ORB) strategy
applied to NQ Futures 5-minute data from 2018-2025.

### Strategy Rules
- **Opening Range**: High/Low of 08:30-08:45 CT (14:30-14:45 UTC)
- **Long Signal**: 5-minute candle closes above the range high
- **Short Signal**: 5-minute candle closes below the range low
- **Stop Loss**: 50% of range OR opposite end if range < 40 points
- **Take Profit**: TP1 = 1:1 R/R, TP2 = 1:2 R/R
- **Filter**: Skip days with range < 20 points

---

## Performance Summary

| Metric | Value |
|--------|-------|
| Total Trades | 1372 |
| Winning Trades | 714 |
| Losing Trades | 654 |
| **Win Rate** | **52.04%** |
| **Profit Factor** | **1.24** |
| Total P&L (points) | 5294.57 |
| Average P&L per Trade | 3.86 |
| **Max Drawdown (points)** | **822.71** |
| Average Range Size | 46.33 |

---

## Long vs Short Distribution

| Direction | Trades | Win Rate |
|-----------|--------|----------|
| Long | 721 | 54.51% |
| Short | 651 | 49.31% |

---

## Exit Types

| Exit Type | Count | Percentage |
|-----------|-------|------------|
| Stop Loss | 456 | 33.2% |
| Take Profit 1 (1:1) | 507 | 37.0% |
| Take Profit 2 (1:2) | 24 | 1.7% |
| End of Session | 385 | 28.1% |

---

## Annual Performance (2018-2025)

| Year | Trades | Wins | Win Rate | P&L (points) | Long | Short |
|------|--------|------|----------|--------------|------|-------|
| 2018 | 89 | 43 | 48.3% | 301.87 | 44 | 45 |
| 2019 | 55 | 29 | 52.7% | 235.29 | 25 | 30 |
| 2020 | 200 | 106 | 53.0% | 1594.91 | 111 | 89 |
| 2021 | 198 | 100 | 50.5% | 169.90 | 89 | 109 |
| 2022 | 235 | 133 | 56.6% | 1870.30 | 120 | 115 |
| 2023 | 194 | 99 | 51.0% | 210.92 | 108 | 86 |
| 2024 | 211 | 99 | 46.9% | -301.96 | 112 | 99 |
| 2025 | 190 | 105 | 55.3% | 1213.34 | 112 | 78 |

---

## Notes

- All P&L values are in NQ Futures points (1 point = $20 per contract)
- Time zone: Data is in UTC, strategy uses New York (CT) session times
- Opening Range: 08:30-08:45 CT = 14:30-14:45 UTC
- Regular session end: 15:00 CT = 21:00 UTC

---

*Report generated on: 2025-11-27 12:55:24*
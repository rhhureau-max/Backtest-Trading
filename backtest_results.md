# Backtest Results

*Generated from backtest of Liquidity Sweep strategy*

---

## Summary Statistics

| Metric | Value |
|--------|-------|
| **Total Trades** | 2767 |
| **Winning Trades** | 1045 |
| **Losing Trades** | 1722 |
| **Win Rate** | 37.77% |
| **Profit Factor** | 0.61 |
| **Net Profit (R)** | -677.00R |
| **Maximum Drawdown** | 681.00R (17025.00%) |
| **Average Win (R:R)** | 1.00 |
| **Average Loss (R:R)** | 1.00 |
| **Average Realized R:R** | -0.24 |

## Statistics by Year

| Year | Trades | Wins | Losses | Win Rate | Net Profit (R) | Profit Factor | Avg R:R |
|------|--------|------|--------|----------|----------------|---------------|---------|
| 2018 | 398 | 161 | 237 | 40.5% | -76.00R | 0.68 | -0.19 |
| 2019 | 379 | 140 | 239 | 36.9% | -99.00R | 0.59 | -0.26 |
| 2020 | 35 | 14 | 21 | 40.0% | -7.00R | 0.67 | -0.20 |
| 2021 | 399 | 154 | 245 | 38.6% | -91.00R | 0.63 | -0.23 |
| 2022 | 422 | 148 | 274 | 35.1% | -126.00R | 0.54 | -0.30 |
| 2023 | 392 | 161 | 231 | 41.1% | -70.00R | 0.70 | -0.18 |
| 2024 | 392 | 139 | 253 | 35.5% | -114.00R | 0.55 | -0.29 |
| 2025 | 350 | 128 | 222 | 36.6% | -94.00R | 0.58 | -0.27 |

## Statistics by Session

| Session | Trades | Wins | Losses | Win Rate | Net Profit (R) | Profit Factor | Avg R:R |
|---------|--------|------|--------|----------|----------------|---------------|---------|
| Session 1 | 1337 | 523 | 814 | 39.1% | -291.00R | 0.64 | -0.22 |
| Session 2 | 1430 | 522 | 908 | 36.5% | -386.00R | 0.57 | -0.27 |

## Strategy Description

### Trading Sessions (UTC)
- **Session 1**: 02:00 to 05:00
- **Session 2**: 08:30 to 11:00

### HTF Context
- Liquidity sweep on old high/low (detected using fractals)

### LTF Entry (M5)
1. New FVG forms in M5 (displacement)
2. Price retraces to fill M5 FVG
3. Reversal candle confirms entry

### Trade Management
- Entry: At close of reversal candle
- Stop Loss: Below/above swing created during FVG rejection
- Take Profit: 1:1 Risk/Reward ratio

---
*Note: All profit/loss values are expressed in R-multiples (risk units)*
# Backtest Results

*Generated from backtest of FVG + Liquidity Sweep strategy*

---

## Summary Statistics

| Metric | Value |
|--------|-------|
| **Total Trades** | 3731 |
| **Winning Trades** | 1009 |
| **Losing Trades** | 2722 |
| **Win Rate** | 27.04% |
| **Profit Factor** | 0.74 |
| **Net Profit (R)** | -704.00R |
| **Maximum Drawdown** | 706.00R (0.00%) |
| **Average Win (R:R)** | 2.00 |
| **Average Loss (R:R)** | 1.00 |
| **Average Realized R:R** | -0.19 |

## Statistics by Year

| Year | Trades | Wins | Losses | Win Rate | Net Profit (R) | Profit Factor | Avg R:R |
|------|--------|------|--------|----------|----------------|---------------|---------|
| 2018 | 488 | 115 | 373 | 23.6% | -143.00R | 0.62 | -0.29 |
| 2019 | 459 | 119 | 340 | 25.9% | -102.00R | 0.70 | -0.22 |
| 2020 | 481 | 131 | 350 | 27.2% | -88.00R | 0.75 | -0.18 |
| 2021 | 476 | 127 | 349 | 26.7% | -95.00R | 0.73 | -0.20 |
| 2022 | 493 | 152 | 341 | 30.8% | -37.00R | 0.89 | -0.08 |
| 2023 | 468 | 135 | 333 | 28.8% | -63.00R | 0.81 | -0.13 |
| 2024 | 464 | 124 | 340 | 26.7% | -92.00R | 0.73 | -0.20 |
| 2025 | 402 | 106 | 296 | 26.4% | -84.00R | 0.72 | -0.21 |

## Statistics by Session

| Session | Trades | Wins | Losses | Win Rate | Net Profit (R) | Profit Factor | Avg R:R |
|---------|--------|------|--------|----------|----------------|---------------|---------|
| Session 1 | 1849 | 500 | 1349 | 27.0% | -349.00R | 0.74 | -0.19 |
| Session 2 | 1882 | 509 | 1373 | 27.0% | -355.00R | 0.74 | -0.19 |

## Strategy Description

### Trading Sessions (UTC)
- **Session 1**: 02:00 to 05:00
- **Session 2**: 08:30 to 11:00

### HTF Context
- FVG (Fair Value Gap) detected in H1 or M15
- OR Liquidity sweep on old high/low

### LTF Entry (M5)
1. New FVG forms in M5 (displacement)
2. Price retraces to fill M5 FVG
3. Reversal candle confirms entry

### Trade Management
- Entry: At close of reversal candle
- Stop Loss: Below/above swing created during FVG rejection
- Take Profit: 1:2 Risk/Reward ratio

---
*Note: All profit/loss values are expressed in R-multiples (risk units)*
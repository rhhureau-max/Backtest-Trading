# Judas Swing + Inversion FVG - Multi-Timeframe Strategy Analysis

## Executive Summary

This report presents the results of an advanced backtesting strategy combining:
- Multi-timeframe Fair Value Gap (FVG) analysis (5m and 1m)
- Hierarchical timeframe priority (5m > 1m)
- A/B testing of Stop Loss placement (Body vs Wick)
- Multiple Take Profit levels (1R, 1.5R, 2R)

## Strategy Rules

### 1. Tokyo Session Identification
- Tokyo Session: 19:00 - 00:00
- Record High, Low, and 50% Equilibrium

### 2. Manipulation Detection
- Manipulation Zone: 02:00 - 02:30 (London session)
- Condition: Price breaks Tokyo High (SHORT) or Low (LONG)

### 3. Multi-Timeframe FVG Detection
**Priority Rule:**
- **Case A (Priority)**: If 5m FVG exists → Use 5m FVG for entry
- **Case B (Secondary)**: If NO 5m FVG → Use 1m FVG for entry

### 4. Entry Trigger
- Wait for price to reverse and fill the FVG
- Entry: Close of candle that closes beyond FVG

### 5. Stop Loss A/B Testing
**Two SL options tested:**
- **SL-Body**: Placed beyond body of manipulation candle
- **SL-Wick**: Placed at absolute wick extreme of manipulation candle

### 6. Take Profit Levels
- **TP 1R**: Risk/Reward ratio of 1:1
- **TP 1.5R**: Risk/Reward ratio of 1:1.5
- **TP 2R**: Risk/Reward ratio of 1:2

## Data Analysis Period

- **Start Date**: 2018-01-01
- **End Date**: 2025-11-09
- **Total Days Analyzed**: 635
- **Total Trade Setups**: 634 (tested with 6 configurations each)

## Results Summary

### Comparison Table

| SL_Type   | TF_Used   | WR_1R_%   | WR_1.5R_%   | WR_2R_%   |   Trades | Expectancy_1R   |
|:----------|:----------|:----------|:------------|:----------|---------:|:----------------|
| SL-Body   | 1m        | 41.9%     | 38.7%       | 35.5%     |       62 | -0.161R         |
| SL-Body   | 5m        | 48.7%     | 39.2%       | 34.3%     |      571 | -0.026R         |
| SL-Wick   | 1m        | 48.4%     | 43.5%       | 40.3%     |       62 | -0.032R         |
| SL-Wick   | 5m        | 52.3%     | 43.6%       | 35.9%     |      570 | +0.045R         |

### Detailed Statistics

| SL_Type   | Timeframe   | TP_Level   |   Total_Trades |   Wins |   Losses |   Win_Rate_% |   Avg_Win_R |   Avg_Loss_R |   Expectancy_R |
|:----------|:------------|:-----------|---------------:|-------:|---------:|-------------:|------------:|-------------:|---------------:|
| SL-Body   | 1m          | 1.5R       |             62 |     24 |       38 |      38.7097 |         1.5 |           -1 |     -0.0322581 |
| SL-Body   | 1m          | 1R         |             62 |     26 |       36 |      41.9355 |         1   |           -1 |     -0.16129   |
| SL-Body   | 1m          | 2R         |             62 |     22 |       40 |      35.4839 |         2   |           -1 |      0.0645161 |
| SL-Body   | 5m          | 1.5R       |            571 |    224 |      347 |      39.2294 |         1.5 |           -1 |     -0.0192644 |
| SL-Body   | 5m          | 1R         |            571 |    278 |      293 |      48.6865 |         1   |           -1 |     -0.0262697 |
| SL-Body   | 5m          | 2R         |            571 |    196 |      375 |      34.3257 |         2   |           -1 |      0.0297723 |
| SL-Wick   | 1m          | 1.5R       |             62 |     27 |       35 |      43.5484 |         1.5 |           -1 |      0.0887097 |
| SL-Wick   | 1m          | 1R         |             62 |     30 |       32 |      48.3871 |         1   |           -1 |     -0.0322581 |
| SL-Wick   | 1m          | 2R         |             62 |     25 |       37 |      40.3226 |         2   |           -1 |      0.209677  |
| SL-Wick   | 5m          | 1.5R       |            571 |    249 |      322 |      43.6077 |         1.5 |           -1 |      0.0901926 |
| SL-Wick   | 5m          | 1R         |            572 |    299 |      273 |      52.2727 |         1   |           -1 |      0.0454545 |
| SL-Wick   | 5m          | 2R         |            568 |    204 |      364 |      35.9155 |         2   |           -1 |      0.0774648 |

## Key Findings

### Best Configuration
- **SL Type**: SL-Wick
- **Timeframe**: 1m
- **TP Level**: 2R
- **Win Rate**: 40.3%
- **Expectancy**: +0.210R
- **Total Trades**: 62

### Timeframe Usage
- **1m**: 124 trades (3.3%)
- **5m**: 1141 trades (30.1%)

### SL Type Performance (1R Target)
- **SL-Body**: WR=45.3%, Exp=-0.094R
- **SL-Wick**: WR=50.3%, Exp=+0.007R

## Recommendations

Based on the backtest results, the optimal configuration is:

1. **Use SL-Wick** for stop loss placement
2. **Prioritize 1m timeframe** for FVG detection
3. **Target 2R** for best risk/reward balance

This configuration provides:
- Win Rate: 40.3%
- Positive Expectancy: +0.210R per trade

## Notes and Limitations

- This backtest uses historical data and past performance does not guarantee future results
- Slippage, commissions, and spreads are not included in this analysis
- Market conditions may vary significantly from the backtest period
- The strategy assumes perfect execution at specified price levels

## Methodology

1. Load 5m and 1m historical data (2018-2025)
2. For each trading day:
   - Identify Tokyo session High/Low
   - Check for manipulation in 02:00-02:30 window
   - Detect FVGs on both 5m and 1m timeframes
   - Apply priority rule (5m > 1m)
   - Wait for FVG inversion signal
   - Test both SL options with 3 TP levels
3. Simulate each trade to determine outcome (WIN/LOSS)
4. Calculate statistics and generate comparison tables

---

*Report generated on: 2025-12-03 22:59:54*

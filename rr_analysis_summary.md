# Risk/Reward Analysis - Executive Summary

**Analysis Date:** 2025-12-02 23:17:31

## Overview

This analysis evaluates the performance of identified trading setups across different Stop Loss (SL) and Take Profit (TP) configurations.

### Tested Configurations

**Stop Loss Placements** (% of 8:30 candle body retracement):
- **100%**: SL at opposite end of body (full body)
- **75%**: SL at 75% of body (long retracement)
- **50%**: SL at middle of body
- **25%**: SL at 25% of body (close SL)

**Risk/Reward Ratios:** 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0

## Key Findings

### Best Overall Configuration

- **Timeframe:** 15m
- **Stop Loss:** 100% body retracement
- **Risk/Reward:** 1.5
- **Win Rate:** 45.65%
- **Total PnL:** 2037.79 risk units
- **Total Trades:** 184

### Highest Win Rate Configuration (min 10 trades)

- **Timeframe:** 15m
- **Stop Loss:** 75% body retracement
- **Risk/Reward:** 1.0
- **Win Rate:** 54.35%
- **Total PnL:** 1208.17 risk units
- **Total Trades:** 184

## Performance by Timeframe

### 1M Timeframe

- **Unique Setups:** 279
- **Total Simulations:** 10044
- **Best Config:** SL 25%, RR 1.0 (Win Rate: 44.80%, Total PnL: -376.46)

### 5M Timeframe

- **Unique Setups:** 232
- **Total Simulations:** 8352
- **Best Config:** SL 25%, RR 3.0 (Win Rate: 22.41%, Total PnL: -191.54)

### 15M Timeframe

- **Unique Setups:** 184
- **Total Simulations:** 6624
- **Best Config:** SL 100%, RR 1.5 (Win Rate: 45.65%, Total PnL: 2037.79)

## Top 10 Configurations by Total PnL

| Rank | Timeframe | SL % | RR | Win Rate | Total PnL | Trades |
|------|-----------|------|-----|----------|-----------|--------|
| 1 | 15m | 100 | 1.5 | 45.65% | 2037.79 | 184 |
| 2 | 15m | 50 | 2.5 | 31.52% | 1960.88 | 184 |
| 3 | 15m | 75 | 2.0 | 38.04% | 1960.60 | 184 |
| 4 | 15m | 100 | 2.0 | 38.04% | 1939.38 | 184 |
| 5 | 15m | 75 | 1.5 | 44.57% | 1624.12 | 184 |
| 6 | 15m | 75 | 2.5 | 33.15% | 1245.11 | 184 |
| 7 | 15m | 75 | 1.0 | 54.35% | 1208.17 | 184 |
| 8 | 15m | 25 | 2.0 | 33.15% | 1167.95 | 184 |
| 9 | 15m | 25 | 2.5 | 28.80% | 1157.80 | 184 |
| 10 | 15m | 25 | 1.5 | 40.76% | 1148.84 | 184 |

## Recommendations

Based on this analysis:

1. Review the top performing configurations in detail
2. Consider the trade-off between win rate and total PnL
3. Examine the distribution of wins/losses across different market conditions
4. Test the selected configurations on out-of-sample data before live trading

## Files Generated

- `rr_analysis_detailed_1m.csv` - Per-trade results for 1-minute timeframe
- `rr_analysis_detailed_5m.csv` - Per-trade results for 5-minute timeframe
- `rr_analysis_detailed_15m.csv` - Per-trade results for 15-minute timeframe
- `rr_analysis_matrix.csv` - Performance matrix for all configurations
- `rr_analysis_comprehensive_report.txt` - Full detailed report

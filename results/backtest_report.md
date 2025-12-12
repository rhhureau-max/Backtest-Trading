# ICT London Session Strategy Backtest Report

## Strategy Overview

**Strategy:** ICT London Session (Silver Bullet + OTE Continuation)  
**Execution Timeframe:** 5m  
**Data Range:** 2018-01-01 to 2025-11-11  
**Initial Capital:** $100,000.00  

---

## Performance Summary

| Metric | Value |
|--------|-------|
| **Final Equity** | $82,210.53 |
| **Total Return** | -17.79% |
| **Max Drawdown** | -18.20% |
| **Sharpe Ratio** | -1.4521852627361846 |
| **Sortino Ratio** | -1.7949592317578695 |
| **Calmar Ratio** | -0.10962572331646254 |

---

## Trade Statistics

| Metric | Value |
|--------|-------|
| **Total Trades** | 511 |
| **Win Rate** | 39.33% |
| **Best Trade** | 0.78% |
| **Worst Trade** | -1.51% |
| **Avg Trade** | -0.04% |
| **Avg Trade Duration** | 0 days 01:04:00 |

---

## Risk Metrics

| Metric | Value |
|--------|-------|
| **Exposure Time** | 1.27% |
| **Profit Factor** | 0.6067284345358105 |
| **Expectancy** | -0.041013608052985866 |

---

## Equity Curve

See `equity_curve.png` for the visual representation.

---

## Strategy Rules Summary

### Entry Criteria

**London Silver Bullet (02:00-03:00 Chicago / 09:00-10:00 Paris)**
1. H4 Close > EMA(20) for longs, H4 Close < EMA(20) for shorts
2. Liquidity sweep of fractal high/low
3. Displacement candle (Body > 2x ATR)
4. Fair Value Gap formation
5. Entry at FVG Low (buy) or FVG High (sell) + 1 tick buffer

**OTE Continuation (03:00-04:00 Chicago / 10:00-11:00 Paris)**
1. 02:00-03:00 range determined as bullish/bearish
2. Entry at 62% Fibonacci retracement

### Exit Criteria
- Stop Loss: Below swing low (longs) or above swing high (shorts)
- Take Profit: Fixed 2R (Risk:Reward 1:2)

### No Trade Zone
- After 04:30 Chicago (11:30 Paris)

---

*Report generated on 2025-11-30 15:47:29*

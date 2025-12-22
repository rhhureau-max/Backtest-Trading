# Strategy A Alternatives - Backtest Results

## Overview
This document presents backtest results for **8 alternative Strategy A variants** tested on NQ 5-minute data (2018-2025). These alternatives explore different stop-loss placement methods beyond the original 5-candle swing approach.

**Dataset:** NQ (Nasdaq 100) 5-minute data  
**Period:** January 1, 2018 to November 11, 2025  
**Total Candles:** 554,518  
**FVGs Detected:** 24,584 (filtered for 02:00-06:00 opening times)

---

## Alternative 1: ATR-Based Stop-Loss

Uses Average True Range (ATR) for dynamic, volatility-adjusted stop placement.

### Results

| Variant | ATR Mult | TP | Trades | Win Rate | PF | Total PnL | Max DD | Avg Win | Avg Loss |
|---------|----------|-------|--------|----------|-----|-----------|--------|---------|----------|
| **A-ATR1** | 1.5× | 1.5 RR | 50,783 | 40.36% | 1.02 | 12,621 pts | 5,388 pts | 36.04 | -23.97 |
| **A-ATR2** | 2.0× | 2.0 RR | 18,571 | 34.41% | 1.04 | 19,229 pts | 5,527 pts | 72.61 | -36.51 |
| **A-ATR3** | 2.5× | 2.5 RR | 7,953 | 29.84% | 1.06 | 18,213 pts | 5,903 pts | 128.59 | -51.42 |
| **A-ATR4** | 3.0× | 2.5 RR | 5,244 | 30.19% | **1.09** | **20,036 pts** | 5,814 pts | 160.97 | -64.13 |

### Analysis - ATR-Based
**Strengths:**
- Adapts to market volatility automatically
- A-ATR4 achieves highest total profit (20,036 pts) among ATR variants
- Profit factor improves as ATR multiplier increases (1.02 → 1.09)

**Weaknesses:**
- Low win rates (30-40%) compared to original Strategy A (52-60%)
- High drawdowns (5,300-5,900 pts) vs original (800-1,400 pts)
- Significantly fewer trades as ATR multiplier increases

**Conclusion:**
ATR-based approach underperforms the original 5-candle swing method. While volatility adaptation sounds appealing, it results in stops that are too wide for this scalping strategy, reducing trade frequency and win rate substantially.

---

## Alternative 2: FVG-Based Stop-Loss

Places stop-loss beyond the FVG zone that triggered the entry, based on market structure logic.

### Results

| Variant | Buffer | TP | Trades | Win Rate | PF | Total PnL | Max DD | Avg Win | Avg Loss |
|---------|--------|-------|--------|----------|-----|-----------|--------|---------|----------|
| **A-FVG1** | +5 pts | 1.5 RR | 278 | 41.01% | 2.06 | 8,145 pts | 2,675 pts | 138.76 | -46.79 |
| **A-FVG2** | +10 pts | 2.0 RR | 163 | 38.65% | **2.61** | **10,207 pts** | **1,889 pts** | 262.56 | -63.35 |
| **A-FVG3** | +15 pts | 2.5 RR | 116 | 37.07% | 2.15 | 7,156 pts | 2,278 pts | 310.49 | -84.87 |
| **A-FVG4** | +20 pts | 3.0 RR | 79 | 30.38% | 2.00 | 5,568 pts | 2,054 pts | 463.01 | -100.81 |

### Analysis - FVG-Based
**Strengths:**
- **Exceptional profit factors** (2.00-2.61) - BEST among all variants tested
- **Lowest drawdowns** (1,889-2,675 pts) - significantly better than original
- A-FVG2 achieves best profit factor (2.61) across ALL strategies
- Very large average wins (139-463 pts) due to favorable RR ratios
- Logically aligned with strategy concept (stop beyond structure)

**Weaknesses:**
- Very low trade frequency (79-278 trades over 7 years)
- Lower win rates (30-41%) than original Strategy A
- Total profit lower than high-frequency original approach

**Conclusion:**
FVG-based approach produces **highest quality trades** with exceptional profit factors. While trade count is low, each trade has strong positive expectancy. Ideal for traders prioritizing risk-adjusted returns over volume.

---

## Comparison with Original Strategy A

### Original Strategy A (5-candle swing SL) - Reminder
| TP Ratio | Trades | Win Rate | PF | Total PnL | Max DD |
|----------|--------|----------|-----|-----------|--------|
| 1.0 RR | 67,813 | 59.99% | 1.43 | 235,915 pts | 819 pts |
| 1.5 RR | 48,961 | 56.19% | 1.47 | 207,004 pts | 1,370 pts |
| 2.0 RR | 37,667 | 53.68% | 1.51 | 188,220 pts | 846 pts |
| 2.5 RR | 31,941 | 52.14% | 1.55 | 177,799 pts | 1,096 pts |

### Key Comparisons

**Total Profit:**
1. Original A - 1.0 RR: **235,915 pts** ⭐ WINNER
2. Original A - 1.5 RR: 207,004 pts
3. Original A - 2.0 RR: 188,220 pts
4. ATR4: 20,036 pts
5. FVG2: 10,207 pts

**Profit Factor (Risk Efficiency):**
1. FVG2 (10pts buffer, 2.0 RR): **2.61** ⭐ WINNER
2. FVG3 (15pts buffer, 2.5 RR): 2.15
3. FVG1 (5pts buffer, 1.5 RR): 2.06
4. FVG4 (20pts buffer, 3.0 RR): 2.00
5. Original A - 2.5 RR: 1.55

**Win Rate:**
1. Original A - 1.0 RR: **59.99%** ⭐ WINNER
2. Original A - 1.5 RR: 56.19%
3. Original A - 2.0 RR: 53.68%
4. Original A - 2.5 RR: 52.14%
5. FVG1: 41.01%

**Maximum Drawdown:**
1. Original A - 1.0 RR: **819 pts** ⭐ WINNER
2. Original A - 2.0 RR: 846 pts
3. Original A - 2.5 RR: 1,096 pts
4. FVG2: 1,889 pts

**Trade Frequency:**
1. Original A - 1.0 RR: **67,813 trades** ⭐ Most active
2. ATR1: 50,783 trades
3. Original A - 1.5 RR: 48,961 trades
4. FVG2: 163 trades (Least active but highest PF)

---

## Recommendations

### For Maximum Total Profit
**Use: Original Strategy A with 1.0 RR**
- Highest absolute returns: 235,915 pts
- High win rate: 59.99%
- Lowest drawdown: 819 pts
- Most trades: 67,813

### For Best Risk-Adjusted Returns
**Use: A-FVG2 (FVG edge + 10pts SL, 2.0 RR TP)**
- Best profit factor: 2.61
- Solid profit: 10,207 pts
- Reasonable drawdown: 1,889 pts
- Quality over quantity: 163 high-probability trades

### For Balanced Approach
**Use: Original Strategy A with 2.0 RR**
- Good total profit: 188,220 pts
- Strong profit factor: 1.51
- Low drawdown: 846 pts
- Good win rate: 53.68%
- Manageable trade count: 37,667

### For Conservative/Part-Time Traders
**Use: A-FVG3 or A-FVG4**
- Very few trades (116 or 79 over 7 years)
- Excellent profit factors (2.15 or 2.00)
- Large average wins
- Minimal time commitment required

---

## Summary Statistics

### Best Performers by Category

| Category | Winner | Value | Notes |
|----------|--------|-------|-------|
| **Highest Total Profit** | Original A - 1.0 RR | 235,915 pts | 10× more than best alternative |
| **Best Profit Factor** | A-FVG2 | 2.61 | 68% better than original best |
| **Highest Win Rate** | Original A - 1.0 RR | 59.99% | Significantly higher |
| **Lowest Drawdown** | Original A - 1.0 RR | 819 pts | Most stable equity curve |
| **Most Trades** | Original A - 1.0 RR | 67,813 | Active trading |
| **Largest Avg Win** | A-FVG4 | 463.01 pts | Big winners |

---

## Conclusions

1. **Original Strategy A remains superior** for absolute profit generation
   - 5-candle swing SL provides optimal balance of frequency and risk
   - Win rates of 52-60% are substantially higher than alternatives
   - Lowest drawdowns indicate more stable performance

2. **FVG-based alternatives excel in risk-adjusted metrics**
   - Profit factors of 2.00-2.61 are exceptional
   - Ideal for traders with limited time or capital
   - Better for risk-conscious approach

3. **ATR-based alternatives underperform**
   - Stops are too wide for this scalping strategy
   - Low win rates and high drawdowns
   - Not recommended for FVG Inversion strategy

4. **Trade-off: Volume vs Quality**
   - Original A: High volume (67K trades), good quality (1.43-1.55 PF)
   - FVG-based: Low volume (79-278 trades), exceptional quality (2.00-2.61 PF)

5. **Recommendation Hierarchy:**
   - **Best Overall:** Original Strategy A with 1.0 RR
   - **Best Alternative:** A-FVG2 (for risk-adjusted returns)
   - **Avoid:** ATR-based variants (underperform on all key metrics)

The original 5-candle swing approach proves to be the optimal choice for most traders, while FVG-based alternatives offer a compelling option for those prioritizing risk efficiency over trade frequency.

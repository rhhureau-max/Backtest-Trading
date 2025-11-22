# FVG Maximum Price Excursion - Multi-Window Comparison

## Overview

Comprehensive comparison of maximum price excursion for Good FVG across all timeframes and window sizes.

## Cross-Timeframe Comparison

### Combined Average Excursion by Window and Timeframe

| Window | 1m (ticks) | 1m (points) | 5m (ticks) | 5m (points) | 15m (ticks) | 15m (points) |
|--------|------------|-------------|------------|-------------|-------------|-------------|
| 5 | 134.89 | 33.72 | 231.99 | 58.00 | 327.93 | 81.98 |
| 10 | 188.55 | 47.14 | 329.15 | 82.29 | 437.78 | 109.45 |
| 15 | 226.27 | 56.57 | 405.34 | 101.33 | 498.91 | 124.73 |
| 20 | 260.74 | 65.19 | 455.39 | 113.85 | 572.78 | 143.20 |
| 25 | 287.61 | 71.90 | 494.73 | 123.68 | 670.55 | 167.64 |
| 30 | 316.34 | 79.09 | 524.77 | 131.19 | 710.61 | 177.65 |
| 50 | 392.61 | 98.15 | 606.70 | 151.67 | 794.19 | 198.55 |

## Key Findings

### 1. Timeframe Impact on Excursion

Higher timeframes consistently show larger maximum excursions across all window sizes:

- 5 candle window: 15m shows 2.43x larger excursions than 1m
- 15 candle window: 15m shows 2.20x larger excursions than 1m
- 30 candle window: 15m shows 2.25x larger excursions than 1m
- 50 candle window: 15m shows 2.02x larger excursions than 1m

### 2. Window Size Impact

Excursion potential grows with window size, but at a decreasing rate:

- **1M**: 134.89 → 392.61 ticks (+191.1% growth from 5 to 50 candles)
- **5M**: 231.99 → 606.70 ticks (+161.5% growth from 5 to 50 candles)
- **15M**: 327.93 → 794.19 ticks (+142.2% growth from 5 to 50 candles)

### 3. Trading Strategy Recommendations

#### By Trading Style

**Scalper (5-10 candle windows):**
- Quick entries/exits
- Smaller targets but higher win rate
- Best on 1m timeframe for precision

**Day Trader (15-25 candle windows):**
- Balanced risk/reward
- Moderate position holding time
- 5m timeframe offers good balance

**Swing Trader (30-50 candle windows):**
- Larger targets and stops
- Extended holding periods
- 15m timeframe maximizes profit potential

#### Position Sizing by Window

Adjust position size based on expected excursion and required stop-loss:

**5 Candle Window:**
- 1m: Target ~33.7 points, Stop ~16.9 points
- 5m: Target ~58.0 points, Stop ~29.0 points
- 15m: Target ~82.0 points, Stop ~41.0 points

**15 Candle Window:**
- 1m: Target ~56.6 points, Stop ~28.3 points
- 5m: Target ~101.3 points, Stop ~50.7 points
- 15m: Target ~124.7 points, Stop ~62.4 points

**30 Candle Window:**
- 1m: Target ~79.1 points, Stop ~39.5 points
- 5m: Target ~131.2 points, Stop ~65.6 points
- 15m: Target ~177.7 points, Stop ~88.8 points

## Conclusion

The multi-window analysis reveals that:

1. **Excursion scales with both timeframe and window size**
2. **15m timeframe offers the largest profit potential**
3. **Window selection should match trading style and risk tolerance**
4. **Longer windows require proportionally larger stops**
5. **Growth rate decreases as window size increases** (diminishing returns)


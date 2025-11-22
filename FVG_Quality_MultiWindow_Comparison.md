# FVG Quality Analysis - Multi-Window Comparison (All Timeframes)

## Overview

This document provides a comprehensive comparison of FVG quality across different candle windows and timeframes.

**Analyzed Windows:** 5, 10, 15, 20, 25, 30, 50 candles  
**Timeframes:** 1-minute, 5-minute, 15-minute  
**Period:** 2018-2025  
**Total FVG Analyzed:** 2,634 occurrences

---

## Key Finding: FVG Quality Degrades Over Time

As the look-ahead window increases, FVG quality consistently decreases across all timeframes. This indicates that most FVG gaps eventually get filled, but the timing matters significantly.

---

## Overall Results by Timeframe and Window

### 1-Minute Data

| Window | Total FVG | Good FVG | Good % | Bad FVG | Bad % | Degradation |
|--------|-----------|----------|--------|---------|-------|-------------|
| 5 | 817 | 313 | 38.31% | 504 | 61.69% | - |
| 10 | 817 | 259 | 31.70% | 558 | 68.30% | -6.61% |
| 15 | 817 | 224 | 27.42% | 593 | 72.58% | -10.89% |
| 20 | 817 | 204 | 24.97% | 613 | 75.03% | -13.34% |
| 25 | 817 | 189 | 23.13% | 628 | 76.87% | -15.18% |
| 30 | 817 | 175 | 21.42% | 642 | 78.58% | -16.89% |
| 50 | 817 | 150 | 18.36% | 667 | 81.64% | -19.95% |

**Time Impact:**  
- 5 candles = ~5 minutes: 38.31% good  
- 50 candles = ~50 minutes: 18.36% good  
- **Net degradation: 19.95 percentage points over 45 minutes**

### 5-Minute Data

| Window | Total FVG | Good FVG | Good % | Bad FVG | Bad % | Degradation |
|--------|-----------|----------|--------|---------|-------|-------------|
| 5 | 925 | 374 | 40.43% | 551 | 59.57% | - |
| 10 | 925 | 301 | 32.54% | 624 | 67.46% | -7.89% |
| 15 | 925 | 267 | 28.86% | 658 | 71.14% | -11.57% |
| 20 | 925 | 249 | 26.92% | 676 | 73.08% | -13.51% |
| 25 | 925 | 234 | 25.30% | 691 | 74.70% | -15.13% |
| 30 | 925 | 225 | 24.32% | 700 | 75.68% | -16.11% |
| 50 | 925 | 199 | 21.51% | 726 | 78.49% | -18.92% |

**Time Impact:**  
- 5 candles = ~25 minutes: 40.43% good  
- 50 candles = ~4 hours 10 minutes: 21.51% good  
- **Net degradation: 18.92 percentage points over 3 hours 45 minutes**

### 15-Minute Data

| Window | Total FVG | Good FVG | Good % | Bad FVG | Bad % | Degradation |
|--------|-----------|----------|--------|---------|-------|-------------|
| 5 | 892 | 370 | 41.48% | 522 | 58.52% | - |
| 10 | 892 | 311 | 34.87% | 581 | 65.13% | -6.61% |
| 15 | 892 | 275 | 30.83% | 617 | 69.17% | -10.65% |
| 20 | 892 | 252 | 28.25% | 640 | 71.75% | -13.23% |
| 25 | 892 | 239 | 26.79% | 653 | 73.21% | -14.69% |
| 30 | 890 | 234 | 26.29% | 656 | 73.71% | -15.19% |
| 50 | 890 | 224 | 25.17% | 666 | 74.83% | -16.31% |

**Time Impact:**  
- 5 candles = ~1 hour 15 minutes: 41.48% good  
- 50 candles = ~12 hours 30 minutes: 25.17% good  
- **Net degradation: 16.31 percentage points over 11 hours 15 minutes**

---

## Cross-Timeframe Analysis

### Good FVG % by Window

| Window | 1-Minute | 5-Minute | 15-Minute | Average | Best TF |
|--------|----------|----------|-----------|---------|---------|
| 5 | 38.31% | 40.43% | 41.48% | 40.07% | 15m |
| 10 | 31.70% | 32.54% | 34.87% | 33.04% | 15m |
| 15 | 27.42% | 28.86% | 30.83% | 29.04% | 15m |
| 20 | 24.97% | 26.92% | 28.25% | 26.71% | 15m |
| 25 | 23.13% | 25.30% | 26.79% | 25.07% | 15m |
| 30 | 21.42% | 24.32% | 26.29% | 24.01% | 15m |
| 50 | 18.36% | 21.51% | 25.17% | 21.68% | 15m |

**Key Insight:** 15-minute timeframe consistently shows best FVG quality across all windows.

### Degradation Rate by Timeframe

| Timeframe | Initial (5c) | Final (50c) | Total Drop | Avg Drop/Window |
|-----------|--------------|-------------|------------|-----------------|
| 1-Minute | 38.31% | 18.36% | -19.95% | -0.44%/candle |
| 5-Minute | 40.43% | 21.51% | -18.92% | -0.42%/candle |
| 15-Minute | 41.48% | 25.17% | -16.31% | -0.36%/candle |

**Key Insight:** 15-minute timeframe shows most resilient FVG quality over time.

---

## Statistical Analysis

### Half-Life Analysis

The "half-life" is the window where 50% of initially good FVG have been filled:

| Timeframe | Initial Good % | 50% Mark | Half-Life Window | Time to Half-Life |
|-----------|----------------|----------|------------------|-------------------|
| 1-Minute | 38.31% | ~19% | ~45 candles | ~45 minutes |
| 5-Minute | 40.43% | ~20% | ~50 candles | ~4 hours 10 min |
| 15-Minute | 41.48% | ~21% | >50 candles | >12 hours 30 min |

### Marginal Degradation

**Degradation rate by window increment:**

| Window Increase | 1m Drop | 5m Drop | 15m Drop | Avg Drop |
|----------------|---------|---------|----------|----------|
| 5 → 10 | -6.61% | -7.89% | -6.61% | -7.04% |
| 10 → 15 | -4.28% | -3.68% | -4.04% | -4.00% |
| 15 → 20 | -2.45% | -1.94% | -2.58% | -2.32% |
| 20 → 25 | -1.84% | -1.62% | -1.46% | -1.64% |
| 25 → 30 | -1.71% | -0.98% | -0.50% | -1.06% |
| 30 → 50 | -3.06% | -2.81% | -1.12% | -2.33% |

**Key Insight:** Steepest degradation occurs in first 10 candles, then gradually slows.

---

## Trading Strategy Implications

### Optimal Window Selection

Based on risk/reward profiles:

#### Conservative Strategy (Maximize Good FVG Rate)
- **Recommended Window:** 5 candles
- **Expected Good Rate:** ~40%
- **Time Commitment:** 
  - 1m: ~5 minutes
  - 5m: ~25 minutes
  - 15m: ~1 hour 15 minutes

#### Balanced Strategy (Medium-Term Holds)
- **Recommended Window:** 15-20 candles
- **Expected Good Rate:** ~27-29%
- **Time Commitment:**
  - 1m: ~15-20 minutes
  - 5m: ~1 hour 15 minutes - 1 hour 40 minutes
  - 15m: ~3 hours 45 minutes - 5 hours

#### Aggressive Strategy (Long-Term Holds)
- **Recommended Window:** 30-50 candles
- **Expected Good Rate:** ~22-24%
- **Time Commitment:**
  - 1m: ~30-50 minutes
  - 5m: ~2 hours 30 minutes - 4 hours 10 minutes
  - 15m: ~7 hours 30 minutes - 12 hours 30 minutes

### Position Sizing Recommendations

| Window | Good FVG % | Risk Level | Position Size | Stop Loss |
|--------|-----------|------------|---------------|-----------|
| 5 | 40% | Low | 100% | Normal |
| 10 | 33% | Moderate | 80% | Tight 10% |
| 15 | 29% | Elevated | 60% | Tight 15% |
| 20 | 27% | High | 50% | Tight 20% |
| 25+ | <26% | Very High | 40% | Tight 25% |

### Exit Strategy

**Based on window analysis:**

1. **Early Exit (5-10 candles):** 
   - Capture profits when ~60-65% of FVG have filled
   - Avoid the steepest degradation period

2. **Medium Exit (15-20 candles):**
   - Hold through initial volatility
   - Exit when ~70-73% filled

3. **Late Exit (30+ candles):**
   - Only for highest conviction setups
   - Accept that ~75-80% will eventually fill

---

## Year-Specific Patterns

### Best Year by Window (15-Minute Data)

| Window | Best Year | Good % | Worst Year | Good % | Spread |
|--------|-----------|--------|------------|--------|--------|
| 5 | 2021 | 49.15% | 2023 | 33.01% | 16.14% |
| 10 | 2021 | 45.76% | 2023 | 28.16% | 17.60% |
| 15 | 2021 | 40.68% | 2023 | 23.30% | 17.38% |
| 20 | 2021 | 38.14% | 2023 | 20.39% | 17.75% |
| 25 | 2021 | 36.44% | 2023 | 19.42% | 17.02% |
| 30 | 2021 | 35.59% | 2023 | 18.45% | 17.14% |
| 50 | 2021 | 34.75% | 2023 | 17.48% | 17.27% |

**Key Insight:** Year-to-year variation remains consistent across all windows (~17% spread).

---

## Critical Insights

### 1. Time Is The Enemy
- FVG quality degrades progressively over time
- Most degradation happens in first 10 candles
- After 20 candles, degradation rate slows significantly

### 2. Timeframe Hierarchy Maintained
- 15m > 5m > 1m across ALL windows
- Relationship is consistent regardless of look-ahead period

### 3. Sweet Spot Identified
- 5-10 candle window offers best risk/reward
- Balances decent hold rate (~33-40%) with manageable time commitment
- Avoids steepest part of degradation curve

### 4. Long-Term Holds Are Challenging
- By 50 candles, only ~20-25% of FVG still hold
- 75-80% of gaps eventually fill
- Long-term FVG trading requires exceptional stock selection

### 5. Market Regime Still Matters
- Year-to-year variation (~17%) persists across all windows
- 2021 consistently best, 2023 consistently worst
- Market conditions impact all holding periods equally

---

## Recommendations for Traders

### When to Use Short Windows (5-10 candles)
- ✅ Scalping strategies
- ✅ High-frequency trading
- ✅ Volatile market conditions
- ✅ When capital efficiency is priority

### When to Use Medium Windows (15-25 candles)
- ✅ Swing trading
- ✅ Position building
- ✅ Stable market conditions
- ✅ When conviction is moderate-high

### When to Use Long Windows (30-50 candles)
- ✅ Core position holds
- ✅ Strong confluence with other signals
- ✅ Low volatility environments
- ✅ When conviction is very high
- ⚠️ Accept 75-80% will fail

### Universal Rules
1. **Always use stop losses** - Even 5-candle windows have 60% failure rate
2. **Adjust for timeframe** - 15m consistently more reliable
3. **Consider market regime** - 2023-type years need extra caution
4. **Scale position size** - Longer windows = smaller positions

---

## Conclusion

This multi-window analysis reveals that FVG quality is time-dependent, with a clear degradation pattern across all timeframes. Traders should:

1. **Optimize for 5-10 candle windows** for best risk/reward
2. **Prefer 15-minute timeframe** for highest reliability
3. **Adjust expectations by window** - longer holds = lower success rates
4. **Manage risk actively** - majority of FVG eventually fill

The data suggests FVG trading is most effective as a short-to-medium-term strategy, with diminishing returns for longer holding periods.

---

*Analysis based on 2,634 FVG occurrences across three timeframes spanning 2018-2025*

# NQ Daily Trend Filter Backtest - Documentation

## Overview

This script tests **lightweight daily trend filters** for the London Manipulation strategy (FVG Inversion). Unlike the restrictive H1 MSS filter (24 trades), these daily filters aim to eliminate counter-trend trades while maintaining reasonable trade frequency.

## Problem Statement

The H1 Market Structure Shift (MSS) filter produces excellent results:
- ✅ 95.83% win rate
- ✅ 30.53 profit factor
- ❌ **Only 24 trades in 7 years** (too restrictive)

**Goal**: Find a filter that:
1. Generates **more trades** than H1 MSS (>24)
2. Improves quality vs baseline (1,618 trades)
3. Uses **daily timeframe only** (simpler, less CPU intensive)
4. Maintains 60-70% win rate target

## Daily Filters Tested

### Filter 1: Previous Day Color (Momentum)
**Principle**: The previous day's candle direction indicates trend continuation.

**Logic**:
- **Long only**: If Close(D-1) > Open(D-1) (previous day was green/bullish)
- **Short only**: If Close(D-1) < Open(D-1) (previous day was red/bearish)

**Reasoning**: Continuation of daily momentum - if yesterday was bullish, today should favor longs.

### Filter 2: Weekly Open (Context)
**Principle**: Current price position relative to weekly open determines bias.

**Reference**: Monday 00:00 or Sunday 17:00 open price = `Weekly_Open`

**Logic**:
- **Long only**: If Current_Price > Weekly_Open (trading above weekly open)
- **Short only**: If Current_Price < Weekly_Open (trading below weekly open)

**Reasoning**: Premium/discount pricing relative to weekly opening auction.

### Baseline: No Filter
All 1,618 setups taken for comparison.

## Backtest Results (2018-2025)

### Summary Statistics
- **Period analyzed**: 2018-2025 (7+ years)
- **Total setups identified**: 1,618
- **Filters tested**: 3 cases (including baseline)

### Comparison Table

| Filter | Trades | Win Rate | Net Profit | Profit Factor | Max Consec. Losses | Trades/Year |
|--------|--------|----------|------------|---------------|-------------------|-------------|
| **1. Baseline (No Filter)** | 1,618 | 64.46% | +557.68 pts | 1.10 | 5 | 231 |
| **2. PrevDay Color** | 821 | 63.58% | +247.87 pts | 1.09 | 5 | 117 |
| **3. Weekly Open** | 691 | 63.97% | +143.56 pts | 1.06 | 4 | 99 |

### Detailed Analysis

#### 📊 **Filter 2: Previous Day Color**
- **Trade reduction**: 49.3% (1,618 → 821 trades)
- **Win rate change**: -0.88pp (64.46% → 63.58%)
- **Profit factor**: 1.09 (vs 1.10 baseline)
- **Trades retained**: 50.7% (moderate filter)

**Performance**:
- ✓ Retains ~117 trades/year (good frequency)
- ✓ Reduces noise by 49%
- ✗ Slightly lower win rate than baseline
- ✗ Profit factor not significantly improved

**Assessment**: **Moderate filtering** - removes about half the trades but doesn't improve quality metrics significantly.

#### 📊 **Filter 3: Weekly Open**
- **Trade reduction**: 57.3% (1,618 → 691 trades)
- **Win rate change**: -0.49pp (64.46% → 63.97%)
- **Profit factor**: 1.06 (vs 1.10 baseline)
- **Trades retained**: 42.7% (moderate filter)

**Performance**:
- ✓ Retains ~99 trades/year (decent frequency)
- ✓ Reduces noise by 57%
- ✓ Reduces max consecutive losses (5 → 4)
- ✗ Lower win rate than baseline
- ✗ Lowest profit factor of all filters

**Assessment**: **More restrictive** than PrevDay Color but doesn't deliver better quality.

#### 📊 **Baseline (No Filter)**
- **All 1,618 trades taken**
- **Best win rate**: 64.46%
- **Best profit factor**: 1.10
- **Problem**: No filtering = takes all setups including counter-trend

**Assessment**: Highest metrics but no trend filtering applied.

## Key Insights

### 1. Daily Filters Don't Improve Quality Significantly

**Surprising result**: Both daily filters **reduce** win rate and profit factor slightly:
- PrevDay Color: -0.88pp win rate, -0.01 PF
- Weekly Open: -0.49pp win rate, -0.04 PF

**Why?**
- Daily trend signals are too **slow** to catch intraday reversals
- M5 setups can occur during counter-trend pullbacks within daily trends
- Previous day's close doesn't predict next day's intraday structure

### 2. Trade Frequency vs H1 MSS Comparison

| Filter | Trades | vs H1 MSS | Win Rate | Profit Factor |
|--------|--------|-----------|----------|---------------|
| **H1 MSS** | 24 | Baseline | 95.83% | 30.53 |
| **PrevDay Color** | 821 | **+797 trades** | 63.58% | 1.09 |
| **Weekly Open** | 691 | **+667 trades** | 63.97% | 1.06 |

**Trade-off**:
- ✅ Daily filters generate **28-34x more trades** than H1 MSS
- ❌ But **much lower quality** (64% vs 96% win rate)
- ❌ Profit factor drops **28x** (1.09 vs 30.53)

### 3. Neither Filter Meets Target Criteria

**Target requirements**:
- ✓ 60-70% win rate
- ✓ Profit factor > 1.5
- ✓ Retain >30% of trades

**Results**:
- ✓ Win rates: 63.58-63.97% (meets target)
- ✗ Profit factors: 1.06-1.09 (below 1.5 target)
- ✓ Trade retention: 43-51% (meets target)

**Verdict**: Daily filters meet **2 out of 3** criteria but fail on profit factor.

### 4. Restrictiveness Analysis

| Filter | Trades Retained | Classification | Effectiveness |
|--------|----------------|----------------|---------------|
| **PrevDay Color** | 50.7% | Moderate | Low (quality not improved) |
| **Weekly Open** | 42.7% | Moderate | Low (quality decreased) |
| **H1 MSS** (reference) | 1.5% | Very Restrictive | Excellent (quality massively improved) |

**Conclusion**: Daily filters are **not restrictive enough** to improve quality, but **too restrictive** relative to the small quality gain.

### 5. Best Balance Assessment

**If forced to choose a daily filter**:
- **Previous Day Color** (821 trades) offers:
  - Better trade frequency (117/year)
  - Slightly better profit factor (1.09 vs 1.06)
  - Same max drawdown (5)
  
**However**: Neither filter justifies use vs baseline or H1 MSS.

## Recommendations

### ❌ **Do NOT Use Daily Filters Alone**

**Reasons**:
1. **Marginal improvement**: Win rate and profit factor barely change or slightly worsen
2. **Wrong timeframe**: Daily trends don't predict M5 intraday reversals effectively
3. **Poor value**: Cutting 50% of trades for -0.88pp win rate change is bad ROI

### ✅ **Stick with H1 MSS Filter Instead**

**Why H1 MSS remains superior**:
- **96% win rate** vs 64% with daily filters
- **30.53 profit factor** vs 1.09 with daily filters
- **Better risk management**: Max 1 consecutive loss vs 4-5

**Accept the trade-off**: 24 trades/year of excellent quality >>> 800 trades/year of mediocre quality.

### 🤔 **Alternative Approach: Combine Filters**

If you need more trades, consider **H1 MSS + Midnight Open**:
- H1 MSS alone: 24 trades, 95.83% WR
- Midnight Open alone: 1,086 trades, 67.77% WR
- Combo: 8 trades, 100% WR (too few, but principle is sound)

**Recommended for future testing**:
- H1 MSS (primary filter) + Daily filter (secondary)
- May achieve 40-60 trades/year with 75-85% win rate
- Better than daily filters alone

## Usage

```bash
# Install dependencies
pip install pandas numpy

# Run the backtest
python nq_daily_filter_backtest.py
```

The script will:
1. Load M5 data for trade execution
2. Load 1D data for daily trend analysis
3. Identify all 1,618 setups
4. Apply 3 filter scenarios
5. Calculate metrics and export results

## Outputs

1. **Console**: Detailed comparison table with analysis
2. **CSV**: `nq_daily_filter_results.csv` with all metrics
3. **Analysis**: Filter effectiveness breakdown and recommendations

## Technical Notes

- **Timeframes**: 1D for filters, M5 for execution
- **Data period**: 2018-2025 (7+ years, 2,449 trading days)
- **Previous day lookback**: Up to 5 days (accounts for weekends)
- **Weekly open**: Sunday 17:00 or Monday 00:00 (futures market hours)
- **Timezone**: Chicago (CST/CDT)

## Strategic Lesson

> **"Lightweight daily filters are not sufficient to improve trade quality significantly."**

This analysis demonstrates:
- ✅ Daily filters reduce trade count by 43-57%
- ❌ But quality metrics (WR, PF) don't improve meaningfully
- ✅ H1 structure (intraday context) is far more predictive than daily momentum
- ❌ Daily timeframe is too slow for M5 execution filtering

**The key insight**: **Intraday structure (H1 MSS) >> Daily momentum** for M5 trade filtering.

## Comparison to H1 MSS Study

| Metric | Daily Filters (Best) | H1 MSS Filter |
|--------|---------------------|---------------|
| **Trades** | 821 | 24 |
| **Win Rate** | 63.58% | 95.83% |
| **Profit Factor** | 1.09 | 30.53 |
| **Max Consec. Losses** | 5 | 1 |
| **Net Profit** | +247.87 pts | +177.91 pts |
| **Trades/Year** | 117 | 3.4 |

**Verdict**: H1 MSS sacrifices quantity but delivers **28x better profit factor** and **32pp higher win rate**.

## Conclusion

**Daily trend filters fail to achieve the goal** of improving trade quality while maintaining frequency:

1. ❌ **Previous Day Color**: Cuts 49% of trades but worsens metrics slightly
2. ❌ **Weekly Open**: Cuts 57% of trades but has worst profit factor (1.06)
3. ✅ **H1 MSS remains superior**: Even with only 24 trades, quality is unmatched

**Final recommendation**: 
- Continue using **H1 MSS filter** for institutional-grade quality (95.83% WR)
- Accept lower trade frequency (24/year) as the price of excellence
- Future research: Combine H1 MSS with secondary filters to reach 40-60 trades/year

## Future Research Ideas

1. **H4 Structure**: Test 4-hour swing detection as middle ground between H1 and 1D
2. **Multi-day Momentum**: 2-3 consecutive green/red days for stronger signal
3. **Daily Range**: Filter based on daily ATR or range expansion
4. **Combined Approach**: H1 MSS primary + Daily secondary filter
5. **Machine Learning**: Use ML to find optimal daily indicator combinations

## Warnings

⚠️ **Disclaimer**: This backtest is for educational purposes. Past performance doesn't guarantee future results. Daily filters show limited effectiveness and should not be used as sole filtering mechanism for this M5 strategy.

---

**Created**: 2025
**Strategy**: London Manipulation (FVG Inversion)
**Author**: Systematic Backtest Analysis

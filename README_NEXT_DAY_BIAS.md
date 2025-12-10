# Next Day Bias Probability Study - Results

## Overview

Statistical analysis of 5 predictive scenarios to determine next-day bias probabilities based on current day patterns for NQ futures (2018-2025).

## Methodology

For each scenario, calculated:
- **Win Rate**: % times next day follows theoretical bias
- **Loss Rate**: % times next day does opposite  
- **Average Return**: Mean performance in points next day

---

## Results Summary (NQ 2018-2025, 2,033 daily candles)

| Scenario | Count | Win Rate | Avg Return | Edge |
|----------|-------|----------|------------|------|
| **Gap Up Continuation** | 20 | **75.00%** ✅ | **+141.23** | **STRONG** |
| **Inside Day Expansion** | 155 | **70.97%** ✅ | **+67.63** | **STRONG** |
| Three Day Rule | 177 | 54.24% | +22.09 | Weak |
| Failed Breakdown | 297 | 53.54% | +2.30 | Minimal |
| Momentum Continuation | 154 | 51.30% | -13.43 | None |

---

## Scenario 1: Momentum Continuation (Strong Close)

### Setup
- **Condition J**: Close in top 10% of daily range AND volume > 20-day MA
- **Theoretical Bias**: BULLISH (buy at open J+1)
- **Strategy**: Buy at open J+1, sell at close J+1

### Results (NQ 2018-2025)
- **Total Occurrences**: 154
- **Win Rate**: 51.30% (barely above coin flip)
- **Loss Rate**: 48.70%
- **Average Return**: -13.43 pts ❌
- **Best Return**: +536.70 pts
- **Worst Return**: -810.98 pts
- **Median Return**: +6.49 pts

### Analysis
❌ **NO EDGE** - Despite strong close with high volume, next day barely breaks even at 51.30% WR with negative average return (-13.43 pts). The median is positive (+6.49) suggesting outlier losses skew the mean. **NOT TRADEABLE**.

---

## Scenario 2: Failed Breakdown (Turtle Soup / Rejection)

### Setup
- **Condition J**: Low breaks previous day low BUT closes green and above prev low (wick rejection)
- **Theoretical Bias**: BULLISH (reversal)
- **Strategy**: Expect next day to be green

### Results (NQ 2018-2025)
- **Total Occurrences**: 297
- **Win Rate**: 53.54%
- **Loss Rate**: 46.46%
- **Average Return**: +2.30 pts
- **Best Return**: +634.87 pts
- **Worst Return**: -967.11 pts

### Analysis
⚠️ **MINIMAL EDGE** - 53.54% WR is statistically insignificant (barely above 50%). Average return of +2.30 pts is too small for practical trading after commissions/slippage. Classic "Turtle Soup" pattern shows **weak predictive power on NQ daily timeframe**.

---

## Scenario 3: Inside Day Compression (Volatility Squeeze)

### Setup
- **Condition J**: High < Prev_High AND Low > Prev_Low (inside bar/consolidation)
- **Theoretical Bias**: EXPANSION (breakout)
- **Strategy**: If J+1 breaks high of inside day, expect green day

### Results (NQ 2018-2025)
- **Total Inside Days**: 242
- **Breakouts**: 155 (64.05% of inside days break out bullish)
- **Win Rate (Breakout & Green)**: **70.97%** ✅
- **Loss Rate**: 29.03%
- **Average Return**: **+67.63 pts** ✅
- **Best Return**: +2,176.14 pts
- **Worst Return**: -590.79 pts

### Analysis
✅ **STRONG EDGE** - Best statistical setup! 70.97% WR when breakout occurs. Average return of +67.63 pts is substantial. Inside day compression followed by bullish breakout is highly predictive of green close. **HIGHLY TRADEABLE** - this is a validated pattern.

**Key Insight**: Not all inside days break out (64%), but when they do bullishly, they have 71% chance of finishing green with excellent average return.

---

## Scenario 4: Three Day Rule (Mean Reversion)

### Setup
- **Condition J**: 3 consecutive red days (selling pressure)
- **Theoretical Bias**: BULLISH (technical bounce/mean reversion)
- **Strategy**: Expect day 4 to be green (reversal)

### Results (NQ 2018-2025)
- **Total Occurrences**: 177 (3 consecutive red days)
- **Win Rate (Day 4 Green)**: 54.24%
- **Loss Rate (Day 4 Red)**: 45.76%
- **Bullish/Bearish Ratio**: 96/81 = 1.19
- **Average Return**: +22.09 pts
- **Best Return**: +714.99 pts
- **Worst Return**: -567.30 pts

### Analysis
⚠️ **WEAK EDGE** - 54.24% WR is barely significant. Average return +22.09 pts is positive but modest. After 3 red days, NQ shows slight tendency to bounce (54% vs expected 50%), but edge is marginal. **NOT STRONG ENOUGH** for standalone strategy.

---

## Scenario 5: Gap Up Continuation (Gap and Go)

### Setup
- **Condition J+1**: Market opens with gap > 0.3% from J close
- **Filter**: Gap NOT filled in first hour (9:00-11:00)
- **Theoretical Bias**: BULLISH CONTINUATION (institutional strength)
- **Strategy**: If gap holds first hour, expect close higher than open

### Results (NQ 2018-2025)
- **Total Gap Up Days (>0.3%)**: 44
- **Gaps NOT filled in first hour**: 20 (45.45%)
- **Gaps filled in first hour**: 15 (34.09%)
- **Win Rate (Finished higher than open)**: **75.00%** ✅
- **Loss Rate**: 25.00%
- **Average Return from open**: **+141.23 pts** ✅
- **Best Return**: +569.73 pts
- **Worst Return**: -112.38 pts
- **Average Gap Size**: 0.67%

### Analysis
✅ **STRONGEST EDGE** - 75% WR with massive +141.23 pts average return! When NQ gaps up >0.3% and holds gap in first hour, it's highly predictive of continued strength. Only 20 occurrences in 7 years = **RARE BUT POWERFUL**. This is institutional continuation - gap and go validated.

**Key Insight**: The first hour filter is critical - only 45% of gaps remain unfilled first hour, but those that do have 75% success rate.

---

## Trading Recommendations

### 🥇 Tier 1: High Probability Setups (Trade These)

**1. Gap Up Continuation**
- **Win Rate**: 75.00%
- **Avg Return**: +141.23 pts
- **Frequency**: Rare (20 occurrences / 7 years ≈ 3 per year)
- **Action**: When NQ gaps up >0.3% and doesn't fill in first hour, BUY. Hold until close.
- **Risk Management**: Stop loss if gap fills. Target: hold for close.

**2. Inside Day Expansion**
- **Win Rate**: 70.97% (when breakout occurs)
- **Avg Return**: +67.63 pts
- **Frequency**: Common (155 breakouts / 7 years ≈ 22 per year)
- **Action**: After inside day, if next day breaks above inside high, BUY. 
- **Risk Management**: Stop below inside day low. Target: hold for close.

### 🥈 Tier 2: Marginal Setups (Use as Confluence Only)

**3. Three Day Rule**
- **Win Rate**: 54.24%
- **Avg Return**: +22.09 pts
- **Action**: After 3 consecutive red days, slight bullish bias for day 4. Don't trade standalone, use as confluence filter.

**4. Failed Breakdown**
- **Win Rate**: 53.54%
- **Avg Return**: +2.30 pts
- **Action**: Minimal edge. Turtle Soup concept doesn't work well on NQ daily. Skip.

### ❌ Tier 3: No Edge (Avoid)

**5. Momentum Continuation**
- **Win Rate**: 51.30%
- **Avg Return**: -13.43 pts
- **Action**: AVOID. Strong close with volume has NO predictive power next day.

---

## Statistical Significance

### Strong Edges (> 55% WR)
1. **Gap Up Continuation**: 75.00% (n=20) - Highly significant despite small sample
2. **Inside Day Expansion**: 70.97% (n=155) - Very significant, large sample

### No Edge (45-55% WR)
3. Three Day Rule: 54.24% (n=177) - Marginal
4. Failed Breakdown: 53.54% (n=297) - Minimal
5. Momentum Continuation: 51.30% (n=154) - Coin flip

---

## Interpretation Guide

**Win Rate Thresholds:**
- **> 70%**: Excellent edge, trade aggressively
- **60-70%**: Strong edge, trade with confidence
- **55-60%**: Moderate edge, trade conservatively
- **50-55%**: Marginal edge, use as confluence only
- **< 50%**: No edge, avoid or consider contrarian

**Average Return:**
- **> +100 pts**: Exceptional
- **+50 to +100 pts**: Excellent
- **+20 to +50 pts**: Good
- **0 to +20 pts**: Marginal
- **< 0 pts**: Avoid

---

## Key Findings

### What Works on NQ Daily (2018-2025)

1. **Gap and Go** (75% WR, +141 pts avg)
   - Institutional strength indicator
   - First hour filter crucial
   - Rare but powerful (3/year)

2. **Inside Day Breakout** (71% WR, +68 pts avg)
   - Compression → Expansion principle validated
   - Common occurrence (22/year)
   - Best risk/reward setup

### What Doesn't Work

1. **Momentum Continuation** (51% WR, -13 pts avg)
   - Strong close ≠ strong next day
   - Volume confirmation doesn't help
   - Avoid this pattern

2. **Failed Breakdown** (54% WR, +2 pts avg)
   - Turtle Soup concept weak on NQ daily
   - Not worth trading standalone

### Surprising Insights

- **Strong close paradox**: Despite volume and momentum, next day is coin flip
- **Compression works**: Inside days followed by bullish breakouts are highly predictive
- **Gaps are powerful**: Unfilled gaps in first hour = strong continuation signal
- **Mean reversion weak**: 3-day decline only slightly increases bounce probability

---

## Usage

```bash
# Run analysis on NQ
python next_day_bias_probability.py
```

### Programmatic Access
```python
from next_day_bias_probability import NextDayBiasProbabilityAnalyzer

# Analyze NQ
analyzer = NextDayBiasProbabilityAnalyzer(symbol='NQ', start_date='2018-01-01', csv_dir='.')
results = analyzer.run_all_scenarios()

# Access specific scenario results
gap_results = results['scenario_5']  # Gap continuation
print(f"Gap Win Rate: {gap_results['win_rate']:.2f}%")
print(f"Gap Avg Return: {gap_results['avg_return']:.2f} pts")
```

---

## Limitations

1. **Sample Size**: Scenario 5 (gaps) only has 20 occurrences - need more data for robustness
2. **Slippage/Commission**: Not included in returns
3. **Market Regime**: Data includes 2018-2025 - strong bull market bias
4. **Execution**: Assumes perfect fills at open/close
5. **Survivorship Bias**: NQ exists, other futures may not

---

## Conclusion

**Best Strategies for NQ Daily Trading:**

1. ✅ **Gap Up Continuation** - 75% WR, +141 pts avg (Tier 1)
2. ✅ **Inside Day Expansion** - 71% WR, +68 pts avg (Tier 1)
3. ⚠️ **Three Day Rule** - 54% WR, +22 pts avg (Tier 2 - confluence only)

**Avoid:**
- ❌ Momentum Continuation (no edge)
- ❌ Failed Breakdown (minimal edge)

**Portfolio Approach**: Focus on Tier 1 setups (Gaps + Inside Days) for highest probability trading on NQ daily timeframe.

---

*Generated: 2025-12-10*  
*Data: NQ Futures 2018-2025*  
*Candles Analyzed: 2,033 daily + 41,035 hourly*  
*Test Period: 7 years*

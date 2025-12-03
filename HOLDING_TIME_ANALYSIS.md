# HOLDING TIME ANALYSIS - FVG Strategy

## Executive Summary

This report analyzes the temporal dimension of FVG (Fair Value Gap) trades, measuring how long it takes for trades to reach Take Profit (TP) or Stop Loss (SL). The goal is to identify optimal holding times and detect "Dead Zones" where win probability drops significantly.

---

## 1. Winners Analysis - Time to Take Profit

### 1R Winners (n=114)

**Statistical Summary:**

- **Mean Time**: 32.2 minutes (0.54 hours)
- **Median Time**: 15.0 minutes (0.25 hours)
- **Standard Deviation**: 40.8 minutes
- **Range**: 5.0 - 285.0 minutes
- **Q25 / Q75**: 5.0 / 45.0 minutes

**Time Distribution:**

| Time Range | Count | Percentage |
|------------|-------|------------|
| < 15 min | 42 | 36.8% |
| 15-45 min | 39 | 34.2% |
| 45-60 min | 9 | 7.9% |
| > 60 min | 24 | 21.1% |

**Key Insights:**

✅ **Excellent**: 71% of winners reach TP within 45 minutes. This indicates strong momentum.

### 1.5R Winners (n=94)

**Statistical Summary:**

- **Mean Time**: 50.7 minutes (0.84 hours)
- **Median Time**: 30.0 minutes (0.50 hours)
- **Standard Deviation**: 59.9 minutes
- **Range**: 5.0 - 300.0 minutes
- **Q25 / Q75**: 10.0 / 73.8 minutes

**Time Distribution:**

| Time Range | Count | Percentage |
|------------|-------|------------|
| < 15 min | 27 | 28.7% |
| 15-45 min | 29 | 30.9% |
| 45-60 min | 6 | 6.4% |
| > 60 min | 32 | 34.0% |

**Key Insights:**

✅ **Good**: 60% of winners reach TP within 45 minutes.

### 2R Winners (n=81)

**Statistical Summary:**

- **Mean Time**: 73.8 minutes (1.23 hours)
- **Median Time**: 35.0 minutes (0.58 hours)
- **Standard Deviation**: 82.4 minutes
- **Range**: 5.0 - 360.0 minutes
- **Q25 / Q75**: 15.0 / 105.0 minutes

**Time Distribution:**

| Time Range | Count | Percentage |
|------------|-------|------------|
| < 15 min | 19 | 23.5% |
| 15-45 min | 22 | 27.2% |
| 45-60 min | 6 | 7.4% |
| > 60 min | 34 | 42.0% |

**Key Insights:**

✅ **Good**: 51% of winners reach TP within 45 minutes.

---

## 2. Losers Analysis - Time to Stop Loss

### Losing Trades (n=211)

**Statistical Summary:**

- **Mean Time**: 41.9 minutes (0.70 hours)
- **Median Time**: 15.0 minutes (0.25 hours)
- **Standard Deviation**: 66.2 minutes
- **Range**: 5.0 - 420.0 minutes
- **Q25 / Q75**: 5.0 / 45.0 minutes

**Rejection Speed:**

| Type | Count | Percentage | Interpretation |
|------|-------|------------|----------------|
| Quick (<15 min) | 97 | 46.0% | Immediate rejection |
| Slow (≥15 min) | 114 | 54.0% | Price lingered before SL |

**Comparison with Winners (1R):**

- Winners reach TP: **15.0 min** (median)
- Losers hit SL: **15.0 min** (median)
- **Difference**: 0.0 minutes

⚠️ **Warning**: Losses occur **0 minutes SLOWER** than wins. Consider tightening SL or implementing time-based exit.

---

## 3. Dead Zone Analysis - Win Rate by Holding Time

This section identifies time thresholds where win probability drops significantly, indicating potential "Dead Zones" where trades should be manually closed.

### 1R Level

| Time Limit | Wins | Losses | Total | Win Rate | Change |
|------------|------|--------|-------|----------|--------|
| 15 min | 27 | 124 | 151 | 17.88% |  |
| 30 min | 42 | 145 | 187 | 22.46% | +4.6% |
| 45 min | 51 | 164 | 215 | 23.72% | +1.3% |
| 60 min | 61 | 174 | 235 | 25.96% | +2.2% |
| 90 min | 71 | 187 | 258 | 27.52% | +1.6% |
| 120 min | 79 | 193 | 272 | 29.04% | +1.5% |
| 180 min | 90 | 202 | 292 | 30.82% | +1.8% |
| 240 min | 101 | 203 | 304 | 33.22% | +2.4% |
| 360 min | 113 | 210 | 323 | 34.98% | +1.8% |
| 480 min | 114 | 211 | 325 | 35.08% | +0.1% |

**Key Findings:**

- **Peak Win Rate**: 35.08% at 480 minutes
- ✅ **No significant drops detected** - Strategy performs consistently over time
- **Recommendation**: No time-based exit needed for 1R

### 1.5R Level

| Time Limit | Wins | Losses | Total | Win Rate | Change |
|------------|------|--------|-------|----------|--------|
| 15 min | 17 | 124 | 141 | 12.06% |  |
| 30 min | 30 | 145 | 175 | 17.14% | +5.1% |
| 45 min | 39 | 164 | 203 | 19.21% | +2.1% |
| 60 min | 46 | 174 | 220 | 20.91% | +1.7% |
| 90 min | 53 | 187 | 240 | 22.08% | +1.2% |
| 120 min | 61 | 193 | 254 | 24.02% | +1.9% |
| 180 min | 71 | 202 | 273 | 26.01% | +2.0% |
| 240 min | 83 | 203 | 286 | 29.02% | +3.0% |
| 360 min | 93 | 210 | 303 | 30.69% | +1.7% |
| 480 min | 94 | 211 | 305 | 30.82% | +0.1% |

**Key Findings:**

- **Peak Win Rate**: 30.82% at 480 minutes
- ✅ **No significant drops detected** - Strategy performs consistently over time
- **Recommendation**: No time-based exit needed for 1.5R

### 2R Level

| Time Limit | Wins | Losses | Total | Win Rate | Change |
|------------|------|--------|-------|----------|--------|
| 15 min | 13 | 124 | 137 | 9.49% |  |
| 30 min | 23 | 145 | 168 | 13.69% | +4.2% |
| 45 min | 31 | 164 | 195 | 15.90% | +2.2% |
| 60 min | 35 | 174 | 209 | 16.75% | +0.8% |
| 90 min | 42 | 187 | 229 | 18.34% | +1.6% |
| 120 min | 47 | 193 | 240 | 19.58% | +1.2% |
| 180 min | 59 | 202 | 261 | 22.61% | +3.0% |
| 240 min | 70 | 203 | 273 | 25.64% | +3.0% |
| 360 min | 80 | 210 | 290 | 27.59% | +1.9% |
| 480 min | 81 | 211 | 292 | 27.74% | +0.2% |

**Key Findings:**

- **Peak Win Rate**: 27.74% at 480 minutes
- ✅ **No significant drops detected** - Strategy performs consistently over time
- **Recommendation**: No time-based exit needed for 2R

---

## 4. Overall Recommendations

### Key Takeaways

1. **⚠️ Momentum Concern**: Losses occur slower (15 min) than wins (15 min)
   - May indicate SL is too tight or entries need refinement
   - Consider implementing time-based exits

2. **✅ Quick Execution**: 71% of winners reach TP within 45 minutes
   - Excellent momentum when trades work
   - Consider tighter time-based exits to avoid slow losers

### Time-Based Exit Recommendations

- **1R**: No time-based exit needed (consistent performance)
- **1.5R**: No time-based exit needed (consistent performance)
- **2R**: No time-based exit needed (consistent performance)

### Implementation Strategy

Based on the analysis, consider the following implementation:

```python
# Pseudocode for time-based exit logic
if time_since_entry > TIME_BASED_EXIT_THRESHOLD:
    if not reached_tp:
        close_position()  # Manual exit
        reason = 'Time-based exit - Dead Zone'
```

**Key Points:**

- Monitor elapsed time from entry
- If TP not reached within threshold, close manually
- This prevents trades from lingering in low-probability zones
- Helps preserve capital and reduce drawdown

---

## 5. Statistical Summary Table

| Metric | 1R Winners | 1.5R Winners | 2R Winners | Losers |
|--------|------------|--------------|------------|--------|
| Count | 114 | 94 | 81 | 211 |
| Mean (min) | 32.2 | 50.7 | 73.8 | 41.9 |
| Median (min) | 15.0 | 30.0 | 35.0 | 15.0 |
| Std Dev (min) | 40.8 | 59.9 | 82.4 | 66.2 |
| Min (min) | 5.0 | 5.0 | 5.0 | 5.0 |
| Max (min) | 285.0 | 300.0 | 360.0 | 420.0 |

---

## 6. Visualizations

Refer to `tokyo_fvg_holding_time_analysis.png` for comprehensive visual analysis including:

1. **Distribution Histogram**: Time to TP vs Time to SL
2. **Box Plots**: Holding time distribution by outcome
3. **Dead Zone Charts**: Win rate vs time limit for each R/R level
4. **Cumulative Distribution**: Exit times across all outcomes
5. **Time Bucket Distribution**: Percentage of winners by time range
6. **Mean vs Median Comparison**: Central tendency analysis
7. **Win Rate Heatmap**: Comprehensive view of performance by time and R/R level

---

## Conclusion

This holding time analysis provides actionable insights into the temporal dynamics of the FVG strategy. Use the identified Dead Zones and time-based exit thresholds to optimize trade management and improve overall performance.

**Next Steps:**

1. Backtest time-based exit strategy with identified thresholds
2. Monitor real-time trades for validation
3. Adjust thresholds based on market conditions
4. Combine with other exit criteria (trailing stops, volatility-based exits)

---

*Report generated: 2025-12-03 22:42:11*

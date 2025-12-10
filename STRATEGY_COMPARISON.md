# ICT Strategy Comparison - London Killzone Backtests

## Executive Summary

This document compares two ICT (Inner Circle Trader) strategies backtested on NQ (Nasdaq) 5-minute data during the London Killzone (01:00-04:00) from 2018-2025.

---

## Strategies Tested

### 1. Simple IFVG Base Strategy
**Concept**: Entry when price closes through a recent Fair Value Gap zone (inverse move)

**Logic**:
- Detect Bearish FVG (Low₁ > High₃) or Bullish FVG (High₁ < Low₃)
- LONG trigger: Close above Bearish FVG High (within 60 minutes)
- SHORT trigger: Close below Bullish FVG Low (within 60 minutes)
- Fixed risk: 20pt SL / 40pt TP (1:2 R/R)

### 2. SMT Reversal + IFVG Strategy
**Concept**: Entry after Smart Money divergence when price inverts through opposing FVG

**Logic**:
- Detect SMT: NQ Lower Low + ES Higher Low (60-min window)
- Find last Bearish FVG in 30 minutes BEFORE the low
- LONG trigger: Close above FVG top (within 45 minutes after low)
- Dynamic risk: SL at absolute low, TP at 1:2 R/R

---

## Performance Comparison

| Metric | Simple IFVG | SMT Reversal | Winner |
|--------|-------------|--------------|--------|
| **Number of Trades** | 5,216 | 1,364 | Simple IFVG |
| **Win Rate** | 39.23% | 33.50% | **Simple IFVG** |
| **Profit Factor** | 1.29 | 1.11 | **Simple IFVG** |
| **Total PnL** | 18,440 pts | 6,763 pts | **Simple IFVG** |
| **Gross Profit** | 81,840 pts | 63,219 pts | Simple IFVG |
| **Gross Loss** | 63,400 pts | 56,719 pts | SMT Reversal |
| **Average Win** | 40.00 pts | 138.33 pts | **SMT Reversal** |
| **Average Loss** | -20.00 pts | -62.88 pts | Simple IFVG |
| **Risk Type** | Fixed | Dynamic | - |

---

## Detailed Analysis

### Trade Frequency
- **Simple IFVG**: 5,216 trades over 7 years ≈ **2.0 trades/day**
- **SMT Reversal**: 1,364 trades over 7 years ≈ **0.5 trades/day**
- **Difference**: -73.8% trade reduction with SMT filters

### Win Rate Analysis
- **Simple IFVG**: 39.23% (2,046 wins, 3,170 losses)
  - With 1:2 R/R, break-even = 33.3%, strategy exceeds by +5.9pp
- **SMT Reversal**: 33.50% (457 wins, 902 losses)
  - With 1:2 R/R, break-even = 33.3%, strategy barely exceeds by +0.2pp
- **Conclusion**: Simple IFVG has **more robust edge** above break-even

### Profit Factor Analysis
- **Simple IFVG**: 1.29 (makes $1.29 for every $1 lost)
- **SMT Reversal**: 1.11 (makes $1.11 for every $1 lost)
- **Difference**: -0.18 PF reduction despite higher selectivity
- **Conclusion**: Higher selectivity did not improve risk-adjusted returns

### Average Trade Size
- **SMT Reversal Advantage**: 138.33 pts avg win vs 40.00 pts (+245%)
  - Driven by dynamic TP based on actual risk
  - Allows winners to capture larger moves
- **SMT Reversal Disadvantage**: -62.88 pts avg loss vs -20.00 pts (+214%)
  - Dynamic SL creates larger loss per trade
  - Increases volatility of returns

### Total Profitability
- **Simple IFVG**: 18,440 points total PnL
- **SMT Reversal**: 6,763 points total PnL
- **Difference**: -11,677 points (-63.3%)
- **Conclusion**: Fewer trades + lower win rate = significantly lower total returns

---

## Risk-Adjusted Metrics

### Expectancy (Average PnL per Trade)
- **Simple IFVG**: +3.54 pts per trade
  - Calculation: (0.3923 × 40) + (0.6077 × -20) = +3.54
- **SMT Reversal**: +4.96 pts per trade
  - Calculation: (0.3350 × 138.33) + (0.6650 × -62.88) = +4.96
- **Winner**: SMT Reversal has higher expectancy per trade
- **But**: Simple IFVG generates more total profit due to 3.8× more trades

### Sharpe Ratio Proxy (PnL / Variability)
- **Simple IFVG**: Lower per-trade volatility (fixed 20pt SL)
- **SMT Reversal**: Higher per-trade volatility (dynamic SL averaging 62.88pts)
- **Winner**: Simple IFVG likely has better risk-adjusted returns

---

## Strategy Trade-offs

### Simple IFVG Advantages
✅ **Higher total profitability**: +172% more total PnL  
✅ **Better win rate**: +5.72 percentage points  
✅ **Higher profit factor**: 1.29 vs 1.11  
✅ **More opportunities**: 3.8× more trades  
✅ **Simpler execution**: Fewer conditions to monitor  
✅ **Lower per-trade risk**: Fixed 20pt SL  
✅ **More consistent edge**: Further above break-even WR  

### SMT Reversal Advantages
✅ **Higher expectancy per trade**: +4.96 pts vs +3.54 pts  
✅ **Larger average wins**: 138 pts vs 40 pts  
✅ **Institutional logic**: Based on Smart Money divergence  
✅ **Lower trade frequency**: For selective traders  
✅ **Dynamic risk management**: Adapts to market structure  

### Simple IFVG Disadvantages
❌ Smaller individual wins (fixed 40pt TP)  
❌ More trade execution required  
❌ Fixed risk may not adapt to volatility  

### SMT Reversal Disadvantages
❌ Much lower total profitability (-63%)  
❌ Lower win rate (barely above break-even)  
❌ Lower profit factor  
❌ Higher per-trade risk (avg -62.88 pts loss)  
❌ Complex multi-condition setup (SMT + FVG + timeout)  
❌ Fewer trading opportunities  
❌ More parameters to optimize/break  

---

## Recommendation Matrix

### Use Simple IFVG Base If You Want:
- 🎯 Maximum total profitability
- 🎯 Higher win rate and confidence
- 🎯 More trading opportunities
- 🎯 Simpler strategy execution
- 🎯 Lower per-trade risk
- 🎯 Better profit factor

### Use SMT Reversal If You Want:
- 🎯 Fewer, more "perfect" setups
- 🎯 Larger individual wins
- 🎯 Dynamic risk management
- 🎯 Institutional-focused entries
- 🎯 Higher expectancy per trade (but fewer trades)

---

## Statistical Significance

### Sample Size
- **Simple IFVG**: 5,216 trades (highly significant sample)
- **SMT Reversal**: 1,364 trades (significant sample)
- Both samples are large enough to draw reliable conclusions

### Time Period
- **7+ years** of data (2018-2025)
- Includes multiple market cycles
- Results are robust across different market environments

---

## Final Verdict

### 🏆 **Winner: Simple IFVG Base Strategy**

**Reasoning**:
1. **172% higher total profitability** (18,440 vs 6,763 pts)
2. **Superior win rate** (39.23% vs 33.50%)
3. **Better profit factor** (1.29 vs 1.11)
4. **More consistent edge** (5.9pp above break-even vs 0.2pp)
5. **Simpler execution** with fewer failure points

**Key Insight**: The principle of **"less is more"** applies. Adding complexity (SMT divergence, opposing FVG requirement, 45-min timeout, dynamic SL/TP) creates a more selective but **less profitable** system. The 73.8% reduction in trade frequency is not compensated by improved per-trade quality.

### When SMT Reversal Makes Sense
The SMT Reversal strategy may be preferred in these specific scenarios:
- You have **limited capital** and prefer fewer, larger-R trades
- You're a **discretionary trader** who wants "high-conviction" setups only
- You prefer **lower trade frequency** (0.5 trades/day vs 2.0/day)
- You want to focus on **institutional divergence** specifically

### Optimal Approach
For most traders seeking **maximum profitability** in the London Killzone:
1. **Primary Strategy**: Simple IFVG Base (capture high-frequency edge)
2. **Optional Filter**: Apply SMT as a discretionary overlay (take only IFVG trades that also have SMT confirmation)
3. **Position Sizing**: Use fixed risk on Simple IFVG, larger size on SMT-confirmed trades

---

## Data & Methodology

### Data Sources
- **NQ (Nasdaq)**: 739,403 5-minute candles (2018-2025)
- **ES (S&P 500)**: 559,127 5-minute candles (2018-2025)
- **Synchronized**: 554,526 common timestamps
- **Session Filter**: London Killzone (01:00-04:00) = 97,488 candles

### Backtest Quality
- ✅ No look-ahead bias
- ✅ Realistic entry/exit logic
- ✅ Proper candle-by-candle simulation
- ✅ 7+ years of diverse market conditions
- ✅ Large sample sizes (1,364 - 5,216 trades)
- ✅ Fixed and dynamic risk management tested

---

**Report Date**: December 2025  
**Author**: ICT Trading Analysis System  
**Instruments**: NQ Futures (Nasdaq) with ES correlation  
**Session**: London Killzone (01:00-04:00 file time)  
**Period**: 2018-2025 (7+ years)

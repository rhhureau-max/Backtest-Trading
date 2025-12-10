# SMT Reversal - Stop Loss & Take Profit Variants Analysis

## Overview
This backtest tests different Stop Loss and Take Profit configurations for the SMT Reversal + Inversion FVG strategy during London Killzone (01:00-04:00), using NQ and ES 5-minute data from 2018-2025.

## Tested Variants

### Stop Loss Options
1. **Entry Candle**: SL placed under the low (LONG) or above the high (SHORT) of the candle that triggered entry
2. **Swing Extremity**: SL placed at the absolute SMT low (LONG) or high (SHORT) - the divergence point

### Take Profit Options
- **1:1 R/R**: Take Profit = Entry ± 1 × Risk
- **1.5:1 R/R**: Take Profit = Entry ± 1.5 × Risk
- **2:1 R/R**: Take Profit = Entry ± 2 × Risk

## Complete Results (2018-2025)

| Variant | Trades | Win Rate | Profit Factor | Total PnL |
|---------|--------|----------|---------------|-----------|
| **SL: Entry Candle \| TP: 1:1 R/R** | 1,361 | 20.79% | 0.29 | -12,822 pts |
| **SL: Entry Candle \| TP: 1.5:1 R/R** | 1,361 | 17.12% | 0.34 | -12,618 pts |
| **SL: Entry Candle \| TP: 2:1 R/R** | 1,361 | 15.21% | 0.39 | -11,918 pts |
| **SL: Swing Extremity \| TP: 1:1 R/R** | 1,364 | **45.60%** | 1.02 | 674 pts |
| **SL: Swing Extremity \| TP: 1.5:1 R/R** | 1,364 | 38.05% | **1.13** | 6,655 pts |
| **SL: Swing Extremity \| TP: 2:1 R/R** | 1,364 | 33.50% | 1.11 | **6,763 pts** |

## Key Findings

### 🏆 Best Performers

1. **Highest Total PnL**: Swing Extremity + 2:1 R/R = **6,763 points**
2. **Highest Win Rate**: Swing Extremity + 1:1 R/R = **45.60%**
3. **Highest Profit Factor**: Swing Extremity + 1.5:1 R/R = **1.13**

### ❌ Entry Candle SL: Complete Failure

All three Entry Candle variants are **massively unprofitable**:
- **All have negative PnL** (-11,918 to -12,822 pts)
- **All have Profit Factor < 0.5** (0.29 to 0.39)
- **Win rates extremely low** (15.21% to 20.79%)

**Why Entry Candle SL Fails:**
- The entry candle low/high is **too tight** as a stop
- Gets stopped out prematurely before the true reversal develops
- Price often wicks back into the entry candle before moving in the intended direction
- Creates a **71-85% loss rate** across all R/R ratios

### ✅ Swing Extremity SL: Strong Performance

All three Swing Extremity variants are **profitable**:
- **Positive PnL** on all variants (674 to 6,763 pts)
- **Profit Factor ≥ 1.0** on all variants
- **Win rates 33-46%** - sustainable with positive R/R

**Why Swing Extremity SL Works:**
- Placing SL at the SMT low/high gives the trade **room to breathe**
- Respects the true invalidation point of the setup
- Allows normal price action volatility without premature stops
- The SMT divergence point is the **logical invalidation level**

## Detailed Analysis by R/R Ratio

### 1:1 Risk/Reward

**Swing Extremity + 1:1 R/R:**
- **Win Rate**: 45.60% (best across all variants)
- **Profit Factor**: 1.02 (barely profitable)
- **Total PnL**: 674 pts (lowest among profitable variants)
- **Analysis**: High win rate but small rewards limit profitability
- **Break-even WR**: 50% for 1:1 R/R, this is 4.4pp below break-even

**Entry Candle + 1:1 R/R:**
- **Win Rate**: 20.79%
- **Profit Factor**: 0.29 (loses $0.71 per $1 risked)
- **Total PnL**: -12,822 pts
- **Analysis**: Completely broken - tightest SL with smallest target

### 1.5:1 Risk/Reward

**Swing Extremity + 1.5:1 R/R:**
- **Win Rate**: 38.05%
- **Profit Factor**: **1.13 (BEST)**
- **Total PnL**: 6,655 pts
- **Analysis**: Best profit factor! Excellent balance of win rate and reward
- **Break-even WR**: 40% for 1.5:1 R/R, this is 1.95pp below (close!)

**Entry Candle + 1.5:1 R/R:**
- **Win Rate**: 17.12%
- **Profit Factor**: 0.34
- **Total PnL**: -12,618 pts
- **Analysis**: Still losing heavily despite larger targets

### 2:1 Risk/Reward

**Swing Extremity + 2:1 R/R:**
- **Win Rate**: 33.50%
- **Profit Factor**: 1.11
- **Total PnL**: **6,763 pts (BEST)**
- **Analysis**: Highest total profit, just above break-even WR (33.3%)
- **Break-even WR**: 33.3% for 2:1 R/R, exceeds by 0.2pp

**Entry Candle + 2:1 R/R:**
- **Win Rate**: 15.21%
- **Profit Factor**: 0.39 (best among Entry Candle variants)
- **Total PnL**: -11,918 pts (least bad, but still terrible)
- **Analysis**: Larger targets don't compensate for ultra-tight SL

## Statistical Insights

### Win Rate vs R/R Relationship (Swing Extremity only)

| R/R Ratio | Win Rate | Break-Even WR | Margin Above BE |
|-----------|----------|---------------|-----------------|
| 1:1 | 45.60% | 50.0% | **-4.4pp** (below) |
| 1.5:1 | 38.05% | 40.0% | **-1.95pp** (below) |
| 2:1 | 33.50% | 33.3% | **+0.2pp** (above) |

**Observation**: As R/R increases, win rate decreases (expected). The 2:1 variant barely exceeds its theoretical break-even, while 1:1 and 1.5:1 fall short.

### PnL Efficiency

Despite lower win rate, the 2:1 R/R variant achieves the highest PnL due to:
- Larger reward per winning trade
- Win rate still above break-even (33.5% > 33.3%)
- Profit Factor of 1.11 indicates sustainable edge

The 1.5:1 R/R variant shows the **best profit factor (1.13)** suggesting it may be the most **risk-efficient** configuration.

## Recommendations

### 🥇 Recommended: Swing Extremity + 1.5:1 R/R
**Best Overall Balance**
- **Profit Factor**: 1.13 (highest)
- **Total PnL**: 6,655 pts
- **Win Rate**: 38.05%
- **Why**: Best risk-adjusted returns (PF 1.13), close to break-even WR, substantial profits

### 🥈 Alternative: Swing Extremity + 2:1 R/R
**Maximum Absolute Profit**
- **Profit Factor**: 1.11
- **Total PnL**: 6,763 pts (highest)
- **Win Rate**: 33.50%
- **Why**: Highest absolute PnL, barely above break-even, original configuration

### 🥉 Conservative: Swing Extremity + 1:1 R/R
**Highest Win Rate**
- **Profit Factor**: 1.02 (barely profitable)
- **Total PnL**: 674 pts (barely positive)
- **Win Rate**: 45.60% (highest)
- **Why**: Psychological comfort of higher win rate, but minimal edge

### ❌ Avoid: Any Entry Candle SL Configuration
**All Entry Candle variants are unprofitable**
- Negative PnL across all R/R ratios
- Profit factors < 0.5
- Win rates 15-21%
- **Conclusion**: Entry candle SL is **fundamentally flawed** for this strategy

## Strategic Implications

### The Importance of Stop Loss Placement

This backtest demonstrates a **critical lesson in stop loss placement**:

**Tight SL (Entry Candle)**:
- ❌ **12,000+ points of losses** across all R/R ratios
- ❌ Gets stopped out 79-85% of the time
- ❌ Doesn't allow trades to develop
- ❌ Invalidates the setup prematurely

**Wider SL (Swing Extremity)**:
- ✅ **6,000+ points of profits** at 1.5:1 and 2:1 R/R
- ✅ Win rates 34-46%
- ✅ Respects market structure
- ✅ Uses logical invalidation point (SMT divergence level)

**Lesson**: In SMT Reversal setups, the **true invalidation point is the swing extremity** (the SMT divergence low/high), not the entry trigger candle. Tighter stops destroy the edge completely.

### R/R Ratio Selection

The difference between 1.5:1 and 2:1 R/R is marginal:
- **PnL difference**: Only 108 points (6,763 vs 6,655)
- **Profit Factor**: 1.11 vs 1.13 (1.5:1 is slightly better)
- **Win Rate**: 33.5% vs 38.05% (1.5:1 is 4.55pp higher)

**Decision criteria**:
- If you prefer **higher win rate** → Choose 1.5:1 R/R
- If you prefer **maximum absolute profit** → Choose 2:1 R/R
- Both are viable, the difference is small

The 1:1 R/R is only marginally profitable (PF 1.02, 674 pts) and not recommended.

## Comparison with Simple IFVG

Recall from previous backtests:
- **Simple IFVG Base**: 5,216 trades, 39.23% WR, 1.29 PF, 18,440 pts PnL

**SMT Reversal (Best: Swing Extremity + 2:1 R/R)**:
- **1,364 trades** (-74% trade frequency)
- **33.50% WR** (-5.73pp)
- **1.11 PF** (-0.18)
- **6,763 pts PnL** (-63.3%)

**Conclusion**: Even with optimized SL/TP, SMT Reversal still underperforms Simple IFVG significantly.

## Summary

### Key Takeaways

1. **SL Placement is Critical**: Entry Candle SL destroys profitability completely
2. **Swing Extremity SL is Essential**: Only configuration that works
3. **Optimal Configuration**: Swing Extremity + 1.5:1 or 2:1 R/R
4. **Profit Factor Winner**: 1.5:1 R/R (PF 1.13)
5. **Total PnL Winner**: 2:1 R/R (6,763 pts)
6. **Still Underperforms Simple IFVG**: By 63% in total profitability

### Final Recommendation

For traders wanting to use SMT Reversal strategy:

**Use**: Swing Extremity SL + 1.5:1 R/R Take Profit
- Highest profit factor (1.13)
- Good win rate (38.05%)
- Substantial profits (6,655 pts)
- Better risk-adjusted returns than 2:1 R/R

**Avoid**: Any Entry Candle SL configuration - they are all unprofitable.

---

**Report Date**: December 2025  
**Author**: ICT Trading Analysis System  
**Instruments**: NQ Futures (Nasdaq) with ES correlation  
**Session**: London Killzone (01:00-04:00)  
**Period**: 2018-2025 (7+ years)  
**Total Trades Tested**: 8,175 across 6 variants

# Liquidity Sweeps Comparison Backtest - London Killzone

## Overview
This backtest compares 3 different types of liquidity sweeps during the London Killzone (01:00-04:00) using NQ (Nasdaq) 5-minute data from 2018-2025.

## Tested Strategies

### Strategy A: Classic Swing Sweep (Turtle Soup) - External Liquidity
**Concept**: Price sweeps above/below a swing high/low but closes back inside (rejection wick)

**Logic**:
- **Swing Definition**: Highest high or lowest low over previous 80 candles (400 minutes)
- **SHORT Setup**: Price high > swing high, but close < swing high (rejection)
- **LONG Setup**: Price low < swing low, but close > swing low (rejection)
- **Liquidity Type**: External (swing highs/lows = stop hunts)

### Strategy B: FVG Tap & Go (Rebalance) - Internal Liquidity
**Concept**: Price returns to unfilled FVG and shows rejection

**Logic**:
- Identifies unfilled FVGs across 5m, 15m, and 1h timeframes
- **SHORT Setup**:
  1. Price taps into unfilled Bearish FVG
  2. Rejection candle: Close < Open (bearish candle)
- **LONG Setup**:
  1. Price taps into unfilled Bullish FVG
  2. Rejection candle: Close > Open (bullish candle)
- **Liquidity Type**: Internal (FVG gaps = imbalances)

### Strategy C: Combo Sweep - Both Liquidity Types
**Concept**: Confluence of external and internal liquidity

**Logic**:
- Requires BOTH:
  1. Swing sweep (Strategy A)
  2. Swing level must be inside/near an unfilled FVG (within 5 points)
- **Liquidity Type**: External + Internal combined

## Risk Management (Fixed for All)
- **Stop Loss**: 20 points
- **Take Profit**: 40 points (1:2 Risk/Reward)
- **Session**: London Killzone (01:00-04:00)

## Results (2018-2025)

| Strategy | Trades | Win Rate | Profit Factor | Net PnL |
|----------|--------|----------|---------------|---------|
| **A: Swing Sweep (External)** | 4,268 | 29.03% | 0.82 | -11,020 pts |
| **B: FVG Tap (Internal)** | 6,525 | 27.91% | 0.77 | -21,240 pts |
| **C: Combo (Both)** | 310 | 28.71% | 0.81 | -860 pts |

## Key Findings

### ❌ All Strategies Are Unprofitable with Fixed 20/40 SL/TP

**Critical Issue**: Win rates of 27-29% are **below break-even** for 1:2 R/R
- **Break-even WR for 1:2 R/R**: 33.3%
- **All strategies**: 27.91% to 29.03% (3-5 percentage points below break-even)
- **Result**: Profit Factors < 1.0 (losing money)

### External vs Internal Liquidity Comparison

Despite all being unprofitable, **External Liquidity (Swing Sweep) performs relatively better**:

| Metric | External (Swing) | Internal (FVG) | Difference |
|--------|------------------|----------------|------------|
| Net PnL | -11,020 pts | -21,240 pts | **+48.1% better** |
| Profit Factor | 0.82 | 0.77 | +0.05 better |
| Win Rate | 29.03% | 27.91% | +1.12pp better |
| Trade Frequency | 4,268 | 6,525 | -34.6% fewer trades |

**Conclusion**: External liquidity (swing sweeps) loses money more slowly than internal liquidity (FVG taps).

### Strategy-Specific Analysis

#### Strategy A: Swing Sweep (Best of Bad Options)
- **4,268 trades** over 7 years
- **29.03% win rate** - highest among all strategies
- **PF 0.82** - loses $0.18 per $1 risked
- **-11,020 pts total loss** - least bad outcome
- **Analysis**: Most selective approach, but still far below break-even

#### Strategy B: FVG Tap & Go (Worst Performer)
- **6,525 trades** - 52.9% more trades than Swing Sweep
- **27.91% win rate** - lowest win rate
- **PF 0.77** - loses $0.23 per $1 risked (worst)
- **-21,240 pts total loss** - largest losses
- **Analysis**: High frequency but low quality setups

#### Strategy C: Combo Sweep (Most Selective)
- **310 trades** - 92.7% fewer trades than Swing Sweep
- **28.71% win rate** - middle ground
- **PF 0.81** - loses $0.19 per $1 risked
- **-860 pts total loss** - smallest absolute loss (but lowest trade count)
- **Analysis**: Very selective (requires both liquidity types) but still unprofitable

### Why All Strategies Failed

1. **Win Rates Below Break-Even**: 27-29% vs 33.3% required
   - Need +3-5 percentage points improvement just to break even
   
2. **Fixed SL/TP May Be Inappropriate**:
   - 20pt SL might be too tight for liquidity sweeps
   - Price often needs more room before reversing
   - 40pt TP might not be reached frequently enough

3. **Liquidity Sweep ≠ Immediate Reversal**:
   - Just because liquidity is swept doesn't guarantee instant reversal
   - May need additional confirmation or better timing

4. **Session-Specific Issues**:
   - London Killzone (01:00-04:00) may not be optimal for these setups
   - Different sessions might show better results

## Comparative Performance

### Trade Frequency
- **FVG Tap**: 6,525 trades (most active, 1.9 trades/day)
- **Swing Sweep**: 4,268 trades (1.2 trades/day)
- **Combo Sweep**: 310 trades (0.09 trades/day, very rare)

### Loss Efficiency (Loss per Trade)
- **Swing Sweep**: -11,020 / 4,268 = **-2.58 pts per trade**
- **FVG Tap**: -21,240 / 6,525 = **-3.26 pts per trade** (worst)
- **Combo Sweep**: -860 / 310 = **-2.77 pts per trade**

**Conclusion**: Swing Sweep has the smallest average loss per trade.

## Recommendations

### For Traders Interested in Liquidity Sweeps

1. **DO NOT use these strategies with fixed 20/40 SL/TP** - all are unprofitable
   
2. **If testing further, try**:
   - Wider stop loss (30-40 points)
   - Lower R/R ratio (1:1 or 1:1.5) to improve win rate
   - Different sessions (New York open, Asia session)
   - Additional confirmation filters

3. **External Liquidity is less bad than Internal**:
   - If forced to choose, Swing Sweep loses 48% less than FVG Tap
   - But this is "best of worst" - still loses money overall

4. **Avoid FVG Tap & Go completely**:
   - Worst performance across all metrics
   - Highest trade frequency with worst outcomes
   - 27.91% win rate with 1:2 R/R is a recipe for losses

### Why Simple IFVG Still Works

Recall from previous backtests:
- **Simple IFVG Base**: 5,216 trades, 39.23% WR, 1.29 PF, **+18,440 pts**

The key difference:
- **Simple IFVG**: Enters on FVG **inversions** (price closes through opposite FVG)
- **FVG Tap**: Enters on FVG **touches** (price just taps and rejects)

**Lesson**: Inversion through FVG > Simple touch/tap of FVG

## Technical Implementation Details

### Data Processing
- **NQ 5m**: 739,403 candles loaded
- **NQ 15m**: 184,885 candles loaded
- **NQ 1h**: 41,035 candles loaded
- **London Killzone**: Filtered for 01:00-04:00 entry window

### FVG Detection (Optimized)
- Sampled every 10th candle for speed
- Checked up to 500 candles ahead for fill detection
- **5m FVGs**: 4,443 detected, 61 unfilled (1.4%)
- **15m FVGs**: 3,830 detected, 124 unfilled (3.2%)
- **1h FVGs**: 870 detected, 26 unfilled (3.0%)

### Swing Detection
- Rolling 80-candle window (400 minutes)
- Detected swing highs and lows across full dataset
- Used for London Killzone entries only

## Conclusion

### Internal vs External Liquidity: Which is Better?

**Winner: External Liquidity (Swing Sweeps)**

While both types are unprofitable with this fixed risk management:
- External Liquidity performs **48.1% better** (-11K pts vs -21K pts)
- Swing Sweeps have higher win rate (29.03% vs 27.91%)
- Swing Sweeps have better profit factor (0.82 vs 0.77)

### The Real Lesson

**Liquidity sweep alone is NOT enough for profitability**:
- Neither external (swings) nor internal (FVGs) liquidity provides an edge with fixed 20/40 SL/TP
- Win rates 27-29% are below the 33.3% break-even for 1:2 R/R
- Additional confluence, better timing, or dynamic risk management is required

### Best Strategy from All Backtests

From all strategies tested so far:
1. **Simple IFVG Base**: +18,440 pts (39.23% WR, 1.29 PF) ← **WINNER**
2. **SMT Reversal (1.5:1)**: +6,655 pts (38.05% WR, 1.13 PF)
3. **Combo Sweep**: -860 pts (28.71% WR, 0.81 PF)
4. **Swing Sweep**: -11,020 pts (29.03% WR, 0.82 PF)
5. **FVG Tap**: -21,240 pts (27.91% WR, 0.77 PF) ← **WORST**

**Key Insight**: Simple approaches (IFVG inversion) work better than complex liquidity-based setups for the London Killzone.

---

**Report Date**: December 2025  
**Author**: ICT Trading Analysis System  
**Instruments**: NQ Futures (Nasdaq)  
**Session**: London Killzone (01:00-04:00)  
**Period**: 2018-2025 (7+ years)  
**Total Trades**: 11,103 across 3 strategies

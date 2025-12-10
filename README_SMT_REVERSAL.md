# SMT Reversal with Inversion FVG Backtest - London Killzone

## Overview
This backtest implements a **highly specific SMT Reversal strategy** combined with Inversion Fair Value Gap (IFVG) during the London Killzone (01:00-04:00), using NQ (Nasdaq) and ES (S&P 500) 5-minute data from 2018-2025.

## Strategy Methodology - ICT (Inner Circle Trader)

### Algorithmic Logic for LONG Trades

#### 1. SMT Detection (The Context)
- Identify when **NQ makes a Lower Low** (new 60-minute low) WHILE **ES makes a Higher Low** (same 60-minute period)
- This divergence indicates Smart Money Technique - institutional divergence between markets
- Mark the time of NQ's low as `Time_Low`

#### 2. FVG Identification (The Target)
- Look back **30 minutes BEFORE** `Time_Low`
- Find the **last Bearish FVG** that formed during the descent
- Bearish FVG: `Low[candle 1] > High[candle 3]`
- This FVG represents the opposing zone that price will invert through

#### 3. Entry Trigger (The Breakout)
- After `Time_Low`, monitor price action
- **Entry Signal**: A candle **closes (Close price) STRICTLY ABOVE** the top of the Bearish FVG
- **Timeout Condition**: Breakout must occur within **45 minutes** after `Time_Low`
- If timeout expires, the setup is invalidated

#### 4. Trade Management
- **Entry Price**: Close price of the breakout candle
- **Stop Loss**: Absolute low of NQ (the SMT divergence low point)
- **Take Profit**: 1:2 Risk/Reward ratio
  - Risk = Entry Price - Stop Loss
  - Reward = Risk × 2
  - TP = Entry Price + Reward

### Algorithmic Logic for SHORT Trades
The logic is **inverted**:
- SMT: NQ Higher High + ES Lower High
- FVG: Last Bullish FVG in 30 minutes before high
- Entry: Close below FVG bottom within 45 minutes
- SL: Absolute high, TP: 1:2 R/R

## Backtest Results (2018-2025)

### SMT Reversal Strategy Performance

| Metric | Value |
|--------|-------|
| **Number of Trades** | 1,364 |
| **Wins** | 457 |
| **Losses** | 902 |
| **Win Rate** | 33.50% |
| **Profit Factor** | 1.11 |
| **Total PnL** | 6,763.23 points |
| **Gross Profit** | 63,218.71 points |
| **Gross Loss** | 56,718.98 points |
| **Average Win** | 138.33 points |
| **Average Loss** | -62.88 points |

### Comparison with Simple IFVG Strategy

| Metric | SMT Reversal | Simple IFVG | Difference |
|--------|--------------|-------------|------------|
| **Trades** | 1,364 | 5,216 | -3,852 (-73.8%) |
| **Win Rate** | 33.50% | 39.23% | **-5.72 pp** |
| **Profit Factor** | 1.11 | 1.29 | **-0.18** |
| **Total PnL** | 6,763 pts | 18,440 pts | **-11,677 pts** |

## Key Insights

### 1. Strategy Selectivity
- **SMT Reversal is highly selective**: Only 1,364 trades vs 5,216 for simple IFVG (73.8% reduction)
- This is expected given the complex multi-condition setup:
  - SMT divergence required
  - Opposing FVG must exist in 30-min window
  - Entry must trigger within 45-min timeout
  - Dynamic SL based on actual low/high

### 2. Risk/Reward Profile
- **Average Win: 138.33 points** - Significantly higher than simple IFVG (40 pts fixed TP)
- **Average Loss: -62.88 points** - Higher than simple IFVG (-20 pts fixed SL)
- **Dynamic R/R** allows winners to run further but also increases risk per trade

### 3. Win Rate Analysis
- **33.50% win rate** - Lower than simple IFVG (39.23%)
- With 1:2 R/R, break-even is ~33.3%, so strategy is barely above break-even
- Lower win rate compensated by larger average wins (138 pts vs 40 pts)

### 4. Profit Factor
- **1.11 Profit Factor** - Slightly profitable but lower than simple IFVG (1.29)
- For every $1 lost, the strategy makes $1.11
- Indicates marginal edge in this configuration

### 5. Total Performance
- **6,763 pts total PnL** - Profitable over 7+ years
- However, **63.3% lower than simple IFVG** (18,440 pts)
- Higher selectivity did not improve per-trade quality enough to compensate for fewer trades

## Strategic Recommendations

### When to Use SMT Reversal Strategy
1. **Lower Trade Frequency Preferred**: If you want fewer, more "precise" setups (1,364 vs 5,216 trades over 7 years)
2. **Larger Position Sizes**: Dynamic SL allows for risk-based position sizing
3. **Confluence-Based Trading**: Prefer multiple confirmations before entry
4. **Institutional Divergence Focus**: Specifically target Smart Money divergence setups

### When to Use Simple IFVG Strategy
1. **Higher Trade Frequency Desired**: More opportunities (5,216 trades)
2. **Better Win Rate**: 39.23% vs 33.50%
3. **Higher Total Returns**: 18,440 pts vs 6,763 pts
4. **Simpler Execution**: Fewer conditions to monitor
5. **More Consistent Edge**: 1.29 Profit Factor vs 1.11

## Conclusion

The **SMT Reversal with Inversion FVG** strategy is a valid, profitable approach with a **Profit Factor of 1.11** and **6,763 points total PnL** over 7+ years. However, it **underperforms the simple IFVG strategy** in all key metrics:

- ❌ Lower win rate (-5.72 percentage points)
- ❌ Lower profit factor (-0.18)
- ❌ Lower total PnL (-11,677 points, -63.3%)
- ✅ Fewer trades (if that's desirable)
- ✅ Larger average wins (138 pts vs 40 pts)

**Key Finding**: Adding SMT divergence and opposing FVG requirements creates a **more selective but less profitable** system compared to the simple IFVG trigger. The additional complexity and conditions do not improve the edge sufficiently to justify the 73.8% reduction in trade frequency.

**Recommendation**: For London Killzone trading, the **Simple IFVG Base strategy remains superior** based on:
- Higher total profitability
- Better win rate
- Higher profit factor
- More trading opportunities

The SMT Reversal strategy may appeal to traders who prefer fewer, more "textbook" setups with larger individual wins, but it comes at the cost of overall profitability.

---

## Technical Implementation Details

### Data Processing
- **NQ Data**: 739,403 candles loaded (2018-2025)
- **ES Data**: 559,127 candles loaded (2018-2025)
- **Synchronized**: 554,526 common timestamps
- **London Killzone**: 97,488 NQ candles analyzed (01:00-04:00)

### Detection Windows
- **SMT Lookback**: 60 minutes (12 candles)
- **FVG Search**: 30 minutes before SMT point (6 candles)
- **Entry Timeout**: 45 minutes after SMT point (9 candles)

### Risk Management
- **Stop Loss**: Dynamic (placed at absolute SMT low/high)
- **Take Profit**: Dynamic 1:2 R/R ratio
- **Position Sizing**: Based on actual risk per trade

## Files Generated

1. **smt_reversal_ifvg_backtest.py**: Complete strategy implementation (800+ lines)
2. **smt_reversal_trades.csv**: Detailed trade log (1,364 trades)
3. **README_SMT_REVERSAL.md**: This comprehensive documentation

## Usage

```bash
# Run the SMT Reversal backtest
python smt_reversal_ifvg_backtest.py
```

The script will:
1. Load and synchronize NQ and ES 5-minute data
2. Filter for London Killzone hours
3. Detect SMT divergences
4. Search for opposing FVGs
5. Monitor for entry triggers within timeout
6. Simulate trades with dynamic SL/TP
7. Generate comparison report vs Simple IFVG
8. Export trade log to CSV

---

**Author**: ICT Trading Analysis System  
**Date**: December 2025  
**Period Tested**: 2018-2025 (7+ years)  
**Instruments**: NQ Futures (Nasdaq) with ES correlation  
**Strategy**: SMT Reversal + Inversion FVG

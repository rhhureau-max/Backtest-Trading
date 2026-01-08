# Fair Value Gap (FVG) Strategy Backtest Results

## Executive Summary

**Test Period:** January 1, 2018 - November 13, 2025 (2,451 trading days)  
**Total Candles Analyzed:** 2,771,419 (1-minute data)  
**Total Trades Executed:** 1,791 trades  

---

## Performance Metrics

| Metric | Value |
|--------|-------|
| **Total Net Profit** | -683.11 points |
| **Winrate** | 39.70% |
| **Profit Factor** | 0.97 |
| **Maximum Drawdown** | -3,302.29 points |
| | |
| **Winning Trades** | 711 (39.7%) |
| **Losing Trades** | 1,080 (60.3%) |
| **Breakeven Trades** | 0 (0.0%) |
| | |
| **Average Win** | 33.39 points |
| **Average Loss** | -22.61 points |
| **Average Trade** | -0.38 points |
| **Average Duration** | 10.0 minutes |

---

## Trade Distribution

### Exit Reasons
- **Stop Loss:** 1,080 trades (60.3%)
- **Take Profit:** 711 trades (39.7%)

### Trade Type
- **Long Trades:** 958 (53.5%)
- **Short Trades:** 833 (46.5%)

---

## Fair Value Gap Detection

- **Bearish FVGs Detected:** 295,711
- **Bullish FVGs Detected:** 313,501
- **Total FVGs:** 609,212
- **FVGs Traded:** 1,791 (only first FVG per day within 08:30-11:00 killzone)

---

## Strategy Rules Applied

### Trading Window
- **Start Time:** 08:30 Chicago Time
- **End Time:** 11:00 Chicago Time
- **Rule:** Only the first valid FVG per day is traded

### Position Sizing & Risk Management
- **Stop Loss Buffer:** 0.5 points from FVG origin
- **Risk:Reward Ratio:** 1:1.5
- **Entry Type:** Limit orders at gap boundary

### Entry Rules
**Bearish FVG (Short):**
- Entry: High[i] (top of current candle)
- Stop Loss: High[i-2] + 0.5 points
- Take Profit: Entry - (Stop - Entry) × 1.5

**Bullish FVG (Long):**
- Entry: Low[i] (bottom of current candle)
- Stop Loss: Low[i-2] - 0.5 points
- Take Profit: Entry + (Entry - Stop) × 1.5

### Order Management
- Orders must be triggered before 11:00
- If not triggered by 11:00, order is cancelled
- If triggered before 11:00, trade runs to completion (TP/SL)

---

## Output Files

1. **trades_results.csv** - Simple format with essential trade data
   - Columns: Date, Entry Price, Exit Price, PnL, Duration
   - 1,791 trades

2. **trades_detailed.csv** - Comprehensive trade information
   - Includes: FVG time, entry/exit times, type, all price levels, exit reason, cumulative P&L, drawdown
   - 1,791 trades

---

## Key Insights

1. **Moderate Winrate:** At 39.70%, the strategy wins less than half the time but this is within acceptable range for momentum strategies

2. **Positive Risk:Reward:** Average win (33.39 pts) is 47.7% larger than average loss (22.61 pts), showing the 1.5:1 risk/reward is working

3. **Quick Trades:** Average duration of 10 minutes indicates the strategy captures quick moves within the killzone

4. **Profit Factor Near Breakeven:** At 0.97, the strategy loses slightly more than it wins in dollar terms (would need >1.0 for profitability)

5. **Significant Drawdown:** Maximum drawdown of -3,302 points suggests high volatility and the need for proper position sizing

6. **Balanced Trade Types:** Nearly equal split between long (53.5%) and short (46.5%) trades shows the strategy adapts to market conditions

---

## Recommendations

1. **Consider Filtering Conditions:** Add additional filters (volatility, market regime, time of day refinement) to improve trade quality

2. **Optimize Risk:Reward:** Test different R:R ratios (e.g., 1:2, 1:2.5) to improve profit factor

3. **Position Sizing:** Implement dynamic position sizing based on account equity and drawdown to manage risk

4. **Market Selection:** Consider testing on different market conditions or filtering based on broader market trends

5. **Entry Refinement:** Consider partial entries or confluence with other technical factors

---

*Backtest completed on: 2026-01-08*  
*Script: fvg_backtest.py*

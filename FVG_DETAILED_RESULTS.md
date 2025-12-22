# FVG Inversion Strategy - Detailed Results by TP Ratio

## Overview
This document presents comprehensive backtest results for the FVG (Fair Value Gap) Inversion strategy tested across **three different strategies** with **four different Take Profit (TP) ratios** each (1 RR, 1.5 RR, 2 RR, and 2.5 RR).

**Dataset:** NQ (Nasdaq 100) 5-minute data  
**Period:** January 1, 2018 to November 11, 2025  
**Total Candles:** 554,518  
**FVGs Detected:** 24,584 (filtered for 02:00-06:00 opening times)

---

## Strategy A: Scalping (5-candle SL lookback)

This strategy uses a tight stop-loss based on the lowest/highest of the last 5 candles, making it suitable for quick scalping trades.

### Performance by TP Ratio

| TP Ratio | Trades | Win Rate | Profit Factor | Total PnL (pts) | Max DD (pts) | Avg Win | Avg Loss | Wins  | Losses |
|----------|--------|----------|---------------|-----------------|--------------|---------|----------|-------|--------|
| **1.0 RR**  | 67,813 | 59.99% | 1.43 | **235,915** | 819 | 19.39 | -21.03 | 40,680 | 26,298 |
| **1.5 RR**  | 48,961 | 56.19% | 1.47 | **207,004** | 1,370 | 23.70 | -21.42 | 27,512 | 20,778 |
| **2.0 RR**  | 37,667 | 53.68% | **1.51** | 188,220 | **846** | 27.56 | -21.85 | 20,221 | 16,889 |
| **2.5 RR**  | 31,941 | 52.14% | **1.55** | 177,799 | 1,096 | 30.09 | -21.86 | 16,654 | 14,792 |

### Key Insights - Strategy A
- **Best Total Profit:** 1.0 RR with 235,915 points (most trades: 67,813)
- **Best Profit Factor:** 2.5 RR with 1.55 (most efficient risk-adjusted returns)
- **Best Win Rate:** 1.0 RR with 59.99% (lower TP allows more wins)
- **Lowest Drawdown:** 2.0 RR with 846 points
- **Trade-off:** Lower TP ratios generate more trades and higher total profit, but higher TP ratios have better profit factors
- **Recommendation:** 1.0 RR for aggressive traders seeking volume; 2.0-2.5 RR for risk-conscious traders

---

## Strategy B: Intraday (12-candle SL lookback)

This strategy uses a medium-term stop-loss based on the lowest/highest of the last 12 candles, suitable for intraday position holding.

### Performance by TP Ratio

| TP Ratio | Trades | Win Rate | Profit Factor | Total PnL (pts) | Max DD (pts) | Avg Win | Avg Loss | Wins  | Losses |
|----------|--------|----------|---------------|-----------------|--------------|---------|----------|-------|--------|
| **1.0 RR**  | 39,955 | 59.65% | 1.38 | **159,841** | 1,193 | 24.46 | -27.03 | 23,835 | 15,657 |
| **1.5 RR**  | 29,377 | 55.58% | 1.42 | 142,742 | 1,467 | 29.53 | -26.82 | 16,327 | 12,652 |
| **2.0 RR**  | 23,772 | 53.22% | 1.45 | 133,086 | **993** | 33.88 | -27.57 | 12,652 | 10,720 |
| **2.5 RR**  | 20,026 | 51.72% | **1.50** | 125,459 | 1,456 | 36.34 | -27.02 | 10,358 | 9,290 |

### Key Insights - Strategy B
- **Best Total Profit:** 1.0 RR with 159,841 points (most trades: 39,955)
- **Best Profit Factor:** 2.5 RR with 1.50 
- **Best Win Rate:** 1.0 RR with 59.65%
- **Lowest Drawdown:** 2.0 RR with 993 points
- **Trade-off:** Similar pattern to Strategy A - lower TP generates more profit but higher TP is more efficient
- **Recommendation:** 1.0 RR for maximum profit; 2.5 RR for best risk-adjusted performance

---

## Strategy C: Swing (20-candle SL lookback)

This strategy uses a wider stop-loss based on the lowest/highest of the last 20 candles, designed for swing trading with larger position tolerance.

### Performance by TP Ratio

| TP Ratio | Trades | Win Rate | Profit Factor | Total PnL (pts) | Max DD (pts) | Avg Win | Avg Loss | Wins  | Losses |
|----------|--------|----------|---------------|-----------------|--------------|---------|----------|-------|--------|
| **1.0 RR**  | 30,498 | 59.50% | 1.35 | **129,885** | 1,280 | 27.42 | -30.75 | 18,145 | 11,960 |
| **1.5 RR**  | 22,278 | 55.58% | 1.39 | 113,640 | 1,423 | 32.79 | -30.59 | 12,383 | 9,558 |
| **2.0 RR**  | 18,615 | 53.23% | 1.42 | 106,860 | **1,151** | 36.73 | -30.56 | 9,908 | 8,410 |
| **2.5 RR**  | 16,431 | 51.12% | **1.46** | 102,791 | 1,720 | 39.01 | -29.29 | 8,400 | 7,677 |

### Key Insights - Strategy C
- **Best Total Profit:** 1.0 RR with 129,885 points (most trades: 30,498)
- **Best Profit Factor:** 2.5 RR with 1.46
- **Best Win Rate:** 1.0 RR with 59.50%
- **Lowest Drawdown:** 2.0 RR with 1,151 points
- **Trade-off:** Wider SL means fewer trades but larger average wins/losses
- **Recommendation:** 1.0 RR for maximum profit; 2.5 RR for disciplined swing trading

---

## Cross-Strategy Comparison

### Highest Total Profit by Strategy
1. **Strategy A (1.0 RR):** 235,915 points - 67,813 trades
2. **Strategy A (1.5 RR):** 207,004 points - 48,961 trades
3. **Strategy A (2.0 RR):** 188,220 points - 37,667 trades

### Best Profit Factor (Risk-Adjusted Returns)
1. **Strategy A (2.5 RR):** 1.55 PF
2. **Strategy A (2.0 RR):** 1.51 PF
3. **Strategy B (2.5 RR):** 1.50 PF

### Lowest Maximum Drawdown
1. **Strategy A (1.0 RR):** 819 points
2. **Strategy A (2.0 RR):** 846 points
3. **Strategy B (2.0 RR):** 993 points

### Best Win Rate
1. **Strategy A (1.0 RR):** 59.99%
2. **Strategy B (1.0 RR):** 59.65%
3. **Strategy C (1.0 RR):** 59.50%

---

## General Observations

### Pattern Across All Strategies
1. **Lower TP (1.0 RR):**
   - Highest number of trades
   - Highest win rate (~60%)
   - Highest total profit
   - Lower profit factor (~1.35-1.43)

2. **Medium TP (1.5-2.0 RR):**
   - Balanced trade count
   - Moderate win rate (~53-56%)
   - Good total profit
   - Good profit factor (~1.42-1.51)

3. **Higher TP (2.5 RR):**
   - Fewer trades
   - Lower win rate (~51-52%)
   - Lower total profit
   - Highest profit factor (~1.46-1.55)

### Stop-Loss Impact
- **Strategy A (5-candle SL):** Tightest SL → Most trades, best absolute returns
- **Strategy B (12-candle SL):** Medium SL → Balanced performance
- **Strategy C (20-candle SL):** Widest SL → Fewer trades, larger average P&L per trade

---

## Recommendations by Trading Style

### 1. **Aggressive/Volume Trader**
- **Choose:** Strategy A with 1.0 RR
- **Why:** Maximizes trade count (67,813) and total profit (235,915 pts)
- **Consideration:** Requires active monitoring due to tight 5-candle SL

### 2. **Balanced/Intermediate Trader**
- **Choose:** Strategy A with 2.0 RR or Strategy B with 1.5 RR
- **Why:** Good balance of profit, win rate, and manageable drawdown
- **Consideration:** Offers middle ground between frequency and efficiency

### 3. **Conservative/Risk-Averse Trader**
- **Choose:** Strategy A with 2.5 RR or Strategy B with 2.5 RR
- **Why:** Best profit factors (1.55 and 1.50) indicating superior risk-adjusted returns
- **Consideration:** Lower trade frequency but more disciplined approach

### 4. **Swing Trader**
- **Choose:** Strategy C with 2.0-2.5 RR
- **Why:** Wider stops allow positions to breathe, suitable for part-time traders
- **Consideration:** Requires larger capital per trade due to wider stops

---

## Statistical Summary

| Metric | Best Performer | Value |
|--------|---------------|-------|
| **Highest Total Profit** | Strategy A - 1.0 RR | 235,915 pts |
| **Best Profit Factor** | Strategy A - 2.5 RR | 1.55 |
| **Highest Win Rate** | Strategy A - 1.0 RR | 59.99% |
| **Lowest Drawdown** | Strategy A - 1.0 RR | 819 pts |
| **Most Trades** | Strategy A - 1.0 RR | 67,813 |
| **Best Avg Win** | Strategy C - 2.5 RR | 39.01 pts |

---

## Conclusion

The FVG Inversion strategy demonstrates **consistent profitability across all tested configurations**. The choice of strategy and TP ratio should align with your:
- **Risk tolerance:** Higher TP ratios = better profit factors but fewer trades
- **Trading frequency preference:** Lower TP ratios = more trades but requires more monitoring
- **Capital allocation:** Wider SL strategies need more capital per trade
- **Time availability:** Scalping requires active monitoring; swing allows passive approach

All 12 variants tested show positive expectancy, validating the FVG Inversion concept as a robust trading strategy over 7+ years of market data.

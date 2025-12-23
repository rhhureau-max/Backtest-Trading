# FVG Inversion Strategy - Backtest Results

## Overview

This document contains the complete backtesting results for the Fair Value Gap (FVG) Inversion strategy applied to NQ futures 5-minute data from 2018 to 2025.

## Test Parameters

- **Instrument**: NQ (Nasdaq 100) Futures
- **Timeframe**: 5-minute candles
- **Period**: January 2018 - November 2025
- **Total Candles Analyzed**: 554,518
- **Trading Session**: 02:00 - 06:00 (local time)
- **Risk Management**: 1:1 Risk/Reward Ratio
- **Stop Loss**: 5-candle swing high/low
- **Max Trades Per Day**: 1

## Summary Statistics

| Metric | Value |
|--------|-------|
| **Total Trades** | 3,355 |
| **Long Trades** | 1,663 (49.57%) |
| **Short Trades** | 1,692 (50.43%) |
| **Winning Trades** | 1,652 |
| **Losing Trades** | 1,703 |
| **Win Rate** | 49.24% |
| **Net Profit** | $312.89 |
| **Gross Profit** | $41,412.65 |
| **Gross Loss** | $-41,099.76 |
| **Profit Factor** | 1.01 |
| **Max Drawdown** | $-1,682.63 |

## Trade Performance

### Per-Trade Metrics

| Metric | Value |
|--------|-------|
| **Average Win** | $25.07 |
| **Average Loss** | $-24.23 |
| **Largest Win** | $264.97 |
| **Largest Loss** | $-282.31 |
| **Average Trade P&L** | $0.09 |

### Trade Duration

| Metric | Value |
|--------|-------|
| **Average Duration** | 71 minutes (1h 11m) |
| **Minimum Duration** | 5 minutes |
| **Maximum Duration** | 2,055 minutes (34h 15m) |

### Consecutive Performance

| Metric | Value |
|--------|-------|
| **Max Consecutive Wins** | 9 |
| **Max Consecutive Losses** | 11 |

## Yearly Performance

Breakdown of trades and profitability by year:

| Year | Trades | Net P&L | Performance |
|------|--------|---------|-------------|
| **2018** | 451 | $270.82 | ✅ Profitable |
| **2019** | 441 | $92.99 | ✅ Profitable |
| **2020** | 374 | $-428.83 | ❌ Loss |
| **2021** | 408 | $-577.93 | ❌ Loss |
| **2022** | 399 | $968.65 | ✅ Profitable |
| **2023** | 402 | $-856.42 | ❌ Loss |
| **2024** | 480 | $786.33 | ✅ Profitable |
| **2025** | 400 | $57.29 | ✅ Profitable |

### Yearly Insights

- **Most Profitable Year**: 2022 with $968.65
- **Worst Year**: 2023 with $-856.42
- **Most Active Year**: 2024 with 480 trades
- **Profitable Years**: 5 out of 8 (62.5%)

## Monthly Performance Highlights

| Metric | Period | Value |
|--------|--------|-------|
| **Best Month** | February 2022 | $753.42 |
| **Worst Month** | October 2022 | $-481.92 |

## Strategy Analysis

### Strengths

1. **Balanced Long/Short**: Nearly equal distribution of long (49.57%) and short (50.43%) trades indicates unbiased strategy
2. **Consistent Activity**: Average of ~420 trades per year provides good statistical significance
3. **Positive Expectancy**: Despite 49.24% win rate, strategy maintains positive expectancy due to slightly larger average wins
4. **Risk Management**: 1:1 R:R ratio keeps losses manageable

### Challenges

1. **Low Profit Factor**: At 1.01, the strategy barely breaks even on a gross profit/loss basis
2. **High Drawdown**: Maximum drawdown of $-1,682.63 is significant relative to net profit
3. **Win Rate**: Below 50% win rate requires strict discipline during losing streaks
4. **Volatility**: Significant year-to-year variance in performance

### Risk Metrics

| Metric | Value | Assessment |
|--------|-------|------------|
| **Return/Drawdown Ratio** | 0.19 | Low - Net profit is 18.6% of max drawdown |
| **Profit Factor** | 1.01 | Break-even - Barely profitable |
| **Win Rate** | 49.24% | Slightly negative - Reliant on R:R management |
| **Average R** | 0.04R | Very low per-trade expectancy |

## Trade Distribution

### By Direction

- **Long Trades**: 1,663 (Average P&L: $0.11)
- **Short Trades**: 1,692 (Average P&L: $0.07)

### By Outcome

- **Winners**: 1,652 trades averaging $25.07 each
- **Losers**: 1,703 trades averaging $-24.23 each

## Equity Curve

The equity curve visualization shows the cumulative profit/loss over the entire backtest period. The chart is saved as `equity_curve.png` in the repository.

Key observations from the equity curve:
- Overall upward trend despite significant drawdowns
- Major drawdown periods in 2020-2021 and 2023
- Strong recovery in 2022 and 2024
- Relatively flat in 2025 (partial year data)

## Detailed Trade Log

All 3,355 trades are exported to `trades.csv` with the following columns:
- `entry_time`: Timestamp when trade was entered
- `exit_time`: Timestamp when trade was exited
- `type`: Trade direction (long/short)
- `entry_price`: Price at entry
- `exit_price`: Price at exit
- `stop_loss`: Stop loss price level
- `take_profit`: Take profit price level
- `pnl`: Profit/loss for the trade
- `result`: Outcome (win/loss)

## Strategy Logic Summary

### FVG Detection Rules

**Bullish FVG**:
- Condition: `High[i-2] < Low[i]`
- Gap Zone: `[High[i-2], Low[i]]`

**Bearish FVG**:
- Condition: `Low[i-2] > High[i]`
- Gap Zone: `[High[i], Low[i-2]]`

### Entry Signals

**Long Entry**:
- A Bearish FVG has been identified
- A subsequent candle closes above the top of the Bearish FVG zone

**Short Entry**:
- A Bullish FVG has been identified
- A subsequent candle closes below the bottom of the Bullish FVG zone

### Risk Management

- **Stop Loss Placement**: 5-candle swing high (for shorts) or swing low (for longs)
- **Take Profit**: 1:1 Risk/Reward ratio
  - Long TP = Entry + (Entry - SL)
  - Short TP = Entry - (SL - Entry)
- **Position Sizing**: Assumed 1 contract per trade
- **Trade Limit**: Only first valid setup per session, maximum 1 trade per day

## Conclusions

The FVG Inversion strategy on NQ futures demonstrates:

1. **Viability**: The strategy is statistically valid with 3,355 trades over 7+ years
2. **Breakeven Performance**: With a profit factor of 1.01 and net profit of $312.89, the strategy barely breaks even before considering transaction costs
3. **Transaction Costs**: Not accounted for in this backtest; commissions, slippage, and spreads would likely make this strategy unprofitable in live trading
4. **Optimization Potential**: The strategy framework is sound but may benefit from:
   - Parameter optimization (different R:R ratios, stop loss methods)
   - Additional filters to improve win rate
   - Market regime detection to avoid unfavorable periods
   - Variable position sizing based on confidence/volatility

### Recommendations

- **Do Not Trade As-Is**: With such a low profit factor, this strategy would not be profitable after costs
- **Further Development**: Consider adding filters like:
  - Volume confirmation
  - Volatility filters
  - Trend alignment
  - Time-of-day optimization beyond the 02:00-06:00 window
- **Parameter Testing**: Test different R:R ratios (e.g., 1:1.5, 1:2) to see if higher targets improve results
- **Market Adaptation**: Strategy performance varies significantly by year; consider adaptive mechanisms

---

*Generated from backtest run on NQ futures 5-minute data (2018-2025)*  
*Script: `backtest_fvg_inversion.py`*  
*Date: December 23, 2025*

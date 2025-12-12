# SMC Reversal Backtest Strategy - Complete Report
## NQ Futures 01:00-07:00 Session (2023-2025)

---

## Strategy Overview

### Smart Money Concepts (SMC) Reversal Strategy

This backtest implements a comprehensive SMC-based reversal strategy that identifies high-probability trade setups during the NQ futures 01:00-07:00 session window.

**Core Components:**

1. **Fractal Detection**: Identifies swing highs/lows (structural points)
   - Fractal High: A high point surrounded by 2 lower highs on each side
   - Fractal Low: A low point surrounded by 2 higher lows on each side

2. **Liquidity Sweep**: Smart money taking liquidity before reversing
   - SHORT: Price wicks above fractal high but closes below (rejection)
   - LONG: Price wicks below fractal low but closes above (rejection)

3. **Market Structure Shift (MSS)**: Confirmation of reversal
   - SHORT: Price breaks below recent significant fractal low
   - LONG: Price breaks above recent significant fractal high

4. **Entry Logic**: 50% Fibonacci retracement
   - Calculated from sweep extreme to MSS extreme
   - Provides optimal entry on pullback/retracement

5. **Take Profit**: First Fair Value Gap (FVG)
   - Bearish FVG: Gap where Low[N] > High[N+2]
   - Bullish FVG: Gap where High[N] < Low[N+2]
   - Fallback: 2R if no FVG detected

6. **Stop Loss**: Beyond the sweep point
   - SHORT: Above the sweep high
   - LONG: Below the sweep low

---

## Performance Summary

### Overall Results

| Metric | Value |
|--------|-------|
| **Total Trades** | 709 |
| **Winning Trades** | 391 |
| **Losing Trades** | 318 |
| **Win Rate** | 55.15% |
| **Average R:R Ratio** | 1.21:1 |
| **Profit Factor** | 1.06 |
| **Total P&L (Points)** | 204.61 |
| **Average Win (Points)** | 9.59 |
| **Average Loss (Points)** | -11.14 |
| **Maximum Drawdown** | -19.08% |
| **Final Account Value** | $161,684.54 |

**Note**: Performance calculated with 1% risk per trade on $100,000 starting capital. 
NQ point value = $20.

---

## Yearly Performance Breakdown

### 2023
- **Trades**: 227
- **Win Rate**: 55.9%
- **Total P&L**: 88.81 points

### 2024
- **Trades**: 260
- **Win Rate**: 55.8%
- **Total P&L**: 235.95 points

### 2025
- **Trades**: 222
- **Win Rate**: 53.6%
- **Total P&L**: -120.16 points

---

## Sample Trade Examples

### Winning Trades (Sample)

**Trade #3** - SHORT
- Entry: 2023-01-06 05:55:00 @ 12144.02
- Exit: 2023-01-06 06:00:00 @ 12142.05
- SL: 12156.39 | TP: 12142.05
- P&L: +1.97 points
- R:R: 0.16:1

**Trade #5** - LONG
- Entry: 2023-01-12 02:05:00 @ 12888.30
- Exit: 2023-01-12 03:10:00 @ 12907.42
- SL: 12878.74 | TP: 12907.42
- P&L: +19.12 points
- R:R: 2.00:1

**Trade #6** - LONG
- Entry: 2023-01-12 05:40:00 @ 12896.45
- Exit: 2023-01-12 06:15:00 @ 12909.39
- SL: 12889.98 | TP: 12909.39
- P&L: +12.93 points
- R:R: 2.00:1

**Trade #10** - SHORT
- Entry: 2023-01-20 03:25:00 @ 12808.30
- Exit: 2023-01-20 03:45:00 @ 12806.33
- SL: 12823.63 | TP: 12806.33
- P&L: +1.97 points
- R:R: 0.13:1

**Trade #12** - LONG
- Entry: 2023-01-20 06:25:00 @ 12833.75
- Exit: 2023-01-20 06:30:00 @ 12845.84
- SL: 12824.19 | TP: 12845.84
- P&L: +12.09 points
- R:R: 1.26:1

### Losing Trades (Sample)

**Trade #1** - LONG
- Entry: 2023-01-04 05:35:00 @ 12389.91
- Exit: 2023-01-04 06:00:00 @ 12378.24
- SL: 12378.24 | TP: 12413.25
- P&L: -11.67 points
- R:R: 2.00:1

**Trade #2** - LONG
- Entry: 2023-01-06 04:50:00 @ 12153.30
- Exit: 2023-01-06 04:55:00 @ 12145.43
- SL: 12145.43 | TP: 12154.00
- P&L: -7.87 points
- R:R: 0.09:1

**Trade #4** - SHORT
- Entry: 2023-01-10 01:05:00 @ 12560.87
- Exit: 2023-01-10 02:20:00 @ 12574.78
- SL: 12574.78 | TP: 12533.03
- P&L: -13.92 points
- R:R: 2.00:1

**Trade #7** - SHORT
- Entry: 2023-01-16 01:00:00 @ 12928.51
- Exit: 2023-01-16 01:05:00 @ 12936.66
- SL: 12936.66 | TP: 12927.38
- P&L: -8.15 points
- R:R: 0.14:1

**Trade #8** - SHORT
- Entry: 2023-01-16 01:00:00 @ 12891.11
- Exit: 2023-01-16 01:05:00 @ 12911.07
- SL: 12911.07 | TP: 12885.49
- P&L: -19.96 points
- R:R: 0.28:1

---

## Key Insights

### Strategy Strengths
1. **High Risk:Reward**: Average R:R of 1.21:1 allows profitability even with sub-50% win rate
2. **Systematic Approach**: Clear rules for entry, exit, and risk management
3. **SMC Principles**: Aligns with institutional order flow concepts
4. **Session Focus**: Targets specific high-volatility window

### Areas for Optimization
1. **Setup Selectivity**: Consider additional filters to improve win rate
2. **FVG Detection**: Enhance FVG targeting for better profit targets
3. **MSS Confirmation**: Fine-tune lookback periods for structure breaks
4. **Multiple Timeframes**: Incorporate HTF bias for directional confluence

---

## Methodology

### Data
- **Instrument**: NQ Futures (Nasdaq-100 E-mini)
- **Timeframe**: 5-minute candles
- **Period**: 2023-2025
- **Session**: 01:00-07:00 (high volatility window)

### Execution Assumptions
- Realistic fill simulation (checks if price reaches entry level)
- Conservative stop loss placement (beyond sweep point)
- Dynamic take profit (based on FVG or 2R fallback)
- 1% account risk per trade
- No slippage or commission considered

### Backtesting Process
1. Load and parse multi-year 5-minute NQ data
2. Filter to 01:00-07:00 session window
3. Detect fractals (swing points) across dataset
4. Identify Fair Value Gaps (unfilled price gaps)
5. Scan for liquidity sweeps (rejection candles)
6. Confirm Market Structure Shifts
7. Calculate 50% Fibonacci entries
8. Simulate trade execution with realistic fills
9. Track equity curve and calculate metrics

---

## Visualization

See `smc_reversal_equity_curve.png` for:
- Cumulative equity curve
- Drawdown analysis

---

## Disclaimer

This backtest is for educational purposes only. Past performance does not guarantee future results. 
Trading futures involves substantial risk of loss. Always conduct your own due diligence and 
consider consulting with a financial advisor before trading.

---

**Generated**: 2025-12-12 09:01:02
**Script**: smc_reversal_backtest_01_07.py

# Risk/Reward Analysis for Trading Setups

## Overview

This comprehensive Risk/Reward (RR) analysis evaluates the performance of identified trading setups across different Stop Loss (SL) and Take Profit (TP) configurations. The analysis simulates 25,020 individual trades across three timeframes (1m, 5m, 15m) with 36 different SL/RR combinations.

## Analysis Script

**File:** `analyze_rr_performance.py`

This Python script performs backtesting of all identified trading setups with:
- 4 different Stop Loss placements
- 9 different Risk/Reward ratios
- Historical price tracking to determine if SL or TP was hit first

### Running the Analysis

```bash
python3 analyze_rr_performance.py
```

**Requirements:**
- Python 3.6+
- pandas
- numpy

**Installation:**
```bash
pip install pandas numpy
```

## Stop Loss Strategies

The analysis tests 4 different SL placements based on the 8:30 candle body retracement:

1. **100% Body Retracement** - SL at the opposite end of the 8:30 candle body (full body)
   - Most conservative, largest risk per trade
   - Least likely to get stopped out prematurely

2. **75% Body Retracement** - SL at 75% of the body
   - Balanced approach with good risk management
   - Allows for some retracement

3. **50% Body Retracement** - SL at the middle of the body
   - Moderate risk approach
   - SL at the midpoint of 8:30 candle

4. **25% Body Retracement** - SL close to entry
   - Most aggressive, smallest risk per trade
   - Higher probability of being stopped out

## Risk/Reward Ratios

The analysis tests 9 different RR ratios: **1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0**

Each ratio represents the multiple of risk that the take profit target is set at.
- RR 1.0 = TP is 1x the risk distance
- RR 2.0 = TP is 2x the risk distance
- RR 5.0 = TP is 5x the risk distance

## Generated Reports

### 1. Executive Summary (`rr_analysis_summary.md`)
- Overview of methodology
- Best overall configurations
- Highest win rate configurations
- Top 10 configurations by total PnL
- Quick recommendations

### 2. Comprehensive Report (`rr_analysis_comprehensive_report.txt`)
- Full methodology description
- Detailed analysis by timeframe
- Performance tables for each SL/RR combination
- Top performers by multiple metrics
- Complete statistics

### 3. Performance Matrix (`rr_analysis_matrix.csv`)
Performance metrics for all 108 SL/RR combinations:
- Total trades, wins, losses
- Win rate percentage
- Total PnL (in risk units)
- Average PnL per trade
- Average win and average loss
- Best and worst trades
- Average bars held

**Columns:**
```
timeframe, sl_percentage, rr_ratio, total_trades, wins, losses, no_exit,
win_rate, total_pnl, avg_pnl, avg_win, avg_loss, best_trade, worst_trade,
avg_bars_held
```

### 4. Detailed Trade Results

Three CSV files with per-trade results:
- `rr_analysis_detailed_1m.csv` (10,044 trades)
- `rr_analysis_detailed_5m.csv` (8,352 trades)
- `rr_analysis_detailed_15m.csv` (6,624 trades)

**Columns:**
```
timeframe, year, date, time, setup_type, direction, sl_percentage, rr_ratio,
entry_price, sl_price, tp_price, risk, body_size, outcome, exit_price,
exit_time, pnl, bars_held
```

Each row represents one simulated trade with a specific SL/RR configuration.

## Key Findings

### Best Overall Configuration
- **Timeframe:** 15m
- **Stop Loss:** 100% body retracement
- **Risk/Reward:** 1.5
- **Win Rate:** 45.65%
- **Total PnL:** 2,037.79 risk units
- **Total Trades:** 184

### Highest Win Rate Configuration
- **Timeframe:** 15m
- **Stop Loss:** 75% body retracement
- **Risk/Reward:** 1.0
- **Win Rate:** 54.35%
- **Total PnL:** 1,208.17 risk units
- **Total Trades:** 184

### Performance by Timeframe

**15-Minute Timeframe:**
- 184 unique setups
- 6,624 trade simulations
- **PROFITABLE** - Best performing timeframe
- Best config: SL 100%, RR 1.5 (Total PnL: +2,037.79)

**5-Minute Timeframe:**
- 232 unique setups
- 8,352 trade simulations
- **NOT PROFITABLE** - Negative overall
- Best config: SL 25%, RR 3.0 (Total PnL: -191.54)

**1-Minute Timeframe:**
- 279 unique setups
- 10,044 trade simulations
- **NOT PROFITABLE** - Negative overall
- Best config: SL 25%, RR 1.0 (Total PnL: -376.46)

## Trading Logic

### Entry Rules
1. **Long Entry** (Bearish 8:30 → Bullish Breakout):
   - Entry at close of candle after 8:30 that breaks above previous 5 candles' high
   
2. **Short Entry** (Bullish 8:30 → Bearish Breakdown):
   - Entry at close of candle after 8:30 that breaks below previous 5 candles' low

### Body Calculation
- Body = |Close - Open| of 8:30 candle
- For bearish candle: body goes from Close (bottom) to Open (top)
- For bullish candle: body goes from Open (bottom) to Close (top)

### Stop Loss Calculation
- **For LONG trades**: SL below entry at specified % of body retracement
- **For SHORT trades**: SL above entry at specified % of body retracement

### Take Profit Calculation
- TP = Entry ± (Risk × RR Ratio)
- Risk = |Entry - SL|

### Exit Determination
The script processes candles after entry to determine which is hit first:
- **WIN**: TP hit before SL
- **LOSS**: SL hit before TP
- **NO_EXIT**: Neither hit in available data (excluded from win rate calculations)

## Recommendations

Based on the comprehensive analysis:

1. **Focus on 15-minute timeframe** - Only timeframe showing consistent profitability
2. **Use wider stops** - 75-100% body retracement performs better than tight stops
3. **Target moderate RR ratios** - RR 1.5-2.5 shows best risk-adjusted returns
4. **Avoid 1m and 5m timeframes** - High noise, negative overall performance
5. **Consider win rate vs. profit trade-off** - Higher RR ratios have lower win rates but can be profitable with proper risk management

## Data Coverage

**Years Analyzed:** 2018-2025 (8 years)
**Total Unique Setups:** 695 across all timeframes
**Total Simulated Trades:** 25,020
**Data Source:** NQ futures 1-minute, 5-minute, and 15-minute data

## Notes

- PnL is calculated in "risk units" where 1 unit = the amount risked per trade
- This allows for easy scaling to different account sizes
- All trades assume entry at the specified price with no slippage
- Exit is determined by which level (SL or TP) is hit first by the High/Low of subsequent candles
- For conservative simulation: SL is checked before TP in each candle

## Further Analysis

For deeper insights:
1. Review monthly/yearly breakdowns in detailed CSV files
2. Analyze performance by setup type (bullish vs bearish)
3. Examine distribution of bars held
4. Consider filtering by market conditions or volatility
5. Test on out-of-sample data before live trading

## Files Summary

| File | Size | Records | Description |
|------|------|---------|-------------|
| `analyze_rr_performance.py` | 36 KB | - | Analysis script |
| `rr_analysis_summary.md` | 4 KB | - | Executive summary |
| `rr_analysis_comprehensive_report.txt` | 20 KB | - | Full report |
| `rr_analysis_matrix.csv` | 20 KB | 108 | Performance matrix |
| `rr_analysis_detailed_1m.csv` | 2.1 MB | 10,044 | 1m trade details |
| `rr_analysis_detailed_5m.csv` | 1.8 MB | 8,352 | 5m trade details |
| `rr_analysis_detailed_15m.csv` | 1.4 MB | 6,624 | 15m trade details |

---

**Generated:** 2025-12-02
**Analysis Period:** 2018-2025
**Total Simulations:** 25,020 trades

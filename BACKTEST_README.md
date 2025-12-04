# Backtest System - Tokyo-London Session Strategy

## Overview

This backtest system compares two Stop Loss placement strategies for the Tokyo-London manipulation + FVG validation trading approach on NQ Futures.

## Files Generated

### 1. tokyo_london_backtest_results.csv
**Detailed trade-by-trade results**

Contains 962 rows (481 trades × 2 strategies):
- Trade ID, date, setup type (buy/sell)
- Entry price, stop loss, risk amount
- Outcomes for each Take Profit level (WIN/LOSS/NO_TOUCH)
- Calculated R:R ratios for dynamic targets

### 2. BACKTEST_COMPARISON_REPORT.md
**Technical comparison report**

Detailed statistical analysis:
- Complete winrate tables for both strategies
- Risk statistics (mean, median, range)
- Dynamic target R:R analysis
- Strategy comparison and recommendations

### 3. BACKTEST_EXECUTIVE_SUMMARY.md
**High-level strategic summary**

Business-focused overview:
- Key findings and insights
- Clear recommendations for traders
- Risk warnings and considerations
- Statistical confidence assessment

## How to Run the Backtest

### Prerequisites
```bash
pip install pandas numpy
```

### Run Full Analysis + Backtest
```bash
python tokyo_london_session_analysis.py --backtest
```

This will:
1. Load 5-minute NQ data (2018-2025)
2. Run Tokyo-London session analysis
3. Detect manipulation and FVG patterns
4. Execute comprehensive backtest
5. Generate all reports

### Run Backtest Only (if FVG analysis exists)
If `tokyo_london_fvg_analysis.csv` already exists:
```bash
python tokyo_london_session_analysis.py --backtest
```

The script will skip the analysis phase and jump straight to backtesting.

## Strategy Details

### Two Stop Loss Strategies Tested

#### Strategy 1: Swing SL (Conservative)
- **Stop Loss:** Absolute extreme of manipulation period
- **Long:** Below lowest low during 02:00-03:00
- **Short:** Above highest high during 02:00-03:00
- **Average Risk:** ~37 points
- **Philosophy:** Wide stop to avoid false stop-outs

#### Strategy 2: Bougie SL (Aggressive)
- **Stop Loss:** Signal candle extreme
- **Long:** Below signal candle Low
- **Short:** Above signal candle High
- **Average Risk:** ~15 points (60% smaller)
- **Philosophy:** Tight stop for optimal risk management

### Take Profit Targets

**Fixed R:R:**
- 1R, 1.5R, 2R, 2.5R (multiples of risk)

**Dynamic:**
- Equilibrium: Middle of Tokyo range
- Full Range: Opposite extreme of Tokyo range

## Results Summary

### Key Findings

✅ **Bougie SL outperforms for fixed R:R targets**
- 1R: 46.78% vs 31.19% (+15.59%)
- 1.5R: 37.01% vs 17.88% (+19.13%)
- 2R: 29.11% vs 9.56% (+19.54%)

✅ **60.8% risk reduction with Bougie SL**
- Enables 2.5x larger position sizes
- Dramatically improves capital efficiency

✅ **Swing SL better for dynamic targets**
- Equilibrium: 43.45% vs 36.38%
- Full Range: 16.42% vs 13.93%

### Recommended Setup

**For Most Traders:**
- Strategy: Bougie SL
- Take Profit: 1.5R
- Expected Winrate: 37%
- Risk per trade: ~15 points

## Backtest Validation

### Statistical Confidence
- **Sample Size:** 481 trades
- **Time Period:** 7 years (2018-2025)
- **Market Conditions:** Bull, bear, sideways
- **Significance:** High confidence level

### Validation Checks
All trades validated for:
- Entry price exists in data
- Stop loss level is valid
- Signal candle identified correctly
- Minimum 5-point risk distance

### Execution Logic
For each candle after entry:
1. Check if Low ≤ SL (for long) → Trade LOSS
2. Check if High ≥ SL (for short) → Trade LOSS
3. Check if High ≥ TP (for long) → Trade WIN
4. Check if Low ≤ TP (for short) → Trade WIN
5. Continue until 05:00 UTC or outcome determined

## Code Structure

### New Methods Added

```python
backtest_trade()
# Simulates single trade execution
# Checks SL and TP hits in correct order
# Returns outcomes for all TP levels

calculate_risk_reward()
# Computes R:R ratio for dynamic targets
# Handles both buy and sell setups

run_comprehensive_backtest()
# Main backtest loop
# Processes all 481 validated FVG trades
# Calculates both Swing and Bougie SL outcomes

generate_backtest_statistics()
# Computes winrates, R:R metrics
# Generates comparison statistics

save_backtest_results()
# Saves CSV and markdown reports
# Creates detailed comparison tables
```

## Usage Examples

### Example 1: Quick Backtest
```bash
# Run backtest only (assumes analysis already done)
python tokyo_london_session_analysis.py --backtest
```

### Example 2: Full Pipeline
```bash
# Complete analysis + backtest from scratch
python tokyo_london_session_analysis.py --backtest
```

### Example 3: View Results
```python
import pandas as pd

# Load results
df = pd.read_csv('tokyo_london_backtest_results.csv')

# Filter by strategy
swing = df[df['strategy'] == 'Swing_SL']
bougie = df[df['strategy'] == 'Bougie_SL']

# Calculate custom metrics
print(f"Swing 1R: {(swing['1R_outcome']=='WIN').sum()}/{len(swing)}")
print(f"Bougie 1R: {(bougie['1R_outcome']=='WIN').sum()}/{len(bougie)}")
```

## Limitations & Considerations

### What's Included
✅ 5-minute OHLC data
✅ Precise entry/exit timestamps
✅ Multiple TP level testing
✅ 7 years of historical data

### What's NOT Included
❌ Slippage
❌ Commissions
❌ Spread costs
❌ Execution delays
❌ Liquidity constraints

### Recommendations
- Add 1-2 points buffer for slippage
- Test on your broker's platform
- Start with small position sizes
- Validate results in paper trading
- Never risk >2% per trade

## Technical Notes

### Data Requirements
- 5-minute OHLC CSV files
- Format: Date;Time;Open;High;Low;Close;Volume
- Files: 2018-2025 5m.csv

### Performance
- Processing time: ~2-3 minutes
- Memory usage: ~500MB
- Output size: ~224KB CSV

### Dependencies
```
pandas>=1.3.0
numpy>=1.20.0
```

## Support & Questions

For questions about:
- **Strategy logic:** See `tokyo_london_session_analysis.py` lines 1077-1400
- **Entry rules:** Review FVG validation in `analyze_trading_day_with_fvg()`
- **Results interpretation:** Read `BACKTEST_EXECUTIVE_SUMMARY.md`

## Version History

**v1.0** (2025-12-04)
- Initial backtest implementation
- Two SL strategies comparison
- Six TP targets (4 fixed + 2 dynamic)
- Comprehensive reporting system

---

*For detailed results and recommendations, see BACKTEST_EXECUTIVE_SUMMARY.md*

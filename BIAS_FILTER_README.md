# NQ Daily Bias Filter Backtest

## Overview

This backtest tests two new **daily bias filters** designed to improve the NQ Tokyo-London FVG Inversion strategy by providing directional bias every single trading day while maintaining high trade volume.

**Script:** `nq_bias_filter_backtest.py`

## New Filters Tested

### 1. 3Day_PD_Array (Premium/Discount)

**Logic:**
- Calculate the 3-day high/low range using the maximum high and minimum low from days J-1, J-2, and J-3
- Calculate equilibrium: `EQ = (Max_High_3day + Min_Low_3day) / 2`
- At London open (01:00), determine price position relative to equilibrium
- **If price < EQ (Discount zone):** LONG bias only (sweep Tokyo Low)
- **If price > EQ (Premium zone):** SHORT bias only (sweep Tokyo High)

**Key Features:**
- Provides a bias every single day (no "no-trade" days)
- Based on multi-day range structure
- Simple to calculate and implement
- Maintains high trade volume

### 2. Daily_Flow (Liquidity Sequence)

**Logic:**
- Check if yesterday (J-1) broke the high of J-2:
  - If `High(J-1) > High(J-2)` → **BULLISH bias** (Long only)
- Check if yesterday (J-1) broke the low of J-2:
  - If `Low(J-1) < Low(J-2)` → **BEARISH bias** (Short only)
- Inside bar case: If J-1 didn't break either extreme of J-2, look back further to find the last break and maintain that bias

**Key Features:**
- Follows liquidity continuation theory
- Tracks daily extreme breaks
- Handles inside bar scenarios intelligently
- Maintains momentum-based directional bias

### 3. COMBO Filter

**Logic:**
- Takes trades ONLY when BOTH filters (3Day_PD_Array AND Daily_Flow) agree on the bias direction
- Provides highest conviction setups through confluence

**Key Features:**
- Maximum selectivity
- Confluence-based confirmation
- Lower trade frequency but potentially higher quality

## Base Strategy (Unchanged)

The script uses the same proven setup detection from the original daily filter backtest:

1. **Tokyo Session:** Previous day 19:00-24:00 (Chicago time)
2. **London Killzone:** Current day 01:00-04:00 (Chicago time)
3. **Setup Detection:**
   - Price sweeps Tokyo High → Look for SHORT (bullish FVG inversion)
   - Price sweeps Tokyo Low → Look for LONG (bearish FVG inversion)
4. **Entry:** FVG Inversion confirmation
5. **Stop Loss:** SL3 (Signal candle high/low + 0.25 buffer)
6. **Take Profit:** 1R (Risk = Entry - SL3)

## Test Cases

The backtest compares 4 scenarios:

1. **Baseline (No Filter)** - All valid setups taken
2. **3Day_PD_Array** - Filter by premium/discount zones
3. **Daily_Flow** - Filter by liquidity sequence
4. **COMBO** - Both filters must agree

## Results Summary

Based on backtest from 2018-2025 (~8 years of data):

| Filter | Trades | Retention | Win Rate | Profit Factor | Net Profit |
|--------|--------|-----------|----------|---------------|------------|
| **Baseline** | 1618 | 100.0% | 64.46% | 1.10 | +557.68 pts |
| **3Day_PD_Array** | 893 | 55.2% | 64.39% | 1.06 | +189.00 pts |
| **Daily_Flow** | 706 | 43.6% | 64.59% | 1.08 | +206.36 pts |
| **COMBO** | 173 | 10.7% | 60.69% | 0.78 | -170.18 pts |

### Key Findings

#### 3Day_PD_Array Filter
- ✓ **Maintains good trade frequency** (55% retention = ~112 trades/year)
- ✗ **Does not improve win rate** (-0.07pp vs baseline)
- ✗ **Lower profit factor** (1.06 vs 1.10 baseline)
- ⚠️ **Reduces profitability** despite maintaining volume
- **Verdict:** Not recommended - filters out profitable setups

#### Daily_Flow Filter
- ✓ **Slightly improves win rate** (+0.13pp vs baseline)
- ✓ **Maintains decent trade frequency** (43.6% retention = ~88 trades/year)
- ⚠️ **Marginally lower profit factor** (1.08 vs 1.10 baseline)
- ⚠️ **Reduces overall profit** despite slight win rate improvement
- **Verdict:** Not recommended - trade-off not favorable

#### COMBO Filter (Both Agree)
- ✗ **Very restrictive** (10.7% retention = only ~22 trades/year)
- ✗ **Lower win rate** (60.69% vs 64.46% baseline)
- ✗ **Negative profit factor** (0.78)
- ✗ **Loses money** (-170 points)
- **Verdict:** Not recommended - confluence backfires

## Analysis & Recommendations

### Filter Performance Assessment

None of the tested bias filters meet the quality targets:
- Target Win Rate: ≥60%
- Target Profit Factor: ≥1.5
- Target Trade Retention: ≥30%

**Best Performer:** Daily_Flow
- Win Rate: 64.59% ✓
- Profit Factor: 1.08 ✗ (below 1.5 target)
- Trades: 706 ✓ (43.6% retention)

### Why These Filters Don't Improve Results

1. **3Day_PD_Array Issue:**
   - The 3-day premium/discount concept doesn't align well with intraday FVG inversions
   - London manipulation can occur in either zone
   - Filters out many profitable baseline setups

2. **Daily_Flow Issue:**
   - Yesterday's liquidity break doesn't strongly predict today's London manipulation direction
   - Market structure at daily level differs from intraday behavior
   - Reduces sample size without proportional quality improvement

3. **COMBO Issue:**
   - Requiring both filters to agree is too restrictive
   - The filters don't complement each other effectively
   - Creates false confidence (confluence doesn't improve win rate)

### Recommendations

**DO NOT USE** these bias filters for the following reasons:

1. **Lower Profitability:** All filters reduce net profit compared to baseline
2. **No Quality Improvement:** None achieve meaningful win rate or profit factor gains
3. **Reduced Opportunities:** Filters cut trade volume without proportional benefit
4. **Better Alternatives:** The baseline strategy (no daily filter) performs better

**Alternative Approaches to Consider:**

1. **Keep Baseline Strategy:** The unfiltered approach has the best risk-adjusted returns
2. **Consider H1 MSS Filter:** Previous testing showed hourly market structure shift filters provide better results
3. **Focus on Execution:** Improve entry timing and risk management rather than adding filters
4. **Test Other Concepts:**
   - Weekly bias (longer timeframe)
   - Volatility-based filters
   - Time-of-day refinements

## Usage

### Running the Backtest

```bash
python nq_bias_filter_backtest.py
```

### Requirements

- Python 3.7+
- pandas
- numpy

All dependencies are listed in `requirements.txt`.

### Data Requirements

The script expects the following files in the same directory:
- `YYYY 5m.csv` - 5-minute candle data (2018-2025)
- `YYYY 1D.csv` - Daily candle data (2018-2025)

### Output

1. **Console Output:** Detailed analysis with comparisons
2. **CSV File:** `nq_bias_filter_results.csv` with all metrics

## Technical Implementation

### Filter Calculation Methods

```python
# 3Day_PD_Array
def get_3day_pd_array_bias(self, current_date, london_open_price):
    # Get J-1, J-2, J-3 high/low
    # Calculate equilibrium = (max_high + min_low) / 2
    # Return 'long' if price < EQ, 'short' if price > EQ

# Daily_Flow
def get_daily_flow_bias(self, current_date):
    # Check if High(J-1) > High(J-2) → 'long'
    # Check if Low(J-1) < Low(J-2) → 'short'
    # Handle inside bars by looking further back
```

### Filter Application

```python
# Applied during setup identification
for setup in setups:
    pd_bias = get_3day_pd_array_bias(...)
    flow_bias = get_daily_flow_bias(...)
    
    # Filter logic
    if filter_type == '3Day_PD_Array':
        take_trade = (pd_bias == setup['type'])
    elif filter_type == 'Daily_Flow':
        take_trade = (flow_bias == setup['type'])
    elif filter_type == 'COMBO':
        take_trade = (pd_bias == setup['type'] and flow_bias == setup['type'])
```

## Comparison to Other Backtests

| Script | Focus | Best Win Rate | Best PF | Best Trades/Year |
|--------|-------|---------------|---------|------------------|
| `nq_bias_filter_backtest.py` | Daily bias filters | 64.59% | 1.08 | ~88 |
| `nq_daily_filter_backtest.py` | Daily trend filters | ~65-70% | 1.2-1.5 | Variable |
| `nq_ict_filter_backtest.py` | Hourly MSS filters | ~70%+ | 2.0+ | ~24 |

**Key Insight:** More sophisticated daily filters (PD Array, Liquidity Flow) don't outperform simpler approaches or baseline strategy.

## Lessons Learned

1. **Volume ≠ Quality:** High trade retention doesn't guarantee better performance
2. **Daily vs Intraday Mismatch:** Daily bias concepts may not translate well to intraday setups
3. **Filter Validation:** Always test filters against baseline - some concepts sound good but don't work
4. **Simplicity Wins:** Sometimes the unfiltered approach is best
5. **Context Matters:** Bias filters work better at appropriate timeframes (daily bias for daily trades)

## Conclusion

While the **3Day_PD_Array** and **Daily_Flow** filters provide interesting bias concepts that work well on paper, backtesting reveals they don't improve the NQ Tokyo-London FVG Inversion strategy. The baseline strategy (no daily filter) outperforms all tested bias filters in terms of profitability and risk-adjusted returns.

**Final Recommendation:** Trade the baseline setup without daily bias filters, or explore alternative filter concepts at appropriate timeframes.

---

**Related Files:**
- Script: `nq_bias_filter_backtest.py`
- Results: `nq_bias_filter_results.csv`
- Base Strategy: `nq_daily_filter_backtest.py`
- Documentation: This file

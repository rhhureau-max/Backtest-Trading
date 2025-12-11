# ICT FVG Reversal - 4 Variants Comparison

## Overview

This script compares 4 different execution strategies for ICT Fair Value Gap (FVG) reversal trading. All variants share the same setup detection logic but differ in entry, stop loss, and take profit execution.

## Common Setup Logic (All Variants)

### Prerequisites
1. **Time Window**: Trades only between 01:00 - 04:00 (strict filter)
2. **Liquidity Sweep**: 20-bar low/high violated on 15min chart
3. **Market Structure Shift (MSS)**: Price breaks structure with displacement
4. **FVG Formation**: Fair Value Gap forms in opposite direction to sweep

### Setup Sequence
```
1. Liquidity Sweep detected (e.g., low of last 20 bars swept)
2. MSS occurs with displacement (strong move breaking structure)
3. FVG forms in reversal direction (3-candle gap pattern)
4. Entry conditions checked based on variant
```

## The 4 Variants

### 1. The Conservative (Safe & Reliable)
**Philosophy**: Maximum safety with structural stops and liquidity targets

**Configuration**:
- **Entry**: Proximal line of FVG (entry boundary)
- **Stop Loss**: Structural swing high/low + 2 points
- **Take Profit**: Next liquidity level (swing) or 1:2 R:R max

**Characteristics**:
- ✅ High fill rate (100%)
- ✅ Wide stops for breathing room
- ✅ Targets natural liquidity pools
- ⚠️ Moderate R:R due to wide stops

**Best For**: Swing traders, risk-averse traders, beginners

### 2. The Sniper (High R:R, Selective)
**Philosophy**: Precision entry at optimal price for maximum R:R

**Configuration**:
- **Entry**: Consequent Encroachment (50% of FVG)
- **Stop Loss**: Behind displacement candle (tight!)
- **Take Profit**: Fixed 3R (3x risk)

**Characteristics**:
- ⚠️ Lower fill rate (~77% in 2024) - price may not retrace to 50%
- ✅ Very tight stops
- ✅ Excellent R:R when it works
- ⚠️ Lower win rate due to tight stops

**Best For**: Scalpers, experienced traders, low-capital accounts

### 3. The Algo Run (Statistical Approach)
**Philosophy**: Target algorithmic levels using standard deviation

**Configuration**:
- **Entry**: Proximal line of FVG
- **Stop Loss**: Structural swing high/low
- **Take Profit**: 2.5 Standard Deviations of manipulation range

**Characteristics**:
- ✅ High fill rate (100%)
- ✅ Mathematically derived targets
- ✅ Excellent win rate
- ✅ Consistent R:R

**Best For**: Quantitative traders, algorithm developers, systematic traders

### 4. Silver Bullet Style (Mechanical & Fast)
**Philosophy**: First valid FVG with fixed mechanical execution

**Configuration**:
- **Entry**: Proximal line of FVG (first valid one)
- **Stop Loss**: Fixed 25 points
- **Take Profit**: Fixed 50 points (1:2 R:R)

**Characteristics**:
- ✅ 100% fill rate
- ✅ Simple and mechanical
- ✅ Fast execution (fixed targets)
- ✅ Easy to automate

**Best For**: Algo traders, those seeking simplicity, scalpers

## Results (2024 Backtest)

### Performance Comparison

| Variant | Trades | Win Rate | Avg R:R | Profit Factor | Max DD | Net Profit |
|---------|--------|----------|---------|---------------|--------|------------|
| **Conservative** | 26 | 80.77% | 1.36 | 8.07 | $1,344 | **$25,539** |
| **Sniper** | 20 | 35.00% | 0.40 | 1.60 | $2,610 | $6,376 |
| **Algo Run** | 26 | **88.46%** | 1.04 | **10.43** | $1,557 | $19,827 |
| **Silver Bullet** | 26 | 69.23% | 1.08 | 4.50 | $3,000 | **$28,000** |

### Key Findings

#### 🏆 Winner: Silver Bullet Style
- **Highest net profit**: $28,000
- **Good win rate**: 69.23%
- **Simplest execution**: Fixed stops/targets
- **Best for automation**: Mechanical rules

#### 🥈 Runner-up: Conservative
- **Second highest profit**: $25,539
- **Highest win rate**: 80.77%
- **Lowest drawdown**: $1,344 (best risk management)
- **Most reliable**: 100% fill rate

#### 🥉 Third Place: Algo Run
- **Best win rate**: 88.46% (exceptional!)
- **Best profit factor**: 10.43
- **Strong profit**: $19,827
- **Most consistent**: Statistical approach works

#### ⚠️ Disappointing: Sniper
- **Lowest profit**: $6,376
- **Lowest win rate**: 35%
- **Highest drawdown**: $2,610
- **Many unfilled**: 6 out of 26 setups (23%)
- **Issue**: Tight stops get hit too often; 50% CE doesn't always fill

### Analysis by Metric

**Win Rate Rankings:**
1. Algo Run: 88.46% ⭐⭐⭐⭐⭐
2. Conservative: 80.77% ⭐⭐⭐⭐
3. Silver Bullet: 69.23% ⭐⭐⭐
4. Sniper: 35.00% ⭐

**Profit Rankings:**
1. Silver Bullet: $28,000 ⭐⭐⭐⭐⭐
2. Conservative: $25,539 ⭐⭐⭐⭐
3. Algo Run: $19,827 ⭐⭐⭐
4. Sniper: $6,376 ⭐

**Risk Management (Max DD):**
1. Conservative: $1,344 ⭐⭐⭐⭐⭐
2. Algo Run: $1,557 ⭐⭐⭐⭐
3. Sniper: $2,610 ⭐⭐
4. Silver Bullet: $3,000 ⭐

**Consistency (Profit Factor):**
1. Algo Run: 10.43 ⭐⭐⭐⭐⭐
2. Conservative: 8.07 ⭐⭐⭐⭐
3. Silver Bullet: 4.50 ⭐⭐⭐
4. Sniper: 1.60 ⭐

## Recommendations

### For Different Trader Types

**New Traders** → **Conservative**
- Highest win rate (80.77%)
- Lowest drawdown
- Most forgiving (wide stops)
- Builds confidence

**Experienced Traders** → **Algo Run**
- Best win rate (88.46%)
- Best profit factor (10.43)
- Sophisticated approach
- Requires understanding of statistics

**Algorithmic Traders** → **Silver Bullet**
- Highest profit
- Fully mechanical
- Easy to code
- Fixed parameters

**Scalpers** → **Conservative or Silver Bullet**
- Avoid Sniper (too many unfilled orders)
- Silver Bullet better for speed
- Conservative better for safety

### Variant Selection Guide

Choose **Conservative** if you want:
- ✅ High win rate
- ✅ Low stress
- ✅ Reliable execution
- ✅ Best risk management

Choose **Algo Run** if you want:
- ✅ Highest win rate
- ✅ Statistical edge
- ✅ Consistent results
- ✅ Systematic approach

Choose **Silver Bullet** if you want:
- ✅ Maximum profit
- ✅ Simple rules
- ✅ Fast execution
- ✅ Easy automation

**Avoid Sniper** unless:
- You have very low capital (need tight stops)
- You're extremely patient (accept low fill rate)
- You're willing to sacrifice win rate for R:R

## Usage

### Basic Usage
```python
from fvg_reversal_variants import FVGReversalVariants

# Initialize
backtest = FVGReversalVariants(capital=100000, risk_per_trade=0.01)

# Run comparison for 2024
comparison = backtest.run_all_variants(years=[2024])

# Save results
backtest.save_results(comparison)
```

### Multi-Year Analysis
```python
# Compare across multiple years
comparison = backtest.run_all_variants(years=[2023, 2024, 2025])
```

### Access Detailed Trades
```python
# Get detailed trades for specific variant
conservative_trades = backtest.results['Conservative']
print(conservative_trades.head())

# Analyze specific variant
wins = conservative_trades[conservative_trades['outcome'] == 'win']
print(f"Average winning trade: ${wins['pnl'].mean():.2f}")
```

## Output Files

The script generates the following CSV files:

1. **fvg_variants_comparison.csv** - Summary comparison table
2. **fvg_variant_conservative_trades.csv** - Detailed Conservative trades
3. **fvg_variant_sniper_trades.csv** - Detailed Sniper trades
4. **fvg_variant_algo_run_trades.csv** - Detailed Algo Run trades
5. **fvg_variant_silver_bullet_trades.csv** - Detailed Silver Bullet trades

## Technical Details

### Liquidity Sweep Detection
- Scans last 20 bars for swing high/low
- Confirms violation (sweep) in recent 2 bars
- Direction determines setup bias (sweep low = bullish setup)

### MSS Detection
- Checks for structure break in last 10 bars
- Requires displacement (1.5x average body size)
- Validates momentum shift

### FVG Detection
- 3-candle gap pattern
- Bullish: Low[i] > High[i-2]
- Bearish: High[i] < Low[i-2]
- Calculates CE (50% level) and proximal line

### Entry Fill Logic
- **Proximal entries**: Filled immediately (100% rate)
- **CE 50% entries**: Scans next 20 bars for retrace
- Unfilled orders = skipped trades

## Configuration Options

### Modify Variant Parameters

```python
# Example: Adjust Sniper to use 4R instead of 3R
backtest = FVGReversalVariants()
backtest.variants['Sniper']['rr_ratio'] = 4.0

# Run with modified parameters
comparison = backtest.run_all_variants(years=[2024])
```

### Create Custom Variant

```python
# Add a new variant
backtest.variants['My_Custom'] = {
    'entry_type': 'proximal',
    'sl_type': 'fixed',
    'sl_points': 30,
    'tp_type': 'fixed_rr',
    'rr_ratio': 2.5,
    'description': 'Custom 30pt SL, 2.5R target'
}
```

## Limitations

1. **No Commission/Slippage**: Results don't include trading costs
2. **Perfect Fills**: Assumes limit orders fill at exact price
3. **15m Only**: Currently uses only 15m timeframe
4. **Simple MSS**: MSS detection could be more sophisticated
5. **Fixed Position Size**: Uses 1% risk regardless of conditions

## Future Enhancements

- [ ] Add 5m entry refinement option
- [ ] Include commission and slippage
- [ ] Add more sophisticated MSS detection
- [ ] Implement dynamic position sizing
- [ ] Add correlation with ES for SMT divergence
- [ ] Multi-timeframe confirmation
- [ ] Walk-forward optimization

## Conclusion

The comparison reveals that **Silver Bullet Style** produces the highest profit with simple, mechanical execution, making it ideal for automation. However, **Algo Run** offers the best consistency with 88.46% win rate, while **Conservative** provides the best risk management.

**The Sniper variant underperformed** significantly, suggesting that while the concept of precise entry at 50% CE is theoretically attractive, in practice the tight stops and lower fill rate make it less viable than other approaches.

**Recommendation**: Start with **Silver Bullet** for maximum profit or **Conservative** for maximum safety. Avoid **Sniper** unless you're specifically testing tight-stop strategies.

---

**Script**: fvg_reversal_variants.py  
**Author**: ICT Quantitative Trader Expert  
**Date**: December 11, 2025  
**Data**: 2024 NQ 15m OHLCV  
**Trades Analyzed**: 98 total (26+20+26+26)

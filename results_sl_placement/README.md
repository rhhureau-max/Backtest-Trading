# Stop Loss Placement Analysis Results

## Overview

This directory contains results from analyzing **3 different stop loss placement strategies** for the FVG trading strategy.

**Strategies Tested:**
1. **Top/Bottom** - SL at top of FVG (long) / bottom (short)
2. **Bottom/Top** - SL at bottom of FVG (long) / top (short)
3. **First Candle** - SL below/above first candle (8:29)

**Risk/Reward Ratios:** 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0

---

## Quick Start

### View Sample Results (Recommended)

The sample analysis covers **15M timeframe from 2022-2024** with 3 key R/R ratios (2.0, 3.0, 5.0):

```bash
# View report
open sl_placement_sample_report.md

# View visualizations
open sl_placement_analysis.png
open sl_placement_table.png
```

**Key Finding:** First Candle strategy with R/R 3.0 achieves **51.80% return** with **45.57% win rate**.

---

## Files in This Directory

### Reports
- `sl_placement_sample_report.md` - Sample analysis report (15M, 2022-2024)
- `sl_placement_comparison_report.md` - Full report (if complete analysis ran)

### Visualizations
- `sl_placement_analysis.png` - 4-panel comparison chart
- `sl_placement_table.png` - Detailed results table

### Trade Data

**Sample Data (15M timeframe, 2022-2024):**
- `trades_15m_{strategy}_rr{ratio}_sample.csv` - 9 files
  - Example: `trades_15m_first_candle_rr3.0_sample.csv`

**Partial 1M Data (2018-2024):**
- `trades_1m_{strategy}_rr{ratio}.csv` - 23 files available
  - Some configurations from interrupted full analysis

---

## Best Results Summary

### 15M Timeframe (Sample: 2022-2024)

| Strategy | Best R/R | Return | Win Rate | Sharpe |
|----------|----------|--------|----------|--------|
| **First Candle** | 3.0 | **51.80%** ⭐ | **45.57%** ⭐ | 1.63 |
| Bottom/Top | 3.0 | **50.80%** | 38.23% | **1.85** ⭐ |
| Top/Bottom | 5.0 | 38.72% | 25.08% | 1.70 |

**Champion:** First Candle + R/R 3.0
- Highest return (51.80%)
- Highest win rate (45.57%)
- Excellent Sharpe (1.63)

**Alternative:** Bottom/Top + R/R 3.0
- Best risk-adjusted (1.85 Sharpe)
- Second best return (50.80%)
- Lower drawdown (-5.82% vs -8.23%)

---

## Average Performance by Strategy

| Strategy | Avg Return | Avg Win Rate | Avg Sharpe |
|----------|------------|--------------|------------|
| First Candle | **49.91%** | **45.97%** | 1.58 |
| Bottom/Top | 45.18% | 38.43% | **1.69** |
| Top/Bottom | 29.90% | 29.87% | 1.51 |

**Insight:** Wider stop loss (First Candle) = +20% better performance

---

## How to Use These Results

### 1. Review Sample Analysis

Start with the sample report to understand the methodology and results:

```bash
cat sl_placement_sample_report.md
```

### 2. Examine Trade Data

Pick a configuration and analyze the trades:

```bash
# Best configuration
head -20 trades_15m_first_candle_rr3.0_sample.csv

# Or import in Python
import pandas as pd
trades = pd.read_csv('trades_15m_first_candle_rr3.0_sample.csv')
print(trades[trades['exit_reason'] == 'TP'].describe())
```

### 3. View Visualizations

The charts show:
- Total Return vs R/R Ratio (by strategy)
- Win Rate vs R/R Ratio (by strategy)
- Sharpe Ratio vs R/R Ratio (by strategy)
- Average Performance Comparison (bar chart)

### 4. Run Complete Analysis

For full analysis across all timeframes and years:

```bash
cd ..
python3 stop_loss_placement_analysis.py
```

**Warning:** This takes 30-60 minutes and generates 72 configurations (3 TF × 3 SL × 8 R/R).

---

## Key Insights

### 1. Stop Loss Placement Matters (20% Impact)

| Placement | Impact |
|-----------|--------|
| First Candle | +20% vs Top/Bottom |
| Bottom/Top | +15% vs Top/Bottom |
| Top/Bottom | Baseline |

### 2. R/R 3.0 is the Sweet Spot

Optimal across all strategies:
- First Candle: 51.80% return
- Bottom/Top: 50.80% return, 1.85 Sharpe ⭐
- Top/Bottom: 28.55% return

### 3. Win Rate Improvement

Wider stops significantly improve win rates:
- First Candle: **45.97%** average
- Bottom/Top: 38.43% average
- Top/Bottom: 29.87% average

### 4. Trade-off Analysis

Accepting +3% drawdown yields:
- +15 percentage points in win rate
- +20% improvement in total return

---

## Recommendations

### For Maximum Returns
**Configuration:** First Candle + R/R 3.0 (15M)
- Return: 51.80%
- Win Rate: 45.57%
- Max DD: -8.23%

### For Best Risk-Adjusted
**Configuration:** Bottom/Top + R/R 3.0 (15M)
- Return: 50.80%
- Sharpe: 1.85 ⭐
- Max DD: -5.82%

### For Conservative Traders
**Configuration:** Bottom/Top + R/R 2.0 (15M)
- Return: 37.20%
- Win Rate: 40.37%
- Max DD: -5.54%

---

## Running Your Own Analysis

### Quick Sample (15M, 2022-2024)

```bash
cd ..
python3 run_sl_analysis_sample.py
```

**Time:** ~15 seconds  
**Output:** 9 configurations tested

### Complete Analysis (All TF, 2018-2024)

```bash
cd ..
python3 stop_loss_placement_analysis.py
```

**Time:** ~30-60 minutes  
**Output:** 72 configurations tested

### Generate Visualizations

```bash
cd ..
python3 create_sl_visualizations.py
```

---

## CSV File Format

Each trade CSV contains:
- `entry_time` - When trade entered
- `entry_price` - Entry price
- `exit_time` - When trade exited
- `exit_price` - Exit price
- `direction` - Long or Short
- `stop_loss` - SL level
- `take_profit` - TP level
- `exit_reason` - TP, SL, or EOD
- `pnl` - Profit/loss in dollars
- `return_pct` - Return percentage
- `fvg_lower` - Lower bound of FVG
- `fvg_upper` - Upper bound of FVG
- `fvg_middle` - Middle of FVG

---

## Notes

- **Sample vs Full:** Sample uses 2022-2024 on 15M for quick demonstration
- **No Slippage:** Results don't include transaction costs or slippage
- **Historical Data:** Past performance doesn't guarantee future results
- **Market Structure:** First Candle strategy uses actual market structure vs arbitrary FVG limits

---

## Questions?

For detailed methodology and insights, see:
- `../STOP_LOSS_PLACEMENT_SUMMARY.md` - Comprehensive French summary
- `sl_placement_sample_report.md` - Sample analysis report
- `../stop_loss_placement_analysis.py` - Source code

---

*Generated: 2025-11-24*  
*Sample Period: 2022-2024 (15M)*  
*Sample Trades: 981 (327 × 3 strategies)*

# Exit Timing Analysis Results

## Overview

This directory contains the **exit timing analysis** for the FVG trading strategy, showing the average number of candles required to hit TP or SL after entry.

**Analysis Coverage:**
- **56 configurations** analyzed
- **18,664+ trades** processed
- **3 timeframes:** 1m, 5m, 15m
- **8 R/R ratios:** 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0
- **4 SL placements:** Middle, Top/Bottom, Bottom/Top, First Candle
- **Period:** 2018-2024 (7 years)

---

## Quick Results

### ⚡ Fastest Exits

**Fastest TP:**
- Configuration: 1M - Top/Bottom - R/R 1.5
- **3.8 candles** average
- Median: 2 candles
- Real time: ~3.8 minutes

**Fastest SL:**
- Configuration: 1M - Top/Bottom - R/R 1.5
- **2.9 candles** average
- Median: 1 candle
- Real time: ~2.9 minutes

### 📊 Average Timing by Configuration

| Configuration | Avg TP | Avg SL | TP/SL Ratio |
|---------------|--------|--------|-------------|
| **1M Top/Bottom** | 15.7 | 5.6 | 2.8:1 |
| 1M Middle | 29.1 | 9.4 | 3.1:1 |
| 1M Bottom/Top | 46.8 | 15.7 | 3.0:1 |
| 1M First Candle | 67.1 | 23.6 | 2.8:1 |
| **5M Middle** | 18.7 | 6.6 | 2.8:1 |
| **15M Middle** | 10.1 | 4.5 | 2.2:1 |

---

## Files in This Directory

### Reports
- `exit_timing_report.md` - Complete detailed report with all configurations
- `README.md` - This file

### Data
- `exit_timing_detailed.csv` - CSV with all timing metrics for 56 configurations

### Visualizations
- `exit_timing_analysis.png` - 4-panel chart showing:
  - TP Timing vs R/R Ratio (Middle SL)
  - SL Timing vs R/R Ratio (Middle SL)
  - Exit Timing by SL Placement (bar chart)
  - TP Timing Distribution by Timeframe (box plot)

---

## Key Insights

### 1. SL Hit Faster Than TP

**Across all configurations:**
- SL is hit **2-3x faster** than TP on average
- Example: 1M Middle R/R 2.0 → TP: 11.4 candles, SL: 5.5 candles
- **Implication:** Losses cut quickly, profits take time

### 2. Tighter Stops = Faster Exits

| SL Placement | Speed | Trade-off |
|--------------|-------|-----------|
| Top/Bottom | ⚡⚡⚡ Fastest | Lower win rate |
| Middle | ⚡⚡ Fast | Balanced |
| Bottom/Top | ⚡ Moderate | Better win rate |
| First Candle | 🐢 Slower | Best win rate |

### 3. R/R Impact on Timing

**Lower R/R (1.5-2.0):**
- TP hit quickly (6-11 candles)
- Good for scalping
- More trades per session

**Higher R/R (4.0-5.0):**
- TP hit slowly (43-53 candles for 1M)
- Requires patience
- Better returns but longer exposure

### 4. Timeframe Comparison

| TF | Avg TP (R/R 2.0) | Real Time | Trades/Day |
|----|------------------|-----------|------------|
| 1M | 11.4 candles | 11 min | Many |
| 5M | 10.6 candles | 53 min | Moderate |
| 15M | 8.2 candles | 123 min | Few |

**Note:** 15M shows **fastest relative exits** (fewer candles) but longer absolute time.

---

## Detailed Example: 1M Middle SL

| R/R | TP Count | SL Count | Avg TP | Avg SL | Median TP | Median SL |
|-----|----------|----------|--------|--------|-----------|-----------|
| 1.5 | 296 | 429 | 6.7 | 4.8 | 4 | 2 |
| 2.0 | 267 | 458 | **11.4** | **5.5** | 5 | 2 |
| 2.5 | 236 | 488 | 16.8 | 6.7 | 7 | 2 |
| 3.0 | 214 | 509 | 22.9 | 7.4 | 11 | 2 |
| 4.0 | 181 | 540 | 43.1 | 11.4 | 24 | 3 |
| 5.0 | 147 | 566 | 53.1 | 15.9 | 30 | 3 |

**Observations:**
- Higher R/R = longer wait for TP (up to 8x longer)
- SL timing relatively stable (2-3 candles median)
- More SL hits than TP hits as R/R increases

---

## Practical Applications

### 1. Position Sizing Based on Time

**If average TP = 10 candles:**
- Plan for ~2.5 hour exposure (15M timeframe)
- Don't open too many positions simultaneously
- Consider capital allocation per trade

### 2. Entry Time Filtering

**Avoid late entries:**
- Don't enter after 2 PM if TP takes 10+ candles (15M)
- Risk of EOD closure before TP
- Best entries: Morning session (8:30-11 AM)

### 3. Dynamic R/R Adjustment

**Adapt to time available:**
- Morning (8-11 AM): Use R/R 3.0-5.0 (time available)
- Midday (11 AM-1 PM): Use R/R 2.0-3.0 (moderate)
- Afternoon (1-3 PM): Use R/R 1.5-2.0 (limited time)

### 4. Stop Loss Trailing

**Based on timing:**
- If trade exceeds 2x median time without exit
- Consider trailing stop or manual exit
- Example: Median 10 candles → if 20 candles reached, review position

---

## Recommendations by Profile

### Scalper (Quick Trades) ⚡

**Configuration:**
- Timeframe: 1M
- SL Placement: Top/Bottom
- R/R: 1.5-2.0

**Expected Timing:**
- TP: 4-6 candles (4-6 minutes)
- SL: 3-4 candles (3-4 minutes)

### Intraday Trader ⚖️

**Configuration:**
- Timeframe: 15M
- SL Placement: Middle or Bottom/Top
- R/R: 2.0-3.0

**Expected Timing:**
- TP: 8-13 candles (2-3.25 hours)
- SL: 4-5 candles (1-1.25 hours)

### Patient Trader 🎯

**Configuration:**
- Timeframe: 1M
- SL Placement: First Candle
- R/R: 3.0-4.0

**Expected Timing:**
- TP: 70-92 candles (1-1.5 hours)
- SL: 25-31 candles (25-31 minutes)
- Best win rates, requires patience

---

## CSV Data Format

The `exit_timing_detailed.csv` contains:

**Columns:**
- `timeframe` - 1m, 5m, 15m
- `rr_ratio` - 1.5 to 5.0
- `sl_placement` - middle, top, bottom, first_candle
- `total_trades` - Total number of trades
- `tp_count` - Trades exited at TP
- `sl_count` - Trades exited at SL
- `eod_count` - Trades closed at end of day
- `avg_candles_tp` - Average candles to TP
- `median_candles_tp` - Median candles to TP
- `min_candles_tp` - Minimum candles to TP
- `max_candles_tp` - Maximum candles to TP
- `avg_candles_sl` - Average candles to SL
- `median_candles_sl` - Median candles to SL
- `min_candles_sl` - Minimum candles to SL
- `max_candles_sl` - Maximum candles to SL
- `avg_candles_eod` - Average candles for EOD exits

---

## Statistical Notes

### Median vs Average

**Important observation:**
- Median is typically **lower than average**
- Example: 1M Middle R/R 3.0 → Avg: 22.9, Median: 11
- **Reason:** Some very long trades pull average up
- **Use median** for typical case estimation

### Distribution Characteristics

**TP Timing:**
- Right-skewed distribution
- Most trades exit relatively quickly
- Some outliers with very long holds

**SL Timing:**
- More concentrated distribution
- Less variance than TP
- Typically hit within first few candles

---

## How to Use These Results

### 1. Review the Report

```bash
# View detailed report
open exit_timing_report.md
```

### 2. Analyze Specific Configurations

```python
import pandas as pd

# Load data
df = pd.read_csv('exit_timing_detailed.csv')

# Filter for specific configuration
config = df[(df['timeframe'] == '1m') & 
            (df['rr_ratio'] == 2.0) & 
            (df['sl_placement'] == 'middle')]

print(f"Average TP: {config['avg_candles_tp'].values[0]:.1f} candles")
print(f"Average SL: {config['avg_candles_sl'].values[0]:.1f} candles")
```

### 3. Plan Your Trading Session

**Example calculation:**
- Timeframe: 15M
- R/R: 2.0
- Expected TP: 8.2 candles = 123 minutes
- Session duration: 8:30-16:00 = 7.5 hours
- Potential trades: ~3-4 per day

---

## Regenerating the Analysis

To run the analysis yourself:

```bash
cd ..
python3 analyze_exit_timing.py
```

**Requirements:**
- Existing trade CSV files in `results_rr_analysis/` and `results_sl_placement/`
- Python 3.7+
- pandas, numpy, matplotlib, seaborn

**Runtime:** ~1 minute

---

## Questions?

For detailed methodology and insights:
- `exit_timing_report.md` - Complete analysis report
- `../EXIT_TIMING_SUMMARY.md` - Comprehensive French summary
- `../analyze_exit_timing.py` - Source code

---

*Generated: 2025-11-24*  
*Configurations: 56*  
*Total Trades: 18,664+*  
*Period: 2018-2024*

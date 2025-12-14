# FVG Strategy - Stop Loss Placement Analysis (Sample)

**Generated:** 2025-11-24 10:16:06

**Period:** 2022-2024 (Sample period for demonstration)

**Timeframe:** 15M

---

## Stop Loss Placement Strategies Tested:

1. **SL at Top/Bottom of FVG:** SL at top (long) / bottom (short)
2. **SL at Bottom/Top of FVG:** SL at bottom (long) / top (short)
3. **SL at First Candle:** SL below/above first candle (8:29)

## 15M Timeframe Results


### Strategy: SL at Top/Bottom

| R/R | Trades | Win Rate (%) | Return (%) | Sharpe | Max DD (%) | Profit Factor |
|-----|--------|--------------|------------|--------|------------|---------------|
| 2.0 | 327 | 34.86 | 22.44 | 1.38 | -6.22 | 1.27 |
| 3.0 | 327 | 29.66 | 28.55 | 1.46 | -6.13 | 1.32 |
| 5.0 | 327 | 25.08 | 38.72 | 1.70 | -6.63 | 1.42 |

**Best R/R:** 5.0 with 38.72% return


### Strategy: SL at Bottom/Top

| R/R | Trades | Win Rate (%) | Return (%) | Sharpe | Max DD (%) | Profit Factor |
|-----|--------|--------------|------------|--------|------------|---------------|
| 2.0 | 327 | 40.37 | 37.20 | 1.50 | -5.54 | 1.30 |
| 3.0 | 327 | 38.23 | 50.80 | 1.85 | -5.82 | 1.39 |
| 5.0 | 327 | 36.70 | 47.54 | 1.70 | -5.82 | 1.36 |

**Best R/R:** 3.0 with 50.80% return


### Strategy: SL at First Candle

| R/R | Trades | Win Rate (%) | Return (%) | Sharpe | Max DD (%) | Profit Factor |
|-----|--------|--------------|------------|--------|------------|---------------|
| 2.0 | 327 | 47.09 | 48.54 | 1.58 | -8.23 | 1.31 |
| 3.0 | 327 | 45.57 | 51.80 | 1.63 | -8.23 | 1.33 |
| 5.0 | 327 | 45.26 | 49.38 | 1.54 | -8.76 | 1.31 |

**Best R/R:** 3.0 with 51.80% return


## Comparison Across SL Placements

| Strategy | Avg Return (%) | Avg Win Rate (%) | Avg Sharpe |
|----------|----------------|------------------|------------|
| top | 29.90 | 29.87 | 1.51 |
| bottom | 45.18 | 38.43 | 1.69 |
| first_candle | 49.91 | 45.97 | 1.58 |

## Notes

This is a sample analysis using a subset of data to demonstrate the SL placement analysis functionality.
For complete analysis across all years and timeframes, run the full `stop_loss_placement_analysis.py` script.

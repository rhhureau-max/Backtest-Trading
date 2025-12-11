# FVG (Fair Value Gap) Analysis at 8:30 AM New York Opening

## Methodology

This analysis examines 1-minute candles from 2018 to 2025 to detect Fair Value Gaps (FVG) at the 8:30 AM New York opening candle.

### FVG Definition (Using Wicks/Shadows)

An FVG is detected when there is **complete imbalance** between the candle n-1 (8:29) and candle n+1 (8:31), meaning there is NO overlap between their full price ranges (body + wicks):

- **Bullish FVG**: Low (including lower wick) of 8:31 > High (including upper wick) of 8:29
  - This creates an upward gap with no price overlap
- **Bearish FVG**: High (including upper wick) of 8:31 < Low (including lower wick) of 8:29
  - This creates a downward gap with no price overlap

### Candle Structure

```
     |  <- Upper Wick (High)
   ┌─┴─┐
   │   │ <- Body (Open to Close)
   └─┬─┘
     |  <- Lower Wick (Low)
```

The FVG detection uses **High** and **Low** values, which include the full wick range, not just the body (Open/Close).

## Summary Statistics

| Metric | Value |
|--------|-------|
| Total trading days analyzed | 2023 |
| Days with FVG at 8:30 | 813 (40.19%) |
| Bullish FVGs | 460 (22.74%) |
| Bearish FVGs | 353 (17.45%) |
| Days without FVG | 1210 (59.81%) |

## FVG Size Statistics (in points)

The FVG Size represents the gap distance between the wicks:
- Bullish: Low(8:31) - High(8:29)
- Bearish: Low(8:29) - High(8:31)

| Statistic | Value |
|-----------|-------|
| Mean | 9.99 |
| Median | 7.27 |
| Min | 0.25 |
| Max | 61.60 |

## Yearly Breakdown

| Year | Total Days | FVG Count | Bullish FVGs | Bearish FVGs | FVG % |
|------|------------|-----------|--------------|--------------|-------|
| 2018 | 256 | 79 | 51 | 28 | 30.86% |
| 2019 | 258 | 109 | 63 | 46 | 42.25% |
| 2020 | 254 | 102 | 58 | 44 | 40.16% |
| 2021 | 258 | 118 | 66 | 52 | 45.74% |
| 2022 | 258 | 105 | 71 | 34 | 40.70% |
| 2023 | 257 | 106 | 63 | 43 | 41.25% |
| 2024 | 259 | 103 | 47 | 56 | 39.77% |
| 2025 | 223 | 91 | 41 | 50 | 40.81% |

## Last 10 FVG Signals

| Date | Type | FVG Size | High 8:29 | Low 8:29 | High 8:31 | Low 8:31 |
|:-----|:----:|:--------:|:---------:|:--------:|:---------:|:--------:|
| 2025-11-12 | Bearish | 35.75 | 25781.75 | 25773.75 | 25738.00 | 25692.75 |
| 2025-11-10 | Bullish | 13.75 | 25547.25 | 25532.25 | 25584.75 | 25561.00 |
| 2025-11-07 | Bearish | 31.00 | 25115.25 | 25101.75 | 25070.75 | 25046.00 |
| 2025-11-06 | Bearish | 6.00 | 25681.75 | 25667.00 | 25661.00 | 25635.50 |
| 2025-11-03 | Bullish | 3.50 | 26236.00 | 26221.75 | 26262.75 | 26239.50 |
| 2025-10-31 | Bearish | 8.50 | 26208.00 | 26196.75 | 26188.25 | 26158.25 |
| 2025-10-30 | Bearish | 4.75 | 26126.25 | 26101.50 | 26096.75 | 26069.25 |
| 2025-10-28 | Bullish | 13.00 | 26056.25 | 26050.00 | 26091.50 | 26069.25 |
| 2025-10-27 | Bullish | 19.25 | 25827.25 | 25814.25 | 25859.50 | 25846.50 |
| 2025-10-24 | Bearish | 6.25 | 25471.50 | 25464.75 | 25458.50 | 25429.75 |

## Data Files

- `fvg_830_analysis_results.csv`: Detailed daily results with all candle data
- `fvg_830_analysis.py`: Python script used for this analysis
- `fvg_backtest.py`: Backtest script with SL/TP analysis
- `FVG_BACKTEST_REPORT.md`: Detailed backtest results

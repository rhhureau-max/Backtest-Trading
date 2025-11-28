# FVG (Fair Value Gap) Analysis at 8:30 AM New York Opening

## Methodology

This analysis examines 1-minute candles from 2018 to 2025 to detect Fair Value Gaps (FVG) at the 8:30 AM New York opening candle.

An FVG occurs when there is an imbalance between the candle before (n-1) and the candle after (n+1):

- **Bullish FVG**: Low of candle at 8:31 > High of candle at 8:29 (gap up)
- **Bearish FVG**: High of candle at 8:31 < Low of candle at 8:29 (gap down)

## Summary Statistics

| Metric | Value |
|--------|-------|
| Total trading days analyzed | 2023 |
| Days with FVG at 8:30 | 813 (40.19%) |
| Bullish FVGs | 460 (22.74%) |
| Bearish FVGs | 353 (17.45%) |
| Days without FVG | 1210 (59.81%) |

## FVG Size Statistics (in points)

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

## Data Files

- `fvg_830_analysis_results.csv`: Detailed daily results with all candle data
- `fvg_830_analysis.py`: Python script used for this analysis

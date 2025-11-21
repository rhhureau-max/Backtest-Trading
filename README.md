# Backtest-Trading

## Overview
This repository contains historical trading data in 1-minute, 5-minute, 15-minute, 1-hour, 4-hour, and daily intervals from 2018 to 2025.

## Analysis Tools

### Returns Analysis Script
The `analyze_returns.py` script analyzes 1-minute trading data files (XLSX and CSV) to calculate annual and overall returns.

### FVG Analysis Script (8:30 AM)
The `analyze_fvg_830.py` script analyzes Fair Value Gap (FVG) occurrences at the 8:30 AM candle across all years from 2018 onwards.

#### Usage
```bash
python3 analyze_returns.py
```

#### Requirements
```bash
pip3 install pandas openpyxl
```

#### Output
The script generates:
- Console output with detailed annual returns
- `returns_analysis.txt` file with a summary report including:
  - Annual returns for each year (2018-2025)
  - Overall return across all years
  - Average annual return
  - Compound Annual Growth Rate (CAGR)

#### Results Summary (as of latest analysis)
- **Overall Return (2018-2025)**: 242.29%
- **Average Annual Return**: 19.68%
- **CAGR**: 16.63% (based on 8 year periods)

| Year | Return % | First Close | Last Close |
|------|----------|-------------|------------|
| 2018 | -2.28%   | 7506.96     | 7336.14    |
| 2019 | 36.31%   | 7337.00     | 10000.85   |
| 2020 | 47.25%   | 10002.56    | 14728.99   |
| 2021 | 26.89%   | 14743.00    | 18706.98   |
| 2022 | -33.83%  | 18767.69    | 12418.73   |
| 2023 | 45.90%   | 12493.81    | 18228.23   |
| 2024 | 20.01%   | 18241.90    | 21891.80   |
| 2025 | 17.23%   | 21919.64    | 25695.75   |

---

### FVG Analysis at 8:30 AM

#### What is FVG?
Fair Value Gap (FVG) is a technical analysis pattern that identifies price gaps between candles:
- **Bullish FVG**: Low of the next candle (8:31) > High of the previous candle (8:29)
- **Bearish FVG**: High of the next candle (8:31) < Low of the previous candle (8:29)

#### Usage
```bash
python3 analyze_fvg_830.py
```

#### Requirements
Same as Returns Analysis Script:
```bash
pip3 install pandas openpyxl
```

#### Output
The script generates:
- Console output with year-by-year FVG statistics
- `fvg_analysis_830.txt` file with detailed breakdown

#### Results Summary (2018-2025)
- **Total Trading Days**: 2,028
- **Total FVG Occurrences**: 813 (40.09% of days)
- **Bullish FVG**: 460 occurrences (22.68% of days, 56.58% of all FVG)
- **Bearish FVG**: 353 occurrences (17.41% of days, 43.42% of all FVG)
- **No FVG**: 1,210 days (59.66%)

| Year | Days | Bullish FVG | Bearish FVG | Total FVG | FVG % |
|------|------|-------------|-------------|-----------|-------|
| 2018 | 256  | 51          | 28          | 79        | 30.86% |
| 2019 | 258  | 63          | 46          | 109       | 42.25% |
| 2020 | 259  | 58          | 44          | 102       | 39.38% |
| 2021 | 258  | 66          | 52          | 118       | 45.74% |
| 2022 | 258  | 71          | 34          | 105       | 40.70% |
| 2023 | 257  | 63          | 43          | 106       | 41.25% |
| 2024 | 259  | 47          | 56          | 103       | 39.77% |
| 2025 | 223  | 41          | 50          | 91        | 40.81% |
# Backtest-Trading

## Overview
This repository contains historical trading data in 1-minute, 5-minute, 15-minute, 1-hour, 4-hour, and daily intervals from 2018 to 2025.

## Analysis Tools

### Returns Analysis Script
The `analyze_returns.py` script analyzes 1-minute trading data files (XLSX and CSV) to calculate annual and overall returns.

### FVG Analysis Scripts (8:30 AM)
Multiple scripts analyze Fair Value Gap (FVG) occurrences and quality at the 8:30 AM candle:

**FVG Detection Scripts:**
- `analyze_fvg_830.py` - 1-minute data (8:29, 8:30, 8:31 candles)
- `analyze_fvg_5m.py` - 5-minute data (8:25, 8:30, 8:35 candles)
- `analyze_fvg_15m.py` - 15-minute data (8:15, 8:30, 8:45 candles)

**FVG Quality Scripts:**
- `analyze_fvg_quality_1m.py` - Analyzes if price returns to FVG zone within 5 candles after FVG closes (by 8:36)
- `analyze_fvg_quality_5m.py` - Analyzes if price returns to FVG zone within 5 candles after FVG closes (by 9:05)
- `analyze_fvg_quality_15m.py` - Analyzes if price returns to FVG zone within 5 candles after FVG closes (by 10:00)

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
- **Bullish FVG**: Low of the next candle > High of the previous candle
- **Bearish FVG**: High of the next candle < Low of the previous candle

#### Usage
```bash
# 1-minute data analysis
python3 analyze_fvg_830.py

# 5-minute data analysis
python3 analyze_fvg_5m.py

# 15-minute data analysis
python3 analyze_fvg_15m.py
```

#### Requirements
Same as Returns Analysis Script:
```bash
pip3 install pandas openpyxl
```

#### Output
Each script generates:
- Console output with year-by-year FVG statistics
- Text file with detailed breakdown:
  - `fvg_analysis_830.txt` (1-minute data)
  - `fvg_analysis_5m.txt` (5-minute data)
  - `fvg_analysis_15m.txt` (15-minute data)

#### Results Summary (2018-2025)

**1-Minute Data:**
- **Total Trading Days**: 2,028
- **Total FVG Occurrences**: 813 (40.09% of days)
- **Bullish FVG**: 460 occurrences (22.68% of days, 56.58% of all FVG)
- **Bearish FVG**: 353 occurrences (17.41% of days, 43.42% of all FVG)
- **No FVG**: 1,210 days (59.66%)

**5-Minute Data:**
- **Total Trading Days**: 2,027
- **Total FVG Occurrences**: 921 (45.44% of days)
- **Bullish FVG**: 497 occurrences (24.52% of days, 53.96% of all FVG)
- **Bearish FVG**: 424 occurrences (20.92% of days, 46.04% of all FVG)
- **No FVG**: 1,101 days (54.32%)

**15-Minute Data:**
- **Total Trading Days**: 2,028
- **Total FVG Occurrences**: 891 (43.93% of days)
- **Bullish FVG**: 465 occurrences (22.93% of days, 52.19% of all FVG)
- **Bearish FVG**: 426 occurrences (21.01% of days, 47.81% of all FVG)
- **No FVG**: 1,136 days (56.02%)

**Detailed Year-by-Year Results:**

*1-Minute Data:*
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

*5-Minute Data:*
| Year | Days | Bullish FVG | Bearish FVG | Total FVG | FVG % |
|------|------|-------------|-------------|-----------|-------|
| 2018 | 256  | 70          | 41          | 111       | 43.36% |
| 2019 | 258  | 66          | 50          | 116       | 44.96% |
| 2020 | 259  | 63          | 58          | 121       | 46.72% |
| 2021 | 258  | 61          | 52          | 113       | 43.80% |
| 2022 | 258  | 59          | 64          | 123       | 47.67% |
| 2023 | 257  | 79          | 44          | 123       | 47.86% |
| 2024 | 259  | 50          | 55          | 105       | 40.54% |
| 2025 | 222  | 49          | 60          | 109       | 49.10% |

*15-Minute Data:*
| Year | Days | Bullish FVG | Bearish FVG | Total FVG | FVG % |
|------|------|-------------|-------------|-----------|-------|
| 2018 | 257  | 58          | 53          | 111       | 43.19% |
| 2019 | 258  | 68          | 61          | 129       | 50.00% |
| 2020 | 259  | 56          | 51          | 107       | 41.31% |
| 2021 | 258  | 65          | 53          | 118       | 45.74% |
| 2022 | 258  | 55          | 59          | 114       | 44.19% |
| 2023 | 257  | 64          | 39          | 103       | 40.08% |
| 2024 | 259  | 50          | 60          | 110       | 42.47% |
| 2025 | 222  | 49          | 50          | 99        | 44.59% |

---

### FVG Quality Analysis at 8:30 AM

#### What is FVG Quality?
FVG Quality measures whether the price returns to the FVG zone after it's formed:
- **Good FVG**: Price doesn't return to the FVG zone after 5 candles
- **Bad FVG**: Price returns to the FVG zone after 5 candles

#### Usage
```bash
# 1-minute data quality analysis (checks by 8:36)
python3 analyze_fvg_quality_1m.py

# 5-minute data quality analysis (checks by 9:05)
python3 analyze_fvg_quality_5m.py

# 15-minute data quality analysis (checks by 10:00)
python3 analyze_fvg_quality_15m.py
```

#### Requirements
Same as other analysis scripts:
```bash
pip3 install pandas openpyxl
```

#### Output
Each script generates:
- Console output with year-by-year FVG quality statistics
- Text file with detailed breakdown:
  - `fvg_quality_analysis_1m.txt` (1-minute data)
  - `fvg_quality_analysis_5m.txt` (5-minute data)
  - `fvg_quality_analysis_15m.txt` (15-minute data)

#### Overall Results Summary (2018-2025)

**FVG Quality Statistics:**

- **1-Minute Data (check by 8:36)**: 813 FVG analyzed
  - Good FVG: 312 (38.38%)
  - Bad FVG: 501 (61.62%)

- **5-Minute Data (check by 9:05)**: 921 FVG analyzed
  - Good FVG: 373 (40.50%)
  - Bad FVG: 548 (59.50%)

- **15-Minute Data (check by 10:00)**: 891 FVG analyzed
  - Good FVG: 370 (41.53%)
  - Bad FVG: 521 (58.47%)

#### Year-by-Year Breakdown

**1-Minute Data:**
| Year | Total FVG | Good Bull | Bad Bull | Good Bear | Bad Bear | Good % |
|------|-----------|-----------|----------|-----------|----------|--------|
| 2018 | 79        | 21        | 30       | 11        | 17       | 40.51% |
| 2019 | 109       | 29        | 34       | 16        | 30       | 41.28% |
| 2020 | 102       | 16        | 42       | 19        | 25       | 34.31% |
| 2021 | 118       | 27        | 39       | 18        | 34       | 38.14% |
| 2022 | 105       | 32        | 39       | 12        | 22       | 41.90% |
| 2023 | 106       | 27        | 36       | 10        | 33       | 34.91% |
| 2024 | 103       | 15        | 32       | 20        | 36       | 33.98% |
| 2025 | 91        | 20        | 21       | 19        | 31       | 42.86% |

**5-Minute Data:**
| Year | Total FVG | Good Bull | Bad Bull | Good Bear | Bad Bear | Good % |
|------|-----------|-----------|----------|-----------|----------|--------|
| 2018 | 111       | 32        | 38       | 22        | 19       | 48.65% |
| 2019 | 116       | 33        | 33       | 24        | 26       | 49.14% |
| 2020 | 121       | 27        | 36       | 16        | 42       | 35.54% |
| 2021 | 113       | 24        | 37       | 17        | 35       | 36.28% |
| 2022 | 123       | 22        | 37       | 24        | 40       | 37.40% |
| 2023 | 123       | 30        | 49       | 16        | 28       | 37.40% |
| 2024 | 105       | 13        | 37       | 23        | 32       | 34.29% |
| 2025 | 109       | 22        | 27       | 28        | 32       | 45.87% |

**15-Minute Data:**
| Year | Total FVG | Good Bull | Bad Bull | Good Bear | Bad Bear | Good % |
|------|-----------|-----------|----------|-----------|----------|--------|
| 2018 | 111       | 25        | 33       | 20        | 33       | 40.54% |
| 2019 | 129       | 35        | 33       | 18        | 43       | 41.09% |
| 2020 | 107       | 26        | 30       | 16        | 35       | 39.25% |
| 2021 | 118       | 36        | 29       | 22        | 31       | 49.15% |
| 2022 | 114       | 24        | 31       | 25        | 34       | 42.98% |
| 2023 | 103       | 26        | 38       | 8         | 31       | 33.01% |
| 2024 | 110       | 23        | 27       | 24        | 36       | 42.73% |
| 2025 | 99        | 21        | 28       | 21        | 29       | 42.42% |

**Key Insights:** 
1. **Majority of FVG gaps are filled**: ~60% of FVG gaps at 8:30 AM get filled within 5 candles after the FVG forms
2. **Higher timeframes show slightly better hold rates**: 15m data has 41.53% good FVG vs 38.38% for 1m
3. **Year-to-year variation**: Good FVG rates vary from 33-49% depending on year and timeframe
4. **2021 notable for 15m**: Shows highest good FVG rate at 49.15%
5. **2020 notably volatile**: Shows lower good FVG rates across all timeframes (34-39%)
6. **Trading implications**: While most gaps fill, ~40% hold, suggesting selective FVG trading based on additional confirmation could be valuable
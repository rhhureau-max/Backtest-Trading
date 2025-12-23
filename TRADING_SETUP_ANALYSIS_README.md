# Trading Setup Analysis Results

## Overview
This analysis identifies a specific trading setup across multiple timeframes (1-minute, 5-minute, and 15-minute) from 2018 to 2025.

## Trading Setup Definition

The analysis looks at the **8:30 AM (Europe time)** candle and checks for the following conditions:

### Bearish 8:30 Setup (Bullish Reversal)
1. The 8:30 AM candle is **bearish** (close < open)
2. The **next candle** is **bullish** (close > open)
3. The next candle's **close** is **ABOVE** the maximum high of the **previous 5 candles**

### Bullish 8:30 Setup (Bearish Reversal)
1. The 8:30 AM candle is **bullish** (close > open)
2. The **next candle** is **bearish** (close < open)
3. The next candle's **close** is **BELOW** the minimum low of the **previous 5 candles**

## Results Summary

### Total Setups Found: **695**

| Timeframe | Total Setups | Bearish→Bullish | Bullish→Bearish |
|-----------|--------------|-----------------|-----------------|
| 1-minute  | 279          | 138             | 141             |
| 5-minute  | 232          | 116             | 116             |
| 15-minute | 184          | 99              | 85              |

### Breakdown by Year

#### 1-Minute Timeframe
- 2018: 40 setups
- 2019: 24 setups
- 2020: 31 setups
- 2021: 45 setups (highest)
- 2022: 30 setups
- 2023: 36 setups
- 2024: 35 setups
- 2025: 38 setups (partial year)

#### 5-Minute Timeframe
- 2018: 37 setups (highest)
- 2019: 35 setups
- 2020: 32 setups
- 2021: 26 setups
- 2022: 30 setups
- 2023: 27 setups
- 2024: 30 setups
- 2025: 15 setups (partial year)

#### 15-Minute Timeframe
- 2018: 31 setups (highest)
- 2019: 23 setups
- 2020: 26 setups
- 2021: 24 setups
- 2022: 21 setups
- 2023: 24 setups
- 2024: 14 setups
- 2025: 21 setups (partial year)

## Output Files

The analysis generated the following files:

### 1. `trading_setup_report.txt`
A human-readable summary report with:
- Setup definition
- Results by timeframe and year
- Overall statistics
- Setup type breakdown

### 2. `trading_setup_detailed_results.json`
Complete detailed results in JSON format including:
- Summary counts
- All setup occurrences with full candle data
- Date, time, and price information for each setup

### 3. `trading_setup_1m_detailed.csv`
Detailed CSV for all 1-minute setups (279 entries) with columns:
- date, time, year
- setup_type
- 8:30 candle: open, high, low, close
- next candle: open, high, low, close
- previous 5 candles: max_high, min_low

### 4. `trading_setup_5m_detailed.csv`
Detailed CSV for all 5-minute setups (232 entries)

### 5. `trading_setup_15m_detailed.csv`
Detailed CSV for all 15-minute setups (184 entries)

### 6. `analyze_trading_setup.py`
The Python script used to perform the analysis. Can be rerun if needed.

## Key Insights

1. **Frequency**: The setup occurs approximately 10-15% of trading days at the 8:30 AM mark
2. **Balance**: The setup types are nearly evenly distributed between bearish-to-bullish reversals and bullish-to-bearish reversals
3. **Timeframe Impact**: Higher timeframes (15m) show fewer setups than lower timeframes (1m), which is expected as the conditions are more stringent on larger candles
4. **Consistency**: The setup appears consistently across all years (2018-2025)

## How to Use These Results

1. **Review the summary report** (`trading_setup_report.txt`) for overall statistics
2. **Analyze specific setups** using the detailed CSV files to understand price levels and patterns
3. **Backtest strategies** using the detailed data to determine entry/exit points
4. **Filter by setup type** to focus on either bullish or bearish reversals
5. **Study year-by-year trends** to understand how market conditions affect setup frequency

## Running the Analysis Again

To rerun the analysis (e.g., with updated data):

```bash
python3 analyze_trading_setup.py
```

The script will:
1. Automatically unzip any zipped 1-minute data files
2. Load all CSV files for 1m, 5m, and 15m timeframes
3. Analyze each 8:30 AM candle
4. Generate all output files

## Data Source

The analysis uses historical trading data from CSV files in the repository:
- Format: Semicolon-delimited CSV
- Columns: Date, Time, Open, High, Low, Close, Volume
- Period: 2018-2025
- Timeframes: 1-minute, 5-minute, 15-minute

---

**Analysis Date**: December 2, 2025
**Total Data Points Analyzed**: ~2.7 million candles
**Execution Time**: ~3 minutes

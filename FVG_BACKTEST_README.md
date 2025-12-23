# Fair Value Gap (FVG) Reversal Strategy Backtest

## Overview
This repository contains a comprehensive backtesting implementation for a Fair Value Gap (FVG) reversal trading strategy on Nasdaq Futures (NQ) using 5-minute timeframe data.

## Strategy Description

### Fair Value Gap (FVG) Definition
- **Bearish FVG**: A downward imbalance where the high of candle N-1 is greater than the low of candle N+1
- **Bullish FVG**: An upward imbalance where the low of candle N-1 is less than the high of candle N+1

### Long Setup (Bearish FVG Reversal)
1. A bearish FVG forms (3 candles with gap)
2. Price returns into the FVG zone
3. Price fills and exceeds the FVG upper bound
4. A bullish candle validates the breakout
5. **Entry**: Long at close of validation candle
6. **Stop Loss**: Below the previous swing low
7. **Take Profit**: At the previous swing high

### Short Setup (Bullish FVG Reversal)
1. A bullish FVG forms (3 candles with gap)
2. Price returns into the FVG zone
3. Price fills and exceeds the FVG lower bound
4. A bearish candle validates the breakout
5. **Entry**: Short at close of validation candle
6. **Stop Loss**: Above the previous swing high
7. **Take Profit**: At the previous swing low

## Data Requirements

### Files
The script expects 5-minute CSV files for years 2018-2025 in the following format:
- Filename pattern: `YYYY 5m.csv` (e.g., "2018 5m.csv", "2019 5m.csv")
- Delimiter: Semicolon (;)

### CSV Structure
```
Column1;Column2;Column3;Column4;Column5;Column6;Column7
Date;Time;Open;High;Low;Close;Volume
DD/MM/YYYY;HH:MM:SS;float;float;float;float;int
```

### Trading Session
- **Session**: 02:00-06:00 (morning session)
- **Timezone**: Uses timestamps exactly as they appear in files (no conversion)

## Installation

### Requirements
- Python 3.7+
- pandas
- numpy

### Install Dependencies
```bash
pip install pandas numpy
```

## Usage

### Run the Backtest
```bash
python3 backtest_fvg_reversal.py
```

### Output
The script generates:
1. **Console Output**: Comprehensive performance report with statistics
2. **CSV File**: `fvg_reversal_trades.csv` containing all trade details

## Results Summary

### Global Performance (2018-2025)
- **Total Trades**: 47,684
- **Win Rate**: 75.74%
- **Net Gain**: 53,156.98 points
- **Profit Factor**: 1.20
- **Average Win**: 8.83 points
- **Average Loss**: 22.97 points
- **Win/Loss Ratio**: 0.38:1
- **Maximum Drawdown**: 3,789.96 points
- **Expectancy per Trade**: 1.11 points

### Annual Performance
| Year | Total Points | Trades | Avg Points/Trade | Win Rate |
|------|-------------|--------|------------------|----------|
| 2018 | 2,640.84    | 5,941  | 0.44             | 75.53%   |
| 2019 | 3,173.22    | 6,135  | 0.52             | 76.41%   |
| 2020 | 11,586.93   | 6,060  | 1.91             | 76.20%   |
| 2021 | 7,448.11    | 6,072  | 1.23             | 74.70%   |
| 2022 | 12,011.42   | 5,907  | 2.03             | 74.47%   |
| 2023 | 4,378.13    | 6,009  | 0.73             | 74.67%   |
| 2024 | 4,468.69    | 6,214  | 0.72             | 77.26%   |
| 2025 | 7,449.63    | 5,346  | 1.39             | 76.71%   |

### Best Performing Periods
- **Best Year**: 2022 (12,011.42 points)
- **Best Months**: March (12,071.36 points), October (13,296.65 points)
- **Maximum Win Streak**: 198 consecutive wins
- **Maximum Loss Streak**: 34 consecutive losses

### Trade Distribution
- **Long Trades**: 44,895 (75.38% win rate)
- **Short Trades**: 2,789 (81.61% win rate)

## Interpretation

### Key Observations
1. **High Win Rate**: The strategy achieves 75.74% win rate, indicating reliable entry signals
2. **Asymmetric Risk/Reward**: Average win (8.83 pts) is smaller than average loss (22.97 pts)
3. **Volume Advantage**: More long setups occur, but short setups have higher win rate
4. **Seasonal Patterns**: March and October show strongest performance
5. **Consistency**: Win rate remains stable across years (74-77%)

### For Discretionary Traders
Consider enhancing the mechanical signals with:
- Volume profile analysis at FVG zones
- Multiple timeframe confirmation
- Broader market context (trend, support/resistance)
- Quality assessment of validation candles
- News event awareness during the 02:00-06:00 session

### Risk Management
- All trades use defined stop losses based on swing points
- No positions held beyond the trading session
- Maximum risk per trade is predetermined
- Positive expectancy of 1.11 points per trade

## Script Features

### Core Components
1. **Data Loading**: Loads all 5m CSV files (2018-2025)
2. **Session Filtering**: Extracts only 02:00-06:00 data
3. **FVG Detection**: Identifies bearish and bullish fair value gaps
4. **Swing Point Detection**: Finds local highs/lows for stops/targets
5. **Trade Execution**: Simulates entries and exits based on strategy rules
6. **Performance Analysis**: Comprehensive statistics and reporting

### Analysis Metrics
- Global performance (trades, win rate, points, profit factor)
- Advanced statistics (drawdown, expectancy, streaks)
- Annual and monthly breakdowns
- Trade type distribution
- Qualitative insights

## Notes

### Strategy Rules
- No discretionary filters applied
- Mechanical implementation of exact strategy specification
- No optimization or curve fitting
- Uses only provided historical data
- No look-ahead bias

### Limitations
- Past performance does not guarantee future results
- Does not account for slippage or commissions
- Assumes perfect execution at specified prices
- Limited to 02:00-06:00 session only
- Requires clean, consistent data format

## File Structure
```
.
├── backtest_fvg_reversal.py    # Main backtest script
├── fvg_reversal_trades.csv     # Output: Detailed trade log
├── FVG_BACKTEST_README.md      # This file
├── 2018 5m.csv                 # Data files
├── 2019 5m.csv
├── ...
└── 2025 5m.csv
```

## License
This is a backtesting tool for educational and research purposes.

## Disclaimer
Trading futures involves substantial risk of loss. This backtest is for informational purposes only and does not constitute trading advice. Past performance is not indicative of future results.

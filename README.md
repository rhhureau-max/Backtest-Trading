# Backtest-Trading

## 8:30 Strategy Backtest System

A comprehensive Python backtest system for analyzing the 8:30 candle strategy on historical trading data from 2018 to 2025.

## Overview

This system backtests a trading strategy based on the 8:30 AM candle. The strategy identifies potential entry points when the 8:30 candle breaks above or below the previous 5 candles.

## Strategy Rules

### LONG Entry Conditions
- Close of 8:30 candle is **greater than** all closes of the previous 5 candles
- Close of 8:30 candle is **greater than** all highs of the previous 5 candles
- The 8:30 candle is bullish (Close > Open)

### SHORT Entry Conditions
- Close of 8:30 candle is **less than** all closes of the previous 5 candles
- Close of 8:30 candle is **less than** all lows of the previous 5 candles
- The 8:30 candle is bearish (Close < Open)

### Entry Point
- Entry at the close of the 8:30 candle

### Stop Loss Options
1. **SL 25%**: 25% retracement of the 8:30 candle body
2. **SL 50%**: 50% retracement of the 8:30 candle body
3. **SL 75%**: 75% retracement of the 8:30 candle body
4. **SL 100%**: 100% retracement (at the open level)
5. **SL Wick**: Below/above the wick with a small buffer

### Risk/Reward Ratios
Tested ratios: 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0

## Installation

```bash
# Clone the repository
git clone https://github.com/rhhureau-max/Backtest-Trading.git
cd Backtest-Trading

# Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
# Run the full backtest with default settings
python backtest_830_strategy.py

# Specify custom output directory
python backtest_830_strategy.py --output-dir my_results

# Backtest specific years
python backtest_830_strategy.py --years 2020-2023

# Backtest specific timeframes
python backtest_830_strategy.py --timeframes 5m,15m
```

## Output Files

The backtest generates the following files in the output directory:

1. **backtest_results.csv**: Detailed results for all SL/RR combinations
2. **trades_log.csv**: Individual trade log with entry/exit details
3. **backtest_report.md**: Comprehensive markdown report with analysis
4. **Charts**: Performance visualizations (PNG files)

## Project Structure

```
Backtest-Trading/
├── backtest_830_strategy.py   # Main backtest script
├── data_loader.py             # Data loading and preparation
├── strategy.py                # Strategy logic (entry, SL, TP)
├── metrics.py                 # Performance metrics calculation
├── report_generator.py        # Report and chart generation
├── requirements.txt           # Python dependencies
├── README.md                  # This file
└── [Data files]               # CSV data files (2018-2025)
```

## Data Format

CSV files use `;` as separator with columns:
- Column1: Date (DD/MM/YYYY)
- Column2: Time (HH:MM:SS)
- Column3: Open
- Column4: High
- Column5: Low
- Column6: Close
- Column7: Volume

## Metrics Calculated

- **Win Rate**: Percentage of winning trades
- **Profit Factor**: Total gains / Total losses
- **Expectancy**: Expected R per trade
- **Max Consecutive Wins/Losses**
- **Max Drawdown**
- **Direction Analysis**: Win rate by LONG/SHORT

## Requirements

- Python 3.8+
- pandas
- numpy
- matplotlib (optional, for charts)

## License

MIT License
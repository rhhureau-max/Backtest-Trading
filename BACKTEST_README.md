# Backtest Strategy Script - User Guide

## Overview
This repository contains a complete Python backtesting script (`backtest_strategy.py`) for testing quantitative trading strategies on Nasdaq (NQ) historical data.

## Features
- **Vectorized Operations**: Fast execution using pandas (no slow for loops)
- **Multiple Strategies**: Three built-in strategies to choose from
- **Flexible Timeframes**: Works with 1m, 5m, and 15m data
- **Session Filtering**: Automatically filters data to 01:00:00 - 05:00:00 session
- **Comprehensive Metrics**: Returns, Drawdown, Sharpe Ratio, Win Rate, and more

## Requirements
```bash
pip install pandas numpy
```

## Quick Start

### 1. Basic Usage
```python
# Open backtest_strategy.py and modify these lines:
csv_file = 'path/to/your/data.csv'  # Change to your CSV file path
strategy = 'ORB'  # Choose: 'ORB', 'RSI', or 'EMA'

# Run the script
python backtest_strategy.py
```

### 2. Data Format
Your CSV file must be semicolon-separated with these columns (with header row):
```
Column1;Column2;Column3;Column4;Column5;Column6;Column7
01/01/2025;17:00:00;21927.625319;21941.801108;21911.645339;21919.635329;444
```

Where:
- **Column1**: Date (DD/MM/YYYY)
- **Column2**: Time (HH:MM:SS)
- **Column3**: Open
- **Column4**: High
- **Column5**: Low
- **Column6**: Close
- **Column7**: Volume

## Available Strategies

### Strategy 1: Opening Range Breakout (ORB)
```python
strategy = 'ORB'
```
- Calculates High and Low of the first candle after 01:00:00
- **Buy Signal**: Price breaks above opening range high
- **Sell Signal**: Price breaks below opening range low

### Strategy 2: Mean Reversion (RSI)
```python
strategy = 'RSI'
```
- Uses 14-period RSI indicator
- **Buy Signal**: RSI < 30 (oversold)
- **Sell Signal**: RSI > 70 (overbought)

### Strategy 3: Trend Following (EMA Cross)
```python
strategy = 'EMA'
```
- Uses EMA(9) and EMA(21) crossovers
- **Buy Signal**: EMA(9) crosses above EMA(21)
- **Sell Signal**: EMA(9) crosses below EMA(21)

## Key Constraints

### ✅ What the Script Does
- ✅ Filters data to **01:00:00 - 05:00:00** session only
- ✅ Forces all positions to **close at 05:00:00**
- ✅ Uses **raw time values** (no timezone conversion)
- ✅ Calculates signals using vectorized pandas operations
- ✅ Computes comprehensive performance metrics

### ⚠️ Important Notes
- All positions are **automatically closed** at 05:00:00
- Data outside the 01:00:00 - 05:00:00 window is **filtered out**
- Times are used **as-is** from the CSV file

## Performance Metrics

The script calculates and displays:

| Metric | Description |
|--------|-------------|
| **Total Cumulative Return** | Overall strategy return percentage |
| **Maximum Drawdown** | Largest peak-to-trough decline |
| **Sharpe Ratio** | Risk-adjusted return (annualized) |
| **Total Signal Changes** | Number of position changes |
| **Winning Periods** | Number of profitable periods |
| **Losing Periods** | Number of loss periods |
| **Win Rate** | Percentage of winning periods |

## Example Output

```
************************************************************
STARTING BACKTEST - ORB STRATEGY
************************************************************
Loading data from: 2025 5m.csv
Loaded 61204 rows of data
Date range: 2025-01-01 00:00:00 to 2025-11-11 00:00:00

Filtering data for session 01:00:00 to 05:00:00...
Filtered to 10927 rows within session time

Applying Opening Range Breakout (ORB) Strategy...

============================================================
PERFORMANCE REPORT - ORB STRATEGY
============================================================

Total Cumulative Return: 2.12%
Maximum Drawdown: -4.32%
Sharpe Ratio (Annualized): 0.06

Total Signal Changes: 732
Winning Periods: 4931
Losing Periods: 5076
Win Rate: 49.28%
============================================================
```

## Advanced Usage

### Save Results to CSV
Uncomment these lines in the `main()` function:
```python
df_results.to_csv('backtest_results.csv', index=False)
print("\nResults saved to 'backtest_results.csv'")
```

### Customize Strategy Parameters
You can modify strategy parameters in the class methods:
- **RSI**: Change `period=14` in `strategy_rsi()`
- **EMA**: Change `fast_period=9, slow_period=21` in `strategy_ema()`

### Access Results Programmatically
```python
backtest = BacktestStrategy(csv_file_path='your_file.csv', strategy='ORB')
df_results, metrics = backtest.run()

# Access the dataframe
print(df_results.head())

# Access metrics dictionary
print(metrics['Total_Return'])
print(metrics['Sharpe_Ratio'])
```

## File Structure
```
Backtest-Trading/
├── backtest_strategy.py      # Main backtesting script
├── BACKTEST_README.md        # This documentation file
├── 2018 1m.csv.zip          # Historical data files
├── 2018 5m.csv
├── 2018 15m.csv
├── 2019 5m.csv
└── ... (more data files)
```

## Troubleshooting

### Issue: "No module named 'pandas'"
**Solution**: Install required packages
```bash
pip install pandas numpy
```

### Issue: "FileNotFoundError"
**Solution**: Use absolute path to your CSV file
```python
csv_file = '/full/path/to/your/file.csv'
```

### Issue: "Empty dataframe after filtering"
**Solution**: Ensure your data has timestamps between 01:00:00 and 05:00:00

## License
This script is provided for educational and research purposes.

## Support
For questions or issues, please refer to the code comments or modify the script according to your needs.

---

**Created**: December 2025  
**Version**: 1.0  
**Language**: Python 3.x

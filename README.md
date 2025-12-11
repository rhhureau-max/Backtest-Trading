# Backtest-Trading

Repository containing OHLC data and backtesting scripts for trading analysis.

## Impulsive Candle Continuation Analysis

The `backtest_impulsive_candles.py` script analyzes the probability of continuation after an impulsive candle on 1m, 5m, and 15m timeframes.

### Definition

An **impulsive candle** is defined as:
- A candle whose range (High - Low) OR body (|Close - Open|) is greater than the maximum of the previous 10 candles
- AND that breaks a previous FVG (Fair Value Gap) or a previous high/low

### Metrics Calculated

For each timeframe (1m, 5m, 15m), the script calculates:
1. Total number of impulsive signals
2. Probability that the next candle continues in the same direction
3. Probability of reversal
4. Separate statistics for bullish vs bearish movements

### Requirements

- Python 3.8+
- pandas
- numpy

Install dependencies:
```bash
pip install pandas numpy
```

### Usage

```bash
python backtest_impulsive_candles.py
```

### Data Files

The repository contains OHLC CSV data files for years 2018-2025:
- `YYYY 1m.csv` or `YYYY 1m.csv.zip` - 1-minute data
- `YYYY 5m.csv` - 5-minute data
- `YYYY 15m.csv` - 15-minute data

CSV files use semicolon (`;`) as delimiter with columns: Date, Time, Open, High, Low, Close, Volume
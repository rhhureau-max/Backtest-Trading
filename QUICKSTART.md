# Quick Start Guide

This guide will help you get started with the backtest strategy in just a few steps.

## Prerequisites

- Python 3.7+ installed
- CSV data files (1m, 5m, 15m) for the years you want to analyze

## Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

## Running the Backtest

### Step 1: Run the Basic Backtest

```bash
python3 backtest_strategy.py
```

This will:
- Process all available CSV files (2018-2025)
- Analyze 1m, 5m, and 15m timeframes
- Generate result files

**Output files:**
- `backtest_results.csv` - All trades combined
- `backtest_results_1m.csv` - 1-minute timeframe trades
- `backtest_results_5m.csv` - 5-minute timeframe trades
- `backtest_results_15m.csv` - 15-minute timeframe trades

### Step 2: Analyze the Results (Optional)

```bash
python3 analyze_results.py
```

This provides additional insights:
- Trades by year and month
- Price level analysis
- Breakout magnitude statistics
- Candle characteristics

## Understanding the Results

### Result Columns

Each row in the results represents a trade signal:

| Column | Meaning |
|--------|---------|
| Date | When the trade signal occurred |
| Time | Always 08:30:00 (the time we're analyzing) |
| Timeframe | 1m, 5m, or 15m |
| Candle_Type | BULLISH or BEARISH |
| Open/High/Low/Close | Price levels of the 8:30 AM candle |
| Reference_Level | The level that was broken (max high or min low of previous 5 candles) |
| Condition | Description of what condition was met |

### Example Trade

```csv
Date,Time,Timeframe,Candle_Type,Open,High,Low,Close,Reference_Level,Condition
03/01/2018,08:30:00,5m,BULLISH,7646.08,7661.90,7645.50,7660.73,7651.35,"Close (7660.73) > Reference (7651.35)"
```

This means:
- On January 3, 2018 at 8:30 AM (5-minute candle)
- The candle was bullish (closed higher than it opened)
- The close price (7660.73) was above the highest high of the previous 5 candles (7651.35)
- This is a valid trade signal

## Strategy Explanation

### Bullish Signal
When the 8:30 AM candle:
1. Closes higher than it opened (bullish)
2. Closes ABOVE the highest high of the previous 5 candles

### Bearish Signal
When the 8:30 AM candle:
1. Closes lower than it opened (bearish)
2. Closes BELOW the lowest low of the previous 5 candles

## Customization

Edit `backtest_strategy.py` to customize:

```python
# Change years to analyze
self.years = list(range(2020, 2024))  # Only 2020-2023

# Change timeframes
self.timeframes = ['5m', '15m']  # Only 5m and 15m

# Change time to analyze (currently 08:30:00)
df_830 = df[df['Time'] == '09:00:00']  # Analyze 9:00 AM instead

# Change lookback period (currently 5 candles)
if original_idx >= 10:  # Look back 10 candles instead of 5
    prev_10 = df.iloc[original_idx-10:original_idx]
```

## Typical Workflow

1. **Initial Run**: `python3 backtest_strategy.py`
2. **Review Summary**: Check the console output for overview statistics
3. **Open Results**: Open `backtest_results.csv` in Excel or any CSV viewer
4. **Detailed Analysis**: `python3 analyze_results.py` for deeper insights
5. **Filter Results**: Use Excel/Python to filter by date, timeframe, or candle type

## Troubleshooting

### "File not found" errors
- Ensure your CSV files follow the naming convention: `YYYY {timeframe}.csv`
- For zipped files: `YYYY {timeframe}.csv.zip`
- Valid timeframe names: `1m`, `5m`, `15m`

### "No module named 'pandas'" error
```bash
pip install pandas numpy
```

### Memory errors with large files
- Process one year at a time by modifying `self.years`
- Or process one timeframe at a time

### Incorrect results
- Verify your CSV file format matches the expected structure
- Check that dates are in DD/MM/YYYY format
- Check that times are in HH:MM:SS format
- Ensure semicolon (;) delimiter is used

## Next Steps

1. Review the results to identify patterns
2. Filter trades by specific criteria (date ranges, price levels, etc.)
3. Backtest the trades to evaluate profitability
4. Optimize parameters (lookback period, time of day, etc.)
5. Apply risk management rules

## Support

For issues or questions:
1. Check the main README.md for detailed documentation
2. Review the code comments in `backtest_strategy.py`
3. Open an issue in the repository

## Performance Tips

- The 1m data is typically the largest; processing it takes the most time
- First-time runs require extracting zipped files
- Subsequent runs are faster as pandas caches some operations
- Consider processing years in parallel for large datasets

Happy backtesting! 🚀

# Quick Start Guide - Backtest Strategy

## 🚀 Get Started in 3 Steps

### Step 1: Install Dependencies
```bash
pip install pandas numpy
```

### Step 2: Edit the Configuration
Open `backtest_strategy.py` and modify lines 349-352:

```python
# Change this to your CSV file path
csv_file = 'path/to/your/data.csv'

# Choose your strategy: 'ORB', 'RSI', or 'EMA'
strategy = 'ORB'
```

### Step 3: Run the Script
```bash
python backtest_strategy.py
```

That's it! 🎉

---

## 📊 Example Output

```
************************************************************
STARTING BACKTEST - ORB STRATEGY
************************************************************
Loading data from: 2025 5m.csv
Loaded 61204 rows of data
Date range: 2025-01-01 to 2025-11-11

Filtering data for session 01:00:00 to 05:00:00...
Filtered to 10927 rows within session time

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

---

## 🎯 Available Strategies

### 1. ORB (Opening Range Breakout)
```python
strategy = 'ORB'
```
- Trades breakouts from first candle after 01:00:00
- Long on break above, Short on break below

### 2. RSI (Mean Reversion)
```python
strategy = 'RSI'
```
- Long when RSI(14) < 30
- Short when RSI(14) > 70

### 3. EMA (Trend Following)
```python
strategy = 'EMA'
```
- Long when EMA(9) crosses above EMA(21)
- Short when EMA(9) crosses below EMA(21)

---

## 📁 Your Data Format

CSV file with semicolon separator:
```
Column1;Column2;Column3;Column4;Column5;Column6;Column7
01/01/2025;17:00:00;21927.62;21980.72;21911.64;21975.04;1482
```

Columns: Date | Time | Open | High | Low | Close | Volume

---

## 💡 Pro Tips

1. **Test all strategies**: Change the `strategy` variable to compare
2. **Different timeframes**: Works with 1m, 5m, and 15m data
3. **Save results**: Uncomment lines in `main()` to save to CSV
4. **See examples**: Check `example_usage.py` for more advanced usage

---

## 📚 Documentation

- **BACKTEST_README.md** - Comprehensive documentation
- **example_usage.py** - Usage examples
- **IMPLEMENTATION_SUMMARY.md** - Technical details

---

## ✅ What It Does

- ✅ Filters data to 01:00:00 - 05:00:00 session
- ✅ Closes all positions at 05:00:00
- ✅ Uses vectorized pandas (fast!)
- ✅ No timezone conversion
- ✅ Calculates comprehensive metrics

---

## 🆘 Need Help?

**Problem**: Module not found
```bash
pip install pandas numpy
```

**Problem**: File not found
- Use absolute path to your CSV file

**Problem**: No data after filtering
- Ensure your data has times between 01:00:00 and 05:00:00

---

Happy backtesting! 📈

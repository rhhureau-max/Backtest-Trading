# Quick Start Guide

## 🚀 Get Started in 3 Steps

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Your First Backtest
```bash
python3 ict_backtest.py
```

This runs the default configuration (Strategy A with Risk Mode 1).

### 3. Customize Your Test

Edit the **CONFIGURATION** section at the top of `ict_backtest.py`:

```python
# Strategy Selection: Choose 'A', 'B', or 'C'
STRATEGY = 'B'  # Try Strategy B (Power of 3)

# Risk Management Mode: Choose 1, 2, or 3
RISK_MODE = 2   # Try Risk Mode 2 (Swing Session)
```

Run again:
```bash
python3 ict_backtest.py
```

## 📊 Expected Output

```
============================================================
ICT TRADING STRATEGIES BACKTEST SYSTEM
============================================================

📊 CONFIGURATION:
  Strategy: B - Power of 3 Intraday (Open Deviation)
  Risk Mode: 2 - Swing Session
  Timeframe: 5m
  Years: 2018 - 2025
  Trading Window: 01:00:00 - 05:00:00
  Initial Capital: $100,000

📂 Loading data...
✓ Loaded multiple CSV files
============================================================
Total data loaded: 554554 rows
Date range: 2018-01-01 to 2025-11-11
============================================================

🕐 Filtering to trading hours (01:00-05:00)...
  Rows after filtering: 99515

🎯 Applying Strategy B: Power of 3 Intraday...
  Generated 7228 signals

⚙️  Running backtest...
  Completed 3207 trades

📈 Calculating performance metrics...

============================================================
BACKTEST RESULTS
============================================================
  Total Trades.......................                3,207
  Winning Trades.....................                1,391
  Losing Trades......................                1,816
  Win Rate (%).......................                43.37
  Profit Factor......................                 1.14
  Total PnL..........................             8,075.22
  Gross Profit.......................            71,039.84
  Gross Loss.........................            62,964.62
  Initial Capital....................              100,000
  Final Equity.......................           108,075.22
  Return (%).........................                 8.08
============================================================

📋 Sample Trades (First 10):
          EntryTime            ExitTime Direction  EntryPrice   ExitPrice      PnL ExitReason
2018-01-02 01:40:00 2018-01-02 05:00:00     Short 7523.954376 7497.783436    26.17   HardExit
2018-01-03 01:15:00 2018-01-03 05:00:00      Long 7641.981863 7649.889785     7.91   HardExit
...

💾 Full results saved to: backtest_results_B_mode2_5m.csv

✅ Backtest complete!
```

## 🧪 Test All Configurations

Want to test all 9 combinations (3 strategies × 3 risk modes)?

```bash
python3 example_batch_test.py
```

This generates a comparison report showing which configuration performs best!

## 📖 Learn More

- **Full Documentation**: See [ICT_BACKTEST_README.md](ICT_BACKTEST_README.md)
- **Strategy Details**: Each strategy is fully documented in the README
- **Risk Management**: Learn about the 3 different risk modes
- **Advanced Usage**: Batch testing, parameter tuning, and more

## 🎯 Quick Tips

1. **Start with Strategy B + Mode 2** - Historically the best performing
2. **Compare multiple modes** - Different market conditions favor different approaches
3. **Review the CSV output** - Detailed trade-by-trade analysis
4. **Adjust timeframes** - Test with '1m', '5m', or '15m' data

## ⚙️ Configuration Options

```python
# Change strategy
STRATEGY = 'A'  # Judas Swing
STRATEGY = 'B'  # Power of 3 (Best returns)
STRATEGY = 'C'  # Displacement

# Change risk mode
RISK_MODE = 1   # Scalper (15/30 pts)
RISK_MODE = 2   # Swing (40/100 pts) - Best for trends
RISK_MODE = 3   # Dynamic ATR-based

# Change timeframe
DATA_TIMEFRAME = '5m'   # Recommended for most strategies
DATA_TIMEFRAME = '1m'   # More signals, slower processing
DATA_TIMEFRAME = '15m'  # Fewer signals, faster processing

# Change date range
START_YEAR = 2018
END_YEAR = 2025
```

Happy backtesting! 🚀

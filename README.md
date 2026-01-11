# Backtest-Trading

## NQ Futures - First FVG Inversion Strategy Backtest

This repository contains a comprehensive backtesting script for testing the "First FVG Inversion" strategy on NQ (Nasdaq 100) Futures using 3-minute timeframe data.

### Strategy Overview

**Strategy Name:** First FVG Inversion (One Bullet Rule)  
**Timeframe:** 3-minute (resampled from 1-minute data)  
**Period:** 2018-2024  
**Trading Sessions:**
- **London Killzone:** 01:00 - 04:00 CT
- **New York Killzone:** 08:30 - 11:00 CT

### Fair Value Gap (FVG) Definition

- **Bearish FVG:** Created when `Low[i-2] > High[i]`. Gap exists between `High[i]` and `Low[i-2]`.
- **Bullish FVG:** Created when `High[i-2] < Low[i]`. Gap exists between `High[i-2]` and `Low[i]`.

### Entry Rules

1. **LONG Signal:** Price creates a Bearish FVG, then a later candle closes ABOVE the top of that Bearish FVG
2. **SHORT Signal:** Price creates a Bullish FVG, then a later candle closes BELOW the bottom of that Bullish FVG

### "One Bullet" Rule

- Take **ONLY the FIRST valid inversion signal** within each trading session
- Once a trade is triggered, stop trading for the rest of that session
- Reset at the start of the New York session to allow one new trade

### Risk Management

- **Entry:** At the close of the signal candle
- **Stop Loss:**
  - Long: Just below the low of the signal candle
  - Short: Just above the high of the signal candle
- **Take Profit:** 1:1 Risk-to-Reward Ratio

### Installation

```bash
pip install pandas numpy matplotlib
```

### Usage

Run the backtest script:

```bash
python3 fvg_inversion_backtest.py
```

### Output Files

The script generates three output files:

1. **backtest_results.md** - Comprehensive markdown report with all performance metrics and statistics
2. **equity_curve.png** - Visual representation of the cumulative equity curve
3. **trade_log.csv** - Detailed log of all trades with entry/exit prices, PnL, etc.

### Sample Results (2018-2024)

```
OVERALL PERFORMANCE
  Total Trades:        3,615
  Win Rate:            38.78%
  Profit Factor:        0.90
  Net Profit (Points): -2,300.37

LONDON SESSION
  Total Trades:        1,809
  Win Rate:            38.47%
  Profit Factor:        0.87
  Net Profit (Points):  -662.49

NEW YORK SESSION
  Total Trades:        1,806
  Win Rate:            39.09%
  Profit Factor:        0.91
  Net Profit (Points): -1,637.89
```

### Data Format

The script expects 1-minute data files in the following format:
- **Separator:** Semicolon (;)
- **Columns:** Date, Time, Open, High, Low, Close, Volume
- **Date Format:** DD/MM/YYYY
- **Time Format:** HH:MM:SS
- **Timezone:** Chicago Time (CT)

### Script Features

- ✅ Automatic data extraction from zip files
- ✅ Proper OHLC resampling from 1-minute to 3-minute
- ✅ FVG identification and tracking
- ✅ Session-based trade execution
- ✅ "One Bullet" rule implementation
- ✅ Comprehensive performance reporting
- ✅ Equity curve visualization
- ✅ Detailed trade logging

### Author

Created by a Senior Quantitative Trader and Python Developer
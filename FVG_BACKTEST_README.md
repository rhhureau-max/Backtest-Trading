# Inverse FVG (Fair Value Gap) Trading Strategy Backtest

This script backtests an Inverse FVG trading strategy on NQ futures data.

## Overview

The Inverse FVG strategy trades **against** traditional Fair Value Gap fills:
- **LONG** when price crosses **above** a Bearish FVG's high zone
- **SHORT** when price crosses **below** a Bullish FVG's low zone

## Requirements

- Python 3.x
- pandas library

Install dependencies:
```bash
pip install pandas
```

## Usage

Run the backtest:
```bash
python3 fvg_backtest.py
```

The script will automatically:
1. Load 5-minute and 15-minute data from "2025 5m.csv" and "2025 15m.csv"
2. Run backtests for both timeframes
3. Display detailed results and a comparison table

## Strategy Rules

### Trading Session
- **Session hours**: 01:00 - 05:00 only
- **Daily reset**: All FVGs cleared at 01:00 each day
- **Session close**: Open positions closed at 05:00 at closing price

### FVG Detection (01:00-05:00 only)
- **Bearish FVG**: When Low[t-2] > High[t]
  - Zone: High_Zone = Low[t-2], Low_Zone = High[t]
- **Bullish FVG**: When High[t-2] < Low[t]
  - Zone: High_Zone = Low[t], Low_Zone = High[t-2]

### Entry Signals (INVERSE)
- **LONG**: Close crosses ABOVE High_Zone of a Bearish FVG
- **SHORT**: Close crosses BELOW Low_Zone of a Bullish FVG

### Risk Management
- **Position limit**: One position at a time
- **Stop Loss**: 
  - LONG: Lowest low of signal candle
  - SHORT: Highest high of signal candle
- **Take Profit**: 1:2 Risk/Reward ratio (TP = 2 × SL distance)

## Output

The script displays:
- Win Rate (%)
- Total number of trades
- Cumulative P&L (in points)
- Profit Factor (Gross Profit / Gross Loss)
- Detailed statistics for each timeframe
- Comparison table between 5m and 15m results

## Example Output

```
================================================================================
INVERSE FVG STRATEGY BACKTEST RESULTS - COMPARISON TABLE
================================================================================
Metric                    5-Minute                  15-Minute                
--------------------------------------------------------------------------------
Win Rate                                 35.51%                40.58%
Total Trades                                   766                      207
Cumulative P&L (pts)                   1038.71              1706.24
Profit Factor                                 1.12                     1.50
--------------------------------------------------------------------------------
```

## Data Format

Expected CSV format (semicolon-separated):
```
Column1;Column2;Column3;Column4;Column5;Column6;Column7
Date;Time;Open;High;Low;Close;Volume
01/01/2025;17:00:00;21927.625319;21980.720091;21911.645339;21975.049775;1482
```

## Notes

- The strategy only processes bars during the 01:00-05:00 trading session
- FVGs are only valid for the session in which they were created
- Each FVG can only trigger one trade (marked as "used" after entry)
- Positions are closed immediately at session end (05:00) if still open

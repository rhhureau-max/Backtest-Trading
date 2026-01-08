# Fair Value Gap (FVG) Trading Strategy Backtest

## Overview
This is a complete Python backtest implementation for a Fair Value Gap (FVG) trading strategy on Nasdaq (NQ) 1-minute data from 2018 to 2025.

## Strategy Description

### Trading Parameters
- **Instrument**: NQ (Nasdaq Futures)
- **Timeframe**: 1-minute
- **Killzone**: 08:30 - 11:00 Chicago Time
- **Max Trades**: 1 per day (first signal only)
- **Risk-Reward Ratio**: 1.5
- **Stop Loss Offset**: 0.5 points

### Fair Value Gap Identification

#### Bearish FVG (Short Setup)
- Condition: `Low[i-2] > High[i]`
- Entry: 50% of the gap (middle)
- Stop Loss: `High[i-2] + 0.5`
- Take Profit: `Entry - (Risk × 1.5)`

#### Bullish FVG (Long Setup)
- Condition: `High[i-2] < Low[i]`
- Entry: 50% of the gap (middle)
- Stop Loss: `Low[i-2] - 0.5`
- Take Profit: `Entry + (Risk × 1.5)`

### Execution Rules
1. Scan for FVG starting from 08:30 close
2. Only take the first valid FVG signal per day
3. Use limit orders at 50% gap entry
4. Check tick-by-tick for entry fill
5. Exit at either Stop Loss or Take Profit (whichever hits first)
6. Cancel unfilled orders at 11:00

## Files

### Main Script
- `fvg_backtest.py` - Complete backtest implementation

### Output Files
- `fvg_backtest_results.csv` - Detailed trade log with all executed trades

## Usage

### Running the Backtest
```bash
python3 fvg_backtest.py
```

### Requirements
- Python 3.7+
- pandas
- numpy
- pytz

Install dependencies:
```bash
pip install pandas numpy pytz
```

## Backtest Results Summary

### Overall Performance (2018-2025)
- **Total Trades**: 1,795
- **Winning Trades**: 831 (46.30%)
- **Losing Trades**: 964 (53.70%)
- **Total PnL**: +2,314.40 points
- **Average Win**: +41.04 points
- **Average Loss**: -32.97 points
- **Profit Factor**: 1.07
- **Maximum Drawdown**: -1,850.48 points
- **Sharpe Ratio**: 0.43

### Yearly Performance
| Year | PnL (points) | Trades | Win Rate |
|------|-------------|---------|----------|
| 2018 | -42.98 | 23 | 34.8% |
| 2019 | +101.28 | 258 | 48.4% |
| 2020 | +2,038.63 | 259 | 50.6% |
| 2021 | +329.81 | 258 | 45.3% |
| 2022 | -1,041.39 | 258 | 43.4% |
| 2023 | +138.73 | 257 | 45.1% |
| 2024 | -77.45 | 259 | 44.4% |
| 2025 | +867.76 | 223 | 48.0% |

## Code Structure

### Main Classes

#### `FVGBacktest`
The main backtest engine that handles:
- Data loading from CSV and ZIP files
- Timezone conversion to Chicago time
- FVG identification (both bullish and bearish)
- Trade execution with limit orders
- Performance metric calculation
- Results export

### Key Methods

#### `load_data()`
Loads all 1-minute data files (2018-2025), handles both `.csv` and `.csv.zip` formats, and combines them into a single DataFrame.

#### `identify_fvg(df, idx)`
Identifies Fair Value Gaps at a given candle index:
- Checks for bearish FVG: `Low[i-2] > High[i]`
- Checks for bullish FVG: `High[i-2] < Low[i]`
- Calculates entry, stop loss, and take profit levels

#### `execute_trade(df, setup, start_idx)`
Executes trades based on FVG setup:
- Checks if limit order gets filled (price touches entry level)
- Monitors subsequent candles for SL or TP hit
- Returns trade result with entry/exit details

#### `calculate_metrics()`
Calculates comprehensive performance metrics:
- Win rate, profit factor, Sharpe ratio
- Maximum drawdown
- Average win/loss
- Gross profit/loss

## Data Format

### Input CSV Format
- Separator: semicolon (`;`)
- Columns: Date, Time, Open, High, Low, Close, Volume
- Date format: DD/MM/YYYY
- Time format: HH:MM:SS
- Example: `01/01/2018;17:00:00;7503.74;7509.30;7499.64;7506.96;822`

### Output CSV Format
The results file contains:
- `type`: LONG or SHORT
- `entry_price`: Trade entry price
- `exit_price`: Trade exit price
- `stop_loss`: Stop loss level
- `take_profit`: Take profit level
- `entry_time`: Entry timestamp
- `exit_time`: Exit timestamp
- `result`: WIN or LOSS
- `pnl`: Profit/Loss in points
- `signal_time`: When FVG signal was identified

## Notes

### Key Features
- ✅ Handles both CSV and ZIP compressed files
- ✅ Accurate timezone conversion (Chicago/America/Chicago)
- ✅ Tick-by-tick execution simulation
- ✅ Strict killzone enforcement (08:30-11:00)
- ✅ One trade per day limit
- ✅ Comprehensive performance metrics
- ✅ Trade log export for analysis

### Strategy Characteristics
- The strategy shows positive overall performance (+2,314 points)
- Best year: 2020 (+2,038 points)
- Worst year: 2022 (-1,041 points)
- Win rate hovers around 45-50%
- Profit factor of 1.07 indicates slight edge
- Average wins are larger than average losses (positive expectancy)

## License
This backtest implementation is provided for educational and research purposes.

## Author
Created by AI Trading System
Date: January 2026

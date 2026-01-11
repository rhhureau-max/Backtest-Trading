# FVG Inversion Backtest Script

This Python script backtests the Fair Value Gap (FVG) Inversion strategy on NQ Futures data.

## Requirements

- Python 3.7+
- pandas
- numpy
- matplotlib

Install dependencies:
```bash
pip install -r requirements.txt
```

## Input Data Format

The script expects a CSV file named `NQ_1min_2018_2024.csv` with the following format:

- **Separator**: Semicolon (`;`)
- **Columns**: Date, Time, Open, High, Low, Close, Volume
- **Date Format**: DD/MM/YYYY
- **Time Format**: HH:MM:SS
- **Timezone**: Chicago Time (CT)

Example:
```
Column1;Column2;Column3;Column4;Column5;Column6;Column7
01/01/2018;17:00:00;7503.74;7511.94;7499.64;7511.35;1451
01/01/2018;17:01:00;7510.77;7516.04;7510.77;7512.53;360
...
```

## Strategy Overview

### FVG Detection (on 3-minute bars)

- **Bearish FVG**: Created when `Low[i-2] > High[i]`
  - Gap range: `High[i]` to `Low[i-2]`
  
- **Bullish FVG**: Created when `High[i-2] < Low[i]`
  - Gap range: `High[i-2]` to `Low[i]`

### Entry Signals

1. **LONG Entry**: When a bearish FVG exists and a subsequent 3-minute candle closes **above** the top of that FVG
2. **SHORT Entry**: When a bullish FVG exists and a subsequent 3-minute candle closes **below** the bottom of that FVG

### Trading Sessions (Chicago Time)

- **London Killzone**: 01:00 - 04:00
- **New York Killzone**: 08:30 - 11:00

### One Bullet Rule

Only the **first valid signal** per session is taken. After one trade in a session, no more trades are taken until the next session starts. The session counter resets at the beginning of the New York session.

### Risk Management

- **Entry Price**: Close of the signal candle
- **Stop Loss**: 
  - Long: Below the low of the signal candle
  - Short: Above the high of the signal candle
- **Take Profit**: 1:1 Risk-to-Reward ratio

## Usage

```bash
python fvg_inversion_backtest.py
```

## Output

The script generates:

1. **Console Output**: Detailed statistics including:
   - Overall statistics (Total trades, Win rate, Profit factor, Net profit)
   - Per-session statistics (London and New York)

2. **Markdown Report**: `fvg_inversion_results.md` - Comprehensive backtest report with formatted tables and statistics

3. **CSV File**: `fvg_inversion_trades.csv` - Detailed trade log with all entry/exit information

4. **Equity Curve**: `fvg_inversion_equity_curve.png` - Visual representation of cumulative profit/loss over time

## Example Output

```
======================================================================
BACKTEST RESULTS - FVG INVERSION STRATEGY
======================================================================

OVERALL STATISTICS:
  Total Trades:    150
  Winning Trades:  82
  Losing Trades:   68
  Win Rate:        54.67%
  Profit Factor:   1.45
  Net Profit:      245.50 points
  Gross Profit:    892.25 points
  Gross Loss:      646.75 points

----------------------------------------------------------------------
STATISTICS BY SESSION:
----------------------------------------------------------------------

LONDON SESSION:
  Total Trades:    65
  Winning Trades:  35
  Losing Trades:   30
  Win Rate:        53.85%
  Profit Factor:   1.38
  Net Profit:      95.25 points

NEW YORK SESSION:
  Total Trades:    85
  Winning Trades:  47
  Losing Trades:   38
  Win Rate:        55.29%
  Profit Factor:   1.51
  Net Profit:      150.25 points

======================================================================
```

## Script Structure

The script is organized as a class-based system:

### Main Class: `FVGInversionBacktest`

Key methods:
- `load_and_preprocess_data()`: Loads and parses the CSV file
- `resample_to_3min()`: Converts 1-minute data to 3-minute bars
- `detect_fvgs()`: Identifies Fair Value Gaps in the data
- `get_session()`: Determines which trading session a datetime belongs to
- `run_backtest()`: Executes the main backtest logic
- `generate_statistics()`: Calculates and displays performance metrics
- `plot_equity_curve()`: Creates the equity curve visualization
- `export_trades()`: Saves trade details to CSV

## Notes

- The script assumes all timestamps are in Chicago Time (CT)
- Only trades within the specified killzone sessions are executed
- The script handles proper OHLC aggregation when resampling from 1-minute to 3-minute bars
- All prices are in points (NQ Futures standard notation)

## Troubleshooting

### File Not Found Error
Ensure `NQ_1min_2018_2024.csv` exists in the same directory as the script.

### Module Import Errors
Install required dependencies: `pip install pandas numpy matplotlib`

### No Trades Executed
- Verify your data covers the London (01:00-04:00) and New York (08:30-11:00) sessions
- Check that the data format matches the expected format (semicolon-separated)
- Ensure timestamps are in Chicago Time

## License

This script is provided as-is for educational and backtesting purposes.

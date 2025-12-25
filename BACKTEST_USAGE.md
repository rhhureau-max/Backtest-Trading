# Judas Swing + FVG Inversion Backtest - Usage Guide

## Overview
This backtesting script implements the "Judas Swing + FVG Inversion" trading strategy for Nasdaq 100 (NQ) 5-minute data.

## Strategy Description

### Session Definitions (Chicago Time)
- **Asia Session**: 18:00 (previous day) to 23:00 (previous day)
- **London Killzone**: 01:00 to 04:00 (current day)

### Entry Logic
During the London Killzone (01:00-04:00):

**LONG Setup:**
1. Price goes below Asia_Low
2. Bearish FVG forms (gap between high of candle n-2 and low of candle n)
3. Current candle closes above the FVG high
4. Enter LONG at close

**SHORT Setup:**
1. Price goes above Asia_High
2. Bullish FVG forms (gap between low of candle n-2 and high of candle n)
3. Current candle closes below the FVG low
4. Enter SHORT at close

**Note:** Only ONE entry per day (first valid signal)

### Risk Management
Three scenarios are tested for each trade:
- **Scenario A**: SL = 20 points / TP = 20 points (Ratio 1:1)
- **Scenario B**: SL = 20 points / TP = 30 points (Ratio 1:1.5)
- **Scenario C**: SL = 20 points / TP = 40 points (Ratio 1:2)

### Exit Rules
- Close when price touches SL or TP
- If neither is hit by 12:00 Chicago, close at market (Time Stop)

## Data Format
The script expects CSV files with the following format:
- **Separator**: Semicolon (;)
- **Columns**: Date;Time;Open;High;Low;Close;Volume
- **Date Format**: DD/MM/YYYY
- **Time Format**: HH:MM:SS
- **Example**: `01/01/2024;17:00:00;18244.57923;18248.331274;18238.951165;18241.631196;1308`

## Installation

### Requirements
```bash
pip install pandas numpy
```

## Usage

### Basic Usage
Simply run the script - it will automatically find and test the first 5-minute CSV file in the directory:

```bash
python judas_swing_fvg_backtest.py
```

### Programmatic Usage
You can also import and use the functions in your own scripts:

```python
from judas_swing_fvg_backtest import run_backtest, run_comparative_analysis

# Test a single scenario
result = run_backtest('2024 5m.csv', tp_points=30)
print(f"Total Trades: {result['total_trades']}")
print(f"Win Rate: {result['win_rate']:.2f}%")
print(f"Net Profit: {result['net_profit']:.2f} points")

# Run all three scenarios and get comparative table
results_df = run_comparative_analysis('2024 5m.csv')
print(results_df)
```

### Testing Specific Files
To test a specific CSV file, modify the `main()` function in the script or use it programmatically.

## Output

### Console Output
The script displays:
- Progress information for each scenario
- Detailed results for each test (Total Trades, Win Rate, Net Profit, Profit Factor, Max Drawdown)
- A comparative results table

### CSV Output
Results are saved to `backtest_results.csv` with columns:
- Scenario
- Total Trades
- Win Rate (%)
- Net Profit (Points)
- Profit Factor
- Max Drawdown (Points)

## Example Output

```
================================================================================
COMPARATIVE RESULTS TABLE
================================================================================

          Scenario  Total Trades Win Rate (%) Net Profit (Points) Profit Factor Max Drawdown (Points)
  Scenario A (1:1)           179        50.84              117.19          1.07                200.00
Scenario B (1:1.5)           179        40.78              107.19          1.05                250.00
  Scenario C (1:2)           179        34.08               97.19          1.04                420.00

================================================================================
```

## Metrics Explanation

- **Total Trades**: Number of trades executed
- **Win Rate**: Percentage of profitable trades
- **Net Profit**: Total profit/loss in points
- **Profit Factor**: Gross profit divided by gross loss (>1 is profitable)
- **Max Drawdown**: Maximum peak-to-trough decline in points

## Features

- ✅ Modular design with reusable functions
- ✅ Handles missing data gracefully
- ✅ Tests multiple risk-reward scenarios automatically
- ✅ Generates comparative analysis
- ✅ Exports results to CSV
- ✅ Detailed trade logging
- ✅ Proper FVG detection logic
- ✅ Time-based session filtering

## Code Structure

### Main Classes
- `JudasSwingFVGBacktest`: Core backtesting engine

### Key Methods
- `load_data()`: Loads and prepares CSV data
- `identify_asia_session()`: Calculates Asia session high/low
- `detect_bearish_fvg()`: Identifies bearish Fair Value Gaps
- `detect_bullish_fvg()`: Identifies bullish Fair Value Gaps
- `manage_trade()`: Handles trade execution and exit
- `run_backtest()`: Executes complete backtest for one scenario

### Utility Functions
- `run_backtest(csv_file, tp_points)`: Standalone backtest function
- `run_comparative_analysis(csv_file)`: Tests all three scenarios

## Notes

- All times are in Chicago timezone (UTC-5)
- The script processes 5-minute candle data only
- Each trading day allows only one trade (first valid signal)
- FVG gaps must exist (no overlap between relevant candles)
- Trades are closed by SL, TP, or time stop (12:00 Chicago)

## Troubleshooting

**Issue**: `ModuleNotFoundError: No module named 'pandas'`
**Solution**: Install required packages: `pip install pandas numpy`

**Issue**: No CSV files found
**Solution**: Ensure 5-minute CSV files (format: `*5m.csv`) are in the same directory as the script

**Issue**: No trades detected
**Solution**: Verify that:
- Data format matches expected format (semicolon-separated)
- Date/time formats are correct (DD/MM/YYYY and HH:MM:SS)
- Data includes both Asia session (18:00-23:00) and London Killzone (01:00-04:00) hours

## License
This script is provided as-is for backtesting purposes.

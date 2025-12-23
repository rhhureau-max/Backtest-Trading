# Backtesting Strategy: 8:30 Candle Wick Breakout

## Overview

This backtesting solution identifies all trades where the 8:30 candle exceeds the wicks of the last 5 candles across three different timeframes (1m, 5m, 15m) from 2018 to 2025.

## Strategy Rules

The strategy identifies two types of breakouts:

1. **Bullish Breakout**: When the 8:30 candle's high exceeds the highest wick (high) of the previous 5 candles
2. **Bearish Breakout**: When the 8:30 candle's low goes below the lowest wick (low) of the previous 5 candles

## Requirements

- Python 3.6 or higher
- pandas library

### Installation

```bash
pip install pandas
```

## Usage

### Basic Usage

Simply run the script from the repository root directory:

```bash
python3 backtest_830_strategy.py
```

The script will:
1. Automatically detect and process all CSV files from 2018 to 2025
2. Handle both zipped (2018-2024 for 1m) and unzipped CSV files
3. Analyze all three timeframes (1m, 5m, 15m)
4. Generate comprehensive reports

## Output Files

The script generates two types of reports with timestamps:

### 1. Text Report (`backtest_report_YYYYMMDD_HHMMSS.txt`)

A detailed human-readable report containing:
- Summary statistics for each timeframe
- Complete details of every trade including:
  - Date and time
  - Direction (Bullish, Bearish, or Both)
  - OHLC values
  - Previous 5 candles' max high and min low
  - Breakout amounts

### 2. CSV Report (`backtest_trades_YYYYMMDD_HHMMSS.csv`)

A machine-readable CSV file with all trades that can be imported into Excel or other analysis tools.

Columns:
- `Timeframe`: 1m, 5m, or 15m
- `Date`: Trade date (DD/MM/YYYY)
- `Time`: Trade time (HH:MM:SS)
- `Direction`: Bullish, Bearish, or Both
- `Open`: Opening price of the 8:30 candle
- `High`: High price of the 8:30 candle
- `Low`: Low price of the 8:30 candle
- `Close`: Closing price of the 8:30 candle
- `Prev_Max_High`: Maximum high of the previous 5 candles
- `Prev_Min_Low`: Minimum low of the previous 5 candles

## Results Summary

Based on the analysis of data from 2018 to 2025:

| Timeframe | Total Trades | Bullish Trades | Bearish Trades | Both Directions |
|-----------|--------------|----------------|----------------|-----------------|
| 1m        | 1,940        | 1,261          | 1,213          | 534             |
| 5m        | 1,972        | 1,323          | 1,297          | 648             |
| 15m       | 2,799        | 1,637          | 1,574          | 412             |
| **Total** | **6,711**    | **4,221**      | **4,084**      | **1,594**       |

## Data Format

The script expects CSV files in the following format:

- **Delimiter**: Semicolon (;)
- **Columns**: Date, Time, Open, High, Low, Close, Volume
- **Date Format**: DD/MM/YYYY
- **Time Format**: HH:MM:SS
- **File Naming**: 
  - `YYYY 1m.csv.zip` (zipped 1-minute files for 2018-2024)
  - `YYYY 1m.csv` (unzipped 1-minute file for 2025)
  - `YYYY 5m.csv` (5-minute files)
  - `YYYY 15m.csv` (15-minute files)

## How It Works

1. **Data Loading**: 
   - Reads CSV files for each year and timeframe
   - Handles both zipped and unzipped files automatically
   - Combines all years into a single dataset per timeframe

2. **8:30 Candle Identification**:
   - Identifies the exact 8:30:00 candle for each trading day
   - For 15m timeframe, also checks 8:15:00 if 8:30:00 is not available

3. **Breakout Detection**:
   - For each 8:30 candle, retrieves the previous 5 candles
   - Calculates the maximum high and minimum low of those 5 candles
   - Determines if the current candle breaks above (bullish) or below (bearish)

4. **Report Generation**:
   - Compiles all identified trades
   - Generates detailed text and CSV reports
   - Provides summary statistics

## Code Structure

The script is organized into a single class `BacktestStrategy` with the following key methods:

- `read_csv_file()`: Reads unzipped CSV files
- `read_zipped_csv()`: Reads CSV files from zip archives
- `get_830_candle()`: Identifies 8:30 candles for each day
- `check_breakout()`: Determines if a candle breaks out from previous 5 candles
- `analyze_timeframe()`: Processes all data for a specific timeframe
- `generate_report()`: Creates text and CSV reports
- `run()`: Main execution method

## Notes

- The script processes approximately 2.7 million 1-minute candles across all years
- Processing time is typically under 2 minutes on modern hardware
- The 8:30 time refers to 08:30:00 in the timezone of the data (not specified in CSV)
- Both bullish and bearish breakouts can occur simultaneously on the same candle

## Troubleshooting

### "No module named 'pandas'"
Install pandas: `pip install pandas`

### "File not found" errors
Ensure you're running the script from the repository root directory where all CSV files are located.

### Memory issues
The script loads all data into memory. For very large datasets, consider processing years individually by modifying the `self.years` range in the code.

## Example Output

```
================================================================================
BACKTESTING STRATEGY: 8:30 CANDLE WICK BREAKOUT
================================================================================
Period: 2018 to 2025
Timeframes: 1m, 5m, 15m
Strategy: Identify 8:30 candles that exceed wicks of previous 5 candles
================================================================================

======================================================================
Analyzing 1m timeframe...
======================================================================
Reading 2018 1m.csv.zip...
Reading 2019 1m.csv.zip...
...
Total candles loaded: 2,771,419
Total 8:30 candles found: 2028

Trades found: 1940
  - Bullish trades: 1261
  - Bearish trades: 1213
  - Both directions: 534
```

## License

This script is provided as-is for backtesting and analysis purposes.

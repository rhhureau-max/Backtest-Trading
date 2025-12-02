# Backtesting Strategy: 8:30 AM Candle Analysis

## Overview

This backtesting strategy analyzes trading opportunities based on the 8:30 AM candle across three timeframes (1-minute, 5-minute, and 15-minute) from 2018 to 2025.

## Strategy Logic

### Entry Conditions

**LONG Trade (Bullish Candle at 8:30 AM):**
- The 8:30 AM candle must be bullish (Close > Open)
- The close price must be ABOVE the highest high of the previous 5 candles
- Formula: `Close > max(High[n-5:n-1])`

**SHORT Trade (Bearish Candle at 8:30 AM):**
- The 8:30 AM candle must be bearish (Close < Open)
- The close price must be BELOW the lowest low of the previous 5 candles
- Formula: `Close < min(Low[n-5:n-1])`

## Files

### Script
- `backtest_strategy.py` - Main backtesting script

### Output Files
- `trades_1m.csv` - All valid trades for 1-minute timeframe
- `trades_5m.csv` - All valid trades for 5-minute timeframe
- `trades_15m.csv` - All valid trades for 15-minute timeframe
- `all_trades.csv` - Combined trades from all timeframes
- `trades_summary.csv` - Summary statistics for each timeframe

## Requirements

```bash
pip install pandas numpy
```

## Usage

```bash
python3 backtest_strategy.py
```

## Results Summary

### Analysis Period: 2018-2025

| Timeframe | Total Trades | Long Trades | Short Trades |
|-----------|--------------|-------------|--------------|
| 1m        | 1,209        | 652         | 557          |
| 5m        | 1,372        | 709         | 663          |
| 15m       | 1,193        | 633         | 560          |
| **Total** | **3,774**    | **1,994**   | **1,780**    |

## Output File Format

Each trade CSV file contains the following columns:

- **Date**: Trade date (YYYY-MM-DD)
- **Time**: Trade time (08:30:00)
- **Timeframe**: 1m, 5m, or 15m
- **Direction**: LONG or SHORT
- **Open**: Opening price of the 8:30 AM candle
- **High**: High price of the 8:30 AM candle
- **Low**: Low price of the 8:30 AM candle
- **Close**: Closing price of the 8:30 AM candle
- **Volume**: Trading volume
- **Reference_Level**: The max high (for LONG) or min low (for SHORT) of the previous 5 candles
- **Condition**: Human-readable description of the condition met

## Sample Trade

```
Date: 2018-01-02
Time: 08:30:00
Timeframe: 15m
Direction: LONG
Close: 7568.17
Reference Level: 7548.84
Condition: Close (7568.17) > Max Previous 5 Highs (7548.84)
```

## Data Sources

The script processes CSV files with the following naming convention:
- 1-minute data: `YYYY 1m.csv.zip` (zipped) or `YYYY 1m.csv` (2025)
- 5-minute data: `YYYY 5m.csv`
- 15-minute data: `YYYY 15m.csv`

CSV format:
- Delimiter: semicolon (;)
- Columns: Date, Time, Open, High, Low, Close, Volume
- Date format: DD/MM/YYYY
- Time format: HH:MM:SS

## Key Features

1. **Automatic Data Loading**: Handles both zipped and unzipped CSV files
2. **Multi-Year Analysis**: Processes data from 2018 to 2025
3. **Multi-Timeframe**: Analyzes 1m, 5m, and 15m data simultaneously
4. **Detailed Output**: Provides comprehensive trade information
5. **Summary Statistics**: Generates summary reports for easy analysis

## Notes

- The script identifies 8:30 AM candles for each trading day
- Only candles that meet the specific entry criteria are recorded
- The analysis requires at least 5 previous candles for reference
- Trades are sorted chronologically in the output files

## Customization

You can modify the following parameters in the script:

```python
# Configuration
YEARS = range(2018, 2026)  # Analysis period
TIMEFRAMES = ['1m', '5m', '15m']  # Timeframes to analyze
TARGET_TIME = time(8, 30)  # Target candle time
```

To change the lookback period (default is 5 candles), modify the `lookback` parameter in the condition check functions.

## Performance

The script processes millions of candles efficiently:
- 1m data: ~2.8 million candles across all years
- 5m data: ~560,000 candles across all years
- 15m data: ~187,000 candles across all years
- Total processing time: ~90 seconds

## License

This script is provided as-is for backtesting and analysis purposes.

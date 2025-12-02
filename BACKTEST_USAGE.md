# Backtesting Strategy - Usage Guide

## Overview
This backtesting strategy analyzes historical trading data from 2018 to 2025 to identify specific trade setups at 08:30:00 (8:30 AM).

## Strategy Rules

### Bullish Trades (Close > Open)
- The closing price of the 08:30:00 candle must be **above** the highest high of the previous 5 candles
- Condition: `Close > max(High of previous 5 candles)`

### Bearish Trades (Close < Open)
- The closing price of the 08:30:00 candle must be **below** the lowest low of the previous 5 candles
- Condition: `Close < min(Low of previous 5 candles)`

## Data Format
- **CSV Format**: Semicolon-separated (;)
- **Columns**: Date (DD/MM/YYYY) | Time (HH:MM:SS) | Open | High | Low | Close | Volume
- **Timeframes**: 1m, 5m, 15m
- **Period**: 2018-2025

## How to Run

### Prerequisites
```bash
pip install pandas
```

### Execution
```bash
python3 backtest_strategy.py
```

The script will:
1. Automatically extract zipped CSV files (1m data for 2018-2024)
2. Process all timeframes (1m, 5m, 15m) for all years
3. Identify trades meeting the strategy conditions
4. Generate comprehensive reports

## Output Files

### 1. backtest_results.csv
Detailed CSV file containing all identified trades with the following columns:
- **Date**: Trade date (DD/MM/YYYY)
- **Time**: Trade time (08:30:00)
- **Timeframe**: 1m, 5m, or 15m
- **Type**: BULLISH or BEARISH
- **Close**: Closing price of the 08:30:00 candle
- **Open**: Opening price of the 08:30:00 candle
- **High**: High price of the 08:30:00 candle
- **Low**: Low price of the 08:30:00 candle
- **Volume**: Trading volume
- **Max_High_Prev5**: Maximum high of the previous 5 candles
- **Min_Low_Prev5**: Minimum low of the previous 5 candles
- **Condition_Met**: Description of the condition that was met

### 2. backtest_summary.txt
Summary report containing:
- Overall statistics (total trades, bullish/bearish breakdown)
- Statistics by timeframe
- Statistics by year
- Average prices and volumes

## Results Summary

### Total Trades Found: 3,774

| Timeframe | Total Trades | Bullish | Bearish |
|-----------|-------------|---------|---------|
| 1m        | 1,209       | 652     | 557     |
| 5m        | 1,372       | 709     | 663     |
| 15m       | 1,193       | 633     | 560     |

### Distribution by Year

| Year | Total Trades | Bullish | Bearish |
|------|-------------|---------|---------|
| 2018 | 475         | 268     | 207     |
| 2019 | 480         | 258     | 222     |
| 2020 | 493         | 256     | 237     |
| 2021 | 509         | 272     | 237     |
| 2022 | 482         | 236     | 246     |
| 2023 | 468         | 289     | 179     |
| 2024 | 445         | 214     | 231     |
| 2025 | 422         | 201     | 221     |

## Script Features

1. **Automatic ZIP Extraction**: Automatically extracts 1m CSV files from ZIP archives
2. **Data Validation**: Handles missing data and validates all price fields
3. **Comprehensive Reporting**: Generates both detailed CSV and summary text reports
4. **Progress Tracking**: Shows real-time progress during processing
5. **Error Handling**: Gracefully handles missing files or corrupted data
6. **Multi-Year Support**: Processes data from 2018 to 2025
7. **Multi-Timeframe Analysis**: Analyzes 1m, 5m, and 15m timeframes

## Code Structure

### Main Components

1. **BacktestStrategy Class**
   - `__init__`: Initialize with base path and configuration
   - `extract_zip_if_needed`: Handle ZIP file extraction
   - `load_data`: Load and parse CSV files
   - `check_830_condition`: Apply strategy conditions
   - `run_backtest`: Execute backtest across all data
   - `save_results`: Save results to CSV
   - `generate_summary_report`: Create summary report

2. **Data Processing**
   - Reads CSV files with semicolon separator
   - Converts price data to numeric format
   - Creates datetime objects for proper sorting
   - Handles missing or invalid data gracefully

3. **Strategy Logic**
   - Filters for 08:30:00 candles
   - Calculates max high and min low of previous 5 candles
   - Determines bullish/bearish classification
   - Validates strategy conditions
   - Records all matching trades

## Notes

- The script automatically skips doji candles (close == open)
- Requires at least 5 previous candles for each 08:30:00 candle
- All times are in the timezone of the original data
- Results are sorted chronologically
- The script is optimized for large datasets

## Troubleshooting

### Issue: Module not found
```bash
pip install pandas
```

### Issue: ZIP files not extracting
- Check that ZIP files exist in the repository
- Verify file permissions
- Ensure sufficient disk space

### Issue: No trades found
- Verify CSV file format matches expected structure
- Check that times include 08:30:00 entries
- Ensure date format is DD/MM/YYYY

## Future Enhancements

Potential improvements:
- Add command-line arguments for custom timeframes
- Include additional technical indicators
- Add visualization/charting capabilities
- Export results to Excel with formatting
- Add backtesting performance metrics (win rate, average gain/loss)

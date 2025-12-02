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
pip install pandas numpy
```

### Basic Execution
```bash
python3 backtest_strategy.py
```

### With Risk/Reward Analysis
```bash
python3 backtest_strategy.py --rr
```
or
```bash
python3 backtest_strategy.py --risk-reward
```

The script will:
1. Automatically extract zipped CSV files (1m data for 2018-2024)
2. Process all timeframes (1m, 5m, 15m) for all years
3. Identify trades meeting the strategy conditions
4. Generate comprehensive reports
5. **(With --rr flag)** Perform detailed Risk/Reward analysis on all identified trades

## Output Files

### Basic Backtest Files

#### 1. backtest_results.csv
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

#### 2. backtest_summary.txt
Summary report containing:
- Overall statistics (total trades, bullish/bearish breakdown)
- Statistics by timeframe
- Statistics by year
- Average prices and volumes

### Risk/Reward Analysis Files (Generated with --rr flag)

#### 3. backtest_rr_analysis_detailed.csv
Comprehensive CSV file containing all trade simulations with the following columns:
- **Date, Time, Timeframe, Type**: Trade identification
- **Entry**: Entry price (close of 08:30 candle)
- **SL_Type**: Stop Loss type (SL100, SL75, SL50, SL25)
- **RR_Ratio**: Risk/Reward ratio tested (1.0 to 5.0)
- **Stop_Loss**: Calculated Stop Loss level
- **Take_Profit**: Calculated Take Profit level
- **Risk**: Risk amount in points
- **Reward**: Reward amount in points
- **Outcome**: WIN, LOSS, or INCONCLUSIVE
- **Candles_To_Hit**: Number of candles until SL or TP hit
- **Exit_Price**: Actual exit price
- **PnL**: Profit or Loss for the trade

#### 4. backtest_rr_summary.csv
Aggregated statistics for each configuration containing:
- **Timeframe, SL_Type, RR_Ratio**: Configuration parameters
- **Total_Trades**: Number of trades tested
- **Wins, Losses, Inconclusive**: Outcome counts
- **Win_Rate_%**: Percentage of winning trades
- **Total_PnL**: Total profit/loss for this configuration
- **Avg_Win**: Average profit per winning trade
- **Avg_Loss**: Average loss per losing trade
- **Avg_Candles_To_Win/Loss**: Average time to hit target
- **Win_Loss_Ratio**: Ratio of average win to average loss

#### 5. backtest_rr_analysis.md
Comprehensive markdown report containing:
- **Methodology**: Detailed explanation of the analysis approach
- **Executive Summary**: Top performing configurations
- **Detailed Results by Timeframe**: Tables for each timeframe and SL type
- **Stop Loss Type Comparison**: Analysis across different SL types
- **Risk/Reward Ratio Comparison**: Performance trends by RR ratio
- **Conclusions and Recommendations**: Trading insights and best configurations

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
8. **Risk/Reward Analysis**: Comprehensive trade simulation with multiple configurations
9. **Data Caching**: Efficient memory management for large datasets
10. **Flexible Stop Loss Strategies**: 4 different SL placement options
11. **Multiple RR Ratios**: Tests 9 different Risk/Reward ratios (1.0 to 5.0)

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
   - **NEW:** `calculate_sl_tp_levels`: Calculate Stop Loss and Take Profit levels
   - **NEW:** `simulate_trade_outcome`: Simulate trade on historical data
   - **NEW:** `analyze_rr_for_trade`: Test all RR scenarios for a single trade
   - **NEW:** `run_rr_analysis`: Execute Risk/Reward analysis on all trades
   - **NEW:** `save_rr_results`: Save RR analysis results
   - **NEW:** `generate_rr_report`: Generate comprehensive markdown report

2. **Data Processing**
   - Reads CSV files with semicolon separator
   - Converts price data to numeric format
   - Creates datetime objects for proper sorting
   - Handles missing or invalid data gracefully
   - **NEW:** Caches loaded data for efficient RR analysis

3. **Strategy Logic**
   - Filters for 08:30:00 candles
   - Calculates max high and min low of previous 5 candles
   - Determines bullish/bearish classification
   - Validates strategy conditions
   - Records all matching trades

4. **Risk/Reward Analysis Logic**
   - **Stop Loss Calculation**: 4 types based on body retracement
     * SL100 (100%): Placed at opening price
     * SL75 (75%): 75% retracement of candle body
     * SL50 (50%): Middle of candle body
     * SL25 (25%): Near closing price
   - **Take Profit Calculation**: Based on risk and RR ratio
   - **Trade Simulation**: Checks subsequent candles to determine outcome
   - **Outcome Classification**: WIN, LOSS, or INCONCLUSIVE
   - **Performance Metrics**: Win rate, P&L, average wins/losses

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

## Risk/Reward Analysis Details

### Stop Loss Types Explained

The Risk/Reward analysis implements 4 different Stop Loss placement strategies based on the 08:30 candle body retracement:

**For Bullish Trades:**
- Body = Close - Open
- SL100: Entry - (Body × 1.00) = Opening price
- SL75: Entry - (Body × 0.75)
- SL50: Entry - (Body × 0.50) = Middle of body
- SL25: Entry - (Body × 0.25)

**For Bearish Trades:**
- Body = Open - Close
- SL100: Entry + (Body × 1.00) = Opening price
- SL75: Entry + (Body × 0.75)
- SL50: Entry + (Body × 0.50) = Middle of body
- SL25: Entry + (Body × 0.25)

### Risk/Reward Ratios

Nine different ratios are tested: 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0

For each ratio:
- **Risk** = |Entry - Stop Loss|
- **Reward** = Risk × RR Ratio
- **Take Profit** = Entry ± Reward (+ for bullish, - for bearish)

### Trade Simulation Process

For each identified trade at 08:30:00:
1. Calculate SL and TP levels for each configuration (36 scenarios)
2. Examine subsequent candles within the same trading day
3. Check if candle Low/High touches SL or TP levels
4. Record outcome as WIN (TP hit first), LOSS (SL hit first), or INCONCLUSIVE (neither hit)
5. Calculate actual P&L based on exit price

### Key Findings (Sample Results)

**Best Win Rate Configuration:**
- Timeframe: 5m
- Stop Loss: SL100 (at opening price)
- Risk/Reward: 1.0
- Win Rate: 50.36%
- Total P&L: +875.54 points

**Best Total P&L Configuration:**
- Timeframe: 15m
- Stop Loss: SL100
- Risk/Reward: 5.0
- Total P&L: +9,995.83 points
- Win Rate: 9.30%

**Key Insights:**
- Lower RR ratios (1.0-2.0) tend to have higher win rates but lower total P&L
- Higher RR ratios (3.0-5.0) have lower win rates but higher potential profits
- SL100 (wider stop) generally performs better than tighter stops
- 5m timeframe shows most consistent results across different configurations

## Future Enhancements

Potential improvements:
- Add command-line arguments for custom timeframes and date ranges
- Include additional technical indicators
- Add visualization/charting capabilities
- Export results to Excel with formatting and charts
- ~~Add backtesting performance metrics (win rate, average gain/loss)~~ ✅ **COMPLETED**
- Monte Carlo simulation for confidence intervals
- Position sizing recommendations based on account risk
- Maximum drawdown analysis
- Consecutive wins/losses tracking

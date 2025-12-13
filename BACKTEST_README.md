# Backtesting Strategy: 8:30 AM Candle Analysis with Risk Management

## Overview

This backtesting strategy analyzes trading opportunities based on the 8:30 AM candle across three timeframes (1-minute, 5-minute, and 15-minute) from 2018 to 2025. 

**Version 2.0** includes comprehensive risk management and profit analysis with multiple Stop Loss levels and Risk-Reward ratios.

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

### Scripts
- `backtest_strategy.py` - Main backtesting script with risk management
- `RISK_ANALYSIS_REPORT.md` - Comprehensive documentation of risk analysis features

### Output Files

#### Enhanced Trade Files
- `trades_enhanced_1m.csv` - Enhanced 1m trades with all SL/TP levels and outcomes
- `trades_enhanced_5m.csv` - Enhanced 5m trades with all SL/TP levels and outcomes
- `trades_enhanced_15m.csv` - Enhanced 15m trades with all SL/TP levels and outcomes

#### Performance Summary Files
- `performance_summary_1m.csv` - Performance metrics for 1m timeframe by SL/RR combination
- `performance_summary_5m.csv` - Performance metrics for 5m timeframe by SL/RR combination
- `performance_summary_15m.csv` - Performance metrics for 15m timeframe by SL/RR combination
- `performance_summary_all.csv` - Combined performance summary across all timeframes

#### Best Configuration Files
- `best_configurations_by_pnl.csv` - Top 10 configurations by total profit/loss
- `best_configurations_by_winrate.csv` - Top 10 configurations by win rate
- `best_configurations_by_profit_factor.csv` - Top 10 configurations by profit factor

#### Basic Summary
- `trades_summary.csv` - Basic trade counts for each timeframe

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

### Top Performing Configurations

Based on the comprehensive risk analysis:

**Best by Total P&L:**
- **15m SL_50 RR_4.5**: +5,102.46 points (21.43% win rate, 1,176 trades)
- **15m SL_50 RR_4.0**: +4,876.07 points (23.05% win rate, 1,180 trades)
- **5m SL_50 RR_4.5**: +4,783.57 points (22.11% win rate, 1,366 trades)

**Best by Win Rate:**
- **5m SL_100 RR_1.0**: 50.40% win rate (+890.89 points, 1,371 trades)
- **15m SL_100 RR_1.0**: 49.58% win rate (+358.20 points, 1,188 trades)
- **5m SL_75 RR_1.0**: 47.30% win rate (-333.65 points, 1,372 trades)

**Best by Profit Factor:**
- **5m SL_50 RR_4.5**: 1.28 profit factor (+4,783.57 points)
- **5m SL_50 RR_4.0**: 1.27 profit factor (+4,481.60 points)
- **5m SL_50 RR_3.0**: 1.24 profit factor (+3,755.39 points)

## Output File Format

### Enhanced Trade Files

Each enhanced trade CSV file contains 160 columns:

**Basic Trade Information:**
- **Date**: Trade date (YYYY-MM-DD)
- **Time**: Trade time (08:30:00)
- **Timeframe**: 1m, 5m, or 15m
- **Direction**: LONG or SHORT
- **Open**: Opening price of the 8:30 AM candle
- **High**: High price of the 8:30 AM candle
- **Low**: Low price of the 8:30 AM candle
- **Close**: Closing price of the 8:30 AM candle (entry price)
- **Volume**: Trading volume
- **Reference_Level**: The max high (for LONG) or min low (for SHORT) of the previous 5 candles
- **Condition**: Human-readable description of the condition met

**Stop Loss Levels:**
- **SL_100**: Stop at 100% body retracement (at Open)
- **SL_75**: Stop at 75% body retracement
- **SL_50**: Stop at 50% body retracement
- **SL_25**: Stop at 25% body retracement
- **Body_Size**: Size of the candle body in points

**Take Profit Levels:**
- 36 columns with naming pattern: `SL_[level]_TP_[RR]`
- Example: `SL_100_TP_1.0`, `SL_75_TP_2.5`, etc.

**Trade Outcomes:**
For each of 36 SL/RR combinations:
- **[SL]_RR_[RR]_Outcome**: WIN, LOSS, or NO_TOUCH
- **[SL]_RR_[RR]_PnL**: Profit/Loss in price points
- **[SL]_RR_[RR]_Candles**: Number of candles to hit SL or TP

### Performance Summary Files

Each performance summary contains:
- **Timeframe**: 1m, 5m, or 15m
- **SL_Level**: SL_100, SL_75, SL_50, or SL_25
- **RR_Ratio**: 1.0 to 5.0
- **Total_Trades**: Count of valid trades (excludes NO_TOUCH)
- **Wins**: Number of winning trades
- **Losses**: Number of losing trades
- **No_Touch**: Trades that didn't hit SL or TP
- **Win_Rate_%**: Percentage of winning trades
- **Total_PnL**: Cumulative profit/loss in points
- **Avg_Win**: Average winning trade
- **Avg_Loss**: Average losing trade
- **Profit_Factor**: Gross profit / Gross loss ratio

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
4. **Multiple Stop Loss Levels**: Tests 4 different SL placements (100%, 75%, 50%, 25% body retracement)
5. **Risk-Reward Analysis**: Evaluates 9 different RR ratios (1.0 to 5.0)
6. **Comprehensive Testing**: 36 unique configurations per trade (4 SL × 9 RR)
7. **Real Price Action**: Analyzes actual subsequent candles to determine outcomes
8. **Detailed Metrics**: Win rate, P&L, profit factor for each configuration
9. **Best Configuration Reports**: Automatically identifies top-performing setups
10. **Summary Statistics**: Generates comprehensive summary reports for easy analysis

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

# Risk Management Configuration
SL_LEVELS = [100, 75, 50, 25]  # Stop Loss percentages of candle body
RR_RATIOS = [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]  # Risk-Reward ratios
```

To change the lookback period (default is 5 candles), modify the `lookback` parameter in the condition check functions.

To change the maximum number of candles analyzed after entry (default is 100), modify `max_lookback` in the `analyze_trade_outcome` function.

## Performance

The enhanced script processes millions of candles with comprehensive risk analysis:
- 1m data: ~2.8 million candles across all years
- 5m data: ~560,000 candles across all years
- 15m data: ~187,000 candles across all years
- Total trades analyzed: 3,774 trades
- Configurations per trade: 36 (4 SL levels × 9 RR ratios)
- Total trade outcomes analyzed: ~135,864 (3,774 × 36)
- Total processing time: ~3-5 minutes

## License

This script is provided as-is for backtesting and analysis purposes.

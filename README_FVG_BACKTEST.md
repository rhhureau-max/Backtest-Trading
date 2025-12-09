# NY Opening FVG Backtest Strategy

## Overview

This is a complete Python backtest system for a Fair Value Gap (FVG) trading strategy focused on the New York market opening session (08:30-09:00 ET).

## File

- **ny_opening_fvg_backtest.py** - Main backtest script

## Strategy Description

### FVG Detection
- **Window**: 08:30-09:00 NY time
- **Selection**: First valid FVG only (if no FVG by 09:00, skip the day)
- **Bullish FVG**: High of candle (n-1) < Low of candle (n+1)
- **Bearish FVG**: Low of candle (n-1) > High of candle (n+1)

### Entry Rules
- **SHORT Entry** (Bullish FVG breakout): Wait for a candle to close BELOW the lower bound of FVG
- **LONG Entry** (Bearish FVG breakout): Wait for a candle to close ABOVE the upper bound of FVG
- Entry occurs at the close price of the trigger candle

### Risk Management
- **Stop Loss for SHORT**: High of Trigger Candle + 0.5 points
- **Stop Loss for LONG**: Low of Trigger Candle - 0.5 points
- **Risk**: Distance between Entry and Stop Loss

### Take Profit Levels
- **TP1**: 1.0 × Risk (closes 33% of position)
- **TP2**: 1.5 × Risk (closes 33% of position)
- **TP3**: 2.0 × Risk (closes 34% of position)

## Data Requirements

### Expected Data Format
- Files: `2018 1m.csv`, `2019 1m.csv`, ..., `2025 1m.csv`
- Format: Semicolon-separated CSV
- Columns: `Date;Time;Open;High;Low;Close;Volume`
- Date format: `DD/MM/YYYY`
- Time format: `HH:MM:SS`

### Example Data Line
```
01/01/2025;17:00:00;21927.625319;21941.801108;21911.645339;21919.635329;444
```

## Installation

### Required Libraries
```bash
pip install pandas numpy pytz
```

## Usage

### Basic Usage
```bash
python3 ny_opening_fvg_backtest.py
```

### Script automatically:
1. Loads all 1-minute CSV files from 2018-2025
2. Converts timestamps to New York timezone (handles DST)
3. Detects FVG patterns during NY opening session
4. Simulates trades with proper risk management
5. Calculates comprehensive statistics
6. Saves results to CSV

## Output

### Console Output
The script displays:
- Overall statistics (win rate, total trades)
- Take profit analysis (TP1, TP2, TP3 hit rates)
- Profit & Loss metrics
- Risk metrics (max drawdown, average risk)
- Trade type breakdown (Long vs Short performance)
- Sample trades (first 10 and last 10)

### CSV Output
File: `ny_opening_fvg_results.csv`

Contains detailed information for each trade:
- Date
- Trade type (LONG/SHORT)
- Entry price and stop loss
- Risk amount
- TP1, TP2, TP3 prices
- Which TPs were hit
- Individual TP PnL
- Total PnL in points

## Key Features

1. **Timezone Handling**: Proper conversion to NY timezone with DST support
2. **Bar-by-bar Simulation**: Realistic trade execution
3. **Partial Position Management**: Different TP levels with varying position sizes
4. **Comprehensive Statistics**: Win rates, profit factor, drawdown analysis
5. **Trade Type Analysis**: Separate statistics for Long and Short trades
6. **Production Ready**: Error handling, progress tracking, clear code structure

## Performance Metrics

The backtest calculates:
- **Overall Win Rate**: Percentage of profitable trades
- **TP Win Rates**: Individual hit rates for each TP level
- **Profit Factor**: Gross profit / Gross loss
- **Maximum Drawdown**: Largest peak-to-trough decline
- **Average Risk**: Mean risk per trade
- **Win Rate by Direction**: Separate for Long and Short trades

## Code Structure

### Main Classes
- **NYOpeningFVGBacktest**: Main backtest engine

### Key Methods
- `load_data()`: Load and parse CSV files
- `detect_fvg()`: Identify FVG patterns
- `find_daily_fvg()`: Search for FVG in 08:30-09:00 window
- `find_entry_signal()`: Detect breakout entry
- `simulate_trade()`: Execute trade with TP/SL management
- `run_backtest()`: Run complete backtest
- `calculate_statistics()`: Compute performance metrics
- `display_results()`: Show and save results

## Customization

To modify the strategy, adjust these parameters in the code:

```python
# FVG detection window (lines ~152-155)
search_window = day_data[
    (day_data['DateTime'].dt.time >= time(8, 30)) &
    (day_data['DateTime'].dt.time < time(9, 0))
]

# Stop loss buffer (lines ~201, 211)
'stop_loss': candle['High'] + 0.5  # SHORT
'stop_loss': candle['Low'] - 0.5   # LONG

# Take profit ratios (lines ~236-239, 245-248)
tp1_price = entry_price + (1.0 * risk)  # LONG
tp2_price = entry_price + (1.5 * risk)
tp3_price = entry_price + (2.0 * risk)

# Position sizes (lines ~257-261)
positions = {
    'tp1': 0.33,  # 33% at TP1
    'tp2': 0.33,  # 33% at TP2
    'tp3': 0.34   # 34% at TP3
}
```

## Notes

- The strategy trades only one setup per day (first FVG found)
- Days without FVG or entry signals are skipped
- All calculations are in index points (not dollars)
- Trade simulation is realistic with bar-by-bar execution
- Stop loss takes priority over take profits in the same bar

## Support

For questions or issues, review the code comments and docstrings which provide detailed explanations of each component.

---

**Author**: Quantitative Trading System  
**Version**: 1.0  
**Date**: December 2025

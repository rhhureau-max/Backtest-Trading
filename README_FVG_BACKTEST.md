# NQ Futures FVG Backtest Strategy

## Overview

This is a complete production-ready backtest system for NQ (Nasdaq) futures using Fair Value Gap (FVG) detection strategy. The backtest analyzes 1-minute timeframe data from 2018 to 2025.

## Strategy Details

### Trading Rules

**Killzone Time Window:**
- Trading hours: 08:30 to 11:00 (Chicago Exchange Time)
- Maximum 1 trade per day (first valid FVG only)

**FVG Detection Logic:**

The strategy uses a 3-candle pattern (i-2, i-1, i) where i is the candle that just closed:

1. **Bearish FVG (Short Setup)**:
   - Condition: `Low[i-2] > High[i]`
   - Gap exists between the bottom of candle i-2 and the top of candle i
   - Entry: High of candle i (Limit Order)
   - Stop Loss: High of candle i-2 + 0.5 points
   - Take Profit: Entry - (Stop Loss - Entry) × 1.5

2. **Bullish FVG (Long Setup)**:
   - Condition: `High[i-2] < Low[i]`
   - Gap exists between the top of candle i-2 and the bottom of candle i
   - Entry: Low of candle i (Limit Order)
   - Stop Loss: Low of candle i-2 - 0.5 points
   - Take Profit: Entry + (Entry - Stop Loss) × 1.5

**Execution Rules:**
- Limit orders placed when FVG is detected
- Order triggers only if subsequent candles (i+1, i+2, etc.) touch entry price
- Orders not triggered by 11:00 are cancelled
- Active trades after 11:00 continue until TP/SL is hit

## Data Format

**CSV Files:**
- Delimiter: Semicolon (;)
- Columns:
  1. Column1: Date (DD/MM/YYYY)
  2. Column2: Time (HH:MM:SS)
  3. Column3: Open
  4. Column4: High
  5. Column5: Low
  6. Column6: Close
  7. Column7: Volume

**Required Files:**
- 2018 1m.csv.zip through 2024 1m.csv.zip (compressed)
- 2025 1m.csv (uncompressed)

All files should be in the same directory as the script.

## Installation

### Prerequisites

```bash
# Python 3.x required
# Install required packages
pip3 install pandas numpy
```

### Files Included

1. `nq_fvg_backtest.py` - Main backtest script
2. `README_FVG_BACKTEST.md` - This documentation file
3. CSV data files (2018-2025)

## Usage

### Basic Execution

```bash
python3 nq_fvg_backtest.py
```

### What Happens During Execution

1. **Unzipping**: Automatically unzips compressed CSV files
2. **Data Loading**: Loads and combines all 1-minute data from 2018-2025
3. **FVG Detection**: Scans for Fair Value Gaps during killzone hours
4. **Trade Simulation**: Simulates order placement and execution
5. **Results**: Generates comprehensive metrics and saves to CSV

### Output Files

**nq_fvg_backtest_results.csv** - Contains all trades with columns:
- Date: Trade date
- Entry_Time: When order was triggered
- Exit_Time: When trade was closed
- Type: Long or Short
- Entry_Price: Actual entry price
- Exit_Price: Actual exit price
- Stop_Loss: Stop loss level
- Take_Profit: Take profit level
- PnL: Profit/Loss in points
- Exit_Reason: TP (Take Profit), SL (Stop Loss), or EOD (End of Day)
- Duration_Minutes: Trade duration in minutes

## Performance Metrics

The backtest calculates and displays:

1. **Trade Statistics**:
   - Total Trades
   - Winning Trades
   - Losing Trades
   - Win Rate (%)

2. **Profit & Loss**:
   - Total Net P&L (points)
   - Gross Profit (points)
   - Gross Loss (points)
   - Average Win (points)
   - Average Loss (points)
   - Profit Factor (Gross Profit / Gross Loss)

3. **Risk Metrics**:
   - Maximum Drawdown (points)
   - Maximum Drawdown (%)
   - Average Trade Duration (minutes)

## Sample Output

```
======================================================================
NQ FUTURES FVG BACKTEST STRATEGY
======================================================================

Strategy Parameters:
  - Killzone: 08:30 to 11:00 (Chicago Time)
  - FVG Detection: 3-candle pattern (i-2, i-1, i)
  - Stop Loss Offset: 0.5 points
  - Take Profit: 1.5x Risk
  - Max Trades per Day: 1
======================================================================

Trading Period: 2018-01-01 to 2025-11-13
Killzone: 08:30 to 11:00

-------------------------PERFORMANCE METRICS--------------------------

Total Trades:          1793
Winning Trades:        789
Losing Trades:         1004
Win Rate:              44.00%

Total Net P&L:         1833.49 points
Gross Profit:          25291.24 points
Gross Loss:            23457.75 points
Average Win:           32.05 points
Average Loss:          -23.36 points
Profit Factor:         1.08

Max Drawdown:          2034.66 points
Max Drawdown %:        326.90%

Avg Trade Duration:    10.4 minutes
```

## Code Structure

### Main Components

1. **NQFVGBacktest Class**:
   - `__init__()`: Initialize backtest parameters
   - `unzip_data_files()`: Extract compressed CSV files
   - `load_data()`: Load and combine all data
   - `detect_fvg()`: FVG detection logic
   - `check_order_trigger()`: Check if limit order gets filled
   - `simulate_trade()`: Simulate trade from entry to exit
   - `run_backtest()`: Main backtest loop
   - `calculate_metrics()`: Calculate performance metrics
   - `print_summary()`: Display results
   - `save_results()`: Save trades to CSV

2. **Key Parameters**:
   ```python
   killzone_start = time(8, 30)  # 08:30
   killzone_end = time(11, 0)    # 11:00
   sl_offset = 0.5               # Stop loss offset in points
   tp_multiplier = 1.5           # Take profit risk multiplier
   ```

## Customization

### Modifying Strategy Parameters

Edit these variables in the `__init__()` method:

```python
self.killzone_start = time(8, 30)  # Change start time
self.killzone_end = time(11, 0)    # Change end time
self.sl_offset = 0.5               # Change SL offset
self.tp_multiplier = 1.5           # Change TP multiplier
```

### Changing Data Directory

Modify the data directory path in `main()`:

```python
data_directory = '/your/custom/path/'
```

## Error Handling

The script includes comprehensive error handling for:
- Missing data files
- Corrupted zip files
- Invalid CSV format
- Data parsing errors

Warnings and errors are printed to console with descriptive messages.

## Limitations & Considerations

1. **Slippage**: Not included in calculations (assumes perfect execution at limit prices)
2. **Commission**: Not included in P&L calculations
3. **Market Hours**: Assumes all data is in Chicago Exchange Time
4. **Overnight Gaps**: Trades are closed by end of day
5. **Volume**: Not considered in execution logic
6. **Bid-Ask Spread**: Not simulated

## Performance Notes

- Processing ~2.7 million candles takes approximately 2-3 minutes
- Memory usage is efficient due to chunked processing
- Results are cached to avoid reprocessing

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError: No module named 'pandas'**
   ```bash
   pip3 install pandas numpy
   ```

2. **FileNotFoundError: CSV files not found**
   - Ensure all CSV files are in the same directory as the script
   - Check file names match exactly (case-sensitive)

3. **MemoryError with large datasets**
   - Process fewer years at a time
   - Increase system RAM

4. **No trades executed**
   - Check killzone times match data timezone
   - Verify FVG detection parameters
   - Review data format

## Future Enhancements

Potential improvements:
- Add commission and slippage modeling
- Implement position sizing
- Add multiple contracts support
- Include volume filters
- Add data visualization (equity curve, drawdown chart)
- Export to multiple formats (Excel, JSON)
- Real-time strategy monitoring
- Parameter optimization

## License

This code is provided as-is for educational and research purposes.

## Contact & Support

For questions, improvements, or bug reports, please refer to the repository documentation.

---

**Version**: 1.0  
**Last Updated**: 2026-01-08  
**Python Version**: 3.x  
**Dependencies**: pandas, numpy

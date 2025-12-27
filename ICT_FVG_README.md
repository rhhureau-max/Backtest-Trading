# ICT Fair Value Gap (FVG) Backtest Strategy

## Overview

This Python script implements a complete backtesting system for an ICT (Inner Circle Trader) based trading strategy on NASDAQ 100 (NQ) 1-minute data from 2018 to 2025.

## Strategy Description

### Core Concept
The strategy identifies Fair Value Gaps (FVGs) and waits for price to return and test these gaps with specific reversal patterns during the New York trading session.

### Strategy Components

#### 1. **Fair Value Gap (FVG) Identification**
- **Bearish FVG**: The Low of candle [i-2] is greater than the High of candle [i]
- **Bullish FVG**: The High of candle [i-2] is less than the Low of candle [i]
- The gap must be created by a "Displacement" candle (candle [i-1]) with:
  - Large body (at least 60% of candle range)
  - Range larger than 1.5x the 20-period average range

#### 2. **Time Filter (Killzone)**
- Trading only during New York session: **08:30 - 11:00** (local exchange time)
- FVGs are only identified and traded during this window

#### 3. **Entry Signal (Mitigation & Reversal Pattern)**
- Price must return to test (mitigate) the FVG
- Critical reversal patterns required:
  - **For SHORT trades (Bearish FVG)**: Shooting Star pattern
    - Upper wick at least 2x larger than the body
    - Small body located in the lower third of candle
    - Upper wick must penetrate the FVG zone
  - **For LONG trades (Bullish FVG)**: Hammer pattern
    - Lower wick at least 2x larger than the body
    - Small body located in the upper third of candle
    - Lower wick must penetrate the FVG zone

#### 4. **Trade Execution**
- **Entry**: At the close of the signal candle (Hammer or Shooting Star)
- **Stop Loss**:
  - SHORT: High of Shooting Star + 0.5 points
  - LONG: Low of Hammer - 0.5 points

#### 5. **Take Profit Targets**
Three Risk:Reward ratios are tested:
- **1R**: 1:1 Risk:Reward
- **1.5R**: 1.5:1 Risk:Reward
- **2R**: 2:1 Risk:Reward

## Requirements

### Python Dependencies
```bash
pip install pandas numpy
```

### Data Files
The script expects 1-minute NASDAQ 100 data files in the following formats:
- **Zipped CSV**: `YYYY 1m.csv.zip` (2018-2024)
- **Plain CSV**: `YYYY 1m.csv` (2025)

CSV format (semicolon-separated):
```
Column1;Column2;Column3;Column4;Column5;Column6;Column7
Date;Time;Open;High;Low;Close;Volume
DD/MM/YYYY;HH:MM:SS;price;price;price;price;volume
```

## Usage

### Basic Execution
```bash
python ict_fvg_backtest.py
```

### Customization
You can modify the following parameters in the script:

```python
# In ICTFVGBacktest class __init__ method:
self.killzone_start = time(8, 30)   # Start of trading window
self.killzone_end = time(11, 0)     # End of trading window
self.stop_buffer = 0.5              # Stop loss buffer in points
self.rr_targets = [1.0, 1.5, 2.0]   # Risk:Reward ratios to test

# In main() function:
start_year = 2018  # First year to backtest
end_year = 2025    # Last year to backtest
```

## Output

### Console Output
The script displays:
1. Data loading progress
2. Backtest execution progress (every 50,000 candles)
3. Comprehensive statistics for each R:R target:
   - Total trades
   - Winning/Losing trades
   - Win rate (%)
   - Profit factor
   - Total profit/loss
   - Net P&L
   - Maximum drawdown
   - Average bars in trade

### Example Output
```
================================================================================
TAKE PROFIT: 1.5R (Risk:Reward)
================================================================================
Total Trades:        4083
Winning Trades:      1683
Losing Trades:       2400
Win Rate:            41.22%
Profit Factor:       1.052
Total Profit:        $23799.67
Total Loss:          $22629.59
Net P&L:             $1170.08
Max Drawdown:        $1157.45
Avg Bars in Trade:   2.9
```

### Trade Log CSV
A detailed CSV file (`trade_log.csv`) is generated with all executed trades containing:
- Entry/Exit timestamps
- Entry/Exit prices
- Direction (long/short)
- Result (win/loss)
- P&L
- Risk amount
- Stop loss levels
- FVG type
- R:R ratio
- Bars in trade

## Performance Metrics Explained

- **Win Rate**: Percentage of winning trades
- **Profit Factor**: Ratio of total profits to total losses (>1 means profitable)
- **Net P&L**: Total profit minus total loss
- **Max Drawdown**: Largest peak-to-trough decline in cumulative P&L
- **Avg Bars in Trade**: Average number of 1-minute candles per trade

## Code Structure

### Main Classes

#### `ICTFVGBacktest`
Main backtesting engine with methods:
- `load_data()`: Load single year data from CSV/ZIP
- `load_all_data()`: Load multiple years
- `identify_fvg()`: Detect Fair Value Gaps with displacement
- `is_shooting_star()`: Identify Shooting Star reversal pattern
- `is_hammer()`: Identify Hammer reversal pattern
- `check_fvg_mitigation()`: Verify FVG is being tested
- `simulate_trade()`: Execute trade simulation with stop/target
- `run_backtest()`: Main backtest loop
- `print_results()`: Format and display results
- `export_trades_to_csv()`: Export trade log

## Strategy Logic Flow

1. Load and prepare 1-minute data
2. Calculate 20-period average range for displacement detection
3. For each candle:
   - Check if in killzone (08:30-11:00)
   - Identify new FVGs with displacement confirmation
   - Check if active FVGs are being mitigated
   - Look for reversal patterns (Hammer/Shooting Star)
   - Execute trade if pattern confirms
   - Simulate trade outcome for each R:R target
4. Calculate and display comprehensive statistics

## Edge Case Handling

- **Data validation**: Removes rows with NaN values
- **FVG expiration**: FVGs expire after 50 candles if not mitigated
- **Overlapping trades**: Only one trade active at a time
- **End of data**: Trades reaching end of data are marked as "no_exit"
- **Zero division protection**: Handles cases where denominators could be zero

## Best Practices

1. **Data Quality**: Ensure CSV files are properly formatted and contain valid data
2. **Memory**: Processing 2.7M+ candles requires adequate RAM
3. **Runtime**: Full backtest takes 2-3 minutes on modern hardware
4. **Analysis**: Review the trade log CSV for detailed trade-by-trade analysis
5. **Optimization**: Adjust parameters based on your risk tolerance and market conditions

## Limitations

- Assumes instant execution at close prices (no slippage)
- Does not account for transaction costs/commissions
- Uses simplified patterns (real patterns may have additional nuances)
- Fixed position sizing (does not vary with account size)

## Future Enhancements

Potential improvements:
- Add slippage and commission modeling
- Implement dynamic position sizing
- Add more FVG variations (imbalances, liquidity voids)
- Include additional ICT concepts (order blocks, breaker blocks)
- Add visualization of equity curve and drawdown
- Implement walk-forward analysis
- Add statistical significance tests

## License

This script is provided for educational and research purposes.

## Author

Expert Quant Developer - ICT Strategy Specialist

## Version

1.0.0 - December 2025

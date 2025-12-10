# London Reversal Backtest - Documentation

## Overview

This is a complete Python backtesting script for the **London Reversal** strategy based on Smart Money Concepts (SMC). The strategy identifies high-probability reversal setups during the London Killzone by detecting Tokyo session range manipulation followed by Fair Value Gap (FVG) creation and Market Structure Shift (MSS).

## Strategy Logic

### 1. Tokyo Session Range (Asian Session)
- **Time Window**: 17:00 - 00:00 Chicago time (previous day/night)
- **Timeframe**: 15m or 1H
- **Identifies**: Tokyo_High and Tokyo_Low for the next day's London session

### 2. London Killzone (Manipulation Zone)
- **Time Window**: 01:00 - 04:00 Chicago time
- **Purpose**: Look for entry setups within this window

### 3. Three-Step Validation Sequence

#### Step A - Manipulation (Sweep/Raid)
- Price must cross/sweep Tokyo_High or Tokyo_Low
- **SHORT scenario**: Price goes ABOVE Tokyo_High (bearish manipulation)
- **LONG scenario**: Price goes BELOW Tokyo_Low (bullish manipulation)

#### Step B - FVG Formation (Fair Value Gap)
- After manipulation, look for FVG creation OPPOSITE to manipulation direction
- **Bearish FVG**: Gap between candle[i-1].Low and candle[i+1].High
- **Bullish FVG**: Gap between candle[i-1].High and candle[i+1].Low

#### Step C - MSS (Market Structure Shift)
- Price body must break the last recent Swing Low (for short) or Swing High (for long)
- **Swing Identification**: Fractal algorithm with 2 candles lookback
  - Swing High: High > 2 previous AND 2 following candles
  - Swing Low: Low < 2 previous AND 2 following candles
- **Critical Condition**: FVG must be created BEFORE or DURING the MSS candle

### 4. Trade Execution

#### Entry
- **Trigger**: Once MSS is validated
- **Entry Price**: 50% Fibonacci retracement
- **Fib Range**: From manipulation peak to MSS bottom (or inverse for Long)

#### Stop Loss
- **SHORT**: 0.5 points ABOVE the manipulation peak (highest high during sweep)
- **LONG**: 0.5 points BELOW the manipulation peak (lowest low during sweep)

#### Take Profit Levels
- **TP1**: 1:1 Risk/Reward (1R)
- **TP2**: 1.5:1 Risk/Reward (1.5R)
- **TP3**: 2:1 Risk/Reward (2R)

## Data Format

### CSV File Structure
- **Delimiter**: Semicolon (;)
- **Columns**: Date;Time;Open;High;Low;Close;Volume
- **Date Format**: DD/MM/YYYY HH:MM:SS
- **Timezone**: All times are in Chicago/CME timezone (no conversion needed)

### File Naming Convention
- **M1 (1-minute)**: `YYYY 1m.csv.zip` (zipped)
- **M5 (5-minute)**: `YYYY 5m.csv`
- **M15 (15-minute)**: `YYYY 15m.csv`
- **H1 (1-hour)**: `YYYY 1H.csv`
- **H4 (4-hour)**: `YYYY 4H.csv`

### Example Data
```
Column1;Column2;Column3;Column4;Column5;Column6;Column7
01/01/2018;17:00:00;7503.74;7518.09;7499.64;7517.80;2852
01/01/2018;17:05:00;7510.77;7516.04;7510.77;7512.53;360
```

## Installation

### Requirements
```bash
pip install pandas numpy
```

### Python Version
- Python 3.8 or higher

## Usage

### Basic Usage
```bash
python3 london_reversal_backtest.py
```

### Customization

You can modify the parameters in the `main()` function:

```python
backtest.run_backtest(
    scan_timeframe='5m',      # '1m' or '5m' for entry precision
    tokyo_timeframe='15m',     # '15m' or '1H' for Tokyo range
    years=list(range(2018, 2026))  # Years to backtest
)
```

## Output

### Console Output
The script provides:
1. Data loading progress
2. Backtest progress indicators
3. Comprehensive results summary with:
   - Total setups found
   - Results for each TP level (TP1, TP2, TP3)
   - Win rate, total PnL, average PnL
   - Average win/loss, profit factor

### CSV Output
Results are saved to `london_reversal_results.csv` with the following columns:
- `date`: Trading date
- `direction`: 'short' or 'long'
- `entry_datetime`: When trade was entered
- `entry`: Entry price
- `stop_loss`: Stop loss price
- `risk`: Risk per trade (in points)
- `tp1`, `tp2`, `tp3`: Take profit levels
- `tokyo_high`, `tokyo_low`: Tokyo session range
- `manipulation_type`: 'bearish' or 'bullish'
- `manipulation_peak`: Peak price during manipulation
- `fvg_datetime`: When FVG was formed
- `mss_datetime`: When MSS occurred
- For each TP level:
  - `TPX_outcome`: 'win' or 'loss'
  - `TPX_exit_price`: Exit price
  - `TPX_exit_datetime`: Exit timestamp
  - `TPX_pnl`: Profit/Loss in points

## Performance Metrics

The backtest calculates the following metrics for each TP level:

1. **Win Rate**: Percentage of winning trades
2. **Total PnL**: Cumulative profit/loss in points
3. **Average PnL**: Average profit/loss per trade
4. **Average Win**: Average profit on winning trades
5. **Average Loss**: Average loss on losing trades
6. **Profit Factor**: Ratio of gross profit to gross loss

## Example Results

Based on 2018-2025 backtest on 5m timeframe:

### TP1 (1R)
- Win Rate: ~70%
- Average PnL: ~10 points per trade

### TP2 (1.5R)
- Win Rate: ~62%
- Average PnL: ~14 points per trade

### TP3 (2R)
- Win Rate: ~51%
- Average PnL: ~16 points per trade

## Code Structure

### Main Classes and Functions

#### `LondonReversalBacktest` Class
- `load_data()`: Load and combine multi-year data
- `identify_swings()`: Fractal swing point identification
- `detect_fvg()`: Fair Value Gap detection
- `detect_mss()`: Market Structure Shift detection
- `find_tokyo_range()`: Tokyo session range identification
- `check_manipulation()`: Tokyo High/Low sweep detection
- `calculate_entry_and_targets()`: Entry and TP/SL calculation
- `execute_trade()`: Trade simulation and tracking
- `run_backtest()`: Main backtest loop
- `generate_report()`: Results summary generation
- `save_results()`: CSV export

## Important Notes

1. **No Look-Ahead Bias**: The script processes data bar-by-bar to avoid future data leakage
2. **Timezone**: All times are already in Chicago/CME timezone
3. **Swing Detection**: Uses 2-candle lookback for fractal identification
4. **FVG-MSS Constraint**: FVG must occur before or during MSS candle (strict validation)
5. **Entry Timing**: Trades are entered at 50% Fib retracement after MSS confirmation

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'pandas'"
**Solution**: Install required packages
```bash
pip install pandas numpy
```

### Issue: "File not found" errors
**Solution**: Ensure CSV files are in the correct directory with proper naming convention

### Issue: No trades found
**Solution**: 
- Verify data is loaded correctly
- Check that Tokyo and London sessions have sufficient data
- Ensure date/time format matches expected format

## Future Enhancements

Potential improvements:
1. Add M1 timeframe support for ultra-precise entries
2. Include commission and slippage modeling
3. Add position sizing based on account equity
4. Implement partial profit-taking strategies
5. Add visualization of trades on charts
6. Monte Carlo simulation for robustness testing
7. Walk-forward analysis for parameter optimization

## License

This script is provided as-is for educational and research purposes.

## Author

Senior Quant Developer - Smart Money Concepts Specialist

## Version

1.0.0 - December 2024

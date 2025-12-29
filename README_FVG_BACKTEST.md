# FVG Inverse Trading Strategy Backtest

This script implements a Fair Value Gap (FVG) inverse trading strategy backtesting system for NQ futures data.

## Strategy Overview

### Time Rules
- **Single Session**: Strategy only executes between 01:00 and 05:00 (daily)
- **FVG Creation**: Only FVGs formed within the session window are considered
- **Daily Reset**: All FVGs from the previous day are cleared at 01:00

### Trading Rules

#### Zone Detection (01:00 - 05:00 only)
- **Bearish FVG**: When `candle[i-2].Low > candle[i].High`
  - Zone: `High_Zone = candle[i-2].Low`, `Low_Zone = candle[i].High`
  
- **Bullish FVG**: When `candle[i-2].High < candle[i].Low`
  - Zone: `High_Zone = candle[i].Low`, `Low_Zone = candle[i-2].High`

#### Position Entry (Inverse Strategy)
- **LONG**: When price closes **above** the `High_Zone` of a Bearish FVG
- **SHORT**: When price closes **below** the `Low_Zone` of a Bullish FVG

#### Position Management
- **Single Position**: Only one position at a time
- **Stop Loss**: 
  - LONG: Signal candle low
  - SHORT: Signal candle high
- **Take Profit**: 1:2 risk-reward ratio (2× the risk distance)
- **Session Close**: If position is open at 05:00, close it at market

## Requirements

Install the required Python packages:

```bash
pip install -r requirements.txt
```

## CSV Data Format

The script expects CSV files with semicolon (`;`) separators:
```
Date;Time;Open;High;Low;Close;Volume
01/01/2024;17:00:00;18244.57923;18248.331274;18238.951165;18241.631196;1308
```

## Usage

Simply run the script:

```bash
python3 fvg_inverse_backtest.py
```

The script will:
1. Load all `*5m.csv` files (5-minute data)
2. Load all `*15m.csv` files (15-minute data)
3. Run the backtest on both timeframes
4. Display a comparison table with results
5. Save detailed trade logs to CSV files

## Output

### Console Output
The script displays a comprehensive comparison table:
- Total Trades
- Winning/Losing Trades
- Winrate (%)
- Total P&L (points)
- Gross Profit/Loss
- Profit Factor
- Average Win/Loss

### Generated Files
- `fvg_inverse_trades_5m.csv`: Detailed 5-minute trade log
- `fvg_inverse_trades_15m.csv`: Detailed 15-minute trade log

Each trade log includes:
- Entry/Exit times and prices
- Position type (LONG/SHORT)
- Stop Loss and Take Profit levels
- Exit reason (TP/SL/SESSION_CLOSE)
- P&L in points

## Example Results

```
================================================================================
FVG INVERSE STRATEGY BACKTEST RESULTS
================================================================================

Metric                         5-Minute             15-Minute           
--------------------------------------------------------------------------------
Total Trades                   4398                 2539                
Winning Trades                 788                  1058                
Losing Trades                  3597                 1466                
Winrate (%)                    17.92                41.67               
Total P&L (points)             -41951.69            2333.33             
Gross Profit (points)          16580.77             27400.03            
Gross Loss (points)            58532.47             25066.70            
Profit Factor                  0.28                 1.09                
Average Win (points)           21.04                25.90               
Average Loss (points)          -16.27               -17.10              
================================================================================
```

## Code Structure

The script is organized into several classes:

- **FVGZone**: Represents a Fair Value Gap zone
- **Position**: Represents an open trading position
- **FVGInverseBacktester**: Main backtesting engine
  - `_detect_fvg()`: Detects FVG formations
  - `_check_entry_signal()`: Checks for entry conditions
  - `_check_exit()`: Monitors exit conditions (TP/SL/session close)
  - `run_backtest()`: Main execution loop
  - `_calculate_metrics()`: Computes performance statistics

## Notes

- The script processes data chronologically, candle by candle
- FVG zones are tracked per session and reset daily at 01:00
- Only one position is allowed at a time (no pyramiding)
- All prices are in index points
- The strategy is fully vectorized and efficient for large datasets

## License

This script is provided as-is for backtesting purposes.

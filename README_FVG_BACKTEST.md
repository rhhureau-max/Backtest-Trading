# Fair Value Gap (FVG) Trading Strategy Backtest

## Overview
This script backtests a Fair Value Gap (FVG) trading strategy on NQ (Nasdaq) 1-minute data from 2018-2025.

## Files
- **fvg_backtest.py**: Main backtest script
- **trades_results.csv**: Simple output with Date, Entry Price, Exit Price, PnL, Duration
- **trades_detailed.csv**: Detailed output with all trade information including FVG detection time, entry/exit times, stop loss, take profit, and exit reason

## Strategy Rules

### Trading Window
- **Killzone**: 08:30 to 11:00 Chicago Exchange Time each day
- Only the first valid FVG per day is traded
- Orders not triggered by 11:00 are cancelled
- Trades already running at 11:00 continue until TP or SL

### FVG Detection Logic
Using candles i-2, i-1, and i (where i is the current candle):
- **Bearish FVG**: Low[i-2] > High[i] (gap between bottom of i-2 and top of i)
- **Bullish FVG**: High[i-2] < Low[i] (gap between top of i-2 and bottom of i)

### Order Placement
After FVG detected at candle i close:

**Bearish FVG (Short):**
- Entry Price (Limit): High[i]
- Stop Loss: High[i-2] + 0.5 points
- Take Profit: Entry - (Stop Loss - Entry) × 1.5

**Bullish FVG (Long):**
- Entry Price (Limit): Low[i]
- Stop Loss: Low[i-2] - 0.5 points
- Take Profit: Entry + (Entry - Stop Loss) × 1.5

### Execution Rules
- Trade triggers only if price touches entry level in subsequent candles
- Once triggered, check each candle for Stop Loss or Take Profit hit
- One trade per day maximum
- Risk:Reward ratio is always 1:1.5

## Usage

### Prerequisites
```bash
pip install pandas numpy
```

### Running the Backtest
```bash
python fvg_backtest.py
```

### Expected Output
The script will:
1. Load and combine all 1-minute CSV files from 2018-2025
2. Detect Fair Value Gaps across all data
3. Run the backtest with the specified rules
4. Display comprehensive statistics including:
   - Total trades, winning/losing trades
   - Winrate percentage
   - Profit Factor
   - Maximum Drawdown
   - Total Net Profit
   - Average win/loss
   - Trade distribution by exit reason and type
5. Save results to two CSV files

## Data Format
- **Separator**: Semicolon (;)
- **Columns**: Date, Time, Open, High, Low, Close, Volume
- **Date Format**: DD/MM/YYYY
- **Time Format**: HH:MM:SS
- **Files**: "2025 1m.csv" and zipped files "2018 1m.csv.zip" through "2024 1m.csv.zip"

## Sample Results
Based on the 2018-2025 backtest:
- **Total Trades**: 1,791
- **Winrate**: 39.70%
- **Profit Factor**: 0.97
- **Maximum Drawdown**: -3,302.29 points
- **Total Net Profit**: -683.11 points
- **Average Win**: 33.39 points
- **Average Loss**: -22.61 points
- **Average Duration**: 10.0 minutes

## Output Files

### trades_results.csv
Simple format with essential information:
```
Date,Entry Price,Exit Price,PnL,Duration
2018-01-03,7656.040391,7672.606235,16.565844,7.0
```

### trades_detailed.csv
Comprehensive format with all trade details:
```
Date,FVG_Time,Entry_Time,Exit_Time,Type,Entry_Price,Exit_Price,Stop_Loss,Take_Profit,PnL,Duration_Minutes,Exit_Reason
```

## Technical Implementation
- Uses pandas for efficient data processing
- Handles both zipped and unzipped CSV files
- Vectorized FVG detection for performance
- Day-by-day trade simulation with proper order management
- Comprehensive error handling
- Progress tracking for long-running operations

## Notes
- The backtest processes over 2.7 million candles across 2,451 trading days
- All times are in Chicago Exchange Time (no conversion needed)
- The strategy shows a slightly negative edge with this parameter set
- Consider optimizing parameters like the stop buffer, R:R ratio, or trading window times

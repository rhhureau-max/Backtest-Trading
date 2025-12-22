# FVG Inversion Backtest Strategy

## Overview
This repository contains a complete implementation of a Fair Value Gap (FVG) Inversion trading strategy for NQ futures 5-minute data from 2018-2024.

## Strategy Description

### Fair Value Gap (FVG) Detection
- **Bearish FVG**: Occurs when `Low[i-1] > High[i+1]` - a gap between the low of candle i-1 and high of candle i+1
- **Bullish FVG**: Occurs when `High[i-1] < Low[i+1]` - a gap between the high of candle i-1 and low of candle i+1
- FVGs are detected **only during the 2:00-6:00 trading window**

### Entry Signals (Inversion Logic)
- **LONG Entry**: When a bullish candle (close > open) closes **ABOVE** the TOP of a Bearish FVG
- **SHORT Entry**: When a bearish candle (close < open) closes **BELOW** the BOTTOM of a Bullish FVG
- Only the last 10 detected FVGs are considered for entry signals
- Only one active trade at a time

### Risk Management
- **Stop Loss Calculation**:
  - LONG: Swing Low (minimum Low of last 10 candles before entry)
  - SHORT: Swing High (maximum High of last 10 candles before entry)
  
- **Take Profit**: Fixed at 2.2x risk-reward ratio (TP_MAX)
  - Example: If risk is 10 points, TP is at 22 points

### Parameters
- `SWING_LOOKBACK`: 10 candles
- `MAX_RECENT_FVGS`: 10 FVGs
- `RISK_REWARD_RATIOS`: [1.2, 1.5, 2.2]
- `TP_MAX`: 2.2x
- `TRADING_WINDOW`: 2:00 AM - 6:00 AM

## Files
- `fvg_inversion_backtest.py`: Main backtest script
- `fvg_inversion_results.csv`: Complete trade log with all entries and exits

## Usage

### Requirements
```bash
pip install pandas numpy
```

### Running the Backtest
```bash
python3 fvg_inversion_backtest.py
```

### Output
The script will:
1. Load all 5-minute CSV files (2018-2024)
2. Detect Fair Value Gaps during the trading window
3. Generate entry signals based on FVG inversions
4. Execute trades with proper stop loss and take profit
5. Display comprehensive statistics
6. Save full results to `fvg_inversion_results.csv`

## Results Summary (2018-2024)

### Overall Performance
- **Total Trades**: 3,999
- **Winning Trades**: 1,297 (32.43%)
- **Losing Trades**: 2,702 (67.57%)
- **Total P&L**: 7,042.47 points
- **Average Win**: 124.98 points
- **Average Loss**: -57.39 points
- **Profit Factor**: 1.05
- **Max Win**: 1,167.68 points
- **Max Loss**: -637.59 points

### Trade Distribution
- **LONG Trades**: 2,085
- **SHORT Trades**: 1,914

### Key Insights
1. The strategy has a relatively low win rate (32.43%) but positive total P&L
2. The average winning trade (124.98 points) is more than 2x the average losing trade (57.39 points)
3. The profit factor of 1.05 indicates slightly more profit than loss overall
4. The strategy generated nearly 4,000 trades over 7 years, averaging ~571 trades per year

## Data Format
The CSV files use semicolon separator with the following structure:
```
Column1;Column2;Column3;Column4;Column5;Column6;Column7
Date;Time;Open;High;Low;Close;Volume
DD/MM/YYYY;HH:MM:SS;price;price;price;price;volume
```

## Implementation Details

### FVG Detection Algorithm
The script scans through each candle during the trading window and checks for gaps:
- For Bearish FVG: Checks if there's a gap between `Low[i-1]` and `High[i+1]`
- For Bullish FVG: Checks if there's a gap between `High[i-1]` and `Low[i+1]`
- Stores FVG top, bottom, type, and creation index

### Trade Execution Logic
1. **Entry**: Monitors closing prices for inversions
   - Checks if current candle direction matches the inversion criteria
   - Validates against the last 10 detected FVGs
   - Calculates appropriate stop loss based on swing high/low

2. **Exit**: Two possible outcomes per candle
   - **Take Profit**: If price reaches TP_MAX (2.2x RR)
   - **Stop Loss**: If price hits the calculated stop loss level

3. **Position Management**: 
   - Only one trade active at a time
   - FVGs are marked as "used" once they trigger an entry
   - Trade tracking includes all relevant metrics (entry, exit, P&L, etc.)

## Example Trade Flow

1. **FVG Detection**: At 3:00 AM, a Bearish FVG is detected with top at 7500 and bottom at 7495
2. **Entry Signal**: At 4:00 AM, a bullish candle closes at 7505 (above the FVG top of 7500)
3. **Risk Calculation**: 
   - Entry: 7505
   - Stop Loss (swing low): 7490
   - Risk: 15 points
   - Take Profit: 7505 + (15 × 2.2) = 7538
4. **Exit**: Price reaches 7538, exit at TP_MAX with +33 point profit

## Notes
- The strategy is designed for futures trading with point-based P&L
- All trades are executed at close prices with stops/targets checked at high/low
- The implementation handles edge cases like invalid stop losses (skip trade if SL would be beyond entry)
- Results are saved in CSV format for further analysis in Excel or other tools

## Author
Expert Data Scientist in Algorithmic Trading

## License
This implementation is for educational and research purposes.

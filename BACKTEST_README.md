# Daily Bias Backtest for NQ (Nasdaq Futures)

This Python script backtests 4 different methods to predict the daily direction (Green vs Red candle) of the Nasdaq (NQ) futures market.

## Overview

The backtest evaluates which method best predicts whether a daily candle will close above or below its opening price, using historical data from 2018 to 2025.

**Important**: The data is already in UTC-6 (Chicago Time). No timezone conversion is performed.

## Requirements

Install the required Python packages:

```bash
pip install -r requirements.txt
```

## Data

The script uses three timeframes of NQ data:
- **Daily (D1)**: Files matching `*1D.csv`
- **4-Hour (H4)**: Files matching `*4H.csv`
- **1-Hour (H1)**: Files matching `*1H.csv` (loaded but not currently used)

CSV format: Date, Time, Open, High, Low, Close, Volume

## The 4 Methods

### Method 1: Price Action H4 (Swing High/Low)
- **LONG**: Current price > Last known Swing High on H4
- **SHORT**: Current price < Last known Swing Low on H4
- **NEUTRAL**: Price between last swing high and swing low

A swing high/low is identified when a candle's high/low is higher/lower than 3 candles on each side.

### Method 2: Trend D1 (EMA Alignment)
- **LONG**: Close(J-1) > EMA20(J-1) > EMA50(J-1)
- **SHORT**: Close(J-1) < EMA20(J-1) < EMA50(J-1)
- **NEUTRAL**: EMAs not properly aligned

### Method 3: Open vs Previous Value
- **LONG**: Open(J) > High(J-1)
- **SHORT**: Open(J) < Low(J-1)
- **NEUTRAL**: Open(J) within previous day's range

### Method 4: Triple Screen (EMA + RSI)
- **LONG**: Close(J-1) > EMA20(J-1) AND RSI_H4(last candle J-1) > 50
- **SHORT**: Close(J-1) < EMA20(J-1) AND RSI_H4(last candle J-1) < 50
- **NEUTRAL**: Conditions not met

## Usage

Run the backtest:

```bash
python3 daily_bias_backtest.py
```

## Output

The script generates:

1. **Console Output**: Comparative table with performance metrics
2. **backtest_results.csv**: Detailed daily results including:
   - Date
   - Actual direction (1=Green, -1=Red)
   - Signals from all 4 methods
   - Daily move (absolute value)
   - Open and Close prices

3. **backtest_metrics.csv**: Performance summary for each method:
   - Total number of trades
   - Win rate (%)
   - Number of wins and losses
   - Profit Factor (Sum of winning moves / Sum of losing moves)
   - Total winning and losing moves

## Performance Metrics

- **Win Rate**: Percentage of trades where the signal correctly predicted the direction
- **Profit Factor**: Ratio of total winning moves to total losing moves
  - > 1.0 indicates profitable strategy (if equal risk per trade)
  - Higher is better
- **Total Trades**: Number of days where the method generated a non-neutral signal

## Interpretation

A **Win** occurs when:
- Signal is LONG (1) and the day closes Green (Close > Open), OR
- Signal is SHORT (-1) and the day closes Red (Close < Open)

Days with NEUTRAL signals (0) are excluded from the trade count and metrics.

## Example Results

Based on the backtest from 2018-03-27 to 2025-11-12:

| Method | Total Trades | Win Rate % | Profit Factor |
|--------|-------------|-----------|---------------|
| M1     | 360         | 63.61%    | 2.30          |
| M2     | 1470        | 52.59%    | 1.00          |
| M3     | 103         | 48.54%    | 0.77          |
| M4     | 1380        | 51.81%    | 1.03          |

**Key Findings**:
- **Method 1 (Price Action H4)** shows the best performance with the highest win rate (63.61%) and profit factor (2.30)
- **Method 2 (Trend D1)** generates the most signals (1470 trades) but with modest performance
- **Method 3 (Open vs Prev)** is the most conservative with only 103 trades
- **Method 4 (Triple Screen)** provides balanced activity with slight edge over random

## Notes

- The backtest starts from day 60 to ensure sufficient data for EMA50 calculation
- All signals are calculated using only data available before or at the market open
- No look-ahead bias is introduced
- The profit factor assumes equal position sizing on all trades
- This is a directional bias analysis, not a complete trading system with entries/exits

## Future Enhancements

Possible improvements:
- Add 1-hour timeframe analysis
- Include stop-loss and take-profit levels
- Test different EMA periods
- Add more advanced money management
- Test different RSI thresholds
- Combine methods for ensemble predictions

# Quick Start Guide

## Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

## Running the Backtest

```bash
# Run the backtest script
python3 backtest_strategy.py
```

## Output Files

After running the script, you'll find these files:

- `trades_1m.csv` - All 1-minute timeframe trades
- `trades_5m.csv` - All 5-minute timeframe trades  
- `trades_15m.csv` - All 15-minute timeframe trades
- `all_trades.csv` - Combined trades from all timeframes
- `trades_summary.csv` - Summary statistics

## Understanding the Results

Each trade in the CSV files contains:

- **Date & Time**: When the trade occurred (always 08:30:00)
- **Direction**: LONG or SHORT
- **Price Data**: Open, High, Low, Close of the 8:30 AM candle
- **Reference Level**: The price level that was breached
- **Condition**: Human-readable explanation of why the trade qualified

## Example Trade

```
Date: 2018-01-02
Time: 08:30:00
Timeframe: 5m
Direction: LONG
Close: 7660.73
Reference Level: 7651.35
Condition: Close (7660.73) > Max Previous 5 Highs (7651.35)
```

This trade qualified because:
1. The 8:30 AM candle was bullish (Close > Open)
2. The close price (7660.73) exceeded the highest high of the previous 5 candles (7651.35)

## Quick Stats

Based on 2018-2025 data:

- **Total Trades**: 3,774
- **1m Timeframe**: 1,209 trades (52% long, 46% short)
- **5m Timeframe**: 1,372 trades (52% long, 48% short)
- **15m Timeframe**: 1,193 trades (53% long, 47% short)

## Next Steps

1. Open the CSV files in Excel or your preferred spreadsheet tool
2. Analyze the trades to identify patterns
3. Consider adding exit strategies and performance metrics
4. Backtest on your own data by modifying the script

For detailed documentation, see [BACKTEST_README.md](BACKTEST_README.md)

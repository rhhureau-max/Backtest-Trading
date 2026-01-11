# Quick Start Guide - FVG Inversion Backtester

## Installation

1. Ensure Python 3.8+ is installed
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Backtest

```bash
python3 fvg_inversion_backtest.py
```

## What the Script Does

1. **Loads Data**: Combines all yearly 5-minute CSV files (2018-2024)
2. **Detects FVGs**: Identifies all Fair Value Gaps in the data
3. **Runs Strategy**: 
   - Tracks FVG inversions within London (01:00-04:00) and New York (08:30-11:00) sessions
   - Takes only the FIRST valid signal per session ("One Bullet Rule")
   - Manages trades with 1:1 Risk-to-Reward ratio
4. **Generates Reports**:
   - Prints comprehensive performance statistics to console
   - Creates equity curve visualization (equity_curve.png)
   - Exports detailed trade log (trades_log.csv)

## Understanding the Output

### Console Output
- **Overall Performance**: Total trades, win rate, profit factor, net P&L
- **Session Breakdown**: Separate stats for London and New York
- **Direction Breakdown**: Performance of LONG vs SHORT trades

### equity_curve.png
- Top chart: Cumulative P&L over all trades
- Bottom chart: Individual trade results (green bars = wins, red bars = losses)

### trades_log.csv
Columns include:
- Entry/Exit DateTime and Price
- Direction (LONG/SHORT)
- Session (London/New York)
- Stop Loss and Take Profit levels
- Risk amount
- P&L and Status (Win/Loss)

## Strategy Parameters

### Fixed Parameters
- **Sessions**: London 01:00-04:00, New York 08:30-11:00 (Chicago Time)
- **Risk-to-Reward**: 1:1 (Distance to TP equals distance to SL)
- **Entry**: At close of signal candle
- **Stop Loss**: 
  - LONG: Signal candle's low
  - SHORT: Signal candle's high

### One Bullet Rule
Once a trade is taken in a session, no more entries are allowed until the next session starts. This prevents overtrading and ensures disciplined execution.

## Customization

To modify the script, edit `fvg_inversion_backtest.py`:

### Change Session Times
```python
self.london_start = time(1, 0)   # 01:00
self.london_end = time(4, 0)     # 04:00
self.ny_start = time(8, 30)      # 08:30
self.ny_end = time(11, 0)        # 11:00
```

### Change Risk-to-Reward Ratio
Look for these lines in `run_backtest()`:
```python
take_profit = entry_price + risk  # For LONG
take_profit = entry_price - risk  # For SHORT
```

Modify to 2:1 RRR:
```python
take_profit = entry_price + (2 * risk)  # For LONG
take_profit = entry_price - (2 * risk)  # For SHORT
```

### Change Data Source
```python
bt = FVGInversionBacktest(data_dir='/path/to/your/data')
```

## Troubleshooting

### No CSV files found
- Ensure CSV files are named: "2018 5m.csv", "2019 5m.csv", etc.
- Check they're in the same directory as the script or specify data_dir

### Missing packages
```bash
pip install pandas numpy matplotlib
```

### Memory issues with large datasets
The script loads all years at once. For very large datasets, consider:
- Processing years individually
- Using chunked reading with pandas
- Increasing system memory

## Strategy Notes

### Why Only LONG Trades?
If your backtest shows only LONG or only SHORT trades, this is normal. It means:
- Market conditions during the tested sessions favored one direction
- FVG inversions predominantly occurred in that direction
- Both LONG and SHORT logic are implemented; the market just didn't create balanced signals

### Interpreting Results
- **Win Rate < 50%**: Normal for FVG strategies; rely on risk management
- **Profit Factor < 1.0**: Strategy is losing money overall
- **Profit Factor > 1.0**: Strategy is profitable
- **High Win Rate + Low Profit**: Winners are smaller than losers
- **Low Win Rate + High Profit**: Big winners compensate for small losses

## Next Steps

1. **Optimize Parameters**: Test different session times or RRR ratios
2. **Add Filters**: Implement trend filters or volatility conditions
3. **Walk-Forward Analysis**: Test on different time periods
4. **Risk Per Trade**: Add position sizing based on account balance
5. **Commission/Slippage**: Account for real trading costs

## Support

For issues or questions about the strategy logic, refer to the code comments in `fvg_inversion_backtest.py`.

# FVG Backtest - Quick Start Guide

## Running the Backtest

### Step 1: Install Dependencies
```bash
pip install pandas numpy pytz
```

### Step 2: Run the Backtest
```bash
python3 fvg_backtest.py
```

### Step 3: View Results
The script will:
- Load all 1-minute data files (2018-2025)
- Scan for FVG patterns in the killzone (08:30-11:00)
- Execute trades based on the strategy rules
- Save results to `fvg_backtest_results.csv`
- Display summary statistics

## Expected Output

```
╔════════════════════════════════════════════════════════════════════════╗
║           FAIR VALUE GAP (FVG) BACKTEST - NQ 1-MINUTE DATA           ║
╚════════════════════════════════════════════════════════════════════════╝

Loading data files...
  Loading 2018 from CSV...
  Loading 2025 from CSV...
  Loading 2019-2024 from ZIP files...

Loaded 3,120,393 rows from 2018-01-01 to 2025-11-13

SCANNING FOR FVG SIGNALS
Total candles in killzone: 345,115
  Processed 1000 days, 1000 trades executed...
  ...

Backtest complete!
Total days scanned: 1,795
Total trades executed: 1,795

BACKTEST RESULTS SUMMARY
================================================================================
Total Trades:           1,795
Winning Trades:         831
Losing Trades:          964
Win Rate:               46.30%

Total PnL:              2,314.40 points
Average Win:            41.04 points
Average Loss:           -32.97 points

Profit Factor:          1.07
Maximum Drawdown:       1,850.48 points
Sharpe Ratio:           0.43
================================================================================

Trade log saved to: fvg_backtest_results.csv
```

## Analyzing Results

### Using Python
```python
import pandas as pd

# Load results
trades = pd.read_csv('fvg_backtest_results.csv')

# View first few trades
print(trades.head())

# Calculate custom metrics
print(f"Total PnL: {trades['pnl'].sum():.2f} points")
print(f"Win Rate: {len(trades[trades['result'] == 'WIN']) / len(trades) * 100:.1f}%")

# Monthly analysis
trades['month'] = pd.to_datetime(trades['entry_time']).dt.to_period('M')
monthly = trades.groupby('month')['pnl'].sum()
print(monthly)
```

### Using Excel
1. Open `fvg_backtest_results.csv` in Excel
2. Create pivot tables for analysis
3. Filter by date, trade type, or result
4. Calculate additional metrics as needed

## Output File Structure

The `fvg_backtest_results.csv` contains:

| Column | Description |
|--------|-------------|
| type | Trade direction (LONG or SHORT) |
| entry_price | Price at which trade was entered |
| exit_price | Price at which trade was exited |
| stop_loss | Stop loss level |
| take_profit | Take profit level |
| entry_time | Timestamp when trade was entered |
| exit_time | Timestamp when trade was exited |
| result | Trade outcome (WIN or LOSS) |
| pnl | Profit/Loss in points |
| signal_time | When FVG signal was identified |

## Customization

To modify the strategy parameters, edit `fvg_backtest.py`:

```python
class FVGBacktest:
    def __init__(self, data_dir: str = '.'):
        # Trading parameters
        self.killzone_start = time(8, 30)  # Change killzone start
        self.killzone_end = time(11, 0)    # Change killzone end
        self.sl_offset = 0.5               # Change stop loss offset
        self.risk_reward = 1.5             # Change risk-reward ratio
```

## Troubleshooting

### Issue: "No module named 'pandas'"
**Solution:** Install pandas with `pip install pandas numpy pytz`

### Issue: "No data files found"
**Solution:** Ensure you're running the script in the directory containing the CSV/ZIP files

### Issue: Script runs too slowly
**Solution:** This is normal - processing 3+ million candles takes a few minutes

## Performance Notes

- The backtest processes ~3.1 million candles
- Execution time: approximately 2-3 minutes
- Memory usage: ~500MB-1GB depending on system
- Output file size: ~260KB (1,795 trades)

## Next Steps

1. Analyze the trade log in detail
2. Experiment with different parameters
3. Add additional filters or conditions
4. Compare with other strategies
5. Perform walk-forward optimization

For more details, see `README_FVG_BACKTEST.md`

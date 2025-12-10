# Liquidity Sweep with FVG - Usage Guide

## Quick Start

### Prerequisites
```bash
pip install pandas numpy
```

### Basic Usage

Run the backtest on all available data (2018-2025):
```bash
python liquidity_sweep_fvg_backtest.py
```

Run with custom data directory:
```bash
python liquidity_sweep_fvg_backtest.py /path/to/your/data
```

### Expected Data Format

The script expects CSV files in the following format:
- File naming: `YYYY 5m.csv`, `YYYY 15m.csv`, `YYYY 1H.csv` (e.g., `2024 5m.csv`)
- Separator: semicolon (`;`)
- Columns: `Date;Time;Open;High;Low;Close;Volume`
- Date format: `DD/MM/YYYY`
- Time format: `HH:MM:SS`

Example data row:
```
01/01/2024;17:00:00;18250.5;18260.75;18245.25;18255.0;1500
```

## Output

### Console Output
The script displays:
- Data loading progress and statistics
- FVG and swing point detection results
- Real-time progress during H1 and M15 scanning (every 1000 candles)
- Final statistics with win rates for each RR level
- Sample of first 10 trades

### CSV Output
Generated file: `liquidity_sweep_fvg_results.csv`

Columns:
- `entry_date`: Trade entry date and time
- `entry_price`: Actual entry price
- `sl_price`: Stop loss price level
- `risk`: Risk amount (SL - Entry)
- `tp1`, `tp2`, `tp3`: Take profit levels for RR 1:1, 1:1.5, 1:2
- `setup_type`: Type of setup (`swing_sweep` or `fvg_mitigation`)
- `timeframe`: Context timeframe (`h1` or `m15`)
- `sweep_high`: Highest point of the sweep
- `m5_fvg_bottom`, `m5_fvg_top`: M5 FVG zone used for validation
- `outcome_rr1`, `outcome_rr1.5`, `outcome_rr2`: Win/Loss for each RR
- `exit_date_rr1`, `exit_date_rr1.5`, `exit_date_rr2`: Exit dates for each level

## Performance Expectations

### Execution Time
- **2024 data only** (~6k H1 + 24k M15 candles): ~16 seconds
- **Full dataset 2018-2025** (~41k H1 + 185k M15 candles): ~2-3 minutes

### Resource Usage
- **Memory**: ~500MB-1GB peak (depends on dataset size)
- **CPU**: Single-threaded, uses vectorized numpy operations
- **Disk**: Generates ~29MB CSV for full dataset (125k+ trades)

## Customization

### Date Range Filtering

To run on a specific date range, edit `main()` function in the script:

```python
# Run on 2024 data only
trades = strategy.run_backtest(start_date='2024-01-01', end_date='2024-12-31')

# Run on 2023-2024
trades = strategy.run_backtest(start_date='2023-01-01', end_date='2024-12-31')
```

### Strategy Parameters

In the `LiquiditySweepFVGStrategy` class, you can adjust:

**Swing Detection Lookback** (default: 5):
```python
self.m15_swings = detect_swing_points(self.m15, lookback=5)
self.h1_swings = detect_swing_points(self.h1, lookback=5)
```

**Setup Lookback Window** (defaults: 50 for H1, 100 for M15):
```python
# In check_swing_sweep() and check_fvg_mitigation()
max_lookback = 50 if timeframe == 'h1' else 100
```

**Trade Duration** (default: 100 M5 candles = ~8 hours):
```python
# In simulate_trade()
outcome = self.simulate_trade(..., max_bars=100)
```

**Risk Limits** (default: max 500 points):
```python
# In run_backtest()
if risk <= 0 or risk > 500:
    continue
```

## Troubleshooting

### No Data Loaded
**Error**: `FileNotFoundError: No files found for timeframe X`

**Solution**: Ensure your CSV files are named correctly:
- `2018 5m.csv`, `2019 5m.csv`, etc.
- `2018 15m.csv`, `2019 15m.csv`, etc.
- `2018 1H.csv`, `2019 1H.csv`, etc.

### Low Trade Count
**Issue**: Few or no trades found

**Possible Causes**:
1. Date range is too restrictive
2. Data quality issues (missing candles, gaps)
3. Strategy parameters are too strict

**Solutions**:
- Check your date range settings
- Verify data completeness with `print(len(df))` statements
- Try reducing lookback windows or max_bars

### Performance Issues
**Issue**: Script running very slowly

**Solutions**:
1. Reduce date range for testing
2. Check available memory (close other applications)
3. Ensure you're using the vectorized version of the script

### Memory Errors
**Issue**: Out of memory errors

**Solutions**:
1. Process data in yearly chunks
2. Reduce precision of float columns
3. Increase system swap space
4. Use a machine with more RAM

## Understanding the Results

### Win Rates Interpretation

For the full dataset (2018-2025):
- **RR 1:1**: ~31% win rate
- **RR 1:1.5**: ~23% win rate
- **RR 1:2**: ~18% win rate

These win rates are typical for mean-reversion strategies. The decreasing win rate with higher RR is expected as reaching further targets becomes progressively more difficult.

### Setup Statistics

**H1 Analysis**:
- ~34k setups found
- 99% have M5 FVG validation
- 81% result in price inversion (entry signal)

**M15 Analysis**:
- ~167k setups found
- 92% have M5 FVG validation
- 76% result in price inversion (entry signal)

The high percentage of setups with M5 FVG (>90%) indicates strong multi-timeframe confluence, which is a positive indicator for the strategy's logic.

## Further Analysis

### Post-Processing with Pandas

Load and analyze results:
```python
import pandas as pd

# Load results
df = pd.read_csv('liquidity_sweep_fvg_results.csv')

# Analyze by setup type
print(df.groupby('setup_type')['outcome_rr1'].value_counts(normalize=True))

# Analyze by timeframe
print(df.groupby('timeframe')['outcome_rr1'].value_counts(normalize=True))

# Monthly performance
df['month'] = pd.to_datetime(df['entry_date']).dt.to_period('M')
monthly = df.groupby('month')['outcome_rr1'].apply(lambda x: (x=='Win').sum())
print(monthly)

# Risk distribution
print(df['risk'].describe())
```

### Visualization Ideas

```python
import matplotlib.pyplot as plt

# Win rate by year
df['year'] = pd.to_datetime(df['entry_date']).dt.year
yearly_wr = df.groupby('year')['outcome_rr1'].apply(lambda x: (x=='Win').mean()*100)
yearly_wr.plot(kind='bar', title='Win Rate by Year (RR 1:1)')
plt.ylabel('Win Rate (%)')
plt.show()

# Risk distribution
df['risk'].hist(bins=50)
plt.xlabel('Risk (points)')
plt.title('Risk Distribution')
plt.show()
```

## Support

For questions or issues:
1. Review the README_LIQUIDITY_SWEEP_FVG.md for strategy details
2. Check OPTIMIZATION_SUMMARY.md for performance insights
3. Examine the code comments for implementation details
4. Verify your data format matches the expected structure

## Version History

- **v1.0** (2024-12): Initial vectorized implementation with binary search optimization

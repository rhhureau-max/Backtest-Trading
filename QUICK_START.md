# Quick Start Guide - Judas Swing Backtest

## Prerequisites

1. Python 3.7 or higher installed
2. Required packages: pandas, matplotlib, numpy

## Installation Steps

### Step 1: Install Dependencies

```bash
pip install pandas matplotlib numpy
```

Or if using pip3:

```bash
pip3 install pandas matplotlib numpy
```

## Running the Backtest

### Option A: Using Multiple Yearly Files (Recommended)

This is the default configuration and works with the existing data files in the repository.

```bash
python3 judas_swing_backtest.py
```

The script will automatically:
- Load all available yearly files (2018 5m.csv, 2019 5m.csv, etc.)
- Combine them into a single dataset
- Process all trading days
- Generate results and visualizations

**Expected Runtime**: 2-3 minutes depending on system

### Option B: Using a Single Combined File

1. Create or prepare a file named `NQ_Data.csv` with columns: Date, Time, Open, High, Low, Close

2. Edit `judas_swing_backtest.py` and change line 437:
   ```python
   DATA_SOURCE = 'single'  # Change from 'combined'
   ```

3. Run the script:
   ```bash
   python3 judas_swing_backtest.py
   ```

## Output Files

After running, you will find:

1. **Console Output**: Detailed statistics printed to terminal
2. **judas_swing_distribution.png**: Histogram showing extension distribution
3. **judas_swing_results.csv**: Detailed CSV with all detected patterns

## Example Output

```
======================================================================
JUDAS SWING BACKTEST - NASDAQ 100 (NQ)
======================================================================

Loading combined yearly data files...
Loading 2018 5m.csv...
  Loaded 69937 rows from 2018 5m.csv
...

Total rows loaded: 554518
Data range: 2018-01-01 17:00:00 to 2025-11-11 23:50:00

======================================================================
JUDAS SWING BACKTEST RESULTS
======================================================================

DATA SUMMARY:
  Total trading days analyzed: 2449
  Date range: 2018-01-01 to 2025-11-11

MANIPULATION OCCURRENCES:
  Total Tokyo range breaks (01:00-05:00): 1735
  Bearish manipulations (break below Tokyo low): 877 (50.5%)
  Bullish manipulations (break above Tokyo high): 858 (49.5%)
  Percentage of days with manipulation: 70.8%

EXTENSION STATISTICS (in points):
  Average extension (all): 40.82
  Average extension (bearish): 43.20
  Average extension (bullish): 38.39
...
======================================================================
```

## Customization

### Change Years to Analyze

Edit line 442 in `judas_swing_backtest.py`:

```python
YEARS_TO_ANALYZE = [2020, 2021, 2022]  # Only these years
```

### Adjust Session Times

Modify the session definitions in the `_analyze_trading_day()` method around line 170-180.

## Troubleshooting

### Error: "No module named 'pandas'"
**Fix**: Install dependencies: `pip install pandas matplotlib numpy`

### Error: "No data files found"
**Fix**: Ensure CSV files (e.g., "2018 5m.csv") are in the same directory as the script

### Error: "FileNotFoundError: NQ_Data.csv"
**Fix**: Either create the file or switch to 'combined' mode (default)

### Script runs slowly
**Normal**: Processing 500K+ rows can take 2-3 minutes. Be patient!

## Understanding Results

- **Bearish Manipulation**: Price breaks BELOW Tokyo low during 01:00-05:00 (Long setup)
- **Bullish Manipulation**: Price breaks ABOVE Tokyo high during 01:00-05:00 (Short setup)
- **Extension Points**: How far price travels beyond the Tokyo range boundary
- **70.8% occurrence**: Tokyo range is broken on ~7 out of 10 trading days

## Next Steps

1. Review the histogram: `judas_swing_distribution.png`
2. Analyze detailed results: `judas_swing_results.csv`
3. Read full documentation: `JUDAS_SWING_README.md`
4. Study the results summary: `BACKTEST_RESULTS_SUMMARY.md`

## Support

For questions or issues:
1. Check the README: `JUDAS_SWING_README.md`
2. Review the results summary: `BACKTEST_RESULTS_SUMMARY.md`
3. Examine the script comments for implementation details

---

**Last Updated**: December 23, 2025
**Script Version**: 1.0

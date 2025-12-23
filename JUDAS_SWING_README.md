# Judas Swing Backtest Strategy - Nasdaq 100 (NQ)

## Overview

This script backtests the "Judas Swing" trading strategy on Nasdaq 100 (NQ) futures data. The strategy identifies manipulation patterns during the London session that break the Tokyo session range.

## Strategy Description

### Session Definitions (New York/EST Time)

- **Tokyo Session**: 18:00 (previous day) to 01:00 (current day)
- **London Manipulation Window**: 01:00 to 05:00 (current day)

### Trading Logic

1. **Tokyo Range**: Calculate the High and Low reached during the Tokyo Session (18:00-01:00)
2. **London Manipulation**: Observe price action during 01:00-05:00 window
3. **Bearish Manipulation (Long Setup)**: Price breaks below Tokyo Low during London window
4. **Bullish Manipulation (Short Setup)**: Price breaks above Tokyo High during London window
5. **Extension Measurement**: Calculate how far price extends beyond the Tokyo range in points

## Installation

### Requirements

- Python 3.7 or higher
- pandas
- matplotlib
- numpy

### Install Dependencies

```bash
pip install pandas matplotlib numpy
```

## Data Format

The script expects CSV files with the following format:

```
Column1;Column2;Column3;Column4;Column5;Column6;Column7
Date;Time;Open;High;Low;Close;Volume
01/01/2018;17:00:00;7503.74;7511.94;7499.64;7511.35;1451
```

- **Separator**: Semicolon (;)
- **Date Format**: DD/MM/YYYY
- **Time Format**: HH:MM:SS
- **Timezone**: EST/New York time (assumed)

## Usage

### Method 1: Using Multiple Yearly Files (Default)

The script will automatically load and combine multiple yearly files:

```bash
python3 judas_swing_backtest.py
```

Expected file names: `2018 5m.csv`, `2019 5m.csv`, `2020 5m.csv`, etc.

### Method 2: Using a Single Combined File

To use a single file named `NQ_Data.csv`:

1. Edit the script and change:
   ```python
   DATA_SOURCE = 'single'  # Change from 'combined' to 'single'
   ```

2. Ensure your data file is named `NQ_Data.csv` with columns: Date, Time, Open, High, Low, Close

3. Run the script:
   ```bash
   python3 judas_swing_backtest.py
   ```

### Method 3: Customizing Years to Analyze

Edit the `YEARS_TO_ANALYZE` list in the script:

```python
YEARS_TO_ANALYZE = [2020, 2021, 2022, 2023, 2024]  # Only analyze these years
```

## Output Files

The script generates three output files:

### 1. Console Output

Displays detailed statistics including:
- Total trading days analyzed
- Number of bearish vs bullish manipulations
- Average extension in points
- Percentile distributions

### 2. judas_swing_distribution.png

A histogram visualization showing:
- Overall distribution of extensions beyond Tokyo range
- Separate distributions for bearish and bullish manipulations
- Mean and median markers

### 3. judas_swing_results.csv

Detailed CSV file with all detected patterns:
- Date
- Type (Bearish/Bullish)
- Tokyo_High
- Tokyo_Low
- Manipulation_Extreme (the furthest point reached)
- Extension_Points (distance beyond Tokyo range)

## Sample Results

Based on backtesting from 2018-2025:

```
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

EXTENSION DISTRIBUTION:
  Minimum: 0.25
  25th percentile: 12.52
  Median (50th percentile): 28.35
  75th percentile: 54.67
  90th percentile: 89.87
  Maximum: 611.62
======================================================================
```

## Interpretation

### Key Findings

1. **High Occurrence Rate**: The Tokyo range is broken during the London manipulation window on approximately 71% of trading days
2. **Balanced Direction**: Bearish and bullish manipulations occur almost equally (50.5% vs 49.5%)
3. **Average Extension**: On average, price extends about 40-43 points beyond the Tokyo range
4. **Variation**: Extensions range from less than 1 point to over 600 points, with significant variation

### Trading Implications

- **Entry**: When Tokyo range is broken during 01:00-05:00 EST
- **Target Expectations**: 
  - Conservative: 12-28 points (25th-50th percentile)
  - Moderate: 28-55 points (50th-75th percentile)
  - Aggressive: 55-90 points (75th-90th percentile)
- **Risk Management**: Account for the wide distribution of extensions

## Customization

### Adjusting Session Times

Edit the `_analyze_trading_day()` method to change session definitions:

```python
# Tokyo Session: 18:00 previous day to 01:00 current day
tokyo_session = self.df[
    ((self.df['Date_Only'] == previous_date) & (self.df['Hour'] >= 18)) |
    ((self.df['Date_Only'] == trading_date) & (self.df['Hour'] < 1))
]

# London Window: 01:00 to 05:00 current day
london_window = self.df[
    (self.df['Date_Only'] == trading_date) &
    (self.df['Hour'] >= 1) &
    (self.df['Hour'] < 5)
]
```

### Adding Additional Metrics

The script is structured as a class, making it easy to extend with additional analysis methods.

## Troubleshooting

### Issue: "No module named 'pandas'"
**Solution**: Install required packages: `pip install pandas matplotlib numpy`

### Issue: "No data files found"
**Solution**: Ensure CSV files are in the same directory as the script and named correctly (e.g., "2018 5m.csv")

### Issue: "No Judas Swing patterns detected"
**Solution**: Check that your data covers the required time periods (18:00-05:00 EST) and has sufficient coverage

## Technical Notes

- The script assumes data is already in EST/New York timezone
- 5-minute data is recommended for accurate session range calculation
- The script handles missing dates and data gaps gracefully
- Processing time depends on the amount of data (typically 1-3 minutes for 8 years)

## Author

Created by Algorithmic Trading Agent
Date: 2025-12-23

## License

This script is provided for educational and research purposes.

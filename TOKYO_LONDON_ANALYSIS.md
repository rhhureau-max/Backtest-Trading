# Tokyo-London Session Analysis

This script analyzes NQ (Nasdaq-100 E-mini futures) 1-minute data to identify and compare trading patterns during the Tokyo Session and London Killzone.

## Overview

The script identifies two mutually exclusive scenarios during the London Killzone (01:00 - 05:00) based on price behavior relative to the Tokyo Session (18:00 - 01:00):

1. **Judas Swing / Reversal (Scenario A)**: Price breaks a Tokyo extreme (High or Low) but returns to touch the Tokyo Equilibrium (EQ) before 05:00
2. **London Continuation (Scenario B)**: Price breaks a Tokyo extreme and does NOT return to the Tokyo EQ before 05:00

## Installation

```bash
pip install -r requirements.txt
```

Requirements:
- Python 3.7+
- pandas >= 2.0.0
- numpy >= 1.24.0

## Usage

Simply run the script from the repository directory:

```bash
python tokyo_london_analysis.py
```

Or specify a custom data directory:

```bash
python tokyo_london_analysis.py /path/to/data
```

You can also set the `BACKTEST_DATA_PATH` environment variable:

```bash
export BACKTEST_DATA_PATH=/path/to/data
python tokyo_london_analysis.py
```

The script will automatically:
1. Load all NQ 1-minute data files (both CSV and ZIP formats) from 2018 to present
2. Identify Tokyo and London sessions
3. Analyze breakout patterns
4. Print comprehensive statistics to the console

## Key Concepts

### Tokyo Session
- **Time**: 18:00 (previous day) to 01:00 (current day)
- **Metrics Calculated**:
  - Tokyo High: Highest price during Tokyo session
  - Tokyo Low: Lowest price during Tokyo session
  - Tokyo EQ: Equilibrium = (Tokyo High + Tokyo Low) / 2
  - Tokyo Range: Tokyo High - Tokyo Low

### London Killzone
- **Time**: 01:00 to 05:00
- **Analysis**: Detects breakouts of Tokyo extremes and measures continuation vs reversal patterns

### Breakout Classification
1. **Breakout**: Price exceeds Tokyo High (bullish) or Tokyo Low (bearish) during London session
2. **Judas Swing**: Breakout followed by return to Tokyo EQ
3. **Continuation**: Breakout without return to Tokyo EQ

## Output Metrics

The script provides the following statistics:

### 1. Breakout Statistics
- Total sessions with breakout
- Count and percentage of Judas Swings
- Count and percentage of London Continuations

### 2. Continuation Probability
- Probability that a breakout will be a continuation
- Probability that a breakout will be a Judas Swing

### 3. Direction Analysis
- Percentage of bullish vs bearish continuations

### 4. Expansion Metrics (for Continuations)
- **Max Expansion**: Distance (in points) traveled beyond the broken extreme
- Statistics: Mean, Median, Min, Max

### 5. Range Multiplier (Expansion Ratio)
- **Ratio**: Max Expansion / Tokyo Range
- Indicates how many times London extends the Tokyo range
- Example: 1.5x means London extends Tokyo range by 1.5 times

### 6-7. Direction-Specific Metrics
- Separate statistics for bullish and bearish continuations

## Performance

- Processing Speed: ~162,000 rows/second
- Total Processing Time: ~17 seconds for 2.7M rows (2018-2025 data)
- Memory Efficient: Uses pandas optimized operations

## Data Format

The script expects NQ 1-minute data in the following format:
- CSV files with semicolon (;) separator
- Columns: Date, Time, Open, High, Low, Close, Volume
- Date format: DD/MM/YYYY
- Time format: HH:MM:SS
- Supports both .csv and .csv.zip files

## Example Output

```
======================================================================
TOKYO-LONDON SESSION ANALYSIS RESULTS
======================================================================

1. BREAKOUT STATISTICS:
   Total sessions with breakout: 1736
   - Judas Swings (Reversal): 534 (30.8%)
   - London Continuations: 1202 (69.2%)

2. CONTINUATION PROBABILITY:
   Probability of Continuation: 69.24%
   Probability of Judas Swing: 30.76%

3. CONTINUATION DIRECTION:
   Bullish Continuations: 737 (61.3%)
   Bearish Continuations: 465 (38.7%)

4. EXPANSION METRICS (for Continuations):
   Max Expansion - Mean: 48.22 points
   Max Expansion - Median: 35.35 points
   Max Expansion - Min: 0.26 points
   Max Expansion - Max: 611.62 points

5. RANGE MULTIPLIER (Expansion Ratio):
   Mean Ratio: 0.72x
   Median Ratio: 0.55x
   Min Ratio: 0.00x
   Max Ratio: 5.57x
   Interpretation: On average, London continuation extends Tokyo range by 0.72x

6. BULLISH CONTINUATION METRICS:
   Mean Expansion: 41.81 points
   Mean Ratio: 0.63x

7. BEARISH CONTINUATION METRICS:
   Mean Expansion: 58.39 points
   Mean Ratio: 0.86x

======================================================================

Execution time: 17.10 seconds
Processing speed: 162,055 rows/second
```

## Key Findings

Based on the analysis of NQ data from 2018-2025:
- **69.2%** of breakouts result in London Continuations
- **30.8%** of breakouts are Judas Swings (reversals)
- Bullish continuations are more frequent (61.3%) than bearish (38.7%)
- Bearish continuations tend to have larger expansions (58.39 points avg) vs bullish (41.81 points avg)
- On average, London continuations extend the Tokyo range by 0.72x

## Trading Implications

This analysis suggests that:
1. When a Tokyo extreme is broken during London, it's more likely to continue (69%) than reverse
2. Traders should be cautious of false breakouts (Judas Swings) which occur ~31% of the time
3. Bearish breakouts tend to be more explosive when they continue
4. The median continuation extends about 35 points beyond the Tokyo extreme

## Customization

You can modify the script to:
- Change session times (edit `identify_sessions` function)
- Add additional metrics or filters
- Export results to CSV/Excel
- Create visualizations of the patterns
- Filter by specific date ranges or market conditions

## Notes

- All times are in the timezone of the data files
- The script handles both regular CSV files and ZIP-compressed CSV files
- Sessions without sufficient data are automatically filtered out
- NaN values in price data are handled gracefully

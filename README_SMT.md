# SMT Divergence Detector

A Python-based tool for detecting SMT (Smart Money Technique) divergences between NQ (NASDAQ-100 E-mini Futures) and ES (S&P 500 E-mini Futures) during key trading sessions.

## Overview

**SMT Divergence** is a concept in Smart Money trading that identifies when two correlated assets (like NQ and ES) move differently at key swing points, indicating potential leadership and directional bias.

### Types of SMT Divergence

1. **Bullish SMT Divergence**
   - One asset makes a **Lower Low (LL)** while the other makes a **Higher Low (HL)**
   - The asset making the HL is the **Bullish Leader** (stronger, refuses to go lower)
   - Suggests potential upward momentum

2. **Bearish SMT Divergence**
   - One asset makes a **Higher High (HH)** while the other makes a **Lower High (LH)**
   - The asset making the LH is the **Bearish Leader** (weaker, refuses to go higher)
   - Suggests potential downward momentum

### Trading Sessions

The detector focuses on two high-probability trading sessions (Chicago/UTC-6 time):

- **London Session**: 02:00 - 05:00 (overlap with London open)
- **New York AM Session**: 08:30 - 11:00 (New York open to lunch)

## Features

- ✅ Loads NQ and ES data from semicolon-delimited CSV files
- ✅ Filters data by trading sessions (London and NY AM)
- ✅ Detects swing highs and swing lows using local extrema
- ✅ Aligns swing points between NQ and ES (±10 minute tolerance)
- ✅ Identifies bullish and bearish SMT divergences
- ✅ Generates comprehensive statistics and leadership analysis
- ✅ Creates visualizations of detected divergences
- ✅ Exports results to CSV for further analysis

## Installation

### Requirements

- Python 3.8 or higher
- Dependencies listed in `requirements.txt`

### Setup

1. **Clone or navigate to the repository:**
   ```bash
   cd /path/to/Backtest-Trading
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

   Or install individually:
   ```bash
   pip install pandas numpy scipy matplotlib
   ```

## Usage

### Basic Usage

Run the detector on all historical data (2018-today) with 5-minute timeframe:

```bash
python smt_divergence_detector.py
```

### Advanced Usage

**Analyze specific year:**
```bash
python smt_divergence_detector.py --years 2024
```

**Analyze multiple years:**
```bash
python smt_divergence_detector.py --years 2023 2024
```

**Use 15-minute timeframe:**
```bash
python smt_divergence_detector.py --timeframe 15m
```

**Specify custom data directory:**
```bash
python smt_divergence_detector.py --years 2024 --path /path/to/csv/files
```

**Custom output directory:**
```bash
python smt_divergence_detector.py --years 2024 --output my_results
```

### Command-Line Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--years` | Years to analyze (space-separated) | `2024` |
| `--timeframe` | Timeframe: `5m` or `15m` | `5m` |
| `--path` | Base directory containing CSV files | `.` (current dir) |
| `--output` | Output directory for results | `smt_analysis_results` |

### Help

```bash
python smt_divergence_detector.py --help
```

## Input Data Format

The script expects CSV files with the following format:

### File Naming Conventions

**NQ (NASDAQ) files:**
- Format: `{YEAR} {TIMEFRAME}.csv`
- Examples: `2024 5m.csv`, `2024 15m.csv`

**ES (S&P 500) files:**
- Format: `ES {TIMEFRAME} ({YEAR_RANGE}).csv`
- Examples: `ES 5m (2024-2025).csv`, `ES 15m (2018-2025).csv`

### CSV Structure

```
Column1;Column2;Column3;Column4;Column5;Column6;Column7
01/01/2024;17:00:00;18244.57923;18248.331274;18238.951165;18241.631196;1308
```

- **Delimiter**: Semicolon (`;`)
- **Columns**:
  - `Column1`: Date (DD/MM/YYYY)
  - `Column2`: Time (HH:MM:SS)
  - `Column3`: Open price
  - `Column4`: High price
  - `Column5`: Low price
  - `Column6`: Close price
  - `Column7`: Volume

**Note**: Data should be in UTC-6 (Chicago time zone).

## Output

### Generated Files

The script creates an output directory (default: `smt_analysis_results/`) containing:

1. **`smt_statistics.csv`**
   - Summary statistics by session (London, NY) and totals
   - Counts of bullish/bearish divergences
   - Leadership counts for each asset

2. **`smt_divergences_detailed.csv`**
   - Complete list of all detected divergences
   - Timestamps, price levels, directions, and leaders
   - Can be used for further analysis or backtesting

3. **Visualization PNG files**
   - Example charts showing detected divergences
   - Naming: `smt_example_{year}_{session}_{type}.png`
   - Up to 4 examples (one per session/type combination)

### Statistics Report

The console output includes:

```
### STATISTICS ###
Session  Total Divergences  Bullish SMT  Bearish SMT  NQ Bullish Leader  ES Bullish Leader  ...
LONDON              15            8            7                4                  4
NY                  23           12           11                6                  6
TOTAL               38           20           18               10                 10

### LEADERSHIP ANALYSIS ###
Bullish Leader: NQ 50.0% | ES 50.0%
Bearish Leader: NQ 55.6% | ES 44.4%
```

### Visualization Examples

Each chart shows:
- Top panel: NQ price with swing points
- Bottom panel: ES price with swing points
- Red markers and dashed lines connecting swing points
- Title indicating divergence type, leader, and session

## Understanding Results

### Leadership Interpretation

**Bullish Leadership**:
- Asset that more frequently makes Higher Lows (refuses to go lower)
- Indicates relative strength
- May lead rallies

**Bearish Leadership**:
- Asset that more frequently makes Lower Highs (refuses to go higher)
- Indicates relative weakness
- May lead declines

### Trading Insights

1. **Session Analysis**: Compare London vs NY sessions to identify time-of-day patterns
2. **Asset Leadership**: Identify which asset (NQ or ES) typically leads moves
3. **Divergence Frequency**: High-frequency divergences may indicate choppy/ranging markets
4. **Leader Shifts**: Changes in leadership patterns may signal regime changes

## Algorithm Details

### Swing Point Detection

- Uses `scipy.signal.argrelextrema()` for local extrema detection
- Default order: 5 (requires 5 candles on each side to confirm)
- Swing highs: Local maxima in High prices
- Swing lows: Local minima in Low prices

### Alignment Logic

- Matches swing points between NQ and ES within ±10 minute window
- Uses closest timestamp match within tolerance
- Ensures we're comparing contemporaneous market structures

### Divergence Rules

**Bullish SMT**:
```
NQ: LL (Lower Low)     ES: HL (Higher Low)  → ES is Bullish Leader
   OR
NQ: HL (Higher Low)    ES: LL (Lower Low)   → NQ is Bullish Leader
```

**Bearish SMT**:
```
NQ: HH (Higher High)   ES: LH (Lower High)  → ES is Bearish Leader
   OR
NQ: LH (Lower High)    ES: HH (Higher High) → NQ is Bearish Leader
```

## Customization

### Adjusting Swing Detection Sensitivity

Edit the `find_swing_points()` method in the script:

```python
# More sensitive (more swing points detected)
swing_highs, swing_lows = self.find_swing_points(df, order=3)

# Less sensitive (fewer, more significant swing points)
swing_highs, swing_lows = self.find_swing_points(df, order=7)
```

### Adjusting Time Alignment Tolerance

Edit the `align_swings()` call in `detect_smt_divergences()`:

```python
# Stricter alignment (within ±5 minutes)
aligned_highs = self.align_swings(nq_highs, es_highs, tolerance_minutes=5)

# Looser alignment (within ±15 minutes)
aligned_highs = self.align_swings(nq_highs, es_highs, tolerance_minutes=15)
```

### Modifying Trading Sessions

Edit session times in `__init__()`:

```python
self.london_session = (time(1, 0), time(5, 0))   # 01:00-05:00
self.ny_session = (time(8, 0), time(12, 0))      # 08:00-12:00
```

## Troubleshooting

### No Data Found

**Error**: `⚠ No NQ data found for {year}`

**Solutions**:
- Verify CSV files exist in the specified directory
- Check file naming matches expected format
- Use `--path` to specify correct directory

### No Divergences Detected

**Possible causes**:
- Not enough swing points in the data (try lower `order` parameter)
- Session times don't have sufficient data
- Time alignment tolerance too strict (try increasing `tolerance_minutes`)

### Import Errors

```bash
ModuleNotFoundError: No module named 'scipy'
```

**Solution**: Install missing dependencies
```bash
pip install -r requirements.txt
```

## Example Workflow

```bash
# 1. Ensure you're in the repository directory
cd /home/runner/work/Backtest-Trading/Backtest-Trading

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run analysis on 2024 data (5-minute timeframe)
python smt_divergence_detector.py --years 2024 --timeframe 5m

# 4. Check results
cd smt_analysis_results
ls -la
# You'll see:
# - smt_statistics.csv
# - smt_divergences_detailed.csv
# - smt_example_*.png files

# 5. View statistics
cat smt_statistics.csv

# 6. Open visualizations (if on desktop environment)
# Or transfer files to view elsewhere
```

## Technical Notes

### Performance

- Processing speed depends on:
  - Data volume (number of candles)
  - Swing detection sensitivity (order parameter)
  - Number of years analyzed
- Typical runtime: 10-30 seconds per year for 5m data

### Memory Usage

- Loads entire datasets into memory
- Peak usage: ~200-500 MB for a full year of 5m data
- Sufficient for typical desktop/laptop systems

### Data Quality

- Script handles missing data by dropping NaN values
- Automatically converts columns to numeric type
- Assumes data is already in UTC-6 timezone (no conversion)

## Future Enhancements

Potential improvements for future versions:

- [ ] Add more timeframes (1m, 30m, 1h)
- [ ] Include additional sessions (Asian, European close)
- [ ] Implement backtesting framework to test divergence signals
- [ ] Add real-time data streaming capability
- [ ] Create interactive HTML dashboard
- [ ] Support for more correlated pairs (YM, RTY)
- [ ] Machine learning for divergence quality scoring

## References

- **Smart Money Concepts (SMC)**: Institutional trading framework
- **ICT (Inner Circle Trader)**: Source of SMT divergence concepts
- **Correlation Analysis**: Understanding NQ/ES relationship

## License

This script is provided as-is for educational and research purposes.

## Support

For issues or questions:
1. Check the Troubleshooting section
2. Review example output in the repository
3. Verify data format matches specifications
4. Open an issue on GitHub with:
   - Command used
   - Error messages
   - Sample data (if possible)

---

**Last Updated**: December 2024  
**Version**: 1.0.0

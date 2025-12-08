# FVG Tokyo Session Analysis

## Overview

This script analyzes Fair Value Gaps (FVG) that form specifically during the Tokyo session hours (19:00-23:00) on NQ (Nasdaq Futures) 1-hour data from 2018 to present.

**NEW**: The script now includes analysis of Tokyo FVGs filled during the London killzone (01:00-04:00) the next day, answering the critical question: "What is the probability that Tokyo session FVGs from day N-1 are filled during the London killzone on day N?"

## What is a Fair Value Gap (FVG)?

A Fair Value Gap is a price imbalance that occurs when the market moves so quickly that it leaves a "gap" in price action. These gaps often act as magnets for future price action.

### FVG Types

1. **Bullish FVG**: Occurs when `Low[i] > High[i-2]`
   - The gap zone is between `High[i-2]` and `Low[i]`
   - Indicates strong upward momentum

2. **Bearish FVG**: Occurs when `High[i] < Low[i-2]`
   - The gap zone is between `Low[i-2]` and `High[i]`
   - Indicates strong downward momentum

### Fill Detection

An FVG is considered "filled" or "touched" when future price action retraces into the gap zone:
- **Bullish FVG filled**: When a future candle's Low touches or penetrates below the upper boundary of the gap
- **Bearish FVG filled**: When a future candle's High touches or penetrates above the lower boundary of the gap

## Requirements

```bash
pip install pandas numpy
```

## Usage

### Basic Usage

Simply run the script from the directory containing your 1H CSV files:

```bash
python3 fvg_tokyo_session_analysis.py
```

### Expected Data Format

The script expects CSV files with the following format:
- Filename pattern: `*1H.csv` (e.g., "2018 1H.csv", "2019 1H.csv", etc.)
- Delimiter: semicolon (;)
- Columns: Date, Time, Open, High, Low, Close, Volume
- Date format: DD/MM/YYYY
- Time format: HH:MM:SS

Example:
```
Column1;Column2;Column3;Column4;Column5;Column6;Column7
01/01/2018;17:00:00;7503.74;7518.09;7499.64;7517.80;2852
01/01/2018;18:00:00;7517.51;7525.71;7517.21;7522.78;2117
```

## Output

### Console Output

The script displays comprehensive statistics including:

1. **Global Statistics**
   - Total FVGs created during Tokyo session
   - Bullish vs Bearish distribution
   - Average FVGs per trading session
   - Average gap sizes

2. **Fill/Retracement Analysis**
   - Total and individual fill rates for bullish/bearish FVGs
   - Average number of candles until fill

3. **Sample FVGs**
   - Detailed information about the first 10 FVGs

4. **NEW: London Killzone Fill Analysis**
   - Probability that Tokyo FVGs are filled during London killzone (01:00-04:00 next day)
   - Comparison of fill rates between overall vs London killzone
   - Bullish vs Bearish fill rates in London
   - Average candles to fill during London session
   - Sample London killzone fills

### CSV Export

The script generates TWO CSV files:

#### 1. `fvg_tokyo_session_results.csv` (Basic Analysis)

| Column | Description |
|--------|-------------|
| datetime | Full datetime of FVG creation |
| date | Date in DD/MM/YYYY format |
| time | Time in HH:MM:SS format |
| hour | Hour of creation (19-23) |
| type | Bullish or Bearish |
| zone_low | Lower boundary of the gap |
| zone_high | Upper boundary of the gap |
| gap_size | Size of the gap in points |
| filled | Whether the FVG was filled (True/False) |
| fill_datetime | When the FVG was filled (if filled) |
| candles_to_fill | Number of candles until fill (if filled) |

#### 2. `fvg_tokyo_london_killzone_results.csv` (NEW - London Analysis)

All columns from above, PLUS:

| Column | Description |
|--------|-------------|
| london_filled | Whether filled during London killzone (01:00-04:00 next day) |
| london_fill_datetime | When filled during London killzone |
| london_candles_to_fill | Number of candles to London fill |

## Example Results

Based on NQ data from 2018 to 2025:

```
FVG TOKYO SESSION ANALYSIS RESULTS (19:00-23:00)
================================================================

DATE RANGE: 2018-01-01 to 2025-11-11
Total Trading Days: 2164

GLOBAL STATISTICS
----------------------------------------------------------------
Total FVGs Created (Tokyo Session):     1716
  - Bullish FVGs:                        979 (57.05%)
  - Bearish FVGs:                        737 (42.95%)

Average FVGs per Session:                0.79
Average Gap Size (All):                  11.96 points

FILL/RETRACEMENT ANALYSIS
----------------------------------------------------------------
Global Fill Rate:                        99.30%
Bullish Fill Rate:                       98.98%
Bearish Fill Rate:                       99.73%
Average Candles to Fill:                 47.02 candles

LONDON KILLZONE FILL ANALYSIS (NEW)
================================================================
Total Tokyo FVGs:                        1716
Filled in London Killzone:               1191 / 1716
London Killzone Fill Rate:               69.41%

Bullish FVGs in London:                  665 / 979
Bullish London Fill Rate:                67.93%

Bearish FVGs in London:                  526 / 737
Bearish London Fill Rate:                71.37%

Average Candles to Fill (London):        4.40 candles
```

## Key Findings

### Overall Fill Behavior

1. **High Fill Rate**: Over 99% of FVGs created during Tokyo session are eventually filled, confirming that these gaps act as strong magnets for price.

2. **Balanced Distribution**: Slightly more bullish FVGs (57%) than bearish (42%), indicating a mild upward bias during Tokyo hours.

3. **Quick Fills**: On average, FVGs are filled within 47 candles (~2 days), suggesting relatively quick mean reversion.

4. **Bearish FVGs More Reliable**: Bearish FVGs show a marginally higher fill rate (99.73%) compared to bullish FVGs (98.98%).

### NEW: London Killzone Findings

5. **69.41% London Probability**: Nearly 7 out of 10 Tokyo FVGs (from day N-1) are filled during the London killzone (01:00-04:00) on day N. This is a VERY HIGH probability for intraday mean reversion.

6. **Bearish Edge in London**: Bearish FVGs have 71.37% London fill rate vs 67.93% for bullish FVGs, showing stronger downward retracement during London hours.

7. **Very Quick London Fills**: FVGs filled during London killzone are touched in just 4.40 candles on average (vs 47 candles overall), indicating the London session provides rapid liquidity into Tokyo gaps.

8. **~70% of Overall Fills**: The London killzone accounts for 69.89% of all eventual fills, making it the PRIMARY session for Tokyo FVG retracements.

### Trading Implications

- **High Probability Setup**: Trading Tokyo FVG fills during London killzone offers 69.41% probability
- **Bearish Bias**: Slightly favor bearish FVG fills during London (71.37% vs 67.93%)
- **Quick Executions**: Average 4.4 candles = ~4 hours for London fills
- **Session Synergy**: Tokyo creates imbalances, London provides liquidity to fill them

## Trading Applications

This analysis can be used for:

1. **Mean Reversion Trading**: Enter trades expecting price to return to unfilled gaps
2. **Support/Resistance Levels**: FVG zones can act as dynamic support/resistance
3. **Market Structure Analysis**: Understanding where imbalances occur during specific sessions
4. **Risk Management**: Placing stops beyond FVG zones that are likely to be tested

## Customization

You can modify the script to:

- Change the Tokyo session hours by editing `start_hour` and `end_hour` parameters
- Filter by specific date ranges
- Analyze different timeframes (requires different input files)
- Add additional filters (e.g., minimum gap size, volume requirements)

## Script Structure

```python
main()
├── load_1h_data()           # Load and combine all CSV files
├── identify_fvg()           # Detect all FVGs in dataset
├── filter_tokyo_session()   # Filter for 19:00-23:00 hours
├── check_fvg_fill()         # Verify which FVGs were filled
├── calculate_statistics()   # Compute comprehensive metrics
├── display_results()        # Show analysis results
└── export_to_csv()          # Export to CSV file
```

## Troubleshooting

**Issue**: `ModuleNotFoundError: No module named 'pandas'`
- **Solution**: Install required packages: `pip install pandas numpy`

**Issue**: `FileNotFoundError: No 1H CSV files found`
- **Solution**: Make sure you run the script from the directory containing the 1H CSV files

**Issue**: Wrong timezone or hours
- **Solution**: The script assumes times are already in the correct timezone. If your data is in a different timezone, adjust the `start_hour` and `end_hour` parameters accordingly.

## Author

Developed by a Quant Data Scientist specializing in ICT (Inner Circle Trader) concepts and quantitative financial analysis.

## Version History

- **1.0.0** (2025-12-08): Initial release
  - FVG identification for Tokyo session
  - Fill rate analysis
  - CSV export functionality
  - Comprehensive statistics

## License

This script is provided as-is for educational and research purposes.

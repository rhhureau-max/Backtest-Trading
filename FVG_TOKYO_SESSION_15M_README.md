# FVG Tokyo Session Analysis - 15 Minute Timeframe

## Overview

This script analyzes Fair Value Gaps (FVG) that form specifically during the Tokyo session hours (19:00-23:00) on NQ (Nasdaq Futures) **15-minute data** from 2018 to present.

**Features**:
- Analyzes FVGs on 15-minute timeframe for higher granularity
- Tracks Tokyo FVGs filled during London killzone (01:00-04:00) next day
- Analyzes sessions with multiple FVGs and fill probability distributions
- Higher frequency data reveals more FVG opportunities (7,696 vs 1,716 on 1H)

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

Simply run the script from the directory containing your 15-minute CSV files:

```bash
python3 fvg_tokyo_session_15m_analysis.py
```

### Expected Data Format

The script expects CSV files with the following format:
- Filename pattern: `*15m.csv` (e.g., "2018 15m.csv", "2019 15m.csv", etc.)
- Delimiter: semicolon (;)
- Columns: Date, Time, Open, High, Low, Close, Volume
- Date format: DD/MM/YYYY
- Time format: HH:MM:SS

Example:
```
Column1;Column2;Column3;Column4;Column5;Column6;Column7
01/01/2018;17:00:00;7503.74;7516.04;7499.64;7511.94;1968
01/01/2018;17:15:00;7511.94;7515.16;7511.94;7514.28;341
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

#### 1. `fvg_tokyo_session_15m_results.csv` (Basic Analysis)

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

#### 2. `fvg_tokyo_london_killzone_15m_results.csv` (London Analysis)

All columns from above, PLUS:

| Column | Description |
|--------|-------------|
| london_filled | Whether filled during London killzone (01:00-04:00 next day) |
| london_fill_datetime | When filled during London killzone |
| london_candles_to_fill | Number of 15m candles to London fill |

## Example Results

Based on NQ 15-minute data from 2018 to 2025:

```
FVG TOKYO SESSION ANALYSIS RESULTS (19:00-23:00) - 15 MINUTE
================================================================

DATE RANGE: 2018-01-01 to 2025-11-11
Total Trading Days: 2449
Total 15-minute Candles: 184,885

GLOBAL STATISTICS
----------------------------------------------------------------
Total FVGs Created (Tokyo Session):     7696
  - Bullish FVGs:                        4152 (53.95%)
  - Bearish FVGs:                        3544 (46.05%)

Average FVGs per Session:                3.14 FVGs/day (vs 0.79 on 1H)
Average Gap Size (All):                  6.40 points (vs 11.96 on 1H)

FILL/RETRACEMENT ANALYSIS
----------------------------------------------------------------
Global Fill Rate:                        99.83%
Bullish Fill Rate:                       99.71%
Bearish Fill Rate:                       99.97%
Average Candles to Fill:                 93.42 candles (~23 hours)

LONDON KILLZONE FILL ANALYSIS
================================================================
Total Tokyo FVGs:                        7696
Filled in London Killzone:               5864 / 7696
London Killzone Fill Rate:               76.20% (vs 69.41% on 1H)

Bullish FVGs in London:                  3060 / 4152
Bullish London Fill Rate:                73.70%

Bearish FVGs in London:                  2804 / 3544
Bearish London Fill Rate:                79.12%

Average Candles to Fill (London):        16.24 candles (~4 hours)

MULTIPLE FVGs PER SESSION
================================================================
Sessions with 1 FVG:                     156 ( 7.80%)
Sessions with 2 FVGs:                    292 (14.60%)
Sessions with 3 FVGs:                    453 (22.65%)
Sessions with 4 FVGs:                    447 (22.35%)
Sessions with 5+ FVGs:                   652 (32.60%)

When 2 FVGs in same session:
  - Both filled in London:               72.26% (vs 52.82% on 1H)
  - Only 1 filled:                       18.84%
  - Neither filled:                       8.90%

When 3 FVGs in same session:
  - All 3 filled in London:              59.16% (vs 36.05% on 1H)
  - 2 filled:                            20.31%
  - Only 1 filled:                       15.45%
  - None filled:                          5.08%

When 4 FVGs in same session:
  - All 4 filled in London:              53.69%
  - 3 filled:                            17.45%
  - 2 filled:                            17.00%
  - Only 1 filled:                        8.28%
  - None filled:                          3.58%
```

## Key Findings - 15 Minute Timeframe

### Overall Fill Behavior

1. **Extremely High Fill Rate**: 99.83% of 15m FVGs are eventually filled (vs 99.30% on 1H), confirming strong mean reversion on finer timeframes.

2. **More Balanced Distribution**: 53.95% bullish vs 46.05% bearish (vs 57%/43% on 1H), indicating more balanced price action on 15m.

3. **4x More FVG Opportunities**: Average 3.14 FVGs per session (vs 0.79 on 1H), providing more trading opportunities.

4. **Smaller Gaps**: Average gap size 6.40 points (vs 11.96 on 1H), reflecting finer price movements.

5. **Bearish Nearly Perfect**: Bearish FVGs show 99.97% fill rate vs 99.71% for bullish.

### London Killzone Findings - 15 Minute

6. **76.20% London Probability**: Over 3 out of 4 Tokyo 15m FVGs are filled during London killzone (vs 69.41% on 1H). **HIGHEST probability setup identified**.

7. **Bearish Dominant in London**: Bearish FVGs have 79.12% London fill rate vs 73.70% for bullish (5.42 percentage point edge).

8. **Quick London Fills**: Average 16.24 candles (~4 hours) for London fills, showing rapid liquidity provision.

9. **London = Primary Fill Window**: 76.32% of all fills occur in London killzone.

### Trading Implications - 15 Minute Advantage

- **HIGHEST Probability Setup**: Trading Tokyo 15m FVG fills during London killzone offers **76.20%** probability (vs 69.41% on 1H)
- **Strong Bearish Bias**: Favor bearish 15m FVG fills during London (79.12% vs 73.70% for bullish)
- **Portfolio Opportunities**: With 3.14 FVGs per session on average, multiple concurrent positions are viable
- **Quick Executions**: Average 16 candles = ~4 hours for London fills
- **Multi-Setup Sessions**: 92% of sessions have 2+ FVGs, enabling diversified entry strategies
- **Session Synergy**: Tokyo creates imbalances at 15m frequency, London provides consistent liquidity

### Multiple FVGs Per Session - 15 Minute

10. **Dramatic Change in Distribution**: 
    - Only 7.80% of Tokyo sessions have 1 FVG (vs 60.83% on 1H)
    - 14.60% have 2 FVGs (vs 30.68% on 1H)
    - 22.65% have 3 FVGs (vs 7.45% on 1H)
    - 22.35% have 4 FVGs (vs 1.04% on 1H)
    - **32.60% have 5+ FVGs** (almost never on 1H)

11. **When 2 FVGs form in same session**:
    - **72.26%** probability that BOTH get filled in London (vs 52.82% on 1H)
    - 18.84% probability that only 1 gets filled
    - 8.90% probability that neither gets filled

12. **When 3 FVGs form in same session**:
    - **59.16%** probability that ALL 3 get filled in London (vs 36.05% on 1H)
    - 20.31% probability that 2 get filled
    - 15.45% probability that only 1 gets filled
    - 5.08% probability that none get filled

13. **When 4 FVGs form in same session**:
    - **53.69%** probability that ALL 4 get filled in London
    - 17.45% probability that 3 get filled
    - Only 3.58% probability that none get filled

**Key Insight**: On 15-minute timeframe, multiple FVGs per session is the NORM (92% of sessions), and the probability of most/all filling in London is dramatically higher than on 1H. This creates exceptional portfolio opportunity with 72% probability for double fills and 59% for triple fills.

## Trading Applications - 15 Minute Advantages

This analysis can be used for:

1. **High-Frequency Mean Reversion**: 15m FVGs provide 4x more trading opportunities than 1H
2. **Precision Entry/Exit**: Tighter gaps (6.40 pts avg) allow for more precise stop placement
3. **Portfolio Diversification**: Multiple FVGs per session enable risk distribution across uncorrelated setups
4. **Scalping Strategies**: Smaller gaps with 99.83% fill rate ideal for quick scalps
5. **London Session Trading**: 76.20% probability makes this a premier London open strategy
6. **Support/Resistance Levels**: More granular FVG zones for tighter technical analysis

## Customization

You can modify the script to:

- Change the Tokyo session hours by editing `start_hour` and `end_hour` parameters
- Filter by specific date ranges
- Analyze different timeframes (requires different input files)
- Add additional filters (e.g., minimum gap size, volume requirements)

## Script Structure

```python
main()
├── load_15m_data()                     # Load and combine all 15m CSV files
├── identify_fvg()                      # Detect all FVGs in dataset
├── filter_tokyo_session()              # Filter for 19:00-23:00 hours
├── check_fvg_fill()                    # Verify which FVGs were filled
├── calculate_statistics()              # Compute comprehensive metrics
├── display_results()                   # Show analysis results
├── export_to_csv()                     # Export to CSV file
├── check_london_killzone_fill()        # Check London fills (01:00-04:00 next day)
├── calculate_london_statistics()       # Compute London-specific metrics
├── display_london_results()            # Show London analysis
├── export_london_csv()                 # Export London results
├── analyze_multiple_fvgs_per_session() # Analyze multi-FVG sessions
└── display_multiple_fvgs_analysis()    # Show multi-FVG distribution
```

## Troubleshooting

**Issue**: `ModuleNotFoundError: No module named 'pandas'`
- **Solution**: Install required packages: `pip install pandas numpy`

**Issue**: `FileNotFoundError: No 15m CSV files found`
- **Solution**: Make sure you run the script from the directory containing the 15-minute CSV files (pattern: *15m.csv)

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

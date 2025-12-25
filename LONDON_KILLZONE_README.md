# London Killzone Analysis - Judas Swing vs Continuation

## Overview

This Python script analyzes the "London Killzone" (01:00-05:00) trading behavior to determine probabilities of "Judas Swing" (false breakout) vs "Continuation" (true breakout) patterns in NQ (Nasdaq 100) futures data.

## Key Findings (2018-2025 Analysis)

### Overall Results
- **Total Breakouts Analyzed**: 1,861 trading days
- **Judas Swings**: 82.2% (1,529 occurrences)
- **Continuations**: 15.7% (292 occurrences)
- **Unclear**: 2.1% (40 occurrences)

### Critical Insights

1. **High Probability of Reversal**: Over 82% of Asian Range breakouts during the London session result in Judas Swings (false breakouts)

2. **Reversal Timing**:
   - **40.3%** of reversals occur at **01:00** (the first hour)
   - **17.0%** at 01:30
   - **21.2%** at 02:00
   - Most reversals (78.5%) happen within the first 2 hours of London open

3. **Extension Statistics**:
   - **Judas Swing**: Average 20.57 points (±23.86 SD)
   - **Continuation**: Average 58.67 points (±40.83 SD)
   - Continuations move significantly further (almost 3x) before establishing direction

4. **Directional Bias**:
   - High breakouts: 55.1% (slightly more frequent)
   - Low breakouts: 44.9%
   - Both directions show similar Judas Swing rates (~81-83%)

## Methodology

### Asian Range Definition
- **Start**: 19:00 (previous day)
- **End**: 00:00 (midnight)
- Records the High and Low during this period

### London Killzone Window
- **Start**: 01:00
- **End**: 05:00

### Classification Logic

**Judas Swing (Fakeout)**:
- Price breaks Asian High/Low
- Price touches the Asian equilibrium (midpoint of Tokyo session range) within 60 minutes
- Asian equilibrium = (asian_high + asian_low) / 2

**Continuation (Breakout)**:
- Price breaks Asian High/Low
- Continues moving away by at least 20 points
- Does NOT touch the Asian equilibrium within 60 minutes

## Requirements

```bash
pip install pandas numpy matplotlib seaborn
```

## Usage

```bash
python3 london_killzone_analysis.py
```

## Input Data

The script processes 5-minute NQ data files in the format:
```
YYYY 5m.csv
```

Expected columns (semicolon-delimited):
- Column1: Date (DD/MM/YYYY)
- Column2: Time (HH:MM:SS)
- Column3: Open
- Column4: High
- Column5: Low
- Column6: Close
- Column7: Volume

## Output Files

1. **london_killzone_results.csv**
   - Detailed results for each trading day
   - Includes: date, Asian range, breakout details, pattern type, extension, reversal time

2. **london_killzone_summary.csv**
   - Yearly summary statistics
   - Percentages of Judas Swings vs Continuations by year

3. **london_killzone_analysis.png**
   - 6-panel visualization dashboard including:
     - Pattern distribution by year
     - Overall pattern pie chart
     - Reversal time distribution
     - Extension distribution histogram
     - Pattern by breakout direction
     - Monthly pattern distribution

## Configuration

You can modify these constants in the script:

```python
TIMEFRAME = '5m'              # Data timeframe
ASIAN_START = time(19, 0, 0)  # Asian session start
ASIAN_END = time(0, 0, 0)     # Asian session end
LONDON_START = time(1, 0, 0)  # London session start
LONDON_END = time(5, 0, 0)    # London session end
CONTINUATION_THRESHOLD = 20   # Points for valid continuation
REVERSAL_WINDOW = 60          # Minutes to check for reversal
```

## Trading Implications

1. **Fade the First Break**: With 82% probability, the first break of Asian range during London open is likely to reverse

2. **Optimal Entry Timing**: Wait for the reversal (most occur by 02:00)

3. **Risk Management**: 
   - Judas Swings extend an average of 20.57 points beyond the range
   - Plan stops accordingly (suggest 25-30 points beyond Asian extreme)

4. **Continuation Recognition**:
   - If price moves 20+ points without reversal within 60 minutes
   - More likely to be a true breakout (15.7% of cases)

## Limitations

- Analysis based on historical data (2018-2025)
- Past performance doesn't guarantee future results
- Market conditions and volatility can change patterns
- Consider additional factors (news, volatility, market sentiment)

## Author

Quantitative Trading Analysis
Date: 2025-12-25

## License

This script is provided for educational and research purposes.

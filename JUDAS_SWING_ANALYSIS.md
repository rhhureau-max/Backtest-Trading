# Judas Swing Analysis - NQ Futures (2018-2025)

## Overview

This analysis performs a comprehensive statistical study of Judas Swing patterns in Nasdaq Futures (NQ) across Tokyo and London trading sessions from 2018 to present. The study is purely statistical with **no trading logic applied**.

## Definitions

### Trading Sessions

**Tokyo Session**
- Hours: 19:00 to 00:00 (midnight)
- Defines: Tokyo High, Tokyo Low, Tokyo Range
- Tokyo Range = Tokyo High - Tokyo Low

**London Session**
- Hours: 01:00 to 05:00
- Period where Judas Swings are detected

### Judas Swing

A Judas Swing represents a manipulation of Tokyo session liquidity during the London session, characterized by:

1. **Bullish Manipulation**: Break above Tokyo High during London session
2. **Bearish Manipulation**: Break below Tokyo Low during London session

The amplitude is measured as:
- **Bullish**: Distance from Tokyo High to the highest point reached during manipulation
- **Bearish**: Distance from Tokyo Low to the lowest point reached during manipulation

## Technical Details

### Data Source
- Instrument: NQ (Nasdaq Futures)
- Timeframe: 15-minute bars
- Period: 2018-01-01 to 2025-11-11
- No timezone conversions applied (timestamps used as-is)

### Analysis Method

1. For each trading day:
   - Calculate Tokyo session High/Low/Range (previous day 19:00 to current day 00:00)
   - Identify London session activity (01:00 to 05:00)
   - Detect breaks of Tokyo High or Low
   - Measure manipulation amplitude

2. When both Tokyo High and Low are broken on the same day:
   - The manipulation with the larger amplitude is selected

## Results Summary

### Global Statistics
- **Total Trading Days Analyzed**: 2,449
- **Judas Swings Detected**: 1,867 (76.24% of days)
  - Bullish Manipulations: 1,023 (54.77%)
  - Bearish Manipulations: 844 (45.23%)

### Amplitude Statistics (All Swings)
| Metric | Value (NQ Points) |
|--------|------------------|
| Mean | 47.07 |
| Median | 33.40 |
| Minimum | 0.29 |
| Maximum | 667.29 |
| Standard Deviation | 48.32 |

### Directional Comparison

**Bullish Manipulations (Tokyo High Breaks)**
| Metric | Value (NQ Points) |
|--------|------------------|
| Count | 1,023 |
| Mean | 43.10 |
| Median | 31.79 |
| Minimum | 0.29 |
| Maximum | 391.21 |
| Std Dev | 42.19 |

**Bearish Manipulations (Tokyo Low Breaks)**
| Metric | Value (NQ Points) |
|--------|------------------|
| Count | 844 |
| Mean | 51.88 |
| Median | 36.35 |
| Minimum | 0.50 |
| Maximum | 667.29 |
| Std Dev | 54.49 |

**Key Observation**: Bearish manipulations tend to have larger amplitudes on average (51.88 vs 43.10 points).

### Amplitude Distribution

| Range (Points) | Count | Percentage |
|---------------|-------|------------|
| 0-5 | 100 | 5.36% |
| 5-10 | 153 | 8.19% |
| 10-15 | 162 | 8.68% |
| 15-20 | 159 | 8.52% |
| 20-25 | 135 | 7.23% |
| 25-30 | 128 | 6.86% |
| 30-50 | 412 | 22.07% |
| 50-100 | 426 | 22.82% |
| 100+ | 192 | 10.28% |

**Key Insights**:
- Most common range: 30-50 points (22.07%) and 50-100 points (22.82%)
- Combined: 44.89% of all swings fall between 30-100 points
- Large manipulations (100+ points): 10.28% of cases

### Probability Analysis

| Threshold | Probability |
|-----------|-------------|
| Exceeds 5 points | 94.64% |
| Exceeds 10 points | 86.45% |
| Exceeds 15 points | 77.77% |
| Exceeds 20 points | 69.26% |

**Key Finding**: There is a very high probability (94.64%) that a detected Judas Swing will exceed 5 points, and nearly 7 in 10 swings (69.26%) exceed 20 points.

## Usage

### Running the Analysis

```bash
python3 judas_swing_analysis.py
```

### Output Files

1. **Console Output**: Comprehensive statistical report
2. **judas_swing_results.csv**: Detailed record of each detected Judas Swing with columns:
   - `date`: Trading date
   - `direction`: 'bullish' or 'bearish'
   - `tokyo_high`: Tokyo session high
   - `tokyo_low`: Tokyo session low
   - `tokyo_range`: Tokyo session range
   - `manipulation_high`: Highest point during bullish manipulation (or empty)
   - `manipulation_low`: Lowest point during bearish manipulation (or empty)
   - `amplitude`: Manipulation amplitude in NQ points

### Dependencies

```bash
pip install pandas numpy
```

## Interpretation for Traders

### Session-Based Trading (ICT/SMT Concepts)

1. **High Occurrence Rate**: Judas Swings occur on 76.24% of trading days, making them a frequent phenomenon in NQ futures.

2. **Typical Amplitude**: The median amplitude is 33.40 points, with the mean at 47.07 points. This suggests that while typical manipulations are around 30-35 points, there are occasions with significantly larger moves that pull the average higher.

3. **Directional Bias**: Bullish manipulations are slightly more frequent (54.77% vs 45.23%) but bearish manipulations tend to be more aggressive (51.88 mean vs 43.10 mean).

4. **Risk Considerations**: 
   - 10.28% of manipulations exceed 100 points
   - Maximum recorded manipulation: 667.29 points (bearish)
   - This highlights the importance of risk management in trading these patterns

5. **Consistency**: With 86.45% probability of exceeding 10 points and 77.77% probability of exceeding 15 points, Judas Swings show consistent movement characteristics.

## Important Notes

⚠️ **This is statistical analysis only**
- No trading logic or strategy is implied
- No risk management rules are included
- Past performance does not guarantee future results
- This data should not be used as sole basis for trading decisions

## Files

- `judas_swing_analysis.py` - Main analysis script
- `judas_swing_results.csv` - Detailed results for each detected swing
- `JUDAS_SWING_ANALYSIS.md` - This documentation file

## Data Files Used

- 2018 15m.csv through 2025 15m.csv (NQ futures 15-minute data)

## Methodology Compliance

✓ No timezone conversions applied  
✓ Using exact timestamps from source files  
✓ Instrument: NQ (Nasdaq Futures)  
✓ Timeframe: 15-minute bars as provided  
✓ Data: Exclusively from provided CSV files  
✓ Sessions: Tokyo (19:00-00:00), London (01:00-05:00)  
✓ No trading logic or filters applied  
✓ Pure statistical analysis  

## Contact

For questions or issues regarding this analysis, please refer to the repository documentation.

---

*Analysis generated on 2025-12-23*  
*Data period: 2018-01-01 to 2025-11-11*  
*Total records analyzed: 184,877 bars*

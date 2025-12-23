# Post-Judas Swing Reversion & Reversal Analysis

## Overview

This analysis extends the original Judas Swing study to examine **price behavior AFTER the manipulation** occurs. It measures the probability and time required for price to return to key Tokyo session levels.

## Definitions

### Key Levels

1. **Tokyo Equilibrium (Eq)**: `(Tokyo High + Tokyo Low) / 2`
   - The midpoint of the Tokyo session range
   - Represents a balanced reversion target

2. **Opposing Liquidity**: 
   - For **Bullish Judas Swings** (Tokyo High break): Target is **Tokyo Low**
   - For **Bearish Judas Swings** (Tokyo Low break): Target is **Tokyo High**
   - Represents a full reversal across the Tokyo range

### Search Window

- **Start**: Timestamp of manipulation extreme (peak for bullish, valley for bearish)
- **End**: 23:00 on the same trading day
- Analysis tracks if/when price reaches target levels within this window

## Methodology

For each of the 1,867 detected Judas Swings:

1. **Identify Manipulation Extreme Time**
   - Find exact timestamp when manipulation high/low occurred during London session (01:00-05:00)

2. **Track Reversion to Equilibrium**
   - For bullish: Check if price drops back down to Tokyo Eq
   - For bearish: Check if price rallies back up to Tokyo Eq
   - Record hit/miss and duration in minutes

3. **Track Full Reversal**
   - For bullish: Check if price reaches Tokyo Low (opposing liquidity)
   - For bearish: Check if price reaches Tokyo High (opposing liquidity)
   - Record hit/miss and duration in minutes

## Key Results

### 1. Reversion to Tokyo Equilibrium (50%)

**Overall Performance:**
- **Hit Rate**: 78.52% (1,466 out of 1,867 swings)
- **Mean Duration**: 218.10 minutes (3.64 hours)
- **Median Duration**: 195.00 minutes (3.25 hours)
- **Range**: 15 minutes to 21.5 hours
- **Standard Deviation**: 171.01 minutes

**Interpretation**: After a Judas Swing manipulation, price returns to the Tokyo session midpoint nearly **4 out of 5 times**, typically within 3-4 hours.

### 2. Full Reversal to Opposing Liquidity

**Overall Performance:**
- **Hit Rate**: 65.35% (1,220 out of 1,867 swings)
- **Mean Duration**: 330.66 minutes (5.51 hours)
- **Median Duration**: 300.00 minutes (5.00 hours)
- **Range**: 15 minutes to 19 hours
- **Standard Deviation**: 176.77 minutes

**Interpretation**: Price completes a full reversal across the entire Tokyo range in **2 out of 3 cases**, typically within 5-6 hours.

### 3. Directional Comparison

#### Bullish Manipulations (Tokyo High Breaks)
| Metric | Equilibrium Reversion | Full Reversal (to Tokyo Low) |
|--------|----------------------|-------------------------------|
| Hit Rate | 77.22% | 63.54% |
| Mean Duration | 222.99 min (3.72 hrs) | 333.78 min (5.56 hrs) |
| Median Duration | 210.00 min (3.50 hrs) | 315.00 min (5.25 hrs) |

#### Bearish Manipulations (Tokyo Low Breaks)
| Metric | Equilibrium Reversion | Full Reversal (to Tokyo High) |
|--------|----------------------|-------------------------------|
| Hit Rate | 80.09% | 67.54% |
| Mean Duration | 212.40 min (3.54 hrs) | 327.11 min (5.45 hrs) |
| Median Duration | 180.00 min (3.00 hrs) | 300.00 min (5.00 hrs) |

**Key Observation**: Bearish manipulations show slightly higher reversion rates (80.09% vs 77.22%) and slightly faster reversion times, particularly for equilibrium targets.

## Statistical Insights

### Reversion Probability Profile

| Target Level | Probability | Typical Timeframe |
|--------------|-------------|-------------------|
| Tokyo Equilibrium | 78.52% | 3-4 hours |
| Opposing Liquidity | 65.35% | 5-6 hours |

### Time Distribution Patterns

**Equilibrium Reversion:**
- **Quick Returns** (< 3 hours): ~40-45% of hits
- **Standard Returns** (3-6 hours): ~40-45% of hits
- **Delayed Returns** (> 6 hours): ~10-15% of hits

**Full Reversals:**
- **Fast Reversals** (< 4 hours): ~30-35% of hits
- **Standard Reversals** (4-8 hours): ~50-55% of hits
- **Slow Reversals** (> 8 hours): ~15-20% of hits

## Practical Implications (Statistical Context)

### For Session-Based Analysis:

1. **High Reversion Probability**: After a Judas Swing, expecting price to return to at least the Tokyo midpoint has strong statistical backing (78.52%).

2. **Timing Considerations**: The median reversion time of 3.25 hours suggests most reversions occur within the same trading session (considering manipulation typically peaks during London session 01:00-05:00).

3. **Full Reversal Frequency**: Nearly 2 out of 3 Judas Swings see price travel all the way back across the Tokyo range to the opposing side.

4. **Directional Symmetry**: Both bullish and bearish manipulations show similar reversion characteristics, with bearish swings showing marginally better reversion statistics.

### Session Timeline Context:

- **Manipulation Extreme**: Typically during London (01:00-05:00)
- **Equilibrium Reversion**: Often by 08:00-09:00 (3-4 hours later)
- **Full Reversal**: Frequently by 10:00-12:00 (5-6 hours later)
- **Search Window Ends**: 23:00 (allowing full trading day observation)

## Data Quality

- **Total Swings Analyzed**: 1,867
- **Coverage**: 100% of detected Judas Swings from original analysis
- **Period**: 2018-01-01 to 2025-11-11
- **Timeframe**: 15-minute bars
- **Missing Data**: Minimal (extreme time found for 1,867 of 1,867 swings)

## Files Generated

1. **judas_swing_reversion_analysis.py** - Analysis script
2. **judas_swing_reversion_results.csv** - Detailed results (1,867 records) with:
   - Date, direction, amplitude
   - Extreme time, Tokyo Eq, Opposing Liquidity levels
   - Equilibrium hit/miss and duration
   - Opposing Liquidity hit/miss and duration

## Usage

```bash
# Run the reversion analysis
python3 judas_swing_reversion_analysis.py
```

**Prerequisites**: Must have already run `judas_swing_analysis.py` to generate `judas_swing_results.csv`

## Important Notes

⚠️ **This is statistical analysis only**
- No trading logic or strategy implied
- No risk management rules included
- Past behavior does not guarantee future performance
- Data should be considered as part of broader market analysis

✓ **Methodology Compliance**
- Uses exact timestamps (no timezone conversion)
- Tracks real price movement to specified levels
- Search window clearly defined (manipulation extreme to 23:00)
- Both directional cases analyzed separately

---

*Analysis Date: 2025-12-23*  
*Data Period: 2018-01-01 to 2025-11-11*  
*Swings Analyzed: 1,867*

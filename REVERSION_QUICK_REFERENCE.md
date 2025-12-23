# Post-Judas Swing Reversion Analysis - Quick Summary

## Overview
Analysis of price behavior AFTER Judas Swing manipulations in NQ Futures (2018-2025).

## Key Statistics

### Reversion to Tokyo Equilibrium (50% Level)
- **Hit Rate**: 78.52% (1,466/1,867 swings)
- **Mean Time**: 3.64 hours (218.10 minutes)
- **Median Time**: 3.25 hours (195.00 minutes)
- **Range**: 15 minutes to 21.5 hours

### Full Reversal to Opposing Liquidity
- **Hit Rate**: 65.35% (1,220/1,867 swings)
- **Mean Time**: 5.51 hours (330.66 minutes)
- **Median Time**: 5.00 hours (300.00 minutes)
- **Range**: 15 minutes to 19.0 hours

## Directional Breakdown

### Bullish Manipulations (Tokyo High Breaks)
| Target | Hit Rate | Mean Duration | Median Duration |
|--------|----------|---------------|-----------------|
| Tokyo Equilibrium | 77.22% | 3.72 hours | 3.50 hours |
| Tokyo Low (Opposing) | 63.54% | 5.56 hours | 5.25 hours |

### Bearish Manipulations (Tokyo Low Breaks)
| Target | Hit Rate | Mean Duration | Median Duration |
|--------|----------|---------------|-----------------|
| Tokyo Equilibrium | 80.09% | 3.54 hours | 3.00 hours |
| Tokyo High (Opposing) | 67.54% | 5.45 hours | 5.00 hours |

## Key Insights

1. **High Reversion Probability**: Nearly 4 out of 5 manipulations revert to Tokyo Eq
2. **Consistent Timing**: Most reversions occur within 3-4 hours
3. **Full Reversals Common**: 2 out of 3 swings complete full range reversal
4. **Directional Symmetry**: Similar behavior for both bullish and bearish swings
5. **Bearish Advantage**: Slightly higher hit rates and faster times for bearish reversions

## Time Distribution

**Equilibrium Reversion:**
- Fast (< 3h): ~40-45% of hits
- Standard (3-6h): ~40-45% of hits
- Delayed (> 6h): ~10-15% of hits

**Full Reversal:**
- Fast (< 4h): ~30-35% of hits
- Standard (4-8h): ~50-55% of hits
- Slow (> 8h): ~15-20% of hits

## Session Timeline (Typical Pattern)

1. **01:00-05:00**: Manipulation occurs (London session)
2. **03:00-04:00**: Peak/valley of manipulation (typical)
3. **06:00-09:00**: Reversion to Equilibrium begins (3-4h later)
4. **08:00-12:00**: Full reversal often completes (5-6h later)
5. **23:00**: End of observation window

## Probability Summary

| Scenario | Probability |
|----------|-------------|
| Reversion to 50% within same day | 78.52% |
| Full reversal within same day | 65.35% |
| Reversion within 4 hours | ~60% |
| Full reversal within 6 hours | ~55% |

## Data Quality
- **Swings Analyzed**: 1,867
- **Period**: 2018-2025
- **Coverage**: 100% of detected Judas Swings
- **Timeframe**: 15-minute bars

## Files
- `judas_swing_reversion_analysis.py` - Analysis script
- `judas_swing_reversion_results.csv` - Detailed data (1,867 records)
- `REVERSION_ANALYSIS.md` - Full documentation

---
*Statistical analysis only - no trading recommendations*

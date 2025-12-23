# Quick Reference: Judas Swing Analysis Results

## Executive Summary

**Analysis Period**: 2018-01-01 to 2025-11-11  
**Total Days Analyzed**: 2,449  
**Judas Swings Detected**: 1,867 (76.24%)

## Core Statistics

### Amplitude (NQ Points)
- **Mean**: 47.07
- **Median**: 33.40
- **Range**: 0.29 to 667.29

### Direction Split
- **Bullish** (Tokyo High breaks): 1,023 (54.77%) - Avg: 43.10 pts
- **Bearish** (Tokyo Low breaks): 844 (45.23%) - Avg: 51.88 pts

## Key Probabilities

| Threshold | Probability |
|-----------|-------------|
| > 5 points | 94.64% |
| > 10 points | 86.45% |
| > 15 points | 77.77% |
| > 20 points | 69.26% |

## Percentile Reference

| Percentile | All Swings | Bullish | Bearish |
|------------|------------|---------|---------|
| 25th | 16.56 | 15.79 | 17.88 |
| 50th | 33.40 | 31.79 | 36.35 |
| 75th | 60.85 | 56.50 | 68.23 |
| 90th | 100.81 | 90.20 | 115.45 |
| 95th | 130.65 | 113.04 | 149.39 |

## Year-by-Year Highlights

| Year | Swings | Avg Amplitude | Max Amplitude |
|------|--------|---------------|---------------|
| 2018 | 228 | 24.99 | 127.53 |
| 2019 | 232 | 22.02 | 173.38 |
| 2020 | 225 | 57.92 | 381.64 |
| 2021 | 239 | 46.89 | 296.11 |
| 2022 | 247 | 69.13 | 424.55 |
| 2023 | 249 | 42.77 | 177.30 |
| 2024 | 243 | 50.05 | 444.91 |
| 2025 | 204 | 63.46 | 667.29 |

**Note**: 2020 and 2022 showed higher volatility with larger average amplitudes.

## Seasonal Patterns (Monthly Averages)

**Highest Amplitude Months**:
1. March: 59.10 points
2. February: 53.87 points
3. September: 50.59 points

**Lowest Amplitude Months**:
1. December: 37.62 points
2. July: 38.20 points
3. November: 39.93 points

## Tokyo Range Correlation

**Correlation coefficient**: 0.3989 (moderate positive correlation)

Larger Tokyo ranges tend to produce larger manipulation amplitudes:
- Tokyo Range 10-20 pts → Avg manipulation: 18.98 pts
- Tokyo Range 50-100 pts → Avg manipulation: 50.21 pts
- Tokyo Range 100+ pts → Avg manipulation: 81.88 pts

## Most Common Amplitude Ranges

1. **50-100 points**: 22.82% of all swings
2. **30-50 points**: 22.07% of all swings
3. **100+ points**: 10.28% of all swings

Combined: 55.17% of swings are 30+ points

## Files Generated

1. `judas_swing_analysis.py` - Main analysis script
2. `judas_swing_extended_analysis.py` - Additional insights
3. `judas_swing_results.csv` - Detailed data (1,867 records)
4. `JUDAS_SWING_ANALYSIS.md` - Full documentation
5. `QUICK_REFERENCE.md` - This file

## Running the Analysis

```bash
# Main analysis
python3 judas_swing_analysis.py

# Extended analysis (requires main analysis to run first)
python3 judas_swing_extended_analysis.py
```

---

*For complete methodology and detailed results, see JUDAS_SWING_ANALYSIS.md*

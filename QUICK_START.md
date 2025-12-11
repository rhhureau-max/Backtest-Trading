# Quick Start Guide - NQ Session Analysis

## What This Analysis Does

Analyzes **NQ (Nasdaq-100) futures price action and volatility** during the **01:00-07:00 time window** using 7+ years of historical data (2018-2025).

## Installation

```bash
# Install required Python packages
pip install -r requirements.txt
```

## Running the Analysis

```bash
# Execute the analysis script
python3 nq_session_analysis_01_07.py
```

**Execution time:** ~30-60 seconds  
**Data processed:** 554,518 5-minute candles  
**Sessions analyzed:** 2,032 sessions

## Output Files

The script generates:

1. **Console Report** - Complete statistical analysis with tables
2. **nq_session_range_analysis.png** - Range distribution charts (4 subplots)
3. **nq_session_timing_analysis.png** - High/Low timing histograms

## Key Results at a Glance

| Metric | Value | Implication |
|--------|-------|-------------|
| **Bullish Bias** | 53.94% | Slight preference for long setups |
| **Average Range** | 100.99 points | Use for stop-loss sizing |
| **Open Drive Win Rate** | 59.83% | Trade with 01:00 candle direction |
| **Best Day** | Wednesday | 55.91% bullish, +5.12 avg return |
| **Worst Day** | Friday | Negative average return (-3.56) |
| **Most Common HIGH** | 01:00 | Opening candle sets extremes |
| **Most Common LOW** | 01:00 | Monitor early for reversals |

## Trading Strategy (Based on Analysis)

### Step-by-Step Approach

1. **Wait for 01:00 candle to close**
   - Observe if it's bullish or bearish
   - Confirm market structure

2. **Trade in the direction of 01:00 candle**
   - Bullish 01:00 → Look for long setups
   - Bearish 01:00 → Look for short setups (mind the bullish bias)
   - Expected win rate: **59.83%**

3. **Day Selection**
   - ✅ **Best:** Wednesday and Thursday
   - ⚠️ **Avoid:** Friday

4. **Risk Management**
   - Stop-loss: ~100 points (baseline)
   - Adjust for 2025 volatility: ~145 points
   - Take profit: Based on average range

5. **Key Times to Watch**
   - **01:00** - Critical opening candle
   - **06:30-06:45** - Late session moves

## Documentation

- **English (Technical):** [README_NQ_SESSION_ANALYSIS.md](README_NQ_SESSION_ANALYSIS.md)
- **French (Executive):** [RESUME_ANALYSE_NQ_01_07_FR.md](RESUME_ANALYSE_NQ_01_07_FR.md)

## Data Requirements

The script expects NQ CSV files in this format:

```
Year 5m.csv (e.g., "2024 5m.csv")
```

File format:
```
Column1;Column2;Column3;Column4;Column5;Column6;Column7
01/01/2024;17:00:00;18244.57923;18248.331274;18238.951165;18241.631196;1308
```

Where:
- Column1 = Date (DD/MM/YYYY)
- Column2 = Time (HH:MM:SS)
- Column3 = Open
- Column4 = High
- Column5 = Low
- Column6 = Close
- Column7 = Volume

## Customization

To analyze different time windows, edit these lines in `nq_session_analysis_01_07.py`:

```python
SESSION_START = time(1, 0)  # 01:00 - Change as needed
SESSION_END = time(7, 0)    # 07:00 - Change as needed
```

## Statistical Confidence

- **Sample size:** 2,032 sessions (robust)
- **Time period:** 2018-2025 (7+ years)
- **Data points:** 554,518 5-minute candles
- **Edge:** 59.83% win rate (9.83% above random)

## Support

For issues or questions, refer to the detailed documentation:
- Technical details: README_NQ_SESSION_ANALYSIS.md
- Trading implications: RESUME_ANALYSE_NQ_01_07_FR.md

---

**Author:** Quantitative Analyst Senior  
**Date:** December 11, 2025  
**Version:** 1.0

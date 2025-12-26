# NQ Futures Backtesting - Paris Timezone Version

## Quick Start

### Run the Paris Timezone Analysis
```bash
python3 nq_london_session_backtest_paris.py
```

This will analyze the NQ futures data with all times displayed in **Paris time (CET/CEST)**.

## What's Different?

The Paris version (`nq_london_session_backtest_paris.py`) is functionally identical to the original JST version, but with all times converted to Paris timezone:

### Time Conversions (JST → Paris)

| What | JST Time | Paris Time |
|------|----------|------------|
| Asian Session | 08:00-15:00 | 00:00-07:00 |
| NY Midnight | 13:00-14:00 | 05:00-06:00 |
| SMT Window | 14:00-16:00 | 06:00-08:00 |
| Judas Window | 15:30-17:00 | 07:30-09:00 |
| London Session | 16:00-21:00 | **08:00-13:00** ⭐ |

**Note:** The London session time in Paris (08:00-13:00) perfectly aligns with actual London market hours!

## Files

1. **`nq_london_session_backtest_paris.py`** - Main analysis script (Paris timezone)
2. **`nq_analysis_results_paris.txt`** - Results output (generated when you run the script)
3. **`PARIS_VERSION_CHANGES.md`** - Detailed changelog and technical documentation

## Trading Methods Analyzed

All 4 methods from the original script:
1. ✅ Judas Swing Post-Asia (Contrarian)
2. ✅ NY Midnight Opening Rule (Trend Follow)
3. ✅ H4 Market Structure (Top-Down)
4. ✅ SMT Divergence (Advanced)

Plus correlation analyses:
- D1/London Session Correlation
- Asian Range Sweep Analysis
- Volume & Volatility by Hour
- H4 Continuation Strategy

## Daily Trading Schedule (Paris Time)

```
00:00-07:00  →  Asian Session (mark range)
05:00-06:00  →  NY Midnight (mark opening level)
06:00-08:00  →  Pre-London / SMT Window
07:30-09:00  →  Judas Swing Window
08:00-13:00  →  London Session Trading ⭐
```

## Requirements

Same as the original script:
```bash
pip install -r requirements_backtest.txt
```

Dependencies:
- pandas >= 2.0.0
- numpy >= 1.24.0
- pytz >= 2024.1

## Timezone Details

- **Source Data:** Chicago Time (CST/CDT)
- **Output Times:** Paris Time (CET/CEST)
- **DST Handling:** Automatic via pytz
- **Winter:** CET = UTC+1
- **Summer:** CEST = UTC+2

## Comparison with JST Version

| Feature | JST Version | Paris Version |
|---------|-------------|---------------|
| Script | `nq_london_session_backtest.py` | `nq_london_session_backtest_paris.py` |
| Results | `nq_analysis_results.txt` | `nq_analysis_results_paris.txt` |
| Timezone | Asia/Tokyo (UTC+9) | Europe/Paris (UTC+1/+2) |
| Lines of Code | 1,070 | 1,070 |

Both versions are functionally equivalent - choose based on your preferred timezone!

## Output

The script generates comprehensive analysis including:
- Success rates for each trading method
- Statistical correlations
- Daily action plan template
- Volume and volatility analysis
- Best performing method identification

Example output:
```
Method 3: H4 Market Structure
Success Rate: 85.5%
```

## Support

For detailed technical documentation, see: `PARIS_VERSION_CHANGES.md`

---

**Created:** 2025-12-26  
**Purpose:** Provide Paris timezone version of NQ futures backtesting analysis

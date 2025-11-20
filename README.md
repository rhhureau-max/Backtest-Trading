# Backtest-Trading

This repository contains historical trading data and tools for analyzing Fair Value Gaps (FVGs).

## Fair Value Gap Analysis

### Quick Start - FVGs at 8:30:00

To see all FVGs at 8:30:00 in a simple table format:
```bash
python3 list_fvg_at_830.py
```

For 2025 FVGs only (at 8:30):
```bash
python3 list_fvg_2025.py
```

For chronology of 1-minute FVGs in 2025 (at 8:30):
```bash
python3 chronologie_fvg_1m_2025.py
```

For chronology of 15-minute FVGs in 2025 (at 8:30):
```bash
python3 chronologie_fvg_15m_2025.py
```

For detailed FVG information including OHLC data for all three candles:
```bash
python3 detect_fvg_at_830.py
```

### Quick Start - FVG Quality Analysis

To analyze the quality of FVGs at 8:30:00 (good vs bad):
```bash
python3 analyse_qualite_fvg_2025.py
```

A "good" FVG is when price doesn't revisit the gap zone within 5 candles.
A "bad" FVG is when price revisits the gap zone within 5 candles.

See [QUALITE_FVG_2025.md](QUALITE_FVG_2025.md) for detailed results and analysis.

### Quick Start - ALL FVGs in 2025

To see **all** FVGs (not just at 8:30) for the year 2025:

For 1-minute timeframe:
```bash
python3 list_all_fvg_1m_2025.py
```

For 15-minute timeframe:
```bash
python3 list_all_fvg_15m_2025.py
```

To save complete lists to files:
```bash
python3 list_all_fvg_1m_2025.py > fvg_1m_2025_complet.txt
python3 list_all_fvg_15m_2025.py > fvg_15m_2025_complet.txt
```

### Results Summary

**FVGs at 8:30:00:**
- **1,908 Fair Value Gaps** at exactly 8:30:00 (as middle candle) across all years (2018-2025)
- See [FVG_830_SUMMARY.md](FVG_830_SUMMARY.md) for a complete breakdown by year and timeframe

**FVG Quality Analysis (2025):**
- **190 FVGs at 8:30:00** analyzed for quality in 2025 (1m and 15m)
  - Good FVGs (price doesn't revisit): 81 (42.6%)
  - Bad FVGs (price revisits): 109 (57.4%)
- See [QUALITE_FVG_2025.md](QUALITE_FVG_2025.md) for detailed analysis

**ALL FVGs in 2025:**
- **72,978 Fair Value Gaps** total in 2025 (1m and 15m timeframes combined)
  - 1 minute: 68,894 FVGs (51.8% Bullish, 48.2% Bearish)
  - 15 minutes: 4,084 FVGs (55.8% Bullish, 44.2% Bearish)
- See [TOUS_FVG_2025_SUMMARY.md](TOUS_FVG_2025_SUMMARY.md) for detailed statistics

### What is a Fair Value Gap (FVG)?

A Fair Value Gap is a trading pattern where there's a gap in price action:
- **Bullish FVG**: Current candle's low > Previous candle's high (2 periods back)
- **Bearish FVG**: Current candle's high < Previous candle's low (2 periods back)

### Data Files

The repository contains historical OHLC (Open, High, Low, Close) data in CSV format:
- Years: 2018-2025
- Timeframes: 1 minute (1m), 5 minutes (5m), 15 minutes (15m), 1 hour (1H), 4 hours (4H), 1 day (1D)
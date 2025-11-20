# Backtest-Trading

This repository contains historical trading data and tools for analyzing Fair Value Gaps (FVGs).

## Fair Value Gap Analysis at 8:30:00

### Quick Start

To see all FVGs at 8:30:00 in a simple table format:
```bash
python3 list_fvg_at_830.py
```

For detailed FVG information including OHLC data for all three candles:
```bash
python3 detect_fvg_at_830.py
```

### Results Summary

**401 Fair Value Gaps** have been identified at exactly 8:30:00 across all years (2018-2025).

See [FVG_830_SUMMARY.md](FVG_830_SUMMARY.md) for a complete breakdown by year and timeframe.

### What is a Fair Value Gap (FVG)?

A Fair Value Gap is a trading pattern where there's a gap in price action:
- **Bullish FVG**: Current candle's low > Previous candle's high (2 periods back)
- **Bearish FVG**: Current candle's high < Previous candle's low (2 periods back)

### Data Files

The repository contains historical OHLC (Open, High, Low, Close) data in CSV format:
- Years: 2018-2025
- Timeframes: 1 minute (1m), 5 minutes (5m), 15 minutes (15m), 1 hour (1H), 4 hours (4H), 1 day (1D)
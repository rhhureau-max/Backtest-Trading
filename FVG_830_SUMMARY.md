# Fair Value Gap (FVG) Analysis at 8:30:00

## Summary

This analysis identifies all Fair Value Gaps (FVGs) that occur at exactly 8:30:00 in the trading data.

### What is a Fair Value Gap?

A Fair Value Gap (FVG) is a trading pattern that occurs when there is a gap in price action between candles:

- **Bullish FVG**: The low of the current candle is higher than the high of the candle 2 periods ago
- **Bearish FVG**: The high of the current candle is lower than the low of the candle 2 periods ago

### Total FVGs Found at 8:30:00

**401 FVGs** were identified across all timeframes and years.

### Breakdown by File

| File | FVGs at 8:30:00 |
|------|----------------|
| 2018 15m.csv | 21 |
| 2018 5m.csv | 19 |
| 2019 15m.csv | 19 |
| 2019 5m.csv | 35 |
| 2020 15m.csv | 17 |
| 2020 5m.csv | 24 |
| 2021 15m.csv | 16 |
| 2021 5m.csv | 25 |
| 2022 15m.csv | 15 |
| 2022 5m.csv | 26 |
| 2023 15m.csv | 20 |
| 2023 5m.csv | 24 |
| 2024 15m.csv | 32 |
| 2024 5m.csv | 43 |
| 2025 15m.csv | 19 |
| 2025 1m.csv | 11 |
| 2025 5m.csv | 35 |
| **Total** | **401** |

### Usage

To generate the detailed FVG report, run:

```bash
python3 detect_fvg_at_830.py
```

This will display all 401 FVGs with complete details including:
- Date and Time
- FVG Type (Bullish/Bearish)
- Gap Size
- Gap Range
- OHLC data for the three candles involved (previous, middle, current)

To save the output to a file:

```bash
python3 detect_fvg_at_830.py > fvg_830_results.txt
```

### Notes

- FVGs at 8:30:00 are particularly significant as this often corresponds to market opening times in various regions
- The analysis covers data from 2018 to 2025
- Higher timeframes (15m, 5m, 1m) show more frequent FVGs at this specific time
- Daily and 4-hour timeframes do not have data points at exactly 8:30:00

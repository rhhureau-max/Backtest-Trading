# Example Output - FVG Analysis at 8:30:00

## Quick List Format

Running `python3 list_fvg_at_830.py` produces:

```
====================================================================================================
FVG List at 8:30:00
====================================================================================================

Total FVGs at 8:30:00: 401

#     File                 Date         Time       Type       Gap Size       
----------------------------------------------------------------------------------------------------
1     2018 15m.csv         03/01/2018   08:30:00   Bullish    2.050202       
2     2018 15m.csv         17/01/2018   08:30:00   Bearish    9.958125       
3     2018 15m.csv         18/01/2018   08:30:00   Bullish    2.928860       
...
399   2025 5m.csv          02/09/2025   08:30:00   Bearish    5.049519       
400   2025 5m.csv          10/09/2025   08:30:00   Bearish    3.787140       
401   2025 5m.csv          11/09/2025   08:30:00   Bullish    6.816851       
====================================================================================================
Total: 401 FVGs
```

## Detailed Format

Running `python3 detect_fvg_at_830.py` shows full details for each FVG:

```
1. 2018 15m.csv
   Date: 03/01/2018
   Time: 08:30:00
   Type: Bullish FVG
   Gap Size: 2.050202
   Gap Range: 7643.446293 to 7645.496495

   Previous Candle (i-2): O=7639.93166 H=7643.446293 L=7639.93166 C=7643.446293
   Middle Candle   (i-1): O=7643.446293 H=7651.354215 L=7641.39609 C=7646.082267
   Current Candle  (i)  : O=7646.082267 H=7673.320666 L=7645.496495 C=7668.927376
--------------------------------------------------------------------------------

2. 2018 15m.csv
   Date: 17/01/2018
   Time: 08:30:00
   Type: Bearish FVG
   Gap Size: 9.958125
   Gap Range: 7945.704658 to 7955.662783

   Previous Candle (i-2): O=7958.298757 H=7961.227617 L=7955.662783 C=7958.591643
   Middle Candle   (i-1): O=7958.591643 H=7960.348959 L=7943.068684 C=7945.411772
   Current Candle  (i)  : O=7945.704658 H=7945.704658 L=7916.123171 C=7923.152435
--------------------------------------------------------------------------------
```

## Summary Statistics

### Breakdown by Year and Timeframe

| Year | Timeframe | FVG Count |
|------|-----------|-----------|
| 2018 | 15m | 21 |
| 2018 | 5m | 19 |
| 2019 | 15m | 19 |
| 2019 | 5m | 35 |
| 2020 | 15m | 17 |
| 2020 | 5m | 24 |
| 2021 | 15m | 16 |
| 2021 | 5m | 25 |
| 2022 | 15m | 15 |
| 2022 | 5m | 26 |
| 2023 | 15m | 20 |
| 2023 | 5m | 24 |
| 2024 | 15m | 32 |
| 2024 | 5m | 43 |
| 2025 | 15m | 19 |
| 2025 | 1m | 11 |
| 2025 | 5m | 35 |

### Key Insights

1. **Most Active Year**: 2024 with 75 FVGs at 8:30:00
2. **Most Active Timeframe**: 5-minute candles show more FVGs than 15-minute
3. **FVG Distribution**: 
   - Bullish and Bearish FVGs are both well-represented
   - Gap sizes vary significantly (from 0.29 to 22.44 points)
4. **Significance**: 8:30:00 is a critical time for FVG formation, likely due to market opening events

## Understanding the Output

### FVG Detection Logic

A Fair Value Gap is detected using a 3-candle pattern:

**Bullish FVG:**
```
Candle i-2:  [====]         (Previous)
                   ^-- High of previous
Candle i-1:        [====]   (Middle)

Candle i:              [====]  (Current)
                       ^-- Low of current

Gap exists when: Low(i) > High(i-2)
```

**Bearish FVG:**
```
Candle i-2:        [====]   (Previous)
                   ^-- Low of previous
Candle i-1:    [====]       (Middle)

Candle i:  [====]           (Current)
           ^-- High of current

Gap exists when: High(i) < Low(i-2)
```

### Column Meanings

- **Date**: Trading date
- **Time**: Exact time (always 08:30:00 for this analysis)
- **Type**: Bullish (gap up) or Bearish (gap down)
- **Gap Size**: Distance between price levels (in points)
- **Gap Range**: The price range where the gap exists
- **OHLC**: Open, High, Low, Close for each candle

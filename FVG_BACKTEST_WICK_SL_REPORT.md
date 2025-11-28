# FVG Trading Strategy Backtest - Wick-Based Stop Loss

## Strategy Description

This backtest analyzes a trading strategy based on Fair Value Gaps (FVG) at 8:30 AM with **wick-based stop loss**:

### Entry
- **Entry Point**: Open of candle n+2 (8:32)

### Stop Loss (Wick-Based)
- **Long Position (Bullish FVG)**: SL = Low of candle 8:30 - 1 point
- **Short Position (Bearish FVG)**: SL = High of candle 8:30 + 1 point

### Take Profit
- Based on Risk/Reward ratios: 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5

## FVG Detection Method

The FVG detection uses **High and Low values** (including wicks):

- **Bullish FVG**: Low (wick) of candle 8:31 > High (wick) of candle 8:29 → Long
- **Bearish FVG**: High (wick) of candle 8:31 < Low (wick) of candle 8:29 → Short

## Data Summary

- **Period**: 2018 - 2025
- **Total FVG Signals**: 813
- **Bullish FVGs (Long)**: 460
- **Bearish FVGs (Short)**: 353
- **Average SL Distance**: 32.23 points

## Overall Results

| RR | Trades | Wins | Losses | Open | Win Rate | Expected Value |
|:--:|:------:|:----:|:------:|:----:|:--------:|:--------------:|
| 1.0 | 813.0 | 428.0 | 385.0 | 0.0 | 52.64% | 🟢 0.0529 |
| 1.5 | 813.0 | 356.0 | 455.0 | 2.0 | 43.79% | 🟢 0.0972 |
| 2.0 | 813.0 | 295.0 | 512.0 | 6.0 | 36.29% | 🟢 0.0959 |
| 2.5 | 813.0 | 255.0 | 548.0 | 10.0 | 31.37% | 🟢 0.1101 |
| 3.0 | 813.0 | 222.0 | 569.0 | 22.0 | 27.31% | 🟢 0.1193 |
| 3.5 | 813.0 | 197.0 | 586.0 | 30.0 | 24.23% | 🟢 0.1273 |
| 4.0 | 813.0 | 174.0 | 598.0 | 41.0 | 21.40% | 🟢 0.1205 |
| 4.5 | 813.0 | 156.0 | 606.0 | 51.0 | 19.19% | 🟢 0.1181 |
| 5.0 | 813.0 | 140.0 | 610.0 | 63.0 | 17.22% | 🟢 0.1107 |

## Results by FVG Type

### Bullish FVG (Long)

| RR | Trades | Wins | Losses | Open | Win Rate | Expected Value |
|:--:|:------:|:----:|:------:|:----:|:--------:|:--------------:|
| 1.0 | 460 | 242 | 218 | 0 | 52.61% | 🟢 0.0522 |
| 1.5 | 460 | 201 | 257 | 2 | 43.70% | 🟢 0.0967 |
| 2.0 | 460 | 165 | 290 | 5 | 35.87% | 🟢 0.0870 |
| 2.5 | 460 | 142 | 313 | 5 | 30.87% | 🟢 0.0913 |
| 3.0 | 460 | 125 | 324 | 11 | 27.17% | 🟢 0.1109 |
| 3.5 | 460 | 110 | 335 | 15 | 23.91% | 🟢 0.1087 |
| 4.0 | 460 | 94 | 343 | 23 | 20.43% | 🟢 0.0717 |
| 4.5 | 460 | 80 | 350 | 30 | 17.39% | 🟢 0.0217 |
| 5.0 | 460 | 70 | 353 | 37 | 15.22% | 🔴 -0.0065 |

### Bearish FVG (Short)

| RR | Trades | Wins | Losses | Open | Win Rate | Expected Value |
|:--:|:------:|:----:|:------:|:----:|:--------:|:--------------:|
| 1.0 | 353 | 186 | 167 | 0 | 52.69% | 🟢 0.0538 |
| 1.5 | 353 | 155 | 198 | 0 | 43.91% | 🟢 0.0977 |
| 2.0 | 353 | 130 | 222 | 1 | 36.83% | 🟢 0.1076 |
| 2.5 | 353 | 113 | 235 | 5 | 32.01% | 🟢 0.1346 |
| 3.0 | 353 | 97 | 245 | 11 | 27.48% | 🟢 0.1303 |
| 3.5 | 353 | 87 | 251 | 15 | 24.65% | 🟢 0.1516 |
| 4.0 | 353 | 80 | 255 | 18 | 22.66% | 🟢 0.1841 |
| 4.5 | 353 | 76 | 256 | 21 | 21.53% | 🟢 0.2436 |
| 5.0 | 353 | 70 | 257 | 26 | 19.83% | 🟢 0.2635 |

## Key Insights

### Best Overall Configuration
- **RR Ratio**: 3.5
- **Win Rate**: 24.23%
- **Expected Value**: 0.1273

### Best Bullish FVG (Long) Configuration
- **RR Ratio**: 3.0
- **Win Rate**: 27.17%
- **Expected Value**: 0.1109

### Best Bearish FVG (Short) Configuration
- **RR Ratio**: 5.0
- **Win Rate**: 19.83%
- **Expected Value**: 0.2635

## Comparison with Body-Based SL

This wick-based SL strategy differs from the body-based SL:

| Aspect | Body-Based SL | Wick-Based SL |
|--------|---------------|---------------|
| SL Location | % of candle body | 1 point from wick |
| Long SL | Entry - (Body × %) | Low of 8:30 - 1 |
| Short SL | Entry + (Body × %) | High of 8:30 + 1 |
| SL Distance | Variable (based on body) | Variable (based on wick) |

## Data Files

- `fvg_backtest_wick_sl_results.csv`: Overall statistics by RR ratio
- `fvg_backtest_wick_sl_by_type.csv`: Statistics separated by FVG type
- `fvg_backtest_wick_sl.py`: Python script used for this backtest

# Trading Setup Pattern Analysis - Summary

## Overview
This analysis examined trading data from **2018 to 2025** across three timeframes (1-minute, 5-minute, and 15-minute) to identify specific reversal patterns at the 8:30 AM trading session.

## Setup Patterns Analyzed

### 1. Bearish Setup (Bearish to Bullish Reversal)
- **Condition 1**: 8:30 AM candle is bearish (Close < Open)
- **Condition 2**: Next candle is bullish (Close > Open)
- **Condition 3**: Next candle closes ABOVE the maximum of the last 5 candles

### 2. Bullish Setup (Bullish to Bearish Reversal)
- **Condition 1**: 8:30 AM candle is bullish (Close > Open)
- **Condition 2**: Next candle is bearish (Close < Open)
- **Condition 3**: Next candle closes BELOW the minimum of the last 5 candles

## Key Findings

### Total Setups Found: **695**

| Timeframe | Bearish Setups | Bullish Setups | Total |
|-----------|---------------|---------------|-------|
| 1-minute  | 138           | 141           | 279   |
| 5-minute  | 116           | 116           | 232   |
| 15-minute | 99            | 85            | 184   |
| **TOTAL** | **353**       | **342**       | **695** |

## Pattern Distribution Insights

1. **Balanced Distribution**: The bearish and bullish setups are nearly evenly distributed (353 vs 342), suggesting no inherent market bias.

2. **Frequency by Timeframe**: 
   - 1-minute data shows the most setups (279 total)
   - 5-minute data shows moderate frequency (232 total)
   - 15-minute data shows fewer setups (184 total)
   - This is expected as smaller timeframes have more trading opportunities

3. **Timeframe Pattern Strength**:
   - **1-minute**: Average breakout ~9 points (both directions)
   - **5-minute**: Average breakout ~13-16 points
   - **15-minute**: Average breakout ~19-24 points
   - **Larger timeframes show stronger breakouts**, indicating more significant moves

## Statistical Analysis

### Bearish Setup Statistics (by Timeframe)

| Timeframe | Avg Breakout | Max Breakout | Min Breakout |
|-----------|-------------|--------------|--------------|
| 1m        | 9.03 pts    | 55.27 pts    | 0.57 pts     |
| 5m        | 12.64 pts   | 79.64 pts    | 0.27 pts     |
| 15m       | 19.02 pts   | 103.09 pts   | 0.29 pts     |

### Bullish Setup Statistics (by Timeframe)

| Timeframe | Avg Breakout | Max Breakout | Min Breakout |
|-----------|-------------|--------------|--------------|
| 1m        | 8.87 pts    | 45.82 pts    | 0.27 pts     |
| 5m        | 15.88 pts   | 68.56 pts    | 0.29 pts     |
| 15m       | 24.24 pts   | 122.92 pts   | 0.57 pts     |

## Trading Implications

1. **Setup Reliability**: With 695 occurrences over 8 years, these patterns occur approximately:
   - **87 times per year** on average
   - **1.7 times per week** across all timeframes

2. **Breakout Magnitude**: 
   - Larger timeframes produce stronger breakouts
   - 15m bullish setups show the strongest average breakout (24.24 points)
   - Maximum recorded breakout: 122.92 points (15m bullish setup)

3. **Risk Management**:
   - Minimum breakouts are very small (< 1 point), suggesting tight stops are viable
   - Average breakouts provide reasonable profit targets
   - Maximum breakouts suggest potential for large moves

## Files Generated

1. **analyze_trading_setups.py** - The Python analysis script
2. **trading_setup_report.txt** - Detailed report (266KB) containing:
   - Complete setup definitions
   - Summary statistics
   - Detailed information for each of the 695 setups found
   - Date, time, and price levels for every setup
   - Additional statistical analysis

## How to Use This Analysis

1. **Review the detailed report** (`trading_setup_report.txt`) for specific dates and setups
2. **Backtest individual setups** using the provided date/time information
3. **Consider timeframe selection** based on your trading style:
   - Short-term traders: 1m or 5m
   - Swing traders: 15m
4. **Apply risk management** based on historical breakout statistics

## Data Sources

- **Years**: 2018-2025
- **1-minute data**: Extracted from .zip files (2018-2024) and CSV (2025)
- **5-minute & 15-minute data**: Direct CSV files
- **Format**: Date;Time;Open;High;Low;Close;Volume

## Next Steps

Consider further analysis:
- Win rate analysis (follow-up price action)
- Optimal entry/exit timing
- Correlation with market volatility
- Seasonal patterns
- Volume analysis at setup times

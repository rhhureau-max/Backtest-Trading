# IFVG (Inversion Fair Value Gap) Backtest - London Killzone

## Overview
This backtest analyzes the **Inversion Fair Value Gap (IFVG)** strategy during the London Killzone (01:00-04:00) using NQ (Nasdaq) 5-minute data from 2018-2025, with ES (S&P 500) correlation analysis.

## Strategy Methodology - ICT (Inner Circle Trader)

### Fair Value Gap (FVG) Definition
- **Bearish FVG**: When Low of Candle 1 > High of Candle 3 (gap down)
  - Zone: High of Candle 3 to Low of Candle 1
- **Bullish FVG**: When High of Candle 1 < Low of Candle 3 (gap up)
  - Zone: Low of Candle 1 to High of Candle 3

### IFVG Trigger (Inversion)
- **LONG Signal**: Price closes ABOVE the High of a recent Bearish FVG (created within last 60 minutes)
- **SHORT Signal**: Price closes BELOW the Low of a recent Bullish FVG (created within last 60 minutes)

### Confluence Filters

#### 1. Displacement / CSID (Candle Strength)
- The trigger candle must have a significant body
- **Rule**: |Close - Open| > 60% of (High - Low)

#### 2. MSS (Market Structure Shift)
- **LONG**: Current candle breaks above the highest high of the last 12 candles (1 hour)
- **SHORT**: Current candle breaks below the lowest low of the last 12 candles (1 hour)

#### 3. SMT Divergence (Smart Money Technique - NQ vs ES)
- **Bullish SMT (LONG)**: NQ makes a Lower Low WHILE ES makes a Higher Low or Double Bottom
- **Bearish SMT (SHORT)**: NQ makes a Higher High WHILE ES makes a Lower High or Double Top
- Comparison window: 60 minutes (12 candles) before signal

## Risk Management
- **Stop Loss**: 20 points (fixed)
- **Take Profit**: 40 points (fixed)
- **Risk/Reward**: 1:2
- **Fees**: Not included (raw analysis)

## Backtest Results (2018-2025)

### Performance Summary

| Scenario | Trades | Win Rate | Total PnL |
|----------|--------|----------|-----------|
| **1. IFVG Base (Trigger Only)** | 5,216 | 39.23% | 18,440 pts |
| **2. IFVG + Displacement** | 1,731 | 37.72% | 4,560 pts |
| **3. IFVG + MSS** | 464 | 38.15% | 1,340 pts |
| **4. IFVG + SMT Divergence** | 423 | 38.77% | 1,380 pts |
| **5. ICT Gold (IFVG + Displacement + SMT)** | 132 | 34.85% | 120 pts |

### Detailed Statistics

#### Scenario 1: IFVG Base (Trigger Only)
- **Trades**: 5,216
- **Wins**: 2,046 | **Losses**: 3,170
- **Win Rate**: 39.23%
- **Total PnL**: 18,440 points
- **Average Win**: 40 points
- **Average Loss**: -20 points

#### Scenario 2: IFVG + Displacement
- **Trades**: 1,731
- **Wins**: 653 | **Losses**: 1,078
- **Win Rate**: 37.72%
- **Total PnL**: 4,560 points
- **Average Win**: 40 points
- **Average Loss**: -20 points

#### Scenario 3: IFVG + MSS
- **Trades**: 464
- **Wins**: 177 | **Losses**: 287
- **Win Rate**: 38.15%
- **Total PnL**: 1,340 points
- **Average Win**: 40 points
- **Average Loss**: -20 points

#### Scenario 4: IFVG + SMT Divergence
- **Trades**: 423
- **Wins**: 164 | **Losses**: 259
- **Win Rate**: 38.77%
- **Total PnL**: 1,380 points
- **Average Win**: 40 points
- **Average Loss**: -20 points

#### Scenario 5: ICT Gold (IFVG + Displacement + SMT)
- **Trades**: 132
- **Wins**: 46 | **Losses**: 86
- **Win Rate**: 34.85%
- **Total PnL**: 120 points
- **Average Win**: 40 points
- **Average Loss**: -20 points

## Key Insights

### 1. Base Strategy Performance
- The **IFVG Base strategy** (no filters) generated the most trades (5,216) and highest total PnL (18,440 pts)
- Win rate: 39.23% - profitable despite sub-40% win rate due to 1:2 R/R ratio
- Demonstrates the core IFVG concept has statistical edge

### 2. Filter Impact Analysis

#### Displacement Filter
- **Trade Reduction**: 66.8% fewer trades (5,216 → 1,731)
- **Win Rate Impact**: Decreased slightly (39.23% → 37.72%)
- **PnL Impact**: 75.3% lower total PnL (18,440 → 4,560 pts)
- **Conclusion**: Filtering for strong candles reduces opportunity without improving win rate

#### MSS Filter
- **Trade Reduction**: 91.1% fewer trades (5,216 → 464)
- **Win Rate Impact**: Minimal decrease (39.23% → 38.15%)
- **PnL Impact**: 92.7% lower total PnL (18,440 → 1,340 pts)
- **Conclusion**: Very selective but doesn't enhance win rate significantly

#### SMT Divergence Filter
- **Trade Reduction**: 91.9% fewer trades (5,216 → 423)
- **Win Rate Impact**: Minimal decrease (39.23% → 38.77%)
- **PnL Impact**: 92.5% lower total PnL (18,440 → 1,380 pts)
- **Conclusion**: Highly selective based on NQ/ES divergence, modest benefit

#### Combined Filters (ICT Gold)
- **Trade Reduction**: 97.5% fewer trades (5,216 → 132)
- **Win Rate Impact**: Significant decrease (39.23% → 34.85%)
- **PnL Impact**: 99.3% lower total PnL (18,440 → 120 pts)
- **Conclusion**: Over-filtering reduces both opportunity and profitability

### 3. Strategic Recommendations

1. **Best Overall Strategy**: **IFVG Base (Trigger Only)**
   - Highest absolute PnL (18,440 pts)
   - Reasonable win rate (39.23%)
   - Good trade frequency (5,216 trades over 7 years ≈ 2 trades/day)
   - With 1:2 R/R, break-even is 33.3% - this strategy exceeds it

2. **For Conservative Traders**: **IFVG + MSS or IFVG + SMT**
   - Fewer trades (464-423)
   - Similar win rates (38.15-38.77%)
   - Still profitable with reduced exposure

3. **Avoid Over-Filtering**:
   - Combining multiple filters (ICT Gold) reduces trade count dramatically
   - Does not improve win rate
   - Results in minimal PnL despite selectivity

### 4. Risk-Adjusted Perspective

**Per Trade Expectancy** (Base Strategy):
- Win Rate: 39.23% × 40 pts = 15.69 pts
- Loss Rate: 60.77% × (-20 pts) = -12.15 pts
- **Expected Value per Trade**: +3.54 pts

This positive expectancy confirms the strategy's edge.

## Data Specifications

### NQ Data
- **Source**: Multiple 5-minute CSV files (2018-2025)
- **Total Candles**: 739,403 candles loaded
- **London Killzone**: 97,488 candles (01:00-04:00)
- **FVGs Detected**: 4,419 Bearish, 5,057 Bullish

### ES Data
- **Source**: ES 5m CSV files (2018-2025)
- **Total Candles**: 559,127 candles loaded
- **Synchronized**: 554,526 common timestamps with NQ
- **London Killzone**: 73,151 candles

## Files Generated

1. **ifvg_london_killzone_backtest.py**: Main backtest script
2. **ifvg_backtest_trades.csv**: Detailed trade log (7,966 total trades across all scenarios)
3. **README_IFVG_BACKTEST.md**: This documentation

## Usage

Run the backtest:
```bash
python ifvg_london_killzone_backtest.py
```

The script will:
1. Load NQ and ES 5-minute data (2018-2025)
2. Synchronize both datasets
3. Filter for London Killzone hours (01:00-04:00)
4. Detect Fair Value Gaps
5. Run all 5 scenarios with different filter combinations
6. Generate performance report
7. Export trade log to CSV

## Technical Implementation

### Data Processing
- Automatic loading of multiple CSV files per instrument
- DateTime synchronization between NQ and ES
- Time filtering for London Killzone session

### FVG Detection
- 3-candle pattern recognition
- Zone boundaries calculation
- Recency tracking (60-minute window)

### Trade Simulation
- Fixed SL/TP levels
- Bar-by-bar execution
- Outcome tracking (WIN/LOSS/OPEN)

### Filter Logic
- Displacement: Body-to-range ratio calculation
- MSS: Rolling high/low detection
- SMT: Cross-asset divergence analysis with NaN handling

## Conclusion

The **IFVG (Inversion Fair Value Gap)** strategy demonstrates a positive edge during the London Killzone with a 1:2 risk/reward ratio. The base strategy (trigger only) outperforms filtered versions, suggesting that the core IFVG concept captures market reversals effectively without requiring additional confluence factors.

**Key Takeaway**: Sometimes less is more. The simplest approach (IFVG Base) provided the best results, challenging the assumption that more filters always improve performance.

---

**Author**: ICT Trading Analysis System  
**Date**: December 2025  
**Period Tested**: 2018-2025 (7+ years)  
**Instrument**: NQ Futures (Nasdaq) with ES correlation

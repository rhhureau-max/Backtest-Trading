# NQ (Nasdaq) 5-Minute Backtesting Strategy

## Overview

This is a complete backtesting implementation for trading NQ (Nasdaq) futures using Fair Value Gaps (FVG) on 5-minute data from 2018 to 2025.

## Strategy Description

### Trading Window
- **Active Hours**: 02:00:00 to 06:00:00 (no timezone conversion)
- Only signals generated and trades entered during this window
- FVGs created outside this window are ignored

### Fair Value Gap (FVG) Detection

**Bullish FVG**: 
- Occurs when `low[n+1] > high[n-1]` (gap upward)
- Upper bound: `low[n+1]`
- Lower bound: `high[n-1]`

**Bearish FVG**: 
- Occurs when `high[n+1] < low[n-1]` (gap downward)
- Upper bound: `low[n-1]`
- Lower bound: `high[n+1]`

Note: FVG detection uses wicks (high/low), not just candle bodies.

### Entry Conditions

**Long Entry**:
- Current candle closes bullish (close > open)
- Close is above upper bound of a previous bearish FVG
- The bearish FVG was created during 02:00-06:00
- No trade has been taken on this FVG yet
- Entry at close price

**Short Entry**:
- Current candle closes bearish (close < open)
- Close is below lower bound of a previous bullish FVG
- The bullish FVG was created during 02:00-06:00
- No trade has been taken on this FVG yet
- Entry at close price

### Stop Loss & Take Profit

**Stop Loss**:
- Long: Below the last Swing Low before entry
- Short: Above the last Swing High before entry

**Swing Points**:
- Swing High: local high surrounded by lower highs
- Swing Low: local low surrounded by higher lows

**Take Profit Strategies** (4 options):
1. **1R**: TP = Entry ± 1 × Risk
2. **1.5R**: TP = Entry ± 1.5 × Risk
3. **2R**: TP = Entry ± 2 × Risk
4. **Structural**: 
   - Long: TP at last Swing High
   - Short: TP at last Swing Low

### Trade Management
- Only one trade at a time (no pyramiding)
- Each FVG can only be used once for entry
- Trades close only via Stop Loss or Take Profit
- All analysis on 5-minute candles

## Backtest Results Summary

### Data Coverage
- **Period**: 2018-01-01 to 2025-11-11
- **Total Candles**: 554,518
- **Total FVGs Detected**: 19,992
  - Bullish FVGs: 10,464
  - Bearish FVGs: 9,528

### Performance by Strategy

| Strategy   | Trades | Win Rate | Total PnL | Profit Factor | Max Drawdown |
|------------|--------|----------|-----------|---------------|--------------|
| 1R         | 19,712 | 49.54%   | 10,043.94 | 1.04          | 5,049.49     |
| 1.5R       | 19,712 | 40.16%   | 13,282.17 | 1.05          | 6,383.90     |
| 2R         | 19,712 | 33.56%   | 13,552.43 | 1.04          | 8,411.04     |
| Structural | 19,566 | 60.12%   | -4,511.83 | 0.96          | 5,694.36     |

### Key Findings

**Best Overall Strategy: 2R**
- Highest total PnL: 13,552.43 points
- Profit Factor: 1.04
- Win Rate: 33.56%
- Average Win: 50.78 points
- Average Loss: -24.62 points
- Trade Duration: 21.6 bars (108 minutes average)

**Most Consistent: 1.5R**
- Second-best PnL: 13,282.17 points
- Highest Profit Factor: 1.05
- Win Rate: 40.16%
- Average Win: 38.17 points
- Average Loss: -24.49 points

**Conservative Option: 1R**
- Lowest drawdown: 5,049.49 points
- Shortest time in trades: 12.8 bars (64 minutes)
- Win Rate: 49.54%
- Balanced risk/reward with 1:1 ratio

**Structural Strategy**
- Highest win rate: 60.12%
- Negative overall PnL: -4,511.83 points
- Fastest exits: 4.7 bars average
- Not recommended for this strategy

### Direction Analysis (2R Strategy)
- **Long Trades**: 9,521 trades, +10,742.66 points (avg +1.13 per trade)
- **Short Trades**: 10,191 trades, +2,809.78 points (avg +0.28 per trade)

## How to Run

### Prerequisites
```bash
pip install pandas numpy
```

### Execute Backtest
```bash
python3 nq_backtest_strategy.py
```

### Run Individual Strategy
To test a single strategy, modify the main section:
```python
if __name__ == "__main__":
    data_dir = "/path/to/data"
    
    # Run single strategy
    backtester = FVGBacktester(data_dir, tp_multiplier='2R')
    backtester.load_data()
    backtester.run_backtest()
    stats = backtester.calculate_statistics()
    backtester.print_results(stats)
```

## Files

- `nq_backtest_strategy.py` - Main backtesting script
- `2018 5m.csv` through `2025 5m.csv` - Data files

## Data Format

CSV files with semicolon separator:
```
Column1;Column2;Column3;Column4;Column5;Column6;Column7
Date;Time;Open;High;Low;Close;Volume
01/01/2018;17:00:00;7503.74;7511.94;7499.64;7511.35;1451
```

## Recommendations

Based on the backtest results:

1. **2R Take Profit** offers the best overall returns with acceptable drawdown
2. **1.5R Take Profit** provides the best balance of profit factor and consistency
3. **Long trades** significantly outperform short trades in this strategy
4. The strategy works best with larger reward targets (1.5R-2R) rather than conservative 1R or structural targets
5. Average holding time increases with larger R multiples (12.8 bars for 1R up to 21.6 bars for 2R)

## Notes

- All times are used exactly as they appear in the data files (no timezone conversion)
- FVGs are only detected and used during the 02:00-06:00 trading window
- Each FVG is single-use only
- The strategy maintains one trade at a time
- Results are based on point movements, not accounting for slippage, commissions, or contract multipliers

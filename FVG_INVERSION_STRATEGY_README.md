# NQ Futures - First FVG Inversion Backtesting Strategy

## Overview
This repository contains a comprehensive backtesting implementation of the **First FVG Inversion Strategy** for NQ (Nasdaq 100) Futures using 1-minute historical data from 2018-2025.

## Strategy Description

### Fair Value Gap (FVG) Definition
- **Bearish FVG**: Created when `Low[i-2] > High[i]` (gap exists between `High[i]` and `Low[i-2]`)
- **Bullish FVG**: Created when `High[i-2] < Low[i]` (gap exists between `High[i-2]` and `Low[i]`)

### Entry Signals (The Inversion)
1. **LONG Signal**: After a Bearish FVG is created, when a 1-minute candle closes **ABOVE** the top of that Bearish FVG
2. **SHORT Signal**: After a Bullish FVG is created, when a 1-minute candle closes **BELOW** the bottom of that Bullish FVG

### Session Management & "One Bullet" Rule
The strategy operates during two specific killzone sessions (Chicago Time):
- **London Session**: 01:00 - 04:00 CT
- **New York Session**: 08:30 - 11:00 CT

**Critical Rule**: Only the **FIRST** valid inversion signal in each session is taken. All subsequent signals are ignored until the next session begins.

### Risk Management
- **Entry**: At the close price of the signal candle
- **Stop Loss**:
  - Long: Below the low of the signal candle
  - Short: Above the high of the signal candle
- **Take Profit**: 1:1 Risk-to-Reward Ratio

## Data Configuration

### Data Source
- **Years**: 2018-2024 (from zip files) + 2025 (from CSV)
- **Format**: Semicolon-delimited CSV files
- **Columns**: Date, Time, Open, High, Low, Close, Volume
- **Timezone**: Chicago Time (CT) - already in correct timezone
- **Timeframe**: 1-minute raw data (no resampling)

### Total Dataset
- **2,771,419** 1-minute candles
- **Date Range**: January 1, 2018 - December 11, 2025

## Installation & Usage

### Prerequisites
```bash
pip install -r requirements.txt
```

### Running the Backtest
```bash
python3 fvg_inversion_backtest.py
```

## Backtest Results

### Overall Performance (2018-2025)
```
Total Trades:      4,059
Wins:              1,926 (47.45%)
Losses:            2,133 (52.55%)
Win Rate:          47.45%
Gross Profit:      $22,956.36
Gross Loss:        $22,913.75
Profit Factor:     1.00
Net Profit:        $42.61
Max Drawdown:      $1,105.92
```

### London Session (01:00-04:00 CT)
```
Total Trades:      2,030
Wins:              941 (46.35%)
Losses:            1,089 (53.65%)
Win Rate:          46.35%
Gross Profit:      $4,508.18
Gross Loss:        $4,660.42
Profit Factor:     0.97
Net Profit:        -$152.24
Max Drawdown:      $259.61
```

### New York Session (08:30-11:00 CT)
```
Total Trades:      2,029
Wins:              985 (48.55%)
Losses:            1,044 (51.45%)
Win Rate:          48.55%
Gross Profit:      $18,448.19
Gross Loss:        $18,253.33
Profit Factor:     1.01
Net Profit:        $194.86
Max Drawdown:      $1,155.07
```

## Key Insights

### Strategy Performance
1. **Balanced Distribution**: Strategy found valid signals in both sessions equally (~2,030 trades per session)
2. **Session Comparison**: New York session slightly outperforms London (48.55% vs 46.35% win rate)
3. **Market Efficiency**: Near break-even results suggest that simple FVG inversion without additional filters operates close to random walk
4. **Consistency**: Profit factor near 1.00 indicates consistent risk/reward execution

### FVG Statistics
- **Total Bearish FVGs Identified**: 296,280
- **Total Bullish FVGs Identified**: 314,351
- **Total FVGs**: 610,631 (across 2.77M candles = 22% FVG occurrence rate)

### Observations
- The "One Bullet" rule ensures **only 4,059 trades** were taken from **610,631 potential FVG formations**
- This demonstrates excellent trade selectivity (0.66% of FVGs converted to trades)
- The 1:1 R:R ratio with ~47% win rate produces near break-even results
- New York session shows better profitability despite similar number of trades

## Output Files

### 1. `fvg_inversion_equity_curve.png`
Visualization showing:
- Overall cumulative equity curve
- Session-separated equity curves (London vs New York)

### 2. `fvg_inversion_trades.csv`
Detailed trade log containing:
- Entry/Exit timestamps
- Entry/Exit prices
- Direction (LONG/SHORT)
- Stop Loss and Take Profit levels
- Session identifier
- Trade outcome (Win/Loss/Open)
- P&L per trade

## Code Structure

### Main Components

1. **`FVGInversionBacktest` Class**
   - `load_data()`: Loads and combines all 1-minute data files
   - `identify_fvg()`: Detects all Fair Value Gaps in the dataset
   - `backtest_strategy()`: Executes the "One Bullet" rule strategy
   - `evaluate_trades()`: Determines win/loss outcomes
   - `calculate_metrics()`: Computes performance statistics
   - `generate_report()`: Creates comprehensive performance report
   - `plot_equity_curve()`: Generates equity curve visualizations
   - `save_trades_to_csv()`: Exports trade log

### Algorithm Efficiency
- Vectorized operations using pandas for FVG detection
- Efficient session management with time-based filtering
- Single-pass backtesting algorithm
- Memory-efficient data handling for 2.7M+ rows

## Recommendations for Improvement

Based on the results, consider these enhancements:
1. **Add Filters**: Implement confluence factors (support/resistance, trend, volume)
2. **Optimize R:R**: Test different risk-reward ratios (1:1.5, 1:2, etc.)
3. **Time-of-Day Analysis**: Analyze which specific minutes within sessions perform best
4. **FVG Quality**: Add size requirements for FVG gaps (minimum point value)
5. **Market Context**: Consider overall market trend before taking signals
6. **Commission/Slippage**: Add realistic transaction costs
7. **Position Sizing**: Implement dynamic position sizing based on equity

## Technical Notes

- **Data Integrity**: Script handles mixed date formats automatically
- **Timezone**: All analysis conducted in Chicago Time (no conversion needed)
- **Session Logic**: Precise time-based session detection with date rollover handling
- **Trade Execution**: Conservative approach (no partial fills, assumes fill at close)

## License
This backtest is for educational and research purposes only. Past performance does not guarantee future results.

## Author
Senior Quantitative Trader & Python Developer

---

**Last Updated**: January 11, 2026

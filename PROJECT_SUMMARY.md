# FVG Inversion Backtesting System - Project Summary

## Overview
This project implements a comprehensive backtesting system for NQ (Nasdaq 100) Futures using the Fair Value Gap (FVG) Inversion strategy on 1-minute data spanning 2018-2024.

## Files Created

### 1. **combine_data.py**
- Merges individual yearly CSV files (2018-2024) into a single consolidated dataset
- Handles semicolon-delimited data with proper datetime parsing
- Output: `NQ_1min_2018_2024.csv` (221MB, 2.46M rows)

### 2. **fvg_inversion_backtest.py**
- Main backtesting engine implementing the FVG Inversion strategy
- Features:
  - Fair Value Gap detection (Bearish and Bullish FVGs)
  - Session-based trading (London: 01:00-04:00 CT, New York: 08:30-11:00 CT)
  - "One Bullet" rule: Only first signal per session
  - 1:1 Risk-to-Reward ratio
  - Comprehensive performance metrics
  - Equity curve visualization

### 3. **FVG_INVERSION_README.md**
- Complete documentation for the backtesting system
- Includes strategy logic, usage instructions, and examples

### 4. **.gitignore**
- Excludes large generated files and Python cache files

## Generated Output Files

### **fvg_inversion_trades.csv**
- Detailed trade-by-trade results (3,615 trades)
- Columns: entry/exit datetime, session, signal type, prices, P&L, exit reason, win/loss

### **fvg_inversion_equity_curve.png**
- Visual representation of cumulative equity over time
- Shows overall performance trajectory

### **fvg_inversion_session_comparison.png**
- Side-by-side comparison of London vs New York session performance
- Separate equity curves for each session

## Backtest Results Summary

### Overall Performance (2018-2024)
- **Total Trades**: 3,615
- **Win Rate**: 37.21%
- **Profit Factor**: 0.82
- **Net P&L**: -$2,760.26
- **Max Drawdown**: $2,797.16

### London Session (01:00-04:00 CT)
- **Total Trades**: 1,809
- **Win Rate**: 36.26%
- **Profit Factor**: 0.80
- **Net P&L**: -$635.34

### New York Session (08:30-11:00 CT)
- **Total Trades**: 1,806
- **Win Rate**: 38.15%
- **Profit Factor**: 0.83
- **Net P&L**: -$2,124.92

## Strategy Implementation Details

### FVG Detection
- **Bearish FVG**: `Low[i-2] > High[i]` → Gap between `High[i]` and `Low[i-2]`
- **Bullish FVG**: `High[i-2] < Low[i]` → Gap between `High[i-2]` and `Low[i]`
- Total FVGs found: 540,316

### Entry Logic (Inversion)
- **LONG**: Bearish FVG created → Later candle closes ABOVE FVG top
- **SHORT**: Bullish FVG created → Later candle closes BELOW FVG bottom

### Risk Management
- Entry at signal candle close
- Stop Loss: Signal candle's high/low
- Take Profit: 1:1 RR based on risk

### Session Management
- Only trades during defined killzones
- "One Bullet" rule enforced per session
- Daily reset of trade flags

## Usage Instructions

### Step 1: Combine Data
```bash
python combine_data.py
```
This creates `NQ_1min_2018_2024.csv` from individual year files.

### Step 2: Run Backtest
```bash
python fvg_inversion_backtest.py
```
This generates:
- Performance report (console output)
- `fvg_inversion_trades.csv`
- `fvg_inversion_equity_curve.png`
- `fvg_inversion_session_comparison.png`

## Requirements
```bash
pip install pandas numpy matplotlib
```

## Key Insights from Results

1. **Win Rate**: The strategy has a win rate below 40%, suggesting it catches fewer but potentially larger moves
2. **Profit Factor < 1**: Indicates losses exceeded profits over the test period
3. **Session Balance**: Both sessions performed similarly, with New York slightly better
4. **Trade Frequency**: Average ~500 trades per year, ~1.5 trades per trading day
5. **Consistency**: The "One Bullet" rule effectively limits overtrading

## Possible Improvements

1. **Filtering**: Add additional filters (trend, volatility, time of day)
2. **Risk-Reward**: Test different RR ratios (2:1, 3:1)
3. **Stop Loss**: Implement trailing stops or ATR-based stops
4. **FVG Selection**: Only trade first FVG of session or highest quality FVGs
5. **Session Optimization**: Focus on best-performing time windows
6. **Multiple Timeframes**: Confirm signals with higher timeframe FVGs

## Data Specifications

- **Source Files**: `2018 1m.csv` through `2024 1m.csv`
- **Format**: Semicolon-delimited (`;`)
- **Columns**: Date;Time;Open;High;Low;Close;Volume
- **Date Format**: DD/MM/YYYY
- **Time Format**: HH:MM:SS
- **Timezone**: Chicago Time (CT)
- **Total Records**: 2,464,047 one-minute candles

## Technical Notes

- Processing time: ~5-10 minutes for full backtest
- Memory usage: ~500MB for data loading
- FVG identification: O(n) complexity
- Trade simulation: Efficient forward-walking algorithm
- All prices in NQ Futures points

## Conclusion

This backtesting system provides a complete framework for testing the FVG Inversion strategy on NQ Futures. The implementation includes proper session management, risk controls, and comprehensive reporting. While the historical results show the strategy was not profitable over 2018-2024, the framework enables further optimization and refinement.

The code is clean, well-documented, and extensible for testing variations of the strategy or applying it to different instruments and timeframes.

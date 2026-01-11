# Backtest-Trading

## NQ Futures FVG Inversion Strategy Backtester

This repository contains a professional backtesting script for NQ (Nasdaq 100) Futures using the **Fair Value Gap (FVG) Inversion** strategy with strict session management.

### Strategy Overview

**Fair Value Gap (FVG) Inversion Strategy** with the "One Bullet Rule":
- **Bearish FVG**: Created when `Low[i-2] > High[i]`
- **Bullish FVG**: Created when `High[i-2] < Low[i]`
- **LONG Signal**: Price closes ABOVE the top of a Bearish FVG
- **SHORT Signal**: Price closes BELOW the bottom of a Bullish FVG

### Trading Sessions (Chicago Time)
- **London Killzone**: 01:00 - 04:00
- **New York Killzone**: 08:30 - 11:00

### Risk Management
- **Entry**: At the close of the signal candle
- **Stop Loss**: 
  - LONG: Below the low of signal candle
  - SHORT: Above the high of signal candle
- **Take Profit**: 1:1 Risk-to-Reward Ratio

### One Bullet Rule
Only the **FIRST** valid signal in each session is taken. Once a trade is executed in a session, no more trades are taken until the next session begins.

---

## Installation

### Prerequisites
- Python 3.8 or higher
- Required packages:
  ```bash
  pip install pandas numpy matplotlib
  ```

---

## Usage

### Running the Backtest

Simply execute the script:

```bash
python3 fvg_inversion_backtest.py
```

### Data Requirements

The script expects CSV files in the repository root with the naming convention:
- `2018 5m.csv`
- `2019 5m.csv`
- `2020 5m.csv`
- etc.

**CSV Format**: Semicolon-separated values with columns:
```
Column1;Column2;Column3;Column4;Column5;Column6;Column7
Date;Time;Open;High;Low;Close;Volume
```

Example:
```
01/01/2018;17:00:00;7503.739664;7511.940473;7499.63926;7511.3547;1451
```

---

## Output Files

After running the backtest, the following files are generated:

1. **`equity_curve.png`**: Visual representation of cumulative P&L and individual trade results
2. **`trades_log.csv`**: Detailed log of all trades with entry/exit information

---

## Performance Metrics

The script provides comprehensive performance analysis:

### Overall Statistics
- Total Trades
- Win Rate (%)
- Profit Factor
- Net Profit (points)
- Average Win/Loss

### Session Breakdown
- Performance metrics for London session
- Performance metrics for New York session

### Direction Breakdown
- LONG trades analysis
- SHORT trades analysis

---

## Script Structure

The backtesting engine is implemented as a class-based system:

```python
class FVGInversionBacktest:
    - load_data()           # Combine and process CSV files
    - detect_fvgs()         # Identify Fair Value Gaps
    - get_session()         # Determine trading session
    - run_backtest()        # Execute strategy logic
    - calculate_performance() # Generate metrics
    - plot_equity_curve()   # Create visualizations
    - export_trades()       # Save trade log
```

---

## Customization

You can modify the following parameters in the script:

- **Session times**: Adjust `london_start`, `london_end`, `ny_start`, `ny_end`
- **Risk-to-Reward ratio**: Modify the TP calculation in `run_backtest()`
- **Data directory**: Change `data_dir` in the initialization

---

## Example Output

```
============================================================
NQ FUTURES - FVG INVERSION STRATEGY BACKTESTER
============================================================
Strategy: First FVG Inversion with One-Bullet Rule
Sessions: London (01:00-04:00) & New York (08:30-11:00)
Risk Management: 1:1 RRR
============================================================

📊 OVERALL PERFORMANCE
------------------------------------------------------------
Total Trades:    3612
Winning Trades:  1393
Losing Trades:   2219
Win Rate:        38.57%
Profit Factor:   0.88
Net Profit:      -3392.10 points

📈 SESSION BREAKDOWN
------------------------------------------------------------
London Session:
  Total Trades:   1806
  Win Rate:       39.15%
  Profit Factor:  0.92
  Net Profit:     -484.68 points

New York Session:
  Total Trades:   1806
  Win Rate:       37.98%
  Profit Factor:  0.87
  Net Profit:     -2907.43 points
```

---

## Notes

- Data is assumed to be in Chicago Time (CT) - no timezone conversion is performed
- The script handles edge cases such as trades open at end of data
- All price data is validated and rows with missing values are dropped
- The backtesting loop properly manages state for session-based trading

---

## License

This is a professional backtesting tool for educational and research purposes.

---

## Author

Senior Quantitative Trader & Python Developer

Date: 2026-01-11
# FVG Inversion Backtesting System

A comprehensive backtesting system for NQ (Nasdaq 100) Futures using the Fair Value Gap (FVG) Inversion strategy on 1-minute data.

## Overview

This backtesting system implements a systematic approach to trading NQ Futures based on Fair Value Gap inversions during specific market sessions (London and New York killzones).

## Strategy Logic

### Fair Value Gap (FVG) Definitions

- **Bearish FVG**: Created when `Low[i-2] > High[i]`
  - Gap exists between `High[i]` and `Low[i-2]`
  
- **Bullish FVG**: Created when `High[i-2] < Low[i]`
  - Gap exists between `High[i-2]` and `Low[i]`

### Entry Signals (Inversion)

- **LONG Signal**: A Bearish FVG is created, and a later 1-minute candle closes **ABOVE** the top of that Bearish FVG
  
- **SHORT Signal**: A Bullish FVG is created, and a later 1-minute candle closes **BELOW** the bottom of that Bullish FVG

### Trading Sessions (Chicago Time)

- **London Killzone**: 01:00 - 04:00 CT
- **New York Killzone**: 08:30 - 11:00 CT

### The "One Bullet" Rule

- Take **ONLY the FIRST** valid inversion signal within each session
- If a trade is triggered in London, ignore all subsequent signals until New York session starts
- If a trade is triggered in New York, ignore all subsequent signals until the session ends
- The "trade taken" flag resets at the beginning of each new session

### Risk Management

- **Entry**: At the close of the 1-minute signal candle
- **Stop Loss**:
  - Long: Just below the low of the signal candle
  - Short: Just above the high of the signal candle
- **Take Profit**: 1:1 Risk-to-Reward ratio

## Files

### 1. `combine_data.py`
Combines individual year CSV files (2018-2024) into a single consolidated dataset.

**Usage:**
```bash
python combine_data.py
```

**Output:** `NQ_1min_2018_2024.csv`

### 2. `fvg_inversion_backtest.py`
Main backtesting engine that implements the FVG Inversion strategy.

**Usage:**
```bash
python fvg_inversion_backtest.py
```

**Outputs:**
- `fvg_inversion_trades.csv` - Detailed trade-by-trade results
- `fvg_inversion_equity_curve.png` - Cumulative equity curve visualization
- `fvg_inversion_session_comparison.png` - Session-by-session performance comparison

## Data Format

**Input CSV Files:**
- Files: `2018 1m.csv`, `2019 1m.csv`, ..., `2024 1m.csv`
- Delimiter: Semicolon (`;`)
- Columns: `Date;Time;Open;High;Low;Close;Volume`
- Date Format: `DD/MM/YYYY`
- Time Format: `HH:MM:SS`
- Timezone: Chicago Time (CT)

## Installation

### Requirements
```bash
pip install pandas numpy matplotlib
```

## Quick Start

1. **Combine the data files:**
   ```bash
   python combine_data.py
   ```

2. **Run the backtest:**
   ```bash
   python fvg_inversion_backtest.py
   ```

3. **Review the results:**
   - Check console output for performance metrics
   - Open `fvg_inversion_trades.csv` for detailed trade list
   - View `fvg_inversion_equity_curve.png` for equity visualization
   - View `fvg_inversion_session_comparison.png` for session breakdown

## Performance Metrics

The system reports the following metrics for Overall, London, and New York sessions:

- **Total Trades**: Number of trades executed
- **Win Rate**: Percentage of winning trades
- **Profit Factor**: Gross profit divided by gross loss
- **Net Profit**: Total profit/loss in points
- **Gross Profit**: Sum of all winning trades
- **Gross Loss**: Sum of all losing trades
- **Max Drawdown**: Maximum peak-to-trough decline

## Example Output

```
=============================================================
PERFORMANCE REPORT
=============================================================

--- OVERALL PERFORMANCE ---
Total Trades:    1234
Wins / Losses:   678 / 556
Win Rate:        54.94%
Profit Factor:   1.23
Net Profit:      $12345.67
Gross Profit:    $45678.90
Gross Loss:      $33333.23
Max Drawdown:    $5678.90

--- LONDON SESSION (01:00-04:00 CT) ---
Total Trades:    567
Wins / Losses:   312 / 255
Win Rate:        55.03%
...

--- NEW YORK SESSION (08:30-11:00 CT) ---
Total Trades:    667
Wins / Losses:   366 / 301
Win Rate:        54.87%
...
```

## Notes

- The strategy uses 1:1 risk-to-reward ratio for all trades
- Each session follows the "One Bullet" rule strictly
- Data is assumed to be in Chicago Time (CT)
- Stop loss and take profit are based on the signal candle's high/low

## License

This is a backtesting tool for educational and research purposes.

## Author

Created for NQ Futures backtesting analysis.

# Backtest-Trading

## NQ Futures Backtesting Strategies

This repository contains professional backtesting scripts for NQ (Nasdaq 100) Futures using advanced trading strategies with strict session management.

### Available Strategies

1. **FVG Inversion Strategy** (`fvg_inversion_backtest.py`)
   - Basic FVG detection and inversion
   - One-bullet rule per session
   
2. **Liquidity Sweep + FVG Inversion Strategy** (`liquidity_sweep_fvg_backtest.py`) ⭐ **NEW**
   - Advanced strategy combining liquidity sweeps with FVG inversions
   - Swing point detection using fractal logic
   - Requires 3-step confirmation process

---

## Strategy 1: FVG Inversion Strategy

### Overview

**Fair Value Gap (FVG) Inversion Strategy** with the "One Bullet Rule":
- **Bearish FVG**: Created when `Low[i-2] > High[i]`
- **Bullish FVG**: Created when `High[i-2] < Low[i]`
- **LONG Signal**: Price closes ABOVE the top of a Bearish FVG
- **SHORT Signal**: Price closes BELOW the bottom of a Bullish FVG

---

## Strategy 2: Liquidity Sweep + FVG Inversion Strategy ⭐

### Overview

An advanced 3-step strategy that requires:

1. **Swing Point Identification** (Liquidity Pools)
   - Swing Highs: Price high is higher than N bars before and after (N=5)
   - Swing Lows: Price low is lower than N bars before and after (N=5)

2. **Liquidity Sweep Detection**
   - **Buy-side Sweep** (for SHORT setups): Price breaks ABOVE a previous Swing High
   - **Sell-side Sweep** (for LONG setups): Price breaks BELOW a previous Swing Low

3. **FVG Formation & Inversion**
   - FVG must form AFTER the liquidity sweep (within 20 bars)
   - Then price must invert the FVG to trigger entry

### Entry Signals

**LONG Entry:**
1. Price sweeps below a Swing Low (sell-side liquidity sweep)
2. A Bearish FVG forms after the sweep
3. Price closes ABOVE the Bearish FVG top

**SHORT Entry:**
1. Price sweeps above a Swing High (buy-side liquidity sweep)
2. A Bullish FVG forms after the sweep
3. Price closes BELOW the Bullish FVG bottom

### Key Features

- ✅ Swing point detection using fractal logic (configurable lookback period)
- ✅ Buy-side and sell-side liquidity sweep detection
- ✅ FVG validation only after recent sweeps (within 20-bar window)
- ✅ Comprehensive sweep analytics and timing metrics
- ✅ Balanced LONG/SHORT trade generation

---

## Common Features (Both Strategies)

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

### Running the Backtests

**FVG Inversion Strategy:**
```bash
python3 fvg_inversion_backtest.py
```

**Liquidity Sweep + FVG Strategy:**
```bash
python3 liquidity_sweep_fvg_backtest.py
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

After running the backtests, the following files are generated:

**FVG Inversion Strategy:**
1. **`equity_curve.png`**: Visual representation of cumulative P&L and individual trade results
2. **`trades_log.csv`**: Detailed log of all trades with entry/exit information

**Liquidity Sweep + FVG Strategy:**
1. **`liquidity_sweep_equity_curve.png`**: Visual representation with sweep timing metrics
2. **`liquidity_sweep_trades_log.csv`**: Detailed log including sweep detection data and timing

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

### Sweep Analytics (Liquidity Sweep Strategy Only)
- Total sweeps detected (buy-side and sell-side)
- Average bars from sweep to entry
- Performance by sweep type

---

## Script Structure

### FVG Inversion Backtest

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

### Liquidity Sweep + FVG Backtest

```python
class LiquiditySweepFVGBacktest:
    - load_data()             # Combine and process CSV files
    - identify_swing_points() # Detect swing highs/lows using fractal logic
    - detect_fvgs()           # Identify Fair Value Gaps
    - get_session()           # Determine trading session
    - run_backtest()          # Execute advanced 3-step strategy logic
    - calculate_performance() # Generate comprehensive metrics
    - plot_equity_curve()     # Create visualizations
    - export_trades()         # Save detailed trade log
```

---

## Customization

### FVG Inversion Strategy

- **Session times**: Adjust `london_start`, `london_end`, `ny_start`, `ny_end`
- **Risk-to-Reward ratio**: Modify the TP calculation in `run_backtest()`
- **Data directory**: Change `data_dir` in the initialization

### Liquidity Sweep + FVG Strategy

All of the above, plus:
- **Swing lookback period**: Adjust `swing_lookback` parameter (default: 5 bars)
- **Max swing history**: Modify `max_swing_history` (default: 50 swings)
- **Sweep lookback window**: Change `sweep_lookback` (default: 20 bars)
- **Active FVG limit**: Adjust maxlen in deque initialization (default: 100)

---

## Example Output

### FVG Inversion Strategy

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

### Liquidity Sweep + FVG Strategy

```
======================================================================
NQ FUTURES - LIQUIDITY SWEEP + FVG INVERSION STRATEGY BACKTESTER
======================================================================
Strategy: Liquidity Sweep → FVG Formation → FVG Inversion
Sessions: London (01:00-04:00) & New York (08:30-11:00)
Risk Management: 1:1 RRR | One Bullet Per Session
======================================================================

📊 Sweep Detection Statistics:
  Total Sweeps Detected: 492918
  Buy-side Sweeps: 363545
  Sell-side Sweeps: 129373

📊 OVERALL PERFORMANCE
----------------------------------------------------------------------
Total Trades:              3557
Winning Trades:            1633
Losing Trades:             1924
Win Rate:                  45.91%
Profit Factor:             0.96
Net Profit:                -1535.21 points
Avg Bars Since Sweep:      21.5 bars

📈 SESSION BREAKDOWN
----------------------------------------------------------------------
London Session:
  Total Trades:   1783
  Win Rate:       44.87%
  Profit Factor:  0.89
  Net Profit:     -902.16 points

New York Session:
  Total Trades:   1774
  Win Rate:       46.96%
  Profit Factor:  0.98
  Net Profit:     -633.05 points

📉 DIRECTION BREAKDOWN
----------------------------------------------------------------------
LONG:  1034 trades (43.91% win rate)
SHORT: 2523 trades (46.73% win rate)
```

---

## Notes

- Data is assumed to be in Chicago Time (CT) - no timezone conversion is performed
- The scripts handle edge cases such as trades open at end of data
- All price data is validated and rows with missing values are dropped
- The backtesting loops properly manage state for session-based trading
- The Liquidity Sweep strategy includes optimizations for performance with large datasets
- Swing point detection requires N bars before and after, so first N bars cannot have swing points

---

## License

This is a professional backtesting tool for educational and research purposes.

---

## Author

Senior Quantitative Trader & Python Developer

Date: 2026-01-11
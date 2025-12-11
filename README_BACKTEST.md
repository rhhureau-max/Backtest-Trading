# NQ Futures Breakout Backtester

A comprehensive Python backtesting tool for NQ futures using oblique trendline breakout strategy with momentum confirmation.

## Overview

This tool backtests a breakout trading strategy on NQ (Nasdaq 100 E-mini) futures using historical 1-minute data from 2018-2025.

### Strategy Logic

**LONG Setup (Breakout above resistance in downtrend):**
1. Detect a downtrend by identifying at least 2 descending swing highs over a 30-bar lookback period
2. Draw a dynamic oblique resistance line connecting these swing highs
3. Wait for price to close above this resistance line
4. Confirm with momentum filter: the breakout candle must have a bullish body larger than the average of the previous 10 candles
5. Take Profit: First swing high of the downtrend (initial peak)

**SHORT Setup (Breakdown below support in uptrend):**
1. Detect an uptrend by identifying at least 2 ascending swing lows over a 30-bar lookback period
2. Draw a dynamic oblique support line connecting these swing lows
3. Wait for price to close below this support line
4. Confirm with momentum filter: the breakout candle must have a bearish body larger than the average of the previous 10 candles
5. Take Profit: First swing low of the uptrend (initial trough)

### Position Management

**Stop Loss Scenarios:**
- **SL 50%**: 50% retracement of the signal candle
- **SL 75%**: 75% retracement of the signal candle
- **SL 100%**: 100% retracement (candle extreme - low for LONG, high for SHORT)

**Time Filter:**
- Session 1: 02:00 to 05:00
- Session 2: 08:30 to 11:00

## Installation

### Requirements

```bash
pip install -r requirements.txt
```

Required packages:
- pandas >= 1.5.0
- numpy >= 1.21.0
- PyYAML >= 6.0
- matplotlib >= 3.5.0

## Data Format

The tool expects historical NQ futures data in CSV format with semicolon separator:

```
Column1;Column2;Column3;Column4;Column5;Column6;Column7
DD/MM/YYYY;HH:MM:SS;Open;High;Low;Close;Volume
```

Data files should be named:
- `{year} 1m.csv.zip` for compressed files (2018-2024)
- `{year} 1m.csv` for uncompressed files (2025)

## Usage

### Basic Usage

```bash
python backtest_breakout_nq.py
```

### With Custom Configuration

```bash
python backtest_breakout_nq.py --config my_config.yaml
```

## Configuration

Edit `config.yaml` to customize the backtesting parameters:

```yaml
# Swing Detection Parameters
swing_detection:
  lookback_period: 30  # Number of bars to look back for swing detection
  min_swing_points: 2  # Minimum swing points to draw trendline

# Momentum Filter
momentum:
  average_period: 10  # Number of periods for average body size calculation

# Stop Loss Levels (retracement of signal candle)
stop_loss_levels:
  - 0.50  # 50% retracement
  - 0.75  # 75% retracement
  - 1.00  # 100% retracement

# Trading Sessions (local time of the data)
trading_sessions:
  session_1:
    start: "02:00:00"
    end: "05:00:00"
  session_2:
    start: "08:30:00"
    end: "11:00:00"

# Data Configuration
data:
  start_year: 2018
  end_year: 2025
  data_directory: "."
```

## Output

The tool generates the following files in the `results/` directory:

### 1. `backtest_report.md`
Comprehensive performance report including:
- Overall performance metrics
- Performance by stop loss type
- Performance by direction (LONG/SHORT)
- Performance by trading session
- Performance by year
- Equity curve visualization

### 2. `trades_log.csv`
Detailed trade-by-trade log with columns:
- Entry_Time, Exit_Time
- Direction (LONG/SHORT)
- Entry_Price, Exit_Price
- Stop_Loss, Take_Profit
- SL_Type (SL_50, SL_75, SL_100)
- PnL (profit/loss in points)
- Result (WIN/LOSS/OPEN)
- Session, Year

### 3. `equity_curve.png`
Visual representation of cumulative P&L over time, separated by stop loss type.

## Performance Metrics

The backtest calculates the following metrics:

| Metric | Description |
|--------|-------------|
| **Win Rate** | Percentage of winning trades |
| **Risk/Reward Ratio** | Average win size / Average loss size |
| **Profit Factor** | Gross profit / Gross loss |
| **Maximum Drawdown** | Largest peak-to-trough decline |
| **Total P&L** | Sum of all trade profits and losses |

## File Structure

```
├── backtest_breakout_nq.py    # Main backtesting script
├── config.yaml                 # Configuration file
├── requirements.txt            # Python dependencies
├── README_BACKTEST.md          # This documentation
├── 2018 1m.csv.zip            # Historical data (compressed)
├── 2019 1m.csv.zip
├── ...
├── 2025 1m.csv                # Historical data (uncompressed)
└── results/                    # Output directory
    ├── backtest_report.md      # Performance report
    ├── trades_log.csv          # Trade log
    └── equity_curve.png        # Equity curve chart
```

## Notes

- The backtest processes over 3 million 1-minute bars spanning 2018-2025
- Each trade is simulated with bar-by-bar exit checking for accurate stop-loss and take-profit execution
- All times are in the local timezone of the data (as provided in the CSV files)
- The tool handles both compressed (.zip) and uncompressed (.csv) data files automatically

## Example Output

```
==============================================================
NQ Futures Breakout Backtester
==============================================================
Loading 2018 1m.csv.zip...
  Loaded 373920 rows for 2018
Loading 2019 1m.csv.zip...
  Loaded 372960 rows for 2019
...

Running backtest...
  Processing bar 100000/3500000 (2.9%)
  Processing bar 200000/3500000 (5.7%)
...

Backtest complete. Total trades: XXXX

==============================================================
BACKTEST COMPLETE
==============================================================

Total Trades: XXXX
Win Rate: XX.XX%
Profit Factor: X.XX
Total P&L: XXXX.XX points

Results saved to: results/
  - backtest_report.md
  - trades_log.csv
  - equity_curve.png
```

## License

This tool is provided for educational and research purposes.

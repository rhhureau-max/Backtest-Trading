# NQ Futures Backtesting System - London Session

A comprehensive backtesting system for NQ (Nasdaq 100) futures trading during the London session (08:00-12:00 Paris time) with three distinct strategies.

## Overview

This system implements and compares three different trading strategies:
- **Strategy A: Judas Swing** - Mean reversion strategy based on Asian range fakeouts
- **Strategy B: ORB Retest** - Opening range breakout with retest confirmation
- **Strategy C: HTF Trend Continuation** - Trend following with trailing stop using EMA(9)

## Features

- ✅ Automated data loading from CSV files (multiple timeframes)
- ✅ Proper timezone handling (Paris/CET)
- ✅ Spread integration (1.5 points per trade)
- ✅ Partial take profit handling
- ✅ One trade per day maximum (first valid signal)
- ✅ Comprehensive performance metrics
- ✅ Comparative analysis between strategies

## Installation

```bash
pip install -r requirements.txt
```

## Usage

Run the complete backtest:

```bash
python main.py
```

This will:
1. Load historical data from CSV files (2018-2025)
2. Run all three strategies
3. Generate performance reports
4. Save results to CSV files

## Output Files

- `strategy_comparison.csv` - Comparison metrics for all strategies
- `judas_swing_trades.csv` - Individual trades for Strategy A
- `orb_retest_trades.csv` - Individual trades for Strategy B
- `htf_trend_continuation_trades.csv` - Individual trades for Strategy C

## Project Structure

```
.
├── main.py                          # Entry point
├── config.py                        # Configuration settings
├── requirements.txt                 # Python dependencies
├── src/
│   ├── __init__.py
│   ├── data_loader.py              # CSV data loading utilities
│   ├── indicators.py               # Technical indicators (ATR, EMA, Fib)
│   ├── backtester.py               # Core backtesting engine
│   ├── performance.py              # Performance metrics calculation
│   ├── report.py                   # Report generation
│   └── strategies/
│       ├── __init__.py
│       ├── base_strategy.py        # Base strategy class
│       ├── judas_swing.py          # Strategy A implementation
│       ├── orb_retest.py           # Strategy B implementation
│       └── htf_trend.py            # Strategy C implementation
└── [CSV files]                      # Historical data files
```

## Strategy Details

### Strategy A: Judas Swing (Mean Reversion)

**Entry Logic:**
1. Calculate Asian Range (00:00-08:00) High and Low
2. Wait for price to break Asian High/Low
3. Enter when M5 candle closes back inside range (fakeout)

**Exit Logic:**
- Stop Loss: High/Low of manipulation wick (no ATR buffer)
- TP1 (50%): 50% retracement of Asian Range → Move SL to breakeven
- TP2 (50%): Opposite liquidity (Asian Low for short, High for long)

### Strategy B: ORB Retest (Expansion)

**Entry Logic:**
1. Define Opening Range Box (08:00-09:00) High and Low
2. Calculate Box Size in points
3. Wait for breakout after 09:00
4. Enter on retest of breakout level

**Exit Logic:**
- Stop Loss: Behind M15 breakout candle low/high
- TP1 (70%): 1x Box Size projection
- TP2 (30%): 2.5x Box Size projection

### Strategy C: HTF Trend Continuation

**Entry Logic:**
1. Determine daily trend from previous daily close
2. Calculate overnight impulse (previous close to 08:00)
3. Wait for retracement into OTE zone (62-79% Fibonacci)
4. Enter on M5 reversal candle in OTE zone

**Exit Logic:**
- Stop Loss: Below/Above Swing Low/High (Fib 0%)
- No fixed TP - Trailing stop using EMA(9) on M15
- Exit when M15 closes below/above EMA(9)

## Performance Metrics

The system calculates the following metrics:

- **Total Trades**: Number of trades executed
- **Win Rate**: Percentage of winning trades
- **Total PnL**: Total profit/loss in points
- **Average Win/Loss**: Average win and loss size
- **Profit Factor**: Gross profit / Gross loss
- **Maximum Drawdown**: Largest peak-to-trough decline
- **Sharpe Ratio**: Risk-adjusted return metric
- **Total Return**: Overall return in points

## KPI Recommendations

The system provides recommendations for validating whether trailing stops (Strategy C) are superior to fixed take profits:

1. **Sharpe Ratio Comparison** - Risk-adjusted performance
2. **Average Win Size** - Ability to capture larger moves
3. **Profit Factor** - Overall risk/reward management
4. **Win Rate vs. Reward** - Quality vs. quantity of wins
5. **Maximum Drawdown** - Capital protection
6. **Market Condition Analysis** - Performance in different regimes
7. **Trade Duration** - Holding period efficiency

## Configuration

Edit `config.py` to customize:

```python
# Trading Parameters
SPREAD_POINTS = 1.5
LONDON_SESSION_START = "08:00:00"
LONDON_SESSION_END = "12:00:00"

# Strategy Parameters
JUDAS_SWING_PARAMS = {...}
ORB_RETEST_PARAMS = {...}
HTF_TREND_PARAMS = {...}
```

## Data Format

CSV files should be in the following format:
```
Column1;Column2;Column3;Column4;Column5;Column6;Column7
01/01/2024;17:00:00;18244.57923;18248.331274;18238.951165;18241.631196;1308
```

Where columns are: Date;Time;Open;High;Low;Close;Volume (semicolon separated)

## Notes

- All times are in Paris timezone (CET/CEST)
- Only first valid signal per day is taken
- Spread of 1.5 points is deducted from each trade
- Partial take profits are properly handled in PnL calculations
- Strategies can be easily extended by inheriting from `BaseStrategy`

## License

MIT License

## Author

Created for NQ Futures backtesting analysis

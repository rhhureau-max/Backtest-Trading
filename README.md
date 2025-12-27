# Backtest-Trading

## Overview

This repository contains historical trading data for Nasdaq 100 (NQ) futures and algorithmic trading strategy implementations for backtesting.

## Data

The repository includes historical OHLCV data for NQ futures from 2018 to 2025 in multiple timeframes:
- 1 minute
- 5 minutes
- 15 minutes
- 1 hour
- 4 hours
- Daily

Data format: CSV files with semicolon separator (Date;Time;Open;High;Low;Close;Volume)

## London Killzone Trading Strategies

This repository now includes a complete implementation of three advanced trading strategies specifically designed for the **London Killzone** session (08:00-12:00 Paris time).

### Strategies Implemented

1. **Strategy A: Judas Swing** - Liquidity hunt reversal strategy that captures false breakouts of the Asian range
2. **Strategy B: ORB Retest** - Opening Range Breakout retest strategy for continuation moves
3. **Strategy C: HTF Continuation** - Higher timeframe Fibonacci OTE strategy for trend following

### Key Features

- ✅ One trade per day maximum (risk management)
- ✅ Precise entry, stop loss, and take profit rules
- ✅ Support for multiple timeframes
- ✅ Timezone management (Paris time)
- ✅ Comprehensive backtesting engine
- ✅ Performance metrics and reporting
- ✅ Strategy comparison table

### Quick Start

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the example backtest:
```bash
python backtest_example.py
```

3. Run validation tests:
```bash
python test_strategies.py
```

### Documentation

**📊 REAL BACKTEST RESULTS:** See [RESULTATS_REELS_NQ.md](RESULTATS_REELS_NQ.md) for complete results on 7+ years of NQ data (2018-2025)

For complete documentation, see [LONDON_KILLZONE_STRATEGIES.md](LONDON_KILLZONE_STRATEGIES.md)

### Real Results Summary (2018-2025)

Backtest performed on **554,518 candles** over **2,449 trading days**:

| Strategy | Trades | Win Rate | Profit Factor | P&L (points) | Status |
|----------|--------|----------|---------------|--------------|---------|
| **A: Judas Swing** | 1,694 | 21.0% | **1.11** | **+4,125** | ✅ Profitable |
| B: ORB Retest | 1,800 | 20.2% | 0.96 | -1,506 | ❌ Needs optimization |
| C: HTF Continuation | 481 | 44.1% | 0.81 | -6,693 | ❌ Needs revision |

**Key Finding:** Only Strategy A (Judas Swing) is profitable over the long term with a Profit Factor > 1.

⚠️ **Important:** Results are before slippage and commissions. See full analysis in [RESULTATS_REELS_NQ.md](RESULTATS_REELS_NQ.md)

### Files

**Core Implementation:**
- `london_killzone_strategies.py` - Main strategy implementation module
- `backtest_example.py` - Example usage script
- `test_strategies.py` - Validation tests

**Real Backtest Results:**
- `real_backtest_results.py` - Script to run full backtest on all data
- `RESULTATS_REELS_NQ.md` - Complete analysis of real results (French)
- `real_results_strategy_a.csv` - All 1,694 trades from Strategy A
- `real_results_strategy_b.csv` - All 1,800 trades from Strategy B
- `real_results_strategy_c.csv` - All 481 trades from Strategy C
- `real_results_comparison.csv` - Summary comparison

**Documentation:**
- `LONDON_KILLZONE_STRATEGIES.md` - Complete strategy documentation (French)
- `DATA_INCONSISTENCIES_GUIDE.md` - Data quality guide (French)
- `IMPLEMENTATION_SUMMARY.md` - Technical summary (English)
- `data_cleaning.py` - Interactive data cleaning utility
- `requirements.txt` - Python dependencies

### Usage Example

```python
from london_killzone_strategies import (
    DataLoader,
    StrategyA_JudasSwing,
    BacktestEngine
)

# Load data
df = DataLoader.load_csv("2024 5m.csv")

# Initialize strategy and engine
strategy = StrategyA_JudasSwing(points_offset=5.0, risk_reward=3.0)
engine = BacktestEngine(df)

# Run backtest
trades = engine.run_strategy(strategy)

# Generate performance report
performance = engine.generate_performance_report(trades, "Judas Swing")
print(performance)
```

## License

This project is provided "as-is" for educational purposes. Trading involves significant risk.
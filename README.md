# Backtest-Trading

## Judas Swing Analysis - NQ Futures

This repository contains a comprehensive statistical analysis of Judas Swing patterns in Nasdaq Futures (NQ) from 2018 to 2025.

### What is a Judas Swing?

A Judas Swing is a manipulation of Tokyo session liquidity during the London session, characterized by:
- **Bullish Manipulation**: Break above Tokyo High (19:00-00:00) during London session (01:00-05:00)
- **Bearish Manipulation**: Break below Tokyo Low during London session

### Quick Start

```bash
# Install dependencies
pip install pandas numpy

# Run main analysis
python3 judas_swing_analysis.py

# Run extended analysis (yearly, monthly breakdowns)
python3 judas_swing_extended_analysis.py

# Run reversion analysis (post-manipulation behavior)
python3 judas_swing_reversion_analysis.py

# Run full strategy backtesting (NEW)
python3 strategy_backtest.py
```

### Key Results - Manipulation Detection

- **76.24% of trading days** exhibit Judas Swing patterns
- **1,867 swings detected** out of 2,449 days analyzed
- **Mean amplitude**: 47.07 NQ points
- **94.64% probability** that a manipulation exceeds 5 points
- **Bearish manipulations** tend to be more aggressive (51.88 pts) than bullish (43.10 pts)

### Key Results - Post-Manipulation Reversion

- **78.52% reversion rate** to Tokyo Equilibrium (median: 3.25 hours)
- **65.35% reversal rate** to Opposing Liquidity (median: 5.00 hours)
- **Bearish swings** show slightly faster and more frequent reversions
- **High consistency** across both bullish and bearish manipulations

### Key Results - Strategy Backtesting (NEW)

**Strategy B (Aggressive Turtle Soup) - Scenario 3 (Best Performer):**
- **Total P&L**: $89.57 over 7 years
- **Win Rate**: 47.90%
- **Profit Factor**: 1.05 (positive edge)
- **Trade Frequency**: ~24 trades/year (~2/month)
- **Expectancy**: $0.54 per trade
- **Max Drawdown**: -$495.34

Strategy A (Conservative ICT) generated only 1 trade in 7 years (too restrictive).

### Documentation

**Statistical Analysis:**
- **[JUDAS_SWING_ANALYSIS.md](JUDAS_SWING_ANALYSIS.md)** - Complete methodology and detailed results
- **[REVERSION_ANALYSIS.md](REVERSION_ANALYSIS.md)** - Post-manipulation reversion study
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Summary statistics and quick reference

**Backtesting:**
- **[BACKTEST_RESULTS.md](BACKTEST_RESULTS.md)** - Full strategy performance analysis (NEW)
- **[backtest_results.csv](backtest_results.csv)** - All 505 trade records (NEW)

**Data Files:**
- **[judas_swing_results.csv](judas_swing_results.csv)** - Raw data of all 1,867 detected swings
- **[judas_swing_reversion_results.csv](judas_swing_reversion_results.csv)** - Reversion data with timestamps

### Files

**Analysis Scripts:**
- `judas_swing_analysis.py` - Main manipulation detection script
- `judas_swing_extended_analysis.py` - Additional statistical insights
- `judas_swing_reversion_analysis.py` - Post-manipulation reversion analysis

**Backtesting:**
- `strategy_backtest.py` - Full strategy backtesting engine (NEW)

**Results:**
- `judas_swing_results.csv` - Detailed manipulation results
- `judas_swing_reversion_results.csv` - Detailed reversion results
- `backtest_results.csv` - All trade execution records (NEW)

### Data

The analysis uses NQ futures data from 2018-2025 in 15-minute timeframe:
- 2018-2025 15m.csv files (semicolon-delimited)
- No timezone conversions applied
- Timestamps used exactly as provided

---

*Analysis performed on 2025-12-23 | Data: 184,877 bars from 2018-01-01 to 2025-11-11*
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

# Run full strategy backtesting (M15 timeframe)
python3 strategy_backtest.py

# Run IFVG strategy backtesting (M1 & M5 timeframes) - NEW
python3 ifvg_backtest.py
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

### Key Results - Strategy Backtesting

**IFVG Inversion Strategy (M1) - BEST PERFORMER:** (NEW)
- **Total P&L**: $6,760.81 over 7 years
- **Win Rate**: 79.86%
- **Profit Factor**: 24.24 (exceptional edge)
- **Trade Frequency**: ~106 trades/year (~9/month)
- **Expectancy**: $9.14 per trade
- **Max Drawdown**: -$26.88
- **Avg R:R**: 6.11:1

**IFVG Inversion Strategy (M5):**
- **Total P&L**: $3,067.27
- **Win Rate**: 73.06%
- **Profit Factor**: 9.97
- **Expectancy**: $6.61 per trade

**Strategy B (Turtle Soup SFP) - M15:**
- Total P&L: $89.57
- Win Rate: 47.90%
- Profit Factor: 1.05

### Documentation

**Statistical Analysis:**
- **[JUDAS_SWING_ANALYSIS.md](JUDAS_SWING_ANALYSIS.md)** - Complete methodology and detailed results
- **[REVERSION_ANALYSIS.md](REVERSION_ANALYSIS.md)** - Post-manipulation reversion study
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Summary statistics and quick reference

**Strategy Backtesting:**
- **[IFVG_BACKTEST_RESULTS.md](IFVG_BACKTEST_RESULTS.md)** - IFVG strategy analysis (M1 & M5) (NEW)
- **[BACKTEST_RESULTS.md](BACKTEST_RESULTS.md)** - ICT & Turtle Soup strategies (M15)
- **[ifvg_backtest_1m.csv](ifvg_backtest_1m.csv)** - 2,220 IFVG trade records (NEW)
- **[ifvg_backtest_5m.csv](ifvg_backtest_5m.csv)** - 1,392 IFVG trade records (NEW)
- **[backtest_results.csv](backtest_results.csv)** - 505 M15 strategy trades

**Data Files:**
- **[judas_swing_results.csv](judas_swing_results.csv)** - Raw data of all 1,867 detected swings
- **[judas_swing_reversion_results.csv](judas_swing_reversion_results.csv)** - Reversion data with timestamps

### Files

**Analysis Scripts:**
- `judas_swing_analysis.py` - Main manipulation detection script
- `judas_swing_extended_analysis.py` - Additional statistical insights
- `judas_swing_reversion_analysis.py` - Post-manipulation reversion analysis

**Backtesting Engines:**
- `ifvg_backtest.py` - IFVG inversion strategy (M1 & M5) (NEW)
- `strategy_backtest.py` - ICT & Turtle Soup strategies (M15)

**Results:**
- `judas_swing_results.csv` - Detailed manipulation results (1,867 swings)
- `judas_swing_reversion_results.csv` - Detailed reversion results
- `backtest_results.csv` - M15 strategy trade records (505 trades)
- `ifvg_backtest_1m.csv` - M1 IFVG trade records (2,220 trades) (NEW)
- `ifvg_backtest_5m.csv` - M5 IFVG trade records (1,392 trades) (NEW)

### Data

The analysis uses NQ futures data from 2018-2025:
- **M15**: 184,877 bars (15-minute timeframe)
- **M5**: 554,510 bars (5-minute timeframe) (NEW)
- **M1**: 2,771,411 bars (1-minute timeframe) (NEW)
- Data format: semicolon-delimited CSV files
- No timezone conversions applied
- Timestamps used exactly as provided

---

*Analysis performed on 2025-12-23 | Data: 184,877 bars from 2018-01-01 to 2025-11-11*
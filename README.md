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

**ONLY ONE VIABLE STRATEGY FOUND:**

**IFVG M1 - Scenario A (100% at Equilibrium) - ONLY PROFITABLE STRATEGY:**
- **Total P&L**: +$10,087.85 over 7 years (~$1,441/year)
- **Win Rate**: 67.25% (NOT 79.86% - previous error corrected)
- **Profit Factor**: 1.02 (thin but positive edge)
- **Trade Frequency**: ~238 trades/year (~20/month)
- **Expectancy**: $6.05 per trade
- **Average Win**: $477.86 | **Average Loss**: -$962.62

**All Other Strategies UNPROFITABLE:**
- IFVG M1 - Scenario B (Opposing): -$518,608 (6.81% win rate)
- IFVG M1 - Scenario C (50/50): -$256,315 (63.65% win rate)
- IFVG M5 - All scenarios: Unprofitable
- Turtle Soup M15 - Scenario 3: +$89.57 (modest profit)

**Critical Finding**: Targeting Tokyo Equilibrium is viable. Targeting Opposing Liquidity causes massive losses despite 65% eventual hit rate (price hits stop loss first).

### Documentation

**Statistical Analysis:**
- **[JUDAS_SWING_ANALYSIS.md](JUDAS_SWING_ANALYSIS.md)** - Complete methodology and detailed results
- **[REVERSION_ANALYSIS.md](REVERSION_ANALYSIS.md)** - Post-manipulation reversion study
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Summary statistics and quick reference

**Strategy Backtesting:**
- **[IFVG_BACKTEST_RESULTS.md](IFVG_BACKTEST_RESULTS.md)** - IFVG strategy with CORRECTED scenario-specific results (M1 & M5)
- **[BACKTEST_RESULTS.md](BACKTEST_RESULTS.md)** - ICT & Turtle Soup strategies (M15)
- **[ifvg_backtest_1m.csv](ifvg_backtest_1m.csv)** - 3,921 IFVG trade records (all scenarios)
- **[ifvg_backtest_5m.csv](ifvg_backtest_5m.csv)** - 3,370 IFVG trade records (all scenarios)
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
- `ifvg_backtest.py` - IFVG inversion strategy with proper scenario separation (M1 & M5)
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
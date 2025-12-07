# Backtest-Trading

## NQ (Nasdaq) Trading Strategy Backtest

A comprehensive Python backtesting framework for an NQ futures trading strategy based on Tokyo Session reference levels, London Killzone execution, and Fair Value Gap (FVG) inversions.

## 🆕 Matrix Backtest (Recommended)

**NEW**: Matrix analysis comparing 4 Stop Loss types × 5 Take Profit types = 20 combinations!

```bash
# Run matrix backtest
python nq_matrix_backtest.py
```

### 🏆 Best Result: SL3 + TP1
- **Win Rate**: 64.46%
- **Net Profit**: +557.68 points
- **Max Drawdown**: Only 5 consecutive losses
- **Strategy**: Aggressive stop (signal candle) with 1:1 RR target

See [MATRIX_BACKTEST_README.md](MATRIX_BACKTEST_README.md) for complete analysis.

---

## Original Backtest

### Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run original backtest
python nq_backtest_strategy.py
```

### Features

✅ **7+ Years of Historical Data** (2018-2025)  
✅ **1,674 Trades Analyzed** across 2,449 trading days  
✅ **Matrix Analysis**: 4 SL × 5 TP = 20 combinations  
✅ **Detailed Performance Metrics** including win rates, drawdown, and profitability  
✅ **Complete Trade Export** to CSV for further analysis  
✅ **Optimized Processing** with vectorized operations  

### Strategy Overview

- **Reference Session**: Tokyo (19:00-23:00 previous day)
- **Trading Session**: London Killzone (01:00-04:00 current day)
- **Entry Signal**: FVG inversion after Tokyo level sweep
- **Risk Management**: 4 different stop loss strategies
- **Multiple TPs**: 1R, 1.5R, 2R, Tokyo Range, Tokyo EQ

### Matrix Results Summary (Best Combinations)

| SL Type | TP Type | Win Rate | Net Profit (pts) | Max DD |
|---------|---------|----------|------------------|--------|
| **SL3** | **1R** | **64.46%** | **+557.68** ✅ | **5** |
| SL1 | EQ | 70.58% | -1,181.14 | 5 |
| SL3 | 1.5R | 51.48% | -238.21 | 9 |

**SL Types:**
- SL1: Swing Extreme (Conservative)
- SL2: FVG Border (Technical)
- SL3: Signal Candle (Aggressive) ⭐
- SL4: Mean Threshold (Institutional)

### Documentation

- [MATRIX_BACKTEST_README.md](MATRIX_BACKTEST_README.md) - Complete matrix analysis
- [BACKTEST_DOCUMENTATION.md](BACKTEST_DOCUMENTATION.md) - Original strategy details
- [QUICK_START.md](QUICK_START.md) - Quick reference guide

### Output Files

- **Console**: Comprehensive performance summary
- **backtest_trades.csv**: Detailed trade-by-trade results

### Requirements

- Python 3.7+
- pandas
- numpy

### Data Format

5-minute NQ futures data in CSV format with semicolon delimiter:
```
Date;Time;Open;High;Low;Close;Volume
01/01/2018;17:00:00;7503.74;7511.94;7499.64;7511.35;1451
```

### Author

Created for quantitative trading research and educational purposes.
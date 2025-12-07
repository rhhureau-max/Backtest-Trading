# # Backtest-Trading

## NQ (Nasdaq) Trading Strategy Backtest

A comprehensive Python backtesting framework for an NQ futures trading strategy based on Tokyo Session reference levels, London Killzone execution, and Fair Value Gap (FVG) inversions.

### Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run backtest
python nq_backtest_strategy.py
```

### Features

✅ **7+ Years of Historical Data** (2018-2025)  
✅ **1,674 Trades Analyzed** across 2,449 trading days  
✅ **5 Take Profit Strategies** evaluated simultaneously  
✅ **Detailed Performance Metrics** including win rates, drawdown, and profitability  
✅ **Complete Trade Export** to CSV for further analysis  
✅ **Optimized Processing** with vectorized operations  

### Strategy Overview

- **Reference Session**: Tokyo (19:00-23:00 previous day)
- **Trading Session**: London Killzone (01:00-04:00 current day)
- **Entry Signal**: FVG inversion after Tokyo level sweep
- **Risk Management**: Dynamic stop loss based on sweep extremes
- **Multiple TPs**: 1R, 1.5R, 2R, Tokyo Range, Tokyo EQ

### Results Summary

| Take Profit | Win Rate | Net R | Max DD |
|-------------|----------|-------|--------|
| TP1 (1R) | 39.37% | -356.00R | 12 |
| TP2 (1.5R) | 32.08% | -331.50R | 16 |
| TP3 (2R) | 27.42% | -297.00R | 16 |
| TP4 (Tokyo Range) | 30.70% | -198.71R | 15 |
| TP5 (Tokyo EQ) | 59.20% | -29.39R | 7 |

### Documentation

For complete documentation, see [BACKTEST_DOCUMENTATION.md](BACKTEST_DOCUMENTATION.md)

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
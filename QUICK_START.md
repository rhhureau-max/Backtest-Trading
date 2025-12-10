# Quick Start Guide - NQ Backtest

## Run the Backtest

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the backtest
python nq_backtest_strategy.py
```

## What It Does

The script analyzes **7+ years** of NQ 5-minute data (2018-2025) to backtest a trading strategy:

1. **Identifies Tokyo Session levels** (19:00-23:00 previous day)
2. **Finds sweep setups** during London Killzone (01:00-04:00)
3. **Detects Fair Value Gaps** and entry signals
4. **Simulates trades** with multiple take profit targets
5. **Generates comprehensive statistics** and exports results

## Expected Output

### Console Output
- Progress updates every 100 days
- Performance summary table
- Detailed statistics by TP type
- Win rates, profitability, drawdown metrics

### File Output
- `backtest_trades.csv` - All 1,674 trades with complete details

## Results at a Glance

Based on the completed backtest:

- **Total Trades**: 1,674
- **Date Range**: Jan 2018 - Nov 2025
- **Best Win Rate**: 59.20% (TP5 - Tokyo EQ)
- **Best Drawdown**: 7 consecutive losses (TP5)
- **Long/Short Split**: 45.7% / 54.3%

## Next Steps

1. Review `BACKTEST_DOCUMENTATION.md` for full strategy details
2. Analyze `backtest_trades.csv` to identify patterns
3. Consider additional filters or optimizations
4. Test parameter variations

## Support

For detailed information:
- Strategy logic: See `BACKTEST_DOCUMENTATION.md`
- Code structure: See inline comments in `nq_backtest_strategy.py`
- Repository info: See `README.md`

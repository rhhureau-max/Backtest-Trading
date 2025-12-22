# Backtest-Trading

## 🎯 IFVG Strategy Backtest (NEW!)

This repository now includes a complete **IFVG (Inversion Fair Value Gap)** backtesting system based on Smart Money Concepts for the NQ (Nasdaq 100).

### Quick Start
```bash
# Install dependencies
pip install pandas numpy matplotlib

# Run the backtest
python backtest_ifvg_strategy.py
```

### Results Summary
- **Period:** 2018-2025 (7 years)
- **Total Trades:** 4,828
- **Win Rate:** 34.49%
- **Profit Factor:** 1.02
- **Total Return:** 1.45%
- **Max Drawdown:** 3.54%

### Documentation
- 📖 **[QUICKSTART.md](QUICKSTART.md)** - Get started in 3 steps
- 📚 **[IFVG_BACKTEST_README.md](IFVG_BACKTEST_README.md)** - Complete strategy documentation (French)
- 📊 **[EXAMPLE_OUTPUT.md](EXAMPLE_OUTPUT.md)** - Detailed results and analysis

### Output Files
- `backtest_ifvg_strategy.py` - Complete Python backtest script
- `equity_curve.png` - Visual performance chart
- `trade_log.csv` - Detailed log of all trades

---

## Data Files

This repository contains historical price data for:
- **NQ (Nasdaq 100)**: 2018-2025 in multiple timeframes (1m, 5m, 15m, 1H, 4H, 1D)
- **ES (S&P 500)**: 2018-2025 in multiple timeframes

All data files use semicolon (`;`) as delimiter with format: Date;Time;Open;High;Low;Close;Volume
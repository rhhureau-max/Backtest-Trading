# Backtest-Trading

## FVG (Fair Value Gap) Trading Strategy Backtesting System

A comprehensive backtesting system for analyzing Fair Value Gap trading strategies across 8 years of historical data (2018-2025).

### Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the backtest
python3 fvg_backtest.py

# Run additional analysis
python3 analyze_results.py
```

### Features

- ✅ Automatic FVG detection at 8:30 AM
- ✅ Tests 432 configurations (3 timeframes × 2 stop-loss types × 9 RR ratios × 8 years)
- ✅ Comprehensive statistical analysis and visualizations
- ✅ Exports detailed results to CSV
- ✅ Additional analysis tools for deeper insights

### Documentation

- **[Quick Start Guide](QUICK_START.md)** - Get started in 5 minutes
- **[Full Documentation](FVG_BACKTEST_README.md)** - Complete technical reference
- **[Implementation Summary](IMPLEMENTATION_SUMMARY.md)** - Project overview and results

### Results

All analysis results are saved in the `results/` directory:
- Summary statistics for all configurations
- Individual trade details (7,983+ trades)
- Visualization charts and graphs
- Filtered result exports

### Key Results

**Best Configuration:** 2024 | 15m timeframe | Edge stop-loss | RR 2.0
- Win Rate: 45.45%
- Profit Factor: 3.59

For detailed results and interpretation, see the generated reports in `results/` directory.

---

**Disclaimer:** This system is for educational and research purposes only. Past performance does not guarantee future results.
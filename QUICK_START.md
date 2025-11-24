# Quick Start Guide - FVG Backtesting System

## Installation & Setup (5 minutes)

### 1. Install Required Packages
```bash
pip install pandas numpy matplotlib seaborn tabulate
```

### 2. Verify Data Files
Ensure your CSV files are present in the repository root:
- `2018 1m.csv`, `2018 5m.csv`, `2018 15m.csv`
- `2019 1m.csv`, `2019 5m.csv`, `2019 15m.csv`
- ... (through 2025)

**Note**: If 1-minute files are zipped (.zip), they will be automatically extracted.

### 3. Run the Backtest
```bash
python3 fvg_backtest.py
```

**Expected Runtime**: 5-10 minutes for full analysis (2018-2025, all configurations)

## What the Script Does

The script automatically:
1. ✅ Loads all historical data (2018-2025)
2. ✅ Detects Fair Value Gaps at 8:30 AM each trading day
3. ✅ Backtests **432 configurations**:
   - 8 years × 3 timeframes × 2 stop-loss types × 9 RR ratios
4. ✅ Generates comprehensive statistics
5. ✅ Creates visualizations
6. ✅ Exports results to CSV

## Output Files

### Results Directory (`results/`)

**CSV Files:**
- `backtest_results_summary.csv` - Statistical summary for each configuration
- `all_trades_detailed.csv` - Every individual trade with entry/exit details

**Visualizations:**
- `win_rate_by_rr_ratio.png` - Win rate trends
- `profit_factor_by_rr_ratio.png` - Profitability analysis
- `win_rate_heatmaps.png` - Configuration heatmaps
- `trades_by_year.png` - Trading frequency over time
- `stop_loss_comparison.png` - Stop-loss strategy comparison

## Understanding Your Results

### Key Findings Summary

The console output shows 5 summary tables:

1. **Overall Performance** - Aggregated by timeframe and stop-loss type
2. **RR Ratio Performance** - How each risk-reward ratio performed
3. **Yearly Performance** - Performance trends over time
4. **Top 10 Configurations** - Best performing setups
5. **Detailed Win Rate Matrix** - Win rates for all combinations

### Quick Interpretation Guide

**Profit Factor > 1.0** = Profitable strategy  
**Profit Factor < 1.0** = Losing strategy  
**Profit Factor = 1.0** = Break-even

**Win Rate Guidelines:**
- 1.5 RR: Need ~40%+ win rate
- 2.0 RR: Need ~33%+ win rate
- 3.0 RR: Need ~25%+ win rate

### Example Results Interpretation

From the output, you might see:
```
15m timeframe | edge SL | 2.0 RR | 45% win rate | 3.59 profit factor
```

This means:
- Using 15-minute charts
- Stop-loss at edge of FVG
- 2:1 risk-reward ratio
- Won 45% of trades
- Made 3.59× more profit than losses (excellent!)

## Customization

### Quick Customizations

Edit `fvg_backtest.py` to customize:

**Test Different Years:**
```python
self.years = list(range(2020, 2024))  # Only 2020-2023
```

**Test Different RR Ratios:**
```python
self.rr_ratios = [2, 3, 4, 5]  # Focus on higher RR ratios
```

**Test Single Timeframe:**
```python
self.timeframes = ['5m']  # Only 5-minute charts
```

## Common Use Cases

### 1. Find the Best Configuration
Look at "TOP 10 BEST PERFORMING CONFIGURATIONS" in console output.
Filter for configurations with at least 20-30 trades for statistical significance.

### 2. Analyze Specific Year
Open `backtest_results_summary.csv` and filter by year column.

### 3. Compare Stop-Loss Strategies
Check `stop_loss_comparison.png` visualization.

### 4. Examine Individual Trades
Open `all_trades_detailed.csv` to see every trade's details:
- Entry/exit prices
- Stop-loss and take-profit levels
- P&L for each trade
- Trade outcome (win/loss)

## Tips for Success

✅ **Do:**
- Run full backtest first to see all results
- Look for consistent performance across multiple years
- Prefer configurations with sufficient trade samples (30+)
- Consider both win rate AND profit factor
- Review the visualizations for patterns

❌ **Don't:**
- Cherry-pick best single-year results
- Ignore configurations with too few trades (<10)
- Focus only on win rate (profit factor matters more)
- Assume past performance guarantees future results

## Troubleshooting

### Script Takes Too Long
The script uses caching for efficiency. First-time loading of large files (especially 1m data) takes time. Subsequent runs are faster.

### Memory Issues
If running on low-memory system:
1. Test fewer years at once
2. Comment out 1m timeframe (uses most memory)

### Missing FVGs
Ensure your data:
- Contains 8:30 AM timestamps
- Has correct date/time format
- Covers full trading days

## Next Steps

1. ✅ Review console output and summary tables
2. ✅ Open visualizations in `results/` directory
3. ✅ Analyze `backtest_results_summary.csv` in spreadsheet
4. ✅ Examine detailed trades in `all_trades_detailed.csv`
5. ✅ Identify promising configurations for further analysis
6. ✅ Consider forward-testing on out-of-sample data

## Support & Documentation

- Full documentation: `FVG_BACKTEST_README.md`
- Technical details: See docstrings in `fvg_backtest.py`
- Strategy explanation: `FVG_BACKTEST_README.md` Strategy Logic section

---

**Remember**: This is for educational/research purposes only. Always practice proper risk management in live trading.

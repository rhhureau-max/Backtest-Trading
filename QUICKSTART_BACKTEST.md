# Quick Start Guide - NQ IVFG Backtester

## 🚀 Quick Start (3 Steps)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

Or manually:
```bash
pip install pandas numpy matplotlib
```

### 2. Run the Backtest
```bash
python3 backtest_nq_ivfg.py
```

### 3. View Results
Results are saved in the `results/` directory:
- Open `backtest_report.txt` for detailed metrics
- View `comparison.csv` for mode comparison
- Check PNG files for visualizations

## 📊 What You'll Get

### Console Output
The script will show:
- Data loading progress (8 years × 2 timeframes)
- FVG detection results (~110,000 FVGs)
- Backtest progress for each mode
- Summary statistics

### Expected Runtime
- **Total Time**: ~5-10 minutes
- **Per Mode**: ~2-3 minutes
- **Data Size**: 554,518 bars (5-minute data)

### Generated Files (15 total)

#### Reports (3 files)
1. `backtest_report.txt` - Detailed text report
2. `comparison.csv` - Mode comparison table
3. `trades_*.csv` - Trade logs (3 files)

#### Charts (12 files)
- **Equity curves** (3): Capital over time
- **Drawdown charts** (3): Risk visualization
- **Trade distribution** (3): 6-panel analysis
- **Monthly returns** (3): Heatmap by year/month

## 🎯 Understanding the Results

### Current Performance (2018-2025)
All three modes show **negative returns** - the strategy needs optimization:

| Mode | Trades | Win Rate | Profit Factor | Return |
|------|--------|----------|---------------|--------|
| **Mode A** (Structural) | 4,544 | 30.90% | 0.47 | -29.54% |
| **Mode B** (Fixed) | 3,327 | 32.52% | 0.63 | -21.58% |
| **Mode C** (ATR) | 3,861 | 32.71% | 0.56 | -26.15% |

**Mode B (Fixed Points)** performs best with:
- ✅ Highest win rate (32.52%)
- ✅ Lowest drawdown (-21.63%)
- ✅ Best profit factor (0.63)
- ✅ Smallest loss (-21.58%)

### Key Insights

#### What's Working ✅
- Consistent trade generation (~400-500 trades/year)
- Win rates stable across years (~30-33%)
- All London Killzone hours utilized
- Multi-timeframe trend filter operational

#### What Needs Improvement ❌
- **Win Rate**: 30-33% (target: >50%)
- **Profit Factor**: 0.47-0.63 (target: >1.5)
- **Negative Edge**: Losses exceed wins
- **Drawdown**: 21-30% (high risk)

## 🔧 Customization

### Quick Parameter Changes

Edit `backtest_nq_ivfg.py` and modify the `Config` class:

```python
class Config:
    # Try different time windows
    SESSION_START_HOUR = 1   # Change to 0, 2, etc.
    SESSION_END_HOUR = 5     # Change to 4, 6, etc.
    
    # Adjust FVG memory
    FVG_LOOKBACK = 12        # Try 8, 16, 20
    
    # Mode A: Structural
    SL_BUFFER_TICKS = 5      # Try 3, 7, 10
    RR_RATIO = 2.0           # Try 1.5, 2.5, 3.0
    
    # Mode B: Fixed Points
    SL_POINTS_FIXED = 20     # Try 15, 25, 30
    TP_POINTS_FIXED = 40     # Try 30, 50, 60
    
    # Mode C: ATR Based
    SL_ATR_MULT = 1.5        # Try 1.0, 2.0
    TP_ATR_MULT = 3.0        # Try 2.0, 4.0
```

### Common Optimization Tests

1. **Tighter Stops + Higher RR**
   ```python
   SL_BUFFER_TICKS = 3
   RR_RATIO = 3.0
   ```

2. **Wider Time Window**
   ```python
   SESSION_START_HOUR = 0
   SESSION_END_HOUR = 8
   ```

3. **Shorter FVG Memory**
   ```python
   FVG_LOOKBACK = 8
   ```

4. **ATR with Tighter Stops**
   ```python
   SL_ATR_MULT = 1.0
   TP_ATR_MULT = 2.5
   ```

## 📈 Reading the Charts

### Equity Curve
- **Upward trend**: Strategy making money
- **Downward trend**: Strategy losing money
- **Smooth line**: Consistent performance
- **Jagged line**: High volatility

### Drawdown Chart
- **Deeper valleys**: Larger losses
- **Wider valleys**: Longer recovery time
- **Flat at zero**: No drawdown (peak equity)

### Trade Distribution
- **P&L histogram**: Most trades should be profitable
- **Hour distribution**: Shows when strategy trades
- **Day of week**: Identifies best/worst days
- **Win/Loss split**: Compare long vs short performance

### Monthly Heatmap
- **Green cells**: Profitable months
- **Red cells**: Losing months
- **Pattern recognition**: Seasonal trends

## 🐛 Troubleshooting

### Script Fails to Start
```bash
# Check Python version (need 3.7+)
python3 --version

# Reinstall dependencies
pip install --upgrade pandas numpy matplotlib
```

### Missing Data Files
```
Error: 2023 5m.csv not found
```
**Solution**: Ensure all CSV files (2018-2025) are in the repository root.

### Memory Issues
```
MemoryError: Unable to allocate array
```
**Solution**: Process fewer years by modifying the `main()` function:
```python
# Change this line
years = [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]

# To this (test with recent data only)
years = [2024, 2025]
```

### Slow Execution
This is normal! Processing 554,518 bars takes time:
- Mode A: ~2-3 minutes
- Mode B: ~2-3 minutes  
- Mode C: ~2-3 minutes
- **Total**: ~10 minutes for all modes

## 💡 Next Steps

### 1. Analyze Current Results
- Review `backtest_report.txt` thoroughly
- Study the trade distribution charts
- Identify losing patterns in trade logs

### 2. Optimize Parameters
- Test different time windows
- Adjust risk/reward ratios
- Experiment with FVG lookback periods

### 3. Add Filters
Consider adding to the strategy:
- Volume confirmation
- Market structure breaks
- News event filters
- Volatility filters

### 4. Forward Test
- Run on recent data only (2024-2025)
- Compare to full backtest
- Check for regime changes

### 5. Paper Trade
- Implement on demo account
- Validate live performance
- Monitor slippage/commission impact

## 📚 More Information

For detailed documentation, see:
- **BACKTEST_README.md** - Complete documentation
- **NQ_IVFG_Strategy_README.md** - Strategy explanation
- **NQ_IVFG_Strategy.pine** - Original Pine Script

## ⚠️ Important Notes

1. **Strategy Not Profitable**: Current results show losses. Do NOT trade live without significant improvements.

2. **Historical Data**: Past performance ≠ future results. Markets change.

3. **Overfitting Risk**: Optimizing on past data may not work forward.

4. **Real Trading Costs**: Actual costs may be higher (wider spreads, worse fills).

5. **Market Conditions**: Strategy may work in some market regimes but not others.

## 🆘 Need Help?

1. Check the full documentation in `BACKTEST_README.md`
2. Review the console output for error messages
3. Verify all CSV files are present and correctly formatted
4. Check the generated reports for data quality issues

---

**Remember**: This is a backtesting tool. Always validate strategies thoroughly before risking real capital!

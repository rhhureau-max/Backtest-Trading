# ICT FVG Backtest - Quick Start Guide

## 🚀 Quick Start (2 Minutes)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run Backtest
```bash
python ict_fvg_backtest.py
```
⏱️ Takes ~2-3 minutes to process 2.7M candles

### Step 3: Analyze Results
```bash
python analyze_trades.py
```

## 📊 What You Get

### Immediate Console Output
```
================================================================================
TAKE PROFIT: 1.5R (Risk:Reward)
================================================================================
Total Trades:        4083
Winning Trades:      1683
Losing Trades:       2400
Win Rate:            41.22%
Profit Factor:       1.052
Net P&L:             $1170.08
Max Drawdown:        $1157.45
================================================================================
```

### CSV Trade Log
File: `trade_log.csv` (12,249 trades)
- Complete trade history
- Entry/Exit prices and times
- Direction, P&L, Risk
- Import into Excel/Python for custom analysis

## 📁 Files Overview

| File | Purpose | Size |
|------|---------|------|
| `ict_fvg_backtest.py` | Main backtest engine | 682 lines |
| `analyze_trades.py` | Advanced trade analysis | 232 lines |
| `trade_log.csv` | Generated trade history | 1.5 MB |
| `requirements.txt` | Python dependencies | 2 packages |

## ⚙️ Customization

Edit `ict_fvg_backtest.py` to change:

```python
# Trading hours
self.killzone_start = time(8, 30)   # NY open
self.killzone_end = time(11, 0)     # NY close

# Risk management
self.stop_buffer = 0.5              # Stop loss buffer (points)
self.rr_targets = [1.0, 1.5, 2.0]   # Risk:Reward ratios

# Data range
start_year = 2018
end_year = 2025
```

## 📈 Strategy Summary

**ICT Fair Value Gap Strategy**
- ✅ Identifies price imbalances (FVGs)
- ✅ Waits for reversal patterns (Hammer/Shooting Star)
- ✅ Trades only during NY Killzone (08:30-11:00)
- ✅ Tests multiple R:R targets (1R, 1.5R, 2R)

**Performance Highlights**
- 4,083 trades per R:R target
- 50.11% win rate @ 1R
- 1.052 profit factor @ 1.5R ⭐
- $1,170 net profit @ 1.5R
- Average 2-4 minute trade duration

## 🎯 Best R:R Target

**1.5R (1.5:1 Risk:Reward)** provides optimal balance:
- Highest profit factor: 1.052
- Best net P&L: $1,170
- Reasonable win rate: 41.22%
- Manageable drawdown: $1,157

## 📚 Full Documentation

See `ICT_FVG_README.md` for complete guide including:
- Detailed strategy explanation
- Pattern definitions
- Edge case handling
- Future enhancements

## 🔍 Detailed Analysis

See `PROJECT_SUMMARY.md` for:
- Complete performance breakdown
- Year-by-year analysis
- Code architecture
- Validation results

## ❓ Troubleshooting

**"No module named pandas"**
```bash
pip install pandas numpy
```

**"No data file found for YYYY"**
- Check that `YYYY 1m.csv` or `YYYY 1m.csv.zip` exists
- Script auto-detects both formats

**Want to test single year?**
```python
# In main() function, change:
df = backtest.load_all_data(start_year=2024, end_year=2024)
```

## 💡 Pro Tips

1. **First Run**: Let it complete fully (~3 min) for accurate results
2. **Trade Log**: Open `trade_log.csv` in Excel for custom pivot tables
3. **Different Timeframes**: Script designed for 1-minute, adapt for others
4. **Parameter Testing**: Run multiple times with different settings
5. **Performance**: 8GB+ RAM recommended for full dataset

## 🎓 Understanding Results

**Win Rate**: Percentage of winning trades
- 1R: 50% (balanced)
- 1.5R: 41% (still profitable)
- 2R: 34% (needs 33%+ to be profitable at 2:1)

**Profit Factor**: Total Profit ÷ Total Loss
- \>1.0 = Profitable
- 1.05+ = Good
- 1.5+ = Excellent

**Drawdown**: Largest equity decline
- Lower is better
- Expect ~1-2% of account size

## 📞 Support

Check documentation files:
1. `ICT_FVG_README.md` - Full user guide
2. `PROJECT_SUMMARY.md` - Project overview
3. Code comments - Inline documentation

## ✅ Success Checklist

- [ ] Dependencies installed
- [ ] Backtest runs without errors
- [ ] trade_log.csv generated
- [ ] Results displayed in console
- [ ] Analysis script runs successfully
- [ ] Ready to customize parameters

---

**Ready to Go!** Run `python ict_fvg_backtest.py` now! 🚀

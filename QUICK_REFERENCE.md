# Quick Reference Guide - Trading Setup Analysis

## 📊 Analysis Results at a Glance

### Total Setups Found: 695 (2018-2025)

```
┌─────────────┬─────────┬─────────┬─────────┐
│ Timeframe   │ Bearish │ Bullish │ Total   │
├─────────────┼─────────┼─────────┼─────────┤
│ 1-minute    │   138   │   141   │   279   │
│ 5-minute    │   116   │   116   │   232   │
│ 15-minute   │    99   │    85   │   184   │
├─────────────┼─────────┼─────────┼─────────┤
│ TOTAL       │   353   │   342   │   695   │
└─────────────┴─────────┴─────────┴─────────┘
```

## 📁 Files Created

1. **analyze_trading_setups.py** (17KB)
   - Python script to analyze trading data
   - Reads 1m, 5m, 15m data from 2018-2025
   - Identifies both bearish and bullish setup patterns

2. **trading_setup_report.txt** (266KB)
   - Complete detailed report
   - All 695 setups with date, time, and price levels
   - Statistical analysis by timeframe

3. **ANALYSIS_SUMMARY.md** (4.3KB)
   - Executive summary
   - Key findings and insights
   - Trading implications

## 🎯 Setup Patterns Explained

### Bearish Setup (Bearish→Bullish Reversal)
```
8:30 AM: Bearish candle (Close < Open)
    ↓
Next candle: Bullish AND closes above max(last 5 candles)
```

### Bullish Setup (Bullish→Bearish Reversal)
```
8:30 AM: Bullish candle (Close > Open)
    ↓
Next candle: Bearish AND closes below min(last 5 candles)
```

## 📈 Average Breakout Strength

| Timeframe | Bearish Setup | Bullish Setup |
|-----------|--------------|---------------|
| 1m        | 9.03 pts     | 8.87 pts      |
| 5m        | 12.64 pts    | 15.88 pts     |
| 15m       | 19.02 pts    | 24.24 pts     |

**Key Insight**: Larger timeframes = Stronger breakouts

## 🚀 How to Run the Analysis

```bash
# Navigate to repository
cd /home/runner/work/Backtest-Trading/Backtest-Trading

# Run the analysis
python3 analyze_trading_setups.py

# View the report
cat trading_setup_report.txt
```

## 📋 What the Script Does

1. ✅ Loads 1m data from ZIP files (2018-2024)
2. ✅ Loads 1m data from CSV (2025)
3. ✅ Loads 5m and 15m data from CSV files
4. ✅ Identifies 8:30 AM candles
5. ✅ Checks for pattern conditions
6. ✅ Calculates breakout statistics
7. ✅ Generates comprehensive report

## 🔍 Data Coverage

- **Years**: 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025
- **Timeframes**: 1-minute, 5-minute, 15-minute
- **Total Candles Analyzed**: Millions
- **Setups Found**: 695

## 💡 Key Statistics

- **Occurrence Rate**: ~87 setups per year
- **Weekly Average**: ~1.7 setups per week (all timeframes)
- **Balance**: Nearly equal bearish/bullish distribution
- **Strongest Breakout**: 122.92 points (15m bullish setup)
- **Smallest Breakout**: 0.27 points

## 🎓 Usage Tips

1. **For Day Traders**: Focus on 1m and 5m setups
2. **For Swing Traders**: Focus on 15m setups
3. **Risk Management**: Use historical breakout averages for stop-loss
4. **Profit Targets**: Consider average breakout as minimum target
5. **Review Details**: Check trading_setup_report.txt for specific dates

## 📞 Need More Information?

- Full setup details: `trading_setup_report.txt`
- Analysis summary: `ANALYSIS_SUMMARY.md`
- Script source: `analyze_trading_setups.py`

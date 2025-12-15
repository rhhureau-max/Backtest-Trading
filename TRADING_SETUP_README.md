# Trading Setup Pattern Analysis - Complete Guide

## 🎯 Project Overview

This project analyzes historical trading data from 2018 to 2025 to identify specific reversal patterns that occur at the 8:30 AM trading session. The analysis covers three timeframes (1-minute, 5-minute, and 15-minute) and identifies two distinct setup patterns.

---

## 📊 Analysis Results Summary

### **Total Setups Found: 695 patterns over 8 years**

| Timeframe | Bearish Setups | Bullish Setups | Total |
|-----------|---------------|---------------|-------|
| 1-minute  | 138           | 141           | 279   |
| 5-minute  | 116           | 116           | 232   |
| 15-minute | 99            | 85            | 184   |
| **TOTAL** | **353**       | **342**       | **695** |

---

## 🔍 Setup Pattern Definitions

### Pattern 1: Bearish Setup (Reversal to Upside)

**Criteria:**
1. The 8:30 AM candle is **bearish** (Close < Open)
2. The next candle is **bullish** (Close > Open)
3. The next candle closes **ABOVE** the maximum of the last 5 candles

**Example:**
```
Time: 8:30 AM
Open: 12,500 | Close: 12,480 (Bearish -20 pts)

Previous 5 candles max high: 12,490

Time: 8:31 AM (or next interval)
Open: 12,480 | Close: 12,500 (Bullish +20 pts)
Close at 12,500 > 12,490 ✓ SETUP TRIGGERED
```

### Pattern 2: Bullish Setup (Reversal to Downside)

**Criteria:**
1. The 8:30 AM candle is **bullish** (Close > Open)
2. The next candle is **bearish** (Close < Open)  
3. The next candle closes **BELOW** the minimum of the last 5 candles

**Example:**
```
Time: 8:30 AM
Open: 12,480 | Close: 12,500 (Bullish +20 pts)

Previous 5 candles min low: 12,490

Time: 8:31 AM (or next interval)
Open: 12,500 | Close: 12,480 (Bearish -20 pts)
Close at 12,480 < 12,490 ✓ SETUP TRIGGERED
```

---

## 📁 Files in This Repository

### 1. **analyze_trading_setups.py** (17 KB)
The main Python script that performs the analysis.

**Features:**
- Reads data from ZIP files (1m 2018-2024) and CSV files
- Identifies 8:30 AM candles across all trading days
- Validates setup patterns against historical data
- Calculates breakout statistics
- Generates comprehensive reports

**Usage:**
```bash
python3 analyze_trading_setups.py
```

### 2. **trading_setup_report.txt** (266 KB)
Complete detailed report containing:
- All 695 setups with exact dates and times
- Price levels for each setup (Open, High, Low, Close)
- Breakout distances from key levels
- Statistical analysis by timeframe

**Sample Entry:**
```
#1. Date: 10/01/2018
    8:30 AM Candle (Bearish):
      Time: 08:30:00
      Open:  7798.97
      High:  7801.31
      Low:   7787.84
      Close: 7790.18
    Next Candle (Bullish):
      Time: 08:31:00
      Open:  7789.89
      High:  7805.41
      Low:   7789.60
      Close: 7805.41
    Key Levels:
      Max of Last 5 Candles: 7798.97
      Close Above Max By:    6.44
```

### 3. **ANALYSIS_SUMMARY.md** (4.3 KB)
Executive summary with:
- Key findings and insights
- Statistical breakdowns
- Trading implications
- Pattern distribution analysis

### 4. **QUICK_REFERENCE.md** (3.2 KB)
Quick reference guide with:
- At-a-glance statistics
- Setup pattern diagrams
- Usage instructions
- Key metrics

---

## 📈 Statistical Insights

### Average Breakout Strength (Points)

| Timeframe | Bearish Setup | Bullish Setup |
|-----------|--------------|---------------|
| 1-minute  | 9.03         | 8.87          |
| 5-minute  | 12.64        | 15.88         |
| 15-minute | 19.02        | 24.24         |

**Key Observation:** Larger timeframes consistently show stronger breakouts, with 15-minute bullish setups averaging 24.24 points.

### Maximum Breakouts Observed

| Timeframe | Bearish Setup | Bullish Setup |
|-----------|--------------|---------------|
| 1-minute  | 55.27 pts    | 45.82 pts     |
| 5-minute  | 79.64 pts    | 68.56 pts     |
| 15-minute | 103.09 pts   | 122.92 pts    |

### Minimum Breakouts Observed

All timeframes show minimum breakouts under 1 point, suggesting tight stop-losses are viable.

---

## 🎓 Trading Implications

### Setup Frequency
- **87 setups per year** on average across all timeframes
- **1.7 setups per week** - frequent enough for active trading
- Nearly **equal distribution** between bearish and bullish setups

### Risk/Reward Analysis

**For 1-minute Traders:**
- Average move: ~9 points
- Max observed: 55.27 points
- Suitable for: Scalpers and high-frequency traders

**For 5-minute Traders:**
- Average move: 13-16 points
- Max observed: 79.64 points
- Suitable for: Day traders seeking quick moves

**For 15-minute Traders:**
- Average move: 19-24 points
- Max observed: 122.92 points
- Suitable for: Swing traders and position traders

### Suggested Trading Rules

1. **Entry**: Wait for candle confirmation after 8:30 AM candle
2. **Stop Loss**: 
   - Bearish: Below the low of the breakout candle
   - Bullish: Above the high of the breakout candle
3. **Profit Targets**: Use average breakout statistics as minimum targets
4. **Risk Management**: Risk no more than 1-2% per trade

---

## 🔧 Technical Details

### Data Sources
- **1-minute data (2018-2024)**: Compressed ZIP files
- **1-minute data (2025)**: CSV file
- **5-minute data (all years)**: CSV files
- **15-minute data (all years)**: CSV files

### CSV Format
```
Column1;Column2;Column3;Column4;Column5;Column6;Column7
Date;Time;Open;High;Low;Close;Volume
DD/MM/YYYY;HH:MM:SS;Price;Price;Price;Price;Volume
```

### Data Processing
1. Extract/read data from ZIP and CSV files
2. Parse dates and times
3. Identify 8:30 AM candles
4. Calculate rolling 5-candle highs/lows
5. Validate setup conditions
6. Record and analyze matches

---

## 🚀 How to Run

### Prerequisites
```bash
pip install pandas
```

### Execution
```bash
# Navigate to repository
cd /home/runner/work/Backtest-Trading/Backtest-Trading

# Run analysis
python3 analyze_trading_setups.py

# View results
cat trading_setup_report.txt
less ANALYSIS_SUMMARY.md
```

### Output Files Generated
1. `trading_setup_report.txt` - Detailed report
2. Console output - Summary statistics

---

## 📊 Sample Use Cases

### 1. Backtesting Strategy
Use the detailed report to identify specific historical setups and analyze their subsequent price action.

### 2. Pattern Recognition
Study the characteristics of successful vs. unsuccessful setups to refine entry criteria.

### 3. Time-of-Day Analysis
Focus on the 8:30 AM time period to understand volatility patterns.

### 4. Multi-Timeframe Confirmation
Compare setups across different timeframes for confluence.

---

## 🎯 Future Enhancements

Potential additions to this analysis:
- [ ] Follow-up price action tracking (5, 10, 30 minutes later)
- [ ] Win rate calculation
- [ ] Profit/Loss simulation
- [ ] Volume analysis at setup times
- [ ] Correlation with market indices
- [ ] Seasonal pattern analysis
- [ ] Day-of-week distribution

---

## 📝 Notes

- All times are in the timezone of the data source
- Analysis focuses strictly on the defined setup criteria
- No subjective interpretation or filtering applied
- Results are purely statistical and historical
- Past performance does not guarantee future results

---

## 🤝 Contributing

To modify or extend this analysis:
1. Edit `analyze_trading_setups.py`
2. Adjust setup criteria in the `find_setups()` method
3. Add new statistical calculations in `generate_report()`
4. Run the script and review new results

---

## 📞 Support

For questions about:
- **Setup patterns**: Review ANALYSIS_SUMMARY.md
- **Usage**: See QUICK_REFERENCE.md
- **Detailed data**: Check trading_setup_report.txt
- **Code**: Review analyze_trading_setups.py

---

## ⚠️ Disclaimer

This analysis is for educational and research purposes only. It does not constitute financial advice. Always conduct your own research and consult with qualified financial advisors before making trading decisions.

---

**Generated:** December 2, 2025  
**Data Period:** 2018-2025  
**Total Patterns Found:** 695

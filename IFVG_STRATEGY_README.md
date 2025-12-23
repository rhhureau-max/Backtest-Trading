# IFVG Backtest Strategy - Documentation

## 📋 Overview

This script implements a comprehensive backtest of an **Inverse Fair Value Gap (IFVG)** strategy on Nasdaq (NQ) futures using 5-minute data from 2018 to 2025.

## 🎯 Strategy Description

### Fair Value Gap (FVG) Detection - STRICT WICK RULES

The strategy identifies Fair Value Gaps using **strict wick rules** (High and Low prices, not just candle bodies):

#### Bearish FVG (Gap Down)
- Requires 3 consecutive candles
- **Condition**: Low of candle 1 > High of candle 3
- **Gap Zone**: Between [High of candle 3] and [Low of candle 1]
- Represents a physical gap created during a downward move

#### Bullish FVG (Gap Up)
- Requires 3 consecutive candles
- **Condition**: High of candle 1 < Low of candle 3
- **Gap Zone**: Between [High of candle 1] and [Low of candle 3]
- Represents a physical gap created during an upward move

### Entry Logic (Inversion)

#### LONG Setup (Inversion of Bearish FVG)
- Identify a recent Bearish FVG
- Wait for price to reverse and close **above** the upper bound (Low of candle 1)
- Entry at close price
- **Time Filter**: Entry candle close must occur between 02:00 and 06:00 (inclusive)

#### SHORT Setup (Inversion of Bullish FVG)
- Identify a recent Bullish FVG
- Wait for price to reverse and close **below** the lower bound (High of candle 1)
- Entry at close price
- **Time Filter**: Entry candle close must occur between 02:00 and 06:00 (inclusive)

### Trade Management

#### Stop Loss (SL)
- **Long**: Placed below the most recent significant Swing Low (lookback: 15 candles)
- **Short**: Placed above the most recent significant Swing High (lookback: 15 candles)

#### Take Profit (TP)
- **Long**: Target the previous major Swing High (lookback: 20 candles)
- **Short**: Target the previous major Swing Low (lookback: 20 candles)

#### Swing Detection
- Uses a local window (10-15 candles) to identify pivot points
- Swing High: A high that is higher than both neighboring candles
- Swing Low: A low that is lower than both neighboring candles

## 📊 Data Format

### Input Files
- **Files**: `2018 5m.csv` through `2025 5m.csv`
- **Separator**: Semicolon (`;`)
- **Columns**:
  - Column1: Date (DD/MM/YYYY)
  - Column2: Time (HH:MM:SS)
  - Column3: Open
  - Column4: High
  - Column5: Low
  - Column6: Close
  - Column7: Volume

### Example Data Row
```
01/01/2018;17:00:00;7503.739664;7511.940473;7499.63926;7511.3547;1451
```

## 🚀 Usage

### Prerequisites
```bash
pip install pandas numpy
```

### Running the Backtest
```bash
python3 ifvg_backtest.py
```

### Output

The script generates:

1. **Console Report** with:
   - Overall performance metrics
   - Win rate, profit factor, max drawdown
   - Yearly breakdown (2018-2025)
   - Trade statistics (long/short, exit reasons)

2. **CSV File** (`ifvg_trades_results.csv`) containing:
   - All trade details
   - Entry/exit times and prices
   - Stop loss and take profit levels
   - P&L for each trade
   - FVG type that triggered the trade

## 📈 Performance Metrics

### Overall Metrics (Example from Latest Run)
- **Total Trades**: 24,012
- **Win Rate**: 51.48%
- **Profit Factor**: 1.03
- **Total P&L**: 9,344.49 points
- **Max Drawdown**: -8,108.88 points

### Best Performing Year
- **2024**: 3,134 trades, 52.58% win rate, +10,127.40 points

### Trade Distribution
- Long Trades: 11,929 (52.57% win rate)
- Short Trades: 12,083 (50.41% win rate)

## 🔧 Configuration

Key parameters that can be adjusted in the code:

```python
# In IFVGBacktest class __init__
self.swing_window = 12  # Window for swing detection

# In find_swing_high/low methods
lookback = 15  # Lookback for SL placement
lookback = 20  # Lookback for TP placement

# In run_backtest method
max_fvg_age = 50  # Maximum candles to keep an FVG active

# Time filter (in is_valid_entry_time)
start_time = time(2, 0, 0)   # 02:00:00
end_time = time(6, 0, 0)     # 06:00:00
```

## 📁 File Structure

```
/home/runner/work/Backtest-Trading/Backtest-Trading/
├── ifvg_backtest.py              # Main backtest script
├── ifvg_trades_results.csv       # Output file with all trades
├── 2018 5m.csv                   # Data file
├── 2019 5m.csv                   # Data file
├── ...
└── 2025 5m.csv                   # Data file
```

## 🔍 Key Features

1. **Strict FVG Detection**: Uses actual High/Low wicks, not just candle bodies
2. **Time-Based Filtering**: Only entries between 02:00-06:00
3. **Dynamic SL/TP**: Based on recent swing levels, not fixed percentages
4. **Complete Trade Log**: All trades saved to CSV for further analysis
5. **Yearly Performance**: Break down results by year for trend analysis
6. **Progress Tracking**: Real-time progress indicator during backtest
7. **Comprehensive Metrics**: Win rate, profit factor, drawdown, and more

## 📝 Notes

- **No Timezone Conversion**: Uses raw time from CSV files as-is
- **No Position Sizing**: Results in points, can be scaled to contracts/position size
- **Sequential Processing**: Processes data chronologically to avoid lookahead bias
- **FVG Cleanup**: Old FVGs (>50 candles) are automatically removed to improve performance

## 🎓 Strategy Insights

### What Makes This Strategy Unique?

1. **Inversion Logic**: Trades against the initial FVG direction (contrarian approach)
2. **Time Window**: Focuses on early morning hours (02:00-06:00) when certain patterns may be more reliable
3. **Strict Rules**: Uses actual wicks (High/Low) rather than bodies for precise gap identification
4. **Smart Exits**: SL/TP based on actual market structure (swing highs/lows)

### Risk Management

- **Stop Loss Always Active**: Every trade has a defined risk
- **Take Profit Targets**: Based on previous swing levels (realistic targets)
- **No Martingale**: Each trade is independent
- **Time-Based Filter**: Reduces exposure to unfavorable market hours

## 📧 Support

For questions or modifications, review the inline code comments in `ifvg_backtest.py`.

---

**Created by**: Senior Quantitative Analyst  
**Version**: 1.0  
**Last Updated**: December 2024

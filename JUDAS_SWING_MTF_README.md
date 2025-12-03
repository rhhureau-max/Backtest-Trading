# Judas Swing Multi-Timeframe (MTF) Strategy - User Guide

## 📖 Overview

This advanced backtesting script implements a sophisticated multi-timeframe analysis of the "Judas Swing + Inversion FVG" trading strategy. It tests multiple configurations simultaneously to identify optimal parameters.

## 🚀 Quick Start

### Prerequisites
```bash
pip install pandas numpy matplotlib seaborn
```

### Running the Backtest
```bash
python3 judas_swing_mtf_strategy.py
```

**Expected Runtime**: 2-3 minutes for 7 years of data

## 📂 Input Data Requirements

The script requires CSV files in the following format:
- **5m data**: Required for all years (e.g., `2018 5m.csv`, `2019 5m.csv`, etc.)
- **1m data**: Optional but recommended (e.g., `2025 1m.csv`)

### CSV Format
```
Column1;Column2;Column3;Column4;Column5;Column6;Column7
Date;Time;Open;High;Low;Close;Volume
01/01/2025;17:00:00;21927.625;21980.720;21911.645;21975.049;1482
```

**Note**: If 1m data is not available, the script will interpolate it from 5m data.

## 🎯 What the Script Does

### 1. Multi-Timeframe Analysis
- Analyzes FVG formations on **both 5m and 1m** timeframes
- Applies **hierarchical priority**: 5m FVG > 1m FVG
- Tracks which timeframe was used for each trade

### 2. A/B Testing of Stop Loss
Tests **two SL placement strategies**:
- **SL-Body**: Stop beyond the body of the manipulation candle
  - LONG: min(Open, Close)
  - SHORT: max(Open, Close)
- **SL-Wick**: Stop at the absolute wick extreme
  - LONG: Absolute Low
  - SHORT: Absolute High

### 3. Multiple Take Profit Levels
Tests **three R:R ratios** for each configuration:
- **1R**: 1:1 risk/reward
- **1.5R**: 1:1.5 risk/reward
- **2R**: 1:2 risk/reward

### 4. Complete Trade Simulation
For each detected setup, the script:
1. Identifies Tokyo session (19:00-00:00)
2. Detects manipulation (02:00-02:30)
3. Finds FVGs on both timeframes
4. Applies priority rule (5m > 1m)
5. Waits for FVG inversion
6. Simulates 6 trade configurations (2 SL × 3 TP)
7. Tracks WIN/LOSS for each configuration

## 📊 Output Files

### 1. Main Results
**File**: `judas_swing_mtf_results.csv`
- All 3,800+ trade records
- Includes: entry price, SL, TP, outcome, timeframe used, etc.

### 2. Statistics
**File**: `judas_swing_mtf_results_statistics.csv`
- Aggregated stats by configuration
- Columns: SL_Type, Timeframe, TP_Level, Win_Rate, Expectancy, etc.

### 3. Comparison Table
**File**: `judas_swing_mtf_results_comparison.csv`
- Summary comparison table
- Format specified in requirements

### 4. Visualizations
**File**: `judas_swing_mtf_comparison.png`
- 5 comprehensive charts:
  1. Win Rate by SL Type and TP Level
  2. Win Rate by Timeframe
  3. Expectancy Comparison
  4. Trade Distribution
  5. Performance Heatmap

### 5. Reports
**Files**: 
- `JUDAS_SWING_MTF_ANALYSIS.md` - Detailed analysis report
- `JUDAS_SWING_MTF_SUMMARY.md` - Executive summary

## 🔧 Script Architecture

### Main Classes

#### `FVG`
Represents a Fair Value Gap with properties:
- `type`: 'BULLISH' or 'BEARISH'
- `top`, `bottom`: Price boundaries
- `formation_time`: When FVG was created
- `timeframe`: '5m' or '1m'

#### `JudasSwingMTFAnalyzer`
Main analysis engine with methods:

**Data Loading**:
- `load_data()`: Load 5m and 1m CSV files
- `resample_5m_to_1m()`: Interpolate 1m from 5m if needed

**Analysis Methods**:
- `identify_tokyo_session()`: Find Tokyo High/Low
- `get_manipulation_data()`: Extract 02:00-02:30 data
- `detect_fvgs()`: Find Fair Value Gaps
- `find_manipulation_candle()`: Identify extreme candle
- `check_fvg_inversion()`: Detect FVG reversal
- `simulate_trade()`: Run trade simulation

**Workflow Methods**:
- `analyze_day()`: Process single day (returns 0-6 trades)
- `run_backtest()`: Main loop through all days
- `generate_statistics()`: Calculate win rates and expectancy
- `create_comparison_table()`: Format results table
- `save_results()`: Export to CSV
- `create_visualizations()`: Generate charts
- `generate_report()`: Create markdown report

## 📈 Key Metrics Explained

### Win Rate
Percentage of trades that hit TP before SL:
```
Win Rate = (Wins / Total Trades) × 100%
```

### Expectancy (R)
Average profit/loss per trade in risk units:
```
Expectancy = (Win Rate × Avg Win) + ((1 - Win Rate) × Avg Loss)
```
- Positive expectancy = Profitable strategy
- Negative expectancy = Losing strategy

### Risk/Reward Ratio (R:R)
Ratio of potential profit to potential loss:
- **1R**: Risk $100 to make $100
- **1.5R**: Risk $100 to make $150
- **2R**: Risk $100 to make $200

## 🎓 Strategy Logic

### Entry Conditions

**For SHORT (Bearish) Trades**:
1. Price breaks Tokyo High during 02:00-02:30 ✅
2. Bullish FVG forms during manipulation ✅
3. Price reverses and fills the FVG ✅
4. Candle closes **below** FVG bottom ✅
5. **Entry**: Close of inversion candle

**For LONG (Bullish) Trades**:
1. Price breaks Tokyo Low during 02:00-02:30 ✅
2. Bearish FVG forms during manipulation ✅
3. Price reverses and fills the FVG ✅
4. Candle closes **above** FVG top ✅
5. **Entry**: Close of inversion candle

### Priority Rule (Critical!)

The script follows **strict hierarchy** for timeframe selection:

```
IF 5m FVG exists:
    USE 5m FVG for entry signal
    IGNORE 1m FVG
ELSE IF 1m FVG exists:
    USE 1m FVG for entry signal
ELSE:
    NO TRADE (no FVG found)
```

**Result**: ~90% of trades use 5m FVG, ~10% use 1m FVG

## 📊 Interpreting Results

### Best Configuration Identification

Look for configuration with:
1. **Positive Expectancy** (> 0)
2. **Reasonable Win Rate** (> 40%)
3. **Sufficient Sample Size** (> 50 trades)
4. **Consistent Performance** across years

### Example from Backtest:
```
SL-Wick + 5m + 1R:
- Win Rate: 52.3%
- Expectancy: +0.045R
- Trades: 572
- Verdict: ✅ Profitable and consistent
```

### Red Flags:
```
SL-Body + 1m + 1R:
- Win Rate: 41.9%
- Expectancy: -0.161R
- Trades: 62
- Verdict: ❌ Losing configuration
```

## 🔍 Customization Options

### Change Timeframes
```python
# In load_data() method
analyzer.load_data(years=range(2020, 2024))  # Only 2020-2023
```

### Modify R:R Ratios
```python
# In analyze_day() method, line ~620
for rr_ratio, rr_name in [(1.0, '1R'), (1.5, '1.5R'), (2.0, '2R')]:
```
Change to:
```python
for rr_ratio, rr_name in [(1.0, '1R'), (2.0, '2R'), (3.0, '3R')]:
```

### Adjust Manipulation Window
```python
# In get_manipulation_data() method
manip_start = next_day + pd.Timedelta(hours=2)   # 02:00
manip_end = manip_start + pd.Timedelta(minutes=30)  # 02:30
```

### Add Custom Filters
```python
# In analyze_day() method, after line ~500
# Example: Filter by manipulation amplitude
manip_amplitude = manip_high - manip_low
if manip_amplitude < 10:  # Skip small manipulations
    return day_trades
```

## 🐛 Troubleshooting

### Issue: "No module named 'pandas'"
```bash
pip install pandas numpy matplotlib seaborn
```

### Issue: "No data loaded"
- Check that CSV files exist in the script directory
- Verify file naming format: `YYYY 5m.csv` (e.g., `2025 5m.csv`)
- Check CSV format matches expected structure

### Issue: "No trades detected"
- Verify Tokyo session times in your timezone
- Check that data includes the full 19:00-02:30 range
- Ensure manipulation window (02:00-02:30) has data

### Issue: Script runs slowly
- **Normal**: Processing 7 years of data takes 2-3 minutes
- **Optimization**: Reduce year range or comment out visualization code

## 💻 Code Structure

```
judas_swing_mtf_strategy.py
│
├── FVG Class (lines 50-100)
│   └── Fair Value Gap representation
│
├── JudasSwingMTFAnalyzer Class (lines 103-950)
│   ├── __init__() - Initialize analyzer
│   ├── Data Loading (lines 109-220)
│   │   ├── load_data()
│   │   └── resample_5m_to_1m()
│   ├── Session Analysis (lines 221-280)
│   │   ├── identify_tokyo_session()
│   │   └── get_manipulation_data()
│   ├── FVG Detection (lines 281-340)
│   │   ├── detect_fvgs()
│   │   └── find_manipulation_candle()
│   ├── Trade Logic (lines 341-450)
│   │   ├── check_fvg_inversion()
│   │   └── simulate_trade()
│   ├── Core Analysis (lines 451-700)
│   │   ├── analyze_day() [Main logic]
│   │   └── run_backtest() [Loop]
│   └── Output Generation (lines 701-950)
│       ├── generate_statistics()
│       ├── create_comparison_table()
│       ├── save_results()
│       ├── create_visualizations()
│       └── generate_report()
│
└── main() Function (lines 953-1000)
    └── Orchestrates entire workflow
```

## 📚 Related Files

- **tokyo_session_analysis.py** - Original Tokyo session analyzer
- **tokyo_fvg_strategy.py** - Single-timeframe FVG strategy
- **visualize_results.py** - Result visualization utilities

## ⚡ Performance Tips

1. **Use Full 1m Data**: Interpolated data is less accurate
2. **Large Sample Size**: More years = more reliable statistics
3. **Consider Market Conditions**: Filter by volatility/volume
4. **Transaction Costs**: Add spread/commission to expectancy
5. **Forward Testing**: Validate on unseen data

## 📞 Support

For issues or questions:
1. Check this README first
2. Review `JUDAS_SWING_MTF_ANALYSIS.md` for detailed results
3. Examine `JUDAS_SWING_MTF_SUMMARY.md` for interpretation

## 🔮 Future Enhancements

Potential improvements:
- [ ] Real-time trading integration
- [ ] Additional timeframes (15m, 1h)
- [ ] Volume profile analysis
- [ ] Market condition filters
- [ ] Position sizing algorithms
- [ ] Monte Carlo simulation
- [ ] Walk-forward optimization

---

**Version**: 1.0  
**Last Updated**: December 3, 2025  
**Author**: Advanced Backtesting System  
**License**: For educational and research purposes

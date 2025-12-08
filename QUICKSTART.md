# London Reversal Backtest - Quick Start Guide

## 🚀 Quick Start (3 Steps)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

Or manually:
```bash
pip install pandas numpy
```

### Step 2: Run the Backtest
```bash
python3 london_reversal_backtest.py
```

### Step 3: View Results
The script will:
- Print a detailed summary to the console
- Generate `london_reversal_results.csv` with all trade details

## 📊 Understanding the Output

### Console Output
You'll see three sets of results for each Take Profit level:

```
TP1_1R Results:
  Total Trades: 852
  Wins: 601
  Losses: 251
  Win Rate: 70.54%
  Total PnL: 9236.67 points
  Average PnL per Trade: 10.84 points
  Average Win: 15.43 points
  Average Loss: -0.15 points
  Profit Factor: 238.75
```

### CSV Output
The `london_reversal_results.csv` file contains detailed information for each trade:
- Entry and exit prices for all 3 TP levels
- Tokyo session ranges
- Manipulation details
- FVG and MSS timestamps
- PnL for each TP level

## ⚙️ Customization

Edit the `main()` function in `london_reversal_backtest.py`:

```python
# Change timeframe for scanning (more precise entries with 1m)
backtest.run_backtest(
    scan_timeframe='1m',      # Change from '5m' to '1m'
    tokyo_timeframe='15m',
    years=list(range(2018, 2026))
)

# Or test specific years only
backtest.run_backtest(
    scan_timeframe='5m',
    tokyo_timeframe='15m',
    years=[2023, 2024, 2025]  # Test recent years only
)
```

## 📈 Key Metrics Explained

### Win Rate
Percentage of trades that hit the take profit target.

### Profit Factor
Total winning points ÷ Total losing points. Higher is better.
- < 1.0: Losing strategy
- 1.0-2.0: Good
- 2.0+: Excellent

### Average PnL per Trade
Expected value per trade in points.

## 🎯 Strategy Overview

The London Reversal strategy:
1. **Tokyo Session** (17:00-00:00): Identifies range
2. **London Killzone** (01:00-04:00): Looks for manipulation
3. **Three-Step Validation**:
   - Manipulation: Sweep of Tokyo High/Low
   - FVG: Fair Value Gap formation
   - MSS: Market Structure Shift
4. **Entry**: 50% Fib retracement
5. **Exit**: 1R, 1.5R, or 2R take profit

## ⏱️ Expected Runtime

- **5m timeframe**: ~2-3 minutes
- **1m timeframe**: ~10-15 minutes (more data to process)

## 📝 Data Requirements

Ensure your CSV files follow this structure:
```
Column1;Column2;Column3;Column4;Column5;Column6;Column7
01/01/2018;17:00:00;7503.74;7518.09;7499.64;7517.80;2852
```

Files should be named:
- `YYYY 1m.csv.zip` (for 1-minute data, zipped)
- `YYYY 5m.csv` (for 5-minute data)
- `YYYY 15m.csv` (for 15-minute data)
- `YYYY 1H.csv` (for 1-hour data)

## 🔍 Troubleshooting

**Problem**: Script runs but finds 0 trades
- **Solution**: Check that your data covers the required time periods (17:00-04:00)

**Problem**: "ModuleNotFoundError"
- **Solution**: Run `pip install pandas numpy`

**Problem**: "FileNotFoundError"
- **Solution**: Ensure CSV files are in the same directory as the script

## 📚 Learn More

For detailed strategy explanation and advanced usage, see:
- `README_LONDON_REVERSAL.md` - Complete documentation

## 💡 Tips

1. **Start with 5m timeframe** for faster results
2. **Use 1m timeframe** for maximum precision (slower)
3. **Analyze TP2 (1.5R)** - Usually offers the best balance of win rate and reward
4. **Check different years** - Market conditions vary over time

## 🎓 Next Steps

1. Run the backtest with default settings
2. Review the results CSV in Excel or Google Sheets
3. Experiment with different timeframes
4. Analyze which market conditions produce the best results
5. Consider forward testing on recent data before live trading

---

**Happy Backtesting! 📈**

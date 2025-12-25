# Quick Start Guide - FVG C.E. Backtesting

## Installation (30 seconds)

```bash
pip install pandas numpy matplotlib
```

## Run the Backtest (1 command)

```bash
python fvg_ce_backtest.py
```

That's it! The script will automatically:
- Load all available CSV data files
- Run the backtest with Risk Model 2 (default)
- Generate performance charts
- Create trade log CSV
- Display comprehensive statistics

## Expected Output

```
================================================================================
FVG CONSEQUENT ENCROACHMENT BACKTESTING SYSTEM
================================================================================

[1/7] Loading data...
[2/7] Identifying Fair Value Gaps...
[3/7] Calculating risk levels (Model 2)...
[4/7] Managing setups and detecting entries...
[5/7] Managing positions and exits...
[6/7] Calculating performance metrics...
[7/7] Generating performance charts...

BACKTEST COMPLETE
================================================================================
```

## Change Risk Model (10 seconds)

Open `fvg_ce_backtest.py` and change line 25:

```python
RISK_MODEL = 1  # Try Model 1 (Aggressive Sniper)
RISK_MODEL = 2  # Try Model 2 (Structural Defender) - DEFAULT
RISK_MODEL = 3  # Try Model 3 (Volatility Adapter)
```

## Change Timeframe (10 seconds)

Edit line 33:

```python
TIMEFRAME = '1m'   # 1-minute bars
TIMEFRAME = '5m'   # 5-minute bars - DEFAULT
TIMEFRAME = '15m'  # 15-minute bars
```

## Change Years (10 seconds)

Edit line 34:

```python
YEARS = [2023, 2024, 2025]  # Test recent years only
YEARS = [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]  # All years - DEFAULT
```

## Output Files

After running, you'll find:

1. **Performance Chart**: `fvg_ce_backtest_model2_5m.png`
   - Visual equity curve
   - Drawdown visualization

2. **Trade Log**: `trade_log_model2_5m.csv`
   - Every trade with entry/exit
   - PnL per trade
   - Exit reasons

## Understanding the Results

### Key Metrics Explained:

- **Win Rate**: % of profitable trades (not most important!)
- **Profit Factor**: Avg Win / Avg Loss (higher is better)
- **Maximum Drawdown**: Largest peak-to-trough decline (lower is better)
- **Total PnL**: Sum of all trade profits/losses (in points)

### Exit Reasons:

- **Stop_Loss**: Trade hit protective stop
- **Take_Profit**: Trade reached target
- **Hard_Exit_08:00**: Forced close at 8am (session end)

## Troubleshooting

**Problem**: Script says "No data loaded"
**Solution**: Check that CSV files are in the correct directory

**Problem**: Script is slow
**Solution**: Normal! Processing 500k+ candles takes 2-3 minutes

**Problem**: No trades executed
**Solution**: Check session times match your data's timezone

## Tips for Best Results

1. ✅ Use 5-minute timeframe (best signal quality)
2. ✅ Test all 3 risk models to find your preference
3. ✅ Review trade logs to understand strategy behavior
4. ✅ Start with Model 2 (most conservative)
5. ✅ Check performance charts for consistency

## Support

- See `README_FVG_CE.md` for detailed documentation
- See `BACKTEST_SUMMARY.md` for results comparison
- Code is heavily commented - read the script!

---

**Total Time to Run First Backtest**: ~3 minutes  
**Difficulty Level**: Beginner-friendly  
**Prerequisites**: Python 3.7+ installed

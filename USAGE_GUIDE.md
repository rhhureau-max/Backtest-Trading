# London Reversal Backtest - Usage Guide

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run backtest with all years
python london_reversal_backtest.py
```

## Output Files

The script generates the following files:

### 1. CSV Trade Logs (3 files)
- `london_reversal_TP1_trades.csv` - Trades with 1R take profit
- `london_reversal_TP2_trades.csv` - Trades with 1.5R take profit
- `london_reversal_TP3_trades.csv` - Trades with 2R take profit

Each CSV contains these columns:
- **Date**: Trade entry date (YYYY-MM-DD)
- **Entry_Time**: Exact entry time (HH:MM:SS)
- **Type**: Long or Short
- **Entry_Price**: Entry price (includes 0.5pt slippage)
- **SL_Price**: Stop loss price
- **TP_Price**: Take profit price for this risk-reward level
- **Exit_Time**: When trade was closed
- **Outcome**: Win/Loss/Missed
- **PnL_Amount**: Profit or loss in points
- **Risk_Reward_Used**: 1.0, 1.5, or 2.0
- **Entry_Hour**: Hour of entry (01-03)
- **Day_of_Week**: Monday through Sunday
- **Year**: Trade year

### 2. Equity Curve Charts (4 PNG files)
- `equity_curve_TP1.png` - Equity curve for 1R target
- `equity_curve_TP2.png` - Equity curve for 1.5R target
- `equity_curve_TP3.png` - Equity curve for 2R target
- `equity_curve_combined.png` - All three curves on one chart

## Understanding the Results

### Global Statistics
Each TP level shows:
- **Net Profit**: Total cumulative profit in points
- **Profit Factor**: Sum of wins / Abs(Sum of losses) - higher is better
- **Win Rate**: Percentage of winning trades
- **Max Drawdown**: Largest equity drop from peak ($ and %)
- **Expectancy**: Average expected value per trade

### Temporal Analysis
- **PnL by Year**: Performance breakdown for each year (2018-2024)
- **Winrate by Day of Week**: Which days perform best
- **Winrate by Entry Hour**: Best hours for entries (01:00-03:00)

### Missed Trades
The script tracks trades where:
- MSS was validated and trade setup calculated
- BUT TP1 level was hit BEFORE entry at 50% Fib
- These are counted separately and marked as "Missed"

## Strategy Rules (Recap)

1. **Tokyo Range**: Identify High/Low between 17:00-00:00 Chicago time
2. **London Killzone**: Monitor 01:00-04:00 for setups
3. **Validation Sequence**:
   - Price sweeps Tokyo High (for shorts) or Low (for longs)
   - Fair Value Gap forms opposite to sweep direction
   - Market Structure Shift validates reversal
4. **Entry**: 50% Fibonacci retracement (with 0.5pt slippage)
5. **Exit**: Stop loss at manipulation peak ±0.5pts, TPs at 1R/1.5R/2R

## Customization

Edit the `main()` function in `london_reversal_backtest.py`:

```python
backtest.run_backtest(
    scan_timeframe='5m',      # Change to '1m' for more precision
    tokyo_timeframe='15m',     # Or use '1H' for Tokyo range
    years=list(range(2018, 2026))  # Adjust year range
)
```

## Performance Optimization

- **M1 timeframe**: Most precise but slower (processes millions of bars)
- **M5 timeframe**: Good balance of precision and speed (recommended)
- **Reduce years**: Test on single year first, then expand

## Interpreting Results

### Good Signs
✓ Profit Factor > 1.5
✓ Win Rate > 40% for TP1
✓ Max Drawdown < 30%
✓ Positive expectancy

### Warning Signs
✗ High missed trade percentage (>80%)
✗ Profit factor < 1.0
✗ Large drawdown periods
✗ Inconsistent yearly performance

## Support

For questions or issues, review:
- `README_LONDON_REVERSAL.md` - Strategy documentation
- `ENHANCEMENTS_SUMMARY.md` - Feature details
- `IMPLEMENTATION_REPORT.md` - Technical implementation

Generated: December 2024
Version: 2.0 (Enhanced)

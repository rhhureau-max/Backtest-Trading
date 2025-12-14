# FVG Backtest System - Usage Guide

## Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <repository-url>
cd Backtest-Trading

# Install dependencies
pip install -r requirements.txt
```

### 2. Run the Backtest

```bash
python main.py
```

The system will automatically:
- Load all available data (2018-2024)
- Process 1-minute, 5-minute, and 15-minute timeframes
- Generate comprehensive reports and visualizations
- Save all results to the `results/` directory

## Understanding the Results

### Performance Summary

After running, you'll see summary statistics for each timeframe:

```
SUMMARY - 15M
============================================================
Total Trades:        793
Winning Trades:      313
Losing Trades:       480
Win Rate:            39.47%
Total P&L:           $5205.57
Total Return:        52.06%
Profit Factor:       1.27
Sharpe Ratio:        1.30
Max Drawdown:        -6.15%
Avg Win:             $78.80
Avg Loss:            $-40.54
============================================================
```

### Key Metrics Explained

- **Win Rate**: Percentage of profitable trades
- **Profit Factor**: Ratio of gross profit to gross loss (>1 is profitable)
- **Sharpe Ratio**: Risk-adjusted return (>1 is good, >2 is excellent)
- **Max Drawdown**: Largest peak-to-trough decline in equity
- **Risk/Reward Ratio**: Average win divided by average loss

### Generated Files

#### Reports
- `backtest_report.md` - Detailed markdown report with all statistics
- `backtest_report.html` - HTML version for web viewing

#### Trade Data
- `trades_1m.csv` - All trades for 1-minute timeframe
- `trades_5m.csv` - All trades for 5-minute timeframe
- `trades_15m.csv` - All trades for 15-minute timeframe

#### Visualizations

For each timeframe (1m, 5m, 15m):
- `equity_curve_*.png` - Shows account balance over time
- `drawdown_*.png` - Shows drawdown periods
- `trade_distribution_*.png` - Win/loss distribution analysis
- `performance_heatmap_*.png` - Monthly performance by year

## Analyzing Trade Data

### CSV Structure

Each trade record contains:

```csv
entry_time,entry_price,exit_time,exit_price,direction,stop_loss,take_profit,exit_reason,pnl,return_pct,fvg_lower,fvg_upper,fvg_middle
```

- **entry_time**: When trade was entered
- **exit_time**: When trade was closed
- **direction**: Long or Short
- **exit_reason**: TP (take profit), SL (stop loss), or EOD (end of day)
- **pnl**: Profit/loss in dollars
- **return_pct**: Return as percentage
- **fvg_***: Fair Value Gap boundaries

### Custom Analysis

You can load and analyze the trade data using pandas:

```python
import pandas as pd

# Load trades
trades = pd.read_csv('results/trades_15m.csv')

# Filter winning trades
wins = trades[trades['pnl'] > 0]

# Calculate statistics
print(f"Average winning trade: ${wins['pnl'].mean():.2f}")
print(f"Best trade: ${wins['pnl'].max():.2f}")

# Analyze by year
trades['year'] = pd.to_datetime(trades['entry_time']).dt.year
yearly_pnl = trades.groupby('year')['pnl'].sum()
print(yearly_pnl)
```

## Customization

### Modifying Parameters

Edit `main.py` to change:

```python
# Configuration
START_YEAR = 2018        # Start year
END_YEAR = 2024          # End year
INITIAL_CAPITAL = 10000  # Starting capital
TIMEFRAMES = ['1m', '5m', '15m']  # Timeframes to test
```

### Testing Different Entry Times

Modify `fvg_detector.py`:

```python
# Change FVG detection time from 8:30 to another time
data_with_fvg = detector.detect_fvg(data, target_time='09:00:00')
```

### Adjusting Risk/Reward

Edit `backtest_engine.py`:

```python
# Change from 2:1 to 3:1 risk/reward
if direction == 1:  # Long
    take_profit = entry_price + (3 * risk)  # Changed from 2 to 3
else:  # Short
    take_profit = entry_price - (3 * risk)  # Changed from 2 to 3
```

## Module Overview

### data_loader.py
- Loads CSV and ZIP files
- Handles multiple years and timeframes
- Preprocesses and cleans data
- Filters trading hours

### fvg_detector.py
- Detects bullish and bearish FVGs
- Identifies gaps at 8:30 AM
- Calculates FVG boundaries
- Determines entry times by timeframe

### backtest_engine.py
- Executes trades based on signals
- Manages stop loss and take profit
- Tracks positions and exits
- Calculates P&L for each trade

### performance_metrics.py
- Calculates comprehensive statistics
- Win rate, profit factor, Sharpe ratio
- Drawdown analysis
- Monthly and yearly breakdowns

### visualization.py
- Creates equity curves
- Generates drawdown charts
- Plots trade distributions
- Creates performance heatmaps

### report_generator.py
- Generates markdown reports
- Creates HTML reports
- Compares timeframe performance
- Provides strategy recommendations

## Interpreting Results

### What Makes a Good Strategy?

Based on the backtest results, look for:

1. **Win Rate > 40%**: Indicates consistent signal quality
2. **Profit Factor > 1.5**: Shows positive expectancy
3. **Sharpe Ratio > 1.0**: Good risk-adjusted returns
4. **Max Drawdown < 20%**: Manageable risk
5. **Consistent yearly returns**: Strategy robustness

### Timeframe Comparison

From the backtest results:

- **1-minute**: Highest number of trades, lower win rate, good Sharpe
- **5-minute**: More trades, moderate performance
- **15-minute**: Best overall performance with 52% return and 1.30 Sharpe

### Red Flags

Watch out for:
- High consecutive losses (>15)
- Large drawdown periods (>20%)
- Declining performance in recent years
- Win rate < 30%
- Profit factor < 1.0

## Best Practices

### Data Requirements
- Ensure all data files are present in the correct format
- Check for missing days or gaps in data
- Verify timezone consistency

### Interpretation
- Backtest results don't guarantee future performance
- Consider transaction costs and slippage in real trading
- Test on out-of-sample data before live trading
- Monitor strategy degradation over time

### Risk Management
- Never risk more than 1-2% of capital per trade
- Use proper position sizing
- Set maximum daily loss limits
- Monitor correlation with market conditions

## Troubleshooting

### Error: File Not Found
```
FileNotFoundError: CSV file not found
```
**Solution**: Ensure data files are in the correct directory with proper naming (e.g., "2018 15m.csv")

### Error: No Trades Generated
```
No trades generated for 1m
```
**Solution**: Check if data contains 8:30 AM candles. Verify trading hours filter.

### Memory Error
```
MemoryError: Unable to allocate array
```
**Solution**: Process fewer years at once, or reduce timeframe scope.

### Missing Visualizations
```
No module named 'matplotlib'
```
**Solution**: Install all requirements: `pip install -r requirements.txt`

## Advanced Usage

### Running Individual Timeframes

```python
from main import run_backtest_for_timeframe

# Test only 15-minute timeframe
result = run_backtest_for_timeframe(
    timeframe='15m',
    start_year=2020,
    end_year=2024,
    initial_capital=10000
)
```

### Exporting Custom Reports

```python
from report_generator import ReportGenerator

# Create custom report
report = ReportGenerator(all_results)
report.generate_markdown_report('custom_report.md')
```

### Analyzing Specific Periods

```python
import pandas as pd

trades = pd.read_csv('results/trades_15m.csv')
trades['entry_time'] = pd.to_datetime(trades['entry_time'])

# Filter 2022 trades only
trades_2022 = trades[trades['entry_time'].dt.year == 2022]
print(f"2022 Performance: ${trades_2022['pnl'].sum():.2f}")
```

## Support and Contributing

For issues, questions, or contributions:
1. Check existing issues on GitHub
2. Create detailed bug reports with error logs
3. Submit pull requests with clear descriptions
4. Follow existing code style and conventions

## License

MIT License - See LICENSE file for details

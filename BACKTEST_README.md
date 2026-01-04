# NQ FVG Inversion Strategy Backtest

## Overview

This is a complete Python backtesting script for a Fair Value Gap (FVG) inversion trading strategy on Nasdaq futures (NQ) using 5-minute data from 2018 to 2025.

## Strategy Description

### Technical Concepts

**Fair Value Gap (FVG)** - Based on ICT (Inner Circle Trader) concepts:
- **Bearish FVG**: 3-candle formation where Low of candle 1 > High of candle 3
- **Bullish FVG**: 3-candle formation where High of candle 1 < Low of candle 3

**FVG Inversion Signals**:
- **Long Signal**: After a Bearish FVG forms, a candle closes STRICTLY above the top of the gap (Low of candle 1)
- **Short Signal**: After a Bullish FVG forms, a candle closes STRICTLY below the bottom of the gap (High of candle 1)

### Trading Rules

1. **Time Filter (London Killzone)**: Only analyze candles between 01:00 and 04:00 (local Chicago time)
2. **Trend Filter (VWAP)**: 
   - Long: Signal candle close must be > current VWAP
   - Short: Signal candle close must be < current VWAP
3. **Entry**: Immediately at the close of the candle that validates FVG Inversion + VWAP condition
4. **Stop Loss (SL)**:
   - Long: Placed below the Low of the entry signal candle
   - Short: Placed above the High of the entry signal candle
5. **Take Profit (TP)**: Fixed 1:1 Risk/Reward ratio (Distance Entry-TP = Distance Entry-SL)

### Risk Management

- Maximum 1 trade per day (stop trading after first trade, win or lose)
- No overnight positions (forced close at 16:00 if still open)

## Installation

### Requirements

- Python 3.7 or higher
- pandas >= 2.0.0
- numpy >= 1.24.0
- matplotlib >= 3.7.0

### Install Dependencies

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install pandas numpy matplotlib
```

## Data Format

The script expects CSV files in the following format:

- **Location**: Same directory as the script
- **File naming**: `2018 5m.csv`, `2019 5m.csv`, ..., `2025 5m.csv`
- **Format**: Semicolon-separated (`;`)
- **Columns**: 
  - Column1: Date (DD/MM/YYYY)
  - Column2: Time (HH:MM:SS)
  - Column3: Open
  - Column4: High
  - Column5: Low
  - Column6: Close
  - Column7: Volume

**Note**: Data is already in Chicago timezone - no conversion is performed.

## Usage

### Basic Usage

Simply run the script:

```bash
python backtest_nq_fvg_strategy.py
```

### Using the Backtester Class

```python
from backtest_nq_fvg_strategy import NQFVGBacktester

# Initialize backtester
backtester = NQFVGBacktester()

# Run complete backtest
performance, trades = backtester.run_backtest()

# Access results
print(f"Total trades: {performance['total_trades']}")
print(f"Win rate: {performance['win_rate']:.2f}%")
print(f"Profit factor: {performance['profit_factor']:.2f}")
```

### Custom Analysis

```python
# Initialize and load data
backtester = NQFVGBacktester()
backtester.load_data()
backtester.calculate_vwap()
backtester.detect_fvg()
backtester.apply_time_filter()
backtester.detect_fvg_inversions()
backtester.apply_vwap_filter()
backtester.execute_trades()
backtester.calculate_performance()

# Access the dataframe with all indicators
df = backtester.df

# Access trades
trades = backtester.trades_df

# Custom plotting
backtester.plot_trades_on_chart(
    start_date='2024-01-01',
    end_date='2024-03-31',
    save_path='custom_chart.png'
)
```

## Output Files

After running the backtest, the following files are generated:

1. **backtest_results.png**: Performance visualization including:
   - Cumulative PnL chart
   - Individual trade PnL bar chart
   - Drawdown chart

2. **trades_chart_sample.png**: Price chart with first 50 trades marked, showing:
   - Entry and exit points
   - Long vs Short trades
   - Win vs Loss outcomes

3. **backtest_trades.csv**: Complete trade log with columns:
   - entry_time, exit_time
   - direction (Long/Short)
   - entry_price, exit_price
   - sl (stop loss), tp (take profit)
   - pnl (profit/loss in points)
   - result (Win/Loss/Force Close)
   - risk (distance to SL)

## Performance Metrics

The script calculates and displays:

- **Total Trades**: Number of trades executed
- **Wins/Losses**: Count of winning and losing trades
- **Force Closes**: Trades closed at 16:00 time limit
- **Win Rate**: Percentage of winning trades
- **Total Return**: Net profit/loss in points
- **Gross Profit/Loss**: Sum of all wins / sum of all losses
- **Profit Factor**: Ratio of gross profit to gross loss
- **Max Drawdown**: Largest peak-to-trough decline
- **Average Win/Loss/Trade**: Mean profit for each category

## Example Results

Based on the backtest from 2018-2025:

```
============================================================
PERFORMANCE METRICS
============================================================
Total Trades: 2022
Wins: 960
Losses: 1062
Force Closes: 0
Win Rate: 47.48%

Total Return: -857.06 points
Gross Profit: 11417.67 points
Gross Loss: 12274.73 points
Profit Factor: 0.93
Max Drawdown: -1468.27 points

Average Win: 11.89 points
Average Loss: -11.56 points
Average Trade: -0.42 points
============================================================
```

## Key Functions

### NQFVGBacktester Class Methods

- `load_data()`: Load and merge all CSV files
- `calculate_vwap()`: Calculate VWAP with daily reset
- `detect_fvg()`: Detect Bearish and Bullish Fair Value Gaps
- `apply_time_filter()`: Filter for London Killzone (01:00-04:00)
- `detect_fvg_inversions()`: Detect FVG inversion signals
- `apply_vwap_filter()`: Filter signals based on VWAP trend
- `execute_trades()`: Execute trades with SL/TP management
- `calculate_performance()`: Calculate performance metrics
- `print_performance()`: Display performance summary
- `plot_results()`: Generate performance visualization
- `plot_trades_on_chart()`: Plot trades on price chart
- `run_backtest()`: Execute complete backtest pipeline

## Customization

### Modify Time Filter

Edit the `apply_time_filter()` method to change trading hours:

```python
def apply_time_filter(self):
    # Change to different hours, e.g., 08:00-12:00
    df['In_Killzone'] = (
        ((df['Hour'] >= 8) & (df['Hour'] < 12))
    )
```

### Modify Risk/Reward Ratio

Edit the `execute_trades()` method:

```python
# Change from 1:1 to 2:1 R/R
tp = entry + (risk * 2)  # For long trades
tp = entry - (risk * 2)  # For short trades
```

### Add Additional Filters

You can add more filters in the main `run_backtest()` workflow:

```python
def run_backtest(self):
    # ... existing code ...
    self.apply_vwap_filter()
    
    # Add your custom filter here
    self.apply_custom_filter()
    
    self.execute_trades()
    # ... rest of code ...
```

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError**: Install required packages
   ```bash
   pip install pandas numpy matplotlib
   ```

2. **File not found**: Ensure CSV files are in the same directory as the script

3. **Memory errors**: For large datasets, consider processing year by year

4. **Plotting issues**: If running on a server without display, ensure matplotlib backend is set correctly

## Notes

- The data is already in Chicago timezone - no timezone conversion is performed
- VWAP resets at the start of each trading day
- The strategy trades a maximum of once per day
- All prices are in points (not dollars/contracts)
- The backtest assumes perfect execution at signal close prices

## License

This script is provided as-is for educational and research purposes.

## Author

Created for backtesting NQ FVG Inversion Strategy (2018-2025)

# FVG (Fair Value Gap) Trading Strategy Backtesting System

## Overview

This is a comprehensive backtesting system designed to analyze Fair Value Gap (FVG) trading strategies across multiple timeframes, stop-loss configurations, and risk-to-reward ratios for the period 2018-2025.

## Features

### 1. FVG Detection
- Automatically detects Fair Value Gaps forming at 8:30 AM local time
- Supports both bullish and bearish FVGs:
  - **Bullish FVG**: High of candle[i-2] < Low of candle[i]
  - **Bearish FVG**: Low of candle[i-2] > High of candle[i]
- Analyzes three timeframes: 1-minute, 5-minute, and 15-minute

### 2. Entry Strategies
- **1-minute timeframe**: Entry at open of 8:32 AM candle
- **5-minute timeframe**: Entry at open of 8:40 AM candle
- **15-minute timeframe**: Entry at open of 9:00 AM candle

### 3. Stop-Loss Configurations
- **Middle of FVG**: Stop-loss at the midpoint of the gap
- **Edge of FVG**: 
  - Long trades: Stop at bottom of FVG
  - Short trades: Stop at top of FVG

### 4. Risk-Reward Ratios
Tests multiple RR ratios: **1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, and 10**

### 5. Comprehensive Analysis
- Win/loss statistics for each configuration
- Profit factor calculations
- Win rate analysis
- P&L tracking
- Yearly performance breakdown

## Installation

### Requirements
```bash
pip install pandas numpy matplotlib seaborn tabulate
```

### Data Files
The system expects CSV files in the format:
- `YYYY 1m.csv` - 1-minute data
- `YYYY 5m.csv` - 5-minute data
- `YYYY 15m.csv` - 15-minute data

For years 2018-2025.

**CSV Format**: Semicolon-delimited with columns:
```
Date;Time;Open;High;Low;Close;Volume
```

## Usage

### Basic Usage
```bash
python3 fvg_backtest.py
```

The script will:
1. Load all available data files (2018-2025)
2. Detect FVGs at 8:30 AM for each trading day
3. Backtest all configuration combinations
4. Generate summary statistics
5. Create visualizations
6. Export results to CSV

### Output Files

All results are saved in the `results/` directory:

#### CSV Files
- `backtest_results_summary.csv` - Summary statistics for each configuration
- `all_trades_detailed.csv` - Individual trade details

#### Visualizations
- `win_rate_by_rr_ratio.png` - Win rate comparison across RR ratios
- `profit_factor_by_rr_ratio.png` - Profit factor analysis
- `win_rate_heatmaps.png` - Heatmaps showing win rates by configuration
- `trades_by_year.png` - Total trades executed per year
- `stop_loss_comparison.png` - Comparison of stop-loss strategies

## Understanding the Results

### Key Metrics

1. **Win Rate**: Percentage of winning trades
   ```
   Win Rate = (Wins / Total Trades) × 100
   ```

2. **Profit Factor**: Ratio of gross profit to gross loss
   ```
   Profit Factor = Gross Profit / Gross Loss
   ```
   - Values > 1.0 indicate profitable strategy
   - Values < 1.0 indicate losing strategy

3. **Total P&L**: Cumulative profit/loss across all trades

4. **Average Win/Loss**: Average profit per winning trade and loss per losing trade

### Summary Tables

The system generates five comprehensive summary tables:

1. **Overall Performance by Timeframe and Stop Loss Type**
   - Aggregated across all years and RR ratios
   - Shows total trades, wins, losses, and win rate

2. **Performance by Risk-Reward Ratio**
   - Aggregated across all configurations
   - Shows how RR ratio affects profitability

3. **Yearly Performance**
   - Shows performance trends over time
   - Helps identify market condition effects

4. **Top 10 Best Performing Configurations**
   - Ranked by profit factor
   - Filtered to configurations with at least 10 trades

5. **Detailed Win Rate Matrix**
   - Separate matrix for each timeframe
   - Shows win rates for each SL type and RR ratio combination

## Strategy Logic

### Trade Execution Flow

1. **Detection Phase** (8:30 AM)
   - Check if a FVG formed at 8:30 AM
   - Calculate FVG boundaries (top, bottom, middle)

2. **Entry Phase** (Varies by timeframe)
   - 1m: Enter at 8:32 AM open
   - 5m: Enter at 8:40 AM open
   - 15m: Enter at 9:00 AM open

3. **Exit Phase** (Intraday)
   - Monitor price action throughout the day
   - Exit on stop-loss hit OR take-profit hit
   - Check stop-loss first (conservative approach)

4. **End of Day**
   - Close any open positions
   - Record trade outcome

### FVG Types

**Bullish FVG** (Long Trade):
```
Candle i-2:  ----
                  GAP (FVG)
Candle i:         ----

Entry: Above FVG
Stop Loss: Middle or Bottom of FVG
Take Profit: Entry + (Risk × RR Ratio)
```

**Bearish FVG** (Short Trade):
```
Candle i:    ----
                  GAP (FVG)
Candle i-2:       ----

Entry: Below FVG
Stop Loss: Middle or Top of FVG
Take Profit: Entry - (Risk × RR Ratio)
```

## Customization

### Modify Parameters

You can customize the backtester by editing the class initialization:

```python
# In fvg_backtest.py, modify these parameters:

# Test different years
self.years = list(range(2018, 2026))

# Test different timeframes
self.timeframes = ['1m', '5m', '15m']

# Test different RR ratios
self.rr_ratios = [1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 10]

# Modify entry times
self.entry_times = {
    '1m': time(8, 32),
    '5m': time(8, 40),
    '15m': time(9, 0)
}
```

### Add New Analysis

The modular design allows easy extension:

```python
# Add new analysis method
def custom_analysis(self):
    df_results = pd.DataFrame(self.results)
    # Your custom analysis here
    return results

# Call from main()
backtester.custom_analysis()
```

## Performance Considerations

- **Memory**: Large datasets (especially 1m data) require significant RAM
- **Processing Time**: Full backtest across all configurations may take several minutes
- **Data Quality**: Results depend on data quality and completeness

## Interpretation Tips

1. **Higher RR Ratios**: Typically show lower win rates but higher profit per win
2. **Lower RR Ratios**: Usually show higher win rates but lower profit per win
3. **Optimal Configuration**: Look for balance between win rate and profit factor
4. **Timeframe Selection**: Different timeframes may perform better in different market conditions
5. **Stop Loss Type**: Edge stops give more room but risk more capital; middle stops exit faster

## Troubleshooting

### Common Issues

1. **File Not Found Error**
   - Ensure CSV files are in the correct directory
   - Check file naming format matches `YYYY Xm.csv`

2. **No FVGs Detected**
   - Verify data contains 8:30 AM timestamps
   - Check data timezone alignment

3. **Memory Error**
   - Process years sequentially instead of all at once
   - Reduce number of timeframes tested simultaneously

4. **Import Errors**
   - Ensure all required packages are installed
   - Use `pip install -r requirements.txt` if provided

## Technical Details

### Data Processing
- Semicolon delimiter parsing
- Datetime conversion and timezone handling
- Missing data handling
- Price normalization

### Trade Simulation
- Realistic order execution (uses candle opens for entry)
- Conservative stop-loss checking (SL checked before TP)
- Intraday-only trades (no overnight positions)
- Slippage not included (assumes perfect execution)

### Statistical Calculations
- Pandas for data aggregation
- NumPy for numerical operations
- Multiple aggregation levels for comprehensive analysis

## Future Enhancements

Potential improvements for future versions:

1. **Commission/Slippage**: Add transaction cost modeling
2. **Position Sizing**: Implement risk-based position sizing
3. **Multiple Entry**: Allow scaling into positions
4. **Trailing Stops**: Add trailing stop-loss functionality
5. **Optimization**: Automated parameter optimization
6. **Walk-Forward Analysis**: Out-of-sample testing
7. **Monte Carlo**: Simulation for robustness testing
8. **Real-time Alerts**: Integration with live trading platforms

## License

This backtesting system is provided as-is for educational and research purposes.

## Disclaimer

**IMPORTANT**: This backtesting system is for educational and research purposes only. Past performance does not guarantee future results. Always practice proper risk management and never risk more than you can afford to lose.

Trading involves substantial risk of loss and is not suitable for all investors. The results shown are hypothetical and do not represent actual trading.

## Support

For issues, questions, or contributions, please refer to the repository documentation.

---

**Version**: 1.0.0  
**Last Updated**: November 24, 2025  
**Author**: Trading Strategy Analyzer

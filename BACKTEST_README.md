# NQ IVFG Strategy Backtester

This Python script implements and backtests the **NQ IVFG (Inverted Fair Value Gap) Strategy** based on the Pine Script strategy (`NQ_IVFG_Strategy.pine`).

## Overview

The script processes historical 5-minute and 4-hour NQ futures data from 2018 to 2025, implements the complete IVFG strategy logic, and generates comprehensive performance reports with visualizations.

## Strategy Components

### 1. Time Filter (London Killzone)
- **Trading Hours**: 01:00 - 05:00
- Only takes trades during this window
- Can be disabled via configuration

### 2. Trend Filter (Multi-Timeframe)
- **Indicator**: EMA 20 on 4-hour timeframe
- **Bullish Trend**: Current price > EMA 20 (4H)
- **Bearish Trend**: Current price < EMA 20 (4H)

### 3. Fair Value Gap (FVG) Detection
- **Bullish FVG**: `low[2] > high[0]` (gap up between 3 bars)
- **Bearish FVG**: `high[2] < low[0]` (gap down between 3 bars)
- Detects gaps on the 5-minute chart

### 4. IVFG Signal (12-Bar Memory)
- **Long Signal**: 
  - Bullish trend + Price crosses above bearish FVG top
  - FVG must have formed within last 12 bars
- **Short Signal**: 
  - Bearish trend + Price crosses below bullish FVG bottom
  - FVG must have formed within last 12 bars

### 5. Risk Management (3 Modes)

#### Mode A - Structural
- **Stop Loss**: Signal candle low/high ± 5 ticks buffer
- **Take Profit**: 2x risk (Risk/Reward Ratio = 1:2)
- Based on actual candle structure

#### Mode B - Fixed Points
- **Stop Loss**: 20 points
- **Take Profit**: 40 points
- Simple fixed distance approach

#### Mode C - ATR Based
- **Stop Loss**: 1.5 × ATR(14)
- **Take Profit**: 3.0 × ATR(14)
- Adapts to market volatility

## Installation

### Requirements
```bash
pip install pandas numpy matplotlib
```

### Python Version
- Python 3.7 or higher

## Usage

### Basic Execution
```bash
python3 backtest_nq_ivfg.py
```

The script will:
1. Load all CSV files (2018-2025) for 5m and 4H data
2. Merge timeframes and calculate indicators
3. Run backtests for all 3 risk management modes
4. Generate comprehensive reports and visualizations

### Configuration

Edit the `Config` class in the script to customize parameters:

```python
class Config:
    # Capital & Costs
    INITIAL_CAPITAL = 100_000
    COMMISSION_PER_TRADE = 2.50
    SLIPPAGE_TICKS = 2
    
    # Time Filter
    SESSION_START_HOUR = 1
    SESSION_END_HOUR = 5
    
    # Strategy Parameters
    EMA_LENGTH = 20
    FVG_LOOKBACK = 12
    
    # Risk Management
    SL_BUFFER_TICKS = 5  # Mode A
    RR_RATIO = 2.0       # Mode A
    
    SL_POINTS_FIXED = 20  # Mode B
    TP_POINTS_FIXED = 40  # Mode B
    
    ATR_LENGTH = 14       # Mode C
    SL_ATR_MULT = 1.5    # Mode C
    TP_ATR_MULT = 3.0    # Mode C
```

## Output Files

All results are saved to the `results/` directory:

### Reports
- **`backtest_report.txt`**: Comprehensive text report with all metrics
- **`comparison.csv`**: Side-by-side comparison of all 3 modes

### Trade Logs
- **`trades_Mode_A.csv`**: All trades for Mode A (Structural)
- **`trades_Mode_B.csv`**: All trades for Mode B (Fixed Points)
- **`trades_Mode_C.csv`**: All trades for Mode C (ATR Based)

### Visualizations

#### Equity Curves
- `equity_curve_Mode_A.png`
- `equity_curve_Mode_B.png`
- `equity_curve_Mode_C.png`

Shows capital growth/decline over time.

#### Drawdown Charts
- `drawdown_Mode_A.png`
- `drawdown_Mode_B.png`
- `drawdown_Mode_C.png`

Shows both dollar and percentage drawdown over time.

#### Trade Distribution
- `trade_distribution_Mode_A.png`
- `trade_distribution_Mode_B.png`
- `trade_distribution_Mode_C.png`

6-panel analysis showing:
1. P&L distribution histogram
2. Trades by hour
3. Trades by day of week
4. Win/Loss by trade type (long/short)
5. Cumulative P&L
6. Trade duration distribution

#### Monthly Returns Heatmap
- `monthly_returns_Mode_A.png`
- `monthly_returns_Mode_B.png`
- `monthly_returns_Mode_C.png`

Color-coded heatmap showing monthly P&L for each year.

## Performance Metrics

The script calculates the following metrics for each mode:

### Trade Statistics
- Total Trades
- Winning Trades
- Losing Trades
- Win Rate (%)
- Average Win ($)
- Average Loss ($)

### Profitability Metrics
- Total P&L ($)
- Total Return (%)
- Profit Factor (Gross Profit / Gross Loss)
- Final Capital ($)

### Risk Metrics
- Maximum Drawdown ($)
- Maximum Drawdown (%)
- Sharpe Ratio (annualized)

### Time-Based Analysis
- Yearly performance breakdown
- Monthly performance breakdown
- Hourly trade distribution
- Day-of-week analysis

## Data Format

The script expects CSV files with semicolon separators:

```
Date;Time;Open;High;Low;Close;Volume
01/01/2018;17:00:00;7503.74;7511.94;7499.64;7511.35;1451
```

### Required Files
- `2018 5m.csv` through `2025 5m.csv` (5-minute data)
- `2018 4H.csv` through `2025 4H.csv` (4-hour data)

Files should be in the repository root directory.

## Key Features

### 1. Accurate Strategy Implementation
- Exact replication of Pine Script logic
- Proper crossover detection
- 12-bar FVG memory system
- Multi-timeframe analysis

### 2. Realistic Trading Costs
- Commission: $2.50 per trade (entry + exit = $5 total)
- Slippage: 2 ticks = $0.50 per side
- NQ tick size: $0.25

### 3. Comprehensive Analysis
- Multiple risk management modes
- Trade-by-trade logs
- Statistical breakdowns
- Visual performance charts

### 4. Performance Optimized
- Efficient FVG detection
- Vectorized calculations where possible
- Progress reporting during execution

## Interpreting Results

### Good Strategy Performance Indicators
- **Win Rate**: > 50% (30-33% achieved - needs improvement)
- **Profit Factor**: > 1.5 (0.47-0.63 achieved - negative edge)
- **Sharpe Ratio**: > 1.0 (negative achieved - indicates losses)
- **Max Drawdown**: < 20% (21-30% achieved - high risk)

### Current Results Summary (2018-2025)

| Metric | Mode A | Mode B | Mode C |
|--------|--------|--------|--------|
| Total Trades | 4,544 | 3,327 | 3,861 |
| Win Rate | 30.90% | 32.52% | 32.71% |
| Profit Factor | 0.47 | 0.63 | 0.56 |
| Total Return | -29.54% | -21.58% | -26.15% |
| Max Drawdown | -29.59% | -21.63% | -26.22% |
| Final Capital | $70,460 | $78,418 | $73,854 |

**Note**: Current results show the strategy is not profitable over the backtest period. Consider:
- Adjusting entry/exit criteria
- Optimizing time filter windows
- Testing different EMA periods
- Refining FVG detection parameters
- Adding additional filters

## Strategy Improvements to Consider

1. **Entry Filters**
   - Add volume confirmation
   - Require stronger trend confirmation
   - Filter for market structure breaks

2. **Exit Management**
   - Implement trailing stops
   - Use time-based exits
   - Add partial profit taking

3. **Risk Management**
   - Dynamic position sizing
   - Volatility-based adjustments
   - Correlation filters

4. **Time Filters**
   - Test different session times
   - Add day-of-week filters
   - Avoid major news events

## Troubleshooting

### Common Issues

**"ModuleNotFoundError: No module named 'pandas'"**
```bash
pip install pandas numpy matplotlib
```

**"File not found" errors**
- Verify CSV files are in the repository root
- Check file names match exactly (case-sensitive)
- Ensure years 2018-2025 are all present

**Memory errors with large datasets**
- Process fewer years at a time
- Reduce FVG lookback period
- Use data sampling for testing

**Slow execution**
- Normal for 554,518 bars (5m data)
- Expect 2-3 minutes per risk mode
- Total runtime: ~10 minutes for all modes

## Technical Notes

### FVG Detection Algorithm
```python
# Bullish FVG: low[i-2] > high[i]
if df['Low'].iloc[i-2] > df['High'].iloc[i]:
    # Gap exists between bar i-2 and bar i
    bull_fvg_top = df['Low'].iloc[i-2]
    bull_fvg_bottom = df['High'].iloc[i]
```

### IVFG Signal Logic
```python
# Long signal example:
# 1. Check if in bullish trend
# 2. Find bearish FVGs within last 12 bars
# 3. Check if price crosses above FVG top
if close > fvg_top and prev_close <= fvg_top:
    # IVFG signal triggered
```

### Multi-Timeframe Synchronization
- 4H EMA calculated on 4H data
- Forward-filled to 5m timeframe
- Ensures no lookahead bias

## License

This script is provided as-is for backtesting purposes. Use at your own risk.

## Author

Generated for backtesting the NQ IVFG Strategy

## Version History

- **v1.0** (2024-12-27): Initial implementation
  - Complete strategy logic
  - 3 risk management modes
  - Comprehensive reporting and visualization

## Support

For issues or questions:
1. Check the output logs for error messages
2. Verify data files are correctly formatted
3. Review configuration parameters
4. Check the generated reports for insights

---

**Disclaimer**: Past performance is not indicative of future results. This backtest uses historical data and does not account for all real-world trading conditions. Always test strategies thoroughly before live trading.

# FVG Consequent Encroachment (C.E.) Backtesting System

## Overview

This is a professional-grade Python backtesting script for the **Fair Value Gap (FVG) with Consequent Encroachment** strategy, based on Smart Money Concepts (ICT methodology).

## Features

- ✅ **Three Risk Management Models** - Switch between aggressive, structural, and adaptive risk approaches
- ✅ **Precise Limit Order Simulation** - Entry at exact C.E. levels (not close prices)
- ✅ **Setup Cancellation Logic** - Automatically invalidates FVG setups if SL broken before entry
- ✅ **Strict Session Management** - Trading window 01:00-05:00, hard exit at 08:00
- ✅ **Multi-Year Data Support** - Loads and combines CSV files from multiple years
- ✅ **Comprehensive Metrics** - Win rate, max drawdown, profit factor, exit breakdown
- ✅ **Performance Visualization** - Cumulative PnL and drawdown charts
- ✅ **Vectorized Operations** - Fast execution using pandas/numpy

## Installation

```bash
pip install pandas numpy matplotlib
```

Or using the requirements file:

```bash
pip install -r requirements_fvg.txt
```

## Data Format

The script expects CSV files with the following format:

```
Column1;Column2;Column3;Column4;Column5;Column6;Column7
01/01/2019;17:00:00;7332.96;7358.66;7326.61;7352.31;1372
```

- **Separator**: Semicolon (`;`)
- **Column1**: Date (DD/MM/YYYY)
- **Column2**: Time (HH:MM:SS)
- **Column3**: Open
- **Column4**: High
- **Column5**: Low
- **Column6**: Close
- **Column7**: Volume

File naming convention: `YYYY Timeframe.csv` (e.g., `2019 5m.csv`)

## Configuration

Edit the following variables in `fvg_ce_backtest.py`:

```python
# Risk Model Selection (1, 2, or 3)
RISK_MODEL = 2

# Trading Session Times
SESSION_START = time(1, 0, 0)   # 01:00 - Start accepting positions
SESSION_END = time(5, 0, 0)     # 05:00 - Stop accepting positions
HARD_EXIT_TIME = time(8, 0, 0)  # 08:00 - Force close all positions

# Data Configuration
TIMEFRAME = '5m'  # Options: '1m', '5m', '15m'
YEARS = [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]
```

## Risk Models

### Model 1: "The Aggressive Sniper" (FVG Border-based Risk)
- **Philosophy**: If price crosses entire FVG, the idea is invalid
- **Stop Loss (Long)**: Below High[i-2] (distal line) - 2 points
- **Stop Loss (Short)**: Above Low[i-2] (distal line) + 2 points
- **Take Profit**: 3x the risk distance (1:3 ratio)
- **Best For**: High conviction setups, tight risk management

### Model 2: "The Structural Defender" (Swing Candle-based Risk)
- **Philosophy**: FVG is part of momentum; true invalidation is the impulse candle
- **Stop Loss (Long)**: Below Low of candle[i] (FVG completion candle)
- **Stop Loss (Short)**: Above High of candle[i]
- **Take Profit**: Fixed 40 points (London session scalping)
- **Best For**: Safer entries, lower risk per trade

### Model 3: "The Volatility Adapter" (ATR-based Dynamic Risk)
- **Philosophy**: Market volatility changes over time - adapt dynamically
- **Stop Loss**: 1.5 × ATR(14) from entry
- **Take Profit**: 3.0 × ATR(14) from entry (1:2 ratio)
- **Best For**: Adaptive to changing market conditions

## Strategy Logic

### 1. FVG Detection
- **Bullish FVG**: High[i-2] < Low[i] (gap between candles)
- **Bearish FVG**: Low[i-2] > High[i]

### 2. Consequent Encroachment Calculation
- **Long C.E.**: (High[i-2] + Low[i]) / 2
- **Short C.E.**: (Low[i-2] + High[i]) / 2

### 3. Entry Trigger
- Price retraces and touches the C.E. level
- Simulated as LIMIT ORDER at exact C.E. price
- Only during trading session (01:00 - 05:00)

### 4. Setup Cancellation
- If price breaks theoretical SL level BEFORE hitting C.E., setup is cancelled
- Uses forward fill (ffill) to propagate levels

### 5. Exit Management
- **Stop Loss**: Based on selected risk model
- **Take Profit**: Based on selected risk model
- **Hard Exit**: All positions closed at 08:00 at Close price

## Usage

```bash
python fvg_ce_backtest.py
```

## Output

The script generates:

1. **Console Output**: Detailed performance metrics including:
   - Total trades, win rate, profit factor
   - Maximum drawdown
   - Exit reason breakdown
   - Average win/loss

2. **Performance Chart**: `fvg_ce_backtest_modelX_Timeframe.png`
   - Cumulative PnL curve
   - Drawdown visualization

3. **Trade Log**: `trade_log_modelX_Timeframe.csv`
   - Detailed record of every trade
   - Entry/exit prices, PnL, timestamps

## Example Results (Model 2, 5m, 2018-2025)

```
Model: The Structural Defender (Swing Candle-based Risk)
Timeframe: 5m
Total Trades:        137
Win Rate:            12.41%
Total PnL:           212.58 points
Maximum Drawdown:    -51.27 points
Profit Factor:       15.26
```

## Golden Rules (Implementation)

✅ **NO timezone conversion** - Uses raw time as-is  
✅ **Strict session filtering** - 01:00 to 05:00 for new positions only  
✅ **Hard exit at 08:00** - All positions closed at Close price  
✅ **Precise limit orders** - Entry at C.E. level, not close price  
✅ **Setup cancellation** - Invalidates setups if SL broken before entry  

## Performance Tips

- **5-minute timeframe** recommended for optimal signal quality
- **Risk Model 2** provides best balance of safety and returns
- **Session times** are critical - London open session (01:00-05:00) captures best setups
- **Hard exit** prevents overnight risk exposure

## File Structure

```
├── fvg_ce_backtest.py          # Main backtesting script
├── README_FVG_CE.md            # This documentation
├── requirements_fvg.txt        # Python dependencies
├── 2018 5m.csv                 # Data files (example)
├── 2019 5m.csv
├── ...
└── Output files:
    ├── fvg_ce_backtest_model2_5m.png
    └── trade_log_model2_5m.csv
```

## Testing Different Configurations

```python
# Test Model 1 (Aggressive)
RISK_MODEL = 1

# Test with 15-minute timeframe
TIMEFRAME = '15m'

# Test specific years only
YEARS = [2023, 2024, 2025]

# Adjust session times for different markets
SESSION_START = time(2, 0, 0)   # 02:00
SESSION_END = time(6, 0, 0)     # 06:00
```

## Technical Details

- **Language**: Python 3.7+
- **Dependencies**: pandas, numpy, matplotlib
- **Processing**: Vectorized operations for performance
- **Memory**: Efficient handling of multi-year datasets
- **Data Points**: ~554,000 5-minute candles (2018-2025)

## Credits

- **Strategy**: ICT Smart Money Concepts
- **Concept**: Fair Value Gap with Consequent Encroachment
- **Implementation**: Senior Quantitative Developer
- **Date**: December 2025

## License

This script is provided for educational and research purposes. Use at your own risk.

---

**Note**: Past performance does not guarantee future results. Always test thoroughly before live trading.

# ICT Three Strategies Backtesting System

## Overview

A comprehensive, modular Python backtesting system for comparing three distinct ICT (Inner Circle Trader) strategies on NQ (Nasdaq 100) Futures data from 2018 to present.

## Strategies Implemented

### Strategy A: "Silver Bullet" (Time-Based)
- **Time Window**: 10:00 AM - 11:00 AM EST (New York Time)
- **Setup**: Liquidity sweep of previous session high/low followed by Fair Value Gap (FVG) creation on M5 chart
- **Entry**: Limit order at FVG proximal line (FVG Low for buys, FVG High for sells)
- **Stop Loss**: 5 points below/above the Swing Low/High formed before the FVG
- **Take Profit**: Fixed 2:1 Risk/Reward Ratio

### Strategy B: "2022 Mentorship Model" (Structure-Based)
- **Context**: H1 timeframe trend bias using EMA 50 (Price > EMA 50 = Bullish)
- **Trigger**: M5 Market Structure Shift (MSS) aligned with H1 trend
- **Confirmation**: Displacement must leave a specific FVG
- **Entry**: Limit order at FVG proximal line
- **Stop Loss**: Above/Below the Swing High/Low that caused the MSS
- **Take Profit**: Next major Swing Point (Liquidity Pool)

### Strategy C: "Unicorn Model" (OB + FVG Confluence)
- **Setup**: Breaker Block (failed Order Block) overlapping with Fair Value Gap on M15 chart
- **Entry**: Market execution when price touches the overlapping zone
- **Stop Loss**: Strictly outside the Breaker Block range
- **Take Profit**: Fixed 3:1 Risk/Reward Ratio

## ICT Concepts Implemented

### 1. Swing Points
- **Definition**: 3-candle fractal pattern
- **Swing High**: High[i] > High[i-1] AND High[i] > High[i+1]
- **Swing Low**: Low[i] < Low[i-1] AND Low[i] < Low[i+1]
- **Implementation**: Vectorized approach for efficiency

### 2. Fair Value Gaps (FVG)
- **Bullish FVG**: When Low[i] > High[i-2] (gap up)
  - Gap zone: Between High[i-2] and Low[i]
  - Entry: Proximal line (lower boundary)
  
- **Bearish FVG**: When High[i] < Low[i-2] (gap down)
  - Gap zone: Between Low[i-2] and High[i]
  - Entry: Proximal line (upper boundary)

### 3. Market Structure Shift (MSS)
- **Bullish MSS**: Price closes above a recent Swing High with displacement (large body candle)
- **Bearish MSS**: Price closes below a recent Swing Low with displacement
- **Displacement**: Body > 50% of candle range

### 4. Order Blocks (OB)
- **Bullish OB**: Last down-candle (red) before a move that caused Bullish MSS and left an FVG
- **Bearish OB**: Last up-candle (green) before a move that caused Bearish MSS and left an FVG

## Architecture

### Phase 1: Feature Engineering (`ICT_Features` class)
Detects and adds ICT features to dataframes:
- Swing Points
- Fair Value Gaps
- Market Structure Shifts
- Order Blocks

### Phase 2: Data Loading (`DataLoader` class)
- Loads multi-timeframe data (M5, M15, H1)
- Handles timezone conversion from UTC to US/Eastern
- Supports year range specification

### Phase 3: Backtesting (`Backtester` class)
- Event-driven trade simulation
- Multi-timeframe logic
- Position sizing (1% risk per trade)
- Trade execution with limit and market orders

### Phase 4: Reporting
- Performance metrics for each strategy
- Equity curve visualization
- Comprehensive comparison report

## Installation

```bash
pip install pandas numpy matplotlib
```

## Usage

### Basic Usage (Default: 2023-2024)

```bash
python ict_three_strategies_backtest.py
```

### Custom Year Range

```python
from ict_three_strategies_backtest import main

# Test on 2018-2025 data
main(start_year=2018, end_year=2025)

# Test on single year
main(start_year=2024, end_year=2024)
```

### Using Individual Components

```python
from ict_three_strategies_backtest import DataLoader, ICT_Features, Backtester

# Load data
loader = DataLoader()
m5_data = loader.load_data('5m', start_year=2023, end_year=2024)

# Apply ICT features
features = ICT_Features(m5_data)
features.detect_swing_points(window=1)\
        .detect_fvg()\
        .detect_mss(lookback=20)\
        .detect_order_blocks()

m5_featured = features.get_dataframe()
```

## Sample Output (2023-2024 Backtest)

```
================================================================================
ICT STRATEGIES COMPARISON REPORT
================================================================================

Initial Capital: $100,000.00
Risk Per Trade: 1.0%
Point Value: $20

--------------------------------------------------------------------------------

Strategy A: Silver Bullet
--------------------------------------------------------------------------------
Total Number of Trades:  71
Winning Trades:          18
Losing Trades:           53
Win Rate:                25.35%
Total Net Profit:        $-16,156.69
Profit Factor:           0.68
Maximum Drawdown:        23.11%
Final Capital:           $83,843.31
Return:                  -16.16%

Strategy B: 2022 Mentorship Model
--------------------------------------------------------------------------------
Total Number of Trades:  1302
Winning Trades:          830
Losing Trades:           472
Win Rate:                63.75%
Total Net Profit:        $35,311.84
Profit Factor:           1.06
Maximum Drawdown:        23.95%
Final Capital:           $135,311.84
Return:                  35.31%

Strategy C: Unicorn Model
--------------------------------------------------------------------------------
Total Number of Trades:  333
Winning Trades:          94
Losing Trades:           239
Win Rate:                28.23%
Total Net Profit:        $45,717.14
Profit Factor:           1.16
Maximum Drawdown:        31.38%
Final Capital:           $145,717.14
Return:                  45.72%

================================================================================
```

## Key Insights

### Strategy Performance Summary (2023-2024)

1. **Best Overall**: Strategy C (Unicorn Model)
   - Highest return: +45.72%
   - Balanced trade count: 333 trades
   - Good profit factor: 1.16

2. **Most Consistent**: Strategy B (2022 Mentorship Model)
   - Highest win rate: 63.75%
   - Most trades: 1,302
   - Solid return: +35.31%

3. **Needs Refinement**: Strategy A (Silver Bullet)
   - Negative return: -16.16%
   - Low win rate: 25.35%
   - Requires additional filters or different time window

## Performance Metrics Explained

- **Win Rate**: Percentage of winning trades
- **Total Net Profit**: Cumulative profit/loss in USD
- **Profit Factor**: Gross profit / Gross loss (>1 is profitable)
- **Maximum Drawdown**: Largest peak-to-trough decline in equity
- **Return**: Percentage return on initial capital

## Risk Management

- **Starting Capital**: $100,000
- **Risk Per Trade**: 1% of current capital
- **NQ Point Value**: $20 per point
- **Position Sizing**: Dynamically calculated based on stop loss distance

## Data Requirements

The script expects NQ Futures data in CSV format with the following structure:
- **Separator**: Semicolon (;)
- **Columns**: Date, Time, Open, High, Low, Close, Volume
- **Date Format**: DD/MM/YYYY
- **Time Format**: HH:MM:SS
- **Timezone**: UTC (converted to US/Eastern internally)

### File Naming Convention
- 5-minute: `YYYY 5m.csv`
- 15-minute: `YYYY 15m.csv`
- 1-hour: `YYYY 1H.csv`

## Technical Details

### Optimization Features
- Vectorized swing point detection for 3-candle fractals
- Efficient pandas operations throughout
- Event-driven backtesting to handle multi-timeframe logic
- Memory-efficient data handling

### Timezone Handling
All data is automatically converted from UTC to US/Eastern for accurate session-based analysis (especially important for Silver Bullet strategy).

## Future Enhancements

1. Add support for M1 data (currently in zip/xlsx format)
2. Implement commission and slippage
3. Add more sophisticated exit strategies (trailing stops, partial exits)
4. Include additional ICT concepts (Premium/Discount zones, Liquidity Voids)
5. Add optimization routines for parameter tuning
6. Export trade log to CSV for detailed analysis

## License

This script is for educational and research purposes. Always backtest thoroughly before live trading.

## Credits

Based on ICT (Inner Circle Trader) concepts and Smart Money trading methodology.

# ICT Fair Value Gap (FVG) Reversal Strategy - Backtest Documentation

## Overview

This is a comprehensive backtesting system for an ICT (Inner Circle Trader) Fair Value Gap reversal strategy with hierarchical setup classification based on confluence factors.

## Strategy Description

### Core Concept
The strategy identifies high-probability reversal opportunities using Fair Value Gaps (FVG) with multiple layers of confluence to classify setup quality.

### Time Constraints (ABSOLUTE)
- **Entry Window**: 01:00 - 04:00 (local time in data)
- **TP2 Force Close**: 05:00 (if TP not hit)
- **All Positions Force Close**: 06:00 (regardless of status)

## Setup Classification Hierarchy

### Setup C - Low Probability
**Requirements:**
- Formation of FVG (Bullish or Bearish) on 5m or 15m
- Market Structure Shift (MSS) - price breaks local structure before FVG
- **No liquidity filter**

### Setup B - Standard Probability
**Requirements:**
- All Setup C conditions, PLUS:
- **Liquidity Sweep (Turtle Soup)**: Movement creating FVG must sweep a swing high/low that's at least 20 bars old

### Setup A - High Probability
**Requirements:**
- All Setup B conditions, PLUS:
- **Displacement Filter**: FVG-creating candle body > 2x average body size of last 10 candles
- **OTE Zone (Optimal Trade Entry)**: Entry in 62-79% retracement zone of manipulation range

### Setup A+ - Unicorn/Perfect Setup
**Requirements:**
- All Setup A conditions, PLUS:
- **Breaker Block Confluence**: FVG overlaps with a breaker block (old demand/supply zone that flipped)
- **London Macro Timing**: Entry during London macro windows:
  - Macro 1: 02:33 - 03:00
  - Macro 2 (Silver Bullet): 03:00 - 04:00

## Money Management

### Position Sizing
- **Risk**: 1% of capital per trade
- **NQ Point Value**: $20 per point

### Entry
- **Limit Order** at FVG proximal line (entry boundary):
  - Bullish FVG: Lower boundary (previous high)
  - Bearish FVG: Upper boundary (previous low)

### Stop Loss
- Placed at swing extreme (high/low that created the move)
- **Buffer**: +2 points beyond swing extreme for safety

### Take Profit (Split Target)
- **50% Position**: Closed at 2R (Risk:Reward ratio of 1:2)
- **50% Position**: Closed at 2.5 Standard Deviations of manipulation range
- **Alternative**: Force close remaining position at 05:00 if TP2 not reached

## Technical Indicators

### Fair Value Gap (FVG)
3-candle pattern showing inefficiency:
- **Bullish FVG**: Low[i] > High[i-2] (gap up)
- **Bearish FVG**: High[i] < Low[i-2] (gap down)

### Market Structure Shift (MSS)
Break of structure indicating trend change:
- **Bullish MSS**: Price breaks above recent swing high
- **Bearish MSS**: Price breaks below recent swing low

### Liquidity Sweep
Price hunts stop losses before reversal:
- Sweeps swing points at least 20 bars old
- Creates "Turtle Soup" pattern (false breakout)

### Displacement
Strong impulsive move indicating institutional activity:
- Candle body > 2x average body size
- Shows conviction in the move

### OTE (Optimal Trade Entry)
Entry in discount/premium zone:
- **Bullish**: 62-79% retracement from high (discount)
- **Bearish**: 62-79% retracement from low (premium)

### Breaker Block
Old support/resistance that flipped:
- Previous demand zone becomes supply (bearish)
- Previous supply zone becomes demand (bullish)

## Data Format

### Input CSV Files
Expected format (semicolon-separated):
```
Column1;Column2;Column3;Column4;Column5;Column6;Column7
Date;Time;Open;High;Low;Close;Volume
01/01/2024;17:00:00;18244.57923;18248.331274;18238.951165;18241.631196;1308
```

### Supported Timeframes
- 5-minute (5m)
- 15-minute (15m)
- Strategy uses 15m for structure, 5m for precision entries

## Usage

### Basic Execution
```python
from fvg_reversal_backtest import FVGReversalBacktest

# Initialize backtest
backtest = FVGReversalBacktest(
    capital=100000,      # Starting capital
    risk_per_trade=0.01  # 1% risk per trade
)

# Run backtest for specific years
trades = backtest.run_backtest(years=[2024])

# Generate comparative results
results = backtest.generate_results()
```

### Command Line
```bash
python fvg_reversal_backtest.py
```

## Output

### Trade Log CSV
File: `fvg_reversal_trades.csv`

Contains detailed information for each trade:
- Entry/exit times and prices
- Setup classification
- Position size
- Stop loss and take profit levels
- P&L and R-multiple
- Exit reason

### Results Summary CSV
File: `fvg_reversal_results.csv`

Comparative metrics by setup class:
- Number of trades
- Win rate (%)
- Profit factor
- Maximum drawdown
- Net profit
- Average R-multiple

### Console Output
Real-time progress and summary statistics during execution.

## Performance Metrics

### Metrics Calculated
1. **Win Rate**: Percentage of winning trades
2. **Profit Factor**: Gross profit / Gross loss
3. **Maximum Drawdown**: Largest peak-to-trough decline
4. **Net Profit**: Total profit/loss in USD
5. **Average R-Multiple**: Average risk-adjusted return

### Interpretation
- **Setup C**: Expected lower win rate but more opportunities
- **Setup B**: Standard performance with liquidity confluence
- **Setup A**: High probability with multiple confluences
- **Setup A+**: Rare but highest quality setups

## Configuration

### Time Windows
Modify in `config` dictionary:
```python
'entry_start_time': time(1, 0),     # 01:00
'entry_end_time': time(4, 0),       # 04:00
'tp_force_close_time': time(5, 0),  # 05:00
'all_force_close_time': time(6, 0), # 06:00
```

### Technical Parameters
```python
'swing_lookback': 20,               # Bars for swing point
'displacement_multiplier': 2.0,     # Body size multiplier
'displacement_lookback': 10,        # Average lookback
'ote_lower': 0.62,                  # OTE lower bound
'ote_upper': 0.79,                  # OTE upper bound
'sl_buffer': 2.0,                   # Stop loss buffer points
'rr_target_1': 2.0,                 # First TP at 2R
'sd_multiplier': 2.5,               # Second TP at 2.5 SD
```

## Dependencies

```python
pandas
numpy
```

Install with:
```bash
pip install pandas numpy
```

## Code Structure

### Main Class: `FVGReversalBacktest`

**Core Methods:**
- `load_data()`: Load and preprocess CSV data
- `detect_fvg()`: Identify Fair Value Gaps
- `detect_swing_points()`: Find swing highs/lows
- `detect_mss()`: Detect Market Structure Shift
- `detect_liquidity_sweep()`: Identify liquidity sweeps
- `check_displacement()`: Verify displacement criteria
- `check_ote_zone()`: Validate OTE entry
- `detect_breaker_block()`: Find breaker block confluence
- `check_london_macro_timing()`: Verify macro timing
- `classify_setup()`: Hierarchical setup classification
- `simulate_trade()`: Execute trade management logic
- `run_backtest()`: Main backtest loop
- `generate_results()`: Calculate and display metrics

## Best Practices

1. **Data Quality**: Ensure CSV files are clean and properly formatted
2. **Multiple Years**: Test across multiple years for robustness
3. **Parameter Tuning**: Adjust parameters based on market conditions
4. **Risk Management**: Never risk more than 1-2% per trade
5. **Setup Quality**: Focus on Setup A and A+ for better results

## Limitations

1. **Slippage**: Not accounted for (assumes perfect fills)
2. **Commissions**: Not included in P&L calculations
3. **Market Impact**: Assumes no impact on price
4. **Overnight Risk**: Positions may be held overnight
5. **Data Gaps**: Missing data may affect results

## Future Enhancements

- [ ] Add slippage and commission modeling
- [ ] Implement real-time scanning capability
- [ ] Add visualization of setups and trades
- [ ] Include correlation with ES (SMT divergence)
- [ ] Add Monte Carlo simulation for robustness testing
- [ ] Implement walk-forward optimization

## References

- ICT (Inner Circle Trader) methodology
- Fair Value Gap concepts
- Market structure analysis
- Liquidity concepts in trading

## Support

For issues, questions, or contributions, please refer to the repository documentation.

---

**Disclaimer**: This is a backtesting tool for educational purposes. Past performance does not guarantee future results. Always practice proper risk management and test strategies thoroughly before live trading.

# Backtest-Trading

## FVG Strategy Backtesting

This repository contains a Python script for backtesting the Fair Value Gap (FVG) inversion strategy on Nasdaq 100 (NQ) 15-minute data.

### FVG Strategy Overview

**Fair Value Gap (FVG)** is a trading concept that identifies gaps in price action:
- **Bearish FVG**: A gap between High[i-2] and Low[i] (gap down)
- **Bullish FVG**: A gap between Low[i-2] and High[i] (gap up)

**Entry Signals**:
- **Long Entry**: Price closes ABOVE the top of a Bearish FVG (inversion)
- **Short Entry**: Price closes BELOW the bottom of a Bullish FVG (inversion)

**Time Window**: 01:00 to 05:00 (no timezone conversion)

### Stop Loss Comparison

The script compares two different Stop Loss (SL) placement strategies:

#### Scenario A: Candle-Based SL (Aggressive)
- **Long Trades**: SL at the Low of the Signal Candle
- **Short Trades**: SL at the High of the Signal Candle

#### Scenario B: Structure-Based SL (Conservative)
- **Long Trades**: SL at the Bottom of the FVG area being inverted
- **Short Trades**: SL at the Top of the FVG area being inverted

### Take Profit Targets

For each scenario, dynamic Take Profit (TP) levels are calculated based on the specific SL distance:
- **TP 1R**: 1x the risk (SL distance)
- **TP 1.5R**: 1.5x the risk
- **TP 2R**: 2x the risk

### Usage

1. **Install dependencies**:
   ```bash
   pip install pandas numpy
   ```

2. **Run the backtest**:
   ```bash
   python3 fvg_backtest_comparison.py
   ```

3. **Output**:
   - Comparative report printed to console
   - Detailed trade logs saved to `trades_scenario_a.csv` and `trades_scenario_b.csv`

### Example Results

```
SCENARIO A: CANDLE-BASED SL (AGGRESSIVE)
Total Trades:        6580
Win Rate:            39.19%
Total Return:        -245.50R

SCENARIO B: STRUCTURE-BASED SL (CONSERVATIVE)
Total Trades:        6580
Win Rate:            46.69%
Total Return:        +468.00R

🏆 WINNER: Scenario B (Structure-Based SL) performs better!
```

### Data Files

The script uses 15-minute historical data from NQ futures contracts:
- Data files: `2018 15m.csv` through `2025 15m.csv`
- Consolidated file: `nq_15m_data.csv` (auto-generated)

### Files

- `fvg_backtest_comparison.py` - Main backtesting script
- `nq_15m_data.csv` - Consolidated 15-minute data (generated)
- `trades_scenario_a.csv` - Detailed trades for Scenario A (generated)
- `trades_scenario_b.csv` - Detailed trades for Scenario B (generated)
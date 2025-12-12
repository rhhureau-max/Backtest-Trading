# SMC Reversal Strategy - Quick Reference Guide

## 📊 Strategy Overview

**Smart Money Concepts (SMC) Reversal Strategy** for NQ Futures 01:00-07:00 session

## 🎯 Trade Setup Requirements

### SHORT Setup
1. **Liquidity Sweep**: Price wicks above a Fractal High, then rejects (closes below)
2. **MSS Confirmation**: Price breaks below a recent significant Fractal Low
3. **Entry**: 50% Fibonacci retracement between sweep high and MSS low
4. **Stop Loss**: Above the sweep high (absolute peak)
5. **Take Profit**: First bearish FVG (or 2R fallback)

### LONG Setup
1. **Liquidity Sweep**: Price wicks below a Fractal Low, then rejects (closes above)
2. **MSS Confirmation**: Price breaks above a recent significant Fractal High
3. **Entry**: 50% Fibonacci retracement between sweep low and MSS high
4. **Stop Loss**: Below the sweep low (absolute bottom)
5. **Take Profit**: First bullish FVG (or 2R fallback)

## 📈 Key Definitions

### Fractal
- **Fractal High**: A high surrounded by 2 lower highs on each side
- **Fractal Low**: A low surrounded by 2 higher lows on each side

### Fair Value Gap (FVG)
- **Bearish FVG**: Gap where `Low[N] > High[N+2]` (downward gap)
- **Bullish FVG**: Gap where `High[N] < Low[N+2]` (upward gap)

### Liquidity Sweep
- Smart money taking out stops at obvious levels before reversing
- Identified by wick beyond fractal + rejection close

### Market Structure Shift (MSS)
- Break of previous swing point in opposite direction
- Confirms change in trend/momentum

## ⚙️ Configuration Parameters

```python
session_start='01:00:00'      # Session start time
session_end='07:00:00'        # Session end time
fractal_periods=2             # Candles each side for fractal
mss_lookback=30               # Lookback for MSS fractals
max_sweep_delay=5             # Max candles after sweep
min_trade_spacing=10          # Minimum candles between trades
```

## 📊 Performance Metrics (2023-2025)

| Metric | Value |
|--------|-------|
| Total Trades | 709 |
| Win Rate | 55.15% |
| Avg R:R | 1.21:1 |
| Profit Factor | 1.06 |
| Max Drawdown | -19.08% |
| ROI | +61.68% |

## 🚀 Quick Start

```bash
# Run backtest with default settings
python3 smc_reversal_backtest_01_07.py

# View results
cat README_SMC_REVERSAL_BACKTEST.md
open smc_reversal_equity_curve.png
```

## 📁 Output Files

1. **smc_reversal_backtest_01_07.py** - Main backtest script
2. **README_SMC_REVERSAL_BACKTEST.md** - Full performance report
3. **smc_reversal_equity_curve.png** - Equity & drawdown charts

## 🎓 SMC Trading Rules

### Entry Rules
✅ Wait for liquidity sweep (wick beyond fractal + rejection)
✅ Confirm MSS (break of opposite structure)
✅ Enter on 50% fib retracement
✅ Only during 01:00-07:00 session

### Exit Rules
✅ Take profit at first FVG (or 2R)
✅ Stop loss beyond sweep point
✅ Exit can occur outside session hours

### Risk Management
✅ 1% account risk per trade
✅ Minimum 10-candle spacing between trades
✅ Realistic fill simulation
✅ Dynamic R:R based on FVG distance

## 🔍 Trade Example

**SHORT Trade:**
```
1. Fractal High at 12,150
2. Price sweeps to 12,165 (wick), closes at 12,145 ✓
3. Price breaks below Fractal Low at 12,100 (MSS) ✓
4. Entry: 50% fib = 12,132.5
5. Stop Loss: 12,165 (risk = 32.5 points)
6. Take Profit: First bearish FVG at 12,090 (reward = 42.5 points)
7. R:R = 1.31:1
```

## 🛠️ Customization Examples

### Conservative (Higher Quality Setups)
```python
fractal_periods=3            # Larger fractals
mss_lookback=20              # Closer MSS
max_sweep_delay=3            # Tighter rejection
```

### Aggressive (More Setups)
```python
fractal_periods=2            # Smaller fractals
mss_lookback=40              # Wider MSS search
max_sweep_delay=7            # Allow delayed rejection
```

## ⚠️ Important Notes

- Strategy designed for 01:00-07:00 session (high volatility)
- NQ point value = $20
- No slippage or commissions included in backtest
- Past performance ≠ future results
- Always use proper risk management

## 📞 Support & Optimization

For strategy optimization, consider:
- Adding higher timeframe bias filter
- Implementing session-specific parameters
- Enhancing FVG detection logic
- Adding volume confirmation
- Incorporating order flow analysis

---

**Created**: 2025-12-12
**Version**: 1.0
**Data**: NQ 5-minute (2023-2025)

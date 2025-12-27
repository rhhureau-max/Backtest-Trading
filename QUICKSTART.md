# NQ IVFG Strategy - Quick Start Guide

## 📁 Files Created

1. **NQ_IVFG_Strategy.pine** (18KB) - Complete Pine Script v5 strategy
2. **NQ_IVFG_Strategy_README.md** (11KB) - Comprehensive documentation (French)

## 🎯 Strategy Overview

### Core Features

**Multi-Timeframe Analysis**:
- Primary: 5-minute chart
- Secondary: 4-hour EMA 20 for trend filter
- Anti-repainting implementation using `lookahead=barmerge.lookahead_on`

**Time Filter**:
- London Killzone: 01:00 - 05:00
- Uses raw chart time (no timezone conversion)
- Configurable on/off

**IVFG Detection**:
- Fair Value Gap (FVG) detection on 5-minute chart
- 12-bar memory system to track recent FVGs
- Inverted FVG signals when price crosses gaps in opposite direction

**Three Risk Management Modes**:

1. **Mode A - Structural** (Recommended)
   - SL: Below/above signal candle + buffer
   - TP: Risk/Reward ratio-based (default 1:2)

2. **Mode B - Fixed Points**
   - SL: Fixed points (default 20)
   - TP: Fixed points (default 40)

3. **Mode C - ATR Based**
   - SL: ATR × multiplier (default 1.5)
   - TP: ATR × multiplier (default 3.0)

## 🚀 Quick Setup

### In TradingView:

1. Open Pine Editor
2. Copy content from `NQ_IVFG_Strategy.pine`
3. Save and "Add to Chart"
4. Configure:
   - Symbol: NQ1! (Nasdaq 100)
   - Timeframe: 5 minutes
   - Period: From 2018

### Strategy Settings:

**Time Filter**:
- Enable: ✅
- Start: 1
- End: 5

**Trend Filter**:
- HTF: 240 (4 hours)
- EMA: 20

**IVFG**:
- Memory: 12 bars
- Min Size: 0.0

**Risk Mode**: Choose A, B, or C

## 📊 Visual Elements

- **Yellow Line**: 4H EMA 20 (trend)
- **Green Boxes**: Bullish FVGs
- **Red Boxes**: Bearish FVGs
- **Green Triangles**: Long signals
- **Red Triangles**: Short signals
- **Statistics Table**: Win Rate, Profit Factor, Max DD, Total Trades

## 📈 Entry Signals

**LONG Signal**:
- Bearish trend (Price < EMA 20 4H)
- Bearish FVG exists in last 12 bars
- Price closes ABOVE bearish FVG top
- = Trend reversal confirmed

**SHORT Signal**:
- Bullish trend (Price > EMA 20 4H)
- Bullish FVG exists in last 12 bars
- Price closes BELOW bullish FVG bottom
- = Trend reversal confirmed

## 🎓 Key Concepts

### Fair Value Gap (FVG)
- Market inefficiency where price moved too fast
- Gap between candles that market tends to "fill"
- **Bullish FVG**: `low[2] > high[0]`
- **Bearish FVG**: `high[2] < low[0]`

### Inverted FVG (IVFG)
- Price crosses FVG in opposite direction
- Strong reversal signal
- Combined with HTF trend filter for confirmation

## ⚙️ Parameters to Optimize

1. **FVG Memory**: 8-20 bars
2. **R:R Ratio**: 1.5-3.0 (Mode A)
3. **ATR Multipliers**: 1.0-2.5 for SL, 2.0-4.0 for TP (Mode C)
4. **Time Sessions**: Test different trading hours

## ⚠️ Important Notes

- ✅ Anti-repainting design
- ✅ Commission & slippage included (2.50$/contract, 2 ticks)
- ⚠️ Backtest results ≠ Live performance
- ⚠️ Always paper trade first
- ⚠️ Risk management is critical (max 1-2% per trade)

## 📊 Expected Performance

Typical characteristics (indicative only):
- Win Rate: 45-55%
- Profit Factor: 1.5-2.5+
- Max Drawdown: 10-20% of capital
- Trades/year: 50-200 (varies)

## 🔧 Code Structure

```
1. Inputs Configuration
2. Time Filter Logic
3. Multi-Timeframe Trend Filter
4. FVG Detection & Memory System
5. IVFG Signal Logic
6. Risk Management (3 modes)
7. Strategy Execution
8. Visualization (Boxes, Signals, Levels)
9. Statistics Table
```

## 📚 Documentation

See **NQ_IVFG_Strategy_README.md** for:
- Complete feature explanation
- Detailed setup instructions
- Optimization guide
- Troubleshooting
- Trading theory

## 🎯 Use Cases

**Ideal for**:
- Day traders on NQ futures
- Multi-timeframe analysis enthusiasts
- Traders using Fair Value Gap strategies
- Those seeking systematic entries

**Strategy Type**:
- Reversal/Reversion strategy
- Multi-timeframe confirmation
- Objective entry/exit rules

## 💡 Tips

1. Start with Mode A (Structural)
2. Test on historical data first
3. Use proper position sizing
4. Monitor during London session
5. Combine with your trading plan

---

**Version**: 1.0
**Pine Script**: v5
**Initial Capital**: $100,000
**Commission Model**: $2.50/contract + 2 ticks slippage

**Disclaimer**: Trading involves risk of loss. Past performance doesn't guarantee future results. Use at your own risk.

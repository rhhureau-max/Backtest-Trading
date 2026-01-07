# NQ IVFG Strategy - Quick Reference Guide

## Strategy Configuration at a Glance

### Default Settings (Recommended Starting Point)

```
Initial Capital: $100,000
Timeframe: 5 minutes
Symbol: NQ (Nasdaq 100 Futures)
```

### Time Window Filter
- **Trading Hours**: 01:00 - 05:00 (London Killzone)
- **Timezone**: Raw chart time (UTC/GMT, no offset)

### Trend Filter (Multi-Timeframe)
- **Higher Timeframe**: 4 Hours (240 minutes)
- **Indicator**: EMA 20
- **Rule**: Long when Close > EMA20(4h), Short when Close < EMA20(4h)

### IVFG Signal Parameters
- **Lookback Period**: 12 bars
- **Min FVG Size**: 0 (no minimum)

### Risk Management Modes

#### 🅰️ Mode A - Structural (Default)
```
Safety Buffer: 5 ticks
Risk/Reward Ratio: 2.0
```
**How it works**: Stop loss based on signal candle high/low + buffer, TP calculated from R:R ratio

#### 🅱️ Mode B - Fixed Points
```
Stop Loss: 20 points
Take Profit: 40 points
```
**How it works**: Fixed distance in points for both SL and TP

#### 🅲 Mode C - ATR Based
```
ATR Length: 14
ATR SL Multiplier: 1.5x
ATR TP Multiplier: 3.0x
```
**How it works**: Dynamic stops based on market volatility (ATR indicator)

---

## Entry Signal Logic

### Long Entry Requirements
1. ✅ Bearish FVG detected in last 12 bars
2. ✅ Current candle closes ABOVE the bearish FVG top
3. ✅ Close > EMA20(4h) (bullish trend)
4. ✅ Time is between 01:00 - 05:00

### Short Entry Requirements
1. ✅ Bullish FVG detected in last 12 bars
2. ✅ Current candle closes BELOW the bullish FVG bottom
3. ✅ Close < EMA20(4h) (bearish trend)
4. ✅ Time is between 01:00 - 05:00

---

## Fair Value Gap (FVG) Definition

### Bullish FVG
```
When: low[0] > high[2]
Gap: Between high[2] and low[0]
```

### Bearish FVG
```
When: high[0] < low[2]
Gap: Between low[2] and high[0]
```

### IVFG (Inverted FVG)
The strategy looks for price to close THROUGH a gap in the opposite direction:
- **Long**: Close above bearish FVG = bullish reversal signal
- **Short**: Close below bullish FVG = bearish reversal signal

---

## Performance Metrics (Displayed on Chart)

| Metric | Description | Good Value |
|--------|-------------|------------|
| **Total Trades** | Number of closed trades | N/A |
| **Win Rate** | Percentage of winning trades | ≥ 50% |
| **Profit Factor** | Gross Profit / Gross Loss | ≥ 1.5 |
| **Max Drawdown** | Largest peak-to-trough decline | Lower is better |
| **Net Profit** | Total profit after costs | Positive |

---

## Visual Elements on Chart

| Element | Color | Meaning |
|---------|-------|---------|
| Yellow Line | 🟡 | EMA 20 from 4H timeframe |
| Green Boxes | 🟢 | Bullish FVG zones |
| Red Boxes | 🔴 | Bearish FVG zones |
| Green Arrow Up | ⬆️ | Long entry signal |
| Red Arrow Down | ⬇️ | Short entry signal |

---

## Optimization Checklist

### Phase 1: Initial Testing (Use Default Settings)
- [ ] Run backtest on 2018-2025
- [ ] Check Win Rate (target: 45-60%)
- [ ] Check Profit Factor (target: >1.3)
- [ ] Note Max Drawdown

### Phase 2: Mode Comparison
- [ ] Test Mode A with RR 1.5, 2.0, 2.5
- [ ] Test Mode B with different point values
- [ ] Test Mode C with different ATR multipliers
- [ ] Compare results across all modes

### Phase 3: Parameter Tuning
- [ ] Test EMA lengths: 15, 20, 25, 30
- [ ] Test Lookback bars: 8, 10, 12, 15, 20
- [ ] Test different time windows
- [ ] Test with/without trend filter

### Phase 4: Validation
- [ ] Walk-forward analysis
- [ ] Test on out-of-sample data
- [ ] Monte Carlo simulation (if available)
- [ ] Paper trading period

---

## Common Issues & Solutions

### ❌ Issue: No trades executing
**Solution**: 
- Check if time window matches your chart timezone
- Verify trend filter is not too restrictive
- Check if FVGs are being detected (look for boxes)

### ❌ Issue: Too many false signals
**Solution**:
- Increase minimum FVG size
- Use stricter trend filter
- Reduce lookback period (try 8 instead of 12)

### ❌ Issue: Stops hit too often
**Solution**:
- Switch to Mode C (ATR-based) for adaptive stops
- Increase safety buffer in Mode A
- Increase fixed SL points in Mode B

### ❌ Issue: Poor profit factor
**Solution**:
- Increase R:R ratio in Mode A (try 2.5 or 3.0)
- Use Mode C with higher TP multiplier
- Add additional filters (volume, volatility)

---

## Best Practices

### ✅ DO:
- Test on multiple years of data
- Include commission and slippage
- Paper trade before going live
- Keep a trading journal
- Review trades weekly
- Adjust for market regime changes

### ❌ DON'T:
- Over-optimize on past data
- Use 100% of capital per trade
- Ignore drawdown periods
- Trade without stops
- Change strategy mid-session
- Trade during low-liquidity periods

---

## Quick Command Reference (TradingView)

### Add Strategy to Chart
1. Pine Editor → New → Paste code → Save
2. Add to Chart button

### View Strategy Performance
1. Strategy Tester tab (bottom of screen)
2. Performance Summary tab
3. List of Trades tab

### Modify Parameters
1. Click strategy name on chart
2. Settings ⚙️ icon
3. Inputs tab
4. Adjust and OK

### Export Results
1. Strategy Tester → Performance Summary
2. Right-click → Export to CSV

---

## Support Matrix

| Parameter | Conservative | Moderate | Aggressive |
|-----------|--------------|----------|------------|
| **Risk Mode** | Mode A (RR 2.0) | Mode A (RR 2.5) | Mode C (3x ATR) |
| **Trend Filter** | Always ON | ON | Optional |
| **Lookback** | 8-10 bars | 12 bars | 15-20 bars |
| **Time Window** | 01:00-03:00 | 01:00-05:00 | 00:00-06:00 |
| **Position Size** | 10-20% capital | 30-50% capital | 50-100% capital |

---

## Emergency Actions

### If Strategy Underperforming:
1. **STOP** - Don't trade live immediately
2. **ANALYZE** - Review losing trades
3. **ADJUST** - Modify one parameter at a time
4. **BACKTEST** - Verify improvement
5. **FORWARD TEST** - Paper trade new settings
6. **RESUME** - Only after consistent results

### If Large Drawdown:
1. Reduce position size by 50%
2. Tighten time window (reduce hours)
3. Consider market regime change
4. Take break and reassess strategy
5. Review risk management mode

---

## Contact & Resources

- **Documentation**: See STRATEGY_DOCUMENTATION.md for detailed guide
- **Code**: NQ_IVFG_Strategy.pine
- **Issues**: Open on GitHub repository

**Remember**: This is a tool, not a guarantee. Use proper risk management! 🛡️

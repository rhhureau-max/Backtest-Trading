# NQ IVFG Strategy - Usage Examples

## Example 1: Basic Setup (Recommended for Beginners)

### Configuration
```
Strategy: NQ IVFG Strategy
Timeframe: 5 minutes
Symbol: NQ1! (or NQ)
Date Range: 2018-01-01 to Present
```

### Settings
```
=== Time Window Filter ===
Start Hour: 1
Start Minute: 0
End Hour: 5
End Minute: 0

=== Multi-Timeframe Trend Filter ===
Higher Timeframe: 240 (4 hours)
EMA Length: 20
Use Trend Filter: ✅ ON

=== IVFG Signal Parameters ===
FVG Memory (Lookback Bars): 12
Minimum FVG Size: 0

=== Risk Management Mode ===
Risk Management Mode: Mode A - Structural

=== Mode A - Structural ===
Safety Buffer (ticks): 5
Risk/Reward Ratio: 2.0

=== Display Options ===
Show FVG Boxes: ✅ ON
Show 4H EMA: ✅ ON
Show Performance Table: ✅ ON
```

### Expected Results (Baseline)
These are typical results you might see with default settings:
- Win Rate: 45-55%
- Profit Factor: 1.2-1.8
- Total Trades: Varies by period (10-30 per month typical for London session)

---

## Example 2: Conservative Setup (Lower Risk)

### Ideal For
- New traders
- Risk-averse investors
- Volatile market conditions

### Key Changes from Default
```
=== Risk Management Mode ===
Risk Management Mode: Mode A - Structural

=== Mode A - Structural ===
Safety Buffer (ticks): 10  ⬅️ Increased for safer stops
Risk/Reward Ratio: 1.5     ⬅️ Lower RR, higher win rate

=== IVFG Signal Parameters ===
FVG Memory (Lookback Bars): 8  ⬅️ Less signals, higher quality
Minimum FVG Size: 5            ⬅️ Only larger FVGs

=== Time Window Filter ===
Start Hour: 1
End Hour: 3  ⬅️ Shorter window, best liquidity only
```

### Expected Characteristics
- Fewer trades (more selective)
- Higher win rate (potentially 55-65%)
- Lower profit factor
- Smaller drawdowns

---

## Example 3: Aggressive Setup (Higher Risk/Reward)

### Ideal For
- Experienced traders
- Trend-following preference
- Higher risk tolerance

### Key Changes from Default
```
=== Risk Management Mode ===
Risk Management Mode: Mode C - ATR Based

=== Mode C - ATR Based ===
ATR Length: 14
ATR SL Multiplier: 2.0  ⬅️ Wider stops
ATR TP Multiplier: 4.0  ⬅️ Larger targets

=== IVFG Signal Parameters ===
FVG Memory (Lookback Bars): 20  ⬅️ More signals

=== Multi-Timeframe Trend Filter ===
Use Trend Filter: ✅ ON  ⬅️ Must follow trend
```

### Expected Characteristics
- More trades
- Lower win rate (35-45%)
- Higher profit factor (potentially >2.0)
- Larger individual wins
- Larger drawdowns

---

## Example 4: Fixed Risk Setup (Consistent Position Sizing)

### Ideal For
- Systematic traders
- Testing specific risk levels
- Simple risk management

### Key Changes from Default
```
=== Risk Management Mode ===
Risk Management Mode: Mode B - Fixed Points

=== Mode B - Fixed Points ===
Stop Loss (points): 15
Take Profit (points): 45  ⬅️ 1:3 RR ratio
```

### Use Cases
- **Scalping**: SL=10, TP=20
- **Day Trading**: SL=20, TP=40
- **Swing (intraday)**: SL=30, TP=90

---

## Example 5: Different Time Windows

### London Killzone (Default)
```
Start Hour: 1
End Hour: 5
```
**Characteristics**: High volatility, good trends

### New York Session
```
Start Hour: 13
End Hour: 17
```
**Characteristics**: High volume, strong moves

### Asian Session
```
Start Hour: 23
End Hour: 3
```
**Characteristics**: Lower volatility, ranging

### Extended London
```
Start Hour: 0
End Hour: 8
```
**Characteristics**: More trades, mixed quality

---

## Example 6: Trend-Following Configuration

### Goal
Capture strong trending moves with the 4H trend

### Configuration
```
=== Multi-Timeframe Trend Filter ===
Higher Timeframe: 240
EMA Length: 30  ⬅️ Smoother trend
Use Trend Filter: ✅ ON (REQUIRED)

=== IVFG Signal Parameters ===
FVG Memory (Lookback Bars): 15  ⬅️ More opportunities

=== Risk Management Mode ===
Mode: Mode C - ATR Based

=== Mode C - ATR Based ===
ATR SL Multiplier: 1.5
ATR TP Multiplier: 4.0  ⬅️ Let winners run
```

---

## Example 7: Mean Reversion Configuration

### Goal
Capture reversals at FVG levels

### Configuration
```
=== Multi-Timeframe Trend Filter ===
Use Trend Filter: ❌ OFF  ⬅️ Trade against trend

=== IVFG Signal Parameters ===
FVG Memory (Lookback Bars): 8  ⬅️ Fresh FVGs
Minimum FVG Size: 10  ⬅️ Significant gaps

=== Risk Management Mode ===
Mode: Mode A - Structural

=== Mode A - Structural ===
Safety Buffer (ticks): 3
Risk/Reward Ratio: 1.5  ⬅️ Quick exits
```

**⚠️ Warning**: Higher risk approach, use with caution

---

## Example 8: Optimization Workflow

### Step 1: Baseline Test
```
Period: 2018-2020
Settings: All default
Record: Win Rate, PF, Drawdown
```

### Step 2: Mode Comparison
Test each mode with same period:
```
Mode A: RR 2.0
Mode B: SL=20, TP=40
Mode C: SL=1.5x, TP=3x
```
Choose best performer

### Step 3: Parameter Sweep (Best Mode)
If Mode A won:
```
Test RR: 1.5, 2.0, 2.5, 3.0
Test Buffer: 3, 5, 7, 10
```

### Step 4: Validation
```
Period: 2021-2023 (out of sample)
Settings: Best from Step 3
Verify similar performance
```

### Step 5: Recent Validation
```
Period: 2024-2025
Settings: Same
Check if still working
```

---

## Example 9: Walk-Forward Analysis Setup

### Training Period
```
Dates: 2018-01-01 to 2020-12-31
Action: Optimize parameters
Find: Best RR ratio, lookback period
```

### Test Period
```
Dates: 2021-01-01 to 2021-12-31
Action: Apply optimized settings
Verify: Performance holds up
```

### Repeat
```
Training: 2019-2021
Test: 2022
... and so on
```

---

## Example 10: Multi-Symbol Testing

While the strategy is designed for NQ, you can test on similar instruments:

### NQ (Nasdaq 100)
```
Timeframe: 5m
Time Window: 01:00-05:00
Expected: High volatility, good for IVFG
```

### ES (S&P 500)
```
Timeframe: 5m
Time Window: 01:00-05:00
Note: May need to adjust stops (less volatile)
Adjust: Use Mode C with lower multipliers
```

### RTY (Russell 2000)
```
Timeframe: 5m
Note: More volatile than ES
Adjust: Increase safety buffer or use ATR mode
```

---

## Real Trading Checklist

### Before Going Live

- [ ] Backtested on minimum 3 years of data
- [ ] Walk-forward tested on out-of-sample periods
- [ ] Paper traded for minimum 1 month
- [ ] Achieved target metrics (Win Rate >45%, PF >1.3)
- [ ] Understand maximum drawdown and can handle it
- [ ] Have proper risk management plan (position sizing)
- [ ] Set up proper broker account with low commissions
- [ ] Tested strategy during current market conditions
- [ ] Have emergency stop plan (max daily loss, etc.)
- [ ] Keep trading journal ready

### Daily Routine

1. **Pre-Market** (30 mins before session)
   - Check market news/events
   - Verify strategy is loaded correctly
   - Confirm time window settings match timezone
   - Review yesterday's trades

2. **During Market** (01:00-05:00)
   - Monitor strategy execution
   - Don't interfere with automated entries
   - Note any unusual behavior
   - Check performance table periodically

3. **Post-Market** (After session)
   - Review all trades
   - Update trading journal
   - Check if strategy parameters need adjustment
   - Calculate daily P&L

### Weekly Review

- [ ] Review all trades of the week
- [ ] Calculate weekly metrics
- [ ] Compare to backtested expectations
- [ ] Identify any pattern in losses
- [ ] Adjust if necessary (one parameter at a time)
- [ ] Plan for next week

---

## Troubleshooting Examples

### Problem: Strategy Not Taking Any Trades

**Diagnosis Steps**:
1. Check if FVG boxes appear on chart
   - If NO: FVG detection issue (increase timeframe visibility)
   - If YES: Continue to step 2

2. Check time window
   - Verify your chart timezone
   - Verify Start/End hours match your trading session
   - Test with wider window (00:00-23:59) temporarily

3. Check trend filter
   - Set "Use Trend Filter" to OFF temporarily
   - If trades appear, trend filter is too restrictive
   - Adjust EMA length or timeframe

4. Check IVFG triggers
   - Reduce "Minimum FVG Size" to 0
   - Increase "FVG Memory" to 20

### Problem: Too Many Losing Trades

**Diagnosis Steps**:
1. Check win rate
   - If <40%: Strategy doesn't fit current market
   - Try different time window
   - Increase selectivity (Minimum FVG Size)

2. Check profit factor
   - If <1.0: Losses too large or wins too small
   - Increase RR ratio (Mode A)
   - Use Mode C for adaptive sizing

3. Review individual trades
   - Are stops too tight? (Mode A: increase buffer)
   - Are targets too ambitious? (Mode A: lower RR)
   - Is slippage accounted for?

### Problem: Large Drawdowns

**Actions**:
1. Reduce position size immediately
2. Tighten time window (fewer trades)
3. Increase trend filter strength (longer EMA)
4. Switch to Mode A with conservative RR (1.5)
5. Add minimum FVG size filter

---

## Performance Benchmarks

### Good Performance Indicators
```
Win Rate: 45-60%
Profit Factor: >1.5
Max Drawdown: <15% of capital
Sharpe Ratio: >1.0 (if available)
Average Win/Loss Ratio: >1.5
```

### Warning Signs
```
Win Rate: <40% (too many losers)
Profit Factor: <1.2 (barely profitable)
Max Drawdown: >25% (too risky)
Consecutive Losses: >10 (review strategy)
```

---

## Advanced Usage: Custom Modifications

### Adding Volume Filter
You can add volume confirmation:
```pinescript
avgVolume = ta.sma(volume, 20)
highVolume = volume > avgVolume * 1.5

// Add to conditions:
longCondition = longSignal and isBullishTrend and isInTimeWindow() and highVolume
```

### Adding Volatility Filter
Avoid trading in low volatility:
```pinescript
minATR = 10 // Adjust for NQ
isVolatileEnough = atrValue > minATR

// Add to conditions:
longCondition = longSignal and isBullishTrend and isInTimeWindow() and isVolatileEnough
```

### Multiple Timeframes
Test same strategy on different timeframes:
- 1 minute (scalping)
- 15 minutes (day trading)
- 1 hour (swing trading)

Adjust parameters accordingly!

---

## Conclusion

Start with Example 1 (Basic Setup) and run a backtest. Based on the results, choose the appropriate example that matches your:
- Risk tolerance
- Trading style
- Market conditions
- Time availability

Remember: **Past performance does not guarantee future results!**

Always paper trade new configurations before risking real capital.

Good luck! 📊

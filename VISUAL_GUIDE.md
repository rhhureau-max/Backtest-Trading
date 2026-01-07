# NQ IVFG Strategy - Visual Guide

## Table of Contents
1. [Fair Value Gap (FVG) Explained](#fair-value-gap-fvg-explained)
2. [IVFG (Inverted FVG) Logic](#ivfg-inverted-fvg-logic)
3. [Multi-Timeframe Filter](#multi-timeframe-filter)
4. [Complete Entry Logic Flow](#complete-entry-logic-flow)
5. [Risk Management Modes](#risk-management-modes)

---

## Fair Value Gap (FVG) Explained

### Bullish FVG Formation

```
Time:     [2]      [1]      [0]     Current
          
Price     
          
  │                          ┌────┐
  │                          │    │ [0] Current candle
  │                          │    │     low[0] = 15,000
  │                          └────┘
  │       
  │        ╔════════════════════╗
  │        ║   BULLISH FVG      ║  <-- Gap between high[2] and low[0]
  │        ║   (Imbalance)      ║      This is the "unfilled" area
  │        ╚════════════════════╝
  │       
  │        ┌────┐
  │        │    │ [2] Two candles ago
  │        │    │     high[2] = 14,980
  │        └────┘
  │
  └────────────────────────────────> Time

Condition: low[0] > high[2]
Gap Size: low[0] - high[2] = 15,000 - 14,980 = 20 points
```

### Bearish FVG Formation

```
Time:     [2]      [1]      [0]     Current
          
Price     
          
  │        ┌────┐
  │        │    │ [2] Two candles ago
  │        │    │     low[2] = 15,020
  │        └────┘
  │       
  │        ╔════════════════════╗
  │        ║   BEARISH FVG      ║  <-- Gap between high[0] and low[2]
  │        ║   (Imbalance)      ║      Price moved down too fast
  │        ╚════════════════════╝
  │       
  │                          ┌────┐
  │                          │    │ [0] Current candle
  │                          │    │     high[0] = 15,000
  │                          └────┘
  │
  └────────────────────────────────> Time

Condition: high[0] < low[2]
Gap Size: low[2] - high[0] = 15,020 - 15,000 = 20 points
```

---

## IVFG (Inverted FVG) Logic

### Long Signal (IVFG on Bearish FVG)

```
Step 1: Bearish FVG Detected
         ┌────┐
         │ [2]│  low[2] = 15,020
         └────┘
          ╔════════════╗
          ║ BEARISH FVG ║  Top = 15,020, Bottom = 15,000
          ╚════════════╝
                   ┌────┐
                   │ [0]│  high[0] = 15,000
                   └────┘

Step 2: Price Returns (within 12 bars)
                          
         15,025 ─ ─ ─ ─ ─ ─ ─ ┐ Bearish FVG TOP
                               │
                          ┌────┤ <-- CLOSE ABOVE FVG TOP
                          │ XX ├─ Close = 15,026
                          └────┤
                               │
         15,000 ─ ─ ─ ─ ─ ─ ─ ┘ Bearish FVG BOTTOM
                          
         ★ LONG SIGNAL TRIGGERED ★
         
Why? Price "inverted" the bearish imbalance by closing above it.
This suggests buyers are now in control.
```

### Short Signal (IVFG on Bullish FVG)

```
Step 1: Bullish FVG Detected
                   ┌────┐
                   │ [0]│  low[0] = 15,020
                   └────┘
          ╔════════════╗
          ║ BULLISH FVG ║  Top = 15,020, Bottom = 15,000
          ╚════════════╝
         ┌────┐
         │ [2]│  high[2] = 15,000
         └────┘

Step 2: Price Returns (within 12 bars)
                          
         15,020 ─ ─ ─ ─ ─ ─ ─ ┐ Bullish FVG TOP
                               │
         14,995 ─ ─ ─ ─ ─ ─ ─ ┘ Bullish FVG BOTTOM
                          
                          ┌────┤
                          │ XX ├─ Close = 14,994
                          └────┤ <-- CLOSE BELOW FVG BOTTOM
                          
         ★ SHORT SIGNAL TRIGGERED ★
         
Why? Price "inverted" the bullish imbalance by closing below it.
This suggests sellers are now in control.
```

---

## Multi-Timeframe Filter

### 4H EMA 20 Trend Filter

```
4H Chart View:
                                    Current 4H EMA20 = 15,100
Price                                            ↓
                                            ═════════════
  │     ┌───┐     ┌───┐                   ║ EMA 20 (4H) ║
  │     │   │ ┌───┤   ├───┐               ═════════════
  │ ┌───┤   │ │   └───┘   │ ┌───┐
  │ │   └───┘ │            ├─┤   │
  │ │         └────────────┘ └───┘
  │─┴──────────────────────────────────> Time (4H bars)

5M Chart View (Current):
                     
  15,150 ├─┐                    ↑ BULLISH ZONE
         │ │  ┌─┐               │ (Close > EMA)
  15,100 ═════════════════════  ← 4H EMA20 plotted on 5m chart
         └─┘  │ │               │
              └─┘               ↓ BEARISH ZONE
  15,050 ├─────────             (Close < EMA)

  └──────────────────────────> Time (5m bars)

Current Close = 15,120
Status: BULLISH (15,120 > 15,100)
→ Only LONG trades allowed
```

---

## Complete Entry Logic Flow

### Long Entry Decision Tree

```
                         ┌─────────────────┐
                         │  New 5m Candle  │
                         │     Closes      │
                         └────────┬────────┘
                                  │
                    ┌─────────────▼────────────┐
                    │  Is Time 01:00-05:00?    │
                    └──┬────────────────────┬──┘
                      NO                  YES
                       │                    │
                       ▼                    ▼
                  ┌─────────┐      ┌──────────────┐
                  │  SKIP   │      │ Check Trend  │
                  │  (Wait) │      │ Filter (4H)  │
                  └─────────┘      └──────┬───────┘
                                          │
                            ┌─────────────▼───────────────┐
                            │ Close > EMA20(4H)?          │
                            └──┬──────────────────────┬───┘
                              NO                    YES
                               │                      │
                               ▼                      ▼
                          ┌─────────┐      ┌──────────────────┐
                          │  SKIP   │      │ Check for        │
                          │ (Wrong  │      │ Bearish FVG in   │
                          │  Trend) │      │ last 12 bars     │
                          └─────────┘      └────────┬─────────┘
                                                     │
                                 ┌───────────────────▼──────────────────┐
                                 │ Did Close cross above Bearish FVG     │
                                 │ top (that was detected in last 12)?   │
                                 └──┬────────────────────────────────┬───┘
                                   NO                              YES
                                    │                                │
                                    ▼                                ▼
                               ┌─────────┐                  ┌──────────────┐
                               │  SKIP   │                  │  ★ ENTER ★   │
                               │ (No FVG │                  │   LONG       │
                               │ Trigger)│                  │  POSITION    │
                               └─────────┘                  └──────────────┘
```

### Short Entry Decision Tree

```
(Similar flow but:)
- Trend: Close < EMA20(4H)
- FVG Type: Look for Bullish FVG
- Trigger: Close crosses BELOW Bullish FVG bottom
- Result: ★ ENTER SHORT POSITION ★
```

---

## Risk Management Modes

### Mode A - Structural

```
Long Entry Example:

Entry Price = 15,000
Signal Candle Low = 14,990
Safety Buffer = 5 ticks
Risk/Reward = 2.0

                    ╔══════════════════╗
         15,040 ──  ║  TAKE PROFIT     ║  ← TP: Entry + (Risk × RR)
                    ║  (+40 points)    ║     = 15,000 + (10 × 2.0)
                    ╚══════════════════╝     = 15,040
                           ▲
                           │
                    ┌──────┴──────┐
         15,000 ──  │ ENTRY PRICE  │
                    └─────────────┘
                           │
                           ▼
                    ╔══════════════════╗
         14,985 ──  ║  STOP LOSS       ║  ← SL: Low - Buffer
                    ║  (-15 points)    ║     = 14,990 - 5 ticks
                    ╚══════════════════╝     = 14,985
                    
Risk = 15,000 - 14,985 = 15 points
Reward = 15,040 - 15,000 = 40 points
R:R Ratio = 40/15 ≈ 2.67 (due to rounding)
```

### Mode B - Fixed Points

```
Long Entry Example:

Entry Price = 15,000
Fixed SL = 20 points
Fixed TP = 40 points

                    ╔══════════════════╗
         15,040 ──  ║  TAKE PROFIT     ║  ← TP: Entry + Fixed TP
                    ║  (+40 points)    ║     = 15,000 + 40
                    ╚══════════════════╝     = 15,040
                           ▲
                           │
                    ┌──────┴──────┐
         15,000 ──  │ ENTRY PRICE  │
                    └─────────────┘
                           │
                           ▼
                    ╔══════════════════╗
         14,980 ──  ║  STOP LOSS       ║  ← SL: Entry - Fixed SL
                    ║  (-20 points)    ║     = 15,000 - 20
                    ╚══════════════════╝     = 14,980

R:R Ratio = 40/20 = 2.0 (Always fixed)
```

### Mode C - ATR Based

```
Long Entry Example:

Entry Price = 15,000
ATR(14) = 12 points
ATR SL Multiplier = 1.5
ATR TP Multiplier = 3.0

                    ╔══════════════════╗
         15,036 ──  ║  TAKE PROFIT     ║  ← TP: Entry + (ATR × TP Mult)
                    ║  (+36 points)    ║     = 15,000 + (12 × 3.0)
                    ╚══════════════════╝     = 15,036
                           ▲
                           │
                    ┌──────┴──────┐
         15,000 ──  │ ENTRY PRICE  │
                    └─────────────┘
                           │
                           ▼
                    ╔══════════════════╗
         14,982 ──  ║  STOP LOSS       ║  ← SL: Entry - (ATR × SL Mult)
                    ║  (-18 points)    ║     = 15,000 - (12 × 1.5)
                    ╚══════════════════╝     = 14,982

R:R Ratio = 36/18 = 2.0
Note: Adapts to volatility! Higher ATR = Wider stops
```

---

## Strategy Timeline Visualization

### Complete Trade Example (Long)

```
Time:  00:30   01:00   01:15   01:30   01:45   02:00   02:15   02:30
       │       │       │       │       │       │       │       │
Phase: │ Wait  │ ← ─ ─ Trading Window Active ─ ─ ─ ─ ─ ─ →    │
       │       │       │       │       │       │       │       │
Event: │       │   Bearish   │   Price  LONG   │       TP      │
       │       │   FVG       │   closes Entry  │       HIT     │
       │       │   Detected  │   above         │       ★       │
       │       │             │   FVG top       │               │
       │       │             │                 │               │
Price  │       │             │                 │               │
       │       │             │                 │               │
15,050 │       │             │        ╔════════╧═══════╗       │
       │       │             │        ║  TP: 15,040    ║ ←─────┤ EXIT
       │       │             │        ╚════════════════╝       │ +$40
15,000 │       │      ┌──────┼────────┬────────┐              │
       │       │      │ FVG  │        │ ENTRY  │              │
       │       │      └──────┼────────┴────────┘              │
14,950 │       │             │                                │
       │       ├─────┐       │        ╔════════════════╗      │
       │       │ [2] │       │        ║  SL: 14,985    ║      │
       │       └─────┘       │        ╚════════════════╝      │
       │       │             │                                │
       └───────┴─────────────┴────────────────────────────────┘

Trade Summary:
- FVG Detected: 01:00
- Entry Time: 01:30
- Entry Price: 15,000
- Stop Loss: 14,985
- Take Profit: 15,040
- Exit Time: 02:30
- Exit Price: 15,040
- Profit: +40 points
- Risk/Reward: 2.67:1
```

---

## FVG Memory System

### 12-Bar Lookback Window

```
Bar Index:  ...  980  985  990  995  1000  (Current Bar)
                 │    │    │    │    │
                 │    │    │    │    └─ Now
                 │    │    │    └────── 5 bars ago
                 │    │    └─────────── 10 bars ago  
                 │    └──────────────── 15 bars ago (TOO OLD)
                 └───────────────────── 20 bars ago (TOO OLD)

FVG A detected at bar 980: ❌ DELETED (>12 bars ago)
FVG B detected at bar 990: ✅ ACTIVE (10 bars ago)
FVG C detected at bar 995: ✅ ACTIVE (5 bars ago)
FVG D detected at bar 1000: ✅ ACTIVE (just detected)

Active FVG Array:
┌────────────────────────────────┐
│ Index │  Top   │ Bottom │ Bar  │
├───────┼────────┼────────┼──────┤
│   0   │ 15,020 │ 15,000 │ 990  │ ← FVG B
│   1   │ 15,045 │ 15,030 │ 995  │ ← FVG C
│   2   │ 15,070 │ 15,055 │ 1000 │ ← FVG D
└────────────────────────────────┘

The strategy checks if current close triggers any of these 3 FVGs!
```

---

## Performance Table Visualization

```
┌──────────────────────────────────────┐
│        PERFORMANCE METRICS           │
├─────────────────┬────────────────────┤
│ Metric          │ Value              │
├─────────────────┼────────────────────┤
│ Total Trades    │ 127                │
├─────────────────┼────────────────────┤
│ Win Rate        │ 52.76% (GREEN)     │ ← >50% = Green
├─────────────────┼────────────────────┤
│ Profit Factor   │ 1.68 (GREEN)       │ ← >1.0 = Green
├─────────────────┼────────────────────┤
│ Max Drawdown    │ -$8,450 (RED)      │ ← Always Red
├─────────────────┼────────────────────┤
│ Net Profit      │ +$12,340 (GREEN)   │ ← Positive = Green
├─────────────────┼────────────────────┤
│ Risk Mode       │ Mode A (YELLOW)    │
└─────────────────┴────────────────────┘
       ↑
       Appears on bottom-right of chart
```

---

## Common Patterns

### Pattern 1: Successful IVFG Long

```
Before:                  After:
                        
  │  ┌──┐                │      ┌──┐  ← Price reversed up
  │  │  │                │  ┌───┤★ │  ← Closed above FVG
  │  └──┤                │  │   └──┘
  │  ╔══╧══╗             │  │  ╔════╗
  │  ║ FVG ║             │  │  ║FVG ║
  │  ╚═════╝             │  │  ╚════╝
  │     ┌──┐             │  │     ┌──┐
  │     │  │             │  └─────┤  │
  │     └──┘             │        └──┘

This is what we want to see!
```

### Pattern 2: Failed IVFG (Price Continues)

```
Before:                  After:
                        
  │  ┌──┐                │  ┌──┐
  │  │  │                │  │  │
  │  └──┤                │  └──┤
  │  ╔══╧══╗             │  ╔══╧══╗
  │  ║ FVG ║             │  ║ FVG ║
  │  ╚═════╝             │  ╚═════╝
  │     ┌──┐             │     ┌──┐
  │     │  │             │     │  │    ← Didn't close above
  │     └──┘             │     │  │    ← No signal triggered
                         │     └──┘
                         │        ┌──┐
                         │        │  │
                         │        └──┘

No signal = No trade!
```

---

## Session Comparison

### London Killzone (01:00-05:00)

```
Volume: ████████████████ 80%
Volatility: ████████████████ 85%
Trend: ████████████████ Strong
Quality: ████████████████ 85%

Best for: IVFG strategy ★★★★★
```

### New York Open (13:30-17:00)

```
Volume: ████████████████████ 100%
Volatility: ████████████████████ 95%
Trend: ████████████ Variable
Quality: ██████████████ 70%

Best for: IVFG strategy ★★★★☆
```

### Asian Session (23:00-03:00)

```
Volume: ████████ 40%
Volatility: ████████ 45%
Trend: ██████ Ranging
Quality: ████████ 40%

Best for: IVFG strategy ★★☆☆☆
```

---

## Quick Visual Decision Guide

```
START
  │
  ▼
Is it 01:00-05:00? ──NO──> WAIT
  │YES
  ▼
Is Close > EMA20(4h)? ──NO──> Check for SHORT setup
  │YES                          │
  ▼                             ▼
Look for Bearish FVG       Look for Bullish FVG
  │                             │
  ▼                             ▼
Found in last 12 bars? ──NO──> WAIT
  │YES                          │YES
  ▼                             ▼
Close above FVG top?       Close below FVG bottom?
  │YES                          │YES
  ▼                             ▼
ENTER LONG                  ENTER SHORT
  │                             │
  ▼                             ▼
Set SL & TP based          Set SL & TP based
on Risk Mode               on Risk Mode
  │                             │
  └─────────────┬───────────────┘
                │
                ▼
           MANAGE TRADE
```

---

## Legend

```
Symbols Used in This Guide:
═══  Double lines = Important levels (SL/TP)
───  Single lines = Price movement
╔═╗  Box = Zone or area
┌─┐  Simple box = Candle
★    Star = Signal or important point
▲▼   Arrows = Direction
→←   Arrows = Flow or movement
✅   Check = Active/Valid
❌   X = Inactive/Invalid
```

---

This visual guide should help you understand how the strategy works at a glance!

For more details, see:
- **STRATEGY_DOCUMENTATION.md** - Complete documentation
- **QUICK_REFERENCE.md** - Parameter reference
- **USAGE_EXAMPLES.md** - Configuration examples

Happy Trading! 📊📈

# Last 10 Trades Analysis - PBTrading Silver Bullet & IFVG

**Strategy:** Silver Bullet + IFVG  
**RR Target:** 2.0  
**Data:** NQ Futures 2025  

---

## Trade Details

| # | Direction | Entry Time | Entry Price | Exit Price | P&L | Result |
|---|-----------|------------|-------------|------------|-----|--------|
| 755 | LONG | 2025-11-07 09:48 | $25,446.00 | $25,440.50 | -$45.52 | LOSS |
| 756 | SHORT | 2025-11-07 09:57 | $25,423.00 | $25,436.75 | -$28.84 | LOSS |
| 757 | LONG | 2025-11-10 09:01 | $25,569.25 | $25,552.50 | -$66.77 | LOSS |
| 758 | LONG | 2025-11-10 09:06 | $25,529.00 | $25,531.00 | -$58.30 | LOSS |
| 759 | LONG | 2025-11-10 09:56 | $25,539.75 | $25,541.00 | -$26.90 | LOSS |
| 760 | LONG | 2025-11-10 09:58 | $25,537.25 | $25,523.75 | -$71.14 | LOSS |
| 761 | LONG | 2025-11-11 09:01 | $25,613.75 | $25,548.25 | -$227.20 | LOSS |
| 762 | SHORT | 2025-11-11 09:09 | $25,580.50 | $25,586.75 | -$49.45 | LOSS |
| 763 | LONG | 2025-11-12 09:06 | $25,605.50 | $25,600.50 | -$45.72 | LOSS |
| 764 | SHORT | 2025-11-12 09:17 | $25,602.25 | $25,584.50 | +$22.54 | WIN |

---

## Trade Logic Explanation

### LONG Entry Conditions

1. **SELL-SIDE LIQUIDITY SWEEP detected**
   - Price wicks BELOW 20-bar fractal low
   - Then closes ABOVE the fractal low

2. **Previous BEARISH FVG gets VIOLATED**
   - Price closes ABOVE the FVG top boundary

3. **Creates BULLISH IFVG (Inversion FVG)**
   - Zone becomes support instead of resistance

4. **ENTRY triggered on RETEST of IFVG zone**
   - Limit order at the IFVG zone

### SHORT Entry Conditions

1. **BUY-SIDE LIQUIDITY SWEEP detected**
   - Price wicks ABOVE 20-bar fractal high
   - Then closes BELOW the fractal high

2. **Previous BULLISH FVG gets VIOLATED**
   - Price closes BELOW the FVG bottom boundary

3. **Creates BEARISH IFVG (Inversion FVG)**
   - Zone becomes resistance instead of support

4. **ENTRY triggered on RETEST of IFVG zone**
   - Limit order at the IFVG zone

---

## Risk Management

- **Stop Loss:** At swing low (longs) / swing high (shorts)
- **Take Profit:** 2R (2x the initial risk)
- **Break-Even:** Move SL to entry when 1R profit reached

## Trading Window

- **Silver Bullet Session:** 9:00 - 10:00 Chicago Time
- **Entries ONLY** during this 1-hour window
- **Forced exit:** All positions closed at 15:00 CT

---

## Example Trade Breakdown

### Trade #764 (WIN - SHORT)

**Entry:** 2025-11-12 09:17 @ $25,602.25

**Logic:**
1. Price swept BUY-SIDE LIQUIDITY (wicked above 20-bar fractal high)
2. A previous BULLISH FVG was violated (price closed below bottom)
3. This created a BEARISH IFVG (zone inverted from support to resistance)
4. Short entry triggered on retest of the IFVG zone

**Exit:** 2025-11-12 09:41 @ $25,584.50

**Result:** Take Profit hit at 2R target (+$22.54)

---

*Generated on 2025-11-30 | Data: NQ Futures 2025*

# ICT 2022 Model - London Continuation Strategy Backtest

## Overview

This implementation provides a complete backtesting system for the **ICT 2022 Model** applied to London continuation trading on NQ 5-minute data (2018-2025).

## Strategy Logic

### Phase 1: Initial State
1. **Tokyo Session** (19:00 - 23:00, previous day N-1):
   - Identify Tokyo_High (highest high in this period)
   - Identify Tokyo_Low (lowest low in this period)
   - Calculate Tokyo_EQ = (Tokyo_High + Tokyo_Low) / 2

2. **Midnight Open** (00:00, day N):
   - Record the open price at midnight

### Phase 2: Event 1 - Liquidity Sweep
- **Time window**: 01:00 - 04:00 (London Killzone)
- **Condition**: Price must go BELOW Tokyo_Low
- **Filter**: The sweep must occur when price is below Midnight_Open (discount zone)
- **Track**: Record the lowest point of the sweep (Sweep_Low)

### Phase 3: Event 2 - Market Structure Shift (MSS)

**Method 1** (Primary - Simplified): 
- After sweep low is created, look at the 3 M5 candles immediately BEFORE the sweep low
- Find the highest high among these 3 candles (Call it "Pre-Sweep High")
- MSS is confirmed when price CLOSES above this Pre-Sweep High

**Method 2** (Alternative - EMA based):
- Calculate EMA 20 on M5 data
- After sweep, MSS is confirmed when:
  - Price closes above EMA 20
  - AND the candle body size > average body size of last 20 candles (showing strength)

### Phase 4: Event 3 - FVG & Entry

**FVG (Fair Value Gap) Detection:**
- A bullish FVG occurs when: Candle[i].Low > Candle[i-2].High
- This creates a gap between candle i-2's high and candle i's low
- Entry placed at FVG_Top (highest level of the FVG)

### Phase 5: Exit Strategy

**Stop Loss:**
- Placed below Sweep_Low (the lowest point reached during the liquidity sweep)

**Take Profits:**
- **TP1**: Tokyo_EQ OR Midnight_Open (whichever is closer but still above entry)
- **TP2**: Tokyo_High (the main target - THIS IS THE KEY METRIC)
- **TP3**: Tokyo_High + 10 points (expansion target)

## Results Summary

### Data Analysis
- **Total Candles Processed**: 554,518 candles
- **Date Range**: January 1, 2018 - November 11, 2025
- **Valid Setups Found**: 958 setups

### Entry Method 1: MSS (Internal Structure) + FVG Entry

```
Total Setups: 958
Entries Filled: 566 (59.1%)
Trades: 566

Win Rate Overall: 65.2%
Win Rate to TP1 (Tokyo_EQ): 73.5%
Win Rate to TP2 (Tokyo_High): 9.2% ← KEY METRIC
Win Rate to TP3 (Tokyo_High + 10): 4.2%

Average RR: 0.59:1
Net Points: +2650.68
Profit Factor: 1.51
Max Consecutive Losses: 4
Average Trade Duration: 58.8 minutes
```

### Entry Method 2: Full Range Breakout Entry

```
Total Setups: 958
Entries Filled: 595 (62.1%)
Trades: 595

Win Rate Overall: 84.5%
Win Rate to TP1: 84.5%
Win Rate to TP2: 30.8%
Win Rate to TP3: 13.6%

Average RR: 0.21:1
Net Points: +1825.67
Profit Factor: 1.31
Max Consecutive Losses: 3
Average Trade Duration: 53.6 minutes
```

### Comparison Analysis

**Key Finding**: Full Range Breakout Entry is MORE effective than MSS Entry for reaching Tokyo_High

- **Difference in Win Rate to Tokyo_High**: -21.6% (MSS underperforms)
- **Difference in Net Points**: +825.00 points (MSS generates more net points despite lower win rate to Tokyo_High)

## Key Insights

1. **Setup Frequency**: The strategy identified 958 valid setups over 7+ years, averaging approximately 135 setups per year or about 11 setups per month.

2. **Entry Fill Rate**: 
   - MSS Method: 59.1% of setups resulted in filled entries
   - Breakout Method: 62.1% of setups resulted in filled entries

3. **Win Rate Paradox**: 
   - The MSS method has a lower overall win rate (65.2% vs 84.5%)
   - BUT generates more net points (+2650.68 vs +1825.67)
   - This suggests MSS entries capture larger moves when they work

4. **Target Achievement**:
   - Only 9.2% of MSS entries reach Tokyo_High (the full range target)
   - Breakout entries reach Tokyo_High 30.8% of the time
   - This confirms that entering INSIDE the range after MSS is less likely to reach the top of the range compared to waiting for a full breakout

5. **Risk Management**:
   - MSS method has slightly worse drawdown characteristics (4 consecutive losses vs 3)
   - But maintains better profit factor (1.51 vs 1.31)

## Hypothesis Testing Result

**Original Hypothesis**: "After sweeping the low of the Tokyo range and breaking the internal structure (MSS), price has a high probability of reaching the top of the Tokyo range."

**Result**: **REJECTED**

The data shows that only 9.2% of trades using the MSS method reach Tokyo_High, which does not constitute a "high probability." In contrast, the Full Range Breakout method achieves Tokyo_High 30.8% of the time, demonstrating that waiting for price to break outside the range before entering is significantly more effective for reaching the range high.

## Trade-offs

The MSS method offers:
- ✅ Better entry prices (lower risk entries inside the range)
- ✅ Higher net profit in points
- ✅ Better profit factor
- ❌ Lower probability of reaching full range target
- ❌ More consecutive losses

The Breakout method offers:
- ✅ Higher win rate to Tokyo_High (30.8% vs 9.2%)
- ✅ More consistent wins (84.5% overall win rate)
- ✅ Fewer consecutive losses
- ❌ Later entries (after breakout)
- ❌ Lower net profit despite higher win rate

## Usage

Run the backtest:

```bash
python3 ict_2022_london_continuation.py
```

This will:
1. Load all 5-minute NQ data files (2018-2025)
2. Process each trading day for valid setups
3. Simulate both entry methods
4. Generate comprehensive statistics
5. Save results to `ICT_2022_RESULTS.txt`

## Files

- `ict_2022_london_continuation.py` - Main backtesting script
- `ICT_2022_RESULTS.txt` - Detailed results output
- `ICT_2022_README.md` - This documentation file

## Dependencies

```bash
pip3 install pandas numpy
```

## Data Format

The script expects semicolon-delimited CSV files with the following format:

```
Column1;Column2;Column3;Column4;Column5;Column6;Column7
01/01/2018;17:00:00;7503.739664;7511.940473;7499.63926;7511.3547;1451
```

Columns: Date;Time;Open;High;Low;Close;Volume
- Date format: DD/MM/YYYY
- Time format: HH:MM:SS
- Timezone: Chicago time (America/Chicago)

## Conclusion

This backtest provides empirical evidence that while the ICT 2022 Model MSS entry method is profitable, it does not achieve a high probability of reaching Tokyo_High. Traders using this approach should consider:

1. Taking profits earlier (TP1 at 73.5% hit rate is more reliable)
2. Using the Full Range Breakout method if the goal is specifically to reach Tokyo_High
3. Combining both methods: Use MSS for quick scalps to TP1, and Breakout method for range expansion plays

The strategy is viable and profitable with proper risk management, but expectations should be calibrated based on these empirical results rather than the hypothesis alone.

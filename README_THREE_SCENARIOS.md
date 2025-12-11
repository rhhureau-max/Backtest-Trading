# London Killzone Three Scenarios Backtest

## Overview

This script implements a comprehensive backtest of three distinct FVG (Fair Value Gap) trading scenarios during the London Killzone (01:00-04:00 Chicago Time) for NQ futures data from 2018-2025.

## Script Information

**File:** `london_killzone_three_scenarios_backtest.py`

**Purpose:** Compare three different FVG-based trading approaches to identify which scenario provides the best risk-adjusted returns.

## Three Scenario Definitions

### Scenario 1: Liquidity Sweep + FVG (Turtle Soup)

A reversal pattern that captures "fake breakouts" followed by immediate displacement.

**Criteria for SHORT setup:**
- Price must wick ABOVE the highest high of the last 12 candles (60 minutes)
- Current candle must CLOSE BELOW that high (rejection/false breakout)
- Immediately after this sweep, a candle creates a BEARISH FVG

**Criteria for LONG setup:**
- Price must wick BELOW the lowest low of the last 12 candles (60 minutes)
- Current candle must CLOSE ABOVE that low (rejection/false breakout)
- Immediately after this sweep, a candle creates a BULLISH FVG

**Logic:** This scenario captures liquidity grabs where market makers sweep stops above/below recent ranges, only to reverse direction. The FVG confirms the displacement.

---

### Scenario 2: Inverted FVG (IFVG)

A unique pattern where a FVG gets "flipped" to the opposite direction, creating support/resistance.

**Criteria for LONG setup (Bearish FVG becomes Bullish):**
1. Identify a standard BEARISH FVG
2. A subsequent candle CLOSES ABOVE the high boundary of this bearish FVG
3. The bearish FVG is now "inverted" and becomes a BUY zone (Support)
4. Entry: Place a limit buy order when price returns to test this inverted zone

**Criteria for SHORT setup (Bullish FVG becomes Bearish):**
1. Identify a standard BULLISH FVG
2. A subsequent candle CLOSES BELOW the low boundary of this bullish FVG
3. The bullish FVG is now "inverted" and becomes a SELL zone (Resistance)
4. Entry: Place a limit sell order when price returns to test this inverted zone

**Logic:** Once a FVG is broken in the opposite direction, it transforms from a gap that needs filling into a support/resistance zone. This represents a market structure shift.

---

### Scenario 3: Continuation FVG (Control Group)

Standard FVG following the prevailing trend without liquidity sweep or inversion.

**Criteria:**
- Standard BULLISH or BEARISH FVG forms during Killzone hours
- Does NOT match Scenario 1 (no liquidity sweep immediately before)
- Is NOT an Inversion (Scenario 2)
- Regular FVG that follows the current trend direction

**Logic:** This serves as a baseline/control group to compare against the more complex patterns. It represents simple trend continuation.

---

## Standard FVG Definition

**Bullish FVG:**
- Condition: High(n-1) < Low(n+1)
- Gap Zone: [High(n-1), Low(n+1)]
- Direction: Upward displacement with unfilled gap

**Bearish FVG:**
- Condition: Low(n-1) > High(n+1)
- Gap Zone: [Low(n-1), High(n+1)]
- Direction: Downward displacement with unfilled gap

Where:
- n-1 = First candle
- n = Middle candle (displacement candle)
- n+1 = Third candle

---

## Trade Execution Rules

### Entry
- Trade is entered when price returns to "mitigate" (touch) the FVG zone
- Entry price: Midpoint of the FVG zone
- Maximum mitigation window: 60 candles (5 hours) after setup formation

### Stop Loss
**Scenario 1 & 3:**
- LONG: Below the low of the setup candle (candle n-1)
- SHORT: Above the high of the setup candle (candle n-1)

**Scenario 2 (IFVG):**
- LONG: Below the low of the inversion candle (candle that flipped the FVG)
- SHORT: Above the high of the inversion candle

### Take Profit
- Fixed 2:1 Risk/Reward ratio
- TP = Entry Price ± (Risk × 2)

### Exit Conditions
1. **Take Profit Hit:** Exit at TP level
2. **Stop Loss Hit:** Exit at SL level
3. **Session Close:** Exit at 16:00 Chicago time at market price (if trade still open)
4. **End of Data:** Exit at last available price

---

## Time Zone and Hours

- **Time Zone:** Chicago Time (CST/CDT)
- **Killzone Hours:** 01:00 to 04:00 Chicago time
- **Setup Detection:** Only during Killzone hours
- **Session Close:** 16:00 Chicago time (forced exit)

---

## Data Requirements

**Files:** `YEAR 5m.csv` (2018-2025)

**Format:** Semicolon-separated CSV with columns:
- Column1: Date (DD/MM/YYYY)
- Column2: Time (HH:MM:SS)
- Column3: Open
- Column4: High
- Column5: Low
- Column6: Close
- Column7: Volume

**Time Zone Handling:**
- Input data assumed to be UTC
- Automatically converted to Chicago time (CST/CDT)
- Handles daylight saving time transitions

---

## Output Files

The script generates three CSV files:

### 1. `three_scenarios_comparison.csv`
Summary comparison table with:
- Scenario name
- Total trades executed
- Win rate (%)
- Profit factor
- Average PnL (points)
- Total PnL
- Max consecutive wins
- Max consecutive losses

### 2. `three_scenarios_detailed_trades.csv`
Complete trade log with every trade including:
- Scenario and trade type (LONG/SHORT)
- Entry/exit datetime and prices
- Stop loss and take profit levels
- Risk amount
- PnL and PnL points
- Exit result (Take Profit/Stop Loss/Session Close)
- Year-Month for analysis

### 3. `three_scenarios_monthly_breakdown.csv`
Monthly performance breakdown by scenario:
- Scenario name
- Year-Month
- Number of trades
- Win rate (%)
- Total PnL for the month

---

## Running the Script

### Prerequisites

Install required packages:
```bash
pip install pandas numpy pytz
```

### Execution

```bash
python london_killzone_three_scenarios_backtest.py
```

### Expected Runtime
- Processing ~550,000 candles
- Detecting ~87,000 potential setups
- Executing ~800 trades
- Runtime: 10-15 minutes (depending on system)

---

## Performance Metrics

The script calculates the following metrics for each scenario:

**Win Rate:** Percentage of profitable trades

**Profit Factor:** Gross profit / Gross loss (higher is better)

**Average PnL:** Mean profit/loss per trade in points

**Total PnL:** Cumulative profit/loss across all trades

**Consecutive Wins/Losses:** Maximum streak of winning/losing trades (risk management insight)

---

## Key Implementation Features

### 1. Efficient FVG Detection
- Vectorized operations where possible
- Progressive filtering (Scenario 1 & 2 first, then Scenario 3)
- Duplicate prevention across scenarios

### 2. Accurate Time Zone Handling
- Proper UTC to Chicago time conversion
- Automatic DST handling via pytz
- Session-based trade management

### 3. Realistic Trade Simulation
- Intra-candle stop loss checking (conservative approach)
- Take profit checking on high/low of candles
- Forced session close at 16:00
- No look-ahead bias

### 4. Comprehensive Statistics
- Trade-by-trade logging
- Monthly/yearly breakdown
- Risk metrics (consecutive losses)
- Profit factor analysis

---

## Interpretation of Results

### High Win Rate (>70%)
Indicates the scenario reliably identifies profitable setups. Consider:
- Is the profit factor still good?
- Are consecutive losses manageable?

### High Profit Factor (>2.0)
Shows that winning trades significantly outweigh losers. This is ideal for:
- Compensating for trading costs
- Building confidence in the strategy
- Managing drawdowns

### Low Average PnL with High Win Rate
May indicate:
- Strategy captures small consistent wins
- Position sizing could be optimized
- Transaction costs may impact profitability

### High Consecutive Losses
Indicates:
- Potential for extended drawdown periods
- Need for robust risk management
- Psychological challenge for traders

---

## Differences from Previous Script

This script (`london_killzone_three_scenarios_backtest.py`) differs from the existing `london_killzone_fvg_scenario_analysis.py` in several key ways:

1. **Different Scenario Definitions:**
   - New Scenario 1: Liquidity Sweep + FVG (vs. previous Liquidity Sweep Reversal)
   - New Scenario 2: Inverted FVG (completely new concept)
   - New Scenario 3: Continuation FVG (vs. Simple Continuation)

2. **Inverted FVG Concept:**
   - IFVG is unique to this implementation
   - FVGs that get "flipped" to opposite direction
   - Creates support/resistance zones

3. **Single Risk/Reward:**
   - Fixed 2:1 RR only (previous used both 1:1 and 2:1)
   - Simplifies comparison
   - Focuses on quality over quantity

4. **Session Management:**
   - Forced close at 16:00 if trade still open
   - Previous may have different exit rules
   - Ensures no overnight exposure in backtest

5. **Output Focus:**
   - Emphasizes scenario comparison
   - Monthly breakdown for trend analysis
   - Simpler, more focused metrics

---

## Best Practices for Use

1. **Review Monthly Breakdown:** Identify periods where each scenario performs best
2. **Consider Market Conditions:** Some scenarios may work better in trending vs. ranging markets
3. **Combine Scenarios:** Consider trading multiple scenarios with appropriate position sizing
4. **Backtest Parameters:** Experiment with different lookback periods or RR ratios
5. **Forward Testing:** Always validate historical results with forward testing

---

## Limitations and Considerations

1. **No Transaction Costs:** Backtest doesn't include commissions or slippage
2. **Fixed Position Size:** All trades treated equally (no position sizing optimization)
3. **Historical Data Only:** Past performance doesn't guarantee future results
4. **Execution Assumptions:** Assumes fills at exact levels (may not reflect live trading)
5. **Data Quality:** Results depend on accurate 5-minute OHLC data

---

## Future Enhancements

Potential improvements to consider:

- [ ] Add transaction cost modeling
- [ ] Implement dynamic position sizing
- [ ] Add equity curve visualization
- [ ] Include drawdown analysis
- [ ] Test different RR ratios (1:1, 1.5:1, 3:1)
- [ ] Add parameter optimization
- [ ] Include market regime filtering
- [ ] Generate trade visualization charts
- [ ] Add walk-forward analysis
- [ ] Export results for external analysis tools

---

## Support and Troubleshooting

### Common Issues

**ModuleNotFoundError:**
```bash
pip install pandas numpy pytz
```

**No Data Found:**
- Ensure CSV files are in the same directory as the script
- Check file naming: "YEAR 5m.csv" (e.g., "2020 5m.csv")

**Memory Issues:**
- Script processes large datasets
- Requires ~2GB RAM minimum
- Close other applications if needed

**Slow Performance:**
- Normal for large datasets (8+ years of 5-minute data)
- Progress indicators show processing status
- Consider reducing date range if needed

---

## Credits

**Author:** GitHub Copilot Coding Agent  
**Date:** December 2024  
**Version:** 1.0  
**License:** Use at your own risk. No warranty provided.

---

## Disclaimer

This script is for educational and research purposes only. Trading futures and derivatives carries substantial risk of loss. Past performance is not indicative of future results. Always conduct your own research and consider consulting with a financial advisor before trading.

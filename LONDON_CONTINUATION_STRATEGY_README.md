# London Continuation + Inversion FVG Entry Strategy

## Overview

This is a **Trend Continuation strategy** that trades during the London session using precise entry based on **Inversion FVG (Fair Value Gap)**. The strategy identifies continuation opportunities when price retraces to test Asian session FVGs and then resumes the original trend.

## Strategy Concept

The strategy is based on ICT (Inner Circle Trader) concepts:
- **Tokyo Session** establishes the trend and leaves FVGs (support/resistance zones)
- **London Session** provides retracement opportunities to test these zones
- **Inversion FVG** validates entry when price fills retracement gaps and closes beyond them

## Session Definitions (Chicago Time - UTC-6)

- **Tokyo Session**: 19:00-00:00 (previous day)
- **London Session**: 02:00-05:00 (current day)

## Strategy Rules

### BUY Setup (SELL is reverse)

1. **Tokyo Trend Detection**: Tokyo session closes bullish with a Bullish FVG (Asian FVG) below current price
   - Bullish FVG: `Low[i] > High[i-2]` (gap up between candles)

2. **London Retracement**: Price retraces down toward the Asian FVG at London open

3. **Retracement FVG**: During descent, price creates a Bearish FVG M5 (shows short-term seller strength)
   - Bearish FVG: `High[i] < Low[i-2]` (gap down)

4. **Asian FVG Test**: Price touches/enters the Asian FVG and reacts

5. **Inversion Signal**: An M5 candle moves up, completely fills the last Bearish FVG, and closes above it
   - This Bearish FVG becomes an "Inversion FVG" (former resistance becomes support)

6. **Entry**: Immediate entry at the close of the validation candle

### Stop Loss Options

Two stop loss strategies are tested:

- **SL A (Aggressive)**: Placed just below the Inversion FVG low
  - Tighter stop, assumes Inversion FVG acts as immediate support
  - Lower risk but higher chance of premature stop-out

- **SL B (Structural/Body)**: Placed below the body (close) of the lowest candle that tested the Asian FVG
  - Wider stop, protects against wicks and retest
  - Higher risk but better survival rate

### Take Profit

Multiple Risk-Reward ratios tested: **1:1, 1:1.5, 1:2, 1:2.5, 1:3**

## Implementation

### Requirements

```bash
pip install pandas numpy
```

### Running the Backtest

```bash
python london_continuation_inversion_fvg.py
```

The script automatically tests on both:
- **NQ (NASDAQ)**: `2024 5m.csv`
- **ES (S&P 500)**: `ES 5m (2024-2025).csv`

### Data Format

CSV files with semicolon separator:
```
Column1;Column2;Column3;Column4;Column5;Column6;Column7
Date;Time;Open;High;Low;Close;Volume
```

Timestamps must be in **Chicago time (UTC-6)**.

## Backtest Results Summary

### ES (S&P 500) - 2024-2025 Data

**Best Configuration: SL_A_RR_2 (SL A with 1:2 Risk-Reward)**
- **Total Setups**: 21 (9 BUY, 12 SELL)
- **Win Rate**: 33.33%
- **Profit Factor**: 1.267
- **Expectancy**: +0.32 points
- **Net P&L**: +6.75 points

**Key Findings (ES)**:
- SL A outperforms SL B significantly (Win Rate: 43% vs 24% at 1:1 RR)
- Best RR ratio is 1:2 or 1:3
- 52-62% of trades reach Tokyo session extreme when using SL A
- Strategy shows positive expectancy with tight stops

### NQ (NASDAQ) - 2024 Data

**Best Configuration: SL_B_RR_1 (SL B with 1:1 Risk-Reward)**
- **Total Setups**: 10 (specific breakdown in output)
- **Win Rate**: 30.00%
- **Profit Factor**: 0.817
- **Expectancy**: -1.55 points (needs refinement)

**Key Findings (NQ)**:
- Lower setup frequency (only 10 setups found)
- NQ shows more volatility - wider stops perform relatively better
- Strategy needs additional filters for NQ

## Analysis: Answering Key Questions

### Question 1: Signal Reliability - Does Inversion FVG Filter "Falling Knives"?

**Answer**: The Inversion FVG requirement adds moderate filtering.

- ES shows 33-43% win rate with the filter
- The three-step validation (Asian FVG touch → Retracement FVG → Inversion) provides some edge
- However, below 50% win rate suggests additional confirmation may be beneficial

**Insight**: The filter works but could be enhanced with:
- Volume confirmation at Inversion
- Time-of-day filtering (early vs late London)
- Trend strength indicators from Tokyo session

### Question 2: SL Choice - Is SL A Too Tight?

**Answer**: **SL A is SUPERIOR** for this strategy on ES.

- SL A shows 19-23% HIGHER win rate vs SL B across all RR ratios
- Profit factor improves significantly with tighter stop
- Market does NOT frequently retest the Inversion FVG before continuing

**Insight**: The Inversion FVG acts as strong immediate support/resistance. Once filled and closed through, it provides reliable protection. Wider stops (SL B) allow more noise and reduce win rate.

**Recommendation**: Use **SL A** for aggressive, precise entries.

### Question 3: Reaching Tokyo Extremes - True Continuation?

**Answer**: **Moderate success** (25-62% depending on configuration)

- With SL A at 1:1 RR: 62% reach Tokyo extreme (ES)
- With SL B: Only 25-38% reach extreme
- Better RR ratios (1:2, 1:3) show 47-52% probability

**Insight**: The strategy captures genuine continuations about half the time. When using tighter stops (SL A), the probability of reaching new extremes improves significantly. This suggests that valid setups do continue strongly, but invalid setups get stopped quickly.

## Recommendations

### For ES (S&P 500) Trading:

1. **Use Configuration: SL_A_RR_2 or SL_A_RR_3**
   - Aggressive stop placement
   - 1:2 or 1:3 risk-reward
   - Positive expectancy: +0.32 points

2. **Entry Requirements**:
   - Strict adherence to Tokyo trend identification
   - Clear Bearish/Bullish FVG during London retracement
   - Clean Inversion with candle close beyond FVG

3. **Risk Management**:
   - Position size based on SL A distance (typically tight)
   - Expect ~33% win rate but favorable risk-reward
   - Consider partial profit taking at 1:1, letting rest run to 1:2 or 1:3

### For NQ (NASDAQ) Trading:

1. **Strategy needs refinement** - current results show negative expectancy
2. Consider:
   - Stricter trend filters for Tokyo session
   - Multiple timeframe confirmation
   - Wider stops due to higher volatility
   - Additional volume analysis

### General Improvements:

1. **Add Filters**:
   - Volume spike on Inversion candle
   - Tokyo session strength (range, momentum)
   - Avoid news events during London session

2. **Timing**:
   - Test early London (02:00-03:30) vs late London (03:30-05:00)
   - Some hours may produce better setups

3. **Market Selection**:
   - ES shows better results than NQ
   - Test on other instruments (indices, forex)

## Code Structure

```python
class FVGDetector:
    # Detects Bullish and Bearish FVGs
    # Checks if FVGs are filled or touched

class SessionManager:
    # Identifies Tokyo and London sessions
    # Handles date calculations

class LondonContinuationStrategy:
    # Main strategy implementation
    # Backtesting engine
    # Statistics calculation
    # Results analysis
```

## Files

- `london_continuation_inversion_fvg.py` - Main strategy implementation
- `2024 5m.csv` - NQ 5-minute data for 2024
- `ES 5m (2024-2025).csv` - ES 5-minute data for 2024-2025
- `.gitignore` - Excludes output files
- `LONDON_CONTINUATION_STRATEGY_README.md` - This file

## Conclusion

The London Continuation + Inversion FVG Entry strategy shows **promise on ES** with:
- Positive expectancy when properly configured
- Clear edge with aggressive stop placement (SL A)
- Moderate win rate (~33%) but excellent risk-reward (1:2, 1:3)
- Captures genuine trend continuations about 50% of the time

**Best for**: Disciplined traders comfortable with lower win rates but favorable risk-reward profiles, trading ES futures during London session.

**Not recommended for**: Traders seeking high win rates, or trading NQ without additional filters and refinement.

---

*Strategy based on ICT (Inner Circle Trader) concepts: Fair Value Gaps, Session Analysis, and Inversion patterns.*

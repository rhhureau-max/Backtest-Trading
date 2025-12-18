# London Reversal Strategy - ICT Backtesting System

## Overview

This backtesting system implements the **London Reversal** trading strategy based on Inner Circle Trader (ICT) concepts, specifically the **Accumulation, Manipulation, Distribution (AMD)** model.

## Strategy Logic

### The Four Phases

#### Phase 1: Asian Range (Accumulation)
- **Time Window**: 19:00 to 23:59 (previous day, Chicago time)
- **Purpose**: Identify the accumulation zone during Tokyo session
- **Key Levels**:
  - **Buy-Side Liquidity**: Asian session high (stops above)
  - **Sell-Side Liquidity**: Asian session low (stops below)
- **Minimum Requirements**: Range must be at least 3 points

#### Phase 2: Judas Swing (Manipulation)
- **Time Window**: 02:00 to 03:00 (London open, Chicago time)
- **Purpose**: Liquidity sweep - aggressive move that traps traders
- **Types**:
  - **Buy-Side Sweep**: Price sweeps above Asian high (expecting bearish reversal)
  - **Sell-Side Sweep**: Price sweeps below Asian low (expecting bullish reversal)
- **Key Element**: Creates Fair Value Gap (FVG) in direction of sweep
  - Bullish FVG: Low[i] > High[i-2]
  - Bearish FVG: High[i] < Low[i-2]

#### Phase 3: Reversal Signal (Distribution Beginning)
- **Purpose**: Confirm exhaustion of manipulation move
- **Patterns**:
  - **Hammer**: After downward sweep (bullish reversal)
    - Long lower wick (≥1.5x body size)
    - Small upper wick
    - Minimum 2-point lower wick
  - **Shooting Star**: After upward sweep (bearish reversal)
    - Long upper wick (≥1.5x body size)
    - Small lower wick
    - Minimum 2-point upper wick

#### Phase 4: Inversion FVG Trigger (Entry)
- **Purpose**: Enter when price confirms reversal with displacement
- **Conditions**:
  - Price returns to fill the FVG created during manipulation
  - Strong candle (≥2 points body) closes decisively beyond FVG
  - This "inverts" the FVG into support (bullish) or resistance (bearish)
- **Entry**: At close of the inversion candle

## Trade Management

### Stop Loss Approaches

#### SL A: Structural (Conservative)
- **Long trades**: 1 point below hammer low
- **Short trades**: 1 point above shooting star high
- **Characteristics**:
  - Wider stop
  - Higher win rate expected
  - Lower RR ratios

#### SL B: Inversion (Aggressive)
- **Long trades**: 1 point below bearish FVG bottom
- **Short trades**: 1 point above bullish FVG top
- **Characteristics**:
  - Tighter stop
  - Lower win rate expected
  - Higher RR ratios (potentially 1:3+)
- **Risk**: Vulnerable to "fakeouts" where price briefly violates FVG before continuing

### Take Profit Targets

1. **TP1**: Opposite side of Asian Range
   - Bullish: Asian High
   - Bearish: Asian Low

2. **TP2**: Fibonacci extensions of manipulation range
   - **TP2_1x**: 1.0x extension
   - **TP2_1.5x**: 1.5x extension (primary target)

## HTF Confluence Analysis

The strategy evaluates whether the liquidity sweep occurs near significant Higher Time Frame (HTF) levels:

- **H1 Support/Resistance**: Swing highs/lows from 1-hour chart
- **Tolerance**: Within 15 points of HTF level
- **Impact**: HTF confluence significantly improves win rates

## Key Statistics Tracked

### 1. Inversion FVG Failure Rate Analysis
- Win rate comparison: SL A vs SL B
- Fakeout analysis: How often SL B stops out while SL A wins
- Reliability of FVG inversion as departure signal

### 2. Sweep Quality Analysis
- Performance with HTF confluence
- Performance without HTF confluence
- Quantifies importance of sweeping into HTF levels vs "sweeping in the void"

### 3. Long-term Profitability Comparison
- Expectancy per trade (both approaches)
- Average RR achieved on winning trades
- Profit factor comparison
- Cumulative returns projection

## Results Summary (2018-2025 Backtest)

### Overall Performance
- **Total Days Analyzed**: 2,893
- **Valid Setups Found**: 13
- **Setup Frequency**: ~0.45% of trading days (highly selective)

### SL A (Structural - Conservative)
- **Win Rate**: 15.38% (2W / 5L)
- **Total P&L**: +34.25 points
- **Profit Factor**: 1.32
- **Expectancy**: +4.00 points per trade
- **Average RR**: 1:0.80

### SL B (Aggressive - Inversion)
- **Win Rate**: 7.69% (1W / 6L)
- **Total P&L**: -12.12 points
- **Profit Factor**: 0.53
- **Expectancy**: -2.93 points per trade
- **Average RR**: 1:2.52

### Key Findings

1. **Best Approach**: SL A (Structural) demonstrated superior expectancy (+4.00 vs -2.93 points)

2. **Fakeout Rate**: 7.69% - SL B is vulnerable to FVG fakeouts where price briefly violates the inversion level

3. **HTF Confluence Impact**: **SIGNIFICANT**
   - With HTF confluence: 18.18% win rate (SL A), 9.09% (SL B)
   - Without HTF confluence: 0.00% win rate (both)
   - **Conclusion**: HTF confluence is CRITICAL for this strategy

4. **RR Advantage**: While SL B offers better RR ratios on wins (1:2.52 vs 1:0.80), the lower win rate negates this advantage

## Usage

### Running the Backtest

```bash
python3 london_reversal_strategy.py
```

### Data Requirements

The script expects CSV files with the following format:
- **Delimiter**: Semicolon (;)
- **Columns**:
  - Column1: Date (DD/MM/YYYY)
  - Column2: Time (HH:MM:SS)
  - Column3: Open
  - Column4: High
  - Column5: Low
  - Column6: Close
  - Column7: Volume
- **Timezone**: Chicago time (UTC-6)

### Required Data Files

- 5-minute data: `ES 5m (2018-2020).csv`, `ES 5m (2021-2023).csv`, `ES 5m (2024-2025).csv`
- 1-hour data: `ES 1h (2018-2025).csv`

### Output Files

1. **london_reversal_results.csv**: Detailed trade log with all entries, exits, and statistics
2. **Console Output**: Comprehensive analysis including:
   - Win rates by SL type
   - Profit factors
   - Expectancy calculations
   - HTF confluence impact
   - Detailed trade-by-trade breakdown

## Dependencies

```bash
pip install pandas numpy
```

## Strategy Insights & Recommendations

### What Works
✅ **HTF Confluence is Essential**: 100% of winning setups had HTF confluence
✅ **Conservative SL (SL A)** provides better expectancy despite lower RR
✅ **Selective Entry Criteria**: Only 13 setups in 8 years ensures quality over quantity
✅ **Clear AMD Model**: Well-defined phases make strategy objective

### Areas for Improvement
⚠️ **Low Sample Size**: 13 setups over 8 years limits statistical significance
⚠️ **Many "Open" Trades**: Several trades didn't reach TP/SL within lookforward window
⚠️ **SL B Underperformance**: Aggressive stop vulnerable to noise despite better RR potential

### Recommended Optimizations

1. **Require HTF Confluence**: Filter out all setups without HTF confluence
2. **Use SL A Approach**: More reliable than SL B based on expectancy
3. **Consider Partial Profits**: Take 50% at TP1, let rest run to TP2
4. **Add Volume Confirmation**: High volume on reversal candle could improve reliability
5. **Test Multiple Timeframes**: Apply to NQ, YM, or RTY for more opportunities

## Strategy Parameters (Adjustable)

| Parameter | Current Value | Purpose |
|-----------|---------------|---------|
| Asian Session Start | 19:00 | Tokyo accumulation begin |
| Asian Session End | 23:59 | Tokyo accumulation end |
| Judas Start | 02:00 | London manipulation begin |
| Judas End | 03:00 | London manipulation end |
| Min Asian Range | 3 points | Filter small ranges |
| Min Reversal Wick | 2 points | Ensure significant rejection |
| Wick-to-Body Ratio | 1.5x | Hammer/Shooting Star criteria |
| Displacement Threshold | 2 points | FVG inversion strength |
| HTF Tolerance | 15 points | Proximity to H1 levels |
| SL A Buffer | 1 point | Beyond reversal extreme |
| SL B Buffer | 1 point | Beyond FVG |

## Advanced Features

### Fair Value Gap (FVG) Detection
- Automatic identification of 3-candle gaps
- Tracks FVG size and location
- Monitors when FVG gets filled and inverted

### HTF Level Detection
- Identifies H1 swing highs and lows
- Uses 5-period rolling window for local extrema
- Checks 7-day lookback for relevant levels

### Trade Simulation
- Realistic order fill simulation
- Tracks both SL approaches simultaneously
- 200-candle (16+ hour) forward-looking window
- Handles partial fills and multi-target management

## Disclaimer

This backtesting system is for educational and research purposes only. Past performance does not guarantee future results. Always practice proper risk management and never risk more than you can afford to lose.

## Author

ICT Trading Strategy Implementation
Based on Inner Circle Trader (ICT) concepts and the Accumulation, Manipulation, Distribution model.

## Version

Version 1.0 - December 2024

---

*For questions, improvements, or bug reports, please refer to the repository documentation.*

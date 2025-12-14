# Judas Swing (London Opening Reversal) Strategy

## Overview

The Judas Swing is a trading strategy that exploits false breakouts during the London opening session. It identifies liquidity sweeps that trap traders before price reverses to its true direction.

## Strategy Components

### 1. Tokyo Session Range (19:00 - 00:00 Previous Day)
- Identifies the high and low of the Tokyo session
- These levels act as liquidity pools that London traders target

### 2. London Opening Sweep (02:00 - 03:30 Current Day)
- Price aggressively breaks Tokyo's high or low
- During the sweep, Fair Value Gaps (FVGs) are created in the sweep direction
- FVG Detection:
  - **Bullish FVG**: `Low[i] > High[i-2]`
  - **Bearish FVG**: `High[i] < Low[i-2]`

### 3. Reversal Pattern Detection
- After sweeping liquidity, price forms a reversal candle:
  - **Hammer** (after sweeping lows) - signals potential bullish reversal
  - **Shooting Star** (after sweeping highs) - signals potential bearish reversal
- Pattern Criteria:
  - Body in top/bottom 30% of candle range
  - Primary wick at least 2x body size
  - Opposite wick < 10% of range

### 4. FVG Inversion Entry
- Wait for price to fill the FVG created during the sweep
- Entry: Close of the candle that completely fills and closes beyond the FVG
- This confirms the reversal with price commitment

### 5. Risk Management

Two stop loss strategies tested:

**SL1 (Aggressive - FVG Based)**
- 1 point above/below the inverted FVG limits
- Tighter risk, but higher probability of premature stop-outs

**SL2 (Conservative - Pattern Based)**
- 1 point above/below the extreme wick of the reversal pattern
- Larger risk, but allows price more room during volatility

### 6. Take Profit Targets

- **Primary Target**: Opposite extreme of Tokyo session
- **Alternative Targets**: Risk-Reward ratios of 2:1, 3:1, and 3.5:1

## Backtest Results Summary

### NQ (2024)
- **Total Trades**: 63
- **SL1 Win Rate**: 7.94% (not viable)
- **SL2 Win Rate**: 20.63% (better but still challenging)
- **Premature SL1 Stops**: 13 (20.6%)
- **Premature SL2 Stops**: 9 (14.3%)
- **Target Hit Rate**: 28.57%
- **Best RR for SL1**: 2:1 with 44.44% success
- **Best RR for SL2**: 2:1 with 34.92% success

### ES (2024-2025)
- **Total Trades**: 90
- **SL1 Win Rate**: 5.56% (not viable)
- **SL2 Win Rate**: 30.00% (significantly better)
- **Premature SL1 Stops**: 27 (30.0%)
- **Premature SL2 Stops**: 14 (15.6%)
- **Target Hit Rate**: 35.56%
- **Best RR for SL1**: 2:1 with 38.89% success
- **Best RR for SL2**: 2:1 with 41.11% success

## Key Findings

### 1. Stop Loss Comparison
The **conservative stop loss (SL2)** performs significantly better than the aggressive FVG-based stop (SL1) across both instruments:
- NQ: SL2 has 12.7% higher win rate
- ES: SL2 has 24.4% higher win rate

### 2. Premature Stop-Outs
The aggressive SL1 gets stopped out prematurely much more frequently:
- Nearly 2x more premature stops in NQ
- Nearly 2x more premature stops in ES

This indicates the tight stop doesn't account for normal volatility during reversals.

### 3. Reversal Characteristics
- **NQ**: More volatile with average 1.91 points/candle movement
- **ES**: Smoother with average 0.39 points/candle movement
- Average time to resolution: 160-219 minutes (32-44 candles)

### 4. Tokyo Target Success
Both instruments show moderate success reaching opposite Tokyo extreme:
- NQ: 28.57%
- ES: 35.56%

This suggests the full Tokyo range target may be ambitious for this setup.

### 5. Optimal Risk-Reward
The **2:1 risk-reward ratio** performs best for both stop loss strategies:
- More achievable than 3:1 or 3.5:1
- Provides reasonable profit potential while acknowledging market reality

## Strategy Psychology

### Why FVG Inversion Entry Works
The FVG inversion entry is superior to entering directly on the reversal pattern because:
1. **Confirmation**: Requires price to show commitment by filling the gap
2. **Reduces False Signals**: Eliminates entries on patterns that fail immediately
3. **Better Timing**: Enters as momentum shifts rather than at potential exhaustion

### Why Conservative SL Outperforms
1. **Volatility Buffer**: Allows for normal price oscillation during reversals
2. **Reduces Premature Exits**: Gives the trade room to develop
3. **Better Risk/Reward**: Despite larger risk, the improved win rate compensates

## Recommendations

### For NQ Trading
1. Use **SL2 (conservative)** stop loss strategy
2. Target **2:1 risk-reward** rather than full Tokyo range
3. Be selective - only ~20% win rate means position sizing is critical
4. Consider filtering setups further (e.g., trend alignment, volatility conditions)

### For ES Trading
1. Use **SL2 (conservative)** stop loss strategy
2. Target **2:1 risk-reward** with 41% success rate
3. 30% win rate is more viable but still requires discipline
4. ES shows better consistency than NQ

### Overall Strategy Assessment
While the strategy shows interesting patterns, the current iteration has:
- **Low win rates** even with conservative stops
- **Negative expectancy** in tested periods
- **High premature stop-out risk** with aggressive stops

**Potential Improvements:**
1. Add confluence filters (order blocks, previous day's levels)
2. Require stronger reversal confirmation (multiple patterns)
3. Consider time-based filters (specific London session times)
4. Volume confirmation for sweep and reversal
5. Trend alignment with higher timeframes
6. Wait for deeper Tokyo range before considering setup

## Files Generated

1. `judas_swing_strategy.py` - Complete backtesting implementation
2. `requirements.txt` - Python dependencies
3. `judas_swing_nq_2024_results.json` - Detailed NQ trade data
4. `judas_swing_nq_2024_results_report.txt` - NQ analysis report
5. `judas_swing_es_2024_2025_results.json` - Detailed ES trade data
6. `judas_swing_es_2024_2025_results_report.txt` - ES analysis report

## Usage

```bash
# Install dependencies
pip install -r requirements.txt

# Run backtest
python judas_swing_strategy.py
```

The script will automatically process both NQ (2024) and ES (2024-2025) data files and generate comprehensive reports.

## Technical Implementation Details

### Data Processing
- Semicolon-delimited CSV parsing
- Chicago time (UTC-6) - no timezone conversion needed
- 5-minute candle data

### Detection Algorithms
- Tokyo session range calculation
- FVG gap detection with precise mathematical conditions
- Pattern recognition using percentage-based criteria
- FVG inversion detection with forward-looking logic
- Trade simulation with concurrent SL tracking

### Analysis Features
- Dual stop loss comparison
- Multiple risk-reward ratio testing
- Premature stop-out tracking
- Favorable/adverse excursion analysis
- Reversal speed calculation
- Comprehensive statistics and insights

## Conclusion

The Judas Swing strategy identifies a real market phenomenon - liquidity sweeps during London opening. However, successful implementation requires:
- Conservative stop placement to avoid premature exits
- Realistic profit targets (2:1 RR rather than full Tokyo range)
- Strict risk management given modest win rates
- Additional confluence factors to improve edge
- Significant position sizing discipline

The strategy framework is sound and the detection logic is robust, but traders should use this as a starting point for further refinement rather than as a standalone system.

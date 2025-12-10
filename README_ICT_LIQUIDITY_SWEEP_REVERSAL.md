# ICT Liquidity Sweep Reversal Strategy

## Overview

This strategy implements the ICT (Inner Circle Trader) methodology to identify high-probability reversal setups based on liquidity sweeps in the Nasdaq Futures (NQ) market, confirmed with S&P 500 Futures (ES) divergence analysis.

## Strategy Concept

The ICT Liquidity Sweep Reversal strategy identifies moments when "smart money" (institutions) sweep liquidity from retail traders by taking out swing highs or lows, then reverse the market in the opposite direction. This creates high-probability reversal opportunities when confirmed with multiple factors.

## Key Components

### 1. Time & Killzones ⏰

The strategy ONLY trades during specific high-volume institutional trading windows:

- **London Open**: 2:00 AM - 5:00 AM New York Time
- **NY Open**: 9:30 AM - 11:00 AM New York Time

These periods have the highest institutional participation and the most reliable setups.

### 2. Liquidity Sweep Detection 🔄

A liquidity sweep occurs when price exceeds a recent swing high or low:

- **Buy Side Liquidity Sweep**: Price exceeds a previous swing high (bearish reversal expected)
- **Sell Side Liquidity Sweep**: Price drops below a previous swing low (bullish reversal expected)

The strategy detects swing points on 15m and 1h timeframes with configurable lookback periods.

### 3. Sweep Quality Analysis ✨

Not all sweeps are created equal. The quality is determined by the candle structure:

- **Excellent (Score 3)**: Strong rejection wick (>60% of candle range)
  - Indicates strong rejection of the swept level
  - Most reliable for reversals

- **Good (Score 2)**: Moderate rejection wick (40-60% of candle range)
  - Shows some rejection
  - Medium reliability

- **Poor (Score 1)**: Full body breakout (<40% wick)
  - Minimal rejection, price continues through
  - Lower reliability, may not reverse

### 4. SMT Divergence (Smart Money Tool) 📊

SMT Divergence compares NQ and ES to identify when they're diverging:

- **Bearish SMT**: NQ makes Higher High, ES makes Lower High or Double Top
  - Indicates weakness in the rally
  - Reversal down expected

- **Bullish SMT**: NQ makes Lower Low, ES makes Higher Low or Double Bottom
  - Indicates weakness in the decline
  - Reversal up expected

**Scoring**:
- High Probability SMT (pure divergence): +3 points
- Medium Probability SMT (double top/bottom): +2 points
- No SMT: 0 points

### 5. Displacement & Market Structure Shift ⚡

After the sweep, we look for an impulsive move (displacement) in the reversal direction:

- **Displacement**: Large-bodied candle (>70% body ratio, >0.3% price change)
- **Market Structure Shift (MSS)**: The displacement breaks previous structure
  - For bearish reversal: Breaks below recent swing low
  - For bullish reversal: Breaks above recent swing high

**Scoring**:
- Strong displacement with MSS: +2 points
- Moderate displacement without MSS: +1 point
- No displacement: 0 points

### 6. Fair Value Gap (FVG) 📍

An FVG is a price imbalance left by the impulsive move:

- **Bearish FVG**: Gap where Low[i-1] > High[i+1]
- **Bullish FVG**: Gap where High[i-1] < Low[i+1]

FVGs act as magnets for price, providing:
- Entry zones for the trade
- Targets for price to fill the gap

**Scoring**: +1 point if present

## Probability Scoring System 🎲

Each setup is scored from 0-9 points based on the factors above:

| Score Range | Probability | Recommendation |
|-------------|-------------|----------------|
| 7-9 points | **Very High** | Prime trading opportunity |
| 5-6 points | **High** | Good trading opportunity |
| 3-4 points | **Medium** | Acceptable with caution |
| 0-2 points | **Low** | Skip (filtered out) |

### Scoring Breakdown:
- Sweep Quality: 0-3 points
- SMT Divergence: 0-3 points
- Displacement & MSS: 0-2 points
- FVG Present: 0-1 point

## Usage

### Running the Analysis

```bash
python3 ict_liquidity_sweep_reversal.py
```

The script will:
1. Load NQ data (1m, 5m, 15m, 1h timeframes)
2. Load ES data (5m timeframe) for SMT analysis
3. Scan for setups on 15m timeframe (full year 2024)
4. Scan for setups on 5m timeframe (December 2024)
5. Generate detailed reports

### Output Files

- **ICT_Liquidity_Sweep_Reversal_Report_2024.txt**: Full year analysis on 15m
- **ICT_Liquidity_Sweep_Reversal_Report_5m_Dec2024.txt**: Last month analysis on 5m

### Requirements

```bash
pip install -r requirements.txt
```

Required packages:
- pandas>=2.0.0
- numpy>=1.24.0
- pytz>=2023.3

## Results (2024 Data)

### 15m Timeframe Analysis
- **Total Setups Found**: 1,313
- **Very High Probability**: 5 setups (0.4%)
- **High Probability**: 221 setups (16.8%)
- **Medium Probability**: 1,087 setups (82.8%)

### 5m Timeframe Analysis (December 2024)
- **Total Setups Found**: 448
- More frequent but requires more monitoring

## Example Setup

```
SETUP #745
Date/Time: 2024-07-22 10:00:00 EDT
Timeframe: 15m
Killzone: NY Open
Price: 20,797.61

LIQUIDITY SWEEP:
  Type: Buy Side Liquidity
  Sweep Level: 20,710.71
  Expected Direction: Bearish Reversal

SWEEP QUALITY:
  Quality: Good
  Type: Rejection Wick
  Wick Ratio: 40.7%

SMT DIVERGENCE:
  ✓ Confirmed: Bearish SMT Divergence (Double Top)
  NQ: Higher High
  ES: Double Top
  Probability: Medium

DISPLACEMENT & MSS:
  ✓ Displacement: Detected (candle +1)
  MSS: ✓ Yes
  Strength: Strong

FAIR VALUE GAP (FVG):
  ✓ Detected: Bearish FVG
  Gap Range: 20,720.37 - 20,762.64
  Gap Size: 42.27 points (0.20%)

OVERALL ASSESSMENT:
  Probability: Very High
  Score: 7/9
```

## Trading the Setup

### Entry Strategy
1. Wait for all confirmations (sweep + quality + SMT)
2. Enter on the displacement candle close or
3. Enter on a pullback to the FVG zone (better risk/reward)

### Stop Loss
- For bearish reversals: Above the sweep high + buffer
- For bullish reversals: Below the sweep low + buffer

### Take Profit
1. First target: FVG fill (if entering before gap is filled)
2. Second target: Previous swing in opposite direction
3. Third target: Market structure level

### Risk Management
- Risk 1-2% of account per trade
- Very High Probability setups: Consider 2% risk
- High Probability setups: Use 1.5% risk
- Medium Probability setups: Use 1% risk or skip

## Advantages

1. **Objective Rules**: Clear criteria eliminate guesswork
2. **Multiple Confirmations**: Requires several factors to align
3. **High Win Rate Potential**: Very High probability setups have strong edge
4. **Clear Entry/Exit**: FVGs and MSS provide specific levels
5. **Time-Based**: Only trades during optimal institutional hours

## Limitations

1. **Frequency**: Very High probability setups are rare (5 per year on 15m)
2. **Complexity**: Requires understanding multiple ICT concepts
3. **Data Requirements**: Needs both NQ and ES data
4. **Discretion Needed**: Some interpretation required for quality assessment

## Customization

You can adjust these parameters in the code:

```python
# Killzone times (New York time)
self.london_killzone = (time(2, 0), time(5, 0))
self.ny_killzone = (time(9, 30), time(11, 0))

# Swing detection lookback periods
self.swing_lookback_15m = 20  # bars
self.swing_lookback_1h = 10   # bars

# SMT divergence tolerance
self.smt_tolerance = 0.002  # 0.2% for double tops/bottoms

# Displacement minimum body size
self.min_displacement_pct = 0.003  # 0.3%

# FVG lookback period
self.fvg_lookback = 60  # bars
```

## Further Development

Potential enhancements:
1. **Backtesting Module**: Add trade simulation with P&L tracking
2. **Real-time Alerts**: Integrate with trading platform for live monitoring
3. **Machine Learning**: Train model to weigh factors optimally
4. **Multi-timeframe Confirmation**: Require alignment across timeframes
5. **Volume Analysis**: Add volume profile confirmation
6. **Order Flow**: Integrate order flow data for additional confirmation

## References

- ICT (Inner Circle Trader) YouTube channel and concepts
- Smart Money Concepts (SMC)
- Market structure and Fair Value Gaps
- Institutional order flow principles

## Author

Implementation of ICT methodology for systematic analysis of reversal setups.

## License

This is an educational tool for strategy research and backtesting. Use at your own risk in live trading.

---

**Disclaimer**: Past performance does not guarantee future results. This strategy is for educational purposes only. Always practice proper risk management and test thoroughly before live trading.

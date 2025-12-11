# London Killzone FVG Analysis - Literal Times

## Overview

This script (`london_killzone_literal_times_backtest.py`) analyzes Fair Value Gaps (FVG) during the literal hours **01:00-03:55** from CSV files **WITHOUT any timezone conversion**.

## Key Features

### ⚠️ IMPORTANT - No Timezone Conversion
- Uses **exact times from CSV files**: 01:00, 01:05, 01:10... to 03:55
- **NO timezone conversion** - timestamps are used as-is
- This is the key difference from other analysis scripts that convert to Chicago time

### CSV Format
```
Date;Time;Open;High;Low;Close;Volume
10/11/2025;01:00:00;25469.5;25481.5;25463.25;25474.5;793
```

## Three Trading Scenarios

### Scenario 1: Liquidity Sweep + FVG (Turtle Soup)
- Price sweeps beyond 12-candle high/low
- Candle closes back inside range (rejection)
- Immediate FVG forms after the sweep
- **Results (2018-2025):**
  - Total Trades: 675
  - Win Rate: 44.3%
  - Total P&L: +3,746.41 points
  - Profit Factor: 1.36

### Scenario 2: Inverted FVG (IFVG)
- Standard FVG gets "flipped" by opposite price action
- Bearish FVG becomes bullish support (vice versa)
- Entry on return to test the inverted zone
- **Results (2018-2025):**
  - Total Trades: 5,645
  - Win Rate: 38.9%
  - Total P&L: -2,777.22 points
  - Profit Factor: 0.96

### Scenario 3: Continuation FVG (Control Group) 🏆
- Standard FVG without sweep or inversion
- Simple trend continuation setups
- **Results (2018-2025):**
  - Total Trades: 7,621
  - Win Rate: 54.4%
  - Total P&L: +128,950.43 points
  - Profit Factor: 2.11
  - **Best performing scenario!**

## Trade Rules

### Entry
- Price mitigation of FVG zone (price touches the zone)
- Entry at mid-point of FVG zone

### Stop Loss
- Scenario 1: 10 points beyond FVG boundary
- Scenario 2: 10 points beyond FVG boundary
- Scenario 3: 10 points beyond FVG boundary

### Take Profit
- Fixed 2:1 Risk/Reward ratio

### Forced Exit
- All trades closed at **16:00 literal time** from CSV

## FVG Detection Logic

### Bullish FVG (Gap Up)
```
Condition: High(n-1) < Low(n+1)
Zone: [High(n-1), Low(n+1)]
Direction: Long
```

### Bearish FVG (Gap Down)
```
Condition: Low(n-1) > High(n+1)
Zone: [High(n+1), Low(n-1)]
Direction: Short
```

## Data Analysis

### Overall Statistics (2018-2025)
- **Total rows loaded:** 554,518
- **Killzone candles:** 73,113 (13.18%)
- **Total FVGs detected:** 17,707
  - Bullish FVGs: 9,333
  - Bearish FVGs: 8,374
  - Average FVG size: 33.94 points

### Time Distribution
Each 5-minute interval from 01:00 to 03:55 has approximately 2,030-2,031 candles across all years.

## Usage

### Requirements
```bash
pip install pandas numpy pytz
```

### Run the Script
```bash
python3 london_killzone_literal_times_backtest.py
```

### Expected Output
1. Data loading progress for each year (2018-2025)
2. Killzone filtering statistics
3. FVG detection results
4. Scenario setup counts
5. Detailed results for each scenario
6. Comparative summary table
7. Best performing scenario

## Key Findings

1. **Scenario 3 (Continuation FVG) is the clear winner** with the highest win rate (54.4%) and profit factor (2.11)

2. **Scenario 1 (Liquidity Sweep)** is modestly profitable with a 1.36 profit factor

3. **Scenario 2 (Inverted FVG)** is slightly unprofitable with a 0.96 profit factor, suggesting inversions may not be reliable signals

4. **Long vs Short Performance in Scenario 3:**
   - Long trades: +63,324.22 points (14.56 avg)
   - Short trades: +65,626.21 points (20.06 avg)
   - Short trades have better average P&L

## Technical Details

### Parameters
- `LOOKBACK_CANDLES = 12` (60 minutes for liquidity sweep detection)
- `MITIGATION_WINDOW = 60` (5 hours to check for FVG mitigation)
- `INVERSION_WINDOW = 40` (~3.3 hours to check for FVG inversion)
- `RR_RATIO = 2.0` (Fixed 2:1 Risk/Reward)

### Processing Flow
1. Load all CSV files (2018-2025)
2. Filter for literal times 01:00-03:55
3. Detect all FVGs
4. Classify FVGs into scenarios
5. Simulate trades with proper risk management
6. Generate comprehensive results

## Comparison with Other Scripts

### vs. `london_killzone_three_scenarios_backtest.py`
- **Main difference:** This script uses **literal CSV times** without timezone conversion
- **Other script:** Converts to Chicago time (CST/CDT)
- **Use case:** This script is better when CSV timestamps are already in the desired timezone

### Files in Repository
- `london_killzone_literal_times_backtest.py` - **This script** (literal times)
- `london_killzone_three_scenarios_backtest.py` - Chicago time conversion
- `london_killzone_fvg_scenario_analysis.py` - Original FVG analysis

## Future Enhancements

Potential improvements:
1. Add more granular exit strategies (trailing stops, partial exits)
2. Include additional filters (volume, trend confirmation)
3. Test different time ranges for liquidity sweep lookback
4. Analyze seasonal patterns or day-of-week effects
5. Export detailed trade logs to CSV for further analysis

## Author Notes

This script was created to analyze ICT (Inner Circle Trader) concepts using real market data. The focus on literal times allows for direct analysis of the data without timezone assumptions.

**Remember:** Past performance does not guarantee future results. Always use proper risk management in live trading.

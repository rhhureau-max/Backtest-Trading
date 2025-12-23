# IFVG (Inversion Fair Value Gap) Backtest Results

## Overview
This backtest analyzes IFVG entries based on 1,867 Judas Swings detected in NQ futures data from 2018-2025.

## Files Created
1. **ifvg_backtest.py** - Complete backtest script
2. **ifvg_backtest_1m.csv** - Results for 1-minute timeframe (3,921 trade records)
3. **ifvg_backtest_5m.csv** - Results for 5-minute timeframe (3,370 trade records)

## Strategy Logic

### Entry Setup
1. **Identify Manipulation Leg**: From Tokyo level break to Manipulation_Extreme
2. **Detect FVGs during manipulation**:
   - Bearish FVG (for longs): 3 candles where candle[i-1].Low > candle[i+1].High
   - Bullish FVG (for shorts): 3 candles where candle[i-1].High < candle[i+1].Low
3. **Entry Trigger** (Inversion):
   - Long: Close ABOVE bearish FVG high
   - Short: Close BELOW bullish FVG low

### Risk Management
- **Stop Loss**: 0.5 points beyond Manipulation_Extreme
- **TP1**: Tokyo Equilibrium = (Tokyo_High + Tokyo_Low) / 2
- **TP2**: Opposing Liquidity = Tokyo_Low (shorts) or Tokyo_High (longs)
- **Commission**: $4 per trade

### Three Testing Scenarios

#### Scenario A: 100% at Equilibrium (TP1)
- Take full position off at Tokyo Equilibrium
- Win = TP1 hit before SL
- Loss = SL hit first

#### Scenario B: 100% at Opposing Liquidity (TP2)
- Hold full position until Opposing Liquidity
- Win = TP2 hit before SL
- Loss = SL hit first

#### Scenario C: 50/50 Split
- If TP1 hit first: Take 50% profit, move remaining 50% to breakeven
- Then check if TP2 hit or BE stop hit
- Calculate P&L based on actual outcomes

## Results Summary

### 1-Minute Timeframe

**Scenario A (100% at Equilibrium):**
- Total Trades: 1,667
- Wins: 1,121 | Losses: 546
- Win Rate: 67.25%
- Total P&L: $10,087.85
- Avg Win: $477.86 | Avg Loss: -$962.62
- Profit Factor: 1.02
- Expectancy: $6.05

**Scenario B (100% at Opposing Liquidity):**
- Total Trades: 587
- Wins: 40 | Losses: 547
- Win Rate: 6.81%
- Total P&L: -$518,608.69
- Avg Win: $179.89 | Avg Loss: -$961.25
- Profit Factor: 0.01
- Expectancy: -$883.49

**Scenario C (50/50 Split):**
- Total Trades: 1,667
- Wins: 1,061 | Losses: 603 | Breakeven: 3
- Win Rate: 63.65%
- Total P&L: -$256,315.37
- Avg Win: $269.87 | Avg Loss: -$899.90
- Profit Factor: 0.53
- Expectancy: -$153.76

### 5-Minute Timeframe

**Scenario A (100% at Equilibrium):**
- Total Trades: 1,404
- Wins: 955 | Losses: 449
- Win Rate: 68.02%
- Total P&L: -$29,629.31
- Avg Win: $430.84 | Avg Loss: -$982.35
- Profit Factor: 0.93
- Expectancy: -$21.10

**Scenario B (100% at Opposing Liquidity):**
- Total Trades: 562
- Wins: 110 | Losses: 452
- Win Rate: 19.57%
- Total P&L: -$398,324.45
- Avg Win: $419.10 | Avg Loss: -$983.24
- Profit Factor: 0.10
- Expectancy: -$708.76

**Scenario C (50/50 Split):**
- Total Trades: 1,404
- Wins: 849 | Losses: 550 | Breakeven: 5
- Win Rate: 60.47%
- Total P&L: -$213,992.56
- Avg Win: $287.61 | Avg Loss: -$833.01
- Profit Factor: 0.53
- Expectancy: -$152.42

## CSV Output Format

Each CSV file contains the following columns:
- **Date**: Trade date
- **Direction**: bearish (long) or bullish (short)
- **Entry_Price**: Entry price after IFVG inversion
- **SL**: Stop loss level
- **TP1**: Tokyo Equilibrium target
- **TP2**: Opposing Liquidity target
- **Scenario**: scenario_a, scenario_b, or scenario_c
- **Outcome**: win, loss, or breakeven
- **PnL**: Profit/Loss in USD (includes $4 commission)
- **FVG_High**: High of the Fair Value Gap
- **FVG_Low**: Low of the Fair Value Gap

## Key Findings

1. **Scenario A (TP1 only)** shows the best performance with 67-68% win rate
2. **Scenario B (TP2 only)** has very low win rates (6.81% - 19.57%) as price rarely reaches opposing liquidity
3. **Scenario C (50/50 split)** shows moderate win rates (60-63%) but suffers from larger losing trades
4. The 1m timeframe shows slightly better entry precision
5. Only Scenario A on 1m timeframe is profitable (+$10,087.85)

## Usage

Run the backtest:
```bash
python ifvg_backtest.py
```

The script will:
1. Load Judas Swing data
2. Process all 1m and 5m price data (including unzipping 1m files)
3. Detect FVGs during manipulation legs
4. Test entry triggers and simulate trades
5. Generate CSV files with all trade results
6. Display statistics for each scenario

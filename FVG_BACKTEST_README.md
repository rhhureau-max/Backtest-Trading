# Fair Value Gap (FVG) Reversal Strategy Backtest

## Overview
This repository contains a comprehensive backtesting implementation for a Fair Value Gap (FVG) reversal trading strategy on Nasdaq Futures (NQ) using 5-minute timeframe data with Risk-Reward based take profits.

## Strategy Description

### Fair Value Gap (FVG) Definition
- **Bearish FVG**: A downward imbalance where the high of candle N-1 is greater than the low of candle N+1
- **Bullish FVG**: An upward imbalance where the low of candle N-1 is less than the high of candle N+1

### Long Setup (Bearish FVG Reversal)
1. A bearish FVG forms (3 candles with gap)
2. Price returns into the FVG zone
3. Price fills and exceeds the FVG upper bound
4. A bullish candle validates the breakout
5. **Entry**: Long at close of validation candle
6. **Stop Loss**: Swing Low - 0.5 points (FIXED)
7. **Take Profit**: Entry + R × (Entry - Stop) where R = 1.0 or 1.5

### Short Setup (Bullish FVG Reversal)
1. A bullish FVG forms (3 candles with gap)
2. Price returns into the FVG zone
3. Price fills and exceeds the FVG lower bound
4. A bearish candle validates the breakout
5. **Entry**: Short at close of validation candle
6. **Stop Loss**: Swing High + 0.5 points (FIXED)
7. **Take Profit**: Entry - R × (Stop - Entry) where R = 1.0 or 1.5

### Key Strategy Features
- **One Trade at a Time**: No pyramiding or simultaneous positions
- **Fixed Stop Loss**: Always Swing ± 0.5 points, never varies
- **Risk-Reward Based TP**: 1R or 1.5R targets (not structure-based)
- **Session-Based**: All trades close at end of session if not hit

## Data Requirements

### Files
The script expects 5-minute CSV files for years 2018-2025 in the following format:
- Filename pattern: `YYYY 5m.csv` (e.g., "2018 5m.csv", "2019 5m.csv")
- Delimiter: Semicolon (;)

### CSV Structure
```
Column1;Column2;Column3;Column4;Column5;Column6;Column7
Date;Time;Open;High;Low;Close;Volume
DD/MM/YYYY;HH:MM:SS;float;float;float;float;int
```

### Trading Session
- **Session**: 02:00-06:00 (morning session)
- **Timezone**: Uses timestamps exactly as they appear in files (no conversion)

## Installation

### Requirements
- Python 3.7+
- pandas
- numpy

### Install Dependencies
```bash
pip install pandas numpy
```

## Usage

### Run the Backtest
```bash
python3 backtest_fvg_reversal.py
```

The script automatically runs TWO backtests:
1. **1R Strategy**: Take profit at 1× risk
2. **1.5R Strategy**: Take profit at 1.5× risk

### Output
The script generates:
1. **Console Output**: Comprehensive performance report with statistics for both strategies
2. **CSV Files**: 
   - `fvg_reversal_trades_1.0R.csv` - All 1R trades with details
   - `fvg_reversal_trades_1.5R.csv` - All 1.5R trades with details
3. **Comparative Analysis**: Side-by-side comparison of both strategies

## Results Summary

### 1R Strategy Performance (2018-2025)
- **Total Trades**: 3,574
- **LONG Trades**: 3,281 (Win Rate: 52.26%)
- **SHORT Trades**: 293 (Win Rate: 45.39%)
- **Global Win Rate**: 51.76%
- **Net Gain**: +2,700.20 points
- **Profit Factor**: 1.06
- **Expectancy**: +0.76 points per trade
- **Maximum Drawdown**: 1,231.01 points
- **Average Win**: 25.60 points
- **Average Loss**: 25.90 points

### 1.5R Strategy Performance (2018-2025)
- **Total Trades**: 2,811
- **LONG Trades**: 2,582 (Win Rate: 38.11%)
- **SHORT Trades**: 229 (Win Rate: 44.10%)
- **Global Win Rate**: 38.60%
- **Net Gain**: -5,519.86 points
- **Profit Factor**: 0.87
- **Expectancy**: -1.96 points per trade
- **Maximum Drawdown**: 5,697.07 points
- **Average Win**: 34.01 points
- **Average Loss**: 24.58 points

### Comparative Analysis: 1R vs 1.5R

| Metric | 1R Strategy | 1.5R Strategy | Winner |
|--------|-------------|---------------|--------|
| Total Trades | 3,574 | 2,811 | 1R |
| Win Rate (%) | 51.76% | 38.60% | 1R |
| Net Points | +2,700.20 | -5,519.86 | 1R |
| Profit Factor | 1.06 | 0.87 | 1R |
| Expectancy | +0.76 pts | -1.96 pts | 1R |
| Max Drawdown | 1,231 pts | 5,697 pts | 1R |

**RECOMMENDATION**: The **1R strategy is clearly superior** for this FVG reversal setup:
- 304% better net profitability
- 13% higher win rate
- 78% lower maximum drawdown
- Positive vs negative expectancy
- More consistent performance

### Best Performing Periods (1R Strategy)
- **Best Year**: 2020 (+1,676.52 points)
- **Best Months**: March, October, September
- **Maximum Win Streak**: 12 consecutive wins
- **Maximum Loss Streak**: 9 consecutive losses

### R-Multiple Distribution (1R Strategy)
- ~52% of trades achieve +1R (winners)
- ~48% of trades achieve -1R (losers)
- Clean distribution confirms proper risk-reward execution

## Interpretation

### Key Observations
1. **1R Target Superior**: Despite larger wins with 1.5R, the lower win rate makes it unprofitable
2. **Win Rate Critical**: With 1R, need >50% win rate; achieved 51.76% ✓
3. **One Trade at a Time**: Prevents overexposure and reduces drawdown
4. **Fixed Stop Loss**: Swing ± 0.5 provides consistent risk management
5. **Long Bias**: Strategy naturally finds more bullish reversal setups
6. **Consistency**: 1R strategy maintains positive expectancy across years

### For Discretionary Traders
Consider enhancing the mechanical 1R signals with:
- Volume profile analysis at FVG zones
- Multiple timeframe confirmation
- Broader market context (trend, support/resistance)
- Quality assessment of validation candles
- News event awareness during the 02:00-06:00 session
- Avoid trades during high volatility events

### Risk Management
- All trades use defined stop losses (Swing ± 0.5 points)
- Take profit targets are risk-reward based (1R or 1.5R)
- Only one position open at any time (no pyramiding)
- No positions held beyond the trading session
- Maximum risk per trade is predetermined by swing-based stops

## Script Features

### Core Components
1. **Data Loading**: Loads all 5m CSV files (2018-2025)
2. **Session Filtering**: Extracts only 02:00-06:00 data
3. **FVG Detection**: Identifies bearish and bullish fair value gaps
4. **Swing Point Detection**: Finds local highs/lows for stops
5. **Trade Execution**: Simulates entries and exits with one-trade-at-a-time rule
6. **Performance Analysis**: Comprehensive statistics and reporting
7. **Comparative Analysis**: Side-by-side 1R vs 1.5R comparison

### Analysis Metrics (Enhanced)
- Global performance (total/long/short trades, win rates, points)
- Profit factor and expectancy calculations
- R-Multiple distribution analysis
- Advanced statistics (drawdown, streaks)
- Annual and monthly performance breakdowns
- Trade type distribution (LONG vs SHORT)
- Qualitative insights and recommendations
- Side-by-side strategy comparison

### Risk-Reward Implementation
- **1R Mode**: TP = Entry ± 1 × Risk (where Risk = Entry - Stop)
- **1.5R Mode**: TP = Entry ± 1.5 × Risk
- Stop Loss ALWAYS = Swing ± 0.5 points (never varies)
- Each trade records its R-multiple for analysis

## Notes

### Strategy Rules
- No discretionary filters applied
- Mechanical implementation of exact strategy specification
- No optimization or curve fitting
- Uses only provided historical data
- No look-ahead bias
- One trade at a time enforced

### New Features vs Original
- ✅ Fixed stop loss at Swing ± 0.5 (previously variable)
- ✅ Risk-Reward based TP: 1R and 1.5R (previously structure-based)
- ✅ One trade at a time (previously allowed simultaneous)
- ✅ Enhanced reporting with R-distribution
- ✅ Separate LONG/SHORT metrics
- ✅ Dual backtest (1R and 1.5R)
- ✅ Comparative analysis between strategies

### Limitations
- Past performance does not guarantee future results
- Does not account for slippage or commissions
- Assumes perfect execution at specified prices
- Limited to 02:00-06:00 session only
- Requires clean, consistent data format
- Results are specific to NQ futures (may differ on other instruments)

## File Structure
```
.
├── backtest_fvg_reversal.py            # Main backtest script (UPDATED)
├── fvg_reversal_trades_1.0R.csv        # Output: 1R trade log
├── fvg_reversal_trades_1.5R.csv        # Output: 1.5R trade log
├── FVG_BACKTEST_README.md              # This file (UPDATED)
├── 2018 5m.csv                         # Data files
├── 2019 5m.csv
├── ...
└── 2025 5m.csv
```

## Changelog

### Version 2.0 (Current)
- Modified stop loss: Swing ± 0.5 points (fixed)
- Modified take profit: 1R and 1.5R risk-reward based
- Implemented one-trade-at-a-time rule
- Enhanced reporting with R-distribution
- Added dual backtest (1R + 1.5R)
- Added comparative analysis
- Separate LONG/SHORT trade metrics
- Improved qualitative analysis

### Version 1.0 (Original)
- Variable stop loss based on swing points
- Structure-based take profit (swing highs/lows)
- Multiple simultaneous trades allowed
- Basic reporting

## License
This is a backtesting tool for educational and research purposes.

## Disclaimer
Trading futures involves substantial risk of loss. This backtest is for informational purposes only and does not constitute trading advice. Past performance is not indicative of future results. The 1.5R strategy showed negative expectancy in this backtest - use with extreme caution or avoid entirely.

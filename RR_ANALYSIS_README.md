# Risk/Reward (RR) Analysis Documentation

## Overview

The RR Analysis system extends the backtest trading strategy by simulating different stop-loss (SL) placements and risk/reward (RR) ratios for each identified trade. This helps determine the optimal combination of SL placement and RR ratio for the trading strategy.

## How It Works

### 1. Prerequisites

Before running the RR analysis, you must first generate the backtest results:

```bash
python3 backtest_strategy.py
```

This will create `backtest_results.csv` containing all trades where the 8:30 AM candle meets the strategy conditions.

### 2. Running RR Analysis

Execute the RR analysis script:

```bash
python3 rr_analysis.py
```

The analysis will:
- Load all identified trades from `backtest_results.csv`
- Preload all required data files for efficient processing
- Simulate each trade with 36 different scenarios (4 SL placements × 9 RR ratios)
- Track whether Stop Loss or Take Profit was hit first
- Calculate Maximum Adverse Excursion (MAE) and Maximum Favorable Excursion (MFE)
- Generate comprehensive reports and CSV files

## Stop-Loss Placements

Four different SL placements based on the 8:30 AM candle body:

### SL_100 (Full Retracement)
- **Position**: At the opposite end of the candle body (Open price)
- **Bullish**: SL = Open (lowest risk point)
- **Bearish**: SL = Open (highest risk point)
- **Description**: Most conservative - full body must retrace to hit SL

### SL_75 (75% Retracement)
- **Position**: 75% back from Close towards Open
- **Bullish**: SL = Open + 0.25 × (Close - Open)
- **Bearish**: SL = Open - 0.25 × (Open - Close)
- **Description**: Moderately conservative

### SL_50 (50% Retracement - Middle)
- **Position**: Exactly at the middle of the candle body
- **Bullish**: SL = Open + 0.50 × (Close - Open)
- **Bearish**: SL = Open - 0.50 × (Open - Close)
- **Description**: Balanced approach

### SL_25 (25% Retracement)
- **Position**: 25% back from Close towards Open (tightest)
- **Bullish**: SL = Open + 0.75 × (Close - Open)
- **Bearish**: SL = Open - 0.75 × (Open - Close)
- **Description**: Most aggressive - closest to entry

## Risk/Reward Ratios

Nine RR ratios are tested: **1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0**

### Calculation Logic

For **BULLISH** trades:
- Entry: Close price of 8:30 AM candle
- Risk = Entry - SL
- Take Profit = Entry + (Risk × RR_Ratio)

For **BEARISH** trades:
- Entry: Close price of 8:30 AM candle
- Risk = SL - Entry
- Take Profit = Entry - (Risk × RR_Ratio)

## Output Files

### 1. rr_analysis_complete.csv
Complete dataset with all 135,864 trade scenarios (3,774 trades × 36 combinations).

**Columns**:
- `Date`, `Time`, `Timeframe`, `Candle_Type`
- `Entry_Price`, `Open_Price`
- `SL_Placement`, `SL_Price`
- `RR_Ratio`, `TP_Price`
- `Risk_Amount`, `Potential_Reward`
- `Outcome` (WIN/LOSS/PENDING)
- `Exit_Price`, `Exit_DateTime`
- `Bars_In_Trade`
- `PnL` (Profit/Loss amount)
- `MAE` (Maximum Adverse Excursion)
- `MFE` (Maximum Favorable Excursion)

### 2. rr_analysis_SL_XXX.csv
Separate files for each SL placement (SL_100, SL_75, SL_50, SL_25).
Each file contains all 9 RR ratios for that specific SL placement.

### 3. rr_analysis_summary.csv
Statistical summary for each SL/RR combination.

**Metrics**:
- `total_trades`: Number of trade scenarios
- `wins`: Number of winning trades
- `losses`: Number of losing trades
- `pending`: Trades that didn't hit SL or TP
- `win_rate`: Percentage of winning trades
- `avg_win`: Average profit per winning trade
- `avg_loss`: Average loss per losing trade
- `avg_pnl`: Average P&L per trade
- `total_pnl`: Total P&L for the combination
- `profit_factor`: Gross profit / Gross loss
- `expectancy`: Expected value per trade
- `avg_bars_in_trade`: Average duration in candles
- `avg_mae`: Average maximum adverse excursion
- `avg_mfe`: Average maximum favorable excursion

## Key Results Summary

Based on the analysis of 3,774 trades (2018-2025):

### Best Performing Combinations

1. **SL_100 + RR 4.0**: Win Rate 22.8%, Expectancy $4.43, Total PnL $16,550
2. **SL_100 + RR 3.0**: Win Rate 27.7%, Expectancy $3.74, Total PnL $14,079
3. **SL_100 + RR 3.5**: Win Rate 24.9%, Expectancy $3.67, Total PnL $13,751

### Key Insights

- **SL_100** (full body retracement) consistently shows best results
- Optimal RR ratios are between **3.0 - 4.0**
- Higher win rates with SL_100 offset the wider stops
- SL_25 (tightest) shows negative expectancy for low RR ratios
- Win rates decrease as RR ratio increases (expected behavior)

### Win Rate by SL Placement and RR Ratio

```
SL_Placement   RR_1.0  RR_1.5  RR_2.0  RR_2.5  RR_3.0  RR_3.5  RR_4.0  RR_4.5  RR_5.0
SL_100         48.7%   41.4%   36.1%   31.3%   27.7%   24.9%   22.8%   20.6%   19.2%
SL_75          45.9%   39.7%   35.1%   31.2%   27.9%   24.8%   22.8%   20.7%   19.3%
SL_50          41.5%   36.4%   32.9%   29.8%   27.3%   25.0%   23.2%   21.5%   19.7%
SL_25          27.9%   27.1%   25.7%   24.0%   22.6%   21.5%   20.5%   19.5%   18.6%
```

### Expectancy by SL Placement and RR Ratio

```
SL_Placement   RR_1.0   RR_1.5   RR_2.0   RR_2.5   RR_3.0   RR_3.5   RR_4.0   RR_4.5   RR_5.0
SL_100         $0.06    $1.93    $3.17    $3.62    $3.74    $3.67    $4.43    $3.57    $3.65
SL_75         -$0.68    $0.46    $1.93    $2.77    $3.02    $2.88    $3.47    $3.26    $3.61
SL_50         -$1.15   -$0.32    $0.71    $1.35    $2.00    $2.61    $3.09    $3.39    $3.34
SL_25         -$2.78   -$1.82   -$1.11   -$0.79   -$0.32    $0.13    $0.60    $0.95    $1.34
```

## Usage Tips

1. **Start with SL_100**: Most forgiving and consistently profitable
2. **Target RR 3.0-4.0**: Best balance of win rate and reward
3. **Monitor MAE/MFE**: Helps optimize entry timing
4. **Consider Timeframes**: Different timeframes may perform differently
5. **Backtest Further**: Test selected combinations on new data

## Technical Details

- **Data Caching**: All data files are preloaded for fast processing
- **Processing Time**: ~5 minutes for 3,774 trades (135,864 scenarios)
- **Memory Efficient**: Processes trades sequentially
- **Accurate Simulation**: Checks high/low of each candle to determine SL/TP hits

## Next Steps

1. Review the summary statistics in `rr_analysis_summary.csv`
2. Identify best performing combinations for your risk tolerance
3. Analyze detailed trade outcomes in individual SL files
4. Consider implementing filters based on timeframe, candle type, or market conditions
5. Forward test selected strategies on new data

## Requirements

- Python 3.7+
- pandas >= 1.5.0
- numpy >= 1.21.0

## Author Notes

This analysis system provides comprehensive data for strategy optimization. Remember:
- Past performance doesn't guarantee future results
- Always validate on out-of-sample data
- Consider transaction costs and slippage
- Adjust position sizing based on risk management rules

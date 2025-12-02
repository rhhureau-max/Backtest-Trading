# Risk Management & Profit Analysis Report

## Overview

This document describes the enhanced backtesting strategy that includes comprehensive risk management and profit analysis capabilities.

## Enhancement Features

### 1. Multiple Stop Loss Levels

The strategy now analyzes each trade with four different Stop Loss (SL) placement levels based on the 8:30 AM candle body:

#### For LONG Trades:
- **SL_100**: Stop at 100% retracement (at Open price) - Full body retracement
- **SL_75**: Stop at 75% retracement - Three-quarters back from Close to Open
- **SL_50**: Stop at 50% retracement - Middle of the candle body
- **SL_25**: Stop at 25% retracement - Near the entry (Close price)

**Calculation:**
```
Body = Close - Open
SL_100 = Open (Close - 1.00 × Body)
SL_75 = Close - 0.75 × Body
SL_50 = Close - 0.50 × Body
SL_25 = Close - 0.25 × Body
```

#### For SHORT Trades:
- **SL_100**: Stop at 100% retracement (at Open price) - Full body retracement
- **SL_75**: Stop at 75% retracement - Three-quarters back from Close to Open
- **SL_50**: Stop at 50% retracement - Middle of the candle body
- **SL_25**: Stop at 25% retracement - Near the entry (Close price)

**Calculation:**
```
Body = Open - Close
SL_100 = Open (Close + 1.00 × Body)
SL_75 = Close + 0.75 × Body
SL_50 = Close + 0.50 × Body
SL_25 = Close + 0.25 × Body
```

### 2. Risk-Reward Ratios

For each Stop Loss level, the strategy calculates Take Profit (TP) targets based on nine different Risk-Reward (RR) ratios:

**RR Ratios**: 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0

**Calculation:**
- For LONG: `TP = Entry + (SL_Distance × RR)`
- For SHORT: `TP = Entry - (SL_Distance × RR)`

This creates **36 unique configurations** per trade (4 SL levels × 9 RR ratios).

### 3. Trade Outcome Analysis

For each configuration, the strategy analyzes subsequent candles to determine:

- **Outcome**: WIN, LOSS, or NO_TOUCH
- **P&L**: Profit or loss in price points
- **Candles to Hit**: How many candles it took to hit SL or TP

The analysis looks ahead at up to 100 subsequent candles to track whether the Stop Loss or Take Profit was hit first.

## Output Files

### Enhanced Trade Files
**Files**: `trades_enhanced_1m.csv`, `trades_enhanced_5m.csv`, `trades_enhanced_15m.csv`

Contains all original trade data plus:
- **SL Levels**: SL_100, SL_75, SL_50, SL_25, Body_Size
- **TP Levels**: All 36 TP levels (e.g., SL_100_TP_1.0, SL_75_TP_2.5, etc.)
- **Outcomes**: WIN/LOSS/NO_TOUCH for each SL/RR combination
- **P&L**: Profit/Loss for each combination
- **Candles**: Number of candles to hit target for each combination

### Performance Summary Files
**Files**: `performance_summary_1m.csv`, `performance_summary_5m.csv`, `performance_summary_15m.csv`

For each timeframe, provides aggregated statistics for each SL/RR combination:
- **Total_Trades**: Number of valid trades (excluding NO_TOUCH)
- **Wins**: Number of winning trades
- **Losses**: Number of losing trades
- **No_Touch**: Number of trades that didn't hit SL or TP
- **Win_Rate_%**: Percentage of winning trades
- **Total_PnL**: Cumulative profit/loss
- **Avg_Win**: Average winning trade
- **Avg_Loss**: Average losing trade
- **Profit_Factor**: Ratio of gross profit to gross loss

### Overall Summary Files

#### `performance_summary_all.csv`
Combined performance data from all timeframes and all configurations.

#### `best_configurations_by_pnl.csv`
Top 10 configurations ranked by Total P&L - shows which setups generated the most profit.

#### `best_configurations_by_winrate.csv`
Top 10 configurations ranked by Win Rate - shows which setups have the highest success rate.

#### `best_configurations_by_profit_factor.csv`
Top 10 configurations ranked by Profit Factor - shows which setups have the best risk-adjusted returns.

### Basic Summary File
**File**: `trades_summary.csv`

Basic statistics showing total trades, long trades, and short trades for each timeframe.

## Usage

### Running the Enhanced Analysis

```bash
python3 backtest_strategy.py
```

The script will:
1. Load historical data for all timeframes (1m, 5m, 15m) from 2018-2025
2. Identify valid trade entries at 8:30 AM
3. Calculate all SL and TP levels for each trade
4. Analyze subsequent price action to determine outcomes
5. Generate comprehensive CSV reports
6. Display top-performing configurations

### Processing Time

The enhanced analysis processes:
- All trades from 2018-2025 across 3 timeframes
- 36 SL/RR combinations per trade
- Potentially 100+ subsequent candles per trade

**Estimated Processing Time**: 2-5 minutes (depending on system)

## Key Metrics Explained

### Win Rate
`Win Rate = (Wins / Total_Trades) × 100`

Higher win rate indicates more consistent success, but doesn't account for the size of wins vs losses.

### Profit Factor
`Profit Factor = (Avg_Win × Wins) / (|Avg_Loss| × Losses)`

A profit factor > 1.0 means the strategy is profitable. Higher values indicate better risk-adjusted performance.

### Total P&L
Sum of all profits and losses. This shows the absolute profitability of a configuration.

## Strategy Insights

### Stop Loss Considerations

- **SL_25**: Tightest stop, lowest risk per trade, but higher chance of being stopped out
- **SL_50**: Moderate risk, balanced approach
- **SL_75**: Wider stop, gives trades more room to breathe
- **SL_100**: Widest stop, allows full retracement, highest risk per trade

### Risk-Reward Considerations

- **Lower RR (1.0-2.0)**: Easier to reach targets, potentially higher win rates
- **Medium RR (2.5-3.5)**: Balanced risk-reward
- **Higher RR (4.0-5.0)**: Larger profits when successful, but targets may be harder to reach

### Optimal Configuration

The optimal configuration depends on your trading goals:

- **For consistent returns**: Look at configurations with high win rates and positive profit factors
- **For maximum profit**: Look at configurations with highest Total P&L
- **For risk-adjusted returns**: Look at configurations with highest profit factors

## Data Validation

The analysis uses actual historical price data to determine:
- Whether stops were hit based on candle lows (for LONG) or highs (for SHORT)
- Whether targets were reached based on candle highs (for LONG) or lows (for SHORT)
- The exact sequence of price action following each trade entry

This provides realistic backtesting results based on actual market behavior.

## Limitations

1. **Slippage**: The analysis assumes exact fills at SL and TP levels
2. **Commissions**: Trading costs are not included in P&L calculations
3. **Liquidity**: Assumes orders can be filled at desired prices
4. **Look-ahead**: Limited to 100 candles after entry; some trades may show NO_TOUCH if they didn't reach SL or TP within this window

## Next Steps

1. Review the `best_configurations_*.csv` files to identify promising setups
2. Analyze the `performance_summary_all.csv` to compare all configurations
3. Examine specific trade outcomes in the `trades_enhanced_*.csv` files
4. Consider forward testing the top-performing configurations
5. Adjust SL levels and RR ratios based on findings
6. Add additional filters or entry criteria to improve win rates

## Configuration Customization

You can modify the analysis parameters in `backtest_strategy.py`:

```python
# Stop Loss Levels (% of candle body)
SL_LEVELS = [100, 75, 50, 25]

# Risk-Reward Ratios
RR_RATIOS = [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]

# Analysis lookback (number of candles)
max_lookback = 100  # in analyze_trade_outcome function
```

## Support

For questions or issues with the enhanced analysis:
1. Check that all data files are present and properly formatted
2. Ensure pandas and numpy are installed: `pip install -r requirements.txt`
3. Review console output for any error messages during processing

---

**Version**: 2.0 (Enhanced with Risk Management)  
**Last Updated**: December 2025  
**Compatibility**: Python 3.7+

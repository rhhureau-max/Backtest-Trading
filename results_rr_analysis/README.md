# Risk/Reward Ratio Analysis Results

## Overview

This directory contains comprehensive backtest results for the FVG trading strategy tested across **8 different risk/reward ratios** (1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0) and **3 timeframes** (1m, 5m, 15m).

**Total Analysis:**
- **24 configurations** tested (3 timeframes × 8 R/R ratios)
- **18,632 total trades** executed
- **7 years** of historical data (2018-2024)
- **2.4M+ candles** analyzed

## Quick Start

### View Results

1. **Comprehensive Report:** Open `rr_comparison_report.md` for detailed analysis
2. **CSV Summary:** Open `rr_comparison_summary.csv` in Excel/Sheets for raw data
3. **Visualizations:**
   - `rr_analysis_visualization.png` - 6 charts showing all metrics vs R/R ratio
   - `best_configurations.png` - Bar chart comparing best R/R for each timeframe

### Best Configuration

**15-Minute Timeframe with R/R 5.0:**
- Total Return: **89.20%** over 7 years
- Sharpe Ratio: **1.92**
- Max Drawdown: **-6.50%**
- Win Rate: **33.04%**
- Profit Factor: **1.43**
- Total Trades: **793**

## Files in This Directory

### Reports
- `rr_comparison_report.md` - Comprehensive markdown report with all results
- `rr_comparison_summary.csv` - Summary table with all metrics
- `README.md` - This file

### Visualizations
- `rr_analysis_visualization.png` - 6-panel chart showing:
  - Total Return vs R/R Ratio
  - Win Rate vs R/R Ratio
  - Sharpe Ratio vs R/R Ratio
  - Max Drawdown vs R/R Ratio
  - Profit Factor vs R/R Ratio
  - Total Return Heatmap
- `best_configurations.png` - Best R/R configuration for each timeframe

### Trade Data (24 CSV files)
- `trades_1m_rr1.5.csv` through `trades_1m_rr5.0.csv` (8 files)
- `trades_5m_rr1.5.csv` through `trades_5m_rr5.0.csv` (8 files)
- `trades_15m_rr1.5.csv` through `trades_15m_rr5.0.csv` (8 files)

Each trade CSV contains:
- Entry/exit times and prices
- Direction (Long/Short)
- Stop loss and take profit levels
- Exit reason (TP/SL/EOD)
- P&L and return percentage
- FVG information

## Key Findings

### 1. Higher R/R Ratios Perform Better
- **R/R 5.0** provides the best returns across all timeframes
- Returns increase from R/R 1.5 to R/R 5.0 in most cases
- Risk-adjusted returns (Sharpe ratio) also improve with higher R/R

### 2. Timeframe Performance
- **15-minute:** Best overall (52-89% returns)
- **5-minute:** Moderate (7-47% returns)
- **1-minute:** Lower but consistent (3-28% returns)

### 3. Win Rate vs Return Trade-off
- Lower R/R ratios (1.5-2.0): Higher win rates (40-45%) but lower returns
- Higher R/R ratios (4.0-5.0): Lower win rates (22-33%) but higher returns
- Sweet spot depends on trader's risk tolerance

### 4. Drawdown Management
- All configurations maintain reasonable drawdowns (< 15%)
- Higher R/R ratios often show better drawdown control
- 15m timeframe shows most stable equity curves

## Recommendations by Trader Profile

### Conservative Trader
- **Timeframe:** 15m
- **R/R Ratio:** 1.5 or 2.0
- **Expected:** 52-56% return, 39-45% win rate
- **Why:** Higher win rate, more predictable

### Balanced Trader
- **Timeframe:** 15m
- **R/R Ratio:** 3.0 or 3.5
- **Expected:** 82-87% return, 34-36% win rate
- **Why:** Best risk-adjusted returns (Sharpe 1.84-1.89)

### Aggressive Trader
- **Timeframe:** 15m
- **R/R Ratio:** 4.5 or 5.0
- **Expected:** 86-89% return, 33% win rate
- **Why:** Maximum total returns, excellent Sharpe ratio

## How to Use These Results

1. **Choose your timeframe** based on trading style and availability
2. **Select R/R ratio** based on risk tolerance and profit goals
3. **Review the specific trade CSV** for your chosen configuration
4. **Analyze the metrics** in the summary CSV or report
5. **Consider market conditions** - results are based on 2018-2024 data

## Running Your Own Analysis

To reproduce or extend this analysis:

```bash
# Run complete analysis (takes ~10 minutes)
python main_rr_analysis.py

# Or run optimized version for specific timeframe
python complete_rr_analysis.py

# Generate visualizations from existing CSVs
python create_rr_visualizations.py
```

## Important Notes

⚠️ **Past Performance Disclaimer:**
- These results are based on historical data
- Past performance does not guarantee future results
- Always backtest on out-of-sample data before live trading
- Consider transaction costs and slippage in live trading

💡 **Data Quality:**
- All data from 2018-2024 market conditions
- Results may vary in different market regimes
- Consider testing on most recent data for relevance

🎯 **Strategy Notes:**
- FVG detection at 8:30 AM only
- Entry delays: 1m→8:31, 5m→8:35, 15m→8:45
- Stop loss at FVG midpoint
- Take profit at configured R/R ratio
- All positions closed at end of day

## Questions?

For questions about methodology, calculations, or implementation details, refer to:
- Main documentation: `../README.md`
- Usage guide: `../USAGE_GUIDE.md`
- Source code: `../main_rr_analysis.py`

---

*Generated: 2025-11-24*
*Analysis Period: 2018-01-01 to 2024-12-31*
*Total Trades: 18,632*

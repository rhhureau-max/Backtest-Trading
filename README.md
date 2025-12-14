# FVG Trading Strategy Backtest System

A comprehensive backtesting system for Fair Value Gap (FVG) trading strategy across multiple timeframes.

## Overview

This project implements a complete backtesting framework for FVG (Fair Value Gap) trading strategy with:
- FVG detection at 8:30 AM daily candles
- Multiple timeframe analysis (1-minute, 5-minute, 15-minute)
- 7 years of historical data (2018-2024)
- Comprehensive performance metrics and visualizations

## Strategy Description

### FVG Detection
A Fair Value Gap (FVG) is identified when there's a price gap between consecutive candles:
- **Bullish FVG**: `candle[i-1].high < candle[i+1].low`
- **Bearish FVG**: `candle[i-1].low > candle[i+1].high`

### Entry Rules
- **1-minute timeframe**: Enter at close of 8:31 candle (1 minute after FVG)
- **5-minute timeframe**: Enter at close of 8:35 candle (5 minutes after FVG)
- **15-minute timeframe**: Enter at close of 8:45 candle (15 minutes after FVG)

### Exit Rules
- **Stop Loss (SL)**: Placed at the middle of the FVG gap
- **Take Profit (TP)**: Set at 2:1 risk/reward ratio
- **End of Day (EOD)**: All positions closed at end of trading day

## Project Structure

```
.
├── main.py                    # Main execution script
├── data_loader.py             # Data loading and preprocessing
├── fvg_detector.py            # FVG detection algorithm
├── backtest_engine.py         # Backtesting engine
├── performance_metrics.py     # Performance calculations
├── visualization.py           # Chart generation
├── report_generator.py        # Report generation
├── requirements.txt           # Python dependencies
└── results/                   # Output directory (generated)
    ├── backtest_report.md     # Markdown report
    ├── backtest_report.html   # HTML report
    ├── trades_*.csv           # Trade data
    └── *.png                  # Visualization charts
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Backtest-Trading
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

Run the complete backtest:
```bash
python main.py
```

This will:
1. Load data for all timeframes (1m, 5m, 15m) from 2018-2024
2. Detect FVG patterns at 8:30 AM
3. Execute backtests with proper entry/exit logic
4. Calculate comprehensive performance metrics
5. Generate visualizations
6. Create detailed reports

## Data Format

The system expects CSV files with the following format:
- Filename: `YYYY {timeframe}.csv` (e.g., "2018 15m.csv")
- For 1-minute data: ZIP files `YYYY 1m.csv.zip`
- CSV structure: `Date;Time;Open;High;Low;Close;Volume`

## Output

The system generates:

### Reports
- **backtest_report.md**: Comprehensive Markdown report
- **backtest_report.html**: HTML version of the report

### Visualizations
- **equity_curve_*.png**: Equity curve and cumulative P&L
- **drawdown_*.png**: Drawdown analysis
- **trade_distribution_*.png**: Win/loss distribution analysis
- **performance_heatmap_*.png**: Monthly performance heatmap

### Data Files
- **trades_*.csv**: Detailed trade data for each timeframe

## Performance Metrics

The system calculates:
- Total trades, win rate, profit factor
- Total return, average return per trade
- Sharpe ratio, maximum drawdown
- Average win/loss, risk/reward ratio
- Consecutive wins/losses
- Exit reason analysis
- Long/short performance
- Monthly and yearly breakdowns

## Requirements

- Python 3.7+
- pandas >= 1.5.0
- numpy >= 1.21.0
- matplotlib >= 3.5.0
- seaborn >= 0.12.0

## Features

✅ Multi-timeframe backtesting (1m, 5m, 15m)  
✅ FVG detection algorithm  
✅ Risk management (SL/TP)  
✅ Comprehensive performance metrics  
✅ Professional visualizations  
✅ Detailed HTML/Markdown reports  
✅ 7+ years of historical analysis  
✅ Monthly and yearly performance breakdowns  

## Notes

- The backtest assumes no slippage or transaction costs
- Results are based on historical data and may not guarantee future performance
- The system handles missing data and edge cases
- All positions are closed at end of day (no overnight holds)

## License

MIT License
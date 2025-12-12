# Backtest-Trading

A comprehensive backtesting system for Smart Money Concepts (SMC) trading strategy applied to Nasdaq, using historical data from 2018 to 2025.

## Overview

This system implements a backtesting framework for a trading strategy based on Smart Money Concepts:
- **Accumulation Phase Detection**: Identifies price consolidation zones
- **Liquidity Sweep Detection**: Detects false breakouts beyond key levels
- **Fair Value Gap (FVG) Detection**: Identifies gaps in price structure
- **Entry Confirmation**: Generates signals when FVGs are broken with confirmation

## Installation

1. Clone the repository:
```bash
git clone https://github.com/rhhureau-max/Backtest-Trading.git
cd Backtest-Trading
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Backtest

Execute the main backtest script:
```bash
python src/smc_backtest.py
```

This will:
- Load all historical data (2018-2025)
- Detect entry signals based on SMC strategy
- Process trades with defined risk management
- Generate a comprehensive report in `analysis/STRATEGY_REPORT.md`
- Save all trades to `analysis/trades_results.csv`

### Configuration

Strategy parameters can be adjusted in `config/settings.yaml`:
- Accumulation detection parameters
- Liquidity sweep sensitivity
- FVG detection thresholds
- Risk/Reward ratios
- Trading hours filter

## Project Structure

```
Backtest-Trading/
├── src/
│   ├── __init__.py
│   ├── smc_backtest.py      # Main backtest script
│   ├── detectors.py         # Pattern detection functions
│   └── trade_manager.py     # Trade management module
├── config/
│   └── settings.yaml        # Strategy configuration
├── analysis/
│   ├── STRATEGY_REPORT.md   # Generated performance report
│   └── trades_results.csv   # All trades data
├── requirements.txt         # Python dependencies
├── README.md
└── [YYYY] [timeframe].csv   # Historical data files
```

## Strategy Description

### Timeframes
- **15 minutes**: Trend and liquidity sweep identification
- **5 minutes**: FVG detection and entry confirmation

### Entry Conditions
1. Accumulation phase (range) on 15m
2. Liquidity sweep detected on 15m/5m
3. FVG formation on 5m after sweep
4. **BUY**: Price closes above bearish FVG
5. **SELL**: Price closes below bullish FVG

### Risk Management
- **Stop-Loss**: Below/above confirmation candle or FVG
- **Take Profits**: RR 1:1, 1:1.5, 1:2

## Data Format

Historical data files use semicolon (`;`) separator with columns:
```
Date;Time;Open;High;Low;Close;Volume
01/01/2018;17:00:00;7503.739664;7511.940473;7499.63926;7511.3547;1451
```

## Results

See `analysis/STRATEGY_REPORT.md` for detailed performance analysis including:
- Global statistics (win rate, profit factor)
- Year-by-year breakdown
- Long vs Short performance
- TP/SL distribution

## License

This project is for educational and research purposes only. Trading involves significant risk of loss.
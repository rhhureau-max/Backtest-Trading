# Backtest-Trading

This repository contains NQ futures market data and backtesting scripts for quantitative trading strategies.

## Data Files

The repository includes historical NQ futures data in various timeframes:
- 5-minute bars (YYYY 5m.csv files from 2018-2025)
- 15-minute bars
- 1-hour bars
- 4-hour bars
- Daily bars

### Data Format

CSV files are semicolon-separated with the following structure:
```
Column1;Column2;Column3;Column4;Column5;Column6;Column7
01/01/2018;17:00:00;7503.739664;7511.940473;7499.63926;7511.3547;1451
```

Columns: `Date;Time;Open;High;Low;Close;Volume`

## FVG Inversion Backtesting Script

### Overview

`backtest_fvg_inversion.py` implements a Fair Value Gap (FVG) inversion strategy with the following logic:

1. **Session-Based Trading**: Operates between 02:00-06:00 (data local time)
2. **FVG Detection**: Identifies the first Fair Value Gap of each session
   - Bullish FVG: High[i-2] < Low[i] → Gap zone is [High[i-2], Low[i]]
   - Bearish FVG: Low[i-2] > High[i] → Gap zone is [High[i], Low[i-2]]
3. **Inversion Signals**:
   - Long: Bearish FVG exists, candle closes above the gap top
   - Short: Bullish FVG exists, candle closes below the gap bottom
4. **Risk Management**:
   - Stop Loss: 5-candle swing high/low
   - Take Profit: 1:1 Risk/Reward ratio
5. **Trade Constraints**: Maximum one trade per day

### Requirements

Install the required Python packages:

```bash
pip install pandas numpy matplotlib
```

### Usage

Run the backtest:

```bash
python backtest_fvg_inversion.py
```

### Output

The script generates:
1. **Console metrics**: Win rate, total trades, net profit, max drawdown
2. **equity_curve.png**: Visual representation of cumulative returns
3. **trades.csv**: Detailed trade log with entry/exit prices, P&L, and timestamps

### Sample Results

Based on 2018-2025 data (554,518 5-minute candles):
- Total Trades: 3,355
- Win Rate: ~49%
- Net Profit: $312.89
- Max Drawdown: $-1,682.63
- Profit Factor: 1.01

## License

Data and scripts are provided for educational and research purposes.
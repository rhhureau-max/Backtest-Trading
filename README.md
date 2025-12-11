# Backtest-Trading

## ICT Fair Value Gap (FVG) Reversal Strategy

This repository contains a comprehensive backtesting system for an ICT (Inner Circle Trader) Fair Value Gap reversal strategy with hierarchical setup classification based on confluence factors.

### Features

- **Time-constrained Trading**: Entry window 01:00-04:00, force close at 06:00
- **Hierarchical Setup Classification**:
  - **Setup C**: FVG + MSS (Low Probability)
  - **Setup B**: Setup C + Liquidity Sweep (Standard)
  - **Setup A**: Setup B + Displacement + OTE (High Probability)  
  - **Setup A+**: Setup A + Breaker Block + London Macro (Unicorn)
- **Advanced Money Management**: 1% risk per trade, split take profits (2R and 2.5 SD)
- **Multi-timeframe Analysis**: Uses 15m for structure, 5m for entry precision

### Installation

```bash
pip install -r requirements.txt
```

### Usage

```bash
python fvg_reversal_backtest.py
```

### Documentation

See [README_FVG_REVERSAL.md](README_FVG_REVERSAL.md) for detailed documentation on:
- Strategy rules and setup classifications
- Technical indicators and confluences
- Money management and risk parameters
- Output files and performance metrics
- Configuration and customization

### Data Format

The backtest expects CSV files with semicolon-separated values:
```
Date;Time;Open;High;Low;Close;Volume
01/01/2024;17:00:00;18244.57923;18248.331274;18238.951165;18241.631196;1308
```

Files should be named: `YYYY 15m.csv`, `YYYY 5m.csv`, etc.

### Results

The backtest generates two output files:
- `fvg_reversal_trades.csv`: Detailed trade log with entry/exit data
- `fvg_reversal_results.csv`: Summary metrics by setup class

### Sample Results (2024)

```
Setup Class  Num Trades  Winrate (%)  Profit Factor  Max Drawdown ($)  Net Profit ($)
          C          18        83.33          15.74            208.86        12837.10
          B           3       100.00           0.00              0.00         1247.14
          A           0         0.00           0.00              0.00            0.00
         A+           0         0.00           0.00              0.00            0.00
```

### License

This is a research and educational tool. Use at your own risk.
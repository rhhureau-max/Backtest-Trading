# FVG + Liquidity Sweep Backtest Strategy

A Python-based backtesting framework for a Fair Value Gap (FVG) and Liquidity Sweep trading strategy.

## Overview

This strategy combines two powerful concepts from Smart Money trading:
1. **Fair Value Gaps (FVG)** - Imbalances in price action that create gaps in the market
2. **Liquidity Sweeps** - Price movements that take out old highs/lows before reversing

## Strategy Logic

### Trading Sessions (UTC)
- **Session 1**: 02:00 to 05:00
- **Session 2**: 08:30 to 11:00

### Entry Conditions

1. **HTF Context (H1/M15)**
   - Price must have retraced into a Fair Value Gap detected on H1 or M15 timeframe
   - OR a liquidity sweep must have occurred on an old high/low (detected using fractals)

2. **LTF Entry (M5)**
   - Once HTF context is established, monitor the 5-minute chart
   - A new FVG must form on M5 (showing displacement)
   - Price must retrace to fill this M5 FVG
   - A reversal candle must form (confirming rejection)

3. **Trade Execution**
   - Entry: At the close of the reversal candle
   - Stop Loss: Below the last low (for buys) or above the last high (for sells) created during FVG rejection
   - Take Profit: 1:2 Risk/Reward ratio

## Installation

```bash
# Navigate to backtest directory
cd backtest

# Install dependencies
pip install -r requirements.txt
```

## Usage

Run the backtest from the repository root:

```bash
python backtest/main.py
```

Or from the backtest directory:

```bash
cd backtest
python main.py
```

## Output

The backtest generates `backtest_results.md` containing:
- Total number of trades
- Win Rate percentage
- Profit Factor
- Statistics by year
- Statistics by session
- Maximum drawdown
- Average realized R:R

## Project Structure

```
backtest/
├── main.py              # Main entry point
├── config.py            # Configuration settings
├── data_loader.py       # CSV data loading and preparation
├── fvg_detector.py      # Fair Value Gap detection
├── liquidity_detector.py # Liquidity sweep and fractal detection
├── strategy.py          # Main strategy logic
├── trade_manager.py     # Trade execution and management
├── metrics.py           # Performance metrics calculation
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

## Data Format

The strategy expects OHLC data files with:
- Format: Semicolon-separated CSV
- Columns: Date;Time;Open;High;Low;Close;Volume
- Date format: DD/MM/YYYY
- Time format: HH:MM:SS

Supported timeframes:
- `YYYY 1H.csv` - 1 hour data (HTF)
- `YYYY 15m.csv` - 15 minute data (HTF)
- `YYYY 5m.csv` - 5 minute data (LTF - entry timeframe)

## Configuration

Key settings in `config.py`:
- `risk_reward_ratio`: Take profit R:R (default: 2.0)
- `sessions`: Trading session times (UTC)
- `fvg_min_gap_pct`: Minimum FVG size as percentage
- `fractal_lookback`: Lookback period for fractal detection
- `max_fvg_fill_candles`: Maximum candles to wait for FVG fill

## Technical Details

### Fair Value Gap Detection
An FVG is detected when:
- **Bullish FVG**: Low of candle N > High of candle N-2 (gap below current candle)
- **Bearish FVG**: High of candle N < Low of candle N-2 (gap above current candle)

### Fractal Detection
Uses Williams fractal methodology:
- **Fractal High**: A candle with 2 lower highs on each side
- **Fractal Low**: A candle with 2 higher lows on each side

### Trade Management
- No overlapping trades (one trade at a time)
- Maximum one entry per session per day
- Trades are closed at SL or TP hit

## Performance Notes

- All profit/loss values are expressed in R-multiples (risk units)
- This allows comparison of results regardless of position sizing
- A profit of 2R means you made 2x your initial risk

## License

This project is for educational and research purposes.

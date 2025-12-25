# SMC/ICT London Killzone Backtest System

## Overview

This is a complete backtesting system for two institutional trading strategies (SMC/ICT) focused on the London Killzone (02:00-05:00 EST) for Nasdaq-100 futures (NQ).

**Period Analyzed:** 2018-2025  
**Instrument:** NQ Futures  
**Timeframes:** 1m, 5m, 15m, 1H  
**Total Trading Days:** 2,449

## Strategies Implemented

### Strategy 1: Liquidity Raid (Reversal/Turtle Soup)
- **Concept:** Judas Swing - price raids Asian session highs/lows then reverses
- **Setup:**
  1. Identify daily bias from H1 market structure
  2. Define Asian Range (19:00-00:00 EST)
  3. Detect liquidity raid during London Killzone
  4. Validate rejection (close inside range OR wick >40%)
  5. Entry options:
     - **Aggressive:** Entry at rejection candle close (M5)
     - **Conservative:** Wait for MSS + FVG confirmation
- **Risk Management:**
  - Stop Loss: Beyond swing wick (+5 pts buffer)
  - TP1: Opposite Asian boundary
  - TP2: Fibonacci 2.0 extension

### Strategy 2: Trend Continuation (Breakout & Momentum)
- **Concept:** Strong breakout with momentum confirmation
- **Setup:**
  1. Identify very strong daily bias (confirmed BOS on H1)
  2. Detect breakout of Asian Range with momentum (>0.5% move)
  3. NEVER enter on initial breakout
  4. Wait for Breaker Block retest or FVG continuation
- **Risk Management:**
  - Stop Loss: Below Breaker Block or M15 swing low
  - TP: 2x breakout range extension

## Installation

### Requirements
- Python 3.8+
- pandas >= 2.0.0
- numpy >= 1.24.0

### Setup
```bash
# Clone the repository
cd Backtest-Trading

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Run Complete Backtest
```bash
python run_backtest.py
```

This will:
1. Load all NQ data (5m, 15m, 1H) from 2018-2025
2. Analyze 2,449 trading days for signals
3. Execute all trades and track results
4. Generate comprehensive reports

### Output Files

The system generates 4 output files:

1. **backtest_results.csv** - Detailed trade log with all entries/exits
2. **backtest_results.json** - Same data in JSON format
3. **backtest_statistics.json** - Performance metrics summary
4. **backtest_analysis.md** - Comprehensive analysis report

## Project Structure

```
Backtest-Trading/
├── run_backtest.py              # Main execution script
├── data_loader.py               # Data loading and preprocessing
├── market_structure.py          # SMC/ICT structure detection
├── strategy1_liquidity_raid.py  # Strategy 1 implementation
├── strategy2_trend_continuation.py # Strategy 2 implementation
├── backtest_engine.py           # Trade execution and tracking
├── requirements.txt             # Python dependencies
└── [Data Files]                 # CSV files with OHLC data
    ├── 2018 5m.csv
    ├── 2018 15m.csv
    ├── 2018 1H.csv
    └── ... (all years 2018-2025)
```

## Key Features

### Market Structure Detection
- **Asian Range:** High/Low between 19:00-00:00 EST
- **London Killzone:** 02:00-05:00 EST
- **Daily Bias:** Higher Highs/Higher Lows (Bullish) or Lower Highs/Lower Lows (Bearish)
- **FVG (Fair Value Gaps):** Price inefficiencies for entry
- **MSS (Market Structure Shift):** Break of recent swing highs/lows
- **Order Blocks:** Last opposite candle before strong move
- **Breaker Blocks:** Failed support/resistance zones

### Trade Execution
- Tracks all trades from entry to exit
- Monitors TP1, TP2, and Stop Loss levels
- 4-hour maximum trade duration
- Calculates R:R ratios and P&L
- Adds market context (COVID, Bull/Bear markets)

### Analysis Features
- Win rate per strategy
- Performance across market regimes
- Volatility impact on stop loss width
- Entry precision comparison (Aggressive vs Conservative)
- Detailed exit analysis (TP1/TP2/SL breakdown)

## Results Summary

Based on 2018-2025 backtest:

### Overall Performance
- **Total Signals:** 737
- **Valid Trades:** 709
- **Win Rate:** 32.58%
- **Average R:R:** 0.84
- **Total P&L:** -2,481.25 points

### Strategy Comparison

| Strategy | Trades | Win Rate | Avg R:R | Total P&L |
|----------|--------|----------|---------|-----------|
| S1 Aggressive | 674 | 32.34% | 0.86 | -2,159.50 pts |
| S1 Conservative | 35 | 37.14% | 0.39 | -321.75 pts |

### Key Insights

1. **Conservative Entry Superiority:** Conservative entries (MSS + FVG) showed 4.8% better win rate
2. **Volatility Impact:** Stop loss width increased ~9% during high volatility (2020/2022)
3. **Market Regime Sensitivity:** Performance varies significantly across different market contexts
4. **Best Period:** Bull Market 2021 (38.27% win rate)
5. **Challenging Period:** Bear Market 2022 (27.84% win rate)

## CSV Data Format

The system expects semicolon-separated CSV files with the following format:

```
Column1;Column2;Column3;Column4;Column5;Column6;Column7
01/01/2024;17:00:00;18244.57923;18248.331274;18238.951165;18241.631196;1308
```

Columns: Date;Time;Open;High;Low;Close;Volume

**Important:** All times must be in EST timezone (no conversion needed).

## Customization

### Modify Strategy Parameters

Edit the strategy files to adjust parameters:

**strategy1_liquidity_raid.py:**
```python
self.min_wick_ratio = 0.40  # Minimum 40% wick for validation
```

**strategy2_trend_continuation.py:**
```python
self.min_breakout_strength = 0.5  # Minimum 0.5% move for breakout
```

**market_structure.py:**
```python
self.asian_start = time(19, 0)   # Asian session start
self.london_start = time(2, 0)   # London Killzone start
```

### Modify Risk Management

Edit stop loss buffers and TP calculations in strategy files:
```python
stop_loss = judas_swing['swing_high'] + 5  # 5 points buffer
tp1 = asian_range['high']  # Opposite Asian boundary
tp2 = tp1 - range * 2.0    # Fibonacci 2.0 extension
```

## Technical Details

### Asian Range Detection
- Session: 19:00 EST (previous day) to 00:00 EST (current day)
- Captures high/low of 5-hour window
- Used to identify liquidity levels

### Daily Bias Algorithm
- Analyzes last 24 H1 bars
- Counts Higher Highs, Higher Lows, Lower Highs, Lower Lows
- Requires 1.5x score difference for directional bias

### FVG Detection
- Bullish FVG: Gap between candle[i-1].high and candle[i+1].low
- Bearish FVG: Gap between candle[i-1].low and candle[i+1].high
- Used for precise entry points

### Trade Timeout
- Maximum 4 hours (48 x 5m bars) per trade
- Prevents indefinite position holding
- Closes at current price if no target hit

## Performance Optimization

The system processes:
- 554,510 x 5-minute bars
- 184,877 x 15-minute bars  
- 41,027 x 1-hour bars
- 2,449 trading days

Typical runtime: 2-3 minutes on modern hardware

## Limitations & Considerations

1. **Slippage Not Modeled:** Assumes fills at exact prices
2. **Commissions Not Included:** P&L is gross, not net
3. **Spread Not Modeled:** Entry/exit at mid prices
4. **No Partial Fills:** Assumes full position filled instantly
5. **Backtest Bias:** Past performance doesn't guarantee future results
6. **Single Instrument:** Only NQ tested (not ES, YM, RTY)

## Future Enhancements

Potential improvements:
- [ ] Add ES correlation filter for Strategy 2
- [ ] Implement partial position management (scale out)
- [ ] Add session volume filters
- [ ] Include news event filters
- [ ] Add VIX-based dynamic stop loss
- [ ] Implement walk-forward optimization
- [ ] Add real-time signal detection

## Contributing

This is a research and educational project. Contributions welcome:
- Strategy improvements
- Additional filters
- Performance optimizations
- Documentation enhancements

## Disclaimer

⚠️ **IMPORTANT:** This backtesting system is for educational and research purposes only. 

- Past performance does not guarantee future results
- Trading futures involves substantial risk of loss
- Do not trade with money you cannot afford to lose
- Always paper trade before risking real capital
- Consult with a financial advisor before trading

## License

This project is provided as-is for educational purposes.

## Author

Senior Quantitative Analyst specializing in institutional market structures (SMC/ICT)

---

**Last Updated:** December 2025  
**Version:** 1.0.0  
**Data Coverage:** 2018-2025

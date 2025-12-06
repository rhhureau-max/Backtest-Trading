# London Manipulation Strategy Backtest - User Guide

## Overview

This repository contains a complete backtest implementation for the "London Manipulation" strategy on NQ (Nasdaq 100 futures) using 5-minute data from January 2018 to present.

## Strategy Description

### Session Definitions (EST/New York Time)
1. **Asian Session (Reference):** 18:00 (previous day) to 02:00 - identify the Asian Low
2. **London Open (Trading Window):** 02:00 to 05:00

### Entry Logic (Sequential Detection Required)

The strategy identifies a specific sequence of price action:

1. **Condition A - Liquidity Sweep:** 
   - During London Open (02:00-05:00 EST), price descends and breaks below the Asian Low
   - This is a "liquidity sweep" that hunts stop losses

2. **Condition B - Bearish Fair Value Gap (FVG):**
   - During the sweep movement, a M5 candle creates a Bearish FVG
   - Bearish FVG criteria: `High[i] < Low[i-2]`
   - This creates an inefficiency in price

3. **Condition C - Inversion Trigger:**
   - Price reverses and a M5 candle closes strictly ABOVE the high boundary of the Bearish FVG
   - This transforms the Bearish FVG into an "Inversion FVG"
   - Signals institutional buying after the liquidity grab

4. **Execution:**
   - Enter LONG at the OPEN of the M5 candle immediately following the confirmation candle
   - Entry is systematic and automated

### Risk Management

- **Stop Loss (SL):** Placed 1 tick (0.25 points for NQ) below the absolute swing low created during the manipulation movement
- **Take Profit (TP):** Set for 1:1 Risk/Reward ratio
  - Distance from Entry to TP = Distance from Entry to SL
- **No Breakeven:** Trade runs to either TP or SL without adjustment

## File Structure

```
├── 2018 5m.csv through 2025 5m.csv  (Data files)
├── london_manipulation_backtest.py  (Main backtest script)
├── london_manipulation_trades.csv   (Generated: Trade log)
├── london_manipulation_report.md    (Generated: Summary report)
└── LONDON_MANIPULATION_README.md    (This file)
```

## Requirements

### Python Packages
```bash
pip install pandas numpy tabulate
```

### Data Files
The script requires NQ 5-minute data files in the following format:
- Filename pattern: `YYYY 5m.csv` (e.g., "2018 5m.csv")
- CSV format: semicolon (`;`) separator
- Columns: `Date;Time;Open;High;Low;Close;Volume`
- Date format: `DD/MM/YYYY`
- Time format: `HH:MM:SS`
- Example row: `01/01/2018;17:00:00;7503.739664;7511.940473;7499.63926;7511.3547;1451`

## Usage

### Running the Backtest

```bash
python london_manipulation_backtest.py
```

The script will:
1. Load all 5-minute data files from 2018-2025
2. Process each trading day sequentially
3. Detect setups matching the strategy criteria
4. Execute virtual trades with proper risk management
5. Calculate comprehensive statistics
6. Export results to CSV and Markdown

### Expected Output

The script generates two files:

#### 1. `london_manipulation_trades.csv`
Detailed log of every trade with columns:
- `trade_id`: Sequential trade number
- `date`: Trading date
- `asian_low`: The identified Asian session low
- `sweep_low`: Lowest point during the sweep
- `fvg_high`: Upper boundary of the Bearish FVG
- `fvg_low`: Lower boundary of the Bearish FVG
- `entry_time`: Exact timestamp of entry
- `entry_price`: Entry price
- `stop_loss`: Stop loss price
- `take_profit`: Take profit price
- `exit_time`: Exact timestamp of exit
- `exit_price`: Exit price
- `exit_type`: Reason for exit (TP/SL/TIMEOUT/EOD)
- `pnl`: Profit/Loss in points
- `pnl_percent`: P&L as percentage
- `risk`: Risk taken (entry - stop loss)
- `reward`: Reward targeted (take profit - entry)
- `winner`: Boolean indicating if trade was profitable

#### 2. `london_manipulation_report.md`
Comprehensive summary report including:
- Overall performance metrics
- Win rate and profit factor
- Average win/loss
- Maximum drawdown
- Yearly performance breakdown
- Monthly performance breakdown
- Strategy notes and implementation details

### Console Output

During execution, the script displays:
- Data loading progress
- Number of trading days processed
- Number of setups found
- Detailed performance statistics
- Yearly and monthly breakdowns

## Results Summary (2018-2025)

Based on the complete backtest:

| Metric | Value |
|--------|-------|
| **Total Trades** | 414 |
| **Win Rate** | 53.14% |
| **Total P&L** | 183.55 points |
| **Profit Factor** | 1.02 |
| **Average Win** | 41.56 points |
| **Average Loss** | -46.18 points |
| **Max Drawdown** | -1352.63 points |
| **Expectancy** | 0.44 points/trade |

### Yearly Performance

| Year | P&L (points) | Trades | Win Rate |
|------|-------------|--------|----------|
| 2018 | 168.01 | 51 | 50.98% |
| 2019 | -242.36 | 37 | 43.24% |
| 2020 | -92.97 | 47 | 51.06% |
| 2021 | 123.17 | 51 | 56.86% |
| 2022 | -693.79 | 61 | 42.62% |
| 2023 | -47.04 | 69 | 55.07% |
| 2024 | 468.94 | 60 | 65.00% |
| 2025 | 499.58 | 38 | 57.89% |

## Implementation Details

### Technical Specifications

1. **Timezone Handling:** All times treated as EST (New York timezone)
2. **FVG Detection:** Implemented as `High[i] < Low[i-2]` for bearish gaps
3. **Inversion Confirmation:** Requires candle CLOSE above FVG high (not just wick)
4. **Entry Timing:** Open of next candle after confirmation
5. **NQ Tick Size:** 0.25 points (1 tick)
6. **Trade Duration:** Maximum 2 days before timeout
7. **Daily Limit:** Only first valid setup per day is taken

### Data Processing

- Loads data sequentially from all CSV files
- Sorts by datetime to ensure chronological order
- Handles weekends and market holidays automatically
- Requires minimum 3 days of history for Asian session calculation

### Performance Optimizations

- Efficient pandas operations for data filtering
- Day-by-day processing to manage memory
- Progress indicators for long-running backtests
- Vectorized calculations where possible

## Customization

### Modifying Strategy Parameters

Edit the following constants in `london_manipulation_backtest.py`:

```python
# Risk/Reward ratio
# Currently 1:1, can be modified in run_backtest() method

# Stop loss buffer
NQ_TICK_SIZE = 0.25  # Adjust tick size if needed

# Session times
# Modify is_asian_session() and is_london_open() methods
```

### Adding Custom Analysis

The `LondonManipulationBacktest` class can be extended:

```python
backtest = LondonManipulationBacktest()
backtest.load_data()
backtest.run_backtest()
backtest.calculate_statistics()

# Access trade data
trades_df = backtest.stats['trades_df']

# Perform custom analysis
# ... your code here ...
```

## Interpretation Notes

### Win Rate vs Profit Factor

- Win rate of 53.14% is slightly above breakeven for 1:1 RR
- Profit factor of 1.02 indicates the strategy is marginally profitable
- Average loss (-46.18) is larger than average win (41.56), but higher win rate compensates

### Drawdown Considerations

- Maximum drawdown of 1,352.63 points is significant
- Represents the largest peak-to-trough decline
- Occurred primarily during 2022 bearish period
- Risk management and position sizing crucial

### Recent Performance

- 2024-2025 shows improved performance (968.52 points combined)
- Win rate improved to 65% in 2024
- Strategy may be adapting well to recent market conditions

## Limitations and Considerations

1. **Slippage Not Included:** Results assume perfect fills at exact prices
2. **Commission Not Included:** No transaction costs applied
3. **Market Gaps:** Weekend gaps and holiday effects not specifically handled
4. **One Setup Per Day:** Conservative approach, multiple setups possible
5. **Fixed Risk/Reward:** 1:1 ratio may not be optimal for all market conditions
6. **Historical Data:** Past performance doesn't guarantee future results

## Troubleshooting

### Common Issues

**Problem:** `ModuleNotFoundError: No module named 'pandas'`
- **Solution:** Install required packages: `pip install pandas numpy tabulate`

**Problem:** `FileNotFoundError` for CSV files
- **Solution:** Ensure all data files are in the same directory as the script

**Problem:** Script runs but finds 0 trades
- **Solution:** Check data format, timezone settings, and verify Asian session spans correctly

**Problem:** Memory errors with large datasets
- **Solution:** Process years individually or increase available RAM

## Support and Contributions

This is a complete implementation of the London Manipulation strategy backtest. The code is designed to be:
- **Readable:** Well-commented and structured
- **Maintainable:** Modular class-based design
- **Extensible:** Easy to add custom features
- **Documented:** Comprehensive documentation provided

## Disclaimer

This backtest is for educational and research purposes only. Trading futures involves substantial risk of loss and is not suitable for all investors. Past performance is not indicative of future results. Always perform your own due diligence and consider consulting with a licensed financial advisor before trading.

---

*Last Updated: December 2025*

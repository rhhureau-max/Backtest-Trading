# ICT Trading Strategies Backtest System

A professional Python backtesting system for testing ICT (Inner Circle Trader) Price Action strategies on Nasdaq futures data (NQ).

## Features

- **3 ICT Trading Strategies:**
  - Strategy A: Judas Swing (False Breakout)
  - Strategy B: Power of 3 Intraday (Open Deviation)
  - Strategy C: Displacement (Impulse Candles)

- **3 Risk Management Modes:**
  - Mode 1: Scalper Fixe (15/30 points, 1:2 ratio)
  - Mode 2: Swing Session (40/100 points, 1:2.5 ratio)
  - Mode 3: Volatilité Dynamique (ATR-based dynamic stops)

- **Key Characteristics:**
  - NO timezone conversion (works with raw time data)
  - Trading window: 01:00 - 05:00 only
  - Hard exit at 05:00 (all positions closed)
  - Vectorized operations with Pandas/Numpy for performance
  - Comprehensive performance metrics

## Installation

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

1. Open `ict_backtest.py` and modify the **CONFIGURATION** section at the top:

```python
# Strategy Selection: Choose 'A', 'B', or 'C'
STRATEGY = 'A'  # A: Judas Swing | B: Power of 3 | C: Displacement

# Risk Management Mode: Choose 1, 2, or 3
RISK_MODE = 1  # 1: Scalper Fixe | 2: Swing Session | 3: Volatilité Dynamique

# Data Configuration
DATA_TIMEFRAME = '5m'  # Options: '1m', '5m', '15m'
START_YEAR = 2018
END_YEAR = 2025
```

2. Run the backtest:
```bash
python3 ict_backtest.py
```

3. Review the results in the console and the generated CSV file.

### Strategy Descriptions

#### Strategy A: Judas Swing (False Breakout)
**Concept:** Trap traders at the beginning of the session by identifying false breakouts.

**Logic:**
- Define the High and Low of the first hour (01:00 - 02:00)
- **Buy Signal:** Price breaks below first hour Low but closes above it (reintegration)
- **Sell Signal:** Price breaks above first hour High but closes below it

**Best for:** Catching reversals after false breakouts in the opening range.

#### Strategy B: Power of 3 Intraday (Open Deviation)
**Concept:** Buy in discount zones (below open) and sell in premium zones (above open).

**Reference:** Opening price of the 01:00 candle

**Logic:**
- **Buy Signal:** Price is >20 points below Open Price AND a bullish candle forms (Close > Open)
- **Sell Signal:** Price is >20 points above Open Price AND a bearish candle forms (Close < Open)

**Best for:** Mean reversion trading based on session open price.

#### Strategy C: Displacement (Impulse Candles)
**Concept:** Follow institutional footprints by identifying strong momentum candles.

**Logic:**
- Uses ATR(14) to measure normal volatility
- **Buy Signal:** Candle body > 2*ATR(14) AND green candle. Enter at close.
- **Sell Signal:** Candle body > 2*ATR(14) AND red candle. Enter at close.

**Best for:** Trend following and catching strong momentum moves.

### Risk Management Modes

#### Mode 1: Scalper Fixe
- Stop Loss: 15 points
- Take Profit: 30 points
- Ratio: 1:2
- **Best for:** Quick scalping trades with tight risk control

#### Mode 2: Swing Session
- Stop Loss: 40 points
- Take Profit: 100 points
- Ratio: 1:2.5
- **Best for:** Larger swings and trending moves within the session

#### Mode 3: Volatilité Dynamique
- Stop Loss: 2 * ATR(14)
- Take Profit: 4 * ATR(14)
- Ratio: 1:2 (dynamic)
- **Best for:** Adapting to changing market volatility from 2018-2025

## Output

The backtest generates:

1. **Console Output:**
   - Configuration summary
   - Data loading progress
   - Performance metrics:
     - Total Trades
     - Winning/Losing Trades
     - Win Rate (%)
     - Profit Factor
     - Total PnL
     - Return (%)
   - Sample trades

2. **CSV File:**
   - Detailed trade log with all entries and exits
   - Filename format: `backtest_results_{STRATEGY}_mode{RISK_MODE}_{TIMEFRAME}.csv`

## Example Results

```
============================================================
BACKTEST RESULTS
============================================================
  Total Trades.......................                3,207
  Winning Trades.....................                1,391
  Losing Trades......................                1,816
  Win Rate (%).......................                43.37
  Profit Factor......................                 1.14
  Total PnL..........................             8,075.22
  Gross Profit.......................            71,039.84
  Gross Loss.........................            62,964.62
  Initial Capital....................              100,000
  Final Equity.......................           108,075.22
  Return (%).........................                 8.08
============================================================
```

## Data Format

The script expects CSV files with semicolon (;) delimiters:
```
Column1;Column2;Column3;Column4;Column5;Column6;Column7
Date;Time;Open;High;Low;Close;Volume
01/01/2025;17:00:00;21927.625319;21980.720091;21911.645339;21975.049775;1482
```

Supported timeframes: 1m, 5m, 15m

## Configuration Options

### Additional Parameters

```python
# Trading Window (NO TIMEZONE CONVERSION - Raw time)
TRADING_START = time(1, 0)   # 01:00
TRADING_END = time(5, 0)     # 05:00 (Hard exit)

# Strategy B Specific Parameters
POWER_OF_3_THRESHOLD = 20  # Points deviation from open price

# Strategy C Specific Parameters
ATR_PERIOD = 14
DISPLACEMENT_MULTIPLIER = 2  # ATR multiplier for displacement detection

# Capital & Position Sizing
INITIAL_CAPITAL = 100000
POSITION_SIZE = 1  # Number of contracts per trade
```

## Performance Tips

- **Start with smaller date ranges** if processing is slow
- **Use 5m or 15m data** for faster backtesting during development
- **Compare all strategies** with the same risk mode to find the best fit
- **Test each strategy** across all risk modes to optimize

## Testing All Combinations

To systematically test all strategy and risk mode combinations:

```bash
# Test all 9 combinations (3 strategies × 3 risk modes)
for strategy in A B C; do
  for mode in 1 2 3; do
    # Edit STRATEGY and RISK_MODE in ict_backtest.py
    python3 ict_backtest.py
  done
done
```

## Notes

- **No timezone conversion:** The script works with raw time data as-is
- **Hard exit at 05:00:** All positions are forcefully closed at session end
- **Vectorized:** Uses Pandas/Numpy for efficient data processing
- **ATR-based:** Dynamic risk mode adapts to market volatility changes from 2018-2025

## License

This project is provided as-is for educational and research purposes.

## Author

Expert Python Quantitative Trading Specialist
ICT Price Action Expert

# NQ ICT Smart Money Backtesting Strategy

A complete Python implementation of an ICT (Inner Circle Trader) Smart Money Concepts backtesting strategy for NQ (Nasdaq 100) futures.

## Strategy Overview

This backtesting system implements a professional trading strategy based on:

### 1. **Trend Filter (Higher Timeframe)**
- Uses H1 (1-hour) and H4 (4-hour) timeframes
- Identifies market structure: Higher Highs & Higher Lows (bullish) or Lower Highs & Lower Lows (bearish)
- Uses a 20-candle sliding window for structure detection
- Only takes LONG trades in bullish trends, SHORT trades in bearish trends

### 2. **Opening Range (08:30 Chicago Time)**
- Captures the High and Low of the 5-minute candle at 08:30
- This range serves as a key reference level for the trading day

### 3. **Entry Protocol (1-minute setup)**
- **Trading Window:** 08:35 - 11:00 Chicago time
- **Entry Requirements:**
  - Price must break out of the 08:30 range (High or Low)
  - Price must return to the range
  - A Fair Value Gap (FVG) must form
  - Price must close through the FVG (inversion)

**LONG Setup (Bullish Trend):**
- Bearish FVG forms (gap between candle[i-2].Low and candle[i].High)
- Entry when 1-minute candle closes ABOVE the bearish FVG

**SHORT Setup (Bearish Trend):**
- Bullish FVG forms (gap between candle[i-2].High and candle[i].Low)
- Entry when 1-minute candle closes BELOW the bullish FVG

### 4. **Risk Management**
- **Stop Loss:** Fixed 20 points
- **Take Profits:** Position split into 3 equal parts:
  - TP1: 20 points
  - TP2: 30 points
  - TP3: 40 points
- Each trade is tracked as 3 separate positions

## Project Structure

```
.
├── data_loader.py           # Loads and preprocesses CSV data
├── market_structure.py      # Detects HH/HL and LH/LL patterns
├── fvg_detector.py          # Identifies Fair Value Gaps
├── entry_signals.py         # Generates entry signals
├── risk_manager.py          # Manages positions and risk
├── backtest_engine.py       # Main backtesting engine
├── results_analyzer.py      # Performance analytics
├── run_backtest.py          # Main execution script
└── requirements.txt         # Python dependencies
```

## Installation

### Prerequisites
- Python 3.8 or higher
- NQ data files (2018-2025) in CSV format

### Setup

1. **Clone or download this repository**

2. **Install required packages:**
```bash
pip install -r requirements.txt
```

3. **Prepare your data:**
   - Place NQ CSV files in the project directory
   - Required files: `YYYY 1m.csv`, `YYYY 5m.csv`, `YYYY 1H.csv`, `YYYY 4H.csv` for each year
   - 1-minute files can be in `.zip` format (will be auto-extracted)

## Usage

### Run the Complete Backtest

```bash
python run_backtest.py
```

This will:
1. Load all CSV data files (2018-2025)
2. Detect market structure on H1 and H4
3. Identify Fair Value Gaps on 1-minute data
4. Execute the complete backtest
5. Generate comprehensive results report
6. Export detailed trade log to CSV

### Output

The script generates two files:

1. **CSV File** (`nq_backtest_results_YYYYMMDD_HHMMSS.csv`):
   - Detailed trade-by-trade breakdown
   - Includes all position exits (TP1, TP2, TP3)
   - Entry/exit times, prices, and PnL

2. **Text Report** (`nq_backtest_report_YYYYMMDD_HHMMSS.txt`):
   - Overall performance metrics
   - Year-by-year breakdown
   - Long vs Short performance
   - Win rate, profit factor, drawdown

### Example Output

```
================================================================================
NQ ICT STRATEGY BACKTEST RESULTS
================================================================================

OVERALL PERFORMANCE
--------------------------------------------------------------------------------
Total Trades:        245
Winning Trades:      147
Losing Trades:       98
Win Rate:            60.00%
Total PnL:           1234.56 points
Average Win:         35.67 points
Average Loss:        18.45 points
Profit Factor:       2.85
Max Drawdown:        -156.78 points (-12.5%)

YEARLY PERFORMANCE
--------------------------------------------------------------------------------
Year   Trades   Win    Loss   WinRate   PnL         PF
--------------------------------------------------------------------------------
2018   32       20     12     62.50%    234.56      3.12
2019   38       22     16     57.89%    189.34      2.45
...
```

## Data Format

Expected CSV format:
- **Separator:** Semicolon (`;`)
- **Columns:** `Date;Time;Open;High;Low;Close;Volume`
- **Date Format:** `DD/MM/YYYY`
- **Time Format:** `HH:MM:SS`
- **Timezone:** Chicago (US/Central)

Example:
```
Column1;Column2;Column3;Column4;Column5;Column6;Column7
01/01/2018;17:00:00;7503.74;7511.94;7499.64;7511.35;1451
```

## Module Descriptions

### data_loader.py
Handles loading CSV files, extracting zipped data, combining multiple years, and timezone conversion.

### market_structure.py
Implements swing point detection and market structure analysis (HH/HL/LH/LL) using a 20-candle lookback window.

### fvg_detector.py
Detects Fair Value Gaps (bullish and bearish) on 1-minute data and tracks them for entry signals.

### entry_signals.py
Manages opening range detection, breakout/return logic, and FVG inversion entry signals.

### risk_manager.py
Handles position creation, stop loss/take profit management, and tracks individual position outcomes.

### backtest_engine.py
Orchestrates the entire backtest, processing each trading day and managing active positions.

### results_analyzer.py
Calculates performance metrics, generates reports, and exports results to CSV.

## Key Features

✅ **Complete ICT Strategy Implementation**
- Market structure (HH/HL vs LH/LL)
- Opening range breakout
- Fair Value Gap detection and inversion
- Proper trend filtering

✅ **Professional Risk Management**
- Fixed stop loss
- Multiple take profit levels
- Position tracking per TP level

✅ **Comprehensive Analytics**
- Overall performance metrics
- Year-by-year breakdown
- Long vs Short analysis
- Drawdown calculation

✅ **Efficient Data Handling**
- Handles multiple timeframes
- Processes years 2018-2025
- Auto-extracts zipped files
- Proper timezone handling

## Customization

You can modify the strategy parameters in `run_backtest.py`:

```python
# Configuration
STOP_LOSS_POINTS = 20.0  # Adjust stop loss
```

Or modify the take profit levels in `risk_manager.py`:

```python
self.tp_levels = [20, 30, 40]  # Modify TP levels
```

## Performance Considerations

- The backtest processes 1-minute data across 8 years (~2-3 million bars)
- Expected runtime: 5-15 minutes depending on hardware
- Memory usage: ~2-4 GB RAM
- Progress bar shows real-time execution status

## Troubleshooting

**Issue:** `No data loaded for timeframe`
- **Solution:** Ensure CSV files are in the correct directory with proper naming

**Issue:** `KeyError: 'DateTime'`
- **Solution:** Check CSV format matches expected semicolon-separated format

**Issue:** Memory errors
- **Solution:** Process fewer years or increase available RAM

## License

This project is provided as-is for educational and research purposes.

## Author

Quantitative Backtesting & ICT Strategy Implementation

## Version

1.0.0 - Initial Release

## Support

For issues or questions, please review the code comments and module docstrings for detailed implementation information.

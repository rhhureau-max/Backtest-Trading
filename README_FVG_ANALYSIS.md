# London Killzone FVG Scenario Analysis

## Overview

This script performs comprehensive Fair Value Gap (FVG) analysis specifically for the London Killzone trading session (01:00-04:00 NY Time) on NQ futures data from 2018-2025.

## Features

### 1. **FVG Detection**
- Detects both Bullish and Bearish Fair Value Gaps
- **Bullish FVG**: When High(n-1) < Low(n+1)
- **Bearish FVG**: When Low(n-1) > High(n+1)
- Only analyzes FVGs that form during London Killzone hours

### 2. **Scenario Classification**
The script classifies each FVG into one of three scenarios:

#### Scenario A - Liquidity Sweep Reversal
- Occurs when price wicks beyond a significant high/low before the FVG forms
- The wick does NOT close beyond the level (body remains inside)
- This represents a "Judas swing" or liquidity grab
- Indicates potential reversal setup

#### Scenario B - Market Structure Shift (MSS)
- The FVG formation breaks previous market structure
- For bullish FVG: breaks above highest high of previous 12 candles
- For bearish FVG: breaks below lowest low of previous 12 candles
- No liquidity sweep occurs first
- Indicates strong directional movement

#### Scenario C - Simple Continuation
- FVG forms without breaking structure or sweeping liquidity
- Occurs mid-trend as a continuation pattern
- Most common scenario but potentially less reliable

### 3. **Mitigation Detection**
- Checks if price touches the FVG zone within 60 minutes (12 candles)
- A FVG is "mitigated" when any subsequent candle touches the zone
- Only mitigated FVGs are used for trade simulation

### 4. **Trade Simulation**
For each mitigated FVG, the script simulates trades with:
- **Entry**: At the mitigation point (when price touches FVG zone)
- **Direction**: Long for bullish FVG, Short for bearish FVG
- **Stop Loss**: 
  - Long: Just below the Low of candle (n-1)
  - Short: Just above the High of candle (n-1)
- **Take Profit Levels**:
  - TP1: Risk-Reward ratio 1:1
  - TP2: Risk-Reward ratio 2:1

### 5. **Comprehensive Statistics**
The script provides:
- Scenario comparison table with all key metrics
- Win rates at both 1:1 and 2:1 risk-reward ratios
- Average profit and loss in points
- Net expectancy per trade
- Breakdown by FVG type (bullish vs bearish)
- Distribution across London Killzone hours
- Yearly performance analysis

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Install Required Packages

```bash
pip install -r requirements_fvg_analysis.txt
```

Or install manually:

```bash
pip install pandas numpy
```

## Usage

### Basic Usage

Simply run the script from the repository root directory:

```bash
python3 london_killzone_fvg_scenario_analysis.py
```

### Data Requirements

The script expects CSV files in the following format:
- **Filename pattern**: `YEAR 5m.csv` (e.g., `2018 5m.csv`, `2019 5m.csv`)
- **Separator**: Semicolon (`;`)
- **Columns**:
  - Column1: Date (format: DD/MM/YYYY)
  - Column2: Time (format: HH:MM:SS)
  - Column3: Open price
  - Column4: High price
  - Column5: Low price
  - Column6: Close price
  - Column7: Volume

Example:
```
Column1;Column2;Column3;Column4;Column5;Column6;Column7
01/01/2018;17:00:00;7503.739664;7511.940473;7499.63926;7511.3547;1451
```

### Output

The script generates:

1. **Console Output**: Detailed analysis results displayed in formatted tables
2. **CSV File**: `london_killzone_fvg_analysis_results.csv` containing detailed results for each FVG

#### Output CSV Columns:
- `datetime`: When the FVG formed
- `type`: Bullish or Bearish
- `scenario`: A, B, or C
- `gap_size`: Size of the gap in points
- `zone_low`: Lower boundary of FVG zone
- `zone_high`: Upper boundary of FVG zone
- `is_mitigated`: Whether the FVG was touched within 60 minutes
- `entry_price`: Trade entry price (if mitigated)
- `stop_loss`: Stop loss level
- `tp1`: Take profit 1 level (1:1 RR)
- `tp2`: Take profit 2 level (2:1 RR)
- `tp1_hit`: Whether TP1 was reached
- `tp2_hit`: Whether TP2 was reached
- `sl_hit`: Whether stop loss was hit
- `pnl_points`: Profit/loss in points
- `outcome`: Trade outcome (TP1, TP2, SL, or No Trade)

## Configuration

You can modify the following constants in the script to adjust the analysis:

```python
# London Killzone hours (NY Time)
LONDON_KILLZONE_START = time(1, 0)  # 01:00
LONDON_KILLZONE_END = time(4, 0)    # 04:00

# Analysis parameters
LOOKBACK_CANDLES = 12  # 60 minutes
MITIGATION_WINDOW = 12  # 60 minutes

# Risk-Reward ratios
RR_RATIO_1 = 1.0  # TP1
RR_RATIO_2 = 2.0  # TP2
```

## Understanding the Results

### Key Metrics Explained

- **Total Occurrences**: Number of FVGs detected in this scenario
- **Mitigation Rate**: Percentage of FVGs that were touched within 1 hour
- **Win Rate RR 1:1**: Percentage of trades that hit TP1 before SL
- **Win Rate RR 2:1**: Percentage of trades that hit TP2 before SL
- **Net Expectancy**: Average profit/loss per trade in points

### Interpretation Tips

1. **High Mitigation Rate**: Indicates FVGs in this scenario are frequently tested by price
2. **Win Rate > 40% at RR 1:1**: Generally considered profitable with proper risk management
3. **Positive Net Expectancy**: Indicates the scenario has edge over many trades
4. **Scenario Comparison**: Compare the three scenarios to identify which setups work best

## Performance Notes

- Processing time: ~5-10 minutes for full dataset (2018-2025)
- The script processes approximately 17,000+ FVGs
- Memory usage: ~500MB-1GB depending on dataset size

## Example Output

```
================================================================================
SCENARIO COMPARISON TABLE
--------------------------------------------------------------------------------
Metric                         Scenario A           Scenario B           Scenario C          
--------------------------------------------------------------------------------
Scenario Name                  Liquidity Sweep      Market Structure Shift Simple Continuation 
Total Occurrences              17518                17                   172                 
Number Mitigated               103                  0                    0                   
Mitigation Rate (%)            0.59%                0.00%                0.00%               
Trades Taken                   103                  0                    0                   
Wins at RR 1:1                 38                   0                    0                   
Win Rate RR 1:1 (%)            36.89%               0.00%                0.00%               
Wins at RR 2:1                 29                   0                    0                   
Win Rate RR 2:1 (%)            28.16%               0.00%                0.00%               
```

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError: No module named 'pandas'**
   - Solution: Run `pip install pandas numpy`

2. **File not found error**
   - Ensure CSV files are in the correct format: `YEAR 5m.csv`
   - Check that files are in the same directory as the script

3. **Memory error**
   - Close other applications to free up memory
   - Process fewer years by modifying the `DATA_YEARS` variable

## Advanced Usage

### Processing Specific Years

Modify the `DATA_YEARS` range in the script:

```python
DATA_YEARS = range(2023, 2026)  # Only 2023-2025
```

### Adjusting Lookback Period

Change the lookback window for scenario classification:

```python
LOOKBACK_CANDLES = 24  # 120 minutes instead of 60
```

### Custom London Killzone Hours

Adjust the killzone time window:

```python
LONDON_KILLZONE_START = time(2, 0)  # 02:00
LONDON_KILLZONE_END = time(5, 0)    # 05:00
```

## Technical Details

### Data Processing
- Uses pandas for efficient data manipulation
- Vectorized operations where possible for performance
- Timezone handling assumes data is in NY time (or consistent timezone)

### FVG Detection Algorithm
- Iterates through price data looking for gaps between candle n-1 and n+1
- Stores complete information about each FVG for later analysis
- Maintains indices for efficient forward-looking analysis

### Trade Simulation Logic
- Simulates realistic trade execution at mitigation point
- Checks each subsequent candle for stop loss or take profit hits
- Assumes stop loss is hit before take profit on the same candle (conservative)
- Limits forward-looking to 200 candles (~16 hours) to avoid stale trades

## License

This script is provided as-is for analysis purposes.

## Contributing

To improve this script:
1. Add error handling for edge cases
2. Implement parallel processing for faster analysis
3. Add visualization capabilities (charts, graphs)
4. Include additional scenarios or filtering criteria
5. Add backtesting with position sizing and portfolio metrics

## Author

Created for comprehensive FVG analysis in NQ futures trading during London Killzone hours.

## Version History

- v1.0 (2024): Initial release with three-scenario classification and comprehensive statistics

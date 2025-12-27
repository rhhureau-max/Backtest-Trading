# London Killzone FVG Inversion Backtesting Script

## Overview
This script backtests the "London Killzone FVG Inversion" strategy on Nasdaq 100 (NQ) using 15-minute timeframe data from 2018 to present.

## Strategy Description

### Time Window
- Trade setups are only considered between **01:00 and 05:00** (London Killzone)

### Fair Value Gap (FVG) Definition
- **Bullish FVG**: When Low[i-2] > High[i], creating a gap between High[i] and Low[i-2]
- **Bearish FVG**: When High[i-2] < Low[i], creating a gap between High[i-2] and Low[i]

### Entry Signals (FVG Inversion)
- **Long Entry**: Price closes ABOVE the top of a previously identified Bearish FVG
- **Short Entry**: Price closes BELOW the bottom of a previously identified Bullish FVG

### Risk Management
- **Stop Loss**:
  - Long: Placed at the Low of the entry candle
  - Short: Placed at the High of the entry candle
  
- **Take Profit**: Three Risk-to-Reward ratios are tested:
  - TP1: 1:1 RR
  - TP2: 1.5:1 RR
  - TP3: 2:1 RR

## Usage

### Data Requirements
The script expects CSV files named in the format `YYYY 15m.csv` (e.g., `2018 15m.csv`, `2019 15m.csv`, etc.) with the following structure:

```
Column1;Column2;Column3;Column4;Column5;Column6;Column7
Date;Time;Open;High;Low;Close;Volume
```

- **Delimiter**: Semicolon (;)
- **Date Format**: DD/MM/YYYY
- **Time Format**: HH:MM:SS

### Running the Script

1. Ensure all required CSV files are in the same directory as the script
2. Install required dependencies:
   ```bash
   pip install pandas
   ```

3. Run the script:
   ```bash
   python london_killzone_fvg_backtest.py
   ```

### Alternative: Custom CSV File
You can also provide a single CSV file named `nq_15m_data.csv` with columns: `Date`, `Time`, `Open`, `High`, `Low`, `Close`.

## Output

The script outputs:
- Total number of trades executed
- Breakdown of long and short trades
- For each Risk-to-Reward ratio (1.0, 1.5, 2.0):
  - Win Rate (%)
  - Total PnL (in points)
  - Average Win (in points)
  - Average Loss (in points)
  - Number of winning trades
  - Number of losing trades

## Script Features

- **FVG Management**: Automatically tracks and manages multiple active FVGs
- **Mitigation Logic**: Removes FVGs that are filled/mitigated before inversion
- **Separate PnL Tracking**: Calculates outcomes for three different take-profit levels
- **Comprehensive Statistics**: Provides detailed performance metrics for analysis
- **Clean Code Structure**: Object-oriented design with FVG and Trade classes

## Example Output

```
=== London Killzone FVG Inversion Backtest Results ===

Total Trades: 3,008
Long Trades: 1,606 (53.39%)
Short Trades: 1,402 (46.61%)

--- Risk-Reward 1.0 Results ---
Win Rate: 38.93%
Total PnL: -4,357.02 points
Average Win: 28.45 points
Average Loss: -28.45 points
Winning Trades: 1,171
Losing Trades: 1,837

--- Risk-Reward 1.5 Results ---
Win Rate: 33.05%
Total PnL: -3,470.47 points
...
```

## Notes

- The script processes data from 2018 to 2025 (all available 15m CSV files)
- FVGs are only identified during the London Killzone window
- The script prevents immediate mitigation on the candle that creates the FVG
- Each trade is tracked independently for the three different RR scenarios

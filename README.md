# Backtest-Trading

## 8:30 AM Candle Breakout Strategy

This repository contains a backtesting strategy that analyzes trading opportunities based on 8:30 AM candles breaking above or below the previous 5 candles' wicks.

## Strategy Description

The strategy identifies trades where the 8:30 AM candle meets specific conditions relative to the previous 5 candles:

- **BULLISH Signal**: The 8:30 AM candle closes ABOVE the highest high (wick) of the previous 5 candles
- **BEARISH Signal**: The 8:30 AM candle closes BELOW the lowest low (wick) of the previous 5 candles

## Data Coverage

- **Years**: 2018 to 2025
- **Timeframes**: 1-minute, 5-minute, and 15-minute data
- **Data Format**: CSV files with columns: Date, Time, Open, High, Low, Close, Volume

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Backtest-Trading.git
cd Backtest-Trading
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Quick Start - Complete Analysis

To run the complete backtest and RR analysis pipeline:

```bash
./run_complete_analysis.sh
```

Or run each step individually:

### Step 1: Running the Backtest

To identify all trades where the 8:30 AM candle breaks the previous 5 candles:

```bash
python3 backtest_strategy.py
```

This will:
1. Analyze all CSV files for years 2018-2025
2. Process 1m, 5m, and 15m timeframes
3. Identify all qualifying trades at 8:30 AM
4. Generate summary statistics
5. Save results to CSV files

### Step 2: Running Risk/Reward Analysis

To analyze each trade with different stop-loss placements and RR ratios:

```bash
python3 rr_analysis.py
```

This will:
1. Load trades from backtest_results.csv
2. Test 4 different SL placements (100%, 75%, 50%, 25% body retracement)
3. Test 9 different RR ratios (1.0 to 5.0)
4. Simulate 36 scenarios per trade (135,864 total scenarios)
5. Calculate win rates, expectancy, and profit factors
6. Generate detailed reports and CSV files

### Step 3: Viewing Best Strategies

To quickly view the top performing strategies:

```bash
python3 view_best_strategies.py
```

This displays:
- Top strategies by expectancy
- Top strategies by win rate
- Top strategies by total P&L
- Top strategies by profit factor
- Average performance by SL placement and RR ratio

### Output Files

#### Backtest Results

- **backtest_results.csv**: All trades across all timeframes
- **backtest_results_1m.csv**: Trades from 1-minute data
- **backtest_results_5m.csv**: Trades from 5-minute data
- **backtest_results_15m.csv**: Trades from 15-minute data

#### RR Analysis Results

- **rr_analysis_complete.csv**: All 135,864 trade scenarios (3,774 trades × 36 combinations)
- **rr_analysis_SL_100.csv**: Results for 100% body retracement stop-loss
- **rr_analysis_SL_75.csv**: Results for 75% body retracement stop-loss
- **rr_analysis_SL_50.csv**: Results for 50% body retracement stop-loss
- **rr_analysis_SL_25.csv**: Results for 25% body retracement stop-loss
- **rr_analysis_summary.csv**: Statistical summary for all SL/RR combinations

For detailed documentation on RR analysis, see **RR_ANALYSIS_README.md**

### Output Format

Each output file contains the following columns:

| Column | Description |
|--------|-------------|
| Date | Date of the trade (DD/MM/YYYY) |
| Time | Time of the trade (HH:MM:SS) |
| Timeframe | Data timeframe (1m, 5m, or 15m) |
| Candle_Type | BULLISH or BEARISH |
| Open | Opening price of the 8:30 AM candle |
| High | Highest price of the 8:30 AM candle |
| Low | Lowest price of the 8:30 AM candle |
| Close | Closing price of the 8:30 AM candle |
| Reference_Level | The level that was broken (max high or min low of previous 5 candles) |
| Condition | Description of the condition that was met |

## Results Summary

### Backtest Results (2018-2025)

- **Total Trades Found**: 3,774
- **1-minute timeframe**: 1,209 trades (557 bearish, 652 bullish)
- **5-minute timeframe**: 1,372 trades (663 bearish, 709 bullish)
- **15-minute timeframe**: 1,193 trades (560 bearish, 633 bullish)

### RR Analysis Results

After simulating 135,864 scenarios (3,774 trades × 36 SL/RR combinations):

#### Top 3 Best Performing Strategies:

1. **SL_100 + RR 4.0**
   - Win Rate: 22.8%
   - Expectancy: $4.43 per trade
   - Profit Factor: 1.18
   - Total P&L: $16,549.61

2. **SL_100 + RR 3.0**
   - Win Rate: 27.7%
   - Expectancy: $3.74 per trade
   - Profit Factor: 1.16
   - Total P&L: $14,079.35

3. **SL_100 + RR 3.5**
   - Win Rate: 24.9%
   - Expectancy: $3.67 per trade
   - Profit Factor: 1.15
   - Total P&L: $13,751.49

#### Key Findings:

- **Best SL Placement**: SL_100 (full body retracement) shows consistently better performance
- **Optimal RR Range**: 3.0 - 4.0 provides the best expectancy
- **Average Win Rate**: 27.9% across all scenarios
- **Overall Profit Factor**: 1.12

For complete analysis, see **RR_ANALYSIS_README.md**

## Strategy Logic

The backtest follows this logic:

1. For each trading day, identify the 8:30 AM candle
2. Look back at the previous 5 candles
3. Determine if the current candle is bullish (close > open) or bearish (close < open)
4. For bullish candles: Check if close > max(previous 5 highs)
5. For bearish candles: Check if close < min(previous 5 lows)
6. Record trades that meet the criteria

## Code Structure

```
backtest_strategy.py
├── BacktestStrategy class
│   ├── read_csv_file()          # Handles CSV and ZIP file reading
│   ├── is_bullish()              # Checks if candle is bullish
│   ├── is_bearish()              # Checks if candle is bearish
│   ├── check_bullish_condition() # Validates bullish breakout
│   ├── check_bearish_condition() # Validates bearish breakout
│   ├── analyze_timeframe()       # Analyzes specific timeframe/year
│   ├── run_backtest()            # Main backtest execution
│   ├── generate_summary()        # Creates summary statistics
│   ├── save_results()            # Saves results to CSV
│   └── print_summary_report()    # Displays formatted report
└── main()                        # Entry point
```

## Customization

You can customize the strategy by modifying the following parameters in the script:

- **Timeframes**: Change the `self.timeframes` list to analyze different intervals
- **Years**: Modify the `self.years` range to analyze different periods
- **Lookback Period**: Change the number 5 in the condition checks to analyze more/fewer previous candles
- **Time Filter**: Modify `'08:30:00'` to analyze different times of day

## Example Analysis

### Sample Trade (Bullish)
```
Date: 16/01/2018
Time: 08:30:00
Timeframe: 1m
Candle Type: BULLISH
Close: 7982.02
Reference Level: 7981.73
Condition: Close (7982.02) > Reference (7981.73)
```

This indicates that on January 16, 2018, the 8:30 AM one-minute candle closed at 7982.02, which was above the highest high (7981.73) of the previous 5 candles.

## Dependencies

- pandas >= 1.5.0
- numpy >= 1.21.0

## License

This project is provided as-is for educational and research purposes.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Contact

For questions or suggestions, please open an issue in the repository.
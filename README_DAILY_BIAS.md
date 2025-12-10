# Daily Bias Probability Analysis Script

## Overview

This script analyzes historical daily (1D) data to calculate statistical probabilities of daily bias (Close > Open or Close < Open) based on previous day conditions. It implements ICT (Inner Circle Trader) concepts and Price Action analysis.

## Features

The script performs three main analyses:

### 1. **Momentum Sequences (Candle Streaks)**
- Calculates probability of green/red candles after consecutive sequences
- Analyzes 1, 2, and 3 consecutive candle patterns
- Shows both continuation and reversal probabilities

### 2. **Price Action & ICT Liquidity Concepts**
- **PDH (Previous Day High) Sweep**: Detects when J-1 wicks above J-2 high but closes below (liquidity grab)
- **PDL (Previous Day Low) Sweep**: Detects when J-1 wicks below J-2 low but closes above (liquidity grab)
- **Inside Bar Pattern**: Identifies consolidation (J-1 contained within J-2) and expansion probabilities

### 3. **Volatility Analysis (Range & Compression)**
- Compares daily range to ADR (Average Daily Range - 10 periods)
- Identifies compression scenarios (low volatility) and expansion potential
- Analyzes high volatility days and contraction probability

## Installation

### Requirements
```bash
pip install -r requirements.txt
```

Required packages:
- pandas >= 2.0.0
- numpy >= 1.24.0
- yfinance >= 0.2.0

## Usage

### Option 1: Using yfinance (default)

```python
from daily_bias_probability_analysis import DailyBiasProbabilityAnalyzer

# Analyze EURUSD
analyzer = DailyBiasProbabilityAnalyzer(symbol='EURUSD=X', start_date='2018-01-01')
results = analyzer.run_full_analysis()

# Analyze BTC-USD
analyzer = DailyBiasProbabilityAnalyzer(symbol='BTC-USD', start_date='2018-01-01')
results = analyzer.run_full_analysis()
```

### Option 2: Using local CSV files

```python
from daily_bias_probability_analysis import DailyBiasProbabilityAnalyzer

# Analyze from local NQ CSV files
analyzer = DailyBiasProbabilityAnalyzer(
    symbol='NQ',
    start_date='2018-01-01',
    use_local_csv=True,
    csv_dir='/path/to/csv/files'
)
results = analyzer.run_full_analysis()
```

### Running the script directly

```bash
python daily_bias_probability_analysis.py
```

The script automatically detects if local CSV files are available and uses them. Otherwise, it fetches data from Yahoo Finance.

## CSV File Format

The script supports NQ/ES CSV format with semicolon separators:
- Column1: Date (DD/MM/YYYY)
- Column2: Time (HH:MM:SS)
- Column3: Open
- Column4: High
- Column5: Low
- Column6: Close
- Column7: Volume

Expected file naming: `YYYY 1D.csv` (e.g., `2018 1D.csv`, `2019 1D.csv`, etc.)

## Output

The script outputs:

1. **Momentum Analysis**: Probability percentages for continuation/reversal after 1, 2, or 3 consecutive candles
2. **PDH/PDL Sweeps**: Reversal probabilities after liquidity grabs
3. **Inside Bar Patterns**: Expansion direction probabilities
4. **Volatility Analysis**: Compression/expansion probabilities based on ADR

Example output:
```
🟢 After 1 GREEN candle:
   • Total occurrences: 1117
   • Next candle GREEN: 596 (53.36%)
   • Next candle RED: 521 (46.64%)

💧 PDH (Previous Day High) SWEEP:
   • Total PDH sweeps detected: 501
   • Bearish reversal on J (RED): 229 (45.71%)
   • Continuation bullish (GREEN): 272 (54.29%)
```

## Key Insights from Analysis

Based on NQ data (2018-2025):

1. **Momentum**: After green candles, there's ~53% continuation probability, while after red candles, there's ~57% chance of reversal to green
2. **PDL Sweeps**: Show 52.76% bullish reversal probability
3. **Inside Bars**: After green J-2, there's 58.65% bullish continuation probability
4. **Volatility Compression**: Low volatility compression shows balanced probability but rarely leads to immediate major expansion

## Google Colab Usage

To run on Google Colab:

1. Upload the script to your Colab environment
2. Install dependencies:
```python
!pip install yfinance pandas numpy
```
3. Run the script:
```python
!python daily_bias_probability_analysis.py
```

Or use it as a module:
```python
from daily_bias_probability_analysis import DailyBiasProbabilityAnalyzer

analyzer = DailyBiasProbabilityAnalyzer(symbol='BTC-USD', start_date='2018-01-01')
results = analyzer.run_full_analysis()
```

## Customization

You can customize the analysis by:
- Changing the symbol/asset
- Adjusting date ranges
- Modifying ADR periods (default: 10)
- Adjusting volatility thresholds for compression/expansion detection
- Adding your own ICT patterns

## Author

Expert Quant Trader - ICT & Price Action Specialist

## Date

2025-12-10

## License

This script is provided for educational and research purposes.

# NQ Futures London Session Backtesting System

## Overview

This comprehensive Python backtesting script analyzes NQ futures (Nasdaq-100) trading strategies focused on the London session with all times displayed in **Japan Standard Time (JST)**.

The script analyzes **8 years of data (2018-2025)** using multiple timeframes (15m, 1H, 4H, 1D) and implements four professional trading methods with detailed statistical analysis.

## Key Features

### Four Trading Methods Implemented

1. **Method 1: Judas Swing Post-Asia (Contrarian)**
   - Identifies false breakouts after Asian session
   - Analyzes rejection wicks at Asian range boundaries
   - **Results**: 69.2% average success rate

2. **Method 2: NY Midnight Opening Rule (Trend Follow)**
   - Uses NY midnight open (13:00/14:00 JST) as bias indicator
   - Confirms directional bias at London open (16:00 JST)
   - **Results**: 73.9% average success rate

3. **Method 3: H4 Market Structure (Top-Down)**
   - Analyzes higher timeframe swing structure
   - Correlates with D1 candle positioning
   - **Results**: 85.8% average success rate ⭐ **BEST PERFORMER**

4. **Method 4: SMT Divergence (Advanced)**
   - Compares NQ and ES price action for divergences
   - Identifies smart money positioning
   - **Results**: 73.8% average success rate

### Comprehensive Analyses Included

- **D1/London Session Correlation**: Probability analysis when D1 closes in top 25%
- **Asian Range Sweep Analysis**: Fakeout vs true breakout statistics
- **Volume & Volatility Patterns**: Hourly analysis to identify optimal trading windows
- **H4 Continuation Strategy**: Price behavior at key discount zones

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. Clone the repository (if not already done)
2. Install required dependencies:

```bash
pip install -r requirements_backtest.txt
```

Or manually install:

```bash
pip install pandas numpy pytz
```

## Usage

### Running the Analysis

Simply execute the script from the repository directory:

```bash
python3 nq_london_session_backtest.py
```

Or if made executable:

```bash
./nq_london_session_backtest.py
```

### Expected Runtime

- **Processing time**: 30-90 seconds depending on system
- **Data processed**: ~184,000+ 15m candles across 8 years
- **Output**: Console display + results file

### Output Files

The script generates:

1. **Console output**: Real-time progress and detailed statistics
2. **nq_analysis_results.txt**: Comprehensive summary report with:
   - Performance statistics for all methods
   - Best performing method identification
   - Key correlations and insights
   - Daily action plan template in JST

## Key Findings

Based on 2,032 trading days analyzed (2018-2025):

### Method Performance Ranking

1. **H4 Market Structure**: 85.8% success rate ⭐
2. **NY Midnight Rule**: 73.9% success rate
3. **SMT Divergence**: 73.8% success rate
4. **Judas Swing**: 69.2% success rate

### Important Insights

- **Volume spike**: Significant increase (2384%) occurs at 23:00 JST (US session)
- **Asian range sweeps**: 17.5% fakeout rate on highs, 22.0% on lows
- **D1 correlation**: 50.5% probability of bullish London when D1 closes in top 25%
- **H4 continuation**: 65.2% of bullish H4 periods test 14:00-15:00 JST levels

## Time Zones Explained

All times in the script are displayed in **JST (Japan Standard Time)** for consistency:

- **Asian Session**: 08:00-15:00 JST
- **NY Midnight**: 13:00 JST (winter) / 14:00 JST (summer DST)
- **London Session**: 16:00-21:00 JST
- **US Session Peak**: 23:00-01:00 JST

The script automatically handles DST transitions when converting from Chicago Time (CT) to JST.

## Daily Action Plan Template

The script provides a detailed daily trading plan:

```
08:00-15:00 JST - ASIAN SESSION
  • Mark Asian Range High and Low
  • Observe key levels and liquidity zones

13:00-14:00 JST - NY MIDNIGHT OPEN
  • Mark the opening price level

14:00-16:00 JST - PRE-LONDON / SMT WINDOW
  • Check for SMT divergence between NQ and ES
  • Monitor for Asian range sweeps

15:30-17:00 JST - JUDAS SWING WINDOW
  • Watch for false breakouts of Asian range
  • Rejection wicks signal potential reversals

16:00 JST - LONDON SESSION OPEN
  • Apply NY Midnight Rule bias
  • Check price vs midnight level for directional bias

16:00-21:00 JST - LONDON SESSION TRADING
  • Trade in direction of confirmed bias
  • Look for H4 structure confirmation
  • Use discount zones for entries
```

## Data Requirements

The script expects CSV files in the following format:

- **Delimiter**: Semicolon (;)
- **Columns**: Date;Time;Open;High;Low;Close;Volume
- **Date format**: DD/MM/YYYY
- **Time format**: HH:MM:SS
- **Timezone**: Chicago Time (CST/CDT)

### Required Files

- NQ data: `YYYY 15m.csv`, `YYYY 1H.csv`, `YYYY 4H.csv`, `YYYY 1D.csv`
- ES data: `ES 15m (2018-2025).csv` (for SMT analysis)

## Code Structure

The script is organized into logical sections:

1. **Timezone Configuration**: Handles CT to JST conversion
2. **Data Loading Functions**: Multi-year data aggregation
3. **Method 1-4 Analysis**: Individual strategy implementations
4. **Correlation Analyses**: Supporting statistical analyses
5. **Report Generation**: Summary and action plan creation

## Customization

You can modify key parameters in the script:

- **Session times**: Adjust in each method's function
- **Success thresholds**: Modify percentage thresholds (currently 0.1-0.2%)
- **Window sizes**: Change rolling window periods for H4 analysis
- **Volatility filters**: Add minimum range requirements

## Error Handling

The script includes robust error handling for:

- Missing data files
- Timezone ambiguity during DST transitions
- Insufficient data points
- Invalid date ranges

## Limitations

- Past performance does not guarantee future results
- Results are for educational and research purposes only
- Assumes continuous data without gaps
- Does not account for spreads, commissions, or slippage
- Simplified entry/exit logic for statistical analysis

## Risk Disclaimer

⚠️ **IMPORTANT**: This analysis is for educational purposes only. Always:

- Use proper risk management
- Test strategies on demo accounts first
- Never risk more than you can afford to lose
- Consider transaction costs and slippage
- Consult with a financial advisor

## Technical Support

### Common Issues

1. **ModuleNotFoundError**: Install required packages using pip
2. **File not found**: Ensure you're running from the correct directory
3. **Timezone warnings**: These are normal during DST transitions (handled automatically)

## Future Enhancements

Potential improvements for future versions:

- Interactive visualization with matplotlib/plotly
- Configurable parameters via command-line arguments
- Export detailed trade-by-trade results to CSV
- Real-time data integration
- Machine learning prediction models
- Monte Carlo simulation for risk analysis

## Author

Trading Analysis System  
Date: 2025-12-26

## License

This script is provided as-is for educational purposes.

---

**Happy Backtesting! 📈**

For questions or issues, please refer to the repository documentation.

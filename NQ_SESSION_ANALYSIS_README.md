# NQ Futures Session Analysis (01:00-07:00)

## Overview
This analysis examines NQ futures price action during the 01:00-07:00 session window across 8 years of historical data (2018-2025).

## Files Created
1. **nq_price_action_analysis_01_07.py** - Main Python analysis script (514 lines)
2. **nq_session_range_distribution.png** - Visualization of session range distribution
3. **nq_session_timing_histogram.png** - Timing analysis of session highs and lows

## How to Run
```bash
python nq_price_action_analysis_01_07.py
```

### Prerequisites
- Python 3.x
- pandas
- numpy
- matplotlib

Install dependencies:
```bash
pip install pandas numpy matplotlib
```

## Analysis Results Summary

### Dataset
- **Total Sessions Analyzed**: 2,032
- **Date Range**: 2018-2025
- **Data Source**: 5-minute CSV files (semicolon-separated)
- **Time Window**: 01:00:00 to 07:00:00

### Key Findings

#### 1. Distribution of Returns (Directionality)
- **Bullish Sessions**: 1,082 (53.25%)
- **Bearish Sessions**: 950 (46.75%)
- **Average Session Return**: +1.48 points
- **Average Bullish Return**: +47.00 points
- **Average Bearish Return**: -50.35 points

**Conclusion**: Slight bullish bias, but essentially neutral market with balanced distribution.

#### 2. Volatility and Range Analysis
- **Average Session Range**: 101.89 points
- **Median Session Range**: 84.50 points
- **Standard Deviation**: 74.12 points

**Yearly Breakdown**:
| Year | Avg Range | Median Range | Std Dev |
|------|-----------|--------------|---------|
| 2018 | 51.94     | 42.83        | 30.71   |
| 2019 | 49.38     | 40.65        | 30.78   |
| 2020 | 118.01    | 100.13       | 81.11   |
| 2021 | 103.05    | 85.86        | 59.43   |
| 2022 | 155.45    | 141.87       | 74.32   |
| 2023 | 90.01     | 81.10        | 39.27   |
| 2024 | 105.94    | 96.96        | 57.30   |
| 2025 | 147.48    | 121.40       | 110.99  |

**Notable**: Significant volatility increase in 2020 (COVID), peak in 2022, and elevated levels in 2025.

#### 3. Timing of Session Extremes

**Session Highs**:
- First 15 minutes (01:00-01:15): 14.17%
- Last 15 minutes (06:45-07:00): 13.19%
- Peak formation: 06:45 interval (239 occurrences)
- Distribution relatively balanced across the session

**Session Lows**:
- First 15 minutes (01:00-01:15): 17.32% ⚠️
- Last 15 minutes (06:45-07:00): 11.02%
- Peak formation: 06:45 interval (202 occurrences)
- **Bias Detected**: Lows tend to form earlier in the session

**Insight**: First hour (01:00-02:00) shows 29.6% of session lows, indicating early morning weakness tendency.

#### 4. Day-of-Week Effects

| Day       | Avg Range | Median Range | Avg Return | Bullish % |
|-----------|-----------|--------------|------------|-----------|
| Monday    | 102.75    | 81.77        | +1.28      | 52.22%    |
| Tuesday   | 103.25    | 87.81        | +2.59      | 53.30%    |
| Wednesday | 97.47     | 83.16        | +5.89      | **55.67%** |
| Thursday  | 103.74    | 87.86        | +1.06      | 54.39%    |
| Friday    | 102.23    | 82.29        | -3.46      | 50.62%    |

**Key Observations**:
- **Wednesday** shows highest bullish probability (55.67%) and best average return (+5.89 points)
- **Friday** shows slightly bearish bias (-3.46 points average return)
- Range consistency across all days (~97-104 points)

#### 5. Open Drive Correlation

**Critical Finding**:
- When first candle (01:00) is **BULLISH**:
  - 941 total sessions
  - 559 closed bullish
  - **Probability: 59.40%** ✅

- When first candle (01:00) is **BEARISH**:
  - 1,091 total sessions
  - 523 closed bullish
  - Probability: 47.94%

**Conclusion**: **STRONG positive correlation detected**. A bullish first candle increases the probability of a bullish session close by 9.40 percentage points (from ~48% to ~59%).

## Trading Implications

### 1. Position Sizing
- Plan for average range of **~102 points**
- Consider median range of **~85 points** for conservative sizing
- Account for higher volatility in current market conditions (2025: 147 points avg)

### 2. Timing Strategy
- **First hour critical**: 29.6% of session lows occur in first hour (01:00-02:00)
- Monitor 01:00 candle direction for continuation bias
- Be aware of potential late-session moves (28.2% of highs in last hour)

### 3. Day Selection
- **Wednesday**: Highest probability day for bullish moves (55.67%)
- **Friday**: Exercise caution, slight bearish bias present
- All days show similar volatility/range characteristics

### 4. Open Drive Strategy
- **If 01:00 candle bullish**: Consider continuation plays (59.4% success rate)
- **Risk Management**: Still allows for 40.6% reversal scenarios
- Combine with other technical factors for higher confidence

### 5. General Guidelines
- Session provides significant intraday opportunity (~102 point average move)
- Early weakness often presents buying opportunities
- Strong directional bias from opening can persist through session
- Wednesday trading preferred for long bias

## Technical Implementation

### Data Processing
- Loads all years (2018-2025) from 5-minute CSV files
- Filters strictly to 01:00-07:00 time window
- Aggregates 5-minute bars into daily sessions
- Tracks timing of intraday extremes

### Analysis Methods
1. **Directionality**: Compares session open vs close
2. **Volatility**: Calculates high-low range with yearly breakdown
3. **Timing**: 15-minute interval histogram for highs/lows
4. **Day-of-Week**: Aggregates by weekday with multiple metrics
5. **Correlation**: Conditional probability analysis of first candle vs session

### Visualizations
- **Chart 1**: Histogram of session ranges with mean/median lines
- **Chart 2**: Dual histogram showing timing distribution of highs and lows

## Code Structure

```python
class NQSessionAnalyzer:
    - load_data()                    # Load and combine all CSV files
    - filter_session_window()        # Filter to 01:00-07:00
    - create_daily_sessions()        # Aggregate to daily sessions
    - analyze_directionality()       # Analysis #1
    - analyze_volatility()           # Analysis #2
    - analyze_timing_extremes()      # Analysis #3
    - analyze_day_of_week()          # Analysis #4
    - analyze_open_drive()           # Analysis #5
    - create_visualizations()        # Generate PNG charts
    - generate_synthesis()           # Print conclusions
    - run_complete_analysis()        # Execute all analyses
```

## Future Enhancements

Potential areas for extension:
1. Volume analysis during the session
2. Gap analysis (overnight vs session performance)
3. Volatility regime filtering (high vs low VIX periods)
4. Market context analysis (trend days vs range days)
5. Multiple timeframe confirmation
6. Machine learning prediction models
7. Real-time monitoring implementation

## Contact & Support

This analysis was created as a comprehensive backtesting tool for NQ futures trading during the 01:00-07:00 session window. The code is fully documented and ready for immediate use or further customization.

---

**Generated**: December 12, 2025  
**Data Period**: 2018-2025  
**Total Sessions**: 2,032  
**Programming Language**: Python 3.x

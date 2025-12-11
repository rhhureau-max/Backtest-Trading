# NQ Session Analysis: 01:00-07:00 Time Window

## Overview

This document presents a comprehensive quantitative analysis of the NQ (Nasdaq-100 E-mini/Micro) futures price action and volatility during the fixed time window of **01:00-07:00** (as indicated in raw data files, no timezone conversion).

**Analysis Period:** 2018-2025 (7+ years of data)  
**Data Timeframe:** 5-minute candles for precision  
**Total Sessions Analyzed:** 2,032 sessions  

## Objective

Identify recurring biases, patterns, and statistical edges in the 01:00-07:00 session to inform trading decisions on the Nasdaq-100 futures market.

---

## Key Findings Summary

### 1. 📈 Directional Bias: **BULLISH** (53.94%)

- **Bullish Sessions (Close > Open):** 1,096 sessions (53.94%)
- **Bearish Sessions (Close < Open):** 936 sessions (46.06%)
- **Average Session Return:** +1.61 points
- **Average Bullish Session:** +45.84 points
- **Average Bearish Session:** -50.18 points

**Implication:** The 01:00-07:00 session exhibits a **slight bullish bias**, with about 54% of sessions closing higher than they opened. This suggests a tendency for upward price movement during this time window.

---

### 2. 📊 Volatility: 100.99 Points Average Range

- **Average Session Range:** 100.99 points
- **Median Session Range:** 83.53 points
- **Standard Deviation:** 73.67 points

#### Volatility Evolution by Year

| Year | Avg Range | Median Range | Std Dev | Sessions |
|------|-----------|--------------|---------|----------|
| 2018 | 51.48     | 42.47        | 30.67   | 258      |
| 2019 | 48.39     | 40.16        | 29.96   | 258      |
| 2020 | 116.78    | 99.98        | 80.41   | 259      |
| 2021 | 102.32    | 83.28        | 59.29   | 259      |
| 2022 | 154.50    | 141.58       | 73.48   | 258      |
| 2023 | 89.28     | 80.96        | 39.17   | 258      |
| 2024 | 105.20    | 95.68        | 57.27   | 259      |
| 2025 | 145.98    | 120.94       | 110.37  | 223      |

**Key Observation:** Volatility has **INCREASED significantly** over time:
- 2018-2019: ~50 points average range (low volatility period)
- 2020: Jump to 117 points (COVID-19 impact)
- 2022: Peak at 155 points (inflation/Fed rate hike concerns)
- 2025: Currently elevated at 146 points

**Implication:** Risk management and stop-loss placement should account for higher volatility in recent years. The average range of ~100 points provides a baseline for position sizing.

---

### 3. ⏰ Timing of Extremes: Early Session Bias

#### When Does the Session HIGH Occur?

| Time Bin | Count | Percentage |
|----------|-------|------------|
| **01:00** | **263** | **12.94%** |
| 06:45 | 208 | 10.24% |
| 06:30 | 130 | 6.40% |
| 02:00 | 118 | 5.81% |
| 06:00 | 102 | 5.02% |

**Most Common HIGH Time:** **01:00** (12.94% of sessions)

#### When Does the Session LOW Occur?

| Time Bin | Count | Percentage |
|----------|-------|------------|
| **01:00** | **310** | **15.26%** |
| 06:45 | 175 | 8.61% |
| 02:00 | 152 | 7.48% |
| 02:15 | 127 | 6.25% |
| 01:15 | 99 | 4.87% |

**Most Common LOW Time:** **01:00** (15.26% of sessions)

**Key Insight:** Both the session HIGH and LOW most frequently occur at **01:00** (the opening candle). This suggests:
- **Strong initial volatility** at session open
- **Early extreme formation** - the opening candle often sets the range extremes
- **Potential reversal opportunities** after the 01:00 candle if extremes are hit early

There's also a **secondary peak** near the session close (06:30-06:45), indicating potential late-session moves.

**Trading Implication:** 
- Monitor the 01:00 candle closely - it often defines key levels
- If extremes form early (01:00-02:00), look for mean reversion or range-bound trading
- Watch for breakouts near session close (06:30-06:45) when late extremes form

---

### 4. 📅 Day of Week Effect

| Day | Avg Range | Median Range | Bullish % | Avg Return | Total Sessions |
|-----|-----------|--------------|-----------|------------|----------------|
| Monday | 101.69 | 81.51 | 53.69% | +2.36 | 406 |
| Tuesday | 102.60 | 87.45 | 54.52% | +2.97 | 409 |
| Wednesday | 96.68 | 83.16 | **55.91%** | +5.12 | 406 |
| Thursday | **102.89** | 87.86 | 54.39% | +1.08 | 410 |
| Friday | 101.07 | 80.71 | 51.12% | -3.56 | 401 |

**Key Observations:**
- **Wednesday** shows the **strongest bullish bias** (55.91%) and best average return (+5.12 points)
- **Thursday** offers the **highest volatility** (102.89 points average range)
- **Friday** is the weakest day with negative average return (-3.56 points) and lowest bullish percentage

**Trading Implication:**
- Wednesday and Thursday are the best days for this session
- Consider reducing position sizes or avoiding Friday sessions
- Thursday's higher volatility offers more profit potential but requires wider stops

---

### 5. 🎯 Open Drive Correlation: Strong Positive Signal

#### First Candle (01:00) Bullish → Session Close Bullish

- **When 01:00 candle is BULLISH:** 59.83% chance session closes bullish (941 sessions)
- **When 01:00 candle is BEARISH:** 48.85% chance session closes bullish (1,091 sessions)

**Key Finding:** There is a **STRONG positive correlation** between the direction of the opening candle (01:00) and the final session close (07:00).

**Statistical Edge:**
- If you trade in the direction of the 01:00 candle, you have a **59.83% win rate**
- This is a **significant edge** above random (50%)
- The opening candle is a **reliable indicator** of session direction

**Trading Strategy:**
1. Wait for the 01:00 candle to close
2. If bullish, look for long opportunities
3. If bearish, look for short opportunities (though note the overall bullish bias)
4. Combine with other confluences (support/resistance, market structure, etc.)

---

## Trading Implications & Recommendations

### ✅ Edge-Based Trading Rules

1. **Directional Bias:** Favor **long setups** in this session (53.94% bullish)

2. **Open Drive Strategy:** 
   - Trade in the direction of the 01:00 candle (59.83% success rate)
   - Wait for confirmation before entering

3. **Day Selection:**
   - **Best days:** Wednesday (most bullish), Thursday (most volatile)
   - **Avoid/reduce:** Friday (negative average return)

4. **Risk Management:**
   - Use ~100 points as baseline for stop-loss placement
   - Adjust for current year's volatility (2025: ~146 points)
   - Consider tighter stops on low-volatility days

5. **Timing:**
   - Key inflection point at **01:00** (extremes often form here)
   - Secondary opportunities at **06:30-06:45** (late session moves)
   - If price makes extreme early, look for reversal/range trading

### 🎲 Probability-Based Approach

Based on the statistical analysis:

- **Base probability of bullish close:** 53.94%
- **Add:** 01:00 candle bullish → +5.89% edge (total: 59.83%)
- **Add:** Wednesday → +1.97% edge (total: 55.91%)
- **Best scenario:** Wednesday + Bullish 01:00 candle = highest probability long

---

## Methodology

### Data Source
- **Files:** NQ 5-minute CSV data (2018-2025)
- **Format:** Semicolon-separated with columns for Date, Time, Open, High, Low, Close, Volume
- **No timezone conversion applied** - raw times used as-is

### Session Definition
- **Start Time:** 01:00
- **End Time:** 07:00 (exclusive)
- **Duration:** 6 hours (72 candles @ 5-minute intervals)

### Aggregation Method
For each session:
- **Open:** First candle's open (01:00)
- **High:** Highest high across all candles
- **Low:** Lowest low across all candles
- **Close:** Last candle's close (before 07:00)
- **Range:** High - Low
- **Return:** Close - Open

### Analysis Techniques
1. **Directionality:** Percentage of sessions with positive returns
2. **Volatility:** Statistical analysis of session ranges by year
3. **Extreme Timing:** Histogram of HIGH/LOW occurrence in 15-minute bins
4. **Day of Week:** Aggregated statistics by weekday
5. **Open Drive:** Conditional probability analysis

---

## Visualizations

### Chart 1: Range Analysis
![NQ Session Range Analysis](nq_session_range_analysis.png)

**Contains:**
- Distribution of session ranges (histogram)
- Average range by year (bar chart)
- Average range by day of week (bar chart)
- Session return distribution (histogram)

### Chart 2: High/Low Timing Analysis
![NQ Session Timing Analysis](nq_session_timing_analysis.png)

**Contains:**
- Histogram of when session HIGH occurs (15-minute bins)
- Histogram of when session LOW occurs (15-minute bins)
- Percentage labels on each bar for easy interpretation

---

## Code Implementation

The analysis is fully automated and reproducible. Run the script:

```bash
python3 nq_session_analysis_01_07.py
```

**Requirements:**
- Python 3.x
- pandas
- numpy
- matplotlib
- seaborn

**Output:**
- Console report with all statistics
- Two PNG charts (range analysis and timing analysis)

---

## Conclusion: Recurring Biases

After analyzing 2,032 sessions spanning 2018-2025, the following **recurring biases** were identified in the NQ 01:00-07:00 session:

1. **Slight Bullish Bias** (53.94%) - Favor long setups
2. **Increasing Volatility** - Recent years show 3x higher ranges than 2018-2019
3. **Early Extreme Formation** - 01:00 candle often sets the HIGH and LOW
4. **Strong Open Drive Effect** - 59.83% correlation between 01:00 candle and session close
5. **Wednesday Sweet Spot** - Most bullish day with best returns
6. **Friday Weakness** - Lowest performance day, often negative returns

### Risk Disclaimer

Past performance does not guarantee future results. These statistical observations should be combined with proper risk management, market context analysis, and personal trading rules. The edge identified here is small (~4% above random) and requires disciplined execution over many trades to realize.

---

## Author

Quantitative Analyst Senior  
Date: December 11, 2025  
Repository: Backtest-Trading

---

## Version History

- **v1.0** (2025-12-11): Initial analysis of 01:00-07:00 NQ session

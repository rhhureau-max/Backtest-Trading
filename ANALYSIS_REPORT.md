# Tokyo & London Session Analysis - NQ Futures (2018-2025)

## Executive Summary

This report presents a comprehensive quantitative analysis of the Tokyo and London trading sessions for Nasdaq Futures (NQ) from January 2018 to November 2025. The analysis examines market manipulation patterns and price behavior across specific intraday time windows.

---

## Methodology

### Session Definitions (File Time)

The analysis follows a strict protocol accounting for midnight crossover:

- **Tokyo Session**: 19:00 (J-1) to 01:00 (J) - 6 hours
- **Gap/Pre-London**: 01:00 to 02:00 - 1 hour  
- **London Manipulation Window (Judas Swing)**: 02:00 to 02:45 - 45 minutes
- **London Continuation/Distribution**: 02:45 to 05:00 - 2h15min

### Analysis Algorithm

For each trading day:

1. **Tokyo Range Calculation**
   - Identify the highest High and lowest Low between 19:00 (J-1) and 01:00 (J)
   - Calculate Equilibrium = (Tokyo High + Tokyo Low) / 2

2. **Manipulation Detection (02:00 - 02:45)**
   - **Bullish Manipulation (Buy Setup)**: Price breaks below Tokyo Low
   - **Bearish Manipulation (Sell Setup)**: Price breaks above Tokyo High
   - **Volatile**: Price breaks both levels

3. **Distribution Analysis (02:45 - 05:00)**
   - Track price revisits to key levels
   - Count retests of Tokyo boundaries and Equilibrium

### Data Specifications

- **Source**: 5-minute candlestick data
- **Period**: January 2, 2018 to November 11, 2025
- **Total Records**: 554,518 5-minute candles
- **Trading Days Analyzed**: 2,032 days

---

## Key Findings

### 1. Manipulation Frequency

**69.19% of trading days exhibit manipulation** during the 02:00-02:45 London opening window.

| Manipulation Type | Days | Percentage |
|-------------------|------|------------|
| **Bearish** (High broken) | 761 | 37.45% |
| **Bullish** (Low broken) | 612 | 30.12% |
| **Volatile/Both** | 33 | 1.62% |
| **None** | 626 | 30.81% |

**Key Insight**: Bearish manipulation (breaking Tokyo High) is **21% more frequent** than Bullish manipulation (breaking Tokyo Low).

### 2. Distribution of Manipulation Types

Among the 1,406 manipulated days:

- **Bearish**: 54.13%
- **Bullish**: 43.53%
- **Volatile**: 2.35%

### 3. Post-Manipulation Price Behavior (02:45-05:00)

#### Bullish Manipulation (Tokyo Low Broken)
*Sample Size: 612 days*

| Metric | Result |
|--------|--------|
| Days with Equilibrium retest | 36.44% (223 days) |
| Average Equilibrium retests | 1.84 per day |
| Days with Tokyo Low retest | **61.76%** (378 days) |
| Average Tokyo Low retests | 3.30 per day |

**Interpretation**: After a bullish manipulation (break below Tokyo Low), the price returns to retest the Tokyo Low level in **61.76% of cases**, often multiple times (average 3.30 retests). The Equilibrium is less frequently visited (36.44%).

#### Bearish Manipulation (Tokyo High Broken)
*Sample Size: 761 days*

| Metric | Result |
|--------|--------|
| Days with Equilibrium retest | 29.96% (228 days) |
| Average Equilibrium retests | 1.43 per day |
| Days with Tokyo High retest | **65.44%** (498 days) |
| Average Tokyo High retests | 3.66 per day |

**Interpretation**: After a bearish manipulation (break above Tokyo High), the price returns to retest the Tokyo High level in **65.44% of cases**, with even more frequent retests (average 3.66). The Equilibrium is visited in about 30% of cases.

#### Volatile Days (Both Levels Broken)
*Sample Size: 33 days*

| Metric | Average Retests |
|--------|-----------------|
| Equilibrium retests | 3.79 |
| Tokyo Low retests | 3.00 |
| Tokyo High retests | 2.85 |

**Interpretation**: On highly volatile days where both Tokyo High and Low are breached during manipulation, all key levels see significantly more price interaction, particularly the Equilibrium.

---

## Trading Implications

### High-Probability Setups

1. **Retest Reliability**: After manipulation, there is a **61-65% probability** that price will retest the breached Tokyo level during the London Continuation phase (02:45-05:00).

2. **Bearish Bias**: The market shows a slight bearish bias with more frequent upside manipulation (54% vs 43%).

3. **Multiple Retests**: When retests occur, they tend to happen multiple times (3-4 times on average), suggesting strong magnet behavior at these levels.

4. **Equilibrium Plays**: The Equilibrium is less frequently visited (30-36%) compared to the extreme levels, but when it is visited on volatile days, it becomes a very active zone.

### Risk Considerations

- **30.81% of days show no manipulation**: Not every day follows the manipulation pattern
- Volatile days (1.62%) require different risk management due to unpredictable price action
- Weekend gaps and low-liquidity sessions may reduce pattern reliability

---

## Statistical Summary

```
╔════════════════════════════════════════════════════════════╗
║   TOKYO & LONDON SESSION ANALYSIS - NQ FUTURES            ║
╠════════════════════════════════════════════════════════════╣
║   Analysis Period: 2018-01-02 to 2025-11-11              ║
║   Trading Days Analyzed: 2,032                            ║
║   Total 5m Candles: 554,518                               ║
╠════════════════════════════════════════════════════════════╣
║   MANIPULATION FREQUENCY                                   ║
║   - Total Manipulated Days: 1,406 (69.19%)               ║
║   - Bearish: 761 days (37.45%)                           ║
║   - Bullish: 612 days (30.12%)                           ║
║   - Volatile: 33 days (1.62%)                            ║
║   - No Manipulation: 626 days (30.81%)                   ║
╠════════════════════════════════════════════════════════════╣
║   RETEST STATISTICS (LONDON CONTINUATION 02:45-05:00)    ║
║                                                            ║
║   Bullish Manipulation (n=612):                           ║
║   • Tokyo Low retest: 61.76% of days (avg 3.30 retests) ║
║   • Equilibrium retest: 36.44% of days (avg 1.84 retests)║
║                                                            ║
║   Bearish Manipulation (n=761):                           ║
║   • Tokyo High retest: 65.44% of days (avg 3.66 retests)║
║   • Equilibrium retest: 29.96% of days (avg 1.43 retests)║
╚════════════════════════════════════════════════════════════╝
```

---

## Files Generated

1. **tokyo_london_session_analysis.py** - Complete Python analysis script
2. **tokyo_london_analysis_results.csv** - Detailed daily results (2,032 rows)
3. **tokyo_london_analysis_results_summary.txt** - Quick summary statistics
4. **ANALYSIS_REPORT.md** - This comprehensive report

---

## Conclusion

This quantitative analysis reveals consistent and exploitable patterns in the NQ Futures market structure:

1. **Manipulation is the norm, not the exception** - Occurring on 69% of trading days
2. **Retests are highly probable** - 61-65% retest rate of breached Tokyo levels
3. **Multiple retest opportunities** - Average 3-4 retests when they occur
4. **Bearish manipulation dominates** - 54% of manipulated days break the Tokyo High

These findings support the "Judas Swing" concept and provide a quantitative foundation for intraday trading strategies based on Tokyo Range manipulation and London continuation patterns.

---

*Analysis completed: December 4, 2025*  
*Script: tokyo_london_session_analysis.py*  
*Data integrity: 100% - All years from 2018-2025 processed successfully*

# Quick Start Guide - ICT London Silver Bullet OTE Backtest

## Overview

This repository contains a complete backtest implementation of the **ICT London Silver Bullet / OTE (Optimal Trade Entry)** strategy for the NQ (Nasdaq 100) futures market.

## Files

| File | Description |
|------|-------------|
| `ict_london_silver_bullet_ote.py` | Main backtest engine - runs the complete strategy |
| `ict_visualize_results.py` | Detailed analysis and reporting tool |
| `ict_london_silver_bullet_results.csv` | Trade-by-trade results export |
| `ICT_LONDON_SILVER_BULLET_README.md` | Comprehensive strategy documentation |
| `QUICK_START.md` | This file |

## Running the Backtest

### Prerequisites

```bash
pip install pandas numpy
```

### Execute the Backtest

```bash
python3 ict_london_silver_bullet_ote.py
```

**Processing time**: ~2-3 minutes for 554k rows of data

**Output**: 
- Console report with performance metrics
- `ict_london_silver_bullet_results.csv` with 578 trades

### Run Detailed Analysis

```bash
python3 ict_visualize_results.py
```

**Output**: Extended analysis including:
- Consecutive win/loss streaks
- Monthly performance breakdown
- Trade duration analysis
- FVG impact comparison
- Day of week patterns
- Tokyo range size effects
- Equity curve progression

## Quick Results Summary

### Performance Metrics

| Metric | Value |
|--------|-------|
| **Total Trades** | 578 |
| **Win Rate** | 18.37% |
| **Profit Factor** | 2.23 |
| **Net Profit** | +3,768.73 points |
| **Max Drawdown** | 4.39% |
| **Avg RR Ratio** | 11.24:1 |
| **Avg Win** | +65.87 points |
| **Avg Loss** | -6.81 points |

### Best Performance

- **Best Year**: 2021 (+924.13 pts, 25.61% WR)
- **Best Hour**: 02:00 Chicago (+1,444.41 pts, 23.03% WR)
- **Best Day**: Friday (+1,149 pts, 20.9% WR)
- **Best Month**: October 2023 (+338.80 pts, 50% WR)

## Strategy Logic

```
IF during London Killzone (01:00-05:00):
  1. Price sweeps BELOW Tokyo_Low
  2. Price breaks back ABOVE Tokyo_Low (MSS)
  3. Price retraces to 70.5% Fibonacci level
  4. Tokyo_High NOT broken yet
  
THEN:
  ENTER LONG at 70.5% Fib
  SL: 1 point below 89% Fib
  TP: Tokyo_High
```

## Key Insights

### ✅ Strengths
- **Asymmetric Payoff**: 11.24:1 avg risk/reward
- **Consistent**: Profitable in 7 out of 8 years
- **Low Drawdown**: Only 4.39% max drawdown
- **High Execution**: 97% of winners hit TP exactly

### ⚠️ Challenges
- **Low Win Rate**: Only 18.37% (4 out of 5 trades lose)
- **Loss Streaks**: Up to 31 consecutive losses
- **Psychology**: Requires extreme discipline
- **Time-Limited**: Only 4-hour trading window daily

### 🔍 Surprising Findings
- **FVG Not Required**: Setups without FVG perform better (2.85 vs 2.26 PF)
- **Winners Take Time**: Avg 133 minutes to hit TP
- **Losers Exit Fast**: Avg 45 minutes to hit SL
- **Friday Best**: Highest profit and win rate

## Data Requirements

The backtest expects NQ 5-minute CSV files in the format:
```
YYYY 5m.csv
```

Example files in repository:
- `2018 5m.csv` through `2025 5m.csv`

**CSV Format**:
- Delimiter: semicolon (`;`)
- Columns: Date, Time, Open, High, Low, Close, Volume
- Date format: DD/MM/YYYY
- Time format: HH:MM:SS
- Timezone: America/Chicago (no conversion needed)

## Customization

### Modify Strategy Parameters

Edit `ict_london_silver_bullet_ote.py`:

```python
# Tokyo session times (line 108)
tokyo_mask = (data['Hour'] >= 19) & (data['Hour'] < 23)

# London session times (line 113)
london_mask = (data['Hour'] >= 1) & (data['Hour'] < 5)

# OTE entry level (line 294)
fib_705 = impulse_high - (fib_range * 0.705)  # Change 0.705 to your preference

# Stop loss level (line 296)
fib_89 = impulse_high - (fib_range * 0.89)  # Change 0.89 to your preference
```

### Test Different Markets

Replace the CSV file loading section (line 34-56) to load different market data in the same format.

## Next Steps

1. **Read Full Documentation**: See `ICT_LONDON_SILVER_BULLET_README.md`
2. **Analyze Results**: Use `ict_visualize_results.py`
3. **Optimize Parameters**: Try different Fibonacci levels
4. **Add Filters**: Implement H1 MSS or daily bias filters
5. **Test Other Markets**: Apply to ES, YM, RTY, or forex pairs

## Support

For questions or issues:
1. Check `ICT_LONDON_SILVER_BULLET_README.md` for detailed explanations
2. Review the code comments in the Python files
3. Examine `ict_london_silver_bullet_results.csv` for trade examples

## Disclaimer

This backtest is for educational and research purposes only. Past performance does not guarantee future results. Always test strategies thoroughly on demo accounts before risking real capital.

---

**Data Period**: January 2018 - November 2025 (554,518 bars)  
**Market**: NQ (Nasdaq 100 Futures)  
**Timeframe**: 5-minute bars  
**Timezone**: America/Chicago

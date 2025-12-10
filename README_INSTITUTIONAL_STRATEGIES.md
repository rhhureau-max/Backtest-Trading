# 5 Institutional Daily Bias Strategies - Backtest System

## Overview

Comprehensive backtesting system for 5 institutional trading methodologies on NQ and ES futures. Tests daily bias determination strategies from 2018 to present across multiple timeframes.

## Strategies Tested

### Strategy 1: Market Profile 80% Rule (Value Area)
**Hypothesis:** Detect bias reversal or continuation  
**Logic:**
- Calculate Value Area (70% of volume range) from previous day
- If price opens outside VA but returns inside with 2 consecutive 30m closes
- **Signal:** Bias toward opposite end of VA (e.g., if enters from top, short to VA Low)

**Expected Win Rate:** ~80% (Dalton/Steidlmayer)  
**Actual Win Rate (NQ 2018-2025):** 53.45%

**Results:**
- Total Trades: 174
- Profit Factor: 1.10
- Net Profit: +656 points
- Max Drawdown: 814 points

---

### Strategy 2: Liquidity Sweep & Reclaim (ICT/Turtle Soup)
**Hypothesis:** Bias reversal after external liquidity grab  
**Logic:**
- Identify Previous Day High (PDH) and Low (PDL)
- If price breaks PDH/PDL during session but closes 4H candle back inside previous day range
- **Signal:** Immediate reversal (false breakout)

**Expected Win Rate:** ~65-70%  
**Actual Win Rate (NQ 2018-2025):** 51.37%

**Results:**
- Total Trades: 1,164
- Profit Factor: 0.97
- Net Profit: -1,794 points
- Max Drawdown: 5,269 points

---

### Strategy 3: Opening Range Breakout (ORB) with Trend Filter
**Hypothesis:** Momentum/continuation bias  
**Logic:**
- Define opening range: first 15 minutes of US session (09:30-09:45 EST)
- **Trend Filter:** Above SMA20 daily = only long breakouts, below = only short
- Entry on breakout of OR high/low, stop at opposite end

**Expected Win Rate:** ~60-65% (NQ specific)  
**Actual Win Rate (NQ 2018-2025):** 33.04%

**Results:**
- Total Trades: 1,925
- Profit Factor: 1.01
- Net Profit: +151 points
- Max Drawdown: 771 points

---

### Strategy 4: Gap Fill (Mean Reversion)
**Hypothesis:** Inefficiency filling  
**Logic:**
- Identify gap > 0.5% from previous settlement
- If gap not filled in first 30 minutes
- **Signal:** Fade the gap when reversal candle appears

**Expected Win Rate:** ~62% (ES/NQ historical)  
**Actual Win Rate (NQ 2018-2025):** 51.11%

**Results:**
- Total Trades: 45
- Profit Factor: 1.29
- Net Profit: +608 points
- Max Drawdown: 879 points

---

### Strategy 5: Structural Alignment 4H/1D (Trend Following)
**Hypothesis:** The trend is your friend  
**Logic:**
- **1D:** Price must be above EMA20
- **4H:** Price must make Higher High (HH) and Higher Low (HL)
- **Signal:** Buy pullback to EMA20 on 4H if 1D condition met (inverse for sells)

**Expected Win Rate:** ~55% (but high R:R > 1:2)  
**Actual Win Rate (NQ 2018-2025):** 66.88% ✅

**Results:**
- Total Trades: 1,905
- Profit Factor: 1.15
- Net Profit: +14,089 points (BEST)
- Max Drawdown: 8,006 points

---

## Installation & Usage

### Requirements
```bash
pip install pandas numpy
```

### Running the Backtest
```bash
python institutional_bias_backtest.py
```

### Programmatic Usage
```python
from institutional_bias_backtest import InstitutionalBiasBacktester

# Initialize backtester
backtester = InstitutionalBiasBacktester(
    symbol='NQ',
    start_date='2018-01-01',
    csv_dir='.'
)

# Run all strategies
results = backtester.run_all_strategies()

# Or run individual strategies
results_1 = backtester.strategy_1_market_profile_80_rule()
results_2 = backtester.strategy_2_liquidity_sweep_reclaim()
results_3 = backtester.strategy_3_opening_range_breakout()
results_4 = backtester.strategy_4_gap_fill()
results_5 = backtester.strategy_5_structural_alignment()
```

## Data Requirements

The script expects CSV files in the following format (semicolon-separated):
- `YYYY 1D.csv` - Daily data
- `YYYY 4H.csv` - 4-hour data
- `YYYY 15m.csv` - 15-minute data
- `YYYY 5m.csv` - 5-minute data

CSV Format:
```
Column1;Column2;Column3;Column4;Column5;Column6;Column7
DD/MM/YYYY;HH:MM:SS;Open;High;Low;Close;Volume
```

## Key Findings

### Performance Summary (NQ 2018-2025)

| Strategy | Trades | Win Rate | PF | Net PnL | Max DD | vs Expected |
|----------|--------|----------|-------|---------|--------|-------------|
| **Market Profile 80%** | 174 | 53.45% | 1.10 | +656 pts | 814 pts | -26.55% |
| **Liquidity Sweep** | 1,164 | 51.37% | 0.97 | -1,794 pts | 5,269 pts | -16.13% |
| **ORB** | 1,925 | 33.04% | 1.01 | +151 pts | 771 pts | -29.46% |
| **Gap Fill** | 45 | 51.11% | 1.29 | +608 pts | 879 pts | -10.89% |
| **Structural Alignment** | 1,905 | **66.88%** | 1.15 | **+14,089 pts** | 8,006 pts | **+11.88%** ✅ |

### Key Insights

1. **Strategy 5 (Structural Alignment) OUTPERFORMED expectations**
   - Only strategy to exceed theoretical win rate
   - Highest net profit: +14,089 points
   - 66.88% win rate vs 55% expected
   - Best for trend-following NQ markets

2. **Strategy 3 (ORB) UNDERPERFORMED significantly**
   - 33.04% win rate vs 62.5% expected
   - Low R:R compensates (2:1 targets)
   - Still barely profitable (+151 points)
   - Needs refinement or tighter filters

3. **Strategy 2 (Liquidity Sweep) NEGATIVE**
   - Only losing strategy overall
   - High trade frequency (1,164 trades) amplifies losses
   - 51.37% win rate insufficient for breakeven
   - May require tighter entry filters or better R:R

4. **Strategy 4 (Gap Fill) BEST PROFIT FACTOR**
   - 1.29 PF (highest among all)
   - Low frequency (45 trades = selective)
   - 51.11% win rate with good R:R
   - Reliable but rare setup

5. **Strategy 1 (Market Profile) MODERATE**
   - 53.45% win rate (below 80% theory)
   - Small positive edge (+656 points)
   - 174 trades = reasonable frequency
   - Value Area calculation may need refinement

### Recommendations

**For Live Trading:**
1. **Primary:** Strategy 5 (Structural Alignment) - proven edge
2. **Secondary:** Strategy 4 (Gap Fill) - high selectivity, good PF
3. **Avoid:** Strategy 2 (Liquidity Sweep) until refined
4. **Refine:** Strategy 3 (ORB) with additional filters

**Improvements Needed:**
- Strategy 1: Improve VA calculation (use actual volume distribution)
- Strategy 2: Add confluence filters, tighten stops
- Strategy 3: Add volatility filter, refine entry timing
- Strategy 4: Already working well, just rare
- Strategy 5: Already excellent, consider position sizing

## Technical Details

### Architecture
```
InstitutionalBiasBacktester
├── load_data() - Multi-timeframe data loading
├── strategy_1_market_profile_80_rule()
├── strategy_2_liquidity_sweep_reclaim()
├── strategy_3_opening_range_breakout()
├── strategy_4_gap_fill()
├── strategy_5_structural_alignment()
├── _check_trade_outcome() - Stop/target logic
├── _calculate_statistics() - Metrics computation
└── run_all_strategies() - Full backtest pipeline
```

### Metrics Calculated
- **Win Rate:** Percentage of winning trades
- **Profit Factor:** Gross profit / Gross loss
- **Max Drawdown:** Largest peak-to-trough decline
- **Net Profit/Loss:** Total points gained/lost
- **Average Win/Loss:** Mean profit per winning/losing trade
- **Average Bars Held:** Mean duration of trades

## Limitations

1. **Slippage/Commission:** Not included (assumes perfect fills)
2. **Market Profile:** Simplified VA calculation (no true volume profile)
3. **Execution:** Assumes immediate fills at breakout prices
4. **Data Quality:** Depends on CSV data accuracy
5. **Survivorship Bias:** Uses historical data (no forward testing)

## Future Enhancements

1. Add slippage/commission simulation
2. Implement true Volume Profile calculations
3. Add Monte Carlo simulation for robustness
4. Include walk-forward optimization
5. Add real-time signal generation
6. Multi-asset correlation analysis (NQ vs ES divergence)
7. Machine learning for entry/exit optimization

## References

- **Market Profile:** Dalton, J. & Steidlmayer, P. "Mind Over Markets"
- **ICT Concepts:** Inner Circle Trader methodology
- **ORB:** Toby Crabel "Opening Range Breakout"
- **Gap Theory:** Classic technical analysis literature
- **Trend Following:** Various systematic trading research

## Author

Senior Quantitative Analyst - NQ & ES Futures Specialist  
Date: 2025-12-10

## License

For educational and research purposes only. Not financial advice.

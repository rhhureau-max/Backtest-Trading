# ICT London Open Backtest - Quick Start Guide

## 🚀 Quick Start (5 Minutes)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Ensure Data Files Are Present
Your data directory should contain:
```
2018 5m.csv, 2018 15m.csv, 2018 1H.csv, 2018 4H.csv
2019 5m.csv, 2019 15m.csv, 2019 1H.csv, 2019 4H.csv
...
2025 5m.csv, 2025 15m.csv, 2025 1H.csv, 2025 4H.csv
```

### Step 3: Run the Backtest
```bash
python ict_london_open_backtest.py
```

### Step 4: Review Results
The script will generate:
- **ict_london_open_trades.csv** - Detailed trade log
- **ict_london_open_results.png** - Performance charts
- **ict_london_open_annual.png** - Annual performance

## 📊 Understanding the Results

### Key Metrics Explained

**Win Rate**: Percentage of winning trades
- 46.21% means nearly half of trades are winners
- ICT strategies often have lower win rates but higher reward/risk

**Profit Factor**: Gross Profit ÷ Gross Loss
- 1.88 means you make $1.88 for every $1 lost
- Above 1.5 is considered good for systematic strategies

**Expectancy**: Average expected profit per trade
- $210.08 means each trade has positive expected value
- This is the "edge" of the strategy

**Max Drawdown**: Largest peak-to-trough decline
- 14.02% is moderate and manageable
- Important for position sizing and risk management

## 🎯 Strategy at a Glance

### What It Does
Finds ICT London Open setups where:
1. **FVG forms** before London session (the pivot)
2. **Judas Swing** sweeps Tokyo liquidity through the FVG
3. **Inversion** occurs - price reverses back through FVG
4. **MSS** confirms the new direction

### When It Trades
- **Entry Window**: 01:00-05:00 NY time (London Open)
- **Best Hour**: 3:00 AM (66.67% win rate)
- **Active Days**: All weekdays, Thursday best performer

### Trade Characteristics
- **Average Winner**: $973 (48.6 NQ points)
- **Average Loser**: -$446 (22.3 NQ points)
- **Risk/Reward**: ~2.2:1 ratio
- **Trade Frequency**: ~17 trades per year

## 📈 Performance Highlights (2018-2025)

### Best Years
1. **2022**: +$8,957 (28 trades)
2. **2025**: +$8,450 (22 trades, partial year)
3. **2023**: +$7,924 (18 trades, 77.8% win rate!)

### Best Times
- **Hour 3 (3:00 AM)**: +$12,342 across 30 trades
- **Hour 4 (4:00 AM)**: +$5,467 across 25 trades
- **Thursday**: +$9,844 across 27 trades

### Challenging Periods
- **2024**: -$3,787 (market regime change)
- **2018**: -$919 (strategy ramp-up period)
- **Hour 1 (1:00 AM)**: -$2,196 (too early)

## 🔍 Trade Log Analysis

### Opening the Trade Log
```bash
# View first 10 trades
head -11 ict_london_open_trades.csv | column -t -s,

# Count trades by year
awk -F, 'NR>1 {print $13}' ict_london_open_trades.csv | sort | uniq -c

# Calculate win rate
awk -F, 'NR>1 {total++; if($9=="win") wins++} END {print wins/total*100 "%"}' ict_london_open_trades.csv
```

### Key Columns in Trade Log
- **date**: Trade date
- **direction**: bullish/bearish
- **entry_time**: When entry was filled
- **entry_price**: Actual entry price
- **exit_time**: When trade closed
- **exit_price**: Exit price (stop or target)
- **outcome**: win/loss
- **points_pnl**: Profit/loss in NQ points
- **dollar_pnl**: Profit/loss in dollars ($20/point)
- **tokyo_high/low**: Session liquidity levels

## 🎨 Reading the Charts

### Equity Curve (Top Left)
- **Upward slope**: Strategy is profitable over time
- **Smooth line**: Consistent performance
- **Steep drops**: Drawdown periods to analyze

### Drawdown Chart (Top Right)
- **Red area**: Capital under water
- **Flat at zero**: New equity highs
- **Depth**: Risk exposure during bad periods

### Win/Loss Distribution (Bottom Left)
- **Green bar**: Number of winning trades
- **Red bar**: Number of losing trades
- **Height comparison**: Win rate visualization

### P&L Distribution (Bottom Right)
- **Right side of zero**: Winning trades
- **Left side of zero**: Losing trades
- **Shape**: Shows trade outcome clustering

## ⚙️ Customization Examples

### Change Date Range
```python
backtest = ICTLondonOpenBacktest(
    data_dir='/path/to/data',
    start_year=2022,  # Start from 2022
    end_year=2024     # End at 2024
)
```

### Adjust FVG Minimum Size
```python
# In __init__ method
self.fvg_min_size = 3.0  # Require larger FVGs (more selective)
```

### Modify Slippage
```python
# In __init__ method
self.slippage = 1.0  # More conservative slippage assumption
```

### Change Stop Loss Buffer
```python
# In simulate_trade method
stop_loss = setup['judas_swing']['high'] + 3.0  # Wider stop
```

## 🐛 Troubleshooting

### "No trades found"
- Check that CSV files exist for all years
- Verify data includes Tokyo session (19:00-00:00) and London session (01:00-05:00)
- Reduce `fvg_min_size` parameter if too restrictive

### "Data loading error"
- Ensure semicolon delimiter in CSV files
- Check date format: DD/MM/YYYY
- Verify file naming: "YYYY 5m.csv" format

### Charts not displaying
- Install matplotlib: `pip install matplotlib`
- Check file permissions in output directory
- Verify seaborn is installed

### Low win rate in specific year
- Normal variation in market conditions
- 2024 shows regime change impact
- Consider filtering by H1/4H bias (future enhancement)

## 📚 Next Steps

### 1. Analyze Individual Trades
```python
import pandas as pd
trades = pd.read_csv('ict_london_open_trades.csv')

# View losing trades
losing_trades = trades[trades['outcome'] == 'loss']
print(losing_trades[['date', 'direction', 'points_pnl', 'hour']])

# Best winning trades
best_wins = trades.nlargest(10, 'dollar_pnl')
print(best_wins[['date', 'direction', 'dollar_pnl']])
```

### 2. Test Parameter Sensitivity
- Run with `fvg_min_size = 1.5, 2.0, 2.5, 3.0`
- Compare results across different settings
- Find optimal balance between trade frequency and quality

### 3. Forward Test
- Run backtest up to 2024 only
- Use 2025 as out-of-sample test
- Compare in-sample vs out-of-sample performance

### 4. Risk Management
- Calculate position size based on max drawdown
- Example: $50k account, 14% max DD = ~$7k risk
- Use 1-2% risk per trade = $500-$1000 per trade
- Position size = Risk / Stop Distance

## 💡 Pro Tips

### Identifying High-Quality Setups
1. **Look for clean FVGs**: Large, obvious gaps work best
2. **Strong Judas Swings**: Clear liquidity sweep above/below Tokyo range
3. **Decisive Inversions**: Quick, aggressive reversal candles
4. **Clear MSS**: Obvious break of structure, not marginal

### Optimizing Entry Timing
- Hour 3 (3:00 AM) has highest win rate (66.67%)
- Avoid Hour 1 (1:00 AM) - too early, poor performance
- Thursday best weekday performance
- Consider waiting for optimal time windows

### Managing Drawdowns
- 2024 shows -$3,787 loss year
- Strategy bounced back strong in 2025
- Keep reserves for drawdown periods
- Don't over-leverage in good years

### Documentation
- Keep a trading journal with setup screenshots
- Note market conditions (VIX, news events)
- Track which setups work best in different regimes
- Review monthly/quarterly performance

## 🎓 Learning Resources

### Understanding ICT Concepts
- Fair Value Gaps (FVG): Price inefficiencies
- Judas Swing: False breakout/liquidity grab
- Inversion: Change in market structure
- Market Structure Shift (MSS): Trend confirmation

### Key Principles
1. **Liquidity**: Markets seek liquidity before reversing
2. **FVG Respect**: Efficient markets fill gaps
3. **Session Dynamics**: London reverses Asian moves
4. **Time of Day**: Specific hours show patterns

## 📞 Support

### Common Questions

**Q: Why 46% win rate?**
A: ICT strategies prioritize high reward/risk over high win rate. 2.2:1 R/R means you can profit with <50% wins.

**Q: Why did 2024 perform poorly?**
A: Market regime changes affect all strategies. The positive expectancy shows edge remains over full cycle.

**Q: Can I use this live?**
A: This is for educational purposes. Always paper trade first and use proper risk management.

**Q: What about 1m data?**
A: Currently uses 5m for execution. 1m could improve entry timing but increases complexity.

**Q: How to reduce drawdown?**
A: Consider adding H1/4H bias filter, avoiding low-probability hours, or reducing position size.

---

## ✅ Success Checklist

- [ ] Dependencies installed
- [ ] Data files present and formatted correctly
- [ ] Backtest runs without errors
- [ ] Trade log CSV generated
- [ ] Charts generated successfully
- [ ] Results match expectations (~132 trades, ~$27k profit)
- [ ] Understand key metrics
- [ ] Reviewed best/worst periods
- [ ] Analyzed trade log for patterns
- [ ] Ready to customize or forward test

---

**Happy Backtesting! 🎉**

Remember: This is a complex, sophisticated strategy. Take time to understand each component, analyze the results thoroughly, and always prioritize risk management over returns.

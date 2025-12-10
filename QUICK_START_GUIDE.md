# Quick Start Guide - ICT Liquidity Sweep Reversal Strategy

## 🚀 Running the Analysis

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the Analyzer
```bash
python3 ict_liquidity_sweep_reversal.py
```

### Step 3: View Results
The script generates detailed reports:
- `ICT_Liquidity_Sweep_Reversal_Report_2024.txt` (15m timeframe, full year)
- `ICT_Liquidity_Sweep_Reversal_Report_5m_Dec2024.txt` (5m timeframe, December)

## 📊 Understanding the Output

Each setup in the report shows:

```
SETUP #745
--------------------------------------------------------------------------------
📅 Date/Time: 2024-07-22 10:00:00 EDT    ← When the setup occurred
⏱️  Timeframe: 15m                       ← Chart timeframe
🎯 Killzone: NY Open                     ← London or NY session
💰 Price: 20,797.61                      ← NQ price at setup

🔄 LIQUIDITY SWEEP:
   Type: Buy Side Liquidity              ← Buy or Sell side sweep
   Sweep Level: 20,710.71                ← Level that was swept
   Expected Direction: Bearish Reversal  ← Predicted move direction

✨ SWEEP QUALITY:
   Quality: Good                         ← Excellent/Good/Poor
   Type: Rejection Wick                  ← Wick rejection or body breakout
   Wick Ratio: 40.7%                     ← How much was wick vs body

📊 SMT DIVERGENCE:
   ✓ Confirmed: Bearish SMT Divergence   ← NQ vs ES divergence
   NQ: Higher High                       ← NQ direction
   ES: Double Top                        ← ES direction
   Probability: Medium                   ← High or Medium

⚡ DISPLACEMENT & MSS:
   ✓ Displacement: Detected (candle +1)  ← Impulsive move found
   MSS: ✓ Yes                            ← Market structure break
   Strength: Strong                      ← Strong or Moderate

📍 FAIR VALUE GAP (FVG):
   ✓ Detected: Bearish FVG               ← Price imbalance found
   Gap Range: 20,720.37 - 20,762.64      ← FVG zone for entry
   Gap Size: 42.27 (0.20%)               ← Gap size

🎲 OVERALL ASSESSMENT:
   Probability: Very High                ← Very High/High/Medium
   Score: 7/9                            ← Total points scored
   Factors:
     • Quality: Good                     ← Contributing factors
     • SMT: Medium Probability
     • Displacement: Strong + MSS
     • FVG: Present
```

## 🎯 Trading the Setup

### Entry Options
1. **Aggressive**: Enter immediately on displacement candle close
2. **Conservative**: Wait for pullback to FVG zone (better risk/reward)

### Stop Loss
- **Bearish Setup**: Place stop above the sweep high + 10-20 points
- **Bullish Setup**: Place stop below the sweep low - 10-20 points

### Take Profit
- **Target 1**: FVG fill (partial profit)
- **Target 2**: Previous swing level
- **Target 3**: Next major structure

### Position Sizing
| Probability | Risk % | Notes |
|-------------|--------|-------|
| Very High (7-9) | 2.0% | Rare, strong edge |
| High (5-6) | 1.5% | Good opportunity |
| Medium (3-4) | 1.0% | Trade with caution |

## 📈 Filtering Setups

### Priority 1: Very High Probability (7-9 points)
- Only 0.4% of all setups (5 in 2024)
- All factors aligned
- Strongest edge
- Focus here first

### Priority 2: High Probability (5-6 points)
- 16.8% of all setups (221 in 2024)
- Most factors aligned
- Good risk/reward
- Main trading pool

### Priority 3: Medium Probability (3-4 points)
- 82.8% of all setups (1,087 in 2024)
- Some confirmation
- Optional, use sparingly

## 🔍 What to Look For

### Best Setups Have:
✓ Excellent sweep quality (strong rejection wick)
✓ SMT divergence confirmed
✓ Strong displacement with MSS
✓ Clear FVG for entry

### Warning Signs:
⚠️ Poor sweep quality (full body breakout)
⚠️ No SMT divergence
⚠️ Weak displacement
⚠️ No FVG for entry refinement

## 🛠️ Customization

Edit these parameters in `ict_liquidity_sweep_reversal.py`:

```python
# Killzone times (line 39-40)
self.london_killzone = (time(2, 0), time(5, 0))
self.ny_killzone = (time(9, 30), time(11, 0))

# Swing detection (line 43-44)
self.swing_lookback_15m = 20  # More = fewer, stronger swings
self.swing_lookback_1h = 10

# SMT tolerance (line 47)
self.smt_tolerance = 0.002  # 0.2% for double tops/bottoms

# Displacement minimum (line 50)
self.min_displacement_pct = 0.003  # 0.3% minimum move
```

## 📚 Further Reading

- `README_ICT_LIQUIDITY_SWEEP_REVERSAL.md` - Complete strategy documentation
- `IMPLEMENTATION_SUMMARY.md` - Results analysis and examples
- `ICT_Top_Setups_Examples.txt` - Best scoring setups from 2024

## ⚠️ Disclaimer

This is an educational tool for strategy research. Always:
- Practice on paper/demo first
- Use proper risk management
- Never risk more than you can afford to lose
- Past performance doesn't guarantee future results

## 🆘 Troubleshooting

**Problem**: Script fails with "File not found"
**Solution**: Ensure CSV files are in the same directory as the script

**Problem**: No setups found
**Solution**: Check date range - only shows setups in killzones

**Problem**: Different results than expected
**Solution**: Verify timezone is set to America/New_York

## 💡 Tips

1. Start with reviewing Very High probability setups only
2. Study the patterns - what makes them score high?
3. Compare 15m vs 5m - different trading styles
4. Use FVG zones for better entry timing
5. Journal your trades and compare with the analysis

---

Happy Trading! 📈

# ICT Risk Management Calculator - Summary

## 📊 Overview

This calculator provides precise entry and exit parameters for ICT Liquidity Sweep Reversal setups, with separate analysis for London and New York killzones.

## 🎯 Entry Point Strategy

**Entry Type:** LIMIT ORDER at FVG Proximal Line

- **For Bullish Reversals:** Entry at bottom of FVG (gap start)
- **For Bearish Reversals:** Entry at top of FVG (gap start)
- **Fallback:** If no FVG, use close of sweep candle

## 🛑 Stop Loss Scenarios

### Scenario A - Conservative
- **Location:** Extreme of the sweep wick (absolute high/low)
- **Advantage:** Wider stop, less likely to get stopped out
- **Disadvantage:** Larger risk per trade, fewer contracts possible

### Scenario B - Aggressive (Body-Based)
- **Location:** Edge of candle body (open/close, ignoring wick)
- **Advantage:** Tighter stop, more contracts possible
- **Disadvantage:** Higher probability of stop-out from wick touches

## 💰 Take Profit Levels

For both scenarios, three risk/reward ratios calculated:
- **RR 1:1** - Quick profit target
- **RR 1:1.5** - Balanced target
- **RR 1:2** - Extended target

All targets calculated in:
- NQ points
- USD value ($20 per point)

## 📈 Best Setups by Killzone

### 🌍 LONDON KILLZONE (01:00-04:00 CSV Time)

**Best Setup Details:**
```
Date:       2024-01-08 03:30:00 EST
Direction:  LONG (Bullish Reversal)
Score:      6/9 (High Probability)
Entry:      17,583.95 NQ

SCENARIO A (Conservative):
├─ Stop Loss:    17,557.69
├─ Risk:         26.26 points ($525.29)
├─ TP 1:1:       17,610.22 (+26.26 pts)
├─ TP 1:1.5:     17,623.35 (+39.40 pts)
└─ TP 1:2:       17,636.48 (+52.53 pts)

SCENARIO B (Aggressive):
├─ Stop Loss:    17,581.54
├─ Risk:         2.41 points ($48.24)
├─ TP 1:1:       17,586.36 (+2.41 pts)
├─ TP 1:1.5:     17,587.57 (+3.62 pts)
└─ TP 1:2:       17,588.78 (+4.82 pts)

Position Sizing (2% risk on $100K):
• Scenario A: 3 contracts
• Scenario B: 41 contracts
```

**Statistics:**
- Total Setups Found: 596
- Best Score: 6/9 (High Probability)
- Setup Quality: Strong rejection wick with FVG confirmation

---

### 🗽 NEW YORK KILLZONE (08:30-11:00 CSV Time)

**Best Setup Details:**
```
Date:       2024-07-22 10:00:00 EDT
Direction:  SHORT (Bearish Reversal)
Score:      7/9 (Very High Probability)
Entry:      20,762.64 NQ

SCENARIO A (Conservative):
├─ Stop Loss:    20,873.54
├─ Risk:         110.90 points ($2,218.04)
├─ TP 1:1:       20,651.74 (-110.90 pts)
├─ TP 1:1.5:     20,596.29 (-166.35 pts)
└─ TP 1:2:       20,540.84 (-221.80 pts)

SCENARIO B (Aggressive):
├─ Stop Loss:    20,828.40
├─ Risk:         65.76 points ($1,315.16)
├─ TP 1:1:       20,696.88 (-65.76 pts)
├─ TP 1:1.5:     20,664.00 (-98.64 pts)
└─ TP 1:2:       20,631.12 (-131.52 pts)

Position Sizing (2% risk on $100K):
• Scenario A: 0 contracts (risk too high)
• Scenario B: 1 contract
```

**Statistics:**
- Total Setups Found: 717
- Best Score: 7/9 (Very High Probability)
- Setup Quality: Strong rejection + SMT + Displacement with MSS + FVG

---

## 📊 Killzone Comparison

| Metric | London Killzone | NY Killzone |
|--------|----------------|-------------|
| **Total Setups** | 596 | 717 |
| **Best Score** | 6/9 | 7/9 |
| **Best Direction** | LONG | SHORT |
| **Entry Price** | 17,583.95 | 20,762.64 |
| **Risk (Scenario A)** | 26.26 pts | 110.90 pts |
| **Risk (Scenario B)** | 2.41 pts | 65.76 pts |
| **Quality** | High | Very High |

## 🎓 Usage Recommendations

### When to Use Scenario A (Conservative)
- Lower probability setups (Medium: 3-4/9)
- Volatile market conditions
- Larger account size allowing bigger stops
- You prefer wider stops for peace of mind

### When to Use Scenario B (Aggressive)
- Higher probability setups (High/Very High: 5-9/9)
- Stable market conditions
- Smaller account size requiring tighter risk
- You can tolerate occasional wick-outs

### Position Sizing Formula
```
Contracts = (Account × Risk%) / (Stop Loss Distance × $20)

Example for NY Setup (Scenario B):
Contracts = ($100,000 × 2%) / (65.76 × $20)
         = $2,000 / $1,315.16
         = 1.52 → 1 contract (round down)
```

## 📁 Generated Reports

1. **ICT_Risk_Management_London.txt**
   - Detailed analysis of best London setup
   - Top 5 other London setups
   - Complete risk parameters

2. **ICT_Risk_Management_NewYork.txt**
   - Detailed analysis of best NY setup
   - Top 5 other NY setups
   - Complete risk parameters

3. **ICT_Risk_Management_Combined.txt**
   - Best setup from all killzones
   - Cross-killzone comparison

## 🚀 Running the Calculator

```bash
# Generate fresh reports
python3 ict_risk_management_calculator.py

# View London report
cat ICT_Risk_Management_London.txt

# View New York report
cat ICT_Risk_Management_NewYork.txt
```

## ⚠️ Risk Disclaimer

These are educational calculations based on historical data. Always:
- Practice on paper/demo first
- Use proper risk management (1-2% per trade)
- Adjust position sizing for your account size
- Consider market conditions
- Never risk more than you can afford to lose

---

**Last Updated:** December 10, 2025  
**Data Period:** Full year 2024  
**Timeframe:** 15-minute charts

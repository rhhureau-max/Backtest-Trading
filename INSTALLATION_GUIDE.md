# Installation and Setup Guide

## Complete Installation Steps for TradingView

### Prerequisites
- TradingView account (Free or Premium)
- Access to NQ (Nasdaq 100) futures data
- Basic understanding of TradingView interface

---

## Step-by-Step Installation

### 1. Access TradingView

Visit [https://www.tradingview.com/](https://www.tradingview.com/) and log in to your account.

### 2. Open the Chart

1. Click on "Chart" at the top of the page
2. In the symbol search box (top left), type: **NQ1!** or **NQ**
3. Select the Nasdaq 100 futures contract
4. Set the timeframe to **5 minutes** (use the dropdown near the top)

### 3. Open Pine Editor

1. Look at the bottom of your screen
2. Click on "Pine Editor" tab
3. If you don't see it, click on the {} icon at the bottom toolbar

### 4. Create New Script

1. In Pine Editor, click "New" button (or press Ctrl+N / Cmd+N)
2. This will open a blank script template
3. Delete all the default template code

### 5. Copy the Strategy Code

1. Open the file `NQ_IVFG_Strategy.pine` from this repository
2. Select ALL the code (Ctrl+A / Cmd+A)
3. Copy it (Ctrl+C / Cmd+C)

### 6. Paste and Save

1. Return to TradingView Pine Editor
2. Paste the code (Ctrl+V / Cmd+V)
3. Give your script a name at the top (e.g., "NQ IVFG Strategy")
4. Click "Save" button (or Ctrl+S / Cmd+S)

### 7. Add to Chart

1. Click the "Add to Chart" button in Pine Editor
2. The strategy should now appear on your chart
3. You should see:
   - A yellow line (4H EMA 20)
   - A performance table in the bottom right
   - Strategy name at the top left of the chart

---

## Initial Configuration

### 8. Access Strategy Settings

1. Look for the strategy name on the chart (top left area)
2. Click on the ⚙️ (gear/settings) icon next to the strategy name
3. A settings window will open

### 9. Configure Basic Settings

Go to the **"Inputs"** tab and configure:

```
Time Window Filter:
├─ Start Hour: 1
├─ Start Minute: 0
├─ End Hour: 5
└─ End Minute: 0

Multi-Timeframe Trend Filter:
├─ Higher Timeframe: 240
├─ EMA Length: 20
└─ Use Trend Filter: ✓ (checked)

IVFG Signal Parameters:
├─ FVG Memory (Lookback Bars): 12
└─ Minimum FVG Size: 0

Risk Management Mode:
└─ Risk Management Mode: Mode A - Structural

Mode A - Structural:
├─ Safety Buffer (ticks): 5
└─ Risk/Reward Ratio: 2.0

Display Options:
├─ Show FVG Boxes: ✓ (checked)
├─ Show 4H EMA: ✓ (checked)
└─ Show Performance Table: ✓ (checked)
```

### 10. Configure Strategy Properties

Go to the **"Properties"** tab:

```
General:
├─ Initial Capital: 100000
├─ Base Currency: USD
├─ Order Size: 100% of equity (or your preference)
└─ Commission: 2.5 per contract

Execution:
├─ Verify Price for Limit Orders: ✓
├─ Fill Limit Orders on Order Price: [ ] (unchecked)
├─ Do Not Counter Trend: [ ] (unchecked)
└─ Recalculate: On Every Tick (for live trading) or On Bar Close (for backtesting)
```

### 11. Set Date Range

Go to the **"Settings"** (or **"Properties"**) tab:

```
Backtesting Range:
├─ From: 2018-01-01
└─ To: (Current date) or leave blank for all data
```

Click **"OK"** to apply all settings.

---

## Verification

### 12. Check Strategy is Working

You should now see:

✅ **Yellow line** on chart (4H EMA 20)  
✅ **Green and red boxes** (FVG zones) if detected  
✅ **Green/red arrows** (entry signals) if conditions are met  
✅ **Performance table** in bottom right corner  
✅ **Strategy Tester** tab at bottom showing results

### 13. View Strategy Results

1. Click on "Strategy Tester" tab at the bottom
2. Go to "Overview" tab to see:
   - Net Profit
   - Total Trades
   - Win Rate
   - Profit Factor
   - Max Drawdown
   - And more...

3. Go to "Performance Summary" tab for detailed metrics
4. Go to "List of Trades" tab to see individual trades

---

## Troubleshooting

### Problem: "Script cannot be compiled"

**Solution:**
- Make sure you copied ALL the code, including the first line `//@version=5`
- Check for any copy-paste errors
- Try copying the code again

### Problem: "No trades appearing"

**Solutions:**
1. Check your date range includes 2018-2025
2. Verify time window settings (01:00-05:00)
3. Check "Use Trend Filter" is enabled
4. Try temporarily setting time window to full day (0-23)
5. Ensure your chart timezone is set correctly

### Problem: "Cannot see FVG boxes"

**Solutions:**
1. Check "Show FVG Boxes" is enabled in settings
2. Zoom out on the chart (FVGs might be small)
3. Wait for FVGs to form (they need specific conditions)

### Problem: "EMA line not showing"

**Solutions:**
1. Check "Show 4H EMA" is enabled in settings
2. The line should be yellow - check if it's behind price bars
3. Try adjusting chart colors/theme

### Problem: "Performance table not visible"

**Solutions:**
1. Check "Show Performance Table" is enabled
2. Look in bottom-right corner of chart
3. Try scrolling the chart or adjusting zoom
4. Table only shows when there's data to display

---

## Advanced Configuration

### Timezone Setup (Important!)

The strategy uses RAW chart time without timezone conversion.

To ensure correct time window:

1. Click on chart settings (⚙️ near top right)
2. Go to "Symbol" tab
3. Check "Timezone" setting
4. For London Killzone (01:00-05:00):
   - Use Exchange Timezone, or
   - Use GMT+0 / UTC
   - Adjust Start/End hours in strategy settings if using different timezone

### Optimization (for experienced users)

1. In strategy settings, click on "Optimization" tab
2. Select parameters to optimize (e.g., EMA Length, Risk Reward Ratio)
3. Set ranges and step sizes
4. Click "Optimize"
5. Review results and select best parameters

⚠️ **Warning**: Don't over-optimize! This can lead to curve-fitting.

---

## Next Steps

### After Installation:

1. **Backtest**: Run the strategy on historical data (2018-2025)
2. **Analyze**: Review the performance metrics
3. **Optimize**: Try different parameter combinations (see USAGE_EXAMPLES.md)
4. **Paper Trade**: Test with paper trading (TradingView paper trading account)
5. **Go Live**: Only after successful paper trading with real-time data

### Recommended Reading Order:

1. ✅ **INSTALLATION_GUIDE.md** (this file) - Setup
2. 📖 **QUICK_REFERENCE.md** - Parameter overview
3. 📊 **VISUAL_GUIDE.md** - Understand the logic
4. 📚 **STRATEGY_DOCUMENTATION.md** - Detailed explanation (French)
5. 💡 **USAGE_EXAMPLES.md** - Configuration examples

---

## Video Tutorial (If Available)

[TradingView Pine Script Tutorial](https://www.tradingview.com/pine-script-docs/en/v5/Introduction.html)

---

## Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review the VISUAL_GUIDE.md for strategy logic
3. Consult USAGE_EXAMPLES.md for different configurations
4. Open an issue on the GitHub repository

---

## Important Reminders

⚠️ **Before Live Trading:**

- [ ] Backtested on at least 3 years of data
- [ ] Paper traded for at least 1 month
- [ ] Understand all strategy parameters
- [ ] Have proper risk management plan
- [ ] Only risk money you can afford to lose
- [ ] Understand that past performance ≠ future results

🎯 **Success Checklist:**

- [ ] Strategy installed and showing on chart
- [ ] Can see EMA line, FVG boxes, and signals
- [ ] Performance table displays metrics
- [ ] Strategy Tester shows historical trades
- [ ] Understand entry/exit logic
- [ ] Configured timezone correctly
- [ ] Set appropriate risk parameters

---

## Quick Start Checklist

```
[ ] 1. Open TradingView
[ ] 2. Load NQ 5-minute chart
[ ] 3. Open Pine Editor
[ ] 4. Create new script
[ ] 5. Copy & paste strategy code
[ ] 6. Save script
[ ] 7. Add to chart
[ ] 8. Configure settings (use defaults for now)
[ ] 9. Verify strategy is working (see signals/table)
[ ] 10. Review backtesting results
[ ] 11. Read documentation files
[ ] 12. Start paper trading
```

---

**Congratulations!** You're now ready to use the NQ IVFG Strategy! 🎉

Remember: **Start with paper trading and never risk more than you can afford to lose.**

Happy Trading! 📈

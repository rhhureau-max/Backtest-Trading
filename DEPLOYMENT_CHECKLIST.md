# Deployment Checklist

Use this checklist to ensure you properly deploy and test the NQ IVFG Strategy.

## Pre-Deployment

### Understanding Phase
- [ ] Read INSTALLATION_GUIDE.md completely
- [ ] Review VISUAL_GUIDE.md to understand IVFG logic
- [ ] Scan QUICK_REFERENCE.md for parameter overview
- [ ] Review at least 3 examples from USAGE_EXAMPLES.md
- [ ] Understand the 3 risk management modes

### Account Setup
- [ ] Have active TradingView account (any plan)
- [ ] Can access NQ (Nasdaq 100) futures data
- [ ] Understand your broker's commission structure
- [ ] Have paper trading account ready for testing

## Installation

### TradingView Setup
- [ ] Open TradingView and log in
- [ ] Load NQ symbol on chart
- [ ] Set timeframe to 5 minutes
- [ ] Verify date range includes 2018-2025
- [ ] Check timezone settings (UTC/GMT preferred)

### Strategy Installation
- [ ] Open Pine Editor in TradingView
- [ ] Create new script
- [ ] Copy all code from NQ_IVFG_Strategy.pine
- [ ] Paste into Pine Editor (verify first line is //@version=5)
- [ ] Save script with meaningful name
- [ ] Click "Add to Chart"
- [ ] Verify strategy appears on chart

### Visual Verification
- [ ] Yellow EMA line visible on chart
- [ ] Performance table visible (bottom right)
- [ ] Strategy name shown (top left)
- [ ] No error messages displayed

## Configuration

### Initial Settings (Use Defaults First)
- [ ] Time Window: 01:00-05:00 (London Killzone)
- [ ] Higher Timeframe: 240 (4 hours)
- [ ] EMA Length: 20
- [ ] Use Trend Filter: ON (checked)
- [ ] FVG Memory: 12 bars
- [ ] Risk Mode: Mode A - Structural
- [ ] Risk/Reward Ratio: 2.0
- [ ] Safety Buffer: 5 ticks
- [ ] Show all visual elements: ON

### Strategy Properties
- [ ] Initial Capital: $100,000 (or your actual capital)
- [ ] Commission: 2.5 per contract (adjust to your broker)
- [ ] Slippage: 2 ticks (adjust based on experience)
- [ ] Order Size: 100% (or more conservative like 10-20%)

### Timezone Configuration
- [ ] Verify chart timezone matches your target session
- [ ] Adjust Start/End hours if using different timezone
- [ ] Document your timezone settings for reference

## Testing Phase 1: Historical Backtest

### Run Initial Backtest
- [ ] Set date range: 2018-01-01 to current
- [ ] Run strategy on entire period
- [ ] Wait for all calculations to complete
- [ ] Open Strategy Tester tab

### Record Baseline Metrics
- [ ] Total Trades: ________
- [ ] Win Rate: ________%
- [ ] Profit Factor: ________
- [ ] Max Drawdown: $________
- [ ] Net Profit: $________
- [ ] Largest Win: $________
- [ ] Largest Loss: $________
- [ ] Average Trade: $________

### Analyze Results
- [ ] Win Rate between 40-60%? (Good)
- [ ] Profit Factor > 1.3? (Acceptable)
- [ ] Max Drawdown < 20%? (Acceptable)
- [ ] Net Profit positive? (Required)
- [ ] Review individual trades in "List of Trades"
- [ ] Identify any patterns in losing trades

### Visual Inspection
- [ ] Review at least 20 entry signals on chart
- [ ] Verify FVG boxes appear correctly
- [ ] Check EMA line makes sense
- [ ] Confirm entry signals align with strategy logic
- [ ] Look for any obvious errors or anomalies

## Testing Phase 2: Parameter Optimization (Optional)

### Mode Comparison
- [ ] Test Mode A with RR 1.5, 2.0, 2.5
- [ ] Test Mode B with different SL/TP values
- [ ] Test Mode C with different ATR multipliers
- [ ] Record results for each configuration
- [ ] Choose best-performing mode for your style

### Parameter Tuning (One at a Time!)
- [ ] Test EMA lengths: 15, 20, 25, 30
- [ ] Test lookback periods: 8, 10, 12, 15
- [ ] Test different time windows
- [ ] Test with/without trend filter
- [ ] Document all results

### Out-of-Sample Testing
- [ ] Optimize on 2018-2021 data
- [ ] Test on 2022-2023 data
- [ ] Verify similar performance
- [ ] Final test on 2024-2025 data

## Testing Phase 3: Forward Testing

### Paper Trading Setup
- [ ] Switch to paper trading account
- [ ] Load strategy with optimized parameters
- [ ] Verify strategy is running
- [ ] Set up alerts (optional)
- [ ] Start monitoring

### Daily Monitoring (Minimum 1 Month)
- [ ] Check strategy daily during trading window
- [ ] Record each trade taken
- [ ] Document entry/exit prices
- [ ] Track actual slippage/commissions
- [ ] Compare to backtest expectations
- [ ] Keep trading journal

### Weekly Review (During Paper Trading)
- [ ] Calculate weekly metrics
- [ ] Compare to backtest results
- [ ] Identify any discrepancies
- [ ] Adjust if necessary (document changes)
- [ ] Continue monitoring

## Pre-Live Checklist

### Performance Validation
- [ ] Paper traded for minimum 30 days
- [ ] At least 20 trades executed
- [ ] Win Rate within 10% of backtest
- [ ] Profit Factor within 20% of backtest
- [ ] No major unexpected issues
- [ ] Comfortable with max drawdown

### Risk Management
- [ ] Position sizing plan documented
- [ ] Maximum daily loss limit set
- [ ] Maximum weekly loss limit set
- [ ] Emergency exit plan defined
- [ ] Understand worst-case scenario
- [ ] Only using risk capital

### Broker Setup
- [ ] Live account funded
- [ ] NQ futures tradable
- [ ] Commission structure confirmed
- [ ] Platform fees understood
- [ ] Order types available (market, limit, stop)
- [ ] Can monitor positions easily

### Psychological Preparation
- [ ] Understand strategy will have losing streaks
- [ ] Comfortable with max drawdown
- [ ] Can follow strategy without emotional decisions
- [ ] Have plan for when things go wrong
- [ ] Not over-leveraged or stressed
- [ ] Ready to start small and scale up

## Go-Live Phase

### Initial Live Trading
- [ ] Start with minimum position size (1 contract)
- [ ] Trade for 2 weeks at minimum size
- [ ] Record all trades meticulously
- [ ] Compare to paper trading results
- [ ] Verify actual costs match expectations
- [ ] Monitor psychological response

### Scaling Up (If Successful)
- [ ] Minimum 2 weeks profitable at minimum size
- [ ] Increase position size gradually (10-20% at a time)
- [ ] Continue monitoring closely
- [ ] Keep detailed trading journal
- [ ] Review performance weekly
- [ ] Scale up only if comfortable

## Ongoing Maintenance

### Daily Tasks
- [ ] Check strategy is running (if automated)
- [ ] Monitor trades during session
- [ ] Record any issues or anomalies
- [ ] Update trading journal

### Weekly Tasks
- [ ] Calculate weekly metrics
- [ ] Compare to expected performance
- [ ] Review all trades
- [ ] Identify patterns
- [ ] Check if market conditions changed
- [ ] Decide if adjustments needed

### Monthly Tasks
- [ ] Full performance review
- [ ] Compare to backtest metrics
- [ ] Calculate Sharpe ratio (if possible)
- [ ] Review max drawdown
- [ ] Consider parameter adjustments
- [ ] Document any changes made

### Quarterly Tasks
- [ ] Comprehensive strategy review
- [ ] Re-run optimization on recent data
- [ ] Consider market regime changes
- [ ] Update documentation
- [ ] Review risk management
- [ ] Plan for next quarter

## Emergency Procedures

### If Strategy Stops Working
- [ ] Stop live trading immediately
- [ ] Review recent trades
- [ ] Check if market conditions changed
- [ ] Verify no coding errors
- [ ] Re-backtest on recent data
- [ ] Consider if strategy needs update
- [ ] Don't resume until issue understood

### If Large Drawdown Occurs
- [ ] Reduce position size by 50%
- [ ] Review losing trades
- [ ] Check if hitting stops properly
- [ ] Verify strategy logic still valid
- [ ] Consider taking break
- [ ] Re-evaluate risk parameters
- [ ] Don't chase losses

### If Technical Issues
- [ ] Have backup plan (manual trading)
- [ ] Know how to close all positions
- [ ] Have broker phone number handy
- [ ] Document all issues
- [ ] Test fixes in paper account first
- [ ] Don't trade if uncertain

## Success Metrics

### Short-term (First Month)
- [ ] Strategy executes as expected
- [ ] Win rate within reasonable range
- [ ] No major technical issues
- [ ] Comfortable with strategy
- [ ] Following plan consistently

### Medium-term (3-6 Months)
- [ ] Positive returns
- [ ] Profit factor > 1.3
- [ ] Drawdowns manageable
- [ ] Consistent performance
- [ ] Comfortable scaling position size

### Long-term (1 Year+)
- [ ] Consistent profitability
- [ ] Understand strategy deeply
- [ ] Can adapt to market changes
- [ ] Have confidence in system
- [ ] Trading without emotional stress

## Final Reminders

### Always Remember
- [ ] Past performance ≠ future results
- [ ] Markets change, strategies must adapt
- [ ] Risk management is crucial
- [ ] Never risk more than you can afford to lose
- [ ] Keep learning and improving
- [ ] Trading is a marathon, not a sprint

### Red Flags (Stop Trading If...)
- [ ] Win rate drops below 30%
- [ ] Profit factor drops below 1.0
- [ ] Drawdown exceeds your limit
- [ ] Strategy behaving unexpectedly
- [ ] Feeling emotional or stressed
- [ ] Not following your plan

### Green Lights (Continue Trading)
- [ ] Strategy performing as expected
- [ ] Following your plan consistently
- [ ] Comfortable with results
- [ ] Managing risk properly
- [ ] Keeping good records
- [ ] Learning from each trade

---

## Completion Date

- [ ] Checklist completed on: _______________
- [ ] Signed off by: _______________________
- [ ] Ready for next phase: ________________

---

**Good luck with your trading journey!**

Remember: Discipline, patience, and proper risk management are keys to long-term success.

For questions, review:
- **INSTALLATION_GUIDE.md** - Setup help
- **USAGE_EXAMPLES.md** - Configuration ideas
- **STRATEGY_DOCUMENTATION.md** - Deep dive (French)
- **VISUAL_GUIDE.md** - Strategy logic

📊 **Trade Safe! Trade Smart!** 📈

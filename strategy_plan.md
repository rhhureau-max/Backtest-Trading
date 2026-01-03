# NQ ICT Backtesting Strategy Implementation Plan

## Components to Build:

### 1. Data Loading Module (data_loader.py)
- [ ] Load and combine CSV files for each timeframe (1m, 5m, 1H, 4H)
- [ ] Handle semicolon-separated format
- [ ] Extract zipped 1-minute files
- [ ] Parse dates and times correctly (Chicago timezone)
- [ ] Create unified DataFrame with proper datetime index

### 2. Market Structure Detection (market_structure.py)
- [ ] Implement Higher High (HH) and Higher Low (HL) detection
- [ ] Implement Lower High (LH) and Lower Low (LL) detection
- [ ] Use sliding window of 20 candles
- [ ] Determine bullish/bearish trend on H1 and H4

### 3. FVG Detection (fvg_detector.py)
- [ ] Detect Bearish FVG: candle[i-2].Low > candle[i].High
- [ ] Detect Bullish FVG: candle[i-2].High < candle[i].Low
- [ ] Track FVG zones for entry signals

### 4. Entry Logic (entry_signals.py)
- [ ] Identify 08:30 opening range on 5-minute chart
- [ ] Detect breakout and return to range
- [ ] Generate entry signals based on FVG inversion
- [ ] Apply trend filter (only LONG in bullish, SHORT in bearish)

### 5. Risk Management (risk_manager.py)
- [ ] Implement fixed 20-point stop loss
- [ ] Split positions into 3 parts (TP1: 20pts, TP2: 30pts, TP3: 40pts)
- [ ] Track individual trade outcomes

### 6. Backtesting Engine (backtest_engine.py)
- [ ] Main execution loop
- [ ] Trade tracking and management
- [ ] Performance metrics calculation

### 7. Results & Analytics (results_analyzer.py)
- [ ] Calculate overall statistics
- [ ] Year-by-year performance
- [ ] Separate Long vs Short analysis
- [ ] Generate comprehensive report

### 8. Main Script (run_backtest.py)
- [ ] Orchestrate all components
- [ ] Execute complete backtest
- [ ] Output results

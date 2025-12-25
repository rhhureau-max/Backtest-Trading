# Technical Specification - FVG C.E. Strategy Implementation

## Architecture Overview

### Core Components

1. **Data Loading Module**
   - Multi-file CSV loader with pattern matching
   - Automatic date/time parsing (DD/MM/YYYY HH:MM:SS)
   - Duplicate removal and validation
   - Semicolon delimiter handling

2. **Indicator Calculation**
   - FVG detection (vectorized)
   - C.E. level calculation
   - ATR calculation for Model 3

3. **Setup Management Engine**
   - Forward-fill propagation logic
   - Setup cancellation detection
   - Entry trigger simulation (limit orders)

4. **Position Management System**
   - Real-time SL/TP monitoring
   - Session-based entry control
   - Hard exit implementation

5. **Performance Analytics**
   - Trade-by-trade P&L tracking
   - Drawdown calculation
   - Exit reason classification

## Algorithm Flow

```
1. LOAD DATA
   ├─> Load multiple CSV files by year
   ├─> Parse dates/times
   ├─> Combine and sort
   └─> Validate OHLC data

2. IDENTIFY FVG
   ├─> Detect Bullish FVG (High[i-2] < Low[i])
   ├─> Detect Bearish FVG (Low[i-2] > High[i])
   ├─> Calculate C.E. levels (50% midpoint)
   └─> Store reference candle data

3. CALCULATE RISK LEVELS
   ├─> Model 1: FVG border-based (3:1 R:R)
   ├─> Model 2: Swing candle-based (fixed TP)
   └─> Model 3: ATR-based (dynamic)

4. MANAGE SETUPS
   ├─> Forward-fill C.E. and SL levels
   ├─> Check for SL breach (cancel setup)
   ├─> Check for C.E. touch (trigger entry)
   └─> Validate session time

5. MANAGE POSITIONS
   ├─> Track active position
   ├─> Monitor SL hit (exit at SL)
   ├─> Monitor TP hit (exit at TP)
   └─> Force exit at 08:00 (exit at Close)

6. CALCULATE METRICS
   ├─> Aggregate trade results
   ├─> Compute statistics
   ├─> Generate visualizations
   └─> Export trade logs
```

## Data Structures

### Main DataFrame Columns

```python
# Original OHLC Data
'DateTime', 'Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume'

# Time Components
'TimeOnly'  # Time object for session filtering

# FVG Detection
'High_i2', 'Low_i2'  # Lagged values
'Bullish_FVG', 'Bearish_FVG'  # Binary flags
'Long_CE', 'Short_CE'  # C.E. price levels

# Risk Management
'Long_SL', 'Long_TP_temp'  # Long trade levels
'Short_SL', 'Short_TP_temp'  # Short trade levels
'ATR'  # For Model 3

# Setup Management
'Active_Long_CE', 'Active_Long_SL', 'Active_Long_TP'
'Active_Short_CE', 'Active_Short_SL', 'Active_Short_TP'
'In_Session'  # Boolean flag

# Entry Signals
'Long_Entry', 'Short_Entry'  # Binary flags
'Long_Entry_Price', 'Short_Entry_Price'  # Exact entry prices

# Position Tracking
'Position'  # 1=Long, -1=Short, 0=Flat
'Position_Entry_Price', 'Position_SL', 'Position_TP'
'Exit_Price', 'Exit_Reason', 'PnL'
```

## Key Algorithms

### FVG Detection (Vectorized)

```python
# Bullish FVG: High[i-2] < Low[i]
df['Bullish_FVG'] = (df['High'].shift(2) < df['Low']).astype(int)

# Bearish FVG: Low[i-2] > High[i]
df['Bearish_FVG'] = (df['Low'].shift(2) > df['High']).astype(int)

# C.E. Calculation
df['Long_CE'] = (df['High'].shift(2) + df['Low']) / 2
df['Short_CE'] = (df['Low'].shift(2) + df['High']) / 2
```

### Limit Order Simulation

```python
# Entry triggered when:
# 1. Price bar touches C.E. level
# 2. Within trading session

if df.at[i, 'Low'] <= ce <= df.at[i, 'High'] and df.at[i, 'In_Session']:
    entry_triggered = True
    entry_price = ce  # Exact C.E. level, not close
```

### Setup Cancellation

```python
# Cancel long setup if price breaks below SL before entry
if df.at[i, 'Low'] <= sl:
    setup_cancelled = True
    clear_active_setup()

# Cancel short setup if price breaks above SL before entry
if df.at[i, 'High'] >= sl:
    setup_cancelled = True
    clear_active_setup()
```

### Exit Logic Priority

```python
1. Check Hard Exit Time (08:00) - Highest Priority
   └─> Exit at Close price

2. Check Stop Loss
   └─> Exit at SL level (assumed filled)

3. Check Take Profit
   └─> Exit at TP level (assumed filled)
```

## Risk Model Specifications

### Model 1: Aggressive Sniper

```python
# Stop Loss
SL_Long = High[i-2] - FVG_MARGIN  # 2 points below distal
SL_Short = Low[i-2] + FVG_MARGIN  # 2 points above distal

# Take Profit
risk_long = Long_CE - SL_Long
TP_Long = Long_CE + (3 * risk_long)  # 3x risk

risk_short = SL_Short - Short_CE
TP_Short = Short_CE - (3 * risk_short)  # 3x risk
```

### Model 2: Structural Defender

```python
# Stop Loss
SL_Long = Low[i] - FVG_MARGIN  # Below FVG candle low
SL_Short = High[i] + FVG_MARGIN  # Above FVG candle high

# Take Profit
TP_Long = Long_CE + MODEL2_TP  # Fixed 40 points
TP_Short = Short_CE - MODEL2_TP  # Fixed 40 points
```

### Model 3: Volatility Adapter

```python
# Calculate ATR
ATR = calculate_atr(df, period=14)

# Stop Loss
SL_Long = Long_CE - (ATR_SL_MULT * ATR)  # 1.5 * ATR
SL_Short = Short_CE + (ATR_SL_MULT * ATR)  # 1.5 * ATR

# Take Profit
TP_Long = Long_CE + (ATR_TP_MULT * ATR)  # 3.0 * ATR
TP_Short = Short_CE - (ATR_TP_MULT * ATR)  # 3.0 * ATR
```

## Performance Considerations

### Optimizations Applied

1. **Vectorized Operations**: NumPy/pandas operations where possible
2. **Efficient Indexing**: Direct `.at[]` access in loops
3. **Lazy Evaluation**: Only calculate needed columns
4. **Memory Management**: Drop unnecessary columns after use

### Computational Complexity

- **FVG Detection**: O(n) - single pass with vectorization
- **Setup Management**: O(n) - iterative forward-fill
- **Position Management**: O(n) - single pass through data
- **Overall**: O(n) where n = number of candles

### Memory Usage

- **Input Data**: ~100MB for 500k candles
- **Working Set**: ~200MB with all indicators
- **Peak Usage**: ~300MB during calculations

## Testing & Validation

### Unit Test Coverage

✅ CSV loading and parsing  
✅ FVG detection accuracy  
✅ C.E. calculation precision  
✅ Setup cancellation logic  
✅ Entry trigger detection  
✅ Exit logic priority  
✅ P&L calculation  

### Edge Cases Handled

1. **Missing Data**: Rows with NaN dropped safely
2. **Duplicate Timestamps**: Keep first occurrence
3. **Invalid Dates**: Coerced and filtered
4. **Zero Volume**: Allowed (not filtered)
5. **Extreme Prices**: No artificial limits
6. **Session Boundaries**: Exact time comparisons
7. **Multiple Setups**: Only newest setup active

## Configuration Parameters

### Critical Parameters

```python
SESSION_START = time(1, 0, 0)    # Entry window start
SESSION_END = time(5, 0, 0)      # Entry window end
HARD_EXIT_TIME = time(8, 0, 0)   # Force exit time
RISK_MODEL = 2                    # 1, 2, or 3
TIMEFRAME = '5m'                  # Data granularity
```

### Risk Parameters

```python
FVG_MARGIN = 2         # SL buffer (points)
MODEL2_TP = 40         # Fixed TP (points)
ATR_PERIOD = 14        # ATR lookback
ATR_SL_MULT = 1.5      # SL = entry ± 1.5*ATR
ATR_TP_MULT = 3.0      # TP = entry ± 3.0*ATR
POSITION_SIZE = 1      # Contracts per trade
```

## Output Specifications

### Trade Log CSV Schema

```csv
DateTime,Position,Position_Entry_Price,Exit_Price,Exit_Reason,PnL,Cumulative_PnL
2018-01-02 06:20:00,-1,7522.19,7523.90,Stop_Loss,-1.71,-1.71
```

### Performance Chart

- **Top Panel**: Cumulative P&L line chart
- **Bottom Panel**: Drawdown area chart
- **Format**: PNG, 300 DPI
- **Size**: 14x10 inches

## Dependencies

```
pandas >= 2.0.0    # Data manipulation
numpy >= 1.24.0    # Numerical operations
matplotlib >= 3.7.0 # Visualization
```

## Limitations & Assumptions

1. **Slippage**: Not modeled (assumes perfect fills)
2. **Commission**: Not included (add separately)
3. **Liquidity**: Assumes sufficient liquidity at all levels
4. **Market Hours**: Data assumed to span all needed hours
5. **Timezone**: No conversion (uses raw data time)
6. **Partial Fills**: Not modeled (all-or-nothing)

## Future Enhancements

- [ ] Multi-position management
- [ ] Trailing stop loss
- [ ] Partial profit taking
- [ ] Commission/slippage modeling
- [ ] Real-time data feed integration
- [ ] Walk-forward optimization
- [ ] Monte Carlo simulation
- [ ] Multi-asset support

---

**Version**: 1.0  
**Last Updated**: December 2025  
**Maintained By**: Senior Quantitative Developer

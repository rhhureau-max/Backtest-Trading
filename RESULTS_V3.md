# PBTrading Silver Bullet & IFVG V3 - Optimization Results

## Objective: Maximize Profit Factor

### Best Configuration Found

| Parameter | Value |
|-----------|-------|
| Fractal Lookback | 50 candles (15m) |
| Sweep Validity | 60 minutes |
| RR Target | 2.5 |
| SL Type | fill_candle |
| Trading Window | 9:00 - 10:00 CT |
| **Trend Filter** | **ON** |

### Performance Metrics

| Metric | Value |
|--------|-------|
| **Profit Factor** | **1.33** |
| Win Rate | 39.81% |
| Max Drawdown | 1.62% |
| Total Trades | 108 |

### All Tested Configurations

| # | RR | SL Type | Trend | PF | Win Rate | Max DD | Trades |
|---|-----|---------|-------|-----|----------|--------|--------|
| 1 | 2.5 | fill_candle | ON | **1.33** | 39.81% | 1.62% | 108 |
| 2 | 2.0 | fill_candle | ON | **1.01** | 42.37% | 2.48% | 118 |
| 3 | 2.5 | fill_candle | OFF | 0.71 | 38.0% | 9.66% | 400 |
| 4 | 2.0 | fill_candle | OFF | 0.69 | 40.21% | 11.89% | 480 |
| 5 | 2.0 | fill_candle | OFF | 0.67 | 40.43% | 10.79% | 423 |
| 6 | 2.0 | ifvg | OFF | 0.66 | 35.55% | 11.69% | 346 |
| 7 | 1.5 | fill_candle | OFF | 0.62 | 43.21% | 12.08% | 449 |

### Key Findings

1. **Trend Filter is Critical**: Enabling the trend filter dramatically improves Profit Factor from ~0.7 to 1.33
2. **Higher RR with Trend Filter**: RR 2.5 with trend filter gives the best PF (1.33)
3. **Trade Quality vs Quantity**: Trend filter reduces trades (108 vs 400+) but improves quality
4. **Lower Drawdown**: Best config has only 1.62% max drawdown

### Strategy Logic V3

**Entry Conditions:**
1. Liquidity sweep on 15m (50 candle lookback)
2. FVG creation on 5m, violated to become IFVG
3. Price fills/tests the IFVG zone
4. **Trend Filter**: Only take longs above 100-period MA, shorts below

**Risk Management:**
- SL: Under the candle that filled the IFVG
- TP: 2.5R (2.5x initial risk)
- Break-even at 1R profit
- Forced close at 15:00 CT

---

*Generated on 2025-11-30 | Data: NQ Futures 2025*

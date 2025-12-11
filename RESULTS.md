# PBTrading Silver Bullet & IFVG Backtest Results

## Strategy Overview

**Instrument:** NQ Futures (Nasdaq 100)  
**Data Period:** 2025 (293,508 bars at 1-minute resolution)  
**Trading Window:** 9:00 - 10:00 Chicago Time (Silver Bullet Session)  
**Strategy Components:**
- Liquidity Sweep Detection (20-bar fractal)
- Fair Value Gap (FVG) Identification
- Inversion FVG (IFVG) Entry Logic
- Break-Even at 1R Profit
- Forced Close at 15:00 CT

---

## Performance Metrics by Risk-Reward Ratio

| RR Target | Win Rate (%) | Profit Factor | Max Drawdown (%) | Sharpe Ratio | Total Trades |
|-----------|--------------|---------------|------------------|--------------|--------------|
| 1.0       | 38.10        | 0.66          | 20.43            | -2.55        | 937          |
| 1.5       | 32.34        | 0.74          | 15.52            | -1.60        | 804          |
| 2.0       | 27.09        | 0.67          | 16.88            | -1.96        | 764          |
| 2.5       | 24.63        | 0.60          | 20.81            | -2.26        | 743          |
| 3.0       | 24.04        | 0.64          | 19.48            | -1.97        | 732          |
| 3.5       | 23.19        | 0.64          | 19.79            | -1.85        | 720          |
| 4.0       | 23.00        | 0.66          | 18.59            | -1.69        | 713          |
| 4.5       | 22.63        | 0.68          | 17.96            | -1.52        | 707          |
| 5.0       | 21.84        | 0.69          | 17.24            | -1.47        | 705          |

---

## Key Insights

### Best Configuration
- **Best Sharpe Ratio:** RR 5.0 (-1.47)
- **Best Win Rate:** RR 1.0 (38.10%)
- **Lowest Drawdown:** RR 1.5 (15.52%)
- **Best Profit Factor:** RR 1.5 (0.74)

### Observations
1. **Win Rate vs RR Trade-off:** As expected, higher RR targets result in lower win rates
2. **Drawdown Stability:** Max drawdown ranges from 15.52% to 20.81% across all configurations
3. **Trade Frequency:** Higher RR targets slightly reduce the number of trades (937 to 705)
4. **Sharpe Ratio Trend:** Improves with higher RR targets (from -2.55 to -1.47)

---

## Risk Management Rules Applied

- **Stop Loss:** Placed at swing low (longs) or swing high (shorts)
- **Take Profit:** Multiple RR ratios tested (1x to 5x risk)
- **Break-Even:** SL moved to entry at 1R profit
- **Time Exit:** All positions closed at 15:00 CT

---

*Generated on 2025-11-30 | Data: NQ Futures 2025*

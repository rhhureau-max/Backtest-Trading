# Backtest-Trading

## NQ IVFG Strategy - Pine Script v5

This repository contains a professional Pine Script v5 trading strategy for the Nasdaq 100 (NQ) futures contract.

### Strategy Overview

The **NQ IVFG Strategy** is a multi-timeframe trading system that uses:
- **Inverted Fair Value Gaps (IVFG)** for entry signals
- **EMA 20 on 4H timeframe** for trend filtering
- **London Killzone (01:00-05:00)** time window filter
- **3 flexible risk management modes** (Structural, Fixed Points, ATR-based)
- **Real-time performance metrics** displayed on chart

### Files

- **`NQ_IVFG_Strategy.pine`**: Complete Pine Script v5 strategy code
- **`STRATEGY_DOCUMENTATION.md`**: Detailed documentation in French (comprehensive guide)
- **CSV files**: Historical price data for various timeframes (2018-2025)

### Quick Start

1. Open [TradingView](https://www.tradingview.com/)
2. Open the Pine Editor (bottom of screen)
3. Create a new script
4. Copy the contents of `NQ_IVFG_Strategy.pine`
5. Save and add to chart
6. Configure chart: NQ symbol, 5-minute timeframe
7. Adjust parameters in the strategy settings

### Key Features

✅ **Multi-Timeframe Analysis**: Uses 5m for entries and 4h for trend direction  
✅ **IVFG Signal Detection**: Detects Fair Value Gaps with 12-bar memory  
✅ **Time Window Filter**: Only trades during London Killzone (01:00-05:00)  
✅ **3 Risk Management Modes**:
  - Mode A: Structural (based on candle structure with R:R ratio)
  - Mode B: Fixed Points (fixed stop loss and take profit)
  - Mode C: ATR-Based (adaptive to volatility)  
✅ **Performance Table**: Real-time metrics (Win Rate, Profit Factor, Drawdown, etc.)  
✅ **No Repainting**: Uses proper lookahead settings for higher timeframe data  
✅ **Professional Code**: Modular, well-commented, and optimized  

### Documentation

For complete documentation including:
- Detailed parameter explanations
- Risk management mode comparisons
- Optimization tips
- Installation instructions
- Trading guidelines

Please see **[STRATEGY_DOCUMENTATION.md](STRATEGY_DOCUMENTATION.md)**

### Data Files

This repository includes historical price data for NQ and ES futures:
- **Timeframes**: 1m, 5m, 15m, 1h, 4h, 1D
- **Period**: 2018-2025
- **Format**: CSV files

### Disclaimer

⚠️ **Important**: This strategy is provided for educational purposes only. Past performance does not guarantee future results. Always test thoroughly in a demo account before using real money. Trading involves substantial risk of loss.

### License

This project is open source. Feel free to use, modify, and distribute.

---

**Happy Trading! 📈**
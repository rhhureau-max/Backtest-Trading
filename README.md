# Backtest-Trading

This repository contains historical trading data for NQ (NASDAQ-100) and ES (S&P 500) futures, along with analysis tools for backtesting trading strategies.

## Available Tools

### SMT Divergence Detector

A Python-based tool for detecting SMT (Smart Money Technique) divergences between NQ and ES futures during key trading sessions.

**Quick Start:**
```bash
# Install dependencies
pip install -r requirements.txt

# Run analysis on all historical data (2018-today)
python smt_divergence_detector.py
```

**Documentation:**
- 📖 [Full Documentation](README_SMT.md) - Comprehensive guide with algorithm details
- 🚀 [Quick Start Guide](QUICKSTART_SMT.md) - Get started in 5 minutes
- 📊 [Example Output](EXAMPLE_OUTPUT.txt) - Sample analysis results

**Features:**
- ✅ Detects Bullish and Bearish SMT divergences
- ✅ Analyzes London (02:00-05:00) and NY AM (08:30-11:00) sessions
- ✅ Identifies leadership between NQ and ES
- ✅ Supports 5-minute and 15-minute timeframes
- ✅ Generates visualizations and statistical reports
- ✅ Exports results to CSV for further analysis

**Example Results (2018-2025, 5-minute data):**
- Total Divergences: 1,562 (846 London, 716 NY)
- Bullish Leadership: NQ 54.6%, ES 45.4%
- Bearish Leadership: NQ 50.6%, ES 49.4%

## Data Format

The repository contains CSV files with OHLC (Open, High, Low, Close) data:
- **NQ Data**: `YYYY 5m.csv`, `YYYY 15m.csv`, etc.
- **ES Data**: `ES 5m (YYYY-YYYY).csv`, `ES 15m (YYYY-YYYY).csv`, etc.

All timestamps are in Chicago time (UTC-6).

## Requirements

- Python 3.8+
- pandas
- numpy
- scipy
- matplotlib

See `requirements.txt` for specific versions.
# Backtest-Trading

## Judas Swing ICT Analysis

This repository includes a Python script for analyzing "Judas Swing" patterns in NASDAQ 100 (NQ) futures data according to ICT (Inner Circle Trader) methodology.

### Overview

The `judas_swing_analysis.py` script detects Judas Swing patterns by analyzing:
- **Asian Range**: 18:00 (J-1) to 23:00 (J-1) Chicago time
- **Midnight Open**: Open price at 23:00 (J-1) - the pivot/reference point
- **London Killzone**: 01:00 to 04:00 (J) Chicago time

### Pattern Detection

**Bearish Judas Swing (Bull Trap / Short Setup):**
1. Price exceeds Asian High during London Killzone
2. At 04:00 close, price closes BELOW Midnight Open

**Bullish Judas Swing (Bear Trap / Long Setup):**
1. Price breaks below Asian Low during London Killzone
2. At 04:00 close, price closes ABOVE Midnight Open

### Requirements

- Python 3.6+
- pandas
- numpy

Install dependencies:
```bash
pip install pandas numpy
```

### Usage

Run the analysis script:
```bash
python judas_swing_analysis.py
```

The script will:
1. Load all 5-minute data from 2018-2025
2. Analyze trading sessions for Judas Swing patterns
3. Generate a comprehensive report with statistics
4. Save results to `judas_swing_results.csv`

### Output

The script generates:
- **Console Report**: Global statistics, precision metrics, and temporal analysis
- **CSV File**: Detailed results for each detected Judas Swing pattern

### Data Format

Expected CSV format:
- Semicolon-delimited (;)
- Columns: Date (DD/MM/YYYY), Time (HH:MM:SS), Open, High, Low, Close, Volume
- Files: `2018 5m.csv` through `2025 5m.csv`
- All times in Chicago timezone (CST/CDT)
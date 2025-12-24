# Backtest-Trading

## Judas Swing ICT Analysis with "Return to Equilibrium" Validation

This repository includes a Python script for analyzing "Judas Swing" patterns in NASDAQ 100 (NQ) futures data according to ICT (Inner Circle Trader) methodology, with strict "Return to Equilibrium" validation.

### Overview

The `judas_swing_analysis.py` script detects Judas Swing patterns by analyzing:
- **Asian Session**: 18:00 (J-1) to 23:00 (J-1) Chicago time (UTC-5)
- **Asian Equilibrium**: (Asian High + Asian Low) / 2 - the pivot level
- **London Killzone**: 01:00 to 04:00 (J) Chicago time

### Pattern Detection with Equilibrium Validation

**Bearish Judas Swing (Bull Trap / Short Setup):**
1. Price exceeds Asian High during London Killzone (lure breakout)
2. Price reaches a peak (KZ High) 
3. **After the peak, price must return to touch or cross Asian Equilibrium BEFORE 04:00**

**Bullish Judas Swing (Bear Trap / Long Setup):**
1. Price breaks below Asian Low during London Killzone (lure breakout)
2. Price reaches a trough (KZ Low)
3. **After the trough, price must return to touch or cross Asian Equilibrium BEFORE 04:00**

**Important**: If the price raids beyond the Asian range but doesn't return to Equilibrium before 04:00, it's NOT a valid Judas Swing (it's a continuation/expansion).

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
2. Analyze trading sessions for Judas Swing patterns with Equilibrium validation
3. Generate a comprehensive report with timing and amplitude metrics
4. Save results to `judas_swing_results.csv`

### Output

The script generates:
- **Console Report**: 
  - Validation statistics (Return to Equilibrium success rate)
  - Amplitude analysis (average/maximum raid extension)
  - Temporal analysis (time to peak, time to equilibrium)
  - Yearly breakdown
- **CSV File**: Detailed results including:
  - Asian Equilibrium level
  - Time to peak/trough (minutes from 01:00)
  - Time to Equilibrium (minutes from peak to Eq touch)
  - Peak/trough timestamp and Equilibrium touch timestamp

### Data Format

Expected CSV format:
- Semicolon-delimited (;)
- Columns: Date (DD/MM/YYYY), Time (HH:MM:SS), Open, High, Low, Close, Volume
- Files: `2018 5m.csv` through `2025 5m.csv`
- All times in Chicago timezone (CST/CDT)
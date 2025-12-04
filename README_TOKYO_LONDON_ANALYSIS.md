# Tokyo & London Session Analysis Tool

## Overview

This Python tool performs quantitative analysis of Tokyo and London trading sessions for Nasdaq Futures (NQ), identifying manipulation patterns and price behavior across specific intraday time windows.

## Quick Start

### Prerequisites

```bash
pip install pandas numpy
```

### Run the Analysis

```bash
python3 tokyo_london_session_analysis.py
```

## What This Tool Does

The script analyzes **7 years of 5-minute NQ Futures data** (2018-2025) to identify:

1. **Tokyo Range Formation** (19:00-01:00)
2. **London Manipulation Patterns** (02:00-02:45) - "Judas Swings"
3. **Distribution Phase Behavior** (02:45-05:00)

## Output Files

After execution, you'll find:

| File | Description |
|------|-------------|
| `tokyo_london_analysis_results.csv` | Detailed daily analysis (2,032 rows) |
| `tokyo_london_analysis_results_summary.txt` | Quick statistics summary |
| `ANALYSIS_REPORT.md` | Comprehensive findings report |

## Key Findings at a Glance

```
📊 MAIN STATISTICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Trading Days Analyzed: 2,032
✓ Manipulation Frequency: 69.19%
✓ Retest Probability: 61-65%
✓ Average Retests: 3-4 per day

📈 MANIPULATION BREAKDOWN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Bearish (High broken): 37.45%
• Bullish (Low broken): 30.12%
• Volatile (Both): 1.62%
• No Manipulation: 30.81%
```

## Understanding the Results CSV

Each row represents one trading day with these columns:

- `london_date`: The reference day (J)
- `tokyo_high`: Highest point during Tokyo session
- `tokyo_low`: Lowest point during Tokyo session
- `equilibrium`: Midpoint between High and Low
- `manipulation_type`: Bullish/Bearish/Volatile/None
- `manipulation_occurred`: Boolean flag
- `retest_low_count`: Number of Tokyo Low retests (02:45-05:00)
- `retest_high_count`: Number of Tokyo High retests (02:45-05:00)
- `retest_equilibrium_count`: Number of Equilibrium retests (02:45-05:00)

## Session Definitions

All times are in the timezone of the data files:

```
┌─────────────────────────────────────────────────────────┐
│  TOKYO SESSION (J-1)        19:00 ─────> 01:00 (J)     │
│  ├─ Range Formation                                     │
│  └─ Establishes High, Low, Equilibrium                  │
├─────────────────────────────────────────────────────────┤
│  GAP / PRE-LONDON           01:00 ─────> 02:00          │
├─────────────────────────────────────────────────────────┤
│  LONDON MANIPULATION        02:00 ─────> 02:45          │
│  ├─ "Judas Swing" Window                                │
│  ├─ Bullish: Break below Tokyo Low                      │
│  └─ Bearish: Break above Tokyo High                     │
├─────────────────────────────────────────────────────────┤
│  LONDON CONTINUATION        02:45 ─────> 05:00          │
│  ├─ Distribution Phase                                  │
│  └─ Retests of Key Levels                               │
└─────────────────────────────────────────────────────────┘
```

## Example Use Cases

### 1. Find All Bullish Manipulations with Equilibrium Retests

```python
import pandas as pd

df = pd.read_csv('tokyo_london_analysis_results.csv')
df['london_date'] = pd.to_datetime(df['london_date'])

bullish_with_eq = df[
    (df['manipulation_type'] == 'Bullish') & 
    (df['retest_equilibrium_count'] > 0)
]

print(f"Found {len(bullish_with_eq)} days")
```

### 2. Calculate Monthly Success Rate

```python
import pandas as pd

df = pd.read_csv('tokyo_london_analysis_results.csv')
df['london_date'] = pd.to_datetime(df['london_date'])
df['year_month'] = df['london_date'].dt.to_period('M')

monthly = df.groupby('year_month').agg({
    'manipulation_occurred': ['sum', 'count']
})

monthly['success_rate'] = monthly[('manipulation_occurred', 'sum')] / monthly[('manipulation_occurred', 'count')] * 100
print(monthly)
```

### 3. Filter High-Probability Setups

```python
import pandas as pd

df = pd.read_csv('tokyo_london_analysis_results.csv')

# Bearish manipulation with high retest
high_prob = df[
    (df['manipulation_type'] == 'Bearish') & 
    (df['retest_high_count'] >= 3)
]

print(f"High probability setups: {len(high_prob)}")
```

## Data Requirements

The script expects CSV files in this format:

```
Filename Pattern: YYYY 5m.csv (e.g., "2018 5m.csv", "2019 5m.csv")
Separator: semicolon (;)
Columns: Date;Time;Open;High;Low;Close;Volume
Date Format: DD/MM/YYYY
Time Format: HH:MM:SS
```

Example:
```
Column1;Column2;Column3;Column4;Column5;Column6;Column7
01/01/2018;17:00:00;7503.74;7511.94;7499.64;7511.35;1451
01/01/2018;17:05:00;7510.77;7516.04;7510.77;7512.53;360
```

## Performance

- **Processing Speed**: ~2,400 days in ~5 minutes
- **Memory Usage**: ~500MB for 554,518 records
- **Output Size**: ~138KB CSV file

## Customization

To modify the session times, edit these sections in `tokyo_london_session_analysis.py`:

```python
# Tokyo session: 19:00 (J-1) to 01:00 (J)
tokyo_data = self.data[
    ((self.data['Date'] == tokyo_start_date) & (self.data['Time'] >= time(19, 0))) |
    ((self.data['Date'] == tokyo_end_date) & (self.data['Time'] < time(1, 0)))
]

# Manipulation window: 02:00 to 02:45
manipulation_data = self.data[
    (self.data['Date'] == date) &
    (self.data['Time'] >= time(2, 0)) &
    (self.data['Time'] < time(2, 45))
]

# Distribution phase: 02:45 to 05:00
distribution_data = self.data[
    (self.data['Date'] == date) &
    (self.data['Time'] >= time(2, 45)) &
    (self.data['Time'] < time(5, 0))
]
```

## Troubleshooting

### Issue: "No data files found"
- Ensure CSV files are in the same directory as the script
- Check filename format: `YYYY 5m.csv`

### Issue: "Not enough data days for analysis"
- Verify CSV files contain data
- Check date format in CSV matches DD/MM/YYYY

### Issue: Script runs slowly
- Expected for large datasets (2M+ records)
- Progress indicators show every 200 days
- Consider analyzing fewer years if needed

## License

This tool is provided as-is for quantitative research purposes.

## Author

Quantitative Analysis Tool for NQ Futures Market Structure Research

---

**Last Updated**: December 2025  
**Version**: 1.0  
**Data Coverage**: 2018-2025

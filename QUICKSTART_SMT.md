# SMT Divergence Detector - Quick Start Guide

Get started with SMT divergence analysis in 5 minutes!

## Installation

```bash
# 1. Navigate to the repository
cd /home/runner/work/Backtest-Trading/Backtest-Trading

# 2. Install dependencies
pip install -r requirements.txt
```

## Basic Usage

### Analyze 2024 Data (5-minute)

```bash
python smt_divergence_detector.py
```

This will:
- ✅ Analyze NQ and ES 5-minute data for 2024
- ✅ Detect SMT divergences in London (02:00-05:00) and NY AM (08:30-11:00) sessions
- ✅ Generate statistics and visualizations in `smt_analysis_results/`

### View Results

```bash
# View statistics summary
cat smt_analysis_results/smt_statistics.csv

# List all output files
ls -lh smt_analysis_results/
```

## Common Commands

### Different Timeframe

```bash
# Use 15-minute data instead
python smt_divergence_detector.py --timeframe 15m
```

### Multiple Years

```bash
# Analyze 2023 and 2024
python smt_divergence_detector.py --years 2023 2024
```

### Custom Output Directory

```bash
# Save results to a specific folder
python smt_divergence_detector.py --output my_analysis
```

## Understanding Output

### Files Generated

| File | Description |
|------|-------------|
| `smt_statistics.csv` | Summary table with counts by session |
| `smt_divergences_detailed.csv` | Full list of all detected divergences |
| `smt_example_*.png` | Visual examples of divergences |

### Reading Statistics

```csv
Session,Total Divergences,Bullish SMT,Bearish SMT,NQ Bullish Leader,ES Bullish Leader,NQ Bearish Leader,ES Bearish Leader
LONDON,95,41,54,23,18,31,23
NY,96,51,45,27,24,18,27
TOTAL,191,92,99,50,42,49,50
```

**Key Metrics:**
- **Total Divergences**: Total SMT divergences found
- **Bullish SMT**: Divergences suggesting upward potential
- **Bearish SMT**: Divergences suggesting downward potential
- **Bullish Leader**: Asset that refuses to go lower (stronger)
- **Bearish Leader**: Asset that refuses to go higher (weaker)

### Leadership Interpretation

```
Bullish Leader: NQ 54.3% | ES 45.7%
Bearish Leader: NQ 49.5% | ES 50.5%
```

- **NQ as Bullish Leader (54.3%)**: NQ more often refuses to make lower lows
- **NQ as Bearish Leader (49.5%)**: NQ less often refuses to make higher highs

## Example Workflow

```bash
# Step 1: Run analysis
python smt_divergence_detector.py --years 2024 --timeframe 5m

# Step 2: Check statistics
cat smt_analysis_results/smt_statistics.csv

# Step 3: View detailed divergences
head -20 smt_analysis_results/smt_divergences_detailed.csv

# Step 4: Open visualization (example names may vary)
# Transfer PNG files to your local machine or view in file manager
ls smt_analysis_results/*.png
```

## What is SMT Divergence?

**Smart Money Technique (SMT) Divergence** occurs when two correlated assets (NQ and ES) show different behavior at key swing points:

### Bullish SMT
```
NQ: Makes Lower Low (LL)    ←→    ES: Makes Higher Low (HL)
         Weak                           Strong (Leader!)
```
→ **ES is the Bullish Leader** (refuses to go lower, shows strength)

### Bearish SMT
```
NQ: Makes Higher High (HH)  ←→    ES: Makes Lower High (LH)
         Strong                         Weak (Leader!)
```
→ **ES is the Bearish Leader** (refuses to go higher, shows weakness)

## Trading Sessions

### London Session (02:00 - 05:00 Chicago Time)
- Overlap with London open
- Typically good liquidity
- European market influence

### New York AM Session (08:30 - 11:00 Chicago Time)
- NY market open to lunch
- Highest volume period
- Major news releases

## Tips

1. **Start with 5m data** - More granular, shows more divergences
2. **Compare timeframes** - Run both 5m and 15m to see different perspectives
3. **Focus on leadership** - Which asset consistently leads in each session?
4. **Check visualizations** - Look at PNG files to understand the patterns
5. **Export to spreadsheet** - Open CSV files in Excel/LibreOffice for deeper analysis

## Troubleshooting

### No data found?
```bash
# Check if files exist
ls *.csv | grep "2024"
ls *.csv | grep "ES"

# Specify path if files are elsewhere
python smt_divergence_detector.py --path /path/to/csv/files
```

### Module not found?
```bash
# Reinstall dependencies
pip install pandas numpy scipy matplotlib
```

### Need help?
```bash
python smt_divergence_detector.py --help
```

## Next Steps

- Read the full documentation: `README_SMT.md`
- Analyze historical data to find patterns
- Use divergence data for backtesting strategies
- Combine with other technical indicators

---

**Happy Trading Analysis!** 📊📈

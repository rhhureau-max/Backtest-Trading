# Backtest-Trading

A collection of trading analysis tools for Nasdaq Mini Futures backtesting.

## FVG Analysis (Fair Value Gap)

The `fvg_analysis.py` script analyzes Fair Value Gaps on the 8:30 AM Chicago candle across multiple timeframes.

### What is a Fair Value Gap (FVG)?

A Fair Value Gap is a price imbalance identified when:
- **Bullish FVG**: The LOW of candle N+1 > HIGH of candle N-1 (gap up)
- **Bearish FVG**: The HIGH of candle N+1 < LOW of candle N-1 (gap down)

### Strategy

- Identifies FVG formed on the 8:30:00 AM (Chicago time) candle
- Entry at the OPEN of candle N+2 (8:32 for 1m, 8:40 for 5m, 8:45 for 15m)

### Non-Return Criteria

The script calculates the probability that price does not return to the FVG zone:
- **Bullish FVG**: Price does NOT go below HIGH of N-1 (top of FVG)
- **Bearish FVG**: Price does NOT go above LOW of N-1 (bottom of FVG)

### Installation

```bash
pip install -r requirements.txt
```

### Usage

```bash
python fvg_analysis.py
```

### Output

The script outputs non-return probabilities for horizons of 5-15 candles across three timeframes (1m, 5m, 15m):

```
=== ANALYSE FVG 8h30 - Nasdaq Mini Futures ===
Période : 2018-2025

TIMEFRAME 1 MINUTE:
Total FVG détectés: XXX (Haussiers: XXX, Baissiers: XXX)

Probabilité de NON-RETOUR dans le FVG:
Bougies |  Global  | Haussier | Baissier
--------|----------|----------|----------
   5    |  XX.XX%  |  XX.XX%  |  XX.XX%
...
  15    |  XX.XX%  |  XX.XX%  |  XX.XX%
```

## Data Files

CSV files are organized by year and timeframe:
- Format: `{year} {timeframe}.csv` (e.g., "2024 5m.csv", "2024 15m.csv")
- 1m files are compressed as .zip for years 2018-2024
- 2025 has an uncompressed 1m file

### CSV Format
- Separator: semicolon (;)
- Columns: date (DD/MM/YYYY), time (HH:MM:SS), open, high, low, close, volume
- Timezone: Chicago (UTC-6 / UTC-5 DST)
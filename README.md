# Backtest-Trading

Repository for backtesting trading strategies on NQ (Nasdaq 100) futures data.

## Available Tools

### Judas Swing Analyzer

Analyzes trading data to identify and measure "Judas Swings" - false breakouts during the London Killzone that trap traders on the wrong side of the market.

#### What is a Judas Swing?

A Judas Swing is a liquidity trap that occurs when:
1. Price breaks the Asian Range (High or Low from 18:00-23:00 previous day) during the London Killzone (01:00-04:00)
2. BUT the 04:00 candle closes on the opposite side, returning inside the range or passing the Midnight Open
3. This represents a false breakout designed to trap traders

**Types:**
- **Bearish Judas (Bull Trap)**: Price breaks Asian High but closes below Midnight Open
- **Bullish Judas (Bear Trap)**: Price breaks Asian Low but closes above Midnight Open

#### Usage

```bash
# Basic usage (defaults to "2024 15m.csv")
python3 judas_swing_analyzer.py

# Specify a custom file
python3 judas_swing_analyzer.py --file "2023 15m.csv"

# Export results to CSV
python3 judas_swing_analyzer.py --file "2024 15m.csv" --export results.csv

# View help
python3 judas_swing_analyzer.py --help
```

#### Requirements

```bash
pip install pandas numpy
```

#### Output

The analyzer generates a comprehensive report including:
- Total count of Judas Swings (broken down by type)
- Extension analysis (mean, median, max, std deviation)
- Temporal analysis (time to peak with histogram)
- Top 5 most violent Judas Swings
- Monthly distribution
- Comparison between Bull and Bear traps

#### Data Format

CSV files should be semicolon-separated with the following structure:
- Column1: Date (DD/MM/YYYY)
- Column2: Time (HH:MM:SS)
- Column3: Open price
- Column4: High price
- Column5: Low price
- Column6: Close price
- Column7: Volume

All times are in Chicago time (UTC-5).

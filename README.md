# Backtest-Trading

## Overview
This repository contains historical trading data in 1-minute, 5-minute, 15-minute, 1-hour, 4-hour, and daily intervals from 2018 to 2025.

## Analysis Tools

### Returns Analysis Script
The `analyze_returns.py` script analyzes 1-minute trading data files (XLSX and CSV) to calculate annual and overall returns.

#### Usage
```bash
python3 analyze_returns.py
```

#### Requirements
```bash
pip3 install pandas openpyxl
```

#### Output
The script generates:
- Console output with detailed annual returns
- `returns_analysis.txt` file with a summary report including:
  - Annual returns for each year (2018-2025)
  - Overall return across all years
  - Average annual return
  - Compound Annual Growth Rate (CAGR)

#### Results Summary (as of latest analysis)
- **Overall Return (2018-2025)**: 242.29%
- **Average Annual Return**: 19.68%
- **CAGR**: 19.22%

| Year | Return % | First Close | Last Close |
|------|----------|-------------|------------|
| 2018 | -2.28%   | 7506.96     | 7336.14    |
| 2019 | 36.31%   | 7337.00     | 10000.85   |
| 2020 | 47.25%   | 10002.56    | 14728.99   |
| 2021 | 26.89%   | 14743.00    | 18706.98   |
| 2022 | -33.83%  | 18767.69    | 12418.73   |
| 2023 | 45.90%   | 12493.81    | 18228.23   |
| 2024 | 20.01%   | 18241.90    | 21891.80   |
| 2025 | 17.23%   | 21919.64    | 25695.75   |
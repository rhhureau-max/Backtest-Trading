# Data Format Documentation

This document describes the expected format for CSV data files used in the backtest strategy.

## File Naming Convention

Files should follow this naming pattern:
```
YYYY {timeframe}.csv
YYYY {timeframe}.csv.zip
```

### Examples:
- `2018 1m.csv` or `2018 1m.csv.zip` - 1-minute data for 2018
- `2019 5m.csv` - 5-minute data for 2019
- `2020 15m.csv` - 15-minute data for 2020

## File Format

### Delimiter
Files must use **semicolon (;)** as the delimiter.

### Header Row
Files must include a header row with these exact column names:
```
Column1;Column2;Column3;Column4;Column5;Column6;Column7
```

### Data Columns

| Column | Name | Description | Format | Example |
|--------|------|-------------|--------|---------|
| Column1 | Date | Trading date | DD/MM/YYYY | 01/01/2018 |
| Column2 | Time | Trading time | HH:MM:SS | 08:30:00 |
| Column3 | Open | Opening price | Numeric | 7503.739664 |
| Column4 | High | Highest price | Numeric | 7511.940473 |
| Column5 | Low | Lowest price | Numeric | 7499.63926 |
| Column6 | Close | Closing price | Numeric | 7511.3547 |
| Column7 | Volume | Trading volume | Integer | 1451 |

## Sample Data

```csv
Column1;Column2;Column3;Column4;Column5;Column6;Column7
01/01/2018;17:00:00;7503.739664;7511.940473;7499.63926;7511.3547;1451
01/01/2018;17:05:00;7510.768928;7516.040877;7510.768928;7512.526245;360
01/01/2018;17:10:00;7512.233359;7514.283561;7510.768928;7511.940473;157
02/01/2018;08:30:00;7545.329478;7550.601426;7528.634975;7533.028265;13826
03/01/2018;08:30:00;7646.082267;7661.898111;7645.496495;7660.726567;9505
```

## Data Requirements

### Timeframes Supported
The backtest strategy currently supports three timeframes:
- **1m** - 1-minute candles
- **5m** - 5-minute candles
- **15m** - 15-minute candles

### Time Coverage
- Data should include trading days from the year specified in the filename
- Each day should have data points starting before 8:30 AM (to calculate the previous 5 candles)
- 8:30 AM candles must be present for analysis

### Data Quality
- All price fields (Open, High, Low, Close) must be numeric
- High should be >= Low
- High should be >= Open and Close
- Low should be <= Open and Close
- Volume should be a positive integer
- No missing values in critical fields (Date, Time, OHLC)

## Compressed Files

### ZIP Format
Files can be compressed as ZIP archives:
- Extension: `.csv.zip`
- Should contain a single CSV file
- The CSV file inside can have any name
- The script automatically extracts and processes zipped files

### Example Structure:
```
2018 1m.csv.zip
  └── 2018 1m.csv (the actual data file inside)
```

## Date and Time Parsing

### Date Format
- Must be in DD/MM/YYYY format
- Examples: 
  - ✅ `01/01/2018`
  - ✅ `31/12/2018`
  - ❌ `2018-01-01` (wrong format)
  - ❌ `1/1/2018` (missing leading zeros)

### Time Format
- Must be in HH:MM:SS format (24-hour clock)
- Examples:
  - ✅ `08:30:00`
  - ✅ `14:45:30`
  - ❌ `8:30:00` (missing leading zero)
  - ❌ `08:30` (missing seconds)

## Validating Your Data

### Quick Validation Commands

Check file format:
```bash
head -5 "2018 5m.csv"
```

Check for 8:30 AM entries:
```bash
grep "08:30:00" "2018 5m.csv" | wc -l
```

Check delimiter:
```bash
head -1 "2018 5m.csv" | grep ";"
```

### Python Validation Script

```python
import pandas as pd

def validate_csv(filepath):
    """Validate CSV file format."""
    try:
        df = pd.read_csv(
            filepath,
            sep=';',
            names=['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume'],
            skiprows=1
        )
        
        print(f"✓ File loaded successfully")
        print(f"✓ Total rows: {len(df)}")
        print(f"✓ Date range: {df['Date'].min()} to {df['Date'].max()}")
        
        # Check for 8:30 AM entries
        am_830 = df[df['Time'] == '08:30:00']
        print(f"✓ 8:30 AM entries: {len(am_830)}")
        
        # Check data types
        df['Open'] = pd.to_numeric(df['Open'], errors='coerce')
        df['High'] = pd.to_numeric(df['High'], errors='coerce')
        df['Low'] = pd.to_numeric(df['Low'], errors='coerce')
        df['Close'] = pd.to_numeric(df['Close'], errors='coerce')
        
        if df[['Open', 'High', 'Low', 'Close']].isnull().any().any():
            print("⚠ Warning: Some price values could not be converted to numbers")
        else:
            print("✓ All price values are numeric")
        
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

# Usage
validate_csv("2018 5m.csv")
```

## Common Issues and Solutions

### Issue: "File not found"
**Solution**: Check file naming exactly matches the pattern `YYYY timeframe.csv`

### Issue: "Error reading file"
**Solution**: Verify semicolon delimiter is used, not comma

### Issue: "No 8:30 AM candles found"
**Solution**: Ensure your data includes 8:30:00 time entries

### Issue: "Cannot convert to numeric"
**Solution**: Check that price fields don't have currency symbols or non-numeric characters

### Issue: "Date parsing errors"
**Solution**: Ensure dates are in DD/MM/YYYY format, not MM/DD/YYYY or YYYY-MM-DD

## Timezone Considerations

- All times should be in the same timezone
- The strategy assumes times are consistent across all files
- If your data spans timezone changes (e.g., daylight saving time), ensure consistency
- 8:30 AM should always be represented as `08:30:00` regardless of timezone

## Data Sources

This format is commonly used for:
- Exported data from trading platforms
- Historical data from financial data providers
- Custom data collection scripts

If your data is in a different format, you may need to convert it before using the backtest strategy.

## Converting Data Formats

### From CSV with comma delimiter:
```bash
sed 's/,/;/g' input.csv > output.csv
```

### From different date format (YYYY-MM-DD to DD/MM/YYYY):
```python
import pandas as pd

df = pd.read_csv('input.csv')
df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%d/%m/%Y')
df.to_csv('output.csv', sep=';', index=False)
```

## Contact

If you have questions about the data format or need help converting your data, please open an issue in the repository.

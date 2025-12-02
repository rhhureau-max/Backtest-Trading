#!/usr/bin/env python3
"""
Backtesting Strategy: 8:30 Candle Wick Breakout
================================================

This script identifies all trades where the 8:30 candle exceeds the wicks 
of the last 5 candles:
- Bullish: when candle's high exceeds the highest wick (high) of previous 5 candles
- Bearish: when candle's low goes below the lowest wick (low) of previous 5 candles

Timeframes: 1m, 5m, 15m
Period: 2018 to 2025
"""

import pandas as pd
import zipfile
from datetime import datetime, time
from pathlib import Path


class BacktestStrategy:
    # Constants
    CSV_COLUMNS = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
    DATETIME_FORMAT = '%d/%m/%Y %H:%M:%S'
    
    def __init__(self, base_path='.'):
        """Initialize the backtesting strategy."""
        self.base_path = Path(base_path)
        self.results = {
            '1m': [],
            '5m': [],
            '15m': []
        }
        self.years = range(2018, 2026)  # 2018 to 2025 inclusive
        
    def _add_datetime_columns(self, df):
        """Add datetime columns to the dataframe."""
        # Convert Date and Time to datetime
        df['DateTime'] = pd.to_datetime(
            df['Date'] + ' ' + df['Time'],
            format=self.DATETIME_FORMAT
        )
        
        # Extract date and time components
        df['DateOnly'] = df['DateTime'].dt.date
        df['TimeOnly'] = df['DateTime'].dt.time
        
        return df
    
    def read_csv_file(self, filepath):
        """Read CSV file with proper handling of format."""
        try:
            df = pd.read_csv(
                filepath,
                sep=';',
                names=self.CSV_COLUMNS,
                skiprows=1  # Skip header row
            )
            
            return self._add_datetime_columns(df)
        except Exception as e:
            print(f"Error reading {filepath}: {e}")
            return None
    
    def read_zipped_csv(self, zip_path):
        """Read CSV from a zip file."""
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                # Get the CSV filename (should be something like "2018 1m.csv")
                csv_files = [f for f in zip_ref.namelist() if f.endswith('.csv')]
                if not csv_files:
                    print(f"No CSV file found in {zip_path}")
                    return None
                
                csv_filename = csv_files[0]
                with zip_ref.open(csv_filename) as csv_file:
                    df = pd.read_csv(
                        csv_file,
                        sep=';',
                        names=self.CSV_COLUMNS,
                        skiprows=1
                    )
                    
                    return self._add_datetime_columns(df)
        except Exception as e:
            print(f"Error reading zipped file {zip_path}: {e}")
            return None
    
    def get_file_path(self, year, timeframe):
        """Get the appropriate file path for a given year and timeframe."""
        if timeframe == '1m':
            # Check for zipped file first (2018-2024), then unzipped (2025)
            zip_path = self.base_path / f"{year} 1m.csv.zip"
            csv_path = self.base_path / f"{year} 1m.csv"
            
            if zip_path.exists():
                return ('zip', zip_path)
            elif csv_path.exists():
                return ('csv', csv_path)
            else:
                return (None, None)
        else:
            csv_path = self.base_path / f"{year} {timeframe}.csv"
            if csv_path.exists():
                return ('csv', csv_path)
            else:
                return (None, None)
    
    def get_830_candle(self, df, timeframe):
        """
        Get the 8:30 candle for each day.
        
        For 1m: exact 08:30:00 candle
        For 5m: candle that includes 08:30 (08:30:00)
        For 15m: candle that includes 08:30 (could be 08:15:00 or 08:30:00)
        """
        target_time = time(8, 30, 0)
        
        if timeframe == '1m':
            # Exact match for 1-minute candles
            mask = df['TimeOnly'] == target_time
        elif timeframe == '5m':
            # For 5-minute candles, 8:30 should be the candle at 08:30:00
            mask = df['TimeOnly'] == target_time
        elif timeframe == '15m':
            # For 15-minute candles, 8:30 could be at 08:30:00 or 08:15:00
            # We'll look for the candle at 08:30:00 first, then 08:15:00
            mask = (df['TimeOnly'] == target_time) | (df['TimeOnly'] == time(8, 15, 0))
        
        return df[mask].copy()
    
    def check_breakout(self, df, idx, lookback=5):
        """
        Check if the candle at idx breaks out above/below the previous 5 candles.
        
        Returns:
            dict: {
                'bullish': bool,
                'bearish': bool,
                'current_high': float,
                'current_low': float,
                'prev_max_high': float,
                'prev_min_low': float
            }
        """
        # Need at least lookback candles before the current one
        if idx < lookback:
            return None
        
        # Get previous 5 candles
        prev_candles = df.iloc[idx-lookback:idx]
        
        if len(prev_candles) < lookback:
            return None
        
        # Current candle
        current = df.iloc[idx]
        
        # Calculate previous highs and lows
        prev_max_high = prev_candles['High'].max()
        prev_min_low = prev_candles['Low'].min()
        
        # Check for bullish breakout (high exceeds previous 5 highs)
        bullish = current['High'] > prev_max_high
        
        # Check for bearish breakout (low goes below previous 5 lows)
        bearish = current['Low'] < prev_min_low
        
        return {
            'bullish': bullish,
            'bearish': bearish,
            'current_high': current['High'],
            'current_low': current['Low'],
            'prev_max_high': prev_max_high,
            'prev_min_low': prev_min_low,
            'current_open': current['Open'],
            'current_close': current['Close']
        }
    
    def analyze_timeframe(self, timeframe):
        """Analyze a specific timeframe across all years."""
        print(f"\n{'='*70}")
        print(f"Analyzing {timeframe} timeframe...")
        print(f"{'='*70}")
        
        all_data = []
        
        for year in self.years:
            # Get file path for this year and timeframe
            file_type, file_path = self.get_file_path(year, timeframe)
            
            if file_type is None:
                print(f"File not found for {year} {timeframe}")
                continue
            
            if file_type == 'zip':
                print(f"Reading {year} {timeframe}.csv.zip...")
                df = self.read_zipped_csv(file_path)
            else:  # csv
                print(f"Reading {year} {timeframe}.csv...")
                df = self.read_csv_file(file_path)
            
            if df is None or df.empty:
                print(f"No data for {year} {timeframe}")
                continue
            
            all_data.append(df)
        
        if not all_data:
            print(f"No data found for {timeframe}")
            return
        
        # Combine all years
        combined_df = pd.concat(all_data, ignore_index=True)
        print(f"Total candles loaded: {len(combined_df):,}")
        
        # Sort by datetime and set index for efficient lookups
        combined_df = combined_df.sort_values('DateTime').reset_index(drop=True)
        
        # Create a dictionary mapping DateTime to index for O(1) lookups
        datetime_to_idx = {dt: idx for idx, dt in enumerate(combined_df['DateTime'])}
        
        # Get all 8:30 candles
        candles_830 = self.get_830_candle(combined_df, timeframe)
        print(f"Total 8:30 candles found: {len(candles_830)}")
        
        # For each 8:30 candle, check for breakout
        trades = []
        
        for _, candle in candles_830.iterrows():
            # Find the index of this candle in the combined dataframe
            candle_datetime = candle['DateTime']
            idx = datetime_to_idx.get(candle_datetime)
            
            if idx is None:
                continue
            
            # Check for breakout
            result = self.check_breakout(combined_df, idx, lookback=5)
            
            if result is None:
                continue
            
            if result['bullish'] or result['bearish']:
                # Determine direction
                if result['bullish'] and result['bearish']:
                    direction = 'Both (Bullish & Bearish)'
                elif result['bullish']:
                    direction = 'Bullish'
                else:
                    direction = 'Bearish'
                
                trade = {
                    'Date': candle['Date'],
                    'Time': candle['Time'],
                    'DateTime': candle_datetime,
                    'Direction': direction,
                    'Open': result['current_open'],
                    'High': result['current_high'],
                    'Low': result['current_low'],
                    'Close': result['current_close'],
                    'Prev_Max_High': result['prev_max_high'],
                    'Prev_Min_Low': result['prev_min_low']
                }
                
                trades.append(trade)
        
        self.results[timeframe] = trades
        
        print(f"\nTrades found: {len(trades)}")
        if trades:
            bullish_count = sum(1 for t in trades if 'Bullish' in t['Direction'])
            bearish_count = sum(1 for t in trades if 'Bearish' in t['Direction'])
            both_count = sum(1 for t in trades if 'Both' in t['Direction'])
            
            print(f"  - Bullish trades: {bullish_count}")
            print(f"  - Bearish trades: {bearish_count}")
            print(f"  - Both directions: {both_count}")
    
    def generate_report(self):
        """Generate a comprehensive report of all trades."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_filename = f"backtest_report_{timestamp}.txt"
        csv_filename = f"backtest_trades_{timestamp}.csv"
        
        # Generate text report
        with open(report_filename, 'w') as f:
            f.write("="*80 + "\n")
            f.write("BACKTESTING REPORT: 8:30 CANDLE WICK BREAKOUT STRATEGY\n")
            f.write("="*80 + "\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Period: 2018 to 2025\n")
            f.write(f"Strategy: Identify 8:30 candles that exceed wicks of previous 5 candles\n")
            f.write("="*80 + "\n\n")
            
            for timeframe in ['1m', '5m', '15m']:
                trades = self.results[timeframe]
                
                f.write(f"\n{'='*80}\n")
                f.write(f"TIMEFRAME: {timeframe}\n")
                f.write(f"{'='*80}\n")
                f.write(f"Total Trades: {len(trades)}\n")
                
                if trades:
                    bullish_count = sum(1 for t in trades if 'Bullish' in t['Direction'])
                    bearish_count = sum(1 for t in trades if 'Bearish' in t['Direction'])
                    both_count = sum(1 for t in trades if 'Both' in t['Direction'])
                    
                    f.write(f"  - Bullish: {bullish_count}\n")
                    f.write(f"  - Bearish: {bearish_count}\n")
                    f.write(f"  - Both: {both_count}\n")
                    f.write(f"\n{'='*80}\n")
                    f.write("TRADE DETAILS:\n")
                    f.write(f"{'='*80}\n\n")
                    
                    for i, trade in enumerate(trades, 1):
                        f.write(f"Trade #{i}\n")
                        f.write(f"  Date: {trade['Date']}\n")
                        f.write(f"  Time: {trade['Time']}\n")
                        f.write(f"  Direction: {trade['Direction']}\n")
                        f.write(f"  Open: {trade['Open']:.2f}\n")
                        f.write(f"  High: {trade['High']:.2f}\n")
                        f.write(f"  Low: {trade['Low']:.2f}\n")
                        f.write(f"  Close: {trade['Close']:.2f}\n")
                        f.write(f"  Previous 5 Candles Max High: {trade['Prev_Max_High']:.2f}\n")
                        f.write(f"  Previous 5 Candles Min Low: {trade['Prev_Min_Low']:.2f}\n")
                        
                        if 'Bullish' in trade['Direction']:
                            breakout_amount = trade['High'] - trade['Prev_Max_High']
                            f.write(f"  Bullish Breakout Amount: {breakout_amount:.2f}\n")
                        
                        if 'Bearish' in trade['Direction']:
                            breakout_amount = trade['Prev_Min_Low'] - trade['Low']
                            f.write(f"  Bearish Breakout Amount: {breakout_amount:.2f}\n")
                        
                        f.write("\n")
                else:
                    f.write("No trades found for this timeframe.\n")
        
        print(f"\n{'='*80}")
        print(f"Report generated: {report_filename}")
        
        # Generate CSV report with all trades
        all_trades = []
        for timeframe in ['1m', '5m', '15m']:
            for trade in self.results[timeframe]:
                trade_copy = trade.copy()
                trade_copy['Timeframe'] = timeframe
                all_trades.append(trade_copy)
        
        if all_trades:
            trades_df = pd.DataFrame(all_trades)
            # Reorder columns
            cols = ['Timeframe', 'Date', 'Time', 'Direction', 'Open', 'High', 'Low', 
                   'Close', 'Prev_Max_High', 'Prev_Min_Low']
            trades_df = trades_df[cols]
            trades_df.to_csv(csv_filename, index=False)
            print(f"CSV report generated: {csv_filename}")
        
        print(f"{'='*80}")
        
        # Print summary to console
        print("\nSUMMARY:")
        print(f"{'='*80}")
        total_trades = sum(len(self.results[tf]) for tf in ['1m', '5m', '15m'])
        print(f"Total trades across all timeframes: {total_trades}")
        
        for timeframe in ['1m', '5m', '15m']:
            trades = self.results[timeframe]
            print(f"\n{timeframe} timeframe: {len(trades)} trades")
            if trades:
                bullish_count = sum(1 for t in trades if 'Bullish' in t['Direction'])
                bearish_count = sum(1 for t in trades if 'Bearish' in t['Direction'])
                print(f"  - Bullish: {bullish_count}")
                print(f"  - Bearish: {bearish_count}")
    
    def run(self):
        """Run the complete backtesting analysis."""
        print("="*80)
        print("BACKTESTING STRATEGY: 8:30 CANDLE WICK BREAKOUT")
        print("="*80)
        print(f"Period: 2018 to 2025")
        print(f"Timeframes: 1m, 5m, 15m")
        print(f"Strategy: Identify 8:30 candles that exceed wicks of previous 5 candles")
        print("="*80)
        
        # Analyze each timeframe
        for timeframe in ['1m', '5m', '15m']:
            self.analyze_timeframe(timeframe)
        
        # Generate report
        print("\n" + "="*80)
        print("GENERATING REPORTS...")
        print("="*80)
        self.generate_report()


def main():
    """Main entry point."""
    # Get the script's directory
    script_dir = Path(__file__).parent
    
    print("Initializing backtesting strategy...")
    print(f"Working directory: {script_dir}")
    
    # Create and run the strategy
    strategy = BacktestStrategy(base_path=script_dir)
    strategy.run()
    
    print("\n" + "="*80)
    print("BACKTESTING COMPLETE!")
    print("="*80)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Analyze trading data files to count impulsive candles and perform backtesting.

An impulsive candle is one where the close breaks above the high 
OR below the low of the last N candles of the range.

Backtesting Strategy:
- Signal: When a candle closes above/below the range of last N candles
- Entry: Open of the next candle after signal
- Stop Loss: 100% of entry candle (Low for LONG, High for SHORT)
- Take Profit: 1:1 Risk/Reward ratio
"""

import os
import zipfile
import pandas as pd
from datetime import datetime, time
from collections import defaultdict
import argparse
from dataclasses import dataclass, field
from typing import List, Optional, Tuple


# Default configuration - can be overridden via command line
DEFAULT_DATA_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_YEARS = range(2018, 2026)
TIMEFRAMES = ["1m", "5m", "15m"]
LOOKBACK_PERIODS = [5, 10, 15, 20]
TIME_START = time(2, 0, 0)
TIME_END = time(12, 0, 0)


@dataclass
class Trade:
    """Represents a single trade."""
    entry_date: datetime
    direction: str  # 'LONG' or 'SHORT'
    entry_price: float
    stop_loss: float
    take_profit: float
    result: Optional[str] = None  # 'WIN', 'LOSS', or None if still open
    exit_price: Optional[float] = None
    profit_points: float = 0.0


@dataclass
class BacktestResult:
    """Stores backtest results for a specific timeframe and lookback period."""
    timeframe: str
    lookback: int
    total_trades: int = 0
    wins: int = 0
    losses: int = 0
    long_trades: int = 0
    short_trades: int = 0
    long_wins: int = 0
    short_wins: int = 0
    total_profit_points: float = 0.0
    trades: List[Trade] = field(default_factory=list)
    
    @property
    def win_rate(self) -> float:
        """Calculate win rate as percentage."""
        if self.total_trades == 0:
            return 0.0
        return (self.wins / self.total_trades) * 100
    
    @property
    def long_win_rate(self) -> float:
        """Calculate long trade win rate as percentage."""
        if self.long_trades == 0:
            return 0.0
        return (self.long_wins / self.long_trades) * 100
    
    @property
    def short_win_rate(self) -> float:
        """Calculate short trade win rate as percentage."""
        if self.short_trades == 0:
            return 0.0
        return (self.short_wins / self.short_trades) * 100


def load_csv_data(file_path):
    """Load CSV data from a file."""
    df = pd.read_csv(
        file_path,
        sep=';',
        header=0,
        names=['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
    )
    
    # Parse datetime
    df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%d/%m/%Y %H:%M:%S')
    df['TimeOnly'] = pd.to_datetime(df['Time'], format='%H:%M:%S').dt.time
    
    # Convert OHLC to numeric
    for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    return df


def extract_zip(zip_path):
    """Extract zip file and return the path to the extracted CSV."""
    extract_dir = os.path.dirname(zip_path)
    csv_name = os.path.basename(zip_path).replace('.zip', '')
    csv_path = os.path.join(extract_dir, csv_name)
    
    # Only extract if CSV doesn't already exist
    if not os.path.exists(csv_path):
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
    
    return csv_path


def get_file_path(year, timeframe, data_dir):
    """Get the file path for a given year and timeframe."""
    if timeframe == "1m":
        if year == 2025:
            csv_path = os.path.join(data_dir, f"{year} 1m.csv")
            if os.path.exists(csv_path):
                return csv_path
        else:
            # Check for zip file
            zip_path = os.path.join(data_dir, f"{year} 1m.csv.zip")
            if os.path.exists(zip_path):
                return extract_zip(zip_path)
    else:
        csv_path = os.path.join(data_dir, f"{year} {timeframe}.csv")
        if os.path.exists(csv_path):
            return csv_path
    
    return None


def count_impulsive_candles(df, lookback):
    """
    Count impulsive candles in the data.
    
    An impulsive candle is one where:
    - close > max(high of last N candles) [bullish breakout]
    - close < min(low of last N candles) [bearish breakout]
    """
    bullish_count = 0
    bearish_count = 0
    
    # Filter for time range (2:00 to 12:00)
    df_range = df[(df['TimeOnly'] >= TIME_START) & (df['TimeOnly'] <= TIME_END)].copy()
    
    if len(df_range) < lookback + 1:
        return bullish_count, bearish_count
    
    # Group by date to reset lookback window for each day
    for date, day_df in df_range.groupby(df_range['DateTime'].dt.date):
        day_df = day_df.reset_index(drop=True)
        
        if len(day_df) < lookback + 1:
            continue
        
        for i in range(lookback, len(day_df)):
            current_close = day_df.iloc[i]['Close']
            
            # Get the last N candles (excluding current)
            lookback_data = day_df.iloc[i - lookback:i]
            max_high = lookback_data['High'].max()
            min_low = lookback_data['Low'].min()
            
            # Check for bullish breakout
            if current_close > max_high:
                bullish_count += 1
            
            # Check for bearish breakout
            if current_close < min_low:
                bearish_count += 1
    
    return bullish_count, bearish_count


def run_backtest(df, lookback):
    """
    Run backtest on the data.
    
    Strategy:
    - Signal: When a candle closes above/below the range of last N candles
    - Entry: Open of the next candle after signal
    - Stop Loss: 100% of entry candle (Low for LONG, High for SHORT)
    - Take Profit: 1:1 Risk/Reward ratio
    
    Returns:
        BacktestResult object with all trade statistics
    """
    trades = []
    
    # Filter for time range (2:00 to 12:00)
    df_range = df[(df['TimeOnly'] >= TIME_START) & (df['TimeOnly'] <= TIME_END)].copy()
    
    if len(df_range) < lookback + 2:
        return trades
    
    # Group by date to reset lookback window for each day
    for date, day_df in df_range.groupby(df_range['DateTime'].dt.date):
        day_df = day_df.reset_index(drop=True)
        
        if len(day_df) < lookback + 2:
            continue
        
        i = lookback
        while i < len(day_df) - 1:
            current_close = day_df.iloc[i]['Close']
            
            # Get the last N candles (excluding current)
            lookback_data = day_df.iloc[i - lookback:i]
            max_high = lookback_data['High'].max()
            min_low = lookback_data['Low'].min()
            
            signal = None
            
            # Check for bullish breakout
            if current_close > max_high:
                signal = 'LONG'
            # Check for bearish breakout
            elif current_close < min_low:
                signal = 'SHORT'
            
            if signal:
                # Entry is at the open of the next candle
                entry_candle = day_df.iloc[i + 1]
                entry_price = entry_candle['Open']
                entry_date = entry_candle['DateTime']
                entry_high = entry_candle['High']
                entry_low = entry_candle['Low']
                
                if signal == 'LONG':
                    stop_loss = entry_low  # SL at low of entry candle
                    risk = entry_price - stop_loss
                    take_profit = entry_price + risk  # 1:1 RR
                else:  # SHORT
                    stop_loss = entry_high  # SL at high of entry candle
                    risk = stop_loss - entry_price
                    take_profit = entry_price - risk  # 1:1 RR
                
                # Avoid trades with zero risk (very rare edge case)
                if risk <= 0:
                    i += 1
                    continue
                
                trade = Trade(
                    entry_date=entry_date,
                    direction=signal,
                    entry_price=entry_price,
                    stop_loss=stop_loss,
                    take_profit=take_profit
                )
                
                # Evaluate trade on subsequent candles
                trade = evaluate_trade(day_df, i + 2, trade)
                trades.append(trade)
                
                # Move to next candle after entry
                i += 2
            else:
                i += 1
    
    return trades


def evaluate_trade(day_df, start_index, trade):
    """
    Evaluate if a trade hits TP or SL by checking subsequent candles.
    
    Args:
        day_df: DataFrame with candle data for the day
        start_index: Index to start checking from
        trade: Trade object to evaluate
    
    Returns:
        Updated Trade object with result
    """
    for j in range(start_index, len(day_df)):
        candle = day_df.iloc[j]
        high = candle['High']
        low = candle['Low']
        
        if trade.direction == 'LONG':
            # Check if TP hit first (using High) or SL hit (using Low)
            # Assumption: Within a candle, we check if price reached either level
            tp_hit = high >= trade.take_profit
            sl_hit = low <= trade.stop_loss
            
            if tp_hit and sl_hit:
                # Both levels hit in same candle - assume worst case (SL hit)
                # Since we can't know intrabar order, we assume loss
                trade.result = 'LOSS'
                trade.exit_price = trade.stop_loss
                trade.profit_points = trade.stop_loss - trade.entry_price
                break
            elif tp_hit:
                trade.result = 'WIN'
                trade.exit_price = trade.take_profit
                trade.profit_points = trade.take_profit - trade.entry_price
                break
            elif sl_hit:
                trade.result = 'LOSS'
                trade.exit_price = trade.stop_loss
                trade.profit_points = trade.stop_loss - trade.entry_price
                break
        
        else:  # SHORT
            # Check if TP hit first (using Low) or SL hit (using High)
            tp_hit = low <= trade.take_profit
            sl_hit = high >= trade.stop_loss
            
            if tp_hit and sl_hit:
                # Both levels hit in same candle - assume worst case (SL hit)
                trade.result = 'LOSS'
                trade.exit_price = trade.stop_loss
                trade.profit_points = trade.entry_price - trade.stop_loss
                break
            elif tp_hit:
                trade.result = 'WIN'
                trade.exit_price = trade.take_profit
                trade.profit_points = trade.entry_price - trade.take_profit
                break
            elif sl_hit:
                trade.result = 'LOSS'
                trade.exit_price = trade.stop_loss
                trade.profit_points = trade.entry_price - trade.stop_loss
                break
    
    # If we reach end of day without hitting TP or SL, 
    # close at last candle's close (mark to market)
    if trade.result is None and len(day_df) > start_index:
        last_candle = day_df.iloc[-1]
        trade.exit_price = last_candle['Close']
        if trade.direction == 'LONG':
            trade.profit_points = trade.exit_price - trade.entry_price
        else:
            trade.profit_points = trade.entry_price - trade.exit_price
        
        # Determine win/loss based on P&L
        if trade.profit_points >= 0:
            trade.result = 'WIN'
        else:
            trade.result = 'LOSS'
    
    return trade


def aggregate_backtest_results(trades: List[Trade], timeframe: str, lookback: int) -> BacktestResult:
    """
    Aggregate trade results into a BacktestResult object.
    
    Args:
        trades: List of Trade objects
        timeframe: Timeframe string (e.g., '1m', '5m', '15m')
        lookback: Lookback period used
    
    Returns:
        BacktestResult object with aggregated statistics
    """
    result = BacktestResult(timeframe=timeframe, lookback=lookback, trades=trades)
    
    for trade in trades:
        result.total_trades += 1
        
        if trade.direction == 'LONG':
            result.long_trades += 1
            if trade.result == 'WIN':
                result.long_wins += 1
                result.wins += 1
            else:
                result.losses += 1
        else:  # SHORT
            result.short_trades += 1
            if trade.result == 'WIN':
                result.short_wins += 1
                result.wins += 1
            else:
                result.losses += 1
        
        result.total_profit_points += trade.profit_points
    
    return result


def main(data_dir=None, years=None):
    """Main function to run the analysis."""
    if data_dir is None:
        data_dir = DEFAULT_DATA_DIR
    if years is None:
        years = DEFAULT_YEARS
    
    results = []
    
    print("Starting impulsive candles analysis...")
    print("=" * 60)
    
    for timeframe in TIMEFRAMES:
        print(f"\nProcessing {timeframe} data...")
        
        for lookback in LOOKBACK_PERIODS:
            total_bullish = 0
            total_bearish = 0
            yearly_data = {}
            
            for year in years:
                file_path = get_file_path(year, timeframe, data_dir)
                
                if file_path and os.path.exists(file_path):
                    print(f"  Loading {year} {timeframe}...")
                    try:
                        df = load_csv_data(file_path)
                        bullish, bearish = count_impulsive_candles(df, lookback)
                        total_bullish += bullish
                        total_bearish += bearish
                        yearly_data[year] = (bullish, bearish)
                        print(f"    {year}: Bullish={bullish}, Bearish={bearish}")
                    except Exception as e:
                        print(f"    Error processing {year} {timeframe}: {e}")
                else:
                    print(f"  File not found for {year} {timeframe}")
            
            total = total_bullish + total_bearish
            results.append({
                'Timeframe': timeframe,
                'Lookback': lookback,
                'Bullish_Count': total_bullish,
                'Bearish_Count': total_bearish,
                'Total_Count': total
            })
            
            print(f"  Lookback {lookback}: Total Bullish={total_bullish}, Bearish={total_bearish}, Total={total}")
    
    # Create results DataFrame
    results_df = pd.DataFrame(results)
    
    # Save to CSV
    output_path = os.path.join(data_dir, "impulsive_candles_analysis.csv")
    results_df.to_csv(output_path, index=False)
    print(f"\nResults saved to: {output_path}")
    
    # Also create a detailed text report
    report_path = os.path.join(data_dir, "impulsive_candles_analysis.txt")
    with open(report_path, 'w') as f:
        f.write("=" * 70 + "\n")
        f.write("IMPULSIVE CANDLES ANALYSIS REPORT\n")
        f.write("=" * 70 + "\n\n")
        f.write(f"Time Range: {TIME_START} to {TIME_END}\n")
        f.write(f"Years Analyzed: {list(years)}\n")
        f.write(f"Timeframes: {TIMEFRAMES}\n")
        f.write(f"Lookback Periods: {LOOKBACK_PERIODS}\n\n")
        
        f.write("Definition of Impulsive Candle:\n")
        f.write("- Bullish: Close > max(High of last N candles)\n")
        f.write("- Bearish: Close < min(Low of last N candles)\n\n")
        
        f.write("-" * 70 + "\n")
        f.write("SUMMARY TABLE\n")
        f.write("-" * 70 + "\n")
        f.write(f"{'Timeframe':<12} {'Lookback':<10} {'Bullish':<12} {'Bearish':<12} {'Total':<12}\n")
        f.write("-" * 70 + "\n")
        
        for _, row in results_df.iterrows():
            f.write(f"{row['Timeframe']:<12} {row['Lookback']:<10} {row['Bullish_Count']:<12} {row['Bearish_Count']:<12} {row['Total_Count']:<12}\n")
        
        f.write("-" * 70 + "\n")
    
    print(f"Detailed report saved to: {report_path}")
    
    # Print summary table
    print("\n" + "=" * 70)
    print("SUMMARY TABLE")
    print("=" * 70)
    print(f"{'Timeframe':<12} {'Lookback':<10} {'Bullish':<12} {'Bearish':<12} {'Total':<12}")
    print("-" * 70)
    for _, row in results_df.iterrows():
        print(f"{row['Timeframe']:<12} {row['Lookback']:<10} {row['Bullish_Count']:<12} {row['Bearish_Count']:<12} {row['Total_Count']:<12}")
    print("=" * 70)
    
    return results_df


def backtest_main(data_dir=None, years=None):
    """Main function to run the backtesting."""
    if data_dir is None:
        data_dir = DEFAULT_DATA_DIR
    if years is None:
        years = DEFAULT_YEARS
    
    all_results = []
    
    print("Starting backtesting...")
    print("=" * 70)
    
    for timeframe in TIMEFRAMES:
        print(f"\nProcessing {timeframe} data...")
        
        for lookback in LOOKBACK_PERIODS:
            all_trades = []
            
            for year in years:
                file_path = get_file_path(year, timeframe, data_dir)
                
                if file_path and os.path.exists(file_path):
                    print(f"  Loading {year} {timeframe} for backtest...")
                    try:
                        df = load_csv_data(file_path)
                        trades = run_backtest(df, lookback)
                        all_trades.extend(trades)
                        print(f"    {year}: {len(trades)} trades generated")
                    except Exception as e:
                        print(f"    Error processing {year} {timeframe}: {e}")
                else:
                    print(f"  File not found for {year} {timeframe}")
            
            # Aggregate results for this timeframe/lookback combination
            result = aggregate_backtest_results(all_trades, timeframe, lookback)
            all_results.append(result)
            
            print(f"  Lookback {lookback}: Trades={result.total_trades}, "
                  f"Wins={result.wins}, Losses={result.losses}, "
                  f"Win Rate={result.win_rate:.1f}%")
    
    # Create results DataFrame
    results_data = []
    for r in all_results:
        results_data.append({
            'Timeframe': r.timeframe,
            'Lookback': r.lookback,
            'Total_Trades': r.total_trades,
            'Wins': r.wins,
            'Losses': r.losses,
            'Win_Rate': round(r.win_rate, 2),
            'Long_Trades': r.long_trades,
            'Short_Trades': r.short_trades,
            'Long_Wins': r.long_wins,
            'Short_Wins': r.short_wins,
            'Long_Win_Rate': round(r.long_win_rate, 2),
            'Short_Win_Rate': round(r.short_win_rate, 2),
            'Total_Profit_Points': round(r.total_profit_points, 2)
        })
    
    results_df = pd.DataFrame(results_data)
    
    # Save to CSV
    output_path = os.path.join(data_dir, "backtest_results.csv")
    results_df.to_csv(output_path, index=False)
    print(f"\nBacktest results saved to: {output_path}")
    
    # Create detailed text report
    report_path = os.path.join(data_dir, "backtest_results.txt")
    with open(report_path, 'w') as f:
        f.write("=" * 90 + "\n")
        f.write("BACKTEST RESULTS REPORT\n")
        f.write("=" * 90 + "\n\n")
        f.write(f"Time Range: {TIME_START} to {TIME_END}\n")
        f.write(f"Years Analyzed: {list(years)}\n")
        f.write(f"Timeframes: {TIMEFRAMES}\n")
        f.write(f"Lookback Periods: {LOOKBACK_PERIODS}\n\n")
        
        f.write("Strategy Rules:\n")
        f.write("-" * 40 + "\n")
        f.write("Signal Detection:\n")
        f.write("  - Bullish: Close > max(High of last N candles)\n")
        f.write("  - Bearish: Close < min(Low of last N candles)\n\n")
        f.write("Entry Rules:\n")
        f.write("  - Enter at OPEN of the next candle after signal\n")
        f.write("  - LONG if signal is bullish, SHORT if bearish\n\n")
        f.write("Risk Management:\n")
        f.write("  - Stop Loss: 100% of entry candle\n")
        f.write("    (Low for LONG, High for SHORT)\n")
        f.write("  - Take Profit: 1:1 Risk/Reward ratio\n\n")
        
        f.write("-" * 90 + "\n")
        f.write("SUMMARY TABLE\n")
        f.write("-" * 90 + "\n")
        header = f"{'TF':<6} {'LB':<5} {'Trades':<8} {'Wins':<6} {'Losses':<8} {'Win%':<8} "
        header += f"{'Long':<6} {'Short':<7} {'L_Win%':<8} {'S_Win%':<8} {'Profit':<12}\n"
        f.write(header)
        f.write("-" * 90 + "\n")
        
        for _, row in results_df.iterrows():
            line = f"{row['Timeframe']:<6} {row['Lookback']:<5} {row['Total_Trades']:<8} "
            line += f"{row['Wins']:<6} {row['Losses']:<8} {row['Win_Rate']:<8.1f} "
            line += f"{row['Long_Trades']:<6} {row['Short_Trades']:<7} "
            line += f"{row['Long_Win_Rate']:<8.1f} {row['Short_Win_Rate']:<8.1f} "
            line += f"{row['Total_Profit_Points']:<12.2f}\n"
            f.write(line)
        
        f.write("-" * 90 + "\n\n")
        
        # Summary statistics
        total_trades = results_df['Total_Trades'].sum()
        total_wins = results_df['Wins'].sum()
        total_losses = results_df['Losses'].sum()
        total_profit = results_df['Total_Profit_Points'].sum()
        overall_win_rate = (total_wins / total_trades * 100) if total_trades > 0 else 0
        
        f.write("OVERALL SUMMARY\n")
        f.write("-" * 40 + "\n")
        f.write(f"Total Trades: {total_trades}\n")
        f.write(f"Total Wins: {total_wins}\n")
        f.write(f"Total Losses: {total_losses}\n")
        f.write(f"Overall Win Rate: {overall_win_rate:.2f}%\n")
        f.write(f"Total Profit (points): {total_profit:.2f}\n")
        f.write("=" * 90 + "\n")
    
    print(f"Detailed report saved to: {report_path}")
    
    # Print summary table
    print("\n" + "=" * 90)
    print("BACKTEST RESULTS SUMMARY")
    print("=" * 90)
    header = f"{'TF':<6} {'LB':<5} {'Trades':<8} {'Wins':<6} {'Losses':<8} {'Win%':<8} "
    header += f"{'Long':<6} {'Short':<7} {'L_Win%':<8} {'S_Win%':<8} {'Profit':<12}"
    print(header)
    print("-" * 90)
    
    for _, row in results_df.iterrows():
        line = f"{row['Timeframe']:<6} {row['Lookback']:<5} {row['Total_Trades']:<8} "
        line += f"{row['Wins']:<6} {row['Losses']:<8} {row['Win_Rate']:<8.1f} "
        line += f"{row['Long_Trades']:<6} {row['Short_Trades']:<7} "
        line += f"{row['Long_Win_Rate']:<8.1f} {row['Short_Win_Rate']:<8.1f} "
        line += f"{row['Total_Profit_Points']:<12.2f}"
        print(line)
    
    print("=" * 90)
    
    # Print overall summary
    total_trades = results_df['Total_Trades'].sum()
    total_wins = results_df['Wins'].sum()
    total_losses = results_df['Losses'].sum()
    total_profit = results_df['Total_Profit_Points'].sum()
    overall_win_rate = (total_wins / total_trades * 100) if total_trades > 0 else 0
    
    print(f"\nOVERALL: Trades={total_trades}, Wins={total_wins}, Losses={total_losses}, "
          f"Win Rate={overall_win_rate:.2f}%, Profit={total_profit:.2f} points")
    
    return results_df


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze trading data for impulsive candles")
    parser.add_argument("--data-dir", type=str, default=None,
                        help="Directory containing the CSV data files")
    parser.add_argument("--start-year", type=int, default=2018,
                        help="First year to analyze (default: 2018)")
    parser.add_argument("--end-year", type=int, default=2025,
                        help="Last year to analyze (default: 2025)")
    parser.add_argument("--backtest", action="store_true",
                        help="Run backtesting instead of just counting impulsive candles")
    parser.add_argument("--both", action="store_true",
                        help="Run both analysis and backtesting")
    args = parser.parse_args()
    
    years = range(args.start_year, args.end_year + 1)
    
    if args.both:
        main(data_dir=args.data_dir, years=years)
        print("\n" + "=" * 90 + "\n")
        backtest_main(data_dir=args.data_dir, years=years)
    elif args.backtest:
        backtest_main(data_dir=args.data_dir, years=years)
    else:
        main(data_dir=args.data_dir, years=years)

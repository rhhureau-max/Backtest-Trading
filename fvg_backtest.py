#!/usr/bin/env python3
"""
FVG Backtest Script for Nasdaq 5-Minute Data Analysis

This script analyzes Fair Value Gaps (FVG) on Nasdaq 5-minute data from 2018-2025.
It identifies FVGs, detects break signals, simulates trades, and generates performance reports.

Strategy:
- Entry: After 8:30 AM Chicago (15:30 Paris time)
- Bullish FVG: Gap between HIGH of candle N-2 and LOW of candle N
- Bearish FVG: Gap between LOW of candle N-2 and HIGH of candle N
- Long Signal: Bearish FVG broken (price closes ABOVE top of FVG)
- Short Signal: Bullish FVG broken (price closes BELOW bottom of FVG)
- SL: Below filled FVG (long) or above (short)
- TP: Various Risk/Reward ratios tested
"""

import os
from dataclasses import dataclass
from typing import Optional

import numpy as np
import pandas as pd


# =============================================================================
# Configuration Constants
# =============================================================================

# Trading session start time (Paris timezone)
# This corresponds to 8:30 AM Chicago time when US markets open
TRADING_START_TIME = "15:30:00"

# Default years to analyze (2018-2025)
DEFAULT_YEARS = list(range(2018, 2026))

# Risk/Reward ratios to test
DEFAULT_RR_RATIOS = [1.5, 2.0, 2.5, 3.0, 5.0]


# =============================================================================
# Data Classes
# =============================================================================

@dataclass
class Trade:
    """Represents a trade."""
    entry_time: pd.Timestamp
    direction: str  # 'long' or 'short'
    entry_price: float
    stop_loss: float
    take_profit: float
    rr_ratio: float
    exit_time: Optional[pd.Timestamp] = None
    exit_price: Optional[float] = None
    result: Optional[str] = None  # 'win', 'loss', or 'open'
    pnl_rr: Optional[float] = None


# =============================================================================
# Data Loading Functions
# =============================================================================

def load_data(data_dir: str, years: list = None) -> pd.DataFrame:
    """
    Load and concatenate all 5-minute CSV data files.
    
    Args:
        data_dir: Directory containing the CSV files
        years: List of years to load (default: DEFAULT_YEARS)
    
    Returns:
        DataFrame with datetime index and OHLCV columns
    """
    if years is None:
        years = DEFAULT_YEARS
    
    dfs = []
    for year in years:
        file_path = os.path.join(data_dir, f"{year} 5m.csv")
        if os.path.exists(file_path):
            df = pd.read_csv(
                file_path,
                delimiter=';',
                names=['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume'],
                skiprows=1  # Skip header row
            )
            dfs.append(df)
            print(f"Loaded {file_path}: {len(df)} rows")
        else:
            print(f"Warning: {file_path} not found")
    
    if not dfs:
        raise ValueError("No data files found!")
    
    # Concatenate all dataframes
    data = pd.concat(dfs, ignore_index=True)
    
    # Parse datetime
    data['Datetime'] = pd.to_datetime(
        data['Date'] + ' ' + data['Time'],
        format='%d/%m/%Y %H:%M:%S'
    )
    
    # Set datetime as index
    data.set_index('Datetime', inplace=True)
    data.sort_index(inplace=True)
    
    # Convert price columns to float
    for col in ['Open', 'High', 'Low', 'Close']:
        data[col] = pd.to_numeric(data[col], errors='coerce')
    
    data['Volume'] = pd.to_numeric(data['Volume'], errors='coerce')
    
    # Drop rows with missing values
    data.dropna(subset=['Open', 'High', 'Low', 'Close'], inplace=True)
    
    # Add year column for later analysis
    data['Year'] = data.index.year
    
    # Add date column for grouping
    data['TradingDate'] = data.index.date
    
    print(f"\nTotal data loaded: {len(data)} rows")
    print(f"Date range: {data.index.min()} to {data.index.max()}")
    
    return data


# =============================================================================
# Optimized FVG Detection Functions (Vectorized)
# =============================================================================

def detect_fvgs_vectorized(data: pd.DataFrame) -> pd.DataFrame:
    """
    Identify all FVGs in the data after trading start time using vectorized operations.
    
    Bullish FVG: Gap between HIGH of candle N-2 and LOW of candle N
                 (middle candle N-1 is a strong bullish candle)
    
    Bearish FVG: Gap between LOW of candle N-2 and HIGH of candle N
                 (middle candle N-1 is a strong bearish candle)
    
    Args:
        data: DataFrame with OHLCV data
    
    Returns:
        DataFrame with FVG information
    """
    # Filter data after trading start time (Paris timezone)
    trading_start = pd.Timestamp(TRADING_START_TIME).time()
    time_filter = data.index.time >= trading_start
    df = data[time_filter].copy()
    
    if len(df) < 3:
        return pd.DataFrame()
    
    # Create shifted columns for candle N-2 and N-1
    df['High_n2'] = df['High'].shift(2)
    df['Low_n2'] = df['Low'].shift(2)
    df['Open_n1'] = df['Open'].shift(1)
    df['Close_n1'] = df['Close'].shift(1)
    df['Date_n2'] = df['TradingDate'].shift(2)
    
    # Drop first 2 rows (no valid N-2 candle)
    df = df.iloc[2:]
    
    # Filter to same day only
    df = df[df['TradingDate'] == df['Date_n2']]
    
    # Detect Bullish FVG: Low_n > High_n2 and middle candle is bullish
    bullish_mask = (df['Low'] > df['High_n2']) & (df['Close_n1'] > df['Open_n1'])
    
    # Detect Bearish FVG: High_n < Low_n2 and middle candle is bearish
    bearish_mask = (df['High'] < df['Low_n2']) & (df['Close_n1'] < df['Open_n1'])
    
    # Create FVG dataframe
    fvg_records = []
    
    # Bullish FVGs
    bullish_fvgs = df[bullish_mask]
    for idx in bullish_fvgs.index:
        fvg_records.append({
            'timestamp': idx,
            'fvg_type': 'bullish',
            'top': bullish_fvgs.loc[idx, 'Low'],        # Top of gap = LOW of candle N
            'bottom': bullish_fvgs.loc[idx, 'High_n2'], # Bottom of gap = HIGH of candle N-2
            'trading_date': bullish_fvgs.loc[idx, 'TradingDate']
        })
    
    # Bearish FVGs
    bearish_fvgs = df[bearish_mask]
    for idx in bearish_fvgs.index:
        fvg_records.append({
            'timestamp': idx,
            'fvg_type': 'bearish',
            'top': bearish_fvgs.loc[idx, 'Low_n2'],    # Top of gap = LOW of candle N-2
            'bottom': bearish_fvgs.loc[idx, 'High'],   # Bottom of gap = HIGH of candle N
            'trading_date': bearish_fvgs.loc[idx, 'TradingDate']
        })
    
    if not fvg_records:
        return pd.DataFrame()
    
    fvg_df = pd.DataFrame(fvg_records)
    fvg_df = fvg_df.sort_values('timestamp').reset_index(drop=True)
    
    print(f"\nDetected {len(fvg_df)} FVGs")
    bullish_count = (fvg_df['fvg_type'] == 'bullish').sum()
    bearish_count = (fvg_df['fvg_type'] == 'bearish').sum()
    print(f"  - Bullish FVGs: {bullish_count}")
    print(f"  - Bearish FVGs: {bearish_count}")
    
    return fvg_df


# =============================================================================
# Optimized FVG Break Detection and Trade Simulation
# =============================================================================

def process_fvg_breaks_and_trades(data: pd.DataFrame, fvg_df: pd.DataFrame, rr_ratios: list) -> list:
    """
    Process all FVGs to find breaks and generate trades using optimized operations.
    
    For Bearish FVG: price returns to FVG and closes ABOVE top → LONG signal
    For Bullish FVG: price returns to FVG and closes BELOW bottom → SHORT signal
    
    Args:
        data: DataFrame with OHLCV data
        fvg_df: DataFrame with FVG information
        rr_ratios: List of Risk/Reward ratios to test
    
    Returns:
        List of Trade objects
    """
    all_trades = []
    
    # Group data by trading date for faster lookup
    data_by_date = {date: group for date, group in data.groupby('TradingDate')}
    
    total_fvgs = len(fvg_df)
    print_interval = max(1, total_fvgs // 10)
    
    for i, fvg_row in fvg_df.iterrows():
        if (i + 1) % print_interval == 0:
            print(f"  Processing FVG {i + 1}/{total_fvgs}...")
        
        fvg_timestamp = fvg_row['timestamp']
        fvg_type = fvg_row['fvg_type']
        fvg_top = fvg_row['top']
        fvg_bottom = fvg_row['bottom']
        trading_date = fvg_row['trading_date']
        
        # Get same-day data after FVG formation
        if trading_date not in data_by_date:
            continue
        
        day_data = data_by_date[trading_date]
        future_data = day_data[day_data.index > fvg_timestamp]
        
        if len(future_data) == 0:
            continue
        
        # Find break candle
        trade_generated = False
        
        for idx in future_data.index:
            if trade_generated:
                break
                
            close = future_data.loc[idx, 'Close']
            
            # Bearish FVG break → LONG signal
            if fvg_type == 'bearish' and close > fvg_top:
                entry_price = close
                stop_loss = fvg_bottom
                risk = entry_price - stop_loss
                
                if risk > 0:
                    for rr in rr_ratios:
                        take_profit = entry_price + (risk * rr)
                        trade = Trade(
                            entry_time=idx,
                            direction='long',
                            entry_price=entry_price,
                            stop_loss=stop_loss,
                            take_profit=take_profit,
                            rr_ratio=rr
                        )
                        all_trades.append(trade)
                    trade_generated = True
            
            # Bullish FVG break → SHORT signal
            elif fvg_type == 'bullish' and close < fvg_bottom:
                entry_price = close
                stop_loss = fvg_top
                risk = stop_loss - entry_price
                
                if risk > 0:
                    for rr in rr_ratios:
                        take_profit = entry_price - (risk * rr)
                        trade = Trade(
                            entry_time=idx,
                            direction='short',
                            entry_price=entry_price,
                            stop_loss=stop_loss,
                            take_profit=take_profit,
                            rr_ratio=rr
                        )
                        all_trades.append(trade)
                    trade_generated = True
    
    return all_trades


def simulate_trades_batch(data: pd.DataFrame, trades: list) -> list:
    """
    Simulate all trades to determine outcomes using optimized batch processing.
    
    Args:
        data: DataFrame with OHLCV data
        trades: List of Trade objects
    
    Returns:
        List of updated Trade objects with exit info
    """
    if not trades:
        return trades
    
    print(f"\n  Simulating {len(trades)} trades...")
    
    # Convert data to numpy for faster access
    data_index = data.index.values
    data_high = data['High'].values
    data_low = data['Low'].values
    
    # Create index lookup
    index_positions = {ts: i for i, ts in enumerate(data_index)}
    
    total_trades = len(trades)
    print_interval = max(1, total_trades // 10)
    
    for i, trade in enumerate(trades):
        if (i + 1) % print_interval == 0:
            print(f"    Simulating trade {i + 1}/{total_trades}...")
        
        entry_ts = trade.entry_time
        if entry_ts not in index_positions:
            trade.result = 'open'
            continue
        
        start_pos = index_positions[entry_ts] + 1
        
        if start_pos >= len(data_index):
            trade.result = 'open'
            continue
        
        # Iterate through future data
        for pos in range(start_pos, len(data_index)):
            high = data_high[pos]
            low = data_low[pos]
            
            if trade.direction == 'long':
                # Check if SL hit first (use low)
                if low <= trade.stop_loss:
                    trade.exit_time = pd.Timestamp(data_index[pos])
                    trade.exit_price = trade.stop_loss
                    trade.result = 'loss'
                    trade.pnl_rr = -1.0
                    break
                
                # Check if TP hit (use high)
                if high >= trade.take_profit:
                    trade.exit_time = pd.Timestamp(data_index[pos])
                    trade.exit_price = trade.take_profit
                    trade.result = 'win'
                    trade.pnl_rr = trade.rr_ratio
                    break
            
            else:  # short
                # Check if SL hit first (use high)
                if high >= trade.stop_loss:
                    trade.exit_time = pd.Timestamp(data_index[pos])
                    trade.exit_price = trade.stop_loss
                    trade.result = 'loss'
                    trade.pnl_rr = -1.0
                    break
                
                # Check if TP hit (use low)
                if low <= trade.take_profit:
                    trade.exit_time = pd.Timestamp(data_index[pos])
                    trade.exit_price = trade.take_profit
                    trade.result = 'win'
                    trade.pnl_rr = trade.rr_ratio
                    break
        else:
            # Trade still open at end of data
            trade.result = 'open'
    
    return trades


# =============================================================================
# Statistics Calculation
# =============================================================================

def calculate_statistics(trades: list) -> dict:
    """
    Calculate performance statistics for a list of trades.
    
    Args:
        trades: List of Trade objects
    
    Returns:
        Dictionary with statistics
    """
    if not trades:
        return {
            'total_trades': 0,
            'closed_trades': 0,
            'wins': 0,
            'losses': 0,
            'open': 0,
            'win_rate': 0.0,
            'profit_factor': 0.0,
            'total_pnl_rr': 0.0
        }
    
    closed_trades = [t for t in trades if t.result in ['win', 'loss']]
    wins = [t for t in closed_trades if t.result == 'win']
    losses = [t for t in closed_trades if t.result == 'loss']
    open_trades = [t for t in trades if t.result == 'open']
    
    total_wins = sum(t.pnl_rr for t in wins) if wins else 0
    total_losses = abs(sum(t.pnl_rr for t in losses)) if losses else 0
    
    win_rate = (len(wins) / len(closed_trades) * 100) if closed_trades else 0
    profit_factor = (total_wins / total_losses) if total_losses > 0 else float('inf') if total_wins > 0 else 0
    
    return {
        'total_trades': len(trades),
        'closed_trades': len(closed_trades),
        'wins': len(wins),
        'losses': len(losses),
        'open': len(open_trades),
        'win_rate': win_rate,
        'profit_factor': profit_factor,
        'total_pnl_rr': sum(t.pnl_rr for t in closed_trades if t.pnl_rr is not None)
    }


def calculate_statistics_by_rr(trades: list, rr_ratios: list) -> dict:
    """
    Calculate statistics grouped by RR ratio.
    
    Args:
        trades: List of Trade objects
        rr_ratios: List of RR ratios
    
    Returns:
        Dictionary with statistics per RR
    """
    stats_by_rr = {}
    for rr in rr_ratios:
        rr_trades = [t for t in trades if t.rr_ratio == rr]
        stats_by_rr[rr] = calculate_statistics(rr_trades)
    return stats_by_rr


def calculate_statistics_by_direction(trades: list) -> dict:
    """
    Calculate statistics grouped by trade direction.
    
    Args:
        trades: List of Trade objects
    
    Returns:
        Dictionary with statistics per direction
    """
    long_trades = [t for t in trades if t.direction == 'long']
    short_trades = [t for t in trades if t.direction == 'short']
    
    return {
        'long': calculate_statistics(long_trades),
        'short': calculate_statistics(short_trades)
    }


def calculate_statistics_by_year(trades: list) -> dict:
    """
    Calculate statistics grouped by year.
    
    Args:
        trades: List of Trade objects
    
    Returns:
        Dictionary with statistics per year
    """
    stats_by_year = {}
    years = set(t.entry_time.year for t in trades)
    
    for year in sorted(years):
        year_trades = [t for t in trades if t.entry_time.year == year]
        stats_by_year[year] = calculate_statistics(year_trades)
    
    return stats_by_year


# =============================================================================
# Report Generation
# =============================================================================

def generate_report(trades: list, rr_ratios: list) -> str:
    """
    Generate a comprehensive performance report.
    
    Args:
        trades: List of Trade objects
        rr_ratios: List of RR ratios tested
    
    Returns:
        Report as string
    """
    report_lines = []
    report_lines.append("=" * 80)
    report_lines.append("FVG BACKTEST RESULTS REPORT")
    report_lines.append("=" * 80)
    report_lines.append("")
    
    # Overall Statistics
    report_lines.append("-" * 80)
    report_lines.append("OVERALL STATISTICS")
    report_lines.append("-" * 80)
    overall_stats = calculate_statistics(trades)
    report_lines.append(f"Total Trades: {overall_stats['total_trades']}")
    report_lines.append(f"Closed Trades: {overall_stats['closed_trades']}")
    report_lines.append(f"Open Trades: {overall_stats['open']}")
    report_lines.append("")
    
    # Statistics by RR
    report_lines.append("-" * 80)
    report_lines.append("STATISTICS BY RISK/REWARD RATIO")
    report_lines.append("-" * 80)
    
    stats_by_rr = calculate_statistics_by_rr(trades, rr_ratios)
    
    for rr in rr_ratios:
        stats = stats_by_rr[rr]
        report_lines.append(f"\n  RR {rr}:")
        report_lines.append(f"    Total Trades: {stats['total_trades']}")
        report_lines.append(f"    Wins: {stats['wins']}")
        report_lines.append(f"    Losses: {stats['losses']}")
        report_lines.append(f"    Win Rate: {stats['win_rate']:.2f}%")
        report_lines.append(f"    Profit Factor: {stats['profit_factor']:.2f}")
        report_lines.append(f"    Total P&L (in R): {stats['total_pnl_rr']:.2f}")
    
    # Statistics by Direction
    report_lines.append("")
    report_lines.append("-" * 80)
    report_lines.append("STATISTICS BY DIRECTION")
    report_lines.append("-" * 80)
    
    for rr in rr_ratios:
        rr_trades = [t for t in trades if t.rr_ratio == rr]
        stats_by_dir = calculate_statistics_by_direction(rr_trades)
        
        report_lines.append(f"\n  RR {rr}:")
        
        for direction in ['long', 'short']:
            stats = stats_by_dir[direction]
            report_lines.append(f"\n    {direction.upper()}:")
            report_lines.append(f"      Total Trades: {stats['total_trades']}")
            report_lines.append(f"      Wins: {stats['wins']}")
            report_lines.append(f"      Losses: {stats['losses']}")
            report_lines.append(f"      Win Rate: {stats['win_rate']:.2f}%")
            report_lines.append(f"      Profit Factor: {stats['profit_factor']:.2f}")
            report_lines.append(f"      Total P&L (in R): {stats['total_pnl_rr']:.2f}")
    
    # Statistics by Year
    report_lines.append("")
    report_lines.append("-" * 80)
    report_lines.append("STATISTICS BY YEAR")
    report_lines.append("-" * 80)
    
    for rr in rr_ratios:
        rr_trades = [t for t in trades if t.rr_ratio == rr]
        stats_by_year = calculate_statistics_by_year(rr_trades)
        
        report_lines.append(f"\n  RR {rr}:")
        
        for year in sorted(stats_by_year.keys()):
            stats = stats_by_year[year]
            report_lines.append(f"\n    {year}:")
            report_lines.append(f"      Total Trades: {stats['total_trades']}")
            report_lines.append(f"      Wins: {stats['wins']}")
            report_lines.append(f"      Losses: {stats['losses']}")
            report_lines.append(f"      Win Rate: {stats['win_rate']:.2f}%")
            report_lines.append(f"      Profit Factor: {stats['profit_factor']:.2f}")
            report_lines.append(f"      Total P&L (in R): {stats['total_pnl_rr']:.2f}")
    
    report_lines.append("")
    report_lines.append("=" * 80)
    report_lines.append("END OF REPORT")
    report_lines.append("=" * 80)
    
    return "\n".join(report_lines)


def export_trades_to_csv(trades: list, filepath: str):
    """
    Export all trades to a CSV file.
    
    Args:
        trades: List of Trade objects
        filepath: Path to save the CSV file
    """
    if not trades:
        print("No trades to export")
        return
    
    data = []
    for t in trades:
        data.append({
            'entry_time': t.entry_time,
            'direction': t.direction,
            'entry_price': t.entry_price,
            'stop_loss': t.stop_loss,
            'take_profit': t.take_profit,
            'rr_ratio': t.rr_ratio,
            'exit_time': t.exit_time,
            'exit_price': t.exit_price,
            'result': t.result,
            'pnl_rr': t.pnl_rr,
            'year': t.entry_time.year
        })
    
    df = pd.DataFrame(data)
    df.to_csv(filepath, index=False)
    print(f"Trades exported to {filepath}")


def export_summary_to_csv(trades: list, rr_ratios: list, filepath: str):
    """
    Export summary statistics to a CSV file.
    
    Args:
        trades: List of Trade objects
        rr_ratios: List of RR ratios
        filepath: Path to save the CSV file
    """
    rows = []
    
    for rr in rr_ratios:
        rr_trades = [t for t in trades if t.rr_ratio == rr]
        
        # Overall for this RR
        overall_stats = calculate_statistics(rr_trades)
        rows.append({
            'rr_ratio': rr,
            'category': 'overall',
            'subcategory': 'all',
            'total_trades': overall_stats['total_trades'],
            'closed_trades': overall_stats['closed_trades'],
            'wins': overall_stats['wins'],
            'losses': overall_stats['losses'],
            'open': overall_stats['open'],
            'win_rate': overall_stats['win_rate'],
            'profit_factor': overall_stats['profit_factor'],
            'total_pnl_rr': overall_stats['total_pnl_rr']
        })
        
        # By direction
        stats_by_dir = calculate_statistics_by_direction(rr_trades)
        for direction in ['long', 'short']:
            stats = stats_by_dir[direction]
            rows.append({
                'rr_ratio': rr,
                'category': 'direction',
                'subcategory': direction,
                'total_trades': stats['total_trades'],
                'closed_trades': stats['closed_trades'],
                'wins': stats['wins'],
                'losses': stats['losses'],
                'open': stats['open'],
                'win_rate': stats['win_rate'],
                'profit_factor': stats['profit_factor'],
                'total_pnl_rr': stats['total_pnl_rr']
            })
        
        # By year
        stats_by_year = calculate_statistics_by_year(rr_trades)
        for year in sorted(stats_by_year.keys()):
            stats = stats_by_year[year]
            rows.append({
                'rr_ratio': rr,
                'category': 'year',
                'subcategory': str(year),
                'total_trades': stats['total_trades'],
                'closed_trades': stats['closed_trades'],
                'wins': stats['wins'],
                'losses': stats['losses'],
                'open': stats['open'],
                'win_rate': stats['win_rate'],
                'profit_factor': stats['profit_factor'],
                'total_pnl_rr': stats['total_pnl_rr']
            })
    
    df = pd.DataFrame(rows)
    df.to_csv(filepath, index=False)
    print(f"Summary statistics exported to {filepath}")


# =============================================================================
# Main Function
# =============================================================================

def main():
    """Main function to run the FVG backtest."""
    print("=" * 80)
    print("FVG BACKTEST - NASDAQ 5-MINUTE DATA")
    print("=" * 80)
    print()
    
    # Configuration - using defined constants
    data_dir = os.path.dirname(os.path.abspath(__file__))
    rr_ratios = DEFAULT_RR_RATIOS
    years = DEFAULT_YEARS
    
    # Step 1: Load data
    print("Step 1: Loading data...")
    data = load_data(data_dir, years)
    
    # Step 2: Detect FVGs using vectorized operations
    print("\nStep 2: Detecting FVGs...")
    fvg_df = detect_fvgs_vectorized(data)
    
    if len(fvg_df) == 0:
        print("No FVGs detected. Exiting.")
        return
    
    # Step 3: Process FVG breaks and generate trades
    print("\nStep 3: Detecting FVG breaks and generating trades...")
    all_trades = process_fvg_breaks_and_trades(data, fvg_df, rr_ratios)
    
    print(f"\nTotal trades generated: {len(all_trades)}")
    
    if not all_trades:
        print("No trades generated. Exiting.")
        return
    
    # Step 4: Simulate trades
    print("\nStep 4: Simulating trades...")
    all_trades = simulate_trades_batch(data, all_trades)
    
    # Step 5: Generate report
    print("\nStep 5: Generating report...")
    report = generate_report(all_trades, rr_ratios)
    print(report)
    
    # Save report to file
    report_path = os.path.join(data_dir, "fvg_backtest_report.txt")
    with open(report_path, 'w') as f:
        f.write(report)
    print(f"\nReport saved to {report_path}")
    
    # Step 6: Export to CSV
    print("\nStep 6: Exporting results to CSV...")
    trades_csv_path = os.path.join(data_dir, "fvg_backtest_trades.csv")
    export_trades_to_csv(all_trades, trades_csv_path)
    
    summary_csv_path = os.path.join(data_dir, "fvg_backtest_summary.csv")
    export_summary_to_csv(all_trades, rr_ratios, summary_csv_path)
    
    print("\n" + "=" * 80)
    print("BACKTEST COMPLETE!")
    print("=" * 80)


if __name__ == "__main__":
    main()

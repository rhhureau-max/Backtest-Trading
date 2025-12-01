#!/usr/bin/env python3
"""
NY Opening First Candle Backtesting Strategy

Strategy Description:
- Entry Condition: The 15:30 candle must close ABOVE or BELOW the closes of the 5 previous candles
  - LONG: 15:30 candle close is higher than ALL 5 previous closes
  - SHORT: 15:30 candle close is lower than ALL 5 previous closes

- Stop Loss: Based on the 8:30 candle retracement levels (25%, 50%, 75%, 100%)
  - For LONG: SL is below entry at X% retracement of 8:30 candle range
  - For SHORT: SL is above entry at X% retracement of 8:30 candle range

- Risk/Reward Ratios: 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0
"""

import pandas as pd
import os
from datetime import datetime, timedelta
from collections import defaultdict
import warnings

warnings.filterwarnings('ignore')

# Configuration - Use the directory where this script is located
DATA_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILES = [
    "2018 15m.csv", "2019 15m.csv", "2020 15m.csv", "2021 15m.csv",
    "2022 15m.csv", "2023 15m.csv", "2024 15m.csv", "2025 15m.csv"
]

# Entry time (NY opening)
ENTRY_TIME = "15:30:00"
# 8:30 candle time (used for SL calculation)
MORNING_CANDLE_TIME = "08:30:00"

# SL retracement levels
SL_LEVELS = [0.25, 0.50, 0.75, 1.00]

# Risk/Reward ratios
RR_RATIOS = [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]


def load_data(file_path):
    """Load CSV data with proper formatting."""
    df = pd.read_csv(
        file_path,
        sep=';',
        names=['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume'],
        skiprows=1
    )
    # Convert to proper datetime
    df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%d/%m/%Y %H:%M:%S')
    df['DateOnly'] = df['Datetime'].dt.date
    return df


def get_candle_at_time(df, date, time_str):
    """Get a specific candle at a given date and time."""
    mask = (df['DateOnly'] == date) & (df['Time'] == time_str)
    candles = df[mask]
    if len(candles) > 0:
        return candles.iloc[0]
    return None


def get_previous_candles(df, date, time_str, n=5):
    """Get n candles before the specified time on the same date."""
    # Get all candles for the given date up to (but not including) the specified time
    mask = (df['DateOnly'] == date) & (df['Time'] < time_str)
    day_candles = df[mask].sort_values('Time')
    
    if len(day_candles) >= n:
        return day_candles.tail(n)
    return None


def get_remaining_day_candles(df, date, time_str):
    """Get all candles after the specified time on the same date."""
    mask = (df['DateOnly'] == date) & (df['Time'] > time_str)
    return df[mask].sort_values('Time')


def check_entry_condition(entry_candle, prev_candles):
    """
    Check if entry condition is met.
    Returns: 'LONG', 'SHORT', or None
    """
    entry_close = entry_candle['Close']
    prev_closes = prev_candles['Close'].values
    
    # LONG: entry close is higher than ALL 5 previous closes
    if all(entry_close > c for c in prev_closes):
        return 'LONG'
    
    # SHORT: entry close is lower than ALL 5 previous closes
    if all(entry_close < c for c in prev_closes):
        return 'SHORT'
    
    return None


def calculate_sl_price(direction, entry_price, morning_candle, sl_level):
    """
    Calculate Stop Loss price based on morning candle retracement.
    
    For LONG: SL is placed below entry, at a distance equal to sl_level * morning candle range
    For SHORT: SL is placed above entry, at a distance equal to sl_level * morning candle range
    """
    morning_range = abs(morning_candle['High'] - morning_candle['Low'])
    sl_distance = morning_range * sl_level
    
    if direction == 'LONG':
        return entry_price - sl_distance
    else:  # SHORT
        return entry_price + sl_distance


def calculate_tp_price(direction, entry_price, sl_price, rr_ratio):
    """Calculate Take Profit price based on R:R ratio."""
    risk = abs(entry_price - sl_price)
    reward = risk * rr_ratio
    
    if direction == 'LONG':
        return entry_price + reward
    else:  # SHORT
        return entry_price - reward


def calculate_expectancy(wins, losses, rr_ratio):
    """
    Calculate trading expectancy.
    
    Expectancy = (Win Rate × R:R) - (Loss Rate × 1)
    
    A positive expectancy indicates a profitable strategy over time.
    The value represents the expected R multiple per trade.
    
    Args:
        wins: Number of winning trades
        losses: Number of losing trades  
        rr_ratio: Risk/Reward ratio
        
    Returns:
        float: Expectancy value, or None if no resolved trades
    """
    resolved = wins + losses
    if resolved == 0:
        return None
    win_rate = wins / resolved
    loss_rate = losses / resolved
    return (win_rate * rr_ratio) - (loss_rate * 1)


def check_trade_outcome(direction, entry_price, sl_price, tp_price, subsequent_candles):
    """
    Check if trade hits TP or SL first using subsequent candles.
    Returns: 'WIN', 'LOSS', or 'NO_RESULT' (if neither hit)
    
    When both SL and TP are hit in the same candle, we conservatively assume LOSS
    since we cannot definitively determine which level was hit first with 15-minute data.
    """
    for _, candle in subsequent_candles.iterrows():
        high = candle['High']
        low = candle['Low']
        
        if direction == 'LONG':
            sl_hit = low <= sl_price
            tp_hit = high >= tp_price
            
            # If both hit in same candle, conservatively count as loss
            if sl_hit and tp_hit:
                return 'LOSS'
            if sl_hit:
                return 'LOSS'
            if tp_hit:
                return 'WIN'
        else:  # SHORT
            sl_hit = high >= sl_price
            tp_hit = low <= tp_price
            
            # If both hit in same candle, conservatively count as loss
            if sl_hit and tp_hit:
                return 'LOSS'
            if sl_hit:
                return 'LOSS'
            if tp_hit:
                return 'WIN'
    
    return 'NO_RESULT'


def run_backtest():
    """Run the complete backtest across all data files."""
    # Initialize results storage
    results = defaultdict(lambda: defaultdict(lambda: {'wins': 0, 'losses': 0, 'no_result': 0, 'total_trades': 0}))
    long_results = defaultdict(lambda: defaultdict(lambda: {'wins': 0, 'losses': 0, 'no_result': 0, 'total_trades': 0}))
    short_results = defaultdict(lambda: defaultdict(lambda: {'wins': 0, 'losses': 0, 'no_result': 0, 'total_trades': 0}))
    
    all_trades = []
    
    print("=" * 80)
    print("NY Opening First Candle Backtesting Strategy")
    print("=" * 80)
    print(f"\nEntry Time: {ENTRY_TIME}")
    print(f"Morning Candle (for SL calculation): {MORNING_CANDLE_TIME}")
    print(f"SL Retracement Levels: {[f'{x*100}%' for x in SL_LEVELS]}")
    print(f"R:R Ratios: {RR_RATIOS}")
    print("\n" + "-" * 80)
    print("Loading data files...")
    
    # Load all data
    all_data = []
    for csv_file in CSV_FILES:
        file_path = os.path.join(DATA_DIR, csv_file)
        if os.path.exists(file_path):
            df = load_data(file_path)
            all_data.append(df)
            print(f"  Loaded {csv_file}: {len(df)} candles")
        else:
            print(f"  WARNING: {csv_file} not found")
    
    # Combine all data
    combined_df = pd.concat(all_data, ignore_index=True)
    combined_df = combined_df.sort_values('Datetime').reset_index(drop=True)
    
    print(f"\nTotal candles: {len(combined_df)}")
    print(f"Date range: {combined_df['Datetime'].min()} to {combined_df['Datetime'].max()}")
    
    # Get unique trading days
    unique_dates = combined_df['DateOnly'].unique()
    print(f"Total trading days: {len(unique_dates)}")
    
    print("\n" + "-" * 80)
    print("Running backtest...")
    
    valid_setups = 0
    long_setups = 0
    short_setups = 0
    
    for date in unique_dates:
        # Get the 15:30 entry candle
        entry_candle = get_candle_at_time(combined_df, date, ENTRY_TIME)
        if entry_candle is None:
            continue
        
        # Get the 8:30 morning candle for SL calculation
        morning_candle = get_candle_at_time(combined_df, date, MORNING_CANDLE_TIME)
        if morning_candle is None:
            continue
        
        # Get 5 previous candles before 15:30
        prev_candles = get_previous_candles(combined_df, date, ENTRY_TIME, n=5)
        if prev_candles is None:
            continue
        
        # Check entry condition
        direction = check_entry_condition(entry_candle, prev_candles)
        if direction is None:
            continue
        
        valid_setups += 1
        if direction == 'LONG':
            long_setups += 1
        else:
            short_setups += 1
        
        # Entry price is the close of the 15:30 candle
        entry_price = entry_candle['Close']
        
        # Get subsequent candles for trade evaluation
        subsequent_candles = get_remaining_day_candles(combined_df, date, ENTRY_TIME)
        
        # Test each SL level and R:R combination
        for sl_level in SL_LEVELS:
            sl_price = calculate_sl_price(direction, entry_price, morning_candle, sl_level)
            
            for rr in RR_RATIOS:
                tp_price = calculate_tp_price(direction, entry_price, sl_price, rr)
                outcome = check_trade_outcome(direction, entry_price, sl_price, tp_price, subsequent_candles)
                
                sl_key = f"{int(sl_level * 100)}%"
                
                # Record overall results
                results[sl_key][rr]['total_trades'] += 1
                if outcome == 'WIN':
                    results[sl_key][rr]['wins'] += 1
                elif outcome == 'LOSS':
                    results[sl_key][rr]['losses'] += 1
                else:
                    results[sl_key][rr]['no_result'] += 1
                
                # Record direction-specific results
                if direction == 'LONG':
                    long_results[sl_key][rr]['total_trades'] += 1
                    if outcome == 'WIN':
                        long_results[sl_key][rr]['wins'] += 1
                    elif outcome == 'LOSS':
                        long_results[sl_key][rr]['losses'] += 1
                    else:
                        long_results[sl_key][rr]['no_result'] += 1
                else:
                    short_results[sl_key][rr]['total_trades'] += 1
                    if outcome == 'WIN':
                        short_results[sl_key][rr]['wins'] += 1
                    elif outcome == 'LOSS':
                        short_results[sl_key][rr]['losses'] += 1
                    else:
                        short_results[sl_key][rr]['no_result'] += 1
                
                # Store trade details
                all_trades.append({
                    'Date': date,
                    'Direction': direction,
                    'Entry Price': entry_price,
                    'SL Level': sl_key,
                    'SL Price': sl_price,
                    'R:R': rr,
                    'TP Price': tp_price,
                    'Outcome': outcome
                })
    
    print(f"\nValid setups found: {valid_setups}")
    print(f"  - LONG setups: {long_setups}")
    print(f"  - SHORT setups: {short_setups}")
    
    return results, long_results, short_results, all_trades


def print_results(results, title):
    """Print results in a formatted table."""
    print(f"\n{'=' * 80}")
    print(f"{title}")
    print("=" * 80)
    
    # Header
    header = f"{'SL Level':<12}"
    for rr in RR_RATIOS:
        header += f"RR {rr:<6}"
    print(header)
    print("-" * 80)
    
    for sl_key in ['25%', '50%', '75%', '100%']:
        row = f"{sl_key:<12}"
        for rr in RR_RATIOS:
            data = results[sl_key][rr]
            resolved = data['wins'] + data['losses']
            if resolved > 0:
                win_rate = (data['wins'] / resolved) * 100
                row += f"{win_rate:>5.1f}% "
            else:
                row += f"{'N/A':>6} "
        print(row)
    
    # Print detailed stats
    print("\n" + "-" * 80)
    print("Detailed Statistics (Wins / Losses / No Result / Total)")
    print("-" * 80)
    
    for sl_key in ['25%', '50%', '75%', '100%']:
        print(f"\nSL {sl_key}:")
        for rr in RR_RATIOS:
            data = results[sl_key][rr]
            print(f"  RR {rr}: {data['wins']}W / {data['losses']}L / {data['no_result']}NR / {data['total_trades']}T")


def generate_report(results, long_results, short_results, all_trades):
    """Generate a comprehensive report."""
    report_lines = []
    
    report_lines.append("=" * 80)
    report_lines.append("NY OPENING FIRST CANDLE BACKTESTING STRATEGY - COMPREHENSIVE ANALYSIS")
    report_lines.append("=" * 80)
    report_lines.append("")
    report_lines.append("STRATEGY RULES:")
    report_lines.append("-" * 40)
    report_lines.append("1. Entry Condition:")
    report_lines.append("   - LONG: 15:30 candle close is HIGHER than ALL 5 previous candle closes")
    report_lines.append("   - SHORT: 15:30 candle close is LOWER than ALL 5 previous candle closes")
    report_lines.append("")
    report_lines.append("2. Stop Loss: Based on 8:30 candle range retracement")
    report_lines.append("   - SL distance = SL% × (8:30 High - 8:30 Low)")
    report_lines.append("")
    report_lines.append("3. Take Profit: Based on Risk/Reward ratio")
    report_lines.append("   - TP distance = SL distance × R:R ratio")
    report_lines.append("")
    report_lines.append("=" * 80)
    
    # Calculate and display summary statistics
    total_trades = results['25%'][1.0]['total_trades']
    long_trades = long_results['25%'][1.0]['total_trades']
    short_trades = short_results['25%'][1.0]['total_trades']
    
    report_lines.append("")
    report_lines.append(f"TRADE STATISTICS:")
    report_lines.append("-" * 40)
    report_lines.append(f"Total Valid Setups: {total_trades}")
    report_lines.append(f"LONG Setups: {long_trades} ({long_trades/total_trades*100:.1f}%)")
    report_lines.append(f"SHORT Setups: {short_trades} ({short_trades/total_trades*100:.1f}%)")
    report_lines.append("")
    
    # Win Rate Tables
    def add_table(title, res):
        report_lines.append("")
        report_lines.append("=" * 80)
        report_lines.append(title)
        report_lines.append("=" * 80)
        
        # Header
        header = f"{'SL Level':<12}"
        for rr in RR_RATIOS:
            header += f"{'RR '+str(rr):<9}"
        report_lines.append(header)
        report_lines.append("-" * 80)
        
        for sl_key in ['25%', '50%', '75%', '100%']:
            row = f"{sl_key:<12}"
            for rr in RR_RATIOS:
                data = res[sl_key][rr]
                resolved = data['wins'] + data['losses']
                if resolved > 0:
                    win_rate = (data['wins'] / resolved) * 100
                    row += f"{win_rate:>6.1f}%  "
                else:
                    row += f"{'N/A':>7}  "
            report_lines.append(row)
    
    add_table("OVERALL WIN RATES (ALL TRADES)", results)
    add_table("LONG TRADES ONLY - WIN RATES", long_results)
    add_table("SHORT TRADES ONLY - WIN RATES", short_results)
    
    # Detailed Stats
    report_lines.append("")
    report_lines.append("=" * 80)
    report_lines.append("DETAILED STATISTICS")
    report_lines.append("=" * 80)
    
    for sl_key in ['25%', '50%', '75%', '100%']:
        report_lines.append("")
        report_lines.append(f"SL {sl_key}:")
        report_lines.append("-" * 40)
        for rr in RR_RATIOS:
            data = results[sl_key][rr]
            resolved = data['wins'] + data['losses']
            win_rate = (data['wins'] / resolved * 100) if resolved > 0 else 0
            report_lines.append(f"  RR {rr}:  Wins={data['wins']:>4}, Losses={data['losses']:>4}, "
                              f"No Result={data['no_result']:>4}, Win Rate={win_rate:>5.1f}%")
    
    # Expectancy Analysis
    report_lines.append("")
    report_lines.append("=" * 80)
    report_lines.append("EXPECTANCY ANALYSIS (Positive = Profitable, Negative = Unprofitable)")
    report_lines.append("Expectancy = (Win Rate × RR) - (Loss Rate × 1)")
    report_lines.append("=" * 80)
    
    header = f"{'SL Level':<12}"
    for rr in RR_RATIOS:
        header += f"{'RR '+str(rr):<9}"
    report_lines.append(header)
    report_lines.append("-" * 80)
    
    for sl_key in ['25%', '50%', '75%', '100%']:
        row = f"{sl_key:<12}"
        for rr in RR_RATIOS:
            data = results[sl_key][rr]
            expectancy = calculate_expectancy(data['wins'], data['losses'], rr)
            if expectancy is not None:
                row += f"{expectancy:>+6.2f}R  "
            else:
                row += f"{'N/A':>7}  "
        report_lines.append(row)
    
    # Best Configurations
    report_lines.append("")
    report_lines.append("=" * 80)
    report_lines.append("TOP 10 CONFIGURATIONS BY EXPECTANCY")
    report_lines.append("=" * 80)
    
    configs = []
    for sl_key in ['25%', '50%', '75%', '100%']:
        for rr in RR_RATIOS:
            data = results[sl_key][rr]
            resolved = data['wins'] + data['losses']
            expectancy = calculate_expectancy(data['wins'], data['losses'], rr)
            if resolved > 0 and expectancy is not None:
                win_rate = data['wins'] / resolved
                configs.append({
                    'SL': sl_key,
                    'RR': rr,
                    'Win Rate': win_rate * 100,
                    'Expectancy': expectancy,
                    'Trades': resolved
                })
    
    configs.sort(key=lambda x: x['Expectancy'], reverse=True)
    
    report_lines.append(f"{'Rank':<6}{'SL':<8}{'R:R':<8}{'Win Rate':<12}{'Expectancy':<12}{'Trades':<8}")
    report_lines.append("-" * 54)
    for i, config in enumerate(configs[:10], 1):
        report_lines.append(f"{i:<6}{config['SL']:<8}{config['RR']:<8}{config['Win Rate']:>5.1f}%     "
                          f"{config['Expectancy']:>+6.2f}R     {config['Trades']:<8}")
    
    return "\n".join(report_lines)


def main():
    # Run backtest
    results, long_results, short_results, all_trades = run_backtest()
    
    # Print results to console
    print_results(results, "OVERALL WIN RATES (ALL TRADES)")
    print_results(long_results, "LONG TRADES ONLY - WIN RATES")
    print_results(short_results, "SHORT TRADES ONLY - WIN RATES")
    
    # Generate and save comprehensive report
    report = generate_report(results, long_results, short_results, all_trades)
    
    report_path = os.path.join(DATA_DIR, "ny_opening_backtest_results.txt")
    with open(report_path, 'w') as f:
        f.write(report)
    print(f"\n\nComprehensive report saved to: {report_path}")
    
    # Save trades to CSV
    trades_df = pd.DataFrame(all_trades)
    trades_path = os.path.join(DATA_DIR, "ny_opening_backtest_trades.csv")
    trades_df.to_csv(trades_path, index=False)
    print(f"All trades saved to: {trades_path}")
    
    # Create summary CSV with win rates
    summary_data = []
    for sl_key in ['25%', '50%', '75%', '100%']:
        for rr in RR_RATIOS:
            data = results[sl_key][rr]
            long_data = long_results[sl_key][rr]
            short_data = short_results[sl_key][rr]
            
            resolved = data['wins'] + data['losses']
            long_resolved = long_data['wins'] + long_data['losses']
            short_resolved = short_data['wins'] + short_data['losses']
            
            summary_data.append({
                'SL Level': sl_key,
                'R:R Ratio': rr,
                'Total Trades': data['total_trades'],
                'Wins': data['wins'],
                'Losses': data['losses'],
                'No Result': data['no_result'],
                'Win Rate (%)': (data['wins'] / resolved * 100) if resolved > 0 else None,
                'Expectancy (R)': calculate_expectancy(data['wins'], data['losses'], rr),
                'Long Trades': long_data['total_trades'],
                'Long Win Rate (%)': (long_data['wins'] / long_resolved * 100) if long_resolved > 0 else None,
                'Short Trades': short_data['total_trades'],
                'Short Win Rate (%)': (short_data['wins'] / short_resolved * 100) if short_resolved > 0 else None,
            })
    
    summary_df = pd.DataFrame(summary_data)
    summary_path = os.path.join(DATA_DIR, "ny_opening_backtest_summary.csv")
    summary_df.to_csv(summary_path, index=False)
    print(f"Summary saved to: {summary_path}")
    
    print("\n" + "=" * 80)
    print("BACKTEST COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()

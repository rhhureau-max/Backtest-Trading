#!/usr/bin/env python3
"""
Multi-Timeframe NY Opening First Candle Backtesting Strategy

This script performs comprehensive backtesting analysis across multiple timeframes:
- 1-minute candles
- 5-minute candles
- 15-minute candles

Strategy Description:
- Entry Condition: The 15:30 candle must close ABOVE or BELOW the closes of the 5 previous candles
  - LONG: 15:30 candle close is higher than ALL 5 previous closes
  - SHORT: 15:30 candle close is lower than ALL 5 previous closes

- Stop Loss: Based on the 8:30 candle retracement levels (25%, 50%, 75%, 100%)
  - For LONG: SL is below entry at X% retracement of 8:30 candle range
  - For SHORT: SL is above entry at X% retracement of 8:30 candle range

- Risk/Reward Ratios: 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0

Note on Trade Outcome Determination:
- When both SL and TP are hit within the same candle, we conservatively count it as a LOSS
- This is because we cannot determine intra-candle price movement order
- Lower timeframes provide more granular data and more accurate outcome detection
"""

import pandas as pd
import os
from collections import defaultdict

# Suppress specific pandas warnings about chained assignment and future warnings
pd.options.mode.chained_assignment = None

# Configuration
DATA_DIR = os.path.dirname(os.path.abspath(__file__))

# Timeframe configurations
TIMEFRAMES = {
    '1m': {
        'files': [f"{year} 1m.csv" for year in range(2018, 2026)],
        'entry_time': "15:30:00",
        'morning_time': "08:30:00",
        'prev_candles': 5,
        'description': '1-Minute Candles'
    },
    '5m': {
        'files': [f"{year} 5m.csv" for year in range(2018, 2026)],
        'entry_time': "15:30:00",
        'morning_time': "08:30:00",
        'prev_candles': 5,
        'description': '5-Minute Candles'
    },
    '15m': {
        'files': [f"{year} 15m.csv" for year in range(2018, 2026)],
        'entry_time': "15:30:00",
        'morning_time': "08:30:00",
        'prev_candles': 5,
        'description': '15-Minute Candles'
    }
}

# SL retracement levels
SL_LEVELS = [0.25, 0.50, 0.75, 1.00]

# Risk/Reward ratios
RR_RATIOS = [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]


def load_data(file_path):
    """
    Load CSV data with proper formatting.
    
    Args:
        file_path: Path to CSV file with semicolon-separated values.
            Expected format: Date;Time;Open;High;Low;Close;Volume
            Date format: DD/MM/YYYY, Time format: HH:MM:SS
    
    Returns:
        DataFrame with columns: Date, Time, Open, High, Low, Close, Volume,
        Datetime (combined), DateOnly (date portion only)
    """
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


def calculate_expectancy(wins, losses, rr_ratio):
    """
    Calculate trading expectancy (expected R multiple per trade).
    
    Formula: Expectancy = (Win Rate × RR) - (Loss Rate × 1)
    
    Args:
        wins: Number of winning trades
        losses: Number of losing trades
        rr_ratio: Risk/Reward ratio used for the trades
    
    Returns:
        float: Expectancy value in R multiples. Positive values indicate
        a profitable strategy, negative values indicate unprofitable.
        Returns None if no resolved trades (wins + losses = 0).
    """
    resolved = wins + losses
    if resolved == 0:
        return None
    win_rate = wins / resolved
    loss_rate = losses / resolved
    return (win_rate * rr_ratio) - (loss_rate * 1)


def run_backtest_for_timeframe(timeframe_key):
    """Run backtest for a specific timeframe - optimized version."""
    config = TIMEFRAMES[timeframe_key]
    
    # Initialize results storage
    results = defaultdict(lambda: defaultdict(lambda: {'wins': 0, 'losses': 0, 'no_result': 0, 'total_trades': 0}))
    long_results = defaultdict(lambda: defaultdict(lambda: {'wins': 0, 'losses': 0, 'no_result': 0, 'total_trades': 0}))
    short_results = defaultdict(lambda: defaultdict(lambda: {'wins': 0, 'losses': 0, 'no_result': 0, 'total_trades': 0}))
    
    all_trades = []
    
    print(f"\n{'=' * 80}")
    print(f"Processing {config['description']} ({timeframe_key})")
    print("=" * 80)
    
    # Load all data
    all_data = []
    for csv_file in config['files']:
        file_path = os.path.join(DATA_DIR, csv_file)
        if os.path.exists(file_path):
            df = load_data(file_path)
            all_data.append(df)
            print(f"  Loaded {csv_file}: {len(df)} candles")
        else:
            print(f"  WARNING: {csv_file} not found")
    
    if not all_data:
        print(f"  ERROR: No data files found for {timeframe_key}")
        return None, None, None, None
    
    # Combine all data
    combined_df = pd.concat(all_data, ignore_index=True)
    combined_df = combined_df.sort_values('Datetime').reset_index(drop=True)
    
    print(f"\nTotal candles: {len(combined_df)}")
    print(f"Date range: {combined_df['Datetime'].min()} to {combined_df['Datetime'].max()}")
    
    # Get unique trading days
    unique_dates = combined_df['DateOnly'].unique()
    print(f"Total trading days: {len(unique_dates)}")
    
    print("\nRunning backtest...")
    
    # Create index for faster lookups (chained for efficiency)
    combined_df = combined_df.set_index(['DateOnly', 'Time']).sort_index()
    
    valid_setups = 0
    long_setups = 0
    short_setups = 0
    progress_interval = len(unique_dates) // 10
    
    for i, date in enumerate(unique_dates):
        if progress_interval > 0 and i % progress_interval == 0:
            print(f"  Progress: {i}/{len(unique_dates)} days processed...")
        
        try:
            # Get the 15:30 entry candle
            entry_candle = combined_df.loc[(date, config['entry_time'])]
            if isinstance(entry_candle, pd.DataFrame):
                entry_candle = entry_candle.iloc[0]
        except KeyError:
            continue
        
        try:
            # Get the 8:30 morning candle for SL calculation
            morning_candle = combined_df.loc[(date, config['morning_time'])]
            if isinstance(morning_candle, pd.DataFrame):
                morning_candle = morning_candle.iloc[0]
        except KeyError:
            continue
        
        # Get candles for this date
        try:
            day_candles = combined_df.loc[date]
        except KeyError:
            continue
        
        # Get 5 previous candles before 15:30
        prev_candles = day_candles[day_candles.index < config['entry_time']].tail(config['prev_candles'])
        if len(prev_candles) < config['prev_candles']:
            continue
        
        # Check entry condition
        entry_close = entry_candle['Close']
        prev_closes = prev_candles['Close'].values
        
        if all(entry_close > c for c in prev_closes):
            direction = 'LONG'
        elif all(entry_close < c for c in prev_closes):
            direction = 'SHORT'
        else:
            continue
        
        valid_setups += 1
        if direction == 'LONG':
            long_setups += 1
        else:
            short_setups += 1
        
        # Entry price is the close of the 15:30 candle
        entry_price = entry_close
        
        # Get subsequent candles for trade evaluation
        subsequent_candles = day_candles[day_candles.index > config['entry_time']]
        
        # Pre-calculate morning range
        morning_range = abs(morning_candle['High'] - morning_candle['Low'])
        
        # Test each SL level and R:R combination
        for sl_level in SL_LEVELS:
            sl_distance = morning_range * sl_level
            
            if direction == 'LONG':
                sl_price = entry_price - sl_distance
            else:
                sl_price = entry_price + sl_distance
            
            for rr in RR_RATIOS:
                risk = abs(entry_price - sl_price)
                reward = risk * rr
                
                if direction == 'LONG':
                    tp_price = entry_price + reward
                else:
                    tp_price = entry_price - reward
                
                # Check outcome using vectorized operations
                outcome = 'NO_RESULT'
                for _, candle in subsequent_candles.iterrows():
                    high = candle['High']
                    low = candle['Low']
                    
                    if direction == 'LONG':
                        sl_hit = low <= sl_price
                        tp_hit = high >= tp_price
                    else:
                        sl_hit = high >= sl_price
                        tp_hit = low <= tp_price
                    
                    if sl_hit and tp_hit:
                        outcome = 'LOSS'
                        break
                    if sl_hit:
                        outcome = 'LOSS'
                        break
                    if tp_hit:
                        outcome = 'WIN'
                        break
                
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
                    'Timeframe': timeframe_key,
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


def generate_timeframe_report(timeframe_key, results, long_results, short_results, all_trades):
    """Generate a comprehensive report for a specific timeframe."""
    config = TIMEFRAMES[timeframe_key]
    report_lines = []
    
    report_lines.append("=" * 80)
    report_lines.append(f"NY OPENING BACKTESTING STRATEGY - {config['description'].upper()} ANALYSIS")
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
    report_lines.append(f"Timeframe: {config['description']}")
    report_lines.append("=" * 80)
    
    # Calculate and display summary statistics
    if results['25%'][1.0]['total_trades'] == 0:
        report_lines.append("\nNo valid trading setups found for this timeframe.")
        return "\n".join(report_lines)
    
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


def generate_comparison_report(all_results):
    """Generate a comprehensive comparison report across all timeframes."""
    report_lines = []
    
    report_lines.append("=" * 100)
    report_lines.append("MULTI-TIMEFRAME BACKTESTING COMPARISON REPORT")
    report_lines.append("=" * 100)
    report_lines.append("")
    report_lines.append("STRATEGY: NY Opening First Candle Strategy")
    report_lines.append("-" * 50)
    report_lines.append("Entry: 15:30 candle close above/below 5 previous closes")
    report_lines.append("Stop Loss: Based on 8:30 candle retracement (25%, 50%, 75%, 100%)")
    report_lines.append("R:R Ratios: 1.0 to 5.0 in 0.5 increments")
    report_lines.append("")
    
    # Summary table header
    report_lines.append("=" * 100)
    report_lines.append("SUMMARY BY TIMEFRAME")
    report_lines.append("=" * 100)
    
    # Trade counts
    report_lines.append("")
    report_lines.append("TRADE COUNTS:")
    report_lines.append("-" * 50)
    report_lines.append(f"{'Timeframe':<15}{'Total Setups':<15}{'LONG':<15}{'SHORT':<15}")
    report_lines.append("-" * 60)
    
    for tf_key, tf_data in all_results.items():
        results = tf_data['results']
        long_results = tf_data['long_results']
        short_results = tf_data['short_results']
        
        if results and results['25%'][1.0]['total_trades'] > 0:
            total = results['25%'][1.0]['total_trades']
            longs = long_results['25%'][1.0]['total_trades']
            shorts = short_results['25%'][1.0]['total_trades']
            report_lines.append(f"{tf_key:<15}{total:<15}{longs:<15}{shorts:<15}")
    
    # Win Rate Comparison for each SL level
    for sl_key in ['25%', '50%', '75%', '100%']:
        report_lines.append("")
        report_lines.append("=" * 100)
        report_lines.append(f"WIN RATE COMPARISON - SL {sl_key}")
        report_lines.append("=" * 100)
        
        # Header
        header = f"{'Timeframe':<12}"
        for rr in RR_RATIOS:
            header += f"{'RR '+str(rr):<9}"
        report_lines.append(header)
        report_lines.append("-" * 100)
        
        for tf_key, tf_data in all_results.items():
            results = tf_data['results']
            if results and results['25%'][1.0]['total_trades'] > 0:
                row = f"{tf_key:<12}"
                for rr in RR_RATIOS:
                    data = results[sl_key][rr]
                    resolved = data['wins'] + data['losses']
                    if resolved > 0:
                        win_rate = (data['wins'] / resolved) * 100
                        row += f"{win_rate:>6.1f}%  "
                    else:
                        row += f"{'N/A':>7}  "
                report_lines.append(row)
    
    # Expectancy Comparison
    for sl_key in ['25%', '50%', '75%', '100%']:
        report_lines.append("")
        report_lines.append("=" * 100)
        report_lines.append(f"EXPECTANCY COMPARISON - SL {sl_key}")
        report_lines.append("=" * 100)
        
        header = f"{'Timeframe':<12}"
        for rr in RR_RATIOS:
            header += f"{'RR '+str(rr):<9}"
        report_lines.append(header)
        report_lines.append("-" * 100)
        
        for tf_key, tf_data in all_results.items():
            results = tf_data['results']
            if results and results['25%'][1.0]['total_trades'] > 0:
                row = f"{tf_key:<12}"
                for rr in RR_RATIOS:
                    data = results[sl_key][rr]
                    expectancy = calculate_expectancy(data['wins'], data['losses'], rr)
                    if expectancy is not None:
                        row += f"{expectancy:>+6.2f}R  "
                    else:
                        row += f"{'N/A':>7}  "
                report_lines.append(row)
    
    # Best configurations across all timeframes
    report_lines.append("")
    report_lines.append("=" * 100)
    report_lines.append("TOP 15 CONFIGURATIONS ACROSS ALL TIMEFRAMES (BY EXPECTANCY)")
    report_lines.append("=" * 100)
    
    all_configs = []
    for tf_key, tf_data in all_results.items():
        results = tf_data['results']
        if results:
            for sl_key in ['25%', '50%', '75%', '100%']:
                for rr in RR_RATIOS:
                    data = results[sl_key][rr]
                    resolved = data['wins'] + data['losses']
                    expectancy = calculate_expectancy(data['wins'], data['losses'], rr)
                    if resolved > 0 and expectancy is not None:
                        win_rate = data['wins'] / resolved
                        all_configs.append({
                            'Timeframe': tf_key,
                            'SL': sl_key,
                            'RR': rr,
                            'Win Rate': win_rate * 100,
                            'Expectancy': expectancy,
                            'Trades': resolved
                        })
    
    all_configs.sort(key=lambda x: x['Expectancy'], reverse=True)
    
    report_lines.append(f"{'Rank':<6}{'TF':<8}{'SL':<8}{'R:R':<8}{'Win Rate':<12}{'Expectancy':<12}{'Trades':<8}")
    report_lines.append("-" * 70)
    for i, cfg in enumerate(all_configs[:15], 1):
        report_lines.append(f"{i:<6}{cfg['Timeframe']:<8}{cfg['SL']:<8}{cfg['RR']:<8}"
                          f"{cfg['Win Rate']:>5.1f}%     {cfg['Expectancy']:>+6.2f}R     {cfg['Trades']:<8}")
    
    # Worst configurations (for risk awareness)
    report_lines.append("")
    report_lines.append("=" * 100)
    report_lines.append("BOTTOM 10 CONFIGURATIONS (AVOID THESE)")
    report_lines.append("=" * 100)
    
    report_lines.append(f"{'Rank':<6}{'TF':<8}{'SL':<8}{'R:R':<8}{'Win Rate':<12}{'Expectancy':<12}{'Trades':<8}")
    report_lines.append("-" * 70)
    for i, cfg in enumerate(all_configs[-10:][::-1], 1):
        report_lines.append(f"{i:<6}{cfg['Timeframe']:<8}{cfg['SL']:<8}{cfg['RR']:<8}"
                          f"{cfg['Win Rate']:>5.1f}%     {cfg['Expectancy']:>+6.2f}R     {cfg['Trades']:<8}")
    
    # Recommendations
    report_lines.append("")
    report_lines.append("=" * 100)
    report_lines.append("ANALYSIS NOTES")
    report_lines.append("=" * 100)
    report_lines.append("")
    report_lines.append("1. Higher timeframes (15m) may provide more reliable signals with less noise")
    report_lines.append("2. Lower timeframes (1m) allow for tighter stops and more precise entries")
    report_lines.append("3. Positive expectancy indicates a potentially profitable configuration")
    report_lines.append("4. Consider the trade-off between win rate and R:R ratio")
    report_lines.append("5. More trades (larger sample size) provide more reliable statistics")
    report_lines.append("")
    
    return "\n".join(report_lines)


def main():
    """Run the complete multi-timeframe backtest."""
    print("=" * 80)
    print("MULTI-TIMEFRAME NY OPENING BACKTESTING STRATEGY")
    print("=" * 80)
    print(f"\nTimeframes: {list(TIMEFRAMES.keys())}")
    print(f"SL Levels: {[f'{x*100}%' for x in SL_LEVELS]}")
    print(f"R:R Ratios: {RR_RATIOS}")
    print("")
    
    all_results = {}
    all_trades = []
    
    # Run backtest for each timeframe
    for tf_key in TIMEFRAMES.keys():
        results, long_results, short_results, trades = run_backtest_for_timeframe(tf_key)
        
        all_results[tf_key] = {
            'results': results,
            'long_results': long_results,
            'short_results': short_results
        }
        
        if trades:
            all_trades.extend(trades)
        
        # Generate and save individual timeframe report
        if results:
            report = generate_timeframe_report(tf_key, results, long_results, short_results, trades)
            report_path = os.path.join(DATA_DIR, f"backtest_results_{tf_key}.txt")
            with open(report_path, 'w') as f:
                f.write(report)
            print(f"\n  Report saved to: {report_path}")
            
            # Save trades CSV for this timeframe
            if trades:
                trades_df = pd.DataFrame([t for t in trades if t['Timeframe'] == tf_key])
                trades_path = os.path.join(DATA_DIR, f"backtest_trades_{tf_key}.csv")
                trades_df.to_csv(trades_path, index=False)
                print(f"  Trades saved to: {trades_path}")
    
    # Generate comparison report
    print("\n" + "=" * 80)
    print("Generating comparison report...")
    
    comparison_report = generate_comparison_report(all_results)
    comparison_path = os.path.join(DATA_DIR, "backtest_comparison_report.txt")
    with open(comparison_path, 'w') as f:
        f.write(comparison_report)
    print(f"Comparison report saved to: {comparison_path}")
    
    # Save combined trades CSV
    if all_trades:
        all_trades_df = pd.DataFrame(all_trades)
        all_trades_path = os.path.join(DATA_DIR, "backtest_all_trades.csv")
        all_trades_df.to_csv(all_trades_path, index=False)
        print(f"All trades saved to: {all_trades_path}")
    
    # Create summary CSV with all configurations
    summary_data = []
    for tf_key, tf_data in all_results.items():
        results = tf_data['results']
        long_results = tf_data['long_results']
        short_results = tf_data['short_results']
        
        if results:
            for sl_key in ['25%', '50%', '75%', '100%']:
                for rr in RR_RATIOS:
                    data = results[sl_key][rr]
                    long_data = long_results[sl_key][rr]
                    short_data = short_results[sl_key][rr]
                    
                    resolved = data['wins'] + data['losses']
                    long_resolved = long_data['wins'] + long_data['losses']
                    short_resolved = short_data['wins'] + short_data['losses']
                    
                    summary_data.append({
                        'Timeframe': tf_key,
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
    summary_path = os.path.join(DATA_DIR, "backtest_summary_all_timeframes.csv")
    summary_df.to_csv(summary_path, index=False)
    print(f"Summary saved to: {summary_path}")
    
    print("\n" + "=" * 80)
    print("MULTI-TIMEFRAME BACKTEST COMPLETE")
    print("=" * 80)
    print("\nGenerated files:")
    print("  - backtest_results_1m.txt    (1-minute candle analysis)")
    print("  - backtest_results_5m.txt    (5-minute candle analysis)")
    print("  - backtest_results_15m.txt   (15-minute candle analysis)")
    print("  - backtest_trades_1m.csv     (1-minute trades)")
    print("  - backtest_trades_5m.csv     (5-minute trades)")
    print("  - backtest_trades_15m.csv    (15-minute trades)")
    print("  - backtest_comparison_report.txt (cross-timeframe comparison)")
    print("  - backtest_all_trades.csv    (all trades combined)")
    print("  - backtest_summary_all_timeframes.csv (summary statistics)")


if __name__ == "__main__":
    main()

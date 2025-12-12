#!/usr/bin/env python3
"""
8:30 Strategy Backtest - Main Script

This script performs a comprehensive backtest of the 8:30 candle strategy
on historical data from 2018 to 2025.

Usage:
    python backtest_830_strategy.py [--output-dir OUTPUT_DIR] [--years YEARS]
"""

import os
import sys
import argparse
from datetime import datetime
import pandas as pd
from typing import List, Dict

from data_loader import (
    load_timeframe_data, 
    get_830_candles, 
    get_previous_candles,
    prepare_simulation_data
)
from strategy import (
    Direction, 
    SLType, 
    get_entry_direction,
    calculate_sl, 
    calculate_tp, 
    simulate_trade,
    simulate_trade_fast,
    get_all_sl_types,
    get_all_rr_values,
    MAX_SIMULATION_CANDLES
)
from metrics import calculate_all_metrics, format_metrics_table
from report_generator import (
    generate_results_csv,
    generate_trades_csv,
    generate_markdown_report,
    generate_charts
)


def run_backtest_for_timeframe(
    data_tf: pd.DataFrame,
    data_1m: pd.DataFrame,
    timeframe: str,
    sl_types: List[SLType],
    rr_values: List[float],
    verbose: bool = True
) -> tuple:
    """
    Run backtest for a specific timeframe.
    
    Args:
        data_tf: DataFrame for the timeframe being analyzed
        data_1m: 1-minute data for simulation
        timeframe: Timeframe string ('1m', '5m', '15m')
        sl_types: List of SL types to test
        rr_values: List of RR values to test
        verbose: Print progress
        
    Returns:
        Tuple of (results list, trades DataFrame)
    """
    results = []
    all_trades = []
    
    # Get all 8:30 candles
    candles_830 = get_830_candles(data_tf)
    
    if verbose:
        print(f"\n{'='*60}")
        print(f"Processing timeframe: {timeframe}")
        print(f"Found {len(candles_830)} candles at 8:30")
        print(f"{'='*60}")
    
    # Find valid entry signals
    valid_entries = []
    
    for entry_time, candle in candles_830.iterrows():
        # Get previous 5 candles
        prev_candles = get_previous_candles(data_tf, entry_time, n_candles=5)
        
        if len(prev_candles) < 5:
            continue
        
        # Check entry direction
        direction = get_entry_direction(candle, prev_candles)
        
        if direction is not None:
            valid_entries.append({
                'time': entry_time,
                'candle': candle,
                'direction': direction
            })
    
    if verbose:
        print(f"Valid entry signals: {len(valid_entries)}")
        long_count = len([e for e in valid_entries if e['direction'] == Direction.LONG])
        short_count = len([e for e in valid_entries if e['direction'] == Direction.SHORT])
        print(f"  - LONG signals: {long_count}")
        print(f"  - SHORT signals: {short_count}")
    
    # Pre-compute 1m data slices for each entry (this is the key optimization)
    if verbose:
        print("Pre-computing 1-minute data slices...")
    
    entry_data_slices = {}
    for entry in valid_entries:
        entry_time = entry['time']
        # Get next MAX_SIMULATION_CANDLES 1-min candles after entry
        future_mask = data_1m.index > entry_time
        future_start_idx = future_mask.argmax() if future_mask.any() else len(data_1m)
        future_end_idx = min(future_start_idx + MAX_SIMULATION_CANDLES, len(data_1m))
        entry_data_slices[entry_time] = data_1m.iloc[future_start_idx:future_end_idx]
    
    if verbose:
        print(f"Running backtest for {len(sl_types)} SL types x {len(rr_values)} RR values...")
    
    # Run backtests for each SL/RR combination
    for sl_type in sl_types:
        for rr in rr_values:
            trades_for_combo = []
            
            for entry in valid_entries:
                entry_time = entry['time']
                candle = entry['candle']
                direction = entry['direction']
                
                entry_price = candle['close']
                sl = calculate_sl(candle, direction, sl_type)
                tp = calculate_tp(entry_price, sl, rr, direction)
                
                # Use pre-computed data slice
                future_data = entry_data_slices[entry_time]
                
                # Simulate trade using pre-sliced 1-minute data
                result = simulate_trade_fast(
                    future_data, entry_price, sl, tp, direction
                )
                
                trade_record = {
                    'date': entry_time.strftime('%Y-%m-%d'),
                    'time': entry_time.strftime('%H:%M:%S'),
                    'timeframe': timeframe,
                    'sl_type': sl_type.value,
                    'rr': rr,
                    'direction': direction.value,
                    'entry': entry_price,
                    'sl': sl,
                    'tp': tp,
                    'exit_price': result['exit_price'],
                    'exit_time': result['exit_time'],
                    'result': result['result'],
                    'pnl_r': result['pnl_r']
                }
                
                trades_for_combo.append(trade_record)
                all_trades.append(trade_record)
            
            # Calculate metrics for this combination
            df_trades = pd.DataFrame(trades_for_combo)
            metrics = calculate_all_metrics(df_trades)
            
            result_record = {
                'timeframe': timeframe,
                'sl_type': sl_type.value,
                'rr': rr,
                **metrics
            }
            
            results.append(result_record)
            
            if verbose and (sl_type == sl_types[0] and rr == rr_values[0]):
                print(f"\nSample metrics for {sl_type.value}, RR {rr}:")
                print(f"  Trades: {metrics['total_trades']}, "
                      f"Win Rate: {metrics['win_rate']:.1f}%")
    
    return results, pd.DataFrame(all_trades)


def main():
    parser = argparse.ArgumentParser(
        description='8:30 Strategy Backtest'
    )
    parser.add_argument(
        '--output-dir', 
        default='backtest_output',
        help='Output directory for results'
    )
    parser.add_argument(
        '--years',
        default='2018-2025',
        help='Year range (e.g., 2018-2025 or 2020-2023)'
    )
    parser.add_argument(
        '--timeframes',
        default='1m,5m,15m',
        help='Comma-separated list of timeframes to analyze'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        default=True,
        help='Print detailed progress'
    )
    
    args = parser.parse_args()
    
    # Parse years
    year_parts = args.years.split('-')
    start_year = int(year_parts[0])
    end_year = int(year_parts[1]) if len(year_parts) > 1 else start_year
    years = list(range(start_year, end_year + 1))
    
    # Parse timeframes
    timeframes = [tf.strip() for tf in args.timeframes.split(',')]
    
    # Get data directory (same as script location)
    data_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Create output directory
    os.makedirs(args.output_dir, exist_ok=True)
    
    print("="*60)
    print("8:30 STRATEGY BACKTEST")
    print("="*60)
    print(f"Data directory: {data_dir}")
    print(f"Output directory: {args.output_dir}")
    print(f"Years: {years}")
    print(f"Timeframes: {timeframes}")
    print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    # Load 1-minute data (needed for trade simulation)
    print("\nLoading 1-minute data for trade simulation...")
    try:
        data_1m = load_timeframe_data(data_dir, '1m', years)
        print(f"Loaded {len(data_1m):,} rows of 1-minute data")
        print(f"Date range: {data_1m.index.min()} to {data_1m.index.max()}")
    except Exception as e:
        print(f"Error loading 1-minute data: {e}")
        print("1-minute data is required for trade simulation")
        sys.exit(1)
    
    # Get SL types and RR values
    sl_types = get_all_sl_types()
    rr_values = get_all_rr_values()
    
    print(f"\nSL Types: {[sl.value for sl in sl_types]}")
    print(f"RR Values: {rr_values}")
    print(f"Total combinations per timeframe: {len(sl_types) * len(rr_values)}")
    
    all_results = []
    all_trades = pd.DataFrame()
    
    # Run backtest for each timeframe
    for timeframe in timeframes:
        print(f"\nLoading {timeframe} data...")
        try:
            if timeframe == '1m':
                data_tf = data_1m
            else:
                data_tf = load_timeframe_data(data_dir, timeframe, years)
            
            print(f"Loaded {len(data_tf):,} rows")
            
            results, trades = run_backtest_for_timeframe(
                data_tf, data_1m, timeframe, sl_types, rr_values, args.verbose
            )
            
            all_results.extend(results)
            all_trades = pd.concat([all_trades, trades], ignore_index=True)
            
        except Exception as e:
            print(f"Error processing {timeframe}: {e}")
            import traceback
            traceback.print_exc()
            continue
    
    print("\n" + "="*60)
    print("GENERATING REPORTS")
    print("="*60)
    
    # Generate outputs
    results_path = os.path.join(args.output_dir, 'backtest_results.csv')
    generate_results_csv(all_results, results_path)
    
    trades_path = os.path.join(args.output_dir, 'trades_log.csv')
    generate_trades_csv(all_trades, trades_path)
    
    report_path = os.path.join(args.output_dir, 'backtest_report.md')
    generate_markdown_report(all_results, all_trades, report_path)
    
    # Generate charts
    generate_charts(all_results, all_trades, args.output_dir)
    
    # Print summary
    print("\n" + "="*60)
    print("BACKTEST COMPLETE")
    print("="*60)
    
    if all_results:
        df_results = pd.DataFrame(all_results)
        
        print(f"\nTotal combinations analyzed: {len(df_results)}")
        print(f"Total trades simulated: {len(all_trades)}")
        
        # Best combinations
        print("\nTop 5 combinations by win rate:")
        top_wr = df_results.nlargest(5, 'win_rate')[
            ['timeframe', 'sl_type', 'rr', 'win_rate', 'expectancy', 'total_trades']
        ]
        print(top_wr.to_string(index=False))
        
        print("\nTop 5 combinations by expectancy:")
        top_exp = df_results.nlargest(5, 'expectancy')[
            ['timeframe', 'sl_type', 'rr', 'win_rate', 'expectancy', 'total_trades']
        ]
        print(top_exp.to_string(index=False))
    
    print(f"\nEnd time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"\nOutputs saved to: {args.output_dir}/")
    print("  - backtest_results.csv")
    print("  - trades_log.csv")
    print("  - backtest_report.md")
    print("  - Charts (if matplotlib available)")


if __name__ == "__main__":
    main()

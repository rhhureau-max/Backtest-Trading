#!/usr/bin/env python3
"""
London Killzone FVG (Fair Value Gap) Scenario Analysis
========================================================

This script analyzes Fair Value Gaps (FVGs) that form during the London Killzone
(01:00-04:00 NY Time) in NQ futures data. It classifies FVGs into three scenarios:
- Scenario A: Liquidity Sweep Reversal
- Scenario B: Market Structure Shift (MSS)
- Scenario C: Simple Continuation

For each mitigated FVG, it simulates trades with 1:1 and 2:1 risk-reward ratios.
"""

import pandas as pd
import numpy as np
from datetime import datetime, time
import os
from typing import List, Dict, Tuple
import warnings

warnings.filterwarnings('ignore')

# ============================================================================
# CONSTANTS
# ============================================================================

# London Killzone hours (NY Time)
LONDON_KILLZONE_START = time(1, 0)  # 01:00
LONDON_KILLZONE_END = time(4, 0)    # 04:00

# Analysis parameters
LOOKBACK_CANDLES = 12  # 60 minutes (12 * 5 minutes)
MITIGATION_WINDOW = 12  # 60 minutes for mitigation check

# Risk-Reward ratios
RR_RATIO_1 = 1.0  # TP1: 1:1
RR_RATIO_2 = 2.0  # TP2: 2:1

# Data years
DATA_YEARS = range(2018, 2026)  # 2018 to 2025

# ============================================================================
# DATA LOADING AND PREPROCESSING
# ============================================================================

def load_all_data(base_path: str) -> pd.DataFrame:
    """
    Load all 5-minute NQ data from CSV files (2018-2025).
    
    Args:
        base_path: Base directory containing the CSV files
        
    Returns:
        Combined DataFrame with all data
    """
    print("=" * 80)
    print("LOADING DATA")
    print("=" * 80)
    
    all_data = []
    
    for year in DATA_YEARS:
        filename = f"{year} 5m.csv"
        filepath = os.path.join(base_path, filename)
        
        if os.path.exists(filepath):
            print(f"Loading {filename}...")
            
            # Read CSV with semicolon separator
            df = pd.read_csv(filepath, sep=';')
            
            # Combine date and time columns
            df['DateTime'] = pd.to_datetime(
                df['Column1'] + ' ' + df['Column2'],
                format='%d/%m/%Y %H:%M:%S'
            )
            
            # Rename columns for clarity
            df = df.rename(columns={
                'Column3': 'Open',
                'Column4': 'High',
                'Column5': 'Low',
                'Column6': 'Close',
                'Column7': 'Volume'
            })
            
            # Select relevant columns
            df = df[['DateTime', 'Open', 'High', 'Low', 'Close', 'Volume']]
            
            all_data.append(df)
            print(f"  Loaded {len(df)} rows from {year}")
        else:
            print(f"  WARNING: {filename} not found, skipping...")
    
    if not all_data:
        raise FileNotFoundError("No data files found!")
    
    # Combine all data
    combined_df = pd.concat(all_data, ignore_index=True)
    combined_df = combined_df.sort_values('DateTime').reset_index(drop=True)
    
    print(f"\nTotal rows loaded: {len(combined_df)}")
    print(f"Date range: {combined_df['DateTime'].min()} to {combined_df['DateTime'].max()}")
    
    return combined_df


def filter_london_killzone(df: pd.DataFrame) -> pd.DataFrame:
    """
    Filter data for London Killzone hours (01:00-04:00 NY Time).
    
    Assumes data is already in NY timezone or adjust if needed.
    
    Args:
        df: DataFrame with DateTime column
        
    Returns:
        Filtered DataFrame
    """
    print("\n" + "=" * 80)
    print("FILTERING LONDON KILLZONE HOURS")
    print("=" * 80)
    
    # Extract time component
    df['Time'] = df['DateTime'].dt.time
    
    # Filter for London Killzone hours
    mask = (df['Time'] >= LONDON_KILLZONE_START) & (df['Time'] < LONDON_KILLZONE_END)
    filtered_df = df[mask].copy()
    
    print(f"Original rows: {len(df)}")
    print(f"Rows in London Killzone (01:00-04:00 NY): {len(filtered_df)}")
    print(f"Percentage: {len(filtered_df) / len(df) * 100:.2f}%")
    
    return filtered_df

# ============================================================================
# FVG DETECTION
# ============================================================================

def detect_fvgs(df: pd.DataFrame) -> pd.DataFrame:
    """
    Detect Fair Value Gaps (FVGs) in the data.
    
    Bullish FVG: High(n-1) < Low(n+1), zone = [High(n-1), Low(n+1)]
    Bearish FVG: Low(n-1) > High(n+1), zone = [High(n+1), Low(n-1)]
    
    Args:
        df: DataFrame with OHLC data
        
    Returns:
        DataFrame with FVG information
    """
    print("\n" + "=" * 80)
    print("DETECTING FAIR VALUE GAPS")
    print("=" * 80)
    
    fvgs = []
    
    # We need at least 3 candles to detect an FVG
    for i in range(1, len(df) - 1):
        candle_prev = df.iloc[i - 1]
        candle_mid = df.iloc[i]
        candle_next = df.iloc[i + 1]
        
        # Bullish FVG: gap up
        if candle_prev['High'] < candle_next['Low']:
            fvgs.append({
                'index': i,
                'datetime': candle_mid['DateTime'],
                'type': 'bullish',
                'zone_low': candle_prev['High'],
                'zone_high': candle_next['Low'],
                'gap_size': candle_next['Low'] - candle_prev['High'],
                'candle_n_minus_1_idx': i - 1,
                'candle_n_idx': i,
                'candle_n_plus_1_idx': i + 1,
                'candle_n_minus_1_low': candle_prev['Low'],
                'candle_n_minus_1_high': candle_prev['High']
            })
        
        # Bearish FVG: gap down
        elif candle_prev['Low'] > candle_next['High']:
            fvgs.append({
                'index': i,
                'datetime': candle_mid['DateTime'],
                'type': 'bearish',
                'zone_low': candle_next['High'],
                'zone_high': candle_prev['Low'],
                'gap_size': candle_prev['Low'] - candle_next['High'],
                'candle_n_minus_1_idx': i - 1,
                'candle_n_idx': i,
                'candle_n_plus_1_idx': i + 1,
                'candle_n_minus_1_low': candle_prev['Low'],
                'candle_n_minus_1_high': candle_prev['High']
            })
    
    fvg_df = pd.DataFrame(fvgs)
    
    if len(fvg_df) > 0:
        print(f"Total FVGs detected: {len(fvg_df)}")
        print(f"  Bullish FVGs: {len(fvg_df[fvg_df['type'] == 'bullish'])}")
        print(f"  Bearish FVGs: {len(fvg_df[fvg_df['type'] == 'bearish'])}")
        print(f"  Average gap size: {fvg_df['gap_size'].mean():.2f} points")
    else:
        print("No FVGs detected!")
    
    return fvg_df

# ============================================================================
# FVG MITIGATION
# ============================================================================

def check_mitigation(fvg: Dict, df: pd.DataFrame) -> Tuple[bool, int, float]:
    """
    Check if an FVG is mitigated (touched) within the next 60 minutes.
    
    Args:
        fvg: FVG dictionary with zone information
        df: Full DataFrame
        
    Returns:
        Tuple of (is_mitigated, mitigation_candle_index, mitigation_price)
    """
    start_idx = fvg['candle_n_plus_1_idx'] + 1  # Start after FVG formation
    end_idx = min(start_idx + MITIGATION_WINDOW, len(df))
    
    zone_low = fvg['zone_low']
    zone_high = fvg['zone_high']
    
    for i in range(start_idx, end_idx):
        candle = df.iloc[i]
        
        # Check if candle touches the FVG zone
        if candle['Low'] <= zone_high and candle['High'] >= zone_low:
            # Mitigated! Determine entry price
            if fvg['type'] == 'bullish':
                # For bullish FVG, entry at the point where price enters zone from below
                entry_price = max(zone_low, candle['Low'])
            else:  # bearish
                # For bearish FVG, entry at the point where price enters zone from above
                entry_price = min(zone_high, candle['High'])
            
            return True, i, entry_price
    
    return False, -1, 0.0

# ============================================================================
# SCENARIO CLASSIFICATION
# ============================================================================

def classify_scenario(fvg: Dict, df: pd.DataFrame) -> str:
    """
    Classify FVG into Scenario A, B, or C.
    
    Scenario A: Liquidity Sweep Reversal
    Scenario B: Market Structure Shift (MSS)
    Scenario C: Simple Continuation
    
    Args:
        fvg: FVG dictionary
        df: Full DataFrame
        
    Returns:
        Scenario name ('A', 'B', or 'C')
    """
    fvg_idx = fvg['candle_n_idx']
    lookback_start = max(0, fvg_idx - LOOKBACK_CANDLES)
    
    # Get previous candles
    prev_candles = df.iloc[lookback_start:fvg_idx]
    
    if len(prev_candles) == 0:
        return 'C'  # Not enough data
    
    # Find significant high and low in lookback period
    significant_high = prev_candles['High'].max()
    significant_low = prev_candles['Low'].min()
    
    # Check for Scenario A: Liquidity Sweep
    # Look for wicks beyond significant levels without closing beyond them
    has_liquidity_sweep = False
    
    for i in range(len(prev_candles)):
        candle = prev_candles.iloc[i]
        
        if fvg['type'] == 'bullish':
            # For bullish FVG, check for sweep below significant low
            if candle['Low'] <= significant_low and candle['Close'] > significant_low:
                has_liquidity_sweep = True
                break
        else:  # bearish
            # For bearish FVG, check for sweep above significant high
            if candle['High'] >= significant_high and candle['Close'] < significant_high:
                has_liquidity_sweep = True
                break
    
    if has_liquidity_sweep:
        return 'A'
    
    # Check for Scenario B: Market Structure Shift
    # FVG breaks structure without liquidity sweep
    fvg_candles = df.iloc[fvg['candle_n_minus_1_idx']:fvg['candle_n_plus_1_idx'] + 1]
    
    if fvg['type'] == 'bullish':
        # Check if FVG breaks above previous high
        fvg_high = fvg_candles['High'].max()
        if fvg_high > significant_high:
            return 'B'
    else:  # bearish
        # Check if FVG breaks below previous low
        fvg_low = fvg_candles['Low'].min()
        if fvg_low < significant_low:
            return 'B'
    
    # Default: Scenario C - Simple Continuation
    return 'C'

# ============================================================================
# TRADE SIMULATION
# ============================================================================

def simulate_trade(fvg: Dict, entry_idx: int, entry_price: float, df: pd.DataFrame) -> Dict:
    """
    Simulate a trade based on FVG mitigation.
    
    Args:
        fvg: FVG dictionary
        entry_idx: Index where mitigation occurred
        entry_price: Entry price
        df: Full DataFrame
        
    Returns:
        Dictionary with trade results
    """
    is_long = (fvg['type'] == 'bullish')
    
    # Set stop loss
    if is_long:
        stop_loss = fvg['candle_n_minus_1_low'] - 0.25  # Just below
    else:
        stop_loss = fvg['candle_n_minus_1_high'] + 0.25  # Just above
    
    # Calculate risk
    risk = abs(entry_price - stop_loss)
    
    # Set take profit levels
    if is_long:
        tp1 = entry_price + (risk * RR_RATIO_1)
        tp2 = entry_price + (risk * RR_RATIO_2)
    else:
        tp1 = entry_price - (risk * RR_RATIO_1)
        tp2 = entry_price - (risk * RR_RATIO_2)
    
    # Simulate trade outcome
    tp1_hit = False
    tp2_hit = False
    sl_hit = False
    exit_price = entry_price
    exit_idx = entry_idx
    
    # Check subsequent candles
    for i in range(entry_idx + 1, len(df)):
        candle = df.iloc[i]
        
        if is_long:
            # Check stop loss first
            if candle['Low'] <= stop_loss:
                sl_hit = True
                exit_price = stop_loss
                exit_idx = i
                break
            
            # Check TP2 (larger target)
            if candle['High'] >= tp2:
                tp2_hit = True
                tp1_hit = True  # TP1 also hit
                exit_price = tp2
                exit_idx = i
                break
            
            # Check TP1
            if candle['High'] >= tp1:
                tp1_hit = True
                # Continue to see if TP2 is hit
        else:  # short
            # Check stop loss first
            if candle['High'] >= stop_loss:
                sl_hit = True
                exit_price = stop_loss
                exit_idx = i
                break
            
            # Check TP2 (larger target)
            if candle['Low'] <= tp2:
                tp2_hit = True
                tp1_hit = True  # TP1 also hit
                exit_price = tp2
                exit_idx = i
                break
            
            # Check TP1
            if candle['Low'] <= tp1:
                tp1_hit = True
                # Continue to see if TP2 is hit
        
        # Stop after reasonable time (e.g., 200 candles = ~16 hours)
        if i - entry_idx > 200:
            break
    
    # Calculate P&L
    if is_long:
        pnl = exit_price - entry_price
    else:
        pnl = entry_price - exit_price
    
    return {
        'entry_price': entry_price,
        'entry_idx': entry_idx,
        'stop_loss': stop_loss,
        'tp1': tp1,
        'tp2': tp2,
        'risk': risk,
        'tp1_hit': tp1_hit,
        'tp2_hit': tp2_hit,
        'sl_hit': sl_hit,
        'exit_price': exit_price,
        'exit_idx': exit_idx,
        'pnl': pnl,
        'pnl_points': pnl,
        'outcome': 'TP2' if tp2_hit else ('TP1' if tp1_hit else 'SL')
    }

# ============================================================================
# ANALYSIS AND REPORTING
# ============================================================================

def analyze_fvgs(fvg_df: pd.DataFrame, df: pd.DataFrame) -> pd.DataFrame:
    """
    Analyze all FVGs: check mitigation, classify scenarios, simulate trades.
    
    Args:
        fvg_df: DataFrame with detected FVGs
        df: Full DataFrame with price data
        
    Returns:
        Enhanced FVG DataFrame with analysis results
    """
    print("\n" + "=" * 80)
    print("ANALYZING FVGs: MITIGATION, SCENARIOS, AND TRADES")
    print("=" * 80)
    
    results = []
    
    total_fvgs = len(fvg_df)
    
    for idx, fvg in fvg_df.iterrows():
        if idx % 100 == 0:
            print(f"Processing FVG {idx + 1}/{total_fvgs}...")
        
        fvg_dict = fvg.to_dict()
        
        # Check mitigation
        is_mitigated, mitigation_idx, entry_price = check_mitigation(fvg_dict, df)
        
        # Classify scenario
        scenario = classify_scenario(fvg_dict, df)
        
        result = {
            **fvg_dict,
            'is_mitigated': is_mitigated,
            'mitigation_idx': mitigation_idx,
            'entry_price': entry_price,
            'scenario': scenario
        }
        
        # Simulate trade if mitigated
        if is_mitigated:
            trade_result = simulate_trade(fvg_dict, mitigation_idx, entry_price, df)
            result.update(trade_result)
        else:
            # No trade taken
            result.update({
                'tp1_hit': False,
                'tp2_hit': False,
                'sl_hit': False,
                'pnl_points': 0.0,
                'outcome': 'No Trade'
            })
        
        results.append(result)
    
    results_df = pd.DataFrame(results)
    
    print(f"\nAnalysis complete!")
    print(f"Total FVGs analyzed: {len(results_df)}")
    print(f"Mitigated FVGs: {results_df['is_mitigated'].sum()}")
    print(f"Mitigation rate: {results_df['is_mitigated'].sum() / len(results_df) * 100:.2f}%")
    
    return results_df


def generate_scenario_statistics(results_df: pd.DataFrame, scenario: str) -> Dict:
    """
    Generate comprehensive statistics for a specific scenario.
    
    Args:
        results_df: DataFrame with all analysis results
        scenario: Scenario identifier ('A', 'B', or 'C')
        
    Returns:
        Dictionary with detailed statistics
    """
    scenario_data = results_df[results_df['scenario'] == scenario]
    
    if len(scenario_data) == 0:
        return {
            'scenario': scenario,
            'total_occurrences': 0,
            'num_mitigated': 0,
            'mitigation_rate': 0.0,
            'trades_taken': 0,
            'wins_rr1': 0,
            'win_rate_rr1': 0.0,
            'loss_rate_rr1': 0.0,
            'wins_rr2': 0,
            'win_rate_rr2': 0.0,
            'loss_rate_rr2': 0.0,
            'avg_profit_points': 0.0,
            'avg_loss_points': 0.0,
            'net_expectancy': 0.0,
            'profit_factor': 0.0,
            'avg_rr_achieved': 0.0,
            'total_profit': 0.0,
            'total_loss': 0.0,
            'max_consecutive_wins': 0,
            'max_consecutive_losses': 0,
            'avg_gap_size': 0.0
        }
    
    mitigated_data = scenario_data[scenario_data['is_mitigated']]
    trades_taken = len(mitigated_data)
    
    # Average gap size
    avg_gap_size = scenario_data['gap_size'].mean()
    
    if trades_taken > 0:
        # TP1 statistics
        wins_rr1 = mitigated_data['tp1_hit'].sum()
        losses_rr1 = trades_taken - wins_rr1
        win_rate_rr1 = (wins_rr1 / trades_taken) * 100
        loss_rate_rr1 = (losses_rr1 / trades_taken) * 100
        
        # TP2 statistics
        wins_rr2 = mitigated_data['tp2_hit'].sum()
        losses_rr2 = trades_taken - wins_rr2
        win_rate_rr2 = (wins_rr2 / trades_taken) * 100
        loss_rate_rr2 = (losses_rr2 / trades_taken) * 100
        
        # P&L statistics
        winning_trades = mitigated_data[mitigated_data['pnl_points'] > 0]
        losing_trades = mitigated_data[mitigated_data['pnl_points'] <= 0]
        
        avg_profit_points = winning_trades['pnl_points'].mean() if len(winning_trades) > 0 else 0.0
        avg_loss_points = losing_trades['pnl_points'].mean() if len(losing_trades) > 0 else 0.0
        
        total_profit = winning_trades['pnl_points'].sum() if len(winning_trades) > 0 else 0.0
        total_loss = abs(losing_trades['pnl_points'].sum()) if len(losing_trades) > 0 else 0.0
        
        # Profit factor
        profit_factor = total_profit / total_loss if total_loss > 0 else 0.0
        
        # Average RR achieved
        avg_rr_achieved = mitigated_data['pnl_points'].mean() / abs(avg_loss_points) if avg_loss_points != 0 else 0.0
        
        # Net expectancy
        net_expectancy = mitigated_data['pnl_points'].mean()
        
        # Max consecutive wins/losses
        max_consecutive_wins = 0
        max_consecutive_losses = 0
        current_wins = 0
        current_losses = 0
        
        for pnl in mitigated_data['pnl_points']:
            if pnl > 0:
                current_wins += 1
                current_losses = 0
                max_consecutive_wins = max(max_consecutive_wins, current_wins)
            else:
                current_losses += 1
                current_wins = 0
                max_consecutive_losses = max(max_consecutive_losses, current_losses)
    else:
        wins_rr1 = 0
        losses_rr1 = 0
        win_rate_rr1 = 0.0
        loss_rate_rr1 = 0.0
        wins_rr2 = 0
        losses_rr2 = 0
        win_rate_rr2 = 0.0
        loss_rate_rr2 = 0.0
        avg_profit_points = 0.0
        avg_loss_points = 0.0
        net_expectancy = 0.0
        profit_factor = 0.0
        avg_rr_achieved = 0.0
        total_profit = 0.0
        total_loss = 0.0
        max_consecutive_wins = 0
        max_consecutive_losses = 0
    
    return {
        'scenario': scenario,
        'total_occurrences': len(scenario_data),
        'num_mitigated': len(mitigated_data),
        'mitigation_rate': (len(mitigated_data) / len(scenario_data) * 100) if len(scenario_data) > 0 else 0.0,
        'trades_taken': trades_taken,
        'wins_rr1': int(wins_rr1),
        'losses_rr1': int(losses_rr1),
        'win_rate_rr1': win_rate_rr1,
        'loss_rate_rr1': loss_rate_rr1,
        'wins_rr2': int(wins_rr2),
        'losses_rr2': int(losses_rr2),
        'win_rate_rr2': win_rate_rr2,
        'loss_rate_rr2': loss_rate_rr2,
        'avg_profit_points': avg_profit_points,
        'avg_loss_points': avg_loss_points,
        'net_expectancy': net_expectancy,
        'profit_factor': profit_factor,
        'avg_rr_achieved': avg_rr_achieved,
        'total_profit': total_profit,
        'total_loss': total_loss,
        'max_consecutive_wins': max_consecutive_wins,
        'max_consecutive_losses': max_consecutive_losses,
        'avg_gap_size': avg_gap_size
    }


def print_results(results_df: pd.DataFrame):
    """
    Print comprehensive results and statistics.
    
    Args:
        results_df: DataFrame with all analysis results
    """
    print("\n" + "=" * 80)
    print("COMPREHENSIVE SCENARIO ANALYSIS RESULTS")
    print("=" * 80)
    
    # Generate statistics for each scenario
    scenario_stats = []
    for scenario in ['A', 'B', 'C']:
        stats = generate_scenario_statistics(results_df, scenario)
        scenario_stats.append(stats)
    
    # Create comparison table
    print("\n" + "-" * 80)
    print("SCENARIO COMPARISON TABLE")
    print("-" * 80)
    
    # Header
    print(f"{'Metric':<30} {'Scenario A':<20} {'Scenario B':<20} {'Scenario C':<20}")
    print("-" * 80)
    
    # Scenario names
    scenario_names = {
        'A': 'Liquidity Sweep',
        'B': 'Market Structure Shift',
        'C': 'Simple Continuation'
    }
    
    print(f"{'Scenario Name':<30} {scenario_names['A']:<20} {scenario_names['B']:<20} {scenario_names['C']:<20}")
    
    # Basic Metrics
    metrics_basic = [
        ('Total Occurrences', 'total_occurrences', '{}'),
        ('Number Mitigated', 'num_mitigated', '{}'),
        ('Mitigation Rate (%)', 'mitigation_rate', '{:.2f}%'),
        ('Trades Taken', 'trades_taken', '{}'),
        ('Average Gap Size (pts)', 'avg_gap_size', '{:.2f}'),
    ]
    
    for metric_name, metric_key, format_str in metrics_basic:
        values = [format_str.format(stats[metric_key]) for stats in scenario_stats]
        print(f"{metric_name:<30} {values[0]:<20} {values[1]:<20} {values[2]:<20}")
    
    print("-" * 80)
    print("WIN/LOSS RATIOS AT RR 1:1")
    print("-" * 80)
    
    metrics_rr1 = [
        ('Wins at RR 1:1', 'wins_rr1', '{}'),
        ('Losses at RR 1:1', 'losses_rr1', '{}'),
        ('Win Rate RR 1:1 (%)', 'win_rate_rr1', '{:.2f}%'),
        ('Loss Rate RR 1:1 (%)', 'loss_rate_rr1', '{:.2f}%'),
    ]
    
    for metric_name, metric_key, format_str in metrics_rr1:
        values = [format_str.format(stats[metric_key]) for stats in scenario_stats]
        print(f"{metric_name:<30} {values[0]:<20} {values[1]:<20} {values[2]:<20}")
    
    print("-" * 80)
    print("WIN/LOSS RATIOS AT RR 2:1")
    print("-" * 80)
    
    metrics_rr2 = [
        ('Wins at RR 2:1', 'wins_rr2', '{}'),
        ('Losses at RR 2:1', 'losses_rr2', '{}'),
        ('Win Rate RR 2:1 (%)', 'win_rate_rr2', '{:.2f}%'),
        ('Loss Rate RR 2:1 (%)', 'loss_rate_rr2', '{:.2f}%'),
    ]
    
    for metric_name, metric_key, format_str in metrics_rr2:
        values = [format_str.format(stats[metric_key]) for stats in scenario_stats]
        print(f"{metric_name:<30} {values[0]:<20} {values[1]:<20} {values[2]:<20}")
    
    print("-" * 80)
    print("PROFITABILITY RATIOS")
    print("-" * 80)
    
    metrics_profit = [
        ('Total Profit (points)', 'total_profit', '{:.2f}'),
        ('Total Loss (points)', 'total_loss', '{:.2f}'),
        ('Avg Profit (points)', 'avg_profit_points', '{:.2f}'),
        ('Avg Loss (points)', 'avg_loss_points', '{:.2f}'),
        ('Net Expectancy (points)', 'net_expectancy', '{:.2f}'),
        ('Profit Factor', 'profit_factor', '{:.2f}'),
        ('Avg RR Achieved', 'avg_rr_achieved', '{:.2f}'),
    ]
    
    for metric_name, metric_key, format_str in metrics_profit:
        values = [format_str.format(stats[metric_key]) for stats in scenario_stats]
        print(f"{metric_name:<30} {values[0]:<20} {values[1]:<20} {values[2]:<20}")
    
    print("-" * 80)
    print("CONSISTENCY METRICS")
    print("-" * 80)
    
    metrics_consistency = [
        ('Max Consecutive Wins', 'max_consecutive_wins', '{}'),
        ('Max Consecutive Losses', 'max_consecutive_losses', '{}'),
    ]
    
    for metric_name, metric_key, format_str in metrics_consistency:
        values = [format_str.format(stats[metric_key]) for stats in scenario_stats]
        print(f"{metric_name:<30} {values[0]:<20} {values[1]:<20} {values[2]:<20}")
    
    print("-" * 80)
    
    # FVG Type breakdown with detailed ratios
    print("\n" + "-" * 80)
    print("DETAILED BREAKDOWN BY FVG TYPE (BULLISH vs BEARISH)")
    print("-" * 80)
    
    for scenario in ['A', 'B', 'C']:
        scenario_data = results_df[results_df['scenario'] == scenario]
        
        if len(scenario_data) == 0:
            continue
        
        print(f"\n{'=' * 80}")
        print(f"SCENARIO {scenario} - {scenario_names[scenario]}")
        print(f"{'=' * 80}")
        print(f"Total FVGs: {len(scenario_data)}")
        
        bullish_data = scenario_data[scenario_data['type'] == 'bullish']
        bearish_data = scenario_data[scenario_data['type'] == 'bearish']
        
        # Bullish FVGs detailed stats
        print(f"\n  BULLISH FVGs: {len(bullish_data)} ({len(bullish_data)/len(scenario_data)*100:.1f}%)")
        if len(bullish_data) > 0:
            mitigated_bullish = bullish_data[bullish_data['is_mitigated']]
            num_mitigated = len(mitigated_bullish)
            print(f"    Mitigated: {num_mitigated}/{len(bullish_data)} ({num_mitigated/len(bullish_data)*100:.1f}%)")
            
            if num_mitigated > 0:
                # RR 1:1 stats
                wins_rr1 = mitigated_bullish['tp1_hit'].sum()
                losses_rr1 = num_mitigated - wins_rr1
                print(f"    RR 1:1 - Wins: {wins_rr1}/{num_mitigated} ({wins_rr1/num_mitigated*100:.1f}%) | Losses: {losses_rr1} ({losses_rr1/num_mitigated*100:.1f}%)")
                
                # RR 2:1 stats
                wins_rr2 = mitigated_bullish['tp2_hit'].sum()
                losses_rr2 = num_mitigated - wins_rr2
                print(f"    RR 2:1 - Wins: {wins_rr2}/{num_mitigated} ({wins_rr2/num_mitigated*100:.1f}%) | Losses: {losses_rr2} ({losses_rr2/num_mitigated*100:.1f}%)")
                
                # P&L stats
                winning = mitigated_bullish[mitigated_bullish['pnl_points'] > 0]
                losing = mitigated_bullish[mitigated_bullish['pnl_points'] <= 0]
                total_profit = winning['pnl_points'].sum() if len(winning) > 0 else 0.0
                total_loss = abs(losing['pnl_points'].sum()) if len(losing) > 0 else 0.0
                avg_profit = winning['pnl_points'].mean() if len(winning) > 0 else 0.0
                avg_loss = losing['pnl_points'].mean() if len(losing) > 0 else 0.0
                profit_factor = total_profit / total_loss if total_loss > 0 else 0.0
                expectancy = mitigated_bullish['pnl_points'].mean()
                
                print(f"    Profit: {total_profit:.2f} pts (Avg: {avg_profit:.2f}) | Loss: {total_loss:.2f} pts (Avg: {avg_loss:.2f})")
                print(f"    Profit Factor: {profit_factor:.2f} | Expectancy: {expectancy:.2f} pts")
        
        # Bearish FVGs detailed stats
        print(f"\n  BEARISH FVGs: {len(bearish_data)} ({len(bearish_data)/len(scenario_data)*100:.1f}%)")
        if len(bearish_data) > 0:
            mitigated_bearish = bearish_data[bearish_data['is_mitigated']]
            num_mitigated = len(mitigated_bearish)
            print(f"    Mitigated: {num_mitigated}/{len(bearish_data)} ({num_mitigated/len(bearish_data)*100:.1f}%)")
            
            if num_mitigated > 0:
                # RR 1:1 stats
                wins_rr1 = mitigated_bearish['tp1_hit'].sum()
                losses_rr1 = num_mitigated - wins_rr1
                print(f"    RR 1:1 - Wins: {wins_rr1}/{num_mitigated} ({wins_rr1/num_mitigated*100:.1f}%) | Losses: {losses_rr1} ({losses_rr1/num_mitigated*100:.1f}%)")
                
                # RR 2:1 stats
                wins_rr2 = mitigated_bearish['tp2_hit'].sum()
                losses_rr2 = num_mitigated - wins_rr2
                print(f"    RR 2:1 - Wins: {wins_rr2}/{num_mitigated} ({wins_rr2/num_mitigated*100:.1f}%) | Losses: {losses_rr2} ({losses_rr2/num_mitigated*100:.1f}%)")
                
                # P&L stats
                winning = mitigated_bearish[mitigated_bearish['pnl_points'] > 0]
                losing = mitigated_bearish[mitigated_bearish['pnl_points'] <= 0]
                total_profit = winning['pnl_points'].sum() if len(winning) > 0 else 0.0
                total_loss = abs(losing['pnl_points'].sum()) if len(losing) > 0 else 0.0
                avg_profit = winning['pnl_points'].mean() if len(winning) > 0 else 0.0
                avg_loss = losing['pnl_points'].mean() if len(losing) > 0 else 0.0
                profit_factor = total_profit / total_loss if total_loss > 0 else 0.0
                expectancy = mitigated_bearish['pnl_points'].mean()
                
                print(f"    Profit: {total_profit:.2f} pts (Avg: {avg_profit:.2f}) | Loss: {total_loss:.2f} pts (Avg: {avg_loss:.2f})")
                print(f"    Profit Factor: {profit_factor:.2f} | Expectancy: {expectancy:.2f} pts")
    
    # Time distribution
    print("\n" + "-" * 80)
    print("DISTRIBUTION BY HOUR (LONDON KILLZONE)")
    print("-" * 80)
    
    results_df['hour'] = pd.to_datetime(results_df['datetime']).dt.hour
    hour_dist = results_df.groupby('hour').size()
    
    for hour in range(1, 5):  # 01:00 to 04:00
        count = hour_dist.get(hour, 0)
        pct = (count / len(results_df) * 100) if len(results_df) > 0 else 0
        print(f"  {hour:02d}:00 - {hour:02d}:59: {count} FVGs ({pct:.1f}%)")
    
    # Yearly breakdown
    print("\n" + "-" * 80)
    print("YEARLY PERFORMANCE")
    print("-" * 80)
    
    results_df['year'] = pd.to_datetime(results_df['datetime']).dt.year
    
    for year in sorted(results_df['year'].unique()):
        year_data = results_df[results_df['year'] == year]
        mitigated = year_data[year_data['is_mitigated']]
        
        if len(mitigated) > 0:
            wins = mitigated['tp1_hit'].sum()
            total_pnl = mitigated['pnl_points'].sum()
            print(f"\n  Year {year}:")
            print(f"    Total FVGs: {len(year_data)}")
            print(f"    Trades: {len(mitigated)}")
            print(f"    Win Rate (RR 1:1): {wins/len(mitigated)*100:.1f}%")
            print(f"    Total P&L: {total_pnl:.2f} points")


def save_results(results_df: pd.DataFrame, output_path: str):
    """
    Save detailed results to CSV file.
    
    Args:
        results_df: DataFrame with all analysis results
        output_path: Path to save the CSV file
    """
    print("\n" + "=" * 80)
    print("SAVING RESULTS")
    print("=" * 80)
    
    # Select relevant columns for output
    output_columns = [
        'datetime', 'type', 'scenario', 'gap_size', 'zone_low', 'zone_high',
        'is_mitigated', 'entry_price', 'stop_loss', 'tp1', 'tp2',
        'tp1_hit', 'tp2_hit', 'sl_hit', 'pnl_points', 'outcome'
    ]
    
    # Filter to include only columns that exist
    available_columns = [col for col in output_columns if col in results_df.columns]
    
    output_df = results_df[available_columns].copy()
    output_df.to_csv(output_path, index=False)
    
    print(f"Results saved to: {output_path}")
    print(f"Total rows: {len(output_df)}")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """
    Main execution function.
    """
    print("\n" + "=" * 80)
    print("LONDON KILLZONE FVG SCENARIO ANALYSIS")
    print("=" * 80)
    print(f"Analysis Period: 2018-2025")
    print(f"London Killzone: 01:00-04:00 NY Time")
    print(f"Mitigation Window: {MITIGATION_WINDOW * 5} minutes ({MITIGATION_WINDOW} candles)")
    print(f"Lookback Period: {LOOKBACK_CANDLES * 5} minutes ({LOOKBACK_CANDLES} candles)")
    print("=" * 80)
    
    # Get base path
    base_path = "/home/runner/work/Backtest-Trading/Backtest-Trading"
    
    # Load all data
    df = load_all_data(base_path)
    
    # Filter for London Killzone hours
    lk_df = filter_london_killzone(df)
    
    # Detect FVGs
    fvg_df = detect_fvgs(lk_df)
    
    if len(fvg_df) == 0:
        print("\nNo FVGs detected. Exiting.")
        return
    
    # Analyze FVGs (mitigation, scenarios, trades)
    results_df = analyze_fvgs(fvg_df, df)  # Use full df for forward-looking analysis
    
    # Print results
    print_results(results_df)
    
    # Save results
    output_path = os.path.join(base_path, "london_killzone_fvg_analysis_results.csv")
    save_results(results_df, output_path)
    
    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE!")
    print("=" * 80)


if __name__ == "__main__":
    main()

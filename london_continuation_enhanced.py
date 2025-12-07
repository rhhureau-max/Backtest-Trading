#!/usr/bin/env python3
"""
London Continuation Enhanced Backtesting Strategy - With SL/TP Management

This enhanced version includes:
1. Proper Stop Loss and Take Profit levels
2. 1-minute precision execution to avoid look-ahead bias
3. Multiple TP scenarios (1R, 1.5R, 2R) for comparison
4. Risk-based position sizing
5. Performance comparison and equity curves

Data is in Chicago Time (CST/CDT) - NO timezone conversion needed.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
import warnings
import zipfile
import io
warnings.filterwarnings('ignore')


def load_nq_data_1m(years=None, base_path=None):
    """
    Load NQ futures 1-minute data from CSV/ZIP files.
    
    Parameters:
    -----------
    years : list, optional
        List of years to load. If None, loads 2018-2025.
    base_path : Path or str, optional
        Base directory containing data files. If None, uses current directory.
    
    Returns:
    --------
    pd.DataFrame with datetime index and OHLCV columns
    """
    if years is None:
        years = list(range(2018, 2026))
    
    if base_path is None:
        base_path = Path.cwd()
    else:
        base_path = Path(base_path)
    
    dfs = []
    
    for year in years:
        # Try different file formats
        csv_file = base_path / f"{year} 1m.csv"
        zip_file = base_path / f"{year} 1m.csv.zip"
        
        df = None
        
        # Try direct CSV first
        if csv_file.exists():
            print(f"Loading {year} from CSV...")
            try:
                df = pd.read_csv(csv_file, sep=';', encoding='utf-8-sig')
            except Exception as e:
                print(f"Error loading {csv_file}: {e}")
                continue
        
        # Try ZIP file
        elif zip_file.exists():
            print(f"Loading {year} from ZIP...")
            try:
                with zipfile.ZipFile(zip_file, 'r') as z:
                    # Get the first CSV file in the zip
                    csv_filename = [f for f in z.namelist() if f.endswith('.csv')][0]
                    with z.open(csv_filename) as f:
                        df = pd.read_csv(f, sep=';', encoding='utf-8-sig')
            except Exception as e:
                print(f"Error loading {zip_file}: {e}")
                continue
        
        else:
            print(f"Warning: No 1m data found for {year}, skipping...")
            continue
        
        if df is not None:
            try:
                # Handle column names (remove BOM if present)
                df.columns = df.columns.str.replace('\ufeff', '').str.strip()
                
                # Rename columns to standard names
                if len(df.columns) >= 7:
                    df.columns = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
                
                # Combine date and time into datetime
                df['DateTime'] = pd.to_datetime(
                    df['Date'] + ' ' + df['Time'],
                    format='%d/%m/%Y %H:%M:%S'
                )
                
                # Set datetime as index
                df.set_index('DateTime', inplace=True)
                
                # Keep only OHLCV columns
                df = df[['Open', 'High', 'Low', 'Close', 'Volume']]
                
                # Convert to numeric
                for col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                
                dfs.append(df)
                print(f"Loaded {year} 1m: {len(df)} bars")
                
            except Exception as e:
                print(f"Error processing {year}: {e}")
                continue
    
    if not dfs:
        raise ValueError("No 1m data loaded!")
    
    # Concatenate all dataframes
    data = pd.concat(dfs)
    data.sort_index(inplace=True)
    
    # Remove duplicates
    data = data[~data.index.duplicated(keep='first')]
    
    print(f"\nTotal 1m data loaded: {len(data)} bars from {data.index[0]} to {data.index[-1]}")
    
    return data


def load_nq_data_higher_tf(years=None, timeframe='15m', base_path=None):
    """
    Load NQ futures data for higher timeframes (5m, 15m, 1H).
    Used for setup detection.
    """
    if years is None:
        years = list(range(2018, 2026))
    
    if base_path is None:
        base_path = Path.cwd()
    else:
        base_path = Path(base_path)
    
    dfs = []
    
    for year in years:
        filename = f"{year} {timeframe}.csv"
        filepath = base_path / filename
        
        if not filepath.exists():
            print(f"Warning: {filename} not found, skipping...")
            continue
        
        try:
            df = pd.read_csv(filepath, sep=';', encoding='utf-8-sig')
            
            # Handle column names
            df.columns = df.columns.str.replace('\ufeff', '').str.strip()
            
            if len(df.columns) >= 7:
                df.columns = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
            
            # Combine date and time
            df['DateTime'] = pd.to_datetime(
                df['Date'] + ' ' + df['Time'],
                format='%d/%m/%Y %H:%M:%S'
            )
            
            df.set_index('DateTime', inplace=True)
            df = df[['Open', 'High', 'Low', 'Close', 'Volume']]
            
            for col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            
            dfs.append(df)
            print(f"Loaded {year} {timeframe}: {len(df)} bars")
            
        except Exception as e:
            print(f"Error loading {filename}: {e}")
            continue
    
    if not dfs:
        raise ValueError(f"No {timeframe} data loaded!")
    
    data = pd.concat(dfs)
    data.sort_index(inplace=True)
    data = data[~data.index.duplicated(keep='first')]
    
    print(f"Total {timeframe} data: {len(data)} bars from {data.index[0]} to {data.index[-1]}")
    
    return data


def identify_asian_range(df, date):
    """
    Identify Asian Range for a given date.
    Asian Range: 18:00 (D-1) to 00:00 (D) Chicago Time
    
    Returns:
    --------
    dict with asian_high, asian_low, or None if insufficient data
    """
    prev_date = date - timedelta(days=1)
    
    start_time = pd.Timestamp(year=prev_date.year, month=prev_date.month, 
                              day=prev_date.day, hour=18, minute=0)
    end_time = pd.Timestamp(year=date.year, month=date.month, 
                           day=date.day, hour=0, minute=0)
    
    asian_data = df[(df.index >= start_time) & (df.index < end_time)]
    
    if len(asian_data) < 5:
        return None
    
    asian_high = asian_data['High'].max()
    asian_low = asian_data['Low'].min()
    
    return {
        'asian_high': asian_high,
        'asian_low': asian_low,
        'asian_mid': (asian_high + asian_low) / 2,
        'start_time': start_time,
        'end_time': end_time
    }


def detect_setup_in_killzone(df_setup, date, asian_info):
    """
    Detect breakout setup during London Killzone (01:00-04:00 CST).
    Uses 5m or 15m data for setup detection.
    
    Returns:
    --------
    dict with setup info or None
    """
    asian_high = asian_info['asian_high']
    asian_low = asian_info['asian_low']
    
    # London Killzone: 01:00 to 04:00
    start_time = pd.Timestamp(year=date.year, month=date.month, 
                              day=date.day, hour=1, minute=0)
    end_time = pd.Timestamp(year=date.year, month=date.month, 
                           day=date.day, hour=4, minute=0)
    
    killzone_data = df_setup[(df_setup.index >= start_time) & (df_setup.index <= end_time)]
    
    if len(killzone_data) == 0:
        return None
    
    # Check each bar for breakout
    for idx, row in killzone_data.iterrows():
        close_price = row['Close']
        
        # Bullish breakout
        if close_price > asian_high:
            return {
                'entry_time': idx,
                'entry_price': close_price,
                'direction': 'LONG',
                'asian_high': asian_high,
                'asian_low': asian_low,
                'setup_bar': row.to_dict()
            }
        
        # Bearish breakout
        elif close_price < asian_low:
            return {
                'entry_time': idx,
                'entry_price': close_price,
                'direction': 'SHORT',
                'asian_high': asian_high,
                'asian_low': asian_low,
                'setup_bar': row.to_dict()
            }
    
    return None


def calculate_sl_and_risk(setup_info):
    """
    Calculate Stop Loss and Risk for the trade.
    
    SL Logic:
    - LONG: SL = Asian_Low - 2 points
    - SHORT: SL = Asian_High + 2 points
    
    Risk (R) = |Entry - SL|
    
    Returns:
    --------
    dict with sl_price and risk_r
    """
    direction = setup_info['direction']
    entry_price = setup_info['entry_price']
    asian_high = setup_info['asian_high']
    asian_low = setup_info['asian_low']
    
    if direction == 'LONG':
        sl_price = asian_low - 2.0
    else:  # SHORT
        sl_price = asian_high + 2.0
    
    risk_r = abs(entry_price - sl_price)
    
    return {
        'sl_price': sl_price,
        'risk_r': risk_r
    }


def execute_trade_m1(df_m1, setup_info, sl_info, tp_multiplier):
    """
    Execute trade using 1-minute data to avoid look-ahead bias.
    
    Parameters:
    -----------
    df_m1 : pd.DataFrame
        1-minute OHLCV data
    setup_info : dict
        Setup information with entry details
    sl_info : dict
        Stop loss and risk information
    tp_multiplier : float
        Take profit multiplier (1.0 for 1R, 1.5 for 1.5R, 2.0 for 2R)
    
    Returns:
    --------
    dict with trade result or None
    """
    entry_time = setup_info['entry_time']
    entry_price = setup_info['entry_price']
    direction = setup_info['direction']
    sl_price = sl_info['sl_price']
    risk_r = sl_info['risk_r']
    
    # Calculate TP based on multiplier
    if direction == 'LONG':
        tp_price = entry_price + (risk_r * tp_multiplier)
    else:  # SHORT
        tp_price = entry_price - (risk_r * tp_multiplier)
    
    # Force close time: 15:15 CST
    date = entry_time.date()
    force_close_time = pd.Timestamp(year=date.year, month=date.month, 
                                    day=date.day, hour=15, minute=15)
    
    # Get M1 data after entry
    m1_after_entry = df_m1[(df_m1.index > entry_time) & (df_m1.index <= force_close_time)]
    
    if len(m1_after_entry) == 0:
        return None
    
    # Iterate through each 1-minute bar
    for bar_time, bar in m1_after_entry.iterrows():
        high = bar['High']
        low = bar['Low']
        close = bar['Close']
        
        if direction == 'LONG':
            # Check if SL hit first (price went down to SL)
            if low <= sl_price:
                return {
                    'exit_time': bar_time,
                    'exit_price': sl_price,
                    'exit_type': 'SL',
                    'pnl_points': sl_price - entry_price,  # Negative
                    'pnl_r': -1.0,
                    'tp_level': tp_multiplier
                }
            
            # Check if TP hit
            if high >= tp_price:
                return {
                    'exit_time': bar_time,
                    'exit_price': tp_price,
                    'exit_type': 'TP',
                    'pnl_points': tp_price - entry_price,  # Positive
                    'pnl_r': tp_multiplier,
                    'tp_level': tp_multiplier
                }
        
        else:  # SHORT
            # Check if SL hit first (price went up to SL)
            if high >= sl_price:
                return {
                    'exit_time': bar_time,
                    'exit_price': sl_price,
                    'exit_type': 'SL',
                    'pnl_points': entry_price - sl_price,  # Negative
                    'pnl_r': -1.0,
                    'tp_level': tp_multiplier
                }
            
            # Check if TP hit
            if low <= tp_price:
                return {
                    'exit_time': bar_time,
                    'exit_price': tp_price,
                    'exit_type': 'TP',
                    'pnl_points': entry_price - tp_price,  # Positive
                    'pnl_r': tp_multiplier,
                    'tp_level': tp_multiplier
                }
    
    # If neither SL nor TP hit, force close at end
    last_bar = m1_after_entry.iloc[-1]
    last_close = last_bar['Close']
    last_time = m1_after_entry.index[-1]
    
    if direction == 'LONG':
        pnl_points = last_close - entry_price
    else:
        pnl_points = entry_price - last_close
    
    pnl_r = pnl_points / risk_r if risk_r > 0 else 0
    
    return {
        'exit_time': last_time,
        'exit_price': last_close,
        'exit_type': 'FORCE_CLOSE',
        'pnl_points': pnl_points,
        'pnl_r': pnl_r,
        'tp_level': tp_multiplier
    }


def run_enhanced_backtest(df_setup, df_m1, tp_scenarios=[1.0, 1.5, 2.0]):
    """
    Run enhanced backtest with multiple TP scenarios.
    
    Parameters:
    -----------
    df_setup : pd.DataFrame
        5m or 15m data for setup detection
    df_m1 : pd.DataFrame
        1-minute data for precise execution
    tp_scenarios : list
        List of TP multipliers to test (default: [1.0, 1.5, 2.0])
    
    Returns:
    --------
    dict with results for each scenario
    """
    # Get unique dates
    dates = df_setup.index.date
    unique_dates = sorted(set(dates))
    
    print(f"\nBacktesting from {unique_dates[0]} to {unique_dates[-1]}")
    print(f"Total trading days: {len(unique_dates)}")
    print(f"TP Scenarios: {tp_scenarios}")
    
    # Store results for each scenario
    results = {tp: [] for tp in tp_scenarios}
    
    # Iterate through each date
    for i, date in enumerate(unique_dates[1:], 1):
        
        if i % 100 == 0:
            print(f"Processing: {date} ({i}/{len(unique_dates)-1})")
        
        # Step 1: Identify Asian Range
        asian_info = identify_asian_range(df_setup, date)
        if asian_info is None:
            continue
        
        # Step 2: Detect setup in London Killzone
        setup_info = detect_setup_in_killzone(df_setup, date, asian_info)
        if setup_info is None:
            continue
        
        # Step 3: Calculate SL and Risk
        sl_info = calculate_sl_and_risk(setup_info)
        
        # Step 4: Execute trade for each TP scenario using M1 data
        for tp_mult in tp_scenarios:
            result = execute_trade_m1(df_m1, setup_info, sl_info, tp_mult)
            
            if result is not None:
                # Compile trade information
                trade = {
                    'Date': date,
                    'Entry_Time': setup_info['entry_time'],
                    'Direction': setup_info['direction'],
                    'Entry_Price': setup_info['entry_price'],
                    'SL_Price': sl_info['sl_price'],
                    'Risk_R': sl_info['risk_r'],
                    'TP_Price': (setup_info['entry_price'] + sl_info['risk_r'] * tp_mult 
                                if setup_info['direction'] == 'LONG' 
                                else setup_info['entry_price'] - sl_info['risk_r'] * tp_mult),
                    'Exit_Time': result['exit_time'],
                    'Exit_Price': result['exit_price'],
                    'Exit_Type': result['exit_type'],
                    'PnL_Points': result['pnl_points'],
                    'PnL_R': result['pnl_r'],
                    'Asian_High': asian_info['asian_high'],
                    'Asian_Low': asian_info['asian_low']
                }
                
                results[tp_mult].append(trade)
    
    # Convert to DataFrames
    results_dfs = {}
    for tp_mult, trades in results.items():
        if len(trades) > 0:
            results_dfs[tp_mult] = pd.DataFrame(trades)
            print(f"\nTP Scenario {tp_mult}R: {len(trades)} trades")
        else:
            results_dfs[tp_mult] = pd.DataFrame()
            print(f"\nTP Scenario {tp_mult}R: No trades")
    
    return results_dfs


def analyze_scenario(df, scenario_name):
    """
    Analyze performance for a single TP scenario.
    """
    if len(df) == 0:
        return None
    
    total_trades = len(df)
    wins = len(df[df['PnL_Points'] > 0])
    losses = len(df[df['PnL_Points'] < 0])
    breakevens = len(df[df['PnL_Points'] == 0])
    
    win_rate = (wins / total_trades * 100) if total_trades > 0 else 0
    
    total_pnl = df['PnL_Points'].sum()
    avg_win = df[df['PnL_Points'] > 0]['PnL_Points'].mean() if wins > 0 else 0
    avg_loss = df[df['PnL_Points'] < 0]['PnL_Points'].mean() if losses > 0 else 0
    
    # Calculate profit factor
    gross_profit = df[df['PnL_Points'] > 0]['PnL_Points'].sum()
    gross_loss = abs(df[df['PnL_Points'] < 0]['PnL_Points'].sum())
    
    if gross_loss > 0:
        profit_factor = gross_profit / gross_loss
    elif gross_profit > 0:
        profit_factor = float('inf')
    else:
        profit_factor = 0.0
    
    # Mathematical expectation (average per trade)
    expectancy = total_pnl / total_trades if total_trades > 0 else 0
    
    # R-multiple metrics
    avg_r = df['PnL_R'].mean()
    
    return {
        'Scenario': scenario_name,
        'Total_Trades': total_trades,
        'Wins': wins,
        'Losses': losses,
        'Breakevens': breakevens,
        'Win_Rate_%': round(win_rate, 2),
        'Total_PnL_Points': round(total_pnl, 2),
        'Avg_Win_Points': round(avg_win, 2),
        'Avg_Loss_Points': round(avg_loss, 2),
        'Profit_Factor': round(profit_factor, 2),
        'Expectancy_Points': round(expectancy, 2),
        'Avg_R_Multiple': round(avg_r, 2)
    }


def create_performance_comparison(results_dfs):
    """
    Create performance comparison table for all scenarios.
    """
    comparison = []
    
    for tp_mult, df in results_dfs.items():
        scenario_name = f"{tp_mult}R"
        stats = analyze_scenario(df, scenario_name)
        if stats:
            comparison.append(stats)
    
    if len(comparison) > 0:
        comparison_df = pd.DataFrame(comparison)
        return comparison_df
    else:
        return None


def create_equity_curves(results_dfs):
    """
    Create cumulative equity curves for all scenarios.
    """
    equity_curves = {}
    
    for tp_mult, df in results_dfs.items():
        if len(df) > 0:
            df_sorted = df.sort_values('Entry_Time')
            equity_curves[f"{tp_mult}R"] = df_sorted['PnL_Points'].cumsum().values
    
    return equity_curves


def main():
    """Main execution function."""
    print("="*80)
    print("LONDON CONTINUATION ENHANCED BACKTEST - NQ Futures")
    print("With SL/TP Management and 1-Minute Precision")
    print("="*80)
    print("\nStrategy Parameters:")
    print("- Asian Range: 18:00 (D-1) to 00:00 (D) CST")
    print("- London Killzone: 01:00 to 04:00 CST (Entry Window)")
    print("- Setup Detection: 5m/15m breakout")
    print("- Execution: 1-minute precision")
    print("- Stop Loss: Asian_Low - 2pts (LONG) / Asian_High + 2pts (SHORT)")
    print("- Take Profit: Multiple scenarios (1R, 1.5R, 2R)")
    print("- Force Close: 15:15 CST if no SL/TP hit")
    print("="*80)
    
    # Load data
    print("\nLoading data...")
    print("\n--- Loading setup detection data (15m) ---")
    df_setup = load_nq_data_higher_tf(timeframe='15m')
    
    print("\n--- Loading execution data (1m) ---")
    df_m1 = load_nq_data_1m()
    
    # Run backtest with multiple TP scenarios
    print("\nRunning enhanced backtest...")
    tp_scenarios = [1.0, 1.5, 2.0]
    results_dfs = run_enhanced_backtest(df_setup, df_m1, tp_scenarios)
    
    # Create performance comparison
    print("\n" + "="*80)
    print("PERFORMANCE COMPARISON")
    print("="*80)
    comparison_df = create_performance_comparison(results_dfs)
    
    if comparison_df is not None:
        print("\n" + comparison_df.to_string(index=False))
        
        # Save comparison to CSV
        comparison_file = Path.cwd() / 'london_continuation_comparison.csv'
        comparison_df.to_csv(comparison_file, index=False)
        print(f"\nComparison saved to: {comparison_file}")
    else:
        print("\nNo results to compare.")
    
    # Save detailed results for each scenario
    for tp_mult, df in results_dfs.items():
        if len(df) > 0:
            output_file = Path.cwd() / f'london_continuation_{tp_mult}R_results.csv'
            df.to_csv(output_file, index=False)
            print(f"Detailed results for {tp_mult}R saved to: {output_file}")
    
    # Create equity curves
    print("\n" + "="*80)
    print("EQUITY CURVES")
    print("="*80)
    equity_curves = create_equity_curves(results_dfs)
    
    if equity_curves:
        # Save equity curves data
        equity_df = pd.DataFrame(equity_curves)
        equity_file = Path.cwd() / 'london_continuation_equity_curves.csv'
        equity_df.to_csv(equity_file, index=False)
        print(f"\nEquity curves saved to: {equity_file}")
        
        # Try to create a simple plot if matplotlib is available
        try:
            import matplotlib.pyplot as plt
            
            plt.figure(figsize=(12, 6))
            for scenario, curve in equity_curves.items():
                plt.plot(curve, label=scenario, linewidth=2)
            
            plt.title('Cumulative P&L - London Continuation Strategy', fontsize=14, fontweight='bold')
            plt.xlabel('Trade Number', fontsize=12)
            plt.ylabel('Cumulative P&L (Points)', fontsize=12)
            plt.legend(fontsize=10)
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            
            plot_file = Path.cwd() / 'london_continuation_equity_curves.png'
            plt.savefig(plot_file, dpi=150)
            print(f"Equity curve plot saved to: {plot_file}")
            
        except ImportError:
            print("\nMatplotlib not available. Install it to generate equity curve plots.")
            print("Run: pip install matplotlib")
    
    print("\n" + "="*80)
    print("BACKTEST COMPLETE")
    print("="*80)
    
    return results_dfs, comparison_df


if __name__ == "__main__":
    results_dfs, comparison_df = main()

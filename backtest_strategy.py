#!/usr/bin/env python3
"""
Backtesting Strategy: 8:30 AM Candle Analysis with Risk Management
Analyzes 1m, 5m, and 15m timeframes from 2018-2025
Enhanced with Stop Loss levels and Risk-Reward ratio analysis
"""

import pandas as pd
import numpy as np
from datetime import datetime, time
import zipfile
import os
from pathlib import Path

# Configuration
BASE_DIR = Path(__file__).parent.absolute()
YEARS = range(2018, 2026)  # 2018 to 2025
TIMEFRAMES = ['1m', '5m', '15m']
TARGET_TIME = time(8, 30)  # 8:30 AM

# Risk Management Configuration
SL_LEVELS = [100, 75, 50, 25]  # Stop Loss percentages of candle body
RR_RATIOS = [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]  # Risk-Reward ratios


def load_csv_data(filepath, is_zipped=False):
    """Load CSV data from file or zip archive."""
    try:
        if is_zipped:
            zip_path = filepath
            csv_filename = filepath.stem  # Get filename without .zip extension
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                # Read the CSV file from the zip
                with zip_ref.open(f"{csv_filename}") as csv_file:
                    df = pd.read_csv(csv_file, sep=';', header=0)
        else:
            df = pd.read_csv(filepath, sep=';', header=0)
        
        # Rename columns to standard names
        df.columns = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
        
        # Parse datetime
        df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%d/%m/%Y %H:%M:%S')
        df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')
        df['Time'] = pd.to_datetime(df['Time'], format='%H:%M:%S').dt.time
        
        # Convert price columns to float
        for col in ['Open', 'High', 'Low', 'Close']:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        df['Volume'] = pd.to_numeric(df['Volume'], errors='coerce')
        
        # Sort by datetime
        df = df.sort_values('DateTime').reset_index(drop=True)
        
        return df
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return None


def is_bullish_candle(row):
    """Check if candle is bullish (close > open)."""
    return row['Close'] > row['Open']


def is_bearish_candle(row):
    """Check if candle is bearish (close < open)."""
    return row['Close'] < row['Open']


def check_bullish_condition(df, idx, lookback=5):
    """
    Check if bullish condition is met:
    Close of current candle > max(highs of previous 5 candles)
    """
    if idx < lookback:
        return False, None
    
    current_close = df.loc[idx, 'Close']
    previous_highs = df.loc[idx-lookback:idx-1, 'High'].values
    max_previous_high = np.max(previous_highs)
    
    return current_close > max_previous_high, max_previous_high


def check_bearish_condition(df, idx, lookback=5):
    """
    Check if bearish condition is met:
    Close of current candle < min(lows of previous 5 candles)
    """
    if idx < lookback:
        return False, None
    
    current_close = df.loc[idx, 'Close']
    previous_lows = df.loc[idx-lookback:idx-1, 'Low'].values
    min_previous_low = np.min(previous_lows)
    
    return current_close < min_previous_low, min_previous_low


def calculate_sl_levels(trade_row):
    """
    Calculate Stop Loss levels based on candle body retracement.
    
    For LONG trades:
        Body = Close - Open
        SL_100 = Open (Close - 1.00 * Body)
        SL_75 = Close - 0.75 * Body
        SL_50 = Close - 0.50 * Body
        SL_25 = Close - 0.25 * Body
    
    For SHORT trades:
        Body = Open - Close
        SL_100 = Open (Close + 1.00 * Body)
        SL_75 = Close + 0.75 * Body
        SL_50 = Close + 0.50 * Body
        SL_25 = Close + 0.25 * Body
    """
    direction = trade_row['Direction']
    open_price = trade_row['Open']
    close_price = trade_row['Close']
    
    if direction == 'LONG':
        body = close_price - open_price
        sl_100 = open_price  # 100% retracement
        sl_75 = close_price - 0.75 * body
        sl_50 = close_price - 0.50 * body
        sl_25 = close_price - 0.25 * body
    else:  # SHORT
        body = open_price - close_price
        sl_100 = open_price  # 100% retracement
        sl_75 = close_price + 0.75 * body
        sl_50 = close_price + 0.50 * body
        sl_25 = close_price + 0.25 * body
    
    return {
        'SL_100': sl_100,
        'SL_75': sl_75,
        'SL_50': sl_50,
        'SL_25': sl_25,
        'Body_Size': body
    }


def calculate_tp_levels(trade_row, sl_levels):
    """
    Calculate Take Profit levels for all Risk-Reward ratios.
    
    For LONG trades: TP = Entry + (SL_Distance * RR)
    For SHORT trades: TP = Entry - (SL_Distance * RR)
    """
    direction = trade_row['Direction']
    entry = trade_row['Close']  # Entry at close of 8:30 candle
    
    tp_levels = {}
    for sl_name, sl_price in sl_levels.items():
        if sl_name == 'Body_Size':
            continue
        
        sl_distance = abs(entry - sl_price)
        
        for rr in RR_RATIOS:
            if direction == 'LONG':
                tp = entry + (sl_distance * rr)
            else:  # SHORT
                tp = entry - (sl_distance * rr)
            
            tp_levels[f'{sl_name}_TP_{rr}'] = tp
    
    return tp_levels


def analyze_trade_outcome(df, trade_idx, trade_row, sl_levels, tp_levels):
    """
    Analyze subsequent candles to determine if SL or TP was hit first.
    Returns a dictionary with results for each SL/RR combination.
    """
    direction = trade_row['Direction']
    entry = trade_row['Close']
    
    # Get subsequent candles (look ahead for the rest of the day)
    # Limit to reasonable lookback (e.g., next 100 candles)
    max_lookback = min(100, len(df) - trade_idx - 1)
    
    if max_lookback <= 0:
        return {}
    
    subsequent_candles = df.iloc[trade_idx + 1:trade_idx + 1 + max_lookback]
    
    results = {}
    
    # Analyze each SL level
    for sl_name in ['SL_100', 'SL_75', 'SL_50', 'SL_25']:
        sl_price = sl_levels[sl_name]
        
        # For each RR ratio
        for rr in RR_RATIOS:
            tp_key = f'{sl_name}_TP_{rr}'
            tp_price = tp_levels[tp_key]
            
            result_key = f'{sl_name}_RR_{rr}'
            
            # Check each subsequent candle
            outcome = None
            hit_candle_idx = None
            pnl = 0
            
            for i, (idx, candle) in enumerate(subsequent_candles.iterrows()):
                if direction == 'LONG':
                    # Check if SL hit (low touches or goes below SL)
                    if candle['Low'] <= sl_price:
                        outcome = 'LOSS'
                        pnl = sl_price - entry
                        hit_candle_idx = i + 1
                        break
                    # Check if TP hit (high touches or goes above TP)
                    if candle['High'] >= tp_price:
                        outcome = 'WIN'
                        pnl = tp_price - entry
                        hit_candle_idx = i + 1
                        break
                else:  # SHORT
                    # Check if SL hit (high touches or goes above SL)
                    if candle['High'] >= sl_price:
                        outcome = 'LOSS'
                        pnl = entry - sl_price
                        hit_candle_idx = i + 1
                        break
                    # Check if TP hit (low touches or goes below TP)
                    if candle['Low'] <= tp_price:
                        outcome = 'WIN'
                        pnl = entry - tp_price
                        hit_candle_idx = i + 1
                        break
            
            if outcome is None:
                outcome = 'NO_TOUCH'
                pnl = 0
                hit_candle_idx = None
            
            results[result_key] = {
                'Outcome': outcome,
                'PnL': pnl,
                'Candles_To_Hit': hit_candle_idx,
                'SL_Price': sl_price,
                'TP_Price': tp_price
            }
    
    return results


def find_trades_in_timeframe(timeframe, years):
    """Find all valid trades for a specific timeframe across multiple years."""
    print(f"\n{'='*60}")
    print(f"Analyzing {timeframe} timeframe...")
    print(f"{'='*60}")
    
    all_trades = []
    
    for year in years:
        # Determine file path
        if timeframe == '1m':
            if year == 2025:
                # 2025 1m data is not zipped
                filepath = BASE_DIR / f"{year} {timeframe}.csv"
                is_zipped = False
            else:
                filepath = BASE_DIR / f"{year} {timeframe}.csv.zip"
                is_zipped = True
        else:
            filepath = BASE_DIR / f"{year} {timeframe}.csv"
            is_zipped = False
        
        if not filepath.exists():
            print(f"  Warning: File not found - {filepath}")
            continue
        
        print(f"  Loading {year} data...")
        df = load_csv_data(filepath, is_zipped)
        
        if df is None or len(df) == 0:
            print(f"  Warning: No data loaded for {year}")
            continue
        
        print(f"    Loaded {len(df)} candles")
        
        # Find all 8:30 AM candles
        target_candles = df[df['Time'] == TARGET_TIME].copy()
        print(f"    Found {len(target_candles)} 8:30 AM candles")
        
        # Analyze each 8:30 AM candle
        trades_found = 0
        for _, target_row in target_candles.iterrows():
            target_idx = target_row.name
            target_date = target_row['Date']
            
            is_bullish = is_bullish_candle(target_row)
            is_bearish = is_bearish_candle(target_row)
            
            trade_entry = None
            
            if is_bullish:
                # Check bullish condition
                condition_met, reference_level = check_bullish_condition(df, target_idx)
                if condition_met:
                    trade_entry = {
                        'Date': target_date.strftime('%Y-%m-%d'),
                        'Time': '08:30:00',
                        'Timeframe': timeframe,
                        'Direction': 'LONG',
                        'Open': target_row['Open'],
                        'High': target_row['High'],
                        'Low': target_row['Low'],
                        'Close': target_row['Close'],
                        'Volume': target_row['Volume'],
                        'Reference_Level': reference_level,
                        'Condition': f"Close ({target_row['Close']:.2f}) > Max Previous 5 Highs ({reference_level:.2f})"
                    }
            
            elif is_bearish:
                # Check bearish condition
                condition_met, reference_level = check_bearish_condition(df, target_idx)
                if condition_met:
                    trade_entry = {
                        'Date': target_date.strftime('%Y-%m-%d'),
                        'Time': '08:30:00',
                        'Timeframe': timeframe,
                        'Direction': 'SHORT',
                        'Open': target_row['Open'],
                        'High': target_row['High'],
                        'Low': target_row['Low'],
                        'Close': target_row['Close'],
                        'Volume': target_row['Volume'],
                        'Reference_Level': reference_level,
                        'Condition': f"Close ({target_row['Close']:.2f}) < Min Previous 5 Lows ({reference_level:.2f})"
                    }
            
            if trade_entry:
                all_trades.append((trade_entry, target_idx, df))
                trades_found += 1
        
        print(f"    Found {trades_found} valid trades in {year}")
    
    return all_trades


def enhance_trades_with_risk_analysis(trades_data):
    """
    Enhance trades with risk management analysis.
    trades_data is a list of tuples: (trade_dict, index, dataframe)
    """
    print("\n" + "="*60)
    print("ENHANCING TRADES WITH RISK ANALYSIS...")
    print("="*60)
    
    enhanced_trades = []
    
    for i, (trade, trade_idx, df) in enumerate(trades_data):
        if (i + 1) % 100 == 0:
            print(f"  Processing trade {i + 1}/{len(trades_data)}...")
        
        # Calculate SL levels
        sl_levels = calculate_sl_levels(trade)
        
        # Calculate TP levels for all SL/RR combinations
        tp_levels = calculate_tp_levels(trade, sl_levels)
        
        # Analyze trade outcomes
        outcomes = analyze_trade_outcome(df, trade_idx, trade, sl_levels, tp_levels)
        
        # Create enhanced trade entry with all SL levels
        enhanced_trade = trade.copy()
        enhanced_trade.update(sl_levels)
        
        # Add all TP levels
        enhanced_trade.update(tp_levels)
        
        # Add outcomes for each SL/RR combination
        for result_key, result_data in outcomes.items():
            enhanced_trade[f'{result_key}_Outcome'] = result_data['Outcome']
            enhanced_trade[f'{result_key}_PnL'] = result_data['PnL']
            enhanced_trade[f'{result_key}_Candles'] = result_data['Candles_To_Hit']
        
        enhanced_trades.append(enhanced_trade)
    
    print(f"  ✓ Enhanced {len(enhanced_trades)} trades")
    return enhanced_trades


def generate_performance_summary(enhanced_trades_df, timeframe):
    """
    Generate performance summary for each SL/RR combination.
    """
    print(f"\n  Generating performance summary for {timeframe}...")
    
    summary_data = []
    
    for sl_level in SL_LEVELS:
        sl_name = f'SL_{sl_level}'
        
        for rr in RR_RATIOS:
            result_key = f'{sl_name}_RR_{rr}'
            outcome_col = f'{result_key}_Outcome'
            pnl_col = f'{result_key}_PnL'
            
            # Filter valid trades (exclude NO_TOUCH)
            valid_trades = enhanced_trades_df[enhanced_trades_df[outcome_col].isin(['WIN', 'LOSS'])]
            
            if len(valid_trades) == 0:
                continue
            
            # Calculate metrics
            total_trades = len(valid_trades)
            wins = len(valid_trades[valid_trades[outcome_col] == 'WIN'])
            losses = len(valid_trades[valid_trades[outcome_col] == 'LOSS'])
            no_touch = len(enhanced_trades_df[enhanced_trades_df[outcome_col] == 'NO_TOUCH'])
            
            win_rate = (wins / total_trades * 100) if total_trades > 0 else 0
            
            total_pnl = valid_trades[pnl_col].sum()
            avg_win = valid_trades[valid_trades[outcome_col] == 'WIN'][pnl_col].mean() if wins > 0 else 0
            avg_loss = valid_trades[valid_trades[outcome_col] == 'LOSS'][pnl_col].mean() if losses > 0 else 0
            
            summary_data.append({
                'Timeframe': timeframe,
                'SL_Level': sl_name,
                'RR_Ratio': rr,
                'Total_Trades': total_trades,
                'Wins': wins,
                'Losses': losses,
                'No_Touch': no_touch,
                'Win_Rate_%': round(win_rate, 2),
                'Total_PnL': round(total_pnl, 2),
                'Avg_Win': round(avg_win, 2),
                'Avg_Loss': round(avg_loss, 2),
                'Profit_Factor': round(abs(avg_win * wins / (avg_loss * losses)), 2) if (losses > 0 and avg_loss != 0) else 0
            })
    
    return pd.DataFrame(summary_data)


def generate_overall_summary(all_performance_summaries):
    """
    Generate an overall summary comparing all configurations.
    """
    print("\n" + "="*60)
    print("GENERATING OVERALL SUMMARY...")
    print("="*60)
    
    combined_df = pd.concat(all_performance_summaries, ignore_index=True)
    
    # Find best configurations
    best_by_pnl = combined_df.nlargest(10, 'Total_PnL')
    best_by_winrate = combined_df.nlargest(10, 'Win_Rate_%')
    best_by_profit_factor = combined_df.nlargest(10, 'Profit_Factor')
    
    print("\n📊 TOP 10 CONFIGURATIONS BY TOTAL P&L:")
    print(best_by_pnl[['Timeframe', 'SL_Level', 'RR_Ratio', 'Total_Trades', 'Win_Rate_%', 'Total_PnL']].to_string(index=False))
    
    print("\n📊 TOP 10 CONFIGURATIONS BY WIN RATE:")
    print(best_by_winrate[['Timeframe', 'SL_Level', 'RR_Ratio', 'Total_Trades', 'Win_Rate_%', 'Total_PnL']].to_string(index=False))
    
    print("\n📊 TOP 10 CONFIGURATIONS BY PROFIT FACTOR:")
    print(best_by_profit_factor[['Timeframe', 'SL_Level', 'RR_Ratio', 'Total_Trades', 'Win_Rate_%', 'Profit_Factor', 'Total_PnL']].to_string(index=False))
    
    return {
        'combined': combined_df,
        'best_pnl': best_by_pnl,
        'best_winrate': best_by_winrate,
        'best_profit_factor': best_by_profit_factor
    }


def main():
    """Main execution function."""
    print("="*60)
    print("BACKTESTING STRATEGY: 8:30 AM CANDLE ANALYSIS")
    print("WITH RISK MANAGEMENT & PROFIT ANALYSIS")
    print("="*60)
    print(f"Period: 2018-2025")
    print(f"Timeframes: {', '.join(TIMEFRAMES)}")
    print(f"Target Time: 08:30 AM")
    print(f"Stop Loss Levels: {', '.join([f'SL_{x}' for x in SL_LEVELS])}")
    print(f"Risk-Reward Ratios: {', '.join([str(x) for x in RR_RATIOS])}")
    print("="*60)
    
    # Store all results
    all_results = {}
    all_performance_summaries = []
    
    # Process each timeframe
    for timeframe in TIMEFRAMES:
        # Find trades (returns list of tuples with dataframe references)
        trades_data = find_trades_in_timeframe(timeframe, YEARS)
        
        if not trades_data:
            print(f"\n  ⚠ No trades found for {timeframe}")
            continue
        
        # Enhance trades with risk analysis
        enhanced_trades = enhance_trades_with_risk_analysis(trades_data)
        all_results[timeframe] = enhanced_trades
        
        # Convert to DataFrame
        df_enhanced = pd.DataFrame(enhanced_trades)
        
        # Save enhanced trades with all calculations
        output_file = BASE_DIR / f"trades_enhanced_{timeframe}.csv"
        df_enhanced.to_csv(output_file, index=False)
        print(f"\n  ✓ Saved {len(enhanced_trades)} enhanced trades to {output_file}")
        
        # Generate performance summary for this timeframe
        perf_summary = generate_performance_summary(df_enhanced, timeframe)
        all_performance_summaries.append(perf_summary)
        
        # Save performance summary
        perf_file = BASE_DIR / f"performance_summary_{timeframe}.csv"
        perf_summary.to_csv(perf_file, index=False)
        print(f"  ✓ Saved performance summary to {perf_file}")
    
    # Generate overall summary
    if all_performance_summaries:
        overall_summary = generate_overall_summary(all_performance_summaries)
        
        # Save overall summaries
        overall_file = BASE_DIR / "performance_summary_all.csv"
        overall_summary['combined'].to_csv(overall_file, index=False)
        print(f"\n✓ Saved overall performance summary to {overall_file}")
        
        best_pnl_file = BASE_DIR / "best_configurations_by_pnl.csv"
        overall_summary['best_pnl'].to_csv(best_pnl_file, index=False)
        print(f"✓ Saved best configurations by P&L to {best_pnl_file}")
        
        best_wr_file = BASE_DIR / "best_configurations_by_winrate.csv"
        overall_summary['best_winrate'].to_csv(best_wr_file, index=False)
        print(f"✓ Saved best configurations by win rate to {best_wr_file}")
        
        best_pf_file = BASE_DIR / "best_configurations_by_profit_factor.csv"
        overall_summary['best_profit_factor'].to_csv(best_pf_file, index=False)
        print(f"✓ Saved best configurations by profit factor to {best_pf_file}")
    
    # Create basic summary report
    print("\n" + "="*60)
    print("BASIC TRADE SUMMARY")
    print("="*60)
    
    summary_data = []
    for timeframe in TIMEFRAMES:
        trades = all_results.get(timeframe, [])
        if trades:
            df = pd.DataFrame(trades)
            long_count = len(df[df['Direction'] == 'LONG'])
            short_count = len(df[df['Direction'] == 'SHORT'])
            
            summary_data.append({
                'Timeframe': timeframe,
                'Total_Trades': len(trades),
                'Long_Trades': long_count,
                'Short_Trades': short_count
            })
            
            print(f"\n{timeframe} Timeframe:")
            print(f"  Total Trades: {len(trades)}")
            print(f"  Long Trades:  {long_count}")
            print(f"  Short Trades: {short_count}")
        else:
            summary_data.append({
                'Timeframe': timeframe,
                'Total_Trades': 0,
                'Long_Trades': 0,
                'Short_Trades': 0
            })
            print(f"\n{timeframe} Timeframe:")
            print(f"  No trades found")
    
    # Save basic summary
    if summary_data:
        df_summary = pd.DataFrame(summary_data)
        summary_file = BASE_DIR / "trades_summary.csv"
        df_summary.to_csv(summary_file, index=False)
        print(f"\n✓ Basic summary saved to {summary_file}")
    
    print("\n" + "="*60)
    print("BACKTESTING COMPLETE!")
    print("="*60)
    print("\n📁 OUTPUT FILES GENERATED:")
    print("  - trades_enhanced_[timeframe].csv : Enhanced trades with all SL/TP levels")
    print("  - performance_summary_[timeframe].csv : Performance by SL/RR combination")
    print("  - performance_summary_all.csv : Combined performance summary")
    print("  - best_configurations_by_*.csv : Top 10 configurations by different metrics")
    print("  - trades_summary.csv : Basic trade counts")
    print("="*60)


if __name__ == "__main__":
    main()

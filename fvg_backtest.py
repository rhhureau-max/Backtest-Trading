#!/usr/bin/env python3
"""
Fair Value Gap (FVG) Breakout Backtesting Script

This script backtests a trading strategy based on FVG breakouts.

Strategy:
- Bearish FVG Breakout (Long Entry): When price closes above the middle candle's low
- Bullish FVG Breakout (Short Entry): When price closes below the middle candle's high

Take Profit levels are tested at 1x, 1.5x, 2x, 2.5x, 3x, and 3.5x risk.
"""

import os
import pandas as pd
from datetime import time


# Configuration
DATA_DIR = os.path.dirname(os.path.abspath(__file__))
YEARS = list(range(2018, 2026))
TIME_START = time(8, 30, 0)
TIME_END = time(10, 0, 0)
TP_LEVELS = [1, 1.5, 2, 2.5, 3, 3.5]


def load_csv_file(year):
    """Load a 15-minute CSV file for a given year."""
    filepath = os.path.join(DATA_DIR, f"{year} 15m.csv")
    
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return None
    
    df = pd.read_csv(
        filepath, 
        delimiter=';',
        names=['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume'],
        skiprows=1
    )
    
    # Convert Date and Time columns
    df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%d/%m/%Y %H:%M:%S')
    df['TimeOnly'] = pd.to_datetime(df['Time'], format='%H:%M:%S').dt.time
    
    # Convert price columns to float
    for col in ['Open', 'High', 'Low', 'Close']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    return df


def filter_time_window(df, start_time, end_time):
    """Filter dataframe to only include rows within the time window (inclusive)."""
    mask = (df['TimeOnly'] >= start_time) & (df['TimeOnly'] <= end_time)
    return df[mask].copy()


def detect_fvg_and_backtest(df_fvg_window, df_full_day):
    """
    Detect FVGs in the time window and backtest breakout trades.
    
    Returns a list of trade dictionaries.
    """
    trades = []
    
    # Group by date to analyze each day separately
    df_fvg_window['DateOnly'] = df_fvg_window['DateTime'].dt.date
    df_full_day['DateOnly'] = df_full_day['DateTime'].dt.date
    
    for date, day_fvg_df in df_fvg_window.groupby('DateOnly'):
        day_fvg_df = day_fvg_df.sort_values('DateTime').reset_index(drop=True)
        
        # Get full day data for checking breakouts
        day_full_df = df_full_day[df_full_day['DateOnly'] == date].sort_values('DateTime').reset_index(drop=True)
        
        # Need at least 3 candles to detect FVG
        if len(day_fvg_df) < 3:
            continue
        
        for i in range(len(day_fvg_df) - 2):
            candle_n = day_fvg_df.iloc[i]
            candle_n1 = day_fvg_df.iloc[i + 1]  # Middle candle
            candle_n2 = day_fvg_df.iloc[i + 2]
            
            # Bullish FVG: High of candle N < Low of candle N+2 (gap up)
            # Short Entry: A candle closes BELOW the high of candle N+1 (middle candle)
            if candle_n['High'] < candle_n2['Low']:
                fvg_type = 'Bullish'
                entry_trigger = candle_n1['High']  # Break level
                stop_loss = candle_n2['Low']  # SL above the gap (top of gap)
                
                # Find candles after the FVG pattern
                fvg_end_time = candle_n2['DateTime']
                subsequent_candles = day_full_df[day_full_df['DateTime'] > fvg_end_time]
                
                for _, candle in subsequent_candles.iterrows():
                    # Entry Signal: Candle closes BELOW the high of middle candle
                    if candle['Close'] < entry_trigger:
                        entry_price = candle['Close']
                        risk = stop_loss - entry_price
                        
                        # Skip this FVG if risk is invalid (entry at or above SL)
                        if risk <= 0:
                            break
                        
                        # Calculate TP levels for short trade
                        tp_results = {}
                        for tp_level in TP_LEVELS:
                            tp_price = entry_price - tp_level * risk
                            tp_results[tp_level] = {'hit': False, 'price': tp_price}
                        
                        # Check subsequent candles for TP/SL hits
                        entry_time = candle['DateTime']
                        future_candles = day_full_df[day_full_df['DateTime'] > entry_time]
                        
                        sl_hit = False
                        for _, future_candle in future_candles.iterrows():
                            # Check SL first (price goes above SL for short)
                            if future_candle['High'] >= stop_loss:
                                sl_hit = True
                                break
                            
                            # Check each TP level (price goes below TP for short)
                            for tp_level in TP_LEVELS:
                                if not tp_results[tp_level]['hit']:
                                    if future_candle['Low'] <= tp_results[tp_level]['price']:
                                        tp_results[tp_level]['hit'] = True
                        
                        # Build trade record with TP results
                        # Keys: TP1, TP1.5, TP2, TP2.5, TP3, TP3.5 (based on TP_LEVELS)
                        trades.append({
                            'Date': date,
                            'FVG_Type': fvg_type,
                            'Trade_Type': 'Short',
                            'Entry_Time': candle['Time'],
                            'Entry_Price': entry_price,
                            'Stop_Loss': stop_loss,
                            'Risk': risk,
                            'SL_Hit': sl_hit,
                            **{f'TP{tp}': tp_results[tp]['hit'] for tp in TP_LEVELS}
                        })
                        break
            
            # Bearish FVG: Low of candle N > High of candle N+2 (gap down)
            # Long Entry: A candle closes ABOVE the low of candle N+1 (middle candle)
            if candle_n['Low'] > candle_n2['High']:
                fvg_type = 'Bearish'
                entry_trigger = candle_n1['Low']  # Break level
                stop_loss = candle_n2['High'] - 0.5  # SL at bottom of gap with 0.5 point buffer below
                
                # Find candles after the FVG pattern
                fvg_end_time = candle_n2['DateTime']
                subsequent_candles = day_full_df[day_full_df['DateTime'] > fvg_end_time]
                
                for _, candle in subsequent_candles.iterrows():
                    # Entry Signal: Candle closes ABOVE the low of middle candle
                    if candle['Close'] > entry_trigger:
                        entry_price = candle['Close']
                        risk = entry_price - stop_loss
                        
                        # Skip this FVG if risk is invalid (entry at or below SL)
                        if risk <= 0:
                            break
                        
                        # Calculate TP levels for long trade
                        tp_results = {}
                        for tp_level in TP_LEVELS:
                            tp_price = entry_price + tp_level * risk
                            tp_results[tp_level] = {'hit': False, 'price': tp_price}
                        
                        # Check subsequent candles for TP/SL hits
                        entry_time = candle['DateTime']
                        future_candles = day_full_df[day_full_df['DateTime'] > entry_time]
                        
                        sl_hit = False
                        for _, future_candle in future_candles.iterrows():
                            # Check SL first (price goes below SL for long)
                            if future_candle['Low'] <= stop_loss:
                                sl_hit = True
                                break
                            
                            # Check each TP level (price goes above TP for long)
                            for tp_level in TP_LEVELS:
                                if not tp_results[tp_level]['hit']:
                                    if future_candle['High'] >= tp_results[tp_level]['price']:
                                        tp_results[tp_level]['hit'] = True
                        
                        # Build trade record with TP results
                        # Keys: TP1, TP1.5, TP2, TP2.5, TP3, TP3.5 (based on TP_LEVELS)
                        trades.append({
                            'Date': date,
                            'FVG_Type': fvg_type,
                            'Trade_Type': 'Long',
                            'Entry_Time': candle['Time'],
                            'Entry_Price': entry_price,
                            'Stop_Loss': stop_loss,
                            'Risk': risk,
                            'SL_Hit': sl_hit,
                            **{f'TP{tp}': tp_results[tp]['hit'] for tp in TP_LEVELS}
                        })
                        break
    
    return trades


def calculate_statistics(trades):
    """Calculate win rates for each TP level."""
    if not trades:
        return {}
    
    stats = {
        'total_trades': len(trades),
        'long_trades': sum(1 for t in trades if t['Trade_Type'] == 'Long'),
        'short_trades': sum(1 for t in trades if t['Trade_Type'] == 'Short'),
    }
    
    # Overall TP win rates
    for tp_level in TP_LEVELS:
        tp_col = f'TP{tp_level}'
        hits = sum(1 for t in trades if t[tp_col])
        stats[f'{tp_col}_win_rate'] = hits / len(trades) * 100
        stats[f'{tp_col}_hits'] = hits
    
    # Long trades TP win rates
    long_trades = [t for t in trades if t['Trade_Type'] == 'Long']
    if long_trades:
        for tp_level in TP_LEVELS:
            tp_col = f'TP{tp_level}'
            hits = sum(1 for t in long_trades if t[tp_col])
            stats[f'Long_{tp_col}_win_rate'] = hits / len(long_trades) * 100
            stats[f'Long_{tp_col}_hits'] = hits
    
    # Short trades TP win rates
    short_trades = [t for t in trades if t['Trade_Type'] == 'Short']
    if short_trades:
        for tp_level in TP_LEVELS:
            tp_col = f'TP{tp_level}'
            hits = sum(1 for t in short_trades if t[tp_col])
            stats[f'Short_{tp_col}_win_rate'] = hits / len(short_trades) * 100
            stats[f'Short_{tp_col}_hits'] = hits
    
    return stats


def main():
    print("=" * 80)
    print("FVG BREAKOUT BACKTESTING")
    print("=" * 80)
    print()
    print("Strategy:")
    print("  - Bearish FVG Breakout → Long Entry (Close above middle candle's low)")
    print("  - Bullish FVG Breakout → Short Entry (Close below middle candle's high)")
    print("  - FVG Detection Window: 8:30 - 10:00")
    print("  - Years: 2018 - 2025")
    print()
    print("=" * 80)
    print()
    
    all_trades = []
    yearly_stats = {}
    
    for year in YEARS:
        print(f"Processing {year}...")
        
        # Load data
        df = load_csv_file(year)
        if df is None:
            continue
        
        # Filter to FVG detection time window
        df_fvg_window = filter_time_window(df, TIME_START, TIME_END)
        
        # Detect FVGs and backtest trades
        trades = detect_fvg_and_backtest(df_fvg_window, df)
        
        if trades:
            stats = calculate_statistics(trades)
            yearly_stats[year] = stats
            all_trades.extend(trades)
            
            print(f"  Trades found: {len(trades)} (Long: {stats['long_trades']}, Short: {stats['short_trades']})")
        else:
            print(f"  No trades found")
    
    print()
    
    if not all_trades:
        print("No trades found in the dataset.")
        return
    
    # Calculate overall statistics
    overall_stats = calculate_statistics(all_trades)
    
    # Print results
    print("=" * 80)
    print("BACKTEST RESULTS SUMMARY")
    print("=" * 80)
    print()
    print(f"Total Trades: {overall_stats['total_trades']}")
    print(f"  - Long Trades (Bearish FVG Breakout): {overall_stats['long_trades']}")
    print(f"  - Short Trades (Bullish FVG Breakout): {overall_stats['short_trades']}")
    print()
    
    # Overall TP Win Rates
    print("=" * 80)
    print("OVERALL WIN RATES BY TAKE PROFIT LEVEL")
    print("=" * 80)
    print()
    print(f"{'TP Level':<15} {'Hits':<15} {'Win Rate':<15}")
    print("-" * 45)
    for tp_level in TP_LEVELS:
        tp_col = f'TP{tp_level}'
        hits = overall_stats[f'{tp_col}_hits']
        win_rate = overall_stats[f'{tp_col}_win_rate']
        print(f"TP {tp_level:<11} {hits:<15} {win_rate:.2f}%")
    print()
    
    # Long Trades Win Rates
    print("=" * 80)
    print("LONG TRADES (BEARISH FVG BREAKOUT) WIN RATES")
    print("=" * 80)
    print()
    if overall_stats['long_trades'] > 0:
        print(f"Total Long Trades: {overall_stats['long_trades']}")
        print()
        print(f"{'TP Level':<15} {'Hits':<15} {'Win Rate':<15}")
        print("-" * 45)
        for tp_level in TP_LEVELS:
            tp_col = f'TP{tp_level}'
            hits = overall_stats.get(f'Long_{tp_col}_hits', 0)
            win_rate = overall_stats.get(f'Long_{tp_col}_win_rate', 0)
            print(f"TP {tp_level:<11} {hits:<15} {win_rate:.2f}%")
    else:
        print("No long trades found.")
    print()
    
    # Short Trades Win Rates
    print("=" * 80)
    print("SHORT TRADES (BULLISH FVG BREAKOUT) WIN RATES")
    print("=" * 80)
    print()
    if overall_stats['short_trades'] > 0:
        print(f"Total Short Trades: {overall_stats['short_trades']}")
        print()
        print(f"{'TP Level':<15} {'Hits':<15} {'Win Rate':<15}")
        print("-" * 45)
        for tp_level in TP_LEVELS:
            tp_col = f'TP{tp_level}'
            hits = overall_stats.get(f'Short_{tp_col}_hits', 0)
            win_rate = overall_stats.get(f'Short_{tp_col}_win_rate', 0)
            print(f"TP {tp_level:<11} {hits:<15} {win_rate:.2f}%")
    else:
        print("No short trades found.")
    print()
    
    # Yearly Breakdown
    print("=" * 80)
    print("YEARLY BREAKDOWN")
    print("=" * 80)
    print()
    print(f"{'Year':<8} {'Total':<8} {'Long':<8} {'Short':<8} {'TP1%':<10} {'TP1.5%':<10} {'TP2%':<10} {'TP2.5%':<10} {'TP3%':<10} {'TP3.5%':<10}")
    print("-" * 100)
    for year in YEARS:
        if year in yearly_stats:
            stats = yearly_stats[year]
            tp1 = stats.get('TP1_win_rate', 0)
            tp15 = stats.get('TP1.5_win_rate', 0)
            tp2 = stats.get('TP2_win_rate', 0)
            tp25 = stats.get('TP2.5_win_rate', 0)
            tp3 = stats.get('TP3_win_rate', 0)
            tp35 = stats.get('TP3.5_win_rate', 0)
            print(f"{year:<8} {stats['total_trades']:<8} {stats['long_trades']:<8} {stats['short_trades']:<8} "
                  f"{tp1:>6.2f}%   {tp15:>6.2f}%   {tp2:>6.2f}%   {tp25:>6.2f}%   {tp3:>6.2f}%   {tp35:>6.2f}%")
    print()
    
    # Print sample trades
    print("=" * 80)
    print("SAMPLE TRADES (First 10)")
    print("=" * 80)
    print()
    for i, trade in enumerate(all_trades[:10]):
        print(f"{i+1}. {trade['Trade_Type']} trade on {trade['Date']} at {trade['Entry_Time']}")
        print(f"   FVG Type: {trade['FVG_Type']}")
        print(f"   Entry: {trade['Entry_Price']:.4f}, SL: {trade['Stop_Loss']:.4f}, Risk: {trade['Risk']:.4f}")
        tp_hits = [f"TP{tp}" for tp in TP_LEVELS if trade[f'TP{tp}']]
        if tp_hits:
            print(f"   TP Hits: {', '.join(tp_hits)}")
        else:
            print(f"   TP Hits: None (SL hit: {trade['SL_Hit']})")
        print()
    
    # Save results to CSV
    results_df = pd.DataFrame(all_trades)
    output_path = os.path.join(DATA_DIR, "fvg_backtest_results.csv")
    results_df.to_csv(output_path, index=False)
    print(f"Trade details saved to: {output_path}")
    
    # Save summary statistics
    summary_data = []
    
    # Overall stats
    for tp_level in TP_LEVELS:
        summary_data.append({
            'Category': 'Overall',
            'TP_Level': tp_level,
            'Total_Trades': overall_stats['total_trades'],
            'Hits': overall_stats[f'TP{tp_level}_hits'],
            'Win_Rate': overall_stats[f'TP{tp_level}_win_rate']
        })
    
    # Long trades stats
    if overall_stats['long_trades'] > 0:
        for tp_level in TP_LEVELS:
            summary_data.append({
                'Category': 'Long (Bearish FVG)',
                'TP_Level': tp_level,
                'Total_Trades': overall_stats['long_trades'],
                'Hits': overall_stats.get(f'Long_TP{tp_level}_hits', 0),
                'Win_Rate': overall_stats.get(f'Long_TP{tp_level}_win_rate', 0)
            })
    
    # Short trades stats
    if overall_stats['short_trades'] > 0:
        for tp_level in TP_LEVELS:
            summary_data.append({
                'Category': 'Short (Bullish FVG)',
                'TP_Level': tp_level,
                'Total_Trades': overall_stats['short_trades'],
                'Hits': overall_stats.get(f'Short_TP{tp_level}_hits', 0),
                'Win_Rate': overall_stats.get(f'Short_TP{tp_level}_win_rate', 0)
            })
    
    summary_df = pd.DataFrame(summary_data)
    summary_path = os.path.join(DATA_DIR, "fvg_backtest_summary.csv")
    summary_df.to_csv(summary_path, index=False)
    print(f"Summary statistics saved to: {summary_path}")
    
    print()
    print("=" * 80)
    print("BACKTESTING COMPLETE")
    print("=" * 80)
    
    return all_trades, overall_stats


if __name__ == "__main__":
    trades, stats = main()

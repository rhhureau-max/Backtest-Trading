"""
FVG Breakout Strategy Backtest Analysis Script
Analyzes the probability of hitting various TP levels after an FVG breakout.

Strategy:
For Bearish FVG breakout (bullish trade):
1. A bearish FVG exists (gap down between candle N-2 low and candle N high)
2. The FVG is broken when a candle CLOSES ABOVE the LOW of candle N (the candle that created the FVG)
3. Entry: At the CLOSE of the breakout candle
4. Stop Loss (SL): Below the FVG zone (at the HIGH of candle N, which is the bottom of the bearish FVG)
5. Risk (R) = Entry price - SL price
6. Check if price reaches TP levels before hitting SL

For Bullish FVG breakout (bearish trade):
1. A bullish FVG exists (gap up between candle N-2 high and candle N low)
2. The FVG is broken when a candle CLOSES BELOW the HIGH of candle N (the candle that created the FVG)
3. Entry: At the CLOSE of the breakout candle
4. Stop Loss (SL): Above the FVG zone (at the LOW of candle N, which is the top of the bullish FVG)
5. Risk (R) = SL price - Entry price
6. Check if price reaches TP levels before hitting SL

Constraints:
- Only analyze FVGs created between 8:30 and 10:00
- TP/SL tracking continues until 16:00
"""

import pandas as pd
from datetime import datetime, time
import os
import sys
import zipfile


def load_data(data_dir):
    """Load all 1-minute data files from 2018 to 2025"""
    all_data = []
    
    years = range(2018, 2026)  # 2018 to 2025
    
    for year in years:
        filepath = os.path.join(data_dir, f"{year} 1m.csv")
        zip_filepath = os.path.join(data_dir, f"{year} 1m.csv.zip")
        
        if os.path.exists(filepath):
            print(f"Loading {filepath}...")
            df = pd.read_csv(filepath, sep=';', skiprows=1, header=None,
                           names=['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume'])
            df['Year'] = year
            all_data.append(df)
            print(f"  Loaded {len(df):,} candles for {year}")
        elif os.path.exists(zip_filepath):
            print(f"Loading {zip_filepath}...")
            with zipfile.ZipFile(zip_filepath, 'r') as z:
                # Find the csv file inside the zip
                csv_files = [f for f in z.namelist() if f.endswith('.csv') and not f.startswith('__MACOSX')]
                if csv_files:
                    with z.open(csv_files[0]) as csv_file:
                        df = pd.read_csv(csv_file, sep=';', skiprows=1, header=None,
                                       names=['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume'])
                        df['Year'] = year
                        all_data.append(df)
                        print(f"  Loaded {len(df):,} candles for {year}")
        else:
            print(f"  Warning: File not found: {filepath}")
    
    if all_data:
        combined = pd.concat(all_data, ignore_index=True)
        print(f"\nTotal candles loaded: {len(combined):,}")
        return combined
    return pd.DataFrame()


def filter_time_range(df, start_time='08:30:00', end_time='10:00:00'):
    """Filter data to only include candles between the specified time range"""
    
    # Convert time strings to time objects for proper comparison
    start = datetime.strptime(start_time, '%H:%M:%S').time()
    end = datetime.strptime(end_time, '%H:%M:%S').time()
    
    # Parse Time column to time objects
    df['TimeObj'] = df['Time'].apply(lambda x: datetime.strptime(x, '%H:%M:%S').time())
    
    # Filter by time range
    mask = (df['TimeObj'] >= start) & (df['TimeObj'] <= end)
    filtered = df[mask].copy()
    filtered = filtered.drop(columns=['TimeObj'])
    
    print(f"Candles between {start_time} and {end_time}: {len(filtered):,}")
    return filtered


def get_full_day_data(df):
    """Get all data for days that have FVGs (for TP/SL tracking)"""
    # Parse Time column
    df['TimeObj'] = df['Time'].apply(lambda x: datetime.strptime(x, '%H:%M:%S').time())
    return df


def analyze_fvg_breakouts(df, full_day_df):
    """
    Analyze FVG breakouts and calculate TP hit rates
    
    Returns detailed results for each trade and summary statistics
    """
    
    tp_levels = [1.0, 1.5, 2.0, 2.5, 3.0, 3.5]
    
    # Time constraints
    fvg_start_time = datetime.strptime('08:30:00', '%H:%M:%S').time()
    fvg_end_time = datetime.strptime('10:00:00', '%H:%M:%S').time()
    tracking_end_time = datetime.strptime('16:00:00', '%H:%M:%S').time()
    
    # Results storage
    bullish_trades = []  # Trades from bearish FVG breakouts (bullish direction)
    bearish_trades = []  # Trades from bullish FVG breakouts (bearish direction)
    
    # Sort by Date and Time
    df_sorted = df.sort_values(['Date', 'Time']).reset_index(drop=True)
    
    # Process each day
    for date, group in df_sorted.groupby('Date'):
        group = group.reset_index(drop=True)
        
        if len(group) < 3:
            continue
        
        # Get full day data for this date
        full_day_group = full_day_df[full_day_df['Date'] == date].sort_values('Time').reset_index(drop=True)
        
        # Detect FVGs and look for breakouts
        for i in range(2, len(group)):
            candle_n_minus_2_high = group.loc[i-2, 'High']
            candle_n_minus_2_low = group.loc[i-2, 'Low']
            candle_n_high = group.loc[i, 'High']
            candle_n_low = group.loc[i, 'Low']
            fvg_time_str = group.loc[i, 'Time']
            fvg_time = datetime.strptime(fvg_time_str, '%H:%M:%S').time()
            
            # Skip if FVG is created outside the time window
            if fvg_time < fvg_start_time or fvg_time > fvg_end_time:
                continue
            
            # Check for Bearish FVG (gap down - for bullish trade)
            if candle_n_minus_2_low > candle_n_high:
                # Look for breakout: candle CLOSES ABOVE candle N's LOW
                # Search in full day data after the FVG
                fvg_idx_in_full = None
                for idx in range(len(full_day_group)):
                    if (full_day_group.loc[idx, 'Time'] == fvg_time_str):
                        fvg_idx_in_full = idx
                        break
                
                if fvg_idx_in_full is None:
                    continue
                
                # Search for breakout
                for j in range(fvg_idx_in_full + 1, len(full_day_group)):
                    check_time = datetime.strptime(full_day_group.loc[j, 'Time'], '%H:%M:%S').time()
                    if check_time > tracking_end_time:
                        break
                    
                    candle_close = full_day_group.loc[j, 'Close']
                    
                    # Breakout: Close above candle N's LOW
                    if candle_close > candle_n_low:
                        # We have a breakout! Now track for TP/SL
                        entry_price = candle_close
                        sl_price = candle_n_high  # Bottom of bearish FVG
                        risk = entry_price - sl_price
                        
                        if risk <= 0:
                            break  # Invalid trade setup
                        
                        # Track which TP levels are hit before SL
                        tp_hits = {level: False for level in tp_levels}
                        hit_sl = False
                        
                        # Check subsequent candles
                        for k in range(j + 1, len(full_day_group)):
                            track_time = datetime.strptime(full_day_group.loc[k, 'Time'], '%H:%M:%S').time()
                            if track_time > tracking_end_time:
                                break
                            
                            candle_high = full_day_group.loc[k, 'High']
                            candle_low = full_day_group.loc[k, 'Low']
                            
                            # Check if SL is hit (price goes to or below SL)
                            if candle_low <= sl_price:
                                hit_sl = True
                                break
                            
                            # Check each TP level
                            for level in tp_levels:
                                if not tp_hits[level]:
                                    tp_price = entry_price + level * risk
                                    if candle_high >= tp_price:
                                        tp_hits[level] = True
                        
                        # Record the trade
                        trade = {
                            'Date': date,
                            'FVG_Time': fvg_time_str,
                            'Breakout_Time': full_day_group.loc[j, 'Time'],
                            'Entry_Price': entry_price,
                            'SL_Price': sl_price,
                            'Risk': risk,
                            'Hit_SL': hit_sl,
                            'Year': date.split('/')[2] if '/' in date else date.split('-')[0]
                        }
                        for level in tp_levels:
                            trade[f'TP_{level}R'] = tp_hits[level] and not hit_sl
                        
                        bullish_trades.append(trade)
                        break  # Only take the first breakout for this FVG
            
            # Check for Bullish FVG (gap up - for bearish trade)
            elif candle_n_minus_2_high < candle_n_low:
                # Look for breakout: candle CLOSES BELOW candle N's HIGH
                fvg_idx_in_full = None
                for idx in range(len(full_day_group)):
                    if (full_day_group.loc[idx, 'Time'] == fvg_time_str):
                        fvg_idx_in_full = idx
                        break
                
                if fvg_idx_in_full is None:
                    continue
                
                # Search for breakout
                for j in range(fvg_idx_in_full + 1, len(full_day_group)):
                    check_time = datetime.strptime(full_day_group.loc[j, 'Time'], '%H:%M:%S').time()
                    if check_time > tracking_end_time:
                        break
                    
                    candle_close = full_day_group.loc[j, 'Close']
                    
                    # Breakout: Close below candle N's HIGH
                    if candle_close < candle_n_high:
                        # We have a breakout! Now track for TP/SL
                        entry_price = candle_close
                        sl_price = candle_n_low  # Top of bullish FVG
                        risk = sl_price - entry_price
                        
                        if risk <= 0:
                            break  # Invalid trade setup
                        
                        # Track which TP levels are hit before SL
                        tp_hits = {level: False for level in tp_levels}
                        hit_sl = False
                        
                        # Check subsequent candles
                        for k in range(j + 1, len(full_day_group)):
                            track_time = datetime.strptime(full_day_group.loc[k, 'Time'], '%H:%M:%S').time()
                            if track_time > tracking_end_time:
                                break
                            
                            candle_high = full_day_group.loc[k, 'High']
                            candle_low = full_day_group.loc[k, 'Low']
                            
                            # Check if SL is hit (price goes to or above SL)
                            if candle_high >= sl_price:
                                hit_sl = True
                                break
                            
                            # Check each TP level (for short trades, TP is below entry)
                            for level in tp_levels:
                                if not tp_hits[level]:
                                    tp_price = entry_price - level * risk
                                    if candle_low <= tp_price:
                                        tp_hits[level] = True
                        
                        # Record the trade
                        trade = {
                            'Date': date,
                            'FVG_Time': fvg_time_str,
                            'Breakout_Time': full_day_group.loc[j, 'Time'],
                            'Entry_Price': entry_price,
                            'SL_Price': sl_price,
                            'Risk': risk,
                            'Hit_SL': hit_sl,
                            'Year': date.split('/')[2] if '/' in date else date.split('-')[0]
                        }
                        for level in tp_levels:
                            trade[f'TP_{level}R'] = tp_hits[level] and not hit_sl
                        
                        bearish_trades.append(trade)
                        break  # Only take the first breakout for this FVG
    
    return bullish_trades, bearish_trades, tp_levels


def calculate_statistics(trades, tp_levels, trade_type):
    """Calculate win rates for each TP level"""
    if not trades:
        return None
    
    df = pd.DataFrame(trades)
    total_trades = len(df)
    
    stats = {
        'Trade_Type': trade_type,
        'Total_Trades': total_trades,
    }
    
    for level in tp_levels:
        col = f'TP_{level}R'
        wins = df[col].sum()
        win_rate = (wins / total_trades * 100) if total_trades > 0 else 0
        stats[f'TP_{level}R_Wins'] = wins
        stats[f'TP_{level}R_Rate'] = win_rate
    
    return stats


def calculate_yearly_statistics(trades, tp_levels):
    """Calculate yearly breakdown of win rates"""
    if not trades:
        return None
    
    df = pd.DataFrame(trades)
    yearly_stats = []
    
    for year in sorted(df['Year'].unique()):
        year_df = df[df['Year'] == year]
        total = len(year_df)
        
        year_stat = {
            'Year': year,
            'Total_Trades': total,
        }
        
        for level in tp_levels:
            col = f'TP_{level}R'
            wins = year_df[col].sum()
            win_rate = (wins / total * 100) if total > 0 else 0
            year_stat[f'TP_{level}R_Wins'] = wins
            year_stat[f'TP_{level}R_Rate'] = win_rate
        
        yearly_stats.append(year_stat)
    
    return yearly_stats


def main():
    # Get the directory where the script is located, or use command line argument
    if len(sys.argv) > 1:
        data_dir = sys.argv[1]
    else:
        data_dir = os.path.dirname(os.path.abspath(__file__))
    
    print("=" * 80)
    print("FVG Breakout Strategy Backtest Analysis")
    print("=" * 80)
    print("\nStrategy Parameters:")
    print("  - FVG Detection Window: 08:30 - 10:00 (New York Time)")
    print("  - TP/SL Tracking: Until 16:00")
    print("  - Data Range: 2018 - 2025")
    print("  - TP Levels: 1R, 1.5R, 2R, 2.5R, 3R, 3.5R")
    print("=" * 80)
    print()
    
    # Load all data
    print("Step 1: Loading data...")
    df = load_data(data_dir)
    
    if df.empty:
        print("No data loaded. Exiting.")
        return
    
    # Prepare full day data for TP/SL tracking
    print("\nStep 2: Preparing full day data for TP/SL tracking...")
    full_day_df = get_full_day_data(df.copy())
    
    # Filter FVG detection to 8:30-10:00
    print("\nStep 3: Filtering FVG detection window (08:30 - 10:00)...")
    df_filtered = filter_time_range(df)
    
    if df_filtered.empty:
        print("No data in the specified time range. Exiting.")
        return
    
    # Analyze FVG breakouts
    print("\nStep 4: Analyzing FVG breakouts and calculating TP hit rates...")
    print("(This may take a few minutes...)")
    bullish_trades, bearish_trades, tp_levels = analyze_fvg_breakouts(df_filtered, full_day_df)
    
    # Calculate statistics
    print("\n" + "=" * 80)
    print("RESULTS SUMMARY")
    print("=" * 80)
    
    # Bullish trades (from bearish FVG breakouts)
    print("\n" + "-" * 60)
    print("BEARISH FVG BREAKOUTS (Bullish Trades)")
    print("-" * 60)
    bullish_stats = calculate_statistics(bullish_trades, tp_levels, "Bullish")
    if bullish_stats:
        print(f"Total Trades: {bullish_stats['Total_Trades']}")
        print("\nTP Level Win Rates:")
        for level in tp_levels:
            wins = bullish_stats[f'TP_{level}R_Wins']
            rate = bullish_stats[f'TP_{level}R_Rate']
            print(f"  TP {level}R: {wins} wins ({rate:.2f}%)")
    else:
        print("No bullish trades found.")
    
    # Bearish trades (from bullish FVG breakouts)
    print("\n" + "-" * 60)
    print("BULLISH FVG BREAKOUTS (Bearish Trades)")
    print("-" * 60)
    bearish_stats = calculate_statistics(bearish_trades, tp_levels, "Bearish")
    if bearish_stats:
        print(f"Total Trades: {bearish_stats['Total_Trades']}")
        print("\nTP Level Win Rates:")
        for level in tp_levels:
            wins = bearish_stats[f'TP_{level}R_Wins']
            rate = bearish_stats[f'TP_{level}R_Rate']
            print(f"  TP {level}R: {wins} wins ({rate:.2f}%)")
    else:
        print("No bearish trades found.")
    
    # Yearly breakdown
    print("\n" + "=" * 80)
    print("YEARLY BREAKDOWN")
    print("=" * 80)
    
    print("\nBearish FVG Breakouts (Bullish Trades) - Yearly:")
    bullish_yearly = calculate_yearly_statistics(bullish_trades, tp_levels)
    if bullish_yearly:
        yearly_df = pd.DataFrame(bullish_yearly)
        # Create a summary with just win rates
        yearly_summary = yearly_df[['Year', 'Total_Trades'] + [f'TP_{level}R_Rate' for level in tp_levels]]
        yearly_summary.columns = ['Year', 'Trades'] + [f'{level}R (%)' for level in tp_levels]
        print(yearly_summary.to_string(index=False))
    
    print("\nBullish FVG Breakouts (Bearish Trades) - Yearly:")
    bearish_yearly = calculate_yearly_statistics(bearish_trades, tp_levels)
    if bearish_yearly:
        yearly_df = pd.DataFrame(bearish_yearly)
        yearly_summary = yearly_df[['Year', 'Total_Trades'] + [f'TP_{level}R_Rate' for level in tp_levels]]
        yearly_summary.columns = ['Year', 'Trades'] + [f'{level}R (%)' for level in tp_levels]
        print(yearly_summary.to_string(index=False))
    
    # Save detailed results
    output_dir = data_dir
    
    # Save bullish trades
    if bullish_trades:
        bullish_df = pd.DataFrame(bullish_trades)
        bullish_file = os.path.join(output_dir, "fvg_breakout_bullish_trades.csv")
        bullish_df.to_csv(bullish_file, index=False)
        print(f"\nBullish trades saved to: {bullish_file}")
    
    # Save bearish trades
    if bearish_trades:
        bearish_df = pd.DataFrame(bearish_trades)
        bearish_file = os.path.join(output_dir, "fvg_breakout_bearish_trades.csv")
        bearish_df.to_csv(bearish_file, index=False)
        print(f"Bearish trades saved to: {bearish_file}")
    
    # Save summary
    summary_file = os.path.join(output_dir, "fvg_breakout_summary.txt")
    with open(summary_file, 'w') as f:
        f.write("=" * 80 + "\n")
        f.write("FVG Breakout Strategy Backtest Analysis Summary\n")
        f.write("=" * 80 + "\n\n")
        f.write("Strategy Parameters:\n")
        f.write("  - FVG Detection Window: 08:30 - 10:00 (New York Time)\n")
        f.write("  - TP/SL Tracking: Until 16:00\n")
        f.write("  - Data Range: 2018 - 2025\n")
        f.write("  - TP Levels: 1R, 1.5R, 2R, 2.5R, 3R, 3.5R\n\n")
        
        f.write("-" * 60 + "\n")
        f.write("BEARISH FVG BREAKOUTS (Bullish Trades)\n")
        f.write("-" * 60 + "\n")
        if bullish_stats:
            f.write(f"Total Trades: {bullish_stats['Total_Trades']}\n\n")
            f.write("TP Level Win Rates:\n")
            for level in tp_levels:
                wins = bullish_stats[f'TP_{level}R_Wins']
                rate = bullish_stats[f'TP_{level}R_Rate']
                f.write(f"  TP {level}R: {wins} wins ({rate:.2f}%)\n")
        else:
            f.write("No bullish trades found.\n")
        
        f.write("\n" + "-" * 60 + "\n")
        f.write("BULLISH FVG BREAKOUTS (Bearish Trades)\n")
        f.write("-" * 60 + "\n")
        if bearish_stats:
            f.write(f"Total Trades: {bearish_stats['Total_Trades']}\n\n")
            f.write("TP Level Win Rates:\n")
            for level in tp_levels:
                wins = bearish_stats[f'TP_{level}R_Wins']
                rate = bearish_stats[f'TP_{level}R_Rate']
                f.write(f"  TP {level}R: {wins} wins ({rate:.2f}%)\n")
        else:
            f.write("No bearish trades found.\n")
        
        f.write("\n" + "=" * 80 + "\n")
        f.write("YEARLY BREAKDOWN\n")
        f.write("=" * 80 + "\n\n")
        
        f.write("Bearish FVG Breakouts (Bullish Trades) - Yearly:\n")
        if bullish_yearly:
            yearly_df = pd.DataFrame(bullish_yearly)
            yearly_summary = yearly_df[['Year', 'Total_Trades'] + [f'TP_{level}R_Rate' for level in tp_levels]]
            yearly_summary.columns = ['Year', 'Trades'] + [f'{level}R (%)' for level in tp_levels]
            f.write(yearly_summary.to_string(index=False))
            f.write("\n")
        
        f.write("\nBullish FVG Breakouts (Bearish Trades) - Yearly:\n")
        if bearish_yearly:
            yearly_df = pd.DataFrame(bearish_yearly)
            yearly_summary = yearly_df[['Year', 'Total_Trades'] + [f'TP_{level}R_Rate' for level in tp_levels]]
            yearly_summary.columns = ['Year', 'Trades'] + [f'{level}R (%)' for level in tp_levels]
            f.write(yearly_summary.to_string(index=False))
            f.write("\n")
    
    print(f"Summary saved to: {summary_file}")
    
    print("\n" + "=" * 80)
    print("Analysis Complete!")
    print("=" * 80)


if __name__ == "__main__":
    main()

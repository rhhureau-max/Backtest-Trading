"""
Impulsive 8:30 Candle Analysis Script
Analyzes 1-minute candlestick data from 2018 to 2025 to find impulsive 8:30 AM candles

Strategy:
1. Find the 8:30 AM candle for each trading day (first candle of NY session)
2. Check if it's an "impulsive" candle: |High - Low| > 8 points
3. If bullish impulse (Close > Open): Enter LONG at Close
4. If bearish impulse (Close < Open): Enter SHORT at Close

Stop Loss Placements Tested:
- 50% retracement: SL at 50% of candle range from entry
- 100% retracement: SL at opposite extreme of the candle

Take Profit Levels: 1R, 1.5R, 2R, 2.5R, 3R, 3.5R, 4R, 4.5R, 5R
"""

import pandas as pd
from datetime import datetime, time, timedelta
import os
import sys


def load_data(data_dir):
    """Load all 1-minute data files from 2018 to 2025"""
    all_data = []
    
    years = range(2018, 2026)  # 2018 to 2025
    
    for year in years:
        filepath = os.path.join(data_dir, f"{year} 1m.csv")
        
        if os.path.exists(filepath):
            print(f"Loading {filepath}...")
            df = pd.read_csv(filepath, sep=';', skiprows=1, header=None,
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


def find_830_candles(df):
    """Find all 8:30 AM candles"""
    # Filter for 8:30:00 candles only
    mask = df['Time'] == '08:30:00'
    candles_830 = df[mask].copy()
    print(f"Found {len(candles_830):,} 8:30 AM candles")
    return candles_830


def identify_impulsive_candles(candles_830, min_points=8):
    """Identify impulsive candles where |High - Low| > min_points"""
    candles_830 = candles_830.copy()
    candles_830['Range'] = candles_830['High'] - candles_830['Low']
    candles_830['Is_Impulsive'] = candles_830['Range'] > min_points
    
    # Determine direction
    candles_830['Is_Bullish'] = candles_830['Close'] > candles_830['Open']
    candles_830['Direction'] = candles_830.apply(
        lambda x: 'LONG' if x['Is_Bullish'] else 'SHORT' if x['Close'] < x['Open'] else 'NEUTRAL',
        axis=1
    )
    
    impulsive = candles_830[candles_830['Is_Impulsive'] & (candles_830['Direction'] != 'NEUTRAL')].copy()
    
    print(f"Found {len(impulsive):,} impulsive 8:30 candles (Range > {min_points} points)")
    print(f"  - Bullish: {len(impulsive[impulsive['Direction'] == 'LONG']):,}")
    print(f"  - Bearish: {len(impulsive[impulsive['Direction'] == 'SHORT']):,}")
    
    return impulsive


def get_subsequent_candles(df, date, start_time='08:31:00', end_time='23:59:00'):
    """Get all candles after the 8:30 candle for the same day"""
    # Filter by date
    day_data = df[df['Date'] == date].copy()
    
    if day_data.empty:
        return pd.DataFrame()
    
    # Filter by time range
    start = datetime.strptime(start_time, '%H:%M:%S').time()
    end = datetime.strptime(end_time, '%H:%M:%S').time()
    
    day_data['TimeObj'] = day_data['Time'].apply(lambda x: datetime.strptime(x, '%H:%M:%S').time())
    mask = (day_data['TimeObj'] >= start) & (day_data['TimeObj'] <= end)
    
    filtered = day_data[mask].copy()
    filtered = filtered.drop(columns=['TimeObj'])
    filtered = filtered.sort_values('Time').reset_index(drop=True)
    
    return filtered


def analyze_trade(entry_price, sl_price, direction, subsequent_candles, tp_levels):
    """
    Analyze a trade and determine which TP levels are hit before SL
    
    Args:
        entry_price: Entry price at 8:30 candle close
        sl_price: Stop loss price
        direction: 'LONG' or 'SHORT'
        subsequent_candles: DataFrame of subsequent 1-minute candles
        tp_levels: List of R-multiples for TP (e.g., [1, 1.5, 2, ...])
    
    Returns:
        Dictionary with results for each TP level
        
    Note:
        When both SL and TP are within the same candle's range, we use a 
        conservative approach: SL is considered hit first (worst case scenario).
        This avoids optimistic bias in backtesting results and provides more
        realistic risk management expectations. Since we cannot know the 
        intra-candle price path from 1-minute data alone, assuming the worst
        case (losing trade) is a more prudent strategy for backtesting.
    """
    risk = abs(entry_price - sl_price)
    
    # Calculate TP prices
    tp_prices = {}
    for r in tp_levels:
        if direction == 'LONG':
            tp_prices[r] = entry_price + (risk * r)
        else:  # SHORT
            tp_prices[r] = entry_price - (risk * r)
    
    results = {r: {'hit': False, 'candles_to_hit': None} for r in tp_levels}
    sl_hit = False
    
    for idx, candle in subsequent_candles.iterrows():
        if sl_hit:
            break
            
        candle_high = candle['High']
        candle_low = candle['Low']
        
        # Check if SL is hit this candle
        sl_hit_this_candle = False
        if direction == 'LONG':
            if candle_low <= sl_price:
                sl_hit_this_candle = True
        else:  # SHORT
            if candle_high >= sl_price:
                sl_hit_this_candle = True
        
        # Check TPs - apply conservative assumption per docstring
        for r in tp_levels:
            if results[r]['hit']:
                continue
                
            tp_price = tp_prices[r]
            tp_hit_this_candle = False
            
            if direction == 'LONG':
                if candle_high >= tp_price:
                    tp_hit_this_candle = True
            else:  # SHORT
                if candle_low <= tp_price:
                    tp_hit_this_candle = True
            
            # Only count TP as hit if SL was not also hit in this same candle
            if tp_hit_this_candle and not sl_hit_this_candle:
                results[r]['hit'] = True
                results[r]['candles_to_hit'] = idx + 1
        
        # Mark SL as hit after checking TPs (so TPs in prior candles are recorded)
        if sl_hit_this_candle:
            sl_hit = True
            break
    
    return results, sl_hit, risk


def run_analysis(df, impulsive_candles, sl_type='50%'):
    """
    Run analysis for all impulsive candles with specified SL type
    
    Args:
        df: Full DataFrame with all 1-minute candles
        impulsive_candles: DataFrame with impulsive 8:30 candles
        sl_type: '50%' for 50% retracement or '100%' for 100% retracement
    
    Returns:
        DataFrame with detailed trade results
    """
    tp_levels = [1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]
    trades = []
    
    print(f"\nAnalyzing trades with {sl_type} SL retracement...")
    
    for idx, candle in impulsive_candles.iterrows():
        date = candle['Date']
        entry_price = candle['Close']
        high = candle['High']
        low = candle['Low']
        range_size = candle['Range']
        direction = candle['Direction']
        year = candle['Year']
        
        # Calculate SL based on type
        if sl_type == '50%':
            if direction == 'LONG':
                sl_price = entry_price - (range_size * 0.5)
            else:  # SHORT
                sl_price = entry_price + (range_size * 0.5)
        else:  # 100% retracement
            if direction == 'LONG':
                sl_price = low  # SL at candle low
            else:  # SHORT
                sl_price = high  # SL at candle high
        
        # Get subsequent candles
        subsequent = get_subsequent_candles(df, date)
        
        if subsequent.empty:
            continue
        
        # Analyze trade
        results, sl_hit, risk = analyze_trade(entry_price, sl_price, direction, subsequent, tp_levels)
        
        trade_record = {
            'Date': date,
            'Year': year,
            'Time': candle['Time'],
            'Direction': direction,
            'Open': candle['Open'],
            'High': high,
            'Low': low,
            'Close': entry_price,
            'Range': range_size,
            'Entry': entry_price,
            'SL': sl_price,
            'Risk': risk,
            'SL_Hit': sl_hit
        }
        
        # Add TP results
        for r in tp_levels:
            trade_record[f'TP_{r}R_Hit'] = results[r]['hit']
            trade_record[f'TP_{r}R_Candles'] = results[r]['candles_to_hit']
        
        trades.append(trade_record)
    
    trades_df = pd.DataFrame(trades)
    print(f"Analyzed {len(trades_df):,} trades")
    
    return trades_df


def calculate_win_rates(trades_df, tp_levels):
    """Calculate win rates for each TP level"""
    total_trades = len(trades_df)
    
    win_rates = {}
    for r in tp_levels:
        wins = trades_df[f'TP_{r}R_Hit'].sum()
        win_rate = (wins / total_trades * 100) if total_trades > 0 else 0
        win_rates[r] = {
            'wins': wins,
            'total': total_trades,
            'win_rate': win_rate
        }
    
    return win_rates


def calculate_yearly_breakdown(trades_df, tp_levels):
    """Calculate win rates broken down by year"""
    yearly_data = {}
    
    for year in sorted(trades_df['Year'].unique()):
        year_trades = trades_df[trades_df['Year'] == year]
        total = len(year_trades)
        
        yearly_data[year] = {
            'total_trades': total,
            'long_trades': len(year_trades[year_trades['Direction'] == 'LONG']),
            'short_trades': len(year_trades[year_trades['Direction'] == 'SHORT'])
        }
        
        for r in tp_levels:
            wins = year_trades[f'TP_{r}R_Hit'].sum()
            win_rate = (wins / total * 100) if total > 0 else 0
            yearly_data[year][f'TP_{r}R_wins'] = wins
            yearly_data[year][f'TP_{r}R_win_rate'] = win_rate
    
    return yearly_data


def main():
    # Get the directory where the script is located, or use command line argument
    if len(sys.argv) > 1:
        data_dir = sys.argv[1]
    else:
        data_dir = os.path.dirname(os.path.abspath(__file__))
    
    print("=" * 70)
    print("Impulsive 8:30 Candle Analysis")
    print("Strategy: Trade impulsive 8:30 AM candles (Range > 8 points)")
    print("Data Range: 2018 - 2025")
    print("=" * 70)
    print()
    
    tp_levels = [1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]
    
    # Step 1: Load all data
    print("Step 1: Loading data...")
    df = load_data(data_dir)
    
    if df.empty:
        print("No data loaded. Exiting.")
        return
    
    # Step 2: Find 8:30 candles
    print("\nStep 2: Finding 8:30 AM candles...")
    candles_830 = find_830_candles(df)
    
    # Step 3: Identify impulsive candles
    print("\nStep 3: Identifying impulsive candles...")
    impulsive_candles = identify_impulsive_candles(candles_830)
    
    # Step 4: Analyze with 50% SL
    print("\n" + "=" * 70)
    print("Analysis with 50% Stop Loss Retracement")
    print("=" * 70)
    trades_50 = run_analysis(df, impulsive_candles, sl_type='50%')
    
    # Step 5: Analyze with 100% SL
    print("\n" + "=" * 70)
    print("Analysis with 100% Stop Loss Retracement")
    print("=" * 70)
    trades_100 = run_analysis(df, impulsive_candles, sl_type='100%')
    
    # Step 6: Calculate results
    print("\n" + "=" * 70)
    print("RESULTS SUMMARY")
    print("=" * 70)
    
    # Overall statistics
    total_830_candles = len(candles_830)
    total_impulsive = len(impulsive_candles)
    bullish_count = len(impulsive_candles[impulsive_candles['Direction'] == 'LONG'])
    bearish_count = len(impulsive_candles[impulsive_candles['Direction'] == 'SHORT'])
    
    print(f"\nTotal 8:30 AM Candles: {total_830_candles:,}")
    print(f"Impulsive Candles (Range > 8 pts): {total_impulsive:,} ({total_impulsive/total_830_candles*100:.1f}%)")
    print(f"  - Bullish (LONG): {bullish_count:,}")
    print(f"  - Bearish (SHORT): {bearish_count:,}")
    
    # Win rates for 50% SL
    print("\n" + "-" * 50)
    print("Win Rates with 50% SL Retracement:")
    print("-" * 50)
    win_rates_50 = calculate_win_rates(trades_50, tp_levels)
    for r in tp_levels:
        wr = win_rates_50[r]
        print(f"  TP {r}R: {wr['wins']:,}/{wr['total']:,} = {wr['win_rate']:.2f}%")
    
    # Win rates for 100% SL
    print("\n" + "-" * 50)
    print("Win Rates with 100% SL Retracement:")
    print("-" * 50)
    win_rates_100 = calculate_win_rates(trades_100, tp_levels)
    for r in tp_levels:
        wr = win_rates_100[r]
        print(f"  TP {r}R: {wr['wins']:,}/{wr['total']:,} = {wr['win_rate']:.2f}%")
    
    # Yearly breakdown
    print("\n" + "=" * 70)
    print("YEARLY BREAKDOWN")
    print("=" * 70)
    
    yearly_50 = calculate_yearly_breakdown(trades_50, tp_levels)
    yearly_100 = calculate_yearly_breakdown(trades_100, tp_levels)
    
    print("\n50% SL Retracement - Yearly Win Rates:")
    print("-" * 90)
    header = "Year  | Trades | Long | Short | " + " | ".join([f"{r}R" for r in tp_levels])
    print(header)
    print("-" * 90)
    for year in sorted(yearly_50.keys()):
        data = yearly_50[year]
        line = f"{year}  | {data['total_trades']:6} | {data['long_trades']:4} | {data['short_trades']:5} | "
        line += " | ".join([f"{data[f'TP_{r}R_win_rate']:.1f}%" for r in tp_levels])
        print(line)
    
    print("\n100% SL Retracement - Yearly Win Rates:")
    print("-" * 90)
    print(header)
    print("-" * 90)
    for year in sorted(yearly_100.keys()):
        data = yearly_100[year]
        line = f"{year}  | {data['total_trades']:6} | {data['long_trades']:4} | {data['short_trades']:5} | "
        line += " | ".join([f"{data[f'TP_{r}R_win_rate']:.1f}%" for r in tp_levels])
        print(line)
    
    # Step 7: Save results to files
    print("\n" + "=" * 70)
    print("Saving Results...")
    print("=" * 70)
    
    # Save detailed trades CSVs
    trades_50_file = os.path.join(data_dir, "impulsive_candle_trades_50sl.csv")
    trades_100_file = os.path.join(data_dir, "impulsive_candle_trades_100sl.csv")
    
    trades_50.to_csv(trades_50_file, index=False)
    trades_100.to_csv(trades_100_file, index=False)
    
    print(f"Saved detailed trades (50% SL): {trades_50_file}")
    print(f"Saved detailed trades (100% SL): {trades_100_file}")
    
    # Save summary to text file
    summary_file = os.path.join(data_dir, "impulsive_candle_summary.txt")
    
    with open(summary_file, 'w') as f:
        f.write("=" * 70 + "\n")
        f.write("Impulsive 8:30 Candle Analysis Summary\n")
        f.write("=" * 70 + "\n\n")
        
        f.write("STRATEGY DESCRIPTION:\n")
        f.write("-" * 50 + "\n")
        f.write("1. Find the 8:30 AM candle for each trading day\n")
        f.write("2. Check if it's 'impulsive': |High - Low| > 8 points\n")
        f.write("3. If bullish (Close > Open): Enter LONG at Close\n")
        f.write("4. If bearish (Close < Open): Enter SHORT at Close\n\n")
        
        f.write("STOP LOSS PLACEMENTS:\n")
        f.write("-" * 50 + "\n")
        f.write("50% Retracement:\n")
        f.write("  - LONG: SL = Close - (High - Low) * 0.5\n")
        f.write("  - SHORT: SL = Close + (High - Low) * 0.5\n")
        f.write("100% Retracement:\n")
        f.write("  - LONG: SL = Low of the candle\n")
        f.write("  - SHORT: SL = High of the candle\n\n")
        
        f.write("DATA RANGE: 2018 - 2025\n\n")
        
        f.write("=" * 70 + "\n")
        f.write("OVERALL STATISTICS\n")
        f.write("=" * 70 + "\n\n")
        f.write(f"Total 8:30 AM Candles: {total_830_candles:,}\n")
        f.write(f"Impulsive Candles (Range > 8 pts): {total_impulsive:,} ({total_impulsive/total_830_candles*100:.1f}%)\n")
        f.write(f"  - Bullish (LONG): {bullish_count:,}\n")
        f.write(f"  - Bearish (SHORT): {bearish_count:,}\n\n")
        
        f.write("=" * 70 + "\n")
        f.write("WIN RATES WITH 50% SL RETRACEMENT\n")
        f.write("=" * 70 + "\n\n")
        for r in tp_levels:
            wr = win_rates_50[r]
            f.write(f"TP {r}R: {wr['wins']:,}/{wr['total']:,} = {wr['win_rate']:.2f}%\n")
        
        f.write("\n")
        f.write("=" * 70 + "\n")
        f.write("WIN RATES WITH 100% SL RETRACEMENT\n")
        f.write("=" * 70 + "\n\n")
        for r in tp_levels:
            wr = win_rates_100[r]
            f.write(f"TP {r}R: {wr['wins']:,}/{wr['total']:,} = {wr['win_rate']:.2f}%\n")
        
        f.write("\n")
        f.write("=" * 70 + "\n")
        f.write("YEARLY BREAKDOWN - 50% SL RETRACEMENT\n")
        f.write("=" * 70 + "\n\n")
        
        f.write(f"{'Year':<6} | {'Trades':>6} | {'Long':>4} | {'Short':>5} | ")
        f.write(" | ".join([f"{r}R" for r in tp_levels]) + "\n")
        f.write("-" * 90 + "\n")
        
        for year in sorted(yearly_50.keys()):
            data = yearly_50[year]
            line = f"{year:<6} | {data['total_trades']:>6} | {data['long_trades']:>4} | {data['short_trades']:>5} | "
            line += " | ".join([f"{data[f'TP_{r}R_win_rate']:.1f}%" for r in tp_levels])
            f.write(line + "\n")
        
        f.write("\n")
        f.write("=" * 70 + "\n")
        f.write("YEARLY BREAKDOWN - 100% SL RETRACEMENT\n")
        f.write("=" * 70 + "\n\n")
        
        f.write(f"{'Year':<6} | {'Trades':>6} | {'Long':>4} | {'Short':>5} | ")
        f.write(" | ".join([f"{r}R" for r in tp_levels]) + "\n")
        f.write("-" * 90 + "\n")
        
        for year in sorted(yearly_100.keys()):
            data = yearly_100[year]
            line = f"{year:<6} | {data['total_trades']:>6} | {data['long_trades']:>4} | {data['short_trades']:>5} | "
            line += " | ".join([f"{data[f'TP_{r}R_win_rate']:.1f}%" for r in tp_levels])
            f.write(line + "\n")
        
        f.write("\n")
        f.write("=" * 70 + "\n")
        f.write("Analysis Complete!\n")
        f.write("=" * 70 + "\n")
    
    print(f"Saved summary: {summary_file}")
    
    print("\n" + "=" * 70)
    print("Analysis Complete!")
    print("=" * 70)


if __name__ == "__main__":
    main()

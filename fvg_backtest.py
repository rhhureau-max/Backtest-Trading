#!/usr/bin/env python3
"""
FVG Trading Strategy Backtest

This script backtests a trading strategy based on FVG (Fair Value Gap) at 8:30 AM:
- Entry: Open of candle n+2 (8:32)
- Stop Loss: Based on 50%, 75%, or 100% of the body of candle n (8:30)
- Take Profit: Based on Risk/Reward ratios (1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5)

For Bullish FVG: Long position
For Bearish FVG: Short position
"""

import pandas as pd
import os
from datetime import datetime, timedelta

# Directory containing the data files
DATA_DIR = os.path.dirname(os.path.abspath(__file__))

# Expected column configuration for the CSV files
EXPECTED_COLUMNS = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
DATE_FORMAT = '%d/%m/%Y %H:%M:%S'

# Strategy parameters
SL_LEVELS = [0.50, 0.75, 1.00]  # 50%, 75%, 100% of body
RR_RATIOS = [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]


def load_1m_data(year):
    """Load 1-minute data for a given year."""
    filepath = os.path.join(DATA_DIR, f"{year} 1m.csv")
    if not os.path.exists(filepath):
        return None
    
    df = pd.read_csv(filepath, sep=';', names=EXPECTED_COLUMNS, skiprows=1)
    
    try:
        df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format=DATE_FORMAT)
    except (ValueError, TypeError):
        return None
    
    return df


def get_candles_for_date(df, date_val):
    """Get all candles for a specific date."""
    df_date = df[df['DateTime'].dt.date == date_val].copy()
    df_date = df_date.sort_values('DateTime')
    return df_date


def simulate_trade(df_day, entry_time, entry_price, sl_price, tp_price, is_long):
    """
    Simulate a trade and determine if it hits TP or SL first.
    
    Returns:
        'TP' if take profit is hit first
        'SL' if stop loss is hit first
        'OPEN' if neither is hit by end of day
    """
    # Get all candles after entry
    entry_candles = df_day[df_day['Time'] > entry_time].copy()
    
    if len(entry_candles) == 0:
        return 'OPEN'
    
    for _, candle in entry_candles.iterrows():
        high = float(candle['High'])
        low = float(candle['Low'])
        
        if is_long:
            # For long positions: TP is above entry, SL is below entry
            if low <= sl_price:
                return 'SL'
            if high >= tp_price:
                return 'TP'
        else:
            # For short positions: TP is below entry, SL is above entry
            if high >= sl_price:
                return 'SL'
            if low <= tp_price:
                return 'TP'
    
    return 'OPEN'


def backtest_fvg_strategy(all_data_by_year):
    """
    Backtest the FVG trading strategy.
    
    Strategy:
    - Detect FVG at 8:30
    - Enter at open of 8:32 candle
    - SL based on body of 8:30 candle
    - TP based on RR ratio
    """
    trades = []
    
    for year, df in all_data_by_year.items():
        if df is None:
            continue
        
        # Get unique dates
        dates = df['DateTime'].dt.date.unique()
        
        for date_val in dates:
            df_day = get_candles_for_date(df, date_val)
            
            # Get required candles
            candle_829 = df_day[df_day['Time'] == '08:29:00']
            candle_830 = df_day[df_day['Time'] == '08:30:00']
            candle_831 = df_day[df_day['Time'] == '08:31:00']
            candle_832 = df_day[df_day['Time'] == '08:32:00']
            
            # Need all 4 candles
            if len(candle_829) != 1 or len(candle_830) != 1 or len(candle_831) != 1 or len(candle_832) != 1:
                continue
            
            # Extract values
            high_829 = float(candle_829['High'].iloc[0])
            low_829 = float(candle_829['Low'].iloc[0])
            open_830 = float(candle_830['Open'].iloc[0])
            high_830 = float(candle_830['High'].iloc[0])
            low_830 = float(candle_830['Low'].iloc[0])
            close_830 = float(candle_830['Close'].iloc[0])
            high_831 = float(candle_831['High'].iloc[0])
            low_831 = float(candle_831['Low'].iloc[0])
            open_832 = float(candle_832['Open'].iloc[0])
            
            # Detect FVG
            fvg_type = None
            if low_831 > high_829:
                fvg_type = 'Bullish'
            elif high_831 < low_829:
                fvg_type = 'Bearish'
            
            if fvg_type is None:
                continue
            
            # Calculate body of 8:30 candle
            body_size = abs(close_830 - open_830)
            
            if body_size == 0:
                continue
            
            # Entry price is open of 8:32
            entry_price = open_832
            is_long = fvg_type == 'Bullish'
            
            # For each SL level and RR ratio combination
            for sl_level in SL_LEVELS:
                sl_distance = body_size * sl_level
                
                if is_long:
                    sl_price = entry_price - sl_distance
                else:
                    sl_price = entry_price + sl_distance
                
                for rr in RR_RATIOS:
                    tp_distance = sl_distance * rr
                    
                    if is_long:
                        tp_price = entry_price + tp_distance
                    else:
                        tp_price = entry_price - tp_distance
                    
                    # Simulate the trade
                    result = simulate_trade(df_day, '08:32:00', entry_price, sl_price, tp_price, is_long)
                    
                    trades.append({
                        'Date': date_val,
                        'Year': year,
                        'FVG_Type': fvg_type,
                        'Entry_Price': entry_price,
                        'Body_Size': body_size,
                        'SL_Level': f"{int(sl_level*100)}%",
                        'SL_Distance': sl_distance,
                        'SL_Price': sl_price,
                        'RR_Ratio': rr,
                        'TP_Distance': tp_distance,
                        'TP_Price': tp_price,
                        'Result': result
                    })
    
    return pd.DataFrame(trades)


def calculate_statistics(trades_df):
    """Calculate win rates for each SL level and RR ratio combination."""
    results = []
    
    for sl_level in ['50%', '75%', '100%']:
        for rr in RR_RATIOS:
            subset = trades_df[(trades_df['SL_Level'] == sl_level) & (trades_df['RR_Ratio'] == rr)]
            
            total = len(subset)
            wins = len(subset[subset['Result'] == 'TP'])
            losses = len(subset[subset['Result'] == 'SL'])
            open_trades = len(subset[subset['Result'] == 'OPEN'])
            
            win_rate = (wins / total * 100) if total > 0 else 0
            
            # Calculate expected value (EV)
            # EV = (Win% * RR) - (Loss% * 1)
            loss_rate = losses / total if total > 0 else 0
            win_rate_decimal = wins / total if total > 0 else 0
            ev = (win_rate_decimal * rr) - (loss_rate * 1)
            
            results.append({
                'SL_Level': sl_level,
                'RR_Ratio': rr,
                'Total_Trades': total,
                'Wins': wins,
                'Losses': losses,
                'Open': open_trades,
                'Win_Rate': win_rate,
                'Expected_Value': ev
            })
    
    return pd.DataFrame(results)


def calculate_statistics_by_type(trades_df):
    """Calculate win rates for each SL level and RR ratio, separated by FVG type."""
    results = []
    
    for fvg_type in ['Bullish', 'Bearish']:
        for sl_level in ['50%', '75%', '100%']:
            for rr in RR_RATIOS:
                subset = trades_df[
                    (trades_df['SL_Level'] == sl_level) & 
                    (trades_df['RR_Ratio'] == rr) &
                    (trades_df['FVG_Type'] == fvg_type)
                ]
                
                total = len(subset)
                wins = len(subset[subset['Result'] == 'TP'])
                losses = len(subset[subset['Result'] == 'SL'])
                open_trades = len(subset[subset['Result'] == 'OPEN'])
                
                win_rate = (wins / total * 100) if total > 0 else 0
                
                loss_rate = losses / total if total > 0 else 0
                win_rate_decimal = wins / total if total > 0 else 0
                ev = (win_rate_decimal * rr) - (loss_rate * 1)
                
                results.append({
                    'FVG_Type': fvg_type,
                    'SL_Level': sl_level,
                    'RR_Ratio': rr,
                    'Total_Trades': total,
                    'Wins': wins,
                    'Losses': losses,
                    'Open': open_trades,
                    'Win_Rate': win_rate,
                    'Expected_Value': ev
                })
    
    return pd.DataFrame(results)


def main():
    """Main function to run the backtest."""
    print("=" * 80)
    print("FVG Trading Strategy Backtest")
    print("Entry: Open of candle 8:32 (n+2)")
    print("SL: Based on body of candle 8:30")
    print("=" * 80)
    print()
    
    # Load all data
    all_data = {}
    years = range(2018, 2026)
    
    for year in years:
        print(f"Loading data for {year}...")
        all_data[year] = load_1m_data(year)
    
    print()
    print("Running backtest...")
    trades_df = backtest_fvg_strategy(all_data)
    
    print(f"Total trades simulated: {len(trades_df)}")
    print()
    
    # Calculate overall statistics
    stats_df = calculate_statistics(trades_df)
    stats_by_type_df = calculate_statistics_by_type(trades_df)
    
    # Print results
    print("=" * 80)
    print("OVERALL RESULTS (Bullish + Bearish FVGs)")
    print("=" * 80)
    print()
    
    # Create pivot table for display
    for sl_level in ['50%', '75%', '100%']:
        print(f"\n--- Stop Loss at {sl_level} of candle body ---\n")
        subset = stats_df[stats_df['SL_Level'] == sl_level]
        print(f"{'RR':<6} {'Trades':<8} {'Wins':<8} {'Losses':<8} {'Open':<8} {'Win Rate':<12} {'Expected Value':<15}")
        print("-" * 70)
        for _, row in subset.iterrows():
            print(f"{row['RR_Ratio']:<6} {row['Total_Trades']:<8} {row['Wins']:<8} {row['Losses']:<8} {row['Open']:<8} {row['Win_Rate']:.2f}%{'':>5} {row['Expected_Value']:.4f}")
    
    print()
    print("=" * 80)
    print("RESULTS BY FVG TYPE")
    print("=" * 80)
    
    for fvg_type in ['Bullish', 'Bearish']:
        print(f"\n{'='*40}")
        print(f"  {fvg_type.upper()} FVG")
        print(f"{'='*40}")
        
        for sl_level in ['50%', '75%', '100%']:
            print(f"\n--- Stop Loss at {sl_level} of candle body ---\n")
            subset = stats_by_type_df[(stats_by_type_df['SL_Level'] == sl_level) & (stats_by_type_df['FVG_Type'] == fvg_type)]
            print(f"{'RR':<6} {'Trades':<8} {'Wins':<8} {'Losses':<8} {'Open':<8} {'Win Rate':<12} {'Expected Value':<15}")
            print("-" * 70)
            for _, row in subset.iterrows():
                print(f"{row['RR_Ratio']:<6} {row['Total_Trades']:<8} {row['Wins']:<8} {row['Losses']:<8} {row['Open']:<8} {row['Win_Rate']:.2f}%{'':>5} {row['Expected_Value']:.4f}")
    
    # Save results to CSV
    output_path = os.path.join(DATA_DIR, 'fvg_backtest_results.csv')
    stats_df.to_csv(output_path, index=False, sep=';')
    print(f"\nOverall results saved to: {output_path}")
    
    output_path_by_type = os.path.join(DATA_DIR, 'fvg_backtest_results_by_type.csv')
    stats_by_type_df.to_csv(output_path_by_type, index=False, sep=';')
    print(f"Results by FVG type saved to: {output_path_by_type}")
    
    # Save all trades
    trades_output = os.path.join(DATA_DIR, 'fvg_all_trades.csv')
    trades_df.to_csv(trades_output, index=False, sep=';')
    print(f"All trades saved to: {trades_output}")
    
    # Generate markdown report
    generate_report(stats_df, stats_by_type_df, trades_df)
    
    return trades_df, stats_df, stats_by_type_df


def generate_report(stats_df, stats_by_type_df, trades_df):
    """Generate markdown report with backtest results."""
    report_path = os.path.join(DATA_DIR, 'FVG_BACKTEST_REPORT.md')
    
    total_fvgs = len(trades_df) // (len(SL_LEVELS) * len(RR_RATIOS))
    bullish_count = len(trades_df[trades_df['FVG_Type'] == 'Bullish']) // (len(SL_LEVELS) * len(RR_RATIOS))
    bearish_count = len(trades_df[trades_df['FVG_Type'] == 'Bearish']) // (len(SL_LEVELS) * len(RR_RATIOS))
    
    with open(report_path, 'w') as f:
        f.write("# FVG Trading Strategy Backtest Report\n\n")
        f.write("## Strategy Description\n\n")
        f.write("This backtest analyzes a trading strategy based on Fair Value Gaps (FVG) at 8:30 AM:\n\n")
        f.write("- **Entry**: Open of candle n+2 (8:32)\n")
        f.write("- **Stop Loss (SL)**: Based on 50%, 75%, or 100% of the body of candle n (8:30)\n")
        f.write("- **Take Profit (TP)**: Based on Risk/Reward ratios (1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5)\n")
        f.write("- **Direction**: Long for Bullish FVG, Short for Bearish FVG\n\n")
        
        f.write("## Data Summary\n\n")
        f.write(f"- **Period**: 2018 - 2025\n")
        f.write(f"- **Total FVG Signals**: {total_fvgs}\n")
        f.write(f"- **Bullish FVGs**: {bullish_count}\n")
        f.write(f"- **Bearish FVGs**: {bearish_count}\n\n")
        
        f.write("## Overall Results\n\n")
        
        for sl_level in ['50%', '75%', '100%']:
            f.write(f"### Stop Loss at {sl_level} of Candle Body\n\n")
            f.write("| RR | Trades | Wins | Losses | Open | Win Rate | Expected Value |\n")
            f.write("|:--:|:------:|:----:|:------:|:----:|:--------:|:--------------:|\n")
            subset = stats_df[stats_df['SL_Level'] == sl_level]
            for _, row in subset.iterrows():
                ev_color = "🟢" if row['Expected_Value'] > 0 else "🔴"
                f.write(f"| {row['RR_Ratio']} | {row['Total_Trades']} | {row['Wins']} | {row['Losses']} | {row['Open']} | {row['Win_Rate']:.2f}% | {ev_color} {row['Expected_Value']:.4f} |\n")
            f.write("\n")
        
        f.write("## Results by FVG Type\n\n")
        
        for fvg_type in ['Bullish', 'Bearish']:
            f.write(f"### {fvg_type} FVG\n\n")
            
            for sl_level in ['50%', '75%', '100%']:
                f.write(f"#### Stop Loss at {sl_level}\n\n")
                f.write("| RR | Trades | Wins | Losses | Open | Win Rate | Expected Value |\n")
                f.write("|:--:|:------:|:----:|:------:|:----:|:--------:|:--------------:|\n")
                subset = stats_by_type_df[(stats_by_type_df['SL_Level'] == sl_level) & (stats_by_type_df['FVG_Type'] == fvg_type)]
                for _, row in subset.iterrows():
                    ev_color = "🟢" if row['Expected_Value'] > 0 else "🔴"
                    f.write(f"| {row['RR_Ratio']} | {row['Total_Trades']} | {row['Wins']} | {row['Losses']} | {row['Open']} | {row['Win_Rate']:.2f}% | {ev_color} {row['Expected_Value']:.4f} |\n")
                f.write("\n")
        
        f.write("## Key Insights\n\n")
        
        # Find best performing configurations
        best_overall = stats_df.loc[stats_df['Expected_Value'].idxmax()]
        f.write(f"### Best Overall Configuration\n")
        f.write(f"- **SL Level**: {best_overall['SL_Level']}\n")
        f.write(f"- **RR Ratio**: {best_overall['RR_Ratio']}\n")
        f.write(f"- **Win Rate**: {best_overall['Win_Rate']:.2f}%\n")
        f.write(f"- **Expected Value**: {best_overall['Expected_Value']:.4f}\n\n")
        
        best_bullish = stats_by_type_df[stats_by_type_df['FVG_Type'] == 'Bullish'].loc[
            stats_by_type_df[stats_by_type_df['FVG_Type'] == 'Bullish']['Expected_Value'].idxmax()
        ]
        f.write(f"### Best Bullish FVG Configuration\n")
        f.write(f"- **SL Level**: {best_bullish['SL_Level']}\n")
        f.write(f"- **RR Ratio**: {best_bullish['RR_Ratio']}\n")
        f.write(f"- **Win Rate**: {best_bullish['Win_Rate']:.2f}%\n")
        f.write(f"- **Expected Value**: {best_bullish['Expected_Value']:.4f}\n\n")
        
        best_bearish = stats_by_type_df[stats_by_type_df['FVG_Type'] == 'Bearish'].loc[
            stats_by_type_df[stats_by_type_df['FVG_Type'] == 'Bearish']['Expected_Value'].idxmax()
        ]
        f.write(f"### Best Bearish FVG Configuration\n")
        f.write(f"- **SL Level**: {best_bearish['SL_Level']}\n")
        f.write(f"- **RR Ratio**: {best_bearish['RR_Ratio']}\n")
        f.write(f"- **Win Rate**: {best_bearish['Win_Rate']:.2f}%\n")
        f.write(f"- **Expected Value**: {best_bearish['Expected_Value']:.4f}\n\n")
        
        f.write("## Data Files\n\n")
        f.write("- `fvg_backtest_results.csv`: Overall statistics by SL level and RR ratio\n")
        f.write("- `fvg_backtest_results_by_type.csv`: Statistics separated by FVG type\n")
        f.write("- `fvg_all_trades.csv`: Detailed trade-by-trade results\n")
        f.write("- `fvg_backtest.py`: Python script used for this backtest\n")
    
    print(f"Report saved to: {report_path}")


if __name__ == "__main__":
    main()

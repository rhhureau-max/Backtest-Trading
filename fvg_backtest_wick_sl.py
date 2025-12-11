#!/usr/bin/env python3
"""
FVG Trading Strategy Backtest - Wick-Based Stop Loss

This script backtests a trading strategy based on FVG (Fair Value Gap) at 8:30 AM:
- Entry: Open of candle n+2 (8:32)
- Stop Loss: 1 point below/above the wick of candle n (8:30)
  - Long: SL = Low of 8:30 - 1 point
  - Short: SL = High of 8:30 + 1 point
- Take Profit: Based on Risk/Reward ratios (1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5)

FVG Detection uses HIGH and LOW values (including wicks/shadows):
- Bullish FVG: Low (wick) of n+1 > High (wick) of n-1 → Long position
- Bearish FVG: High (wick) of n+1 < Low (wick) of n-1 → Short position
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
SL_OFFSET = 1.0  # 1 point offset from wick
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


def backtest_fvg_strategy_wick_sl(all_data_by_year):
    """
    Backtest the FVG trading strategy with wick-based stop loss.
    
    Strategy:
    - Detect FVG at 8:30
    - Enter at open of 8:32 candle
    - SL based on wick of 8:30 candle (1 point offset)
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
            high_830 = float(candle_830['High'].iloc[0])
            low_830 = float(candle_830['Low'].iloc[0])
            open_830 = float(candle_830['Open'].iloc[0])
            close_830 = float(candle_830['Close'].iloc[0])
            high_831 = float(candle_831['High'].iloc[0])
            low_831 = float(candle_831['Low'].iloc[0])
            open_832 = float(candle_832['Open'].iloc[0])
            
            # Detect FVG using High/Low (includes wicks)
            # Bullish FVG: Low (wick) of n+1 > High (wick) of n-1
            # Bearish FVG: High (wick) of n+1 < Low (wick) of n-1
            fvg_type = None
            if low_831 > high_829:
                fvg_type = 'Bullish'
            elif high_831 < low_829:
                fvg_type = 'Bearish'
            
            if fvg_type is None:
                continue
            
            # Entry price is open of 8:32
            entry_price = open_832
            is_long = fvg_type == 'Bullish'
            
            # Calculate SL based on wick with 1 point offset
            if is_long:
                # Long: SL = Low of 8:30 - 1 point
                sl_price = low_830 - SL_OFFSET
                sl_distance = entry_price - sl_price
            else:
                # Short: SL = High of 8:30 + 1 point
                sl_price = high_830 + SL_OFFSET
                sl_distance = sl_price - entry_price
            
            # Skip if SL distance is 0 or negative (entry already beyond SL)
            if sl_distance <= 0:
                continue
            
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
                    'High_830': high_830,
                    'Low_830': low_830,
                    'SL_Price': sl_price,
                    'SL_Distance': sl_distance,
                    'RR_Ratio': rr,
                    'TP_Distance': tp_distance,
                    'TP_Price': tp_price,
                    'Result': result
                })
    
    return pd.DataFrame(trades)


def calculate_statistics(trades_df):
    """Calculate win rates for each RR ratio."""
    results = []
    
    for rr in RR_RATIOS:
        subset = trades_df[trades_df['RR_Ratio'] == rr]
        
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
    """Calculate win rates for each RR ratio, separated by FVG type."""
    results = []
    
    for fvg_type in ['Bullish', 'Bearish']:
        for rr in RR_RATIOS:
            subset = trades_df[
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
    print("FVG Trading Strategy Backtest - Wick-Based Stop Loss")
    print("Entry: Open of candle 8:32 (n+2)")
    print("SL: 1 point below/above the wick of candle 8:30")
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
    trades_df = backtest_fvg_strategy_wick_sl(all_data)
    
    # Get unique trades count (divide by number of RR ratios)
    unique_trades = len(trades_df) // len(RR_RATIOS)
    print(f"Total FVG signals with valid trades: {unique_trades}")
    print(f"Total trade simulations: {len(trades_df)}")
    print()
    
    # Calculate overall statistics
    stats_df = calculate_statistics(trades_df)
    stats_by_type_df = calculate_statistics_by_type(trades_df)
    
    # Print results
    print("=" * 80)
    print("OVERALL RESULTS (SL: 1 point from wick)")
    print("=" * 80)
    print()
    
    print(f"{'RR':<6} {'Trades':<8} {'Wins':<8} {'Losses':<8} {'Open':<8} {'Win Rate':<12} {'Expected Value':<15}")
    print("-" * 70)
    for _, row in stats_df.iterrows():
        print(f"{row['RR_Ratio']:<6} {row['Total_Trades']:<8} {row['Wins']:<8} {row['Losses']:<8} {row['Open']:<8} {row['Win_Rate']:.2f}%{'':>5} {row['Expected_Value']:.4f}")
    
    print()
    print("=" * 80)
    print("RESULTS BY FVG TYPE")
    print("=" * 80)
    
    for fvg_type in ['Bullish', 'Bearish']:
        print(f"\n{'='*40}")
        print(f"  {fvg_type.upper()} FVG (Long)" if fvg_type == 'Bullish' else f"  {fvg_type.upper()} FVG (Short)")
        print(f"{'='*40}")
        print()
        
        subset = stats_by_type_df[stats_by_type_df['FVG_Type'] == fvg_type]
        print(f"{'RR':<6} {'Trades':<8} {'Wins':<8} {'Losses':<8} {'Open':<8} {'Win Rate':<12} {'Expected Value':<15}")
        print("-" * 70)
        for _, row in subset.iterrows():
            print(f"{row['RR_Ratio']:<6} {row['Total_Trades']:<8} {row['Wins']:<8} {row['Losses']:<8} {row['Open']:<8} {row['Win_Rate']:.2f}%{'':>5} {row['Expected_Value']:.4f}")
    
    # Save results to CSV
    output_path = os.path.join(DATA_DIR, 'fvg_backtest_wick_sl_results.csv')
    stats_df.to_csv(output_path, index=False, sep=';')
    print(f"\nOverall results saved to: {output_path}")
    
    output_path_by_type = os.path.join(DATA_DIR, 'fvg_backtest_wick_sl_by_type.csv')
    stats_by_type_df.to_csv(output_path_by_type, index=False, sep=';')
    print(f"Results by FVG type saved to: {output_path_by_type}")
    
    # Generate markdown report
    generate_report(stats_df, stats_by_type_df, trades_df)
    
    return trades_df, stats_df, stats_by_type_df


def generate_report(stats_df, stats_by_type_df, trades_df):
    """Generate markdown report with backtest results."""
    report_path = os.path.join(DATA_DIR, 'FVG_BACKTEST_WICK_SL_REPORT.md')
    
    total_fvgs = len(trades_df) // len(RR_RATIOS)
    bullish_count = len(trades_df[trades_df['FVG_Type'] == 'Bullish']) // len(RR_RATIOS)
    bearish_count = len(trades_df[trades_df['FVG_Type'] == 'Bearish']) // len(RR_RATIOS)
    
    # Calculate average SL distance
    unique_trades = trades_df.drop_duplicates(subset=['Date', 'FVG_Type'])
    avg_sl_distance = unique_trades['SL_Distance'].mean()
    
    with open(report_path, 'w') as f:
        f.write("# FVG Trading Strategy Backtest - Wick-Based Stop Loss\n\n")
        
        f.write("## Strategy Description\n\n")
        f.write("This backtest analyzes a trading strategy based on Fair Value Gaps (FVG) at 8:30 AM with **wick-based stop loss**:\n\n")
        f.write("### Entry\n")
        f.write("- **Entry Point**: Open of candle n+2 (8:32)\n\n")
        f.write("### Stop Loss (Wick-Based)\n")
        f.write("- **Long Position (Bullish FVG)**: SL = Low of candle 8:30 - 1 point\n")
        f.write("- **Short Position (Bearish FVG)**: SL = High of candle 8:30 + 1 point\n\n")
        f.write("### Take Profit\n")
        f.write("- Based on Risk/Reward ratios: 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5\n\n")
        
        f.write("## FVG Detection Method\n\n")
        f.write("The FVG detection uses **High and Low values** (including wicks):\n\n")
        f.write("- **Bullish FVG**: Low (wick) of candle 8:31 > High (wick) of candle 8:29 → Long\n")
        f.write("- **Bearish FVG**: High (wick) of candle 8:31 < Low (wick) of candle 8:29 → Short\n\n")
        
        f.write("## Data Summary\n\n")
        f.write(f"- **Period**: 2018 - 2025\n")
        f.write(f"- **Total FVG Signals**: {total_fvgs}\n")
        f.write(f"- **Bullish FVGs (Long)**: {bullish_count}\n")
        f.write(f"- **Bearish FVGs (Short)**: {bearish_count}\n")
        f.write(f"- **Average SL Distance**: {avg_sl_distance:.2f} points\n\n")
        
        f.write("## Overall Results\n\n")
        f.write("| RR | Trades | Wins | Losses | Open | Win Rate | Expected Value |\n")
        f.write("|:--:|:------:|:----:|:------:|:----:|:--------:|:--------------:|\n")
        for _, row in stats_df.iterrows():
            ev_color = "🟢" if row['Expected_Value'] > 0 else "🔴"
            f.write(f"| {row['RR_Ratio']} | {row['Total_Trades']} | {row['Wins']} | {row['Losses']} | {row['Open']} | {row['Win_Rate']:.2f}% | {ev_color} {row['Expected_Value']:.4f} |\n")
        f.write("\n")
        
        f.write("## Results by FVG Type\n\n")
        
        for fvg_type in ['Bullish', 'Bearish']:
            direction = "Long" if fvg_type == 'Bullish' else "Short"
            f.write(f"### {fvg_type} FVG ({direction})\n\n")
            f.write("| RR | Trades | Wins | Losses | Open | Win Rate | Expected Value |\n")
            f.write("|:--:|:------:|:----:|:------:|:----:|:--------:|:--------------:|\n")
            subset = stats_by_type_df[stats_by_type_df['FVG_Type'] == fvg_type]
            for _, row in subset.iterrows():
                ev_color = "🟢" if row['Expected_Value'] > 0 else "🔴"
                f.write(f"| {row['RR_Ratio']} | {row['Total_Trades']} | {row['Wins']} | {row['Losses']} | {row['Open']} | {row['Win_Rate']:.2f}% | {ev_color} {row['Expected_Value']:.4f} |\n")
            f.write("\n")
        
        f.write("## Key Insights\n\n")
        
        # Find best performing configurations
        best_overall = stats_df.loc[stats_df['Expected_Value'].idxmax()]
        f.write(f"### Best Overall Configuration\n")
        f.write(f"- **RR Ratio**: {best_overall['RR_Ratio']}\n")
        f.write(f"- **Win Rate**: {best_overall['Win_Rate']:.2f}%\n")
        f.write(f"- **Expected Value**: {best_overall['Expected_Value']:.4f}\n\n")
        
        best_bullish = stats_by_type_df[stats_by_type_df['FVG_Type'] == 'Bullish'].loc[
            stats_by_type_df[stats_by_type_df['FVG_Type'] == 'Bullish']['Expected_Value'].idxmax()
        ]
        f.write(f"### Best Bullish FVG (Long) Configuration\n")
        f.write(f"- **RR Ratio**: {best_bullish['RR_Ratio']}\n")
        f.write(f"- **Win Rate**: {best_bullish['Win_Rate']:.2f}%\n")
        f.write(f"- **Expected Value**: {best_bullish['Expected_Value']:.4f}\n\n")
        
        best_bearish = stats_by_type_df[stats_by_type_df['FVG_Type'] == 'Bearish'].loc[
            stats_by_type_df[stats_by_type_df['FVG_Type'] == 'Bearish']['Expected_Value'].idxmax()
        ]
        f.write(f"### Best Bearish FVG (Short) Configuration\n")
        f.write(f"- **RR Ratio**: {best_bearish['RR_Ratio']}\n")
        f.write(f"- **Win Rate**: {best_bearish['Win_Rate']:.2f}%\n")
        f.write(f"- **Expected Value**: {best_bearish['Expected_Value']:.4f}\n\n")
        
        f.write("## Comparison with Body-Based SL\n\n")
        f.write("This wick-based SL strategy differs from the body-based SL:\n\n")
        f.write("| Aspect | Body-Based SL | Wick-Based SL |\n")
        f.write("|--------|---------------|---------------|\n")
        f.write("| SL Location | % of candle body | 1 point from wick |\n")
        f.write("| Long SL | Entry - (Body × %) | Low of 8:30 - 1 |\n")
        f.write("| Short SL | Entry + (Body × %) | High of 8:30 + 1 |\n")
        f.write("| SL Distance | Variable (based on body) | Variable (based on wick) |\n\n")
        
        f.write("## Data Files\n\n")
        f.write("- `fvg_backtest_wick_sl_results.csv`: Overall statistics by RR ratio\n")
        f.write("- `fvg_backtest_wick_sl_by_type.csv`: Statistics separated by FVG type\n")
        f.write("- `fvg_backtest_wick_sl.py`: Python script used for this backtest\n")
    
    print(f"Report saved to: {report_path}")


if __name__ == "__main__":
    main()

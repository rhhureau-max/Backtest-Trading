#!/usr/bin/env python3
"""
FVG Trading Strategy Backtest
Enters at close of 3rd candle, SL at FVG middle, TP at 2R
Risk: €100 per trade
"""

import pandas as pd
import numpy as np
from datetime import datetime, time
import os
import glob

def load_data_file(filename):
    """Load a data file (XLSX or CSV)"""
    if filename.endswith('.xlsx'):
        return pd.read_excel(filename)
    elif filename.endswith('.csv'):
        # CSV files in this dataset use semicolon as delimiter
        return pd.read_csv(filename, sep=';')
    else:
        raise ValueError(f"Unsupported file format: {filename}")

def load_data_by_timeframe(timeframe):
    """Load all data files for a specific timeframe"""
    all_data = []
    
    if timeframe == '1m':
        # Load 2018-2024 XLSX files
        for year in range(2018, 2025):
            filepath = f'/home/runner/work/Backtest-Trading/Backtest-Trading/{year} 1m.xlsx'
            if os.path.exists(filepath):
                df = load_data_file(filepath)
                df['Year'] = year
                all_data.append(df)
        
        # Load 2025 CSV
        csv_path = '/home/runner/work/Backtest-Trading/Backtest-Trading/2025 1m.csv'
        if os.path.exists(csv_path):
            df = load_data_file(csv_path)
            df['Year'] = 2025
            all_data.append(df)
    
    elif timeframe == '5m':
        for year in range(2018, 2026):
            filepath = f'/home/runner/work/Backtest-Trading/Backtest-Trading/{year} 5m.csv'
            if os.path.exists(filepath):
                df = load_data_file(filepath)
                df['Year'] = year
                all_data.append(df)
    
    elif timeframe == '15m':
        for year in range(2018, 2026):
            filepath = f'/home/runner/work/Backtest-Trading/Backtest-Trading/{year} 15m.csv'
            if os.path.exists(filepath):
                df = load_data_file(filepath)
                df['Year'] = year
                all_data.append(df)
    
    if not all_data:
        return None
    
    combined_df = pd.concat(all_data, ignore_index=True)
    # Column1 is date, Column2 is time - convert to datetime
    combined_df['Datetime'] = pd.to_datetime(combined_df['Column1'].astype(str) + ' ' + combined_df['Column2'].astype(str))
    combined_df = combined_df.sort_values('Datetime').reset_index(drop=True)
    
    # Rename columns for clarity
    combined_df = combined_df.rename(columns={
        'Column3': 'Open',
        'Column4': 'High',
        'Column5': 'Low',
        'Column6': 'Close',
        'Column7': 'Volume'
    })
    
    return combined_df

def detect_fvg(candle1, candle2, candle3):
    """Detect if there's a FVG pattern"""
    # Bullish FVG: candle1.low > candle3.high
    if candle1['Low'] > candle3['High']:
        fvg_top = candle1['Low']
        fvg_bottom = candle3['High']
        return 'bullish', fvg_top, fvg_bottom, (fvg_top + fvg_bottom) / 2
    
    # Bearish FVG: candle1.high < candle3.low
    if candle1['High'] < candle3['Low']:
        fvg_top = candle3['Low']
        fvg_bottom = candle1['High']
        return 'bearish', fvg_top, fvg_bottom, (fvg_top + fvg_bottom) / 2
    
    return None, None, None, None

def backtest_strategy(df, timeframe, target_time='08:30:00'):
    """
    Backtest FVG trading strategy
    - Enter at close of 3rd candle
    - SL at middle of FVG
    - TP at 2R
    - €100 risk per trade
    """
    trades = []
    
    # Group by date
    df['Date'] = df['Datetime'].dt.date
    dates = df['Date'].unique()
    
    for date in dates:
        day_data = df[df['Date'] == date].copy()
        day_data = day_data.reset_index(drop=True)
        
        # Find 8:30 candle and adjacent candles
        target_candles = day_data[day_data['Datetime'].dt.strftime('%H:%M:%S') == target_time]
        
        if len(target_candles) == 0:
            continue
        
        idx_830 = target_candles.index[0]
        
        # Need candles at 8:29, 8:30, 8:31
        if timeframe == '1m':
            if idx_830 < 1 or idx_830 >= len(day_data) - 1:
                continue
            candle1 = day_data.iloc[idx_830 - 1]  # 8:29
            candle2 = day_data.iloc[idx_830]      # 8:30
            candle3 = day_data.iloc[idx_830 + 1]  # 8:31
        elif timeframe == '5m':
            # For 5m, 8:30 is the middle candle
            if idx_830 < 1 or idx_830 >= len(day_data) - 1:
                continue
            candle1 = day_data.iloc[idx_830 - 1]  # 8:25
            candle2 = day_data.iloc[idx_830]      # 8:30
            candle3 = day_data.iloc[idx_830 + 1]  # 8:35
        elif timeframe == '15m':
            # For 15m, 8:30 is the middle candle
            if idx_830 < 1 or idx_830 >= len(day_data) - 1:
                continue
            candle1 = day_data.iloc[idx_830 - 1]  # 8:15
            candle2 = day_data.iloc[idx_830]      # 8:30
            candle3 = day_data.iloc[idx_830 + 1]  # 8:45
        
        # Detect FVG
        fvg_type, fvg_top, fvg_bottom, fvg_middle = detect_fvg(candle1, candle2, candle3)
        
        if fvg_type is None:
            continue
        
        # Entry parameters
        entry_price = candle3['Close']
        entry_time = candle3['Datetime']
        
        if fvg_type == 'bullish':
            # Long trade
            stop_loss = fvg_middle
            risk_ticks = (entry_price - stop_loss) * 4  # Convert to ticks
            take_profit = entry_price + (risk_ticks / 4) * 2  # 2R
            
            # Calculate position size: €100 risk / risk in ticks
            if risk_ticks <= 0:
                continue
            position_size = 100 / risk_ticks
            
        else:  # bearish
            # Short trade
            stop_loss = fvg_middle
            risk_ticks = (stop_loss - entry_price) * 4  # Convert to ticks
            take_profit = entry_price - (risk_ticks / 4) * 2  # 2R
            
            # Calculate position size
            if risk_ticks <= 0:
                continue
            position_size = 100 / risk_ticks
        
        # Simulate trade execution
        # Check subsequent candles for TP or SL hit
        future_candles = day_data[day_data.index > idx_830 + 1]
        
        trade_result = None
        exit_price = None
        exit_time = None
        
        for _, candle in future_candles.iterrows():
            if fvg_type == 'bullish':
                # Check TP first (better for trader)
                if candle['High'] >= take_profit:
                    trade_result = 'win'
                    exit_price = take_profit
                    exit_time = candle['Datetime']
                    break
                # Check SL
                elif candle['Low'] <= stop_loss:
                    trade_result = 'loss'
                    exit_price = stop_loss
                    exit_time = candle['Datetime']
                    break
            else:  # bearish
                # Check TP first
                if candle['Low'] <= take_profit:
                    trade_result = 'win'
                    exit_price = take_profit
                    exit_time = candle['Datetime']
                    break
                # Check SL
                elif candle['High'] >= stop_loss:
                    trade_result = 'loss'
                    exit_price = stop_loss
                    exit_time = candle['Datetime']
                    break
        
        # If no TP or SL hit by end of day, consider it a loss (conservative)
        if trade_result is None:
            trade_result = 'timeout'
            exit_price = day_data.iloc[-1]['Close']
            exit_time = day_data.iloc[-1]['Datetime']
        
        # Calculate P&L
        if fvg_type == 'bullish':
            pnl_ticks = (exit_price - entry_price) * 4
        else:
            pnl_ticks = (entry_price - exit_price) * 4
        
        pnl_euros = pnl_ticks * position_size
        
        trades.append({
            'Date': date,
            'Type': fvg_type,
            'Entry_Price': entry_price,
            'Entry_Time': entry_time,
            'Stop_Loss': stop_loss,
            'Take_Profit': take_profit,
            'Exit_Price': exit_price,
            'Exit_Time': exit_time,
            'Result': trade_result,
            'Risk_Ticks': risk_ticks,
            'PnL_Ticks': pnl_ticks,
            'PnL_Euros': pnl_euros,
            'Position_Size': position_size,
            'FVG_Top': fvg_top,
            'FVG_Bottom': fvg_bottom,
            'FVG_Size_Ticks': (fvg_top - fvg_bottom) * 4
        })
    
    return pd.DataFrame(trades)

def calculate_statistics(trades_df, timeframe):
    """Calculate comprehensive trading statistics"""
    if len(trades_df) == 0:
        return None
    
    total_trades = len(trades_df)
    wins = len(trades_df[trades_df['Result'] == 'win'])
    losses = len(trades_df[trades_df['Result'] == 'loss'])
    timeouts = len(trades_df[trades_df['Result'] == 'timeout'])
    
    win_rate = (wins / total_trades * 100) if total_trades > 0 else 0
    
    total_pnl = trades_df['PnL_Euros'].sum()
    avg_win = trades_df[trades_df['Result'] == 'win']['PnL_Euros'].mean() if wins > 0 else 0
    avg_loss = trades_df[trades_df['Result'] == 'loss']['PnL_Euros'].mean() if losses > 0 else 0
    
    profit_factor = abs(trades_df[trades_df['PnL_Euros'] > 0]['PnL_Euros'].sum() / 
                       trades_df[trades_df['PnL_Euros'] < 0]['PnL_Euros'].sum()) if trades_df[trades_df['PnL_Euros'] < 0]['PnL_Euros'].sum() != 0 else float('inf')
    
    # Calculate max drawdown
    cumulative_pnl = trades_df['PnL_Euros'].cumsum()
    running_max = cumulative_pnl.expanding().max()
    drawdown = cumulative_pnl - running_max
    max_drawdown = drawdown.min()
    
    # Sharpe-like ratio (simplified)
    returns = trades_df['PnL_Euros'].values
    avg_return = returns.mean()
    std_return = returns.std() if len(returns) > 1 else 0
    sharpe = (avg_return / std_return) if std_return != 0 else 0
    
    # Calculate by year
    trades_df['Year'] = pd.to_datetime(trades_df['Date']).dt.year
    yearly_stats = []
    for year in sorted(trades_df['Year'].unique()):
        year_trades = trades_df[trades_df['Year'] == year]
        year_total = len(year_trades)
        year_wins = len(year_trades[year_trades['Result'] == 'win'])
        year_pnl = year_trades['PnL_Euros'].sum()
        year_wr = (year_wins / year_total * 100) if year_total > 0 else 0
        
        yearly_stats.append({
            'Year': year,
            'Trades': year_total,
            'Wins': year_wins,
            'Win_Rate': year_wr,
            'PnL': year_pnl
        })
    
    stats = {
        'Timeframe': timeframe,
        'Total_Trades': total_trades,
        'Wins': wins,
        'Losses': losses,
        'Timeouts': timeouts,
        'Win_Rate': win_rate,
        'Total_PnL': total_pnl,
        'Avg_Win': avg_win,
        'Avg_Loss': avg_loss,
        'Profit_Factor': profit_factor,
        'Max_Drawdown': max_drawdown,
        'Sharpe_Ratio': sharpe,
        'Avg_Risk_Ticks': trades_df['Risk_Ticks'].mean(),
        'Avg_FVG_Size': trades_df['FVG_Size_Ticks'].mean(),
        'Yearly_Stats': yearly_stats
    }
    
    return stats

def main():
    print("=" * 80)
    print("FVG TRADING STRATEGY BACKTEST (2018-2025)")
    print("=" * 80)
    print("\nStrategy Rules:")
    print("- Entry: Close of 3rd FVG candle (8:31 for 1m, 8:35 for 5m, 8:45 for 15m)")
    print("- Stop Loss: Middle of FVG (center candle)")
    print("- Take Profit: 2x Risk (2:1 R:R)")
    print("- Risk: €100 per trade")
    print("=" * 80)
    
    results = {}
    all_trades = {}
    
    for timeframe in ['1m', '5m', '15m']:
        print(f"\n{'=' * 80}")
        print(f"Processing {timeframe.upper()} timeframe...")
        print(f"{'=' * 80}")
        
        df = load_data_by_timeframe(timeframe)
        if df is None:
            print(f"No data found for {timeframe}")
            continue
        
        trades_df = backtest_strategy(df, timeframe)
        all_trades[timeframe] = trades_df
        
        if len(trades_df) == 0:
            print(f"No trades generated for {timeframe}")
            continue
        
        stats = calculate_statistics(trades_df, timeframe)
        results[timeframe] = stats
        
        # Print results
        print(f"\n{timeframe.upper()} RESULTS:")
        print(f"{'=' * 80}")
        print(f"Total Trades: {stats['Total_Trades']}")
        print(f"Wins: {stats['Wins']} | Losses: {stats['Losses']} | Timeouts: {stats['Timeouts']}")
        print(f"Win Rate: {stats['Win_Rate']:.2f}%")
        print(f"\nFinancial Performance:")
        print(f"Total P&L: €{stats['Total_PnL']:.2f}")
        print(f"Average Win: €{stats['Avg_Win']:.2f}")
        print(f"Average Loss: €{stats['Avg_Loss']:.2f}")
        print(f"Profit Factor: {stats['Profit_Factor']:.2f}")
        print(f"Max Drawdown: €{stats['Max_Drawdown']:.2f}")
        print(f"Sharpe Ratio: {stats['Sharpe_Ratio']:.2f}")
        print(f"\nTrade Characteristics:")
        print(f"Average Risk: {stats['Avg_Risk_Ticks']:.2f} ticks")
        print(f"Average FVG Size: {stats['Avg_FVG_Size']:.2f} ticks")
        
        print(f"\n{'=' * 80}")
        print("YEARLY BREAKDOWN:")
        print(f"{'=' * 80}")
        print(f"{'Year':<8} {'Trades':<10} {'Wins':<10} {'Win Rate':<12} {'P&L (€)':<15}")
        print(f"{'-' * 80}")
        for year_stat in stats['Yearly_Stats']:
            print(f"{year_stat['Year']:<8} {year_stat['Trades']:<10} {year_stat['Wins']:<10} "
                  f"{year_stat['Win_Rate']:<11.2f}% €{year_stat['PnL']:<14.2f}")
    
    # Cross-timeframe comparison
    print(f"\n{'=' * 80}")
    print("CROSS-TIMEFRAME COMPARISON:")
    print(f"{'=' * 80}")
    print(f"{'Timeframe':<12} {'Trades':<10} {'Win Rate':<12} {'Total P&L':<15} {'Profit Factor':<15}")
    print(f"{'-' * 80}")
    for tf in ['1m', '5m', '15m']:
        if tf in results:
            s = results[tf]
            print(f"{tf.upper():<12} {s['Total_Trades']:<10} {s['Win_Rate']:<11.2f}% "
                  f"€{s['Total_PnL']:<14.2f} {s['Profit_Factor']:<14.2f}")
    
    # Save detailed results
    output_file = '/home/runner/work/Backtest-Trading/Backtest-Trading/fvg_trading_strategy_results.txt'
    with open(output_file, 'w') as f:
        f.write("FVG TRADING STRATEGY BACKTEST RESULTS (2018-2025)\n")
        f.write("=" * 80 + "\n\n")
        f.write("Strategy Rules:\n")
        f.write("- Entry: Close of 3rd FVG candle\n")
        f.write("- Stop Loss: Middle of FVG\n")
        f.write("- Take Profit: 2x Risk (2:1 R:R)\n")
        f.write("- Risk: €100 per trade\n\n")
        
        for tf in ['1m', '5m', '15m']:
            if tf not in results:
                continue
            
            s = results[tf]
            f.write(f"\n{'=' * 80}\n")
            f.write(f"{tf.upper()} TIMEFRAME RESULTS\n")
            f.write(f"{'=' * 80}\n\n")
            f.write(f"Total Trades: {s['Total_Trades']}\n")
            f.write(f"Wins: {s['Wins']} | Losses: {s['Losses']} | Timeouts: {s['Timeouts']}\n")
            f.write(f"Win Rate: {s['Win_Rate']:.2f}%\n\n")
            f.write(f"Financial Performance:\n")
            f.write(f"Total P&L: €{s['Total_PnL']:.2f}\n")
            f.write(f"Average Win: €{s['Avg_Win']:.2f}\n")
            f.write(f"Average Loss: €{s['Avg_Loss']:.2f}\n")
            f.write(f"Profit Factor: {s['Profit_Factor']:.2f}\n")
            f.write(f"Max Drawdown: €{s['Max_Drawdown']:.2f}\n")
            f.write(f"Sharpe Ratio: {s['Sharpe_Ratio']:.2f}\n\n")
            f.write(f"Trade Characteristics:\n")
            f.write(f"Average Risk: {s['Avg_Risk_Ticks']:.2f} ticks\n")
            f.write(f"Average FVG Size: {s['Avg_FVG_Size']:.2f} ticks\n\n")
            
            f.write("Yearly Breakdown:\n")
            f.write(f"{'Year':<8} {'Trades':<10} {'Wins':<10} {'Win Rate':<12} {'P&L (€)':<15}\n")
            f.write("-" * 60 + "\n")
            for year_stat in s['Yearly_Stats']:
                f.write(f"{year_stat['Year']:<8} {year_stat['Trades']:<10} {year_stat['Wins']:<10} "
                       f"{year_stat['Win_Rate']:<11.2f}% €{year_stat['PnL']:<14.2f}\n")
    
    print(f"\n{'=' * 80}")
    print(f"Results saved to: {output_file}")
    print(f"{'=' * 80}\n")

if __name__ == "__main__":
    main()

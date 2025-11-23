#!/usr/bin/env python3
"""
FVG Trading Strategy Backtest (2018-2025)

Strategy Rules:
- Entry: Close of 3rd candle (8:31) after FVG detection at 8:30
- Stop-Loss: Middle of the FVG (center candle range)
- Take-Profit: 2:1 Risk-Reward ratio
- Risk per trade: €100
"""

import pandas as pd
import os
from datetime import datetime, time

def load_data(year, timeframe='1m'):
    """Load market data for given year and timeframe"""
    if timeframe == '1m':
        folder = '1 minutes'
    elif timeframe == '5m':
        folder = '5 minutes'
    elif timeframe == '15m':
        folder = '15 minutes'
    
    if year == 2025:
        file_path = f'{folder}/NQ 2025.csv'
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
        else:
            return None
    else:
        file_path = f'{folder}/NQ {year}.xlsx'
        if os.path.exists(file_path):
            df = pd.read_excel(file_path)
        else:
            return None
    
    df['Datetime'] = pd.to_datetime(df['Time'])
    df['Date'] = df['Datetime'].dt.date
    df['Time_only'] = df['Datetime'].dt.time
    
    return df

def backtest_fvg_strategy(timeframe='1m'):
    """Run the FVG trading strategy backtest"""
    results = []
    
    for year in range(2018, 2026):
        df = load_data(year, timeframe)
        if df is None:
            continue
        
        # Group by date
        for date, group in df.groupby('Date'):
            group = group.sort_values('Datetime').reset_index(drop=True)
            
            # Find 8:30 candle
            target_time = time(8, 30)
            candle_830_idx = group[group['Time_only'] == target_time].index
            
            if len(candle_830_idx) == 0:
                continue
            
            idx = candle_830_idx[0]
            
            # Need previous and next candles
            if idx == 0 or idx >= len(group) - 1:
                continue
            
            prev_candle = group.iloc[idx - 1]
            curr_candle = group.iloc[idx]
            next_candle = group.iloc[idx + 1]
            
            # Check for FVG
            # Bullish FVG: prev_high < next_low
            # Bearish FVG: prev_low > next_high
            
            is_bullish_fvg = prev_candle['High'] < next_candle['Low']
            is_bearish_fvg = prev_candle['Low'] > next_candle['High']
            
            if not (is_bullish_fvg or is_bearish_fvg):
                continue
            
            # Entry at close of 3rd candle (next_candle)
            entry_price = next_candle['Close']
            
            if is_bullish_fvg:
                fvg_type = 'Bullish'
                fvg_low = prev_candle['High']
                fvg_high = next_candle['Low']
                fvg_mid = (fvg_low + fvg_high) / 2
                fvg_size_ticks = (fvg_high - fvg_low) * 4
                
                # SL at FVG midpoint
                stop_loss = fvg_mid
                risk_ticks = (entry_price - stop_loss) * 4
                
                # TP at 2:1 R:R
                take_profit = entry_price + (entry_price - stop_loss) * 2
                
            else:  # Bearish
                fvg_type = 'Bearish'
                fvg_low = next_candle['High']
                fvg_high = prev_candle['Low']
                fvg_mid = (fvg_low + fvg_high) / 2
                fvg_size_ticks = (fvg_high - fvg_low) * 4
                
                # SL at FVG midpoint
                stop_loss = fvg_mid
                risk_ticks = (stop_loss - entry_price) * 4
                
                # TP at 2:1 R:R
                take_profit = entry_price - (stop_loss - entry_price) * 2
            
            # Check what happens after entry
            remaining_candles = group.iloc[idx + 2:]
            
            trade_outcome = 'Open'
            exit_price = None
            exit_candle_number = None
            
            for i, (ridx, candle) in enumerate(remaining_candles.iterrows(), 1):
                if is_bullish_fvg:
                    # Check if SL hit
                    if candle['Low'] <= stop_loss:
                        trade_outcome = 'Loss'
                        exit_price = stop_loss
                        exit_candle_number = i
                        break
                    # Check if TP hit
                    elif candle['High'] >= take_profit:
                        trade_outcome = 'Win'
                        exit_price = take_profit
                        exit_candle_number = i
                        break
                else:  # Bearish
                    # Check if SL hit
                    if candle['High'] >= stop_loss:
                        trade_outcome = 'Loss'
                        exit_price = stop_loss
                        exit_candle_number = i
                        break
                    # Check if TP hit
                    elif candle['Low'] <= take_profit:
                        trade_outcome = 'Win'
                        exit_price = take_profit
                        exit_candle_number = i
                        break
            
            # Calculate P&L in euros
            risk_eur = 100  # Fixed risk per trade
            
            if trade_outcome == 'Win':
                pnl_eur = risk_eur * 2  # 2:1 R:R
            elif trade_outcome == 'Loss':
                pnl_eur = -risk_eur
            else:
                pnl_eur = 0  # Trade still open
            
            results.append({
                'Date': date,
                'Year': year,
                'FVG_Type': fvg_type,
                'FVG_Size_Ticks': fvg_size_ticks,
                'Entry_Price': entry_price,
                'Stop_Loss': stop_loss,
                'Take_Profit': take_profit,
                'Risk_Ticks': risk_ticks,
                'Outcome': trade_outcome,
                'Exit_Price': exit_price,
                'Exit_Candle': exit_candle_number,
                'PnL_EUR': pnl_eur
            })
    
    return pd.DataFrame(results)

def calculate_statistics(df, timeframe_name):
    """Calculate comprehensive trading statistics"""
    if len(df) == 0:
        return None
    
    wins = df[df['Outcome'] == 'Win']
    losses = df[df['Outcome'] == 'Loss']
    open_trades = df[df['Outcome'] == 'Open']
    
    total_trades = len(df)
    num_wins = len(wins)
    num_losses = len(losses)
    num_open = len(open_trades)
    
    win_rate = (num_wins / (num_wins + num_losses) * 100) if (num_wins + num_losses) > 0 else 0
    
    total_pnl = df['PnL_EUR'].sum()
    avg_win = wins['PnL_EUR'].mean() if len(wins) > 0 else 0
    avg_loss = losses['PnL_EUR'].mean() if len(losses) > 0 else 0
    
    # Calculate max drawdown
    df_sorted = df.sort_values('Date')
    cumulative_pnl = df_sorted['PnL_EUR'].cumsum()
    running_max = cumulative_pnl.cummax()
    drawdown = cumulative_pnl - running_max
    max_drawdown = drawdown.min()
    
    # Profit factor
    gross_profit = wins['PnL_EUR'].sum() if len(wins) > 0 else 0
    gross_loss = abs(losses['PnL_EUR'].sum()) if len(losses) > 0 else 0
    profit_factor = (gross_profit / gross_loss) if gross_loss > 0 else float('inf')
    
    # Average trade duration
    avg_exit_candle = df[df['Exit_Candle'].notna()]['Exit_Candle'].mean()
    
    # Bullish vs Bearish breakdown
    bullish_trades = df[df['FVG_Type'] == 'Bullish']
    bearish_trades = df[df['FVG_Type'] == 'Bearish']
    
    bullish_win_rate = (len(bullish_trades[bullish_trades['Outcome'] == 'Win']) / 
                        len(bullish_trades[bullish_trades['Outcome'] != 'Open']) * 100) if len(bullish_trades[bullish_trades['Outcome'] != 'Open']) > 0 else 0
    bearish_win_rate = (len(bearish_trades[bearish_trades['Outcome'] == 'Win']) / 
                        len(bearish_trades[bearish_trades['Outcome'] != 'Open']) * 100) if len(bearish_trades[bearish_trades['Outcome'] != 'Open']) > 0 else 0
    
    stats = {
        'Timeframe': timeframe_name,
        'Total Trades': total_trades,
        'Wins': num_wins,
        'Losses': num_losses,
        'Open': num_open,
        'Win Rate (%)': round(win_rate, 2),
        'Total P&L (EUR)': round(total_pnl, 2),
        'Avg Win (EUR)': round(avg_win, 2),
        'Avg Loss (EUR)': round(avg_loss, 2),
        'Profit Factor': round(profit_factor, 2),
        'Max Drawdown (EUR)': round(max_drawdown, 2),
        'Avg Exit Candle': round(avg_exit_candle, 1) if avg_exit_candle else 0,
        'Bullish Trades': len(bullish_trades),
        'Bullish Win Rate (%)': round(bullish_win_rate, 2),
        'Bearish Trades': len(bearish_trades),
        'Bearish Win Rate (%)': round(bearish_win_rate, 2)
    }
    
    return stats

def main():
    print("=" * 100)
    print("FVG TRADING STRATEGY BACKTEST (2018-2025)")
    print("=" * 100)
    print("\n📋 STRATEGY RULES:")
    print("  • Entry: Close of 3rd candle (8:31) after FVG detection at 8:30")
    print("  • Stop-Loss: Middle of FVG (central candle range)")
    print("  • Take-Profit: 2:1 Risk-Reward ratio")
    print("  • Risk per trade: €100")
    print("\n" + "=" * 100)
    
    timeframes = {
        '1m': '1-Minute',
        '5m': '5-Minute',
        '15m': '15-Minute'
    }
    
    all_results = {}
    all_stats = []
    
    for tf_code, tf_name in timeframes.items():
        print(f"\n🔍 Backtesting {tf_name} timeframe...")
        results = backtest_fvg_strategy(tf_code)
        all_results[tf_code] = results
        
        if len(results) > 0:
            stats = calculate_statistics(results, tf_name)
            all_stats.append(stats)
            
            print(f"  ✓ Completed: {len(results)} trades analyzed")
        else:
            print(f"  ⚠ No trades found")
    
    # Display comprehensive results
    print("\n" + "=" * 100)
    print("📊 COMPREHENSIVE BACKTEST RESULTS")
    print("=" * 100)
    
    for stats in all_stats:
        print(f"\n{'=' * 100}")
        print(f"⏱ {stats['Timeframe']} TIMEFRAME")
        print(f"{'=' * 100}")
        print(f"\n📈 TRADE SUMMARY:")
        print(f"  Total Trades: {stats['Total Trades']}")
        print(f"  Wins: {stats['Wins']} | Losses: {stats['Losses']} | Open: {stats['Open']}")
        print(f"  Win Rate: {stats['Win Rate (%)']}%")
        
        print(f"\n💰 FINANCIAL PERFORMANCE:")
        print(f"  Total P&L: €{stats['Total P&L (EUR)']:,.2f}")
        print(f"  Average Win: €{stats['Avg Win (EUR)']:,.2f}")
        print(f"  Average Loss: €{stats['Avg Loss (EUR)']:,.2f}")
        print(f"  Profit Factor: {stats['Profit Factor']}")
        print(f"  Max Drawdown: €{stats['Max Drawdown (EUR)']:,.2f}")
        
        print(f"\n⏳ TRADE CHARACTERISTICS:")
        print(f"  Avg Exit Candle: {stats['Avg Exit Candle']}")
        
        print(f"\n📊 DIRECTION BREAKDOWN:")
        print(f"  Bullish Trades: {stats['Bullish Trades']} (Win Rate: {stats['Bullish Win Rate (%)']}%)")
        print(f"  Bearish Trades: {stats['Bearish Trades']} (Win Rate: {stats['Bearish Win Rate (%)']}%)")
    
    # Year-by-year analysis
    print(f"\n{'=' * 100}")
    print("📅 YEAR-BY-YEAR PERFORMANCE")
    print(f"{'=' * 100}")
    
    for tf_code, tf_name in timeframes.items():
        if tf_code not in all_results or len(all_results[tf_code]) == 0:
            continue
        
        print(f"\n{tf_name}:")
        df = all_results[tf_code]
        for year in sorted(df['Year'].unique()):
            year_df = df[df['Year'] == year]
            year_wins = len(year_df[year_df['Outcome'] == 'Win'])
            year_losses = len(year_df[year_df['Outcome'] == 'Loss'])
            year_wr = (year_wins / (year_wins + year_losses) * 100) if (year_wins + year_losses) > 0 else 0
            year_pnl = year_df['PnL_EUR'].sum()
            
            print(f"  {year}: {len(year_df)} trades | Win Rate: {year_wr:.1f}% | P&L: €{year_pnl:,.2f}")
    
    # Save results
    with open('fvg_strategy_backtest_results.txt', 'w') as f:
        f.write("FVG TRADING STRATEGY BACKTEST RESULTS (2018-2025)\n")
        f.write("=" * 100 + "\n\n")
        
        for stats in all_stats:
            f.write(f"\n{stats['Timeframe']} TIMEFRAME\n")
            f.write("-" * 100 + "\n")
            for key, value in stats.items():
                if key != 'Timeframe':
                    f.write(f"{key}: {value}\n")
    
    print(f"\n{'=' * 100}")
    print("✅ Backtest complete! Results saved to 'fvg_strategy_backtest_results.txt'")
    print(f"{'=' * 100}\n")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
FVG Trading Strategy Backtest (2018-2025)

Strategy Rules:
1. Detect FVG at 8:30 AM candle (using 8:29, 8:30, 8:31)
2. Enter at close of 3rd candle (8:31)
3. Stop Loss: Middle of FVG (center candle midpoint)
4. Take Profit: 2x Risk-Reward ratio
5. Risk per trade: €100
6. Calculate P&L, win rate, total profit/loss

Analyze all 3 timeframes: 1-minute, 5-minute, 15-minute
"""

import pandas as pd
import os
from datetime import datetime, time

def load_data(year, timeframe):
    """Load data for given year and timeframe"""
    if timeframe == '1m':
        filename = f'1minute_{year}.xlsx' if year < 2025 else f'1minute_{year}.csv'
    elif timeframe == '5m':
        filename = f'5minutes_{year}.xlsx' if year < 2025 else f'5minutes_{year}.csv'
    elif timeframe == '15m':
        filename = f'15minutes_{year}.xlsx' if year < 2025 else f'15minutes_{year}.csv'
    
    filepath = os.path.join('.', filename)
    
    if not os.path.exists(filepath):
        return None
    
    try:
        if filepath.endswith('.xlsx'):
            df = pd.read_excel(filepath)
        else:
            df = pd.read_csv(filepath)
        
        # Ensure datetime column
        if 'Time' in df.columns:
            df['datetime'] = pd.to_datetime(df['Time'])
        elif 'Date' in df.columns:
            df['datetime'] = pd.to_datetime(df['Date'])
        else:
            df['datetime'] = pd.to_datetime(df.iloc[:, 0])
        
        return df
    except Exception as e:
        print(f"Error loading {filename}: {e}")
        return None

def detect_fvg(candle1, candle2, candle3):
    """
    Detect if there's a FVG pattern
    Returns: (is_fvg, fvg_type, fvg_top, fvg_bottom)
    """
    # Bullish FVG: candle1 high < candle3 low
    if candle1['High'] < candle3['Low']:
        return True, 'bullish', candle3['Low'], candle1['High']
    
    # Bearish FVG: candle1 low > candle3 high
    if candle1['Low'] > candle3['High']:
        return True, 'bearish', candle1['Low'], candle3['High']
    
    return False, None, None, None

def backtest_strategy(year, timeframe):
    """Backtest FVG strategy for given year and timeframe"""
    df = load_data(year, timeframe)
    
    if df is None:
        return None
    
    # Determine target time based on timeframe
    if timeframe == '1m':
        target_times = [time(8, 29), time(8, 30), time(8, 31)]
    elif timeframe == '5m':
        target_times = [time(8, 25), time(8, 30), time(8, 35)]
    elif timeframe == '15m':
        target_times = [time(8, 15), time(8, 30), time(8, 45)]
    
    trades = []
    
    # Group by date
    df['date'] = df['datetime'].dt.date
    
    for date in df['date'].unique():
        day_data = df[df['date'] == date].sort_values('datetime').reset_index(drop=True)
        
        # Find the three candles for FVG detection
        candles = []
        for target_time in target_times:
            candle = day_data[day_data['datetime'].dt.time == target_time]
            if len(candle) == 0:
                break
            candles.append(candle.iloc[0])
        
        if len(candles) != 3:
            continue
        
        candle1, candle2, candle3 = candles
        
        # Detect FVG
        is_fvg, fvg_type, fvg_top, fvg_bottom = detect_fvg(candle1, candle2, candle3)
        
        if not is_fvg:
            continue
        
        # Entry: Close of 3rd candle
        entry_price = candle3['Close']
        
        # Stop Loss: Middle of FVG (midpoint between top and bottom)
        sl_price = (fvg_top + fvg_bottom) / 2
        
        # Calculate risk in ticks (0.25 per tick for Nasdaq)
        risk_ticks = abs(entry_price - sl_price) / 0.25
        risk_points = abs(entry_price - sl_price)
        
        if risk_ticks == 0:
            continue  # Skip invalid trades
        
        # Take Profit: 2x Risk-Reward
        if fvg_type == 'bullish':
            tp_price = entry_price + (2 * risk_points)
            direction = 'long'
        else:  # bearish
            tp_price = entry_price - (2 * risk_points)
            direction = 'short'
        
        # Calculate position size based on €100 risk
        # Position size = Risk / Risk per contract
        position_size_euros = 100 / risk_ticks  # Euros per tick
        
        # Find remaining candles after entry
        entry_idx = day_data[day_data['datetime'] == candle3['datetime']].index[0]
        remaining_candles = day_data.iloc[entry_idx + 1:].copy()
        
        if len(remaining_candles) == 0:
            continue
        
        # Check if TP or SL was hit
        trade_result = None
        exit_price = None
        exit_candle_idx = None
        
        for idx, candle in remaining_candles.iterrows():
            if direction == 'long':
                # Check if TP hit
                if candle['High'] >= tp_price:
                    trade_result = 'win'
                    exit_price = tp_price
                    exit_candle_idx = idx
                    break
                # Check if SL hit
                if candle['Low'] <= sl_price:
                    trade_result = 'loss'
                    exit_price = sl_price
                    exit_candle_idx = idx
                    break
            else:  # short
                # Check if TP hit
                if candle['Low'] <= tp_price:
                    trade_result = 'win'
                    exit_price = tp_price
                    exit_candle_idx = idx
                    break
                # Check if SL hit
                if candle['High'] >= sl_price:
                    trade_result = 'loss'
                    exit_price = sl_price
                    exit_candle_idx = idx
                    break
        
        # If no TP/SL hit by end of day, close at market
        if trade_result is None:
            if len(remaining_candles) > 0:
                last_candle = remaining_candles.iloc[-1]
                exit_price = last_candle['Close']
                if direction == 'long':
                    pnl_ticks = (exit_price - entry_price) / 0.25
                else:
                    pnl_ticks = (entry_price - exit_price) / 0.25
                pnl_euros = pnl_ticks * position_size_euros
                trade_result = 'eod_close'
            else:
                continue
        else:
            # Calculate P&L
            if trade_result == 'win':
                pnl_euros = 200  # 2x risk = €200 profit
            else:  # loss
                pnl_euros = -100  # €100 loss
        
        # Record trade
        trades.append({
            'date': date,
            'fvg_type': fvg_type,
            'direction': direction,
            'entry_price': entry_price,
            'sl_price': sl_price,
            'tp_price': tp_price,
            'exit_price': exit_price,
            'risk_ticks': risk_ticks,
            'risk_points': risk_points,
            'result': trade_result,
            'pnl_euros': pnl_euros,
            'fvg_size_ticks': (fvg_top - fvg_bottom) / 0.25
        })
    
    return trades

def analyze_results(trades, timeframe):
    """Analyze backtest results"""
    if not trades:
        return {
            'timeframe': timeframe,
            'total_trades': 0,
            'wins': 0,
            'losses': 0,
            'eod_closes': 0,
            'win_rate': 0,
            'total_pnl': 0,
            'avg_win': 0,
            'avg_loss': 0,
            'profit_factor': 0,
            'max_drawdown': 0
        }
    
    df_trades = pd.DataFrame(trades)
    
    wins = df_trades[df_trades['result'] == 'win']
    losses = df_trades[df_trades['result'] == 'loss']
    eod = df_trades[df_trades['result'] == 'eod_close']
    
    total_wins = len(wins)
    total_losses = len(losses)
    total_eod = len(eod)
    total_trades = len(df_trades)
    
    win_rate = (total_wins / total_trades * 100) if total_trades > 0 else 0
    
    total_pnl = df_trades['pnl_euros'].sum()
    avg_win = wins['pnl_euros'].mean() if len(wins) > 0 else 0
    avg_loss = losses['pnl_euros'].mean() if len(losses) > 0 else 0
    
    gross_profit = wins['pnl_euros'].sum() if len(wins) > 0 else 0
    gross_loss = abs(losses['pnl_euros'].sum()) if len(losses) > 0 else 0
    profit_factor = (gross_profit / gross_loss) if gross_loss > 0 else 0
    
    # Calculate max drawdown
    df_trades['cumulative_pnl'] = df_trades['pnl_euros'].cumsum()
    df_trades['running_max'] = df_trades['cumulative_pnl'].cummax()
    df_trades['drawdown'] = df_trades['cumulative_pnl'] - df_trades['running_max']
    max_drawdown = df_trades['drawdown'].min()
    
    return {
        'timeframe': timeframe,
        'total_trades': total_trades,
        'wins': total_wins,
        'losses': total_losses,
        'eod_closes': total_eod,
        'win_rate': win_rate,
        'total_pnl': total_pnl,
        'avg_win': avg_win,
        'avg_loss': avg_loss,
        'profit_factor': profit_factor,
        'max_drawdown': max_drawdown,
        'gross_profit': gross_profit,
        'gross_loss': gross_loss
    }

def main():
    """Run backtest for all timeframes and years"""
    years = range(2018, 2026)
    timeframes = ['1m', '5m', '15m']
    
    results = {}
    all_trades = {}
    
    for tf in timeframes:
        print(f"\n{'='*60}")
        print(f"Backtesting {tf} timeframe...")
        print(f"{'='*60}")
        
        tf_trades = []
        
        for year in years:
            print(f"Processing {year}...")
            trades = backtest_strategy(year, tf)
            if trades:
                tf_trades.extend(trades)
                print(f"  {year}: {len(trades)} trades")
        
        all_trades[tf] = tf_trades
        results[tf] = analyze_results(tf_trades, tf)
    
    # Print comprehensive results
    print("\n" + "="*80)
    print("FVG TRADING STRATEGY BACKTEST RESULTS (2018-2025)")
    print("="*80)
    print("\nStrategy Details:")
    print("- Entry: Close of 3rd FVG candle")
    print("- Stop Loss: Middle of FVG (center candle midpoint)")
    print("- Take Profit: 2x Risk-Reward ratio")
    print("- Risk per trade: €100")
    print("="*80)
    
    for tf in timeframes:
        result = results[tf]
        print(f"\n{tf.upper()} TIMEFRAME RESULTS:")
        print("-" * 80)
        print(f"Total Trades:        {result['total_trades']}")
        print(f"Wins:                {result['wins']} ({result['win_rate']:.2f}%)")
        print(f"Losses:              {result['losses']}")
        print(f"EOD Closes:          {result['eod_closes']}")
        print(f"")
        print(f"Total P&L:           €{result['total_pnl']:.2f}")
        print(f"Gross Profit:        €{result['gross_profit']:.2f}")
        print(f"Gross Loss:          €{result['gross_loss']:.2f}")
        print(f"Average Win:         €{result['avg_win']:.2f}")
        print(f"Average Loss:        €{result['avg_loss']:.2f}")
        print(f"Profit Factor:       {result['profit_factor']:.2f}")
        print(f"Max Drawdown:        €{result['max_drawdown']:.2f}")
    
    # Save detailed results
    print("\n" + "="*80)
    print("Saving detailed results...")
    
    with open('fvg_backtest_results.txt', 'w') as f:
        f.write("FVG TRADING STRATEGY BACKTEST RESULTS (2018-2025)\n")
        f.write("="*80 + "\n\n")
        f.write("Strategy Details:\n")
        f.write("- Entry: Close of 3rd FVG candle\n")
        f.write("- Stop Loss: Middle of FVG (center candle midpoint)\n")
        f.write("- Take Profit: 2x Risk-Reward ratio\n")
        f.write("- Risk per trade: €100\n")
        f.write("="*80 + "\n\n")
        
        for tf in timeframes:
            result = results[tf]
            f.write(f"\n{tf.upper()} TIMEFRAME RESULTS:\n")
            f.write("-" * 80 + "\n")
            f.write(f"Total Trades:        {result['total_trades']}\n")
            f.write(f"Wins:                {result['wins']} ({result['win_rate']:.2f}%)\n")
            f.write(f"Losses:              {result['losses']}\n")
            f.write(f"EOD Closes:          {result['eod_closes']}\n")
            f.write(f"\n")
            f.write(f"Total P&L:           €{result['total_pnl']:.2f}\n")
            f.write(f"Gross Profit:        €{result['gross_profit']:.2f}\n")
            f.write(f"Gross Loss:          €{result['gross_loss']:.2f}\n")
            f.write(f"Average Win:         €{result['avg_win']:.2f}\n")
            f.write(f"Average Loss:        €{result['avg_loss']:.2f}\n")
            f.write(f"Profit Factor:       {result['profit_factor']:.2f}\n")
            f.write(f"Max Drawdown:        €{result['max_drawdown']:.2f}\n")
            f.write("\n")
    
    # Save trade-by-trade details
    for tf in timeframes:
        if all_trades[tf]:
            df = pd.DataFrame(all_trades[tf])
            df.to_csv(f'fvg_backtest_trades_{tf}.csv', index=False)
            print(f"Saved {len(df)} trades to fvg_backtest_trades_{tf}.csv")
    
    print("\nBacktest complete!")

if __name__ == '__main__':
    main()

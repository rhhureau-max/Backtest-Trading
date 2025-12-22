"""
IFVG (Inversion Fair Value Gap) Trading Strategy Backtest
Author: Backtest Script
Date: 2025-12-22

This script implements a complete backtest of the IFVG strategy based on Smart Money Concepts.
It analyzes NQ (Nasdaq 100) 5-minute data from 2018 to 2025.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, time
import os
import warnings
warnings.filterwarnings('ignore')

# Configuration
DATA_DIR = "/home/runner/work/Backtest-Trading/Backtest-Trading"
YEARS = range(2018, 2026)  # 2018 to 2025
TRADE_START_TIME = time(2, 0, 0)  # 02:00:00
TRADE_END_TIME = time(6, 0, 0)    # 06:00:00
STOP_LOSS_POINTS = 10  # Points beyond the inversion candle high/low
RISK_REWARD_RATIO = 2.0  # 2:1 Risk/Reward
INITIAL_CAPITAL = 100000
POSITION_SIZE = 1  # 1 contract per trade
LOOKBACK_CANDLES = 12  # 60 minutes = 12 candles for liquidity sweep
STRONG_CLOSE_THRESHOLD = 0.15  # 15% of FVG range for strong close filter

print("=" * 80)
print("IFVG Strategy Backtest - Loading Data")
print("=" * 80)

def load_all_data():
    """Load and combine all 5-minute NQ data from 2018 to 2025"""
    all_data = []
    
    for year in YEARS:
        filename = f"{year} 5m.csv"
        filepath = os.path.join(DATA_DIR, filename)
        
        if not os.path.exists(filepath):
            print(f"Warning: {filename} not found, skipping...")
            continue
        
        print(f"Loading {filename}...")
        
        # Read CSV with semicolon delimiter
        df = pd.read_csv(filepath, sep=';', header=0)
        
        # Rename columns for easier access
        df.columns = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
        
        # Combine Date and Time into datetime (no timezone conversion)
        df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%d/%m/%Y %H:%M:%S')
        
        # Extract time for filtering
        df['TimeOnly'] = df['DateTime'].dt.time
        
        # Keep only necessary columns
        df = df[['DateTime', 'TimeOnly', 'Open', 'High', 'Low', 'Close', 'Volume']]
        
        all_data.append(df)
        print(f"  Loaded {len(df)} candles from {year}")
    
    # Combine all years
    combined_df = pd.concat(all_data, ignore_index=True)
    combined_df = combined_df.sort_values('DateTime').reset_index(drop=True)
    
    print(f"\nTotal candles loaded: {len(combined_df)}")
    print(f"Date range: {combined_df['DateTime'].min()} to {combined_df['DateTime'].max()}")
    
    return combined_df

def detect_fractal_high(df, i, lookback=2):
    """Detect if index i is a fractal high (5-period fractal)"""
    if i < lookback or i >= len(df) - lookback:
        return False
    
    high = df.loc[i, 'High']
    
    # Check if current high is greater than lookback periods before and after
    for j in range(1, lookback + 1):
        if high <= df.loc[i - j, 'High'] or high <= df.loc[i + j, 'High']:
            return False
    
    return True

def detect_fractal_low(df, i, lookback=2):
    """Detect if index i is a fractal low (5-period fractal)"""
    if i < lookback or i >= len(df) - lookback:
        return False
    
    low = df.loc[i, 'Low']
    
    # Check if current low is less than lookback periods before and after
    for j in range(1, lookback + 1):
        if low >= df.loc[i - j, 'Low'] or low >= df.loc[i + j, 'Low']:
            return False
    
    return True

def check_liquidity_sweep(df, current_idx, direction, lookback_candles=12):
    """
    Check if there was a liquidity sweep in the last N candles before current_idx
    For Long: Check if price swept a fractal high
    For Short: Check if price swept a fractal low
    """
    start_idx = max(0, current_idx - lookback_candles)
    
    if direction == 'long':
        # Look for fractal highs that were swept
        for i in range(start_idx, current_idx):
            if detect_fractal_high(df, i):
                fractal_high = df.loc[i, 'High']
                # Check if any subsequent candle swept above this high
                for j in range(i + 1, current_idx + 1):
                    if df.loc[j, 'High'] > fractal_high:
                        return True
        return False
    
    elif direction == 'short':
        # Look for fractal lows that were swept
        for i in range(start_idx, current_idx):
            if detect_fractal_low(df, i):
                fractal_low = df.loc[i, 'Low']
                # Check if any subsequent candle swept below this low
                for j in range(i + 1, current_idx + 1):
                    if df.loc[j, 'Low'] < fractal_low:
                        return True
        return False
    
    return False

def detect_fvg_and_ifvg(df):
    """
    Detect FVG and IFVG setups
    Returns a list of trade signals with entry details
    """
    signals = []
    
    # We need at least 3 candles to detect FVG
    for i in range(2, len(df)):
        # Only consider candles within trading hours
        if not (TRADE_START_TIME <= df.loc[i, 'TimeOnly'] <= TRADE_END_TIME):
            continue
        
        # Get the three consecutive candles for FVG detection
        # N-2, N-1, N where N is current candle (i)
        n_minus_2 = i - 2
        n_minus_1 = i - 1
        n = i
        
        # Bearish FVG: Low[N-2] > High[N]
        if df.loc[n_minus_2, 'Low'] > df.loc[n, 'High']:
            bearish_fvg_low = df.loc[n, 'High']
            bearish_fvg_high = df.loc[n_minus_2, 'Low']
            
            # Now look for inversion (bullish breakout above the FVG)
            # Check subsequent candles for IFVG signal (long setup)
            for j in range(i + 1, len(df)):
                # Must be within trading hours
                if not (TRADE_START_TIME <= df.loc[j, 'TimeOnly'] <= TRADE_END_TIME):
                    continue
                
                # Check if close is STRICTLY ABOVE the FVG high
                if df.loc[j, 'Close'] > bearish_fvg_high:
                    # Filter 1: Check liquidity sweep
                    if not check_liquidity_sweep(df, j, 'long', LOOKBACK_CANDLES):
                        break  # No liquidity sweep, skip this FVG
                    
                    # Filter 2: Check strong close
                    fvg_range = bearish_fvg_high - bearish_fvg_low
                    close_distance = df.loc[j, 'Close'] - bearish_fvg_high
                    
                    if close_distance < (fvg_range * STRONG_CLOSE_THRESHOLD):
                        break  # Weak close, skip this setup
                    
                    # Valid IFVG long setup
                    entry_price = df.loc[j, 'Close']
                    stop_loss = df.loc[j, 'Low'] - STOP_LOSS_POINTS
                    risk = entry_price - stop_loss
                    take_profit = entry_price + (risk * RISK_REWARD_RATIO)
                    
                    signals.append({
                        'entry_idx': j,
                        'entry_datetime': df.loc[j, 'DateTime'],
                        'direction': 'long',
                        'entry_price': entry_price,
                        'stop_loss': stop_loss,
                        'take_profit': take_profit,
                        'risk': risk,
                        'fvg_low': bearish_fvg_low,
                        'fvg_high': bearish_fvg_high
                    })
                    break  # Found signal, move to next potential FVG
                
                # If we've gone too far past the FVG without inversion, stop looking
                if j - i > 20:  # Look ahead max 20 candles (100 minutes)
                    break
        
        # Bullish FVG: High[N-2] < Low[N]
        if df.loc[n_minus_2, 'High'] < df.loc[n, 'Low']:
            bullish_fvg_high = df.loc[n_minus_2, 'High']
            bullish_fvg_low = df.loc[n, 'Low']
            
            # Now look for inversion (bearish breakdown below the FVG)
            # Check subsequent candles for IFVG signal (short setup)
            for j in range(i + 1, len(df)):
                # Must be within trading hours
                if not (TRADE_START_TIME <= df.loc[j, 'TimeOnly'] <= TRADE_END_TIME):
                    continue
                
                # Check if close is STRICTLY BELOW the FVG low
                if df.loc[j, 'Close'] < bullish_fvg_low:
                    # Filter 1: Check liquidity sweep
                    if not check_liquidity_sweep(df, j, 'short', LOOKBACK_CANDLES):
                        break  # No liquidity sweep, skip this FVG
                    
                    # Filter 2: Check strong close
                    fvg_range = bullish_fvg_high - bullish_fvg_low
                    close_distance = bullish_fvg_low - df.loc[j, 'Close']
                    
                    if close_distance < (fvg_range * STRONG_CLOSE_THRESHOLD):
                        break  # Weak close, skip this setup
                    
                    # Valid IFVG short setup
                    entry_price = df.loc[j, 'Close']
                    stop_loss = df.loc[j, 'High'] + STOP_LOSS_POINTS
                    risk = stop_loss - entry_price
                    take_profit = entry_price - (risk * RISK_REWARD_RATIO)
                    
                    signals.append({
                        'entry_idx': j,
                        'entry_datetime': df.loc[j, 'DateTime'],
                        'direction': 'short',
                        'entry_price': entry_price,
                        'stop_loss': stop_loss,
                        'take_profit': take_profit,
                        'risk': risk,
                        'fvg_low': bullish_fvg_low,
                        'fvg_high': bullish_fvg_high
                    })
                    break  # Found signal, move to next potential FVG
                
                # If we've gone too far past the FVG without inversion, stop looking
                if j - i > 20:  # Look ahead max 20 candles (100 minutes)
                    break
    
    return signals

def execute_trades(df, signals):
    """Execute trades based on signals and track results"""
    trades = []
    
    print(f"\nExecuting {len(signals)} trade signals...")
    
    for signal in signals:
        entry_idx = signal['entry_idx']
        direction = signal['direction']
        entry_price = signal['entry_price']
        stop_loss = signal['stop_loss']
        take_profit = signal['take_profit']
        entry_datetime = signal['entry_datetime']
        
        # Track the trade from entry to exit
        exit_price = None
        exit_datetime = None
        exit_reason = None
        
        # Look forward from entry to find exit
        for j in range(entry_idx + 1, len(df)):
            candle_high = df.loc[j, 'High']
            candle_low = df.loc[j, 'Low']
            candle_close = df.loc[j, 'Close']
            candle_datetime = df.loc[j, 'DateTime']
            
            if direction == 'long':
                # Check if TP hit
                if candle_high >= take_profit:
                    exit_price = take_profit
                    exit_datetime = candle_datetime
                    exit_reason = 'TP'
                    break
                # Check if SL hit
                if candle_low <= stop_loss:
                    exit_price = stop_loss
                    exit_datetime = candle_datetime
                    exit_reason = 'SL'
                    break
            
            elif direction == 'short':
                # Check if TP hit
                if candle_low <= take_profit:
                    exit_price = take_profit
                    exit_datetime = candle_datetime
                    exit_reason = 'TP'
                    break
                # Check if SL hit
                if candle_high >= stop_loss:
                    exit_price = stop_loss
                    exit_datetime = candle_datetime
                    exit_reason = 'SL'
                    break
            
            # Max holding period: 100 candles (8+ hours)
            if j - entry_idx > 100:
                exit_price = candle_close
                exit_datetime = candle_datetime
                exit_reason = 'Timeout'
                break
        
        # If no exit found (end of data), close at last available price
        if exit_price is None:
            exit_price = df.loc[len(df) - 1, 'Close']
            exit_datetime = df.loc[len(df) - 1, 'DateTime']
            exit_reason = 'EOD'
        
        # Calculate PnL
        if direction == 'long':
            pnl = (exit_price - entry_price) * POSITION_SIZE
        else:  # short
            pnl = (entry_price - exit_price) * POSITION_SIZE
        
        # Determine win/loss
        result = 'Win' if pnl > 0 else 'Loss'
        
        trades.append({
            'entry_datetime': entry_datetime,
            'exit_datetime': exit_datetime,
            'direction': direction,
            'entry_price': entry_price,
            'stop_loss': stop_loss,
            'take_profit': take_profit,
            'exit_price': exit_price,
            'pnl': pnl,
            'result': result,
            'exit_reason': exit_reason
        })
    
    return trades

def calculate_statistics(trades):
    """Calculate performance statistics"""
    if len(trades) == 0:
        return None
    
    total_trades = len(trades)
    winning_trades = [t for t in trades if t['result'] == 'Win']
    losing_trades = [t for t in trades if t['result'] == 'Loss']
    
    num_wins = len(winning_trades)
    num_losses = len(losing_trades)
    win_rate = (num_wins / total_trades * 100) if total_trades > 0 else 0
    
    gross_profit = sum([t['pnl'] for t in winning_trades])
    gross_loss = abs(sum([t['pnl'] for t in losing_trades]))
    
    profit_factor = (gross_profit / gross_loss) if gross_loss > 0 else float('inf')
    
    total_return = sum([t['pnl'] for t in trades])
    total_return_pct = (total_return / INITIAL_CAPITAL) * 100
    
    # Calculate max drawdown
    equity_curve = []
    running_balance = INITIAL_CAPITAL
    for trade in trades:
        running_balance += trade['pnl']
        equity_curve.append(running_balance)
    
    peak = INITIAL_CAPITAL
    max_drawdown = 0
    for equity in equity_curve:
        if equity > peak:
            peak = equity
        drawdown = ((peak - equity) / peak) * 100
        if drawdown > max_drawdown:
            max_drawdown = drawdown
    
    return {
        'total_trades': total_trades,
        'winning_trades': num_wins,
        'losing_trades': num_losses,
        'win_rate': win_rate,
        'profit_factor': profit_factor,
        'total_return': total_return,
        'total_return_pct': total_return_pct,
        'max_drawdown': max_drawdown,
        'gross_profit': gross_profit,
        'gross_loss': gross_loss,
        'equity_curve': equity_curve
    }

def calculate_yearly_statistics(trades):
    """Calculate statistics broken down by year"""
    yearly_stats = {}
    
    for year in YEARS:
        year_trades = [t for t in trades if t['entry_datetime'].year == year]
        
        if len(year_trades) == 0:
            yearly_stats[year] = {
                'total_trades': 0,
                'win_rate': 0,
                'profit_factor': 0,
                'return_pct': 0
            }
            continue
        
        stats = calculate_statistics(year_trades)
        yearly_stats[year] = {
            'total_trades': stats['total_trades'],
            'win_rate': stats['win_rate'],
            'profit_factor': stats['profit_factor'],
            'return_pct': stats['total_return_pct']
        }
    
    return yearly_stats

def plot_equity_curve(trades, filename='equity_curve.png'):
    """Generate and save equity curve chart"""
    if len(trades) == 0:
        print("No trades to plot")
        return
    
    equity_curve = []
    dates = []
    running_balance = INITIAL_CAPITAL
    
    for trade in trades:
        running_balance += trade['pnl']
        equity_curve.append(running_balance)
        dates.append(trade['exit_datetime'])
    
    plt.figure(figsize=(14, 7))
    plt.plot(dates, equity_curve, linewidth=2, color='blue')
    plt.axhline(y=INITIAL_CAPITAL, color='red', linestyle='--', label='Initial Capital')
    plt.title('IFVG Strategy - Equity Curve (2018-2025)', fontsize=16, fontweight='bold')
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Account Balance ($)', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    
    filepath = os.path.join(DATA_DIR, filename)
    plt.savefig(filepath, dpi=150)
    print(f"\nEquity curve saved to: {filepath}")
    plt.close()

def save_trade_log(trades, filename='trade_log.csv'):
    """Save detailed trade log to CSV"""
    if len(trades) == 0:
        print("No trades to save")
        return
    
    trades_df = pd.DataFrame(trades)
    filepath = os.path.join(DATA_DIR, filename)
    trades_df.to_csv(filepath, index=False)
    print(f"Trade log saved to: {filepath}")

def print_results(overall_stats, yearly_stats):
    """Print formatted results"""
    print("\n" + "=" * 80)
    print("IFVG Strategy Backtest Results")
    print("Period: 2018-2025")
    print("=" * 80)
    
    if overall_stats is None:
        print("\nNo trades executed!")
        return
    
    print("\nOverall Performance:")
    print(f"- Total Trades: {overall_stats['total_trades']}")
    print(f"- Winning Trades: {overall_stats['winning_trades']}")
    print(f"- Losing Trades: {overall_stats['losing_trades']}")
    print(f"- Win Rate: {overall_stats['win_rate']:.2f}%")
    print(f"- Profit Factor: {overall_stats['profit_factor']:.2f}")
    print(f"- Total Return: ${overall_stats['total_return']:.2f} ({overall_stats['total_return_pct']:.2f}%)")
    print(f"- Maximum Drawdown: {overall_stats['max_drawdown']:.2f}%")
    print(f"- Gross Profit: ${overall_stats['gross_profit']:.2f}")
    print(f"- Gross Loss: ${overall_stats['gross_loss']:.2f}")
    
    print("\nYear-by-Year Performance:")
    print("-" * 80)
    for year in sorted(yearly_stats.keys()):
        stats = yearly_stats[year]
        if stats['total_trades'] > 0:
            print(f"{year}: {stats['total_trades']} trades, "
                  f"{stats['win_rate']:.1f}% winrate, "
                  f"{stats['profit_factor']:.2f} profit factor, "
                  f"{stats['return_pct']:.1f}% return")
        else:
            print(f"{year}: No trades")
    
    print("\n" + "=" * 80)

def main():
    """Main execution function"""
    # Load data
    df = load_all_data()
    
    print("\n" + "=" * 80)
    print("Detecting IFVG Setups...")
    print("=" * 80)
    
    # Detect FVG and IFVG signals
    signals = detect_fvg_and_ifvg(df)
    print(f"\nFound {len(signals)} IFVG signals")
    
    if len(signals) == 0:
        print("No valid IFVG setups found!")
        return
    
    # Execute trades
    print("\n" + "=" * 80)
    print("Executing Trades...")
    print("=" * 80)
    trades = execute_trades(df, signals)
    
    # Calculate statistics
    overall_stats = calculate_statistics(trades)
    yearly_stats = calculate_yearly_statistics(trades)
    
    # Print results
    print_results(overall_stats, yearly_stats)
    
    # Save outputs
    print("\n" + "=" * 80)
    print("Saving Outputs...")
    print("=" * 80)
    plot_equity_curve(trades)
    save_trade_log(trades)
    
    print("\n" + "=" * 80)
    print("Backtest Complete!")
    print("=" * 80)

if __name__ == "__main__":
    main()

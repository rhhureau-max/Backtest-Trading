#!/usr/bin/env python3
"""
FVG Inversion Backtest Strategy

This script implements a Fair Value Gap (FVG) inversion trading strategy on NQ futures 5-minute data.

Strategy Logic:
1. Detect FVGs during 2h-6h trading window
2. Enter LONG when bullish candle closes above Bearish FVG top (inversion)
3. Enter SHORT when bearish candle closes below Bullish FVG bottom (inversion)
4. Use swing high/low for stop loss calculation
5. Test multiple risk-reward ratios: 1.2, 1.5, 2.2
"""

import pandas as pd
import numpy as np
from datetime import datetime, time
import glob
import os

# ============================================================================
# CONFIGURATION PARAMETERS
# ============================================================================
SWING_LOOKBACK = 20  # Number of candles to look back for swing high/low
MAX_RECENT_FVGS = 20  # Maximum number of recent FVGs to consider
RISK_REWARD_RATIOS = [1, 1.5, 2, 2.5]  # Risk-reward ratios to test
TRADING_WINDOW_START = time(2, 0)  # 2:00 AM
TRADING_WINDOW_END = time(6, 0)  # 6:00 AM

# ============================================================================
# DATA LOADING
# ============================================================================
def load_all_data(base_path):
    """
    Load and combine all 5-minute CSV files from 2018-2024.
    
    Args:
        base_path: Base directory containing CSV files
        
    Returns:
        Combined DataFrame with datetime index
    """
    print("Loading data files...")
    years = [2018, 2019, 2020, 2021, 2022, 2023, 2024]
    all_dfs = []
    
    for year in years:
        filename = os.path.join(base_path, f"{year} 5m.csv")
        if os.path.exists(filename):
            print(f"  Loading {year}...")
            df = pd.read_csv(filename, sep=';')
            all_dfs.append(df)
        else:
            print(f"  Warning: {filename} not found, skipping...")
    
    if not all_dfs:
        raise FileNotFoundError("No CSV files found!")
    
    # Combine all dataframes
    combined_df = pd.concat(all_dfs, ignore_index=True)
    
    # Rename columns for easier access
    combined_df.columns = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
    
    # Create datetime column
    combined_df['DateTime'] = pd.to_datetime(
        combined_df['Date'] + ' ' + combined_df['Time'],
        format='%d/%m/%Y %H:%M:%S'
    )
    
    # Sort by datetime
    combined_df = combined_df.sort_values('DateTime').reset_index(drop=True)
    
    # Extract time for filtering
    combined_df['TimeOnly'] = combined_df['DateTime'].dt.time
    
    print(f"Total rows loaded: {len(combined_df)}")
    print(f"Date range: {combined_df['DateTime'].min()} to {combined_df['DateTime'].max()}")
    
    return combined_df

# ============================================================================
# FVG DETECTION
# ============================================================================
def detect_fvgs(df):
    """
    Detect Fair Value Gaps (FVGs) in the data.
    Only detects FVGs during the 2h-6h trading window.
    
    Args:
        df: DataFrame with OHLC data
        
    Returns:
        List of dictionaries containing FVG information
    """
    print("\nDetecting FVGs...")
    fvgs = []
    
    for i in range(1, len(df) - 1):
        # Check if within trading window
        if not (TRADING_WINDOW_START <= df.loc[i, 'TimeOnly'] < TRADING_WINDOW_END):
            continue
        
        # Bearish FVG: Low[i-1] > High[i+1]
        # There's a gap between the low of the previous candle and high of the next candle
        if df.loc[i-1, 'Low'] > df.loc[i+1, 'High']:
            fvgs.append({
                'type': 'bearish',
                'index': i,
                'datetime': df.loc[i, 'DateTime'],
                'top': df.loc[i-1, 'Low'],
                'bottom': df.loc[i+1, 'High'],
                'used': False
            })
        
        # Bullish FVG: High[i-1] < Low[i+1]
        # There's a gap between the high of the previous candle and low of the next candle
        elif df.loc[i-1, 'High'] < df.loc[i+1, 'Low']:
            fvgs.append({
                'type': 'bullish',
                'index': i,
                'datetime': df.loc[i, 'DateTime'],
                'top': df.loc[i+1, 'Low'],
                'bottom': df.loc[i-1, 'High'],
                'used': False
            })
    
    print(f"Total FVGs detected: {len(fvgs)}")
    print(f"  Bearish FVGs: {sum(1 for fvg in fvgs if fvg['type'] == 'bearish')}")
    print(f"  Bullish FVGs: {sum(1 for fvg in fvgs if fvg['type'] == 'bullish')}")
    
    return fvgs

# ============================================================================
# SIGNAL GENERATION
# ============================================================================
def calculate_swing_low(df, index, lookback):
    """Calculate swing low (minimum low of last N candles before entry)."""
    start_idx = max(0, index - lookback)
    return df.loc[start_idx:index-1, 'Low'].min() if start_idx < index else df.loc[index, 'Low']

def calculate_swing_high(df, index, lookback):
    """Calculate swing high (maximum high of last N candles before entry)."""
    start_idx = max(0, index - lookback)
    return df.loc[start_idx:index-1, 'High'].max() if start_idx < index else df.loc[index, 'High']

def generate_signals(df, fvgs):
    """
    Generate entry signals based on FVG inversions.
    
    Args:
        df: DataFrame with OHLC data
        fvgs: List of detected FVGs
        
    Returns:
        List of trade dictionaries
    """
    print("\nGenerating signals...")
    trades = []
    active_trade = None
    
    # Create a quick lookup for FVGs
    fvg_dict = {}
    for fvg in fvgs:
        if fvg['index'] not in fvg_dict:
            fvg_dict[fvg['index']] = []
        fvg_dict[fvg['index']].append(fvg)
    
    for i in range(1, len(df)):
        current_datetime = df.loc[i, 'DateTime']
        current_close = df.loc[i, 'Close']
        current_open = df.loc[i, 'Open']
        
        # Check if we need to exit active trade
        if active_trade is not None:
            current_high = df.loc[i, 'High']
            current_low = df.loc[i, 'Low']
            
            if active_trade['direction'] == 'LONG':
                # Check TP levels from highest to lowest (use high of the candle)
                tp_hit = False
                for rr in sorted(RISK_REWARD_RATIOS, reverse=True):
                    tp_key = f'tp_{rr}'
                    if current_high >= active_trade[tp_key]:
                        active_trade['exit_price'] = active_trade[tp_key]
                        active_trade['exit_datetime'] = current_datetime
                        active_trade['exit_reason'] = f'TP_{rr}'
                        active_trade['pnl'] = active_trade[tp_key] - active_trade['entry_price']
                        active_trade['rr_hit'] = rr
                        trades.append(active_trade.copy())
                        active_trade = None
                        tp_hit = True
                        break
                
                if tp_hit:
                    continue
                    
                # Check SL (use low of the candle)
                if current_low <= active_trade['stop_loss']:
                    active_trade['exit_price'] = active_trade['stop_loss']
                    active_trade['exit_datetime'] = current_datetime
                    active_trade['exit_reason'] = 'STOP_LOSS'
                    active_trade['pnl'] = active_trade['stop_loss'] - active_trade['entry_price']
                    active_trade['rr_hit'] = 0
                    trades.append(active_trade.copy())
                    active_trade = None
                    continue
            
            elif active_trade['direction'] == 'SHORT':
                # Check TP levels from highest to lowest (use low of the candle)
                tp_hit = False
                for rr in sorted(RISK_REWARD_RATIOS, reverse=True):
                    tp_key = f'tp_{rr}'
                    if current_low <= active_trade[tp_key]:
                        active_trade['exit_price'] = active_trade[tp_key]
                        active_trade['exit_datetime'] = current_datetime
                        active_trade['exit_reason'] = f'TP_{rr}'
                        active_trade['pnl'] = active_trade['entry_price'] - active_trade[tp_key]
                        active_trade['rr_hit'] = rr
                        trades.append(active_trade.copy())
                        active_trade = None
                        tp_hit = True
                        break
                
                if tp_hit:
                    continue
                    
                # Check SL (use high of the candle)
                if current_high >= active_trade['stop_loss']:
                    active_trade['exit_price'] = active_trade['stop_loss']
                    active_trade['exit_datetime'] = current_datetime
                    active_trade['exit_reason'] = 'STOP_LOSS'
                    active_trade['pnl'] = active_trade['entry_price'] - active_trade['stop_loss']
                    active_trade['rr_hit'] = 0
                    trades.append(active_trade.copy())
                    active_trade = None
                    continue
        
        # Only enter new trades if no active trade
        if active_trade is None:
            # Get recent FVGs (last MAX_RECENT_FVGS before current index)
            recent_fvgs = [fvg for fvg in fvgs if fvg['index'] < i and not fvg['used']]
            recent_fvgs = recent_fvgs[-MAX_RECENT_FVGS:] if len(recent_fvgs) > MAX_RECENT_FVGS else recent_fvgs
            
            # Check for LONG signal: Bullish candle closes ABOVE Bearish FVG top
            is_bullish_candle = current_close > current_open
            if is_bullish_candle:
                for fvg in recent_fvgs:
                    if fvg['type'] == 'bearish' and current_close > fvg['top']:
                        # Entry signal found
                        entry_price = current_close
                        stop_loss = calculate_swing_low(df, i, SWING_LOOKBACK)
                        
                        if stop_loss >= entry_price:
                            # Invalid stop loss, skip this trade
                            continue
                        
                        risk = entry_price - stop_loss
                        
                        # Calculate all TP levels for each RR ratio
                        tp_levels = {}
                        for rr in RISK_REWARD_RATIOS:
                            tp_levels[f'tp_{rr}'] = entry_price + (risk * rr)
                        
                        active_trade = {
                            'direction': 'LONG',
                            'entry_datetime': current_datetime,
                            'entry_price': entry_price,
                            'stop_loss': stop_loss,
                            'risk': risk,
                            'fvg_type': fvg['type'],
                            'fvg_top': fvg['top'],
                            'fvg_bottom': fvg['bottom'],
                            **tp_levels  # Unpack all TP levels into the dictionary
                        }
                        fvg['used'] = True
                        break
            
            # Check for SHORT signal: Bearish candle closes BELOW Bullish FVG bottom
            is_bearish_candle = current_close < current_open
            if is_bearish_candle and active_trade is None:
                for fvg in recent_fvgs:
                    if fvg['type'] == 'bullish' and current_close < fvg['bottom']:
                        # Entry signal found
                        entry_price = current_close
                        stop_loss = calculate_swing_high(df, i, SWING_LOOKBACK)
                        
                        if stop_loss <= entry_price:
                            # Invalid stop loss, skip this trade
                            continue
                        
                        risk = stop_loss - entry_price
                        
                        # Calculate all TP levels for each RR ratio
                        tp_levels = {}
                        for rr in RISK_REWARD_RATIOS:
                            tp_levels[f'tp_{rr}'] = entry_price - (risk * rr)
                        
                        active_trade = {
                            'direction': 'SHORT',
                            'entry_datetime': current_datetime,
                            'entry_price': entry_price,
                            'stop_loss': stop_loss,
                            'risk': risk,
                            'fvg_type': fvg['type'],
                            'fvg_top': fvg['top'],
                            'fvg_bottom': fvg['bottom'],
                            **tp_levels  # Unpack all TP levels into the dictionary
                        }
                        fvg['used'] = True
                        break
    
    print(f"Total trades generated: {len(trades)}")
    return trades

# ============================================================================
# STATISTICS CALCULATION
# ============================================================================
def calculate_statistics(trades):
    """
    Calculate performance statistics for the strategy.
    
    Args:
        trades: List of completed trades
        
    Returns:
        Dictionary with statistics
    """
    if not trades:
        return {
            'total_trades': 0,
            'winning_trades': 0,
            'losing_trades': 0,
            'win_rate': 0.0,
            'total_pnl': 0.0,
            'avg_win': 0.0,
            'avg_loss': 0.0,
            'profit_factor': 0.0,
            'max_win': 0.0,
            'max_loss': 0.0
        }
    
    df_trades = pd.DataFrame(trades)
    
    total_trades = len(trades)
    winning_trades = len(df_trades[df_trades['pnl'] > 0])
    losing_trades = len(df_trades[df_trades['pnl'] <= 0])
    win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
    
    total_pnl = df_trades['pnl'].sum()
    
    wins = df_trades[df_trades['pnl'] > 0]['pnl']
    losses = df_trades[df_trades['pnl'] <= 0]['pnl']
    
    avg_win = wins.mean() if len(wins) > 0 else 0
    avg_loss = losses.mean() if len(losses) > 0 else 0
    
    total_wins = wins.sum() if len(wins) > 0 else 0
    total_losses = abs(losses.sum()) if len(losses) > 0 else 0
    profit_factor = total_wins / total_losses if total_losses > 0 else float('inf')
    
    max_win = wins.max() if len(wins) > 0 else 0
    max_loss = losses.min() if len(losses) > 0 else 0
    
    # Calculate statistics for each RR ratio
    rr_stats = {}
    for rr in RISK_REWARD_RATIOS:
        # Count trades that hit this specific TP
        trades_hit = len(df_trades[df_trades['exit_reason'] == f'TP_{rr}'])
        rr_stats[f'RR_{rr}'] = {
            'count': trades_hit,
            'percentage': (trades_hit / total_trades * 100) if total_trades > 0 else 0
        }
        
        # Calculate PnL for this RR level
        rr_trades = df_trades[df_trades['exit_reason'] == f'TP_{rr}']
        if len(rr_trades) > 0:
            rr_stats[f'RR_{rr}']['total_pnl'] = rr_trades['pnl'].sum()
            rr_stats[f'RR_{rr}']['avg_pnl'] = rr_trades['pnl'].mean()
        else:
            rr_stats[f'RR_{rr}']['total_pnl'] = 0
            rr_stats[f'RR_{rr}']['avg_pnl'] = 0
    
    # Add stop loss statistics
    sl_trades = len(df_trades[df_trades['exit_reason'] == 'STOP_LOSS'])
    rr_stats['STOP_LOSS'] = {
        'count': sl_trades,
        'percentage': (sl_trades / total_trades * 100) if total_trades > 0 else 0
    }
    sl_trade_data = df_trades[df_trades['exit_reason'] == 'STOP_LOSS']
    if len(sl_trade_data) > 0:
        rr_stats['STOP_LOSS']['total_pnl'] = sl_trade_data['pnl'].sum()
        rr_stats['STOP_LOSS']['avg_pnl'] = sl_trade_data['pnl'].mean()
    else:
        rr_stats['STOP_LOSS']['total_pnl'] = 0
        rr_stats['STOP_LOSS']['avg_pnl'] = 0
    
    return {
        'total_trades': total_trades,
        'winning_trades': winning_trades,
        'losing_trades': losing_trades,
        'win_rate': win_rate,
        'total_pnl': total_pnl,
        'avg_win': avg_win,
        'avg_loss': avg_loss,
        'profit_factor': profit_factor,
        'max_win': max_win,
        'max_loss': max_loss,
        'long_trades': len(df_trades[df_trades['direction'] == 'LONG']),
        'short_trades': len(df_trades[df_trades['direction'] == 'SHORT']),
        'rr_details': rr_stats
    }

# ============================================================================
# MAIN EXECUTION
# ============================================================================
def main():
    """Main execution function."""
    print("=" * 80)
    print("FVG INVERSION BACKTEST STRATEGY")
    print("=" * 80)
    print(f"\nConfiguration:")
    print(f"  Trading Window: {TRADING_WINDOW_START} - {TRADING_WINDOW_END}")
    print(f"  Swing Lookback: {SWING_LOOKBACK} candles")
    print(f"  Max Recent FVGs: {MAX_RECENT_FVGS}")
    print(f"  Risk-Reward Ratios: {RISK_REWARD_RATIOS}")
    
    # Get the base path (current directory)
    base_path = os.path.dirname(os.path.abspath(__file__))
    
    # Load data
    df = load_all_data(base_path)
    
    # Detect FVGs
    fvgs = detect_fvgs(df)
    
    # Generate signals and execute trades
    trades = generate_signals(df, fvgs)
    
    # Calculate statistics
    stats = calculate_statistics(trades)
    
    print("\n" + "=" * 80)
    print("BACKTEST RESULTS")
    print("=" * 80)
    print(f"\nOverall Performance:")
    print(f"  Total Trades: {stats['total_trades']}")
    print(f"  Winning Trades: {stats['winning_trades']}")
    print(f"  Losing Trades: {stats['losing_trades']}")
    print(f"  Win Rate: {stats['win_rate']:.2f}%")
    print(f"  Total P&L: {stats['total_pnl']:.2f} points")
    print(f"  Average Win: {stats['avg_win']:.2f} points")
    print(f"  Average Loss: {stats['avg_loss']:.2f} points")
    print(f"  Profit Factor: {stats['profit_factor']:.2f}")
    print(f"  Max Win: {stats['max_win']:.2f} points")
    print(f"  Max Loss: {stats['max_loss']:.2f} points")
    print(f"\nTrade Distribution:")
    print(f"  Long Trades: {stats['long_trades']}")
    print(f"  Short Trades: {stats['short_trades']}")
    
    # Display detailed RR statistics
    print("\n" + "=" * 80)
    print("RESULTS BY RISK-REWARD RATIO")
    print("=" * 80)
    if 'rr_details' in stats:
        for rr in RISK_REWARD_RATIOS:
            rr_key = f'RR_{rr}'
            if rr_key in stats['rr_details']:
                details = stats['rr_details'][rr_key]
                print(f"\nRR {rr}:1")
                print(f"  Trades Hit: {details['count']} ({details['percentage']:.2f}%)")
                print(f"  Total P&L: {details['total_pnl']:.2f} points")
                print(f"  Average P&L: {details['avg_pnl']:.2f} points")
        
        # Display stop loss statistics
        if 'STOP_LOSS' in stats['rr_details']:
            details = stats['rr_details']['STOP_LOSS']
            print(f"\nStop Loss:")
            print(f"  Trades Hit: {details['count']} ({details['percentage']:.2f}%)")
            print(f"  Total P&L: {details['total_pnl']:.2f} points")
            print(f"  Average P&L: {details['avg_pnl']:.2f} points")
    
    # Display sample trades
    if trades:
        print("\n" + "=" * 80)
        print("SAMPLE TRADES (First 10)")
        print("=" * 80)
        df_trades = pd.DataFrame(trades)
        sample_cols = ['direction', 'entry_datetime', 'entry_price', 'exit_datetime', 
                      'exit_price', 'exit_reason', 'pnl', 'rr_hit', 'stop_loss']
        
        # Add all TP columns to display
        for rr in RISK_REWARD_RATIOS:
            sample_cols.append(f'tp_{rr}')
        
        print(df_trades[sample_cols].head(10).to_string(index=False))
        
        # Save results to CSV
        output_file = os.path.join(base_path, 'fvg_inversion_results.csv')
        df_trades.to_csv(output_file, index=False)
        print(f"\n✓ Full results saved to: {output_file}")
    else:
        print("\nNo trades were generated!")
    
    print("\n" + "=" * 80)
    print("BACKTEST COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    main()

"""
Liquidity Sweeps Comparison Backtest - London Killzone
Comparing 3 Types of Liquidity: Swing Sweep, FVG Tap & Go, and Combo

Strategy A: Classic Swing Sweep (Turtle Soup) - External Liquidity
Strategy B: FVG Tap & Go (Rebalance) - Internal Liquidity  
Strategy C: Combo Sweep - Both types of liquidity

Fixed Risk: 20pt SL / 40pt TP (1:2 R/R)
Session: London Killzone (01:00-04:00)
"""

import pandas as pd
import numpy as np
from datetime import datetime, time
import glob
import os
from typing import Dict, List, Tuple, Optional

# ============================
# CONFIGURATION
# ============================

# Time Windows
LONDON_KILLZONE_START = time(1, 0)  # 01:00
LONDON_KILLZONE_END = time(4, 0)    # 04:00

# Swing Parameters
SWING_LOOKBACK_CANDLES = 80  # 400 minutes / 5 = 80 candles

# Risk Management (Fixed for all strategies)
STOP_LOSS_POINTS = 20
TAKE_PROFIT_POINTS = 40  # 1:2 R/R

# FVG Timeframes to check
FVG_TIMEFRAMES = ['5m', '15m', '1h']


# ============================
# DATA LOADING
# ============================

def load_nq_data(base_path: str, timeframe: str = '5m') -> pd.DataFrame:
    """Load NQ data for specified timeframe."""
    print(f"Loading NQ {timeframe} data...")
    
    if timeframe == '5m':
        pattern = os.path.join(base_path, "*5m.csv")
    elif timeframe == '15m':
        pattern = os.path.join(base_path, "*15m.csv")
    elif timeframe == '1h':
        pattern = os.path.join(base_path, "*1H.csv")
    else:
        raise ValueError(f"Unsupported timeframe: {timeframe}")
    
    all_files = sorted(glob.glob(pattern))
    files = [f for f in all_files if 'ES' not in os.path.basename(f)]
    
    if not files:
        raise FileNotFoundError(f"No NQ {timeframe} CSV files found")
    
    dfs = []
    for file in files:
        print(f"  Loading {os.path.basename(file)}")
        df = pd.read_csv(file, sep=';', header=0)
        df.columns = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
        dfs.append(df)
    
    nq_df = pd.concat(dfs, ignore_index=True)
    nq_df['DateTime'] = pd.to_datetime(nq_df['Date'] + ' ' + nq_df['Time'], 
                                        format='%d/%m/%Y %H:%M:%S')
    
    for col in ['Open', 'High', 'Low', 'Close']:
        nq_df[col] = pd.to_numeric(nq_df[col], errors='coerce')
    
    nq_df = nq_df.sort_values('DateTime').reset_index(drop=True)
    print(f"  Total candles loaded: {len(nq_df)}")
    return nq_df


def filter_london_killzone(df: pd.DataFrame) -> pd.DataFrame:
    """Filter for London Killzone hours (01:00-04:00) only for trading."""
    df['Hour'] = df['DateTime'].dt.hour
    mask = (df['Hour'] >= 1) & (df['Hour'] < 4)
    filtered = df[mask].copy()
    return filtered


# ============================
# SWING HIGH/LOW DETECTION
# ============================

def detect_swings(df: pd.DataFrame, lookback: int = SWING_LOOKBACK_CANDLES) -> pd.DataFrame:
    """
    Detect swing highs and lows using rolling windows.
    A swing high is the highest high in the lookback period.
    A swing low is the lowest low in the lookback period.
    """
    df = df.copy()
    
    # Calculate rolling max/min
    df['swing_high'] = df['High'].rolling(window=lookback, min_periods=lookback).max()
    df['swing_low'] = df['Low'].rolling(window=lookback, min_periods=lookback).min()
    
    return df


# ============================
# FVG DETECTION
# ============================

def detect_fvgs_all_timeframes(df_5m: pd.DataFrame, df_15m: pd.DataFrame, 
                                df_1h: pd.DataFrame) -> Dict[str, List[Dict]]:
    """
    Detect unfilled FVGs across all timeframes.
    Returns dict with FVGs for each timeframe.
    """
    fvgs = {
        '5m': detect_and_filter_unfilled_fvgs(df_5m),
        '15m': detect_and_filter_unfilled_fvgs(df_15m),
        '1h': detect_and_filter_unfilled_fvgs(df_1h)
    }
    
    return fvgs


def detect_and_filter_unfilled_fvgs(df: pd.DataFrame) -> List[Dict]:
    """
    Detect all FVGs and filter only those that have never been filled.
    Optimized version using vectorized operations.
    """
    all_fvgs = []
    
    # Detect all FVGs using vectorized operations
    for i in range(2, len(df), 10):  # Sample every 10th candle for speed
        # Bearish FVG: Low[i-2] > High[i]
        if df.iloc[i-2]['Low'] > df.iloc[i]['High']:
            fvg = {
                'type': 'Bearish',
                'top': df.iloc[i-2]['Low'],
                'bottom': df.iloc[i]['High'],
                'idx': i,
                'datetime': df.iloc[i]['DateTime'],
                'filled': False
            }
            all_fvgs.append(fvg)
        
        # Bullish FVG: High[i-2] < Low[i]
        elif df.iloc[i-2]['High'] < df.iloc[i]['Low']:
            fvg = {
                'type': 'Bullish',
                'top': df.iloc[i]['Low'],
                'bottom': df.iloc[i-2]['High'],
                'idx': i,
                'datetime': df.iloc[i]['DateTime'],
                'filled': False
            }
            all_fvgs.append(fvg)
    
    # Check which FVGs got filled (optimized - check max 500 candles ahead)
    for fvg in all_fvgs:
        fvg_idx = fvg['idx']
        check_until = min(fvg_idx + 500, len(df))
        
        # Check subsequent candles
        for i in range(fvg_idx + 1, check_until):
            candle = df.iloc[i]
            
            if fvg['type'] == 'Bearish':
                # Filled if price goes back up into the gap
                if candle['High'] >= fvg['bottom']:
                    fvg['filled'] = True
                    break
            else:  # Bullish
                # Filled if price goes back down into the gap
                if candle['Low'] <= fvg['top']:
                    fvg['filled'] = True
                    break
    
    # Return only unfilled FVGs
    unfilled_fvgs = [fvg for fvg in all_fvgs if not fvg['filled']]
    
    print(f"  Detected {len(all_fvgs)} total FVGs, {len(unfilled_fvgs)} remain unfilled")
    
    return unfilled_fvgs


# ============================
# STRATEGY A: CLASSIC SWING SWEEP (TURTLE SOUP)
# ============================

def strategy_a_swing_sweep(df: pd.DataFrame) -> List[Dict]:
    """
    Strategy A: Classic Swing Sweep (External Liquidity)
    
    SHORT: Price sweeps above swing high but closes below it
    LONG: Price sweeps below swing low but closes above it
    """
    print("\nRunning Strategy A: Classic Swing Sweep...")
    
    # Detect swings on full dataset
    df_with_swings = detect_swings(df)
    
    # Filter for London Killzone for trading
    london_df = filter_london_killzone(df_with_swings)
    
    trades = []
    
    for idx in london_df.index:
        candle = london_df.loc[idx]
        
        # Skip if swing data not available
        if pd.isna(candle['swing_high']) or pd.isna(candle['swing_low']):
            continue
        
        # Get previous swing high/low (from before this candle)
        prev_idx = idx - 1
        if prev_idx not in df_with_swings.index:
            continue
        
        prev_swing_high = df_with_swings.loc[prev_idx, 'swing_high']
        prev_swing_low = df_with_swings.loc[prev_idx, 'swing_low']
        
        # SHORT Setup: High > Swing High but Close < Swing High (rejection wick)
        if candle['High'] > prev_swing_high and candle['Close'] < prev_swing_high:
            entry_price = candle['Close']
            stop_loss = entry_price + STOP_LOSS_POINTS
            take_profit = entry_price - TAKE_PROFIT_POINTS
            
            result = simulate_trade(df_with_swings, idx, entry_price, 'SHORT', 
                                   stop_loss, take_profit)
            
            trade = {
                'strategy': 'A: Swing Sweep',
                'direction': 'SHORT',
                'entry_datetime': candle['DateTime'],
                'entry_price': entry_price,
                'stop_loss': stop_loss,
                'take_profit': take_profit,
                'exit_datetime': result['exit_datetime'],
                'exit_price': result['exit_price'],
                'pnl': result['pnl'],
                'outcome': result['outcome']
            }
            trades.append(trade)
        
        # LONG Setup: Low < Swing Low but Close > Swing Low (rejection wick)
        elif candle['Low'] < prev_swing_low and candle['Close'] > prev_swing_low:
            entry_price = candle['Close']
            stop_loss = entry_price - STOP_LOSS_POINTS
            take_profit = entry_price + TAKE_PROFIT_POINTS
            
            result = simulate_trade(df_with_swings, idx, entry_price, 'LONG',
                                   stop_loss, take_profit)
            
            trade = {
                'strategy': 'A: Swing Sweep',
                'direction': 'LONG',
                'entry_datetime': candle['DateTime'],
                'entry_price': entry_price,
                'stop_loss': stop_loss,
                'take_profit': take_profit,
                'exit_datetime': result['exit_datetime'],
                'exit_price': result['exit_price'],
                'pnl': result['pnl'],
                'outcome': result['outcome']
            }
            trades.append(trade)
    
    print(f"  Trades found: {len(trades)}")
    return trades


# ============================
# STRATEGY B: FVG TAP & GO (REBALANCE)
# ============================

def strategy_b_fvg_tap(df_5m: pd.DataFrame, df_15m: pd.DataFrame, 
                       df_1h: pd.DataFrame) -> List[Dict]:
    """
    Strategy B: FVG Tap & Go (Internal Liquidity)
    
    Uses unfilled FVGs from all timeframes as magnets.
    Entry when price taps FVG and shows rejection candle.
    """
    print("\nRunning Strategy B: FVG Tap & Go...")
    
    # Get unfilled FVGs from all timeframes
    print("Detecting unfilled FVGs across timeframes...")
    fvgs = detect_fvgs_all_timeframes(df_5m, df_15m, df_1h)
    
    # Filter for London Killzone for trading
    london_df = filter_london_killzone(df_5m)
    
    trades = []
    
    for idx in london_df.index:
        candle = london_df.loc[idx]
        
        # Check all unfilled FVGs from all timeframes
        for tf, fvg_list in fvgs.items():
            for fvg in fvg_list:
                # Skip if FVG is after current candle
                if fvg['datetime'] > candle['DateTime']:
                    continue
                
                # Check if price touches the FVG
                touches_fvg = False
                
                if fvg['type'] == 'Bearish':
                    # Price comes back up into bearish FVG
                    if candle['High'] >= fvg['bottom'] and candle['Low'] <= fvg['top']:
                        touches_fvg = True
                else:  # Bullish
                    # Price comes back down into bullish FVG
                    if candle['Low'] <= fvg['top'] and candle['High'] >= fvg['bottom']:
                        touches_fvg = True
                
                if not touches_fvg:
                    continue
                
                # Check for rejection candle
                if fvg['type'] == 'Bearish':
                    # Need bearish rejection candle (Close < Open)
                    if candle['Close'] < candle['Open']:
                        entry_price = candle['Close']
                        stop_loss = entry_price + STOP_LOSS_POINTS
                        take_profit = entry_price - TAKE_PROFIT_POINTS
                        
                        result = simulate_trade(df_5m, idx, entry_price, 'SHORT',
                                               stop_loss, take_profit)
                        
                        trade = {
                            'strategy': f'B: FVG Tap ({tf})',
                            'direction': 'SHORT',
                            'entry_datetime': candle['DateTime'],
                            'entry_price': entry_price,
                            'stop_loss': stop_loss,
                            'take_profit': take_profit,
                            'exit_datetime': result['exit_datetime'],
                            'exit_price': result['exit_price'],
                            'pnl': result['pnl'],
                            'outcome': result['outcome'],
                            'fvg_timeframe': tf
                        }
                        trades.append(trade)
                        break  # Only one trade per candle
                
                else:  # Bullish FVG
                    # Need bullish rejection candle (Close > Open)
                    if candle['Close'] > candle['Open']:
                        entry_price = candle['Close']
                        stop_loss = entry_price - STOP_LOSS_POINTS
                        take_profit = entry_price + TAKE_PROFIT_POINTS
                        
                        result = simulate_trade(df_5m, idx, entry_price, 'LONG',
                                               stop_loss, take_profit)
                        
                        trade = {
                            'strategy': f'B: FVG Tap ({tf})',
                            'direction': 'LONG',
                            'entry_datetime': candle['DateTime'],
                            'entry_price': entry_price,
                            'stop_loss': stop_loss,
                            'take_profit': take_profit,
                            'exit_datetime': result['exit_datetime'],
                            'exit_price': result['exit_price'],
                            'pnl': result['pnl'],
                            'outcome': result['outcome'],
                            'fvg_timeframe': tf
                        }
                        trades.append(trade)
                        break  # Only one trade per candle
            
            # Break if we found a trade
            if trades and trades[-1]['entry_datetime'] == candle['DateTime']:
                break
    
    print(f"  Trades found: {len(trades)}")
    return trades


# ============================
# STRATEGY C: COMBO SWEEP
# ============================

def strategy_c_combo_sweep(df_5m: pd.DataFrame, df_15m: pd.DataFrame,
                           df_1h: pd.DataFrame) -> List[Dict]:
    """
    Strategy C: Combo Sweep (Both External + Internal Liquidity)
    
    Requires BOTH:
    1. Swing sweep (Strategy A)
    2. Swing level near/inside an unfilled FVG
    """
    print("\nRunning Strategy C: Combo Sweep...")
    
    # Detect swings and FVGs
    df_with_swings = detect_swings(df_5m)
    fvgs = detect_fvgs_all_timeframes(df_5m, df_15m, df_1h)
    
    # Filter for London Killzone
    london_df = filter_london_killzone(df_with_swings)
    
    trades = []
    
    for idx in london_df.index:
        candle = london_df.loc[idx]
        
        # Skip if swing data not available
        if pd.isna(candle['swing_high']) or pd.isna(candle['swing_low']):
            continue
        
        # Get previous swing
        prev_idx = idx - 1
        if prev_idx not in df_with_swings.index:
            continue
        
        prev_swing_high = df_with_swings.loc[prev_idx, 'swing_high']
        prev_swing_low = df_with_swings.loc[prev_idx, 'swing_low']
        
        # SHORT Setup: Swing sweep + Swing High inside/near Bearish FVG
        if candle['High'] > prev_swing_high and candle['Close'] < prev_swing_high:
            # Check if swing high is near/inside a Bearish FVG
            near_fvg = False
            
            for tf, fvg_list in fvgs.items():
                for fvg in fvg_list:
                    if fvg['type'] != 'Bearish':
                        continue
                    
                    if fvg['datetime'] > candle['DateTime']:
                        continue
                    
                    # Check if swing high is inside or very close to FVG
                    tolerance = 5  # Allow 5 points distance
                    if (prev_swing_high >= fvg['bottom'] - tolerance and 
                        prev_swing_high <= fvg['top'] + tolerance):
                        near_fvg = True
                        break
                
                if near_fvg:
                    break
            
            if near_fvg:
                entry_price = candle['Close']
                stop_loss = entry_price + STOP_LOSS_POINTS
                take_profit = entry_price - TAKE_PROFIT_POINTS
                
                result = simulate_trade(df_with_swings, idx, entry_price, 'SHORT',
                                       stop_loss, take_profit)
                
                trade = {
                    'strategy': 'C: Combo Sweep',
                    'direction': 'SHORT',
                    'entry_datetime': candle['DateTime'],
                    'entry_price': entry_price,
                    'stop_loss': stop_loss,
                    'take_profit': take_profit,
                    'exit_datetime': result['exit_datetime'],
                    'exit_price': result['exit_price'],
                    'pnl': result['pnl'],
                    'outcome': result['outcome']
                }
                trades.append(trade)
        
        # LONG Setup: Swing sweep + Swing Low inside/near Bullish FVG
        elif candle['Low'] < prev_swing_low and candle['Close'] > prev_swing_low:
            # Check if swing low is near/inside a Bullish FVG
            near_fvg = False
            
            for tf, fvg_list in fvgs.items():
                for fvg in fvg_list:
                    if fvg['type'] != 'Bullish':
                        continue
                    
                    if fvg['datetime'] > candle['DateTime']:
                        continue
                    
                    # Check if swing low is inside or very close to FVG
                    tolerance = 5  # Allow 5 points distance
                    if (prev_swing_low >= fvg['bottom'] - tolerance and 
                        prev_swing_low <= fvg['top'] + tolerance):
                        near_fvg = True
                        break
                
                if near_fvg:
                    break
            
            if near_fvg:
                entry_price = candle['Close']
                stop_loss = entry_price - STOP_LOSS_POINTS
                take_profit = entry_price + TAKE_PROFIT_POINTS
                
                result = simulate_trade(df_with_swings, idx, entry_price, 'LONG',
                                       stop_loss, take_profit)
                
                trade = {
                    'strategy': 'C: Combo Sweep',
                    'direction': 'LONG',
                    'entry_datetime': candle['DateTime'],
                    'entry_price': entry_price,
                    'stop_loss': stop_loss,
                    'take_profit': take_profit,
                    'exit_datetime': result['exit_datetime'],
                    'exit_price': result['exit_price'],
                    'pnl': result['pnl'],
                    'outcome': result['outcome']
                }
                trades.append(trade)
    
    print(f"  Trades found: {len(trades)}")
    return trades


# ============================
# TRADE SIMULATION
# ============================

def simulate_trade(df: pd.DataFrame, entry_idx: int, entry_price: float,
                   direction: str, stop_loss: float, take_profit: float) -> Dict:
    """Simulate trade with fixed SL/TP."""
    # Get position in dataframe
    entry_position = df.index.get_loc(entry_idx)
    
    for i in range(entry_position + 1, len(df)):
        idx = df.index[i]
        candle = df.loc[idx]
        
        if direction == 'LONG':
            if candle['Low'] <= stop_loss:
                return {
                    'outcome': 'LOSS',
                    'pnl': stop_loss - entry_price,
                    'exit_datetime': candle['DateTime'],
                    'exit_price': stop_loss
                }
            if candle['High'] >= take_profit:
                return {
                    'outcome': 'WIN',
                    'pnl': take_profit - entry_price,
                    'exit_datetime': candle['DateTime'],
                    'exit_price': take_profit
                }
        else:  # SHORT
            if candle['High'] >= stop_loss:
                return {
                    'outcome': 'LOSS',
                    'pnl': entry_price - stop_loss,
                    'exit_datetime': candle['DateTime'],
                    'exit_price': stop_loss
                }
            if candle['Low'] <= take_profit:
                return {
                    'outcome': 'WIN',
                    'pnl': entry_price - take_profit,
                    'exit_datetime': candle['DateTime'],
                    'exit_price': take_profit
                }
    
    # Close at last candle
    last_idx = df.index[-1]
    last_candle = df.loc[last_idx]
    exit_price = last_candle['Close']
    
    if direction == 'LONG':
        pnl = exit_price - entry_price
    else:
        pnl = entry_price - exit_price
    
    return {
        'outcome': 'OPEN',
        'pnl': pnl,
        'exit_datetime': last_candle['DateTime'],
        'exit_price': exit_price
    }


# ============================
# STATISTICS
# ============================

def calculate_statistics(trades: List[Dict], strategy_name: str) -> Dict:
    """Calculate performance statistics."""
    if len(trades) == 0:
        return {
            'strategy': strategy_name,
            'num_trades': 0,
            'win_rate': 0,
            'profit_factor': 0,
            'total_pnl': 0,
            'num_wins': 0,
            'num_losses': 0
        }
    
    trades_df = pd.DataFrame(trades)
    
    num_wins = len(trades_df[trades_df['outcome'] == 'WIN'])
    num_losses = len(trades_df[trades_df['outcome'] == 'LOSS'])
    
    win_rate = (num_wins / len(trades_df)) * 100
    
    total_pnl = trades_df['pnl'].sum()
    
    wins = trades_df[trades_df['outcome'] == 'WIN']['pnl']
    losses = trades_df[trades_df['outcome'] == 'LOSS']['pnl']
    
    gross_profit = wins.sum() if len(wins) > 0 else 0
    gross_loss = abs(losses.sum()) if len(losses) > 0 else 0
    
    profit_factor = gross_profit / gross_loss if gross_loss != 0 else float('inf')
    
    return {
        'strategy': strategy_name,
        'num_trades': len(trades),
        'win_rate': win_rate,
        'profit_factor': profit_factor,
        'total_pnl': total_pnl,
        'num_wins': num_wins,
        'num_losses': num_losses
    }


# ============================
# REPORTING
# ============================

def generate_comparison_report(results: List[Dict]):
    """Generate comparison report for all strategies."""
    print("\n" + "="*80)
    print("LIQUIDITY SWEEPS COMPARISON - LONDON KILLZONE (01:00-04:00)")
    print("="*80)
    print("Period: 2018-2025 | Risk: 20pt SL / 40pt TP (1:2 R/R)")
    print("="*80)
    
    print(f"\n{'Strategy':<35} {'Trades':<10} {'Win Rate':<12} {'PF':<10} {'Net PnL':<15}")
    print("-" * 80)
    
    for result in results:
        strategy = result['strategy']
        trades = result['num_trades']
        wr = f"{result['win_rate']:.2f}%"
        pf = f"{result['profit_factor']:.2f}" if result['profit_factor'] != float('inf') else "∞"
        pnl = f"{result['total_pnl']:.2f} pts"
        
        print(f"{strategy:<35} {trades:<10} {wr:<12} {pf:<10} {pnl:<15}")
    
    print("-" * 80)
    
    # Find best strategy
    best_pnl = max(results, key=lambda x: x['total_pnl'])
    best_wr = max(results, key=lambda x: x['win_rate'])
    best_pf = max(results, key=lambda x: x['profit_factor'] if x['profit_factor'] != float('inf') else 0)
    
    print("\n🏆 BEST PERFORMERS:")
    print(f"  Highest PnL: {best_pnl['strategy']} ({best_pnl['total_pnl']:.2f} pts)")
    print(f"  Highest Win Rate: {best_wr['strategy']} ({best_wr['win_rate']:.2f}%)")
    print(f"  Highest Profit Factor: {best_pf['strategy']} ({best_pf['profit_factor']:.2f})")
    
    print("\n" + "="*80)
    print("CONCLUSION: INTERNAL vs EXTERNAL LIQUIDITY")
    print("="*80)
    
    # Compare internal vs external
    swing_pnl = next((r['total_pnl'] for r in results if 'Swing Sweep' in r['strategy']), 0)
    fvg_pnl = next((r['total_pnl'] for r in results if 'FVG Tap' in r['strategy']), 0)
    combo_pnl = next((r['total_pnl'] for r in results if 'Combo' in r['strategy']), 0)
    
    print(f"\nExternal Liquidity (Swing Sweep): {swing_pnl:.2f} pts")
    print(f"Internal Liquidity (FVG Tap): {fvg_pnl:.2f} pts")
    print(f"Combined (Combo Sweep): {combo_pnl:.2f} pts")
    
    if fvg_pnl > swing_pnl:
        winner = "INTERNAL LIQUIDITY (FVG)"
        diff = ((fvg_pnl - swing_pnl) / abs(swing_pnl) * 100) if swing_pnl != 0 else 100
        print(f"\n✅ {winner} is more profitable by {diff:.1f}%")
    elif swing_pnl > fvg_pnl:
        winner = "EXTERNAL LIQUIDITY (Swing)"
        diff = ((swing_pnl - fvg_pnl) / abs(fvg_pnl) * 100) if fvg_pnl != 0 else 100
        print(f"\n✅ {winner} is more profitable by {diff:.1f}%")
    else:
        print("\n⚖️ Both liquidity types perform equally")
    
    print("\n" + "="*80)


# ============================
# MAIN
# ============================

def main():
    """Main execution."""
    print("="*80)
    print("LIQUIDITY SWEEPS BACKTEST - 3 STRATEGIES COMPARISON")
    print("="*80)
    
    base_path = "/home/runner/work/Backtest-Trading/Backtest-Trading"
    
    # Load data
    print("\n=== LOADING DATA ===")
    df_5m = load_nq_data(base_path, '5m')
    df_15m = load_nq_data(base_path, '15m')
    df_1h = load_nq_data(base_path, '1h')
    
    # Run all strategies
    print("\n=== RUNNING BACKTESTS ===")
    
    trades_a = strategy_a_swing_sweep(df_5m)
    trades_b = strategy_b_fvg_tap(df_5m, df_15m, df_1h)
    trades_c = strategy_c_combo_sweep(df_5m, df_15m, df_1h)
    
    # Calculate statistics
    results = [
        calculate_statistics(trades_a, "Strategy A: Swing Sweep"),
        calculate_statistics(trades_b, "Strategy B: FVG Tap & Go"),
        calculate_statistics(trades_c, "Strategy C: Combo Sweep")
    ]
    
    # Generate report
    generate_comparison_report(results)
    
    # Save trades
    all_trades = trades_a + trades_b + trades_c
    if len(all_trades) > 0:
        output_file = os.path.join(base_path, "liquidity_sweeps_trades.csv")
        trades_df = pd.DataFrame(all_trades)
        trades_df.to_csv(output_file, index=False)
        print(f"\nAll trades saved to: {output_file}")
    
    print("\n" + "="*80)
    print("BACKTEST COMPLETE")
    print("="*80)


if __name__ == "__main__":
    main()

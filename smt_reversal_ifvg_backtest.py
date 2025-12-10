"""
SMT Reversal with Inversion FVG Backtest - London Killzone
Strategy: ICT (Inner Circle Trader) - SMT + IFVG Reversal

Specific algorithmic logic:
1. Detect SMT divergence (NQ Lower Low + ES Higher Low)
2. Identify opposing FVG formed in 30min before the low
3. Entry when price closes above FVG within 45min after low
4. SL at absolute low, TP at 1:2 R/R
"""

import pandas as pd
import numpy as np
from datetime import datetime, time, timedelta
import glob
import os
from typing import Dict, List, Tuple, Optional

# ============================
# CONFIGURATION
# ============================

# Time Windows
LONDON_KILLZONE_START = time(1, 0)  # 01:00
LONDON_KILLZONE_END = time(4, 0)    # 04:00

# SMT Detection Parameters
SMT_LOOKBACK_MINUTES = 60  # 60 minutes for SMT divergence detection
SMT_LOOKBACK_CANDLES = 12  # 60 minutes = 12 x 5-minute candles

# FVG Search Parameters
FVG_SEARCH_MINUTES = 30  # Look back 30 minutes before low for FVG
FVG_SEARCH_CANDLES = 6  # 30 minutes = 6 x 5-minute candles

# Entry Trigger Parameters
ENTRY_TIMEOUT_MINUTES = 45  # Entry must occur within 45 minutes after low
ENTRY_TIMEOUT_CANDLES = 9  # 45 minutes = 9 x 5-minute candles

# Risk Management
RISK_REWARD_RATIO = 2.0  # 1:2 R/R


# ============================
# DATA LOADING (Reuse from previous implementation)
# ============================

def load_nq_data(base_path: str) -> pd.DataFrame:
    """Load and concatenate all NQ 5-minute CSV files."""
    print("Loading NQ data...")
    
    pattern = os.path.join(base_path, "*5m.csv")
    all_files = sorted(glob.glob(pattern))
    files = [f for f in all_files if 'ES' not in os.path.basename(f)]
    
    if not files:
        raise FileNotFoundError("No NQ 5-minute CSV files found")
    
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
    print(f"  Total NQ candles loaded: {len(nq_df)}")
    return nq_df


def load_es_data(base_path: str) -> pd.DataFrame:
    """Load and concatenate all ES 5-minute CSV files."""
    print("Loading ES data...")
    
    pattern = os.path.join(base_path, "ES 5m*.csv")
    files = sorted(glob.glob(pattern))
    
    if not files:
        raise FileNotFoundError("No ES 5-minute CSV files found")
    
    dfs = []
    for file in files:
        print(f"  Loading {os.path.basename(file)}")
        df = pd.read_csv(file, sep=';', header=0)
        df.columns = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
        dfs.append(df)
    
    es_df = pd.concat(dfs, ignore_index=True)
    es_df['DateTime'] = pd.to_datetime(es_df['Date'] + ' ' + es_df['Time'], 
                                        format='%d/%m/%Y %H:%M:%S')
    
    for col in ['Open', 'High', 'Low', 'Close']:
        es_df[col] = pd.to_numeric(es_df[col], errors='coerce')
    
    es_df = es_df.sort_values('DateTime').reset_index(drop=True)
    print(f"  Total ES candles loaded: {len(es_df)}")
    return es_df


def synchronize_data(nq_df: pd.DataFrame, es_df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Synchronize NQ and ES data on DateTime index."""
    print("Synchronizing NQ and ES data...")
    
    nq_indexed = nq_df.set_index('DateTime')
    es_indexed = es_df.set_index('DateTime')
    
    common_times = nq_indexed.index.intersection(es_indexed.index)
    print(f"  Common timestamps: {len(common_times)}")
    
    nq_sync = nq_indexed.loc[common_times].reset_index()
    es_sync = es_indexed.loc[common_times].reset_index()
    
    return nq_sync, es_sync


def filter_london_killzone(df: pd.DataFrame) -> pd.DataFrame:
    """Filter data to only include London Killzone hours (01:00 - 04:00)."""
    df['Hour'] = df['DateTime'].dt.hour
    mask = (df['Hour'] >= 1) & (df['Hour'] < 4)
    filtered = df[mask].copy()
    print(f"  London Killzone candles: {len(filtered)}")
    return filtered


# ============================
# FVG DETECTION
# ============================

def detect_bearish_fvg(df: pd.DataFrame, idx: int) -> Optional[Dict]:
    """
    Detect Bearish FVG at given index.
    Bearish FVG: Low[i-2] > High[i]
    Returns FVG zone or None.
    """
    if idx < 2:
        return None
    
    low_candle1 = df.iloc[idx-2]['Low']
    high_candle3 = df.iloc[idx]['High']
    
    if low_candle1 > high_candle3:
        return {
            'type': 'Bearish',
            'top': low_candle1,
            'bottom': high_candle3,
            'idx': idx,
            'datetime': df.iloc[idx]['DateTime']
        }
    
    return None


def detect_bullish_fvg(df: pd.DataFrame, idx: int) -> Optional[Dict]:
    """
    Detect Bullish FVG at given index.
    Bullish FVG: High[i-2] < Low[i]
    Returns FVG zone or None.
    """
    if idx < 2:
        return None
    
    high_candle1 = df.iloc[idx-2]['High']
    low_candle3 = df.iloc[idx]['Low']
    
    if high_candle1 < low_candle3:
        return {
            'type': 'Bullish',
            'top': low_candle3,
            'bottom': high_candle1,
            'idx': idx,
            'datetime': df.iloc[idx]['DateTime']
        }
    
    return None


# ============================
# SMT DIVERGENCE DETECTION
# ============================

def detect_smt_bullish(nq_df: pd.DataFrame, es_df: pd.DataFrame, idx: int) -> Optional[Dict]:
    """
    Detect Bullish SMT divergence at given index.
    
    Bullish SMT: NQ makes Lower Low WHILE ES makes Higher Low
    
    Returns dict with low info if SMT detected, None otherwise.
    """
    lookback_start = max(0, idx - SMT_LOOKBACK_CANDLES)
    
    if lookback_start >= idx - 1:
        return None
    
    try:
        # Get NQ lookback data
        nq_lookback = nq_df.iloc[lookback_start:idx]
        
        if len(nq_lookback) < 2:
            return None
        
        # Find current low and previous low in NQ
        nq_current_low = nq_df.iloc[idx]['Low']
        nq_prev_low = nq_lookback['Low'].min()
        
        # NQ must make a lower low
        if nq_current_low >= nq_prev_low:
            return None
        
        # Get corresponding ES data
        start_time = nq_df.iloc[lookback_start]['DateTime']
        end_time = nq_df.iloc[idx]['DateTime']
        
        es_lookback = es_df[(es_df['DateTime'] >= start_time) & 
                           (es_df['DateTime'] <= end_time)]
        
        if len(es_lookback) < 2:
            return None
        
        # Find current low and previous low in ES
        es_current_low = es_lookback.iloc[-1]['Low']
        es_prev_low = es_lookback.iloc[:-1]['Low'].min()
        
        # ES must make a higher low (or equal - allowing small tolerance)
        if es_current_low >= es_prev_low * 0.998:  # Allow 0.2% tolerance
            return {
                'type': 'Bullish_SMT',
                'nq_low': nq_current_low,
                'nq_low_idx': idx,
                'time_low': nq_df.iloc[idx]['DateTime'],
                'nq_prev_low': nq_prev_low,
                'es_current_low': es_current_low,
                'es_prev_low': es_prev_low
            }
    
    except (IndexError, KeyError, ValueError):
        return None
    
    return None


def detect_smt_bearish(nq_df: pd.DataFrame, es_df: pd.DataFrame, idx: int) -> Optional[Dict]:
    """
    Detect Bearish SMT divergence at given index.
    
    Bearish SMT: NQ makes Higher High WHILE ES makes Lower High
    
    Returns dict with high info if SMT detected, None otherwise.
    """
    lookback_start = max(0, idx - SMT_LOOKBACK_CANDLES)
    
    if lookback_start >= idx - 1:
        return None
    
    try:
        # Get NQ lookback data
        nq_lookback = nq_df.iloc[lookback_start:idx]
        
        if len(nq_lookback) < 2:
            return None
        
        # Find current high and previous high in NQ
        nq_current_high = nq_df.iloc[idx]['High']
        nq_prev_high = nq_lookback['High'].max()
        
        # NQ must make a higher high
        if nq_current_high <= nq_prev_high:
            return None
        
        # Get corresponding ES data
        start_time = nq_df.iloc[lookback_start]['DateTime']
        end_time = nq_df.iloc[idx]['DateTime']
        
        es_lookback = es_df[(es_df['DateTime'] >= start_time) & 
                           (es_df['DateTime'] <= end_time)]
        
        if len(es_lookback) < 2:
            return None
        
        # Find current high and previous high in ES
        es_current_high = es_lookback.iloc[-1]['High']
        es_prev_high = es_lookback.iloc[:-1]['High'].max()
        
        # ES must make a lower high (or equal - allowing small tolerance)
        if es_current_high <= es_prev_high * 1.002:  # Allow 0.2% tolerance
            return {
                'type': 'Bearish_SMT',
                'nq_high': nq_current_high,
                'nq_high_idx': idx,
                'time_high': nq_df.iloc[idx]['DateTime'],
                'nq_prev_high': nq_prev_high,
                'es_current_high': es_current_high,
                'es_prev_high': es_prev_high
            }
    
    except (IndexError, KeyError, ValueError):
        return None
    
    return None


# ============================
# FVG SEARCH IN WINDOW
# ============================

def find_last_fvg_before_low(nq_df: pd.DataFrame, smt_idx: int, fvg_type: str) -> Optional[Dict]:
    """
    Find the last FVG of specified type in the 30 minutes BEFORE the SMT low/high.
    
    For LONG setup: Look for last Bearish FVG before the low
    For SHORT setup: Look for last Bullish FVG before the high
    """
    # Search window: 30 minutes before SMT point
    search_start = max(0, smt_idx - FVG_SEARCH_CANDLES)
    
    if search_start >= smt_idx:
        return None
    
    # Search backwards from SMT point
    for idx in range(smt_idx - 1, search_start - 1, -1):
        if fvg_type == 'Bearish':
            fvg = detect_bearish_fvg(nq_df, idx)
        else:  # Bullish
            fvg = detect_bullish_fvg(nq_df, idx)
        
        if fvg is not None:
            return fvg
    
    return None


# ============================
# ENTRY TRIGGER
# ============================

def check_entry_trigger_long(nq_df: pd.DataFrame, smt_idx: int, fvg: Dict) -> Optional[Dict]:
    """
    Check if price closes above FVG top within timeout period after SMT low.
    
    Returns entry details if triggered, None otherwise.
    """
    # Monitor price for ENTRY_TIMEOUT_CANDLES after SMT low
    max_idx = min(smt_idx + ENTRY_TIMEOUT_CANDLES, len(nq_df) - 1)
    
    for idx in range(smt_idx + 1, max_idx + 1):
        close = nq_df.iloc[idx]['Close']
        
        # Entry trigger: Close strictly above FVG top
        if close > fvg['top']:
            return {
                'entry_idx': idx,
                'entry_price': close,
                'entry_datetime': nq_df.iloc[idx]['DateTime']
            }
    
    return None


def check_entry_trigger_short(nq_df: pd.DataFrame, smt_idx: int, fvg: Dict) -> Optional[Dict]:
    """
    Check if price closes below FVG bottom within timeout period after SMT high.
    
    Returns entry details if triggered, None otherwise.
    """
    # Monitor price for ENTRY_TIMEOUT_CANDLES after SMT high
    max_idx = min(smt_idx + ENTRY_TIMEOUT_CANDLES, len(nq_df) - 1)
    
    for idx in range(smt_idx + 1, max_idx + 1):
        close = nq_df.iloc[idx]['Close']
        
        # Entry trigger: Close strictly below FVG bottom
        if close < fvg['bottom']:
            return {
                'entry_idx': idx,
                'entry_price': close,
                'entry_datetime': nq_df.iloc[idx]['DateTime']
            }
    
    return None


# ============================
# TRADE SIMULATION
# ============================

def simulate_trade_smt(nq_df: pd.DataFrame, entry_idx: int, entry_price: float,
                       direction: str, stop_loss: float, take_profit: float) -> Dict:
    """
    Simulate trade with dynamic SL/TP levels.
    
    Returns trade result.
    """
    # Check subsequent candles for SL or TP hit
    for i in range(entry_idx + 1, len(nq_df)):
        candle = nq_df.iloc[i]
        
        if direction == 'LONG':
            # Check if stopped out
            if candle['Low'] <= stop_loss:
                pnl = stop_loss - entry_price
                return {
                    'outcome': 'LOSS',
                    'pnl': pnl,
                    'pnl_percent': (pnl / (entry_price - stop_loss)) * 100,
                    'exit_idx': i,
                    'exit_price': stop_loss,
                    'exit_datetime': candle['DateTime']
                }
            # Check if take profit hit
            if candle['High'] >= take_profit:
                pnl = take_profit - entry_price
                return {
                    'outcome': 'WIN',
                    'pnl': pnl,
                    'pnl_percent': (pnl / (entry_price - stop_loss)) * 100,
                    'exit_idx': i,
                    'exit_price': take_profit,
                    'exit_datetime': candle['DateTime']
                }
        
        else:  # SHORT
            # Check if stopped out
            if candle['High'] >= stop_loss:
                pnl = entry_price - stop_loss
                return {
                    'outcome': 'LOSS',
                    'pnl': pnl,
                    'pnl_percent': (pnl / (stop_loss - entry_price)) * 100,
                    'exit_idx': i,
                    'exit_price': stop_loss,
                    'exit_datetime': candle['DateTime']
                }
            # Check if take profit hit
            if candle['Low'] <= take_profit:
                pnl = entry_price - take_profit
                return {
                    'outcome': 'WIN',
                    'pnl': pnl,
                    'pnl_percent': (pnl / (stop_loss - entry_price)) * 100,
                    'exit_idx': i,
                    'exit_price': take_profit,
                    'exit_datetime': candle['DateTime']
                }
    
    # If we reach end of data, close at last candle
    last_candle = nq_df.iloc[-1]
    exit_price = last_candle['Close']
    
    if direction == 'LONG':
        pnl = exit_price - entry_price
    else:
        pnl = entry_price - exit_price
    
    return {
        'outcome': 'OPEN',
        'pnl': pnl,
        'pnl_percent': 0,
        'exit_idx': len(nq_df) - 1,
        'exit_price': exit_price,
        'exit_datetime': last_candle['DateTime']
    }


# ============================
# BACKTEST ENGINE
# ============================

def run_smt_reversal_backtest(nq_df: pd.DataFrame, es_df: pd.DataFrame) -> List[Dict]:
    """
    Run the SMT Reversal with Inversion FVG backtest.
    """
    print("\nRunning SMT Reversal + IFVG Backtest...")
    
    trades = []
    
    # Iterate through NQ data looking for SMT setups
    for idx in range(SMT_LOOKBACK_CANDLES + FVG_SEARCH_CANDLES, len(nq_df) - ENTRY_TIMEOUT_CANDLES):
        
        # Check for LONG setup (Bullish SMT)
        smt_bullish = detect_smt_bullish(nq_df, es_df, idx)
        
        if smt_bullish is not None:
            # Find last Bearish FVG before the low
            fvg = find_last_fvg_before_low(nq_df, idx, 'Bearish')
            
            if fvg is not None:
                # Check for entry trigger
                entry = check_entry_trigger_long(nq_df, idx, fvg)
                
                if entry is not None:
                    # Calculate SL and TP
                    entry_price = entry['entry_price']
                    stop_loss = smt_bullish['nq_low']
                    risk = entry_price - stop_loss
                    take_profit = entry_price + (risk * RISK_REWARD_RATIO)
                    
                    # Only take trade if risk is positive
                    if risk > 0:
                        # Simulate trade
                        result = simulate_trade_smt(nq_df, entry['entry_idx'], 
                                                    entry_price, 'LONG', 
                                                    stop_loss, take_profit)
                        
                        # Record trade
                        trade_record = {
                            'direction': 'LONG',
                            'smt_datetime': smt_bullish['time_low'],
                            'smt_idx': idx,
                            'fvg_type': fvg['type'],
                            'fvg_top': fvg['top'],
                            'fvg_bottom': fvg['bottom'],
                            'entry_datetime': entry['entry_datetime'],
                            'entry_idx': entry['entry_idx'],
                            'entry_price': entry_price,
                            'stop_loss': stop_loss,
                            'take_profit': take_profit,
                            'risk': risk,
                            'reward': risk * RISK_REWARD_RATIO,
                            'exit_datetime': result['exit_datetime'],
                            'exit_price': result['exit_price'],
                            'pnl': result['pnl'],
                            'outcome': result['outcome']
                        }
                        
                        trades.append(trade_record)
        
        # Check for SHORT setup (Bearish SMT)
        smt_bearish = detect_smt_bearish(nq_df, es_df, idx)
        
        if smt_bearish is not None:
            # Find last Bullish FVG before the high
            fvg = find_last_fvg_before_low(nq_df, idx, 'Bullish')
            
            if fvg is not None:
                # Check for entry trigger
                entry = check_entry_trigger_short(nq_df, idx, fvg)
                
                if entry is not None:
                    # Calculate SL and TP
                    entry_price = entry['entry_price']
                    stop_loss = smt_bearish['nq_high']
                    risk = stop_loss - entry_price
                    take_profit = entry_price - (risk * RISK_REWARD_RATIO)
                    
                    # Only take trade if risk is positive
                    if risk > 0:
                        # Simulate trade
                        result = simulate_trade_smt(nq_df, entry['entry_idx'],
                                                    entry_price, 'SHORT',
                                                    stop_loss, take_profit)
                        
                        # Record trade
                        trade_record = {
                            'direction': 'SHORT',
                            'smt_datetime': smt_bearish['time_high'],
                            'smt_idx': idx,
                            'fvg_type': fvg['type'],
                            'fvg_top': fvg['top'],
                            'fvg_bottom': fvg['bottom'],
                            'entry_datetime': entry['entry_datetime'],
                            'entry_idx': entry['entry_idx'],
                            'entry_price': entry_price,
                            'stop_loss': stop_loss,
                            'take_profit': take_profit,
                            'risk': risk,
                            'reward': risk * RISK_REWARD_RATIO,
                            'exit_datetime': result['exit_datetime'],
                            'exit_price': result['exit_price'],
                            'pnl': result['pnl'],
                            'outcome': result['outcome']
                        }
                        
                        trades.append(trade_record)
    
    print(f"  Total trades found: {len(trades)}")
    
    return trades


# ============================
# REPORTING
# ============================

def calculate_statistics(trades: List[Dict]) -> Dict:
    """Calculate performance statistics."""
    if len(trades) == 0:
        return {
            'num_trades': 0,
            'win_rate': 0,
            'profit_factor': 0,
            'total_pnl': 0,
            'avg_win': 0,
            'avg_loss': 0,
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
    
    avg_win = wins.mean() if len(wins) > 0 else 0
    avg_loss = losses.mean() if len(losses) > 0 else 0
    
    return {
        'num_trades': len(trades),
        'win_rate': win_rate,
        'profit_factor': profit_factor,
        'total_pnl': total_pnl,
        'gross_profit': gross_profit,
        'gross_loss': gross_loss,
        'avg_win': avg_win,
        'avg_loss': avg_loss,
        'num_wins': num_wins,
        'num_losses': num_losses
    }


def generate_report(smt_stats: Dict, simple_ifvg_stats: Dict = None):
    """Generate comparison report."""
    print("\n" + "="*80)
    print("SMT REVERSAL + INVERSION FVG BACKTEST RESULTS")
    print("="*80)
    print("Strategy: SMT Divergence + Opposing FVG Inversion")
    print("Session: London Killzone (01:00-04:00)")
    print("Period: 2018-2025")
    print("="*80)
    
    print("\n📊 SMT REVERSAL STRATEGY:")
    print(f"  Number of Trades: {smt_stats['num_trades']}")
    print(f"  Wins: {smt_stats['num_wins']} | Losses: {smt_stats['num_losses']}")
    print(f"  Win Rate: {smt_stats['win_rate']:.2f}%")
    print(f"  Profit Factor: {smt_stats['profit_factor']:.2f}")
    print(f"  Total PnL: {smt_stats['total_pnl']:.2f} points")
    print(f"  Gross Profit: {smt_stats['gross_profit']:.2f} points")
    print(f"  Gross Loss: {smt_stats['gross_loss']:.2f} points")
    print(f"  Average Win: {smt_stats['avg_win']:.2f} points")
    print(f"  Average Loss: {smt_stats['avg_loss']:.2f} points")
    
    if simple_ifvg_stats is not None:
        print("\n" + "-"*80)
        print("📊 COMPARISON WITH SIMPLE IFVG (from previous backtest):")
        print("-"*80)
        
        print(f"\n{'Metric':<25} {'SMT Reversal':<20} {'Simple IFVG':<20}")
        print("-"*80)
        print(f"{'Number of Trades':<25} {smt_stats['num_trades']:<20} {simple_ifvg_stats['num_trades']:<20}")
        print(f"{'Win Rate':<25} {smt_stats['win_rate']:.2f}%{' '*14} {simple_ifvg_stats['win_rate']:.2f}%")
        print(f"{'Profit Factor':<25} {smt_stats['profit_factor']:.2f}{' '*16} {simple_ifvg_stats['profit_factor']:.2f}")
        print(f"{'Total PnL (pts)':<25} {smt_stats['total_pnl']:.2f}{' '*14} {simple_ifvg_stats['total_pnl']:.2f}")
        
        # Calculate improvements
        if simple_ifvg_stats['win_rate'] > 0:
            wr_improvement = smt_stats['win_rate'] - simple_ifvg_stats['win_rate']
            print(f"\n🎯 Win Rate Change: {wr_improvement:+.2f} percentage points")
        
        if simple_ifvg_stats['profit_factor'] > 0:
            pf_improvement = smt_stats['profit_factor'] - simple_ifvg_stats['profit_factor']
            print(f"🎯 Profit Factor Change: {pf_improvement:+.2f}")
    
    print("\n" + "="*80)


def save_trades_to_csv(trades: List[Dict], output_path: str):
    """Save trades to CSV."""
    if len(trades) > 0:
        trades_df = pd.DataFrame(trades)
        trades_df.to_csv(output_path, index=False)
        print(f"\nTrades saved to: {output_path}")


# ============================
# MAIN
# ============================

def main():
    """Main execution function."""
    print("="*80)
    print("SMT REVERSAL + INVERSION FVG BACKTEST")
    print("ICT Methodology - London Killzone")
    print("="*80)
    
    base_path = "/home/runner/work/Backtest-Trading/Backtest-Trading"
    
    # Load data
    print("\n=== LOADING DATA ===")
    nq_df = load_nq_data(base_path)
    es_df = load_es_data(base_path)
    
    # Synchronize
    print("\n=== SYNCHRONIZING DATA ===")
    nq_df, es_df = synchronize_data(nq_df, es_df)
    
    # Filter London Killzone
    print("\n=== FILTERING LONDON KILLZONE ===")
    nq_df = filter_london_killzone(nq_df)
    es_df = filter_london_killzone(es_df)
    
    # Run backtest
    print("\n=== RUNNING SMT REVERSAL BACKTEST ===")
    trades = run_smt_reversal_backtest(nq_df, es_df)
    
    # Calculate statistics
    smt_stats = calculate_statistics(trades)
    
    # Load simple IFVG results if available for comparison
    simple_ifvg_stats = None
    simple_ifvg_path = os.path.join(base_path, "ifvg_backtest_trades.csv")
    
    if os.path.exists(simple_ifvg_path):
        print("\n=== LOADING SIMPLE IFVG RESULTS FOR COMPARISON ===")
        simple_df = pd.read_csv(simple_ifvg_path)
        # Filter to base strategy only
        simple_base = simple_df[simple_df['scenario'] == '1. IFVG Base (Trigger Only)']
        
        if len(simple_base) > 0:
            num_wins = len(simple_base[simple_base['outcome'] == 'WIN'])
            num_losses = len(simple_base[simple_base['outcome'] == 'LOSS'])
            win_rate = (num_wins / len(simple_base)) * 100
            total_pnl = simple_base['pnl'].sum()
            
            wins = simple_base[simple_base['outcome'] == 'WIN']['pnl']
            losses = simple_base[simple_base['outcome'] == 'LOSS']['pnl']
            
            gross_profit = wins.sum() if len(wins) > 0 else 0
            gross_loss = abs(losses.sum()) if len(losses) > 0 else 0
            profit_factor = gross_profit / gross_loss if gross_loss != 0 else 0
            
            simple_ifvg_stats = {
                'num_trades': len(simple_base),
                'win_rate': win_rate,
                'profit_factor': profit_factor,
                'total_pnl': total_pnl
            }
    
    # Generate report
    print("\n=== GENERATING REPORT ===")
    generate_report(smt_stats, simple_ifvg_stats)
    
    # Save trades
    output_file = os.path.join(base_path, "smt_reversal_trades.csv")
    save_trades_to_csv(trades, output_file)
    
    print("\n" + "="*80)
    print("BACKTEST COMPLETE")
    print("="*80)


if __name__ == "__main__":
    main()

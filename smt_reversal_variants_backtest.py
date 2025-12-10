"""
SMT Reversal with Multiple SL/TP Variants - London Killzone
Strategy: ICT (Inner Circle Trader) - SMT + IFVG Reversal

Testing different Stop Loss and Take Profit configurations:
- SL Option 1: Under entry candle (reversal candle)
- SL Option 2: At swing extremity (SMT low/high)
- TP Options: 1:1 R/R, 1.5:1 R/R, 2:1 R/R
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

# Risk Management Variants
RR_RATIOS = [1.0, 1.5, 2.0]  # Test 1:1, 1.5:1, and 2:1 R/R


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
    """Detect Bearish FVG at given index."""
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
    """Detect Bullish FVG at given index."""
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
    """Detect Bullish SMT divergence: NQ Lower Low + ES Higher Low."""
    lookback_start = max(0, idx - SMT_LOOKBACK_CANDLES)
    
    if lookback_start >= idx - 1:
        return None
    
    try:
        nq_lookback = nq_df.iloc[lookback_start:idx]
        
        if len(nq_lookback) < 2:
            return None
        
        nq_current_low = nq_df.iloc[idx]['Low']
        nq_prev_low = nq_lookback['Low'].min()
        
        if nq_current_low >= nq_prev_low:
            return None
        
        start_time = nq_df.iloc[lookback_start]['DateTime']
        end_time = nq_df.iloc[idx]['DateTime']
        
        es_lookback = es_df[(es_df['DateTime'] >= start_time) & 
                           (es_df['DateTime'] <= end_time)]
        
        if len(es_lookback) < 2:
            return None
        
        es_current_low = es_lookback.iloc[-1]['Low']
        es_prev_low = es_lookback.iloc[:-1]['Low'].min()
        
        if es_current_low >= es_prev_low * 0.998:
            return {
                'type': 'Bullish_SMT',
                'nq_low': nq_current_low,
                'nq_low_idx': idx,
                'time_low': nq_df.iloc[idx]['DateTime']
            }
    
    except (IndexError, KeyError, ValueError):
        return None
    
    return None


def detect_smt_bearish(nq_df: pd.DataFrame, es_df: pd.DataFrame, idx: int) -> Optional[Dict]:
    """Detect Bearish SMT divergence: NQ Higher High + ES Lower High."""
    lookback_start = max(0, idx - SMT_LOOKBACK_CANDLES)
    
    if lookback_start >= idx - 1:
        return None
    
    try:
        nq_lookback = nq_df.iloc[lookback_start:idx]
        
        if len(nq_lookback) < 2:
            return None
        
        nq_current_high = nq_df.iloc[idx]['High']
        nq_prev_high = nq_lookback['High'].max()
        
        if nq_current_high <= nq_prev_high:
            return None
        
        start_time = nq_df.iloc[lookback_start]['DateTime']
        end_time = nq_df.iloc[idx]['DateTime']
        
        es_lookback = es_df[(es_df['DateTime'] >= start_time) & 
                           (es_df['DateTime'] <= end_time)]
        
        if len(es_lookback) < 2:
            return None
        
        es_current_high = es_lookback.iloc[-1]['High']
        es_prev_high = es_lookback.iloc[:-1]['High'].max()
        
        if es_current_high <= es_prev_high * 1.002:
            return {
                'type': 'Bearish_SMT',
                'nq_high': nq_current_high,
                'nq_high_idx': idx,
                'time_high': nq_df.iloc[idx]['DateTime']
            }
    
    except (IndexError, KeyError, ValueError):
        return None
    
    return None


# ============================
# FVG SEARCH
# ============================

def find_last_fvg_before_low(nq_df: pd.DataFrame, smt_idx: int, fvg_type: str) -> Optional[Dict]:
    """Find the last FVG of specified type in the 30 minutes BEFORE the SMT low/high."""
    search_start = max(0, smt_idx - FVG_SEARCH_CANDLES)
    
    if search_start >= smt_idx:
        return None
    
    for idx in range(smt_idx - 1, search_start - 1, -1):
        if fvg_type == 'Bearish':
            fvg = detect_bearish_fvg(nq_df, idx)
        else:
            fvg = detect_bullish_fvg(nq_df, idx)
        
        if fvg is not None:
            return fvg
    
    return None


# ============================
# ENTRY TRIGGER
# ============================

def check_entry_trigger_long(nq_df: pd.DataFrame, smt_idx: int, fvg: Dict) -> Optional[Dict]:
    """Check if price closes above FVG top within timeout period after SMT low."""
    max_idx = min(smt_idx + ENTRY_TIMEOUT_CANDLES, len(nq_df) - 1)
    
    for idx in range(smt_idx + 1, max_idx + 1):
        close = nq_df.iloc[idx]['Close']
        
        if close > fvg['top']:
            return {
                'entry_idx': idx,
                'entry_price': close,
                'entry_datetime': nq_df.iloc[idx]['DateTime'],
                'entry_candle_low': nq_df.iloc[idx]['Low'],
                'entry_candle_high': nq_df.iloc[idx]['High']
            }
    
    return None


def check_entry_trigger_short(nq_df: pd.DataFrame, smt_idx: int, fvg: Dict) -> Optional[Dict]:
    """Check if price closes below FVG bottom within timeout period after SMT high."""
    max_idx = min(smt_idx + ENTRY_TIMEOUT_CANDLES, len(nq_df) - 1)
    
    for idx in range(smt_idx + 1, max_idx + 1):
        close = nq_df.iloc[idx]['Close']
        
        if close < fvg['bottom']:
            return {
                'entry_idx': idx,
                'entry_price': close,
                'entry_datetime': nq_df.iloc[idx]['DateTime'],
                'entry_candle_low': nq_df.iloc[idx]['Low'],
                'entry_candle_high': nq_df.iloc[idx]['High']
            }
    
    return None


# ============================
# TRADE SIMULATION
# ============================

def simulate_trade_smt(nq_df: pd.DataFrame, entry_idx: int, entry_price: float,
                       direction: str, stop_loss: float, take_profit: float) -> Dict:
    """Simulate trade with dynamic SL/TP levels."""
    for i in range(entry_idx + 1, len(nq_df)):
        candle = nq_df.iloc[i]
        
        if direction == 'LONG':
            if candle['Low'] <= stop_loss:
                pnl = stop_loss - entry_price
                return {
                    'outcome': 'LOSS',
                    'pnl': pnl,
                    'exit_idx': i,
                    'exit_price': stop_loss,
                    'exit_datetime': candle['DateTime']
                }
            if candle['High'] >= take_profit:
                pnl = take_profit - entry_price
                return {
                    'outcome': 'WIN',
                    'pnl': pnl,
                    'exit_idx': i,
                    'exit_price': take_profit,
                    'exit_datetime': candle['DateTime']
                }
        
        else:  # SHORT
            if candle['High'] >= stop_loss:
                pnl = entry_price - stop_loss
                return {
                    'outcome': 'LOSS',
                    'pnl': pnl,
                    'exit_idx': i,
                    'exit_price': stop_loss,
                    'exit_datetime': candle['DateTime']
                }
            if candle['Low'] <= take_profit:
                pnl = entry_price - take_profit
                return {
                    'outcome': 'WIN',
                    'pnl': pnl,
                    'exit_idx': i,
                    'exit_price': take_profit,
                    'exit_datetime': candle['DateTime']
                }
    
    # Close at last candle
    last_candle = nq_df.iloc[-1]
    exit_price = last_candle['Close']
    
    if direction == 'LONG':
        pnl = exit_price - entry_price
    else:
        pnl = entry_price - exit_price
    
    return {
        'outcome': 'OPEN',
        'pnl': pnl,
        'exit_idx': len(nq_df) - 1,
        'exit_price': exit_price,
        'exit_datetime': last_candle['DateTime']
    }


# ============================
# BACKTEST ENGINE WITH VARIANTS
# ============================

def run_smt_reversal_variant(nq_df: pd.DataFrame, es_df: pd.DataFrame,
                             sl_type: str, rr_ratio: float) -> List[Dict]:
    """
    Run SMT Reversal backtest with specific SL/TP configuration.
    
    sl_type: 'entry_candle' or 'swing_extremity'
    rr_ratio: 1.0, 1.5, or 2.0
    """
    trades = []
    
    for idx in range(SMT_LOOKBACK_CANDLES + FVG_SEARCH_CANDLES, len(nq_df) - ENTRY_TIMEOUT_CANDLES):
        
        # LONG setups
        smt_bullish = detect_smt_bullish(nq_df, es_df, idx)
        
        if smt_bullish is not None:
            fvg = find_last_fvg_before_low(nq_df, idx, 'Bearish')
            
            if fvg is not None:
                entry = check_entry_trigger_long(nq_df, idx, fvg)
                
                if entry is not None:
                    entry_price = entry['entry_price']
                    
                    # Calculate SL based on type
                    if sl_type == 'entry_candle':
                        stop_loss = entry['entry_candle_low']
                    else:  # swing_extremity
                        stop_loss = smt_bullish['nq_low']
                    
                    risk = entry_price - stop_loss
                    
                    if risk > 0:
                        take_profit = entry_price + (risk * rr_ratio)
                        
                        result = simulate_trade_smt(nq_df, entry['entry_idx'], 
                                                    entry_price, 'LONG', 
                                                    stop_loss, take_profit)
                        
                        trade_record = {
                            'direction': 'LONG',
                            'sl_type': sl_type,
                            'rr_ratio': rr_ratio,
                            'smt_datetime': smt_bullish['time_low'],
                            'entry_datetime': entry['entry_datetime'],
                            'entry_price': entry_price,
                            'stop_loss': stop_loss,
                            'take_profit': take_profit,
                            'risk': risk,
                            'reward': risk * rr_ratio,
                            'exit_datetime': result['exit_datetime'],
                            'exit_price': result['exit_price'],
                            'pnl': result['pnl'],
                            'outcome': result['outcome']
                        }
                        
                        trades.append(trade_record)
        
        # SHORT setups
        smt_bearish = detect_smt_bearish(nq_df, es_df, idx)
        
        if smt_bearish is not None:
            fvg = find_last_fvg_before_low(nq_df, idx, 'Bullish')
            
            if fvg is not None:
                entry = check_entry_trigger_short(nq_df, idx, fvg)
                
                if entry is not None:
                    entry_price = entry['entry_price']
                    
                    # Calculate SL based on type
                    if sl_type == 'entry_candle':
                        stop_loss = entry['entry_candle_high']
                    else:  # swing_extremity
                        stop_loss = smt_bearish['nq_high']
                    
                    risk = stop_loss - entry_price
                    
                    if risk > 0:
                        take_profit = entry_price - (risk * rr_ratio)
                        
                        result = simulate_trade_smt(nq_df, entry['entry_idx'],
                                                    entry_price, 'SHORT',
                                                    stop_loss, take_profit)
                        
                        trade_record = {
                            'direction': 'SHORT',
                            'sl_type': sl_type,
                            'rr_ratio': rr_ratio,
                            'smt_datetime': smt_bearish['time_high'],
                            'entry_datetime': entry['entry_datetime'],
                            'entry_price': entry_price,
                            'stop_loss': stop_loss,
                            'take_profit': take_profit,
                            'risk': risk,
                            'reward': risk * rr_ratio,
                            'exit_datetime': result['exit_datetime'],
                            'exit_price': result['exit_price'],
                            'pnl': result['pnl'],
                            'outcome': result['outcome']
                        }
                        
                        trades.append(trade_record)
    
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


def generate_comparison_report(all_results: Dict[str, Dict]):
    """Generate comprehensive comparison report."""
    print("\n" + "="*80)
    print("SMT REVERSAL - SL/TP VARIANTS COMPARISON")
    print("="*80)
    print("Session: London Killzone (01:00-04:00)")
    print("Period: 2018-2025")
    print("="*80)
    
    print(f"\n{'Variant':<40} {'Trades':<10} {'Win Rate':<12} {'PF':<8} {'Total PnL':<15}")
    print("-" * 80)
    
    for variant_name, stats in all_results.items():
        trades = stats['num_trades']
        wr = f"{stats['win_rate']:.2f}%"
        pf = f"{stats['profit_factor']:.2f}"
        pnl = f"{stats['total_pnl']:.2f} pts"
        
        print(f"{variant_name:<40} {trades:<10} {wr:<12} {pf:<8} {pnl:<15}")
    
    print("-" * 80)
    
    # Find best variants
    print("\n🏆 BEST PERFORMERS:")
    
    best_pnl_variant = max(all_results.items(), key=lambda x: x[1]['total_pnl'])
    print(f"  Highest PnL: {best_pnl_variant[0]} ({best_pnl_variant[1]['total_pnl']:.2f} pts)")
    
    best_wr_variant = max(all_results.items(), key=lambda x: x[1]['win_rate'])
    print(f"  Highest Win Rate: {best_wr_variant[0]} ({best_wr_variant[1]['win_rate']:.2f}%)")
    
    best_pf_variant = max(all_results.items(), key=lambda x: x[1]['profit_factor'] if x[1]['profit_factor'] != float('inf') else 0)
    print(f"  Highest Profit Factor: {best_pf_variant[0]} ({best_pf_variant[1]['profit_factor']:.2f})")
    
    print("\n" + "="*80)


# ============================
# MAIN
# ============================

def main():
    """Main execution function."""
    print("="*80)
    print("SMT REVERSAL - TESTING MULTIPLE SL/TP VARIANTS")
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
    
    # Test all variants
    print("\n=== RUNNING BACKTEST VARIANTS ===")
    
    all_results = {}
    all_trades = []
    
    sl_types = [
        ('entry_candle', 'SL: Entry Candle'),
        ('swing_extremity', 'SL: Swing Extremity')
    ]
    
    for sl_type, sl_label in sl_types:
        for rr_ratio in RR_RATIOS:
            variant_name = f"{sl_label} | TP: {rr_ratio}:1 R/R"
            
            print(f"\n  Testing: {variant_name}")
            trades = run_smt_reversal_variant(nq_df, es_df, sl_type, rr_ratio)
            print(f"    Trades found: {len(trades)}")
            
            stats = calculate_statistics(trades)
            all_results[variant_name] = stats
            
            # Add variant name to trades for CSV export
            for trade in trades:
                trade['variant'] = variant_name
                all_trades.append(trade)
    
    # Generate report
    print("\n=== GENERATING COMPARISON REPORT ===")
    generate_comparison_report(all_results)
    
    # Save all trades
    output_file = os.path.join(base_path, "smt_reversal_variants_trades.csv")
    if len(all_trades) > 0:
        trades_df = pd.DataFrame(all_trades)
        trades_df.to_csv(output_file, index=False)
        print(f"\nAll trades saved to: {output_file}")
    
    print("\n" + "="*80)
    print("BACKTEST COMPLETE")
    print("="*80)


if __name__ == "__main__":
    main()

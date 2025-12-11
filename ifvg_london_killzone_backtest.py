"""
IFVG (Inversion Fair Value Gap) Backtest - London Killzone
Strategy: ICT (Inner Circle Trader) Methodology

Backtest an IFVG strategy during London Killzone (01:00-04:00) with:
- FVG detection and inversion triggers
- Multiple confluence filters (Displacement, MSS, SMT Divergence)
- 5 scenario comparisons
- Risk management: 20pt SL, 40pt TP (1:2 R/R)
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

# Risk Management Parameters
STOP_LOSS_POINTS = 20
TAKE_PROFIT_POINTS = 40

# Time Windows
LONDON_KILLZONE_START = time(1, 0)  # 01:00
LONDON_KILLZONE_END = time(4, 0)    # 04:00
FVG_RECENCY_MINUTES = 60  # FVG must be created within last 60 minutes
FVG_RECENCY_CANDLES = 12  # 60 minutes = 12 x 5-minute candles

# Filters
DISPLACEMENT_THRESHOLD = 0.6  # Body must be > 60% of range
MSS_LOOKBACK_CANDLES = 12  # 1 hour lookback for swing high/low
SMT_LOOKBACK_CANDLES = 12  # 60 minutes for SMT divergence analysis
SMT_TOLERANCE = 0.002  # 0.2% tolerance for double tops/bottoms in SMT divergence


# ============================
# DATA LOADING
# ============================

def load_nq_data(base_path: str) -> pd.DataFrame:
    """
    Load and concatenate all NQ 5-minute CSV files from 2018-2025.
    
    CSV Format: Column1;Column2;Column3;Column4;Column5;Column6;Column7
    Where: Date;Time;Open;High;Low;Close;Volume
    """
    print("Loading NQ data...")
    
    # Find all 5m CSV files (excluding ES files)
    pattern = os.path.join(base_path, "*5m.csv")
    all_files = sorted(glob.glob(pattern))
    
    # Filter to only NQ files (exclude ES)
    files = [f for f in all_files if 'ES' not in os.path.basename(f)]
    
    if not files:
        raise FileNotFoundError("No NQ 5-minute CSV files found in the specified path")
    
    dfs = []
    for file in files:
        print(f"  Loading {os.path.basename(file)}")
        df = pd.read_csv(file, sep=';', header=0)
        
        # Rename columns
        df.columns = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
        
        dfs.append(df)
    
    # Concatenate all dataframes
    nq_df = pd.concat(dfs, ignore_index=True)
    
    # Create datetime index
    nq_df['DateTime'] = pd.to_datetime(nq_df['Date'] + ' ' + nq_df['Time'], 
                                        format='%d/%m/%Y %H:%M:%S')
    
    # Convert price columns to float
    for col in ['Open', 'High', 'Low', 'Close']:
        nq_df[col] = pd.to_numeric(nq_df[col], errors='coerce')
    
    # Sort by datetime and reset index
    nq_df = nq_df.sort_values('DateTime').reset_index(drop=True)
    
    print(f"  Total NQ candles loaded: {len(nq_df)}")
    return nq_df


def load_es_data(base_path: str) -> pd.DataFrame:
    """
    Load and concatenate all ES 5-minute CSV files from 2018-2025.
    """
    print("Loading ES data...")
    
    # Find all ES 5m CSV files
    pattern = os.path.join(base_path, "ES 5m*.csv")
    files = sorted(glob.glob(pattern))
    
    if not files:
        raise FileNotFoundError("No ES 5-minute CSV files found in the specified path")
    
    dfs = []
    for file in files:
        print(f"  Loading {os.path.basename(file)}")
        df = pd.read_csv(file, sep=';', header=0)
        
        # Rename columns
        df.columns = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
        
        dfs.append(df)
    
    # Concatenate all dataframes
    es_df = pd.concat(dfs, ignore_index=True)
    
    # Create datetime index
    es_df['DateTime'] = pd.to_datetime(es_df['Date'] + ' ' + es_df['Time'], 
                                        format='%d/%m/%Y %H:%M:%S')
    
    # Convert price columns to float
    for col in ['Open', 'High', 'Low', 'Close']:
        es_df[col] = pd.to_numeric(es_df[col], errors='coerce')
    
    # Sort by datetime and reset index
    es_df = es_df.sort_values('DateTime').reset_index(drop=True)
    
    print(f"  Total ES candles loaded: {len(es_df)}")
    return es_df


def synchronize_data(nq_df: pd.DataFrame, es_df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Synchronize NQ and ES data on DateTime index.
    Only keep candles that exist in both datasets.
    """
    print("Synchronizing NQ and ES data...")
    
    # Set DateTime as index for both
    nq_indexed = nq_df.set_index('DateTime')
    es_indexed = es_df.set_index('DateTime')
    
    # Find common timestamps
    common_times = nq_indexed.index.intersection(es_indexed.index)
    
    print(f"  Common timestamps: {len(common_times)}")
    
    # Filter both dataframes to common times
    nq_sync = nq_indexed.loc[common_times].reset_index()
    es_sync = es_indexed.loc[common_times].reset_index()
    
    return nq_sync, es_sync


def filter_london_killzone(df: pd.DataFrame) -> pd.DataFrame:
    """
    Filter data to only include London Killzone hours (01:00 - 04:00).
    """
    df['Hour'] = df['DateTime'].dt.hour
    df['Minute'] = df['DateTime'].dt.minute
    
    # Filter for 01:00 to 04:00 (inclusive of 01:00, exclusive of 04:00)
    mask = (df['Hour'] >= 1) & (df['Hour'] < 4)
    
    filtered = df[mask].copy()
    print(f"  London Killzone candles: {len(filtered)}")
    
    return filtered


# ============================
# FVG DETECTION
# ============================

def detect_fvgs(df: pd.DataFrame) -> pd.DataFrame:
    """
    Detect Fair Value Gaps (FVG) in the dataframe.
    
    Bearish FVG: Low[i-2] > High[i] (Gap between candle 1 and candle 3)
    Bullish FVG: High[i-2] < Low[i] (Gap between candle 1 and candle 3)
    
    Returns dataframe with FVG information added.
    """
    df = df.copy()
    
    # Initialize FVG columns
    df['FVG_Type'] = None  # 'Bearish' or 'Bullish'
    df['FVG_High'] = np.nan
    df['FVG_Low'] = np.nan
    
    # Need at least 3 candles
    for i in range(2, len(df)):
        # Bearish FVG: Low of candle 1 (i-2) > High of candle 3 (i)
        if df.iloc[i-2]['Low'] > df.iloc[i]['High']:
            df.at[i, 'FVG_Type'] = 'Bearish'
            df.at[i, 'FVG_High'] = df.iloc[i-2]['Low']
            df.at[i, 'FVG_Low'] = df.iloc[i]['High']
        
        # Bullish FVG: High of candle 1 (i-2) < Low of candle 3 (i)
        elif df.iloc[i-2]['High'] < df.iloc[i]['Low']:
            df.at[i, 'FVG_Type'] = 'Bullish'
            df.at[i, 'FVG_High'] = df.iloc[i]['Low']
            df.at[i, 'FVG_Low'] = df.iloc[i-2]['High']
    
    return df


# ============================
# IFVG TRIGGER DETECTION
# ============================

def check_ifvg_trigger(df: pd.DataFrame, idx: int) -> Optional[Dict]:
    """
    Check if current candle triggers an IFVG (Inversion Fair Value Gap) signal.
    
    LONG: Close ABOVE the High of a recent Bearish FVG (created in last 60 min)
    SHORT: Close BELOW the Low of a recent Bullish FVG (created in last 60 min)
    
    Returns: Dict with trigger info or None
    """
    current_close = df.iloc[idx]['Close']
    
    # Look back up to FVG_RECENCY_CANDLES for recent FVGs
    lookback_start = max(0, idx - FVG_RECENCY_CANDLES)
    
    # Check for LONG trigger (price closes above Bearish FVG High)
    for i in range(idx - 1, lookback_start - 1, -1):
        if df.iloc[i]['FVG_Type'] == 'Bearish':
            fvg_high = df.iloc[i]['FVG_High']
            if pd.notna(fvg_high) and current_close > fvg_high:
                return {
                    'direction': 'LONG',
                    'entry_price': current_close,
                    'fvg_idx': i,
                    'fvg_type': 'Bearish',
                    'trigger_idx': idx
                }
    
    # Check for SHORT trigger (price closes below Bullish FVG Low)
    for i in range(idx - 1, lookback_start - 1, -1):
        if df.iloc[i]['FVG_Type'] == 'Bullish':
            fvg_low = df.iloc[i]['FVG_Low']
            if pd.notna(fvg_low) and current_close < fvg_low:
                return {
                    'direction': 'SHORT',
                    'entry_price': current_close,
                    'fvg_idx': i,
                    'fvg_type': 'Bullish',
                    'trigger_idx': idx
                }
    
    return None


# ============================
# CONFLUENCE FILTERS
# ============================

def check_displacement(df: pd.DataFrame, idx: int) -> bool:
    """
    Filter 1: Displacement / CSID (Candle Strength)
    
    The candle that validates the inversion must have a significant body.
    Body size > 60% of total range (High - Low)
    """
    candle = df.iloc[idx]
    
    body_size = abs(candle['Close'] - candle['Open'])
    total_range = candle['High'] - candle['Low']
    
    if total_range == 0:
        return False
    
    body_percentage = body_size / total_range
    
    return body_percentage > DISPLACEMENT_THRESHOLD


def check_mss(df: pd.DataFrame, idx: int, direction: str) -> bool:
    """
    Filter 2: MSS (Market Structure Shift)
    
    LONG: Price must have broken a recent Swing High (highest high in last 12 candles)
    SHORT: Price must have broken a recent Swing Low (lowest low in last 12 candles)
    """
    lookback_start = max(0, idx - MSS_LOOKBACK_CANDLES)
    
    if direction == 'LONG':
        # Find the highest high in the lookback period (before current candle)
        if lookback_start >= idx:
            return False
        
        swing_high = df.iloc[lookback_start:idx]['High'].max()
        current_high = df.iloc[idx]['High']
        
        # Current candle must break above the swing high
        return current_high > swing_high
    
    elif direction == 'SHORT':
        # Find the lowest low in the lookback period (before current candle)
        if lookback_start >= idx:
            return False
        
        swing_low = df.iloc[lookback_start:idx]['Low'].min()
        current_low = df.iloc[idx]['Low']
        
        # Current candle must break below the swing low
        return current_low < swing_low
    
    return False


def check_smt_divergence(nq_df: pd.DataFrame, es_df: pd.DataFrame, 
                         nq_idx: int, direction: str) -> bool:
    """
    Filter 3: SMT Divergence (Smart Money Technique - NQ vs ES comparison)
    
    Compare lows/highs formed in the 60 minutes preceding the signal.
    
    LONG (Bullish SMT): NQ made a Lower Low WHILE ES made a Higher Low or Double Bottom
    SHORT (Bearish SMT): NQ made a Higher High WHILE ES made a Lower High or Double Top
    """
    lookback_start = max(0, nq_idx - SMT_LOOKBACK_CANDLES)
    
    if lookback_start >= nq_idx - 1:
        return False  # Not enough data
    
    try:
        # Get NQ data for lookback period
        nq_lookback = nq_df.iloc[lookback_start:nq_idx]
        
        # Get corresponding ES data (same DateTime range)
        start_time = nq_df.iloc[lookback_start]['DateTime']
        end_time = nq_df.iloc[nq_idx - 1]['DateTime']
        
        es_lookback = es_df[(es_df['DateTime'] >= start_time) & 
                           (es_df['DateTime'] <= end_time)]
        
        if len(es_lookback) < 2:
            return False
        
        if direction == 'LONG':
            # Bullish SMT: NQ Lower Low, ES Higher Low or Double Bottom
            
            # Find the two most recent significant lows in NQ
            nq_lows = nq_lookback['Low'].values
            if len(nq_lows) < 2:
                return False
            
            # Recent low vs previous low in NQ
            nq_recent_low = nq_lows[-1]
            nq_prev_low = nq_lows[:-1].min()
            
            # NQ should make lower low
            nq_lower_low = nq_recent_low < nq_prev_low
            
            # Find corresponding lows in ES
            es_lows = es_lookback['Low'].values
            if len(es_lows) < 2:
                return False
            
            es_recent_low = es_lows[-1]
            es_prev_low = es_lows[:-1].min()
            
            # ES should make higher low or double bottom (within tolerance)
            es_higher_low = es_recent_low > es_prev_low * (1 - SMT_TOLERANCE)
            
            return nq_lower_low and es_higher_low
        
        elif direction == 'SHORT':
            # Bearish SMT: NQ Higher High, ES Lower High or Double Top
            
            # Find the two most recent significant highs in NQ
            nq_highs = nq_lookback['High'].values
            if len(nq_highs) < 2:
                return False
            
            nq_recent_high = nq_highs[-1]
            nq_prev_high = nq_highs[:-1].max()
            
            # NQ should make higher high
            nq_higher_high = nq_recent_high > nq_prev_high
            
            # Find corresponding highs in ES
            es_highs = es_lookback['High'].values
            if len(es_highs) < 2:
                return False
            
            es_recent_high = es_highs[-1]
            es_prev_high = es_highs[:-1].max()
            
            # ES should make lower high or double top (within tolerance)
            es_lower_high = es_recent_high < es_prev_high * (1 + SMT_TOLERANCE)
            
            return nq_higher_high and es_lower_high
    
    except (IndexError, KeyError, ValueError) as e:
        # Handle synchronization issues, missing data, or calculation errors
        return False
    
    return False


# ============================
# TRADE MANAGEMENT
# ============================

def simulate_trade(df: pd.DataFrame, entry_idx: int, direction: str, 
                   entry_price: float) -> Dict:
    """
    Simulate trade outcome with fixed SL/TP.
    
    Returns: Trade result dictionary
    """
    if direction == 'LONG':
        stop_loss = entry_price - STOP_LOSS_POINTS
        take_profit = entry_price + TAKE_PROFIT_POINTS
    else:  # SHORT
        stop_loss = entry_price + STOP_LOSS_POINTS
        take_profit = entry_price - TAKE_PROFIT_POINTS
    
    # Check subsequent candles for SL or TP hit
    for i in range(entry_idx + 1, len(df)):
        candle = df.iloc[i]
        
        if direction == 'LONG':
            # Check if stopped out
            if candle['Low'] <= stop_loss:
                return {
                    'outcome': 'LOSS',
                    'pnl': -STOP_LOSS_POINTS,
                    'exit_idx': i,
                    'exit_price': stop_loss
                }
            # Check if take profit hit
            if candle['High'] >= take_profit:
                return {
                    'outcome': 'WIN',
                    'pnl': TAKE_PROFIT_POINTS,
                    'exit_idx': i,
                    'exit_price': take_profit
                }
        
        else:  # SHORT
            # Check if stopped out
            if candle['High'] >= stop_loss:
                return {
                    'outcome': 'LOSS',
                    'pnl': -STOP_LOSS_POINTS,
                    'exit_idx': i,
                    'exit_price': stop_loss
                }
            # Check if take profit hit
            if candle['Low'] <= take_profit:
                return {
                    'outcome': 'WIN',
                    'pnl': TAKE_PROFIT_POINTS,
                    'exit_idx': i,
                    'exit_price': take_profit
                }
    
    # If we reach end of data without hitting SL or TP, close at last candle
    last_candle = df.iloc[-1]
    exit_price = last_candle['Close']
    
    if direction == 'LONG':
        pnl = exit_price - entry_price
    else:
        pnl = entry_price - exit_price
    
    return {
        'outcome': 'OPEN',
        'pnl': pnl,
        'exit_idx': len(df) - 1,
        'exit_price': exit_price
    }


# ============================
# BACKTEST ENGINE
# ============================

def run_backtest_scenario(nq_df: pd.DataFrame, es_df: pd.DataFrame,
                         scenario_name: str, filters: Dict[str, bool]) -> Dict:
    """
    Run backtest for a specific scenario with given filters.
    
    Filters dict:
    - 'displacement': bool
    - 'mss': bool
    - 'smt': bool
    """
    print(f"\nRunning scenario: {scenario_name}")
    print(f"  Filters: {filters}")
    
    trades = []
    
    # Iterate through NQ data looking for IFVG triggers
    for idx in range(FVG_RECENCY_CANDLES, len(nq_df) - 1):
        # Check for IFVG trigger
        trigger = check_ifvg_trigger(nq_df, idx)
        
        if trigger is None:
            continue
        
        # Apply filters
        passed_filters = True
        
        if filters.get('displacement', False):
            if not check_displacement(nq_df, idx):
                passed_filters = False
        
        if filters.get('mss', False):
            if not check_mss(nq_df, idx, trigger['direction']):
                passed_filters = False
        
        if filters.get('smt', False):
            if not check_smt_divergence(nq_df, es_df, idx, trigger['direction']):
                passed_filters = False
        
        if not passed_filters:
            continue
        
        # Execute trade
        result = simulate_trade(nq_df, idx, trigger['direction'], trigger['entry_price'])
        
        # Record trade
        trade_record = {
            'entry_datetime': nq_df.iloc[idx]['DateTime'],
            'direction': trigger['direction'],
            'entry_price': trigger['entry_price'],
            'exit_price': result['exit_price'],
            'pnl': result['pnl'],
            'outcome': result['outcome'],
            'entry_idx': idx,
            'exit_idx': result['exit_idx']
        }
        
        trades.append(trade_record)
    
    # Calculate statistics
    if len(trades) == 0:
        return {
            'scenario': scenario_name,
            'num_trades': 0,
            'win_rate': 0.0,
            'total_pnl': 0.0,
            'avg_win': 0.0,
            'avg_loss': 0.0,
            'trades': []
        }
    
    trades_df = pd.DataFrame(trades)
    
    num_wins = len(trades_df[trades_df['outcome'] == 'WIN'])
    num_losses = len(trades_df[trades_df['outcome'] == 'LOSS'])
    win_rate = (num_wins / len(trades_df)) * 100 if len(trades_df) > 0 else 0
    
    total_pnl = trades_df['pnl'].sum()
    
    wins = trades_df[trades_df['outcome'] == 'WIN']['pnl']
    losses = trades_df[trades_df['outcome'] == 'LOSS']['pnl']
    
    avg_win = wins.mean() if len(wins) > 0 else 0
    avg_loss = losses.mean() if len(losses) > 0 else 0
    
    print(f"  Trades: {len(trades)}, Win Rate: {win_rate:.2f}%, PnL: {total_pnl:.2f} pts")
    
    return {
        'scenario': scenario_name,
        'num_trades': len(trades),
        'win_rate': win_rate,
        'total_pnl': total_pnl,
        'avg_win': avg_win,
        'avg_loss': avg_loss,
        'num_wins': num_wins,
        'num_losses': num_losses,
        'trades': trades
    }


def run_all_scenarios(nq_df: pd.DataFrame, es_df: pd.DataFrame) -> List[Dict]:
    """
    Run all 5 backtest scenarios and return results.
    """
    scenarios = [
        {
            'name': '1. IFVG Base (Trigger Only)',
            'filters': {'displacement': False, 'mss': False, 'smt': False}
        },
        {
            'name': '2. IFVG + Displacement',
            'filters': {'displacement': True, 'mss': False, 'smt': False}
        },
        {
            'name': '3. IFVG + MSS',
            'filters': {'displacement': False, 'mss': True, 'smt': False}
        },
        {
            'name': '4. IFVG + SMT Divergence',
            'filters': {'displacement': False, 'mss': False, 'smt': True}
        },
        {
            'name': '5. ICT Gold (IFVG + Displacement + SMT)',
            'filters': {'displacement': True, 'mss': False, 'smt': True}
        }
    ]
    
    results = []
    
    for scenario in scenarios:
        result = run_backtest_scenario(nq_df, es_df, scenario['name'], scenario['filters'])
        results.append(result)
    
    return results


# ============================
# REPORTING
# ============================

def generate_report(results: List[Dict]):
    """
    Generate and display comparative performance report.
    """
    print("\n" + "="*80)
    print("IFVG BACKTEST RESULTS - LONDON KILLZONE (01:00-04:00)")
    print("="*80)
    print(f"Period: 2018-2025 | Data: NQ 5-minute | Risk: {STOP_LOSS_POINTS}pt SL / {TAKE_PROFIT_POINTS}pt TP")
    print("="*80)
    
    # Create comparison table
    print(f"\n{'Scenario':<45} {'Trades':<10} {'Win Rate':<12} {'Total PnL':<15}")
    print("-" * 80)
    
    for result in results:
        scenario = result['scenario']
        num_trades = result['num_trades']
        win_rate = f"{result['win_rate']:.2f}%"
        total_pnl = f"{result['total_pnl']:.2f} pts"
        
        print(f"{scenario:<45} {num_trades:<10} {win_rate:<12} {total_pnl:<15}")
    
    print("-" * 80)
    
    # Additional statistics
    print("\nDETAILED STATISTICS:")
    print("-" * 80)
    
    for result in results:
        print(f"\n{result['scenario']}")
        print(f"  Number of Trades: {result['num_trades']}")
        print(f"  Wins: {result['num_wins']}")
        print(f"  Losses: {result['num_losses']}")
        print(f"  Win Rate: {result['win_rate']:.2f}%")
        print(f"  Total PnL: {result['total_pnl']:.2f} points")
        print(f"  Average Win: {result['avg_win']:.2f} points")
        print(f"  Average Loss: {result['avg_loss']:.2f} points")
    
    print("\n" + "="*80)


def save_trades_to_csv(results: List[Dict], output_path: str):
    """
    Save all trades to CSV for further analysis.
    """
    all_trades = []
    
    for result in results:
        for trade in result['trades']:
            trade_record = trade.copy()
            trade_record['scenario'] = result['scenario']
            all_trades.append(trade_record)
    
    if len(all_trades) > 0:
        trades_df = pd.DataFrame(all_trades)
        trades_df.to_csv(output_path, index=False)
        print(f"\nTrades saved to: {output_path}")


# ============================
# MAIN
# ============================

def main():
    """
    Main execution function.
    """
    print("="*80)
    print("IFVG (Inversion Fair Value Gap) Backtest - London Killzone")
    print("ICT Methodology - NQ Futures")
    print("="*80)
    
    # Set base path
    base_path = "/home/runner/work/Backtest-Trading/Backtest-Trading"
    
    # Step 1: Load data
    print("\n=== STEP 1: LOADING DATA ===")
    nq_df = load_nq_data(base_path)
    es_df = load_es_data(base_path)
    
    # Step 2: Synchronize data
    print("\n=== STEP 2: SYNCHRONIZING DATA ===")
    nq_df, es_df = synchronize_data(nq_df, es_df)
    
    # Step 3: Filter for London Killzone
    print("\n=== STEP 3: FILTERING LONDON KILLZONE (01:00-04:00) ===")
    nq_df = filter_london_killzone(nq_df)
    es_df = filter_london_killzone(es_df)
    
    # Step 4: Detect FVGs
    print("\n=== STEP 4: DETECTING FVGs ===")
    nq_df = detect_fvgs(nq_df)
    es_df = detect_fvgs(es_df)
    
    num_bearish = len(nq_df[nq_df['FVG_Type'] == 'Bearish'])
    num_bullish = len(nq_df[nq_df['FVG_Type'] == 'Bullish'])
    print(f"  NQ Bearish FVGs: {num_bearish}")
    print(f"  NQ Bullish FVGs: {num_bullish}")
    
    # Step 5: Run all scenarios
    print("\n=== STEP 5: RUNNING BACKTESTS ===")
    results = run_all_scenarios(nq_df, es_df)
    
    # Step 6: Generate report
    print("\n=== STEP 6: GENERATING REPORT ===")
    generate_report(results)
    
    # Step 7: Save trades
    output_file = os.path.join(base_path, "ifvg_backtest_trades.csv")
    save_trades_to_csv(results, output_file)
    
    print("\n" + "="*80)
    print("BACKTEST COMPLETE")
    print("="*80)


if __name__ == "__main__":
    main()

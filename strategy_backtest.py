#!/usr/bin/env python3
"""
Trading Strategy Backtesting for Judas Swing Patterns
Implements Strategy A (Conservative ICT) and Strategy B (Aggressive Turtle Soup)

This script performs full backtesting with P&L tracking, position management,
and comprehensive performance metrics.
"""

import pandas as pd
from pathlib import Path
from datetime import time
import numpy as np


# Constants
TOKYO_START = time(19, 0)
TOKYO_END = time(0, 0)
LONDON_START = time(1, 0)
LONDON_END = time(5, 0)

# Backtesting parameters
POSITION_SIZE = 1  # Number of contracts per trade
COMMISSION_PER_TRADE = 4.0  # Round-trip commission in points


def load_nq_data(base_path, years, timeframe='15m'):
    """Load NQ futures data from CSV files"""
    all_data = []
    
    for year in years:
        file_pattern = f"{year} {timeframe}.csv"
        file_path = Path(base_path) / file_pattern
        
        if not file_path.exists():
            print(f"Warning: File not found: {file_path}")
            continue
        
        print(f"Loading {file_path}...")
        
        df = pd.read_csv(
            file_path,
            sep=';',
            header=0,
            names=['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume'],
            skiprows=1
        )
        
        df['DateTime'] = pd.to_datetime(
            df['Date'] + ' ' + df['Time'],
            format='%d/%m/%Y %H:%M:%S'
        )
        
        all_data.append(df)
    
    if not all_data:
        raise ValueError("No data loaded")
    
    combined_df = pd.concat(all_data, ignore_index=True)
    combined_df = combined_df.sort_values('DateTime').reset_index(drop=True)
    
    print(f"Total records loaded: {len(combined_df)}")
    return combined_df


def detect_market_structure_shift(df, extreme_time, direction):
    """
    Detect Market Structure Shift (MSS) after manipulation extreme.
    
    For bullish Judas (short setup): Look for lower high after manipulation peak
    For bearish Judas (long setup): Look for higher low after manipulation valley
    
    Returns: (mss_detected, mss_time, entry_level)
    """
    # Get data after extreme
    after_extreme = df[df['DateTime'] > extreme_time].copy()
    
    if after_extreme.empty or len(after_extreme) < 3:
        return False, None, None
    
    if direction == 'bullish':
        # For bullish Judas (short setup): Look for price making lower high
        # This indicates structure shift to downside
        extreme_high = after_extreme.iloc[0:4]['High'].max()
        
        for i in range(1, min(len(after_extreme), 20)):  # Check next 20 bars (5 hours)
            current_bar = after_extreme.iloc[i]
            previous_bars = after_extreme.iloc[max(0, i-3):i]
            
            if not previous_bars.empty:
                recent_high = previous_bars['High'].max()
                
                # Check if we have a lower high (structure shift)
                if current_bar['High'] < recent_high and current_bar['Low'] < previous_bars['Low'].min():
                    # Displacement check: body should be significant
                    body_size = abs(current_bar['Close'] - current_bar['Open'])
                    bar_range = current_bar['High'] - current_bar['Low']
                    
                    if body_size > bar_range * 0.5 and current_bar['Close'] < current_bar['Open']:
                        # Check for FVG (Fair Value Gap)
                        if i >= 2:
                            prev_bar = after_extreme.iloc[i-1]
                            prev_prev_bar = after_extreme.iloc[i-2]
                            
                            # FVG exists if there's a gap
                            if prev_bar['Low'] > current_bar['High']:
                                fvg_entry = (prev_bar['Low'] + current_bar['High']) / 2
                                return True, current_bar['DateTime'], fvg_entry
        
    else:  # bearish Judas (long setup)
        # For bearish Judas (long setup): Look for price making higher low
        extreme_low = after_extreme.iloc[0:4]['Low'].min()
        
        for i in range(1, min(len(after_extreme), 20)):
            current_bar = after_extreme.iloc[i]
            previous_bars = after_extreme.iloc[max(0, i-3):i]
            
            if not previous_bars.empty:
                recent_low = previous_bars['Low'].min()
                
                # Check if we have a higher low (structure shift)
                if current_bar['Low'] > recent_low and current_bar['High'] > previous_bars['High'].max():
                    # Displacement check
                    body_size = abs(current_bar['Close'] - current_bar['Open'])
                    bar_range = current_bar['High'] - current_bar['Low']
                    
                    if body_size > bar_range * 0.5 and current_bar['Close'] > current_bar['Open']:
                        # Check for FVG
                        if i >= 2:
                            prev_bar = after_extreme.iloc[i-1]
                            prev_prev_bar = after_extreme.iloc[i-2]
                            
                            if prev_bar['High'] < current_bar['Low']:
                                fvg_entry = (prev_bar['High'] + current_bar['Low']) / 2
                                return True, current_bar['DateTime'], fvg_entry
    
    return False, None, None


def detect_swing_failure_pattern(df, extreme_time, direction, tokyo_high, tokyo_low):
    """
    Detect Swing Failure Pattern (SFP) - rejection at extreme.
    
    Returns: (sfp_detected, entry_time, entry_price, stop_loss)
    """
    # Get the bar that created the extreme and next few bars
    extreme_bar_idx = df[df['DateTime'] == extreme_time].index
    
    if len(extreme_bar_idx) == 0:
        return False, None, None, None
    
    extreme_idx = extreme_bar_idx[0]
    
    if extreme_idx >= len(df) - 2:
        return False, None, None, None
    
    extreme_bar = df.iloc[extreme_idx]
    next_bar = df.iloc[extreme_idx + 1]
    
    if direction == 'bullish':
        # Bullish Judas - check if bar wicked above Tokyo High but closed inside
        if (extreme_bar['High'] > tokyo_high and 
            extreme_bar['Close'] < tokyo_high and
            extreme_bar['Close'] < extreme_bar['Open']):  # Bearish close
            
            # Entry at close of rejection bar or 50% retracement of wick
            wick_size = extreme_bar['High'] - extreme_bar['Close']
            entry_price = extreme_bar['Close'] - wick_size * 0.5
            stop_loss = extreme_bar['High'] + 2  # 2 points above wick
            
            return True, next_bar['DateTime'], entry_price, stop_loss
            
    else:  # bearish
        # Bearish Judas - check if bar wicked below Tokyo Low but closed inside
        if (extreme_bar['Low'] < tokyo_low and 
            extreme_bar['Close'] > tokyo_low and
            extreme_bar['Close'] > extreme_bar['Open']):  # Bullish close
            
            wick_size = extreme_bar['Close'] - extreme_bar['Low']
            entry_price = extreme_bar['Close'] + wick_size * 0.5
            stop_loss = extreme_bar['Low'] - 2
            
            return True, next_bar['DateTime'], entry_price, stop_loss
    
    return False, None, None, None


def simulate_trade_strategy_a(df, swing_data, reversion_data):
    """
    Simulate Strategy A: Conservative ICT 2022 Model
    
    Entry: After MSS + FVG confirmation
    Exit scenarios:
    - Scenario 1: 100% at Tokyo Eq
    - Scenario 2: 100% at Opposing Liquidity
    - Scenario 3: 50% at Tokyo Eq, 50% at Opposing Liquidity
    """
    trades_scenario_1 = []
    trades_scenario_2 = []
    trades_scenario_3 = []
    
    print("\n" + "="*80)
    print("STRATEGY A: CONSERVATIVE ICT 2022 MODEL")
    print("="*80)
    
    for idx, swing in swing_data.iterrows():
        if idx % 100 == 0:
            print(f"Processing swing {idx + 1}/{len(swing_data)}...")
        
        date = swing['date']
        direction = swing['direction']
        tokyo_high = swing['tokyo_high']
        tokyo_low = swing['tokyo_low']
        
        # Get extreme_time from reversion_data
        reversion_row = reversion_data.iloc[idx]
        extreme_time = pd.Timestamp(reversion_row['extreme_time'])
        tokyo_eq = reversion_row['tokyo_eq']
        opposing_liq = reversion_row['opposing_liq']
        
        # Detect MSS
        mss_detected, mss_time, entry_price = detect_market_structure_shift(
            df, extreme_time, direction
        )
        
        if not mss_detected:
            continue
        
        # Set stop loss
        if direction == 'bullish':
            # Short trade - stop above manipulation high
            stop_loss = tokyo_high + swing['amplitude'] + 5
        else:
            # Long trade - stop below manipulation low
            stop_loss = tokyo_low - swing['amplitude'] - 5
        
        # Simulate trade from entry
        entry_data = df[df['DateTime'] >= mss_time]
        
        if entry_data.empty:
            continue
        
        entry_bar = entry_data.iloc[0]
        entry_time = entry_bar['DateTime']
        
        # Scenario 1: Exit 100% at Tokyo Eq
        trade_1 = simulate_single_trade(
            df, entry_time, entry_price, stop_loss, 
            [tokyo_eq], [1.0], direction
        )
        if trade_1:
            trade_1.update({
                'date': date,
                'strategy': 'A',
                'scenario': 1,
                'direction': direction
            })
            trades_scenario_1.append(trade_1)
        
        # Scenario 2: Exit 100% at Opposing Liquidity
        trade_2 = simulate_single_trade(
            df, entry_time, entry_price, stop_loss,
            [opposing_liq], [1.0], direction
        )
        if trade_2:
            trade_2.update({
                'date': date,
                'strategy': 'A',
                'scenario': 2,
                'direction': direction
            })
            trades_scenario_2.append(trade_2)
        
        # Scenario 3: Exit 50% at Eq, 50% at Opposing (with BE after first TP)
        trade_3 = simulate_partial_exit_trade(
            df, entry_time, entry_price, stop_loss,
            tokyo_eq, opposing_liq, direction
        )
        if trade_3:
            trade_3.update({
                'date': date,
                'strategy': 'A',
                'scenario': 3,
                'direction': direction
            })
            trades_scenario_3.append(trade_3)
    
    return trades_scenario_1, trades_scenario_2, trades_scenario_3


def simulate_trade_strategy_b(df, swing_data, reversion_data):
    """
    Simulate Strategy B: Aggressive Turtle Soup
    
    Entry: SFP at manipulation extreme
    """
    trades_scenario_1 = []
    trades_scenario_2 = []
    trades_scenario_3 = []
    
    print("\n" + "="*80)
    print("STRATEGY B: AGGRESSIVE TURTLE SOUP")
    print("="*80)
    
    for idx, swing in swing_data.iterrows():
        if idx % 100 == 0:
            print(f"Processing swing {idx + 1}/{len(swing_data)}...")
        
        date = swing['date']
        direction = swing['direction']
        tokyo_high = swing['tokyo_high']
        tokyo_low = swing['tokyo_low']
        
        # Get extreme_time from reversion_data
        reversion_row = reversion_data.iloc[idx]
        extreme_time = pd.Timestamp(reversion_row['extreme_time'])
        tokyo_eq = reversion_row['tokyo_eq']
        opposing_liq = reversion_row['opposing_liq']
        
        # Detect SFP
        sfp_detected, entry_time, entry_price, stop_loss = detect_swing_failure_pattern(
            df, extreme_time, direction, tokyo_high, tokyo_low
        )
        
        if not sfp_detected:
            continue
        
        # Scenario 1: Exit 100% at Tokyo Eq
        trade_1 = simulate_single_trade(
            df, entry_time, entry_price, stop_loss,
            [tokyo_eq], [1.0], direction
        )
        if trade_1:
            trade_1.update({
                'date': date,
                'strategy': 'B',
                'scenario': 1,
                'direction': direction
            })
            trades_scenario_1.append(trade_1)
        
        # Scenario 2: Exit 100% at Opposing Liquidity
        trade_2 = simulate_single_trade(
            df, entry_time, entry_price, stop_loss,
            [opposing_liq], [1.0], direction
        )
        if trade_2:
            trade_2.update({
                'date': date,
                'strategy': 'B',
                'scenario': 2,
                'direction': direction
            })
            trades_scenario_2.append(trade_2)
        
        # Scenario 3: Partial exits
        trade_3 = simulate_partial_exit_trade(
            df, entry_time, entry_price, stop_loss,
            tokyo_eq, opposing_liq, direction
        )
        if trade_3:
            trade_3.update({
                'date': date,
                'strategy': 'B',
                'scenario': 3,
                'direction': direction
            })
            trades_scenario_3.append(trade_3)
    
    return trades_scenario_1, trades_scenario_2, trades_scenario_3


def simulate_single_trade(df, entry_time, entry_price, stop_loss, targets, portions, direction):
    """Simulate a single trade with given parameters"""
    trade_data = df[df['DateTime'] >= entry_time].copy()
    
    if trade_data.empty:
        return None
    
    # Check each bar for TP or SL hit
    for _, bar in trade_data.iterrows():
        if direction == 'bullish':  # Short trade
            # Check stop loss (price goes up)
            if bar['High'] >= stop_loss:
                pnl = (entry_price - stop_loss) * POSITION_SIZE - COMMISSION_PER_TRADE
                return {
                    'entry_time': entry_time,
                    'entry_price': entry_price,
                    'exit_time': bar['DateTime'],
                    'exit_price': stop_loss,
                    'pnl': pnl,
                    'outcome': 'loss',
                    'exit_reason': 'stop_loss'
                }
            
            # Check take profit (price goes down)
            if bar['Low'] <= targets[0]:
                pnl = (entry_price - targets[0]) * POSITION_SIZE - COMMISSION_PER_TRADE
                return {
                    'entry_time': entry_time,
                    'entry_price': entry_price,
                    'exit_time': bar['DateTime'],
                    'exit_price': targets[0],
                    'pnl': pnl,
                    'outcome': 'win',
                    'exit_reason': 'take_profit'
                }
        else:  # Long trade
            # Check stop loss (price goes down)
            if bar['Low'] <= stop_loss:
                pnl = (stop_loss - entry_price) * POSITION_SIZE - COMMISSION_PER_TRADE
                return {
                    'entry_time': entry_time,
                    'entry_price': entry_price,
                    'exit_time': bar['DateTime'],
                    'exit_price': stop_loss,
                    'pnl': pnl,
                    'outcome': 'loss',
                    'exit_reason': 'stop_loss'
                }
            
            # Check take profit (price goes up)
            if bar['High'] >= targets[0]:
                pnl = (targets[0] - entry_price) * POSITION_SIZE - COMMISSION_PER_TRADE
                return {
                    'entry_time': entry_time,
                    'entry_price': entry_price,
                    'exit_time': bar['DateTime'],
                    'exit_price': targets[0],
                    'pnl': pnl,
                    'outcome': 'win',
                    'exit_reason': 'take_profit'
                }
    
    return None


def simulate_partial_exit_trade(df, entry_time, entry_price, stop_loss, tp1, tp2, direction):
    """Simulate trade with partial exits: 50% at TP1, 50% at TP2"""
    trade_data = df[df['DateTime'] >= entry_time].copy()
    
    if trade_data.empty:
        return None
    
    position_remaining = 1.0
    total_pnl = -COMMISSION_PER_TRADE  # Initial commission
    tp1_hit = False
    current_stop = stop_loss
    
    for _, bar in trade_data.iterrows():
        if direction == 'bullish':  # Short trade
            # Check stop loss
            if bar['High'] >= current_stop:
                exit_pnl = (entry_price - current_stop) * position_remaining
                total_pnl += exit_pnl
                return {
                    'entry_time': entry_time,
                    'entry_price': entry_price,
                    'exit_time': bar['DateTime'],
                    'exit_price': current_stop,
                    'pnl': total_pnl,
                    'outcome': 'partial_loss' if tp1_hit else 'loss',
                    'exit_reason': 'stop_loss',
                    'tp1_hit': tp1_hit
                }
            
            # Check TP1 (Tokyo Eq)
            if not tp1_hit and bar['Low'] <= tp1:
                partial_pnl = (entry_price - tp1) * 0.5
                total_pnl += partial_pnl
                position_remaining = 0.5
                tp1_hit = True
                current_stop = entry_price  # Move to breakeven
                continue
            
            # Check TP2 (Opposing Liq)
            if tp1_hit and bar['Low'] <= tp2:
                partial_pnl = (entry_price - tp2) * 0.5
                total_pnl += partial_pnl
                return {
                    'entry_time': entry_time,
                    'entry_price': entry_price,
                    'exit_time': bar['DateTime'],
                    'exit_price': tp2,
                    'pnl': total_pnl,
                    'outcome': 'full_win',
                    'exit_reason': 'both_tps',
                    'tp1_hit': True
                }
        
        else:  # Long trade
            # Check stop loss
            if bar['Low'] <= current_stop:
                exit_pnl = (current_stop - entry_price) * position_remaining
                total_pnl += exit_pnl
                return {
                    'entry_time': entry_time,
                    'entry_price': entry_price,
                    'exit_time': bar['DateTime'],
                    'exit_price': current_stop,
                    'pnl': total_pnl,
                    'outcome': 'partial_loss' if tp1_hit else 'loss',
                    'exit_reason': 'stop_loss',
                    'tp1_hit': tp1_hit
                }
            
            # Check TP1
            if not tp1_hit and bar['High'] >= tp1:
                partial_pnl = (tp1 - entry_price) * 0.5
                total_pnl += partial_pnl
                position_remaining = 0.5
                tp1_hit = True
                current_stop = entry_price
                continue
            
            # Check TP2
            if tp1_hit and bar['High'] >= tp2:
                partial_pnl = (tp2 - entry_price) * 0.5
                total_pnl += partial_pnl
                return {
                    'entry_time': entry_time,
                    'entry_price': entry_price,
                    'exit_time': bar['DateTime'],
                    'exit_price': tp2,
                    'pnl': total_pnl,
                    'outcome': 'full_win',
                    'exit_reason': 'both_tps',
                    'tp1_hit': True
                }
    
    return None


def calculate_performance_metrics(trades_df):
    """Calculate comprehensive performance metrics"""
    if trades_df.empty:
        return None
    
    metrics = {}
    
    # Basic stats
    metrics['total_trades'] = len(trades_df)
    metrics['winning_trades'] = len(trades_df[trades_df['pnl'] > 0])
    metrics['losing_trades'] = len(trades_df[trades_df['pnl'] <= 0])
    metrics['win_rate'] = metrics['winning_trades'] / metrics['total_trades'] * 100
    
    # P&L stats
    metrics['total_pnl'] = trades_df['pnl'].sum()
    metrics['avg_win'] = trades_df[trades_df['pnl'] > 0]['pnl'].mean() if metrics['winning_trades'] > 0 else 0
    metrics['avg_loss'] = trades_df[trades_df['pnl'] <= 0]['pnl'].mean() if metrics['losing_trades'] > 0 else 0
    metrics['largest_win'] = trades_df['pnl'].max()
    metrics['largest_loss'] = trades_df['pnl'].min()
    
    # Risk metrics
    if metrics['avg_loss'] != 0:
        metrics['profit_factor'] = abs(metrics['avg_win'] * metrics['winning_trades'] / 
                                       (metrics['avg_loss'] * metrics['losing_trades']))
    else:
        metrics['profit_factor'] = float('inf')
    
    # Drawdown
    cumulative_pnl = trades_df['pnl'].cumsum()
    running_max = cumulative_pnl.cummax()
    drawdown = running_max - cumulative_pnl
    metrics['max_drawdown'] = drawdown.max()
    
    # Expectancy
    metrics['expectancy'] = trades_df['pnl'].mean()
    
    return metrics


def print_strategy_results(trades_s1, trades_s2, trades_s3, strategy_name):
    """Print comprehensive results for a strategy"""
    print("\n" + "="*80)
    print(f"{strategy_name} - BACKTEST RESULTS")
    print("="*80)
    
    scenarios = [
        (trades_s1, "Scenario 1: 100% Exit at Tokyo Equilibrium"),
        (trades_s2, "Scenario 2: 100% Exit at Opposing Liquidity"),
        (trades_s3, "Scenario 3: 50% at Equilibrium / 50% at Opposing")
    ]
    
    for trades_list, scenario_name in scenarios:
        if not trades_list:
            print(f"\n{scenario_name}")
            print("No trades executed")
            continue
        
        trades_df = pd.DataFrame(trades_list)
        metrics = calculate_performance_metrics(trades_df)
        
        print(f"\n{'-'*80}")
        print(scenario_name)
        print(f"{'-'*80}")
        print(f"Total Trades: {metrics['total_trades']}")
        print(f"Winning Trades: {metrics['winning_trades']}")
        print(f"Losing Trades: {metrics['losing_trades']}")
        print(f"Win Rate: {metrics['win_rate']:.2f}%")
        print(f"\nP&L Performance:")
        print(f"  Total P&L: ${metrics['total_pnl']:.2f}")
        print(f"  Average Win: ${metrics['avg_win']:.2f}")
        print(f"  Average Loss: ${metrics['avg_loss']:.2f}")
        print(f"  Largest Win: ${metrics['largest_win']:.2f}")
        print(f"  Largest Loss: ${metrics['largest_loss']:.2f}")
        print(f"\nRisk Metrics:")
        print(f"  Profit Factor: {metrics['profit_factor']:.2f}")
        print(f"  Expectancy: ${metrics['expectancy']:.2f}")
        print(f"  Max Drawdown: ${metrics['max_drawdown']:.2f}")


def main():
    """Main execution"""
    print("="*80)
    print("JUDAS SWING TRADING STRATEGY BACKTEST")
    print("Full backtest with P&L tracking - NQ Futures 2018-2025")
    print("="*80)
    
    base_path = '/home/runner/work/Backtest-Trading/Backtest-Trading'
    years = list(range(2018, 2026))
    
    # Load data
    print("\nLoading market data...")
    df = load_nq_data(base_path, years, '15m')
    
    print("\nLoading swing data...")
    swing_data = pd.read_csv(f"{base_path}/judas_swing_results.csv")
    reversion_data = pd.read_csv(f"{base_path}/judas_swing_reversion_results.csv")
    
    print(f"Loaded {len(swing_data)} Judas Swings for backtesting")
    
    # Strategy A
    a_s1, a_s2, a_s3 = simulate_trade_strategy_a(df, swing_data, reversion_data)
    print_strategy_results(a_s1, a_s2, a_s3, "STRATEGY A: CONSERVATIVE ICT 2022")
    
    # Strategy B
    b_s1, b_s2, b_s3 = simulate_trade_strategy_b(df, swing_data, reversion_data)
    print_strategy_results(b_s1, b_s2, b_s3, "STRATEGY B: AGGRESSIVE TURTLE SOUP")
    
    # Save results
    all_trades = []
    for trades, strat, scen in [
        (a_s1, 'A', 1), (a_s2, 'A', 2), (a_s3, 'A', 3),
        (b_s1, 'B', 1), (b_s2, 'B', 2), (b_s3, 'B', 3)
    ]:
        if trades:
            df_temp = pd.DataFrame(trades)
            df_temp['strategy'] = strat
            df_temp['scenario'] = scen
            all_trades.append(df_temp)
    
    if all_trades:
        all_trades_df = pd.concat(all_trades, ignore_index=True)
        all_trades_df.to_csv(f"{base_path}/backtest_results.csv", index=False)
        print(f"\nAll trades saved to backtest_results.csv")
    
    print("\n" + "="*80)
    print("Backtest complete!")
    print("="*80)


if __name__ == "__main__":
    main()

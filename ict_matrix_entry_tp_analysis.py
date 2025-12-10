#!/usr/bin/env python3
"""
ICT London Silver Bullet - Matrix Analysis: Entry Points x Take Profit Levels
=============================================================================

Analyzes performance across:
- Entry Points: 62% Fib, 80% Fib
- Take Profit Levels: 1R, 1.5R, 2R, 2.5R, 3R, 3.5R, 4R, 4.5R, Previous Swing High

Stop Loss: 1 point below 100% Fibonacci (Sweep Low)
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# DATA LOADING
# ============================================================================

def load_nq_data():
    """Load all NQ 5-minute data from 2018 to 2025"""
    print("Loading NQ 5-minute data...")
    
    dfs = []
    years = [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]
    
    for year in years:
        filename = f"{year} 5m.csv"
        try:
            df = pd.read_csv(
                filename,
                sep=';',
                names=['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume'],
                skiprows=1
            )
            
            df['DateTime'] = pd.to_datetime(
                df['Date'] + ' ' + df['Time'],
                format='%d/%m/%Y %H:%M:%S'
            )
            
            df = df.drop(['Date', 'Time'], axis=1)
            df = df.set_index('DateTime')
            dfs.append(df)
            print(f"  {year}: {len(df)} rows loaded")
        except FileNotFoundError:
            print(f"  {year}: File not found, skipping")
            continue
    
    data = pd.concat(dfs, axis=0)
    data = data.sort_index()
    
    print(f"\nTotal rows: {len(data)}")
    print(f"Date range: {data.index.min()} to {data.index.max()}")
    
    return data


def identify_sessions(data):
    """Identify Tokyo and London sessions"""
    print("\nIdentifying sessions...")
    
    data['Hour'] = data.index.hour
    data['Date'] = data.index.date
    
    data['Tokyo_Session'] = False
    data['London_Session'] = False
    
    tokyo_mask = (data['Hour'] >= 19) & (data['Hour'] < 23)
    data.loc[tokyo_mask, 'Tokyo_Session'] = True
    
    london_mask = (data['Hour'] >= 1) & (data['Hour'] < 5)
    data.loc[london_mask, 'London_Session'] = True
    
    print(f"  Tokyo sessions: {tokyo_mask.sum()} bars")
    print(f"  London sessions: {london_mask.sum()} bars")
    
    return data


def calculate_tokyo_levels(data):
    """Calculate Tokyo High/Low for each trading day"""
    print("\nCalculating Tokyo levels...")
    
    tokyo_data = data[data['Tokyo_Session']].copy()
    
    tokyo_levels = tokyo_data.groupby('Date').agg({
        'High': 'max',
        'Low': 'min'
    }).rename(columns={'High': 'Tokyo_High', 'Low': 'Tokyo_Low'})
    
    tokyo_levels['Tokyo_EQ'] = (tokyo_levels['Tokyo_High'] + tokyo_levels['Tokyo_Low']) / 2
    
    tokyo_levels.index = pd.to_datetime(tokyo_levels.index) + timedelta(days=1)
    
    data['Trading_Date'] = pd.to_datetime(data['Date'])
    data = data.merge(tokyo_levels, left_on='Trading_Date', right_index=True, how='left')
    
    data[['Tokyo_High', 'Tokyo_Low', 'Tokyo_EQ']] = data[['Tokyo_High', 'Tokyo_Low', 'Tokyo_EQ']].ffill()
    
    valid_tokyo = data['Tokyo_High'].notna().sum()
    print(f"  Valid Tokyo levels: {valid_tokyo} bars")
    
    return data


def detect_swings_m5(data, lookback=5):
    """Detect swing highs and lows on M5 timeframe"""
    print(f"\nDetecting M5 swings (lookback={lookback})...")
    
    data['Swing_High'] = False
    data['Swing_Low'] = False
    
    highs = data['High'].values
    lows = data['Low'].values
    
    for i in range(lookback, len(data) - lookback):
        is_swing_high = True
        for j in range(1, lookback + 1):
            if highs[i] <= highs[i-j] or highs[i] <= highs[i+j]:
                is_swing_high = False
                break
        if is_swing_high:
            data.iloc[i, data.columns.get_loc('Swing_High')] = True
        
        is_swing_low = True
        for j in range(1, lookback + 1):
            if lows[i] >= lows[i-j] or lows[i] >= lows[i+j]:
                is_swing_low = False
                break
        if is_swing_low:
            data.iloc[i, data.columns.get_loc('Swing_Low')] = True
    
    swing_highs = data['Swing_High'].sum()
    swing_lows = data['Swing_Low'].sum()
    print(f"  Swing Highs: {swing_highs}")
    print(f"  Swing Lows: {swing_lows}")
    
    return data


# ============================================================================
# SETUP DETECTION WITH MATRIX TESTING
# ============================================================================

def find_london_setups_matrix(data):
    """
    Find ICT London Silver Bullet setups and test matrix of entry/TP combinations
    
    Entry Points: 62% Fib, 80% Fib
    TP Levels: 1R, 1.5R, 2R, 2.5R, 3R, 3.5R, 4R, 4.5R, Previous Swing High
    SL: 1 point below 100% Fibonacci (Sweep Low)
    """
    print("\nSearching for London Silver Bullet setups (Matrix Analysis)...")
    
    setups = []
    
    london_dates = data[data['London_Session']]['Trading_Date'].unique()
    
    for trade_date in london_dates:
        day_mask = (data['Trading_Date'] == trade_date) & (data['London_Session'])
        london_bars = data[day_mask].copy()
        
        if len(london_bars) == 0:
            continue
        
        tokyo_high = london_bars['Tokyo_High'].iloc[0]
        tokyo_low = london_bars['Tokyo_Low'].iloc[0]
        
        if pd.isna(tokyo_high) or pd.isna(tokyo_low):
            continue
        
        sweep_detected = False
        sweep_low = None
        sweep_time = None
        
        mss_detected = False
        impulse_high = None
        impulse_time = None
        
        # Track previous swing high before sweep
        prev_swing_high = None
        
        for idx, row in london_bars.iterrows():
            
            if not sweep_detected and row['Swing_High']:
                prev_swing_high = row['High']
            
            if not sweep_detected and row['Low'] < tokyo_low:
                sweep_detected = True
                sweep_low = row['Low']
                sweep_time = idx
            
            if sweep_detected and not mss_detected:
                if row['High'] > tokyo_low:
                    mss_detected = True
                    impulse_high = row['High']
                    impulse_time = idx
            
            if mss_detected and impulse_high:
                fib_range = impulse_high - sweep_low
                
                # Entry levels
                fib_62 = impulse_high - (fib_range * 0.62)
                fib_80 = impulse_high - (fib_range * 0.80)
                fib_100 = sweep_low
                
                # Check for invalidation
                if row['High'] > tokyo_high:
                    break
                
                # Check if price retraces to either entry level
                entry_62_triggered = row['Low'] <= fib_62 and not pd.isna(fib_62)
                entry_80_triggered = row['Low'] <= fib_80 and not pd.isna(fib_80)
                
                if entry_62_triggered or entry_80_triggered:
                    
                    # Test both entry points
                    for entry_level, entry_name in [(fib_62, '62%'), (fib_80, '80%')]:
                        if (entry_name == '62%' and not entry_62_triggered) or \
                           (entry_name == '80%' and not entry_80_triggered):
                            continue
                        
                        entry_price = entry_level
                        entry_time = idx
                        entry_hour = idx.hour
                        
                        sl_price = fib_100 - 1.0
                        risk = entry_price - sl_price
                        
                        if risk <= 0:
                            continue
                        
                        # Test multiple TP levels
                        tp_configs = [
                            ('1R', entry_price + (risk * 1.0)),
                            ('1.5R', entry_price + (risk * 1.5)),
                            ('2R', entry_price + (risk * 2.0)),
                            ('2.5R', entry_price + (risk * 2.5)),
                            ('3R', entry_price + (risk * 3.0)),
                            ('3.5R', entry_price + (risk * 3.5)),
                            ('4R', entry_price + (risk * 4.0)),
                            ('4.5R', entry_price + (risk * 4.5)),
                            ('Swing_High', prev_swing_high if prev_swing_high else tokyo_high)
                        ]
                        
                        for tp_name, tp_price in tp_configs:
                            if pd.isna(tp_price):
                                continue
                            
                            reward = tp_price - entry_price
                            rr_ratio = reward / risk if risk > 0 else 0
                            
                            outcome = simulate_trade(data, entry_time, entry_price, sl_price, tp_price)
                            
                            setups.append({
                                'Date': trade_date,
                                'Entry_Time': entry_time,
                                'Entry_Hour': entry_hour,
                                'Entry_Level': entry_name,
                                'TP_Level': tp_name,
                                'Sweep_Low': sweep_low,
                                'Impulse_High': impulse_high,
                                'Prev_Swing_High': prev_swing_high,
                                'Tokyo_High': tokyo_high,
                                'Tokyo_Low': tokyo_low,
                                'Entry_Price': entry_price,
                                'SL_Price': sl_price,
                                'TP_Price': tp_price,
                                'Risk': risk,
                                'Reward': reward,
                                'RR_Ratio': rr_ratio,
                                'Outcome': outcome['outcome'],
                                'Exit_Price': outcome['exit_price'],
                                'PnL': outcome['pnl'],
                                'Exit_Time': outcome['exit_time'],
                                'Bars_Held': outcome['bars_held']
                            })
                    
                    break  # One setup per day
    
    print(f"  Found {len(setups)} setup x entry x TP combinations")
    return pd.DataFrame(setups)


def simulate_trade(data, entry_time, entry_price, sl_price, tp_price):
    """Simulate trade execution and determine outcome"""
    future_bars = data[data.index > entry_time].head(100)
    
    bars_held = 0
    for idx, row in future_bars.iterrows():
        bars_held += 1
        
        if row['Low'] <= sl_price:
            return {
                'outcome': 'Loss',
                'exit_price': sl_price,
                'pnl': sl_price - entry_price,
                'exit_time': idx,
                'bars_held': bars_held
            }
        
        if row['High'] >= tp_price:
            return {
                'outcome': 'Win',
                'exit_price': tp_price,
                'pnl': tp_price - entry_price,
                'exit_time': idx,
                'bars_held': bars_held
            }
    
    if len(future_bars) > 0:
        last_bar = future_bars.iloc[-1]
        pnl = last_bar['Close'] - entry_price
        outcome = 'Win' if pnl > 0 else 'Loss'
        return {
            'outcome': outcome,
            'exit_price': last_bar['Close'],
            'pnl': pnl,
            'exit_time': last_bar.name,
            'bars_held': bars_held
        }
    
    return {
        'outcome': 'No Exit',
        'exit_price': entry_price,
        'pnl': 0,
        'exit_time': entry_time,
        'bars_held': 0
    }


# ============================================================================
# MATRIX ANALYSIS
# ============================================================================

def analyze_matrix_performance(setups):
    """Analyze performance across all entry/TP combinations"""
    print("\n" + "="*100)
    print("MATRIX ANALYSIS: ENTRY POINTS x TAKE PROFIT LEVELS")
    print("="*100)
    
    if len(setups) == 0:
        print("No setups found!")
        return
    
    # Group by Entry Level and TP Level
    entry_levels = ['62%', '80%']
    tp_levels = ['1R', '1.5R', '2R', '2.5R', '3R', '3.5R', '4R', '4.5R', 'Swing_High']
    
    results_matrix = []
    
    for entry_level in entry_levels:
        print(f"\n{'='*100}")
        print(f"ENTRY AT {entry_level} FIBONACCI RETRACEMENT")
        print(f"{'='*100}")
        
        entry_setups = setups[setups['Entry_Level'] == entry_level]
        
        for tp_level in tp_levels:
            tp_setups = entry_setups[entry_setups['TP_Level'] == tp_level]
            
            if len(tp_setups) == 0:
                continue
            
            total_trades = len(tp_setups)
            wins = len(tp_setups[tp_setups['Outcome'] == 'Win'])
            losses = len(tp_setups[tp_setups['Outcome'] == 'Loss'])
            win_rate = (wins / total_trades * 100) if total_trades > 0 else 0
            
            gross_profit = tp_setups[tp_setups['PnL'] > 0]['PnL'].sum()
            gross_loss = abs(tp_setups[tp_setups['PnL'] < 0]['PnL'].sum())
            net_profit = tp_setups['PnL'].sum()
            profit_factor = (gross_profit / gross_loss) if gross_loss > 0 else 0
            
            avg_win = tp_setups[tp_setups['PnL'] > 0]['PnL'].mean() if wins > 0 else 0
            avg_loss = tp_setups[tp_setups['PnL'] < 0]['PnL'].mean() if losses > 0 else 0
            avg_rr = tp_setups['RR_Ratio'].mean()
            
            # Drawdown
            tp_setups_sorted = tp_setups.sort_values('Entry_Time')
            tp_setups_sorted['Cumulative_PnL'] = tp_setups_sorted['PnL'].cumsum()
            tp_setups_sorted['Running_Max'] = tp_setups_sorted['Cumulative_PnL'].cummax()
            tp_setups_sorted['Drawdown'] = tp_setups_sorted['Cumulative_PnL'] - tp_setups_sorted['Running_Max']
            max_drawdown = tp_setups_sorted['Drawdown'].min()
            
            print(f"\n📊 TP: {tp_level}")
            print(f"  Trades: {total_trades} | Wins: {wins} | Losses: {losses}")
            print(f"  Win Rate: {win_rate:.2f}%")
            print(f"  Net Profit: {net_profit:+.2f} pts")
            print(f"  Profit Factor: {profit_factor:.2f}")
            print(f"  Avg Win: {avg_win:+.2f} pts | Avg Loss: {avg_loss:.2f} pts")
            print(f"  Avg RR: {avg_rr:.2f}:1")
            print(f"  Max Drawdown: {max_drawdown:.2f} pts")
            
            results_matrix.append({
                'Entry_Level': entry_level,
                'TP_Level': tp_level,
                'Total_Trades': total_trades,
                'Wins': wins,
                'Losses': losses,
                'Win_Rate': win_rate,
                'Net_Profit': net_profit,
                'Profit_Factor': profit_factor,
                'Avg_Win': avg_win,
                'Avg_Loss': avg_loss,
                'Avg_RR': avg_rr,
                'Max_Drawdown': max_drawdown
            })
    
    # Summary table
    print(f"\n{'='*100}")
    print("SUMMARY TABLE")
    print(f"{'='*100}")
    
    df_results = pd.DataFrame(results_matrix)
    
    # Best combinations
    print("\n🏆 TOP 5 COMBINATIONS BY NET PROFIT:")
    top_5 = df_results.nlargest(5, 'Net_Profit')
    for idx, row in top_5.iterrows():
        print(f"  {row['Entry_Level']} + {row['TP_Level']}: {row['Net_Profit']:+.2f} pts " +
              f"({row['Win_Rate']:.1f}% WR, {row['Profit_Factor']:.2f} PF)")
    
    print("\n🏆 TOP 5 COMBINATIONS BY WIN RATE:")
    top_5_wr = df_results.nlargest(5, 'Win_Rate')
    for idx, row in top_5_wr.iterrows():
        print(f"  {row['Entry_Level']} + {row['TP_Level']}: {row['Win_Rate']:.1f}% WR " +
              f"({row['Net_Profit']:+.2f} pts, {row['Profit_Factor']:.2f} PF)")
    
    print("\n🏆 TOP 5 COMBINATIONS BY PROFIT FACTOR:")
    top_5_pf = df_results.nlargest(5, 'Profit_Factor')
    for idx, row in top_5_pf.iterrows():
        print(f"  {row['Entry_Level']} + {row['TP_Level']}: {row['Profit_Factor']:.2f} PF " +
              f"({row['Win_Rate']:.1f}% WR, {row['Net_Profit']:+.2f} pts)")
    
    # Export detailed results
    df_results.to_csv('ict_matrix_summary.csv', index=False)
    print(f"\n✅ Summary exported to: ict_matrix_summary.csv")
    
    return df_results


def export_detailed_results(setups):
    """Export detailed trade-by-trade results"""
    if len(setups) > 0:
        output_file = 'ict_matrix_detailed_results.csv'
        setups.to_csv(output_file, index=False)
        print(f"✅ Detailed results exported to: {output_file}")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    print("="*100)
    print("ICT LONDON SILVER BULLET - MATRIX ANALYSIS")
    print("="*100)
    print("\nEntry Points: 62% Fib, 80% Fib")
    print("TP Levels: 1R, 1.5R, 2R, 2.5R, 3R, 3.5R, 4R, 4.5R, Previous Swing High")
    print("SL: 1 point below 100% Fibonacci (Sweep Low)")
    print()
    
    # Load data
    data = load_nq_data()
    
    # Identify sessions
    data = identify_sessions(data)
    
    # Calculate Tokyo levels
    data = calculate_tokyo_levels(data)
    
    # Detect swings
    data = detect_swings_m5(data, lookback=5)
    
    # Find setups with matrix testing
    setups = find_london_setups_matrix(data)
    
    # Analyze performance
    if len(setups) > 0:
        analyze_matrix_performance(setups)
        export_detailed_results(setups)
    else:
        print("\n⚠️ No valid setups found!")
    
    print("\n" + "="*100)
    print("MATRIX ANALYSIS COMPLETE")
    print("="*100)


if __name__ == "__main__":
    main()

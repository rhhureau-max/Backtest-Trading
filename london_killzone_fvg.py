"""
London Killzone FVG Inversion Strategy Backtest
Tests a strategy on NQ 15-minute data with multiple RR scenarios
"""

import pandas as pd
import numpy as np

def load_and_prepare_data(filepath):
    """Load and prepare the 15-minute NQ data"""
    df = pd.read_csv(filepath)
    
    # Combine Date and Time into a single datetime column
    df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%d/%m/%Y %H:%M:%S')
    
    # Extract hour for filtering
    df['Hour'] = df['Datetime'].dt.hour
    
    # Sort by datetime
    df = df.sort_values('Datetime').reset_index(drop=True)
    
    return df

def detect_fvg(df):
    """
    Detect Fair Value Gaps (FVG)
    Bullish FVG: Low[i-2] > High[i] (gap up)
    Bearish FVG: High[i-2] < Low[i] (gap down)
    """
    df = df.copy()
    
    # Initialize FVG columns
    df['Bearish_FVG_Top'] = np.nan
    df['Bearish_FVG_Bottom'] = np.nan
    df['Bullish_FVG_Top'] = np.nan
    df['Bullish_FVG_Bottom'] = np.nan
    
    # Start from index 2 (need i-2, i-1, i)
    for i in range(2, len(df)):
        # Bearish FVG: High[i-2] < Low[i] (gap down)
        # Gap area is between High[i-2] and Low[i]
        if df.loc[i-2, 'High'] < df.loc[i, 'Low']:
            df.loc[i, 'Bearish_FVG_Top'] = df.loc[i, 'Low']
            df.loc[i, 'Bearish_FVG_Bottom'] = df.loc[i-2, 'High']
        
        # Bullish FVG: Low[i-2] > High[i] (gap up)
        # Gap area is between Low[i-2] and High[i]
        if df.loc[i-2, 'Low'] > df.loc[i, 'High']:
            df.loc[i, 'Bullish_FVG_Top'] = df.loc[i-2, 'Low']
            df.loc[i, 'Bullish_FVG_Bottom'] = df.loc[i, 'High']
    
    return df

def identify_trades(df):
    """
    Identify trade entries based on FVG inversions
    Long Entry: Price closes ABOVE the top of a Bearish FVG
    Short Entry: Price closes BELOW the bottom of a Bullish FVG
    Time Window: 01:00 - 05:00
    """
    trades = []
    
    # Track active FVGs
    active_bearish_fvgs = []  # List of (top, bottom) tuples
    active_bullish_fvgs = []  # List of (top, bottom) tuples
    
    for i in range(len(df)):
        # Add new FVGs to active lists
        if not pd.isna(df.loc[i, 'Bearish_FVG_Top']):
            active_bearish_fvgs.append({
                'top': df.loc[i, 'Bearish_FVG_Top'],
                'bottom': df.loc[i, 'Bearish_FVG_Bottom'],
                'index': i
            })
        
        if not pd.isna(df.loc[i, 'Bullish_FVG_Top']):
            active_bullish_fvgs.append({
                'top': df.loc[i, 'Bullish_FVG_Top'],
                'bottom': df.loc[i, 'Bullish_FVG_Bottom'],
                'index': i
            })
        
        # Check for Long Entry (inversion of Bearish FVG)
        # Only within time window 01:00 - 05:00
        if 1 <= df.loc[i, 'Hour'] < 5:
            for fvg in active_bearish_fvgs[:]:  # Use slice to allow removal during iteration
                # Long Entry: Close above Bearish FVG top (inversion)
                if df.loc[i, 'Close'] > fvg['top']:
                    # Entry at close of this candle
                    entry_price = df.loc[i, 'Close']
                    sl_price = df.loc[i, 'Low']  # SL at low of entry candle
                    sl_distance = entry_price - sl_price
                    
                    if sl_distance > 0:
                        trades.append({
                            'Entry_Index': i,
                            'Entry_Time': df.loc[i, 'Datetime'],
                            'Direction': 'LONG',
                            'Entry_Price': entry_price,
                            'SL_Price': sl_price,
                            'SL_Distance': sl_distance,
                            'TP_1R': entry_price + (1.0 * sl_distance),
                            'TP_1_5R': entry_price + (1.5 * sl_distance),
                            'TP_2R': entry_price + (2.0 * sl_distance)
                        })
                    
                    # Remove this FVG from active list
                    active_bearish_fvgs.remove(fvg)
        
        # Check for Short Entry (inversion of Bullish FVG)
        if 1 <= df.loc[i, 'Hour'] < 5:
            for fvg in active_bullish_fvgs[:]:
                # Short Entry: Close below Bullish FVG bottom (inversion)
                if df.loc[i, 'Close'] < fvg['bottom']:
                    # Entry at close of this candle
                    entry_price = df.loc[i, 'Close']
                    sl_price = df.loc[i, 'High']  # SL at high of entry candle
                    sl_distance = sl_price - entry_price
                    
                    if sl_distance > 0:
                        trades.append({
                            'Entry_Index': i,
                            'Entry_Time': df.loc[i, 'Datetime'],
                            'Direction': 'SHORT',
                            'Entry_Price': entry_price,
                            'SL_Price': sl_price,
                            'SL_Distance': sl_distance,
                            'TP_1R': entry_price - (1.0 * sl_distance),
                            'TP_1_5R': entry_price - (1.5 * sl_distance),
                            'TP_2R': entry_price - (2.0 * sl_distance)
                        })
                    
                    # Remove this FVG from active list
                    active_bullish_fvgs.remove(fvg)
        
        # Remove mitigated/invalidated FVGs
        # Bearish FVG is invalidated if price goes back into the gap
        active_bearish_fvgs = [
            fvg for fvg in active_bearish_fvgs
            if not (df.loc[i, 'Low'] <= fvg['top'] and df.loc[i, 'High'] >= fvg['bottom'])
        ]
        
        # Bullish FVG is invalidated if price goes back into the gap
        active_bullish_fvgs = [
            fvg for fvg in active_bullish_fvgs
            if not (df.loc[i, 'Low'] <= fvg['top'] and df.loc[i, 'High'] >= fvg['bottom'])
        ]
    
    return pd.DataFrame(trades)

def simulate_trade_outcomes(df, trades_df):
    """
    Simulate trade outcomes for each TP scenario (1R, 1.5R, 2R)
    Returns a dictionary with results for each scenario
    """
    scenarios = {
        '1R': [],
        '1.5R': [],
        '2R': []
    }
    
    for idx, trade in trades_df.iterrows():
        entry_idx = trade['Entry_Index']
        direction = trade['Direction']
        sl_price = trade['SL_Price']
        
        # Check each TP scenario
        for scenario_name, tp_key in [('1R', 'TP_1R'), ('1.5R', 'TP_1_5R'), ('2R', 'TP_2R')]:
            tp_price = trade[tp_key]
            
            # Simulate from next candle onwards
            hit_tp = False
            hit_sl = False
            
            for i in range(entry_idx + 1, len(df)):
                low = df.loc[i, 'Low']
                high = df.loc[i, 'High']
                
                if direction == 'LONG':
                    # Check if SL hit first (conservative: assume SL hit before TP if both in same candle)
                    if low <= sl_price:
                        hit_sl = True
                        break
                    # Check if TP hit
                    if high >= tp_price:
                        hit_tp = True
                        break
                
                else:  # SHORT
                    # Check if SL hit first
                    if high >= sl_price:
                        hit_sl = True
                        break
                    # Check if TP hit
                    if low <= tp_price:
                        hit_tp = True
                        break
            
            # Record result
            if hit_tp:
                # Extract R-multiple from scenario name
                r_value = float(scenario_name.replace('R', ''))
                scenarios[scenario_name].append(r_value)
            elif hit_sl:
                scenarios[scenario_name].append(-1.0)
            else:
                # Trade didn't exit within data range - count as loss
                scenarios[scenario_name].append(-1.0)
    
    return scenarios

def calculate_metrics(results):
    """Calculate performance metrics for each scenario"""
    metrics = {}
    
    for scenario_name, r_multiples in results.items():
        if len(r_multiples) == 0:
            metrics[scenario_name] = {
                'Total_Trades': 0,
                'Win_Rate': 0.0,
                'Net_Profit_R': 0.0,
                'Max_Drawdown_R': 0.0
            }
            continue
        
        total_trades = len(r_multiples)
        wins = sum(1 for r in r_multiples if r > 0)
        win_rate = (wins / total_trades * 100) if total_trades > 0 else 0.0
        net_profit = sum(r_multiples)
        
        # Calculate max drawdown
        cumulative = 0
        peak = 0
        max_dd = 0
        
        for r in r_multiples:
            cumulative += r
            if cumulative > peak:
                peak = cumulative
            drawdown = peak - cumulative
            if drawdown > max_dd:
                max_dd = drawdown
        
        metrics[scenario_name] = {
            'Total_Trades': total_trades,
            'Win_Rate': win_rate,
            'Net_Profit_R': net_profit,
            'Max_Drawdown_R': max_dd
        }
    
    return metrics

def print_comparison_table(metrics):
    """Print a formatted comparison table"""
    print("\n" + "="*80)
    print("LONDON KILLZONE FVG INVERSION STRATEGY - RR COMPARISON")
    print("="*80)
    print("\nTime Window: 01:00 - 05:00")
    print("Strategy: FVG Inversion (Long above Bearish FVG, Short below Bullish FVG)")
    print("Stop Loss: Entry Candle High/Low")
    print("\n" + "="*80)
    
    # Create comparison table
    print("\n{:<15} {:<15} {:<15} {:<20} {:<20}".format(
        "TP Scenario", "Total Trades", "Win Rate (%)", "Net Profit (R)", "Max Drawdown (R)"
    ))
    print("-" * 80)
    
    for scenario in ['1R', '1.5R', '2R']:
        m = metrics[scenario]
        print("{:<15} {:<15} {:<15.2f} {:<20.2f} {:<20.2f}".format(
            scenario,
            m['Total_Trades'],
            m['Win_Rate'],
            m['Net_Profit_R'],
            m['Max_Drawdown_R']
        ))
    
    print("="*80)
    
    # Determine best scenario
    best_scenario = max(metrics.keys(), key=lambda k: metrics[k]['Net_Profit_R'])
    print(f"\n🏆 BEST RR SCENARIO: {best_scenario}")
    print(f"   Net Profit: {metrics[best_scenario]['Net_Profit_R']:.2f}R")
    print(f"   Win Rate: {metrics[best_scenario]['Win_Rate']:.2f}%")
    print(f"   Max Drawdown: {metrics[best_scenario]['Max_Drawdown_R']:.2f}R")
    print("\n" + "="*80 + "\n")

def main():
    """Main execution function"""
    print("Loading data...")
    df = load_and_prepare_data('nq_15m_data.csv')
    print(f"Loaded {len(df)} candles from {df['Datetime'].min()} to {df['Datetime'].max()}")
    
    print("\nDetecting FVGs...")
    df = detect_fvg(df)
    bearish_fvgs = df['Bearish_FVG_Top'].notna().sum()
    bullish_fvgs = df['Bullish_FVG_Top'].notna().sum()
    print(f"Found {bearish_fvgs} Bearish FVGs and {bullish_fvgs} Bullish FVGs")
    
    print("\nIdentifying trades (01:00-05:00 window)...")
    trades_df = identify_trades(df)
    print(f"Found {len(trades_df)} total trades")
    
    if len(trades_df) == 0:
        print("\nNo trades found!")
        return
    
    long_trades = len(trades_df[trades_df['Direction'] == 'LONG'])
    short_trades = len(trades_df[trades_df['Direction'] == 'SHORT'])
    print(f"  - Long trades: {long_trades}")
    print(f"  - Short trades: {short_trades}")
    
    print("\nSimulating trade outcomes for all TP scenarios...")
    results = simulate_trade_outcomes(df, trades_df)
    
    print("Calculating metrics...")
    metrics = calculate_metrics(results)
    
    # Print comparison table
    print_comparison_table(metrics)
    
    # Save detailed trades
    if len(trades_df) > 0:
        trades_df.to_csv('london_killzone_trades.csv', index=False)
        print("Detailed trades saved to: london_killzone_trades.csv\n")

if __name__ == "__main__":
    main()

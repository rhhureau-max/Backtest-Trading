"""
FVG (Fair Value Gap) Strategy Backtest with Stop Loss Comparison
Compares Candle-Based SL (Aggressive) vs Structure-Based SL (Conservative)
"""

import pandas as pd
import numpy as np
from datetime import datetime, time

def load_and_prepare_data(filepath):
    """Load and prepare the 15-minute NQ data"""
    df = pd.read_csv(filepath)
    
    # Combine Date and Time into a single datetime column
    df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%d/%m/%Y %H:%M:%S')
    
    # Extract hour and minute for filtering
    df['Hour'] = df['Datetime'].dt.hour
    df['Minute'] = df['Datetime'].dt.minute
    
    # Sort by datetime
    df = df.sort_values('Datetime').reset_index(drop=True)
    
    return df

def detect_fvg(df):
    """
    Detect Fair Value Gaps (FVG)
    Bearish FVG: Gap between High[i-2] and Low[i]
    Bullish FVG: Gap between Low[i-2] and High[i]
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
        if df.loc[i-2, 'High'] < df.loc[i, 'Low']:
            df.loc[i, 'Bearish_FVG_Top'] = df.loc[i, 'Low']
            df.loc[i, 'Bearish_FVG_Bottom'] = df.loc[i-2, 'High']
        
        # Bullish FVG: Low[i-2] > High[i] (gap up)
        if df.loc[i-2, 'Low'] > df.loc[i, 'High']:
            df.loc[i, 'Bullish_FVG_Top'] = df.loc[i-2, 'Low']
            df.loc[i, 'Bullish_FVG_Bottom'] = df.loc[i, 'High']
    
    return df

def identify_entries(df):
    """
    Identify entry signals
    Long Entry: Price closes ABOVE the top of a Bearish FVG
    Short Entry: Price closes BELOW the bottom of a Bullish FVG
    """
    df = df.copy()
    df['Long_Entry'] = False
    df['Short_Entry'] = False
    df['Entry_FVG_Top'] = np.nan
    df['Entry_FVG_Bottom'] = np.nan
    
    # Track active FVGs (forward fill until filled)
    active_bearish_fvg_top = None
    active_bearish_fvg_bottom = None
    active_bullish_fvg_top = None
    active_bullish_fvg_bottom = None
    
    for i in range(len(df)):
        # Update active bearish FVG if a new one appears
        if not pd.isna(df.loc[i, 'Bearish_FVG_Top']):
            active_bearish_fvg_top = df.loc[i, 'Bearish_FVG_Top']
            active_bearish_fvg_bottom = df.loc[i, 'Bearish_FVG_Bottom']
        
        # Update active bullish FVG if a new one appears
        if not pd.isna(df.loc[i, 'Bullish_FVG_Top']):
            active_bullish_fvg_top = df.loc[i, 'Bullish_FVG_Top']
            active_bullish_fvg_bottom = df.loc[i, 'Bullish_FVG_Bottom']
        
        # Check for Long Entry (close above bearish FVG top)
        if active_bearish_fvg_top is not None:
            if df.loc[i, 'Close'] > active_bearish_fvg_top:
                # Filter: only between 01:00 and 05:00
                if 1 <= df.loc[i, 'Hour'] < 5:
                    df.loc[i, 'Long_Entry'] = True
                    df.loc[i, 'Entry_FVG_Top'] = active_bearish_fvg_top
                    df.loc[i, 'Entry_FVG_Bottom'] = active_bearish_fvg_bottom
                # Reset the FVG after entry signal
                active_bearish_fvg_top = None
                active_bearish_fvg_bottom = None
        
        # Check for Short Entry (close below bullish FVG bottom)
        if active_bullish_fvg_top is not None:
            if df.loc[i, 'Close'] < active_bullish_fvg_bottom:
                # Filter: only between 01:00 and 05:00
                if 1 <= df.loc[i, 'Hour'] < 5:
                    df.loc[i, 'Short_Entry'] = True
                    df.loc[i, 'Entry_FVG_Top'] = active_bullish_fvg_top
                    df.loc[i, 'Entry_FVG_Bottom'] = active_bullish_fvg_bottom
                # Reset the FVG after entry signal
                active_bullish_fvg_top = None
                active_bullish_fvg_bottom = None
    
    return df

def simulate_trades_scenario_a(df):
    """
    Scenario A: Candle-Based SL (Aggressive)
    Long SL: Low of Signal Candle
    Short SL: High of Signal Candle
    """
    trades = []
    
    for i in range(len(df)):
        # Long Entry
        if df.loc[i, 'Long_Entry']:
            entry_price = df.loc[i, 'Close']
            sl_price = df.loc[i, 'Low']  # Signal candle low
            sl_distance = entry_price - sl_price
            
            if sl_distance <= 0:
                continue  # Skip invalid trades
            
            # Calculate TPs based on risk
            tp_1r = entry_price + (1.0 * sl_distance)
            tp_1_5r = entry_price + (1.5 * sl_distance)
            tp_2r = entry_price + (2.0 * sl_distance)
            
            # Simulate trade from next candle onwards
            trade_result = simulate_trade_exit(df, i+1, 'LONG', entry_price, sl_price, 
                                               tp_1r, tp_1_5r, tp_2r, sl_distance)
            if trade_result:
                trades.append({
                    'Entry_Index': i,
                    'Entry_Time': df.loc[i, 'Datetime'],
                    'Direction': 'LONG',
                    'Entry_Price': entry_price,
                    'SL_Price': sl_price,
                    'SL_Distance': sl_distance,
                    'TP_1R': tp_1r,
                    'TP_1_5R': tp_1_5r,
                    'TP_2R': tp_2r,
                    **trade_result
                })
        
        # Short Entry
        if df.loc[i, 'Short_Entry']:
            entry_price = df.loc[i, 'Close']
            sl_price = df.loc[i, 'High']  # Signal candle high
            sl_distance = sl_price - entry_price
            
            if sl_distance <= 0:
                continue  # Skip invalid trades
            
            # Calculate TPs based on risk
            tp_1r = entry_price - (1.0 * sl_distance)
            tp_1_5r = entry_price - (1.5 * sl_distance)
            tp_2r = entry_price - (2.0 * sl_distance)
            
            # Simulate trade from next candle onwards
            trade_result = simulate_trade_exit(df, i+1, 'SHORT', entry_price, sl_price,
                                               tp_1r, tp_1_5r, tp_2r, sl_distance)
            if trade_result:
                trades.append({
                    'Entry_Index': i,
                    'Entry_Time': df.loc[i, 'Datetime'],
                    'Direction': 'SHORT',
                    'Entry_Price': entry_price,
                    'SL_Price': sl_price,
                    'SL_Distance': sl_distance,
                    'TP_1R': tp_1r,
                    'TP_1_5R': tp_1_5r,
                    'TP_2R': tp_2r,
                    **trade_result
                })
    
    return pd.DataFrame(trades)

def simulate_trades_scenario_b(df):
    """
    Scenario B: Structure-Based SL (Conservative)
    Long SL: Bottom of FVG area
    Short SL: Top of FVG area
    """
    trades = []
    
    for i in range(len(df)):
        # Long Entry (Bearish FVG Inversion)
        if df.loc[i, 'Long_Entry']:
            entry_price = df.loc[i, 'Close']
            sl_price = df.loc[i, 'Entry_FVG_Bottom']  # Bottom of FVG
            sl_distance = entry_price - sl_price
            
            if sl_distance <= 0 or pd.isna(sl_price):
                continue  # Skip invalid trades
            
            # Calculate TPs based on risk
            tp_1r = entry_price + (1.0 * sl_distance)
            tp_1_5r = entry_price + (1.5 * sl_distance)
            tp_2r = entry_price + (2.0 * sl_distance)
            
            # Simulate trade from next candle onwards
            trade_result = simulate_trade_exit(df, i+1, 'LONG', entry_price, sl_price,
                                               tp_1r, tp_1_5r, tp_2r, sl_distance)
            if trade_result:
                trades.append({
                    'Entry_Index': i,
                    'Entry_Time': df.loc[i, 'Datetime'],
                    'Direction': 'LONG',
                    'Entry_Price': entry_price,
                    'SL_Price': sl_price,
                    'SL_Distance': sl_distance,
                    'TP_1R': tp_1r,
                    'TP_1_5R': tp_1_5r,
                    'TP_2R': tp_2r,
                    **trade_result
                })
        
        # Short Entry (Bullish FVG Inversion)
        if df.loc[i, 'Short_Entry']:
            entry_price = df.loc[i, 'Close']
            sl_price = df.loc[i, 'Entry_FVG_Top']  # Top of FVG
            sl_distance = sl_price - entry_price
            
            if sl_distance <= 0 or pd.isna(sl_price):
                continue  # Skip invalid trades
            
            # Calculate TPs based on risk
            tp_1r = entry_price - (1.0 * sl_distance)
            tp_1_5r = entry_price - (1.5 * sl_distance)
            tp_2r = entry_price - (2.0 * sl_distance)
            
            # Simulate trade from next candle onwards
            trade_result = simulate_trade_exit(df, i+1, 'SHORT', entry_price, sl_price,
                                               tp_1r, tp_1_5r, tp_2r, sl_distance)
            if trade_result:
                trades.append({
                    'Entry_Index': i,
                    'Entry_Time': df.loc[i, 'Datetime'],
                    'Direction': 'SHORT',
                    'Entry_Price': entry_price,
                    'SL_Price': sl_price,
                    'SL_Distance': sl_distance,
                    'TP_1R': tp_1r,
                    'TP_1_5R': tp_1_5r,
                    'TP_2R': tp_2r,
                    **trade_result
                })
    
    return pd.DataFrame(trades)

def simulate_trade_exit(df, start_idx, direction, entry_price, sl_price,
                       tp_1r, tp_1_5r, tp_2r, sl_distance):
    """
    Simulate trade exit by checking each subsequent candle
    Returns dict with exit info or None if no valid exit
    """
    if start_idx >= len(df):
        return None
    
    for i in range(start_idx, len(df)):
        low = df.loc[i, 'Low']
        high = df.loc[i, 'High']
        
        if direction == 'LONG':
            # Check if SL hit
            if low <= sl_price:
                return {
                    'Exit_Index': i,
                    'Exit_Time': df.loc[i, 'Datetime'],
                    'Exit_Type': 'SL',
                    'Exit_Price': sl_price,
                    'PnL_Points': sl_price - entry_price,
                    'PnL_R': -1.0
                }
            # Check TPs in order (2R, 1.5R, 1R)
            if high >= tp_2r:
                return {
                    'Exit_Index': i,
                    'Exit_Time': df.loc[i, 'Datetime'],
                    'Exit_Type': 'TP_2R',
                    'Exit_Price': tp_2r,
                    'PnL_Points': tp_2r - entry_price,
                    'PnL_R': 2.0
                }
            if high >= tp_1_5r:
                return {
                    'Exit_Index': i,
                    'Exit_Time': df.loc[i, 'Datetime'],
                    'Exit_Type': 'TP_1.5R',
                    'Exit_Price': tp_1_5r,
                    'PnL_Points': tp_1_5r - entry_price,
                    'PnL_R': 1.5
                }
            if high >= tp_1r:
                return {
                    'Exit_Index': i,
                    'Exit_Time': df.loc[i, 'Datetime'],
                    'Exit_Type': 'TP_1R',
                    'Exit_Price': tp_1r,
                    'PnL_Points': tp_1r - entry_price,
                    'PnL_R': 1.0
                }
        
        else:  # SHORT
            # Check if SL hit
            if high >= sl_price:
                return {
                    'Exit_Index': i,
                    'Exit_Time': df.loc[i, 'Datetime'],
                    'Exit_Type': 'SL',
                    'Exit_Price': sl_price,
                    'PnL_Points': entry_price - sl_price,
                    'PnL_R': -1.0
                }
            # Check TPs in order (2R, 1.5R, 1R)
            if low <= tp_2r:
                return {
                    'Exit_Index': i,
                    'Exit_Time': df.loc[i, 'Datetime'],
                    'Exit_Type': 'TP_2R',
                    'Exit_Price': tp_2r,
                    'PnL_Points': entry_price - tp_2r,
                    'PnL_R': 2.0
                }
            if low <= tp_1_5r:
                return {
                    'Exit_Index': i,
                    'Exit_Time': df.loc[i, 'Datetime'],
                    'Exit_Type': 'TP_1.5R',
                    'Exit_Price': tp_1_5r,
                    'PnL_Points': entry_price - tp_1_5r,
                    'PnL_R': 1.5
                }
            if low <= tp_1r:
                return {
                    'Exit_Index': i,
                    'Exit_Time': df.loc[i, 'Datetime'],
                    'Exit_Type': 'TP_1R',
                    'Exit_Price': tp_1r,
                    'PnL_Points': entry_price - tp_1r,
                    'PnL_R': 1.0
                }
    
    return None  # Trade didn't exit within data range

def calculate_metrics(trades_df):
    """Calculate performance metrics"""
    if len(trades_df) == 0:
        return {
            'Total_Trades': 0,
            'Win_Rate': 0,
            'Total_Return_R': 0,
            'Avg_Win_R': 0,
            'Avg_Loss_R': 0,
            'Long_Trades': 0,
            'Short_Trades': 0,
            'TP_1R_Count': 0,
            'TP_1_5R_Count': 0,
            'TP_2R_Count': 0,
            'SL_Count': 0
        }
    
    total_trades = len(trades_df)
    winning_trades = trades_df[trades_df['PnL_R'] > 0]
    losing_trades = trades_df[trades_df['PnL_R'] < 0]
    
    win_rate = (len(winning_trades) / total_trades * 100) if total_trades > 0 else 0
    total_return_r = trades_df['PnL_R'].sum()
    avg_win_r = winning_trades['PnL_R'].mean() if len(winning_trades) > 0 else 0
    avg_loss_r = losing_trades['PnL_R'].mean() if len(losing_trades) > 0 else 0
    
    long_trades = len(trades_df[trades_df['Direction'] == 'LONG'])
    short_trades = len(trades_df[trades_df['Direction'] == 'SHORT'])
    
    tp_1r_count = len(trades_df[trades_df['Exit_Type'] == 'TP_1R'])
    tp_1_5r_count = len(trades_df[trades_df['Exit_Type'] == 'TP_1.5R'])
    tp_2r_count = len(trades_df[trades_df['Exit_Type'] == 'TP_2R'])
    sl_count = len(trades_df[trades_df['Exit_Type'] == 'SL'])
    
    return {
        'Total_Trades': total_trades,
        'Win_Rate': win_rate,
        'Total_Return_R': total_return_r,
        'Avg_Win_R': avg_win_r,
        'Avg_Loss_R': avg_loss_r,
        'Long_Trades': long_trades,
        'Short_Trades': short_trades,
        'TP_1R_Count': tp_1r_count,
        'TP_1_5R_Count': tp_1_5r_count,
        'TP_2R_Count': tp_2r_count,
        'SL_Count': sl_count
    }

def print_comparative_report(metrics_a, metrics_b):
    """Print comparative report for both scenarios"""
    print("\n" + "="*80)
    print("FVG STRATEGY BACKTEST - STOP LOSS COMPARISON")
    print("="*80)
    print("\nTime Window: 01:00 - 05:00")
    print("Strategy: FVG (Fair Value Gap) Inversion")
    print("Take Profit Targets: 1R, 1.5R, 2R")
    print("\n" + "="*80)
    
    print("\nSCENARIO A: CANDLE-BASED SL (AGGRESSIVE)")
    print("-" * 80)
    print(f"Total Trades:        {metrics_a['Total_Trades']}")
    print(f"  - Long Trades:     {metrics_a['Long_Trades']}")
    print(f"  - Short Trades:    {metrics_a['Short_Trades']}")
    print(f"Win Rate:            {metrics_a['Win_Rate']:.2f}%")
    print(f"Total Return:        {metrics_a['Total_Return_R']:.2f}R")
    print(f"Average Win:         {metrics_a['Avg_Win_R']:.2f}R")
    print(f"Average Loss:        {metrics_a['Avg_Loss_R']:.2f}R")
    print(f"\nExit Distribution:")
    print(f"  - TP 1R:           {metrics_a['TP_1R_Count']}")
    print(f"  - TP 1.5R:         {metrics_a['TP_1_5R_Count']}")
    print(f"  - TP 2R:           {metrics_a['TP_2R_Count']}")
    print(f"  - Stop Loss:       {metrics_a['SL_Count']}")
    
    print("\n" + "="*80)
    print("\nSCENARIO B: STRUCTURE-BASED SL (CONSERVATIVE)")
    print("-" * 80)
    print(f"Total Trades:        {metrics_b['Total_Trades']}")
    print(f"  - Long Trades:     {metrics_b['Long_Trades']}")
    print(f"  - Short Trades:    {metrics_b['Short_Trades']}")
    print(f"Win Rate:            {metrics_b['Win_Rate']:.2f}%")
    print(f"Total Return:        {metrics_b['Total_Return_R']:.2f}R")
    print(f"Average Win:         {metrics_b['Avg_Win_R']:.2f}R")
    print(f"Average Loss:        {metrics_b['Avg_Loss_R']:.2f}R")
    print(f"\nExit Distribution:")
    print(f"  - TP 1R:           {metrics_b['TP_1R_Count']}")
    print(f"  - TP 1.5R:         {metrics_b['TP_1_5R_Count']}")
    print(f"  - TP 2R:           {metrics_b['TP_2R_Count']}")
    print(f"  - Stop Loss:       {metrics_b['SL_Count']}")
    
    print("\n" + "="*80)
    print("\nCOMPARATIVE ANALYSIS")
    print("-" * 80)
    
    trade_diff = metrics_b['Total_Trades'] - metrics_a['Total_Trades']
    win_rate_diff = metrics_b['Win_Rate'] - metrics_a['Win_Rate']
    return_diff = metrics_b['Total_Return_R'] - metrics_a['Total_Return_R']
    
    print(f"Trade Count Difference:     {trade_diff:+d} (Scenario B vs A)")
    print(f"Win Rate Difference:        {win_rate_diff:+.2f}% (Scenario B vs A)")
    print(f"Total Return Difference:    {return_diff:+.2f}R (Scenario B vs A)")
    
    if metrics_b['Total_Return_R'] > metrics_a['Total_Return_R']:
        print(f"\n🏆 WINNER: Scenario B (Structure-Based SL) performs better!")
    elif metrics_a['Total_Return_R'] > metrics_b['Total_Return_R']:
        print(f"\n🏆 WINNER: Scenario A (Candle-Based SL) performs better!")
    else:
        print(f"\n🤝 RESULT: Both scenarios perform equally.")
    
    print("="*80 + "\n")

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
    
    print("\nIdentifying entry signals (01:00-05:00 window)...")
    df = identify_entries(df)
    long_entries = df['Long_Entry'].sum()
    short_entries = df['Short_Entry'].sum()
    print(f"Found {long_entries} Long entries and {short_entries} Short entries")
    
    print("\nSimulating trades for Scenario A (Candle-Based SL)...")
    trades_a = simulate_trades_scenario_a(df)
    
    print("Simulating trades for Scenario B (Structure-Based SL)...")
    trades_b = simulate_trades_scenario_b(df)
    
    print("\nCalculating metrics...")
    metrics_a = calculate_metrics(trades_a)
    metrics_b = calculate_metrics(trades_b)
    
    # Print comparative report
    print_comparative_report(metrics_a, metrics_b)
    
    # Save detailed trade logs
    if len(trades_a) > 0:
        trades_a.to_csv('trades_scenario_a.csv', index=False)
        print("Detailed trades saved to: trades_scenario_a.csv")
    
    if len(trades_b) > 0:
        trades_b.to_csv('trades_scenario_b.csv', index=False)
        print("Detailed trades saved to: trades_scenario_b.csv")

if __name__ == "__main__":
    main()

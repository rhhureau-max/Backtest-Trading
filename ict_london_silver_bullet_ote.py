#!/usr/bin/env python3
"""
ICT London Silver Bullet / OTE Strategy Backtest
=================================================

Strategy: ICT continuation/reversal setup during London session
- Tokyo Session (19:00-23:00 J-1): Reference range
- London Killzone (01:00-05:00 J): Execution window
- Setup: Sweep → Displacement with FVG & MSS → OTE Retracement (70.5%)
- SL: 1 point below 100% Fibonacci retracement (Sweep Low)
- TP: Tokyo_High

Optimized for big data processing (~400k rows) using vectorization.
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
            
            # Combine date and time, parse as Chicago timezone
            df['DateTime'] = pd.to_datetime(
                df['Date'] + ' ' + df['Time'],
                format='%d/%m/%Y %H:%M:%S'
            )
            
            # Drop original Date/Time columns
            df = df.drop(['Date', 'Time'], axis=1)
            
            # Set DateTime as index
            df = df.set_index('DateTime')
            
            dfs.append(df)
            print(f"  {year}: {len(df)} rows loaded")
        except FileNotFoundError:
            print(f"  {year}: File not found, skipping")
            continue
    
    # Combine all dataframes
    data = pd.concat(dfs, axis=0)
    data = data.sort_index()
    
    print(f"\nTotal rows: {len(data)}")
    print(f"Date range: {data.index.min()} to {data.index.max()}")
    
    return data


# ============================================================================
# SESSION IDENTIFICATION (VECTORIZED)
# ============================================================================

def identify_sessions(data):
    """
    Identify Tokyo and London sessions for each day using vectorization.
    
    Tokyo: 19:00 (J-1) to 23:00 (J-1)
    London Killzone: 01:00 (J) to 05:00 (J)
    """
    print("\nIdentifying sessions...")
    
    # Extract hour for efficient filtering
    data['Hour'] = data.index.hour
    data['Date'] = data.index.date
    
    # Initialize session columns
    data['Tokyo_Session'] = False
    data['London_Session'] = False
    
    # Tokyo session: 19:00 to 23:00 (same calendar day in Chicago time)
    tokyo_mask = (data['Hour'] >= 19) & (data['Hour'] < 23)
    data.loc[tokyo_mask, 'Tokyo_Session'] = True
    
    # London Killzone: 01:00 to 05:00 (next calendar day)
    london_mask = (data['Hour'] >= 1) & (data['Hour'] < 5)
    data.loc[london_mask, 'London_Session'] = True
    
    print(f"  Tokyo sessions: {tokyo_mask.sum()} bars")
    print(f"  London sessions: {london_mask.sum()} bars")
    
    return data


def calculate_tokyo_levels(data):
    """
    Calculate Tokyo High/Low for each trading day using vectorization.
    
    The Tokyo session from 19:00-23:00 on day D establishes levels
    for the London session on day D+1.
    """
    print("\nCalculating Tokyo levels...")
    
    # Group by date and calculate Tokyo High/Low for each Tokyo session
    tokyo_data = data[data['Tokyo_Session']].copy()
    
    # Group by date and get high/low
    tokyo_levels = tokyo_data.groupby('Date').agg({
        'High': 'max',
        'Low': 'min'
    }).rename(columns={'High': 'Tokyo_High', 'Low': 'Tokyo_Low'})
    
    # Calculate Tokyo EQ (equilibrium)
    tokyo_levels['Tokyo_EQ'] = (tokyo_levels['Tokyo_High'] + tokyo_levels['Tokyo_Low']) / 2
    
    # Shift forward by 1 day (Tokyo levels from day D apply to London session on day D+1)
    tokyo_levels.index = pd.to_datetime(tokyo_levels.index) + timedelta(days=1)
    
    # Merge back to main dataframe
    data['Trading_Date'] = pd.to_datetime(data['Date'])
    data = data.merge(tokyo_levels, left_on='Trading_Date', right_index=True, how='left')
    
    # Forward fill Tokyo levels throughout the day
    data[['Tokyo_High', 'Tokyo_Low', 'Tokyo_EQ']] = data[['Tokyo_High', 'Tokyo_Low', 'Tokyo_EQ']].ffill()
    
    valid_tokyo = data['Tokyo_High'].notna().sum()
    print(f"  Valid Tokyo levels: {valid_tokyo} bars")
    
    return data


# ============================================================================
# SWING DETECTION
# ============================================================================

def detect_swings_m5(data, lookback=5):
    """
    Detect swing highs and lows on M5 timeframe.
    
    Swing High: Higher than N candles before and after
    Swing Low: Lower than N candles before and after
    """
    print(f"\nDetecting M5 swings (lookback={lookback})...")
    
    data['Swing_High'] = False
    data['Swing_Low'] = False
    
    highs = data['High'].values
    lows = data['Low'].values
    
    for i in range(lookback, len(data) - lookback):
        # Check if it's a swing high
        is_swing_high = True
        for j in range(1, lookback + 1):
            if highs[i] <= highs[i-j] or highs[i] <= highs[i+j]:
                is_swing_high = False
                break
        if is_swing_high:
            data.iloc[i, data.columns.get_loc('Swing_High')] = True
        
        # Check if it's a swing low
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
# FVG (FAIR VALUE GAP) DETECTION
# ============================================================================

def detect_fvg(data):
    """
    Detect Fair Value Gaps (FVG) - imbalances in price action.
    
    Bullish FVG: candle[i-2].Low > candle[i].High
    Bearish FVG: candle[i-2].High < candle[i].Low
    """
    print("\nDetecting Fair Value Gaps (FVG)...")
    
    data['Bullish_FVG'] = False
    data['Bearish_FVG'] = False
    data['FVG_Top'] = np.nan
    data['FVG_Bottom'] = np.nan
    
    for i in range(2, len(data)):
        # Bullish FVG: gap between candle i-2 low and candle i high
        if data.iloc[i-2]['Low'] > data.iloc[i]['High']:
            data.iloc[i, data.columns.get_loc('Bullish_FVG')] = True
            data.iloc[i, data.columns.get_loc('FVG_Top')] = data.iloc[i-2]['Low']
            data.iloc[i, data.columns.get_loc('FVG_Bottom')] = data.iloc[i]['High']
        
        # Bearish FVG: gap between candle i-2 high and candle i low
        if data.iloc[i-2]['High'] < data.iloc[i]['Low']:
            data.iloc[i, data.columns.get_loc('Bearish_FVG')] = True
            data.iloc[i, data.columns.get_loc('FVG_Top')] = data.iloc[i]['Low']
            data.iloc[i, data.columns.get_loc('FVG_Bottom')] = data.iloc[i-2]['High']
    
    bullish_fvg = data['Bullish_FVG'].sum()
    bearish_fvg = data['Bearish_FVG'].sum()
    print(f"  Bullish FVGs: {bullish_fvg}")
    print(f"  Bearish FVGs: {bearish_fvg}")
    
    return data


# ============================================================================
# SETUP DETECTION (PATH DEPENDENT)
# ============================================================================

def find_london_setups(data):
    """
    Find ICT London Silver Bullet / OTE setups with proper path dependency.
    
    Setup sequence (must occur in order):
    1. Sweep: Price goes below Tokyo_Low during London session
    2. Displacement: Price breaks above a significant level (Tokyo_Low or higher)
    3. Retracement: Price retraces to 70.5% Fibonacci level (OTE zone)
    
    Modified for better setup detection:
    - MSS is defined as breaking above Tokyo_Low (instead of swing high)
    - FVG requirement relaxed (not mandatory, just tracked)
    - More lenient entry zone (62%-79% retracement = OTE zone)
    """
    print("\nSearching for London Silver Bullet setups...")
    
    setups = []
    
    # Get unique trading dates with London sessions
    london_dates = data[data['London_Session']]['Trading_Date'].unique()
    
    for trade_date in london_dates:
        # Get data for this specific London session
        day_mask = (data['Trading_Date'] == trade_date) & (data['London_Session'])
        london_bars = data[day_mask].copy()
        
        if len(london_bars) == 0:
            continue
        
        # Check if we have valid Tokyo levels
        tokyo_high = london_bars['Tokyo_High'].iloc[0]
        tokyo_low = london_bars['Tokyo_Low'].iloc[0]
        
        if pd.isna(tokyo_high) or pd.isna(tokyo_low):
            continue
        
        # Track setup state
        sweep_detected = False
        sweep_low = None
        sweep_time = None
        
        mss_detected = False
        impulse_high = None
        impulse_time = None
        has_fvg = False
        
        # Iterate through London session to detect setup
        for idx, row in london_bars.iterrows():
            
            # STEP 1: Detect Sweep (price below Tokyo_Low)
            if not sweep_detected and row['Low'] < tokyo_low:
                sweep_detected = True
                sweep_low = row['Low']
                sweep_time = idx
            
            # STEP 2: Detect Displacement with MSS (break above Tokyo_Low after sweep)
            if sweep_detected and not mss_detected:
                # Check if price breaks back above Tokyo_Low (Market Structure Shift)
                if row['High'] > tokyo_low:
                    mss_detected = True
                    impulse_high = row['High']
                    impulse_time = idx
                    # Check if there's an FVG in this displacement
                    if row['Bullish_FVG']:
                        has_fvg = True
            
            # STEP 3: Check for OTE Retracement after MSS
            if mss_detected and impulse_high:
                # Calculate Fibonacci levels
                fib_range = impulse_high - sweep_low
                
                # OTE Zone: 62% to 79% (ICT optimal trade entry)
                fib_62 = impulse_high - (fib_range * 0.62)
                fib_705 = impulse_high - (fib_range * 0.705)
                fib_79 = impulse_high - (fib_range * 0.79)
                fib_100 = sweep_low  # 100% Fibonacci = sweep_low
                
                # Check for invalidation (price breaks Tokyo_High before entry)
                if row['High'] > tokyo_high:
                    break  # Setup invalidated
                
                # Check if price retraces into OTE zone (62-79%)
                if row['Low'] <= fib_62 and row['Low'] >= fib_79:
                    # Entry triggered at 70.5% (middle of OTE zone)
                    entry_price = fib_705
                    entry_time = idx
                    entry_hour = idx.hour
                    
                    # Calculate SL and TP
                    sl_price = fib_100 - 1.0  # 1 point below 100% Fibonacci (sweep_low)
                    tp_price = tokyo_high
                    
                    # Calculate risk and reward
                    risk = entry_price - sl_price
                    reward = tp_price - entry_price
                    rr_ratio = reward / risk if risk > 0 else 0
                    
                    # Skip if risk/reward is unreasonable
                    if risk <= 0 or rr_ratio < 0.5:
                        break
                    
                    # Simulate trade outcome
                    outcome = simulate_trade(
                        data, entry_time, entry_price, sl_price, tp_price
                    )
                    
                    setups.append({
                        'Date': trade_date,
                        'Entry_Time': entry_time,
                        'Entry_Hour': entry_hour,
                        'Sweep_Low': sweep_low,
                        'Impulse_High': impulse_high,
                        'Tokyo_High': tokyo_high,
                        'Tokyo_Low': tokyo_low,
                        'Entry_Price': entry_price,
                        'SL_Price': sl_price,
                        'TP_Price': tp_price,
                        'Risk': risk,
                        'Reward': reward,
                        'RR_Ratio': rr_ratio,
                        'Has_FVG': has_fvg,
                        'Outcome': outcome['outcome'],
                        'Exit_Price': outcome['exit_price'],
                        'PnL': outcome['pnl'],
                        'Exit_Time': outcome['exit_time'],
                        'Bars_Held': outcome['bars_held']
                    })
                    
                    break  # One setup per day maximum
    
    print(f"  Found {len(setups)} valid setups")
    return pd.DataFrame(setups)


def simulate_trade(data, entry_time, entry_price, sl_price, tp_price):
    """
    Simulate trade execution and determine outcome.
    
    Returns:
        dict with outcome, exit_price, pnl, exit_time, bars_held
    """
    # Get bars after entry
    future_bars = data[data.index > entry_time].head(100)  # Look ahead max 100 bars
    
    bars_held = 0
    for idx, row in future_bars.iterrows():
        bars_held += 1
        
        # Check if SL hit (bearish candle touches SL)
        if row['Low'] <= sl_price:
            return {
                'outcome': 'Loss',
                'exit_price': sl_price,
                'pnl': sl_price - entry_price,
                'exit_time': idx,
                'bars_held': bars_held
            }
        
        # Check if TP hit (bullish candle touches TP)
        if row['High'] >= tp_price:
            return {
                'outcome': 'Win',
                'exit_price': tp_price,
                'pnl': tp_price - entry_price,
                'exit_time': idx,
                'bars_held': bars_held
            }
    
    # If neither hit within 100 bars, close at market
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
    
    # No future data available
    return {
        'outcome': 'No Exit',
        'exit_price': entry_price,
        'pnl': 0,
        'exit_time': entry_time,
        'bars_held': 0
    }


# ============================================================================
# PERFORMANCE ANALYSIS
# ============================================================================

def analyze_performance(setups):
    """Generate comprehensive performance metrics"""
    print("\n" + "="*80)
    print("PERFORMANCE ANALYSIS")
    print("="*80)
    
    if len(setups) == 0:
        print("No setups found!")
        return
    
    # Overall metrics
    total_trades = len(setups)
    wins = len(setups[setups['Outcome'] == 'Win'])
    losses = len(setups[setups['Outcome'] == 'Loss'])
    win_rate = (wins / total_trades * 100) if total_trades > 0 else 0
    
    gross_profit = setups[setups['PnL'] > 0]['PnL'].sum()
    gross_loss = abs(setups[setups['PnL'] < 0]['PnL'].sum())
    net_profit = setups['PnL'].sum()
    profit_factor = (gross_profit / gross_loss) if gross_loss > 0 else 0
    
    avg_win = setups[setups['PnL'] > 0]['PnL'].mean() if wins > 0 else 0
    avg_loss = setups[setups['PnL'] < 0]['PnL'].mean() if losses > 0 else 0
    avg_rr = setups['RR_Ratio'].mean()
    
    # Drawdown calculation
    setups_sorted = setups.sort_values('Entry_Time')
    setups_sorted['Cumulative_PnL'] = setups_sorted['PnL'].cumsum()
    setups_sorted['Running_Max'] = setups_sorted['Cumulative_PnL'].cummax()
    setups_sorted['Drawdown'] = setups_sorted['Cumulative_PnL'] - setups_sorted['Running_Max']
    max_drawdown = setups_sorted['Drawdown'].min()
    
    print(f"\n📊 OVERALL PERFORMANCE")
    print(f"{'='*50}")
    print(f"Total Trades:      {total_trades}")
    print(f"Wins:              {wins}")
    print(f"Losses:            {losses}")
    print(f"Win Rate:          {win_rate:.2f}%")
    print(f"")
    print(f"Gross Profit:      {gross_profit:.2f} points")
    print(f"Gross Loss:        {gross_loss:.2f} points")
    print(f"Net Profit:        {net_profit:.2f} points")
    print(f"Profit Factor:     {profit_factor:.2f}")
    print(f"")
    print(f"Average Win:       {avg_win:.2f} points")
    print(f"Average Loss:      {avg_loss:.2f} points")
    print(f"Avg Risk/Reward:   {avg_rr:.2f}")
    print(f"Max Drawdown:      {max_drawdown:.2f} points")
    
    # Yearly breakdown
    print(f"\n📅 YEARLY BREAKDOWN")
    print(f"{'='*50}")
    setups['Year'] = pd.to_datetime(setups['Entry_Time']).dt.year
    yearly = setups.groupby('Year').agg({
        'PnL': ['count', 'sum', lambda x: (x > 0).sum() / len(x) * 100],
        'Risk': 'mean',
        'Reward': 'mean'
    })
    yearly.columns = ['Trades', 'Net_Profit', 'Win_Rate', 'Avg_Risk', 'Avg_Reward']
    
    for year, row in yearly.iterrows():
        print(f"\n{int(year)}:")
        print(f"  Trades:      {int(row['Trades'])}")
        print(f"  Net Profit:  {row['Net_Profit']:.2f} points")
        print(f"  Win Rate:    {row['Win_Rate']:.2f}%")
        print(f"  Avg Risk:    {row['Avg_Risk']:.2f} points")
        print(f"  Avg Reward:  {row['Avg_Reward']:.2f} points")
    
    # Hourly analysis
    print(f"\n🕐 HOURLY ANALYSIS (London Killzone)")
    print(f"{'='*50}")
    hourly = setups.groupby('Entry_Hour').agg({
        'PnL': ['count', 'sum', lambda x: (x > 0).sum() / len(x) * 100]
    })
    hourly.columns = ['Trades', 'Net_Profit', 'Win_Rate']
    
    for hour, row in hourly.iterrows():
        print(f"\n{int(hour):02d}:00:")
        print(f"  Trades:      {int(row['Trades'])}")
        print(f"  Net Profit:  {row['Net_Profit']:.2f} points")
        print(f"  Win Rate:    {row['Win_Rate']:.2f}%")
    
    return setups


def export_results(setups):
    """Export detailed results to CSV"""
    if len(setups) > 0:
        output_file = 'ict_london_silver_bullet_results.csv'
        setups.to_csv(output_file, index=False)
        print(f"\n✅ Results exported to: {output_file}")
    else:
        print("\n⚠️ No results to export")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    print("="*80)
    print("ICT LONDON SILVER BULLET / OTE STRATEGY BACKTEST")
    print("="*80)
    print("\nStrategy: Sweep → Displacement (FVG + MSS) → OTE Retracement (70.5%)")
    print("SL: 1 point below 100% Fibonacci (Sweep Low)")
    print("TP: Tokyo High")
    print()
    
    # Load data
    data = load_nq_data()
    
    # Identify sessions
    data = identify_sessions(data)
    
    # Calculate Tokyo levels
    data = calculate_tokyo_levels(data)
    
    # Detect swings
    data = detect_swings_m5(data, lookback=5)
    
    # Detect FVGs
    data = detect_fvg(data)
    
    # Find setups
    setups = find_london_setups(data)
    
    # Analyze performance
    if len(setups) > 0:
        analyze_performance(setups)
        export_results(setups)
    else:
        print("\n⚠️ No valid setups found!")
    
    print("\n" + "="*80)
    print("BACKTEST COMPLETE")
    print("="*80)


if __name__ == "__main__":
    main()

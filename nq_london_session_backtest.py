#!/usr/bin/env python3
"""
NQ Futures London Session Backtesting Script (JST Time)
========================================================

This script analyzes NQ futures trading strategies focused on the London session
with all times displayed in Japan Standard Time (JST).

Author: Trading Analysis System
Date: 2025-12-26
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import pytz
import glob
import warnings
warnings.filterwarnings('ignore')

# =====================================================================
# TIMEZONE CONFIGURATION
# =====================================================================

CST = pytz.timezone('America/Chicago')
JST = pytz.timezone('Asia/Tokyo')

# =====================================================================
# DATA LOADING FUNCTIONS
# =====================================================================

def load_nq_data(base_path, timeframe):
    """
    Load NQ data files for a specific timeframe across all years (2018-2025).
    
    Args:
        base_path: Base directory path
        timeframe: '15m', '1H', '4H', or '1D'
    
    Returns:
        DataFrame with combined data
    """
    pattern = f"{base_path}/*{timeframe}.csv"
    files = glob.glob(pattern)
    
    # Filter to only NQ files (not ES)
    files = [f for f in files if 'ES ' not in f and '/ES ' not in f]
    
    if not files:
        print(f"Warning: No files found for pattern {pattern}")
        return pd.DataFrame()
    
    print(f"Loading {timeframe} data from {len(files)} files...")
    
    dataframes = []
    for file in sorted(files):
        try:
            df = pd.read_csv(file, sep=';', encoding='utf-8-sig')
            df.columns = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
            
            # Combine date and time
            df['DateTime_CT'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], 
                                               format='%d/%m/%Y %H:%M:%S')
            
            # Convert to timezone-aware CST, then to JST
            df['DateTime_CT'] = df['DateTime_CT'].dt.tz_localize(CST, ambiguous='infer', nonexistent='shift_forward')
            df['DateTime_JST'] = df['DateTime_CT'].dt.tz_convert(JST)
            
            # Extract JST components
            df['Date_JST'] = df['DateTime_JST'].dt.date
            df['Time_JST'] = df['DateTime_JST'].dt.time
            df['Hour_JST'] = df['DateTime_JST'].dt.hour
            df['DayOfWeek'] = df['DateTime_JST'].dt.dayofweek  # 0=Monday, 6=Sunday
            
            dataframes.append(df)
            
        except Exception as e:
            print(f"Error loading {file}: {e}")
            continue
    
    if not dataframes:
        return pd.DataFrame()
    
    combined = pd.concat(dataframes, ignore_index=True)
    combined = combined.sort_values('DateTime_JST').reset_index(drop=True)
    
    print(f"Loaded {len(combined)} records for {timeframe}")
    print(f"Date range: {combined['DateTime_JST'].min()} to {combined['DateTime_JST'].max()}")
    
    return combined


def load_es_data(base_path, timeframe):
    """
    Load ES (S&P 500) data for SMT divergence analysis.
    
    Args:
        base_path: Base directory path
        timeframe: '15m', '1h', '4h', or '1D'
    
    Returns:
        DataFrame with ES data
    """
    # ES files use different naming convention
    timeframe_map = {
        '15m': '15m',
        '1H': '1h',
        '4H': '4h',
        '1D': '1D'
    }
    
    tf = timeframe_map.get(timeframe, timeframe)
    pattern = f"{base_path}/ES {tf} (2018-2025).csv"
    
    try:
        df = pd.read_csv(pattern, sep=';', encoding='utf-8-sig')
        df.columns = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
        
        # Combine date and time
        df['DateTime_CT'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], 
                                           format='%d/%m/%Y %H:%M:%S')
        
        # Convert to timezone-aware CST, then to JST
        df['DateTime_CT'] = df['DateTime_CT'].dt.tz_localize(CST, ambiguous='infer', nonexistent='shift_forward')
        df['DateTime_JST'] = df['DateTime_CT'].dt.tz_convert(JST)
        
        # Extract JST components
        df['Date_JST'] = df['DateTime_JST'].dt.date
        df['Hour_JST'] = df['DateTime_JST'].dt.hour
        
        print(f"Loaded ES {timeframe} data: {len(df)} records")
        return df
        
    except Exception as e:
        print(f"Error loading ES data: {e}")
        return pd.DataFrame()


# =====================================================================
# METHOD 1: JUDAS SWING POST-ASIA (CONTRARIAN)
# =====================================================================

def analyze_judas_swing(df_15m):
    """
    Identify Judas Swing setups after Asian session.
    
    Asian Session: 08:00-15:00 JST
    Judas Window: 15:30-17:00 JST
    
    Returns:
        Dictionary with analysis results
    """
    print("\n" + "="*70)
    print("METHOD 1: JUDAS SWING POST-ASIA (CONTRARIAN)")
    print("="*70)
    
    results = {
        'total_days': 0,
        'bearish_setups': 0,
        'bullish_setups': 0,
        'bearish_success': 0,
        'bullish_success': 0,
        'details': []
    }
    
    # Group by date
    df_15m['Date_JST'] = pd.to_datetime(df_15m['Date_JST'])
    
    for date, day_data in df_15m.groupby('Date_JST'):
        # Skip weekends
        if day_data['DayOfWeek'].iloc[0] >= 5:
            continue
        
        # Asian session: 08:00-15:00 JST
        asian_session = day_data[(day_data['Hour_JST'] >= 8) & (day_data['Hour_JST'] < 15)]
        
        if len(asian_session) < 10:  # Need sufficient data
            continue
        
        asian_high = asian_session['High'].max()
        asian_low = asian_session['Low'].min()
        asian_range = asian_high - asian_low
        
        # Judas window: 15:30-17:00 JST
        judas_window = day_data[
            (day_data['Hour_JST'] == 15) & (day_data['DateTime_JST'].dt.minute >= 30) |
            (day_data['Hour_JST'] == 16)
        ]
        
        if len(judas_window) == 0:
            continue
        
        # London session: 16:00-21:00 JST for success validation
        london_session = day_data[(day_data['Hour_JST'] >= 16) & (day_data['Hour_JST'] < 21)]
        
        if len(london_session) == 0:
            continue
        
        results['total_days'] += 1
        
        # Check for false breakout (Judas Swing)
        judas_high = judas_window['High'].max()
        judas_low = judas_window['Low'].min()
        judas_close = judas_window['Close'].iloc[-1] if len(judas_window) > 0 else None
        
        london_high = london_session['High'].max()
        london_low = london_session['Low'].min()
        
        setup_type = None
        success = False
        
        # Bearish setup: Break above Asian High but close back in range
        if judas_high > asian_high and judas_close < asian_high:
            setup_type = 'bearish'
            results['bearish_setups'] += 1
            # Success: London session goes lower
            if london_low < judas_low:
                results['bearish_success'] += 1
                success = True
        
        # Bullish setup: Break below Asian Low but close back in range
        elif judas_low < asian_low and judas_close > asian_low:
            setup_type = 'bullish'
            results['bullish_setups'] += 1
            # Success: London session goes higher
            if london_high > judas_high:
                results['bullish_success'] += 1
                success = True
        
        if setup_type:
            results['details'].append({
                'date': date,
                'setup': setup_type,
                'success': success,
                'asian_high': asian_high,
                'asian_low': asian_low,
                'asian_range': asian_range
            })
    
    # Calculate statistics
    bearish_rate = (results['bearish_success'] / results['bearish_setups'] * 100) if results['bearish_setups'] > 0 else 0
    bullish_rate = (results['bullish_success'] / results['bullish_setups'] * 100) if results['bullish_setups'] > 0 else 0
    
    print(f"\nTotal Trading Days Analyzed: {results['total_days']}")
    print(f"\nBearish Judas Setups: {results['bearish_setups']}")
    print(f"Bearish Success: {results['bearish_success']} ({bearish_rate:.1f}%)")
    print(f"\nBullish Judas Setups: {results['bullish_setups']}")
    print(f"Bullish Success: {results['bullish_success']} ({bullish_rate:.1f}%)")
    
    results['bearish_rate'] = bearish_rate
    results['bullish_rate'] = bullish_rate
    
    return results


# =====================================================================
# METHOD 2: NY MIDNIGHT OPENING RULE (TREND FOLLOW)
# =====================================================================

def analyze_ny_midnight(df_15m):
    """
    Analyze NY Midnight opening rule.
    
    NY Midnight: 13:00 JST (winter) or 14:00 JST (summer/DST)
    Entry time: 16:00 JST (London open)
    
    Returns:
        Dictionary with analysis results
    """
    print("\n" + "="*70)
    print("METHOD 2: NY MIDNIGHT OPENING RULE (TREND FOLLOW)")
    print("="*70)
    
    results = {
        'total_days': 0,
        'bullish_bias': 0,
        'bearish_bias': 0,
        'bullish_success': 0,
        'bearish_success': 0,
        'details': []
    }
    
    df_15m['Date_JST'] = pd.to_datetime(df_15m['Date_JST'])
    
    for date, day_data in df_15m.groupby('Date_JST'):
        # Skip weekends
        if day_data['DayOfWeek'].iloc[0] >= 5:
            continue
        
        # Find NY Midnight (13:00 or 14:00 JST)
        midnight_candidates = day_data[
            ((day_data['Hour_JST'] == 13) | (day_data['Hour_JST'] == 14)) &
            (day_data['DateTime_JST'].dt.minute == 0)
        ]
        
        if len(midnight_candidates) == 0:
            continue
        
        midnight_price = midnight_candidates['Open'].iloc[0]
        
        # Find 16:00 JST entry point
        entry_point = day_data[
            (day_data['Hour_JST'] == 16) &
            (day_data['DateTime_JST'].dt.minute == 0)
        ]
        
        if len(entry_point) == 0:
            continue
        
        entry_price = entry_point['Open'].iloc[0]
        
        # London session for validation (16:00-21:00 JST)
        london_session = day_data[(day_data['Hour_JST'] >= 16) & (day_data['Hour_JST'] < 21)]
        
        if len(london_session) == 0:
            continue
        
        results['total_days'] += 1
        
        london_high = london_session['High'].max()
        london_low = london_session['Low'].min()
        
        bias = None
        success = False
        
        # Bullish bias: price at 16:00 > midnight level
        if entry_price > midnight_price:
            bias = 'bullish'
            results['bullish_bias'] += 1
            # Success: London high exceeds entry by meaningful amount
            if london_high > entry_price * 1.001:  # 0.1% threshold
                results['bullish_success'] += 1
                success = True
        
        # Bearish bias: price at 16:00 < midnight level
        elif entry_price < midnight_price:
            bias = 'bearish'
            results['bearish_bias'] += 1
            # Success: London low goes below entry by meaningful amount
            if london_low < entry_price * 0.999:  # 0.1% threshold
                results['bearish_success'] += 1
                success = True
        
        if bias:
            results['details'].append({
                'date': date,
                'midnight_price': midnight_price,
                'entry_price': entry_price,
                'bias': bias,
                'success': success,
                'london_high': london_high,
                'london_low': london_low
            })
    
    # Calculate statistics
    bullish_rate = (results['bullish_success'] / results['bullish_bias'] * 100) if results['bullish_bias'] > 0 else 0
    bearish_rate = (results['bearish_success'] / results['bearish_bias'] * 100) if results['bearish_bias'] > 0 else 0
    
    print(f"\nTotal Trading Days Analyzed: {results['total_days']}")
    print(f"\nBullish Bias Days: {results['bullish_bias']}")
    print(f"Bullish Success: {results['bullish_success']} ({bullish_rate:.1f}%)")
    print(f"\nBearish Bias Days: {results['bearish_bias']}")
    print(f"Bearish Success: {results['bearish_success']} ({bearish_rate:.1f}%)")
    
    results['bullish_rate'] = bullish_rate
    results['bearish_rate'] = bearish_rate
    
    return results


# =====================================================================
# METHOD 3: H4 MARKET STRUCTURE (TOP-DOWN)
# =====================================================================

def analyze_h4_structure(df_4h, df_1d):
    """
    Analyze H4 market structure and D1 correlation.
    
    Returns:
        Dictionary with analysis results
    """
    print("\n" + "="*70)
    print("METHOD 3: H4 MARKET STRUCTURE (TOP-DOWN)")
    print("="*70)
    
    results = {
        'total_periods': 0,
        'bullish_structure': 0,
        'bearish_structure': 0,
        'bullish_success': 0,
        'bearish_success': 0,
        'details': []
    }
    
    if len(df_4h) < 20 or len(df_1d) < 5:
        print("Insufficient data for H4 analysis")
        return results
    
    df_4h['Date_JST'] = pd.to_datetime(df_4h['Date_JST'])
    df_1d['Date_JST'] = pd.to_datetime(df_1d['Date_JST'])
    
    # Identify swing points (simplified version)
    df_4h['Swing_High'] = (df_4h['High'] > df_4h['High'].shift(1)) & (df_4h['High'] > df_4h['High'].shift(-1))
    df_4h['Swing_Low'] = (df_4h['Low'] < df_4h['Low'].shift(1)) & (df_4h['Low'] < df_4h['Low'].shift(-1))
    
    # Analyze structure over rolling windows
    window_size = 10  # 10 H4 candles = 40 hours
    
    for i in range(window_size, len(df_4h) - 5):
        window = df_4h.iloc[i-window_size:i]
        
        swing_highs = window[window['Swing_High']]['High'].values
        swing_lows = window[window['Swing_Low']]['Low'].values
        
        if len(swing_highs) < 2 or len(swing_lows) < 2:
            continue
        
        results['total_periods'] += 1
        
        # Determine structure
        higher_highs = swing_highs[-1] > swing_highs[-2]
        higher_lows = swing_lows[-1] > swing_lows[-2]
        lower_highs = swing_highs[-1] < swing_highs[-2]
        lower_lows = swing_lows[-1] < swing_lows[-2]
        
        structure = None
        
        if higher_highs and higher_lows:
            structure = 'bullish'
            results['bullish_structure'] += 1
        elif lower_highs and lower_lows:
            structure = 'bearish'
            results['bearish_structure'] += 1
        
        # Check D1 correlation
        current_date = df_4h.iloc[i]['Date_JST']
        d1_candle = df_1d[df_1d['Date_JST'] == current_date]
        
        if len(d1_candle) > 0 and structure:
            d1_close = d1_candle['Close'].iloc[0]
            d1_high = d1_candle['High'].iloc[0]
            d1_low = d1_candle['Low'].iloc[0]
            d1_range = d1_high - d1_low
            
            # Check if D1 closed in top 25%
            d1_top_quarter = (d1_close - d1_low) / d1_range > 0.75 if d1_range > 0 else False
            
            # Validate with next 5 H4 candles
            future = df_4h.iloc[i:i+5]
            future_high = future['High'].max()
            future_low = future['Low'].min()
            current_close = df_4h.iloc[i]['Close']
            
            if structure == 'bullish':
                success = future_high > current_close * 1.002  # 0.2% move up
                if success:
                    results['bullish_success'] += 1
            else:  # bearish
                success = future_low < current_close * 0.998  # 0.2% move down
                if success:
                    results['bearish_success'] += 1
            
            results['details'].append({
                'date': current_date,
                'structure': structure,
                'd1_top_quarter': d1_top_quarter,
                'success': success
            })
    
    # Calculate statistics
    bullish_rate = (results['bullish_success'] / results['bullish_structure'] * 100) if results['bullish_structure'] > 0 else 0
    bearish_rate = (results['bearish_success'] / results['bearish_structure'] * 100) if results['bearish_structure'] > 0 else 0
    
    print(f"\nTotal Periods Analyzed: {results['total_periods']}")
    print(f"\nBullish H4 Structure: {results['bullish_structure']}")
    print(f"Bullish Success: {results['bullish_success']} ({bullish_rate:.1f}%)")
    print(f"\nBearish H4 Structure: {results['bearish_structure']}")
    print(f"Bearish Success: {results['bearish_success']} ({bearish_rate:.1f}%)")
    
    results['bullish_rate'] = bullish_rate
    results['bearish_rate'] = bearish_rate
    
    return results


# =====================================================================
# METHOD 4: SMT DIVERGENCE (ADVANCED)
# =====================================================================

def analyze_smt_divergence(df_nq_15m, df_es_15m):
    """
    Analyze SMT (Smart Money Technique) divergence between NQ and ES.
    
    Window: 14:00-16:00 JST
    
    Returns:
        Dictionary with analysis results
    """
    print("\n" + "="*70)
    print("METHOD 4: SMT DIVERGENCE (ADVANCED)")
    print("="*70)
    
    results = {
        'total_days': 0,
        'bullish_smt': 0,
        'bearish_smt': 0,
        'bullish_success': 0,
        'bearish_success': 0,
        'details': []
    }
    
    if df_es_15m.empty:
        print("ES data not available for SMT analysis")
        return results
    
    df_nq_15m['Date_JST'] = pd.to_datetime(df_nq_15m['Date_JST'])
    df_es_15m['Date_JST'] = pd.to_datetime(df_es_15m['Date_JST'])
    
    # Merge on datetime for comparison
    merged = pd.merge(
        df_nq_15m[['DateTime_JST', 'Date_JST', 'High', 'Low', 'Close', 'Hour_JST', 'DayOfWeek']],
        df_es_15m[['DateTime_JST', 'High', 'Low', 'Close']],
        on='DateTime_JST',
        suffixes=('_NQ', '_ES'),
        how='inner'
    )
    
    for date, day_data in merged.groupby('Date_JST'):
        # Skip weekends
        if day_data['DayOfWeek'].iloc[0] >= 5:
            continue
        
        # SMT window: 14:00-16:00 JST
        smt_window = day_data[(day_data['Hour_JST'] >= 14) & (day_data['Hour_JST'] < 16)]
        
        if len(smt_window) < 4:  # Need at least 4 candles
            continue
        
        nq_high = smt_window['High_NQ'].max()
        nq_low = smt_window['Low_NQ'].min()
        es_high = smt_window['High_ES'].max()
        es_low = smt_window['Low_ES'].min()
        
        # Get previous window for comparison
        prev_window = day_data[(day_data['Hour_JST'] >= 12) & (day_data['Hour_JST'] < 14)]
        
        if len(prev_window) < 2:
            continue
        
        prev_nq_high = prev_window['High_NQ'].max()
        prev_nq_low = prev_window['Low_NQ'].min()
        prev_es_high = prev_window['High_ES'].max()
        prev_es_low = prev_window['Low_ES'].min()
        
        # London session for validation (16:00-21:00 JST)
        london = day_data[(day_data['Hour_JST'] >= 16) & (day_data['Hour_JST'] < 21)]
        
        if len(london) == 0:
            continue
        
        results['total_days'] += 1
        
        divergence = None
        success = False
        
        # Bullish SMT: NQ makes lower low, ES makes higher low
        if nq_low < prev_nq_low and es_low > prev_es_low:
            divergence = 'bullish'
            results['bullish_smt'] += 1
            # Success: London session moves up
            if london['High_NQ'].max() > smt_window['Close_NQ'].iloc[-1] * 1.001:
                results['bullish_success'] += 1
                success = True
        
        # Bearish SMT: NQ makes higher high, ES fails to make higher high
        elif nq_high > prev_nq_high and es_high <= prev_es_high:
            divergence = 'bearish'
            results['bearish_smt'] += 1
            # Success: London session moves down
            if london['Low_NQ'].min() < smt_window['Close_NQ'].iloc[-1] * 0.999:
                results['bearish_success'] += 1
                success = True
        
        if divergence:
            results['details'].append({
                'date': date,
                'divergence': divergence,
                'success': success,
                'nq_low': nq_low,
                'es_low': es_low,
                'nq_high': nq_high,
                'es_high': es_high
            })
    
    # Calculate statistics
    bullish_rate = (results['bullish_success'] / results['bullish_smt'] * 100) if results['bullish_smt'] > 0 else 0
    bearish_rate = (results['bearish_success'] / results['bearish_smt'] * 100) if results['bearish_smt'] > 0 else 0
    
    print(f"\nTotal Trading Days Analyzed: {results['total_days']}")
    print(f"\nBullish SMT Divergences: {results['bullish_smt']}")
    print(f"Bullish Success: {results['bullish_success']} ({bullish_rate:.1f}%)")
    print(f"\nBearish SMT Divergences: {results['bearish_smt']}")
    print(f"Bearish Success: {results['bearish_success']} ({bearish_rate:.1f}%)")
    
    results['bullish_rate'] = bullish_rate
    results['bearish_rate'] = bearish_rate
    
    return results


# =====================================================================
# CORRELATION ANALYSES
# =====================================================================

def analyze_d1_london_correlation(df_1d, df_15m):
    """
    Analyze correlation between D1 close position and London session outcome.
    
    Question: If D1 closes in top 25% of its range, what's probability 
    London session (16:00+ JST) is bullish?
    """
    print("\n" + "="*70)
    print("D1/LONDON SESSION CORRELATION")
    print("="*70)
    
    results = {
        'total_d1_top_quarter': 0,
        'london_bullish_after_d1_top': 0,
        'total_days': 0
    }
    
    df_1d['Date_JST'] = pd.to_datetime(df_1d['Date_JST'])
    df_15m['Date_JST'] = pd.to_datetime(df_15m['Date_JST'])
    
    for i in range(len(df_1d) - 1):
        current_d1 = df_1d.iloc[i]
        d1_high = current_d1['High']
        d1_low = current_d1['Low']
        d1_close = current_d1['Close']
        d1_range = d1_high - d1_low
        
        if d1_range == 0:
            continue
        
        # Check if D1 closed in top 25%
        close_position = (d1_close - d1_low) / d1_range
        
        if close_position > 0.75:
            results['total_d1_top_quarter'] += 1
            
            # Check next day's London session
            next_date = df_1d.iloc[i + 1]['Date_JST']
            london_data = df_15m[
                (df_15m['Date_JST'] == next_date) &
                (df_15m['Hour_JST'] >= 16) &
                (df_15m['Hour_JST'] < 21)
            ]
            
            if len(london_data) > 0:
                results['total_days'] += 1
                london_open = london_data['Open'].iloc[0]
                london_close = london_data['Close'].iloc[-1]
                
                if london_close > london_open:
                    results['london_bullish_after_d1_top'] += 1
    
    probability = (results['london_bullish_after_d1_top'] / results['total_days'] * 100) if results['total_days'] > 0 else 0
    
    print(f"\nD1 candles closing in top 25%: {results['total_d1_top_quarter']}")
    print(f"Days with valid London data: {results['total_days']}")
    print(f"London sessions that were bullish: {results['london_bullish_after_d1_top']}")
    print(f"Probability: {probability:.1f}%")
    
    return results


def analyze_asian_range_sweep(df_15m):
    """
    Analyze Asian range sweep patterns.
    
    Asian Range: 08:00-15:00 JST
    Sweep Window: 15:00-17:00 JST
    """
    print("\n" + "="*70)
    print("ASIAN RANGE SWEEP ANALYSIS")
    print("="*70)
    
    results = {
        'total_days': 0,
        'high_sweep_attempts': 0,
        'high_true_breakouts': 0,
        'high_fakeouts': 0,
        'low_sweep_attempts': 0,
        'low_true_breakouts': 0,
        'low_fakeouts': 0
    }
    
    df_15m['Date_JST'] = pd.to_datetime(df_15m['Date_JST'])
    
    for date, day_data in df_15m.groupby('Date_JST'):
        # Skip weekends
        if day_data['DayOfWeek'].iloc[0] >= 5:
            continue
        
        # Asian session
        asian = day_data[(day_data['Hour_JST'] >= 8) & (day_data['Hour_JST'] < 15)]
        
        if len(asian) < 10:
            continue
        
        asian_high = asian['High'].max()
        asian_low = asian['Low'].min()
        
        # Sweep window
        sweep = day_data[
            ((day_data['Hour_JST'] == 15) | (day_data['Hour_JST'] == 16))
        ]
        
        if len(sweep) == 0:
            continue
        
        results['total_days'] += 1
        
        sweep_high = sweep['High'].max()
        sweep_low = sweep['Low'].min()
        
        # Rest of session for validation
        rest = day_data[day_data['Hour_JST'] >= 17]
        
        if len(rest) > 0:
            rest_high = rest['High'].max()
            rest_low = rest['Low'].min()
            
            # High sweep analysis
            if sweep_high > asian_high:
                results['high_sweep_attempts'] += 1
                if rest_high > sweep_high:
                    results['high_true_breakouts'] += 1
                else:
                    results['high_fakeouts'] += 1
            
            # Low sweep analysis
            if sweep_low < asian_low:
                results['low_sweep_attempts'] += 1
                if rest_low < sweep_low:
                    results['low_true_breakouts'] += 1
                else:
                    results['low_fakeouts'] += 1
    
    high_fakeout_rate = (results['high_fakeouts'] / results['high_sweep_attempts'] * 100) if results['high_sweep_attempts'] > 0 else 0
    low_fakeout_rate = (results['low_fakeouts'] / results['low_sweep_attempts'] * 100) if results['low_sweep_attempts'] > 0 else 0
    
    print(f"\nTotal Days Analyzed: {results['total_days']}")
    print(f"\nAsian High Sweep Attempts: {results['high_sweep_attempts']}")
    print(f"  - True Breakouts: {results['high_true_breakouts']}")
    print(f"  - Fakeouts: {results['high_fakeouts']} ({high_fakeout_rate:.1f}%)")
    print(f"\nAsian Low Sweep Attempts: {results['low_sweep_attempts']}")
    print(f"  - True Breakouts: {results['low_true_breakouts']}")
    print(f"  - Fakeouts: {results['low_fakeouts']} ({low_fakeout_rate:.1f}%)")
    
    return results


def analyze_volume_volatility(df_15m):
    """
    Identify the exact JST hour when volume significantly increases.
    """
    print("\n" + "="*70)
    print("VOLUME & VOLATILITY ANALYSIS")
    print("="*70)
    
    # Calculate average volume by hour (JST)
    hourly_volume = df_15m.groupby('Hour_JST')['Volume'].agg(['mean', 'median', 'std'])
    hourly_volume = hourly_volume.sort_values('mean', ascending=False)
    
    print("\nAverage Volume by Hour (JST) - Top 10:")
    print("-" * 50)
    for hour, row in hourly_volume.head(10).iterrows():
        print(f"Hour {hour:02d}:00 JST - Mean: {row['mean']:,.0f}, Median: {row['median']:,.0f}")
    
    # Calculate volatility (range) by hour
    df_15m['Range'] = df_15m['High'] - df_15m['Low']
    hourly_volatility = df_15m.groupby('Hour_JST')['Range'].agg(['mean', 'median'])
    hourly_volatility = hourly_volatility.sort_values('mean', ascending=False)
    
    print("\nAverage Volatility (Range) by Hour (JST) - Top 10:")
    print("-" * 50)
    for hour, row in hourly_volatility.head(10).iterrows():
        print(f"Hour {hour:02d}:00 JST - Mean: {row['mean']:.2f}, Median: {row['median']:.2f}")
    
    # Identify Tokyo afternoon calm (typically 13:00-15:00 JST)
    tokyo_afternoon = df_15m[(df_15m['Hour_JST'] >= 13) & (df_15m['Hour_JST'] < 15)]
    avg_tokyo_afternoon_vol = tokyo_afternoon['Volume'].mean()
    
    print(f"\nTokyo Afternoon (13:00-15:00 JST) Average Volume: {avg_tokyo_afternoon_vol:,.0f}")
    
    # Find when volume increases significantly
    print("\nHours with >50% higher volume than Tokyo afternoon:")
    print("-" * 50)
    for hour, row in hourly_volume.iterrows():
        if row['mean'] > avg_tokyo_afternoon_vol * 1.5:
            increase = (row['mean'] / avg_tokyo_afternoon_vol - 1) * 100
            print(f"Hour {hour:02d}:00 JST - {increase:.0f}% higher volume")
    
    return {
        'hourly_volume': hourly_volume,
        'hourly_volatility': hourly_volatility,
        'tokyo_afternoon_volume': avg_tokyo_afternoon_vol
    }


def analyze_h4_continuation(df_4h, df_15m):
    """
    Analyze H4 continuation strategy.
    
    Question: If H4 trend is bullish, does price tend to test 
    14:00/15:00 JST level before moving up?
    """
    print("\n" + "="*70)
    print("H4 CONTINUATION STRATEGY")
    print("="*70)
    
    results = {
        'bullish_h4_periods': 0,
        'tested_1400_1500': 0,
        'moved_up_after_test': 0,
        'moved_up_without_test': 0
    }
    
    df_4h['Date_JST'] = pd.to_datetime(df_4h['Date_JST'])
    df_15m['Date_JST'] = pd.to_datetime(df_15m['Date_JST'])
    
    # Identify bullish H4 periods
    df_4h['Higher_High'] = (df_4h['High'] > df_4h['High'].shift(1))
    df_4h['Higher_Low'] = (df_4h['Low'] > df_4h['Low'].shift(1))
    
    for i in range(10, len(df_4h) - 5):
        window = df_4h.iloc[i-3:i]
        
        # Check for bullish structure
        if window['Higher_High'].sum() >= 2 and window['Higher_Low'].sum() >= 2:
            results['bullish_h4_periods'] += 1
            
            current_date = df_4h.iloc[i]['Date_JST']
            current_low = df_4h.iloc[i]['Low']
            
            # Check 15m data for that day
            day_15m = df_15m[df_15m['Date_JST'] == current_date]
            
            if len(day_15m) > 0:
                # Check 14:00-15:00 JST window
                test_window = day_15m[
                    ((day_15m['Hour_JST'] == 14) | (day_15m['Hour_JST'] == 15))
                ]
                
                if len(test_window) > 0:
                    test_low = test_window['Low'].min()
                    
                    # Did price test near current support (within 0.3%)?
                    tested = abs(test_low - current_low) / current_low < 0.003
                    
                    if tested:
                        results['tested_1400_1500'] += 1
                    
                    # Check if price moved up in London session
                    london = day_15m[(day_15m['Hour_JST'] >= 16) & (day_15m['Hour_JST'] < 21)]
                    
                    if len(london) > 0:
                        london_high = london['High'].max()
                        entry_price = test_window['Close'].iloc[-1] if len(test_window) > 0 else day_15m[day_15m['Hour_JST'] == 16]['Open'].iloc[0] if len(day_15m[day_15m['Hour_JST'] == 16]) > 0 else 0
                        
                        if entry_price > 0 and london_high > entry_price * 1.002:
                            if tested:
                                results['moved_up_after_test'] += 1
                            else:
                                results['moved_up_without_test'] += 1
    
    test_rate = (results['tested_1400_1500'] / results['bullish_h4_periods'] * 100) if results['bullish_h4_periods'] > 0 else 0
    success_after_test = (results['moved_up_after_test'] / results['tested_1400_1500'] * 100) if results['tested_1400_1500'] > 0 else 0
    
    print(f"\nBullish H4 Periods: {results['bullish_h4_periods']}")
    print(f"Times price tested 14:00-15:00 JST level: {results['tested_1400_1500']} ({test_rate:.1f}%)")
    print(f"Successful moves up after test: {results['moved_up_after_test']} ({success_after_test:.1f}%)")
    print(f"Successful moves up without test: {results['moved_up_without_test']}")
    
    return results


# =====================================================================
# MAIN EXECUTION
# =====================================================================

def main():
    """Main execution function."""
    
    print("="*70)
    print("NQ FUTURES LONDON SESSION BACKTESTING SYSTEM")
    print("All times displayed in Japan Standard Time (JST)")
    print("="*70)
    print()
    
    base_path = "/home/runner/work/Backtest-Trading/Backtest-Trading"
    
    # Load data
    print("Loading NQ data...")
    nq_15m = load_nq_data(base_path, "15m")
    nq_1h = load_nq_data(base_path, "1H")
    nq_4h = load_nq_data(base_path, "4H")
    nq_1d = load_nq_data(base_path, "1D")
    
    print("\nLoading ES data for SMT analysis...")
    es_15m = load_es_data(base_path, "15m")
    
    if nq_15m.empty:
        print("Error: Could not load NQ 15m data")
        return
    
    # Run all analyses
    results = {}
    
    # Method 1: Judas Swing
    results['judas_swing'] = analyze_judas_swing(nq_15m)
    
    # Method 2: NY Midnight
    results['ny_midnight'] = analyze_ny_midnight(nq_15m)
    
    # Method 3: H4 Structure
    results['h4_structure'] = analyze_h4_structure(nq_4h, nq_1d)
    
    # Method 4: SMT Divergence
    results['smt_divergence'] = analyze_smt_divergence(nq_15m, es_15m)
    
    # Correlation analyses
    results['d1_london_corr'] = analyze_d1_london_correlation(nq_1d, nq_15m)
    results['asian_range_sweep'] = analyze_asian_range_sweep(nq_15m)
    results['volume_volatility'] = analyze_volume_volatility(nq_15m)
    results['h4_continuation'] = analyze_h4_continuation(nq_4h, nq_15m)
    
    # Generate summary report
    generate_summary_report(results)
    
    print("\n" + "="*70)
    print("ANALYSIS COMPLETE")
    print("="*70)
    print("\nResults saved to: nq_analysis_results.txt")


def generate_summary_report(results):
    """Generate comprehensive summary report."""
    
    report = []
    report.append("="*70)
    report.append("NQ FUTURES LONDON SESSION BACKTEST SUMMARY")
    report.append("All times in Japan Standard Time (JST)")
    report.append("="*70)
    report.append("")
    
    # Method comparison
    report.append("TRADING METHODS PERFORMANCE SUMMARY")
    report.append("-"*70)
    report.append("")
    
    methods = [
        ("Method 1: Judas Swing", results['judas_swing']),
        ("Method 2: NY Midnight Rule", results['ny_midnight']),
        ("Method 3: H4 Market Structure", results['h4_structure']),
        ("Method 4: SMT Divergence", results['smt_divergence'])
    ]
    
    best_method = None
    best_rate = 0
    
    for method_name, method_results in methods:
        report.append(f"{method_name}:")
        
        if 'bullish_rate' in method_results and 'bearish_rate' in method_results:
            avg_rate = (method_results['bullish_rate'] + method_results['bearish_rate']) / 2
            report.append(f"  Bullish Success Rate: {method_results['bullish_rate']:.1f}%")
            report.append(f"  Bearish Success Rate: {method_results['bearish_rate']:.1f}%")
            report.append(f"  Overall Average: {avg_rate:.1f}%")
            
            if avg_rate > best_rate:
                best_rate = avg_rate
                best_method = method_name
        
        report.append("")
    
    if best_method:
        report.append(f"BEST PERFORMING METHOD: {best_method}")
        report.append(f"Success Rate: {best_rate:.1f}%")
        report.append("")
    
    # Key correlations
    report.append("="*70)
    report.append("KEY CORRELATIONS & INSIGHTS")
    report.append("-"*70)
    report.append("")
    
    if 'd1_london_corr' in results:
        d1_corr = results['d1_london_corr']
        if d1_corr['total_days'] > 0:
            prob = (d1_corr['london_bullish_after_d1_top'] / d1_corr['total_days'] * 100)
            report.append(f"D1/London Correlation:")
            report.append(f"  When D1 closes in top 25% of range:")
            report.append(f"  Probability of bullish London session: {prob:.1f}%")
            report.append("")
    
    if 'asian_range_sweep' in results:
        sweep = results['asian_range_sweep']
        if sweep['high_sweep_attempts'] > 0:
            high_fake = (sweep['high_fakeouts'] / sweep['high_sweep_attempts'] * 100)
            report.append(f"Asian Range High Sweep:")
            report.append(f"  Fakeout Rate: {high_fake:.1f}%")
        if sweep['low_sweep_attempts'] > 0:
            low_fake = (sweep['low_fakeouts'] / sweep['low_sweep_attempts'] * 100)
            report.append(f"Asian Range Low Sweep:")
            report.append(f"  Fakeout Rate: {low_fake:.1f}%")
        report.append("")
    
    # Daily action plan
    report.append("="*70)
    report.append("DAILY ACTION PLAN TEMPLATE (JST)")
    report.append("-"*70)
    report.append("")
    report.append("08:00-15:00 JST - ASIAN SESSION")
    report.append("  • Mark Asian Range High and Low")
    report.append("  • Observe key levels and liquidity zones")
    report.append("")
    report.append("13:00-14:00 JST - NY MIDNIGHT OPEN")
    report.append("  • Mark the opening price level")
    report.append("  • Note: 13:00 JST (winter) or 14:00 JST (summer)")
    report.append("")
    report.append("14:00-16:00 JST - PRE-LONDON / SMT WINDOW")
    report.append("  • Check for SMT divergence between NQ and ES")
    report.append("  • Monitor for Asian range sweeps")
    report.append("")
    report.append("15:30-17:00 JST - JUDAS SWING WINDOW")
    report.append("  • Watch for false breakouts of Asian range")
    report.append("  • Rejection wicks signal potential reversals")
    report.append("")
    report.append("16:00 JST - LONDON SESSION OPEN")
    report.append("  • Apply NY Midnight Rule bias")
    report.append("  • Check price vs midnight level for directional bias")
    report.append("")
    report.append("16:00-21:00 JST - LONDON SESSION TRADING")
    report.append("  • Trade in direction of confirmed bias")
    report.append("  • Look for H4 structure confirmation")
    report.append("  • Use discount zones for entries")
    report.append("")
    
    report.append("="*70)
    report.append("RISK DISCLAIMER")
    report.append("-"*70)
    report.append("Past performance does not guarantee future results.")
    report.append("This analysis is for educational purposes only.")
    report.append("Always use proper risk management and position sizing.")
    report.append("="*70)
    
    # Write to file
    report_text = "\n".join(report)
    
    with open("/home/runner/work/Backtest-Trading/Backtest-Trading/nq_analysis_results.txt", "w") as f:
        f.write(report_text)
    
    # Also print to console
    print("\n" + report_text)


if __name__ == "__main__":
    main()

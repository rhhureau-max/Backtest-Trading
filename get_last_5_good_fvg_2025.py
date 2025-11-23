#!/usr/bin/env python3
"""
Extract the last 5 good FVG from 2025 for all three timeframes
"""

import pandas as pd
import os
from datetime import datetime, time

def read_data_file(filepath):
    """Read data file (XLSX or CSV)"""
    if filepath.endswith('.csv'):
        df = pd.read_csv(filepath, sep=';')
        # Remove header row if it exists
        if df.columns[0] == 'Column1':
            df = df.iloc[:]  # Keep data as is
        # Set proper column names
        if len(df.columns) == 7:
            df.columns = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
            df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], dayfirst=True, format='mixed')
            df = df.drop(['Date', 'Time'], axis=1)
        else:
            df.columns = ['DateTime', 'Open', 'High', 'Low', 'Close', 'Volume']
            df['DateTime'] = pd.to_datetime(df['DateTime'], dayfirst=True, format='mixed')
    else:
        df = pd.read_excel(filepath, header=None)
        df.columns = ['DateTime', 'Open', 'High', 'Low', 'Close', 'Volume']
        df['DateTime'] = pd.to_datetime(df['DateTime'], dayfirst=True, format='mixed')
    
    # Convert numeric columns
    for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    return df

def detect_good_fvg(df, target_time):
    """Detect good FVG at target time"""
    results = []
    
    for date in df['DateTime'].dt.date.unique():
        day_data = df[df['DateTime'].dt.date == date].copy()
        day_data = day_data.sort_values('DateTime').reset_index(drop=True)
        
        # Find target time candle
        target_candles = day_data[day_data['DateTime'].dt.time == target_time]
        if len(target_candles) == 0:
            continue
            
        target_idx = target_candles.index[0]
        
        if target_idx < 1 or target_idx >= len(day_data) - 1:
            continue
            
        prev_candle = day_data.iloc[target_idx - 1]
        curr_candle = day_data.iloc[target_idx]
        next_candle = day_data.iloc[target_idx + 1]
        
        # Check for bullish FVG
        if next_candle['Low'] > prev_candle['High']:
            fvg_size = next_candle['Low'] - prev_candle['High']
            
            # Check if good FVG (price doesn't return in next 5 candles)
            is_good = True
            for i in range(1, 6):
                if target_idx + 1 + i >= len(day_data):
                    break
                check_candle = day_data.iloc[target_idx + 1 + i]
                if check_candle['Low'] <= prev_candle['High']:
                    is_good = False
                    break
            
            if is_good:
                results.append({
                    'Date': date,
                    'DateTime': curr_candle['DateTime'],
                    'Type': 'Bullish',
                    'Size_Ticks': round(fvg_size * 4, 2),
                    'Size_Points': round(fvg_size, 2),
                    'Prev_High': prev_candle['High'],
                    'Next_Low': next_candle['Low'],
                    'Target_Close': curr_candle['Close']
                })
        
        # Check for bearish FVG
        elif next_candle['High'] < prev_candle['Low']:
            fvg_size = prev_candle['Low'] - next_candle['High']
            
            # Check if good FVG
            is_good = True
            for i in range(1, 6):
                if target_idx + 1 + i >= len(day_data):
                    break
                check_candle = day_data.iloc[target_idx + 1 + i]
                if check_candle['High'] >= prev_candle['Low']:
                    is_good = False
                    break
            
            if is_good:
                results.append({
                    'Date': date,
                    'DateTime': curr_candle['DateTime'],
                    'Type': 'Bearish',
                    'Size_Ticks': round(fvg_size * 4, 2),
                    'Size_Points': round(fvg_size, 2),
                    'Prev_Low': prev_candle['Low'],
                    'Next_High': next_candle['High'],
                    'Target_Close': curr_candle['Close']
                })
    
    return results

def main():
    # Define timeframes
    timeframes = {
        '1-Minute': {
            'file': '2025 1m.csv',
            'time': time(8, 30, 0)
        },
        '5-Minute': {
            'file': '2025 5m.csv',
            'time': time(8, 30, 0)
        },
        '15-Minute': {
            'file': '2025 15m.csv',
            'time': time(8, 30, 0)
        }
    }
    
    print('=' * 90)
    print('LAST 5 GOOD FVG IDENTIFIED IN 2025 (BY TIMEFRAME)')
    print('=' * 90)
    
    for tf_name, config in timeframes.items():
        print(f'\n\n{"=" * 90}')
        print(f'{tf_name.upper()} TIMEFRAME')
        print('=' * 90)
        
        filepath = config['file']
        target_time = config['time']
        
        if not os.path.exists(filepath):
            print(f'\nFile not found: {filepath}')
            continue
        
        try:
            df = read_data_file(filepath)
            good_fvgs = detect_good_fvg(df, target_time)
            
            if len(good_fvgs) == 0:
                print('\nNo good FVG found in 2025')
                continue
            
            # Get last 5
            last_5 = good_fvgs[-5:] if len(good_fvgs) >= 5 else good_fvgs
            
            print(f'\nTotal Good FVG in 2025: {len(good_fvgs)}')
            print(f'Showing last {len(last_5)} Good FVG:\n')
            
            for i, fvg in enumerate(last_5, 1):
                print(f'{"-" * 90}')
                print(f'#{i} - {fvg["Date"]} at {fvg["DateTime"].strftime("%H:%M:%S")}')
                print(f'{"-" * 90}')
                print(f'  Type:          {fvg["Type"]}')
                print(f'  Size:          {fvg["Size_Ticks"]:.2f} ticks ({fvg["Size_Points"]:.2f} points)')
                print(f'  Target Close:  {fvg["Target_Close"]:.2f}')
                
                if fvg['Type'] == 'Bullish':
                    print(f'  FVG Zone:      {fvg["Prev_High"]:.2f} (prev high) to {fvg["Next_Low"]:.2f} (next low)')
                else:
                    print(f'  FVG Zone:      {fvg["Next_High"]:.2f} (next high) to {fvg["Prev_Low"]:.2f} (prev low)')
                print()
        
        except Exception as e:
            print(f'\nError processing {tf_name}: {str(e)}')
            continue
    
    print('=' * 90)
    print('END OF REPORT')
    print('=' * 90)

if __name__ == '__main__':
    main()

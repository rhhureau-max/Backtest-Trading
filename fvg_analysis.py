#!/usr/bin/env python3
"""
FVG (Fair Value Gap) Analysis Script
Analyzes trading candle data to detect FVGs, their fills with breaks, 
and calculates the probability of continuation.
"""

import os
import numpy as np
import pandas as pd


def load_data(base_path: str, timeframe: str, years: list) -> pd.DataFrame:
    """Load and concatenate CSV data for specified years and timeframe."""
    all_data = []
    
    for year in years:
        filename = f"{year} {timeframe}.csv"
        filepath = os.path.join(base_path, filename)
        
        if os.path.exists(filepath):
            df = pd.read_csv(filepath, sep=';')
            df.columns = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
            df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%d/%m/%Y %H:%M:%S')
            all_data.append(df)
        else:
            print(f"Warning: File not found - {filepath}")
    
    if not all_data:
        return pd.DataFrame()
    
    combined = pd.concat(all_data, ignore_index=True)
    combined = combined.sort_values('DateTime').reset_index(drop=True)
    return combined


def detect_fvgs(df: pd.DataFrame) -> list:
    """
    Detect Fair Value Gaps in the data.
    
    FVG baissier (Bearish FVG): Low of candle 1 > High of candle 3 (gap between candles 1 and 3)
    FVG haussier (Bullish FVG): High of candle 1 < Low of candle 3 (gap between candles 1 and 3)
    
    Returns a list of FVG dictionaries with their properties.
    """
    fvgs = []
    
    for i in range(len(df) - 2):
        candle1 = df.iloc[i]
        candle2 = df.iloc[i + 1]
        candle3 = df.iloc[i + 2]
        
        # Bearish FVG: Low of candle 1 > High of candle 3
        if candle1['Low'] > candle3['High']:
            fvgs.append({
                'type': 'bearish',
                'candle1_idx': i,
                'candle2_idx': i + 1,
                'candle3_idx': i + 2,
                'fvg_top': candle1['Low'],      # Top of the gap
                'fvg_bottom': candle3['High'],  # Bottom of the gap
                'datetime': candle2['DateTime']
            })
        
        # Bullish FVG: High of candle 1 < Low of candle 3
        elif candle1['High'] < candle3['Low']:
            fvgs.append({
                'type': 'bullish',
                'candle1_idx': i,
                'candle2_idx': i + 1,
                'candle3_idx': i + 2,
                'fvg_top': candle3['Low'],      # Top of the gap
                'fvg_bottom': candle1['High'],  # Bottom of the gap
                'datetime': candle2['DateTime']
            })
    
    return fvgs


def check_fvg_fill_and_break_vectorized(df: pd.DataFrame, fvgs: list) -> list:
    """
    Vectorized check for FVG fills and breaks using numpy arrays.
    Much faster than checking each FVG individually.
    
    Returns list of fill info for each FVG.
    """
    # Pre-compute arrays for faster access
    opens = df['Open'].values
    closes = df['Close'].values
    body_highs = np.maximum(opens, closes)
    body_lows = np.minimum(opens, closes)
    n = len(df)
    
    results = []
    
    for fvg in fvgs:
        start_idx = fvg['candle3_idx'] + 1
        fvg_type = fvg['type']
        fvg_top = fvg['fvg_top']
        fvg_bottom = fvg['fvg_bottom']
        
        found = False
        
        if fvg_type == 'bearish':
            # For bearish FVG: body must enter the gap AND close above the FVG top
            for i in range(start_idx, n):
                if body_highs[i] >= fvg_bottom and closes[i] > fvg_top:
                    results.append({
                        'filled': True,
                        'fill_idx': i,
                        'fill_datetime': df.iloc[i]['DateTime'],
                        'fill_candle_direction': 'bullish' if closes[i] > opens[i] else 'bearish'
                    })
                    found = True
                    break
        else:  # bullish FVG
            # For bullish FVG: body must enter the gap AND close below the FVG bottom
            for i in range(start_idx, n):
                if body_lows[i] <= fvg_top and closes[i] < fvg_bottom:
                    results.append({
                        'filled': True,
                        'fill_idx': i,
                        'fill_datetime': df.iloc[i]['DateTime'],
                        'fill_candle_direction': 'bullish' if closes[i] > opens[i] else 'bearish'
                    })
                    found = True
                    break
        
        if not found:
            results.append({'filled': False})
    
    return results


def check_next_candle_direction(df: pd.DataFrame, fill_idx: int) -> str:
    """
    Check the direction of the candle following the fill candle.
    Returns 'bullish', 'bearish', or 'neutral'.
    """
    next_idx = fill_idx + 1
    
    if next_idx >= len(df):
        return 'no_next_candle'
    
    next_candle = df.iloc[next_idx]
    
    if next_candle['Close'] > next_candle['Open']:
        return 'bullish'
    elif next_candle['Close'] < next_candle['Open']:
        return 'bearish'
    else:
        return 'neutral'


def analyze_timeframe(base_path: str, timeframe: str, years: list) -> dict:
    """Analyze FVGs for a specific timeframe."""
    print(f"\n{'='*60}")
    print(f"Analyzing {timeframe} timeframe...")
    print(f"{'='*60}")
    
    df = load_data(base_path, timeframe, years)
    
    if df.empty:
        print(f"No data found for {timeframe}")
        return None
    
    print(f"Loaded {len(df)} candles for {timeframe}")
    
    # Detect all FVGs
    fvgs = detect_fvgs(df)
    print(f"Found {len(fvgs)} FVGs total")
    
    bearish_fvg_count = sum(1 for fvg in fvgs if fvg['type'] == 'bearish')
    bullish_fvg_count = sum(1 for fvg in fvgs if fvg['type'] == 'bullish')
    print(f"  - Bearish FVGs: {bearish_fvg_count}")
    print(f"  - Bullish FVGs: {bullish_fvg_count}")
    
    # Analyze FVG fills and continuation using vectorized function
    results = {
        'bearish': {
            'total_fvgs': 0,
            'filled_and_broken': 0,
            'next_candle_same_direction': 0  # Same direction as fill candle (bullish)
        },
        'bullish': {
            'total_fvgs': 0,
            'filled_and_broken': 0,
            'next_candle_same_direction': 0  # Same direction as fill candle (bearish)
        }
    }
    
    # Get fill info for all FVGs at once
    print(f"  Analyzing FVG fills... (this may take a moment)")
    fill_infos = check_fvg_fill_and_break_vectorized(df, fvgs)
    
    for i, fvg in enumerate(fvgs):
        fvg_type = fvg['type']
        results[fvg_type]['total_fvgs'] += 1
        
        fill_info = fill_infos[i]
        
        if fill_info['filled']:
            results[fvg_type]['filled_and_broken'] += 1
            
            next_direction = check_next_candle_direction(df, fill_info['fill_idx'])
            
            # For bearish FVG broken, fill candle is bullish, check if next is also bullish
            # For bullish FVG broken, fill candle is bearish, check if next is also bearish
            if fvg_type == 'bearish' and next_direction == 'bullish':
                results[fvg_type]['next_candle_same_direction'] += 1
            elif fvg_type == 'bullish' and next_direction == 'bearish':
                results[fvg_type]['next_candle_same_direction'] += 1
    
    return results


def print_results(results: dict, timeframe: str):
    """Print analysis results for a timeframe."""
    print(f"\n{'='*60}")
    print(f"RESULTS FOR {timeframe}")
    print(f"{'='*60}")
    
    # Bearish FVG results
    bearish = results['bearish']
    print(f"\n📉 BEARISH FVGs (comblés par une bougie haussière qui casse au-dessus):")
    print(f"   Total FVGs baissiers: {bearish['total_fvgs']}")
    print(f"   FVGs comblés et cassés: {bearish['filled_and_broken']}")
    print(f"   Bougie suivante haussière (même direction): {bearish['next_candle_same_direction']}")
    
    if bearish['filled_and_broken'] > 0:
        prob = (bearish['next_candle_same_direction'] / bearish['filled_and_broken']) * 100
        print(f"   📊 PROBABILITÉ de continuation haussière: {prob:.2f}%")
    else:
        print(f"   📊 PROBABILITÉ: N/A (aucun FVG comblé)")
    
    # Bullish FVG results
    bullish = results['bullish']
    print(f"\n📈 BULLISH FVGs (comblés par une bougie baissière qui casse en-dessous):")
    print(f"   Total FVGs haussiers: {bullish['total_fvgs']}")
    print(f"   FVGs comblés et cassés: {bullish['filled_and_broken']}")
    print(f"   Bougie suivante baissière (même direction): {bullish['next_candle_same_direction']}")
    
    if bullish['filled_and_broken'] > 0:
        prob = (bullish['next_candle_same_direction'] / bullish['filled_and_broken']) * 100
        print(f"   📊 PROBABILITÉ de continuation baissière: {prob:.2f}%")
    else:
        print(f"   📊 PROBABILITÉ: N/A (aucun FVG comblé)")


def main():
    """Main function to run the FVG analysis."""
    # Use current directory as default, or specify custom path
    base_path = os.path.dirname(os.path.abspath(__file__))
    years = list(range(2018, 2026))  # 2018 to 2025
    timeframes = ['4H', '1H', '15m']
    
    print("╔" + "═"*58 + "╗")
    print("║" + " FVG (Fair Value Gap) Analysis ".center(58) + "║")
    print("║" + f" Période: 2018-2025 ".center(58) + "║")
    print("╚" + "═"*58 + "╝")
    
    all_results = {}
    
    for tf in timeframes:
        results = analyze_timeframe(base_path, tf, years)
        if results:
            all_results[tf] = results
            print_results(results, tf)
    
    # Summary table
    print("\n" + "="*80)
    print(" SUMMARY TABLE ".center(80))
    print("="*80)
    print(f"\n{'Timeframe':<12} | {'Type':<10} | {'Total FVGs':<12} | {'Filled/Broken':<14} | {'Same Dir':<10} | {'Probability':<12}")
    print("-"*80)
    
    for tf, results in all_results.items():
        for fvg_type in ['bearish', 'bullish']:
            data = results[fvg_type]
            prob = (data['next_candle_same_direction'] / data['filled_and_broken'] * 100) if data['filled_and_broken'] > 0 else 0
            print(f"{tf:<12} | {fvg_type.upper():<10} | {data['total_fvgs']:<12} | {data['filled_and_broken']:<14} | {data['next_candle_same_direction']:<10} | {prob:.2f}%")
    
    print("="*80)
    print("\nLégende:")
    print("  - 'Total FVGs': Nombre total de FVGs détectés")
    print("  - 'Filled/Broken': FVGs comblés ET cassés (close au-delà du FVG)")
    print("  - 'Same Dir': Bougie suivante de même direction que la bougie de cassure")
    print("  - 'Probability': Probabilité que la bougie suivante continue dans la même direction")


if __name__ == "__main__":
    main()

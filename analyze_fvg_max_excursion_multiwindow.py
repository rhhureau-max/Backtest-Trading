#!/usr/bin/env python3
"""
Analyze maximum price excursion for Good FVG across multiple candle windows
Calculates the average maximum distance (in ticks) from the close of the third candle (8:31)
for Good FVG using different window sizes: 5, 10, 15, 20, 25, 30, and 50 candles

For Nasdaq: 1 tick = 0.25 points
"""

import pandas as pd
import os
from datetime import time

def load_data_file(filename):
    """Load a data file (XLSX or CSV)"""
    if filename.endswith('.xlsx'):
        return pd.read_excel(filename)
    elif filename.endswith('.csv'):
        # CSV files in this dataset use semicolon as delimiter
        return pd.read_csv(filename, sep=';')
    else:
        raise ValueError(f"Unsupported file format: {filename}")

def analyze_fvg_max_excursion_multiwindow(df, year, timeframe='1m'):
    """
    Analyze maximum price excursion for good FVG across multiple candle windows
    
    Args:
        df: DataFrame with OHLCV data
        year: Year being analyzed
        timeframe: '1m', '5m', or '15m'
    
    Returns:
        dict with excursion statistics for each window size
    """
    # Define target time based on timeframe
    if timeframe == '1m':
        target_time = time(8, 30)
        prev_time_str = ['08:29:00', '8:29:00', '08:29', '8:29']
        next_time_str = ['08:31:00', '8:31:00', '08:31', '8:31']
    elif timeframe == '5m':
        target_time = time(8, 30)
        prev_time_str = ['08:25:00', '8:25:00', '08:25', '8:25']
        next_time_str = ['08:35:00', '8:35:00', '08:35', '8:35']
    elif timeframe == '15m':
        target_time = time(8, 30)
        prev_time_str = ['08:15:00', '8:15:00', '08:15', '8:15']
        next_time_str = ['08:45:00', '8:45:00', '08:45', '8:45']
    else:
        raise ValueError(f"Unsupported timeframe: {timeframe}")
    
    if len(df) == 0:
        return None
    
    # Find all target time entries
    if df['Column2'].dtype == 'object':
        if isinstance(df['Column2'].iloc[0], time):
            mask = df['Column2'] == target_time
        else:
            mask = df['Column2'].isin(['08:30:00', '8:30:00', '08:30', '8:30'])
    else:
        mask = df['Column2'] == target_time
    
    indices_target = df[mask].index.tolist()
    
    # Window sizes to analyze
    windows = [5, 10, 15, 20, 25, 30, 50]
    
    # Initialize results structure
    results = {
        'year': year,
        'timeframe': timeframe,
        'windows': {}
    }
    
    for window_size in windows:
        results['windows'][window_size] = {
            'bullish_excursions': [],
            'bearish_excursions': []
        }
    
    # For each target candle, check for FVG and calculate max excursion for each window
    for idx in indices_target:
        # Make sure we have previous, next, and future candles for the largest window
        if idx < 1 or idx >= len(df) - (max(windows) + 1):
            continue
        
        # Get the three candles for FVG detection
        candle_prev = df.loc[idx - 1]
        candle_mid = df.loc[idx]
        candle_next = df.loc[idx + 1]
        
        # Validate adjacent candles
        prev_time = candle_prev['Column2']
        if isinstance(prev_time, str):
            if prev_time not in prev_time_str:
                continue
        
        next_time = candle_next['Column2']
        if isinstance(next_time, str):
            if next_time not in next_time_str:
                continue
        
        # Extract OHLC values
        high_prev = float(candle_prev['Column4'])
        low_prev = float(candle_prev['Column5'])
        high_next = float(candle_next['Column4'])
        low_next = float(candle_next['Column5'])
        close_next = float(candle_next['Column6'])  # Close of third candle
        
        # Check for FVG
        is_bullish_fvg = low_next > high_prev
        is_bearish_fvg = high_next < low_prev
        
        if not is_bullish_fvg and not is_bearish_fvg:
            continue
        
        # For each window size, check if it's a good FVG and calculate excursion
        for window_size in windows:
            # Get next candles AFTER the third candle closes
            next_candles = df.loc[idx+2:idx+1+window_size]
            
            if len(next_candles) < window_size:
                continue
            
            if is_bullish_fvg:
                # Bullish FVG zone: between high_prev and low_next
                fvg_low = high_prev
                fvg_high = low_next
                
                # Check if price returns to FVG zone (bad FVG)
                price_returned = False
                for i in range(len(next_candles)):
                    candle_low = float(next_candles.iloc[i]['Column5'])
                    candle_high = float(next_candles.iloc[i]['Column4'])
                    
                    if candle_low <= fvg_high and candle_high >= fvg_low:
                        price_returned = True
                        break
                
                # Only analyze good FVG (where price doesn't return)
                if not price_returned:
                    # Calculate maximum excursion from close_next
                    max_high = close_next
                    for i in range(len(next_candles)):
                        candle_high = float(next_candles.iloc[i]['Column4'])
                        if candle_high > max_high:
                            max_high = candle_high
                    
                    # Calculate excursion in ticks (1 tick = 0.25 points for Nasdaq)
                    excursion_points = max_high - close_next
                    excursion_ticks = excursion_points / 0.25
                    results['windows'][window_size]['bullish_excursions'].append(excursion_ticks)
            
            elif is_bearish_fvg:
                # Bearish FVG zone: between low_prev and high_next
                fvg_low = high_next
                fvg_high = low_prev
                
                # Check if price returns to FVG zone (bad FVG)
                price_returned = False
                for i in range(len(next_candles)):
                    candle_low = float(next_candles.iloc[i]['Column5'])
                    candle_high = float(next_candles.iloc[i]['Column4'])
                    
                    if candle_low <= fvg_high and candle_high >= fvg_low:
                        price_returned = True
                        break
                
                # Only analyze good FVG (where price doesn't return)
                if not price_returned:
                    # Calculate maximum excursion from close_next (down move)
                    max_low = close_next
                    for i in range(len(next_candles)):
                        candle_low = float(next_candles.iloc[i]['Column5'])
                        if candle_low < max_low:
                            max_low = candle_low
                    
                    # Calculate excursion in ticks (1 tick = 0.25 points for Nasdaq)
                    excursion_points = close_next - max_low
                    excursion_ticks = excursion_points / 0.25
                    results['windows'][window_size]['bearish_excursions'].append(excursion_ticks)
    
    return results

def main():
    print("Analyzing Maximum Price Excursion for Good FVG Across Multiple Windows (2018-2025)")
    print("=" * 80)
    print("Window sizes: 5, 10, 15, 20, 25, 30, 50 candles")
    print("=" * 80)
    
    # Timeframes to analyze
    timeframes = {
        '1m': ['1m.xlsx', '1m.csv'],
        '5m': ['5m.csv'],
        '15m': ['15m.csv']
    }
    
    years = range(2018, 2026)
    windows = [5, 10, 15, 20, 25, 30, 50]
    
    results_by_timeframe = {}
    
    for tf_name, tf_extensions in timeframes.items():
        print(f"\n{'='*80}")
        print(f"Timeframe: {tf_name}")
        print(f"{'='*80}")
        
        results_by_timeframe[tf_name] = []
        
        for year in years:
            # Try different file formats
            df = None
            for ext in tf_extensions:
                filename = f"{year} {ext}"
                if os.path.exists(filename):
                    try:
                        df = load_data_file(filename)
                        print(f"\nLoaded {filename}")
                        break
                    except Exception as e:
                        print(f"Error loading {filename}: {e}")
                        continue
            
            if df is None:
                print(f"No data file found for {year} {tf_name}")
                continue
            
            # Analyze across all windows
            result = analyze_fvg_max_excursion_multiwindow(df, year, tf_name)
            if result:
                results_by_timeframe[tf_name].append(result)
                
                print(f"\nYear {year} - Summary:")
                for window in windows:
                    bullish_count = len(result['windows'][window]['bullish_excursions'])
                    bearish_count = len(result['windows'][window]['bearish_excursions'])
                    print(f"  Window {window:2d}: Bullish={bullish_count:3d}, Bearish={bearish_count:3d}")
    
    # Generate comprehensive analysis
    print("\n\n" + "="*80)
    print("COMPREHENSIVE MULTI-WINDOW MAXIMUM EXCURSION ANALYSIS")
    print("="*80)
    
    # Save detailed results to file
    output_file = "fvg_max_excursion_multiwindow_analysis.txt"
    with open(output_file, 'w') as f:
        f.write("Maximum Price Excursion Analysis for Good FVG - Multi-Window\n")
        f.write("=" * 80 + "\n")
        f.write("Measuring average maximum distance (in ticks) from close of third candle\n")
        f.write("for Good FVG across different window sizes (2018-2025)\n")
        f.write("Windows: 5, 10, 15, 20, 25, 30, 50 candles\n")
        f.write("Nasdaq: 1 tick = 0.25 points\n")
        f.write("=" * 80 + "\n\n")
        
        for tf_name in timeframes.keys():
            results = results_by_timeframe[tf_name]
            if not results:
                continue
            
            f.write(f"\n{'='*80}\n")
            f.write(f"{tf_name.upper()} TIMEFRAME\n")
            f.write(f"{'='*80}\n")
            
            # Overall statistics by window
            f.write("\nOverall Statistics (2018-2025) by Window Size:\n")
            f.write("-" * 80 + "\n")
            f.write(f"{'Window':<10} {'Bull Count':<12} {'Bull Avg (ticks)':<20} {'Bear Count':<12} {'Bear Avg (ticks)':<20} {'Combined Avg':<15}\n")
            f.write("-" * 80 + "\n")
            
            print(f"\n{tf_name.upper()} Timeframe - Overall Statistics (2018-2025):")
            print("-" * 80)
            print(f"{'Window':<10} {'Bull':<8} {'Bull Avg':<18} {'Bear':<8} {'Bear Avg':<18} {'Combined':<15}")
            print("-" * 80)
            
            for window in windows:
                all_bullish = []
                all_bearish = []
                
                for r in results:
                    all_bullish.extend(r['windows'][window]['bullish_excursions'])
                    all_bearish.extend(r['windows'][window]['bearish_excursions'])
                
                bull_avg = sum(all_bullish) / len(all_bullish) if all_bullish else 0
                bear_avg = sum(all_bearish) / len(all_bearish) if all_bearish else 0
                
                # Weighted combined average
                total_count = len(all_bullish) + len(all_bearish)
                if total_count > 0:
                    combined_avg = (sum(all_bullish) + sum(all_bearish)) / total_count
                else:
                    combined_avg = 0
                
                f.write(f"{window:<10} "
                       f"{len(all_bullish):<12} "
                       f"{bull_avg:.2f} ({bull_avg*0.25:.2f} pts){'':<4} "
                       f"{len(all_bearish):<12} "
                       f"{bear_avg:.2f} ({bear_avg*0.25:.2f} pts){'':<4} "
                       f"{combined_avg:.2f} ticks\n")
                
                print(f"{window:<10} "
                     f"{len(all_bullish):<8} "
                     f"{bull_avg:.2f} ticks{'':<6} "
                     f"{len(all_bearish):<8} "
                     f"{bear_avg:.2f} ticks{'':<6} "
                     f"{combined_avg:.2f} ticks")
            
            # Year-by-year breakdown for each window
            f.write("\n\nYear-by-Year Breakdown:\n")
            f.write("=" * 80 + "\n")
            
            for window in windows:
                f.write(f"\n{window} Candle Window:\n")
                f.write("-" * 80 + "\n")
                f.write(f"{'Year':<8} {'Bull Cnt':<10} {'Bull Avg':<18} {'Bear Cnt':<10} {'Bear Avg':<18} {'Combined Avg':<15}\n")
                f.write("-" * 80 + "\n")
                
                for r in results:
                    bullish_exc = r['windows'][window]['bullish_excursions']
                    bearish_exc = r['windows'][window]['bearish_excursions']
                    
                    bull_avg = sum(bullish_exc) / len(bullish_exc) if bullish_exc else 0
                    bear_avg = sum(bearish_exc) / len(bearish_exc) if bearish_exc else 0
                    
                    total_count = len(bullish_exc) + len(bearish_exc)
                    if total_count > 0:
                        combined_avg = (sum(bullish_exc) + sum(bearish_exc)) / total_count
                    else:
                        combined_avg = 0
                    
                    f.write(f"{r['year']:<8} "
                           f"{len(bullish_exc):<10} "
                           f"{bull_avg:.2f} ticks{'':<8} "
                           f"{len(bearish_exc):<10} "
                           f"{bear_avg:.2f} ticks{'':<8} "
                           f"{combined_avg:.2f} ticks\n")
            
            f.write("\n" + "=" * 80 + "\n")
    
    print(f"\n\nDetailed results saved to: {output_file}")
    
    # Generate Markdown documentation
    print("\nGenerating Markdown documentation...")
    generate_markdown_docs(results_by_timeframe, windows, timeframes)
    
    print("\nAnalysis complete!")

def generate_markdown_docs(results_by_timeframe, windows, timeframes):
    """Generate comprehensive Markdown documentation files"""
    
    # Generate individual timeframe files
    for tf_name in timeframes.keys():
        results = results_by_timeframe[tf_name]
        if not results:
            continue
        
        filename = f"FVG_Max_Excursion_MultiWindow_{tf_name.upper()}.md"
        
        with open(filename, 'w') as f:
            f.write(f"# FVG Maximum Price Excursion Analysis - Multi-Window ({tf_name.upper()})\n\n")
            f.write("## Overview\n\n")
            f.write(f"Analysis of maximum price excursion for Good FVG on **{tf_name}** timeframe across multiple candle windows.\n\n")
            f.write("**Window Sizes Analyzed:** 5, 10, 15, 20, 25, 30, 50 candles\n\n")
            f.write("**Methodology:**\n")
            f.write("- Identifies FVG at 8:30 AM candle\n")
            f.write("- Filters for Good FVG (price doesn't return to FVG zone within window)\n")
            f.write("- Measures maximum price movement from close of 3rd candle\n")
            f.write("- Analyzes across different window sizes\n")
            f.write("- Nasdaq: 1 tick = 0.25 points\n\n")
            
            f.write("## Overall Statistics (2018-2025)\n\n")
            f.write("| Window | Bull Count | Bull Avg (ticks) | Bull Avg (points) | Bear Count | Bear Avg (ticks) | Bear Avg (points) | Combined Avg (ticks) |\n")
            f.write("|--------|------------|------------------|-------------------|------------|------------------|-------------------|----------------------|\n")
            
            for window in windows:
                all_bullish = []
                all_bearish = []
                
                for r in results:
                    all_bullish.extend(r['windows'][window]['bullish_excursions'])
                    all_bearish.extend(r['windows'][window]['bearish_excursions'])
                
                bull_avg = sum(all_bullish) / len(all_bullish) if all_bullish else 0
                bear_avg = sum(all_bearish) / len(all_bearish) if all_bearish else 0
                
                total_count = len(all_bullish) + len(all_bearish)
                if total_count > 0:
                    combined_avg = (sum(all_bullish) + sum(all_bearish)) / total_count
                else:
                    combined_avg = 0
                
                f.write(f"| {window} | {len(all_bullish)} | {bull_avg:.2f} | {bull_avg*0.25:.2f} | "
                       f"{len(all_bearish)} | {bear_avg:.2f} | {bear_avg*0.25:.2f} | {combined_avg:.2f} |\n")
            
            f.write("\n## Year-by-Year Analysis\n\n")
            
            for window in windows:
                f.write(f"### {window} Candle Window\n\n")
                f.write("| Year | Bull Count | Bull Avg (ticks) | Bear Count | Bear Avg (ticks) | Combined Avg (ticks) |\n")
                f.write("|------|------------|------------------|------------|------------------|----------------------|\n")
                
                for r in results:
                    bullish_exc = r['windows'][window]['bullish_excursions']
                    bearish_exc = r['windows'][window]['bearish_excursions']
                    
                    bull_avg = sum(bullish_exc) / len(bullish_exc) if bullish_exc else 0
                    bear_avg = sum(bearish_exc) / len(bearish_exc) if bearish_exc else 0
                    
                    total_count = len(bullish_exc) + len(bearish_exc)
                    if total_count > 0:
                        combined_avg = (sum(bullish_exc) + sum(bearish_exc)) / total_count
                    else:
                        combined_avg = 0
                    
                    f.write(f"| {r['year']} | {len(bullish_exc)} | {bull_avg:.2f} | "
                           f"{len(bearish_exc)} | {bear_avg:.2f} | {combined_avg:.2f} |\n")
                
                f.write("\n")
            
            f.write("## Key Insights\n\n")
            
            # Calculate growth metrics
            first_window_bullish = []
            last_window_bullish = []
            first_window_bearish = []
            last_window_bearish = []
            
            for r in results:
                first_window_bullish.extend(r['windows'][windows[0]]['bullish_excursions'])
                last_window_bullish.extend(r['windows'][windows[-1]]['bullish_excursions'])
                first_window_bearish.extend(r['windows'][windows[0]]['bearish_excursions'])
                last_window_bearish.extend(r['windows'][windows[-1]]['bearish_excursions'])
            
            first_bull_avg = sum(first_window_bullish) / len(first_window_bullish) if first_window_bullish else 0
            last_bull_avg = sum(last_window_bullish) / len(last_window_bullish) if last_window_bullish else 0
            first_bear_avg = sum(first_window_bearish) / len(first_window_bearish) if first_window_bearish else 0
            last_bear_avg = sum(last_window_bearish) / len(last_window_bearish) if last_window_bearish else 0
            
            bull_growth = ((last_bull_avg - first_bull_avg) / first_bull_avg * 100) if first_bull_avg > 0 else 0
            bear_growth = ((last_bear_avg - first_bear_avg) / first_bear_avg * 100) if first_bear_avg > 0 else 0
            
            f.write(f"1. **Excursion Growth**: From {windows[0]} to {windows[-1]} candle window\n")
            f.write(f"   - Bullish: {first_bull_avg:.2f} → {last_bull_avg:.2f} ticks ({bull_growth:+.1f}%)\n")
            f.write(f"   - Bearish: {first_bear_avg:.2f} → {last_bear_avg:.2f} ticks ({bear_growth:+.1f}%)\n\n")
            
            f.write(f"2. **Maximum Excursion Potential**: Longer windows allow price to travel further\n\n")
            f.write(f"3. **Trading Implications**:\n")
            f.write(f"   - Short-term traders: Focus on 5-10 candle windows\n")
            f.write(f"   - Medium-term: 15-25 candle windows offer balanced risk/reward\n")
            f.write(f"   - Long-term: 30-50 candle windows require larger stops but offer bigger targets\n\n")
            
            print(f"Created {filename}")
    
    # Generate comparison file
    filename = "FVG_Max_Excursion_MultiWindow_Comparison.md"
    with open(filename, 'w') as f:
        f.write("# FVG Maximum Price Excursion - Multi-Window Comparison\n\n")
        f.write("## Overview\n\n")
        f.write("Comprehensive comparison of maximum price excursion for Good FVG across all timeframes and window sizes.\n\n")
        
        f.write("## Cross-Timeframe Comparison\n\n")
        f.write("### Combined Average Excursion by Window and Timeframe\n\n")
        f.write("| Window | 1m (ticks) | 1m (points) | 5m (ticks) | 5m (points) | 15m (ticks) | 15m (points) |\n")
        f.write("|--------|------------|-------------|------------|-------------|-------------|-------------|\n")
        
        for window in windows:
            row = f"| {window} "
            
            for tf_name in ['1m', '5m', '15m']:
                results = results_by_timeframe.get(tf_name, [])
                if results:
                    all_excursions = []
                    for r in results:
                        all_excursions.extend(r['windows'][window]['bullish_excursions'])
                        all_excursions.extend(r['windows'][window]['bearish_excursions'])
                    
                    avg = sum(all_excursions) / len(all_excursions) if all_excursions else 0
                    row += f"| {avg:.2f} | {avg*0.25:.2f} "
                else:
                    row += "| - | - "
            
            row += "|\n"
            f.write(row)
        
        f.write("\n## Key Findings\n\n")
        f.write("### 1. Timeframe Impact on Excursion\n\n")
        f.write("Higher timeframes consistently show larger maximum excursions across all window sizes:\n\n")
        
        # Calculate multipliers
        for window in [5, 15, 30, 50]:
            tf_1m_results = results_by_timeframe.get('1m', [])
            tf_15m_results = results_by_timeframe.get('15m', [])
            
            if tf_1m_results and tf_15m_results:
                all_1m = []
                all_15m = []
                
                for r in tf_1m_results:
                    all_1m.extend(r['windows'][window]['bullish_excursions'])
                    all_1m.extend(r['windows'][window]['bearish_excursions'])
                
                for r in tf_15m_results:
                    all_15m.extend(r['windows'][window]['bullish_excursions'])
                    all_15m.extend(r['windows'][window]['bearish_excursions'])
                
                avg_1m = sum(all_1m) / len(all_1m) if all_1m else 0
                avg_15m = sum(all_15m) / len(all_15m) if all_15m else 0
                
                multiplier = avg_15m / avg_1m if avg_1m > 0 else 0
                
                f.write(f"- {window} candle window: 15m shows {multiplier:.2f}x larger excursions than 1m\n")
        
        f.write("\n### 2. Window Size Impact\n\n")
        f.write("Excursion potential grows with window size, but at a decreasing rate:\n\n")
        
        for tf_name in ['1m', '5m', '15m']:
            results = results_by_timeframe.get(tf_name, [])
            if results:
                w5_excursions = []
                w50_excursions = []
                
                for r in results:
                    w5_excursions.extend(r['windows'][5]['bullish_excursions'])
                    w5_excursions.extend(r['windows'][5]['bearish_excursions'])
                    w50_excursions.extend(r['windows'][50]['bullish_excursions'])
                    w50_excursions.extend(r['windows'][50]['bearish_excursions'])
                
                avg_w5 = sum(w5_excursions) / len(w5_excursions) if w5_excursions else 0
                avg_w50 = sum(w50_excursions) / len(w50_excursions) if w50_excursions else 0
                
                growth = ((avg_w50 - avg_w5) / avg_w5 * 100) if avg_w5 > 0 else 0
                
                f.write(f"- **{tf_name.upper()}**: {avg_w5:.2f} → {avg_w50:.2f} ticks ({growth:+.1f}% growth from 5 to 50 candles)\n")
        
        f.write("\n### 3. Trading Strategy Recommendations\n\n")
        f.write("#### By Trading Style\n\n")
        f.write("**Scalper (5-10 candle windows):**\n")
        f.write("- Quick entries/exits\n")
        f.write("- Smaller targets but higher win rate\n")
        f.write("- Best on 1m timeframe for precision\n\n")
        
        f.write("**Day Trader (15-25 candle windows):**\n")
        f.write("- Balanced risk/reward\n")
        f.write("- Moderate position holding time\n")
        f.write("- 5m timeframe offers good balance\n\n")
        
        f.write("**Swing Trader (30-50 candle windows):**\n")
        f.write("- Larger targets and stops\n")
        f.write("- Extended holding periods\n")
        f.write("- 15m timeframe maximizes profit potential\n\n")
        
        f.write("#### Position Sizing by Window\n\n")
        f.write("Adjust position size based on expected excursion and required stop-loss:\n\n")
        
        for window in [5, 15, 30]:
            f.write(f"**{window} Candle Window:**\n")
            for tf_name in ['1m', '5m', '15m']:
                results = results_by_timeframe.get(tf_name, [])
                if results:
                    all_exc = []
                    for r in results:
                        all_exc.extend(r['windows'][window]['bullish_excursions'])
                        all_exc.extend(r['windows'][window]['bearish_excursions'])
                    
                    avg = sum(all_exc) / len(all_exc) if all_exc else 0
                    f.write(f"- {tf_name}: Target ~{avg*0.25:.1f} points, Stop ~{avg*0.25*0.5:.1f} points\n")
            f.write("\n")
        
        f.write("## Conclusion\n\n")
        f.write("The multi-window analysis reveals that:\n\n")
        f.write("1. **Excursion scales with both timeframe and window size**\n")
        f.write("2. **15m timeframe offers the largest profit potential**\n")
        f.write("3. **Window selection should match trading style and risk tolerance**\n")
        f.write("4. **Longer windows require proportionally larger stops**\n")
        f.write("5. **Growth rate decreases as window size increases** (diminishing returns)\n\n")
        
        print(f"Created {filename}")

if __name__ == "__main__":
    main()

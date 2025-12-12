"""
Example: Using ICT Feature Engineering Components Independently

This script demonstrates how to use individual components of the
ICT backtesting system for custom analysis.
"""

from ict_three_strategies_backtest import DataLoader, ICT_Features
import pandas as pd

def example_1_load_and_analyze_single_timeframe():
    """
    Example 1: Load data and apply ICT features to a single timeframe
    """
    print("="*80)
    print("EXAMPLE 1: Single Timeframe Feature Engineering")
    print("="*80)
    
    # Load 5-minute data
    loader = DataLoader()
    m5_data = loader.load_data('5m', start_year=2024, end_year=2024)
    
    print(f"\nLoaded {len(m5_data):,} candles for 2024")
    print(f"Date range: {m5_data['Datetime'].min()} to {m5_data['Datetime'].max()}")
    
    # Apply ICT features
    features = ICT_Features(m5_data)
    features.detect_swing_points(window=1) \
            .detect_fvg() \
            .detect_mss(lookback=20) \
            .detect_order_blocks()
    
    m5_featured = features.get_dataframe()
    
    # Analyze FVG occurrences
    bullish_fvg_count = m5_featured['FVG_Bullish_Top'].notna().sum()
    bearish_fvg_count = m5_featured['FVG_Bearish_Top'].notna().sum()
    
    print(f"\nFair Value Gaps Found:")
    print(f"  Bullish FVG: {bullish_fvg_count}")
    print(f"  Bearish FVG: {bearish_fvg_count}")
    
    # Analyze MSS occurrences
    bullish_mss_count = (m5_featured['MSS_Bullish'] == 1).sum()
    bearish_mss_count = (m5_featured['MSS_Bearish'] == 1).sum()
    
    print(f"\nMarket Structure Shifts:")
    print(f"  Bullish MSS: {bullish_mss_count}")
    print(f"  Bearish MSS: {bearish_mss_count}")
    
    # Analyze Swing Points
    swing_high_count = (m5_featured['Swing_High'] > 0).sum()
    swing_low_count = (m5_featured['Swing_Low'] > 0).sum()
    
    print(f"\nSwing Points:")
    print(f"  Swing Highs: {swing_high_count}")
    print(f"  Swing Lows: {swing_low_count}")
    
    return m5_featured


def example_2_filter_specific_patterns():
    """
    Example 2: Filter for specific ICT patterns
    """
    print("\n" + "="*80)
    print("EXAMPLE 2: Filter for Specific Patterns")
    print("="*80)
    
    # Load and process data
    loader = DataLoader()
    m5_data = loader.load_data('5m', start_year=2024, end_year=2024)
    
    features = ICT_Features(m5_data)
    features.detect_swing_points(window=1) \
            .detect_fvg() \
            .detect_mss(lookback=20) \
            .detect_order_blocks()
    
    df = features.get_dataframe()
    
    # Find instances where Bullish MSS coincides with Bullish FVG
    bullish_setup = df[
        (df['MSS_Bullish'] == 1) & 
        (df['FVG_Bullish_Top'].notna())
    ].copy()
    
    print(f"\nBullish MSS + FVG Confluence: {len(bullish_setup)} occurrences")
    
    if len(bullish_setup) > 0:
        print("\nFirst 5 occurrences:")
        for idx, row in bullish_setup.head(5).iterrows():
            print(f"  {row['Datetime']}: FVG Zone {row['FVG_Bullish_Bottom']:.2f} - {row['FVG_Bullish_Top']:.2f}")
    
    # Find Order Block opportunities
    bullish_ob = df[df['OB_Bullish_High'].notna()].copy()
    bearish_ob = df[df['OB_Bearish_High'].notna()].copy()
    
    print(f"\nOrder Blocks Found:")
    print(f"  Bullish OB: {len(bullish_ob)}")
    print(f"  Bearish OB: {len(bearish_ob)}")
    
    return df


def example_3_export_features_to_csv():
    """
    Example 3: Export ICT features to CSV for external analysis
    """
    print("\n" + "="*80)
    print("EXAMPLE 3: Export Features to CSV")
    print("="*80)
    
    # Load and process data
    loader = DataLoader()
    m15_data = loader.load_data('15m', start_year=2024, end_year=2024)
    
    features = ICT_Features(m15_data)
    features.detect_swing_points(window=1) \
            .detect_fvg() \
            .detect_mss(lookback=20) \
            .detect_order_blocks()
    
    df = features.get_dataframe()
    
    # Select relevant columns for export
    export_cols = [
        'Datetime', 'Open', 'High', 'Low', 'Close', 'Volume',
        'Swing_High', 'Swing_Low',
        'FVG_Bullish_Top', 'FVG_Bullish_Bottom', 'FVG_Bullish_Mean',
        'FVG_Bearish_Top', 'FVG_Bearish_Bottom', 'FVG_Bearish_Mean',
        'MSS_Bullish', 'MSS_Bearish',
        'OB_Bullish_High', 'OB_Bullish_Low',
        'OB_Bearish_High', 'OB_Bearish_Low'
    ]
    
    output_file = 'ict_features_2024_m15.csv'
    df[export_cols].to_csv(output_file, index=False)
    
    print(f"\nFeatures exported to: {output_file}")
    print(f"Total rows: {len(df):,}")
    print(f"Total columns: {len(export_cols)}")
    
    return df


def example_4_analyze_time_of_day_patterns():
    """
    Example 4: Analyze FVG patterns by time of day
    """
    print("\n" + "="*80)
    print("EXAMPLE 4: Time of Day Analysis")
    print("="*80)
    
    # Load and process data
    loader = DataLoader()
    m5_data = loader.load_data('5m', start_year=2024, end_year=2024)
    
    features = ICT_Features(m5_data)
    features.detect_swing_points(window=1).detect_fvg()
    
    df = features.get_dataframe()
    
    # Extract hour from datetime
    df['Hour'] = df['Datetime'].dt.hour
    
    # Count FVGs by hour
    hourly_stats = []
    
    for hour in range(24):
        hour_data = df[df['Hour'] == hour]
        
        bullish_fvg = hour_data['FVG_Bullish_Top'].notna().sum()
        bearish_fvg = hour_data['FVG_Bearish_Top'].notna().sum()
        
        if bullish_fvg > 0 or bearish_fvg > 0:
            hourly_stats.append({
                'hour': hour,
                'bullish_fvg': bullish_fvg,
                'bearish_fvg': bearish_fvg,
                'total': bullish_fvg + bearish_fvg
            })
    
    # Sort by total FVGs
    hourly_stats.sort(key=lambda x: x['total'], reverse=True)
    
    print("\nTop 5 Hours for FVG Formation (EST):")
    print("-" * 60)
    print(f"{'Hour':<10} {'Bullish FVG':<15} {'Bearish FVG':<15} {'Total':<10}")
    print("-" * 60)
    
    for stat in hourly_stats[:5]:
        hour_str = f"{stat['hour']:02d}:00"
        print(f"{hour_str:<10} {stat['bullish_fvg']:<15} {stat['bearish_fvg']:<15} {stat['total']:<10}")
    
    return df


def example_5_custom_swing_window():
    """
    Example 5: Use custom swing point window sizes
    """
    print("\n" + "="*80)
    print("EXAMPLE 5: Custom Swing Point Detection")
    print("="*80)
    
    loader = DataLoader()
    h1_data = loader.load_data('1H', start_year=2024, end_year=2024)
    
    # Test different window sizes
    for window in [1, 2, 3]:
        features = ICT_Features(h1_data)
        features.detect_swing_points(window=window)
        df = features.get_dataframe()
        
        swing_high_count = (df['Swing_High'] > 0).sum()
        swing_low_count = (df['Swing_Low'] > 0).sum()
        
        print(f"\nWindow Size {window} ({2*window+1}-candle pattern):")
        print(f"  Swing Highs: {swing_high_count}")
        print(f"  Swing Lows: {swing_low_count}")
        print(f"  Total Swings: {swing_high_count + swing_low_count}")


if __name__ == "__main__":
    print("\n" + "="*80)
    print("ICT FEATURE ENGINEERING - USAGE EXAMPLES")
    print("="*80)
    print("\nThis script demonstrates various ways to use the ICT components")
    print("for custom analysis and research.\n")
    
    # Run examples
    try:
        example_1_load_and_analyze_single_timeframe()
        example_2_filter_specific_patterns()
        example_3_export_features_to_csv()
        example_4_analyze_time_of_day_patterns()
        example_5_custom_swing_window()
        
        print("\n" + "="*80)
        print("ALL EXAMPLES COMPLETED SUCCESSFULLY")
        print("="*80)
        
    except Exception as e:
        print(f"\nError running examples: {e}")
        import traceback
        traceback.print_exc()

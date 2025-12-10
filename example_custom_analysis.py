"""
Example: Custom Daily Bias Analysis

This script demonstrates how to use the DailyBiasProbabilityAnalyzer class
to perform custom analysis on different symbols and time periods.
"""

from daily_bias_probability_analysis import DailyBiasProbabilityAnalyzer


def example_1_analyze_bitcoin():
    """
    Example 1: Analyze Bitcoin (BTC-USD) daily bias
    """
    print("\n" + "="*80)
    print("EXAMPLE 1: Bitcoin Daily Bias Analysis")
    print("="*80)
    
    analyzer = DailyBiasProbabilityAnalyzer(
        symbol='BTC-USD',
        start_date='2020-01-01',  # Start from 2020 for more recent crypto data
        end_date='2025-12-31'
    )
    
    try:
        results = analyzer.run_full_analysis()
        print("\n✅ Bitcoin analysis complete!")
    except Exception as e:
        print(f"❌ Error: {e}")


def example_2_analyze_nq_local():
    """
    Example 2: Analyze NQ futures from local CSV files
    """
    print("\n" + "="*80)
    print("EXAMPLE 2: NQ Futures (Local CSV)")
    print("="*80)
    
    analyzer = DailyBiasProbabilityAnalyzer(
        symbol='NQ',
        start_date='2018-01-01',
        use_local_csv=True,
        csv_dir='.'  # Current directory
    )
    
    try:
        results = analyzer.run_full_analysis()
        print("\n✅ NQ analysis complete!")
        
        # Access specific results
        print("\n📊 Custom Result Extraction:")
        print(f"   Momentum after 1 green: {results['momentum']['1_green']['prob_green']:.2f}%")
        print(f"   PDL sweep reversal rate: {results['price_action']['pdl_sweep']['prob_reversal']:.2f}%")
        
    except Exception as e:
        print(f"❌ Error: {e}")


def example_3_analyze_specific_period():
    """
    Example 3: Analyze a specific time period (e.g., 2023 only)
    """
    print("\n" + "="*80)
    print("EXAMPLE 3: Specific Period Analysis (2023 only)")
    print("="*80)
    
    analyzer = DailyBiasProbabilityAnalyzer(
        symbol='NQ',
        start_date='2023-01-01',
        end_date='2023-12-31',
        use_local_csv=True,
        csv_dir='.'
    )
    
    try:
        results = analyzer.run_full_analysis()
        print("\n✅ 2023 analysis complete!")
    except Exception as e:
        print(f"❌ Error: {e}")


def example_4_compare_periods():
    """
    Example 4: Compare statistics across different periods
    """
    print("\n" + "="*80)
    print("EXAMPLE 4: Period Comparison (2018-2020 vs 2021-2023)")
    print("="*80)
    
    # Period 1: 2018-2020
    print("\n📅 Period 1: 2018-2020")
    analyzer1 = DailyBiasProbabilityAnalyzer(
        symbol='NQ',
        start_date='2018-01-01',
        end_date='2020-12-31',
        use_local_csv=True,
        csv_dir='.'
    )
    
    try:
        results1 = analyzer1.run_full_analysis()
        period1_green_continuation = results1['momentum']['1_green']['prob_green']
    except Exception as e:
        print(f"❌ Period 1 error: {e}")
        period1_green_continuation = None
    
    # Period 2: 2021-2023
    print("\n📅 Period 2: 2021-2023")
    analyzer2 = DailyBiasProbabilityAnalyzer(
        symbol='NQ',
        start_date='2021-01-01',
        end_date='2023-12-31',
        use_local_csv=True,
        csv_dir='.'
    )
    
    try:
        results2 = analyzer2.run_full_analysis()
        period2_green_continuation = results2['momentum']['1_green']['prob_green']
    except Exception as e:
        print(f"❌ Period 2 error: {e}")
        period2_green_continuation = None
    
    # Comparison
    if period1_green_continuation and period2_green_continuation:
        print("\n" + "="*80)
        print("📊 COMPARISON RESULTS")
        print("="*80)
        print(f"Green continuation after 1 green candle:")
        print(f"   Period 1 (2018-2020): {period1_green_continuation:.2f}%")
        print(f"   Period 2 (2021-2023): {period2_green_continuation:.2f}%")
        print(f"   Difference: {period2_green_continuation - period1_green_continuation:+.2f}%")


def example_5_custom_analysis():
    """
    Example 5: Extract data and perform custom calculations
    """
    print("\n" + "="*80)
    print("EXAMPLE 5: Custom Statistical Analysis")
    print("="*80)
    
    analyzer = DailyBiasProbabilityAnalyzer(
        symbol='NQ',
        start_date='2018-01-01',
        use_local_csv=True,
        csv_dir='.'
    )
    
    try:
        # Fetch and prepare data
        analyzer.fetch_data()
        
        # Access the dataframe for custom analysis
        df = analyzer.df
        
        print(f"\n📊 Custom Statistics:")
        print(f"   Total candles: {len(df)}")
        print(f"   Green candles: {(df['Candle_Direction'] == 1).sum()} ({(df['Candle_Direction'] == 1).sum() / len(df) * 100:.2f}%)")
        print(f"   Red candles: {(df['Candle_Direction'] == -1).sum()} ({(df['Candle_Direction'] == -1).sum() / len(df) * 100:.2f}%)")
        print(f"   Average daily range: {df['Daily_Range'].mean():.2f}")
        print(f"   Maximum daily range: {df['Daily_Range'].max():.2f}")
        print(f"   Minimum daily range: {df['Daily_Range'].min():.2f}")
        
        # Calculate additional custom metrics
        import numpy as np
        
        # Days with range > 2x ADR (extreme volatility)
        extreme_vol = df['Range_Ratio'] > 2.0
        print(f"\n   Extreme volatility days (>2x ADR): {extreme_vol.sum()} ({extreme_vol.sum() / len(df) * 100:.2f}%)")
        
        # Win streaks analysis
        green_streaks = []
        current_streak = 0
        for direction in df['Candle_Direction']:
            if direction == 1:
                current_streak += 1
            else:
                if current_streak > 0:
                    green_streaks.append(current_streak)
                current_streak = 0
        if current_streak > 0:
            green_streaks.append(current_streak)
        
        if green_streaks:
            print(f"\n   Longest green streak: {max(green_streaks)} candles")
            print(f"   Average green streak: {np.mean(green_streaks):.2f} candles")
        
    except Exception as e:
        print(f"❌ Error: {e}")


def main():
    """
    Run all examples
    """
    print("\n" + "="*80)
    print("🎯 DAILY BIAS ANALYSIS - CUSTOM EXAMPLES")
    print("="*80)
    
    # Uncomment the examples you want to run:
    
    # example_1_analyze_bitcoin()
    # example_2_analyze_nq_local()
    # example_3_analyze_specific_period()
    # example_4_compare_periods()
    example_5_custom_analysis()
    
    print("\n" + "="*80)
    print("✅ ALL EXAMPLES COMPLETED")
    print("="*80)


if __name__ == "__main__":
    main()

"""
Analyze Exit Timing - TP and SL Hit Timing Analysis
Calculate average number of candles until TP or SL is hit after entry
"""

import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')


def get_candles_to_exit(entry_time, exit_time, timeframe):
    """
    Calculate number of candles between entry and exit
    
    Parameters:
    -----------
    entry_time : datetime
        Entry time
    exit_time : datetime
        Exit time
    timeframe : str
        Timeframe ('1m', '5m', '15m')
    
    Returns:
    --------
    int
        Number of candles
    """
    if pd.isna(entry_time) or pd.isna(exit_time):
        return None
    
    # Parse if strings
    if isinstance(entry_time, str):
        entry_time = pd.to_datetime(entry_time)
    if isinstance(exit_time, str):
        exit_time = pd.to_datetime(exit_time)
    
    time_diff = exit_time - entry_time
    minutes_diff = time_diff.total_seconds() / 60
    
    # Convert to candles based on timeframe
    if timeframe == '1m':
        candles = int(minutes_diff / 1)
    elif timeframe == '5m':
        candles = int(minutes_diff / 5)
    elif timeframe == '15m':
        candles = int(minutes_diff / 15)
    else:
        return None
    
    return max(1, candles)  # At least 1 candle


def analyze_timing_from_csv(csv_path, timeframe, rr_ratio, sl_placement):
    """
    Analyze timing from a trade CSV file
    
    Returns:
    --------
    dict with timing statistics
    """
    if not os.path.exists(csv_path):
        return None
    
    try:
        df = pd.read_csv(csv_path)
        
        if len(df) == 0:
            return None
        
        # Calculate candles to exit for each trade
        df['candles_to_exit'] = df.apply(
            lambda row: get_candles_to_exit(row['entry_time'], row['exit_time'], timeframe),
            axis=1
        )
        
        # Filter out None values
        df = df[df['candles_to_exit'].notna()].copy()
        
        if len(df) == 0:
            return None
        
        # Separate TP and SL exits
        tp_trades = df[df['exit_reason'] == 'TP'].copy()
        sl_trades = df[df['exit_reason'] == 'SL'].copy()
        eod_trades = df[df['exit_reason'] == 'EOD'].copy()
        
        result = {
            'timeframe': timeframe,
            'rr_ratio': rr_ratio,
            'sl_placement': sl_placement,
            'total_trades': len(df),
            'tp_count': len(tp_trades),
            'sl_count': len(sl_trades),
            'eod_count': len(eod_trades),
            'avg_candles_tp': tp_trades['candles_to_exit'].mean() if len(tp_trades) > 0 else None,
            'median_candles_tp': tp_trades['candles_to_exit'].median() if len(tp_trades) > 0 else None,
            'min_candles_tp': tp_trades['candles_to_exit'].min() if len(tp_trades) > 0 else None,
            'max_candles_tp': tp_trades['candles_to_exit'].max() if len(tp_trades) > 0 else None,
            'avg_candles_sl': sl_trades['candles_to_exit'].mean() if len(sl_trades) > 0 else None,
            'median_candles_sl': sl_trades['candles_to_exit'].median() if len(sl_trades) > 0 else None,
            'min_candles_sl': sl_trades['candles_to_exit'].min() if len(sl_trades) > 0 else None,
            'max_candles_sl': sl_trades['candles_to_exit'].max() if len(sl_trades) > 0 else None,
            'avg_candles_eod': eod_trades['candles_to_exit'].mean() if len(eod_trades) > 0 else None,
        }
        
        return result
        
    except Exception as e:
        print(f"Error processing {csv_path}: {e}")
        return None


def analyze_all_configurations():
    """Analyze all available configurations"""
    
    print("\n" + "="*80)
    print("EXIT TIMING ANALYSIS - FVG STRATEGY")
    print("="*80)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    results = []
    
    # R/R Analysis (middle SL placement)
    print("Analyzing R/R ratio configurations (middle SL)...")
    rr_dir = 'results_rr_analysis'
    if os.path.exists(rr_dir):
        for timeframe in ['1m', '5m', '15m']:
            for rr in [1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]:
                csv_path = os.path.join(rr_dir, f'trades_{timeframe}_rr{rr}.csv')
                result = analyze_timing_from_csv(csv_path, timeframe, rr, 'middle')
                if result:
                    results.append(result)
                    print(f"  {timeframe} R/R {rr}: {result['tp_count']} TP, {result['sl_count']} SL")
    
    # SL Placement Analysis
    print("\nAnalyzing SL placement configurations...")
    sl_dir = 'results_sl_placement'
    if os.path.exists(sl_dir):
        # Sample files (15m, 2022-2024)
        for sl_placement in ['top', 'bottom', 'first_candle']:
            for rr in [2.0, 3.0, 5.0]:
                csv_path = os.path.join(sl_dir, f'trades_15m_{sl_placement}_rr{rr}_sample.csv')
                result = analyze_timing_from_csv(csv_path, '15m', rr, sl_placement)
                if result:
                    results.append(result)
                    print(f"  15m {sl_placement} R/R {rr}: {result['tp_count']} TP, {result['sl_count']} SL")
        
        # 1m full data if available
        for sl_placement in ['top', 'bottom', 'first_candle']:
            for rr in [1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]:
                csv_path = os.path.join(sl_dir, f'trades_1m_{sl_placement}_rr{rr}.csv')
                result = analyze_timing_from_csv(csv_path, '1m', rr, sl_placement)
                if result:
                    results.append(result)
    
    return results


def generate_timing_report(results, output_dir='results_timing_analysis'):
    """Generate comprehensive timing analysis report"""
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Convert to DataFrame
    df = pd.DataFrame(results)
    
    # Save detailed CSV
    csv_path = os.path.join(output_dir, 'exit_timing_detailed.csv')
    df.to_csv(csv_path, index=False)
    print(f"\nDetailed CSV saved to: {csv_path}")
    
    # Generate markdown report
    report_path = os.path.join(output_dir, 'exit_timing_report.md')
    
    with open(report_path, 'w') as f:
        f.write("# FVG Strategy - Exit Timing Analysis\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("---\n\n")
        
        f.write("## Executive Summary\n\n")
        f.write("This report analyzes the average number of candles required to hit TP or SL ")
        f.write("after the entry candle (3rd candle of FVG pattern).\n\n")
        
        f.write("**Key Metrics:**\n")
        f.write("- Average candles to TP\n")
        f.write("- Average candles to SL\n")
        f.write("- Median values for robustness\n")
        f.write("- Min/Max ranges\n\n")
        
        # Group by timeframe
        for timeframe in df['timeframe'].unique():
            f.write(f"\n## {timeframe.upper()} Timeframe\n\n")
            
            tf_data = df[df['timeframe'] == timeframe].copy()
            
            # Group by SL placement
            for sl_placement in tf_data['sl_placement'].unique():
                sl_data = tf_data[tf_data['sl_placement'] == sl_placement].copy()
                
                sl_name = {
                    'middle': 'Middle of FVG',
                    'top': 'Top/Bottom of FVG',
                    'bottom': 'Bottom/Top of FVG',
                    'first_candle': 'First Candle'
                }.get(sl_placement, sl_placement)
                
                f.write(f"\n### SL Placement: {sl_name}\n\n")
                
                # Create table
                f.write("| R/R | Total | TP Count | SL Count | Avg Candles TP | Avg Candles SL | Median TP | Median SL |\n")
                f.write("|-----|-------|----------|----------|----------------|----------------|-----------|----------|\n")
                
                for _, row in sl_data.sort_values('rr_ratio').iterrows():
                    tp_avg = f"{row['avg_candles_tp']:.1f}" if pd.notna(row['avg_candles_tp']) else "N/A"
                    sl_avg = f"{row['avg_candles_sl']:.1f}" if pd.notna(row['avg_candles_sl']) else "N/A"
                    tp_med = f"{row['median_candles_tp']:.0f}" if pd.notna(row['median_candles_tp']) else "N/A"
                    sl_med = f"{row['median_candles_sl']:.0f}" if pd.notna(row['median_candles_sl']) else "N/A"
                    
                    f.write(f"| {row['rr_ratio']:.1f} | {row['total_trades']} | {row['tp_count']} | {row['sl_count']} | ")
                    f.write(f"{tp_avg} | {sl_avg} | {tp_med} | {sl_med} |\n")
                
                # Summary statistics
                if len(sl_data) > 0:
                    avg_tp_overall = sl_data['avg_candles_tp'].mean()
                    avg_sl_overall = sl_data['avg_candles_sl'].mean()
                    
                    f.write(f"\n**Overall Averages:**\n")
                    f.write(f"- Average candles to TP: {avg_tp_overall:.1f}\n")
                    f.write(f"- Average candles to SL: {avg_sl_overall:.1f}\n\n")
        
        # Key insights
        f.write("\n## Key Insights\n\n")
        
        # Find fastest TP
        df_with_tp = df[df['avg_candles_tp'].notna()].copy()
        if len(df_with_tp) > 0:
            fastest_tp = df_with_tp.loc[df_with_tp['avg_candles_tp'].idxmin()]
            f.write(f"### Fastest Average TP Hit\n")
            f.write(f"- Configuration: {fastest_tp['timeframe'].upper()} - {fastest_tp['sl_placement']} - R/R {fastest_tp['rr_ratio']}\n")
            f.write(f"- Average candles: **{fastest_tp['avg_candles_tp']:.1f}**\n")
            f.write(f"- Median candles: {fastest_tp['median_candles_tp']:.0f}\n\n")
        
        # Find fastest SL
        df_with_sl = df[df['avg_candles_sl'].notna()].copy()
        if len(df_with_sl) > 0:
            fastest_sl = df_with_sl.loc[df_with_sl['avg_candles_sl'].idxmin()]
            f.write(f"### Fastest Average SL Hit\n")
            f.write(f"- Configuration: {fastest_sl['timeframe'].upper()} - {fastest_sl['sl_placement']} - R/R {fastest_sl['rr_ratio']}\n")
            f.write(f"- Average candles: **{fastest_sl['avg_candles_sl']:.1f}**\n")
            f.write(f"- Median candles: {fastest_sl['median_candles_sl']:.0f}\n\n")
        
        # Timing patterns
        f.write("### Timing Patterns\n\n")
        f.write("1. **Lower R/R ratios** generally show faster TP hits (smaller target)\n")
        f.write("2. **Higher R/R ratios** may show slower TP hits but better returns\n")
        f.write("3. **SL placement** significantly affects timing - tighter stops hit faster\n")
        f.write("4. **Timeframe matters** - smaller timeframes show faster exits in absolute time\n\n")
    
    print(f"Report saved to: {report_path}")


def create_timing_visualizations(results, output_dir='results_timing_analysis'):
    """Create visualizations for timing analysis"""
    
    import matplotlib.pyplot as plt
    import seaborn as sns
    
    df = pd.DataFrame(results)
    
    # Filter to have clean data
    df_clean = df[(df['avg_candles_tp'].notna()) & (df['avg_candles_sl'].notna())].copy()
    
    if len(df_clean) == 0:
        print("Not enough data for visualizations")
        return
    
    # Create figure with subplots
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Exit Timing Analysis - Average Candles to TP/SL', 
                 fontsize=18, fontweight='bold')
    
    # Plot 1: TP timing by R/R ratio (middle SL)
    ax = axes[0, 0]
    middle_data = df_clean[df_clean['sl_placement'] == 'middle'].copy()
    if len(middle_data) > 0:
        for tf in middle_data['timeframe'].unique():
            tf_data = middle_data[middle_data['timeframe'] == tf].sort_values('rr_ratio')
            ax.plot(tf_data['rr_ratio'], tf_data['avg_candles_tp'], 
                   marker='o', linewidth=2, markersize=8, label=tf.upper())
        ax.set_xlabel('Risk/Reward Ratio', fontsize=12, fontweight='bold')
        ax.set_ylabel('Average Candles to TP', fontsize=12, fontweight='bold')
        ax.set_title('TP Timing vs R/R Ratio (Middle SL)', fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    # Plot 2: SL timing by R/R ratio (middle SL)
    ax = axes[0, 1]
    if len(middle_data) > 0:
        for tf in middle_data['timeframe'].unique():
            tf_data = middle_data[middle_data['timeframe'] == tf].sort_values('rr_ratio')
            ax.plot(tf_data['rr_ratio'], tf_data['avg_candles_sl'], 
                   marker='s', linewidth=2, markersize=8, label=tf.upper())
        ax.set_xlabel('Risk/Reward Ratio', fontsize=12, fontweight='bold')
        ax.set_ylabel('Average Candles to SL', fontsize=12, fontweight='bold')
        ax.set_title('SL Timing vs R/R Ratio (Middle SL)', fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    # Plot 3: TP timing by SL placement
    ax = axes[1, 0]
    sl_comparison = df_clean.groupby('sl_placement').agg({
        'avg_candles_tp': 'mean',
        'avg_candles_sl': 'mean'
    }).reset_index()
    
    x = range(len(sl_comparison))
    width = 0.35
    ax.bar([i - width/2 for i in x], sl_comparison['avg_candles_tp'], 
           width, label='Avg Candles to TP', color='#2ecc71', alpha=0.8)
    ax.bar([i + width/2 for i in x], sl_comparison['avg_candles_sl'], 
           width, label='Avg Candles to SL', color='#e74c3c', alpha=0.8)
    ax.set_xlabel('SL Placement Strategy', fontsize=12, fontweight='bold')
    ax.set_ylabel('Average Candles', fontsize=12, fontweight='bold')
    ax.set_title('Exit Timing by SL Placement', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(sl_comparison['sl_placement'])
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    
    # Plot 4: Distribution comparison
    ax = axes[1, 1]
    if len(middle_data) > 0:
        # Box plot of TP timing by timeframe
        timeframes = middle_data['timeframe'].unique()
        tp_data = [middle_data[middle_data['timeframe'] == tf]['avg_candles_tp'].values 
                   for tf in timeframes]
        
        bp = ax.boxplot(tp_data, labels=[tf.upper() for tf in timeframes],
                        patch_artist=True)
        for patch in bp['boxes']:
            patch.set_facecolor('#3498db')
            patch.set_alpha(0.7)
        
        ax.set_xlabel('Timeframe', fontsize=12, fontweight='bold')
        ax.set_ylabel('Average Candles to TP', fontsize=12, fontweight='bold')
        ax.set_title('TP Timing Distribution by Timeframe', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    
    viz_path = os.path.join(output_dir, 'exit_timing_analysis.png')
    plt.savefig(viz_path, dpi=150, bbox_inches='tight')
    print(f"Visualization saved to: {viz_path}")


def main():
    """Main execution"""
    
    # Analyze all configurations
    results = analyze_all_configurations()
    
    if len(results) == 0:
        print("\nNo data found to analyze")
        return
    
    print(f"\nAnalyzed {len(results)} configurations")
    
    # Generate report
    print("\nGenerating timing analysis report...")
    generate_timing_report(results)
    
    # Create visualizations
    print("\nCreating visualizations...")
    create_timing_visualizations(results)
    
    print("\n" + "="*80)
    print("TIMING ANALYSIS COMPLETE")
    print("="*80)
    print(f"Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\nResults saved to: results_timing_analysis/")


if __name__ == "__main__":
    main()

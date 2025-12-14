"""
Quick sample run of Stop Loss Placement Analysis
Tests subset of configurations to demonstrate functionality
"""

import os
import pandas as pd
from datetime import datetime
import warnings
warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', category=DeprecationWarning)

from stop_loss_placement_analysis import StopLossPlacementBacktest, generate_sl_comparison_report
from data_loader import DataLoader
from fvg_detector import FVGDetector
from performance_metrics import PerformanceMetrics


def run_sample_analysis():
    """Run sample analysis with subset of data"""
    
    print("\n" + "="*80)
    print("STOP LOSS PLACEMENT ANALYSIS - SAMPLE RUN")
    print("="*80)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    print("Testing 15m timeframe with selected R/R ratios to demonstrate functionality\n")
    
    # Configuration - smaller subset for demo
    START_YEAR = 2022  # Use only recent years for demo
    END_YEAR = 2024
    INITIAL_CAPITAL = 10000
    TIMEFRAME = '15m'  # Start with 15m as it's fastest
    RISK_REWARD_RATIOS = [2.0, 3.0, 5.0]  # Test key ratios
    SL_PLACEMENTS = ['top', 'bottom', 'first_candle']
    SL_NAMES = {
        'top': 'SL at Top/Bottom of FVG',
        'bottom': 'SL at Bottom/Top of FVG',
        'first_candle': 'SL at First Candle'
    }
    OUTPUT_DIR = 'results_sl_placement'
    
    # Create output directory
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"Created output directory: {OUTPUT_DIR}\n")
    
    # Store all results
    all_results = {}
    
    print(f"{'='*80}")
    print(f"PROCESSING {TIMEFRAME.upper()} TIMEFRAME ({START_YEAR}-{END_YEAR})")
    print(f"{'='*80}\n")
    
    # Load data once for this timeframe
    print(f"Loading {TIMEFRAME} data...")
    loader = DataLoader()
    data = loader.load_multiple_years(START_YEAR, END_YEAR, TIMEFRAME)
    data = loader.filter_trading_hours(data, start_hour=8, end_hour=17)
    print(f"Loaded {len(data)} rows\n")
    
    # Detect FVG signals once
    print(f"Detecting FVG signals...")
    detector = FVGDetector()
    data_with_fvg = detector.detect_fvg(data, target_time='08:30:00')
    print()
    
    # Test each SL placement strategy
    for sl_placement in SL_PLACEMENTS:
        print(f"\n{'-'*60}")
        print(f"Testing: {SL_NAMES[sl_placement]}")
        print(f"{'-'*60}\n")
        
        all_results[f"{TIMEFRAME}_{sl_placement}"] = {}
        
        # Test each R/R ratio
        for rr_ratio in RISK_REWARD_RATIOS:
            print(f"  R/R {rr_ratio}...", end=' ', flush=True)
            
            # Run backtest
            engine = StopLossPlacementBacktest(
                initial_capital=INITIAL_CAPITAL,
                risk_reward_ratio=rr_ratio,
                sl_placement=sl_placement
            )
            
            trades_df = engine.run_backtest(data_with_fvg, TIMEFRAME)
            
            if trades_df is None or len(trades_df) == 0:
                print("No trades")
                continue
            
            # Calculate metrics
            perf = PerformanceMetrics(trades_df, initial_capital=INITIAL_CAPITAL)
            metrics = perf.calculate_all_metrics()
            metrics['risk_reward_ratio'] = rr_ratio
            metrics['sl_placement'] = sl_placement
            
            all_results[f"{TIMEFRAME}_{sl_placement}"][rr_ratio] = {
                'trades_df': trades_df,
                'metrics': metrics
            }
            
            # Save trades CSV
            csv_filename = f"trades_{TIMEFRAME}_{sl_placement}_rr{rr_ratio}_sample.csv"
            csv_path = os.path.join(OUTPUT_DIR, csv_filename)
            trades_df.to_csv(csv_path, index=False)
            
            print(f"Trades: {metrics['total_trades']}, Return: {metrics['total_return']:.2f}%, Win Rate: {metrics['win_rate']:.2f}%")
    
    # Generate sample report
    print(f"\n{'='*80}")
    print("GENERATING SAMPLE REPORT")
    print(f"{'='*80}\n")
    
    report_path = os.path.join(OUTPUT_DIR, 'sl_placement_sample_report.md')
    
    with open(report_path, 'w') as f:
        f.write("# FVG Strategy - Stop Loss Placement Analysis (Sample)\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"**Period:** {START_YEAR}-{END_YEAR} (Sample period for demonstration)\n\n")
        f.write(f"**Timeframe:** {TIMEFRAME.upper()}\n\n")
        f.write("---\n\n")
        
        f.write("## Stop Loss Placement Strategies Tested:\n\n")
        f.write("1. **SL at Top/Bottom of FVG:** SL at top (long) / bottom (short)\n")
        f.write("2. **SL at Bottom/Top of FVG:** SL at bottom (long) / top (short)\n")
        f.write("3. **SL at First Candle:** SL below/above first candle (8:29)\n\n")
        
        f.write(f"## {TIMEFRAME.upper()} Timeframe Results\n\n")
        
        for sl_placement in SL_PLACEMENTS:
            key = f"{TIMEFRAME}_{sl_placement}"
            
            if key not in all_results or not all_results[key]:
                continue
            
            sl_name = {
                'top': 'Top/Bottom',
                'bottom': 'Bottom/Top',
                'first_candle': 'First Candle'
            }[sl_placement]
            
            f.write(f"\n### Strategy: SL at {sl_name}\n\n")
            
            # Create table
            f.write("| R/R | Trades | Win Rate (%) | Return (%) | Sharpe | Max DD (%) | Profit Factor |\n")
            f.write("|-----|--------|--------------|------------|--------|------------|---------------|\n")
            
            results = all_results[key]
            for rr in sorted(results.keys()):
                m = results[rr]['metrics']
                f.write(f"| {rr:.1f} | {m['total_trades']} | {m['win_rate']:.2f} | ")
                f.write(f"{m['total_return']:.2f} | {m['sharpe_ratio']:.2f} | ")
                f.write(f"{m['max_drawdown']:.2f} | {m['profit_factor']:.2f} |\n")
            
            # Find best R/R for this strategy
            if results:
                best_rr = max(results.items(), key=lambda x: x[1]['metrics']['total_return'])
                f.write(f"\n**Best R/R:** {best_rr[0]} with {best_rr[1]['metrics']['total_return']:.2f}% return\n\n")
        
        # Comparison
        f.write("\n## Comparison Across SL Placements\n\n")
        
        comparison_data = []
        for sl_placement in SL_PLACEMENTS:
            key = f"{TIMEFRAME}_{sl_placement}"
            if key in all_results and all_results[key]:
                # Get average metrics across R/R ratios
                avg_return = sum(r['metrics']['total_return'] for r in all_results[key].values()) / len(all_results[key])
                avg_win_rate = sum(r['metrics']['win_rate'] for r in all_results[key].values()) / len(all_results[key])
                avg_sharpe = sum(r['metrics']['sharpe_ratio'] for r in all_results[key].values()) / len(all_results[key])
                
                comparison_data.append({
                    'Strategy': sl_placement,
                    'Avg Return': avg_return,
                    'Avg Win Rate': avg_win_rate,
                    'Avg Sharpe': avg_sharpe
                })
        
        if comparison_data:
            f.write("| Strategy | Avg Return (%) | Avg Win Rate (%) | Avg Sharpe |\n")
            f.write("|----------|----------------|------------------|------------|\n")
            for row in comparison_data:
                f.write(f"| {row['Strategy']} | {row['Avg Return']:.2f} | {row['Avg Win Rate']:.2f} | {row['Avg Sharpe']:.2f} |\n")
        
        f.write("\n## Notes\n\n")
        f.write("This is a sample analysis using a subset of data to demonstrate the SL placement analysis functionality.\n")
        f.write(f"For complete analysis across all years and timeframes, run the full `stop_loss_placement_analysis.py` script.\n")
    
    print(f"Sample report saved to: {report_path}")
    
    print(f"\n{'='*80}")
    print("SAMPLE ANALYSIS COMPLETE")
    print(f"{'='*80}")
    print(f"Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"\nSample results saved to: {OUTPUT_DIR}/")
    print("\nTo run complete analysis with all years and timeframes:")
    print("  python3 stop_loss_placement_analysis.py")


if __name__ == "__main__":
    run_sample_analysis()

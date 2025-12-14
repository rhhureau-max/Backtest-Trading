"""
Main Execution Script for FVG Trading Strategy Backtest with Multiple Risk/Reward Ratios
Run complete backtest analysis across multiple timeframes and risk/reward ratios
"""

import os
import sys
from datetime import datetime
import warnings
import pandas as pd
import numpy as np
# Suppress only pandas and matplotlib future warnings
warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', category=DeprecationWarning)

# Import modules
from data_loader import DataLoader
from fvg_detector import FVGDetector
from backtest_engine import BacktestEngine
from performance_metrics import PerformanceMetrics
from visualization import Visualizer
from report_generator import ReportGenerator


def create_output_directory(output_dir='results_rr_analysis'):
    """Create output directory if it doesn't exist"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")
    return output_dir


def run_backtest_for_timeframe_rr(timeframe, risk_reward_ratio, start_year=2018, end_year=2024, 
                                   initial_capital=10000, output_dir='results_rr_analysis'):
    """
    Run complete backtest for a specific timeframe and risk/reward ratio
    
    Parameters:
    -----------
    timeframe : str
        Timeframe to test ('1m', '5m', '15m')
    risk_reward_ratio : float
        Risk/reward ratio (e.g., 2.0 for 2:1)
    start_year : int
        Start year for backtest
    end_year : int
        End year for backtest
    initial_capital : float
        Initial capital for backtest
    output_dir : str
        Output directory for results
        
    Returns:
    --------
    dict
        Dictionary with trades_df and metrics
    """
    print(f"\n{'='*80}")
    print(f"BACKTESTING {timeframe.upper()} - R/R Ratio: {risk_reward_ratio}")
    print(f"{'='*80}")
    
    # Step 1: Load Data
    print(f"\n[1/4] Loading data...")
    loader = DataLoader()
    
    try:
        data = loader.load_multiple_years(start_year, end_year, timeframe)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error loading data: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error loading data: {e}")
        raise
    
    # Filter trading hours (8:00 AM to 5:00 PM)
    data = loader.filter_trading_hours(data, start_hour=8, end_hour=17)
    print(f"Filtered to trading hours: {len(data)} rows")
    
    # Step 2: Detect FVG Signals
    print(f"\n[2/4] Detecting FVG signals at 8:30 AM...")
    detector = FVGDetector()
    data_with_fvg = detector.detect_fvg(data, target_time='08:30:00')
    
    # Step 3: Run Backtest with specific R/R ratio
    print(f"\n[3/4] Running backtest with R/R ratio {risk_reward_ratio}...")
    engine = BacktestEngine(initial_capital=initial_capital, risk_reward_ratio=risk_reward_ratio)
    trades_df = engine.run_backtest(data_with_fvg, timeframe)
    
    if trades_df is None or len(trades_df) == 0:
        print(f"No trades generated for {timeframe} with R/R {risk_reward_ratio}")
        return None
    
    # Step 4: Calculate Performance Metrics
    print(f"\n[4/4] Calculating performance metrics...")
    perf = PerformanceMetrics(trades_df, initial_capital=initial_capital)
    metrics = perf.calculate_all_metrics()
    
    # Add R/R ratio to metrics
    metrics['risk_reward_ratio'] = risk_reward_ratio
    
    # Print summary
    print(f"\n{'='*60}")
    print(f"SUMMARY - {timeframe.upper()} - R/R {risk_reward_ratio}")
    print(f"{'='*60}")
    print(f"Total Trades:        {metrics['total_trades']}")
    print(f"Win Rate:            {metrics['win_rate']:.2f}%")
    print(f"Total Return:        {metrics['total_return']:.2f}%")
    print(f"Profit Factor:       {metrics['profit_factor']:.2f}")
    print(f"Sharpe Ratio:        {metrics['sharpe_ratio']:.2f}")
    print(f"Max Drawdown:        {metrics['max_drawdown']:.2f}%")
    print(f"Avg Win:             ${metrics['avg_win']:.2f}")
    print(f"Avg Loss:            ${metrics['avg_loss']:.2f}")
    print(f"{'='*60}")
    
    return {
        'trades_df': trades_df,
        'metrics': metrics,
        'data': data_with_fvg
    }


def generate_rr_comparison_report(all_results, output_dir):
    """
    Generate comprehensive report comparing different R/R ratios
    
    Parameters:
    -----------
    all_results : dict
        Dictionary of results organized by timeframe and R/R ratio
    output_dir : str
        Output directory for report
    """
    report_path = os.path.join(output_dir, 'rr_comparison_report.md')
    
    with open(report_path, 'w') as f:
        f.write("# FVG Trading Strategy - Risk/Reward Ratio Analysis\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("---\n\n")
        
        f.write("## Executive Summary\n\n")
        f.write("This report compares the performance of the FVG trading strategy across different risk/reward ratios ")
        f.write("(1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0) and timeframes (1m, 5m, 15m).\n\n")
        
        # Summary table for each timeframe
        for timeframe in ['1m', '5m', '15m']:
            f.write(f"\n## {timeframe.upper()} Timeframe - R/R Ratio Comparison\n\n")
            
            if timeframe not in all_results:
                f.write(f"No results available for {timeframe}\n\n")
                continue
            
            # Create comparison table
            f.write("| R/R Ratio | Total Trades | Win Rate (%) | Total Return (%) | Profit Factor | Sharpe Ratio | Max Drawdown (%) | Avg Win ($) | Avg Loss ($) |\n")
            f.write("|-----------|--------------|--------------|------------------|---------------|--------------|------------------|-------------|-------------|\n")
            
            rr_results = all_results[timeframe]
            for rr in sorted(rr_results.keys()):
                metrics = rr_results[rr]['metrics']
                f.write(f"| {rr:.1f} | {metrics['total_trades']} | {metrics['win_rate']:.2f} | ")
                f.write(f"{metrics['total_return']:.2f} | {metrics['profit_factor']:.2f} | ")
                f.write(f"{metrics['sharpe_ratio']:.2f} | {metrics['max_drawdown']:.2f} | ")
                f.write(f"{metrics['avg_win']:.2f} | {metrics['avg_loss']:.2f} |\n")
            
            f.write("\n")
            
            # Find best R/R ratio for this timeframe
            best_rr = None
            best_return = -float('inf')
            for rr, result in rr_results.items():
                if result['metrics']['total_return'] > best_return:
                    best_return = result['metrics']['total_return']
                    best_rr = rr
            
            if best_rr:
                f.write(f"**Best R/R Ratio for {timeframe.upper()}:** {best_rr} with {best_return:.2f}% return\n\n")
        
        # Overall best configuration
        f.write("\n## Overall Best Configuration\n\n")
        best_config = None
        best_overall_return = -float('inf')
        
        for timeframe in all_results:
            for rr, result in all_results[timeframe].items():
                ret = result['metrics']['total_return']
                if ret > best_overall_return:
                    best_overall_return = ret
                    best_config = (timeframe, rr, result['metrics'])
        
        if best_config:
            tf, rr, metrics = best_config
            f.write(f"**Timeframe:** {tf.upper()}\n\n")
            f.write(f"**Risk/Reward Ratio:** {rr}\n\n")
            f.write(f"**Total Return:** {metrics['total_return']:.2f}%\n\n")
            f.write(f"**Sharpe Ratio:** {metrics['sharpe_ratio']:.2f}\n\n")
            f.write(f"**Max Drawdown:** {metrics['max_drawdown']:.2f}%\n\n")
            f.write(f"**Win Rate:** {metrics['win_rate']:.2f}%\n\n")
            f.write(f"**Profit Factor:** {metrics['profit_factor']:.2f}\n\n")
        
        f.write("\n## Key Insights\n\n")
        f.write("### Impact of Risk/Reward Ratio\n\n")
        f.write("- **Lower R/R ratios (1.5-2.5):** Generally higher win rates but lower profit per trade\n")
        f.write("- **Medium R/R ratios (3.0-3.5):** Balanced win rate and profit per trade\n")
        f.write("- **Higher R/R ratios (4.0-5.0):** Lower win rates but higher profit per winning trade\n\n")
        
        f.write("### Recommendations\n\n")
        f.write("1. Choose R/R ratio based on your risk tolerance and market conditions\n")
        f.write("2. Consider using adaptive R/R ratios based on market volatility\n")
        f.write("3. Monitor Sharpe ratio and drawdown alongside returns\n")
        f.write("4. Test the best configuration on out-of-sample data before live trading\n\n")
    
    print(f"\nComparison report saved to: {report_path}")
    
    # Also create a CSV summary
    csv_path = os.path.join(output_dir, 'rr_comparison_summary.csv')
    summary_data = []
    
    for timeframe in all_results:
        for rr, result in all_results[timeframe].items():
            metrics = result['metrics']
            summary_data.append({
                'Timeframe': timeframe,
                'Risk_Reward_Ratio': rr,
                'Total_Trades': metrics['total_trades'],
                'Win_Rate_Pct': metrics['win_rate'],
                'Total_Return_Pct': metrics['total_return'],
                'Profit_Factor': metrics['profit_factor'],
                'Sharpe_Ratio': metrics['sharpe_ratio'],
                'Max_Drawdown_Pct': metrics['max_drawdown'],
                'Avg_Win': metrics['avg_win'],
                'Avg_Loss': metrics['avg_loss']
            })
    
    summary_df = pd.DataFrame(summary_data)
    summary_df.to_csv(csv_path, index=False)
    print(f"CSV summary saved to: {csv_path}")


def main():
    """Main execution function"""
    print("\n" + "="*80)
    print("FVG TRADING STRATEGY - RISK/REWARD RATIO ANALYSIS")
    print("="*80)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Configuration
    START_YEAR = 2018
    END_YEAR = 2024
    INITIAL_CAPITAL = 10000
    TIMEFRAMES = ['1m', '5m', '15m']
    RISK_REWARD_RATIOS = [1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]
    OUTPUT_DIR = 'results_rr_analysis'
    
    # Create output directory
    output_dir = create_output_directory(OUTPUT_DIR)
    
    # Store results for all timeframes and R/R ratios
    all_results = {}
    
    # Run backtest for each timeframe and R/R ratio
    for timeframe in TIMEFRAMES:
        all_results[timeframe] = {}
        
        for rr_ratio in RISK_REWARD_RATIOS:
            result = run_backtest_for_timeframe_rr(
                timeframe=timeframe,
                risk_reward_ratio=rr_ratio,
                start_year=START_YEAR,
                end_year=END_YEAR,
                initial_capital=INITIAL_CAPITAL,
                output_dir=output_dir
            )
            
            if result:
                all_results[timeframe][rr_ratio] = result
                
                # Save individual trade data
                trades_df = result['trades_df']
                csv_path = os.path.join(output_dir, f'trades_{timeframe}_rr{rr_ratio}.csv')
                trades_df.to_csv(csv_path, index=False)
    
    # Generate comprehensive comparison report
    if all_results:
        print(f"\n{'='*80}")
        print("GENERATING COMPREHENSIVE COMPARISON REPORT")
        print(f"{'='*80}")
        
        generate_rr_comparison_report(all_results, output_dir)
    
    print(f"\n{'='*80}")
    print("ANALYSIS COMPLETE")
    print(f"{'='*80}")
    print(f"Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"\nAll results saved to: {output_dir}/")
    print("\nGenerated files:")
    print("  - rr_comparison_report.md (Comprehensive comparison)")
    print("  - rr_comparison_summary.csv (Summary data)")
    for tf in TIMEFRAMES:
        if tf in all_results:
            for rr in RISK_REWARD_RATIOS:
                if rr in all_results[tf]:
                    print(f"  - trades_{tf}_rr{rr}.csv")


if __name__ == "__main__":
    main()

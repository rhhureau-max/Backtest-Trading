"""
Complete the remaining R/R analysis for 15m timeframe and generate report
"""

import os
import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', category=DeprecationWarning)

from data_loader import DataLoader
from fvg_detector import FVGDetector
from backtest_engine import BacktestEngine
from performance_metrics import PerformanceMetrics


def run_single_backtest(data_with_fvg, timeframe, risk_reward_ratio, initial_capital=10000):
    """Run a single backtest with given data and R/R ratio"""
    print(f"Running {timeframe} with R/R {risk_reward_ratio}...")
    
    engine = BacktestEngine(initial_capital=initial_capital, risk_reward_ratio=risk_reward_ratio)
    trades_df = engine.run_backtest(data_with_fvg, timeframe)
    
    if trades_df is None or len(trades_df) == 0:
        return None
    
    perf = PerformanceMetrics(trades_df, initial_capital=initial_capital)
    metrics = perf.calculate_all_metrics()
    metrics['risk_reward_ratio'] = risk_reward_ratio
    
    print(f"  Trades: {metrics['total_trades']}, Win Rate: {metrics['win_rate']:.2f}%, Return: {metrics['total_return']:.2f}%")
    
    return {'trades_df': trades_df, 'metrics': metrics}


def main():
    print("Completing 15m timeframe analysis...")
    
    # Load 15m data once
    loader = DataLoader()
    data = loader.load_multiple_years(2018, 2024, '15m')
    data = loader.filter_trading_hours(data, start_hour=8, end_hour=17)
    
    # Detect FVG signals once
    detector = FVGDetector()
    data_with_fvg = detector.detect_fvg(data, target_time='08:30:00')
    
    # Run remaining R/R ratios for 15m
    remaining_rr = [2.5, 3.0, 3.5, 4.0, 4.5, 5.0]
    output_dir = 'results_rr_analysis'
    
    for rr in remaining_rr:
        result = run_single_backtest(data_with_fvg, '15m', rr)
        if result:
            csv_path = os.path.join(output_dir, f'trades_15m_rr{rr}.csv')
            result['trades_df'].to_csv(csv_path, index=False)
            print(f"  Saved: {csv_path}")
    
    print("\nAll backtests complete! Now generating report...")
    
    # Load all results and generate report
    generate_comprehensive_report(output_dir)


def generate_comprehensive_report(output_dir):
    """Generate comprehensive report from all CSV files"""
    
    # Collect all metrics
    all_results = {}
    
    for timeframe in ['1m', '5m', '15m']:
        all_results[timeframe] = {}
        
        for rr in [1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]:
            csv_path = os.path.join(output_dir, f'trades_{timeframe}_rr{rr}.csv')
            
            if os.path.exists(csv_path):
                trades_df = pd.read_csv(csv_path)
                perf = PerformanceMetrics(trades_df, initial_capital=10000)
                metrics = perf.calculate_all_metrics()
                metrics['risk_reward_ratio'] = rr
                all_results[timeframe][rr] = {'metrics': metrics}
    
    # Generate markdown report
    report_path = os.path.join(output_dir, 'rr_comparison_report.md')
    
    with open(report_path, 'w') as f:
        f.write("# FVG Trading Strategy - Risk/Reward Ratio Analysis\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("---\n\n")
        
        f.write("## Executive Summary\n\n")
        f.write("This report compares the performance of the FVG trading strategy across different risk/reward ratios ")
        f.write("(1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0) and timeframes (1m, 5m, 15m).\n\n")
        f.write("**Analysis Period:** 2018-2024 (7 years)\n\n")
        
        # Summary table for each timeframe
        for timeframe in ['1m', '5m', '15m']:
            f.write(f"\n## {timeframe.upper()} Timeframe - R/R Ratio Comparison\n\n")
            
            if timeframe not in all_results or not all_results[timeframe]:
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
                metrics = rr_results[best_rr]['metrics']
                f.write(f"**Best R/R Ratio for {timeframe.upper()}:** {best_rr}\n")
                f.write(f"- Total Return: {best_return:.2f}%\n")
                f.write(f"- Sharpe Ratio: {metrics['sharpe_ratio']:.2f}\n")
                f.write(f"- Max Drawdown: {metrics['max_drawdown']:.2f}%\n")
                f.write(f"- Win Rate: {metrics['win_rate']:.2f}%\n\n")
        
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
            f.write(f"**Performance Metrics:**\n")
            f.write(f"- Total Return: {metrics['total_return']:.2f}%\n")
            f.write(f"- Sharpe Ratio: {metrics['sharpe_ratio']:.2f}\n")
            f.write(f"- Max Drawdown: {metrics['max_drawdown']:.2f}%\n")
            f.write(f"- Win Rate: {metrics['win_rate']:.2f}%\n")
            f.write(f"- Profit Factor: {metrics['profit_factor']:.2f}\n")
            f.write(f"- Total Trades: {metrics['total_trades']}\n\n")
        
        f.write("\n## Key Insights\n\n")
        f.write("### Impact of Risk/Reward Ratio\n\n")
        f.write("- **Lower R/R ratios (1.5-2.5):** Generally higher win rates but lower profit per trade\n")
        f.write("- **Medium R/R ratios (3.0-3.5):** Balanced win rate and profit per trade\n")
        f.write("- **Higher R/R ratios (4.0-5.0):** Lower win rates but higher profit per winning trade\n\n")
        
        f.write("### Optimal R/R Ratio by Timeframe\n\n")
        for timeframe in ['1m', '5m', '15m']:
            if timeframe in all_results and all_results[timeframe]:
                best_rr = max(all_results[timeframe].items(), 
                             key=lambda x: x[1]['metrics']['total_return'])
                f.write(f"- **{timeframe.upper()}:** R/R {best_rr[0]} ")
                f.write(f"({best_rr[1]['metrics']['total_return']:.2f}% return)\n")
        f.write("\n")
        
        f.write("### Recommendations\n\n")
        f.write("1. **Conservative traders:** Use R/R ratios of 1.5-2.0 for higher win rates\n")
        f.write("2. **Aggressive traders:** Use R/R ratios of 3.0-5.0 for higher profit potential\n")
        f.write("3. **Balanced approach:** R/R ratios of 2.5-3.5 offer good risk-adjusted returns\n")
        f.write("4. **Best overall:** Based on the analysis, the optimal configuration provides the highest total return\n")
        f.write("5. **Consider Sharpe ratio:** Higher Sharpe ratios indicate better risk-adjusted returns\n\n")
    
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
    summary_df = summary_df.sort_values(['Timeframe', 'Risk_Reward_Ratio'])
    summary_df.to_csv(csv_path, index=False)
    print(f"CSV summary saved to: {csv_path}")


if __name__ == "__main__":
    main()

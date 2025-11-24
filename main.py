"""
Main Execution Script for FVG Trading Strategy Backtest
Run complete backtest analysis across multiple timeframes
"""

import os
import sys
from datetime import datetime
import warnings
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


def create_output_directory(output_dir='results'):
    """Create output directory if it doesn't exist"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")
    return output_dir


def run_backtest_for_timeframe(timeframe, start_year=2018, end_year=2024, 
                                initial_capital=10000, output_dir='results'):
    """
    Run complete backtest for a specific timeframe
    
    Parameters:
    -----------
    timeframe : str
        Timeframe to test ('1m', '5m', '15m')
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
    print(f"BACKTESTING {timeframe.upper()} TIMEFRAME")
    print(f"{'='*80}")
    
    # Step 1: Load Data
    print(f"\n[1/5] Loading data...")
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
    print(f"\n[2/5] Detecting FVG signals at 8:30 AM...")
    detector = FVGDetector()
    data_with_fvg = detector.detect_fvg(data, target_time='08:30:00')
    
    # Step 3: Run Backtest
    print(f"\n[3/5] Running backtest...")
    engine = BacktestEngine(initial_capital=initial_capital)
    trades_df = engine.run_backtest(data_with_fvg, timeframe)
    
    if trades_df is None or len(trades_df) == 0:
        print(f"No trades generated for {timeframe}")
        return None
    
    # Step 4: Calculate Performance Metrics
    print(f"\n[4/5] Calculating performance metrics...")
    perf = PerformanceMetrics(trades_df, initial_capital=initial_capital)
    metrics = perf.calculate_all_metrics()
    
    # Print summary
    print(f"\n{'='*60}")
    print(f"SUMMARY - {timeframe.upper()}")
    print(f"{'='*60}")
    print(f"Total Trades:        {metrics['total_trades']}")
    print(f"Winning Trades:      {metrics['winning_trades']}")
    print(f"Losing Trades:       {metrics['losing_trades']}")
    print(f"Win Rate:            {metrics['win_rate']:.2f}%")
    print(f"Total P&L:           ${metrics['total_pnl']:.2f}")
    print(f"Total Return:        {metrics['total_return']:.2f}%")
    print(f"Profit Factor:       {metrics['profit_factor']:.2f}")
    print(f"Sharpe Ratio:        {metrics['sharpe_ratio']:.2f}")
    print(f"Max Drawdown:        {metrics['max_drawdown']:.2f}%")
    print(f"Avg Win:             ${metrics['avg_win']:.2f}")
    print(f"Avg Loss:            ${metrics['avg_loss']:.2f}")
    print(f"{'='*60}")
    
    # Step 5: Generate Visualizations
    print(f"\n[5/5] Generating visualizations...")
    viz = Visualizer(trades_df, metrics, timeframe, output_dir=output_dir)
    viz.create_all_visualizations()
    
    return {
        'trades_df': trades_df,
        'metrics': metrics,
        'data': data_with_fvg
    }


def main():
    """Main execution function"""
    print("\n" + "="*80)
    print("FVG TRADING STRATEGY BACKTEST SYSTEM")
    print("="*80)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Configuration
    START_YEAR = 2018
    END_YEAR = 2024
    INITIAL_CAPITAL = 10000
    TIMEFRAMES = ['1m', '5m', '15m']
    OUTPUT_DIR = 'results'
    
    # Create output directory
    output_dir = create_output_directory(OUTPUT_DIR)
    
    # Store results for all timeframes
    all_results = {}
    
    # Run backtest for each timeframe
    for timeframe in TIMEFRAMES:
        result = run_backtest_for_timeframe(
            timeframe=timeframe,
            start_year=START_YEAR,
            end_year=END_YEAR,
            initial_capital=INITIAL_CAPITAL,
            output_dir=output_dir
        )
        
        if result:
            all_results[timeframe] = result
    
    # Generate comprehensive report
    if all_results:
        print(f"\n{'='*80}")
        print("GENERATING COMPREHENSIVE REPORT")
        print(f"{'='*80}")
        
        report_gen = ReportGenerator(all_results, output_dir=output_dir)
        report_gen.generate_markdown_report()
        report_gen.generate_html_report()
        
        # Save trades data to CSV
        for tf, result in all_results.items():
            trades_df = result['trades_df']
            csv_path = os.path.join(output_dir, f'trades_{tf}.csv')
            trades_df.to_csv(csv_path, index=False)
            print(f"Saved trades data to: {csv_path}")
    
    print(f"\n{'='*80}")
    print("BACKTEST COMPLETE")
    print(f"{'='*80}")
    print(f"Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"\nAll results saved to: {output_dir}/")
    print("\nGenerated files:")
    print("  - backtest_report.md (Markdown report)")
    print("  - backtest_report.html (HTML report)")
    for tf in TIMEFRAMES:
        if tf in all_results:
            print(f"  - trades_{tf}.csv (Trade data)")
            print(f"  - equity_curve_{tf}.png")
            print(f"  - drawdown_{tf}.png")
            print(f"  - trade_distribution_{tf}.png")
            print(f"  - performance_heatmap_{tf}.png")
    

if __name__ == "__main__":
    main()

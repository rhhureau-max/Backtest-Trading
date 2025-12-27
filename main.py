"""
Main entry point for running the backtesting system.
"""

import sys
import warnings
warnings.filterwarnings('ignore')

# Add src directory to path
sys.path.insert(0, 'src')

from data_loader import DataLoader
from backtester import Backtester
from strategies.judas_swing import JudasSwingStrategy
from strategies.orb_retest import ORBRetestStrategy
from strategies.htf_trend import HTFTrendContinuationStrategy
from report import StrategyReport
import config


def main():
    """
    Main function to run all three strategies and generate reports.
    """
    print("="*80)
    print("NQ FUTURES BACKTEST - LONDON SESSION")
    print("="*80)
    print(f"Session Hours: {config.LONDON_SESSION_START} - {config.LONDON_SESSION_END} Paris Time")
    print(f"Spread: {config.SPREAD_POINTS} points per trade")
    print(f"Max Trades per Day: 1 (first valid signal only)")
    print(f"Years: {min(config.YEARS)} - {max(config.YEARS)}")
    print("="*80)
    
    # 1. Load data
    print("\nStep 1: Loading data...")
    loader = DataLoader(config.DATA_DIR)
    
    # Load multiple timeframes
    timeframes_to_load = ['5m', '15m', '1D']
    data = loader.load_multiple_timeframes(timeframes_to_load, config.YEARS)
    
    print(f"  Loaded timeframes: {list(data.keys())}")
    for tf, df in data.items():
        print(f"    {tf}: {len(df)} candles from {df.index[0]} to {df.index[-1]}")
    
    # 2. Initialize strategies
    print("\nStep 2: Initializing strategies...")
    strategies = [
        JudasSwingStrategy(spread_points=config.SPREAD_POINTS),
        ORBRetestStrategy(spread_points=config.SPREAD_POINTS),
        HTFTrendContinuationStrategy(spread_points=config.SPREAD_POINTS)
    ]
    
    for strategy in strategies:
        print(f"  - {strategy.name}")
    
    # 3. Run backtests
    print("\nStep 3: Running backtests...")
    print("-"*80)
    
    for strategy in strategies:
        backtester = Backtester(strategy)
        trades = backtester.run(data)
        print(f"  {strategy.name}: {len(trades)} trades executed")
    
    # 4. Generate reports
    print("\nStep 4: Generating reports...")
    print("-"*80)
    
    report_generator = StrategyReport(strategies)
    
    # Print comparison report
    report_generator.print_comparison_report()
    
    # Print detailed reports for each strategy
    for strategy in strategies:
        report_generator.print_detailed_report(strategy.name)
    
    # Print KPI recommendations
    print("="*80)
    print(report_generator.generate_kpi_recommendations())
    
    # 5. Save results to CSV
    print("\nStep 5: Saving results to CSV...")
    comparison_df = report_generator.generate_comparison_report()
    comparison_df.to_csv('strategy_comparison.csv', index=False)
    print("  Saved: strategy_comparison.csv")
    
    # Save individual strategy trades
    for strategy in strategies:
        backtester = Backtester(strategy)
        trades_df = backtester.get_trades_dataframe()
        
        if not trades_df.empty:
            filename = f"{strategy.name.lower().replace(' ', '_')}_trades.csv"
            trades_df.to_csv(filename, index=False)
            print(f"  Saved: {filename}")
    
    print("\n" + "="*80)
    print("BACKTEST COMPLETE!")
    print("="*80)


if __name__ == "__main__":
    main()

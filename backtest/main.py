"""
Main entry point for the backtest strategy.

Run this script with: python backtest/main.py
"""
import os
import sys
import logging
from datetime import datetime

# Add backtest directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import BacktestConfig, DEFAULT_CONFIG
from data_loader import DataLoader
from strategy import Strategy
from metrics import calculate_metrics, generate_results_markdown


def setup_logging(level: str = "INFO"):
    """Configure logging for the backtest."""
    # Set root logger to WARNING to suppress verbose messages from FVG detector
    logging.basicConfig(
        level=logging.WARNING,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    # Set main module logger to INFO for progress messages
    logging.getLogger(__name__).setLevel(getattr(logging, level.upper()))
    logging.getLogger('strategy').setLevel(getattr(logging, level.upper()))
    logging.getLogger('data_loader').setLevel(getattr(logging, level.upper()))


def main():
    """Main function to run the backtest."""
    # Setup logging
    config = DEFAULT_CONFIG
    setup_logging("INFO")  # Always show INFO for main progress
    
    logger = logging.getLogger(__name__)
    print("=" * 60)
    print("FVG + Liquidity Sweep Backtest Strategy")
    print("=" * 60)
    
    # Determine data directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, config.data_dir)
    data_dir = os.path.abspath(data_dir)
    
    print(f"\nData directory: {data_dir}")
    print(f"Backtest period: {config.start_year} to {config.end_year}")
    print(f"Risk/Reward ratio: 1:{config.risk_reward_ratio}")
    
    # Load data
    print("\n--- Loading Data ---")
    try:
        loader = DataLoader(data_dir, config.start_year, config.end_year)
        data = loader.get_all_data()
        
        h1_data = data['H1']
        m15_data = data['M15']
        m5_data = data['M5']
        
        print(f"H1 data: {len(h1_data)} candles from {h1_data.index.min()} to {h1_data.index.max()}")
        print(f"M15 data: {len(m15_data)} candles from {m15_data.index.min()} to {m15_data.index.max()}")
        print(f"M5 data: {len(m5_data)} candles from {m5_data.index.min()} to {m5_data.index.max()}")
        
    except Exception as e:
        print(f"ERROR: Failed to load data: {e}")
        raise
    
    # Run backtest
    print("\n--- Running Backtest ---")
    print("(This may take several minutes...)")
    strategy = Strategy(config)
    
    start_time = datetime.now()
    trades = strategy.run_backtest(h1_data, m15_data, m5_data)
    end_time = datetime.now()
    
    duration = (end_time - start_time).total_seconds()
    print(f"Backtest completed in {duration:.2f} seconds")
    
    # Calculate metrics
    print("\n--- Calculating Metrics ---")
    closed_trades = strategy.get_closed_trades()
    metrics = calculate_metrics(closed_trades)
    
    # Print summary to console
    print("\n" + "=" * 60)
    print("BACKTEST RESULTS SUMMARY")
    print("=" * 60)
    print(f"Total Trades: {metrics.total_trades}")
    print(f"Winning Trades: {metrics.winning_trades}")
    print(f"Losing Trades: {metrics.losing_trades}")
    print(f"Win Rate: {metrics.win_rate:.2f}%")
    print(f"Profit Factor: {metrics.profit_factor:.2f}")
    print(f"Net Profit: {metrics.net_profit:.2f}R")
    print(f"Max Drawdown: {metrics.max_drawdown:.2f}R")
    print(f"Average R:R: {metrics.avg_rr:.2f}")
    
    # Generate results markdown
    print("\n--- Generating Results Report ---")
    results_md = generate_results_markdown(metrics, trades)
    
    # Save results to file
    results_path = os.path.join(script_dir, "..", "backtest_results.md")
    results_path = os.path.abspath(results_path)
    
    with open(results_path, 'w') as f:
        f.write(results_md)
    
    print(f"Results saved to: {results_path}")
    print("\nBacktest complete!")
    
    return metrics


if __name__ == "__main__":
    main()

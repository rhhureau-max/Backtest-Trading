"""
Quick demo script to test the backtesting system with a smaller dataset.
This is useful for quick testing and understanding how the system works.
"""
from data_loader import DataLoader
from strategy import FVGStrategy
from backtest import Backtest
from visualization import Visualizer


def demo():
    """Run a demo backtest with limited data."""
    
    print("="*60)
    print("NQ FVG BACKTESTING SYSTEM - DEMO")
    print("="*60)
    print("\nLoading data for 2024-2025 only (faster demo)...\n")
    
    # Configuration
    START_YEAR = 2024
    END_YEAR = 2025
    SESSION_START_HOUR = 2
    SESSION_END_HOUR = 6
    RISK_REWARD_RATIO = 1.0
    SWING_LOOKBACK = 5
    INITIAL_CAPITAL = 100000
    
    # Load and prepare data
    loader = DataLoader(data_directory=".")
    df = loader.load_data(start_year=START_YEAR, end_year=END_YEAR)
    df = loader.filter_trading_session(df, start_hour=SESSION_START_HOUR, end_hour=SESSION_END_HOUR)
    df = loader.add_session_markers(df)
    
    # Initialize strategy and detect signals
    strategy = FVGStrategy(risk_reward_ratio=RISK_REWARD_RATIO, swing_lookback=SWING_LOOKBACK)
    df = strategy.detect_fvg(df)
    df = strategy.get_first_fvg_per_session(df)
    df = strategy.check_fvg_fill_and_reversal(df)
    
    print(f"\nFVGs detected: {df['fvg_type'].notna().sum()}")
    print(f"Entry signals: {df['entry_signal'].notna().sum()}")
    
    # Run backtest
    backtest = Backtest(strategy, initial_capital=INITIAL_CAPITAL)
    trades = backtest.run(df)
    
    # Show results
    backtest.print_statistics()
    
    # Generate visualizations
    if trades:
        visualizer = Visualizer()
        visualizer.plot_equity_curve(trades, INITIAL_CAPITAL, 'demo_equity_curve.png')
        visualizer.plot_trade_distribution(trades, 'demo_trade_distribution.png')
        print(f"\nDemo charts saved:")
        print("  - demo_equity_curve.png")
        print("  - demo_trade_distribution.png")
    
    print("\nDemo complete! To run the full backtest, use: python main.py")


if __name__ == "__main__":
    demo()

"""
Main entry point for the NQ FVG Backtesting System.
"""
import os
from data_loader import DataLoader
from strategy import FVGStrategy
from backtest import Backtest
from visualization import Visualizer


def main():
    """Run the complete backtesting system."""
    
    print("="*60)
    print("NQ FAIR VALUE GAP BACKTESTING SYSTEM")
    print("="*60)
    print()
    
    # Configuration parameters (easily adjustable)
    START_YEAR = 2018
    END_YEAR = 2025
    SESSION_START_HOUR = 2
    SESSION_START_MINUTE = 0
    SESSION_END_HOUR = 6
    SESSION_END_MINUTE = 0
    RISK_REWARD_RATIO = 1.0
    SWING_LOOKBACK = 5
    INITIAL_CAPITAL = 100000
    DATA_DIRECTORY = "."
    
    print("Configuration:")
    print(f"  Period: {START_YEAR} - {END_YEAR}")
    print(f"  Trading Session: {SESSION_START_HOUR:02d}:{SESSION_START_MINUTE:02d} - {SESSION_END_HOUR:02d}:{SESSION_END_MINUTE:02d}")
    print(f"  Risk/Reward Ratio: {RISK_REWARD_RATIO}:1")
    print(f"  Swing Lookback: {SWING_LOOKBACK} candles")
    print(f"  Initial Capital: ${INITIAL_CAPITAL:,.2f}")
    print()
    
    # Step 1: Load data
    print("Step 1: Loading data...")
    print("-" * 60)
    loader = DataLoader(data_directory=DATA_DIRECTORY)
    df = loader.load_data(start_year=START_YEAR, end_year=END_YEAR)
    print()
    
    # Step 2: Filter to trading session
    print("Step 2: Filtering to trading session...")
    print("-" * 60)
    df = loader.filter_trading_session(
        df, 
        start_hour=SESSION_START_HOUR,
        start_minute=SESSION_START_MINUTE,
        end_hour=SESSION_END_HOUR,
        end_minute=SESSION_END_MINUTE
    )
    print()
    
    # Step 3: Add session markers
    print("Step 3: Adding session markers...")
    print("-" * 60)
    df = loader.add_session_markers(df)
    print()
    
    # Step 4: Initialize strategy
    print("Step 4: Initializing strategy...")
    print("-" * 60)
    strategy = FVGStrategy(
        risk_reward_ratio=RISK_REWARD_RATIO,
        swing_lookback=SWING_LOOKBACK
    )
    print("Strategy initialized")
    print()
    
    # Step 5: Detect FVGs
    print("Step 5: Detecting Fair Value Gaps...")
    print("-" * 60)
    df = strategy.detect_fvg(df)
    total_fvgs = df['fvg_type'].notna().sum()
    bearish_fvgs = (df['fvg_type'] == 'bearish').sum()
    bullish_fvgs = (df['fvg_type'] == 'bullish').sum()
    print(f"Total FVGs detected: {total_fvgs}")
    print(f"  Bearish FVGs: {bearish_fvgs}")
    print(f"  Bullish FVGs: {bullish_fvgs}")
    print()
    
    # Step 6: Identify first FVG per session
    print("Step 6: Identifying first FVG per session...")
    print("-" * 60)
    df = strategy.get_first_fvg_per_session(df)
    first_fvgs = df['first_fvg_of_session'].sum()
    print(f"First FVGs per session: {first_fvgs}")
    print()
    
    # Step 7: Check for FVG fill and reversal signals
    print("Step 7: Checking for entry signals...")
    print("-" * 60)
    df = strategy.check_fvg_fill_and_reversal(df)
    total_signals = df['entry_signal'].notna().sum()
    long_signals = (df['entry_signal'] == 'long').sum()
    short_signals = (df['entry_signal'] == 'short').sum()
    print(f"Total entry signals: {total_signals}")
    print(f"  LONG signals: {long_signals}")
    print(f"  SHORT signals: {short_signals}")
    print()
    
    # Step 8: Run backtest
    print("Step 8: Running backtest...")
    print("-" * 60)
    backtest = Backtest(strategy, initial_capital=INITIAL_CAPITAL)
    trades = backtest.run(df)
    print()
    
    # Step 9: Calculate and display statistics
    print("Step 9: Calculating performance statistics...")
    print("-" * 60)
    backtest.print_statistics()
    
    # Step 10: Export results
    print("Step 10: Exporting results...")
    print("-" * 60)
    backtest.export_trades('trade_journal.csv')
    print()
    
    # Step 11: Generate visualizations
    print("Step 11: Generating visualizations...")
    print("-" * 60)
    visualizer = Visualizer()
    
    if trades:
        visualizer.plot_equity_curve(trades, INITIAL_CAPITAL, 'equity_curve.png')
        visualizer.plot_trade_distribution(trades, 'trade_distribution.png')
        visualizer.plot_monthly_returns(trades, 'monthly_returns.png')
        visualizer.plot_sample_trades(df, trades, num_trades=min(10, len(trades)), filename='sample_trades.png')
    else:
        print("No trades to visualize.")
    print()
    
    print("="*60)
    print("BACKTEST COMPLETE!")
    print("="*60)
    print()
    print("Generated files:")
    print("  - trade_journal.csv (detailed trade log)")
    print("  - equity_curve.png (equity over time)")
    print("  - trade_distribution.png (trade statistics)")
    print("  - monthly_returns.png (monthly P&L)")
    print("  - sample_trades.png (sample trade charts)")
    print()


if __name__ == "__main__":
    main()
